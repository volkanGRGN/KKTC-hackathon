# Konuşma notu (iskelet)

Anlatan: Volkan. Slayt numaraları [slaytlar.md](slaytlar.md) ile aynı. Rakamların etiketi orada; burada tekrar edilmez.

## Açılış cümlesi (slayt 1–2)
"Kıb-Tek, evlerin bağlı olduğu mahalle trafolarını göremiyor; bu yüzden çatı güneşi başvuruları bekliyor. Güney bağladı ve şimdi ürettiğinin yarısını atıyor."

## Ana cümle (slayt 5'ten önce)
"Kıbrıs'ı ölçemiyoruz; yöntemi ölçebildiğimiz her şeyde kanıtlıyoruz, sonra uyguluyoruz."

## Dürüstlük cümleleri (söylenmesi zorunlu; ROADMAP Faz 5 sınavı)
1. **Kanıt sırası:** "%80 İngiltere'de, gerçek veride. Farazi şehir yalnız gösterim. Kıbrıs'taki doğruluğu pilot söyler."
2. **Farazi şehir üst sınırdır** ([ADR-0008](../decisions/adr-0008-farazi-cesitlilik-saf-tahmin.md) madde 3): "Farazi şehir isabeti gerçek isabetin üst sınırıdır. Gerçek veride, İspanya'da 29 trafoda sınadık: yalnız müşteri sayısıyla ~%25, fatura bilgisiyle ~%10 ortanca hata. Kıbrıs'taki doğruluğu pilot söyler."
3. **Gerilim** (karar masası 17:00, güncelleme 18:46): "Gerilim hesabını İngiltere'de 6 gerçek hatta sınadık: beşinde ölçülen yükselme hesabın güvenli sınırının altında; birinde küçük gördük. Bu yüzden canlıda yeşil önce pilotla sınanır." [Hesap: PR #11 + docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md]
4. **Fatura** (karar masası 17:38): "Fatura olmadan model ortalama trafoda basit hesaptan pek iyi değil; fatura girince hata dörtte bire iniyor. İspanya'da da aynı: %25 → %10." [Hesap: farazi 11–20 faturasız %20,6, faturalı %3,8 (gösterim); İspanya PR #10]
5. **Temsil yanlılığı:** "Ölçülen trafolar yereldir; her tipten örnek yoksa model görmediği tipte kendinden emin yanlış tahmin yapar. Tabakalı seçim, ölçülü/ölçülmeyen dağılım karşılaştırması ve düşük güven etiketiyle bunu sınırlıyoruz, tamamen kaldırmıyoruz."

## Jüri soruları ve cevap iskeleti (ROADMAP Faz 5: 8 soru, her birine ekipten en az iki kişi)
Kaynak: [araştırma günlüğü](../log/2026-10-31-kapsamli-arastirma.md) bölüm 8, ADR-0005, ADR-0010. Cevaplar iskelet [Yorum]; provada kişi adı yazılır.

| # | Soru | Cevap iskeleti | Cevaplayan |
|---|---|---|---|
| 1 | İngiltere'nin kopyası değil mi? | Yöntem İngiltere'nin, hedef bizim: ilkbahar öğlen en düşük yük ve hat ucu gerilimi; bunu doğrulayan çalışma bulamadık | |
| 2 | Veri nereden? | Tüketim eğrileri Güney Kıbrıs dağıtım şirketinin 2022 resmi profilleri, büyüklükler Kıb-Tek 2023 istatistiği, güneş Lefkoşa'nın gerçek verisi; şebeke ölçüleri Alman açık setinden (SimBench); köy, yurt ve sulama varsayım | |
| 3 | Doğruluğunuz ne? | Güven merdiveni: İspanya gerçek veride faturayla ~%10; İngiltere ~%80; farazi şehir gösterim; Kıbrıs için pilot ve kör test | |
| 4 | Kıb-Tek bunu neden alsın? | Başvurular bekliyor, izleme sistemi yok; Güney bağladı, şimdi kısıyor. Pilot 120–170 trafo, taşınabilir cihazla ~20 bin € + pens | |
| 5 | Hangi abone hangi trafoda, biliyor musunuz? | Hayır; Kıb-Tek başvuruda abonelik belgesi istiyor, eşleşme onda. Uzmana ilk sorumuz | |
| 6 | Model yanlış "yer var" derse? | Yeşil yalnız karamsar senaryo marjla geçiyor ve güven yüksekse; canlı bütçe yanlış yeşil < %2; sarılara ölçüm cihazı | |
| 7 | "Yapay zekâ hayır dedi" — kim hesap verir? | Ret yok, triyaj var; son karar Kıb-Tek mühendisinin; itiraz eden gerçek ölçüm ister | |
| 8 | Paneller arttıkça model eskimez mi? | Eskir; ölçüm cihazları her ilkbahar sarılara dolaşır, şablon yenilenir | |

## Bekleyenler
- Slayt 9 canlı harita (Faz 4) ve slayt 10 %40 kuralı karşılaştırması (Faz 3): rakam gelince bu nota bir cümle.
- KTTO raporunun adresi (slayt 1): BULAMADIM.
- Prova süreleri (2 prova, ≤ 7 dk) ve yedekler (PDF, ekran kaydı).
