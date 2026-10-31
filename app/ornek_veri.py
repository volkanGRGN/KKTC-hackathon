"""Harita için sahte şehirler üretir (Faz 1, Civan).

Sütunlar docs/data/tablo-bicimi.md sürüm 1 ile birebir. Değerler yalnız biçimi
ve haritayı denemek içindir: ölçüm ya da sonuç değil, "SAHTE VERİ — gösterim".

Çalıştırma: python3 app/ornek_veri.py  →  data/synthetic/sehir-901/ … 903/
"""

import csv
import math
import random
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CIKTI_KOK = KOK / "data" / "synthetic"

SEHIRLER = (901, 902, 903)
TRAFO_SAYISI = 40
OLCULU_MIN, OLCULU_MAX = 10, 15
ARKETIP_SAYISI = 4

# Referans: Girne merkez, data/raw/osm-kasaba alanının ortası (görev kartı).
REF_ENLEM, REF_BOYLAM = 35.3375, 33.318
YARICAP_M = 1500
KUZEY_MAX_M = 400  # denize düşmesin [Yorum]
METRE_BASINA_DERECE = 1 / 111_320

DIREK_KVA = (25, 50, 100, 250, 400)
YER_KVA = (630, 1000)
BOLGELER = ("kentsel", "kirsal", "turistik", "sanayi")
YENI_PANEL_KW = 6.5

TRAFOLAR_SUTUN = [
    "sehir", "trafo_no", "enlem", "boylam", "x_m", "y_m", "bolge", "montaj",
    "kva", "hat_sayisi", "hat_boyu_max_m", "hat_boyu_toplam_m", "kablo",
    "abone_konut", "abone_ticari1", "abone_ticari2", "abone_turizm",
    "abone_sanayi1", "abone_sanayi2", "abone_su_motoru",
    "panel_sayisi", "panel_kw",
]
TAHMIN_SUTUN = [
    "sehir", "trafo_no", "olculdu", "olculu_sayi", "arketip",
    "arketip_olasilik", "ogle_min_kw", "ogle_min_kw_p10", "ogle_min_kw_p90",
    "ogle_min_kw_olculen", "guven",
]
KAC_EV_SUTUN = [
    "sehir", "trafo_no", "kac_ev_karamsar", "kac_ev_iyimser", "isil_pay_kw",
    "gerilim_pay_kw_karamsar", "gerilim_pay_kw_iyimser", "sinir_karamsar",
    "renk", "kural40_ev",
]


def konum(rng):
    """Referans çevresinde (x_m, y_m, enlem, boylam); kuzeye en çok KUZEY_MAX_M."""
    x = rng.randint(-YARICAP_M, YARICAP_M)
    y = rng.randint(-YARICAP_M, KUZEY_MAX_M)
    enlem = REF_ENLEM + y * METRE_BASINA_DERECE
    boylam = REF_BOYLAM + x * METRE_BASINA_DERECE / math.cos(math.radians(REF_ENLEM))
    return x, y, round(enlem, 6), round(boylam, 6)


def aboneler(rng, bolge, kva):
    """Bölgeye göre abone karışımı; konut sayısı kVA ile büyür."""
    konut = max(1, round(kva * rng.uniform(0.15, 0.35)))
    abone = {
        "abone_konut": konut, "abone_ticari1": 0, "abone_ticari2": 0,
        "abone_turizm": 0, "abone_sanayi1": 0, "abone_sanayi2": 0,
        "abone_su_motoru": 0,
    }
    if bolge == "kentsel":
        abone["abone_ticari1"] = rng.randint(1, 8)
        abone["abone_ticari2"] = rng.randint(0, 2)
    elif bolge == "kirsal":
        abone["abone_konut"] = max(1, konut // 2)
        abone["abone_su_motoru"] = rng.randint(0, 4)
    elif bolge == "turistik":
        abone["abone_turizm"] = rng.randint(1, 3)
        abone["abone_ticari1"] = rng.randint(0, 4)
    else:  # sanayi
        abone["abone_konut"] = max(1, konut // 4)
        abone["abone_sanayi1"] = rng.randint(1, 4)
        abone["abone_sanayi2"] = rng.randint(0, 2)
    return abone


def trafo_satiri(rng, sehir, no):
    bolge = rng.choice(BOLGELER)
    montaj = "yer" if rng.random() < 0.2 else "direk"
    kva = rng.choice(YER_KVA if montaj == "yer" else DIREK_KVA)
    x, y, enlem, boylam = konum(rng)
    hat_sayisi = rng.randint(1, 4)
    hat_max = rng.randint(300, 700) if bolge == "kirsal" else rng.randint(120, 450)
    hat_toplam = max(hat_max, round(hat_max * hat_sayisi * rng.uniform(0.6, 0.9)))
    abone = aboneler(rng, bolge, kva)
    panel_sayisi = rng.randint(0, abone["abone_konut"] // 2)
    panel_kw = round(sum(rng.uniform(4, 8) for _ in range(panel_sayisi)), 2)
    return {
        "sehir": sehir, "trafo_no": f"T{no:02d}", "enlem": enlem, "boylam": boylam,
        "x_m": x, "y_m": y, "bolge": bolge, "montaj": montaj, "kva": kva,
        "hat_sayisi": hat_sayisi, "hat_boyu_max_m": hat_max,
        "hat_boyu_toplam_m": hat_toplam, "kablo": rng.choice(("ABC70", "ABC95")),
        **abone, "panel_sayisi": panel_sayisi, "panel_kw": panel_kw,
    }


def guven_etiketi(olasilik):
    if olasilik >= 0.8:
        return "yuksek"
    return "orta" if olasilik >= 0.6 else "dusuk"


def tahmin_satiri(rng, trafo, olculdu, olculu_sayi):
    abone_toplam = sum(v for k, v in trafo.items() if k.startswith("abone_"))
    ogle = abone_toplam * rng.uniform(0.25, 0.6)
    olasilik = round(rng.uniform(0.4, 0.97), 3)
    olculen = round(ogle * rng.uniform(0.9, 1.1), 2) if olculdu else ""
    return {
        "sehir": trafo["sehir"], "trafo_no": trafo["trafo_no"],
        "olculdu": int(olculdu), "olculu_sayi": olculu_sayi,
        "arketip": rng.randrange(ARKETIP_SAYISI), "arketip_olasilik": olasilik,
        "ogle_min_kw": round(ogle, 2),
        "ogle_min_kw_p10": round(ogle * rng.uniform(0.6, 0.85), 2),
        "ogle_min_kw_p90": round(ogle * rng.uniform(1.15, 1.5), 2),
        "ogle_min_kw_olculen": olculen, "guven": guven_etiketi(olasilik),
    }


def renk(karamsar, iyimser, guven):
    """docs/method/modeling.md bölüm 5'teki kural."""
    if iyimser == 0:
        return "kirmizi"
    return "yesil" if karamsar > 0 and guven == "yuksek" else "sari"


def kac_ev_satiri(rng, trafo, tahmin):
    kva, panel_kw = trafo["kva"], trafo["panel_kw"]
    aday = trafo["abone_konut"] - trafo["panel_sayisi"]
    isil = max(0.0, kva + tahmin["ogle_min_kw_p10"] - panel_kw)
    gerilim_iyimser = max(0.0, rng.uniform(-10, 60) * kva / 250)
    gerilim_karamsar = gerilim_iyimser * rng.uniform(0.2, 0.6)
    karamsar = min(aday, math.floor(min(isil, gerilim_karamsar) / YENI_PANEL_KW))
    iyimser = min(aday, math.floor(min(isil, gerilim_iyimser) / YENI_PANEL_KW))
    return {
        "sehir": trafo["sehir"], "trafo_no": trafo["trafo_no"],
        "kac_ev_karamsar": karamsar, "kac_ev_iyimser": iyimser,
        "isil_pay_kw": round(isil, 2),
        "gerilim_pay_kw_karamsar": round(gerilim_karamsar, 2),
        "gerilim_pay_kw_iyimser": round(gerilim_iyimser, 2),
        "sinir_karamsar": "gerilim" if gerilim_karamsar < isil else "isil",
        "renk": renk(karamsar, iyimser, tahmin["guven"]),
        "kural40_ev": math.floor(max(0.0, 0.4 * kva - panel_kw) / YENI_PANEL_KW),
    }


def csv_yaz(yol, sutunlar, satirlar):
    with open(yol, "w", encoding="utf-8", newline="") as f:
        yazici = csv.DictWriter(f, fieldnames=sutunlar, lineterminator="\n")
        yazici.writeheader()
        yazici.writerows(satirlar)


def sehir_uret(sehir):
    """Bir sahte şehrin tablolarını üretir; aynı tohum aynı tabloları verir."""
    rng = random.Random(sehir)
    trafolar = [trafo_satiri(rng, sehir, no) for no in range(1, TRAFO_SAYISI + 1)]
    olculu_sayi = rng.randint(OLCULU_MIN, OLCULU_MAX)
    olculu_nolar = set(rng.sample(range(TRAFO_SAYISI), olculu_sayi))
    tahminler = [
        tahmin_satiri(rng, t, i in olculu_nolar, olculu_sayi)
        for i, t in enumerate(trafolar)
    ]
    kac_ev = [kac_ev_satiri(rng, t, tm) for t, tm in zip(trafolar, tahminler)]
    return {"trafolar": trafolar, "tahmin": tahminler, "kac_ev": kac_ev}


def sehir_yaz(sehir, tablolar):
    klasor = CIKTI_KOK / f"sehir-{sehir:03d}"
    klasor.mkdir(parents=True, exist_ok=True)
    csv_yaz(klasor / "trafolar.csv", TRAFOLAR_SUTUN, tablolar["trafolar"])
    csv_yaz(klasor / "tahmin.csv", TAHMIN_SUTUN, tablolar["tahmin"])
    csv_yaz(klasor / "kac_ev.csv", KAC_EV_SUTUN, tablolar["kac_ev"])


def main():
    for sehir in SEHIRLER:
        tablolar = sehir_uret(sehir)
        sehir_yaz(sehir, tablolar)
        print(f"sehir-{sehir:03d}: {len(tablolar['trafolar'])} trafo")


if __name__ == "__main__":
    main()
