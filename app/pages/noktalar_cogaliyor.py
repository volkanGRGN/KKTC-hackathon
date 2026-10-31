"""Harita uygulamasının ikinci sayfası: "noktalar çoğalıyor" geçişi (app/animasyon.py)."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from animasyon import goster  # noqa: E402

st.set_page_config(page_title="Noktalar çoğalıyor", layout="wide")
goster()
st.page_link("harita.py", label="Canlı haritaya geç →")
