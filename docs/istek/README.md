# İstek kutuları

Başkasının dosyasında bir değişiklik gerekiyorsa o dosyaya dokunma; **o kişinin kutusuna** yaz. Kutular: [volkan.md](volkan.md), [can.md](can.md), [civan.md](civan.md); dışarıya sorular [muhittin.md](muhittin.md). Her kutuyu yalnız sahibi işler; sahibi işi yapınca durumu "yapıldı" yapar.

Her istek şu kalıpla, dosyanın SONUNA:

```
## UYARI! 31 Eki 13:40 — Can'dan
Ne: tablo biçimine "hat_sayisi" sütunu ekle
Dosya: docs/data/tablo-bicimi.md
Neden: profiller.py hat başına eğri üretiyor
Durum: bekliyor
```

**Sormadan yaz, bekleme, devam et** (Volkan, 31 Ekim). Kutuya yazmak için kimseden izin istenmez; ajanlar da "kutuya yazayım mı?" diye sormaz. Yaz, gönder, kartındaki sıradaki işe geç. Yalnız işin gerçekten duruyorsa başlığa `BLOKLUYOR` ekle ve sesli söyle.

## Kim neye karar verir

| Kim | Neye |
|---|---|
| **Kişi kendisi** (sormadan, günlüğe yazarak) | Kendi dosyasındaki uygulama ayrıntısı, adlandırma, küçük hata düzeltme; eleme ölçütüyle net çıkan veri kararı (3+ "evet" → al, azı → ele); bulunamayan veri için "varsayım" etiketi (Bulamadım akışıyla); kartın "kendin karar ver" listesindekiler. |
| **Karar masası** (Volkan'ın Fable oturumu; `volkan.md` kutusunu işler) | Sözleşmeye sütun ekleme/değiştirme, ADR'ye uyan iki seçenekli yöntem kararı, eşik ve parametre seçimi, BULAMADIM için ikinci arama, kart maddesi belirsizliği, iki kişi arasında çakışma. Kararı isteyenin kutusuna yazar. |
| **Yalnız Volkan** | Kapsam/MVP değişikliği, ADR'ye ters iş, hesap ya da kayıt gerektiren iş, dışarıya mesaj (Muhittin, organizatör), sunum hikâyesi. Karar masası bunları Volkan'a tek satırlık soru olarak iletir. |

Cevap kalıbı (karar masası, isteyenin kutusuna):

```
## KARAR 31 Eki 14:10 — volkan.md'deki "<başlık>" isteğine
Karar: …
Neden: … (ADR/ROADMAP bağlantısı)
Senden beklenen: …
Durum: bekliyor
```
Karar verilince `volkan.md`'deki asıl isteğin durumu `Durum: karar verildi 14:10 → can.md` olur.

Kurallar:
- Yazmadan önce `git pull --rebase`; yazınca hemen gönder, bekletme.
- Sahibi işi yapınca aynı girdide `Durum: yapıldı 14:05` yazar; isteği silmez.
- "UYARI!" kelimesi başlıkta kalır; arama ile bekleyenler bulunur: `grep -n "Durum: bekliyor" docs/istek/*.md`.
- Acil ve bloklayan bir istekse ayrıca sesli söyle; ama kayıt yine kutuda.
