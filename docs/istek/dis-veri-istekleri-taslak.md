# Dış veri istekleri — taslak (Civan + Claude, 31 Ekim 2026)

Karar masası 21:39 madde 2. **Gönderen Volkan**; ekip göndermez. Metinler İngilizce, gönderilmeye hazır; köşeli parantezleri Volkan doldurur. Kaynak ve gerekçe: [ada veri setleri günlüğü](../log/2026-10-31-civan-ada-veri-setleri.md).

Ortak ilkeler (iki istekte de söz veriyoruz, tutabileceğimiz kadar):
- Ham veri **yayımlanmaz**: depomuz açık, ham veri zaten depoya girmiyor (`data/raw/` git dışı). Yalnız özet rakam ve kaynak atfıyla.
- Kullanım: bir doğrulama testi (modelimizin hesapladığını ölçülene karşı), hackathon sunumu ve sonrası pilot önerisi. Ticari kullanım yok.
- Atıf: yazar ve yayın adıyla, her slaytta ve günlükte.
- Dil [Yorum]: "Northern Cyprus" yerine "the northern part of Cyprus" ve "Turkish Cypriot community" deniyor; Güney Kıbrıslı araştırmacılara yazarken siyasi okuma riskini düşürmek için. Karar Volkan'ın.

---

## 1. Micallef 2015 tezi — Malta Üniversitesi, "Request a copy"

**Kime / nereden:** Malta Üniversitesi açık arşivi (OAR), tez sayfasındaki "Request a copy" formu: https://www.um.edu.mt/library/oar/handle/123456789/6612 (dosya 15MSSE010.pdf, 9,07 MB, "Restricted Access"). Form adı, e-postası ve mesaj ister; yazara ya da kütüphaneye iletilir.

**Ne istiyoruz:** Tezin kendisi. İçinde aradığımız: Gozo'da aşırı gerilim yaşayan dört trafo merkezinin DIgSILENT modeli için kullanılan **hat boyları, kablo tipleri, müşteri sayısı ve trafo gücü / kademe ayarı**; özellikle Micallef & Weissenbacher (Graz 2016) Tablo 3'teki Srug F1 hattı (500 kVA, 106.219 kWh/yıl, 26,72 kWp panel).

**Ne için:** Gozo hattında hesabımızın dış sınaması (ROADMAP "dış sınama adayları"; karar masası 20:47'de bilgi eksik diye koşulmadı). Hat boyu ve kablo gelirse sonuç aralık değil tek tahmin olur.

**Lisans / koşul:** Tez telif yazarın; kopya kişisel araştırma için verilir. Yalnız tablo değerlerini atıfla kullanırız, PDF'i paylaşmayız.

**Mesaj (forma yapıştırılacak):**

> Dear Mr Micallef,
>
> I lead a small team building an open tool that estimates, transformer by transformer, how much rooftop PV a low-voltage network can host when the utility has no monitoring and no smart meters (our case is the northern part of Cyprus). Your 2016 Graz paper with Dr Weissenbacher on the Gozo networks is the closest real-world reference we have found: same 11 kV / 433 V transformers, the same no-load voltage problem.
>
> We would be grateful for a copy of your 2015 M.Sc. dissertation, "High photovoltaic penetration analysis: case study of Gozo high and low voltage networks". We would like to use the feeder data (line lengths, cable types, number of customers, transformer rating and tap setting) for the four Gozo substations, in particular the Srug F1 feeder in Table 3 of the Graz paper, to test our voltage calculation against your results.
>
> We will not redistribute the dissertation or any raw data; we would only cite summary values with full attribution to you and the University of Malta.
>
> Kind regards,
> [Volkan — ad soyad, ekip / kurum, e-posta]

---

## 2. KIOS (Kıbrıs Üniversitesi) + EAC yazarları — AG hat modeli ve tüketici verisi

**Kime:** Kotsonias, Hadjidemetriou, Kyriakides (KIOS Araştırma ve İnovasyon Mükemmeliyet Merkezi, Kıbrıs Üniversitesi) ve Ioannou (EAC). Makalede yayımlanan adresler: kotsonias.andreas@ucy.ac.cy, hadjidemetriou.lenos@ucy.ac.cy (ilk yazışma bu ikisine; Kyriakides ve Ioannou bilgi olarak, Volkan karar verir).

**Kaynak:** "Operation of a Low Voltage Distribution Grid in Cyprus and the Impact of Photovoltaics and Electric Vehicles", IEEE ISGT-Europe 2019, Zenodo 10.5281/zenodo.3561929, CC BY 4.0.

**Ne istiyoruz (öncelik sırasıyla):**
1. Makaledeki AG hattın modeli: her hat parçasının boyu ve kesiti (Şekil 1'deki 74 düğüm), her bağlantı noktasının fazı, trafo gücü ve boşta çıkış gerilimi / kademe ayarı.
2. Simülasyonun gerilim çıktısı (en azından ana hat düğümlerinde yaz iki haftası, faz–nötr ve nötr–toprak), ya da yalnız özet: düğüm başına en yüksek gerilim.
3. Yük verisi: EAC'nin ~60 tüketicilik yarım saatlik bir yıllık kaydı ve panel üretimi. Bu EAC'nin verisi; yalnız anonim, ya da yalnız toplu (ortalama + dağılım), ya da gizlilik sözleşmesiyle olabilir. Olmazsa yalnız 1 ve 2.

**Ne için:** (1) Benzetimimizdeki kablo direnci varsayımı (ABC 70/95, 0,50 / 0,36 Ω/km) ve uç kollardaki ince iletken (16–22 mm²) senaryosu, üretici 1.3 (karar masası 21:16 madde a). (2) Hesabımızı Kıbrıs'ta gerçek bir hat topolojisinde, makalenin sonucuna karşı sınamak. (3) Yük: tek evin tepesinin sınıf ortalamasında ne kadar basık göründüğü.

**Lisans / koşul:** Makale CC BY 4.0; model ve veri ayrı, yazarların / EAC'nin izniyle. Ham veri yayımlanmaz; yalnız özet ve atıf.

**Mesaj (e-posta):**

> Subject: Request: LV feeder model from your ISGT-Europe 2019 Cyprus paper
>
> Dear Dr Hadjidemetriou, dear Mr Kotsonias,
>
> We are a small team working on an open tool that estimates, for each distribution transformer, how much rooftop PV a low-voltage network can host when the utility has no monitoring and no smart meters. We are developing it for the Turkish Cypriot community's network in the northern part of Cyprus, where the rule today is a flat 40% of transformer rating.
>
> Your ISGT-Europe 2019 paper, "Operation of a Low Voltage Distribution Grid in Cyprus and the Impact of Photovoltaics and Electric Vehicles", is the only published description of a real Cypriot LV feeder we have found, and Table I has already given us a better basis for our conductor assumptions. Thank you for making it openly available.
>
> Would you be willing to share the feeder model behind Fig. 1: segment lengths and conductor sizes, the phase of each service point, and the transformer rating and no-load voltage setting? A summary of the simulated node voltages would also help us test our calculation against yours. If the EAC consumer dataset could be shared in any anonymised or aggregated form, we would be glad to follow whatever conditions you or EAC require; if not, the feeder model alone would already be very valuable.
>
> We will not publish any raw data. Results would appear only as summary figures with full credit to you, KIOS and EAC.
>
> Kind regards,
> [Volkan — ad soyad, ekip / kurum, e-posta]

---

Durum: taslak, Volkan'a (volkan.md'de satır). Gönderilince bu dosyaya tarih ve kanal eklenir; cevap gelince günlüğe.
