# 2026-11-01 — Can: pitch maliyet kutusunun BEKLİYOR kalemleri için kaba tahmin

**Etiket: [Hesap] / [Yorum], kaba.** Can (1 Kas): "maliyet için kesin bir rakam şart değil, tahmini değer yeterli." Rakam uydurulmaz: her tahmin kaynaklı bir fiyattan ya da adı konmuş bir varsayımdan. Girdi: Civan'ın pitch 6. slayt metni (Civan'ın günlüğü `2026-11-01-civan-pitch-maliyet.md`, Civan'dan yama olarak geldi), [Can'ın maliyet günlüğü](2026-11-01-can-maliyet.md), KARAR 09:46 (can.md).

## Hipotez / amaç
KARAR 09:46 (3) üç şeyin aranmasını istedi: Kıb-Tek konut tarifesi ve mahsuplaşma fiyatı, şebeke emisyon katsayısı, trafo değişim maliyeti. Bunlarla Civan'ın Kutu 3'ündeki "yıllık fayda (para)", "geri ödeme" ve "emisyon" BEKLİYOR'ları bir mertebeye iner mi?

## Yaptıklarım (arama izi)
1. **Konut tarifesi — buldum.** Kıb-Tek konut tarifesi, 1 Haziran 2026'dan beri (%22 zam), 28 Temmuz 2026 belgesinde değişmedi: 0–250 kWh 5,8614 TL; 251–500 12,0920; 501–750 13,0019; 751–1.000 14,0933; 1.000 üstü 16,8444 TL/kWh; sabit 110,58 TL/ay [Kaynaklı: cyprus-faq.com "Electricity tariffs in Northern Cyprus", Ekim 2026 sürümü, https://cyprus-faq.com/en/north/bytovye-voprosy/kakie-seichas-tarify-na-elektrichestvo ; zam haberi: Cyprus Mail 26.05.2026, https://cyprus-mail.com/2026/05/26/norths-electricity-prices-rise-by-22 ]. İkincil kaynak (Kıb-Tek'in kendi sayfası açılmadı); belge Kıb-Tek duyurusunu aktarıyor.
2. **Mahsuplaşma fiyatı — BULAMADIM.** Aramalar: "KKTC Kıb-Tek mahsuplaşma güneş paneli satış fiyatı kWh", "mahsuplaşma Kıb-Tek yenilenebilir enerji yönetmeliği fazla üretim kWh bedel"; cyprus-faq güneş paneli sayfası (fiyat yok, yalnız "Kıb-Tek kapasiteyi sınırlar"). Çıkanlar Türkiye EPDK kuralları (KKTC'ye uymaz). EMU 2020 tezi (PV maliyet-etkinliği, i-rep.emu.edu.tr) özetinde fiyat yok, açılmadı.
3. **Emisyon katsayısı — vekil buldum.** Kıb-Tek'in tek yakıtı 6 no. fuel oil; PV'nin termik santral yerine geçince önlediği CO₂ **584–886 g/kWh** [Kaynaklı: Erciyas, "Sustainability Assessment of Photovoltaic Power Plants in North Cyprus", EMU yüksek lisans tezi, 2014, https://i-rep.emu.edu.tr/items/e2115ea7-1187-40ac-8087-308934332196 ]. Arama özetinde bir KKTC enerji sunumu (EMO) ülke ortalaması ~0,75 kg/kWh diyor; dosya 404, okunmadı, kullanılmadı.
4. **Trafo değişim maliyeti — Kıb-Tek'inki BULAMADIM, vekil depoda.** Arama: "Kıb-Tek trafo ihalesi 250 kVA 400 kVA dağıtım transformatörü fiyat" (Kıb-Tek ihalesi çıkmadı; TEDAŞ 400 kVA kuru tip poz fiyatı var ama malzeme / montaj ayrımı belirsiz, kullanılmadı). Vekil: NIE Networks (Kuzey İrlanda), Ağustos 2024: direk trafosu 25 → 50 kVA 7.408 £; yeni 315 kVA trafo merkezi 50.000 £ [Kaynaklı: kapsamlı araştırma §5]. Kur 67,0171 TL/£ [Kaynaklı: TCMB 30.10.2026 döviz satış, https://www.tcmb.gov.tr/kurlar/202610/30102026.xml ].

## Sonuç [Hesap]

| Kutu 3 kalemi | Tahmin | Etiket |
|---|---|---|
| **Geri ödeme** (kaçınılan güçlendirme) | Pilot, **~5–7 gereksiz direk trafosu büyütmesini ya da ~1 yeni trafo merkezini** önlerse kendini öder | [Hesap: 7.408 £ × 67,02 = ~0,50 milyon TL; 50.000 £ = ~3,35 milyon TL; pilot 2,23–3,44 milyon TL ÷ 0,50 = 4,5–6,9; ÷ 3,35 = 0,7–1,0. Fiyat İngiltere'den, vekil; Kıb-Tek'inki BULAMADIM] |
| **Yıllık fayda (para)**, panel takan ev başına | ~26 bin TL/yıl elektrik faturası (sabit ücret hariç) | [Hesap: ortalama konut 3,69 MWh/yıl = 308 kWh/ay (Kıb-Tek 2023: 648.494 MWh ÷ 175.577); 250 × 5,8614 + 58 × 12,092 = 2.164 TL/ay. Varsayım: panel evin bütün tüketimini karşılar, mahsuplaşma fiyatı BULAMADIM; fayda ev sahibinin, Kıb-Tek'in geliri o kadar düşer] |
| | İlk 20 ölçümün açtığı 64–133 ev panel takarsa ~1,7–3,5 milyon TL/yıl | [Hesap: × 25.970 TL; 64–133 ev farazi şehirler 31–50, gösterim (dashboard `icerik.json`); "takarsa" Yorum] |
| **Emisyon etkisi**, panel takan ev başına | ~6–9 ton CO₂/yıl | [Hesap: 6,5 kW × 1.600 kWh/kWp = 10.400 kWh/yıl × 0,584–0,886 kg/kWh; 6,5 kW Yorum, 1.600 kWh/kWp Yorum (KARAR, volkan.md); katsayı Kaynaklı: Erciyas 2014] |
| | 64–133 ev takarsa ~390–1.230 ton CO₂/yıl | [Hesap; farazi şehir, gösterim] |

Okunuş: pilotun nakit karşılığı ilk 20 ölçümün açtığı evlerin bir yıllık faturasına yakın; asıl kalem, gereksiz trafo büyütmesinden kaçınmak (KARAR 09:46'nın "en değerli" dediği). İkisi de mertebe, kesinlik iddiası yok.

## Kararlar (Can'ın yetkisinde; sorulmadan verildi)
1. **Toplamın iki okunuşu (Civan'ın sorusu):** pitch'in başlık rakamı sunum ve dashboard'la aynı: **~2,2–3,2 milyon TL (~40–57 bin €)**, cihazlar 3 yıla bölünmüş. Nakit çıkışı **~2,7–3,4 milyon TL** küçük yazıda kalır ("fark: 3 cihaz pilottan sonra 64–114 ölçüm daha yapar"). Neden: KARAR 09:43, rakam kaynağı `dashboard/icerik.json`; aynı soruya üç yerde iki sayı jüriye kötü görünür.
2. **Kutu 3, "Fayda (para dışı)":** Civan "22/44" (şehir 21–30) yazmış; resmi rakam **24/46 ↔ 0** (şehir 31–40, `icerik.json`, KARAR 01:20). 24/46 kullanılır.
3. **Geliştirme / bakım:** KARAR 09:46 (2) "para karşılığı uydurulmaz, nitel cümle" dedi; pitch o cümleyle kalır. Kaynaklı ücretten bir tahmin hazır: 2 gün × 3 kişi × 8 saat × 3.544,65 TL (EMO saat ücreti) = **~170 bin TL (~3 bin €)** [Hesap]. Kararın değişmesi Volkan'ın işi; volkan.md'ye yazıldı.

## Aynı günün öbür araması ile fark
Başka bir Can oturumu aynı aramayı aynı saatlerde yaptı ([tarife / emisyon günlüğü](2026-11-01-can-tarife-emisyon.md)); tarife ve emisyon rakamları birebir aynı kaynaklardan. İki fark: (a) orada geri ödeme "mahsuplaşma bilinmeden yapılmadı"; burada geri ödeme mahsuplaşmaya değil **kaçınılan trafo büyütmesine** dayanıyor, o yüzden yapılabildi. (b) Orada vekil TEDAŞ 2022 pozu (250 kVA 72.755,59 TL, yalnız cihaz) bulundu, 2026 pilotuyla yan yana konmadı; burada NIE 2024 (montajlı iş, £) kullanıldı: daha yeni ve işçilik dahil, ama İngiltere [Yorum]. Sabit ücret orada "110,58 ya da 134,91" belirsiz; burada sabit ücret hesaba girmedi.

## Sıradaki adım
- Civan'a: kutu metinleri (civan.md).
- Volkan'a: geliştirme tahmini için bir satırlık soru (volkan.md); dashboard'a geri ödeme / emisyon satırı isteniyorsa `icerik.json` Volkan'ın dosyası.
- İsterse biri: Kıb-Tek mahsuplaşma fiyatı ve gerçek trafo değişim maliyeti uzmana soru (Muhittin; dış mesaj Volkan'ın).

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
