# 2026-11-08 — Volkan (KARAR): üretici 1.7 — hava verisinin saati ve panelin sıcaklık kaybı

**Etiket: [Hesap] (KTEMO gerçek veri) / gösterim (deneme şehirleri).** Volkan (8 Kasım): "son indirdiğim datalarla modelimizi tekrar eğit." Son indirilen veri (3 Kasım, `hackaton/dis-veri`): KTEMO çatı paneli 5 dk üretim 2018-01-01 – 2026-04-10, PVGIS Lefkoşa 2018–2023, Open-Meteo Lefkoşa 2018–2022 ve 2026 Ocak–Nisan. Önceki bulgular: [KTEMO karşılaştırması](2026-11-03-volkan-ktemo-pv-karsilastirma.md). Dal #43'ün (üretici 1.6) üstünde.

## Hipotez / amaç
3 Kasım karşılaştırması iki hata buldu: (1) Open-Meteo saat sütunu yaz saatsiz sabit UTC+2, model yerel (yaz saatli) sanıyor → Mart sonu – Ekim sonu güneş ve sıcaklık 1 saat erken; (2) panel kaybı sabit 0,82, sıcaklığı görmüyor → yazın açık öğlende fazla, kışın az üretim. İkisi düzeltilirse dünya (deneme şehirleri) ve model gerçek panele yaklaşır.

## Ne değişti
- **`src/pv_hava.py` (yeni):** `om_yerel` (Open-Meteo etiketi → Lefkoşa yerel saati; AB yaz saati kuralı, zoneinfo'suz, Windows'ta da çalışır), `bosluk_doldur` (yaz saatine geçişte boş kalan saat), `panel_carpani` (sıcaklık çarpanı) ve KTEMO ayar betiği (`python3 src/pv_hava.py <ktemo gunluk> <open-meteo klasörü>`).
- **Sıcaklık çarpanı:** 1 + γ × (hücre − T_ref), hücre = hava + 0,03 × ışınım (W/m²). γ = −0,004 / °C (kristal silikon veri sayfası değeri, [Yorum]); T_ref = 50,8 °C = KTEMO 2018–2022 Nisan açık öğle (eğik > 700 W/m², 654 saat) hücre sıcaklığı ortalaması [Hesap]. Böylece Nisan (panel katmanının ayı) eski 0,82 düzeyinde kalır.
- **`src/sehir_uret.py` (üretici 1.7):** ışınım ve sıcaklık yerel saatle okunur; panel üretimi (Nisan ve yaz / kış pencereleri) `panel_isinimi` ile sıcaklıklı; OG öğlen çarpanı da aynı ışınımdan. `ayar.json`'a `panel_sicaklik` ve `hava_saati`.
- **`src/tepe.py`:** hava yerel saatle (ışınım [L−1, L), sıcaklık L); önceden ışınım kışın 1 saat geç, sıcaklık yazın 1 saat erken okunuyordu. Panel için ayın saatlik ışınımı, o saatin sıcaklığı (tepe gününde ± ΔT) ile çarpılır.
- **`src/sahte_kayit.py`:** 1.7 şehirlerinde aynı sıcaklıklı ışınım (yeniden kurma üreticiyle birebir kalsın).
- Değişmeyen: `kac_ev_olasilik.py` öğlen güneşi (Nisan en yüksek saat 998 W/m² × 0,82): yeni çarpan o saatte 0,995 [Hesap], etkisi yok sayıldı. `eszamanlilik.py` (Can'ın) aynı hava klasörünü okuyor; saat kontrolü can.md'de (3 Kasım).
- Hava yılları 2018–2022 üreticiye **eklenmedi**: bayram listesi (`BAYRAMLAR`) yalnız 2023–2025 için yazılı; Ramazan ve Kurban bayramları yıldan yıla kayıyor. Ayrı iş.

## KTEMO gerçek paneliyle ayar ve sınav [Hesap: `src/pv_hava.py`]
Ayar 2018–2022 (etkin güç ve T_ref), sınav 2023–2026 (12.114 gündüz saati; 10 çevrim dışı gün atıldı). Gerçek ÷ formül, açık öğle saatleri:

| Ay | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | Aylar arası yayılım | Günlük hata (ortanca / P90) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Eski (sabit 0,82) | 0,98 | 1,01 | 0,97 | 1,00 | 0,96 | 0,94 | 0,90 | 0,89 | 0,94 | 1,01 | 0,98 | 1,00 | 0,116 | %9,1 / %25,9 |
| 1.7 (sıcaklıklı) | 0,96 | 0,99 | 0,97 | 1,01 | 0,99 | 1,00 | 0,97 | 0,95 | 0,99 | 1,03 | 0,98 | 0,98 | 0,076 | %7,2 / %26,0 |

Yazın fazla tahmin (Temmuz–Ağustos) ~%10 → ~%4; saatlik hata ortancası %17,1 → %17,0 (bulutlu saatler baskın). γ denemesi (−0,004 … −0,007) sınav yıllarına bakılarak yapıldı; seçilen değer önceden belirlenen veri sayfası değeri, aynı zamanda denenenler arasında yayılımı en küçük olan (−0,006 yazı tam düzeltir ama kışı bozar, yayılım 0,098). Ayar ↔ sınav ayrımı bu yüzden γ için kusursuz değil; T_ref ve etkin güç yalnız ayar yıllarından.

## Deneme şehirleri (gösterim)
- **Ayar 1–10, aynı tohumlar, 1.6 ↔ 1.7** (Mac, karar masası 8 Kasım 16:38; aynı `sinav.py` (main) iki kümede; tepe sapması / dolu yakalama karar masasının kVA hesabı):

| | 1.6 | 1.7 |
|---|---|---|
| **Yük haritası:** tepe hatası ortanca / P90 (sinav faz2, net kW) | %8,9 / %21,4 | %9,5 / %21,7 |
| İşaretli sapma ortanca (kVA, ölçülmeyen 280) | +%6,2 | +%7,4 (güvenli yön) |
| %80 bant (faz2) ; gerçek P90 üstü | %97,5 ; 0 | %97,5 ; 0 |
| %80'den dolu yakalanan ; uyarı (P90 ≥ %80) | 19/19 ; 120 | 18/18 ; 120 |
| **Tepe saati ±60 dk isabet ; iki adaydan biri ; dönem** | %46,4 ; %55,4 ; %66,4 | **%55,0 ; %64,6 ; %76,4** |
| Akşam 207 V altı yakalanan ; "yeterli"de yanlış | — | 1/1 ; 223'te 0 |
| **Panel:** yanlış yeşil | 0/64 | 0/64 |
| Dolu trafoya "yer var": %40 kuralı ↔ model | 31/40 ↔ 0 | 30/37 ↔ 0 |
| Kaç ev hatası ortanca (orta) | 2 ev | 3 ev |
| Kaç ev bandı: gerçek P10 altı ; P90 üstü | %2,2 ; %8,2 | %2,2 ; %13,9 |
| Faz1: 259 V üstü trafo ; en düşük gerilim (yıl tepesi) | 39/400 ; 200,9 V | 36/400 ; 201,0 V |

Okuma: tepe saati, sıcaklık doğru saate oturunca belirgin iyileşti (+9 puan). Tepe büyüklüğü hatası ve sapma gürültü düzeyinde arttı, yön güvenli. Panelde yanlış yeşil yine 0; ama yeni dünyada panel biraz az üretiyor ve güneş öğlen penceresinde bir saat geç, gerçek kaç ev artıyor (sıfır olan trafo 40 → 37), model tarafı (`kac_ev_olasilik.py` öğlen güneşi) değişmediği için bant tutucu tarafa kaydı (P90 üstü %8,2 → %13,9). Güvenli yön; düzeltmek ayrı iş (öğlen güneşini saat ve sıcaklıkla hizalamak). Ayar şehirlerine bakılarak yöntem değiştirilmedi → sınav 61–70'e geçilebilir.
- Sınav 61–70: bir kez, 1.7 ile (Can; can.md).

## Karar / sıradaki adım
- PR: #43'ün üstünde; #43 birleşince yalnız 1.7 farkı görünür. Birleşme Volkan'ın sözüyle.
- Bundan önce "1.7" diye anılan BUILD 1 listesi (gerçek faz dağılımı, kapalı döngü düşüm, sızma kontrolü, Nisan → yaz) artık **1.8**.

## Sınav 61–70 — bir kez (Can, 8 Kasım) [Hesap; farazi, gösterim]
Kim / nasıl: Can, Windows, dal `veri/saat-sicaklik-pv` 772fa64; komutlar `docs/istek/can.md` "UYARI! 8 Kasım 16:36" aynen. 61–70 ilk kez üretildi, ayar sonucuna bakılmadan bir kez koşuldu; üretim 10 şehir 37–52 sn. Rakamlar Can'ın KONTROL girdisinden (`docs/istek/volkan.md`, 2d84516). Çıktılar Can'ın makinesinde, depoda yok; Mac teyidi yapılmadı. Bu koşuda B-Y2 yaz eğimi PR'ın bugünkü hâliyle 0,065.

**Panel (faz3)**
- **Yanlış yeşil 0/64 GEÇTİ** (en kötü şehir 0/6). Dolu trafoya "yer var": %40 kuralı 40/57, model 0/57.
- Bayrak isabeti %68,8 (16 bayrak; eşik 0,56) GEÇTİ. Sarı %63,2 UYARI.
- **Kaç ev hatası KALDI:** ortanca karamsar 10, iyimser 4, orta 4 ev (eşik ≤ 2, en az bir sayı; n 225).
- Olasılık kovaları karamsar: 0,5–0,7 kovasında söylenen %57,7 ↔ gerçek %36,2.

**Öğlen yükü (faz2)**
- Arketip %76,8 (eşik %75; en kötü sehir-061 %46,4), şehirler arası 1,13, düşük güven %10,7 (en kötü sehir-061 %35,7) GEÇTİ.
- **Öğlen yük hatası KALDI:** ortanca %12,2, **P90 %30,1** (eşik %30); en kötü sehir-063 %17,3 / %41,4. İspanya satırları komutta yoktu, ölçülmedi.

**Faz1** 5/5 GEÇTİ: en düşük gerilim 201,7 V (sehir-061 T34, yılın tepesi), 207 V altı 2/400 (%0,5); üretim süresi en uzun 51,7 sn.

**Yük haritası** (`tepe.py` özeti, ölçülmeyen 280 trafo)
- Tepe hatası ortanca **%8,2**, P90 **%19,9**; %80 bant %98,2, %95 bant %100 (geniş, güvenli yön).
- Tepe saati ±60 dk %53,2; iki adaydan biri %59,3; dönem %70,4.
- Doluluk hatası ortanca 3,0 / P90 8,3 yüzde puan; bant içinde %98,9. **≥ %80 dolu 14/14 yakalandı** (104 uyarı); ≥ %100 dolu 2/2 (51 uyarı), orta tahmin 1/2.
- **Akşam 207 V:** gerçekte altında 2/280, yakalanan 1/2. "Yeterli" denen 214 trafodan 1'i gerçekte 207 V altında: **sehir-061 T34** (köy, 100 kVA, 3 hat, en uzun 826 m, ABC95): gerçek 201,7 V; tahmin orta 231,7, P10 212,2; 207 V altı olasılığı %7,5. Öbürü (sehir-065 T25, şehir konutu, gerçek 202,8 V) P10 155,3 ile yakalandı.

**Bağlam** (farklı şehir ve üretici sürümleri; yalnız yön için)
- Akşam gerilimi "yeterli"de yanlış: 41–50 (1.5) 211'de 0, 51–60 (1.6) 230'da 0, ayar 1–10 (1.7) 223'te 0 → 61–70'teki T34 yük tarafının ilk yanlış "yeterli"si.
- T34'ün tipi 51–60'taki sehir-055 T36 ile aynı (köy, 100 kVA, ~850 m ABC95): orada üreticinin hat kuralı düşümü ~16 V az görüyordu, dünyanın en düşük gerilimi 199,0 V ([1.6 günlüğü](2026-11-01-volkan-uretici-1.6.md), Ek 11:01). T34'ün sebebi (yük mü, hat mı, dünya mı) incelenmedi [Yorum].
- Öğlen P90: 21–30 %27,0, 31–40 %28,1, 41–50 %30,1 (KALDI, eşik oynatılmadı, KARAR 1 Kasım 10:26), 51–60 (1.6) GEÇTİ, 61–70 %30,1. Eşiğin çevresinde gidip geliyor. 1.6 ↔ 1.7 öğlen farkı ayar 1–10'da ölçülmedi; bu KALDI'nın 1.7'den gelip gelmediği bilinmiyor.
- Kaç ev: ayar 1–10'da 1.6 → 1.7 orta 2 → 3 ev, gerçek P90 üstü %8,2 → %13,9; 61–70'teki KALDI aynı yönde. `kac_ev_olasilik.py` öğlen güneşi `kac_ev.GUNES_KW_KWP` = 1,0 kW/kWp × `PV_DERATE`: saat ve sıcaklık yok; dünya artık `pv_hava.panel_carpani` ve yerel saatli ışınımla üretiyor [Yorum: kod okundu, etkisi ayrı ölçülmedi]. Yön karamsar (model gerçekten az ev söylüyor), yanlış yeşil yok.

**Eşzamanlılık** (Can'ın günlüğü, [2026-11-01-can-eszamanlilik.md](2026-11-01-can-eszamanlilik.md) Ek 8 Kasım, 7270e25): `eszamanlilik.py` Open-Meteo saatini düzeltince Temmuz yaz eğimi 0,065 → 0,058 (P10–P90 0,051–0,068), tasarım tepesi +%2. Bu sınav 0,065 ile.

### Okuma [Yorum]
- En kritik ölçü (panelde yanlış yeşil) 0; yük haritasının tepe hatası ve dolu yakalama önceki sınav şehirleriyle aynı düzeyde ya da iyi.
- İki KALDI'dan kaç ev yönü bilinen ve güvenli (karamsar); öğlen P90 eşiğin 0,1 puan üstünde, 41–50'de de aynıydı. İkisi de bu sınavda yanlış yeşil üretmedi.
- T34 güvensiz yönde tek kaçırma (1/214, %0,5); tipi uzun köy hattı.

### Karar / sıradaki
- Bloklama ve birleştirme Volkan'da; birleşme yalnız açık "birleştir" sözüyle. 61–70 artık görülmüş: bundan sonraki yöntem değişikliğinin sınavı 71–80'de bir kez.
- #49 birleşince: `tepe.py` B-Y2 sabiti 0,065 → 0,058 (BUILD 1); `eszamanlilik.py` saat okuması `pv_hava.om_yerel` ile (Can).
- Ayrı iş (BUILD 2): `kac_ev_olasilik.py` öğlen güneşini dünyanın saat ve sıcaklık hesabıyla hizalamak; ayar 1–10, sınav 71–80. Sırası (#49'dan önce mi sonra mı) Volkan'a soruldu.
- Ayrı iş: T34 tipi (uzun köy hattı) akşam gerilimi kaçırmasının sebebi.

## Ek (8 Kasım, BUILD 2 — panel): kaç ev öğlen güneşini saat ve sıcaklıkla hizalamak denendi, olumsuz
Volkan: "Önce düzelt, sonra birleştiririz." Hipotez: 61–70'teki kaç ev KALDI'sı, `kac_ev_olasilik.py`'nin öğlen güneşini dünyanın yeni saat ve sıcaklık hesabıyla hizalamamasından. **Sonuç: değil.** Kod birleşmez; dal `panel/oglen-gunes` (abdd632) kalır, PR açılmadı.

**Ne denendi** (dal `panel/oglen-gunes`, #49'un üstünde): eskiden tam güneş (1 kW/kWp × 0,82) öğlenin en düşük yüküyle aynı anda sayılıyordu. Denemede her gündüz adımında güneş = Nisan açık gün zarfı (`pv_hava.gunes_zarfi`: Open-Meteo Lefkoşa 2018–2022 Nisan günleri, yerel saat, sıcaklıklı, her 5 dakikada günlerin en yükseği; dünyanın hava yılları 2023–2025 kullanılmadı), yük = çekilen öğlen en düşük yük × trafonun arketip biçimi (`arketipler.csv`, öğlenin en düşüğüne bölünmüş, iş günü ve tatilin küçüğü). Her çözümde iki an: toplam net vermenin en büyük olduğu adım ve güneşin tepesi; kötüsü sayılır. Çekilişler aynı. Eski kural (`--eski-gunes`) ayar 1–10'un 10/10 şehrinde `kac_ev.csv`'yi bayt bayt aynı verdi.

**Ayar 1–10** (üretici 1.7 şehirleri, karar masasının 16:38 klasörü kopyası; Mac; `sinav.py faz3 --aralik 1-10`) [Hesap; farazi, gösterim]:

| | Eski kural | Saat ve sıcaklıkla hizalı |
|---|---|---|
| Yanlış yeşil | 0/64 | 0/64 |
| Kaç ev hatası karamsar / iyimser / orta | 9 / 2 / 3 ev | 9 / 2 / 3 ev |
| Kaç ev bandı: gerçek P10 altı ; P90 üstü | %2,2 ; %13,9 | %2,2 ; **%18,2** |
| Renk yeşil / sarı / kırmızı | 64 / 238 / 52 | 64 / 237 / 53 |

**Neden işe yaramadı** [Hesap: ayar 1–10, `yuk_5dk.csv`; scratchpad betikleri]:
- Gerçek havanın Nisan açık gün tepesi zaten ~1: 2018–2022 zarfı 12:30'da **1,011** kW/kWp (11:00'de 0,901, 14:00'te 0,959); dünyanın yılları 2023–2025'in zarfı 0,999. Eski 1,0 doğruymuş; hizalı zarf onu %1 artırıyor.
- Modelin kendi yük biçimleri (arketip) öğlenin en düşüğünü güneşin tepesine yakın gösteriyor: seçilen an ortanca 12:30, o anda biçim çarpanı ~1,0–1,02. Yani modelin bildiğiyle "en düşük yük güneşin tepesinde değil" denemiyor.
- Dünyada ise iki uç aynı anda gelmiyor: 14 günlük Nisan penceresinde güneş tepesi ortanca 0,987 (P10 0,967), 12:30'da; öğlenin en düşük yükü çoğu trafoda pencerenin başında (ortanca 11:15), o anda güneş ortanca 0,87; güneş tepesindeki yük öğlen en düşüğünün ortanca 1,17 katı. Öğlenin en düşüğü 14 gün × 36 adımın en küçüğü (tek bir an); güneşin tepesindeki yük sıradan.
- Sonuç: dünyanın gün boyu en büyük net vermesi, eski kuralın varsaydığından panel gücünün ortanca %3,7'si kadar az (panel 4 katına çıkmış hâlde; yeni kural %4,4) [Hesap].

**Duyarlılık (yalnız bilgi, benimsenmedi)**: modelin güneşi ×0,95 → kaç ev 9 / 3 / **2** (orta GEÇER), P10 altı %3,0, P90 üstü %2,2, yanlış yeşil 0/70 (yeşil 70); ×0,90 → 8 / 4 / 2, %4,3 / %1,3, 0/79. Bant güneşe çok duyarlı: %5 güneş, P90 üstü payını 13,9'dan 2,2'ye indiriyor.

### Okuma [Yorum]
- Kaç ev KALDI'sı saat ve sıcaklık hizasızlığından değil, modelin bilerek koyduğu çift uçtan: "en parlak an ile en düşük yük aynı anda". Dünyanın cevabı tek bir yılın iki Nisan haftası; gerçekte trafo yılın her gününde tutmalı, bu yüzden iki haftadan katı olmak güvenli yön.
- Güneşi %5 kısmak hatayı kapatıyor ama bu, modeli farazi dünyaya uydurmak olur (ADR-0009: aralıklar üreticiden değil, gerçek veriden). Gerekçe ancak gerçek ölçümden gelir: düşük yük ile güneş tepesinin gerçek trafolarda ne kadar çakıştığı (pilot ölçümü ya da açık trafo verisi).
- 61–70'te iyimser 4 ev, 1–10'da 2 ev: aynı yön, sınav şehirlerinde biraz daha geniş.

### Karar / sıradaki
- Kaç ev kodu değişmiyor; 71–80 sınavı gerekmiyor (yöntem değişmedi).
- #49'un kaç ev KALDI'sı bilinen ve güvenli yönde; birleştirme Volkan'ın sözüyle.
- Ayrı iş (pilot): gerçek trafoda öğlen en düşük yük ile güneş tepesinin çakışması; çıkarsa modelin güneşi o ölçümle.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
