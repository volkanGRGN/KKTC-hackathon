# Yöntem

Gerekçeler: [ADR-0001](../decisions/adr-0001-sekil-buyukluk-sablon.md), [ADR-0002](../decisions/adr-0002-gerilim-ilk-surumde.md), [ADR-0003](../decisions/adr-0003-rastgele-farazi-sehirler.md), [ADR-0007](../decisions/adr-0007-yillik-fatura-tuketimi-girdi.md) (fatura), [ADR-0008](../decisions/adr-0008-farazi-cesitlilik-saf-tahmin.md) (mahalle farkı, saf tahmin). Kod: `src/sablon.py` (bölüm 0–3, 5), `src/kac_ev.py` (bölüm 4, Faz 3). Sonuçlar ve neden böyle seçildiği: [Faz 2 günlüğü](../log/2026-10-31-volkan-faz2.md).

Kural: model yalnız Kıb-Tek'in bileceğini girdi alır (`trafolar.csv`) ve yalnız ölçülü trafoların yükünü görür (`yuk_5dk.csv`'nin o satırları). Cevap anahtarını okumaz.

## 0. Hangi trafolar ölçülür (öğretici küme)

- Kıb-Tek'in bildiği özellikler (abone karışımı, büyüklük, bölge) standartlaştırılır, trafolar n tabakaya bölünür (k-means), her tabakadan bir rastgele trafo seçilir. Benzer yerlere değil boşluklara ([doğrulama](validation.md) "temsil yanlılığı").
- Abone karışımı enerjiye göre: abone sayısı × o tarifenin abone başına yıllık tüketimi (Kıb-Tek 2023 istatistiği, [Hesap]). Kıb-Tek bunu faturadan bilir.
- **Fatura (sözleşme 1.2):** `trafolar.csv`'de `yillik_tuketim_mwh` varsa her trafonun abone satırı, tarife ortalamasıyla hesaplanan enerjisi faturaya eşit olacak biçimde ölçeklenir: sınıf karışımı abone sayısından, büyüklük faturadan. "Toplam enerji" özelliği o zaman faturadır. Sütun yoksa ya da boşsa (gerçek veri) abone sayıları aynen kullanılır; `--faturasiz` aynı şeyi kıyas için zorlar.
- Ana çalıştırma 40'tan 12; deneyler 5 / 10 / 20, beşer tekrar.
- İlk sürümde tabaka "baskın tarife × bölge × kVA" idi: aynı tarifedeki çarşı ve yurt aynı tabakaya düştü, biri hiç ölçülmedi.

## 1. Şekil: kümeleme

- Ölçülü her trafonun Nisan iş günü ortalama eğrisi (5 dk → saatlik), tepesine bölünür.
- Ward hiyerarşik kümeleme, k = 3–6 (ölçülü < 9 ise 2'den) arasında siluet en yüksek olan; sonra Ward merkezleriyle başlayan k-means.
- Arketip eğrisi (`arketipler.csv`): kümedeki trafoların tepeye bölünmüş eğrilerinin ortalaması, tekrar tepeye bölünür; iş günü ve tatil ayrı. Ad eğriden okunur: `aksam_tepeli`, `gunduz_tepeli`, `duz` (en düşük ÷ en yüksek > 0,55), aynı ad iki kümede `_2`.

## 2. Atama

- Girdiler (standartlaştırılmış): abone karışımı (enerji payı, 7 tarife), büyüklük (toplam enerji, abone sayısı, kVA; log), bölge, panel (kW ÷ kVA), hat (en uzun hat, hat sayısı, yer/direk).
- Çok sınıflı lojistik regresyon (C = 1) → her arketipin olasılığı. `arketip` = en olası; tahmin bütün olasılıklarla ağırlıklı.

## 3. Büyüklük: ölçekleme

- Hedef: bahar öğleni (11–14) en düşük brüt tüketim, 14 günün hepsinde.
- Öğlen en düşük ≈ Σ_sınıf γ_sınıf × abone_sınıf × abone başına yıllık ortalama kW. γ = o sınıfın "öğlen en düşük ÷ yıllık ortalama" oranı; γ ≥ 0, negatif olmayan en küçük kareler (NNLS).
- Göreli hata en küçüklenir (küçük trafo büyük kadar önemli).
- İki kat:
  - Önce bütün ölçülülerle **ortak γ**, tek ortak orana (Σ ölçülen ÷ Σ enerji) çekilerek. Ölçülü kümede hiç olmayan tarife sıfır değil ortak oranı alır.
  - Sonra **küme başına γ**, ortak γ'ya çekilerek (ağırlık 1). Aynı tarifede farklı şekil böyle ayrılır: ticari II'de çarşı dükkânı öğlen tepeli, yurt akşam tepeli.
- Ölçülmeyen trafo: Σ_k olasılık_k × (küme k'nın ölçeği).
- İngiliz ölçeklemesinin bizim yeniden kurgumuz; formülleri kapalı olduğu için **doğrulanmadı**. İlk deneme (enerjisiz, sınıf başına serbest NNLS) 12 ölçümde ezberledi: bir-dışarıda hata ortancası %53.

## 4. Kaç ev sığar (Faz 3)

Kod: `src/kac_ev.py`. Girdi: `trafolar.csv` (kVA, hat sayısı ve en uzun hat boyu, kablo, abone ve panel sayıları) ve `tahmin.csv` (öğlen en düşük yükün P10 / P90'ı, güven). Ölçülü trafoda ölçülen yük.

- Fizik, ev ev benzetimin (`src/trafo_bos_kapasite.py` `solve`) empedanslarıyla tek denklem: hat ucu gerilimi = trafo çıkışı × (1 + OG öğlen yükselmesi) + r_trafo × faz akımı + r_hat × akım × mesafe; akım = (panel kW × öğlen güneşi − yük) ÷ 250 V. Tek fazlı akım nötrden döner (r_faz + r_nötr), dengeli üç fazda nötr akımı yok. Her yeni ev (6,5 kW) gerilimi sabit bir miktar artırır; 259 V'a kalan pay ÷ ev başına artış = gerilimin izin verdiği ev.
- Öğlen güneşi: Nisan'da en yüksek saatlik eğik ışınım 998 W/m² (2023–2025, Open-Meteo) × 0,82 kayıp [Hesap].
- Isıl: ters akış ≤ kVA: (kVA + yük − mevcut panel × güneş) ÷ güneş = ısıl pay kW.
- Sonuç = gerilim ve ısılın küçüğü, aşağı yuvarlanır, panelsiz konut abone sayısıyla sınırlı.
- **Karamsar:** P10 yük; trafo çıkışı 250 V + %0,8 OG öğlen yükselmesi [Yorum]; yeni paneller **hattın ucunda ve tek fazda** (İngiltere UKPN: paneller uca toplanınca eşit yayılmış model yükselmeyi 2–4 kat az gösterdi; karar masası 16:27); mevcut panellerin yarısı aynı fazda, hat boyunun 2/3'ünde; hat üstünde yük indirimi yok; en uzun hattın payı eşit pay ile boy payının büyüğü.
- **İyimser:** P90 yük, 246 V, yeni ve mevcut paneller hat ortasında, dengeli üç faz, hat yükü panel üretimini azaltır.
- `v_max` 264 V üstü benzetim değerleri fiziksel değil (inverter kapanır; ADR-0006); Faz 3 259 V sınırını kullanır.
- Benzetimdeki "gerçek kaç ev" sıra sıra başvurur, sığmayanı atlayıp sıradakine geçer (trafoya yakın ev uçtaki evden sonra da sığabilir). Bu yüzden gerçek, karamsar ile iyimser arasında, iyimsere yakın düşer.

## 5. Belirsizlik ve renk

- **Bant (%80):** ölçülülerde bir-trafo-dışarıda (kümeleme dahil her şey yeniden kurulur) log artıklar. Artık, trafonun **ölçek birimine** bölünür: √(1 ÷ N_etkin + taban²). N_etkin = enerji ağırlıklı etkin abone sayısı = (Σ E)² ÷ Σ E_i². 40 ev ≈ 40, tek otel ≈ 1–2; abonelerin büyüklük farkı toplamda 1/√N ile söner. Bölünmüş artıkların P10–P90'ı, hedef trafonun birimiyle çarpılır: çok aboneli trafoda dar, tek büyük müşterili trafoda geniş bant. Bant tahmin etrafında **simetrik** (log ölçekte; genişlik P10–P90'ın yarısı): 12 ölçülünün artıkları sağa çarpık çıkıyor, ölçülmeyende ise gerçek tahminin altına daha sık düşüyordu (yanlış yeşil yönü; Faz 2 resmi sınavı, karar masası 17:38).
- **Taban (1.2):** artıklardan seçilir. Var(artık) ∝ 1 ÷ N_etkin + taban² varsayımıyla profil olabilirlik, adaylar 0,05–5. Küçük taban = hata abone sayısıyla söner; büyük taban = her trafoda aynı (faturalı modelde büyüklük zaten bilindiği için; faturasız modelde mahalle farkı yüzünden). Fatura yoksa taban en az 0,3: büyüklüğü abone sayısından bilen model mahalle farkını göremez (gerçek veride müşteri başına öğlen yükünün trafodan trafoya değişimi 0,46, ADR-0008). Sabit 0,05 tabanla, mahalle farkı olan şehirlerde çok aboneli konut trafosu en dar bandı ve "yüksek güven"i alıp en çok yanılan oluyordu.
- İlk sürümde bant küçük örnek düzeltmeli sıra istatistiğiyle (en küçük / en büyük artık) kurulmuştu; bir-dışarıda kötümser olduğu için gerçeğin %100'ünü kapsadı.
- **Güven:**
  - `dusuk`: beklenen hata > %25; ya da enerjinin ≥ %20'si hiç ölçülmemiş tarifede; ya da en yakın ölçülüye uzaklık, ölçülülerin kendi arasındaki tipik uzaklığın 2 katından fazla; ya da atama olasılığı < 0,5.
  - `yuksek`: beklenen hata ≤ %10, olasılık ≥ 0,7, uzaklık ≤ 1 kat, görülmemiş tarife < %5.
  - Diğerleri `orta`. Ölçülü trafo `yuksek`.
  - **Fatura yoksa `yuksek` verilmez** (1.2): büyüklük mahalle farkı kadar (±%30) bilinmez; 12 ölçülünün bir-dışarıda hatası şans eseri küçük çıkan şehirde "yüksek" en çok yanılan oluyordu.
  - Beklenen hata = bölünmüş artıkların mutlak ortancası × trafonun birimi.
  - Eşikler [Yorum]; günlükte gerekçe.
- **Renk (Faz 3, [ADR-0010](../decisions/adr-0010-yesil-karari-marj-guven-kumulatif.md)):**
  - **yeşil** = karamsar senaryo bekleyen evi marjla alıyor (marj = gerilim payının %10'u, en az 1 ev: karamsarda en az ~2 ev sığmalı) **ve** güven yüksek;
  - **kırmızı** = karamsar senaryoda bugün aşıyor (yeni panel olmadan hat ucu 259 V üstünde ya da ısıl pay eksi): "önce ölç ya da güçlendir"; **sarı** = sınırda (karamsar bugün aşmıyor ama bekleyen ev sığmıyor) ya da güven orta / düşük. Karar masası 17:26 bu okumayı seçti (`KIRMIZI_KURALI = karamsar_bugun`); kod öbür iki okumayı da tanır (`karamsar_yeni_ev`: bekleyen ev hattın ucunda sığmıyor; `beklenen_bugun`). Yanlış kırmızı ve sarı oranı ROADMAP hedeflerinin üstünde: sebep ±4 V bilinmeyen bara gerilimi, pilotun ilk ölçeceği şey ([Faz 3 günlüğü](../log/2026-10-31-volkan-faz3.md));
  - sarı → sınırlı onay ya da önce ölçüm (ölçüm cihazı sarılara).
  - Renk, panelsiz konut abone sayısıyla sınırlanmamış fiziğe bakar (başvuru ticari aboneden de gelebilir).
