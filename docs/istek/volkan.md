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
Durum: bekliyor

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
Durum: bekliyor
