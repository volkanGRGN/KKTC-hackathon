# ADR-0001: Şekil + büyüklük şablonu, doğrudan model değil

Tarih: 2026-10-31 · Durum: kabul

## Bağlam
Ölçülmeyen trafonun günlük yükünü tahmin etmek için iki yol vardı: (a) 24 saatlik eğriyi doğrudan tahmin eden bir model (gradyan artırma, kuantil regresyon, Fourier katsayıları), (b) İngiltere'nin ağ şablonları yöntemi: ölçülü eğrileri şekline göre kümele, ölçülmeyeni abone karışımıyla bir kümeye ata, abone sayısıyla ölçekle. Az veri var (pilotta 20–50 trafo).

## Karar
(b). Problem şekil (3–6 arketip) ve büyüklük (tarife sınıfı başına abone sayısı ile negatif olmayan regresyon) olarak ikiye bölünür. Hedef tepe değil, bahar öğleni (11–14) en düşük yük.

## Sonuç
- Artı: İngiltere'de gerçek veride ~%80, başka şirketlerin 284 trafosunda %80–90; az veriyle ezberlemez; Kıb-Tek'e açıklanabilir. Muhittin de aynı başlangıcı önerdi.
- Eksi: öğlen minimumu için şablonu doğrulayan çalışma bulamadık; ölçekleme formülü bizim yeniden kurgumuz. "Doğrulanmadı" diye söylenir.
- Doğrudan olasılıksal model ikinci adım olarak kalır.
