# ADR-0014: Yük katmanı ayrı bir tepe modeliyle; yük kVA (pf varsayımı yazılı), güneş kWp; iki sayılı kart asimetrik etiketle

Tarih: 2026-10-31 · Durum: kabul (sunum sonrası; sunumda yalnız "sıradaki katman, ön") · ADR-0001, ADR-0002 üstüne · kaynak: Can'ın "iki sayılı kart" önerisi (volkan.md 20:58 sonrası) ve Muhittin'in üçüncü cevabı (5, 6) · karar masası 21:15

## Bağlam
Harita panele özgü kalmamalı (Volkan, 31 Ekim). Malta'nın haritası her trafo merkezinde iki sayı veriyor: tüketim için ve güneş için kalan yer. Modelimiz en yüksek yükü hedeflemedi; Can'ın denemesinde öğlen tahmininden türetilen tepe Nisan'da %4 / %10 hata veriyor, ama Kıbrıs'ın bağlayıcı tepesi Temmuz akşamı klima yükü.

## Karar
1. **Ayrı, hafif bir tepe modeli:** sürücüsü sıcaklık (gerekirse nem) ve müşteri karışımı; eşzamanlılık yük seviyesiyle değişir (ADMD müşteri sayısıyla ölçeklenir). Tepe, güneş modelinin yan ürünü sayılmaz. Can'ın 3. yolu (öğlen × tepe/öğlen oranı) yalnız Nisan içi kıyas ve başlangıç.
2. **Nisan → yıl tepesi hava normalizasyonuyla:** tepe sıcaklığa karşı fit edilir, tasarım sıcaklığına (1-in-N yıl sıcak akşam) uzatılır; yalnız Nisan varsa pencere içi günlük değişimden sıcaklık-tepki eğimi, "riskli" etiketiyle. Sınıf profili mevsim oranı tek başına yetmez. Yaz ölçümü gelene kadar sonuç **"ön, düşük güven, yaz verisiyle güncellenecek"**, geniş bant.
3. **Birim:** yük tarafı **kVA**; güç katsayısı bilinmiyorsa 1 alınmaz (boş yeri fazla gösterir); Kıb-Tek planlama pf'i (bulunana kadar 0,95 [varsayım, yazılı]) ve duyarlılık. Güneş tarafı **kWp**. Uzmana soru 9: Kıb-Tek trafo yüklenmesini kVA mı kW mı izliyor, pf varsayımı ne?
4. **İki sayılı kart, asimetrik:** güneş sıkı bant + yüksek güven rozeti; yük geniş bant + "ön" etiketi. Bir sayı ancak dürüst bir bant konabiliyorsa gösterilir; yüke sorumlu bant konamıyorsa "tahmini — yakında" diye düşük seviyede, gizlenmeden. İki sayı bağımsız değil ve farklı saatlerde bağlanır: "toplanmaz, takas değildir" ibaresi.
5. **Sunumda:** kart gösterilmez; "aynı harita, sıradaki katman: yük (ön; Nisan tepesi yaz tepesi değil)" cümlesi ve jüri cevabı.

## Sonuçlar
- Sözleşme 1.4 adayı: `tepe_kva` + P10/P90 + `pf_varsayim`; `sablon.py` ya da ayrı `tepe.py` (ana oturum); Can `sinav.py faz2`'ye tepe maddesi (geçici eşik ortanca ≤ %15 / P90 ≤ %35 [Yorum]); Civan kart görünümü.
- ROADMAP "sunum sonrası" Faz 11 (karar masası 21:15; yeniden numara 21:25).
