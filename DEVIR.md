# Devir notu — şu an nerede kaldık

Bu dosya tek sayfa, anlık durum. Her faz sonunda ve iş devrederken Volkan (+ Claude) günceller; eski hali silinir, geçmiş [docs/log/](docs/log/) altında. Yeni gelen ya da yeni oturum: önce bunu, sonra [README](README.md) ve [Faz 0](docs/02-faz-0-ogrenim.md).

**Güncellendi:** 31 Ekim 2026, 19:45 — ilk BUILD oturumu doldu, yeni BUILD oturumuna devir.

## Durum
- Fikir: trafo görünürlük haritası (MVP), güneş paneli ilk uygulama katmanı. Gerekçeler [docs/decisions/](docs/decisions/) (ADR-0001…0011).
- **Faz 1 bitti.**
  - Altı madde geçti; gerilim eşiği 207 V (EN 50160).
  - Üretici 1.2: mahalle farkı, yıllık fatura, bayramlar, kıyı, bara 244–252 V.
  - Ayrıntı: [Faz 1](docs/log/2026-10-31-volkan-faz1.md), [üretici 1.2](docs/log/2026-10-31-volkan-uretici-1-2.md).
- **Faz 2 bitti (faturalı).** Can'ın `sinav.py faz2`'si, sınav şehirleri 11–20, 7/7 GEÇTİ:
  - hata %3,8 / P90 %8,0;
  - kapsama %87,5 (bant simetrik);
  - arketip %98.
  - Saf tahmin (fatura) %5,5 / %15,2 → model %31 / %48 iyi.
  - Faturasız model saf tahmini ortancada geçmiyor (bilgi).
  - Gerçek veri: İspanya %25 → faturayla %10.
- **Faz 3: resmi hesap olasılıklı** ([ADR-0011](docs/decisions/adr-0011-faz3-olasilikli-hesap.md)). `src/kac_ev_olasilik.py` main'de ([PR #15](https://github.com/volkanGRGN/KKTC-hackathon/pull/15) birleşti 19:37). `kac_ev.csv` sözleşme 1.3: §6 + `p_bugun_asar`, `p_iki_ev_sigar`, `kac_ev_orta`. Tek denklem `kac_ev.py` yedek ve pay sütunlarının kaynağı.
  - Can'ın `faz3`'ü PR #15 dalındaki dosyalarla, sınav 11–20:
    - yanlış yeşil 0/87 GEÇTİ;
    - %40 kuralı 41/284 (%14);
    - kaç ev GEÇTİ (karamsar 2, orta 2);
    - yanlış kırmızı %27 ve sarı %62 UYARI.
  - **Resmi koşu main'de bir kez daha yapılacak (Can).** ROADMAP Faz 3 kutuları onunla dolacak.
  - Dil (karar masası 19:13): karamsar–iyimser %80 bant, "en az" değil; manşet "yaklaşık N ev (A–B)"; vaat renkte.
  - Günlükler:
    - [tek denklem](docs/log/2026-10-31-volkan-faz3.md);
    - [varsayım envanteri](docs/log/2026-10-31-volkan-faz3-varsayimlar.md): hiçbir ayar kırmızıyı düzeltmiyor; öğlen OG +%0,8 UKPN'le çelişiyor;
    - [olasılıklı](docs/log/2026-10-31-volkan-faz3-olasilik.md);
    - [İngiltere geri-testi](docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md): 6 hattın 5'i kapsandı, Bancroft kaçtı; yeşil bütçesi gerçek veride doğrulanmadı.
- **Faz 4** (Civan): harita ve yan panel Faz 3 tablosuna bağlı. Açık: internetsiz açılış, 2 dk ekran kaydı, 20 şehirde kontrol.
- **Faz 5** (paralel): `docs/sunum/` (Can) ve [konuşma notu taslağı](docs/konusma-notu-taslak.md) (BUILD). Hikâye "güven merdiveni"; dashboard içinde 7 ekran (Volkan 17:32). Ekran 5 rakamları Can'ın main'deki `faz3` koşusuyla. 2 prova yapılmadı.

## Açık işler (yeni BUILD oturumu buradan başlar)
1. **Faz 3 eksik listesi karar masasında** (19:44'te gönderildi, cevap volkan.md'ye gelecek):
   - yanlış kırmızı %27 (hedef ≤ %20);
   - sarı %62 (hedef ≤ %30);
   - yeşil bütçesi gerçek veride doğrulanmadı (İngiltere 5/6);
   - olasılık düşük uçta iyimser (%10–30 kovası → %43);
   - kaç ev aralığı taban değil (P10 altı %15);
   - faturasız ortancada geçmiyor.
2. **BUILD'in iki önerisi, karar masası onayı bekliyor:**
   - (a) Bilginin değeri denemesi: bara gerilimi / panelli evlerin adresi / faz bilinseydi yanlış kırmızı ve sarı ne kadar düşer. Yalnız şehir 1–10'da, sonra 11–20 bir kez.
   - (b) Yeşil eşiği tablosu: 0,98 / 0,95 / 0,90 için yeşil, sarı, yanlış yeşil.
3. **Can:**
   - main'de `sinav.py faz3` bir kez;
   - ekran 5 rakamları;
   - ASTOR kataloğu KAYNAK ve sözlük satırı (can.md 19:26).
   - Sonra BUILD ROADMAP Faz 3 kutularını doldurur: yanlış yeşil ve kaç ev GEÇTİ; yanlış kırmızı ve sarı "KALDI, sebep günlükte".
4. Uzmana sorulacaklar güncel: [plan](docs/01-plan.md) soru 2–8 (abone–trafo eşleşmesi, hat kaydı, faz, panelli abone, çekilen/verilen kaydı, trafo plakası ve kademe).

## Bilinen sorunlar ve kararlar
- Ham veri depoda yok; KAYNAK.txt adreslerinden indirilir. Üretici 1.2 iki yeni dosya ister: kıyı (`osm-kasaba`) ve Open-Meteo 2023 (README).
- **Sanal ortam şart** (`pip install -r requirements.txt`). `openpyxl` yoksa üretici sessizce yer tutucu eğriye düşer; `ayar.json`'da `profil_kaynagi` = `eac` olduğuna bak.
- **Ayar disiplini:**
  - Model ve kaç ev ayarları yalnız şehir 1–10'da. 11–20 sınav, her yöntem değişikliğinden sonra bir kez ölçülür.
  - İspanya donuk sınav (ADR-0009).
  - Sınav şehirleri bu gece donuk: üretici değişmez (K2 OG düzeltmesi üretici 1.3'te).
- **Birleştirme:**
  - BUILD'in `gh pr merge`'ü izin sisteminde durabiliyor.
  - Volkan'ın sohbette açık "birleştir" demesi gerekiyor; "Can onaylasın" yetmedi.
  - Sözleşme değişikliği Can ya da Civan onayı ister.
- Farazi isabet gerçeğin üst sınırı (ADR-0008); farazi faturalı iyimser.
- Sunum saati bilinmiyor; sıra var, saat yok.

## Sıradaki üç adım
1. Karar masasının Faz 3 eksik listesi cevabını uygula (volkan.md). Onay gelirse (a) bilginin değeri, (b) yeşil eşiği tablosu.
2. Can'ın main'deki `faz3` koşusundan sonra ROADMAP Faz 3 kutuları ve ekran 5.
3. Faz 5: konuşma notu taslağını Can'ın `docs/sunum/`'u ile birleştirmek; gece 2 prova.
