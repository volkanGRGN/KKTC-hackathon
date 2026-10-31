# 2026-10-31 — Muhittin'e danışma ve plan

**Amaç:** Seçilen fikri (trafo şablonu + kaç ev sığar + harita) 36 saatte nasıl kuracağımızı bir dış göze sormak.

**Yaptıklarım:** Soru volki'nin danışman kanalından Muhittin'e gitti; iki cevap geldi, Volkan yapıştırdı. Cevaplar [kapsamlı araştırmayla](2026-10-31-kapsamli-arastirma.md) birleştirilip [plan](../01-plan.md) yazıldı.

**Sonuç:**
- Başlangıç: problemi şekil + büyüklük diye böl, 3–6 arketip → ADR-0001.
- Doğrulama trafo bazında bir-dışarıda; test asla yalnız sentetik; temsil yanlılığına dikkat; dilim başına 5–10, ilk tur 20–50 tabakalı trafo → [doğrulama](../method/validation.md).
- Belirsizlik: P10–P90 bant, kalibrasyon, ölçülü trafolara uzaklıkla güven etiketi → [yöntem](../method/modeling.md).
- Gerilim: önce "sonraya bırak" dedi; ikinci cevapta Kıbrıs gibi ada şebekesinde önce gerilimin bağladığına katıldı → ADR-0002.
- Farazi şehir: tek şehir yerine alan rastgeleleştirme → ADR-0003.
- Karar aracı: ret değil triyaj → ADR-0005.
- Proje düzeni: README, CONTRIBUTING, ADR, günlük, PR/issue şablonları → bu klasör. Muhittin'in başlangıç paketi (proje-md-starter, 31 Ekim) sonradan geldi; dal/commit kuralları, ADR ve günlük şablonları, PR ve görev/hata şablonları paketten alındı, projeye özel kurallar (veri etiketleri, gösterim etiketi, doğrulama protokolü) eklendi.

**Karar / sıradaki adım:** Kol 1 (rastgeleleştirilmiş farazi şehir üreticisi) ile koda başla.
