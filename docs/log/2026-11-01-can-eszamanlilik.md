# 1 Kasım 2026 — Can — Eşzamanlılık ve sıcaklık eğimi: 20 Kıbrıs evi (B-Y2 girdisi)

KARAR 23:02 m. 2–3, 23:12 ("eğim ve eşzamanlılık senin analizinden girer, tablo olarak günlüğe ve kutuya"), 23:18, 00:15.
Civan'ın bulut oturumu (`deneme/eszamanlilik`, 23:08) dal açmadı; analizi Can yaptı (civan.md'ye not).

## Veri
- Zenodo 23043383: 20 konut prosumer, Güney Kıbrıs, 2016, 30 dk (CC BY 4.0). KAYNAK: `data/raw/kibris-20-prosumer/KAYNAK.txt`.
  Değerler 30 dk ortalama güç (W), başlıktaki "kWh" yanlış [Yorum: PV tepesi ~3 kW]. Ev 4'ün export / tüketim sütunu bozuk
  (net = import; brüte girmez).
- Lefkoşa saatlik sıcaklık, Open-Meteo 2015–2025 (BUILD 1'in dosyası; Can yeniden indirdi, SHA-256 birebir).
- Kod: `src/eszamanlilik.py` (tohum sabit; `--cikti` özet JSON). Net = import − export (trafoya binen); brüt bilgi.

## 1. Yılın tepesi ne zaman (ev başına) [Hesap]
- Net (20 ev): tepe ortanca 6,46 kW; akşam (17–01) 13, gündüz 7. Ay: Temmuz 8, Aralık 5, Ocak 4, Kasım 2, Şubat 1.
- Brüt (19 ev): ortanca 6,19 kW; akşam 11, gündüz 8.
- Okuma [Yorum]: tek evin yıl tepesi yaz akşamı kadar sık kış akşamı (ısıtma, termosifon); tepe saate ve aya kilitlenmemeli
  (ADR-0014, KARAR 23:12 ile uyumlu).

## 2. Eşzamanlılık: N ev birlikte (net; sıcak akşam = 19–22 ortalaması ≥ 29,7 °C, yılın P90'ı, 39 gün: Haziran 9, Temmuz 22, Ağustos 8) [Hesap]

| N | ev başına tepe kW, sıcak | diğer | CF sıcak | CF diğer |
|---|---|---|---|---|
| 1 | 5,22 | 6,33 | 1,00 | 1,00 |
| 2 | 4,20 | 4,57 | 0,78 | 0,73 |
| 3 | 3,65 | 3,87 | 0,68 | 0,62 |
| 5 | 3,12 | 3,25 | 0,58 | 0,51 |
| 10 | 2,60 | 2,68 | 0,49 | 0,42 |
| 15 | 2,46 | 2,42 | 0,46 | 0,38 |
| 20 | 2,41 | 2,22 | 0,45 | 0,35 |

(N < 20'de 300 rastgele altküme ortalaması; CF = birlikte tepe ÷ tek tepelerin toplamı, gün kümesi içinde, saat serbest.)

`tepe.py` biçimi (ADR-0018 m. 5, Velander): ev başına tepe = a × (1 + c ÷ √N):
- **sıcak akşamlar: a 1,48 kW/ev, c 2,51** (artık %1,9);
- **diğer günler: a 1,07 kW/ev, c 4,74** (artık %2,0);
- brüt (bilgi): c sıcak 3,22, diğer 5,16.
Okuma [Yorum]: sıcakta çeşitlilik az (c yarıya iniyor): Muhittin'in "klima tepesinde çeşitlilik düşük"ü veride görünüyor.
Bugünkü `tepe.py` c'yi ölçülü trafoların Nisan R'sinden uyduruyor; farazi 31–40'ta ve İspanya'da c = 0 çıkıyor.

## 3. İki bileşen (KARAR 23:18) [Hesap]
Sıcak günde ev başına tepe = 0,79 × (1 + 4,74/√N) + **0,70 kW/ev klima** (N'den bağımsız; taban c'si diğer günlerden).
Artık %1,9, tek Velander ile aynı: veri iki bileşeni dışlamıyor ama kanıtlamıyor da (20 ev az) [Yorum]. N = 20'de klima payı %29.

## 4. Sıcaklık eğimi (net, yaz akşamları Haziran–Eylül 122 gün; 20 evin 17–24 toplam tepesi ÷ ev ~ 19–22 sıcaklığı) [Hesap]
- Parçalı doğrusal: eşik **T0 24,5 °C** (bootstrap P10–P90 23,5–25,0); eşik altı 1,04 kW/ev; eşik üstü **0,104 kW/°C/ev**
  (P10–P90 0,089–0,133) = eşik altı tepeye göre °C başına %10,0 (%8,1–12,7). Bootstrap evler üzerinden, 500.
- **`tepe.py` ölçeğinde** (Temmuz ortalama akşamı 29,8 °C'deki tepeye göre °C başına): **%6,5** (P10–P90 %5,6–7,5).
  `tepe.py`'nin bugünkü konut yaz eğimi (EAC ay tipik günleri ~ ay ortalama sıcaklığı) **%3,0** → model sıcak günde konut
  tepesini **az** gösteriyor (güvensiz yön) [Hesap: tepe.egimler()]. Tanım farkı: burada akşam sıcaklığı, `tepe.py`'de günlük
  ortalamanın ay ortalamasından sapması [Yorum: ikisi birlikte oynar, birebir değil].

## 5. Tasarım akşamı [Hesap]
Lefkoşa 2015–2025, yılın en sıcak 19–22 ortalaması: ortanca 32,4 °C, **10 yılda bir ~33,4 °C** (2016: 32,4). Tasarım
akşamında 20 evin akşam tepesi eşik altının ~1,88 katı.

## Yanlılık ve sınır
- 20 ev, hepsi panelli ve ortalamadan büyük (brüt ortanca 7,2 MWh; Kıb-Tek konut ortalaması 3,7) [Kaynaklı: KAYNAK.txt;
  Hesap]; Güney Kıbrıs, tek yıl, aynı mahalle olmayabilir. N ≤ 20: c'nin büyük N'ye taşınması Velander biçimine güven [Yorum].
- `tepe.py`'nin n'si enerji cinsinden konut eşdeğeri (enerji ÷ 3,69 MWh); bu evler ~1,95 konut eşdeğeri → `tepe.py`'ye
  giden c = c_ev × √(7,21 ÷ 3,69) ≈ c_ev × 1,40 [Hesap; brüt enerjiyle, fatura brüt].
- Farazi şehir bu değerleri sınayamaz (üretici kendi β'sı ve çeşitliliğiyle kuruyor; ADR-0008); gerçek ölçü yok
  (İspanya Mayıs tepesinde klima yok). Eğim ve c'nin `tepe.py`'ye girişi ayrı PR (`yuk/b-y2`), BUILD 1 inceler.

## Sonraki
`tepe.py`: konut yaz eğimi veriden, eşzamanlılık c'si veriden (sıcak / diğer), iki bileşen; 31–40 önce / sonra; PR.
Üretici (sehir_uret.py) β çapası da bu sayılardan yapılabilir (BUILD 1 notu, PR #21) — Volkan'ın dosyası, ayrı iş.

## B-Y2: `tepe.py`'ye bağlama (dal `yuk/b-y2`, PR) — sınav şehirleri 31–40, Windows, üretici main (1.5) [Hesap; gösterim]
Üç sürüm denendi; ölçü `cevap_anahtari.csv` `tepe_yil_kw`, ölçülmeyen 280 trafo (`sinav.py faz2` ve ayrıştırma betiği).

| Sürüm | hata ortanca | P90 | işaretli ortanca (+ fazla) | %80 bant | konut | çarşı | otel | sanayi |
|---|---|---|---|---|---|---|---|---|
| on (eski; eğim EAC, c ölçülülerden = 0) | %5,8 | %15,1 | +%0,2 | %99,6 | −%0,7 | +%9,8 | +%4,2 | +%2,1 |
| **b-y2 (konut yaz eğimi 0,065)** | %10,1 | %19,9 | +%8,4 | %98,9 | +%10,7 | +%11,3 | +%4,4 | +%2,1 |
| b-y2, eğim P10 0,056 / P90 0,075 | %8,1 / %11,8 | %17,5 / %23,2 | +%6,7 / +%10,5 | %99,3 / %97,5 | +%7,8 / +%14,1 | | | |
| b-y2-esz (+ c bütün enerjiye) | %13,6 | %33,3 | −%9,1 | %92,5 | −%2,8 | −%22,8 | −%27,7 | −%24,0 |
| b-y2-esz (+ c yalnız konut payına) | %18,3 | %35,2 | +%2,2 | %85,0 | +%17,5 | −%17,7 | −%24,3 | −%25,8 |

Okuma [Yorum]:
- **Eğim**: konut tepesi farazide %11 fazla çıkıyor → üreticinin konut klima eğimi (β sınıf × U(0,5; 1,5)) 20 gerçek evden düşük; güvenli yön, hata eşiğin içinde. Varsayılan bu.
- **c (ev çeşitliliği)**: Nisan R0'ı konut ağırlıklı ölçülülerden 1 + c/√n ile bölününce düşüyor; konut dışı trafo (çarşı, otel, sanayi) %18–28 **az** → yük tarafının yanlış "yer var"ı (güvensiz). Üretici küçük-N fazlasını kurmuyor; 20 evden 100 evlik trafoya taşıma da veri dışı (Velander uzatması). `--model b-y2-esz` deneme olarak kodda, kapalı; pilot (Faz 10) trafo ölçümüyle sınanır.
- Akşam gerilimi (b-y2): gerçekte 207 V altı 2/280, ikisi de yakalandı; "yeterli" dediğimiz 223 trafoda 0 yanlış (on: 233'te 0).
- Tepe saati ±60 dk %52,1 (aynı), iki adaydan biri %61,1 (on %60,0), dönem %70,0 (on %69,3).
- Geliştirme şehirleri 1–10 bu makinede eski üreticiyle; koşulmadı (Mac koşumu TEST / BUILD 1).

Öneri (karar masası / BUILD 1): (1) varsayılan b-y2 birleşsin; (2) üretici β'sı (sehir_uret.py) konutta bu eğime çapalansın — yoksa farazi tepe sınavı modelin doğru yöne gidişini "hata" sayıyor (Volkan'ın dosyası); (3) c pilotla.
