# Dashboard (`dashboard/`)

Haritadan ayrı, tek sayfa: projenin kimliği, şehir özetleri, bütün trafo verisi ve resmi rakamlar. Harita (`app/`, Civan) ayrı kalır; bu klasör `app/`'e dokunmaz.

## Çalıştırma

```bash
streamlit run dashboard/dashboard.py
```

Tarayıcıda `http://localhost:8501` (harita açıksa bir sonraki port). Gereken paketler haritanınkiyle aynı (`streamlit`, `pandas`, `pydeck`; `altair` Streamlit'le gelir).

## Sekmeler

| Sekme | Ne gösterir |
|---|---|
| Özet | Trafo, ölçülen trafo, abone, kurulu panel. **Panel katmanı:** trafo renkleri, güvenli uçlar, kaç ev daha (yaklaşık N, A–B), %40 kuralı, güneş payının dolu kısmı, kural ile renklerin yan yana tablosu (civan.md KARAR 18:46, 19:13, 20:56). **Yük haritası:** doluluk, %80'den dolu olabilecek trafo, gücü aşabilecek trafo, akşam gerilimi, boş güç; doluluk dağılımı ve tepe zamanı. |
| Trafolar | Bütün trafolar, süzgeçle (renk, bölge, ölçüm, trafo no). Satıra tıklayınca kart: kimlik (Kıb-Tek'in bildiği), panel katmanı, yük haritası, günlük eğri, konum. |
| Şehirler | Veri setindeki her şehir bir satır; şehir şehir renk çubukları. |
| Model ne kadar iyi | Resmi rakamlar katmana göre (sorun, panel, yük haritası): durum (geçti / kaldı / uyarı / bilgi), veri türü, kapsam, depodaki kaynağa bağlantı. |
| Proje | Sorun, kullanıcı, yöntem, renklerin anlamı, iki soru, takım, sözlük, veri kaynakları (`data/raw/*/KAYNAK.txt`'ten okunur). |
| Ham veri | Şehrin her tablosu, CSV indirme. |

## Veri değişince

- **Şehir verisi:** `data/synthetic/` ve altındaki klasörler okunur (ör. `data/synthetic/u15/sehir-031`); sol menüden veri seti ve şehir seçilir. Yeni şehir klasörünü koy, sayfayı yenile; kod değişmez. Başka bir kök için `DASHBOARD_VERI=<klasör> streamlit run dashboard/dashboard.py`.
- **Kimlik, resmi rakamlar, sözlük:** [icerik.json](icerik.json). Yeni sonuç gelince yalnız o dosya değişir. Her rakamda katman (`panel` / `yuk` / `sorun`), veri türü (`farazi` / `gercek` / `kaynakli` / `sahte_kayit`), durum (`gecti` / `kaldi` / `uyari` / `bilgi`) ve depodaki kaynak dosyası yazılı.
- Eksik tablo sayfayı bozmaz: `kac_ev.csv` yoksa panel bölümü, `tepe.csv` yoksa yük bölümü üretme komutunu gösterir.

## Kurallar

- `cevap_anahtari.csv` okunmaz; `yuk_5dk.csv`'den yalnız ölçülü trafoların satırları okunur (sözleşme).
- Etiket haritayla aynı: şehir 900+ "SAHTE VERİ", 800–899 "GERÇEK ÖLÇÜM … (Kıbrıs değil)", diğerleri "örnek veri (farazi şehir) — gösterim".
- Dil: "en az" yok; "yaklaşık N ev (A–B)" ve "%80 ihtimalle"; vaat renkte. Her rakamın yanında katmanı (panel ya da yük haritası) yazılı.
- Renkler haritayla aynı ve her zaman yazısıyla birlikte.

## Denendi

Mac, Python 3.12, Streamlit 1.66: bütün şehirler, tek şehir, veri yok ve yalnız trafo tablosu olan şehirde hata yok (Streamlit `AppTest`); tarayıcıda koyu ve açık tema, telefon genişliği. Deneme verisi üretici 1.5 sınav şehirleri 31–40 (tepe tablosu `src/tepe.py` ile üretildi). Windows denenmedi.
