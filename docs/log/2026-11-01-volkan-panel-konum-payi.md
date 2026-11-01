# 2026-11-01 — Sarıda konum payı: `yesil_konum_payi` (BUILD 2 — panel; ADR-0015 m. 4)

**Amaç:** Karar masası 00:39 / 00:49: renksiz trafoda (ADR-0017 `pv_uc` = `bos`) yan panele bilgi olarak "hattın ilk %x'indeki evden başvuru büyük olasılıkla evet" (renk değil). ADR-0015 m. 4: sarı düz renk değil sayı + konum; sözleşme 1.4 adayı `yesil_konum_payi` (hat boyunun payı). Soru: bu bilgi ne kadar trafoda ve başvuruda verilebiliyor, ve verildiğinde yanlış "evet" çıkıyor mu.

## Yöntem
- `src/kac_ev_olasilik.py` `konum_payi()`: başvuranın hattı ve hattaki yeri biliniyor (başvuru formu), gerisi resmi hesabın aynı çekilişleriyle (ağ, bara, OG, öğlen yükü, panellerin yeri, model-sapma; ayrı rastgele akış, resmi sütunlar değişmez). Her çekilişte her hatta, y = 0,1 … 1,0 yerindeki eve (o hattın y'yi geçen ilk evi, temkinli) tek 6,5 kW başvuru eklenir; 259 V ya da kVA aşılırsa o yer ve ötesi düşer. Pay = 40 çekilişin hepsinde ve bütün hatlarda sığan en büyük y (P ≥ %98, haritanın yeşil eşiği; 40 çekilişte "hepsi"). Yük güveni yüksek değilse ya da haritanın bugün aşma olasılığı > 0,02 ise 0 (haritayla çelişmesin). Yalnız panelli evlerden oluşan kol atlanır (başvuran panelsiz).
- Hat bilinmediği için harita düzeyinde **en kötü hat** belirler (en uzun hat genelde): pay her hat için geçerli.
- `kac_ev.csv` sonuna `yesil_konum_payi` (sözleşme §6, 1.4 adayı) yazıldı; 1–10 ve 21–30'da yeniden koşuldu, ilk 13 sütun eski çıktıyla 800 satırda birebir. (Karar masası 01:01'den sonra sütun çıkarıldı; aşağıda.)
- Doğrulama `src/guvenli_uc.py --konum` (PR #22'nin `sahte_kayit`'i gerekir): payı > 0 olan trafolarda hattın ilk x'indeki her panelsiz konutun tek başvurusu gerçek ağda kritik anlarda sığıyor mu (cevap anahtarının tanımı).
- 1–10'da kuruldu (ayar yok; eşik yeşilinki); **sınav 21–30 bir kez** (~00:56). Platform BUILD 2 klasörü, Mac, Python 3.12.13; üretici 1.3 (K_YUK 1,47).

## Sonuç [Hesap; farazi şehir, gösterim]
| | Geliştirme 1–10 | Sınav 21–30 |
|---|---|---|
| Renksiz trafo / payı > 0 | 336 / **18** (pay ortancası 0,4) | 336 / **17** (0,5) |
| Renksizde payın içindeki aday / tüm aday | **%0,4** (34/8.167) | **%0,4** (33/8.027) |
| Renksizde yanlış evet | **0/34** | **0/33** |
| Yeşil trafo / payı > 0; kapsanan aday | 44 / 41; 140/227 | 38 / 36; 77/87 |
| Yeşilde yanlış evet | 0/140 | 0/77 |
| Bayraklı trafoda payı > 0 | 0/20 | 0/26 |
| Hepsi: yanlış evet | 0/174 | 0/110 (95% üst sınır ~%3,4) |

Renksiz trafolarda payın neden 0 olduğu (sınav 21–30, 336 trafo): yük güveni yüksek değil **193 (%57)**; güven yüksek ama bugün aşma olasılığı > 0 **112 (%33)**; ikisi de uygun 31, bunların 17'sinde pay > 0. Geliştirmede aynı yön (189 / 122 / 25 → 18).

## Bulgular
1. **Konum payı güvenli:** verildiği her yerde gerçekte sığıyor (iki şehir grubunda 284 başvuruda 0 yanlış evet). Ama örnek küçük: tüzük madde 6'ya göre "%2'nin altında" demek için ~150 bağımsız noktada 0 gerekir, sınavda 110 [Yorum].
2. **Renksiz trafoda değeri çok küçük:** renksiz trafoların %5'inde bilgi var, olası başvuruların %0,4'ünü kapsıyor. Sarıyı açmıyor.
3. **Darboğaz yine yük tarafı:** renksizin %57'sinde öğlen yükü tahmininin güveni yüksek değil (kural gereği bilgi yok), %33'ünde bugün bile aşma olasılığı sıfır değil. Konumu bilmek tek başına yetmiyor; ADR-0015'in "sarının çoğunu konuma bağlı yeşile çevirir" beklentisi (bilginin değeri S4, eski şehirler, faz + konum + bara birlikte) bu kayıtsız hâlde tutmuyor.
4. Yeşil trafolarda pay çoğunlukla 1,0 (hattın tamamı): yeşil zaten "ilk iki başvuru güvenle sığar"; konum payı orada ek bilgi değil.

## Ne kaldı
- Gösterim Civan'da (civan.md UYARI): yalnız renksiz trafoda ve pay > 0 ise yan panelde bir cümle; renk değişmez.
- Kayıtlarla konum payı (PR #22 motoruyla, başvuranın kayıtlı yeri + diğer panellerin kayıtlı yeri) ölçülmedi; başvuru anı motoru zaten başvuranın yeriyle karar veriyor (PR #22: hemen evet %3,8 → %9,7).
- Güven eşiği ve "40 çekilişin hepsi" kuralı yeşilinkiyle aynı; gevşetmek 1–10'da ayrı bir karar.

## Karar (karar masası 01:01)
Haritaya kart yok, `kac_ev.csv`'ye `yesil_konum_payi` sütunu yok: renksiz trafoda neredeyse hep boş kalıyor; evin konumuna göre kararı başvuru anı motoru (PR #22) zaten veriyor. Sütunu yazan kısım çıkarıldı (`kac_ev.csv` ilk 13 sütun + `pv_uc` aynen), sözleşme §6 satırı geri alındı; `konum_payi()` ve `guvenli_uc.py --konum` analiz olarak kaldı (aynı tohumlar, 1–10'da sonuç birebir: renksiz 18 trafo, 0/34). Sonuç ROADMAP Faz 9'a: "denendi, renksizde bilgi vermiyor; darboğaz yük güveni ve bugünkü aşma olasılığı". Panelde evet'in darboğazının öğlen yük güveni olduğu bulgusu BUILD 1'e gidiyor (karar masası).

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas ~00:52 | v2b + `yesil_konum_payi` (yeşil eşiği, en kötü hat) | 1–10 | renksizde konum bilgisi verilebilir, yanlış evet yok | renksiz 24 trafo, %0,7 aday, 0/60; 6 trafo haritayla çelişiyordu | haritayla çelişme kuralı |
| 1 Kas ~00:54 | + `p_bugun_asar` > 0,02 ise 0 | 1–10 | aynı | renksiz 18 trafo, %0,4 aday, 0/34; ilk 13 sütun birebir | 21–30 bir kez |
| 1 Kas ~00:56 | aynı | 21–30 | aynı | renksiz 17 trafo, %0,4 aday, 0/33; hepsi 0/110 | PR, Civan'a yan panel |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
