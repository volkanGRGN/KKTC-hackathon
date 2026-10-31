# 2026-11-01 — Öğlen yük güveni: etiket hatayı ayırmıyor, bant ayırıyor (KARAR 00:57 madde 5)

**Amaç:** Panel tarafında "evet" ve yeşil için öğlen yük güveni "yüksek" şartı var; trafoların ~%57'sinde güven yüksek değil. Soru (KARAR 00:57 m. 5): güven kuralı hatayı doğru sıralıyor mu; fatura ve Kıb-Tek tepe kaydı güveni meşru biçimde yükseltir mi. BUILD 1 (yük). **Yöntem değişmedi**: yalnız ölçüm; şehir 1–10 geliştirme, 21–30 ve İspanya mevcut çıktılardan bilgi (ayar yok).

## 1. Güven etiketi hatayı ayırmıyor [Hesap]
| Ölçülmeyen trafo, öğlen | yüksek | orta | düşük |
|---|---|---|---|
| Şehir 1–10: n; hata ortanca / P90 | 80; %8,5 / %22,8 | 158; %10,2 / %31,5 | 42; %15,2 / %41,0 |
| Sınav 21–30: n; hata ortanca / P90 | 76; %11,1 / %26,7 | 183; %11,1 / %28,6 | 21; %13,0 / %34,3 |
| İspanya gerçek (girdi c, tabakalı 10 + 15): satır (trafo); hata ortanca / P90 | 125 (27); **%13,9** / %31,0 | 468 (27); **%8,7** / %32,5 | 67 (22); %12,3 / %37,2 |

- 21–30'da yüksek = orta; İspanya'da sıra ters (yüksek en kötü).
- Kuralın girdisi arketip olasılığı hatayı haber vermiyor (1–10, |log hata| ile Spearman +0,05); haber verenler abone sayısı (−0,32), büyük abone varlığı (+0,28), yıllık enerji (+0,25).

## 2. Panel için güvenlik bantta: tehlikeli yanda her sınıf nominalin altında [Hesap]
"Tehlikeli yan" = gerçek öğlen yükü bandın altında (yük az → gerilim yükselmesi fazla → yanlış evet). %80 bantta nominal %10.

| Gerçek < P10 | yüksek | orta | düşük |
|---|---|---|---|
| Şehir 1–10 | %10,0 | %6,3 | %0 |
| Sınav 21–30 | %9,2 | %2,7 | %0 |
| İspanya gerçek | %2,4 | %2,1 | %6,0 |

- Orta ve düşük bantlar yüksekten daha temkinli (daha geniş); bant belirsizliği zaten taşıyor. "Güven yüksek" kapısı güvenlik eklemiyor, yalnız trafo seçiyor.

## 3. Yeşil kapısı açılırsa (karşı-olgu, mevcut `kac_ev.csv` + `tahmin.csv`; panel kodu değişmedi) [Hesap; farazi, gösterim]
Yeşil = `p_iki_ev_sigar` ≥ 0,98 ve güven ∈ kapı; aday evli trafolar. "Söz bozulan" = ilk iki başvurudan (aday tek evse o tek ev) biri sığmıyor.

| Kapı | 1–10: yeşil / yanlış yeşil / söz bozulan | 21–30: yeşil / yanlış yeşil / söz bozulan | Konut yeşili (1–10 / 21–30) |
|---|---|---|---|
| yalnız yüksek (bugün) | 20 / 0 / 0 | 17 / 0 / 0 | 1 / 0 |
| yüksek + orta | 38 / 0 / 0 | 43 / 0 / 0 | 1 / 0 |
| hepsi | 47 / 0 / 0 | 47 / 0 / 0 | 1 / 0 |

- Yanlış yeşil %95 üst sınırı 47'de %6,2 (n küçük). Yeşiller çoğunlukla çarşı ve otel (öğlen yükü büyük).
- **Konutta yeşil değişmiyor:** konut trafosunda darboğaz güven değil, gerilim fiziği ve ağ bilgisi (p_iki_ev_sigar < 0,98).
- İlk sayımımda "ilk iki sığmıyor" 5 çıkmıştı; beşinde de aday tek ev, o ev sığıyor. Tanım düzeltildi, söz bozulan 0.

## 4. Fatura ve Kıb-Tek tepe kaydı [Hesap; 1–10]
- **Fatura güveni meşru yükseltir:** faturasız model hata ortanca %28,2 (P90 %61,6), faturalı %10,0 (%32,0). Kural zaten "yüksek" için fatura istiyor.
- **Kıb-Tek tepe kaydı öğlen güvenini yükseltmez:** MD kaydı olan 58 ölçülmeyen trafoda kaydın sapması ile öğlen artığı zayıf ilişkili (Spearman +0,25); kayıtla düzeltme öğlen hatasını %12,3 → %12,7 (iç örnekte bile iyileşme yok); etütte ilişki yok (−0,02). Fatura büyüklüğü zaten veriyor; akşam kaydı öğlene yeni bilgi katmıyor.

## Öneri (BUILD 1 görüşü; karar KARAR'da, kod panel tarafında)
1. Yeşil ve başvuru anı "evet" kapısında "güven yüksek" şartı yerine bandın kendisi (kalibre: tehlikeli yanda ≤ nominal). Güven yalnız bilgi etiketi. Panelde evet payına etkisini BUILD 2 başvuru akışında ölçer (PR #22 motoru).
2. Etiket yeniden tasarlanacaksa girdisi abone sayısı, büyük abone ve fatura; arketip olasılığı çıkar (`sablon.guven`, BUILD 1; ayrı PR, 1–10'da kurulur).
3. Öğlen güvenini meşru yükselten tek şey öğlen ölçümü (ölçülü trafo) ve fatura; Kıb-Tek tepe kaydı değil.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
