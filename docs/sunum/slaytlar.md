# Slayt listesi (iskelet)

Akış: **yük haritası öne** (Volkan 09:43; sıra KARAR 10:16): sorun → yük haritası (doluluk, yılın tepesi "ön", akşam 207 V) → neden inanılır (İspanya öğlen %25 → %10, Mayıs tepesi %15, bant %82) → panel güvenli uçlar (0/60, 15/22, renksiz %76, 24/46 ↔ 0) → pilot ve maliyet → jüri cevapları. Tek cümle: *"Kıbrıs'ı ölçemiyoruz; yöntemi ölçebildiğimiz her şeyde kanıtlıyoruz, sonra uyguluyoruz."* Her slaytta tek iddia + tek rakam. Manşet rakam: **İspanya %25 → %10.**

Rakam kaynağı `dashboard/icerik.json` (KARAR 09:43). Yük rakamları yeni tepe modeli B-Y2, hiç bakılmamış sınav şehirleri 41–50 (KARAR 10:26, 10:43); panel rakamları 31–40. İkisi de üretici 1.5, farazi, **gösterim**. Eski yük rakamları (%5,8 / %15,1; 16/16, 87 uyarı; "yeterli" 233) ve "%27 → %19" (eski yanlış kırmızı ölçüsü, KARAR 10:16) kullanılmaz.

Süre hedefi 5–7 dk; dakika sütunu kaba [Yorum].

| # | Slayt | Tek iddia | Rakam ve etiket | dk |
|---|---|---|---|---|
| 1 | Sorun | Kuzey'de çatı güneşi başvuruları bekliyor; Kıb-Tek mahalle trafolarını göremiyor | ~2.670 bekleyen başvuru, çoğu 5–8 kW; alçak/orta gerilimde izleme sistemi yok [Kaynaklı: KTTO raporu, Mart 2023; adres doğrulanmadı] (karar masası 17:38; bulunursa değişir) | 0,5 |
| 2 | Neden şimdi | Güney bağladı, şimdi üretimi kısıyor | 2025'te dağıtıma bağlı güneşin %47,44'ü kısıldı, Ocak–Mayıs 2026 %65 [Kaynaklı: pv-magazine.com 13.01.2026 ve 15.06.2026] | 0,5 |
| 3 | Fikir | Az trafoyu ölç, gerisini şablonla tahmin et (İngiltere'nin yöntemi); her trafoya iki soru: ne kadar dolu, güneşe ne kadar yer var | İngiltere 824 trafoyu (%2,6) ölçüp gerisini ~%80 doğrulukla tahmin etti; başka şirketlerin 284 trafosunda %80–90 [Kaynaklı: Ofgem WPD LV Templates raporları 2013, 2015]. İki an: yılın tepesi (çoğunlukla yaz akşamı; sınır trafo gücü ve 207 V) ve bahar öğleni (11–14; sınır 259 V, inverter 264 V'ta kapanır) [Kaynaklı: ADR-0002, ADR-0014] | 0,75 |
| 4 | Yük haritası — trafo ne kadar dolu | Hangi trafonun dolu olduğunu kaçırmadan "önce buraya bak" listesi veriyoruz | **%80'den dolu 12/12 yakalanır**; bedeli: 124 uyarının 12'si gerçek (her 10 uyarıdan 1'i) [Hesap: sınav şehirleri 41–50 (hiç bakılmamış), üretici 1.5, ölçülmeyen 280 trafo, tepe modeli B-Y2; docs/log/2026-11-01-can-eszamanlilik.md; `dashboard/icerik.json`] — **gösterim**. Yılın tepesi "ön" etiketiyle: hata ortanca %11,4, en kötü onda birlik dilim %23,9; tahmin gerçeğin ortanca %11 üstünde (güvenli yön), gerçek hiçbir trafoda bandın üstüne çıkmadı [Hesap: aynı] | 1 |
| 5 | Yük haritası — akşam gerilimi | "Yeterli" dediğimiz trafo akşam 207 voltun altına inmiyor | **"Yeterli" 211 trafonun 0'ı** gerçekte 207 V altında; altına inen 2 trafonun 2'si yakalandı; 69 uyarının 2'si gerçek [Hesap: aynı küme] — **gösterim** | 0,5 |
| 6 | Neden inanılır — güven merdiveni | Yöntemi ölçebildiğimiz her yerde sınadık; farazi şehir üst sınırdır | **MANŞET — İspanya, 29 gerçek trafo, öğlen yükü: yalnız müşteri sayısıyla ~%25, faturayla ~%10 ortanca hata** [Hesap: PR #10, docs/log/2026-10-31-volkan-edp-gercek.md; veri Arboleya vd. 2019, CC BY]. Konuşmada açılan basamaklar: İspanya yılın (Mayıs) tepesi %15,4 / %36,1 [gerçek veri; docs/log/2026-11-01-volkan-yuk-tepe-on.md]; %80 aralık gerçekte %82,1 tuttu [gerçek veri, 28 trafo; docs/log/2026-11-01-volkan-faz7-kalibrasyon.md]; İngiltere gerilim: 6 gerçek hattın 5'inde ölçülen yükselme hesabın güvenli sınırının altında, birinde (Bancroft) küçük gördük → yeşil önce pilotla sınanır [Hesap: PR #11 + docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md; UKPN 2015, CC BY]; deneme şehrinde öğlen hatası %11,3 / %28, gerçekle aynı seviye [Hesap: sınav 31–40, üretici 1.5; `dashboard/icerik.json`; gösterim, üst sınır] | 1,25 |
| 7 | Panel — güvenli uçlar (canlı harita + kilit grafik) | Dolu trafoya "yer var" demiyoruz; bugünkü %40 kuralı diyor | **KİLİT GRAFİK: dolu trafoya "yer var" — %40 kuralı 46 dolu trafonun 24'üne, biz hiçbirine; yanlış yeşil 0/60** [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`] — **gösterim**. Bedeli söylenir: ölçülmeyenlerin %76'sı renksiz (önce ölç ya da başvuruda karar); "büyük olasılıkla dolu" 22 uyarının 15'i gerçekten dolu [Hesap: aynı]. [kilit_yanlis_yesil.png](kilit_yanlis_yesil.png). Canlı harita (Faz 4, Civan; farazi şehirde "SAHTE VERİ / gösterim") — **BEKLİYOR**. Eski rakamlar (0/87, 41/73, 41/284, %25 / %62 / %27, 0/21, %42, %63) kullanılmaz | 1 |
| 8 | Pilot ve maliyet | Kıbrıs'taki doğruluğu pilot söyler; ilk ölçülecek şey trafonun çıkış gerilimi | 120–170 trafo ölç (Kuzey'deki ~6.400–6.700 trafonun (vekil) ~%2–3'ü) [Hesap: araştırma günlüğü §7; 120 ÷ 6.700 = %1,8, 170 ÷ 6.400 = %2,7; ~6.400–6.700 trafo Güney'in ve Korsika'nın abone / trafo oranından vekil, Kıb-Tek sayısı BULAMADIM; docs/log/2026-11-01-volkan-maliyet-sunum.md]; taşınabilir cihazla ~2,2–3,2 milyon TL (~40–57 bin €, işçilik dahil), ilkbaharda; her trafoya cihaz takmanın ~%1'i [Hesap: docs/log/2026-11-01-can-maliyet.md; aşağıda "Maliyet"]; kör test 10 trafo, başarı: gerçek kırmızıların ≥ %90'ı yakalanır, öğlen yük hatası ±%20 [Yorum: validation.md] | 0,75 |
| 9 | İtirazlar ve jüri cevapları | Ret değil triyaj; son karar insanın | Aşağıda "İtiraz slaydı"; jüri cevapları [konusma-notu.md](konusma-notu.md) | 0,5 |
| 10 | Kaynaklar | Her rakamın nereden geldiği | Aşağıda "Kaynak slaydı" | (gösterilmez, soru gelirse) |

## İtiraz slaydı (9)

[ADR-0005](../decisions/adr-0005-triyaj-ret-degil.md), [ADR-0010](../decisions/adr-0010-yesil-karari-marj-guven-kumulatif.md).

| İtiraz | Cevap |
|---|---|
| **Adalet:** az ölçülen bölgeye haksızlık | Ölçülmemiş trafoda "ölçülmedi" etiketi; ölçülü trafolar tabakalı seçilir (tip × bölge × kVA), benzer yerlere değil boşluklara |
| **Yanlış "evet" maliyeti** (aşırı gerilim, cihaz, güvenlik) | Yeşil = ilk iki başvuru, bilinmeyenlerin 40 çekilişinin %98'inde (en düşük yük, paneller hattın ucunda dahil) sınırı geçmiyor; "güven yüksek" şartı ADR-0019'la kalktı (güvenlik bantta); deneme şehrinde yanlış yeşil 0/60 [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`]; canlıya geçiş bütçesi yanlış yeşil < %2 [Yorum: ADR-0010] |
| **Yanlış "hayır" maliyeti** (vatandaşın hakkı) | Kırmızı ret değil işaret; sarı ve düşük güvene ölçüm cihazı ya da sınırlı onay; itiraz eden gerçek ölçüm isteyebilir |
| **Hesap verebilirlik:** "yapay zekâ hayır dedi" | Model önerir, Kıb-Tek mühendisi karar verir; her tahminin bandı (P10–P90) ve güveni görünür |
| **Komşu etkisi:** bir onay komşunun payını yer | Onaylar bağımsız sayılmaz; kalan pay her onaydan sonra yeniden hesaplanır (sunum sonrası, sözleşme 1.3) |
| **Zamanla bozulma:** paneller arttıkça şablon eskir | Ölçüm cihazları her ilkbahar sarılara dolaşır; şablon her yıl yenilenir [Yorum] |

## Maliyet (slayt 8; pitch şablonunun maliyet kutusu, dashboard)

Kaba hesap; kesinlik iddiası yok. Ayrıntı ve dahil olmayanlar: [maliyet günlüğü](../log/2026-11-01-can-maliyet.md).

| Ne | Kaç trafo | Maliyet | Etiket |
|---|---|---|---|
| Bir trafoyu taşınabilir cihazla ölçmek | 1 | ~18,6 bin TL (~333 €) | [Hesap: Civan'ın ölçüm maliyeti günlüğü — KTEMO birim fiyatı, EMO mühendis saati, Fluke 1736, TCMB kuru] |
| Kıbrıs pilotu | 120–170 | ~2,2–3,2 milyon TL (~40–57 bin €) | [Hesap: maliyet günlüğü] |
| Kıyas: her trafoya kalıcı cihaz | ~6.400–6.700 | ~300–419 milyon TL (~5,4–7,5 milyon €) | [Hesap: Civan'ın günlüğü, B tablosu] |
| Başlangıçta 3 cihaz almak | — | ~1,03 milyon TL (~18,5 bin €) | [Hesap: Fluke 6.164 € × 55,82] |

Söylenebilecek iki cümle:
- "Pilot, her trafoya cihaz takmanın yüzde biri." [Hesap: 3,16 ÷ 300 milyon TL]
- "Bir trafoyu ölçmek, o trafodaki bir evin güneş panelinin yüzde altısı." [Hesap: 333 € ↔ 6,5 kW × 800 €/kW = 5.200 €; 800 €/kW Kaynaklı: KTEMO PİD Ekim 2024, J1; 6,5 kW Yorum]

Bağlam (pitch kutusu; ayrıntı [tarife / emisyon günlüğü](../log/2026-11-01-can-tarife-emisyon.md)):
- Kıb-Tek konut tarifesi: ilk 250 kWh 5,86 TL/kWh, üst kademeler 12,09–16,84 TL/kWh (1 Haziran 2026) [Kaynaklı: Cyprus Mail 26.05.2026; Kıb-Tek belgesi değil, ikincil].
- Kuzey'in elektriği fuel oilden; termik santrallerde ~0,58–0,89 kg CO₂/kWh [Kaynaklı: Erciyas 2014, DAÜ tezi; eski, resmi katsayı BULAMADIM].

Yok: geliştirme / bakım maliyeti (ekibin kararı; para yazılmaz, KARAR 09:46), geri ödeme (mahsuplaşma bedeli BULAMADIM), Kıb-Tek trafo değişim maliyeti (BULAMADIM; Türkiye TEDAŞ 2022 vekili günlükte, sunumda kullanılmaz) — nitel cümleyle kalır (KARAR 10:16 m. 3).

## Kaynak slaydı (10)

- **Kıbrıs evlerinin sıcaklık duyarlılığı (yük modeli yaz eğimi):** 20 konut prosumer, Güney Kıbrıs, 2016, Zenodo 23043383, CC BY 4.0 (`data/raw/kibris-20-prosumer/KAYNAK.txt`; [eşzamanlılık günlüğü](../log/2026-11-01-can-eszamanlilik.md)).

- **İngiltere yöntemi:** Ofgem, WPD "LV Network Templates" ilerleme raporu (Mayıs 2013) ve ödül başvurusu (Mayıs 2015) — https://www.ofgem.gov.uk/sites/default/files/docs/2013/09/ppr_wpd_lv_templates_may2013.pdf · https://www.ofgem.gov.uk/sites/default/files/docs/2015/05/final_-_sdrc_reward_submission_v1.7_redacted.pdf
- **İngiltere gerilim verisi:** UK Power Networks, "Validation of PV Connection Assessment Tool" kapanış raporu v1.1, Ofgem, Mart 2015 — https://www.ofgem.gov.uk/ofgem-publications/93938/pvtoolcdrfinal-pdf ; veri London Datastore, CC BY 4.0. Dış çapalar: bara gerilimi tasarım varsayımı 248 V; gündüz en düşük talep müşteri başına 200–400 W; faz dengesizliği kentsel %25 / kırsal %50 ([Faz 1 günlüğü](../log/2026-10-31-volkan-faz1.md)).
- **İspanya gerçek veri:** Arboleya vd., "Non-Synthetic European Low Voltage Test System", Mendeley Data 2019, DOI 10.17632/685vgp64sm.1, CC BY 4.0.
- **Kıbrıs tüketim eğrileri:** EAC (Güney Kıbrıs dağıtım) profil sınıfları 2022, web.archive kopyası; lisans belirtilmemiş, kaynak gösterilir.
- **Kıb-Tek büyüklükleri:** Kıb-Tek 2023 istatistik (tarife sınıfı abone ve tüketim; Nisan en az tüketilen ay, 101.671 MWh).
- **Güneş:** Open-Meteo Historical Weather API (ERA5), Lefkoşa 2023–2025, CC BY 4.0.
- **Güney kısıntı:** pv magazine, 13.01.2026 ve 15.06.2026 (CyprusGrid verisi).
- **Kuzey bekleyen başvuru:** KTTO raporu, Mart 2023 — adres doğrulanmadı (Can ve Volkan aramalarında bulunamadı).
- **Malta kapasite haritası:** Enemalta, "Available Capacity" haritasının verisi, 31 Ekim 2026'da indirildi (1.332 trafo merkezi; adres [ada ülkeleri günlüğü](../log/2026-10-31-volkan-ada-ulkeleri.md), `data/raw/enemalta-kapasite/KAYNAK.txt`); lisans belirsiz, ham veri depoda yok. "%25 tavanı" Enemalta'nın yazdığı kural değil, bizim veriden çıkarımımız (karar masası 20:47).
- **Hawaii düz kuralı:** Hawaiian Electric (HECO), "Minimum Day Time Load Calculation and Screening", 2014 — https://www.energy.gov/sites/prod/files/Hawaiian%20Electric%202014-04-30_minimum-day-time-load-calculation-and-screening.pdf
- **Maliyet:** KTEMO (KTMMOB Elektrik Mühendisleri Odası) PİD Elektrik Tesisatları Asgari Birim Fiyat Listesi, Ekim 2024 — https://www.ktemo.org/files/teknikbilgiler/EKIM2024.pdf; KTEMO kontrollük ücretleri Rev.13; Fluke 1736/EUS bayi fiyatı (datatec.eu, 1 Kasım 2026); TCMB kuru 30.10.2026 ([Civan'ın günlüğü](../log/2026-11-01-civan-olcum-maliyeti.md)).
- Bütün liste ve adresler: [veri sözlüğü](../data/data-dictionary.md), [araştırma günlüğü](../log/2026-10-31-kapsamli-arastirma.md) "Kaynaklar" bölümü.
