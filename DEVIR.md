# Devir notu — şu an nerede kaldık

Bu dosya tek sayfa, anlık durum. Her faz sonunda ve iş devrederken Volkan (+ Claude) günceller; eski hali silinir, geçmiş [docs/log/](docs/log/) altında. Yeni gelen ya da yeni oturum: önce bunu, sonra [README](README.md) ve [Faz 0](docs/02-faz-0-ogrenim.md).

**Güncellendi:** 1 Kasım 2026, 01:53 (KARAR) — faz haritası ROADMAP'te; #27 birleşti; 10 PR testi geçti, onay bekliyor; ADR-0017 / 0018 / 0019. Önceki 00:30: PR #19, #21 birleşti; iş tahtası; üç oturum düzeni. Önceki: 31 Ekim 2026, 23:55 — oturumlar siliniyor (Volkan); bütün iş main'de ya da PR dallarında (#19, #21, #22). Yeni oturum buradan, `grep -n "Durum: bekliyor" docs/istek/*.md` ve ROADMAP "Faz 6–12"den devam eder.

## Kim nerede (1 Kasım 00:15; Volkan'ın üç oturumu, CONTRIBUTING "Volkan'ın üç oturumu")
- **KARAR:** Volkan adına karar, istek kutusu (`docs/istek/volkan.md`), PR birleştirme, ADR. PR'ların Mac testini 1 Kasım 00:42'den beri **TEST** oturumu (Opus) koşar ve KARAR'a yazar (öneren ≠ puanlayan; resmi rakam Mac koşusu).
- **BUILD 1 — yük haritası** (dal `yuk/`, PR "[Yük]"): Muhittin 4 madde 1–4 — yük temel katman, akşam tepesi ön sürümü ([ADR-0018](docs/decisions/adr-0018-aksam-tepesi-on-surum.md), `src/tepe.py`), Kıb-Tek tepe verisinin girişi, öğlen yükü; Can'ın yük PR'larını inceler.
- **BUILD 2 — panel gerilimi** (dal `panel/`, PR "[Panel]"): PR #19 ve #22'yi bitirir; Muhittin 4 madde 1'in panel kısmı (güvenli uçlar, [ADR-0017](docs/decisions/adr-0017-pv-katmani-guvenli-uclar.md)) ve madde 5 (kademe, inverter geri çözümü).
- **Can:** veri, eşzamanlılık, sıcaklık eğimi, üretici 1.5 (31–40), B-Y2 (`tepe.py`'ye PR), tepe sınav kodu. **Civan:** Faz 4 kalanı, harita kartları (güvenli uçlar, yük ikinci sayısı).
- BUILD'ler yalnız KARAR'a yazar; kutu girdisinin başlığında "(BUILD 1 — yük)" ya da "(BUILD 2 — panel)".

## İş tahtası (KARAR günceller; her PR ve kutu olayında, 1 Kasım 09:21)
Tek yer: açık PR'lar ve sürmekte olan işler, kimde, kimi bekliyor. Ayrıntı kutu girdisinde (`docs/istek/volkan.md`).

| İş | Kimde | Durum | Bekleyen |
|---|---|---|---|
| PR #36 ticari I / II bölmesi (gece prizi) | BUILD 2 | olumsuz sonuç, kod birleşmez (KARAR 08:41) | günlük main'e (BUILD 2) → KARAR PR'ı kapatır |
| Öğlen yük güveni ölçümü (panelin darboğazı) | BUILD 1 | bitti → ADR-0019 | — |
| Ölçüm sırası ve konum payı analizini yeni kurala çevirme (#33 sonrası, küçük PR) | BUILD 2 | sırada | #33 |
| PR testleri (Mac, bağımsız koşu) | TEST oturumu (Opus) | main sağlık koşusu birebir (KONTROL 01:00); sırada #25 (a5cfddd), sonra #24, #26 | KARAR'ın mesajı |
| B-Y2 incelemesi (Can'ın PR'ı gelince) | BUILD 1 | bekliyor | Can |
| B-Y2 (iki bileşen, eğim fitleri; `tepe.py`'ye PR), tepe ve bayrak sınav maddeleri | Can | sırada (can.md 00:15) | BUILD 1'in iskeleti |
| Harita: güvenli uçlar kartı (`pv_uc`), yük ikinci sayısı ve iki aday saat (`tepe.csv`); Faz 4 kalanı | Civan | sütunlar main'de (02:00) | — |
| Sunum rakam sürümü (v2 / v3) | Volkan | bekliyor | — |

Birleşenler (1 Kasım): #19, #21–#35, #37 (dashboard) — ADR-0019 yürürlükte. **Birleştirme kuralı (Volkan 01:5x):** karar masasının (ya da TEST'in) Mac testini geçen PR GitHub onayı beklemeden birleşir; eksi bulgulu PR düzelmeden birleşmez.

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
- Sahte kaydın "gerçek" ağı yeniden kurması `kac_ev_gercek`'te 784/800 birebir (farklar 1–2 ev): kritik anlar 0,1 V'a yuvarlanmış gerilim serisinden seçiliyor. Panel sınavlarında trafoların ~%2'si bu payla okunur; düzeltme yavaş, şimdilik yok (karar masası 02:25).
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

## Sıradaki üç adım (1 Kasım 01:53)
1. Gece 14 PR birleşti, açık PR yok (02:29); ADR-0019 yürürlükte. Faz haritası ROADMAP "Faz 6–12" başında (01:53 hâli; Faz 9–12 satırlarındaki "onay bekliyor" ifadeleri artık "main'de").
2. BUILD 2: ölçüm sırası ve konum payını ADR-0019 kuralına çevirir (31–40 bir kez); BUILD 1: Can'ın B-Y2'sini inceler; TEST: gelen PR'lar.
3. Civan: güvenli uçlar kartı, yük ikinci sayısı, iki aday saat. Volkan: sunum rakam sürümü, Kıb-Tek istek metni, tanıdık evde inverter + priz ölçümü.
