# 2026-11-01 — B-Y1: üretici 1.4, yıl boyu tepe (yük haritasının cevap anahtarı)

**Amaç:** Karar masası 23:12 (Faz 11, ADR-0014; Can'ın altı maddesi): deneme şehirleri bugün yalnız Nisan'ı üretiyor; yük haritasının sorusu ("trafo ne kadar dolu") yılın en yüksek saatinde. Aynı şehirlere yaz ve kış haftası eklenir, cevap anahtarına yılın net tepesi, saati, ayı ve akşam gerilim düşümü yazılır. Model değişmez; tepe modeli B-Y2.

## Yöntem
- **Ekleme yalnız.** Nisan çıktıları 1.3 ile birebir (aşağıda sağlama); yeni rastgelelik ayrı akışlardan (`klima14-`, `yaz14-`, `kis14-`, `og14-`). Şehrin ağı, aboneleri, tohumu aynı. Sınav şehirlerinin donukluğu bozulmaz.
- **Pencereler:** şehrin hava yılında (2023 / 2024 / 2025, Nisan'la aynı) yazın (Haziran–Eylül) günlük ortalama sıcaklığı en yüksek 7 ardışık gün, kışın (Ocak–Şubat) en düşük 7 gün [Yorum: bir hafta; günlük ortalama, çünkü akşam klima tepesi sıcak geceyi de görür]. Işınım ve sıcaklık Open-Meteo'nun aynı dosyasından. Tatil: hafta sonu, 1 Ocak, 20 Temmuz, Kurban Bayramı.
- **Eğri:** her günün kendi ayının EAC 2022 tipik günü (iş günü / tatil). Temmuz konutunun tipik günü gece yarısı tepe yapıyor (23:45; tepe ÷ ortalama 1,21) [Hesap: EAC profil sınıfları]; şekil veriden kalır.
- **Sıcaklık terimi:** tipik gün o ayın ortalama havasını taşır. Günün ortalama sıcaklığı ayın ortalamasından ΔT farklıysa günün yükü × (1 + β·ΔT) (yaz) ya da × (1 − β·ΔT) (kış), en az × 0,6. β sınıf başına [Yorum, hepsi varsayım; Kıbrıs'a özgü sınıf eğimi BULAMADIM]: yaz konut ve yurt 0,045, küçük ve büyük ticaret 0,03, otel 0,02, su motoru 0,02, sanayi 0,01 / 0,005; kış konut ve yurt 0,03, küçük ticaret 0,02, diğerleri ≤ 0,015. Trafo başına gizli **klima yaygınlığı** U(0,5; 1,5) (cevap anahtarında `klima_carpani`). Bütün evler aynı havayı görür: klima tepesi eşzamanlı (Muhittin 4 madde 2). β'lar Can'ın 20 Kıbrıs evi + sıcaklık analizine çapalanacak.
- İlk denemede sıcaklık farkı saat saat uygulanmıştı: sıcak dalgada öğleden sonra en çok ısındığı için konut tepesi 17:00'ye kaydı, EAC'nin gece tepesi kayboldu. Günlük farka çevrildi (şehir 1–10'da; sınav şehirlerine bakılmadı).
- **Cevap anahtarı (sözleşme 1.4, sonda):** `tepe_yil_kw` (yılın net tepesi, üç pencere), `tepe_yil_kva`, `tepe_saati`, `tepe_ayi`, `v_min_tepe_v`, `tepe_yaz_kw`, `tepe_kis_kw`, `kva_tavan`, `klima_carpani`. Yeni dosyalar `yuk_5dk_yaz.csv`, `yuk_5dk_kis.csv` (`sicaklik_c` ve `trafo_kva` sütunlarıyla). Can'ın `sinav.py faz2` tepe bölümü `tepe_yil_kw` ve `tepe_saati`'ni okuyor (3bfa967), adlar onunla aynı.

## Sağlama (şehir 1–10, üretici 1.4) [Hesap]
| | |
|---|---|
| Nisan dosyaları (trafolar, yuk_5dk, cevap anahtarının 1.3 sütunları) | 10 şehirde 30 dosyanın 30'u 1.3 ile bayt bayt aynı |
| Üretim süresi | 10 şehir aynı anda 37–42 sn (tek başına ~25 sn; faz1 sınırı 60 sn) |
| Tepe ayı (400 trafo) | Ağustos 198, Temmuz 80, Ocak 67, Haziran 51, Nisan 3, Şubat 1 |
| Tepe saati | şehir konutu 00:xx (31), 20:xx (21), 17:xx (19); çarşı 12–13; otel 12–13; sanayi 09–12; sulama gece |
| Yıl tepesi ÷ Nisan brüt tepesi (ortanca) | konut 1,73; köy 1,61; çarşı 2,00; otel 2,39; yurt 1,79; sanayi 1,22; sulama 1,13 |
| Şehir konutunda yıl tepesi, abone başına | ortanca 0,88 kW (P10 0,49, P90 1,38); gerçek Kıbrıs değeri BULAMADIM, Can'ın 20 ev verisiyle sağlanır |
| Yıl tepesinde kVA'yı aşan trafo | 17/400 (%4): otel 9/42, köy 4, konut 2, çarşı 1, sulama 1; `kva_tavan` 12 trafo, ikisi aynı değil |
| Yıl pencerelerinde 207 V altı | 8/400 (%2), 200 V altı 7, en düşük 162,8 V (köy, uzun tek hat); Nisan'da 0 |

## Bulgular
1. **Yazın en sıcak haftası yükü belirgin artırıyor ve tepe tipine göre farklı saatte:** konutta gece ve akşam, çarşı ve otelde öğlen; Can'ın "tepe saate kilitlenmez" maddesiyle tutarlı. Kış akşamı konut trafolarının %29'unda (40/138) yılın tepesi.
2. **Otel trafolarının %21'i (9/42) yaz tepesinde kVA'yı aşıyor.** Sebep üretici: trafo gücü sınıfın tepesine göre seçiliyor, büyük abonenin kendi büyüklük farkı (log-normal σ 0,3) seçime girmiyor. Gerçekte Kıb-Tek büyük abonenin kayıtlı en yüksek talebini biliyor (Muhittin 4 madde 3). Nisan donuk olduğu için boyutlandırma değişmedi; yük haritasının sınavında bu trafolar ayrı raporlanmalı.
3. **Uzun köy hatlarında yaz tepesinde gerilim çok düşüyor (en düşük 162,8 V).** Hat boyu ve kesiti Nisan'ın gerilim yükselmesine göre kurulmuştu; gerçekte bu kadar düşen hat Kıb-Tek tarafından güçlendirilir [Yorum]. Bu, akşam düşümü maddesini (207 V) farazide abartır.
4. 1.600 / 2.500 kVA listeye eklenmedi: 20 şehrin 15'inde en az bir trafo 1000 kVA'ya kesilmiş; eklemek Nisan'daki `kva`'yı ve sınav şehirlerini değiştirirdi. Öneri: yeni sınav şehirleriyle (üretici 1.5) yaz tepesine göre boyutlandırma (büyük abone ölçeği, hat kesiti, 1.600 / 2.500 kVA).

## Sınav şehirleri
21–30 aynı sürümle üretildi (bir kez; sonuçlarına ayar için bakılmadı). Nisan dosyaları 1.3 ile birebir olduğu sağlandı. Tepe sütunlarını Can'ın `faz2`'si puanlar (öneren ≠ puanlayan).

## Ne kaldı
- β ve klima yaygınlığı varsayım; Can'ın eşzamanlılık ve sıcaklık eğimi sonucu gelince çapalanır (üretici 1.5 adayı).
- Tasarım sıcaklığı (10 yılda bir sıcak akşam) üreticide yok; pencere yalnız şehrin hava yılının en sıcak haftası.
- B-Y2 (tepe modeli) sıradaki iş.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 31 Eki ~23:45 | üretici 1.4, saatlik ΔT | 1–10 | yaz haftası konut tepesini akşama koyar | konut tepesi 17:00'ye kaydı (EAC gece tepesi kayboldu) | günlük ΔT'ye geç |
| 31 Eki ~23:55 | üretici 1.4, günlük ΔT | 1–10 | aynı | konut 00:xx / 20:xx, çarşı ve otel öğlen; Nisan birebir | kabul; 21–30 bir kez üret |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
