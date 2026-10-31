# Yöntem

Gerekçeler: [ADR-0001](../decisions/adr-0001-sekil-buyukluk-sablon.md), [ADR-0002](../decisions/adr-0002-gerilim-ilk-surumde.md), [ADR-0003](../decisions/adr-0003-rastgele-farazi-sehirler.md). Kod: `src/sablon.py` (bölüm 0–3, 5), `src/kac_ev.py` (bölüm 4, Faz 3). Sonuçlar ve neden böyle seçildiği: [Faz 2 günlüğü](../log/2026-10-31-volkan-faz2.md).

Kural: model yalnız Kıb-Tek'in bileceğini girdi alır (`trafolar.csv`) ve yalnız ölçülü trafoların yükünü görür (`yuk_5dk.csv`'nin o satırları). Cevap anahtarını okumaz.

## 0. Hangi trafolar ölçülür (öğretici küme)

- Kıb-Tek'in bildiği özellikler (abone karışımı, büyüklük, bölge) standartlaştırılır, trafolar n tabakaya bölünür (k-means), her tabakadan bir rastgele trafo seçilir. Benzer yerlere değil boşluklara ([doğrulama](validation.md) "temsil yanlılığı").
- Abone karışımı enerjiye göre: abone sayısı × o tarifenin abone başına yıllık tüketimi (Kıb-Tek 2023 istatistiği, [Hesap]). Kıb-Tek bunu faturadan bilir.
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

- Isıl: trafo gücü + öğlen en düşük yük − mevcut panel. Yanına bugünkü %40 kuralı.
- Gerilim: pay = 259 − trafo çıkış gerilimi − trafo yükselmesi; etkin mesafe hat boyunun yarısı; tek faz karamsar, dengeli üç faz iyimser. Trafo çıkışı: şartname boşta 250 V, kademe ayarı bilinmiyor → 246–250 V.
- Sonuç = küçüğü ÷ 6,5 kW. İki senaryo: karamsar (P10 yük, faz bilinmiyor) ve iyimser.
- `v_max` 264 V üstü benzetim değerleri fiziksel değil (inverter kapanır; ADR-0006); Faz 3 259 V sınırını kullanır.

## 5. Belirsizlik ve renk

- **Bant (%80):** ölçülülerde bir-trafo-dışarıda (kümeleme dahil her şey yeniden kurulur) log artıklar. Artık, trafonun **ölçek birimine** bölünür: √(1 ÷ N_etkin + 0,05²). N_etkin = enerji ağırlıklı etkin abone sayısı = (Σ E)² ÷ Σ E_i². 40 ev ≈ 40, tek otel ≈ 1–2; abonelerin büyüklük farkı toplamda 1/√N ile söner. Bölünmüş artıkların P10–P90'ı, hedef trafonun birimiyle çarpılır: çok aboneli trafoda dar, tek büyük müşterili trafoda geniş bant.
- İlk sürümde bant küçük örnek düzeltmeli sıra istatistiğiyle (en küçük / en büyük artık) kurulmuştu; bir-dışarıda kötümser olduğu için gerçeğin %100'ünü kapsadı.
- **Güven:**
  - `dusuk`: beklenen hata > %25; ya da enerjinin ≥ %20'si hiç ölçülmemiş tarifede; ya da en yakın ölçülüye uzaklık, ölçülülerin kendi arasındaki tipik uzaklığın 2 katından fazla; ya da atama olasılığı < 0,5.
  - `yuksek`: beklenen hata ≤ %10, olasılık ≥ 0,7, uzaklık ≤ 1 kat, görülmemiş tarife < %5.
  - Diğerleri `orta`. Ölçülü trafo `yuksek`.
  - Beklenen hata = bölünmüş artıkların mutlak ortancası × trafonun birimi.
  - Eşikler [Yorum]; günlükte gerekçe.
- **Renk (Faz 3):** yeşil = karamsar senaryoda bile yer var ve güven yüksek; kırmızı = iyimser senaryoda bile yer yok; diğerleri sarı → ölç ya da esnek onay.
