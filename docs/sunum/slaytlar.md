# Slayt listesi (iskelet)

Hikâye: **güven merdiveni** (karar masası 17:00). Tek cümle: *"Kıbrıs'ı ölçemiyoruz; yöntemi ölçebildiğimiz her şeyde kanıtlıyoruz, sonra uyguluyoruz."* Dört basamak, her birinde tek iddia + tek rakam, hepsi "saf tahmine göre ne kadar iyi" cinsinden. Manşet rakam: **İspanya %25 → %10.**

Süre hedefi 5–7 dk; dakika sütunu kaba [Yorum].

| # | Slayt | Tek iddia | Rakam ve etiket | dk |
|---|---|---|---|---|
| 1 | Sorun | Kuzey'de çatı güneşi başvuruları bekliyor; Kıb-Tek mahalle trafolarını göremiyor | ~2.670 bekleyen başvuru, çoğu 5–8 kW; alçak/orta gerilimde izleme sistemi yok [Kaynaklı: KTTO raporu, Mart 2023 — **adres BULAMADIM**, araştırma günlüğünde yalnız ad; slayttan önce bulunmalı] | 0,5 |
| 2 | Neden şimdi | Güney bağladı, şimdi üretimi kısıyor | 2025'te dağıtıma bağlı güneşin %47,44'ü kısıldı, Ocak–Mayıs 2026 %65 [Kaynaklı: pv-magazine.com 13.01.2026 ve 15.06.2026] | 0,5 |
| 3 | Fikir | Az trafoyu ölç, gerisini şablonla tahmin et (İngiltere'nin yöntemi) | İngiltere 824 trafoyu (%2,6) ölçüp gerisini ~%80 doğrulukla tahmin etti; başka şirketlerin 284 trafosunda %80–90 [Kaynaklı: Ofgem WPD LV Templates raporları 2013, 2015] | 0,75 |
| 4 | Bizim uyarlamamız: fotoğraf değil film | Kurulumcu gerilimi tek noktada, tek gün ölçüyor; biz trafonun gün ve mevsim boyu davranışını tahmin edip "kaç ev daha eklenince sınıra gelir"i önceden söylüyoruz | Hedef: ilkbahar öğlen en düşük yük (11–14) ve hat ucu gerilimi; planlama sınırı 259 V, inverter 264 V'ta kapanır [Kaynaklı: CLAUDE.md / ADR-0002] | 0,75 |
| 5 | Güven merdiveni — basamak 1: farazi şehir (kontrollü gerçek) | Cevabı bildiğimiz şehirde yöntem çalışıyor | Öğlen yük hatası ortanca %8,6 [Hesap: ADR-0007, PR #8 geliştirme şehirleri] — **gösterim**, destek rakamı, manşet değil. **Not:** üretici 1.2 ile faturalı %3,9, faturasız %22 [Hesap: docs/log/2026-10-31-volkan-uretici-1-2.md]; Can'ın `sinav.py faz2` sonucu gelince hangisinin konacağına karar masası karar verir | 0,5 |
| 6 | Basamak 2: İspanya (yük, gerçek veri) — **MANŞET** | Hiç görmediğimiz 29 gerçek trafoda, Kıb-Tek'in zaten elinde olan abone sayısı + faturayla | Yalnız müşteri sayısıyla ~%25, faturayla ~%10 ortanca hata [Hesap: PR #10, docs/log/2026-10-31-volkan-edp-gercek.md; veri Arboleya vd. 2019, CC BY] | 0,75 |
| 7 | Basamak 3: İngiltere (gerilim, gerçek veri) | Gerilim fiziğimiz gerçek hatlarda tutuyor; tutmadığı yerden karamsar senaryoyu çıkardık | 6 hat ucunun 4'ünde ölçülen yükselmenin ±%40'ı içinde; 2 ıskalama panellerin hat ucunda toplanmasından → karamsar senaryo panelleri uca koyar [Hesap: PR #11; veri UKPN 2015, CC BY] | 0,5 |
| 8 | Basamak 4: Kıbrıs pilotu (saha) | Kıbrıs'taki doğruluğu pilot söyler | 120–170 trafo ölç (adadaki ~6.400 trafonun ~%2'si) [Hesap: araştırma günlüğü §7; ~6.400 trafo Güney'den vekil, Kıb-Tek sayısı BULAMADIM]; 10 taşınabilir cihazla ~20 bin € + pens, ilkbaharda [Hesap: araştırma günlüğü §5; Hioki PW3360-21 1.978 € KDV hariç, shop.hioki.eu]; kör test 10 trafo, başarı: gerçek kırmızıların ≥ %90'ı yakalanır, öğlen yük hatası ±%20 [Yorum: validation.md] | 0,5 |
| 9 | Canlı harita | Her trafo yeşil / sarı / kırmızı, "ölçülmedi" etiketiyle | Faz 4 paneli (Civan); farazi şehirde "SAHTE VERİ / gösterim" yazısı — **BEKLİYOR** | 1 |
| 10 | %40 kuralıyla yan yana | Bugünkü kural ("trafo gücünün %40'ı") ile modelin yanlış yeşili aynı trafolarda yan yana | Yanlış yeşil oranı: model vs %40 kuralı — **BEKLİYOR** (Faz 3, `sinav.py faz3`) | 0,5 |
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
- **Kuzey bekleyen başvuru:** KTTO raporu, Mart 2023 — adres BULAMADIM.
- Bütün liste ve adresler: [veri sözlüğü](../data/data-dictionary.md), [araştırma günlüğü](../log/2026-10-31-kapsamli-arastirma.md) "Kaynaklar" bölümü.
