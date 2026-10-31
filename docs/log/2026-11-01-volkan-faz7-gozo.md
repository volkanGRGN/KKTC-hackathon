# 2026-11-01 — Volkan (+ Claude, BUILD): Faz 7 — Gozo hattında dış sınama (tek hat, gösterim)

Tüzük: geçerli. Karar: Volkan 21:39 / karar masası madde 2a (Gozo Faz 7'ye, İngiltere'nin yanına; hat boyu ve kablo aralıkla, "tek hat, gösterim"). Dal `deneme/gozo`. Yazıldığı saat 31 Ekim ~22:00.

## Hipotez / amaç
Hesabımızın gerilim fiziği, Malta Gozo'daki bir hattın yayımlanmış dört sonucunu tutturuyor mu? Hat boyu, kablo ve ev sayısı bilinmiyor; aralıkla. Sonuç bir oran, tek tahmin değil.

## Veri partisi (tüzük §2)
- **P3-gozo-2016:** Micallef & Weissenbacher, 14. Symposium Energieinnovation, Graz 2016, Tablo 3 ve metin ([ada ülkeleri günlüğü](2026-10-31-volkan-ada-ulkeleri.md)). Srug F1: 500 kVA, 11 kV / 433 V (boşta faz ~250 V), elle kademe ±%5, yıllık 106.219 kWh, akşam tepe 41 kW, gündüz tepe 25 kW, panel 26,72 kWp; +1 kWp ve +2 kWp her panelsiz eve.
- Bilinen yanlılık: Malta (230 V, sınır 253 V); bir hat; trafonun öbür hatları ve OG seviyesi bilinmiyor.
- Kullanım: **yalnız doğrulama** (hiçbir şey ayarlanmadı). Bu gösterim bir kez koşuldu.

## Yaptıklarım
`src/gozo_dis_sinama.py` (yeni, deneme): bir hat, 27 ev (9 panelli, 18 panelsiz [Hesap]), öğlen en düşük yük 5–10 kW [Hesap: en yüksek anlık panel payı %304 → ≈ 7 kW]. Çekilenler [Yorum]:
- hat boyu 150–600 m;
- kablo ABC70 / ABC95 ya da 50 / 100 mm² (Kotsonias 2019);
- faz ağırlığı 1 ± U(0, 0,3);
- paneller üçte bir çekilişte uçta.

OG değişimi yok. 400 çekiliş; her çekilişte aynı geometride üç panel düzeyi × üç kademe. v1 (s yok) ve v2 (Faz 7 sapma çarpanı s).

## Sonuç

| Makalenin sonucu | v1: tutan | v1: en yüksek gerilim P10 / 50 / 90 | v2: tutan |
|---|---|---|---|
| S1 bugün, normal kademe (250 V): sorun yok | **%13** | 252,8 / 255,9 / 262,2 V | %15 |
| S2 +1 kWp, normal kademe: aşım | %95 | 253,8 / 257,7 / 264,2 V | %95 |
| S3 +1 kWp, bir adım aşağı (243,75 V): sorun yok | %61 | 247,6 / 251,6 / 258,3 V | %51 |
| S4 +2 kWp, en alt kademe (237,5 V): aşım | **%23** | 243,1 / 248,3 / 256,3 V | %36 |
| **Dördü birden** | **%0** (1 çekiliş) | | **%0** |

### − Hesap Gozo'nun sıralamasını tutturmuyor
- **Bugün:** normal kademede bara 250 V, sınır 253 V. Pay 3 V ve 26,7 kWp panel çoğu çekilişte bunu aşıyor. Makale "bugün sorun yok" diyor.
- **+1 kWp:** her panelsiz eve 1 kWp eklemek bizim hesapta en yüksek gerilimi çok az değiştiriyor. En yüksek gerilimi 3 kWp'lik toplu paneller belirliyor; diğer fazlara eklenen panel nötr akımını dengeliyor. Makalede bu ekleme kademe değişikliği gerektirdi.
- **+2 kWp:** en alt kademede hesap çoğu çekilişte aşım görmüyor. Makale aşım ve trafo değişimi diyor.

### ? Sebep iki bilinmeyen, ikisi de veride yok
1. **Öğlen bara gerilimi:** Bu merkezler "mevsimlik kademe ayarı isteyen" merkezlerdi; yazın kademe zaten aşağıda ya da 11 kV öğlen düşük olabilir. "Normal kademe = 250 V" öğlen için doğru olmayabilir. Bu, Faz 3'teki bilginin değeri bulgusuyla aynı: en değerli tek bilgi bara gerilimi.
2. **Panellerin hatta dağılımı ve fazı:** bugünkü 26,7 kWp'nin hangi evlerde ve fazlarda olduğu bilinmiyor; sonuç buna çok duyarlı.

Hat boyu ve kablo da bilinmiyor ama tek başına açıklamıyor. Hiçbir boy / kablo dördünü birlikte tutturmuyor.

### ? Ne söylenebilir, ne söylenemez
- **Söylenemez:** "hesabımız Gozo'da doğrulandı" ya da "yanlış çıktı". Bilinmeyenler sonucu belirliyor. Karar masasının 20:47'deki "bilgi eksik, rakam üretmez" sezgisi doğru çıktı.
- **Söylenebilir:** Gozo'da da kaldıracı hat değil bara ve panel dağılımı belirliyor.
- Micallef tezi (dış veri isteği) kademe ayarını ve hat verisini verirse bu sınama tek tahminle yeniden koşulur.

## Deney günlüğü satırı (tüzük §3)
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 31 Eki ~22:00 | v1 fizik ve v2 (Faz 7 s); `deneme/gozo` | 11 | Gozo'nun 4 sonucunu tutturur | dördü birden %0; S1 %13, S4 %23 (v1) | olumsuz / belirsiz; terfi yok; tez verisi beklenir |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
