# 2026-11-01 — Gece prizi: ticari grubunu ikiye bölmek (olumsuz sonuç) ve ölçüm sırası sınavı 41–50 (BUILD 2 — panel)

**Amaç:** TEST'in PR #35 sonrası önerisi (karar masası 03:0x, Volkan "evet"): gece prizinin beklenen ↔ gerçekleşen farkının çoğu ticari grubunda (31–40: 13,0 → 9); TEST'e göre çarşı ve yurt trafolarının gece hatası farklı. Ticari grubunu ikiye böl. **Tüzük notu (karar masası):** fikir 31–40'taki yurt farkına bakarak çıktı; gerekçe, grup sınırı ve sabitler yalnız 1–10'dan; 31–40 sonucu bu betik için **gece prizine üçüncü bakış, görülmüş**; gece kalibrasyonunda bir değişiklik daha olursa sınav yeni şehirlerde (41–50).

## Yöntem
- **1–10'daki gerekçe:** gece prizinde ticari grubunun büyük abonelilerinde (yurt benzeri) beklenen 7,2 → gerçekleşen 5 (PR #35 çıktısı, 1–10).
- **Ayırıcı:** TEST'in önerdiği "en büyük enerjili sınıf" (ticari I ↔ ticari II) ayırmıyor: ticari II'nin abone başına yıllık tüketimi büyük olduğu için (Kıb-Tek 2023: ~343 ↔ ~10 MWh) çarşıda da yurtta da baskın sınıf ticari II; "ticari I baskın" grup 1–10'da boş. Kıb-Tek'in bildiği ayırıcı **küçük dükkân (ticari I) abone sayısı**: 1–10'da çarşılarda 15–39, yurtlarda 2–8 [Hesap; cevap anahtarı yalnız eşik seçerken bakıldı]. Eşik `TICARI1_ESIK = 12` (aranın ortası): **ticari dükkân** (≥ 12) ve **ticari büyük** (< 12). Farazi şehirde ayrım keskin (üretici türleri böyle kuruyor); gerçekte bu kadar keskin olmayabilir [Yorum].
- `GECE_HATA_GRUP` 1–10'dan yeniden: ticari dükkân ortanca −1,06 V (n 41), ticari büyük −0,93 V (n 48) (ortak ticari −1,01 idi); diğer gruplar aynı.

## Sonuç [Hesap; farazi şehir, gösterim]; parantezde ortak ticari (PR #35)
| | 1–10 | 31–40 (üçüncü bakış, görülmüş) |
|---|---|---|
| Hepsine gece prizi: yeşil (yanlış) / ev | 15 (0) / 182 (aynı) | 10 (0) / 72 (aynı) |
| İlk 20: yeşil / ev | 16 / 198 (17 / 202) | 9 / 76 (aynı) |
| Gece beklenen → gerçekleşen, hepsi | 15,6 → 15 (15,4 → 15) | 16,1 → 10 (16,0 → 10) |
| Ticari büyük (yurt benzeri) | 7,5 → 5 | 7,1 → 4 (1,7 standart sapma) |
| Ticari dükkân (çarşı benzeri) | 4,8 → 6 | 6,0 → 5 |

Yanlış yeşil her satırda 0; kademe ve öğlen yükü değişmedi.

## Bulgular
1. **Bölme sonucu değiştirmedi** (olumsuz sonuç): gece prizinin açtığı trafo ve ev iki şehir grubunda da aynı; beklenen ↔ gerçekleşen farkı aynı (31–40: 16,1 → 10).
2. **Yurttaki fark gece hatasının ortancasından gelmiyor:** ortanca −1,01 → −0,93 V'a gelince beklenen yeşil biraz arttı, gerçekleşen değişmedi. Olası sebep [Yorum]: ölçüm öncesi varsayımsal sonuç bara öncülünü her trafoda U(244, 252) alıyor; yüksek baralı trafoda (TEST: renksiz yurtların gerçek bara ortancası 249,0 V) gece ölçümünden sonra da yeşil çıkmıyor. Bu, öncülün trafoya göre değişmemesinden; gece kalibrasyonuyla düzelmez.
3. Öneri: bu bölme birleşmesin (kazanç yok, bir eşik ekliyor); günlük olumsuz sonuç olarak kalsın. Karar masasında.

## Ek: ölçüm sırası sınavı hiç bakılmamış şehirlerde, 41–50 (karar masası 03:1x)
Karar masası: bölme + yeni sınav şehirleri; 31–40 bu betik için artık bilgi. Üretici 1.5 şehirleri 41–50 sıfırdan üretildi (main'in üreticisi; `sablon.py`, `kac_ev_olasilik.py` ADR-0019 koduyla); renksiz (aday evi olan) 266 trafo. İki sürüm de bu şehirlere bakılmadan sabitlenmişti, **bir kez** koşuldu (~08:44):

| 41–50, renksiz 266, ölçüm sonrası | Bölmeli (bu PR): yeşil (yanlış) / ev | Bölmesiz (main, PR #35): yeşil (yanlış) / ev |
|---|---|---|
| Hepsine gece prizi | 16 (0) / 150 | 16 (0) / 151 |
| Hepsine öğlen yükü | 4 (0) / 47 (+2 bayrak, ikisi dolu) | aynı |
| Hepsine kademe fotoğrafı | 11 (0) / 104 | aynı |
| Kendi en iyi ölçümü | 15 (0) / 142 | 15 (0) / 143 |
| **İlk 20** | **11 (0) / 132** | 11 (0) / 133 |
| Rastgele 20 (ortalama) | 1,1 / 10,7 | 1,1 / 10,8 |
| Beklenen → gerçekleşen yeşil: gece / kademe / öğlen yükü | **15,9 → 16 / 12,9 → 11 / 4,5 → 4** | 15,8 → 16 / 12,9 → 11 / 4,5 → 4 |

**Bulgular (ek):**
4. **Yeni şehirlerde ölçüm öncesi değer tutuyor:** gece prizi 15,9 → 16 (z 0,05), kademe 12,9 → 11 (z −0,85), öğlen yükü 4,5 → 4. 31–40'taki gece iyimserliği (16,0 → 10) o şehirlere özgü görünüyor [Yorum].
5. **Bölme yeni şehirlerde de bir şey katmıyor** (150 ↔ 151 ev): kod main'in hâline geri alındı; bu PR yalnız günlük ve ROADMAP notu. Bölme gerekirse ab41db3.
6. **Ölçüm sırası sınavı artık 41–50:** ilk 20 trafo 132 ev, rastgele 20'nin ~12 katı; yanlış yeşil her satırda 0. Bu şehirlerde gece prizi kademeden fazla ev açıyor (150 ↔ 104; 31–40'ta tersiydi, 43 ↔ 100): tek bir "önce bu ölçüm" kuralı yerine trafo başına en iyi ölçüm (ilk 20 listesi) kullanılmalı [Yorum].

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas ~08:33 | ölçüm sırası v1.4: ticari dükkân / büyük (ticari I ≥ 12) | 1–10 (1.5) | yurtta beklenen ↔ gerçekleşen farkı kapanır | değişmedi (7,5 → 5; gece 15 / 182) | 31–40 bir kez (karar masası) |
| 1 Kas ~08:38 | aynı | 31–40 (1.5; gece için üçüncü bakış) | aynı | değişmedi (gece 10 / 72; 16,1 → 10; ticari büyük 7,1 → 4) | olumsuz; birleşmemesi önerildi |
| 1 Kas ~08:44 | bölmeli (v1.4) ve bölmesiz (main) | 41–50 (1.5, hiç bakılmamış) | yeni şehirde beklenen değer tutar; bölme fark yaratır | beklenen tutuyor (gece 15,9 → 16); bölme fark yaratmıyor (150 ↔ 151 ev); ilk 20 → 11 / 132; yanlış yeşil 0 | kod geri alındı; sınav 41–50 |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
