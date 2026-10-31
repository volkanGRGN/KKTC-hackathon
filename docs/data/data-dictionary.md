# Veri sözlüğü

Her satır: ne, birim/çözünürlük, kaynak, lisans, ölçülü mü, bilinen yanlılık. Ayrıntı ve adresler [araştırma günlüğünde](../log/2026-10-31-kapsamli-arastirma.md).

## Yeni veri eklerken (kontrol listesi)

Her yeni veri için KAYNAK.txt ve aşağıdaki satır bunları cevaplar; cevap yoksa "BULAMADIM" yazılır, tahmin edilmez.
1. **Birim:** kW mı kWh mı, pu ise neye göre (kVA, kurulu güç, yıllık enerji)?
2. **Çözünürlük:** 1 / 5 / 10 / 30 dk, saatlik; ortalama mı, anlık mı, en düşük/en yüksek mi?
3. **Saat damgasının anlamı:** dilimin başı mı sonu mu (EAC'de 00:30 satırı 00:00–00:30 dilimi)?
4. **Saat dilimi:** UTC mi, yerel mi, yaz saati dahil mi?
5. **SHA-256** ve bayt boyu, indirme tarihi ve adresi (KAYNAK.txt).
6. **Çifte sayım riski:** aynı tüketim iki kaynakta mı (ör. net = tüketim − panel; trafo ölçümü ile sayaç toplamı)?
7. **Çapraz sağlama:** hangi bağımsız kaynakla, hangi rakamla karşılaştırılacak (ör. yıllık toplam ↔ Kıb-Tek)?
8. **Lisans** ve atıf metni; lisans yoksa "belirtilmemiş, kaynak gösterilir".
9. **Etiket:** satırdaki her rakam [Kaynaklı: adres] / [Hesap] / [Yorum]; ölçülü mü, türetilmiş mi.

## Elimizde

Depo açık olduğu ve lisanslar belirsiz olduğu için ham dosyalar depoya konmaz; her klasördeki KAYNAK.txt'de indirme adresi var.

**EAC profil sınıfları** — `data/raw/eac-profil-siniflari/`
- 12 tüketici sınıfının 2022 yılı yarım saatlik eğrisi (17.520 satır) + 24 tipik gün (12 ay × iş günü/tatil). Birim: abonenin yük hakkına (kVA) göre birim değer.
- Kaynak: Güney Kıbrıs dağıtım şirketi, Nisan 2023 (web.archive kopyası). Lisans belirtilmemiş → kaynak gösterilir.
- Ölçülü: konut ve konut+panel 68 ev (2016), küçük ticari 23, büyük ticari 79, otel 30, küçük sanayi 66, büyük sanayi 41. Su pompası, sokak aydınlatması, ısı depolama **ölçülmemiş**, kuraldan türetilmiş.
- Yanlılık: Güney, Kuzey değil; konut 2016 ve 68 ev; ortalama eğri tek evin tepesini düşük gösterir. Cumartesi = pazar = bayram: tek tatil tipik günü (tam yıl serisi iki tipik günün tekrarı, pazar ayrı bilgi yok). **5. sayfanın adı "L._COMM._STORES" ama otel sınıfıdır** (PDF sırasıyla doğrulandı).

**EAC üretim (injection) profilleri** — `data/raw/eac-profil-siniflari/Injection_Profile_Classes.xlsx`
- 4 sınıf: PV_SYSTEMS (büyük güneş), PVs_ROOFTOPS (çatı), WIND_PARKS, BIOMASS. 2022, yarım saatlik + 24 tipik gün. Birim: kurulu güce göre pu.
- Kaynak, lisans: Offtake ile aynı (EAC, web.archive, lisans belirtilmemiş).
- Sağlama [Hesap]: çatı güneşi Nisan iş günü tepesi 0,63 pu (13:00); büyük güneş 0,71 pu.
- Kullanım: benzetimdeki panel çıkışının (Open-Meteo ışınımı × kayıp katsayısı) gerçek Kıbrıs çatı eğrisiyle karşılaştırılması. Yanlılık: Güney'in toplam çatı filosunun ortalaması, tek evin bulut geçişini göstermez.

**Kıb-Tek istatistikleri** — `data/raw/kibtek-istatistik/` (stat_2023, stat_2024, tuketim_2024, tuketim_2025; PDF; depoda yok, KAYNAK.txt'de nereden)
- Tarife sınıfı başına abone sayısı ve yıllık MWh (2023: toplam 219.931 tüketici, konut 175.577, ticari I 20.950, ticari II 494, sanayi I 1.227, sanayi II 352, su motorları 3.250).
- Farazi şehirde trafo başına abone karışımı bu oranlardan kurulur. Trafo eşleşmesi YOK.

**Kıb-Tek trafo ve kablo şartnameleri** — **kaynak bağlantısı yok, doğrulanmadı** (BULAMADIM — varsayım)
- Direk 25/50/100/250/400 kVA, 433 V (faz 250 V boşta), kademe yalnız enerjisizken; yer tipi 50–2.500 kVA. Adet ve konum yayımlanmıyor.
- 30 Ekim araştırmasında şartname tarihleri not edilmiş (direk tipi 17.04.2018, yer tipi 24.09.2021), bağlantı kaydedilmemiş; 31 Ekim'de Can ve Volkan'ın aramalarında bulunamadı (arama izi: [Can'ın Faz 1 veri günlüğü](../log/2026-10-31-can-faz1-veri.md)).
- Benzetimdeki kVA listesi, trafo çıkışı 250 V ve ABC 70/95 dirençleri (r 0,50 / 0,36 Ω/km) **varsayım** etiketiyle kullanılır.

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
- Yanlılık: Alman şebekesi, **yer altı kablosu** (NAYY 150/240 mm², r 0,21 / 0,13 Ω/km). [Yorum] Kıb-Tek mahalle hatları büyük ölçüde havai ABC 70/95; benzetimdeki varsayım r 0,50 / 0,36 Ω/km → aynı boyda hatta gerilim yükselmesi ~2–3 kat. Hat boyu ve ev sayısı SimBench'ten alınır; kablo direnci SimBench'ten alınmaz, benzetimdeki ABC varsayımı kalır (Kıb-Tek şartnamesi BULAMADIM, yukarıda).

**OSM kasaba haritası** — `data/raw/osm-kasaba/`
- Girne merkez (~1 km × 1,1 km) bina ve yol geometrisi (Overpass JSON). İndirildi 31 Ekim 2026 (Civan).
- Kaynak: OpenStreetMap, ODbL 1.0; "© OpenStreetMap katkıcıları" atfı.
- Ölçülü değil: gönüllü çizim. Sağlama [Hesap]: 974 bina (278'inde kat bilgisi), 330 yol.
- Yanlılık: binaların %89'unun türü belirtilmemiş (konut/dükkân ayrımı çıkmaz); OSM'de trafo yok, trafo konumları farazi şehirden. Lapta elendi (aynı alanda 17 bina).
- Kullanım: Faz 4 harita altlığı. Ayrıntı ve sorgu KAYNAK.txt'de.

**Yurt yatak sayısı** — BULAMADIM — varsayım: yurt tipi konut eğrisinden türetilir ([ADR-0004](../decisions/adr-0004-veri-eac-profil-siniflari.md); Volkan onayı 31 Ekim).

**İspanya EDP gerçek AG şebekesi — gerçek doğrulama adayı** — `data/raw/edp-oviedo/`
- 30 trafo (28 × 630, 1 × 1000, 1 × 250 kVA), 8.087 müşteri; **saatlik** akıllı sayaç, 1–21 Mayıs 2018 (20 gün); GIS'ten hat boyları ve kablo; sayaç başına çekilen ve verilen enerji.
- Kaynak: Arboleya vd., Universidad de Oviedo + EDP, Mendeley Data 2019, DOI 10.17632/685vgp64sm.1, CC BY 4.0. İndirildi 31 Ekim 2026.
- Ölçülü: evet, gerçek sayaç. Müşteri → trafo eşleşmesi çıkarılabiliyor (ham dosyada trafo merkezi kodu var; ağ izlenince 8.087 yükün 8.073'ü tek trafoya). [Hesap] 29 trafonun öğlen (11–14) en düşük yükü 25–163 kW.
- Eksik / yanlılık: **abone tipi (tarife sınıfı) yok**, yalnız müşteri sayısı ve faz; kentsel, kuzey İspanya [Yorum: Oviedo çevresi], Akdeniz iklimi değil; saatlik (bizim 5 dk); bir trafonun (TD009456, 251 müşteri) verisi tamamen sıfır; çatı paneli az (bir dosyada 1.344 sayacın 54'ünde şebekeye verme).
- Eleme: Kıbrıs/Akdeniz H · ölçülmüş E · ≤ 1 saat E · kaynak ve lisans E · bu fazda kullanımı belli E (Faz 2 2i) → 4/5, **alındı**. Kullanım: modelin bir-trafo-dışarıda doğrulaması gerçek veride; girdi yalnız toplam müşteri sayısı ve kVA olabilir.
- Düzeltme (karar masası 15:12): TD009456 yalnız OpenDSS profilinde (`day_20_profile`) sıfır; ham sayaç verisinde dolu. Ham veride trafo başı ölçüm sayaçları da var (ZIVS…) ve ondalık virgül düzeltmesi gerekiyor; BUILD ham veriden koştu (`src/edp_test.py`, PR #10).

**İngiltere UKPN PV izleme verisi — gerçek gerilim doğrulaması** — `data/raw/ukpn-pv-dogrulama/`
- 20 ikincil trafo (18'i yüksek PV'li, 2'si PV'siz; kırsal + banliyö, Londra değil; 50–1.000 kVA; havai Cu'dan 300 mm² yeraltı Al'a) + 10 PV'li ev (6'sı izlenen trafoların hat ucunda). Her AG fider çıkışında cihaz (57 cihaz): V, I, P, Q, THD faz faz; 9 trafoda ışınım (30 dk). 27 Tem 2013 – 19 Kas 2014 (480 gün).
- **Çözünürlük dikkati:** 10 Haziran 2014 öncesi saatlik en düşük / en yüksek (10 dk ölçümden toplulaştırılmış); tam 10 dk yalnız Haziran 2014 sonrası, 1 dk 18 Haz – 7 Eyl 2014. Bahar öğleni için yalnız saatlik min/maks var.
- Kaynak: UK Power Networks, London Datastore (CC BY 4.0, kayıtsız) + Ofgem kapanış raporu v1.1, Mart 2015. İndirildi 31 Ekim 2026 (karar masası); PV_Data.zip SHA-256 KAYNAK.txt'de. Müşteri sayısı, kVA ve hat boyu veri sayfasında yok, raporun Tablo 3'ünde.
- Ölçülü: evet. [Kaynaklı: kapanış raporu] tasarım bara gerilimi 248 V (yasal üst 253 V); gündüz en düşük talep müşteri başına 200–400 W (Low Carbon London).
- Yanlılık: İngiltere şebekesi (230 V nominal, çoğu yeraltı Al); bizim havai ABC 70/95 hatta **fizik taşınır, rakam taşınmaz**; yalnız 20 trafo.
- Kullanım: Faz 3 gerilim fiziği doğrulaması (PR #11). [Hesap, PR #11] `solve()` 6 hat ucu evin 4'ünde ölçülen yükselmenin 0,84–1,39 katı; paneller uca toplanan 2 sitede az gösterdi → karamsar senaryo panelleri hat ucuna koyar (karar masası 16:27).

## Adaylar (henüz indirilmedi)
- **NGED LV Load Monitor Data** (İngiltere): 301 CSV, gerçek trafo ölçümü; kayıt istiyor (kaydı Volkan yapmalı).

## Üreteceğimiz

**Deneme şehirleri (Faz 1 çıktısı)** — `data/synthetic/sehir-<NNN>/`, `src/sehir_uret.py` üretir, depoya girmez.
- Dosyalar, sütunlar ve birimler tek yerde: [tablo biçimi sözleşmesi](tablo-bicimi.md) (`trafolar.csv`, `yuk_5dk.csv`, `cevap_anahtari.csv`, `ayar.json`). Kıb-Tek'in bilmediği her şey (tip, faz dağılımı, trafo çıkış gerilimi, gerçek kaç ev) cevap anahtarında.
- Etiket: **gösterim, kanıt değil**.
