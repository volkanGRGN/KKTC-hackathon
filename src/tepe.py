#!/usr/bin/env python3
"""Akşam / yılın tepesi, ön sürüm (Faz 11, ADR-0014, ADR-0018): her trafoda yılın net tepesi (kW, kVA), saati, ayı ve
geniş bandı; "ön" etiketli. Öğlen yükü sablon.py'de kalır (ADR-0018 m. 7); bu dosya yük haritasının "trafo ne kadar dolu"
sorusu.

Yöntem (ADR-0018 m. 1–4, 6; BUILD 1):
  1 Önsel eğri (Kıb-Tek'in bildiğiyle, her trafoda): abone karışımı tarife sınıflarına, sınıf enerjisi (yoksa tarife
    ortalaması) faturaya ölçeklenir; her sınıfın EAC 2022 ay tipik günü (Güney Kıbrıs, açık veri; ADR-0004) × sınıfın
    yıllık ortalama kW'ı, eksi güneş (panel kW × ayın saatlik ortalama ışınımı × PR_GUNES). Şablonun büyüklüğü faturadan.
  2 Ölçülü trafolar (sablon.py'nin tabakalı seçtiği 12'si; bugün yalnız Nisan ölçümü var) önseli ölçüye bağlar:
    R = ölçülen Nisan net tepesi ÷ önselin Nisan tepesi. Ölçülmeyen trafo R'lerin geometrik ortalamasını alır, ölçülü kendi R'sini.
    Eşzamanlılık yuvası (ADR-0018 m. 5, Can'ın B-Y2'si): bugün R abone sayısına bağlı değil.
  3 Yıl taraması: Haziran–Eylül ve Ocak–Şubat'ın her ayı (ve Nisan) için ayın tipik günü × sıcaklık terimi
    (1 ± eğim × ΔT; ΔT = hava yılında ayın en sıcak / en soğuk gününün ay ortalamasından farkı; tasarım kipinde + TASARIM_EK_C),
    iş günü ve tatil; en büyük net değer tepe, saati ve ayı (tepe anı saate kilitlenmez; ADR-0014).
    Eğim (ADR-0018 m. 4): sınıfın EAC ay tipik günü tepesinin Lefkoşa ay ortalama sıcaklığına regresyonu (yaz: Nisan–Ağustos,
    kış: Kasım–Mart), Temmuz / Ocak tepesine göre [Hesap: EAC 2022 × Open-Meteo 2023–2025 ay ortalaması; yıllar farklı, Yorum].
  4 Bant (ADR-0018 m. 2): İspanya Mayıs tepesinin bir-dışarıda log artıkları (edp_test.py --hedef tepe; BANT_LOG, K_TEPE)
    ⊕ eğim belirsizliği (eğim × EGIM_ARALIK ile yeniden tarama). Farazi şehre uydurulmaz. Haritanın "yük için boş" sayısı
    P90 tepeden (`bos_kva_p10`; ADR-0018 m. 6).
  Etiket (ADR-0018 m. 3): `guven` = on, `kor_nokta` = "mayis_temmuz;klima_kuyrugu": gerçek veri bahar, Kıbrıs'ın bağlayıcı tepesi
  yaz akşamı; sıcak dalga kuyruğu ölçülmedi.

Farazi sınav uyarısı: üretici de yazı EAC ay tipik günleriyle kuruyor; model aynı açık veriyi kullandığı için farazi tepe
sınavı iyimser (ADR-0008), eğim hatasını ve "Kuzey ≠ Güney Kıbrıs"ı görmez. Gerçek ölçü İspanya Mayıs (sinav.py faz2).

Okur: trafolar.csv (hepsi), yuk_5dk.csv (YALNIZ ölçülülerin satırları), ayar.json'dan yalnız `hava_yili` (hangi yıl; Kıb-Tek
bilir), Open-Meteo Lefkoşa saatlik dosyaları. cevap_anahtari.csv'yi okumaz.
Yazar: tepe.csv (sözleşme 1.4 adayı, satır = trafo), tepe_ozet.json (bilgi).

Çalıştırma:
  python3 src/tepe.py data/synthetic --aralik 1-10            # her şehirde tepe.csv
  python3 src/tepe.py data/synthetic --aralik 1-10 --hava tasarim
"""
import argparse
import calendar
import csv
import datetime as dt
import json
import math
import statistics
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import profiller  # noqa: E402  EAC sınıf eğrileri (Can'ın okuyucusu)

KOK = Path(__file__).resolve().parent.parent
HAVA_DOSYALARI = [KOK / 'data' / 'raw' / 'open-meteo-lefkosa' / ad
                  for ad in ('lefkosa_saatlik_2023.csv', 'lefkosa_saatlik_2024_2025.csv')]
ADIM = 288
ABONE = ['abone_konut', 'abone_ticari1', 'abone_ticari2', 'abone_turizm',
         'abone_sanayi1', 'abone_sanayi2', 'abone_su_motoru']
# Abone sütunu -> EAC sınıfı. Ticari II tarifesi büyük ticaret sayıldı: tarifesi ticari II olan yurt (akşam tepeli) yanlış
# eğriyi alır; Kıb-Tek tarife sınıfını bilir, yapı tipini bilmez [Yorum].
SINIF = {'abone_konut': 'konut', 'abone_ticari1': 'kucuk_ticari', 'abone_ticari2': 'buyuk_ticari',
         'abone_turizm': 'otel', 'abone_sanayi1': 'kucuk_sanayi', 'abone_sanayi2': 'buyuk_sanayi',
         'abone_su_motoru': 'su_pompasi'}
# Abone başına yıllık MWh (sablon.py MWH ile aynı kaynak: Kıb-Tek 2023 tarife tüketimi ÷ abone) [Hesap]
MWH = {'abone_konut': 648494 / 175577, 'abone_ticari1': 210978 / 20950, 'abone_ticari2': 169496 / 494,
       'abone_turizm': 215147 / 171, 'abone_sanayi1': 22391 / 1227, 'abone_sanayi2': 95996 / 352,
       'abone_su_motoru': 51256 / 3250}
YAZ, KIS, NISAN = (6, 7, 8, 9), (1, 2), 4
YAZ_EGIM_AYLARI, KIS_EGIM_AYLARI = (4, 5, 6, 7, 8), (11, 12, 1, 2, 3)
PR_GUNES = 0.80                        # panel performans oranı [Yorum]
PF = 0.95                              # güç katsayısı [varsayım; ADR-0014]
SICAKLIK_TABAN = 0.6                   # sıcaklık çarpanı en az [Yorum]
EGIM_ARALIK = (0.5, 2.0)               # eğim belirsizliği: yarısı – iki katı [Yorum; ADR-0018 m. 4 "geniş aralık"]
TASARIM_EK_C = 2.0                     # tasarım kipi: hava yılının uç gününe + 2 °C (10 yılda bir sıcak akşam vekili)
                                       # [Yorum; Lefkoşa uzun seri BULAMADIM, yalnız 2023–2025 elde]
# Bant tabanı (ADR-0018 m. 2): İspanya Mayıs tepesi (EDP Oviedo 2018, 28 trafo), girdi c (fatura), tabakalı 10 + 15 ölçülü,
# bir-dışarıda log artıkları ln(gerçek ÷ tahmin): P10 −0,218, ortanca −0,041, P90 +0,420 (660 satır) [Hesap: edp_test.py
# --hedef tepe --kalibrasyonsuz]. Sağa çarpık: gerçek tepe tahminin %52 üstüne çıkabiliyor; bant simetrik yapılmaz (güvenli
# yön üstte). Kıbrıs trafosunun bandı doğrudan bu nicellerden (+ eğim belirsizliği). Günlük docs/log/2026-11-01-volkan-yuk-tepe-on.md.
BANT_LOG = (-0.218, 0.420)
# edp_test.py'nin kendi bir-dışarıda bandının şişirme katsayısı (İspanya satırları, sinav.py --ispanya-tepe): k 1,164 →
# bir-dışarıda %80 kapsama %75,5 → %78,8 [Hesap: kalibrasyon.py ispanya, girdi c, 10 + 15, tabakalı]. Yalnız edp_test.py.
K_TEPE = 1.164
OLCULU_ANA = 12                        # sablon.py ile aynı (ölçüm cihazı takılan trafolar)
KOR_NOKTA = 'mayis_temmuz;klima_kuyrugu'
TEPE_SUTUNLARI = ['sehir', 'trafo_no', 'olculdu', 'tepe_kw', 'tepe_kw_p10', 'tepe_kw_p90', 'tepe_saati', 'tepe_ayi',
                  'pf_varsayim', 'tepe_kva', 'tepe_kva_p10', 'tepe_kva_p90', 'bos_kva', 'bos_kva_p10', 'bos_kva_p90',
                  'guven', 'kor_nokta']


# ---------- açık veri: EAC eğrileri, hava ----------

def yillik_ortalama(veri, sinif):
    """24 tipik günün 2022 takvimine göre ağırlıklı ortalaması (cumartesi, pazar tatil; bayram yok sayıldı)."""
    toplam, gun = 0.0, 0
    for ay in range(1, 13):
        for g in range(1, calendar.monthrange(2022, ay)[1] + 1):
            toplam += float(np.mean(profiller.sinif_egrisi(veri, sinif, ay, 'tatil' if dt.date(2022, ay, g).weekday() >= 5
                                                          else 'is')))
            gun += 1
    return toplam / gun


def eac_hazirla():
    """{(sınıf, ay, gün türü): 288 değer, sınıfın yıllık ortalaması = 1}."""
    veri = profiller.oku()
    out = {}
    for c in set(SINIF.values()):
        o = yillik_ortalama(veri, c)
        for ay in range(1, 13):
            for g in ('is', 'tatil'):
                out[(c, ay, g)] = np.array(profiller.sinif_egrisi(veri, c, ay, g)) / o
    return out


def hava_oku():
    """{tarih: (24 sıcaklık °C, 24 ışınım W/m²)}; yalnız 24 saati tam günler."""
    gun = {}
    for yol in HAVA_DOSYALARI:
        if not yol.exists():
            continue
        with open(yol, encoding='utf-8', newline='') as fh:
            satir = list(csv.reader(fh))
        bas = next(i for i, r in enumerate(satir) if r and r[0] == 'time')
        bas_sat = satir[bas]
        it, ig = bas_sat.index('temperature_2m (°C)'), bas_sat.index('shortwave_radiation (W/m²)')
        for r in satir[bas + 1:]:
            if not r or not r[it] or not r[ig]:
                continue
            z = dt.datetime.fromisoformat(r[0])
            t, g = gun.setdefault(z.date(), ([None] * 24, [None] * 24))
            t[z.hour], g[z.hour] = float(r[it]), float(r[ig])
    return {d: (t, g) for d, (t, g) in gun.items() if None not in t and None not in g}


def egimler(eac, hava):
    """Sınıf başına göreli tepe–sıcaklık eğimi (°C başına), yaz ve kış. EAC ay tipik günü tepesi (iş günü) ~ Lefkoşa ay
    ortalama sıcaklığı (elde olan yılların ortalaması), doğrusal; Temmuz / Ocak tepesine bölünür; en az 0."""
    Tay = {m: statistics.fmean(statistics.fmean(t) for d, (t, _) in hava.items() if d.month == m) for m in range(1, 13)}
    out = {}
    for c in set(SINIF.values()):
        tep = {m: float(eac[(c, m, 'is')].max()) for m in range(1, 13)}
        b_yaz = statistics.linear_regression([Tay[m] for m in YAZ_EGIM_AYLARI], [tep[m] for m in YAZ_EGIM_AYLARI]).slope
        b_kis = statistics.linear_regression([Tay[m] for m in KIS_EGIM_AYLARI], [tep[m] for m in KIS_EGIM_AYLARI]).slope
        out[c] = dict(yaz=max(0.0, b_yaz / tep[7]), kis=max(0.0, -b_kis / tep[1]))
    return out, Tay


def ay_kosullari(hava, yil, kip):
    """Ay başına sıcaklık sapması ΔT (°C, ≥ 0: yazın en sıcak günün, kışın en soğuk günün ay ortalamasından farkı) ve
    ayın saatlik ortalama ışınımı (288 adım). kip 'tasarim': ΔT + TASARIM_EK_C."""
    out = {}
    for m in (NISAN,) + YAZ + KIS:
        gunler = [d for d in hava if d.year == yil and d.month == m]
        if not gunler:
            continue
        gt = [statistics.fmean(hava[d][0]) for d in gunler]
        ort = statistics.fmean(gt)
        dT = 0.0 if m == NISAN else (max(gt) - ort if m in YAZ else ort - min(gt))
        if kip == 'tasarim' and m != NISAN:
            dT += TASARIM_EK_C
        ghi = np.array([statistics.fmean(hava[d][1][h] for d in gunler) for h in range(24)])
        out[m] = dict(dT=dT, ghi=np.repeat(ghi, ADIM // 24), gun=len(gunler))
    return out


# ---------- önsel ----------

def sinif_kw(tr):
    """Trafo × sınıf yıllık ortalama kW. Fatura (yillik_tuketim_mwh) varsa sınıf enerjileri faturaya ölçeklenir."""
    E = np.column_stack([tr[a].fillna(0).to_numpy(float) * MWH[a] for a in ABONE])      # MWh/yıl
    if 'yillik_tuketim_mwh' in tr and tr['yillik_tuketim_mwh'].notna().all():
        top = E.sum(1)
        E = E * np.divide(tr['yillik_tuketim_mwh'].to_numpy(float), top, out=np.ones_like(top), where=top > 0)[:, None]
    return E / 8.76


def net_egri(kw, eac, ay, g, dT, egim, carp, panel_kw, ghi, mevsim):
    """Bir trafonun ayın tipik günü net yükü (288, kW)."""
    out = np.zeros(ADIM)
    for j, a in enumerate(ABONE):
        if kw[j] <= 0:
            continue
        c = SINIF[a]
        f = 1.0 if mevsim is None else max(SICAKLIK_TABAN, 1 + egim[c][mevsim] * carp * dT)
        out += kw[j] * eac[(c, ay, g)] * f
    return out - panel_kw * ghi / 1000 * PR_GUNES


def tarama(kw, panel_kw, eac, kosul, egim, carp=1.0):
    """Yıl taraması: Nisan + yaz ayları + kış ayları, iş günü ve tatil; en büyük net değer. -> (kW, adım, ay)."""
    en = (-math.inf, 0, 0)
    for m, k in kosul.items():
        mev = None if m == NISAN else ('yaz' if m in YAZ else 'kis')
        for g in ('is', 'tatil'):
            e = net_egri(kw, eac, m, g, k['dT'], egim, carp, panel_kw, k['ghi'], mev)
            i = int(e.argmax())
            if e[i] > en[0]:
                en = (float(e[i]), i, m)
    return en


def nisan_tepesi(kw, panel_kw, eac, kosul, egim):
    k = kosul[NISAN]
    return max(float(net_egri(kw, eac, NISAN, g, 0.0, egim, 1.0, panel_kw, k['ghi'], None).max()) for g in ('is', 'tatil'))


# ---------- şehir ----------

def eszamanlilik(n_abone):
    """Eşzamanlılık yuvası (ADR-0018 m. 5): Can'ın B-Y2'si iki bileşenli (taban √N, klima ~doğrusal) düzeltmeyi buraya
    getirir. Ön sürümde 1: R ölçülü trafoların ortalamasından, abone sayısına bağlı değil [Yorum]."""
    return np.ones_like(np.asarray(n_abone, float))


def sehir_calistir(klasor, eac, hava, egim, kip='yil'):
    from sablon import ogretici_sec          # ölçülü küme sablon.py ile aynı (ürünün tabakalı seçimi)
    tr = pd.read_csv(klasor / 'trafolar.csv', encoding='utf-8')
    sehir = int(tr['sehir'].iloc[0])
    with open(klasor / 'ayar.json', encoding='utf-8') as fh:
        yil = int(json.load(fh)['hava_yili'])     # yalnız yıl; üreticinin gizli ayarları okunmaz
    kosul = ay_kosullari(hava, yil, kip)
    eksik = [m for m in (NISAN,) + YAZ + KIS if m not in kosul]
    if eksik:
        raise SystemExit(f'sehir-{sehir:03d}: {yil} hava verisi eksik (aylar {eksik}); data/raw/open-meteo-lefkosa')
    secilen = ogretici_sec(tr, OLCULU_ANA, f'sec-{sehir}')
    ids = [tr['trafo_no'].iloc[i] for i in secilen]
    yuk = pd.read_csv(klasor / 'yuk_5dk.csv', encoding='utf-8', usecols=['trafo_no', 'net_kw'])
    y = yuk[yuk['trafo_no'].isin(ids)].groupby('trafo_no')['net_kw'].max()          # model yalnız bunu görür

    KW = sinif_kw(tr)
    panel = tr['panel_kw'].fillna(0).to_numpy(float)
    n_abone = tr[ABONE].fillna(0).sum(axis=1).to_numpy(float)
    R = {}
    for i in secilen:
        p = nisan_tepesi(KW[i], panel[i], eac, kosul, egim)
        R[tr['trafo_no'].iloc[i]] = float(y[tr['trafo_no'].iloc[i]]) / max(p, 0.1)
    logR = np.log(list(R.values()))
    R_ort = float(np.exp(logR.mean()))
    # bir-dışarıda (bilgi): ölçülü trafonun Nisan tepesi öbürlerinin R'siyle
    loo = [float(np.log(R[t]) - (logR.sum() - np.log(R[t])) / (len(logR) - 1)) for t in R]

    satirlar = []
    lo_k, hi_k = BANT_LOG
    for i, t in enumerate(tr['trafo_no']):
        ham, adim, ay = tarama(KW[i], panel[i], eac, kosul, egim)
        ham_lo = tarama(KW[i], panel[i], eac, kosul, egim, EGIM_ARALIK[0])[0]
        ham_hi = tarama(KW[i], panel[i], eac, kosul, egim, EGIM_ARALIK[1])[0]
        olc = t in R
        r = R[t] if olc else R_ort * float(eszamanlilik(n_abone[i]))
        tepe = max(r * ham, 0.0)
        s_lo = math.log(max(ham_lo, 1e-6) / max(ham, 1e-6))
        s_hi = math.log(max(ham_hi, 1e-6) / max(ham, 1e-6))
        a = 0.0 if olc else lo_k                   # ölçülünün Nisan'ı biliniyor; yazı yalnız eğimle belirsiz
        b = 0.0 if olc else hi_k
        p10 = tepe * math.exp(-math.hypot(a, min(s_lo, 0.0)))
        p90 = tepe * math.exp(math.hypot(b, max(s_hi, 0.0)))
        kva = float(tr['kva'].iloc[i])
        satirlar.append(dict(
            sehir=sehir, trafo_no=t, olculdu=int(olc), tepe_kw=round(tepe, 2), tepe_kw_p10=round(p10, 2),
            tepe_kw_p90=round(p90, 2), tepe_saati=f'{adim * 5 // 60:02d}:{adim * 5 % 60:02d}', tepe_ayi=ay,
            pf_varsayim=PF, tepe_kva=round(tepe / PF, 2), tepe_kva_p10=round(p10 / PF, 2), tepe_kva_p90=round(p90 / PF, 2),
            bos_kva=round(kva - tepe / PF, 2), bos_kva_p10=round(kva - p90 / PF, 2), bos_kva_p90=round(kva - p10 / PF, 2),
            guven='on', kor_nokta=KOR_NOKTA))
    with open(klasor / 'tepe.csv', 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=TEPE_SUTUNLARI, lineterminator='\n')
        w.writeheader()
        w.writerows(satirlar)
    ozet = dict(sehir=sehir, hava_yili=yil, kip=kip, olculu=ids, R={t: round(v, 3) for t, v in R.items()},
                R_ortalama=round(R_ort, 3), R_bir_disarida_log_artik=[round(x, 3) for x in loo],
                egim={c: {k: round(v, 4) for k, v in e.items()} for c, e in egim.items()},
                dT={m: round(k['dT'], 1) for m, k in kosul.items()}, bant_log=[lo_k, hi_k], egim_aralik=list(EGIM_ARALIK),
                pr_gunes=PR_GUNES, pf=PF, kor_nokta=KOR_NOKTA)
    with open(klasor / 'tepe_ozet.json', 'w', encoding='utf-8', newline='') as fh:
        json.dump(ozet, fh, ensure_ascii=False, indent=1)
    return satirlar, ozet


def main():
    ap = argparse.ArgumentParser(description='Yılın tepesi, ön sürüm (Faz 11, ADR-0018).')
    ap.add_argument('kok', type=Path)
    ap.add_argument('--aralik', default=None, help='ör. 1-10 (yoksa kökteki bütün sehir-* klasörleri)')
    ap.add_argument('--hava', choices=['yil', 'tasarim'], default='yil',
                    help="yil: şehrin hava yılı (sınav); tasarim: + TASARIM_EK_C (harita)")
    a = ap.parse_args()
    if a.aralik:
        i, j = map(int, a.aralik.split('-'))
        klasorler = [a.kok / f'sehir-{s:03d}' for s in range(i, j + 1)]
    else:
        klasorler = sorted(a.kok.glob('sehir-*'))
    eac, hava = eac_hazirla(), hava_oku()
    egim, _ = egimler(eac, hava)
    for k in klasorler:
        s, o = sehir_calistir(k, eac, hava, egim, a.hava)
        print(f"{k.name}: {len(s)} trafo; R ortalama {o['R_ortalama']}; tepe ayı "
              f"{dict(sorted(pd.Series([r['tepe_ayi'] for r in s]).value_counts().items()))}")


if __name__ == '__main__':
    main()
