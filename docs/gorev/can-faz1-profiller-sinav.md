# Can — Faz 1 — profiller.py'yi birleştir, sonra Faz 1 sınavı

Kartı yazan: Volkan (+ Claude), 31 Ekim 2026. Sözleşme: [docs/data/tablo-bicimi.md](../data/tablo-bicimi.md) ([PR #4](https://github.com/volkanGRGN/KKTC-hackathon/pull/4); birleşene kadar `sozlesme/tablo-bicimi` dalında).

**Amaç (1 cümle):** Şehir üreticisinin çağıracağı EAC sınıf eğrilerini main'e almak, sonra üretilen şehirlerin Faz 1 geçme sınavını ölçen kodu yazmak (üreteci yazan sınavı yazmaz).

**Girdi:**
- Senin `veri/profiller-ilk-surum` dalındaki `src/profiller.py` (ea1c1dc). İyi durumda; aşağıdaki küçük işlerle birleşir.
- `data/raw/eac-profil-siniflari/Offtake_Profile_Classes.xlsx` (indirdin).
- Şehirler: `data/synthetic/sehir-NNN/` (şehir üreticisi `sehir/ilk-surum` dalında geliyor; komut `python3 src/sehir_uret.py 1 20`).

**Çıktı:**
1. `src/profiller.py` main'de. Şehir üreticisi bunları çağırıyor; **adları ve imzaları değiştirme** (gerekirse önce Volkan'ın kutusu):
   - `oku(yol=XLSX)` → `{sınıf: {'Apr_WD': [48 değer], ...}}`
   - `sinif_egrisi(veri, sinif, ay, gun)` → 288 değer, pu; `gun` = `'is'` ya da `'tatil'`
   - sınıf adları: `konut`, `kucuk_ticari`, `buyuk_ticari`, `otel`, `kucuk_sanayi`, `buyuk_sanayi`, `su_pompasi`
   - pu → kW çevirisi ve tiplerin abone karışımı şehir üreticisinde (Kıb-Tek yıllık tüketimi ile); profiller'de değil.
2. `src/sinav.py` içinde Faz 1 bölümü: `python3 src/sinav.py faz1 data/synthetic` her madde için GEÇTİ/KALDI ve rakamı yazar.

**Adımlar:**
1. (≤ 30 dk) `profiller.py` küçük işler:
   - `TIPLER`'in üstüne not: "Yalnız sağlama için. Şehir üreticisi trafo başına abone sayısını kendi kurar ve sınıf eğrilerini toplar (ROADMAP Faz 1)." Oranlara dokunma.
   - Sağlamaya bir madde: her sınıf × 24 tipik gün için 288 değerin ortalaması ÷ 48 değerin ortalaması, aralık 0,99–1,01 (5 dk açma günlük enerjiyi koruyor mu).
   - `python3 src/profiller.py` Mac ve Windows'ta; çıktıyı günlüğe.
2. (≤ 15 dk) Dalı main'e göre güncelle, PR aç (yeni modülün ilk sürümü: CONTRIBUTING "Dallar" 2). Volkan bakar, sen birleştirirsin.
3. (≤ 30 dk) Kutundaki iki istek ([docs/istek/can.md](../istek/can.md): BULAMADIM işaretleri, OSM satırı). Aynı değişiklikte veri sözlüğünün "Üreteceğimiz" bölümünü sözleşmeye bağla (faz dağılımı artık cevap anahtarında; ayrıntıyı kopyalama, bağlantı ver).
4. (≤ 1 saat) `src/sinav.py` Faz 1 bölümü. Her şehir klasöründen `trafolar.csv`, `cevap_anahtari.csv`, `ayar.json` okur (biçim: sözleşme). Ölçer (ROADMAP Faz 1 geçme sınavı):
   - Her şehirde 7 tipin her biri ≥ 3 trafo; bütün şehirlerde her tipten ≥ 60 trafo (20 şehir).
   - En az bir trafoda `v_max_bugun_v` > 259; hiçbir trafoda `v_min_bugun_v` < 216.
   - Süre: `ayar.json` → `sure_sn` ≤ 60.
   - `profil_kaynagi` = `yer_tutucu` olan şehri sayma, uyarı yaz.
   - Bilgi olarak (eşiksiz): tip başına `ogle_min_kw` ortancası; `kac_ev_gercek` dağılımı; `kac_ev_sinir` sayımı (gerilim / ısıl / yok); `kac_ev_tavan` oranı.
5. (≤ 15 dk) Aynı tohum aynı şehir: `python3 src/sehir_uret.py 7` iki kez, klasörü ikisinin arasında kopyalayıp dosyaları karşılaştır (Windows'ta `fc`, Mac'te `diff -r`). Windows'ta bir şehir üret + sınav çalıştır; Türkçe karakter bozulmuyor mu bak → geçme sınavındaki "Windows'ta çalıştı" onayı.

**Nasıl denenir:**
- `python3 src/profiller.py` → 5 sağlama satırı GEÇTİ. Kalan varsa rakamıyla günlüğe; eşiğe uydurmak için değer ayarlama.
- `python3 src/sehir_uret.py 1 20`, sonra `python3 src/sinav.py faz1 data/synthetic` → madde madde GEÇTİ/KALDI.

**Bitti sayılması için:**
- [ ] `profiller.py` main'de; beş sağlama rakamı `docs/log/2026-10-31-can-faz1.md`'de.
- [ ] `sinav.py faz1` 20 şehirde çalışıyor; her madde rakamıyla günlükte.
- [ ] Windows'ta üretim + sınav çalıştı; tohum sınavı (iki çalıştırma birebir) günlükte.
- [ ] Kutundaki iki istek "yapıldı".

**Dokunulmayacak dosyalar:** `src/sehir_uret.py`, `src/trafo_bos_kapasite.py`, `docs/data/tablo-bicimi.md`, `app/`. Biçimde eksik ya da yanlış görürsen Volkan'ın kutusuna.

**Kendin karar ver (sorma, günlüğe yaz):** `profiller.py` ve `sinav.py` içindeki uygulama ayrıntısı (önbellek, okuma, çıktı metni, adlandırma); sağlaması eşiği geçmeyen maddeyi rakamıyla günlüğe yazmak; dal adı.

**Karar masasına yaz (`volkan.md`, bekleme, sıradaki işe geç):** `profiller.py` imzası ya da sınıf adı değişmeli mi; sözleşmede eksik ya da çelişkili sütun; bir sağlama eşiğinde kalırsa eşik mi değişmeli (değeri ayarlama); Faz 1 sınav maddesinin anlamı belirsizse.

**Takılırsan:** önce şehir üreticisini `sehir/ilk-surum` dalından al ve bir şehir üret; sonra istek kutusu (sormadan) / bloklarsa sesli.
