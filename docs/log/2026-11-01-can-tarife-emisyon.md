# 1 Kasım 2026 — Can — Tarife, mahsuplaşma, emisyon katsayısı, trafo değişim maliyeti (KARAR 09:46, 10:16 m. 3)

30 dakikalık zaman kutusu, Bulamadım akışı. Ham dosya indirilmedi (yalnız web sayfaları ve bir PDF okundu; PDF'in SHA-256'sı aşağıda). Hepsi pitch'in maliyet / etki kutusu için; modele girmez.

## Sonuç

| Ne | Bulunan | Etiket |
|---|---|---|
| Kıb-Tek konut tarifesi (tek zamanlı, aylık kademe) | 0–250 kWh **5,8614 TL**; 251–500 12,092; 501–750 13,0019; 751–1.000 14,0933; > 1.000 16,8444 TL/kWh; 1 Haziran 2026'dan (%22 zam; önceki 4,8044 / 9,9115 / 10,6573 / 11,5519 / 13,8069). Sabit ücret 110,58 TL/ay (zamma girip girmediği haberde belirsiz; 134,91 olabilir) | [Kaynaklı: Cyprus Mail, 26.05.2026, https://cyprus-mail.com/2026/05/26/norths-electricity-prices-rise-by-22 ; aynı rakamlar cyprus-faq.com "Electricity tariffs in Northern Cyprus" (Ekim 2026; "28 Temmuz 2026 Kıb-Tek belgesi değiştirmedi"), https://cyprus-faq.com/en/north/bytovye-voprosy/kakie-seichas-tarify-na-elektrichestvo ] — Kıb-Tek'in kendi tarife belgesi açılamadı (kibtek.com); ikincil kaynak |
| Konut üç zamanlı | gündüz (07–17) 12,092; puant (17–22) 16,7282; gece (22–07) 7,9711 TL/kWh | [Kaynaklı: Cyprus Mail, aynı haber] |
| Mahsuplaşma (şebekeye verilen kWh'nin bedeli / devri) | **BULAMADIM** | arama izi aşağıda |
| Şebeke emisyon katsayısı (Kuzey) | Kıb-Tek yalnız 6 numaralı fuel oil yakıyor; termik santrallerde **584–886 g CO₂/kWh**; özgül yakıt tüketimi 233,9 g/kWh. Sağlama: aynı tezde 2012'de 2.209.322 kWh güneş üretimi 1.590 t CO₂ azaltmış → **~720 g/kWh** [Hesap: 1.590 ÷ 2.209,3 MWh] | [Kaynaklı: Erciyas, O. (2014), "Sustainability Assessment of Photovoltaic Power Plants in North Cyprus", yüksek lisans tezi, DAÜ (EMU) Makine Müh., https://hdl.handle.net/11129/1625 — özet] — 2012–2014 karışımı; bugünkü Kıb-Tek / Aksa karışımı ve resmi katsayı BULAMADIM |
| Kıb-Tek trafo değişim / güçlendirme maliyeti | **BULAMADIM** (Kıb-Tek). Vekil: Türkiye TEDAŞ pozu, direk tipi trafo postası transformatörü 15,8 / 0,4 kV: 160 kVA 57.735,33; 250 kVA **72.755,59**; 400 kVA 89.525,40 TL/adet (yalnız transformatör, montaj ve hat hariç, Eylül 2022 fiyatı) | [Kaynaklı: TKDK, "İkame işlemlerinde kullanılacak özel poz tablosu", 28 Eylül 2022, poz 31.6.4.2-008 / -010 / -012 (TEDAŞ), https://www.tkdk.gov.tr/Dokuman/ikame-islemlerinde-kullanilacak-ozel-poz-tablosu-28-eylul-2022-1345 ; PDF SHA-256 7ea07d64ab6f7fd6ebfd5306fd1965e6c87ab9e268c35d3a5b54ec4ff543dd33] — Türkiye, 2022 TL, enflasyonla güncel değil; Kıb-Tek'e taşınmaz [Yorum] |

KTEMO PİD birim fiyat listesinde (Ekim 2024, depoda) dağıtım trafosu kalemi yok: yalnız ölçü akım trafosu, oto trafo yol verme, kompanzasyon [Hesap: `EKIM2024.pdf` metninde "trafo|kVA" taraması].

## Kullanım önerisi (pitch / dashboard maliyet kutusu) [Yorum]
- **Tarife:** "Bir panelli evin şebekeden çekmediği her kWh, ilk kademede 5,86 TL, üst kademelerde 12–17 TL." Geri ödeme hesabı **yapılmadı**: mahsuplaşma kuralı (devir, yıl sonu, fazla üretimin bedeli) bilinmeden yanlış olur.
- **Emisyon:** "Kuzey'in elektriği fuel oilden; her kWh ~0,6–0,9 kg CO₂ (2014 tezi)." Panel başına yıllık ton hesabı yapılacaksa panelin yıllık üretimi ayrı kaynakla ([Kaynaklı] ya da Open-Meteo'dan [Hesap]) ve sonuç aralık olarak; tek sayı yazılmaz.
- **Trafo değişimi:** Kıb-Tek rakamı yok; TEDAŞ 2022 vekili yalnız "trafo pahalı, ölçüm ucuz" sırası için ve "Türkiye, 2022, yalnız cihaz" etiketiyle. Pilot (~18,6 bin TL / trafo ölçümü, 2026) ile 2022 TL'si yan yana konmaz (enflasyon).

## Arama izi (Bulamadım akışı)
- Tarife: "Kıb-Tek elektrik tarifesi konut kWh fiyatı 2026"; "kibtek.com tarifeler konut tek zamanlı 5,8614" — kibtek.com tarife belgesine ulaşılamadı; Ekim 2024 tarife PDF'i (tak.gov.ct.tr) eski.
- Mahsuplaşma: "KKTC net metering mahsuplaşma Kıb-Tek fazla üretim kWh bedeli"; "KKTC yenilenebilir enerji yönetmeliği güneş paneli mahsuplaşma şebekeye verilen elektrik Kıb-Tek ödeme 2025" — yönetmelik metni, Resmi Gazete ya da Kıb-Tek duyurusu çıkmadı; ADR-0006'da da "mahsuplaşmadaki abone sayısı" BULAMADIM. Sonraki: Resmi Gazete'de "Yenilenebilir Enerji Kaynakları" tüzüğü, KKTC Elektrik Kurumu Yasası değişiklikleri, Kıb-Tek'e doğrudan soru (uzman listesine).
- Emisyon: "Northern Cyprus electricity grid emission factor kg CO2 per kWh Teknecik"; "TRNC electricity generation CO2 emissions tonnes per MWh fuel oil Kib-Tek study" — Ember / IEA'da Kuzey ayrı değil (GreenCalculus 0,489 kg/kWh Güney Kıbrıs, kullanılmaz). DAÜ tezleri (i-rep.emu.edu.tr) tek kaynak.
- Trafo maliyeti: "Kıb-Tek trafo değişimi maliyeti 250 kVA trafo fiyatı TL KKTC" — Kıb-Tek birim fiyatı çıkmadı; TKDK'nın TEDAŞ pozları bulundu; KTEMO listesinde kalem yok.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
