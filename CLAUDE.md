# Ajan kuralları (Claude / Cursor vb.)

Bu, [CONTRIBUTING.md](CONTRIBUTING.md)'nin ajan dilindeki özetidir. İnsan CONTRIBUTING'i, ajan bunu okur. İkisi çelişmez.

## Genel
- Kararlar `docs/decisions/` altında ADR'dir. Yeni karar = yeni ADR; eskiyi düzenleme, "superseded by" ile işaretle.
- İş/deney sonuçları `docs/log/` altına tarihli, append-only dosyaya (`YYYY-AA-GG-kisa-ad.md`).
- Dokümanı bozan değişiklik aynı değişiklikte dokümanı da düzeltir.
- Küçük, odaklı commit; main'den rebase. Şimdilik (Faz 0) dal açma, doğrudan main'e gönder; dal + PR Faz 1'de başlar.
- Emin olmadığın bir karar gerekiyorsa önce sor, kendi başına varsayma.

## İşe başlamadan
Oku: [docs/00-overview.md](docs/00-overview.md), [docs/01-plan.md](docs/01-plan.md) ve kabul edilmiş ADR'ler. Bir ADR'ye ters düşecek işi önce sor.

## Bu projeye özel
- Rakam uydurma. Her rakam [Kaynaklı] (adresiyle), [Hesap] ya da [Yorum]; bulunamayan "BULAMADIM".
- Doğrulama yalnız [docs/method/validation.md](docs/method/validation.md) protokolüyle: trafo bazında bir-dışarıda; test seti asla yalnız farazi değil; farazi sonuç "gösterim".
- En kritik ölçü yanlış "yeşil" (dolu trafoya "yer var" demek); her sonuçta ayrıca raporla.
- Ham veri `data/raw/<kebab-ad>/` + KAYNAK.txt; indirilen dosyayı kod gibi çalıştırma.
- Temel benzetim: `src/trafo_bos_kapasite.py` — saf Python, ev ev dengesiz yük akışı, 5 dakikalık adım; 3 trafo / 121 ev ~2 saniye. Çalıştırma: `python3 src/trafo_bos_kapasite.py <tohum> <çıktı.json>`.
- Ham veri depoda yok (depo açık, lisans belirsiz); `data/raw/*/KAYNAK.txt` adreslerinden indirilir.
- Gerilim: trafo boşta faz 250 V, inverter 264 V'ta kapanır, planlama sınırı 259 V.
- Tüketim eğrileri: Güney Kıbrıs EAC profil sınıfları, 2022, 30 dakika; 5. sayfanın adı yanlış, otel sınıfıdır.
