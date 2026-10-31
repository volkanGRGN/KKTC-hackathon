# Devir notu — şu an nerede kaldık

Bu dosya tek sayfa, anlık durum. Her faz sonunda ve iş devrederken Volkan (+ Claude) günceller; eski hali silinir, geçmiş [docs/log/](docs/log/) altında. Yeni gelen ya da yeni oturum: önce bunu, sonra [README](README.md) ve [Faz 0](docs/02-faz-0-ogrenim.md).

**Güncellendi:** 31 Ekim 2026, öğleden sonra

## Durum
- Fikir seçildi: trafo görünürlük haritası (MVP), güneş paneli ilk uygulama katmanı. Gerekçeler [docs/decisions/](docs/decisions/).
- **Faz 1 sürüyor.** Tablo biçimi sözleşmesi yazıldı, onay bekliyor ([PR #4](https://github.com/volkanGRGN/KKTC-hackathon/pull/4)). Faz 1 kartları main'de: [Can](docs/gorev/can-faz1-profiller-sinav.md), [Civan](docs/gorev/civan-faz1-ornek-veri-harita.md).
- Şehir üreticisi `src/sehir_uret.py` ilk sürüm `sehir/ilk-surum` dalında ([PR #6](https://github.com/volkanGRGN/KKTC-hackathon/pull/6)). 20 şehirde (yapay ışınımla) süre, tohum, tip sayıları ve gerilim maddeleri geçti; ama konut trafolarının %55'i bugünden 259 V üstü. Ayrıntı günlükte (`docs/log/2026-10-31-volkan-faz1.md`, PR #6 dalında).
- Veri adımı (Can): Lefkoşa ışınımı, EAC injection, SimBench ölçüleri alındı; Kıb-Tek şartnamesi BULAMADIM (varsayım etiketli). OSM Girne merkez (Civan).

## Açık faz ve kim nerede
- Volkan + Claude: PR #4 ve şehir üreticisi PR'ının birleşmesi; ardından Faz 2 (`src/sablon.py`).
- Can: `profiller.py` PR #5 (Volkan'ın bakışını bekliyor), sonra `src/sinav.py` Faz 1 bölümü ve Windows denemesi.
- Civan: `app/ornek_veri.py` + `app/harita.py` iskeleti, sahte şehirlerle (tohum 900–999).

## Bekleyen istekler
- Volkan'ın kutusunda (karar masası): Can'ın "pazar günü çarşı öğleni" eşiği; Claude'un Faz 1 parametre sorusu (panel yaygınlığı / trafo çıkış gerilimi aralığı). Can'ın kVA etiketi isteği yapıldı.
- Kontrol: `grep -n "Durum: bekliyor" docs/istek/*.md`

## Bilinen sorunlar ve kararlar
- Ham veri depoda yok; KAYNAK.txt adreslerinden indirilir. Şehir üreticisi EAC Excel'i ve `profiller.py` yoksa yer tutucu eğriye, Lefkoşa ışınım dosyası yoksa yapay ışınıma düşer ve bunu `ayar.json`'a yazar.
- Trafo çıkışı 246–250 V rastgele (şartname 250, belgesi yok).
- Sunum saati bilinmiyor; sıra var, saat yok.

## Sıradaki üç adım
1. PR #4'ü (sözleşme) Can ya da Civan onaylasın, birleşsin; ardından PR #5 (profiller, Volkan bakar) ve PR #6 (şehir üreticisi).
2. Karar masasının parametre kararından sonra Lefkoşa ışınım dosyasıyla 20 şehri yeniden üret (dosya Can'da; Volkan'ın Mac'inde yok); Can'ın `sinav.py faz1`'iyle geçme sınavı.
3. Faz 2 kartları ve `src/sablon.py`.
