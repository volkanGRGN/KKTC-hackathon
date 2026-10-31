# Muhittin'e sorulacaklar

Nadir ve toplu. Buraya yazılır, Volkan uygun anda volki üzerinden iletir. Bir soru ancak şu iki durumda girer: (1) iki yol denendi, 30 dakikadır ilerleme yok; (2) bir ADR'yi belirleyecek ve bizde uzmanlığı olmayan bir karar. Kalıp:

```
## <saat> — <kimden> — <konu>
Ne denedik:
Karar noktası:
Seçenekler:
Durum: bekliyor | soruldu | cevaplandı (cevap: docs/log/…)
```

## 16:50 — karar masası (Volkan adına) — Gerçekçi farazi şehir, modelin hata payı ve mimari (17:00'de yeniden yazıldı: giriş eklendi)
Ne denedik: Aşağıdaki gönderilecek metinde. Kısaca: deneme şehirleri gerçek Kıbrıs verisine çapalı (EAC 2022 eğrileri, Kıb-Tek 2023 büyüklükleri), bugün trafo başına mahalle çarpanı eklendi (İspanya yayılımına çapalı: CV 0,46 / 0,14); şablon modeli; kontroller farazi %8,6 (saf tahmin %9,7), İspanya %25 → fatura ile %10, İngiltere gerilim fiziği 6 hatta 4'ü ±%40.
Karar noktası: hata payını küçültme önceliği; çapalama istatistikleri; mimari; yanlış yeşil için karamsar senaryo yeterli mi.
Seçenekler: cevap ADR-0009'a (hata payı önceliği) ve Faz 5 hikâyesine girer; cevapsız kalırsa mevcut kararlarla (ADR-0007 fatura, ADR-0008 mahalle çarpanı) devam.
Durum: bekliyor

Gönderilecek metin (Volkan iletir):

> Merhaba Muhittin hocam, projede ilerledik, kısa bir danışma.
>
> Hatırlatma: Kıb-Tek mahalle trafolarını ölçmüyor; biz az sayıda trafoyu ölçüp gerisini şablonla tahmin eden, her trafo için "öğlen ne kadar dolu, kaç ev daha panel takabilir, ne kadar eminiz" diyen bir harita yapıyoruz. Sizin önerinizle problemi şekil + büyüklük diye böldük, doğrulamayı trafo bazında bir-dışarıda kurduk, belirsizliği bant olarak veriyoruz, gerilimi ilk sürüme aldık.
>
> Kıbrıs'ta gerçek trafo ölçümü olmadığı için modeli "deneme şehirlerinde" geliştiriyoruz: bilgisayarda kurduğumuz, cevap anahtarı bizde olan 20 farazi Kıbrıs kasabası (sizin "alan rastgeleleştirme" öneriniz). Bunları gerçeğe şöyle çapaladık: eğri şekilleri Güney Kıbrıs'ın 2022 sayaç eğrileri; büyüklükler Kıb-Tek 2023 sınıf tüketimi bölü abone sayısı; hat boyu, kablo, abone karışımı varsayım aralıkları; şehirden şehre tüketim, saat, panel yaygınlığı, hava yılı rastgele. Bugün bir eksik bulduk: trafolar birbirine fazla benziyordu. İspanya'dan 29 gerçek trafonun sayaç verisini indirip karşılaştırdık; gerçekte müşteri başına öğlen yükü trafodan trafoya 0,46 değişim katsayısıyla oynuyor, bizde 0,14'tü. Üreticiye trafo başına bir "mahalle çarpanı" ekledik, gücünü bu yayılıma çapalıyoruz.
>
> Durum: deneme şehirlerinde öğlen en düşük yük hatası ortanca %8,6; ama hiç model kullanmadan "müşteri başına ortalama × müşteri" diyen saf tahmin bile %9,7 veriyor, bu yüzden sınava saf tahmin kıyası koyduk. İspanya'nın gerçek trafolarında aynı yöntem yalnız müşteri sayısıyla %25 hata veriyor, trafodaki abonelerin fatura toplamı girince %10'a iniyor. Gerilim tarafını İngiltere'den gerçek ölçümle sınadık (20 trafo, hat ucunda 6 ev, dakikalık gerilim): bizim yük akışı hesabı 6 hattın 4'ünde ölçülen yükselmenin ±%40 içinde; 2'sinde paneller hattın ucunda toplandığı için eşit yayılmış model yükselmeyi yarıdan az gösterdi. Karamsar senaryoyu buna göre kurduk: yeni paneller hattın ucunda, tek fazda, düşük yük, trafo çıkışı 250 V.
>
> Dört sorum var:
> 1) Modelin kendi ölçtüğü hata payını küçültmek için öncelik ne olmalı: daha çok ölçülü trafo mu (bizde 5'ten 15'e çıkmak hatayı düşürmedi), fatura gibi daha iyi girdi mi (2,5 kat düşürdü), yoksa mahalle farkını açıklayan dış değişkenler mi (gelir, bina yaşı, klima)?
> 2) Deneme şehrini gerçeğe çapalarken hangi istatistikleri eşlemeliyiz? Bizim seçtiklerimiz: trafolar arası müşteri başına öğlen yükü yayılımı, eğri benzerliği, trafo çıkış gerilimi dağılımı, faz dengesizliği. Eksik var mı; İspanya'ya "fazla uydurma" riskini nasıl önleriz?
> 3) Mimari şu an dört parça: deneme şehri (geliştirme) → İspanya (yük doğrulaması) → İngiltere (gerilim doğrulaması) → Kıbrıs pilot (gerçek doğruluk). Sizce bu dağınık mı, tek hikâyeye nasıl bağlanır, öne çıkarılacak rakam hangisi olmalı?
> 4) Yanlış yeşil (dolu trafoya "yer var" demek) için karamsar senaryo yeterli bir koruma mı, yoksa trafo başına ölçüm olmadan yeşil hiç verilmemeli mi?
>
> Teşekkürler.
