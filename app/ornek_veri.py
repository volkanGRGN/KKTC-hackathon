"""Harita için sahte şehirler üretir (Faz 1, Civan).

Sütunlar docs/data/tablo-bicimi.md sürüm 1 ile birebir. Değerler yalnız biçimi
ve haritayı denemek içindir: ölçüm ya da sonuç değil, "SAHTE VERİ — gösterim".

Çalıştırma: python3 app/ornek_veri.py  →  data/synthetic/sehir-901/ … 903/
"""

import csv
import json
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
KUZEY_MAX_M = 400  # denize düşmesin [Yorum]; kıyı dosyası yoksa tek önlem
METRE_BASINA_DERECE = 1 / 111_320
# OSM kıyı çizgisi (data/raw/osm-kasaba/KAYNAK.txt); varsa denizdeki nokta yeniden çekilir.
KIYI_DOSYASI = KOK / "data" / "raw" / "osm-kasaba" / "girne_kiyi.json"

DIREK_KVA = (25, 50, 100, 250, 400)
YER_KVA = (630, 1000)
BOLGELER = ("kentsel", "kirsal", "turistik", "sanayi")
YENI_PANEL_KW = 6.5
PANEL_YAYGINLIGI = (0.03, 0.25)  # konut abonelerinin payı, ADR-0006
PANEL_KW = (4.0, 6.5)  # bir çatı paneli, kW (civan.md 13:33, Volkan)

SOZLESME_SURUMU = 1
ADIM_SAYISI = 288  # 5 dakikalık adım, bir gün
OGLE_ADIMLARI = range(132, 168)  # 11:00–14:00, sözleşme "Öğlen penceresi"
GUNLER = ((0, "isgunu"), (1, "tatil"))  # kart: 2 gün yeter
CATI_GUNES_TEPE = 0.63  # Nisan iş günü tepesi, pu [Kaynaklı: EAC injection, veri sözlüğü]

# Arketip eğrileri: (tepe saati, genişlik saat, ağırlık) tümsekleri + taban.
# Biçim gösterimi; EAC eğrisi değil.
ARKETIPLER = (
    ("aksam_tepeli_konut", 0.35, ((8.0, 1.5, 0.35), (20.5, 2.0, 0.65))),
    ("oglen_tepeli_carsi", 0.20, ((12.5, 3.0, 0.80),)),
    ("duz_sanayi", 0.60, ((10.0, 4.0, 0.40),)),
    ("gun_boyu_turizm", 0.50, ((13.0, 4.0, 0.30), (21.0, 2.0, 0.20))),
)
TATIL_CARPANI = {
    "aksam_tepeli_konut": 1.10, "oglen_tepeli_carsi": 0.75,
    "duz_sanayi": 0.60, "gun_boyu_turizm": 1.00,
}

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
ARKETIP_SUTUN = ["sehir", "arketip", "arketip_adi", "gun_turu", "adim", "oran"]
YUK_SUTUN = [
    "sehir", "trafo_no", "gun", "gun_turu", "adim", "saat",
    "tuketim_kw", "uretim_kw", "net_kw", "v_max_v", "v_min_v",
]


def kiyi_segmentleri():
    """OSM kıyı çizgisi parçaları [((boylam, enlem), (boylam, enlem))]; dosya yoksa None."""
    if not KIYI_DOSYASI.exists():
        return None
    veri = json.loads(KIYI_DOSYASI.read_text(encoding="utf-8"))
    segmentler = []
    for yol in veri["elements"]:
        noktalar = [(n["lon"], n["lat"]) for n in yol["geometry"]]
        segmentler += list(zip(noktalar, noktalar[1:]))
    return segmentler


def karada(boylam, enlem, segmentler):
    """Kuzeye ışın: kıyıyı tek sayıda kesiyorsa nokta karada (deniz kuzeyde)."""
    kesisme = 0
    for (x1, y1), (x2, y2) in segmentler:
        if (x1 > boylam) != (x2 > boylam):
            y = y1 + (boylam - x1) * (y2 - y1) / (x2 - x1)
            kesisme += y > enlem
    return kesisme % 2 == 1


def konum(rng, segmentler):
    """Referans çevresinde (x_m, y_m, enlem, boylam); kıyı varsa karada kalana dek çeker."""
    while True:
        x = rng.randint(-YARICAP_M, YARICAP_M)
        y = rng.randint(-YARICAP_M, KUZEY_MAX_M)
        enlem = REF_ENLEM + y * METRE_BASINA_DERECE
        boylam = REF_BOYLAM + x * METRE_BASINA_DERECE / math.cos(math.radians(REF_ENLEM))
        if segmentler is None or karada(boylam, enlem, segmentler):
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


def trafo_satiri(rng, sehir, no, yayginlik, segmentler):
    bolge = rng.choice(BOLGELER)
    montaj = "yer" if rng.random() < 0.2 else "direk"
    kva = rng.choice(YER_KVA if montaj == "yer" else DIREK_KVA)
    x, y, enlem, boylam = konum(rng, segmentler)
    hat_sayisi = rng.randint(1, 4)
    hat_max = rng.randint(300, 700) if bolge == "kirsal" else rng.randint(120, 450)
    hat_toplam = max(hat_max, round(hat_max * hat_sayisi * rng.uniform(0.6, 0.9)))
    abone = aboneler(rng, bolge, kva)
    konut = abone["abone_konut"]
    panel_sayisi = min(konut, round(konut * yayginlik * rng.uniform(0.5, 1.5)))
    panel_kw = round(sum(rng.uniform(*PANEL_KW) for _ in range(panel_sayisi)), 2)
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
    gerilim_iyimser = max(0.0, rng.uniform(-8, 40) + 0.08 * kva)
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


def arketip_oranlari():
    """{(arketip, gun_turu): 288 oran}; her eğri kendi tepesine bölünür (0–1)."""
    oranlar = {}
    for no, (_, taban, tumsekler) in enumerate(ARKETIPLER):
        carpan = TATIL_CARPANI[ARKETIPLER[no][0]]
        for _, gun_turu in GUNLER:
            k = carpan if gun_turu == "tatil" else 1.0
            ham = [
                taban + k * sum(
                    w * math.exp(-0.5 * ((adim / 12 - t) / g) ** 2)
                    for t, g, w in tumsekler
                )
                for adim in range(ADIM_SAYISI)
            ]
            tepe = max(ham)
            oranlar[(no, gun_turu)] = [h / tepe for h in ham]
    return oranlar


def arketip_satirlari(sehir, oranlar):
    return [
        {
            "sehir": sehir, "arketip": no, "arketip_adi": ARKETIPLER[no][0],
            "gun_turu": gun_turu, "adim": adim, "oran": round(oran, 3),
        }
        for (no, gun_turu), egri in oranlar.items()
        for adim, oran in enumerate(egri)
    ]


def saat(adim):
    return f"{adim // 12:02d}:{adim % 12 * 5:02d}"


def gunes_pu(adim):
    """Açık gün çatı güneşi, 07:00–19:00, tepe 13:00 (biçim gösterimi)."""
    return CATI_GUNES_TEPE * max(0.0, math.sin(math.pi * (adim / 12 - 7) / 12))


def yuk_satirlari(trafo, tahmin, oranlar):
    """Ölçülü trafonun 2 günlük yükü; öğlen en düşüğü tahmin.csv'deki ölçülene eşit."""
    a = tahmin["arketip"]
    ogle_min_oran = min(oranlar[(a, gt)][i] for _, gt in GUNLER for i in OGLE_ADIMLARI)
    olcek = tahmin["ogle_min_kw_olculen"] / ogle_min_oran
    kva = trafo["kva"]
    satirlar = []
    for gun, gun_turu in GUNLER:
        for adim, oran in enumerate(oranlar[(a, gun_turu)]):
            tuketim = olcek * oran
            uretim = trafo["panel_kw"] * gunes_pu(adim)
            net = tuketim - uretim
            v_orta = 248 - 25 * net / kva
            satirlar.append({
                "sehir": trafo["sehir"], "trafo_no": trafo["trafo_no"],
                "gun": gun, "gun_turu": gun_turu, "adim": adim, "saat": saat(adim),
                "tuketim_kw": round(tuketim, 2), "uretim_kw": round(uretim, 2),
                "net_kw": round(net, 2), "v_max_v": round(v_orta + 2, 1),
                "v_min_v": round(v_orta - 6 - 15 * max(net, 0) / kva, 1),
            })
    return satirlar


def ayar(sehir, yayginlik, kiyi_kontrolu):
    return {
        "sehir": sehir, "tohum": sehir, "sozlesme_surumu": SOZLESME_SURUMU,
        "sahte": True, "referans_enlem": REF_ENLEM, "referans_boylam": REF_BOYLAM,
        "panel_yayginligi": round(yayginlik, 3), "kiyi_kontrolu": kiyi_kontrolu,
    }


def csv_yaz(yol, sutunlar, satirlar):
    with open(yol, "w", encoding="utf-8", newline="") as f:
        yazici = csv.DictWriter(f, fieldnames=sutunlar, lineterminator="\n")
        yazici.writeheader()
        yazici.writerows(satirlar)


def sehir_uret(sehir, segmentler):
    """Bir sahte şehrin tablolarını üretir; aynı tohum (ve kıyı dosyası) aynı tabloları verir."""
    rng = random.Random(sehir)
    yayginlik = rng.uniform(*PANEL_YAYGINLIGI)
    trafolar = [
        trafo_satiri(rng, sehir, no, yayginlik, segmentler)
        for no in range(1, TRAFO_SAYISI + 1)
    ]
    olculu_sayi = rng.randint(OLCULU_MIN, OLCULU_MAX)
    olculu_nolar = set(rng.sample(range(TRAFO_SAYISI), olculu_sayi))
    tahminler = [
        tahmin_satiri(rng, t, i in olculu_nolar, olculu_sayi)
        for i, t in enumerate(trafolar)
    ]
    kac_ev = [kac_ev_satiri(rng, t, tm) for t, tm in zip(trafolar, tahminler)]
    oranlar = arketip_oranlari()
    yuk = [
        satir
        for t, tm in zip(trafolar, tahminler) if tm["olculdu"]
        for satir in yuk_satirlari(t, tm, oranlar)
    ]
    return {
        "trafolar": trafolar, "tahmin": tahminler, "kac_ev": kac_ev,
        "arketipler": arketip_satirlari(sehir, oranlar), "yuk_5dk": yuk,
        "ayar": ayar(sehir, yayginlik, segmentler is not None),
    }


def sehir_yaz(sehir, tablolar):
    klasor = CIKTI_KOK / f"sehir-{sehir:03d}"
    klasor.mkdir(parents=True, exist_ok=True)
    csv_yaz(klasor / "trafolar.csv", TRAFOLAR_SUTUN, tablolar["trafolar"])
    csv_yaz(klasor / "tahmin.csv", TAHMIN_SUTUN, tablolar["tahmin"])
    csv_yaz(klasor / "kac_ev.csv", KAC_EV_SUTUN, tablolar["kac_ev"])
    csv_yaz(klasor / "arketipler.csv", ARKETIP_SUTUN, tablolar["arketipler"])
    csv_yaz(klasor / "yuk_5dk.csv", YUK_SUTUN, tablolar["yuk_5dk"])
    with open(klasor / "ayar.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(tablolar["ayar"], f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    segmentler = kiyi_segmentleri()
    if segmentler is None:
        print(f"UYARI: {KIYI_DOSYASI.name} yok; yalnız 'kuzeye en çok "
              f"{KUZEY_MAX_M} m' kuralı (bazı trafolar denize düşebilir).")
    for sehir in SEHIRLER:
        tablolar = sehir_uret(sehir, segmentler)
        sehir_yaz(sehir, tablolar)
        print(f"sehir-{sehir:03d}: {len(tablolar['trafolar'])} trafo")


if __name__ == "__main__":
    main()
