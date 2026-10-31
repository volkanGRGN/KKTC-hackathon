"""Sunum geçişi: "noktalar çoğalıyor" (civan.md KARAR 17:32, EK 17:33).

Önce Girne'deki farazi şehirde (sehir-001) ölçülü trafolar tek tek belirir, sonra kalanı
tahminle yayılır; ardından görünüm adaya açılır ve öbür farazi şehirler adanın kasabalarına
temsili olarak yerleşir. Renkler kac_ev.csv'den, ölçülü/ölçülmedi tahmin.csv'den.
Ölçülen trafo dolu nokta, tahmin edilen soluk halka. İnternetsiz: dış kaynak yok.

Tek başına: streamlit run app/animasyon.py
"""

import json
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

KOK = Path(__file__).resolve().parent.parent
VERI_KOK = KOK / "data" / "synthetic"
ADA_DOSYASI = Path(__file__).resolve().parent / "ada_kiyi.json"  # Natural Earth 1:50m, kamu malı
FARAZI_SEHIRLER = range(1, 800)  # 800–899 gerçek ölçüm, 900–999 sahte: animasyona girmez

# Farazi şehirlerin adaya temsili yerleşimi (enlem, boylam) [Yorum: yaklaşık kasaba merkezi,
# gerçek trafo yeri değil]. sehir-001 kendi koordinatıyla Girne'de durur.
KASABALAR = [
    ("Lefkoşa", 35.19, 33.36), ("Gazimağusa", 35.12, 33.93), ("Güzelyurt", 35.20, 32.99),
    ("İskele", 35.29, 33.89), ("Lefke", 35.11, 32.85), ("Lapta", 35.335, 33.165),
    ("Dipkarpaz", 35.60, 34.38), ("Değirmenlik", 35.25, 33.48), ("Akdoğan", 35.21, 33.73),
    ("Mehmetçik", 35.42, 34.08), ("Esentepe", 35.35, 33.58), ("Tatlısu", 35.38, 33.76),
    ("Yeni Erenköy", 35.535, 34.19), ("Beyarmudu", 35.05, 33.70), ("Serdarlı", 35.25, 33.61),
    ("Kalkanlı", 35.23, 33.08), ("Çamlıbel", 35.30, 33.07), ("Gönyeli", 35.215, 33.31),
    ("Yeniboğaziçi", 35.165, 33.89),
]
KUCULTME = 0.4  # öbür şehirlerin trafo dağılımı küçültülür, kasabalar üst üste binmesin

# Basit izdüşüm: km cinsinden x (doğu), y (güney); 35,2° enlemde 1° boylam ≈ 90,7 km.
BOYLAM_0, ENLEM_0 = 32.2, 35.75
KM_BOYLAM, KM_ENLEM = 90.7, 111.0


def xy(enlem, boylam):
    return round((boylam - BOYLAM_0) * KM_BOYLAM, 3), round((ENLEM_0 - enlem) * KM_ENLEM, 3)


def sehir_tablosu(klasor):
    """trafolar + tahmin + kac_ev; dosyalardan biri yoksa None."""
    yollar = [klasor / ad for ad in ("trafolar.csv", "tahmin.csv", "kac_ev.csv")]
    if not all(y.exists() for y in yollar):
        return None
    tablolar = [pd.read_csv(y, encoding="utf-8", dtype={"trafo_no": str}) for y in yollar]
    birlesik = tablolar[0][["trafo_no", "enlem", "boylam"]]
    birlesik = birlesik.merge(tablolar[1][["trafo_no", "olculdu"]], on="trafo_no")
    return birlesik.merge(tablolar[2][["trafo_no", "renk"]], on="trafo_no")


def noktalar(tablo, merkez, kucultme):
    """Şehrin trafoları, merkez (enlem, boylam) çevresine kucultme oranıyla yerleşmiş."""
    orta_enlem, orta_boylam = tablo["enlem"].mean(), tablo["boylam"].mean()
    hedef_enlem, hedef_boylam = merkez if merkez else (orta_enlem, orta_boylam)
    sonuc = []
    for _, s in tablo.iterrows():
        x, y = xy(hedef_enlem + (s["enlem"] - orta_enlem) * kucultme,
                  hedef_boylam + (s["boylam"] - orta_boylam) * kucultme)
        sonuc.append({"x": x, "y": y, "c": s["renk"], "o": int(s["olculdu"])})
    return sonuc


@st.cache_data
def animasyon_verisi():
    """İlk farazi şehir Girne'de gerçek yerinde, kalanı kasabalara; ada kıyısı."""
    klasorler = [k for k in sorted(VERI_KOK.iterdir()) if k.name.startswith("sehir-")
                 and int(k.name.split("-")[1]) in FARAZI_SEHIRLER] if VERI_KOK.exists() else []
    tablolar = [t for t in (sehir_tablosu(k) for k in klasorler) if t is not None]
    sehirler = []
    for i, tablo in enumerate(tablolar[: len(KASABALAR) + 1]):
        if i == 0:
            sehirler.append({"ad": "Girne", "n": noktalar(tablo, None, 1.0)})
        else:
            ad, enlem, boylam = KASABALAR[i - 1]
            sehirler.append({"ad": ad, "n": noktalar(tablo, (enlem, boylam), KUCULTME)})
    ada = json.loads(ADA_DOSYASI.read_text(encoding="utf-8"))
    cizgi = lambda halkalar: [[xy(e, b) for b, e in h] for h in halkalar]
    return {"sehirler": sehirler, "dolgu": cizgi(ada["dolgu"]), "kiyi": cizgi(ada["kiyi"])}


HTML_DOSYASI = Path(__file__).resolve().parent / "animasyon.html"


def goster():
    """Animasyonu çizer (sayfa dosyasından, ileride sunum ekranından çağrılır)."""
    veri = animasyon_verisi()
    if not veri["sehirler"]:
        st.error("Farazi şehir yok (data/synthetic/sehir-001 … ). Önce şehirleri üret.")
        return
    html = HTML_DOSYASI.read_text(encoding="utf-8")
    components.html(html.replace("__VERI__", json.dumps(veri, ensure_ascii=False)), height=600)


if __name__ == "__main__":
    st.set_page_config(page_title="Noktalar çoğalıyor", layout="wide")
    goster()
