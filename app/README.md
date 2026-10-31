# Trafo haritası (`app/`)

Her trafo haritada bir 3D sütun: rengi karar (yeşil / sarı / kırmızı), boyu kaç ev daha panel takabileceği. Sütuna tıklayınca yan panelde trafonun bilgisi, tahmini ve günlük eğrisi açılır. Tablolar [sözleşmeye](../docs/data/tablo-bicimi.md) göre okunur; gerçek şehir gelince yalnız klasör değişir, kod değişmez.

Sahibi: Civan. Görev kartı: [civan-faz1-ornek-veri-harita](../docs/gorev/civan-faz1-ornek-veri-harita.md).

## Kurulum (bir kez)

Mac:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Windows (PowerShell; Git Bash'te ters eğik çizgi yerine `/`):

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

Harita için yalnız `streamlit` (≥ 1.39), `pydeck` ve `pandas` gerekir.

## Çalıştırma

1. Sahte şehirleri üret (`data/synthetic/sehir-901/`, `-902/`, `-903/`; depoya girmez):

   ```bash
   python3 app/ornek_veri.py
   ```

   Beklenen: `sehir-901: 40 trafo` gibi üç satır. Aynı komut her seferinde aynı dosyaları verir.

2. Haritayı aç:

   ```bash
   streamlit run app/harita.py
   ```

   Tarayıcıda `http://localhost:8501`. Sol menüden şehir seç, bir sütuna tıkla.

Windows'ta `python3` yerine `python`. Sanal ortamı etkinleştirmeden çalıştırmak için: `.venv\Scripts\python app\ornek_veri.py` ve `.venv\Scripts\python -m streamlit run app\harita.py`.

**İnternetsiz zemin (isteğe bağlı):** `data/raw/osm-kasaba/girne_merkez.json` varsa zemin bu dosyadaki Girne merkez binaları (kat sayısıyla 3D) ve yollarıdır; internetten hiçbir şey istenmez. Yoksa Streamlit'in internetten gelen zemin haritası kullanılır. İndirme komutu [KAYNAK.txt](../data/raw/osm-kasaba/KAYNAK.txt)'de.

**Sunum bilgisayarı:** `girne_merkez.json` depoda yok (`data/raw/` git dışı). Sunumdan önce, internet varken indir; yoksa internetsiz açılışta zemin boş kalır.

**Kıyı kontrolü (isteğe bağlı):** `data/raw/osm-kasaba/girne_kiyi.json` varsa sahte trafolar karada tutulur; yoksa uyarı çıkar ve trafoların bir kısmı denize düşebilir. İndirme komutu [KAYNAK.txt](../data/raw/osm-kasaba/KAYNAK.txt)'de.

## "Noktalar çoğalıyor" (sunum geçişi, haritadan ayrı)

Harita sayfasına bağlı değil; tek başına çalışır: `streamlit run app/animasyon.py` (`app/animasyon.py` + `app/animasyon.html`; civan.md KARAR 17:32). Sunum ekranları kurulunca `goster()` oradan çağrılır. ~14 saniye:
1. sehir-001 Girne'de: önce 3 ölçülü trafo tek tek, sonra kalan ölçülüler (dolu nokta, beyaz kenar).
2. Tahmin edilenler ölçülenlere yakından uzağa, küçük gruplar hâlinde (soluk halka); renk `kac_ev.csv`'den.
3. Görünüm adaya açılır; öbür farazi şehirler (002–020) kasabalara **temsili** yerleşir (dağılım 0,4 küçültülmüş). Kasaba merkezleri yaklaşık [Yorum], gerçek trafo yeri değil.

Yalnız farazi şehirler (1–799) girer; 800+ girmez. Ada çizimi `app/ada_kiyi.json`: Natural Earth 1:50m (kamu malı), `world-atlas@2.0.2/countries-50m.json`'dan Cyprus + N. Cyprus (SHA-256 `04342cdc…469502394`, 31 Ekim 2026). İnternet istemez. "Baştan oynat" düğmesi tekrarlar.

## Ne gösterir

| Şehirde ne var | Harita |
|---|---|
| Yalnız `trafolar.csv` (Faz 1 gerçek şehri) | Gri sütunlar, boy kVA ile orantılı; yan panelde trafo bilgisi; **eğri yok** (hangi trafonun ölçülü olduğu `tahmin.csv` gelince belli olur) |
| + `tahmin.csv`, `arketipler.csv` (Faz 2) | Yan panelde öğlen en düşük yük, %80 bant, güven, "ölçülmedi"; eğri |
| + `kac_ev.csv` (Faz 3) | Renkli sütunlar; kaç ev aralığı ve %40 kuralı |

Eğri: ölçülü trafoda `yuk_5dk.csv`'nin gün 0 tüketimi; ölçülmeyende arketip eğrisi × ölçek (sözleşme §5) ve P10–P90 bandı.

Etiket: şehir no ≥ 900 → "SAHTE VERİ — gösterim"; 800–899 → "GERÇEK ÖLÇÜM — <`ayar.json` `veri_kaynagi`> (Kıbrıs değil)"; diğerleri → "örnek veri (farazi şehir) — gösterim".

## Kurallar

- `cevap_anahtari.csv` **okunmaz**. `yuk_5dk.csv`'den yalnız ölçülü trafoların satırları okunur; ölçülmeyenin satırı cevap anahtarı sayılır.
- Sahte şehirdeki her sayı biçim denemesidir: ölçüm ya da sonuç değil.

## Bilinen eksikler

- **İnternetsiz açılış:** OSM dosyası varken tarayıcının istediği tek adres `localhost:8501` (ölçüldü); kapalı internetle ayrıca denenmedi. Dosya yoksa zemin `basemaps.cartocdn.com`'dan gelir ve internet kapalıyken görünmez.
- OSM zemini yalnız Girne merkezi kapsar (~1 km × 1,1 km); dışındaki trafolar boş zeminde durur. Deniz çizilmiyor.
- Windows 11 (Python 3.14, Streamlit 1.66) ve Mac (Python 3.13; karar masası, PR #9 incelemesi) denendi.
- Faz 1 gerçek şehirlerinde bazı trafolar denizde (şehir üreticisi; Volkan'ın kutusunda istek var).
