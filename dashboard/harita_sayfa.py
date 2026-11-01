"""Harita sayfası: Civan'ın haritası (app/harita.py, harita/ui düzeni) dashboard'un içinde.

Civan'ın dosyasına dokunulmaz; onun fonksiyonları çağrılır ve düzeni onun main()'iyle aynı. İki fark var:
  - şehir dashboard'un veri setinden seçilir (data/synthetic altındaki klasörler dahil, ör. u15/sehir-031);
  - sayfa ayarı ve menüyü gizleyen CSS uygulanmaz, yoksa dashboard'un sayfa menüsü kaybolur.
Civan haritasını güncelleyince bu sayfa da kendiliğinden güncellenir.
"""

import sys

import streamlit as st

from ortak import KOK, veri_seti_sec

if str(KOK / "app") not in sys.path:
    sys.path.insert(0, str(KOK / "app"))

try:
    import harita as civan  # noqa: E402  (app/harita.py, Civan)
except Exception:  # pragma: no cover
    civan = None

# Sayfa Civan'ın harita/ui düzenine dayanır; main'deki eski harita.py'de bu fonksiyonlar yok → menüde gösterilmez.
GEREKEN = ("sutun_verisi", "birlesik_tablo", "etiket", "etiket_rengi", "ayar_oku", "osm_zemin", "KIYI_DOSYASI",
           "sehir_ozeti", "harita", "HARITA_YUKSEKLIK_PX", "lejant", "secili_satir", "bos_panel", "yan_panel", "alt_serit")
KULLANILABILIR = civan is not None and all(hasattr(civan, a) for a in GEREKEN)


def sayfa():
    _, klasorler = veri_seti_sec()
    st.sidebar.caption("Bu sayfa Civan'ın haritası (app/harita.py). Bir direğe tıkla: kararı ve gün boyu yükü.")
    if not klasorler:
        st.error("Şehir yok. Önce sahte şehirleri üret: python app/ornek_veri.py")
        return
    baslik, secim, rozet = st.columns([6, 2, 4], vertical_alignment="center")
    baslik.markdown("### Mahalle şebekesi haritası · Girne")
    secili = secim.selectbox("Şehir", klasorler, format_func=lambda p: p.name, label_visibility="collapsed",
                             key="harita_sehir")
    veri = civan.sutun_verisi(civan.birlesik_tablo(secili))
    sehir_no = int(veri["sehir"].iloc[0])
    with rozet.container(horizontal=True, horizontal_alignment="right"):
        st.badge(civan.etiket(sehir_no, civan.ayar_oku(secili)), color=civan.etiket_rengi(sehir_no),
                 icon=":material/info:")
    zemin = civan.osm_zemin(str(civan.OSM_DOSYASI), str(civan.KIYI_DOSYASI))
    oz = civan.sehir_ozeti(veri)
    sol, sag = st.columns([13, 7], gap="medium")
    with sol:
        durum = st.pydeck_chart(
            civan.harita(veri, zemin), on_select="rerun", selection_mode="single-object",
            key=f"harita-{civan_anahtar(secili)}", height=civan.HARITA_YUKSEKLIK_PX,
            alt="Trafo haritası: her sütun bir trafo, renk karar, boy trafo gücü",
        )
        civan.lejant(veri, zemin)
    with sag:
        with st.container(border=True, height=civan.HARITA_YUKSEKLIK_PX + 40):
            satir = civan.secili_satir(durum, veri)
            if satir is None:
                civan.bos_panel(oz)
            else:
                civan.yan_panel(secili, veri, satir)
    civan.alt_serit(oz)


def civan_anahtar(klasor):
    return f"{klasor.parent.name}-{klasor.name}"
