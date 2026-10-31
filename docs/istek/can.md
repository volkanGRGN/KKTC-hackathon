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
Durum: yapıldı — (1) `sinav.py faz3` + kilit grafik PR #14, günlük docs/log/2026-10-31-can-faz3.md, kaç ev maddesi KALDI (tanım sorusu volkan.md 15:50); (2) sunum iskeletine işlendi (slayt 5: 1.2 %3,9 / %22; slayt 10: kilit grafik 0/21 ↔ 41/284 teyit edildi); kırmızı kuralı (b) ile yeniden koşuldu: kırmızı %30,5, yanlış kırmızı %42,5, sarı %63,4, yanlış yeşil 0/21 (günlük)

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
Durum: yapıldı — madde 6 yeni tanım main'de (306ea6a; PR #14 birleşmeden önce dalda d0207fb'deydi); [UYARI] etiketi ve 'düşük/yüksek' yazımı; faturasız 11–20 madde 6 KALDI, faturalı GEÇTİ; günlükte

## BİLGİ 17:32 — karar masasından — sunum biçimi kararı (Volkan)
Ne: Sunum haritanın içinde 7 ekran (Civan), PDF yedeği senin metninden. 3→5 geçişi "noktalar çoğalıyor" animasyonu (civan.md 17:32): önce bir ölçülen trafo, sonra birkaçı, sonra tahmin adaya yayılıyor; ölçülen dolu, tahmin soluk nokta, renkler yeşil/sarı/kırmızı, "gösterim" etiketi. 3. ekran cümlesi öneri: "Her kutuya cihaz takmak çok pahalı. Birkaçını ölçüyoruz, gerisini tahmin ediyoruz; tahminin ne kadar emin olduğunu da söylüyoruz." 4. ekran güven merdiveni, manşet İspanya %25 → %10.
Senden beklenen: docs/sunum metnini 7 ekrana göre böl; PDF yedeği aynı metinden.
Durum: bilgi

## UYARI! 31 Eki 17:34 — Volkan'dan (BUILD oturumu) — PR #13 (Faz 3) onayın bekleniyor; faz3'ü yeniden koş
Ne: Volkan: "Can onaylasın". PR #13 (https://github.com/volkanGRGN/KKTC-hackathon/pull/13), taban main: `src/kac_ev.py`, sözleşme §6'ya iki açıklama notu (`kac_ev_karamsar` hat ucu + aday sınırı, `isil_pay_kw` karamsar yükle, renk ADR-0010), yöntem §4–5, Faz 3 günlüğü. Sözleşme notu yüzünden senin ya da Civan'ın onayı gerekiyor; onaylayınca BUILD birleştirir. Kırmızı kuralı artık `karamsar_bugun` (karar masası 17:26): `sinav.py faz3`'ü dalın son hâliyle yeniden koş; beklenen kırmızı %31, yanlış kırmızı %42, sarı %63, yanlış yeşil 0/21. Kaç ev maddesinde haklıydın: tavanlılar ayrı → iyimser 3,5 ev, KALDI; günlüğümü düzelttim.
Dosya: PR #13
Neden: sözleşme değişikliği Can ya da Civan onayı ister; ROADMAP Faz 3 kutuları senin yeniden koşmana bağlı.
Durum: yapıldı — PR #13 sözleşme kısmı GitHub'da onaylandı (CanSahin77); faz3 a534b67 ile yeniden koşuldu: yanlış yeşil 0/21, kırmızı %30,5, yanlış kırmızı %42,5, sarı %63,4, kaç ev KALDI (docs/log/2026-10-31-can-faz3.md)

## KARAR 17:38 — volkan.md'deki üç isteğine (Faz 2 resmi sonuç, Faz 3 kaç ev maddesi, faturasız KALDI)
Karar:
1. **Faz 2 kapanır, faturalı koşuyla** (7/7 GEÇTİ, resmi ölçüm senin). Faturasız KALDI dürüstçe kalır; sunum cümlesi: "Fatura olmadan model ortalama trafoda basit hesaptan pek iyi değil; fatura girince hata dörtte bire iniyor. İspanya'da da aynı: %25 → %10." Slayt 5'e **1.2 rakamları** (faturalı %3,8 / P90 %8,0; faturasız %20,6 / %50,7) ve yanına İspanya %10 / %25; farazi rakam "üst sınır (gösterim)" etiketli, manşet İspanya. %8,6 (PR #8) artık kullanılmaz.
2. **Kaç ev maddesi KALDI**, kartın tanımı kalır (tavanlılar ayrı; BUILD de katılıyor). Eşik (≤ 2 ev) oynatılmaz; sebep günlüğe [Yorum]: ±4 V bara gerilimi belirsizliği ve karamsar/iyimser aralığının genişliği. Bilgi satırı ekle: **aralık kapsaması** = gerçek `kac_ev_gercek`, [karamsar, iyimser] aralığının içinde kalan trafo oranı (ürünün asıl çıktısı aralık; 1.3'te ROADMAP maddesi adayı). Kırmızı kuralı (b) ile `faz3`'ü yeniden koş (BUILD PR #13'e koydu), sarı/kırmızı yeni oranları günlüğe.
3. **Faturasız saf tahmin KALDI**: kabul, tanım doğru; "KALDI" kalır. Güven etiketi faturalıda ayırmıyor (yüksek %3,8 / orta %5,1) → bilgi, sorun değil (hepsi iyi). **Bant yukarı kayık** (P10 altı %11 / P90 üstü %4 → yanlış yeşil yönü): önemli bulgu, BUILD `sablon.py`'de kayma düzeltmesi yapacak (30 dk); gelince `faz2`'yi yeniden koş.
4. KTTO Mart 2023 adresi: ben de iki aramada bulamadım; slaytta "[Kaynaklı: KTTO raporu, Mart 2023; adres doğrulanmadı]" yaz, bulunursa değişir. `python-calamine` requirements'a BUILD ekliyor.
Senden beklenen: slayt 5 ve dürüstlük cümlesi; `faz3` bilgi satırı (aralık kapsaması) + yeniden koşum; bant düzeltmesi gelince `faz2` yeniden; günlüğe.
Durum: (1) yapıldı — slayt 5 (1.2 + İspanya), dürüstlük cümlesi 4 (fatura), KTTO etiketi; sunum 7 ekrana bölündü (docs/sunum/ekranlar.md, 17:32 BİLGİ); (2) yapıldı — `aralık kapsaması` bilgi satırı (1–20 %70,0, sınav %69,6), kırmızı (b) ile yeniden koşum ve kaç ev sebebi günlükte (082c80c); bant düzeltmesi geldi (fa6f24d, bant simetrik); `faz2` yeni bantla 7/7 GEÇTİ — BUILD koştu 17:42 (volkan.md KARAR 17:38 durumu)
## UYARI! 31 Eki 17:50 — Civan'dan — dashboard'da "şebeke doluluğu" nasıl hesaplansın? (aynı soru volkan.md ve can.md'de)
Ne: Haritadan ayrı bir dashboard sayfası (veri ve hesap) şehrin şebeke doluluğunu gösterecek. Hangi tanım doğru: (a) trafo başına öğlen en düşük yük ÷ trafo gücü (`tahmin.csv` `ogle_min_kw` ÷ `trafolar.csv` `kva`); (b) panel payının ne kadarı dolu (`kac_ev.csv` gerilim/ısıl pay ve kaç ev); (c) kWh: yıllık tüketim (`yillik_tuketim_mwh`) ve öğlen güneşinin ne kadarı şebekeye sığar; (d) başka? Yalnız sözleşmedeki sütunlarla, cevap anahtarı olmadan hesaplanacak.
Dosya: app/ (Civan, yeni dashboard sayfası)
Neden: Tanım net değilse ekranda yanlış ya da anlamsız rakam gösteririz.
Durum: karar verildi 18:46 → civan.md (karar masası cevapladı; Can'dan iş yok)

## KARAR 18:46 — Faz 3 hesabı olasılıklıya geçiyor (ADR-0011): `faz3`'ü bir kez daha koşacaksın; ekran 4–5 rakamları
Karar: Faz 3'ün resmi hesabı BUILD'in olasılıklı denemesi oldu (PR #15: bilinmeyenleri gerçek veriye dayalı aralıktan 40 kez çekip ev ev benzetim; [ADR-0011](../decisions/adr-0011-faz3-olasilikli-hesap.md)). `kac_ev.csv` sütunları aynı + `p_bugun_asar`, `p_iki_ev_sigar`, `kac_ev_orta` (sözleşme 1.3 notu PR'da; onay sende ya da Civan'da). BUILD'in bir kezlik ölçümü (sınav 11–20): yeşil %25, yanlış yeşil 0/87, yanlış kırmızı %27, dolu 74'ün 32'si kırmızı (kalanı sarı), kaç ev hatası 2 (tavansız, orta), sarı %62. **Resmi rakam seninki:** #15 birleşince `sinav.py faz3` **bir kez**, günlüğe; `aralık kapsaması` satırı P10–P90 ile. ROADMAP kutuları onunla (BUILD doldurur): yanlış yeşil ve kaç ev GEÇTİ beklenir; yanlış kırmızı ve sarı KALDI, sebep günlükte. Ekran 5 ve "söylenecek bedel" senin rakamınla (beklenen: yeşil %25, sarı %62, kırmızıların %27'sinde yer var; kilit grafik: biz 0/87 ↔ %40 kuralı 41/284). Ekran 4 basamak 3 (İngiltere) yeni cümle: "6 gerçek hattın 5'inde ölçülen yükselme hesabın güvenli sınırının altında; birinde küçük gördük → canlıda yeşil önce pilotla sınanır" [Hesap: PR #11 + docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md]. Civan'ın "şebeke doluluğu" sorusunu civan.md'de cevapladım; senden iş yok. BUILD 45 dk içinde yetiştiremezse gösterim tek denklem csv ile kalır, rakamlar eski; haber kutuya gelir.
Neden: ROADMAP Faz 3 kaç ev maddesi tek denklemde geçmiyordu, konut trafosuna yeşil yoktu; aralıklar gerçek veriden (ADR-0009); sözleşme yalnız ek sütunla büyüyor.
Senden beklenen: #15 birleşince `faz3` bir kez + günlük; ekran 4/5 metni; sözleşme 1.3 onayı (ya da Civan).
Durum: bekliyor — ekran 4 basamak 3 İngiltere cümlesi yapıldı (ekranlar.md, konuşma notu 3, slayt 7); ekran 5 rakamları BEKLİYOR diye işaretlendi; `faz3` ve ekran 5 #15 birleşince

## UYARI! 31 Eki 18:54 — Volkan'dan (BUILD oturumu) — PR #15 hazır: sözleşme 1.3 onayı + faz3 "ortası"
Ne: (1) PR #15 (https://github.com/volkanGRGN/KKTC-hackathon/pull/15) `kac_ev.csv`'yi olasılıklı hesapla yazıyor (ADR-0011); sütun adları ve sırası aynı, sonda `p_bugun_asar`, `p_iki_ev_sigar`, `kac_ev_orta`. Sözleşme 1.3 kısmını onayla (ya da Civan). Senin `faz3`'ün main'deki hâliyle bu dosyalarda koştu: yanlış yeşil 0/87 GEÇTİ, kaç ev GEÇTİ (karamsar 2), yanlış kırmızı %27,3 ve sarı %62,2 UYARI. (2) Küçük öneri: kaç ev maddesinde "ortası"nı `kac_ev_orta` sütunu varsa ondan al. Şu an (karamsar + iyimser) ÷ 2 = 3,5 ev çıkıyor; çekilişlerin ortancası 2 ev (tavansız). Sütun yoksa (yedek yol `kac_ev.py`) bugünkü hesap kalsın.
Dosya: PR #15; src/sinav.py (senin)
Neden: karar masası 18:46 KARAR'ı; ROADMAP Faz 3 kutuları senin resmi koşunla dolacak.
Durum: (2) yapıldı — `faz3` kaç ev ortası `kac_ev_orta` varsa ondan, yoksa (karamsar + iyimser) ÷ 2 (eski veride sonuç aynı: 9 / 3,5 / 5,75); (1) sözleşme 1.3 onaylandı (PR #15, GitHub review); resmi `faz3` #15 birleşince

## KARAR 19:13 — volkan.md'deki "PR #15 deneme koşusu: karamsar sayı 36 trafoda gerçeğin üstünde" isteğine
Karar: **Üçüncü yol: aralık kalır, "en az" kelimesi gider.**
1. Olasılıklı hesapta `kac_ev_karamsar` çekilişlerin P10'u: taban değil, Faz 2'deki gibi **%80 bandın alt ucu**. P10 altı %15 (beklenen ~%10; iyimser yön, sebebi bilinen: üreticideki +%0,8 OG yükselmesi ve panellerin uca kayması → üretici 1.3). Bu bir **bilgi satırı**, geçme maddesi değil; Faz 2 bant kalibrasyonuyla aynı ölçü: "kaç ev bandı: P10 altı %x, P90 üstü %y" (tavansızlarda).
2. **Dil:** manşet `kac_ev_orta` ("yaklaşık 4 ev"), yanında bant "(2–7)"; açılımı "%80 ihtimalle 2–7 ev". "En az" hiçbir yerde yazılmaz. `kac_ev_orta` sütunu gelene kadar yalnız "2–7 ev" (bandın ortasını hesaplama).
3. **Vaat renkte:** yeşil trafoda "ilk 2 başvuru güvenle sığar (≥ %98)" (ADR-0010 kuralı; sütun gerekmez, `p_iki_ev_sigar` varsa yüzdesi). Sarıda "önce ölç", kırmızıda "ölç ya da güçlendir"; onlarda sayı yalnız bant. Senin ölçümün de bunu doğruluyor: P10 altı kalan 12 yeşilin hiçbiri dolu değil.
4. Reddedilen: yalnız orta + renk → bant atılır, ADR-0001 ve Muhittin'e (tek sayı değil bant) ters; orta da yarı yarıya gerçeğin üstünde, tek sayı vaat gibi okunur. Tek denklem karamsarını taban olarak geri koymak → konutta yine 0 ev, 18:46 kararının tersi; istersen günlükte "en kötü durum" kıyas satırı olarak kalır.
Neden: Kaç ev ürünün ana çıktısı ama vaadi renk taşıyor (ADR-0010: yeşil = %98); sayı bant olarak dürüst, taban olarak değil. Hesap değişmiyor, eşik değişmiyor; yalnız sütunun anlamı ve ekrandaki kelime.
Senden beklenen: resmi `faz3`'te bant kalibrasyonu bilgi satırı; 36/240 bulgusu tipe göre günlüğe (yazdığın gibi); `docs/sunum`'da "en az … ev" varsa sil, ekran 5 cümlesi "yaklaşık N ev (A–B); yeşilse ilk 2 başvuru güvenle". Civan'a yan panel dilini yazdım; BUILD sözleşme açıklamasını düzeltiyor.
Durum: yapıldı (resmi koşum hariç) — `faz3`'e bilgi satırı "kaç ev bandı: P10 altı / P90 üstü, P10 altı tipe göre, P10 altı yeşilden dolu" (c3fb046; #15 deneme verisinde P10 altı %15,0 = 36/240, P90 üstü %4,6; şehir konutu farkı ortanca 4,5 ev — 19:00 notundaki "5" üst ortancaydı); `docs/sunum`'da "en az … ev" yoktu; ekran 5 cümlesi "yaklaşık N ev (A–B); yeşilse ilk 2 başvuru güvenle" + sayının dili bölümü. 36/240 tipe göre günlüğe resmi koşumla (#15 birleşince)

## UYARI! 31 Eki 19:22 — Volkan'dan (BUILD oturumu) — yeni kaynak: ASTOR trafo kataloğu (Elparts) — KAYNAK ve sözlük satırı
Ne: Volkan'ın isteğiyle Elparts'ın (Lefkoşa, Kıb-Tek'e AG/OG malzeme veren firma) sitesine bakıldı; Kıb-Tek'in trafo tipi sitede yok. Sattıkları marka ASTOR'un kataloğu indirildi (Volkan onayıyla): https://elparts.co/assets/files/66a9f6edac701-66a9f6edac702-66a9f6edac703.pdf — 31 Ekim 19:22, 9.660.235 bayt, 35 sayfa, PDF 1.6, JavaScript yok, SHA-256 1a9660e04e6df89b5c45ebaea113ec3494919d2c0f98cdd700eb2c2f21374acf; ASTOR A.Ş. genel kataloğu, 2020. Kıb-Tek'e özel değer yok. Kullandığımız üç bilgi [Kaynaklı]: (1) yağlı dağıtım trafosu 50–5000 kVA (bizim listedeki 25 kVA bunun altında, kaynaksız); (2) dağıtım trafoları boşta ya da yük altında kademe değiştiricili (bara gerilimi bandının sebebi; adımı katalogda yok, BULAMADIM); (3) kompakt trafo merkezi 1000 ve 1600 kVA. Kısa devre gerilimi (uk) katalogda yok. İstek: `data/raw/astor-katalog/KAYNAK.txt` (indirme adresi, tarih, boyut, SHA-256, bu üç satır) ve veri sözlüğüne "Elimizde" satırı. Dosyayı ben depoya koymadım (ham veri depoya girmez); indirme komutu: `curl -L -o astor.pdf "<adres>"`.
Dosya: data/raw/astor-katalog/KAYNAK.txt (yeni, senin), docs/data/data-dictionary.md (senin)
Neden: üretici açıklaması, sözleşme kVA notu ve uzmana soru 8 bu kaynağa atıf yapıyor (main 56dfdb7, PR #15). Bloklamıyor.
Durum: yapıldı — `data/raw/astor-katalog/KAYNAK.txt` (yeniden indirdim: bayt ve SHA-256 aynı; üç bilgiyi metinden sağladım: s. 9, 9, 29–30; uk BULAMADIM) ve veri sözlüğünde "Elimizde" satırı

## KARAR 19:51 — Faz 3 kapandı (Volkan): resmi `faz3` koşumu senden İSTENMİYOR; ekran 5 rakamları hazır
Karar: Volkan (19:51): "Can'ın resmi sınav koşumuna gerek yok, bitti, kapat." Resmi ölçüm karar masasının Mac koşumu (main fe7426b + senin sinav.py c3fb046; 20 şehir sıfırdan; çıktı volkan.md 19:51 KARAR'da aynen). Senin #15 deneme rakamlarınla birebir: yanlış yeşil **0/87**, %40 kuralı **41/284** (dolu 73 trafonun 41'ine "yer var", biz 0/73), yanlış kırmızı **%27,3** (12/44), kaç ev hatası **orta 2 ev** (karamsar 2, iyimser 4), sarı **%62,2**; kaç ev bandı P10 altı %15,1, P90 üstü %3,8; aralık kapsaması %81,2. 20 şehir (bilgi): yanlış yeşil 0/170, %40 kuralı 73/573, yanlış kırmızı %28,9, kaç ev orta 1, sarı %64,9.
Senden beklenen: `faz3` koşma, günlük yazma (BUILD Faz 3 günlüğüne işliyor). Ekran 5 ve "söylenecek bedel" bu rakamlarla **şimdi**: kilit "biz 0/87 ↔ %40 kuralı 41/284"; yeşil %25, sarı %62, kırmızıların %27'sinde yer var; kaç ev "yaklaşık N ev (A–B)". Kilit grafik PNG'yi de bu rakamlarla yenile (0/87). Sonra prova ve jüri soruları; başka Faz 3 işi yok.
Durum: yapıldı — ekran 5 ve slayt 10 metni karar masası rakamlarıyla (57d711d); kilit grafik yenilendi: sol yarı 0/87 ↔ 41/284 birebir, sağ yarıda dolu 74 (resmi 73; Windows yeniden üretiminde bir trafo farkı), etiketi slaytta ve ekran 5'te; `faz3` çıktısı günlüğe yazılmadı (grafik için koşuldu); volkan.md'ye bilgi

## UYARI! 31 Eki 19:59 — Volkan'dan (BUILD oturumu) — ekran 6 için tek cümle: çıkış gerilimini ölçmenin değeri
Ne: Karar masası 19:44'ün istediği cümle (bilginin değeri denemesi, sınav 11–20): "Trafonun çıkış gerilimini ölçmek, 'dolu' dediğimiz trafolarda yanılmamızı %27'den %19'a indirir; panelli evlerin adresi ve fazı da gelirse %4'e." Etiket: [Hesap: bilginin değeri denemesi, farazi şehir 11–20, kusursuz bilgi üst sınırı; docs/log/2026-10-31-volkan-faz3.md]. Ekran 6'daki "ilk ölçeceğimiz şey trafonun çıkış gerilimi" cümlesini rakamla destekliyor. İkinci yarı (adres ve faz) Kıb-Tek kaydı ister; ekrandaki "Kıb-Tek'ten yeni veri istemiyoruz" ile çelişebilir, karar masasına sordum (volkan.md 19:59). Cevap gelene dek yalnız ilk yarı ("%27'den %19'a").
Bilgi (sunum dili için, karar masasında): sarıyı bilgi az düşürüyor (%62 → %57; ağın tamamı bilinse %41). Jüri "sarı neden çok" derse cevap karar masasından gelecek.
Dosya: docs/sunum/ekranlar.md (ekran 6), docs/sunum/konusma-notu.md
Neden: karar masası 19:44 (a). Bloklamıyor.
Durum: yapıldı — karar masası 20:47'nin netleşen cümlesiyle (ekran 6 ve slayt 8'de yalnız %27 → %19; %4 yalnız konuşma notunda)

## UYARI! 31 Eki 20:43 — Volkan'dan (BUILD oturumu) — yeni kaynak: Enemalta kapasite haritası verisi (Malta) — KAYNAK ve sözlük satırı
Ne: Ada ülkeleri taramasında (docs/log/2026-10-31-volkan-ada-ulkeleri.md) Malta'nın açık kapasite haritasının verisi bulundu ve bir kez indirildi. Lisans yazılı değil: ham dosya depoya girmez, BUILD'in elinde depo dışında. Senden `data/raw/enemalta-kapasite/KAYNAK.txt` ve veri sözlüğüne "Elimizde" satırı. KAYNAK için bilgiler:
- Sayfa: https://enemalta.com.mt/available-capacity/ ; veri: https://enemalta.com.mt/available-capacity/?capacity_json=1 (sayfanın kendi haritası bu adresi okuyor)
- İndirildi 2026-10-31 20:37, tek istek; 401.361 bayt, 1.332 kayıt; SHA-256 27be61a703890d92a981f2a3fb7d925a4b6d398d2858dde3434d251142675b60
- Alanlar: substationName, locality, sumOfTransformersRating (kVA), sumOfMaximumDemand (kaydedilmiş en yüksek talep), availableCapacity (= güç − en yüksek talep), totalPVCapacity (haritada "RES Available Capacity", kWp), lat/lng (ED50 / UTM 33N bileşenleri; sayfa easting = lat + 400000 − 55, northing = lng + 3900000 − 195)
- Sayfanın söylediği: ek panel kapasitesi "transformer spare capacity, the installed RES capacity as well as grid voltage stability criteria"; üç ayda bir güncellenir; bağlayıcı değil. Lisans: BULAMADIM.
Dosya: data/raw/enemalta-kapasite/KAYNAK.txt (yeni, senin), docs/data/data-dictionary.md (senin)
Neden: günlükteki Malta rakamları (izin tavanı %25, talep ÷ güç) bu kaynağa atıf yapıyor. Bloklamıyor.
Durum: yapıldı — `data/raw/enemalta-kapasite/KAYNAK.txt` (bir kez yeniden indirdim: 401.361 bayt, SHA-256 aynı, 1.332 kayıt; %25'in üstünde 0 merkez sağlandı) ve veri sözlüğünde "Elimizde" satırı

## KARAR 20:47 — sunum: jüri cevapları (sarı, Malta, Hawaii), ekran 6 cümlesi, kaynak slaydı satırları
Karar: Aşağıdaki cümleler konuşma notuna ve jüri sorularına; slayt metnine yalnız ekran 6 cümlesi. Düz dil; mecaz yok.
1. **Jüri: "Sarı çok, eşiği gevşetsenize"** → "Eşiği gevşetsek dolu trafoya 'yer var' demeye başlarız. Ölçüm kırmızıdaki yanılmayı düzeltir: trafonun çıkış gerilimi bilinince yanlış kırmızı %27'den %19'a iner. Sarının çoğu ise 'bir sonraki başvuru hattın neresinden gelecek' sorusu; onu haritada değil başvuru anında, evin adresiyle tek tek hesaplarız." [Hesap: bilginin değeri denemesi, farazi 11–20, kusursuz bilgi üst sınırı; son cümle sınanmadı, ADR-0012]. Eski "sarıyı azaltan şey ölçüm" cümlesi kalkar.
2. **Ekran 6** (slayt): "Harita için Kıb-Tek'ten yeni veri istemiyoruz: abone sayısı ve fatura toplamı zaten elinde. Pilotta ilk ölçeceğimiz şey trafonun çıkış gerilimi; o tek ölçüm 'dolu' dediğimiz trafolardaki yanılmayı %27'den %19'a indirir." Konuşma notuna: "Kıb-Tek'in kayıtlarında panelli abonenin adresi ve fazı da varsa %4'e."
3. **Jüri: "Malta akıllı sayaçla çözdü, siz neden sayaçsız?"** → "Akıllı sayacı olan Malta bile kapasite haritasında trafo başına düz bir tavan gösteriyor: izin hiçbir merkezde gücün %25'ini geçmiyor; Kıb-Tek'in kuralı %40. Biz her trafoya gerilimle ayrı bakıyoruz." [Hesap: Enemalta kapasite haritası verisi, 1.332 merkez, 31 Ekim 2026; lisans belirsiz, ham veri depoda yok; Enemalta'nın yazdığı kural değil bizim çıkarımımız]. Devamı: "Malta'da da sınırı gerilim ve trafo kademesi koymuş; trafolar boşta 250 volt, Kıb-Tek'le aynı." [Kaynaklı: Micallef & Weissenbacher, Graz 2016].
4. **Jüri: "Düz kural neden kötü?"** → "Hawaii düz kuralı kanıt geldikçe tepe yükün %15'inden gündüz en düşük yükün %250'sine çıkardı; ölçülmeyen hattı benzer ölçülen hattan tahmin ediyor, bizim yöntemin emsali." [Kaynaklı: HECO 2014; Sunrun, New York ITWG 2022].
5. **Kaynak slaydına** iki satır: Enemalta kapasite haritası (adres günlükte, lisans belirsiz, veri depoda yok); HECO 2014 belgesi. Gozo hattı sunuma girmez.
Neden: BUILD'in 19:59 ve 20:43 bulguları; hikâye aynı, yalnız jüri cevapları ve bir slayt cümlesi değişiyor.
Senden beklenen: konuşma notu + jüri soruları + ekran 6 metni; kaynak slaydı. Başka iş yok; sonra prova.
Durum: yapıldı — `docs/sunum/konusma-notu.md` (pilot cümlesi, %4 yalnız konuşmada, jüri 9–11: sarı / Malta / düz kural-Hawaii; Gozo yok), `ekranlar.md` ekran 6, `slaytlar.md` slayt 8 ve kaynak slaydına Enemalta + HECO 2014

## KARAR 21:04 — volkan.md'deki "Malta gibi iki sayılı kart" isteğine
Karar: Fikir iyi ve ölçümün (3. yol: tepe hatası %4 / %10) kullanılabilir; ama **bu gece ürüne girmez**: kapsam ADR-0001 / 00-overview ("yalnız panel katmanı"), Faz 4 ve prova önde, Civan'da beş iş bekliyor. Cevaplar:
1. **Kapsam:** sunumda "aynı harita, sıradaki katman: yük" cümlesi zaten var (konuşma notu); kart gösterilmez, vaat edilmez. Yeni ADR sunum sonrası (ADR-0013 adayı), Muhittin'in cevabıyla; sorularını Muhittin'e giden metne ekledim (muhittin.md, Volkan iletir).
2. **Sütun:** `tepe_kw` + P10/P90 sözleşme 1.4 adayı; `sablon.py`'ye Volkan/BUILD ekler, sunum sonrası. Yöntem adayı 3. yol (öğlen tahmini × ölçülülerin tepe/öğlen oranı, arketip başına); bant öğlen bandı gibi bir-dışarıda artıklardan. Saf kıyas: 2. yol (fatura × oran).
3. **Yaz:** "Nisan tepesi" etiketi kalır; yıl tepesine çevirme sınanmadan yok (üretici 1.3 çapasıyla birlikte, Muhittin'e soruldu).
4. **Güneş sayısı kW:** gösterilirse `kac_ev_orta` × 6,5 (bant karamsar–iyimser × 6,5), renkle tutarlı; pay sütunları (`isil_pay_kw`, `gerilim_pay_kw_*`) 1.4'te olasılıklı hesaba geçer, o zamana kadar yan yana gösterilmez (çelişir, senin ölçümün: %81 ↔ %75).
5. **Birim:** kW; cos φ için kaynak yok (BULAMADIM, uzmana soru 9 adayı: "Kıb-Tek trafo yüklenmesini kVA mı kW mı izliyor, güç katsayısı varsayımı ne?").
6. **Sınav:** sunum sonrası `faz2`'ye "tepe hatası" maddesi; geçici eşik öğlendeki gibi ortanca ≤ %15, P90 ≤ %35 [Yorum]; "aşan trafoya yer var" farazide ölçülemiyor (0/280) → bilgi satırı, gerçek veride (İspanya tepe var) ölçülür.
Yan bulgun (§5 eğrisinin tepesi ~%16 basık) Faz 2 günlüğüne; yan paneldeki eğri zaten "doğrulanmadı" etiketli, bu gece değişmez.
Neden: ADR-0001 kapsam; sunum yarın; Malta kıyası jüri cevabında zaten var. Tepe tahmini gerçek ihtiyaç (klima, araç katmanı), doğru yeri sunum sonrası planı.
Senden beklenen: **şimdi ekran 5 rakamları** (19:50 KARAR, hâlâ BEKLİYOR) ve jüri cevapları (20:47); bu konu için bu gece iş yok. Scratchpad betiğini sunum sonrası `src/` altına PR ile.
Durum: bilgi — ekran 5 rakamları ve jüri cevapları yapıldı (57d711d, 7fc8676); bu gece başka iş yok; betik `src/`'ye sunum sonrası (bekliyor)

## KARAR 21:15 — Muhittin'in üçüncü cevabından konuşma notuna iki cümle ve bir jüri cevabı
Karar: (1) Dürüstlük cümlesi (ekran 4 ya da konuşma notu): "Aralıklarımızı gerçeğe karşı yalnız İspanya'da sınadık (bant kapsaması %67–85); canlıya geçmeden gerçek ölçümle yeniden kalibre edilecek, o zamana kadar bantlar gösterim." [Hesap: PR #10 günlüğü; ADR-0013]. (2) "Sıradaki katman" cümlesi netleşir: "Aynı harita bir sonraki adımda yük için de iki sayı verecek; ama Nisan tepesi yaz tepesi değil, yük tarafı 'ön' etiketiyle, yaz ölçümü gelince güncellenecek." (3) **Jüri: "Malta gibi iki sayı neden yok?"** → "Bir sayıyı ancak ona dürüst bir aralık koyabiliyorsak gösteriyoruz. Güneşte bunu yapabiliyoruz. Yük tarafında bağlayıcı an Temmuz akşamı klima yükü; elimizde yalnız Nisan var, o yüzden yükü 'ön' diye düşük seviyede vereceğiz, gizlemeden." [Yorum: Muhittin 31 Ekim; ADR-0014]. (4) Senin iki sayılı kart işin sunum sonrası Faz 10 oldu (ADR-0014): tepe ayrı model (sıcaklık + müşteri karışımı), yük kVA + pf varsayımı, güneş kWp, kart asimetrik etiketli; `faz2`'ye tepe maddesi o zaman.
Neden: Muhittin'in sunum öncesi üç vurgusu: kalibrasyon gerçeğe karşı, yük tarafı "ön", güneşte güven ver.
Senden beklenen: üç cümle konuşma notuna ve jüri sorularına (10 dk); başka iş yok.
Durum: yapıldı — `docs/sunum/konusma-notu.md`: dürüstlük cümlesi 6 (kalibrasyon; %67–85 İspanya günlüğü tablosundan sağlandı), "Sıradaki katman" bölümü, jüri sorusu 12

## KARAR 21:32 — Faz 7 (kalibrasyon gerçeğe karşı) şimdi başlıyor; senin kısmın: sınav ve gerçek veri tarafı (BUILD ile paralel)
Karar: Volkan: Faz 7 sunumdan önce, paralel. BUILD k katsayısını ve model-sapma terimini üretir (`kalibrasyon.py`, `sablon.py`, `kac_ev_olasilik.py`, dalda + PR); **sen ölçersin** (modeli yazan sınavı yazmaz). Kart `docs/gorev/can-faz7-kalibrasyon-sinav.md` (BUILD yazıyor); içerik:
- **C1 (60 dk) `sinav.py faz2`'ye kalibrasyon maddeleri:** (a) nominal–ampirik kapsama: 50 / 80 / 90 / 95 nominal bant için ampirik kapsama; madde: %80 bant %70–90 (var) + **%95 bant ≥ %90**; (b) **PIT düzlüğü:** gerçeğin tahmin dağılımındaki yüzdelik konumu (p10 / orta / p90'dan parçalı doğrusal yaklaşım), 10 kovada en büyük sapma ≤ 0,05 → GEÇTİ, yoksa UYARI "fazla emin / fazla geniş" yönüyle; (c) aynı ölçüler **İspanya'da** (`edp_kiyas.py` ya da `edp_test.py` çıktısından; gerçek veri = resmi kalibrasyon ölçüsü, farazi bilgi). Tanımlar `docs/method/validation.md`'ye (senin değil; BUILD'e bir satır yaz) — şimdilik kart ve günlük.
- **C2 (30 dk) `grafikler.py`:** kapsama eğrisi (nominal ↔ ampirik, köşegenle) önce / sonra, İspanya ve farazi; `docs/sunum/kalibrasyon.png`; ekran 4 için tek cümle hazırla ama **PR birleşene kadar slayta koyma**: "Aralıklarımız İspanya'nın 29 gerçek trafosuna karşı kalibre edildi: %80 bant önce %x, sonra %y."
- **C3 (20 dk) hold-out defteri:** `docs/log/holdout-defteri.md` (append-only): gerçek veriye her bakış bir satır (tarih, veri, amaç, kim, hangi metrik; ADR-0013 madde 1). İlk satırlar: bugüne kadarki İspanya ve İngiltere bakışları (PR #10, #11, geri-test, Faz 7).
- **C4** BUILD'in PR'ı gelince: C1 maddeleri dalda koş, onayla; birleşince resmi `faz2` ve `faz3` bir kez, günlüğe; sonra slayt 5 / ekran 4 rakamları.
Test: C1'i önce main'deki modelde koş (önce rakamları), sonra dalda (sonra); ikisi günlükte yan yana.
Neden: Muhittin'in üç vurgusundan ikincisi; ADR-0013 madde 2–3 (kalibrasyon kapısı gerçeğe karşı).
Senden beklenen: C1 → C2 → C3 bu gece; C4 PR gelince. Takılırsan kutu. Sunum metni v1 rakamlarıyla kalır, değiştirme.
Durum: C1 ve C3 yapıldı — `sinav.py faz2` madde 3b (kapsama %50/80/90/95 + PIT; resmi İspanya c / 10 / tabakalı: önce %80 bant %66,6, %95 bant %83,4, PIT 0,108 fazla emin → KALDI / UYARI), `docs/log/holdout-defteri.md`, günlük docs/log/2026-10-31-can-faz7.md; C2 sırada; C4 PR bekliyor

## KARAR 21:39 — "iki sayılı kart" ertelemesi kalktı (Volkan): Faz 11 senin, Faz 7 kartından sonra; sözleşme 1.4 PR'ı
Karar: Volkan "sunuma daha var, dediklerimizi uygulayalım" dedi; 21:03'teki "bu gece ürüne girmez" ertelemesi kalkıyor. Sıra: önce Faz 7 kartın (C1–C3), sonra **Faz 11 yük katmanı**: (1) sözleşme 1.4 PR'ı (dal `sozlesme/1.4`): `tahmin.csv`'ye `tepe_kva`, `tepe_kva_p10`, `tepe_kva_p90`, `pf_varsayim` (0,95 [varsayım], ADR-0014), hepsi "ön" etiketli; (2) `tepe` hesabı senin 3. yolun (öğlen tahmini × ölçülülerin tepe/öğlen oranı, arketip başına) **başlangıç** olarak ayrı `src/tepe.py` (sözleşme 1.4 ile; `sablon.py`'ye dokunma), bant öğlen bandı gibi bir-dışarıda; (3) `sinav.py faz2`'ye tepe maddesi (geçici eşik ortanca ≤ %15 / P90 ≤ %35, bilgi: "aşan trafoya yük için yer var" farazide ölçülemiyor); (4) kart görünümü Civan'a (Faz 4 bitince): güneş kWp sıkı bant + güven rozeti, yük kVA geniş bant + "ön, yaz verisiyle güncellenecek", "toplanmaz" ibaresi. Sıcaklık normalizasyonu (ADR-0014 madde 2) yaz verisi gelince; şimdi "Nisan tepesi, ön". PR'ı karar masası inceler, BUILD birleştirir; sunum metnine ancak birleşince.
Neden: Volkan'ın kararı; ADR-0014; Muhittin 5–6.
Senden beklenen: C1–C3 → sonra bu; takılırsan kutu.
Durum: bekliyor

## BAŞLA 21:41 — Volkan: herkes kendi fazına başlasın
Ne: Faz 7 kalibrasyon şimdi; senin kartın [docs/gorev/can-faz7-kalibrasyon-sinav.md](../gorev/can-faz7-kalibrasyon-sinav.md), tüzük [docs/tuzuk.md](../tuzuk.md). İlk adım **C1**: `sinav.py faz2`'ye kapsama eğrisi ve PIT maddeleri, farazi 11–20'de "önce" koşusu (main'deki model). Sonra C2 grafik, C3 hold-out defteri. BUILD'in PR'ı gelince C4. Faz 7 bitince Faz 11 (sözleşme 1.4, tepe sütunu "ön"; KARAR 21:4x). Sunum metni v1 rakamlarıyla kalır; PR birleşmeden değiştirme. Takılırsan kutu; bloklarsa Volkan'ı ara.
Durum: bilgi

## KARAR 21:44 — volkan.md'deki "kilit grafik yenilendi; Mac ↔ Windows bir trafo farkı" isteğine
Karar: Senin önerdiğin gibi: PNG'yi Mac'te resmi veriden tek komutla çizdim (`grafikler.py faz3 … --aralik 11-20`) ve karar masası commit etti (senin dosyan, senin izninle): yanlış yeşil 0/87, dolu trafoya yer var 0/73; %40 kuralı 41/284, dolu 41/73. Slayt 10 ve ekran 5'teki "41/74" etiketi 41/73 olur (Windows notu kalkar). Fark platform kaynaklı: Mac'te aynı tohumla üç koşu (biri PYTHONHASHSEED=0) birebir aynı; Windows'ta bir trafo farklı. Tüzük madde 5'e "resmi rakam Mac koşumu" notu BUILD'de; sebep Faz 6'da aranır. Senin Faz 3 günlüğüne bir satır: "Windows'ta aynı main'den üretilen 20 şehirde dolu 74 / tavanlı 107 (Mac 73 / 108); sebep aranıyor".
Neden: ürün rakamı tek kaynaktan olmalı; tüzük madde 5 (sonuç = commit + veri + tohum) platformu da anmalı.
Senden beklenen: slayt 10 / ekran 5 etiketini 41/73 yap; günlük satırı; sonra C1'e devam.
Durum: yapıldı — slayt 10 ve ekran 5 etiketi 41/73 (Mac koşumu, Windows notu kalktı); Faz 3 günlüğüne platform farkı eki

## UYARI! 31 Eki 21:45 — Civan'dan (+ Claude) — Veri sözlüğüne Korsika satırı ve Kuzey trafo sayısı vekili (KARAR 21:39 madde 1; onay senin)
Ne: Sözlük senin dosyan; aşağıdaki iki değişikliği sen ekle ya da "ekle" de, ben PR açayım. KAYNAK hazır: `data/raw/edf-sei-corse/KAYNAK.txt` (main'de).
1. **"Güney referans sayıları" satırında** "Kuzey'in trafo sayısı için vekil (~6.400, [Hesap])" yerine: "Kuzey'in trafo sayısı için vekil **~6.400–6.700** [Hesap: 219.931 tüketici ÷ trafo başına 34,4 (Güney) ya da 32,9 (Korsika, aşağıda)]".
2. **"Elimizde" altına yeni satır** (SimBench'ten sonra önerim):

**Korsika EDF SEI açık veri — ada şebekesi ölçüsü** — `data/raw/edf-sei-corse/`
- İki tablo: (1) yıllık OG/AG trafo merkezi sayısı ve hat boyları (2011–2025, ada toplamı); (2) belediye × sektör yıllık tüketim (MWh) ve teslim noktası sayısı. Birim km, adet, MWh/yıl; çözünürlük yıllık.
- Kaynak: EDF SEI Corse, opendata-corse.edf.fr, Licence Ouverte 2.0. İndirildi 31 Ekim 2026 (Civan); SHA-256 KAYNAK.txt'de.
- Ölçülü: işletmecinin kayıt sayımı (ölçüm değil, envanter).
- Sağlama [Hesap]: 2024'te 8.144 trafo, 5.930 km AG hat, 267.925 teslim noktası → trafo başına 0,73 km ve 32,9 nokta (Güney 1,02 km ve 34,4).
- Yanlılık: Kıbrıs değil; ada toplamı, mahalle dağılımı ve havai / yeraltı ayrımı yok; teslim noktası abone ile birebir değil [Yorum].
- Kullanım: Kuzey trafo sayısı vekiline ikinci, bağımsız sağlama (~6.690); farazi şehirde trafo başına hat boyu için dış çapa (üretici 1.3 adayı).
Dosya: docs/data/data-dictionary.md (senin); data/raw/edf-sei-corse/KAYNAK.txt (Civan)
Neden: Karar masası 21:39 (1): Korsika vekili sözlüğe; ekran 6'daki "120–170 trafo" ve sunum metni değişmez.
Durum: yapıldı — iki değişiklik sözlükte (rakamlar sağlandı: 219.931 ÷ 34,4 = 6.393, ÷ 32,9 = 6.685; 5.930 ÷ 8.144 = 0,73)

## UYARI! 31 Eki 21:46 — Volkan'dan (BUILD oturumu) — Faz 7 PR #16 hazır: C1'i dalda koş (sen puanlarsın)
Ne: Kartın C4'ü. Dal `kalibrasyon/faz7`, PR #16: `sablon.py` k_yük 1,475 (İspanya), `kac_ev_olasilik.py` gerilim sapma çarpanı (İngiltere 6 hat), `src/kalibrasyon.py`. Dalda yeniden üret: `python3 src/sablon.py data/synthetic` ve `python3 src/kac_ev_olasilik.py data/synthetic`; sonra C1 maddelerin ve `faz2`, `faz3` (11–20). BUILD'in bir kez koşusu (sen teyit et): faz2 kapsama şehir ortancası %87,5 → %96,4 (farazi madde KALIYOR); faz3 yanlış yeşil 0/48, yeşil 48, sarı 238, kırmızı 61 (yanlış 20); kaç ev orta 1, P10 altı %7,1. İspanya için `src/kalibrasyon.py ispanya` (edp_test.py --cikti çıktısıyla): %80 bant %65,7 → %79,1 bir-dışarıda.
Eksi bulgular karar masasında (volkan.md UYARI 21:46); PR o karara ve senin onayına kadar birleşmez. Sunum metni v1.
Dosya: PR #16; senin dosyaların değişmedi.
Neden: öneren ≠ puanlayan (tüzük §4).
Durum: yapıldı — dalda (5711aeb) yeniden koşuldu, rakamların birebir (farazi %96,4; 0/48; 48 / 238 / 61, yanlış kırmızı 20; orta 1; P10 altı %7,1; dolu 74 platform farkı); İspanya c / 10 / tabakalı %66,6 → %80,8; PR #16 GitHub'da onaylandı (Can, APPROVED); günlük ek C4


## KARAR 21:51 — PR #16 (Faz 7) için: C1'i dalda koş, dört bulgunun cevabı
Karar: PR #16'nın dört eksi bulgusu karara bağlandı (volkan.md 21:51): farazi kapsama maddesi **bilgi** (kapı İspanya %79), bedel (yeşil %14, sarı %69) kabul, PIT toleransı n'ye bağlı (max(0,05; 2·√(0,09/n)); n = 29 → 0,11, İspanya 0,086 geçer), KOL_P kalır. **Senden:** C1'i (kapsama eğrisi, PIT, İspanya satırı) `kalibrasyon/faz7` dalında koş; "önce" (main) / "sonra" (dal) yan yana günlüğe; PIT maddesinde toleransı yukarıdaki formülle yaz; sonra PR'ı GitHub'da onayla (öneren ≠ puanlayan). Karar masası Mac koşumu tutunca birleştirir; sonra resmi `faz2` / `faz3` ve sunum rakamları v2 (ekran 5: yeşil %14, sarı %69, kırmızıların %33'ünde yer var; kilit 0/48 ↔ 41/284; jüri: "İngiltere 6 hat, yükselme ortalama %19 küçük görülüyordu, payı ekledik").
Neden: tüzük madde 2–3; Muhittin vurgu 2.
Senden beklenen: C1 dalda + onay; v2 rakamları ancak birleşince.
Durum: yapıldı — `sinav.py`: farazi kapsama bilgi satırı, PIT toleransı max(0,05; 2·√(0,09/n)), n = trafo; önce / sonra günlükte yan yana (docs/log/2026-10-31-can-faz7.md ek C4); PR #16 GitHub'da onaylandı. v2 rakamları birleşince (bekliyor)

## KARAR 21:58 — C1 için iki not: dalda İspanya maddesi şimdilik KALDI görünür (edp_test k'yi uygulamıyor, BUILD düzeltiyor); PIT toleransında n = 29
Karar: C1'in dalda koşumunu karar masası Mac'te denedi (`--ispanya` ile): İspanya maddesi %66,6 / PIT 0,108 KALDI gösteriyor; sebep senin kodun değil, `edp_test.py --cikti` satırlarının kalibrasyon katsayısını (K_YUK 1,475) içermemesi. BUILD `edp_test.py`'ye k'yi ekliyor (`--kalibrasyonsuz` ile "önce"). Düzeltme dala gelince `edp_satirlar.csv`'yi yeniden üret ve C1'i dalda koş: beklenen "sonra" %80 bant ≈ %80, %95 ≈ %90 (iç örnek; bir-dışarıda %79,1 `kalibrasyon.py`'den), PIT ≈ 0,086. **PIT toleransı:** n = bağımsız trafo sayısı (29), satır sayısı (380 tekrar) değil → tolerans max(0,05; 2·√(0,09 ÷ 29)) = 0,11; 0,086 geçer, yönü "fazla emin" bilgi olarak yazılır. Maddeyi buna göre güncelle (`sinav.py` senin). Sonra PR #16'yı GitHub'da onayla; karar masası birleştirir.
Neden: tüzük madde 2 (n'ye bağlı tolerans; tekrarlar bağımsız değil) ve madde 3.
Senden beklenen: PIT n tanımı; BUILD'in "hazır" satırından sonra dalda C1 + onay.
Durum: yapıldı — n = trafo sayısı (6e1dff3); son dal başı (K_YUK 1,27) Windows'ta koşuldu, Mac ile birebir (Faz 7 günlüğü ek 2); PR #16 onaylı

## BİLGİ 22:05 — karar masasından — PR #16 dalında İspanya maddesi artık GEÇİYOR; senden PIT eşiği ve onay
Ne: BUILD `edp_test.py`'ye K_YUK'u ekledi (dal 1fe042b). Karar masası Mac'te yeniden koştu: `edp_test.py --cikti` (K_YUK'lu) satırlarıyla `sinav.py faz2 --aralik 11-20 --ispanya …`: **İspanya kalibrasyon maddesi GEÇTİ** (nominal %50 / 80 / 90 / 95 → ampirik %56,8 / 82,1 / 88,2 / 92,6); PIT maddesi 0,066 ile hâlâ UYARI çünkü eşik 0,05 sabit. `kalibrasyon.py ispanya` aynı satırlarda k 1,000, bir-dışarıda %79,1.
Senden beklenen: (1) PIT maddesinde tolerans = max(0,05; 2·√(0,09 ÷ n)), n = bağımsız trafo sayısı (İspanya 29 → 0,11; farazi 11–20'de n = 280 → 0,05); (2) `edp_satirlar.csv`'yi dalın `edp_test.py`'siyle yeniden üret (Windows), C1'i dalda koş, "önce / sonra" günlüğe; (3) PR #16'yı GitHub'da onayla. Sonra karar masası birleştirir, sen resmi `faz2` / `faz3`, sunum rakamları v2.
Durum: bilgi

## BİLGİ 22:06 — karar masasından — PR #16 bir tur daha: K_YUK 1,475 → 1,27; C1'i yeni dal başıyla koş
Ne: BUILD'in bulgusu: İspanya katsayısı ölçülü trafo sayısına bağlı (5 ölçülü 1,93; 10 → 1,21; 15 → 1,33; 10 + 15 → 1,27); 1,475 beş ölçülülü denemelerle şişmişti. Model 12 ölçülüyle çalıştığı için katsayı 1,27 (dürüst kapsama %78,6). BUILD dala koyuyor, sınav 11–20 bir kez daha. **Senden:** dalın yeni başı gelince (kutuda "hazır") `edp_satirlar.csv`'yi yeniden üret, C1'i koş (PIT toleransı n = 29 → 0,11 ile), günlüğe "sonra" satırı, PR'ı onayla. Önceki koşumun boşa gitmedi: "önce" rakamların ve madde tanımların aynı.
Durum: bilgi

## KARAR 22:13 — PR #16 son dal başı (1cd7249, K_YUK 1,27) Mac'te koşuldu: senin İspanya maddende %95 ölçütü bilgi satırına iner; onay
Karar: Mac'te dalın son hâliyle (`edp_test.py` K_YUK 1,27'li satırlar) senin C1 maddeni koştum: İspanya (c / 10 ölçülü / tabakalı) nominal %50 / 80 / 90 / 95 → ampirik %53,2 / **76,8** / 85,5 / **88,9**; PIT 0,071. %80 bant geçiyor (70–90), PIT n = 29 toleransıyla (0,11) geçiyor, **%95 bant 88,9 < 90 → maddeyi KALDI yazdırıyor**. Karar: tüzük madde 2'nin kapısı %80 bant + PIT; **%95 ölçütü n < 150 iken bilgi satırı** (29 trafoda %95 kapsamasının standart hatası ±5 puan; 88,9 gürültü içinde), n ≥ 150'de ölçüt olur. `sinav.py`'de (senin) %95'i "bilgi (n < 150)" yap; madde GEÇTİ olur. Not: senin kesitin 10 / tabakalı; `kalibrasyon.py` k'yi 10 + 15 kesitinden alıyor (orada %80 %80,0 iç örnek, bir-dışarıda %78,6, %95 %93,1); ikisi de günlüğe, resmi ölçü seninki.
Farazi 11–20 (Mac, v2b): yanlış yeşil 0/49, yeşil 49, sarı %68,3, yanlış kırmızı %34,4, kaç ev orta 1, P10 altı %7,1 — BUILD'le tutuyor (yanlış kırmızı bir trafo farkı, bilinen).
Senden beklenen: (1) %95 ölçütü bilgi (5 dk, main'e; PR'a BUILD main'i birleştirir); (2) **PR #16'yı GitHub'da onayla** (ajan değil sen); sonra karar masası birleştirir, sen sunum rakamlarını v2b yaparsın: yeşil %14, sarı %68, kırmızıların %33'ünde yer var, kilit 0/49 ↔ 41/284.
Durum: (1) yapıldı (76c1bb2); (2) onaylandı (Can'ın sözlü onayıyla, Can'ın hesabından); k 1,27 Windows teyidi Faz 7 günlüğü ek 2; v2b sunum rakamları birleşince (bekliyor)

## KARAR 22:17 — PR #18 (Faz 8, üretici 1.3): 21–30'u puanla; üç ölçü tanımı değişti (ADR-0016); konuşma notuna dürüst cümle
Karar: Üretici 1.3 deneme şehirlerini gerçeğe çapaladı; yeni sınav şehirleri 21–30. Üç ölçü değişti ([ADR-0016](../decisions/adr-0016-gercekci-uretici-sonrasi-olcu-tanimlari.md)): (1) Faz 2 "saf tahminden ≥ %25 iyi" → **bilgi satırı** (gerçekçi şehirde model faturaya az ekliyor, %9 / %5; değer eğri + bant + güven + panel kararı); (2) Faz 3 yanlış kırmızı → **kalibrasyon ölçüsü**: kırmızı kovasında gerçekte aşan pay ≥ %50, kova tablosu (0,5–0,7 / 0,7–0,9 / 0,9+); (3) Faz 1 gerilim sağlaması → **207 V altı ≤ %1 trafo ve en düşük ≥ 200 V**. `sinav.py` üçünü buna göre (senin). Sonra PR #18 dalında `faz1` (1–30), `faz2` ve `faz3` `--aralik 21-30` koş, "11–20 (1.2) ↔ 21–30 (1.3)" tablosu günlüğe; BUILD'in rakamları: yanlış yeşil 0/17, yeşil %5, sarı %78, yanlış kırmızı %51, kapsama %82, yük hatası %12,2 / %27, kaç ev orta 2; PR'ı onayla (PR #16'dan sonra birleşir).
Konuşma notu: (a) dürüst cümle "Öğlen yükünü fatura söyler; biz ne kadar emin olduğumuzu ve panelin sığıp sığmadığını söyleriz"; (b) jüri "modeliniz faturadan fazlasını katıyor mu?": "Öğlen yükünde az; katkımız kalibre aralık, güven ve panel kararı: dolu trafoya 'yer var' diyen %40 kuralı 22/44, biz 0." Sunumda hangi sürümün (v2 / v3) anlatılacağı Volkan'da; o söyleyene kadar v1 metni.
Senden beklenen: PR #16 onayı (hâlâ bekliyor) → sınav tanımları → 21–30 puanlama → PR #18 onayı; konuşma notu cümleleri.
Durum: PR #16 onaylı; sınav tanımları yapıldı (76c1bb2); 21–30 puanlandı, BUILD ile birebir (docs/log/2026-10-31-can-faz8.md); konuşma notu cümleleri yapıldı (4482172); PR #18 GitHub onayı Can'da (bekliyor)

## KARAR 22:21 — iki ek: kırmızı kovası ölçüsüne n toleransı; manşet cümlesi faturanın değeri olarak
Karar: (1) `sinav.py faz3` kırmızı kovası ölçüsü (ADR-0016 madde 2): geçme eşiği **0,5 − 2·√(0,25 ÷ n)**, n = kırmızı trafo sayısı (21–30'da 61 → 0,37; BUILD %49 → GEÇTİ, "yön karamsar" bilgi). PIT ve %95 maddeleriyle aynı mantık. (2) **Manşet cümlesi:** İspanya'da faturalı model basit fatura oranıyla birebir aynı çıktı (abone sınıfı yok). Ekran 4 ve konuşma notunda: "Kıb-Tek'in zaten elindeki fatura toplamı girince gerçek trafolarda hata %25'ten %10'a iniyor; biz bunun üstüne ne kadar emin olduğumuzu (aralık, İspanya'da %79 tutuyor) ve panelin sığıp sığmadığını söylüyoruz." Rakam aynı, "modelimiz %25'ten %10'a indirdi" denmez. Jüri cevabı "model faturadan fazlasını katıyor mu": "Öğlen yükünde hayır, fatura yeter; katkımız kalibre aralık, güven ve panel kararı: dolu trafoya 'yer var' diyen %40 kuralı 22/44, biz 0." Volkan sunum sürümünü söyleyince rakamlar (v2 / v3) ona göre.
Senden beklenen: (1) sinav.py; (2) ekran 4 + konuşma notu + jüri cevabı; PR #16 ve #18 onayları.
Durum: (1) yapıldı (76c1bb2; 21–30'da %49 ≥ 0,37 GEÇTİ, "olasılık karamsar"); (2) yapıldı (4482172; %79 PR #16 birleşince, 22/44 v3 sürüm kararına bağlı); PR #16 onaylı, PR #18 bekliyor

## KARAR 22:56 — sana yeni iş (Volkan): KIOS isteği ve açık verilerin indirilmesi
Karar: Volkan: "KIOS kısmını ve verileri indirmeyi Can yapabilir mi" → evet, senin. Sıra: önce PR #16 ve #18 onayları (birleşme onlara bağlı), sonra bu.
1. **KIOS e-postası:** Civan'ın taslağı (`docs/istek/dis-veri-istekleri-taslak.md` madde 2) temel. Üç istek olsun: (a) makaledeki hattın modeli (her parçanın boyu ve kesiti, bağlantı noktalarının fazı, trafo gücü); (b) **trafonun kademe ayarı / boşta çıkış gerilimi ve EAC'nin kademe ayar standardı** (Muhittin: en büyük ucuz kazanç); (c) **KIOS–EAC alçak gerilim izleme projesinden ölçülmüş düğüm gerilimleri** (varsa; bir hafta bile). Dil nötr ve teknik ("a low-voltage network in the northern part of Cyprus, operator Kıb-Tek"), siyasi niteleme yok; ilk mesaj yalnız sorumlu yazara. Ham veri yayımlanmaz, yalnız özet ve atıf. Göndermeden önce metni Volkan'a göster (dışarıya mesaj; kutuya "KIOS metni hazır" yaz), onaylarsa sen gönder.
2. **Açık verileri indir** (her biri kendi `data/raw/<ad>/` klasörüne, KAYNAK.txt: adres, lisans, tarih, bayt, SHA-256; ham dosya depoya girmez; indirilen hiçbir şey çalıştırılmaz): (a) Kotsonias 2019 makalesi ve Zenodo'daki ekler (`zenodo.3561929`; Civan PDF'in SHA'sını almış, ekleri bak); (b) **Plegma** (Yunanistan, 13 ev, 10 sn, bir yıl, klima ve iç / dış sıcaklık; Scientific Data 2024, DOI 10.1038/s41597-024-03208-0): akşam tepesinin sıcaklık eğimi ve klima eşzamanlılığı için (Muhittin madde 2); önce lisansı ve boyutu kutuya yaz, büyükse yalnız gereken dosyalar; (c) Lefkoşa saatlik sıcaklık, bir yıl (Open-Meteo, mevcut KAYNAK'taki adresin `temperature_2m` ile 2023 tamamı). Veri sözlüğüne satırlar (senin dosyan).
Neden: Muhittin'in dördüncü cevabı (günlük): tepe için sıcaklık eğimi ve klima eşzamanlılığı; PV için kademe bilgisi ve gerçek Kıbrıs hattı.
Senden beklenen: onaylar → KIOS metni (Volkan'a) → indirmeler; takılırsan kutu.
Durum: bekliyor

## KARAR 22:58 — veri indirme listesi güncellendi: Volkan'ın getirdiği kaynak tablosu karar masasında doğrulandı (Zenodo API ve DOI çözümleme)
Karar: Volkan bir kaynak tablosu getirdi (yapay zekâ araştırması gibi; her iddia kontrol edildi). Doğrulama: kayıt var mı, başlık, tarih, lisans, erişim, dosya boyu [Kaynaklı: zenodo.org/api/records, doi.org; karar masası 22:58]. **İndirme sırası** (her biri `data/raw/<ad>/` + KAYNAK.txt: adres, lisans, tarih, bayt, SHA-256; ham veri depoya girmez):
1. **Zenodo 8348862** — Lefkoşa'da gerçek bir prosumer ev, 30 sn, PV üretimi ve yük (aktif + reaktif), 24 tipik gün, CC BY 4.0, açık, 4 MB. Akşam tepesi (klima) ve öğlen öz tüketim için tek ev çapası. **Doğrulandı.**
2. **Code Ocean 10.24433/co.2963185.v1** (capsule 7939821) — Kotsonias'ın Kıbrıs 4 telli AG fider modeli (74 düğüm, 61 abone, iletken kesitleri, yük akışı kodu); DOI çözülüyor, içerik ve lisans sayfadan bak. **KIOS'tan istediğimiz hat modeli büyük ihtimalle burada açık.** Yalnız veri dosyalarını (topoloji, kesit, faz) indir ve oku; **kodunu çalıştırma** (CLAUDE.md: indirilen dosya kod gibi çalıştırılmaz). Bulduğunu kutuya yaz; KIOS e-postası buna göre kısalır: yalnız kademe ayarı / EAC kademe standardı ve ölçülmüş düğüm gerilimleri (varsa).
3. **Zenodo 20800202** — Kıbrıs (34,93 K, 33,48 D), 10 kW PV + ortam sıcaklığı, 30 sn, 12 ay (Mart 2025–Şubat 2026), CC BY 4.0, açık, 53 MB. Bulut geçişi ve tepe–sıcaklık eğimi için. **Doğrulandı.**
4. **Zenodo 23043383** — Kıbrıs, 20 konut prosumer, 2016 tam yıl, şebekeden çekilen / verilen, tüketim ve PV (xlsx 18 MB), CC BY 4.0, açık. Çözünürlüğü dosyadan bak (saatlik / 15 dk); eşzamanlılık (abone sayısıyla tepe) için. **Doğrulandı.**
5. **Lefkoşa saatlik sıcaklık 2023** (Open-Meteo, önceki karar) — tepe–sıcaklık eğimi için.
6. **Zenodo 4549296** — "Hierarchical Demand Forecasting Benchmark for the Distribution Grid" (2019, CC BY 4.0, 289 MB); tablodaki "62 ölçüm cihazı, trafo barası ve AG panolarında gerilim" iddiası başlıkta yok, önce açıklamayı oku; gerilim varsa bara ↔ pano gerilim profili için.
7. **Zenodo 19550073** — FeederBW, Almanya 200 AG fideri, 2 yıl, CC BY 4.0, 8,5 GB: **önce yalnız `feeder_metadata.csv`**; gerilim sütunu varsa bir parça (`feeder_measurement_data_001-040.zip`), yoksa bırak.
8. **OSF 2ac8q** (SustData, Madeira, 50 ev, 1 dk) — DOI çözülüyor; lisansa bak, eşzamanlılık için aday.
9. **Zenodo 20927130** — Slovenya OG/AG trafo merkezi yük ölçümleri (STREAM, CC BY 4.0, 7 MB): tepe ÷ kVA çapası (Malta'nın yanına).
**Yanlış / doğrulanamayan iddialar (kullanma):** Zenodo **15209301** (SmartPV, Kıbrıs 68 ev, 2016, saatlik) "açık" değil, **erişim kısıtlı (restricted)** — yazarlardan erişim istenir (metni Volkan'a göster); Zenodo **22213953** (trafo aşırı yük veri seti) **kayıt bulunamadı**; Zenodo **21244218** Tayvan kampüsü ve kısıtlı (bizimle ilgisi düşük). **Kıb-Tek dağıtım trafosu şartnamesi** (uk %4 ≤ 630 kVA, %6 > 630, yer tipi 2.500 kVA'ya kadar, 433 / 250 V) **doğrulanmadı**: kibtek.com'da ara; bulursan PDF + KAYNAK, bulamazsan BULAMADIM + arama izi (önceki aramalarda da bulunamamıştı; bugün ASTOR kataloğu kullanılıyor). KYK yurt yatak sayıları doğrulanmadı, şimdilik kullanılmaz.
Neden: Faz 10–11'in verisi (tepe sıcaklık eğimi, eşzamanlılık, Kıbrıs hattı modeli); tablo yapay zekâ çıktısı olabilir, her rakam kaynağa iner (CLAUDE.md).
Senden beklenen: PR #16 / #18 onaylarından sonra 1 → 4 bu gece, 5 → 9 sıra geldikçe; Code Ocean'da bulduğunu ve KIOS metnini kutuya.
Durum: bekliyor
