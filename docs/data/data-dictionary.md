# Veri sözlüğü

Her satır: ne, birim/çözünürlük, kaynak, lisans, ölçülü mü, bilinen yanlılık. Ayrıntı ve adresler [araştırma günlüğünde](../log/2026-10-31-kapsamli-arastirma.md).

## Elimizde

Depo açık olduğu ve lisanslar belirsiz olduğu için ham dosyalar depoya konmaz; her klasördeki KAYNAK.txt'de indirme adresi var.

**EAC profil sınıfları** — `data/raw/eac-profil-siniflari/`
- 12 tüketici sınıfının 2022 yılı yarım saatlik eğrisi (17.520 satır) + 24 tipik gün (12 ay × iş günü/tatil). Birim: abonenin yük hakkına (kVA) göre birim değer.
- Kaynak: Güney Kıbrıs dağıtım şirketi, Nisan 2023 (web.archive kopyası). Lisans belirtilmemiş → kaynak gösterilir.
- Ölçülü: konut ve konut+panel 68 ev (2016), küçük ticari 23, büyük ticari 79, otel 30, küçük sanayi 66, büyük sanayi 41. Su pompası, sokak aydınlatması, ısı depolama **ölçülmemiş**, kuraldan türetilmiş.
- Yanlılık: Güney, Kuzey değil; konut 2016 ve 68 ev; ortalama eğri tek evin tepesini düşük gösterir. **5. sayfanın adı "L._COMM._STORES" ama otel sınıfıdır** (PDF sırasıyla doğrulandı).

**Kıb-Tek istatistikleri** — `data/raw/kibtek-istatistik/` (stat_2023, stat_2024, tuketim_2024, tuketim_2025; PDF; depoda yok, KAYNAK.txt'de nereden)
- Tarife sınıfı başına abone sayısı ve yıllık MWh (2023: toplam 219.931 tüketici, konut 175.577, ticari I 20.950, ticari II 494, sanayi I 1.227, sanayi II 352, su motorları 3.250).
- Farazi şehirde trafo başına abone karışımı bu oranlardan kurulur. Trafo eşleşmesi YOK.

**Kıb-Tek trafo şartnameleri** — [Kaynaklı, hafızadan]
- Direk 25/50/100/250/400 kVA, 433 V (faz 250 V boşta), kademe yalnız enerjisizken; yer tipi 50–2.500 kVA. Adet ve konum yayımlanmıyor.

**Güney referans sayıları** — EAC on yıllık plan 2025–2034
- 17.886 dağıtım trafosu (direk 11.048 ort. ~95 kVA; yer 6.838 ort. ~583 kVA), alçak gerilim 18.203 km, 615.479 tüketici. Kuzey'in trafo sayısı için vekil (~6.400, [Hesap]).

**Güneş** — Open-Meteo (2024–2026 saatlik, CC BY) ve PVGIS, Lefkoşa. Önceki çalışmada kullanıldı; dosyası bu klasörde yok, yeniden indirilecek.

## Adaylar (henüz indirilmedi)

- **SimBench** (Almanya, ODbL): 6 alçak gerilim şebekesi; hat boyu, kablo, ev sayısı için ölçü kaynağı.
- **İspanya EDP gerçek şebeke** (Mendeley 685vgp64sm, CC BY 4.0): 30 trafo, 8.087 abone, 20 gün akıllı sayaç, GIS. Çözünürlük ve abone tipi bilgisi belirsiz → 2 saatlik zaman kutusu; gerçek doğrulama adayı.
- **NGED LV Load Monitor Data** (İngiltere): 301 CSV, gerçek trafo ölçümü; kayıt istiyor (kaydı Volkan yapmalı).

## Üreteceğimiz

**Deneme şehirleri (Faz 1 çıktısı)** — `data/synthetic/<şehir-no>/` (henüz yok; üretici yazılınca)
- Trafo listesi: kVA, tip, abone karışımı, panel sayısı, hat boyu, faz dağılımı.
- Her trafo için 5 dakikalık yük ve ev ev gerilim; "cevap anahtarı" olarak öğlen en düşük yük ve gerçek kaç ev sığar.
- Her şehrin rastgeleleştirme ayarları kaydedilir (tohum dahil). Etiket: **gösterim, kanıt değil**.
