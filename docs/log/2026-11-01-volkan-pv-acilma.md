# 2026-11-01 — Volkan (+ Claude, BUILD): PV'yi tamamen bırakmadan ne kadar açılır — inverter geri çözümü ve kademe öncülü

Tüzük: geçerli. Karar: karar masası 22:56 (Volkan: "eldeki verilerle devam etsek ne kadar iyileşir, test edelim"; Muhittin cevap 4 madde 5). Dal `deneme/pv-acilma` (taban `uretici/1.3`). Resmi hesap ve resmi rakamlar değişmedi. Yazıldığı saat 31 Ekim ~23:10.

## Soru
Muhittin: PV'yi dondurmak erken olabilir. (A) Kademe ayrık ve politikayla belirli; bara gerilimi sürekli bir bilinmeyen olmaktan çıkar. (B) Panelli evin inverteri sakin anda trafo barasını, öğlen salınımında hat empedansını verir. Bu ikisi, gürültüleriyle, gerçekçi şehirlerde (üretici 1.3) haritayı ne kadar açar?

## Yöntem (`src/pv_acilma.py`, deneme)
Gerçekçi `bilgi_degeri.py`. Resmi kod (v2b) her çekilişte ağı kendi rastgelesiyle kurar; betik ardından bilineni yerleştirir; yeni gürültüler ayrı bir akıştan. Sağlama: S0 iki aralıkta da (geliştirme ve sınav, 400 + 400 trafo) resmi `kac_ev.csv` ile birebir (renk farkı 0).

| Senaryo | Ne bilinir | Nereden |
|---|---|---|
| S0 | bugün (v2b): bara 244–252 V düz, hat boyu ×0,6–1,6, gerilim sapma s | — |
| S-kademe | bara: gerçek değer ya da bir kademe ötesi (±6,25 V), yarı yarıya; ±1 V OG / ölçüm payı | Kıb-Tek kademe standardı, "politika iki değer" [varsayım] |
| S-inverter | panelli evi olan trafoda: bara gerçek ±1 V; hat empedansı gerçek ±%20, s yerine | panelli evin inverter kaydı (sakin an 05:00–06:30, öğlen salınımı) |
| S-ikisi | panelli evi olanda inverter, olmayanda kademe | ikisi |

Varsayımlar [Yorum]:
- Üretici 1.3'te gerçek bara sürekli (244–252 V), kademe politikası verisi yok. Politika bilgisi, "gerçek değer ile bir kademe ötesindeki değer" ikilisi olarak taklit edildi.
- İnverterden empedans ±%20 bütün hatlara uygulandı (hangi evin verisi olduğu bu gürültüye katıldı, sadeleştirme). Yüksüz kol (`KOL_P`) bilinmeyeni kaldı.
- Trafoların %77'sinde en az bir panelli ev var (geliştirme 274/354, sınav 268/349).

## Sonuç

### Sınav 21–30 (bir kez; 349 trafo, 44 dolu)
| Senaryo | Yeşil | Yanlış yeşil | Sarı | Kırmızı (yanlış) | Kırmızıda gerçekte aşan (sınır) | Kaç ev P10 altı / P90 üstü | Kaç ev hatası (orta) |
|---|---|---|---|---|---|---|---|
| S0 | 17 (%5) | 0/17 | %78 | 61 (31) | %49 (%37) | %0,9 / %16,3 | 2 |
| S-kademe | 15 (%4) | 0/15 | %77 | 65 (36) | %45 (%38) | %0,4 / %17,6 | 2 |
| **S-inverter** | **36 (%10)** | **0/36** | %78 | **41 (15)** | **%61** (%34) | %1,7 / %14,6 | 1 |
| S-ikisi | 34 (%10) | 0/34 | %79 | 41 (15) | %61 (%34) | %1,7 / %14,6 | 1 |

Panelli evi olan trafolar (268, 42 dolu):

| Senaryo | Yeşil | Yanlış yeşil | Sarı | Kırmızı (yanlış) |
|---|---|---|---|---|
| S0 | 4 (%1) | 0/4 | %76 | 61 (31) |
| S-inverter | **23 (%9)** | 0/23 | %76 | 41 (15) |

Yeşil, türe göre (sınav): S0 → S-inverter: şehir konutu 0 → **9**/142, yurt 2 → 5/39, çarşı 9 → 13/46, otel 6 → 8/34, köy 0 → 1/56, sulama 0 → 0/32.

### Geliştirme 1–10 (aynı yön)
| Senaryo | Yeşil | Yanlış yeşil | Kırmızı (yanlış) | Kırmızıda gerçekte aşan | Şehir konutunda yeşil |
|---|---|---|---|---|---|
| S0 | 20 (%6) | 0/20 | 53 (24) | %55 | 1/138 |
| S-kademe | 15 (%4) | 0/15 | 54 (27) | %50 | 1/138 |
| S-inverter | 44 (%12) | 0/44 | 34 (8) | %76 | 11/138 |
| S-ikisi | 41 (%12) | 0/41 | 34 (8) | %76 | 11/138 |

### + İnverter kaydı PV'yi açıyor, güvenli
- Yeşil ikiye katlanıyor (%5 → %10); panelli evi olan trafolarda dört katından fazla (4 → 23).
- Şehir konutuna yeşil geri geliyor (0 → 9/142).
- Yanlış kırmızı yarıdan aza iniyor (31 → 15). Kırmızıların gerçekte aşan payı %49 → %61; olasılıklar gerçeğe yaklaşıyor.
- Yanlış yeşil kapısı tutuyor: 0/36.
- Muhittin'in B yolu doğrulanıyor: inverter verisi olan trafoda PV erken açılabilir.

### − İki değerli kademe politikası açmıyor
- Yeşil 17 → 15, yanlış kırmızı 31 → 36: biraz kötüleşiyor.
- Sebep aritmetik: kademe adımı 6,25 V. "İki değerden biri" bilgisi, bugünkü 8 V'luk sürekli banttan dar değil; bir değer bandın dışına taşınca karamsarlaşıyor.
- Kademe bilgisi yalnız **tek değer** biliniyorsa (trafonun kademesi ya da tek değerli politika) açar. O durumda S-inverter'in bara kısmıyla aynıdır. Kıb-Tek'ten istenecek olan bu yüzden "standart" değil, **trafo başına kademe ayarı** (devreye alma kaydı).

### − Sarı değişmiyor (%78)
İnverter verisi kırmızıyı ve yeşili düzeltiyor, sarının boyutunu değil. Sarının kaynağı "sıradaki başvuru hattın neresinden gelecek" sorusu (bilginin değeri, ADR-0012); bara ve empedans bunu çözmez. Çözüm başvuru anında karar (ADR-0012, ADR-0015).

### ? Bu bir üst sınır değil, ama iyimser yanları var
- İnverter gürültüsü ±1 V ve ±%20 [Yorum]; gerçek kayıtta gece boşluğu (sabahın ilk değeri), anlık / ortalama farkı ve evin hattaki yeri daha büyük hata getirebilir. Faz 10'un ilk P6 kayıtları bu payları ölçecek.
- Empedansın bütün hatlara uygulanması iyimser: tek ev yalnız kendi hattını görür.
- Panelli evi olan her trafodan veri gelmez; ev sahibi izniyle, gönüllü.

## Deney günlüğü satırı (tüzük §3)
| Tarih | Sürüm | Tohum | Hipotez | Kapılar | İşletme | Karar |
|---|---|---|---|---|---|---|
| 31 Eki ~23:10 | üretici 1.3, model v2b; deneme | 1–10 kurulum, 21–30 bir kez | inverter + kademe PV'yi açar | yanlış yeşil 0 (bütün senaryolarda) | S-inverter: yeşil %5 → %10, konut 0 → 9, yanlış kırmızı 31 → 15; S-kademe (iki değer) açmıyor; sarı değişmiyor | gösterim; terfi yok (deneme); Faz 10 P6 kartı bu payları ölçer |

## Çalıştırma
```
python3 src/pv_acilma.py <şehir kökü> --aralik 1-10     # geliştirme
python3 src/pv_acilma.py <şehir kökü> --aralik 21-30    # sınav, bir kez
```

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
