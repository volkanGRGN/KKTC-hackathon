# Trafo Şablonu (çalışma adı)

Kıb-Tek mahalle trafolarının gerçek yükünü ve hat ucundaki gerilimi görmüyor; bu yüzden ~2.670 çatı güneşi başvurusu bekliyor. Bu araç trafoların küçük bir kısmını ölçüp gerisini "şablonla" tahmin eder ve her trafo için **öğlen ne kadar dolu, kaç ev daha panel takabilir, ne kadar eminiz** sorusunu haritada cevaplar. Kullanıcısı Kıb-Tek'in planlama birimi; araç başvuru reddetmez, **ayırır**: bariz uygun → hızlı onay, bariz dolu → işaret, emin değil → ölçüm cihazı tak.

VCC-2 · Sürdürülebilir Kıbrıs Hackathonu · 31 Ekim – 1 Kasım 2026

## Kurulum

Python 3.10 ya da üstü. Windows'ta `python3` yerine `python` yazın.

```bash
git clone https://github.com/volkanGRGN/KKTC-hackathon.git
cd KKTC-hackathon
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Ham veri depoda değil (açık depo, lisanslar belirsiz). Her `data/raw/<ad>/KAYNAK.txt` dosyasındaki adresten indirip aynı klasöre koyun; ilk gereken `data/raw/eac-profil-siniflari/`.

## Çalıştırma

Şimdilik yalnız temel benzetim var (saf Python, bağımlılık istemez):

```bash
python3 src/trafo_bos_kapasite.py 7 cikti.json
```

2 saniyede 3 trafonun sonucunu yazar. Şehir üreticisi, model, kaç ev ve harita geldikçe buraya eklenecek (her biri kendi görev kartında).

## Repo haritası

- [DEVIR.md](DEVIR.md) — **şu an nerede kaldık**: açık faz, kim nerede, bekleyen istekler, sıradaki adım
- [NOTLAR.md](NOTLAR.md) — fikre dair yeni bulduğunu at: kaynak, itiraz, fikir (herkes ekler, Volkan işler)
- [docs/02-faz-0-ogrenim.md](docs/02-faz-0-ogrenim.md) — **yeni gelen buradan başlar**: sorun, kavramlar, okuma sırası, ilk uygulama
- [ROADMAP.md](ROADMAP.md) — fazlar ve bitiş ölçütleri
- [docs/00-overview.md](docs/00-overview.md) — amaç, kapsam, kapsam dışı, başarı ölçütü
- [docs/01-plan.md](docs/01-plan.md) — iş kolları ve takvim
- [docs/glossary.md](docs/glossary.md) — ortak terimler
- [docs/data/data-dictionary.md](docs/data/data-dictionary.md) — her veri: kaynak, birim, kalite, yanlılık
- [docs/method/modeling.md](docs/method/modeling.md) — yöntem ve neden
- [docs/method/validation.md](docs/method/validation.md) — doğrulama protokolü
- [docs/decisions/](docs/decisions/) — karar kayıtları (ADR)
- [docs/log/](docs/log/) — iş ve deney günlüğü (yalnız ekleme)
- [data/raw/](data/raw/) — indirilen ham veri, her klasörde KAYNAK.txt
- [docs/gorev/](docs/gorev/README.md) — görev kartları (Can ve Civan buradan iş alır)
- [docs/istek/](docs/istek/README.md) — istek kutuları: başkasının dosyasında değişiklik istemek için
- [CONTRIBUTING.md](CONTRIBUTING.md) — nasıl çalışıyoruz · [CLAUDE.md](CLAUDE.md) — aynı kurallar ajan için

> Bu README kısa kalır. Derinlik `docs/` altındadır.
