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

Sürüm 1.2 (sözleşme 1.2; ADR-0007, ADR-0008, karar masası 31 Ekim):
- Mahalle farkı: trafo başına log-normal tüketim çarpanı (σ = MAHALLE_SIGMA) küçük abonelere (konut, ticari I,
  sanayi I, su motoru); trafo başına saat kayması ±30 dk bütün abonelere. Sürüm 0.2'de rastgelelik yalnız şehir
  ve ev başınaydı; 40–80 evin ortalamasında ev farkı sönüyor, konut trafolarında müşteri başına öğlen yükünün
  trafodan trafoya değişimi gerçekten (İspanya EDP) çok düşük çıkıyordu (ADR-0008).
- trafolar.csv'ye yillik_tuketim_mwh: abonelerin yıllık enerjisi toplamı × fatura sapması 0,95–1,05 (ADR-0007).
- KKTC resmi tatilleri gun_turu = tatil (BAYRAMLAR); sürüm 0.2'de bayramlar iş günü sayılıyordu (PR #6 notu).
- Kıyı: OSM kıyı çizgisi varsa trafo karada kalana dek yeniden çekilir (Civan'ın app/ornek_veri.py
  kiyi_segmentleri() ve karada() fonksiyonları, aynen); yoksa eski "kuzeye en çok 400 m" kuralı + uyarı.
- Faz dağılımı: tek fazlı abonelerin faz ağırlıkları kentsel ±%25, kırsal ±%50 [Kaynaklı: UKPN 2015].
- Hava yılı 2023 / 2024 / 2025 (tüketim ve abone sayıları 2023).
- Trafo çıkış gerilimi 244–252 V (sürüm 0.2'de 246–250): İngiltere UKPN'de siteler arası bara gerilimi yayılımı
  ss 3,3 V, bizimki 1,2 V'tu; merkez 248 V (UKPN tasarım varsayımı) aynı. ayar.json faz_dengesizlik_ortanca.
- ayar.json: mahalle_sigma, kiyi_kontrolu, kva_tavan_sayisi (gereken güç 1000 kVA'yı aşıp tavana kesilen trafo;
  Nisan tepesi kVA'nın yarısının altında, şimdilik etkisiz; yaz benzetilirse yer tipi listeye 1600/2500 gerekir).

Sürüm 1.3 (Faz 8; karar masası 21:25, 21:51; tüzük madde 1, 6): üretici GERÇEĞE çapalanır, hedef plato.
Yeni rastgelelik ayrı akışlardan (`og13-`, `faz13-`, `ogle13-`); şehrin trafo / abone / hat yapısı 1.2 ile aynı kalır.
- Öğlen evde olma farkı: trafo (mahalle) ve abone başına öğlen çarpanı (log-normal), günlük enerji korunur. 1.2'de aynı
  tarifedeki bütün abonelerin eğri şekli aynıydı: trafo eğrilerinin benzerliği 0,99 (İspanya 0,93), faturalı model
  farazide %4 hata (İspanya %10). Parametreler şehir 1–10'da İspanya'ya göre (docs/log/2026-11-01-volkan-faz8-uretici.md).
- Faz dengesi: tek fazlı abonelerin bir payı fazlara sırayla bağlanır (dağıtım işletmecisinin dengelemesi). 1.2'de faz
  dengesizliği UKPN kent hatlarının ~2 katıydı (PR #11 günlüğü); pay UKPN'e göre.
- Öğlen orta gerilim değişimi şehir başına −%0,4…+%0,8 (UKPN: öğlen bara geceden ~1 V düşük; karar masası 18:46).
  1.2'de sabit +%0,8.

Sürüm 1.4 (B-Y1, Faz 11; karar masası 23:12, ADR-0014): yıl boyu tepe, yük haritasının cevap anahtarı. Ekleme
yalnız: Nisan çıktıları (trafolar.csv, yuk_5dk.csv, cevap anahtarının 1.3 sütunları) 1.3 ile birebir; yeni rastgelelik
ayrı akışlardan (`klima14-`, `yaz14-`, `kis14-`, `og14-`), şehrin ağı aynı.
- Aynı şehir, aynı ağ, aynı hava yılı için iki pencere daha: yazın en sıcak 7 günü (Haziran–Eylül, günlük ortalama
  sıcaklığın 7 günlük ortalaması en büyük) ve kışın en soğuk 7 günü (Ocak–Şubat, aynı ölçünün en küçüğü).
  Eğri o günün ayının EAC tipik günü; ışınım ve sıcaklık Open-Meteo'nun aynı dosyasından.
- Sıcaklık terimi: EAC tipik günü o ayın ortalama havasını ve günün şeklini (Temmuz konutunda gece klima tepesi)
  taşır; şekil veriden kalır, seviye sıcaklıkla değişir. Günün ortalama sıcaklığı o ayın günlük ortalamasından ΔT
  farklıysa günün yükü × (1 + β·ΔT) (yaz) ya da × (1 − β·ΔT) (kış), en az ×0,6. β sınıf başına [Yorum] × trafo başına
  klima / ısıtma yaygınlığı U(0,5; 1,5) (gizli; mahalle gibi). Bütün evler aynı havayı görür: klima tepesi eşzamanlı.
  β'lar Can'ın 20 Kıbrıs evi + sıcaklık analizine çapalanacak (Faz 11).
- Cevap anahtarına sonda: yılın net tepesi (`tepe_yil_kw`, kVA'sı, saati, ayı; brüt tepe ayrıca), yaz ve kış tepeleri, yıl pencerelerinde
  en düşük ev gerilimi (`v_min_tepe_v`, 207 V), `kva_tavan` (gereken güç 1000 kVA'yı aştı, listeye kesildi; Nisan
  donuk olduğu için 1.600 / 2.500 kVA eklenmedi). Yeni dosyalar `yuk_5dk_yaz.csv`, `yuk_5dk_kis.csv`.

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
ISINIM_DOSYALARI = [KOK / 'data' / 'raw' / 'open-meteo-lefkosa' / ad
                    for ad in ('lefkosa_saatlik_2023.csv', 'lefkosa_saatlik_2024_2025.csv')]
KIYI_JSON = KOK / 'data' / 'raw' / 'osm-kasaba' / 'girne_kiyi.json'
CIKTI = KOK / 'data' / 'synthetic'

SOZLESME_SURUMU = '1.2'
URETICI_SURUMU = '1.4'                   # 1.4: yıl boyu tepe (ek); 0.2: panel %3–25 (ADR-0006); 1.2: mahalle farkı, fatura, bayram, kıyı
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
KUZEY_SINIRI_M = 400                     # kıyı dosyası yoksa: referansın kuzeyine en çok 400 m [Yorum]
KVA_LISTESI = [25, 50, 100, 250, 400, 630, 1000]   # direk ≤ 400 [varsayım: Kıb-Tek şartnamesi, bağlantısı yok]; yer [Yorum]
# Dayanak [Kaynaklı: ASTOR A.Ş. kataloğu 2020, Elparts'ın sattığı marka, elparts.co]: yağlı dağıtım trafosu 50–5000 kVA
# (25 kVA bunun altında, kaynaksız; üretici 1.3'te kaynak ya da 50'den başlayan liste), kompakt trafo merkezi 1000 ve
# 1600 kVA (yaz benzetilirse yer tipi listeye 1600). Kıb-Tek'e özel güç listesi BULAMADIM.
HAVA_YILLARI = [2023, 2024, 2025]
# KKTC resmi tatilleri, Nisan [Kaynaklı: Ramazan Bayramı tarihleri Diyanet takvimi (Türkiye ile aynı ay takvimi;
# KKTC Resmi Gazete listesi BULAMADIM), 23 Nisan KKTC'de resmi tatil]. Arife yarım günü iş günü sayıldı [Yorum].
BAYRAMLAR = {dt.date(2023, 4, 21), dt.date(2023, 4, 22), dt.date(2023, 4, 23),
             dt.date(2024, 4, 10), dt.date(2024, 4, 11), dt.date(2024, 4, 12), dt.date(2024, 4, 23),
             dt.date(2025, 4, 1), dt.date(2025, 4, 23)}
MAHALLE_SIGMA = 0.35                     # ADR-0008 "≈ 0,3" [Yorum]; 0,30'da konut trafosu CV şehir içi ortanca 0,29 çıktı, hedef 0,3–0,4 (şehir 1–10)
MAHALLE_KAYMA_DK = 30                    # trafo başına saat kayması ±30 dk (ADR-0008)
# 1.3 (Faz 8): gerçeğe çapalama. Değerler günlükte; şehir 1–10'da ayarlandı, sınav şehirlerine bakılmadı.
OGLE_EVDE_SIGMA_TRAFO = 0.20             # trafo (mahalle) başına öğlen çarpanı, log-sd [Hesap: 1–10'da faturalı hata %10,0 / P90 %31,9 ↔ İspanya %10–11 / %32–33]
OGLE_EVDE_SIGMA_EV = 0.30                # abone başına öğlen çarpanı, log-sd [Yorum]
OGLE_MERKEZ_SAAT, OGLE_GENISLIK_SAAT = 12.5, 3.0     # öğlen çan eğrisi (çarpanın etki penceresi) [Yorum]
OG_OGLE_BANT = (-0.004, 0.008)           # öğlen OG değişimi, şehir başına düz [UKPN çapası; karar masası 18:46]
FAZ_DENGELI_P = {'kentsel': 0.7, 'turistik': 0.7, 'sanayi': 0.7, 'kirsal': 0.0}   # sırayla bağlanan pay [Hesap: UKPN kent ortanca %14,4 → 1–10'da %13,6; kırsalda zaten dengeli]
FATURA_SAPMA = (0.95, 1.05)              # tahmini okuma, farklı yıl (ADR-0007) [Yorum]
# Tek fazlı abonelerin faz ağırlığı 1 ± bu oran: tek fazlı PV faz dengesizliği varsayımı kentsel %25, kırsal %50
# [Kaynaklı: UKPN, "Validation of PV Connection Assessment Tool" kapanış raporu, Ofgem, Mart 2015]. Turistik ve
# sanayi bölgesi kentsel sayıldı [Yorum].
FAZ_SAPMA = {'kentsel': 0.25, 'turistik': 0.25, 'sanayi': 0.25, 'kirsal': 0.50}
# Trafo çıkışı (boşta faz gerilimi): şartname 250 V, kademe ayarı bilinmiyor; Kıbrıs dağılımı BULAMADIM. Bant ±4 V
# Kademe değiştirici var: dağıtım trafoları boşta (ya da yük altında) kademe değiştiricili [Kaynaklı: ASTOR kataloğu 2020];
# adım sayısı ve yüzdesi katalogda yok, BULAMADIM (uzmana soru 8). Bandın sebebi bu sahadaki elle ayar.
# [Yorum; karar masası 16:27: UKPN 20 trafoda gece ortanca 245,0 V, +1 ss 248,2 V, siteler arası ss 3,3 V; PR #11].
V0_BANT = (244.0, 252.0)
# 1.4 (B-Y1): yaz ve kış pencereleri. Aylar: pencerenin arandığı aylar (hava yılı). Gün sayısı bir hafta [Yorum].
MEVSIM_AYLARI = {'yaz': (6, 7, 8, 9), 'kis': (1, 2)}
MEVSIM_GUN = 7
# Sıcaklık duyarlılığı β: °C başına göreli yük değişimi, tipik günün o saatine göre [Yorum, hepsi varsayım: Kıbrıs'a
# özgü sınıf eğimi BULAMADIM; Can'ın 20 ev + sıcaklık analiziyle çapalanacak]. Konut ve küçük ticaret klimalı;
# sanayi ve büyük sanayi az; su motoru yazın sıcakla sulama artar, kışın değişmez.
SICAKLIK_BETA = {
    'yaz': {'konut': 0.045, 'ticari1': 0.03, 'dukkan': 0.03, 'otel': 0.02, 'sanayi1': 0.01, 'sanayi2': 0.005,
            'su_motoru': 0.02, 'yurt': 0.045},
    'kis': {'konut': 0.03, 'ticari1': 0.02, 'dukkan': 0.015, 'otel': 0.015, 'sanayi1': 0.005, 'sanayi2': 0.0,
            'su_motoru': 0.0, 'yurt': 0.03},
}
KLIMA_YAYGINLIK = (0.5, 1.5)             # trafo başına β çarpanı, gizli [Yorum]
SICAKLIK_TABAN = 0.6                     # sıcaklık çarpanı en az [Yorum]
# Yaz ve kış tatilleri: hafta sonu + KKTC resmi tatilleri [Kaynaklı: 1 Ocak ve 20 Temmuz KKTC resmi tatil; Kurban
# Bayramı tarihleri Diyanet takvimi, Nisan bayramlarıyla aynı kaynak; KKTC Resmi Gazete listesi BULAMADIM].
MEVSIM_BAYRAMLARI = {dt.date(y, 1, 1) for y in HAVA_YILLARI} | {dt.date(y, 7, 20) for y in HAVA_YILLARI} | {
    dt.date(2023, 6, 28), dt.date(2023, 6, 29), dt.date(2023, 6, 30), dt.date(2023, 7, 1),
    dt.date(2024, 6, 16), dt.date(2024, 6, 17), dt.date(2024, 6, 18), dt.date(2024, 6, 19),
    dt.date(2025, 6, 6), dt.date(2025, 6, 7), dt.date(2025, 6, 8), dt.date(2025, 6, 9)}

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
# Mahalle çarpanı yalnız küçük abonelere: büyük abonenin kendi büyüklük farkı (σ = 0,3) zaten tek başına
# trafoyu belirliyor; mahalle (gelir, ev büyüklüğü, boş yazlık, klima) konut ve küçük dükkânı ortak etkiler [Yorum].
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


def mevsim_egrileri(aylar):
    """1.4: {(sınıf, ay, gün türü): 288 değer} istenen aylar için, egrileri_yukle() ile aynı birim (yıllık ortalama = 1).
    EAC yoksa None (yer tutucu şehirde yaz / kış penceresi üretilmez)."""
    try:
        import profiller
        veri = profiller.oku(EAC_XLSX)
    except (ImportError, OSError):
        return None
    ort = {s: yillik_ortalama(veri, SINIFLAR[s][0]) for s in SINIFLAR}
    return {(s, ay, g): [x / ort[s] for x in profiller.sinif_egrisi(veri, SINIFLAR[s][0], ay, g)]
            for s in SINIFLAR for ay in aylar for g in ('is', 'tatil')}


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


def isinim_oku(yollar):
    """Open-Meteo saatlik CSV'leri -> {tarih: 24 değer}, değer = eğik (30°, güney) ışınım ÷ 1000 W/m².
    Satır 'T12:00' = 11:00–12:00 ortalaması (KAYNAK.txt)."""
    saatlik = {}
    for yol in yollar:
        saatlik.update(_isinim_dosyasi(yol))
    return saatlik


def _isinim_dosyasi(yol):
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


def sicaklik_oku(yollar):
    """1.4: Open-Meteo saatlik CSV'leri -> {tarih: 24 değer}, temperature_2m (°C), saatin kendisinde (anlık)."""
    out = {}
    for yol in yollar:
        with open(yol, encoding='utf-8') as fh:
            satirlar = fh.read().splitlines()
        bas = next(i for i, s in enumerate(satirlar) if s.startswith('time,'))
        sut = next(i for i, b in enumerate(satirlar[bas].split(',')) if b.startswith('temperature_2m'))
        for s in satirlar[bas + 1:]:
            p = s.split(',')
            if len(p) <= sut or not p[sut]:
                continue
            an = dt.datetime.fromisoformat(p[0])
            out.setdefault(an.date(), [float('nan')] * 24)[an.hour] = float(p[sut])
    return out


def gunun_sicakligi(sicaklik, tarih):
    """24 saatlik anlık değer -> 288 beş dakika, doğrusal (gün sonunda ertesi günün 00:00'ı, yoksa son saat)."""
    h = sicaklik[tarih]
    ert = sicaklik.get(tarih + dt.timedelta(days=1), [h[23]])[0]
    out = []
    for s in range(ADIM):
        x = s * 5 / 60
        i, w = int(x), x - int(x)
        a, b = h[i], (h[i + 1] if i < 23 else ert)
        out.append(a * (1 - w) + b * w)
    return out


def uc_hafta(sicaklik, yil, aylar, sicak):
    """1.4: hava yılının verilen aylarında ardışık MEVSIM_GUN gün; sıcak = günlük ortalama sıcaklığın ortalaması en
    büyük (sıcak geceler dahil; akşam klima tepesi gece sıcaklığını da görür [Yorum]), değilse en küçük. Eğri her günün
    kendi ayından."""
    gunler = sorted(d for d in sicaklik if d.year == yil and d.month in aylar and len(sicaklik[d]) == 24)
    deger = {d: statistics.fmean(sicaklik[d]) for d in gunler}
    en, sec = None, None
    for i in range(len(gunler) - MEVSIM_GUN + 1):
        pen = gunler[i:i + MEVSIM_GUN]
        if (pen[-1] - pen[0]).days != MEVSIM_GUN - 1:
            continue
        o = statistics.fmean(deger[d] for d in pen)
        if en is None or (o > en if sicak else o < en):
            en, sec = o, pen
    return sec, en


def ay_ortalamasi(sicaklik, yil, ay):
    """Ayın günlük ortalama sıcaklıklarının ortalaması: EAC tipik günü bu havayı taşır [Yorum]."""
    return statistics.fmean(statistics.fmean(sicaklik[d]) for d in sicaklik if d.year == yil and d.month == ay)


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


def og_carpani(g, rng, og_ogle=0.008):
    """Orta gerilim ortak çarpanı; eski benzetimin mv_factor'ü, kendi rastgelemizle. og_ogle: öğlen değişimi (1.3'te
    şehir başına OG_OGLE_BANT'tan; 1.2'de sabit 0,008)."""
    n, w = len(g), 12
    duz = [sum(g[max(0, i - w):min(n, i + w + 1)]) / (min(n, i + w + 1) - max(0, i - w)) for i in range(n)]
    m, ar = [], 0.0
    for i in range(n):
        h = (i % ADIM) * 5 / 60
        ar = 0.97 * ar + rng.gauss(0, 0.0006)
        m.append(1 + og_ogle * duz[i] - 0.006 * math.exp(-((h - 20) / 1.8) ** 2) + ar)
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


def kiyi_segmentleri():
    """OSM kıyı çizgisi parçaları [((boylam, enlem), (boylam, enlem))]; dosya yoksa None.
    Civan, app/ornek_veri.py (aynen; dosya yolu bu modülün)."""
    if not KIYI_JSON.exists():
        return None
    veri = json.loads(KIYI_JSON.read_text(encoding="utf-8"))
    segmentler = []
    for yol in veri["elements"]:
        noktalar = [(n["lon"], n["lat"]) for n in yol["geometry"]]
        segmentler += list(zip(noktalar, noktalar[1:]))
    return segmentler


def karada(boylam, enlem, segmentler):
    """Kuzeye ışın: kıyıyı tek sayıda kesiyorsa nokta karada (deniz kuzeyde). Civan, app/ornek_veri.py (aynen)."""
    kesisme = 0
    for (x1, y1), (x2, y2) in segmentler:
        if (x1 > boylam) != (x2 > boylam):
            y = y1 + (boylam - x1) * (y2 - y1) / (x2 - x1)
            kesisme += y > enlem
    return kesisme % 2 == 1


def konum(rng, k, kiyi):
    """Tipin alanından rastgele nokta; kıyı çizgisi varsa karada kalana dek, yoksa kuzeye en çok 400 m."""
    while True:
        if k[0] == 'halka':
            r, a = rng.uniform(k[1], k[2]), rng.uniform(0, 2 * math.pi)
            x, y = r * math.cos(a), r * math.sin(a)
        else:
            x, y = rng.uniform(k[1], k[2]), rng.uniform(k[3], k[4])
        x, y = round(x), round(y)
        if kiyi is None:
            if y <= KUZEY_SINIRI_M:
                return x, y
        elif karada(*reversed(enlem_boylam(x, y)), kiyi):
            return x, y


def sehir_kur(rng, n_trafo, ayar, tepe_orani, kiyi):
    sayi = tip_sayilari(rng, n_trafo)
    tipler = [t for t in TIPLER for _ in range(sayi[t])]
    rng.shuffle(tipler)
    trafolar, tavan = [], 0
    for ti, tip in enumerate(tipler):
        a = TIPLER[tip]
        abone = []
        for sinif, (lo, hi) in a['abone'].items():
            abone += [sinif] * rng.randint(lo, hi)
        n_hat = min(rng.randint(*a['hat']), len(abone))
        sig = ayar['mahalle_sigma']
        mahalle = rng.lognormvariate(-sig ** 2 / 2, sig)
        kayma = 5 * round(rng.uniform(-MAHALLE_KAYMA_DK, MAHALLE_KAYMA_DK) / 5)
        # boyut: sınıfın yıl içi tepesi (24 tipik gün) × yıllık ortalama kW, büyütme payı 1,2–2,0 [Yorum]
        # Plan tarife ortalamasıyla [Yorum]; mahalle çarpanı yalnız yılın tepesinde aşırı yük olacaksa girer
        # (Kıb-Tek aşırı yüklenen trafoyu büyütür [Yorum]). Mahalle doğrudan boyuta girseydi gizli fark Kıb-Tek'in
        # bildiği kva sütununa sızardı (şehir 1–10'da faturasız model artığıyla korelasyon 0,6); İspanya gerçek
        # verisinde şebeke bilgisi müşteri sayısına bir şey katmadı (PR #10). Hiç girmeyince 800'de 3 trafo
        # Nisan akşamında kVA'yı aştı (en kötü %121, 205,7 V).
        tepe = {s: SINIFLAR[s][2] * 1000 / 8760 * tepe_orani[s] * ayar['tuketim_carpani'][s] for s in SINIFLAR}
        gerek = sum(tepe[s] for s in abone) * rng.uniform(1.2, 2.0)
        gerek = max(gerek, sum(tepe[s] * (1 if s in BUYUK else mahalle) for s in abone))
        tavan += gerek > KVA_LISTESI[-1]
        kva = next((k for k in KVA_LISTESI if k >= gerek), KVA_LISTESI[-1])
        x, y = konum(rng, a['konum'], kiyi)
        d = FAZ_SAPMA[a['bolge']]
        fw = [rng.uniform(1 - d, 1 + d) for _ in range(3)]
        tr = dict(no=f'T{ti + 1:02d}', tip=tip, bolge=a['bolge'], kva=kva, x=x, y=y, kva_tavan=int(gerek > KVA_LISTESI[-1]),
                  montaj='direk' if kva <= 400 else 'yer', kablo=rng.choice(a['kablo']),
                  v0=round(rng.uniform(*V0_BANT), 1), mahalle=mahalle, kayma_dk=kayma,
                  fatura_sapma=rng.uniform(*FATURA_SAPMA), feeders=[], evler=[])
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
                olcek = rng.lognormvariate(-sigma ** 2 / 2, sigma) * (1 if sinif in BUYUK else mahalle)
                h = dict(id=len(tr['evler']), sinif=sinif, ph=ph, pv=pv, olcek=olcek)
                f['houses'].append(h)
                tr['evler'].append(h)
            tr['feeders'].append(f)
        trafolar.append(tr)
    return trafolar, sayi, tavan


def uretici13(trafolar, tohum):
    """1.3 eklemeleri, ayrı rastgele akışlarla (yapı aynı kalır): faz dengesi ve öğlen evde olma çarpanları."""
    for tr in trafolar:
        frng = random.Random(f'faz13-{tohum}-{tr["no"]}')
        p = FAZ_DENGELI_P.get(tr['bolge'], 0.0)
        for f in tr['feeders']:
            sira = frng.randrange(3)
            for h in f['houses']:
                if h['ph'] != 3 and frng.random() < p:
                    h['ph'] = sira % 3
                    sira += 1
        drng = random.Random(f'ogle13-{tohum}-{tr["no"]}')
        st_, se = OGLE_EVDE_SIGMA_TRAFO, OGLE_EVDE_SIGMA_EV
        tr['ogle_evde'] = drng.lognormvariate(-st_ ** 2 / 2, st_) if st_ > 0 else 1.0
        for h in tr['evler']:
            h['ogle_evde'] = drng.lognormvariate(-se ** 2 / 2, se) if se > 0 else 1.0


def ogle_agirlik(G):
    """Öğlen çarpanı G'nin 288 adımlık ağırlığı: 1 + (G − 1)·çan(saat). Günlük enerji sonra korunur."""
    return [1 + (G - 1) * math.exp(-(((i * 5 / 60) - OGLE_MERKEZ_SAAT) / OGLE_GENISLIK_SAAT) ** 2) for i in range(ADIM)]


def faz_dengesizligi(tr, ayar):
    """Hat başına (en büyük faz − ortalama) ÷ ortalama, faz yükü = yıllık enerji (tek fazlı abone kendi fazına,
    üç fazlı üçe eşit). UKPN'in tanımı (akşam faz yükü; PR #11 günlüğü); burada enerjiyle yaklaşık [Hesap]."""
    out = []
    for f in tr['feeders']:
        faz = [0.0, 0.0, 0.0]
        for h in f['houses']:
            e = SINIFLAR[h['sinif']][2] * ayar['tuketim_carpani'][h['sinif']] * h['olcek']
            for p in (range(3) if h['ph'] == 3 else (h['ph'],)):
                faz[p] += e / 3 if h['ph'] == 3 else e
        ort = sum(faz) / 3
        if ort > 0:
            out.append((max(faz) - ort) / ort)
    return out


def fatura_mwh(tr, ayar):
    """trafolar.csv yillik_tuketim_mwh: abonelerin yıllık enerjisi (eğri yıllık ortalaması = 1 olduğu için abone
    başına MWh × şehir çarpanı × abone ölçeği) toplamı × fatura sapması (ADR-0007). Brüt tüketim [Yorum]:
    mahsuplaşmalı panelli evin faturası net olabilir; Kıb-Tek'in sayaçtan içeri alınan enerjiyi ayrı bilip
    bilmediği BULAMADIM."""
    return tr['fatura_sapma'] * sum(SINIFLAR[h['sinif']][2] * ayar['tuketim_carpani'][h['sinif']] * h['olcek']
                                    for h in tr['evler'])


# ---------- benzetim ----------

def yuk_serisi(tr, ayar, egriler, gun_turleri, rng):
    """Abone başına 14 gün × 288 adım kW (brüt tüketim)."""
    gunluk = {}
    for s in SINIFLAR:
        kw = SINIFLAR[s][2] * 1000 / 8760 * ayar['tuketim_carpani'][s]
        k = (ayar['saat_kaymasi_dk'][s] + tr['kayma_dk']) // 5
        for g in ('is', 'tatil'):
            eg = egriler[(s, g)]
            gunluk[(s, g)] = [kw * eg[(i - k) % ADIM] for i in range(ADIM)]
    out = {}
    for h in tr['evler']:
        gurultu = 0.2 if h['sinif'] in ('konut', 'ticari1') else 0.05   # 5 dk dalgalanma [Yorum]
        G = tr.get('ogle_evde', 1.0) * h.get('ogle_evde', 1.0)          # 1.3: öğlen evde olma; günlük enerji korunur
        w = ogle_agirlik(G) if G != 1.0 else None
        sekil = {}
        for g in ('is', 'tatil'):
            taban = gunluk[(h['sinif'], g)]
            if w is None:
                sekil[g] = taban
            else:
                q = [b * x for b, x in zip(taban, w)]
                c = sum(taban) / sum(q)
                sekil[g] = [x * c for x in q]
        seri = []
        for tur in gun_turleri:
            for p in sekil['is' if tur == 'isgunu' else 'tatil']:
                seri.append(max(0.02, p * h['olcek'] * (1 + rng.gauss(0, gurultu))))
        out[h['id']] = seri
    return out


def yuk_serisi_mevsim(tr, ayar, egriler, tarihler, gun_turleri, T, Tort, mevsim, klima, rng):
    """1.4: yaz / kış penceresi, abone başına kW (brüt). yuk_serisi ile aynı adımlar; eğri günün ayından, üstüne
    günlük sıcaklık çarpanı max(SICAKLIK_TABAN, 1 ± β·klima·ΔT), ΔT = günün ortalama sıcaklığı − ayın günlük
    ortalaması (Tort[ay])."""
    isaret = 1.0 if mevsim == 'yaz' else -1.0
    out = {}
    kw = {s: SINIFLAR[s][2] * 1000 / 8760 * ayar['tuketim_carpani'][s] for s in SINIFLAR}
    kay = {s: (ayar['saat_kaymasi_dk'][s] + tr['kayma_dk']) // 5 for s in SINIFLAR}
    for h in tr['evler']:
        s = h['sinif']
        gurultu = 0.2 if s in ('konut', 'ticari1') else 0.05
        G = tr.get('ogle_evde', 1.0) * h.get('ogle_evde', 1.0)
        w = ogle_agirlik(G) if G != 1.0 else None
        beta = SICAKLIK_BETA[mevsim][s] * klima
        seri = []
        for d, (tarih, tur) in enumerate(zip(tarihler, gun_turleri)):
            eg = egriler[(s, tarih.month, 'is' if tur == 'isgunu' else 'tatil')]
            taban = [kw[s] * eg[(i - kay[s]) % ADIM] for i in range(ADIM)]
            if w is not None:
                q = [b * x for b, x in zip(taban, w)]
                c = sum(taban) / sum(q)
                taban = [x * c for x in q]
            dT = statistics.fmean(T[d * ADIM:(d + 1) * ADIM]) - Tort[tarih.month]
            f = max(SICAKLIK_TABAN, 1 + isaret * beta * dT)
            for p in taban:
                seri.append(max(0.02, p * h['olcek'] * f * (1 + rng.gauss(0, gurultu))))
        out[h['id']] = seri
    return out


def mevsim_benzet(tr, g, m, yuk):
    """1.4: pencere boyunca ev ev yük akışı; tüketim, üretim, ev gerilimi uçları, trafo görünür gücü (kVA)."""
    n = len(g)
    seri = dict(tuketim=[0.0] * n, uretim=[0.0] * n, vmax=[0.0] * n, vmin=[0.0] * n, s_kva=[0.0] * n)
    warm = None
    for i in range(n):
        V, seri['s_kva'][i] = tb.solve(tr, net_guc(tr, i, g, yuk), m[i], warm, iters=3 if warm else 6)
        warm = V
        seri['vmax'][i], seri['vmin'][i] = gerilim_uclari(tr, V)
        seri['tuketim'][i] = sum(yuk[h['id']][i] for h in tr['evler'])
        seri['uretim'][i] = sum(h['pv'] for h in tr['evler']) * g[i] * tb.PV_DERATE
    return seri


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
    seri = dict(tuketim=[0.0] * n, uretim=[0.0] * n, vmax=[0.0] * n, vmin=[0.0] * n, s_kva=[0.0] * n)
    warm = None
    for i in range(n):
        V, seri['s_kva'][i] = tb.solve(tr, net_guc(tr, i, g, yuk), m[i], warm, iters=3 if warm else 6)
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
        panel_yayginligi=round(rng.uniform(0.03, 0.25), 3),                         # %3–25 [ADR-0006]
        mahalle_sigma=MAHALLE_SIGMA, mahalle_kayma_dk=MAHALLE_KAYMA_DK, faz_sapma=FAZ_SAPMA,
        yeni_panel_kw=YENI_PANEL_KW, v_sinir_v=V_SINIR,
        referans_enlem=REFERANS[0], referans_boylam=REFERANS[1], veri_turu='farazi',
        profil_kaynagi=profil_kaynagi, kac_ev_sira_sayisi=SIRA_SAYISI)

    # hava yılı ve günler: 2023, 2024 ya da 2025 Nisan'ından ardışık 14 gün; hafta sonu ve bayram tatil
    yil = rng.choice(HAVA_YILLARI)
    bas = dt.date(yil, AY, rng.randint(1, 30 - GUN_SAYISI + 1))
    tarihler = [bas + dt.timedelta(days=d) for d in range(GUN_SAYISI)]
    gun_turleri = ['tatil' if t.weekday() >= 5 or t in BAYRAMLAR else 'isgunu' for t in tarihler]
    saatlik = isinim_oku([y for y in ISINIM_DOSYALARI if y.exists()])
    if all(t in saatlik for t in tarihler):
        g = [x for t in tarihler for x in gunun_isinimi(saatlik, t)]
        ayar.update(isinim_kaynagi='open-meteo-lefkosa', hava_yili=yil)
    else:
        print(f'UYARI: {yil} Nisan ışınımı yok (data/raw/open-meteo-lefkosa); yapay ışınım kullanılıyor.')
        g = yapay_isinim(random.Random(f'hava-{tohum}'))
        ayar.update(isinim_kaynagi='yapay', hava_yili=None)
    ayar.update(gun_turleri=gun_turleri, tarihler=[t.isoformat() for t in tarihler],
                bayramlar=[t.isoformat() for t in tarihler if t in BAYRAMLAR])
    og_ogle = random.Random(f'og13-{tohum}').uniform(*OG_OGLE_BANT)       # 1.3: şehir başına (ayrı akış)
    ayar.update(og_ogle=round(og_ogle, 4), ogle_evde_sigma=[OGLE_EVDE_SIGMA_TRAFO, OGLE_EVDE_SIGMA_EV],
                faz_dengeli_p=FAZ_DENGELI_P)
    m = og_carpani(g, random.Random(f'og-{tohum}'), og_ogle)

    kiyi = kiyi_segmentleri()
    if kiyi is None:
        print(f'UYARI: {KIYI_JSON.name} yok; yalnız "kuzeye en çok {KUZEY_SINIRI_M} m" kuralı '
              '(bazı trafolar denize düşebilir; indirme komutu data/raw/osm-kasaba/KAYNAK.txt).')
    trafolar, sayi, tavan = sehir_kur(rng, n_trafo, ayar, tepe_orani, kiyi)
    uretici13(trafolar, tohum)
    ayar.update(tip_sayilari=sayi, kiyi_kontrolu=kiyi is not None, kva_tavan_sayisi=tavan, v0_bant_v=list(V0_BANT),
                faz_dengesizlik_ortanca=round(statistics.median(d for tr in trafolar
                                                                for d in faz_dengesizligi(tr, ayar)), 3))

    # 1.4: yaz ve kış pencereleri, aynı hava yılı; ayrı akışlar (Nisan değişmez). EAC ve hava dosyası yoksa yok.
    mevsimler, egriler_m = {}, None
    if ayar['isinim_kaynagi'] == 'open-meteo-lefkosa' and profil_kaynagi == 'eac':
        sicaklik = sicaklik_oku([y for y in ISINIM_DOSYALARI if y.exists()])
        egriler_m = mevsim_egrileri(sorted({a for v in MEVSIM_AYLARI.values() for a in v}))
        for mev, aylar in MEVSIM_AYLARI.items():
            gunler, uc = uc_hafta(sicaklik, yil, aylar, mev == 'yaz')
            if egriler_m is None or not gunler or not all(d in saatlik for d in gunler):
                continue
            gt = ['tatil' if d.weekday() >= 5 or d in MEVSIM_BAYRAMLARI else 'isgunu' for d in gunler]
            gm = [x for d in gunler for x in gunun_isinimi(saatlik, d)]
            mevsimler[mev] = dict(tarihler=gunler, gun_turleri=gt, g=gm,
                                  T=[x for d in gunler for x in gunun_sicakligi(sicaklik, d)],
                                  Tort={a: ay_ortalamasi(sicaklik, yil, a) for a in {d.month for d in gunler}},
                                  m=og_carpani(gm, random.Random(f'og14-{mev}-{tohum}'), og_ogle))
            ayar[f'{mev}_penceresi'] = {'tarihler': [d.isoformat() for d in gunler], 'gun_turleri': gt,
                                        'gunluk_ortalama_c': round(uc, 1)}
    # Pencere eksikse yıl tepesi yazılmaz (sessizce Nisan tepesine düşmez; karar masası 23:35).
    eksik = [mev for mev in MEVSIM_AYLARI if mev not in mevsimler]
    if eksik:
        sebep = ('EAC eğrileri yok' if profil_kaynagi != 'eac' else
                 f'{yil} hava verisi yok (data/raw/open-meteo-lefkosa)' if ayar['isinim_kaynagi'] != 'open-meteo-lefkosa'
                 else f'{yil} için {", ".join(eksik)} haftası bulunamadı')
        print(f'UYARI: sehir-{tohum:03d}: yaz / kış penceresi üretilemedi ({sebep}); cevap anahtarında yıl tepesi '
              'sütunları BOŞ, bu şehir yük haritası sınavına girmez.')
    ayar.update(mevsim_pencereleri=sorted(mevsimler), sicaklik_beta=SICAKLIK_BETA,
                klima_yayginlik=list(KLIMA_YAYGINLIK), sicaklik_taban=SICAKLIK_TABAN,
                yil_tepe_kaynagi=None if eksik else 'nisan+yaz+kis')
    mevsim_satir = {mev: [] for mev in mevsimler}

    klasor = Path(cikti) / f'sehir-{tohum:03d}'
    klasor.mkdir(parents=True, exist_ok=True)
    trafo_satir, cevap_satir, yuk_satir = [], [], []
    for tr in trafolar:
        trng = random.Random(f'yuk-{tohum}-{tr["no"]}')
        yuk = yuk_serisi(tr, ayar, egriler, gun_turleri, trng)
        seri, cevap = trafo_benzet(tr, g, m, yuk, gun_turleri, trng)

        # 1.4: yaz ve kış; yılın net tepesi (net = tüketim − üretim, trafodan geçen)
        klima = random.Random(f'klima14-{tohum}-{tr["no"]}').uniform(*KLIMA_YAYGINLIK)
        pencere = [('nisan', seri, tarihler)]
        for mev, M in mevsimler.items():
            yk = yuk_serisi_mevsim(tr, ayar, egriler_m, M['tarihler'], M['gun_turleri'], M['T'], M['Tort'], mev,
                                   klima, random.Random(f'{mev}14-{tohum}-{tr["no"]}'))
            ms = mevsim_benzet(tr, M['g'], M['m'], yk)
            pencere.append((mev, ms, M['tarihler']))
            for i in range(len(M['g'])):
                d, s = divmod(i, ADIM)
                tk, ur = ms['tuketim'][i], ms['uretim'][i]
                mevsim_satir[mev].append([tohum, tr['no'], d, M['tarihler'][d].isoformat(), M['gun_turleri'][d], s,
                                          f'{s * 5 // 60:02d}:{s * 5 % 60:02d}', round(M['T'][i], 1), round(tk, 2),
                                          round(ur, 2), round(tk - ur, 2), round(ms['vmax'][i], 1),
                                          round(ms['vmin'][i], 1), round(ms['s_kva'][i], 1)])
        tepe, mev_tepe = None, {}
        brut = max(max(ps['tuketim']) for _, ps, _ in pencere)
        for ad, ps, tar in pencere:
            for i in range(len(ps['tuketim'])):
                net = ps['tuketim'][i] - ps['uretim'][i]
                mev_tepe[ad] = max(mev_tepe.get(ad, net), net)
                if tepe is None or net > tepe[0]:
                    d, s = divmod(i, ADIM)
                    tepe = (net, tar[d].month, f'{s * 5 // 60:02d}:{s * 5 % 60:02d}')
        cevap.update(tepe_yil_kw=tepe[0], tepe_ayi=tepe[1], tepe_saati=tepe[2],
                     tepe_yil_kva=max(max(ps['s_kva']) for _, ps, _ in pencere),
                     v_min_tepe_v=min(min(ps['vmin']) for _, ps, _ in pencere),
                     tepe_yaz_kw=mev_tepe.get('yaz'), tepe_kis_kw=mev_tepe.get('kis'), klima=klima, brut=brut)

        abone = {c: 0 for c in ABONE_SUTUNLARI}
        for h in tr['evler']:
            abone[SINIFLAR[h['sinif']][1]] += 1
        enlem, boylam = enlem_boylam(tr['x'], tr['y'])
        boylar = [f['boy'] for f in tr['feeders']]
        panelli = [h for h in tr['evler'] if h['pv'] > 0]
        trafo_satir.append([tohum, tr['no'], enlem, boylam, tr['x'], tr['y'], tr['bolge'], tr['montaj'],
                            tr['kva'], len(boylar), max(boylar), sum(boylar), tr['kablo'],
                            *[abone[c] for c in ABONE_SUTUNLARI], len(panelli),
                            round(sum(h['pv'] for h in panelli), 2), round(fatura_mwh(tr, ayar), 2)])

        faz = [sum(1 for h in tr['evler'] if h['ph'] == p) for p in range(4)]
        cevap_satir.append([tohum, tr['no'], tr['tip'], tr['v0'], *faz,
                            round(cevap['ogle_min_kw'], 2), round(cevap['ogle_min_kw_isgunu'], 2),
                            round(cevap['ogle_min_kw_tatil'], 2), round(cevap['ogle_min_net_kw'], 2),
                            round(cevap['tepe_kw'], 2), round(cevap['v_max_bugun_v'], 1),
                            round(cevap['v_min_bugun_v'], 1), cevap['kac_ev_aday'], cevap['kac_ev_gercek'],
                            cevap['kac_ev_gercek_min'], cevap['kac_ev_gercek_max'],
                            cevap['kac_ev_tavan'], cevap['kac_ev_sinir'], round(tr['mahalle'], 3), tr['kayma_dk'],
                            *(['', '', '', '', '', '', ''] if eksik else
                              [round(cevap['tepe_yil_kw'], 2), round(cevap['tepe_yil_kva'], 2), cevap['tepe_saati'],
                               cevap['tepe_ayi'], round(cevap['v_min_tepe_v'], 1), round(cevap['tepe_yaz_kw'], 2),
                               round(cevap['tepe_kis_kw'], 2)]),
                            tr['kva_tavan'], round(cevap['klima'], 3), '' if eksik else round(cevap['brut'], 2)])

        for i in range(len(g)):
            d, s = divmod(i, ADIM)
            tk, ur = seri['tuketim'][i], seri['uretim'][i]
            yuk_satir.append([tohum, tr['no'], d, gun_turleri[d], s, f'{s * 5 // 60:02d}:{s * 5 % 60:02d}',
                              round(tk, 2), round(ur, 2), round(tk - ur, 2),
                              round(seri['vmax'][i], 1), round(seri['vmin'][i], 1)])

    csv_yaz(klasor / 'trafolar.csv',
            ['sehir', 'trafo_no', 'enlem', 'boylam', 'x_m', 'y_m', 'bolge', 'montaj', 'kva', 'hat_sayisi',
             'hat_boyu_max_m', 'hat_boyu_toplam_m', 'kablo', *ABONE_SUTUNLARI, 'panel_sayisi', 'panel_kw',
             'yillik_tuketim_mwh'],
            trafo_satir)
    csv_yaz(klasor / 'yuk_5dk.csv',
            ['sehir', 'trafo_no', 'gun', 'gun_turu', 'adim', 'saat', 'tuketim_kw', 'uretim_kw', 'net_kw',
             'v_max_v', 'v_min_v'], yuk_satir)
    csv_yaz(klasor / 'cevap_anahtari.csv',
            ['sehir', 'trafo_no', 'tip', 'v0_v', 'faz_a_ev', 'faz_b_ev', 'faz_c_ev', 'uc_faz_ev',
             'ogle_min_kw', 'ogle_min_kw_isgunu', 'ogle_min_kw_tatil', 'ogle_min_net_kw', 'tepe_kw',
             'v_max_bugun_v', 'v_min_bugun_v', 'kac_ev_aday', 'kac_ev_gercek', 'kac_ev_gercek_min',
             'kac_ev_gercek_max', 'kac_ev_tavan', 'kac_ev_sinir', 'mahalle_carpani', 'saat_kaymasi_dk',
             'tepe_yil_kw', 'tepe_yil_kva', 'tepe_saati', 'tepe_ayi', 'v_min_tepe_v', 'tepe_yaz_kw', 'tepe_kis_kw',
             'kva_tavan', 'klima_carpani', 'tepe_yil_brut_kw'],
            cevap_satir)
    for mev, satir in mevsim_satir.items():          # 1.4
        csv_yaz(klasor / f'yuk_5dk_{mev}.csv',
                ['sehir', 'trafo_no', 'gun', 'tarih', 'gun_turu', 'adim', 'saat', 'sicaklik_c', 'tuketim_kw',
                 'uretim_kw', 'net_kw', 'v_max_v', 'v_min_v', 'trafo_kva'], satir)
    ayar['sure_sn'] = round(time.time() - t0, 1)
    with open(klasor / 'ayar.json', 'w', encoding='utf-8', newline='') as fh:   # LF (karar masası 13:00)
        json.dump(ayar, fh, ensure_ascii=False, indent=1)

    vmax = max(r[13] for r in cevap_satir)
    n_abone = sum(len(tr['evler']) for tr in trafolar)
    kac = statistics.median(r[16] for r in cevap_satir)
    print(f'{klasor.name}: {len(trafolar)} trafo, {n_abone} abone, {ayar["sure_sn"]} sn; '
          f'en yüksek gerilim {vmax} V; kaç ev ortancası {kac}; profil {profil_kaynagi}, '
          f'ışınım {ayar["isinim_kaynagi"]}')
    return klasor


def main():
    ap = argparse.ArgumentParser(description='Deneme şehri üreticisi (Faz 1; sürüm 1.4, Faz 11 yıl boyu tepe).')
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
