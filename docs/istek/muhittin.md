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
Durum: cevaplandı 17:00 (cevap: docs/log/2026-10-31-muhittin-cevap-2-hata-payi-mimari.md; kararlar ADR-0009, ADR-0010)

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

## 20:52 — karar masası (Volkan adına) — Sunumdan sonra: modeli gerçek veriyle nasıl iyileştiririz; çalışma belgeleri ve talimatlar nasıl olmalı
Ne denedik: (21:04: Can'ın "Malta gibi iki sayılı kart" sorusu eklendi, volkan.md 20:58 sonrası) Faz 3 bitti (olasılıklı hesap, ADR-0011); bilginin değeri denemesi (Faz 3 günlüğü 19:55): trafo çıkış gerilimi bilinince yanlış kırmızı %27 → %19, adres ve fazla %4; sarı %62 → %57, tam ağda %41. İngiltere geri-testi 6 hattın 5'i. Başvuru-anı kararı ADR-0012 (sınanmadı). Veri edinme yolları DEVIR'de (inverter kaydı, akıllı priz, plaka, Kıb-Tek kayıtları, pilot).
Karar noktası: Volkan (20:52): "bundan sonra iş modeli verilerle iyileştirmek; bunu nasıl yapacağımızı, doğru talimatların ve belgelerin nasıl olması gerektiğini Muhittin'e soralım; veri işe yarar deniyor ama düzeltme önerilmiyor." Cevap ROADMAP "sunum sonrası / pilot" planına, üretici 1.3'e ve görev kartı kalıbına girer.
Seçenekler: Aşağıdaki metinde bizim önerdiğimiz sıra var; Muhittin düzeltir ya da onaylar. Cevapsız kalırsa önerilen sırayla devam.
Durum: bekliyor

Gönderilecek metin (Volkan iletir):

> Merhaba Muhittin hocam, sunum öncesi son danışma; bu kez sonrası için.
>
> Nerede kaldık: Önerdiğiniz gibi kurduk. Deneme şehirlerinde öğlen yükü hatası faturayla ortanca %3,8, İspanya'nın 29 gerçek trafosunda %10 (faturasız %25). Panel kararında yeşil kuralınızı olasılıkla uyguladık: bilinmeyenleri (trafo çıkış gerilimi, panelin yeri ve fazı, hat boyu) gerçek veriye dayalı aralıktan kırk kez çekip ev ev benzetim koşuyoruz; dolu trafoya "yer var" hiç demedi (87 yeşilde 0), kaç ev sayısında ortanca 2 ev sapıyor. Bedeli: trafoların %62'si sarı, kırmızıların %27'sinde aslında yer var. İngiltere'nin 6 gerçek hattında gerilim tahmini 5'inde güvenli sınırın altında kaldı, birinde (paneller yüksüz bir kolda) yükselmeyi küçük gördü.
>
> Sonra ne hangi bilgiyi düzeltir diye ölçtük: trafo çıkış gerilimi bilinince yanlış kırmızı %27'den %19'a iniyor, panelli evlerin adresi ve fazı da bilinirse %4'e. Sarı ise bilgiyle az düşüyor (%62'den %57'ye; ağın tamamı bilinse bile %41), çünkü yeşil kuralı "sıradaki başvuru hattın neresinden gelirse gelsin sığsın" diyor. Bunun üzerine sarı trafoda kararı haritada değil başvuru anında, başvuranın adresiyle vermeyi düşündük; henüz sınamadık.
>
> Bundan sonraki iş modeli gerçek veriyle iyileştirmek. Elimize girebilecek veri, ucuzdan pahalıya: panelli evlerin inverter uygulamasındaki 5 dakikalık gerilim kaydı (gece kaydı yok), birkaç evde gerilim ölçen akıllı priz, trafo plakası ve kademe, Kıb-Tek'in abone–trafo ve faz kayıtları, pilotta sarı trafoların hat ucunda geçici ölçüm. Bizim önerdiğimiz sıra şu: (1) önce trafo çıkış gerilimi, çünkü tek başına en çok düzelten o; hesapta aralık yerine ölçülen değer; (2) her ölçülen trafo modele öğretici olarak girer ve aralıklar (bant, çekiliş dağılımları) ölçümle yeniden ayarlanır; (3) deneme şehri üreticisi gerçek dağılımlara çapalanır (öğlen orta gerilim değişimi, panellerin hat üstündeki yeri, trafo içi tüketim çeşitliliği) ve test şehirleri yeniden üretilir; (4) başvuru-anı kararı sınanır. Her adımda ölçü: yanlış yeşil bütçesi (<%2), yanlış kırmızı, sarı oranı, kaç ev hatası; geliştirme ve sınav şehirleri ayrı, sınav şehrine göre ayar yok.
>
> Sorularım:
> 1) Bu sıra doğru mu, neyi atlıyoruz? Hangi veri ne kadar gelince "model iyileşti" deriz; ölçülen trafo sayısı için bir hedef koymalı mıyız?
> 2) Ölçülen trafo modeli nasıl güncellemeli: ölçüm geldikçe aralıkları daraltmak mı, belli sayıda ölçümden sonra baştan eğitmek mi? Aralıkların "fazla emin" çıkmasını (kusursuz bilgide bant kapsaması %80'den %57'ye düştü) nasıl yakalarız?
> 3) Bu döngüyü ekibin ve yapay zekâ ajanlarının belge düzeniyle yürütüyoruz; şablonu sizden almıştık (karar kayıtları, günlük, görev kartı, veri sözleşmesi, devir notu). "Veri geldi → modeli güncelle → sına → raporla" döngüsü için bu belgeler ve ajan talimatları nasıl olmalı: bir veri partisi için görev kartında ne yazmalı, hangi kurallar sabit kalmalı (sınav setine ayar yok, geri-test bütçesi, her rakama kaynak), deney günlüğü nasıl tutulmalı, "bitti" ne zaman denir?
> 4) Sarı trafoda kararı başvuru anında başvuranın adresiyle vermek size mantıklı geliyor mu, yoksa sarıyı azaltmanın daha doğru bir yolu var mı?
>
> Bir de ekipten Can'ın sorusu. Malta'nın açık kapasite haritasında her trafo merkezine tıklayınca iki sayı çıkıyor: tüketim için kalan yer (kVA) ve güneş için kalan yer (kWp). Bizim harita bugün yalnız güneşe bakıyor. Aynı iki sayıyı, tahmin ve aralık olarak, Kıbrıs'ta göstermek istiyoruz. Güneş tarafı hazır. Yük tarafı için en yüksek yükü tahmin etmek gerekiyor; modelimiz onu hedeflemedi. Can üç yol denedi: eğri şeklini öğlen değeriyle ölçeklemek (tepe hatası ortanca %16, en kötü onda birde %33), faturadan düz oran (%4 / %17), ve öğlen tahminini ölçülü trafoların tepe-öğlen oranıyla çarpmak (%4 / %10). Ama elimizdeki tepe Nisan'ın tepesi; Kıbrıs'ın gerçek tepesi Temmuz akşamı klima yükü.
> 5) Yük için boş kapasiteyi bu yolla vermek doğru mu, yoksa tepe yükü ayrı bir model mi ister? Nisan tepesini yıl tepesine çevirmek için ne yapılmalı (sınıf profillerinden mevsim oranı yeterli mi)? Güç katsayısı bilinmezken kW mı yazmalı, kVA mı?
> 6) Sizce harita iki sayılı bu kartla mı anlatılmalı (yük ve güneş yan yana), yoksa güneş katmanı tek başına daha mı dürüst?
>
> Teşekkürler.
