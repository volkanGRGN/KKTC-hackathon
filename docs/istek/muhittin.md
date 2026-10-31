# Muhittin'e sorulacaklar

Nadir ve toplu. Buraya yazılır, Volkan uygun anda volki üzerinden iletir. Bir soru ancak şu iki durumda girer: (1) iki yol denendi, 30 dakikadır ilerleme yok; (2) bir ADR'yi belirleyecek ve bizde uzmanlığı olmayan bir karar. Kalıp:

```
## <saat> — <kimden> — <konu>
Ne denedik:
Karar noktası:
Seçenekler:
Durum: bekliyor | soruldu | cevaplandı (cevap: docs/log/…)
```

## 16:50 — karar masası (Volkan adına) — Gerçekçi farazi şehir, modelin hata payı ve mimari
Ne denedik: Farazi şehirleri gerçeğe çapaladık (eğri şekilleri Güney Kıbrıs 2022 sayaç eğrileri; büyüklük Kıb-Tek 2023 sınıf tüketimi ÷ abone; şebeke geometrisi varsayım aralıkları; şehirler arası rastgeleleştirme; bugün trafo başına "mahalle çarpanı" eklendi, İspanya'daki gerçek trafolar arası yayılıma çapalı: müşteri başına öğlen yükü CV gerçekte 0,46, bizde 0,14 idi). Model şablon yöntemi (kümeleme + atama + ölçek + bir-dışarıda P10–P90 bant + güven etiketi). Kontroller: farazi şehirde öğlen hatası ortanca %8,6 (saf "müşteri başına ortalama" tahmini bile %9,7 → sınava saf tahmin satırı eklendi); İspanya'da 29 gerçek trafoda müşteri sayısıyla %25, fatura toplamıyla %10; İngiltere'de 6 gerçek hatta gerilim fiziği 4'ünde ±%40, 2'sinde paneller hat ucunda toplandığı için model yükselmeyi az gösterdi → karamsar senaryo paneli hat ucuna, tek faza koyuyor.
Karar noktası: (1) Modelin kendi ölçtüğü hata payını (bir-dışarıda bant, kapsama %74–85) küçültmek için öncelik ne olmalı: daha çok ölçülü trafo mu (bizde 5→15 düşürmedi), fatura gibi daha iyi girdi mi (2,5 kat düşürdü), mahalle farkını açıklayan dış değişken mi (gelir, bina yaşı, klima)? (2) Farazi şehri gerçeğe çapalarken hangi istatistikleri eşlemeli (biz: trafolar arası müşteri başına öğlen yükü CV, eğri benzerliği, bara gerilimi yayılımı, faz dengesizliği); eksik var mı, İspanya'ya "fazla uydurma" nasıl önlenir? (3) Mimari: farazi şehir (geliştirme) → İspanya (yük doğrulama) → İngiltere (gerilim doğrulama) → Kıbrıs pilot. Parçalar dağınık mı, tek hikâyeye nasıl bağlanır, öne çıkacak rakam hangisi? (4) Yanlış yeşil için karamsar senaryo (hat ucu + tek faz + P10 yük + 250 V) yeterli mi, yoksa trafo başına ölçüm şart mı?
Seçenekler: cevap ADR-0009'a (hata payı önceliği) ve Faz 5 hikâyesine girer; cevapsız kalırsa mevcut kararlarla (ADR-0007 fatura, ADR-0008 mahalle çarpanı) devam.
Durum: bekliyor
