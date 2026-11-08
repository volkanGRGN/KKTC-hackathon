# 2026-11-01 — Volkan (MALİYET oturumu): sunuma girecek maliyet rakamları, sınanmış

**Etiket: [Hesap] / [Kaynaklı] / [Yorum], her satırda ayrı.** Volkan (1 Kas): "maliyet verilerini gerçeğe yakın yap, sunuma koyacağız." Kurallar: KARAR 09:46 "para uydurulmaz" (can.md; vekil kullanılırsa vekil diye yazılır), KARAR 11:43 m. 2 (~170 bin TL'nin adı "prototip emeği", "geliştirme maliyeti" denmez) ve m. 1 (tarife ve emisyon dashboard tablosuna girmez, slaytta bağlam). Girdi: [Can'ın maliyet günlüğü](2026-11-01-can-maliyet.md), [pitch tahmini](2026-11-01-can-pitch-maliyet-tahmin.md), [tarife / emisyon](2026-11-01-can-tarife-emisyon.md), [Civan'ın ölçüm maliyeti](2026-11-01-civan-olcum-maliyeti.md), `docs/sunum/slaytlar.md` slayt 8 ve "Maliyet", `dashboard/icerik.json` maliyet kartları. Zaman kutusu ~45 dk; yeni ham dosya indirilmedi.

## Hipotez / amaç
Sunumdaki maliyet rakamları kaynaklı mı, kuru güncel mi, KKTC'ye uyuyor mu? Zayıf vekiller (cihaz fiyatı, trafo fiyatı, mahsuplaşma, trafo sayısı) daha iyi kaynakla değiştirilebilir mi?

## Manşet önerisi
"Bir trafoyu ölçmek yaklaşık 19 bin TL; 120–170 trafoluk pilot 2,2–3,2 milyon TL, her trafoya kalıcı cihaz takmanın yaklaşık yüzde biri."

## Sunuma girecek maliyet

Kur: 1 € = 55,8153 TL, 1 £ = 67,0171 TL (TCMB döviz satış, 30.10.2026; 31 Ekim–1 Kasım hafta sonu, 1 Kasım'ın geçerli kuru bu — `tcmb.gov.tr/kurlar/today.xml` 1 Kasım'da hâlâ 30.10.2026 bülteni 2026/204).

| # | Ne | Rakam | Etiket | Tarih |
|---|---|---|---|---|
| 1 | Bir trafoyu taşınabilir cihazla ölçmek (cihaz 3 yılda 78 ölçüme bölünür; 2 gidiş × 2 saat mühendis) | **~18,6–19,0 bin TL (~333–341 €)** | [Hesap: cihaz 6.164–6.790 € × kur ÷ 78 + 14.179 TL işçilik; cihaz Kaynaklı: datatec.eu 6.164 € (1 Kas 2026), Lieske 6.618–6.790 € (KDV hariç, 2026); işçilik Kaynaklı: EMO Rev.13 saat = asgari ücretin %5'i, KKTC brüt asgari ücret 70.893 TL (Temmuz 2026); süreler Yorum] | Kas 2026 |
| 2 | Kıbrıs pilotu, 120–170 trafo | **~2,2–3,2 milyon TL (~40–58 bin €)** | [Hesap: satır 1 × 120–170 = 2,23–3,24 milyon TL; 120–170 Hesap: araştırma §7] | Kas 2026 |
| 3 | Pilotun Kuzey'deki trafolara oranı | **~%2–3** | [Hesap: 120 ÷ 6.700 = %1,8; 170 ÷ 6.400 = %2,7; trafo sayısı vekil, satır 8] | — |
| 4 | Başlangıçta 3 cihaz almak (nakit) | **~1,03–1,14 milyon TL (~18,5–20,4 bin €)** | [Hesap: 3 × 6.164–6.790 € × kur] | Kas 2026 |
| 5 | Kıyas: her trafoya kalıcı cihaz | **~300–419 milyon TL (~5,4–7,5 milyon €)** | [Hesap: Civan B tablosu, 46.910–62.474 TL/trafo × 6.400–6.700; akım trafosu ve pano KTEMO PİD Ekim 2024 (enflasyonla güncel değil, düşük kalır); panel analizörü fiyatı Yorum (doğrulanmadı)] | Eki 2024 / Kas 2026 |
| 6 | Pilot ÷ kalıcı cihaz | **~%0,5–1** ("yaklaşık yüzde biri") | [Hesap: 2,23 ÷ 419 = %0,53; 3,24 ÷ 300 = %1,08] | — |
| 7 | Prototip emeği (2 gün × 3 kişi, EMO saat ücreti) | **~170 bin TL (~3 bin €)** | [Hesap: 48 saat × 3.544,65 TL = 170.143 TL; KARAR 11:43 m. 2: "geliştirme maliyeti" denmez, pilotun geliştirme ve bakımı nitel cümle] | Kas 2026 |
| 8 | Kuzey'deki dağıtım trafosu sayısı | **~6.400–6.700** | [Hesap, vekil: 219.931 tüketici ÷ trafo başına 34,4 (Güney) ya da 32,9 (Korsika); Kıb-Tek sayısı BULAMADIM] | — |
| 9 | Bağlam (yalnız konuşmada, soru gelirse): kaçınılan bir trafo büyütmesi | İngiltere'de bir direk trafosunu 25 → 50 kVA büyütmek **~0,5 milyon TL** (7.408 £); yeni 315 kVA trafo merkezi **~3,35 milyon TL** (50.000 £) → pilot ~5–7 büyütmeyi ya da ~1 trafo merkezini önlerse kendini öder | [Hesap, vekil: NIE Networks Ağustos 2024 (kapsamlı araştırma §5), montajlı iş; Kıb-Tek'in maliyeti BULAMADIM; İngiltere işçiliği pahalı, KKTC'de düşük olabilir — Yorum] | Ağu 2024 |
| 10 | Bağlam: ortalama konutun yıllık elektrik faturası | **~26 bin TL/yıl** (sabit ücret hariç; ile ~27,3 bin) | [Hesap: 308 kWh/ay (Kıb-Tek 2023: 648.494 MWh ÷ 175.577 konut) × Haziran 2026 kademeleri; tarife Kaynaklı ama ikincil: Cyprus Mail 26.05.2026, cyprus-faq.com] | Haz 2026 |
| 11 | Bağlam: Kuzey'in elektriğinin emisyonu | **~0,58–0,89 kg CO₂/kWh** | [Kaynaklı: Erciyas 2014, DAÜ tezi; 6 no. fuel oil; eski, resmi katsayı BULAMADIM] | 2014 |

Değişen rakam yok denecek kadar az: yalnız cihazın pahalı satıcıdaki fiyatı aralığın üst ucunu ~%2 kaldırıyor (333 → 341 €, 57 → 58 bin €), başlangıç nakdinin üstü 1,03 → 1,14 milyon TL. Dashboard'daki "~333 €", "~40–57 bin €" alt uç olarak doğru kalır; değiştirmek şart değil [Yorum].

**Dahil değil (sunumda söylenir):** KKTC'ye getirme maliyeti (KDV, gümrük, nakliye); Kıb-Tek personelinin eşlik süresi ve aracı; kalıcı cihazda veri iletimi (modem, hat); enflasyon (KTEMO PİD Ekim 2024).

## Sınama: rakam rakam
- **Kur:** TCMB 30.10.2026 bülteni, 1 Kasım'da da yürürlükte (hafta sonu). Doğru.
- **Fluke 1736/EUS:** datatec.eu 6.164 € (Civan, 1 Kas) en düşük; Lieske (industry-electronics.com) 6.617,70 € (20.03.2026 kaydı) ve 6.789,84 € (KDV hariç, sayfa şimdiki), 2+ adette ~6.400–6.500 €. RS / Bürklin'de 1736/B (pensiz) 5.526 € KDV hariç. Aralık 6.164–6.790 € olarak alındı. Daha ucuz cihaz (ör. Hioki) aranmadı: ölçüm sınıfı farklı olur, karar uzmanın [Yorum].
- **Mühendis saati:** EMO Rev.13 kontrollük (asgari ücretin %5'i) + KKTC brüt asgari ücret Temmuz 2026 (gzt.com). Brüt alındı (yüksek olan). Yeni bir asgari ücret kararı aranmadı.
- **Pilot 120–170, kalıcı cihaz kıyası, %1:** hesaplar yeniden yapıldı, tutuyor.
- **Slayt 8'de "adadaki ~6.400 trafonun ~%2'si":** vekil Kuzey için (Güney'in oranıyla); "adadaki" yanlış okunur. Öneri: "Kuzey'deki ~6.400–6.700 trafonun (vekil) ~%2–3'ü". `docs/sunum/` Can'ın; değişiklik Volkan'ın sözüyle.
- **Dashboard kartı (`icerik.json`, "pilot, her trafoya kalıcı cihazın…" açıklaması):** "Geri ödeme ve emisyon hesaplanmadı: … aranıyor" artık eski (arama yapıldı; KARAR 11:43). Öneri: "Geri ödeme hesaplanmadı: Kıb-Tek'in trafo büyütme maliyeti ve mahsuplaşma bedeli bulunamadı." `dashboard/` dashboard oturumunun; PR #46 aynı dosyanın yazılarını değiştiriyor, bu oturum dokunmadı.
- **Ev başına fatura 26 bin TL:** hesap tutuyor (2.166,7 TL/ay × 12). "Panel takan evin kazancı" diye söylenmez: mahsuplaşma bilinmiyor, ev bütün tüketimini panelden karşılamaz [Yorum].
- **Emisyon ev başına 6–9 t CO₂/yıl:** 10.400 kWh × 0,584–0,886 = 6,1–9,2 t; 6,5 kW ve 1.600 kWh/kWp Yorum. Sunumda tek sayı yok, aralık.

## Arama izi (Bulamadım akışı)
- **Mahsuplaşmada fazla üretimin bedeli — BULAMADIM.** "Kıb-Tek mahsuplaşma yönetmeliği güneş paneli fazla üretim şebekeye verilen elektrik bedeli 2026"; "North Cyprus solar panel net metering Kib-Tek excess electricity paid price per kWh"; "KKTC çatı güneş paneli Kıb-Tek mahsup fazla enerji yıl sonu sıfırlanır … tüzüğü". Çıkanlar: Türkiye EPDK (Nisan 2026 saatlik mahsuplaşma, 30.04.2026 kurul kararı — KKTC'ye uymaz), Güney Kıbrıs (1 Ocak 2026'dan yeni başvuruya yalnız net billing, 11 sent/kWh — başka ülke), cyprus-faq güneş paneli rehberi (yalnız "Kıb-Tek kapasiteyi sınırlar", fiyat yok), DAÜ 2023 PV maliyet tezi (özet, fiyat yok). Sonraki: KKTC Resmi Gazete, Kıb-Tek'e soru (uzman listesinde, KARAR 11:43 m. 1).
- **Kıb-Tek dağıtım trafosu sayısı — BULAMADIM.** "Kıb-Tek dağıtım trafosu sayısı adet KKTC elektrik dağıtım şebekesi trafo": haberler, EMO 2012 yazısı; envanter yok. Vekil ~6.400–6.700 kalır.
- **Dağıtım trafosu (250–630 kVA) birim fiyatı ve montajı — Kıb-Tek'inki BULAMADIM; daha iyi vekil de doğrulanamadı.** "Çevre Şehircilik Bakanlığı 2026 elektrik birim fiyatları trafo 250/400/630 kVA" (2026 cetvelinde kVA'lı trafo pozu görünmedi, cetvel lisanslı yazılımda); "TEDAŞ 2026 birim fiyat direk tipi transformatör 250 kVA montaj"; "250 kVA yağlı tip dağıtım trafosu fiyatı 2026 TL". Arama özetinde TEDAŞ kuru tip 250 kVA (bina içi) Aralık 2025: 704.644,73 TL + 42.542,91 TL montaj görüldü; ama birimfiyat.com sayfaları HTTP 500 verdi (dört sayfa, 1 Kas), rakam okunamadı, bir başka özet aynı pozun 2025 satırını boş gösteriyor. **Kullanılmadı.** Kuru tip direk trafosu değil, pahalıdır. Sunumda Kıb-Tek trafo maliyeti yerine yalnız NIE 2024 vekili (satır 9), etiketiyle ve yalnız soru gelirse.
- **TEDAŞ 2022 vekili (250 kVA 72.755 TL, yalnız cihaz):** 2022 TL'si ve montajsız; 2026 pilotuyla yan yana konmaz (Can'ın günlüğüyle aynı karar).

## Karar / sıradaki adım
- Tablo sunuma ve pitch maliyet kutusuna aday; slayt 8 ve dashboard metni için iki öneri yukarıda (Can'ın ve dashboard oturumunun dosyaları; Volkan'ın sözüyle).
- Açık sorular uzmana (Kıb-Tek): mahsuplaşmada fazla üretimin bedeli; bir dağıtım trafosunu büyütmenin maliyeti; dağıtım trafosu sayısı.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
