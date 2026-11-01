"""Trafo Görünürlük Haritası — dashboard: proje kimliği, bütün tablolar, resmi rakamlar.

Haritadan ayrı, tek başına çalışır:  streamlit run dashboard/dashboard.py

Veri: data/synthetic altındaki şehir klasörleri ve alt klasörleri (ör. data/synthetic/u15/sehir-031),
biçimi docs/data/tablo-bicimi.md. Yeni veri gelince yalnız klasör değişir, kod değişmez. Başka bir kök için
DASHBOARD_VERI=<klasör>. Proje kimliği, resmi rakamlar ve sözlük dashboard/icerik.json'da (kod dışında).

Kurallar (sözleşme): cevap_anahtari.csv okunmaz; yuk_5dk.csv'den yalnız ölçülü trafoların satırları okunur.
Dil (civan.md KARAR 18:46, 19:13, 20:56): "en az" yok; "yaklaşık N ev (A–B)" ve "%80 ihtimalle"; vaat renkte.
Her rakamın katmanı yazılı: panel (bahar öğleni, güneş için yer) ya da yük haritası (yılın tepesi, doluluk).
"""

import html
import json
import math
import os
from pathlib import Path

import altair as alt
import pandas as pd
import pydeck as pdk
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
}
KATMANLAR = [
    ("sorun", "Sorun", "Neden önemli"),
    ("panel", "Panel katmanı", "Güneş için ne kadar yer var · bahar öğleni"),
    ("yuk", "Yük haritası", "Trafo ne kadar dolu · yılın tepesi, ön sürüm"),
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


# ---------- kimlik ----------

def kimlik_bandi(k):
    uyeler = ", ".join(u.get("ad", "") for u in k.get("uyeler", []))
    ust = " · ".join(x for x in (k.get("takim"), k.get("etkinlik"), k.get("kategori")) if x)
    cipler = []
    if k.get("takim"):
        cipler.append(f"Takım {k['takim']}" + (f": {uyeler}" if uyeler else ""))
    if k.get("tarih"):
        cipler.append(" · ".join(x for x in (k.get("tarih"), k.get("yer")) if x))
    if k.get("kullanici"):
        cipler.append(f"Kullanıcı: {k['kullanici']}")
    cip_html = "".join(f"<span class='cip'>{e(c)}</span>" for c in cipler)
    depo = k.get("depo", DEPO_VARSAYILAN)
    cip_html += f"<a class='cip' href='{e(depo)}' target='_blank'>Depo ↗</a>"
    calisma = f" <span class='calisma'>çalışma adı: {e(k['calisma_adi'])}</span>" if k.get("calisma_adi") else ""
    st.markdown(
        f"<div class='kimlik'><div class='ust'>{e(ust)}</div>"
        f"<h1>{e(k.get('ad', 'Trafo Görünürlük Haritası'))}{calisma}</h1>"
        f"<p class='cumle'>{e(k.get('tek_cumle', ''))}</p>"
        f"<div class='cipler'>{cip_html}</div></div>",
        unsafe_allow_html=True,
    )


def veri_bandi(klasorler, t):
    ayarlar = {sehir_no(k): (json_oku(k / "ayar.json") or {}) for k in klasorler}
    etiketler = sorted({etiket(no, a) for no, a in ayarlar.items()})
    st.warning(" · ".join(etiketler))

    def kume(anahtar):
        degerler = sorted({str(a[anahtar]) for a in ayarlar.values() if a.get(anahtar) not in (None, "")})
        return ", ".join(degerler) if degerler else "—"

    nolar = sorted(ayarlar)
    sehirler = f"şehir {nolar[0]}" if len(nolar) == 1 else f"{len(nolar)} şehir ({nolar[0]}–{nolar[-1]})"
    dosyalar = [ad for ad in ("tahmin.csv", "kac_ev.csv", "tepe.csv") if any((k / ad).exists() for k in klasorler)]
    st.caption(
        f"Veri: {kisa_yol(klasorler[0].parent)} · {sehirler} · {tr(len(t))} trafo · "
        f"üretici {kume('uretici_surumu')} · sözleşme {kume('sozlesme_surumu')} · hava yılı {kume('hava_yili')} · "
        f"tablolar: trafolar" + "".join(f", {ad[:-4]}" for ad in dosyalar)
    )


# ---------- grafikler ----------

def doluluk_grafigi(t):
    """Yük haritası: orta tahmin doluluğunun dağılımı, %10'luk kovalar; %80 ve %100 çizgisi."""
    d = (t["doluluk"].dropna() * 100).clip(lower=0)
    ust = max(110, int(d.max() // 10 + 1) * 10)
    kova = pd.cut(d, bins=list(range(0, ust + 10, 10)), right=False).value_counts(sort=False)
    df = pd.DataFrame({
        "bas": [i.left for i in kova.index],
        "son": [i.right for i in kova.index],
        "trafo": kova.to_numpy(),
    })
    df["aralik"] = [f"%{int(b)}–{int(s)}" for b, s in zip(df["bas"], df["son"])]
    df["son_bosluklu"] = df["son"] - 0.5  # çubuklar arasında ince boşluk
    cubuk = alt.Chart(df).mark_bar(
        color=MAVI_HEX, cornerRadiusTopLeft=4, cornerRadiusTopRight=4
    ).encode(
        x=alt.X("bas:Q", title="Doluluk, orta tahmin (%)", scale=alt.Scale(domain=[0, ust])),
        x2="son_bosluklu:Q",
        y=alt.Y("trafo:Q", title="Trafo sayısı"),
        y2=alt.datum(0),  # x2 varken çubuk dikey kalsın: alt uç sıfır
        tooltip=[alt.Tooltip("aralik:N", title="Doluluk"), alt.Tooltip("trafo:Q", title="Trafo")],
    )
    esik = pd.DataFrame({"x": [80, 100], "ad": ["%80", "%100"]})
    cizgi = alt.Chart(esik).mark_rule(strokeDash=[4, 3], color=GRI_HEX, strokeWidth=1.5).encode(x="x:Q")
    yazi = alt.Chart(esik).mark_text(align="left", dx=4, dy=4, baseline="top", color=GRI_HEX, fontSize=11).encode(
        x="x:Q", y=alt.value(0), text="ad:N"
    )
    st.altair_chart((cubuk + cizgi + yazi).properties(height=240), width="stretch")


def donem_grafigi(t):
    sayim = t["tepe_donemi"].value_counts()
    df = pd.DataFrame({"donem": [DONEM_ADI[d] for d in DONEM_SIRA], "trafo": [int(sayim.get(d, 0)) for d in DONEM_SIRA]})
    taban = alt.Chart(df).encode(
        y=alt.Y("donem:N", sort=[DONEM_ADI[d] for d in DONEM_SIRA], title=None, axis=alt.Axis(labelLimit=220)),
        x=alt.X("trafo:Q", title="Trafo sayısı"),
        tooltip=[alt.Tooltip("donem:N", title="Tepe dönemi"), alt.Tooltip("trafo:Q", title="Trafo")],
    )
    cubuk = taban.mark_bar(color=MAVI_HEX, cornerRadiusTopRight=4, cornerRadiusBottomRight=4, height=18)
    yazi = taban.mark_text(align="left", dx=4, fontSize=12, color=GRI_HEX).encode(text="trafo:Q")
    st.altair_chart((cubuk + yazi).properties(height=170), width="stretch")


def egri_grafigi(df, bantli):
    """Günlük eğri; bantlıysa %80 aralık açık alan, tahmin koyu çizgi. İmleçle saat ve değer."""
    x = alt.X("dakika:Q", title=None, scale=alt.Scale(domain=[0, 1440]),
              axis=alt.Axis(values=list(range(0, 1441, 180)), labelExpr="utcFormat(datum.value * 60000, '%H:%M')"))
    taban = alt.Chart(df).encode(x=x)
    katmanlar = []
    ipucu = [alt.Tooltip("saat:N", title="Saat"), alt.Tooltip("deger:Q", title="kW", format=".1f")]
    if bantli:
        katmanlar.append(taban.mark_area(color=MAVI_HEX, opacity=0.18).encode(y="p10:Q", y2="p90:Q"))
        ipucu += [alt.Tooltip("p10:Q", title="aralık alt (kW)", format=".1f"),
                  alt.Tooltip("p90:Q", title="aralık üst (kW)", format=".1f")]
    katmanlar.append(taban.mark_line(color=MAVI_HEX, strokeWidth=2).encode(y=alt.Y("deger:Q", title="kW")))
    yakin = alt.selection_point(nearest=True, on="pointerover", fields=["dakika"], empty=False)
    katmanlar.append(taban.mark_rule(color=GRI_HEX).encode(
        opacity=alt.condition(yakin, alt.value(0.7), alt.value(0)), tooltip=ipucu).add_params(yakin))
    katmanlar.append(taban.mark_point(color=MAVI_HEX, filled=True, size=60).encode(
        y="deger:Q", opacity=alt.condition(yakin, alt.value(1), alt.value(0))))
    st.altair_chart(alt.layer(*katmanlar).properties(height=230), width="stretch")


# ---------- özet ----------

def ozet_sekmesi(t, icerik):
    n = len(t)
    k = st.columns(4)
    k[0].metric("Trafo", tr(n), border=True)
    if "olculdu" in t:
        olc = int(t["olculdu"].sum())
        k[1].metric("Ölçülen trafo", f"{tr(olc)} · {yuzde(olc / n)}", border=True,
                    help="Cihaz takılı trafolar. Gerisinin yükü bunlardan öğrenilen şablonla tahmin edilir.")
    else:
        k[1].metric("Ölçülen trafo", "—", border=True, help="Tahmin tablosu (tahmin.csv) yok.")
    k[2].metric("Abone", tr(t["abone_toplam"].sum()), border=True, help="Bütün tarife sınıfları.")
    k[3].metric("Kurulu güneş paneli", f"{tr(t['panel_kw'].sum())} kW", border=True,
                help=f"{tr(t['panel_sayisi'].sum())} panelli abone, bugün bağlı.")
    st.write("")
    panel_ozeti(t, icerik)
    st.divider()
    yuk_ozeti(t)


def panel_ozeti(t, icerik):
    st.subheader("Panel katmanı · güneş için ne kadar yer var")
    st.caption("Bahar öğleni (11:00–14:00), yükün en düşük olduğu saatler. Sınır: evde 259 V ve trafo gücü. "
               "Bu bölümdeki bütün rakamlar panel katmanının.")
    if "renk" not in t:
        st.info("Kaç ev tablosu yok, renk ve kaç ev hesaplanmamış. Üretmek için:")
        st.code("python3 src/kac_ev_olasilik.py <şehir klasörlerinin kökü>", language="bash")
        return
    n = len(t)
    cumleler = {**VARSAYILAN_RENK_CUMLE, **icerik.get("renk_cumleleri", {})}
    s1, s2, s3 = st.columns(3)
    with s1:
        with st.container(border=True):
            st.markdown("**Trafo renkleri**")
            sayim = t["renk"].value_counts()
            parcalar = [(RENK_ADI[r], int(sayim.get(r, 0)), RENK_HEX[r]) for r in RENK_SIRA]
            st.markdown(yigin_html(parcalar), unsafe_allow_html=True)
            st.markdown(lejant_html(parcalar, [cumleler[r] for r in RENK_SIRA]), unsafe_allow_html=True)
            if "olculdu" in t:
                st.caption(f"{tr(t['olculdu'].sum())} trafo ölçülü, {tr(n - t['olculdu'].sum())} trafo tahmin.")
            if "pv_uc" in t:
                st.markdown("**Güvenli uçlar**")
                sayim = t["pv_uc"].value_counts()
                parcalar = [(PV_UC_ADI[u], int(sayim.get(u, 0)), PV_UC_HEX[u]) for u in PV_UC_SIRA]
                st.markdown(yigin_html(parcalar), unsafe_allow_html=True)
                st.markdown(lejant_html(parcalar), unsafe_allow_html=True)
                st.caption("Büyük olasılıkla dolu: bugün sınırı aşma olasılığı en az %70. Ret değil, başvuruda ölçüm.")
    with s2:
        with st.container(border=True):
            st.markdown("**Kaç ev daha panel takabilir**")
            kar, iyi = t["kac_ev_karamsar"].sum(), t["kac_ev_iyimser"].sum()
            if "kac_ev_orta" in t:
                st.markdown(f"<div class='buyuk'>yaklaşık {tr(t['kac_ev_orta'].sum())} ev</div>",
                            unsafe_allow_html=True)
                st.markdown(f"büyük olasılıkla toplam **{aralik(kar, iyi)} ev**")
            else:
                st.markdown(f"<div class='buyuk'>{aralik(kar, iyi)} ev</div>", unsafe_allow_html=True)
            st.caption("Trafo aralıklarının toplamı; her trafonun aralığı %80 ihtimalle.")
            kural, gosterilen = t["kural40_ev"].sum(), t["kural_gosterilen"].sum()
            st.markdown(f"Bugünkü %40 kuralı: **{tr(gosterilen)} ev**"
                        + (f" ({tr(kural)} evlik yer)" if kural > gosterilen else ""))
            st.caption(f"Kuralın sayısı panelsiz konut sayısıyla kesilir. Panelsiz konut toplam {tr(t['aday'].sum())}.")
    with s3:
        with st.container(border=True):
            st.markdown("**Güneş payının dolu kısmı**")
            panel = t["panel_kw"].sum()
            pay_k, pay_i = t["pay_karamsar"].sum(), t["pay_iyimser"].sum()
            dol_k = panel / (panel + pay_k) if panel + pay_k > 0 else float("nan")
            dol_i = panel / (panel + pay_i) if panel + pay_i > 0 else float("nan")
            metin = yuzde(dol_k) if yuzde(dol_k) == yuzde(dol_i) else f"{yuzde(dol_i)}–{yuzde(dol_k)}"
            st.markdown(f"<div class='buyuk'>{metin}</div>", unsafe_allow_html=True)
            st.caption(f"Bağlı paneller {tr(panel)} kW. Kalan pay {aralik(pay_k, pay_i)} kW (karamsar–iyimser). "
                       "Dolu kısım = bağlı ÷ (bağlı + kalan). Aralık geniş, çünkü hat ucundaki gerilim bilinmiyor.")
            st.caption("Öğlen yükünün trafo gücüne oranı doluluk değildir: öğlen yükü düşük trafo panel için daha risklidir.")
    kural_kiyasi(t)


def kural_kiyasi(t):
    """Bugünkü %40 kuralı ile renklerimiz aynı trafolarda yan yana (cevap anahtarı okunmaz)."""
    st.markdown("**Bugünkü %40 kuralı ile renklerimiz yan yana**")
    yer_var = t["kural_gosterilen"] >= 1
    satirlar = []
    for r in RENK_SIRA:
        m = t["renk"] == r
        satirlar.append({
            "Renk": f"{RENK_ISARET[r]} {RENK_ADI[r]}",
            "Trafo": int(m.sum()),
            "Kural \"yer var\" diyor": int((m & yer_var).sum()),
            "Kural \"yer yok\" diyor": int((m & ~yer_var).sum()),
        })
    sol, sag = st.columns([3, 2])
    with sol:
        st.dataframe(pd.DataFrame(satirlar), hide_index=True, width="stretch")
    with sag:
        celiski = int(((t["renk"] == "kirmizi") & yer_var).sum())
        st.markdown(f"Kuralın **\"yer var\"** dediği **{tr(celiski)} trafoya** biz kırmızı diyoruz: "
                    "büyük olasılıkla bugün bile sınırda.")
        st.caption("Hangisinin gerçekte dolu olduğunu yalnız sınav bilir; cevap anahtarı burada okunmaz. "
                   "Sınavdaki sonuç \"Model ne kadar iyi\" sekmesinde.")


def yuk_ozeti(t):
    st.subheader("Yük haritası · trafo ne kadar dolu")
    st.caption("Yılın en yüksek saati, çoğunlukla yaz akşamı. Sınır: trafo gücü ve akşam evde 207 V. Ön sürüm: yaz "
               "ölçümü yok, sıcak dalga ölçülmedi. Bu bölümdeki bütün rakamlar yük haritasının.")
    if "doluluk" not in t:
        st.info("Yılın tepesi tablosu (tepe.csv) yok. Üretmek için:")
        st.code("python3 src/tepe.py <şehir klasörlerinin kökü>", language="bash")
        return
    n = len(t)
    k = st.columns(5)
    k[0].metric("Ortanca doluluk", yuzde(t["doluluk"].median()), border=True,
                help="Yılın tepesi ÷ trafo gücü, orta tahmin; trafoların ortancası.")
    dolu = int((t["doluluk_temkinli"] >= DOLU_ESIK).sum())
    k[1].metric("%80'den dolu olabilir", f"{tr(dolu)} trafo", border=True,
                help="Temkinli uçta (aralığın üstü) doluluk %80 ve üstü. \"Önce bak\" listesi: dolu olanı kaçırmaz, "
                     "ama uyarıların çoğu gerçekte dolu değil.")
    asan = int((t["doluluk_temkinli"] > 1).sum())
    k[2].metric("Gücü aşabilir", f"{tr(asan)} trafo", border=True,
                help="Temkinli uçta yılın tepesi trafo gücünü aşıyor.")
    if "v_min_tepe_v_p10" in t:
        bak = int((t["v_min_tepe_v_p10"] < V_AKSAM_SINIR).sum())
        k[3].metric("Akşam: önce bak", f"{tr(bak)} trafo", border=True,
                    help="Akşam gerilimi: temkinli uçta bir evde 207 V altına inebilir. \"Yeterli\" dediklerimiz "
                         "sınavda hiç inmedi.")
    bos = t["bos_kva_p10"].clip(lower=0).sum() if "bos_kva_p10" in t else float("nan")
    k[4].metric("Boş güç, kVA", tr(bos), border=True,
                help="Yük için boş: trafo gücü − temkinli tepe, bütün trafoların toplamı; eksi olanlar sıfır sayıldı.")
    sol, sag = st.columns([3, 2])
    with sol:
        st.markdown("**Doluluk dağılımı** · orta tahmin")
        doluluk_grafigi(t)
        st.caption("Kesik çizgiler: %80 ve %100. %100 trafo gücüne eşit demek.")
    with sag:
        if "tepe_donemi" in t:
            st.markdown("**Yılın tepesi ne zaman**")
            donem_grafigi(t)
        if "tepe_ayi" in t:
            aylar = t["tepe_ayi"].value_counts().sort_index()
            st.caption("Tepe ayı: " + " · ".join(f"{AY_ADI.get(int(a), a)} {tr(s)}" for a, s in aylar.items()))
    st.caption(f"{tr(n)} trafo. Tepe trafo başına bilerek temkinli; şehir toplamı fider ya da sistem tepesi değildir.")


# ---------- trafolar ----------

def tablo_gorunumu(s, cok_sehir):
    g = pd.DataFrame(index=s.index)
    if cok_sehir:
        g["Şehir"] = s["sehir"]
    g["Trafo"] = s["trafo_no"]
    if "renk" in s:
        g["Renk"] = s["renk"].map(lambda r: f"{RENK_ISARET.get(r, '')} {RENK_ADI.get(r, r)}")
        if "kac_ev_orta" in s:
            g["Kaç ev"] = s["kac_ev_orta"]
        g["Aralık"] = [aralik(a, b) for a, b in zip(s["kac_ev_karamsar"], s["kac_ev_iyimser"])]
        g["%40 kuralı"] = s["kural_gosterilen"]
    if "pv_uc" in s:
        g["Güvenli uç"] = s["pv_uc"].map(PV_UC_ADI)
    if "doluluk" in s:
        g["Doluluk"] = s["doluluk"] * 100
        g["Doluluk temkinli"] = s["doluluk_temkinli"] * 100
        g["Tepe saati"] = s["tepe_saati"]
        if "v_min_tepe_v_p10" in s:
            g["Akşam alt uç (V)"] = s["v_min_tepe_v_p10"]
    g["kVA"] = s["kva"]
    g["Bölge"] = s["bolge"].map(lambda b: BOLGE_ADI.get(b, b))
    g["Montaj"] = s["montaj"]
    g["Abone"] = s["abone_toplam"]
    g["Panel (kW)"] = s["panel_kw"]
    if "olculdu" in s:
        g["Ölçüldü"] = s["olculdu"].map({1: "evet", 0: "hayır"})
        g["Güven"] = s["guven"].map(lambda v: GUVEN_ADI.get(v, v))
        g["Öğlen yükü (kW)"] = s["ogle_min_kw"]
    return g.reset_index(drop=True)


SUTUN_AYARI = {
    "Renk": st.column_config.TextColumn("Renk", help="Panel katmanı"),
    "Kaç ev": st.column_config.NumberColumn("Kaç ev", help="Panel katmanı: yaklaşık kaç ev daha panel takabilir"),
    "Aralık": st.column_config.TextColumn("Aralık", help="Panel katmanı: %80 ihtimalle"),
    "%40 kuralı": st.column_config.NumberColumn("%40 kuralı", help="Bugünkü kural, panelsiz konutla kesilmiş"),
    "Güvenli uç": st.column_config.TextColumn("Güvenli uç", help="Panel katmanı (ADR-0017)"),
    "Doluluk": st.column_config.NumberColumn("Doluluk", format="%%%.0f", help="Yük haritası: yılın tepesi ÷ trafo gücü, orta tahmin"),
    "Doluluk temkinli": st.column_config.NumberColumn("Doluluk temkinli", format="%%%.0f", help="Yük haritası: aralığın üstü"),
    "Tepe saati": st.column_config.TextColumn("Tepe saati", help="Yük haritası"),
    "Akşam alt uç (V)": st.column_config.NumberColumn("Akşam alt uç (V)", format="%.1f", help="Yük haritası: tepe anında en düşük ev gerilimi, temkinli uç; 207 V sınır"),
    "Panel (kW)": st.column_config.NumberColumn("Panel (kW)", format="%.1f", help="Bugün bağlı paneller"),
    "Öğlen yükü (kW)": st.column_config.NumberColumn("Öğlen yükü (kW)", format="%.1f", help="Panel katmanının girdisi: öğlen en düşük yük, orta tahmin"),
}


def trafolar_sekmesi(t, klasorler, tek):
    filtre = st.columns([2, 2, 1.3, 1.3])
    s = t
    if "renk" in t:
        renkler = filtre[0].multiselect("Renk (panel)", [r for r in RENK_SIRA if r in set(t["renk"])],
                                        format_func=lambda r: RENK_ADI[r], placeholder="hepsi")
        if renkler:
            s = s[s["renk"].isin(renkler)]
    bolgeler = filtre[1].multiselect("Bölge", sorted(t["bolge"].unique()),
                                     format_func=lambda b: BOLGE_ADI.get(b, b), placeholder="hepsi")
    if bolgeler:
        s = s[s["bolge"].isin(bolgeler)]
    if "olculdu" in t:
        olcum = filtre[2].selectbox("Ölçüm", ["hepsi", "ölçülü", "ölçülmedi"])
        if olcum != "hepsi":
            s = s[s["olculdu"] == (1 if olcum == "ölçülü" else 0)]
    ara = filtre[3].text_input("Trafo no", placeholder="ör. T07").strip().upper()
    if ara:
        s = s[s["trafo_no"].str.contains(ara, regex=False)]
    if s.empty:
        st.info("Bu süzgeçle trafo yok.")
        return
    st.caption(f"{tr(len(s))} trafo gösteriliyor. Bir satıra tıkla, trafonun kimlik kartı aşağıda açılır. "
               "Sütun başlığının üstünde durunca katmanı yazar.")
    # Anahtar süzgeçle değişir: süzgeç değişince eski satır numarası yanlış trafoyu seçmesin
    anahtar = "|".join(map(str, (kisa_yol(klasorler[0].parent), tek.name if tek else "hepsi",
                                 len(s), s["sehir"].iloc[0], s["trafo_no"].iloc[0], s["trafo_no"].iloc[-1])))
    olay = st.dataframe(
        tablo_gorunumu(s, tek is None), hide_index=True, width="stretch", height=360,
        column_config=SUTUN_AYARI, on_select="rerun", selection_mode="single-row",
        key=f"tablo-{hash(anahtar)}",
    )
    secim = [i for i in olay.selection.rows if i < len(s)]
    satir = s.iloc[secim[0]] if secim else s.iloc[0]
    if not secim:
        st.caption("Seçim yok: ilk satır gösteriliyor.")
    st.divider()
    klasor = next(k for k in klasorler if sehir_no(k) == int(satir["sehir"]))
    trafo_karti(satir, t[t["sehir"] == satir["sehir"]], klasor)


def renk_basligi(r, cumleler):
    renk = r["renk"]
    st.markdown(f"<div class='buyuk'><span style='color:{RENK_HEX[renk]}'>●</span> {RENK_BUYUK[renk]}</div>",
                unsafe_allow_html=True)
    st.markdown(f"**{cumleler.get(renk, VARSAYILAN_RENK_CUMLE[renk])}**")


def kural_cumlesi(r):
    """%40 kuralı aday evle kesilir ve aralığımızla kıyaslanır (civan.md KARAR 20:56; app/harita.py ile aynı dil)."""
    aday, kural = int(r["aday"]), int(r["kural40_ev"])
    karamsar, iyimser = int(r["kac_ev_karamsar"]), int(r["kac_ev_iyimser"])
    if kural > aday:
        metin = f"Bugünkü kural panelsiz {aday} evin hepsine izin veriyor ({kural} evlik yer)"
    else:
        metin = f"Bugünkü kural (%40): {kural} ev"
    gosterilen = min(kural, aday)
    if gosterilen > iyimser and iyimser == 0:
        return f":red[**{metin}**, yer olmayan trafoya \"yer var\" diyor]"
    if gosterilen > iyimser:
        return f":red[**{metin}**, aralığımızın üstünde; fazlası sınırı aşabilir]"
    if gosterilen < karamsar:
        return f":blue[**{metin}**, aralığımızın altında; bekletmeye gerek olmayan başvuruları bekletiyor]"
    return f"{metin}, aralığımızın içinde"


def trafo_karti(r, sehir_t, klasor):
    """Seçilen trafonun bütün verisi: kimlik (Kıb-Tek'in bildiği), panel katmanı, yük haritası, eğri, konum."""
    ayar = json_oku(klasor / "ayar.json") or {}
    st.markdown(f"### Trafo {r['trafo_no']} · şehir {int(r['sehir'])}")
    st.caption(etiket(int(r["sehir"]), ayar) + " · trafo yeri gerçek değil")
    k1, k2, k3 = st.columns(3)
    with k1:
        with st.container(border=True):
            st.markdown("**Kimlik** · Kıb-Tek'in bildiği")
            aboneler = ", ".join(f"{ad} {int(r[c])}" for c, ad in ABONE_ADI.items() if c in r and r[c] > 0)
            bilgi_tablosu([
                ("Trafo gücü", f"{tr(r['kva'])} kVA"),
                ("Montaj", r["montaj"]),
                ("Bölge", BOLGE_ADI.get(r["bolge"], r["bolge"])),
                ("Konum", f"{r['enlem']:.5f}, {r['boylam']:.5f}"),
                ("Merkeze göre", f"{tr(r['x_m'])} m doğu, {tr(r['y_m'])} m kuzey"),
                ("Hat", f"{int(r['hat_sayisi'])} hat, en uzunu {tr(r['hat_boyu_max_m'])} m, toplam {tr(r['hat_boyu_toplam_m'])} m"),
                ("Kablo", r["kablo"]),
                ("Abone", f"{tr(r['abone_toplam'])} ({aboneler})" if aboneler else tr(r["abone_toplam"])),
                ("Panelli abone", f"{int(r['panel_sayisi'])}, toplam {tr(r['panel_kw'], 1)} kW"),
                ("Panelsiz konut", tr(r["aday"])),
                ("Yıllık tüketim", f"{tr(r['yillik_tuketim_mwh'], 1)} MWh" if pd.notna(r.get("yillik_tuketim_mwh")) else "—"),
            ])
    with k2:
        with st.container(border=True):
            st.markdown("**Panel katmanı** · bahar öğleni")
            if "renk" in r and pd.notna(r["renk"]):
                icerik = json_oku(ICERIK_DOSYASI) or {}
                renk_basligi(r, icerik.get("renk_cumleleri", {}))
                if r["aday"] <= 0:
                    st.markdown("Kaç ev daha panel takabilir: **panelsiz konut yok**")
                else:
                    orta = r.get("kac_ev_orta")
                    ara = aralik(r["kac_ev_karamsar"], r["kac_ev_iyimser"])
                    if pd.notna(orta):
                        parantez = "" if "–" not in ara else f" ({ara})"
                        st.markdown(f"Kaç ev daha panel takabilir: **yaklaşık {int(orta)} ev**{parantez}")
                    else:
                        st.markdown(f"Kaç ev daha panel takabilir: **{ara} ev**")
                    st.caption("%80 ihtimalle")
                    st.markdown(kural_cumlesi(r))
            else:
                st.info("Kaç ev tablosu yok.")
            satirlar = []
            if "p_bugun_asar" in r:
                satirlar += [("Bugün sınırı aşma olasılığı", yuzde(r["p_bugun_asar"])),
                             ("İlk 2 başvurunun sığma olasılığı", yuzde(r["p_iki_ev_sigar"], 1))]
            if "pv_uc" in r and pd.notna(r["pv_uc"]):
                satirlar.append(("Güvenli uç", PV_UC_ADI.get(r["pv_uc"], r["pv_uc"])))
            if "sinir_karamsar" in r:
                satirlar += [("Sınırı belirleyen", SINIR_ADI.get(r["sinir_karamsar"], r["sinir_karamsar"])),
                             ("Isıl pay", f"{tr(r['isil_pay_kw'], 1)} kW"),
                             ("Gerilim payı", aralik(r["gerilim_pay_kw_karamsar"], r["gerilim_pay_kw_iyimser"], 1, " kW"))]
            if "ogle_min_kw" in r and pd.notna(r.get("ogle_min_kw")):
                satirlar.append(("Öğlen en düşük yük", f"{tr(r['ogle_min_kw'], 1)} kW "
                                 f"(aralık {aralik(r['ogle_min_kw_p10'], r['ogle_min_kw_p90'], 1)})"))
                if r["olculdu"] == 1:
                    satirlar.append(("Ölçülen", f"{tr(r['ogle_min_kw_olculen'], 1)} kW"))
                satirlar += [("Ölçüm", "ölçüldü" if r["olculdu"] == 1 else "ölçülmedi"),
                             ("Güven", GUVEN_ADI.get(r["guven"], r["guven"]))]
                ark = csv_oku(klasor / "arketipler.csv")
                if ark is not None:
                    ad = ark.loc[ark["arketip"] == r["arketip"], "arketip_adi"]
                    if not ad.empty:
                        satirlar.append(("Günlük eğri tipi", f"{ad.iloc[0].replace('_', ' ')} "
                                         f"(olasılık {yuzde(r['arketip_olasilik'])})"))
            bilgi_tablosu(satirlar)
    with k3:
        with st.container(border=True):
            st.markdown("**Yük haritası** · yılın tepesi, ön sürüm")
            if "doluluk" in r and pd.notna(r.get("doluluk")):
                st.markdown(f"<div class='buyuk'>{yuzde(r['doluluk'])} dolu</div>", unsafe_allow_html=True)
                st.caption(f"Orta tahmin. Temkinli uçta {yuzde(r['doluluk_temkinli'])}.")
                saat = r["tepe_saati"]
                if isinstance(r.get("tepe_saati_2"), str) and r["tepe_saati_2"]:
                    saat += f", ikinci aday {r['tepe_saati_2']}"
                satirlar = [
                    ("Yılın tepesi", f"{tr(r['tepe_kw'], 1)} kW (aralık {aralik(r['tepe_kw_p10'], r['tepe_kw_p90'], 1)})"),
                    ("Görünür güç", f"{tr(r['tepe_kva'], 1)} kVA (aralık {aralik(r['tepe_kva_p10'], r['tepe_kva_p90'], 1)})"),
                    ("Yük için boş", f"{tr(r['bos_kva_p10'], 1)} kVA (temkinli)"),
                    ("Tepe saati", saat),
                    ("Tepe dönemi", DONEM_ADI.get(r.get("tepe_donemi"), r.get("tepe_donemi"))),
                    ("Tepe ayı", AY_ADI.get(int(r["tepe_ayi"]), r["tepe_ayi"]) if pd.notna(r.get("tepe_ayi")) else "—"),
                ]
                if "v_min_tepe_v" in r and pd.notna(r.get("v_min_tepe_v")):
                    yeterli = r["v_min_tepe_v_p10"] >= V_AKSAM_SINIR
                    satirlar += [
                        ("Akşam en düşük gerilim", f"{tr(r['v_min_tepe_v'], 1)} V (aralık "
                         f"{aralik(r['v_min_tepe_v_p10'], r['v_min_tepe_v_p90'], 1)})"),
                        ("Akşam gerilimi", "yeterli (alt uç ≥ 207 V)" if yeterli else "önce bak (alt uç < 207 V)"),
                        ("207 V altına inme payı", yuzde(r["p_aksam_207"], 1)),
                    ]
                kor = "; ".join(KOR_NOKTA_ADI.get(p, p) for p in str(r.get("kor_nokta", "")).split(";") if p)
                satirlar += [
                    ("Sayının kaynağı", TEPE_KAYNAGI_ADI.get(r.get("tepe_kaynagi"), r.get("tepe_kaynagi"))),
                    ("Güç katsayısı varsayımı", tr(r["pf_varsayim"], 2) if pd.notna(r.get("pf_varsayim")) else "—"),
                    ("Kör nokta", kor),
                ]
                bilgi_tablosu(satirlar)
            else:
                st.info("Yılın tepesi tablosu (tepe.csv) yok.")
    sol, sag = st.columns([3, 2])
    with sol:
        gunluk_egri(klasor, sehir_t, r)
    with sag:
        kucuk_harita(sehir_t, r["trafo_no"])


def gunluk_egri(klasor, sehir_t, r):
    """Ölçülüde ölçülen tüketim (gün 0); ölçülmeyende arketip × öğlen tahmini ve %80 aralık (sözleşme §5)."""
    if "olculdu" not in sehir_t:
        st.info("Eğri yok: hangi trafonun ölçülü olduğu tahmin tablosu gelince belli olur.")
        return
    olculu = sehir_t.loc[sehir_t["olculdu"] == 1, "trafo_no"]
    yuk = olculu_yuk(klasor / "yuk_5dk.csv", olculu)
    if yuk is None or yuk.empty:
        st.info("Eğri yok: bu şehirde ölçülü trafonun yük satırı bulunamadı.")
        return
    gun_turu = yuk.loc[yuk["gun"] == 0, "gun_turu"].iloc[0]
    if r["olculdu"] == 1:
        g = yuk[(yuk["trafo_no"] == r["trafo_no"]) & (yuk["gun"] == 0)].sort_values("adim")
        df = pd.DataFrame({"dakika": g["adim"].to_numpy() * 5, "deger": g["tuketim_kw"].to_numpy()})
        baslik, bantli = "Ölçülen tüketim", False
    else:
        ark = csv_oku(klasor / "arketipler.csv")
        if ark is None:
            st.info("Eğri yok: arketipler.csv bulunamadı.")
            return
        a = ark[ark["arketip"] == r["arketip"]]
        ogle_min = a[a["adim"].isin(OGLE_ADIMLARI)]["oran"].min()
        egri = a[a["gun_turu"] == gun_turu].sort_values("adim")
        oran = egri["oran"].to_numpy() / ogle_min
        df = pd.DataFrame({
            "dakika": egri["adim"].to_numpy() * 5,
            "deger": oran * r["ogle_min_kw"],
            "p10": oran * r["ogle_min_kw_p10"],
            "p90": oran * r["ogle_min_kw_p90"],
        })
        baslik, bantli = "Tahmini tüketim · açık alan %80 aralık", True
    df["saat"] = df["dakika"].map(saat_metni)
    st.markdown(f"**{baslik}** · Nisan, gün 0, {GUN_TURU_ADI.get(gun_turu, gun_turu)}")
    egri_grafigi(df, bantli)
    st.caption("Panel katmanının girdisi: öğlen penceresinde (11:00–14:00) en düşük yük.")


def kucuk_harita(sehir_t, secili):
    st.markdown("**Konum** · şehirdeki bütün trafolar")
    v = sehir_t[["trafo_no", "enlem", "boylam", "kva"]].copy()
    renk = sehir_t["renk"] if "renk" in sehir_t else pd.Series([None] * len(sehir_t), index=sehir_t.index)
    v["rgba"] = renk.map(lambda x: RENK_RGBA.get(x, GRI_RGBA))
    v["renk_adi"] = renk.map(lambda x: RENK_ADI.get(x, "renk yok"))
    v["yaricap"] = 70
    nokta = pdk.Layer("ScatterplotLayer", id="trafolar", data=v, get_position=["boylam", "enlem"],
                      get_fill_color="rgba", get_radius="yaricap", radius_min_pixels=4,
                      stroked=True, get_line_color=[255, 255, 255, 220], line_width_min_pixels=1, pickable=True)
    halka = pdk.Layer("ScatterplotLayer", id="secili", data=v[v["trafo_no"] == secili],
                      get_position=["boylam", "enlem"], get_radius=220, radius_min_pixels=10, filled=False,
                      stroked=True, get_line_color=[42, 120, 214, 255], line_width_min_pixels=3)
    # Bütün şehir sığsın: en geniş açıklığa göre yakınlık (Web Mercator, ~280 px yükseklik)
    acik = max(v["enlem"].max() - v["enlem"].min(), v["boylam"].max() - v["boylam"].min(), 0.005)
    yakinlik = min(14.0, math.log2(280 * 360 / (256 * acik * 1.25)))
    gorunum = pdk.ViewState(latitude=(v["enlem"].max() + v["enlem"].min()) / 2,
                            longitude=(v["boylam"].max() + v["boylam"].min()) / 2, zoom=yakinlik)
    st.pydeck_chart(pdk.Deck(layers=[nokta, halka], initial_view_state=gorunum, map_style=None,
                             tooltip={"text": "{trafo_no} · {renk_adi} · {kva} kVA"}), height=280)
    st.caption("Mavi halka seçili trafo. Renk panel katmanının. Yerler farazi, gerçek trafo yeri değil.")


# ---------- şehirler ----------

def sehirler_sekmesi(t_hepsi, klasorler):
    if len(klasorler) < 2:
        st.info("Bu veri setinde tek şehir var.")
    satirlar = []
    for k in klasorler:
        no = sehir_no(k)
        s = t_hepsi[t_hepsi["sehir"] == no]
        ayar = json_oku(k / "ayar.json") or {}
        satir = {"Şehir": no, "Trafo": len(s)}
        if "olculdu" in s:
            satir["Ölçülü"] = int(s["olculdu"].sum())
        if "renk" in s:
            for r in RENK_SIRA:
                satir[RENK_ADI[r].capitalize()] = int((s["renk"] == r).sum())
            if "pv_uc" in s:
                satir["Büyük olasılıkla dolu"] = int((s["pv_uc"] == "dolu_bayrak").sum())
            if "kac_ev_orta" in s:
                satir["Kaç ev (yaklaşık)"] = int(s["kac_ev_orta"].sum())
            satir["Kaç ev aralığı"] = aralik(s["kac_ev_karamsar"].sum(), s["kac_ev_iyimser"].sum())
            satir["%40 kuralı (ev)"] = int(s["kural_gosterilen"].sum())
        if "doluluk" in s:
            satir["Ortanca doluluk"] = s["doluluk"].median() * 100
            satir["%80'den dolu olabilir"] = int((s["doluluk_temkinli"] >= DOLU_ESIK).sum())
            if "v_min_tepe_v_p10" in s:
                satir["Akşam: önce bak"] = int((s["v_min_tepe_v_p10"] < V_AKSAM_SINIR).sum())
        satir["Üretici"] = str(ayar.get("uretici_surumu", "—"))
        satir["Hava yılı"] = str(ayar.get("hava_yili", "—"))
        satirlar.append(satir)
    df = pd.DataFrame(satirlar)
    st.caption("Her satır bir şehir. Renkler, kaç ev ve %40 kuralı panel katmanının; doluluk ve akşam gerilimi yük haritasının.")
    st.dataframe(df, hide_index=True, width="stretch", column_config={
        "Ortanca doluluk": st.column_config.NumberColumn(format="%%%.0f", help="Yük haritası"),
        "Kaç ev (yaklaşık)": st.column_config.NumberColumn(help="Panel katmanı, şehir toplamı"),
    })
    if "renk" in t_hepsi:
        st.markdown("**Şehir şehir trafo renkleri** · panel katmanı")
        satir_html = []
        for k in klasorler:
            s = t_hepsi[t_hepsi["sehir"] == sehir_no(k)]
            sayim = s["renk"].value_counts()
            parcalar = [(RENK_ADI[r], int(sayim.get(r, 0)), RENK_HEX[r]) for r in RENK_SIRA]
            ozet = " / ".join(str(p[1]) for p in parcalar)
            satir_html.append(f"<div class='sehir-satir'><span>{e(k.name)}</span>{yigin_html(parcalar)}"
                              f"<span class='soluk'>{ozet}</span></div>")
        lejant = " ".join(f"<span class='nokta' style='color:{RENK_HEX[r]}'>●</span> {RENK_ADI[r]}" for r in RENK_SIRA)
        st.markdown(f"<div class='lejant'>{lejant} <span class='soluk'>· sağdaki sayılar yeşil / sarı / kırmızı</span></div>"
                    + "".join(satir_html), unsafe_allow_html=True)


# ---------- model ne kadar iyi ----------

def rakam_karti(r, depo):
    etiket_, isaret, renk = DURUM.get(r.get("durum"), DURUM["bilgi"])
    kaynak = r.get("kaynak")
    baglanti = (f" · <a href='{e(depo)}/blob/main/{e(kaynak)}' target='_blank'>kaynak ↗</a>" if kaynak else "")
    with st.container(border=True):
        st.markdown(
            f"<span class='rozet' style='border-color:{renk}'><span style='color:{renk}'>{isaret}</span> {etiket_}</span>"
            f"<span class='soluk'>{e(VERI_TURU.get(r.get('veri'), r.get('veri', '')))}</span>"
            f"<div class='rakam'>{e(r.get('deger', ''))}</div>"
            f"<div class='rakam-baslik'>{e(r.get('baslik', ''))}</div>"
            f"<div>{e(r.get('aciklama', ''))}</div>"
            f"<div class='soluk' style='margin-top:.45rem'>{e(r.get('kapsam', ''))}{baglanti}</div>",
            unsafe_allow_html=True,
        )


def model_sekmesi(icerik):
    rakamlar = icerik.get("rakamlar", [])
    depo = icerik.get("kimlik", {}).get("depo", DEPO_VARSAYILAN).rstrip("/")
    st.caption(f"{icerik.get('rakam_notu', '')} Güncellendi: {icerik.get('guncellendi', '—')}. "
               "Bu rakamlar dashboard/icerik.json dosyasından gelir; yeni sonuçta yalnız o dosya değişir.")
    if not rakamlar:
        st.info("dashboard/icerik.json'da rakam yok.")
        return
    lejant = " ".join(
        f"<span class='rozet' style='border-color:{renk}'><span style='color:{renk}'>{isaret}</span> {ad}</span>"
        for ad, isaret, renk in DURUM.values()
    )
    st.markdown(f"<div style='margin:.2rem 0 .6rem'>{lejant}</div>", unsafe_allow_html=True)
    for anahtar, ad, alt_baslik in KATMANLAR:
        grup = [r for r in rakamlar if r.get("katman") == anahtar]
        if not grup:
            continue
        st.subheader(ad)
        st.caption(alt_baslik)
        for bas in range(0, len(grup), 3):
            kolonlar = st.columns(3)
            for kolon, r in zip(kolonlar, grup[bas:bas + 3]):
                with kolon:
                    rakam_karti(r, depo)


# ---------- proje ----------

def kaynak_tablosu():
    satirlar = []
    for kaynak in sorted(HAM_KOK.glob("*/KAYNAK.txt")):
        metin = kaynak.read_text(encoding="utf-8").splitlines()
        ilk = next((s.strip() for s in metin if s.strip()), "")
        lisans = next((s.split(":", 1)[1].strip() for s in metin if s.lower().startswith("lisans") and ":" in s), "")
        yerel = any(p.name != "KAYNAK.txt" and not p.name.startswith(".") for p in kaynak.parent.iterdir())
        satirlar.append({
            "Klasör": kaynak.parent.name,
            "Bu bilgisayarda": "var" if yerel else "yok",
            "Ne": ilk,
            "Lisans": lisans or "—",
        })
    return pd.DataFrame(satirlar)


def proje_sekmesi(icerik):
    k = icerik.get("kimlik", {})
    cumleler = {**VARSAYILAN_RENK_CUMLE, **icerik.get("renk_cumleleri", {})}
    sol, sag = st.columns([3, 2])
    with sol:
        st.subheader("Ne yapıyor")
        for baslik, anahtar in (("Sorun", "sorun"), ("Kullanıcı", "kullanici"), ("Yöntem", "yontem"), ("Karar", "karar")):
            if k.get(anahtar):
                st.markdown(f"**{baslik}.** {k[anahtar]}")
        st.markdown("**Panel katmanında üç renk**")
        st.markdown("<div class='lejant'>" + "<br>".join(
            f"<span class='nokta' style='color:{RENK_HEX[r]}'>●</span> <b>{RENK_ADI[r]}</b>: {e(cumleler[r])}"
            for r in RENK_SIRA) + "</div>", unsafe_allow_html=True)
        if k.get("iki_soru"):
            st.markdown("**İki ayrı soru, birbirinden bağımsız**")
            for s in k["iki_soru"]:
                katman = "Yük haritası" if s.get("katman") == "yuk" else "Panel katmanı"
                st.markdown(f"- **{katman}: {s.get('soru', '')}** {s.get('an', '')}. Sınır: {s.get('sinir', '')}.")
            st.caption("Panel akşam tepesini düşürmez: tepe gün battıktan sonra, batarya yok.")
    with sag:
        st.subheader("Kim")
        bilgi_tablosu([
            ("Takım", k.get("takim", "—")),
            *[(u.get("ad", ""), u.get("rol", "")) for u in k.get("uyeler", [])],
            ("Etkinlik", k.get("etkinlik", "—")),
            ("Düzenleyen", k.get("duzenleyen", "—")),
            ("Tarih", k.get("tarih", "—")),
            ("Yer", k.get("yer", "—")),
            ("Kategori", k.get("kategori", "—")),
            ("Depo", k.get("depo", DEPO_VARSAYILAN)),
        ])
        with st.expander("Sözlük: terimler sade dille", expanded=False):
            for s in icerik.get("sozluk", []):
                st.markdown(f"**{s.get('terim', '')}.** {s.get('anlam', '')}")
    st.subheader("Veri kaynakları")
    df = kaynak_tablosu()
    if df.empty:
        st.info("data/raw altında KAYNAK.txt bulunamadı.")
    else:
        st.caption("Her satır depodaki bir KAYNAK.txt dosyasının ilk satırı. Ham dosyalar depoda değil; "
                   "\"bu bilgisayarda\" sütunu indirilip indirilmediğini gösterir.")
        st.dataframe(df, hide_index=True, width="stretch", column_config={
            "Klasör": st.column_config.TextColumn(width="small"),
            "Bu bilgisayarda": st.column_config.TextColumn(width="small"),
            "Ne": st.column_config.TextColumn(width="large"),
            "Lisans": st.column_config.TextColumn(width="medium"),
        })


# ---------- ham veri ----------

def ham_veri_sekmesi(klasorler, tek):
    mevcut = [(ad, acik) for ad, acik in DOSYALAR if any((k / ad).exists() for k in klasorler)]
    secim = st.selectbox("Dosya", mevcut, format_func=lambda x: f"{x[0]} · {x[1]}")
    ad = secim[0]
    if ad.endswith(".json"):
        hedef = [tek] if tek else klasorler
        for k in hedef:
            veri = json_oku(k / ad)
            if veri is not None:
                with st.expander(f"{k.name} / {ad}", expanded=len(hedef) == 1):
                    st.json(veri, expanded=1)
    elif ad == "yuk_5dk.csv":
        if tek is None:
            st.info("5 dakikalık yük büyük: önce soldan bir şehir seç.")
        else:
            tahmin = csv_oku(tek / "tahmin.csv")
            if tahmin is None:
                st.info("Hangi trafonun ölçülü olduğu tahmin tablosu gelince belli olur; o zamana kadar gösterilmez.")
            else:
                df = olculu_yuk(tek / ad, tahmin.loc[tahmin["olculdu"] == 1, "trafo_no"])
                tablo_goster(df, f"{tek.name}_{ad}")
    else:
        df = topla([tek] if tek else klasorler, ad)
        tablo_goster(df, f"{tek.name if tek else 'hepsi'}_{ad}")
    st.caption("cevap_anahtari.csv gösterilmez: benzetimin bildiği gerçek, yalnız sınav okur (sözleşme). "
               "Ölçülmeyen trafonun 5 dakikalık yükü de aynı sebeple gösterilmez.")


def tablo_goster(df, dosya_adi):
    if df is None:
        st.info("Bu şehirde dosya yok.")
        return
    st.caption(f"{tr(len(df))} satır, {len(df.columns)} sütun.")
    st.dataframe(df, hide_index=True, width="stretch", height=420)
    st.download_button("CSV olarak indir", df.to_csv(index=False).encode("utf-8"),
                       file_name=dosya_adi, mime="text/csv")


# ---------- sayfa ----------

def main():
    st.set_page_config(page_title="Trafo Görünürlük Haritası · Dashboard", page_icon="⚡", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    icerik = json_oku(ICERIK_DOSYASI) or {}
    kimlik_bandi(icerik.get("kimlik", {}))

    setler = veri_setleri()
    klasorler, tek = [], None
    st.sidebar.header("Veri")
    if setler:
        secili_set = st.sidebar.selectbox("Veri seti", setler, format_func=kisa_yol,
                                          help="data/synthetic ve altındaki şehir klasörü içeren klasörler.")
        klasorler = sehir_klasorleri(secili_set)
        secenek = st.sidebar.selectbox(
            "Şehir", ["hepsi"] + klasorler,
            format_func=lambda p: f"Bütün şehirler ({len(klasorler)})" if p == "hepsi" else p.name,
        )
        tek = None if secenek == "hepsi" else secenek
    st.sidebar.caption("Yeni veri: şehir klasörlerini data/synthetic altına ya da bir alt klasöre koy, sayfayı "
                       "yenile. Kod değişmez.")
    st.sidebar.caption("Kimlik, resmi rakamlar ve sözlük: dashboard/icerik.json.")
    st.sidebar.caption("Harita ayrı sayfa: streamlit run app/harita.py")

    t_hepsi = t = None
    if klasorler:
        t_hepsi = birlesik_tablo(tuple(klasorler))
        t = t_hepsi if tek is None else t_hepsi[t_hepsi["sehir"] == sehir_no(tek)]
        veri_bandi([tek] if tek else klasorler, t)

    sekmeler = st.tabs(["Özet", "Trafolar", "Şehirler", "Model ne kadar iyi", "Proje", "Ham veri"])
    with sekmeler[3]:
        model_sekmesi(icerik)
    with sekmeler[4]:
        proje_sekmesi(icerik)
    if not klasorler:
        for i in (0, 1, 2, 5):
            with sekmeler[i]:
                st.info(f"Şehir verisi yok ({kisa_yol(VERI_KOK)}). Deneme şehri üretmek için:")
                st.code("python3 src/sehir_uret.py 1 10", language="bash")
        return
    with sekmeler[0]:
        ozet_sekmesi(t, icerik)
    with sekmeler[1]:
        trafolar_sekmesi(t, klasorler, tek)
    with sekmeler[2]:
        sehirler_sekmesi(t_hepsi, klasorler)
    with sekmeler[5]:
        ham_veri_sekmesi(klasorler, tek)


if __name__ == "__main__":
    main()
