# Dashboard (`dashboard/`)

Haritadan ayrı uygulama, üç sayfa: **Genel bakış** (proje kimliği, şehir özetleri, bütün trafo verisi, resmi rakamlar), **Harita** (Civan'ın haritası, `app/harita.py`) ve **Canlı tahmin** (harita kapalı açılır; trafoya tıkla, ölçülmüş sayılır; model o an kurulur, gerisini tahmin eder). Bu klasör `app/`'e yazmaz; Civan'ın haritası onun fonksiyonları çağrılarak gösterilir.

## Çalıştırma

```bash
streamlit run dashboard/dashboard.py
```

Tarayıcıda `http://localhost:8501` (harita açıksa bir sonraki port). Sayfalar sol menüde. Gereken paketler haritanınkiyle ve modelinkiyle aynı (`streamlit` ≥ 1.46, `pandas`, `pydeck`, `numpy`, `scipy`, `scikit-learn`; `altair` Streamlit'le gelir). Eski model sürümleri için `git` gerekir.

## Genel bakış sayfasının sekmeleri

| Sekme | Ne gösterir |
|---|---|
| Özet | Trafo, ölçülen trafo, abone, kurulu panel. **Panel katmanı:** trafo renkleri, güvenli uçlar, kaç ev daha (yaklaşık N, A–B), %40 kuralı, güneş payının dolu kısmı, kural ile renklerin yan yana tablosu (civan.md KARAR 18:46, 19:13, 20:56). **Yük haritası:** doluluk, %80'den dolu olabilecek trafo, gücü aşabilecek trafo, akşam gerilimi, boş güç; doluluk dağılımı ve tepe zamanı. |
| Trafolar | Bütün trafolar, süzgeçle (renk, bölge, ölçüm, trafo no). Satıra tıklayınca kart: kimlik (Kıb-Tek'in bildiği), panel katmanı, yük haritası, günlük eğri, konum. |
| Şehirler | Veri setindeki her şehir bir satır; şehir şehir renk çubukları. |
| Model ne kadar iyi | Resmi rakamlar katmana göre (sorun, panel, yük haritası): durum (geçti / kaldı / uyarı / bilgi), veri türü, kapsam, depodaki kaynağa bağlantı. |
| Proje | Sorun, kullanıcı, yöntem, renklerin anlamı, iki soru, takım, sözlük, veri kaynakları (`data/raw/*/KAYNAK.txt`'ten okunur). |
| Ham veri | Şehrin her tablosu, CSV indirme. |

## Harita sayfası

Civan'ın haritası olduğu gibi: sütun = trafo, renk = karar, boy = trafo gücü, beyaz uç = ölçüm cihazı var; Girne binaları, yollar ve kıyı internetsiz (`data/raw/osm-kasaba/`). İki fark: şehir dashboard'un veri setinden seçilir (alt klasörler dahil) ve Civan'ın menüyü gizleyen ayarı uygulanmaz (yoksa sayfa menüsü kaybolur). Civan haritasını güncelleyince sayfa da güncellenir.

## Canlı tahmin sayfası

- **Harita kapalı açılır:** bütün trafolar gri. Bir sütuna tıkla: ölçülmüş sayılır (beyaz uç). En az 3 ölçümle model kurulur ve ölçülmeyen bütün trafoları boyar; her tıklamada yeniden kurulur (~1 sn). Ölçümü kaldırmak için sağdaki listeden çıkar.
- **Düğmeler:** "Önerilen 12'yi ölç" (ürünün tabakalı seçimi, resmi koşuyla aynı), "Önerilenden 1 ekle", "Sırayla oynat" (kapalı haritadan 12'ye birer birer), "Sıfırla".
- **Katman:** yük haritası (yılın tepesi; renk temkinli uçtaki doluluğa göre: %80 altı / %80–100 önce bak / %100 üstü; eşikler gösterim) ya da panel (öğlen gerilimi, 259 V; yeşil / sarı / kırmızı).
- **Model sürümü** (sol menü): güncel ve depo tarihçesinden üç eski sürüm (1 Kasım 01:59 yük haritası ilk sürüm, 31 Ekim 23:33 kalibrasyon sonrası, 31 Ekim 21:33 sunum v1). Eski sürümün kodu `git archive` ile geçici klasöre çıkarılır ve ayrı süreçte koşar; ölçümler sürüm değişince yerinde kalır, aynı test sürümler arasında karşılaştırılır. Yük haritası olmayan sürümde panel gösterilir.
- **Gerçekle kıyas (sınav görünümü):** yalnız farazi şehirde, yalnız ölçülmeyen trafolarda: tepe hatası, öğlen yükü hatası, yanlış yeşil, %40 kuralının yanlış yeşili; "ölçtükçe hata" grafiği. Gerçek cevap anahtarından gelir; **model onu görmez** (hesap `canli.py`'de, kıyas ayrı fonksiyonda). Sözleşmede harita cevap anahtarını okumaz; bu görünüm sinav.py gibi yalnız puanlar, kapatılabilir.
- **Hesap ürünün kendi kodu:** öğlen yükü `src/sablon.py`, renk ve kaç ev `src/kac_ev_olasilik.py`, yılın tepesi `src/tepe.py` (geçici klasörde; şehir klasörüne yazmaz). Resmi 12 ölçümle sonuç main'deki `tahmin.csv`, `kac_ev.csv` ve `tepe.csv` ile birebir (sehir-031 ve -036, 40/40).
- **Az ölçümde dikkat:** 8'in altında %80 aralık birkaç artıktan çıkıyor, fazla dar; sayfa uyarır. 3 ölçümle model sehir-031'de 11 trafoya yeşil dedi (12 ölçümle 12).

## Veri değişince

- **Şehir verisi:** `data/synthetic/` ve altındaki klasörler okunur (ör. `data/synthetic/u15/sehir-031`); sol menüden veri seti ve şehir seçilir. Yeni şehir klasörünü koy, sayfayı yenile; kod değişmez. Başka bir kök için `DASHBOARD_VERI=<klasör> streamlit run dashboard/dashboard.py`.
- **Kimlik, resmi rakamlar, sözlük:** [icerik.json](icerik.json). Yeni sonuç gelince yalnız o dosya değişir. Her rakamda katman (`panel` / `yuk` / `sorun`), veri türü (`farazi` / `gercek` / `kaynakli` / `sahte_kayit`), durum (`gecti` / `kaldi` / `uyari` / `bilgi`) ve depodaki kaynak dosyası yazılı.
- Eksik tablo sayfayı bozmaz: `kac_ev.csv` yoksa panel bölümü, `tepe.csv` yoksa yük bölümü üretme komutunu gösterir.

## Kurallar

- Genel bakış ve Harita `cevap_anahtari.csv`'yi okumaz. Canlı tahmin onu yalnız sınav görünümünde okur ve modele vermez (kapatılabilir). `yuk_5dk.csv`'den modele yalnız ölçülü (seçilen) trafoların satırları girer (sözleşme).
- Etiket haritayla aynı: şehir 900+ "SAHTE VERİ", 800–899 "GERÇEK ÖLÇÜM … (Kıbrıs değil)", diğerleri "örnek veri (farazi şehir) — gösterim".
- Dil: "en az" yok; "yaklaşık N ev (A–B)" ve "%80 ihtimalle"; vaat renkte. Her rakamın yanında katmanı (panel ya da yük haritası) yazılı.
- Renkler haritayla aynı ve her zaman yazısıyla birlikte.

## Denendi

Mac, Python 3.12, Streamlit 1.66: Genel bakış (bütün şehirler, tek şehir, veri yok, yalnız trafo tablosu olan şehir), Harita ve Canlı tahmin (önerilen 12, katman, dört sürüm, sıfırla) `AppTest` ile hatasız; tarayıcıda tıklayarak ölçme, sırayla oynatma, sürüm değiştirme. Deneme verisi üretici 1.5 sınav şehirleri 31–40. Windows denenmedi; Windows'ta süreç havuzu ve `git archive` denenmedi.
