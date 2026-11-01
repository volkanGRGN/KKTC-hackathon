# 2026-11-01 — KTEMO dokümanları: yük haritası için kayda değer rakamlar

**Amaç:** Volkan'ın sorusu: ktemo.org/dokumanlar.php'den kayda değer veri çıkar mı. BUILD 1 (yük) tarayıp yük tarafına ve panel tarafına (KARAR üzerinden) ayırdı. Belgelerin adresi, boyutu ve SHA-256'sı `data/raw/ktemo-dokumanlar/KAYNAK.txt`'te; birim fiyat listeleri `data/raw/ktemo-birim-fiyat/` (Civan / Can).

## Taranan belgeler
Sayfada ~60 belge var. Okunanlar: Teknik Komite bildirimleri 1–4, reaktif güç kompanzasyonu, Kıb-Tek reaktif bilgilendirme toplantısı, Solar Enerji Projelendirme sunumu, 2. Ulusal Enerji Verimliliği Çalıştayı (2023), Enerjide Aküye Bakış raporu (Haziran 2026), Kıb-Tek Yakıt Değişim Fizibilite sunumu (RAR içinde pptx), Enerji Depolamaya Odaklı Ağ Çalışması (RAR içinde pptx), Volkan'ın gönderdiği Birim Fiyat PİD Ekim 2024.
Şebeke verisi içermeyenler: yönetmelik ve rehberler (bina içi tesisat; Fotovoltaik Uygulama Rehberi İngiltere IET uygulama kodunun çevirisi), formlar, birim fiyatlar (bina içi tesisat). Depolama sunumu Güney Kıbrıs'ın (EAC) 2019 santral listesi.

## Yük tarafı [Kaynaklı]
1. **Sistem puantı ve yıllık enerji** — Kıb-Tek Yakıt Değişim Fizibilite sunumu (2022), slayt 38, "Yıl / Puant Güç MW / Enerji GWh": 2022 368 MW / 1.836 GWh; 2023 386 / 1.927; 2024 405 / 2.024; 2025 425 / 2.125; 2026 447 / 2.231 (2023 sonrası projeksiyon; 2022 satırının ölçüm mü tahmin mi olduğu sunumda yazmıyor). Kıb-Tek istatistik dosyalarımızda (stat_2023 / 2024) puant yok. Sistem tepe ÷ yıllık ortalama = 368 ÷ (1.836 GWh ÷ 8.760 h) = **1,76** [Hesap]. Deneme şehirleriyle karşılaştırma aşağıda.
2. **Tek tesisatın öngörülen puant gücü** — Teknik Komite Düzeltme Bildirim No-1 (8.06.2018), s. 1: müstakil konut tek faz 5 kVA, üç faz 8 kVA; apartman dairesi 4 kVA; dükkân tek faz 5, üç faz en az 8 kVA; apartman ortak kısım 1 / 8 kVA. Puant gücü 25 kVA üstü yapılarda Kıb-Tek görüşü zorunlu → Kıb-Tek'te büyük yapıların öngörülen puant kayıtları var (KARAR 01:25: istek metni madde 9'a eklendi). Proje değeri (tek ev, eşzamansız), ölçüm değil; eşzamanlılık fitinin tek ev ucu için bilgi (Can'ın B-Y2'si).
3. **Güç katsayısı kuralı** — "Güç katsayısının düzeltilmesi", s. 3–4 (Bakanlar Kurulu Önerge 2227/2010): kurulu gücü 25 kVA ve üstü konut dışı tesislerde ve bütün üç fazlı konutlarda kompanzasyon zorunlu, proje cos φ 0,90–1'e göre; tek fazlı konutta şart yok. s. 5: KTEMO'nun Kıb-Tek'e önerisi, reaktif aktifin %33'ünü (cos φ 0,95) aşarsa faturalansın. Modelin `pf_varsayim` 0,95'i kuralın üst tarafında; temkinli uç 0,90 → `tepe_kva` +%5,6 (sözleşme §8 notu).
4. **Kıb-Tek kompanzasyonu OG'de** — reaktif bilgilendirme, s. 15–18: kompanzasyon 11 / 22 kV trafo merkezlerinde otomatik (Güneşköy, Çamlıbel, Alsancak, Girne 1 / 2, Meriç, Geçitkale, Kalecik, Ecvet Yusuf ve Gönyeli yük tevzi, Haspolat, Yeniboğaziçi, Mağusa 1…; kapasitör 1.500–3.000 kVAr). OG fider / merkez tepe isteği (madde 8) için merkez adları.
5. **Yaz ve kış pik talebi** — Enerjide Aküye Bakış raporu (13 Haziran 2026), s. 3: "yaz ve kış aylarında oluşan pik talep" emre amade kapasiteyi zorluyor; s. 10, kısa vade: "kritik pik talep bölgelerinde hızlı devreye alınabilecek projelere öncelik". Yük haritasının yaptığı iş; sunum cümlesi.

## Panel tarafı (KARAR üzerinden BUILD 2'ye ve Can'a gitti) [Kaynaklı]
- Solar Projelendirme sunumu (Yrd. Doç. Dr. Mehmet Şenol), s. 3: 2018 sonu PV 21 MWp devrede, 36 MWp kurulum izinli, 10 MWp bekleyen, Kıb-Tek ihale kotası 10 MWp, toplam dolmuş kota 77 MWp; 2019'un ilk 6 ayında 1.300'ü aşkın başvuru. s. 5: kurulu güç 405 MW.
- 2. Ulusal Enerji Verimliliği Çalıştayı (25 Ağustos 2023), s. 14: konut GES kurulumlarını 3 kW ile sınırlama önerisi.
- Birim Fiyat PİD Ekim 2024, J1: fotovoltaik sistem kW başına asgari 800 € (sunumda maliyet cümlesi).

## Sistem puantıyla karşılaştırma (sonuç)
Deneme şehirlerinde (üretici 1.5, 1–10) toplam yükün tepe ÷ ortalaması: üretici 1,95, model (trafo tahminlerinin eşzamanlı toplamı) 2,30; Kıb-Tek 1,76. Ayrıntı ve çekinceler [günlükte](2026-11-01-volkan-yuk-uretici15.md).

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
