# ADR-0003: Tek şehir değil 20–30 rastgele farazi şehir; test asla yalnız farazi değil

Tarih: 2026-10-31 · Durum: kabul

## Bağlam
Gerçek Kıbrıs trafo ölçümü yok; hackathon kaynağı belirtilen benzetim verisine izin veriyor. Muhittin: tek şehirde model şehri değil benzetimin varsayımlarını öğrenir; fizik (güç akışı, güneş) gerçeğe taşınır, insan davranışı taşınmaz.

## Karar
Belirsiz ayarlar (sınıf başına tüketim, kullanım saatleri, panel yaygınlığı, hava yılı) rastgeleleştirilerek 20–30 şehir üretilir; sonuçlar şehirler arası aralık olarak verilir. Farazi sonuç "gösterim" etiketlidir. Kanıt sırası: İngiltere gerçek veride ~%80 → varsa İspanya'nın 30 gerçek trafosu → farazi şehirler.

## Sonuç
- Artı: davranış katmanı uydurma değil, Güney Kıbrıs'ın gerçek sayaç eğrileri (ADR-0004).
- Eksi: Kıbrıs'ta gerçek doğruluk bilinmiyor; pilot ve kör test önerisiyle kapatılır ([doğrulama](../method/validation.md)).
