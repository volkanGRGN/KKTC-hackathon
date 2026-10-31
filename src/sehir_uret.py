#!/usr/bin/env python3
"""Deneme şehri üreticisi (Faz 1): cevap anahtarı bilinen farazi Kıbrıs şehri.

Bir tohum = bir şehir: ~40 trafo, 7 tip (sözlük "Tip"). Her trafonun aboneleri tarife sınıfına
göre kurulur; abone başına eğri EAC profil sınıfından (Can'ın profiller.py'si), büyüklüğü Kıb-Tek
2023 yıllık tüketiminden. Panel üretimi Lefkoşa saatlik ışınımından (Open-Meteo). Ev ev dengesiz
yük akışı eski benzetimin solve() fonksiyonuyla. Belirsiz ayarlar şehir başına rastgele (ADR-0003).

Çıktı biçimi: docs/data/tablo-bicimi.md (trafolar.csv, yuk_5dk.csv, cevap_anahtari.csv, ayar.json).
Yer tutucular: profiller.py ya da EAC Excel'i yoksa her sınıf eski benzetimin konut eğrisini alır
(ayar.json: profil_kaynagi = yer_tutucu; bu şehir Faz 1 sınavına girmez). Open-Meteo dosyası yoksa
ışınım yapaydır (isinim_kaynagi = yapay).

Etiketler: [Kaynaklı] belge, [Hesap] bizim hesabımız, [Yorum] varsayım. Tip ayarlarının çoğu [Yorum].

Çalıştırma:
  python3 src/sehir_uret.py 7            # data/synthetic/sehir-007/
  python3 src/sehir_uret.py 1 20         # sehir-001 … sehir-020
"""
import argparse
import calendar
import csv
import datetime as dt
import json
import math
import random
import statistics
import sys
import time
from pathlib import Path

# Eski benzetim içe alınırken komut satırından tohum okuyor (random.seed(sys.argv[1])); bizim
# komut satırımız ona karışmasın. Rastgeleliğimiz kendi random.Random nesnelerimizde.
_argv, sys.argv = sys.argv, sys.argv[:1]
import trafo_bos_kapasite as tb  # noqa: E402
sys.argv = _argv

KOK = Path(__file__).resolve().parent.parent
EAC_XLSX = KOK / 'data' / 'raw' / 'eac-profil-siniflari' / 'Offtake_Profile_Classes.xlsx'
ISINIM_CSV = KOK / 'data' / 'raw' / 'open-meteo-lefkosa' / 'lefkosa_saatlik_2024_2025.csv'
CIKTI = KOK / 'data' / 'synthetic'

SOZLESME_SURUMU = 1
URETICI_SURUMU = '0.1'
ADIM = tb.STEPS_PER_DAY                  # 288, 5 dakika
AY = 4                                   # Nisan: Kıb-Tek 2023'te en az tüketilen ay [Kaynaklı: stat_2023]
GUN_SAYISI = 14                          # iki tam hafta = 10 iş günü + 4 tatil
OGLE = range(132, 168)                   # 11:00–14:00 (sözleşme)
AYLAR = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']  # EAC sütun adları
YENI_PANEL_KW = 6.5                      # bekleyen başvuruların orta değeri [ROADMAP Faz 1]
V_SINIR = tb.V_LIMIT                     # 259 V planlama sınırı
SIRA_SAYISI = 7                          # "gerçek kaç ev" için başvuru sırası
# Girne merkez: Civan'ın OSM alanının ortası [Kaynaklı: data/raw/osm-kasaba/KAYNAK.txt]
REFERANS = (35.3375, 33.318)
KUZEY_SINIRI_M = 400                     # kıyı: referansın kuzeyine en çok 400 m [Yorum]
KVA_LISTESI = [25, 50, 100, 250, 400, 630, 1000]   # direk ≤ 400 [Kaynaklı: şartname, belgesi BULAMADIM]; yer [Yorum]

# Abone sınıfı: (profiller.py sınıfı, trafolar.csv sütunu, yıllık MWh / abone, üç faz olasılığı).
# Yıllık MWh / abone [Hesap]: Kıb-Tek 2023 tarife sınıfı tüketimi (stat_2023) ÷ abone sayısı (veri sözlüğü).
SINIFLAR = {
    'konut':     ('konut',        'abone_konut',     648494 / 175577, 0.08),   # ≈ 3,69
    'ticari1':   ('kucuk_ticari', 'abone_ticari1',   210978 / 20950, 0.20),    # ≈ 10,1
    'dukkan':    ('buyuk_ticari', 'abone_ticari2',   169496 / 494, 1.0),       # ≈ 343
    # Turizm tarifesi II 215.147 MWh (2023) ÷ 171 tesis (2025) [Hesap, kaba: yıllar farklı, tesis ≠ abone]
    'otel':      ('otel',         'abone_turizm',    215147 / 171, 1.0),       # ≈ 1.258
    'sanayi1':   ('kucuk_sanayi', 'abone_sanayi1',   22391 / 1227, 1.0),       # ≈ 18,2
    'sanayi2':   ('buyuk_sanayi', 'abone_sanayi2',   95996 / 352, 1.0),        # ≈ 273
    'su_motoru': ('su_pompasi',   'abone_su_motoru', 51256 / 3250, 1.0),       # ≈ 15,8
    # Yurt binası = 40 konut eşdeğeri, konut eğrisi; tarifesi ticari II sayıldı [Yorum: BULAMADIM]
    'yurt':      ('konut',        'abone_ticari2',   40 * 648494 / 175577, 1.0),
}
BUYUK = {'dukkan', 'otel', 'sanayi2', 'yurt'}      # hattın başına (trafoya yakın) konur [Yorum]
ABONE_SUTUNLARI = ['abone_konut', 'abone_ticari1', 'abone_ticari2', 'abone_turizm',
                   'abone_sanayi1', 'abone_sanayi2', 'abone_su_motoru']

# 7 tip [Yorum, hepsi varsayım; hat boyu SimBench'in 0,23–0,57 km en uzak ev aralığıyla
# kıyaslandı, köy ve sulama Kıbrıs kırsalı için daha uzun]. abone: sınıf -> (en az, en çok).
# konum: ('halka', r_min, r_max) ya da ('kutu', x_min, x_max, y_min, y_max), metre.
TIPLER = {
    'sehir_konutu': dict(adet=14, bolge='kentsel', abone={'konut': (30, 80), 'ticari1': (0, 4)},
                         hat=(2, 4), hat_m=(150, 450), kablo=('ABC70', 'ABC95'), konum=('halka', 300, 2000)),
    'koy':          dict(adet=6, bolge='kirsal', abone={'konut': (15, 45), 'ticari1': (1, 4), 'su_motoru': (0, 2)},
                         hat=(1, 2), hat_m=(300, 900), kablo=('ABC70',), konum=('halka', 3000, 7000)),
    'carsi':        dict(adet=5, bolge='kentsel', abone={'ticari1': (15, 40), 'dukkan': (2, 8), 'konut': (0, 20)},
                         hat=(2, 4), hat_m=(100, 300), kablo=('ABC95',), konum=('halka', 0, 600)),
    'otel':         dict(adet=4, bolge='turistik', abone={'otel': (1, 2), 'ticari1': (0, 6), 'konut': (0, 10)},
                         hat=(1, 2), hat_m=(80, 250), kablo=('ABC95',), konum=('kutu', -4000, 4000, 0, 400)),
    'sanayi':       dict(adet=4, bolge='sanayi', abone={'sanayi1': (5, 15), 'sanayi2': (1, 4), 'ticari1': (0, 4)},
                         hat=(1, 3), hat_m=(150, 500), kablo=('ABC95',), konum=('kutu', 2500, 4000, -2500, -1000)),
    'sulama':       dict(adet=3, bolge='kirsal', abone={'su_motoru': (3, 8), 'konut': (0, 8)},
                         hat=(1, 2), hat_m=(400, 1200), kablo=('ABC70',), konum=('halka', 2500, 6000)),
    'yurt':         dict(adet=4, bolge='kentsel', abone={'yurt': (2, 5), 'ticari1': (2, 8), 'konut': (0, 15)},
                         hat=(1, 3), hat_m=(100, 300), kablo=('ABC95',), konum=('halka', 800, 2000)),
}


# ---------- girdiler: eğriler ve ışınım ----------

def egrileri_yukle():
    """Nisan eğrileri {(sınıf, gün türü): 288 değer, 2022 yıllık ortalaması = 1}, sınıfın yıl
    içindeki en yüksek değeri (aynı birimde; trafo boyu için) ve kaynak adı."""
    try:
        import profiller
        veri = profiller.oku(EAC_XLSX)
        ort = {s: yillik_ortalama(veri, SINIFLAR[s][0]) for s in SINIFLAR}
        egriler = {(s, g): [x / ort[s] for x in profiller.sinif_egrisi(veri, SINIFLAR[s][0], AY, g)]
                   for s in SINIFLAR for g in ('is', 'tatil')}
        tepe = {s: max(max(seri) for seri in veri[SINIFLAR[s][0]].values()) / ort[s] for s in SINIFLAR}
        return egriler, tepe, 'eac'
    except (ImportError, OSError) as e:
        print(f'UYARI: EAC eğrileri yok ({e.__class__.__name__}: {e}); yer tutucu eğri kullanılıyor.')
        eg = [tb.base_load(s * 5 / 60) for s in range(ADIM)]
        o = statistics.fmean(eg)
        eg = [x / o for x in eg]
        return ({(s, g): eg for s in SINIFLAR for g in ('is', 'tatil')},
                {s: max(eg) for s in SINIFLAR}, 'yer_tutucu')


def yillik_ortalama(veri, sinif):
    """24 tipik günün 2022 takvimine göre ağırlıklı ortalaması (pu) [Hesap: cumartesi ve pazar
    tatil, bayramlar yok sayıldı]."""
    toplam, gun = 0.0, 0
    for ay in range(1, 13):
        for g in range(1, calendar.monthrange(2022, ay)[1] + 1):
            tur = 'NWD' if dt.date(2022, ay, g).weekday() >= 5 else 'WD'
            seri = veri[sinif][f'{AYLAR[ay - 1]}_{tur}']
            toplam += sum(seri) / len(seri)
            gun += 1
    return toplam / gun


def isinim_oku(yol):
    """Open-Meteo saatlik CSV -> {tarih: 24 değer}, değer = eğik (30°, güney) ışınım ÷ 1000 W/m².
    Satır 'T12:00' = 11:00–12:00 ortalaması (KAYNAK.txt)."""
    saatlik = {}
    with open(yol, encoding='utf-8') as fh:
        satirlar = fh.read().splitlines()
    bas = next(i for i, s in enumerate(satirlar) if s.startswith('time,'))
    basliklar = satirlar[bas].split(',')
    sut = next(i for i, b in enumerate(basliklar) if b.startswith('global_tilted_irradiance'))
    for s in satirlar[bas + 1:]:
        p = s.split(',')
        if len(p) <= sut or not p[sut]:
            continue
        an = dt.datetime.fromisoformat(p[0]) - dt.timedelta(hours=1)   # saatin başı
        saatlik.setdefault(an.date(), [0.0] * 24)[an.hour] = float(p[sut]) / 1000
    return saatlik


def gunun_isinimi(saatlik, tarih):
    """24 saatlik ortalama -> 288 beş dakika; değerler saat ortasına konur, arası doğrusal."""
    h = saatlik[tarih]
    out = []
    for s in range(ADIM):
        x = (s + 0.5) * 5 / 60 - 0.5
        i = math.floor(x)
        w = x - i
        a, b = h[min(max(i, 0), 23)], h[min(max(i + 1, 0), 23)]
        out.append(max(0.0, a * (1 - w) + b * w))
    return out


def yapay_isinim(rng):
    """Open-Meteo dosyası yoksa: eski benzetimin açık / parçalı / kapalı gün kurgusu [Yorum]."""
    turler = ['açık'] * 8 + ['parçalı'] * 4 + ['kapalı'] * 2
    rng.shuffle(turler)
    g, bulut = [], 1.0
    for tur in turler:
        for s in range(ADIM):
            h = s * 5 / 60
            acik = math.sin(math.pi * (h - 6.6) / 12.5) ** 1.2 if 6.6 < h < 19.1 else 0.0
            if tur == 'açık':
                c = 1 - abs(rng.gauss(0, 0.02))
            elif tur == 'kapalı':
                c = min(1, max(0.15, 0.4 + rng.gauss(0, 0.08)))
            else:
                bulut = 0.6 * bulut + 0.4 * rng.choice([1.0, 1.0, 0.95, 0.35, 0.5])
                c = bulut
            g.append(acik * c)
    return g


def og_carpani(g, rng):
    """Orta gerilim ortak çarpanı; eski benzetimin mv_factor'ü, kendi rastgelemizle."""
    n, w = len(g), 12
    duz = [sum(g[max(0, i - w):min(n, i + w + 1)]) / (min(n, i + w + 1) - max(0, i - w)) for i in range(n)]
    m, ar = [], 0.0
    for i in range(n):
        h = (i % ADIM) * 5 / 60
        ar = 0.97 * ar + rng.gauss(0, 0.0006)
        m.append(1 + 0.008 * duz[i] - 0.006 * math.exp(-((h - 20) / 1.8) ** 2) + ar)
    return m


# ---------- şehir kurma ----------

def tip_sayilari(rng, n):
    """Her tipe 3, kalanı taban dağılımın (40 trafoda 'adet') oranında; sonra 6 rastgele kaydırma.
    Her tip en az 3 trafo."""
    fazla = {t: a['adet'] - 3 for t, a in TIPLER.items()}
    sayi = {t: 3 + (n - 3 * len(TIPLER)) * f // sum(fazla.values()) for t, f in fazla.items()}
    sayi['sehir_konutu'] += n - sum(sayi.values())
    for _ in range(6):
        kaynaklar = [t for t in sayi if sayi[t] > 3]
        if not kaynaklar:
            break
        sayi[rng.choice(kaynaklar)] -= 1
        sayi[rng.choice(list(sayi))] += 1
    return sayi


def konum(rng, k):
    while True:
        if k[0] == 'halka':
            r, a = rng.uniform(k[1], k[2]), rng.uniform(0, 2 * math.pi)
            x, y = r * math.cos(a), r * math.sin(a)
        else:
            x, y = rng.uniform(k[1], k[2]), rng.uniform(k[3], k[4])
        if y <= KUZEY_SINIRI_M:
            return round(x), round(y)


def sehir_kur(rng, n_trafo, ayar, tepe_orani):
    sayi = tip_sayilari(rng, n_trafo)
    tipler = [t for t in TIPLER for _ in range(sayi[t])]
    rng.shuffle(tipler)
    trafolar = []
    for ti, tip in enumerate(tipler):
        a = TIPLER[tip]
        abone = []
        for sinif, (lo, hi) in a['abone'].items():
            abone += [sinif] * rng.randint(lo, hi)
        n_hat = min(rng.randint(*a['hat']), len(abone))
        # boyut: sınıfın yıl içi tepesi (24 tipik gün) × yıllık ortalama kW, büyütme payı 1,2–2,0 [Yorum]
        gerek = sum(SINIFLAR[s][2] * 1000 / 8760 * tepe_orani[s] * ayar['tuketim_carpani'][s] for s in abone)
        gerek *= rng.uniform(1.2, 2.0)
        kva = next((k for k in KVA_LISTESI if k >= gerek), KVA_LISTESI[-1])
        x, y = konum(rng, a['konum'])
        fw = [rng.uniform(0.8, 1.2) for _ in range(3)]
        tr = dict(no=f'T{ti + 1:02d}', tip=tip, bolge=a['bolge'], kva=kva, x=x, y=y,
                  montaj='direk' if kva <= 400 else 'yer', kablo=rng.choice(a['kablo']),
                  v0=round(rng.uniform(246.0, 250.0), 1), feeders=[], evler=[])
        zb = 240.0 ** 2 / (kva * 1000 / 3)
        rt = 0.04 * zb / math.sqrt(5)                 # uk %4, X/R = 2 (eski benzetim)
        tr['zt'] = complex(rt, 2 * rt)
        rng.shuffle(abone)
        hatlar = [abone[i::n_hat] for i in range(n_hat)]
        for hat in hatlar:
            hat.sort(key=lambda s: s not in BUYUK)    # büyükler trafoya yakın
            boy = round(rng.uniform(*a['hat_m']))
            zc, znc = tb.CABLES[tr['kablo']]
            seg = boy / 1000 / len(hat)
            f = dict(zs=zc * seg, zn=znc * seg, houses=[], boy=boy)
            for k, sinif in enumerate(hat):
                uc_faz = rng.random() < SINIFLAR[sinif][3]
                ph = 3 if uc_faz else rng.choices([0, 1, 2], weights=fw)[0]
                pv = 0.0
                if sinif == 'konut':
                    konum_orani = (k + 1) / len(hat)
                    if rng.random() < ayar['panel_yayginligi'] * (0.6 + 0.8 * konum_orani):
                        pv = 8.0 if uc_faz else rng.choice([5.0, 5.0, 5.0, 4.0, 3.0])
                sigma = 0.35 if sinif == 'konut' else 0.3     # abone farkı [Yorum]
                h = dict(id=len(tr['evler']), sinif=sinif, ph=ph, pv=pv,
                         olcek=rng.lognormvariate(-sigma ** 2 / 2, sigma))
                f['houses'].append(h)
                tr['evler'].append(h)
            tr['feeders'].append(f)
        trafolar.append(tr)
    return trafolar, sayi


# ---------- benzetim ----------

def yuk_serisi(tr, ayar, egriler, gun_turleri, rng):
    """Abone başına 14 gün × 288 adım kW (brüt tüketim)."""
    gunluk = {}
    for s in SINIFLAR:
        kw = SINIFLAR[s][2] * 1000 / 8760 * ayar['tuketim_carpani'][s]
        k = ayar['saat_kaymasi_dk'][s] // 5
        for g in ('is', 'tatil'):
            eg = egriler[(s, g)]
            gunluk[(s, g)] = [kw * eg[(i - k) % ADIM] for i in range(ADIM)]
    out = {}
    for h in tr['evler']:
        gurultu = 0.2 if h['sinif'] in ('konut', 'ticari1') else 0.05   # 5 dk dalgalanma [Yorum]
        seri = []
        for tur in gun_turleri:
            for p in gunluk[(h['sinif'], 'is' if tur == 'isgunu' else 'tatil')]:
                seri.append(max(0.02, p * h['olcek'] * (1 + rng.gauss(0, gurultu))))
        out[h['id']] = seri
    return out


def net_guc(tr, i, g, yuk, ek=None):
    net = {}
    for h in tr['evler']:
        p = yuk[h['id']][i]
        pv = (h['pv'] + (ek.get(h['id'], 0.0) if ek else 0.0)) * g[i] * tb.PV_DERATE
        net[h['id']] = ((p - pv) * 1000, p * 0.33 * 1000)
    return net


def gerilim_uclari(tr, V):
    hi, lo = 0.0, 1e9
    for fi, f in enumerate(tr['feeders']):
        for k, h in enumerate(f['houses']):
            v = V[fi][k]
            fazlar = range(3) if h['ph'] == 3 else (h['ph'],)
            for p in fazlar:
                u = abs(v[p] - v[3])
                hi, lo = max(hi, u), min(lo, u)
    return hi, lo


def asim(tr, g, m, yuk, kritik, ek, taban):
    """Kritik adımlarda sınır aşılıyor mu: 'gerilim', 'isil' ya da None. taban: o adımın bugünkü
    çözümü; solve() başlangıç değerini yerinde değiştirdiği için kopyası verilir."""
    for i in kritik:
        bas = [[list(v) for v in hat] for hat in taban[i]]
        V, s_tr = tb.solve(tr, net_guc(tr, i, g, yuk, ek), m[i], bas, iters=5)
        if gerilim_uclari(tr, V)[0] > V_SINIR:
            return 'gerilim'
        if s_tr > tr['kva']:
            return 'isil'
    return None


def trafo_benzet(tr, g, m, yuk, gun_turleri, rng):
    n = len(g)
    seri = dict(tuketim=[0.0] * n, uretim=[0.0] * n, vmax=[0.0] * n, vmin=[0.0] * n)
    warm = None
    for i in range(n):
        V, _ = tb.solve(tr, net_guc(tr, i, g, yuk), m[i], warm, iters=3 if warm else 6)
        warm = V
        seri['vmax'][i], seri['vmin'][i] = gerilim_uclari(tr, V)
        seri['tuketim'][i] = sum(yuk[h['id']][i] for h in tr['evler'])
        seri['uretim'][i] = sum(h['pv'] for h in tr['evler']) * g[i] * tb.PV_DERATE

    # cevap anahtarı: öğlen en düşük yük
    ogle = [d * ADIM + s for d in range(len(gun_turleri)) for s in OGLE]
    tur_ogle = {t: [d * ADIM + s for d, tt in enumerate(gun_turleri) if tt == t for s in OGLE]
                for t in ('isgunu', 'tatil')}
    cevap = dict(
        ogle_min_kw=min(seri['tuketim'][i] for i in ogle),
        ogle_min_kw_isgunu=min(seri['tuketim'][i] for i in tur_ogle['isgunu']),
        ogle_min_kw_tatil=min(seri['tuketim'][i] for i in tur_ogle['tatil']),
        ogle_min_net_kw=min(seri['tuketim'][i] - seri['uretim'][i] for i in ogle),
        tepe_kw=max(seri['tuketim']),
        v_max_bugun_v=max(seri['vmax']), v_min_bugun_v=min(seri['vmin']))

    # cevap anahtarı: gerçek kaç ev (tanım sözleşmede)
    # Başvurular sırayla; sınırı aşan reddedilir, sıradakine geçilir (Kıb-Tek'in sırası gibi).
    kritik = sorted(range(n), key=lambda i: -seri['vmax'][i])[:6]
    kritik += [i for i in sorted(range(n), key=lambda i: -g[i])[:3] if i not in kritik]
    taban = {i: tb.solve(tr, net_guc(tr, i, g, yuk), m[i], None, iters=8)[0] for i in kritik}
    adaylar = [h['id'] for h in tr['evler'] if h['sinif'] == 'konut' and h['pv'] == 0]
    bugun = asim(tr, g, m, yuk, kritik, {}, taban)
    sonuclar = []
    for _ in range(SIRA_SAYISI):
        sira = adaylar[:]
        rng.shuffle(sira)
        ek, ilk_ret = {}, bugun
        if bugun is None:
            for hid in sira:
                ek[hid] = YENI_PANEL_KW
                neden = asim(tr, g, m, yuk, kritik, ek, taban)
                if neden:
                    del ek[hid]
                    ilk_ret = ilk_ret or neden
        sonuclar.append((len(ek), ilk_ret or 'yok'))
    sonuclar.sort(key=lambda r: r[0])
    orta = sonuclar[SIRA_SAYISI // 2]
    cevap.update(kac_ev_aday=len(adaylar), kac_ev_gercek=orta[0],
                 kac_ev_gercek_min=sonuclar[0][0], kac_ev_gercek_max=sonuclar[-1][0],
                 kac_ev_tavan=int(orta[0] == len(adaylar)), kac_ev_sinir=orta[1])
    return seri, cevap


# ---------- yazma ----------

def csv_yaz(yol, basliklar, satirlar):
    with open(yol, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(basliklar)
        w.writerows(satirlar)


def enlem_boylam(x, y):
    enlem = REFERANS[0] + y / 111320
    boylam = REFERANS[1] + x / (111320 * math.cos(math.radians(REFERANS[0])))
    return round(enlem, 6), round(boylam, 6)


def sehir_uret(tohum, n_trafo=40, cikti=CIKTI):
    t0 = time.time()
    rng = random.Random(f'yapi-{tohum}')
    egriler, tepe_orani, profil_kaynagi = egrileri_yukle()

    siniflar = list(SINIFLAR)
    kayma_ust = rng.uniform(30, 60)                   # ±30–60 dk [ROADMAP Faz 1]
    ayar = dict(
        sehir=tohum, tohum=tohum, sozlesme_surumu=SOZLESME_SURUMU, uretici_surumu=URETICI_SURUMU,
        trafo_sayisi=n_trafo, ay=AY,
        tuketim_carpani={s: round(rng.uniform(0.8, 1.2), 3) for s in siniflar},       # ±%20
        saat_kaymasi_dk={s: 5 * round(rng.uniform(-kayma_ust, kayma_ust) / 5) for s in siniflar},
        panel_yayginligi=round(rng.uniform(0.10, 0.50), 3),                         # %10–50
        yeni_panel_kw=YENI_PANEL_KW, v_sinir_v=V_SINIR,
        referans_enlem=REFERANS[0], referans_boylam=REFERANS[1],
        profil_kaynagi=profil_kaynagi, kac_ev_sira_sayisi=SIRA_SAYISI)

    # hava yılı ve günler: 2024 ya da 2025 Nisan'ından ardışık 14 gün
    yil = rng.choice([2024, 2025])
    bas = dt.date(yil, AY, rng.randint(1, 30 - GUN_SAYISI + 1))
    tarihler = [bas + dt.timedelta(days=d) for d in range(GUN_SAYISI)]
    gun_turleri = ['tatil' if t.weekday() >= 5 else 'isgunu' for t in tarihler]
    if ISINIM_CSV.exists():
        saatlik = isinim_oku(ISINIM_CSV)
        g = [x for t in tarihler for x in gunun_isinimi(saatlik, t)]
        ayar.update(isinim_kaynagi='open-meteo-lefkosa', hava_yili=yil)
    else:
        print(f'UYARI: {ISINIM_CSV.name} yok; yapay ışınım kullanılıyor.')
        g = yapay_isinim(random.Random(f'hava-{tohum}'))
        ayar.update(isinim_kaynagi='yapay', hava_yili=None)
    ayar.update(gun_turleri=gun_turleri, tarihler=[t.isoformat() for t in tarihler])
    m = og_carpani(g, random.Random(f'og-{tohum}'))

    trafolar, sayi = sehir_kur(rng, n_trafo, ayar, tepe_orani)
    ayar['tip_sayilari'] = sayi

    klasor = Path(cikti) / f'sehir-{tohum:03d}'
    klasor.mkdir(parents=True, exist_ok=True)
    trafo_satir, cevap_satir, yuk_satir = [], [], []
    for tr in trafolar:
        trng = random.Random(f'yuk-{tohum}-{tr["no"]}')
        yuk = yuk_serisi(tr, ayar, egriler, gun_turleri, trng)
        seri, cevap = trafo_benzet(tr, g, m, yuk, gun_turleri, trng)

        abone = {c: 0 for c in ABONE_SUTUNLARI}
        for h in tr['evler']:
            abone[SINIFLAR[h['sinif']][1]] += 1
        enlem, boylam = enlem_boylam(tr['x'], tr['y'])
        boylar = [f['boy'] for f in tr['feeders']]
        panelli = [h for h in tr['evler'] if h['pv'] > 0]
        trafo_satir.append([tohum, tr['no'], enlem, boylam, tr['x'], tr['y'], tr['bolge'], tr['montaj'],
                            tr['kva'], len(boylar), max(boylar), sum(boylar), tr['kablo'],
                            *[abone[c] for c in ABONE_SUTUNLARI], len(panelli),
                            round(sum(h['pv'] for h in panelli), 2)])

        faz = [sum(1 for h in tr['evler'] if h['ph'] == p) for p in range(4)]
        cevap_satir.append([tohum, tr['no'], tr['tip'], tr['v0'], *faz,
                            round(cevap['ogle_min_kw'], 2), round(cevap['ogle_min_kw_isgunu'], 2),
                            round(cevap['ogle_min_kw_tatil'], 2), round(cevap['ogle_min_net_kw'], 2),
                            round(cevap['tepe_kw'], 2), round(cevap['v_max_bugun_v'], 1),
                            round(cevap['v_min_bugun_v'], 1), cevap['kac_ev_aday'], cevap['kac_ev_gercek'],
                            cevap['kac_ev_gercek_min'], cevap['kac_ev_gercek_max'],
                            cevap['kac_ev_tavan'], cevap['kac_ev_sinir']])

        for i in range(len(g)):
            d, s = divmod(i, ADIM)
            tk, ur = seri['tuketim'][i], seri['uretim'][i]
            yuk_satir.append([tohum, tr['no'], d, gun_turleri[d], s, f'{s * 5 // 60:02d}:{s * 5 % 60:02d}',
                              round(tk, 2), round(ur, 2), round(tk - ur, 2),
                              round(seri['vmax'][i], 1), round(seri['vmin'][i], 1)])

    csv_yaz(klasor / 'trafolar.csv',
            ['sehir', 'trafo_no', 'enlem', 'boylam', 'x_m', 'y_m', 'bolge', 'montaj', 'kva', 'hat_sayisi',
             'hat_boyu_max_m', 'hat_boyu_toplam_m', 'kablo', *ABONE_SUTUNLARI, 'panel_sayisi', 'panel_kw'],
            trafo_satir)
    csv_yaz(klasor / 'yuk_5dk.csv',
            ['sehir', 'trafo_no', 'gun', 'gun_turu', 'adim', 'saat', 'tuketim_kw', 'uretim_kw', 'net_kw',
             'v_max_v', 'v_min_v'], yuk_satir)
    csv_yaz(klasor / 'cevap_anahtari.csv',
            ['sehir', 'trafo_no', 'tip', 'v0_v', 'faz_a_ev', 'faz_b_ev', 'faz_c_ev', 'uc_faz_ev',
             'ogle_min_kw', 'ogle_min_kw_isgunu', 'ogle_min_kw_tatil', 'ogle_min_net_kw', 'tepe_kw',
             'v_max_bugun_v', 'v_min_bugun_v', 'kac_ev_aday', 'kac_ev_gercek', 'kac_ev_gercek_min',
             'kac_ev_gercek_max', 'kac_ev_tavan', 'kac_ev_sinir'], cevap_satir)
    ayar['sure_sn'] = round(time.time() - t0, 1)
    with open(klasor / 'ayar.json', 'w', encoding='utf-8') as fh:
        json.dump(ayar, fh, ensure_ascii=False, indent=1)

    vmax = max(r[13] for r in cevap_satir)
    n_abone = sum(len(tr['evler']) for tr in trafolar)
    kac = statistics.median(r[16] for r in cevap_satir)
    print(f'{klasor.name}: {len(trafolar)} trafo, {n_abone} abone, {ayar["sure_sn"]} sn; '
          f'en yüksek gerilim {vmax} V; kaç ev ortancası {kac}; profil {profil_kaynagi}, '
          f'ışınım {ayar["isinim_kaynagi"]}')
    return klasor


def main():
    ap = argparse.ArgumentParser(description='Deneme şehri üreticisi (Faz 1).')
    ap.add_argument('ilk', type=int, help='tohum (şehir no)')
    ap.add_argument('son', type=int, nargs='?', help='verilirse ilk…son arası her tohum')
    ap.add_argument('--trafo', type=int, default=40, help='trafo sayısı (en az 21: 7 tip × 3)')
    ap.add_argument('--cikti', type=Path, default=CIKTI, help='çıktı klasörü')
    a = ap.parse_args()
    if a.trafo < 21:
        ap.error('--trafo en az 21 olmalı (her tipten en az 3)')
    for tohum in range(a.ilk, (a.son if a.son is not None else a.ilk) + 1):
        sehir_uret(tohum, a.trafo, a.cikti)


if __name__ == '__main__':
    main()
