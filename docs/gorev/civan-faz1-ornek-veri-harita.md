# Civan — Faz 1 — sahte şehir ve harita iskeleti

Kartı yazan: Volkan (+ Claude), 31 Ekim 2026. Sözleşme: [docs/data/tablo-bicimi.md](../data/tablo-bicimi.md) ([PR #4](https://github.com/volkanGRGN/KKTC-hackathon/pull/4); birleşene kadar `sozlesme/tablo-bicimi` dalında).

**Amaç (1 cümle):** Sözleşmeye birebir uyan sahte şehirlerle haritanın iskeletini kurmak; gerçek şehirler gelince yalnız klasör değişsin, kod değişmesin.

**Girdi:**
- Sözleşme bölüm 1 (`trafolar.csv`), 2 (`yuk_5dk.csv`), 5 (`tahmin.csv`, `arketipler.csv`), 6 (`kac_ev.csv`).
- `data/raw/osm-kasaba/girne_merkez.json` (indirdin; bu kartta isteğe bağlı).

**Çıktı:**
- `app/ornek_veri.py`: `python3 app/ornek_veri.py` → `data/synthetic/sehir-901/`, `-902/`, `-903/` içine `trafolar.csv`, `yuk_5dk.csv`, `tahmin.csv`, `arketipler.csv`, `kac_ev.csv`, `ayar.json`. **`cevap_anahtari.csv` yazma** (harita okumaz).
- `app/harita.py`: Streamlit + pydeck iskeleti.
- `app/README.md`: kurulum ve komut.

Sahte veri kuralları:
- Sütun adları ve sırası sözleşmeyle birebir. Değerler makul: 40 trafo; `kva` direk 25/50/100/250/400, yer 630/1000; `bolge` dört değerden; `renk`'te üçü de çıksın; 10–15 trafoda `olculdu` = 1.
- Konum: referans noktası Girne merkez, senin OSM alanının ortası (enlem 35.3375, boylam 33.318). Trafolar ±1,5 km içinde; denize düşmesin diye kuzeye en çok 400 m [Yorum]. Şehir üreticisi de aynı referansı kullanacak.
- `yuk_5dk.csv`: 2 gün yeter (`gun` 0 `isgunu`, 1 `tatil`), yalnız `olculdu` = 1 trafolar. Harita gün sayısını varsaymasın (gerçek şehirde 14 gün).
- `ayar.json`: `sehir`, `tohum`, `sozlesme_surumu` (1), `sahte` (true), `referans_enlem`, `referans_boylam`.
- Rastgelelik tohumlu (`random.Random(tohum)`): aynı komut aynı dosyaları verir. `open(..., 'w', encoding='utf-8', newline='')`; yollar `pathlib`.

Harita kuralları:
1. Kenar çubuğu: `data/synthetic/` altında `trafolar.csv` olan klasörler → şehir seçimi. `sehir` ≥ 900 ise her ekranın üstünde "SAHTE VERİ — gösterim"; değilse "örnek veri (farazi şehir) — gösterim".
2. `trafolar.csv` + `tahmin.csv` + `kac_ev.csv`'yi (sehir, trafo_no) ile birleştir. `tahmin.csv` ya da `kac_ev.csv` yoksa çökme: yalnız `trafolar.csv` ile gri sütunlar (Faz 1 bitince gerçek şehirde önce yalnız o olacak).
3. pydeck `ColumnLayer`: konum [`boylam`, `enlem`]; yükseklik `kac_ev_karamsar` (yoksa `kva` ÷ 10); renk `renk`'ten (yoksa gri). Katmanda `id="trafolar"`, `pickable=True`; `st.pydeck_chart(deck, on_select="rerun", selection_mode="single-object")` (Streamlit ≥ 1.39; [araştırma](../log/2026-10-31-kapsamli-arastirma.md) bölüm 3).
4. Altlık harita yok (`map_style=None`): internetsiz açılsın.
5. Tıklanınca yan panel: `trafo_no`, `kva`, `bolge`, abone toplamı, `panel_kw`; varsa öğlen en düşük yük + P10–P90 + `guven` + "ölçülmedi" (`olculdu` = 0); varsa kaç ev karamsar–iyimser, `renk`, %40 kuralının dediği (`kural40_ev`).
6. Eğri: ölçülü trafoda `yuk_5dk.csv`'den `tuketim_kw` (gün 0); ölçülmeyende `arketipler.csv`'den tahmini eğri (sözleşme bölüm 5'teki formül). **Ölçülmeyen trafonun `yuk_5dk.csv` satırını okuma**: gerçek şehirde o, cevap anahtarı sayılır.

**Adımlar** (her biri ≤ 1 saat; yeni modülün ilk sürümü olduğu için kendi dalında, ör. `harita/iskelet`, bitince PR, Volkan bakar):
1. `ornek_veri.py`: `trafolar.csv`, `tahmin.csv`, `kac_ev.csv`.
2. `ornek_veri.py`: `arketipler.csv`, `yuk_5dk.csv`, `ayar.json`; üç şehir.
3. `harita.py`: şehir seçimi, birleştirme, sütunlar, renk, etiket şeridi.
4. `harita.py`: tıklama, yan panel, eğri.
5. `app/README.md`, Windows denemesi, günlük `docs/log/2026-10-31-civan-faz1.md`.
6. (Zaman kalırsa) OSM binaları `PolygonLayer` olarak altlık (`girne_merkez.json`; atıf "© OpenStreetMap katkıcıları").

**Nasıl denenir:**
- `python3 app/ornek_veri.py` → üç satır: "sehir-901: 40 trafo" …
- `python3 -c "import csv; print(next(csv.reader(open('data/synthetic/sehir-901/trafolar.csv', encoding='utf-8'))))"` → sözleşme bölüm 1'deki sütunlar, aynı sırada (öbür dosyalar için de).
- `streamlit run app/harita.py` → harita; şehir seç; bir sütuna tıkla → yan panel.

**Bitti sayılması için:**
- [ ] `ornek_veri.py`'nin beş CSV'sinin başlığı sözleşmeyle birebir.
- [ ] Tıklamayla yan panel ≤ 1 saniyede açılıyor; 40 trafoda takılma yok.
- [ ] İnternet kapalıyken açılıyor.
- [ ] Mac ve Windows'ta çalıştı; "SAHTE VERİ" şeridi her ekranda; üç şehir seçilebiliyor.

**Dokunulmayacak dosyalar:** `src/`, `docs/data/tablo-bicimi.md`, `data/raw/` (osm-* hariç), `.gitignore`. Biçimde eksik görürsen Volkan'ın kutusuna.

**Kendin karar ver (sorma, günlüğe yaz):** sahte değerlerin dağılımı; renk tonları, sütun boyu çarpanı, yan panel düzeni; dal adı; 6. adımı (OSM altlığı) yapıp yapmamak.

**Karar masasına yaz (`volkan.md`, bekleme, sıradaki işe geç):** haritanın ihtiyacı olup sözleşmede olmayan sütun; referans noktasını değiştirmek; tıklama çalışmazsa seçme kutusu yedeğinin kalıcı olup olmayacağı.

**Takılırsan:** tıklama gelmiyorsa `streamlit --version` (≥ 1.39), katmanda `id` ve `pickable`; olmazsa kenar çubuğuna trafo seçme kutusu (`st.selectbox`) koyup devam et; sonra istek kutusu (sormadan) / bloklarsa sesli.

**Faz 2'de aynı kart (31 Ekim):** yeni kart yok. Yan panel `tahmin.csv` ve `arketipler.csv`'yi sahte veriyle göstersin: arketip eğrisi × ölçek ([sözleşme §5](../data/tablo-bicimi.md) son paragraf), %80 bant (`ogle_min_kw_p10`–`p90`), `guven` etiketi, `olculdu` = 0 ise "ölçülmedi". Gerçek `tahmin.csv` `src/sablon.py` main'e gelince `data/synthetic/sehir-001…020/` klasörlerinde oluşur; sütunlar sözleşmeyle aynı, harita kodunda değişiklik gerekmez.
