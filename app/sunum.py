"""Sunum: 7 ekran (Volkan kararı 17:32). Metin Can'ın docs/sunum/ekranlar.md tablosundan okunur;
Can metni değiştirince ekran da değişir. Görseller sonra eklenecek (yer tutucu).

Çalıştırma: streamlit run app/sunum.py
"""

import re
from pathlib import Path

import streamlit as st

KOK = Path(__file__).resolve().parent.parent
EKRANLAR_MD = KOK / "docs" / "sunum" / "ekranlar.md"
KILIT_GRAFIK = KOK / "docs" / "sunum" / "kilit_yanlis_yesil.png"
SATIR = re.compile(r"^\| \*\*(\d) ([^*]+)\*\*(.*)\|\s*$")

STIL = """
<style>
#MainMenu, header, footer, [data-testid="stToolbar"] {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 1100px;}
.cumle {font-size: 2.4rem; line-height: 1.25; font-weight: 600; margin: 1.5rem 0;}
.rakam {font-size: 1.6rem; font-weight: 700; color: #F0B41E;}
.etiket {font-size: 0.85rem; opacity: 0.7;}
.ust {font-size: 0.9rem; letter-spacing: 0.08em; opacity: 0.6; text-transform: uppercase;}
</style>
"""


def hucreler(satir):
    """'| a | b |' satırını hücrelere böler (bağlantı içindeki | yok sayılmaz; tabloda yok)."""
    return [h.strip() for h in satir.strip().strip("|").split("|")]


@st.cache_data
def ekranlari_oku(yol, zaman):
    ekranlar = []
    for satir in Path(yol).read_text(encoding="utf-8").splitlines():
        if not SATIR.match(satir):
            continue
        no_ad, cumle, gorsel, rakam, sure = hucreler(satir)[:5]
        no, ad = re.match(r"\*\*(\d) ([^*]+)\*\*", no_ad).groups()
        ekranlar.append({
            "no": int(no), "ad": ad.strip(), "cumle": cumle.strip('"“” '),
            "gorsel": gorsel, "rakam": "" if rakam == "—" else rakam, "sure": sure,
        })
    return ekranlar


def rakam_ve_etiket(metin):
    """'**rakam** [etiket]' → (rakam, etiket)."""
    eslesme = re.match(r"\*\*(.+?)\*\*\s*(.*)", metin)
    return eslesme.groups() if eslesme else (metin, "")


def gorsel_alani(ekran):
    if ekran["no"] == 5 and KILIT_GRAFIK.exists():
        st.image(str(KILIT_GRAFIK), width="stretch")
        st.caption("Canlı harita ayrı sayfada: streamlit run app/harita.py — gösterim")
        return
    st.info(f"Görsel (yapılacak): {ekran['gorsel']}")


def gezinme(adet):
    sol, orta, sag = st.columns([1, 6, 1])
    if sol.button("←", width="stretch", disabled=st.session_state.ekran == 0):
        st.session_state.ekran -= 1
        st.rerun()
    if sag.button("→", width="stretch", disabled=st.session_state.ekran == adet - 1):
        st.session_state.ekran += 1
        st.rerun()
    noktalar = " ".join("●" if i == st.session_state.ekran else "○" for i in range(adet))
    orta.markdown(f"<div style='text-align:center'>{noktalar}</div>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Mahalle şebekesi", layout="wide")
    st.markdown(STIL, unsafe_allow_html=True)
    if not EKRANLAR_MD.exists():
        st.error("docs/sunum/ekranlar.md bulunamadı.")
        return
    ekranlar = ekranlari_oku(str(EKRANLAR_MD), EKRANLAR_MD.stat().st_mtime_ns)
    if not ekranlar:
        st.error("ekranlar.md'de ekran tablosu okunamadı (satırlar '| **0 Açılış** | …' biçiminde olmalı).")
        return
    st.session_state.setdefault("ekran", 0)
    ekran = ekranlar[st.session_state.ekran]
    st.markdown(f"<div class='ust'>{ekran['no']} · {ekran['ad']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='cumle'>{ekran['cumle']}</div>", unsafe_allow_html=True)
    if ekran["rakam"]:
        rakam, etiket = rakam_ve_etiket(ekran["rakam"])
        st.markdown(f"<div class='rakam'>{rakam}</div>", unsafe_allow_html=True)
        st.markdown(f"<span class='etiket'>{etiket}</span>", unsafe_allow_html=True)
    gorsel_alani(ekran)
    gezinme(len(ekranlar))


if __name__ == "__main__":
    main()
