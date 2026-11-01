# 2026-11-01 — Gece prizi: ticari grubunu ikiye bölmek (BUILD 2 — panel) — olumsuz sonuç

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

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas ~08:33 | ölçüm sırası v1.4: ticari dükkân / büyük (ticari I ≥ 12) | 1–10 (1.5) | yurtta beklenen ↔ gerçekleşen farkı kapanır | değişmedi (7,5 → 5; gece 15 / 182) | 31–40 bir kez (karar masası) |
| 1 Kas ~08:38 | aynı | 31–40 (1.5; gece için üçüncü bakış) | aynı | değişmedi (gece 10 / 72; 16,1 → 10; ticari büyük 7,1 → 4) | olumsuz; birleşmemesi önerildi |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
