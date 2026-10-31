# 2026-11-01 — Volkan (+ Claude, BUILD): Faz 7 — kalibrasyon gerçeğe karşı, model tarafı

Tüzük: geçerli ([docs/tuzuk.md](../tuzuk.md)). Kart: [volkan-faz7-kalibrasyon](../gorev/volkan-faz7-kalibrasyon.md). Karar: karar masası 21:32 (31 Ekim). Dal `kalibrasyon/faz7`, PR. Yazıldığı saat 31 Ekim 21:40–22:00; dosya adı karardaki gibi 1 Kasım.

## Hipotez / amaç
Muhittin (cevap 3): "kalibrasyon gerçeğe karşı; %80 → %57 düzeltilmeden bant yayınlanmaz." Bilginin değeri denemesinde kusursuz bilgide bile bant kapsaması %80'den %57'ye düştü: hesap, şehir üreticisinin dünyasına göre ayarlı ve gerçek dünyaya göre fazla emin. Hipotez: iki gerçek artık kaynağı (yük için İspanya, gerilim için İngiltere) bandı genişletmeyi söyler; yanlış yeşil 0 kalır, yeşil azalır.

## Veri partileri (tüzük §2)
| Parti | Kaynak | Kapsam | Bilinen yanlılık | Kullanım |
|---|---|---|---|---|
| P1-edp-2018 | EDP Oviedo 2018, Mendeley 685vgp64sm, CC BY ([KAYNAK](../../data/raw/edp-oviedo/KAYNAK.txt)) | 29 trafo, Mayıs 2018; `edp_test.py` faturalı (c) koşusu: 3 ölçülü sayısı × 2 seçim × 20 tekrar, 2.280 bir-dışarıda tahmin | İspanya kenti, klima yok; PR #10'dan beri birçok kez görüldü | k_yük **29 trafonun tamamından** (karar). Dokunulmamış payı yok; kapsama iç örnek + **k'si o trafo dışarıda bulunmuş** bir-dışarıda |
| P2-ukpn-2014 | UKPN, Ofgem 2015 kapanış raporu, CC BY ([KAYNAK](../../data/raw/ukpn-pv-dogrulama/KAYNAK.txt)) | 6 hat ucu ev, yaz 2014, 1 dk; `ukpn_olasilik.py` faz bilinmeyen, hat boyu ±0,47, site başına 60 çekiliş | İngiltere, 6 hat az, gerilim baradan eve | s (μ, σ) **6 hattın tamamından**; kapsama iç örnek + bir-dışarıda (μ, σ diğer 5 hattan) |

Tüzük madde 1–2 gereği: iki kaynağın da dokunulmamış payı kalmıyor. Sonuç **"kalibre edildi"**, "iyileşti" değil. Pilotun doğrulama payı dokunulmaz.

Sürümler: v1 = etiket `sunum-v1` (main 0db616e); v2 = dal `kalibrasyon/faz7`. Üretici 1.2, şehirler aynı (BUILD klasörü, 16:57; 11–20'de karar masası koşumuyla bir trafo farkı, Faz 3 günlüğü). Tohumlar değişmedi; s ayrı bir akıştan çekildi (`sapma-<şehir>-<trafo>`), diğer çekilişler v1 ile aynı.

## Yaptıklarım
- **B1** `src/kalibrasyon.py` (saf Python):
  - birim artık u = ln(gerçek ÷ tahmin) ÷ o taraftaki yarım bant;
  - k = |u|'nun %80 yüzdeliği; kapsama eğrisi (%50 / 80 / 90 / 95; iki parçalı normal [Yorum]); PIT; bir-dışarıda k;
  - model-sapma moment tahmini: δ = −ortalama ln(model ÷ ölçülen), μ = ortalama δ, σ² = var(δ) − iç varyans ortalaması.
  - Deneme (`--deneme`): kalibre bantta k 1,012, kapsama %79,5; yayılım × 1,5'te k 1,497 [Hesap].
- **B2** `src/sablon.py`: `K_YUK = 1,475`; bant log ölçekte k ile genişler (güven sınıfları ve tahmin değişmez); `sablon_ozet.json`'a `kalibrasyon` kaydı. Sözleşme değişmedi.
- **B3** `src/kac_ev_olasilik.py`: çekiliş başına s = exp(N(0,172; 0,414)), hat empedanslarını (zs, zn) çarpar; trafo empedansına dokunmaz (İngiltere ölçümü baradan eve). `src/ukpn_olasilik.py`'ye `CEKILIS_JSON` (çekilişleri dosyaya yazar, varsayılan kapalı).
- Seçim yalnız gerçek veriyle yapıldı: k ve (μ, σ) farazi şehir koşulmadan önce sabitlendi; farazi rakamlar sonra ölçüldü.

## Sonuç

### + İspanya: yük bandı kalibre
| Nominal bant | Önce | Sonra, iç örnek | Sonra, bir-dışarıda |
|---|---|---|---|
| %50 | %46,3 | %58,5 | — |
| %80 | **%65,7** | %80,0 | **%79,1** |
| %90 | %74,8 | %87,1 | — |
| %95 | %81,3 | %90,3 | — |

- k_yük = 1,475; bir-dışarıda k aralığı 1,38–1,50 [Hesap: `kalibrasyon.py ispanya`].
- %80 bant İspanya'da gerçeğin üçte ikisini kapsıyordu; şimdi %79.

### + İngiltere: gerilim, 6 hatta P98 kapsaması 5/6 → 6/6
| Hat | δ (ln ölçülen ÷ model) | İç yayılım (sd) | P98 önce | P98 sonra | Bir-dışarıda kapsar |
|---|---|---|---|---|---|
| Alverston Close | −0,04 | 0,30 | kapsar (1,84) | kapsar (3,71) | evet |
| Bancroft Close | **+0,78** | 0,31 | **kapsamaz (0,78)** | kapsar (1,54) | evet |
| Forest Road | +0,03 | 0,32 | kapsar (1,66) | kapsar (3,17) | evet |
| Maple Drive East | −0,71 | 0,28 | kapsar (3,15) | kapsar (6,57) | evet |
| Suffolk Road | +0,67 | 0,49 | kapsar (1,54) | kapsar (2,46) | evet |
| YMCA | +0,30 | 0,38 | kapsar (1,45) | kapsar (2,68) | evet |

- μ = 0,172 (model yükselmeyi ortalama ~%19 küçük görüyor), σ = 0,414 [Hesap: `kalibrasyon.py ingiltere`].
- 6/6 için gereken en küçük σ 0,12 (μ sabit). Aralık σ 0,12–0,41; seçilen moment tahmini. **"6 hatla ayarlandı, pilotta yeniden."**

### + Farazi şehir: yanlış yeşil kapısı tutuyor, kaç ev artık iyimser değil
Geliştirme 1–10 (354 trafo, 56 dolu; ayar değil, etki ölçümü):

| | v1 | Yalnız yük bandı | v2 (ikisi) |
|---|---|---|---|
| Yeşil | 83 | 85 | **44** |
| Yanlış yeşil | 0/83 | 0/85 | **0/44** |
| Kırmızı / yanlış kırmızı | 32 / %28 | 32 / %28 | 51 / %41 |
| Sarı | %68 | %67 | %73 |
| Kaç ev hatası (orta / karamsar) | 1 / 2,5 | 1 / 3 | 2 / 5 |
| Kaç ev: gerçek < karamsar (P10 altı) | %12,2 | %12,6 | **%3,3** |
| Faz 2 %80 bant kapsaması (tüm ölçülmeyen) | %76,8 | %89,3 | %89,3 |

Sınav 11–20 (347 trafo, 74 dolu; **bir kez**, v2):

| | v1 | v2 |
|---|---|---|
| Yeşil | 87 (%25) | **48 (%14)** |
| Yanlış yeşil | 0/87 | **0/48** (GEÇTİ) |
| Kırmızı / yanlış kırmızı | 44 / %27,3 | 61 / %32,8 |
| Dolu trafoyu kırmızı görme | 32/74 | 41/74 |
| Sarı | %62,2 | %68,6 |
| Kaç ev hatası (orta / karamsar / iyimser) | 2 / 2 / 4 | 1 / 2 / 4 (GEÇTİ) |
| Kaç ev: P10 altı / P90 üstü | %15,0 / %4,6 | **%7,1 / %3,8** |
| Kaç ev aralık kapsaması | %80 | %89 |
| %40 kuralı | 41/284 | 41/284 (değişmez) |
| Faz 2 %80 bant kapsaması (`sinav.py faz2`, şehir ortancası) | %87,5 | **%96,4 (KALDI)** |

Yük hatası (ortanca %3,8, P90 %8,0) ve arketip değişmedi.

### − Yeşil yarıya iniyor, yanlış kırmızı ve sarı artıyor
- Gerçeğe karşı kalibrasyonun bedeli: farazi şehirde konut trafosuna yeşil 1, köye 0; yeşillerin çoğu otel ve çarşı.
- Sebep: farazi şehrin fiziği hesabın fiziğiyle aynı (aynı çözücü); gerçek dünyadaki model hatası farazide yok. İngiltere'ye göre eklenen sapma farazide yalnız temkin olarak görünüyor.

### − Faz 2'nin farazi kapsama maddesi kalıyor (%96)
- İspanya'ya göre genişleyen bant farazi şehirde fazla geniş: farazi şehir gerçek dünyadan daha düzgün (Muhittin: "üreticinin dünyaya göre fazla düzgün olması").
- Tüzük madde 3: kalibrasyon gerçeğe karşı ölçülür, yalnız üreticiyle değil. Farazi madde bilgi satırına inmeli; düzeltmesi Faz 8 (üreticiyi gerçeğe çapalama). Karar masasına soruldu.

### ? PIT İspanya'da düz değil
- 10 kovada en büyük sapma 0,100 → 0,086 (hedef ≤ 0,05).
- Tek bir k bandın genişliğini düzeltiyor, şeklini değil: önce kuyruklar ağır (ilk ve son kova %14 ve %20), sonra orta kova şişkin (%19).
- Model-sapma terimi ya da konformal kalibrasyon sonraki adım (ADR-0013 madde 3).

### ? Çift sayım
- `KOL_P` (yüksüz panelli kol, 1/6) da s de Bancroft'tan geliyor.
- İkisi birlikte temkinli yönde çift sayıyor olabilir. Kaldırmak model yapısı değişikliği; karar masasına soruldu.

## Deney günlüğü satırı (tüzük §3)
| Tarih | Sürüm | Tohum | Hipotez | Kapılar | İşletme | Karar |
|---|---|---|---|---|---|---|
| 31 Eki 21:55 | v1 → v2 (dal `kalibrasyon/faz7`), üretici 1.2, veri P1 + P2 | değişmedi; s ayrı akış | gerçeğe göre bant genişler, yanlış yeşil 0 kalır | yanlış yeşil 0/48 GEÇTİ; kalibrasyon: İspanya %80 → %79,1 bir-dışarıda (tolerans %70–90), %95 ≥ %90 (iç örnek %90,3), PIT 0,086 KALDI; İngiltere P98 6/6 (bir-dışarıda 6/6) | yeşil %25 → %14, yanlış kırmızı %27 → %33, sarı %62 → %69, kaç ev P10 altı %15 → %7 | terfi **önerisi** → PR; puanlayan Can (C1, C4); "iyileşti" denmez (doğrulama payı yok) |

## Karar / sıradaki adım
- PR açılır; Can dalda C1'i koşar ve onaylar (öneren ≠ puanlayan); birleşince karar masası Mac'te ve Can resmi `faz2`, `faz3`.
- Karar masasına iki soru (volkan.md UYARI): Faz 2'nin farazi kapsama maddesi bilgi satırına mı insin; `KOL_P` s ile birlikte kalsın mı.
- Sunum metni v1 rakamlarıyla kalır (karar masası 21:32).
- Çalıştırma:
```
python3 src/kalibrasyon.py --deneme
python3 src/edp_test.py <GIS_data> --cikti edp_satirlar.csv && python3 src/kalibrasyon.py ispanya edp_satirlar.csv
BOY=0.47 CEKILIS_JSON=ukpn_cekilis.json python3 src/ukpn_olasilik.py <ukpn klasörü> && python3 src/kalibrasyon.py ingiltere ukpn_cekilis.json
python3 src/sablon.py data/synthetic && python3 src/kac_ev_olasilik.py data/synthetic
python3 src/sinav.py faz2 data/synthetic --aralik 11-20; python3 src/sinav.py faz3 data/synthetic --aralik 11-20
```

## Ek girdi — 31 Ekim 21:51: karar masası dört eksi bulguya karar verdi (kod değişmedi, yeniden koşum yok)
1. **Faz 2 farazi kapsama maddesi bilgi satırına indi; kapı İspanya** (%79, bir-dışarıda). Farazi 11–20'de %96 beklenen: üretici fazla düzgün; Faz 8'de gerçeğe çapalanınca yeniden. PR Faz 8'i beklemez.
2. **Bedel kabul:** yeşil %25 → %14, yanlış kırmızı %27 → %33, sarı %62 → %69. Önce iki kapı (yanlış yeşil 0/48, İspanya %79, İngiltere 6/6), işletme ölçüleri sonra (tüzük madde 2). **σ notu:** σ = 0,41 altı hattan moment tahmini; aralık 0,12–0,41. 0,41 en temkinli uç değil, tahmin. Pilot hatlarıyla yeniden (Faz 10).
3. **PIT toleransı örnek büyüklüğüne bağlı:** max(0,05; 2·√(0,09 ÷ n)); İspanya n = 29 → 0,11; 0,086 geçer. Formül tüzük madde 2'de; Can'ın C1 (b) maddesi aynı. Şekil düzeltmesi (konformal / yük tarafı model-sapma) Faz 10'da.
4. **`KOL_P` kalır.** s, `KOL_P`'li modelin İngiltere artıklarından tahmin edildi; `KOL_P`'yi kaldırıp s'yi yeniden fit etmek aynı 6 hattın bilgisini s'ye taşır, kazanç yok. **Çift sayım riski temkin yönünde; Faz 10'da pilot hatlarıyla ayrıştırılır.**

Birleşme koşulu (karar masası): karar masasının Mac koşumu BUILD rakamlarıyla tutar **ve** Can C1'i dalda koşup onaylar; sonra karar masası birleştirir, Can resmi `faz2` / `faz3`, sunum rakamları v2.

## Ek girdi — 31 Ekim 22:15: İspanya satırları artık yayımlanan bandı taşıyor (karar masası 22:0x)
- **Sorun:** `edp_test.py --cikti` satırlarındaki alt / üst bant K_YUK'u içermiyordu; k yalnız `sablon.py`'de ve `kalibrasyon.py`'nin içindeydi. Can'ın resmi İspanya maddesi bu satırlarla "KALDI" gösterdi (%80 bant %66,6, PIT 0,108).
- **Düzeltme:** `edp_test.py` bandı `sablon.K_YUK` ile log ölçekte genişletiyor (tek kaynak). `--kalibrasyonsuz` "önce" ve k'nin hesabı için. Tüzük madde 2'de n = bağımsız trafo / karar noktası (İspanya 29; satırlar tekrar).
- **Sağlama (Mac, BUILD):**

| `edp_test.py` | k (`kalibrasyon.py ispanya`) | %80 bant | %95 bant | PIT sapması |
|---|---|---|---|---|
| `--kalibrasyonsuz` | 1,475 | %65,7 | %81,3 | 0,100 |
| varsayılan (K_YUK) | 1,000 | %80,0 (iç örnek) | %90,3 | 0,086 (tolerans 0,11) |

- Komutlar (önceki komut bloğunun yerine):
```
python3 src/edp_test.py <GIS_data> --kalibrasyonsuz --cikti edp_once.csv && python3 src/kalibrasyon.py ispanya edp_once.csv   # k
python3 src/edp_test.py <GIS_data> --cikti edp_sonra.csv && python3 src/kalibrasyon.py ispanya edp_sonra.csv                   # sağlama: k ≈ 1
```

## Ek girdi — 31 Ekim 22:20: k_yük ölçülü sayısına bağlı; K_YUK 1,475 → 1,27 (karar masası 22:0x)
**Bulgu (Faz 8 ayarında):** üretici dağınıklaşınca farazi kapsama hiç inmedi. Sebep k'nin hesabında: İspanya satırları 5, 10 ve 15 ölçülü denemelerin karışımıydı. Model her şehirde 12 ölçülü kullanıyor (`OLCULU_ANA`).

| Ölçülü (İspanya, girdi c) | Satır | k | %80 bant önce | Bir-dışarıda kapsama, sonra |
|---|---|---|---|---|
| 5 | 960 | 1,93 | %57,9 | %79,2 |
| 10 | 760 | 1,21 | %73,4 | %78,3 |
| 15 | 560 | 1,33 | %68,8 | %77,9 |
| **10 + 15** | 1.320 | **1,27** | %71,4 | **%78,6** |
| hepsi (önceki K_YUK) | 2.280 | 1,475 | %65,7 | %79,1 |

- **İlke (tüzük madde 3'e eklendi):** kalibrasyon modelin sevk edildiği yapılandırmada ölçülür. 5 ölçülü denemeler başka bir modelin hatası; karışım k'yi şişiriyordu.
- **k ölçülü sayısına bağlı:** ölçülü sayısı değişirse k yeniden; pilotta yeniden.
- `K_YUK = 1,27` (`sablon.py`, `edp_test.py` aynı sabiti okur); `kalibrasyon.py ispanya --n 10,15` varsayılan.
- İspanya, 10 + 15 kesiti: %80 bant %71,4 → %80,0 iç örnek, %78,6 bir-dışarıda; %95 bant %87,5 → %93,1; PIT sapması 0,068 → 0,102 (tolerans n = 29'da 0,11: geçer, ama şekil k ile kötüleşiyor, Faz 10).

**Sınav 11–20 bir kez daha (v2b; v1.2 şehirleri, BUILD klasörü):**

| | v1 | v2 (k 1,475) | **v2b (k 1,27)** |
|---|---|---|---|
| Yanlış yeşil | 0/87 | 0/48 | **0/49** (GEÇTİ) |
| Yeşil | 87 (%25) | 48 (%14) | 49 (%14) |
| Kırmızı / yanlış kırmızı | 44 / %27,3 | 61 / %32,8 | 61 / %32,8 |
| Sarı | %62,2 | %68,6 | %68,3 |
| Kaç ev orta / karamsar | 2 / 2 | 1 / 2 | 1 / 2 (GEÇTİ) |
| Kaç ev P10 altı / P90 üstü | %15,0 / %4,6 | %7,1 / %3,8 | %7,1 / %4,6 |
| Faz 2 farazi kapsama (şehir ortancası; bilgi) | %87,5 | %96,4 | **%92,9** |

Geliştirme 1–10: Faz 2 farazi kapsama %87,5 (GEÇTİ); Faz 3 v2 ile aynı (yeşil 44, yanlış yeşil 0/44). Faz 3 değişmiyor, çünkü k yalnız yük bandını genişletiyor; yeşil ve kırmızıyı belirleyen gerilim tarafı (s).

## Ek 3 (31 Ekim 23:45, BUILD; karar masası 23:13): K_YUK 1,27 → 1,47, ürünün seçim yöntemi tabakalı

**Neden:** Can'ın sınav işlerinin kontrolünde (can.md KONTROL 23:15) bulundu: sınav ürünün seçimini ölçüyor (faturalı, 10 ölçülü, **tabakalı**), K_YUK ise rastgele + tabakalı seçimin havuzundan geliyordu. İki yolun hatası ters yönde. Kural 22:06'daki ilke (sevk yapılandırması), sonuca bakılarak değil: ürün ölçülecek trafoyu tabakalı seçer (`sablon.py` `ogretici_sec`).

**k, seçim yöntemi × ölçülü sayısı** [Hesap: `edp_test.py --kalibrasyonsuz`, girdi c, main]:

| Seçim | 5 | 10 | 15 | 10 + 15 |
|---|---|---|---|---|
| rastgele | 1,99 | 0,99 | 1,17 | 1,07 |
| **tabakalı** | 1,86 | 1,39 | 1,56 | **1,47** |
| ikisi havuzda (eski) | 1,93 | 1,21 | 1,33 | 1,27 |

- `K_YUK = 1,47` (`sablon.py`; `edp_test.py` aynı sabiti okur); `kalibrasyon.py ispanya` varsayılan kesiti tabakalı 10 + 15 (`--yol`); tüzük madde 3'e "ölçülü sayısı ve seçim yöntemi dahil".
- Tabakalı 10 + 15 kesitinde (28 trafo, 660 satır): %80 bant %65,2 → %80,0 iç örnek, **%78,5 bir-dışarıda** (bir-dışarıda k 1,38–1,50); PIT sapması 0,130 → 0,097 (tolerans 0,113).

**Sınav 21–30 bir kez (üretici 1.3, model v2b, K 1,47; Mac):**

| | K 1,27 | **K 1,47** |
|---|---|---|
| İspanya %80 bant (Can'ın maddesi, 10 / tabakalı) | %76,8 | **%82,1** (GEÇTİ) |
| İspanya %95 bant (bilgi, n < 150) | %88,9 | %92,6 |
| İspanya PIT sapması (tolerans 0,113) | 0,071 fazla emin | 0,066 fazla geniş (GEÇTİ) |
| Farazi %80 bant (bilgi) | %82,1 | %89,3 |
| Yanlış yeşil | 0/17 | **0/17** (GEÇTİ) |
| Yeşil / kırmızı / sarı | 17 / 61 / %77,7 | 17 / 61 / %77,7 |
| Kırmızı kovasında aşan (eşik %37) | %49 | %49 (GEÇTİ) |
| Kaç ev orta / P10 altı | 2 | 2 |

Geliştirme 1–10: renkler aynı (yeşil 20, kırmızı 53, sarı 281, yanlış yeşil 0/20); İspanya %82,1, PIT 0,066. Renk değişmiyor, çünkü k yalnız yük bandını genişletiyor; rengi gerilim tarafı belirliyor (Ek 2'deki gibi). Bant genişleyince yeşil ancak azalabilir; bu turda azalmadı.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
