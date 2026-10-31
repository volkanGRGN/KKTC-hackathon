# 2026-11-01 — Öğlen yükü: panelli abonenin faturası net ise üretim iki kez düşülür (Muhittin 4 madde 4)

**Amaç:** BAŞLA 00:16 madde 4, ADR-0018 m. 7: "fatura × oran + kalibre bant" (K_YUK 1,47) öğlen için üretim yöntemi kalır. Kontrol: panelli abonede öğlen net yükü panelin kendi üretimiyle düşülüyor mu; fatura net ise iki kez düşülüyor mu. Şehir 1–10'da ölç, gerekiyorsa düzelt. BUILD 1 (yük).

## Bugünkü zincir
- `sablon.py` öğlen **brüt** tüketimini tahmin eder (sözleşme: `ogle_min_kw` brüt; ölçülü trafodan `tuketim_kw`); büyüklüğü faturadan (`yillik_tuketim_mwh`, ADR-0007).
- Panel üretimi öğlende **bir kez**, `kac_ev_olasilik.py`'nin yük akışında düşülür (BUILD 2'nin dosyası).
- Üretici faturayı brüt yazıyor (`fatura_mwh`: abone enerjileri × sapma). Deneme şehirlerinde üretim iki kez düşülmüyor.
- Gerçekte Kıb-Tek'in mahsuplaşmalı abone faturası net olabilir (çekilen − verilen). Kıb-Tek'in faturası net mi, çekilen / verilen ayrı mı: **BULAMADIM** (istek metni madde 3 bunu soruyor; uzmana soru).

## Ölçüm (şehir 1–10, üretici 1.3 şehirleri, ölçülmeyen 280 trafo) [Hesap; farazi, gösterim]
Faturayı net yaptım: brüt − panel kW × 1,69 MWh/kWp (yıllık verim: Open-Meteo Lefkoşa 2023–2025, 30° güneye eğik ışınım 2.099–2.127 kWh/m² × PR 0,8 [Yorum]). 400 trafonun 276'sında fatura düştü, ortanca %14, P90 %43, en çok %91.

| Öğlen tahmini | Hepsi: hata ortanca | Sapma | %80 kapsama | Panel > tüketimin %30'u (n 36–41): sapma | Kapsama |
|---|---|---|---|---|---|
| Brüt fatura (bugün) | %10,0 | +%0,2 | %88,2 | −%1,6 | %92,3 |
| **Net fatura, düzeltmesiz** | %13,6 | +%0,1 | %86,8 | **−%24,4** | **%66,7** |
| Net fatura, düzeltmeli (verim doğru) | %10,0 | +%0,2 | %88,2 | −%1,6 | %92,3 |
| Net fatura, düzeltmeli (verim %15 düşük) | %10,7 | −%0,7 | %87,1 | −%2,1 | %95,1 |
| Net fatura, düzeltmeli (verim %15 yüksek) | %10,1 | +%0,6 | %88,9 | −%0,2 | %94,9 |

- Düzeltmesiz net faturada panelsiz trafolar +%7 fazla çıkıyor: oran (öğlen ÷ fatura) panelli ölçülülerden şişiyor.
- **Yılın tepesinde (tepe.py, PR #24) etki daha büyük ve güvensiz yönde:** düzeltmesiz net faturada hata ortanca %6,1 → %16,8, P90 %15,9 → %45,0, kapsama %98 → %72; paneli tüketiminin %30'undan fazlası olan trafolarda tepe **%27 eksik**, gerçeğin P90'ın üstüne çıktığı trafo %36 (önce 0). Düzeltmeyle brüt faturayla birebir.
- Öğlende eksik yük haritayı kırmızıya iter (temkinli, yanlış kırmızı artar); akşamda eksik tepe "yük için boş"u büyütür (güvensiz).

## Karar (BUILD 1, kendi dosyası)
- `sablon.py`: `fatura_mwh()` brüt tüketimi verir; `--fatura-net` (FATURA_NET) faturaya panel kW × `PV_VERIM_MWH_KWP` (1,69) ekler. Varsayılan brüt: deneme şehirleri brüt, Kıb-Tek'in uygulaması bilinmiyor. `tepe.py` aynı fonksiyonu kullanır (`--fatura-net`).
- Varsayılan yol değişmedi: şehir 1–10'da `tahmin.csv` resmi u13 çıktısıyla 10/10 bayt bayt aynı.
- Kıb-Tek verisi gelince ilk soru: mahsuplaşma faturası net mi. Net ise brüt = fatura + yıllık üretim (bu düzeltme); çekilen ve verilen ayrı kayıtlıysa üretim tahmini yerine sayaç kullanılır.

## Kalan
1. Ölçüm cihazı da net ölçer: pilotta trafo başındaki cihaz brüt değil net görür; `sablon.py` ölçülüden brüt (`tuketim_kw`) okuyor. Gerçek ölçümde ölçülü trafonun üretimi (panel kW × o günün ışınımı) geri eklenmeli; bunun hatası ölçülmedi. Faz 10 pilot kartına not.
2. Verim tek sayı (yön, gölge, kirlilik yok) [Yorum]; ±%15 hatada öğlen sapması %1–2.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas 00:55 | sablon (main) | 1–10, net fatura | net faturada üretim iki kez düşülür | panelli (> %30) öğlen −%24, tepe −%27 | `--fatura-net` düzeltmesi; varsayılan brüt |
| 1 Kas 01:00 | sablon + `--fatura-net` | 1–10 | düzeltme brüte döndürür, verim hatasına az duyarlı | birebir; verim ±%15'te sapma ≤ %2 | kabul |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
