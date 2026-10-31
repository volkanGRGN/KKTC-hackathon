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

Kurallar:
- Yazmadan önce `git pull --rebase`; yazınca hemen gönder, bekletme.
- Sahibi işi yapınca aynı girdide `Durum: yapıldı 14:05` yazar; isteği silmez.
- "UYARI!" kelimesi başlıkta kalır; arama ile bekleyenler bulunur: `grep -n "Durum: bekliyor" docs/istek/*.md`.
- Acil ve bloklayan bir istekse ayrıca sesli söyle; ama kayıt yine kutuda.
