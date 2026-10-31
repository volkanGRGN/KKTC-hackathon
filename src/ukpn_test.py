#!/usr/bin/env python3
"""Faz 3 doğrulama: ev ev yük akışının gerilim hesabı İngiltere UKPN verisinde (yaz 2014, 1 dakika).

Soru: bizim solve() (trafo_bos_kapasite.py) hat ucundaki evin gerilimini, trafo çıkışından
ne kadar yükseldiğini doğru büyüklükte hesaplıyor mu? Taşınan şey fizik (direnç, akım, nötr),
rakam değil: İngiltere 230 V / 253 V, yeraltı Al kablo; Kıbrıs kurgusu bunlara uygulanmaz.

Veri: UK Power Networks "Validation of PV Connection Assessment Tool" (CC BY 4.0), KAYNAK.txt.
Klasör yapısı: <veri>/acik/csv/2014-11-28 Cleansed and Processed/EXPORT OneMinData|TenMinData/...,
<veri>/indirilen/Weather_Data_2014-11-30.xlsx. Zaman damgaları GMT (PV tepesi 11:00–13:00 arası
ortalanıyor [Hesap]); pencereler damgaya göre.

Adımlar:
1. Hat ucu evin fideri ve fazı: ev−bara gerilim farkının fider faz gücüyle en güçlü (eksi)
   ilişkisi. Rapor Tablo 14'teki faz ile karşılaştırılır.
2. Ölçülen: ΔV = ev V − bara V (aynı faz, aynı dakika; bara = fiderin trafo çıkışındaki cihazı).
   Cihazlar arası ölçüm farkı (±%0,5) sabit kaydırma yaratır; yükselme her gün gece (00–04)
   ortancasına göre alınır.
3. Model: tek fider, DUGUM düğüm eşit aralıklı, ev en uçta. v0 = ölçülen bara gerilimi (trafo
   empedansı devre dışı, bara zaten ölçülü). Ev = ölçülen net güç; diğer yük = fiderin ölçülen
   faz gücü − ev, o fazın düğümlerine eşit [Yorum]. Hat boyu BULAMADIM, bu yüzden:
   (a) akşam 17–21 dakikalarından (yük kaynaklı düşüm, PV yok) etkin boy kestirilir;
   (b) bu boyla öğlen PV kaynaklı yükselme hesaplanır, UKPN'in tanımıyla: Haz–Ağu 11–13,
       ΔV'nin evin birim üretimine eğimi; model÷ölçülen. Boy öğlen verisini görmez.
   (c) ayrıca 150–450 m boy bandında aynı eğim (boy kestirimi olmadan).
   (d) güneşli günlerde öğlen − gece seviyesi; panelin hat üstündeki yerine duyarlı.
4. Çapraz sağlamalar (modelsiz): bara gerilimi dağılımı, müşteri başına gündüz en düşük talep,
   akşam faz dengesizliği.

Çalıştırma (sanal ortam: pandas, numpy, openpyxl; ~30 saniye):
    python3 src/ukpn_test.py data/raw/ukpn-pv-dogrulama ukpn_sonuc.csv
Çıktı: özet csv (bölüm, site, ölçü, değer, birim, etiket) + yanına <ad>_dakika.csv (güneşli
günlerin gece / öğlen / akşam dakikaları, ölçülen ve model ΔV).
"""
import csv
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Eski benzetim içe alınırken komut satırından tohum okuyor; bizim argümanlarımız ona karışmasın.
_argv, sys.argv = sys.argv, sys.argv[:1]
import trafo_bos_kapasite as tb  # noqa: E402
sys.argv = _argv

KLASOR = Path('acik') / 'csv' / '2014-11-28 Cleansed and Processed'
HAVA = Path('indirilen') / 'Weather_Data_2014-11-30.xlsx'
BIR_DK = ('2014-06-19', '2014-09-07')       # tam 1 dk günler (18 Haz ve 7 Eyl yarım) [Kaynaklı: veri]
GUNESLI_GUN = 12
OGLE, GECE, AKSAM = (11, 13), (0, 4), (17, 21)   # saat aralıkları, GMT
DUGUM = 30                                  # ev dışı yük düğümü (10 / faz) [Yorum]; 9 / 90 düğümde oran ±%13 [Hesap]
BOY_M = (150, 300, 450)                     # hat boyu bandı, m [Yorum: BULAMADIM; bizim şehir konutu 150–450]
FAZ = 'ABC'

# Hat ucu evli altı site. musteri, pv_kw [Kaynaklı: kapanış raporu Tablo 3 s.17];
# ev_pv_kw: cihaz listesindeki görünen panel gücü [Kaynaklı: deviceListTable];
# kablo: veri notlarındaki "LV CableType" [Kaynaklı: Dataset Notes]; boşsa BULAMADIM;
# rapor_faz / rapor_v_pu: Tablo 14 "Rise along LV feeder" [Kaynaklı: rapor s.50].
SITELER = {
    'Alverston Close':  dict(musteri=655, pv_kw=80, ev_pv_kw=3.0, kablo='185 Al', rapor_faz='C', rapor_v_pu=2.13),
    'Bancroft Close':   dict(musteri=226, pv_kw=60, ev_pv_kw=3.5, kablo=None, rapor_faz='C', rapor_v_pu=1.13),
    'Forest Road':      dict(musteri=167, pv_kw=117, ev_pv_kw=3.0, kablo=None, rapor_faz='A', rapor_v_pu=1.07),
    'Maple Drive East': dict(musteri=147, pv_kw=77, ev_pv_kw=4.0, kablo='120 Al', rapor_faz='C', rapor_v_pu=2.92),
    'Suffolk Road':     dict(musteri=394, pv_kw=37, ev_pv_kw=0.5, kablo='0.2 in2 Cu', rapor_faz='A', rapor_v_pu=0.78),
    'YMCA':             dict(musteri=80, pv_kw=35, ev_pv_kw=0.45, kablo='185 Al', rapor_faz='C', rapor_v_pu=1.03),
}
# Faz iletkeni Ω/km, 20 °C: IEC 60228 sınıf 2 en yüksek DC direnç
# [Kaynaklı: https://mycableengineering.com/conductor-resistance/]. 0,2 in² Cu = 129 mm² →
# 0,153 × 120/129 [Hesap]. Nötr = faz (Waveform/CNE eş kesitli nötr) [Yorum]. X 0,075 Ω/km [Yorum].
# Kablosu bilinmeyen site: 95–300 mm² Al bandı, orta 185 [Yorum].
KABLO_R = {'95 Al': 0.320, '120 Al': 0.253, '185 Al': 0.164, '300 Al': 0.100, '0.2 in2 Cu': 0.142}
X_KM = 0.075
# Kırsal = direk tipi trafo [Kaynaklı: Dataset Notes "Type"]; kalanı kentsel/banliyö.
KIRSAL = {'Chapel Lane', 'Old Mill', 'Priesthawes', 'Upper Staplefield Common', 'Bircham Newton',
          'Warninglid Lane'}


# ---------- okuma ----------

def oku_musteri(veri):
    c = pd.read_csv(veri / KLASOR / 'EXPORT OneMinData' / 'EXPORT OneMinData - Customer Endpoints.csv',
                    usecols=['Substation', 'datetime', 'V_Filtered', 'P_GEN', 'P_IMPORT', 'Q_IMPORT'],
                    encoding='utf-8')
    c = c[(c.datetime >= BIR_DK[0]) & (c.datetime < BIR_DK[1])].copy()
    c['datetime'] = pd.to_datetime(c.datetime)
    return c


def oku_fider(veri):
    """1 dk fider cihazları (trafo çıkışı), bütün siteler, 1 dk dönemi."""
    sut = ['Substation', 'To', 'datetime', 'VA_Filtered', 'VB_Filtered', 'VC_Filtered',
           'PA', 'PB', 'PC', 'QA', 'QB', 'QC']
    parca = []
    for ch in pd.read_csv(veri / KLASOR / 'EXPORT OneMinData' / 'EXPORT OneMinData - Feeders.csv',
                          usecols=sut, chunksize=2_000_000, encoding='utf-8',
                          dtype={'Substation': str, 'To': str, 'datetime': str}):
        parca.append(ch[(ch.datetime >= BIR_DK[0]) & (ch.datetime < BIR_DK[1])])
    f = pd.concat(parca, ignore_index=True)
    f['datetime'] = pd.to_datetime(f.datetime)
    f['To'] = f.To.str.strip()
    return f


def gunesli_gunler(veri, gunler):
    """Beş hava istasyonunun günlük ışınım enerjisi ortalamasına göre en güneşli günler."""
    h = pd.read_excel(veri / HAVA, sheet_name='Weather Data', usecols=['Site', 'Date', 'SolarEnergy'])
    h['gun'] = pd.to_datetime(h.Date).dt.normalize()
    h['SolarEnergy'] = pd.to_numeric(h.SolarEnergy, errors='coerce')      # eksik kayıt '---'
    h = h[h.gun.isin(gunler)]
    g = h.groupby(['gun', 'Site']).SolarEnergy.sum().unstack('Site')
    g = g[g.notna().sum(axis=1) >= 4].mean(axis=1).sort_values(ascending=False)
    return list(g.index[:GUNESLI_GUN]), g


# ---------- 1. eşleşme ----------

def eslestir(site, ev, fid):
    """Ev−bara farkını en çok açıklayan (fider, faz): fider faz gücüyle en eksi korelasyon."""
    fs = fid[fid.Substation == site]
    en = None
    for to, g in fs.groupby('To'):
        j = ev.join(g.drop(columns=['Substation', 'To']).groupby('datetime').mean(), how='inner')
        for ph in FAZ:
            r = (j.V_Filtered - j[f'V{ph}_Filtered']).corr(j[f'P{ph}'])
            if en is None or r < en[2]:
                en = (to, ph, r)
    return en


# ---------- 3. model ----------

def kur(boy_m, r_km, faz_ev):
    """Tek fider: DUGUM yük düğümü (A,B,C sırayla) + uçta ev; eşit aralıklı."""
    n = DUGUM + 1
    z = complex(r_km, X_KM) * boy_m / 1000 / n
    evler = [dict(id=k, ph=k % 3) for k in range(DUGUM)] + [dict(id='ev', ph=faz_ev)]
    return dict(v0=230.0, zt=0j, feeders=[dict(zs=z, zn=z, houses=evler)])


def model_dv(tr, df, faz_ev, dengeli=False):
    """Her dakika için modelin ev gerilimi − bara gerilimi (V). dengeli: fiderin faz faz ölçümü
    yokmuş gibi, ev dışı yük üç faza eşit (Kıbrıs'ta faz bilgisi olmayacak)."""
    say = [sum(1 for k in range(DUGUM) if k % 3 == p) for p in range(3)]
    out, warm = [], None
    for s in df[MODEL_SUT].to_dict('records'):
        pe, qe = s['P_IMPORT'] * 1000, s['Q_IMPORT'] * 1000
        net = {'ev': (pe, qe)}
        for p in range(3):
            if dengeli:
                kp = (s['PA'] + s['PB'] + s['PC']) * 1000 / 3 - pe / 3
                kq = (s['QA'] + s['QB'] + s['QC']) * 1000 / 3 - qe / 3
            else:
                kp = s[f'P{FAZ[p]}'] * 1000 - (pe if p == faz_ev else 0)
                kq = s[f'Q{FAZ[p]}'] * 1000 - (qe if p == faz_ev else 0)
            for k in range(p, DUGUM, 3):
                net[k] = (kp / say[p], kq / say[p])
        tr['v0'] = s['bara']
        V, _ = tb.solve(tr, net, 1.0, warm, iters=4 if warm else 6)
        warm = V
        v = V[0][-1]
        out.append(abs(v[faz_ev] - v[3]) - s['bara'])
    return pd.Series(out, index=df.index)


MODEL_SUT = ['bara', 'P_IMPORT', 'Q_IMPORT', 'PA', 'PB', 'PC', 'QA', 'QB', 'QC']


def seviye(j, gunler, tr, faz_ev):
    """Seçili günlerin gece / öğlen / akşam dakikaları; ölçülen ve model ΔV, aynı günün gece
    ortancasına göre (yuk_olc, yuk_mod)."""
    g = j[j.index.normalize().isin(gunler)].copy()
    sa = g.index.hour
    g['pencere'] = np.select([(sa >= GECE[0]) & (sa < GECE[1]), (sa >= OGLE[0]) & (sa < OGLE[1]),
                              (sa >= AKSAM[0]) & (sa < AKSAM[1])], ['gece', 'ogle', 'aksam'], '')
    g = g[g.pencere != '']
    g['dv_model'] = model_dv(tr, g, faz_ev)
    gece = g[g.pencere == 'gece']
    ref = gece.groupby(gece.index.normalize())[['dv', 'dv_model']].median().reindex(g.index.normalize())
    g['yuk_olc'] = g.dv - ref.dv.values
    g['yuk_mod'] = g.dv_model - ref.dv_model.values
    return g


def egim(x, y):
    """En küçük kareler: eğim, kesişim, R²."""
    a = np.polyfit(x, y, 1)
    r = np.corrcoef(x, y)[0, 1]
    return a[0], a[1], r * r


# ---------- 4. çapraz sağlamalar ----------

def bara_dagilimi(veri, sonuc):
    s = pd.read_csv(veri / KLASOR / 'EXPORT TenMinData' / 'EXPORT TenMinData - Substation Voltages.csv',
                    encoding='utf-8')
    s['datetime'] = pd.to_datetime(s.datetime)
    uzun = s.melt(id_vars=['Substation', 'datetime'],
                  value_vars=['Substation_VA_Filtered', 'Substation_VB_Filtered', 'Substation_VC_Filtered'],
                  value_name='V').dropna()
    saat, ay = uzun.datetime.dt.hour, uzun.datetime.dt.month
    pencereler = {'gece 00-05 (en düşük yük)': saat < 5,
                  'öğlen 11-13 Haz-Ağu (PV tepesi)': saat.between(11, 12) & ay.between(6, 8),
                  'bütün saatler': saat >= 0}
    for ad, m in pencereler.items():
        v = uzun.V[m]
        for olcu, deger in [('ortanca', v.median()), ('ss', v.std()), ('P84', v.quantile(0.84)),
                            ('P99', v.quantile(0.99)), ('ortanca+1ss', v.median() + v.std())]:
            sonuc.append(('capraz_bara', ad, olcu, round(deger, 2), 'V', '[Hesap]'))
        sonuc.append(('capraz_bara', ad, 'site_sayisi', uzun.Substation[m].nunique(), 'site', '[Hesap]'))
    site_ort = uzun[pencereler['öğlen 11-13 Haz-Ağu (PV tepesi)']].groupby('Substation').V.median()
    sonuc.append(('capraz_bara', 'site ortancaları öğlen', 'en_dusuk', round(site_ort.min(), 1), 'V', '[Hesap]'))
    sonuc.append(('capraz_bara', 'site ortancaları öğlen', 'en_yuksek', round(site_ort.max(), 1), 'V', '[Hesap]'))


def en_dusuk_talep(fid, mus, gunler, sonuc):
    """Müşteri başına gündüz (10–16) en düşük 30 dk talep. Fider net + PV tahmini (site PV kW ×
    izlenen evin birim üretimi) = brüt [Yorum]. PV'siz iki site düzeltmesiz."""
    pvsiz = {'Upper Staplefield Common': 27, 'Rampling Court': 27}   # [Kaynaklı: Tablo 3]
    # Cihaz listesindeki fiderlerin hepsi 1 dk veride yoksa müşteri başına değer alt sınırdır.
    KAPSAM = {'YMCA': '4 fiderden 2si izli: alt sınır, kullanılmaz', 'Forest Road': '4 fiderden 3ü izli: alt sınır',
              'Rampling Court': 'müşteriler apartman blokları: ev değil, kullanılmaz'}
    gun = fid[fid.datetime.dt.normalize().isin(gunler)]
    for site in list(SITELER) + list(pvsiz):
        fs = gun[gun.Substation == site]
        top = fs.groupby('datetime')[['PA', 'PB', 'PC']].sum().sum(axis=1)
        if site in SITELER:
            a = SITELER[site]
            pu = mus[mus.Substation == site].set_index('datetime').P_GEN.clip(lower=0) / a['ev_pv_kw']
            top = (top + a['pv_kw'] * pu.reindex(top.index)).dropna()
            n = a['musteri']
        else:
            n = pvsiz[site]
        y = top.resample('30min').mean()
        y = y[(y.index.hour >= 10) & (y.index.hour < 16)]
        gunluk_min = y.groupby(y.index.normalize()).min() / n * 1000
        not_ = KAPSAM.get(site, 'bütün fiderler izli')
        sonuc.append(('capraz_talep', site, 'gunduz_min_W_musteri_ortanca', round(gunluk_min.median()), 'W',
                      ('[Hesap]' if site in pvsiz else '[Hesap+Yorum: PV tahmini eklendi]') + f'; {not_}'))


def faz_dengesizligi(fid, sonuc):
    """Akşam 17–20 ortalama faz yükü; dengesizlik = (en büyük − ortalama) / ortalama (rapor Tablo 11
    örneği: 30 kW → 12,5/8,75/8,75 = %25)."""
    a = fid[fid.datetime.dt.hour.between(17, 19)]
    g = a.groupby(['Substation', 'To', a.datetime.dt.normalize()])[['PA', 'PB', 'PC']].mean()
    g = g[(g > 0).all(axis=1)]
    ort = g.mean(axis=1)
    d = (g.max(axis=1) - ort) / ort * 100
    kir = d.index.get_level_values('Substation').isin(KIRSAL)
    for ad, m in [('kentsel, fider-gün', ~kir), ('kırsal, fider-gün', kir)]:
        x = d[m]
        for olcu, deger in [('ortanca', x.median()), ('ss', x.std()), ('P84', x.quantile(0.84)),
                            ('adet', len(x))]:
            sonuc.append(('capraz_faz', ad, olcu, round(deger, 1), '%' if olcu != 'adet' else 'adet', '[Hesap]'))
    # Fider başına bütün dönemin akşam ortalaması (günlük oynama ortalanır)
    gf = a.groupby(['Substation', 'To'])[['PA', 'PB', 'PC']].mean()
    gf = gf[(gf > 0).all(axis=1)]
    of = gf.mean(axis=1)
    df = (gf.max(axis=1) - of) / of * 100
    kf = df.index.get_level_values('Substation').isin(KIRSAL)
    for ad, m in [('kentsel, fider', ~kf), ('kırsal, fider', kf)]:
        x = df[m]
        for olcu, deger in [('ortanca', x.median()), ('ss', x.std()), ('P84', x.quantile(0.84)), ('adet', len(x))]:
            sonuc.append(('capraz_faz', ad, olcu, round(deger, 1), '%' if olcu != 'adet' else 'adet', '[Hesap]'))
    # Bizim üretici: trafo başına faz ağırlığı U(0,8; 1,2), ev fazı bu ağırlıkla rastgele
    # (sehir_uret.py); hat başına 10–40 ev [Hesap: aynı kuralın Monte Carlo'su, ev sayısıyla].
    rng = random.Random(1)
    biz = []
    for _ in range(4000):
        w = [rng.uniform(0.8, 1.2) for _ in range(3)]
        n = rng.randint(10, 40)
        say = [0, 0, 0]
        for _ in range(n):
            say[rng.choices([0, 1, 2], weights=w)[0]] += 1
        biz.append((max(say) - n / 3) / (n / 3) * 100)
    biz = pd.Series(biz)
    for olcu, deger in [('ortanca', biz.median()), ('P84', biz.quantile(0.84))]:
        sonuc.append(('capraz_faz', 'bizim üretici (ev sayısı)', olcu, round(deger, 1), '%', '[Hesap]'))


# ---------- ana akış ----------

def main():
    veri, cikti = Path(sys.argv[1]), Path(sys.argv[2])
    print('okunuyor...', flush=True)
    mus = oku_musteri(veri)
    fid = oku_fider(veri)
    gunler_tum = sorted(mus.datetime.dt.normalize().unique())
    gunler, sira = gunesli_gunler(veri, gunler_tum)
    bulutlu = list(sira.index[-GUNESLI_GUN:])
    sonuc = [('gunler', 'hepsi', 'gunesli_gunler', ' '.join(d.strftime('%m-%d') for d in sorted(gunler)), '',
              '[Hesap: 5 istasyon ışınım ortalaması, ilk 12]'),
              ('gunler', 'hepsi', 'bulutlu_gunler', ' '.join(d.strftime('%m-%d') for d in sorted(bulutlu)), '',
               '[Hesap: son 12]')]
    dakika = []
    for site, a in SITELER.items():
        ev = mus[mus.Substation == site].drop(columns='Substation').groupby('datetime').mean()
        to, ph, r = eslestir(site, ev, fid)
        p = FAZ.index(ph)
        sonuc += [('yapi', site, 'fider', to, '', f'[Hesap: r={r:.2f}]'),
                  ('yapi', site, 'faz', ph, '', f'[Hesap]; rapor Tablo 14: {a["rapor_faz"]}')]
        fs = fid[(fid.Substation == site) & (fid.To == to)].drop(columns=['Substation', 'To'])
        j = ev.join(fs.groupby('datetime').mean(), how='inner')
        j['bara'] = j[f'V{ph}_Filtered']
        j['dv'] = j.V_Filtered - j.bara
        j = j.dropna(subset=['dv', 'P_GEN', 'P_IMPORT', 'Q_IMPORT', 'PA', 'PB', 'PC', 'QA', 'QB', 'QC'])
        saat = j.index.hour
        r_orta = KABLO_R[a['kablo'] or '185 Al']
        rler = [KABLO_R[a['kablo']]] if a['kablo'] else [KABLO_R['300 Al'], KABLO_R['185 Al'], KABLO_R['95 Al']]
        L_ref = BOY_M[1]

        # (a) Akşam 17–21, bütün 1 dk günleri: yük kaynaklı düşümden etkin boy. Öğlen verisini görmez.
        ak = j[(saat >= AKSAM[0]) & (saat < AKSAM[1])]
        k, c, r2_ak = egim(model_dv(kur(L_ref, r_orta, p), ak, p), ak.dv)
        L_etkin = k * L_ref
        sonuc += [('model_aksam', site, 'etkin_boy_m', round(L_etkin), 'm',
                   f'[Hesap: akşam ΔV = c + k·model, R²={r2_ak:.2f}; kablo {a["kablo"] or "185 Al [Yorum]"}]'),
                  ('model_aksam', site, 'cihaz_farki_c', round(c, 2), 'V', '[Hesap: kesişim; ev ve bara cihazı farkı + modelin karşılamadığı sabit]')]

        # (b) UKPN yöntemi: Haz–Ağu 11–13, bütün günler; ΔV'nin evin birim PV üretimine eğimi.
        og = j[(saat >= OGLE[0]) & (saat < OGLE[1]) & (j.index.month <= 8)]
        pu = og.P_GEN / a['ev_pv_kw']
        e_olc, _, r2 = egim(pu, og.dv)
        m_og = model_dv(kur(L_etkin, r_orta, p), og, p)
        e_mod, _, _ = egim(pu, m_og)
        e_den, _, _ = egim(pu, model_dv(kur(L_etkin, r_orta, p), og, p, dengeli=True))
        _, _, r2_og = egim(m_og, og.dv)
        sonuc += [('olculen', site, 'egim_V_pu', round(e_olc, 2), 'V/pu', f'[Hesap]; rapor Tablo 14: {a["rapor_v_pu"]}'),
                  ('olculen', site, 'egim_V_kW_ev_pv', round(e_olc / a['ev_pv_kw'], 2), 'V/kW', "[Hesap: izlenen evin kW'ı başına]"),
                  ('olculen', site, 'egim_R2', round(r2, 2), '', '[Hesap]'),
                  ('model_aksam', site, 'egim_V_pu_model', round(e_mod, 2), 'V/pu', '[Hesap: akşam boyuyla]'),
                  ('model_aksam', site, 'oran_egim', round(e_mod / e_olc, 2), 'model÷ölçülen',
                   '[Hesap: öğlen PV kaynaklı yükselme, UKPN tanımı]'),
                  ('model_aksam', site, 'oran_egim_faz_bilgisiz', round(e_den / e_olc, 2), 'model÷ölçülen',
                   '[Hesap: ev dışı yük üç faza eşit]'),
                  ('model_aksam', site, 'ogle_R2_dakika', round(r2_og, 2), '', '[Hesap: öğlen dakikalarında ölçülen ΔV ~ model ΔV]')]
        for L in BOY_M:
            for rk in rler:
                e, _, _ = egim(pu, model_dv(kur(L, rk, p), og, p))
                sonuc.append(('model_bant', site, f'egim_L{L}_R{rk:.3f}', round(e, 2), 'V/pu',
                              f'[Hesap; boy ve kablo [Yorum]]; ölçülen {e_olc:.2f}'))

        # (c) Güneşli günler: öğlen seviyesi, aynı günün gecesine göre (cihaz farkı düşer).
        # Aynısı en bulutlu günlerde: ölçülen − model açığı güneşle büyüyorsa açık panelden gelir.
        g = seviye(j, gunler, kur(L_etkin, r_orta, p), p)
        gs = g[g.pencere == 'ogle']
        gb = seviye(j, bulutlu, kur(L_etkin, r_orta, p), p)
        gb = gb[gb.pencere == 'ogle']
        gece = g[g.pencere == 'gece']
        hata = (c + gs.dv_model) - gs.dv
        sonuc += [('olculen', site, 'gunesli_ogle_dv_ortanca', round(gs.dv.median(), 2), 'V', '[Hesap: ham, cihaz farkı dahil]'),
                  ('olculen', site, 'gunesli_gece_dv_ortanca', round(gece.dv.median(), 2), 'V', '[Hesap: ham]'),
                  ('olculen', site, 'gunesli_ogle_yukselme_ortanca', round(gs.yuk_olc.median(), 2), 'V', '[Hesap: öğlen − aynı gün gece]'),
                  ('olculen', site, 'gunesli_ogle_yukselme_P90', round(gs.yuk_olc.quantile(0.9), 2), 'V', '[Hesap]'),
                  ('olculen', site, 'gunesli_ogle_ev_pv_kW', round(gs.P_GEN.median(), 2), 'kW', '[Hesap: ortanca]'),
                  ('olculen', site, 'gunesli_ogle_fider_net_kW', round(gs[['PA', 'PB', 'PC']].sum(axis=1).median(), 1), 'kW', '[Hesap: ortanca; + çekiş]'),
                  ('olculen', site, 'gunesli_ogle_fider_evfazi_kW', round(gs[f'P{ph}'].median(), 1), 'kW', '[Hesap: ortanca]'),
                  ('model_aksam', site, 'gunesli_ogle_yukselme_model', round(gs.yuk_mod.median(), 2), 'V', '[Hesap: akşam boyuyla]'),
                  ('model_aksam', site, 'oran_seviye', round(gs.yuk_mod.median() / gs.yuk_olc.median(), 2), 'model÷ölçülen',
                   '[Hesap: güneşli öğlen − gece; panelin hat üstündeki yerine duyarlı]'),
                  ('model_aksam', site, 'hata_ortanca', round(hata.median(), 2), 'V', '[Hesap: model − ölçülen ev V, güneşli öğlen]'),
                  ('model_aksam', site, 'hata_mutlak_P90', round(hata.abs().quantile(0.9), 2), 'V', '[Hesap]'),
                  ('model_aksam', site, 'acik_gunesli', round((gs.yuk_olc - gs.yuk_mod).median(), 2), 'V',
                   '[Hesap: ölçülen − model, öğlen − gece, 12 güneşli gün]'),
                  ('model_aksam', site, 'acik_bulutlu', round((gb.yuk_olc - gb.yuk_mod).median(), 2), 'V',
                   '[Hesap: aynısı 12 en bulutlu gün]')]

        g['site'], g['fider'], g['faz'] = site, to, ph
        dakika.append(g.reset_index()[['site', 'fider', 'faz', 'datetime', 'pencere', 'bara', 'V_Filtered', 'P_GEN',
                                       'P_IMPORT', 'PA', 'PB', 'PC', 'QA', 'QB', 'QC', 'dv', 'yuk_olc',
                                       'dv_model', 'yuk_mod']])
        print(f'{site}: {to} {ph}; akşam boyu {L_etkin:.0f} m (R² {r2_ak:.2f}); eğim ölçülen {e_olc:.2f} model '
              f'{e_mod:.2f} V/pu (oran {e_mod / e_olc:.2f}); seviye oranı {gs.yuk_mod.median() / gs.yuk_olc.median():.2f}',
              flush=True)

    print('çapraz sağlamalar...', flush=True)
    bara_dagilimi(veri, sonuc)
    en_dusuk_talep(fid, mus, gunler, sonuc)
    faz_dengesizligi(fid, sonuc)

    with open(cikti, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['bolum', 'site', 'olcu', 'deger', 'birim', 'etiket'])
        w.writerows(sonuc)
    pd.concat(dakika).to_csv(cikti.with_name(cikti.stem + '_dakika.csv'), index=False, encoding='utf-8',
                             float_format='%.3f')
    for s in sonuc:
        print(*s, sep=' | ')


if __name__ == '__main__':
    main()
