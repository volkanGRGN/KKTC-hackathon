# 2026-11-01 — Volkan (+ Claude, BUILD): Faz 8 — üretici 1.3, gerçeğe çapalama ve yeni sınav şehirleri

Tüzük: geçerli. Kart: [volkan-faz8-uretici](../gorev/volkan-faz8-uretici.md). Karar: karar masası 21:25, 21:51. Dal `uretici/1.3` (taban `kalibrasyon/faz7`, PR #16). Yazıldığı saat 31 Ekim 22:15–22:30.

## Hipotez / amaç
Faz 7 farazi şehrin gerçekten düzgün olduğunu gösterdi: faturalı model farazide %4, İspanya'da %10 hata yapıyor; trafo eğrilerinin benzerliği farazide 0,99, İspanya'da 0,93. Hipotez: üretici gerçek kadar dağınık olursa farazi şehir "fazla iyi" görünmeyi bırakır ve sınav rakamları gerçeğe yaklaşır.

## Veri partileri ve bölünme (tüzük §2; DONDURULDU 22:05)
- **Ayar:** İspanya (P1: eğri benzerliği, CV, W/müşteri, faturalı hata), İngiltere (P2: kent faz dengesizliği, öğlen OG). Yalnız şehir 1–10.
- **Sınav:** **yeni tohumlar 21–30**, bir kez. Eski sınav şehirleri 11–20 hiçbir ayara girmedi.
- Model (Faz 7, v2b: k_yük 1,27, gerilim sapma s) bu fazda değişmedi.

Sürüm üçlüsü: üretici 1.3 (dal `uretici/1.3`), model v2b (PR #16, 1cd7249), veri P1 + P2; tohumlar 1–10 ve 21–30; Mac, Python 3.12 (tüzük madde 5: resmi rakam karar masasının Mac koşumundan).

## Yaptıklarım
`src/sehir_uret.py` 1.3, üç düğme, yeni rastgelelik ayrı akışlardan (şehrin trafo / abone / hat yapısı 1.2 ile aynı):
1. **Öğlen evde olma farkı:** trafo (mahalle) başına log-normal çarpan σ 0,20 ve abone başına σ 0,30 [Yorum]. Çarpan 12:30 merkezli, 3 saat genişliğinde bir çan üzerinden günü ağırlıklandırır; günlük enerji korunur. Fatura değişmez, öğlen değişir.
2. **Faz dengesi:** kent / turistik / sanayi hatlarında tek fazlı abonelerin %70'i fazlara sırayla bağlanır (dağıtım işletmecisinin dengelemesi); kırsalda değişiklik yok.
3. **Öğlen OG değişimi:** şehir başına −%0,4…+%0,8 düz (1.2'de sabit +%0,8).

### Ayar (şehir 1–10; model v2, k 1,475 ile; kapsama sütunu bu yüzden bilgi)
| Öğlen farkı σ (trafo) | Faturalı hata ortanca / P90 | Eğri benzerliği (tüm / konut) | Konut CV | Konut W/müşteri |
|---|---|---|---|---|
| 0 (yalnız faz + OG) | %4,0 / %9,6 | 0,96 / 0,99 | 0,32 | 313 |
| 0,15 | %8,1 / %26,0 | 0,92 / 0,99 | 0,35 | 302 |
| **0,20** | **%10,0 / %31,9** | **0,91 / 0,98** | 0,36 | 299 |
| 0,25 | %12,0 / %36,3 | 0,90 / 0,98 | 0,37 | 291 |
| 0,35 | %15,9 / %50,5 | 0,87 / 0,97 | 0,40 | 281 |
| **Gerçek** | İspanya %10–11 / %32–33 (10–15 ölçülü) | İspanya 0,93 (karışık) | İspanya 0,45 (karışık) | İspanya 285; İngiltere 205–355 |

- Seçilen 0,20: faturalı hatanın ortancası ve P90'ı İspanya'yla tutuyor. Benzerlik 0,91 (İspanya 0,93; 0,15'te 0,92). Mesafe bu tek düğmede 0,20 civarında en küçük (plato).
- Faz dengesi (yük benzetimsiz, 10 şehrin yapısıyla): sırayla bağlanan pay 0 / 0,3 / 0,5 / 0,7 / 0,8 → kent dengesizliği ortanca %21,0 / 18,7 / 16,6 / **13,6** / 11,9; P84 %53 / 46 / 41 / **36** / 32. İngiltere kent %14,4 / %30,3. Seçilen 0,7 (P84 biraz yüksek kalıyor: temkinli yön).
- Ayar sırasında bulunan: farazi kapsama üretici dağınıklaşınca inmiyordu. Sebep k_yük'ün karışık ölçülü sayısından hesaplanmasıydı → Faz 7'de K_YUK 1,475 → 1,27 (karar masası 22:06; Faz 7 günlüğü).

### Mesafe tablosu: üretici 1.2 ↔ 1.3 ↔ gerçek (şehir 1–10, model v2b)
| Ölçü | 1.2 | 1.3 | Gerçek |
|---|---|---|---|
| Faturalı hata ortanca / P90 | %4,2 / %9,4 | %10,0 / %31,9 | İspanya %10–11 / %32–33 |
| Eğri benzerliği (tüm trafolar) | 0,96 | 0,914 | İspanya 0,93 |
| Faz dengesizliği (enerji, şehir ortancası) | ~%21 (kent) | %15,5 | İngiltere kent %14,4 |
| Öğlen OG | +%0,8 sabit | −%0,2…+%0,4 (10 şehir) | İngiltere öğlen ~1 V düşük |
| Farazi %80 bant kapsaması | %87,5 | %87,5 (havuz %85) | hedef %70–90 |

## Sonuç: sınav 21–30, bir kez (üretici 1.3, model v2b)
| Madde | Eski sınav 11–20 (1.2, v2b) | **Yeni sınav 21–30 (1.3, v2b)** |
|---|---|---|
| Faz 1: en düşük gerilim ≥ 207 V | geçti | **KALDI** (1 trafo 205,9 V) |
| Faz 2: yük hatası ortanca / P90 | %3,8 / %8,0 | %12,2 / %27,0 (geçti) |
| Faz 2: %80 bant kapsaması | %92,9 (bilgi) | **%82,1 (geçti)** |
| Faz 2: arketip doğru oranı | — | %89,3 (en kötü %67,9) |
| Faz 2: saf tahminden ≥ %25 iyi | geçti | **KALDI** (%9,3 / %5,2) |
| Faz 3: yanlış yeşil | 0/49 | **0/17 (geçti)**; dolu trafoya yeşil 0/44 |
| Faz 3: yeşil | 49 (%14) | **17 (%5)**: otel 6, çarşı 9, yurt 2; konut 0, köy 0 |
| Faz 3: kırmızı / yanlış kırmızı | 61 / %32,8 | 61 / **%50,8** |
| Faz 3: sarı | %68,3 | %77,7 |
| Faz 3: kaç ev hatası (orta) | 1 | 2 (geçti) |
| Faz 3: kaç ev P10 altı / P90 üstü | %7,1 / %4,6 | %0,9 / **%16,3** |
| %40 kuralı yanlış yeşil | 41/284 | 22/275 (dolu trafoya "yer var" 22/44) |

Geliştirme 1–10 aynı yönde: yeşil 44 → 20, yanlış yeşil 0/20, sarı %79, yanlış kırmızı %45; saf tahmin maddesi %16,6 ile kaldı.

### + Farazi şehir artık gerçeğe yakın
Faturalı model hatası farazide %12 (İspanya %10), bant kapsaması %82: Faz 7'nin gerçeğe göre kalibre ettiği bant, gerçeğe çapalanmış farazide de tutuyor. Faz 7'de "farazi madde bilgi satırına" inmişti; 1.3 şehirlerinde yeniden geçiyor.

### + Yanlış yeşil kapısı tutuyor
Gerçekçi dünyada da dolu trafoya hiç "yer var" demedi (0/17; dolu 44). %40 kuralı dolu trafoların yarısına "yer var" diyor.

### − Gerçekçi dünyada konut trafosuna yeşil yok, kırmızıların yarısı yanlış
- Yeşil %5'e indi, yalnız otel, çarşı ve yurt. Kırmızıların %51'inde aslında yer var. Kaç ev bandı artık karamsar: gerçek, iyimser sayının üstünde %16 trafoda.
- Sebep: ölçülmeyen trafonun öğlen yükü artık gerçek kadar belirsiz (P90 hata %27). Bant genişleyince çekilişlerin bir kısmı çok düşük yük görüyor; bugün aşma olasılığı yükseliyor (kırmızı, çoğu yanlış), ilk iki başvurunun %98 sığması tutmuyor (yeşil yok).
- Anlamı: harita tek başına konutta "evet" diyemiyor; "önce ölç" ve başvuru anında karar (ADR-0012) asıl yol. Trafonun öğlen yükü ölçülünce (Faz 10 pilot) ya da Kıb-Tek kaydı gelince (Faz 9) belirsizlik daralır. Bilginin değeri denemesinin "+ öğlen yükü" satırı bunu söylüyordu.

### − Faz 2'nin saf tahmin maddesi kalıyor
Gerçekçi dünyada model, faturayı ortak oranla çarpan saf tahmini ortancada ancak %9, P90'da %5 geçiyor (madde %25 ister). Mahalleden mahalleye öğlen davranışı faturadan görünmüyor; abone sınıfı ve kümeler bunu az açıklıyor. İspanya'da bu kıyas yapılmadı (orada saf tahmin müşteri sayısıyla: %25 → model %10). Model fatura üstüne az şey katıyor; değeri bantta ve gerilim hesabında.

### − Faz 1'in "207 V altı yok" sağlaması kalıyor
sehir-021 T25: köy, 100 kVA, tek hat 802 m ABC70, 31 konut; akşam tepesinde 205,9 V. Öğlen evde olma farkı (G < 1) enerjinin bir kısmını akşama kaydırıyor. Uzun kırsal hatta gerçekçi; sağlama "benzetim bozuk değil" amacıyla konmuştu. Karar masasına: madde "≤ %1 trafo" mu olsun, yoksa üreticide kVA boyutlandırma öğlen çarpanını görsün mü.

### ? Bu turda yapılmayanlar
Malta trafo boyutu çapası (Nisan / yıl tepe oranı EAC'den türetilmeli), Kotsonias ince uç kol senaryosu (yaygınlığı BULAMADIM), panel yeri dağılımı, mahsuplaşmalı faturanın net yazılması (uzmana soru 7).

## Deney günlüğü satırı (tüzük §3)
| Tarih | Sürüm | Tohum | Hipotez | Kapılar | İşletme | Karar |
|---|---|---|---|---|---|---|
| 31 Eki 22:25 | üretici 1.2 → 1.3; model v2b; veri P1 + P2 | ayar 1–10, sınav 21–30 | gerçekçi üretici, farazi "fazla iyi" bitmeli | yanlış yeşil 0/17 GEÇTİ; kalibrasyon farazide %82 (İspanya kapısı Faz 7) | yeşil %5 (konut 0), yanlış kırmızı %51, sarı %78; Faz 1 ve Faz 2'de birer madde KALDI | terfi **önerisi**, eksi bulgular karar masasında; puanlayan Can; "iyileşti" denmez (dünyayı değiştirdik, modeli değil) |

## Çalıştırma
```
python3 src/sehir_uret.py 1 10 --cikti data/synthetic/u13      # ayar şehirleri
python3 src/sehir_uret.py 21 30 --cikti data/synthetic/u13     # yeni sınav şehirleri
python3 src/sablon.py <kök> && python3 src/kac_ev_olasilik.py <kök>
python3 src/sinav.py faz1|faz2|faz3 <kök> --aralik 21-30
python3 src/edp_kiyas.py <EDP GIS_data> <kök>                 # İspanya ↔ farazi mesafe (Can'ın)
```

## Ek girdi — 31 Ekim 22:30: karar masası 22:2x ve ADR-0016 (ölçü tanımları)
Karar: bedel kabul. Saf fatura kıyası bilgi satırı; yanlış kırmızı bir kalibrasyon ölçüsü (kırmızı kovasında gerçekte aşan ≥ %50, "≤ %20" kalkar); Faz 1 sağlaması 207 V altı ≤ %1 trafo ve en düşük ≥ 200 V; kVA boyutlandırması değişmez. Yeni koşum yok; aşağıdakiler 21–30'un tek koşusunun çıktısından ve İspanya'nın bir koşusundan.

### Kırmızı olasılığı kovaları ↔ gerçekte bugün aşan (259 V)
| Kova | Sınav 21–30: trafo / ortalama olasılık / gerçekte aşan | Geliştirme 1–10 |
|---|---|---|
| 0,0–0,1 | 167 / 0,01 / %1 | 175 / 0,01 / %0 |
| 0,1–0,3 | 60 / 0,18 / %2 | 73 / 0,19 / %4 |
| 0,3–0,5 | 61 / 0,39 / %15 | 53 / 0,38 / %28 |
| 0,5–0,7 | 35 / 0,57 / %34 | 33 / 0,58 / %42 |
| 0,7–0,9 | 25 / 0,78 / %68 | 19 / 0,77 / %74 |
| 0,9–1,0 | 1 / 0,90 / %100 | 1 / 0,95 / %100 |
| **Kırmızı (≥ 0,5)** | **61 / 0,66 / %49** | **53 / 0,65 / %55** |

- "Gerçekte dolu" (kaç ev gerçek 0) her kovada "bugün aşan" ile aynı çıktı.
- **Ölçü sınavda sınırda kalıyor (%49 < %50)**, geliştirmede geçiyor (%55). Olasılıklar karamsar: model %57 dediğinde gerçekte %34 aşıyor. Kaynağı Faz 7'nin temkini (gerilim sapma s, geniş yük bandı). Düzeltme, pilot verisiyle asimetrik yeniden kalibrasyon (Faz 10); bu turda ayar yok.

### İspanya'da saf fatura kıyası (bir koşu; `edp_test.py`, girdi `saf_fatura` eklendi)
| Ölçülü | Model (faturalı, c) ortanca / P90 | Saf fatura (Σ öğlen ÷ Σ fatura × fatura) | Müşteri sayısıyla kıyas |
|---|---|---|---|
| 5 | %13,0 / %33,8 | %13,0 / %33,8 | %23,8 / %56,5 |
| 10 | %10,9 / %32,3 | %10,9 / %32,3 | %25,6 / %58,8 |
| 15 | %10,3 / %33,1 | %10,3 / %33,1 | %25,2 / %54,5 |

- Satır satır: model tahmini saf faturanın 0,9993–1,0001 katı. İspanya'da abone sınıfı yok, model tek bir fatura sütunuyla ve ortak orana çekili katsayıyla saf fatura kıyasına iniyor. **Faturalı model İspanya'da fatura üstüne hiçbir şey katmıyor**; farazi 1.3'te (abone sınıflı) %9 katıyor.
- "%25 → %10" manşeti fatura toplamının değeri: doğru, ama modelin değil, faturanın. Sunumda ADR-0016'nın cümlesi: "Öğlen yükünü fatura söyler; biz ne kadar emin olduğumuzu ve panelin sığıp sığmadığını söyleriz."

### Faz 1, yeni ölçütle
Sınav 21–30: 207 V altı 1/400 (%0,25), en düşük 205,9 V → geçer. Geliştirme 1–10: 0/400, en düşük 212,3 V.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
