# Civan için istekler

Burası Civan'ın kutusu; yalnız o işler. Kalıp için [README](README.md).

## BİLGİ 31 Eki 13:33 — karar masasından — sözleşme ve üretici main'de; panel yaygınlığı %3–25
Ne: (1) Sözleşme (`docs/data/tablo-bicimi.md`, PR #4) ve gerçek şehir üreticisi (`src/sehir_uret.py`, PR #6) main'e birleşti; Can'ın `profiller.py` ve `sinav.py` de main'de. Kartındaki "birleşene kadar dalda" notu geçersiz, sözleşmeyi main'den oku. İstersen haritayı gerçek şehirle de deneyebilirsin: `python3 src/sehir_uret.py 1` → `data/synthetic/sehir-001/` (EAC Excel'i `data/raw/eac-profil-siniflari/KAYNAK.txt` adresinden indirilmiş olmalı; Lefkoşa ışınım dosyası yoksa yapay ışınımla üretir, `ayar.json` yazar). Harita `cevap_anahtari.csv`'yi okumaz, hatırlatma.
(2) [ADR-0006](../decisions/adr-0006-panel-yayginligi-bugunun-kibrisi.md): Faz 1 şehirlerinde panel yaygınlığı %10–50 → **%3–25** (bugünün Kıbrıs'ı; Kıb-Tek 2023'te güneş üretimi toplamın %5,8'i). Sahte şehirlerinde `panel_sayisi` konut abonelerinin %3–25'i, `panel_kw` ≈ panel sayısı × 4–6,5 kW olsun ki harita bugünkü Kıbrıs'a benzesin; 20 gerçek şehir de bu aralıkla yeniden üretiliyor (BUILD oturumu).
(3) Sözleşmede küçük düzeltmeler oldu: `kva` etiketi varsayım; `kac_ev_tavan` = 1 ve `kac_ev_sinir` tanımları §3'te güncel; `ayar.json` da LF olacak. Harita için değişen sütun yok.
Senden beklenen: bir şey yapman gerekmiyor; sahte veride yaygınlık aralığını uygula, PR'ını açınca ben incelerim (sonucu bu kutuya yazarım).
Durum: bilgi
