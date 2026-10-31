# Konuşma notu (iskelet)

Anlatan: Volkan. Slayt numaraları [slaytlar.md](slaytlar.md) ile aynı. Rakamların etiketi orada; burada tekrar edilmez.

## Açılış cümlesi (slayt 1–2)
"Kıb-Tek, evlerin bağlı olduğu mahalle trafolarını göremiyor; bu yüzden çatı güneşi başvuruları bekliyor. Güney bağladı ve şimdi ürettiğinin yarısını atıyor."

## Ana cümle (slayt 5'ten önce)
"Kıbrıs'ı ölçemiyoruz; yöntemi ölçebildiğimiz her şeyde kanıtlıyoruz, sonra uyguluyoruz."

## Dürüstlük cümleleri (söylenmesi zorunlu; ROADMAP Faz 5 sınavı)
1. **Kanıt sırası:** "%80 İngiltere'de, gerçek veride. Farazi şehir yalnız gösterim. Kıbrıs'taki doğruluğu pilot söyler."
2. **Farazi şehir üst sınırdır** ([ADR-0008](../decisions/adr-0008-farazi-cesitlilik-saf-tahmin.md) madde 3): "Farazi şehir isabeti gerçek isabetin üst sınırıdır. Gerçek veride, İspanya'da 29 trafoda sınadık: yalnız müşteri sayısıyla ~%25, fatura bilgisiyle ~%10 ortanca hata. Kıbrıs'taki doğruluğu pilot söyler."
3. **Gerilim** (karar masası 17:00, güncelleme 18:46): "Gerilim hesabını İngiltere'de 6 gerçek hatta sınadık: beşinde ölçülen yükselme hesabın güvenli sınırının altında; birinde küçük gördük. Bu yüzden canlıda yeşil önce pilotla sınanır." [Hesap: PR #11 + docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md]
4. **Fatura** (karar masası 17:38): "Fatura olmadan model ortalama trafoda basit hesaptan pek iyi değil; fatura girince hata dörtte bire iniyor. İspanya'da da aynı: %25 → %10." [Hesap: farazi 11–20 faturasız %20,6, faturalı %3,8 (gösterim); İspanya PR #10]
5. **Temsil yanlılığı:** "Ölçülen trafolar yereldir; her tipten örnek yoksa model görmediği tipte kendinden emin yanlış tahmin yapar. Tabakalı seçim, ölçülü/ölçülmeyen dağılım karşılaştırması ve düşük güven etiketiyle bunu sınırlıyoruz, tamamen kaldırmıyoruz."

## Kilit cümle (ekran 5, slayt 10)
"Dolu trafoya 'yer var' demek en pahalı hata. Bugünkü %40 kuralı 73 dolu trafonun 41'ine 'yer var' diyor. Bizim 87 yeşilimizin hiçbiri dolu değil." Bedeli hemen arkasından: "Yeşil %25, sarı %62; bu bilerek: konut trafolarında ölçmeden evet demiyoruz. Kırmızıların %27'sinde gerçekte yer var; kırmızı ret değil, 'ölç ya da güçlendir'." [Hesap: sınav şehirleri 11–20, karar masası koşumu (19:51); gösterim]

## Pilot cümlesi (ekran 6, slayt 8; karar masası 20:47)
- Ekranda yazan: "Harita için Kıb-Tek'ten yeni veri istemiyoruz: abone sayısı ve fatura toplamı zaten elinde. Pilotta ilk ölçeceğimiz şey trafonun çıkış gerilimi; o tek ölçüm 'dolu' dediğimiz trafolardaki yanılmayı %27'den %19'a indirir."
- Yalnız konuşmada (slaytta yazılmaz): "Kıb-Tek'in kayıtlarında panelli abonenin adresi ve fazı da varsa %4'e."
- İkisinin etiketi: [Hesap: bilginin değeri denemesi, farazi şehir 11–20, kusursuz bilgi üst sınırı; docs/log/2026-10-31-volkan-faz3.md]

## Jüri soruları ve cevap iskeleti (ROADMAP Faz 5: 8 soru, her birine ekipten en az iki kişi)
Kaynak: [araştırma günlüğü](../log/2026-10-31-kapsamli-arastirma.md) bölüm 8, ADR-0005, ADR-0010. Cevaplar iskelet [Yorum]; provada kişi adı yazılır.

| # | Soru | Cevap iskeleti | Cevaplayan |
|---|---|---|---|
| 1 | İngiltere'nin kopyası değil mi? | Yöntem İngiltere'nin, hedef bizim: ilkbahar öğlen en düşük yük ve hat ucu gerilimi; bunu doğrulayan çalışma bulamadık | |
| 2 | Veri nereden? | Tüketim eğrileri Güney Kıbrıs dağıtım şirketinin 2022 resmi profilleri, büyüklükler Kıb-Tek 2023 istatistiği, güneş Lefkoşa'nın gerçek verisi; şebeke ölçüleri Alman açık setinden (SimBench); köy, yurt ve sulama varsayım | |
| 3 | Doğruluğunuz ne? | Güven merdiveni: İspanya gerçek veride faturayla ~%10; İngiltere ~%80; farazi şehir gösterim; Kıbrıs için pilot ve kör test | |
| 4 | Kıb-Tek bunu neden alsın? | Başvurular bekliyor, izleme sistemi yok; Güney bağladı, şimdi kısıyor. Pilot 120–170 trafo, taşınabilir cihazla ~20 bin € + pens | |
| 5 | Hangi abone hangi trafoda, biliyor musunuz? | Hayır; Kıb-Tek başvuruda abonelik belgesi istiyor, eşleşme onda. Uzmana ilk sorumuz | |
| 6 | Model yanlış "yer var" derse? | Yeşil yalnız karamsar senaryo marjla geçiyor ve güven yüksekse; canlı bütçe yanlış yeşil < %2; sarılara ölçüm cihazı | |
| 7 | "Yapay zekâ hayır dedi" — kim hesap verir? | Ret yok, triyaj var; son karar Kıb-Tek mühendisinin; itiraz eden gerçek ölçüm ister | |
| 8 | Paneller arttıkça model eskimez mi? | Eskir; ölçüm cihazları her ilkbahar sarılara dolaşır, şablon yenilenir | |
| 9 | Sarı çok, eşiği gevşetsenize? | "Eşiği gevşetsek dolu trafoya 'yer var' demeye başlarız. Ölçüm kırmızıdaki yanılmayı düzeltir: trafonun çıkış gerilimi bilinince yanlış kırmızı %27'den %19'a iner. Sarının çoğu ise 'bir sonraki başvuru hattın neresinden gelecek' sorusu; onu haritada değil başvuru anında, evin adresiyle tek tek hesaplarız." [Hesap: bilginin değeri denemesi, farazi 11–20, kusursuz bilgi üst sınırı; son cümle **sınanmadı**, ADR-0012; slaytta yazılmaz] (karar masası 20:47; eski "sarıyı azaltan şey ölçüm" cümlesi kullanılmaz) | |
| 10 | Malta akıllı sayaçla çözdü, siz neden sayaçsız? | "Akıllı sayacı olan Malta bile kapasite haritasında trafo başına düz bir tavan gösteriyor: izin hiçbir merkezde gücün %25'ini geçmiyor; Kıb-Tek'in kuralı %40. Biz her trafoya gerilimle ayrı bakıyoruz." [Hesap: Enemalta kapasite haritası verisi, 1.332 merkez, 31 Ekim 2026; lisans belirsiz, ham veri depoda yok; Enemalta'nın yazdığı kural değil bizim çıkarımımız]. Devamı: "Malta'da da sınırı gerilim ve trafo kademesi koymuş; trafolar boşta 250 volt, Kıb-Tek'le aynı." [Kaynaklı: Micallef & Weissenbacher, Graz 2016, https://www.tugraz.at/fileadmin/user_upload/Events/Eninnov2016/files/lf/Session_B1/LF_Weissenbacher.pdf] (karar masası 20:47) | |
| 11 | Düz kural neden kötü? | "Hawaii düz kuralı kanıt geldikçe tepe yükün %15'inden gündüz en düşük yükün %250'sine çıkardı; ölçülmeyen hattı benzer ölçülen hattan tahmin ediyor, bizim yöntemin emsali." [Kaynaklı: HECO 2014; Sunrun, New York ITWG 2022; adresler [ada ülkeleri günlüğü](../log/2026-10-31-volkan-ada-ulkeleri.md)] (karar masası 20:47) | |

Gozo hattı sunuma ve cevaplara girmez (karar masası 20:47).

## Bekleyenler
- Slayt 9 canlı harita (Faz 4): Civan'ın panel dili düzelince bu nota tıklama cümleleri (sıra BUILD taslağında: sehir-001 T02, T06, T07).
- KTTO raporunun adresi (slayt 1): BULAMADIM.
- Prova süreleri (2 prova, ≤ 7 dk) ve yedekler (PDF, ekran kaydı).
