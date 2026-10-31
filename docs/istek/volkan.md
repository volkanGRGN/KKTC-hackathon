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
Durum: bekliyor
