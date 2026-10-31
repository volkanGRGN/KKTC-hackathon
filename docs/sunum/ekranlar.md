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
| **5 Canlı harita** | "Bir kutuya tıklayın: yaklaşık N ev daha sığar (A–B); yeşilse ilk 2 başvuru güvenle. Bugünkü kural ne diyor, yanında." (N = `kac_ev_orta`, A–B = karamsar–iyimser, "%80 ihtimalle A–B ev"; "en az" yazılmaz — karar masası 19:13) | Canlı harita; yanında kilit grafik [kilit_yanlis_yesil.png](kilit_yanlis_yesil.png) | **Dolu trafoya "yer var": bugünkü %40 kuralı 41/284, biz 0/21** [Hesap: sınav şehirleri 11–20, `sinav.py faz3`] — gösterim; #15 birleşince olasılıklı hesapla yenilenir (BEKLİYOR) | 1 dk |
| **6 Pilot** | "Baharda birkaç düzine trafoyu ölçelim; ilk ölçeceğimiz şey trafonun çıkış gerilimi. Kıb-Tek'ten yeni veri istemiyoruz: abone sayısı ve fatura toplamı zaten elinde." | Takvim + cihaz | **Ada geneli için 120–170 trafo** [Hesap: araştırma günlüğü §7; İngiltere'de ölçülen pay %2,6] | 30 sn |

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

## Ekran 5: söylenecek bedel
Faz 3 hesabı olasılıklıya geçti (ADR-0011, PR #15). Rakamlar **BEKLİYOR**: #15 birleşince Can'ın `sinav.py faz3` koşumundan gelir; aşağıdaki eski rakamlar (tek denklem) o zamana kadar kullanılmaz. Karar masasının beklediği (BUILD'in bir kezlik ölçümü, resmi değil): yeşil %25, sarı %62, kırmızıların %27'sinde yer var; kilit grafik biz 0/87 ↔ %40 kuralı 41/284.
- Yeşil az: konut trafolarında ölçmeden "evet" demiyoruz. — BEKLİYOR (eski: %6)
- Trafoların çoğu sarı, yani "önce ölç". — BEKLİYOR (eski: %63)
- Kırmızıların bir kısmında gerçekte yer var: kırmızı "ret" değil, "ölç ya da güçlendir". — BEKLİYOR (eski: %42) [Hesap: sınav 11–20, `sinav.py faz3`]

## PDF yedeği
Aynı 7 ekran, her biri bir sayfa: cümle + görselin ekran görüntüsü + rakam ve etiketi. Ekran görüntüleri Civan'ın uygulamasından (Faz 4); son sayfa kaynaklar ([slaytlar.md](slaytlar.md) "Kaynak slaydı").
