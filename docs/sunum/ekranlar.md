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
| **5 Canlı harita** | "Bir kutuya tıklayın: yaklaşık N ev daha sığar (A–B); yeşilse ilk 2 başvuru güvenle. Bugünkü kural ne diyor, yanında." (N = `kac_ev_orta`, A–B = karamsar–iyimser, "%80 ihtimalle A–B ev"; "en az" yazılmaz — karar masası 19:13) | Canlı harita; yanında kilit grafik [kilit_yanlis_yesil.png](kilit_yanlis_yesil.png) | **Dolu trafoya "yer var": bugünkü %40 kuralı 46 dolu trafonun 24'üne, biz hiçbirine** (yanlış yeşil: biz 0/60) [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`] — gösterim. Kilit grafik PNG hâlâ eski şehirlerden (11–20): 1.5 ile yeniden üretilecek, **BEKLİYOR** | 1 dk |
| **6 Pilot** | "Harita için Kıb-Tek'ten yeni veri istemiyoruz: abone sayısı ve fatura toplamı zaten elinde. Pilotta ilk ölçeceğimiz şey trafonun çıkış gerilimi; o tek ölçüm 'dolu' dediğimiz trafolardaki yanılmayı %27'den %19'a indirir." (karar masası 20:47) | Takvim + cihaz | **Ada geneli için 120–170 trafo** [Hesap: araştırma günlüğü §7; İngiltere'de ölçülen pay %2,6]; cümledeki %27 → %19 [Hesap: bilginin değeri denemesi, farazi şehir 11–20, kusursuz bilgi üst sınırı; docs/log/2026-10-31-volkan-faz3.md] | 30 sn |

## Ekran 4: dört basamak (ekranda kısa, konuşmada açılır)

Hepsi "hiç model kullanmadan yapılan basit hesaba göre ne kadar iyi" diye anlatılır.

1. **Farazi Kıbrıs şehri** (cevabını bildiğimiz deney; gösterim, üst sınır).
   - Faturayla öğlen yükü hatası ortanca %11,3, en kötü onda birlik dilimde %28 [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`].
   - Cümle: "Deneme şehrinde hata, gerçek veride (İspanya) gördüğümüzle aynı seviyede." (Eski 11–20 kıyası %3,8 / %20,6 kullanılmaz; üretici 1.5'te faturasız koşu yok.)
2. **İspanya** (manşet): %25 → %10, gerçek veri. Cümle (karar masası 22:21): "Kıb-Tek'in zaten elindeki fatura toplamı girince gerçek trafolarda hata %25'ten %10'a iniyor; biz bunun üstüne ne kadar emin olduğumuzu ve panelin sığıp sığmadığını söylüyoruz." "Modelimiz indirdi" denmez (%10 faturanın değeri). Parantez: "(aralığımız İspanya'da %82,1 tutuyor)" [gerçek veri, İspanya 28 trafo; docs/log/2026-11-01-volkan-faz7-kalibrasyon.md].
3. **İngiltere** (gerilim): "6 gerçek hattın 5'inde ölçülen yükselme hesabın güvenli sınırının altında; birinde küçük gördük → canlıda yeşil önce pilotla sınanır" [Hesap: PR #11 + docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md; UKPN, CC BY] (karar masası 18:46, ADR-0011).
4. **Kıbrıs pilotu**: doğruluğu pilot söyler.

## Ekran 5: sayının dili (karar masası 19:13)
- Manşet orta sayı: "yaklaşık 4 ev"; yanında bant "(2–7)", açılımı "%80 ihtimalle 2–7 ev" [Yorum: örnek değer, rakam değil]. "En az … ev" hiçbir yerde yazılmaz: bandın alt ucu taban değil, gerçek trafoların ~%10–15'inde altına düşer.
- Vaat renkte: yeşilde "ilk 2 başvuru güvenle sığar (≥ %98)"; sarıda "önce ölç"; kırmızıda "ölç ya da güçlendir". Sarı ve kırmızıda sayı yalnız bant.

## Ekran 5: kilit cümle
"Dolu trafoya 'yer var' demek en pahalı hata. Bugünkü %40 kuralı 46 dolu trafonun 24'üne 'yer var' diyor. Bizim 60 yeşilimizin hiçbiri dolu değil." [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`]; gösterim

Grafik dosyası (kilit_yanlis_yesil.png) eski şehirlerden (0/87 ↔ 41/284, sınav 11–20); üretici 1.5 şehirleriyle yeniden üretilecek — **BEKLİYOR**.

## Ekran 5: söylenecek bedel
Rakamlar [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`]; gösterim. Eski 11–20 rakamları (yeşil %25, sarı %62, kırmızıların %27'si, 87 yeşil, 0/21) kullanılmaz.
- Yeşil az ve bu bilerek: ölçülmeyen 280 trafonun 60'ı yeşil, hiçbiri gerçekte dolu değil. — **0/60**
- Trafoların çoğunda emin değiliz: karar başvuru gelince verilir ya da önce ölçülür. — **renksiz %76**
- "Büyük olasılıkla dolu" uyarısı ret değil, "ölç ya da güçlendir": 22 uyarının 15'i gerçekten dolu. — **15/22 (%68)**
- Kaç ev hatası üretici 1.5 şehirlerinde raporlanmadı (eski 11–20: 2 ev) — **BEKLİYOR**, eski rakam kullanılmaz

## PDF yedeği
Aynı 7 ekran, her biri bir sayfa: cümle + görselin ekran görüntüsü + rakam ve etiketi. Ekran görüntüleri Civan'ın uygulamasından (Faz 4); son sayfa kaynaklar ([slaytlar.md](slaytlar.md) "Kaynak slaydı").
