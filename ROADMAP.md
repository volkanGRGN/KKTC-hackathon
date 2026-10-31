# Yol haritası

**MVP nedir:** Kıb-Tek'in bugün göremediği mahalle trafolarını, az sayıda ölçümden öğrenen bir modelle **haritada görünür kılmak**. Her trafo için iki çıktı: **trafo ne kadar dolu** (yılın en yüksek saati, kVA, saatiyle) ve **güneş için ne kadar yer var** (bahar öğleni; panel katmanı veri geldikçe açılır). İki soru bağımsız: biri yılın en yüksek yükünde trafo gücü ve akşam gerilim düşümü (207 V), öteki bahar öğleninde gerilim yükselmesi (259 V); panel akşam tepesini düşürmez. **Yük temel katman:** Kıb-Tek'in kendi verisiyle (fatura, abone) kalibre edilebilen ve bütün trafoları kapsayan o (Faz 11). **Panel katmanı güvenli uçlarla** (kesin dolu için uyarı, kesin yeşil azınlık; belirsiz olan başvuru anında bakılır; Muhittin 4, ADR karar masasında) ve Kıb-Tek'in ağ / faz / kademe kayıtları geldikçe açılır; güvenilir olana kadar sunumda anlatılmaz (karar masası 23:12).

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
- [x] En az bir trafo bugün 259 V üstü (yöntemin görecek bir şeyi var); hiçbir trafo 207 V altı değil (benzetim bozuk değil). Eşik 207 V (EN 50160 alt sınır; karar masası 31 Ekim; ilk taslak 216). 259 V üstü 119/800 geçti; 207 V altı 0/800 (216 V altı 3 trafo, en düşük 211,4 V, bulgu olarak günlükte): [docs/log/2026-10-31-volkan-faz1.md](docs/log/2026-10-31-volkan-faz1.md)
  - **Ölçüt değişti (ADR-0016, karar masası 22:2x):** 207 V altındaki trafo payı ≤ %1 ve en düşük ≥ 200 V (EN 50160 zamanın %95'i; 800 m tek hatlı köyde akşam 206 V gerçekçi). Üretici 1.3 sınav 21–30: 1/400 (%0,25), en düşük 205,9 V → geçer. kVA boyutlandırması bunu gizlemek için değişmez.
- [x] Windows'ta çalıştı ve çıktı UTF-8 (Can onayı): [can-faz1](docs/log/2026-10-31-can-faz1.md)
- [x] Veri adımı: her aday için veri sözlüğünde satır ya da "elendi + neden"; indirilenlerin KAYNAK.txt'si eksiksiz: [veri sözlüğü](docs/data/data-dictionary.md), [can-faz1-veri](docs/log/2026-10-31-can-faz1-veri.md)

## Faz 2 — Modeli eğitme ve sınama: ölçülü trafolardan öğrenip ölçülmeyen trafonun öğlen yükünü tahmin etmek (bitti 31 Ekim, faturalı)

**Amaç:** Ölçülmeyen trafonun bahar öğleni en düşük yükünü bant ve güvenle tahmin etmek (ADR-0001).
**Girdi:** Faz 1 şehirleri. **Çıktı:** `src/sablon.py` ve şehir başına sonuç tablosu.
**Kim / süre:** üçü paralel · uzun.
**Paralel işler ve dosyalar:**
- Volkan+Claude → `src/sablon.py` (2a–2g: model ve bant), `docs/method/`, `docs/log/…-volkan-faz2.md`.
- Can → `src/sinav.py` (2h dahil): tahmin tablosu + cevap anahtarını alır, geçme sınavındaki her ölçüyü hesaplar (doğru arketip oranı, öğlen hata ortanca/P90, bant kapsama, şehirler arası fark, düşük güven oranı); `src/grafikler.py`: kalibrasyon ve "kaç trafo ölçmeli" grafikleri; + gerçek veri adayları (İspanya EDP, NGED) inceleme ve KAYNAK; `docs/log/…-can-faz2.md`. Modeli yazan sınavı yazmaz.
- Civan → `app/harita.py` yan panel ve tıklama (sahte veriyle).
- Kartlar: [Can](docs/gorev/can-faz2-sinav-grafikler.md); Civan Faz 1 kartının sonundaki Faz 2 notu.
- **Durum (17:42):** bitti, faturalı. Model (#8) ve üretici 1.2 + fatura (#12) main'de; resmi ölçüm Can'ın `sinav.py faz2`'si (#14), 7/7 GEÇTİ. Ayrıntı: [üretici 1.2 günlüğü](docs/log/2026-10-31-volkan-uretici-1-2.md), [can-faz2](docs/log/2026-10-31-can-faz2.md).

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
- [x] Doğru arketip oranı ortanca ≥ %75 (İngiltere ~%80 ile kıyas; "gösterim"). Sınav 11–20: %98,2, en kötü %89,3: [can-faz2](docs/log/2026-10-31-can-faz2.md)
- [x] Öğlen en düşük yük hatası ortanca ≤ %15, P90 ≤ %30. Faturalı %3,8 / %8,0 (en kötü şehir %5,1 / %9,5); saf tahmin (fatura) %5,5 / %15,2, model %31 / %48 iyi: [can-faz2](docs/log/2026-10-31-can-faz2.md)
- [x] %80 bandın gerçek kapsama oranı %70–90 arasında (sahte güven yok). **Faz 7'den beri kapı gerçek veride** (karar masası 21:51; tüzük madde 3): İspanya, 29 trafo, bir-dışarıda %79 (PR #16). Farazi 11–20'de %96 (bilgi; üretici Faz 8'de gerçeğe çapalanınca yeniden). v1: farazi %87,5 (simetrik bant), İspanya %66: [can-faz2](docs/log/2026-10-31-can-faz2.md), [1.2 günlüğü](docs/log/2026-10-31-volkan-uretici-1-2.md)
- [x] Şehirler arası sınav (A'da kur, B'de dene) hatası şehir içi hatanın 1,5 katını geçmiyor. Ortanca 1,08; en kötü 1,81, 2 şehir 1,5 üstünde (payda küçük: şehir içi hata %3–4): [can-faz2](docs/log/2026-10-31-can-faz2.md)
- [x] Ölçülü ve ölçülmeyen trafoların tip dağılımı karşılaştırılmış, günlükte. Uzaklık (TV) ortanca 0,21: [can-faz2](docs/log/2026-10-31-can-faz2.md)
- [x] "Düşük güven" oranı raporlandı (hedef ≤ %25; aşarsa sebep günlükte). Faturalı %0; faturasız %100 (fatura yoksa büyüklük ±%30 bilinmez): [can-faz2](docs/log/2026-10-31-can-faz2.md)
- [x] 5 / 10 / 20 ölçülü trafo eğrisi çizildi, "gösterim" etiketli. 5 / 10 / 12 / 20 ölçülü → hata %4,6 / %3,8 / %4,1 / %3,5: faturalı modelde ölçülü sayısı hatayı az değiştiriyor (İspanya'yla aynı yön): `outputs/faz2_kac_trafo.png`, [can-faz2](docs/log/2026-10-31-can-faz2.md)
- **Bilgi (karar masası 17:38):** fatura olmadan model, saf tahmini ortancada geçmiyor. Sınav 11–20 faturasız %20,6 / %50,7; tarife saf tahmini %22,9 / %62,2; model yalnız %10 / %19 iyi. Kazanç kötü uçta (P90). Faz 2 faturayla geçti (ADR-0007 faturayı girdi yaptı); Kıb-Tek'ten fatura toplamı istemenin kanıtı.
- **Saf fatura kıyası bilgi satırı (ADR-0016):** öğlen yükünün büyüklüğünü fatura söyler. Üretici 1.3 sınav 21–30: model %12,2 / %27,0 ↔ saf fatura %13,4 / %28,5 (model %9 / %5 iyi). İspanya: faturalı model saf fatura kıyasıyla birebir (10 ölçülü %10,9 / %32,3; 15 ölçülü %10,3 / %33,1; abone sınıfı yok, tek sütun). Modelin değeri bant, güven ve panel kararı.

## Faz 3 — İlk uygulama katmanı, güneş paneli: her trafo için kaç ev daha, aralık ve yeşil/sarı/kırmızı karar (bitti 31 Ekim, gösterim; açık eksikler pilotta)

**Amaç:** Her trafo için kaç ev daha, karamsar/iyimser aralık, triyaj rengi (ADR-0002, ADR-0005).
**Girdi:** Faz 2 tahminleri ve bantları; trafo kVA, hat boyu, iletken, mevcut panel. **Çıktı:** `src/kac_ev_olasilik.py` (resmi, ADR-0011; `src/kac_ev.py` yedek); trafo tablosu + karşılaştırma raporu.
**Kim / süre:** üçü paralel · orta.
**Paralel işler ve dosyalar:**
- Volkan+Claude → `src/kac_ev.py`, `docs/log/…-volkan-faz3.md`.
- Can → `src/sinav.py`'ye Faz 3 ölçüleri (yanlış yeşil, yanlış kırmızı, kaç ev hatası, sarı oranı) ve %40 kuralı karşılaştırması; `src/grafikler.py`'ye kilit grafik (biz vs %40 kuralı); `docs/log/…-can-faz3.md`.
- Civan → `app/harita.py`'yi gerçek Faz 3 tablosuna bağlar.
- Kartlar: [Can](docs/gorev/can-faz3-sinav-grafik.md), [Civan](docs/gorev/civan-faz3-yan-panel.md).
- **Durum (31 Ekim 19:51, Faz 3 kapandı; Volkan).**
  - Resmi hesap olasılıklı ([ADR-0011](docs/decisions/adr-0011-faz3-olasilikli-hesap.md)): `src/kac_ev_olasilik.py`, `kac_ev.csv` sözleşme 1.3. Tek denklem `src/kac_ev.py` yedek.
  - Resmi ölçüm: karar masası koşumu (Mac, 31 Ekim 19:35–19:50; main fe7426b + `sinav.py` c3fb046; 20 şehir sıfırdan). Can'ın #15 deneme koşusuyla birebir. Çıktılar [Faz 3 günlüğünde](docs/log/2026-10-31-volkan-faz3.md).
  - Ayrıntı: [olasılıklı hesap](docs/log/2026-10-31-volkan-faz3-olasilik.md), [varsayım envanteri](docs/log/2026-10-31-volkan-faz3-varsayimlar.md), [İngiltere geri-testi](docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md).

Yapılacaklar:
- Isıl sınır ve gerilim sınırı, küçüğü; yanında %40 kuralının sonucu.
- İki senaryo: karamsar (P10 yük, tek faz, 250 V, bekleyen paneller hattın ucunda: İngiltere UKPN, karar masası 16:27) ve iyimser (P90 yük, dengeli üç faz, 246 V, hat ortası).
- Renk kuralı ([ADR-0010](docs/decisions/adr-0010-yesil-karari-marj-guven-kumulatif.md)): yeşil = karamsar senaryo bekleyen evi marjla alıyor (payın %10'u, en az 1 ev) ve güven yüksek; kırmızı = karamsar sınırı aşıyor (okuması karar masasında); diğerleri sarı (sınırlı onay ya da önce ölçüm; ölçüm cihazı sarılara). İlk taslakta kırmızı "iyimserde bile yok" idi. "Ölçülmedi" etiketi.
- Benzetimdeki gerçek "kaç ev" ile karşılaştırma; %40 kuralıyla aynı karşılaştırma.

- **Faz 3 ikinci sürüm (kalemler; plan olarak Faz 6–12; karar masası 17:00, ADR-0009, ADR-0010):**
  - kümülatif onay düşümü (`kac_ev.csv`'ye `onaylanan_kw`, `kalan_ev`; sözleşme 1.3);
  - **başvuru anında karar** ([ADR-0012](docs/decisions/adr-0012-sari-trafoda-karar-basvuru-aninda.md), kabul, sınanmadı): sarı trafoda onay, aynı hesap başvuranın hattaki yerine ve fazına konarak o ev için bir kez daha koşar (evet / önce ölç / hayır); her onay paydan düşülür (kümülatif düşümün yeri). Farazi şehirde ölçü: başvuru anı kararında yanlış evet oranı. Pilotta başvuru formuna hat / direk bilgisi (uzmana soru 2–4);
  - yeşil kuralının İspanya / İngiltere geri-testi ve canlı bütçe (yanlış yeşil < %2);
  - **dış sınama adayları** (karar masası 20:47): İngiltere UKPN 6 hat (yapıldı, 5/6); Malta Gozo tek hat (Srug F1: 500 kVA, 11 kV / 433 V, 18 panelsiz ev, +1 kWp/ev kademe, +2 kWp/ev trafo değişimi; hat boyu, kablo ve ev sayısı bilinmiyor; Faz 7'de aralıkla koşuldu, **tutmadı**: makalenin dört sonucunu birden tutan çekiliş 1/400; sebep öğlen bara gerilimi ve panel dağılımı bilinmiyor; olumsuz sonuç olarak kayıtlı (PR #17, [günlük](docs/log/2026-11-01-volkan-faz7-gozo.md)); Micallef tezi gelirse tek tahminle yeniden; [ada ülkeleri günlüğü](docs/log/2026-10-31-volkan-ada-ulkeleri.md));
  - üretici 1.3 çapaları: korelasyon matrisi, P90/P95 kuyruk, hat üstünde PV konum dağılımı ve fazı, trafo içi çeşitlilik (Can'ın `edp_kiyas.py`'si);
  - "farazi − İspanya" fark ölçeri her sürümde.
  - Fatura dağılım sütunları (yüksek tüketen abone oranı, mevsimsellik; ADR-0009 madde 1a): sözleşme 1.3 adayı. Sözleşme 1.2'deki `yillik_tuketim_mwh` kalır.
  - **Üretici 1.3** (karar masası 17:26; plan olarak Faz 8):
    - trafo güç listesi: ASTOR kataloğu (2020; Elparts'ın sattığı marka) yağlı dağıtım trafosunu 50–5000 kVA, kompakt trafo merkezini 1000 / 1600 kVA veriyor. Listedeki 25 kVA kaynaksız: kaynak bulunmazsa liste 50'den başlar; yaz benzetilirse yer tipine 1600. Kademe değiştirici var, adımı BULAMADIM (uzmana soru 8);
    - öğlen orta gerilim değişimi şehir başına −%0,4…+%0,8 aralığından (bugün sabit +%0,8; UKPN'de öğlen bara geceden ~1 V düşük; karar masası 18:46, varsayım envanteri K2). Sınav şehirleri bu gece donuk;
    - panelli evde `yillik_tuketim_mwh` net yazılır (mahsuplaşma), model `panel_kw` × yıllık üretimle (≈ 1.600 kWh/kWp [Yorum]) düzeltir; uzmana soru 7;
    - ince uç kol senaryosu (karar masası 21:16, Civan'ın ada veri setleri bulgusu): uç kollarda 16–22 mm² havai iletken (Rac 1,23–1,91 Ω/km); olasılıklı hesabın kol çekilişine (ADR-0011 kol yapısı) ince iletkenle girer [Kaynaklı: Kotsonias vd. (KIOS + EAC), ISGT-Europe 2019, Zenodo 10.5281/zenodo.3561929, CC BY 4.0]. Kıb-Tek'in kesiti uzmana soru 3;
    - trafo boyutu çapası (karar masası 20:47): Malta en yüksek talep ÷ güç P10/50/90 0,13 / 0,42 / 0,74 (yılın tepesi, 1.331 trafo merkezi [Hesap: Enemalta kapasite haritası verisi, 31 Ekim; ham veri depoda yok]); bizim Nisan tepesi ÷ kVA 0,16 / 0,27 / 0,47. Kıyas için Nisan / yıl tepe oranı EAC profillerinden türetilir; bugünkü "gerek × 1,2–2,0" [Yorum] buna göre;
    - abone başına eğri farkı: aynı tarifede öğlen ÷ yıllık oranı abone abone dağılsın (ADR-0009 trafo içi çeşitlilik). Bugün farazi faturalı %3,9 üst sınır, İspanya'da faturayla %10.

Geçme sınavı (20–30 şehirde):
Rakamlar sınav şehirleri 11–20 (347 trafo, 73 dolu), karar masası koşumu; 1–20 bilgi satırları günlükte.
- [x] **Yanlış yeşil oranı ≤ %5** (dolu trafoya "yer var"); en kötü şehirde ≤ %10. — **0/87**, en kötü şehir 0/12; dolu trafoya yeşil 0/73.
- [x] %40 kuralının yanlış yeşil oranı aynı şehirlerde hesaplanmış ve yan yana (sunumun kilit grafiği). — %40 kuralı 41/284 (%14,4); dolu trafoya "yer var": %40 kuralı 41/73, biz 0/73.
- [x] Yanlış kırmızı oranı raporlandı (hedef ≤ %20). — %27,3 (12/44), **hedef üstü**; sebep bilgi eksikliği (aşağıda "Açık eksikler" 1).
  - **Ölçü değişti (ADR-0016):** yanlış kırmızı bir kalibrasyon ölçüsü; "≤ %20" kalkar. Ölçü: kırmızı kovasında gerçekte bugün aşan pay ≥ 0,5 − 2·√(0,25 ÷ n), n = kırmızı trafo sayısı (karar masası 22:3x); olasılık kovalarının yönü bilgi. Üretici 1.3 sınav 21–30: n = 61, sınır %37, kırmızıların %49'u gerçekte aşıyor → **geçer**; geliştirme 1–10 %55. Yön karamsar: 0,5–0,7 → %34, 0,7–0,9 → %68 (Faz 8 günlüğü); Faz 10'da pilot verisiyle yeniden.
- [x] Kaç ev hatası ortanca ≤ 2 ev. — orta 2 ev (karamsar 2, iyimser 4; n 239, tavanlı 108 ayrı).
- [x] Sarı oranı raporlandı (hedef ≤ %30; aşarsa sebep günlükte). — %62,2 (216/347), **hedef üstü**; sebep aşağıda "Açık eksikler" 2.

**Açık eksikler** (karar masası 19:44; bu gece kapanmaz, pilotta). Rakamlar sınav 11–20.

| # | Eksik | Bu gece | Pilot / sunum sonrası |
|---|---|---|---|
| 1 | Yanlış kırmızı %27 (hedef ≤ %20) | Bilginin değeri denemesi ([günlük](docs/log/2026-10-31-volkan-faz3.md), üst sınır, farazi şehir): bara gerilimi bilinirse %19; bara + panelli evin yeri + faz bilinirse %4, dolu trafoyu kırmızı görme 32 → 43 (BUILD şehirlerinde 74 dolu). Madde "raporlandı" | Bara gerilimi (akıllı priz gece seviyesi, trafo plakası kademe); Kıb-Tek'ten panelli abonenin adresi ve fazı (uzmana soru 2, 4, 8) |
| 2 | Sarı %62 (hedef ≤ %30) | Yeşil eşiği 0,98 kalır (eşiğin bedeli tablosu günlükte: 0,80'de bile sarı %42, dolu trafoya "yer var" 3). Deneme: bilgi sarıyı az düşürür (üç bilgiyle %57, ağın tamamı ve yükle %41); kalan sarı "sıradaki başvuru kimden gelecek" belirsizliği | Ölçüm cihazı sarılara (asıl pilot); 1'deki bilgiler. Sarı trafoda karar başvuru anında, başvuranın adresi ve fazıyla: [ADR-0012](docs/decisions/adr-0012-sari-trafoda-karar-basvuru-aninda.md) (kabul, sınanmadı) |
| 3 | Yeşil bütçesi (%2) gerçek veride doğrulanmadı (İngiltere 6 hattın 5'i, Bancroft kaçtı) | İş yok; ekran 4 cümlesi hazır (Can) | Panelli evlerin inverter uygulamasındaki 5 dk gerilim kaydı (izinle) + sarıların hat ucunda öğlen gerilimi; her ölçülen hat geri-teste; kol yapısı (soru 3) |
| 4 | Olasılık düşük uçta iyimser (%10–30 diyene ~%43 aşıyor) | İş yok: sınav şehirleri donuk, gece yeniden üretim bütün rakamları değiştirir (ADR-0009). Not (bilginin değeri, S6): kusursuz bilgide bile hesap kendinden fazla emin: aralık kapsaması %80 → %57, ilk yanlış yeşil (1/166); kalan aralıklar (öğlen OG, tek an) üreticiden farklı | Üretici 1.3: OG aralığı, panellerin uca kayma dağılımı; sonra kalibrasyon yeniden; pilotta aralıklar ölçümle yeniden ayarlanır (ADR-0011 madde 5) |
| 5 | Kaç ev aralığı taban değil (P10 altı %15) | Çözüldü: dil 19:13 ("yaklaşık N ev (A–B)", "en az" yok), Can'ın bilgi satırı (c3fb046) | Üretici 1.3 ile yeniden ölç |
| 6 | Faturasız model basit tahmini geçmiyor (Faz 2) | İş yok | Kıb-Tek'ten trafo başına fatura toplamı = pilotun veri isteği (soru 7) |

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
- [ ] Tıklama ile yan panel ≤ 1 saniyede açılıyor; 40 trafoda takılma yok. — Mac (BUILD, 20:55): 6 tıklamada 0,35–0,40 sn; 40'ın hepsi denenmedi.
- [x] Yan paneldeki sayılar Faz 3 tablosuyla birebir (3 trafo elle kontrol). — Mac (BUILD, 20:55): 3 şehirde 6 trafo birebir; renk sayıları aynı. Dil 19:13 kararına göre değil ve %40 kuralının ev sayısı aday evden fazla çıkabiliyor (civan.md KONTROL 20:55).
- [ ] İnternet kapalıyken açılıyor; 2 dakikalık ekran kaydı var. — Zemin dosyasıyla dışarıya istek yok, iki platformda ölçüldü (Mac BUILD 20:55: 98/98 yerel; Windows Civan 21:29). Zemin dosyası depoda yok, sunum bilgisayarına indirilmeli. **Ekran kaydı 1 Kasım sabah provada** (Civan, yedek: sunum bilgisayarı çökerse PDF + kayıt); ağ fiilen kapalı deneme isteğe bağlı (karar masası 21:44). Ekran kaydı yok.
- [x] Windows ve Mac'te çalıştı; README'de komut. — Mac (BUILD 20:55, streamlit 1.66.1) ve Windows (Civan KONTROL 21:29); README'de komut ve sunum bilgisayarı satırı (karar masası 21:44).
- [x] En az 3 şehir seçilebiliyor; "örnek veri" etiketi her ekranda. — Mac (BUILD, 20:55): 001, 011, 020 seçildi; etiket her şehirde.

## Faz 5 — Sunum ve prova: hikâye, canlı gösteri, itirazlara hazır cevap

**Amaç:** 5–7 dakikada hikâye + canlı gösteri + itirazlara hazır cevap. **Girdi:** Faz 3 grafikleri, Faz 4 paneli, [araştırma](docs/log/2026-10-31-kapsamli-arastirma.md) bölüm 8. **Çıktı:** slaytlar (PDF yedek), konuşma notu, soru-cevap.
**Kim / süre:** başladı 31 Ekim akşam, Faz 3 ile paralel (karar masası 16:50); Volkan anlatır · orta (gece 2 prova).
**Dosyalar:** `docs/sunum/` (Can açar; slaytlar ve konuşma notu).

Yapılacaklar:
- **Hikâye: güven merdiveni** (karar masası 17:00, [ADR-0009](docs/decisions/adr-0009-dogruluk-onceligi-ve-capalama.md)).
  - Tek cümle: "Kıbrıs'ı ölçemiyoruz; yöntemi ölçebildiğimiz her şeyde kanıtlıyoruz, sonra uyguluyoruz."
  - Dört basamak, her birine tek iddia + tek rakam, hepsi "saf tahmine göre ne kadar iyi" cinsinden:
    1. farazi şehir (kontrollü gerçek);
    2. İspanya (yük, dış geçerlilik);
    3. İngiltere (gerilim, dış geçerlilik);
    4. Kıbrıs pilotu (saha).
  - **Manşet rakam: İspanya %25 → %10** ("hiç görmediğimiz 29 gerçek trafoda, Kıb-Tek'in zaten elinde olan abone sayısı + faturayla").
  - İkinci vurgu: gerilimde İngiltere'nin 6 gerçek hattının 5'inde ölçülen yükselme olasılıklı hesabın güvenli sınırının altında; birinde küçük gördük → canlıda yeşil önce pilotla sınanır (karar masası 18:46, ADR-0011).
  - Farazi rakamlar destek, manşet değil. Farazi 1.2'de faturasız %22, faturalı %3,9 (iyimser üst sınır).
  - Kilit grafik: yanlış yeşil, biz 0 / %40 kuralı %14.
- Akış (eski taslak, merdivene yerleşir): Güney %47'sini atıyor → Kuzey'de 2.670 bekliyor, Kıb-Tek mahalleyi görmüyor → İngiltere 800 trafo, %80 → bizim uyarlama (öğlen + gerilim, Kıbrıs'a özel; **fotoğraf değil film**: bugün kurulumcu gerilimi tek noktada, tek gün ölçüyor, komşular panel ekledikçe baharda sınır aşılıyor ve kimse önceden görmüyor; biz trafonun gün ve mevsim boyu davranışını tahmin edip "kaç ev daha ekleyince sınıra gelir" sorusuna önceden cevap veriyoruz) → canlı harita → %40 kuralıyla yan yana yanlış yeşil → pilot (20–50 → 120–170 trafo, ~20 bin € + pens, baharda) → itirazlar ve triyaj.
- Dürüstlük cümleleri: "%80 İngiltere'de gerçek veride; farazi şehir gösterim; Kıbrıs'taki doğruluğu pilot söyler." + temsil yanlılığı: "Ölçülen trafolar yereldir; her tipten örnek yoksa model görmediği tipte kendinden emin yanlış tahmin yapar. Tabakalı seçim, ölçülü/ölçülmeyen dağılım karşılaştırması ve düşük güven etiketiyle bunu sınırlıyoruz, tamamen kaldırmıyoruz." + gerçek veri ([ADR-0008](docs/decisions/adr-0008-farazi-cesitlilik-saf-tahmin.md) madde 3): "Farazi şehir isabeti gerçek isabetin üst sınırıdır. Gerçek veride, İspanya'da 29 trafoda sınadık: yalnız müşteri sayısıyla ~%25, fatura bilgisiyle ~%10 ortanca hata. Kıbrıs'taki doğruluğu pilot söyler." + gerilim (karar masası 16:27): "Gerilim fiziğini İngiltere'de 6 gerçek hatta sınadık: dördünde ±%40 içinde, ikisinde paneller hat ucunda toplandığı için model yükselmeyi az gösterdi; bu yüzden karamsar senaryomuz panelleri hattın ucuna koyar."
- İtiraz slaydı (adalet, yanlış evet/hayır maliyeti, hesap verebilirlik, komşu etkisi, zamanla bozulma) → ret değil triyaj, insan onayı, itiraz eden ölçüm ister.
- Kaynak slaydı (UKPN "Validation of PV Connection Assessment Tool" kapanış raporu, Ofgem, Mart 2015: bara gerilimi 248 V tasarım varsayımı, gündüz en düşük talep 200–400 W/müşteri, faz dengesizliği kentsel %25 / kırsal %50; [Faz 1 günlüğü](docs/log/2026-10-31-volkan-faz1.md) dış çapa); PDF ve ekran kaydı yedeği.

Geçme sınavı:
- [ ] 2 prova yapıldı, ikisi de ≤ 7 dakika.
- [ ] 8 jüri sorusuna ekipten en az iki kişi anlatarak cevap verdi.
- [ ] Dürüstlük cümleleri konuşma notunda ve provada söylendi.
- [ ] Her rakamın slaytta kaynağı ya da etiketi var (rakam sayısı = etiket sayısı).
- [ ] Yedekler açıldı ve çalıştı.

## Faz 6–12 — Modeli gerçek veriyle iyileştirme (başladı 31 Ekim gece; sunum 1 Kasım bir kilometre taşı, `sunum-v1` yedek)

Karar masası 21:15, 21:20, 21:25; Volkan 21:39: "sunum sonrası" ertelemesi kalktı, fazlar şimdi başlıyor. **Kim:** Volkan + Can model ve sınav, Civan harita ve veri araştırması ([kartı](docs/gorev/civan-veri-arastirma.md)). Her adım dalda + PR; tüzük kapıları her PR'da; sunum metni PR'lar birleşip Can resmi koştukça güncellenir, hikâye aynı. Eksi bulgulu PR karar masasında test edilir, düzelmeden birleşmez (Volkan, 21:46).
**Durum (31 Ekim 23:15):** Faz 7 (PR #16) ve Faz 8 (PR #18, içinde PV açılma denemesi PR #20) main'de, Can'ın 21–30 puanlaması ve karar masasının Mac koşumuyla; resmi rakamlar v3 (gerçekçi şehirler), sunum sürümü (v1 / v3) Volkan'da. Gozo dış sınaması main'de (PR #17; sonuç olumsuz / belirsiz, tez verisi beklenir, [günlük](docs/log/2026-11-01-volkan-faz7-gozo.md)). Açık PR'lar: #19 (Faz 10 hazırlığı), #21 (üretici 1.4 yıl boyu tepe; Can'a devredildi, Civan'ın sözleşme onayını bekliyor), #22 (başvuru anı motoru + sahte kayıtlar; karar masasının testinde).
**Sıra ve iş bölümü (1 Kasım 00:15, Volkan'ın üç oturum düzeni; CONTRIBUTING "Volkan'ın üç oturumu"; 23:12 / 23:18'in yerine; panel güvenilir olana kadar sunumda anlatılmaz, yük haritası öne):** **yük haritası (Faz 11) Volkan tarafında BUILD 1'de** (dal `yuk/`): öğlen yükü, akşam tepesi ön sürümü ([ADR-0018](docs/decisions/adr-0018-aksam-tepesi-on-surum.md); `src/sablon.py`, `src/tepe.py`), Kıb-Tek tepe verisinin modele girişi, Can'ın yük PR'larının incelemesi. **Can yükte kalır:** veri, eşzamanlılık ve sıcaklık eğimi analizi, üretici 1.5 (yaz boyutlandırması, yeni sınav şehirleri 31–40), tepe modelinin B-Y2 kısmı (iki bileşen, fitler; `tepe.py`'ye PR), tepe sınav kodu; Can'ın yazdığını Civan ya da BUILD 1 puanlar (öneren ≠ puanlayan). **Panel (Faz 9–10) BUILD 2'de** (dal `panel/`): başvuru anı motoru + sahte Kıb-Tek kayıtları (PR #22), güvenli uçlar ([ADR-0017](docs/decisions/adr-0017-pv-katmani-guvenli-uclar.md)), sarıda konum payı, inverter geri çözümü ve kademe, Faz 10 pilot hazırlığı (PR #19). **KARAR:** kutu, PR testi (resmi rakam Mac koşusu), birleştirme, ADR. KIOS e-postası hackathon sonrasına (cevap bu süre içinde gelmez).

Panel tarafında sıra Muhittin'in uyarısıyla: ucuz olan değil, sarıyı ve yanlış kırmızıyı en çok düşüren önde. Dayanak: [Muhittin'in üçüncü cevabı](docs/log/2026-10-31-muhittin-cevap-3-veri-dongusu.md), [dördüncü cevabı](docs/log/2026-10-31-muhittin-cevap-4-odak-tepe-kademe.md) (yük temel katman, akşam tepesi "ön" şartlarıyla, kademe, inverter geri çözümü), [ADR-0013](docs/decisions/adr-0013-veri-dongusu-tuzugu.md) (veri döngüsü tüzüğü), [ADR-0014](docs/decisions/adr-0014-yuk-katmani-ayri-tepe-modeli.md) (yük katmanı), [ADR-0012](docs/decisions/adr-0012-sari-trafoda-karar-basvuru-aninda.md) (başvuru anında karar), [ADR-0015](docs/decisions/adr-0015-basvuru-ani-motoru-durumlu-sari-sayi-konum.md) (başvuru anı motoru).

- **Faz 6 — Tüzük ve döngü altyapısı** (başladı 31 Ekim gece; [`docs/tuzuk.md`](docs/tuzuk.md) yazıldı, Faz 7 kartları ona referans veriyor): `docs/tuzuk.md` (ADR-0013'ün yedi maddesi + veri partisi görev kartı şablonu; içerik karar masası 21:20'de: görev kartı alanları, deney günlüğü, öneren ≠ puanlayan, iki seviyeli bitti); hold-out defteri; sürümleme (model + üretici + veri + tohum); `src/kalibrasyon.py` (PIT histogramı, nominal–ampirik kapsama eğrisi, şişirme katsayısı). Bitti: tüzük var, her görev kartı ona referans veriyor, kalibrasyon betiği İspanya ve İngiltere artıklarında koşuyor.
- **Faz 7 — Kalibrasyon gerçeğe karşı** (İspanya yük, İngiltere gerilim, gelen inverter kayıtları): bantlar gerçek artıklarla şişirilir ya da model-sapma terimi eklenir; "fazla emin" düzeltilmeden bant yayınlanmaz. Bitti: nominal %80 gerçek doğrulamada %70–90; PIT düz.
  - **Durum (31 Ekim 23:15; PR #16 main'de 23:06):** k_yük = 1,27 (İspanya, 29 trafo, 10 + 15 ölçülü = sevk yapılandırması; karar masası 22:0x), gerilim model-sapma s = exp(N(0,172; 0,414)) (İngiltere, 6 hat); [Faz 7 günlüğü](docs/log/2026-11-01-volkan-faz7-kalibrasyon.md). "Kalibre edildi", "iyileşti" değil (doğrulama payı yok, tüzük madde 1–2). Kutular Can'ın resmi ölçümüyle (öneren ≠ puanlayan; `sinav.py faz2`, BUILD'in kontrolü can.md KONTROL 23:15).
  - [x] İspanya %80 bant gerçekte %70–90 — Can'ın maddesi (faturalı, 10 ölçülü, tabakalı): K 1,27 ile %76,8, K 1,47 ile %82,1; BUILD bir-dışarıda (tabakalı 10 + 15): %78,5.
  - %95 bant: n = 28 trafo < 150 iken bilgi satırı (karar masası 22:13): %92,6 (K 1,47).
  - [x] PIT düz (10 kovada sapma ≤ tolerans = max(0,05; 2·√(0,09 ÷ n)), n = bağımsız trafo; karar masası 21:51) — Can'ın maddesi: K 1,47 ile 0,066 ≤ 0,113 (n = 28), yön "fazla geniş"; şekil düzeltmesi Faz 10'da.
  - [ ] İngiltere P98 6 hatta — BUILD: 5/6 → 6/6 (bir-dışarıda 6/6); Can'ın sınavında madde yok.
  - [x] Yanlış yeşil kapısı tutuyor — sınav 11–20 (v2b): 0/87 → 0/49 (bedeli yeşil %25 → %14, yanlış kırmızı %27 → %33, sarı %62 → %69; kaç ev P10 altı %15 → %7); yeni sınav 21–30 (üretici 1.3): 0/17.
  - **K_YUK 1,27 → 1,47 (karar masası 23:13):** kalibrasyon ürünün seçim yöntemiyle (tabakalı) ölçülür; 1,27 rastgele + tabakalı havuzundandı. Sınav 21–30 bir kez: İspanya %80 bant %76,8 → %82,1, PIT 0,066; renkler aynı (yanlış yeşil 0/17, yeşil 17, sarı %78). [Faz 7 günlüğü](docs/log/2026-11-01-volkan-faz7-kalibrasyon.md) Ek 3.
  - Farazi Faz 2 kapsama %87,5 → %92,9 (v2b; k 1,475'te %96,4): bilgi satırı, kapı İspanya (karar masası 21:51); farazi şehir gerçekten düzgün, Faz 8'de yeniden. Bedel kabul (yanlış yeşil 0 ve kalibrasyon kapıları önce). `KOL_P` kalır.
- **Faz 8 — Üretici çapalama ve yeni sınav şehirleri (üretici 1.3)** (karar masası 21:25): eldeki gerçek veriyle (İspanya yayılım ve korelasyon, İngiltere OG değişimi ve panel yeri, Kotsonias ince uç kol, Malta trafo boyutu çapası, Faz 7 kalibrasyon artıkları) üretici gerçek dağılımlara çapalanır, hedef plato (ADR-0013 madde 6); kalemler Faz 3 "üretici 1.3" listesinde. **Yeni tohumla yeni sınav şehirleri**; eskiler ayara girmez (madde 1). Faz 3 rakamları sürüm üçlüsüyle (model + üretici + veri + tohum) yeniden ölçülür ve günlüğe yazılır. Bitti: "gerçek – üretilen dağılım mesafesi" ölçülüp düzleşti, yeni sınav şehirlerinde iki kapı tutuyor.
  - **Durum (31 Ekim 23:15; PR #18 main'de 23:05; Can 21–30'u puanladı, BUILD ve karar masası Mac koşumuyla birebir; resmi rakamlar v3):** üretici 1.3: öğlen evde olma farkı (σ 0,20, İspanya'ya çapa: faturalı hata farazide %10,0 / P90 %31,9 ↔ İspanya %10–11 / %32–33), faz dengesi (kent %70 sırayla; İngiltere %14,4 ↔ %13,6), öğlen OG şehir başına. Yeni sınav 21–30 bir kez: yanlış yeşil 0/17 (dolu 44; %40 kuralı 22/44), farazi bant kapsaması %82 (geçer), yük hatası %12,2 / %27; **yeşil %5 (konut 0), yanlış kırmızı %51**; karar masası 22:2x / ADR-0016: bedel kabul; Faz 1 ölçütü ≤ %1 trafo + ≥ 200 V (geçer); saf fatura bilgi; yanlış kırmızı kalibrasyon ölçüsü (kırmızıların %49'u aşıyor; n'ye bağlı sınır %37 → geçer, yön karamsar). [Faz 8 günlüğü](docs/log/2026-11-01-volkan-faz8-uretici.md). Bu turda yok: Malta trafo boyutu, ince uç kol, panel yeri, net fatura.
- **Faz 9 — Kıb-Tek kayıtları ve başvuru anında karar** (sarıyı asıl düşüren; veri sunumdan önce gelmez, **istek metni şimdi**: `docs/istek/kibtek-veri-istegi-taslak.md`, BUILD taslak, Volkan gönderir; uzmana soru 2–4, 6–10 kampta): abone–trafo eşleşmesi, panelli abonenin adresi ve fazı, başvuru formuna hat / direk bilgisi (uzmana soru 2–4, 6–8); ADR-0012 başvuru anı hesabı yazılır ([ADR-0015](docs/decisions/adr-0015-basvuru-ani-motoru-durumlu-sari-sayi-konum.md): motor durumlu, haritayla aynı model ve kapı; sarıda sayı + konum) ve farazi şehirde "başvuru anı yanlış evet oranı" ile sınanır. Bitti: Kıb-Tek'ten kayıt geldi ya da gelmeyeceği belli; başvuru anı kararı farazide yanlış yeşil ≤ %2.
  - **Kademe (PV açılma denemesi, PR #20):** Kıb-Tek'in kademe *standardını* bilmek açmıyor (iki değerli politika: adım 6,25 V, belirsizlik bandı 8 V'tan dar değil; yanlış kırmızı 31 → 36); açan **trafo başına kademe ayarı / devreye alma kaydı**. İstek taslağına bu kalem eklendi. Tepe kalemleri (Muhittin 4 madde 3: trafo maksimum talep kayıtları ya da yaz yük etüdü, OG fider SCADA tepe geçmişi + sıcaklık, ticari / sanayi kayıtlı maksimum talep) Faz 11'le taslağa.
  - **Başvuru anı motoru + sahte kayıtlar (PR #22, deneme; karar masası 23:18; sınav 21–30 bir kez, gösterim):** kayıtlar gelirse hemen evet alan başvuru %3,8 → %10,5 (beklenen kayıt hatası; kusursuz bilgiyle %18), yanlış evet %0,1; aynı başvurularda %40 kuralının evetlerinin %13,4'ü yanlış; harita kayıtlarla kırmızı 61 → 41, yanlış yeşil 0. **Eksi:** kayıt hataları iki katıysa yanlış evet %2,6 (sınır %2); başvuruların üçte ikisi yine "önce ölç", yarısı yük tahmini yüksek güvenli olmayan trafolarda. [Günlük](docs/log/2026-11-01-volkan-sahte-kayit.md). Kalan: sarıda konum payı (`yesil_konum_payi`).
  - **Kayda koşullu evet için pilot şartı (karar masası 00:27):** motor kayıt hatasını iki kat varsayar (iki kat hatalı kayıtta yanlış evet %2,6 → %1,9, ama %95 aralığın üst ucu %3,2; sınav 21–30, gösterim) **ve** gerçek Kıb-Tek kayıtlarıyla canlıda kayda koşullu "hemen evet" ancak kayıt kalitesi sahada ölçüldükten sonra (pilotta 20–30 kayıt: kademe, direk sırası, faz); o zamana kadar bu evetler "önce ölç (kayıt teyidi)". Haritanın kayıtsız yeşili etkilenmez. [Günlük](docs/log/2026-11-01-volkan-panel-iki-kat-hata.md).
  - **Panel katmanı bırakılmaz; sahte kayıt testinin tanımı:** Kıb-Tek'in vereceği kayıtlar deneme şehrinde kusurlarıyla taklit edilir: `kayitlar.csv` (sözleşme 1.4 adayı), cevap anahtarından bozularak. Kusurlar [Yorum; gerçek oranlar Kıb-Tek'e sorulur]: kademe kaydı %80 doğru; abone → trafo %95 doğru; panelli abonenin hattı ve direk sırası ±2; faz kaydı %70 dolu, dolunun %90'ı doğru; hat boyu ±%15; inverter kaydı panelli evlerin %20'sinde (izinle). Üç düzey: hataların yarısı / aynısı / iki katı. Model kayıt varsa o bilinmeyenin çekilişini kayda koşullar (hiyerarşik, hata payıyla: kayıt öncülü daraltır, sıfırlamaz), yoksa bugünkü aralık; hat empedansı yalnız inverterin olduğu hatta bilinir; inverter gürültüsü ±1 V / ±%20 ve ±2 V / ±%40. Ölçü yan yana: bugün / sahte kayıtlarla / kusursuz bilgi; kur 1–10, sınav 21–30 bir kez. Gerçek kayıt gelince yalnız dosya değişir.
- **Faz 10 — Pilot A, ucuz ölçüm** (Faz 8 ve 9'la paralel; karamsar yönleri burada yeniden kalibre et: kırmızı olasılığı kovaları (0,5–0,7 → %34), kaç ev bandının üst ucu (P90 üstü %16), İspanya PIT şekli; ADR-0016): akıllı priz gece seviyesi (birkaç ev), inverter kayıtları (izinle), trafo plakası ve kademe; her ölçülü trafo partisi ayar / doğrulama diye bölünür (ADR-0013 madde 1). Her ölçülü partiden sonra hiyerarşik güncelleme ve sürümlü yeniden-fit (ADR-0013 madde 4); ayar payı hem modele hem üreticiye, doğrulama payı dokunulmaz; yani üretici çapalama Faz 8'de bir kez değil, her partide tekrarlanır. Hedef: yanlış kırmızı %27 → ~%19 (plato; fazla satılmaz), yeşil kuralının ilk Kıbrıs geri-testi. Bitti: en az 1 parti işlendi, hold-out defteri açık, kapılar tutuyor.
  - **Inverter kaydı açıyor (PV açılma denemesi, PR #20, model değişmedi; sınav 21–30, gösterim):** her panelli trafoda bir evin kaydıyla (iyimser uç; Muhittin 4 madde 5B: sakin an gerilimi ≈ trafo barası, öğlen salınımı hat empedansı) yeşil %5 → %10, konutta 0 → 9/142, yanlış kırmızı 31 → 15, yanlış yeşil 0/36; sarı %78 değişmiyor (sarının tabanı başvurunun yeri; çözüm başvuru anı, ADR-0012 / 0015). [Günlük](docs/log/2026-11-01-volkan-pv-acilma.md). Gerçekçi kapsama (panelli evlerin %20'si) sahte kayıt testinde (Faz 9).
  - **Hazırlık (PR #19, açık):** pilot A görev kartı (P6 inverter kaydı, P7 akıllı priz, P8 trafo plakası, P9 Kıb-Tek) ve `src/inverter_kaydi.py`; birleşme Volkan'ın sözüyle.
- **Faz 11 — Yük katmanı: trafo ne kadar dolu** (öncelikli; ADR-0014; Muhittin 4 madde 2–4; karar masası 23:12): haritanın temel çıktısı.
  - **İki ayrı soru:** tüketim doluluğu (yılın en yüksek saati, kVA ve akşam gerilim düşümü, 207 V) ↔ güneş sığma (bahar öğleni, en düşük yük, 259 V). Bağımsız; panel akşam tepesini düşürmez (tepe gün batımından sonra, batarya yok).
  - **Tepe anı saate kilitlenmez:** her trafoda yılın en yüksek saati bulunur ve saatiyle raporlanır (konut yaz akşamı, çarşı yaz öğleni, otel / sulama tipine göre).
  - **Net yükle:** trafodan geçen net yük; panel arttıkça öğlen düşer, tepe akşama kayar ve sivrilir.
  - **Ayrı tepe modeli, iki bileşen:** taban (fatura / tarife enerjisiyle ölçek, çeşitlilik √N) + klima (sıcaklık eğimi × klimalı ev sayısı; hava aynı anda vurduğu için eşzamanlılık yüksek). Eşzamanlılık Velander biçiminde (tepe ≈ N·a + b·√(N·a)), sıcak akşamlar ayrı. Sıcaklık düzeltme terimi: tepe ↔ sıcaklık eğimi, tasarım sıcaklığına (Lefkoşa, 10 yılda bir sıcak akşam) ölçeklenir, eğimin belirsizliği banda girer. Öğlen tahmini × tepe / öğlen oranı başlangıç olarak bile kullanılmaz (ADR-0014 madde 1).
  - **"Ön" sürüm şartları:** bant İspanya Mayıs artıklarından ve geniş; "Mayıs ≠ Temmuz" ve klima kuyruğu kör nokta olarak açık etiketli; birim kVA, güç katsayısı varsayımı 0,95 yazılı; yaz ölçümü gelene kadar düşük güven.
  - **İş (karar masası 23:18: yük kodu Can'da):** **B-Y1** (PR #21, BUILD yazdı, Can'a devredildi; Nisan çıktıları 1.3 ile birebir; Mac'te doğrulandı) üretici yıl boyu: aynı şehirler (aynı tohum, aynı ağ) için Temmuz ve Ocak haftası; Open-Meteo saatlik sıcaklık ve ışınımı o aya; yer trafosu listesine 1.600 / 2.500 kVA; cevap anahtarına `tepe_yil_kw`, `tepe_saati`, `tepe_ayi`, `v_min_tepe_v` (sözleşme 1.4, Can ya da Civan onayı). **B-Y2 (Can)** tepe modeli: sözleşme 1.4 `tepe_kva`, P10 / P90, `tepe_saati`, `pf_varsayim`, "ön" etiketi; eşzamanlılık ve sıcaklık eğimi gelene kadar Velander varsayılanı [Yorum]. **Can:** veri (Kıbrıs 20 prosumer evi 2016, Lefkoşa prosumer evi, Kıbrıs PV + sıcaklık, Lefkoşa saatlik sıcaklık, Slovenya trafo yükleri; Civan'ın bulut oturumu `deneme/eszamanlilik` yardımcı), eşzamanlılık eğrisi, sıcaklık eğimi, sözleşme 1.4 tepe sütunları, `sinav.py faz2` tepe maddesi (İspanya Mayıs tepesi gerçek veri, bir-dışarıda; geçici eşik ortanca ≤ %15 / P90 ≤ %35 [Yorum]). **Civan:** kart görünümü Faz 4 bitince. Kıb-Tek'ten tepe verisi Faz 9 istek listesine.
  - Bitti: her trafoda tepe, saati ve bandı "ön" etiketli; tepe sınav maddesi (İspanya Mayıs) bilgi satırı; Temmuz şehirlerinde tepe hatası ve 207 V düşümü raporlandı.
- **Faz 12 — Canlı geçiş kapısı:** dokunulmamış gerçek hold-out'ta ~150 bağımsız karar noktası, 0 ihlal (yanlış yeşil < %2, %95 güven), kalibrasyon toleransta, sürümlü yayın; sarı trafolarda geçici ölçüm cihazı (asıl pilot). Bitti: iki kapı geçildi, ilk sürüm Kıb-Tek'e teslim.
- Her fazda ölçü sırası: yanlış yeşil kapısı → kalibrasyon kapısı → sarı ve yanlış kırmızı. "İyileşti" yalnız dokunulmamış veride söylenir.
- Sarı düzelir ama ölçümle değil kayıtla: gerilim ölçümü yanlış kırmızıyı düzeltir ve platoya oturur; sarıyı düşüren Kıb-Tek'in adres / faz kaydı ve başvuru anında karar (Faz 9). Bu yüzden Faz 9 pilotla paralel ve önde.

**Dış veri istekleri** (karar masası 21:16; mesajı Volkan yazar, ekip yazmaz):
- KIOS yazarları (Kotsonias vd. 2019): Kıbrıs AG hat modeli ve EAC'nin 60 tüketici verisi.
- Micallef 2015 yüksek lisans tezi (Malta Üniversitesi, "Request a copy"): Gozo hat boyu ve kablo; dış sınama adayı Gozo hattını koşulabilir yapar ([ada ülkeleri günlüğü](docs/log/2026-10-31-volkan-ada-ulkeleri.md)).
