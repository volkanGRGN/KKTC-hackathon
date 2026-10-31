# 2026-10-31 — Volkan (+ Claude, BUILD): üretici ve sözleşme 1.2, fatura sütunu, Faz 2 yeniden ölçüm

## Hipotez / amaç
Karar masasının 31 Ekim kararları (volkan.md KARAR 13:58, 15:12, 15:29; [ADR-0007](../decisions/adr-0007-yillik-fatura-tuketimi-girdi.md), [ADR-0008](../decisions/adr-0008-farazi-cesitlilik-saf-tahmin.md)) tek pakette:
- farazi şehirler fazla düzenliydi: konut trafolarında müşteri başına öğlen yükü CV şehir içinde 0,08, gerçekte (İspanya) 0,46;
- büyük müşterili trafolarda hata, abone sayısının büyüklüğü göstermemesinden geliyordu.

Beklenti (ADR-0008): mahalle farkı eklenince "yalnız abone sayısı" modeli farazide de kötüleşir, faturalı model ayakta kalır.

Bütün rakamlar farazi şehirde: **gösterim**.

## Yaptıklarım

**Üretici `src/sehir_uret.py` sürüm 1.2:**
- **Mahalle çarpanı.**
  - Trafo başına log-normal, σ = 0,35. Küçük abonelere uygulanır: konut, ticari I, sanayi I, su motoru.
  - Büyük abonenin (otel, dükkân, sanayi II, yurt) kendi büyüklük farkı (σ = 0,3) zaten var [Yorum].
  - Trafo başına saat kayması ±30 dk, bütün abonelere.
- **`yillik_tuketim_mwh`.** Abonelerin yıllık enerjisi toplamı × fatura sapması 0,95–1,05 [Yorum].
- **Bayramlar.** KKTC resmi tatilleri `tatil` sayılıyor:
  - 2023: 21–23 Nisan;
  - 2024: 10–12 Nisan ve 23 Nisan;
  - 2025: 1 Nisan ve 23 Nisan.
  - Kaynak: Ramazan Bayramı tarihleri Diyanet takviminden (Türkiye ile aynı ay takvimi), 23 Nisan KKTC'de resmi tatil. KKTC Resmi Gazete listesini BULAMADIM. Arife yarım günü iş günü sayıldı [Yorum].
- **Kıyı.** Civan'ın `app/ornek_veri.py` `kiyi_segmentleri()` ve `karada()` fonksiyonları aynen ve atıfla kopyalandı. Kıyı dosyası KAYNAK.txt'deki komutla indirildi (25 yol, 2.141 nokta, Civan'ınkiyle aynı). Dosya yoksa eski 400 m kuralı + uyarı.
- **Faz ağırlıkları.** Tek fazlı abonenin fazı 1 ± sapma ağırlıklı: kentsel %25, kırsal %50 [Kaynaklı: UKPN 2015 kapanış raporu]. Turistik ve sanayi kentsel sayıldı [Yorum]. Önceden ±%20 [Yorum].
- **Hava yılı** 2023 / 2024 / 2025. Open-Meteo 2023 dosyası indirildi.
  - Sağlama: yatay 1.903, 30° güney 2.102 kWh/m². Nisan 11–14 ortalaması 754 W/m² (2024–25: 787 / 769).
- **Trafo çıkış gerilimi 244–252 V** (0.2'de 246–250; karar masası 16:27, PR #11: UKPN 20 trafoda siteler arası bara yayılımı ss 3,3 V, bizimki 1,2 V; merkez 248 V aynı) [Yorum, ±4 V].
- **Faz dengesizliği raporu** `ayar.json` `faz_dengesizlik_ortanca`: hat başına (en büyük faz − ortalama) ÷ ortalama, yıllık enerjiyle (UKPN tanımı akşam faz yükü). 20 şehrin ortancası %20,7 (şehir aralığı %16–29). UKPN kentsel fider ortancası %14, P84 %30 [Hesap, PR #11]: ±%25 / ±%50 çapasıyla üretici hâlâ biraz karamsar (güvenli yön).
- **`ayar.json` yeni anahtarlar:** `mahalle_sigma`, `mahalle_kayma_dk`, `faz_sapma`, `kiyi_kontrolu`, `kva_tavan_sayisi`, `bayramlar`, `veri_turu`.
- **Cevap anahtarı yeni sütunlar:** `mahalle_carpani`, `saat_kaymasi_dk`.

**Yolda verdiğim üç üretici kararı.** Hepsi kendi dosyam, ölçerek; şehir 1–10'da.
1. **σ 0,30 → 0,35.**
   - 0,30'da konut trafosu CV'si şehir içi ortanca 0,29 çıktı; hedef 0,3–0,4 (ADR-0008).
   - 0,35'te ortanca 0,33 (şehir aralığı 0,25–0,45); 1–10 havuzunda 0,37.
   - EDP'ye uydurmadım, aralığa çapaladım.
2. **Trafo gücü mahalle farkını görmez.**
   - İlk yazımda kVA mahallenin gerçek yüküne göre seçiliyordu. Gizli mahalle farkı, Kıb-Tek'in bildiği `kva` sütununa sızıyordu: faturasız modelin artığıyla log(kVA ÷ enerji) korelasyonu konut ve köyde 0,62 [Hesap].
   - İspanya gerçek verisinde şebeke bilgisi müşteri sayısına bir şey katmamıştı (PR #10). Plan artık tarife ortalamasıyla yapılıyor (sürüm 0.2'deki gibi).
   - Ama tamamen mahallesiz plan 800 trafonun 3'ünde Nisan akşamında kVA'yı aştı: en kötüsü %121, 205,7 V (sehir-001 T22 köy, çarpan 2,6). Gerçekte Kıb-Tek aşırı yüklenen trafoyu büyütür. Kural: plan = tarife ortalaması × 1,2–2,0; yılın tepesinde mahalleyle aşılıyorsa bir üst boy [Yorum].
   - Sonrası: korelasyon 0,11; Nisan tepesi kVA'yı aşan trafo 0.
3. Tüketim serileri bu iki düzeltmede değişmedi (aynı tohum, birebir). Değişen yalnız kVA ve ona bağlı gerilim / kaç ev.

**Model `src/sablon.py`:**
- **Fatura varsa** abone satırı, tarife ortalamasıyla hesaplanan enerjisi faturaya eşit olacak biçimde ölçeklenir. Sınıf karışımı abone sayısından, büyüklük faturadan. Yeni katsayı yok. `--faturasiz` kıyas için sütunu yok sayar.
- **Hata tabanı artıklardan seçiliyor** (sabit 0,05 değil). Profil olabilirlik, adaylar 0,05–5. Fatura yoksa en az 0,3.
  - Sebep: sabit tabanla, mahalle farkı olan şehirlerde çok aboneli konut trafosu en dar bandı ve "yüksek güven"i alıyor, en çok yanılan oluyordu.
  - Şehir 1–10'da faturasız "yüksek"in hata ortancası %41; "orta" %25, "düşük" %24.
- **Fatura yoksa "yüksek güven" verilmiyor.**
  - Taban 0,3 olunca da 12 ölçülünün bir-dışarıda hatası şans eseri küçük çıkan şehirde 13 trafo "yüksek" aldı; hata ortancaları %43.
  - Faturasız büyüklük ±%30 bilinmez; jüriye de böyle anlatılır.
- Sözleşme 1.2 ([tablo-bicimi.md](../data/tablo-bicimi.md)) ve [yöntem](../method/modeling.md) bölüm 0 ve 5 güncellendi.

**Ayar disiplini.** Bütün denemeler şehir 1–10'da. 11–20 en sonda bir kez ölçüldü; ölçümden sonra hiçbir şey değişmedi.

## Sonuç

### Üretici 1.2, Faz 1 ölçüleri (20 şehir, 800 trafo; Can'ın `sinav.py faz1`'i main'deki hâliyle + kıyı sayımı)

| Ölçü | 0.2 (öğlen) | 1.2 |
|---|---|---|
| Her tipten ≥ 3 / ≥ 60 | geçti, en az sanayi 73 | aynı |
| 259 V üstü | 119/800 | 123/800 |
| 207 V altı | 0 | 0 (en düşük 210,6 V; 216 V altı 5) |
| 264 V üstü | 33/800 | 46/800 |
| Denizde trafo | sehir-001'de 4/40 (Civan) | 0/800 [Hesap: `karada()`] |
| Nisan tepesi > kVA | — | 0/800 (> %80: 2) |
| `kva_tavan_sayisi` (20 şehir toplamı) | — | 28 (otel / sanayi; Nisan'da etkisiz) |
| En uzun üretim | 16,1 sn | 14,7 sn |
| Profil / ışınım | eac / open-meteo | eac / open-meteo, 20/20 |
| Konut trafosu müşteri başına öğlen CV, şehir içi ortanca | 0,08 (karar masası) | 0,33 (şehir 1–20; 1–10'da da 0,33) |
| Konut trafosu öğlen en düşük, abone başına ortanca | ~330 W | 318 W (UKPN Low Carbon London 200–400 W aralığında) |

Main'deki `sinav.py faz1` (207 V) ile 5/5 madde geçti. Bara bandı 244–252 V olunca gerilim satırları değişti, tüketim serileri ve `trafolar.csv` değişmedi (aynı tohum, birebir), dolayısıyla Faz 2 sonuçları da aynı.

### Faz 2: sütunlu / sütunsuz, saf tahmin yan yana

- Ölçülmeyen trafolar, gerçeği ≥ 1 kW, 12 ölçülü.
- Hata = |tahmin − gerçek| ÷ gerçek. Havuz: şehirlerin bütün ölçülmeyenleri (n = 280).
- Ölçen: geliştirme betiğim; resmi ölçüm Can'ın `sinav.py faz2`'si.

**Sınav şehirleri 11–20** (bir kez):

| | ortanca | P90 | kapsama | düşük güven | doğru arketip (şehir ortancası) | şehirler arası oran (şehir ortancası / en kötü) |
|---|---|---|---|---|---|---|
| **Model, faturalı** | **%3,9** | **%8,3** | %85 | %1 | %98 | 1,08 / 1,81 |
| **Model, faturasız** | **%22,2** | **%54,8** | %85 | %66 | %96 | 1,01 / 1,74 |
| Saf tahmin, ADR-0008 tanımı (Σ öğlen ÷ Σ abone × abone sayısı) | %176 | %726 | — | — | — | — |
| Saf, tarife enerjisiyle (Σ öğlen ÷ Σ enerji × enerji) | %22,9 | %81,6 | — | — | — | — |
| Saf, faturayla (Σ öğlen ÷ Σ fatura × fatura) | %5,8 | %16,0 | — | — | — | — |

**Geliştirme şehirleri 1–10** (son ayarla):

| | ortanca | P90 | kapsama | düşük güven |
|---|---|---|---|---|
| Model, faturalı | %4,0 | %9,6 | %78 | %1 |
| Model, faturasız | %24,8 | %59,5 | %68 | %61 |
| Saf, tarife enerjisiyle | %28,6–30,2 | %89–101 | — | — |
| Saf, faturayla | %7,1 | %17 | — | — |

Saf tahminlerdeki iki rakam: iki koşuda öğretici küme biraz farklı (fatura seçimdeki büyüklük özelliğini değiştiriyor).

**Şehir başına, sınav, faturalı** (Can'ın ölçütü şehir başına; sonra şehirlerin ortancası ve en kötüsü):
- Ortanca hata en kötü %5,1, P90 en kötü %9,5. Eşik %15 / %30: geçer.
- Kapsama %71–100. 3 şehir %90'ın üstünde, bant gereğinden geniş.
- Şehirler arası oran: 2 şehir 1,5'in üstünde (sehir-012 1,52, sehir-019 1,81). Payda çok küçük (şehir içi hata %3–4); iki şehirde de şehirler arası hata ortancası ~%5.

**Tip başına, sınav, faturalı** (ortanca / P90 / kapsama):

| Tip | n | Model | Saf-fatura ortanca |
|---|---|---|---|
| Şehir konutu | 107 | %3,2 / %7,7 / %82 | %6,0 |
| Köy | 35 | %3,5 / %8,2 / %86 | %3,4 |
| Çarşı | 30 | %4,3 / %8,0 / %100 | %2,3 |
| Otel | 33 | %3,9 / %8,1 / %88 | %5,9 |
| Sanayi | 21 | %4,0 / %6,0 / %95 | %8,9 |
| Sulama | 26 | %6,5 / %11,6 / %81 | %18,8 |
| Yurt | 28 | %4,2 / %9,4 / %75 | %6,2 |

İlk sürümde (PR #8, şehir 0.2) en kötüleri otel, yurt, çarşı ve sanayiydi (%21–25). Fatura bunu kapattı.

**Faturasız, tip başına (sınav):** şehir konutu %27,7 / P90 %59, köy %20,6, çarşı %26, otel %16,4, sanayi %14,8, sulama %21,5, yurt %21,4. En kötüsü artık konut: mahalle farkı abone sayısıyla görünmüyor.

### Okuma
- **ADR-0008'in beklentisi tuttu.**
  - Faturasız model farazide de İspanya gerçek verisinin seviyesine düştü: %22 / %55; İspanya ~%25 / ~%58 (PR #10).
  - Faturalı model ayakta: %3,9 / %8,3.
  - Fatura, Kıb-Tek'ten isteyeceğimiz en değerli tek veri.
- **ADR-0008 madde 1 ölçütü** (modelin ortanca ve P90'ı saf tahminden en az %25 düşük):
  - ADR'deki tanımla (Σ abone) iki koşu da kolayca geçiyor. Ama bu saf tahmin karışık şehirde anlamsız: bir otel ile bir ev aynı "1 abone".
  - Faturalı model, faturalı saf tahmine karşı: ortanca %33, P90 %48 daha düşük → **geçer**.
  - Faturasız model, tarife enerjili saf tahmine karşı: ortanca yalnız %3 (sınavda; denemede %13), P90 %33 daha düşük → **ortancada geçmez**. Fatura yoksa model, ortanca trafoda tarife ortalamasından pek iyi değil; kazancı kötü uçta (P90).
- **Farazi faturalı isabet iyimser.**
  - İspanya'da fatura girince %10–11 / P90 %32–33 çıkmıştı; burada %3,9 / %8,3.
  - Sebep üreticide: aynı tarifedeki her abone aynı EAC eğrisini taşıyor, öğlen ÷ yıllık oranı abone abone değişmiyor. Faturayı bilen model büyüklüğü neredeyse tam biliyor.
  - ADR-0008 madde 3 cümlesi ("farazi isabet gerçek isabetin üst sınırı") bunu karşılıyor.
- **Faturasız güven etiketi bilgi taşımıyor.**
  - Sınavda "orta" %20, "düşük" %22; trafoların %66'sı "düşük".
  - Dürüst sonuç: fatura yoksa büyüklük her trafoda ±%30 belirsiz.
- **Fatura sütunu brüt tüketim** (ADR-0007'nin tarifi). Mahsuplaşmalı panelli evin faturası net olabilir, o zaman fatura panelli trafoda düşük kalır. Kıb-Tek'in içeri alınan enerjiyi ayrı bilip bilmediğini BULAMADIM. Karar masasına yazdım.

## Karar / sıradaki adım
- PR: sözleşme 1.2 + üretici 1.2 + model; PR #8'in üstüne. Can ya da Civan onayı.
- Can:
  - `sinav.py faz2` resmi ölçüm (saf tahmin satırı);
  - CV bilgi satırı (ADR-0008 madde 2, 4).
  - Yeni şehirler: `python3 src/sehir_uret.py 1 20` sonra `python3 src/sablon.py data/synthetic`. Kıyı ve 2023 dosyası KAYNAK.txt komutlarıyla.
- Civan: haritada `yillik_tuketim_mwh` (sahte üreticiye), 800–899 etiketi.
- Karar masasına (volkan.md):
  1. Saf tahminin tanımı: Σ abone yerine tarife enerjisi; faturalıda saf-fatura.
  2. Panelli evde fatura brüt mü net mi.
  3. Farazi faturalı isabeti gerçekçi kılmak için abone başına eğri farkı (aynı tarifede öğlen ÷ yıllık oranının abone abone değişmesi): sürüm 1.3 adayı.

## Ek girdi — 31 Ekim 17:30: karar masasının üç cevabı (KARAR 17:26)

1. **Saf tahmin tanımı.** Saf tahmin, modelin bildiği bilgiyle kuruluyor:
   - faturasızda Σ öğlen ÷ Σ tarife enerjisi × trafonun tarife enerjisi;
   - faturalıda Σ öğlen ÷ Σ fatura × fatura.

   ADR-0008'in "Σ abone" tanımının yerine geçiyor; ADR dosyası düzenlenmedi.
   - Sonuç: faturalı model geçiyor (ortanca %33, P90 %48 daha iyi).
   - Faturasız model **ortancada geçmiyor** (%3); kazancı kötü uçta (P90 %33).
   - `sablon.py` artık `sablon_ozet.json`'a iki saf tahmini de yazıyor: oran ve ölçülülerde bir-dışarıda hatası, modelinkiyle yan yana. Örnek sehir-012: model %4,2 / %10,9; saf tarife %16,5 / %40,7; saf fatura %6,0 / %16,1.
   - Resmi kıyas Can'ın `sinav.py faz2`'si (PR #14). Can'ın ölçümü: saf tarife %25,2 / %67,2, saf fatura %5,5 / %15,2.
2. **Panelli evin faturası: bu sürümde iyimser.**
   - Sürüm 1.2 brüt tüketimi yazıyor. Gerçekte mahsuplaşmada fatura net: evin kendi tükettiği panel üretimi sayaçtan hiç geçmez. Bu yüzden brüt tüketimi Kıb-Tek de bilemez [Yorum].
   - Sonuç: panelli trafolarda faturalı isabet iyimser.
   - Üretici 1.3'te panelli evin faturası net yazılacak, model `panel_kw` × yıllık üretimle düzeltecek.
   - Uzmana soru 7 (01-plan): çekilen ve verilen enerji ayrı kayıtlı mı?
3. **Farazi faturalı isabet bir üst sınır.** Farazide %3,9, İspanya gerçek verisinde faturayla %10. Abone başına eğri farkı üretici 1.3'e (ADR-0009, trafo içi çeşitlilik).

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
