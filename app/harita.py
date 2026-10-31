"""Trafo görünürlük haritası (Faz 1 iskeleti, Civan).

Tabloları docs/data/tablo-bicimi.md sürüm 1'e göre okur. cevap_anahtari.csv
okunmaz; ölçülmeyen trafonun yuk_5dk.csv satırı da okunmaz (sözleşme).

Çalıştırma: streamlit run app/harita.py
"""

from pathlib import Path

import pandas as pd
import pydeck as pdk
import streamlit as st

KOK = Path(__file__).resolve().parent.parent
VERI_KOK = KOK / "data" / "synthetic"
ANAHTAR = ["sehir", "trafo_no"]
SAHTE_SEHIR_ALT_SINIR = 900  # sözleşme: sahte şehir tohumu 900–999

RENKLER = {
    "yesil": [46, 160, 67, 230],
    "sari": [240, 180, 30, 230],
    "kirmizi": [210, 50, 45, 230],
}
GRI = [150, 150, 150, 200]
RENK_ADI = {"yesil": "yeşil", "sari": "sarı", "kirmizi": "kırmızı"}

METRE_BASINA_EV = 25  # sütun boyu çarpanı [Yorum]
EN_KISA_SUTUN_EV = 0.5  # 0 ev yine de görünsün
SUTUN_YARICAP_M = 35


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


def etiket(sehir_no):
    if sehir_no >= SAHTE_SEHIR_ALT_SINIR:
        return "SAHTE VERİ — gösterim"
    return "örnek veri (farazi şehir) — gösterim"


def sutun_verisi(tablo):
    """Harita için renk ve yükseklik sütunları eklenmiş yeni tablo."""
    if "renk" in tablo:
        rgba = tablo["renk"].map(lambda r: RENKLER.get(r, GRI))
    else:
        rgba = pd.Series([GRI] * len(tablo), index=tablo.index)
    if "kac_ev_karamsar" in tablo:
        ev = tablo["kac_ev_karamsar"].fillna(0)
    else:
        ev = tablo["kva"] / 10
    yukseklik = ev.clip(lower=EN_KISA_SUTUN_EV) * METRE_BASINA_EV
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


def harita(veri):
    gorunum = pdk.ViewState(
        latitude=veri["enlem"].mean(),
        longitude=veri["boylam"].mean(),
        zoom=13.5,
        pitch=45,
    )
    return pdk.Deck(
        layers=[harita_katmani(veri)],
        initial_view_state=gorunum,
        map_style=None,  # altlık yok: internetsiz açılsın
        tooltip={"text": "{trafo_no}"},
    )


def renk_ozeti(veri):
    if "renk" not in veri:
        return "Renk yok (kaç ev tablosu henüz yok): sütunlar gri, boy kVA ÷ 10."
    sayilar = veri["renk"].value_counts()
    parcalar = [f"{RENK_ADI[r]} {sayilar.get(r, 0)}" for r in RENKLER]
    return "Trafolar: " + " · ".join(parcalar) + " · sütun boyu: kaç ev (karamsar)"


def main():
    st.set_page_config(page_title="Trafo haritası", layout="wide")
    klasorler = sehir_klasorleri()
    if not klasorler:
        st.error("Şehir yok. Önce sahte şehirleri üret: python app/ornek_veri.py")
        return
    secili = st.sidebar.selectbox("Şehir", klasorler, format_func=lambda p: p.name)
    veri = sutun_verisi(birlesik_tablo(secili))
    st.warning(etiket(int(veri["sehir"].iloc[0])))
    st.caption(renk_ozeti(veri))
    st.pydeck_chart(harita(veri))


main()
