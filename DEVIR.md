# Devir notu — şu an nerede kaldık

Bu dosya tek sayfa, anlık durum. Her faz sonunda ve iş devrederken Volkan (+ Claude) günceller; eski hali silinir, geçmiş [docs/log/](docs/log/) altında. Yeni gelen ya da yeni oturum: önce bunu, sonra [README](README.md) ve [Faz 0](docs/02-faz-0-ogrenim.md).

**Güncellendi:** 31 Ekim 2026, 17:42 (BUILD oturumu)

## Durum
- Fikir: trafo görünürlük haritası (MVP), güneş paneli ilk uygulama katmanı. Gerekçeler [docs/decisions/](docs/decisions/) (ADR-0001…0010).
- **Faz 1 bitti.** Altı madde geçti; gerilim eşiği 207 V (EN 50160). Dış çapa: İngiltere UKPN raporu ([Faz 1 günlüğü](docs/log/2026-10-31-volkan-faz1.md)).
- **Faz 2 bitti (faturalı).** Can'ın `sinav.py faz2`'si 7/7 GEÇTİ; bant simetrik yapıldı (kapsama %87,5, iki kuyruk %6). Faturasız model saf tahmini ortancada geçmiyor (bilgi satırı). 17:24'te main'e birleşti: #8 (şablon modeli + sözleşme 1.1), #12 (üretici ve sözleşme 1.2: mahalle farkı, yıllık fatura, bayramlar, kıyı, bara 244–252 V; model faturayı kullanır), #10 (İspanya EDP), #11 (İngiltere UKPN gerilim). Main'de: üretici birebir aynı şehri veriyor, `sinav.py faz1` 5/5.
  - Yeni şehir için: README'deki iki indirme, sonra `sehir_uret.py 1 20` ve `sablon.py data/synthetic`.
  - Sınav şehirleri 11–20 (geliştirme ölçümü, gösterim):
    - faturalı %3,9 / P90 %8,3;
    - faturasız %22 / %55, İspanya gerçek verisiyle aynı seviye.
  - Resmi ölçüm Can'ın `sinav.py faz2`'si ([PR #14](https://github.com/volkanGRGN/KKTC-hackathon/pull/14) birleşti 17:32; 11–20: %3,8 / %8,0, kapsama %84). Saf tahmin maddesi hâlâ eski Σ abone tanımıyla notlanıyor, düzeltme Can'da (can.md 17:32). Saf tahmin tanımı karar masası 17:26: tarife enerjisi / fatura; faturasız model ortancada geçmiyor (dürüstçe söylenir).
- **Faz 3 başladı.**
  - `src/kac_ev.py` [PR #13](https://github.com/volkanGRGN/KKTC-hackathon/pull/13)'te (artık main'e bağlı; Can'ın incelemesini bekliyor).
  - Sınav şehirleri 11–20: yanlış yeşil 0/21; %40 kuralı 41/284 (%14).
  - Kırmızı = karamsar senaryoda bugün aşıyor (karar masası 17:26): kırmızı %31, yanlış kırmızı %42, sarı %63. Hedef aşımının sebebi ±4 V bilinmeyen bara gerilimi; pilotun ilk ölçeceği şey.
  - Varsayım envanteri ([günlük](docs/log/2026-10-31-volkan-faz3-varsayimlar.md)): hiçbir ayar kırmızıyı düzeltmiyor, sıralama 0,75'te sabit; öğlen OG yükselmesi (+%0,8) UKPN'le çelişiyor.
  - Olasılıklı deneme [PR #15](https://github.com/volkanGRGN/KKTC-hackathon/pull/15): sınav 11–20'de yanlış yeşil 0/97 (yeşil %28), yanlış kırmızı %23, kaç ev hatası 2. Resmi hesap olup olmayacağı karar masasında.
  - Gerçek veride geri-test ([günlük](docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md)): İngiltere 6 hattın 5'inde ölçülen yükselme hesabın %98 sınırının altında, Bancroft'ta değil (kol yapısı). Yeşil kuralı gerçek veride doğrulanmış sayılmaz.
  - 18:43: hat boyu belirsizliği ve yüksüz panelli kol PR #15'e eklendi; sınav 11–20 yanlış yeşil 0/87, dolu trafonun kırmızı denen payı 32/74, kaç ev hatası 2.
- **Faz 5 başladı** (paralel). Hikâye "güven merdiveni", manşet İspanya %25 → %10 (ROADMAP Faz 5).

## Açık faz ve kim nerede
- **Volkan + Claude (BUILD):**
  - #8, #12, #10, #11 birleşti (17:24, Volkan'ın onayıyla). #13 Can'ın incelemesini bekliyor.
  - Konuşma notu taslağı hazır ([docs/konusma-notu-taslak.md](docs/konusma-notu-taslak.md)). #14 (Can'ın Faz 2 sınavı) incelendi ve birleşti; saf tahmin maddesinin düzeltmesi Can'da.
- **Can:**
  - PR #13 incelemesi (Faz 3; sözleşme §6 notları);
  - `sinav.py faz2` (saf tahmin satırıyla);
  - [Faz 3 kartı](docs/gorev/can-faz3-sinav-grafik.md): `sinav.py faz3` + kilit grafik;
  - `docs/sunum/` iskeleti.
- **Civan:** [Faz 3 kartı](docs/gorev/civan-faz3-yan-panel.md): yan panel `kac_ev.csv`; Faz 4 sınavı (internetsiz açılış, ekran kaydı, 3 şehir).

## Bekleyen istekler
- Volkan'da: sunum biçimi (Civan'ın "haritanın içinde 7 ekran" önerisi; karar masasının önerisi dashboard + aynı metinden PDF yedeği, animasyon yok).
- Kontrol: `grep -n "Durum: bekliyor" docs/istek/*.md`

## Bilinen sorunlar ve kararlar
- Ham veri depoda yok; KAYNAK.txt adreslerinden indirilir. Üretici 1.2 iki yeni dosya ister: kıyı (`osm-kasaba`) ve Open-Meteo 2023 (README).
- **Sanal ortam şart** (`pip install -r requirements.txt`). `openpyxl` yoksa üretici sessizce yer tutucu eğriye düşer; `ayar.json`'da `profil_kaynagi` = `eac` olduğuna bak.
- Model ve kaç ev ayarları yalnız şehir 1–10'da denendi; 11–20 sınav için ayrı, bir kez ölçüldü. Yeni denemede 11–20'ye bakarak ayar değiştirme.
- İspanya donuk sınav: üretici ve model İspanya hatasını düşürmek için ayarlanmaz (ADR-0009).
- Farazi faturalı isabet iyimser (aynı tarifede her abone aynı eğri); farazi isabet gerçeğin üst sınırı (ADR-0008).
- Sunum saati bilinmiyor; sıra var, saat yok.

## Sıradaki üç adım
1. Can #13'ü incelesin, birleşsin. Can `sinav.py faz2` ve `faz3`'ü koşsun; ROADMAP kutuları rakamla dolsun.
2. Can `faz3`'ü yeni kırmızı kuralıyla yeniden koşsun; ROADMAP Faz 3'te yanlış kırmızı, sarı ve kaç ev "KALDI, sebep günlükte".
3. Faz 5: konuşma notu taslağı hazır (BUILD), slayt iskeleti Can'da (83b0f11), gece 2 prova.
