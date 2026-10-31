"""Trafo görünürlük haritası (Faz 1 iskeleti, Civan).

Tabloları docs/data/tablo-bicimi.md sürüm 1'e göre okur. cevap_anahtari.csv
okunmaz; ölçülmeyen trafonun yuk_5dk.csv satırı da okunmaz (sözleşme).

Çalıştırma: streamlit run app/harita.py
"""

import json
from pathlib import Path

import pandas as pd
import pydeck as pdk
import streamlit as st

KOK = Path(__file__).resolve().parent.parent
VERI_KOK = KOK / "data" / "synthetic"
ANAHTAR = ["sehir", "trafo_no"]
SAHTE_SEHIR_ALT_SINIR = 900  # sözleşme: sahte şehir tohumu 900–999
GERCEK_VERI_SEHIRLERI = range(800, 900)  # sözleşme 1.2: gerçek ölçüm verisi (civan.md KARAR 15:12)

RENKLER = {
    "yesil": [46, 160, 67, 230],
    "sari": [240, 180, 30, 230],
    "kirmizi": [210, 50, 45, 230],
}
GRI = [150, 150, 150, 200]
RENK_ADI = {"yesil": "yeşil", "sari": "sarı", "kirmizi": "kırmızı"}

METRE_BASINA_EV = 25  # sütun boyu çarpanı [Yorum]
EN_KISA_SUTUN_EV = 0.5  # 0 ev yine de görünsün
METRE_BASINA_KVA = 0.25  # kaç ev yokken boy: 1000 kVA = 250 m, renkli sütunlarla aynı ölçek
SUTUN_YARICAP_M = 35

# İnternetsiz zemin: OSM bina ve yolları (data/raw/osm-kasaba/KAYNAK.txt). Yoksa Streamlit'in
# internetten gelen zemin haritası kullanılır.
OSM_DOSYASI = KOK / "data" / "raw" / "osm-kasaba" / "girne_merkez.json"
OSM_ATIF = "Zemin: © OpenStreetMap katkıcıları (ODbL)"
KAT_YUKSEKLIGI_M = 3  # kat bilgisi olmayan bina 1 kat sayılır [Yorum]
BINA_RENK = [72, 82, 100, 210]
YOL_RENK = [105, 115, 135, 200]

OGLE_ADIMLARI = range(132, 168)  # 11:00–14:00, sözleşme "Öğlen penceresi"
GUN_TURU_ADI = {"isgunu": "iş günü", "tatil": "tatil"}
GUVEN_ADI = {"yuksek": "yüksek", "orta": "orta", "dusuk": "düşük"}


def sehir_klasorleri():
    """trafolar.csv olan şehir klasörleri, ada göre sıralı."""
    if not VERI_KOK.exists():
        return []
    return sorted(p for p in VERI_KOK.iterdir() if (p / "trafolar.csv").exists())


@st.cache_data
def tablo_oku(yol):
    """CSV'yi okur; dosya yoksa None (Faz 1'de tahmin ve kac_ev henüz olmaz)."""
    yol = Path(yol)
    if not yol.exists():
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


def sutun_verisi(tablo):
    """Harita için renk ve yükseklik sütunları eklenmiş yeni tablo."""
    if "renk" in tablo:
        rgba = tablo["renk"].map(lambda r: RENKLER.get(r, GRI))
    else:
        rgba = pd.Series([GRI] * len(tablo), index=tablo.index)
    if "kac_ev_karamsar" in tablo:
        ev = tablo["kac_ev_karamsar"].fillna(0)
        yukseklik = ev.clip(lower=EN_KISA_SUTUN_EV) * METRE_BASINA_EV
    else:
        yukseklik = tablo["kva"] * METRE_BASINA_KVA
    return tablo.assign(rgba=rgba, yukseklik=yukseklik)


def harita_katmani(veri):
    return pdk.Layer(
        "ColumnLayer",
        id="trafolar",
        data=veri,
        get_position=["boylam", "enlem"],
        get_elevation="yukseklik",
        get_fill_color="rgba",
        radius=SUTUN_YARICAP_M,
        pickable=True,
        auto_highlight=True,
    )


def kat_sayisi(etiketler):
    try:
        return max(1, int(etiketler.get("building:levels", 1)))
    except ValueError:
        return 1


@st.cache_data
def osm_zemin(yol):
    """OSM binaları (çokgen + yükseklik) ve yolları; dosya yoksa None."""
    yol = Path(yol)
    if not yol.exists():
        return None
    ogeler = json.loads(yol.read_text(encoding="utf-8"))["elements"]
    binalar, yollar = [], []
    for oge in ogeler:
        if oge["type"] != "way":  # tek relation kale suru, atlandı
            continue
        noktalar = [[n["lon"], n["lat"]] for n in oge["geometry"]]
        if "building" in oge["tags"]:
            yukseklik = kat_sayisi(oge["tags"]) * KAT_YUKSEKLIGI_M
            binalar.append({"cokgen": noktalar, "yukseklik": yukseklik})
        elif "highway" in oge["tags"]:
            yollar.append({"yol": noktalar})
    return {"binalar": binalar, "yollar": yollar}


def zemin_katmanlari(zemin):
    yollar = pdk.Layer(
        "PathLayer", id="yollar", data=zemin["yollar"], get_path="yol",
        get_color=YOL_RENK, width_min_pixels=1, get_width=4,
    )
    binalar = pdk.Layer(
        "PolygonLayer", id="binalar", data=zemin["binalar"], get_polygon="cokgen",
        get_elevation="yukseklik", extruded=True, get_fill_color=BINA_RENK,
    )
    return [yollar, binalar]


def harita(veri, zemin):
    gorunum = pdk.ViewState(
        latitude=veri["enlem"].mean(),
        longitude=veri["boylam"].mean(),
        zoom=13.5,
        pitch=45,
    )
    katmanlar = [harita_katmani(veri)]
    if zemin is None:
        return pdk.Deck(
            layers=katmanlar, initial_view_state=gorunum,
            map_style=None, tooltip={"text": "{trafo_no}"},
        )
    return pdk.Deck(
        layers=zemin_katmanlari(zemin) + katmanlar, initial_view_state=gorunum,
        map_provider=None,  # internet zemini kapalı; zemin OSM dosyasından
        tooltip={"text": "{trafo_no}"},
    )


def renk_ozeti(veri):
    if "renk" not in veri:
        return "Renk yok (kaç ev tablosu henüz yok): sütunlar gri, boy kVA ile orantılı."
    sayilar = veri["renk"].value_counts()
    parcalar = [f"{RENK_ADI[r]} {sayilar.get(r, 0)}" for r in RENKLER]
    return "Trafolar: " + " · ".join(parcalar) + " · sütun boyu: kaç ev (karamsar)"


@st.cache_data
def olculu_yuk(yol, olculu_nolar):
    """yuk_5dk.csv'den YALNIZ ölçülü trafoların satırları (ölçülmeyenin satırı cevap anahtarıdır)."""
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
    tablo = pd.DataFrame(
        {"ölçülen tüketim (kW)": gun0["tuketim_kw"].to_numpy()}, index=gun0["saat"]
    )
    return tablo, gun0["gun_turu"].iloc[0]


def tahmini_egri(arketipler, satir, gun_turu):
    """Sözleşme §5: oran × (öğlen tahmini ÷ arketipin öğlen penceresindeki en düşük oranı)."""
    a = arketipler[arketipler["arketip"] == satir["arketip"]]
    ogle_min_oran = a[a["adim"].isin(OGLE_ADIMLARI)]["oran"].min()
    egri = a[a["gun_turu"] == gun_turu].sort_values("adim")
    oran = egri["oran"].to_numpy() / ogle_min_oran
    return pd.DataFrame(
        {
            "tahmin (kW)": oran * satir["ogle_min_kw"],
            "P10 (kW)": oran * satir["ogle_min_kw_p10"],
            "P90 (kW)": oran * satir["ogle_min_kw_p90"],
        },
        index=saat_ekseni(egri["adim"]),
    )


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
        baslik = "Ölçülen tüketim"
    else:
        arketipler = tablo_oku(str(klasor / "arketipler.csv"))
        if arketipler is None:
            st.info("Eğri yok: arketipler.csv bulunamadı.")
            return
        tablo = tahmini_egri(arketipler, satir, gun_turu)
        baslik = "Tahmini tüketim, %80 bant (P10–P90)"
    st.markdown(f"**{baslik}** · gün 0, {GUN_TURU_ADI.get(gun_turu, gun_turu)}")
    st.line_chart(tablo, height=220)


def yan_panel(klasor, veri, satir):
    abone = int(satir.filter(like="abone_").sum())
    st.subheader(f"Trafo {satir['trafo_no']}")
    st.markdown(
        f"{int(satir['kva'])} kVA · {satir['bolge']} · {satir['montaj']}  \n"
        f"{abone} abone · {int(satir['panel_sayisi'])} panel, {satir['panel_kw']:.1f} kW"
    )
    if "olculdu" in veri:
        olcum = "ölçüldü" if satir["olculdu"] == 1 else "**ölçülmedi**"
        st.markdown(
            f"Öğlen en düşük yük: **{satir['ogle_min_kw']:.1f} kW** "
            f"(%80 bant {satir['ogle_min_kw_p10']:.1f}–{satir['ogle_min_kw_p90']:.1f})  \n"
            f"Güven: {GUVEN_ADI.get(satir['guven'], satir['guven'])} · {olcum}"
        )
    if "renk" in veri:
        st.markdown(
            f"Kaç ev daha panel: **{int(satir['kac_ev_karamsar'])}–"
            f"{int(satir['kac_ev_iyimser'])}** (karamsar–iyimser) · "
            f"{RENK_ADI[satir['renk']]}  \n"
            f"%40 kuralı: {int(satir['kural40_ev'])} ev"
        )
    egri_ciz(klasor, veri, satir)


def secili_satir(durum, veri):
    """Haritada tıklanan trafo; seçim yoksa None."""
    indisler = durum.selection.indices.get("trafolar", [])
    return veri.iloc[indisler[0]] if indisler else None


def main():
    st.set_page_config(page_title="Trafo haritası", layout="wide")
    klasorler = sehir_klasorleri()
    if not klasorler:
        st.error("Şehir yok. Önce sahte şehirleri üret: python app/ornek_veri.py")
        return
    secili = st.sidebar.selectbox("Şehir", klasorler, format_func=lambda p: p.name)
    veri = sutun_verisi(birlesik_tablo(secili))
    st.warning(etiket(int(veri["sehir"].iloc[0]), ayar_oku(secili)))
    st.caption(renk_ozeti(veri))
    zemin = osm_zemin(str(OSM_DOSYASI))
    sol, sag = st.columns([3, 2])
    with sol:
        durum = st.pydeck_chart(
            harita(veri, zemin), on_select="rerun", selection_mode="single-object",
            key=f"harita-{secili.name}",
        )
        if zemin is not None:
            st.caption(OSM_ATIF)
    with sag:
        satir = secili_satir(durum, veri)
        if satir is None:
            st.info("Bir trafoya (sütuna) tıkla.")
        else:
            yan_panel(secili, veri, satir)


if __name__ == "__main__":
    main()
