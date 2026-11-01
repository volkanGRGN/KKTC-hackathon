# 2026-11-01 — Yük haritası: tepe saati (yurt eğrisi, ikinci aday, dönem)

**Amaç:** KARAR 01:30: tepe saati zayıf (±60 dk isabet %45); konutta iki tepe (16–17 ve 23), yurt ticari II eğrisini alıyor. 1–10'da kur, 31–40 bir kez (üretici 1.5). BUILD 1 (yük).

## Teşhis [Hesap: EAC 2022 ay tipik günleri, sınıfın yıllık ortalaması = 1]
- Konut Temmuz iş günü: 23:00 1,86, 00:00 1,84, 16:00 1,83 (neredeyse eşit); Temmuz tatil: 16:00 1,96, 23:00 1,77; Ağustos iş günü 00:00 1,77, 16:00 1,70. Yılın tepesinin hangi tepede olacağını haftanın havası (sıcak gün iş günü mü tatil mi), panelin öğleden sonra üretimi ve ev ev gürültü belirliyor; tek saat söyleyen model konutta en iyi ihtimalle yarı yarıya tutar (öncesi %56).
- Yurt: tarifesi ticari II, model büyük ticaret eğrisini veriyordu (öğlen 13:00); gerçek konut eğrisi (öğleden sonra / gece). ±60 dk %8. Kıb-Tek tarife sınıfını bilir, yapı tipini bilmez. Öğlen modelinin arketipi (ölçülü trafoların Nisan eğrilerinden, Kıb-Tek'in bildiği özelliklerle atanan) yurdu ayırıyor: ticari II abonesi olan trafolarda yurtların 41/48'i "akşam tepeli", çarşıların 0/41'i [Hesap, 1–10].

## Yöntem (`tepe.py` madde 7; 1–10'da)
1. Ticari II abonesi olan trafoda arketip "akşam tepeli" ise ticari II konut eğrisini alır (Nisan oranı, kayıtlar, fider, akşam gerilimi dahil hep aynı harita); yoksa büyük ticaret. `tahmin.csv` / `arketipler.csv` yoksa eski davranış + UYARI.
2. `tepe_saati_2`: yıl taramasının zarfında (bütün ay ve gün türlerinin adım adım en büyüğü) ana tepeden en az 3 saat uzaktaki en büyük; ana tepenin %95'i kadarsa yazılır [Yorum: eşik 1–10'da].
3. `tepe_donemi`: sabah / öğle / öğleden sonra / gece.
Ana tepe saatinin seçimi değişmedi (zarfın en büyüğü).

## Sonuç [Hesap; farazi, gösterim; üretici 1.5; ölçülmeyen 280 trafo]
| | 1–10 önce | 1–10 sonra | 31–40 önce | **31–40 sonra (bir kez)** |
|---|---|---|---|---|
| Tepe saati ±60 dk | %42,1 | %48,2 | %47,5 | **%52,1** |
| İki adaydan biri ±60 dk | — | %59,3 | — | **%60,0** |
| Dönem aynı | %58,9 | %68,9 | %60,7 | **%69,3** |
| İkinci aday yazılan trafo | 0 | 118 | 0 | 97 |
| Yurt: saat ±60 / dönem / tepe hatası | %8 / %5 / %10,2 | %53 / %79 / %4,2 | %17 / %9 / %8,4 | **%57 / %77 / %5,3** |
| Tepe hata ortanca / P90 (hepsi) | %7,5 / %18,4 | %6,3 / %16,8 | %6,7 / %15,3 | **%5,8 / %15,1** |
| Gerçek P90 üstünde | 1/280 | — | 0 | **0** |

- Akşam gerilimi değişmedi (31–40: 3,5 V; 207 V altı 2/2; "yeterli" 233'te 0 yanlış).
- Konutta ana saat isabeti aynı (%62, 31–40); iki adayla %68. Kalan kaçışlar: panelli konutta tahmin gece, gerçek tatil öğleden sonrası (ya da tersi); otel ve çarşıda gerçek tepe 09–13 arası dağınık.

## Eksiler
1. Ana saat hâlâ tek; konutta yarı yarıya. Harita kartında "16–17 ya da 23–00" (iki aday) gösterilmeli (Civan'ın kart işi).
2. Arketip yalnız Nisan eğrisinden; yazın klimalı ticari II'yi ayırmayabilir. Kıb-Tek müşteri listesinde yapı tipi (istek metni madde 9) gelince yerine konur.
3. Can'ın sınavı tek saati ölçüyor; "iki adaydan biri" ve dönem bilgi satırı olarak eklenebilir (can.md'ye öneri).

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas 01:35 | tepe.py + arketipli ticari II, ikinci aday | 1–10 | yurt doğru eğriyle saat ve tepe düzelir; iki aday konutun iki tepesini kapsar | yurt %8 → %53; iki adaydan biri %59; dönem %59 → %69; tepe hatası %7,5 → %6,3 | kabul |
| 1 Kas 01:35 | aynı | 31–40 bir kez | aynı | saat %48 → %52, iki aday %60, dönem %61 → %69; tepe %6,7 → %5,8, P90 üstü 0 | PR |

## Düzeltme (02:11, TEST bulgusu, KARAR 02:0x) — "önceki sütunlar ve akşam gerilimi değişmedi" doğru değil
Yukarıdaki "Ana tepe saatinin seçimi değişmedi" yalnız seçim kuralı için doğru; "Akşam gerilimi değişmedi" yanlış. **Yurt eğrisi değişince ölçülü yurt trafolarının Nisan oranı (R) değişir, R'lerin ortalaması popülasyon R'si olduğu için yurt dışındaki ölçülmeyen trafoların tepesi, bandı ve boş kVA'sı da değişir** [Hesap; TEST'in bağımsız koşusu ve BUILD 1'in koşusu birebir; üretici 1.5, 31–40]:
- Tepe, P90 ya da boş kVA'sı değişen trafo: **262/400**.
- Popülasyon R'si (Velander R0): 9/10 şehirde **−%0,3 … −%1,5** (şehir 31–40: −1,2, −0,9, −1,0, −1,0, −0,3, −0,6, −1,5, −1,2, −0,6, 0,0).
- Yurt dışındaki trafolarda tepe değişimi: ortanca **%0,4**, en çok **%13,8**.
- Akşam gerilimi neredeyse aynı, birebir değil: "yeterli" (P10 ≥ 207 V) **232 → 233** (ikisinde de 0 yanlış), uyarı **48 → 47**, %80 kapsama **%87,9 → %88,9**.
- Ölçüm rakamları değişmedi (saat ±60 dk %52,1, iki aday %60,0, dönem %69,3, tepe hatası %5,8, gerçek P90 üstü 0). Kod değişmedi.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
