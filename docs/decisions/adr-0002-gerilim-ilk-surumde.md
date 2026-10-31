# ADR-0002: "Kaç ev sığar" ilk sürümde gerilimi de hesaplar

Tarih: 2026-10-31 · Durum: kabul

## Bağlam
Muhittin'in ilk önerisi: ilk sürümde yalnız trafo ısıl payı, gerilim "henüz modellenmedi" diye işaretlensin. Bizim benzetimimizde Kıbrıs'ta önce hat ucundaki gerilim doluyor (trafo boşta 250 V, inverter 264 V'ta kapanıyor, ~14 V pay); %40 kuralı ortalamada bağlamıyor. Isıl payla yetinilirse harita yanlış "yeşil" verir.

## Karar
İlk sürümde ikisi birden: ısıl pay ve basit gerilim payı formülü (tek faz karamsar, dengeli iyimser); küçüğü alınır. Formül ev ev benzetimle karşılaştırılır.

## Sonuç
- Muhittin ikinci cevabında katıldı: küçük, yalıtık, uzun kırsal hatlı ada şebekesinde önce gerilim bağlar; anakara aracı olduğu gibi taşınamaz.
- Eksi: hat boyu ve faz bilgisi gerekir; gerçekte Kıb-Tek'te kayıtlı olup olmadığı BULAMADIM. Faz bilinmezse sonuç ~6 kat oynar → renk karamsara göre.
