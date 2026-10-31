# Yöntem

Gerekçeler: [ADR-0001](../decisions/adr-0001-sekil-buyukluk-sablon.md), [ADR-0002](../decisions/adr-0002-gerilim-ilk-surumde.md), [ADR-0003](../decisions/adr-0003-rastgele-farazi-sehirler.md).

## 1. Şekil: kümeleme

- Ölçülü her trafo için bahar (Mart–Mayıs) iş günü ortalama günlük eğrisi, tepesine bölünerek normalize. Ayrı dönem olarak yaz da tutulur.
- Hiyerarşik kümeleme ile küme sayısına bak, k-means ile 3–6 arketip. Küme sayısı seçimi günlüğe yazılır.

## 2. Atama

- Ölçülmeyen trafo için girdiler: kVA, tarife sınıfı başına abone sayısı (konut, ticari I/II, sanayi I/II, su motoru, otel), bağlı panel sayısı, bölge tipi.
- Çok sınıflı lojistik regresyon → en olası arketip ve olasılıkları (olasılık düşükse güven düşer).

## 3. Büyüklük: ölçekleme

- Küme başına: öğlen en düşük yük ≈ Σ β(sınıf) × o sınıftaki abone sayısı, β ≥ 0 (negatif olmayan en küçük kareler). İngiliz ölçeklemesinin bizim yeniden kurgumuz; formül kapalı olduğu için **doğrulanmadı**.
- Hedef tepe değil, bahar öğleni (11–14) en düşük yük.

## 4. Kaç ev sığar

- Isıl: trafo gücü + öğlen en düşük yük − mevcut panel. Yanına bugünkü %40 kuralı.
- Gerilim: pay = 259 − trafo çıkış gerilimi − trafo yükselmesi; etkin mesafe hat boyunun yarısı; tek faz karamsar, dengeli üç faz iyimser. Trafo çıkışı: şartname boşta 250 V, kademe ayarı bilinmiyor → 246–250 V arası (benzetim şu an 246–247 kullanıyor).
- Sonuç = küçüğü ÷ 6,5 kW. İki senaryo: karamsar (düşük yük P10, faz bilinmiyor) ve iyimser.

## 5. Belirsizlik ve renk

- Bant: bir-trafo-dışarıda artıklarının P10–P90'ı.
- Güven: trafonun ölçülü trafolara uzaklığı + atama olasılığı.
- Renk: yeşil = karamsar senaryoda bile yer var ve güven yüksek; kırmızı = iyimser senaryoda bile yer yok; diğerleri sarı → ölç ya da esnek onay.
