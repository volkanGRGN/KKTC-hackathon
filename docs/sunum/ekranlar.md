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
| **5 Canlı harita** | "Bir kutuya tıklayın: kaç ev daha sığar, bugünkü kural ne diyor." | Canlı harita; yanında kilit grafik [kilit_yanlis_yesil.png](kilit_yanlis_yesil.png) | **Dolu trafoya "yer var": bugünkü %40 kuralı 41/284, biz 0/21** [Hesap: sınav şehirleri 11–20, `sinav.py faz3`] — gösterim | 1 dk |
| **6 Pilot** | "Baharda birkaç düzine trafoyu ölçelim; ilk ölçeceğimiz şey trafonun çıkış gerilimi. Kıb-Tek'ten yeni veri istemiyoruz: abone sayısı ve fatura toplamı zaten elinde." | Takvim + cihaz | **Ada geneli için 120–170 trafo** [Hesap: araştırma günlüğü §7; İngiltere'de ölçülen pay %2,6] | 30 sn |

## Ekran 4: dört basamak (ekranda kısa, konuşmada açılır)

Hepsi "hiç model kullanmadan yapılan basit hesaba göre ne kadar iyi" diye anlatılır.

1. **Farazi Kıbrıs şehri** (cevabını bildiğimiz deney; gösterim, üst sınır).
   - Faturayla %3,8, yalnız abone sayısıyla %20,6 ortanca hata [Hesap: sınav şehirleri 11–20, `sinav.py faz2`].
   - Cümle: "Fatura olmadan model ortalama trafoda basit hesaptan pek iyi değil; fatura girince hata dörtte bire iniyor."
2. **İspanya** (manşet): %25 → %10, gerçek veri.
3. **İngiltere** (gerilim): 6 gerçek hattın 4'ünde ölçülen yükselme ±%40 içinde; ikisinde paneller hat ucunda toplanmıştı → karamsar senaryo [Hesap: PR #11, UKPN, CC BY].
4. **Kıbrıs pilotu**: doğruluğu pilot söyler.

## Ekran 5: söylenecek bedel
- Yeşil az (%6): konut trafolarında ölçmeden "evet" demiyoruz.
- Trafoların %63'ü sarı, yani "önce ölç".
- Kırmızıların %42'sinde gerçekte yer var: kırmızı "ret" değil, "ölç ya da güçlendir" [Hesap: sınav 11–20, kırmızı kuralı `karamsar_bugun`].

## PDF yedeği
Aynı 7 ekran, her biri bir sayfa: cümle + görselin ekran görüntüsü + rakam ve etiketi. Ekran görüntüleri Civan'ın uygulamasından (Faz 4); son sayfa kaynaklar ([slaytlar.md](slaytlar.md) "Kaynak slaydı").
