# 2026-10-31 — Volkan (+ Claude, BUILD): Faz 3 kaç ev, olasılıklı deneme

## Hipotez / amaç
Tek denklemli `kac_ev.py` bilinmeyen her şey için tek bir "en kötü" değer seçiyor. [Varsayım envanteri](2026-10-31-volkan-faz3-varsayimlar.md) bu değerlerin kırmızıyı yalnız kaydırdığını, sıralamayı düzeltmediğini gösterdi. Ek olarak kaç ev hatası 3,5 ev (eşik ≤ 2).

Fikir (Volkan, 31 Ekim akşam):
- Her trafonun ağını Kıb-Tek'in bildikleriyle yeniden kur.
- Bilinmeyenleri aralığından yüzlerce kez çek, her seferinde ev ev benzetimi koş.
- Kararı olasılıkla ver.

Bütün rakamlar farazi şehirde: **gösterim**.

## Yaptıklarım
- `src/kac_ev_olasilik.py` (dal `kac-ev/olasilik`, PR #13'ün üstünde). Trafo başına 40 çekiliş; ev ev yük akışı eski benzetimin `solve()`'u. Şehir başına 3–5 sn.
- **Bilinenler:** abone sayıları, hat sayısı, en uzun ve toplam hat boyu, kablo, kVA, panel sayısı ve toplam gücü, Faz 2'nin öğlen yükü bandı ve güveni.
- **Çekilenler ve aralıkları.** Envanterden alındı; şehir üreticisinin kendi değerlerinden değil (ADR-0009):

| Bilinmeyen | Aralık | Dayanak |
|---|---|---|
| Bara gerilimi | 244–252 V düz | karar masası 16:27 bandı; Kıbrıs BULAMADIM |
| Öğlen orta gerilim değişimi | −%0,4 … +%0,8 | UKPN (öğlen ~1 V düşük) ile eski benzetim arası [Yorum] |
| Abonenin hattı | rastgele hat | [Yorum] |
| Diğer hatların boyu | toplam − en uzun, rastgele bölünür | [Yorum] |
| Büyük abonelerin yeri | yarı yarıya trafoya yakın ya da rastgele | veri yok [Yorum] |
| Panellerin hangi evde olduğu | üçte bir çekilişte hattın ucuna toplanmış, yoksa düz | UKPN: 6 hat ucu evin 2'sinde paneller uçta [Hesap, PR #11] |
| Tek fazlı abonenin fazı | faz ağırlığı 1 ± U(0, d); d kentsel 0,3, kırsal 0,5 | UKPN dengesizlik kentsel P84 %30, kırsal ~%50 |
| Üç fazlı abone payı | konut %0–20, ticari I %0–40, diğerleri üç faz | [Yorum] |
| Trafonun öğlen yükü | Faz 2 P10–P90 bandından log-normal; ölçülü trafoda ölçülen | Faz 2 |
| Yükün abonelere dağılımı | tarife enerjisi × log-normal fark (σ 0,3) | Kıb-Tek 2023 + [Yorum] |

- **Her çekilişte:**
  - Bugün aşılıyor mu: öğlen güneşi, en düşük yük, yeni panel yok; 259 V ya da kVA.
  - Bekleyen panelsiz konutlar rastgele sırayla 6,5 kW alırsa kaçı sığar. Sığmayan atlanır; cevap anahtarıyla aynı tanım.
  - İlk iki başvuru sığıyor mu.
- **Renk** (ADR-0010 olasılıkla):
  - kırmızı = bugün aşma olasılığı ≥ 0,5;
  - yeşil = ilk iki başvurunun sığma olasılığı ≥ 0,98 (canlı bütçe %2; marj 1 ev) ve güven yüksek;
  - diğerleri sarı.
- **Sayılar:** karamsar = çekilişlerin P10'u, orta = ortancası, iyimser = P90'ı.
- **Ayar disiplini:** şehir 1–10'da iki değişiklik yapıldı, ikisi de gerçek veriye dayalı. Sınav şehirleri 11–20 en sonda bir kez ölçüldü.
  - İlk koşuda paneller hep düz dağılıyordu. UKPN'in "6 hattın 2'sinde uçta" bulgusu eklendi.
  - Büyük abone yeri, veri olmadığı için iki duruma eşit bölündü.
  - Eşikler (0,5 ve 0,98) ilkeden geldi, ayarlanmadı.

## Sonuç

### Sınav şehirleri 11–20 (bir kez; 347 trafo, 74'ü dolu)

| | Tek denklem, kırmızı (b) | **Olasılıklı** | %40 kuralı |
|---|---|---|---|
| Yeşil ("yer var") | %6 (21) | **%28 (97)** | %82 (284) |
| **Yanlış yeşil** | 0/21 | **0/97** (her şehirde 0) | 41/284 (%14) |
| Kırmızı | %31 | %9 | — |
| Yanlış kırmızı | %42 | **%23** | — |
| Dolu trafonun kırmızı denen payı | 61/74 | 23/74 (kalanı sarı) | — |
| Sarı | %63 | %63 | — |
| Kaç ev hatası (tavansız, ortanca) | iyimser 3,5 / karamsar 9 | **orta 2** / P10 2 / P90 3,5 | — |
| Gerçek, karamsar–iyimser aralığında | %79 | %83 | — |

- Geliştirme şehirleri 1–10'da aynı yön:
  - yeşil %26, yanlış yeşil 0/93;
  - kırmızı %8, yanlış kırmızı %26, dolu yakalanan 20/56;
  - sarı %66, kaç ev hatası 2.
- **Kim yeşil** (sınav): otel %83, çarşı %77, yurt %50, şehir konutu %8; köy ve sulamada yok.
  - Tek denklemde konut trafosuna hiç yeşil yoktu. Şimdi var ve hiçbiri yanlış değil.
- **Olasılıklar gerçekle tutuyor mu?** Sınavda olasılık kovasına göre gerçekte aşan pay:
  - 0,3–0,5 → %48;
  - 0,5–0,7 → %74;
  - 0,7–0,9 → %88.
  - En düşük iki kovada eksik: %0–10 → %4 (243 trafo); %10–30 → %51 (43 trafo). Bu ikincisi kaçan dolu trafoların yığıldığı yer.
- **Kırmızı eşiğinin bedeli** (sınav, bilgi, ayarlanmadı):
  - 0,3 → kırmızı %19, yanlış %40, yakalanan 40/74;
  - 0,5 → %9, %23, 23/74;
  - 0,7 → %3, %10, 9/74.

### Okuma
- **+ Yeşil 4–5 katına çıktı, yanlış yeşil yine sıfır.**
  - Tek denklem "yeni ev hattın ucunda ve tek fazda" diyerek konutta hiç yeşil vermiyordu.
  - Olasılıklı hesap aynı riski çekilişle görüyor; yalnız bütün 40 çekilişte iki başvuru da sığıyorsa yeşil diyor.
- **+ Kaç ev sayısı eşiğe indi** (ortanca hata 2 ev, ROADMAP ≤ 2). Aralık gerçeği %83 kapsıyor.
- **+ Yanlış kırmızı %42 → %23.**
  - Bedeli: dolu trafoların üçte biri kırmızı, gerisi sarı. Sarı "önce ölç" demek, onay değil (karar masası 17:26); zarar yok.
  - Sarı oranı değişmedi (%63, hedef ≤ %30). Bunu ancak yeni bilgi düşürür: bara gerilimi, panelin adresi.
- **− Olasılık düşük uçta iyimser.** %10–30 dediği trafoların yarısı gerçekte aşıyor.
  - Sebep: deneme şehrinin içindeki iki varsayım hesabın aralıklarından daha kötü. Biri UKPN'le çelişen +%0,8 öğlen yükselmesi; öbürü panellerin uca kayması.
  - Aralıkları üreticiye uydurmadım (ADR-0009). Gerçekte nasıl olduğunu İngiltere'nin 6 hattı ve pilot söyler.
- **? Bu sonuç farazi şehirde.**
  - Aralıklar gerçek veriye dayandırıldı, üretici değerine değil. Ama yapı (ev ev benzetim) şehir üreticisinin kullandığının aynısı. Bu yüzden deneme şehrinde olduğundan iyi görünebilir.
  - Canlıya geçmeden yeşil kuralı gerçek veride geri-test edilmeli (ADR-0010 madde 3): İngiltere 6 hat, sonra pilot.

## Karar / sıradaki adım
- PR: `kac-ev/olasilik` (taban `kac-ev/ilk-surum`). Tek denklemli `kac_ev.py` olduğu gibi duruyor; olasılıklı hesap ayrı dosya ve ayrı çıktı (`kac_ev_olasilik.csv`, sözleşmede değil).
- Karar masasına (volkan.md):
  - Faz 3'ün resmi hesabı olasılıklı olsun mu?
  - Olursa sözleşme §6'ya sütunlar gerekir (`p_bugun_asar`, `p_iki_ev_sigar`, `kac_ev_orta`).
  - Civan'ın paneli ve Can'ın sınavı buna göre değişir.
- Kırmızı eşiği 0,5 ilkeden ("aşma olasılığı daha yüksek"). Değiştirmek karar masasının işi; yukarıdaki tablo bedelini gösteriyor.

## Ek girdi — 31 Ekim 18:43: hat boyu belirsizliği ve kol yapısı (İngiltere geri-testinden, Volkan)

**Neden.** Gerçek veri geri-testinde ([günlük](2026-10-31-volkan-faz3-ukpn-geritest.md)) iki şey çıktı:
- Hat boyu kesin sayılınca İngiltere'nin 6 hattından 4'ünde ölçülen yükselme hesabın %98 sınırının altındaydı; boy belirsiz sayılınca 5'inde.
- Kaçan hatta (Bancroft) ev, yüksüz ama panelli bir koldaydı.

**Eklenen iki aralık:**
- Hat boyu × e^U(−0,47; 0,47) ≈ ×0,6–1,6 [Yorum; Kıb-Tek kaydı BULAMADIM].
- Çekilişlerin altıda birinde panelli evler, trafodan en uzun hat boyunda, yüksüz ayrı bir kolda [Hesap: UKPN 6 hattın 1'i].
  - Bu oran aynı 6 hattan geldiği için o hatlarda sınanamaz.

| | Önce (11–20) | Sonra (11–20, bir kez) | Sonra (1–10) |
|---|---|---|---|
| Yeşil | %28 | %25 | %23 |
| Yanlış yeşil | 0/97 | **0/87** (her şehirde 0) | 0/83 |
| Kırmızı | %9 | %13 | %9 |
| Yanlış kırmızı | %23 | %27 | %28 |
| Dolu trafonun kırmızı denen payı | 23/74 | **32/74** | 23/56 |
| Sarı | %63 | %62 | %68 |
| Kaç ev hatası (orta, tavansız) | 2 | 2 | 1 |
| Gerçek, P10–P90 aralığında | %83 | %86 | %86 |
| Bugün aşma olasılığının sıra uyumu | 0,75 | 0,79 | 0,75 |

- Olasılıklar daha iyi tutuyor (sınav, kova → gerçekte aşan): 0,3–0,5 → %53, 0,5–0,7 → %62, 0,7–0,9 → %91. Düşük uçta (%10–30 → %43) hâlâ iyimser.
- Yeşil bedeli küçük: %28 → %25. Kazanç: dolu trafoyu kırmızı görme 23 → 32.
- Yeşiller (sınav): otel %83, çarşı %65, yurt %47, şehir konutu %4, köy %2.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
