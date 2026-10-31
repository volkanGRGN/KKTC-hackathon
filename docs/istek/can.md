# Can için istekler

Burası Can'ın kutusu; yalnız o işler. Kalıp için [README](README.md).

## UYARI! 31 Eki — Volkan'dan — Faz 1 veri adımı: iki BULAMADIM'a cevap
Ne: (1) **Kıb-Tek trafo/kablo şartnamesi:** bizde de belgesi yok. 30 Ekim'deki araştırmada şartname tarihleri not edilmiş (direk tipi 17.04.2018, yer tipi 24.09.2021) ama bağlantı kaydedilmemiş; bugün iki aramada (Türkçe teknik şartname, site:kibtek.com) bulunamadı. Veri sözlüğündeki "Kıb-Tek trafo şartnameleri [Kaynaklı, hafızadan]" satırını "kaynak bağlantısı yok, doğrulanmadı" diye işaretle; benzetimdeki kVA listesi, 250 V ve kablo dirençleri (r 0,50 / 0,36 Ω/km) "varsayım" etiketiyle kalsın. Bakılabilecek tek ipucu: ODTÜ Kuzey Kıbrıs kampüsünün trafo ihale dosyası (ncc.metu.edu.tr/sites/default/files/ihale-dosyasi-trafo17.pdf), Kıb-Tek'e uygun teknik değer içerebilir, kontrol edilmedi; zamanın kalırsa bak. (2) **Yurt yatak sayısı:** varsayım kararını onaylıyorum (ADR-0004).
Dosya: docs/data/data-dictionary.md, docs/log/2026-10-31-can-faz1-veri.md (kendi günlüğün; yeni girdi olarak)
Neden: kaynaksız rakam "kaynaklı" görünmesin; Faz 1 eleme kararı onayı. Yeni kural: CONTRIBUTING "Bulamadım akışı" — bundan sonra BULAMADIM'ları günlüğün yanında benim kutuma da yaz.
Durum: yapıldı 13:50 (veri sözlüğü işaretlendi; ODTÜ dosyasına erişilemedi, arama izi günlükte)

## UYARI! 31 Eki 12:10 — Civan'dan — veri sözlüğüne OSM satırı
Ne: "Elimizde" altına OSM kasaba satırı ekle: `data/raw/osm-kasaba/` — Girne merkez (~1 km × 1,1 km) bina ve yol geometrisi, OpenStreetMap, ODbL 1.0, indirildi 31 Ekim 2026. Ölçülü değil, gönüllü çizim. [Hesap] 974 bina (278'inde kat bilgisi), 330 yol. Yanlılık: binaların %89'unun türü belirtilmemiş; OSM'de trafo yok (konumlar farazi şehirden). Kullanım: Faz 4 harita altlığı. Lapta elendi (17 bina). Ayrıntı `data/raw/osm-kasaba/KAYNAK.txt`.
Dosya: docs/data/data-dictionary.md
Neden: her indirilen veri sözlükte satır olmalı (ROADMAP Faz 1 geçme sınavı); sözlük senin dosyan.
Durum: yapıldı 13:50

## KARAR 31 Eki 12:25 — volkan.md'deki "Faz 1 sağlama eşiği: 'pazar günü çarşı öğleni'" isteğine
Karar: Madde sağlamada kalır, eşik değişir: "çarşı Nisan tatil öğleni / iş günü öğleni (11–14)" aralığı **0,6–0,9** olur ("pazar" kelimesi kalkar, "tatil" olur). Şehir üreticisine ayrıca varsayım konmaz; sözleşmedeki `gun_turu` zaten `isgunu` / `tatil`, EAC'nin tatil tipik günüyle birebir.
Neden: ROADMAP'teki "yarısından az" eşiği pazar için yazılmıştı; EAC'de pazar ayrı yok, tatil tipik günü cumartesi + pazar + bayram ortalaması ve Kıbrıs'ta dükkânlar cumartesi açık [Yorum], o yüzden yarıya inmesi beklenmez. Sağlamanın amacı "tatilde çarşı düşüyor mu, veri doğru okunuyor mu": üst sınır 0,9 düşüşü, alt sınır 0,6 yanlış sütun okumayı (tatil ≈ 0) yakalar. Mac'te senin kodunla doğruladım [Hesap, PR #5 @ 3bfef6a]: çarşı Nisan 0,83; ay ay 0,64–0,83 (en yükseği Nisan); küçük ticari 0,59–0,84; konut 1,00–1,44 (tatilde artıyor, beklendiği gibi). Eşik [Yorum]. ADR-0004 EAC'yi sınırlarıyla seçti, bu da o sınırlardan biri; yöntem kararı değişmiyor, yeni ADR gerekmez.
Senden beklenen: PR #5'te `saglama()` son maddesinin adı "çarşı Nisan tatil öğleni / iş günü öğleni (11–14)", aralığı (0.6, 0.9) olsun; günlüğündeki tabloya yeni satır ("eşik karar masasında değişti 12:25"; eski KALDI satırı silinmez). Veri sözlüğündeki EAC satırına yanlılık olarak "cumartesi = pazar = bayram, tek tatil tipik günü" ekle. ROADMAP Faz 1'deki "pazar günü çarşı öğleni iş gününün yarısından az" satırını Volkan'ın ana oturumu düzeltir; sen dokunma.
Durum: yapıldı 14:35 (PR #5 @ f76edda: aralık 0,6–0,9, 5/5 GEÇTİ; günlüğe yeni satır; veri sözlüğüne yanlılık)

## PR İNCELEME 31 Eki 12:25 — PR #5 "veri: profiller.py ilk sürüm (EAC sınıf eğrileri, 5 dk, sağlama)"
Sonuç: sağlama eşiği düzeltilince birleştirilebilir (yukarıdaki ilk KARAR).
+ İmzalar ve adlar kartla birebir: `oku(yol=XLSX)`, `sinif_egrisi(veri, sinif, ay, gun)`, 7 sınıf adı; 7 tip adı sözleşmedeki `tip` değerleriyle aynı; TIPLER notu ve enerji sağlaması eklendi; her `open()` utf-8, yollar pathlib; önbellek `data/raw/` altında ve .gitignore tutuyor; yalnız kendi dosyaların; main'le çakışma yok (MERGEABLE / CLEAN).
+ Mac'te çalıştırdım (Python 3.13, openpyxl 3.1.5): beş rakam Windows'takiyle birebir (0,71 · 11:15 · 3,96 · 1,00 · 0,83); Excel'den soğuk okuma 0,1 s (tipik gün bloğundan sonra duruyor), önbellekten 0,03 s. Kartın "Mac ve Windows'ta" maddesi sağlandı; günlüğüne "Mac: karar masası doğruladı 12:25" yazabilirsin.
− `saglama()` son maddesi: ad ve aralık KARAR'daki gibi değişmeli (src/profiller.py, `saglama()` içindeki son `sonuc.append`). Şu an çıkış kodu 1; kartın "5 sağlama GEÇTİ" denemesi bu yüzden geçmiyor.
− Günlükteki tabloya yeni sonuç satırı (append-only; eski satır kalır).
? Windows'ta çıktı ve Türkçe karakter: sen çalıştırdın, bende ölçülmedi. 14 "tamamen sıfır" sınıf-günün hepsi `isi_depolama` (kullanmadığımız sınıf) [Hesap]; sorun değil, günlüğe bir kelime yeter.
Senden beklenen: iki düzeltmeyi dala gönder, sonra kartın dediği gibi sen birleştir (Volkan'ın bakması = bu inceleme).
Durum: düzeltmeler dalda 14:35 (f76edda); birleştirme Can'ın onayını bekliyor

## KARAR 31 Eki 13:00 — volkan.md'deki "Faz 1 sınavı: üretim süresi 60 sn'yi aşıyor" isteğine
Karar: Eşik 60 sn kalır ("her şehir", yani en uzun; senin uyguladığın gibi) ve **şehirlerin üretildiği makinede** ölçülür (bugün Volkan'ın Mac'i). Windows süresi günlüğe bilgi olarak girer; Windows maddesi "çalıştı + çıktı UTF-8" olarak kalır. Hızlandırma mı eşik mi: önce hızlandırma, eşik en son; ama şimdi değil, ADR-0006 aralığıyla yeniden üretince ölçüme göre.
Neden: Aynı üreticiyle (sehir/ilk-surum @ 7195227 + PR #5 f76edda, EAC eğrileri, yapay ışınım, eski %10–50 aralığı) Mac'te üç şehir 8,8 / 8,8 / 10,3 sn [Hesap, karar masası 12:55]; Volkan'ın 20 şehri ortanca 11,0, en uzun 14,2 sn. Senin Windows'un 5–6 kat yavaş; fark algoritmadan çok makine/ortam ve girdi: kodda kaç ev döngüsü yalnız "bugün aşmayan" trafoda çalışıyor (`trafo_benzet`, `if bugun is None`), gerçek Lefkoşa ışınımıyla bugünden aşan trafo azalınca döngü her trafoda koşuyor (senin uzun şehirlerinde kaç ev ortancası 6,5–8,5, benimkilerde 0). ADR-0006 ile aşan trafo daha da azalacak → süre iki makinede de artacak; o zaman bakılır. Eşiğin amacı 20–30 şehrin pratikte üretilebilmesi; Mac'te 20 şehir ~4 dk, amaç sağlanıyor.
Senden beklenen: `sinav.py` süre maddesinin ayrıntısına `ayar.json`'dan `isinim_kaynagi` ve `profil_kaynagi` ekle (hangi girdiyle ölçüldüğü görünsün); Windows ölçümünü günlükte "bilgi: Windows 11, i7-13700H, Python 3.13" diye tut. Resmi Faz 1 süre sonucu: Volkan Mac'te üretir + `sinav.py faz1` koşar, kendi günlüğüne yazar.
Senden beklenen (ana oturum): ADR-0006 aralığıyla 20 şehri yeniden üretince süreyi günlüğe; en uzun > 60 sn olursa kaç ev döngüsünü hızlandır (adaylar: `SIRA_SAYISI` 7 → 5; `asim()` içinde solve `iters` 5 → 3; sıralar arası taban çözümü paylaşımı), eşiği oynatma.
Durum: bekliyor

## KARAR 31 Eki 13:00 — volkan.md'deki "cevap anahtarı: kac_ev_sinir ile kac_ev_tavan çelişiyor" isteğine
Karar: Çelişki yok; sözleşmenin güncel hali (PR #4 @ 2a02a81, §3) tam bu durumu tanımlıyor: `kac_ev_aday` = 0 ise `kac_ev_tavan` = 1 ("kaç ev sütunları bilgi taşımaz"), `kac_ev_sinir` = bugün aşıyorsa bugünkü aşımın nedeni (`gerilim`), aşmıyorsa `yok` ("hiç ret yok"). Eski taslaktaki "yok (tavan)" ifadesi değişmişti; o yüzden tavan sayısı ≠ `yok` sayısı, fark tam olarak "aday yok + bugün aşıyor" trafolar (sende 3).
Neden: Üretici de böyle yazıyor: Mac'te 3 şehir / 120 trafoda 15 trafo aday = 0 (sanayi, sulama, otel; konut abonesi yok), biri (sehir-002 T03 sulama, v_max 259,9 V) tavan 1 + sınır `gerilim` [Hesap, karar masası 12:55]. Aday yoksa "kaç ev" sorusu o trafoda anlamsız; tavan 1 bunu söylüyor, sınır ise bugünün durumunu (Faz 3 "ölçülmedi/aday yok" etiketi için işe yarar).
Senden beklenen: `sinav.py` bilgi satırlarına "aday = 0 trafo: N (tip dağılımı)" ekle; tavan oranını ve sınır sayımını aday > 0 olan trafolar üzerinden ver, aday = 0'ları ayrı say. Sözleşmeyi PR #4'ün son halinden oku (2a02a81).
Durum: bekliyor

## KARAR 31 Eki 13:00 — volkan.md'deki "bilgi: 105/800 trafoda v_max > 264 V; ayar.json CRLF" isteğine
Karar: Okundu. (1) 264 V: ADR-0006'da var: `v_max` 264 V üstü değerler fiziksel değil, "gösterim" etiketli; Faz 3 zaten 259 V sınırını kullanır, inverter kapanması şimdi modellenmez. (2) `ayar.json` da LF olsun; sözleşmenin satır sonu kuralı CSV ve JSON'u kapsayacak.
Neden: Tohum sınavı ("iki çalıştırma birebir") makineler arası da anlamlı olsun; `json.dump` için `open(..., 'w', encoding='utf-8', newline='')` yeter (Mac'te zaten LF çıkıyor).
Senden beklenen: Hiçbir şey; bilgi için teşekkürler, rakamlar günlüğünde kalsın.
Senden beklenen (ana oturum): `src/sehir_uret.py` satır 478 `open(klasor / 'ayar.json', 'w', encoding='utf-8', newline='')` (PR #6); sözleşme "Genel kurallar" CSV satırına "JSON da LF" (PR #4); Faz 3 kartına "264 V üstü gerçekte görülmez, üretim kesilir" notu.
Durum: bilgi — iş ana oturumda

## PR İNCELEME 31 Eki 13:00 — PR #5 @ f76edda (güncelleme) "veri: profiller.py ilk sürüm"
Sonuç: birleştirilebilir.
+ Tek düzeltme istendiği gibi: sağlama 5 adı ve aralığı (0.6, 0.9), açıklama satırı doğru; günlükte eski satır duruyor, yeni satır eklendi; Mac'te 5/5 GEÇTİ, çıkış kodu 0 [karar masası 12:53].
Senden beklenen: birleştir (kart: Volkan bakar, sen birleştirirsin; bakıldı). Önce #5, sonra #7.
Durum: bekliyor

## PR İNCELEME 31 Eki 13:00 — PR #7 "sinav: Faz 1 geçme sınavı ölçüleri"
Sonuç: iki küçük düzeltmeyle birleştirilebilir.
+ Kartın 4. adımındaki her madde var; sütun ve anahtar adları sözleşmeyle birebir (§1, §3, §4); yer tutuculu ve eksik dosyalı şehir atlanıp uyarı yazılıyor; her `open()` utf-8 + `newline=''`, yollar pathlib; ek bağımlılık yok; yalnız kendi dosyan; main'le çakışma yok. Mac'te gerçek üreticiyle 3 şehir / 120 trafoda çalıştı, çıktı doğru, < 1 sn [karar masası 12:55].
− Madde 3 (259 V üstü) ROADMAP'te toplamda "en az bir trafo"; sen şehir başına ölçüyorsun. ADR-0006 ile %3 yaygınlıklı bir şehirde hiç aşan olmayabilir, o şehir bozuk değildir → geçme ölçütü toplam ≥ 1, şehir başına sayı bilgi satırına (karar: karar masası, bu girdi).
− Madde 2 eşiği şehir sayısına bağlansın: 3 × şehir sayısı (20 şehirde 60); 3 şehirlik denememde "KALDI: sanayi 10" dedi, oysa 10 ≥ 9. 20'den az şehirde ayrıca "UYARI: ROADMAP eşiği 20 şehir için" yaz.
− Yukarıdaki iki KARAR'ın sinav.py kalemleri: süre ayrıntısına `isinim_kaynagi` / `profil_kaynagi`; aday = 0 trafo sayısı ve aday > 0 üzerinden tavan/sınır.
? Windows'ta ve kusurlu şehir senaryonla bende ölçülmedi (sahte şehirlerin bende yok); senin kanıtın geçerli.
Senden beklenen: düzeltmeleri dala gönder, sonra sen birleştir (#5'ten sonra).
Durum: bekliyor
