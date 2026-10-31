# Trafo Şablonu — hackathon iş planı

VCC-2 · yazıldı 31 Ekim 2026 sabahı · [araştırma](log/2026-10-31-kapsamli-arastirma.md) + Muhittin'in cevabı birleştirildi · kararların gerekçesi [decisions/](decisions/)

**Ürün tek cümle:** Kıb-Tek için bir **triyaj aracı** — az sayıda trafoyu ölç, gerisini şablonla tahmin et; her trafo için "öğlen ne kadar dolu, kaç ev daha panel takabilir, ne kadar eminiz" göster. Yeşil → hızlı onay, kırmızı → işaretle, sarı / düşük güven → **ret değil, ölçüm cihazı tak** (ya da esnek onay).

**Varsayım:** sunum 1 Kasım; saat belli olunca sıra sıkıştırılır.

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

## İş kolları

Fazlar, bitiş listeleri (DoD), kim ve ne zamana [ROADMAP.md](../ROADMAP.md)'de; burada tekrar edilmiyor. Kol numaraları fazlarla aynı: Kol 1 = Faz 1 (deneme şehirleri), Kol 2 = Faz 2 (modeli eğitme ve sınama), Kol 3 = Faz 3 (panel katmanı: kaç ev sığar), Kol 4 = Faz 4 (ürün: trafo görünürlük haritası), Kol 5 = Faz 5 (sunum ve prova).

## Sıra (saat yok; önce/sonra)

1. Tablo biçimi sözleşmesi (kısa) → herkes kendi dosyasına çekilir.
2. Paralel: Faz 1 (biz şehir üreticisi, Can eğri okuma + veri, Civan sahte veri + harita iskeleti).
3. Faz 2 (biz model; Can sınav kodu ve grafikler, gerçek veri adayları; Civan yan panel).
4. Faz 3 (biz kaç ev; Can Faz 3 ölçüleri ve kilit grafik; Civan haritayı gerçek tabloya bağlar).
5. Faz 4 son hali (Civan) ve her fazın geçme sınavına birlikte bakış; geçmeyen varsa önce o.
6. En son Faz 5: sunum, 2 prova.

Hedef: sunumdan önce her trafo için sayı + bant + güven + renk veren, sınavdan geçmiş uçtan uca hat ve onu gösteren panel.

## Uzmana sorulacaklar (fırsat olursa kampta)
1. Kuzey'de kaç dağıtım trafosu var? 2. Hangi abone hangi trafoda — dijital mi? 3. Trafo başına hat uzunluğu / kablo kaydı var mı? 4. Evlerin hangi faza bağlı olduğu biliniyor mu? 5. Kıb-Tek'te taşınabilir yük analizörü var mı? 6. Kaç konut abonesi mahsuplaşmada (çatı panelli)? Ülke geneli yaygınlık ([ADR-0006](decisions/adr-0006-panel-yayginligi-bugunun-kibrisi.md): BULAMADIM). 7. Mahsuplaşma sayaçlarında çekilen ve verilen enerji ayrı kayıtlı mı? (Faturada net görünüyorsa evin kendi tükettiği panel üretimi hiç sayılmıyor; trafo başına fatura toplamı panelli trafoda tüketimi küçük gösterir. Karar masası 31 Ekim 17:26; üretici 1.3'te net fatura + panel düzeltmesi.)
