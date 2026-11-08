# Konuşma notu (iskelet)

Anlatan: Volkan. Slayt numaraları [slaytlar.md](slaytlar.md), ekran numaraları [ekranlar.md](ekranlar.md) ile aynı. Akış yük haritası öne (KARAR 10:16): sorun → yük haritası → neden inanılır → panel güvenli uçlar → pilot ve maliyet → jüri. Rakamların etiketi slaytlar.md'de; burada kısaltılır.

## Açılış cümlesi (slayt 1–2)
"Kıb-Tek, evlerin bağlı olduğu mahalle trafolarını göremiyor; bu yüzden çatı güneşi başvuruları bekliyor. Güney bağladı ve şimdi ürettiğinin yarısını atıyor."

## Yük haritası cümleleri (ekran 4, slayt 4–5; ana katman, KARAR 09:43, rakamlar KARAR 10:26 / 10:43)
- "Hangi trafonun dolu olduğunu kaçırmadan, ölçüm cihazını nereye takacağınızı söylüyoruz." — %80'den dolu 12/12 yakalanır; bedeli: 124 uyarının 12'si gerçek, her 10 uyarıdan 1'i [Hesap: sınav şehirleri 41–50 (hiç bakılmamış), üretici 1.5, ölçülmeyen 280 trafo, tepe modeli B-Y2; docs/log/2026-11-01-can-eszamanlilik.md; `dashboard/icerik.json`; gösterim]
- Akşam gerilimi: "'Yeterli' dediğimiz 211 trafonun hiçbiri gerçekte 207 voltun altına inmiyor; altına inen 2 trafonun ikisini de yakalıyoruz." [Hesap: aynı küme; gösterim]
- Model cümlesi (söylenmesi zorunlu, KARAR 10:43): "Tepe modelimiz Kıbrıs evlerinin gerçek sıcaklık duyarlılığını kullanır; deneme şehirlerinde bu yüzden yaklaşık %11 fazla tahmin eder, yani güvenli tarafta; gerçek bahar verisinde hata %15." [farazi: 41–50 hata %11,4 / %23,9, işaretli +%11; gerçek: İspanya Mayıs tepesi %15,4 / %36,1, docs/log/2026-11-01-volkan-yuk-tepe-on.md; eğim: 20 Kıbrıs evi, docs/log/2026-11-01-can-eszamanlilik.md]
- "Harita sıralar ve 'önce bak' listesi verir; yılın tepesi 'ön' etiketli, Kıb-Tek'in tepe kaydı gelince daralır." (ADR-0014, ADR-0018)
- Eski "%5,8", "16/16, 87 uyarı", "233", "gerçekte 3 kat" kullanılmaz.

## Ana cümle (ekran 5, slayt 6'nın başı)
"Kıbrıs'ı ölçemiyoruz; yöntemi ölçebildiğimiz her şeyde kanıtlıyoruz, sonra uyguluyoruz."

## Dürüstlük cümleleri (söylenmesi zorunlu; ROADMAP Faz 5 sınavı)
1. **Kanıt sırası:** "%80 İngiltere'de, gerçek veride. Farazi şehir yalnız gösterim. Kıbrıs'taki doğruluğu pilot söyler."
2. **Farazi şehir üst sınırdır** ([ADR-0008](../decisions/adr-0008-farazi-cesitlilik-saf-tahmin.md) madde 3): "Farazi şehir isabeti gerçek isabetin üst sınırıdır. Gerçek veride, İspanya'da 29 trafoda sınadık: yalnız müşteri sayısıyla ~%25, fatura bilgisiyle ~%10 ortanca hata. Kıbrıs'taki doğruluğu pilot söyler."
3. **Gerilim** (karar masası 17:00, güncelleme 18:46): "Gerilim hesabını İngiltere'de 6 gerçek hatta sınadık: beşinde ölçülen yükselme hesabın güvenli sınırının altında; birinde küçük gördük. Bu yüzden canlıda yeşil önce pilotla sınanır." [Hesap: PR #11 + docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md]
4. **Fatura** (karar masası 17:38): "Gerçek İspanya verisinde yalnız müşteri sayısıyla hata ~%25, fatura girince ~%10." [Hesap: PR #10, İspanya 29 trafo, gerçek veri] (eski farazi 11–20 kıyası %20,6 / %3,8 kullanılmaz; üretici 1.5'te faturasız koşu yok)
5. **Temsil yanlılığı:** "Ölçülen trafolar yereldir; her tipten örnek yoksa model görmediği tipte kendinden emin yanlış tahmin yapar. Tabakalı seçim, ölçülü/ölçülmeyen dağılım karşılaştırması ve düşük güven etiketiyle bunu sınırlıyoruz, tamamen kaldırmıyoruz."
6. **Kalibrasyon** (karar masası 21:15; ekran 5'te ya da burada): "Aralıklarımızı gerçeğe karşı yalnız İspanya'da sınadık (%80 aralığımız %82,1 tuttu); canlıya geçmeden gerçek ölçümle yeniden kalibre edilecek, o zamana kadar bantlar gösterim." [Hesap: Faz 7 kalibrasyonu, İspanya 28 trafo, [kalibrasyon günlüğü](../log/2026-11-01-volkan-faz7-kalibrasyon.md); [ADR-0013](../decisions/adr-0013-veri-dongusu-tuzugu.md)]
7. **Faturanın değeri** (karar masası 22:17, ADR-0016 m. 1): "Öğlen yükünü fatura söyler; biz ne kadar emin olduğumuzu ve panelin sığıp sığmadığını söyleriz."

## Manşet cümlesi (ekran 5, slayt 6, İspanya; karar masası 22:21)
"Kıb-Tek'in zaten elindeki fatura toplamı girince gerçek trafolarda hata %25'ten %10'a iniyor; biz bunun üstüne ne kadar emin olduğumuzu (aralığımız İspanya'da %82,1 tutuyor) ve panelin sığıp sığmadığını söylüyoruz." [Hesap: PR #10 (%25 → %10); %82,1: Faz 7 kalibrasyonu, İspanya 28 trafo, docs/log/2026-11-01-volkan-faz7-kalibrasyon.md]
- "Modelimiz hatayı %25'ten %10'a indirdi" **denmez**: İspanya'da faturalı model basit fatura oranıyla birebir aynı çıktı (abone sınıfı yok); %10 faturanın değeri.

## Kilit cümle (ekran 6, slayt 7)
"Dolu trafoya 'yer var' demek en pahalı hata. Bugünkü %40 kuralı 46 dolu trafonun 24'üne 'yer var' diyor. Bizim 60 yeşilimizin hiçbiri dolu değil." Bedeli hemen arkasından: "Yeşil az ve bu bilerek: ölçülmeyen trafoların çoğunda (%76) emin değiliz; kararı başvuru gelince veriyoruz ya da önce ölçüyoruz. 'Büyük olasılıkla dolu' dediğimiz 22 trafonun 15'i gerçekten dolu; bu uyarı ret değil, 'ölç ya da güçlendir'." [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`]; gösterim

## Pilot ve maliyet cümlesi (ekran 7, slayt 8; karar masası 20:47, KARAR 10:16)
- Ekranda yazan: "Harita için Kıb-Tek'ten yeni veri istemiyoruz: abone sayısı ve fatura toplamı zaten elinde. Pilotta ilk ölçeceğimiz şey trafonun çıkış gerilimi."
- Maliyet: "120–170 trafoyu taşınabilir cihazla ölçmek ~2,2–3,2 milyon TL; her trafoya cihaz takmanın yüzde biri." [Hesap: docs/log/2026-11-01-can-maliyet.md]
- Eski "%27'den %19'a" ve "%4'e" cümleleri (bilginin değeri denemesi, farazi 11–20, eski yanlış kırmızı ölçüsü) kullanılmaz: ADR-0017'den beri kırmızı yok (KARAR 10:16).

## Jüri soruları ve cevap iskeleti (ROADMAP Faz 5: 8 soru, her birine ekipten en az iki kişi)
Kaynak: [araştırma günlüğü](../log/2026-10-31-kapsamli-arastirma.md) bölüm 8, ADR-0005, ADR-0010. Cevaplar iskelet [Yorum]; provada kişi adı yazılır.

| # | Soru | Cevap iskeleti | Cevaplayan |
|---|---|---|---|
| 1 | İngiltere'nin kopyası değil mi? | Yöntem İngiltere'nin, hedef bizim: ilkbahar öğlen en düşük yük ve hat ucu gerilimi; bunu doğrulayan çalışma bulamadık | |
| 2 | Veri nereden? | Tüketim eğrileri Güney Kıbrıs dağıtım şirketinin 2022 resmi profilleri, büyüklükler Kıb-Tek 2023 istatistiği, güneş Lefkoşa'nın gerçek verisi; şebeke ölçüleri Alman açık setinden (SimBench); köy, yurt ve sulama varsayım | |
| 3 | Doğruluğunuz ne? | Güven merdiveni: İspanya gerçek veride faturayla ~%10; İngiltere ~%80; farazi şehir gösterim; Kıbrıs için pilot ve kör test | |
| 4 | Kıb-Tek bunu neden alsın? | Başvurular bekliyor, izleme sistemi yok; Güney bağladı, şimdi kısıyor. Pilot 120–170 trafo, taşınabilir cihazla ~2,2–3,2 milyon TL (~40–57 bin €, işçilik dahil); her trafoya cihaz takmanın ~%1'i [Hesap: docs/log/2026-11-01-can-maliyet.md] | |
| 5 | Hangi abone hangi trafoda, biliyor musunuz? | Hayır; Kıb-Tek başvuruda abonelik belgesi istiyor, eşleşme onda. Uzmana ilk sorumuz | |
| 6 | Model yanlış "yer var" derse? | Yeşil = ilk iki başvuru 40 çekilişin %98'inde sığıyor (güven şartı ADR-0019'la kalktı; güvenlik bantta); deneme şehrinde yanlış yeşil 0/60 [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`]; canlı bütçe yanlış yeşil < %2; emin olmadığımız trafoya önce ölçüm cihazı | |
| 7 | "Yapay zekâ hayır dedi" — kim hesap verir? | Ret yok, triyaj var; son karar Kıb-Tek mühendisinin; itiraz eden gerçek ölçüm ister | |
| 8 | Paneller arttıkça model eskimez mi? | Eskir; ölçüm cihazları her ilkbahar sarılara dolaşır, şablon yenilenir | |
| 9 | Renksiz çok, eşiği gevşetsenize? | "Eşiği gevşetsek dolu trafoya 'yer var' demeye başlarız. 'Büyük olasılıkla dolu' dediğimiz 22 trafonun 15'i gerçekten dolu; o uyarı ret değil, 'ölç ya da güçlendir'. Renksizlerin çoğu ise 'bir sonraki başvuru hattın neresinden gelecek' sorusu; onu haritada değil başvuru anında, evin adresiyle tek tek hesaplarız." [Hesap: 15/22 sınav şehirleri 31–40, üretici 1.5, docs/log/2026-11-01-volkan-panel-guven-kapisi.md; son cümle **sınanmadı**, ADR-0012; slaytta yazılmaz] (KARAR 10:16: eski "%27'den %19'a" kalktı) | |
| 10 | Malta akıllı sayaçla çözdü, siz neden sayaçsız? | "Akıllı sayacı olan Malta bile kapasite haritasında trafo başına düz bir tavan gösteriyor: izin hiçbir merkezde gücün %25'ini geçmiyor; Kıb-Tek'in kuralı %40. Biz her trafoya gerilimle ayrı bakıyoruz." [Hesap: Enemalta kapasite haritası verisi, 1.332 merkez, 31 Ekim 2026; lisans belirsiz, ham veri depoda yok; Enemalta'nın yazdığı kural değil bizim çıkarımımız]. Devamı: "Malta'da da sınırı gerilim ve trafo kademesi koymuş; trafolar boşta 250 volt, Kıb-Tek'le aynı." [Kaynaklı: Micallef & Weissenbacher, Graz 2016, https://www.tugraz.at/fileadmin/user_upload/Events/Eninnov2016/files/lf/Session_B1/LF_Weissenbacher.pdf] (karar masası 20:47) | |
| 11 | Düz kural neden kötü? | "Hawaii düz kuralı kanıt geldikçe tepe yükün %15'inden gündüz en düşük yükün %250'sine çıkardı; ölçülmeyen hattı benzer ölçülen hattan tahmin ediyor, bizim yöntemin emsali." [Kaynaklı: HECO 2014; Sunrun, New York ITWG 2022; adresler [ada ülkeleri günlüğü](../log/2026-10-31-volkan-ada-ulkeleri.md)] (karar masası 20:47) | |
| 12 | Malta gibi iki sayı (yük ve güneş için boş kapasite) neden yok? | "Artık iki sayı var: güneş için yer ve yük için doluluk (yılın tepesi, çoğunlukla yaz akşamı). Yükü geniş bantla ve 'ön' etiketiyle veriyoruz: gerçek veride (İspanya) hata ortanca %15; Kıb-Tek'in tepe kaydı gelince daralır." [gerçek veri: İspanya Mayıs tepesi %15,4 / %36,1, docs/log/2026-11-01-volkan-yuk-tepe-on.md; ADR-0014, ADR-0018] (eski "elimizde yalnız Nisan var" cevabı geçersiz: üretici 1.4'ten beri yaz / kış penceresi var) | |
| 13 | Modeliniz faturadan fazlasını katıyor mu? | "Öğlen yükünde hayır, fatura yeter; katkımız kalibre aralık, güven ve panel kararı: dolu trafoya 'yer var' diyen %40 kuralı 24/46, biz 0." [Hesap: sınav şehirleri 31–40, üretici 1.5; karar masası Mac koşusu (volkan.md KARAR 01:20) ve ADR-0019 ölçümü (docs/log/2026-11-01-volkan-panel-guven-kapisi.md); `dashboard/icerik.json`]; gösterim (karar masası 22:17, 22:21; ADR-0016; eski 22/44 ve 41/73 kullanılmaz) | |

| 14 | Deneme şehrinde eski model daha isabetli değil miydi? | "Eski model deneme şehrinde sıfır sapmalıydı ama gerçek Kıbrıs evlerinin sıcaklık duyarlılığını yarım alıyordu (%3,0 ↔ %6,5 / °C); deneme şehirleri de o düşük eğimle kurulmuştu. Yeni model tepeyi az göstermiyor: ortanca %11 yukarıda, gerçek hiçbir trafoda bandın üstünde değil. Bedeli daha çok uyarı." İki modelin tablosu dashboard'da ("model sürümü" seçimi) [Hesap: volkan.md KARAR 10:43 tablosu, 31–40 ve 41–50; eğim docs/log/2026-11-01-can-eszamanlilik.md] | |

Gozo hattı sunuma ve cevaplara girmez (karar masası 20:47).

## Bekleyenler
- Canlı harita (ekran 4 ve 6, slayt 4–5 ve 7; Faz 4): Civan'ın panel dili düzelince bu nota tıklama cümleleri (sıra BUILD taslağında: sehir-001 T02, T06, T07).
- KTTO raporunun adresi (slayt 1): BULAMADIM.
- Prova süreleri (2 prova, ≤ 7 dk) ve yedekler (PDF, ekran kaydı).
