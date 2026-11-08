# 2026-11-03 — KTEMO çatı panelinin gerçek üretimi ↔ modelin panel formülü

**Amaç:** Modelin panel üretimi formülünü (kurulu güç × 30° güneye eğik ışınım ÷ 1000 × 0,82, `src/sehir_uret.py`) Kuzey'de ölçülmüş gerçek bir panelle sınamak. Soru: panel üretimini hesapla bulup evin kendi tüketimini (sayacın görmediği kısım) ayırırken hata payı ne kadar? Volkan'ın isteği.

**Katman:** panel (öğlen üretim); yaz saati bulgusu yük haritasını da etkiler (sıcaklık).

## Veri
- **KTEMO çatı sistemi** (ktemo.org "EMO Solar" → Fronius Solar.web misafir görünümü): 5 dakikalık üretim, 2018-01-01 – 2026-04-10, 3.022 gün [Kaynaklı: solarweb.com, sistem 4cace063-a5b4-4e4d-b61f-a4bf00dc7b64]. Sayfanın "tüketim" sekmesi binanın tüketimi değil: yılda 80–215 kWh, gece ~24 W (inverterin kendi çekişi) [Kaynaklı: aynı sayfa].
- **Open-Meteo** Lefkoşa saatlik (modelin kaynağı): 2023, 2024–2025 dosyaları + yeni 2018–2022 ve 2026 Ocak–Nisan.
- **PVGIS-SARAH3** (Avrupa Komisyonu JRC, uydu): Lefkoşa saatlik 2018–2023; eğik ışınım, sıcaklık ve kendi 1 kWp güç hesabı (sıcaklık etkisi dahil).
- Adresler, boyut, SHA-256: aşağıda "Ek: KAYNAK taslakları". Ham dosyalar depoda yok (Volkan'ın Mac'inde `hackaton/dis-veri/`).

## Yöntem
- `src/ktemo_karsilastir.py`. Her şey UTC saatine çevrilir; gerçek değer = o saatin 5 dakikalık ortalaması (en az 11/12 örnek).
- Tek katsayı (etkin güç) **ayar yıllarında (2018–2022)** enerji eşitliğiyle bulunur; **sınav 2023** (PVGIS 2023'te bitiyor), Open-Meteo için ayrıca 2023–2026. Sınav yıllarına bakılarak hiçbir şey ayarlanmadı.
- Tahminciler: Open-Meteo (a) modelin bugünkü saat okumasıyla, (b) saat düzeltilmiş; PVGIS (c) eğik ışınım × 0,82, (d) PVGIS'in kendi sıcaklıklı gücü.
- Hata = |gerçek − tahmin| ÷ tahmin. "Saatlik": tahmin > ~120 W/m² eğik ışınım karşılığı; "açık öğlen": eğik ışınım > 700 W/m² (d'de güç > 700 W/kWp, seçim farklı).
- Çevrim dışı gün: açık saatte gerçek < 50 W → gün atıldı (Open-Meteo'da 9, PVGIS'te 2 gün).

## Sonuç

### − Open-Meteo'nun saat sütunu yaz saatsiz (sabit UTC+2); model onu yaz saatli okuyor
- Dosyada Mart / Ekim geçişinde atlanan ya da tekrarlanan saat yok (`2024-03-31T03:00` satırı var; 2015–2025 sıcaklık dosyası dahil) [Kaynaklı: dosyalar]. İstekte `timezone=Europe/Nicosia` olsa da bütün yıl GMT+2.
- KTEMO'yla karşılıklı ilişki (2018) [Hesap]: kış (Kas–Şub) kayma 0'da en yüksek (0,942; ±1 saat 0,876 / 0,883). Yaz (May–Ağu) modelin okumasıyla en iyi kayma −1 saat (0,976; 0'da 0,915); sabit UTC+2 okununca en iyi kayma 0 (0,976).
- `src/sehir_uret.py` (`isinim_oku`, `sicaklik_oku`) etiketi yaz saatli yerel saat sayıp EAC eğrileriyle (saat düzeninde) yan yana koyuyor → **Mart sonu – Ekim sonu güneş ve sıcaklık 1 saat erken**. Aynı klasörü okuyan başka dosyalar: `src/tepe.py`, `src/eszamanlilik.py`, `src/sahte_kayit.py` (grep; saat kullanımları tek tek bakılmadı).
- Panel tahmininde saatlik hatayı iki katına çıkarıyor (aşağıdaki tablo, a ↔ b). **Modelin rakamlarına (yük, panel, renk) etkisi ölçülmedi.** Depodaki `data/raw/open-meteo-lefkosa/KAYNAK.txt` "yerel saat, yaz saati dahil" diyor; yanlış (Can'a UYARI).

### + Panel üretimini hesapla bulmanın hata payı (tek panel)
Sınav 2023 (Open-Meteo için 2023–2026 parantezde) [Hesap]:

| Tahminci | Saatlik ortanca / P90 | Açık öğlen ortanca / P90 | Günlük ortanca / P90 | Aylık ortanca / P90 | Nisan açık öğlen gerçek ÷ tahmin |
|---|---|---|---|---|---|
| (a) Open-Meteo, modelin bugünkü okuması | %36 / %95 (%35 / %94) | %11 / %25 (%11 / %24) | %9 / %23 (%9 / %25) | %2 / %12 (%5 / %13) | 0,96 (0,96) |
| (b) Open-Meteo, saat düzeltilmiş | %16 / %78 (%16 / %81) | %7 / %15 (%8 / %16) | aynı | aynı | 1,02 (0,99) |
| (c) PVGIS eğik ışınım × 0,82 | %14 / %77 | %6 / %13 | %6 / %17 | %3 / %10 | 1,03 |
| (d) PVGIS sıcaklıklı güç | %12 / %74 | %3 / %16 | %6 / %18 | %3 / %9 | 1,00 |

- Okuma [Yorum]: güneşli öğlende ve gün / ay toplamında hesap iyi; bulutlu tek saatlerde zayıf (P90 %74–81: yeniden analiz ve uydu bulutun saatini tam yakalamıyor). Bir trafodaki evler toplanınca yön / gölge farkı azalır, bulut hatası mahallede ortak kalır; tek sistemle ölçülemez.
- Etkin güç (0,82 ile) [Hesap]: Open-Meteo 16,0 kWp, PVGIS ışınımıyla 15,2 kWp. Sistemin gerçek kurulu gücü BULAMADIM (KTEMO'ya sorulur); 0,82'nin mutlak doğruluğu bu yüzden sınanmadı, yalnız şekli.

### − Sabit 0,82 kayıp yazın üretimi fazla gösteriyor
Açık öğlen, gerçek ÷ (b), bütün yıllar 2018–2026, ay (o saatlerin ortalama hava sıcaklığı) [Hesap]:
Şub 1,07 (17 °C) · Mar 1,03 (20 °C) · Nis 1,02 (26 °C) · May 0,93 (31 °C) · Haz 0,95 (34 °C) · Tem 0,93 (37 °C) · Ağu 0,92 (37 °C) · Eyl 0,94 (34 °C) · Eki 1,00 (29 °C) · Kas 1,03 (25 °C).
- (d) aynı ölçüde aylara göre ~0,96–1,04, düz → fark panelin sıcakta az üretmesinden [Yorum]. Nisan öğleninde (panel katmanının kritik anı) fark %0–2.

### ? Gerçek ÷ ışınım yıllar içinde düşüyor
Gerçek ÷ Open-Meteo eğik ışınım [Hesap]: 2019 13,48 · 2020 12,39 · 2021 12,95 · 2022 12,95 · 2023 12,64 · 2024 12,68 · 2025 12,24 → 2019 → 2025 %9 (yılda ~%1,5). Tipik panel yaşlanmasının (~%0,5 / yıl [Yorum]) üç katı; kirlenme, kısa kesinti ve yaşlanma ayrılmadı. 2018 (19 Şubat'tan) ve 2026 (Ocak–Nisan) yarım yıl, karşılaştırılmaz.

### ? Başka açık sistem
Kuzey'de saatlik verisi açık başka sistem BULAMADIM. Arama: Solar.web, Sunny Portal, PVOutput, Kıbrıs PV izleme (web araması). English School of Kyrenia, 34,4 kWp, 2014, Sunny Portal'da yalnız tanıtım sayfası açık; kurulumcunun beklentisi 1.760 kWh/kWp [Kaynaklı: sunnyportal.com PublicPage, plant 268d8b28-6f51-4533-84b5-3e322a57b75c] (modelin varsayımı 1.690, `src/sablon.py` PV_VERIM_MWH_KWP). Zenodo 15209301 (Kıbrıs 68 ev) hâlâ kısıtlı.

## Yapılacaklar (DEVIR iş tahtasına işlendi; hiçbiri başlamadı)
1. **Saat düzeltmesi:** Open-Meteo saatini sabit UTC+2 okuyup yaz saatli yerel saate çevir (`sehir_uret.py`; `tepe.py`, `eszamanlilik.py`, `sahte_kayit.py` kontrol). Yöntem değişikliği: ayar 1–10, yeni sınav şehirleri bir kez.
2. **Sıcaklıklı panel kaybı:** sabit 0,82 yerine sıcaklığa bağlı kayıp; dayanak bu tablo ve PVGIS'in formülü. 1'den sonra.
3. **Hava kaynağı:** PVGIS günlük hatası %6 ↔ Open-Meteo %9, ama 2023'te bitiyor; adayı değerlendir.
4. **KTEMO'ya sorulacak:** çatı sisteminin kurulu gücü; sahip hesabında gerilim kaydı var mı.

## Ek: KAYNAK taslakları (Can'ın dosyaları; UYARI ile kutusunda)

`data/raw/ktemo-solarweb/KAYNAK.txt`:
```
KTEMO (KTMMOB Elektrik Mühendisleri Odası) çatı güneş sistemi — Fronius Solar.web misafir görünümü, gerçek üretim ölçümü.
Sistem: "KTEMO - ON-GRID PV SYSTEM", Nicosia (Lefkoşa). Kurulu güç sayfada yazmıyor (karşılaştırmada etkin güç ~16 kWp [Hesap]).
Giriş: ktemo.org ana sayfası "EMO Solar" → https://www.solarweb.com/Home/GuestLogOn?pvSystemId=d32ed201-6fc3-4443-8bca-44aca07e06cc
Veri (gün başına bir istek, misafir girişinin çereziyle; kayıt / anahtar gerekmez):
  https://www.solarweb.com/Chart/GetChartNew?pvSystemId=4cace063-a5b4-4e4d-b61f-a4bf00dc7b64&year=Y&month=M&day=D&interval=day&view=production
İndirildi: 3 Kasım 2026, curl, 2018-01-01 – 2026-04-10 (3.022 gün, ~58 MB). Son veri 10.04.2026 15:05; sistem o günden beri çevrim dışı.
  Dosyalar: <klasör>/gunluk/YYYY-MM-DD.json. Yerelde hackaton/dis-veri/ktemo-solarweb (Volkan'ın Mac'i); depoya girmez.
Biçim: Highcharts JSON; settings.series[].data = [[zaman damgası, değer], ...].
  Zaman damgası: UTC milisaniye (gerçek UTC; yerel gün 00:00'da başlar). Değer: W, 5 dakikada bir (288 nokta / gün).
  Seri id'leri: FromGenToGrid (şebekeye giden), FromGenToConsumer (doğrudan tüketilen), FromGenToSomewhere (2015–2017 sayaçsız dönem üretimi),
  ToConsumer (binanın tüketimi DEĞİL: sayaç panelin bağlantısında, yalnız inverterin kendi çekişini görüyor; gece ~24 W, yılda 80–215 kWh).
  Üretim = FromGen* serilerinin toplamı. Seri adları tarayıcı diline göre değişir (Türkçe / İngilizce); id'ye bakın.
Sağlama [Kaynaklı: sayfanın kendi yıllık toplamı, MWh]: 2018 25,7 · 2019 27,3 · 2020 24,1 · 2021 27,8 · 2022 27,4 · 2023 26,6 · 2024 26,7 · 2025 26,1 · 2026 6,1; toplam (2015'ten) 238,78.
Bilinen: 9 gün açık öğlende sıfır üretim (çevrim dışı) — karşılaştırmada atıldı.
Lisans: belirtilmemiş (herkese açık misafir sayfası) → kaynak gösterilir.
Karşılaştırma: src/ktemo_karsilastir.py, günlük docs/log/2026-11-03-volkan-ktemo-pv-karsilastirma.md.
```

`data/raw/pvgis-lefkosa/KAYNAK.txt`:
```
PVGIS 5.3 (Avrupa Komisyonu Ortak Araştırma Merkezi, JRC), uydu tabanlı ışınım veritabanı PVGIS-SARAH3, Lefkoşa, saatlik 2018–2023.
Adres (aynısını çalıştırınca aynı dosya iner, kayıt / anahtar gerekmez):
https://re.jrc.ec.europa.eu/api/v5_3/seriescalc?lat=35.1856&lon=33.3823&startyear=2018&endyear=2023&pvcalculation=1&peakpower=1&loss=14&angle=30&aspect=0&components=1&outputformat=csv
İndirildi: 3 Kasım 2026, curl, tek istek. pvgis_saatlik_2018_2023.csv — 52.607 satır, SHA-256 2afc109521e622e4d49aba88645e9f888c1b82ac539cf17ec16831600047b203
  Yerelde hackaton/dis-veri/pvgis-lefkosa (Volkan'ın Mac'i).
Biçim: üstte 10 satır açıklama, sonra başlık; altta sütun açıklamaları.
Sütunlar: time (UTC, "YYYYMMDD:HHMM", dakika :09 — o anın değeri, saat ortalaması değil),
  P (1 kWp sistemin gücü, W; sıcaklık etkisi ve %14 kayıp dahil), Gb(i) / Gd(i) / Gr(i) 30° güneye eğik doğrudan / yaygın / yansıyan ışınım (W/m²),
  H_sun güneş yüksekliği (°), T2m sıcaklık (°C), WS10m rüzgâr (m/s), Int (1 = değer yeniden kurulmuş).
Ölçülü değil: uydu görüntüsünden hesap (~5 km); saatlik, tek bulut geçişini göstermez. SARAH3 2023 sonunda bitiyor (2024–2025 yok).
Lisans: serbest kullanım, kaynak gösterilir ("PVGIS © European Union, 2001–2026").
Kullanım: KTEMO gerçek üretimiyle Open-Meteo'ya karşı ikinci hava kaynağı (docs/log/2026-11-03-volkan-ktemo-pv-karsilastirma.md).
```

`data/raw/open-meteo-lefkosa/KAYNAK.txt` için önerilen değişiklik (fark):
```
--- a/data/raw/open-meteo-lefkosa/KAYNAK.txt
+++ b/data/raw/open-meteo-lefkosa/KAYNAK.txt
@@ -6,7 +6,7 @@ https://archive-api.open-meteo.com/v1/archive?latitude=35.1856&longitude=33.3823
 
 Dosya adı: lefkosa_saatlik_2024_2025.csv — 773.425 bayt, SHA-256 ba297ed72e165dcee602c7481a9787b10bb71ba231c35f9cce6d52c67032e53a (Can, 1 Kasım; eksikti, eklendi)
 Biçim: ilk 2 satır konum bilgisi (ızgara noktası 35.1845, 33.4056, 130 m), 3. satır boş, 4. satır başlık, sonra 17.544 saat.
-Sütunlar: time (yerel saat, Europe/Nicosia, yaz saati dahil), shortwave_radiation (yatay küresel, W/m²), direct_normal_irradiance, diffuse_radiation, global_tilted_irradiance (30° eğim, güneye), temperature_2m (°C), cloud_cover (%).
+Sütunlar: time (DÜZELTME 3 Kasım 2026: yaz saatsiz sabit UTC+2 — istekte timezone=Europe/Nicosia olsa da; Mart / Ekim geçişinde atlanan ya da tekrarlanan saat yok, KTEMO gerçek üretimiyle kışın kayma 0, yazın 1 saat; docs/log/2026-11-03-volkan-ktemo-pv-karsilastirma.md. Önceki not "yerel saat, yaz saati dahil" yanlıştı), shortwave_radiation (yatay küresel, W/m²), direct_normal_irradiance, diffuse_radiation, global_tilted_irradiance (30° eğim, güneye), temperature_2m (°C), cloud_cover (%).
 Not: ışınım değerleri önceki saatin ortalaması (ör. 12:00 satırı = 11:00–12:00).
 
 Sağlama (Can, 31 Ekim): yatay yıllık 1.908 (2024) / 1.929 (2025) kWh/m²; 30° güney 2.099 / 2.127 kWh/m²; Nisan 11–14 ortalaması 787 / 769 W/m²; Haziran tepe saati 12.
@@ -20,3 +20,11 @@ Sağlama (Volkan, 31 Ekim) [Hesap]: yatay yıllık 1.903, 30° güney 2.102 kWh/
 https://archive-api.open-meteo.com/v1/archive?latitude=35.1856&longitude=33.3823&start_date=2015-01-01&end_date=2025-12-31&hourly=temperature_2m&timezone=Europe%2FNicosia&format=csv
 İndirildi 1 Kasım 2026 (BUILD 1). 2.111.056 bayt, SHA-256 e63c92be06428fe4388ad5b8ac227946a1676ce3f630461e0e723e1abb744a0e. Biçim: ilk 2 satır konum, 3. boş, 4. başlık (time, temperature_2m (°C)), sonra 96.432 saat.
 Doğrulama (Can, 1 Kasım 2026): üçüncü dosya aynı adresten yeniden indirildi; bayt ve SHA-256 birebir, 96.432 saat; 2023–2025'in 26.304 saatinde sıcaklık eski iki dosyayla birebir (0 fark).
+
+Saat dilimi notu (3 Kasım 2026, bütün dosyalar): time sütunu sabit UTC+2'dir (yaz saati yok); lefkosa_sicaklik_2015_2025.csv dahil (2024-03-31T03:00 satırı var, tekrar eden saat yok).
+Bu klasörü okuyan kod (sehir_uret.py, tepe.py, eszamanlilik.py, sahte_kayit.py) etiketi yaz saatli yerel saat sayıyor → Mart sonu – Ekim sonu güneş ve sıcaklık 1 saat erken. Düzeltme DEVIR iş tahtasında.
+
+Dördüncü ve beşinci dosya (KTEMO karşılaştırması, 3 Kasım 2026, curl): aynı adres ve sütunlar, start_date / end_date değişik:
+  lefkosa_saatlik_2018_2022.csv (2018-01-01 – 2022-12-31, 43.824 saat) — 1.930.036 bayt, SHA-256 f8d280085726f7eb38442945d0a5785e2bb2dd6c01485ae896fda4ce0f5db0d0
+  lefkosa_saatlik_2026_ocak_nisan.csv (2026-01-01 – 2026-04-10) — 105.475 bayt, SHA-256 7e918ff4844c35c4e8615035f74efea96d2201cf82f3eef1b9a8bfa0745e70d7
+  Yerelde hackaton/dis-veri/open-meteo-lefkosa (2023 ve 2024_2025 dosyalarının kopyasıyla birlikte).
```

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
