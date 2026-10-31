# Slayt listesi (iskelet)

Hikâye: **güven merdiveni** (karar masası 17:00). Tek cümle: *"Kıbrıs'ı ölçemiyoruz; yöntemi ölçebildiğimiz her şeyde kanıtlıyoruz, sonra uyguluyoruz."* Dört basamak, her birinde tek iddia + tek rakam, hepsi "saf tahmine göre ne kadar iyi" cinsinden. Manşet rakam: **İspanya %25 → %10.**

Süre hedefi 5–7 dk; dakika sütunu kaba [Yorum].

| # | Slayt | Tek iddia | Rakam ve etiket | dk |
|---|---|---|---|---|
| 1 | Sorun | Kuzey'de çatı güneşi başvuruları bekliyor; Kıb-Tek mahalle trafolarını göremiyor | ~2.670 bekleyen başvuru, çoğu 5–8 kW; alçak/orta gerilimde izleme sistemi yok [Kaynaklı: KTTO raporu, Mart 2023; adres doğrulanmadı] (karar masası 17:38; bulunursa değişir) | 0,5 |
| 2 | Neden şimdi | Güney bağladı, şimdi üretimi kısıyor | 2025'te dağıtıma bağlı güneşin %47,44'ü kısıldı, Ocak–Mayıs 2026 %65 [Kaynaklı: pv-magazine.com 13.01.2026 ve 15.06.2026] | 0,5 |
| 3 | Fikir | Az trafoyu ölç, gerisini şablonla tahmin et (İngiltere'nin yöntemi) | İngiltere 824 trafoyu (%2,6) ölçüp gerisini ~%80 doğrulukla tahmin etti; başka şirketlerin 284 trafosunda %80–90 [Kaynaklı: Ofgem WPD LV Templates raporları 2013, 2015] | 0,75 |
| 4 | Bizim uyarlamamız: fotoğraf değil film | Kurulumcu gerilimi tek noktada, tek gün ölçüyor; biz trafonun gün ve mevsim boyu davranışını tahmin edip "kaç ev daha eklenince sınıra gelir"i önceden söylüyoruz | Hedef: ilkbahar öğlen en düşük yük (11–14) ve hat ucu gerilimi; planlama sınırı 259 V, inverter 264 V'ta kapanır [Kaynaklı: CLAUDE.md / ADR-0002] | 0,75 |
| 5 | Güven merdiveni — basamak 1: farazi şehir (kontrollü gerçek) | Cevabı bildiğimiz şehirde yöntem çalışıyor | Öğlen yük hatası ortanca / P90: faturalı %3,8 / %8,0, faturasız %20,6 / %50,7; yanında İspanya %10 / %25 [Hesap: sınav şehirleri 11–20, üretici 1.2, `sinav.py faz2`, docs/log/2026-10-31-can-faz2.md] — **üst sınır (gösterim)**, manşet İspanya (karar masası 17:38). Eski %8,6 (PR #8) artık kullanılmaz | 0,5 |
| 6 | Basamak 2: İspanya (yük, gerçek veri) — **MANŞET** | Hiç görmediğimiz 29 gerçek trafoda, Kıb-Tek'in zaten elinde olan abone sayısı + faturayla | Yalnız müşteri sayısıyla ~%25, faturayla ~%10 ortanca hata [Hesap: PR #10, docs/log/2026-10-31-volkan-edp-gercek.md; veri Arboleya vd. 2019, CC BY] | 0,75 |
| 7 | Basamak 3: İngiltere (gerilim, gerçek veri) | Gerilim hesabımız gerçek hatlarda tutuyor; tutmadığı yer yüzünden yeşil önce pilotla sınanır | 6 gerçek hattın 5'inde ölçülen yükselme hesabın güvenli sınırının altında; birinde (Bancroft, panelli kol) küçük gördük [Hesap: PR #11 + docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md; veri UKPN 2015, CC BY] (karar masası 18:46) | 0,5 |
| 8 | Basamak 4: Kıbrıs pilotu (saha) | Kıbrıs'taki doğruluğu pilot söyler; ilk ölçülecek şey trafonun çıkış gerilimi | Çıkış gerilimi bilinince "dolu" dediğimiz trafolardaki yanılma %27 → %19 [Hesap: bilginin değeri denemesi, farazi 11–20, kusursuz bilgi üst sınırı; docs/log/2026-10-31-volkan-faz3.md] (karar masası 20:47; ekran 6). 120–170 trafo ölç (adadaki ~6.400 trafonun ~%2'si) [Hesap: araştırma günlüğü §7; ~6.400 trafo Güney'den vekil, Kıb-Tek sayısı BULAMADIM]; 10 taşınabilir cihazla ~20 bin € + pens, ilkbaharda [Hesap: araştırma günlüğü §5; Hioki PW3360-21 1.978 € KDV hariç, shop.hioki.eu]; kör test 10 trafo, başarı: gerçek kırmızıların ≥ %90'ı yakalanır, öğlen yük hatası ±%20 [Yorum: validation.md] | 0,5 |
| 9 | Canlı harita | Her trafo yeşil / sarı / kırmızı, "ölçülmedi" etiketiyle | Faz 4 paneli (Civan); farazi şehirde "SAHTE VERİ / gösterim" yazısı — **BEKLİYOR** | 1 |
| 10 | %40 kuralıyla yan yana | Bugünkü kural ("trafo gücünün %40'ı") ile modelin yanlış yeşili aynı trafolarda yan yana | **KİLİT GRAFİK** [kilit_yanlis_yesil.png](kilit_yanlis_yesil.png): dolu trafoya "yer var" — bizim yeşil 0/87, %40 kuralı 41/284 (%14); dolu 73 trafonun 41'ine %40 kuralı "yer var" diyor, biz hiçbirine [Hesap: sınav şehirleri 11–20, olasılıklı hesap (ADR-0011), karar masası koşumu 31 Ekim (karar masası 19:51), `sinav.py faz3`, docs/log/2026-10-31-volkan-faz3.md] — **gösterim**. Bedeli söylenir: yeşil %25, trafoların %62'si sarı, yani "önce ölç"; kırmızıların %27'sinde gerçekte yer var (12/44; dolu 73 trafonun 32'si kırmızıda, kalanı sarı) [Hesap: aynı koşum]. Eski tek denklem rakamları (0/21, %42, %63) kullanılmaz. Grafik dosyası karar masasının Mac koşumundan, resmi veriden (0/87 ↔ 41/284, dolu 41/73; karar masası 21:44) | 0,5 |
| 11 | İtirazlar ve triyaj | Ret değil triyaj; son karar insanın | Aşağıda "İtiraz slaydı" | 0,5 |
| 12 | Kaynaklar | Her rakamın nereden geldiği | Aşağıda "Kaynak slaydı" | (gösterilmez, soru gelirse) |

## İtiraz slaydı (11)

[ADR-0005](../decisions/adr-0005-triyaj-ret-degil.md), [ADR-0010](../decisions/adr-0010-yesil-karari-marj-guven-kumulatif.md).

| İtiraz | Cevap |
|---|---|
| **Adalet:** az ölçülen bölgeye haksızlık | Ölçülmemiş trafoda "ölçülmedi" etiketi; ölçülü trafolar tabakalı seçilir (tip × bölge × kVA), benzer yerlere değil boşluklara |
| **Yanlış "evet" maliyeti** (aşırı gerilim, cihaz, güvenlik) | Yeşil = karamsar senaryo (en düşük yük, paneller hattın ucunda, tek faz, 250 V) sınırı marjla geçiyor **ve** güven yüksek; canlıya geçiş bütçesi yanlış yeşil < %2 [Yorum: ADR-0010] |
| **Yanlış "hayır" maliyeti** (vatandaşın hakkı) | Kırmızı ret değil işaret; sarı ve düşük güvene ölçüm cihazı ya da sınırlı onay; itiraz eden gerçek ölçüm isteyebilir |
| **Hesap verebilirlik:** "yapay zekâ hayır dedi" | Model önerir, Kıb-Tek mühendisi karar verir; her tahminin bandı (P10–P90) ve güveni görünür |
| **Komşu etkisi:** bir onay komşunun payını yer | Onaylar bağımsız sayılmaz; kalan pay her onaydan sonra yeniden hesaplanır (sunum sonrası, sözleşme 1.3) |
| **Zamanla bozulma:** paneller arttıkça şablon eskir | Ölçüm cihazları her ilkbahar sarılara dolaşır; şablon her yıl yenilenir [Yorum] |

## Kaynak slaydı (12)

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
- Bütün liste ve adresler: [veri sözlüğü](../data/data-dictionary.md), [araştırma günlüğü](../log/2026-10-31-kapsamli-arastirma.md) "Kaynaklar" bölümü.
