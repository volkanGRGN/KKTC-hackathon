# 2026-11-01 — Can: kod envanteri (öncesi) ve `sinav.py` deneme incelemesi (clean review adım 1–2)

**Etiket: ölçüm, salt okur.** Kod değişmedi. Yöntem: "Clean review" planı (Volkan, 1 Kas; Muhittin'in rehberi sürüm 1, 2, §8 eki). Bu günlük planın §2 "öncesi" ölçümü ve §6 adım 2 (deneme modülü: `sinav.py`).

## Hipotez / amaç
Plan: önce ölç ve haritala, sıcak noktadan başla. Araç kurulumu (lizard, jscpd, vulture) Volkan'ın izninde; izin gelmeden yapılabilecek kadarı. Deneme modülü `sinav.py` en sıcak dosya ve Can'ın dosyası: ölçüt ve bulgu şablonu burada denenir.

## Yaptıklarım
1. **Araç yok → dilin kendi aracı** (plan Ek B "araç yoksa"): kurulum ve indirme yok. Python 3.13'ün `ast` + `tokenize` modülleri ve `git` ile tek betik (aşağıda, "Ölçüm betiği"). Ölçüler lizard / jscpd / vulture'ın **tahmini** karşılığı:
   - karmaşıklık: 1 + if / elif / for / while / except / koşullu ifade / `and`-`or` / comprehension ve `if`'i / `case` (lizard'a yakın; **iç fonksiyonlar dış fonksiyona da sayılır**, lizard ayrı sayar);
   - kopya: adlar, dizgiler, sayılar normalize edilmiş 60 jetonluk pencere (jscpd'nin "adı değişmiş kopya"sı gibi; min 50 jeton yerine 60), bitişik pencereler birleştirilir;
   - ölü aday: modül düzeyinde tanımlanıp hiçbir dosyada adı (ya da dizgi içinde adı) geçmeyen fonksiyon / sınıf (vulture %60 güvenine yakın, daha gevşek);
   - sıcak nokta: son 31 günde dosyanın değiştiği commit × dosyadaki dal sayısı (karmaşıklık − 1 toplamı).
2. Kapsam: `src/*.py` (24) + `app/*.py` (3). `app/` ölçüldü, incelenmedi (kapsam kararı Volkan / Civan'da, plan §6 adım 0).
3. `sinav.py` derin geçiş: dosya tek parça okundu (816 satır, 30 fonksiyon); her bulgu satıra bağlandı, "neden var" için `git blame` ve commit mesajı; çağıranlar: `grafikler.py` (`sinav.KAPSAMA`, `HATA_ORTANCA_MAX`, `_hatalar`, `sehirleri_oku`, `faz2_oku`, `faz3_oku`).
4. İkinci göz: bulgular ayrı bir ajana (öneren ≠ puanlayan) kanıtıyla teyit ettirildi: 10 bulgunun 6'sı olduğu gibi, 4'ü düzeltmeyle teyitli (S-03 anlatım, S-04 sayı, S-05 kapsam, S-09 eksik biçim; düzeltmeler bulgulara işlendi), bırakılan üç gerekçe teyitli; ikinci göz iki bulgu ekledi (S-11, S-12), ilk inceleyen bunları satırlarından teyit etti.

## Sonuç — envanter (main 35d5445, 1 Kas) [Hesap: betik, aşağıda]

| ölçü | değer |
|---|---|
| dosya / satır | 27 / 8.632 (`src/` 24 dosya 7.798; `app/` 3 dosya 834) |
| tek başına yorum satırı | 319 (%3,7; satır sonu yorum ve docstring sayılmadı) |
| etiket | [Kaynaklı 23 · [Hesap 70 · [Yorum 93 · BULAMADIM 19 |
| fonksiyon | 352; karmaşıklık > 15: 37; > 30: 9; 100 satırdan uzun: 6 |
| kopya (60 jeton, tahmini) | 591 / 8.632 satır (%6,8) en az bir kopyada; ≥ 100 jetonluk 13 çift |
| ölü aday (kaba) | 0 — gevşek yöntem; vulture koşulmadı, "ölçülmedi: vulture yok" sayılmalı |
| son 31 günde commit | 441 |

**Sıcak noktalar** (commit × dal):

| sıra | dosya | satır | commit | dal | sıcaklık |
|---|---|---|---|---|---|
| 1 | `src/sinav.py` | 816 | 16 | 415 | 6.640 — ikinciden 1,9 kat |
| 2 | `src/sehir_uret.py` | 990 | 12 | 291 | 3.492 |
| 3 | `src/tepe.py` | 611 | 6 | 180 | 1.080 |
| 4 | `src/sablon.py` | 599 | 8 | 110 | 880 |
| 5 | `src/kac_ev_olasilik.py` | 325 | 7 | 100 | 700 |
| 6 | `src/trafo_bos_kapasite.py` | 530 | 3 | 212 | 636 |
| 7 | `app/harita.py` | 375 | 9 | 49 | 441 |
| 8 | `src/edp_test.py` | 375 | 5 | 55 | 275 |
| 9 | `app/ornek_veri.py` | 358 | 6 | 45 | 270 |
| 10 | `src/kalibrasyon.py` | 237 | 4 | 67 | 268 |

Plandaki tablodan (b1b810c) fark: `tepe.py` 566 → 611 satır, 4. → 3. sıra (BUILD 1'in tepe saati işi).

**En karmaşık 10 fonksiyon:**

| fonksiyon | satır | karmaşıklık | boy | param | iç içe |
|---|---|---|---|---|---|
| `sinav.py` `faz2` | 337–606 | 145 (iç fonksiyonlar hariç ~126) | 270 | 3 | 5 |
| `sinav.py` `faz3` | 630–771 | 102 (iç hariç ~94) | 142 | 1 | 3 |
| `sehir_uret.py` `sehir_uret` | 793–973 | 76 | 181 | 3 | 4 |
| `sinav.py` `faz1` | 74–168 | 63 | 95 | 1 | 2 |
| `tepe.py` `sehir_calistir` | 422–579 | 63 | 158 | 8 | 6 |
| `basvuru.py` `ag_kur_kayitli` | 49–144 | 62 | 96 | 5 | 3 |
| `trafo_bos_kapasite.py` `main` | 423–526 | 58 | 104 | 0 | 4 |
| `inverter_kaydi.py` `main` | 117–183 | 55 | 67 | 0 | 3 |
| `bilgi_degeri.py` `olc` | 218–249 | 32 | 32 | 3 | 4 |
| `kac_ev_olasilik.py` `ag_kur` | 92–153 | 30 | 62 | 2 | 3 |

**Kopya, dosya başına pay** (en yüksek): `pv_acilma.py` %33, `kac_ev_olasilik.py` %27, `bilgi_degeri.py` %24, `basvuru.py` %22, `olcum_sirasi.py` %13. En büyük çiftler (jeton): `basvuru.py` 161–177 ↔ 196–212 (213, dosya içi); `sehir_uret.py` 681–689 ↔ 728–736 (187, dosya içi); `bilgi_degeri.py` 200–212 ↔ `pv_acilma.py` 92–104 (170); `bilgi_degeri.py` 64–73 ↔ `sahte_kayit.py` 68–77 (165); `app/ornek_veri.py` 89–111 ↔ `sehir_uret.py` 397–420 (162); `kac_ev.py` 183–191 ↔ `kac_ev_olasilik.py` 308–316 (136); `sehir_uret.py` 353–364 ↔ `trafo_bos_kapasite.py` 93–104 (129); `edp_test.py` 180–184 ↔ `sablon.py` 190–194 (98).

**Adım 3 için işaretler (incelenmedi, yalnız nereye bakılacağı):**
- `sinav.py faz3` tanımları (küme kac_ev_aday > 0, dolu = kac_ev_gercek = 0, yanlış yeşil, kaç ev hatası, aralık kapsaması) üç yerde daha yeniden yazılmış: `bilgi_degeri.py:218` `olc` ("sinav.py faz3 ile aynı tanımlar"), `pv_acilma.py:126` `main` (ölçüler "`sinav.py faz3` tanımları"), ve bu ikisi birbirinin kopyası (170 + 143 + 79 + 79 jeton). `grafikler.py` aynı işi `import sinav` ile yapıyor — tek kaynak örneği var.
- `ABONE` + abone başına MWh sözlüğü beş dosyada (bkz. S-05).
- `app/ornek_veri.py` ↔ `sehir_uret.py` 162 jetonluk kopya: sahte veri üreticisi üreticinin bir parçasını kopyalamış (plan §1 "sahte veri" maddesiyle birlikte bakılmalı).

## Sonuç — `sinav.py` deneme incelemesi

**Dosya memosu.** Amaç: üretilen şehirleri ROADMAP eşiklerine göre ölçmek; üç giriş `faz1` / `faz2` / `faz3`, her biri `(maddeler, bilgi)` döner; madde = `(True | False | 'UYARI', ad, ayrıntı)`. Ana türler: şehir sözlüğü `s` (`sehirleri_oku` + `faz2_oku` / `faz3_oku` alanları ekler; `faz2` de `s['gercek']`, `s['tip']`, `s['hata']` ekler — fonksiyon girdisini değiştirir). Dışarıdan kullanılan adlar (`grafikler.py`): `KAPSAMA`, `HATA_ORTANCA_MAX`, `_hatalar`, `sehirleri_oku`, `faz2_oku`, `faz3_oku` — temizlikte bunlar korunmalı. Model kodunu import etmez (öneren ≠ puanlayan; sabit kopyaları bilerek). Birim testi yok; davranışın ölçüsü üç fazın çıktı metni (karakterizasyon).

**"Neden var" — bırakılanlar (bulgu değil):**
- `faz2` İspanya ızgarası (432–434) girdiyi `('a', 'b', 'c')` ile sabitliyor; `edp_test.py` ayrıca bantsız `kiyas` ve `saf_fatura` satırları yazıyor (`edp_test.py:310`, `:316`), bunlar `_kal`'da `float('')` ile çökerdi. Sabit liste koruma; veriden türetme önerilmez.
- Hep geçen maddeler (`_madde(m, True, …)` 584, 676): ROADMAP'te "karşılaştırıldı / yan yana" maddeleri; kaldırılmaz.
- `ABONE` / `MWH_ABONE` kopyası (171–177): yorumda "sınav kendi kopyasını tutar" (174); bağımsızlık için doğru tekrar (S-05 yalnız eşitlik denetimi ve etiket önerir).

**Özet tablo** (kazanç ÷ (risk × efor); D = düşük, O = orta, Y = yüksek):

| ID | başlık | kategori | risk | efor | kazanç | güven |
|---|---|---|---|---|---|---|
| S-03 | `guv` / `tip_h` döngüleri `_hatalar`'ın filtresini kopyalıyor, sıraya gizlice bağlı | tekrar | D | D | O | gözlemlendi |
| S-06 | docstring `kac_ev.csv`'nin yazarını `kac_ev.py` diyor | belge-çelişkisi | D | D | D | gözlemlendi |
| S-07 | üç tahmin listesi iki kez | tekrar | D | D | D | gözlemlendi |
| S-08 | "en kötü şehir" hesabı iki kez | tekrar | D | D | D | gözlemlendi |
| S-01 | `faz2` tek fonksiyonda dokuz bölüm | spagetti | D | O | Y | gözlemlendi |
| S-04 | `olculdu` filtresi 13 kez | tekrar | D | O | O | gözlemlendi |
| S-05 | abone başına MWh beş dosyada, etiketler farklı | tekrar / belge-çelişkisi | D | D | O | gözlemlendi |
| S-10 | sabitler dört blokta, `_oran` kullanıldığı yerden sonra | tutarsız-desen | D | D | D | gözlemlendi |
| S-02 | `faz3` tek fonksiyonda | spagetti | D | O | O | gözlemlendi |
| S-09 | üç durumlu sonuç dizginin doğruluk değerine dayanıyor, yazımı üç biçim | tutarsız-desen | D | D | D | gözlemlendi |
| S-11 | "dolu" tanımı (`gercek == 0`) satır içi tekrar | tekrar | D | D | O | gözlemlendi |
| S-12 | boş olabilen sayı sütunu iki biçimde okunuyor | tutarsız-desen | D | D | D | gözlemlendi |

### [S-01] `faz2` tek fonksiyonda dokuz bölüm
- Dosya: src/sinav.py:337-606
- Kategori: spagetti
- Ne: arketip, hata, bant, kalibrasyon (farazi + İspanya), yük haritası (farazi + İspanya), şehirler arası, düşük güven, saf tahmin, tip dağılımı ve sondaki bilgi satırları tek fonksiyonda; beş iç fonksiyon (`_sec`, `_kal`, `_tarife`, `_fatura`, `_saf_ozet`).
- Kanıt: 270 satır, karmaşıklık 145 (iç fonksiyonlar hariç ~126), iç içe 5; dosyanın en sıcak fonksiyonu (dosya 16 commit). Bölüm başlıkları yorum olarak: `# 1.` (347), `# 2.` (359), `# 3.` (374), `# 3b.` (396), `# 3c.` (443), `# 4.` (507), `# 5.` (523), `# 6.` (531), `# 7.` (573).
- Neden sorun: her yeni karar (ADR-0013, -0014, -0016, -0018) bu fonksiyona bir bölüm ekledi; bölümler arası paylaşılan durum (`h_ort`, `h_p90`, `havuz`, `s['hata']`) yalnız okuyarak bulunuyor; bir bölümü değiştirirken diğerinin değişkenine çarpmak kolay (`o`, `k`, `h`, `kt` adları bölümler arasında yeniden kullanılıyor: 367, 517, 526, 583; 467, 496).
- Neden var (kaynak): 61bf7b7 (7 madde) + e0e72f2, 6e1dff3 (Faz 7) + 3bfa967, 672ce1a, ce5b18d (Faz 11) — her biri ekleme; tasarım kararı değil.
- Önerilen değişiklik: yalnız taşıma — her bölüm `_f2_<ad>(sehirler, m, bilgi, …)` fonksiyonuna; paylaşılan değerler açık dönüş değeri (`_f2_hata` → `h_ort, h_p90, havuz`; 491'de yeniden atanan `ispanya_tepe` de). Çıktı sırası aynı kalır. Davranış değişmez.
- Risk · Efor · Kazanç: düşük (çıktı metni karşılaştırılarak) · orta · yüksek   Güven: gözlemlendi
- Bağımlılık: önce karakterizasyon (plan §5: aynı şehirlerde `faz1`/`faz2 --ispanya --ispanya-tepe`/`faz3` çıktısı dosyaya; sonra fark boş). S-03, S-04 ile birlikte yapılırsa daha az satır oynar.   Durum: teyitli

### [S-02] `faz3` tek fonksiyonda
- Dosya: src/sinav.py:630-771
- Kategori: spagetti
- Ne: satır kurma, yanlış yeşil, %40 kuralı, kırmızı kovası, bayrak, güvenli uçlar, olasılık kovaları, kaç ev hatası, sarı ve altı bilgi satırı tek fonksiyonda.
- Kanıt: 142 satır, karmaşıklık 102 (iç hariç ~94); bölüm yorumları `# 1.` (661) … `# 5.` (739), `# Bilgi.` (745).
- Neden sorun: S-01 ile aynı; daha küçük.
- Neden var (kaynak): 575d46b, sonra 5fa8c42, c3fb046, 76c1bb2, ce5b18d eklemeleri.
- Önerilen değişiklik: S-01 ile aynı kalıp; satır kurma (633–650) ayrı fonksiyon.
- Risk · Efor · Kazanç: düşük · orta · orta   Güven: gözlemlendi
- Bağımlılık: S-01'in kalıbı önce `faz2`'de denensin.   Durum: teyitli

### [S-03] `guv` / `tip_h` döngüleri `_hatalar`'ın filtresini kopyalıyor ve sıraya gizlice bağlı
- Dosya: src/sinav.py:590-605 (ve 223-234)
- Kategori: tekrar
- Ne: iki döngü aynı; yalnız anahtar farklı (`r['guven']` / `s['tip'][r['trafo_no']]`); ikisi de `s['hata']` listesini `next(hata)` ile, `_hatalar`'ın atlama kuralını elle tekrar ederek eşliyor.
- Kanıt: 594 ve 602 `if not int(r['olculdu']) and s['gercek'][r['trafo_no']] >= GERCEK_MIN_KW:` ↔ 227–232 `if int(r['olculdu']): continue` … `if g < GERCEK_MIN_KW: atla += 1; continue`.
- Neden sorun: `_hatalar`'ın atlama kuralı değişirse eşleme bozulur. Yeni bir atlama eklenirse döngüler fazla `next` çeker ve `StopIteration` ile gürültülü çöker; ama kural gevşerse ya da atlanan küme aynı boyda başka trafolar olursa hata sessizce yanlış güvene / tipe yazılır. (`GERCEK_MIN_KW` üç yerde ortak sabit; eşik değişikliği tek başına bozmaz.)
- Neden var (kaynak): 61bf7b7, ilk yazım; yama değil.
- Önerilen değişiklik: hatayı trafoyla birlikte tut (`s['hata']` yalnız `sinav.py` içinde okunuyor, değiştirmek güvenli; `_hatalar` yanında `(trafo_no, hata)` döndüren küçük yardımcı ya da `s['hata']` sözlük) ve tek döngüde iki gruplama. `_hatalar`'ın dönüşü değişmesin (`grafikler.py:87` kullanıyor).
- Risk · Efor · Kazanç: düşük · düşük · orta   Güven: gözlemlendi
- Bağımlılık: —   Durum: teyitli

### [S-04] `olculdu` filtresi 13 kez
- Dosya: src/sinav.py:227, 299, 320, 351, 379, 398, 455, 524-525, 577-578, 594, 602
- Kategori: tekrar
- Ne: "ölçülmeyen trafolar" kümesi her bölümde `int(r['olculdu'])` ile yeniden süzülüyor.
- Kanıt: `grep -c "int(r\['olculdu'\])" src/sinav.py` → 13; bunların 11'i değiştirilebilir (227 `_hatalar` içinde: `saf` (326) ve `deney` (513) satırlarında ve `grafikler.py:87`'de de çağrılıyor, kalır; 455 `tepe.csv`'nin kendi sütunu, kalır).
- Neden sorun: aynı tanım 13 yerde; bir yer farklı süzerse (ör. `tepe.csv`'nin `olculdu`'su `tahmin.csv`'ninkinden farklıysa) kimse fark etmez.
- Neden var (kaynak): bölümler ayrı ayrı eklendi (S-01).
- Önerilen değişiklik: `faz2_oku`'da bir kez `s['olcusuz']` (tahmin satırları) ve `s['olculu']`; bölümler onu kullanır. 227 ve 455 ayrı kalır.
- Risk · Efor · Kazanç: düşük · orta · orta   Güven: gözlemlendi
- Bağımlılık: S-01 ile birlikte.   Durum: teyitli

### [S-05] Abone başına MWh beş dosyada, etiketler farklı
- Dosya: src/sinav.py:171-177; src/sablon.py:54-60; src/kac_ev_olasilik.py:57-62; src/tepe.py:79; app/ornek_veri.py:41 (ve `src/sehir_uret.py:161-170` `SINIFLAR` içinde aynı oranlar)
- Kategori: tekrar / belge-çelişkisi
- Ne: aynı yedi bölme beş dosyada (ikinci göz `tepe.py` ve `app/ornek_veri.py`'yi buldu); `sinav.py` `[Kaynaklı: Kıb-Tek 2023 istatistik, …]`, `sablon.py` / `tepe.py` / `app/ornek_veri.py` `[Hesap …]`, `kac_ev_olasilik.py:59` etiketsiz ("Kıb-Tek 2023, sablon.py ile aynı kaynak").
- Kanıt: `grep -n "648494 / 175577" src/*.py app/*.py` → `kac_ev_olasilik.py:60`, `sablon.py:58`, `sinav.py:175`, `tepe.py:79`, `app/ornek_veri.py:41`, `sehir_uret.py:161,170`; değerler birebir aynı. Ölçüm betiği yalnız üçünü kopya diye buldu (`tepe.py` ve `ornek_veri.py`'yi jeton penceresi kaçırdı).
- Neden sorun: biri güncellenirse (ör. Kıb-Tek 2024) öbürleri eski kalır; sınavın saf tahmini modelden farklı sayıyla koşar. Etiket: değer kaynaklı iki sayının bölümü, yani [Hesap]; `sinav.py`'deki [Kaynaklı] yanlış etiket.
- Neden var (kaynak): 61bf7b7; 174 "sınav kendi kopyasını tutar" — öneren ≠ puanlayan için bilerek. **Birleştirme önerilmez.**
- Önerilen değişiklik: (a) `sinav.py` etiketi `[Hesap: Kıb-Tek 2023 istatistik … ÷ abone]` (Can); (b) beş sözlüğün (ve `SINIFLAR`'ın) eşitliğini denetleyen bir satır — plan §5b'deki işaretçi denetimi betiğine (sözleşme testi); (c) `kac_ev_olasilik.py` etiketi ve (b)'nin `tepe.py` / `app/` tarafı (Volkan'ın / Civan'ın dosyaları → kutu).
- Risk · Efor · Kazanç: düşük · düşük · orta   Güven: gözlemlendi
- Bağımlılık: (b) denetim betiği yazılınca.   Durum: teyitli

### [S-06] Docstring `kac_ev.csv`'nin yazarını `kac_ev.py` diyor
- Dosya: src/sinav.py:11
- Kategori: belge-çelişkisi
- Ne: `(kac_ev.csv: src/kac_ev.py)`; ADR-0011'den beri resmi yazar `src/kac_ev_olasilik.py`.
- Kanıt: `src/kac_ev.py:7` "ADR-0011'den beri yedek yol: resmi hesap src/kac_ev_olasilik.py"; `src/kac_ev_olasilik.py:294` `ke.csv_yaz(klasor / 'kac_ev.csv', …)`.
- Neden sorun: yeni okuyan sınavı yanlış üreticiyle besler.
- Neden var (kaynak): 575d46b (31 Eki), ADR-0011'den önce.
- Önerilen değişiklik: `(kac_ev.csv: src/kac_ev_olasilik.py; yedek src/kac_ev.py)`.
- Risk · Efor · Kazanç: düşük · düşük · düşük   Güven: gözlemlendi
- Bağımlılık: —   Durum: teyitli

### [S-07] Üç tahmin listesi iki kez
- Dosya: src/sinav.py:728-729, 735-736
- Kategori: tekrar
- Ne: `(('karamsar', lambda x: x['kar']), ('iyimser', lambda x: x['iyi']), (orta_ad, lambda x: x['orta']))` iki kez yazılı.
- Kanıt: 729 ve 736 aynı demet.
- Neden sorun: dördüncü bir tahmin eklenirse biri unutulur (5fa8c42'de `orta` ikisine birden eklenmiş, bu kez unutulmamış).
- Neden var (kaynak): 575d46b; 5fa8c42 iki yeri birlikte değiştirdi.
- Önerilen değişiklik: `tahminler = (…)` bir kez, iki yerde kullan.
- Risk · Efor · Kazanç: düşük · düşük · düşük   Güven: gözlemlendi
- Bağımlılık: —   Durum: teyitli

### [S-08] "En kötü şehir" hesabı iki kez
- Dosya: src/sinav.py:663, 675
- Kategori: tekrar
- Ne: `max(sehir.items(), key=lambda x: x[1][0] / x[1][1]) if sehir else None` model ve %40 kuralı için ayrı ayrı.
- Kanıt: 663 `kotu = max(sehir.items(), …) if sehir else None`; 675 `kotu40 = max(sehir40.items(), …) if sehir40 else None`.
- Neden sorun: küçük; tanım (oran) iki yerde.
- Neden var (kaynak): 575d46b.
- Önerilen değişiklik: `yanlis_yesil` en kötü şehri de döndürsün.
- Risk · Efor · Kazanç: düşük · düşük · düşük   Güven: gözlemlendi
- Bağımlılık: —   Durum: teyitli

### [S-09] Üç durumlu sonuç dizginin doğruluk değerine dayanıyor, yazımı üç biçim
- Dosya: src/sinav.py:61, 428, 528, 742, 808, 812
- Kategori: tutarsız-desen
- Ne: madde sonucu `True` / `False` / `'UYARI'`; çıkış kodu `all(g for g, _, _ in maddeler)` (812) — `'UYARI'` boş olmayan dizgi olduğu için "geçti" sayılıyor; bu, yorumdaki niyetle (61: "geçmeyi bozmaz") aynı ama örtük. Yazım üç biçim: `True if … else UYARI` (428, 528), `UYARI if asti else True` (742), doğrudan `_madde(m, UYARI, …)` (441, 504, 711).
- Kanıt: satırlar yukarıda.
- Neden sorun: örtük kural; `UYARI = ''` gibi masum bir değişiklik bütün UYARI'ları çıkış kodunda kaldı sayar (etiket de boş `[]` basar).
- Neden var (kaynak): 822c081 (Volkan 17:32 notları: raporla maddelerinde [UYARI]).
- Önerilen değişiklik: çıkış kodunu açık yaz (`all(g is not False …)`; bütün ilk argümanlar saf `bool` ya da `UYARI`, sonuç aynı) ve tek yardımcı `_rapor(m, tutar, ad, ayr)` (tutmazsa UYARI). Davranış aynı.
- Risk · Efor · Kazanç: düşük · düşük · düşük   Güven: gözlemlendi
- Bağımlılık: —   Durum: teyitli

### [S-10] Sabitler dört blokta, `_oran` kullanıldığı yerden sonra tanımlı
- Dosya: src/sinav.py:22-28, 61, 171-204, 609-615, 626-627
- Kategori: tutarsız-desen
- Ne: sabitler fazlarının önüne dağılmış; `faz1` (116) `_oran`'ı kullanıyor, `_oran` 626'da `faz3`'ün önünde.
- Kanıt: 116 `{_oran(len(alti), len(v_min))}` (`faz2` de 474, 483); 626 `def _oran(pay, payda):`.
- Neden sorun: okurken yardımcıyı bulmak için dosyanın sonuna gitmek; çalışmayı etkilemez.
- Neden var (kaynak): fazlar sırayla eklendi; `faz1`'in 4. maddesi sonradan `_oran`'ı kullandı (76c1bb2).
- Önerilen değişiklik: yalnız taşıma — yardımcılar (`_csv`, `_oran`, `_yuzde`, `_p90`, `_cv`, …) başa; faz sabitleri faz fonksiyonunun hemen önünde kalabilir (bugünkü düzen) ama `_oran` yardımcılara.
- Risk · Efor · Kazanç: düşük · düşük · düşük   Güven: gözlemlendi
- Bağımlılık: S-01 / S-02 taşımasıyla birlikte.   Durum: teyitli

### [S-11] "Dolu" tanımı (`gercek == 0`) satır içi tekrar (ikinci gözün bulgusu)
- Dosya: src/sinav.py:648, 658-659, 684, 707, 714-715, 722, 753, 768
- Kategori: tekrar
- Ne: `dolu = [x for x in satir if x['gercek'] == 0]` (648) var, ama koşul sonraki yerlerde satır içi yeniden yazılıyor.
- Kanıt: 659 `return sum(x['gercek'] == 0 for x in ys), len(ys), sehir`; 684 `asan = sum(x['gercek'] == 0 for x in kir)`; 707 `db = sum(x['gercek'] == 0 for x in bay)`.
- Neden sorun: yanlış yeşilin (en kritik ölçü) ve kırmızı / bayrak isabetinin dayandığı tanım; docstring 631 ve `bilgi_degeri.py` / `pv_acilma.py` "aynı tanım" diyor. Değişirse hepsini bulmak elle.
- Neden var (kaynak): 575d46b ve sonraki eklemeler.
- Önerilen değişiklik: satır kurarken (643) `dolu=int(r['kac_ev_gercek']) == 0` anahtarı, her yerde `x['dolu']`. Davranış aynı.
- Risk · Efor · Kazanç: düşük · düşük · orta   Güven: gözlemlendi
- Bağımlılık: S-02 ile birlikte.   Durum: teyitli

### [S-12] Boş olabilen sayı sütunu iki biçimde okunuyor (ikinci gözün bulgusu)
- Dosya: src/sinav.py:459, 462, 463, 642, 646, 649
- Kategori: tutarsız-desen
- Ne: "boşsa None" okuması `if r.get('x')` ve `if k.get('x') not in (None, '')` diye iki biçimde.
- Kanıt: 459 `float(r['v_min_tepe_v']) if r.get('v_min_tepe_v') else None`; 646 `float(k['p_bugun_asar']) if k.get('p_bugun_asar') not in (None, '') else None`.
- Neden sorun: dizgide ikisi eşdeğer, ama okuyan bunu doğrulamak zorunda; sözleşme sürümleri arası boş sütun davranışı tek yerde olmalı.
- Neden var (kaynak): farklı commit'lerde eklendi.
- Önerilen değişiklik: `_sayi_ya_da_none(r, ad)` yardımcısı; 461'deki `or … or 0` zinciri (P10 yoksa ortanca) ayrı kalır.
- Risk · Efor · Kazanç: düşük · düşük · düşük   Güven: gözlemlendi
- Bağımlılık: —   Durum: teyitli

## Karar / sıradaki adım
- **Ölçüt ve şablon denendi:** bulgu şablonu `sinav.py`'de işledi; ekleme önerisi yok. Ölçü yalnız yer gösterdi (en karmaşık iki fonksiyon); bulguların yarısı (S-03, S-05, S-06, S-09, S-11, S-12) ölçünün göremediği türden (plan §3 madde 1, 2, 6, 8).
- **Temizlik yapılmadı** (plan §6 adım 5: öbür oturumların kod işi bitip dallar main'e alındıktan sonra). `sinav.py` Can'ın; sıra önerisi: karakterizasyon dosyaları → S-06, S-07, S-08, S-03, S-12 (küçük, davranışsız) → S-01 + S-04 + S-10 (taşıma) → S-02 + S-11 → S-09; her adım ayrı commit, her adımda üç fazın çıktısı aynı.
- **Volkan'a** (kutu): araç izni (lizard, jscpd, vulture; bu ölçüm onlarsız "tahmini"), `app/` kapsamı, ölçüm betiğinin `src/sicak_nokta.py` olarak kalıcı yapılması, S-05 (c) etiketi, adım 3 işaretleri (faz3 tanımları `bilgi_degeri.py` / `pv_acilma.py`'de).

## Ölçüm betiği (aynı komutla "sonrası" ölçümü için)
`python -I olc.py <depo kökü> <çıktı.json>` — Python 3.13, yalnız standart kütüphane + `git`.

```python
"""Kurulumsuz kod envanteri (Python'un kendi aracı: ast, tokenize, git).
lizard / jscpd / vulture yerine, "tahmini" yakın ölçüler.
Kullanım: python olc.py <depo_kökü> <çıktı.json>
"""
import ast, io, json, keyword, subprocess, sys, tokenize
from collections import defaultdict
from pathlib import Path

KOK = Path(sys.argv[1])
DOSYALAR = sorted(list((KOK / 'src').glob('*.py')) + list((KOK / 'app').glob('*.py')))
PENCERE = 60


def karmasiklik(dugum):
    k = 1
    for d in ast.walk(dugum):
        if isinstance(d, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp)):
            k += 1
        elif isinstance(d, ast.BoolOp):
            k += len(d.values) - 1
        elif isinstance(d, ast.comprehension):
            k += 1 + len(d.ifs)
        elif isinstance(d, ast.match_case):
            k += 1
    return k


def derinlik(dugum, d=0):
    blok = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.Try, ast.Match)
    en = d
    for c in ast.iter_child_nodes(dugum):
        if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        en = max(en, derinlik(c, d + 1 if isinstance(c, blok) else d))
    return en


def fonksiyonlar(agac, yol):
    out = []
    for d in ast.walk(agac):
        if isinstance(d, (ast.FunctionDef, ast.AsyncFunctionDef)):
            a = d.args
            out.append(dict(dosya=yol, ad=d.name, bas=d.lineno, son=d.end_lineno,
                            satir=d.end_lineno - d.lineno + 1,
                            param=len(a.args) + len(a.kwonlyargs) + bool(a.vararg) + bool(a.kwarg),
                            kk=karmasiklik(d), derin=derinlik(d)))
    return out


def jetonlar(metin):
    out = []
    for t in tokenize.generate_tokens(io.StringIO(metin).readline):
        if t.type in (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                      tokenize.DEDENT, tokenize.ENDMARKER):
            continue
        if t.type == tokenize.NAME and not keyword.iskeyword(t.string):
            s = 'ID'
        elif t.type == tokenize.STRING:
            s = 'STR'
        elif t.type == tokenize.NUMBER:
            s = 'NUM'
        else:
            s = t.string
        out.append((s, t.start[0]))
    return out


def main():
    kayit, fon, ad_gecen, tanim = [], [], defaultdict(int), []
    jet = {}
    for p in DOSYALAR:
        yol = p.relative_to(KOK).as_posix()
        metin = p.read_text(encoding='utf-8')
        agac = ast.parse(metin)
        satirlar = metin.splitlines()
        yorum = sum(1 for s in satirlar if s.strip().startswith('#'))
        kayit.append(dict(dosya=yol, satir=len(satirlar), yorum=yorum,
                          kaynakli=metin.count('[Kaynaklı'), hesap=metin.count('[Hesap'),
                          yorum_etiket=metin.count('[Yorum'), bulamadim=metin.count('BULAMADIM')))
        fon += fonksiyonlar(agac, yol)
        for d in ast.walk(agac):
            if isinstance(d, ast.Name):
                ad_gecen[d.id] += 1
            elif isinstance(d, ast.Attribute):
                ad_gecen[d.attr] += 1
            elif isinstance(d, ast.alias):
                ad_gecen[(d.name.split('.')[-1])] += 1
        for d in agac.body:
            if isinstance(d, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                tanim.append((yol, d.name, d.lineno))
        # dizgi içinde geçen adlar (getattr, argparse alt komutları vb.)
        for d in ast.walk(agac):
            if isinstance(d, ast.Constant) and isinstance(d.value, str):
                for w in d.value.replace('.', ' ').split():
                    if w.isidentifier():
                        ad_gecen['STR:' + w] += 1
        jet[yol] = jetonlar(metin)

    olu = [dict(dosya=y, ad=a, satir=s) for y, a, s in tanim
           if ad_gecen.get(a, 0) == 0 and ad_gecen.get('STR:' + a, 0) == 0
           and a not in ('main',) and not a.startswith('__')]

    # kopya: pencere özetleri
    idx = defaultdict(list)
    for yol, js in jet.items():
        semb = [s for s, _ in js]
        for i in range(len(js) - PENCERE + 1):
            idx[hash(tuple(semb[i:i + PENCERE]))].append((yol, i))
    ciftler = defaultdict(set)  # (yolA, yolB) -> {(iA, iB)}
    for yerler in idx.values():
        if len(yerler) < 2 or len(yerler) > 20:
            continue
        for a in range(len(yerler)):
            for b in range(a + 1, len(yerler)):
                (ya, ia), (yb, ib) = yerler[a], yerler[b]
                if ya == yb and abs(ia - ib) < PENCERE:
                    continue
                ciftler[(ya, yb)].add((ia, ib))
    kopya = []
    for (ya, yb), noktalar in ciftler.items():
        noktalar = sorted(noktalar)
        bas = onc = noktalar[0]
        for n in noktalar[1:] + [None]:
            if n is not None and n[0] == onc[0] + 1 and n[1] == onc[1] + 1:
                onc = n
                continue
            ja, jb = jet[ya], jet[yb]
            kopya.append(dict(a=ya, a_satir=[ja[bas[0]][1], ja[onc[0] + PENCERE - 1][1]],
                              b=yb, b_satir=[jb[bas[1]][1], jb[onc[1] + PENCERE - 1][1]],
                              jeton=onc[0] - bas[0] + PENCERE))
            if n is not None:
                bas = onc = n
    kopya.sort(key=lambda k: -k['jeton'])

    # sıcak nokta
    log = subprocess.run(['git', '-C', str(KOK), 'log', '--since=31.days', '--name-only', '--pretty=format:'],
                         capture_output=True, text=True, encoding='utf-8').stdout
    sayi = defaultdict(int)
    for s in log.splitlines():
        if s.strip():
            sayi[s.strip()] += 1
    toplam_commit = subprocess.run(['git', '-C', str(KOK), 'rev-list', '--count', '--since=31.days', 'HEAD'],
                                   capture_output=True, text=True).stdout.strip()
    dal = defaultdict(int)
    for f in fon:
        dal[f['dosya']] += f['kk'] - 1
    for k in kayit:
        k['commit'] = sayi.get(k['dosya'], 0)
        k['dal'] = dal[k['dosya']]
        k['sicaklik'] = k['commit'] * k['dal']
        k['fonksiyon'] = sum(1 for f in fon if f['dosya'] == k['dosya'])
    json.dump(dict(dosyalar=kayit, fonksiyonlar=fon, olu_aday=olu, kopya=kopya,
                   toplam_commit=toplam_commit, pencere=PENCERE),
              open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


main()
```

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
