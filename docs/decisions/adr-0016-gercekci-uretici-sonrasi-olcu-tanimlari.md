# ADR-0016: Gerçekçi üreticiden sonra ölçü tanımları — saf fatura kıyası bilgi, yanlış kırmızı kalibrasyon ölçüsü, Faz 1 gerilim sağlaması %1

Tarih: 2026-10-31 · Durum: kabul · ADR-0008, ADR-0010, ADR-0011, ADR-0013 üstüne · kaynak: Faz 8 PR #18 ([günlük](../log/2026-11-01-volkan-faz8-uretici.md)) · karar masası 22:17

## Bağlam
Üretici 1.3 deneme şehirlerini gerçeğe çapaladı (faturalı hata %10 / P90 %32 ≈ İspanya; eğri benzerliği 0,91 ≈ 0,93; faz dengesizliği %15,5 ≈ İngiltere %14,4). Yeni sınav şehirleri 21–30'da üç eski ölçü kalıyor: (a) model, saf fatura tahmininden yalnız %9 / %5 iyi (ADR-0008 şartı ≥ %25); (b) yanlış kırmızı %51 (hedef ≤ %20); (c) bir köy trafosunda en düşük gerilim 205,9 V (Faz 1 sağlaması "207 V altı yok"). Üçü de modelin hatası değil, ölçünün gerçekçi dünyaya uymamasıdır.

## Karar
1. **Saf fatura kıyası bilgi satırıdır, geçme şartı değil.** Öğlen yükünün büyüklüğünü fatura belirler; model fatura üstüne az ekler (farazi %9, İspanya'da saf fatura ölçülecek). Modelin değeri eğri şekli, bant ve güven (kalibre), ve panel kararıdır (dolu trafoya "yer var": %40 kuralı 22/44, biz 0/44). ROADMAP Faz 2'de madde "bilgi"; sunumda dürüst cümle: "Öğlen yükünü fatura söyler; biz ne kadar emin olduğumuzu ve panelin sığıp sığmadığını söyleriz."
2. **Yanlış kırmızı bir kalibrasyon ölçüsüdür.** Kırmızı = bugün aşma olasılığı ≥ 0,5 (ADR-0011); olasılıklar kalibreyse kırmızı denenlerin bir kısmı gerçekte aşmaz, bu beklenir (yanlış kırmızı ≈ 1 − kırmızıların ortalama olasılığı). Ölçü: **kırmızı kovasında gerçekte aşan pay ≥ %50** ve olasılık kovaları gerçekle tutuyor; "≤ %20" hedefi kalkar. Kırmızı "ret" değil "ölç ya da güçlendir"; kırmızıların yarısında yer çıkması pilotun ölçümle açacağı kapasitedir.
3. **Faz 1 gerilim sağlaması: 207 V altındaki trafo payı ≤ %1 ve en düşük ≥ 200 V** (EN 50160 zamanın %95'i; 800 m tek hatlı köyde akşam 206 V gerçekçi). Üretici kVA boyutlandırması bunu gizlemek için değiştirilmez.
4. Yeşil azlığı (gerçekçi şehirde %5; konut ve köyde 0) kabul: kapılar tutuyor (yanlış yeşil 0/17, kapsama %82). Çözüm model ayarı değil karar birimi: başvuru anında karar (ADR-0012, ADR-0015) ve ölçüm (Faz 9–10). Kaç ev bandının üst ucu karamsar (gerçek P90 üstünde %16): Faz 10'da pilot verisiyle asimetrik yeniden kalibrasyon.

## Sonuçlar
- ROADMAP: Faz 2 saf tahmin maddesi "bilgi"; Faz 3 yanlış kırmızı maddesi "kırmızı kovası ≥ %50 aşar (kalibrasyon)"; Faz 1 sağlaması "≤ %1 ve ≥ 200 V" (BUILD).
- Can: sınav maddeleri buna göre (saf tahmin bilgi; kırmızı kovası ölçüsü; Faz 1 %1); konuşma notuna dürüst cümle ve jüri cevabı.
- Sunum rakamları: hangi sürümün (v2 = 1.2 şehirleri, v3 = 1.3 gerçekçi şehirler) anlatılacağı Volkan'ın kararı; ikisi de "gösterim", manşet İspanya değişmez.
