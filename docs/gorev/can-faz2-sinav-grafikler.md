# Can — Faz 2 — sınav ölçüleri, grafikler, gerçek veri adayı

Kartı yazan: Volkan (+ Claude), 31 Ekim 2026. Sözleşme: [docs/data/tablo-bicimi.md](../data/tablo-bicimi.md) §5 (`tahmin.csv`, `arketipler.csv`). Yöntem: [docs/method/modeling.md](../method/modeling.md), ölçüler: [docs/method/validation.md](../method/validation.md).

**Amaç (1 cümle):** Modelin (`src/sablon.py`, Volkan + Claude) tahminlerini cevap anahtarıyla karşılaştırıp ROADMAP Faz 2 geçme sınavını ölçmek, iki grafiği çizmek ve bir gerçek veri adayını kısa bir zaman kutusunda denemek. Modeli yazan sınavı yazmaz.

**Girdi:**
- Şehirler: `data/synthetic/sehir-NNN/` (`python3 src/sehir_uret.py 1 20`; artık gerçek Lefkoşa ışınımı ve %3–25 panel yaygınlığıyla).
- Model çıktısı, her şehir klasöründe ([sözleşme §5](../data/tablo-bicimi.md)):
  - `tahmin.csv` (ana çalıştırma, 12 ölçülü trafo) ve `arketipler.csv`.
  - `deney/tahmin_n<5|10|20>_t<1..5>.csv`: aynı sütunlar, farklı ölçülü sayısı ve tekrar.
  - `deney/tahmin_capraz_s<AAA>.csv`: şehirler arası; model AAA şehrinin ölçülü trafolarıyla kuruldu, bu şehrin bütün trafolarını tahmin etti (`olculdu` hepsinde 0). Sözleşmeye `sablon/ilk-surum` PR'ında eklenecek; ad kesin.
- `sablon.py` gelene kadar: sözleşme biçiminde sahte bir `tahmin.csv` / `arketipler.csv` üret (ör. `ogle_min_kw` = gerçek × rastgele 0,8–1,2, bant ±%25) ve onunla test et. Sahte dosyayı depoya koyma.

**Çıktı:**
1. `src/sinav.py` içinde `faz2` bölümü: `python3 src/sinav.py faz2 data/synthetic` → her madde GEÇTİ/KALDI ve rakam; her ölçü **ortanca + en kötü şehir**.
2. `src/grafikler.py`: `python3 src/grafikler.py faz2 data/synthetic outputs/` → iki PNG; her grafikte "gösterim — farazi şehirler" yazısı.
3. Veri adımı: İspanya EDP için KAYNAK.txt + veri sözlüğü satırı (kullanılır / elendi + neden).

**Adımlar:**
1. (≤ 1 saat) `sinav.py faz2`. Yalnız `olculdu` = 0 olan trafolar ölçülür (ölçülüler zaten biliniyor). Ölçüler:
   - **Doğru arketip oranı.** Trafonun "gerçek kümesi": `yuk_5dk.csv`'den o trafonun iş günü ortalama `tuketim_kw` eğrisi (adım başına ortalama), tepesine bölünür; `arketipler.csv`'deki `gun_turu` = `isgunu` eğrilerinden (`oran`) öklid uzaklığı en küçük olan arketip. `tahmin.csv`'deki `arketip` buna eşitse doğru. Eşik: ortanca ≥ %75.
   - **Öğlen en düşük yük hatası**: |`ogle_min_kw` (tahmin) − `ogle_min_kw` (cevap anahtarı)| ÷ gerçek. Gerçek < 1 kW olanı atla ve say. Eşik: ortanca ≤ %15, P90 ≤ %30 (şehir başına ortanca ve P90; sonra şehirlerin ortancası ve en kötüsü).
   - **Bant kapsama**: gerçek, [`p10`, `p90`] içinde olan oran. Eşik: %70–90 (altı = sahte güven, üstü = bant gereğinden geniş).
   - **Şehirler arası**: aynı şehirde `deney/tahmin_capraz_s*.csv` hata ortancası ÷ `tahmin.csv` hata ortancası. Eşik: ≤ 1,5.
   - **Düşük güven oranı**: `guven` = `dusuk` payı. Hedef ≤ %25; aşarsa madde KALDI değil "UYARI", sebebini Volkan'ın günlüğü yazar.
   - **Ölçülü / ölçülmeyen tip dağılımı**: cevap anahtarındaki `tip`, `olculdu` = 1 ve 0 için ayrı sayım; şehirlerin toplamı ve en çok farklı şehir. Eşiksiz, bilgi satırı (ROADMAP "karşılaştırılmış, günlükte").
   - Bilgi (eşiksiz): güven etiketine göre hata ortancası (yüksek < orta < düşük olmalı; değilse güven etiketi işe yaramıyor) ve tip başına hata ortancası.
2. (≤ 45 dk) `grafikler.py`:
   - **Kalibrasyon**: şehir başına bant kapsama (nokta) ve %70–90 hedef şeridi; yanına gerçeğin P10'un altında ve P90'ın üstünde kalan payı (iki taraf dengeli mi).
   - **Kaç trafo ölçmeli**: x = ölçülü sayısı (5, 10, 12, 20), y = hata ortancası (tekrarların ve şehirlerin ortancası, P10–P90 gölgesiyle); ikinci çizgi bant kapsama. Faz 3'te aynı grafiğe yanlış yeşil eklenecek.
3. (≤ 2 saat, **zaman kutusu**; olmazsa bırak, nedeni günlüğe) İspanya EDP (Mendeley 685vgp64sm, CC BY 4.0): indir, trafo başına toplam yük çıkarılabiliyor mu, çözünürlük, abone tipi var mı. Eleme ölçütü Faz 1'deki gibi (Kıbrıs/Akdeniz · ölçülmüş · ≤ 1 saat · kaynak ve lisans · bu fazda kullanılacağı belli). Kullanılabilirse veri sözlüğüne "gerçek doğrulama adayı" diye yaz ve Volkan'ın kutusuna `UYARI!` ile bildir; modeli onun üstünde koşmak Volkan'ın işi (2i). NGED kaydını Volkan açar; sen açma.
4. (≤ 15 dk) Günlük `docs/log/2026-10-31-can-faz2.md`: sahte dosyayla deneme çıktısı, sonra gerçek `tahmin.csv` gelince 20 şehrin sonucu (append-only).

**Nasıl denenir:**
- Sahte dosyayla: `python3 src/sinav.py faz2 data/synthetic` → yedi satır; sahte hatalar ±%20 ise hata ortancası ~%10, kapsama ~%90 civarı çıkmalı (ölçünün kendisi doğru mu).
- `sablon.py` main'e gelince: `python3 src/sablon.py data/synthetic` sonra aynı komut.

**Bitti sayılması için:**
- [ ] `sinav.py faz2` 20 şehirde çalışıyor; yedi madde rakamla `docs/log/2026-10-31-can-faz2.md`'de.
- [ ] İki grafik `outputs/` altında üretiliyor, "gösterim" yazılı; dosya adları günlükte.
- [ ] EDP için veri sözlüğünde satır (kullanılır ya da elendi + neden), indirildiyse KAYNAK.txt.
- [ ] Faz 1 sınavı (`sinav.py faz1`) bozulmadı.

**Dokunulmayacak dosyalar:** `src/sablon.py`, `src/sehir_uret.py`, `src/trafo_bos_kapasite.py`, `docs/data/tablo-bicimi.md`, `docs/method/`, `app/`. `sablon.py` çıktısında eksik ya da sözleşmeye uymayan sütun görürsen Volkan'ın kutusuna.

**Kendin karar ver (sorma, günlüğe yaz):** `sinav.py` ve `grafikler.py` içindeki uygulama ayrıntısı (okuma, çıktı metni, grafik düzeni, renk); "gerçek < 1 kW" gibi küçük atlama kuralları (sayısını yaz); EDP'yi zaman kutusu dolunca bırakmak; dal adı (yeni dosya `grafikler.py` ilk sürümü: dal + PR, `sinav/faz2`).

**Karar masasına yaz (`volkan.md`, bekleme, sıradaki işe geç):** bir ölçünün tanımı belirsizse (ör. "gerçek küme" kuralı bir tipte saçma sonuç veriyorsa); eşik tartışmalıysa (değeri ayarlama); EDP kullanılabilir çıkarsa; `tahmin.csv`'de sözleşmede olmayan bir sütuna ihtiyaç.

**Takılırsan:** önce sahte `tahmin.csv` ile tek şehirde dene; sonra istek kutusu (sormadan) / bloklarsa sesli.
