# Sunum (Faz 5)

Klasör Can'ın ([CONTRIBUTING](../../CONTRIBUTING.md) sahiplik tablosu); hikâye ve dürüstlük cümleleri karar masasından ([ROADMAP](../../ROADMAP.md) Faz 5, volkan.md KARAR 17:00, [ADR-0008](../decisions/adr-0008-farazi-cesitlilik-saf-tahmin.md)). Volkan anlatır; 5–7 dakika.

| Dosya | Ne |
|---|---|
| [ekranlar.md](ekranlar.md) | **Sunumun kendisi** (Volkan 17:32): haritanın içinde 8 ekran (yük haritası öne, KARAR 10:16), her biri tek cümle + tek görsel + en fazla bir rakam; PDF yedeği bu metinden |
| [slaytlar.md](slaytlar.md) | Slayt listesi: her slaytta tek iddia, rakamlar ve etiketleri; itiraz ve kaynak slaydı dahil |
| [konusma-notu.md](konusma-notu.md) | Konuşma notu: dürüstlük cümleleri (söylenmesi zorunlu), jüri soruları ve cevap iskeleti |

**Kural:** slaytta her rakamın yanında kaynak ya da etiket ([Kaynaklı: adres] / [Hesap: günlük] / [Yorum]); ROADMAP Faz 5 sınavı "rakam sayısı = etiket sayısı". Farazi şehir rakamı her yerde "gösterim". Henüz gelmeyen rakam **BEKLİYOR** diye yazılır, tahmin edilmez.

**Durum (1 Kasım):** akış yük haritası öne (KARAR 10:16); rakamlar `dashboard/icerik.json` (yük: B-Y2, 41–50; panel: 31–40; üretici 1.5). Kilit grafik ([kilit_yanlis_yesil.png](kilit_yanlis_yesil.png)) 31–40 ile yeniden: `python src/kac_ev_olasilik.py <kök> --sehir N` (31…40), sonra `python src/grafikler.py faz3 <kök> docs/sunum/ --aralik 31-40` — 0/60, 24/46 (dashboard'la aynı). Canlı harita (Faz 4) bekleniyor. Yedekler (PDF, ekran kaydı) en son.
