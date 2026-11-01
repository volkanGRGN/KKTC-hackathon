"""Modelin eski sürümleri: depodaki commit'ten src/ çıkarılır, canlı motor (canli.py) o sürümün koduyla ayrı süreçte koşar.

Kod kopyalanmaz: her sürüm git tarihçesinden olduğu gibi alınır (git archive), geçici klasöre yazılır, veri klasörü bağlanır.
Bu modül bilerek canli.py'yi en üstte içe aktarmaz: ayrı süreç önce CANLI_SRC'yi ayarlamalı, sonra canli.py'yi yüklemeli.
"""

import io
import multiprocessing as mp
import os
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
         aciklama="Yeşilde güven şartı yok (ADR-0019), güvenli uçlar; yük haritası: yılın tepesi, akşam gerilimi, "
                  "tepe saati."),
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


def klasor(s):
    """Sürümün src/'si geçici klasörde; ilk çağrıda çıkarılır. Veri klasörü bağlantı (eski kod KOK/data okur)."""
    tam = _git("rev-parse", f"{s['commit']}^{{commit}}").decode().strip()
    hedef = ONBELLEK / tam[:12]
    if (hedef / "src" / "sablon.py").exists():
        return hedef
    with _kilit:
        gecici = ONBELLEK / f".{tam[:12]}-{os.getpid()}"
        gecici.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(_git("archive", tam, "src")), mode="r:") as arsiv:
            arsiv.extractall(gecici, filter="data")
        (gecici / "data").symlink_to(KOK / "data", target_is_directory=True)
        if not (hedef / "src" / "sablon.py").exists():
            gecici.rename(hedef)
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
