# 2026-10-31 — Gerilim fiziği gerçek veride: İngiltere UKPN, yaz 2014, 1 dakika

**Etiket: gerçek veri — İngiltere (UKPN), yaz 2014, 1 dk.** Kıbrıs verisi değil. Taşınan şey fizik (direnç, akım, nötr), rakam değil.

Kod: [src/ukpn_test.py](../../src/ukpn_test.py). Veri ve yapı notları: [data/raw/ukpn-pv-dogrulama/KAYNAK.txt](../../data/raw/ukpn-pv-dogrulama/KAYNAK.txt). Görev: [brif](../istek/brif-ukpn-gerilim.md). Oturum 16:00–16:30, zaman kutusu 3 saat; brifin beş adımı bitti.

## Hipotez / amaç
Bizim ev ev yük akışımız (`trafo_bos_kapasite.py` `solve()`), panel basınca hat ucundaki evin geriliminin ne kadar yükseldiğini doğru büyüklükte hesaplıyor mu? Hedef [Yorum, brif]: model ÷ ölçülen 0,7–1,5.

Bu, [ADR-0002](../decisions/adr-0002-gerilim-ilk-surumde.md)'nin ("Kıbrıs'ta önce gerilim bağlar") dayandığı fiziğin ilk gerçek veri sınaması. Faz 2'nin İspanya sınavında gerilim ölçümü yoktu.

## Yaptıklarım
1. **Yapı.** Veri notları (docx) ve cihaz listesi (xlsx) okundu. Altı hat ucu evin fideri ve fazı veriden bulundu: ev − bara farkı hangi fiderin hangi fazındaki güçle en güçlü ters ilişkideyse o [Hesap]. Beş evde faz raporun Tablo 14'üyle aynı. YMCA'da veri açıkça A diyor (r = −0,89), rapor C diyor. Veri notları zaten "uçtaki A fazı trafodaki A olmayabilir" uyarısı veriyor [Kaynaklı: Dataset Notes].
2. **Hat boyu ve kablo.** Hat boyu raporda, veri notlarında ve cihaz listesinde yok: **BULAMADIM** (aranan: "length", "metres", "mm2", "cable", "feeder", "Netmap", ekler A–D). Kablo tipi dört sitede var (185 Al, 120 Al, 0,2 in² Cu) [Kaynaklı: Dataset Notes], ikisinde BULAMADIM. Direnç IEC 60228 tablosundan: 95 / 120 / 185 / 300 mm² Al = 0,320 / 0,253 / 0,164 / 0,100 Ω/km, 20 °C [Kaynaklı: https://mycableengineering.com/conductor-resistance/]; 0,2 in² Cu ≈ 0,142 Ω/km [Hesap]. Nötr = faz (İngiliz yeraltı kablosunda eş kesitli nötr) [Yorum].
3. **Ölçülen yükselme.** ΔV = ev gerilimi − bara gerilimi, aynı faz, aynı dakika. Bara = fiderin trafo çıkışındaki cihazı (1 dk). Zaman damgası GMT [Hesap: üretim 11:00–13:00 arasında tepe yapıyor].
   - Raporun yöntemiyle aynı eğim: Haziran–Ağustos, 11–13, ΔV'nin evin birim üretimine (pu) eğimi. Bu, işlememin doğru olduğunun sağlaması.
   - Güneşli 12 gün: beş hava istasyonunun günlük ışınım ortalamasıyla seçildi (21–22 Haz; 3, 4, 14, 16, 17, 18, 22, 23, 24, 31 Tem) [Hesap]. Bu günlerde öğlen − aynı gecenin (00–04) ortancası = "seviye yükselmesi". Gece referansı cihaz farkını düşürür. Karşılaştırma için aynı ölçü en bulutlu 12 günde (19 ve 28 Haz; 5, 10, 11, 13, 20, 28 Tem; 1, 4, 5, 6 Eyl).
4. **Model.** Tek fider; 30 yük düğümü eşit aralıklı (A, B, C sırayla) + uçta ev [Yorum]. Bara gerilimi ölçülen (trafo empedansı devre dışı). Ev = ölçülen net gücü. Diğer yük = fiderin ölçülen faz gücü − ev, o fazın düğümlerine eşit [Yorum]. Brifteki "faz dağılımı %25/%50" yerine fiderin faz faz ölçümü kullanıldı (elimizde var); faz bilgisi olmasa ne olacağı ayrı varyant ("faz bilgisiz": ev dışı yük üç faza eşit).
5. **Boy bilinmediği için iki yol.**
   - (a) Boy bandı 150–450 m [Yorum: bizim şehir konutu aralığı] × kablo; ölçülen eğim bandın içinde mi?
   - (b) Akşam 17–21 dakikalarından (PV yok, yalnız yük düşümü; 1 dk dönemin bütün günleri) etkin boy kestirildi [Hesap], sonra bu boyla öğlen PV eğimi hesaplandı. Boy öğlen verisini görmez; aynı empedans akşam düşümünü ve öğlen yükselmesini birlikte açıklıyorsa fizik tutarlıdır. Brifteki "ölçülen ΔV'den ters hesap yapma" kuralını böyle yorumladım: sınanan pencereden değil, başka bir pencereden kestirim.
6. **Çapraz sağlamalar (modelsiz):** 20 trafonun bara gerilimi (10 dk, 10 Haz – 19 Kas); müşteri başına gündüz en düşük talep; akşam 17–20 faz dengesizliği.

## Sonuç

### + İşleme sağlaması: raporun ölçtüğü eğimi tutturdum
Ölçülen eğim (V/pu), benim / rapor Tablo 14 [Hesap / Kaynaklı: rapor s.50]: Alverston 2,18 / 2,13; Bancroft 1,21 / 1,13; Forest Road 1,03 / 1,07; Maple Drive East 2,83 / 2,92; Suffolk Road 0,66 / 0,78; YMCA 0,82 / 1,03 (YMCA'da faz farklı). Dördünde fark %8'in altında.

### + Model, altı evin dördünde PV yükselmesini doğru büyüklükte veriyor
Akşamdan kestirilen boyla model ÷ ölçülen PV eğimi [Hesap]:

| Site | Kablo | Akşam boyu (R²) | Ölçülen V/pu | Model V/pu | Model ÷ ölçülen | Faz bilgisiz | Öğlen dakika R² |
|---|---|---|---|---|---|---|---|
| Alverston Close | 185 Al | 289 m (0,61) | 2,18 | 1,12 | **0,52** | 1,03 | 0,66 |
| Bancroft Close | BULAMADIM, 185 [Yorum] | 77 m (0,38) | 1,21 | 0,27 | **0,22** | 0,45 | 0,43 |
| Forest Road | BULAMADIM, 185 [Yorum] | 135 m (0,23) | 1,03 | 0,93 | **0,90** | 0,94 | 0,49 |
| Maple Drive East | 120 Al | 257 m (0,78) | 2,83 | 2,37 | **0,84** | 1,94 | 0,85 |
| Suffolk Road | 0,2 in² Cu | 335 m (0,80) | 0,66 | 0,91 | **1,39** | 0,66 | 0,82 |
| YMCA | 185 Al | 312 m (0,86) | 0,82 | 0,79 | **0,96** | 0,62 | 0,91 |

- Dört site 0,84–1,39 aralığında, hedefin içinde. Altısının ortancası 0,87 [Hesap].
- Akşam düşümüyle kestirilen boylar beş sitede 135–335 m, İngiliz kent fiderleri için akla yatkın [Yorum]; Bancroft'ta 77 m (aşağıda).
- Öğlen dakika dakika: akşam boyuyla model, ölçülen ΔV'nin oynamasının %43–91'ini açıklıyor [Hesap: R²].
- Boy kestirmeden bant: ölçülen eğim 150–450 m bandında beş sitede bandın içinde; Alverston'da bandın üstünde (2,18 > 1,76 V/pu) [Hesap].
- Model − ölçülen ev gerilimi, güneşli öğlen dakikaları: ortanca −0,69…0,00 V, mutlak P90 0,18–1,31 V [Hesap; cihaz farkı akşam kesişimiyle düşüldü]. Cihaz doğruluğu ±%0,5 ≈ ±1,2 V [Kaynaklı: rapor s.51].

### − İki sitede model yükselmeyi yarıdan az gösteriyor: yanlış yeşil yönü
Alverston'da 0,52, Bancroft'ta 0,22. Model düşük derse "yer var" der; bu yanlış yeşil yönüdür. Altı sitenin ikisi (%33) hedefin altında, hiçbiri üstünde değil [Hesap].

Sebep [Yorum, kanıtı var]: model fiderin yükünü ve panellerini hat boyunca eşit yayıyor. Paneller evin bulunduğu kola, hattın ucuna toplanmışsa trafo çıkışındaki net akış küçük kalır ama uçtaki gerilim yükselir. Kanıtlar:
- Öğlen − gece seviyesinde ölçülen − model açığı, 12 güneşli / 12 en bulutlu gün (6 Eyl'e kadar) [Hesap]: Bancroft +0,54 / +0,15 V, Alverston +0,92 / +0,55 V. Açık güneşle büyüyor, yani panelden geliyor (Alverston'da bir kısmı güneşten bağımsız). İyi tutan sitelerde açık iki durumda da sıfıra yakın: Forest Road 0,00 / −0,09, Maple +0,04 / −0,12, YMCA −0,15 / −0,12 V.
- Bancroft'ta akşam düşümü çok küçük (etkin boy 77 m) ama öğlen yükselmesi büyük: ev, yükün olduğu kolda değil, panellerin olduğu kolda.
- UKPN'in kendi ayrıntılı modeli de (gerçek panel yerleriyle) Alverston'u ölçülenin 0,43'ü kadar gösterdi: hesap %0,37, ölçülen %0,87 [Kaynaklı: rapor s.30]. Rapor bunu en uçtaki üç panelin aynı fazda olmasına bağlıyor.

### + Faz bilgisi önemli: olmazsa hata iki yöne de büyüyor
Ev dışı yük üç faza eşit sayılınca oran 0,45–1,94 aralığına yayılıyor (faz bilgisiyle 0,22–1,39) [Hesap]. Maple'da model 1,94 kat abartıyor, YMCA'da 0,62'ye düşüyor. ADR-0002'nin "faz bilinmezse sonuç oynar, renk karamsara göre" kuralını destekliyor; burada gözlenen oynama ~2 kat, ADR'deki ~6 kat üst sınır.

### ? Seviye (öğlen − gece) ölçüsü panel yerine çok duyarlı
Güneşli öğlende geceye göre ölçülen yükselme: Alverston 1,16 V, Bancroft 0,61, Forest Road 0,75, Maple 1,02, Suffolk −0,80 (öğlen hâlâ net 47 kW çekiş var), YMCA 0,25 V [Hesap]. Model ÷ ölçülen: 0,23 / 0,10 / 0,98 / 0,85 / işaret ters / 1,55. Suffolk'ta açık güneşe pek bağlı değil (ölçülen − model güneşli −1,02, bulutlu −0,75 V [Hesap]); sebep gündüz yükünün hat üstündeki yeri [Yorum]. Bu ölçü PV fiziğinden çok hattın yük ve panel dağılımını sınıyor; ana sonuç olarak eğimi aldım (UKPN'in tanımı da bu).

### + Çapraz sağlama 1: bara gerilimi raporla aynı
20 trafo, 10 dk, gece 00–05: ortanca 245,0 V, ss 3,3 V, P84 247,7 V, ortanca + 1 ss 248,2 V [Hesap]. Rapor: ortanca 245 V, ss 3 V, tasarım 248 V [Kaynaklı: rapor s.33–36]. Öğlen 11–13 (Haz–Ağu): ortanca 244,0, P84 247,2, P99 250,6 V. Site ortancaları öğlen 237,3–249,2 V, yani siteler arası 12 V fark [Hesap].

Bizim kurgu: trafo çıkışı 246–250 V düzgün dağılım, ss 1,2 V [Hesap: 4/√12]. İngiltere'deki dağılım bizimkinden ~3 kat geniş [Hesap]. Kıbrıs'ın gerçek dağılımı BULAMADIM.

### + Çapraz sağlama 2: gündüz en düşük talep 205–355 W/müşteri
Güneşli 12 günde 10–16 arası 30 dk'lık en düşük toplam talep, müşteri başına, günlerin ortancası [Hesap]. Fider net gücüne, sitenin panel gücü (Tablo 3) × izlenen evin birim üretimi eklendi [Yorum: brüt talep tahmini]. Bütün fiderleri izli siteler: Alverston 205, Bancroft 279, Maple 354, Suffolk 311 W; panelsiz Upper Staplefield Common 355 W. Rapor 200–400 W [Kaynaklı: rapor s.37, Low Carbon London]. Bizim şehir konutu 330 W/abone [Hesap, 20 farazi şehir] aralıkta. Kullanılmayanlar: Forest Road 288 W (4 fiderden 3'ü izli, alt sınır), YMCA 83 W (4'ten 2'si), Rampling Court (müşteriler apartman blokları).

### + Çapraz sağlama 3: kent faz dengesizliği %14, bizim üretici daha dengesiz
Akşam 17–20 ortalama faz yükü; dengesizlik = (en büyük faz − ortalama) / ortalama (raporun 30 kW → 12,5 / 8,75 / 8,75 = %25 örneğiyle aynı tanım). Fider başına bütün dönem: kentsel ortanca %14,4, ss %11,2, P84 %30,3 (40 fider); kırsal ortanca %51,4 (3 fider) [Hesap]. Rapor kentsel ortanca %15, ss %10 [Kaynaklı: rapor s.35]. Fider-gün bazında daha oynak: kentsel ortanca %21,4.

Bizim `sehir_uret.py` kuralı (trafo başına faz ağırlığı 0,8–1,2, ev fazı rastgele, hat başına 10–40 ev): ev sayısında ortanca %28,6, P84 %50 [Hesap: aynı kuralın 4.000 denemesi]. Bizim üretici İngiliz kent fiderlerinden ~2 kat dengesiz; gerilim için karamsar, yani güvenli yön [Yorum].

## Sınırlamalar
- Hat boyu BULAMADIM. Etkin boy akşam düşümünden kestirildi; bu bir tutarlılık sınaması, çizimden bağımsız mutlak tahmin değil.
- Hat tek kol ve eşit yayılmış sayıldı [Yorum]; gerçek fiderler dallı. İki sitedeki açık büyük ölçüde bundan.
- Düğüm sayısı duyarlılığı: Maple'da 9 / 30 / 90 düğüm → oran 0,95 / 0,84 / 0,79; Alverston'da 30 / 90 → 0,52 / 0,51 [Hesap].
- Fider eşleşmesi korelasyonla; Forest Road'da iki fider neredeyse eşit (r −0,55 / −0,55, ilk taramada). Akşam R²'si düşük (0,23); boy kestirimi zayıf.
- Suffolk ve YMCA'da panel küçük (0,5 kW); ölçülen eğimin R²'si 0,04 ve 0,22. Rapor da bu iki sitede PV etkisini "zayıf" buldu.
- Ölçüm: cihaz doğruluğu ±%0,5, zaman damgası eşleşmesi kusurlu olabilir [Kaynaklı: rapor s.51]. Mutlak ΔV güvenilmez; eğim ve gece referansı bu yüzden.
- Yaz, 6 ev, 6 trafo. Bu, [validation.md](../method/validation.md)'nin trafo-dışarıda protokolü değil; şablon modelini değil, benzetimin gerilim fiziğini sınıyor. Sınanan pencere (öğlen) kestirim penceresinden (akşam) ayrı.

## İngiltere'de tutuyor ≠ Kıbrıs'ta doğru
- **İngiltere'de sınanan:** tek fazlı panelin faz + nötr üzerinden gerilim yükseltmesi, yük düşümüyle üst üste binmesi, fazlar arası etkileşim. Aynı empedans akşam düşümünü ve öğlen yükselmesini dört hatta birlikte açıklıyor.
- **Kıbrıs'a taşınmayan:** rakamlar. İngiltere 230 V / 253 V, yeraltı Al kablo, eş kesitli nötr, 0,5–4 kW panel. Kıbrıs kurgumuz 246–250 V çıkış, 259 V sınır, havai ABC70/95, ince nötr (54,6 mm², faz 70/95) ve 5 kW panel. Nötr incelince tek faz yükselmesi büyür; bu, İngiltere'de sınanamadı.
- **Sınanmayan:** havai hat, uzun kırsal hat, trafo seviyesinde ters akış, inverterin gerilim tepkisi, Kıbrıs'ın bara gerilimi dağılımı.

## Karar / sıradaki adım
Ne öğrendik [Yorum]:
1. `solve()` fiziği doğru büyüklükte; hat yapısı doğruysa ±%40 içinde. Fiziği değiştirmeye gerek yok.
2. Yanlış yeşil riski fizikten değil hat yapısından: paneller hattın ucuna toplanırsa eşit yayılmış model yükselmeyi 2–4 kat az gösteriyor. `kac_ev.py`'nin karamsar durumu (ADR-0002: tek faz) bekleyen panelleri hattın ucuna ve evin fazına koymalı; renk karamsara göre. Bu ADR-0002'nin içinde, yeni ADR gerekmiyor.
3. Bara gerilimi: İngiltere'de siteler arası yayılım bizim 246–250 V kurgusundan ~3 kat geniş. Kıb-Tek verisi yokken bant genişlesin mi, karar masasına.
4. Faz dengesizliği: bizim üretici kent fiderlerinden daha dengesiz (karamsar). Üretici 1.2'deki "kentsel ±%25" çapası ölçümle uyumlu (kentsel P84 %30) [Hesap].

Sıradaki: karar masası bakar (volkan.md UYARI). PR birleştirilmedi.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
