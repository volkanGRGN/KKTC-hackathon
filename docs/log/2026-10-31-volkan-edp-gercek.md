# 2026-10-31 — Şablon yöntemi gerçek veride (ROADMAP 2i)

**Etiket: gerçek veri — İspanya (Oviedo, EDP), 1–20 Mayıs 2018, saatlik.** Farazi şehir sonuçları "gösterim"dir; bu dosyadaki rakamlar ölçümdür.

## Hipotez / amaç
Farazi şehirde doğru cevabı biz ürettik; model kendi kurallarımızla kurulmuş bir dünyayı tahmin ediyor olabilir. Doğru cevabı bizim yazmadığımız bir veride, aynı testle hata kaç?

## Yaptıklarım
- Veri: Mendeley 685vgp64sm (CC BY 4.0), `data/raw/edp-oviedo/KAYNAK.txt`. Zip bu makinede yoktu, aynı adresten yeniden indirildi; SHA-256 KAYNAK'takiyle aynı (4ac9986b…). Ham veri depo dışında.
- Kod: `src/edp_test.py` (yeni). `src/sablon.py` PR #8'de, main'de yok ve abone tarifesine bağlı; o yüzden aynı adımlar (Ward + siluet kümeleme, lojistik atama, ortağa çekili NNLS ölçek, bir-dışarıda P10–P90 bant, sablon.py güven eşikleri) tarifesiz biçimde ayrı dosyada. PR #8 birleşince ortak fonksiyonlara indirilebilir.
- Çalıştırma: `python3 src/edp_test.py <zip>/Sim_files_190128_OK_V0/GIS_data --cikti sonuc.csv` (~40 sn).

### Veri temizliği [Hesap]
- 7 dosya, 3.823.860 saatlik satır, 8.079 sayaç, 30 trafo merkezi.
- **Ondalık virgül hatası:** 1 kWh'i aşan değerler ("1,015") Excel'de binlik ayraç sanılıp 1015 okunmuş. Bu değerlerin hepsi tamsayı ve ≥ 1001; saatte 1000 kWh bir sayaçta olamaz. ≥ 1000 olanlar 1000'e bölündü. Bölünmeden müşteri toplamı trafo ölçümünün 100–400 katıydı; bölünce 0,4–1,04 katı, saatlik korelasyon çoğunda 0,95+.
- Estado ≠ 0: 18.370 satır; Tipo proceso = M (elle/tahmini): 289 satır. Birlikte 18.659 satır (%0,49) atıldı. 21 Mayıs (yarım gün) atıldı.
- **Trafo başı ölçüm cihazı bulundu:** "ZIVS…" ile başlayan 30 sayaç, her trafo merkezinde bir tane; değerleri müşteri toplamıyla saat saat örtüşüyor. Doğru cevap olarak bu kullanıldı (Kıb-Tek'in takacağı cihazın karşılığı). Müşteri toplamı/trafo ölçümü oranı 0,42–1,04: bazı trafolarda müşteri sayaçlarının bir kısmı veride yok ya da kayıp/aydınlatma var.
- Çıkarılan trafo: C401571 (TD402679), tek sayaç, sıfır. **TD009456 (C005648) çıkarılmadı:** Can'ın sıfır bulduğu OpenDSS profilleriydi; ham sayaç verisinde bu trafo dolu (öğlen en düşük gerçek), 29 trafo kaldı.
- Panel: 246 sayaç dönemde en az bir saat elektrik verdi, ama trafo başında hiç geri akış yok (en çok 0,0 kW). Brüt ≈ net; hedef trafo başı çekilen yük. Panel üretimi bilinmiyor, ayrıştırılmadı.
- Hedef: iş günü + tatil, 11:00–13:59 saatlik en düşük trafo yükü: 24,6–187,2 kW. 1 Mayıs tatil.

### Girdiler (Kıb-Tek'in de bildiği türden)
Müşteri sayısı, kVA (28 × 630, 1 × 1000, 1 × 250), panelli sayaç / müşteri, toplam hat boyu, havai hat payı, üç faz sayaç payı.
- **a:** bunlar; ölçek = müşteri sayısı.
- **b:** a + 4 "sayaç tipi". Tipler YALNIZ ölçülü trafoların sayaçlarının iş günü eğrilerinden k-means ile çıkar. Ölçülmeyen trafonun sayacına tip eğrisiyle (o eğriler toplanınca cevap olur = sızıntı) değil, Kıb-Tek'in bildiği dönem faturası, panel ve faz ile eğitilmiş sınıflandırıcıyla verilir.
- **c:** a + trafodaki faturaların toplamı. Fatura hedefle aynı üç haftayı kapsadığı için **üst sınır**; gerçek kullanımda yıllık fatura olur (ADR-0007).
- **Kıyas:** ölçülülerde Σ öğlen en düşük ÷ Σ müşteri × müşteri sayısı.

Deney: 5 / 10 / 15 ölçülü, her biri 20 rastgele + 20 tabakalı seçim; hata yalnız ölçülmeyenlerde.

## Sonuç [Hesap]

Ölçülmeyen trafolarda öğlen en düşük yük hatası (|tahmin − gerçek| ÷ gerçek), 10 ölçülü:

| | ortanca | P90 | %80 bant kapsama |
|---|---|---|---|
| Farazi şehir, 12 ölçülü (gösterim, PR #8) | %8,6 | %32,6 | — |
| Gerçek, a (müşteri + kVA + hat + faz + panel) | %25–26 | %57–59 | %74 (rastgele) / %85 (tabakalı) |
| Gerçek, b (a + sayaç tipi) | %24–25 | %58 | %73 / %83 |
| Gerçek, c (a + fatura toplamı, üst sınır) | %10–11 | %32–33 | %80 / %67 |
| Gerçek, kıyas (müşteri başına ortalama) | %25–26 | %57–59 | — |

5 ve 15 ölçülüde tablo hemen hemen aynı (a: ortanca %23–25; c: %10–14). Ölçülü sayısını 5'ten 15'e çıkarmak bu 29 trafoda hatayı düşürmedi.

Güvene göre (bütün deneyler): a'da yüksek %18 / orta %24 / düşük %26 ortanca; az da olsa sıralı, ama "yüksek" çok seyrek (19 / 2.280). c'de etiket ayırmıyor (%13 / %11 / %12).

Yanlış yeşil vekili (öğlen en düşük yükü %20'den fazla yüksek tahmin etmek = trafoya olduğundan fazla güneş sığar demek), 10 ölçülü: a %44, b %42, kıyas %44, c %17. a/b/kıyas ortancada %15 yukarı kayık.

## Yorum [Yorum]
1. Yalnız müşteri sayısı ve şebeke bilgisiyle şablon modeli, "müşteri başına ortalama × müşteri" kıyasını **geçmiyor**. Eğri şekli kümeleri büyüklüğü açıklamıyor; burada trafolar arası fark müşteri başına tüketimden geliyor.
2. Kıb-Tek'in elindeki fatura bilgisi girince hata 2,5 kat düşüyor, P90 farazi şehirle aynı (%33). Fatura burada iyimser (aynı dönem); yıllık faturayla gerçek kayıp ölçülmedi.
3. Farazi şehirdeki %8,6 ortanca gerçek veride %10–11 (faturalı) ya da %25 (faturasız). Farazi şehir yöntemi iyi gösteriyor; yalnız farazi sonuca dayanmak iyimser.
4. Sayaç tipi (b) neredeyse hiçbir şey katmıyor: tipi ölçülmeyen sayaca verecek elde yalnız fatura/faz/panel var.

## Sınırlamalar
- İklim: Kuzey İspanya, Mayıs; klima yok, panel çok az (geri akış sıfır). KKTC öğlen yükü ve panel etkisi farklı.
- Saatlik çözünürlük (sözleşme 5 dakika); saatlik en düşük, 5 dakikalık en düşükten yüksek olur.
- Abone tipi yok; 28/29 trafo aynı güçte (kVA bilgi taşımıyor).
- 29 trafo, 20 gün; bir-dışarıda bant ve güven küçük örnekte oynak.
- Müşteri sayaçlarının bir kısmı eksik (toplam/trafo ölçümü 0,42'ye kadar); fatura girdisi bu yüzden bazı trafolarda eksik.
- c'deki fatura hedefle aynı dönem: üst sınır.

## Yıl uyumu kontrolü (Volkan'ın sorusu, farazi şehir)
Farazi şehirde nüfus × tüketim çarpımı yok. Abone sayısı ve abone başına tüketim ikisi de Kıb-Tek 2023 [Kaynaklı: stat_2023]. Tek istisna otel: 2023 tüketimi ÷ 2025 tesis sayısı. EAC eğrileri 2022, ama yalnız şekil (yıllık ortalamaya bölünmüş). Işınım 2024/2025 (Open-Meteo).
2024'e taşıma denendi: Kıb-Tek "2024 statistic.pdf" (kibtek.com/statistikler) yalnız Ocak–Temmuz tüketimini tarife sınıfına göre veriyor, **abone sayısı yok** [Kaynaklı]. Yani tüketim ve abone sayısının aynı yıldan geldiği en yeni tam yıl 2023, şimdiki hali zaten bu. Kalan uyumsuzluk: ışınım yılı (Open-Meteo'dan 2023 indirilerek giderilebilir) ve otel tesis sayısı.

## Karar / sıradaki adım
- Jüriye doğruluk rakamı olarak gerçek veri: "müşteri sayısıyla ~%25, fatura bilgisiyle ~%10 ortanca hata (İspanya, 29 trafo)".
- Modele yıllık fatura toplamı girdisi şart (ADR-0007 ile uyumlu); şablonun asıl kazancı burada.
- Karar masasına: farazi şehirde ışınım yılını 2023'e çekmek (`src/sehir_uret.py`, Volkan'ın dosyası).
- Zaman kalırsa (6): OpenDSS gerilimi ile `trafo_bos_kapasite.py` kıyası — yapılmadı.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
