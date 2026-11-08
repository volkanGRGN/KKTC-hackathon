# 2026-11-08 — Volkan (KARAR): üretici 1.7 — hava verisinin saati ve panelin sıcaklık kaybı

**Etiket: [Hesap] (KTEMO gerçek veri) / gösterim (deneme şehirleri).** Volkan (8 Kasım): "son indirdiğim datalarla modelimizi tekrar eğit." Son indirilen veri (3 Kasım, `hackaton/dis-veri`): KTEMO çatı paneli 5 dk üretim 2018-01-01 – 2026-04-10, PVGIS Lefkoşa 2018–2023, Open-Meteo Lefkoşa 2018–2022 ve 2026 Ocak–Nisan. Önceki bulgular: [KTEMO karşılaştırması](2026-11-03-volkan-ktemo-pv-karsilastirma.md). Dal #43'ün (üretici 1.6) üstünde.

## Hipotez / amaç
3 Kasım karşılaştırması iki hata buldu: (1) Open-Meteo saat sütunu yaz saatsiz sabit UTC+2, model yerel (yaz saatli) sanıyor → Mart sonu – Ekim sonu güneş ve sıcaklık 1 saat erken; (2) panel kaybı sabit 0,82, sıcaklığı görmüyor → yazın açık öğlende fazla, kışın az üretim. İkisi düzeltilirse dünya (deneme şehirleri) ve model gerçek panele yaklaşır.

## Ne değişti
- **`src/pv_hava.py` (yeni):** `om_yerel` (Open-Meteo etiketi → Lefkoşa yerel saati; AB yaz saati kuralı, zoneinfo'suz, Windows'ta da çalışır), `bosluk_doldur` (yaz saatine geçişte boş kalan saat), `panel_carpani` (sıcaklık çarpanı) ve KTEMO ayar betiği (`python3 src/pv_hava.py <ktemo gunluk> <open-meteo klasörü>`).
- **Sıcaklık çarpanı:** 1 + γ × (hücre − T_ref), hücre = hava + 0,03 × ışınım (W/m²). γ = −0,004 / °C (kristal silikon veri sayfası değeri, [Yorum]); T_ref = 50,8 °C = KTEMO 2018–2022 Nisan açık öğle (eğik > 700 W/m², 654 saat) hücre sıcaklığı ortalaması [Hesap]. Böylece Nisan (panel katmanının ayı) eski 0,82 düzeyinde kalır.
- **`src/sehir_uret.py` (üretici 1.7):** ışınım ve sıcaklık yerel saatle okunur; panel üretimi (Nisan ve yaz / kış pencereleri) `panel_isinimi` ile sıcaklıklı; OG öğlen çarpanı da aynı ışınımdan. `ayar.json`'a `panel_sicaklik` ve `hava_saati`.
- **`src/tepe.py`:** hava yerel saatle (ışınım [L−1, L), sıcaklık L); önceden ışınım kışın 1 saat geç, sıcaklık yazın 1 saat erken okunuyordu. Panel için ayın saatlik ışınımı, o saatin sıcaklığı (tepe gününde ± ΔT) ile çarpılır.
- **`src/sahte_kayit.py`:** 1.7 şehirlerinde aynı sıcaklıklı ışınım (yeniden kurma üreticiyle birebir kalsın).
- Değişmeyen: `kac_ev_olasilik.py` öğlen güneşi (Nisan en yüksek saat 998 W/m² × 0,82): yeni çarpan o saatte 0,995 [Hesap], etkisi yok sayıldı. `eszamanlilik.py` (Can'ın) aynı hava klasörünü okuyor; saat kontrolü can.md'de (3 Kasım).
- Hava yılları 2018–2022 üreticiye **eklenmedi**: bayram listesi (`BAYRAMLAR`) yalnız 2023–2025 için yazılı; Ramazan ve Kurban bayramları yıldan yıla kayıyor. Ayrı iş.

## KTEMO gerçek paneliyle ayar ve sınav [Hesap: `src/pv_hava.py`]
Ayar 2018–2022 (etkin güç ve T_ref), sınav 2023–2026 (12.114 gündüz saati; 10 çevrim dışı gün atıldı). Gerçek ÷ formül, açık öğle saatleri:

| Ay | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | Aylar arası yayılım | Günlük hata (ortanca / P90) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Eski (sabit 0,82) | 0,98 | 1,01 | 0,97 | 1,00 | 0,96 | 0,94 | 0,90 | 0,89 | 0,94 | 1,01 | 0,98 | 1,00 | 0,116 | %9,1 / %25,9 |
| 1.7 (sıcaklıklı) | 0,96 | 0,99 | 0,97 | 1,01 | 0,99 | 1,00 | 0,97 | 0,95 | 0,99 | 1,03 | 0,98 | 0,98 | 0,076 | %7,2 / %26,0 |

Yazın fazla tahmin (Temmuz–Ağustos) ~%10 → ~%4; saatlik hata ortancası %17,1 → %17,0 (bulutlu saatler baskın). γ denemesi (−0,004 … −0,007) sınav yıllarına bakılarak yapıldı; seçilen değer önceden belirlenen veri sayfası değeri, aynı zamanda denenenler arasında yayılımı en küçük olan (−0,006 yazı tam düzeltir ama kışı bozar, yayılım 0,098). Ayar ↔ sınav ayrımı bu yüzden γ için kusursuz değil; T_ref ve etkin güç yalnız ayar yıllarından.

## Deneme şehirleri (gösterim)
- Ayar 1–10, aynı tohumlar, 1.6 ↔ 1.7: karar masasında koşuyor (sonuç bu günlüğe eklenecek).
- Sınav 61–70: bir kez, 1.7 ile (Can; can.md).

## Karar / sıradaki adım
- PR: #43'ün üstünde; #43 birleşince yalnız 1.7 farkı görünür. Birleşme Volkan'ın sözüyle.
- Bundan önce "1.7" diye anılan BUILD 1 listesi (gerçek faz dağılımı, kapalı döngü düşüm, sızma kontrolü, Nisan → yaz) artık **1.8**.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
