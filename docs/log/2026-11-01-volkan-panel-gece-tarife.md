# 2026-11-01 — Gece prizi hatası tarife grubuna göre (BUILD 2 — panel)

**Amaç:** TEST'in PR #34 bulgusu (karar masası 02:5x, Volkan "evet"): gece prizinin ölçüm öncesi değeri sınavda iyimserdi (31–40'ta beklenen 15,6 yeşil → gerçekleşen 7); gece hatası (ölçüm − boşta gerilim) trafonun türüne göre çok farklı, `GECE_HATA_Q` ise tek havuz (ortanca −1,16 V). Hatayı gruba göre ayır; grup yalnız Kıb-Tek'in bildiğinden (cevap anahtarının trafo tipi sınavı sızdırır). Kalibrasyon yalnız 1–10, sınav 31–40 bir kez, kapı yanlış yeşil 0; beklenen ↔ gerçekleşen gece yeşili yan yana.

## Yöntem (`src/olcum_sirasi.py`)
- `tarife_grubu(tr)`: `trafolar.csv`'den tahmini enerjisi en büyük abone sınıfı (abone sayısı × sınıfın ortalama yıllık MWh'i, Kıb-Tek 2023, `kac_ev_olasilik.MWH`): su motoru → **sulama**, sanayi I / II → **sanayi**, turizm → **turizm**, ticari I / II → **ticari**, konut → en uzun hat ≥ 400 m ise **konut kırsal**, değilse **konut kısa** (400 m eşiği 1–10'da seçildi [Yorum]).
- `GECE_HATA_GRUP`: grup başına 21 nicelik, 1–10'dan (`--kalibrasyon`); 30'dan az trafolu grupta havuz grubun ortancasına kaydırılırdı (gerek olmadı: en küçük grup 34). Model ve ölçüm öncesi varsayımsal sonuç trafonun grubunun dağılımını kullanır.
- Kalibrasyon (1–10, 400 trafo) [Hesap], grup ortancası / n: sulama −3,75 V / 37, sanayi −2,06 / 34, turizm −1,31 / 42, konut kırsal −1,16 / 104, ticari −1,01 / 89, konut kısa −0,83 / 94 (havuz −1,16). TEST'in tipe göre sırasıyla aynı (sulama −3,75 … şehir konutu −0,81).
- Diğer her şey PR #34 ile aynı (ADR-0019, üretici 1.5, gece / kademe sonrası bayrak yok). Platform BUILD 2 klasörü, Mac, Python 3.12.13.

## Sonuç [Hesap; farazi şehir, gösterim]; parantezde havuz dağılımıyla (PR #34)
| Renksiz trafo, ölçüm sonrası | 1–10: yeşile dönen (yanlış) / ev | **31–40 (bir kez): yeşile dönen (yanlış) / ev** |
|---|---|---|
| Hepsine gece prizi | 15 (0) / 182 (12 / 142) | **10 (0) / 72** (7 / 43) |
| Hepsine öğlen yükü | 10 (0) / 70 (aynı) | 2 (0) / 12 (aynı) |
| Hepsine kademe fotoğrafı | 16 (0) / 163 (aynı) | 13 (0) / 100 (aynı) |
| Kendi en iyi ölçümü | 23 (0) / 232 (22 / 211) | 12 (0) / 96 (10 / 71) |
| **İlk 20** | 17 (0) / 202 (14 / 173) | **9 (0) / 76** (8 / 64) |
| Rastgele 20 (ortalama) | 1,7 / 16,9 | 0,9 / 7,2 |

**Gece prizi, beklenen ↔ gerçekleşen yeşil:**

| | 1–10 | 31–40 |
|---|---|---|
| Bütün renksiz | 15,4 → 15 (havuz 14,2 → 12) | **16,0 → 10** (havuz 15,6 → 7) |
| Ticari (n 43 / 47) | 12,0 → 11 | 13,0 → 9 |
| Turizm (n 14 / 11) | 2,0 → 2 | 3,0 → 1 |
| Konut kısa (n 94 / 85) | 1,4 → 2 | 0 → 0 |
| Konut kırsal, sulama | 0 → 0 | 0 → 0 |

## Bulgular
1. **Ayrım işe yarıyor:** gece prizi sınavda 7 → 10 trafoyu, 43 → 72 evi yeşile çeviriyor; ilk 20 trafo 64 → 76 ev. Yanlış yeşil her satırda 0.
2. **Beklenen ↔ gerçekleşen farkı daraldı ama kapanmadı:** 31–40'ta 15,6 → 7 iken 16,0 → 10; geliştirmede artık tutuyor (15,4 → 15). Kalan fark en çok ticari trafolarda (13,0 → 9; 1,6 standart sapma). Bütün renksizde 16,0 → 10, 2,3 standart sapma [Hesap: Σp(1 − p)]: rastlantı sayılamayacak kadar büyük, ölçüm öncesi değer sınavda hâlâ iyimser. Olası sebep ticari grubun içindeki çarşı / yurt farkı (TEST: −1,06 / −0,93 V) [Yorum]. Yön güvenli (yanlış yeşil yok).
3. Gecenin yeşil yapabildiği trafolar neredeyse hep ticari ve turizm (31–40: 10 yeşilin 10'u); konut ve sulamada gece prizi rengi değiştirmiyor. Pilotta priz, ticari / turizm trafolarında anlamlı [Yorum].
4. Pilot sırası değişmez: kademe fotoğrafı tutarlı ve en çok ev açan (13 / 100); priz ikinci, ticari / turizm trafolarında.

## Ne kaldı
- Ticari grubun içinde ayrım (ör. turizm ↔ ticari II payı, abone sayısı) ölçülmedi; 31–40'a bakılarak yapılmaz.
- Gerçek veride gece hatası pilotta (P6 + P7 aynı evde) ölçülmeli; buradaki gruplar farazi şehrin.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas ~08:18 | ölçüm sırası v1.3: gece hatası tarife grubuna göre | 1–10 (1.5) | gece prizinin beklenen değeri tutar, değeri artar; yanlış yeşil 0 | gece 15,4 → 15 yeşil, 182 ev; ilk 20 → 17 / 202 | 31–40 bir kez |
| 1 Kas ~08:23 | aynı | 31–40 (1.5) | aynı | gece 7 → 10 yeşil, 43 → 72 ev; beklenen 16,0 → 10; ilk 20 → 9 / 76; yanlış yeşil 0 | PR, karar masasına |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
