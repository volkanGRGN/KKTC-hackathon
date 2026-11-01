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
