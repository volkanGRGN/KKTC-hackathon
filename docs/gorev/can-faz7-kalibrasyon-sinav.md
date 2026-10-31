# Can — Faz 7 — Kalibrasyon sınavı, grafik ve hold-out defteri

Tüzük: geçerli ([docs/tuzuk.md](../tuzuk.md)). Karar: karar masası 21:32 (can.md). BUILD ile paralel. **Öneren ≠ puanlayan:** k katsayısını ve model-sapma terimini BUILD üretir (`kalibrasyon.py`, `sablon.py`, `kac_ev_olasilik.py`, dal `kalibrasyon/faz7`); sen ölçersin.

Amaç (1 cümle): Bantların gerçeğe karşı kalibre olup olmadığını sınavın kalıcı maddesi yapmak ve önce / sonra göstermek.

Girdi: `data/synthetic/sehir-*/tahmin.csv`, `kac_ev.csv`, cevap anahtarı; İspanya için `src/edp_test.py` ya da `src/edp_kiyas.py` çıktısı (bir-dışarıda tahmin, P10, P90, gerçek).

Çıktı:
- `src/sinav.py faz2`'ye kalibrasyon maddeleri (C1).
- `src/grafikler.py`'ye kapsama eğrisi; `docs/sunum/kalibrasyon.png` (C2).
- `docs/log/holdout-defteri.md` (C3).
- Günlük `docs/log/…-can-faz7.md`.

Adımlar:
1. **C1 (60 dk)** `sinav.py faz2`'ye:
   - (a) nominal–ampirik kapsama: %50 / 80 / 90 / 95 nominal bant için ampirik kapsama. Madde: %80 bant %70–90 (var) **ve %95 bant ≥ %90**.
   - (b) PIT düzlüğü: gerçeğin tahmin dağılımındaki yüzdelik konumu (P10 / orta / P90'dan parçalı doğrusal yaklaşım); 10 kovada en büyük sapma ≤ 0,05 → GEÇTİ, yoksa UYARI, yönüyle ("fazla emin" / "fazla geniş").
   - (c) aynı ölçüler İspanya'da: gerçek veri = resmi kalibrasyon ölçüsü; farazi = bilgi.
   - %50 / 90 / 95 bantlar P10 / P90'dan normal varsayımıyla türetilir [Yorum]; tanımı günlüğe yaz.
2. **C2 (30 dk)** `grafikler.py`: kapsama eğrisi (nominal ↔ ampirik, köşegenle), önce / sonra, İspanya ve farazi. Ekran 4 için tek cümle hazırla ama **PR birleşene kadar slayta koyma**: "Aralıklarımız İspanya'nın 29 gerçek trafosuna karşı kalibre edildi: %80 bant önce %x, sonra %y."
3. **C3 (20 dk)** `docs/log/holdout-defteri.md` (append-only): gerçek veriye her bakış bir satır (tarih, veri, amaç, kim, hangi metrik). İlk satırlar bugüne kadarki bakışlar: PR #10 (İspanya), PR #11 (İngiltere), olasılıklı geri-test, Faz 7.
4. **C4** BUILD'in PR'ı gelince: C1 maddelerini dalda koş, onayla. Birleşince resmi `faz2` ve `faz3` bir kez, günlüğe; sonra slayt 5 / ekran 4 rakamları.

Nasıl denenir:
```
python3 src/sinav.py faz2 data/synthetic --aralik 11-20     # önce main'de (önce rakamları), sonra dalda (sonra)
python3 src/grafikler.py
```
İkisi günlükte yan yana.

Bitti sayılması için:
- `faz2` çıktısında kapsama eğrisi ve PIT maddeleri var; İspanya satırı ayrı.
- Grafik önce / sonra, İspanya ve farazi.
- Hold-out defteri açık, geçmiş bakışlar yazılı.
- PR'da C1 koşuldu, onay ya da itiraz kutuda.

Dokunulmayacak dosyalar: `src/sablon.py`, `src/kac_ev_olasilik.py`, `src/kalibrasyon.py` (BUILD); `app/` (Civan). `docs/method/validation.md` BUILD'in: tanım satırını can.md'den değil volkan.md'den iste.

Kendin karar ver (sorma, günlüğe yaz): PIT kova sayısı, grafik biçimi, İspanya çıktısını hangi betikten aldığın.

Karar masasına yaz (volkan.md, bekleme): dalda yanlış yeşil 0'dan çıkarsa; İspanya'da %80 bant sonrası %70–90 dışındaysa.

Takılırsan: önce main'de koş, rakamlar v1 günlükleriyle tutuyor mu bak; sonra kutu.

Sunum metni v1 rakamlarıyla kalır, PR birleşip resmi koşum yapılana kadar değiştirme.
