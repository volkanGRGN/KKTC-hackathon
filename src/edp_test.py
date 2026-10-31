#!/usr/bin/env python3
"""Şablon yöntemini GERÇEK veride sınar (ROADMAP Faz 2, adım 2i): İspanya EDP, Oviedo, 1–21 Mayıs 2018, saatlik.

Veri: Mendeley 685vgp64sm (CC BY 4.0), data/raw/edp-oviedo/KAYNAK.txt. Ham veri depoya girmez; ilk okuma
Excel'den bir kez yapılır, ön bellek (pickle) ham klasörün yanına yazılır.

Yöntem src/sablon.py (PR #8) ile aynı adımlar, ama abone tarifesi yok, o yüzden ayrı dosya:
  2c ölçülü trafoların iş günü eğrisi tepeye bölünür; Ward + siluet ile k, sonra k-means
  2d çok sınıflı lojistik regresyon: Kıb-Tek'in bileceği özellikler -> küme
  2e ölçek: küme başına NNLS (göreli hata), ortak katsayıya çekilmiş
  2f %80 bant: bir-trafo-dışarıda log artıklarının P10–P90'ı
  2g güven: atama olasılığı + ölçülülere uzaklık + beklenen hata (sablon.py eşikleri)

Doğru cevap: trafonun başındaki ölçüm cihazı (Referencia ZIVS…, trafo başına bir tane). Kıb-Tek'in takacağı
cihazın aynısı. Model YALNIZ seçilen ölçülü trafoların bu ölçümünü görür.

Girdi türleri (Kıb-Tek'in bildiği; ölçülmeyen trafo için de vardır):
  a  müşteri sayısı, kVA, panelli sayaç sayısı, toplam hat boyu, havai hat payı, üç faz payı; ölçek = müşteri
  b  a + "sayaç tipi" sayıları: tipler YALNIZ ölçülü trafoların sayaç eğrilerinden kümelenir; ölçülmeyen
     sayaca tip, eğrisiyle değil, faturası (dönem kWh), fazı ve paneli ile sınıflandırıcı üzerinden verilir
  c  a + trafonun fatura toplamı (aynı üç haftanın kWh'i): ÜST SINIR, çünkü hedefle aynı dönem
Kıyas: ölçülülerde ortalama "öğlen en düşük ÷ müşteri" × müşteri sayısı.

Çalıştırma:
  python3 src/edp_test.py <GIS_data klasörü>                # bütün deneyler, özet ekrana ve JSON'a
  python3 src/edp_test.py <GIS_data klasörü> --hazirlik     # yalnız veri temizliği sayıları
"""
import argparse
import json
import math
import random
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import nnls
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import silhouette_score

warnings.filterwarnings('ignore', category=ConvergenceWarning)

OGLE_SAAT = (11, 12, 13)                # 11:00–14:00 (sözleşme); saat damgası aralığın başı sayıldı [Yorum]
K_EN_COK = 6
BANT = (0.10, 0.90)
DENEY_N = (5, 10, 15)
TEKRAR = 20
TIP_K = 4                               # sayaç tipi sayısı (b) [Yorum]
LAMBDA = 1.0
# sablon.py ile aynı güven eşikleri
GUVEN_YUKSEK_P, GUVEN_DUSUK_P = 0.70, 0.50
GUVEN_YUKSEK_UZAK, GUVEN_DUSUK_UZAK = 1.0, 2.0
GUVEN_YUKSEK_HATA, GUVEN_DUSUK_HATA = 0.10, 0.25
TATIL = {pd.Timestamp('2018-05-01')}    # İşçi Bayramı, İspanya ulusal tatili [Kaynaklı]


# ---------- veri ----------

def oku(G):
    """Excel -> temiz saatlik ölçüm (pickle ön bellekli). -> (ölçüm, sayılar)."""
    onb = Path(G).parent / 'edp_olcum.pkl'
    if onb.exists():
        d = pd.read_pickle(onb)
    else:
        parca = [pd.read_excel(Path(G) / f'file{i}.xlsx', engine='calamine',
                               usecols=['Codigo Ct', 'Referencia', 'Fecha', 'Activa E', 'Activa S', 'Estado',
                                        'Tipo proceso']) for i in range(1, 8)]
        d = pd.concat(parca, ignore_index=True)
        d['Fecha'] = pd.to_datetime(d['Fecha'])
        d.to_pickle(onb)
    say = dict(satir=len(d), sayac=int(d.Referencia.nunique()))
    # Ondalık virgül: "1,015" (1,015 kWh) Excel'de 1015 diye okunmuş. Bu satırların hepsi ≥ 1001 ve tamsayı;
    # bir konut sayacında saatte 1000 kWh olamaz. ≥ 1000 olan değer 1000'e bölünür [Hesap; Faz 2i günlüğü].
    for c in ['Activa E', 'Activa S']:
        d[c] = pd.to_numeric(d[c].astype(str).str.replace(',', '.'), errors='coerce')
        say[f'virgul_{c}'] = int((d[c] >= 1000).sum())
        d[c] = np.where(d[c] >= 1000, d[c] / 1000, d[c])
    kotu = (d['Estado'].astype(str) != '0') | (d['Tipo proceso'] != 'A') | d['Activa E'].isna()
    say['estado_sifir_degil'] = int((d['Estado'].astype(str) != '0').sum())
    say['tipo_M'] = int((d['Tipo proceso'] != 'A').sum())
    say['atilan'] = int(kotu.sum())
    d = d[~kotu]
    d = d[d.Fecha < '2018-05-21']                     # 21 Mayıs yarım gün
    return d, say


def trafo_tablosu(G, d):
    """Trafo başına Kıb-Tek'in bileceği sütunlar + ölçüm (yalnız cevap/ölçülü için)."""
    m = pd.read_excel(Path(G) / 'master.xlsx', sheet_name=None, engine='calamine')
    tr = m['CT - TRAFO'].rename(columns={'CLAVE_BDI': 'ct', 'CLAVE TRAFO': 'trafo', 'POTENCIA TRAFO': 'kva'})
    tr = tr[['ct', 'trafo', 'kva']].set_index('ct')
    hat = m['Linea BT'][['Mslink', 'Clave CT']].rename(columns={'Mslink': 'Mslink Línea'})
    seg = m['Segmento BT'].merge(hat, on='Mslink Línea')
    tr['hat_m'] = seg.groupby('Clave CT').Longitud.sum()
    tr['havai_pay'] = seg.assign(h=seg.Longitud * (seg.Tipo == 'Aéreo')).groupby('Clave CT').h.sum() / tr['hat_m']
    ld = pd.read_excel(Path(G) / 'load.xlsx', sheet_name='Load', engine='calamine')
    tr['musteri'] = ld.groupby('Codigo Ct').size()
    tr['uc_faz_pay'] = ld.assign(u=ld.Fases != 'M').groupby('Codigo Ct').u.mean()   # M = tek faz

    bas = d.Referencia.str.startswith('ZIVS')          # trafo başı ölçüm cihazı
    sy = d[~bas]
    tr['panelli'] = sy[sy['Activa S'] > 0].groupby('Codigo Ct').Referencia.nunique()
    tr['fatura_kwh'] = sy.groupby('Codigo Ct')['Activa E'].sum()   # dönem faturası (c)
    tr = tr.fillna({'panelli': 0, 'fatura_kwh': 0})

    # cevap: trafo başı, saatlik kW (kWh/saat)
    yk = d[bas].groupby(['Codigo Ct', 'Fecha'])['Activa E'].sum().unstack(0)
    yk_s = d[bas].groupby(['Codigo Ct', 'Fecha'])['Activa S'].sum().unstack(0)
    gun = yk.index.normalize()
    isg = (yk.index.dayofweek < 5) & ~gun.isin(TATIL)
    ogle = yk.index.hour.isin(OGLE_SAAT)
    olcum = {}
    for ct in yk.columns:
        x = yk[ct]
        egri = x[isg].groupby(x[isg].index.hour).mean().reindex(range(24)).interpolate().to_numpy()
        olcum[ct] = dict(ogle_min=float(x[ogle].min()), isgunu=egri, verilen=float(yk_s[ct].max()))
    return tr, olcum, sy


# ---------- sayaç tipi (b) ----------

def sayac_ozellik(sy):
    """Sayaç başına: tepeye bölünmüş iş günü eğrisi (yalnız ölçülü trafoda kümeye girer) ve Kıb-Tek'in bildiği
    fatura (dönem kWh), panel, faz."""
    g = sy[sy.Fecha.dt.dayofweek < 5]
    e = g.groupby(['Referencia', g.Fecha.dt.hour])['Activa E'].mean().unstack().reindex(columns=range(24))
    e = e.fillna(0).to_numpy()
    mx = e.max(1, keepdims=True)
    sekil = np.divide(e, mx, out=np.zeros_like(e), where=mx > 0)
    ref = g.groupby('Referencia').size().index
    ozet = sy.groupby('Referencia').agg(ct=('Codigo Ct', 'first'), kwh=('Activa E', 'sum'),
                                       panel=('Activa S', lambda s: float((s > 0).any())))
    ozet = ozet.loc[ref]
    return ozet, sekil


def tip_sayilari(ozet, sekil, faz, olculu_ct, tohum):
    """Tipler yalnız ölçülü trafoların sayaç eğrilerinden (k-means). Her sayaca (ölçülü olanlar dahil, tutarlı
    olsun diye) tip, eğrisiyle değil, fatura/panel/faz ile eğitilmiş sınıflandırıcıdan verilir.
    -> trafo × tip sayı tablosu."""
    X = np.column_stack([np.log1p(ozet.kwh), ozet.panel, faz.reindex(ozet.index).fillna(0)])
    ic = ozet.ct.isin(olculu_ct).to_numpy()
    km = KMeans(n_clusters=TIP_K, n_init=5, random_state=tohum).fit(sekil[ic])
    sinif = LogisticRegression(max_iter=2000).fit(X[ic], km.labels_)
    tip = sinif.predict(X)
    return pd.crosstab(ozet.ct, tip).reindex(columns=range(TIP_K), fill_value=0)


# ---------- model ----------

def kumele(egri):
    n = len(egri)
    k_ust = min(K_EN_COK, n - 1)
    k_alt = 3 if n >= 9 else 2
    if k_ust < 2:
        return np.zeros(n, int), 1
    sil = {}
    for k in range(min(k_alt, k_ust), k_ust + 1):
        sil[k] = silhouette_score(egri, AgglomerativeClustering(n_clusters=k, linkage='ward').fit_predict(egri))
    k = max(sil, key=lambda x: (round(sil[x], 3), -x))
    ward = AgglomerativeClustering(n_clusters=k, linkage='ward').fit_predict(egri)
    merkez = np.array([egri[ward == j].mean(0) for j in range(k)])
    et = KMeans(n_clusters=k, init=merkez, n_init=1, random_state=0).fit_predict(egri)
    return (et if len(set(et)) == k else ward), k


def olcek(B, y, onsel=None):
    """y ≈ B @ β, göreli hata, β ≥ 0, `onsel`e çekili (yoksa tek ortak oran)."""
    if onsel is None:
        onsel = np.full(B.shape[1], y.sum() / max(B.sum(), 1e-9))
    w = 1 / np.maximum(y, 1.0)
    # sütun ölçeği: ceza her sütunda aynı ağırlıkta olsun
    s = np.maximum(B.mean(0), 1e-9)
    Bs = B / s
    M = np.vstack([Bs * w[:, None], math.sqrt(LAMBDA) * np.eye(B.shape[1])])
    b = np.concatenate([y * w, math.sqrt(LAMBDA) * onsel * s])
    g, _ = nnls(M, b)
    return g / s


def kur(X, B, y, egri):
    et, k = kumele(egri)
    ort, sap = X.mean(0), X.std(0)
    sap[sap == 0] = 1
    Z = (X - ort) / sap
    lr = LogisticRegression(max_iter=2000).fit(Z, et) if k > 1 else None
    ortak = olcek(B, y)
    beta = np.array([olcek(B[et == j], y[et == j], onsel=ortak) for j in range(k)])
    d = np.sqrt(((Z[:, None] - Z[None]) ** 2).sum(-1))
    np.fill_diagonal(d, np.inf)
    ref = float(np.median(d.min(1))) if len(Z) > 1 else 1.0
    return dict(k=k, lr=lr, ort=ort, sap=sap, Z=Z, beta=beta, ref=max(ref, 1e-6))


def tahmin(m, X, B):
    Z = (X - m['ort']) / m['sap']
    if m['lr'] is not None:
        p = np.zeros((len(X), m['k']))
        p[:, m['lr'].classes_] = m['lr'].predict_proba(Z)
    else:
        p = np.ones((len(X), 1))
    orta = ((B @ m['beta'].T) * p).sum(1)
    uzak = np.sqrt(((Z[:, None] - m['Z'][None]) ** 2).sum(-1)).min(1) / m['ref']
    return orta, p.max(1), uzak


def guven(p, uzak, beklenen):
    if uzak > GUVEN_DUSUK_UZAK or p < GUVEN_DUSUK_P or beklenen > GUVEN_DUSUK_HATA:
        return 'dusuk'
    if p >= GUVEN_YUKSEK_P and uzak <= GUVEN_YUKSEK_UZAK and beklenen <= GUVEN_YUKSEK_HATA:
        return 'yuksek'
    return 'orta'


def calistir(X, B, y, egri, sec, hedef):
    m = kur(X[sec], B[sec], y[sec], egri[sec])
    r = []
    for i in range(len(sec)):
        kal = np.delete(sec, i)
        mi = kur(X[kal], B[kal], y[kal], egri[kal])
        t = tahmin(mi, X[[sec[i]]], B[[sec[i]]])[0][0]
        r.append(math.log(max(y[sec[i]], .01) / max(t, .01)))
    r = np.array(r)
    alt, ust = np.exp(np.quantile(r, BANT))
    beklenen = float(np.median(np.abs(np.exp(r) - 1)))
    orta, p, uzak = tahmin(m, X[hedef], B[hedef])
    return orta, orta * alt, orta * ust, [guven(p[j], uzak[j], beklenen) for j in range(len(hedef))]


# ---------- seçim ----------

def sec_tabakali(X, n, rng):
    Z = (X - X.mean(0)) / np.where(X.std(0) == 0, 1, X.std(0))
    et = KMeans(n_clusters=n, n_init=10, random_state=rng.randrange(2 ** 31)).fit_predict(Z)
    return np.array(sorted(rng.choice(np.flatnonzero(et == j).tolist()) for j in range(n)))


# ---------- deney ----------

def deney(tr, olcum, ozet, sekil, faz):
    cts = list(tr.index)
    y = np.array([olcum[c]['ogle_min'] for c in cts])
    egri = np.array([olcum[c]['isgunu'] / olcum[c]['isgunu'].max() for c in cts])
    temel = np.column_stack([np.log(tr.musteri), np.log(tr.kva), tr.panelli / tr.musteri,
                             np.log(tr.hat_m), tr.havai_pay, tr.uc_faz_pay])
    sonuc = []
    for n in DENEY_N:
        for yol in ('rastgele', 'tabakali'):
            for t in range(TEKRAR):
                rng = random.Random(1000 * n + t + (0 if yol == 'rastgele' else 500))
                sec = (np.array(sorted(rng.sample(range(len(cts)), n))) if yol == 'rastgele'
                       else sec_tabakali(temel, n, rng))
                hedef = np.setdiff1d(np.arange(len(cts)), sec)
                tipler = tip_sayilari(ozet, sekil, faz, [cts[i] for i in sec], t).reindex(cts, fill_value=0)
                tip_pay = tipler.to_numpy() / tr.musteri.to_numpy()[:, None]
                girdi = {
                    'a': (temel, tr[['musteri']].to_numpy(float)),
                    'b': (np.hstack([temel, tip_pay]), tipler.to_numpy(float)),
                    'c': (np.column_stack([temel, np.log1p(tr.fatura_kwh / tr.musteri)]),
                          tr[['fatura_kwh']].to_numpy(float)),
                }
                for ad, (X, B) in girdi.items():
                    orta, alt, ust, gv = calistir(X, B, y, egri, sec, hedef)
                    for j, h in enumerate(hedef):
                        sonuc.append(dict(n=n, yol=yol, tekrar=t, girdi=ad, ct=cts[h], y=y[h], tah=orta[j],
                                          alt=alt[j], ust=ust[j], guven=gv[j]))
                kiyas = y[sec].sum() / tr.musteri.to_numpy()[sec].sum() * tr.musteri.to_numpy()[hedef]
                for j, h in enumerate(hedef):
                    sonuc.append(dict(n=n, yol=yol, tekrar=t, girdi='kiyas', ct=cts[h], y=y[h], tah=kiyas[j],
                                      alt=np.nan, ust=np.nan, guven=''))
    s = pd.DataFrame(sonuc)
    s['hata'] = (s.tah - s.y).abs() / s.y
    s['kapsar'] = (s.y >= s.alt) & (s.y <= s.ust)
    return s


def ozetle(s):
    g = s.groupby(['girdi', 'n', 'yol'])
    t = pd.DataFrame({'ortanca_%': g.hata.median() * 100, 'P90_%': g.hata.quantile(.9) * 100,
                      'kapsama_%': g.kapsar.mean() * 100}).round(1)
    gv = s[s.girdi != 'kiyas'].groupby(['girdi', 'guven']).agg(
        adet=('hata', 'size'), ortanca_pct=('hata', lambda h: round(h.median() * 100, 1)),
        P90_pct=('hata', lambda h: round(h.quantile(.9) * 100, 1)))
    return t, gv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('gis')
    ap.add_argument('--hazirlik', action='store_true')
    ap.add_argument('--cikti', default=None)
    a = ap.parse_args()
    d, say = oku(a.gis)
    tr, olcum, sy = trafo_tablosu(a.gis, d)
    bos = [c for c in tr.index if c not in olcum or tr.loc[c, 'fatura_kwh'] == 0]
    say['cikarilan_trafo'] = bos
    tr = tr.drop(bos)
    say['trafo'] = len(tr)
    say['ogle_min_kw'] = [round(min(olcum[c]['ogle_min'] for c in tr.index), 1),
                          round(max(olcum[c]['ogle_min'] for c in tr.index), 1)]
    say['verilen_en_cok_kw'] = round(max(olcum[c]['verilen'] for c in tr.index), 2)
    say['panelli_sayac'] = int(tr.panelli.sum())
    print(json.dumps(say, ensure_ascii=False, indent=1, default=str))
    print(tr.round(2).to_string())
    if a.hazirlik:
        return
    ld = pd.read_excel(Path(a.gis) / 'load.xlsx', sheet_name='Load', engine='calamine')
    faz = (ld.set_index('Referencia').Fases != 'M').astype(float)
    faz = faz[~faz.index.duplicated()]
    ozet, sekil = sayac_ozellik(sy[sy['Codigo Ct'].isin(tr.index)])
    s = deney(tr, olcum, ozet, sekil, faz)
    t, gv = ozetle(s)
    print(t.to_string())
    print(gv.to_string())
    if a.cikti:
        s.to_csv(a.cikti, index=False)


if __name__ == '__main__':
    main()
