# ADR-0010: Yeşil kararı karamsar senaryo + yüksek güven + marj ister; onaylar kümülatif düşülür; yanlış yeşil bütçesi geri-testle tutulur

Tarih: 2026-10-31 · Durum: kabul · ADR-0005 (triyaj) ve ADR-0002 (gerilim) üstüne

## Bağlam
İngiltere gerçek verisinde eşit yayılmış model, paneller hattın ucunda toplanınca yükselmeyi yarıdan az gösterdi (PR #11). Yanlış yeşilin zararı (aşırı gerilim, cihaz, güvenlik) yanlış kırmızıdan (kaçan fırsat) ağır. Muhittin: karamsar senaryo gerekli ama yetmez; kural asimetrik olmalı, ölçüm cihazı sarılara, onaylar bağımsız sayılmaz, yeşil kuralı gerçek veride geri-test edilip bütçelenir.

## Karar
1. **Yeşil** = karamsar senaryo (P10 yük, bekleyen paneller hattın ucunda, tek faz, trafo çıkışı 250 V) sınırı **marjla** geçiyor (marj: gerilim payının %10'u ya da en az 1 ev [Yorum]) **ve** güven yüksek. **Sarı** = karamsar sınırda ya da güven orta/düşük → sınırlı miktar onayı ya da önce geçici ölçüm. **Kırmızı** = karamsar sınırı aşıyor. Ölçümsüz yeşil verilir; ölçüm cihazı sarılara gider (triyaj değeri burada).
2. **Kümülatif:** kaç ev, o anki kalan paya göre; onaylanan başvuru paydan düşülür ve trafo yeniden değerlendirilir; aynı mahallede onaylar bağımsız sayılmaz (`kac_ev.csv`'ye `onaylanan_kw` ve `kalan_ev` sütunları sözleşme 1.3'te).
3. **Geri-test ve bütçe:** "yalnız ön bilgiyle yeşil deseydik gerçekte kaç trafo aşardı" ölçüsü farazi şehirlerde (Faz 3 sınavı) ve gerçek veride (İspanya yük tarafı; İngiltere 6 hat gerilim tarafı) hesaplanır. Canlıya geçiş bütçesi yanlış yeşil **< %2** [Yorum, Muhittin %1–2]; eşikler (marj, güven) bu bütçeyi tutacak şekilde ayarlanır. ROADMAP Faz 3'ün farazi şehir eşiği (≤ %5) gösterim eşiği olarak kalır.

## Sonuç
- Artı: "yapay zekâ yer var dedi, trafo yandı" riski üç kademeyle kapanır; jüriye "yeşili ölçümsüz veriyoruz ama yalnız rahat marjlı, yüksek güvenli trafoda" denir. Ölçüm planı anlamlı: sarılar.
- Eksi: sarı oranı artar (ROADMAP hedef ≤ %30, aşarsa sebep günlükte). Kümülatif düşüm ve geri-test sunum sonrasına (üretici 1.3 / Faz 3 ikinci sürüm); bugün yalnız marj + güven kuralı ve farazi şehirde yanlış yeşil ölçüsü.
