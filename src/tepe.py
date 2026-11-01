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
    Eşzamanlılık varsayılanı (ADR-0018 m. 5, Velander biçimi N·a + b·√(N·a)): R = R0 × (1 + c ÷ √n), n = trafonun enerjisi
    konut abonesi cinsinden; c ölçülülerin Nisan R'lerinden (CF(N) ölçülü trafolardan), belirsizliği banda.
    B-Y2 deneme (`--model b-y2-esz`, varsayılan değil): c 20 Kıbrıs evinin verisinden, yalnız konut payına; Nisan ölçümü R0'a
    diğer günlerin c'siyle bağlanır, yaz tepesi sıcak akşamların c'siyle (yaz eğrisi × f_sıcak ÷ f_diğer). 31–40'ta konut dışı
    tepeyi %18–26 az gösterdi (R0 konut ağırlıklı ölçülülerden düşüyor; üretici küçük-N fazlasını kurmuyor, 20 evden 100 eve
    taşıma da veri dışı) → pilot verisi gelene kadar kapalı (günlük docs/log/2026-11-01-can-eszamanlilik.md).
  3 Yıl taraması: Haziran–Eylül ve Ocak–Şubat'ın her ayı (ve Nisan) için ayın tipik günü × sıcaklık terimi
    (1 ± eğim × ΔT; ΔT = hava yılında ayın en sıcak / en soğuk gününün ay ortalamasından farkı; tasarım kipinde Lefkoşa
    2015–2025 serisinden 10 yılda bir uç günün iklim ortalamasından farkı),
    iş günü ve tatil; en büyük net değer tepe, saati ve ayı (tepe anı saate kilitlenmez; ADR-0014).
    Eğim (ADR-0018 m. 4): sınıfın EAC ay tipik günü tepesinin Lefkoşa ay ortalama sıcaklığına regresyonu (yaz: Nisan–Ağustos,
    kış: Kasım–Mart), Temmuz / Ocak tepesine göre [Hesap: EAC 2022 × Open-Meteo 2023–2025 ay ortalaması; yıllar farklı, Yorum].
    B-Y2 (varsayılan `--model b-y2`): konutun yaz eğimi 20 Kıbrıs evinden (Temmuz ölçeğinde 0,065/°C; EAC'den çıkan 0,030
    sıcak günü az gösteriyordu). `--model on`: eski ön sürüm (bütün eğimler EAC'den), kıyas için.
  4 Bant (ADR-0018 m. 2): İspanya Mayıs tepesinin bir-dışarıda log artıkları (edp_test.py --hedef tepe; BANT_LOG, K_TEPE)
    ⊕ eğim belirsizliği (eğim × EGIM_ARALIK ile yeniden tarama). Farazi şehre uydurulmaz. Haritanın "yük için boş" sayısı
    P90 tepeden (`bos_kva_p10`; ADR-0018 m. 6).
  Etiket (ADR-0018 m. 3): `guven` = on, `kor_nokta` = "mayis_temmuz;klima_kuyrugu": gerçek veri bahar, Kıbrıs'ın bağlayıcı tepesi
  yaz akşamı; sıcak dalga kuyruğu ölçülmedi.
  5 Kıb-Tek tepe verisi (Muhittin 4 m. 3; varsa `kibtek_tepe.csv`, `kibtek_fider.csv`, sözleşme §9 adayı; sahtesi
    sahte_tepe_kaydi.py): kaydı olan trafo ölçülü sayılır (R = kayıt ÷ önselin aynı andaki değeri; MD kaydı zamansız = yaz
    tepesi), tahmin kayda çöker. Popülasyon R'si ve bant kendiliğinden değişmez: kayıtlar temsilî değil (MD büyük yer tipi
    trafoda); kayıtlardan popülasyon R'si ve bant önerisi `tepe_ozet.json`'a, sürümlü yeniden-fit (tüzük m. 4) KARAR'da.
    OG fider tepesi: aşağıdan yukarı toplamla mutabakat (fider başına kayıt ÷ tahmin; kontrol). `--fider-duzelt` ölçülmeyenleri
    fider oranına ölçekler (yukarıdan aşağı); 1–10'da kötüleştirdi, varsayılan kapalı.
  7 Tepe saati (KARAR 01:30): ticari II abonesi, öğlen arketipi akşam tepeliyse konut eğrisiyle (yurt); ikinci aday saat
    (konutta öğleden sonra ↔ gece neredeyse eşit) ve dönem (sabah / öğle / öğleden sonra / gece).
  6 Akşam gerilimi (KARAR 00:57 m. 4; ADR-0014, 207 V): tepe anında en düşük ev gerilimi, panel tarafıyla aynı fizik
    (`kac_ev_olasilik.ag_kur`: Kıb-Tek'in bildiğiyle ağ, bilinmeyenler aralıktan; İngiltere'ye kalibre empedans payı;
    `trafo_bos_kapasite.solve`). Çekiliş başına: ağ, tepe bandından toplam yük, sınıfların tepe anındaki payı × kişisel fark,
    OG değişimi. Çıktı ortanca, P10 / P90 ve 207 V altına inme olasılığı.

Farazi sınav uyarısı: üretici de yazı EAC ay tipik günleriyle kuruyor; model aynı açık veriyi kullandığı için farazi tepe
sınavı iyimser (ADR-0008), eğim hatasını ve "Kuzey ≠ Güney Kıbrıs"ı görmez. Gerçek ölçü İspanya Mayıs (sinav.py faz2).

Okur: trafolar.csv (hepsi), yuk_5dk.csv (YALNIZ ölçülülerin satırları), tahmin.csv + arketipler.csv (sablon.py; arketip), ayar.json'dan yalnız `hava_yili` (hangi yıl; Kıb-Tek
bilir), Open-Meteo Lefkoşa saatlik dosyaları. cevap_anahtari.csv'yi okumaz.
Yazar: tepe.csv (sözleşme §8, 1.4 adayı, satır = trafo), tepe_ozet.json (bilgi).

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
import random
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
# Tasarım sıcaklığı (ADR-0018 m. 4; KARAR 00:50): Lefkoşa 2015–2025 saatlik sıcaklık (Open-Meteo, KAYNAK.txt); her yaz /
# kış ayında yılın en uç gününün iklim ay ortalamasından farkı, 11 yılın TASARIM_NICEL'i ("10 yılda bir" [Yorum]).
UZUN_SERI = KOK / 'data' / 'raw' / 'open-meteo-lefkosa' / 'lefkosa_sicaklik_2015_2025.csv'
TASARIM_NICEL = 0.9
# Eşzamanlılık varsayılanı (ADR-0018 m. 5; KARAR 00:50): Velander biçimi, R = R0 × (1 + c ÷ √n). n = enerji ÷ konut abonesi
# yıllık enerjisi. c ölçülü trafolardan (ızgara 0–VELANDER_C_UST); bant c = 0 ile max(2ĉ; VELANDER_C_BANT) arası [Yorum].
KONUT_MWH = 648494 / 175577
VELANDER_C_UST, VELANDER_C_BANT = 3.0, 0.5
# B-Y2 (Can, 1 Kasım; src/eszamanlilik.py, docs/log/2026-11-01-can-eszamanlilik.md) [Hesap: 20 Kıbrıs konut prosumer'ı, 2016,
# Zenodo 23043383, net yük; Lefkoşa sıcaklığı]: ev başına tepe = a (1 + c ÷ √N), N = ev; sıcak akşam (19–22 ≥ yılın P90'ı)
# c 2,51, diğer günler 4,74. n burada enerji cinsinden konut eşdeğeri; 20 evin brüt ortancası 7,21 MWh/yıl →
# c_n = c_ev × √(7,21 ÷ KONUT_MWH). c belirsizliği ×0,5–×1,5 [Yorum; 20 ev]. Konut yaz eğimi Temmuz ortalama akşamındaki
# tepeye göre °C başına 0,065 (bootstrap P10–P90 0,056–0,075); EAC'den çıkan 0,030'un yerine. Uydurma ölçülü trafolardan
# değil: farazi şehir bu sayıları sınayamaz (üretici kendi β'sıyla kuruyor; ADR-0008) [Yorum]. Varsayılan 'b-y2' yalnız eğimi
# alır; c'yi 'b-y2-esz' (deneme) kullanır.
MODEL = 'b-y2'                         # 'on': eski ön sürüm (eğim EAC'den); 'b-y2-esz': + ev çeşitliliği (deneme)
ESZ_C_EV = {'sicak': 2.51, 'diger': 4.74}
ESZ_EV_MWH = 7.21
ESZ_C_ARALIK = (0.5, 1.5)
KONUT_YAZ_EGIM = 0.065
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
# Kıb-Tek tepe kaydı (madde 5) [Yorum]: MD kaydının bandı; üst yan kayıt kalitesi ölçülene kadar en kötü kabulle geniş
# (eski / sıfırlanmamış MD × 0,70'e kadar az gösterir → +0,36; KARAR 23:47 ilkesi: kalite ölçülmeden en kötü kayıt hatası).
# Etüt (tek okuma) tepe ölçümü değil: merkezi taşır, bandı daraltmaz (BANT_LOG). Popülasyon R'si yalnız MD kayıtlarından
# (sezon tepesi; etüt anlık), en az KAYIT_MIN kayıtla. Fider: kayıp payı, düzeltme oranının sınırı.
KAYIT_BANT_LOG = (-0.10, 0.36)
KAYIT_MIN = 3
FIDER_KAYIP = 0.03
FIDER_ORAN_SINIR = (0.7, 1.5)
# Akşam gerilimi (madde 6) [Yorum]: çekiliş sayısı; tepe anında OG değişimi (sistem tepesinde bara biraz düşer; Kıb-Tek
# ölçümü BULAMADIM); 207 V sınırı (EN 50160, ADR-0016 m. 3).
CEKILIS_V = 40
OG_AKSAM = (-0.01, 0.0)
V_ALT = 207.0
# Tepe saati (KARAR 01:30) [Yorum; şehir 1–10'da]: ikinci aday ana tepeden en az IKINCI_ARALIK_SAAT uzakta ve zarfın
# IKINCI_ESIK'i kadar yüksekse yazılır. Ticari II abonesi olan trafoda öğlen modelinin arketipi "akşam tepeli" ise (ölçülü
# trafoların Nisan eğrilerinden, sablon.py) ticari II konut eğrisini alır (yurt gibi); yoksa büyük ticaret. Kıb-Tek tarife
# sınıfını bilir, yapı tipini bilmez; arketip bunun vekili (1–10'da yurtların 41/48'i akşam tepeli, çarşıların 0/41'i).
IKINCI_ESIK, IKINCI_ARALIK_SAAT = 0.95, 3
TEPE_SUTUNLARI = ['sehir', 'trafo_no', 'olculdu', 'tepe_kw', 'tepe_kw_p10', 'tepe_kw_p90', 'tepe_saati', 'tepe_ayi',
                  'pf_varsayim', 'tepe_kva', 'tepe_kva_p10', 'tepe_kva_p90', 'bos_kva', 'bos_kva_p10', 'bos_kva_p90',
                  'guven', 'kor_nokta', 'tepe_kaynagi', 'v_min_tepe_v', 'v_min_tepe_v_p10', 'v_min_tepe_v_p90',
                  'p_aksam_207', 'tepe_saati_2', 'tepe_donemi']


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
    if MODEL in ('b-y2', 'b-y2-esz'):
        out['konut']['yaz'] = KONUT_YAZ_EGIM
    return out, Tay


def tasarim_sapmasi():
    """Lefkoşa 2015–2025: yaz ve kış aylarında, her yıl ayın en uç gününün (günlük ortalama) o ayın 11 yıllık iklim
    ortalamasından farkı; yıllar arası TASARIM_NICEL. -> ({ay: ΔT}, bilgi)."""
    with open(UZUN_SERI, encoding='utf-8', newline='') as fh:
        satir = list(csv.reader(fh))
    bas = next(i for i, r in enumerate(satir) if r and r[0] == 'time')
    gun = {}
    for r in satir[bas + 1:]:
        if r and r[1]:
            gun.setdefault(r[0][:10], []).append(float(r[1]))
    gt = {dt.date.fromisoformat(d): statistics.fmean(v) for d, v in gun.items() if len(v) == 24}
    out, bilgi = {}, {}
    for m in YAZ + KIS:
        iklim = statistics.fmean(v for d, v in gt.items() if d.month == m)
        uc = []
        for y in sorted({d.year for d in gt}):
            x = [v for d, v in gt.items() if d.year == y and d.month == m]
            uc.append(max(x) - iklim if m in YAZ else iklim - min(x))
        out[m] = float(np.quantile(uc, TASARIM_NICEL))
        bilgi[m] = dict(iklim_c=round(iklim, 1), yillik_uc_ortanca=round(statistics.median(uc), 1), tasarim=round(out[m], 1),
                        yil=len(uc))
    return out, bilgi


def ay_kosullari(hava, yil, kip, tasarim=None):
    """Ay başına sıcaklık sapması ΔT (°C, ≥ 0: yazın en sıcak günün, kışın en soğuk günün ay ortalamasından farkı) ve
    ayın saatlik ortalama ışınımı (288 adım). kip 'tasarim': ΔT = 10 yılda bir uç günün iklim ortalamasından farkı."""
    out = {}
    for m in (NISAN,) + YAZ + KIS:
        gunler = [d for d in hava if d.year == yil and d.month == m]
        if not gunler:
            continue
        gt = [statistics.fmean(hava[d][0]) for d in gunler]
        ort = statistics.fmean(gt)
        dT = 0.0 if m == NISAN else (max(gt) - ort if m in YAZ else ort - min(gt))
        if kip == 'tasarim' and m != NISAN:
            dT = tasarim[m]
        ghi = np.array([statistics.fmean(hava[d][1][h] for d in gunler) for h in range(24)])
        out[m] = dict(dT=dT, ghi=np.repeat(ghi, ADIM // 24), gun=len(gunler))
    return out


# ---------- önsel ----------

def sinif_kw(tr):
    """Trafo × sınıf yıllık ortalama kW. Fatura varsa sınıf enerjileri brüt faturaya ölçeklenir (sablon.fatura_mwh:
    fatura net ise panel üretimi geri eklenir; net faturayla akşam tepesi az çıkar, güvensiz yön)."""
    import sablon
    E = np.column_stack([tr[a].fillna(0).to_numpy(float) * MWH[a] for a in ABONE])      # MWh/yıl
    if sablon.fatura_var(tr):
        top = E.sum(1)
        E = E * np.divide(sablon.fatura_mwh(tr), top, out=np.ones_like(top), where=top > 0)[:, None]
    return E / 8.76


def net_egri(kw, eac, ay, g, dT, egim, carp, panel_kw, ghi, mevsim, sinif=None):
    """Bir trafonun ayın tipik günü net yükü (288, kW)."""
    out = np.zeros(ADIM)
    for j, a in enumerate(ABONE):
        if kw[j] <= 0:
            continue
        c = (sinif or SINIF)[a]
        f = 1.0 if mevsim is None else max(SICAKLIK_TABAN, 1 + egim[c][mevsim] * carp * dT)
        out += kw[j] * eac[(c, ay, g)] * f
    return out - panel_kw * ghi / 1000 * PR_GUNES


def tarama(kw, panel_kw, eac, kosul, egim, carp=1.0, sinif=None, yaz_carp=1.0):
    """Yıl taraması: Nisan + yaz ayları + kış ayları, iş günü ve tatil; en büyük net değer. yaz_carp: yaz aylarının eğrisine
    eşzamanlılık oranı (B-Y2, yaz_orani). -> (kW, adım, ay, zarf)."""
    en = (-math.inf, 0, 0)
    zarf = np.full(ADIM, -np.inf)
    for m, k in kosul.items():
        mev = None if m == NISAN else ('yaz' if m in YAZ else 'kis')
        for g in ('is', 'tatil'):
            e = net_egri(kw, eac, m, g, k['dT'], egim, carp, panel_kw, k['ghi'], mev, sinif)
            if mev == 'yaz':
                e = e * yaz_carp
            zarf = np.maximum(zarf, e)
            i = int(e.argmax())
            if e[i] > en[0]:
                en = (float(e[i]), i, m)
    return en + (zarf,)


def ikinci_aday(zarf, ana):
    """Ana tepeden en az IKINCI_ARALIK_SAAT uzakta zarfın en büyüğü; ana tepenin IKINCI_ESIK'i kadar yüksekse adımı, yoksa
    None. Konutun Temmuz gününde öğleden sonra (16–17) ve gece (23–00) tepeleri neredeyse eşit; hangisinin yılın tepesi
    olacağı haftanın havasına, panele ve gürültüye bağlı (tek saat yarı yarıya tutar)."""
    uzak = np.abs((np.arange(ADIM) - ana + ADIM // 2) % ADIM - ADIM // 2) >= IKINCI_ARALIK_SAAT * 12
    if not uzak.any():
        return None
    j = int(np.where(uzak, zarf, -np.inf).argmax())
    return j if zarf[j] >= IKINCI_ESIK * zarf[ana] else None


def donem(adim):
    s = adim * 5 // 60
    return 'gece' if s >= 20 or s < 4 else 'sabah' if s < 10 else 'ogle' if s < 14 else 'ogleden_sonra'


def nisan_tepesi(kw, panel_kw, eac, kosul, egim, sinif=None):
    k = kosul[NISAN]
    return max(float(net_egri(kw, eac, NISAN, g, 0.0, egim, 1.0, panel_kw, k['ghi'], None, sinif).max())
               for g in ('is', 'tatil'))


def yaz_egrileri(kw, panel_kw, eac, kosul, egim, sinif=None):
    """Yaz aylarının tipik günleri (iş günü, tatil): {(ay, gün türü): 288}."""
    return {(m, g): net_egri(kw, eac, m, g, kosul[m]['dT'], egim, 1.0, panel_kw, kosul[m]['ghi'], 'yaz', sinif)
            for m in YAZ for g in ('is', 'tatil')}


def zaman_coz(z):
    d = dt.datetime.fromisoformat(z)
    return d.date(), (d.hour * 60 + d.minute) // 5


def gun_egrisi(kw, panel_kw, eac, hava, gun, egim, sinif=None):
    """Belli bir günün önsel net eğrisi: ayın tipik günü × o günün sıcaklık sapması, o günün ışınımı."""
    m = gun.month
    ort = statistics.fmean(statistics.fmean(hava[d][0]) for d in hava if d.year == gun.year and d.month == m)
    dT = statistics.fmean(hava[gun][0]) - ort
    mev = 'yaz' if m in YAZ else ('kis' if m in KIS else None)
    g = 'tatil' if gun.weekday() >= 5 else 'is'
    ghi = np.repeat(np.array(hava[gun][1]), ADIM // 24)
    return net_egri(kw, eac, m, g, (dT if mev == 'yaz' else -dT) if mev else 0.0, egim, 1.0, panel_kw, ghi, mev, sinif)


def kibtek_oku(klasor):
    """kibtek_tepe.csv ve kibtek_fider.csv (sözleşme §9 adayı); yoksa boş. tepe_kw boşsa tepe_a'dan (en yüklü faz akımı):
    kW ≈ 3 × 230 V × A × PF ÷ 1000 (dengesizlikte fazla gösterir, güvenli yön) [Yorum]."""
    tepe = pd.read_csv(klasor / 'kibtek_tepe.csv', encoding='utf-8', dtype={'zaman': str}) \
        if (klasor / 'kibtek_tepe.csv').exists() else pd.DataFrame(columns=['trafo_no', 'kaynak', 'tepe_kw', 'zaman'])
    if 'tepe_a' in tepe:
        bos = tepe['tepe_kw'].isna()
        tepe.loc[bos, 'tepe_kw'] = 3 * 230 * tepe.loc[bos, 'tepe_a'] * PF / 1000
    tepe = tepe[tepe['tepe_kw'].notna() & (tepe['tepe_kw'] > 0)]
    fider = pd.read_csv(klasor / 'kibtek_fider.csv', encoding='utf-8', dtype={'zaman': str}) \
        if (klasor / 'kibtek_fider.csv').exists() else None
    return tepe, fider


# ---------- akşam gerilimi ----------

def en_dusuk_gerilim(ag, V):
    """Evlerin en düşük faz gerilimi (üç fazlı evde üç faz da)."""
    lo = math.inf
    for fi, f in enumerate(ag['feeders']):
        for k, h in enumerate(f['houses']):
            v = V[fi][k]
            for p in (range(3) if h['ph'] == 3 else (h['ph'],)):
                lo = min(lo, abs(v[p] - v[3]))
    return lo


def tepe_payi(kw, eac, egim, kosul, ay, adim, abone_sayisi, sinif=None):
    """Tepe anında abone başına yük ağırlığı (sınıf sütunu → kW / abone) ve o andaki güneş çarpanı (kW / kWp).
    Gün türü o adımda toplamı büyük olan."""
    mev = None if ay == NISAN else ('yaz' if ay in YAZ else 'kis')
    en = None
    for g in ('is', 'tatil'):
        pay = {}
        for j, a in enumerate(ABONE):
            if kw[j] <= 0 or abone_sayisi[j] <= 0:
                continue
            c = (sinif or SINIF)[a]
            f = 1.0 if mev is None else max(SICAKLIK_TABAN, 1 + egim[c][mev] * kosul[ay]['dT'])
            pay[a] = kw[j] * float(eac[(c, ay, g)][adim]) * f / abone_sayisi[j]
        top = sum(pay[a] * abone_sayisi[ABONE.index(a)] for a in pay)
        if en is None or top > en[0]:
            en = (top, pay)
    return en[1], float(kosul[ay]['ghi'][adim]) / 1000 * PR_GUNES


def aksam_gerilimi(trs, pay, gunes, tepe, p10, p90, rng, srng):
    """CEKILIS_V çekilişte tepe anının en düşük ev gerilimi (V). trs: trafolar.csv satırı (sözlük)."""
    _argv, sys.argv = sys.argv, sys.argv[:1]
    import kac_ev_olasilik as kv            # panel tarafının ağ kurucusu (BUILD 2'nin dosyası; yalnız okunur)
    import trafo_bos_kapasite as tb
    sys.argv = _argv
    s_lo = math.log(max(tepe, 1e-6) / max(p10, 1e-6)) / 1.2816
    s_hi = math.log(max(p90, 1e-6) / max(tepe, 1e-6)) / 1.2816
    out = []
    for _ in range(CEKILIS_V):
        ag, evler = kv.ag_kur(trs, rng)
        s = math.exp(srng.gauss(kv.SAPMA_MU, kv.SAPMA_SIGMA))
        for f in ag['feeders']:
            f['zs'], f['zn'] = f['zs'] * s, f['zn'] * s
        if not evler:
            out.append(ag['v0'])
            continue
        z = rng.gauss(0, 1)
        net_top = tepe * math.exp(z * (s_hi if z > 0 else s_lo))
        brut_top = net_top + sum(h['pv'] for h in evler) * gunes          # brüt = net + o anki üretim
        w = [pay.get(h['sinif'], 0.0) * rng.lognormvariate(-kv.BIREY_SIGMA ** 2 / 2, kv.BIREY_SIGMA) for h in evler]
        sw = sum(w) or 1.0
        net = {}
        for h, x in zip(evler, w):
            p = brut_top * x / sw
            net[h['id']] = ((p - h['pv'] * gunes) * 1000, p * kv.Q_ORAN * 1000)
        V, _ = tb.solve(ag, net, 1 + rng.uniform(*OG_AKSAM), None, iters=6)
        out.append(en_dusuk_gerilim(ag, V))
    return out


# ---------- şehir ----------

def arketip_aksam(klasor):
    """{trafo_no: True/False}: öğlen modelinin arketipi akşam tepeli mi (tahmin.csv + arketipler.csv, sablon.py yazar).
    Dosya yoksa boş (ticari II büyük ticaret eğrisini alır)."""
    if not ((klasor / 'tahmin.csv').exists() and (klasor / 'arketipler.csv').exists()):
        print(f'UYARI: {klasor.name}: tahmin.csv / arketipler.csv yok (önce sablon.py); ticari II büyük ticaret eğrisiyle')
        return {}
    ad = pd.read_csv(klasor / 'arketipler.csv', encoding='utf-8')[['arketip', 'arketip_adi']].drop_duplicates()
    ad = dict(zip(ad['arketip'], ad['arketip_adi']))
    t = pd.read_csv(klasor / 'tahmin.csv', encoding='utf-8')
    return {r['trafo_no']: str(ad.get(r['arketip'], '')).startswith('aksam_tepeli') for _, r in t.iterrows()}


def eszamanlilik(n, c):
    """Eşzamanlılık çarpanı (ADR-0018 m. 5): Velander biçimi 1 + c ÷ √n (n = konut abonesi eşdeğeri)."""
    return 1 + c / np.sqrt(np.maximum(np.asarray(n, float), 1.0))


def esz_c(tur):
    """B-Y2: 20 evin c'si (ev başına) → n'nin ölçeğine (enerji cinsinden konut eşdeğeri)."""
    return ESZ_C_EV[tur] * math.sqrt(ESZ_EV_MWH / KONUT_MWH)


def yaz_orani(carp, c_diger):
    """B-Y2: Nisan'a (diğer günlerin c'siyle) bağlanmış R'yi yaz tepesine taşır: f_sıcak ÷ f_diğer (carp: c → trafonun
    eşzamanlılık çarpanı); sıcak c'si diğer c'yle aynı oranda (bant uçlarında da). Yalnız `--model b-y2-esz`; yoksa 1."""
    if MODEL != 'b-y2-esz':
        return 1.0
    return carp(c_diger * ESZ_C_EV['sicak'] / ESZ_C_EV['diger']) / carp(c_diger)


def sabit_c(R, carp, c):
    """B-Y2: c sabit (veriden); R0 ölçülülerin Nisan R'lerinden: ln R0 = ort(ln R − ln f(c)); carp: {trafo: c → çarpan}.
    -> (c, R0 fonksiyonu)."""
    lr = np.log(np.array(list(R.values())))
    return c, lambda c_: float(np.exp((lr - np.log([carp[t](c_) for t in R])).mean()))


def velander_uydur(R, n):
    """Ölçülülerin Nisan R'lerinden c (ızgara) ve her c için R0: ln R = ln R0 + ln(1 + c ÷ √n), en küçük kareler.
    -> (ĉ, R0(c) fonksiyonu)."""
    lr = np.log(np.array(list(R.values())))
    g = lambda c: np.log(eszamanlilik(np.array(list(n.values())), c))       # noqa: E731
    r0 = lambda c: float(np.exp((lr - g(c)).mean()))                       # noqa: E731
    izgara = np.arange(0.0, VELANDER_C_UST + 1e-9, 0.05)
    c = float(min(izgara, key=lambda c: float(((lr - g(c) - np.log(r0(c))) ** 2).sum())))
    return c, r0


def sehir_calistir(klasor, eac, hava, egim, kip='yil', tasarim=None, fider_duzelt=False, kibtek=True):
    from sablon import ogretici_sec          # ölçülü küme sablon.py ile aynı (ürünün tabakalı seçimi)
    tr = pd.read_csv(klasor / 'trafolar.csv', encoding='utf-8')
    sehir = int(tr['sehir'].iloc[0])
    with open(klasor / 'ayar.json', encoding='utf-8') as fh:
        yil = int(json.load(fh)['hava_yili'])     # yalnız yıl; üreticinin gizli ayarları okunmaz
    kosul = ay_kosullari(hava, yil, kip, tasarim)
    kosul_yil = ay_kosullari(hava, yil, 'yil')    # kayıtlar o yılın havasında alındı (tasarım kipinde de)
    eksik = [m for m in (NISAN,) + YAZ + KIS if m not in kosul]
    if eksik:
        raise SystemExit(f'sehir-{sehir:03d}: {yil} hava verisi eksik (aylar {eksik}); data/raw/open-meteo-lefkosa')
    secilen = ogretici_sec(tr, OLCULU_ANA, f'sec-{sehir}')
    ids = [tr['trafo_no'].iloc[i] for i in secilen]
    yuk = pd.read_csv(klasor / 'yuk_5dk.csv', encoding='utf-8', usecols=['trafo_no', 'net_kw'])
    y = yuk[yuk['trafo_no'].isin(ids)].groupby('trafo_no')['net_kw'].max()          # model yalnız bunu görür

    KW = sinif_kw(tr)
    aksam = arketip_aksam(klasor)
    snf = [dict(SINIF, abone_ticari2='konut') if aksam.get(t) and tr['abone_ticari2'].iloc[i] > 0 else None
           for i, t in enumerate(tr['trafo_no'])]
    panel = tr['panel_kw'].fillna(0).to_numpy(float)
    n_esd = KW.sum(1) * 8.76 / KONUT_MWH            # enerji, konut abonesi eşdeğeri (Velander'in N·a'sı)
    # B-Y2: ev çeşitliliği (20 evin verisi) yalnız konut payına: tek sayaçlı otelde, çarşıda, sanayide ev çeşitliliği yok;
    # bütün enerjiye uygulanınca 31–40'ta büyük ticari / otel / sanayi tepesi %24–28 az çıktı (güvensiz yön). Pay = konut
    # enerji payı [Yorum: tepe anındaki pay yerine].
    pay_k = np.divide(KW[:, 0], KW.sum(1), out=np.zeros(len(KW)), where=KW.sum(1) > 0)
    n_k = KW[:, 0] * 8.76 / KONUT_MWH

    def carpan(i, c):
        if MODEL != 'b-y2-esz':
            return float(eszamanlilik(n_esd[i], c))
        return float(pay_k[i] * eszamanlilik(n_k[i], c) + 1 - pay_k[i])
    R = {}
    for i in secilen:
        p = nisan_tepesi(KW[i], panel[i], eac, kosul, egim, snf[i])
        R[tr['trafo_no'].iloc[i]] = float(y[tr['trafo_no'].iloc[i]]) / max(p, 0.1)
    logR = np.log(list(R.values()))
    R_ort = float(np.exp(logR.mean()))
    n_olc = {t: n_esd[secilen[j]] for j, t in enumerate(R)}
    if MODEL == 'b-y2-esz':
        c_hat, R0 = sabit_c(R, {t: (lambda c, i=secilen[j]: carpan(i, c)) for j, t in enumerate(R)}, esz_c('diger'))
        c_bant = tuple(c_hat * k for k in ESZ_C_ARALIK)
    else:
        c_hat, R0 = velander_uydur(R, n_olc)
        c_bant = (0.0, max(2 * c_hat, VELANDER_C_BANT))
    # bir-dışarıda (bilgi): ölçülü trafonun Nisan tepesi öbürlerinin R'siyle
    loo = [float(np.log(R[t]) - (logR.sum() - np.log(R[t])) / (len(logR) - 1)) for t in R]

    # Madde 5: Kıb-Tek tepe kayıtları (yaz). Kayıt Nisan ölçümünden önce gelir.
    kayit, fider = kibtek_oku(klasor) if kibtek else (pd.DataFrame(columns=['trafo_no']), None)
    sira = {t: i for i, t in enumerate(tr['trafo_no'])}
    RK, kayit_turu = {}, {}
    for _, k in kayit.iterrows():
        i = sira[k['trafo_no']]
        if isinstance(k['zaman'], str) and k['zaman']:
            gun, s = zaman_coz(k['zaman'])
            p = float(gun_egrisi(KW[i], panel[i], eac, hava, gun, egim, snf[i])[s])
        else:                                   # MD: sezonun en yükseği, zamanı yok
            p = max(float(e.max()) for e in yaz_egrileri(KW[i], panel[i], eac, kosul_yil, egim, snf[i]).values())
        RK[k['trafo_no']] = float(k['tepe_kw']) / max(p, 0.1)
        kayit_turu[k['trafo_no']] = 'kayit_md' if k['kaynak'] == 'md_kaydi' else 'kayit_etut'
    # Popülasyon R'si tabakalı ölçülülerden kalır: Kıb-Tek kayıtları temsilî değil (MD göstergesi çoğunlukla büyük yer
    # tipi trafoda, eski kayıt az gösterir); kayıtlardan popülasyona aktarım 1–10'da tahmini −%2 / −%4 (güvensiz yön)
    # kaydırdı [Hesap; günlük]. Kayıt kendi trafosunu düzeltir; popülasyonu sürümlü yeniden-fit (tüzük m. 4) düzeltir:
    # öneri `tepe_ozet.json`'a.
    R_pop = R0(c_hat)
    kayit_oneri = None
    RM = {t: v for t, v in RK.items() if kayit_turu[t] == 'kayit_md'}
    if len(RM) >= KAYIT_MIN:
        lk = np.log(list(RM.values()))
        dis = [float(np.log(RM[t]) - np.median(np.delete(lk, j))) for j, t in enumerate(RM)]
        montaj = dict(zip(tr['trafo_no'], tr['montaj']))
        kayit_oneri = dict(n_md=len(RM), R_md_ortanca=round(float(np.exp(np.median(lk))), 3), R_nisan=round(R_ort, 3),
                           md_montaj={m_: sum(montaj[t] == m_ for t in RM) for m_ in sorted(set(montaj.values()))},
                           bant_log_P10=round(float(np.quantile(dis, 0.1)), 3),
                           bant_log_P90=round(float(np.quantile(dis, 0.9)), 3),
                           not_='yeniden-fit önerisi (tüzük m. 4: sürümle, kendiliğinden değil); bugün popülasyon Nisan R, bant BANT_LOG')

    # Her trafonun R'si ve kaynağı: Kıb-Tek kaydı > Nisan ölçümü > popülasyon
    r_tr, kaynak = {}, {}
    for i, t in enumerate(tr['trafo_no']):
        if t in RK:
            r_tr[t], kaynak[t] = RK[t], kayit_turu[t]
        elif t in R:
            r_tr[t], kaynak[t] = R[t], 'olcum_nisan'
        else:
            r_tr[t], kaynak[t] = R0(c_hat) * carpan(i, c_hat), 'model'

    # Fider mutabakatı (aşağıdan yukarı ↔ OG kaydı); isteğe bağlı yukarıdan aşağı düzeltme
    fider_rapor, fider_carpan = [], {}
    if fider is not None:
        for _, f in fider.iterrows():
            uye = [u for u in str(f['trafolar']).split(';') if u in sira]
            if isinstance(f['zaman'], str) and f['zaman']:
                gun, s = zaman_coz(f['zaman'])
                parca = {u: r_tr[u] * float(gun_egrisi(KW[sira[u]], panel[sira[u]], eac, hava, gun, egim, snf[sira[u]])[s])
                         for u in uye}
                tah = sum(parca.values())
            else:
                eg = {u: yaz_egrileri(KW[sira[u]], panel[sira[u]], eac, kosul_yil, egim, snf[sira[u]]) for u in uye}
                anah = max(eg[uye[0]], key=lambda a: sum(r_tr[u] * eg[u][a] for u in uye).max())
                top = sum(r_tr[u] * eg[u][anah] for u in uye)
                s = int(top.argmax())
                parca = {u: r_tr[u] * float(eg[u][anah][s]) for u in uye}
                tah = float(top[s])
            gercek = float(f['tepe_kw']) / (1 + FIDER_KAYIP)
            olcusuz = sum(v for u, v in parca.items() if kaynak[u] == 'model')
            oran = None
            if olcusuz > 0:
                oran = min(max((gercek - (tah - olcusuz)) / olcusuz, FIDER_ORAN_SINIR[0]), FIDER_ORAN_SINIR[1])
                if fider_duzelt:
                    for u in uye:
                        if kaynak[u] == 'model':
                            fider_carpan[u] = oran
            fider_rapor.append(dict(fider=f['fider_no'], trafo=len(uye), kayit_kw=round(float(f['tepe_kw']), 1),
                                    tahmin_kw=round(tah * (1 + FIDER_KAYIP), 1),
                                    kayit_tahmin_orani=round(float(f['tepe_kw']) / max(tah * (1 + FIDER_KAYIP), 0.1), 3),
                                    olcusuz_carpan=None if oran is None else round(oran, 3)))

    satirlar = []
    lo_k, hi_k = BANT_LOG
    for i, t in enumerate(tr['trafo_no']):
        # B-Y2: Nisan seviyesindeki R (model ve Nisan ölçümü) yaz aylarında sıcak akşam eşzamanlılığına taşınır; Kıb-Tek
        # kaydı zaten yaz tepesi.
        yo = yaz_orani(lambda c: carpan(i, c), c_hat) if kaynak[t] in ('model', 'olcum_nisan') else 1.0
        ham, adim, ay, zarf = tarama(KW[i], panel[i], eac, kosul, egim, 1.0, snf[i], yo)
        ham_lo = tarama(KW[i], panel[i], eac, kosul, egim, EGIM_ARALIK[0], snf[i], yo)[0]
        ham_hi = tarama(KW[i], panel[i], eac, kosul, egim, EGIM_ARALIK[1], snf[i], yo)[0]
        adim2 = ikinci_aday(zarf, adim)
        tepe = max(r_tr[t] * fider_carpan.get(t, 1.0) * ham, 0.0)
        s_lo = math.log(max(ham_lo, 1e-6) / max(ham, 1e-6))
        s_hi = math.log(max(ham_hi, 1e-6) / max(ham, 1e-6))
        # ölçülünün Nisan'ı biliniyor (yazı yalnız eğimle belirsiz); kaydı olanın kaydın hatası; ölçülmeyende eşzamanlılık
        # belirsizliği: c bant uçlarında R'nin oranı
        a, b = {'model': (lo_k, hi_k), 'olcum_nisan': (0.0, 0.0), 'kayit_etut': (lo_k, hi_k)}.get(kaynak[t], KAYIT_BANT_LOG)
        e_lo = e_hi = 0.0
        if kaynak[t] == 'model':
            oy = (lambda c: yaz_orani(lambda c_: carpan(i, c_), c) / yo) if ay in YAZ else (lambda c: 1.0)  # noqa: E731
            rc = [R0(c) * carpan(i, c) * oy(c) / (R0(c_hat) * carpan(i, c_hat)) for c in c_bant]
            e_lo, e_hi = math.log(min(rc + [1.0])), math.log(max(rc + [1.0]))
        p10 = tepe * math.exp(-math.sqrt(a ** 2 + min(s_lo, 0.0) ** 2 + e_lo ** 2))
        p90 = tepe * math.exp(math.sqrt(b ** 2 + max(s_hi, 0.0) ** 2 + e_hi ** 2))
        kva = float(tr['kva'].iloc[i])
        abone_sayisi = tr[ABONE].iloc[i].fillna(0).to_numpy(float)
        pay, gunes = tepe_payi(KW[i], eac, egim, kosul, ay, adim, abone_sayisi, snf[i])
        vs = sorted(aksam_gerilimi(tr.iloc[i].to_dict(), pay, gunes, tepe, p10, p90,
                                   random.Random(f'aksam-{sehir}-{t}'), random.Random(f'aksam-sapma-{sehir}-{t}')))
        satirlar.append(dict(
            sehir=sehir, trafo_no=t, olculdu=int(kaynak[t] != 'model'), tepe_kw=round(tepe, 2), tepe_kw_p10=round(p10, 2),
            tepe_kw_p90=round(p90, 2), tepe_saati=f'{adim * 5 // 60:02d}:{adim * 5 % 60:02d}', tepe_ayi=ay,
            pf_varsayim=PF, tepe_kva=round(tepe / PF, 2), tepe_kva_p10=round(p10 / PF, 2), tepe_kva_p90=round(p90 / PF, 2),
            bos_kva=round(kva - tepe / PF, 2), bos_kva_p10=round(kva - p90 / PF, 2), bos_kva_p90=round(kva - p10 / PF, 2),
            guven='on', kor_nokta=KOR_NOKTA, tepe_kaynagi=kaynak[t] + ('+fider' if t in fider_carpan else ''),
            v_min_tepe_v=round(float(np.median(vs)), 1), v_min_tepe_v_p10=round(float(np.quantile(vs, 0.1)), 1),
            v_min_tepe_v_p90=round(float(np.quantile(vs, 0.9)), 1),
            p_aksam_207=round(sum(v < V_ALT for v in vs) / len(vs), 3),
            tepe_saati_2='' if adim2 is None else f'{adim2 * 5 // 60:02d}:{adim2 * 5 % 60:02d}', tepe_donemi=donem(adim)))
    with open(klasor / 'tepe.csv', 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=TEPE_SUTUNLARI, lineterminator='\n')
        w.writeheader()
        w.writerows(satirlar)
    ozet = dict(sehir=sehir, hava_yili=yil, kip=kip, olculu=ids, R={t: round(v, 3) for t, v in R.items()},
                R_ortalama=round(R_ort, 3), R_bir_disarida_log_artik=[round(x, 3) for x in loo],
                model=MODEL, velander_c=round(c_hat, 2), velander_R0=round(R0(c_hat), 3),
                velander_c_bant=[round(c, 2) for c in c_bant], esz_c_ev=ESZ_C_EV if MODEL == 'b-y2-esz' else None,
                tasarim_dT=None if tasarim is None else {m: round(v, 1) for m, v in tasarim.items()},
                egim={c: {k: round(v, 4) for k, v in e.items()} for c, e in egim.items()},
                dT={m: round(k['dT'], 1) for m, k in kosul.items()}, bant_log=[lo_k, hi_k], egim_aralik=list(EGIM_ARALIK),
                pr_gunes=PR_GUNES, pf=PF, kor_nokta=KOR_NOKTA,
                ticari2_konut_egrisi=[t for i, t in enumerate(tr['trafo_no']) if snf[i] is not None],
                kibtek=dict(kayit=len(RK), md=sum(v == 'kayit_md' for v in kayit_turu.values()),
                            etut=sum(v == 'kayit_etut' for v in kayit_turu.values()),
                            R_kayit={t: round(v, 3) for t, v in RK.items()}, populasyon_R=round(R_pop, 3),
                            yeniden_fit_onerisi=kayit_oneri, fider=fider_rapor,
                            fider_duzeltme=fider_duzelt))
    with open(klasor / 'tepe_ozet.json', 'w', encoding='utf-8', newline='') as fh:
        json.dump(ozet, fh, ensure_ascii=False, indent=1)
    return satirlar, ozet


def main():
    ap = argparse.ArgumentParser(description='Yılın tepesi, ön sürüm (Faz 11, ADR-0018).')
    ap.add_argument('kok', type=Path)
    ap.add_argument('--aralik', default=None, help='ör. 1-10 (yoksa kökteki bütün sehir-* klasörleri)')
    ap.add_argument('--hava', choices=['yil', 'tasarim'], default='yil',
                    help="yil: şehrin hava yılı (sınav); tasarim: Lefkoşa 2015–2025'te 10 yılda bir uç gün (harita)")
    ap.add_argument('--fatura-net', action='store_true', help='fatura mahsuplaşmalı abonelerde net (sablon.py ile aynı)')
    ap.add_argument('--kibtek-yok', action='store_true', help='kibtek_tepe.csv / kibtek_fider.csv olsa da okuma (kıyas)')
    ap.add_argument('--fider-duzelt', action='store_true', help='ölçülmeyen trafoları OG fider kaydının oranına ölçekle')
    ap.add_argument('--model', choices=['b-y2', 'b-y2-esz', 'on'], default='b-y2',
                    help='b-y2: konut yaz eğimi 20 Kıbrıs evinden (Can); b-y2-esz: + ev çeşitliliği konut payına (deneme); '
                         'on: eski ön sürüm (kıyas)')
    a = ap.parse_args()
    global MODEL
    MODEL = a.model
    import sablon
    sablon.FATURA_NET = a.fatura_net
    if a.aralik:
        i, j = map(int, a.aralik.split('-'))
        klasorler = [a.kok / f'sehir-{s:03d}' for s in range(i, j + 1)]
    else:
        klasorler = sorted(a.kok.glob('sehir-*'))
    eac, hava = eac_hazirla(), hava_oku()
    egim, _ = egimler(eac, hava)
    tasarim = tasarim_sapmasi()[0] if a.hava == 'tasarim' else None
    for k in klasorler:
        s, o = sehir_calistir(k, eac, hava, egim, a.hava, tasarim, a.fider_duzelt, not a.kibtek_yok)
        kb = o['kibtek']
        print(f"{k.name}: {len(s)} trafo; R Nisan {o['R_ortalama']}, Velander c {o['velander_c']}; "
              f"Kıb-Tek kayıt {kb['kayit']} (md {kb['md']}, etüt {kb['etut']}), fider {len(kb['fider'])}; tepe ayı "
              f"{dict(sorted(pd.Series([r['tepe_ayi'] for r in s]).value_counts().items()))}")


if __name__ == '__main__':
    main()
