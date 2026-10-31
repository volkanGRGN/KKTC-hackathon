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
RENK_BUYUK = {"yesil": "YEŞİL", "sari": "SARI", "kirmizi": "KIRMIZI"}  # str.upper() "YEŞIL" yazar
RENK_ST = {"yesil": "green", "sari": "orange", "kirmizi": "red"}  # Streamlit metin rengi
RENK_CUMLE = {  # Faz 3 kartı, yan panel 1. madde
    "yesil": "En kötü durumda bile yer var",
    "sari": "Sınırda ya da emin değiliz, önce ölç",
    "kirmizi": "En kötü durumda yer yok",
}
SINIR_ADI = {"gerilim": "gerilim", "isil": "ısıl (trafo gücü)"}

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


def degisim_zamani(yol):
    """Önbellek anahtarı: dosya yeniden üretilince değişir, harita eski veriyi göstermez."""
    yol = Path(yol)
    return yol.stat().st_mtime_ns if yol.exists() else None


def tablo_oku(yol):
    """CSV'yi okur; dosya yoksa None (Faz 1'de tahmin ve kac_ev henüz olmaz)."""
    return _tablo_oku(yol, degisim_zamani(yol))


@st.cache_data
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


def osm_zemin(yol):
    """OSM binaları (çokgen + yükseklik) ve yolları; dosya yoksa None."""
    return _osm_zemin(yol, degisim_zamani(yol))


@st.cache_data
def _osm_zemin(yol, zaman):
    if zaman is None:
        return None
    ogeler = json.loads(Path(yol).read_text(encoding="utf-8"))["elements"]
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


def olculu_yuk(yol, olculu_nolar):
    """yuk_5dk.csv'den YALNIZ ölçülü trafoların satırları (ölçülmeyenin satırı cevap anahtarıdır)."""
    return _olculu_yuk(yol, olculu_nolar, degisim_zamani(yol))


@st.cache_data
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


def renk_basligi(satir):
    """Kart 1. madde: renk ve tek cümle, panelin en üstünde."""
    renk = satir["renk"]
    st.markdown(f"### :{RENK_ST[renk]}[● {RENK_BUYUK[renk]}]")
    st.markdown(f"**{RENK_CUMLE[renk]}**")


def kac_ev_metni(satir):
    """Kart 2. madde: bizim aralık ve %40 kuralı yan yana; farklıysa vurgulu."""
    # Aday: panelsiz konut abonesi; trafolar.csv'den (cevap anahtarı okunmaz).
    aday = int(satir["abone_konut"] - satir["panel_sayisi"])
    kural = int(satir["kural40_ev"])
    if aday <= 0:
        st.markdown(f"Kaç ev daha panel takabilir: **panelsiz konut yok**  \n"
                    f"Bugünkü kural (%40): {kural} ev")
        return
    karamsar, iyimser = int(satir["kac_ev_karamsar"]), int(satir["kac_ev_iyimser"])
    aralik = f"{karamsar}" if karamsar == iyimser else f"{karamsar}–{iyimser}"
    st.markdown(f"Kaç ev daha panel takabilir: **{aralik} ev**")
    if kural > iyimser and iyimser == 0:
        st.markdown(f":red[**Bugünkü kural (%40): {kural} ev** — kural, yer olmayan "
                    "trafoya \"yer var\" diyor]")
    elif kural > iyimser:
        st.markdown(f":red[**Bugünkü kural (%40): {kural} ev** — en iyimser tahminimizden "
                    "fazla; fazlası sınırı aşabilir]")
    elif kural < karamsar:
        st.markdown(f":blue[**Bugünkü kural (%40): {kural} ev** — en kötü durumdan "
                    "bile az; kural bekletmeye gerek olmayan başvuruları bekletiyor]")
    else:
        st.markdown(f"Bugünkü kural (%40): {kural} ev — aralığımızın içinde")


def yan_panel(klasor, veri, satir):
    st.subheader(f"Trafo {satir['trafo_no']}")
    if "renk" in veri:
        renk_basligi(satir)
        kac_ev_metni(satir)
    if "olculdu" in veri:
        olcum = "ölçüldü" if satir["olculdu"] == 1 else "**ölçülmedi**"
        st.markdown(f"{olcum} · güven {GUVEN_ADI.get(satir['guven'], satir['guven'])}")
    abone = int(satir.filter(like="abone_").sum())
    ayrinti = (f"{int(satir['kva'])} kVA · {satir['bolge']} · {satir['montaj']} · "
               f"{abone} abone · {int(satir['panel_sayisi'])} panel, {satir['panel_kw']:.1f} kW")
    if "sinir_karamsar" in veri:
        ayrinti += f" · sınırı belirleyen: {SINIR_ADI.get(satir['sinir_karamsar'], satir['sinir_karamsar'])}"
    if "olculdu" in veri:
        ayrinti += (f" · öğlen en düşük yük {satir['ogle_min_kw']:.1f} kW "
                    f"(%80 bant {satir['ogle_min_kw_p10']:.1f}–{satir['ogle_min_kw_p90']:.1f})")
    st.caption(ayrinti)
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
