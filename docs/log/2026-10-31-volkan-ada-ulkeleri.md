# 2026-10-31 — Volkan (+ Claude, BUILD): ada şebekeleri çatı panelini nasıl sınırlıyor; kullanılabilir açık veri

## Hipotez / amaç
Kıb-Tek trafoları izlemiyor, akıllı sayacı yok ve trafo başına düz bir kural kullanıyor (panel ≤ trafo gücünün %40'ı). Soru: başka ada şebekeleri (Malta akıllı sayaçla mı yaptı?) bunu nasıl çözdü ve kullanabileceğimiz açık veri var mı? Amaç sunum kıyası, jüri cevabı ve üretici 1.3 için dış çapa.

## Yaptıklarım
- Web taraması: Malta, Hawaii, Güney Kıbrıs; kısaca Porto Riko, Mauritius, Kanarya / Balear, Girit, Barbados, Jamaika, Singapur, Réunion / Korsika, Madeira / Azorlar, Guernsey / Jersey.
- Kritik rakamlar kaynağında açılıp kontrol edildi. Açılamayanlar "ikinci el" diye işaretli.
- Enemalta harita verisi tek istekle indirildi (aşağıda). Lisansı yazılı değil: **depoya girmedi**; burada yalnız özet rakamlar [Hesap]. KAYNAK.txt ve sözlük satırı Can'ın (can.md).

## Sonuç

### + Malta'nın kapasite haritası açık veri: 1.332 trafo merkezi
- Enemalta'nın [Available Capacity](https://enemalta.com.mt/available-capacity/) sayfasındaki harita, verisini `?capacity_json=1` adresinden okuyor. 31 Ekim 20:37'de indirildi; SHA-256 `27be61a7…251142675b60`, 1.332 kayıt.
- Alanlar: merkez adı, yer, trafo gücü toplamı (kVA), kaydedilmiş en yüksek talep, boş güç (= güç − en yüksek talep; 1.311/1.331 kayıtta birebir), izin verilen ek panel ("RES Available Capacity", kWp), konum.
- Sayfanın söylediği [Kaynaklı: aynı sayfa]: ek panel kapasitesi "transformer spare capacity, the installed RES capacity as well as grid voltage stability criteria" ile bulunuyor; harita üç ayda bir güncelleniyor; bağlayıcı değil. Gerilim yöntemi yayınlanmamış.

### + Malta'nın izni de düz bir yüzde: trafo gücünün %25'i [Hesap]
İzin verilen ek panel ÷ trafo gücü (1.331 merkez):

| | Merkez | Talep ÷ güç (ortanca) |
|---|---|---|
| Tam %25 | 245 | 0,20 |
| Sıfır | 290 | 0,59 |
| Arada | 796 | — |
| %25'in üstünde | **0** | — |

- En sık izin değerleri gücün tam dörtte biri: 400 kWp (1.600 kVA), 250 (1.000), 200 (800), 125 (500), 62,5 (250).
- Okuma [Yorum]: izin, gücün %25'i eksi kurulu panel gibi davranıyor; dolu trafolarda sıfır. Enemalta kuralı hiçbir yerde yazmıyor; bu bizim veriden çıkarımımız.
- Sunum için: akıllı sayacı olan Malta da haritasında trafo başına düz bir tavan kullanıyor, Kıb-Tek'in %40'ından sıkı. Biz her trafoya gerilimle ayrı bakıyoruz.

### ? Malta'da trafo doluluğu: dış çapa adayı, kıyas tam değil
- Kaydedilmiş en yüksek talep ÷ trafo gücü P10 / P50 / P90: 0,13 / 0,42 / 0,74; 20 merkezde > 1 [Hesap].
- Trafo güçleri çoğunlukla 1.000 (356), 1.600 (338), 500 (277), 800 (221) kVA.
- Bizim üretici (20 şehir, 800 trafo): Nisan 14 günün tepe ÷ kVA P10 / P50 / P90 0,16 / 0,27 / 0,47 [Hesap]. Malta'nınki yılın en yüksek yükü (yaz ve klima dahil), bizimki yalnız Nisan: birebir kıyas değil. Üretici 1.3'te trafo boyutlandırması için (bugün "gerek × 1,2–2,0" [Yorum]) çapa olabilir.

### + Malta'da sınırı gerilim ve kademe koydu, güç değil
[Kaynaklı: Micallef & Weissenbacher, 14. Symposium Energieinnovation, Graz 2016](https://www.tugraz.at/fileadmin/user_upload/Events/Eninnov2016/files/lf/Session_B1/LF_Weissenbacher.pdf):
- ~1.200 adet 11 kV / 400 V trafo (140'ı Gozo'da). Manuel kademe, beş adım, ±%5; "set once and never changed again".
- Ev sayaçları reaktif güç kaydetmiyor.
- Gozo'da dört trafo merkezi (mevsimlik kademe ayarı isteyen, aşırı gerilim yüzünden): 33 milyon 15 dakikalık sayaç kaydı, 1.600 tüketici ve 157 panel sayacı.
- Senaryolar: her panelsiz eve +1 kWp mevcut trafo ve faz dengelemeyle EN 50160 içinde. +2 kWp trafo değişimi (433 V → 400 V) ya da inverterde Q(V), bir merkezde yük altında kademe değiştirici.
- 11 kV / 433 V trafo boşta faz başına 433 ÷ √3 ≈ 250 V [Hesap]: Kıb-Tek şartnamesindeki boşta 250 V ile aynı.

### + Gozo'da tek hattın tam tablosu: dış sınama adayı
Aynı makale, Tablo 3 (Srug, F1):

| | Panelsiz | Bugün | +1 kWp/ev | +2 kWp/ev |
|---|---|---|---|---|
| Trafo (11 kV / 433 V) | 500 kVA | 500 | 500 | 500 |
| Yıllık tüketim | 106.219 kWh | | | |
| Akşam tepe / gündüz (11–15) tepe | 41 / 25 kW | | | |
| Panel | — | 26,72 kWp | 44,72 | 62,72 |
| Ne gerekti | — | sorun yok | bir kez kalıcı kademe değişikliği | trafo değişimi 433 → 400 V + faz dengeleme |

- Hatta 18 panelsiz ev var [Hesap: (44,72 − 26,72) ÷ 1 kWp].
- Eksik: hat boyu, kablo, ev sayısının tamamı. Hesabımız bu hatta aralıkla koşulabilir; sonuç "tek hat, gösterim".

### + Hawaii düz kuralı kanıtla gevşetti
[Kaynaklı: Sunrun sunumu, New York ITWG, 15.09.2022](https://dps.ny.gov/si-hawaii-smart-inverter-settings):
- Sınır tepe yükün %15'i ile başladı. Önce gündüz en düşük yükün %50'si, sonra %75 (< 10 kW), %100 ve %120 oldu (devre çalışmalarıyla). En son tahmini brüt gündüz en düşük yükün %250'si.
- Ev trafosu için ayrı eleği var: trafo gücünün %166'sı. "Doymuş" trafodaki müşteri volt-watt ayarıyla bağlanabiliyor.

[Kaynaklı: HECO, "Minimum Day Time Load Calculation and Screening", 2014](https://www.energy.gov/sites/prod/files/Hawaiian%20Electric%202014-04-30_minimum-day-time-load-calculation-and-screening.pdf):
- Brüt gündüz en düşük yük = ölçülen net en düşük yük + kurulu panelin bir yüzdesi; pencere 10:00–14:00.
- Ölçülmeyen hat, benzer ölçülen hattın tepe / en düşük yük oranıyla tahmin ediliyor.
- Bizim yöntemin emsali: az ölçüm, gerisi benzerlikten tahmin.

### ? Akıllı inverter ayarı kapasite açıyor (ikinci el)
- Malta Aralık 2024'ten beri Volt-Var ayarlı invertere %25 fazla panel izni veriyor; tek faz 4,6 kW [ikinci el: maltatoday.com.mt/comment/opinions/132720, enemalta.com.mt/?p=13824; BUILD sayfaları açmadı].

### ? Malta akıllı sayaçları panel için alınmamış
- IBM sözleşmesi 2008 sonu, ~€70 milyon, 250.000 sayaç; Enel sayaçları 2010'da başladı; amaç teknik olmayan kayıp ve faturalama [ikinci el: tdworld.com, gridspertise.com; BUILD açmadı].
- Enemalta'nın panel kuralını sayaç gerilim verisiyle koyduğuna kanıt BULAMADIM. Sayaç verisiyle yapılan panel çalışmaları akademik (Graz 2016; Energies 2022, 15(18), 6731).

### − Güney Kıbrıs: sayaç var, sorun ülke çapında kısıntı (ikinci el)
- ~220.000 akıllı sayaç (Ocak 2026), hedef ~400.000 [ikinci el: en.politis.com.cy/economy/982967].
- 2025 Ocak–Mayıs olası yenilenebilir üretimin %58'i kısıldı; yeni mahsuplaşma başvuruları 1 Ekim 2025'te kapandı [ikinci el: pv-magazine.com, 17.07.2025].
- Kapasite haritası iletim trafo merkezi düzeyinde, mahalle trafosu düzeyinde değil.

### − Akıllı sayaç verisinin kendisi açık değil
BULAMADIM. Arama izi:
- Malta: Gozo 33 milyon kayıt ve Energies 2022 verisi yayınlanmamış.
- Güney Kıbrıs: data.gov.cy'de EAC dağıtım ya da sayaç verisi yok (yalnız şarj istasyonları); ülke çapında yük iletim işletmecisinde.
- Hawaii: indirilebilir kapasite dosyası bulunamadı; 2014 belgesinde rakam değil yöntem var.
- Mauritius: trafo trafo izin var, oran BULAMADIM.
- Porto Riko: hat tepe yükünün %15'inde çalışma; ölçüm yoksa en düşük yük = tepe × %33 [ikinci el: energia.pr.gov, 05.09.2024].
- Réunion / Korsika, Madeira / Azorlar, Guernsey / Jersey: alçak gerilim yöntemi BULAMADIM.

## Karar / sıradaki adım
- Karar masasına (volkan.md UYARI): sunum cümlesi (Malta %25 ↔ Kıb-Tek %40; Hawaii), Gozo hattında dış sınama, üretici 1.3 kVA çapası.
- Can'a (can.md UYARI): `data/raw/enemalta-kapasite/KAYNAK.txt` ve veri sözlüğü satırı. Ham veri depoya girmez.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
