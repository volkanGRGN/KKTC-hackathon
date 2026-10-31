# Devir notu — şu an nerede kaldık

Bu dosya tek sayfa, anlık durum. Her faz sonunda ve iş devrederken Volkan (+ Claude) günceller; eski hali silinir, geçmiş [docs/log/](docs/log/) altında. Yeni gelen ya da yeni oturum: önce bunu, sonra [README](README.md) ve [Faz 0](docs/02-faz-0-ogrenim.md).

**Güncellendi:** 31 Ekim 2026, 17:20 (BUILD oturumu)

## Durum
- Fikir: trafo görünürlük haritası (MVP), güneş paneli ilk uygulama katmanı. Gerekçeler [docs/decisions/](docs/decisions/) (ADR-0001…0010).
- **Faz 1 bitti.** Altı madde geçti; gerilim eşiği 207 V (EN 50160). Dış çapa: İngiltere UKPN raporu ([Faz 1 günlüğü](docs/log/2026-10-31-volkan-faz1.md)).
- **Faz 2 kapanıyor.** Değişiklik istekleri birbirine bağlı: #8 → #12 → #13.
  - [PR #8](https://github.com/volkanGRGN/KKTC-hackathon/pull/8): şablon modeli + sözleşme 1.1.
  - [PR #12](https://github.com/volkanGRGN/KKTC-hackathon/pull/12): üretici ve sözleşme 1.2 (mahalle farkı, yıllık fatura, bayramlar, kıyı, bara 244–252 V); model faturayı kullanır.
  - Sınav şehirleri 11–20 (geliştirme ölçümü, gösterim):
    - faturalı %3,9 / P90 %8,3;
    - faturasız %22 / %55, İspanya gerçek verisiyle aynı seviye.
  - Resmi ölçüm Can'ın `sinav.py faz2`'si.
- **Faz 3 başladı.**
  - `src/kac_ev.py` [PR #13](https://github.com/volkanGRGN/KKTC-hackathon/pull/13)'te.
  - Sınav şehirleri 11–20: yanlış yeşil 0/21; %40 kuralı 41/284 (%14).
  - Kırmızı kuralının okuması karar masasında.
- **Faz 5 başladı** (paralel). Hikâye "güven merdiveni", manşet İspanya %25 → %10 (ROADMAP Faz 5).

## Açık faz ve kim nerede
- **Volkan + Claude (BUILD):**
  - #8 / #12 / #13 Can'ın onayını bekliyor (Volkan 17:06: "Can'ı ve bağımlı PR'ları bekleriz").
  - #10 (EDP) ve #11 (UKPN) bağımsız; birleştirmek Volkan'da, BUILD'in izni yok.
  - Sırada: konuşma notu taslağı; karar masası kırmızı kuralını seçince `KIRMIZI_KURALI`.
- **Can:**
  - PR #8 / #12 sözleşme onayı;
  - `sinav.py faz2` (saf tahmin satırıyla);
  - [Faz 3 kartı](docs/gorev/can-faz3-sinav-grafik.md): `sinav.py faz3` + kilit grafik;
  - `docs/sunum/` iskeleti.
- **Civan:** [Faz 3 kartı](docs/gorev/civan-faz3-yan-panel.md): yan panel `kac_ev.csv`; Faz 4 sınavı (internetsiz açılış, ekran kaydı, 3 şehir).

## Bekleyen istekler
- Karar masasında (volkan.md):
  - Faz 3 kırmızı kuralı okuması (17:17);
  - saf tahmin tanımı, panelli evin faturası, üretici 1.3 (17:03);
  - Civan'ın sunum-dashboard önerisi (17:11).
- Kontrol: `grep -n "Durum: bekliyor" docs/istek/*.md`

## Bilinen sorunlar ve kararlar
- Ham veri depoda yok; KAYNAK.txt adreslerinden indirilir. Üretici 1.2 iki yeni dosya ister: kıyı (`osm-kasaba`) ve Open-Meteo 2023 (README).
- **Sanal ortam şart** (`pip install -r requirements.txt`). `openpyxl` yoksa üretici sessizce yer tutucu eğriye düşer; `ayar.json`'da `profil_kaynagi` = `eac` olduğuna bak.
- Model ve kaç ev ayarları yalnız şehir 1–10'da denendi; 11–20 sınav için ayrı, bir kez ölçüldü. Yeni denemede 11–20'ye bakarak ayar değiştirme.
- İspanya donuk sınav: üretici ve model İspanya hatasını düşürmek için ayarlanmaz (ADR-0009).
- Farazi faturalı isabet iyimser (aynı tarifede her abone aynı eğri); farazi isabet gerçeğin üst sınırı (ADR-0008).
- Sunum saati bilinmiyor; sıra var, saat yok.

## Sıradaki üç adım
1. Can onaylasın: #8 → #12 → #13 sırayla birleşsin. Can `sinav.py faz2` ve `faz3`'ü koşsun; ROADMAP kutuları rakamla dolsun.
2. Karar masası kırmızı kuralını seçsin. BUILD tek satırı değiştirir, `kac_ev.csv` yeniden üretilir.
3. Faz 5: konuşma notu taslağı (BUILD), slayt iskeleti (Can), gece 2 prova.
