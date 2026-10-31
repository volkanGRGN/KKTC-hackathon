# Devir notu — şu an nerede kaldık

Bu dosya tek sayfa, anlık durum. Her faz sonunda ve iş devrederken Volkan (+ Claude) günceller; eski hali silinir, geçmiş [docs/log/](docs/log/) altında. Yeni gelen ya da yeni oturum: önce bunu, sonra [README](README.md) ve [Faz 0](docs/02-faz-0-ogrenim.md).

**Güncellendi:** 31 Ekim 2026, öğlen

## Durum
- Fikir seçildi: trafo görünürlük haritası (MVP), güneş paneli ilk uygulama katmanı. Gerekçeler [docs/decisions/](docs/decisions/).
- Faz 0 (öğrenim) yazıldı; ekip çalışıyor.
- Yol haritası, kurallar, görev kartı düzeni ve istek kutuları kuruldu.
- Kod: yalnız eski benzetim var (`src/trafo_bos_kapasite.py`); şehir üreticisi, model, kaç ev, harita henüz yok.

## Açık faz ve kim nerede
- Sıradaki: tablo biçimi sözleşmesi (`docs/data/tablo-bicimi.md`) → Faz 1 kartları.
- Volkan + Claude: sözleşme, sonra `src/sehir_uret.py`.
- Can: Faz 0; kart gelince `src/profiller.py` + veri adımı.
- Civan: Faz 0; kart gelince `app/ornek_veri.py` + `app/harita.py` iskeleti.

## Bekleyen istekler
- Yok. (Kontrol: `grep -n "Durum: bekliyor" docs/istek/*.md`)

## Bilinen sorunlar ve kararlar
- Ham EAC verisi depoda yok; `data/raw/eac-profil-siniflari/KAYNAK.txt` adresinden indirilir. 5. sayfa adı yanlış, otel sınıfı.
- Benzetimde trafo çıkışı 246–247 V (şartname 250); Faz 1'de 246–250 rastgele olacak.
- Sunum saati bilinmiyor; sıra var, saat yok.

## Sıradaki üç adım
1. Tablo biçimi sözleşmesi.
2. Can ve Civan'a Faz 1 kartları.
3. Şehir üreticisi.
