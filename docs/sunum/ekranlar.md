# Sunum — 7 ekran (haritanın içinde)

Biçim kararı: Volkan 17:32 (can.md BİLGİ, civan.md). Sunum Civan'ın harita uygulamasının içinde 7 kısa ekran (0–6). Her ekranda tek cümle, tek görsel, en fazla bir rakam. Teknik terim yok (arketip, kVA, P10 sunum dilinde geçmez). **PDF yedeği bu metinden.**

- Rakamların etiketi her ekranda yazılı; ayrıntılı kaynak [slaytlar.md](slaytlar.md) "Kaynak slaydı".
- Konuşma: BUILD taslağı [../konusma-notu-taslak.md](../konusma-notu-taslak.md); dürüstlük cümleleri [konusma-notu.md](konusma-notu.md).
- Süre hedefi 6 dk [Yorum].

| Ekran | Cümle (ekranda yazan) | Görsel | Tek rakam ve etiketi | Süre |
|---|---|---|---|---|
| **0 Açılış** | "Bu sokakta kaç ev daha çatısına güneş paneli takabilir? Kıb-Tek bilmiyor." | Bir sokak, çatılar | — | 20 sn |
| **1 Kıb-Tek** | "Kıb-Tek, Kuzey Kıbrıs'ta elektriği üreten ve evlere dağıtan devlet kurumu." | Ada haritası | — | 15 sn |
| **2 Mahalle şebekesi** | "Her mahallenin köşesinde gri bir kutu (trafo) var; elektriğin evden önceki son durağı. Kıb-Tek bu kutuları izlemiyor; dolu mu boş mu bilmiyor. Bu yüzden temkinli: evler sırada bekliyor." | Direk, kutu, evler | **~2.670 bekleyen başvuru** [Kaynaklı: KTTO raporu, Mart 2023; adres doğrulanmadı] | 50 sn |
| **3 Fikrimiz** | "Her kutuya cihaz takmak çok pahalı. Birkaçını ölçüyoruz, gerisini tahmin ediyoruz; tahminin ne kadar emin olduğunu da söylüyoruz." | "Noktalar çoğalıyor": önce bir ölçülen trafo, sonra birkaçı, sonra tahmin adaya yayılıyor (ölçülen dolu, tahmin soluk; yeşil / sarı / kırmızı; "gösterim") — 3 → 5 geçişi | İngiltere aynı yöntemle ~%80 tuttu [Kaynaklı: Ofgem, WPD LV Templates 2015] | 45 sn |
| **4 Neden inanılır** (güven merdiveni) | "Kıbrıs'ı ölçemiyoruz. Yöntemi ölçebildiğimiz her yerde sınadık." | Dört basamak; manşet büyük | **İspanya, 29 gerçek trafo: %25 → %10** (yalnız müşteri sayısıyla → fatura toplamıyla, ortanca hata) [Hesap: PR #10, EDP Oviedo 2018, CC BY] | 2 dk |
| **5 Canlı harita** | "Bir kutuya tıklayın: yaklaşık N ev daha sığar (A–B); yeşilse ilk 2 başvuru güvenle. Bugünkü kural ne diyor, yanında." (N = `kac_ev_orta`, A–B = karamsar–iyimser, "%80 ihtimalle A–B ev"; "en az" yazılmaz — karar masası 19:13) | Canlı harita; yanında kilit grafik [kilit_yanlis_yesil.png](kilit_yanlis_yesil.png) | **Dolu trafoya "yer var": bugünkü %40 kuralı 73 dolu trafonun 41'ine, biz hiçbirine** (yeşil yanlışı: biz 0/87, %40 kuralı 41/284) [Hesap: sınav şehirleri 11–20, olasılıklı hesap (ADR-0011), karar masası koşumu 31 Ekim 19:35–19:50, `sinav.py faz3`] — gösterim | 1 dk |
| **6 Pilot** | "Harita için Kıb-Tek'ten yeni veri istemiyoruz: abone sayısı ve fatura toplamı zaten elinde. Pilotta ilk ölçeceğimiz şey trafonun çıkış gerilimi; o tek ölçüm 'dolu' dediğimiz trafolardaki yanılmayı %27'den %19'a indirir." (karar masası 20:47) | Takvim + cihaz | **Ada geneli için 120–170 trafo** [Hesap: araştırma günlüğü §7; İngiltere'de ölçülen pay %2,6]; cümledeki %27 → %19 [Hesap: bilginin değeri denemesi, farazi şehir 11–20, kusursuz bilgi üst sınırı; docs/log/2026-10-31-volkan-faz3.md] | 30 sn |

## Ekran 4: dört basamak (ekranda kısa, konuşmada açılır)

Hepsi "hiç model kullanmadan yapılan basit hesaba göre ne kadar iyi" diye anlatılır.

1. **Farazi Kıbrıs şehri** (cevabını bildiğimiz deney; gösterim, üst sınır).
   - Faturayla %3,8, yalnız abone sayısıyla %20,6 ortanca hata [Hesap: sınav şehirleri 11–20, `sinav.py faz2`].
   - Cümle: "Fatura olmadan model ortalama trafoda basit hesaptan pek iyi değil; fatura girince hata dörtte bire iniyor."
2. **İspanya** (manşet): %25 → %10, gerçek veri.
3. **İngiltere** (gerilim): "6 gerçek hattın 5'inde ölçülen yükselme hesabın güvenli sınırının altında; birinde küçük gördük → canlıda yeşil önce pilotla sınanır" [Hesap: PR #11 + docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md; UKPN, CC BY] (karar masası 18:46, ADR-0011).
4. **Kıbrıs pilotu**: doğruluğu pilot söyler.

## Ekran 5: sayının dili (karar masası 19:13)
- Manşet orta sayı: "yaklaşık 4 ev"; yanında bant "(2–7)", açılımı "%80 ihtimalle 2–7 ev" [Yorum: örnek değer, rakam değil]. "En az … ev" hiçbir yerde yazılmaz: bandın alt ucu taban değil, gerçek trafoların ~%10–15'inde altına düşer.
- Vaat renkte: yeşilde "ilk 2 başvuru güvenle sığar (≥ %98)"; sarıda "önce ölç"; kırmızıda "ölç ya da güçlendir". Sarı ve kırmızıda sayı yalnız bant.

## Ekran 5: kilit cümle
"Dolu trafoya 'yer var' demek en pahalı hata. Bugünkü %40 kuralı 73 dolu trafonun 41'ine 'yer var' diyor. Bizim 87 yeşilimizin hiçbiri dolu değil." [Hesap: sınav şehirleri 11–20, karar masası koşumu; gösterim]

Grafik dosyası karar masasının Mac koşumundan, resmi veriden (0/87 ↔ 41/284, dolu 41/73; karar masası 21:44).

## Ekran 5: söylenecek bedel
Rakamlar karar masası koşumundan (karar masası 19:51; main fe7426b + `sinav.py` c3fb046, 20 şehir sıfırdan, sınav şehirleri 11–20, 347 trafo; Can'ın #15 deneme koşusuyla birebir). Eski tek denklem rakamları (%6 / %63 / %42, 0/21) artık kullanılmaz.
- Yeşil az: konut trafolarında ölçmeden "evet" demiyoruz. — **yeşil %25** (87/347; şehir konutunda 6/139)
- Trafoların çoğu sarı, yani "önce ölç". — **sarı %62** (216/347)
- Kırmızıların bir kısmında gerçekte yer var: kırmızı "ret" değil, "ölç ya da güçlendir". — **kırmızıların %27'sinde yer var** (12/44)
- Kaç ev: orta sayının ortanca hatası 2 ev (tavansız 239 trafo); gerçek %80 bandın içinde %81 [Hesap: sınav 11–20, `sinav.py faz3`, karar masası koşumu; gösterim]

## PDF yedeği
Aynı 7 ekran, her biri bir sayfa: cümle + görselin ekran görüntüsü + rakam ve etiketi. Ekran görüntüleri Civan'ın uygulamasından (Faz 4); son sayfa kaynaklar ([slaytlar.md](slaytlar.md) "Kaynak slaydı").
