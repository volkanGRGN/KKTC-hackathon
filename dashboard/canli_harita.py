"""Canlı tahmin haritası: kendi çizimimiz (harita karosu yok, internetsiz) ve sunum animasyonu (Volkan, 1 Kasım).

Etkileşim: Girne'deki farazi şehir; trafoya tıkla, ölçülmüş sayılır (sayfa modeli yeniden kurar).
Animasyon (~30 sn, kendi oynar): Girne'de küçük bir mahalle, sonra sağındaki ve solundaki mahalle belirir ve oradaki
trafo ölçülür; üç ölçümle model kurulur, 12 ölçüme kadar mahalleler açılır; sonra görünüm adaya açılır, öbür deneme
şehirleri kasabalara temsili yerleşir ve kasaba kasaba dolar. Güney Kıbrıs soluk, Kuzey belirgin.
Ölçülen trafo dolu nokta (kalın kontur), tahmin soluk halka; renk yük haritası ya da panel katmanı.

Renkler gerçek modelden: Girne'de her adım canli.py ile o anki ölçülerle kurulur (12. adım resmi koşuyla aynı küme);
kasabalarda her şehrin resmi 12 ölçümlü çıktısı (tahmin.csv, tepe.csv, kac_ev.csv; aynı ürün kodu).
Çizim canli_harita.js'te (tuval); tıklama ve animasyon olayları Python'a döner (st.components.v2).
Zemin: ada Natural Earth 1:50m (app/ada_kiyi.json, Civan'ın; yalnız okunur), Girne kıyısı ve binaları OSM
(data/raw/osm-kasaba/, git dışı; yoksa yalnız ada çizimi).
"""

import json
import math
from pathlib import Path

import pandas as pd
import streamlit as st

from ortak import GRI_HEX, HAM_KOK, KOK, MAVI_HEX, RENK_HEX, degisim_zamani, sehir_no

ADA_DOSYASI = KOK / "app" / "ada_kiyi.json"  # Natural Earth 1:50m, kamu malı (Civan, 31 Ekim)
GIRNE_KIYI = HAM_KOK / "osm-kasaba" / "girne_kiyi.json"
GIRNE_BINA = HAM_KOK / "osm-kasaba" / "girne_merkez.json"
JS_DOSYASI = Path(__file__).resolve().with_name("canli_harita.js")
OSM_ATIF = "© OpenStreetMap katkıcıları"
ETIKET = "gösterim — farazi şehir · noktalar temsili"

GIRNE_MERKEZ = (35.3375, 33.318)  # şehir üreticisinin referans noktası (osm-kasaba KAYNAK.txt)
GIRNE_YAMA = (35.22, 33.19, 35.42, 33.45)  # güney, batı, kuzey, doğu: ayrıntılı OSM kıyısının çizildiği dikdörtgen
BOYLAM_0, ENLEM_0 = 33.3, 35.2
KM_BOYLAM, KM_ENLEM = 90.97, 110.95  # 35,2° enlemde 1° boylam ≈ 91 km

# Öbür farazi şehirlerin temsili yeri (ad, enlem, boylam) [Yorum: yaklaşık kasaba merkezi, gerçek trafo yeri değil].
# Önem sırasıyla; veri setindeki şehir sayısı kadarı kullanılır, animasyon Girne'ye yakınlık sırasıyla oynar.
KASABALAR = [
    ("Lefkoşa", 35.19, 33.36), ("Gazimağusa", 35.12, 33.93), ("Güzelyurt", 35.20, 32.99),
    ("İskele", 35.29, 33.89), ("Lapta", 35.335, 33.165), ("Lefke", 35.11, 32.85),
    ("Dipkarpaz", 35.60, 34.38), ("Değirmenlik", 35.25, 33.48), ("Esentepe", 35.35, 33.58),
    ("Mehmetçik", 35.42, 34.08), ("Tatlısu", 35.38, 33.76), ("Akdoğan", 35.21, 33.73),
    ("Yeni Erenköy", 35.535, 34.19), ("Beyarmudu", 35.05, 33.70), ("Serdarlı", 35.25, 33.61),
    ("Kalkanlı", 35.23, 33.08), ("Çamlıbel", 35.30, 33.07), ("Yeniboğaziçi", 35.165, 33.89),
]
MAHALLE_SIGASI = 4  # ölçülen trafo dahil; 12 ölçümle 48 yer, 40 trafoya yeter
KUCULTME = 0.55 # kasabaya konan şehrin trafo dağılımı küçültülür, kasabalar üst üste binmesin

DOLULUK_SINIF = [  # yük haritası: temkinli uç (aralığın üstü); eşikler Özet'teki %80 ve %100 ile aynı
    (1.0, "kirmizi", "%100 üstü, gücü aşabilir"),
    (0.8, "sari", "%80–100, önce bak"),
    (0.0, "yesil", "%80 altı"),
]


def doluluk_sinifi(d):
    for esik, renk, ad in DOLULUK_SINIF:
        if d >= esik:
            return renk, ad
    return DOLULUK_SINIF[-1][1], DOLULUK_SINIF[-1][2]


def xy(enlem, boylam):
    """km: x doğuya, y güneye (tuvalde aşağı)."""
    return round((boylam - BOYLAM_0) * KM_BOYLAM, 3), round((ENLEM_0 - enlem) * KM_ENLEM, 3)


def duz(noktalar):
    """[(enlem, boylam)] -> [x0, y0, x1, y1, …] (km); JSON küçük kalsın."""
    sonuc = []
    for enlem, boylam in noktalar:
        sonuc.extend(xy(enlem, boylam))
    return sonuc


# ---------- zemin ----------

def _girne_kara():
    """OSM kıyı parçalarını uç uca ekleyip karayı çokgen yapar (OSM: kara solda, deniz sağda; zincir doğudan batıya).
    Ana zincir yamanın güney kenarına inilerek kapatılır; kapalı parçalar adacık."""
    ogeler = [o for o in json.loads(GIRNE_KIYI.read_text(encoding="utf-8"))["elements"]
              if o["type"] == "way" and "geometry" in o]
    adacik = [[(n["lat"], n["lon"]) for n in o["geometry"]] for o in ogeler if o["nodes"][0] == o["nodes"][-1]]
    zincir = [(list(o["nodes"]), [(n["lat"], n["lon"]) for n in o["geometry"]])
              for o in ogeler if o["nodes"][0] != o["nodes"][-1]]
    while True:
        for i in range(len(zincir)):
            j = next((j for j in range(len(zincir)) if j != i and zincir[j][0][0] == zincir[i][0][-1]), None)
            if j is not None:
                break
        else:
            break
        zincir[i] = (zincir[i][0] + zincir[j][0][1:], zincir[i][1] + zincir[j][1][1:])
        del zincir[j]
    guney = GIRNE_YAMA[0] - 0.02  # yamanın altına in: kapatma kenarı kırpılsın, çizgi görünmesin
    cokgenler = [n + [(guney, n[-1][1]), (guney, n[0][1])] for _, n in zincir if len(n) > 50]
    return [duz(c) for c in cokgenler + adacik]


def _osm_bina():
    binalar, yollar = [], []
    for o in json.loads(GIRNE_BINA.read_text(encoding="utf-8"))["elements"]:
        if o["type"] != "way" or "geometry" not in o:
            continue
        noktalar = duz((n["lat"], n["lon"]) for n in o["geometry"])
        if "building" in o.get("tags", {}):
            binalar.append(noktalar)
        elif "highway" in o.get("tags", {}):
            yollar.append(noktalar)
    return binalar, yollar


@st.cache_data(show_spinner=False, max_entries=4)
def _zemin(zamanlar):
    ada = json.loads(ADA_DOSYASI.read_text(encoding="utf-8"))
    kuzey, guney = [], []
    for halka in ada["dolgu"]:  # Natural Earth: "Cyprus" ve "N. Cyprus" ayrı
        ort_enlem = sum(e for _, e in halka) / len(halka)
        (kuzey if ort_enlem > 35.1 else guney).append(duz((e, b) for b, e in halka))
    zemin = dict(kuzey=kuzey, guney=guney, girne_kara=None, binalar=[], yollar=[], atif="",
                 yama=list(xy(GIRNE_YAMA[2], GIRNE_YAMA[1]) + xy(GIRNE_YAMA[0], GIRNE_YAMA[3])))
    if zamanlar[1] is not None:
        zemin["girne_kara"] = _girne_kara()
        zemin["atif"] = OSM_ATIF
    if zamanlar[2] is not None:
        zemin["binalar"], zemin["yollar"] = _osm_bina()
        zemin["atif"] = OSM_ATIF
    return zemin


def zemin():
    return _zemin(tuple(degisim_zamani(y) for y in (ADA_DOSYASI, GIRNE_KIYI, GIRNE_BINA)))


# ---------- animasyon ----------

def girne_sirasi(tr, oneri):
    """Önerilen ölçümlerin sırası: Girne merkezine en yakın mahalle, sonra sağındaki (doğu), sonra solundaki (batı),
    sonra ilk mahalleden uzaklık sırasıyla. Küme aynı kaldığı için son adım resmi koşuyla aynı."""
    p = {t: xy(e, b) for t, e, b in zip(tr["trafo_no"], tr["enlem"], tr["boylam"])}
    uzaklik = lambda t, x, y: math.hypot(p[t][0] - x, p[t][1] - y)
    kalan = list(oneri)
    mx, my = xy(*GIRNE_MERKEZ)
    sira = [min(kalan, key=lambda t: uzaklik(t, mx, my))]
    kalan.remove(sira[0])
    fx, fy = p[sira[0]]
    for yon in (1, -1):  # sağ, sol
        yanda = [t for t in kalan if (p[t][0] - fx) * yon > 0]
        aday = [t for t in yanda if abs(p[t][0] - fx) >= 0.5 * abs(p[t][1] - fy)] or yanda or kalan
        if aday:
            sira.append(min(aday, key=lambda t: uzaklik(t, fx, fy)))
            kalan.remove(sira[-1])
    return sira + sorted(kalan, key=lambda t: uzaklik(t, fx, fy))


def mahalleler(tr, sira):
    """Her trafo bir ölçülen trafonun mahallesine, o ölçümün adımında belirir. En yakın eşleşmeden başlayarak, mahalle
    başına en çok MAHALLE_SIGASI trafo: şehir merkezi sık, en yakın ölçülene bağlamak ilk mahalleyi 11 trafo yapıyordu."""
    p = [xy(e, b) for e, b in zip(tr["enlem"], tr["boylam"])]
    no = list(tr["trafo_no"])
    olculu = [no.index(t) for t in sira]
    sonuc = [None] * len(p)
    for k, i in enumerate(olculu):
        sonuc[i] = k
    sigasi = max(MAHALLE_SIGASI, -(-len(p) // len(olculu)))
    dolu = [1] * len(olculu)
    ciftler = sorted((math.hypot(p[i][0] - p[j][0], p[i][1] - p[j][1]), i, k)
                     for i in range(len(p)) if sonuc[i] is None for k, j in enumerate(olculu))
    for _, i, k in ciftler:
        if sonuc[i] is None and dolu[k] < sigasi:
            sonuc[i], dolu[k] = k, dolu[k] + 1
    return sonuc


def siniflar(sonuc, nolar):
    """Model sonucundan iki katmanın sınıfı (trafo sırasıyla); model yoksa None."""
    if sonuc is None:
        return None
    t = sonuc["tablo"].set_index("trafo_no")
    yuk = None
    if "doluluk_temkinli" in t:
        yuk = [doluluk_sinifi(t.at[n, "doluluk_temkinli"])[0] if pd.notna(t.at[n, "doluluk_temkinli"]) else None
               for n in nolar]
    panel = [t.at[n, "renk"] if isinstance(t.at[n, "renk"], str) else None for n in nolar]
    return dict(yuk=yuk, panel=panel)


@st.cache_data(show_spinner=False, max_entries=64)
def _kasaba_sehri(klasor, zamanlar):
    k = Path(klasor)
    oku = lambda ad, sutunlar: pd.read_csv(k / ad, encoding="utf-8", dtype={"trafo_no": str})[sutunlar]
    t = oku("trafolar.csv", ["trafo_no", "enlem", "boylam", "kva"]).merge(
        oku("tahmin.csv", ["trafo_no", "olculdu"]), on="trafo_no")
    t["yuk"] = None
    if (k / "tepe.csv").exists():
        t = t.merge(oku("tepe.csv", ["trafo_no", "tepe_kva_p90"]), on="trafo_no", how="left")
        t["yuk"] = [doluluk_sinifi(p / v)[0] if pd.notna(p) else None for p, v in zip(t["tepe_kva_p90"], t["kva"])]
    t["panel"] = None
    if (k / "kac_ev.csv").exists():
        t = t.drop(columns="panel").merge(oku("kac_ev.csv", ["trafo_no", "renk"]).rename(columns={"renk": "panel"}),
                                          on="trafo_no", how="left")
        t["panel"] = [r if isinstance(r, str) else None for r in t["panel"]]
    return t[["enlem", "boylam", "olculdu", "yuk", "panel"]].to_dict("records")


def kasabalar(klasorler, haric):
    """Öbür farazi şehirler kasabalara: her şehrin resmi çıktısı (tahmin.csv gerekir). Girne'ye yakınlık sırasıyla."""
    uygun = [k for k in klasorler if k != haric and sehir_no(k) < 800 and (k / "tahmin.csv").exists()]
    sonuc = []
    for klasor, (ad, enlem, boylam) in zip(uygun, KASABALAR):
        satirlar = _kasaba_sehri(str(klasor), tuple(degisim_zamani(klasor / a) for a in
                                                    ("trafolar.csv", "tahmin.csv", "tepe.csv", "kac_ev.csv")))
        orta_e = sum(s["enlem"] for s in satirlar) / len(satirlar)
        orta_b = sum(s["boylam"] for s in satirlar) / len(satirlar)
        noktalar = []
        for s in satirlar:
            x, y = xy(enlem + (s["enlem"] - orta_e) * KUCULTME, boylam + (s["boylam"] - orta_b) * KUCULTME)
            noktalar.append(dict(x=x, y=y, o=int(s["olculdu"]), yuk=s["yuk"], panel=s["panel"]))
        x, y = xy(enlem, boylam)
        sonuc.append(dict(ad=ad, sehir=klasor.name, x=x, y=y, n=noktalar))
    gx, gy = xy(*GIRNE_MERKEZ)
    return sorted(sonuc, key=lambda k: math.hypot(k["x"] - gx, k["y"] - gy))


def animasyon(h, sira, adimlar, klasorler, klasor):
    """sira: ölçülme sırası (trafo no); adimlar: her adımda siniflar() (3 ölçümden önce None)."""
    nolar = h["nolar"]
    return dict(
        mahalle=mahalleler(h["tr"], sira),
        sira=[nolar.index(t) for t in sira],
        adimlar=adimlar,
        kasabalar=kasabalar(klasorler, klasor),
    )


# ---------- bileşen ----------

CSS = """
.kok {position:relative; width:100%; overflow:hidden; border-radius:10px; user-select:none;}
canvas {display:block; width:100%; height:100%;}
.ipucu {position:absolute; pointer-events:none; display:none; max-width:340px; padding:8px 10px; border-radius:8px;
        font:12.5px/1.45 var(--st-font, sans-serif); background:rgba(20,24,31,.92); color:#f1f4f7;
        box-shadow:0 4px 14px rgba(0,0,0,.25); z-index:3;}
.ipucu b {font-weight:650;}
.dugmeler {position:absolute; top:10px; right:10px; display:none; gap:6px; z-index:2;}
.dugmeler button {font:600 12.5px var(--st-font, sans-serif); padding:6px 12px; border-radius:999px; cursor:pointer;
                  border:1px solid rgba(128,128,128,.45); background:rgba(255,255,255,.9); color:#1f2933;}
.dugmeler button:hover {border-color:#2a78d6;}
"""

_bilesen = None


def _harita():
    global _bilesen
    if _bilesen is None:
        _bilesen = st.components.v2.component("canli_harita", css=CSS,
                                              js=JS_DOSYASI.read_text(encoding="utf-8"))
    return _bilesen


def renkler():
    return dict(RENK_HEX, olculdu=MAVI_HEX, kapali=GRI_HEX)


def ciz(anahtar, veri, **olaylar):
    """veri: zemin, sehir (etkileşim), anim (oynarken), katman, lejant, oynat, oynat_no, yukseklik.
    olaylar: on_tiklama_change, on_bitti_change, on_bastan_change, on_don_change."""
    veri = dict(veri, etiket=ETIKET, renk=renkler())
    return _harita()(key=anahtar, data=veri, height="content", **olaylar)
