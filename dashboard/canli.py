"""Canlı tahmin motoru: seçilen ölçülü trafolarla modeli o an kurar, gerisini tahmin eder (Streamlit'siz).

Ürünün kendi kodunu çağırır, kopyalamaz:
  öğlen en düşük yük (panel katmanının girdisi)  src/sablon.py calistir()
  renk, kaç ev (panel katmanı)                    src/kac_ev_olasilik.py trafo_cek(), sehir_calistir() ile aynı kural
  yılın tepesi, doluluk (yük haritası)            src/tepe.py sehir_calistir(), geçici klasörde (şehir klasörüne yazmaz)
Model yalnız ölçülü seçilen trafoların ölçümünü görür: sablon.calistir ve tepe.sehir_calistir bunu kendileri süzer.
Resmi 12'li seçimle (sablon.ogretici_sec) sonuç main'deki tahmin.csv ve tepe.csv ile birebir (sehir-031'de denendi).
cevap_anahtari.csv'yi yalnız sinav_kiyasi() okur (sınav görünümü, gösterim); modele girmez.
"""

import contextlib
import csv
import inspect
import io
import math
import os
import random
import sys
import tempfile
import threading
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

KOK = Path(__file__).resolve().parent.parent
# Modelin hangi sürümü: CANLI_SRC verilmişse o klasördeki src (eski sürüm, surumler.py çıkarır), yoksa depodaki src.
SRC = Path(os.environ.get("CANLI_SRC") or KOK / "src")
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import sablon  # noqa: E402

EN_AZ_OLCULU = 3  # 1 ölçülüyle model kurulmuyor; 2'de bir-dışarıda bant tek artıktan, anlamsız dar
GUVENILIR_OLCULU = 8  # bunun altında %80 aralık birkaç artıktan çıkıyor [Yorum]; ürünün tasarımı 12
GERCEK_MIN_KW = 1.0  # sinav.py ile aynı: gerçek bunun altındaysa göreli hata anlamsız

_kilit = threading.Lock()  # tepe.sehir_calistir sablon.ogretici_sec'i çağırıyor; geçici değiştirme tek iş parçacığında
_havuz = None
_tepe_girdi = None


# ---------- şehir ----------

def sehir_hazirla(klasor):
    """Şehrin Kıb-Tek'in bildiği tablosu ve her trafonun ölçülürse göreceğimiz değeri.
    olcum sözlüğü bütün trafoları taşır ama modele yalnız seçilenler verilir (sablon.calistir süzer)."""
    klasor = Path(klasor)
    tr, _, X, A = sablon.sehir_oku(klasor)
    yuk = pd.read_csv(klasor / "yuk_5dk.csv", encoding="utf-8",
                      usecols=["trafo_no", "gun", "gun_turu", "adim", "tuketim_kw"])
    olcum = sablon.olcumleri_hazirla(yuk, list(tr["trafo_no"]))
    with open(klasor / "trafolar.csv", encoding="utf-8", newline="") as fh:
        ham = list(csv.DictReader(fh))
    return dict(klasor=klasor, tr=tr, X=X, A=A, olcum=olcum, ham=ham,
                sehir=int(tr["sehir"].iloc[0]), nolar=list(tr["trafo_no"]))


def oneri(h, n=sablon.OLCULU_ANA):
    """Ürünün ölçüm önerisi: tabakalı seçim, resmi koşuyla aynı tohum (sablon.py sehir_calistir)."""
    return [h["nolar"][i] for i in sablon.ogretici_sec(h["tr"], n, f"sec-{h['sehir']}")]


# ---------- öğlen yükü (sablon.py) ----------

def ogle_tahmini(h, olculu_nolar):
    """-> (tahmin tablosu, model özeti). Satırlar sözleşme §5 tahmin.csv ile aynı."""
    sira = {t: i for i, t in enumerate(h["nolar"])}
    secilen = sorted(sira[t] for t in olculu_nolar)
    satirlar, m = sablon.calistir(h["tr"], h["X"], h["A"], h["olcum"], secilen)
    ozet = dict(k=m["k"], ad=m["ad"], bant=m["bant"],
                arketip_satirlari=sablon.arketip_satirlari(h["sehir"], m),
                loo_hata=float(np.median(np.abs(np.exp(-m["loo_log_artik"]) - 1))))
    return pd.DataFrame(satirlar), ozet


# ---------- renk (kac_ev_olasilik.py) ----------

def _renk_bir(arg):
    """Bir trafo: kac_ev_olasilik.sehir_calistir döngüsünün gövdesi, dosya yazmadan. Ayrı süreçte koşabilir."""
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    import kac_ev as ke
    import kac_ev_olasilik as ko
    r, t = arg
    tr = {k: (r[k] if k in ("trafo_no", "kablo", "bolge", "montaj") else ke.sayi(r[k])) for k in r}
    rng = random.Random(f'olasilik-{r["sehir"]}-{r["trafo_no"]}')
    s = ko.trafo_cek(tr, t, rng)
    aday = max(0, int(tr["abone_konut"] - tr["panel_sayisi"]))
    p_bugun = sum(b for b, _, _ in s) / len(s)
    p_iki = sum(i for _, _, i in s) / len(s)
    kac = [min(k, aday) for _, k, _ in s]
    if p_bugun >= ko.KIRMIZI_P:
        renk = "kirmizi"
    elif p_iki >= ko.YESIL_P and (not getattr(ko, "YESIL_GUVEN_SARTI", True) or t["guven"] == "yuksek"):
        renk = "yesil"
    else:
        renk = "sari"
    kural = math.floor(max(0.0, 0.4 * tr["kva"] - tr["panel_kw"]) / ke.YENI_PANEL_KW)
    return dict(trafo_no=r["trafo_no"], renk=renk, p_bugun_asar=round(p_bugun, 3), p_iki_ev_sigar=round(p_iki, 3),
                kac_ev_karamsar=ko.nicel(kac, 0.1), kac_ev_orta=ko.nicel(kac, 0.5), kac_ev_iyimser=ko.nicel(kac, 0.9),
                pv_uc=ko.pv_uc(renk, p_bugun) if hasattr(ko, "pv_uc") else "", kural40_ev=kural, aday=aday)


def _havuz_al():
    global _havuz
    if _havuz is None:
        _havuz = ProcessPoolExecutor(max_workers=max(1, min(8, (os.cpu_count() or 2) - 1)))
    return _havuz


def _isinma():
    """Havuz sürecinde modülleri önceden yükler (ilk tıklamada beklenmesin)."""
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    import kac_ev_olasilik  # noqa: F401
    return True


def isit():
    """Süreç havuzunu ve tepe girdilerini arka planda hazırlar; beklemez. Sayfa açılınca bir kez çağrılır."""
    if os.environ.get("CANLI_SIRALI"):
        return
    try:
        havuz = _havuz_al()
        for _ in range(havuz._max_workers):
            havuz.submit(_isinma)
    except Exception:
        pass
    if tepe_var():
        threading.Thread(target=_tepe_hazir, daemon=True).start()


def renk_tahmini(h, tahmin):
    """Her trafo için renk ve kaç ev; tahmin tablosundaki öğlen yükü bandından (ölçülüde ölçülenden)."""
    t_sozluk = {r["trafo_no"]: {k: ("" if pd.isna(v) else str(v)) for k, v in r.items()}
                for r in tahmin.to_dict("records")}
    isler = [(r, t_sozluk[r["trafo_no"]]) for r in h["ham"]]
    if os.environ.get("CANLI_SIRALI"):  # eski sürüm süreci: iç içe süreç havuzu açılmaz (kapanışta birbirini bekler)
        return pd.DataFrame([_renk_bir(i) for i in isler])
    try:
        sonuc = list(_havuz_al().map(_renk_bir, isler))
    except Exception:  # süreç havuzu açılamazsa (ör. kısıtlı ortam) sırayla, aynı sonuç
        sonuc = [_renk_bir(i) for i in isler]
    return pd.DataFrame(sonuc)


# ---------- yılın tepesi (tepe.py) ----------

def tepe_var():
    """Bu sürümde yük haritası (src/tepe.py) var mı? İlk kez 1 Kasım 01:58'de (PR #24)."""
    return (SRC / "tepe.py").exists()


def _tepe_hazir():
    global _tepe_girdi
    if _tepe_girdi is None:
        import tepe
        eac, hava = tepe.eac_hazirla(), tepe.hava_oku()
        egim, _ = tepe.egimler(eac, hava)
        _tepe_girdi = (tepe, eac, hava, egim)
    return _tepe_girdi


def tepe_tahmini(h, olculu_nolar, tahmin, model):
    """tepe.sehir_calistir'i geçici klasörde koşar: trafolar / ayar / yük bağlantı, tahmin ve arketip canlı modelden.
    Ölçülü küme sablon.ogretici_sec'in yerine geçici olarak verilir (tepe.py kendi içinde onu çağırıyor).
    Kıb-Tek tepe kayıtları okunmaz (kibtek=False): canlı görünümde tek bilgi kaynağı seçilen ölçümler."""
    tepe, eac, hava, egim = _tepe_hazir()
    sira = {t: i for i, t in enumerate(h["nolar"])}
    secilen = sorted(sira[t] for t in olculu_nolar)
    with tempfile.TemporaryDirectory(prefix="canli-tepe-") as gecici, _kilit:
        g = Path(gecici)
        for ad in ("trafolar.csv", "ayar.json", "yuk_5dk.csv"):
            os.symlink(h["klasor"] / ad, g / ad)
        sablon.csv_yaz(g / "tahmin.csv", sablon.TAHMIN_SUTUNLARI, tahmin.to_dict("records"))
        sablon.csv_yaz(g / "arketipler.csv", ["sehir", "arketip", "arketip_adi", "gun_turu", "adim", "oran"],
                       model["arketip_satirlari"])
        eski = sablon.ogretici_sec
        sablon.ogretici_sec = lambda *_a, **_k: list(secilen)
        try:
            ek = {"kibtek": False} if "kibtek" in inspect.signature(tepe.sehir_calistir).parameters else {}
            with contextlib.redirect_stdout(io.StringIO()):
                satirlar, _ = tepe.sehir_calistir(g, eac, hava, egim, **ek)
        finally:
            sablon.ogretici_sec = eski
    return pd.DataFrame(satirlar)


# ---------- hepsi ----------

def tahmin_et(h, olculu_nolar):
    """Seçilen ölçülerle üç katmanın tahmini. En az EN_AZ_OLCULU ölçülü gerekir; azsa None."""
    olculu_nolar = [t for t in h["nolar"] if t in set(olculu_nolar)]
    if len(olculu_nolar) < EN_AZ_OLCULU:
        return None
    tahmin, model = ogle_tahmini(h, olculu_nolar)
    renk = renk_tahmini(h, tahmin)
    tablo = (h["tr"][["sehir", "trafo_no", "enlem", "boylam", "kva", "bolge", "montaj", "panel_kw", "abone_konut"]]
             .merge(tahmin.drop(columns=["sehir"]), on="trafo_no")
             .merge(renk, on="trafo_no"))
    if tepe_var():
        tepe_df = tepe_tahmini(h, olculu_nolar, tahmin, model)
        tablo = tablo.merge(tepe_df.drop(columns=["sehir", "olculdu", "guven"]), on="trafo_no")
        tablo["doluluk"] = tablo["tepe_kva"] / tablo["kva"]
        tablo["doluluk_temkinli"] = tablo["tepe_kva_p90"] / tablo["kva"]
    model = {k: v for k, v in model.items() if k != "arketip_satirlari"}
    model["yuk_var"] = tepe_var()
    return dict(tablo=tablo, model=model, olculu=olculu_nolar)


def tahmin_et_klasor(klasor, olculu_nolar):
    """Ayrı süreçte (eski sürüm) çağrılmak için: şehri hazırlar ve tahmin eder."""
    return tahmin_et(sehir_hazirla(klasor), olculu_nolar)


# ---------- sınav görünümü ----------

def sinav_kiyasi(klasor, tablo):
    """Ölçülmeyen trafolarda tahmin ↔ benzetimin bildiği gerçek (cevap_anahtari.csv). Yalnız farazi şehirde var.
    Tanımlar sinav.py ile aynı: öğlen ve tepe göreli hata (gerçek ≥ 1 kW), dolu = kac_ev_gercek = 0 (aday > 0).
    -> (özet, trafo başına gerçek tablosu) ya da (None, None)."""
    yol = Path(klasor) / "cevap_anahtari.csv"
    if not yol.exists():
        return None, None
    cevap = pd.read_csv(yol, encoding="utf-8", dtype={"trafo_no": str})
    sutunlar = ["trafo_no", "ogle_min_kw", "kac_ev_gercek", "kac_ev_aday"]
    sutunlar += [c for c in ("tepe_yil_kw", "tepe_yil_kva") if c in cevap]
    g = cevap[sutunlar].rename(columns={"ogle_min_kw": "gercek_ogle_kw", "kac_ev_gercek": "gercek_kac_ev",
                                        "tepe_yil_kw": "gercek_tepe_kw", "tepe_yil_kva": "gercek_tepe_kva"})
    k = tablo.merge(g, on="trafo_no", how="left")
    if "gercek_tepe_kva" in k:
        k["gercek_doluluk"] = k["gercek_tepe_kva"] / k["kva"]
    o = k[k["olculdu"] == 0]
    ozet = dict(olculmeyen=len(o))
    ogle = o[o["gercek_ogle_kw"] >= GERCEK_MIN_KW]
    if len(ogle):
        h = (ogle["ogle_min_kw"] - ogle["gercek_ogle_kw"]).abs() / ogle["gercek_ogle_kw"]
        ozet.update(ogle_hata=float(h.median()), ogle_hata_p90=float(h.quantile(0.9)),
                    ogle_kapsama=float(((ogle["gercek_ogle_kw"] >= ogle["ogle_min_kw_p10"])
                                        & (ogle["gercek_ogle_kw"] <= ogle["ogle_min_kw_p90"])).mean()))
    if "gercek_tepe_kw" in o and "tepe_kw" in o:
        tp = o[o["gercek_tepe_kw"] >= GERCEK_MIN_KW]
        if len(tp):
            h = (tp["tepe_kw"] - tp["gercek_tepe_kw"]).abs() / tp["gercek_tepe_kw"]
            ozet.update(tepe_hata=float(h.median()), tepe_hata_p90=float(h.quantile(0.9)),
                        tepe_kapsama=float(((tp["gercek_tepe_kw"] >= tp["tepe_kw_p10"])
                                            & (tp["gercek_tepe_kw"] <= tp["tepe_kw_p90"])).mean()))
        if "gercek_doluluk" in o:
            gercek_dolu = o["gercek_doluluk"] >= 0.8
            uyari = o["doluluk_temkinli"] >= 0.8
            ozet.update(dolu80=int(gercek_dolu.sum()), dolu80_yakalanan=int((gercek_dolu & uyari).sum()),
                        dolu80_uyari=int(uyari.sum()))
    adayli = o[o["kac_ev_aday"] > 0]
    yesil = adayli[adayli["renk"] == "yesil"]
    ozet.update(yesil=len(yesil), yanlis_yesil=int((yesil["gercek_kac_ev"] == 0).sum()),
                dolu=int((adayli["gercek_kac_ev"] == 0).sum()),
                kural_yanlis=int(((adayli["kural40_ev"] >= 1) & (adayli["gercek_kac_ev"] == 0)).sum()))
    return ozet, k
