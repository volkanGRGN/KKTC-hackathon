# Sunum — 8 ekran (haritanın içinde)

Biçim kararı: Volkan 17:32 (can.md BİLGİ, civan.md). Sunum Civan'ın harita uygulamasının içinde 8 kısa ekran (0–7). Her ekranda tek cümle, tek görsel, en fazla bir rakam. Teknik terim yok (arketip, kVA, P10 sunum dilinde geçmez). **PDF yedeği bu metinden.**

- Akış **yük haritası öne** (Volkan 09:43; sıra KARAR 10:16): sorun (0–3) → yük haritası (4) → neden inanılır (5) → panel güvenli uçlar (6) → pilot ve maliyet (7) → jüri cevapları ([konusma-notu.md](konusma-notu.md)). Civan'ın pitch şablonu aynı sıraya uyar (civan.md 09:43).
- Rakam kaynağı `dashboard/icerik.json` (KARAR 09:43). Yük rakamları tepe modeli B-Y2, hiç bakılmamış sınav şehirleri 41–50; panel rakamları 31–40; ikisi de üretici 1.5, farazi, gösterim (KARAR 10:26, 10:43).
- Rakamların etiketi her ekranda yazılı; ayrıntılı kaynak [slaytlar.md](slaytlar.md) "Kaynak slaydı".
- Konuşma: BUILD taslağı [../konusma-notu-taslak.md](../konusma-notu-taslak.md) (eski sıra); dürüstlük cümleleri [konusma-notu.md](konusma-notu.md).
- Süre hedefi 6–7 dk [Yorum].

| Ekran | Cümle (ekranda yazan) | Görsel | Tek rakam ve etiketi | Süre |
|---|---|---|---|---|
| **0 Açılış** | "Bu sokakta kaç ev daha çatısına güneş paneli takabilir? Kıb-Tek bilmiyor." | Bir sokak, çatılar | — | 20 sn |
| **1 Kıb-Tek** | "Kıb-Tek, Kuzey Kıbrıs'ta elektriği üreten ve evlere dağıtan devlet kurumu." | Ada haritası | — | 15 sn |
| **2 Mahalle şebekesi** | "Her mahallenin köşesinde gri bir kutu (trafo) var; elektriğin evden önceki son durağı. Kıb-Tek bu kutuları izlemiyor; dolu mu boş mu bilmiyor. Bu yüzden temkinli: evler sırada bekliyor." | Direk, kutu, evler | **~2.670 bekleyen başvuru** [Kaynaklı: KTTO raporu, Mart 2023; adres doğrulanmadı] | 45 sn |
| **3 Fikrimiz** | "Her kutuya cihaz takmak çok pahalı. Birkaçını ölçüyoruz, gerisini tahmin ediyoruz; her kutu için iki şey söylüyoruz: ne kadar dolu, güneşe ne kadar yer var. Ne kadar emin olduğumuzu da." | "Noktalar çoğalıyor": önce bir ölçülen trafo, sonra birkaçı, sonra tahmin adaya yayılıyor (ölçülen dolu, tahmin soluk; "gösterim") — 3 → 5 geçişi | İngiltere aynı yöntemle ~%80 tuttu [Kaynaklı: Ofgem, WPD LV Templates 2015] | 40 sn |
| **4 Yük haritası** | "Yılın en yoğun saatinde (çoğunlukla yaz akşamı) hangi kutu dolu? Dolu olanı kaçırmadan, önce nereye bakacağınızı söylüyoruz." | Canlı harita, yük katmanı: doluluk renkleri, "ön" etiketi, bir kutuya tıklayınca akşam gerilimi | **%80'den dolu 12 kutunun 12'si yakalandı** (bedeli: her 10 uyarıdan 1'i gerçek; "yeterli" dediğimiz 211 kutunun hiçbiri akşam 207 voltun altına inmedi) [Hesap: sınav şehirleri 41–50 (hiç bakılmamış), üretici 1.5, ölçülmeyen 280 trafo, tepe modeli B-Y2; docs/log/2026-11-01-can-eszamanlilik.md; `dashboard/icerik.json`] — gösterim | 1 dk |
| **5 Neden inanılır** (güven merdiveni) | "Kıbrıs'ı ölçemiyoruz. Yöntemi ölçebildiğimiz her yerde sınadık." | Dört basamak; manşet büyük | **İspanya, 29 gerçek trafo: %25 → %10** (öğlen yükü; yalnız müşteri sayısıyla → fatura toplamıyla, ortanca hata) [Hesap: PR #10, EDP Oviedo 2018, CC BY] | 1,5 dk |
| **6 Panel: güvenli uçlar** | "Bir kutuya tıklayın: yaklaşık N ev daha sığar (A–B); yeşilse ilk 2 başvuru güvenle. Bugünkü kural ne diyor, yanında." (N = `kac_ev_orta`, A–B = karamsar–iyimser, "%80 ihtimalle A–B ev"; "en az" yazılmaz — karar masası 19:13) | Canlı harita, panel katmanı; yanında kilit grafik [kilit_yanlis_yesil.png](kilit_yanlis_yesil.png) | **Dolu trafoya "yer var": bugünkü %40 kuralı 46 dolu trafonun 24'üne, biz hiçbirine** (yanlış yeşil: biz 0/60) [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`] — gösterim | 1 dk |
| **7 Pilot ve maliyet** | "Harita için Kıb-Tek'ten yeni veri istemiyoruz: abone sayısı ve fatura toplamı zaten elinde. Pilotta ilk ölçeceğimiz şey trafonun çıkış gerilimi." | Takvim + cihaz | **120–170 trafo, ~2,2–3,2 milyon TL: her trafoya cihaz takmanın yüzde biri** [Hesap: araştırma günlüğü §7; docs/log/2026-11-01-can-maliyet.md] | 40 sn |

Eski rakamlar kullanılmaz: "%27 → %19" (eski yanlış kırmızı ölçüsü; ADR-0017'den beri kırmızı yok, KARAR 10:16), yük için %5,8 / 16/16 / 87 uyarı / 233 (eski model ve şehirler, KARAR 10:26).

## Ekran 4: yük haritası (ekranda kısa, konuşmada açılır)
- Yılın tepesi "ön" etiketli: deneme şehrinde hata ortanca %11,4, en kötü onda birlik dilimde %23,9; tahmin gerçeğin ortanca %11 üstünde (güvenli yön), gerçek hiçbir trafoda bandın üstüne çıkmadı [Hesap: ekran 4'teki küme].
- Model cümlesi (KARAR 10:43): "Tepe modelimiz Kıbrıs evlerinin gerçek sıcaklık duyarlılığını kullanır; deneme şehirlerinde bu yüzden yaklaşık %11 fazla tahmin eder, yani güvenli tarafta; gerçek bahar verisinde hata %15." [eğim: 20 Kıbrıs evi, docs/log/2026-11-01-can-eszamanlilik.md; gerçek: İspanya Mayıs tepesi %15,4 / %36,1]
- Bedel: temkinli uç çok uyarı veriyor (124 uyarının 12'si gerçek); harita ret değil "önce bak" listesi.

## Ekran 5: dört basamak (ekranda kısa, konuşmada açılır)

Hepsi "hiç model kullanmadan yapılan basit hesaba göre ne kadar iyi" diye anlatılır.

1. **İspanya, öğlen yükü** (manşet): %25 → %10, gerçek veri. Cümle (karar masası 22:21): "Kıb-Tek'in zaten elindeki fatura toplamı girince gerçek trafolarda hata %25'ten %10'a iniyor; biz bunun üstüne ne kadar emin olduğumuzu ve panelin sığıp sığmadığını söylüyoruz." "Modelimiz indirdi" denmez (%10 faturanın değeri). Parantez: "(aralığımız İspanya'da %82,1 tutuyor)" [gerçek veri, İspanya 28 trafo; docs/log/2026-11-01-volkan-faz7-kalibrasyon.md].
2. **İspanya, yılın tepesi** (yük): Mayıs tepesinde hata ortanca %15, en kötü onda birlik dilimde %36 [gerçek veri: %15,4 / %36,1; docs/log/2026-11-01-volkan-yuk-tepe-on.md]; Kıb-Tek'in tepe kaydı gelince daralır.
3. **İngiltere** (gerilim): "6 gerçek hattın 5'inde ölçülen yükselme hesabın güvenli sınırının altında; birinde küçük gördük → canlıda yeşil önce pilotla sınanır" [Hesap: PR #11 + docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md; UKPN, CC BY] (karar masası 18:46, ADR-0011).
4. **Farazi Kıbrıs şehri** (cevabını bildiğimiz deney; gösterim, üst sınır): faturayla öğlen yükü hatası ortanca %11,3, en kötü onda birlik dilimde %28 [Hesap: sınav şehirleri 31–40, üretici 1.5; `dashboard/icerik.json`]. Cümle: "Deneme şehrinde hata, gerçek veride (İspanya) gördüğümüzle aynı seviyede." Kıbrıs'taki doğruluğu pilot söyler (ekran 7).

## Ekran 6: sayının dili (karar masası 19:13)
- Manşet orta sayı: "yaklaşık 4 ev"; yanında bant "(2–7)", açılımı "%80 ihtimalle 2–7 ev" [Yorum: örnek değer, rakam değil]. "En az … ev" hiçbir yerde yazılmaz: bandın alt ucu taban değil, gerçek trafoların ~%10–15'inde altına düşer.
- Vaat renkte: yeşilde "ilk 2 başvuru güvenle sığar (≥ %98)"; sarıda "önce ölç"; kırmızıda "ölç ya da güçlendir". Sarı ve kırmızıda sayı yalnız bant.

## Ekran 6: kilit cümle
"Dolu trafoya 'yer var' demek en pahalı hata. Bugünkü %40 kuralı 46 dolu trafonun 24'üne 'yer var' diyor. Bizim 60 yeşilimizin hiçbiri dolu değil." [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`]; gösterim

## Ekran 6: söylenecek bedel
Rakamlar [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`]; gösterim. Eski 11–20 rakamları (yeşil %25, sarı %62, kırmızıların %27'si, 87 yeşil, 0/21) kullanılmaz.
- Yeşil az ve bu bilerek: ölçülmeyen 280 trafonun 60'ı yeşil, hiçbiri gerçekte dolu değil. — **0/60**
- Trafoların çoğunda emin değiliz: karar başvuru gelince verilir ya da önce ölçülür. — **renksiz %76**
- "Büyük olasılıkla dolu" uyarısı ret değil, "ölç ya da güçlendir": 22 uyarının 15'i gerçekten dolu. — **15/22 (%68)**
- Kaç ev hatası: 31–40'ta ortası 2 ev [Hesap: Can, Windows, `sinav.py faz3 --aralik 31-40`, n = 234; dashboard'da yok, karar masası teyit etmeden kullanılmaz]; eski 11–20 rakamı kullanılmaz

## PDF yedeği
Aynı 8 ekran, her biri bir sayfa: cümle + görselin ekran görüntüsü + rakam ve etiketi. Ekran görüntüleri Civan'ın uygulamasından (Faz 4); son sayfa kaynaklar ([slaytlar.md](slaytlar.md) "Kaynak slaydı").
