# 2026-11-01 — Can: üretici 1.5 (yük haritası için trafo gücü ve hat tasarımı)

**Etiket: farazi şehir, gösterim.** Çapalar gerçek veri: Malta (Enemalta kapasite haritası), ADR-0016 m. 3.

## Hipotez / amaç
Karar masası 23:35 (2): üretici 1.4 yılın tepesini benzetiyor ama trafo gücü ve hatlar Nisan'a göre kurulu. Sonuç (BUILD, 1–10): yaz tepesinde 17/400 trafo gücünü aşıyor (otel 9/42), 8/400 trafoda akşam gerilimi 207 V altı, en düşük 162,8 V. Gerçekte Kıb-Tek trafoyu ve hattı yılın tepesine göre kurar; bu kadar aşan ya da düşen hat güçlendirilir [Yorum]. Yük haritası sınavı ancak gerçekçi bir şebekede anlamlı. Hedef: Malta'nın yıl tepesi ÷ güç dağılımı (P10 / 50 / 90 0,13 / 0,42 / 0,74, aşan %1,5) ve ADR-0016 m. 3 (207 V altı ≤ %1, en düşük ≥ 200 V).

## Yaptıklarım (dal `uretici/1.5`, PR #21'in üstünde; `src/sehir_uret.py` Volkan'ın, karar masası 23:18 / 23:35 ile Can'a verildi)
1. **Trafo gücü yılın tepesinden:** tasarım tepesi = sınıfın tipik gün tepesi × (1 + β_yaz · ΔT_tasarım), ΔT_tasarım 5 °C [Yorum]; büyük abonenin kendi büyüklüğü (log-normal ölçek) girer (Kıb-Tek kayıtlı en yüksek talebini bilir; Muhittin); küçük abonede tarife ortalaması, gizli mahalle çarpanı yalnız aşırı yük olacaksa (1.4 kuralı). Büyütme payı 1,2–2,0 (değişmedi). Güç listesine 1.600 / 2.500 kVA (yer tipi) [Kaynaklı: ASTOR kataloğu]. Güç evler kurulduktan sonra seçilir.
2. **Büyük abone baradan kendi kablosuyla:** otel, büyük dükkân, büyük sanayi, yurt ortak alçak gerilim hattından çıkarılır, 30 m, yüke göre paralel ABC95 (faz akımı ≤ 250 A) [Yorum; Kıb-Tek pratiği ve kablo taşıma değeri BULAMADIM]. 1.4'te otel ortak hatta ABC95'in birkaç katı akım çekiyordu; ilk denemede (yalnız 1 ve 3 ile) yaz tepesinde benzetim otel trafolarında çöktü (en düşük 15,5 V, tepe 4.148 kVA): bölme işe yaramaz, büyük abone tek bir noktadır.
3. **Hat akşam tepesine göre tasarlanır:** her hattın tasarım düşümü I × |z_hat| ÷ 2 (yük düzgün dağılmış), I = tasarım yükü (trafoyla aynı: plan × büyütme payı) × en yüklü faz payı (1 + FAZ_SAPMA: kentsel 1,25, kırsal 1,5; UKPN). Sınır 24 V (244 V bara − 5 V trafo − 24 ≈ 215 V) [Yorum]. Aşan trafoda önce kesit ABC95, sonra aşan hat ikiye bölünür (evler sırayla iki hatta, aynı boy). Yeni kablo türü eklenmedi (direnci kaynaksız olurdu).
- Rastgele akış korunur: büyütme payı 1.4'teki sırada çekilir, büyük abone ve hat değişiklikleri evler kurulduktan sonra yapılır. Nisan dosyaları yalnız gücü ya da hattı değişen trafolarda farklıdır.
- `ayar.json`: `uretici_surumu` 1.5, `hat_tasarim` ({ilk, kesit, bolme} sayısı).

## Sonuç [Hesap] — ayar şehirleri 1–10 (400 trafo), sınav şehirlerine bakılmadı

| Ölçü | 1.4 (BUILD) | 1.5 deneme 1 (1 + 3) | 1.5 deneme 2 (+ 2) | 1.5 son (+ tasarım yükü) | Hedef |
|---|---|---|---|---|---|
| Yıl tepesi ÷ güç P10 / 50 / 90 | — | 0,22 / 0,45 / 0,74 | 0,22 / 0,44 / 0,72 | **0,22 / 0,44 / 0,72** | Malta 0,13 / 0,42 / 0,74 |
| Gücünü aşan | 17 (%4,3) | 10 (%2,5) | 3 (%0,8) | **3 (%0,8)**: otel 2, köy 1 | Malta %1,5 |
| 207 V altı | 8 (%2) | 24 (%6) | 2 (%0,5) | **1 (%0,2)** | ≤ %1 |
| En düşük gerilim | 162,8 V | 15,5 V (çöküş) | 188,4 V | **203,6 V** | ≥ 200 V |
| Hat tasarımı ilk / kesit / bölme | — | 270 / 5 / 125 | 385 / 5 / 10 | 333 / 10 / 57 | |

Deneme 2'de kalan: 200 V altı iki köy trafosu (775 m ve 886 m hat, ABC95); tasarım yükü ev başına ~1,3 kW iken yaz tepesinde ~2,6 kW (klima, sıcak gün, mahalle). Düzeltme: hat tasarımı trafo seçimindeki büyütme payını kullanır, dengesizlik bölgeye göre.

Son tur (1–10): tipe göre yıl tepesi ÷ güç ortancası çarşı 0,47, köy 0,41, otel 0,56, sanayi 0,49, şehir konutu 0,34, sulama 0,45, yurt 0,46. Güç dağılımı 25:17, 50:49, 100:103, 250:111, 400:38, 630:29, 1000:31, 1600:20, 2500:2. Şehir konutunda tepe saati 00:xx 31, 20:xx 21, 17:xx 19, 23:xx 17 (gece yarısı tepesi 1.4'te de var; EAC konut eğrisinden, sebebi ayrıca bakılacak [Yorum]). P10 0,22 Malta'nın 0,13'ünden yüksek: farazide az yüklü (boş yazlık, yeni yerleşim) trafo yok [Yorum]; ayarlanmadı.

**Üretim süresi:** son turda 40–140 sn; sebep makine yükü (aynı anda başka oturumlar, işlemci %43): sehir-007 tek başına 1.5 ile 73,4 sn, **1.4 ile 70,6 sn** (aynı anda ölçüldü); önceki turda (makine daha boşken) aynı şehir 37,0 sn. 1.5 süreyi değiştirmiyor; Faz 1'in 60 sn sınırı boş makinede ölçülmeli.

## Sınav şehirleri 31–40 (bir kez üretildi; ayar 1–10'da bitti, 31–40'a bakılarak değiştirilmedi)

| Ölçü | 1–10 (ayar) | **31–40 (sınav)** | Hedef |
|---|---|---|---|
| Yıl tepesi ÷ güç P10 / 50 / 90 | 0,22 / 0,44 / 0,72 | **0,24 / 0,43 / 0,67** | Malta 0,13 / 0,42 / 0,74 |
| Gücünü aşan | 3 (%0,8) | **3 (%0,8)**: sulama 2, otel 1 | Malta %1,5 |
| 207 V altı (yıl pencereleri) | 1 (%0,2) | **2 (%0,5)** | ≤ %1 |
| En düşük gerilim | 203,6 V | **202,8 V** | ≥ 200 V |
| Hat tasarımı ilk / kesit / bölme | 333 / 10 / 57 | 325 / 14 / 61 | |

Şehir konutu tepe saati (31–40): 23:xx 44, 00:xx 20, 17:xx 17, 22:xx 16, 01:xx 15. Güç dağılımı 25:20, 50:24, 100:104, 250:116, 400:48, 630:32, 1000:29, 1600:24, 2500:3.

Sınavlar (main'deki `sinav.py` 672ce1a; şablon ve kaç ev bu dalın kodu, K_YUK dalın tabanındaki gibi; İspanya satırı K_YUK 1,27'li `edp_test.py` çıktısı):
- **`faz1` 31–40:** 5 maddenin 4'ü GEÇTİ: tipler, v_max > 259 V 45/400, Nisan v_min 207 V altı 0/400 (en düşük 222,3 V). **Üretim süresi KALDI** (en uzun 112,2 sn, ortanca 85,5): makine yükü (yukarıda; 1.4 aynı anda aynı yavaşlıkta). Boş makinede yeniden ölçülmeli (karar masası, Mac).
- **`faz2` 31–40:** bütün maddeler GEÇTİ; yük hatası %11,3 / P90 %28,1; İspanya %80 bant %76,8, PIT 0,071; şehirler arası 1,01; düşük güven %5,4; farazi kapsama %82,1 (bilgi); saf fatura farkı %10,9 / %4,9 (bilgi). **Doğru arketip ortancası %75,0, tam eşikte** (en kötü sehir-033 %42,9); 1.3'te 21–30 %89,3. Büyük abonenin ayrı hatta alınması ölçülü trafo eğrisini değiştirmez; düşüşün sebebi bilinmiyor [Yorum], karar masasına.
- **`faz3` 31–40:** yanlış yeşil **0/28** GEÇTİ; %40 kuralı dolu 46 trafonun 24'üne "yer var", biz 0; kırmızı kovası %44,6 ≥ 0,38 GEÇTİ; kaç ev orta 2 GEÇTİ; yeşil / sarı / kırmızı 28 / 254 / 65 (%8 / %73 / %19).
- Yük haritası sınavı: tepe modeli (B-Y2) olmadığı için "ölçülmedi"; cevap anahtarının yıl tepesi sütunları dolu.

## Sıradaki
- PR (taban `uretici/1.4-tepe`, PR #21); karar masası Mac koşumu ve süre ölçümü; Civan / BUILD onayı.
- B-Y2 tepe modeli 1.5 şehirlerinde (Civan'ın eşzamanlılık / sıcaklık analizi gelince).

## Ek — birleşik ağaç (main + 1.5), karar masası Mac koşumu (KARAR 01:20)
Dal PR #21'in yaz penceresi düzeltmesinden (13e8485) önceki hâlin üstünde; yukarıdaki tablolar düzeltme öncesi pencereyle. main'e çakışmasız birleşiyor; karar masası birleşik ağacı Mac'te sıfırdan koştu [Hesap: karar masası 01:18]:
- 1–10: yıl tepesi ÷ güç P50 / P90 0,47 / 0,73, aşan %0,8, 207 V altı %0,5, en düşük 201,1 V.
- **31–40: 0,44 / 0,68, aşan %0,5, 207 V altı %0,5, en düşük 201,1 V**; tepe ayı Temmuz. Hedeflerin hepsi tutuyor; yeniden ayar gerekmedi (KARAR 00:24'ün istediği).
- faz1 20 şehir 5/5, **üretim süresi 55,6 sn GEÇTİ** (Windows'taki KALDI makine yüküydü); faz2 31–40 GEÇTİ (arketip ortancası %75,0, eşikte — açık); faz3 31–40 yanlış yeşil 0/28, %40 kuralı 24/46, kırmızı kovası %45,3, sarı %73,5.
Resmi rakamlar bunlar (birleşik ağaç, Mac); puanlayan karar masası.
