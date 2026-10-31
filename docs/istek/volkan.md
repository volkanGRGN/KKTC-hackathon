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
Durum: bekliyor

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
