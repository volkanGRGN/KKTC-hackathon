# Trafo Şablonu fikri — kapsamlı araştırma

VCC-2 · Sürdürülebilir Kıbrıs Hackathonu · 31 Ekim 2026 gece

**Etiketler:** [Kaynaklı] yayın/rapor · [Hesap] bizim hesabımız · [Yorum] değerlendirme · BULAMADIM → uzmana soru

**Fikir (tek cümle):** Kıb-Tek mahalle trafolarının gerçek yükünü görmüyor; İngiltere'nin "ağ şablonları" yöntemiyle az sayıda trafoyu ölçüp gerisini tahmin ediyoruz ve her trafo için "öğlen ne kadar dolu, kaç panel daha sığar" sonucunu haritada gösteriyoruz. Gösterim farazi bir Kıbrıs şehrinde; kanıt İngiltere'nin gerçek verideki ~%80'i.

---

## 1. İngiltere projesi — doğrulanmış rakamlar [Kaynaklı, kaynak PDF'leri okundu]

- 828 trafoda 84 milyon gerilim ölçümü: %99,31 sınır içinde, %0,69 253 V üstü. Hat uçlarında 96 milyon ölçüm: %99,62 içinde, %0,35 üstte. Ev panellerinin **trafodaki** gerilimde görünür etkisi yok (etki hat ucunda görünür). (Ofgem ilerleme raporu, Mayıs 2013)
- 824 trafo = Güney Galler trafolarının %2,6'sı. Şablon doğruluğu "yaklaşık %80", diğer dağıtım şirketlerinin verisinde %80–90; şablonlar İngiltere trafolarının %82'sine uydu (hedef %50). Panel çıkışı beyanın en çok %81,1'i → gerilim etkisi hesaplanandan %36 düşük → şirket planlama aracını değiştirip daha çok panel bağladı. (Ofgem ödül başvurusu, Mayıs 2015)
- Para gerilim ölçümünden geldi: Güney Galler'de gerilim %1 düşürüldü, ölçülen kazanç yılda ~14 milyon £. Dört bölgeye yayılan ikinci %1 için 116 milyon £/yıl şirketin 2019 mektubundaki **beklenti**. Şirket mühendisi: en büyük fayda gerilim ölçümünün gerilim profilini göstermesi. (REF 2021 Bath etki vakası)
- Ekibin notundaki "%87 doğruluk (Ran Li tezi)" doğrulanamadı; sunumda Ofgem'in ~%80'i kullanılmalı.

## 2. KKTC parametreleri (farazi şehir için) [Kaynaklı, hafıza notlarından]

- Kıb-Tek tüketici: 219.931 (Aralık 2023), konut 175.577. Tarife sınıfına göre (2023): Ticari I 20.950 abone / 210.978 MWh; Ticari II 494 / 169.496; Endüstri I 1.227 / 22.391; Endüstri II (kVA'lı) 352 / 95.996; Su Motorları 3.250 / 51.256 (köy depoları + sulama kuyuları); soğuk zincir ve ağıllar 556 / 7.593. → İngiltere'deki "profil sınıfına göre müşteri sayısı" girdisinin Kıbrıs karşılığı bu tarife sınıfları.
- Trafo: direk tipi 25/50/100/250/400 kVA, çıkış 433 V (faz 250 V, boşta), kademe ±%5 yalnız enerjisizken; yer tipi 50–2.500 kVA. Mahalle trafosunda yük altında ayar yok.
- Inverter 240 V +%10 ≈ 264 V'ta kapanıyor; 50,2 Hz üstünde her 0,1 Hz'de %4 kısıyor (YEK EK2 2025). Boştaki 250 V ile 264 V arasında ~14 V pay; benzetimde planlama sınırı 259 V.
- %40 kuralı: panel bağlandığı trafoda sayılır; aynı trafoya çok başvuru güç oranında paylaşılır; müstakil trafolu su motorları ve özel tesislerde aranmaz (tüzük 5(14), 5(6)(A)(a)).
- Bekleyen çatı başvurusu ~2.670 (çoğu 5–8 kW, 13–21 MW). Kıb-Tek'in alçak/orta gerilimde izleme sistemi yok (KTTO raporu, Mart 2023).
- Sistem yükü: ilkbahar öğleninde 91–130 MW'a iniyor; gece en düşük ilkbahar 145–160, yaz 230–260, kış 165–210 MW.
- Turizm: 2025 sonu 171 tesis, 27.775 yatak (25 beş yıldızlı otel 17.434 yatak); Girne 15.220, İskele 7.793 yatak. Doluluk Ağustos %68,5, Şubat %28,4.
- Tarife: düz 12,09 TL/kWh; üç zamanlı yazın puant 09–18 (16,73), kışın 17–22.
- [Hesap, vekil] Güney: 17.886 dağıtım trafosu, 615.479 tüketici → trafo başına ~34 tüketici; Kuzey'de ~6.400 trafo. Güney'de alçak gerilim hattı 18.203 km → trafo başına ~1,0 km. Ölçülecek trafo: %2,6 × 6.400 ≈ 170.
- BULAMADIM: Kuzey'de gerçek trafo sayısı, abone–trafo eşleşmesinin dijital olup olmadığı, öğrenci yurdu sayısı.

## 3. Harita paneli teknolojisi [Kaynaklı]

- Streamlit 1.39 ve sonrası pydeck haritasında tıklamayı yakalıyor (`on_select="rerun"`, katmana `id` ve `pickable=True` gerekli). 3D sütun için pydeck ColumnLayer.
- [Yorum] pydeck'in varsayılan altlık haritası internetten iniyor; kamp internetine güvenmeyin. Yedek: altlıksız harita + şehir sınırını/sokakları çizen GeoJSON katmanı, ya da ekran kaydı.

## 4. Farazi şehrin verisi — en iyi kaynak Güney Kıbrıs'ın kendisi

**Güney dağıtım şirketinin "Profil Sınıfları" (EAC, Nisan 2023) [Kaynaklı, Excel ve PDF arşiv kopyasından indirilip okundu]:** 12 tüketim sınıfı, 2022 yılı için 30 dakikalık seri (17.520 satır) + 24 tipik gün (12 ay × iş günü/tatil). Değerler birim değer; taban abonenin yük hakkı (kVA). Lisans belirtilmemiş → kaynak gösterilerek kullanılmalı.
- Sayfalar: DOMESTIC, DOMESTIC_with_NM (konut + panel), SMALL_COMMERCIAL, L._COMM._SHOPS_STORES (büyük ticari, otel hariç), **L._COMM._STORES = otel** (PDF'teki sıra "ε. Büyük ticari (otel birimleri)" bölümüne denk geliyor; sayfa adı yanlış yazılmış — ben de PDF'ten doğruladım), SMALL_INDUSTRIAL, LARGE_INDUSTRIAL, COMM._with_NB ve IND._with_NB (panelli ticari/sanayi), STREET_LIGHTING, WATER_PUMPS, THERMAL_ENERGY_STORAGE.
- Örneklem: konut ve konut+panel 2016'da 68 ev; küçük ticari 23, büyük ticari-dükkân 79, otel 30, küçük sanayi 66, büyük sanayi 41. Su pompası, sokak aydınlatması, ısı depolama ölçüm değil "analizle türetilmiş" (pompa: sürekli 1,0, Haziran–Eylül iş günü 11:00–15:30 kapalı).
- Ajanın okuduğu değerler [Kaynaklı/Hesap, ben tek tek kontrol etmedim]: konut Temmuz öğlen 0,110, Nisan öğlen 0,065 (akşam tepesinin ~%71'i); konut+panel Nisan öğlen −0,152 (şebekeye veriyor); küçük ticari Temmuz öğlen ~0,28; otel Temmuz ortalaması Ocak'ın ~4 katı; sanayi Nisan iş günü öğlen ~0,21–0,23.
- Adresler: Excel `web.archive.org/web/20240429185043/https://www.eac.com.cy/EL/RegulatedActivities/Distribution/agorailektrismou/Documents/Profile%20Classes/Offtake_Profile_Classes.xlsx`, PDF aynı klasörde Profile_Classes.pdf. Aynı klasörde Injection_Profile_Classes.xlsx ve Profile_Class_Calculator.xlsx var.
- [Yorum] Bu, İngiltere'deki 8 profil sınıfının Kıbrıs karşılığı ve Kıb-Tek'in tarife sınıflarıyla (konut, ticari I/II, sanayi I/II, su motorları) neredeyse birebir eşleşiyor → "abone karışımından şablona atama" adımı doğrudan kurulabilir.
- BULAMADIM: köy (varsayım: konut + küçük ticari karışımı), öğrenci yurdu (Akdeniz'den açık veri yok; LoadProfileGenerator klima modülüyle ya da konuttan türetme), tarımsal sulama (EAC pompa kuralı içme suyu pompası için).

**Diğer Kıbrıs verisi:** Lefkoşa'da tek ev, 30 saniyelik, split klimalı, CC-BY-4.0 (zenodo.org/records/8348862); SmartPV 68 ev 2016 saatlik CC-BY-4.0 ama erişim kısıtlı (zenodo.org/records/15209301).

**Yedekler:** İspanya REE 2026 başlangıç profilleri (saatlik, konut 2.0TD + küçük ticari 3.0TD, akıllı sayaç 2022–2025); Almanya BDEW H0/G0–G6/L0–L2 ve 2025 sürümleri (klima yükü yok, Kıbrıs'a zayıf).

**Şebeke yapısı (hazır, Python'dan açılır) [Kaynaklı]:**
- SimBench (Almanya): 6 alçak gerilim şebekesi — rural1 (13 düğüm, 160 kVA), rural2 (93, 250 kVA), rural3 (118, 400 kVA), semiurb4 (39, 400), semiurb5 (104, 630), urban6 (53, 630). Veri ODbL, kod BSD-3; pip ile kurulup pandapower'da hazır.
- IEEE Avrupa Alçak Gerilim Test Fideri: 906 bara, 55 tek fazlı ev, pandapower'da hazır.
- ENWL: 25 gerçek İngiliz şebekesi, 131 fider, 5.952 müşteri (OpenDSS/Excel).
- İspanya EDP gerçek kentsel şebeke: 30 trafo, 8.087 müşteri, 20 gün akıllı sayaç, CC BY 4.0 (data.mendeley.com/datasets/685vgp64sm/1) — Akdeniz'e en yakın gerçek şebeke.
- [Yorum] Bizim saf Python benzetimimiz zaten ev ev gerilim hesaplıyor; SimBench'i şebeke ölçüleri (hat boyu, kablo, ev sayısı) için kaynak olarak kullanmak, pandapower'a geçmekten daha az risk.

**İngiltere'nin 10 şablonunun sayısal verisi:** indirilebilir halde BULAMADIM (2013 ön veri dosyasının bağlantısı ölü; Ofgem raporunda yalnız grafik; bugünkü NGED portalında yok). Şablonları kendi farazi şehrimizden kümeleyerek çıkarmamız gerekiyor — zaten yöntemin kendisi bu.

## 5. Kaç panel sığar — hesap yöntemi, dünya örnekleri, maliyet

**Tanım [Kaynaklı]:** barındırma kapasitesi = güç kalitesini bozmadan, şebekeyi yükseltmeden bağlanabilecek üretim. EPRI'nin üç yolu: stokastik (binlerce rastgele yerleşim), streamlined (empedanstan hızlı hesap, devre başına ~10 dakika), iteratif (Kaliforniya, ~27 saat). (EPRI Ocak 2016, okundu; süre karşılaştırması arama özeti)

**48 saatte kodlanacak yöntem (trafo başına) [Hesap, standart mühendislik + yorum]:**
1. Girdiler: trafo gücü S, mevcut panel gücü, şablondan öğlen en düşük yük P_min (karamsar: alt yüzdelik), en uzak eve hat boyu L, iletken direnci r (Ω/km), V0 = 250 V, sınır 259 V.
2. Isıl sınır: S·cosφ + P_min − mevcut panel. Yanına bugünkü kural: 0,4·S − mevcut panel.
3. Gerilim sınırı: pay ΔV = 259 − 250 − trafo yükselmesi; panel hatta yayılmışsa etkin mesafe d = L/2. Dengeli üç faz P = 3·V0·ΔV/(r·d); faz bilinmiyorsa tek faz en kötü durum P = V0·ΔV/(2·r·d) (2 = nötr dönüşü). Kapasite = P + P_min − mevcut panel.
4. Sonuç = ikisinin küçüğü; 6,5 kW'a bölünce "kaç ev daha".
5. Renk: yeşil = karamsar senaryoda (düşük yük, faz bilinmiyor) bile yer var; sarı = yalnız iyimser senaryoda; kırmızı = hiçbirinde.
6. İsteğe bağlı: 1.000 rastgele yerleşim, aşırı gerilim olasılığı ≤%5 olan kapasite (Deakin vd. 2019, okundu).
- Örnek [Hesap]: 400 m hat, d = 0,2 km, r = 0,32 Ω/km (varsayım, doğrulanmadı), 9 V pay → dengeli üç fazda ~105 kW, tek fazda ~17,6 kW. Faz bilgisi sonucu ~6 kat değiştiriyor; 250 kVA trafoda %40 kuralı 100 kW der → kural tek faza yığılmada yanlış "yeşil" verebilir. Benzetimimiz için bu formül, ev ev yük akışıyla karşılaştırılıp doğrulanmalı.

**Ölçümsüz tahmin örnekleri:**
- İngiltere ENWL izlenmeyen trafoların tepe yükünü orta gerilim fider ölçümünü abone sayısı oranıyla paylaştırarak tahmin ediyor (açık veri sayfası, okundu).
- Torquato vd. 2018 (IEEE TPWRD 33(2)): Brezilya'da 50.000 gerçek alçak gerilim şebekesi; rastgele %1'lik örnek bütünün kapasitesini tahmin etmeye yetiyor, en kısıtlayıcı etki aşırı gerilim (arama özeti). [Hesap] 170/6.400 ≈ %2,7.
- NGED ölçümsüz trafoda günlük tepe yük tahmini "%5–15" (arama özeti, ne ölçüldüğü belirsiz — kullanmayın).

**Dünyada mahalle trafosu düzeyinde güneş kapasitesi haritası neredeyse yok [Kaynaklı + Yorum]:** Kaliforniya ve New York orta gerilim hattı düzeyinde; Hawaii orta gerilim, alçak gerilimi başvuruda ayrıca kontrol ediyor; İrlanda ESB alçak gerilim trafolarını gösteriyor ama yük için; İngiltere NGED sekonder trafoda yalnız talep payı. Trafo başına çatı güneşi katmanı olan tek örnek Avustralya Energex/Ergon (sayfa 403, arama özeti, "güvenilmemeli" uyarılı). Hepsi "harita gösterge, başvuruda ayrıca kontrol" diyor.

**Güney Kıbrıs:** 2025'te dağıtım şebekesine bağlı güneş ve biyogaz üretiminin %47,44'ü (306 GWh) kısıldı; Ocak–Mayıs 2026'da %65; 2025'ten itibaren ev panelleri de kısılıyor (pv magazine 13.01.2026 ve 15.06.2026, CyprusGrid verisi). Güney dağıtım şirketi bağlantıda "ekipman yükü <%100, gerilim farkı <%2" ve tüm inverterlerde %40 güçten itibaren cosφ(P) ayarı istiyor (CIRED 2024, okundu). Mahalle trafosu kuralı BULAMADIM. → [Yorum] Sunum için güçlü cümle: "Güney panelleri bağladı, şimdi yarısını atıyor; Kuzey bağlamadan önce nereye sığdığını bilmeli."

**Maliyet [Kaynaklı]:**
| Kalem | Fiyat | Kaynak |
|---|---|---|
| Fluke 1736/1738 taşınabilir analizör | 9.384 $ (kiralama ~85 $/gün, arama özeti) | shop.fluke.com, okundu |
| Hioki PW3360-21 | 1.978 € KDV hariç, pensler ayrı | shop.hioki.eu, okundu |
| İngiltere kalıcı trafo izleme | trafo başına 3.000–3.600 £ (ED1 dönemi teklifleri); plan toplamı ~1.660 £/trafo [Hesap] | SPEN, Haziran 2017, okundu |
| Direk trafosu 25→50 kVA | 7.408 £ | NIE Networks, Ağustos 2024, okundu |
| Yeni 315 kVA trafo merkezi | 50.000 £ | aynı belge |
| Kıb-Tek trafo değişimi | BULAMADIM | |

- SPEN'de izleme, eski maksimum talep göstergelerine göre trafo başına ortalama %8 (39,2 kVA) ek kapasite açtı (okundu).
- [Hesap] 170 trafo: kalıcı cihazla ~0,28–0,61 milyon £; 10 Hioki ile ~20.000 € + pensler, trafo başına 1 hafta → ~17 hafta; Fluke kiralayarak ~101.000 $. Ölçüm ilkbahar öğlen en düşük yük günlerini kapsamalı.

**Güvenlik payları [Kaynaklı]:** New York DRIVE 1,05 pu aşırı gerilim, %3 gerilim sapması, %100 ısıl; EN 50160 haftalık 10 dakikalık ortalamaların %95'i ±%10 içinde (arama özeti); Güney Kıbrıs <%2 gerilim farkı. [Yorum] KKTC için: faz bilinmiyorsa tek faz en kötü durum, öğlen yükünde alt yüzdelik, 264 yerine 259 V, ölçülmemiş trafoya "ölçülmedi" etiketi, sarıları ilk ölçüm listesine.

## 6. Yöntemin tarifi — 48 saatte kodlanabilir hali

Makalelerin tam metni kapalı (IEEE ücretli, açık kopyalar 403). Aşağısı proje belgeleri ve özetlerden; tam formül ve katsayılar BULAMADIM.

1. **Kümeleme [Kaynaklı]:** her trafonun 10 dakikalık gerçek gücünden hafta içi, cumartesi ve pazar için ayrı ortalama günlük profil; profil dönemin tepesine bölünerek normalize; mevsim dönemlerine ayrı ("high summer" gibi). Önce hiyerarşik kümeleme, sonra k-means → 10 küme. Küme sayısının seçim ölçütü BULAMADIM. (Ofgem 2013; makale özeti)
   - [Yorum] Bizde: bahar (Mart–Mayıs) öğlenini ayrı dönem al, çünkü güneşi sıkıştıran an o.
2. **Sınıflandırma [Kaynaklı]:** çok sınıflı lojistik regresyon. Projede toplanan sabit veri: trafo kapasitesi, beslenen müşteri tipleri ve sayıları, müşterilerdeki PV sayısı, çıkış fideri sayısı, fider tipi ve uzunluğu (Zhao vd. ISGT 2015 ön baskı — ben de okudum). Müşteri tipleri Elexon'un 8 profil sınıfı.
   - [Yorum] Kıbrıs karşılığı: kVA, Kıb-Tek tarife sınıfı başına abone sayısı (konut, ticari I/II, sanayi I/II, su motoru), bağlı panel sayısı (başvuru listesi), fider sayısı ve uzunluğu.
3. **Ölçekleme [Kaynaklı]:** her şablon için "katkı faktörü", kümeye göre ağırlıklı kısıtlı regresyon; katsayılar ters akış çıkarmayacak ve sıfır yüklü trafoyu işleyecek şekilde sınırlı; 800 trafoda çapraz doğrulama.
   - [Yorum, doğrulanmadı] Kodlanabilir hali: trafo yükü ≈ Σ β(şablon, sınıf) × o sınıftaki abone sayısı, β ≥ 0 → küme başına negatif olmayan en küçük kareler (scipy nnls). Hedef tepe yerine **öğlen (11–14) en düşük yük** olmalı.

**Doğruluk [Kaynaklı]:** ölçülenle karşılaştırmada ~%80; diğer şirketlerin seçtiği 284 örnek trafoda %80–90 (ben de okudum); şablonlar İngiltere trafolarının %82'sine uydu. Metriğin tam tanımı BULAMADIM.

**Öğlen minimumu için şablonu doğrulayan çalışma BULAMADIM.** İngiltere'nin ikinci makalesi yalnız tepe yükü tahmin ediyor. [Yorum] Bu hem risk hem yenilik: "yöntem İngiltere'nin, hedef bizim" — jüriye "öğlen minimumu için kullanan bir çalışma bulamadık" diye söylenmeli, "dünyada ilk" denmemeli.

**Kaba karşılaştırma ölçütü [Kaynaklı, okundu]:** New York'ta fiderlerin %70–80'inde öğlen minimum yük verisi yok; veri yoksa şirketler minimumu tepenin %15–40'ı sayıyor (%15, %25, %30–40). Bizim şablon tahminimiz bu kaba kuralla yan yana gösterilebilir.

## 7. Dünyada benzerleri ve kaç trafo ölçülmeli

| Yer | Ne yapıyor | Doğruluk |
|---|---|---|
| WPD Güney Galler | 824 trafo + 3.600 hat ucu; 2017'den tüm trafolara sabit veriyle şablon | ~%80; başka şirketlerde %80–90 |
| UKPN (İngiltere) | 120 binden fazla trafonun %14'ü izleniyor, makine öğrenmesiyle "efektif %100" görünürlük | şirket beyanı, tanım yok |
| SSEN (İngiltere) | 46 trafo, 242 izlenen ev; fider ölçümüyle | ~35 müşterili fiderde ortalama yüzde hata %27 |
| SAPN (Güney Avustralya) | "temsili şebeke" ile dinamik şablon; 2024 incelemesinde trafoların %97'sinde kategorik yöntem, "kategorik yaklaşımdan kaçının" eleştirisi (arama özeti) | BULAMADIM |
| Brezilya (ANEEL PRODIST) | her tarife döneminde ölçüm kampanyası, abone sınıfına göre tabakalı örnek, tipik eğri hafta içi/cumartesi/pazar | hedef: tabaka başına en çok %20 hata, %95 güven |
| Almanya (BDEW) | 1999 standart profilleri 2025'te yenilendi; panelli ve bataryalı eve ayrı profil (arama özeti) | – |

**Kaç trafo ölçülmeli:**
- [Kaynaklı] WPD %2,6. Torquato vd. 2018 (Brezilya, 50.000 gerçek şebeke): rastgele %1'lik örnek bütünün güneş kapasitesini tahmin etmeye yetiyor (arama özeti).
- [Kaynaklı] Brezilya örneklem formülü: n = (1,96·CV/R)² / [1 + (1,96·CV/R)²/N] (CV değişkenlik katsayısı, R kabul edilen hata ≤ %20, N tabakadaki trafo).
- [Hesap] R = %20 ile 40 trafolu farazi şehirde tabaka başına 7–22 trafo (CV 0,3–0,7); adada ~6.400 trafo varsayımıyla 5 tabaka × 24 ≈ 120 trafo (%1,9). WPD'nin %2,6'sıyla aynı mertebede → "Kıb-Tek 120–170 trafo ölçerse yeter" savunulabilir.
- "Ölçülen trafo arttıkça doğruluk" eğrisi BULAMADIM → farazi şehirde kendimiz çizebiliriz ama kanıt değil, gösterim.

## 8. Zayıflıklar ve jürinin soracakları

**Zayıflıklar [Kaynaklı + Yorum]:**
- Şablonlar eskir: İngiliz şablonları 2012–13 verisi; panel arttıkça öğlen şekli değişir. Brezilya ölçümü her tarife döneminde yeniliyor.
- Kategorik yaklaşım Avustralya'da eleştirildi; akıllı sayaç verisine geçilmesi önerildi (arama özeti).
- Bath'ın aynı 800 trafo çalışmasında hata kırsalda en yüksek, banliyöde en düşük.
- Müşteri–fider eşleme kayıtlarındaki hatalar doğruluğu düşürüyor → Kıb-Tek'te eşleşmenin dijital olup olmadığı en kritik soru.
- İngiliz %80'i klimasız, yoğun panelsiz bir iklimden; Kıbrıs'ta tutup tutmadığı bilinmiyor.
- Faz bilgisi yoksa "kaç panel sığar" sonucu ~6 kat oynuyor (bölüm 5).

**Jüri soruları ve cevap iskeleti [Yorum]:**
- "İngiltere'nin kopyası değil mi?" → Yöntem İngiltere'nin, hedef bizim: öğlen en düşük yük ve hat ucu gerilimi; bunu doğrulayan çalışma bulamadık.
- "Veri nereden?" → Şebeke yapısı Alman açık veri setinden (SimBench), tüketim eğrileri Güney Kıbrıs dağıtım şirketinin 2022 resmi profillerinden, güneş Lefkoşa'nın gerçek verisinden; köy, yurt ve sulama varsayım.
- "Doğruluğunuz ne?" → Gerçek veride İngiltere ~%80, başka şirketlerde %80–90. Farazi şehirdeki sonucumuz yöntemin çalıştığını gösterir, Kıbrıs'taki doğruluğu kanıtlamaz; kanıt için ilkbaharda 10 trafoda kör test.
- "Kıb-Tek bunu neden alsın?" → Bugün 2.670 başvuru bekliyor ve izleme sistemi yok; Güney bağladı, şimdi güneşinin %47'sini kısıyor. 120–170 trafo taşınabilir cihazla ~20 bin € + pens.
- "Hangi abone hangi trafoda, biliyor musunuz?" → Hayır; Kıb-Tek başvuruda abonelik belgesi istiyor, eşleşme onda. Bu bizim uzmana ilk sorumuz.

## 9. Plana girdi — araştırmanın netleştirdiği kararlar [Yorum]

- Farazi şehir: SimBench şebeke ölçüleri + EAC profil sınıfları + Lefkoşa güneşi; mevcut saf Python benzetimi büyütülür (3 trafo 2 saniye → 40 trafo ~30 saniye).
- Şablon hedefi: bahar öğleni en düşük yük; sınıflandırma girdisi Kıb-Tek tarife sınıfları.
- Kaç panel sığar: bölüm 5'teki formül, karamsar/iyimser iki hesap, renk karamsara göre; sonuç ev ev yük akışıyla karşılaştırılarak gösterilir.
- Harita: Streamlit + pydeck 3D sütunlar; internet kesilirse altlıksız yedek.
- Sunumun kanıt cümlesi: İngiltere ~%80 (gerçek veri); farazi şehir yalnız gösterim.
- Açık karar: Esnek Onay katmanı eklensin mi (Muhittin'e de soruldu).

## Kaynaklar

- Ofgem ilerleme raporu, Mayıs 2013: https://www.ofgem.gov.uk/sites/default/files/docs/2013/09/ppr_wpd_lv_templates_may2013.pdf
- Ofgem ödül başvurusu, Mayıs 2015: https://www.ofgem.gov.uk/sites/default/files/docs/2015/05/final_-_sdrc_reward_submission_v1.7_redacted.pdf
- REF 2021 Bath etki vakası: https://results2021.ref.ac.uk/impact/4b604c22-18a1-4c14-a404-37ed28217a21/pdf
- Zhao vd. ISGT 2015 (sabit veri, gerilim dağılımı): https://purehost.bath.ac.uk/ws/files/133401444/Understanding_LV_Network_Voltage_Distribution_Experience_from_UK_Smart_Grid_Demonstration_14_08_2014_2_cg.pdf
- Part I / Part II özetleri: https://api.openalex.org/works/doi:10.1109/TPWRS.2014.2371474 · https://api.openalex.org/works/doi:10.1109/TPWRS.2014.2371477
- EAC Profil Sınıfları (arşiv): bölüm 4'teki adresler; yerel kopya data/raw/eac-profil-siniflari
- SimBench: https://github.com/e2nIEE/simbench · lisans https://simbench.readthedocs.io/en/stable/about/license.html
- IEEE Avrupa AG test fideri (pandapower): https://pandapower.readthedocs.io/en/stable/networks/3phase_grids.html
- ENWL LV Network Solutions: https://www.enwl.co.uk/zero-carbon/smaller-projects/low-carbon-networks-fund/low-voltage-network-solutions/
- İspanya EDP kentsel şebeke: https://data.mendeley.com/datasets/685vgp64sm/1
- İspanya REE profilleri: https://www.ree.es/es/clientes/distribuidor/gestion-medidas-electricas/consulta-perfiles-de-consumo
- Lefkoşa tek ev verisi: https://zenodo.org/records/8348862
- EPRI barındırma kapasitesi, 2016: restservice.epri.com/publicdownload/000000003002005793/0/Product
- Deakin vd. 2019: https://arxiv.org/abs/1902.08780
- Güney Kıbrıs CIRED 2024: https://sps.cut.ac.cy/publication/2024ctherapontos/2024CTherapontos.pdf
- Güney Kıbrıs kısıntı: https://www.pv-magazine.com/2026/01/13/cyprus-solar-curtailment-hits-47-in-2025/ · https://www.pv-magazine.com/2026/06/15/cyprus-curtails-65-of-solar-generation-in-january-may-2026/
- New York minimum gündüz yükü: https://dps.ny.gov/si-cesir-analysis-minimum-daytime-load-application-assumptions-february-2024
- Brezilya PRODIST Modül 2: https://www.light.com.br/Documentos%20Compartilhados/Legislacao-Prodist-Aneel/PRODIST-M%C3%B3dulo2_Revis%C3%A3o7.pdf
- SSEN / Giasemidis vd. 2017: https://arxiv.org/pdf/1612.06833
- UKPN Smart Grid Index: https://dso.ukpowernetworks.co.uk/smart-grid-index
- EA Technology SAPN vakası: https://eatechnology.com/media/skbaej5p/aus-case-study-sapn.pdf
- SAPN AER LV Planning Engine Review 2024: https://aer.gov.au/system/files/2024-02/SAPN%20-%205.7.14%20-%20LV%20Planning%20Engine%20Review%20-%20January%202024%20-%20Public_0.pdf
- SPEN izleme maliyeti (ED1, 2017): ofgem.gov.uk, SPEN IRM belgesi
- NIE Networks bağlantı maliyetleri, Ağustos 2024
- Streamlit pydeck seçim: https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart
