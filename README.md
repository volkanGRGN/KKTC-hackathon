# Trafo Görünürlük Haritası

Kıb-Tek'in göremediği mahalle trafolarını, az sayıda ölçümden öğrenen bir modelle haritada görünür kılar: her trafo yılın en yoğun saatinde ne kadar dolu, kaç ev daha çatıya güneş paneli takabilir, bu tahminden ne kadar eminiz.

*In English:* a visibility map for distribution transformers in Northern Cyprus. A share of transformers is measured for two weeks; a template model estimates every other transformer's annual peak load and how many more homes can add rooftop solar, with an honest uncertainty band. Prototype built at the Sustainable Cyprus Hackathon (VCC-2), 31 Oct – 1 Nov 2026.

Sürdürülebilir Kıbrıs Hackathonu (VCC-2) · Lapta · 31 Ekim – 1 Kasım 2026 · **Durum: çalışan prototip; Kıbrıs verisiyle henüz sınanmadı.**

## Sorun

- Kuzey'de yaklaşık **2.670 çatı güneşi başvurusu** bekliyor; Kıb-Tek'in alçak gerilim şebekesini izleyen bir sistemi yok [KTTO raporu, Mart 2023; adres doğrulanmadı].
- Güney Kıbrıs paneli bağladı, şebeke taşıyamayınca 2025'te güneş üretiminin **%47'sini** kıstı [pv-magazine, Ocak 2026].
- Bugünkü kaba kural ("trafo gücünün %40'ına kadar panel") hat ucundaki gerilimi görmüyor.

## Ne yapıyor

Trafoların bir kısmı iki hafta ölçülür. Model, benzer trafolardan öğrendiği günlük yük eğrileriyle ("şablon") gerisini tahmin eder ve haritada iki soruyu cevaplar:

| Katman | Soru | Ne zaman | Sınır |
|---|---|---|---|
| **Yük haritası** | Trafo ne kadar dolu? | Yılın en yoğun saati, çoğunlukla yaz akşamı | Trafo gücü ve akşam gerilimi (207 V) |
| **Panel** | Güneş için ne kadar yer var? | Bahar öğleni, yük en düşükken | Öğlen gerilimi (259 V) ve trafo gücü |

Yöntem, İngiltere'nin 824 trafoyu ölçüp gerisini tahmin ettiği mahalle trafosu şablonu çalışmasının Kıbrıs'a uyarlamasıdır. Araç başvuru reddetmez, ayırır: bariz uygun olan hızlı onay alır, bariz dolu olan işaretlenir, emin olunamayan yerde önce ölçülür.

## Ne kadar tutuyor

Kıbrıs'tan trafo verisi alamadık. Yöntemi iki yoldan sınadık: açık **gerçek veride** (İspanya, İngiltere) ve Kıbrıs'a benzetilmiş **deneme şehirlerinde** (cevabı bilinen, modelin hiç görmediği şehirler). Deneme şehri rakamları gerçeğin üst sınırıdır.

| Katman | Nerede | Sonuç |
|---|---|---|
| Yük haritası | Gerçek veri, İspanya, Mayıs tepesi | yılın tepesi hatası ortanca %15,4 (bölgede klima yok) |
| Yük haritası | Deneme şehirleri 41–50 | tepe hatası ortanca %11,4; %80'den dolu 12 trafonun 12'si yakalandı; tahmin güvenli yönde, gerçeğin biraz üstünde |
| Panel | Gerçek veri, İspanya, 29 trafo | öğlen yükü hatası yalnız abone sayısıyla ~%25, faturayla ~%10 |
| Panel | Gerçek veri, İspanya, 28 trafo | söylenen "%80 aralık" trafoların %82,1'inde tuttu |
| Panel | Deneme şehirleri 31–40 | "güvenle sığar" (yeşil) denen 60 trafonun hiçbiri dolu değil; gerçekte dolu 46 trafonun 24'üne bugünkü %40 kuralı "yer var" diyor, model hiçbirine |

Ayrıntı ve kaynaklar: [dashboard/icerik.json](dashboard/icerik.json) ve [docs/log/](docs/log/).

## Ne tutar

| Ne | Maliyet |
|---|---|
| Bir trafoyu taşınabilir cihazla ölçmek | ~19 bin TL (~333–341 €) |
| Kıbrıs pilotu, 120–170 trafo | ~2,2–3,2 milyon TL (~40–58 bin €) |
| Kıyas: her trafoya kalıcı cihaz | ~300–419 milyon TL; pilot bunun ~%1'i |

Kur TCMB 30.10.2026; KDV, gümrük ve Kıb-Tek personelinin süresi dahil değil. Hesap: [maliyet günlüğü](docs/log/2026-11-01-volkan-maliyet-sunum.md).

## Sıradaki adım

Kıb-Tek ile ilkbaharda 120–170 trafoluk pilot: ölç, tahmin et, 10 trafoda kör test. Başarı ölçütü: gerçekten dolu trafoların en az %90'ı yakalanır. Kıb-Tek'e sorulacaklar: [docs/01-plan.md](docs/01-plan.md) ("Uzmana sorulacaklar").

## Dene

```bash
git clone https://github.com/volkanGRGN/KKTC-hackathon.git
cd KKTC-hackathon
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

Deneme şehirleri ve ham veri depoda değil: önce şehirleri üretin ya da hazır kopyayı `data/synthetic/` altına koyun. Komutlar [docs/calistirma.md](docs/calistirma.md), dashboard ayrıntısı [dashboard/README.md](dashboard/README.md).

## Ekip

Volkan Görgün (takım lideri; model ve panel katmanı) · Can Şahin (veri, yük haritası ve sınav) · Civan Orak (harita, veri araştırması ve sunum)

## Lisans

[Business Source License 1.1](LICENSE). Özetle: kodu okumak, denemek, değiştirmek ve araştırmada kullanmak serbest; gerçek şebeke işletmesinde ya da ticari bir hizmette kullanmak için ekipten ticari lisans gerekir. 1 Kasım 2030'da Apache 2.0'a döner. `data/raw/` altındaki üçüncü taraf verileri kendi lisanslarındadır (her klasörde KAYNAK.txt). Bağlayıcı metin [LICENSE](LICENSE).

## Ekip için: repo haritası

- [docs/calistirma.md](docs/calistirma.md) — bütün komutlar: deneme şehri üretimi, model, sınav, kalibrasyon, dashboard
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
- [dashboard/](dashboard/README.md) — proje kimliği, şehir özetleri, trafo kartları, resmi rakamlar, canlı tahmin (model sürümleriyle)
- [docs/gorev/](docs/gorev/README.md) — görev kartları (Can ve Civan buradan iş alır)
- [docs/istek/](docs/istek/README.md) — istek kutuları: başkasının dosyasında değişiklik istemek için
- [CONTRIBUTING.md](CONTRIBUTING.md) — nasıl çalışıyoruz · [CLAUDE.md](CLAUDE.md) — aynı kurallar ajan için
