# 2026-11-01 — Yük haritası: Kıb-Tek tepe verisi modele nasıl girer (Muhittin 4 madde 3)

**Amaç:** BAŞLA 00:16 madde 3: Kıb-Tek'ten tepe verisi gelince (istek metni madde 7–10) modele girişi: trafo maksimum talep kaydı → o trafo ölçülü sayılır, tahmin kayda çöker, popülasyon öncülü güncellenir (tüzük m. 4); OG fider tepesi → aşağıdan yukarı toplamla mutabakat; giriş biçimi + gerçeğe yakın sahte örnek; Faz 9 veri partisi kartı. BUILD 1 (yük).

## Ne yapıldı
- **Giriş biçimi:** sözleşme §8 adayı, `kibtek_tepe.csv` (kaynak `md_kaydi` / `etut` / `akilli_sayac`, `tepe_kw` ya da `tepe_a`, `zaman`) ve `kibtek_fider.csv` (fider, trafo listesi, tepe, zaman). `tepe.csv`'ye `tepe_kaynagi`.
- **Sahte kayıt** (`src/sahte_tepe_kaydi.py`, hepsi [Yorum]; Kıb-Tek'in kayıt türü ve doğruluğu BULAMADIM): MD göstergesi yer tipi trafoların %60'ında, direk tipinin %10'unda; değer = yaz penceresinin gerçek tepesi × (1 + N(0; %5)); kayıtların %10'u eski / sıfırlanmamış × U(0,70; 0,95). MD'si olmayanların %15'inde yaz etüdü: yaz haftasının rastgele bir akşamında (20–23) tek okuma, zamanıyla, hata %8. Trafolar konuma göre 5 fidere; fider tepesi = üyelerin net yük toplamının en yükseği × 1,03 (kayıp) × (1 + N(0; %2)), zamanıyla.
- **Model** (`tepe.py` madde 5): kaydın R'si = kayıt ÷ önselin aynı andaki değeri (MD: zamansız, önselin yaz tepesi; etüt: o günün sıcaklığı ve ışınımıyla o an). Kayıtlı trafo kendi R'sini alır (`olculdu` = 1). MD bandı (−0,10; +0,36): üst yan eski kaydın en kötü hâlini kapsar (KARAR 23:47 ilkesi: kalite ölçülmeden en kötü kayıt hatası). Etüt tek okuma: merkezi taşır, bandı daraltmaz.
- **Fider mutabakatı:** fider başına kayıt ÷ aşağıdan yukarı tahmin (aynı andaki trafo tahminlerinin toplamı × 1,03), `tepe_ozet.json`'da; kontrol.

## Denenen ve bırakılan iki yol [Hesap; şehir 1–10, üretici 1.4, sahte kayıt, farazi]
| Kayıtsız kalan 190 trafo | Hata ortanca | P90 | Sapma | %80 kapsama | Gerçek P90 üstü |
|---|---|---|---|---|---|
| Kayıt yok | %6,0 | %15,1 | +%2,7 | %98,9 | %0 |
| Popülasyon R'si yaz kayıtlarından (hepsi) | %5,7 | %14,5 | −%3,9 | %100 | %0 |
| Popülasyon R'si yalnız MD'den | %6,3 | %14,5 | −%4,1 | %100 | %0 |
| Popülasyon R'si montaj tipi içinde MD'den | %6,1 | %14,8 | −%2,0 | %100 | %0 |
| Fider oranıyla yukarıdan aşağı düzeltme | %13,2 | %32,8 | −%5,6 | %86,3 | %1,6 |

- **Kayıtlardan popülasyona doğrudan aktarım tahmini aşağı (güvensiz yöne) kaydırıyor.** MD göstergesi çoğunlukla büyük yer tipi trafoda; büyük trafonun tepe ÷ önsel oranı küçük trafonunkinden düşük, eski kayıtlar da aşağı çekiyor. Kayıtlar temsilî bir örnek değil (tabakalı ölçülü küme öyle). **Karar:** popülasyon R'si ve bant tabakalı ölçülülerden kalır; kayıtlardan çıkan R ve bant `yeniden_fit_onerisi` olarak yazılır, sürümlü yeniden-fit (tüzük m. 4) KARAR'da. Eşzamanlılık (B-Y2, abone sayısına bağlı R) gelince aktarım yeniden denenir.
- **Fider oranıyla düzeltme hatayı iki katına çıkarıyor:** fider oranı fider içindeki dağılımı bilmiyor; büyük bir trafonun hatası küçüklere yayılıyor. Varsayılan kapalı (`--fider-duzelt`).

## Sonuç (bu sürüm) [Hesap; farazi, gösterim]
| | Şehir 1–10 | Sınav 21–30 (bir kez) |
|---|---|---|
| MD kaydı olan trafo: n, hata ortanca / P90, gerçek P90 üstü | 83; %3,7 / %12,1; %0 | 77; %3,3 / %9,7; %0 |
| Etüdü olan trafo: n, hata ortanca / P90, gerçek P90 üstü | 46; %11,2 / %38,8; %0 | 45; %13,1 / %41,5; %2,2 |
| Kayıtsız trafolar | kayıtsız koşuyla birebir (17 sütun, 10/10 şehir) | birebir: %5,0 / %15,3, kapsama %99 |
| Fider kayıt ÷ tahmin (50 fider): ortanca, P10, P90; \|ln\| > 0,15 | 1,00; 0,91; 1,14; 7 | 1,00; 0,92; 1,17; 9 |

- MD kaydı olan trafoda tepe hatası %10–15'ten %3–4'e iniyor: kaydın değeri, Muhittin'in "tahminden ölçüme" dediği.
- Fider mutabakatı aşağıdan yukarı toplamı ortanca birebir buluyor; sapan fiderler (|ln| > 0,15) eşleşme ya da kayıp kontrolüne aday. Gerçek veride satış argümanı: "trafo trafo toplamımız Kıb-Tek'in kendi fider ölçümünü ±%15 içinde tutuyor" (gerçekte ölçülmedi).

## Kalan
1. Popülasyon R'sinin kayıtlarla güncellenmesi temsil yanlılığını düzeltmeden yapılamıyor: montaj tipi ya da abone sayısı ile tabakalı yeniden-fit (B-Y2 eşzamanlılığıyla birlikte).
2. Kıb-Tek'in MD kaydı türü, sıfırlama düzeni ve doğruluğu BULAMADIM: uzmana soru; sahte kusur oranları [Yorum].
3. Fider eşleşmesi (hangi trafo hangi fiderde) Kıb-Tek'ten; sahtede konumdan.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas ~01:15 | tepe.py + kayıt, popülasyon kayıtlardan | 1–10 | yaz kayıtları popülasyon R'sini iyileştirir | sapma +%2,7 → −%3,9 / −%4,1 / −%2,0 | aktarma; öneri olarak yaz |
| 1 Kas ~01:20 | tepe.py + fider düzeltmesi | 1–10 | yukarıdan aşağı oran ölçülmeyeni düzeltir | hata %6,0 → %13,2 | kapalı; yalnız kontrol |
| 1 Kas ~01:25 | tepe.py + kayıt (kendi trafosu) | 1–10, 21–30 bir kez | kayıtlı trafo kayda çöker, öbürleri değişmez | MD %3,3–3,7, P90 üstü 0; kayıtsızlar birebir | PR |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
