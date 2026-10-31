# Volkan (+ Claude, BUILD) — Faz 7 — Kalibrasyon gerçeğe karşı: model tarafı

Tüzük: geçerli ([docs/tuzuk.md](../tuzuk.md)). Karar: karar masası 21:32 (volkan.md). Dal `kalibrasyon/faz7`, PR; Can onaylar, Volkan sohbette "birleştir" der.

Amaç (1 cümle): Yük bandını İspanya'nın, gerilim yükselmesini İngiltere'nin gerçek artıklarına göre genişletip "fazla emin" hesabı düzeltmek; hiçbir katsayıyı farazi şehre bakarak seçmemek.

Girdi:
- İspanya: `src/edp_test.py` faturalı (c) koşusunun bir-dışarıda artıkları (EDP Oviedo 2018, 29 trafo; `data/raw/edp-oviedo/KAYNAK.txt`).
- İngiltere: `src/ukpn_olasilik.py`'nin 6 hattaki ölçülen ↔ hesaplanan yükselmesi (UKPN 2014; `data/raw/ukpn-pv-dogrulama/KAYNAK.txt`).

Veri partileri (tüzük §2):
- **P1-edp-2018**: 29 trafo, Kasım 2018; bilinen yanlılık: Oviedo kenti, Kıbrıs değil, klima yok. Kullanım: katsayı k_yük **29 trafonun tamamından** (karar masası 21:32). Bu veri PR #10'dan beri birçok kez görüldü; dokunulmamış doğrulama payı yok. Bu yüzden kapsama iki türlü yazılır: iç örnek ("ayarlandığı veride ölçüldü") ve **k'si o trafo dışarıda bulunmuş bir-dışarıda kapsama** (dürüst tahmin).
- **P2-ukpn-2014**: 6 hat, yaz 2014, 1 dakika; bilinen yanlılık: İngiltere, faz kaydı var, 6 hat az. Kullanım: model-sapma çarpanı s **6 hattın tamamından**; aynı şekilde bir-dışarıda kapsama ayrıca. Etiket: "6 hatla ayarlandı, pilotta yeniden".
- Tüzük madde 1 ile gerilim: iki kaynağın da dokunulmamış payı kalmıyor. Bu yüzden Faz 7'nin sonucu "kalibre edildi", **"iyileşti" değil** (madde 2). Pilot doğrulama payı dokunulmaz kalır.

Çıktı:
- `src/kalibrasyon.py`: `pit(tahmin, p10, p90, gercek)`, `kapsama_egrisi(satirlar, nominaller=(0.5, 0.8, 0.9, 0.95))`, `sisirme_k(satirlar, hedef=0.8)`, `model_sapma(oranlar)`; saf Python.
- `src/sablon.py`: bant k_yük ile genişler; sözleşme değişmez; `sablon_ozet.json`'a `kalibrasyon` kaydı.
- `src/kac_ev_olasilik.py`: gerilim yükselmesine çekiliş başına model-sapma çarpanı s.
- Günlük `docs/log/2026-11-01-volkan-faz7-kalibrasyon.md`; ROADMAP Faz 7; DEVIR.

Adımlar:
1. B1 `kalibrasyon.py` ve birim denemesi (bilinen dağılımla k ≈ 1).
2. B2 k_yük İspanya'dan; `sablon.py`; İspanya kapsama önce / sonra (iç örnek + bir-dışarıda); farazi 1–10'da etki; sınav 11–20 bir kez.
3. B3 s İngiltere'den; `kac_ev_olasilik.py`; 6 hatta P98 kapsaması (iç örnek + bir-dışarıda); sınav 11–20 bir kez: yeşil, yanlış yeşil, sarı, kaç ev bandı.
4. B4 günlük, ROADMAP, DEVIR, PR.

Nasıl denenir:
```
python3 src/kalibrasyon.py --deneme            # bilinen dağılımla k ≈ 1
python3 src/sablon.py data/synthetic           # sablon_ozet.json'da kalibrasyon kaydı
python3 src/kac_ev_olasilik.py data/synthetic
python3 src/sinav.py faz2 data/synthetic --aralik 11-20
python3 src/sinav.py faz3 data/synthetic --aralik 11-20
```

Bitti sayılması için:
- İspanya'da %80 bandın bir-dışarıda kapsaması %70–90 içinde (önce / sonra yazılı).
- İngiltere'de P98 sınırı 6 hattın kaçını kapsıyor, önce / sonra; s'nin aralığı günlükte.
- Sınav 11–20 bir kez: yanlış yeşil 0 kalıyor (kapı), yeşil / sarı / kaç ev bandı değişimi yazılı.
- k ve s farazi şehre bakılarak seçilmedi (günlükte hangi veriden geldiği).

Dokunulmayacak dosyalar: `src/sinav.py`, `src/grafikler.py`, `src/profiller.py` (Can); `app/` (Civan); sözleşme `docs/data/tablo-bicimi.md` değişmez.

Kendin karar ver (sorma, günlüğe yaz): k'nin tanımındaki yüzdelik (%80 hedef), s'nin dağılım biçimi (log-normal), çekiliş sayısı.

Karar masasına yaz (volkan.md, bekleme): yanlış yeşil 0'dan çıkarsa; k ya da s beklenmedik büyükse (> 2); sunum rakamını değiştirecek bir şey.

Takılırsan: önce `edp_test.py` / `ukpn_olasilik.py` çıktısını tek başına koş; sonra kutu.
