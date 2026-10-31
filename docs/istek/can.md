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
Durum: bekliyor

## PR İNCELEME 31 Eki 12:25 — PR #5 "veri: profiller.py ilk sürüm (EAC sınıf eğrileri, 5 dk, sağlama)"
Sonuç: sağlama eşiği düzeltilince birleştirilebilir (yukarıdaki ilk KARAR).
+ İmzalar ve adlar kartla birebir: `oku(yol=XLSX)`, `sinif_egrisi(veri, sinif, ay, gun)`, 7 sınıf adı; 7 tip adı sözleşmedeki `tip` değerleriyle aynı; TIPLER notu ve enerji sağlaması eklendi; her `open()` utf-8, yollar pathlib; önbellek `data/raw/` altında ve .gitignore tutuyor; yalnız kendi dosyaların; main'le çakışma yok (MERGEABLE / CLEAN).
+ Mac'te çalıştırdım (Python 3.13, openpyxl 3.1.5): beş rakam Windows'takiyle birebir (0,71 · 11:15 · 3,96 · 1,00 · 0,83); Excel'den soğuk okuma 0,1 s (tipik gün bloğundan sonra duruyor), önbellekten 0,03 s. Kartın "Mac ve Windows'ta" maddesi sağlandı; günlüğüne "Mac: karar masası doğruladı 12:25" yazabilirsin.
− `saglama()` son maddesi: ad ve aralık KARAR'daki gibi değişmeli (src/profiller.py, `saglama()` içindeki son `sonuc.append`). Şu an çıkış kodu 1; kartın "5 sağlama GEÇTİ" denemesi bu yüzden geçmiyor.
− Günlükteki tabloya yeni sonuç satırı (append-only; eski satır kalır).
? Windows'ta çıktı ve Türkçe karakter: sen çalıştırdın, bende ölçülmedi. 14 "tamamen sıfır" sınıf-günün hepsi `isi_depolama` (kullanmadığımız sınıf) [Hesap]; sorun değil, günlüğe bir kelime yeter.
Senden beklenen: iki düzeltmeyi dala gönder, sonra kartın dediği gibi sen birleştir (Volkan'ın bakması = bu inceleme).
Durum: bekliyor
