# 2026-11-01 — Ölçüm sırası ve konum payı ADR-0019 sonrası (BUILD 2 — panel)

**Amaç:** Karar masası 02:0x / 02:3x: ADR-0019 yürürlükte (yeşil ve "hemen evet" kapısında güven şartı yok). İki deneme betiği güven şartını kendi kuralında kullanıyordu: `olcum_sirasi.py` (PR #30; renksiz trafoyu yeşile çeviren ölçüm) ve `kac_ev_olasilik.konum_payi` (PR #28, analiz). Yeni kurala çevir, üretici 1.5 şehirleri 1–10'da kur, dokunulmamış 31–40'ta bir kez; ROADMAP Faz 10.

## Yöntem
- `olcum_sirasi.uc()`: yeşil = ilk iki başvuru ≥ %98 (güven şartı `kac_ev_olasilik.YESIL_GUVEN_SARTI`'ye bağlı; şimdi yok). `konum_payi()`: güven kapısı aynı sabite bağlandı.
- `GECE_HATA_Q` üretici 1.5 şehirleri 1–10'dan yeniden (400 trafo): ortanca **−1,16 V**, P10–P90 −2,79 … −0,53 V (1.3'te −1,64 V idi).
- `kac_ev.csv` 1.5 şehirlerinde main'in koduyla (ADR-0019) yeniden: renksiz (aday evi olan) 1–10'da 274, 31–40'ta 265 (eski kural ve 1.3 şehirlerinde 314 / 306).
- Diğer her şey PR #30 / #28 ile aynı (gece / kademe sonrası bayrak yok; ölçüm öncesi 8 varsayımsal sonuç; gerçek ağda doğrulama). Platform BUILD 2 klasörü, Mac, Python 3.12.13.

## Sonuç [Hesap; farazi şehir, gösterim]
**Ölçüm sırası** (renksiz trafo, ölçüm sonrası gerçek sonuçla):

| Seçim | 1–10: yeşile dönen (yanlış) / açılan ev | **31–40 (bir kez): yeşile dönen (yanlış) / açılan ev** |
|---|---|---|
| Hepsine gece prizi | 12 (0) / 142 | 7 (0) / 43 |
| Hepsine öğlen yükü | 10 (0) / 70 | 2 (0) / 12 (+1 bayrak, dolu değil) |
| Hepsine kademe fotoğrafı | 16 (0) / 163 | **13 (0) / 100** |
| Kendi en iyi ölçümü (beklenen) | 22 (0) / 211 | 10 (0) / 71 |
| **İlk 20** (beklenen değere göre) | 14 (0) / 173 | **8 (0) / 64** |
| Rastgele 20 (ortalama) | 1,6 / 15,4 | 0,8 / 5,4 |

Beklenen ↔ gerçekleşen (yeşile dönen, bütün renksiz trafolar toplamı):

| | 1–10 | 31–40 |
|---|---|---|
| Gece prizi | 14,2 → 12 | **15,6 → 7** |
| Öğlen yükü | 8,0 → 10 | 4,4 → 2 |
| Kademe | 13,1 → 16 | 14,2 → 13 |

**Konum payı** (analiz, `guvenli_uc.py --konum`): renksiz trafoda pay > 0 — 1–10'da 41 trafo (eski kuralla 18), adayların %2,0'ı (157/8.019); **31–40'ta 40/276 trafo, %2,0 (159/7.768)**; yanlış evet 0/157 ve **0/159**. Yeşil trafolarda 78–80 trafo; hepsinde yanlış evet 0 (31–40: 0/312).

## Bulgular
1. **Güven şartı kalkınca öğlen yükü ölçümü değerini kaybetti:** eski kuralda renksizi açan tek ölçümdü (21–30: 31 trafo / 175 ev), çünkü trafoyu "güveni yüksek" yapıyordu. Şimdi 31–40'ta 2 trafo / 12 ev. Renksiz trafoyu artık **barayı daraltan** ölçümler açıyor: kademe fotoğrafı 13 / 100, gece prizi 7 / 43.
2. **Yanlış yeşil her satırda 0** (kapı tutuyor; örnek küçük: en çok 22 yeşile dönen).
3. **Sıralama hâlâ rastgeleden iyi** (ilk 20: 64 ↔ 5,4 ev) ama 31–40'ta "her trafoya kendi en iyi ölçümü" (71 ev) "hepsine kademe"den (100) kötü: **gece prizinin ölçüm öncesi değeri sınavda iyimser** (beklenen 15,6 yeşil → 7). Kademe tutarlı (14,2 → 13). Sebep bulunmadı: gece hatası 31–40'ta benzer dağılıyor (ortanca −1,03 ↔ −1,16 V; renksizde −0,97 V), fark güvenli yönde (bara biraz yüksek tahmin, yeşil az). [Yorum] Pilot için öneri: önce kademe fotoğrafı (ucuz, tahmini tutarlı), gece prizi ikinci.
4. **Konum payı renksizde yine az bilgi veriyor** ama iki katına çıktı (renksiz trafoların %15'i, adayların %2'si); yanlış evet 0. ROADMAP Faz 9'daki "renksizde bilgi vermiyor" sonucu değişmedi; harita kartı ve sütun kararı (karar masası 01:01) aynı kalır [Yorum].

## Ne kaldı
- Gece prizinin ölçüm öncesi iyimserliğinin sebebi (şehir başına gece yükü farkı mı, örnek mi) aranmadı.
- Ölçümlerin maliyeti tartılmadı; iki ölçüm birlikte (kademe + gece) ölçülmedi.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas ~02:28 | ölçüm sırası v1.2 (ADR-0019), `GECE_HATA_Q` 1.5'ten | 1–10 (1.5) | güven şartı kalkınca sıra değişir, yanlış yeşil 0 | kademe 16 / 163, gece 12 / 142, öğlen yükü 10 / 70; ilk 20 → 14 / 173; konum payı renksiz 41 trafo, 0/157 | 31–40 bir kez |
| 1 Kas ~02:33 | aynı | 31–40 (1.5) | aynı | kademe 13 / 100, gece 7 / 43, öğlen yükü 2 / 12; ilk 20 → 8 / 64 (rastgele 5,4); gece beklenen 15,6 → 7; konum payı 40 trafo, 0/159 | PR, karar masasına |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
