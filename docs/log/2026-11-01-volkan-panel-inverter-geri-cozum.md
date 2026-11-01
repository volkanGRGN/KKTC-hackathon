# 2026-11-01 — İnverter geriliminden geri çözüm, benzetimde gerçekten (BUILD 2 — panel; Muhittin 4 madde 5B)

**Amaç:** Muhittin'in dördüncü cevabı madde 5: kademe / çıkış gerilimini ölçmeden daraltma. (A) Kıb-Tek'ten trafo başına kademe ayarı ve devreye alma kaydı; (B) inverter geriliminden geri çözüm (sakin an → bara, öğlen salınımı → hat empedansı). Bugüne kadar (B) hep "gerçek değer + gürültü" diye taklit edildi: PR #20'de her panelli trafoda bir inverter, bara ±1 V, empedans ±%20; PR #22'nin sahte kayıtlarında inverter panelli evlerin %20'sinde, empedans yalnız inverterin hattında, iki kat düzeyde ±2 V / ±%40 (karar masası 23:03'ün iki düzeltmesi orada uygulanmış; PR #20 betiğinde değil). Soru: geri çözümü benzetimde gerçekten yaparsak hata ne kadar, ve motorun varsayımı bunu karşılıyor mu.

**(A) durumu:** Kıb-Tek istek taslağında madde 4 "her trafonun kendi kademe ayarı: devreye alma kaydı ya da son ayar kaydı" zaten var (karar masası 00:14). Yeni iş yok; PR #20'nin bulgusu (standart değil trafonun kendi ayarı açıyor) taslağın notunda.

## Yöntem
- `src/inverter_geri_cozum.py`: her panelli evin inverterinin göreceği seri gerçek ağda üretilir (`sahte_kayit.gercek_trafo`; aynı yük, ışınım, OG; 14 gün × 5 dk). İnverter **yalnız gündüz** kayıt tutar (ışınım > STC'nin %2'si [Yorum]); gece uyur. Geri çözüm yalnız inverterin bildiğiyle: kendi ev gerilimi, kendi panel gücü, saat.
  - **Bara:** sabah ilk değer = her gün ilk uyanık adımdaki gerilim, 14 günün ortancası. Ayrıca gündüz doğrusu V = a + s × P_kendi'nin kesişimi a.
  - **Salınım:** s (V / kW kendi paneli), gündüz doğrusunun eğimi; günden güne oynaklığı.
  - Gerçekle kıyas: hata = tahmin − `v0` (trafonun boşta gerilimi, modelin bilinmeyeni).
- **Uçtan uca:** `sahte_kayit.kayit_uret(..., inv_bara=)`: kayıttaki inverter barası gerçek + gürültü yerine benzetimde geri çözülmüş sabah ilk değer (rastgele akış aynı; diğer kayıtlar değişmez). `basvuru.py`: `hp['inv_bara_hata']` varsa motor barayı `b − hata` diye ölçülmüş hata dağılımından çeker (yoksa eskisi gibi ±U). `basvuru_testi.py --inverter-bara <json> [--bara-hata <json>]`. Sağlama: bayraksız koşum 1–10'da önceki tabloyla birebir.
  - **R0:** bugünkü sahte kayıt (bara = gerçek ± U), motor iki kat varsayar (±2 V) — PR #22'nin tablosu.
  - **R1:** kayıttaki bara gerçek geri çözümden, motor değişmedi.
  - **R2:** R1 + motor bara hatasını **geliştirme 1–10'da ölçülen** dağılımdan çeker (1.148 ev; yöntem değişikliği, ayar yalnız 1–10'dan).
- Geliştirme 1–10'da kuruldu; **sınav 21–30 bir kez** (1 Kasım ~00:30). Hat empedansı kaydı R1 / R2'de de gerçek ± gürültü (aşağıda "Ne kaldı").
- Platform: BUILD 2 klasörü, Mac, Python 3.12.13; üretici 1.3 şehirleri (K_YUK 1,47); taban PR #22 (858a999).

## Sonuç 1: geri çözümün hatası [Hesap; farazi şehir, gösterim]
| | Geliştirme 1–10 (1.148 ev, 276 trafo) | Sınav 21–30 (1.479 ev, 269 trafo) |
|---|---|---|
| Bara, sabah ilk değer: hata ortancası | **−0,79 V** | **−0,97 V** |
| P10 … P90 | −2,15 … −0,28 V | −2,15 … −0,39 V |
| \|hata\| ≤ 1 V / ≤ 2 V | %62 / %88 | %52 / %87 |
| Kuyruk (1–10): P1 / P5 / en düşük; pozitif hata | −5,4 / −3,3 / −9,8 V; 18/1.148 | — |
| Hat ucundaki evler (yer > 2/3): ortanca, ≤ 1 V | −0,85 V, %58 | −1,03 V, %48 |
| Gündüz doğrusu kesişimi: ortanca, ≤ 1 V | −1,45 V, %27 | −1,61 V, %18 |
| Salınım eğimi, günden güne oynaklık (std ÷ ort): ortanca / P90 | %23 / %100 | %21 / %106 |
| PR #20'nin sakin anı (05:00–06:30) adımlarında inverter uyanık | %68 | %65 |

- **Hata hep aynı yönde: geri çözülen bara gerçekten düşük.** Sabah ilk değerde ev zaten yük çekiyor (gerilim düşümü), güneş henüz zayıf. Modelin varsayımı ±1 V'ta ortalanmış düz bir hata; gerçekte ortanca ~1 V aşağıda ve uzun bir alt kuyruk var (evlerin ~%12'sinde 2 V'tan fazla).
- **Bu güvensiz yön:** bara düşük sanılırsa model gerilim payını olduğundan büyük görür, fazla "evet" der.

## Sonuç 2: motor uçtan uca, sınav 21–30 (bir kez) [Hesap; farazi, sahte kayıt, gösterim]
Satır = kayıtların gerçek hata düzeyi (diğer kayıtlar için); motor iki kat varsayar. Yanlış evet: evetlerin gerçekte aşan payı; parantezde 95% aralık (Wilson, evetler bağımsız sayılarak; değiller) ve yanlış evetli trafo / evet veren trafo.

| Kayıtlar | R0 bugünkü sahte kayıt | R1 gerçek geri çözüm, motor aynı | **R2 gerçek geri çözüm, motor ölçülmüş hatayla** |
|---|---|---|---|
| Yarı — hemen evet | %10,7 | %11,3 | %10,0 |
| Yarı — yanlış evet | %0,1 (1/766) | %0,2 (2/810) | **%0,0 (0/720)** (%0–0,5) |
| Beklenen — hemen evet | %9,7 | %10,4 | %9,5 |
| Beklenen — yanlış evet | %0,0 (0/694) | %0,9 (7/749) | **%0,3 (2/680)** (%0,1–1,1; 2/82 trafo) |
| İki kat — hemen evet | %10,1 | %10,8 | %9,6 |
| İki kat — yanlış evet | %1,9 (14/722) | **%2,7 (21/772)** (%1,8–4,1; 11/102 trafo) | **%1,3 (9/692)** (%0,7–2,5; 5/93 trafo) |
| Harita yanlış evet (yeşilse ilk iki) | ≤ %1,5 | ≤ %1,7 | ≤ %0,7 |
| Yanlış yeşil | 0 | 0 | 0 |

Geliştirme 1–10 aynı yön: iki kat kayıtta yanlış evet R0 %1,1 → R1 %1,7 (15/874) → R2 %0,4 (3/784); beklenen kayıtta %0,7 → %1,0 → %0,6; hemen evet R0 %11,3 → R2 %10,7.

## Bulgular
1. **Gerçek geri çözümle motorun bugünkü varsayımı yetmiyor:** kayıtlar iki kat hatalıyken yanlış evet %1,9 → %2,7 (sınır %2 aşılıyor, 11 trafoda), beklenen kayıtta 0 → %0,9. Sebep bara tahmininin sistematik olarak düşük çıkması. PR #22'nin "iki kat varsayım" kuralı bu kaymayı kapsamıyor (±2 V ortalanmış).
2. **Motor ölçülmüş hata dağılımını kullanınca yanlış evet düşüyor:** aynı gerçekçi kayıtlarla iki kat düzeyde %2,7 → %1,3, beklenende %0,9 → %0,3, yarıda 0. Bedel: hemen evet %10,8 → %9,6 (iki kat), %10,4 → %9,5 (beklenen). Yanlış yeşil her yerde 0.
3. **Hâlâ "güvenle %2 altında" değil:** iki kat satırında aralığın üst ucu %2,5 (5 trafo). Tüzük madde 6 ölçüsüyle (~150 bağımsız noktada 0 ihlal) kapı söylenemez [Yorum].
4. **PR #20'nin sakin anı (05:00–06:30) inverter için kısmen yok:** adımların üçte birinde inverter uyuyor; PR #20'deki bara ±1 V varsayımı ve sakin an tanımı iyimser. Doğru kullanım sabah ilk değer + ölçülmüş kayma.
5. **Salınım eğimi günden güne çok oynuyor** (ortanca %21–23, P90 ~%100): tek günlük kayıtla hat empedansı ±%20'yle çözülmez; 14 günlük doğru gerekir.

## Ne kaldı
- **Hat empedansının geri çözümü** (eğim → eşdeğer boy) yapılmadı: eğimi boya çevirmek için hattaki diğer panellerin yeri ve fazı gerekiyor (kayıtta %95'i var); R1 / R2'de empedans kaydı hâlâ gerçek ± %20 / %40. Bara kayması empedans tarafında da varsa sonuç daha kötü olabilir.
- Ölçülmüş bara hatası farazi şehirden; gerçekte pilotta (Faz 10, P6 inverter kaydı + akıllı priz gece seviyesi aynı evde) ölçülmeli. Gece seviyesi bilinirse sabah kayması doğrudan ölçülür.
- PR #20 betiği (`pv_acilma.py`) değiştirilmedi; gerçekçi sürüm bu betik ve PR #22 motoru.

## Ek (1 Kasım ~00:45): ham özet kayda, çözüm motorda (karar masası 00:27); hat boyu çevirici tutmadı
**Neden:** karar masası 00:27 (Civan'ın notu): kayıtta türetilmiş değer değil inverterin ham kaydı olsun, bara ve hat boyu motorun içinde çözülsün; PR #19 okuyucusu buna bağlansın. Ölçü: inverterli trafolarda yeşil / bayrak / renksiz ve yanlış yeşil.

**Yöntem:**
- `inverter_kaydi.geri_coz(veri)`: gerçek kayıt ve benzetim için tek fonksiyon. Ham özet: bara ölçümü (her günün ilk geçerli değerinin ortancası) ve eğim (gündüz gerilim ↔ kendi panel gücü doğrusu, V/kW). Okuyucu güç sütununu da arar (W → kW); yoksa eğim boş. `inverter_geri_cozum.py` aynı fonksiyonu kullanır (1–10'da önceki bara ve eğimle 1.148 evde birebir).
- Sözleşme §7: yeni satır türü `inverter_ham` (`bara_olcum_V;egim_V_kW`); eski `inverter` (türetilmiş) deneme için durur. Yazılıp okununca 36 satırda fark 0.
- Motor (`basvuru.py`): `inverter_ham` varsa bara = ölçüm − hata, hata 1–10'da ölçülen nicelik dağılımından (`INV_BARA_HATA_Q`, 1.148 ev). Hat boyu için çevirici `inverter_boy_ham` (eğim × kendi kWp → trafonun payı düşülür → hattın kayıtlı panelleri ve direnciyle boy).
- **Çevirici 1–10'da tutmadı** (olumsuz sonuç): gerçek ÷ ham boy ortancası 0,29; düzeltme sonrası hata P10–P90 ×0,30 … ×2,63, ±%20 içinde %19, ±%40 içinde %32 (21–30'da ×0,27 … ×2,72, %18). Hat boyu kaydı (±%15) bundan iyi. Sebep [Yorum]: tek fazlı evde gerilimi kendi fazı ve nötr belirliyor, diğer panellerin fazı ve yükler eğimi oynatıyor; dengeli üç faz sadeleştirmesi taşımıyor. Bu yüzden çevirici **kapalı** (`INV_BOY_C = None`): inverterli hatta da hat boyu kaydı ve model-sapma kalır. Ham özetteki eğim kayıtta durur; daha iyi bir çözüm (motor çekilişlerini gözlenen öğlen yükselmesine göre tartmak) sonraki iş.
- **R3:** kayıt `inverter_ham`, motor barayı ölçülmüş hatayla, hat boyunu kayıttan. 1–10'da kuruldu; **sınav 21–30 bir kez** (~00:43). İnverterli trafo = "beklenen" kaydında en az bir inverter olan (her satırda aynı alt küme).

**Sonuç: sınav 21–30 (bir kez)** [Hesap; farazi, sahte kayıt, gösterim]; motor iki kat varsayar. Parantezde R0 (bugünkü sahte kayıt, inverter = gerçek ± gürültü).

| Kayıtlar | Hemen evet | Yanlış evet | 95% aralık | Yanlış evetli trafo |
|---|---|---|---|---|
| Yarı | %7,9 (%10,7) | 0/568 | %0–0,7 | 0/69 |
| Beklenen | %7,8 (%9,7) | %0,2 (1/558) | %0,03–1,0 | 1/74 |
| İki kat | %8,0 (%10,1) | %0,7 (4/576) (%1,9) | %0,3–1,8 | 2/76 |

Yanlış yeşil her satırda 0. Geliştirme 1–10: hemen evet %9,7 / %9,1 / %9,3; yanlış evet 0/705, 2/663, 1/681.

İnverterli trafolarda panel katmanı (aday evi olan 156 trafo; ADR-0017; bayrak = bugün aşma olasılığı ≥ 0,7):

| Görünüm | Yeşil (yanlış) | Bayrak (gerçekte dolu) | Renksiz |
|---|---|---|---|
| Kayıtsız (resmi) | 0 (0) | 20 (14) | %87 |
| Kayıtlı, yarı | 3 (0) | 9 (9) | %92 |
| Kayıtlı, beklenen | 1 (0) | 15 (10) | %90 |
| Kayıtlı, iki kat | 3 (0) | 13 (9) | %90 |

Geliştirme 1–10 (141 trafo): resmi 4 (0) / 14 (11) / %87; kayıtlı 6–8 (0) / 14–15 (12–14) / %84–86. R0 1–10: kayıtlı 6–9 yeşil.

**Bulgular (ek):**
6. **Gerçekçi inverter kaydıyla motor güvenli:** iki kat hatalı kayıtta bile yanlış evet %0,7 (aralık üst ucu %1,8), yanlış yeşil 0. Bunun bedeli hemen evet: %10,1 → %8,0 (R0'a göre), çünkü inverter artık hattın direncini bildirmiyor ve barayı temkinli (ölçülmüş kaymayla) veriyor.
7. **İnverter haritayı açmıyor:** inverterli trafolarda yeşil 0 → 1–3 (sınav), 4 → 6–8 (geliştirme); bayrak sayısı bazen düşüyor ama isabeti artıyor. PR #20'deki "her panelli trafoda bir inverterle yeşil %5 → %10" sonucu iyimser uçtu (bara ±1 V ve hat empedansı ±%20 doğru varsayılıyordu); gerçekçi hâlde (inverter panelli evlerin %20'sinde, bara ölçülmüş kaymayla, empedans çözülemiyor) tutmuyor. Sunum / jüri cümlesinde kullanılmamalı [Yorum].
8. **Hat empedansı tek inverterden bu yöntemle çözülmüyor** (olumsuz sonuç, yukarıda). Muhittin 5B'nin bara yarısı çalışıyor (ölçülmüş kaymayla), empedans yarısı bu sadeleştirmeyle çalışmıyor.

## Karar (karar masası 00:39)
Mac tekrarı birebir. (1) Motor inverter barasını **yalnız ölçülmüş kayma dağılımıyla** kullanır; dağılım yoksa inverter satırı bara için hiç kullanılmaz (kademe kaydı ya da 244–252 V). R1 yolu (gerçek geri çözüm + ölçülmemiş ±U) kapandı: gerçek kayıt `inverter_ham` yolundan gider ve barası yalnız ölçülmüş kaymayla kullanılır (`INV_BARA_HATA_Q` yoksa hiç). Türetilmiş `inverter` satırının ±`inv_bara_v`'si yalnız sahte kayıt içindir (değeri gerçek ± o gürültü), kodda açıklama satırıyla ayrıldı (karar masası 00:49; 00:39'un "geri dönüş kalksın" düzeltmesi 00:49'a göre bu ayrıma çevrildi). Bayraksız `basvuru_testi.py` PR #22'nin tablosunu birebir verir. (2) Deneme şehirlerinde sonuç R2 / R3. (3) **Pilot şartı:** canlıda inverter barasına dayanan "hemen evet" ancak pilotta aynı evde, aynı hafta P6 inverter kaydı ve P7 priz gece seviyesi yan yana ölçülüp kayma gerçek veriden çıkınca; o zamana kadar "önce ölç". Faz 10 kartına satır eklendi. Hat empedansı geri çözümü şimdilik yok (eğim çok oynuyor; gerçek pilot verisi beklenir).

## Düzeltme (karar masası 01:22, TEST'in eksisi)
- **Eksi:** eski tür (türetilmiş) `inverter` satırının gerçek kayıtta kullanılmasını kod engellemiyordu; motor bu satırdan bara yanında hat boyunu da (±%20) alıyor, §7 bu türü geçerli sayıyordu. **Düzeltme:** `sahte_kayit.kayit_uret` kayda `kaynak = 'sahte'` yazar; `kayit_oku(yol, kaynak='gercek')` türetilmiş satırı gerçek kayıtta atlar ve UYARI basar (sahte dosya için `kaynak='sahte'`); motor (`ag_kur_kayitli`) kaynağı sahte olmayan kayıtta türetilmiş satırı görürse hata verir. §7: türetilmiş tür "yalnız deneme". Sınandı: 36 türetilmiş satır gerçek diye okununca 0'a iner (UYARI), sahte diye okununca 36; elle verilen gerçek kayıtta motor reddeder.
- **Gerçekçi rakam:** PR #22'nin "hemen evet %3,8 → %10,5"i ve iki kat varsayımla %9,7–10,1, inverter kaydını gerçek ± gürültü sayıyordu (bara ±1–2 V, hat boyu ±%20–40 doğru). Ham özet yolunda (R3) hemen evet **%7,8–8,0** (sınav 21–30). Kayıtlar gelirse söylenecek rakam "%3,8 → ~%8"; ROADMAP Faz 9'a yazıldı.

## Düzeltme ve üretici 1.5 ile yeniden koşum (karar masası 02:1x, TEST'in eksisi)
- **Eksi:** `sahte_kayit.py` şehrin "gerçek" ağını o anki `sehir_uret.py` ile yeniden kuruyor, şehrin hangi üreticiyle yapıldığına (`ayar.json` `uretici_surumu`) bakmıyordu. Main üretici 1.5'e geçince 1.3 şehirlerinde ağ sessizce değişiyordu (TEST: 40 trafonun 12'sinde kVA farklı; BUILD 2: kVA, hat ya da panel sayısı 24/40'ta farklı). Etkilenen: `sahte_kayit`, `basvuru_testi`, `inverter_geri_cozum`, `guvenli_uc --kayitli / --konum`.
- **Düzeltme:** `gercek_sehir()` şehrin üretici sürümünü `sehir_uret.URETICI_SURUMU` ile karşılaştırır, farklıysa `YenidenKurmaHatasi` ("bu şehir üretici 1.3 ile yapıldı; yeniden kurma 1.5 ile tutmaz"); yeniden kurulan ağı `trafolar.csv` ile (kVA, hat sayısı, panel sayısı) karşılaştırır, uyuşmazlıkta durur. Bilerek zorlamak için açık bayrak `--surum-zorla` (dört betikte; yalnız uyarır). Sınandı: 1.3 şehri bayraksız durdu; zorlanınca iki uyarı (sürüm, 24/40 trafo); 1.5 şehri hatasız, yeniden kurma 38/40 birebir.
- **Yeniden koşum, üretici 1.5** (main'in üreticisiyle BUILD 2 klasöründe sıfırdan; `sablon.py`, `kac_ev_olasilik.py` bu dalın koduyla, güven şartı var): bara kayması 1–10'da yeniden ölçüldü, `INV_BARA_HATA_Q` güncellendi (ortanca **−0,62 V**, P10–P90 −1,47 … −0,15 V, ≤ 1 V %76; 1.3'te −0,79 V idi). Hat boyu çevirici yine tutmuyor (×0,29 … ×2,60). Resmi panel sınavı artık **31–40** (dokunulmamış 1.5); 21–30 1.3'te kaldı. **Sınav 31–40 bir kez** (~02:17):

| Kayıtlar (motor iki kat varsayar) | R0 türetilmiş inverter (yalnız sahte): hemen evet / yanlış evet | R3 ham özet: hemen evet / yanlış evet |
|---|---|---|
| Kayıtsız (bugün) | %4,6 / 0/326 | — |
| Yarı | %10,8 / 1/762 | %8,9 / 1/633 |
| Beklenen | %11,0 / 2/783 | **%8,8 / 0/622** |
| İki kat | %10,6 / 9/751 = %1,2 (aralık %0,6–2,3; 3 trafo) | **%8,3 / 0/591** |
| Kusursuz bilgi | %18,7 / 10/1.326 | — |

Geri çözüm hatası 31–40: ortanca −0,53 V, P10–P90 −1,43 … +0,06 V, ≤ 1 V %80. İnverterli 165 trafoda (aday evi olan): kayıtsız yeşil 6 / bayrak 21 (15 dolu) / renksiz %84 → kayıtlı yeşil 4–8 / bayrak 24–28 (19–24 dolu) / renksiz %80–82; yanlış yeşil 0. Geliştirme 1–10 (1.5): R0 beklenen %10,4 / 3/761, iki kat %10,4 / 2/761; R3 %8,9 / 2/651 ve %8,9 / 2/650. Harita politikası (yeşilse ilk iki) R0 iki kat kayıtta 4/168 (%2,4; türetilmiş inverter yolu, yalnız sahte), R3'te 0/138.
- Sonuç değişmedi: gerçekçi inverter yolunda hemen evet ~%8–9, yanlış evet sınırın güvenle altında; inverter haritayı açmıyor; hat boyu inverterden çözülmüyor.
- **Yeniden kurma sağlaması, üretici 1.5 (karar masası 02:2x sorusu: TEST 40/40, BUILD 2 38/40):** 20 şehirde yapı 800/800 aynı, `kac_ev_gercek` **784/800** birebir (1–10: 394, 31–40: 390; şehir 3, 4, 6–8, 31–33 40/40, şehir 1 38/40); farklılar 1–2 ev. Sebep (sehir-001 T20, T31'de doğrulandı): ağ birebir — üreticinin kendi hesabı yeniden koşulunca dosyadaki sayı aynen çıkıyor —, ama `gercek_trafo` kritik 6 adımı `yuk_5dk.csv`'nin 0,1 V'a yuvarlanmış geriliminden seçiyor; eşitlenen adımlar başka sırayla gelince kritik anlardan biri değişiyor. TEST'in 40/40'ı büyük olasılıkla 40/40 tutan bir şehirden [Yorum]. Etki: gerçekte aşar kontrolü trafoların ~%2'sinde bir iki ev oynar; tablolardaki oranlara etkisi küçük. Düzeltmek için gerilim serisi yuvarlanmadan yeniden benzetilmeli (trafo başına 14 gün × 288 çözüm; testi birkaç kat yavaşlatır), şimdilik yapılmadı.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas ~00:25 | geri çözüm v1 (sabah ilk değer, gündüz doğrusu) | 1 | bara ±1 V'ta çözülür | ortanca −0,82 V, ≤ 1 V %65 | 1–10 |
| 1 Kas ~00:26 | aynı | 1–10 | aynı | ortanca −0,79 V, P10 −2,15, ≤ 1 V %62; hep aşağı | uçtan uca |
| 1 Kas ~00:28 | motor v1.1 (iki kat) + R1 / R2 (bara hatası 1–10'dan) | 1–10 | R1 yanlış evet artar, R2 geri indirir | iki kat: %1,1 → %1,7 → %0,4 | 21–30 bir kez |
| 1 Kas ~00:30 | aynı | 21–30 | aynı | geri çözüm −0,97 V; iki kat: R0 %1,9 → R1 %2,7 → R2 %1,3 (aralık %0,7–2,5); hemen evet %10,1 → %9,6; yanlış yeşil 0 | karar masasına (PR) |
| 1 Kas ~00:43 | motor v1.2: `inverter_ham`, bara 1–10 nicelikleriyle, boy çevirici kapalı (1–10'da ×0,30–2,63) | 21–30 | gerçekçi inverterle yanlış evet < %2, inverterli trafoda açılır | iki kat 4/576 (%0,7; üst %1,8); hemen evet %8,0; inverterli yeşil 0 → 1–3, yanlış yeşil 0 | karar masasına (PR) |
| 1 Kas ~02:17 | motor v1.3: sürüm / sağlama kontrolü, `INV_BARA_HATA_Q` üretici 1.5 1–10'dan | 31–40 (1.5) | 1.5'te de gerçekçi inverterle yanlış evet < %2 | R3: 0/622, 0/591; hemen evet %8,3–8,9; kayma −0,53 V; inverterli yeşil 6 → 4–8 | TEST'e |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
