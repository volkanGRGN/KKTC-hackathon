# Trafo Şablonu — hackathon iş planı

VCC-2 · yazıldı 31 Ekim 2026, 09:30 · [araştırma](log/2026-10-31-kapsamli-arastirma.md) + Muhittin'in cevabı birleştirildi · kararların gerekçesi [decisions/](decisions/)

**Ürün tek cümle:** Kıb-Tek için bir **triyaj aracı** — az sayıda trafoyu ölç, gerisini şablonla tahmin et; her trafo için "öğlen ne kadar dolu, kaç ev daha panel takabilir, ne kadar eminiz" göster. Yeşil → hızlı onay, kırmızı → işaretle, sarı / düşük güven → **ret değil, ölçüm cihazı tak** (ya da esnek onay).

**Varsayım:** sunum 1 Kasım öğleden sonra (saat belli değil; belli olunca kaydır).

---

## Kilit kararlar

1. **Problem ikiye bölünür (Muhittin + İngiliz yöntemi aynı şeyi söylüyor):** şekil (normalize günlük eğri → 3–6 arketip) + büyüklük (abone sayısı × tarife sınıfı ile ölçekleme).
2. **Hedef tepe değil, bahar öğleni (11–14) en düşük yük.** İngiliz makalesi tepe tahmin ediyor; öğlen için doğrulanmış çalışma bulamadık → "doğrulanmadı" diye söylenir.
3. **Gerilim ilk sürümde VAR.** Muhittin önce "ısıl pay, gerilim sonra" demişti; ikinci cevabında katıldı: küçük, yalıtık, uzun kırsal hatlı ada şebekesinde önce gerilim bağlar, anakara aracı Kıbrıs'a olduğu gibi taşınamaz, "fazla kapasite"nin tanımı bile değişir (ısıl pay yerine gerilim payı). Gerilim formülü tek satır, ev ev benzetimimiz hazır → ikisinin küçüğü alınır.
4. **Test asla yalnız farazi veride değil (Muhittin).** Kanıt sırası: (a) İngiltere gerçek veride ~%80 (dış kanıt), (b) mümkünse İspanya'nın 30 gerçek trafosunda bizim hattımızla bir-trafo-dışarıda doğrulama, (c) farazi şehir yalnız gösterim.
4b. **Tek şehir değil, onlarca farazi şehir (Muhittin: "alan rastgeleleştirme").** Tek şehirde model şehri değil benzetimin varsayımlarını öğrenir. Fizik (güç akışı, güneş) gerçeğe iyi taşınır, insan davranışı taşınmaz. Belirsiz parametreler (sınıf başına tüketim, kullanım saatleri, panel yaygınlığı, hava yılı) rastgele değiştirilerek 20–30 şehir üretilir; yöntemin başarısı tek sayı değil, şehirler arası aralık olarak verilir. Bizim avantajımız: davranış katmanı uydurma değil, Güney Kıbrıs'ın 2022'de gerçek sayaçlardan ölçtüğü eğriler. Gerçek verinin görevi "eğitmek" değil "benzetimin yanlılığını düzeltip kanıtlamak"; birkaç gerçek trafo bile açığı görmeye yeter.
5. **Belirsizlik tek sayı değil bant:** bir-trafo-dışarıda artıklarından P10–P90; "%80 bandım gerçekten %80'i kapsıyor mu" kontrolü; ölçülü trafolara benzemeyen trafoya "düşük güven".
6. **Kesilenler:** derin öğrenme, Fourier katsayıları, havaya bağlı dinamik model, saat altı çözünürlük, pandapower'a geçiş. Esnek Onay kod değil, tek slayt (sarı trafolar için seçenek).

---

## İş kolları (isimleri Volkan dağıtır)

**Kol 1 — Veri ve farazi şehir** (Claude kodlar, bir kişi kontrol eder)
- EAC profil sınıflarını oku (12 sınıf; bahar ve yaz tipik günleri), 30 dk → 5 dk ara değer.
- 40 trafo, 7 tip (şehir konutu, köy, çarşı, otel, sanayi, sulama, yurt): kVA (Kıb-Tek direk 25–400, yer 50–2.500), tarife sınıfı karışımı (Kıb-Tek 2023 abone oranları), hat boyu ve ev sayısı (SimBench ölçüleri), panel sayısı.
- Mevcut benzetimle her trafonun "gerçek" öğlen yükü ve hat ucu gerilimi → farazi şehrin cevap anahtarı.
- Şehir üreticisi rastgeleleştirmeli olsun: sınıf başına tüketim ±%20, kullanım saatleri ±30–60 dk kayma, ev başına ölçek dağılımı, panel yaygınlığı %10–50, EAC'nin farklı ay/gün tipleri, Open-Meteo 2024 ve 2025 hava yılı → 20–30 şehir (40 trafo ~30 sn ise hepsi ~15 dk).
- **Zaman kutusu 2 saat:** İspanya EDP verisi (30 gerçek trafo, 20 gün akıllı sayaç, CC BY) indir; trafo başına toplam eğri çıkıyorsa gerçek doğrulama seti olur. Çıkmazsa bırak.

**Kol 2 — Şablon hattı** (Claude kodlar, bir kişi sunuma çevirir)
- Ölçülecek trafoları tabakalı ve çeşitli seç (Muhittin: benzer yere değil boşluğa sayaç).
- Normalize eğri → k-means / hiyerarşik → 3–6 arketip.
- Atama: çok sınıflı lojistik regresyon (abone karışımı, kVA, panel sayısı, bölge tipi).
- Ölçekleme: küme başına negatif olmayan regresyon, hedef öğlen minimum.
- Bir-trafo-dışarıda doğrulama; P10–P90 bant; kalibrasyon; güven etiketi.
- Doğrulamayı her şehirde ayrı koş; bir şehirde eğitip başka şehirde dene (şehirler arası) → sonuç "20–30 şehirde yanlış yeşil oranı şu aralıkta" diye verilir.
- Gösterim grafiği: ölçülen trafo 5 / 10 / 20 → hata (farazi, "gösterim" etiketli).

**Kol 3 — Kaç ev sığar** (Claude kodlar, bir kişi kontrol eder)
- Isıl pay: trafo gücü + öğlen yükü − mevcut panel; yanına bugünkü %40 kuralı.
- Gerilim payı: 259 − 250 V, tek faz karamsar / dengeli iyimser, hat boyu ve iletken direnci.
- İkisinin küçüğü ÷ 6,5 kW = kaç ev. Renk karamsara göre; düşük güven → sarı.
- Formül, ev ev benzetimle 40 trafoda karşılaştırılır (yanlış yeşil sayısı = en kritik ölçü).

**Kol 4 — Harita paneli** (bir kişi, Claude yardım eder)
- Streamlit + pydeck: trafo = 3D sütun (boy doluluk, renk triyaj). Tıklayınca: öğlen eğrisi + bant, kaç ev, güven, "ölçülmedi" etiketi.
- Üstte üç rakam: açılabilecek başvuru, MW, yılda yakıt.
- Kenarda "örnek veri" etiketi ve kaynaklar. İnternet yedeği: altlıksız harita + ekran kaydı.

**Kol 5 — Sunum ve hikâye** (Volkan önerilir)
- Akış: Güney bağladı, güneşinin %47'sini atıyor → Kuzey'de 2.670 başvuru bekliyor, Kıb-Tek mahalleyi görmüyor → İngiltere 800 trafo ölçüp gerisini %80 tahmin etti → biz Kıbrıs'a uyarladık, hedefimiz öğlen ve gerilim → canlı harita → pilot: önce 20–50 trafo (Muhittin), sonra 120–170, taşınabilir cihazla ~20 bin € + pens, baharda → itirazlar ve cevapları.
- İtiraz slaytı (Muhittin): ret değil triyaj, insan onayı, itiraz edenin gerçek ölçüm isteme hakkı, az ölçülen bölgeye haksızlık riski, komşu etkileşimi, zamanla yeniden ölçüm.
- Jüri soru provası ([araştırma bölüm 8](log/2026-10-31-kapsamli-arastirma.md#8-zayıflıklar-ve-jürinin-soracakları)).

---

## Takvim (sunum saati belli olunca kaydır)

| Ne zaman | Kol 1 | Kol 2 | Kol 3 | Kol 4 | Kol 5 |
|---|---|---|---|---|---|
| Cmt 10–13 | farazi şehir + cevap anahtarı | arketip kümeleme (eski benzetim verisiyle başla) | formül yazımı | panel iskeleti, sahte veriyle | hikâye taslağı |
| Cmt 13–15 | İspanya verisi (2 saat kutu) | atama + ölçekleme | benzetimle karşılaştırma | harita + tıklama | slayt iskeleti |
| Cmt 15–20 | yardım | doğrulama, bant, güven | renk/triyaj kuralı | gerçek çıktıları bağla | rakamlar, kaynak slaytı |
| Cmt 20–24 | — | **uçtan uca ilk çalışan hal** | — | panel uçtan uca | prova 1 |
| Paz sabah | hata ayıklama | gösterim grafiği | — | ekran kaydı yedeği | prova 2, jüri soruları |

**Cumartesi gece yarısı hedefi:** her trafo için sayı + bant + güven + renk veren, doğrulanmış uçtan uca hat ve onu gösteren panel. Rafine işler pazar sabahı.

## Uzmana sorulacaklar (fırsat olursa kampta)
1. Kuzey'de kaç dağıtım trafosu var? 2. Hangi abone hangi trafoda — dijital mi? 3. Trafo başına hat uzunluğu / kablo kaydı var mı? 4. Evlerin hangi faza bağlı olduğu biliniyor mu? 5. Kıb-Tek'te taşınabilir yük analizörü var mı?
