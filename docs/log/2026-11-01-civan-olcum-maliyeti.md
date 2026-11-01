# 1 Kasım 2026 — Civan — Bir trafoyu ölçmenin maliyeti (EMO belgeleri)

Amaç: sunumun 6. maddesi ("Pilot: ne kadar ölçüm, ne kadar maliyet") ve "sarı trafoya ölçüm cihazı tak" cümlesi için kaynaklı bir maliyet.

## Arama izi

- `https://ktmmob.org/dokumanlar` tarandı (tarayıcıyla; Firecrawl CLI bu makinede kurulu değil). Maliyete yarar bir şey yok: Eurocodes yapı el kitabı (2018), "yakında" işaretli iki örnek form, TMMOB bağlantısı. `ktmmob.org/mevzuat`'ta da ücret tarifesi yok (yasa, tüzük, bilirkişi yönetmeliği).
- `ktmmob.org/odalar` → Elektrik Mühendisleri Odası'nın sitesi `ktemo.org`. Asıl kaynak `https://www.ktemo.org/dokumanlar.php` ve `laboratuvar.php`.
- İndirilen (1 Kasım 2026; `data/raw/ktemo-birim-fiyat/`, git dışı; KAYNAK.txt Can'ın kutusunda istendi):
  - PİD Elektrik Tesisatları Asgari Birim Fiyat Listesi, Ekim 2024 — `https://www.ktemo.org/files/teknikbilgiler/EKIM2024.pdf`
  - Proje Hazırlama ve Kontrollük Asgari Birim Fiyat Rev.13 (xls + kontrollük pdf; xls son kayıt Mayıs 2026) — `https://www.ktemo.org/files/uploads/1780990679_Proje_Haz__rlama_ve_Kontroll__k_Asgari_Birim_Fiyat_Rev.13.xls`, `https://www.ktemo.org/files/uploads/1780990699_Proje_Haz__rlama_ve_Kontroll__k_Asgari_Birim_Fiyat_Rev.13-kontrolluk.pdf`
  - Yeni Proje Vize ve Tadilat Ücretleri (Eylül 2023) — `https://www.ktemo.org/files/teknikbilgiler/YEN%C4%B0%20PROJE%20V%C4%B0ZE%20%C3%9CCRETLER%C4%B0.pdf`
  - EMO laboratuvarı Deney Kapsamı — `https://www.ktemo.org/files/DeneyKapsami.pdf`
- PDF metni `pdftotext -table` ile okundu; `-layout` fiyat sütununu bir satır kaydırıyor (ilk okumada akım trafosu fiyatı yanlış satırda göründü).

## Kaynaklı rakamlar

| Kalem | Değer | Kaynak |
|---|---|---|
| Ölçü akım trafosu 100–500/5 A, sınıf 0,5–1, temin + montaj | 3.286 TL/adet | PİD Ekim 2024, C3.1 |
| Ölçü akım trafosu 501–2000/5 A | 8.474 TL/adet | PİD Ekim 2024, C3.2 |
| Galvaniz pano 70×50×30 (üç faz 63 A tek sayaç) | 8.376 TL | PİD Ekim 2024, A1 madde 4 |
| Mühendis ek kontrollük saat ücreti | asgari ücretin %5'i / saat; gidiş başı = saat × süre (yol dahil) | EMO Rev.13 kontrollük, "Hesaplama yöntemi" |
| KKTC asgari ücret (16 Temmuz 2026 haberi) | brüt 70.893 TL, net 61.677 TL | [gzt.com](https://www.gzt.com/ekonomi/kktc-asgari-ucret-2026-son-dakika-yeni-asgari-ucret-belli-oldu-kktcde-net-ve-brut-asgari-ucret-ne-kadar-4241979) |
| Fluke 1736/EUS üç faz güç kaydedici, 4 esnek 1500 A pens dahil | 6.164 € (KDV hariç) | [datatec.eu](https://datatec.eu/at/en/fluke-fluke-1736-eus), 1 Kasım 2026 |
| EUR/TRY döviz satış | 55,8153 | TCMB `today.xml`, 30.10.2026 |

EMO laboratuvarının deney kapsamı cihaz/malzeme deneyleri (60335, RCD, kablo direnci, topraklama direnci); **trafo yük ölçümü hizmeti yok**.

## Hesap

[Hesap] Mühendis saati = 70.893 × %5 = **3.544,65 TL** (brüt asgari ücretle; net alınırsa 3.083,85). EMO belgesi brüt/net demiyor, yüksek olanı aldım [Yorum].

**A — Taşınabilir kaydedici (önerilen; sarı trafoya "geçici cihaz" bu).** Pensler kabloya sarılır; akım trafosu, pano ve kesinti gerekmez. 1500 A pens 1000 kVA trafoya yeter ([Hesap] 1000 kVA, 415 V → 1.391 A).

| | TL |
|---|---|
| Cihaz (6.164 € × 55,8153) | 344.046 |
| Ölçüm başına işçilik: 2 gidiş (tak + sök) × 2 saat [Yorum: süre] × 3.544,65 | 14.179 |
| Ölçüm başına toplam, cihaz 1 yılda 26 ölçüm (2 haftalık ölçüm [Yorum]) | **27.411** |
| Aynısı, cihaz 3 yılda 78 ölçüm | **18.589** |

Pilot, 12 trafo (modelin ölçülü trafo sayısı, n = 12):

| Düzen | Süre | TL |
|---|---|---|
| 12 cihaz, hepsi aynı anda | 2 hafta | 4.298.689 |
| 3 cihaz, sırayla | 8 hafta | **1.202.280** |
| 1 cihaz, sırayla | 24 hafta | 514.189 |

**B — Kalıcı panel analizörü (trafo başına sabit).**

| | 100–250 kVA | 400–1000 kVA |
|---|---|---|
| 3 akım trafosu (250 kVA 348 A → C3.1; 400 kVA 556 A → C3.2) | 9.858 | 25.422 |
| Pano | 8.376 | 8.376 |
| Panel analizörü: BULAMADIM (doğrulanmış fiyat). Aramada RS Belçika'da Entes MPR-46S 323,25 € (KDV hariç) göründü, sayfa açılamadı → 18.042 [Yorum] | 18.042 | 18.042 |
| Mühendis, 1 gidiş × 3 saat [Yorum] | 10.634 | 10.634 |
| **Toplam** | **46.910** | **62.474** |

B'de eksik: veri iletimi (GSM modem, hat ücreti) BULAMADIM; akım trafosunu canlı baraya takmak Kıb-Tek kesintisi isteyebilir, maliyeti yok.

## Eksiler ve uyarılar

- PİD fiyatları **Ekim 2024**; bugüne enflasyonla güncellenmedi. B'nin akım trafosu ve pano satırları düşük kalır.
- Fluke fiyatı Avusturya bayisinin KDV hariç fiyatı; KKTC gümrük, KDV, nakliye yok. Arama özetindeki 4.140 € eski çıktı, sayfada 6.164 €.
- Kıb-Tek personelinin trafoya erişim için eşlik süresi ve araç maliyeti dahil değil.
- Ölçüm süresi (2 hafta) ve gidiş süreleri [Yorum]; uzmana sorulacak (yük analizörü sorusu, `docs/01-plan.md` soru 2–8).

## Sonuç

[Hesap] Bir trafoyu taşınabilir kaydediciyle ölçmek ~**18–27 bin TL**; 12 trafoluk pilot 3 cihazla 8 haftada ~**1,2 milyon TL**. Her trafoya kalıcı cihaz ~**47–62 bin TL** + iletişim. Kuzey'in tüm trafolarına (vekil ~6.400–6.700, `docs/data/data-dictionary.md`) kalıcı cihaz [Hesap] 6.400 × 46.910 ≈ **300 milyon TL** ile 6.700 × 62.474 ≈ **419 milyon TL** arası; pilotun ~250–350 katı. Sunum cümlesi önerisi: "Her trafoya cihaz takmak yerine 3 cihazı sarı trafolarda dolaştırıyoruz."
