# 2026-11-01 — Yük haritası: akşam gerilimi tahmini, ön sürüm (`tepe.csv` `v_min_tepe_v`)

**Amaç:** KARAR 00:57 madde 4: yük tarafının gerilim sorusu, "yılın tepesinde evler 207 V'un altına iniyor mu" (ADR-0014, ADR-0016 m. 3). Can'ın `sinav.py faz2` 207 V maddesi `tepe.csv`'de `v_min_tepe_v` bekliyor. BUILD 1 (yük).

## Yöntem
- **Aynı fizik:** panel tarafının olasılıklı ağ kurucusu (`kac_ev_olasilik.ag_kur`, BUILD 2'nin dosyası, yalnız okunur): Kıb-Tek'in bildiğiyle (abone sayıları, hat sayısı ve boyu, kablo, kVA, panel) ağ; bilinmeyenler aralıktan (bara 244–252 V, hat boyu × 0,6–1,6, abonenin hattı ve sırası, fazı, büyük abonenin yeri, panelli evler). İngiltere'ye kalibre empedans payı (s = e^N(0,172; 0,414)) aynen. `trafo_bos_kapasite.solve`.
- **Çekiliş başına (40):** ağ; toplam net yük tepe bandından (ortanca `tepe_kw`, iki yan P10 / P90'dan ayrı log-normal); abonelere dağılım sınıfın tepe anındaki EAC değeri × sıcaklık çarpanı × kişisel fark (log-normal σ 0,3, panel tarafıyla aynı); o anki güneş üretimi panelli evlerde düşülür (brüt = net + üretim); OG değişimi U(−%1; 0) [Yorum: sistem tepesinde bara biraz düşer; Kıb-Tek ölçümü BULAMADIM]. Sonuç: evlerin en düşük faz gerilimi (üç fazlı evde üç faz da; üreticinin tanımıyla aynı fiziksel büyüklük).
- **Çıktı (`tepe.csv` sonuna, sözleşme §8):** `v_min_tepe_v` (ortanca), `v_min_tepe_v_p10` / `_p90`, `p_aksam_207`. **Karar P10'dan:** P10 ≥ 207 V ise "akşam gerilimi yeterli".

## Sonuç [Hesap; farazi, gösterim, üretici 1.4]
| Ölçülmeyen trafolar | Şehir 1–10 (280) | Sınav 21–30, bir kez (280) |
|---|---|---|
| Hata \|Δ\| ortanca / P90 | 4,1 V / 15,5 V | 5,2 V / 16,5 V |
| Sapma (ortanca; − = model daha düşük gerilim) | −2,8 V | −3,8 V |
| %80 bant kapsama | %86,1 | %79,3 |
| Gerçek P10'ın altında | %0,7 | %2,5 |
| Gerçekte 207 V altı | 6 | 10 |
| Yakalanan (P10 < 207) | **6/6** | **10/10** |
| Yakalanan ortancayla (< 207) | 3/6 | 5/10 |
| "Yeterli" (P10 ≥ 207): trafo, gerçekte altında | 178, **0** | 173, **0** |
| "Yeterli" ortancayla: trafo, gerçekte altında | 263, 3 | 259, 5 |
| Uyarı (P10 < 207), gerçekte altında | 102, 6 | 107, 10 |

- Çarşı / otel / sanayi trafolarında model gerilimi 10–16 V düşük buluyor (temkinli yön): büyük abone çekilişlerin yarısında ortak hattın başında, empedans payı ortancada × 1,19.
- **Ortancayla karar verilirse yük tarafının yanlış yeşili çıkıyor** (1–10'da 3/263, 21–30'da 5/259 "yeterli" trafo gerçekte 207 V altında); P10 ile 0. Bu yüzden karar sütunu P10; Can'ın sınavı bugün `v_min_tepe_v`'yi (ortanca) karar için okuyor → can.md'ye UYARI.
- Uyarılar çok (yaklaşık 100 trafo, 6–10'u gerçek): ağ kaydı yok, bilinmeyenler geniş. Kıb-Tek hat / faz kaydı geldikçe daralır (Faz 9).
- Önceki 18 sütun PR #26 ile birebir (10/10 şehir).

## Eksiler
1. Uyarı payı yüksek (ölçülmeyenin %36–38'i P10 < 207): ağ bilgisi yokken temkinli; tek başına "güçlendir" denmez, "önce bak" sınıfı.
2. Ağ kurucu panel tarafının dosyasında; BUILD 2 değiştirirse akşam sonucu da değişir (aynı fizik ilkesi; ADR-0015 m. 3).
3. Üretici 1.4'te uzun köy hatları gerçekçi değildi (1.5 düzeltiyor, PR #27); 1.5 şehirleriyle bir kez daha.
4. OG değişimi ve kişisel fark [Yorum]; akşam OG gerilimi Kıb-Tek'ten (istek metni madde 8, SCADA) gelince yerine konur.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas 01:09 | tepe.py + akşam gerilimi | 1–10 | panel fiziği akşam düşümünü kapsar | P10 6/6 yakaladı, P10 ≥ 207'de 0 yanlış | kabul (ayar yok) |
| 1 Kas 01:09 | aynı | 21–30 bir kez | aynı | P10 10/10, 0 yanlış; kapsama %79 | PR; karar masası tekrarlar |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
