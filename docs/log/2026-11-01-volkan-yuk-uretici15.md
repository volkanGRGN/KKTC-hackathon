# 2026-11-01 — Yük modeli üretici 1.5 şehirlerinde; sistem tepe ÷ ortalama Kıb-Tek'le

**Amaç:** KARAR 01:22: PR #27 (üretici 1.5, Can: trafo gücü yılın tepesinden, büyük abone ayrı bağlantı, hat akşam tepesine göre) birleşti. `tepe.py` (PR #24 / #26 / #29 yöntemi) 1.5 şehirlerinde: 1–10 geliştirme, 31–40 bir kez. KARAR 01:25 madde 1: deneme şehirlerinde toplam yükün tepe ÷ ortalaması ↔ Kıb-Tek 2022. BUILD 1 (yük). **Yöntem değişmedi** (ayar yapılmadı).

## Şehirler
Üretici 1.5 (main 6013342 ile birleşik kod), şehir 1–10 ve 31–40, 10'ar paralel; UYARI yok. Model kodu `yuk/aksam-gerilim` (fc1207f).

## Yılın tepesi [Hesap; farazi, gösterim; ölçülmeyen 280 trafo]
| | 1.4, 1–10 | 1.4, 21–30 | **1.5, 1–10** | **1.5, 31–40 (bir kez)** |
|---|---|---|---|---|
| Hata ortanca / P90 | %6,0 / %15,3 | %5,8 / %17,7 | %7,5 / %18,4 | %6,7 / %15,3 |
| Sapma (+ = fazla tahmin) | +%3,9 | +%2,9 | +%5,2 | +%1,4 |
| %80 bant kapsama | %98,6 | %99,3 | %97,5 | %99,6 |
| Gerçek P90'ın üstünde | %0 | %0 | %0,4 (1 otel) | %0 |
| Tepe saati ±60 dk | %42 | %45 | %42 | %48 |

- 1.5'te ölçülü küme değişiyor (seçim özellikleri `kva`, montaj, kablo, hat sayısını görüyor; Nisan tüketimi aynı), Velander ĉ 1–10'da 8 şehirde 0, ötekilerde 0,3 ve 1,45. Hata 1.4'e yakın; sapma güvenli yönde.

## Akşam gerilimi [Hesap; farazi]
| | 1.4, 21–30 | **1.5, 1–10** | **1.5, 31–40 (bir kez)** |
|---|---|---|---|
| Hata ortanca / P90 | 5,2 / 16,5 V | 3,1 / 10,3 V | 3,5 / 8,9 V |
| %80 bant kapsama | %79,3 | %88,2 | %87,9 |
| Gerçekte 207 V altı; P10 ile yakalanan | 10; 10 | 1; 1 | 2; 2 |
| "Yeterli" (P10 ≥ 207); gerçekte altında | 173; 0 | 224; 0 | 232; 0 |
| Ortancayla karar; gerçekte altında | 259; 5 | 277; 1 | 280; 2 |
| Uyarı (P10 < 207) | 107 | 56 | 48 |

- 1.5'in hat tasarımıyla (ağır yük hattında kesit, bölme; büyük abone ayrı) gerçek 207 V altı azaldı, model uyarısı yarıya indi. Karar P10'dan kalmalı: ortancayla 31–40'ta 2 yanlış "yeterli".

## Sistem tepe ÷ yıllık ortalama ↔ Kıb-Tek [Hesap]
Kıb-Tek 2022: 368 MW ÷ (1.836 GWh ÷ 8.760 h) = **1,76** [Kaynaklı: KTEMO, Kıb-Tek Yakıt Değişim Fizibilite sunumu, slayt 38; `docs/log/2026-11-01-volkan-ktemo-tarama.md`]. Şehirde ortalama = faturaların toplamı ÷ 8,76.

| Şehir 1–10 (1.5) | ortanca | aralık |
|---|---|---|
| Üretici: üç pencerenin (Nisan 14, yaz 7, kış 7 gün) 5 dk net toplamının tepesi ÷ ortalama | **1,95** | 1,84–2,13 |
| Model: trafo tahminlerinin aynı andaki toplamı (önsel × R) ÷ ortalama | **2,30** | 2,05–2,53 |
| Trafo tepelerinin düz toplamı ÷ ortalama (eşzamansız) | 2,58 | 2,27–2,70 |

- **Üretici şehri gerçek adadan ~%11 sivri, model ~%31 sivri.** Modelin farkı beklenen yönde: trafo başına tahmin bilerek yukarı (bant üstü güvenli) ve R ölçülü trafonun kendi tepesinden (ev ev dalgalanma payı dahil); şehir toplamında bu dalgalanma söner. Trafo tahminleri toplanarak fider ya da sistem tepesi bulunmaz; toplam için R'siz eşzamanlı eğri gerekir (Faz 9 fider mutabakatı bunu kayıtla sınar).
- Kıyas kaba [Yorum]: (1) ada sanayi, su pompası ve turizmi de içerir, 40 trafoluk şehir içermez; (2) Kıb-Tek'in GWh'ı üretim (kayıplar dahil), şehrin ortalaması tüketim; (3) Kıb-Tek'in enerjisi çatı panelinin kendi tüketimini görmez, fatura brüt; (4) 2022 satırının ölçüm mü tahmin mi olduğu sunumda yazmıyor. (2) ve (3) gerçek oranı tüketim tabanında biraz yükseltir; fark yine de üretici için küçük, model için büyük.
- Sonraki adım (öneri): üreticinin yıl tepesi ÷ ortalamasını Kıb-Tek'in saatlik sistem yüküyle (istek metni madde 8) çapalamak; model tarafında şehir / fider toplamı için ayrı, R'siz eşzamanlı tahmin.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas 01:28 | tepe.py (fc1207f), üretici 1.5 | 1–10 | yöntem 1.5'te de tutar | tepe %7,5 / %18,4, P90 üstü 1/280; gerilim 0 yanlış "yeterli" | değişiklik yok |
| 1 Kas 01:28 | aynı | 31–40 bir kez | aynı | tepe %6,7 / %15,3, P90 üstü 0; gerilim 2/2 yakalandı, 0 yanlış | değişiklik yok |
| 1 Kas 01:28 | sistem tepe ÷ ortalama | 1–10 | üretici ve model Kıb-Tek'in 1,76'sına yakın | üretici 1,95, model 2,30 | günlüğe; çapalama önerisi |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
