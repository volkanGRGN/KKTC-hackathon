# ADR-0008: Farazi şehirde trafolar arası çeşitlilik gerçek veriye çapalanır; Faz 2 sınavına "saf tahmin" kıyası

Tarih: 2026-10-31 · Durum: kabul · ADR-0003 ve ADR-0007'yi tamamlar

## Bağlam
Üç ayrı ölçüm aynı şeyi söyledi (31 Ekim, öğleden sonra):
- Can [Hesap, günlüğe yazılacak]: İspanya EDP'nin 28 gerçek trafosu ile 20 farazi şehrin 800 trafosu aynı ölçülerle. Hiç model kullanmadan "müşteri başına ortalama × müşteri sayısı" diyen saf tahmin farazi konut trafolarında öğlen hatası ortanca %9,7, P90 %25,9 veriyor; Faz 2 eşiği (≤ %15 / ≤ %30) model hiçbir şey öğrenmese de geçiliyor. Aynı saf tahmin gerçek trafolarda %19 / %45. Müşteri başına öğlen yükünün trafodan trafoya değişim katsayısı farazide 0,14, gerçekte 0,46; eğri benzerliği 0,98'e karşı 0,89.
- Karar masası [Hesap, 20 yeni şehir, %3–25]: şehir konutu trafolarında müşteri başına öğlen yükü CV şehir içi ortanca 0,08, 20 şehir havuzu 0,13; EDP büyüklüğündeki kentsel trafolarda 0,09.
- BUILD [Hesap, PR #10, gerçek veri]: şablon yöntemi yalnız müşteri sayısı + şebeke bilgisiyle İspanya'da saf kıyası geçmiyor (ortanca %25–26, ikisi de); fatura toplamı girince %10–11, P90 %32–33, farazi şehirle aynı.

Sebep üreticide: rastgelelik şehir başına (bütün trafolar aynı çarpanı paylaşıyor) ve ev başına (±%35, 50 evin ortalamasında kayboluyor); **trafo başına, yani mahalle düzeyinde fark yok**. Gerçekte mahalleler gelir, ev büyüklüğü, boş yazlık, klima ile birbirinden ayrılır. Sonuç: farazi şehir isabeti iyimser; Faz 2 sınavı modelsiz de geçilebilir.

Sınırlar: EDP'de abone sınıfı yok, trafolar karışık; 0,46'nın bir kısmı sınıf karışımından gelir ve bizim model onu sınıf sayılarıyla açıklar. 28 trafo az, Kıbrıs değil. Sorun var, büyüklüğü kesin değil.

## Karar
1. **Faz 2 sınavına "saf tahmin" satırı** (Can, `sinav.py faz2`): ölçülü trafolarda Σ öğlen en düşük ÷ Σ abone × bu trafonun abone sayısı (BUILD'in PR #10'daki "kıyas"ıyla aynı tanım). Geçme ölçütü: modelin ortanca ve P90 hatası saf tahminden **en az %25 daha düşük** [Yorum, eşik]; madde rakamıyla günlükte, "gösterim" etiketi. Model saf tahmini geçemiyorsa Faz 2 geçmemiş sayılır.
2. **Üretici sürüm 1.2'de mahalle çarpanı** (BUILD, `sehir_uret.py`): trafo başına log-normal çarpan, σ ≈ 0,3 [Yorum]; hedef konut trafolarında müşteri başına öğlen yükü CV 0,3–0,4 (EDP'nin 0,46'sı karışık olduğu için üst sınır); ek olarak trafo başına saat kayması ±30 dk; `ayar.json`'a `mahalle_sigma`. Değer EDP'ye uydurulmaz, aralığa çapalanır; CV her üretimde `sinav.py faz1` bilgi satırı olarak raporlanır (Can). Aynı yeniden üretimde: fatura sütunu (ADR-0007), bayram listesi, kıyı kontrolü, `kva_tavan_sayisi`, ışınım yılına 2023 eklenmesi.
3. **Sunum cümlesi** (Faz 5 dürüstlük cümlelerine): "Farazi şehir isabeti gerçek isabetin üst sınırıdır. Gerçek veride, İspanya'da 29 trafoda sınadık: yalnız müşteri sayısıyla ~%25, fatura bilgisiyle ~%10 ortanca hata. Kıbrıs'taki doğruluğu pilot söyler."
4. Can'ın karşılaştırma betiği ve rakamları depoya girer (`src/edp_kiyas.py` + `docs/log/2026-10-31-can-faz2.md`); aynı ölçü yeniden üretimden sonra tekrar koşulur ve ADR'nin "hedef CV" maddesi orada sınanır.

## Sonuç
- Artı: Faz 2 sınavı anlam kazanır (model saf tahmini geçmek zorunda). Mahalle farkı eklenince "yalnız abone sayısı" modeli farazide de kötüleşir, faturalı model ayakta kalır; bu, Kıb-Tek'ten fatura istemenin kanıtı olur. Farazi ve gerçek rakamlar yan yana söylenir.
- Eksi: Şehirler bir kez daha üretilir, Faz 2 ve Faz 3 ölçümleri yenilenir. σ ve hedef CV tahmin [Yorum]; İspanya ile Kıbrıs mahalleleri aynı değil. Mahalle çarpanı artınca Faz 1 "259 V üstü / 207 V altı" sayıları da değişir; sınav yeniden koşulur.
