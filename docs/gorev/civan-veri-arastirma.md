# Civan — Sunum sonrası döngü — Yeni veri araştırması ve veri partisi teslimi

Kartı yazan: karar masası (Volkan adına), 31 Ekim 2026 21:35. Tüzük: [docs/tuzuk.md](../tuzuk.md). Öncelik: **önce Faz 4 işleri** (ağ kapalı açılış, ekran kaydı) ve sunum; bu kart arkada yürür.

**Amaç (1 cümle):** Modelin eksik verileri için gerçek veri bulmak ve her bulguyu, Volkan ile Can'ın modeli iyileştirmek için kullanabileceği **veri partisi** olarak teslim etmek.

**Girdi:** veri sözlüğündeki BULAMADIM satırları; ROADMAP "Sunum sonrası" → "Dış veri istekleri"; [ada veri setleri günlüğün](../log/2026-10-31-civan-ada-veri-setleri.md); Faz 3 "Açık eksikler" tablosu (hangi bilgi neyi düzeltir).

**Öncelik sırası (en çok düzelten önde, tüzük madde 7):**
1. **Kıbrıs'ta gerçek gerilim:** panelli evlerin inverter kaydı (izinle; Volkan tanıdıklara soruyor) ve akıllı priz gece seviyesi. Senin işin: dosya biçimini (marka marka dışa aktarma) ve okuma betiği iskeletini hazırlamak, kişisel bilgi depoya girmeden.
2. **Hat / kablo / faz kayıtları:** KIOS (Kotsonias 2019) hat modeli, Kıb-Tek kesit bilgisi (uzmana soru 3, 4).
3. **Yaz tepesi ve sıcaklık** (Faz 11, ADR-0014): Lefkoşa saatlik sıcaklık (Open-Meteo, yaz ayları), herhangi bir Akdeniz trafo tepe verisi; Malta / Gozo hat tablosu (Micallef tezi).
4. Diğer: bulut geçişi (NREL Oahu), ev düzeyi klima (Plegma) — indirilmez, aday olarak yazılır.

**Çıktı (her bulgu için):** `docs/istek/volkan.md`'ye `## UYARI! … — Civan'dan — veri partisi: <ad>` girdisi, tüzükteki parti kartı alanlarıyla: kaynak + adres + lisans; çekim tarihi; kapsam (trafo / ev sayısı, gözlem penceresi, eksik ne); şema, birim, saat dilimi, boş değer; **bilinen yanlılık**; hangi eksiği düzeltmesi beklenir (hipotez); indirildi mi, boyut, SHA-256; `data/raw/<ad>/KAYNAK.txt` (lisans uygunsa). Ham veri depoya girmez (lisans yazılı değilse hiç). Kullanım bölünmesini (ayar / doğrulama) karar masası yazar, sen değer görmeden listeyi verirsin.

**Nasıl denenir:** UYARI girdisi tüzükteki alanların hepsini içeriyor mu; KAYNAK.txt'deki adres ve sağlama tekrar indirince tutuyor mu.

**Bitti sayılması için:** her parti için (1) UYARI girdisi tam alanlarla; (2) KAYNAK.txt (uygunsa); (3) veri sözlüğüne satır (Can'ın dosyası → Can'a bir satır yaz).

**Dokunulmayacak dosyalar:** `src/` (model, sınav), `docs/data/tablo-bicimi.md`; kişisel veri (ad, adres) hiçbir dosyaya.

**Kendin karar ver (günlüğe yaz):** arama sırası, hangi kaynağın "aday" hangisinin "elimizde" olduğu, betik iskeleti.

**Karar masasına yaz (volkan.md, bekleme):** lisans belirsiz ama veri değerli; kişisel veri içeren kaynak; bir kaynağın hangi eksiği düzelttiği belirsiz.

**Takılırsan:** önce veri sözlüğü "Adaylar" ve ada günlüğü; sonra kutu.
