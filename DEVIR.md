# Devir notu — şu an nerede kaldık

Bu dosya tek sayfa, anlık durum. Her faz sonunda ve iş devrederken Volkan (+ Claude) günceller; eski hali silinir, geçmiş [docs/log/](docs/log/) altında. Yeni gelen ya da yeni oturum: önce bunu, sonra [README](README.md) ve [Faz 0](docs/02-faz-0-ogrenim.md).

**Güncellendi:** 1 Kasım 2026, 00:30 (KARAR) — PR #19, #21 birleşti; iş tahtası; üç oturum düzeni, ADR-0017 / 0018. Önceki: 31 Ekim 2026, 23:55 — oturumlar siliniyor (Volkan); bütün iş main'de ya da PR dallarında (#19, #21, #22). Yeni oturum buradan, `grep -n "Durum: bekliyor" docs/istek/*.md` ve ROADMAP "Faz 6–12"den devam eder.

## Kim nerede (1 Kasım 00:15; Volkan'ın üç oturumu, CONTRIBUTING "Volkan'ın üç oturumu")
- **KARAR:** Volkan adına karar, istek kutusu (`docs/istek/volkan.md`), PR birleştirme, ADR. PR'ların Mac testini 1 Kasım 00:42'den beri **TEST** oturumu (Opus) koşar ve KARAR'a yazar (öneren ≠ puanlayan; resmi rakam Mac koşusu).
- **BUILD 1 — yük haritası** (dal `yuk/`, PR "[Yük]"): Muhittin 4 madde 1–4 — yük temel katman, akşam tepesi ön sürümü ([ADR-0018](docs/decisions/adr-0018-aksam-tepesi-on-surum.md), `src/tepe.py`), Kıb-Tek tepe verisinin girişi, öğlen yükü; Can'ın yük PR'larını inceler.
- **BUILD 2 — panel gerilimi** (dal `panel/`, PR "[Panel]"): PR #19 ve #22'yi bitirir; Muhittin 4 madde 1'in panel kısmı (güvenli uçlar, [ADR-0017](docs/decisions/adr-0017-pv-katmani-guvenli-uclar.md)) ve madde 5 (kademe, inverter geri çözümü).
- **Can:** veri, eşzamanlılık, sıcaklık eğimi, üretici 1.5 (31–40), B-Y2 (`tepe.py`'ye PR), tepe sınav kodu. **Civan:** Faz 4 kalanı, harita kartları (güvenli uçlar, yük ikinci sayısı).
- BUILD'ler yalnız KARAR'a yazar; kutu girdisinin başlığında "(BUILD 1 — yük)" ya da "(BUILD 2 — panel)".

## İş tahtası (KARAR günceller; her PR ve kutu olayında, 1 Kasım 00:49)
Tek yer: açık PR'lar ve sürmekte olan işler, kimde, kimi bekliyor. Ayrıntı kutu girdisinde (`docs/istek/volkan.md`).

| İş | Kimde | Durum | Bekleyen |
|---|---|---|---|
| PR #22 başvuru anı motoru + sahte kayıt (deneme) | BUILD 2 | Mac tekrarı birebir (KARAR 00:27); dal güncellendi, pilot şartı yazıldı (34c10ab) | §7 onayı (Civan) |
| Öğlen yükü kontrolü, Kıb-Tek tepe verisi girişi (Muhittin 4 m. 3–4) | BUILD 1 | sırada | — |
| PR #23 güvenli uçlar, `pv_uc` (Muhittin 4 m. 1 panel, ADR-0017) | BUILD 2 | Mac'te tuttu (KARAR 00:32) | §6 onayı (Civan / Can) |
| PR #25 inverter geri çözümü (Muhittin 4 m. 5B; #22 üstünde) | BUILD 2 | yeni hâli bf19af4: ölçülmüş kayma, ham özet; inverter haritayı açmıyor (KARAR 00:49) | TEST'in Mac tekrarı; ROADMAP / kart satırları (BUILD 2); sonra #22 |
| Sarıda konum payı (`yesil_konum_payi`, ADR-0015 m. 4) | BUILD 2 | sırada | — |
| PR #24 yılın tepesi ön sürümü (`tepe.py`, ADR-0018) | BUILD 1 | Mac'te birebir; İspanya kıl payı KALDI (%15,4); iki ADR uyum düzeltmesi (KARAR 00:42) | Velander + uzun seri (BUILD 1), §7/§8 numarası, onay (Civan / Can) |
| PR testleri (Mac, bağımsız koşu) | TEST oturumu (Opus) | başladı: main sağlık koşusu | KARAR'ın yolladığı PR'lar |
| Üretici 1.5, sınav şehirleri 31–40 | Can | PR #21'in son hâlinin üstüne taşınacak (can.md 00:24) | — |
| B-Y2 (iki bileşen, eğim fitleri; `tepe.py`'ye PR), tepe ve bayrak sınav maddeleri | Can | sırada (can.md 00:15) | BUILD 1'in iskeleti |
| Harita: güvenli uçlar kartı, yük ikinci sayısı; Faz 4 kalanı | Civan | `pv_uc` sütunu gelince (civan.md 00:15) | BUILD 2 |
| Sunum rakam sürümü (v2 / v3) | Volkan | bekliyor | — |

Birleşenler (1 Kasım): #19 (07ea153), #21 (c53ab31).

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
  - **Bilginin değeri** (üst sınır, farazi şehir): bara gerilimi bilinirse yanlış kırmızı %19; bara + panelli evin yeri + faz %4. Sarı ancak %57, ağın tamamıyla %41: sarı bilgi değil yeşilin sorusu ("sıradaki başvuru kimden").
  - **Sarı trafoda karar başvuru anında** ([ADR-0012](docs/decisions/adr-0012-sari-trafoda-karar-basvuru-aninda.md), karar masası 20:47; kabul, sınanmadı, bu gece kod yok). Sunumda yalnız jüri cevabı, "sınanmadı" etiketiyle.
  - Ada ülkeleri ([günlük](docs/log/2026-10-31-volkan-ada-ulkeleri.md)): Malta'nın açık haritasında izin hiçbir merkezde trafo gücünün %25'ini geçmiyor; jüri cevabı ve kaynak slaydına girer, ana ekran değil. Gozo hattı koşulmadı (bilgi eksik), dış sınama adayı.
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
1. **Faz 4 Mac kontrolü yapıldı (20:58, civan.md KONTROL 20:55):** sayılar birebir ve 3 şehir [x]; tıklama 0,35–0,40 sn; dışarıya istek yok. Civan'da: dil 19:13'e göre değil; %40 kuralının ev sayısı aday evden fazla (241/701). Windows ve ekran kaydı açık. Eski görev metni: Civan'ın uygulamasını Mac'te çalıştır; internetsiz açılış, 3 şehir seçimi, yan paneldeki sayılar `kac_ev.csv` ile 3 trafoda birebir, tıklama süresi. Sonuç civan.md "## KONTROL" ve ROADMAP Faz 4 kutuları (ölçülen kadarı). `app/`'e dokunma; düzeltme Civan'ın.
2. **Faz 5:** [konuşma notu taslağı](docs/konusma-notu-taslak.md) 20:58'te güncel (karar masası 20:47 cümleleri, sehir-001 tıklama sırası, prova listesi). Can `docs/sunum/`'a taşır; ekran 5 rakamları orada hâlâ "BEKLİYOR". Gece 2 prova. Konuşma notuna "%4" cümlesi: "Kıb-Tek'in kendi kayıtlarında panelli abonenin adresi ve fazı varsa %4'e" (karar masası 20:47).
3. **Can:** ekran 5 ve kilit grafik PNG karar masası rakamlarıyla (0/87); ekran 6 netleşen cümle ve jüri cevapları (can.md 20:50); Enemalta KAYNAK ve sözlük satırı (can.md 20:43).
4. Uzmana sorulacaklar güncel: [plan](docs/01-plan.md) soru 2–8 (abone–trafo eşleşmesi, hat kaydı, faz, yük analizörü, panelli abone, çekilen/verilen kaydı, trafo plakası ve kademe).

5. **Faz 6–12 durumu** (ROADMAP "Faz 6–12" güncel): Faz 7 kalibrasyonu (K_YUK 1,47, karar masası 23:13; ürünün tabakalı seçimi), Faz 8 üretici 1.3 ve sınav şehirleri 21–30, PV açılma denemesi, Gozo main'de. Resmi rakamlar v3 (gerçekçi şehirler), Mac doğrulamalı.
6. **Açık işler (öncelik sırasıyla):**
   - **Açık PR'lar ve kimin işi:** yukarıdaki "İş tahtası" (KARAR günceller).
   - **Can (yük haritası, Faz 11):** üretici 1.5 (yaz boyutlandırması: kVA yılın tepesine göre, 1.600 / 2.500 kVA, uzun hatta kesit; yeni sınav şehirleri 31–40; çapa Malta ortanca 0,42, aşan %1,5; 207 V altı ≤ %1, en düşük ≥ 200 V), `src/tepe.py` iki bileşenli tepe modeli (eşzamanlılık ve sıcaklık eğimi 20 Kıbrıs evinden), sözleşme `tepe.csv`. Volkan'ın dosyalarına PR ile, BUILD onaylar; tepe sınavını Civan ya da BUILD puanlar.
   - **Volkan'da:** sunum rakam sürümü (v1 / v3; karar masası önerisi v3); panel sunumda anlatılmayacak (yük haritası öne).
7. **BUILD'in yerel durumu** (git dışı): üretici 1.3 şehirleri `trafo-sablonu-build/data/synthetic/u13/` (1–10, 21–30; K_YUK 1,47 ile `tahmin.csv` / `kac_ev.csv`; her şehirde sahte `kayitlar.csv`); Open-Meteo 2024–2025 dosyası yalnız bu klasörde (`data/raw/open-meteo-lefkosa/`); İspanya ham verisi `hackaton/edp-ham/Sim_files_190128_OK_V0/GIS_data`. Başvuru testi: `python3 src/basvuru_testi.py data/synthetic/u13 --aralik 21-30 --json x.json` (~1 dk).

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
1. PR #22: iki kat hata varsayan motor koşumu + tüzük madde 2 cümlesi (BUILD); Mac tekrarı (karar masası); §7 onayı (Can / Civan).
2. PR #21 Civan onayı, PR #19 ve #21 için Volkan'ın "birleştir" sözü.
3. Can'ın üretici 1.5 + tepe modeli PR'ları geldikçe BUILD onayı; sunum sürümü kararı (Volkan).
