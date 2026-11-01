"""Modelin eski sürümleri: depodaki commit'ten src/ çıkarılır, canlı motor (canli.py) o sürümün koduyla ayrı süreçte koşar.

Kod kopyalanmaz: her sürüm git tarihçesinden olduğu gibi alınır (git archive), geçici klasöre yazılır, veri klasörü bağlanır.
Bu modül bilerek canli.py'yi en üstte içe aktarmaz: ayrı süreç önce CANLI_SRC'yi ayarlamalı, sonra canli.py'yi yüklemeli.
"""

import hashlib
import io
import multiprocessing as mp
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import threading
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
ONBELLEK = Path(tempfile.gettempdir()) / "trafo-model-surumleri"

# Ana daldaki birleşmelerden (git log --first-parent -- src/sablon.py src/kac_ev_olasilik.py src/tepe.py).
SURUMLER = [
    dict(anahtar="guncel", ad="Güncel", commit=None,
         aciklama="Yük haritası B-Y2: konut yaz eğimi 20 Kıbrıs evinden (PR #39). Panelde yeşilde güven şartı yok "
                  "(ADR-0019), güvenli uçlar."),
    dict(anahtar="by2-oncesi", ad="1 Kasım 10:22 · B-Y2 öncesi", commit="f51e434",
         aciklama="Yük haritası ön sürüm: konut yaz eğimi EAC eğrilerinden; tepe saati ve akşam gerilimi var. Panel "
                  "güncelle aynı."),
    dict(anahtar="yuk-ilk", ad="1 Kasım 01:59 · yük haritası ilk sürüm", commit="ff8836f",
         aciklama="Yük haritası ilk kez: yılın tepesi ve akşam gerilimi (PR #24, #26, #29). Panelde yeşil için "
                  "güven şartı var (ADR-0019 öncesi)."),
    dict(anahtar="faz7", ad="31 Ekim 23:33 · kalibrasyon sonrası", commit="0f736cc",
         aciklama="Öğlen yükü aralığı gerçek İspanya verisine göre 1,47 kat genişletildi (Faz 7). Yük haritası yok."),
    dict(anahtar="sunum-v1", ad="31 Ekim 21:33 · sunum v1", commit="sunum-v1",
         aciklama="Faz 1–3 bittiği hâl: öğlen yükü aralığı kalibrasyonsuz, yük haritası yok."),
]

_kilit = threading.Lock()
_havuzlar = {}


def surum(anahtar):
    return next(s for s in SURUMLER if s["anahtar"] == anahtar)


def _git(*arg):
    return subprocess.run(["git", "-C", str(KOK), *arg], capture_output=True, check=True).stdout


def kullanilabilir(s):
    """Güncel her zaman; eski sürüm için git ve commit gerekir. -> (bool, neden)."""
    if s["commit"] is None:
        return True, ""
    try:
        _git("rev-parse", "--verify", f"{s['commit']}^{{commit}}")
        return True, ""
    except (OSError, subprocess.CalledProcessError):
        return False, "bu bilgisayarda git ya da o commit yok"


def _bag_mi(yol):
    """Sembolik bağlantı ya da Windows klasör bağlantısı (junction)."""
    junction = getattr(os.path, "isjunction", None)  # Python 3.12+
    return yol.is_symlink() or bool(junction and junction(yol))


def _veri_bagla(hedef):
    """hedef/data bu depo kopyasının data klasörünü göstersin; göstermiyorsa yenilenir (TEST, KARAR 10:34).
    Windows'ta sembolik bağlantı geliştirici modu ister; olmazsa klasör bağlantısı (junction, yönetici istemez)."""
    bag, dogru = hedef / "data", (KOK / "data").resolve()
    if _bag_mi(bag) and bag.resolve() == dogru:
        return
    if _bag_mi(bag):
        try:
            bag.unlink()
        except OSError:  # Windows junction
            os.rmdir(bag)
    elif bag.exists():
        raise RuntimeError(f"{bag} bağlantı değil, gerçek klasör; elle silin")
    try:
        bag.symlink_to(dogru, target_is_directory=True)
    except OSError:
        if os.name != "nt":
            raise
        import _winapi
        _winapi.CreateJunction(str(dogru), str(bag))


def klasor(s):
    """Sürümün src/'si geçici klasörde; ilk çağrıda çıkarılır. Klasör her depo kopyasına ayrı (commit + kopya yolu):
    eski kod KOK/data okur, başka bir kopyanın verisine bağlanmasın. Veri bağlantısı her çağrıda doğrulanır."""
    tam = _git("rev-parse", f"{s['commit']}^{{commit}}").decode().strip()
    kopya = hashlib.sha1(str(KOK.resolve()).encode("utf-8")).hexdigest()[:8]
    hedef = ONBELLEK / f"{tam[:12]}-{kopya}"
    with _kilit:
        if not (hedef / "src" / "sablon.py").exists():
            gecici = ONBELLEK / f".{tam[:12]}-{kopya}-{os.getpid()}"
            gecici.mkdir(parents=True, exist_ok=True)
            with tarfile.open(fileobj=io.BytesIO(_git("archive", tam, "src")), mode="r:") as arsiv:
                try:
                    arsiv.extractall(gecici, filter="data")
                except TypeError:  # filter parametresi olmayan eski Python
                    arsiv.extractall(gecici)
            if not (hedef / "src" / "sablon.py").exists():
                gecici.rename(hedef)
            else:  # başka bir süreç önce çıkardı
                shutil.rmtree(gecici, ignore_errors=True)
        _veri_bagla(hedef)
    return hedef


MODEL_MODULLERI = ("canli", "sablon", "kac_ev", "kac_ev_olasilik", "tepe", "trafo_bos_kapasite", "profiller")


def _baslat(src):
    """Ayrı sürecin ilk işi: canli.py bu sürümün src'sini kullansın. Süreç açılırken ana betik güncel modülleri
    yüklemiş olabilir (spawn ana betiği yeniden içe aktarır); onlar atılır, sürümünkiler yüklensin."""
    os.environ["CANLI_SRC"] = src
    os.environ["CANLI_SIRALI"] = "1"
    for ad in MODEL_MODULLERI:
        sys.modules.pop(ad, None)
    sys.path.insert(0, src)


def _is(sehir_klasoru, olculu):
    import canli  # CANLI_SRC ayarlandıktan sonra
    return canli.tahmin_et_klasor(sehir_klasoru, olculu)


def tahmin_et(s, sehir_klasoru, olculu):
    """Eski sürümle tahmin; her sürümün kendi kalıcı süreci var (ilk çağrı yavaş, sonrakiler ~1–2 sn)."""
    src = str(klasor(s) / "src")
    with _kilit:
        havuz = _havuzlar.get(src)
        if havuz is None:
            havuz = ProcessPoolExecutor(max_workers=1, mp_context=mp.get_context("spawn"),
                                        initializer=_baslat, initargs=(src,))
            _havuzlar[src] = havuz
    return havuz.submit(_is, str(sehir_klasoru), list(olculu)).result(timeout=int(os.environ.get("SURUM_ZAMAN_ASIMI", "300")))
