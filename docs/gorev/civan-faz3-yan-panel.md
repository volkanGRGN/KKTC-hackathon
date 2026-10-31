# Civan — Faz 3 — yan panel gerçek kaç ev tablosunda

Kartı yazan: Volkan (+ Claude, BUILD), 31 Ekim 2026 akşam. Sözleşme: [docs/data/tablo-bicimi.md](../data/tablo-bicimi.md) §5–6. Renk: [ADR-0010](../decisions/adr-0010-yesil-karari-marj-guven-kumulatif.md).

**Amaç (1 cümle):** Haritadaki trafo rengi ve yan panel, `src/kac_ev.py`'nin gerçek `kac_ev.csv`'sini göstersin. Jüri tıkladığında ne gördüğünü tek bakışta anlasın.

**Girdi:**
- Her şehir klasöründe: `trafolar.csv`, `tahmin.csv`, `kac_ev.csv`.
- Üretmek için:
  - `python3 src/sehir_uret.py 1 20`
  - `python3 src/sablon.py data/synthetic`
  - `python3 src/kac_ev.py data/synthetic`
- PR #8 → #12 → #13 birleşene kadar `kac-ev/ilk-surum` dalından üret.
- Sahte şehirlerin (900–999) zaten ADR-0010 renginde (d097404).

**Çıktı:** `app/harita.py` yan paneli; değişiklik doğrudan main (senin dosyan).

**Yan panelde, sırayla:**
1. **Renk ve tek cümle:**
   - yeşil: "En kötü durumda bile yer var";
   - sarı: "Sınırda ya da emin değiliz, önce ölç";
   - kırmızı: "En kötü durumda yer yok".
2. **Kaç ev:**
   - "`kac_ev_karamsar`–`kac_ev_iyimser` ev" aralığı.
   - Yanında "%40 kuralı: `kural40_ev` ev".
   - İkisi farklıysa vurgula; kilit mesaj bu.
3. **Etiketler:**
   - "ölçülmedi" (`olculdu` = 0) ve güven (`guven`).
   - Panelsiz konut yoksa (`abone_konut` − `panel_sayisi` = 0) "panelsiz konut yok"; sayı gösterme.
4. **Bağlayan sınır:** `sinir_karamsar` (gerilim / ısıl), küçük harfle.
5. **Faz 2 eğrisi:** zaten yaptığın gibi (`arketipler.csv` × ölçek).

**Kural:**
- Renk ve sayılar yalnız `kac_ev.csv`'den.
- Cevap anahtarını okuma.
- Farazi şehirde şerit "örnek veri (farazi şehir) — gösterim".

**Adımlar** (her biri ≤ 1 saat):
1. `kac_ev.csv`'yi (sehir, trafo_no) ile birleştir.
2. Yan panel metni.
3. 3 trafoda elle kontrol: bir yeşil, bir sarı, bir kırmızı. CSV'deki sayılarla aynı mı?

**Nasıl denenir:**
- Haritayı aç; sehir-011 T37 (otel) yeşil ve 2–7 ev olmalı.
- Çoğu konut trafosu kırmızı ya da sarı (kırmızı kuralı karar masasında).
- Yeşil olup "panelsiz konut yok" olan da var (ör. sehir-012 T05 sanayi): renk fiziğe bakar, başvuru ticari aboneden de gelebilir.

**Bitti sayılması için:**
- 20 şehirde renkler `kac_ev.csv` ile aynı (elle 3 trafo).
- "Ölçülmedi" ve "panelsiz konut yok" görünüyor.
- %40 kuralı yan yana.

**Dokunulmayacak dosyalar:** `src/*`, `docs/data/tablo-bicimi.md`.

**Kendin karar ver** (sorma, günlüğüne yaz): metinlerin tam ifadesi, renk tonları, yerleşim.

**Karar masasına yaz:** kırmızı kuralı değişirse (volkan.md, "kırmızı kuralı" UYARI'sı) yalnız `kac_ev.csv` değişir, senin kodun değişmez.

**Takılırsan:** sahte şehirle dene; sonra civan.md / volkan.md.
