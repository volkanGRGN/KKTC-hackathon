# Hold-out defteri — gerçek veriye her bakış

[ADR-0013](../decisions/adr-0013-veri-dongusu-tuzugu.md) madde 1: gerçek doğrulama verisine her bakış "istatistik gücü harcar"; burada bir satır olur. **Append-only:** satır silinmez, düzeltilmez; düzeltme yeni satırdır. Sahibi Can (Faz 7 kartı C3); herkes yazar, sona ekler.

Ne zaman satır: gerçek veriden (İspanya, İngiltere, ileride pilot) model sonucu ya da sınav ölçüsü hesaplandığında; yeniden koşum da bakıştır. Ham veri okuma / temizlik sayısı bakış değildir. Farazi şehir buraya yazılmaz.

Sütunlar: tarih saat · veri · amaç · kim · ne ölçüldü (metrik) · sonuç değişti mi (model / eşik bu bakıştan sonra değişti mi) · iz (commit, PR, günlük).

| # | Tarih | Veri | Amaç | Kim | Metrik | Sonrasında değişen | İz |
|---|---|---|---|---|---|---|---|
| 1 | 31 Eki 14:34 | İspanya EDP Oviedo, 29 trafo, 1–20 Mayıs 2018 | Faz 2 (2i): şablon yöntemi gerçek veride | Volkan (BUILD) | öğlen en düşük yük hatası ortanca / P90, %80 bant kapsaması, güven etiketi; girdi a / b / c / kıyas × 5 / 10 / 15 ölçülü × rastgele / tabakalı × 20 tekrar | ADR-0007 (fatura girdi), manşet %25 → %10 | PR #10 (1e5183e), `src/edp_test.py`, [günlük](2026-10-31-volkan-edp-gercek.md) |
| 2 | 31 Eki 15:24 | İspanya EDP Oviedo, aynı 29 trafo | ADR-0008: farazi şehir fazla kolay mı (çeşitlilik) | Can | müşteri başına öğlen yükü CV, eğri benzerliği, saf tahmin hatası (model yok) | üreticide mahalle çarpanı (BUILD), `faz2` saf tahmin maddesi | 8435348, `src/edp_kiyas.py`, [Faz 2 günlüğü](2026-10-31-can-faz2.md) |
| 3 | 31 Eki 16:24 | İngiltere UKPN PV doğrulama, yaz 2014, 6 hat ucu ev | Faz 3: gerilim fiziği (`solve()`) gerçek hatta | Volkan (BUILD) | model ÷ ölçülen gerilim yükselmesi (hedef 0,7–1,5) | karamsar senaryo panelleri hat ucuna koyar (karar masası 16:27) | PR #11 (f011ce0), `src/ukpn_test.py`, [günlük](2026-10-31-volkan-ukpn-gerilim.md) |
| 4 | 31 Eki 18:09 | İngiltere UKPN, aynı 6 hat | Faz 3: olasılıklı hesabın P98'i ölçülen yükselmeyi kapsıyor mu | Volkan (BUILD) | 6 hattın kaçında ölçülen ≤ P98 (5/6; Bancroft kaçtı) | `kac_ev_olasilik.py`'ye hat boyu belirsizliği ve yüksüz panelli kol (392e224); sunum cümlesi "5/6" | fa49ef8, [günlük](2026-10-31-volkan-faz3-ukpn-geritest.md) |
| 5 | 31 Eki (21:41 sonrası) | İspanya EDP Oviedo, aynı 29 trafo | Faz 7 C1 "önce": kalibrasyon ölçüsü main'deki modelde | Can | `edp_test.py` yeniden koşum (PR #10 tablosu birebir); nominal %50 / 80 / 90 / 95 ↔ ampirik kapsama, PIT 10 kova; resmi koşul girdi c, 10 ölçülü, tabakalı | — (ölçü; model değişmedi) | `src/sinav.py faz2 --ispanya`, [Faz 7 günlüğü](2026-10-31-can-faz7.md) |

Not: 1–4 commit kaydından ve günlüklerden geriye doğru yazıldı (defter 31 Ekim akşamı açıldı); bu dört bakış dışında ara yeniden koşumlar olmuş olabilir (ör. karar masasının rakam teyitleri), kaydı yok. İspanya ve İngiltere'de ayar / doğrulama ayrımı yapılmadı: 29 trafo ve 6 hat bütünüyle dört kez görüldü. ADR-0013'e göre bundan sonraki "iyileşti" iddiası bu verilerde değil, dokunulmamış veride (pilot doğrulama payı) kanıtlanır.
