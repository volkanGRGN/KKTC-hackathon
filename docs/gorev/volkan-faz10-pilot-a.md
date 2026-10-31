# Volkan (+ Claude, BUILD) — Faz 10 — Pilot A, ucuz ölçüm: hazırlık

Tüzük: geçerli ([docs/tuzuk.md](../tuzuk.md)). Karar: karar masası 21:15 ve 21:25 (Faz 10 satırı), 22:21 ve ADR-0016 (karamsar yönler burada yeniden kalibre edilir). Dal `hazirlik/faz10`, PR.

Amaç (1 cümle): Kıbrıs'tan ilk gerçek gerilim verisini tüzük kartlarıyla toplamak ve işlemek; veri gelmeden önce neyin doğrulamaya, neyin ayara gideceğini yazıp dondurmak.

## Veri partileri (taslak; her parti geldiğinde bu alanlarla kendi kartı açılır)

### P6 — panelli evin inverter gerilim kaydı (`P6-inverter-ev-NN`)
- **Kaynak:** ev sahibinin inverter uygulaması ya da web portalı, bir hafta, ~5 dk. Ev sahibinin izniyle; isteyen Volkan, ekip kimseden veri istemez.
- **Kapsam:** tek ev; hattın neresinde olduğu ve fazı genelde bilinmez. Gece kaydı büyük olasılıkla yok: şebekeye bağlı inverter güneş batınca uyur.
- **Veri sözleşmesi:** zaman (yerel saat), faz başına şebeke gerilimi (V), varsa etkin güç. Ölçüm inverter ucunda, sayaçtan biraz yüksek. Bazı markalar anlık değer, bazıları 15 dk ortalama yazar; ortalama kısa tepeleri saklar.
- **Bilinen yanlılık:** yalnız panelli ev; gece seviyesi yerine sabahın ilk değeri.
- **Kişisel veri:** ad, adres, seri numarası depoya girmez. Ev kodla anılır (`ev-01`), konum en fazla bölge düzeyinde ("Girne"). Ham dosya depo dışında; `data/raw/inverter-p6/KAYNAK.txt` kişisel bilgisiz (tarih, marka, süre, SHA-256).
- **Kullanım bölünmesi (DONDURULDU 31 Ekim 22:35, değer görülmeden):** ilk 5 ev **doğrulama**, hiçbir ayara girmez; 6. evden sonra çift sıra numaralı evler ayar, tekler doğrulama. Tek ev "gösterim"; doğrulama için tüzük madde 6'nın ~150 bağımsız karar noktası hedefi geçerli.
- **İşleme:** `src/inverter_kaydi.py` (gece veya sabah seviyesi, öğlen 11–14 yükselmesi, 253 V ve 259 V üstü süre, 10 dk ortalaması; modelin panelli şehir konutu dağılımıyla kıyas).
- **Hipotez:** sabah seviyesi modelin bara bandında (P10–P90 245–251 V); öğlen yükselmesi modelin bara üstü dağılımında (3,4–10,5 V; trafonun en kötü evi, tek ev bunun altında kalabilir).

### P7 — gerilim ölçen akıllı priz (`P7-priz-ev-NN`)
- **Kaynak:** birkaç evde 15–20 €'luk priz, gece 00–05. Satın alma ve kurulum Volkan'ın.
- **Ne verir:** gece bara seviyesine en yakın değer; P6'nın gece boşluğunu kapatır.
- **Kullanım:** bara bandının (244–252 V, karar masası 16:27, İngiltere çapası) ilk Kıbrıs çapası. Bölünme P6 ile aynı kural.

### P8 — trafo plakası fotoğrafı (`P8-plaka-trafo-NN`)
- **Ne verir:** kısa devre gerilimi (uk), kademe aralığı ve ayarı (uzmana soru 8).
- **Kullanım:** kademe → boşta bara gerilimi; modelin `V0` aralığı ve trafo empedansı (`uk` %4 [Yorum]) için ilk çapa.

### P9 — Kıb-Tek kayıtları (Faz 9 ile)
İstek metni [kibtek-veri-istegi-taslak.md](../istek/kibtek-veri-istegi-taslak.md). Gelince kendi kartı.

## Faz 10'da yeniden kalibre edilecekler (ADR-0016)
- Kırmızı olasılığı kovaları karamsar: 0,5–0,7 → gerçekte %34, 0,7–0,9 → %68 (üretici 1.3 sınav 21–30).
- Kaç ev bandının üst ucu karamsar: gerçek iyimser sayının üstünde %16 trafoda.
- İspanya PIT şekli: k ile genişlik düzeldi, şekil düzelmedi (0,068 → 0,102).
- Yalnız ayar payındaki ölçümle; doğrulama payı dokunulmaz (tüzük madde 1). Her bakış [hold-out defterine](../log/holdout-defteri.md).

## Adımlar
1. P6 gelince: `python3 src/inverter_kaydi.py <kayıt>` → tek ev raporu, Faz 10 günlüğüne; KAYNAK.txt kişisel bilgisiz; hold-out defterine bir satır.
2. P7 için alışveriş listesi ve kurulum notu (Volkan).
3. P8 için fotoğraf talimatı: plakanın tamamı, okunur; trafo numarası ve konum fotoğrafa girmez.
4. Yeterli ayar verisi birikince: `src/kalibrasyon.py`'ye kova kalibrasyonu (asimetrik) — veri gelmeden yazılmaz.

Nasıl denenir: `python3 src/inverter_kaydi.py <yapay kayıt>`; yapay kayıtla iki biçim sınandı (gece kayıtlı tek faz, gecesiz üç faz).

Bitti sayılması için (iki seviye, tüzük §5): **parti bitti** = kart, rapor, günlük, defter satırı; **faz bitti** = taze doğrulama payında kapılar ve kalibrasyon tutuyor, yeni ölçüm ölçüyü artık oynatmıyor.

Dokunulmayacak: Can'ın dosyaları (`src/sinav.py`, `src/grafikler.py`, `src/profiller.py`, `src/edp_kiyas.py`), `app/` (Civan).

Karar masasına yaz: ilk ölçüm modelin bara bandının ya da yükselme dağılımının dışındaysa; kişisel veri riski görülürse.
