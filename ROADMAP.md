# Yol haritası

**MVP nedir:** Kıb-Tek'in bugün göremediği mahalle trafolarını, az sayıda ölçümden öğrenen bir modelle **haritada görünür kılmak**: her trafo için öğlen doluluk, tahminin aralığı ve güveni. Güneş paneli (kaç ev daha sığar) bu haritanın **ilk uygulama katmanı** ve sunumun hikâyesi; harita aynı modelle başka sorulara da (akşam yükü, trafo değişim önceliği) açılabilir.

**Veriden modele akış:** Faz 1 veriyi üretir ve toplar (deneme şehirleri + gerçek Kıbrıs eğrileri) → Faz 2 modeli bu veriyle eğitir ve sınar → Faz 3 model çıktısını panel sorusuna çevirir → Faz 4 hepsini haritada gösterir.

Her fazda iki liste: **Yapılacaklar** (iş tarifi) ve **Geçme sınavı** (ölçülebilir; her maddede eşik var, geçilmeden faz bitmez). Sıra ve kilit kararlar [docs/01-plan.md](docs/01-plan.md)'de; gerekçeler [docs/decisions/](docs/decisions/) altında. Tek kaynak kuralı: aynı şeyi iki yerde yazma, bağla.

Taslak 31 Ekim; ekiple oturtuluyor. Süreler kaba: kısa < orta < uzun; saat yok, sıra var. Kod dosyaları kendi fazında, kendi görev kartıyla yazılır; main'de olanlar: `src/sehir_uret.py`, `src/profiller.py`, `src/sinav.py` (Faz 1).

**Her fazda ortak sınav (Muhittin):** ilgili doküman güncel · sonuç `docs/log/` altında gerçek rakamla · karar değiştiyse yeni ADR · farazi sonuç "gösterim" etiketli · her rakam [Kaynaklı]/[Hesap]/[Yorum].

**Roller (Volkan, 31 Ekim):** Planlama, sözleşmeler ve görev kartları Volkan'da (+ Claude; en güçlü model ve en geniş bütçe burada); Can ve Civan kartları uygular ([docs/gorev/](docs/gorev/README.md)). Volkan, Can ve Claude çekirdek hatta birlikte ilerler (Faz 1 → 2 → 3); veri aramayı her fazın kendi adımı olarak **Can yapar** (indirme, KAYNAK, veri sözlüğü); Volkan indirmez, yalnız eleme kararını onaylar (31 Ekim, iş iki kez yapılmasın diye). Civan harita fazındadır (Faz 4), veri aramaya girmez. Sunum (Faz 5) en sonda, hepsi birlikte.

**Bağımlılıklar:** 1 → 2 → 3 → 4 (gerçek veri) → 5. Faz 4 iskeleti, Faz 1'den çıkan **tablo biçimi** kararlaştırılır kararlaştırılmaz sahte veriyle başlar.

---

## Faz 0 — Öğrenim: projeyi sıfırdan anlamak (yazıldı; ekip çalışıyor)

[docs/02-faz-0-ogrenim.md](docs/02-faz-0-ogrenim.md). Sınavı orada: 8 soru, benzetim çalıştırıldı, EAC verisi indirildi, doğrudan main'e küçük commit gönderdi.

## Faz 1 — Deneme şehirleri: cevap anahtarı bilinen farazi Kıbrıs şehirleri kurmak (bitti 31 Ekim)

**Amaç:** Cevap anahtarı bilinen, Kıbrıs'a benzeyen 20–30 şehir.
**Girdi:** Aşağıdaki veri adımı + EAC profil sınıfları (elimizde) + Kıb-Tek 2023 tarife sınıfı abone oranları + mevcut benzetim.
**Çıktı:** `src/sehir_uret.py`; `data/synthetic/sehir-<NNN>/`: trafo tablosu, 5 dakikalık yük (adım adım en yüksek ve en düşük ev gerilimiyle), cevap anahtarı, ayar dosyası (tohum dahil). Biçim: [docs/data/tablo-bicimi.md](docs/data/tablo-bicimi.md).
**Kim / süre:** üçü paralel · uzun (günün büyük kısmı).
**Paralel işler ve dosyalar:**
- Volkan+Claude → önce `docs/data/tablo-bicimi.md` (kısa; herkes bunu bekler), sonra `src/sehir_uret.py` (şehir kurma, rastgeleleştirme, cevap anahtarı), `docs/log/…-volkan-faz1.md`.
- Can → `src/profiller.py`: EAC Excel'ini okur, kullandığımız 8 abone sınıfının şekil eğrisini verir (yıllık ortalama = 1; tiplerin abone karışımı ve büyüklük şehir üreticisinde), 30 dk → 5 dk açar, iş günü/tatil ve ay seçer, sağlama rakamlarını yazdırır (öğlen/akşam oranı, otel yaz/kış); + veri adımı (`data/raw/<veri>/KAYNAK.txt`, `docs/data/data-dictionary.md`), `docs/log/…-can-faz1.md`. Şehir üreticisi bu dosyayı çağırır.
- Civan → `app/ornek_veri.py` (tablo biçimine uygun sahte şehir) + `app/harita.py` iskeleti; `data/raw/osm-kasaba/`.

Yapılacaklar — veri (Can yapar, Volkan eleme kararını onaylar; her aday için eleme: Kıbrıs/Akdeniz mi · ölçülmüş mü · ≤ 1 saat mi · kaynak ve lisans var mı · bu fazda kullanılacağı belli mi; üçten az "evet" → elenir, nedeni günlükte):
- Lefkoşa saatlik güneş 2024 ve 2025 (Open-Meteo, CC BY) — hava yılı.
- EAC "Injection" profil sınıfları (panelli evin şebekeye verdiği eğri; EAC arşiv klasöründe).
- SimBench alçak gerilim şebekeleri (yalnız hat boyu, kablo kesiti, trafo başına ev sayısı).
- Kıb-Tek kablo ve trafo şartnameleri: ABC 70/95 direnci, kVA listesi.
- Otel doluluk aylık (elimizde), yurt yatak sayısı (BULAMADIM → varsayım).
- Her indirilen `data/raw/<ad>/` + KAYNAK.txt; her aday [veri sözlüğünde](docs/data/data-dictionary.md) satır ya da "elendi + neden".

Yapılacaklar — kod (Claude):
- Can'ın `profiller.py`'sinden abone sınıfı eğrilerini al (30 dk → 5 dk açma orada); 7 tipin abone karışımı ve abone başına büyüklük (Kıb-Tek yıllık tüketimi) şehir üreticisinde; bahar iş günü ve tatil günü.
- Sözleşmeyi yaz: [docs/data/tablo-bicimi.md](docs/data/tablo-bicimi.md). Civan ve Can baştan hepsine göre kurar: trafo tablosu, 5 dakikalık yük, cevap anahtarı, Faz 2 tahmin tablosu, Faz 3 kaç ev tablosu. Tip ve faz dağılımı Kıb-Tek'in bilmediği şeyler olduğu için trafo tablosunda değil cevap anahtarında.
- Rastgeleleştirme: tüketim ±%20, saat kayması ±30–60 dk, panel yaygınlığı %3–25 ([ADR-0006](docs/decisions/adr-0006-panel-yayginligi-bugunun-kibrisi.md); ilk taslak %10–50 idi), hava yılı 2024/2025, trafo çıkışı 246–250 V, faz dağılımı.
- Cevap anahtarı: öğlen (11–14) en düşük yük (iş günü ve tatil) + ev ev benzetimle gerçek "kaç ev sığar" (259 V; ev başına 6,5 kW: bekleyen başvurular 5–8 kW, orta değer; eski benzetim kendi içinde 5 kW kullanır).
- README'de komut; günlük.

Geçme sınavı:
- [x] 40 trafolu şehir ≤ 60 saniyede üretiliyor; aynı tohum aynı şehri veriyor (iki çalıştırma birebir). En uzun 16,1 sn (Mac); tohum: [can-faz1](docs/log/2026-10-31-can-faz1.md); [docs/log/2026-10-31-volkan-faz1.md](docs/log/2026-10-31-volkan-faz1.md)
- [x] Veri sağlaması: konut öğlen/akşam oranı 0,6–0,8; çarşı tepesi 11–14 arasında; otel Temmuz/Ocak 3–5×; çarşı Nisan tatil öğleni / iş günü öğleni 0,6–0,9 (EAC'de pazar ayrı yok; karar masası 31 Ekim; ilk taslak "pazar günü yarısından az" idi). 5/5: [docs/log/2026-10-31-volkan-faz1.md](docs/log/2026-10-31-volkan-faz1.md)
- [x] 7 tipin 7'si en az 3 trafoda var; 20 şehirde her tipten ≥ 60 trafo. En az sanayi 73: [docs/log/2026-10-31-volkan-faz1.md](docs/log/2026-10-31-volkan-faz1.md)
- [~] En az bir trafo bugün 259 V üstü (yöntemin görecek bir şeyi var); hiçbir trafo 216 V altı değil (benzetim bozuk değil). 259 V üstü 119/800 geçti; 216 V altı 3 trafo (en düşük 211,4 V, otel / uzun köy hattı / sanayi) → eşik karar masasında, Faz 2'yi bloklamıyor: [docs/log/2026-10-31-volkan-faz1.md](docs/log/2026-10-31-volkan-faz1.md)
- [x] Windows'ta çalıştı ve çıktı UTF-8 (Can onayı): [can-faz1](docs/log/2026-10-31-can-faz1.md)
- [x] Veri adımı: her aday için veri sözlüğünde satır ya da "elendi + neden"; indirilenlerin KAYNAK.txt'si eksiksiz: [veri sözlüğü](docs/data/data-dictionary.md), [can-faz1-veri](docs/log/2026-10-31-can-faz1-veri.md)

## Faz 2 — Modeli eğitme ve sınama: ölçülü trafolardan öğrenip ölçülmeyen trafonun öğlen yükünü tahmin etmek (sürüyor)

**Amaç:** Ölçülmeyen trafonun bahar öğleni en düşük yükünü bant ve güvenle tahmin etmek (ADR-0001).
**Girdi:** Faz 1 şehirleri. **Çıktı:** `src/sablon.py` ve şehir başına sonuç tablosu.
**Kim / süre:** üçü paralel · uzun.
**Paralel işler ve dosyalar:**
- Volkan+Claude → `src/sablon.py` (2a–2g: model ve bant), `docs/method/`, `docs/log/…-volkan-faz2.md`.
- Can → `src/sinav.py` (2h dahil): tahmin tablosu + cevap anahtarını alır, geçme sınavındaki her ölçüyü hesaplar (doğru arketip oranı, öğlen hata ortanca/P90, bant kapsama, şehirler arası fark, düşük güven oranı); `src/grafikler.py`: kalibrasyon ve "kaç trafo ölçmeli" grafikleri; + gerçek veri adayları (İspanya EDP, NGED) inceleme ve KAYNAK; `docs/log/…-can-faz2.md`. Modeli yazan sınavı yazmaz.
- Civan → `app/harita.py` yan panel ve tıklama (sahte veriyle).
- Kartlar: [Can](docs/gorev/can-faz2-sinav-grafikler.md); Civan Faz 1 kartının sonundaki Faz 2 notu.

Yapılacaklar — veri (Can yapar, Volkan onaylar; gerçek doğrulama adayları, aynı eleme). İstisna: NGED kaydını Volkan açar (hesap onun):
- İspanya EDP gerçek şebeke (Mendeley, CC BY): trafo başına toplam yük çıkıyor mu, çözünürlük, abone tipi.
- İngiltere NGED "LV Load Monitor Data" (301 gerçek trafo; kayıt gerekiyor, Volkan açar).

Yapılacaklar — kod (her biri bir görev; eğitim akışı: veri hazırla → öğretici trafoları seç → öğren → sına → belirsizlik):
- 2a Eğitim verisi hazırlama (özellik tablosu): yalnız Kıb-Tek'in bileceği sütunlar (kVA, sınıf başına abone, panel sayısı, bölge tipi, hat sayısı ve uzunluğu). Gerçek yük asla girdi değil.
- 2b Öğretici küme (ölçülecek trafolar) seçimi: tabakalı (tip × kVA × bölge), 40'tan 10–15; sonra 5 / 10 / 20 ile tekrar.
- 2c Eğitim 1, kümeleme (şekil): bahar iş günü eğrisi tepesine bölünür; hiyerarşik + k-means; küme sayısı siluet/dirsek ile; kümelere isim.
- 2d Eğitim 2, atama modeli: çok sınıflı lojistik regresyon, çapraz doğrulama; sütun çıkararak "hangi veri en çok işe yarıyor".
- 2e Eğitim 3, ölçekleme modeli: küme başına negatif olmayan regresyon, hedef öğlen en düşük yük; katsayılar yorumlanabilir.
- 2f Sınama ve bant: bir-dışarıda artıklarından P10–P90; kalibrasyon grafiği.
- 2g Güven etiketi: özellik uzaklığı + atama olasılığı → yüksek / orta / düşük.
- 2h Sınama 2, şehirler arası; "kaç trafo ölçmeli" eğrisi.
- 2i Bonus (kısa zaman kutusu; olmazsa bırakılır): İspanya ya da NGED gerçek verisi.
- Not: modeller bilerek küçük ve yorumlanabilir (ADR-0001); derin öğrenme kapsam dışı.

Geçme sınavı (20–30 şehirde, [doğrulama protokolüyle](docs/method/validation.md); her ölçü ortanca ve en kötü şehir):
- [ ] Doğru arketip oranı ortanca ≥ %75 (İngiltere ~%80 ile kıyas; "gösterim").
- [ ] Öğlen en düşük yük hatası ortanca ≤ %15, P90 ≤ %30.
- [ ] %80 bandın gerçek kapsama oranı %70–90 arasında (sahte güven yok).
- [ ] Şehirler arası sınav (A'da kur, B'de dene) hatası şehir içi hatanın 1,5 katını geçmiyor.
- [ ] Ölçülü ve ölçülmeyen trafoların tip dağılımı karşılaştırılmış, günlükte.
- [ ] "Düşük güven" oranı raporlandı (hedef ≤ %25; aşarsa sebep günlükte).
- [ ] 5 / 10 / 20 ölçülü trafo eğrisi çizildi, "gösterim" etiketli.

## Faz 3 — İlk uygulama katmanı, güneş paneli: her trafo için kaç ev daha, aralık ve yeşil/sarı/kırmızı karar

**Amaç:** Her trafo için kaç ev daha, karamsar/iyimser aralık, triyaj rengi (ADR-0002, ADR-0005).
**Girdi:** Faz 2 tahminleri ve bantları; trafo kVA, hat boyu, iletken, mevcut panel. **Çıktı:** `src/kac_ev.py`; trafo tablosu + karşılaştırma raporu.
**Kim / süre:** üçü paralel · orta.
**Paralel işler ve dosyalar:**
- Volkan+Claude → `src/kac_ev.py`, `docs/log/…-volkan-faz3.md`.
- Can → `src/sinav.py`'ye Faz 3 ölçüleri (yanlış yeşil, yanlış kırmızı, kaç ev hatası, sarı oranı) ve %40 kuralı karşılaştırması; `src/grafikler.py`'ye kilit grafik (biz vs %40 kuralı); `docs/log/…-can-faz3.md`.
- Civan → `app/harita.py`'yi gerçek Faz 3 tablosuna bağlar.

Yapılacaklar:
- Isıl sınır ve gerilim sınırı, küçüğü; yanında %40 kuralının sonucu.
- İki senaryo: karamsar (P10 yük, tek faz, 250 V) ve iyimser (P90 yük, dengeli üç faz, 246 V).
- Renk kuralı: yeşil = karamsarda bile yer var ve güven yüksek; kırmızı = iyimserde bile yok; diğerleri sarı (ölç ya da esnek onay). "Ölçülmedi" etiketi.
- Benzetimdeki gerçek "kaç ev" ile karşılaştırma; %40 kuralıyla aynı karşılaştırma.

Geçme sınavı (20–30 şehirde):
- [ ] **Yanlış yeşil oranı ≤ %5** (dolu trafoya "yer var"); en kötü şehirde ≤ %10.
- [ ] %40 kuralının yanlış yeşil oranı aynı şehirlerde hesaplanmış ve yan yana (sunumun kilit grafiği).
- [ ] Yanlış kırmızı oranı raporlandı (hedef ≤ %20).
- [ ] Kaç ev hatası ortanca ≤ 2 ev.
- [ ] Sarı oranı raporlandı (hedef ≤ %30; aşarsa sebep günlükte).

## Faz 4 — Ürün, trafo görünürlük haritası: Kıb-Tek'in göremediği trafoları tıklanır bir haritada göstermek

**Amaç:** Jürinin tıklayıp göreceği canlı panel. **Girdi:** Faz 1 tablo biçimi (sahte veriyle başlar), Faz 3 tablosu, kasaba haritası. **Çıktı:** `app/harita.py` (Streamlit + pydeck).
**Kim / süre:** Civan yapar, Claude yardım eder · uzun, ama Faz 1–3'e paralel; iskelet erken, son hali gerçek tablo gelince.
**Dosyalar:** Civan → `app/harita.py`, `app/ornek_veri.py`, `app/README.md`, `data/raw/osm-kasaba/KAYNAK.txt`, `docs/log/…-civan-harita.md`. Başka dosyaya dokunmaz; tablo biçimi değişikliği gerekirse Volkan'a söyler. Faz 1–3 boyunca sahte veriyle ilerler, Faz 3 bitince gerçek tabloya bağlanır.

Yapılacaklar — veri (Civan, kendi fazı için): gerçek bir KKTC kasabasının sokak ve bina haritası (OpenStreetMap, ODbL; aday Lapta ya da Girne'den bir mahalle), KAYNAK.txt ile.

Yapılacaklar — kod:
- 4a Tabloyu harita biçimine çevirme (koordinat, renk, boy, yan panel verisi).
- 4b Harita, 3D sütunlar, tıklama.
- 4c Yan panel: öğlen eğrisi + bant, kaç ev (aralık), güven, "ölçülmedi", %40 kuralının dediği.
- 4d Üst şerit: açılabilecek başvuru, MW, yılda yakıt; "örnek veri — gösterim" etiketi; kaynak listesi.
- 4e İnternetsiz görünüm, Windows/Mac, ekran kaydı.
- İsteğe bağlı: tıklanan trafonun sonucunu düz Türkçeyle anlatan açıklama katmanı (dil modeli; ambalaj, asıl değer değil).

Geçme sınavı:
- [ ] Tıklama ile yan panel ≤ 1 saniyede açılıyor; 40 trafoda takılma yok.
- [ ] Yan paneldeki sayılar Faz 3 tablosuyla birebir (3 trafo elle kontrol).
- [ ] İnternet kapalıyken açılıyor; 2 dakikalık ekran kaydı var.
- [ ] Windows ve Mac'te çalıştı; README'de komut.
- [ ] En az 3 şehir seçilebiliyor; "örnek veri" etiketi her ekranda.

## Faz 5 — Sunum ve prova: hikâye, canlı gösteri, itirazlara hazır cevap

**Amaç:** 5–7 dakikada hikâye + canlı gösteri + itirazlara hazır cevap. **Girdi:** Faz 3 grafikleri, Faz 4 paneli, [araştırma](docs/log/2026-10-31-kapsamli-arastirma.md) bölüm 8. **Çıktı:** slaytlar (PDF yedek), konuşma notu, soru-cevap.
**Kim / süre:** en son, Faz 3 ve 4 bittikten sonra, hep birlikte; Volkan anlatır · orta (2 prova dahil).
**Dosyalar:** `docs/sunum/` (Can açar; slaytlar ve konuşma notu).

Yapılacaklar:
- Akış: Güney %47'sini atıyor → Kuzey'de 2.670 bekliyor, Kıb-Tek mahalleyi görmüyor → İngiltere 800 trafo, %80 → bizim uyarlama (öğlen + gerilim, Kıbrıs'a özel; **fotoğraf değil film**: bugün kurulumcu gerilimi tek noktada, tek gün ölçüyor, komşular panel ekledikçe baharda sınır aşılıyor ve kimse önceden görmüyor; biz trafonun gün ve mevsim boyu davranışını tahmin edip "kaç ev daha ekleyince sınıra gelir" sorusuna önceden cevap veriyoruz) → canlı harita → %40 kuralıyla yan yana yanlış yeşil → pilot (20–50 → 120–170 trafo, ~20 bin € + pens, baharda) → itirazlar ve triyaj.
- Dürüstlük cümleleri: "%80 İngiltere'de gerçek veride; farazi şehir gösterim; Kıbrıs'taki doğruluğu pilot söyler." + temsil yanlılığı: "Ölçülen trafolar yereldir; her tipten örnek yoksa model görmediği tipte kendinden emin yanlış tahmin yapar. Tabakalı seçim, ölçülü/ölçülmeyen dağılım karşılaştırması ve düşük güven etiketiyle bunu sınırlıyoruz, tamamen kaldırmıyoruz."
- İtiraz slaydı (adalet, yanlış evet/hayır maliyeti, hesap verebilirlik, komşu etkisi, zamanla bozulma) → ret değil triyaj, insan onayı, itiraz eden ölçüm ister.
- Kaynak slaydı; PDF ve ekran kaydı yedeği.

Geçme sınavı:
- [ ] 2 prova yapıldı, ikisi de ≤ 7 dakika.
- [ ] 8 jüri sorusuna ekipten en az iki kişi anlatarak cevap verdi.
- [ ] Dürüstlük cümleleri konuşma notunda ve provada söylendi.
- [ ] Her rakamın slaytta kaynağı ya da etiketi var (rakam sayısı = etiket sayısı).
- [ ] Yedekler açıldı ve çalıştı.
