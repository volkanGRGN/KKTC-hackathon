# Volkan için istekler

Burası Volkan'ın kutusu; yalnız o işler. Kalıp için [README](README.md).

## UYARI! 31 Eki 13:40 — Can'dan — Faz 1 sağlama eşiği: "pazar günü çarşı öğleni"
Ne: ROADMAP Faz 1 "pazar günü çarşı öğleni iş gününün yarısından az" sağlaması EAC verisiyle kalıyor: çarşı Nisan tatil/iş günü öğleni (11–14) 0,83. Eşik mi değişmeli, yoksa bu madde sağlamadan çıkıp şehir üreticisinde varsayım mı olmalı? Değer ayarlanmadı.
Dosya: ROADMAP.md (Faz 1 geçme sınavı), src/profiller.py `saglama()`
Neden: EAC'nin tam yıl serisi iki tipik günün tekrarı (cumartesi = pazar = bayram); pazar ayrı bilgi yok. Tatil/iş günü öğleni Nisan: küçük ticari 0,84, büyük ticari 0,77, küçük sanayi 0,75; küçük ticari diğer aylarda 0,68–0,84. Rakamlar: docs/log/2026-10-31-can-faz1.md. PR: https://github.com/volkanGRGN/KKTC-hackathon/pull/5
Durum: bekliyor

## UYARI! 31 Eki 13:55 — Can'dan — sözleşmede kVA etiketi "Kaynaklı"
Ne: `docs/data/tablo-bicimi.md` (PR #4) §1 `trafolar.csv` `kva` satırında "direk 25/50/100/250/400 [Kaynaklı: Kıb-Tek şartnamesi, veri sözlüğü]" yazıyor. Senin kararınla şartname "kaynak bağlantısı yok, doğrulanmadı"; veri sözlüğü buna göre güncellendi. Etiket "[varsayım: Kıb-Tek şartnamesi, kaynak bağlantısı yok]" olmalı.
Dosya: docs/data/tablo-bicimi.md
Neden: kaynaksız rakam "kaynaklı" görünmesin (CLAUDE.md, veri etiketleri). Arama izi: docs/log/2026-10-31-can-faz1-veri.md.
Durum: bekliyor
