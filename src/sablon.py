#!/usr/bin/env python3
"""Şablon modeli (Faz 2): birkaç ölçülü trafodan öğrenip ölçülmeyen trafonun bahar öğleni en düşük
yükünü bant ve güvenle tahmin eder.

Yöntem: docs/method/modeling.md; gerekçe ADR-0001 (şekil + büyüklük, küçük ve yorumlanabilir model).
Okur: trafolar.csv (hepsi; Kıb-Tek'in bildiği; yillik_tuketim_mwh varsa büyüklük faturadan, ADR-0007), yuk_5dk.csv (YALNIZ ölçülü seçilen trafoların satırları
modele girer). cevap_anahtari.csv'yi okumaz: model ya da harita onu okursa sınav anlamsızlaşır.
Yazar (sözleşme §5): tahmin.csv, arketipler.csv, deney/tahmin_n<N>_t<T>.csv,
deney/tahmin_capraz_s<AAA>.csv; bilgi için sablon_ozet.json.

Adımlar (ROADMAP Faz 2):
  2a ozellikler()     Kıb-Tek'in bildiği sütunlardan özellik tablosu
  2b ogretici_sec()   tabakalı öğretici küme (ölçüm cihazı takılacak trafolar; özellik uzayında n tabaka)
  2c kumele()         iş günü eğrisi tepesine bölünür; Ward + siluet ile k, sonra k-means
  2d atama            çok sınıflı lojistik regresyon (abone karışımı, bölge, büyüklük)
  2e olcek_kur()      abone enerjisine oran: sınıf başına NNLS, önce ortak, sonra küme başına (ortağa çekilmiş)
  2f bant             bir-trafo-dışarıda artıklarından %80 bant (küçük örnek düzeltmeli)
  2g guven()          atama olasılığı + ölçülülere uzaklık + görülmemiş abone sınıfı payı

Çalıştırma:
  python3 src/sablon.py data/synthetic                 # her şehir: ana çalıştırma + deneyler + şehirler arası
  python3 src/sablon.py data/synthetic --sehir 7 --yalniz-ana
  python3 src/sablon.py data/synthetic --onem          # 2d: sütun grubu çıkarınca bir-dışarıda hata (günlük için)
  python3 src/sablon.py data/synthetic --faturasiz     # yillik_tuketim_mwh olsa da kullanma (sütunsuz kıyas)
"""
import argparse
import csv
import json
import math
import random
import time
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

KOK = Path(__file__).resolve().parent.parent
OLCULU_ANA = 12                         # 40'tan 10–15 [ROADMAP 2b]
DENEY_N = (5, 10, 20)                   # "kaç trafo ölçmeli" [ROADMAP 2b, 2h]
DENEY_TEKRAR = 5
OGLE = slice(132, 168)                  # 11:00–14:00 (sözleşme)
K_EN_COK = 6                            # 3–6 arketip [ADR-0001]
BANT = (0.10, 0.90)                     # %80 bant

ABONE = ['abone_konut', 'abone_ticari1', 'abone_ticari2', 'abone_turizm',
         'abone_sanayi1', 'abone_sanayi2', 'abone_su_motoru']
# Abone başına yıllık MWh: Kıb-Tek 2023 tarife sınıfı tüketimi ÷ abone [Hesap; sehir_uret.py SINIFLAR ile aynı
# kaynak]. Kıb-Tek bunu faturadan bilir; burada yalnız abone karışımını enerjiye çevirmek için.
MWH = {'abone_konut': 648494 / 175577, 'abone_ticari1': 210978 / 20950, 'abone_ticari2': 169496 / 494,
       'abone_turizm': 215147 / 171, 'abone_sanayi1': 22391 / 1227, 'abone_sanayi2': 95996 / 352,
       'abone_su_motoru': 51256 / 3250}
BOLGELER = ['kentsel', 'kirsal', 'turistik', 'sanayi']
FATURA_SUTUNU = 'yillik_tuketim_mwh'    # sözleşme 1.2, ADR-0007; gerçek veride (EDP) yok
FATURA_KULLAN = True                    # --faturasiz: sütun olsa da abone sayılarıyla çalış (günlükte kıyas)

# Güven eşikleri [Yorum; Faz 2 günlüğünde gerekçe]
GUVEN_YUKSEK_P, GUVEN_DUSUK_P = 0.70, 0.50
GUVEN_YUKSEK_UZAK, GUVEN_DUSUK_UZAK = 1.0, 2.0     # en yakın ölçülüye uzaklık ÷ ölçülülerin kendi arası ortanca
GUVEN_DUSUK_GORULMEMIS = 0.20                      # enerjinin bu kadarı hiç ölçülmemiş abone sınıfında
GUVEN_YUKSEK_HATA, GUVEN_DUSUK_HATA = 0.10, 0.25    # beklenen hata: atandığı kümelerin bir-dışarıda hatası


# ---------- 2a özellik tablosu ----------

def fatura_var(tr):
    return bool(FATURA_KULLAN and FATURA_SUTUNU in tr and tr[FATURA_SUTUNU].notna().all())


def abone_matrisi(tr):
    """Abone sayıları (trafo × 7 sınıf), modelin büyüklük girdisi. trafolar.csv'de yillik_tuketim_mwh varsa
    (ADR-0007) her satır, tarife ortalamasıyla hesaplanan enerjisi faturaya eşit olacak şekilde ölçeklenir:
    sınıf karışımı abone sayısından, büyüklük faturadan. Sütun yoksa, boşsa ya da --faturasiz: sayılar aynen."""
    A = tr[ABONE].to_numpy(float)
    if not FATURA_KULLAN or FATURA_SUTUNU not in tr:
        return A
    e = A @ np.array([MWH[c] for c in ABONE])
    f = pd.to_numeric(tr[FATURA_SUTUNU], errors='coerce').to_numpy(float)
    gecerli = np.isfinite(f) & (f > 0) & (e > 0)
    s = np.divide(f, e, out=np.ones(len(A)), where=gecerli)
    return A * s[:, None]


def ozellikler(tr):
    """trafolar.csv satırları (DataFrame) -> (tam özellik matrisi, sütun grupları).
    Gerçek yük asla girdi değil; yalnız Kıb-Tek'in bileceği sütunlar."""
    a = tr[ABONE].to_numpy(float)
    e = abone_matrisi(tr) * np.array([MWH[c] for c in ABONE])     # faturalıysa e_top = fatura
    e_top = e.sum(1, keepdims=True)
    pay = np.divide(e, e_top, out=np.zeros_like(e), where=e_top > 0)
    gruplar = {
        'abone_karisimi': pay,
        'buyukluk': np.column_stack([np.log1p(e_top[:, 0]), np.log1p(a.sum(1)), np.log(tr['kva'].to_numpy(float))]),
        'bolge': np.column_stack([(tr['bolge'] == b).to_numpy(float) for b in BOLGELER]),
        'panel': (tr['panel_kw'] / tr['kva']).to_numpy(float)[:, None],
        'hat': np.column_stack([tr['hat_boyu_max_m'].to_numpy(float) / 1000, tr['hat_sayisi'].to_numpy(float),
                                (tr['montaj'] == 'yer').to_numpy(float)]),
    }
    return gruplar


def birlestir(gruplar, adlar):
    return np.hstack([gruplar[g] for g in adlar])


ATAMA_GRUPLARI = ['abone_karisimi', 'buyukluk', 'bolge', 'panel', 'hat']


# ---------- 2b öğretici küme ----------

SECIM_GRUPLARI = ['abone_karisimi', 'buyukluk', 'bolge']


def ogretici_sec(tr, n, tohum):
    """n trafo seç: Kıb-Tek'in bildiği özelliklerle (abone karışımı, büyüklük, bölge) trafolar n tabakaya
    bölünür (k-means), her tabakadan bir rastgele trafo. Tip bilinmez (cevap anahtarında); tabaka onun vekili.
    Benzer yerlere değil boşluklara (validation.md 'temsil yanlılığı'). İlk sürümde tabaka = baskın tarife ×
    bölge × kVA idi; aynı tarifedeki (ticari II) çarşı ve yurt aynı tabakaya düşüyordu (Faz 2 günlüğü)."""
    if n >= len(tr):
        return list(range(len(tr)))
    rng = random.Random(tohum)
    X = birlestir(ozellikler(tr), SECIM_GRUPLARI)
    sap = X.std(0)
    sap[sap == 0] = 1
    Z = (X - X.mean(0)) / sap
    et = KMeans(n_clusters=n, n_init=10, random_state=rng.randrange(2 ** 31)).fit_predict(Z)
    return sorted(rng.choice([i for i in range(len(tr)) if et[i] == j]) for j in range(n))


# ---------- ölçüm: yalnız ölçülü trafodan ----------

def olcumleri_hazirla(yuk, trafo_nolari):
    """yuk_5dk.csv -> {trafo_no: dict(isgunu=288, tatil=288, ogle_min=kW)}. Hız için bir kez hesaplanır;
    modele yalnız seçilen (ölçülü) trafoların girdisi verilir (bkz. modeli_kur)."""
    out = {}
    for t, g in yuk.groupby('trafo_no', sort=False):
        k = g['tuketim_kw'].to_numpy().reshape(-1, 288)
        tur = g['gun_turu'].to_numpy()[::288]
        out[t] = dict(isgunu=k[tur == 'isgunu'].mean(0), tatil=k[tur == 'tatil'].mean(0),
                      ogle_min=float(k[:, OGLE].min()))
    return {t: out[t] for t in trafo_nolari}


def tepeye_bol(x):
    m = x.max()
    return x / m if m > 0 else x


def saatlik(x):
    return x.reshape(24, 12).mean(1)


# ---------- 2c kümeleme ----------

def kumele(egriler):
    """Satır = ölçülü trafonun tepeye bölünmüş iş günü eğrisi (24 saat). -> (etiketler, k, siluetler)."""
    n = len(egriler)
    k_ust = min(K_EN_COK, n - 1)
    k_alt = 3 if n >= 9 else 2
    if k_ust < 2:
        return np.zeros(n, int), 1, {}
    siluet = {}
    for k in range(min(k_alt, k_ust), k_ust + 1):
        et = AgglomerativeClustering(n_clusters=k, linkage='ward').fit_predict(egriler)
        siluet[k] = float(silhouette_score(egriler, et))
    k = max(siluet, key=lambda x: (round(siluet[x], 3), -x))
    ward = AgglomerativeClustering(n_clusters=k, linkage='ward').fit_predict(egriler)
    merkez = np.array([egriler[ward == j].mean(0) for j in range(k)])
    et = KMeans(n_clusters=k, init=merkez, n_init=1, random_state=0).fit_predict(egriler)
    # boş küme kalırsa Ward etiketine dön
    if len(set(et)) < k:
        et = ward
    return et, k, siluet


def arketip_adi(egri288):
    """Tepeye bölünmüş iş günü eğrisinden okunur ad [Yorum]."""
    if egri288.min() / egri288.max() > 0.55:
        return 'duz'
    s = int(egri288.argmax()) * 5 // 60
    if 17 <= s <= 23:
        return 'aksam_tepeli'
    if 9 <= s <= 16:
        return 'gunduz_tepeli'
    return 'sabah_tepeli' if 5 <= s <= 8 else 'gece_tepeli'


# ---------- 2e ölçek ----------

E_KW = np.array([MWH[c] for c in ABONE]) / 8.76     # abone başına yıllık ortalama kW (MWh/yıl ÷ 8,76)
OLCEK_LAMBDA = 1.0                                  # ortak katsayıları tek orana çeken ağırlık (Faz 2 günlüğü)
KUME_LAMBDA = 1.0                                   # küme katsayılarını ortak katsayıya çeken ağırlık


def olcek_kur(A, y, onsel=None, lam=None):
    """Abone başına kW katsayıları (β = γ × E_KW). γ_sınıf = o sınıfın öğlen en düşük ÷ yıllık ortalama oranı.
    Göreli hata en küçüklenir (küçük trafo büyük kadar önemli); γ'lar `onsel`e çekilir (verilmezse tek ortak
    orana γ0 = Σy ÷ ΣE), böylece ölçülü kümede olmayan sınıf sıfır değil önseli alır. NNLS, γ ≥ 0."""
    E = A * E_KW
    lam = OLCEK_LAMBDA if lam is None else lam
    if onsel is None:
        onsel = np.full(len(ABONE), float(y.sum() / max(E.sum(), 1e-9)))
    w = 1 / np.maximum(y, 1.0)
    M = np.vstack([E * w[:, None], math.sqrt(lam) * np.eye(len(ABONE))])
    b = np.concatenate([y * w, math.sqrt(lam) * onsel])
    g, _ = nnls(M, b)
    return g * E_KW


# ---------- model: 2c + 2d + 2e ----------

def modeli_kur(X_tam, A, olcum, secilen, trafo_no):
    """Ölçülü trafolarla modeli kurar. X_tam, A: bütün trafoların özellik ve abone matrisi (Kıb-Tek'in bildiği);
    olcum: YALNIZ seçilenlerin ölçümü. -> model sözlüğü."""
    ids = [trafo_no[i] for i in secilen]
    egri = np.array([saatlik(tepeye_bol(olcum[t]['isgunu'])) for t in ids])
    et, k, siluet = kumele(egri)

    # 2d atama: standartlaştırılmış özellik -> arketip
    X = X_tam[secilen]
    ort, sap = X.mean(0), X.std(0)
    sap[sap == 0] = 1
    Z = (X - ort) / sap
    if k > 1:
        lr = LogisticRegression(C=1.0, max_iter=2000).fit(Z, et)
    else:
        lr = None

    # 2e ölçek: önce bütün ölçülülerle ortak katsayı, sonra her küme kendi katsayısı (ortak olana çekilerek).
    # Aynı tarifede farklı şekil (ticari II: çarşı dükkânı öğlen tepeli, yurt akşam tepeli) böyle ayrılır.
    y = np.array([olcum[t]['ogle_min'] for t in ids])
    ortak = olcek_kur(A[secilen], y)
    beta = np.array([olcek_kur(A[secilen][et == j], y[et == j], onsel=ortak / E_KW, lam=KUME_LAMBDA)
                     for j in range(k)])

    # 2g için: ölçülülerin kendi arasındaki en yakın komşu uzaklığı (ortanca)
    if len(Z) > 1:
        d = np.sqrt(((Z[:, None, :] - Z[None, :, :]) ** 2).sum(-1))
        np.fill_diagonal(d, np.inf)
        ref = float(np.median(d.min(1)))
    else:
        ref = 1.0
    gorulmemis = A[secilen].sum(0) == 0          # hiç ölçülmemiş abone sınıfı

    ad = [arketip_adi(np.mean([tepeye_bol(olcum[t]['isgunu']) for t, e in zip(ids, et) if e == j], 0))
          for j in range(k)]
    sayac = {}
    for j, a in enumerate(ad):                   # aynı ad iki kümede: _2, _3
        sayac[a] = sayac.get(a, 0) + 1
        if sayac[a] > 1:
            ad[j] = f'{a}_{sayac[a]}'
    return dict(secilen=list(secilen), ids=ids, etiket=et, k=k, siluet=siluet, lr=lr, ort=ort, sap=sap, Z=Z,
                beta=beta, ortak=ortak, ref=max(ref, 1e-6), gorulmemis=gorulmemis, ad=ad, olcum=olcum)


def tahmin_et(m, X_tam, A, satirlar):
    """Model ile istenen satırlar için (olasılıklar, orta tahmin, uzaklık oranı, görülmemiş pay)."""
    Z = (X_tam[satirlar] - m['ort']) / m['sap']
    if m['lr'] is not None:
        p = np.zeros((len(satirlar), m['k']))
        p[:, m['lr'].classes_] = m['lr'].predict_proba(Z)
    else:
        p = np.ones((len(satirlar), 1))
    orta = ((A[satirlar] @ m['beta'].T) * p).sum(1)          # Σ_k olasılık_k × küme k'nın ölçeği
    d = np.sqrt(((Z[:, None, :] - m['Z'][None, :, :]) ** 2).sum(-1)).min(1) / m['ref']
    e = A[satirlar] * np.array([MWH[c] for c in ABONE])
    e_top = e.sum(1)
    gor = np.divide(e[:, m['gorulmemis']].sum(1), e_top, out=np.zeros(len(satirlar)), where=e_top > 0)
    return p, orta, d, gor


# ---------- 2f bant: bir-trafo-dışarıda ----------

def bir_disarida(X_tam, A, olcum, secilen, trafo_no):
    """Her ölçülü trafo sırayla dışarı: kalanlarla model kurulur (kümeleme dahil), dışarıdaki tahmin edilir.
    -> (tahminler, log artıklar)."""
    tah = []
    for i in secilen:
        kalan = [j for j in secilen if j != i]
        m = modeli_kur(X_tam, A, {trafo_no[j]: olcum[trafo_no[j]] for j in kalan}, kalan, trafo_no)
        tah.append(float(tahmin_et(m, X_tam, A, [i])[1][0]))
    tah = np.array(tah)
    y = np.array([olcum[trafo_no[i]]['ogle_min'] for i in secilen])
    r = np.log(np.maximum(y, 0.01) / np.maximum(tah, 0.01))
    return tah, r


BANT_YONTEMI = 'nicel'                  # 'nicel': artıkların P10–P90'ı; 'uyumlu': küçük örnek düzeltmeli sıra
TABAN_HATA = 0.05                       # model hatası tabanının alt sınırı (çok aboneli trafoda bile) [Yorum]
# Taban artıklardan seçilir (taban_sec). Sürüm 1.2 şehirlerinde mahalle farkı (ADR-0008) abone sayısıyla
# sönmüyor: sabit 0,05 tabanla çok aboneli konut trafosu "yüksek güven" alıp en çok yanılan oluyordu.
TABAN_ADAYLARI = (0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 1.0, 2.0, 5.0)
# Fatura yoksa taban en az 0,3: büyüklüğü abone sayısından bilen model mahalle farkını göremez; gerçek veride
# müşteri başına öğlen yükünün trafodan trafoya değişimi 0,46 (İspanya, karışık), konut hedefi 0,3–0,4 (ADR-0008).
# 12 ölçülüyle taban seçimi bunu her şehirde yakalayamadı (şehir 1–10: "yüksek güven" en çok yanılan oldu).
TABAN_FATURASIZ = 0.3


def etkin_abone(A):
    """Enerji ağırlıklı etkin abone sayısı: (Σ E)² ÷ Σ E_i², abone başına ortalama enerjiyle (Kıb-Tek tarife
    ortalaması). 40 ev ≈ 40; tek otel + birkaç dükkân ≈ 1–2. Abonelerin büyüklük farkı toplamda 1/√N ile söner."""
    e = E_KW
    pay = (A * e).sum(1) ** 2
    payda = (A * e ** 2).sum(1)
    return np.divide(pay, payda, out=np.ones(len(A)), where=payda > 0)


def olcek_birimi(A, taban=TABAN_HATA):
    """Göreli belirsizliğin ölçeği: √(1/N_etkin + taban²)."""
    return np.sqrt(1 / np.maximum(etkin_abone(A), 1) + taban ** 2)


def taban_sec(r, A, en_az=TABAN_HATA):
    """Model hatası tabanı (en az `en_az`), ölçülülerin bir-dışarıda log artıklarından: Var(r) ∝ 1/N_etkin + taban² varsayımıyla
    profil olabilirlik, TABAN_ADAYLARI içinden. Küçük taban = hata abone sayısıyla söner (abone büyüklüğü farkı);
    büyük taban = her trafoda aynı (mahalle farkı, ya da fatura büyüklüğü zaten verdiği için)."""
    x = 1 / np.maximum(etkin_abone(A), 1)

    def olabilirlik(c):
        v = x + c * c
        return -0.5 * np.log(v).sum() - len(r) / 2 * math.log(max(float(np.mean(r ** 2 / v)), 1e-12))
    return max((c for c in TABAN_ADAYLARI if c >= en_az), key=olabilirlik)


def bant_carpanlari(r):
    """%80 bandın alt/üst çarpanı, bir-dışarıda log artıklarından.
    'nicel': P10 ve P90 (doğrusal ara değer). 'uyumlu' (conformal): alt sıra ⌊(n+1)·0,1⌋, üst ⌈(n+1)·0,9⌉;
    n = 12'de en küçük ve en büyük artık. Bir-dışarıda kötümser: dışarı alınan çoğu zaman tabakasının tek
    ölçülüsü, ölçülmeyen trafonun tabakasında ise ölçülü var; 'uyumlu' bu yüzden kapsamayı %100'e itti
    (Faz 2 günlüğü)."""
    if BANT_YONTEMI == 'nicel':
        alt, ust = np.quantile(r, BANT)
        return math.exp(alt), math.exp(ust)
    s = np.sort(r)
    n = len(s)
    alt = max(1, math.floor((n + 1) * BANT[0]))
    ust = min(n, math.ceil((n + 1) * BANT[1]))
    return math.exp(s[alt - 1]), math.exp(s[ust - 1])


def guven(p_max, uzak, gor, beklenen, faturali=True):
    """yuksek / orta / dusuk. beklenen = ölçülülerin bir-dışarıda hatası, trafonun etkin abone sayısına göre
    ölçeklenmiş (bkz. olcek_birimi). İlk sürümde yalnız olasılık + uzaklık vardı; hata sırasını tutturmuyordu
    (Faz 2 günlüğü). Fatura yoksa "yuksek" verilmez: büyüklük mahalle farkı kadar (±%30, ADR-0008) bilinmez;
    12 ölçülünün bir-dışarıda hatası şans eseri küçük çıkan şehirde "yuksek" en çok yanılan oluyordu (şehir 1–10)."""
    if (gor >= GUVEN_DUSUK_GORULMEMIS or uzak > GUVEN_DUSUK_UZAK or p_max < GUVEN_DUSUK_P
            or beklenen > GUVEN_DUSUK_HATA):
        return 'dusuk'
    if (faturali and p_max >= GUVEN_YUKSEK_P and uzak <= GUVEN_YUKSEK_UZAK and gor < 0.05
            and beklenen <= GUVEN_YUKSEK_HATA):
        return 'yuksek'
    return 'orta'


# ---------- çalıştırma ----------

def calistir(tr, X_tam, A, olcum_hepsi, secilen, hedef=None):
    """Bir çalıştırma: secilen ölçülü, hedef tahmin edilecek trafolar (varsayılan: aynı şehrin hepsi).
    -> (tahmin satırları, model, bant çarpanları)."""
    trafo_no = list(tr['trafo_no'])
    olcum = {trafo_no[i]: olcum_hepsi[trafo_no[i]] for i in secilen}     # model yalnız bunu görür
    m = modeli_kur(X_tam, A, olcum, secilen, trafo_no)
    loo, r = bir_disarida(X_tam, A, olcum, secilen, trafo_no)
    # Bant ve beklenen hata: artık, trafonun ölçek birimine bölünür (çok aboneli trafoda dar, tek büyük
    # müşterili trafoda geniş bant); P10–P90 bu bölünmüş artıklardan, sonra hedefin birimiyle çarpılır.
    faturali = fatura_var(tr)
    taban = taban_sec(r, A[secilen], TABAN_HATA if faturali else TABAN_FATURASIZ)
    u = r / olcek_birimi(A[secilen], taban)
    alt, ust = bant_carpanlari(u)
    u_ortanca = float(np.median(np.abs(u)))
    m.update(loo_log_artik=r, bant=(alt, ust), taban=taban)
    hedef_tr = tr if hedef is None else hedef[0]
    Xh, Ah = (X_tam, A) if hedef is None else (hedef[1], hedef[2])
    p, orta, uzak, gor = tahmin_et(m, Xh, Ah, list(range(len(hedef_tr))))
    birim = olcek_birimi(Ah, taban)
    beklenen = u_ortanca * birim                                 # beklenen göreli hata (log ölçek, ortanca)
    alt_c, ust_c = np.exp(np.log(alt) * birim), np.exp(np.log(ust) * birim)
    olculu = {} if hedef is not None else {trafo_no[i]: (j, loo[j]) for j, i in enumerate(secilen)}
    satirlar = []
    for i, t in enumerate(hedef_tr['trafo_no']):
        if t in olculu:
            j, o = olculu[t]
            ark, pr, g, olc = int(m['etiket'][j]), 1.0, 'yuksek', round(olcum[t]['ogle_min'], 2)
        else:
            ark, pr, o = int(p[i].argmax()), float(p[i].max()), float(orta[i])
            g, olc = guven(pr, float(uzak[i]), float(gor[i]), float(beklenen[i]), faturali), ''
        satirlar.append(dict(sehir=int(hedef_tr['sehir'].iloc[i]), trafo_no=t, olculdu=int(t in olculu),
                             olculu_sayi=len(secilen), arketip=ark, arketip_olasilik=round(pr, 3),
                             ogle_min_kw=round(o, 2), ogle_min_kw_p10=round(o * alt_c[i], 2),
                             ogle_min_kw_p90=round(o * ust_c[i], 2), ogle_min_kw_olculen=olc, guven=g))
    return satirlar, m


TAHMIN_SUTUNLARI = ['sehir', 'trafo_no', 'olculdu', 'olculu_sayi', 'arketip', 'arketip_olasilik', 'ogle_min_kw',
                    'ogle_min_kw_p10', 'ogle_min_kw_p90', 'ogle_min_kw_olculen', 'guven']


def csv_yaz(yol, sutunlar, satirlar):
    yol.parent.mkdir(parents=True, exist_ok=True)
    with open(yol, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=sutunlar, lineterminator='\n')
        w.writeheader()
        w.writerows(satirlar)


def arketip_satirlari(sehir, m):
    satir = []
    for j in range(m['k']):
        uyeler = [t for t, e in zip(m['ids'], m['etiket']) if e == j]
        for gt in ('isgunu', 'tatil'):
            egri = tepeye_bol(np.mean([tepeye_bol(m['olcum'][t][gt]) for t in uyeler], 0))
            satir += [dict(sehir=sehir, arketip=j, arketip_adi=m['ad'][j], gun_turu=gt, adim=a,
                           oran=round(float(v), 3)) for a, v in enumerate(egri)]
    return satir


def sehir_oku(klasor):
    tr = pd.read_csv(klasor / 'trafolar.csv', encoding='utf-8')
    gruplar = ozellikler(tr)
    X = birlestir(gruplar, ATAMA_GRUPLARI)
    A = abone_matrisi(tr)
    return tr, gruplar, X, A


def sehir_calistir(klasor, yalniz_ana=False):
    t0 = time.time()
    tr, _, X, A = sehir_oku(klasor)
    sehir = int(tr['sehir'].iloc[0])
    yuk = pd.read_csv(klasor / 'yuk_5dk.csv', encoding='utf-8',
                      usecols=['trafo_no', 'gun', 'gun_turu', 'adim', 'tuketim_kw'])
    olcum = olcumleri_hazirla(yuk, list(tr['trafo_no']))

    secilen = ogretici_sec(tr, OLCULU_ANA, f'sec-{sehir}')
    satirlar, m = calistir(tr, X, A, olcum, secilen)
    csv_yaz(klasor / 'tahmin.csv', TAHMIN_SUTUNLARI, satirlar)
    csv_yaz(klasor / 'arketipler.csv', ['sehir', 'arketip', 'arketip_adi', 'gun_turu', 'adim', 'oran'],
            arketip_satirlari(sehir, m))

    if not yalniz_ana:
        for n in DENEY_N:
            for t in range(1, DENEY_TEKRAR + 1):
                s = ogretici_sec(tr, n, f'sec-{sehir}-n{n}-t{t}')
                csv_yaz(klasor / 'deney' / f'tahmin_n{n}_t{t}.csv', TAHMIN_SUTUNLARI, calistir(tr, X, A, olcum, s)[0])

    loo_hata = np.abs(np.exp(-m['loo_log_artik']) - 1)          # |tahmin − ölçülen| ÷ ölçülen
    saf = saf_tahmin(tr, olcum, m)
    ozet = dict(sehir=sehir, fatura_kullanildi=fatura_var(tr), olculu=m['ids'], k=m['k'], siluet={str(k): round(v, 3) for k, v in m['siluet'].items()},
                arketip_adlari=m['ad'], kume_uye_sayisi=[int((m['etiket'] == j).sum()) for j in range(m['k'])],
                ortak_kw_abone={c: round(float(b), 3) for c, b in zip(ABONE, m['ortak'])},
                kume_kw_abone=[{c: round(float(b), 3) for c, b in zip(ABONE, bk)} for bk in m['beta']],
                taban=m['taban'], bant_birim_log=[round(math.log(m['bant'][0]), 3), round(math.log(m['bant'][1]), 3)],
                bant_p90_p10_ortanca=round(float(np.median([s['ogle_min_kw_p90'] / max(s['ogle_min_kw_p10'], 0.01)
                                                         for s in satirlar if s['olculdu'] == 0])), 2),
                loo_hata_ortanca=round(float(np.median(loo_hata)), 3),
                loo_hata_p90=round(float(np.quantile(loo_hata, 0.9)), 3),
                saf_tahmin=saf,
                gorulmemis_siniflar=[c for c, g in zip(ABONE, m['gorulmemis']) if g],
                guven_sayilari={g: sum(1 for s in satirlar if s['olculdu'] == 0 and s['guven'] == g)
                                for g in ('yuksek', 'orta', 'dusuk')},
                sure_sn=round(time.time() - t0, 1))
    with open(klasor / 'sablon_ozet.json', 'w', encoding='utf-8', newline='') as fh:
        json.dump(ozet, fh, ensure_ascii=False, indent=1)
    return dict(tr=tr, X=X, A=A, olcum=olcum, secilen=secilen, ozet=ozet)


def saf_tahmin(tr, olcum, m):
    """ADR-0008 madde 1, tanım karar masası 31 Ekim 17:26: saf tahmin modelin bildiğiyle kurulur:
    Σ öğlen ÷ Σ tarife enerjisi × trafonun tarife enerjisi; fatura varsa ayrıca Σ öğlen ÷ Σ fatura × fatura.
    Ölçülülerde bir-dışarıda hatası, modelin `loo_hata_*`'sıyla yan yana (bilgi; resmi kıyas sinav.py faz2)."""
    y = np.array([olcum[t]['ogle_min'] for t in m['ids']])
    enerji = {'tarife': tr[ABONE].to_numpy(float) @ np.array([MWH[c] for c in ABONE])}
    if fatura_var(tr):
        enerji['fatura'] = tr[FATURA_SUTUNU].to_numpy(float)
    out = {}
    for ad, e in enerji.items():
        es = e[m['secilen']]
        tah = (y.sum() - y) / np.maximum(es.sum() - es, 1e-9) * es       # her ölçülü, kalanların oranıyla
        h = np.abs(tah / np.maximum(y, 0.01) - 1)
        out[ad] = dict(oran_kw_mwh=round(float(y.sum() / max(es.sum(), 1e-9)), 4),
                       loo_hata_ortanca=round(float(np.median(h)), 3), loo_hata_p90=round(float(np.quantile(h, 0.9)), 3))
    return out


def capraz(klasorler, veriler):
    """Şehirler arası (2h): B'nin trafoları, bir önceki şehrin (A) 12 ölçülüsüyle kurulan modelle tahmin edilir."""
    for i, kb in enumerate(klasorler):
        ka = klasorler[i - 1]
        a, b = veriler[ka], veriler[kb]
        sat, _ = calistir(a['tr'], a['X'], a['A'], a['olcum'], a['secilen'], hedef=(b['tr'], b['X'], b['A']))
        sehir_a = int(a['tr']['sehir'].iloc[0])
        csv_yaz(kb / 'deney' / f'tahmin_capraz_s{sehir_a:03d}.csv', TAHMIN_SUTUNLARI, sat)


def onem(klasorler):
    """2d 'hangi veri en çok işe yarıyor': her sütun grubu çıkarılınca bir-dışarıda öğlen hatası (ölçülülerde)."""
    sonuc = {}
    for g in ['hic'] + ATAMA_GRUPLARI:
        adlar = [x for x in ATAMA_GRUPLARI if x != g]
        hatalar = []
        for k in klasorler:
            tr, gruplar, _, A = sehir_oku(k)
            X = birlestir(gruplar, adlar)
            yuk = pd.read_csv(k / 'yuk_5dk.csv', encoding='utf-8', usecols=['trafo_no', 'gun_turu', 'tuketim_kw'])
            olcum = olcumleri_hazirla(yuk, list(tr['trafo_no']))
            s = ogretici_sec(tr, OLCULU_ANA, f'sec-{int(tr["sehir"].iloc[0])}')
            trafo_no = list(tr['trafo_no'])
            _, r = bir_disarida(X, A, {trafo_no[i]: olcum[trafo_no[i]] for i in s}, s, trafo_no)
            hatalar.append(float(np.median(np.abs(np.exp(-r) - 1))))
        sonuc[g] = round(float(np.median(hatalar)), 3)
        print(f'  çıkarılan: {g:16s} bir-dışarıda öğlen hatası ortancası (şehirlerin ortancası) {sonuc[g]:.3f}')
    return sonuc


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('kok', nargs='?', default=str(KOK / 'data' / 'synthetic'))
    ap.add_argument('--sehir', type=int, help='yalnız bu tohum')
    ap.add_argument('--yalniz-ana', action='store_true', help='deneyleri ve şehirler arasını atla')
    ap.add_argument('--onem', action='store_true', help='sütun grubu önemini yazdır, dosya yazma')
    ap.add_argument('--faturasiz', action='store_true', help='yillik_tuketim_mwh olsa da kullanma (kıyas için)')
    a = ap.parse_args()
    global FATURA_KULLAN
    FATURA_KULLAN = not a.faturasiz
    klasorler = sorted(k for k in Path(a.kok).glob('sehir-*') if k.is_dir() and (k / 'trafolar.csv').exists()
                       and (k / 'yuk_5dk.csv').exists())
    if a.sehir is not None:
        klasorler = [k for k in klasorler if k.name == f'sehir-{a.sehir:03d}']
    if not klasorler:
        raise SystemExit(f'{a.kok} altında şehir yok (önce: python3 src/sehir_uret.py 1 20)')
    if a.onem:
        onem(klasorler)
        return
    veriler = {}
    for k in klasorler:
        veriler[k] = sehir_calistir(k, a.yalniz_ana)
        o = veriler[k]['ozet']
        print(f"{k.name}: k={o['k']} {o['arketip_adlari']} · bir-dışarıda hata ortanca {o['loo_hata_ortanca']:.0%}"
              f" P90 {o['loo_hata_p90']:.0%} · bant P90/P10 ortanca {o['bant_p90_p10_ortanca']:.2f}"
              f" · güven {o['guven_sayilari']} · {o['sure_sn']} sn")
    if not a.yalniz_ana and len(klasorler) > 1:
        capraz(klasorler, veriler)
        print(f'şehirler arası: {len(klasorler)} dosya (deney/tahmin_capraz_s<AAA>.csv)')


if __name__ == '__main__':
    main()
