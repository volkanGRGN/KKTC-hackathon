#!/usr/bin/env python3
"""Farazi şehir ↔ gerçek veri (İspanya EDP) karşılaştırması: trafolar arası çeşitlilik ölçüleri (ADR-0008, ADR-0009).

Bu dosya Can'ın. Model kurmaz; iki veri kümesinde aynı üç ölçüyü yan yana koyar:
  1. Müşteri başına öğlen en düşük yükün trafodan trafoya değişim katsayısı (CV = ss ÷ ortalama).
  2. Eğri benzerliği: trafonun iş günü saatlik ortalama eğrisinin (ortalamasına bölünmüş) aynı kümedeki
     trafoların ortalama eğrisiyle Pearson korelasyonu; ortanca. 1'e yakın = bütün trafolar aynı şekil.
  3. Saf tahmin (bir-trafo-dışarıda): kalan trafolarda Σ öğlen ÷ Σ müşteri × bu trafonun müşterisi;
     |tahmin − gerçek| ÷ gerçek, ortanca ve P90. Model yok; "müşteri sayısı ne kadar açıklıyor".
Öğlen = 11:00–14:00. Farazi tarafta müşteri = abone (7 sütunun toplamı), gerçek tarafta load.xlsx sayaç sayısı.

Gerçek veri okuma ve temizlik BUILD'in src/edp_test.py'siyle aynı kurallar (PR #10, docs/log/2026-10-31-volkan-edp-gercek.md):
ondalık virgül (≥ 1000 → ÷ 1000), Estado ≠ 0 ve Tipo proceso ≠ A atılır, 21 Mayıs (yarım gün) atılır, doğru cevap
trafo başı ölçüm cihazı (Referencia "ZIVS…"), 1 Mayıs tatil. Ham veri depoda yok: data/raw/edp-oviedo/KAYNAK.txt.

Çalıştırma: python3 src/edp_kiyas.py <EDP GIS_data klasörü> <farazi şehir kökü, ör. data/synthetic>
Etiket: gerçek taraf "gerçek veri — İspanya"; farazi taraf "gösterim".
"""
import csv
import statistics as st
import sys
from pathlib import Path

import pandas as pd

try:
    import python_calamine  # noqa: F401  hızlı Excel okuyucu (BUILD'in edp_test.py'si de kullanıyor)
    MOTOR = 'calamine'
except ImportError:
    MOTOR = 'openpyxl'                    # requirements.txt'de; ilk okuma birkaç dakika sürer

OGLE_SAAT = (11, 12, 13)
TATIL_EDP = {pd.Timestamp('2018-05-01')}     # İşçi Bayramı, İspanya ulusal tatili [Kaynaklı]
ABONE = ['abone_konut', 'abone_ticari1', 'abone_ticari2', 'abone_turizm', 'abone_sanayi1', 'abone_sanayi2',
         'abone_su_motoru']


def _cv(x):
    return st.pstdev(x) / st.mean(x)


def _p90(x):
    return st.quantiles(x, n=10, method='inclusive')[-1]


def _korelasyon(a, b):
    ma, mb = st.mean(a), st.mean(b)
    pay = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    return pay / (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5


def benzerlik(egriler):
    """Eğri listesi (24 saat) -> her eğrinin grup ortalamasıyla korelasyonu."""
    n = [[v / st.mean(e) for v in e] for e in egriler]
    ort = [st.mean(s) for s in zip(*n)]
    return [_korelasyon(e, ort) for e in n]


def saf_hata(ogle, musteri):
    """Bir-trafo-dışarıda saf tahmin hataları."""
    top_o, top_m = sum(ogle), sum(musteri)
    return [abs((top_o - o) / (top_m - m) * m - o) / o for o, m in zip(ogle, musteri)]


# ---------- gerçek veri: EDP ----------

def edp_oku(G):
    """-> {trafo merkezi: dict(musteri, ogle_min, egri)}; temizlik sayıları."""
    G = Path(G)
    onb = G.parent / 'edp_kiyas_olcum.pkl'
    if onb.exists():
        d = pd.read_pickle(onb)
    else:
        d = pd.concat([pd.read_excel(G / f'file{i}.xlsx', engine=MOTOR,
                                     usecols=['Codigo Ct', 'Referencia', 'Fecha', 'Activa E', 'Estado', 'Tipo proceso'])
                       for i in range(1, 8)], ignore_index=True)
        d['Fecha'] = pd.to_datetime(d['Fecha'])
        d.to_pickle(onb)
    say = dict(satir=len(d))
    d['Activa E'] = pd.to_numeric(d['Activa E'].astype(str).str.replace(',', '.'), errors='coerce')
    say['virgul'] = int((d['Activa E'] >= 1000).sum())
    d.loc[d['Activa E'] >= 1000, 'Activa E'] /= 1000
    kotu = (d['Estado'].astype(str) != '0') | (d['Tipo proceso'] != 'A') | d['Activa E'].isna()
    say['atilan'] = int(kotu.sum())
    d = d[~kotu & (d.Fecha < '2018-05-21')]
    bas = d.Referencia.astype(str).str.startswith('ZIVS')
    yk = d[bas].groupby(['Codigo Ct', 'Fecha'])['Activa E'].sum().unstack(0)
    fatura = d[~bas].groupby('Codigo Ct')['Activa E'].sum()
    ld = pd.read_excel(G / 'load.xlsx', sheet_name='Load', engine=MOTOR)
    musteri = ld.groupby('Codigo Ct').size()
    gun = yk.index.normalize()
    isg = (yk.index.day_of_week < 5) & ~gun.isin(TATIL_EDP)
    ogle = yk.index.hour.isin(OGLE_SAAT)
    trafo, cik = {}, []
    for ct in yk.columns:
        x = yk[ct]
        if fatura.get(ct, 0) == 0 or not musteri.get(ct) or x[ogle].min() <= 0:
            cik.append(ct)
            continue
        egri = x[isg].groupby(x[isg].index.hour).mean().reindex(range(24)).interpolate().tolist()
        trafo[ct] = dict(musteri=int(musteri[ct]), ogle_min=float(x[ogle].min()), egri=egri)
    say['cikarilan'] = cik
    return trafo, say


# ---------- farazi şehirler ----------

def farazi_oku(kok, tip='sehir_konutu'):
    """-> {şehir: [dict(musteri, ogle_min, egri)]} (tip = None ise bütün trafolar)."""
    sonuc = {}
    for k in sorted(Path(kok).glob('sehir-*')):
        if not (k / 'yuk_5dk.csv').exists():
            continue
        with open(k / 'trafolar.csv', encoding='utf-8', newline='') as fh:
            abone = {r['trafo_no']: sum(int(r[a] or 0) for a in ABONE) for r in csv.DictReader(fh)}
        with open(k / 'cevap_anahtari.csv', encoding='utf-8', newline='') as fh:
            cevap = {r['trafo_no']: r for r in csv.DictReader(fh) if tip is None or r['tip'] == tip}
        top = {t: [0.0] * 24 for t in cevap}
        say = {t: [0] * 24 for t in cevap}
        with open(k / 'yuk_5dk.csv', encoding='utf-8', newline='') as fh:
            for r in csv.DictReader(fh):
                t = r['trafo_no']
                if t in top and r['gun_turu'] == 'isgunu':
                    h = int(r['adim']) // 12
                    top[t][h] += float(r['tuketim_kw'])
                    say[t][h] += 1
        sonuc[k.name] = [dict(musteri=abone[t], ogle_min=float(cevap[t]['ogle_min_kw']),
                              egri=[v / n for v, n in zip(top[t], say[t])])
                         for t in cevap if abone[t] and float(cevap[t]['ogle_min_kw']) > 0]
    return sonuc


def farazi_olcu(sehirler):
    cv, havuz_mo, benz, hata = [], [], [], []
    for liste in sehirler.values():
        if len(liste) < 3:
            continue
        mo = [x['ogle_min'] / x['musteri'] for x in liste]
        cv.append(_cv(mo))
        havuz_mo += mo
        benz += benzerlik([x['egri'] for x in liste])
        hata += saf_hata([x['ogle_min'] for x in liste], [x['musteri'] for x in liste])
    return dict(cv_sehir_ici=st.median(cv), cv_havuz=_cv(havuz_mo), w_musteri=1000 * st.median(havuz_mo),
                benzerlik=st.median(benz), saf_ortanca=st.median(hata), saf_p90=_p90(hata),
                trafo=sum(len(v) for v in sehirler.values()), sehir=len(cv))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 3:
        sys.exit('Kullanım: python3 src/edp_kiyas.py <EDP GIS_data klasörü> <farazi şehir kökü>')
    edp, say = edp_oku(sys.argv[1])
    t = list(edp.values())
    mo = [x['ogle_min'] / x['musteri'] for x in t]
    hata = saf_hata([x['ogle_min'] for x in t], [x['musteri'] for x in t])
    gercek = dict(cv_sehir_ici=_cv(mo), cv_havuz=_cv(mo), w_musteri=1000 * st.median(mo),
                  benzerlik=st.median(benzerlik([x['egri'] for x in t])),
                  saf_ortanca=st.median(hata), saf_p90=_p90(hata), trafo=len(t), sehir=1)
    print(f"EDP temizlik: {say['satir']} satır, ondalık virgül düzeltilen {say['virgul']}, atılan {say['atilan']}, "
          f"çıkarılan trafo {say['cikarilan']}")
    konut = farazi_olcu(farazi_oku(sys.argv[2]))
    hepsi = farazi_olcu(farazi_oku(sys.argv[2], tip=None))
    satirlar = [('müşteri başına öğlen yükü CV, şehir içi ortanca', 'cv_sehir_ici', '{:.2f}'),
                ('müşteri başına öğlen yükü CV, havuz', 'cv_havuz', '{:.2f}'),
                ('müşteri başına öğlen en düşük, ortanca (W)', 'w_musteri', '{:.0f}'),
                ('eğri benzerliği (grup ortalamasıyla korelasyon), ortanca', 'benzerlik', '{:.2f}'),
                ('saf tahmin hatası, bir-dışarıda, ortanca', 'saf_ortanca', '%{:.1%}'),
                ('saf tahmin hatası, bir-dışarıda, P90', 'saf_p90', '%{:.1%}')]
    print(f"\n| ölçü | gerçek veri — İspanya ({gercek['trafo']} trafo, karışık) | farazi, şehir konutu "
          f"({konut['trafo']} trafo, {konut['sehir']} şehir; gösterim) | farazi, bütün trafolar ({hepsi['trafo']}; gösterim) |")
    print('|---|---|---|---|')
    for ad, k, f in satirlar:
        bic = (lambda v: f'%{100 * v:.1f}') if f.startswith('%') else f.format
        print(f'| {ad} | {bic(gercek[k])} | {bic(konut[k])} | {bic(hepsi[k])} |')


if __name__ == '__main__':
    main()
