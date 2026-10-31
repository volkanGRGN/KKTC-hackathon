# Veri sözlüğü

Her satır: ne, birim/çözünürlük, kaynak, lisans, ölçülü mü, bilinen yanlılık. Ayrıntı ve adresler [araştırma günlüğünde](../log/2026-10-31-kapsamli-arastirma.md).

## Elimizde

Depo açık olduğu ve lisanslar belirsiz olduğu için ham dosyalar depoya konmaz; her klasördeki KAYNAK.txt'de indirme adresi var.

**EAC profil sınıfları** — `data/raw/eac-profil-siniflari/`
- 12 tüketici sınıfının 2022 yılı yarım saatlik eğrisi (17.520 satır) + 24 tipik gün (12 ay × iş günü/tatil). Birim: abonenin yük hakkına (kVA) göre birim değer.
- Kaynak: Güney Kıbrıs dağıtım şirketi, Nisan 2023 (web.archive kopyası). Lisans belirtilmemiş → kaynak gösterilir.
- Ölçülü: konut ve konut+panel 68 ev (2016), küçük ticari 23, büyük ticari 79, otel 30, küçük sanayi 66, büyük sanayi 41. Su pompası, sokak aydınlatması, ısı depolama **ölçülmemiş**, kuraldan türetilmiş.
- Yanlılık: Güney, Kuzey değil; konut 2016 ve 68 ev; ortalama eğri tek evin tepesini düşük gösterir. **5. sayfanın adı "L._COMM._STORES" ama otel sınıfıdır** (PDF sırasıyla doğrulandı).

**EAC üretim (injection) profilleri** — `data/raw/eac-profil-siniflari/Injection_Profile_Classes.xlsx`
- 4 sınıf: PV_SYSTEMS (büyük güneş), PVs_ROOFTOPS (çatı), WIND_PARKS, BIOMASS. 2022, yarım saatlik + 24 tipik gün. Birim: kurulu güce göre pu.
- Kaynak, lisans: Offtake ile aynı (EAC, web.archive, lisans belirtilmemiş).
- Sağlama [Hesap]: çatı güneşi Nisan iş günü tepesi 0,63 pu (13:00); büyük güneş 0,71 pu.
- Kullanım: benzetimdeki panel çıkışının (Open-Meteo ışınımı × kayıp katsayısı) gerçek Kıbrıs çatı eğrisiyle karşılaştırılması. Yanlılık: Güney'in toplam çatı filosunun ortalaması, tek evin bulut geçişini göstermez.

**Kıb-Tek istatistikleri** — `data/raw/kibtek-istatistik/` (stat_2023, stat_2024, tuketim_2024, tuketim_2025; PDF; depoda yok, KAYNAK.txt'de nereden)
- Tarife sınıfı başına abone sayısı ve yıllık MWh (2023: toplam 219.931 tüketici, konut 175.577, ticari I 20.950, ticari II 494, sanayi I 1.227, sanayi II 352, su motorları 3.250).
- Farazi şehirde trafo başına abone karışımı bu oranlardan kurulur. Trafo eşleşmesi YOK.

**Kıb-Tek trafo şartnameleri** — [Kaynaklı, hafızadan]
- Direk 25/50/100/250/400 kVA, 433 V (faz 250 V boşta), kademe yalnız enerjisizken; yer tipi 50–2.500 kVA. Adet ve konum yayımlanmıyor.

**Güney referans sayıları** — EAC on yıllık plan 2025–2034
- 17.886 dağıtım trafosu (direk 11.048 ort. ~95 kVA; yer 6.838 ort. ~583 kVA), alçak gerilim 18.203 km, 615.479 tüketici. Kuzey'in trafo sayısı için vekil (~6.400, [Hesap]).

**Güneş (hava yılı)** — `data/raw/open-meteo-lefkosa/`
- Lefkoşa saatlik, 2024 ve 2025 (17.544 saat): yatay küresel, doğrudan, yaygın ve 30° güney eğimli ışınım (W/m²), sıcaklık, bulutluluk. Yerel saat (yaz saati dahil).
- Kaynak: Open-Meteo Historical Weather API (ERA5 yeniden analiz), CC BY 4.0. İndirildi 31 Ekim 2026.
- Ölçülü değil: uydu + model yeniden analizi, ~9 km ızgara; tek bulut geçişini göstermez (saatlik ortalama).
- Sağlama [Hesap]: yatay yıllık 1.908 / 1.929 kWh/m² (2024 / 2025), Nisan 11–14 ortalaması ~780 W/m².
- Kullanım: Faz 1 rastgeleleştirmede hava yılı 2024 / 2025. PVGIS ikinci kaynak olarak gerekirse.

**SimBench alçak gerilim şebekeleri** — `data/raw/simbench/`
- Almanya'nın 6 tip AG şebekesi (rural1–3, semiurb4–5, urban6): trafo kVA, hat boyları, kablo tipi, yük düğümleri. Yalnız ölçü kaynağı (hat boyu, kablo, trafo başına ev sayısı); pandapower'a geçilmiyor.
- Kaynak: SimBench 1.6.3, veri ODbL 1.0. İndirildi 31 Ekim 2026; paket kurulmadan wheel içinden CSV.
- Sağlama [Hesap]: trafodan en uzak eve 0,23–0,57 km, ortalama eve 0,09–0,20 km; trafo başına 13–118 yük; 160–630 kVA. Tablo KAYNAK.txt'de.
- Yanlılık: Alman şebekesi, **yer altı kablosu** (NAYY 150/240 mm², r 0,21 / 0,13 Ω/km). [Yorum] Kıb-Tek mahalle hatları büyük ölçüde havai ABC 70/95; benzetimdeki varsayım r 0,50 / 0,36 Ω/km → aynı boyda hatta gerilim yükselmesi ~2–3 kat. Hat boyu ve ev sayısı SimBench'ten, kablo direnci Kıb-Tek şartnamesinden alınmalı (şartname adımı açık).

## Adaylar (henüz indirilmedi)
- **İspanya EDP gerçek şebeke** (Mendeley 685vgp64sm, CC BY 4.0): 30 trafo, 8.087 abone, 20 gün akıllı sayaç, GIS. Çözünürlük ve abone tipi bilgisi belirsiz → 2 saatlik zaman kutusu; gerçek doğrulama adayı.
- **NGED LV Load Monitor Data** (İngiltere): 301 CSV, gerçek trafo ölçümü; kayıt istiyor (kaydı Volkan yapmalı).

## Üreteceğimiz

**Deneme şehirleri (Faz 1 çıktısı)** — `data/synthetic/<şehir-no>/` (henüz yok; üretici yazılınca)
- Trafo listesi: kVA, tip, abone karışımı, panel sayısı, hat boyu, faz dağılımı.
- Her trafo için 5 dakikalık yük ve ev ev gerilim; "cevap anahtarı" olarak öğlen en düşük yük ve gerçek kaç ev sığar.
- Her şehrin rastgeleleştirme ayarları kaydedilir (tohum dahil). Etiket: **gösterim, kanıt değil**.
