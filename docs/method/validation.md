# Doğrulama protokolü

Kural: **test seti asla yalnız farazi değil.** Farazi şehir yöntemin çalıştığını gösterir, Kıbrıs'taki doğruluğu kanıtlamaz. Gerekçe [ADR-0003](../decisions/adr-0003-rastgele-farazi-sehirler.md).

## Ayırma

- Bölme **trafo bazında**: bir trafonun hiçbir saati hem eğitimde hem testte olamaz (saat bazında bölmek hatayı yanıltıcı düşük gösterir).
- Bir-trafo-dışarıda: her ölçülü trafo sırayla dışarı alınır, kalanlarla tahmin edilir.
- Şehirler arası: bir farazi şehirde kurulan şablon başka şehirde denenir.

## Ölçüler

| Ölçü | Tanım | Neden |
|---|---|---|
| Doğru arketip oranı | atanan arketip = gerçek kümesi | İngiltere ile kaba kıyas |
| Öğlen en düşük yük hatası | |tahmin − gerçek| / gerçek, ortanca ve P90 | ölçeklemenin kalitesi |
| **Yanlış yeşil oranı** | "yeşil" denen trafolardan gerçekte dolu olanların payı | en pahalı hata |
| Yanlış kırmızı oranı | "kırmızı" denen ama yeri olan | vatandaşın hakkı |
| Kaç ev hatası | tahmini kaç ev − ev ev benzetimde gerçek kaç ev | ürünün asıl sayısı |
| Kalibrasyon | %80 bandın gerçek değeri kapsama oranı | sahte güven var mı |

Her ölçü 20–30 şehir üzerinden **aralık** olarak raporlanır (ortanca, en kötü). Ayrıca kaba kıyas: New York şirketlerinin "öğlen yükü = tepenin %15–40'ı" kuralı.

## Temsil yanlılığı

- Ölçülecek trafolar tabakalı ve çeşitli seçilir (tip × kVA × kırsal/kentsel); benzer yerlere değil boşluklara.
- Ölçülü ve ölçülmeyen trafoların özellik dağılımı karşılaştırılıp günlüğe yazılır.
- Gösterim grafiği: ölçülen trafo 5 / 10 / 20 → yanlış yeşil ve hata.

## Gerçek veri

- İspanya EDP (30 gerçek trafo) kullanılabilirse aynı protokol orada koşulur; sonuç ayrı başlıkta "gerçek veri" diye verilir.
- Kıbrıs için kanıt önerisi: ilkbaharda 10 trafoda kör test (tahmin önce kaydedilir, sonra ≥7 gün ölçülür); başarı ölçütü önerisi: gerçek kırmızıların ≥%90'ı yakalanır, öğlen yük hatası ±%20 ([Yorum]).
