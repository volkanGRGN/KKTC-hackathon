# 2026-11-01 — Yük haritası: yaz / kış penceresi tepeyi kaçırıyordu (PR #21 düzeltmesi)

**Amaç:** BUILD 1 (yük) PR #21'i (üretici 1.4, B-Y1) devralırken Civan'ın onay notunu ölçmek: "`tepe_yil_kw` yılın tepesi değil, üç pencerenin tepesi; yılın tepesinin alt sınırı." Alt sınır ne kadar aşağıda?

## Bulgu
- Üreticinin yaz / kış yükü = günün ayının EAC 2022 tipik günü × sıcaklık çarpanı (1 ± β·ΔT, ΔT ayın günlük ortalamasına göre). Tipik gün ayın ortalama havasını zaten taşıyor; ay ay seviyesi çok farklı [Hesap: EAC profil sınıfları, iş günü tepesi]:

| Sınıf | Haziran | Temmuz | Ağustos | Ocak | Şubat |
|---|---|---|---|---|---|
| konut | 1,37 | 1,89 | 1,78 | 1,59 | 1,48 |
| küçük ticaret | 1,90 | 2,36 | 2,25 | 1,67 | 1,54 |
| çarşı | 1,72 | 2,07 | 1,96 | 1,43 | 1,29 |
| otel | 1,65 | 2,07 | 2,11 | 0,50 | 0,47 |

- Pencere ise **günlük ortalama sıcaklığı en yüksek 7 gün** diye seçiliyordu. 2024 hava yılında bu 3–9 Haziran'a düştü: Haziran eğrisi Temmuz'un ~%72'si, 1 + β·ΔT farkı kapatmıyor (ΔT en çok 4,5 °C → × 1,20).
- **Sonuç: 2024 havasıyla üretilen şehirlerde cevap anahtarının "yılın tepesi" üreticinin kendi dünyasındaki tepeden belirgin düşük.** Gürültüsüz sınıf eğrisinde, Haziran–Eylül'ün bütün günlerinin en büyüğüne göre eksik pay [Hesap, klima çarpanı 0,5 / 1,5]:
  - yaz 2024: konut %33–35, küçük ticaret %11–19, çarşı %8–16, otel %21–26;
  - yaz 2025 (pencere 9–15 Ağustos): konut %9–12, çarşı %1–4;
  - yaz 2023 (13–19 Temmuz): ≤ %2;
  - kış (Ocak–Şubat): 2023'te %3–10, 2025'te %0–9 (Şubat haftası seçilince).
- Yük haritasının sınavı bu hedefe karşı ölçseydi **tepeyi az gösteren model ödüllendirilirdi** (güvensiz yön; Muhittin 4 madde 2'nin uyarısı). B-Y1 günlüğündeki "kış akşamı konut trafolarının %29'unda yılın tepesi" de bundan: 2024 şehirlerinde yaz penceresi zayıf olduğu için kış öne geçiyordu.

## Düzeltme (PR #21, `uc_hafta`)
- Pencere **üreticinin kendi konut yüküyle** seçilir: gün skoru = EAC konut eğrisinin o ayki (iş günü / tatil) tepesi × sıcaklık çarpanı (β konut, klima 1); 7 ardışık günün ortalaması en büyük. Yaz ve kış aynı kural. `ayar.json`'a `pencere_secimi` = `konut_yuk_vekili`; `*_penceresi.gunluk_ortalama_c` pencerenin günlük ortalama sıcaklığı olarak kalır.
- Konut seçildi, çünkü yük haritasının asıl sorusu konut akşam tepesi (Muhittin 4: "modelin hırsı akşam tepesinde") ve trafoların çoğu konut ağırlıklı [Yorum].
- Yeni pencereler: yaz 2023 14–20 Temmuz, 2024 18–24 Temmuz, 2025 22–28 Temmuz; kış 2023 25–31 Ocak, 2024 26 Ocak–1 Şubat, 2025 2–8 Ocak.
- Kalan eksik pay (aynı gürültüsüz ölçü): her sınıf ve yılda **≤ %5** (en büyükleri: otel yaz 2025 %4–5, su motoru yaz 2024 %2–5, konut kış 2025 klima 1,5'te %5).

## Sağlama (şehir 1–10, 400 trafo) [Hesap]
| | Önce (df08987) | Sonra |
|---|---|---|
| Nisan dosyaları (trafolar, yuk_5dk, cevap anahtarının 1.3 sütunları) 1.3 ile | 30/30 bayt bayt | 30/30 bayt bayt |
| Tepe ayı | Ağustos 198, Temmuz 80, Ocak 67, Haziran 51, Nisan 3, Şubat 1 | Temmuz 396, Ocak 4 |
| Yıl tepesi sonra ÷ önce (trafo) | — | ortanca 1,038; P10 0,985; P90 1,160; en az 0,926; en çok 1,338 |
| 2024 şehirleri (001, 002, 010), tip ortancası | — | konut 1,14; köy 1,14; çarşı 1,11; otel 1,20; yurt 1,23; sanayi 1,09; sulama 1,03 |
| 2025 şehirleri, tip ortancası | — | konut 1,05; yurt 1,07; **otel 0,97** (Ağustos penceresi otelde daha yüksekti); diğerleri 1,00–1,03 |
| 2023 şehirleri | — | 0,99–1,00 (pencere bir gün kaydı) |
| Yıl tepesinde kVA'yı aşan | 17/400 | 22/400 |
| Yıl pencerelerinde 207 V altı | 8/400, en düşük 162,8 V | 10/400, en düşük 160,1 V |
| Faz 1 sınavı (main'in `sinav.py faz1`) | — | 4/5 GEÇTİ; süre KALDI (10 şehir aynı anda 96–102 sn, makine yüklü: yük ortalaması 12–20; düzeltme öncesi kod da 93–95 sn). Tek başına sehir-005 **26,5 sn**, çıktısı paralel koşumla bayt bayt aynı |

- Sınav şehirleri 21–30 düzeltilmiş sürümle **bir kez** üretildi (5'er paralel, şehir başına 30–32 sn, UYARI yok): Nisan dosyaları 1.3 ile **30/30 bayt bayt aynı**. Tepe sütunlarına ayar için bakılmadı; onları Can'ın `faz2` tepe bölümü puanlar.

## Eksiler (kalan)
1. **Mevsim başına tek pencere:** tepe ayı artık hemen hep Temmuz; `tepe_ayi` pencerenin ayını söylüyor, ay ayrımı bilgisi zayıf. Otel trafolarının yılın tepesi Ağustos'ta olabilir; 2025 şehirlerinde otelin yıl tepesi eskisinden %3,5 düşük (ikisi de alt sınır). Gerekirse ikinci yaz penceresi (Ağustos / otel vekili) üretici 1.5'te; süre ~%25 artar [Yorum].
2. **Alt sınır kalır:** bütün yıl üretilmiyor; kalan pay sınıf başına ≤ %5 (gürültüsüz). Gürültü ve çeşitlilik bu ölçüye girmedi.
3. **Tasarım sıcaklığı yok:** pencere şehrin hava yılının içinde; 10 yılda bir sıcak akşam üreticide yok. Bu, cevap anahtarının değil modelin işi (Muhittin 4 madde 2: sıcaklık düzeltme terimi).
4. kVA aşan ve 207 V altı trafolar biraz arttı (17 → 22, 8 → 10): üretici 1.5'in yaz boyutlandırması bu tepeye göre yapılmalı (Can'ın 1.5'i PR #21'in üstünde).

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas 00:05 | üretici 1.4 (df08987) | — (Open-Meteo 2023–2025, EAC) | en sıcak hafta yılın tepesini taşır | 2024'te Haziran'a düşüyor; konutta %33–35 eksik | pencereyi yük vekiliyle seç |
| 1 Kas 00:10 | üretici 1.4, konut yük vekili | 1–10 | eksik pay ≤ %5'e iner, Nisan değişmez | sınıf başına ≤ %5; Nisan 30/30 aynı; 2024 şehirlerinde yıl tepesi ortanca +%14 | kabul; 21–30 bir kez üret; karar masası Mac'te dener |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
