# Görev kartları

Planlamayı Volkan (+ Claude) yapar; Can ve Civan kartları uygular. Sebep: planlama ve sözleşme (tablo biçimleri, fonksiyon imzaları) en çok düşünme isteyen iş, o yüzden en güçlü model ve en geniş bütçe orada; uygulama kartla net olunca daha az yardım ister.

Her kart bir dosya: `docs/gorev/<kişi>-<faz>-<konu>.md`. Yalnız Volkan yazar; Can ve Civan okur, soruyu [istek kutusuna](../istek/README.md) ya da sesli sorar, bitince kartın sonuna "Bitti <saat>, kanıt: …" yazar (kartın sahibi sonra düzeltir).

Kart kalıbı:

```
# <Kişi> — Faz N — <konu>
Amaç (1 cümle):
Girdi: hangi dosya/veri, nereden
Çıktı: dosya adı, fonksiyon imzası ya da tablo sütunları (sözleşme: docs/data/tablo-bicimi.md)
Adımlar: 1., 2., 3. (her biri ≤ 1 saat)
Nasıl denenir: komut + beklenen çıktı
Bitti sayılması için: ölçülebilir 2–4 madde (ROADMAP geçme sınavından)
Dokunulmayacak dosyalar: …
Takılırsan: önce şunu dene …; sonra istek kutusu / sesli
```

Sıra: önce `docs/data/tablo-bicimi.md` (sözleşme), sonra Faz 1 kartları (Can: profiller; Civan: ornek_veri + harita iskeleti), sonra bizim kod.
