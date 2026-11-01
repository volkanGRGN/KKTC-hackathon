"""Dashboard sayfalarının ortak parçaları: sabitler, renkler, biçim, veri okuma, etiket.

Genel sayfa (dashboard.py) ve canlı tahmin sayfası (canli_sayfa.py) buradan alır; aynı kural iki yerde yazılmasın.
"""

import html
import json
import os
from pathlib import Path

import pandas as pd
import streamlit as st

KOK = Path(__file__).resolve().parent.parent
VERI_KOK = Path(os.environ.get("DASHBOARD_VERI") or KOK / "data" / "synthetic")
HAM_KOK = KOK / "data" / "raw"
ICERIK_DOSYASI = Path(__file__).resolve().with_name("icerik.json")
ANAHTAR = ["sehir", "trafo_no"]

SAHTE_SEHIR_ALT_SINIR = 900  # sözleşme: sahte şehir 900–999
GERCEK_VERI_SEHIRLERI = range(800, 900)  # sözleşme 1.2: gerçek ölçüm verisi

# Renkler haritayla aynı (app/harita.py RENKLER); her zaman yazısıyla birlikte gösterilir.
RENK_SIRA = ["yesil", "sari", "kirmizi"]
RENK_HEX = {"yesil": "#2ea043", "sari": "#f0b41e", "kirmizi": "#d2322d"}
RENK_RGBA = {"yesil": [46, 160, 67, 235], "sari": [240, 180, 30, 235], "kirmizi": [210, 50, 45, 235]}
GRI_HEX = "#8c8c8c"
GRI_RGBA = [150, 150, 150, 210]
MAVI_HEX = "#2a78d6"  # büyüklük (doluluk, eğri): tek ton
RENK_ADI = {"yesil": "yeşil", "sari": "sarı", "kirmizi": "kırmızı"}
RENK_BUYUK = {"yesil": "YEŞİL", "sari": "SARI", "kirmizi": "KIRMIZI"}  # str.upper() "YEŞIL" yazar
RENK_ISARET = {"yesil": "🟢", "sari": "🟡", "kirmizi": "🔴"}
VARSAYILAN_RENK_CUMLE = {
    "yesil": "İlk 2 başvuru güvenle sığar (≥ %98)",
    "sari": "Önce ölç",
    "kirmizi": "Ölç ya da güçlendir",
}
PV_UC_SIRA = ["yesil", "dolu_bayrak", "bos"]  # ADR-0017 güvenli uçlar
PV_UC_ADI = {"yesil": "yeşil", "dolu_bayrak": "büyük olasılıkla dolu", "bos": "renksiz, başvuruda bakılır"}
PV_UC_HEX = {"yesil": RENK_HEX["yesil"], "dolu_bayrak": RENK_HEX["kirmizi"], "bos": GRI_HEX}
DONEM_SIRA = ["sabah", "ogle", "ogleden_sonra", "gece"]
DONEM_ADI = {
    "sabah": "sabah (04–10)", "ogle": "öğle (10–14)",
    "ogleden_sonra": "öğleden sonra (14–20)", "gece": "gece (20–04)",
}
AY_ADI = {1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran", 7: "Temmuz",
          8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"}
GUVEN_ADI = {"yuksek": "yüksek", "orta": "orta", "dusuk": "düşük", "on": "ön sürüm"}
BOLGE_ADI = {"kentsel": "kentsel", "kirsal": "kırsal", "turistik": "turistik", "sanayi": "sanayi"}
SINIR_ADI = {"gerilim": "gerilim (259 V)", "isil": "ısıl (trafo gücü)"}
GUN_TURU_ADI = {"isgunu": "iş günü", "tatil": "tatil"}
ABONE_ADI = {
    "abone_konut": "konut", "abone_ticari1": "ticari I", "abone_ticari2": "ticari II",
    "abone_turizm": "turizm", "abone_sanayi1": "sanayi I", "abone_sanayi2": "sanayi II",
    "abone_su_motoru": "su motoru",
}
TEPE_KAYNAGI_ADI = {
    "model": "model (ölçülmedi)", "olcum_nisan": "Nisan ölçümüne bağlı",
    "kayit_md": "Kıb-Tek en yüksek talep kaydı", "kayit_etut": "Kıb-Tek yük etüdü",
}
KOR_NOKTA_ADI = {"mayis_temmuz": "gerçek veri baharda, tepe yazın", "klima_kuyrugu": "sıcak dalga ölçülmedi"}
OGLE_ADIMLARI = range(132, 168)  # 11:00–14:00, sözleşme "Öğlen penceresi"
V_AKSAM_SINIR = 207
DOLU_ESIK = 0.8

DURUM = {
    "gecti": ("GEÇTİ", "✓", RENK_HEX["yesil"]),
    "kaldi": ("KALDI", "✗", RENK_HEX["kirmizi"]),
    "uyari": ("UYARI", "!", "#d9822b"),
    "bilgi": ("BİLGİ", "i", GRI_HEX),
}
VERI_TURU = {
    "farazi": "farazi şehir — gösterim",
    "gercek": "gerçek veri — Kıbrıs değil",
    "kaynakli": "kaynaklı",
    "sahte_kayit": "sahte kayıtla — gösterim",
    "hesap": "kaynaklı fiyatlardan kaba hesap",
}
KATMANLAR = [  # sıra: Volkan 1 Kasım, "yük haritası öne"
    ("sorun", "Sorun", "Neden önemli"),
    ("yuk", "Yük haritası", "Trafo ne kadar dolu · yılın tepesi, ön sürüm"),
    ("panel", "Panel katmanı", "Güneş için ne kadar yer var · bahar öğleni"),
    ("maliyet", "Maliyet", "Ölçüm ve pilot · kaba hesap"),
]
DOSYALAR = [  # Ham veri sekmesi. cevap_anahtari.csv bilerek yok (sözleşme: yalnız sınav okur).
    ("trafolar.csv", "Trafo tablosu: Kıb-Tek'in bildiği (konum, güç, hat, abone, panel)"),
    ("tahmin.csv", "Öğlen yükü tahmini ve hangi trafonun ölçülü olduğu"),
    ("kac_ev.csv", "Panel katmanı: kaç ev, renk, %40 kuralı, olasılıklar"),
    ("tepe.csv", "Yük haritası: yılın tepesi, doluluk, akşam gerilimi (ön sürüm)"),
    ("arketipler.csv", "Günlük eğri şablonları"),
    ("kayitlar.csv", "Kıb-Tek kayıtları: sahte, deneme; harita ve resmi hesap okumaz"),
    ("kibtek_tepe.csv", "Kıb-Tek tepe kayıtları (deneme)"),
    ("kibtek_fider.csv", "Kıb-Tek fider tepeleri (deneme)"),
    ("yuk_5dk.csv", "5 dakikalık yük, Nisan: yalnız ölçülü trafolar"),
    ("ayar.json", "Şehrin ayarları (üretici)"),
    ("sablon_ozet.json", "Şablon modelinin özeti"),
    ("tepe_ozet.json", "Tepe modelinin özeti"),
]
DEPO_VARSAYILAN = "https://github.com/volkanGRGN/KKTC-hackathon"

CSS = """
<style>
.kimlik {border:1px solid rgba(128,128,128,.28); border-radius:14px; padding:18px 22px 16px; margin:0 0 12px;
         background:linear-gradient(135deg, rgba(46,160,67,.12), rgba(42,120,214,.07));}
.kimlik .ust {font-size:.78rem; letter-spacing:.06em; text-transform:uppercase; opacity:.75;}
.kimlik h1 {font-size:2.15rem; line-height:1.15; margin:.2rem 0 .4rem; padding:0;}
.kimlik .calisma {font-size:.95rem; font-weight:400; opacity:.65;}
.kimlik .cumle {font-size:1.06rem; margin:0 0 .75rem; max-width:64rem;}
.cipler {display:flex; flex-wrap:wrap; gap:6px;}
.cip {font-size:.82rem; padding:3px 11px; border-radius:999px; border:1px solid rgba(128,128,128,.32);
      background:rgba(128,128,128,.07); color:inherit; text-decoration:none;}
a.cip:hover {border-color:rgba(42,120,214,.7);}
.yigin {display:flex; gap:2px; height:22px; border-radius:4px; overflow:hidden; margin:.45rem 0 .55rem;}
.yigin div {min-width:3px;}
.lejant {font-size:.92rem; line-height:1.75;}
.nokta {font-size:1.05rem;}
.buyuk {font-size:2rem; font-weight:650; line-height:1.15; margin:.25rem 0 .2rem;}
.soluk {opacity:.72; font-size:.86rem;}
.rozet {display:inline-block; font-size:.72rem; font-weight:700; letter-spacing:.04em; padding:1px 9px;
        border-radius:999px; border:1.5px solid; margin-right:6px;}
.rakam {font-size:1.85rem; font-weight:650; line-height:1.15; margin:.5rem 0 .2rem;}
.rakam-baslik {font-weight:600; margin-bottom:.3rem;}
.bilgi {border-collapse:collapse; width:100%;}
.bilgi td {padding:3px 10px 3px 0; vertical-align:top; font-size:.9rem; border:none;}
.bilgi td:first-child {opacity:.68; white-space:nowrap; width:44%;}
.sehir-satir {display:grid; grid-template-columns:5.5rem 1fr 7rem; align-items:center; gap:10px; font-size:.88rem;}
.sehir-satir .yigin {margin:.2rem 0;}
.kutular {display:grid; grid-template-columns:repeat(auto-fit, minmax(150px, 1fr)); gap:8px; margin:.3rem 0 .6rem;}
.kutu {border:1px solid rgba(128,128,128,.3); border-radius:10px; padding:9px 12px;}
.kutu .etiket {font-size:.86rem; font-weight:600; line-height:1.25;}
.kutu .deger {font-size:1.55rem; font-weight:650; line-height:1.2; margin:.15rem 0 .2rem;}
.kutu .aciklama {font-size:.76rem; opacity:.72; line-height:1.32;}
</style>
"""


# ---------- biçim yardımcıları ----------

def tr(x, hane=0):
    """Türkçe sayı: binlik nokta, ondalık virgül."""
    if x is None or pd.isna(x):
        return "—"
    metin = f"{float(x):,.{hane}f}"
    return metin.replace(",", "\0").replace(".", ",").replace("\0", ".")


def yuzde(oran, hane=0):
    """Türkçe yüzde: işaret önde (%12)."""
    if oran is None or pd.isna(oran):
        return "—"
    return "%" + tr(oran * 100, hane)


def e(metin):
    return html.escape(str(metin))


def aralik(alt_uc, ust_uc, hane=0, birim=""):
    if pd.isna(alt_uc) or pd.isna(ust_uc):
        return "—"
    if round(alt_uc, hane) == round(ust_uc, hane):
        return f"{tr(alt_uc, hane)}{birim}"
    return f"{tr(alt_uc, hane)}–{tr(ust_uc, hane)}{birim}"


def yigin_html(parcalar):
    """Tek çubuk, parçalar arasında 2 px boşluk; parca = (ad, sayı, renk). Sıfırlar çizilmez."""
    toplam = sum(sayi for _, sayi, _ in parcalar) or 1
    kutular = "".join(
        f"<div title='{e(ad)}: {sayi} trafo ({yuzde(sayi / toplam)})' "
        f"style='flex:{sayi};background:{renk}'></div>"
        for ad, sayi, renk in parcalar if sayi > 0
    )
    return f"<div class='yigin'>{kutular}</div>"


def lejant_html(parcalar, cumleler=None):
    toplam = sum(sayi for _, sayi, _ in parcalar) or 1
    satirlar = []
    for anahtar, (ad, sayi, renk) in zip(cumleler or [None] * len(parcalar), parcalar):
        cumle = f" · <span class='soluk'>{e(anahtar)}</span>" if anahtar else ""
        satirlar.append(f"<span class='nokta' style='color:{renk}'>●</span> {e(ad)} "
                        f"<b>{tr(sayi)}</b> <span class='soluk'>{yuzde(sayi / toplam)}</span>{cumle}")
    return "<div class='lejant'>" + "<br>".join(satirlar) + "</div>"


def bilgi_tablosu(satirlar):
    """(etiket, değer) çiftleri, iki sütunlu sade tablo; boş değerler atlanır."""
    govde = "".join(f"<tr><td>{e(a)}</td><td>{e(d)}</td></tr>" for a, d in satirlar if d not in (None, "", "—"))
    st.markdown(f"<table class='bilgi'>{govde}</table>", unsafe_allow_html=True)


def saat_metni(dakika):
    return f"{int(dakika) // 60:02d}:{int(dakika) % 60:02d}"


# ---------- veri okuma (önbellek dosya değişince yenilenir) ----------

def degisim_zamani(yol):
    yol = Path(yol)
    return yol.stat().st_mtime_ns if yol.exists() else None


@st.cache_data(show_spinner=False)
def _csv(yol, zaman):
    if zaman is None:
        return None
    return pd.read_csv(yol, encoding="utf-8", dtype={"trafo_no": str})


def csv_oku(yol):
    return _csv(str(yol), degisim_zamani(yol))


@st.cache_data(show_spinner=False)
def _json(yol, zaman):
    if zaman is None:
        return None
    return json.loads(Path(yol).read_text(encoding="utf-8"))


def json_oku(yol):
    return _json(str(yol), degisim_zamani(yol))


def olculu_yuk(yol, olculu_nolar):
    """yuk_5dk.csv'den YALNIZ ölçülü trafoların satırları (ölçülmeyenin satırı cevap anahtarıdır)."""
    return _olculu_yuk(str(yol), tuple(olculu_nolar), degisim_zamani(yol))


@st.cache_data(show_spinner=False)
def _olculu_yuk(yol, olculu_nolar, zaman):
    if zaman is None:
        return None
    parcalar = pd.read_csv(yol, encoding="utf-8", dtype={"trafo_no": str}, chunksize=50_000)
    return pd.concat(p[p["trafo_no"].isin(olculu_nolar)] for p in parcalar)


def sehir_klasorleri(kok):
    return sorted(p for p in Path(kok).glob("sehir-*") if (p / "trafolar.csv").exists())


def sehir_no(klasor):
    return int(klasor.name.split("-", 1)[1])


def veri_setleri():
    """Şehir klasörü içeren kök ve alt klasörler (ör. data/synthetic, data/synthetic/u15)."""
    if not VERI_KOK.exists():
        return []
    adaylar = [VERI_KOK] + sorted(
        p for p in VERI_KOK.iterdir() if p.is_dir() and not p.name.startswith("sehir-")
    )
    return [k for k in adaylar if sehir_klasorleri(k)]


def kisa_yol(yol):
    try:
        return str(Path(yol).relative_to(KOK))
    except ValueError:
        return str(yol)


def topla(klasorler, ad):
    parcalar = [t for t in (csv_oku(k / ad) for k in klasorler) if t is not None]
    return pd.concat(parcalar, ignore_index=True) if parcalar else None


def birlesik_tablo(klasorler):
    """trafolar + tahmin + kac_ev + tepe, (sehir, trafo_no) ile; eksik dosya atlanır."""
    tablo = topla(klasorler, "trafolar.csv")
    for ad in ("tahmin.csv", "kac_ev.csv", "tepe.csv"):
        ek = topla(klasorler, ad)
        if ek is not None:  # tepe.csv'nin olculdu / guven sütunları _tepe ekiyle
            tablo = tablo.merge(ek, on=ANAHTAR, how="left", suffixes=("", "_tepe"), validate="one_to_one")
    return turetilmis(tablo)


def turetilmis(t):
    """Gösterim için türetilen sütunlar; hepsi sözleşme sütunlarından, cevap anahtarı yok."""
    t = t.copy()
    t["abone_toplam"] = t[[c for c in ABONE_ADI if c in t]].sum(axis=1)
    t["aday"] = (t["abone_konut"] - t["panel_sayisi"]).clip(lower=0)  # panelsiz konut
    if "kural40_ev" in t:  # civan.md KARAR 20:56: kural sayısı aday evle kesilir
        t["kural_gosterilen"] = t[["kural40_ev", "aday"]].min(axis=1)
    if "isil_pay_kw" in t:  # civan.md KARAR 18:46 kutu 3
        t["pay_karamsar"] = t[["isil_pay_kw", "gerilim_pay_kw_karamsar"]].min(axis=1).clip(lower=0)
        t["pay_iyimser"] = t[["isil_pay_kw", "gerilim_pay_kw_iyimser"]].min(axis=1).clip(lower=0)
    if "tepe_kva" in t:  # yük haritası: yılın tepesi ÷ trafo gücü
        t["doluluk"] = t["tepe_kva"] / t["kva"]
        t["doluluk_temkinli"] = t["tepe_kva_p90"] / t["kva"]
    return t


def etiket(no, ayar):
    """Haritayla aynı etiket kuralı (app/harita.py)."""
    if no >= SAHTE_SEHIR_ALT_SINIR:
        return "SAHTE VERİ — gösterim"
    if no in GERCEK_VERI_SEHIRLERI:
        kaynak = ayar.get("veri_kaynagi", "gerçek ölçüm verisi")
        return f"GERÇEK ÖLÇÜM — {kaynak} (Kıbrıs değil)"
    return "örnek veri (farazi şehir) — gösterim"


def veri_seti_sec():
    """Sol menü: veri seti (iki sayfada aynı seçim). -> (seçili klasör ya da None, şehir klasörleri)."""
    st.sidebar.header("Veri")
    setler = veri_setleri()
    if not setler:
        return None, []
    secili = st.sidebar.selectbox("Veri seti", setler, format_func=kisa_yol, key="veri_seti",
                                  help="data/synthetic ve altındaki şehir klasörü içeren klasörler.")
    return secili, sehir_klasorleri(secili)


def harita_yakinligi(enlem, boylam, yukseklik_px):
    """Bütün noktalar sığsın: en geniş açıklığa göre Web Mercator yakınlığı."""
    import math
    acik = max(enlem.max() - enlem.min(), boylam.max() - boylam.min(), 0.005)
    return min(14.0, math.log2(yukseklik_px * 360 / (256 * acik * 1.25)))


# Sunumda söylenecek ad ve altındaki açıklama (Volkan, 1 Kasım: "sunabileceğimiz şekilde, altına açıklaması").
# Teknik ad (ortanca, P90, temkinli uç) ekranda yok; açıklama ekibin anlaması için düz Türkçe.
SUNUM = {
    "trafo": ("Mahalle trafosu", "Şehirdeki trafolar; her biri bir mahalleyi besler."),
    "olculen": ("Ölçülen trafo", "Cihaz takılı (ya da takılmış sayılan) trafolar. Model yalnız bunlardan öğrenir."),
    "tahmin_edilen": ("Model tahmin etti", "Ölçülmeyen trafolar; değerleri ölçülenlerden öğrenilen şablondan."),
    "abone": ("Abone", "Konut, ticaret, otel, sanayi ve su motoru aboneleri birlikte."),
    "panel_kurulu": ("Kurulu güneş paneli", "Bugün şebekeye bağlı çatı panellerinin toplam gücü."),
    "doluluk_tipik": ("Tipik trafo doluluğu", "Trafoların yarısı bundan az, yarısı bundan çok dolu. Doluluk: yılın en "
                                               "yoğun saatindeki yük ÷ trafo gücü."),
    "once_bak": ("Önce bakılacak trafo", "En kötü durumda %80'den fazla dolu olabilir. Kıb-Tek önce bunlara bakar; "
                                         "çoğu gerçekte dolu çıkmaz."),
    "gucu_asabilir": ("Gücünü aşabilecek trafo", "En kötü durumda yılın en yoğun saatinde trafonun gücünü aşabilir."),
    "aksam_gerilim": ("Akşam gerilimi düşebilecek trafo", "En kötü durumda bir evde akşam gerilimi 207 V sınırının "
                                                          "altına inebilir."),
    "bos_guc": ("Yeni yük için boş güç", "En kötü durumda bütün trafolarda kalan güç (kVA): klima ve elektrikli araç "
                                         "için yer."),
    "tepe_sapma": ("Yoğun saat tahmininde sapma", "Yılın en yoğun saatindeki yükü tahmin ederken tipik trafoda gerçekten "
                                                  "bu kadar saptık."),
    "tepe_aralik": ("Gerçek, söylediğimiz aralıkta", "Verdiğimiz aralık gerçek değeri bu kadar trafoda içine aldı."),
    "dolu_yakalama": ("Dolu trafoyu yakalama", "Gerçekte %80'den dolu trafolardan kaçını önce bakılacaklar listesine "
                                               "aldık."),
    "ogle_sapma": ("Öğlen yükü tahmininde sapma", "Bahar öğleninde en düşük yükü tahmin ederken tipik trafoda gerçekten "
                                                  "bu kadar saptık. Panel kararının girdisi."),
    "yanlis_yesil": ("Yanlışlıkla \"yer var\" dediğimiz", "Yeşil dediğimiz ama gerçekte hiç ev sığmayan trafo. En "
                                                           "kritik ölçü; sınır %2."),
    "kural_yanlis": ("Bugünkü kuralın yanlış \"yer var\"ı", "Gerçekte dolu trafolardan bugünkü %40 kuralının "
                                                             "\"yer var\" dediği."),
}


def sunum(anahtar, deger, ek=""):
    """(sunum adı, değer, açıklama [+ ek]) üçlüsü; kutu_izgarasi için."""
    ad, aciklama = SUNUM[anahtar]
    return ad, deger, f"{aciklama} {ek}".strip()


def kutu_izgarasi(kutular):
    """Sunulabilir sayı kutuları: üstte ad, ortada değer, altında açıklama (dar sütunda da kesilmez).
    kutular: [(ad, değer, açıklama)]."""
    govde = "".join(f"<div class='kutu'><div class='etiket'>{e(a)}</div><div class='deger'>{e(d)}</div>"
                    f"<div class='aciklama'>{e(y)}</div></div>" for a, d, y in kutular)
    st.markdown(f"<div class='kutular'>{govde}</div>", unsafe_allow_html=True)
