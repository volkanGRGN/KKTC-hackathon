"""Trafo görünürlük haritası (Civan).

Tabloları docs/data/tablo-bicimi.md'ye göre okur. cevap_anahtari.csv
okunmaz; ölçülmeyen trafonun yuk_5dk.csv satırı da okunmaz (sözleşme).
Düzen: app/ui-brief.md (üst şerit, harita + lejant, yan panel, alt şerit).

Çalıştırma: streamlit run app/harita.py
"""

import json
import math
from pathlib import Path

import altair as alt
import pandas as pd
import pydeck as pdk
import streamlit as st

KOK = Path(__file__).resolve().parent.parent
VERI_KOK = KOK / "data" / "synthetic"
ANAHTAR = ["sehir", "trafo_no"]
SAHTE_SEHIR_ALT_SINIR = 900  # sözleşme: sahte şehir tohumu 900–999
GERCEK_VERI_SEHIRLERI = range(800, 900)  # sözleşme 1.2: gerçek ölçüm verisi (civan.md KARAR 15:12)

RENKLER = {
    "yesil": [46, 160, 67, 235],
    "sari": [240, 180, 30, 235],
    "kirmizi": [210, 50, 45, 235],
}
GRI = [150, 150, 150, 210]
RENK_ADI = {"yesil": "yeşil", "sari": "sarı", "kirmizi": "kırmızı"}
RENK_BUYUK = {"yesil": "YEŞİL", "sari": "SARI", "kirmizi": "KIRMIZI"}  # str.upper() "YEŞIL" yazar
RENK_ROZET = {"yesil": "green", "sari": "orange", "kirmizi": "red"}  # st.badge rengi
RENK_CUMLE = {  # yan panel 1. madde; vaat renkte, sayıda değil (civan.md KARAR 19:13, 20:56)
    "yesil": "İlk 2 başvuru güvenle sığar (≥ %98)",
    "sari": "Önce ölç",
    "kirmizi": "Ölç ya da güçlendir",
}
SINIR_ADI = {"gerilim": "gerilim", "isil": "ısıl (trafo gücü)"}

# Sütun boyu = trafo gücü (ui-brief §5, Civan'ın kararı: kaç ev çoğu gerçek trafoda 0, boy anlamını yitiriyor)
METRE_BASINA_KVA = 0.25  # 1000 kVA = 250 m
SUTUN_YARICAP_M = 35
OLCULU_UC_YARICAP_M = 13  # ölçülü trafonun beyaz ucu
OLCULU_UC_FAZLA_M = 30

# İnternetsiz zemin: OSM bina, yol ve kıyı (data/raw/osm-kasaba/KAYNAK.txt). Yoksa Streamlit'in
# internetten gelen zemin haritası kullanılır.
OSM_DOSYASI = KOK / "data" / "raw" / "osm-kasaba" / "girne_merkez.json"
KIYI_DOSYASI = KOK / "data" / "raw" / "osm-kasaba" / "girne_kiyi.json"
OSM_ATIF = "Zemin: © OpenStreetMap katkıcıları (ODbL)"
KAT_YUKSEKLIGI_M = 3  # kat bilgisi olmayan bina 1 kat sayılır [Yorum]
BINA_RENK = [72, 82, 100, 200]
YOL_RENK = [150, 158, 172, 190]
KIYI_RENK = [127, 184, 230, 230]
HARITA_YUKSEKLIK_PX = 620

OGLE_ADIMLARI = range(132, 168)  # 11:00–14:00, sözleşme "Öğlen penceresi"
GUN_TURU_ADI = {"isgunu": "iş günü", "tatil": "tatil"}
GUVEN_ADI = {"yuksek": "yüksek", "orta": "orta", "dusuk": "düşük"}

# Streamlit menüsü ve "Deploy" düğmesi gizli (.streamlit/config.toml depoya girmiyor; ui-brief §3)
GIZLE_CSS = """
<style>
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebarCollapsedControl"],
header[data-testid="stHeader"] {display: none;}
.block-container {padding-top: 1.2rem; padding-bottom: 0.6rem;}
</style>
"""


# ------------------------------------------------------------------ veri
def sehir_klasorleri():
    """trafolar.csv olan şehir klasörleri, ada göre sıralı."""
    if not VERI_KOK.exists():
        return []
    return sorted(p for p in VERI_KOK.iterdir() if (p / "trafolar.csv").exists())


def degisim_zamani(yol):
    """Önbellek anahtarı: dosya yeniden üretilince değişir, harita eski veriyi göstermez."""
    yol = Path(yol)
    return yol.stat().st_mtime_ns if yol.exists() else None


def tablo_oku(yol):
    """CSV'yi okur; dosya yoksa None (Faz 1'de tahmin ve kac_ev henüz olmaz)."""
    return _tablo_oku(yol, degisim_zamani(yol))


@st.cache_data(max_entries=64)
def _tablo_oku(yol, zaman):
    if zaman is None:
        return None
    return pd.read_csv(yol, encoding="utf-8", dtype={"trafo_no": str})


def birlesik_tablo(klasor):
    """trafolar + tahmin + kac_ev, (sehir, trafo_no) ile; eksik dosya atlanır."""
    tablo = tablo_oku(str(klasor / "trafolar.csv"))
    for ad in ("tahmin.csv", "kac_ev.csv"):
        ek = tablo_oku(str(klasor / ad))
        if ek is not None:
            tablo = tablo.merge(ek, on=ANAHTAR, how="left", validate="one_to_one")
    return tablo


def ayar_oku(klasor):
    """Şehrin ayar.json'u; yoksa boş sözlük."""
    yol = klasor / "ayar.json"
    if not yol.exists():
        return {}
    return json.loads(yol.read_text(encoding="utf-8"))


def etiket(sehir_no, ayar):
    if sehir_no >= SAHTE_SEHIR_ALT_SINIR:
        return "SAHTE VERİ — gösterim"
    if sehir_no in GERCEK_VERI_SEHIRLERI:
        kaynak = ayar.get("veri_kaynagi", "gerçek ölçüm verisi")
        return f"GERÇEK ÖLÇÜM — {kaynak} (Kıbrıs değil)"
    return "örnek veri (farazi şehir) — gösterim"


def etiket_rengi(sehir_no):
    if sehir_no >= SAHTE_SEHIR_ALT_SINIR:
        return "orange"
    if sehir_no in GERCEK_VERI_SEHIRLERI:
        return "blue"
    return "gray"


def aday_ev(satir):
    """Panelsiz konut abonesi; trafolar.csv'den (cevap anahtarı okunmaz)."""
    return int(satir["abone_konut"] - satir["panel_sayisi"])


def kural_gosterilen(tablo):
    """%40 kuralının ev sayısı aday evle kesilir (civan.md KARAR 20:56)."""
    aday = (tablo["abone_konut"] - tablo["panel_sayisi"]).clip(lower=0)
    return tablo["kural40_ev"].clip(upper=aday)


def aralik_metni(satir):
    """Tooltip ve özet için kısa 'yaklaşık N ev (A–B)'."""
    if aday_ev(satir) <= 0:
        return "panelsiz konut yok"
    karamsar, iyimser = int(satir["kac_ev_karamsar"]), int(satir["kac_ev_iyimser"])
    orta = satir.get("kac_ev_orta")
    if pd.notna(orta):
        return f"yaklaşık {int(orta)} ev" + ("" if karamsar == iyimser else f" ({karamsar}–{iyimser})")
    return f"{karamsar}–{iyimser} ev"


def sutun_verisi(tablo):
    """Harita için renk, yükseklik ve ipucu sütunları eklenmiş yeni tablo."""
    if "renk" in tablo:
        rgba = tablo["renk"].map(lambda r: RENKLER.get(r, GRI))
        ipucu = tablo.apply(lambda s: f"{s['trafo_no']} · {RENK_ADI.get(s['renk'], 'karar yok')} · "
                                      f"{aralik_metni(s)}", axis=1)
    else:
        rgba = pd.Series([GRI] * len(tablo), index=tablo.index)
        ipucu = tablo["trafo_no"] + " · karar yok"
    yukseklik = tablo["kva"] * METRE_BASINA_KVA
    return tablo.assign(rgba=rgba, yukseklik=yukseklik, ipucu=ipucu)


# ------------------------------------------------------------------ zemin
def kat_sayisi(etiketler):
    try:
        return max(1, int(etiketler.get("building:levels", 1)))
    except ValueError:
        return 1


def osm_zemin(yol, kiyi_yol):
    """OSM binaları (çokgen + yükseklik), yollar ve kıyı; bina dosyası yoksa None."""
    return _osm_zemin(yol, degisim_zamani(yol), kiyi_yol, degisim_zamani(kiyi_yol))


@st.cache_data(max_entries=4)
def _osm_zemin(yol, zaman, kiyi_yol, kiyi_zaman):
    if zaman is None:
        return None
    ogeler = json.loads(Path(yol).read_text(encoding="utf-8"))["elements"]
    binalar, yollar, kiyi = [], [], []
    for oge in ogeler:
        if oge["type"] != "way":  # tek relation kale suru, atlandı
            continue
        noktalar = [[n["lon"], n["lat"]] for n in oge["geometry"]]
        if "building" in oge["tags"]:
            yukseklik = kat_sayisi(oge["tags"]) * KAT_YUKSEKLIGI_M
            binalar.append({"cokgen": noktalar, "yukseklik": yukseklik})
        elif "highway" in oge["tags"]:
            yollar.append({"yol": noktalar})
    if kiyi_zaman is not None:
        for oge in json.loads(Path(kiyi_yol).read_text(encoding="utf-8"))["elements"]:
            if oge["type"] == "way" and "geometry" in oge:
                kiyi.append({"yol": [[n["lon"], n["lat"]] for n in oge["geometry"]]})
    return {"binalar": binalar, "yollar": yollar, "kiyi": kiyi}


def zemin_katmanlari(zemin):
    katmanlar = [
        pdk.Layer("PathLayer", id="yollar", data=zemin["yollar"], get_path="yol",
                  get_color=YOL_RENK, width_min_pixels=1, get_width=4),
        pdk.Layer("PolygonLayer", id="binalar", data=zemin["binalar"], get_polygon="cokgen",
                  get_elevation="yukseklik", extruded=True, get_fill_color=BINA_RENK),
    ]
    if zemin["kiyi"]:
        katmanlar.insert(0, pdk.Layer("PathLayer", id="kiyi", data=zemin["kiyi"], get_path="yol",
                                      get_color=KIYI_RENK, width_min_pixels=2, get_width=8))
    return katmanlar


# ------------------------------------------------------------------ harita
def trafo_katmanlari(veri):
    """Sütun görsel; tıklanan 'trafolar' yerde, ekranda en az 10 px (ince sütun uzaktan tıklanamıyor).
    secili_satir() 'trafolar' id'sine ve veri sırasına dayanır."""
    sutunlar = pdk.Layer(
        "ColumnLayer", id="sutunlar", data=veri, get_position=["boylam", "enlem"],
        get_elevation="yukseklik", get_fill_color="rgba", radius=SUTUN_YARICAP_M, pickable=False,
    )
    trafolar = pdk.Layer(
        "ScatterplotLayer", id="trafolar", data=veri, get_position=["boylam", "enlem"],
        get_fill_color="rgba", get_radius=SUTUN_YARICAP_M * 1.4, radius_min_pixels=10,
        stroked=True, get_line_color=[14, 17, 23, 255], line_width_min_pixels=1,
        pickable=True, auto_highlight=True, highlight_color=[255, 255, 255, 90],
    )
    if "olculdu" not in veri:
        return [sutunlar, trafolar]
    olculu = veri.loc[veri["olculdu"] == 1, ["boylam", "enlem", "yukseklik"]].assign(
        uc=lambda t: t["yukseklik"] + OLCULU_UC_FAZLA_M)
    uc = pdk.Layer(
        "ColumnLayer", id="olculu", data=olculu, get_position=["boylam", "enlem"],
        get_elevation="uc", get_fill_color=[245, 247, 250, 255], radius=OLCULU_UC_YARICAP_M,
        pickable=False,
    )
    return [sutunlar, trafolar, uc]


def acilis_gorunumu(veri, genislik_px=900, yukseklik_px=HARITA_YUKSEKLIK_PX):
    """Bütün trafoları kapsayan kamera (sınır kutusu), eğim 45°. Web Mercator: z'de piksel başına
    360 / (256 · 2^z) derece boylam; enlemde 1 / cos(enlem) kadar uzar."""
    b0, b1 = veri["boylam"].min(), veri["boylam"].max()
    e0, e1 = veri["enlem"].min(), veri["enlem"].max()
    orta_enlem = (e0 + e1) / 2
    z_boylam = math.log2(360 * genislik_px / (256 * max(b1 - b0, 1e-4)))
    z_enlem = math.log2(360 * yukseklik_px * math.cos(math.radians(orta_enlem)) / (256 * max(e1 - e0, 1e-4)))
    return pdk.ViewState(latitude=orta_enlem, longitude=(b0 + b1) / 2,
                         zoom=min(z_boylam, z_enlem) - 0.45, pitch=45)  # pay: eğimde uzak kenar


def harita(veri, zemin):
    katmanlar = trafo_katmanlari(veri)
    ipucu = {"text": "{ipucu}"}
    if zemin is None:
        return pdk.Deck(layers=katmanlar, initial_view_state=acilis_gorunumu(veri),
                        map_style=None, tooltip=ipucu)
    return pdk.Deck(
        layers=zemin_katmanlari(zemin) + katmanlar, initial_view_state=acilis_gorunumu(veri),
        map_provider=None,  # internet zemini kapalı; zemin OSM dosyasından
        tooltip=ipucu,
    )


def lejant(veri, zemin):
    with st.container(horizontal=True, vertical_alignment="center", gap="small"):
        if "renk" in veri:
            for r in RENKLER:
                st.badge(RENK_ADI[r], color=RENK_ROZET[r], icon=":material/circle:")
        else:
            st.badge("karar yok (kaç ev tablosu henüz yok)", color="gray")
        st.caption("Sütun boyu = trafo gücü · beyaz uç = ölçüm cihazı var")
        if zemin is not None:
            st.caption(OSM_ATIF)


# ------------------------------------------------------------------ özetler
def sehir_ozeti(veri):
    """Alt şerit ve boş panel için sayılar."""
    oz = {"trafo": len(veri)}
    if "olculdu" in veri:
        oz["olculen"] = int((veri["olculdu"] == 1).sum())
    if "renk" in veri:
        oz["renk"] = {r: int((veri["renk"] == r).sum()) for r in RENKLER}
        oz["kural_fazla"] = int((kural_gosterilen(veri) > veri["kac_ev_iyimser"]).sum())
    return oz


def alt_serit(oz):
    parcalar = [f"{oz['trafo']} trafo"]
    if "olculen" in oz:
        parcalar.append(f"{oz['olculen']} ölçüldü, {oz['trafo'] - oz['olculen']} tahmin")
    if "renk" in oz:
        parcalar.append(" · ".join(f"{RENK_ADI[r]} {n}" for r, n in oz["renk"].items()))
        parcalar.append(f"%40 kuralı {oz['kural_fazla']} trafoda bizim en iyimser tahminimizden fazla söz veriyor"
                        if oz["kural_fazla"] else "%40 kuralı hiçbir trafoda en iyimser tahminimizi aşmıyor")
    st.caption(" · ".join(parcalar))


def bos_panel(oz):
    st.subheader("Şehrin özeti")
    with st.container(horizontal=True):
        st.metric("Trafo", oz["trafo"])
        if "olculen" in oz:
            st.metric("Ölçülen", oz["olculen"])
            st.metric("Tahmin edilen", oz["trafo"] - oz["olculen"])
    if "renk" in oz:
        with st.container(horizontal=True):
            for r, n in oz["renk"].items():
                st.metric(RENK_ADI[r].capitalize(), n)
        if oz["kural_fazla"]:
            st.warning(f"{oz['kural_fazla']} trafoda bugünkü %40 kuralı bizim en iyimser tahminimizden "
                       "fazla ev söz veriyor.", title="Bugünkü kural")
    st.info("Bir direğe (sütuna) tıkla: o trafonun kararı, kaç ev daha panel takabileceği ve gün boyu yükü.",
            icon=":material/touch_app:")


# ------------------------------------------------------------------ eğri
def olculu_yuk(yol, olculu_nolar):
    """yuk_5dk.csv'den YALNIZ ölçülü trafoların satırları (ölçülmeyenin satırı cevap anahtarıdır)."""
    return _olculu_yuk(yol, olculu_nolar, degisim_zamani(yol))


@st.cache_data(max_entries=16)
def _olculu_yuk(yol, olculu_nolar, zaman):
    sutunlar = ["trafo_no", "gun", "gun_turu", "adim", "saat", "tuketim_kw"]
    parcalar = pd.read_csv(
        yol, encoding="utf-8", usecols=sutunlar, dtype={"trafo_no": str}, chunksize=50_000
    )
    return pd.concat(p[p["trafo_no"].isin(olculu_nolar)] for p in parcalar)


def saat_ekseni(adimlar):
    return [f"{a // 12:02d}:{a % 12 * 5:02d}" for a in adimlar]


def olculen_egri(yuk, trafo_no):
    """Ölçülü trafonun gün 0 tüketimi; dönüş (tablo, gün türü)."""
    gun0 = yuk[(yuk["trafo_no"] == trafo_no) & (yuk["gun"] == 0)].sort_values("adim")
    tablo = pd.DataFrame({"saat": gun0["saat"].to_numpy(), "kw": gun0["tuketim_kw"].to_numpy()})
    return tablo, gun0["gun_turu"].iloc[0]


def tahmini_egri(arketipler, satir, gun_turu):
    """Sözleşme §5: oran × (öğlen tahmini ÷ arketipin öğlen penceresindeki en düşük oranı)."""
    a = arketipler[arketipler["arketip"] == satir["arketip"]]
    ogle_min_oran = a[a["adim"].isin(OGLE_ADIMLARI)]["oran"].min()
    egri = a[a["gun_turu"] == gun_turu].sort_values("adim")
    oran = egri["oran"].to_numpy() / ogle_min_oran
    return pd.DataFrame({
        "saat": saat_ekseni(egri["adim"]),
        "kw": oran * satir["ogle_min_kw"],
        "alt": oran * satir["ogle_min_kw_p10"],
        "ust": oran * satir["ogle_min_kw_p90"],
    })


def egri_grafigi(tablo, bantli, aciklama):
    """Saat ekseni sıralı; bantlı ise %80 aralık gölgesi."""
    x = alt.X("saat:O", title=None, sort=None,
              axis=alt.Axis(values=["00:00", "06:00", "12:00", "18:00"], labelAngle=0))
    cizgi = alt.Chart(tablo).mark_line(color="#BFDFFF", strokeWidth=2.5).encode(
        x=x, y=alt.Y("kw:Q", title="kW"), tooltip=["saat", alt.Tooltip("kw:Q", format=".1f")])
    grafik = cizgi
    if bantli:
        bant = alt.Chart(tablo).mark_area(color="#BFDFFF", opacity=0.22).encode(x=x, y="alt:Q", y2="ust:Q")
        grafik = bant + cizgi
    st.altair_chart(grafik.properties(height=200), alt=aciklama)


def egri_ciz(klasor, veri, satir):
    """Ölçülüde ölçülen, ölçülmeyende arketipten tahmin; tahmin tablosu yoksa eğri yok."""
    if "olculdu" not in veri:
        st.info("Eğri yok: hangi trafonun ölçülü olduğu tahmin tablosu (Faz 2) gelince belli olur.")
        return
    olculu_nolar = tuple(veri.loc[veri["olculdu"] == 1, "trafo_no"])
    yuk = olculu_yuk(str(klasor / "yuk_5dk.csv"), olculu_nolar)
    if yuk.empty:
        st.info("Eğri yok: bu şehirde ölçülü trafonun yük satırı bulunamadı.")
        return
    gun_turu = yuk.loc[yuk["gun"] == 0, "gun_turu"].iloc[0]
    if satir["olculdu"] == 1:
        tablo, gun_turu = olculen_egri(yuk, satir["trafo_no"])
        baslik, bantli = "Bu trafonun gün boyu yükü (ölçülen)", False
    else:
        arketipler = tablo_oku(str(klasor / "arketipler.csv"))
        if arketipler is None:
            st.info("Eğri yok: arketipler.csv bulunamadı.")
            return
        tablo = tahmini_egri(arketipler, satir, gun_turu)
        baslik, bantli = "Bu trafonun gün boyu yükü (tahmin, %80 aralık)", True
    st.markdown(f"**{baslik}**")
    st.caption(f"Gün 0, {GUN_TURU_ADI.get(gun_turu, gun_turu)}")
    egri_grafigi(tablo, bantli, baslik)


# ------------------------------------------------------------------ yan panel
def renk_basligi(satir):
    """Kart 1. madde: renk ve tek cümle, panelin en üstünde."""
    renk = satir["renk"]
    st.badge(RENK_BUYUK[renk], color=RENK_ROZET[renk], icon=":material/circle:")
    st.markdown(f"#### {RENK_CUMLE[renk]}")


def kural_etiketi(kural, aday):
    """%40 kuralının ev sayısı aday evle kesilir (civan.md KARAR 20:56)."""
    if kural > aday:
        return f"Bugünkü kural panelsiz {aday} evin hepsine izin veriyor ({kural} evlik yer)"
    return f"Bugünkü kural (%40): {kural} ev"


def kac_ev_metni(satir):
    """Kart 2. madde: bizim aralık büyük; %40 kuralı yanında, farklıysa vurgulu kutu."""
    aday = aday_ev(satir)
    kural = int(satir["kural40_ev"])
    if aday <= 0:
        st.metric("Kaç ev daha panel takabilir", "panelsiz konut yok")
        st.caption(f"Bugünkü kural (%40): {kural} evlik yer")
        return
    karamsar, iyimser = int(satir["kac_ev_karamsar"]), int(satir["kac_ev_iyimser"])
    aralik = f"{karamsar}" if karamsar == iyimser else f"{karamsar}–{iyimser}"
    orta = satir.get("kac_ev_orta")
    if pd.notna(orta):  # sözleşme 1.3; yoksa yalnız aralık (KARAR 19:13)
        st.metric("Kaç ev daha panel takabilir", f"yaklaşık {int(orta)} ev")
        st.caption(f"%80 ihtimalle {aralik} ev")
    else:
        st.metric("Kaç ev daha panel takabilir", f"{aralik} ev")
        st.caption("%80 ihtimalle")
    gosterilen = min(kural, aday)
    metin = kural_etiketi(kural, aday)
    if gosterilen > iyimser and iyimser == 0:
        st.error(f"{metin}: kural, yer olmayan trafoya \"yer var\" diyor.", title="Kural fazla söz veriyor")
    elif gosterilen > iyimser:
        st.error(f"{metin}: aralığımızın üstünde; fazlası sınırı aşabilir.", title="Kural fazla söz veriyor")
    elif gosterilen < karamsar:
        st.info(f"{metin}: aralığımızın altında; kural bekletmeye gerek olmayan başvuruları bekletiyor.",
                title="Kural gereksiz bekletiyor")
    else:
        st.caption(f"{metin} — aralığımızın içinde")


def yan_panel(klasor, veri, satir):
    st.subheader(f"Trafo {satir['trafo_no']}")
    if "renk" in veri:
        renk_basligi(satir)
        kac_ev_metni(satir)
    if "olculdu" in veri:
        with st.container(horizontal=True, gap="small"):
            if satir["olculdu"] == 1:
                st.badge("ölçüldü", color="blue", icon=":material/sensors:")
            else:
                st.badge("ölçülmedi, tahmin", color="gray", icon=":material/insights:")
            st.badge(f"güven {GUVEN_ADI.get(satir['guven'], satir['guven'])}", color="gray")
    egri_ciz(klasor, veri, satir)
    abone = int(satir.filter(like="abone_").sum())
    ayrinti = (f"Ayrıntı: {int(satir['kva'])} kVA · {satir['bolge']} · {satir['montaj']} · "
               f"{abone} abone · {int(satir['panel_sayisi'])} panel, {satir['panel_kw']:.1f} kW")
    if "sinir_karamsar" in veri:
        ayrinti += f" · sınırı belirleyen: {SINIR_ADI.get(satir['sinir_karamsar'], satir['sinir_karamsar'])}"
    if "olculdu" in veri:
        ayrinti += (f" · öğlen en düşük yük {satir['ogle_min_kw']:.1f} kW "
                    f"(%80 bant {satir['ogle_min_kw_p10']:.1f}–{satir['ogle_min_kw_p90']:.1f})")
    st.caption(ayrinti)


def secili_satir(durum, veri):
    """Haritada tıklanan trafo; seçim yoksa None."""
    indisler = durum.selection.indices.get("trafolar", [])
    return veri.iloc[indisler[0]] if indisler else None


# ------------------------------------------------------------------ sayfa
def main():
    st.set_page_config(page_title="Trafo haritası", layout="wide", initial_sidebar_state="collapsed")
    st.html(GIZLE_CSS)
    klasorler = sehir_klasorleri()
    if not klasorler:
        st.error("Şehir yok. Önce sahte şehirleri üret: python app/ornek_veri.py")
        return
    baslik, secim, rozet = st.columns([6, 2, 4], vertical_alignment="center")
    baslik.markdown("### Mahalle şebekesi haritası · Girne")
    secili = secim.selectbox("Şehir", klasorler, format_func=lambda p: p.name, label_visibility="collapsed")
    veri = sutun_verisi(birlesik_tablo(secili))
    sehir_no = int(veri["sehir"].iloc[0])
    with rozet.container(horizontal=True, horizontal_alignment="right"):
        st.badge(etiket(sehir_no, ayar_oku(secili)), color=etiket_rengi(sehir_no), icon=":material/info:")
    zemin = osm_zemin(str(OSM_DOSYASI), str(KIYI_DOSYASI))
    oz = sehir_ozeti(veri)
    sol, sag = st.columns([13, 7], gap="medium")
    with sol:
        durum = st.pydeck_chart(
            harita(veri, zemin), on_select="rerun", selection_mode="single-object",
            key=f"harita-{secili.name}", height=HARITA_YUKSEKLIK_PX,
            alt="Trafo haritası: her sütun bir trafo, renk karar, boy trafo gücü",
        )
        lejant(veri, zemin)
    with sag:
        with st.container(border=True, height=HARITA_YUKSEKLIK_PX + 40):
            satir = secili_satir(durum, veri)
            if satir is None:
                bos_panel(oz)
            else:
                yan_panel(secili, veri, satir)
    alt_serit(oz)


if __name__ == "__main__":
    main()
