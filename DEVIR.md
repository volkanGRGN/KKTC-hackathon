# Devir notu — şu an nerede kaldık

Bu dosya tek sayfa, anlık durum. Her faz sonunda ve iş devrederken Volkan (+ Claude) günceller; eski hali silinir, geçmiş [docs/log/](docs/log/) altında. Yeni gelen ya da yeni oturum: önce bunu, sonra [README](README.md) ve [Faz 0](docs/02-faz-0-ogrenim.md).

**Güncellendi:** 31 Ekim 2026, 20:45 — Faz 3 kapandı (Volkan 19:51); bilginin değeri denemesi; ada ülkeleri taraması.

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
- **Faz 3 bitti (31 Ekim 19:51, gösterim; açık eksikler pilotta).** Resmi hesap olasılıklı ([ADR-0011](docs/decisions/adr-0011-faz3-olasilikli-hesap.md), `src/kac_ev_olasilik.py`; tek denklem `kac_ev.py` yedek). `kac_ev.csv` sözleşme 1.3.
  - Resmi sınav = karar masası koşumu (Mac, 19:35–19:50, 20 şehir sıfırdan), sınav 11–20:
    - yanlış yeşil 0/87 GEÇTİ;
    - %40 kuralı 41/284 yan yana; dolu trafoya "yer var" %40 kuralı 41/73, biz 0/73;
    - kaç ev orta 2 GEÇTİ;
    - yanlış kırmızı %27,3 ve sarı %62,2 hedef üstü, raporlandı.
  - ROADMAP Faz 3'te kutular [x] ve **"Açık eksikler"** tablosu (bu gece / pilot).
  - **Bilginin değeri** (üst sınır, farazi şehir): bara gerilimi bilinirse yanlış kırmızı %19; bara + panelli evin yeri + faz %4. Sarı ancak %57, ağın tamamıyla %41: sarı bilgi değil yeşilin sorusu ("sıradaki başvuru kimden"). Karar masasına UYARI 19:59.
  - Yeşil eşiği 0,98 kalır (karar masası 19:44, eşiğin bedeli tablosu günlükte).
  - Dil (karar masası 19:13): karamsar–iyimser %80 bant, "en az" değil; manşet "yaklaşık N ev (A–B)"; vaat renkte.
  - Günlükler:
    - [Faz 3](docs/log/2026-10-31-volkan-faz3.md): tek denklem, resmi sınav çıktıları, eşiğin bedeli, bilginin değeri;
    - [varsayım envanteri](docs/log/2026-10-31-volkan-faz3-varsayimlar.md): hiçbir ayar kırmızıyı düzeltmiyor; öğlen OG +%0,8 UKPN'le çelişiyor;
    - [olasılıklı](docs/log/2026-10-31-volkan-faz3-olasilik.md);
    - [İngiltere geri-testi](docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md): 6 hattın 5'i kapsandı, Bancroft kaçtı; yeşil bütçesi gerçek veride doğrulanmadı.
- **Faz 4** (Civan): harita ve yan panel Faz 3 tablosuna bağlı. Açık: internetsiz açılış, 2 dk ekran kaydı, 20 şehirde kontrol.
- **Faz 5** (paralel): `docs/sunum/` (Can) ve [konuşma notu taslağı](docs/konusma-notu-taslak.md) (BUILD). Hikâye "güven merdiveni"; dashboard içinde 7 ekran (Volkan 17:32). Ekran 5 rakamları karar masası koşumundan (can.md 19:51); ekran 6 cümlesi Can'da (can.md 19:59). 2 prova yapılmadı.

## Açık işler (BUILD)
1. **Karar masasının cevabı bekleniyor** (volkan.md UYARI 19:59, bilginin değeri):
   - jüri cevabı "sarıyı azaltan şey ölçüm" deneme ile tam tutmuyor, yeni cümle önerildi;
   - ürün önerisi: sarı trafoda karar başvuru anında, evin adresi ve fazıyla (sınanmadı);
   - ekran 6 "Kıb-Tek'ten yeni veri istemiyoruz" ↔ %4 için panelli abonenin adresi ve fazı gerekiyor.
2. **Karar masasının cevabı bekleniyor** (volkan.md UYARI 20:43, [ada ülkeleri günlüğü](docs/log/2026-10-31-volkan-ada-ulkeleri.md)):
   - sunum / jüri cümlesi: Malta'nın açık haritası da düz %25 tavan (Kıb-Tek %40), Hawaii %15 → %250;
   - Gozo hattında dış sınama (30 dk);
   - üretici 1.3 trafo boyutu çapası (Malta talep ÷ güç).
3. **Faz 5:** konuşma notu taslağını Can'ın `docs/sunum/`'u ile birleştirmek; gece 2 prova.
4. **Can:** ekran 5 ve kilit grafik PNG karar masası rakamlarıyla (0/87); ekran 6 cümlesinin ilk yarısı; Enemalta KAYNAK ve sözlük satırı (can.md 20:43).
5. Uzmana sorulacaklar güncel: [plan](docs/01-plan.md) soru 2–8 (abone–trafo eşleşmesi, hat kaydı, faz, yük analizörü, panelli abone, çekilen/verilen kaydı, trafo plakası ve kademe).

## Bilinen sorunlar ve kararlar
- BUILD klasöründeki şehirler (16:57) karar masasının sıfırdan ürettikleriyle aynı renkleri verir, ama 11–20'de bir trafo farkı var (dolu 74 ↔ 73); sebep aranmadı. Resmi rakam karar masasınınki.
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
1. Karar masasının 19:59 cevabını uygula (jüri cevabı, ekran 6 cümlesi; başvuru anında hesap pilot listesine girerse ROADMAP).
2. Faz 5: konuşma notu ↔ `docs/sunum/` birleştirme (Can'la, kutudan); 2 prova.
3. Faz 4 kontrol: Civan'ın yan paneli sözleşme 1.3 sütunlarıyla (kutudan, `app/`'e yazmadan).
