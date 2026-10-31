# Konuşma notu — taslak (BUILD, 31 Ekim akşam; 21:00'de karar masası 20:47 ve Faz 3 / Faz 4 sonuçlarıyla güncellendi)

Hikâye Volkan'ın; bu, karar masasının 17:00 kararına (güven merdiveni) göre rakamları yerine oturtulmuş iskelet. Can slaytlara (`docs/sunum/`) taşır. Sunum haritanın içinde 7 ekran (Volkan 17:32); ekran metni Can'ın [ekranlar.md](sunum/ekranlar.md)'sinde.

Süre hedefi 6 dakika: açılış 45 sn · sorun 1 dk · fikir 45 sn · güven merdiveni 2 dk · canlı harita 1 dk · kapanış 30 sn.

Kural:
- Her rakamın yanında kaynağı ya da "gösterim" etiketi slaytta.
- Farazi şehir rakamı manşet değil.
- "Sınanmadı" etiketli cümleler yalnız konuşmada ve soru-cevapta, slaytta yazılmaz.

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
> "Her trafoya cihaz takmak pahalı. Birkaçını ölçüyoruz, gerisini tahmin ediyoruz; tahminin ne kadar emin olduğunu da söylüyoruz."

- Yöntem İngiltere'den: 800 trafoyu ölçüp ağın geri kalanını tahmin ettiler, ~%80 doğruluk [Kaynaklı: Ofgem 2015].
- Biz Kıbrıs'a uyarladık:
  - hedef baharın öğlen en düşük yükü;
  - üstüne gerilim hesabı, bilinmeyenler aralığından çekilerek (olasılıklı, ADR-0011);
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
   - "6 gerçek hattın 5'inde ölçülen yükselme hesabımızın güvenli sınırının altında kaldı. Birinde yükselmeyi küçük gördük; bu yüzden canlıda yeşil önce pilotla sınanır."
   - [Hesap: PR #11, olasılıklı geri-test; UKPN 2014, CC BY]
4. **Kıbrıs pilotu: sahada son basamak.**
   - "Harita için Kıb-Tek'ten yeni veri istemiyoruz: abone sayısı ve fatura toplamı zaten elinde. Pilotta ilk ölçeceğimiz şey trafonun çıkış gerilimi; o tek ölçüm 'dolu' dediğimiz trafolardaki yanılmayı %27'den %19'a indirir."
   - [Hesap: bilginin değeri denemesi, farazi şehir 11–20, kusursuz bilgi üst sınırı; [Faz 3 günlüğü](log/2026-10-31-volkan-faz3.md)]
   - Yalnız konuşmada: "Kıb-Tek'in kendi kayıtlarında panelli abonenin adresi ve fazı varsa %4'e." (aynı etiket)
   - Ölçek: "Ada geneli için 120–170 trafo yeter." [Hesap: araştırma; İngiltere'de ölçülen pay %2,6]

## 5. Canlı harita (1 dk; Civan sürer)
- Şehir açılır (sehir-001 varsayılan). Trafolar yeşil / sarı / kırmızı.
- **Yeşil:** sıradaki iki başvuru %98 olasılıkla sığıyor, model de emin. Ölçmeden "evet" denebilir.
- **Sarı:** sınırda ya da emin değiliz. Ölçüm cihazı buraya gider.
- **Kırmızı:** bugün bile sınır aşılıyor olabilir (olasılık ≥ %50). "Ret" değil: ölç ya da güçlendir. Kırmızıların %27'sinde gerçekte yer var.
- Sayının dili: "yaklaşık N ev daha sığar (A–B)". Sayı ortanca, aralık %80 bant; "en az" denmez, vaat renkte (karar masası 19:13).
- Üç tıklama, sehir-001 (farazi, cevabını biliyoruz):
  1. **T02, sarı şehir konutu (100 kVA):** "Bugünkü kural 2 ev diyor. Biz yaklaşık 16 ev diyoruz (7–17). Bu deneyde gerçekte 17 ev sığıyor: kural bekletmeye gerek olmayan başvuruları bekletiyor."
  2. **T06, kırmızı köy trafosu (100 kVA):** "Bu trafo dolu. Bugünkü kural 'bir ev daha olur' diyor; biz kırmızı diyoruz, önce ölçülmeli."
  3. **T07, yeşil otel (630 kVA):** "5 başvurunun hepsi sığıyor; ilk ikisi güvenle, ölçmeden evet."
- **Kilit grafik** (farazi şehir, gösterim, sınav şehirleri 11–20, karar masası koşumu):

  > "Dolu trafoya 'yer var' demek en pahalı hata. %40 kuralı 73 dolu trafonun 41'ine 'yer var' diyor. Bizim 87 yeşilimizin hiçbiri dolu değil."

  - Yeşil %25, sarı %62. Bu bilerek: konut trafolarında ölçmeden evet demiyoruz, önce ölçüyoruz.

## 6. Kapanış (30 sn)
> "Harita için Kıb-Tek'ten yeni bir şey istemiyoruz. Trafo başına abone sayısı ve fatura toplamı zaten elinde. Bunlarla hangi mahallede kaç ev daha panel takabileceğini haritada görür, ölçüm cihazını en çok işe yarayacağı yere takar."

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
- Yeşil için iki şart birden: sıradaki iki başvurunun %98 olasılıkla sığması ve yüksek güven (ADR-0010, ADR-0011).
- Sınav şehirlerinde 87 yeşilin hiçbiri dolu değil (gösterim). İngiltere'nin 6 gerçek hattının 5'inde güvenli sınır tuttu.
- Canlıda hedef bütçe %2'nin altı; pilotta ölçümle sınanır.
- Kırmızı "ret" değil: ölç ya da şebekeyi güçlendir (ADR-0005).

**Sarı neden bu kadar çok (%62)?** (karar masası 20:47)
- "Eşiği gevşetsek dolu trafoya 'yer var' demeye başlarız. Ölçüm kırmızıdaki yanılmayı düzeltir: trafonun çıkış gerilimi bilinince yanlış kırmızı %27'den %19'a iner. Sarının çoğu ise 'bir sonraki başvuru hattın neresinden gelecek' sorusu; onu haritada değil başvuru anında, evin adresiyle tek tek hesaplarız."
- Son cümle **sınanmadı** ([ADR-0012](decisions/adr-0012-sari-trafoda-karar-basvuru-aninda.md)); slaytta yazılmaz.

**Malta akıllı sayaçla çözdü; siz neden sayaç istemiyorsunuz?** (karar masası 20:47)
- "Malta'nın sayaçları kayıp ve faturalama için alındı. Malta'nın açık kapasite haritasında izin verilen ek panel hiçbir trafo merkezinde trafo gücünün %25'ini geçmiyor. Biz her trafoya gerilimle ayrı bakıyoruz."
- [Hesap: Enemalta kapasite haritası verisi, 31 Ekim 2026; Enemalta'nın yazdığı kural değil, bizim çıkarımımız; [ada ülkeleri günlüğü](log/2026-10-31-volkan-ada-ulkeleri.md)]
- "Hawaii de düz bir kuralla başladı, tepe yükün %15'i. Kanıt geldikçe gündüz en düşük yükün %250'sine çıkardı. Bizim harita o kanıtın trafo trafo hâli." [Kaynaklı: HECO 2014; Sunrun 2022]

**Neden İngiltere yöntemi Kıbrıs'ta tutsun?**
- Tutup tutmadığını bilmiyoruz; o yüzden merdiven var.
- Klima ve yoğun panel İngiltere'de yok. Pilot bunun için.

**Kişisel veri?**
- Trafo düzeyinde toplam; ev ev veri yok.

---

## Prova listesi
- **Süre:** 6 dakika, kronometreyle; iki prova.
- **Sunum bilgisayarı:**
  - `data/raw/osm-kasaba/girne_merkez.json` indirilmiş olmalı (komut KAYNAK.txt'de). Yoksa zemin internetten gelir.
  - `streamlit run app/harita.py`. Bir kez interneti kapatıp açılışı dene.
  - Mac'te denendi (BUILD, 20:55): 3 şehir, tıklama 0,35–0,40 sn, dışarıya istek yok. Windows denenmedi.
- **Tıklama sırası:** sehir-001 → T02, T06, T07 (yukarıda). Sütunlar küçük; yerlerini provada ezberle.
  - Şehirler sunum bilgisayarında yeniden üretildiyse tek tük trafo farklı çıkabiliyor (11–20'de bir trafo farkı görüldü, Faz 3 günlüğü). Provada bu üç trafonun panelde yazanını yukarıdaki cümlelerle karşılaştır.
- **Civan düzeltene kadar ekranda olanlar** (civan.md KONTROL 20:55):
  - panel ortadaki sayıyı göstermiyor ("7–17 ev"); konuşmada "yaklaşık 16" de;
  - yeşilde "En kötü durumda bile yer var" yazıyor; konuşmada "ilk iki başvuru güvenle" de;
  - büyük trafolarda %40 kuralının ev sayısı trafodaki panelsiz evden fazla çıkıyor (T07'de kural 38, ev 5). Konuşmada "kural buradaki bütün evlere izin veriyor" de.
- **Yedek:** 2 dakikalık ekran kaydı ve PDF henüz yok (Civan, Can).
