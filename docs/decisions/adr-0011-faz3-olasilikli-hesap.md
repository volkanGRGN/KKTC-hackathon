# ADR-0011: Faz 3 "kaç ev" hesabı olasılıklı (çekilişli ev ev benzetim); renk olasılık eşiğiyle; tek denklem yedek

Tarih: 2026-10-31 · Durum: kabul · ADR-0010 (yeşil kuralı) ve ADR-0009 (çapalama) üstüne · karar masası 18:46

## Bağlam
Tek denklemli `kac_ev.py` bilinmeyen her şey (bara gerilimi, öğlen orta gerilim değişimi, panelin yeri ve fazı, hat boyu) için tek bir "en kötü" değer seçiyor. [Varsayım envanteri](../log/2026-10-31-volkan-faz3-varsayimlar.md) gösterdi: bu değerleri oynatmak kırmızıyı yalnız kaydırıyor, trafoları doğru sıraya dizme gücünü (0,75) değiştirmiyor. Sınav şehirleri 11–20'de yanlış kırmızı %42, kaç ev hatası 3,5 ev (eşik ≤ 2), konut trafosuna hiç yeşil yok. Çözüm ayar değil yapı: bilinmeyenleri gerçek veriye dayalı aralıktan çekip her çekilişte ev ev benzetim koşmak ([olasılıklı deneme](../log/2026-10-31-volkan-faz3-olasilik.md), PR #15; Volkan'ın fikri).

## Karar
1. **Faz 3'ün resmi hesabı `src/kac_ev_olasilik.py`:** trafo başına 40 çekiliş; aralıklar varsayım envanterinden ve gerçek veriden (İngiltere UKPN), şehir üreticisinin kendi değerlerinden değil (ADR-0009). Hat boyu ×0,6–1,6 belirsizliği ve "panelli evler yüksüz kolda" (1/6) dahil (İngiltere geri-testinden).
2. **Renk, ADR-0010'un olasılıklı okuması:** kırmızı = bugün (yeni panelsiz) sınırı aşma olasılığı ≥ 0,5; yeşil = ilk iki başvurunun sığma olasılığı ≥ 0,98 (canlı bütçe %2) **ve** güven yüksek; diğerleri sarı. İki eşik ilkeden; sınav şehrine göre ayarlanmaz (bedel tablosu günlükte).
3. **Sayılar:** `kac_ev_karamsar` = çekilişlerin P10'u, `kac_ev_iyimser` = P90'ı, yeni `kac_ev_orta` = ortanca. **Sözleşme 1.3, küçük:** §6'ya `p_bugun_asar`, `p_iki_ev_sigar`, `kac_ev_orta` eklenir; var olan sütunların adı ve yeri değişmez (karamsar/iyimser açıklaması "çekiliş P10/P90" olur); `isil_pay_kw`, `gerilim_pay_kw_*`, `sinir_karamsar`, `kural40_ev` tek denklemden gelmeye devam eder. Harita (Civan) ve `sinav.py faz3` (Can) bu yüzden değişmeden çalışır.
4. **Tek denklemli `kac_ev.py` silinmez:** pay sütunlarını üretir, yedek ve kıyas satırıdır (günlükte yan yana).
5. **Dürüstlük:** farazi sonuç gösterim. Gerilim tarafı İngiltere'nin 6 gerçek hattında [geri-test](../log/2026-10-31-volkan-faz3-ukpn-geritest.md) edildi: 5'inde ölçülen yükselme hesabın %98 sınırının altında, Bancroft'ta değil (ev yüksüz ama panelli bir kolda). Yeşilin %2 bütçesi gerçek veride **doğrulanmış sayılmaz**; canlıda yeşil önce pilotla sınanır (sarı trafoların hat uçlarında öğlen gerilimi). Olasılık düşük uçta (%10–30 kovası) iyimser; sebep üreticideki +%0,8 öğlen OG yükselmesi (UKPN'le çelişir; üretici 1.3'te aralığa alınır) ve panellerin uca kayması.

## Gerekçe
Sınav 11–20 (bir kez ölçüldü; 347 trafo, 74'ü dolu), tek denklem kırmızı (b) → olasılıklı:

| Ölçü | Tek denklem | Olasılıklı |
|---|---|---|
| Yeşil | %6 (21) | %25 (87) |
| Yanlış yeşil | 0/21 | 0/87 |
| Yanlış kırmızı | %42 | %27 |
| Dolu trafonun kırmızı denen payı | 61/74 | 32/74 (kalanı sarı) |
| Kaç ev hatası (tavansız, ortanca) | 3,5 | 2 |
| Sarı | %63 | %62 |

Konut trafosunda yeşil artık var (%4) ve hiçbiri yanlış değil. Bedeli: dolu trafoların yarıdan azı kırmızı; sarı "önce ölç" demek, onay değil (karar masası 17:26), zarar yok. Sarı hedefi (≤ %30) KALDI; onu ancak yeni bilgi düşürür (bara gerilimi, panelli abonenin adresi ve fazı: pilot ve uzmana soru 2–4).

Reddedilenler: (a) tek denklem resmi kalsın, olasılıklı ikinci sürüm → ürünün ana çıktısı (kaç ev) eşiği geçmiyor, konut trafosuna yeşil yok; (b) eşikleri 11–20'ye göre ayarlamak → ADR-0009'a aykırı; (c) sözleşmeyi baştan yazmak → sunum gecesi haritayı ve sınavı kırar.

## Sonuçlar
- BUILD: PR #13 ve #15 birleşir; `kac_ev_olasilik.py` `kac_ev.csv`'yi sözleşme sütunlarıyla (+3) yazar; sözleşme 1.3 notu (Can ya da Civan onayı); ROADMAP Faz 3 kutuları Can'ın yeniden koşumuyla. **Zaman kutusu 45 dk**; sığmazsa gösterim tek denklem csv ile kalır, olasılıklı günlükte "ikinci sürüm".
- Can: `sinav.py faz3` yeni csv ile bir kez; ekran 4 (İngiltere cümlesi) ve ekran 5 rakamları.
- Civan: panel değişmez; zaman kalırsa "bugün aşma olasılığı" ve orta sayı yan panelde.
- Pilot: ilk ölçüm bara gerilimi ve sarı trafoların hat uçları; her ölçülen hat geri-teste eklenir.
