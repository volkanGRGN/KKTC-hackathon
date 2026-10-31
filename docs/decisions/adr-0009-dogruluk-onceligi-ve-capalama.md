# ADR-0009: Doğruluk için öncelik girdi > dış değişken > ölçüm; farazi şehir ilişki ve kuyrukla çapalanır

Tarih: 2026-10-31 · Durum: kabul · ADR-0003, ADR-0007, ADR-0008'i tamamlar

## Bağlam
Ölçülü trafo sayısını 5'ten 15'e çıkarmak hatayı düşürmedi; trafodaki abonelerin fatura toplamı girince hata 2,5 kat düştü (İspanya, gerçek veri, PR #10 günlüğü). Farazi şehirler trafolar arası yayılımda gerçeğin altındaydı (ADR-0008). Muhittin (ikinci cevap, docs/log/2026-10-31-muhittin-cevap-2-hata-payi-mimari.md): sorun etiket kıtlığı değil ayırt edici bilgi kıtlığı; çapalamada tek tek dağılımlar yetmez, ilişkiler ve kuyruk gerekir; İspanya eğitim hedefi olursa sınav olmaktan çıkar.

## Karar
1. **Öncelik sırası:** (a) Kıb-Tek'te ağ genelinde var olan girdi: fatura toplamı ve dağılımı (yüksek tüketen abone oranı, tarife karışımı, mevsimsellik); (b) her trafoda ucuza bulunan dış değişken (tarife bölgesi, kentsel/kırsal, bina yaşı vekilleri); (c) daha çok ölçülü trafo, ama doğruluk için değil doğrulama ve kalibrasyon için ("özellik değil sınav kâğıdı"). **Her trafoda olmayan değişken modele girmez.**
2. **Çapalama ölçüleri** (farazi şehir ↔ gerçek veri, Can'ın karşılaştırma betiği): mevcut dört moment (müşteri başına öğlen yükü CV, eğri benzerliği, bara gerilimi yayılımı, faz dengesizliği) + **korelasyon matrisi** (büyüklük ↔ şekil, yük ↔ PV konumu, PV yoğunluğu ↔ hat boyu), **kuyruk** (müşteri başına yük ve metre başına empedans P90/P95), **hat üzerinde PV konum dağılımı ve fazı** (uca kümelenme olasılığı üretici girdisi), **trafo içi çeşitlilik** (eşzamanlılık). Çapalar boyutsuz (CV, oran, işaret, Ω/km); mutlak büyüklük Kıb-Tek'ten.
3. **İspanya donuk sınav:** üretici ve model parametreleri İspanya hatasını düşürmek için ayarlanmaz; çapalar aralık olarak (ör. CV 0,3–0,6) ve bandın her yerinde test edilir. "Farazi − İspanya" hata farkı aşırı uydurma ölçeri olarak her sürümde günlüğe yazılır.

## Sonuç
- Artı: Faz 2 iyileştirmesinin yönü belli (fatura dağılımı, ADR-0007'nin genişlemesi); ölçüm planı pilotta doğrulamaya ayrılır; farazi şehir kuyrukta da gerçeğe benzer.
- Eksi: korelasyon ve kuyruk eşlemesi 29 İspanya trafosuyla gürültülü; sunum öncesi yalnız korelasyon matrisi ve P90 raporlanır, üretici 1.3'te uygulanır. Fatura dağılımı için Kıb-Tek verisi yok, farazi şehirde üretilir [Yorum].
