"""Canlı tahmin sayfası: harita kapalı açılır; bir trafoya tıkla, "ölçüldü" sayılır; model o an kurulur, gerisini tahmin eder.

Hesap dashboard/canli.py'de (ürünün kendi kodu: sablon.py, kac_ev_olasilik.py, tepe.py); eski model sürümleri
dashboard/surumler.py ile depo tarihçesinden. Harita Civan'ın (app/harita.py): sütun boyu trafo gücü, ölçülü trafoda
beyaz uç, Girne zemini. Gerçekle kıyas (sınav görünümü) yalnız farazi şehirde ve ölçülmeyen trafolarda; model gerçeği
görmez.
"""

import random
import sys
import time
from pathlib import Path

import altair as alt
import pandas as pd
import pydeck as pdk
import streamlit as st

import canli
import surumler
from ortak import *  # noqa: F401,F403 — sabitler, renkler, biçim ve veri okuma (ortak.py)

if str(KOK / "app") not in sys.path:
    sys.path.insert(0, str(KOK / "app"))
try:  # Civan'ın haritası (app/harita.py, harita/ui düzeni): varsa onun katmanları, yoksa aynı görünümde yerel katmanlar
    import harita as civan  # noqa: E402
except Exception:  # pragma: no cover — harita dosyası yoksa ya da açılmıyorsa
    civan = None
CIVAN_KATMANLARI = civan is not None and all(
    hasattr(civan, a) for a in ("trafo_katmanlari", "acilis_gorunumu", "zemin_katmanlari", "osm_zemin", "KIYI_DOSYASI"))
METRE_BASINA_KVA = 0.25  # Civan'ın kararı: sütun boyu = trafo gücü, 1000 kVA = 250 m
SUTUN_YARICAP_M = 35

ONERI_SAYISI = 12  # ürünün tasarımı: 40 trafodan 12'si ölçülür (sablon.py OLCULU_ANA)
OYNAT_ARALIK_SN = 1.0
HARITA_YUKSEKLIK = 600
OLCULDU_RGBA = [42, 120, 214, 235]  # model kurulmadan önce ölçülen trafo
KAPALI_RGBA = [110, 110, 110, 200]  # henüz tahmin yok
DOLULUK_SINIF = [  # yük haritası haritada: temkinli uç (aralığın üstü); eşikler Özet'teki %80 ve %100 ile aynı
    (1.0, "kirmizi", "%100 üstü, gücü aşabilir"),
    (0.8, "sari", "%80–100, önce bak"),
    (0.0, "yesil", "%80 altı"),
]
KATMAN_ADI = {"yuk": "Yük haritası · yılın tepesi", "panel": "Panel · öğlen gerilimi (259 V)"}


# ---------- hesap (önbellekli) ----------

def _zaman(klasor):
    return tuple(degisim_zamani(klasor / ad) for ad in ("trafolar.csv", "yuk_5dk.csv", "ayar.json"))


@st.cache_resource(show_spinner=False)
def _hazir(klasor, zaman):
    canli.isit()  # süreç havuzu ve tepe girdileri arka planda; ilk tıklama beklemesin
    return canli.sehir_hazirla(Path(klasor))


def hazir(klasor):
    return _hazir(str(klasor), _zaman(klasor))


@st.cache_data(show_spinner=False, max_entries=512)
def _hesap(klasor, zaman, olculu, surum):
    if len(olculu) < canli.EN_AZ_OLCULU:
        return None
    if surum == "guncel":
        return canli.tahmin_et(_hazir(klasor, zaman), list(olculu))
    return surumler.tahmin_et(surumler.surum(surum), klasor, list(olculu))


def hesap(klasor, olculu, surum):
    return _hesap(str(klasor), _zaman(klasor), tuple(olculu), surum)


@st.cache_data(show_spinner=False, max_entries=512)
def _kiyas(klasor, zaman, olculu, surum):
    sonuc = _hesap(klasor, zaman, olculu, surum)
    return canli.sinav_kiyasi(klasor, sonuc["tablo"]) if sonuc else (None, None)


def kiyas(klasor, olculu, surum):
    return _kiyas(str(klasor), _zaman(klasor), tuple(olculu), surum)


# ---------- oturum durumu ----------

def anahtarlar(klasor):
    k = kisa_yol(klasor)
    return dict(olculu=f"olculu::{k}", son=f"son-secim::{k}", gecmis=f"gecmis::{k}", oynat=f"oynat::{k}",
                bekleyen=f"bekleyen::{k}", harita=f"canli-harita::{k}")


def olculu_ayarla(a, nolar, olculu):
    st.session_state[a["olculu"]] = [t for t in nolar if t in set(olculu)]


def tiklamayi_isle(a, nolar):
    """Haritada yeni seçilen trafo ölçülüyse çıkar, değilse ekle. Harita aynı anahtarla yerinde güncellenir (yakınlık
    korunur); seçim değişmedikçe bir şey yapılmaz. Aynı trafoya ikinci tıklama seçimi kaldırır, üçüncüsü yine sayılır."""
    durum = st.session_state.get(a["harita"])
    nesneler = (((durum or {}).get("selection") or {}).get("objects") or {}).get("trafolar") or []
    secim = nesneler[0].get("trafo_no") if nesneler else None
    if secim == st.session_state.get(a["son"]):
        return
    st.session_state[a["son"]] = secim
    if secim is None or secim not in nolar:
        return
    olculu = list(st.session_state.get(a["olculu"], []))
    olculu.remove(secim) if secim in olculu else olculu.append(secim)
    olculu_ayarla(a, nolar, olculu)


def _oneri_ekle(a, nolar, oneri, hepsi):
    olculu = list(st.session_state.get(a["olculu"], []))
    if hepsi:
        olculu = list(oneri)
    else:
        kalan = [t for t in oneri if t not in olculu]
        olculu += kalan[:1] if kalan else _rastgele(nolar, olculu)
    olculu_ayarla(a, nolar, olculu)


def _rastgele(nolar, olculu):
    kalan = [t for t in nolar if t not in olculu]
    return [random.choice(kalan)] if kalan else []


def _rastgele_ekle(a, nolar):
    olculu = list(st.session_state.get(a["olculu"], []))
    olculu_ayarla(a, nolar, olculu + _rastgele(nolar, olculu))


def _sifirla(a):
    st.session_state[a["olculu"]] = []
    st.session_state[a["gecmis"]] = {}
    st.session_state[a["oynat"]] = False


def _oynat(a):
    _sifirla(a)
    st.session_state[a["oynat"]] = True


def _durdur(a):
    st.session_state[a["oynat"]] = False


# ---------- harita (Civan'ın katmanları) ----------

def doluluk_sinifi(d):
    for esik, renk, ad in DOLULUK_SINIF:
        if d >= esik:
            return renk, ad
    return DOLULUK_SINIF[-1][1], DOLULUK_SINIF[-1][2]


def ipucu_satirlari(r, gercek):
    """Haritada üstüne gelince: iki katmanın tahmini, sınav açıksa gerçeği."""
    s = []
    if pd.notna(r.get("doluluk")):
        s.append(f"Yük haritası: yılın tepesi {tr(r['tepe_kw'])} kW, doluluk {yuzde(r['doluluk'])} "
                 f"(en kötü durumda {yuzde(r['doluluk_temkinli'])})")
        if pd.notna(r.get("v_min_tepe_v_p10")):
            s.append(f"Akşam en düşük gerilim: {tr(r['v_min_tepe_v'], 1)} V (en kötü durumda {tr(r['v_min_tepe_v_p10'], 1)} V; "
                     "sınır 207 V)")
    if isinstance(r.get("renk"), str):
        ara = aralik(r["kac_ev_karamsar"], r["kac_ev_iyimser"])
        ev = "panelsiz konut yok" if r["aday"] <= 0 else f"yaklaşık {int(r['kac_ev_orta'])} ev ({ara})"
        s.append(f"Panel: {RENK_ADI[r['renk']]} · {ev} · bugün 259 V'u aşma olasılığı {yuzde(r['p_bugun_asar'])}")
    if pd.notna(r.get("ogle_min_kw")):
        if r["olculdu"] == 1:
            s.append(f"Öğlen en düşük yük: {tr(r['ogle_min_kw_olculen'], 1)} kW (ölçülen)")
        else:
            s.append(f"Öğlen en düşük yük: {tr(r['ogle_min_kw'], 1)} kW "
                     f"(aralık {aralik(r['ogle_min_kw_p10'], r['ogle_min_kw_p90'], 1)})")
    if gercek is not None and r["olculdu"] == 0 and r["trafo_no"] in gercek:
        g = gercek[r["trafo_no"]]
        parca = []
        if pd.notna(g.get("gercek_doluluk")):
            parca.append(f"doluluk {yuzde(g['gercek_doluluk'])}")
        parca.append(f"öğlen {tr(g['gercek_ogle_kw'], 1)} kW")
        if g.get("kac_ev_aday", 0) > 0:
            parca.append(f"kaç ev {int(g['gercek_kac_ev'])}")
        s.append("Gerçek: " + " · ".join(parca))
    return "<br/>".join(e(x) for x in s)


def harita_verisi(h, sonuc, olculu, katman, gercek):
    olculu_k = set(olculu)
    if sonuc is None:
        v = h["tr"][["trafo_no", "enlem", "boylam", "kva"]].copy()
        v["olculdu"] = v["trafo_no"].isin(olculu_k).astype(int)
        v["rgba"] = [OLCULDU_RGBA if o else KAPALI_RGBA for o in v["olculdu"]]
        v["baslik"] = [f"{t} · " + ("ölçüldü" if o else "henüz tahmin yok") for t, o in zip(v["trafo_no"], v["olculdu"])]
        v["metin"] = f"Model için en az {canli.EN_AZ_OLCULU} ölçülü trafo gerekir."
    else:
        v = sonuc["tablo"].copy()
        if katman == "yuk":
            renkler = [doluluk_sinifi(d)[0] for d in v["doluluk_temkinli"]]
        else:
            renkler = list(v["renk"])
        v["rgba"] = [RENK_RGBA[r] for r in renkler]
        v["baslik"] = [f"{t} · " + ("ölçüldü" if o else "model tahmini") for t, o in zip(v["trafo_no"], v["olculdu"])]
        g = None if gercek is None else gercek.set_index("trafo_no").to_dict("index")
        v["metin"] = [ipucu_satirlari(r, g) for r in v.to_dict("records")]
    v["yukseklik"] = v["kva"] * METRE_BASINA_KVA  # Civan: sütun boyu = trafo gücü
    return v[["trafo_no", "enlem", "boylam", "kva", "olculdu", "rgba", "yukseklik", "baslik", "metin"]]


def yerel_katmanlar(v):
    """Civan'ın yeni haritası yokken aynı görünüm: sütun (boy = trafo gücü), tıklanır taban, ölçülüye beyaz uç."""
    sutunlar = pdk.Layer("ColumnLayer", id="sutunlar", data=v, get_position=["boylam", "enlem"],
                         get_elevation="yukseklik", get_fill_color="rgba", radius=SUTUN_YARICAP_M, pickable=False)
    taban = pdk.Layer("ScatterplotLayer", id="trafolar", data=v, get_position=["boylam", "enlem"],
                      get_fill_color="rgba", get_radius=SUTUN_YARICAP_M * 1.4, radius_min_pixels=10, stroked=True,
                      get_line_color=[14, 17, 23, 255], line_width_min_pixels=1, pickable=True, auto_highlight=True,
                      highlight_color=[255, 255, 255, 90])
    olculu = v.loc[v["olculdu"] == 1, ["boylam", "enlem", "yukseklik"]].assign(uc=lambda t: t["yukseklik"] + 30)
    uc = pdk.Layer("ColumnLayer", id="olculu", data=olculu, get_position=["boylam", "enlem"], get_elevation="uc",
                   get_fill_color=[245, 247, 250, 255], radius=13, pickable=False)
    return [sutunlar, taban, uc]


def harita_ciz(v, anahtar):
    ipucu = {"html": "<b>{baslik}</b><br/>{metin}"}
    zemin = None
    if CIVAN_KATMANLARI:  # Civan'ın katmanları ve Girne zemini (internetsiz)
        zemin = civan.osm_zemin(str(civan.OSM_DOSYASI), str(civan.KIYI_DOSYASI))
        katmanlar = civan.trafo_katmanlari(v)
        gorunum = civan.acilis_gorunumu(v, genislik_px=760, yukseklik_px=HARITA_YUKSEKLIK)
    else:
        katmanlar = yerel_katmanlar(v)
        gorunum = pdk.ViewState(latitude=(v["enlem"].max() + v["enlem"].min()) / 2,
                                longitude=(v["boylam"].max() + v["boylam"].min()) / 2,
                                zoom=harita_yakinligi(v["enlem"], v["boylam"], HARITA_YUKSEKLIK) - 0.3, pitch=45)
    if zemin is None:
        deck = pdk.Deck(layers=katmanlar, initial_view_state=gorunum, map_style=None, tooltip=ipucu)
    else:
        deck = pdk.Deck(layers=civan.zemin_katmanlari(zemin) + katmanlar, initial_view_state=gorunum,
                        map_provider=None, tooltip=ipucu)
    st.pydeck_chart(deck, on_select="rerun", selection_mode="single-object", key=anahtar, height=HARITA_YUKSEKLIK,
                    alt="Canlı tahmin haritası: sütun bir trafo, boy trafo gücü, beyaz uç ölçüldü")
    return zemin


def lejant(katman, sonuc, zemin):
    if sonuc is None:
        parca = [("ölçüldü", "#2a78d6"), ("henüz tahmin yok", "#6e6e6e")]
    elif katman == "yuk":
        parca = [(ad, RENK_HEX[r]) for _, r, ad in reversed(DOLULUK_SINIF)]
    else:
        parca = [(RENK_ADI[r], RENK_HEX[r]) for r in RENK_SIRA]
    renkli = " ".join(f"<span class='nokta' style='color:{h}'>●</span> {e(ad)}" for ad, h in parca)
    st.markdown(f"<div class='lejant'>{renkli}</div>", unsafe_allow_html=True)
    not_ = "Sütun boyu = trafo gücü · beyaz uç = ölçüldü · üstüne gelince sayılar."
    if katman == "yuk" and sonuc is not None:
        not_ += " Renk en kötü duruma göre; eşikler gösterim için (Özet'teki %80 ve %100)."
    if zemin is not None:
        not_ += f" {civan.OSM_ATIF}"
    if not CIVAN_KATMANLARI:
        not_ += " (Civan'ın yeni haritası bu dalda yok: aynı görünüm yerel katmanlarla.)"
    st.caption(not_)


# ---------- sağ panel ----------

def ozet_kutulari(sonuc, katman):
    t = sonuc["tablo"]
    if katman == "yuk":
        aksam = int((t["v_min_tepe_v_p10"] < 207).sum()) if "v_min_tepe_v_p10" in t else None
        kutu_izgarasi([
            sunum("doluluk_tipik", yuzde(t["doluluk"].median())),
            sunum("once_bak", tr((t["doluluk_temkinli"] >= 0.8).sum())),
            sunum("aksam_gerilim", "—" if aksam is None else tr(aksam)),
        ])
    else:
        sayim = t["renk"].value_counts()
        parcalar = [(RENK_ADI[r], int(sayim.get(r, 0)), RENK_HEX[r]) for r in RENK_SIRA]
        st.markdown("**Panel katmanı · öğlen gerilimi**")
        st.markdown(yigin_html(parcalar), unsafe_allow_html=True)
        st.markdown(lejant_html(parcalar, [VARSAYILAN_RENK_CUMLE[r] for r in RENK_SIRA]), unsafe_allow_html=True)
        st.caption(f"Kaç ev daha: yaklaşık {tr(t['kac_ev_orta'].sum())} ev, büyük olasılıkla "
                   f"{aralik(t['kac_ev_karamsar'].sum(), t['kac_ev_iyimser'].sum())} (trafo aralıklarının toplamı).")
    m = sonuc["model"]
    st.caption(f"Model {len(sonuc['olculu'])} ölçümle kuruldu: {m['k']} günlük eğri tipi "
               f"({', '.join(a.replace('_', ' ') for a in m['ad'])}). Öğlen yükü %80 aralığı tahminin "
               f"×{tr(m['bant'][0], 2)}–×{tr(m['bant'][1], 2)} katı.")


def sinav_paneli(ozet, katman, gecmis):
    st.markdown(f"**Gerçekle kıyas — yalnız deneme şehrinde, model görmez** · ölçülmeyen {ozet['olculmeyen']} trafo")
    if katman == "yuk" and "tepe_hata" in ozet:
        kutular = [
            sunum("tepe_sapma", yuzde(ozet.get("tepe_hata")),
                  f"Kötü giden onda birlik dilimde {yuzde(ozet.get('tepe_hata_p90'))}."),
            sunum("tepe_aralik", yuzde(ozet.get("tepe_kapsama"))),
        ]
        if "dolu80" in ozet:
            kutular.append(sunum("dolu_yakalama", f"{ozet['dolu80_yakalanan']} / {ozet['dolu80']}",
                                 f"Bunun için {ozet['dolu80_uyari']} trafoya uyarı verdik."))
        kutu_izgarasi(kutular)
    else:
        kutu_izgarasi([
            sunum("ogle_sapma", yuzde(ozet.get("ogle_hata")),
                  f"Kötü giden onda birlik dilimde {yuzde(ozet.get('ogle_hata_p90'))}."),
            sunum("yanlis_yesil", f"{ozet['yanlis_yesil']} / {ozet['yesil']}"),
            sunum("kural_yanlis", f"{ozet['kural_yanlis']} / {ozet['dolu']}"),
        ])
        if ozet["yanlis_yesil"] > 0:
            st.error(f"{ozet['yanlis_yesil']} trafoya yanlış yeşil: model az ölçümle fazla emin olabilir.")
    st.caption("Gerçek, deneme şehrinin cevap anahtarından; model onu görmez. Yalnız farazi şehirde, gösterim.")
    if len(gecmis) >= 2:
        hata_grafigi(gecmis)


def hata_grafigi(gecmis):
    """Ölçülen trafo sayısına göre hata; iki seri aynı birim (%), tek eksen."""
    satirlar = []
    for n, (ogle, tepe) in sorted(gecmis.items()):
        if ogle is not None:
            satirlar.append(dict(n=n, seri="öğlen yükü (panel)", hata=ogle * 100))
        if tepe is not None:
            satirlar.append(dict(n=n, seri="yılın tepesi (yük haritası)", hata=tepe * 100))
    if not satirlar:
        return
    df = pd.DataFrame(satirlar)
    renk = alt.Scale(domain=["yılın tepesi (yük haritası)", "öğlen yükü (panel)"], range=[MAVI_HEX, "#eb6834"])
    taban = alt.Chart(df).encode(
        x=alt.X("n:Q", title="Ölçülen trafo sayısı", axis=alt.Axis(tickMinStep=1)),
        y=alt.Y("hata:Q", title="Tipik trafoda sapma (%)", scale=alt.Scale(zero=True)),
        color=alt.Color("seri:N", scale=renk, legend=alt.Legend(title=None, orient="top")),
        tooltip=[alt.Tooltip("seri:N", title="Ne"), alt.Tooltip("n:Q", title="Ölçülen"),
                 alt.Tooltip("hata:Q", title="Hata %", format=".1f")],
    )
    st.markdown("**Ölçtükçe hata**")
    st.altair_chart((taban.mark_line(strokeWidth=2) + taban.mark_point(filled=True, size=70))
                    .properties(height=200), width="stretch")


def tahmin_tablosu(sonuc, gercek):
    t = sonuc["tablo"]
    g = pd.DataFrame({"Trafo": t["trafo_no"], "Durum": t["olculdu"].map({1: "ölçüldü", 0: "tahmin"})})
    ayar = {}
    if "doluluk" in t:
        g["Doluluk"] = t["doluluk"] * 100
        g["Doluluk, en kötü durum"] = t["doluluk_temkinli"] * 100
        g["Tepe (kW)"] = t["tepe_kw"]
        ayar.update({
            "Doluluk": st.column_config.NumberColumn(format="%%%.0f", help="Yük haritası, orta tahmin"),
            "Doluluk, en kötü durum": st.column_config.NumberColumn(format="%%%.0f", help="Yük haritası: aralığın üst ucu"),
            "Tepe (kW)": st.column_config.NumberColumn(format="%.1f", help="Yük haritası"),
        })
        if "v_min_tepe_v_p10" in t:
            g["Akşam en düşük gerilim (V)"] = t["v_min_tepe_v_p10"]
            ayar["Akşam en düşük gerilim (V)"] = st.column_config.NumberColumn(format="%.1f", help="Yük haritası, en kötü durumda; sınır 207 V")
    g["Renk"] = t["renk"].map(lambda r: f"{RENK_ISARET[r]} {RENK_ADI[r]}")
    g["259 V'u aşma"] = t["p_bugun_asar"] * 100
    g["Kaç ev"] = t["kac_ev_orta"]
    g["Aralık"] = [aralik(a, b) for a, b in zip(t["kac_ev_karamsar"], t["kac_ev_iyimser"])]
    g["Öğlen yükü (kW)"] = t["ogle_min_kw"]
    ayar["259 V'u aşma"] = st.column_config.NumberColumn(format="%%%.0f", help="Panel: bugün aşma olasılığı")
    ayar["Öğlen yükü (kW)"] = st.column_config.NumberColumn(format="%.1f", help="Panel katmanının girdisi")
    if gercek is not None:
        gg = gercek.set_index("trafo_no")
        if "gercek_doluluk" in gg:
            g["Gerçek doluluk"] = t["trafo_no"].map(gg["gercek_doluluk"]) * 100
            ayar["Gerçek doluluk"] = st.column_config.NumberColumn(format="%%%.0f", help="Cevap anahtarı, gösterim")
        g["Gerçek kaç ev"] = t["trafo_no"].map(gg["gercek_kac_ev"])
        g["Gerçek öğlen (kW)"] = t["trafo_no"].map(gg["gercek_ogle_kw"])
        ayar["Gerçek öğlen (kW)"] = st.column_config.NumberColumn(format="%.1f", help="Cevap anahtarı, gösterim")
    st.dataframe(g, hide_index=True, width="stretch", column_config=ayar, height=380)


# ---------- sayfa ----------

def sayfa():
    _, klasorler = veri_seti_sec()
    if not klasorler:
        st.info("Şehir verisi yok. Deneme şehri üretmek için:")
        st.code("python3 src/sehir_uret.py 1 10", language="bash")
        return
    gerekli = [k for k in klasorler if (k / "yuk_5dk.csv").exists()]
    if not gerekli:
        st.info("Canlı tahmin için şehir klasöründe yuk_5dk.csv gerekir (ölçülecek trafoların yükü).")
        return
    klasor = st.sidebar.selectbox("Şehir", gerekli, key="canli_sehir", format_func=lambda p: p.name)
    secenekler = [s for s in surumler.SURUMLER if surumler.kullanilabilir(s)[0]]
    surum = st.sidebar.selectbox("Model sürümü", [s["anahtar"] for s in secenekler], key="canli_surum",
                                 format_func=lambda k: surumler.surum(k)["ad"],
                                 help="Depo tarihçesinden: aynı ölçümlerle eski sürüm ne derdi?")
    st.sidebar.caption(surumler.surum(surum)["aciklama"])
    st.sidebar.caption("Haritada bir trafoya tıkla: ölçülmüş sayılır. Ölçümü kaldırmak için aşağıdaki listeden çıkar.")

    h = hazir(klasor)
    a = anahtarlar(klasor)
    st.session_state.setdefault(a["olculu"], [])
    st.session_state.setdefault(a["gecmis"], {})
    st.session_state.setdefault(a["oynat"], False)
    if a["bekleyen"] in st.session_state:  # oynatın bir önceki turda seçtiği trafo (liste kutusu çizilmeden önce)
        olculu_ayarla(a, h["nolar"], st.session_state.pop(a["bekleyen"]))
    tiklamayi_isle(a, h["nolar"])
    oneri = canli.oneri(h, ONERI_SAYISI)
    ayar = json_oku(klasor / "ayar.json") or {}
    sinav_var = (klasor / "cevap_anahtari.csv").exists() and sehir_no(klasor) < 800

    st.markdown("## Canlı tahmin")
    st.caption("Harita kapalı açılır. Bir trafoya tıkla: o trafo ölçülmüş sayılır. Model o an yalnız ölçülenlerden "
               f"kurulur ve ölçülmeyen bütün trafoları tahmin eder. En az {canli.EN_AZ_OLCULU} ölçüm gerekir; "
               f"ürünün tasarımı 40 trafodan {ONERI_SAYISI}'si.")
    st.warning(f"{etiket(sehir_no(klasor), ayar)} · {klasor.name} · {len(h['nolar'])} trafo · trafo yerleri gerçek "
               f"değil · model: {surumler.surum(surum)['ad']}")

    ust = st.columns([2.4, 1.25, 1.25, 1.25, 1])
    katman = ust[0].radio("Haritada", ["yuk", "panel"], horizontal=True, key="canli_katman",
                          format_func=lambda k: KATMAN_ADI[k])
    ust[1].button(f"Önerilen {ONERI_SAYISI}'yi ölç", on_click=_oneri_ekle, args=(a, h["nolar"], oneri, True),
                  width="stretch", help="Ürünün tabakalı seçimi: benzer trafolar değil, boşluklar ölçülür.")
    ust[2].button("Önerilenden 1 ekle", on_click=_oneri_ekle, args=(a, h["nolar"], oneri, False), width="stretch")
    if st.session_state[a["oynat"]]:
        ust[3].button("Durdur", on_click=_durdur, args=(a,), width="stretch", type="primary")
    else:
        ust[3].button("Sırayla oynat", on_click=_oynat, args=(a,), width="stretch",
                      help=f"Haritayı kapatır, önerilen {ONERI_SAYISI} trafoyu birer birer ölçer.")
    ust[4].button("Sıfırla", on_click=_sifirla, args=(a,), width="stretch", help="Haritayı kapatır.")
    sinav = st.toggle("Gerçekle kıyas — yalnız deneme şehrinde, model görmez", value=sinav_var, disabled=not sinav_var,
                      key="canli_sinav", help="Benzetimin bildiği gerçekle (cevap anahtarı) yalnız puanlar; tahmine giden "
                                              "hiçbir yola girmez (KARAR, 1 Kasım).")

    olculu = st.session_state[a["olculu"]]
    with st.spinner("Model kuruluyor…" if surum == "guncel" else "Eski sürüm hazırlanıyor (ilk seferde birkaç saniye)…"):
        sonuc = hesap(klasor, olculu, surum)
        ozet, gercek = kiyas(klasor, olculu, surum) if (sinav and sonuc) else (None, None)
    gecmis = st.session_state[a["gecmis"]].setdefault(surum, {})
    if ozet is not None:
        gecmis[len(olculu)] = (ozet.get("ogle_hata"), ozet.get("tepe_hata"))
    yuk_yok = sonuc is not None and not sonuc["model"].get("yuk_var", True)
    gosterilen = "panel" if (katman == "yuk" and yuk_yok) else katman

    sol, sag = st.columns([3, 2])
    with sol:
        if katman == "yuk" and yuk_yok:
            st.info("Bu model sürümünde yük haritası yoktu (ilk kez 1 Kasım 01:58); panel katmanı gösteriliyor.")
        zemin = harita_ciz(harita_verisi(h, sonuc, olculu, gosterilen, gercek), a["harita"])
        lejant(gosterilen, sonuc, zemin)
    with sag:
        kutu_izgarasi([
            sunum("olculen", f"{len(olculu)} / {len(h['nolar'])}"),
            sunum("tahmin_edilen", tr(len(h["nolar"]) - len(olculu)) if sonuc else "—"),
        ])
        if sonuc is None:
            kalan = canli.EN_AZ_OLCULU - len(olculu)
            st.info(f"Harita kapalı. Model için {kalan} trafo daha ölç: haritada bir sütuna tıkla ya da "
                    "\"Önerilenden 1 ekle\".")
        else:
            if len(olculu) < canli.GUVENILIR_OLCULU:
                st.warning(f"{len(olculu)} ölçümle aralıklar güvenilmez: aralık ölçülülerin birbirini tahmin etme "
                           "hatasından çıkıyor, az ölçümde fazla dar. Model fazla emin olabilir.")
            ozet_kutulari(sonuc, gosterilen)
            if ozet is not None:
                sinav_paneli(ozet, gosterilen, gecmis)
        st.multiselect("Ölçülen trafolar", h["nolar"], key=a["olculu"], placeholder="henüz yok",
                       help="Elle de eklenip çıkarılabilir.")

    if sonuc is not None:
        with st.expander("Bütün tahminler (tablo)"):
            tahmin_tablosu(sonuc, gercek)

    if st.session_state[a["oynat"]]:  # sırayla oynat: her turda önerilenden bir trafo
        kalan = [t for t in oneri if t not in olculu]
        if kalan:
            time.sleep(OYNAT_ARALIK_SN)
            st.session_state[a["bekleyen"]] = olculu + kalan[:1]
            st.rerun()
        else:
            st.session_state[a["oynat"]] = False
