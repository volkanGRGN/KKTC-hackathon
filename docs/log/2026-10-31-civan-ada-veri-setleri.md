# 2026-10-31 — Civan (+ Claude): eksik verilerimize uyarlanabilir ada veri setleri

## Hipotez / amaç
Veri sözlüğündeki BULAMADIM ve "Açık eksikler" satırları için başka adalarda (ve Akdeniz'de) açık veri var mı? Volkan'ın [ada ülkeleri günlüğü](2026-10-31-volkan-ada-ulkeleri.md) yöntem ve kurala baktı; bu günlük **veri setine** bakar. Karar masası 20:47 "bu gece yeni araştırma yok" dedi: buradaki hiçbir şey bu geceki rakamları değiştirmez; pilot ve üretici 1.3 için.

Hedeflenen eksikler:
1. Kıb-Tek kablo / iletken dirençleri (şartname BULAMADIM; benzetim ABC 70/95 r 0,50 / 0,36 Ω/km varsayımı).
2. Trafo başına hat boyu ve abone sayısı (Kuzey trafo sayısı ~6.400 vekil, [Hesap]).
3. Faz dağılımı ve dengesizlik.
4. Tek evin 5 dk eğrisi (EAC sınıf ortalaması 30 dk, tepeyi basık gösterir).
5. Bulut geçişi (Open-Meteo saatlik).
6. Ada AG şebekesinde ölçülmüş gerilim (yeşil bütçesi gerçek veride doğrulanmadı).

## Yaptıklarım
- Web taraması: Kıbrıs (Güney, Kuzey), Malta / Gozo, Korsika / Réunion, Girit ve Yunan adaları, Kanarya / Balear, Madeira, Bornholm, İrlanda, Wight, Hawaii.
- İki açık kaynak indirildi (depo dışında, scratchpad): Korsika EDF iki tablo, Kıbrıs Üniversitesi makalesi. Rakamlar kaynağında okundu.

## Sonuç

### + Kıbrıs'ta gerçek bir AG hattı: iletken dirençleri ve topoloji (eksik 1, 3)
[Kaynaklı: Kotsonias, Hadjidemetriou, Kyriakides (KIOS, Kıbrıs Üniversitesi), Ioannou (EAC), "Operation of a Low Voltage Distribution Grid in Cyprus and the Impact of Photovoltaics and Electric Vehicles", IEEE ISGT-Europe 2019, Zenodo 10.5281/zenodo.3561929, CC BY 4.0; PDF SHA-256 `cdfbe594…be5a0a`, 1.436.248 bayt, indirildi 31 Ekim 2026]
- "Typical" Kıbrıs AG hattı (Güney, banliyö): 4 telli, radyal, nötr **yalnız trafoda** topraklı; 49 bağlantı noktası, 61 tüketici (52 konut, 9 ticari), çoğu tek faz; 3 panel (2,5 / 7,35 / 4,05 kWp). Trafo kVA'sı ve hat boyları makalede yok.
- Tablo I, iletkenler (Rac, Ω/km; taşıma A):

| İletken | Rac (Ω/km) | A | Bizim varsayım |
|---|---|---|---|
| 100 mm² havai | 0,2702 | 271 | ABC95 0,36 |
| 50 mm² havai | 0,5419 | 181 | ABC70 0,50 |
| 22 mm² havai | 1,2271 | 155 | — |
| 16 mm² havai | 1,9102 | 155 | — |
| 185/90 mm² yeraltı | 0,1432 | 320 | — |

- Okuma [Yorum]: ana hatta (100 mm²) bizim ABC95 varsayımı ~%33 daha dirençli → karamsar yönde. Uç kollarda 16–22 mm² var; bizim benzetimde bu kadar ince kol yok → hat ucunda gerilim yükselmesini **az** gösteriyor olabiliriz. İletken malzemesi yazmıyor; Kıb-Tek değil EAC.
- Nötr: yaz iki haftasında ana hat düğümlerinde nötr gerilimi ortalama ~5–10 V, tepe ~23 V (Şekil 7, grafikten okunan). Dengesizlik yüzünden faz–nötr gerilimi, faz–toprak içindeyken bile 253 V'u aşıyor. Bizim benzetimde nötr 0,69 Ω/km var; ölçüsü bu makaleyle kıyaslanabilir.
- Yük verisi: EAC'nin "60'tan fazla" tüketicinin bir yıllık yarım saatlik akıllı sayaç kaydı ve panel üretimi [Yorum: bizim EAC profil sınıflarındaki 68 ev ile aynı örnek olabilir; doğrulanmadı]. Veri yayımlanmamış; yazarlardan istenebilir.

### + Korsika: trafo başına hat boyu ve abone, Kuzey vekiline bağımsız sağlama (eksik 2)
[Kaynaklı: EDF SEI Corse açık veri, opendata-corse.edf.fr, Licence Ouverte 2.0; `lignes-et-postes-electriques-corse` (SHA-256 `239bdff0…36923d5e`, 689 bayt) ve `consommation-annuelle-par-commune-corse` (SHA-256 `626c02ff…112be5a0a`, 539.724 bayt); indirildi 31 Ekim 2026]
- 2024: 8.144 OG/AG trafo merkezi, 5.930 km AG hat; 267.925 teslim noktası (konut 221.310).
- [Hesap] Trafo başına AG hat 0,73 km (Güney Kıbrıs 1,02); trafo başına teslim noktası 32,9 (Güney 34,4); konut başına yıllık 4,26 MWh.
- [Hesap] Kuzey'in 219.931 tüketicisi Korsika oranıyla ~6.690 trafo, Güney oranıyla ~6.390. Bugünkü ~6.400 vekili yalnız Güney'den türetilmişti; Korsika ikinci, bağımsız bir ada sağlaması verir: **~6.400–6.700**.
- Aynı portalda: aylık PV kesinti saatleri (`deconnexions-des-installations-photovoltaiques-corse`), saatlik üretim. AG hat havai / yeraltı ayrımı ve trafo başına dağılım yok (yalnız ada toplamı).

### ? Tek evin yüksek çözünürlüklü eğrisi (eksik 4)
- **Plegma** (Yunanistan, ada değil, Akdeniz): 13 ev, 10 sn, 1 yıl (Temmuz 2022'den), klima ve elektrikli termosifon dahil, iç/dış sıcaklık; Strathclyde deposu, DOI 10.1038/s41597-024-03208-0 [Kaynaklı: Scientific Data 2024; lisans ve dosya boyu açılıp bakılmadı]. Kullanım: EAC sınıf ortalamasının tek ev tepesini ne kadar basık gösterdiğini ölçmek (Can'ın %16 bulgusu).
- **İrlanda CER** (ada): 5.000+ konut, 30 dk, 2009–2010; ISSDA başvuru formu ister, yalnız AEA ve yeterlilik kararlı ülkelere [Kaynaklı: ucd.ie/issda]. 30 dk bizim sınıflardan ince değil; düşük öncelik.
- **Portekiz 50 ev + PV** (Zenodo 10854881, CC BY 4.0, 145 MB xlsx): yer ve çözünürlük sayfada yok; Madeira değil gibi [Yorum].
- Madeira **SustData** (50 ev, 1 dk): indirme adresi BULAMADIM.

### ? Bulut geçişi (eksik 5)
- **NREL Oahu ışınım ızgarası** (Hawaii): 17 istasyon, 1 sn, 1 yıl, ~1 km ızgara; DOI 10.7799/1052451, CC BY [Kaynaklı: data.nrel.gov/submissions/11]. Kullanım: saatlik Open-Meteo'nun gizlediği 1–5 dk dalgalanmanın büyüklüğü; tropik iklim, Kıbrıs değil.

### − Ada AG şebekesinde açık gerilim ölçüsü (eksik 6): BULAMADIM
Arama izi:
- Gozo: Micallef 2015 tezi (Malta Üniv. OAR 123456789/6612, dört merkez, DIgSILENT) **kısıtlı, "Request a copy"**; Gabdullin 2018 ve Costea 2024 kısıtlı; MCAST Energies 2022 (Zenodo 6800833) yalnız makale, 7 fiderli Malta AG ağı.
- Kıbrıs: KIOS–EAC gerçek zamanlı AG izleme projesi var, verisi yayımlanmamış; FOSS / PHAETHON PV verisi açık değil.
- Yunan adaları: Kythnos ölçümleri 1990'lar, dosya yok; DEDDIE adaya göre PV payı yalnız Girit 2015.
- Hawaii: devre bazında barındırma kapasitesi dosyası bulunamadı (yalnız EV aracı, 2023).
- Bornholm EcoGrid: 5 dk ölçüm var, açık veri bulunamadı.
- Wight (SSEN "Smart Meter LV Feeder Usage"): fider bazında yarım saatlik toplam tüketim, en az 5 sayaç; gerilim yok; erişim ve lisans çelişkili (portalda "No License", aynada CC BY 4.0).
- Kuzey Kıbrıs: Atikol vd. 1999 (Energy), anketten saatlik konut eğrisi; kapalı erişim, ısıtma dönemi.

## Karar / sıradaki adım
- Karar masasına (volkan.md UYARI 21:20): Kotsonias iletken tablosu ve ince uç kolları (benzetim kablo varsayımı, uzmana soru 3), Korsika sağlaması (trafo sayısı vekili), pilot için iki veri isteği (KIOS yazarları; Micallef tezi kopya isteği → Gozo dış sınaması).
- Veri sözlüğü ve KAYNAK.txt satırı Civan'ın dosyası değil; karar masası kime vereceğini seçer. Ham dosyalar depoya girmez.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
