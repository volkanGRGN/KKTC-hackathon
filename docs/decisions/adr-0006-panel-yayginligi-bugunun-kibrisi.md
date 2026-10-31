# ADR-0006: Faz 1 panel yaygınlığı bugünün Kıbrıs'ına çapalanır (%3–25)

Tarih: 2026-10-31 · Durum: kabul

## Bağlam
Şehir üreticisinin ilk 20 şehrinde (ROADMAP Faz 1 aralığı: panel yaygınlığı %10–50, trafo çıkışı 246–250 V) konut ve köy trafolarının %55'i bugünden 259 V planlama sınırının üstünde çıktı; oran yaygınlıkla artıyor: %11–14'te %9–21, %24–26'da %47–58, %36 üstünde %86–95 [Hesap: `docs/log/2026-10-31-volkan-faz1.md`, yapay ışınım, gösterim]. Soru (karar masasına, 31 Ekim): yaygınlık aralığı mı, gerilim aralığı mı daraltılmalı, yoksa bulgu olarak mı kalmalı?

Bugünün Kıbrıs'ı:
- Kıb-Tek 2023 üretim tablosunda PV üretimi 110.371 MWh, toplam üretimin %5,81'i; 2024 Ocak–Temmuz 75.964 MWh, %6,33; Nisan 2023'te aylık üretimin %9,4'ü [Kaynaklı: Kıb-Tek 2023 ve 2024 istatistik, "PV toplam" satırı; `data/raw/kibtek-istatistik/KAYNAK.txt`].
- Kıbrıs'ta yılda kWp başına ~1.600 kWh alınırsa [Yorum] kurulu PV ~70 MWp [Hesap]; 2022 ortasında "95 MW kurulu fotovoltaik" deniyordu [Kaynaklı: Kıbrıs Postası, 4 Temmuz 2022; kaynak kişi belirtilmemiş].
- Bunun tamamı konut çatısı olsaydı 6,5 kW'tan 10.600–14.600 ev, yani konut abonelerinin (175.577) %6–8'i [Hesap]. Gerçekte güneş santralleri ve ticari çatılar da bu toplamın içinde; ülke genelinde konut yaygınlığı kabaca %2–6 [Hesap + Yorum]. Bekleyen 2.670 başvuru +%1,5 [Kaynaklı: KTTO raporu, Mart 2023].
- Yaygınlık mahalleye göre kümelenir (komşu etkisi, aynı müteahhit, yeni siteler); ülke ortalamasının birkaç katına çıkan trafolar olur [Yorum].
- Doğrudan "mahsuplaşmadaki konut abonesi sayısı" BULAMADIM (web araması; Kıb-Tek istatistik PDF'lerinde yok).

Seçenekler: (a) yaygınlık aralığını bugüne çapala; (b) gerilim aralığını daralt; (c) olduğu gibi bırak, bulgu say; (d) inverterin 264 V'ta kapanmasını modelle.

## Karar
(a). Panel yaygınlığı şehir başına **%3–25** (düzgün dağılım; hat sonuna doğru artan konum ağırlığı aynı). Trafo çıkışı **246–250 V değişmez**: şartname boşta 250 V, kademe bilinmiyor; ADR-0002'nin "Kıbrıs'ta önce gerilim bağlar" savı tam da burada sınanıyor, aralık daraltılarak gizlenmez. %55 bulgusu silinmez: günlükte kalır ve `ayar.json`'daki `panel_yayginligi` ile banda göre raporlanır; sunumda "yaygınlık %25'i geçince konut trafolarının yarısı dolar" cümlesinin dayanağıdır (gösterim). (d) şimdi değil: `v_max` 264 V üstü değerler fiziksel değildir, "gösterim" etiketiyle kalır; Faz 3 zaten 259 V sınırını kullanır.

## Sonuç
- Artı: Şehirler bugünün Kıbrıs'ına benzer; Faz 3 sınavı için yeşil/sarı/kırmızı karışımı oluşur (ilk ölçümde %11–14 yaygınlıkta konut trafolarının %9–21'i, %24–26'da yarısı dolu). ADR-0003 bozulmaz: aralık yine rastgele, yalnız kanıta çapalı. Faz 1 sınavındaki "en az bir trafo bugün 259 V üstü" maddesi sağlanır.
- Eksi: %3–25 bir tahmin [Yorum]; ülke geneli konut yaygınlığı doğrudan bulunamadı → uzmana soru: "Kaç konut abonesi mahsuplaşmada?" Gelecek senaryosu (yaygınlık %40+) Faz 1'de yok; istenirse ayrı bir "gelecek" şehir kümesi üretilir, aynı üreticiyle.
- Uygulama (ana oturum): ROADMAP Faz 1 rastgeleleştirme satırı ve `src/sehir_uret.py`'deki aralık (PR #6); 20 şehir yeniden üretilir.
