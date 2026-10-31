# Konuşma notu — taslak (BUILD, 31 Ekim akşam)

Hikâye Volkan'ın; bu, karar masasının 17:00 kararına (güven merdiveni) göre rakamları yerine oturtulmuş iskelet. Can slaytlara (`docs/sunum/`) taşır. Civan'ın "sunum haritanın içinde 7 ekran" önerisi karar masasında; o kabul edilirse aynı metin ekranlara bölünür.

Süre hedefi 6 dakika: açılış 45 sn · sorun 1 dk · fikir 45 sn · güven merdiveni 2 dk · canlı harita 1 dk · kapanış 30 sn.

Kural:
- Her rakamın yanında kaynağı ya da "gösterim" etiketi slaytta.
- Farazi şehir rakamı manşet değil.

---

## 1. Açılış (45 sn)
> "Bu sokakta kaç ev daha çatısına güneş paneli takabilir? Bugün Kıb-Tek bunu bilmiyor."

> "Kuzey'de çatısına panel koymak için sırada bekleyen yaklaşık 2.670 ev var."
> [Kaynaklı: KTTO raporu, Mart 2023; [araştırma](log/2026-10-31-kapsamli-arastirma.md)]

> "Güney panelleri bağladı. 2025'te dağıtım şebekesine bağlı güneş ve biyogaz üretiminin yaklaşık yarısını (%47) kıstı."
> [Kaynaklı: pv magazine, CyprusGrid verisi]

> "Kuzey bağlamadan önce nereye sığdığını bilmeli."

## 2. Sorun (1 dk)
- Her mahallenin köşesinde bir trafo var; panel, klima, elektrikli araç önce onu zorlar.
- Kıb-Tek büyük hatları izliyor, mahalle trafolarını izlemiyor [Kaynaklı: KTTO 2023]. Bu yüzden kaba bir kural kullanıyor: trafo gücünün %40'ı.
- Bu kural iki yönde yanılıyor: bazı trafolarda gereksiz yere "hayır" diyor, bazılarında dolu trafoya "evet" diyor.
- Baharda öğlen: güneş en güçlü, tüketim en düşük. Gerilim sınırı o an aşılıyor. Kurulumcu gerilimi tek gün, tek noktada ölçüyor. Biz trafonun gün ve mevsim boyu davranışını tahmin ediyoruz: **fotoğraf değil film.**

## 3. Fikir (45 sn)
> "Her trafoya cihaz takmak pahalı. Birkaçını ölçüyoruz, gerisini tahmin ediyoruz."

- Yöntem İngiltere'den: 800 trafoyu ölçüp ağın geri kalanını tahmin ettiler, ~%80 doğruluk [Kaynaklı: Ofgem 2015].
- Biz Kıbrıs'a uyarladık:
  - hedef baharın öğlen en düşük yükü;
  - üstüne gerilim hesabı;
  - girdi Kıb-Tek'in zaten elinde olan bilgi: trafodaki abone sayıları ve fatura toplamı.

## 4. Güven merdiveni (2 dk)
> "Kıbrıs'ı ölçemiyoruz. Yöntemi ölçebildiğimiz her şeyde kanıtlıyoruz, sonra uyguluyoruz."

Her basamakta tek iddia, tek rakam; hepsi "hiç model kullanmadan yapılan saf tahmine göre ne kadar iyi" diye.

1. **Farazi Kıbrıs şehri: cevabını bildiğimiz kontrollü deney** (gösterim).
   - 20 şehir, 800 trafo; gerçek Kıbrıs tüketim eğrileri ve güneşiyle.
   - Ölçmediğimiz trafolarda öğlen yükü hatası:
     - faturayla ~%4;
     - saf tahmin (fatura × ortak oran) ~%6;
     - yalnız abone sayısıyla ~%22.
   - Bu üst sınır: gerçek veri daha zor.
2. **İspanya: hiç görmediğimiz 29 gerçek trafo** (manşet).
   - "Yalnız müşteri sayısıyla ortanca hata %25. Kıb-Tek'in zaten elinde olan fatura toplamını ekleyince **%10**."
   - [Hesap: PR #10, EDP Oviedo 2018, CC BY]
3. **İngiltere: gerilim fiziği, 6 gerçek hat.**
   - "Hesabımız 6 hattın 4'ünde ölçülen yükselmeyi ±%40 içinde tutturdu."
   - "İkisinde paneller hattın ucunda toplanmıştı, model yükselmeyi az gösterdi. Bu yüzden karamsar senaryomuz bekleyen panelleri hattın ucuna koyuyor."
   - [Hesap: PR #11, UKPN 2014, CC BY]
4. **Kıbrıs pilotu: sahada son basamak.**
   - "Baharda 20–50 trafoya ölçüm cihazı; ilk ölçeceğimiz şey trafo çıkış gerilimi."
   - Ölçek: "Ada geneli için 120–170 trafo yeter." [Hesap: araştırma; İngiltere'de ölçülen pay %2,6]

## 5. Canlı harita (1 dk; Civan sürer)
- Bir şehir açılır. Trafolar yeşil / sarı / kırmızı.
- **Yeşil:** sıradaki iki başvuru %98 olasılıkla sığıyor, model de emin. Ölçmeden "evet" denebilir.
- **Sarı:** sınırda ya da emin değiliz. Ölçüm cihazı buraya gider.
- **Kırmızı:** en kötü durumda yer yok. (Kural karar masasında; konuşmayı karara göre düzelt.)
- Bir otel trafosuna tıkla: "yaklaşık N ev daha sığar (A–B arası); %40 kuralı şunu diyor." Sayı haritadaki ortanca, aralık %80 bant; "en az" denmez, vaat renkte (karar masası 19:13).
- **Kilit grafik** (farazi şehir, gösterim, sınav şehirleri):

  > "Dolu trafoya 'yer var' demek en pahalı hata. %40 kuralı dolu trafoların yarısından fazlasına 'yer var' diyor: 284 'evet'in 41'i yanlış. Bizim yeşillerimizin hiçbiri yanlış değil."

  - Yeşil az, %6. Bu bilerek: konut trafolarında ölçmeden evet demiyoruz, önce ölçüyoruz.

## 6. Kapanış (30 sn)
> "Kıb-Tek'ten yeni bir şey istemiyoruz. Trafo başına abone sayısı ve fatura toplamı zaten elinde. Bunlarla hangi mahallede kaç ev daha panel takabileceğini haritada görür, ölçüm cihazını en çok işe yarayacağı yere takar."

> "Farazi şehirdeki isabet gerçeğin üst sınırı. Gerçek veride İspanya'da %10. Kıbrıs'taki doğruluğu pilot söyler."

---

## Olası sorular (kısa cevap)

**Neden farazi şehir?**
- Kıbrıs'ta trafo ölçümü yok.
- Cevabı bildiğimiz şehirde yöntemi sınıyoruz, sonra gerçek veride (İspanya, İngiltere) dışarıdan sınıyoruz.
- Farazi rakam manşet değil.

**Fatura yoksa?**
- Hata %25 seviyesine çıkar (İspanya da farazi de aynı).
- Model o zaman "yüksek güven" vermez; trafolar sarıya düşer, ölçüm oraya gider.

**Yanlış yeşil olursa ne olur?**
- Yeşil için üç şart birden: en kötü senaryo, marj, yüksek güven.
- Canlıda hedef bütçe %2'nin altı; gerçek veride geri-testle tutulur (ADR-0010).
- Kırmızı "ret" değil: ölç ya da şebekeyi güçlendir (ADR-0005).

**Neden İngiltere yöntemi Kıbrıs'ta tutsun?**
- Tutup tutmadığını bilmiyoruz; o yüzden merdiven var.
- Klima ve yoğun panel İngiltere'de yok. Pilot bunun için.

**Kişisel veri?**
- Trafo düzeyinde toplam; ev ev veri yok.
