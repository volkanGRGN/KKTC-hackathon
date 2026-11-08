# 2026-11-01 — Üretici 1.6: konut ve yurt yaz eğimi 20 Kıbrıs evine çapalı; yeni sınav şehirleri 51–60 (BUILD 1)

**Amaç:** B-Y2 (PR #39) modelin konut yaz eğimini 20 gerçek Kıbrıs evinden aldı (0,065/°C); üretici ise hâlâ 0,045 [Yorum] ile kuruyordu. Farazi sınav gerçek yöne gidişi "hata" sayıyordu (41–50: tepe hatası %11,4, işaretli +%11,1, konut +%13,6). Volkan (1 Kasım sabahı): yanlı şehirleri bırakıp üreticiyi düzeltmek, dalda şimdi. Bu dal yalnız üreticiyi değiştirir; model (`tepe.py`, `sablon.py`) değişmedi.

**Etiket:** farazi şehir, gösterim. [Hesap: BUILD 1 koşusu]; resmi rakam KARAR / TEST'in Mac koşusu. Ayar yalnız 1–10'da yapılmadı bile: eğim veriden geldi, 1–10 yalnız çapaların tutup tutmadığını görmek için; sınav 51–60 (hiç üretilmemiş tohumlar) bir kez.

## Ne değişti (`src/sehir_uret.py`)
- `SICAKLIK_BETA['yaz']['konut']` ve `['yurt']`: 0,045 → **0,060**. Öbür sınıflar ve kış değişmedi (Kıbrıs'a özgü veri yok).
- Dayanak: Can'ın 20 konut prosumer analizi, yaz akşamı tepesinin akşam (19–22) sıcaklığına eğimi Temmuz ölçeğinde 0,065/°C (bootstrap P10–P90 0,056–0,075) [Hesap: Can, `docs/log/2026-11-01-can-eszamanlilik.md`; Zenodo 23043383]. Üretici ise günün ortalama sıcaklığının ay ortalamasından farkını kullanır. Lefkoşa 2015–2025 Haziran–Eylül'de (1.342 gün) akşam sıcaklık farkı günlük ortalama farkının **0,923** katı (r 0,94; yalnız Temmuz 0,908) → 0,065 × 0,92 ≈ **0,060** [Hesap: BUILD 1, yıl-ay ortalamasına göre fark, üreticiyle aynı tanım].
- `URETICI_SURUMU` 1.6; başlık açıklaması. Rastgele akış aynı (eğim rastgele sayı çekmez).
- Eğim trafo boyutuna da girer (1.5: tasarım tepesi × (1 + β_yaz · ΔT_tasarım), ΔT_tasarım 5 °C değişmedi): bazı konut / yurt trafolarının gücü bir üst boya çıkar, bu yüzden Nisan dosyaları ve panel cevap anahtarı da değişir.

## Ayar şehirleri 1–10: 1.5 ↔ 1.6 (aynı tohumlar)
| Ölçü | 1.5 | 1.6 | Hedef |
|---|---|---|---|
| Bayt bayt aynı dosya (trafolar, yuk_5dk, yaz, kış, cevap anahtarı) | — | 0 / 10 şehir (her şehirde en az bir trafo değişti) | — |
| Gücü değişen trafo | — | 20 / 400 (şehir konutu 12, yurt 4, köy 3, sulama 1) | — |
| Öğlen en düşük yük (`ogle_min_kw`) değişen | — | 0 | (Nisan tüketimi aynı) |
| Panel cevap anahtarı: `kac_ev_gercek` / `v_max_bugun_v` değişen | — | 22 / 30 | (trafo gücü ve hat) |
| Yılın tepesi 1.6 ÷ 1.5, ortanca | — | konut 1,036; yurt 1,045; köy 1,032; çarşı, otel, sanayi ~1,00 | — |
| Tepe ayı | Temmuz 396, Ocak 4 | aynı | — |
| Yıl tepesi ÷ güç P10 / 50 / 90 | 0,23 / 0,47 / 0,73 | 0,22 / 0,47 / 0,73 | Malta 0,13 / 0,42 / 0,74 |
| Gücü aşan | 3 (%0,8) | 3 (%0,8) | Malta %1,5 |
| Yıl pencerelerinde 207 V altı | 2 (%0,5) | 2 (%0,5) | ≤ %1 |
| En düşük gerilim | 201,1 V | **199,8 V** (sehir-001 T22: köy, 250 kVA, 799 m, mahalle çarpanı 2,6) | ≥ 200 V |

Yük modeli (ana dal `tepe.py`, B-Y2), aynı 1–10, ölçülmeyen 280 trafo:

| | 1.5 | 1.6 |
|---|---|---|
| Tepe hata ortanca / P90 | %12,3 / %23,2 | %8,9 / %21,4 |
| İşaretli (+ fazla tahmin) | +%11,9 | +%7,7 |
| Konut / yurt / çarşı / sanayi işaretli | +%15,5 / +%14,4 / +%16,3 / +%11,8 | +%10,2 / +%5,9 / +%11,5 / +%11,2 |
| %80 bant; gerçek P90 üstü | %95,4; 1 | %97,5; 0 |
| Saat ±60 dk; iki adaydan biri; dönem | %49,3; %59,6; %70,0 | %46,4; %55,4; %66,4 |
| Doluluk hatası ortanca (puan); ≥ %80 dolu yakalanan / uyarı | 4,6; 17 / 17, 139 | 3,2; 19 / 19, 120 |
| Akşam: 207 V altı yakalanan; "yeterli"de yanlış; uyarı | 1 / 1; 217'de 0; 63 | 2 / 2; 223'te 0; 57 |

## Sınav şehirleri 51–60 (1.6, bir kez; hiçbir şey ayarlanmadı)
| Ölçü | 41–50 (1.5; KARAR 10:26, bilgi) | **51–60 (1.6)** |
|---|---|---|
| Yılın tepesi hata ortanca / P90 | %11,4 / %23,9 | **%7,9 / %17,0** |
| İşaretli (konut) | +%11,1 (+%13,6) | **+%5,0 (+%7,5)** |
| %80 bant; gerçek P90 üstü | %95,0; 0 | %99,6; 0 |
| Saat ±60 dk; iki adaydan biri; dönem | %47; %59; — | %49,3; %59,6; %63,9 |
| ≥ %80 dolu: yakalanan / uyarı | 12 / 12, 124 | 8 / 8, 110 |
| Akşam: 207 V altı yakalanan; "yeterli"de yanlış; uyarı | 2 / 2; 211'de 0; 69 | 2 / 2; 230'da 0; 50 |
| Üretici çapası: tepe ÷ güç P10 / 50 / 90; aşan; 207 V altı; en düşük | — | 0,25 / 0,45 / 0,69; %0,8; %0,8; **199,0 V** |

`sinav.py` (Can'ın, ana dal) 51–60:
- **faz1:** tipler GEÇTİ; v_max > 259 V 48/400 GEÇTİ; Nisan en düşük 220,6 V GEÇTİ; **üretim süresi KALDI** (en uzun 119,8 sn): dört paralel koşu ve başka oturumların yükü; eğim değişikliği hesap eklemez, boş makinede ölçülmeli (1.5'te de aynı durum, Can'ın günlüğü).
- **faz2:** arketip %82,1, öğlen hatası %12,5 / P90 %27,2 (41–50'de %30,1 KALDI'ydı; farklı şehirler), şehirler arası 0,75, düşük güven %7,1 — hepsi GEÇTİ; farazi kapsama %83,9; saf fatura (bilgi) model %9 / %8 yüksek; yük bölümü yukarıdakiyle birebir.
- **faz3 (panel):** yanlış yeşil 0/52 (en kötü şehir 0/7) GEÇTİ; dolu trafoya "yer var": %40 kuralı 38/57, model 0/57; bayrak isabeti %68 (17/25) GEÇTİ; kaç ev orta 2 GEÇTİ; kırmızı kovası %58,2.

## Bulgular
1. **+** Farazi sınav artık gerçek yöne gidişi daha az cezalandırıyor: 1–10'da işaretli sapma +%11,9 → +%7,7 (konut +%15,5 → +%10,2), 51–60'ta +%5,0; gerçek P90 üstü 0, dolu trafo kaçmıyor, akşam gerilimi "yeterli"de yanlış yok.
2. **−** Üretici gerilim sağlaması "en düşük ≥ 200 V" kıl payı kalıyor: 1–10'da 199,8 V, 51–60'ta 199,0 V (1.5'te 201,1 V). 207 V altı pay ≤ %1 tutuyor. ADR-0016 m. 3 gereği trafo boyutu ya da hat tasarımı bunu gizlemek için değiştirilmedi; karar KARAR'da.
3. **?** Konutta kalan +%8–10 fazla tahmin eğimle açıklanmıyor: eğimi değişmeyen sanayide de +%11 (1–10). Model ve üretici sıcaklık farkını aynı tanımla alıyor (yılın ayının en sıcak günü − ay ortalaması); üreticinin yaz haftası her şehirde Temmuz'un en sıcak gününü içeriyor [Hesap: 1–10, 10/10]. Aday sebep: ölçülü trafoların Nisan oranı R (1,08–1,16) ev ev gürültüyü de taşıyor [Yorum]; ayrı iş, bu dalda dokunulmadı.
4. **?** Model eğimi 0,065'i günlük ortalama farkına uyguluyor; aynı dönüşümle 0,060 olurdu (akşam ↔ günlük, 0,92). Tanım uyumu için `tepe.py`'de ayrı küçük PR adayı; güvenli yönde %1–2.
5. **?** 20 ev hepsi panelli, ortalamadan büyük (brüt 7,2 MWh ↔ konut ortalaması 3,7), Güney Kıbrıs, 2016 (Can'ın günlüğü). Eğim farazi şehirde sınanamaz (üretici ve model aynı veriden); eğimi gerçek yaz ölçümü sınar (Kıb-Tek tepe kayıtları, pilot).

## Benimsenirse ne değişir
Bütün sınavlar (yük ve panel) 51–60 ile; pano ve sunum rakamları 51–60 / 1.6'ya. İspanya sonuçları değişmez (üreticiden bağımsız).

## Yeniden üretim
```
python3 src/sehir_uret.py 1 10 --cikti <ayar>       # ve 51 60 --cikti <sınav>
python3 src/sablon.py <kök>                          # tam kip (faz2 şehirler arası için)
python3 src/tepe.py <kök> --aralik 51-60
python3 src/kac_ev_olasilik.py <kök> --sehir 51      # her şehir
python3 src/sinav.py faz1|faz2|faz3 <kök> --aralik 51-60
```

## Ek — 11:01: KARAR'ın iki sorusu (hat tasarımı düzeltmesi; kalan fazla tahminin kaynağı)

KARAR: 1.6 sunuma girmez, birleşme sunumdan sonra; PR açık ve güncel kalır.

### 1. "En düşük ≥ 200 V" neden tutmadı
- Tahmin edilen sebep (hat tasarımı eski eğimle) değil: hat tasarımı zaten 0,060'lı tasarım tepesini kullanıyor (`plan` = `tepe` × olcek).
- **Asıl sebep:** trafo gücü gizli mahalle yükünü hesaba katıyor (`gerek = max(Σ plan × marj, Σ tepe × olcek)`, 1.4 kuralı), hat tasarımı katmıyordu (yalnız `plan × marj`); koddaki "hat tasarımı trafoyla aynı tasarım yüküne bakar" notuyla çelişki, 1.5'ten beri. sehir-001 T22: mahalle çarpanı 2,6, trafo büyütülmüş, hat güçlendirilmemiş.
- **Düzeltme:** `hat_dusumu` / `hat_tasarla` aynı kuralı alır: hattın tasarım yükü = max(Σ plan × marj, Σ gizli mahalle yükü).
- 1–10 (1.6 ↔ 1.6 + hat): 6/10 şehir bayt bayt aynı; trafo gücü değişen 0; `kac_ev_gercek` / `v_max_bugun_v` değişen 4 / 4; hat tasarımı ilk / kesit / bölme 330 / 8 / 62 → 327 / 9 / 64; **en düşük 199,8 → 200,9 V**, 207 V altı 2 → 1 (%0,2); yük modeli rakamları aynı.
- **51–60 bir kez daha (KARAR'ın izniyle):** 4/10 şehir değişti, `kac_ev_gercek` 1; **en düşük 199,0 V kaldı**: sehir-055 T36 (köy, 100 kVA, 861 m ABC95, hat iki kez bölünmüş, mahalle 1,09, klima 0,91; tepe ÷ güç 0,59). Hat kuralının kaba düşüm tahmini (düzgün dağılmış yük, I × |z| ÷ 2, en yüklü faz 1,5) bu hatta gerçek düşümü ~16 V az görüyor [Hesap: 246 − 199 = 47 V ↔ 24 V tasarım + ~5 V trafo]. 207 V altı %0,8 (≤ %1). Eşik oynatılmadı, kural sıkılaştırılmadı (ADR-0016 m. 3); karar KARAR'da.
- `sinav.py` 51–60 (düzeltmeli): faz2 ve faz3 önceki koşuyla aynı, bütün maddeler GEÇTİ; faz1 üretim süresi en uzun 80,9 sn, ortanca 29,7 sn (makine yükü). Yük modeli 51–60 rakamları aynı (%7,9 / %17,0, +%5,0, P90 üstü 0, dolu 8/8, akşam 230'da 0 yanlış).

### 2. Kalan fazla tahminin kaynağı (1–10, 1.6 + hat, ölçülmeyen 280, işaretli +%7,7) [Hesap: BUILD 1]
| Aday | Sınama | Sonuç |
|---|---|---|
| Tasarım sıcaklığı (10 yılda bir) ↔ üreticinin hava yılı | model kipi ve ΔT | **Değil:** model `yil` kipinde, ΔT üreticinin aynı hava yılından (ör. sehir-001 Temmuz 2,6 °C = üreticinin penceresi) |
| Üreticinin √N çeşitliliği ↔ modelin Velander c'si | şehir başına c | **Değil:** 10 şehrin 8'inde c = 0; c = 0 şehirlerde +%7,9, c > 0'da +%6,8 |
| Nisan → yaz taşıma (ölçülü oran R) | ölçülü trafolar kendi R'siyle | **Asıl pay:** ölçülüde bile +%5,9. Nisan oranı (14 günün en yükseği ÷ tipik gün) ortanca 1,103; yaz oranı (gerçek yaz tepesi ÷ önsel yaz tepesi) 1,042 (r 0,86) |
| Havuzlama (ölçülmeyen ortalama R alır) | ölçülmeyen ↔ ölçülü | +%1,8 daha |

- Gün sayısı mı: Nisan oranı 7 günle 1,095–1,096, tek günün tepesiyle (günlerin ortancası) **1,053** ≈ yaz 1,042. Fark gün sayısından değil, "havası eşit 14 günün en iyisi" payından; yazın tepe en sıcak tek güne düşüyor [Hesap; mekanizma Yorum].
- Büyüklüğe göre (ölçülmeyen, konut eşdeğeri): 10–25 −%0,2; 25–50 +%7,3; 50–100 +%10,7; > 100 +%8,8.
- Öneri (sunumdan sonra, `tepe.py`): R'yi 14 günün en yükseği yerine günlük tepelerin ortancasından almak; farazide beklenen etki ~5 puan [Yorum]; 1–10'da kurulur, yeni sınav şehirlerinde (61–70) bir kez. İspanya Mayıs testi R kullanmıyor, değişmez.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
