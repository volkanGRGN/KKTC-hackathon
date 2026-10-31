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

Yanlış yeşil eşikleri: farazi şehirde ≤ %5 (en kötü şehir ≤ %10) **gösterim** eşiği; canlıya geçiş bütçesi **< %2**, gerçek veride geri-testle tutulur (ADR-0010; marj ve güven eşikleri bu bütçeye göre ayarlanır). Faz 2'de ayrıca **saf tahmin** kıyası: model, saf tahminden ortanca ve P90'da en az %25 iyi olmalı (ADR-0008; tanımı karar masasında: abone sayısı / tarife enerjisi / fatura).

Her ölçü 20–30 şehir üzerinden **aralık** olarak raporlanır (ortanca, en kötü). Ayrıca kaba kıyas: New York şirketlerinin "öğlen yükü = tepenin %15–40'ı" kuralı.

## Temsil yanlılığı

- Ölçülecek trafolar tabakalı ve çeşitli seçilir (tip × kVA × kırsal/kentsel); benzer yerlere değil boşluklara.
- Ölçülü ve ölçülmeyen trafoların özellik dağılımı karşılaştırılıp günlüğe yazılır.
- Gösterim grafiği: ölçülen trafo 5 / 10 / 20 → yanlış yeşil ve hata.

## Gerçek veri

- İspanya EDP (29 gerçek trafo, yük): aynı protokol koşuldu (PR #10); sonuç ayrı başlıkta "gerçek veri". Donuk sınav: üretici ve model İspanya hatasını düşürmek için ayarlanmaz (ADR-0009).
- İngiltere UKPN (6 hat ucu ev, gerilim): `solve()` ölçülen yükselmenin 4 sitede 0,84–1,39 katı, 2 sitede (paneller uçta) 0,22 / 0,52 (PR #11) → karamsar senaryo panelleri hattın ucuna koyar.
- **Pilotun ilk ölçeceği şey bara gerilimi dağılımı** (trafo çıkışı; karar masası 16:27). Farazi şehirde 244–252 V varsayıldı, Kıbrıs dağılımı BULAMADIM. Faz 3'te kırmızı kararını en çok bu belirsizlik bulandırıyor: bugün dolu trafoların hemen hepsi zaten 259 V üstünde, bunu ±4 V bilinmeyen bara gerilimi belirliyor ([Faz 3 günlüğü](../log/2026-10-31-volkan-faz3.md)).
- Kıbrıs için kanıt önerisi: ilkbaharda 10 trafoda kör test (tahmin önce kaydedilir, sonra ≥7 gün ölçülür); başarı ölçütü önerisi: gerçek kırmızıların ≥%90'ı yakalanır, öğlen yük hatası ±%20 ([Yorum]).
