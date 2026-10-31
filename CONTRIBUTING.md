# Nasıl çalışıyoruz

Kod ne yaptığını söyler; bu dosyalar neden ve nasıl çalıştığımızı söyler. Aynı kuralların ajan dili [CLAUDE.md](CLAUDE.md); ikisi çelişmez, biri değişirse öteki aynı değişiklikte güncellenir.

## Dallar
- `main` her zaman çalışır durumda.
- İş dalı: `tur/kisa-aciklama` (ör. `feat/profil-kumeleme`, `fix/veri-okuma`).

## Commit
- Küçük ve anlamlı parçalar. Mesaj: `tür: ne yaptı` (ör. `feat: arketip kümeleme eklendi`).
- Push'tan önce `git pull --rebase`.

## Pull Request
- Şablonu doldur (ne değişti · hangi doküman/ADR güncellendi · kanıt).
- En az 1 gözden geçiren onayı. Hackathonda gözden geçirme 15 dakikayı geçmesin.
- **Dokümanı bozan değişiklik aynı PR'da dokümanı düzeltir.**

## Definition of Done
- [ ] Kod çalışıyor ve test edildi; nasıl çalıştırıldığı README'de
- [ ] İlgili doküman/ADR güncel
- [ ] Karar verildiyse ADR yazıldı
- [ ] Deneyse [docs/log/](docs/log/) altına gerçek sonuç rakamıyla günlük yazıldı

## Kararlar
Önemli her karar `docs/decisions/` altına ADR olur. **Sözlü/konuşmadaki karar yok sayılır** — "ADR-X'e yazdım" ile kapanır. ADR düzenlenmez; karar değişince yeni ADR yazılır, eskisinin durumu "superseded by ADR-XXXX" olur. Şablon: [adr-0000-sablon.md](docs/decisions/adr-0000-sablon.md).

## Bu projeye özel: veri ve rakamlar
- Her rakamın yanında etiketi olur: **[Kaynaklı]** yayın/rapor (adresiyle), **[Hesap]** bizim hesabımız, **[Yorum]** değerlendirme. Bulunamayan şey "BULAMADIM" diye yazılır, uydurulmaz.
- Ham veri `data/raw/<kebab-ad>/` altına, yanında KAYNAK.txt (adres, indirme tarihi, lisans).
- Farazi şehirden çıkan sonuç "gösterim" diye etiketlenir; kanıt değildir ([doğrulama protokolü](docs/method/validation.md)).

## Düzen (5 kural)
1. Her konu için tek kaynak; kopyalama, bağlantı ver.
2. Karar = ADR (tarihli, değişmez, supersede edilir).
3. Bir doküman ≈ bir sayfa; uzadıysa böl.
4. Dosya adı kebab-case, sıralı olanlar numaralı (00-, 01-).
5. README kısa; derinlik docs/'ta. Doküman güncellemeden merge yok.
