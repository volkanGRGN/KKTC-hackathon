# ADR-0012: Sarı trafoda karar haritada değil başvuru anında, başvuranın adresi ve fazıyla verilir

Tarih: 2026-10-31 · Durum: kabul, sınanmadı (ikinci sürüm / pilot) · ADR-0010 ve ADR-0011 üstüne · karar masası 20:50

## Bağlam
Bilginin değeri denemesi ([Faz 3 günlüğü](../log/2026-10-31-volkan-faz3.md), 19:55): trafo çıkış gerilimi, panelli evlerin yeri ve fazı bilinince yanlış kırmızı %27'den %4'e iniyor; sarı ise %62'den ancak %57'ye, ağın tamamı ve öğlen yükü bilinse bile %41'e. Sarının kalan kısmı bilgi eksikliği değil, yeşil kuralının sorusu: yeşil "sıradaki iki başvuru, hattın neresinden gelirse gelsin, %98 sığar" diyor; başvurunun hattın ucundan mı ortasından mı geleceği harita yapılırken bilinemez. Başvuru geldiğinde ise bilinir: başvuru formunda adres var, faz Kıb-Tek bağlantı kaydında olabilir (uzmana soru 4).

## Karar
1. Haritanın rengi trafo içindir; **sarı trafoda onay kararı başvuru anında, o ev için** verilir: aynı hesap (ADR-0011), yeni panel başvuranın hattaki yerine ve fazına konularak bir kez daha koşar; "bu başvuru sığar mı" sorusuna evet / önce ölç / hayır denir. Yeşil trafoda harita kararı yeter; kırmızıda önce ölçüm ya da güçlendirme (değişmedi).
2. Bu adım ADR-0010 madde 2'nin (onaylar kümülatif düşülür) doğal yeri: her onay paydan düşülür, trafo yeniden değerlendirilir.
3. **Bu gece kod yok; sınanmadı.** Sunumda yalnız jüri cevabı olarak ve "sınanmadı" etiketiyle söylenir; slaytta vaat olarak yazılmaz. Pilot / ikinci sürüm listesine girer; farazi şehirde ölçüsü "başvuru-anı kararında yanlış evet oranı" olur.

## Gerekçe
Sarı oranı ürün için bedeldir (trafoların %62'si "önce ölç"); eşik gevşetmek yanlış yeşil getiriyor (19:44 tablosu), bilgi az düşürüyor. Karar birimini trafodan başvuruya taşımak belirsizliğin kaynağını (başvuranın yeri) ortadan kaldırır; ek veri istemez, başvuru formundaki adresi kullanır.
Reddedilen: (a) eşik 0,95 → dolu trafoya "yer var" başlıyor; (b) yeşili "hat ortası" varsayımıyla gevşetmek → İngiltere'de 6 hattın 2'sinde paneller uçtaydı, geri-test yok.

## Sonuçlar
- ROADMAP Faz 3 ikinci sürüm listesine madde; "Açık eksikler" tablosunda sarı satırının pilot sütunu bu ADR'ye bağlanır.
- Can: jüri cevabı ve konuşma notu cümlesi (can.md, karar masası 20:50).
- Pilot: başvuru formuna hat / direk bilgisi eklenmesi Kıb-Tek'e teklif edilir (uzmana soru 2–4).
