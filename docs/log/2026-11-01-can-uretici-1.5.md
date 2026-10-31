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

**Üretim süresi:** son turda 40–140 sn; sebep makine yükü (aynı anda başka oturumlar, işlemci %43): sehir-007 tek başına 1.5 ile 73,4 sn, **1.4 ile 70,6 sn** (aynı anda ölçüldü); önceki turda yükle aynı şehir 37,0 sn. 1.5 süreyi değiştirmiyor; Faz 1'in 60 sn sınırı boş makinede ölçülmeli.
