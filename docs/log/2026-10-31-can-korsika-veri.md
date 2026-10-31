# 31 Ekim 2026 — Can — Korsika'dan başka ne alınır (araştırma)

Soru: Civan'ın indirdiği iki tablonun (`data/raw/edf-sei-corse/`: trafo sayısı ve hat boyu, belediye tüketimi) dışında Korsika'da işe yarar açık veri var mı?

## Arama izi
- Eski portal `opendata-corse.edf.fr` API'si artık 410 dönüyor; `opendata-corse-outremer.edf.fr` → `https://opendata.edf.fr` adresine yönleniyor (data-fair portalı, 438 veri seti).
- Katalog: `https://opendata.edf.fr/data-fair/api/v1/datasets?size=200&page=1..3` (yalnız başlık, satır sayısı ve tarih okundu). Başlıkta Corse / poste / BT / capacité / consommation geçenler süzüldü.
- Web: "EDF Corse open data postes HTA/BT", "opendata-corse.edf.fr consommation 30 minutes", "EDF SEI Corse compteurs communicants courbe de charge poste".
- Licence Ouverte 2.0, hepsi aynı portal. Hiçbir dosya çalıştırılmadı; yalnız JSON/CSV okundu, iki küçük çekim scratchpad'de kaldı (depoya girmedi).

## Bulunanlar (projeye yararına göre)
1. **Limitations de production au titre de la sûreté système — Corse** (`-loom5g9u-cpg3or2i-i5ibo`, 96 satır, 2016-01 – 2023-12, aylık). Adanın anlık yenilenebilir sınırı %35; aşınca rüzgâr ve güneş kesiliyor; her ay kaç saat kesildiği yazıyor.
   - [Hesap: 96 satır, aylara göre toplam] 2016–2023'te kesinti saatlerinin **%56,9'u Nisan + Mayıs'ta** (Nisan 513 sa, Mayıs 645 sa, Haziran 315, Ekim 252, Mart 172); **Temmuz–Ağustos ve Aralık–Ocak'ta ~0**. Yıllık toplam 54 sa (2016) → 356 sa (2023).
   - Okuma [Yorum]: Kıbrıs'a benzer yalıtık bir adada güneşin şebekeye sığmama sorunu baharda en büyük. Bizim "Nisan öğlen en düşük yük" seçimimizin (11–14, adım 132–167) dış sağlaması. Mekanizma farklı: Korsika'daki sistem (frekans) sınırı, bizimki mahalle trafosunda gerilim; ama sebep aynı (düşük yük + yüksek güneş).
2. **Production d'électricité par filière … au pas horaire — Corse** (`p57z3vkij2q8njk2z74ih-ne`, 52.608 satır, 2019–2024, saatlik): toplam üretim (= ada talebi, ithalat dahil), PV MW, maliyet.
   - [Hesap: 2023, 8.760 saat, UTC'den yerele +1/+2] yıllık tepe 467,9 MW (9 Şubat akşam, elektrikli ısıtma); Nisan 11–14 en düşük 209,0 MW (23 Nisan, Pazar), ortanca 252,5 MW → **Nisan öğle en düşük ÷ yıllık tepe = 0,45** (ortanca 0,54). PV tepe 149,8 MW.
   - Kullanım adayı: Kıbrıs dışı bir adada "öğle en düşük ÷ tepe" oranı için kaba dış çapa; PV üretim eğrisinin şekli (enlem 42°, Kıbrıs 35°). Yanlılık: ada toplamı, trafo değil; Korsika tepesi kışın, Kıbrıs'ta yazın (klima).
3. **Lignes basse tension (BT aérien / BT souterrain) — Corse** (`em2hugg9zm5e4jgz3x2l8pqq` 39.054 parça, `a-6k77pgindfq3tyect9hj34` 61.011 parça): AG hat geometrisi, havai/yeraltı ayrı. Civan'ın kaydındaki "havai / yeraltı ayrımı yok" eksiğini kapatır (km'ye çevirmek için ~100 bin geometri inmeli; inmedi). Trafo kimliği yok → hat trafoya bağlanamaz.
4. **Capacités d'accueil du réseau — Corse** (`g2wxe-03pfyiy5x7l7573w9l`, 34 satır, 1 Ekim 2026): boş kapasite yalnız **34 ana indirici merkez** (HTB/HTA) için; ~8.200 mahalle trafosu için yok. Jüri cevabı adayı [Yorum]: EDF bile mahalle trafosu düzeyinde boş kapasite yayınlamıyor; Malta yayınlıyor (akıllı sayaç).
5. **Registre national des installations — Corse** (`eydtgekr285ytj5qxuu-972d`, 1.035 satır): üretim tesisleri, IRIS, bağlantı gerilimi (BT/HTA), kW. Belediye başına AG'ye bağlı PV ÷ konut teslim noktası (yayılma oranı) çıkarılabilir; düşük öncelik.

## Bulunamayan
- **Mahalle trafosu (HTA/BT) düzeyinde yük, gerilim ya da boş kapasite: BULAMADIM.** Korsika trafo konumları da yok (ulusal "Postes HTA/BT" Enedis'in; Korsika'yı EDF SEI işletir). Akıllı sayaç eğrileri yayınlanmıyor.
- 30 dakikalık Korsika'ya özel tüketim profili: BULAMADIM (ulusal Enedis agregaları Korsika'yı kapsamıyor).

## Sonuç
Bizim asıl eksiğimiz olan trafo düzeyi ölçüm Korsika'da da yok. İşe yarayan: (1) bahar kesintisi bulgusu (sunum ve jüri), (2) saatlik ada talebi (oran sağlaması), (3) havai/yeraltı hat ayrımı (benzetimdeki ABC havai varsayımına dış çapa). İndirme ve veri sözlüğü satırı ancak kullanılacaksa; şimdilik sözlükte "Adaylar".
