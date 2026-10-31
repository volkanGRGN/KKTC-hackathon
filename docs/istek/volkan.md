# Volkan için istekler

Burası Volkan'ın kutusu; yalnız o işler. Kalıp için [README](README.md).

## UYARI! 31 Eki 13:40 — Can'dan — Faz 1 sağlama eşiği: "pazar günü çarşı öğleni"
Ne: ROADMAP Faz 1 "pazar günü çarşı öğleni iş gününün yarısından az" sağlaması EAC verisiyle kalıyor: çarşı Nisan tatil/iş günü öğleni (11–14) 0,83. Eşik mi değişmeli, yoksa bu madde sağlamadan çıkıp şehir üreticisinde varsayım mı olmalı? Değer ayarlanmadı.
Dosya: ROADMAP.md (Faz 1 geçme sınavı), src/profiller.py `saglama()`
Neden: EAC'nin tam yıl serisi iki tipik günün tekrarı (cumartesi = pazar = bayram); pazar ayrı bilgi yok. Tatil/iş günü öğleni Nisan: küçük ticari 0,84, büyük ticari 0,77, küçük sanayi 0,75; küçük ticari diğer aylarda 0,68–0,84. Rakamlar: docs/log/2026-10-31-can-faz1.md. PR: https://github.com/volkanGRGN/KKTC-hackathon/pull/5
Durum: karar verildi 12:30 → can.md

## UYARI! 31 Eki 13:55 — Can'dan — sözleşmede kVA etiketi "Kaynaklı"
Ne: `docs/data/tablo-bicimi.md` (PR #4) §1 `trafolar.csv` `kva` satırında "direk 25/50/100/250/400 [Kaynaklı: Kıb-Tek şartnamesi, veri sözlüğü]" yazıyor. Senin kararınla şartname "kaynak bağlantısı yok, doğrulanmadı"; veri sözlüğü buna göre güncellendi. Etiket "[varsayım: Kıb-Tek şartnamesi, kaynak bağlantısı yok]" olmalı.
Dosya: docs/data/tablo-bicimi.md
Neden: kaynaksız rakam "kaynaklı" görünmesin (CLAUDE.md, veri etiketleri). Arama izi: docs/log/2026-10-31-can-faz1-veri.md.
Durum: yapıldı 12:23 (PR #4, 2a02a81; şehir üreticisindeki aynı not da düzeltildi)

## UYARI! 31 Eki 12:23 — Claude'dan (Volkan'ın oturumu) — Faz 1 parametresi: konut trafolarının yarısı bugünden dolu
Ne: Şehir üreticisinin ilk 20 şehrinde (yapay ışınım) konut + köy trafolarının %55'i bugünden 259 V üstünde; oran panel yaygınlığıyla artıyor: %11–14'te %9–21, %24–26'da %47–58, %36 üstünde %86–95. "Gerçek kaç ev" ortancası 0. Soru: panel yaygınlığı aralığı (%10–50) ya da trafo çıkış gerilimi aralığı (246–250 V) daraltılmalı mı, yoksa bu "Kıbrıs hatları sınırda" bulgusu olarak mı kalmalı? Değer değiştirilmedi.
Dosya: src/sehir_uret.py (ayar aralıkları; PR #6), ROADMAP.md Faz 1 rastgeleleştirme
Neden: Neredeyse her konut trafosu kırmızıysa Faz 3'ün yanlış yeşil ölçüsü ve harita az bilgi taşır; öte yandan aralıklar ROADMAP kararı. Rakamlar ve sebep: docs/log/2026-10-31-volkan-faz1.md (sehir/ilk-surum dalında, PR #6).
Durum: karar verildi 12:35 → volkan.md (KARAR aşağıda), ADR-0006

## KARAR 31 Eki 12:35 — volkan.md'deki "Faz 1 parametresi: konut trafolarının yarısı bugünden dolu" isteğine
Karar: Panel yaygınlığı aralığı %10–50 → **%3–25** (bugünün Kıbrıs'ına çapalı); trafo çıkışı 246–250 V değişmez; %55 bulgusu silinmez, yaygınlık bandına göre raporlanır. Gerekçe ve rakamlar [ADR-0006](../decisions/adr-0006-panel-yayginligi-bugunun-kibrisi.md).
Neden: Kıb-Tek 2023'te PV üretimi toplamın %5,81'i, 2024 Ocak–Temmuz %6,33 [Kaynaklı: kibtek-istatistik]; ~70 MWp kurulu [Hesap]; tamamı konut olsa bile abonelerin %6–8'i [Hesap], gerçekte santral ve ticari de içinde → ülke geneli konut yaygınlığı kabaca %2–6, bekleyen 2.670 başvuru +%1,5; mahallede kümelenme için üst sınır %25 [Yorum]. %10–50 geleceğin şehirlerini üretiyordu; Faz 3 sınavına renk karışımı lazım. Gerilim aralığı şartnameden ve ADR-0002'nin sınadığı şey, gizlenmez. "Mahsuplaşmadaki konut abonesi sayısı" BULAMADIM (web; Kıb-Tek PDF'lerinde yok) → uzmana soru.
Senden beklenen (ana oturum): ROADMAP Faz 1 rastgeleleştirme satırında "%10–50" → "%3–25 (ADR-0006)"; `src/sehir_uret.py` satır 406 `rng.uniform(0.10, 0.50)` → `(0.03, 0.25)` (PR #6); 20 şehri yeniden üret, günlüğe yaygınlık bandına göre "bugünden dolu" oranı; `docs/01-plan.md` "Uzmana sorulacaklar"a 6: "Kaç konut abonesi mahsuplaşmada (çatı panelli)?".
Durum: yapıldı 13:43 (BUILD: üretici 0.2 main'de 42eb5d1; ROADMAP ve plan güncel; 20 şehir yeniden üretildi, bant tablosu Faz 1 günlüğünün ek girdisinde: konut+köy bugünden dolu %27, yaygınlığa göre %10 → %55)

## UYARI! 31 Eki 14:35 — Can'dan — Faz 1 sınavı: üretim süresi 60 sn'yi aşıyor
Ne: 20 şehirde (`sehir/ilk-surum` @ 530ccb2, eski ayar %10–50, Windows i7-13700H) `sure_sn` ortanca 56,1 sn, en uzun 78,4 sn; 9/20 şehir > 60 sn → Faz 1 süre maddesi KALDI. Tek başına da uzun: sehir-020 81,0 sn, sehir-008 76,1 sn. Uzun sürenlerde abone ~1.500 ve kaç ev ortancası 6,5–8,5 (kaç ev sıraları uzuyor). Hızlandırma mı, eşik mi? Değer ayarlanmadı. Diğer 4 madde GEÇTİ, tohum sınavı GEÇTİ.
Dosya: src/sehir_uret.py (PR #6) ya da ROADMAP Faz 1 eşiği
Neden: geçme sınavı; rakamlar docs/log/2026-10-31-can-faz1.md (PR #5 dalında, f76edda). ADR-0006 (%3–25) girince kaç ev ve süre değişecek, yeniden koşarım.
Durum: karar verildi 13:00 → can.md

## UYARI! 31 Eki 14:35 — Can'dan — cevap anahtarı: kac_ev_sinir ile kac_ev_tavan çelişiyor (3 trafo)
Ne: `kac_ev_aday` = 0 olan 3 trafoda `kac_ev_tavan` = 1 ama `kac_ev_sinir` = `gerilim` (sehir-002 T03, sehir-010 T38, sehir-019 T14). Sözleşmede `yok` = tavan. Aday yoksa hangisi doğru: tavan 0 mı, sınır `yok` mu?
Dosya: src/sehir_uret.py, docs/data/tablo-bicimi.md §3
Neden: sinav.py `kac_ev_sinir` sayımı ile tavan oranı bu yüzden 318 / 321 farklı çıkıyor.
Durum: karar verildi 13:00 → can.md

## UYARI! 31 Eki 14:35 — Can'dan — bilgi: 105/800 trafoda v_max > 264 V; ayar.json CRLF
Ne: (1) Bugünkü panellerle 105/800 trafoda `v_max_bugun_v` > 264 V (inverterin kapandığı gerilim), 6'sında > 280 V, en yüksek 304,6 V; benzetim inverter kapanmasını modellemiyor. Faz 3 için "264 üstü gerçekte görülmez, üretim kesilir" notu gerekebilir. (2) Windows'ta `ayar.json` CRLF satır sonuyla yazılıyor (`open(..., 'w')` newline'sız); CSV'ler LF. Sözleşmenin LF kuralı yalnız CSV için; istersen ayar.json da `newline=''`.
Dosya: src/sehir_uret.py
Neden: bilgi; karar gerekmiyorsa "okundu" yeterli. Rakamlar Can'ın Faz 1 günlüğünde.
Durum: karar verildi 13:00 → can.md (okundu; iki küçük iş ana oturumda)

## UYARI! 31 Eki 13:43 — Claude'dan (BUILD oturumu) — Faz 1 eşiği: 216 V altı 3 trafo
Ne: Yeni ayarlarla (gerçek EAC + Lefkoşa ışınımı, yaygınlık %3–25) Faz 1'in beş maddesinden dördü geçti; "hiçbir trafo 216 V altı değil" maddesi 3/800 trafoda kalıyor: sehir-015 T36 otel 1000 kVA 247 m 211,4 V; sehir-012 T07 köy 100 kVA 794 m ABC70 214,9 V; sehir-017 T21 sanayi 400 kVA 497 m 215,4 V. Soru: eşik 207 V'a mı insin (EN 50160: 230 V −%10, 10 dakikalık ortalamaların %95'i için alt sınır), yoksa üretici mi değişsin (otel hattı kısalsın / köy hattında ABC95)? Değer değiştirilmedi.
Dosya: ROADMAP.md (Faz 1 geçme sınavı; şimdilik [~]), src/sinav.py (V_ALT, Can'ın), src/sehir_uret.py (TIPLER)
Neden: Maddenin amacı "benzetim bozuk değil"; üç trafo bozuk görünmüyor (büyük yük ya da uzun ince hat, akşam tepesi) [Yorum]. Önceki yapay ışınımlı 20 şehirde 0 idi. Rakamlar: docs/log/2026-10-31-volkan-faz1.md ek girdi. Faz 2'yi bloklamıyor.
Durum: karar verildi 13:55 → volkan.md (KARAR aşağıda) + can.md (V_ALT)

## UYARI! 31 Eki 14:20 — Can'dan — İspanya EDP kullanılabilir: gerçek doğrulama adayı (Faz 2, 2i)
Ne: EDP veri seti indirildi ve incelendi (zaman kutusu ~40 dk). 30 trafo (28 × 630, 1 × 1000, 1 × 250 kVA), 8.087 müşteri, **saatlik**, 1–21 Mayıs 2018. Müşteri → trafo eşleşmesi çıkarılabiliyor (ağ radyal; 8.073/8.087 yük tek trafoya); 29 trafonun saatlik toplam yükü elde, öğlen (11–14) en düşük 25–163 kW [Hesap]. Sınırlama: **tarife sınıfı / abone tipi yok** (yalnız müşteri sayısı, faz, kVA, hat boyu); TD009456 (251 müşteri) tamamen sıfır; kentsel, kuzey İspanya, Akdeniz değil. Eleme 4/5 → alındı.
Dosya: data/raw/edp-oviedo/KAYNAK.txt, docs/data/data-dictionary.md, docs/log/2026-10-31-can-faz2.md
Neden: Faz 2 kartı adım 3 ("kullanılabilirse Volkan'ın kutusuna"). Modeli EDP'de koşmak senin işin (2i); girdi yalnız toplam müşteri + kVA olabilir. İstersen trafo başına saatlik toplamı sözleşme biçiminde çıkaran küçük betiği ben yazarım; karar senin.
Durum: karar verildi 13:55 → can.md

## UYARI! 31 Eki 14:20 — Can'dan — sözleşme §5: arketipler.csv `oran` brüt mü net mi?
Ne: Faz 2 kartındaki "doğru arketip" ölçüsü trafonun gerçek kümesini `yuk_5dk.csv` **`tuketim_kw`** (brüt) iş günü eğrisinden bulup `arketipler.csv` `oran` ile karşılaştırıyor. Sözleşme `oran`ın hangi seriden (brüt `tuketim_kw` mi, sayacın gördüğü `net_kw` mi) çıktığını yazmıyor. `sablon.py` net üzerinden kümelerse ölçü yanlış arketiple karşılaştırır. Harita formülü (`oran` × `ogle_min_kw` ÷ öğlen en düşük `oran`) brütü ima ediyor. Öneri: §5'e "`oran`: brüt tüketim (`tuketim_kw`) eğrisi" satırı.
Dosya: docs/data/tablo-bicimi.md §5, src/sablon.py
Neden: iskelet uyumu; `sinav.py faz2` yazılmadan netleşsin. Bloklamıyor.
Durum: karar verildi 13:55 → can.md (brüt; PR #8 sözleşme 1.1)

## UYARI! 31 Eki 14:20 — Can'dan — bilgi: PR #6 okuma notları (birleşmeden önce bakıldı)
Ne: Engelleyen bulgu yok (ısıl sınır kVA ile doğru, ışınım saat kaydırması doğru, sütunlar sözleşmeyle birebir, tohumlar platformdan bağımsız). İki küçük not: (1) Bayramlar iş günü sayılıyor (yalnız cumartesi/pazar tatil): eski 20 şehrin 12'sinin penceresi 23 Nisan ya da 2024 Ramazan Bayramı'na (10–12 Nisan) denk geliyor, `isgunu` etiketli [Yorum: tarihler resmi kaynaktan doğrulanmadı]. Ya bayram listesi ya da "bayram yok sayıldı [Yorum]" notu. (2) `KVA_LISTESI` en büyüğü 1000; gerek büyükse sessizce 1000 seçiliyor: 800 trafonun 104'ü 1000 kVA (otel 49, çarşı 55); Nisan tepesi kVA'nın en çok %50'si, şimdilik etkisiz, yaz benzetilirse önemli.
Dosya: src/sehir_uret.py
Neden: bilgi; karar gerekmiyorsa "okundu" yeterli.
Durum: karar verildi 13:55 → can.md (okundu; notlar ana oturuma)

## UYARI! 31 Eki 13:51 — Claude'dan (BUILD oturumu) — Faz 2: Kıb-Tek trafo başına yıllık fatura tüketimini biliyor mu? (doğruluk önerisi)
Ne: Şablon modelinde ([PR #8](https://github.com/volkanGRGN/KKTC-hackathon/pull/8)) öğlen hatası ortanca %8,6 ama P90 %32,6 (eşik %30). Kalan hatanın çoğu tek büyük müşterili trafolarda: şehir konutu %4,5, köy %6,7, ama otel %21,5, yurt %22, çarşı %25, sanayi %22 (geliştirme şehirleri). Deneme şehrinde her büyük abonenin büyüklüğü rastgele (σ = 0,3); abone sayısı bunu göstermiyor. Öneri: `trafolar.csv`'ye `yillik_tuketim_mwh` (trafodaki abonelerin fatura toplamı) sütunu, üreticide abone başına yıllık enerji (+ Nisan ile yıl arasında küçük bir sapma, [Yorum]), model ölçeği bu sütunla. Değer değiştirilmedi, sütun eklenmedi.
Dosya: docs/data/tablo-bicimi.md (sözleşme sütunu), src/sehir_uret.py, src/sablon.py
Neden: Model zaten "hangi abone hangi trafoda"yı bildiğini varsayıyor (abone sayıları; uzmana soru 2); bunu bilen Kıb-Tek o abonelerin faturasını da bilir [Yorum]. İngiltere'nin şablon ölçeklemesi de müşteri sayısının yanında yıllık tüketimi kullanıyordu [Yorum: hatırladığım kadarıyla; doğrulanmadı]. Volkan: "doğruluk önemli". Bloklamıyor; Faz 3 mevcut modelle başlayabilir.
Durum: karar verildi 13:58 → volkan.md (KARAR aşağıda), ADR-0007

## UYARI! 31 Eki 13:51 — BUILD'den — Faz 1 kapandı, Faz 2 kartları yazıldı
Ne: Faz 1'in beş maddesi geçti; 216 V maddesi yukarıda karar bekliyor. ROADMAP kutuları ve günlük ek girdisi main'de. Faz 2: Can'ın kartı (docs/gorev/can-faz2-sinav-grafikler.md) ve Civan notu main'de; `src/sablon.py` PR #8'de (sözleşme 1.1, Can/Civan onayı). Ön bakış şehir 11–20: arketip %93, hata %8,6 / P90 %32,6, kapsama %82, düşük güven %18. Can'ın "arketip oranı brüt mü" sorusu: brüt, PR #8 sözleşmesine yazıldı. ADR-0006 KARAR'ı "yapıldı". DEVIR tazelendi.
Dosya: ROADMAP.md, DEVIR.md, docs/log/2026-10-31-volkan-faz1.md, docs/log/2026-10-31-volkan-faz2.md (PR #8), docs/gorev/can-faz2-sinav-grafikler.md
Neden: karar masasının Faz 1 kapanış / Faz 2 iş bölümü isteği; Volkan'a iletilsin.
Durum: Volkan'a iletildi 13:58 (karar masası)

## KARAR 31 Eki 13:55 — volkan.md'deki "Faz 1 eşiği: 216 V altı 3 trafo" isteğine (BUILD)
Karar: Eşik **207 V** olur (EN 50160: nominal 230 V −%10; haftalık 10 dakikalık ortalamaların %95'i için alt sınır [Kaynaklı: EN 50160]); üretici değişmez (eşiğe uydurmak için hat kısaltma yok). Üç trafo (211,4 / 214,9 / 215,4 V) standardın içinde kalır, bulgu olarak günlükte durur.
Neden: Maddenin amacı "benzetim bozuk değil"; 216 V ilk taslakta [Yorum] bir tahmindi, 207 V standardın alt sınırı. Üç trafo bozuk değil: uzun ince kırsal hat (794 m ABC70) ve büyük yüklü tek hat, akşam tepesinde. Ayrıca [Yorum]: yer tipi 630/1000 kVA trafolar (otel, sanayi, çarşı) kodda havai ABC95 ile besleniyor; gerçekte yeraltı kablo (SimBench NAYY 150/240, r 0,21/0,13 Ω/km, veri sözlüğü) → bu trafolarda düşüm ve yükselme 2–3 kat abartılı. Sözleşme `kablo` yalnız ABC70/ABC95; sürüm 1.2 adayı, şimdi değil (Faz 2'yi etkilemez, kümeleme şekle bakar).
Senden beklenen (ana oturum): ROADMAP Faz 1 satırı "216 V" → "207 V (EN 50160 alt sınır; karar masası 31 Ekim; ilk taslak 216)", [~] → [x], günlük bağlantısı; günlüğe üç trafo + yer tipi/ABC95 notu. `sinav.py` `V_ALT` Can'da (can.md'ye yazdım). Faz 1 böylece kapanır.
Durum: yapıldı 16:23 (BUILD) — ROADMAP Faz 1 maddesi [x] 207 V, Faz 1 günlüğüne ek girdi (üç trafo + yer tipi/ABC95 notu). Faz 1 kapandı.

## KARAR 31 Eki 13:58 — volkan.md'deki "Faz 2: Kıb-Tek trafo başına yıllık fatura tüketimini biliyor mu?" isteğine (BUILD)
Karar: Evet, ekle: `trafolar.csv`'ye `yillik_tuketim_mwh`; üretici abone başına yıllık enerjilerin toplamı × 0,95–1,05 fatura sapması [Yorum]; model sütun **varsa** kullanır, yoksa abone sayılarıyla (EDP'de yok); günlükte sütunlu/sütunsuz yan yana. Gerekçe [ADR-0007](../decisions/adr-0007-yillik-fatura-tuketimi-girdi.md). Soru: faturayı Kıb-Tek bilir; abone–trafo eşleşmesi BULAMADIM (uzmana soru 2), ama model o varsayımı zaten yapıyor, yeni varsayım yok.
Neden: Hata tek büyük müşterili trafolarda (%21–25), abone sayısı büyüklüğü göstermiyor; İngiltere de müşteri sayısının yanında yıllık tüketimle ölçekliyor [Yorum]. Ayrım kuralı korunuyor: fatura Kıb-Tek'in bildiği şey.
Senden beklenen (ana oturum): PR #8 olduğu gibi birleşsin (Can onayı; can.md'ye yazdım). Sonra ayrı küçük PR: sözleşme 1.2 (`yillik_tuketim_mwh` + gerçek veri `sehir` 800–899 satırı) + `sehir_uret.py` (sütun, bayram listesi, `kva_tavan_sayisi`; can.md 13:55 KARAR) + `sablon.py` (varsa kullan); 20 şehir yeniden; Faz 2 ölçümünü iki koşuyla günlüğe. Can/Civan onayı.
Birleşti 17:24 (BUILD, Volkan'ın sohbetteki onayıyla "incelediysen birleştir"): #8 (Can onaylı) → #12 (Can + Civan onaylı; taban main'e çevrildi) → #10 → #11 (BUILD gözden geçirdi: yalnız yeni dosya). #13 (Faz 3) main'e çevrildi, Can'ın incelemesini bekliyor. Main'de deneme: üretici birebir aynı şehir, model çalışıyor, `sinav.py faz1` 5/5.
Durum: yapıldı 17:03 (BUILD) — PR #12 (sözleşme 1.2 + üretici 1.2 + model), PR #8'in üstünde; Can/Civan onayı bekliyor. Sütunlu/sütunsuz ölçüm: docs/log/2026-10-31-volkan-uretici-1-2.md (PR #12). Sınav şehirleri 11–20: faturalı %3,9 / P90 %8,3, faturasız %22 / %55.

## UYARI! 31 Eki 14:06 — Civan'dan — gerçek şehirlerde trafolar denize düşüyor (otellerin %31'i)
Ne: `src/sehir_uret.py` `konum()` yalnız "y ≤ 400 m" ile kıyıyı düz sayıyor; Girne kıyısı limanın doğusunda güneye kıvrılıyor. OSM kıyı çizgisiyle ölçtüm [Hesap]: tip başına 2.000 örnekte otel %31 denizde (kutu −4000…4000 × 0…400), köy ve sulama %4, yurt %3, şehir konutu %2, çarşı ve sanayi %0; sehir-001'de 4/40 (T07, T13, T32 otel; T26 şehir konutu). Haritada jüri bunları denizde görür. Öneri: kıyı dosyası varsa `konum()` döngüsüne "karada mı" koşulu (kuzeye ışın, kıyıyı tek sayıda kesiyorsa kara; 10 satır, `app/ornek_veri.py` `kiyi_segmentleri()` + `karada()` ile aynı), yoksa bugünkü 400 m kuralı + uyarı (ışınım dosyasındaki gibi). Kıyı dosyası: `data/raw/osm-kasaba/girne_kiyi.json`, indirme komutu KAYNAK.txt'de. Sahte şehirlerde uyguladım (`harita/iskelet-2` 9703aa1, 120 trafoda denizde 0).
Dosya: src/sehir_uret.py (konum), ayar.json'a istersen kiyi_kontrolu
Neden: harita gerçek şehri gösterecek; denizdeki trafo sunumda ilk göze batan hata olur. Bloklamıyor.
Durum: karar verildi 15:12 → civan.md (uygulama BUILD, üretici 1.2)

## UYARI! 31 Eki 14:06 — Civan'dan — sözleşme 1.2: gerçek veri şehir no 800–899 haritada nasıl etiketlensin?
Ne: KARAR 13:58'de sözleşme 1.2'ye "gerçek veri `sehir` 800–899" geliyor. Harita bugün kartın kuralıyla `sehir` ≥ 900 → "SAHTE VERİ — gösterim", diğer her şey → "örnek veri (farazi şehir) — gösterim" yazıyor; 800–899 da "farazi şehir" diye etiketlenir, yanlış olur. Önerim: 800–899 → "gerçek ölçüm verisi (<kaynak>, Kıbrıs değil)". Kaynak adı haritaya nereden gelsin: `ayar.json`'da bir anahtar mı (ör. `veri_kaynagi`)? Ayrıca 1.2'deki `yillik_tuketim_mwh` sütununu sahte üreticiye eklerim; sözleşme PR'ı açılınca Civan onayı için bakarım.
Dosya: docs/data/tablo-bicimi.md (Genel kurallar, şehir no aralıkları), app/harita.py
Neden: etiket kuralı kartta (Harita kuralları 1); şehir aralığı sözleşmede. Bloklamıyor.
Durum: karar verildi 15:12 → civan.md

## KARAR 31 Eki 15:12 — BUILD'e: ADR-0008 (mahalle çarpanı, saf tahmin), PR #10 soruları, üretici 1.2 paketi
Karar: [ADR-0008](../decisions/adr-0008-farazi-cesitlilik-saf-tahmin.md) kabul: farazi şehirler fazla düzenli (konut trafolarında müşteri başına öğlen yükü CV 0,08–0,14; gerçekte 0,46), Faz 2 sınavı saf tahminle geçiliyor. PR #10 günlüğündeki soru: ışınım yılına **2023 eklenir** (Open-Meteo'dan indir; tüketim ve abone sayısı 2023), hava yılı 2023/2024/2025'ten rastgele (ADR-0003 korunur). Sunum rakamı olarak gerçek veri cümlesi ADR-0008 madde 3.
Senden beklenen (ana oturum), tek paket = üretici sürüm 1.2 + sözleşme 1.2 (Can/Civan onayı), sonra 20 şehir yeniden: (a) trafo başına mahalle çarpanı log-normal σ ≈ 0,3 + trafo başına saat kayması ±30 dk, `ayar.json` `mahalle_sigma`; (b) `yillik_tuketim_mwh` (ADR-0007); (c) KKTC bayramları `gun_turu = tatil` (2024: 10–12 Nisan, 23 Nisan; 2025: 1 Nisan, 23 Nisan; tarihleri doğrula); (d) kıyı kontrolü: Civan'ın `kiyi_segmentleri`/`karada` fonksiyonları `konum()`'a, atıfla; kıyı dosyası KAYNAK.txt komutuyla; (e) `kva_tavan_sayisi` `ayar.json`'a; (f) ışınım 2023 dosyası + rastgele yıl; (g) sözleşme 1.2: `yillik_tuketim_mwh`, "800–899 gerçek veri, `veri_kaynagi`/`veri_turu` zorunlu", `mahalle_sigma` ve `kiyi_kontrolu` bilgi anahtarları. Sonra `sablon.py` sütun varsa kullanır; Faz 2 sütunlu/sütunsuz + saf tahmin satırı yan yana günlüğe; ROADMAP Faz 5 dürüstlük cümlelerine ADR-0008 madde 3. PR #8 önce birleşsin (Can onayı bekleniyor), 1.2 onun üstüne.
Durum: yapıldı 17:03 (BUILD) — (a)–(g) PR #12'de; σ 0,35 (0,30'da konut CV şehir içi 0,29 çıktı, 0,35'te 0,33); bayram tarihleri doğrulandı (2023: 21–23 Nisan da eklendi); ROADMAP Faz 5'e ADR-0008 madde 3 main'de (7af5272). Yolda iki üretici kararı günlükte: kVA mahalle farkını görmez (sızıntı), aşırı yüklenen trafo bir üst boy.

## KARAR 15:29 — BUILD'e: UKPN raporundan üç çapa (indirme yok, atıf var)
Karar: UKPN kapanış raporunun (Mart 2015) üç rakamı günlüğe ve sunuma girer, veri indirilmez (can.md'deki bilgi girdisinde ayrıntı): (1) trafo bara gerilimi tasarım varsayımı 248 V, 251 V risksiz, yasal 253 V → bizim 246–250 V / 259 V kurgusuyla aynı mantık; "hat ucu gerilimi asıl bara gerilimine bağlı" bulgusu ADR-0002'ye gerçek veri desteği; (2) gündüz en düşük talep 200–400 W/müşteri (Low Carbon London) → bizim şehir konutu 330 W/abone aralıkta [Hesap]; (3) tek fazlı PV faz dengesizliği kentsel %25, kırsal %50 → üretici 1.2'de faz dağılımı rastgeleliği bu aralığa çapalanır (şu an [Yorum]).
Senden beklenen (ana oturum): Faz 1 günlüğüne "dış çapa" paragrafı (üç rakam, atıfla), ROADMAP Faz 5 kaynak slaydına UKPN raporu; üretici 1.2'de faz ağırlıkları: kentsel ±%25, kırsal ±%50 [Kaynaklı: UKPN 2015].
Durum: yapıldı 17:03 (BUILD) — dış çapa Faz 1 günlüğünde, UKPN raporu ROADMAP Faz 5 kaynak slaydında (7af5272); faz ağırlıkları kentsel ±%25 / kırsal ±%50 PR #12'de.

## UYARI! 16:25 — UKPN oturumundan — gerilim doğrulaması bitti
Ne: Gerçek veri (İngiltere UKPN, yaz 2014, 1 dk), 6 hat ucu ev. (1) `solve()` öğlen PV yükselmesini, akşam düşümünden kestirilen hat boyuyla, 4 sitede ölçülenin 0,84–1,39 katı veriyor (hedef 0,7–1,5; ortanca 0,87) [Hesap]; fizik doğru büyüklükte. 2 sitede 0,22 ve 0,52: paneller evin kolunda, hattın ucunda toplanınca eşit yayılmış model yükselmeyi az gösteriyor → **yanlış yeşil yönü**; UKPN'in kendi modeli de Alverston'u 0,43 kat gösterdi [Kaynaklı: rapor s.30]. (2) Faz bilgisi olmadan oran 0,45–1,94'e yayılıyor [Hesap]. (3) Bara gerilimi 20 trafoda gece ortanca 245,0 V, +1 ss 248,2 V (raporun 245 / 248'i); siteler arası 12 V fark, bizim 246–250 V bandından ~3 kat geniş [Hesap]. Çapraz: gündüz en düşük talep 205–355 W/müşteri (330 aralıkta); kent faz dengesizliği %14, bizim üretici %29 (karamsar, güvenli yön). Önerilerim [Yorum]: `kac_ev.py` karamsar durumu bekleyen panelleri hat ucuna ve evin fazına koysun (ADR-0002 içinde); trafo çıkışı bandı genişlesin mi, karar sizin. Hat boyu BULAMADIM (iki sitede kablo da).
Dosya: docs/log/2026-10-31-volkan-ukpn-gerilim.md, src/ukpn_test.py — PR #11 (https://github.com/volkanGRGN/KKTC-hackathon/pull/11), birleştirilmedi
Neden: brif-ukpn-gerilim.md'nin istediği bitiş bildirimi; bloklamıyor.
Durum: karar verildi 16:27 → volkan.md (KARAR aşağıda); Volkan'a iletildi

## KARAR 16:27 — BUILD'e: UKPN gerilim doğrulamasının sonuçları (PR #11) Faz 3'e nasıl girer
Karar: (1) **Fizik değişmez**: `solve()` İngiltere'de 6 hat ucu evin 4'ünde ölçülen yükselmenin 0,84–1,39 katını verdi (ortanca 0,87) [Hesap, PR #11 günlüğü]; ADR-0002'nin fiziği gerçek veride ilk kez tutuyor. (2) **Faz 3 karamsar senaryo hat ucu + evin fazı**: `kac_ev.py` karamsar durumda bekleyen panelleri hattın **ucuna** (etkin mesafe = hat boyu, yarısı değil) ve tek faza koyar; iyimser durum eşit yayılmış + dengeli üç faz kalır. Gerekçe: paneller uca toplanınca eşit yayılmış model yükselmeyi 2–4 kat az gösteriyor (UKPN 2 sitede 0,22 / 0,52; UKPN'in kendi modeli 0,43) → yanlış yeşil yönü. ADR-0002'nin "tek faz karamsar / dengeli iyimser" kuralının içinde; yeni ADR yok, `docs/method/modeling.md` §4'teki "etkin mesafe hat boyunun yarısı" satırı "karamsar: hat boyu, iyimser: yarısı" olur. (3) **Trafo çıkış gerilimi bandı 246–250 → 244–252 V** (üretici 1.2): İngiltere'de siteler arası bara gerilimi yayılımı ss 3,3 V, bizimki 1,2 V; Kıbrıs dağılımı BULAMADIM, UKPN tasarım varsayımı 248 V bizim merkezimizle aynı; bant ±4 V [Yorum, ss 2,3 V, ikisinin arası]. Pilotun ilk ölçeceği şey bara gerilimi dağılımı: validation.md "gerçek veri" bölümüne satır. (4) Faz dengesizliği çapası doğrulandı: kentsel ortanca %14, P84 %30; bizim üretici %29 ortanca (karamsar). 1.2'de kentsel ±%25 / kırsal ±%50 kalır; üretici dengesizliği raporlasın (`ayar.json` `faz_dengesizlik_ortanca`). (5) PR #11 birleşsin (karar masası baktı; kod kurallara uygun, veri depoya girmiyor).
Senden beklenen (ana oturum): Faz 3 kartı ve `src/kac_ev.py`'de (2); üretici 1.2'de (3) ve (4); `modeling.md` §4 ve `validation.md` satırları; Faz 5 dürüstlük cümlesine: "Gerilim fiziğini İngiltere'de 6 gerçek hatta sınadık: dördünde ±%40 içinde, ikisinde paneller hat ucunda toplandığı için model yükselmeyi az gösterdi; bu yüzden karamsar senaryomuz panelleri hattın ucuna koyar." PR #11'i birleştir (ben deniyorum; olmazsa sen).
İlerleme 17:03 (BUILD): (3) trafo çıkışı 244–252 V ve (4) `faz_dengesizlik_ortanca` PR #12'de (c934d48; 20 şehir ortancası %20,7). (2) `kac_ev.py` ile şimdi; `modeling.md` §4, `validation.md`, Faz 5 cümlesi bu akşam. (5) PR #11: BUILD'in birleştirme izni yok (aşağıda UYARI).
Birleşti 17:24 (BUILD, Volkan'ın sohbetteki onayıyla "incelediysen birleştir"): #8 (Can onaylı) → #12 (Can + Civan onaylı; taban main'e çevrildi) → #10 → #11 (BUILD gözden geçirdi: yalnız yeni dosya). #13 (Faz 3) main'e çevrildi, Can'ın incelemesini bekliyor. Main'de deneme: üretici birebir aynı şehir, model çalışıyor, `sinav.py faz1` 5/5.
Durum: yapıldı 17:17 (BUILD) — (2) `kac_ev.py` karamsar = hat ucu + tek faz, PR #13; (3) 244–252 V ve (4) `faz_dengesizlik_ortanca` PR #12; `modeling.md` §4 PR #13; `validation.md` satırları ve Faz 5 gerilim cümlesi main'de (655dc8e). (5) PR #11'i birleştirmek Volkan'da (BUILD'in izni yok).

## KARAR 16:50 — BUILD'e: yeniden planlama (Volkan: "PR'ı birleştir, fazları buna göre düzenle, Can ve Civan'ın yükünü yeniden dağıt")
Karar: Sunum yarın, saat bilinmiyor; bu akşam üç şey paralel gider: Faz 2 kapanışı, Faz 3 çekirdeği, Faz 5 başlangıcı. Zaman kutuları kesin.
1. **Birleştirmeler (şimdi):** PR #10 ve #11 sen birleştir (karar masası ikisine baktı, kurallara uygun; izin sistemi bana birleştirme vermiyor). PR #9'u Civan birleştirir. PR #8: Can onayı 17:30'a kadar gelmezse Volkan'a sor, o karar verir.
2. **Faz 2 kapanışı (zaman kutusu 19:00):** üretici 1.2 paketi (volkan.md 15:12 + 15:29 + 16:27 KARAR'ları: mahalle çarpanı, fatura, bayram, kıyı, LF, 2023 ışınım, bara 244–252 V, faz ±%25/±%50) → 20 şehir → Can `sinav.py faz2` (saf tahmin satırıyla) → ROADMAP Faz 2 kutuları rakamla. 19:00'da bitmezse mevcut şehirler ve mevcut ölçümle Faz 2 "gösterim" notuyla kapanır, 1.2 sunum sonrasına kalır.
3. **Faz 3 çekirdeği (şimdi, BUILD, 2 saat):** `src/kac_ev.py`: ısıl pay + gerilim payı, karamsar = P10 yük + bekleyen paneller hat ucunda + tek faz + 250 V (UKPN kararı 16:27), iyimser = P90 + yarı boy + dengeli + 246 V; küçüğü ÷ 6,5 kW; renk kuralı (modeling.md §5); `kural40_ev`; sözleşme §6 `kac_ev.csv`. Faz 3 kartları: Can → `sinav.py faz3` (yanlış yeşil, yanlış kırmızı, kaç ev hatası, sarı oranı; %40 kuralı aynı ölçülerle yan yana) + `grafikler.py` kilit grafik (biz vs %40 kuralı, yanlış yeşil); Civan → yan panel gerçek `kac_ev.csv`'ye, "ölçülmedi" etiketi, 800–899 etiketi, internetsiz deneme + 2 dk ekran kaydı, 3 şehir seçimi (Faz 4 sınavı).
4. **Faz 5 başlangıcı (şimdi, paralel):** Can `docs/sunum/` açar: slayt listesi (ROADMAP Faz 5 akışı), kaynak slaydı (her rakam etiketli), dürüstlük cümleleri (farazi üst sınır; İspanya %25 → %10; İngiltere 6 hatta 4'ü ±%40, 2'sinde hat ucu → karamsar; Kıbrıs pilot), itiraz slaydı (ADR-0005). BUILD konuşma notu taslağı; hikâye Volkan'ın. Gece 2 prova.
5. ROADMAP: Faz 2 başlığına durum, Faz 3 ve Faz 5 "başladı 31 Ekim akşam"; kartları docs/gorev'e; DEVIR tazele. Can ve Civan'ın kutularına iş sırasını ben yazdım (can.md / civan.md 16:50); kartlar gelince onlar kartı esas alır.
Senden beklenen (ana oturum): yukarıdakiler; bitirdiğin kalemi bu girdinin altına "yapıldı <saat>" satırıyla işle.
İlerleme 17:03 (BUILD): (2) üretici 1.2 paketi bitti, PR #12 (zaman kutusu 19:00 içinde); 20 şehir yeniden üretildi, `sinav.py faz1` (207 V) 5/5 geçti. (1) birleştirmeler: izin yok (aşağıda UYARI). (3) `kac_ev.py` şimdi başlıyor.
İlerleme 17:17 (BUILD): (1) Volkan kararı 17:06: #8 ve #12 Can'ı bekler. (2) Faz 2: PR #12 hazır, Can'ın `sinav.py faz2` ölçümü bekleniyor. (3) Faz 3 çekirdeği: `kac_ev.py` PR #13 (sınav 11–20: yanlış yeşil 0/21, %40 kuralı 41/284); Can ve Civan Faz 3 kartları main'de (docs/gorev/can-faz3-sinav-grafik.md, civan-faz3-yan-panel.md). (5) ROADMAP Faz 2/3/5 güncel (655dc8e); DEVIR sırada. (4) konuşma notu taslağı sırada.
Birleşti 17:24 (BUILD, Volkan'ın sohbetteki onayıyla "incelediysen birleştir"): #8 (Can onaylı) → #12 (Can + Civan onaylı; taban main'e çevrildi) → #10 → #11 (BUILD gözden geçirdi: yalnız yeni dosya). #13 (Faz 3) main'e çevrildi, Can'ın incelemesini bekliyor. Main'de deneme: üretici birebir aynı şehir, model çalışıyor, `sinav.py faz1` 5/5.
Durum: yapıldı 17:17 (BUILD) — (2) PR #12, (3) PR #13 + Faz 3 kartları, (4) konuşma notu taslağı docs/konusma-notu-taslak.md (Can `docs/sunum/`'a taşır), (5) ROADMAP ve DEVIR main'de. (1) birleştirmeler Volkan kararıyla Can'ı bekliyor (17:06).

## KARAR 17:00 — BUILD'e: Muhittin'in cevabı → sunum hikâyesi, Faz 3 yeşil kuralı, bugün / sonra ayrımı
Karar: Muhittin'in ikinci cevabı günlükte (docs/log/2026-10-31-muhittin-cevap-2-hata-payi-mimari.md); [ADR-0009](../decisions/adr-0009-dogruluk-onceligi-ve-capalama.md) ve [ADR-0010](../decisions/adr-0010-yesil-karari-marj-guven-kumulatif.md) kabul.
**Bugün (sunum öncesi):**
1. Faz 5 hikâyesi "güven merdiveni": tek cümle "Kıbrıs'ı ölçemiyoruz; yöntemi ölçebildiğimiz her şeyde kanıtlıyoruz, sonra uyguluyoruz." Dört basamak, her birine tek iddia + tek rakam, hepsi "saf tahmine göre ne kadar iyi" cinsinden: farazi şehir (kontrollü gerçek), İspanya (yük, dış geçerlilik), İngiltere (gerilim, dış geçerlilik), Kıbrıs pilotu (saha). **Manşet rakam: İspanya %25 → %10** ("hiç görmediğimiz 29 gerçek trafoda, Kıb-Tek'in zaten elinde olan abone sayısı + faturayla"). İkinci vurgu: gerilimde 6 hattın 4'ü ±%40, 2 ıskalama uca kümelenme → karamsar senaryo. Farazi %8,6 destek rakamı, manşet değil. ROADMAP Faz 5 akışı ve dürüstlük cümleleri buna göre; Can'ın sunum iskeletine aktar.
2. `kac_ev.py` renk kuralı ADR-0010: yeşil = karamsar sınırı marjla geçiyor (gerilim payının %10'u ya da ≥ 1 ev) VE güven yüksek; sarı = sınırda ya da güven orta/düşük; kırmızı = karamsar aşıyor. `modeling.md` §5 güncelle. Can'ın Faz 3 sınavına "yanlış yeşil" zaten var; "canlı bütçe < %2" notu validation.md'ye.
3. Fatura: sözleşme 1.2'deki `yillik_tuketim_mwh` kalır; dağılım sütunları (yüksek tüketen abone oranı) 1.3'e not.
**Sonra (sunum sonrası / pilot öncesi), ROADMAP'e "Faz 3 ikinci sürüm" olarak:** kümülatif düşüm (`onaylanan_kw`, `kalan_ev`), yeşil kuralının İspanya/İngiltere geri-testi ve bütçe eşikleri, çapalamaya korelasyon matrisi + P90/P95 + PV konum dağılımı + trafo içi çeşitlilik (Can'ın `edp_kiyas.py`; üretici 1.3), "farazi − İspanya" fark ölçeri her sürümde.
Senden beklenen (ana oturum): 1–3 bugün, "sonra" listesi ROADMAP'e; bitince bu girdiye "yapıldı <saat>".
İlerleme 17:17 (BUILD): (1) ROADMAP Faz 5 güven merdiveni, manşet ve dürüstlük cümleleri main'de (655dc8e); Can'a aktarım can.md'de. (2) ADR-0010 rengi `kac_ev.py`'de (PR #13), `modeling.md` §5 PR #13'te, canlı bütçe < %2 `validation.md`'de; kırmızı kuralının okuması aşağıdaki UYARI'da. (3) fatura dağılım sütunları 1.3 notu ROADMAP'e. "Sonra" listesi ROADMAP Faz 3 ikinci sürümde.
Durum: yapıldı 17:17 (BUILD) — 1: ROADMAP Faz 5 + konuşma notu taslağı + can.md; 2: `kac_ev.py` ADR-0010 (PR #13), kırmızı okuması 17:17 UYARI'da; 3: 1.3 notu ROADMAP'te; "sonra" listesi ROADMAP Faz 3 ikinci sürüm.

## UYARI! 31 Eki 17:03 — BUILD'den — BLOKLUYOR: BUILD PR birleştiremiyor (#10, #11, #8, #12)
Ne: `gh pr merge 10` izin sisteminde "gözden geçirmesiz birleştirme" diye reddedildi; karar masası da birleştiremiyor. Birleştirme Volkan'da (GitHub'da düğme ya da Claude Code ayarında izin kuralı). Sıra: #10 (EDP, yalnız yeni dosya) ve #11 (UKPN, yalnız yeni dosya; karar masası baktı) bağımsız. #8 Can onayı ya da 17:30'dan sonra Volkan kararı. #12 #8'in üstünde: sözleşme 1.2, Can ya da Civan onayı; #8 birleşince tabanı main'e döner.
Dosya: https://github.com/volkanGRGN/KKTC-hackathon/pulls
Neden: Can ve Civan main'den çalışıyor; yeni şehirler (1.2) ve model #8 + #12 birleşmeden main'de yok. Faz 3 `kac_ev.py` bunlara dayanıyor, ama dalda ilerliyor; bloklanan, ekibin main'deki işi.
Durum: yapıldı 17:24 — Birleşti 17:24 (BUILD, Volkan'ın sohbetteki onayıyla "incelediysen birleştir"): #8 (Can onaylı) → #12 (Can + Civan onaylı; taban main'e çevrildi) → #10 → #11 (BUILD gözden geçirdi: yalnız yeni dosya). #13 (Faz 3) main'e çevrildi, Can'ın incelemesini bekliyor. Main'de deneme: üretici birebir aynı şehir, model çalışıyor, `sinav.py faz1` 5/5.

## UYARI! 31 Eki 17:03 — BUILD'den — Faz 2 (1.2) sonuçları ve üç soru
Ne: Sınav şehirleri 11–20 (bir kez, gösterim): faturalı model %3,9 / P90 %8,3, kapsama %85, düşük güven %1; faturasız %22 / %55 (İspanya gerçek verisiyle aynı seviye: ADR-0008'in beklentisi tuttu). Saf tahminler: ADR tanımı (Σ abone) %176 / %726, tarife enerjisiyle %23 / %82, faturayla %5,8 / %16. Sorular: (1) **Saf tahmin tanımı**: Σ abone karışık şehirde anlamsız (otel = 1 abone); öneri: faturasızda "Σ öğlen ÷ Σ tarife enerjisi × enerji", faturalıda "Σ öğlen ÷ Σ fatura × fatura". Bu tanımla faturalı model geçiyor (ortanca %33, P90 %48 düşük), faturasız ortancada geçmiyor (%3; P90'da %33). (2) **Panelli evin faturası**: üretici brüt tüketim yazıyor (ADR-0007); mahsuplaşmada fatura net olabilir, Kıb-Tek'in içeri alınan enerjiyi ayrı bilip bilmediği BULAMADIM; net ise panelli trafolarda fatura düşük kalır. (3) **Farazi faturalı isabet iyimser** (%3,9; İspanya faturayla %10–11): aynı tarifedeki her abone aynı EAC eğrisini taşıyor. Abone başına eğri farkı üretici 1.3'e (ADR-0009 "trafo içi çeşitlilik" ile aynı iş).
Dosya: docs/log/2026-10-31-volkan-uretici-1-2.md (PR #12)
Neden: ADR-0008 madde 1 ölçütü Can'ın `sinav.py faz2`'sinde; tanım ona gidiyor. Bloklamıyor.
Durum: karar verildi 17:26 → volkan.md (KARAR aşağıda) + can.md (saf tahmin tanımı)

## UYARI! 31 Eki 17:11 — Civan'dan — sunum dashboard'un içinde olsun mu?
Ne: Öneri: sunum ayrı slayt yerine harita uygulamasının içinde 7 kısa ekran
olsun; her ekranda tek cümle, tek görsel, en fazla bir rakam. Sıfırdan
gelen biri hiçbir terimi bilmeden anlayabilsin:
(0) Açılış sorusu: "Bu sokakta kaç ev daha çatısına güneş paneli takabilir?
    Kıb-Tek bilmiyor."
(1) Kıb-Tek kim: "Kuzey Kıbrıs'ta elektriği üreten ve evlere dağıtan
    devlet kurumu."
(2) Mahalle şebekesi ne, neden önemli: "Her mahallenin köşesinde, direğin
    üstünde gri bir kutu (trafo) ve ondan evlere giden kablolar var; elektriğin
    evden önceki son durağı. Panel, klima, elektrikli araç: hepsi önce bu
    kutuyu zorlar. Kıb-Tek büyük hatları izliyor, bu kutuları izlemiyor; dolu
    mu boş mu bilmiyor. Bu yüzden temkinli davranıyor: 2.670 ev bekliyor."
    Görsel: 3D direk, kutu ve evler.
(3) Fikrimiz: "Her kutuya cihaz takmak çok pahalı. Birkaçını ölçüyoruz,
    gerisini tahmin ediyoruz." Görsel: kısa animasyon (Blender, sahte veriyle).
(4) Neden inanılır: güven merdiveni, dört basamak; manşet İspanya %25 → %10
    (17:00 kararı).
(5) Canlı harita: bir kutuya tıkla, kaç ev daha sığar, %40 kuralı ne diyor.
(6) Pilot: Kıbrıs'ta ne kadar ölçüm, ne kadar maliyet, ne istiyoruz.
Metin Can'ın sunum iskeletiyle ve 17:00 kararıyla uyumlu tutulur; rakamlar
repodaki kaynaklardan (2.670: KTTO 2023). PDF yedeği yine olur.
Dosya: app/ (Civan, ekranlar), docs/sunum/ (Can, metin)
Neden: tek ekran, slayttan haritaya geçiş yok; rakamlar veriden gelir;
teknik terimler (arketip, kVA, P10) sunum dilinde yok.
Karar gereken: (a) sunum dashboard'da mı, slaytta mı;
(b) animasyona zaman ayrılsın mı (iş sırası 4–5 öncelikli kalır).
Durum: karar verildi 17:32 (Volkan) → civan.md + can.md: dashboard içinde ekranlar, geçiş animasyonu Volkan'ın "noktalar çoğalıyor" fikri, Blender yok

## UYARI! 31 Eki 17:17 — BUILD'den — Faz 3: ADR-0010'daki "kırmızı = karamsar sınırı aşıyor" hangi okuma?
Ne: `kac_ev.py` (PR #13) yeşil kuralı tuttu: sınav şehirleri 11–20'de yanlış yeşil 0/21 (%40 kuralı 41/284 = %14; dolu 74 trafonun 41'ine "yer var"). Kırmızı için metin üç türlü okunuyor, sınav 11–20 (347 trafo, 74 dolu): (a) **karamsar_yeni_ev** (bekleyen ev hattın ucunda sığmıyor; düz okuma, şu an varsayılan): kırmızı %68, yanlış kırmızı %69, dolu yakalanan 74/74, sarı %26; (b) **karamsar_bugun** (karamsar senaryoda yeni panelsiz bugün aşıyor): kırmızı %31, yanlış kırmızı %42, dolu yakalanan 61/74, sarı %63; (c) **beklenen_bugun** (her belirsizliğin ortasında bugün aşıyor): kırmızı %3, yanlış kırmızı %17, dolu yakalanan 10/74, sarı %90. Yeşil üçünde aynı. Sebep: dolu trafoların hemen hepsi bugün zaten 259 V üstünde ve bunu en çok ±4 V bilinmeyen bara gerilimi belirliyor; hiçbir eşik ikisini birden iyi yapmıyor. Önerim (b): kırmızı = "karamsar senaryoda bugün bile sınırda; önce ölç ya da güçlendir"; dolu trafoların %82'si kırmızı, sarı %63. (a) haritayı jüriye "her konut ve köy trafosu kırmızı" gösterir (kırmızıların üçte ikisinde yer var). Kod tek satır (`KIRMIZI_KURALI`).
Dosya: src/kac_ev.py, docs/log/2026-10-31-volkan-faz3.md (PR #13)
Neden: ADR-0010 karar masasının; okumayı ben seçmedim, düz okumayla bıraktım (CLAUDE.md: ADR'ye ters düşecek işi önce sor). Bloklamıyor: Can ve Civan kurala bağlı değil, yalnız `kac_ev.csv` değişir.
Durum: karar verildi 17:26 → volkan.md (KARAR aşağıda): (b) karamsar_bugun

## KARAR 17:26 — BUILD'e: Faz 3 kırmızı kuralı (b) karamsar_bugun; ADR-0010 okuması
Karar: `KIRMIZI_KURALI = 'karamsar_bugun'`: kırmızı = karamsar senaryoda (bara 252 V, tek faz, P10 yük) **bugün, yeni panel olmadan** sınır aşılıyor ya da ısıl pay eksi → "önce ölç ya da güçlendir". Karamsar senaryoda bugün aşmıyor ama bekleyen ev sığmıyorsa **sarı** (sınırda → ölç ya da sınırlı onay). Yeşil kuralı değişmez (yanlış yeşil 0/21 iyi).
Neden: Muhittin'in kademesi tam bu: kırmızı = karamsar aşıyor, sarı = sınırda; (a) düz okuma "yer olmayan" ile "sınırda" olanı aynı renge koyuyor, kırmızıların üçte ikisinde yer var, harita jüriye her konut trafosunu kırmızı gösterir; (c) dolu trafoların %86'sını kaçırıyor, yanlış yeşile komşu. (b) dolu 74 trafonun 61'ini yakalıyor, kaçan 13'ü sarıya düşüyor (sarı = ölç, onay değil; zarar yok). Yanlış kırmızı %42 ve sarı %63 ROADMAP hedeflerinin (≤ %20, ≤ %30) üstünde: sebep ±4 V bilinmeyen bara gerilimi (244–252), hiçbir eşik ikisini birden tutturamıyor; bu **pilotun ilk ölçeceği şey** ve sunumda "ölçüm cihazı sarılara" cümlesinin dayanağı. Günlüğe üç okumanın tablosu aynen, hedef aşımının sebebi [Yorum] olarak.
Senden beklenen (ana oturum): tek satır değişiklik + `kac_ev.csv` yeniden + Faz 3 günlüğüne tablo ve sebep; `modeling.md` §5'e "kırmızı = karamsar senaryoda bugün aşıyor; sarı = sınırda ya da güven düşük" cümlesi (ADR-0010 dosyası düzenlenmez). ROADMAP Faz 3 kutuları Can'ın `sinav.py faz3`'üyle; yanlış kırmızı ve sarı maddeleri "KALDI, sebep günlükte" olarak dürüstçe.
Durum: yapıldı 17:30 (BUILD) — `KIRMIZI_KURALI = 'karamsar_bugun'`, `kac_ev.csv` yeniden (sınav 11–20: kırmızı %31, yanlış kırmızı %42, dolu 61/74 kırmızı, 13'ü sarı; yanlış yeşil 0/21), Faz 3 günlüğüne tablo + sebep, `modeling.md` §5 cümlesi: PR #13 (2a9ea6e). ROADMAP Faz 3 kutuları Can'ın `sinav.py faz3`'üyle.

## KARAR 17:26 — BUILD'e: Faz 2 (1.2) üç soru — saf tahmin tanımı, panelli evin faturası, iyimserlik
Karar: (1) **Saf tahmin tanımı** BUILD'in önerisi: model hangi bilgiyle çalışıyorsa saf tahmin de onunla: faturasız koşuda "Σ öğlen ÷ Σ tarife enerjisi × trafonun tarife enerjisi" (Kıb-Tek sınıf sayılarını bildiği için tarife ortalaması saf tahminin hakkı), faturalı koşuda "Σ öğlen ÷ Σ fatura × fatura". ADR-0008 madde 1'in "Σ abone" tanımı bu ikisiyle değişir (ADR dosyası düzenlenmez; bu KARAR ve Can'ın sınavı kaynak). Sonuç dürüstçe söylenir: faturalı model saf tahminden ortanca %33, P90 %48 iyi → geçer; faturasız model ortancada yalnız %3 iyi → **ortancada geçmez**, kazancı kötü uçta (P90 %33) ve gerilim katmanında; sunumda "fatura olmadan ortalama trafoda basit hesaptan pek iyi değiliz" cümlesi güven merdiveninin birinci basamağıdır. (2) **Panelli evin faturası**: mahsuplaşmada fatura net (çekilen − verilen); evin kendi tükettiği panel üretimi sayaçtan hiç geçmez, yani brüt tüketim Kıb-Tek için de bilinemez [Yorum]. Sürüm 1.2 brüt kalır, günlüğe "panelli trafolarda iyimser" notu; **1.3'te** `yillik_tuketim_mwh` panelli evde net yazılır, model `panel_kw` × yıllık üretimle (≈ 1.600 kWh/kWp [Yorum]) düzeltir. Uzmana soru 7 (01-plan): "Kıb-Tek mahsuplaşma sayaçlarında çekilen ve verilen enerji ayrı kayıtlı mı?" (3) **İyimserlik**: evet, abone başına eğri farkı (öğlen ÷ yıllık oranı abone bazında dağılsın) üretici 1.3'e, ADR-0009 "trafo içi çeşitlilik" kalemiyle birlikte; bugün yalnız günlükte "farazi faturalı %3,9 üst sınır, gerçek %10" cümlesi.
Senden beklenen (ana oturum): (1) Can'a tanımı ben yazdım (can.md); sen `sablon_ozet.json`'a iki saf tahmini de yaz. (2) 01-plan uzman soruları 7; günlük notu. (3) ROADMAP "üretici 1.3" listesine. 
Durum: yapıldı 17:30 (BUILD) — (1) `sablon_ozet.json`'a `saf_tahmin` (tarife / fatura: oran + bir-dışarıda hata); (2) 01-plan uzman sorusu 7, 1.2 günlüğüne iyimser notu; (3) ROADMAP "Üretici 1.3" kalemleri. Ayrıca `requirements.txt`'e `python-calamine` (Can'ın notu).

## UYARI! 31 Eki 15:25 — Can'dan — Faz 2 sınavı resmi sonuç (PR #14) + edp_kiyas + sunum iskeleti
Ne: (1) **PR #14** `sinav.py faz2` + `grafikler.py` (dal `sinav/faz2`; yeni modül → Volkan bakar, Can birleştirir). PR #12 dalının 1.2 üreticisi + `sablon.py` ile 20 şehir, Windows. Sınav şehirleri 11–20, 7/7 GEÇTİ:
- doğru arketip %98,2
- hata %3,8 / P90 %8,0
- kapsama %83,9
- şehirler arası 1,08 (en kötü 1,81)
- düşük güven %0
- saf (Σ abone) %172 / %672

Bilgi satırları:
- Saf tahmin tarife enerjisiyle %25,2 / %67,2, faturayla %5,5 / %15,2. Model faturalı saftan %31 / %48 düşük; ≥ %25 ölçütü dar geçiyor.
- Güven etiketi hatayı ayırmıyor: yüksek %3,8, orta %5,1, düşük n = 3.
- Kalibrasyonda bant yukarı kayık: P10 altı ~%11, P90 üstü ~%4. Yanlış yeşil yönü.

Faz 1, 1.2'de 5/5; konut CV 0,32. Rakamların senin geliştirme ölçümünle tutuyor. (2) `src/edp_kiyas.py` main'de, gerçek İspanya ↔ farazi konut:
- CV 0,45 ↔ 0,32 (eski şehirler 0,09)
- saf tahmin %25,5 ↔ %25,4 (eski %6,6)
- eğri benzerliği 0,93 ↔ 0,99 (hâlâ tekdüze, 1.3 trafo içi çeşitlilik)

(3) `docs/sunum/` iskeleti main'de (güven merdiveni, itiraz ve kaynak slaydı, dürüstlük cümleleri, 8 jüri sorusu). Slayt 5'te farazi rakam için %8,6 (PR #8) mi, 1.2 %3,9 / %22 mi; senin 17:17 notuna göre 1.2'yi koyacağım. Slayt 1'deki KTTO Mart 2023 raporunun adresi BULAMADIM (araştırma günlüğünde yalnız ad).
(4) Not: `edp_kiyas.py` hızlı okuma için `python-calamine` kullanıyor (yoksa openpyxl'e düşüyor); senin `edp_test.py` de istiyor, `requirements.txt`'de yok (kök belge, senin).
Dosya: PR #14, src/edp_kiyas.py, docs/log/2026-10-31-can-faz2.md, docs/sunum/
Neden: karar masası 16:50 sırası (2), (3), (5); ADR-0008 madde 1, 2, 4; 17:03 UYARI.
Durum: karar verildi 17:38 → can.md (slayt 5 rakamı 1.2 + İspanya; KTTO adresi aranıyor) + volkan.md (BUILD: bant kayması, requirements)

## UYARI! 31 Eki 15:50 — Can'dan — Faz 3 sınavı resmi sonuç (PR #14'e eklendi) + kaç ev maddesi KALDI
Ne: `sinav.py faz3` ve kilit grafik PR #14'te (dal `sinav/faz2`, ikinci commit). Girdi: `kac-ev/ilk-surum` dalındaki `kac_ev.py`, Faz 2'deki 1.2 şehirleri, kırmızı kuralı varsayılan (`karamsar_yeni_ev`). Sınav şehirleri 11–20 senin ölçümünle birebir:

| Ölçü | Sonuç |
|---|---|
| Yanlış yeşil | 0/21 (her şehirde 0) → GEÇTİ |
| %40 kuralı | 41/284 (%14,4; en kötü şehir 6/23); dolu 74'ün 41'ine "yer var" |
| Yanlış kırmızı | %68,8 → UYARI |
| Sarı | %25,6 |

Kilit grafik: `docs/sunum/kilit_yanlis_yesil.png` (main). Slayt 5'e 1.2 rakamları (%3,9 / %22), slayt 10'a kilit grafik işlendi.
**Kaç ev maddesi KALDI.** Kart "`kac_ev_tavan` = 1 olanlar ayrı" diyor. Tavan = 0 trafolarda (n 240) ortanca hata: karamsar 9, iyimser 3,5, ortası 5,75 ev; hiçbiri ≤ 2 değil. Senin "iyimser 2" ölçümün tavan = 1 dahil (n 347). Tavanlı trafoda gerçek sayı alttan kesik, iyimser de genelde aynı tavana dayanınca hata yapay küçük çıkıyor. Bilgi satırında ikisi de yazıyor; eşiği ve tanımı oynatmadım.
Soru: madde tanımı hangisi olsun (kart: ayrı → KALDI; dahil → iyimser 2, geçer)? Kırmızı kuralı kararı gelince `faz3` yeniden koşulur.
Dosya: PR #14 (src/sinav.py, src/grafikler.py), docs/log/2026-10-31-can-faz3.md, docs/sunum/
Neden: karar masası 16:50 (4), 17:17 UYARI; kart "karar masasına yaz: eşik tartışmalıysa".
BUILD görüşü 17:33: Can haklı; kartı ben yazdım, tanım kartınki kalsın (tavanlılar ayrı) → madde KALDI. Benim "iyimser 2 ev" ölçümüm tavanlıları dahil ettiği için yapay küçüktü; Faz 3 günlüğüne düzeltme yazıldı (PR #13, a534b67). Kırmızı kuralı (b) PR #13'te; `faz3` yeniden koşulmalı (kırmızı %31, yanlış kırmızı %42, sarı %63 bekleniyor). PR #14 birleşti 17:32.
Durum: karar verildi 17:38 → can.md: kart tanımı kalır (tavanlılar ayrı), madde KALDI; aralık kapsaması bilgi satırı

## UYARI! 31 Eki 16:05 — Can'dan — 17:26 kararı uygulandı: faturasız model saf tahmini geçmiyor (KALDI)
Ne: `sinav.py faz2` 6. madde artık modelin koştuğu bilgiye göre (`sablon_ozet.json` `fatura_kullanildi`); Σ abone kalktı (PR #14 @ d0207fb). Sınav şehirleri 11–20:

| Model | Saf tahmin | Hata | Sonuç |
|---|---|---|---|
| Faturalı | fatura %5,5 / %15,2 | model %3,8 / %8,0 (%31 / %48 düşük) | GEÇTİ |
| Faturasız (`--faturasiz`) | tarife %22,9 / %62,2 | model %20,6 / %50,7 (%10 / %19 düşük) | **KALDI** |

Faturasızda öğlen hatası maddesi de KALDI (%20,6 / %50,7). Düşük güven %100 (UYARI). Geliştirme 1–10'da kapsama da KALDI (%69,6). Ayrıntı docs/log/2026-10-31-can-faz2.md.
Neden: karar masası 17:26 ("KALDI ise KALDI"). Sunum için anlamı: farazide de Faz 2'yi geçiren şey fatura; İspanya'daki %25 → %10 ile aynı mesaj.
Dosya: PR #14, docs/log/2026-10-31-can-faz2.md
Durum: karar verildi 17:38 → can.md: Faz 2 faturalı koşuyla kapanır, faturasız KALDI dürüstlük cümlesine

## KARAR 17:38 — BUILD'e: Faz 2 resmi sonuçtan iki küçük iş (bant kayması, requirements) ve Faz 2 kapanışı
Karar: (1) **Bant yukarı kayık** (Can: gerçek P10'un altında %11, P90'ın üstünde %4): öğlen yükünü yüksek tahmin etmek paneli fazla sığdırır → yanlış yeşil yönü. `sablon.py`'de bir-dışarıda artıkların ortancasıyla kayma düzeltmesi (tahmin ve bant birlikte kaydırılır), 30 dk zaman kutusu; sonra Can `faz2`'yi yeniden koşar. Olmazsa günlüğe "bant %7 yukarı kayık, yanlış yeşil yönü, 1.3" notu. (2) `requirements.txt`'e `python-calamine` (isteğe bağlı, hızlı Excel okuma; yoksa openpyxl) satırı. (3) **Faz 2 kapanır**: resmi ölçüm Can'ın `sinav.py faz2`'si, faturalı koşuyla 7/7 GEÇTİ (ADR-0007 faturayı girdi yaptı); faturasız koşu KALDI ve ROADMAP'te "bilgi: fatura olmadan model saf tahmini ortancada geçmiyor (%10), kazanç P90'da" satırıyla kalır. ROADMAP Faz 2 kutuları Can'ın rakamlarıyla [x]; Faz 2 başlığına "(bitti 31 Ekim, faturalı)". (4) Can'ın bulamadığı KTTO Mart 2023 rapor adresi: karar masası aradı, iki aramada bulunamadı; slaytta "[Kaynaklı: KTTO raporu, Mart 2023; adres doğrulanmadı]" etiketi; bulunursa güncellenir.
Senden beklenen (ana oturum): (1)–(3) bugün; DEVIR.
Durum: yapıldı 17:42 (BUILD) — (1) ortancayla kaydırma işe yaramadı (artık ortancası %0,1, tahmin kaymıyor; kayma bandın şeklinde); bant simetrik yapıldı: sınav 11–20 P10 altı %11 → %6, P90 üstü %4 → %6, kapsama %87,5; Can'ın `faz2`'si yeni bantla 7/7. Günlük: 1.2 günlüğü ek girdi. (2) `python-calamine` 17:30'da eklenmişti. (3) ROADMAP Faz 2 "(bitti 31 Ekim, faturalı)", 7 kutu [x] Can'ın rakamlarıyla, faturasız bilgi satırı; DEVIR.

## UYARI! 31 Eki 17:49 — BUILD'den — Faz 3 varsayım envanteri: kırmızıyı ayar değil bilgi düzeltir; bir varsayım UKPN'le çelişiyor
Ne: Volkan'ın isteğiyle `kac_ev.py`'nin bütün varsayımları listelendi ve tek tek oynatıldı (yalnız şehir 1–10). (1) Bara gerilimi, OG yükselmesi, faz payı, panel yeri hepsi aynı "bugünkü gerilim" tahminini birkaç volt kaydırıyor; sıra uyumu 0,75 hiç değişmiyor → kırmızının kalitesi ayarla değil yeni bilgiyle (panelin adresi/hattaki yeri, fazı, bara gerilimi) artar. (2) **OG öğlen yükselmesi (+%0,8) UKPN ölçümüyle çelişiyor**: İngiltere'de öğlen bara gerilimi geceden ~1 V düşük; aynı varsayım şehir üreticisinde de var. Öneri: üretici 1.3'te ve hesapta 0 ya da eksi. (3) Yeşil iki varsayıma çok duyarlı (yeni panel hat ortasında ya da hat yükü panel akımını azaltır → yeşil %4 → %22–25, şehir 1–10'da yanlış yeşil yine 0); ikisi de sizin kararınız, gerçek veride geri-test olmadan değişmemeli. Hiçbir sayıyı değiştirmedim. Sıradaki: olasılıklı hesap ayrı dalda, aralıklar bu envanterden (üreticinin kendi değerlerinden değil).
Dosya: docs/log/2026-10-31-volkan-faz3-varsayimlar.md
Neden: Volkan "modelin yanlış bulmasının çözümü nedir" sorusu; kod inceleme rehberindeki "ölçülmemiş sayı" kuralı. Bloklamıyor.
Durum: karar verildi 18:46 → volkan.md (KARAR aşağıda): K2 bu gece değişmez, üretici 1.3'te aralık; K9/K6 değişmez

## UYARI! 31 Eki 17:58 — BUILD'den — Faz 3 olasılıklı hesap (PR #15): resmi hesap olsun mu?
Ne: Volkan'ın isteğiyle (modelin yanlış bulduğu yerlerin çözümü) Faz 3 olasılıklı denendi: her trafonun ağı Kıb-Tek'in bildikleriyle kurulur, bilinmeyenler (bara, OG değişimi, hat/sıra, faz, panelin yeri, yük) gerçek veriye dayalı aralıktan 40 kez çekilir, ev ev benzetim koşar. Sınav 11–20 (bir kez, gösterim): yeşil %28, **yanlış yeşil 0/97** (tek denklem 0/21; %40 kuralı 41/284); **yanlış kırmızı %23** (tek denklem %42); **kaç ev hatası 2** (tek denklem 3,5; eşik ≤ 2); sarı %63 (aynı). Bedeli: dolu 74 trafonun 23'ü kırmızı, gerisi sarı ("önce ölç"). Olasılıklar orta ve yüksek kovada gerçekle tutuyor, düşük uçta iyimser (üretici UKPN'le çelişen +%0,8 OG yükselmesi içeriyor; aralıklar üreticiye uydurulmadı). Soru: Faz 3'ün resmi hesabı bu olsun mu? Olursa sözleşme §6'ya üç sütun (`p_bugun_asar`, `p_iki_ev_sigar`, `kac_ev_orta`), Civan'ın paneli ve Can'ın `faz3`'ü güncellenir; kırmızı eşiği 0,5 ilkeden (ayarlanmadı, bedeli günlükte tablo). Canlı için yeşil kuralı gerçek veride (İngiltere 6 hat) geri-test şart.
Dosya: src/kac_ev_olasilik.py, docs/log/2026-10-31-volkan-faz3-olasilik.md (PR #15, PR #13'ün üstünde)
Neden: Faz 3 yanlış kırmızı ve kaç ev maddeleri KALDI; varsayım envanteri (17:49) çözümün ayar değil yapı olduğunu gösterdi.
Durum: karar verildi 18:46 → volkan.md (KARAR aşağıda) + ADR-0011: evet, sözleşmeyi bozmadan (+3 sütun), 45 dk zaman kutusu

## UYARI! 31 Eki 18:09 — BUILD'den — Olasılıklı hesabın İngiltere geri-testi: 6 hattın 5'i kapsandı, biri kaçtı
Ne: Volkan'ın isteğiyle olasılıklı hesabın gerilim tarafı İngiltere UKPN'in 6 gerçek hattında sınandı (ADR-0010 madde 3). Soru: ölçülen panel kaynaklı yükselme, hesabın "%98 güvenli" sınırının (P98) altında mı? Faz bilinmezken (Kıb-Tek'in durumu) ve hat boyu ×0,6–1,6 belirsizken 5/6 evet; **Bancroft'ta hayır** (ölçülen, P98'in 1,3 katı; ev yüksüz ama panelli bir kolda, tek hatlı model kol yapısını görmüyor). Hat boyu kesin sayılınca 4/6. Eski düz model 2/6'da yarıdan az gösteriyordu. Sonuç: yeşil kuralının %2 bütçesi gerçek veride doğrulanmış sayılmaz; olasılıklı hesaba hat boyu belirsizliği ve kol yapısı eklenmeli (farazi şehirde yeşil azalır, ölçülecek); canlıdan önce pilotta sarı uçlarında ölçüm. Sunum cümlesi önerisi günlükte.
Dosya: docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md, src/ukpn_olasilik.py
Neden: PR #15'in resmi hesap olup olmayacağı kararı (17:57 UYARI) bu geri-teste bağlı. Bloklamıyor.
İlerleme 18:43 (BUILD, Volkan "hesaba ekle"): hat boyu ×0,6–1,6 belirsizliği ve altıda bir yüksüz panelli kol PR #15'e eklendi. Sınav 11–20 (bir kez): yeşil %25, yanlış yeşil 0/87, kırmızı %13 (yanlış %27), dolu trafonun kırmızı denen payı 23/74 → 32/74, kaç ev hatası 2, aralık kapsaması %86. Kol oranı aynı 6 İngiliz hattından geldiği için o hatlarda sınanamaz; canlı için pilot şart.
Durum: karar verildi 18:46 → volkan.md (KARAR aşağıda): ADR-0011 madde 5; ekran 4 İngiltere cümlesi günlükteki öneri

## KARAR 18:46 — BUILD'e: Faz 3 resmi hesap olasılıklı (ADR-0011); varsayım envanteri; İngiltere geri-testi
Karar: (1) **Evet, Faz 3'ün resmi hesabı olasılıklı** (PR #15, hat boyu + kol yapısı eklenmiş hâli); [ADR-0011](../decisions/adr-0011-faz3-olasilikli-hesap.md) yazıldı. Sözleşmeyi bozmadan: `kac_ev_olasilik.py` `kac_ev.csv`'yi §6 sütunlarıyla yazar (`kac_ev_karamsar` = çekiliş P10, `kac_ev_iyimser` = P90, `renk` olasılıklı; `isil_pay_kw`, `gerilim_pay_kw_*`, `sinir_karamsar`, `kural40_ev` tek denklemden) + üç yeni sütun `p_bugun_asar`, `p_iki_ev_sigar`, `kac_ev_orta`. Sözleşme 1.3 küçük (ek sütun; §6 karamsar/iyimser açıklaması "çekiliş P10/P90"), Can ya da Civan onayı; harita ve `faz3` değişmeden çalışır. Kırmızı 0,5 ve yeşil 0,98 eşiği kalır (ilkeden). Tek denklem `kac_ev.py` yedek ve pay sütunları için kalır. Sıra: #13 birleşir → #15 üstüne csv + sözleşme notu → onay → birleşir → Can `faz3` **bir kez** koşar; ROADMAP Faz 3 kutuları onunla (yanlış yeşil ve kaç ev GEÇTİ beklenir; yanlış kırmızı %27 ve sarı %62 KALDI, sebep günlükte). **Zaman kutusu 45 dk**; sığmazsa gösterim tek denklem csv ile kalır, olasılıklı günlükte "ikinci sürüm" ve ekran 4'te cümle.
(2) **Varsayım envanteri:** K2 (öğlen OG yükselmesi +%0,8) bu gece ne üreticide ne tek denklemde değişmez (sınav şehirleri donuk, ADR-0009; yeniden üretim yok). Olasılıklı hesap zaten −%0,4…+%0,8 çekiyor. ROADMAP üretici 1.3 listesine: öğlen OG değişimi şehir başına −%0,4…+%0,8 aralığından (UKPN çapası), sabit +%0,8 kalkar. K9/K6 (yeşil gevşetme) değişmez; geri-test (5/6, Bancroft kaçtı) gevşetmeyi haklı çıkarmıyor. K4/K8 ölçümle uyumlu, kalır. Pilotun ilk ölçümü bara gerilimi; Kıb-Tek'ten panelli abonenin adresi ve fazı (01-plan uzman soruları 2–4 zaten kapsıyor).
(3) **İngiltere geri-testi:** sonuç ADR-0011 madde 5'e dürüstçe girdi; yeşilin %2 bütçesi gerçek veride doğrulanmış sayılmaz, canlıda yeşil pilotla sınanır. Sunumda ekran 4 basamak 3 cümlesi günlükteki öneri: "İngiltere'nin 6 gerçek hattında 5'ini kapsadı, birinde yükselmeyi küçük gördü; bu yüzden canlıda yeşil önce pilotla sınanır" (hikâye aynı, rakam değişiyor; Volkan'a söylendi). Kol yapısı ve hat kaydı uzmana soru 3'e bağlı.
Neden: ADR-0010 (yeşil = karamsar + güven + bütçe) olasılıkla doğrudan uygulanıyor; ADR-0009 (aralıklar gerçek veriden, üreticiye uydurma yok) korunuyor; ürünün ana çıktısı kaç ev eşiğe geldi, konut trafosuna yeşil çıktı ve yanlış yeşil yine sıfır; sözleşme 1.2'deki gibi yalnız ek sütunla büyüdüğü için kimsenin işi kırılmıyor.
Senden beklenen (ana oturum): (1) csv + sözleşme 1.3 notu + birleştirmeler + ROADMAP/DEVIR; (2) ROADMAP üretici 1.3 kalemi; (3) yok. Can'a ve Civan'a kutularına yazdım.
İlerleme 18:54 (BUILD): (1) PR #15'te `kac_ev_olasilik.py` artık `kac_ev.csv`'yi §6 sütunlarıyla + `p_bugun_asar`, `p_iki_ev_sigar`, `kac_ev_orta` yazıyor (pay sütunları ve %40 kuralı `kac_ev.py` `sehir_hesapla()`'dan); sözleşme 1.3, yöntem §4–5, README güncel (744b118). 20 şehirde üretildi (~1 dk). Can'ın `sinav.py faz3`'ü (main) bu dosyalarla, sınav 11–20: yanlış yeşil 0/87 GEÇTİ; %40 kuralı 41/284; kaç ev GEÇTİ (karamsar 2); yanlış kırmızı %27,3 ve sarı %62,2 UYARI. **Birleştirme duruyor:** BUILD'in `gh pr merge 13` denemesi izin sisteminde reddedildi (Volkan'ın "Can onaylasın" sözü birleştirme onayı sayılmadı); #13 Can onaylı, #15 sözleşme 1.3 için Can ya da Civan onayı bekliyor; ikisini Volkan birleştirir ya da BUILD'e açıkça "birleştir" der. (2) ROADMAP üretici 1.3'e OG aralığı kalemi. (3) DEVIR'de sunum biçimi satırı düzeltildi.
İlerleme 18:57 (BUILD): #13 birleşti (Volkan sohbette "Evet, birleştir"); #15'in tabanı main'e çevrildi, çakışma yok, sözleşme 1.3 için Can ya da Civan onayı bekliyor (can.md 18:56). Main'de yedek yol denendi: `kac_ev.py` + `sinav.py faz3` çalışıyor.
Durum: yapıldı 19:45 (BUILD) — #13 ve #15 main'de (#15 Volkan 19:37); `kac_ev.csv` sözleşme 1.3 ile olasılıklı hesaptan. Kalan: Can main'de `faz3` bir kez → BUILD ROADMAP Faz 3 kutuları (DEVIR açık işler 3).

## UYARI! 31 Eki (18:57 sonrası) — Can'dan — PR #15 deneme koşusu: rakamların tuttu; karamsar sayı 36 trafoda gerçeğin üstünde
Ne: #15'in `kac_ev_olasilik.py`'siyle ayrı bir kopyada (tahmin main'in simetrik bandıyla yeniden) sınav 11–20'de main'deki `sinav.py faz3`'ü bir kez denedim; resmi değil, günlüğe yazılmadı (resmi koşum #15 birleşince). (1) Rakamların birebir tuttu: yanlış yeşil 0/87, yanlış kırmızı %27,3, sarı %62,2, kaç ev karamsar 2 ve **ortası (`kac_ev_orta`) 2 → GEÇTİ** (18:54 önerin 5fa8c42'de). Aralık kapsaması tavan = 1 dahil %86,5 (seninkiyle aynı), sınavın tanımıyla (tavan = 0) %80,4. (2) **Yeni bulgu:** gerçek < `kac_ev_karamsar` olan trafo 36/240 (%15; tek denklemde 0). 20'si şehir konutu (fark ortancası 5 ev, 18'i sarı, 2'si yeşil), 6 yurt, 6 çarşı, 1 otel, 1 sulama, 1 köy; 12'si yeşil, ama hiçbiri dolu değil (yanlış yeşil 0). Yani renk güvenli; **haritada "en az … ev" diye gösterilen karamsar sayı** %15 trafoda fazla söylüyor (P10'dan beklenen ~%10). Soru: haritada karamsar sayı "en az" diye mi kalsın, yoksa yalnız `kac_ev_orta` + renk mi gösterilsin?
Dosya: src/kac_ev_olasilik.py (PR #15), docs/data/tablo-bicimi.md §6, app/ (Civan'ın yan paneli)
Neden: Kaç ev, ürünün ana çıktısı; "en az" denen sayının gerçeği aşması yanlış yeşil yönü. Bloklamıyor; sözleşme 1.3 onayını Can bekletmiyor, kullanıcıya soruldu.
Durum: karar verildi 19:13 → can.md (aralık kalır, "en az" kelimesi gider; manşet orta sayı + %80 bant; vaat renkte) + civan.md (yan panel dili) + volkan.md (BUILD: sözleşme ve yöntem cümlesi)

## KARAR 19:13 — BUILD'e: kaç ev sayısının dili — karamsar/iyimser %80 bant, taban değil ("en az" yok)
Karar: Can'ın bulgusu (gerçek, çekiliş P10'unun altında 36/240 = %15; tek denklemde 0) ürünü değiştirmiyor, dili değiştiriyor: `kac_ev_karamsar` / `kac_ev_iyimser` = çekilişlerin P10 / P90'ı, yani Faz 2'deki gibi **%80 bant**; taban değil. Manşet sayı `kac_ev_orta`; vaat renkte (yeşil = ilk 2 başvuru ≥ %98 sığar, ADR-0010). Bant kalibrasyonu (P10 altı / P90 üstü, hedef ~%10 / %10) Faz 2'deki gibi bilgi satırı olur, madde değil; %15'in sebebi bilinen iyimserlik (üreticideki +%0,8 OG, panellerin uca kayması) → üretici 1.3.
Senden beklenen (ana oturum, 1.3 notuna 2 cümle): sözleşme §6'da `kac_ev_karamsar` / `kac_ev_iyimser` açıklaması "çekilişlerin P10 / P90'ı; %80 bant, 'en az' değil"; `modeling.md` §4'e aynı cümle; konuşma notu taslağında "en az … ev" varsa "yaklaşık N ev (A–B)". Başka iş yok; 45 dk kutun aynı.
Durum: yapıldı 19:15 (BUILD) — sözleşme §6 karamsar/iyimser "%80 bant, 'en az' değil", `kac_ev_orta` "yaklaşık N ev (karamsar–iyimser)", modeling.md §4 aynı cümle: PR #15 (12d726e); konuşma notu taslağında "en az" yoktu, otel örneği "yaklaşık N ev (A–B)" ve yeşil cümlesi "%98" diye düzeltildi (main).

## KARAR 19:44 — BUILD'e (Volkan'ın isteği, BUILD 19:4x mesajı): Faz 3 açık eksikleri — bu gece ne, pilotta ne
Karar: **Faz 3 bu gece kapanır (gösterim), açık eksikler pilota.** #15 birleşti (19:37). Can'ın resmi `faz3`'ü gelince ROADMAP Faz 3 kutuları: yanlış yeşil [x], %40 kuralı yan yana [x], kaç ev ≤ 2 [x] (orta 2), yanlış kırmızı ve sarı [x] "raporlandı, hedef üstü, sebep bilgi eksikliği" (Faz 2'deki faturasız satırı gibi). Başlık: "(bitti 31 Ekim, gösterim; açık eksikler pilotta)". ROADMAP Faz 3'e **"Açık eksikler"** bölümü, bu tabloyla:

| # | Eksik (sınav 11–20) | Bu gece | Pilot / sunum sonrası |
|---|---|---|---|
| 1 | Yanlış kırmızı %27 (hedef ≤ %20) | (a) bilginin değeri denemesi rakamını verir; madde "raporlandı" | bara gerilimi (akıllı priz gece seviyesi, trafo plakası kademe); Kıb-Tek'ten panelli abonenin adresi ve fazı (uzmana soru 2, 4, 8) |
| 2 | Sarı %62 (hedef ≤ %30) | eşik **0,98 kalır** (tablo aşağıda) | ölçüm cihazı sarılara (asıl pilot); 1'deki bilgiler |
| 3 | Yeşil bütçesi (%2) gerçek veride doğrulanmadı (İngiltere 5/6, Bancroft) | iş yok; ekran 4 cümlesi hazır (Can) | inverter uygulamasının 5 dk gerilim kaydı (panelli evler, izinle) + sarıların hat ucunda öğlen gerilimi; her ölçülen hat geri-teste; kol yapısı (soru 3) |
| 4 | Olasılık düşük uçta iyimser (%10–30 diyene ~%43 aşıyor) | iş yok: sınav şehirleri donuk, gece yeniden üretim bütün rakamları değiştirir (ADR-0009) | üretici 1.3: OG aralığı (ROADMAP'te), panellerin uca kayma dağılımı; sonra kalibrasyon yeniden |
| 5 | Kaç ev aralığı taban değil (P10 altı %15) | çözüldü: dil 19:13, Can'ın bilgi satırı (c3fb046) | üretici 1.3 ile yeniden ölç |
| 6 | Faturasız model basit tahmini geçmiyor (Faz 2) | iş yok | Kıb-Tek'ten trafo başına fatura toplamı = pilotun veri isteği (soru 7) |

**(a) Bilginin değeri denemesi: onay, bu gece, yeni BUILD'in ilk işi, zaman kutusu 60 dk.** `kac_ev_olasilik.py`'ye dokunmadan ayrı deney betiği; resmi `kac_ev.csv` ve sınav rakamları değişmez; ayar yok. Senaryolar: S0 bugünkü; S1 bara gerilimi bilinir (cevap anahtarı `v0_v`); S2 panelli evlerin hattaki yeri bilinir (üreticiden, aynı tohum; yalnız deney); S3 tek fazlıların fazı bilinir (`faz_a_ev`…); S4 hepsi. Ölçüler: yanlış kırmızı, sarı, yeşil, yanlış yeşil, kaç ev hatası. Şehir 1–10, sonra 11–20 bir kez. Etiket: "üst sınır (kusursuz bilgi, farazi şehir)"; gerçek ölçüm gürültülü olur. Çıktı: Faz 3 günlüğüne tablo + Can'a ekran 6 için tek cümle ("bara gerilimini ölçmek yanlış kırmızıyı %27'den %x'e indirir"). Bilgi kaynağı eşlemesi günlükte: S1 ← akıllı priz / plaka, S2 ← Kıb-Tek abone adresi, S3 ← Kıb-Tek bağlantı kaydı. 60 dk'ya sığmazsa bırak, ekran 6 bugünkü cümleyle kalır.

**(b) Yeşil eşiği: yapıldı (karar masası, 19:44), eşik 0,98 kalır.** Hesap: #15 birleşik kodla Mac'te üretilen 20 şehrin `kac_ev.csv`'sinden (40 çekilişte 0,98 = 40/40, 0,95 = 38/40); kırmızı kuralı aynı, yeşil = `p_iki_ev_sigar` ≥ eşik ve güven yüksek:

| Eşik | Geliştirme 1–10 (354 trafo, 55 dolu): yeşil / sarı / yanlış yeşil | Sınav 11–20 (347, 73 dolu, bilgi): yeşil / sarı / yanlış yeşil |
|---|---|---|
| **0,98** | %23 / %68 / **0/83** | %25 / %62 / **0/87** |
| 0,95 | %31 / %61 / 1/108 (en kötü şehir %7,7) | %33 / %54 / 1/116 |
| 0,90 | %35 / %56 / 2/124 | %38 / %49 / 1/132 |
| 0,80 | %45 / %46 / 3/159 (en kötü %10) | %45 / %42 / 3/156 |

Neden 0,98: 0,95'te dolu trafoya ilk "yer var" geliyor (geliştirme şehirlerinde de); 0,80'e kadar inse bile sarı %46'nın altına düşmüyor, yani sarıyı eşik değil bilgi düşürür; bütçe gerçek veride doğrulanmadı (Bancroft). Karar 1–10 ve ilkeden; 11–20 yalnız bilgi. Tablo Faz 3 günlüğüne "eşiğin bedeli" olarak (yeni BUILD kopyalar). Jüri cevabı: "Eşiği gevşetsek sarı ancak yarıya iner ve dolu trafoya 'yer var' demeye başlarız; sarıyı azaltan şey ölçüm."

**Veri alma yolları (BUILD notu, pilot sırası, ucuzdan pahalıya):** (1) panelli evlerin inverter uygulaması 5 dk gerilim kaydı, izinle (bedava; Kıbrıs'tan ilk hat ucu gerilimi; eksik 3); (2) gerilim ölçen akıllı priz birkaç evde (15–20 €; gece bara seviyesi; eksik 1–2); (3) trafo plakası fotoğrafı (uk, kademe; soru 8); (4) Kıb-Tek'ten abone–trafo eşleşmesi, panelli abonenin adresi ve fazı, trafo başına fatura toplamı (soru 2, 4, 6, 7); (5) sarı trafoların hat ucunda geçici ölçüm cihazı (asıl pilot); (6) uydu görüntüsünde panel sayımı (yaygınlık, ADR-0006 BULAMADIM). Kampta uzmana 2, 3, 4, 6, 7, 8. Şartname: Kıb-Tek ihale ilanları / EMO / yetki belgeli firma.
Neden: Sunum yarın; Faz 3'ün ürünü (yanlış yeşil 0, kaç ev ≤ 2) geçti, kalan iki hedef bilgi eksikliğinden ve bu gece ayarla kapanmaz (varsayım envanteri). (a) bu zayıflığı pilotun rakamlı isteğine çeviriyor, ekran 6'yı güçlendiriyor. 4 ve 5'in kökü üretici; gece yeniden üretim sınavı ve sunum rakamlarını bozar.
Senden beklenen (yeni BUILD, DEVIR'den devralır): (1) ROADMAP Faz 3 kutuları Can'ın resmi `faz3`'üyle + "Açık eksikler" bölümü + DEVIR; (2) (a) denemesi, 60 dk; (3) (b) tablosunu Faz 3 günlüğüne. Sonra Faz 5 (prova).
Durum: yapıldı 19:59 (BUILD) — (1) ROADMAP Faz 3 kutuları, başlık ve "Açık eksikler" tablosu (936566e); (2) (a) denemesi `src/bilgi_degeri.py`, tablo Faz 3 günlüğünde (1ebd6a7): sınav 11–20 yanlış kırmızı bara bilinirse %19, bara + panel yeri + faz %4; sarı ancak %57 (ağın tamamıyla %41) → UYARI 19:59 aşağıda; Can'a ekran 6 cümlesi (can.md 19:59); (3) (b) tablosu Faz 3 günlüğünde aynen. DEVIR güncel.

## KARAR 19:51 — BUILD'e: Faz 3 KAPANDI (Volkan); Can'ın resmi koşumu beklenmez, kutular karar masasının koşumuyla
Karar: Volkan (19:51, sohbette): "Can'ın resmi sınav koşumuna gerek yok, bitti, kapat." Faz 3 resmi ölçümü = karar masasının Mac koşumu: main'in son hâli (fe7426b + Can'ın sinav.py c3fb046), 20 şehir sıfırdan üretildi (üretici 1.2, EAC profilleri, Open-Meteo 2023, kıyı kontrolü), `sablon.py` → `kac_ev_olasilik.py` → `sinav.py faz3`. Sınav şehirleri 11–20 resmi, 1–20 bilgi. ROADMAP Faz 3 kutuları: [x] yanlış yeşil 0/87 (en kötü şehir 0/12); [x] %40 kuralı yan yana 41/284 (%14,4), dolu trafoya "yer var" 41/73 ↔ biz 0/73; [x] yanlış kırmızı raporlandı %27,3 (12/44), hedef üstü, sebep bilgi eksikliği (19:51 öncesi 19:44 KARAR tablosu); [x] kaç ev hatası orta 2 ev (karamsar 2, iyimser 4; n 239, tavanlı 108 ayrı); [x] sarı raporlandı %62,2 (216/347), hedef üstü, sebep aynı. Başlık "(bitti 31 Ekim, gösterim; açık eksikler pilotta)". Etiket: "karar masası koşumu, Mac, 31 Ekim 19:35–19:50; Can'ın #15 deneme koşusuyla birebir (0/87, %27,3, %62,2, 2 ev)".
Senden beklenen (BUILD): ROADMAP Faz 3 kutuları ve "Açık eksikler" bölümü (19:44 KARAR); Faz 3 günlüğüne aşağıdaki iki çıktı aynen (başlığıyla "karar masası koşumu"); DEVIR "Faz 3 bitti". Can'a ayrıca yazdım: koşum istenmiyor, ekran 5 rakamları buradan.

Sınav çıktısı, 11–20 (resmi):
```
Faz 3 geçme sınavı: 10 şehir (sehir-011…sehir-020), 400 trafo — gösterim, farazi şehirler

[GEÇTİ] yanlış yeşil ≤ %5, en kötü şehirde ≤ %10: %0.0 (0/87); en kötü şehir %0.0 (0/12) sehir-011; yeşili olan şehir 10/10; dolu trafoya yeşil %0.0 (0/73)
[GEÇTİ] %40 kuralının yanlış yeşili aynı trafolarda, yan yana: %40 kuralı %14.4 (41/284) (en kötü şehir %26.1 (6/23) sehir-014), model %0.0 (0/87); dolu trafoya "yer var": %40 kuralı %56.2 (41/73), model 0/73
[UYARI] yanlış kırmızı raporlandı (hedef ≤ %20): %27.3 (12/44); kırmızı payı %12.7 (44/347); dolu yakalanan (kırmızı) 32/73; hedefin üstünde
[GEÇTİ] kaç ev hatası ortanca ≤ 2 ev (en az bir sayı): karamsar 2, iyimser 4, ortası (kac_ev_orta) 2 ev; eşiği geçen: karamsar, ortası (kac_ev_orta); n = 239, tavan = 1 ayrı 108
[UYARI] sarı oranı raporlandı (hedef ≤ %30): %62.2 (216/347); hedefin üstünde, sebep BUILD günlüğünde

Bilgi:
  canlı bütçe (ADR-0010) yanlış yeşil < %2: tutuyor (%0.0 (0/87); farazi şehir, gösterim)
  kaç ev hatası ortancası, tavan = 1 dahil (gerçek alttan kesik): karamsar 1, iyimser 1, ortası (kac_ev_orta) 1 ev (n = 347)
  küme: kac_ev_aday > 0 347 trafo (73 dolu); aday = 0 ayrı 53
  renk: yesil 87, sari 216, kirmizi 44
    sehir_konutu (n 139, dolu 35): yesil 6, sari 110, kirmizi 23; ortanca gerçek / karamsar / iyimser 14 / 0 / 19 ev
    koy (n 57, dolu 30): yesil 1, sari 35, kirmizi 21; ortanca gerçek / karamsar / iyimser 0 / 0 / 11 ev
    carsi (n 43, dolu 0): yesil 28, sari 15, kirmizi 0; ortanca gerçek / karamsar / iyimser 9 / 9 / 9 ev
    otel (n 42, dolu 0): yesil 35, sari 7, kirmizi 0; ortanca gerçek / karamsar / iyimser 4 / 4 / 4 ev
    sulama (n 30, dolu 7): yesil 0, sari 30, kirmizi 0; ortanca gerçek / karamsar / iyimser 2 / 1 / 3 ev
    yurt (n 36, dolu 1): yesil 17, sari 19, kirmizi 0; ortanca gerçek / karamsar / iyimser 5 / 6 / 6 ev
  aralık kapsaması (gerçek kac_ev_gercek [karamsar, iyimser] içinde; tavan = 0): %81.2 (194/239); gerçek < karamsar 36, gerçek > iyimser 9
  kaç ev bandı (tavan = 0; beklenen ~%10 / ~%10): P10 altı %15.1 (36/239), P90 üstü %3.8 (9/239); P10 altı tipe göre: sehir_konutu 20 (fark ortanca 5 ev), carsi 6 (fark ortanca 1 ev), yurt 5 (fark ortanca 2 ev), sulama 2 (fark ortanca 1 ev), otel 2 (fark ortanca 1 ev), koy 1 (fark ortanca 1 ev); P10 altı yeşil 12, bunlardan dolu 0
  sinir_karamsar: gerilim 347
```

Sınav çıktısı, 1–20 (bilgi):
```
Faz 3 geçme sınavı: 20 şehir (sehir-001…sehir-020), 800 trafo — gösterim, farazi şehirler

[GEÇTİ] yanlış yeşil ≤ %5, en kötü şehirde ≤ %10: %0.0 (0/170); en kötü şehir %0.0 (0/10) sehir-001; yeşili olan şehir 20/20; dolu trafoya yeşil %0.0 (0/128)
[GEÇTİ] %40 kuralının yanlış yeşili aynı trafolarda, yan yana: %40 kuralı %12.7 (73/573) (en kötü şehir %26.1 (6/23) sehir-014), model %0.0 (0/170); dolu trafoya "yer var": %40 kuralı %57.0 (73/128), model 0/128
[UYARI] yanlış kırmızı raporlandı (hedef ≤ %20): %28.9 (22/76); kırmızı payı %10.8 (76/701); dolu yakalanan (kırmızı) 54/128; hedefin üstünde
[GEÇTİ] kaç ev hatası ortanca ≤ 2 ev (en az bir sayı): karamsar 3, iyimser 3, ortası (kac_ev_orta) 1 ev; eşiği geçen: ortası (kac_ev_orta); n = 484, tavan = 1 ayrı 217
[UYARI] sarı oranı raporlandı (hedef ≤ %30): %64.9 (455/701); hedefin üstünde, sebep BUILD günlüğünde

Bilgi:
  canlı bütçe (ADR-0010) yanlış yeşil < %2: tutuyor (%0.0 (0/170); farazi şehir, gösterim)
  kaç ev hatası ortancası, tavan = 1 dahil (gerçek alttan kesik): karamsar 1, iyimser 1, ortası (kac_ev_orta) 1 ev (n = 701)
  küme: kac_ev_aday > 0 701 trafo (128 dolu); aday = 0 ayrı 99
  renk: yesil 170, sari 455, kirmizi 76
    sehir_konutu (n 277, dolu 55): yesil 12, sari 237, kirmizi 28; ortanca gerçek / karamsar / iyimser 16 / 0 / 18 ev
    koy (n 117, dolu 59): yesil 1, sari 72, kirmizi 44; ortanca gerçek / karamsar / iyimser 0 / 0 / 10 ev
    carsi (n 83, dolu 0): yesil 55, sari 28, kirmizi 0; ortanca gerçek / karamsar / iyimser 10 / 10 / 11 ev
    otel (n 79, dolu 0): yesil 62, sari 17, kirmizi 0; ortanca gerçek / karamsar / iyimser 4 / 4 / 4 ev
    sulama (n 64, dolu 13): yesil 0, sari 60, kirmizi 4; ortanca gerçek / karamsar / iyimser 2 / 1 / 3 ev
    yurt (n 81, dolu 1): yesil 40, sari 41, kirmizi 0; ortanca gerçek / karamsar / iyimser 6 / 6 / 7 ev
  aralık kapsaması (gerçek kac_ev_gercek [karamsar, iyimser] içinde; tavan = 0): %79.3 (384/484); gerçek < karamsar 65, gerçek > iyimser 35
  kaç ev bandı (tavan = 0; beklenen ~%10 / ~%10): P10 altı %13.4 (65/484), P90 üstü %7.2 (35/484); P10 altı tipe göre: sehir_konutu 35 (fark ortanca 5 ev), yurt 12 (fark ortanca 1.5 ev), carsi 7 (fark ortanca 1 ev), koy 4 (fark ortanca 2.5 ev), otel 4 (fark ortanca 1 ev), sulama 3 (fark ortanca 1 ev); P10 altı yeşil 15, bunlardan dolu 0
  sinir_karamsar: gerilim 701
```
Durum: yapıldı 19:59 (BUILD) — kutular [x] ve başlık "(bitti 31 Ekim, gösterim; açık eksikler pilotta)" (936566e); iki çıktı Faz 3 günlüğünde aynen, başlık "karar masası koşumu" (1ebd6a7); DEVIR "Faz 3 bitti". Not: BUILD klasöründeki 16:57 şehirlerinde `sinav.py faz3` aynı renkleri verir ama dolu 74 / n 240 (sizde 73 / 239): tek trafo farkı, sebep aranmadı, günlükte.

## UYARI! 31 Eki 19:59 — BUILD'den — Bilginin değeri: kırmızıyı bilgi düzeltir, sarıyı düzeltmez; jüri cevabı ve ekran 6
Ne: (a) denemesi yapıldı (resmi hesap ve rakamlar değişmedi; kusursuz bilgi üst sınırı, farazi şehir). Sınav 11–20, bir kez: **yanlış kırmızı** bugün %27 → bara bilinirse **%19** (hedef ≤ %20 tutar) → bara + panelli evin yeri + faz **%4**, dolu trafoyu kırmızı görme 32 → 43. **Sarı** ise %62 → %57 (üç bilgi) → %53 (+ öğlen yükü) → **%41** (ağın tamamı + yük; sarının sebebini ayırmak için eklenen iki teşhis satırı). Tam ağda bile 104 sarı trafo gerçekte yeşil olabilirdi: kalan sarı bilgi eksikliği değil, yeşilin sorusu ("sıradaki iki başvuru, kimden gelirse gelsin, %98 sığar") — başvurunun hattın neresinden geleceği bilinmiyor. Ayrıca kusursuz bilgide aralık kapsaması %80 → %57 ve ilk yanlış yeşil (1/166): eksik 4'ün (düşük uçta iyimser) kökü, bilgi gelince aralıklar yeniden ayarlanmalı.
Üç soru:
(1) **Jüri cevabı** (19:44): "sarıyı azaltan şey ölçüm" deneme ile tam tutmuyor. Öneri: "Eşiği gevşetsek dolu trafoya 'yer var' demeye başlarız. Ölçüm kırmızıdaki yanılmayı düzeltir; sarı ise 'sıradaki başvuru nereden gelecek' sorusu, onu başvuru anında evin adresiyle tek tek hesaplarız." Son kısım sınanmadı [Yorum].
(2) **Ürün önerisi:** sarı trafoda karar başvuru anında, o evin adresi ve fazıyla tek hesap ("bu başvuru sığar mı"). Pilot / ikinci sürüm listesine girsin mi? Bu gece kod yok.
(3) **Ekran 6** "Kıb-Tek'ten yeni veri istemiyoruz" diyor; %4'e inmek panelli abonenin adresi ve fazını ister (Kıb-Tek kaydında olabilir; uzmana soru 2, 4, 6). Cümle kalsın mı, "elindeki kayıtlardan adres ve faz" mı desin? Can'a şimdilik yalnız bara yarısını kullanmasını yazdım.
Dosya: docs/log/2026-10-31-volkan-faz3.md (19:55 ek girdi), ROADMAP Faz 3 "Açık eksikler", src/bilgi_degeri.py
Neden: KARAR 19:44 (a). Bloklamıyor; BUILD Faz 5'e (konuşma notu, prova) geçiyor.
Durum: karar verildi 20:47 → volkan.md (KARAR aşağıda) + ADR-0012 + can.md: jüri cevabı yeni cümle; başvuru-anı kararı ikinci sürüme (sınanmadı); ekran 6 cümlesi bara ölçümüyle

## UYARI! 31 Eki 20:43 — BUILD'den — Ada ülkeleri: Malta'nın açık haritası da düz %25 tavan; Gozo hattı dış sınama adayı
Ne: Volkan'ın isteğiyle ada şebekeleri tarandı ve kullanılabilir açık veri arandı (günlük). Üç kullanılabilir şey çıktı.
(1) **Enemalta'nın kapasite haritası açık veri** (1.332 trafo merkezi: güç, en yüksek talep, boş güç, izin verilen ek panel). İzin verilen ek panel hiçbir merkezde trafo gücünün **%25'ini geçmiyor**: 245'inde tam %25, 290'ında sıfır [Hesap]. Enemalta gerilim ölçütü de kullandığını söylüyor ama yöntemi yayınlamıyor. Akıllı sayaçlar kayıp ve faturalama için alınmış; panel kuralını sayaçla koyduklarına kanıt BULAMADIM.
(2) **Malta'da sınırı gerilim ve kademe koymuş** (Graz 2016; trafolar boşta 250 V, Kıb-Tek şartnamesiyle aynı). Gozo'da bir hattın tam tablosu var: 500 kVA, 18 panelsiz ev; +1 kWp/ev kademe, +2 kWp/ev trafo değişimi.
(3) **Hawaii düz kuralı kanıtla gevşetmiş:** tepe yükün %15'i → gündüz en düşük yükün %250'si; ev trafosu eleği gücün %166'sı. Ölçülmeyen hattı benzer ölçülen hattan tahmin etmişler; bizim yöntemin emsali.
Üç soru:
(a) Sunuma girsin mi? Öneri, jüri "Malta akıllı sayaçla çözdü" derse: "Akıllı sayacı olan Malta bile haritasında trafo başına düz bir tavan kullanıyor, gücün %25'i; Kıb-Tek %40. Biz her trafoya gerilimle ayrı bakıyoruz." Hawaii: "Hawaii düz kuralı kanıt geldikçe %15'ten %250'ye çıkardı; bizim harita o kanıtın trafo trafo hâli." (`docs/sunum/` Can'ın.)
(b) Gozo hattında hesabımız bu gece dış sınama olarak koşulsun mu? Hat boyu ve kablo aralıkla; tek hat, gösterim; 30 dk.
(c) Üretici 1.3 listesine "trafo boyutu çapası: Malta en yüksek talep ÷ güç P10/50/90 0,13 / 0,42 / 0,74" girsin mi? Bizim Nisan tepesi ortanca 0,27, ama Malta'nınki bütün yıl: birebir kıyas değil.
Dosya: docs/log/2026-10-31-volkan-ada-ulkeleri.md, NOTLAR.md; ham veri depo dışında (lisans yazılı değil), KAYNAK için can.md 20:43
Neden: Kıb-Tek'in %40 kuralına dış kıyas ve jüri sorusu ("akıllı sayaç neden yok"). Bloklamıyor.
Durum: karar verildi 20:47 → volkan.md (KARAR aşağıda) + can.md: Malta ve Hawaii jüri cevabı + kaynak slaydı; Gozo sınaması bu gece YOK; üretici 1.3 çapası evet

## KARAR 20:47 — BUILD'e: bilginin değeri (19:59) ve ada ülkeleri (20:43)
Karar:
**Bilginin değeri.** (1) Jüri cevabı değişti; yeni cümle (Can'a yazıldı, düz dille): "Eşiği gevşetsek dolu trafoya 'yer var' demeye başlarız. Ölçüm kırmızıdaki yanılmayı düzeltir: trafonun çıkış gerilimi bilinince yanlış kırmızı %27'den %19'a iner. Sarının çoğu ise 'bir sonraki başvuru hattın neresinden gelecek' sorusu; onu haritada değil başvuru anında, evin adresiyle tek tek hesaplarız." Son cümle konuşma notunda "sınanmadı" etiketli; slaytta yazılmaz. (2) **Ürün önerisi kabul, sınanmadı:** [ADR-0012](../decisions/adr-0012-sari-trafoda-karar-basvuru-aninda.md) yazıldı: sarı trafoda karar başvuru anında, başvuranın adresi ve fazıyla; ADR-0010 madde 2'nin (kümülatif) yeri. ROADMAP Faz 3 ikinci sürüm listesine madde, "Açık eksikler" sarı satırının pilot sütununa bağlantı. Bu gece kod yok. (3) **Ekran 6 cümlesi kalır, netleşir:** "Harita için Kıb-Tek'ten yeni veri istemiyoruz: abone sayısı ve fatura toplamı zaten elinde. Pilotta ilk ölçeceğimiz şey trafonun çıkış gerilimi; o tek ölçüm 'dolu' dediğimiz trafolardaki yanılmayı %27'den %19'a indirir." %4 rakamı konuşma notuna: "Kıb-Tek'in kendi kayıtlarında panelli abonenin adresi ve fazı varsa %4'e" [Hesap: bilginin değeri, kusursuz bilgi üst sınırı, farazi 11–20]. (4) Günlükteki "kusursuz bilgide hesap kendinden fazla emin" bulgusu (S6: kapsama %57, 1 yanlış yeşil) "Açık eksikler" 4. satırına (düşük uç iyimser) not olarak; pilotta aralıklar ölçümle yeniden ayarlanır (ADR-0011 madde 5 zaten).
**Ada ülkeleri.** (a) **Sunuma girer, ama ana ekran olarak değil:** jüri cevabı ("akıllı sayaç neden yok / Malta nasıl yaptı") ve kaynak slaydı satırı. Cümleler Can'a yazıldı; Malta cümlesi "kural" demez, "haritasındaki izin hiçbir merkezde gücün %25'ini geçmiyor" der, etiketi [Hesap: Enemalta kapasite haritası verisi, 31 Ekim 2026; lisans belirsiz, ham veri depoda yok; Enemalta'nın yazdığı kural değil bizim çıkarımımız]. Hawaii cümlesi [Kaynaklı: HECO 2014; Sunrun 2022]. (b) **Gozo hattı bu gece koşulmaz.** Hat boyu, kablo ve ev sayısı bilinmiyor; sonuç geniş bir aralık olur, "tek hat, gösterim" jüriye İngiltere 6 hattın üstüne bir şey eklemez; gece önceliği Faz 4 ve prova. Pilot öncesi "dış sınama adayları" listesine (ROADMAP Faz 3 ikinci sürüm) İngiltere'nin yanına. (c) **Üretici 1.3 çapası evet:** "trafo boyutu: Malta en yüksek talep ÷ güç P10/50/90 0,13 / 0,42 / 0,74 (yıl tepe); bizim Nisan tepe ÷ kVA 0,16 / 0,27 / 0,47; kıyas için Nisan/yıl tepe oranı EAC profillerinden türetilir" ROADMAP üretici 1.3 listesine. Ham veri depo dışında kalır, KAYNAK satırı Can'da.
**BUILD'in bu geceki sırası:** (1) ROADMAP/DEVIR güncellemeleri (yukarıdakiler, 15 dk); (2) **Faz 4 sınavının Mac kısmı**: Civan'ın uygulamasını Mac'te çalıştır, internetsiz açılış, 3 şehir seçimi, yan paneldeki sayıların `kac_ev.csv` ile 3 trafoda birebir kontrolü, tıklama süresi; sonucu civan.md'ye "## KONTROL" girdisiyle ve ROADMAP Faz 4 kutularına (ölçülen kadarı) yaz; app/ dosyalarına dokunma, düzeltmeyi Civan yapar; (3) konuşma notu ve prova. Yeni araştırma yok.
Neden: Bilginin değeri denemesi kırmızıyı bilginin, sarıyı karar biriminin düzelttiğini gösterdi; ADR-0010 kümülatif onay zaten başvuru bazlı. Ada araştırması jüri sorusunu cevaplıyor, hikâyeyi değiştirmiyor; Gozo testi bilgi yokluğunda rakam üretmez (CLAUDE.md: rakam uydurma). Faz 4'ün beş kutusu da açık ve Civan 17:28'den beri sessiz; en riskli yer orası.
Senden beklenen (BUILD): yukarıdaki sıra; (2)'nin sonucu kutuya.
Durum: (1) yapıldı 20:49 (BUILD) — ROADMAP Faz 3 ikinci sürüm: ADR-0012 maddesi ve dış sınama adayları (İngiltere, Gozo); Açık eksikler sarı satırı ADR-0012'ye bağlandı, 4. satıra S6 notu; üretici 1.3'e Malta trafo boyutu çapası; DEVIR. (2) yapıldı 20:55: Faz 4 Mac kontrolü civan.md KONTROL 20:55 ve ROADMAP Faz 4 (sayılar birebir ve 3 şehir [x]; tıklama 0,35–0,40 sn; dışarıya istek yok; Windows, ekran kaydı denenmedi). İki bulgu Civan'da: dil 19:13'e göre değil; %40 kuralının ev sayısı 701 trafonun 241'inde aday evden fazla. (3) yapıldı 20:58: konuşma notu taslağı güncel (İngiltere 5/6, pilot cümlesi %27 → %19 ve %4 yalnız konuşmada, kırmızı tanımı, kilit cümle 41/73 ↔ 0/87, yeşil %25 / sarı %62, sarı / Malta / Hawaii jüri cevapları, sehir-001 tıklama sırası T02 / T06 / T07, prova listesi). Prova insanların; BUILD'in yapacağı kalmadı.

## UYARI! 31 Eki (20:58 sonrası) — Can'dan — Haritada Malta gibi iki sayılı kart: "yük için boş kapasite" + "güneş için boş kapasite" — yapalım mı, nasıl?
**Ne yapmak istiyoruz:** Enemalta'nın haritasında her trafo merkezine tıklayınca iki sayı çıkıyor: "Available Load Capacity: 346 kVA" (tüketime kalan yer) ve "RES Available Capacity: 244 kWp" (güneşe kalan yer). Bizim harita bugün yalnız güneşe bakıyor (renk + kaç ev). İstediğimiz: her trafoda aynı iki sayı, ama dürüst hâli — tahmin, aralıklı, "ölçülmedi" etiketiyle: "Yük için boş: ~480 kW (…–…), Nisan · Güneş için boş: ~90 kW (78–91)". Sunum cümlesi önerisi [Yorum]: "Malta bu kartı her eve sayaç takarak çıkardı; biz az trafoyu ölçüp kalanını aynı biçimde, aralıkla gösteriyoruz." (Senin 20:43 bulgunu gördüm: Malta'nın güneş sayısı düz %25 tavan; bu bizim için daha da iyi — bizimki her trafoda fizikten.)

**Teknik durum** (deneme: sınav şehirleri 11–20, #15 olasılıklı `kac_ev.csv`, ölçülmeyen trafolar; [Hesap: Can, scratchpad betiği, resmi değil] — gösterim):
1. **Güneş için boş kapasite: zaten var.** `kac_ev_orta` × 6,5 kW, bant karamsar–iyimser × 6,5. Gerçeğe hata ortanca 13 kW (~2 ev), bant gerçeği %81,3 tutuyor (n 171, tavan = 0). Ama `isil_pay_kw` / `gerilim_pay_kw_*` hâlâ tek denklemden; onlardan kurulan bant %75,4 tutuyor → ikisi yan yana gösterilirse çelişebilir. Bu sayı yıl boyu geçerli (en kötü an bahar öğleni, ADR-0002).
2. **Yük için boş kapasite: yok.** Model en yüksek yükü tahmin etmiyor (`tepe_kw` yalnız cevap anahtarında). Üç yol denedim; boş kapasite = `kva` − tahmini tepe (cos φ = 1 varsayımı):
   | Yol | Tepe hatası ortanca / P90 | Boş kapasite hatası ortanca / P90 |
   |---|---|---|
   | Sözleşme §5 eğri ölçekleme (`ogle_min_kw` ÷ arketipin öğlen en düşük `oran`'ı) | %15,9 / %32,8 | 5,5 / 62,8 kW |
   | Saf: fatura × ölçülülerin Σ tepe ÷ Σ fatura | %3,9 / %17,0 | 1,4 / 29,2 kW |
   | **`ogle_min_kw` × ölçülülerin tepe ÷ öğlen oranı (arketip başına ortanca)** | **%4,0 / %10,4** | **1,5 / 13,1 kW** |
   Yeni model yok; bir sütun. Ölçülü trafoda tepe zaten ölçülüyor. Yan bulgu: §5 yöntemiyle yan panelde çizilen eğrinin tepesi ~%16 düşük (ortalama gün eğrisi tek anın tepesini basık gösterir).
3. **Sınırlar:** (a) Tepe **Nisan 14 günün** tepesi; Kıbrıs'ın gerçek tepesi Temmuz akşamı (klima). Malta'nınki yıl tepesi [Yorum]. (b) Farazi şehirde Nisan'da gücünü aşan trafo **yok** (0/280) → "dolu trafoya yük için yer var" hatası bu veride ölçülemiyor. (c) Malta kVA, biz kW; güç katsayısı Kıb-Tek için BULAMADIM.

**Sorular:**
1. **Kapsam:** "Yük için boş kapasite" katmanı ürüne girsin mi (bu gece mi, yoksa sunumda "sıradaki katman" mı)? Yeni ADR gerekir mi (00-overview "hackathonda yalnız panel katmanı")?
2. **Sütun:** `sablon.py`'ye `tepe_kw` tahmini + P10/P90 (sözleşme 1.4) sen mi eklersin? Yöntem 3. yol mu; bant öğlen bandıyla aynı mı kurulur?
3. **Yaz:** Ekranda "Nisan" etiketiyle mi kalsın, yoksa senin üretici 1.3 çapasındaki "Nisan/yıl tepe oranı (EAC profillerinden)" ile yıl tepesine çevrilsin mi (sınanmamış olur)?
4. **Güneş sayısı:** Ekranda kW olarak hangisi: `kac_ev_orta` × 6,5 (benim önerim, rengiyle tutarlı) mı, pay sütunları mı? Pay sütunları da olasılıklı hesaba geçmeli mi?
5. **Birim:** kW mı gösterelim, yoksa kVA için cos φ varsayımı mı (kaynak yok)?
6. **Sınav:** Eklenirse `sinav.py faz2`'ye "tepe hatası" maddesi yazarım; eşik ne olsun (öğlendeki gibi ortanca ≤ %15, P90 ≤ %35 mi)? "Aşan trafoya yer var" ölçülemediği için bilgi satırı mı?
Dosya: src/sablon.py (senin), docs/data/tablo-bicimi.md (senin), src/sinav.py (Can), app/ (Civan, kart görünümü)
Neden: Can'ın isteği: harita Malta'nınki gibi her trafoda iki sayı göstersin; bugünkü model güneşe çok odaklı. Bloklamıyor.
Durum: karar verildi 21:04 → can.md (bu gece ürüne girmez; sunumda 'sıradaki katman'; tepe tahmini 3. yol sözleşme 1.4 adayı; güneş kW = kac_ev_orta × 6,5) + muhittin.md (sorular 5–6 Muhittin'e eklendi; Volkan iletir)


## UYARI! 31 Eki 21:20 — Civan'dan (+ Claude) — Eksik verilerimize uyan ada veri setleri: Kıbrıs AG iletken tablosu ve Korsika sağlaması
Ne: Veri sözlüğündeki BULAMADIM'lar için ada / Akdeniz açık verisi tarandı ([günlük](../log/2026-10-31-civan-ada-veri-setleri.md)). Bu geceki rakamları değiştirmez (karar masası 20:47 "yeni araştırma yok"); pilot ve üretici 1.3 için.
1. **Kıbrıs'ta gerçek AG hattı** [Kaynaklı: Kotsonias vd. (KIOS + EAC), ISGT-Europe 2019, Zenodo 10.5281/zenodo.3561929, CC BY 4.0]: havai iletken Rac 100 mm² 0,2702 / 50 mm² 0,5419 / 22 mm² 1,2271 / 16 mm² 1,9102 Ω/km; 49 bağlantı noktası, 61 tüketici, çoğu tek faz; nötr yalnız trafoda topraklı, nötr gerilimi tepede ~23 V. [Yorum] Ana hatta bizim ABC95 0,36 varsayımı karamsar; ama uç kollarda 16–22 mm² var, bizde yok → hat ucunu iyimser gösteriyor olabiliriz. EAC'nin, Kıb-Tek'in değil.
2. **Korsika** [Kaynaklı: EDF SEI Corse açık veri, Licence Ouverte 2.0]: 8.144 trafo, 5.930 km AG, 267.925 teslim noktası (2024). [Hesap] trafo başına 0,73 km ve 32,9 abone (Güney 1,02 / 34,4); Kuzey trafo sayısı vekili Korsika oranıyla ~6.690 → aralık **~6.400–6.700** (bugünkü vekil yalnız Güney'den).
3. Tek ev yüksek çözünürlük: Plegma (Yunanistan, 13 ev, 10 sn, klima dahil); bulut geçişi: NREL Oahu 1 sn ışınım (CC BY). İkisi de indirilmedi.
4. Ada AG gerilim ölçüsü açık değil: BULAMADIM (Gozo tezleri kısıtlı, KIOS–EAC izleme verisi yayımlanmamış; arama izi günlükte).
Sorular:
(a) Kotsonias tablosu üretici 1.3'e "ince uç kol (16–22 mm²)" senaryosu olarak girsin mi, yoksa yalnız uzmana soru 3'e not mu?
(b) Kuzey trafo sayısı vekili sözlükte "~6.400–6.700 (Güney + Korsika)" diye güncellensin mi; KAYNAK ve sözlük satırı kimde (Can mı)?
(c) Pilot veri isteği listesine iki kişi eklensin mi: KIOS yazarları (hat modeli + EAC 60 tüketici verisi) ve Micallef 2015 tezi "Request a copy" (Gozo dış sınamasının eksik hat boyu / kablosu)?
Dosya: docs/log/2026-10-31-civan-ada-veri-setleri.md; ham dosyalar depo dışında
Neden: Civan'ın isteği: eksik veriler için adalardan uyarlanabilir veri. Bloklamıyor.
Durum: karar verildi 21:16 → civan.md: (a) üretici 1.3 'ince uç kol' senaryosu evet (ROADMAP, BUILD) + uzmana soru 3 notu; (b) sözlük vekili sunum sonrası Can'a, ekran 6 rakamı bu gece değişmez; (c) dış veri istekleri listesine evet, gönderme Volkan

## KARAR 21:15 — BUILD'e: Muhittin'in üçüncü cevabı işlendi; sunum sonrası faz haritası (Volkan: "sarının düzelmesi lazım"); bu gece yalnız ROADMAP'e taslak
Karar: Cevap günlükte ([muhittin-cevap-3](../log/2026-10-31-muhittin-cevap-3-veri-dongusu.md)); [ADR-0013](../decisions/adr-0013-veri-dongusu-tuzugu.md) (veri döngüsü tüzüğü) ve [ADR-0014](../decisions/adr-0014-yuk-katmani-ayri-tepe-modeli.md) (yük katmanı) yazıldı. **Sunum sonrası faz haritası** (ROADMAP'e "Sunum sonrası" bölümü; Faz 6–11; sıra Muhittin'in uyarısıyla: ucuz olan değil, sarıyı ve yanlış kırmızıyı en çok düşüren önde):
- **Faz 6 — Tüzük ve döngü altyapısı** (ilk hafta): `docs/tuzuk.md` (ADR-0013'ün yedi maddesi + veri partisi görev kartı şablonu; Muhittin'in 3. maddesinin devamı gelince tamamlanır); hold-out defteri; sürümleme (model + üretici + veri + tohum); `src/kalibrasyon.py` (PIT histogramı, nominal–ampirik kapsama eğrisi, şişirme katsayısı). Bitti: tüzük var, her görev kartı ona referans veriyor, kalibrasyon betiği İspanya ve İngiltere artıklarında koşuyor.
- **Faz 7 — Kalibrasyon gerçeğe karşı** (İspanya yük, İngiltere gerilim, gelen inverter kayıtları): bantlar gerçek artıklarla şişirilir / model-sapma terimi; "fazla emin" düzeltilmeden bant yayınlanmaz. Bitti: nominal %80 gerçek doğrulamada %70–90; PIT düz.
- **Faz 8 — Kıb-Tek kayıtları ve başvuru-anı kararı** (sarıyı asıl düşüren): abone–trafo eşleşmesi, panelli abonenin adresi ve fazı, başvuru formuna hat / direk bilgisi (uzmana soru 2–4, 6–8); ADR-0012 başvuru-anı hesabı yazılır ve farazi şehirde "başvuru-anı yanlış evet oranı" ile sınanır. Bitti: Kıb-Tek'ten kayıt geldi ya da gelmeyeceği belli; başvuru-anı kararı farazide yanlış yeşil ≤ %2.
- **Faz 9 — Pilot A, ucuz ölçüm** (Faz 8'le paralel): akıllı priz gece seviyesi (birkaç ev), inverter kayıtları (izinle), trafo plakası ve kademe; her ölçülü trafo partisi ayar / doğrulama diye bölünür (ADR-0013 madde 1). Hedef: yanlış kırmızı %27 → ~%19 (plato; fazla satılmaz), yeşil kuralının ilk Kıbrıs geri-testi. Bitti: ≥ 1 parti işlendi, hold-out defteri açık, kapılar tutuyor.
- **Faz 10 — Yük katmanı** (ADR-0014): ayrı tepe modeli (sıcaklık + müşteri karışımı), hava normalizasyonu, kVA + pf varsayımı, iki sayılı kart asimetrik ("ön"); yaz ölçümü gelene kadar düşük güven. Bitti: kart var, yük tarafı "ön" etiketli, sınav maddesi (tepe hatası) bilgi satırı.
- **Faz 11 — Canlı geçiş kapısı:** dokunulmamış gerçek hold-out'ta ~150 bağımsız karar noktası, 0 ihlal (yanlış yeşil < %2, %95 güven), kalibrasyon toleransta, sürümlü yayın; sarı trafolarda geçici ölçüm cihazı (asıl pilot). Bitti: iki kapı geçildi, ilk sürüm Kıb-Tek'e teslim.
- Her fazda ölçü sözlük sırası: yanlış yeşil kapı → kalibrasyon kapı → sarı + yanlış kırmızı. "İyileşti" yalnız dokunulmamış veride.
Volkan'ın sorusuna cevap ("sarı düzelecek mi"): düzelir ama ölçümle değil kayıtla: gerilim ölçümü yanlış kırmızıyı düzeltir ve platoya oturur; sarıyı düşüren şey Kıb-Tek'in adres / faz kaydı + başvuru-anı kararı (Faz 8). Bu yüzden Faz 8 pilotla paralel ve önde.
Senden beklenen (BUILD): bu gece yalnız ROADMAP'e "Sunum sonrası (taslak, karar masası 21:15; Muhittin'in 3. maddesinin devamı ve 4. maddesi bekleniyor)" başlığı altında yukarıdaki altı satır (20 dk) + DEVIR satırı; `docs/tuzuk.md` ve kalibrasyon betiği sunumdan sonra. Konuşma notuna iki cümle Can'a yazıldı. Prova önde.
Durum: yapıldı 21:18 (BUILD) — ROADMAP sonunda "Sunum sonrası (taslak)": Faz 6–11, ölçü sırası, sarının kayıtla düzeleceği satırı ve dış veri istekleri (KIOS yazarları, Micallef 2015; civan.md 21:16 (c)); üretici 1.3'e ince uç kol (Kotsonias 2019; civan.md 21:16 (a)); 01-plan soru 3'e kesit notu; Faz 5'teki eski İngiltere cümlesi 5/6'ya; DEVIR açık iş 5.

## KARAR 21:20 — BUILD'e: Muhittin'in eksik iki parçası geldi; ADR-0015; tüzük içeriği; ROADMAP notu
Karar: 3. maddenin devamı ve 4. madde günlüğe eklendi (ek girdi 21:20). [ADR-0015](../decisions/adr-0015-basvuru-ani-motoru-durumlu-sari-sayi-konum.md): başvuru-anı motoru durumlu (taahhütlü bağlantıları sayar), haritayla aynı model, aynı < %2 kapısı; sarı düz renk değil sayı + konum ("hattın ilk %x'inde yeşil"); işletme kaldıraçları (kademe, faz dengeleme, volt-var) ayrı kategori, uzmana soru 10. **Tüzük içeriği** (`docs/tuzuk.md`, sunum sonrası Faz 6): ADR-0013'ün yedi maddesi + Muhittin'in şablonu: veri partisi görev kartı alanları (kimlik, kaynak, çekim tarihi, kapsam, veri sözleşmesi, **dondurulmuş kullanım bölünmesi**, hipotez, kapılar, sürüm ve ebeveyn); deney günlüğü (append-only, koşu başına satır, olumsuz sonuç dahil); ajan ayrımı (değişmezler direktif, parti görev kartı; model değişikliği ADR açar; **öneren ≠ puanlayan**); iki seviyeli bitti (parti bitti ≠ iyileşti; faz bitti = taze hold-out + kalibrasyon + plato).
Senden beklenen (BUILD): bu gece yalnız ROADMAP "Sunum sonrası" başlığındaki "(3. ve 4. madde bekleniyor)" notunu kaldır, Faz 8 satırına "ADR-0015" ekle (2 dk). Tüzük ve kalibrasyon betiği sunumdan sonra. Prova önde.
Durum: yapıldı 21:21 (BUILD) — ROADMAP "Sunum sonrası" başlığındaki bekleniyor notu kaldırıldı ("karar masası 21:15 ve 21:20"); bölüm dayanağına ve Faz 8 satırına ADR-0015; Faz 6 satırına tüzük içeriğinin yeri; DEVIR.

## UYARI! 31 Eki (21:21 sonrası) — Can'dan — kilit grafik yenilendi; Mac ↔ Windows bir trafo farkı
Ne: Karar masası 19:51'in istediği kilit grafik (docs/sunum/kilit_yanlis_yesil.png) yenilendi. Resmi koşumun dosyaları bende olmadığı için grafik Windows'ta aynı main'den 20 şehir sıfırdan üretilerek çizildi. Sol yarı resmi koşumla birebir: yanlış yeşil 0/87, %40 kuralı 41/284; yanlış kırmızı %27,3 (12/44), sarı %62,2, kaç ev orta 2 ev da aynı. Fark: dolu trafo **74** (resmi 73), bu yüzden sağ yarı "41/74" yazıyor; tavanlı 107 (resmi 108). Slayt 10 ve ekran 5'e etiket yazıldı; konuşmada resmi 41/73 söylenir. Bu `faz3` çıktısı günlüğe yazılmadı (19:51'e göre resmi koşum istenmiyor; yalnız grafik için). İsterseniz grafik Mac'te resmi veriden tek komutla birebir çizilir: `python3 src/grafikler.py faz3 data/synthetic docs/sunum --aralik 11-20` (dosya Can'ın; PNG'yi bana gönderin ya da onaylarsanız BUILD commit'lesin).
Dosya: docs/sunum/kilit_yanlis_yesil.png (Can)
Neden: Aynı tohumla Mac ve Windows bir trafoda farklı sonuç veriyor; prova notundaki "sunum bilgisayarında yeniden üretilirse tek tük trafo farklı çıkar" uyarısının ölçülmüş hâli. Bloklamıyor.
Durum: karar verildi 21:44 → can.md: PNG Mac'te resmi veriden çizildi ve karar masası commit etti (0/87 ↔ 41/284; dolu 41/73); Mac'te üç koşu birebir aynı, fark platform (Windows ↔ Mac), bilinen sorun

## UYARI! 31 Eki 21:24 — BUILD'den — Sunum sonrası faz haritası: Muhittin'e giden sıradaki "üreticiyi gerçeğe çapala, sınav şehirlerini yeniden üret" adımı Faz 6–11'de yok
Ne: Muhittin'e 20:52'de giden sıra dört adımdı: (1) trafo çıkış gerilimi; (2) her ölçülen trafoyla aralıkları yeniden ayarla; (3) deneme şehri üreticisini gerçek dağılımlara çapala ve sınav şehirlerini yeniden üret; (4) başvuru-anı kararını sına. Muhittin "sıra büyük ölçüde doğru" dedi, üç uyarı ekledi. ROADMAP "Sunum sonrası" Faz 6–11'de (1) Faz 9'da, (2) Faz 7'de, (4) Faz 8'de var. **(3) hiçbir fazda yok**; kalemleri yalnız ROADMAP Faz 3 "ikinci sürüm / üretici 1.3" listesinde duruyor, sıralı plana bağlı değil.
Muhittin'in tekniği bu adımı zaten şart koşuyor ama faz satırında adı geçmiyor:
- ADR-0013 madde 1: ayar payı "model + üretici"; doğrulama payı ve İspanya / İngiltere / pilot dokunulmaz. Sızıntı uyarısı tam bu adımla ilgili: aynı ölçüm hem modele hem üreticiye girerse sınav iyi görünür.
- ADR-0013 madde 6: ayar hedefi plato, yani gerçek ile üretilen dağılım arasındaki mesafe düzleşene kadar.
- ADR-0013 madde 4: hiyerarşik güncelleme (popülasyon dağılımı + ölçülen trafonun kendi değeri) ve periyodik, sürümlü yeniden-fit. Bu da hiçbir faz satırında adıyla yok.
Öneri (BUILD):
(a) Faz 7 ile 8 arasına bir satır: **"Üretici çapalama ve yeni sınav şehirleri (üretici 1.3)":**
   - ayar payıyla OG öğlen değişimi, panellerin hat üstündeki yeri, ince uç kol, trafo boyutu (Malta çapası), trafo içi çeşitlilik gerçek dağılımlara çapalanır;
   - hedef plato (ADR-0013 madde 6);
   - yeni sınav şehirleri yeni tohumla üretilir; eski sınav şehirleri ayar için kullanılmaz;
   - Faz 3 rakamları yeniden ölçülür, sürüm üçlüsüyle yazılır (madde 5).
   - Bitti: mesafe platoda, iki kapı yeni sınav şehirlerinde tutuyor.
(b) Faz 9 satırına "her partiden sonra hiyerarşik güncelleme ve sürümlü yeniden-fit (ADR-0013 madde 4)".
Numara: araya girerse Faz 8–11 kayar; ya "Faz 7b" ya yeniden numara, sizin kararınız.
Dosya: ROADMAP.md "Sunum sonrası" ve Faz 3 üretici 1.3 listesi (BUILD yazar); docs/istek/muhittin.md 20:52; docs/log/2026-10-31-muhittin-cevap-3-veri-dongusu.md
Neden: Volkan "fazlarda Muhittin'in dediği teknikle yapacağız" diyor; faz satırları tekniği adıyla anmazsa görev kartları ona referans vermez. Bloklamıyor; bu gece iş yok, prova önde.
Durum: karar verildi 21:25 → volkan.md (KARAR aşağıda): üretici çapalama yeni Faz 8, yeniden numara 6–12; hiyerarşik güncelleme pilot fazına

## KARAR 21:25 — BUILD'e: sunum sonrası haritaya eksik adım — üretici çapalama ve yeni sınav şehirleri; yeniden numara
Karar: (a) **Evet, ayrı faz; yeniden numara 6–12.** Yeni **Faz 8 — Üretici çapalama ve yeni sınav şehirleri (üretici 1.3)**: elde olan gerçek veriyle (İspanya yayılım / korelasyon, İngiltere OG değişimi ve panel yeri, Kotsonias ince uç kol, Malta kVA çapası, Faz 7 kalibrasyon artıkları) üretici gerçek dağılımlara çapalanır, hedef plato (ADR-0013 madde 6); **yeni tohumla yeni sınav şehirleri**, eskiler ayara girmez (madde 1); Faz 3 rakamları sürüm üçlüsüyle (model + üretici + veri + tohum) yeniden ölçülür ve günlüğe. Bitti: "gerçek – üretilen dağılım mesafesi" ölçülüp düzleşti, yeni sınav şehirlerinde iki kapı tutuyor. Sıra: 6 tüzük → 7 kalibrasyon gerçeğe karşı → **8 üretici çapalama** → 9 Kıb-Tek kayıtları + başvuru-anı (ADR-0012, 0015) → 10 pilot A ucuz ölçüm (8–9 ile paralel) → 11 yük katmanı (ADR-0014) → 12 canlı geçiş kapısı. (b) **Evet:** Faz 10 (pilot) satırına "her ölçülü partiden sonra hiyerarşik güncelleme ve sürümlü yeniden-fit (ADR-0013 madde 4); ayar payı hem modele hem üreticiye, doğrulama payı dokunulmaz" cümlesi; yani üretici çapalama Faz 8'de bir kez değil, her partide tekrarlanır.
Neden: Muhittin'in sızıntı uyarısı tam bu adım için; üretici gerçeğe göre düzelmeden ne kalibrasyon ne sınav rakamları güvenilir (S6 fazla eminlik). Faz 3'teki 1.3 listesi kalem listesi, plan değildi.
Senden beklenen (BUILD): ROADMAP "Sunum sonrası" bölümünde yeniden numara ve iki satır (5 dk); DEVIR. Bu gece kod yok; prova önde.
Durum: yapıldı 21:26 (BUILD) — ROADMAP "Sunum sonrası" 6–12: yeni Faz 8 üretici çapalama ve yeni sınav şehirleri; Faz 10 pilot satırına hiyerarşik güncelleme / sürümlü yeniden-fit / ayar payı modele + üreticiye cümlesi; "sarı kayıtla düzelir" satırı Faz 9; Faz 3 üretici 1.3 listesi Faz 8'e bağlandı; DEVIR. Not: ADR-0014 "Faz 10" (artık 11) ve ADR-0015 "Faz 8", "Faz 10" (artık 9 ve 11) eski numarayı anıyor; ADR'ler karar masasının, BUILD dokunmadı.

## KONTROL 21:29 — Civan'dan (+ Claude) — Faz 4 sınavı, Windows kısmı ve panel dili (civan.md KARAR 20:56)
Ne ölçüldü: main'deki `app/` (ada78f3 sonrası), Windows 11, Python 3.14.5, streamlit 1.66.1, pydeck 0.9.3.
- **+ Panel dili ve %40 sayısı yapıldı** (ada78f3): manşet "yaklaşık N ev (A–B)" + "%80 ihtimalle"; renk cümleleri 19:13'e göre; kural sayısı min(`kural40_ev`, aday), aşınca "panelsiz N evin hepsine izin veriyor (M evlik yer)"; "aralığımızın altında / içinde / üstünde"; sütun boyu `kac_ev_orta`. sehir-001 T30: "yaklaşık 13 ev (10–13)", "panelsiz 13 evin hepsine izin veriyor (23 evlik yer) — aralığımızın içinde" (BUILD'in örneğiyle aynı). 20 şehrin bütün trafolarında mantık koşuldu, hata yok.
- **+ Windows'ta 3 şehir:** renk sayıları Mac'le aynı (001: 13 / 22 / 5; 011: 15 / 25 / 0; 020: 13 / 27 / 0); 001 T30, T39 ve 011 T06'da yan panel açıldı.
- **+ Dışarıya istek yok:** OSM zemin dosyası varken sayfa 98 isteğin 98'ini localhost'tan aldı (Mac'le aynı).
- **+ README:** "Sunum bilgisayarı" satırı (zemin dosyası depoda yok, önceden indir).
- **? Açık:** ağ fiilen kapalıyken açılış ve 2 dakikalık ekran kaydı **ertelendi** (Civan: kontrol katmanı, sunum yerinde internet ve elektrik var; sonra yapılacak). ROADMAP Faz 4 kutuları senin dosyan; Windows maddesi işaretlenebilir.
Dosya: app/harita.py, app/README.md
Neden: KARAR 20:56 (4). Bloklamıyor.
Durum: karar verildi 21:44 → civan.md: Windows kutusu [x] (BUILD ROADMAP); ekran kaydı yarın sabah provada zorunlu (yedek), ağ kapalı test isteğe bağlı; animasyon (e85e21b) karara uygun, BUILD provada Mac'te açar

## KARAR 21:32 — BUILD'e: Faz 7 (kalibrasyon gerçeğe karşı) ŞİMDİ başlıyor; Volkan + Can paralel; Faz 6 tüzük de bu gece
Karar: Volkan (21:32): "sunuma daha var, Faz 7'ye başlayalım; Can ile benim aramda paylaştıralım, paralel yapıp test edelim." Sunum sonrası planı öne çekildi: **Faz 6 (belge) ve Faz 7 bu gece / yarın sabah**, Faz 8 sunum sonrası. Önce güvenlik: main'in bugünkü hâli `sunum-v1` etiketiyle işaretlenir (git tag, BUILD); Faz 7 kodu **dalda + PR** (model değişikliği, Can onayı); PR birleşmezse sunum v1 ile yapılır, hikâye değişmez.
**BUILD (Volkan) — model tarafı, sırayla:**
- B0 (30 dk) `docs/tuzuk.md`: ADR-0013'ün yedi maddesi + Muhittin'in şablonu (veri partisi görev kartı alanları; deney günlüğü append-only; öneren ≠ puanlayan; iki seviyeli bitti). Faz 7 kartları buna referans verir. `docs/gorev/` kartları: `volkan-faz7-kalibrasyon.md`, `can-faz7-kalibrasyon-sinav.md` (aşağıdaki içerikle).
- B1 (45 dk) `src/kalibrasyon.py`: girdi (tahmin, p10, p90, gerçek) satırları; çıktı PIT değerleri, nominal–ampirik kapsama eğrisi (50 / 80 / 90 / 95), **şişirme katsayısı k** (bir-dışarıda artıklarla: |artık| ÷ yarı bant genişliğinin %80 yüzdeliği; k = 1 ise kalibre) ve isteğe bağlı model-sapma terimi (artık dağılımından ek yayılım). Saf Python; her sayı kaynağıyla.
- B2 (60 dk) **Yük bandı İspanya'ya karşı:** `edp_test.py` faturalı (c) koşusunun bir-dışarıda artıklarından k_yük; `sablon.py`'de bant k_yük ile genişler (sözleşme değişmez; `sablon_ozet.json`'a `kalibrasyon: {kaynak: "EDP Oviedo 2018, 29 trafo, bir-dışarıda", k: …}`); İspanya'da kapsama önce / sonra (iç örnek, dürüstçe "ayarlandığı veride ölçüldü" etiketi), farazi 11–20'de kapsama ve kaç ev etkisi. **Ayar yalnız gerçek artıkla; farazi şehre bakarak k seçilmez.**
- B3 (60 dk) **Gerilim tarafı İngiltere'ye karşı:** 6 hattın model ÷ ölçülen dağılımından (ukpn_olasilik) model-sapma çarpanı s (çekiliş başına, ör. log-normal; parametreleri 6 hattın artıklarından) `kac_ev_olasilik.py`'nin gerilim yükselmesine girer; hedef 6 hatta P98 kapsaması 6/6 ama 6 hat az: s'nin aralığı günlüğe, "6 hatla ayarlandı, pilotta yeniden" etiketi. Sınav 11–20 **bir kez** yeniden (yeşil, yanlış yeşil, sarı, kaç ev bandı); beklenen: yeşil azalır, yanlış yeşil 0 kalır. Rakamlar Can'ın resmi koşumuyla teyit.
- B4 ROADMAP Faz 7 kutuları, Faz 7 günlüğü (`docs/log/2026-11-01-volkan-faz7-kalibrasyon.md`), DEVIR; PR açılır, Can onaylar, birleşince karar masası Mac'te koşar.
**Can — sınav ve gerçek veri tarafı (paralel, aynı anda başlar; can.md'de):** C1 kalibrasyon sınav maddeleri; C2 kapsama eğrisi grafiği önce / sonra; C3 hold-out defteri; C4 resmi koşumlar. Modeli yazan sınavı yazmaz: k'yi BUILD üretir, Can ölçer.
**Sınır:** Faz 7 sunumun hikâyesini değiştirmez, rakamları değiştirir; slayt 5 / ekran 4 rakamları ancak PR birleşip Can resmi koşunca güncellenir; o zamana kadar v1 rakamları. Civan'ın Faz 4 işleri önde kalır, Faz 7'de Civan'a iş yok.
Neden: Muhittin: "kalibrasyon gerçeğe karşı; %80 → 57 düzeltilmeden bant yayınlanmaz"; elimizde iki gerçek artık kaynağı zaten var (İspanya, İngiltere); kod küçük, sunuma zaman var (Volkan).
Senden beklenen (BUILD): `sunum-v1` etiketi → B0 → kartlar → B1–B3 dalda → PR. Takıldığında kutuya.
İlerleme 21:37 (karar masası): Volkan "görev kartlarını sen yap" dedi; aynı dakikada BUILD de yazmış (c90c98a): `docs/tuzuk.md`, `volkan-faz7-kalibrasyon.md`, `can-faz7-kalibrasyon-sinav.md` BUILD'in sürümüyle kaldı; karar masası `docs/gorev/civan-veri-arastirma.md` ekledi. `sunum-v1` etiketi BUILD'de (0db616e). BUILD B1'den devam eder. Civan: dashboard + sunum arkasında yeni veri arıyor, bulunca veri partisi olarak kutuya atar (kartı); modeli Volkan + Can iyileştirir.
Durum: yapıldı 21:46 (BUILD) — `sunum-v1` etiketi (0db616e); B0 tüzük ve iki kart (c90c98a, main); B1–B3 dalda, PR #16 (https://github.com/volkanGRGN/KKTC-hackathon/pull/16): k_yük 1,475, gerilim sapma s (μ 0,172, σ 0,414); sınav 11–20 bir kez. Dört eksi bulgu → UYARI 21:46 aşağıda, karar masası test eder; düzelmeden birleşmez.

## KARAR 21:39 — BUILD'e: "sunum sonrası" etiketi kalkıyor; Faz 6–12 ŞİMDİ başlayan plan; ertelenen Malta / Gozo / yük katmanı işleri fazlara geri alındı (Volkan)
Karar: Volkan (21:39): "Malta vs. için 'bu gece sunum var, olmaz' demişsin; fazlarda düzelt; sunuma daha var, modeli iyileştirmemiz ve dediklerimizi (Muhittin'inkileri de) uygulamamız lazım." Buna göre:
1. **ROADMAP:** "Sunum sonrası (taslak …)" başlığı → **"Faz 6–12 — Modeli gerçek veriyle iyileştirme (başladı 31 Ekim gece; sunum 1 Kasım bir kilometre taşı, `sunum-v1` yedek)"**. Satırlardaki "sunum sonrası", "bu gece yok", "pilot öncesi" ertelemeleri kaldırılır; her fazın "Kim / ne zaman" satırı şimdiki ekip: Volkan + Can model, Civan harita + veri.
2. **Geri alınan işler, yerleri:** (a) **Gozo hattı dış sınaması** → Faz 7'ye, İngiltere'nin yanına: hat boyu ve kablo aralıkla, "tek hat, gösterim" etiketiyle koşulur (BUILD, B3'ten sonra 30 dk); Micallef tezi "request a copy" isteğini Volkan gönderir (Civan metni hazırlar). (b) **Malta kVA çapası ve Kotsonias ince uç kol** → Faz 8 üretici çapalama (zaten orada; "sunum sonrası" ibaresi kalkar). (c) **Yük katmanı / iki sayılı kart (Faz 11)** → Can, Faz 7 kartının C1–C3'ü bitince başlar: sözleşme 1.4 PR'ı (`tepe_kva` + P10/P90 + `pf_varsayim`, "ön" etiketi), Can'ın 3. yolu başlangıç, ADR-0014 kuralları (kVA, pf 0,95 varsayım, asimetrik kart); Civan kartı Faz 4 bitince. (d) **Kuzey trafo sayısı vekili (Korsika)** → Civan sözlük satırını ve KAYNAK'ı yazar, Can onaylar; ekran 6 rakamı Can'ın koşumuyla güncellenir, "yarın" değil "hazır olunca". (e) **Faz 9 Kıb-Tek kayıtları:** sunumdan önce veri gelmez; ama **istek metni** (abone–trafo eşleşmesi, panelli abonenin adresi ve fazı, trafo başına fatura toplamı, hat kaydı) şimdi hazırlanır (BUILD taslak, Volkan gönderir) ve uzmana sorular 2–4, 6–10 kampta sorulur.
3. **Sıra (bu gece → yarın sabah):** Faz 7 (koşuyor) → Faz 8 üretici çapalama ve yeni sınav şehirleri (BUILD, PR; Can yeni şehirlerde sınav) → Faz 11 sözleşme 1.4 + tepe sütunu "ön" (Can) → Gozo dış sınaması (BUILD) → Faz 9 istek metni. Her adım dalda + PR; `sunum-v1` yedek; sunum metni PR'lar birleşip Can resmi koştukça güncellenir, hikâye aynı.
4. **Değişmeyen:** tüzük kapıları (yanlış yeşil ≤ %2, kalibrasyon) her PR'da; ayar farazi şehre göre yapılmaz; Civan'ın Faz 4 işleri (ağ kapalı açılış, ekran kaydı) ve prova ekipten düşmez.
Neden: Volkan'ın kararı; sunumun hikâyesi değişmiyor, yalnız rakamlar PR'larla güncelleniyor; ertelemeler karar masasının temkiniydi, Volkan kaldırdı.
Senden beklenen (BUILD): ROADMAP başlık ve ibareler (10 dk), DEVIR "Faz 6–12 başladı"; B1–B3 devam; sonra Gozo ve Faz 8. Kıb-Tek istek metni taslağı `docs/istek/kibtek-veri-istegi-taslak.md` (Volkan gönderir).
Durum: kısmen 21:46 (BUILD) — (1) ROADMAP başlığı "Faz 6–12 — Modeli gerçek veriyle iyileştirme", ertelemeler kalktı, Kim satırı, sıra; Gozo Faz 7'ye (dış sınama listesinde), Faz 9'a istek metni, Faz 11'e Can'ın sözleşme 1.4 işi; DEVIR "Faz 6–12 başladı". (2) Gozo dış sınaması yapıldı 21:53: PR #17, tutmadı (UYARI 21:53); (3) Kıb-Tek istek taslağı yapıldı 21:50: `docs/istek/kibtek-veri-istegi-taslak.md` (kişisel veri yok, anonim numara + trafo / hat / direk; 6 kalem; gönderen Volkan, kampta uzmanla kısalır); Faz 8, PR #16'nın bulguları kapanınca.

## BAŞLA 21:41 — Volkan: herkes kendi fazına başlasın (BUILD)
Ne: BUILD kartı [docs/gorev/volkan-faz7-kalibrasyon.md](../gorev/volkan-faz7-kalibrasyon.md): B1 `src/kalibrasyon.py` → B2 İspanya k_yük → B3 İngiltere model-sapma + sınav 11–20 bir kez → PR (Can onaylar). Sonra Gozo dış sınaması (30 dk), Faz 8 üretici çapalama ve yeni sınav şehirleri (dal + PR), Kıb-Tek veri istek taslağı. Önce ROADMAP başlık değişikliği (KARAR 21:4x, 10 dk). Can C1'den, Civan Faz 4'ün kalanından başlıyor; bildirim kutularda.
Durum: bilgi

## KARAR 21:44 — BUILD'e: Faz 4 Windows kutusu, ekran kaydı, animasyon kontrolü, Mac ↔ Windows farkı notu
Karar: (1) ROADMAP Faz 4 "Windows ve Mac'te çalıştı" [x] (Civan KONTROL 21:29 + BUILD 20:55); "internet kapalıyken açılıyor; ekran kaydı" kutusu: zemin dosyasıyla dışarıya istek yok (iki platformda ölçüldü), **ekran kaydı yarın sabah provada alınır** (Civan, yedek; sunum bilgisayarı çökerse PDF + kayıt), ağ fiilen kapalı deneme isteğe bağlı. (2) Civan'ın "noktalar çoğalıyor" geçişi main'de (e85e21b: ikinci sayfa, pop 0 → %115 → %100, ölçülen dolu / tahmin soluk halka, renkler, "gösterim" etiketi, Natural Earth kıyısı kamu malı); karar masası diff'i inceledi, 17:32 kararına uygun; **BUILD provada Mac'te açıp 3 → 5 geçişini dener** (2 dk), sorun varsa civan.md. (3) Kilit grafik: Can'ın isteğiyle karar masası Mac'te resmi veriden yeniden çizdi ve commit etti (`docs/sunum/kilit_yanlis_yesil.png`: 0/87 ↔ 41/284, dolu 41/73). Mac'te aynı tohumla üç koşu (biri PYTHONHASHSEED=0) birebir aynı: üretici Mac'te deterministik; fark Windows ↔ Mac (platform / sürüm), bir trafo. Tüzük madde 5'e not (BUILD, 2 satır): "resmi rakamlar karar masasının Mac koşumundan; başka platformda yeniden üretilen şehirler gösterim için, sınav için değil; sebep Faz 6'da aranır (Python 3.14 ↔ 3.12, kayan nokta)".
Senden beklenen (BUILD): ROADMAP Faz 4 iki kutu metni, tüzük notu (5 dk, B1'i bölme; B1 bitince); provada animasyon.
Durum: yapıldı 21:49 (BUILD) — ROADMAP Faz 4: "Windows ve Mac" [x], internet / ekran kaydı kutusu metni (iki platformda dışarıya istek yok; kayıt provada, Civan); tüzük madde 5'e platform notu. Animasyon 3 → 5 geçişi provada Mac'te denenecek.


## UYARI! 31 Eki 21:46 — Civan'dan (+ Claude) — Dış veri istek metinleri hazır, gönderen sensin (KARAR 21:39 madde 2)
Ne: `docs/istek/dis-veri-istekleri-taslak.md`: (1) Micallef 2015 tezi, Malta Üniv. OAR "Request a copy" formu (Gozo hat boyu, kablo, Srug F1); (2) KIOS yazarlarına e-posta (makaledeki AG hattın modeli, düğüm gerilimleri; EAC ~60 tüketici verisi yalnız anonim / toplu / gizlilik sözleşmesiyle). İkisi İngilizce, gönderilmeye hazır; köşeli parantezde senin imzan. Ham veriyi yayımlamama ve atıf sözü var.
Sorular: (a) Metinde "the northern part of Cyprus / Turkish Cypriot community" dili uygun mu? (b) KIOS'ta Kyriakides ve EAC'den Ioannou bilgi olarak eklensin mi?
Ayrıca: Korsika KAYNAK main'de (`data/raw/edf-sei-corse/KAYNAK.txt`); sözlük satırı Can'ın kutusunda (can.md 21:46).
Dosya: docs/istek/dis-veri-istekleri-taslak.md, data/raw/edf-sei-corse/KAYNAK.txt
Neden: KARAR 21:39. Bloklamıyor.
Durum: Volkan'a soruldu 21:51 (dışarıya mesaj Volkan'ın): (a) dil ve (b) bilgi alıcıları; karar masası önerisi aşağıdaki KARAR'da

## UYARI! 31 Eki 21:46 — BUILD'den — Faz 7 PR #16 hazır; dört eksi bulgu: test edin, düzelmeden birleşmez
Ne: Faz 7 model tarafı dalda (`kalibrasyon/faz7`), PR #16. Gerçek veride: İspanya %80 bant %65,7 → %79,1 (bir-dışarıda), %95 bant %81,3 → %90,3; İngiltere P98 5/6 → 6/6 (bir-dışarıda 6/6). Sınav 11–20 bir kez: yanlış yeşil 0/87 → 0/48 (GEÇTİ), kaç ev orta 2 → 1, kaç ev P10 altı %15 → %7. Ayrıntı ve komutlar: docs/log/2026-11-01-volkan-faz7-kalibrasyon.md (dalda).
Eksi bulgular (Volkan'ın kuralı: eksi bulgulu PR karar masasında test edilir; düzelmediyse beklenir, düzeldiyse birleşir):
1. **Faz 2 farazi kapsama maddesi kalıyor:** %87,5 → %96,4. Farazi şehir gerçekten düzgün; İspanya'ya göre genişleyen bant farazide fazla geniş. Soru: tüzük madde 3'e göre madde bilgi satırına mı insin (resmi ölçü İspanya, Can C1), yoksa Faz 8 (üretici çapalama) bitene kadar PR beklesin mi?
2. **Yeşil yarıya iniyor:** %25 → %14 (konut 1, köy 0). Yanlış kırmızı %27 → %33, sarı %62 → %69. Farazinin fiziği hesabınkiyle aynı, model hatası yok; gerçeğe göre eklenen sapma farazide yalnız temkin. Soru: bu bedel kabul mü?
3. **İspanya'da PIT düz değil:** 0,100 → 0,086 (hedef ≤ 0,05). Tek k genişliği düzeltiyor, şekli değil. Soru: Faz 7'nin kapısı mı (o zaman konformal / model-sapma ek iş), yoksa bilgi mi?
4. **Çift sayım olabilir:** `KOL_P` (1/6, Bancroft) ve s (Bancroft dahil) aynı 6 hattan. Soru: s varken `KOL_P` kalksın mı? Kalkarsa sınav 11–20 yeniden (bir kez).
Test için (Mac): dalı çek; `python3 src/kalibrasyon.py --deneme`; İspanya ve İngiltere komutları günlükte (ham veri: edp-ham, ukpn açık klasörü); `python3 src/sablon.py data/synthetic`, `python3 src/kac_ev_olasilik.py data/synthetic`, `python3 src/sinav.py faz2|faz3 data/synthetic --aralik 11-20`. Beklenen rakamlar yukarıda.
Dosya: PR #16 (src/kalibrasyon.py, src/sablon.py, src/kac_ev_olasilik.py, src/ukpn_olasilik.py, günlük, ROADMAP Faz 7, DEVIR, README)
Neden: KARAR 21:32 (B1–B3); tüzük madde 2 (iki kapı), madde 3 (kalibrasyon gerçeğe karşı). Bloklamıyor: BUILD beklerken Gozo dış sınamasını ve Kıb-Tek istek taslağını yapar; Faz 8 PR #16'dan sonra.
Durum: karar verildi 21:51 → volkan.md (KARAR aşağıda): (1) farazi kapsama bilgi satırı, kapı İspanya; (2) bedel kabul; (3) PIT toleransı n'ye bağlı, 29 trafoda 0,11 → geçer; (4) KOL_P kalır. Birleşme: karar masası Mac koşumu + Can'ın C1'i dalda

## UYARI! 31 Eki (21:41 sonrası) — Can'dan — Faz 7 C1 "önce" rakamları; resmi İspanya koşulu; validation.md tanım satırı
Ne: (1) `sinav.py faz2`'ye kalibrasyon maddeleri geldi (main'de; `--ispanya <edp_test.py --cikti CSV>`). **Önce** (main'deki model, gerçek veri — İspanya, girdi c, 10 ölçülü, **tabakalı**): nominal %50 / 80 / 90 / 95 → ampirik %46,1 / **%66,6** / %77,6 / **%83,4**; PIT en büyük sapma **0,108, fazla emin** (10. kova %21, 1. kova %13) → kapsama maddesi KALDI, PIT UYARI. Farazi 11–20 (bilgi): %60,7 / %87,9 / %93,9 / %96,8, PIT 0,046 fazla geniş — ters yön; farazide ayarlamak İspanya'yı daha emin yapar. (2) **Resmi koşul benim kararım:** c / 10 / tabakalı (ürünün girdisi ve seçimi). Rastgeleyle havuzlamıyorum: iki yol ters yönde yanılıyor, havuzda PIT 0,046 "geçer" görünüyor (rastgele 0,068 geniş, tabakalı 0,108 emin). k katsayın bu koşulda sınanacak; az ölçülüde (5) bant en kötü (c %57–59), k ölçülü sayısına bağlı olmalı [Yorum]. (3) `docs/method/validation.md`'ye (senin) tanım satırı, kartın istediği: "Kalibrasyon (Faz 7, ADR-0013 m. 3): bant log uzayında normal sayılır (orta = P10–P90 log ortası, σ = log genişlik ÷ 2,563); nominal %50 / 80 / 90 / 95 ↔ ampirik kapsama, madde %80 bant %70–90 ve %95 bant ≥ %90; PIT 10 kova, en büyük sapma ≤ 0,05, yön uç kovalardan; resmi ölçü gerçek veride (İspanya c / 10 / tabakalı), farazi bilgi."
Dosya: src/sinav.py (Can, yapıldı), docs/method/validation.md (senin), docs/log/2026-10-31-can-faz7.md, docs/log/holdout-defteri.md
Neden: Faz 7 kartı C1 ve 21:32 KARAR; PR'ın "sonra" rakamı aynı komutla ölçülecek. Bloklamıyor.
Durum: bekliyor

## KARAR 21:51 — BUILD'e: PR #16 (Faz 7) dört eksi bulgu; birleşme koşulu
Karar:
1. **Faz 2 farazi kapsama maddesi (%96,4) bilgi satırına iner; kapı İspanya.** Tüzük madde 3: kalibrasyon gerçeğe karşı. Farazi şehir gerçekten düzgün (üretici fazla düzgün, Muhittin); İspanya'ya göre genişleyen bant farazide fazla geniş çıkar, beklenen bu. ROADMAP Faz 2 kutusu: "[x] gerçek veride (İspanya, 29 trafo, bir-dışarıda) %80 bant %79; farazi 11–20'de %96 (bilgi; üretici Faz 8'de gerçeğe çapalanınca yeniden)". Can'ın C1'inde resmi kapsama maddesi İspanya satırı, farazi satır bilgi. PR Faz 8'i beklemez.
2. **Bedel kabul:** yeşil %25 → %14, yanlış kırmızı %27 → %33, sarı %62 → %69. Tüzük madde 2: önce iki kapı (yanlış yeşil 0/48 ✓, İspanya %79 ✓, İngiltere 6/6 ✓), işletme ölçüleri sonra. Fazla eminlikle bant yayınlamaktansa temkin (Muhittin, vurgu 2). Sunumda hikâye aynı; ekran 5 bedel cümlesi yeni rakamlarla ("sarı %69: aralıklar gerçeğe göre genişletildi; bilgi geldikçe düşer, Faz 9–10"); jüri cevabı "yeşil neden az": "İngiltere'nin 6 gerçek hattı modelimizin yükselmeyi ortalama %19 küçük gördüğünü söyledi; o payı ekledik." Not: σ 0,41 altı hattan moment tahmini, aralık 0,12–0,41; en temkinli uç değil, tahmin; pilot hatlarıyla yeniden (Faz 10). Günlüğe.
3. **PIT kapısının toleransı örnek büyüklüğüne bağlı:** tolerans = max(0,05; 2·√(0,09 ÷ n)). n = 29'da 0,11; İspanya 0,086 **geçer** (10 kovada beklenen 2,9 trafo; 0,05 ancak n ≥ ~150'de anlamlı, tüzük madde 6 ile tutarlı). Tüzük madde 2'ye formül (BUILD, 1 satır); Can'ın C1 (b) maddesi aynı formülle. Şekil düzeltmesi (konformal / model-sapma yük tarafı) Faz 10'da veri gelince.
4. **KOL_P kalır.** s, KOL_P'li modelin artıklarından tahmin edildi; KOL_P'yi kaldırıp s'yi yeniden fit etmek aynı 6 hattın aynı bilgisini s'ye taşır, kazanç yok, sınav yeniden koşulur. KOL_P fiziksel (yüksüz kol) ve pilotta hat kaydıyla ölçülebilir; s ise yapısal hata. Günlüğe "çift sayım riski temkin yönünde; Faz 10'da pilot hatlarıyla ayrıştırılır". Yeniden koşum yok.
**Birleşme koşulu:** (a) karar masasının Mac koşumu (dal, 20 şehir sıfırdan; İspanya ve İngiltere komutları) BUILD'in rakamlarıyla tutar; (b) Can C1'i dalda koşar ve onaylar (öneren ≠ puanlayan). İkisi olunca karar masası birleştirir (Volkan'ın "işi bittikten sonra birleştir" izni). Sonra Can resmi `faz2` / `faz3`, sunum rakamları v2.
**Civan'ın dış veri istek metinleri (21:46):** dışarıya mesaj Volkan'ın; öneri: (a) dil nötr ve teknik kalsın: "a low-voltage distribution network in the northern part of Cyprus (operator: Kıb-Tek)", siyasi niteleme yok; (b) ilk mesaj yalnız sorumlu yazara, EAC'den Ioannou ve KIOS'tan Kyriakides bilgi alıcısı **değil** (yazarın yönlendirmesiyle sonra). Volkan onaylarsa gönderir.
Senden beklenen (BUILD): PR'a dokunma; ROADMAP Faz 2 kutu metni, tüzük madde 2 formülü ve günlük notları (2, 4) PR dalına (küçük commit); Can'a dalda C1 için haber kutuda (21:46'da yazılmış).
İlerleme 21:55 (karar masası): İspanya Mac'te birebir (k 1,38–1,50 aralığı, %80 bir-dışarıda 0,791, PIT 0,100 → 0,086); İngiltere Mac'te birebir (5 → 6, bir-dışarıda 6/6, σ en az 0,12). Farazi 20 şehir koşumu sürüyor. Can'ın dalda C1 koşumu ve onayı bekleniyor.
İlerleme 21:56 (karar masası): farazi 11–20 Mac'te de tuttu: yanlış yeşil 0/48, yeşil 48 (%14), sarı %68,6, kaç ev orta 1, P10 altı %7,1, Faz 2 farazi kapsama %96,4 (bilgi); yanlış kırmızı 21/61 = %34,4 (BUILD 20/61, bir trafo farkı, bilinen). **Koşul (a) tamam; birleşme yalnız Can'ın dalda C1 koşumu ve onayına bakıyor.** BUILD Faz 8'e PR #16 dalının üstünde başlayabilir.
İlerleme 22:05 (karar masası): BUILD'in düzeltmesiyle (1fe042b) İspanya testi Mac'te yeniden: K_YUK'lu satırlarda k 1,000, %80 bant %80,0 / %95 %90,3 (iç örnek), bir-dışarıda %79,1. Can'ın C1 maddesi dalda `--ispanya` ile **GEÇTİ** (%82,1 / %92,6); PIT 0,066 Can'ın maddesinde hâlâ 0,05 eşiğiyle UYARI → n = 29 toleransı (0,11) girince geçer. **Kalan: Can PIT toleransını n'ye bağlar, dalda koşar, PR'ı onaylar → karar masası birleştirir.**
Durum: yapıldı 21:55 (BUILD) — PR #16 dalına 5711aeb (kod değişmedi): ROADMAP Faz 2 kapsama kutusu "kapı İspanya %79, farazi %96 bilgi"; Faz 7 satırları (PIT toleransı 0,11, 0,086 geçer; bedel kabul; KOL_P kalır); tüzük madde 2'ye tolerans formülü; günlüğe ek girdi (σ aralığı, çift sayım riski). Dal main ile birleşik (c1dd2c5). Birleşme: karar masası Mac koşumu + Can C1 onayı.

## UYARI! 31 Eki 21:53 — BUILD'den — Gozo dış sınaması (PR #17): tutmadı, bilgi eksik — test edin
Ne: KARAR 21:39 madde 2a. `src/gozo_dis_sinama.py` Srug F1 hattında (Graz 2016, Tablo 3) 400 çekiliş; hat boyu, kablo, faz, panel yeri aralıktan. Makalenin dört sonucunu birden tutan çekiliş **%0** (1/400). Tek tek, v1: bugün sorun yok %13, +1 kWp aşım %95, +1 kWp bir adım aşağı sorun yok %61, +2 kWp en alt kademe aşım %23. v2'de (Faz 7 s) %15 / %95 / %51 / %36.
Sebep iki bilinmeyen: (1) öğlen bara gerilimi: merkezler mevsimlik kademe ayarı istiyordu, "normal kademe = 250 V" öğlen doğru olmayabilir; 3 V payda bugünkü 26,7 kWp aşıyor. (2) Bugünkü panellerin dağılımı ve fazı. Hiçbir hat boyu / kablo dördünü birlikte tutturmuyor.
Ne söylenebilir: ne "doğrulandı" ne "yanlış" (20:47'deki "bilgi eksik, rakam üretmez" sezginiz doğru çıktı); Gozo'da da kaldıraç hat değil bara ve panel dağılımı. Micallef tezi gelirse tek tahminle yeniden.
Soru: PR #17 olumsuz sonuç olarak birleşsin mi (tüzük §3: olumsuz sonuçlar da yazılır; model kodu değişmiyor)? Sunumda söylenmez.
Dosya: PR #17 (https://github.com/volkanGRGN/KKTC-hackathon/pull/17): src/gozo_dis_sinama.py, docs/log/2026-11-01-volkan-faz7-gozo.md
Neden: Volkan'ın kuralı: eksi bulgulu PR karar masasında test edilir. Bloklamıyor; Faz 8 PR #16'dan sonra.
Durum: karar verildi 21:55 → olumsuz sonuç olarak BİRLEŞİR (tüzük §3: olumsuz sonuç da yazılır; model koduna dokunmuyor; günlük 'doğrulandı' demiyor). Birleştirmeyi karar masası denedi, izin sistemi incelemesiz birleştirmeyi reddetti; Volkan'ın açık 'birleştir' sözüyle yapılır.

## KARAR 21:58 — BUILD'e: PR #16'da bir tutarsızlık — Can'ın resmi İspanya maddesi k'yi görmüyor; edp_test.py de K_YUK uygulasın; PIT toleransında n = bağımsız trafo
Karar: Karar masası Can'ın C1 maddelerini dalda koştu (Mac, `--ispanya` ile): resmi İspanya maddesi **KALDI** gösteriyor (%80 bant %66,6, PIT 0,108) çünkü `edp_test.py --cikti` satırlarındaki alt / üst bant **K_YUK uygulanmadan** yazılıyor; k yalnız `sablon.py`'de ve `kalibrasyon.py`'nin kendi içinde. Yani sınav, kalibre edilmemiş modeli ölçüyor. Düzeltme (BUILD, dalda, 20 dk): (1) `edp_test.py` bandı `sablon.K_YUK` ile genişletir (tek kaynak: `from sablon import K_YUK` ya da ortak sabit), `--kalibrasyonsuz` anahtarı "önce" satırlarını üretir; `--cikti` dosyasına `k` sütunu ya da başlık notu. (2) Can'ın maddesi böylece iç örnek "sonra"yı ölçer (~%80 / %90; etiket "k aynı veriden, iç örnek; bir-dışarıda %79,1 kalibrasyon.py"). (3) **PIT toleransında n = bağımsız trafo sayısı (İspanya 29), satır sayısı değil:** `edp_satirlar.csv`'de 380 satır aynı 29 trafonun tekrarları; tolerans max(0,05; 2·√(0,09 ÷ 29)) = 0,11; tüzük madde 2 formülüne "n = bağımsız trafo / karar noktası sayısı" ibaresi. (4) Sonra karar masası `edp_test.py`'yi Mac'te yeniden koşar (2 dk) ve Can dalda `--ispanya` ile C1'i koşup onaylar; birleşme o zaman.
Neden: tüzük madde 3 ve 5 (sınav, sevk edilen modeli ölçer; k tek yerde); öneren ≠ puanlayan korunur (k'yi BUILD üretir, Can ölçer).
Senden beklenen (BUILD): (1) ve (3) dala; kutuya "hazır" satırı. Faz 8 başlangıcını bölme.
Durum: yapıldı 22:04 (BUILD) — PR #16 dalına 1fe042b: `edp_test.py` bandı `sablon.K_YUK` ile genişletir (tek kaynak), `--kalibrasyonsuz` önce için; tüzük madde 2 n = bağımsız trafo / karar noktası (İspanya 29); README ve günlük komutları. Sağlama Mac: kalibrasyonsuz k 1,475, %80 bant %65,7; varsayılan k 1,000, %80 bant %80,0, %95 %90,3, PIT 0,086 (tolerans 0,11). Can'ın İspanya maddesi bu satırlarla yeniden koşulmalı.

## UYARI! 31 Eki (21:55 sonrası) — Can'dan — PR #16 puanlandı, onay veriliyor; iki bilgi
Ne: C1 dalda koşuldu (Windows, 5711aeb; şehirlerin kopyası, sınav main'deki `sinav.py`). BUILD'in rakamları birebir: farazi %80 kapsama %96,4 (artık bilgi), `faz3` yanlış yeşil 0/48, yeşil / sarı / kırmızı 48 / 238 / 61, yanlış kırmızı 20/61, kaç ev orta 1, P10 altı %7,1 (dolu 74: bilinen platform farkı). Kapı (İspanya, c / 10 / tabakalı, bir-dışarıda k): %80 bant %66,6 → **%80,8**, %95 %83,4 → **%91,3**, PIT 0,108 → 0,058 → GEÇTİ. Puanlama olumlu; GitHub onayını Can kendi hesabından verecek (oturumdan gönderilemedi), gelene kadar birleşme koşulu (b) yarım. `sinav.py`'de 21:51 işlendi (farazi kapsama bilgi; PIT toleransı n = trafo sayısıyla).
Bilgi (PR'ı bloklamaz, günlükte): (1) **Tek k ortalamayı düzeltiyor, koşulu değil:** aynı k ile c / 10 / rastgele %92 / %99 (PIT 0,132 fazla geniş, toleransı aşıyor), c / 5 her iki yol %71–72 / %84 (hâlâ fazla emin). k'nın ölçülü sayısına ve seçime bağlı olması gerekir [Yorum]; Faz 10 / pilot adayı. (2) **PIT toleransı 29 trafoda ayırt etmiyor:** "önce" (0,108, açıkça fazla emin) de 0,113 ile geçiyor; bu gece kapıyı taşıyan kapsama maddesi. Hold-out defterine BUILD'in ayar bakışı (k, s) ve karar masasının 21:55 teyidi satır olarak eklendi (6, 7).
Dosya: PR #16 (onay), docs/log/2026-10-31-can-faz7.md, docs/log/holdout-defteri.md
Neden: KARAR 21:51 birleşme koşulu (b). Bloklamıyor.
Durum: bekliyor

## UYARI! 31 Eki 22:05 — BUILD'den — PR #16'da yeni eksi bulgu: k_yük ölçülü trafo sayısına bağlı; model n = 12, k 1,475 değil ~1,27
Ne: Faz 8 ayarında farazi kapsama hiç inmedi; sebebi aranırken bulundu. İspanya k'si `edp_test.py`'nin 5, 10 ve 15 ölçülü trafolu denemelerinin karışımından hesaplanmıştı. Ölçülü sayısına göre ayrı hesap (kalibrasyonsuz satırlar, `kalibrasyon.py`):
| Ölçülü | k | %80 bant önce | Bir-dışarıda kapsama, sonra |
|---|---|---|---|
| 5 | 1,93 | %58 | %79 |
| 10 | 1,21 | %73 | %78 |
| 15 | 1,33 | %69 | %78 |
| **10 + 15** | **1,27** | %71 | %79 |
| hepsi (PR #16) | 1,475 | %66 | %79 |
`sablon.py` her şehirde **12** ölçülü trafo kullanıyor (OLCULU_ANA). 5 ölçülüyle yüzdelikler kaba kestirilir ve bant dar çıkar; o satırlar k'yi şişiriyor. Farazide %96'lık kapsamanın bir kısmı buradan.
Öneri (BUILD): K_YUK = 1,27 (n 10 + 15, üretimdeki 12'ye en yakın; dürüst kapsama %78,6); günlüğe "k ölçülü sayısına bağlı; ölçülü sayısı değişirse k yeniden". Değişirse: `sablon.py` ve `edp_test.py` aynı sabitle (tek kaynak); sınav 11–20 bir kez daha (yeşil biraz artar, yanlış yeşil kapısı yeniden bakılır). İsterseniz ileride k(n) eğrisi.
Soru: K_YUK 1,27'ye insin mi, yoksa PR #16 1,475'le birleşip düzeltme Faz 8'de mi gelsin?
Dosya: PR #16 (src/sablon.py K_YUK); veri `edp_test.py --kalibrasyonsuz --cikti` (BUILD scratchpad); komut günlükte.
Neden: tüzük madde 3; Volkan'ın kuralı (eksi bulgu karar masasında). Bloklamıyor: BUILD Faz 8'e devam ediyor; PR #16'ya kendisi dokunmadı.
Durum: karar verildi 22:06 → volkan.md (KARAR aşağıda): K_YUK = 1,27, PR #16'da (Faz 8'e bırakılmaz); sınav 11–20 bir kez; karar masası Mac'te yeniden; Can C1 yeni dalda

## KARAR 22:06 — BUILD'e: K_YUK 1,475 → 1,27, PR #16'da; kalibrasyon işletme noktasında (12 ölçülü) ölçülür
Karar: **Evet, 1,27; PR #16'da, Faz 8'e kalmaz.** Gerekçe ilke, farazi kapsama değil: model her şehirde 12 ölçülü trafoyla çalışıyor (OLCULU_ANA); kalibrasyon katsayısı aynı işletme noktasındaki gerçek artıklardan gelmeli. 5 ölçülülü denemeler (k 1,93) başka bir modelin (az veriyle) hatasını ölçüyor; karışıma katmak katsayıyı şişirir. n = 10 ve 15'in birleşimi (k 1,27; dürüst kapsama %78,6) 12'ye en yakın kesit. Tüzük madde 3 "gerçeğe karşı" sağlanıyor, madde 5 için günlüğe k(n) tablosu (5 / 10 / 15 / 10+15 / hepsi) ve "k ölçülü sayısına bağlı; pilotta ölçülü sayısı değişirse yeniden" notu. `sablon.py` ve `edp_test.py` aynı sabit (tek kaynak). ADR-0013'e ek değil, günlük + tüzük madde 3'e bir cümle: "kalibrasyon, modelin sevk edildiği yapılandırmada (ölçülü sayısı, girdi seti) ölçülür".
Sıra: (1) dalda K_YUK = 1,27 + günlük tablosu + tüzük cümlesi; `kalibrasyon.py ispanya` ile n = 10 + 15 satırlarında k ≈ 1 ve bir-dışarıda kapsama; İngiltere değişmez; (2) sınav 11–20 **bir kez** (yeşil / yanlış yeşil / sarı / kaç ev bandı), günlüğe v2 → v2b satırı; (3) kutuya "hazır"; karar masası Mac'te yeniden koşar (farazi + İspanya); Can C1'i yeni dalda koşar, onaylar; birleşir.
Neden: Tüzük madde 3 ve 6 (hedef plato, doğru kesit); yanlış katsayıyı main'e sokup Faz 8'de düzeltmek iki kez rakam değiştirir.
Senden beklenen (BUILD): (1)–(3), 30 dk; Faz 8'i sonra sürdür.
Durum: bekliyor
