#!/usr/bin/env python3
"""Sahte Kıb-Tek tepe kayıtları (Muhittin 4 madde 3; ADR-0018; BAŞLA 00:16 madde 3; BUILD 1): gerçek veri gelene kadar
yük haritasının "Kıb-Tek tepe verisi gelince" yolunu deneme şehrinde kurmak için. Kayıtlar gerçeğe yakın kusurlarıyla;
veri gelince yalnız dosya değişir (Volkan 31 Ekim 23:00: "mock veriyle, gerçeğe yakın").

Okur (yalnız üretici çıktısı; gerçek kaydın yerine): cevap_anahtari.csv (`tepe_yaz_kw`), yuk_5dk_yaz.csv (yaz penceresi),
trafolar.csv (konum, montaj).
Yazar (sözleşme §8 adayı): kibtek_tepe.csv (trafo tepe kayıtları), kibtek_fider.csv (OG fider tepesi).

Kayıt türleri ve kusurları (hepsi [Yorum]; Kıb-Tek'in elindeki kayıtların türü ve doğruluğu BULAMADIM, uzmana soru):
  md_kaydi  Trafo maksimum talep göstergesi (sürüklenen ibreli ampermetre ya da sayaç yazmacı): sezonun en yükseği, zamanı
            yok. Yer tipi trafoların MD_PAY_YER'inde, direk tipinin MD_PAY_DIREK'inde var. Ölçüm hatası N(0; MD_HATA).
            Kayıtların ESKI_PAY'ı sıfırlanmamış ya da eski yılın: × U(0,70; 0,95) (az gösterir, güvensiz yön).
  etut      Yaz yük etüdü (pens ampermetre, örneklem): MD'si olmayan trafoların ETUT_PAY'ında, yaz haftasının rastgele bir
            akşamında (20:00–23:00) tek okuma, zamanıyla; hata N(0; ETUT_HATA). Tepe değil, o anın yükü.
  fider     OG fider tepesi (merkez SCADA): şehrin trafoları konuma göre FIDER_SAYISI fidere bölünür; fider tepesi = yaz
            penceresinde üye trafoların net yük toplamının en yükseği × (1 + KAYIP) × (1 + N(0; FIDER_HATA)), zamanıyla.

Çalıştırma:
  python3 src/sahte_tepe_kaydi.py data/synthetic --aralik 1-10
"""
import argparse
import csv
import random
from pathlib import Path

import numpy as np
import pandas as pd

MD_PAY_YER, MD_PAY_DIREK = 0.6, 0.1     # MD göstergesi olan trafo payı [Yorum]
MD_HATA = 0.05                          # [Yorum]
ESKI_PAY = 0.10                         # eski / sıfırlanmamış kayıt payı [Yorum]
ESKI_CARPAN = (0.70, 0.95)
ETUT_PAY = 0.15                         # MD'si olmayanlarda etüt örneklemi [Yorum]
ETUT_HATA = 0.08
ETUT_SAAT = (20, 23)
FIDER_SAYISI = 5
KAYIP = 0.03                            # trafo + OG kaybı, fider tepesine [Yorum]
FIDER_HATA = 0.02
TEPE_SUTUNLARI = ['sehir', 'trafo_no', 'kaynak', 'tepe_kw', 'zaman']
FIDER_SUTUNLARI = ['sehir', 'fider_no', 'trafolar', 'tepe_kw', 'zaman']


def fiderlere_bol(tr, k, rng):
    """Konuma göre k fider (k-means, birkaç tur; trafo sırası tohumla)."""
    xy = tr[['x_m', 'y_m']].to_numpy(float)
    merkez = xy[rng.sample(range(len(xy)), k)]
    for _ in range(20):
        et = ((xy[:, None] - merkez[None]) ** 2).sum(-1).argmin(1)
        merkez = np.array([xy[et == j].mean(0) if (et == j).any() else merkez[j] for j in range(k)])
    return et


def sehir_yaz(klasor, tohum_ek='tepe-kayit'):
    tr = pd.read_csv(klasor / 'trafolar.csv', encoding='utf-8')
    sehir = int(tr['sehir'].iloc[0])
    rng = random.Random(f'{tohum_ek}-{sehir}')
    cevap = pd.read_csv(klasor / 'cevap_anahtari.csv', encoding='utf-8').set_index('trafo_no')
    yaz = pd.read_csv(klasor / 'yuk_5dk_yaz.csv', encoding='utf-8',
                      usecols=['trafo_no', 'tarih', 'saat', 'net_kw'])
    yaz['zaman'] = yaz['tarih'] + 'T' + yaz['saat']
    kayit = []
    for _, r in tr.iterrows():
        t = r['trafo_no']
        pay = MD_PAY_YER if r['montaj'] == 'yer' else MD_PAY_DIREK
        if rng.random() < pay:
            v = float(cevap.loc[t, 'tepe_yaz_kw']) * (1 + rng.gauss(0, MD_HATA))
            if rng.random() < ESKI_PAY:
                v *= rng.uniform(*ESKI_CARPAN)
            kayit.append(dict(sehir=sehir, trafo_no=t, kaynak='md_kaydi', tepe_kw=round(v, 2), zaman=''))
        elif rng.random() < ETUT_PAY:
            g = yaz[(yaz['trafo_no'] == t) & yaz['saat'].str[:2].astype(int).between(ETUT_SAAT[0], ETUT_SAAT[1] - 1)]
            s = g.iloc[rng.randrange(len(g))]
            kayit.append(dict(sehir=sehir, trafo_no=t, kaynak='etut', tepe_kw=round(float(s['net_kw']) * (1 + rng.gauss(0, ETUT_HATA)), 2),
                              zaman=s['zaman']))
    et = fiderlere_bol(tr, FIDER_SAYISI, rng)
    toplam = yaz.pivot_table(index='zaman', columns='trafo_no', values='net_kw', aggfunc='sum')
    fider = []
    for j in range(FIDER_SAYISI):
        uye = list(tr['trafo_no'][et == j])
        if not uye:
            continue
        s = toplam[uye].sum(axis=1)
        fider.append(dict(sehir=sehir, fider_no=f'F{j + 1}', trafolar=';'.join(uye),
                          tepe_kw=round(float(s.max()) * (1 + KAYIP) * (1 + rng.gauss(0, FIDER_HATA)), 2), zaman=s.idxmax()))
    for ad, sut, sat in (('kibtek_tepe.csv', TEPE_SUTUNLARI, kayit), ('kibtek_fider.csv', FIDER_SUTUNLARI, fider)):
        with open(klasor / ad, 'w', encoding='utf-8', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=sut, lineterminator='\n')
            w.writeheader()
            w.writerows(sat)
    return kayit, fider


def main():
    ap = argparse.ArgumentParser(description='Sahte Kıb-Tek tepe kayıtları (Muhittin 4 m. 3).')
    ap.add_argument('kok', type=Path)
    ap.add_argument('--aralik', required=True, help='ör. 1-10')
    a = ap.parse_args()
    i, j = map(int, a.aralik.split('-'))
    for s in range(i, j + 1):
        k, f = sehir_yaz(a.kok / f'sehir-{s:03d}')
        print(f'sehir-{s:03d}: md {sum(x["kaynak"] == "md_kaydi" for x in k)}, etüt {sum(x["kaynak"] == "etut" for x in k)}, '
              f'fider {len(f)}')


if __name__ == '__main__':
    main()
