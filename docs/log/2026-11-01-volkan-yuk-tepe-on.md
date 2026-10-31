# 2026-11-01 — Yük haritası: yılın tepesi, ön sürüm (`src/tepe.py`, ADR-0018)

**Amaç:** Muhittin 4 madde 2 ve ADR-0018 (karar masası 00:30): her trafoda "trafo ne kadar dolu" sorusunun cevabı, yılın net tepesi (kW, kVA), saati, ayı ve geniş bandı, "ön" etiketiyle. Bant İspanya Mayıs artıklarından; "Mayıs ≠ Temmuz" ve "klima kuyruğu ölçülmedi" açık etiket; sıcaklık düzeltme terimi; eşzamanlılık için yuva (fitler Can'ın B-Y2'si). BUILD 1 (yük).

## Yöntem
1. **Önsel eğri (her trafoda, Kıb-Tek'in bildiğiyle):** abone karışımı tarife sınıflarına, sınıf enerjisi faturaya ölçeklenir; her sınıfın EAC 2022 ay tipik günü (Güney Kıbrıs, açık veri) × sınıfın yıllık ortalama kW'ı; eksi güneş (panel kW × ayın saatlik ortalama ışınımı × 0,80 [Yorum]). Ticari II tarifesi büyük ticaret eğrisini alır (Kıb-Tek yapı tipini bilmez; yurt bu yüzden yanlış eğri alır).
2. **Ölçüye bağlama:** ölçülü 12 trafo (sablon.py'nin tabakalı seçimi, bugün yalnız Nisan) için R = ölçülen Nisan net tepesi ÷ önselin Nisan tepesi. Ölçülmeyen R'lerin geometrik ortalamasını alır. Şehir 1–10'da R ortalaması 1,08–1,16 [Hesap]: ölçülen tepe tipik günden %8–16 yüksek (günler arası fark ve ev ev gürültü). Eşzamanlılık yuvası (`eszamanlilik`) bugün 1.
3. **Yıl taraması:** Haziran–Eylül ve Ocak–Şubat'ın her ayı (ve Nisan), iş günü ve tatil; ayın tipik günü × (1 ± eğim × ΔT), ΔT = şehrin hava yılında ayın en sıcak (kışın en soğuk) gününün ay ortalamasından farkı. En büyük net değer tepe, saati, ayı. Tasarım kipi (`--hava tasarim`) ΔT'ye + 2 °C [Yorum; Lefkoşa uzun seri BULAMADIM, elde 2023–2025]: tepe ortanca × 1,056 (P90 1,076) [Hesap, şehir 1–10].
4. **Eğim (sıcaklık düzeltme terimi):** sınıfın EAC ay tipik günü tepesinin Lefkoşa ay ortalama sıcaklığına doğrusal regresyonu (yaz Nisan–Ağustos, kış Kasım–Mart), Temmuz / Ocak tepesine göre [Hesap: EAC 2022 × Open-Meteo 2023–2025; yıllar farklı, Yorum]. Yaz °C başına: konut %3,0, küçük ticaret %3,8, büyük ticaret %3,7, otel %4,7 (turizm mevsimi karışık), küçük sanayi %1,8, büyük sanayi %1,1, su pompası 0. Kış: konut %2,8, küçük ticaret %2,1, büyük ticaret %1,9. Belirsizlik: eğim × 0,5 ve × 2 ile yeniden tarama [Yorum].
5. **Bant:** İspanya Mayıs tepesinin bir-dışarıda log artıkları ln(gerçek ÷ tahmin), girdi c (fatura), tabakalı 10 + 15 ölçülü, 660 satır, 28 trafo: **P10 −0,218, ortanca −0,041, P90 +0,420** [Hesap]. Sağa çarpık (gerçek tepe tahminin %52 üstüne çıkabiliyor), simetrik yapılmadı. Trafo bandı = bu niceller ⊕ eğim belirsizliği (log ölçekte karelerin toplamının kökü, iki yan ayrı). Ölçülü trafonun bandı yalnız eğimden. Farazi şehre bakılarak seçilmedi.
6. **Çıktı:** `tepe.csv` (sözleşme §7, 1.4 adayı; Can'ın sütun önerisi + `kor_nokta`), `tepe_ozet.json`. Haritanın "yük için boş" sayısı `bos_kva_p10` = `kva` − P90 tepe (ADR-0018 m. 6).

## İspanya Mayıs tepesi (gerçek veri, `edp_test.py --hedef tepe`)
- Veri: EDP Oviedo, 1–20 Mayıs 2018, 29 trafo (30'dan biri faturasız, çıkarıldı; tabakalı denemelerde tahmin edilen 28). Tepe 51–322 kW. Tepe saati: 22:00'de 11 trafo, 23:00'te 3, öğlen (11–14) 11, diğer 4 [Hesap].
- Model (girdi c, fatura) bu veride saf fatura kıyasıyla aynı rakamı veriyor (öğlende de böyleydi, ADR-0016).

| Girdi c (fatura) | Hata ortanca | P90 | %80 bant, kalibrasyonsuz | %80 bant, K_TEPE 1,164 |
|---|---|---|---|---|
| 10 ölçülü, tabakalı | %15,4 | %36,1 | %76,6 | %80,3 |
| 15 ölçülü, tabakalı | %13,4 | %34,8 | %73,9 | %79,6 |
| 10 ölçülü, rastgele | %16,0 | %33,9 | %79,7 | %84,7 |

- K_TEPE (edp_test.py'nin kendi bandı için): `kalibrasyon.py ispanya`, girdi c, 10 + 15, tabakalı: k 1,164; bir-dışarıda %80 kapsama %75,5 → %78,8; trafo bırakınca k 1,02–1,28 [Hesap].
- Can'ın geçici eşiği (ortanca ≤ %15, P90 ≤ %35, %80 bant %70–90; `sinav.py faz2 --ispanya-tepe`): 10 ölçülü tabakalıda hata eşiklerin kıl payı üstünde (%15,4 / %36,1), bant içinde. Puanlayan Can / karar masası.

## Geliştirme (şehir 1–10, üretici 1.4 düzeltilmiş, ölçülmeyen 280 trafo) [Hesap; farazi, gösterim]
| | Hepsi | Şehir konutu | Köy | Çarşı | Otel | Sanayi | Sulama | Yurt |
|---|---|---|---|---|---|---|---|---|
| n | 280 | 109 | 39 | 24 | 31 | 12 | 27 | 38 |
| Hata ortanca | %6,1 | %4,9 | %5,3 | %14,1 | %9,5 | %12,8 | %4,8 | %6,9 |
| Hata P90 | %15,9 | %11,2 | %10,3 | %27,4 | %19,0 | %21,2 | %11,3 | %18,7 |
| Sapma (ortanca, + = fazla tahmin) | +%3,6 | +%2,1 | −%0,5 | +%14,1 | +%7,5 | +%11,5 | −%2,5 | +%6,2 |
| %80 bant kapsama | %98,2 | %100 | %100 | %83,3 | %100 | %91,7 | %100 | %100 |
| Gerçek P90'ın üstünde | %0 | | | | | | | |
| Tepe saati ±60 dk | %42,1 | %56,9 | %48,7 | %45,8 | %22,6 | %41,7 | %40,7 | %7,9 |

- Bant P90 ÷ P10 ortanca 1,93.

## Sınav şehirleri 21–30 (bir kez; model 1–10'dan sonra değişmedi) [Hesap: BUILD 1 koşusu, resmi değil; resmi = karar masasının Mac koşusu, puanlayan Can]
| | Hepsi | Şehir konutu | Köy | Çarşı | Otel | Sanayi | Sulama | Yurt |
|---|---|---|---|---|---|---|---|---|
| n | 280 | 110 | 34 | 32 | 26 | 24 | 23 | 31 |
| Hata ortanca | %6,0 | %4,8 | %4,4 | %17,8 | %6,4 | %8,4 | %8,2 | %7,5 |
| Hata P90 | %17,7 | %10,6 | %9,6 | %24,7 | %14,7 | %20,0 | %16,8 | %15,7 |
| Sapma | +%2,7 | +%1,7 | −%1,1 | +%17,8 | +%5,2 | +%8,4 | −%7,0 | +%6,5 |
| %80 bant kapsama | %98,6 | %100 | %100 | %90,6 | %100 | %95,8 | %100 | %100 |
| Gerçek P90'ın üstünde | %0 | | | | | | | |
| Tepe saati ±60 dk | %45,4 | %53,6 | %50,0 | %53,1 | %46,2 | %54,2 | %34,8 | %3,2 |

## Bulgular
1. **Farazi şehirde tepe hatası küçük (ortanca %6), ama bu iyimser:** üretici de yazı EAC ay tipik günleriyle kuruyor, model aynı açık veriyi kullanıyor (ADR-0008). Gerçeğe en yakın ölçü İspanya: Mayıs tepesi faturayla ortanca %15, P90 %36. Kıbrıs yaz akşamı ölçülmedi.
2. **Bant farazide çok geniş (%98–99 kapsama), gerçekte yerinde (İspanya %80):** bant gerçek dünyanın dağınıklığını taşıyor; farazi şehir daha düzenli. Haritanın "yük için boş" sayısı bu yüzden temkinli (ADR-0018'in istediği yön).
3. **Gerçeğin bandın üstüne çıktığı trafo yok (0/560)**; sapma çoğunlukla fazla tahmin yönünde (çarşı +%14–18, sanayi +%8–12): ayın en sıcak günü terimi üreticinin tek haftasından sert. Güvenli yön.
4. **Tepe saati zayıf (±60 dk %42–45):** konutun Temmuz tipik gününde iki tepe var (16–17 ve 23), hangisinin büyük çıktığı güne göre değişiyor; model tipik günün büyüğünü (23) söylüyor. Yurtta tarife ticari II büyük ticaret eğrisini veriyor (öğlen), gerçek akşam (%3–8 isabet).

## Eksiler (kalan)
1. İspanya gerçek veride tepe hatası Can'ın geçici eşiğinin kıl payı üstünde (10 tabakalı: %15,4 / %36,1); fatura × oran Mayıs tepesinde bu kadar iyi. Kıb-Tek tepe verisi gelince yeniden fit.
2. Eşzamanlılık yok: R abone sayısına bağlı değil (küçük trafoda tepe ÷ ortalama daha yüksek); Can'ın B-Y2'si (iki bileşen: taban √N, klima ~doğrusal) `eszamanlilik` yuvasına.
3. Eğim Güney Kıbrıs'ın aylar arası farkından; gün gün eğim (sıcak dalga içi) ve Kuzey Kıbrıs farkı ölçülmedi; Can'ın 20 ev + sıcaklık fiti gelince değişir.
4. Akşam gerilimi (`v_min_tepe_v`) tahmin edilmiyor; Can'ın sınavı okuyabiliyor; sonraki adım (hat boyu + tepe yükü ile düşüm).
5. Tasarım sıcaklığı yalnız 3 yıllık seriden + 2 °C [Yorum]; 10 yıllık Lefkoşa serisi BULAMADIM (indirilmedi).
6. Yurt ve ticari II: yanlış eğri; Kıb-Tek'in müşteri listesinde yapı tipi varsa (Muhittin 4 madde 3, kalem 9) düzelir.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas 00:25 | edp_test --hedef tepe | İspanya 28 trafo | fatura × oran Mayıs tepesini de taşır | ortanca %15,4, P90 %36,1 (10 tabakalı); artık sağa çarpık | bant tabanı bu artıklar; K_TEPE 1,164 |
| 1 Kas 00:30 | tepe.py ön | 1–10 | EAC ay eğrisi × fatura × Nisan oranı yaz tepesini taşır | ortanca %6,1, kapsama %98, üst kaçış 0 | kabul (ayar yok) |
| 1 Kas 00:35 | tepe.py ön | 21–30 bir kez | aynı | ortanca %6,0, kapsama %98,6, üst kaçış 0 | PR; karar masası Mac'te tekrarlar |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
