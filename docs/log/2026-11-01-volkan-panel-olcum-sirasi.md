# 2026-11-01 — Faz 10 ölçüm sırası: renksiz trafoya hangi tek ucuz ölçüm (BUILD 2 — panel)

**Amaç:** Karar masası 01:01: her renksiz trafo (ADR-0017 `pv_uc` = `bos`) için hangi tek ucuz ölçüm onu yeşile ya da "büyük olasılıkla dolu" bayrağına en çok taşır — akıllı prizle gece bara seviyesi, trafo başında bir haftalık öğlen yükü, plaka / kademe fotoğrafı (`bilgi_degeri.py` üstüne). Çıktı: pilot için "ilk 20 trafo" listesi ve her ölçümün açtığı ev sayısı; yanlış yeşil kapısı her satırda.

## Yöntem (`src/olcum_sirasi.py`)
- **Ölçümlerin gerçek tarafı** (benzetimin kendi dosyalarından; model yalnız sonucu görür):
  - **gece** (akıllı priz, 00:00–05:00): trafodaki bir evin gece gerilimi, 14 gecenin ortancası; evin yeri bilinmez, `yuk_5dk.csv`'nin o adımdaki en düşük ve en yüksek ev gerilimi arasında trafoya özgü sabit bir yer [Yorum]. Model: bara = ölçüm − hata, hata 1–10'da ölçülen dağılımdan (`GECE_HATA_Q`, 400 trafo): **ortanca −1,64 V, P10–P90 −4,31 … −0,64 V**, hep aşağı (gece evler yük çekiyor; inverterin sabah değerinden kötü, o −0,79 V idi).
  - **yuk** (trafo başında bir hafta): ilk 7 günün 11:00–14:00 tüketiminin en düşüğü; trafo ölçülü sayılır (`sablon.py` kuralı: öğlen yükü = ölçülen, güven yüksek). Gerçekte trafo başı net yükü ölçer; brüt tüketime panel gücüyle çevrilir [Yorum].
  - **kademe** (plaka / kademe fotoğrafı): trafonun kendi kademesi (boşta gerilime en yakın, 5 pozisyon); bara bu kademenin ±3,125 V penceresinde (başvuru motorunun kademe kaydı gibi), fotoğraf doğru sayılır.
- **Renk** resmi kuralla: yeşil = ilk iki başvuru ≥ %98 sığar ve güven yüksek; bayrak = bugün aşma olasılığı ≥ 0,7; açılan ev = yeşile dönerse karamsar kaç ev (çekilişlerin P10'u). Çekilişler resmi akışla, bilgi ayrı akıştan: bilgisiz koşum `kac_ev.csv` ile birebir (12 trafoda sınandı).
- **Ölçüm öncesi değer** (sıralama, cevap anahtarına bakmadan): her ölçüm için modelin öncülünden 8 varsayımsal sonuç (bara U(244, 252) + gece hatası; öğlen yükü Faz 2 bandından; kademe baradan); beklenen yeşile dönme / bayrak / açılan ev. Trafonun en iyi ölçümü = beklenen açılan ev en büyük (eşitlikte bayrak olasılığı). **İlk 20** = beklenen değere göre en üstteki 20 trafo.
- **Ölçüm sonrası** (doğrulama, cevap anahtarıyla): gerçek sonuçla renk; yanlış yeşil, bayrak isabeti, gerçekleşen açılan ev. Kıyas: rastgele 20 renksiz trafo (kendi en iyi ölçümüyle, ortalama).
- 1–10'da kuruldu (yalnız `GECE_HATA_Q` 1–10'dan); **sınav 21–30 bir kez** (~01:13). Platform BUILD 2 klasörü, Mac, Python 3.12.13; üretici 1.3 (K_YUK 1,47); `kac_ev.csv` PR #23 çıktısı (`pv_uc`).

## Sonuç [Hesap; farazi şehir, gösterim]
Renksiz trafo (aday evi olan): 1–10'da 314, 21–30'da 306.

| Seçim (ölçüm sonrası, gerçek sonuçla) | 1–10: yeşile dönen (yanlış) / açılan ev / bayrak (gerçekte dolu) | 21–30: yeşile dönen (yanlış) / açılan ev / bayrak (gerçekte dolu) |
|---|---|---|
| Hepsine gece prizi | 6 (0) / 49 / 8 (6) | 2 (0) / 5 / **15 (3)** |
| Hepsine öğlen yükü | **28 (0) / 201** / 0 | **31 (0) / 175** / 4 (3) |
| Hepsine kademe | 5 (0) / 46 / 3 (1) | 2 (0) / 5 / **7 (0)** |
| Her trafoya kendi en iyi ölçümü | 32 (0) / 238 / 7 (5) | 32 (0) / 178 / 16 (3) |
| **İlk 20** (beklenen değere göre) | **17 (0) / 177** | **14 (0) / 131** |
| Rastgele 20 (ortalama) | 2,0 / 15,2 | 2,1 / 11,6 |

- İlk 20'nin ölçümü: 1–10'da öğlen yükü 16, kademe 3, gece 1; 21–30'da öğlen yükü 18, kademe 1, gece 1. İlk 20'de beklenen açılan ev 189 → gerçekleşen 177 (1–10), 152 → 131 (21–30).
- Öğlen yüküyle yeşile dönenlerin hepsi bugün güveni "orta" ya da "düşük" olan trafolar (21–30: 24 orta, 7 düşük).
- Tek ölçümün rengi beklenen olarak değiştirebildiği trafo: 1–10'da 106/314, 21–30'da 110/306; kalan ~%65'te tek ölçüm önerilmiyor.

## Bulgular
1. **Renksiz trafoyu açan ölçüm öğlen yükü:** trafo başında bir haftalık ölçüm 21–30'da 31 trafoyu yeşile çeviriyor ve 175 ev açıyor; gece prizi ve kademe fotoğrafı yalnız 2'şer trafo, 5'er ev. Panelde "evet"in darboğazı öğlen yük güveni (konum payı günlüğüyle aynı sonuç).
2. **Sıralama işe yarıyor:** ölçüm öncesi beklenen değere göre seçilen ilk 20 trafo, rastgele 20 trafodan ~11 kat fazla ev açıyor (131 ↔ 11,6); beklenen ile gerçekleşen yakın (152 ↔ 131).
3. **Yanlış yeşil her satırda 0** (kapı tutuyor; örnek küçük: yeşile dönen en çok 32 trafo).
4. **Eksi — gece prizi ve kademe sonrası bayraklar güvenilmez:** 21–30'da gece prizinden sonra 15 bayrağın 3'ü, kademeden sonra 7'nin 0'ı gerçekten dolu (1–10'da 8'de 6, 3'te 1). Sebep [Yorum]: gece hatası evin hattaki yerine bağlı ama model tek dağılım kullanıyor; trafoya yakın evde düzeltme barayı fazla yükseltiyor. Kademe penceresi de barayı çoğu trafoda öncülün ortasından yukarı taşıyor. Bu ölçümlerden sonra "dolu" bayrağı konmamalı (yalnız yeşil yönü kullanılmalı) ya da hata modeli gerçek veride (P6 / P7 aynı evde) kalibre edilmeli.
5. Gece prizi barayı inverterin sabah değerinden daha düşük gösteriyor (−1,64 ↔ −0,79 V): pilotta bara için önce inverterli evler, sonra priz.

## Ne kaldı
- Gerçek pilot listesi gerçek trafolardan çıkar (Kıb-Tek'in trafo tablosu, fatura toplamları ve bu betik); buradaki ilk 20 farazi şehirde yöntemin gösterimi.
- Öğlen yükü ölçümünün maliyeti (trafo başına bir haftalık kayıt cihazı, Kıb-Tek izni) diğer ikisinden yüksek; "ucuz" sırası maliyetle tartılmadı.
- İki ölçümün birlikteliği (ör. öğlen yükü + kademe) ölçülmedi; kart yalnız "tek ölçüm" istedi.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas ~01:06 | ölçüm sırası v1, `--kalibrasyon` | 1–10 | gece prizi barayı az düşük gösterir | ortanca −1,64 V, P10 −4,31 V | dağılım modele |
| 1 Kas ~01:09 | v1, K = 8 | 1–10 | ilk 20, rastgele 20'den çok ev açar; yanlış yeşil 0 | 177 ↔ 15,2 ev; yanlış yeşil 0; öğlen yükü baskın | 21–30 bir kez |
| 1 Kas ~01:13 | aynı | 21–30 | aynı | 131 ↔ 11,6 ev; yanlış yeşil 0; gece / kademe bayrakları 3/15, 0/7 | karar masasına (PR) |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
