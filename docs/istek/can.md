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
Durum: yapıldı 14:55 (birleşti, f3615ba)

## KARAR 31 Eki 13:00 — volkan.md'deki "Faz 1 sınavı: üretim süresi 60 sn'yi aşıyor" isteğine
Karar: Eşik 60 sn kalır ("her şehir", yani en uzun; senin uyguladığın gibi) ve **şehirlerin üretildiği makinede** ölçülür (bugün Volkan'ın Mac'i). Windows süresi günlüğe bilgi olarak girer; Windows maddesi "çalıştı + çıktı UTF-8" olarak kalır. Hızlandırma mı eşik mi: önce hızlandırma, eşik en son; ama şimdi değil, ADR-0006 aralığıyla yeniden üretince ölçüme göre.
Neden: Aynı üreticiyle (sehir/ilk-surum @ 7195227 + PR #5 f76edda, EAC eğrileri, yapay ışınım, eski %10–50 aralığı) Mac'te üç şehir 8,8 / 8,8 / 10,3 sn [Hesap, karar masası 12:55]; Volkan'ın 20 şehri ortanca 11,0, en uzun 14,2 sn. Senin Windows'un 5–6 kat yavaş; fark algoritmadan çok makine/ortam ve girdi: kodda kaç ev döngüsü yalnız "bugün aşmayan" trafoda çalışıyor (`trafo_benzet`, `if bugun is None`), gerçek Lefkoşa ışınımıyla bugünden aşan trafo azalınca döngü her trafoda koşuyor (senin uzun şehirlerinde kaç ev ortancası 6,5–8,5, benimkilerde 0). ADR-0006 ile aşan trafo daha da azalacak → süre iki makinede de artacak; o zaman bakılır. Eşiğin amacı 20–30 şehrin pratikte üretilebilmesi; Mac'te 20 şehir ~4 dk, amaç sağlanıyor.
Senden beklenen: `sinav.py` süre maddesinin ayrıntısına `ayar.json`'dan `isinim_kaynagi` ve `profil_kaynagi` ekle (hangi girdiyle ölçüldüğü görünsün); Windows ölçümünü günlükte "bilgi: Windows 11, i7-13700H, Python 3.13" diye tut. Resmi Faz 1 süre sonucu: Volkan Mac'te üretir + `sinav.py faz1` koşar, kendi günlüğüne yazar.
Senden beklenen (ana oturum): ADR-0006 aralığıyla 20 şehri yeniden üretince süreyi günlüğe; en uzun > 60 sn olursa kaç ev döngüsünü hızlandır (adaylar: `SIRA_SAYISI` 7 → 5; `asim()` içinde solve `iters` 5 → 3; sıralar arası taban çözümü paylaşımı), eşiği oynatma.
Durum: yapıldı 15:00 (PR #7 @ de55442: süre ayrıntısında profil/ışınım kaynağı; Windows ölçümü günlükte bilgi)

## KARAR 31 Eki 13:00 — volkan.md'deki "cevap anahtarı: kac_ev_sinir ile kac_ev_tavan çelişiyor" isteğine
Karar: Çelişki yok; sözleşmenin güncel hali (PR #4 @ 2a02a81, §3) tam bu durumu tanımlıyor: `kac_ev_aday` = 0 ise `kac_ev_tavan` = 1 ("kaç ev sütunları bilgi taşımaz"), `kac_ev_sinir` = bugün aşıyorsa bugünkü aşımın nedeni (`gerilim`), aşmıyorsa `yok` ("hiç ret yok"). Eski taslaktaki "yok (tavan)" ifadesi değişmişti; o yüzden tavan sayısı ≠ `yok` sayısı, fark tam olarak "aday yok + bugün aşıyor" trafolar (sende 3).
Neden: Üretici de böyle yazıyor: Mac'te 3 şehir / 120 trafoda 15 trafo aday = 0 (sanayi, sulama, otel; konut abonesi yok), biri (sehir-002 T03 sulama, v_max 259,9 V) tavan 1 + sınır `gerilim` [Hesap, karar masası 12:55]. Aday yoksa "kaç ev" sorusu o trafoda anlamsız; tavan 1 bunu söylüyor, sınır ise bugünün durumunu (Faz 3 "ölçülmedi/aday yok" etiketi için işe yarar).
Senden beklenen: `sinav.py` bilgi satırlarına "aday = 0 trafo: N (tip dağılımı)" ekle; tavan oranını ve sınır sayımını aday > 0 olan trafolar üzerinden ver, aday = 0'ları ayrı say. Sözleşmeyi PR #4'ün son halinden oku (2a02a81).
Durum: yapıldı 15:00 (PR #7 @ de55442: aday = 0 ayrı, tavan/sınır aday > 0 üzerinden)

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
Durum: yapıldı 14:55 (birleşti, f3615ba)

## PR İNCELEME 31 Eki 13:00 — PR #7 "sinav: Faz 1 geçme sınavı ölçüleri"
Sonuç: iki küçük düzeltmeyle birleştirilebilir.
+ Kartın 4. adımındaki her madde var; sütun ve anahtar adları sözleşmeyle birebir (§1, §3, §4); yer tutuculu ve eksik dosyalı şehir atlanıp uyarı yazılıyor; her `open()` utf-8 + `newline=''`, yollar pathlib; ek bağımlılık yok; yalnız kendi dosyan; main'le çakışma yok. Mac'te gerçek üreticiyle 3 şehir / 120 trafoda çalıştı, çıktı doğru, < 1 sn [karar masası 12:55].
− Madde 3 (259 V üstü) ROADMAP'te toplamda "en az bir trafo"; sen şehir başına ölçüyorsun. ADR-0006 ile %3 yaygınlıklı bir şehirde hiç aşan olmayabilir, o şehir bozuk değildir → geçme ölçütü toplam ≥ 1, şehir başına sayı bilgi satırına (karar: karar masası, bu girdi).
− Madde 2 eşiği şehir sayısına bağlansın: 3 × şehir sayısı (20 şehirde 60); 3 şehirlik denememde "KALDI: sanayi 10" dedi, oysa 10 ≥ 9. 20'den az şehirde ayrıca "UYARI: ROADMAP eşiği 20 şehir için" yaz.
− Yukarıdaki iki KARAR'ın sinav.py kalemleri: süre ayrıntısına `isinim_kaynagi` / `profil_kaynagi`; aday = 0 trafo sayısı ve aday > 0 üzerinden tavan/sınır.
? Windows'ta ve kusurlu şehir senaryonla bende ölçülmedi (sahte şehirlerin bende yok); senin kanıtın geçerli.
Senden beklenen: düzeltmeleri dala gönder, sonra sen birleştir (#5'ten sonra).
Durum: yapıldı 15:05 (birleşti, f1b2a0c)

## UYARI! 31 Eki 13:36 — Volkan'dan (BUILD oturumu) — Faz 2 kartın hazır
Ne: Faz 1 kapandı (sonuç Volkan'ın Faz 1 günlüğünde). Faz 2 kartın: [docs/gorev/can-faz2-sinav-grafikler.md](../gorev/can-faz2-sinav-grafikler.md) — `sinav.py faz2` (yedi ölçü), `grafikler.py` (kalibrasyon, kaç trafo ölçmeli), İspanya EDP zaman kutusu. `sablon.py` gelene kadar sözleşme biçiminde sahte `tahmin.csv` ile başla.
Dosya: src/sinav.py, src/grafikler.py, data/raw/edp-*/KAYNAK.txt, docs/data/data-dictionary.md
Neden: ROADMAP Faz 2; modeli yazan sınavı yazmaz.
Durum: yapıldı 15:25 — PR #14 (`sinav.py faz2`, `grafikler.py`); 20 şehir (1.2) sonucu docs/log/2026-10-31-can-faz2.md; EDP adımı 31 Ekim öğlen

## UYARI! 31 Eki 13:51 — Volkan'dan (BUILD oturumu) — PR #8: sözleşme 1.1 onayı + sablon.py geldi
Ne: [PR #8](https://github.com/volkanGRGN/KKTC-hackathon/pull/8) `src/sablon.py` ilk sürüm ve sözleşme 1.1: `deney/tahmin_capraz_s<AAA>.csv` (kartındaki ad), `sablon_ozet.json` (bilgi), JSON da LF, §5 `oran` **brüt** (`tuketim_kw`; senin sorun). Sözleşme değişikliği olduğu için onayın gerekiyor; sütunlara bakman yeter. Birleşince `python3 src/sablon.py data/synthetic` (~1 dk) gerçek `tahmin.csv` üretir; sahte dosyayı bırakıp `sinav.py faz2`'yi bununla koş.
Dosya: docs/data/tablo-bicimi.md, src/sablon.py
Neden: CONTRIBUTING "Dallar" 1 ve 2 (sözleşme + yeni modül). Model ayarları yalnız şehir 1–10'da denendi; 11–20'yi sınav için ayrı raporlarsan iyi olur (Faz 2 günlüğü).
Durum: yapıldı — sözleşme onaylandı; `sinav.py faz2` gerçek `tahmin.csv` (PR #12 dalı, 1.2) ile koşuldu, 11–20 ayrı raporlandı (günlük)

## KARAR 31 Eki 13:55 — Faz 1 eşiği 216 V → 207 V (BUILD'in sorusuna karar)
Karar: `src/sinav.py` `V_ALT = 207.0` (EN 50160 alt sınırı: 230 V −%10); madde adı "hiçbir trafoda v_min_bugun_v < 207 V". ROADMAP satırını BUILD değiştiriyor.
Neden: Yeni şehirlerde (gerçek ışınım, %3–25) 3/800 trafo 211–215 V; benzetim bozuk değil, uzun kırsal hat ve büyük yüklü tek hat. Gerekçe volkan.md'deki KARAR'da.
Senden beklenen: tek satır değişiklik, doğrudan main (kendi dosyan); günlüğe bir satır.
Durum: yapıldı (66b51e6; eski 20 şehirde en düşük 216,0 V → GEÇTİ; ek: Windows'ta boruya UTF-8 çıktı düzeltmesi)

## KARAR 31 Eki 13:55 — volkan.md'deki "İspanya EDP kullanılabilir" isteğine
Karar: Evet, çıkarma betiğini sen yaz (zaman kutusu 1 saat): `src/edp_oku.py` (yeni, senin). Çıktı `data/raw/edp-oviedo/turetilmis/` altına (gitignore'da, betikle yeniden üretilir): (1) `trafolar.csv` sözleşme §1 sütunlarıyla, `sehir` = 801 (gerçek veri 800–899 [Yorum]; sözleşmeye satırı BUILD ekler), `kva`, `hat_boyu_max_m` varsa, `abone_konut` = toplam müşteri (sınıf yok [Yorum]), kalan abone sütunları 0, `panel_sayisi`/`panel_kw` 0 (2018 İspanya AG'de çatı PV ihmal [Yorum]); (2) `yuk_saatlik.csv`: `sehir, trafo_no, gun, gun_turu, saat, net_kw` (21 gün × 24; 5 dakikaya açma yok, model tarafı karar verir; `tuketim_kw` = `net_kw` varsayımı [Yorum]); (3) `cevap_anahtari.csv` yalnız `ogle_min_kw` (11–14, 21 gün, saatlikten) ve `tepe_kw`; `tip` boş. TD009456 (tamamen sıfır) dışarıda, sayısı KAYNAK.txt'de.
Neden: Veriyi sen tanıyorsun, BUILD `sablon.py`'de; eleme 4/5 doğru. EDP'nin görevi eğitmek değil benzetimin yanlılığını görmek (ADR-0003 kanıt sırası: İngiltere → İspanya gerçek → farazi). Sınıf yok diye modelin yalnız kVA + müşteri + hat boyuyla koşması da sonuç: "gerçek veri, sınıfsız" başlığıyla raporlanır, "gösterim" değil.
Senden beklenen: betik + üç dosya + günlüğe satır (`docs/log/2026-10-31-can-faz2.md`); bitince volkan.md'ye "EDP türetilmiş dosyalar hazır" (BUILD koşar, 2i). NGED şimdi değil.
Durum: iptal 15:12 — BUILD ham veriden doğrudan koştu (PR #10, edp_test.py); betik gerekmez

## KARAR 31 Eki 13:55 — volkan.md'deki "sözleşme §5: arketipler.csv oran brüt mü net mi?" isteğine
Karar: **Brüt** (`tuketim_kw`). BUILD'in PR #8'indeki sözleşme 1.1 tam bunu yazıyor: "`oran` … brüt tüketimden: ölçülü trafoların `tuketim_kw` gün türü ortalaması, net değil". Kartındaki "gerçek küme" kuralı ve harita formülü buna uyuyor; `sinav.py faz2` böyle kalsın.
Neden: ADR-0001 şekli tüketim eğrisinden kümeler; net eğri panel payıyla değişir, şekil ile PV karışır. Hedef `ogle_min_kw` de brüt (§3). Ölçülü trafoda brütün netten çıkarılabildiği varsayımı §2'de [Yorum].
Senden beklenen: PR #8'in **sözleşme kısmını** (docs/data/tablo-bicimi.md, 12 satır: şehirler arası deney dosyası, `sablon_ozet.json`, JSON LF, `oran` brüt) GitHub'da gözden geçirip onayla; sözleşme değişikliği Can ya da Civan onayı istiyor, §5 senin sınavını ilgilendiriyor. `sablon.py` kodunu incelemen gerekmez. Onaydan sonra BUILD birleştirir.
Durum: yapıldı (PR #8 GitHub'da onaylandı, CanSahin77; BUILD birleştirir)

## KARAR 31 Eki 13:55 — volkan.md'deki "bilgi: PR #6 okuma notları" isteğine
Karar: Okundu; iki not da doğru, ikisi de şimdi yeniden üretim gerektirmiyor (Faz 2 bu şehirlerde koşuyor). (1) Bayramlar: sürüm 1'de "bayramlar iş günü sayıldı [Yorum]" notu; bir sonraki yeniden üretimde (sözleşme 1.2 ya da Faz 3 öncesi) KKTC resmi tatilleri `gun_turu = tatil` olsun: 2024 Ramazan Bayramı 10–12 Nisan, 23 Nisan; 2025'te 1 Nisan (bayramın son günü) ve 23 Nisan [Kaynaklı: resmi takvim; tarihler BUILD tarafından doğrulanır]. EAC'nin tatil tipik günü bayramı zaten kapsıyor, tutarlı. (2) 1000 kVA tavanı: Nisan tepesi ≤ %50 kVA, şimdilik etkisiz; üretici `ayar.json`'a `kva_tavan_sayisi` yazsın (bilgi; ek anahtar serbest). Yaz benzetilirse yer tipi listeye 1600/2500 (veri sözlüğü: yer tipi 50–2.500 kVA) — o zaman sözleşme değişikliği.
Senden beklenen: hiçbir şey; teşekkürler.
Senden beklenen (ana oturum): iki notu `sehir_uret.py` docstring'ine ve Faz 1 günlüğüne; bayram listesi ve `kva_tavan_sayisi` bir sonraki üretici sürümüne.
Durum: bilgi — iş ana oturumda

## KARAR 31 Eki 13:58 — Volkan'ın ilettiği öneriye: "yeni veri kontrol listesi" ve `src/veri_sagla.py`
Karar: (1) Kontrol listesi **evet, şimdi**: veri sözlüğünün başına 8–10 satırlık "yeni veri eklerken" listesi (birim, çözünürlük, saat damgasının anlamı, saat dilimi, SHA-256, çifte sayım riski, hangi kaynakla çapraz sağlanacağı, lisans, etiket Kaynaklı/Hesap/Yorum). Senin dosyan, doğrudan main, ≤ 15 dk. (2) `src/veri_sagla.py` **evet ama sonra**: önce `sinav.py faz2` + grafikler + EDP betiği (kartın ve bugünkü üç KARAR); onlar bitince zaman kutusu 1 saat. İçerik: EAC sınıf eğrileri × Kıb-Tek sınıf başına yıllık tüketim → aylık toplam ↔ Kıb-Tek 2023 aylık tüketim (Nisan dahil 12 ay, sapma eşiği [Yorum] %15); EAC çatı güneşi tipik günü ↔ Open-Meteo Nisan ışınım şekli (tepe saati ±1 saat, öğlen/akşam oranı); üretici 20 şehrin abone başına yıllık enerjisi ↔ Kıb-Tek sınıf ortalaması (±%10). Her madde GEÇTİ/KALDI + rakam, `profiller.py` sağlamasıyla aynı kalıp; kalan madde eşiğe uydurulmaz, günlüğe yazılır. Yeni dosya senin (veri adımı); ilk sürüm dal + PR.
Neden: Kontrol listesi Muhittin'in ortak sınavının ("her rakam etiketli", "çifte sayım yok") günlük karşılığı, ucuz. Çapraz sağlama değerli (modelin ölçeği Kıb-Tek yıllık tüketimine dayanıyor; EAC × Kıb-Tek aylık toplamı tutmuyorsa büyüklük yanlış) ama Faz 2 geçme sınavı önce; "çok duraksıyoruz" (Volkan).
Senden beklenen: (1) bugün; (2) kart işlerinden sonra, günlüğe sonuç. Soru gerekmez.
Durum: (1) yapıldı (d9e69a7, 9 madde); (2) bekliyor — kart işlerinden sonra (Faz 3 kartı önce)

## KARAR 31 Eki 15:12 — Can'ın "Faz 2 sınavı farazi şehirde fazla kolay olabilir" önerisine (Volkan iletti)
Karar: Üç öneri de kabul; gerekçe ve ölçüler [ADR-0008](../decisions/adr-0008-farazi-cesitlilik-saf-tahmin.md). Rakamların benimkiyle tutuyor (şehir konutu CV şehir içi 0,08, havuz 0,13; seninki 0,14).
Senden beklenen: (1) `sinav.py faz2`'ye "saf tahmin" satırı: ölçülülerde Σ öğlen ÷ Σ abone × abone; geçme = model ortanca ve P90 saf tahminden ≥ %25 düşük [Yorum]; rakamla günlüğe. (2) Karşılaştırma betiğin `src/edp_kiyas.py` (senin, doğrudan main) + rakamlar günlüğe (CV, eğri benzerliği, saf tahmin farazi/gerçek), "gerçek veri — İspanya" etiketiyle. (3) `sinav.py faz1`'e bilgi satırı: konut trafolarında müşteri başına öğlen yükü CV, şehir içi ortanca ve havuz (ADR-0008 hedefi 0,3–0,4; yeniden üretimden sonra bakılacak). (4) Sunum cümlesi Faz 5'e BUILD yazar. Üreticideki mahalle çarpanı BUILD'de.
Durum: yapıldı — (1) saf tahmin maddesi PR #14; (2) `src/edp_kiyas.py` main (8435348, 6ff169c) + günlük; (3) faz1 CV satırı PR #14 (1.2'de 0,32, havuz 0,43)

## KARAR 31 Eki 15:12 — 13:55'teki "İspanya EDP türetme betiği" kararı iptal
Karar: `src/edp_oku.py` gerekmiyor: BUILD, PR #10'da (`src/edp_test.py`) ham sayaç verisinden doğrudan koştu, üstelik trafo başı ölçüm cihazlarını (ZIVS… sayaçları) buldu ve ondalık virgül hatasını düzeltti; PR #10 günlüğünü oku (docs/log/2026-10-31-volkan-edp-gercek.md). TD009456 ham veride doluymuş, OpenDSS profilinde sıfır; günlüğüne bir satır düşersin.
Senden beklenen: hiçbir şey; yukarıdaki (2) ile yetin.
Durum: bilgi — TD009456 satırı günlüğe, KAYNAK.txt'ye ve veri sözlüğüne eklendi (eac1fe7)

## BİLGİ 15:29 — karar masasından — İngiltere gerilim verisi adayı (UK Power Networks, PV bağlantı aracı doğrulaması)
Ne: Volkan'ın sorusu üzerine araştırıldı; veri sözlüğü "Adaylar"a satır olarak girsin (senin dosyan), **indirme şimdi değil** (sunum öncesi zaman yok; pilot öncesi Faz 3 doğrulaması için). Gerçekler [Kaynaklı: UKPN "Validation of PV Connection Assessment Tool" kapanış raporu v1.1, Mart 2015, Ofgem; veri sayfası London Datastore]:
- 20 ikincil trafo (18'i yüksek PV'li, 2'si PV'siz; kırsal + banliyö, EPN/SPN bölgeleri, Londra değil; 50–1.000 kVA; havai Cu'dan 300 mm² yeraltı Al'a kablo çeşidi) + 10 PV'li ev (6'sı izlenen trafoların hat ucunda; 10'unda net alış/veriş, 6'sında üretim ayrı ölçülü). Her AG fider çıkışında ayrı cihaz (57 cihaz): V, I, P, Q, THD faz faz; 9 trafoda hava istasyonu (ışınım 30 dk).
- Dönem 27 Tem 2013 – 19 Kas 2014 (480 gün). **Dikkat:** 10 Haziran 2014 öncesi 10 dakikalık ölçümler saatlik en düşük/en yüksek olarak toplulaştırılmış; tam 10 dk veri yalnız Haziran 2014 sonrası (ortalama 157 gün), 1 dk 18 Haz–7 Eyl 2014. Bahar öğleni için elde yalnız saatlik min/maks var (öğlen en düşük için yeterli).
- Erişim: CC BY 4.0, kayıtsız; "PV Data" zip 783,5 MB + hava xlsx 19 MB. Veri sayfasında müşteri sayısı, kVA, hat boyu yok; raporun site tablosunda var (Tablo 3; PDF metninden çıkmadı, tablo elle okunmalı).
- Raporun bize doğrudan yarayan rakamları (indirmeden, sunumda atıfla kullanılabilir): (1) Trafo çıkış (bara) gerilimi siteler arası ve zaman içinde çok değişken; tasarım varsayımı 248 V (gözlenen ortancanın bir standart sapma üstü, %84), 251 V riski sıfırlar; İngiltere yasal üst sınır 253 V → pay ~5 V. Bizim 246–250 V + 259 V sınırı aynı mantık. (2) "PV hat boyunca ölçülebilir gerilim yükseltti ama hat ucu gerilimi asıl OG regülasyonu ve trafo bara gerilimine bağlı" → ADR-0002'nin "trafo çıkışı belirleyici" varsayımına gerçek veri desteği. (3) Gündüz en düşük talep müşteri başına 200–400 W (Low Carbon London, ~5.600 sayaç); tasarım 200 W/müşteri (≥10 müşteri), <10 müşteride 0 → bizim şehir konutu 330 W/abone [Hesap, 20 farazi şehir] bu aralıkta. (4) Tek fazlı PV faz dengesizliği varsayımı: kentsel %25, kırsal %50 (ölçülen yük dengesizliğinden; ortalamanın bir sapma üstü). (5) En yüksek PV'li sitelerde bile yasal sınır aşılmadı; ölçülen gerilim yükselmesi örneği %0,87 (~2 V).
- Diğer İngiltere adayları: SPEN "Flexible Networks" (Strathclyde): 150+ ikincil trafo, 10 dk V/I/P/Q, Ara 2012–Eyl 2015, kayıt + onay gerekli, lisans belirsiz, PV odağı yok. NGED "LV Load Monitor Data": 301 trafo CSV, bazıları girişli, çözünürlük sayfada yazmıyor (Volkan kaydı). ENWL LVNS (200 trafo, 2013–14) açık değil. Low Carbon London: 5.567 ev, 30 dk, 2011–14, CC BY; ev düzeyi, trafo değil.
Neden: İspanya gerilim vermiyor; gerilim fiziğini gerçek veride sınayabilecek tek açık set bu. Ama yalnız 20 trafo, İngiltere şebekesi (230 V nominal, çoğu yeraltı Al), bahar verisi saatlik; bizim ABC70/95 havai Kıbrıs hattına fizik taşınır, rakam taşınmaz.
Senden beklenen: veri sözlüğü "Adaylar"a satır (yukarıdaki rakamlarla), KAYNAK yok (indirilmedi). Başka bir şey değil.
Durum: yapıldı (eac1fe7) — veri bu arada indirildiği için (6fde357, KAYNAK.txt var) satır "Elimizde" altında; PR #11 sonucu ve 16:27 kararı eklendi

## KARAR 16:50 — iş sırası (yeniden planlama; kartlar BUILD'den gelecek, beklemeden başla)
Karar: Sıra: (1) PR #8'i GitHub'da onayla (sözleşme kısmı, 5 dk); (2) `sinav.py`: `V_ALT = 207.0` + Faz 2'ye "saf tahmin" satırı (ADR-0008) + aday = 0 ayrımı zaten yaptın; (3) `docs/sunum/` klasörünü aç: slayt listesi, kaynak slaydı, dürüstlük cümleleri, itiraz slaydı (ROADMAP Faz 5; rakamlar: farazi %8,6 üst sınır, İspanya %25 → fatura ile %10, İngiltere 6 hatta 4'ü ±%40, Kıbrıs pilot); (4) Faz 3 kartı gelince `sinav.py faz3` (yanlış yeşil / yanlış kırmızı / kaç ev hatası / sarı oranı; %40 kuralı yan yana) ve `grafikler.py` kilit grafiği; (5) `src/edp_kiyas.py` + günlük; (6) veri kontrol listesi. Gerçek `tahmin.csv` ve `kac_ev.csv` BUILD'den gelince sınavları koş, rakamları günlüğe.
Neden: Sunum yarın; Faz 2 kapanışı, Faz 3 ölçüleri ve sunum iskeleti aynı akşama sığmalı; en kısa yolu olan işler önde.
Senden beklenen: yukarıdaki sıra; takılırsan kutu.
Durum: (1) (2) (3) (5) (6) yapıldı (PR #14, 83b0f11 sunum, 8435348 edp_kiyas); (4) Faz 3 kartı geldi, sıradaki iş

## BİLGİ 17:00 — karar masasından — Muhittin'in cevabı sunuma ve sınava nasıl giriyor
Ne: Sunum iskeletinde hikâye "güven merdiveni" (dört basamak, her birine tek iddia + tek rakam, hepsi "saf tahmine göre ne kadar iyi"); manşet rakam **İspanya %25 → %10**, farazi %8,6 destek. Dürüstlük cümlesi: "gerilimde 6 hattın 4'ü ±%40, 2 ıskalama uca kümelenme → karamsar senaryo". Faz 3 sınavındaki yanlış yeşil ölçüsü aynen; ADR-0010 yeşil kuralını (karamsar + marj + yüksek güven) BUILD `kac_ev.py`'ye koyuyor, sen ölçersin. `edp_kiyas.py`'ye sunum sonrası ek: korelasyon matrisi ve P90/P95 (ADR-0009), şimdi değil.
Senden beklenen: sunum iskeletini buna göre kur; başka iş yok.
Durum: bilgi — sunum iskeleti güven merdiveniyle kuruldu (83b0f11)

## UYARI! 31 Eki 17:03 — Volkan'dan (BUILD oturumu) — PR #12: sözleşme 1.2 onayı + yeni şehirler + KAYNAK satırı
Ne: (1) PR #12 (https://github.com/volkanGRGN/KKTC-hackathon/pull/12) sözleşme 1.2: `trafolar.csv` → `yillik_tuketim_mwh`; `cevap_anahtari.csv` → `mahalle_carpani`, `saat_kaymasi_dk`; bayramlar `tatil` (14 günde 4–7 tatil); `v0_v` 244–252; gerçek veri 800–899; `ayar.json` bilgi anahtarları. Sözleşme kısmını onayla (ya da Civan). `sinav.py`'nin okuduğu sütunlar değişmedi, yalnız eklendi. (2) Yeni şehirler (dalda ya da birleşince): önce iki indirme, sonra `python3 src/sehir_uret.py 1 20` ve `python3 src/sablon.py data/synthetic`. Benim ölçümüm: `sinav.py faz1` (207 V) 5/5 geçti; Faz 2 sınav şehirleri faturalı %3,9 / P90 %8,3, faturasız %22 / %55 (günlük: docs/log/2026-10-31-volkan-uretici-1-2.md). (3) **Senin dosyan** `data/raw/open-meteo-lefkosa/KAYNAK.txt`'e 2023 satırı (ben indirdim, sen yaz): `lefkosa_saatlik_2023.csv`, aynı adres `start_date=2023-01-01&end_date=2023-12-31`, 31 Ekim 16:30, 386.495 bayt, SHA-256 8cd56dd0d088e9ee4bff138ddc19a91be8931a9701ace92667af3a48771f4889; sağlama yatay 1.903, 30° güney 2.102 kWh/m², Nisan 11–14 eğik ortalama 754 W/m²; ilk denemede sunucu zaman aşımı verdi. (4) Saf tahmin tanımı için karar masasına öneri yazdım (volkan.md 17:03): Σ abone yerine tarife enerjisi / fatura. Karar gelene kadar ADR-0008 tanımını koş, yanına bu ikisini de koyarsan iyi olur.
Dosya: docs/data/tablo-bicimi.md (PR #12), data/raw/open-meteo-lefkosa/KAYNAK.txt
Neden: sözleşme değişikliği Can ya da Civan onayı ister; KAYNAK senin dosyan.
Durum: yapıldı — (1) PR #12 onaylandı; (2) 1.2 şehirleri üretildi, Faz 1 5/5, Faz 2 7/7; (3) KAYNAK.txt 2023 satırı (8290893); (4) iki tanım bilgi satırı (PR #14): tarife %25,2 / %67,2, fatura %5,5 / %15,2, model ikisinden de ≥ %25 düşük

## UYARI! 31 Eki 17:17 — Volkan'dan (BUILD oturumu) — Faz 3 kartın hazır; sunum iskeletine yeni rakamlar
Ne: (1) Kart: docs/gorev/can-faz3-sinav-grafik.md (`sinav.py faz3` + kilit grafik). `kac_ev.py` PR #13'te (#12'nin üstünde); birleşene kadar `kac-ev/ilk-surum` dalından üret. (2) Sunum iskeleti için (ROADMAP Faz 5 "güven merdiveni" main'de): manşet İspanya %25 → %10 (PR #10); gerilim 6 hattın 4'ü ±%40 (PR #11); farazi 1.2 faturalı %3,9 / faturasız %22 (destek, üst sınır); **kilit grafik: dolu trafoya "yer var" — biz 0/21, %40 kuralı 41/284 (%14)** (sınav şehirleri 11–20, gösterim). Hepsi senin resmi ölçümünle teyit edilecek.
Dosya: docs/gorev/can-faz3-sinav-grafik.md, ROADMAP.md (Faz 5)
Neden: karar masası 16:50 iş sırası (4) ve 17:00 BİLGİ.
Durum: yapıldı — (1) `sinav.py faz3` + kilit grafik PR #14, günlük docs/log/2026-10-31-can-faz3.md, kaç ev maddesi KALDI (tanım sorusu volkan.md 15:50); (2) sunum iskeletine işlendi (slayt 5: 1.2 %3,9 / %22; slayt 10: kilit grafik 0/21 ↔ 41/284 teyit edildi)

## KARAR 17:26 — `sinav.py faz2` saf tahmin satırının kesin tanımı (ADR-0008 madde 1 düzeltmesi)
Karar: İki saf tahmin, model hangi bilgiyle koştuysa onunla karşılaştırılır: **faturasız** → ölçülü trafolarda Σ öğlen en düşük ÷ Σ tarife enerjisi × trafonun tarife enerjisi (tarife enerjisi = sınıf başına abone sayısı × sınıfın yıllık ortalaması, `sehir_uret.py` SINIFLAR; Kıb-Tek bunu bilir); **faturalı** → Σ öğlen ÷ Σ `yillik_tuketim_mwh` × trafonun `yillik_tuketim_mwh`. Geçme: modelin ortanca ve P90 hatası ilgili saf tahminden ≥ %25 düşük. "Σ abone" tanımı kaldırıldı (karışık şehirde otel = 1 abone, anlamsız).
Neden: BUILD'in 1.2 ölçümü: Σ abone saf tahmini %176 hata veriyor, kıyas değil; tarife enerjili saf tahmin %23 / %82, faturalı %5,8 / %16. Model faturalıda geçiyor, faturasızda ortancada geçmiyor; ikisini de rakamıyla yaz, "KALDI" ise KALDI.
Senden beklenen: `faz2`'ye iki satır ("saf tahmin (tarife)" ve "saf tahmin (fatura)"), `sablon.py --faturasiz` koşusunu da ölç; günlüğe.
Durum: yapıldı — PR #14 @ d0207fb; faturalı GEÇTİ (saf fatura %5,5 / %15,2 → model %31 / %48 düşük), faturasız KALDI (saf tarife %22,9 / %62,2 → model %10 / %19 düşük); günlük + volkan.md 16:05

## UYARI! 31 Eki 17:32 — Volkan'dan (BUILD oturumu) — PR #14 birleşti; saf tahmin maddesi yeni tanıma geçsin
Ne: PR #14'ü inceleyip birleştirdim (Volkan'ın isteğiyle). Ölçümlerin doğru: faturalı 11–20'de %3,8 / %8,0, kapsama %83,9, arketip %98,2, şehirler arası 1,08 / 1,81 benim ölçümümle birebir tutuyor (fark yalnız havuz / şehir ortancası). `faz1` 5/5. Bir düzeltme gerekiyor:
- **Madde 6 eski tanımla notlanıyor.** `src/sinav.py` (madde 6, "Σ öğlen ÷ Σ abone × abone") karar masasının 17:26 KARAR'ından önce yazılmış. Bu tanımla saf tahmin %172 hata veriyor, madde her zaman geçiyor. Yeni tanım: faturasız koşuda "Σ öğlen ÷ Σ tarife enerjisi × tarife enerjisi", faturalı koşuda "Σ öğlen ÷ Σ fatura × fatura"; model hangi bilgiyle koştuysa o (`sablon_ozet.json` `fatura_kullanildi`). Σ abone satırı çıkabilir ya da bilgi satırına iner. Somut örnek: `sablon.py --faturasiz` ile koşulan 11–20'de madde 6 şu an `[GEÇTİ]` yazıyor; doğru kıyasla model %20,6 / %50,7, saf tarife %22,9 / %62,2 → yalnız %10 / %19 iyi, **KALDI** olmalı. Faturalı koşuda model saf faturadan %30,6 / %47,5 iyi → GEÇTİ.
- Küçükler: bilgi satırındaki "tarife enerjisiyle (Σ öğlen ÷ Σ abone × …)" etiketi "Σ tarife enerjisi" olmalı; düşük güven %100 olsa da `[GEÇTİ]` yazıyor (`[UYARI]` daha doğru); geçemeyen kıyasta "düşük" yüzdesi eksi çıkıyor (ör. "%-226.9"); `faz1` artık `veri_turu = gercek` şehirleri atlıyor (doğru, günlüğüne bir satır). `outputs/`'u `.gitignore`'a ekledim.
- Ayrıca `sablon_ozet.json`'da artık `saf_tahmin` (tarife / fatura: oran + ölçülülerde bir-dışarıda hata) var; sınav kendi hesabını yapmaya devam etsin, bu yalnız bilgi.
Dosya: src/sinav.py (madde 6 ve bilgi satırları)
Neden: karar masası 17:26 KARAR'ı (Faz 2 üç soru, madde 1); ROADMAP Faz 2 saf tahmin kutusu bu maddeye bağlı.
Durum: bekliyor

## BİLGİ 17:32 — karar masasından — sunum biçimi kararı (Volkan)
Ne: Sunum haritanın içinde 7 ekran (Civan), PDF yedeği senin metninden. 3→5 geçişi "noktalar çoğalıyor" animasyonu (civan.md 17:32): önce bir ölçülen trafo, sonra birkaçı, sonra tahmin adaya yayılıyor; ölçülen dolu, tahmin soluk nokta, renkler yeşil/sarı/kırmızı, "gösterim" etiketi. 3. ekran cümlesi öneri: "Her kutuya cihaz takmak çok pahalı. Birkaçını ölçüyoruz, gerisini tahmin ediyoruz; tahminin ne kadar emin olduğunu da söylüyoruz." 4. ekran güven merdiveni, manşet İspanya %25 → %10.
Senden beklenen: docs/sunum metnini 7 ekrana göre böl; PDF yedeği aynı metinden.
Durum: bilgi
