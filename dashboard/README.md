# Dashboard (`dashboard/`)

Haritadan ayrı uygulama. Sayfalar: **Kıbrısçık'a genel bakış** (proje kimliği, özet, rakamlar ne kadar tutuyor, proje ve ekip; teknik tablolar "Ekip için"de), **Harita** (Civan'ın haritası, `app/harita.py`; onun düzeni yoksa gizli) ve **Kıbrısçık'ta canlı tahmin** (bütün ada; Girne'de birkaç trafoyu ölç, model gerisini tahmin eder; Oynat). Bu klasör `app/`'e yazmaz. **Dil herkesin anlayacağı gibi** (Volkan, 1 Kasım: site pitch sunumunda kullanılacak): teknik terim yok ya da yanında açıklaması; her rakamın altında tek cümle.

## Çalıştırma

```bash
streamlit run dashboard/dashboard.py
```

Tarayıcıda `http://localhost:8501` (harita açıksa bir sonraki port). Sayfalar sol menüde. Gereken paketler haritanınkiyle ve modelinkiyle aynı (`streamlit` ≥ 1.46, `pandas`, `pydeck`, `numpy`, `scipy`, `scikit-learn`; `altair` Streamlit'le gelir). Eski model sürümleri için `git` gerekir.

## Kıbrısçık'a genel bakış: sekmeler

Sunumda görünenler önde, ekibin çalışma tabloları "Ekip için"de (silinmedi).

| Sekme | Ne gösterir |
|---|---|
| Özet | Trafo, ölçülen trafo, abone, kurulu panel. **Trafo ne kadar dolu?** (yılın en yoğun saati): tipik doluluk, önce bakılacak, gücünü aşabilecek, akşam gerilimi düşebilecek, boş güç; doluluk dağılımı ve en yoğun saat. **Güneş paneli için ne kadar yer var?** (bahar öğleni): renkler, emin olduğumuz trafolar, kaç ev daha (yaklaşık N, A–B), bugünkü %40 kuralı, kural ile renklerin yan yana tablosu. |
| Ne kadar tutuyor | Resmi rakamlar konuya göre (sorun, doluluk, güneş paneli, maliyet): durum (hedefte / hedefin biraz dışında / dikkat / bilgi), veri türü, tek cümlelik açıklama, kapsam ve kaynak bağlantısı. Metinler `icerik.json`'da. |
| Proje ve ekip | Sorun, kullanıcı, yöntem, karar, renklerin anlamı, iki soru, takım, sözlük (açık). |
| Ekip için | Verinin teknik kimliği (üretici, sözleşme, hava yılı) ve alt sekmeler: **Trafolar** (süzgeçli tablo, satıra tıklayınca kart), **Şehirler**, **Veri kaynakları** (`data/raw/*/KAYNAK.txt`), **Ham veri** (CSV indirme). |

## Harita sayfası

Civan'ın haritası olduğu gibi: sütun = trafo, renk = karar, boy = trafo gücü, beyaz uç = ölçüm cihazı var; Girne binaları, yollar ve kıyı internetsiz (`data/raw/osm-kasaba/`). İki fark: şehir dashboard'un veri setinden seçilir (alt klasörler dahil) ve Civan'ın menüyü gizleyen ayarı uygulanmaz (yoksa sayfa menüsü kaybolur). Civan haritasını güncelleyince sayfa da güncellenir.

## Canlı tahmin sayfası

- **Harita kendi çizimimiz** (`canli_harita.py` + `canli_harita.js`, tuval; harita karosu yok, internetsiz; Volkan 1 Kasım "harita bizim olsun"): ada Natural Earth 1:50m (`app/ada_kiyi.json`, Civan'ın, yalnız okunur), Girne kıyısı ve binaları OSM (`data/raw/osm-kasaba/`, git dışı; yoksa yalnız ada çizimi). **Ölçülen trafo dolu nokta (kalın kontur), tahmin soluk halka, henüz tahmin yok gri nokta.** Etiket her karede: "gösterim — Kıbrısçık ülkesindeki şehirler · noktalar temsili" (Volkan 1 Kasım: deneme şehirlerinin adı "farazi şehir" değil Kıbrısçık ülkesindeki şehirler; yine gösterim).
- **Normal harita bütün ada** (animasyonun sonundaki görünüm; tam genişlik, sayılar altında): Güney soluk, Kuzey belirgin; seçilen şehir Girne'de canlı, veri setindeki öbür şehirler kasabalara temsili yerleşir (`KASABALAR`, küçültme 0,55; gerçek trafo yeri değil) ve her birinin resmi 12 ölçümlü çıktısıyla boyanır (`tahmin.csv`, `tepe.csv`, `kac_ev.csv`). Tekerlek, sürükleme, çift tıklama, +/− ve "Girne" / "Kıbrıs" düğmeleriyle yakınlaşılır. Uzaktan bakınca başlık bütün adanın özeti.
- **Trafoya tıkla: kart açılır** (Malta haritası gibi): trafo gücü, yük haritası (yılın tepesi, doluluk, akşam gerilimi), panel rengi ve kaç ev, öğlen yükü; sınav açıksa gerçek. Girne trafosunun kartında "Ölçülmüş say (cihaz takıldı)" / "Ölçümü kaldır". **Girne'de harita kapalı açılır:** en az 3 ölçümle model kurulur ve ölçülmeyen bütün trafoları boyar; her ölçümde yeniden kurulur (~1 sn). Ölçüm sağdaki listeden de eklenip çıkarılır.
- **Düğmeler:** "Önerilen 12 trafoyu ölç" (ürünün tabakalı seçimi, resmi koşuyla aynı), "Bir trafo daha ölç", "Oynat", "Sıfırla". **"Ayrıntı" köşesi** (kapalı): haritadaki soru (doluluk / güneş paneli), gerçekle karşılaştırma, model sürümü. Sunumda ekranda yalnız harita, düğmeler ve birkaç sayı kalır.
- **Oynat (yarım dakika, kendi oynar):** her yer karanlık. Girne'de bir trafo ölçülür, çevresi küçük bir aydınlık daire olur; sonra sağdaki, sonra soldaki mahallede. 3 ölçümle model kurulur, tahminler karanlıkta belirir (az ölçüp çoğunu tahmin); 12 ölçüme kadar sürer. Sonra karanlık kalkar, görünüm adaya açılır, kasabalar sırayla dolar (önce ölçülenler, sonra tahminler). Haritada duraklat / baştan; bitince harita kendiliğinden normal haritaya geçer, sayfa 12 ölçümlü Girne sonucunu gösterir (sınav açıksa ölçtükçe hata grafiği 3–12 dolar).
  - Sıra: ürünün önerdiği 12 trafo; ilki Girne merkezine en yakın, ikincisi onun doğusu (sağ), üçüncüsü batısı (sol), kalanı uzaklık sırasıyla. Küme aynı olduğu için 12. adım resmi koşuyla birebir (sehir-031, 40/40). Her trafo bir ölçülen trafonun adımında belirir (en yakından başlayarak adım başına en çok 4).
  - Renkler gerçek modelden: Girne'de her adım o anki ölçülerle canlı kurulur (ilk Oynat ~10–15 sn hazırlık, sonra önbellekte); kasabalarda resmi çıktılar.
- **Katman:** yük haritası (yılın tepesi; renk temkinli uçtaki doluluğa göre: %80 altı / %80–100 önce bak / %100 üstü; eşikler gösterim) ya da panel (öğlen gerilimi, 259 V; yeşil / sarı / kırmızı).
- **Model sürümü** ("Ayrıntı" köşesinde): güncel ve depo tarihçesinden üç eski sürüm (1 Kasım 10:22 B-Y2 öncesi, 1 Kasım 01:59 yük haritası ilk sürüm, 31 Ekim 23:33 kalibrasyon sonrası, 31 Ekim 21:33 sunum v1). Eski sürümün kodu `git archive` ile geçici klasöre (her depo kopyasına ayrı; veri bağlantısı her çağrıda doğrulanır) çıkarılır ve ayrı süreçte koşar; ölçümler sürüm değişince yerinde kalır, aynı test sürümler arasında karşılaştırılır. Yük haritası olmayan sürümde panel gösterilir.
- **Gerçekle karşılaştırma (sınav görünümü; "Ayrıntı" köşesinde, açılışta kapalı):** yalnız deneme şehrinde, yalnız ölçülmeyen trafolarda: tepe hatası, öğlen yükü hatası, yanlış yeşil, %40 kuralının yanlış yeşili; "ölçtükçe hata" grafiği. Gerçek cevap anahtarından gelir; **model onu görmez** (hesap `canli.py`'de, kıyas ayrı fonksiyonda). Sözleşmede harita cevap anahtarını okumaz; bu görünüm sinav.py gibi yalnız puanlar, kapatılabilir.
- **Hesap ürünün kendi kodu:** öğlen yükü `src/sablon.py`, renk ve kaç ev `src/kac_ev_olasilik.py`, yılın tepesi `src/tepe.py` (geçici klasörde; şehir klasörüne yazmaz). Resmi 12 ölçümle sonuç main'deki `tahmin.csv`, `kac_ev.csv` ve `tepe.csv` ile birebir (sehir-031 ve -036, 40/40).
- **Az ölçümde dikkat:** 8'in altında %80 aralık birkaç artıktan çıkıyor, fazla dar; sayfa uyarır. 3 ölçümle model sehir-031'de 11 trafoya yeşil dedi (12 ölçümle 12).

## Veri değişince

- **Şehir verisi:** `data/synthetic/` ve altındaki klasörler okunur (ör. `data/synthetic/u15/sehir-031`); sol menüden veri seti ve şehir seçilir. Yeni şehir klasörünü koy, sayfayı yenile; kod değişmez. Başka bir kök için `DASHBOARD_VERI=<klasör> streamlit run dashboard/dashboard.py`.
- **Kimlik, resmi rakamlar, sözlük:** [icerik.json](icerik.json). Yeni sonuç gelince yalnız o dosya değişir. Her rakamda katman (`panel` / `yuk` / `sorun`), veri türü (`farazi` / `gercek` / `kaynakli` / `sahte_kayit`), durum (`gecti` / `kaldi` / `uyari` / `bilgi`) ve depodaki kaynak dosyası yazılı.
- Eksik tablo sayfayı bozmaz: `kac_ev.csv` yoksa panel bölümü, `tepe.csv` yoksa yük bölümü üretme komutunu gösterir.

## Kurallar

- Genel bakış ve Harita `cevap_anahtari.csv`'yi okumaz. Canlı tahmin onu yalnız sınav görünümünde okur ve modele vermez (kapatılabilir). `yuk_5dk.csv`'den modele yalnız ölçülü (seçilen) trafoların satırları girer (sözleşme).
- Etiket: şehir 900+ "SAHTE VERİ", 800–899 "GERÇEK ÖLÇÜM … (Kıbrıs değil)", diğerleri "gösterim — Kıbrısçık ülkesindeki şehirler" (Volkan, 1 Kasım: deneme şehirlerinin adı "farazi şehir" değil).
- Dil: "en az" yok; "yaklaşık N ev (A–B)" ve "%80 ihtimalle"; vaat renkte. Her rakamın yanında katmanı (panel ya da yük haritası) yazılı.
- Renkler haritayla aynı ve her zaman yazısıyla birlikte.

## Denendi

Mac, Python 3.12, Streamlit 1.66: Genel bakış (bütün şehirler, tek şehir, veri yok, yalnız trafo tablosu olan şehir), Harita ve Canlı tahmin (önerilen 12, katman, dört sürüm, sıfırla) `AppTest` ile hatasız; tarayıcıda tıklayarak ölçme, sürüm değiştirme. Yeni harita (1 Kasım): `AppTest` ile açılış, önerilen 12, katman, Oynat, Haritaya dön, üç ölçüm, sıfırla, eski sürümle (B-Y2 öncesi, sunum v1) Oynat hatasız; tarayıcıda (açık ve koyu tema) yakınlaşma, Girne ve kasaba trafosunun kartı, karttan ölçme, Oynat baştan sona (karanlık ve daireler), duraklat, baştan, bitince normal haritaya geçiş. Haritanın tıklama ve animasyon olayları (`st.components.v2`) `AppTest`'te denenemiyor, yalnız tarayıcıda. Deneme verisi üretici 1.5 sınav şehirleri 31–40. Windows denenmedi; Windows'ta süreç havuzu ve `git archive` denenmedi.
