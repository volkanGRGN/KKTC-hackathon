# Nasıl çalışıyoruz

Kod ne yaptığını söyler; bu dosyalar neden ve nasıl çalıştığımızı söyler. Aynı kuralların ajan dili [CLAUDE.md](CLAUDE.md); ikisi çelişmez, biri değişirse öteki aynı değişiklikte güncellenir.

## Dallar
- **Varsayılan: kendi dosyanda küçük ve çalışır değişiklik → doğrudan `main`.** Çakışmayı aşağıdaki dosya sahipliği önler.
- **Gerektiğinde dal aç** (Volkan, 31 Ekim). Dört durum:
  1. Ortak sözleşme değişikliği (`docs/data/tablo-bicimi.md`): başkasının kodunu etkiler.
  2. `main`'i bozabilecek büyük ya da yarım iş: yeni modülün ilk sürümü, yeniden yazım.
  3. Deneme: belki atılacak iş.
  4. Birden fazla kişinin dosyasına dokunan iş.
- Dal adı alan önekiyle: `alan/kisa-aciklama` (ör. `sehir/ilk-surum`, `sablon/kumeleme`, `harita/yan-panel`).
- Dal kısa ömürlü: aynı gün birleşir ya da silinir.
- `main` her zaman çalışır durumda; bozan kişi hemen düzeltir.

## Paralel çalışma: dosya sahipliği (31 Ekim)
Üçümüz yan yana, aynı anda, doğrudan `main`'e gönderiyoruz. Çakışmamanın tek yolu **herkesin yalnız kendi dosyalarına yazması**:

| Kim | Yazdığı yerler |
|---|---|
| Volkan (+ Claude) | `src/sehir_uret.py`, `src/sablon.py`, `src/kac_ev.py`, `docs/method/`, `docs/decisions/`, `docs/data/tablo-bicimi.md`, `docs/gorev/` (görev kartları), kök belgeler (`README.md`, `DEVIR.md`, `ROADMAP.md`, `CONTRIBUTING.md`, `CLAUDE.md`), `docs/00-overview.md`, `docs/01-plan.md`, `docs/02-faz-0-ogrenim.md`, `docs/glossary.md` |
| Can | `src/profiller.py` (EAC eğrilerini okuma ve tiplere çevirme), `src/sinav.py` (geçme sınavı ölçüleri), `src/grafikler.py`, `data/raw/*/KAYNAK.txt` (osm-* hariç), `docs/data/data-dictionary.md`, `docs/sunum/`, kendi günlükleri |
| Civan | `app/` (harita + `app/ornek_veri.py` sahte veri), `data/raw/osm-*/` (KAYNAK dahil), kendi günlükleri |
| Herkes | yalnız `docs/istek/<kişi>.md` kutuları (istek yazmak için), `NOTLAR.md` (sona ekleme; "Durum" satırı yalnız Volkan) ve kendi günlüğü |

Dosyalar arasındaki sözleşme (hangi dosya hangi biçimde ne üretir) `docs/data/tablo-bicimi.md`'de; önce o yazılır, sonra herkes kendi dosyasına çekilir. **Planlama Volkan'da (+ Claude): görevler [docs/gorev/](docs/gorev/README.md) kartlarıyla verilir; Can ve Civan kartı uygular, soruyu istek kutusuna yazar.** Sınav kodunu (`sinav.py`) modeli yazan değil Can yazar: ölçü bağımsız olsun.

- Başkasının dosyasına ekleme gerekiyorsa o dosyaya dokunma; **o kişinin istek kutusuna** yaz ([docs/istek/](docs/istek/README.md), başlık `UYARI!`), o kişi yapar ve durumu "yapıldı" yapar. Bekleyenler: `grep -n "Durum: bekliyor" docs/istek/*.md`.
- Günlük dosya adı `YYYY-AA-GG-<kişi>-<konu>.md`; böylece günlükler de çakışmaz. (31 Ekim'den önceki iki günlük bu kalıptan önce yazıldı, istisna.)
- Göndermeden önce `git pull --rebase`, sonra `git push`. Küçük ve sık commit.
- Çakışma çıkarsa dokunma, yan yana birlikte çöz.
- Üretilen şehirler (`data/synthetic/`) ve ham veri depoya girmez (`.gitignore`); tohumla yeniden üretilir / KAYNAK.txt'den indirilir.

## Commit
- **Sık commit** (Volkan, 31 Ekim): her anlamlı adımdan sonra küçük bir commit ve hemen `git pull --rebase` + `git push`; işi saatlerce yerelde biriktirme. Küçük ve anlamlı parçalar. Mesaj alan önekiyle: `alan: ne yaptı` (ör. `sehir: panel yaygınlığı eklendi`, `veri: EAC injection indirildi`, `docs: sözlüğe tohum eklendi`). Alanlar: `sehir`, `sablon`, `kacev`, `veri`, `harita`, `sinav`, `docs`.
- Push'tan önce `git pull --rebase`.

## Pull Request (dal açıldığında)
- Şablonu doldur (ne değişti · hangi doküman/ADR güncellendi · kanıt).
- Etkilenen kişiden biri kısa bakar ve onaylar (sözleşme değişikliğinde Can ya da Civan); sonra dalı açan birleştirir.
- **Dokümanı bozan değişiklik aynı PR'da dokümanı düzeltir.**

## Bulamadım akışı
Bir veri bulunamazsa sessizce bırakılmaz; neyin arandığı ve bulunamadığı depoda kanıtıyla durur, aynı arama iki kez yapılmaz:
1. Kendi günlüğüne **arama izi**: nerelere bakıldı (site, klasör, kurum), hangi aramalar yazıldı, tarih, en yakın ne bulundu.
2. Veri sözlüğüne satır: `BULAMADIM — varsayım: …` ya da `aranıyor`.
3. Volkan'ın kutusuna `UYARI! BULAMADIM — <veri>` girdisi, günlüğe bağlantıyla. Volkan'ın oturumu kendi aramasını yapar: bulursa kutuya adresi yazar, bulamazsa "varsayım" kararını ve gerekiyorsa Muhittin'e ya da uzmana soruyu yazar.

## Devir
İş devrederken ya da faz bitince `DEVIR.md` güncellenir (yalnız Volkan): durum, kim nerede, bekleyen istekler, sıradaki üç adım. Eski hali silinir; geçmiş günlükte.

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

## Mac + Windows birlikte
- Dosya açarken hep `open(..., encoding='utf-8')` (yazma ve okuma). Windows'ta varsayılan kodlama farklı; bir kez bu yüzden bozuldu.
- Satır sonları `.gitattributes` ile LF; Windows'ta "LF will be replaced by CRLF" uyarısı normal.
- Yol ayırıcı için `pathlib` ya da `os.path.join`; elle `/` ya da `\\` yazma.
- Komutlarda `python3` (Mac) = `python` (Windows).

## Düzen (5 kural)
1. Her konu için tek kaynak; kopyalama, bağlantı ver.
2. Karar = ADR (tarihli, değişmez, supersede edilir).
3. Bir doküman ≈ bir sayfa; uzadıysa böl.
4. Dosya adı kebab-case, sıralı olanlar numaralı (00-, 01-).
5. README kısa; derinlik docs/'ta. Doküman güncellemeden merge yok.
