# Civan için istekler

Burası Civan'ın kutusu; yalnız o işler. Kalıp için [README](README.md).

## BİLGİ 31 Eki 13:33 — karar masasından — sözleşme ve üretici main'de; panel yaygınlığı %3–25
Ne: (1) Sözleşme (`docs/data/tablo-bicimi.md`, PR #4) ve gerçek şehir üreticisi (`src/sehir_uret.py`, PR #6) main'e birleşti; Can'ın `profiller.py` ve `sinav.py` de main'de. Kartındaki "birleşene kadar dalda" notu geçersiz, sözleşmeyi main'den oku. İstersen haritayı gerçek şehirle de deneyebilirsin: `python3 src/sehir_uret.py 1` → `data/synthetic/sehir-001/` (EAC Excel'i `data/raw/eac-profil-siniflari/KAYNAK.txt` adresinden indirilmiş olmalı; Lefkoşa ışınım dosyası yoksa yapay ışınımla üretir, `ayar.json` yazar). Harita `cevap_anahtari.csv`'yi okumaz, hatırlatma.
(2) [ADR-0006](../decisions/adr-0006-panel-yayginligi-bugunun-kibrisi.md): Faz 1 şehirlerinde panel yaygınlığı %10–50 → **%3–25** (bugünün Kıbrıs'ı; Kıb-Tek 2023'te güneş üretimi toplamın %5,8'i). Sahte şehirlerinde `panel_sayisi` konut abonelerinin %3–25'i, `panel_kw` ≈ panel sayısı × 4–6,5 kW olsun ki harita bugünkü Kıbrıs'a benzesin; 20 gerçek şehir de bu aralıkla yeniden üretiliyor (BUILD oturumu).
(3) Sözleşmede küçük düzeltmeler oldu: `kva` etiketi varsayım; `kac_ev_tavan` = 1 ve `kac_ev_sinir` tanımları §3'te güncel; `ayar.json` da LF olacak. Harita için değişen sütun yok.
Senden beklenen: bir şey yapman gerekmiyor; sahte veride yaygınlık aralığını uygula, PR'ını açınca ben incelerim (sonucu bu kutuya yazarım).
Durum: bilgi

## KARAR 31 Eki 15:18 — volkan.md'deki "gerçek şehirlerde trafolar denize düşüyor" isteğine
Karar: Evet; `src/sehir_uret.py` `konum()` döngüsüne "karada mı" koşulu girer: senin `app/ornek_veri.py`'deki `kiyi_segmentleri()` + `karada()` olduğu gibi (docstring'de "Civan, app/ornek_veri.py" atfıyla), kıyı dosyası yoksa bugünkü 400 m kuralı + uyarı, `ayar.json`'a `kiyi_kontrolu`. Üretici sürüm 1.2 ile birlikte (fatura sütunu, mahalle çarpanı, bayramlar); şehirler o zaman yeniden üretilir. BUILD kıyı dosyasını KAYNAK.txt'deki komutla indirir.
Neden: Haritada denizdeki trafo ilk göze batan hata; ölçümün (otel %31) doğru. Kod senin dosyandan kopyalanır, sen `src/`'ye dokunmazsın.
Senden beklenen: hiçbir şey. (ana oturum: BUILD.)
Durum: bilgi — iş ana oturumda

## KARAR 31 Eki 15:18 — volkan.md'deki "sözleşme 1.2: gerçek veri şehir no 800–899 haritada nasıl etiketlensin?" isteğine
Karar: 800–899 → şerit "GERÇEK ÖLÇÜM — <veri_kaynagi> (Kıbrıs değil)"; kaynak adı `ayar.json` `veri_kaynagi` anahtarından (ör. "EDP Oviedo 2018, Mendeley CC BY"), anahtar yoksa "gerçek ölçüm verisi". Sözleşme 1.2'ye "800–899 gerçek veri; `ayar.json`'da `veri_kaynagi` ve `veri_turu` = `gercek` zorunlu" satırını BUILD ekler. Not: şu an gerçek veri klasörü üretilmiyor (BUILD İspanya'yı ham veriden koştu, PR #10); bu kural ileride lazım olursa diye, acil değil. `yillik_tuketim_mwh` sahte üreticiye 1.2 gelince, evet.
Neden: Etiket kuralı kartında, aralık sözleşmede; yanlış "farazi" etiketi jüri önünde dürüstlük sorunu olur.
Senden beklenen: `app/harita.py` `etiket()`'e üçüncü dal (tek satır), PR #9'dan sonra doğrudan main; sözleşme 1.2 PR'ı açılınca onay için bak (Can ya da sen).
Durum: bekliyor
