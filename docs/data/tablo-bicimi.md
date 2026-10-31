# Tablo biçimi sözleşmesi

Sürüm 1.4 adayı (PR, Can ya da Civan onayı bekliyor) · 31 Ekim 2026 (1.1: şehirler arası deney dosyası, `sablon_ozet.json`, JSON da LF, `oran` brüt; 1.2: `yillik_tuketim_mwh`, bayramlar tatil, gerçek veri 800–899, cevap anahtarında mahalle farkı, `ayar.json` bilgi anahtarları; ADR-0007, ADR-0008; 1.3: `kac_ev.csv` olasılıklı hesaptan, sonda üç ek sütun; ADR-0011; 1.4: yıl boyu tepe, cevap anahtarında sonda on sütun, `yuk_5dk_yaz.csv` / `yuk_5dk_kis.csv`; ADR-0014, karar masası 23:12) · sahibi Volkan (+ Claude) · değişiklik yalnız dal + PR ile, Can ya da Civan onayıyla ([CONTRIBUTING](../../CONTRIBUTING.md) "Dallar").

Dosyalar arasında geçen tabloların **tek tanımı**. Kod buna uyar. Sütun eksik ya da yanlış geliyorsa önce bu dosyaya bak; değişiklik gerekiyorsa [Volkan'ın kutusuna](../istek/volkan.md) yaz. Örnek değerler biçimi göstermek içindir; ölçüm ya da sonuç değildir.

## Genel kurallar

- **Klasör:** her şehir `data/synthetic/sehir-<NNN>/` (NNN = tohum, üç hane: `sehir-007`). Depoya girmez (`.gitignore`), tohumla yeniden üretilir.
- **Sahte şehir** (Civan'ın `app/ornek_veri.py`'si): tohum 900–999, aynı klasör düzeni (`sehir-901/`). Harita bu şehirlerde "SAHTE VERİ" yazar.
- **Gerçek veri** (sürüm 1.2): şehir no 800–899, aynı klasör düzeni; `ayar.json`'da `veri_turu` = `gercek` ve `veri_kaynagi` (ör. `"EDP Oviedo 2018, Mendeley CC BY"`) zorunlu. Harita "GERÇEK ÖLÇÜM — <veri_kaynagi> (Kıbrıs değil)" yazar. Gerçek veride bulunmayan sütun boş bırakılır (ör. abone sınıfı yoksa hepsi `abone_konut`'ta, `yillik_tuketim_mwh` boş). Farazi şehir 1–799 (`veri_turu` = `farazi`).
- **CSV:** UTF-8 (BOM yok), ayırıcı virgül, **ondalık nokta** (`12.5`; `12,5` değil), ilk satır başlık, satır sonu LF. **JSON da** UTF-8 ve LF (`newline=''`). Python'da `open(yol, 'w', encoding='utf-8', newline='')` + `csv`, ya da `pandas.to_csv(yol, index=False)`.
- **Adlar:** sütun adları ve kategorik değerler ASCII küçük harf ve alt çizgi; Türkçe harf yok (`koy`, `carsi`, `isgunu`). Doğru/yanlış = `1`/`0`. Boş hücre = değer yok.
- **Anahtar:** her tabloda `sehir` (int) ve `trafo_no` (str, `T01`…`T40`). (sehir, trafo_no) bütün dosyalarda aynı trafodur. Satırlar `trafo_no` sırasında.
- **Yuvarlama:** kW ve MWh 2 hane, V 1 hane, metre tam sayı, derece 6 hane, oran 3 hane.
- **Zaman:** yerel saat (EAC eğrileriyle aynı). `adim` 0–287; adım i = [i×5, i×5+5) dakika; `saat` adımın başı, `"HH:MM"`. **Öğlen penceresi** 11:00–14:00 = adım 132–167 (36 adım).
- **Benzetilen günler:** Nisan, ardışık 14 gün. Sürüm 1–1.1: 10 iş günü + 4 tatil (hafta sonu). **Sürüm 1.2:** hafta sonu ve KKTC resmi tatilleri (Ramazan Bayramı, 23 Nisan) `tatil`; 14 günde 4–7 tatil, liste `ayar.json` `bayramlar`'da. Hava yılı 2023 / 2024 / 2025. Nisan, Kıb-Tek'in 2023'te en az tükettiği ay [Kaynaklı: Kıb-Tek 2023 istatistik, aylık tüketim, Nisan 101.671 MWh; `data/raw/kibtek-istatistik/`].

## Dosyalar: kim yazar, kim okur

| Dosya | Yazan | Okuyan | Faz |
|---|---|---|---|
| `trafolar.csv` | `src/sehir_uret.py` (Volkan) | `sablon.py`, `kac_ev.py`, `sinav.py`, harita | 1 |
| `yuk_5dk.csv` | `src/sehir_uret.py` | `sablon.py` ve harita yan paneli (**yalnız ölçülü trafoların satırları**; ölçülmeyenin eğrisi `arketipler.csv`'den), `sinav.py` (hepsi) | 1 |
| `yuk_5dk_yaz.csv`, `yuk_5dk_kis.csv` | `src/sehir_uret.py` (**1.4**) | tepe modeli (yalnız ölçülü trafoların satırları), `sinav.py` (hepsi) | 11 |
| `cevap_anahtari.csv` | `src/sehir_uret.py` | **yalnız** `sinav.py` ve `grafikler.py` | 1 |
| `ayar.json` | `src/sehir_uret.py` | herkes (bilgi) | 1 |
| `tahmin.csv`, `arketipler.csv` | `src/sablon.py` (Volkan) | `kac_ev.py`, `sinav.py`, harita | 2 |
| `kac_ev.csv` | `src/kac_ev.py` (Volkan) | `sinav.py`, `grafikler.py`, harita | 3 |

**Ayrım kuralı:** `trafolar.csv` yalnız Kıb-Tek'in gerçekte bilebileceğini taşır (modelin girdisi). Benzetimin bilip Kıb-Tek'in bilmediği her şey (tip, faz dağılımı, trafo çıkış gerilimi, gerçek yük, gerçek kaç ev) `cevap_anahtari.csv`'dedir. Model ya da harita cevap anahtarını okursa sınav anlamsızlaşır.

---

## 1. `trafolar.csv` — trafo tablosu (Faz 1)

Satır = bir trafo.

| Sütun | Tür | Birim | Örnek | Açıklama |
|---|---|---|---|---|
| `sehir` | int | — | `7` | tohum |
| `trafo_no` | str | — | `T07` | |
| `enlem` | float | derece | `35.341210` | WGS84; `ayar.json`'daki referans noktası çevresine yerleştirilir, gerçek trafo yeri değil |
| `boylam` | float | derece | `33.171804` | |
| `x_m` | int | m | `520` | referans noktasından doğuya |
| `y_m` | int | m | `-310` | referans noktasından kuzeye |
| `bolge` | str | — | `kentsel` | `kentsel` / `kirsal` / `turistik` / `sanayi` |
| `montaj` | str | — | `direk` | `direk` / `yer` |
| `kva` | int | kVA | `250` | direk 25/50/100/250/400 [varsayım: Kıb-Tek şartnamesi, kaynak bağlantısı yok]; yer 630/1000 [Yorum]. Dayanak: ASTOR kataloğu (2020; Elparts'ın sattığı marka) yağlı dağıtım trafosu 50–5000 kVA, kompakt trafo merkezi 1000 / 1600 kVA [Kaynaklı]; 25 kVA kaynaksız |
| `hat_sayisi` | int | adet | `2` | trafodan çıkan alçak gerilim hattı |
| `hat_boyu_max_m` | int | m | `420` | en uzun hattın trafodan son eve boyu (Faz 3 formülündeki L) |
| `hat_boyu_toplam_m` | int | m | `740` | |
| `kablo` | str | — | `ABC70` | `ABC70` / `ABC95` |
| `abone_konut` | int | adet | `38` | Kıb-Tek konut tarifesi |
| `abone_ticari1` | int | adet | `3` | ticari tarife I |
| `abone_ticari2` | int | adet | `0` | ticari tarife II (yurt binaları da burada, [Yorum]: tarifesi BULAMADIM) |
| `abone_turizm` | int | adet | `0` | turizm tarifesi (otel) |
| `abone_sanayi1` | int | adet | `0` | endüstri tarifesi I |
| `abone_sanayi2` | int | adet | `0` | endüstri tarifesi II |
| `abone_su_motoru` | int | adet | `0` | su motorları tarifesi |
| `panel_sayisi` | int | adet | `9` | bağlı panelli abone |
| `panel_kw` | float | kW | `40.0` | bağlı panellerin kurulu toplamı |
| `yillik_tuketim_mwh` | float | MWh | `142.38` | **1.2.** Trafodaki abonelerin son 12 ay fatura toplamı ([ADR-0007](../decisions/adr-0007-yillik-fatura-tuketimi-girdi.md)). Kıb-Tek faturayı bilir; abone–trafo eşleşmesi varsayımı abone sütunlarınınkiyle aynı. Üretici: abone yıllık enerjilerinin toplamı × fatura sapması 0,95–1,05 [Yorum]; brüt tüketim (mahsuplaşmalı panelli evin faturası net olabilir, [Yorum]). Boş olabilir (gerçek veri): model o zaman abone sayılarıyla çalışır |

Varsayım: hat boyu ve kablonun Kıb-Tek kaydında olup olmadığı BULAMADIM ([plan](../01-plan.md), uzmana soru 3); burada biliniyor sayıldı. Faz dağılımı bilinmiyor sayıldı ([ADR-0002](../decisions/adr-0002-gerilim-ilk-surumde.md)) → cevap anahtarında.

## 2. `yuk_5dk.csv` — 5 dakikalık trafo yükü (Faz 1)

Satır = bir trafo × bir gün × bir adım (40 trafo × 14 gün × 288 adım = 161.280 satır).

| Sütun | Tür | Birim | Örnek | Açıklama |
|---|---|---|---|---|
| `sehir`, `trafo_no` | | | | anahtar |
| `gun` | int | — | `3` | 0–13 |
| `gun_turu` | str | — | `isgunu` | `isgunu` / `tatil` |
| `adim` | int | — | `133` | 0–287 |
| `saat` | str | — | `11:05` | |
| `tuketim_kw` | float | kW | `31.42` | abonelerin brüt tüketimi, panel hariç |
| `uretim_kw` | float | kW | `12.80` | bağlı panellerin üretimi |
| `net_kw` | float | kW | `18.62` | trafodan geçen = tüketim − üretim; **eksi = ters akış**. Ölçüm cihazının göreceği değer |
| `v_max_v` | float | V | `252.3` | o adımda bu trafonun evlerinde en yüksek faz gerilimi |
| `v_min_v` | float | V | `238.9` | en düşük faz gerilimi |

Ölçülü trafoda `tuketim_kw`'nin ölçümden çıkarılabildiği varsayılır (net + kurulu güç × ışınım) [Yorum]. Ev ev gerilim serisi dosyaya yazılmaz (şehir başına milyonlarca değer); trafo başına adım adım en yüksek ve en düşük yeter.

## 3. `cevap_anahtari.csv` — benzetimin bildiği gerçek (Faz 1)

Satır = bir trafo. **Model ve harita okumaz.**

| Sütun | Tür | Birim | Örnek | Açıklama |
|---|---|---|---|---|
| `sehir`, `trafo_no` | | | | anahtar |
| `tip` | str | — | `sehir_konutu` | `sehir_konutu` / `koy` / `carsi` / `otel` / `sanayi` / `sulama` / `yurt` ([sözlük](../glossary.md) "Tip") |
| `v0_v` | float | V | `247.6` | trafo çıkış faz gerilimi, boşta; trafoda boşta kademe değiştirici var [Kaynaklı: ASTOR kataloğu], adımı ve Kıb-Tek'in ayarı bilinmiyor, rastgele: 246–250 (1.1'e kadar), **244–252 (1.2**; UKPN bara yayılımı, karar masası 16:27) |
| `faz_a_ev`, `faz_b_ev`, `faz_c_ev` | int | adet | `14` | tek fazlı aboneler hangi fazda |
| `uc_faz_ev` | int | adet | `3` | üç fazlı abone |
| `ogle_min_kw` | float | kW | `9.84` | **Faz 2'nin hedefi:** öğlen penceresinde brüt tüketimin en düşüğü, 14 günün hepsinde |
| `ogle_min_kw_isgunu` | float | kW | `10.21` | yalnız iş günleri |
| `ogle_min_kw_tatil` | float | kW | `9.84` | yalnız tatiller |
| `ogle_min_net_kw` | float | kW | `-21.30` | aynı pencerede `net_kw`'nin en düşüğü |
| `tepe_kw` | float | kW | `62.10` | 14 günde brüt tüketim tepesi (New York'un "öğlen = tepenin %15–40'ı" kaba kuralıyla kıyas için) |
| `v_max_bugun_v` | float | V | `256.8` | bugünkü panellerle 14 günde en yüksek ev gerilimi |
| `v_min_bugun_v` | float | V | `229.4` | en düşük ev gerilimi |
| `kac_ev_aday` | int | adet | `29` | panelsiz konut abone (başvurabilecek ev) |
| `kac_ev_gercek` | int | ev | `4` | ev ev benzetimle "kaç ev daha sığar"; 7 başvuru sırasının ortancası (tanım aşağıda) |
| `kac_ev_gercek_min` | int | ev | `2` | 7 sıranın en küçüğü |
| `kac_ev_gercek_max` | int | ev | `7` | en büyüğü |
| `kac_ev_tavan` | int | 0/1 | `0` | 1 = adayların hepsi sığdı; gerçek kapasite daha yüksek olabilir (sayı alttan kesik). `kac_ev_aday` = 0 ise de 1; o trafoda kaç ev sütunları bilgi taşımaz |
| `kac_ev_sinir` | str | — | `gerilim` | ortanca sırada ilk reddin nedeni (bugün zaten aşıyorsa bugünkü aşımın): `gerilim` / `isil` / `yok` (hiç ret yok) |
| `mahalle_carpani` | float | oran | `0.932` | **1.2.** Trafonun küçük abonelerine (konut, ticari I, sanayi I, su motoru) uygulanan mahalle tüketim çarpanı, log-normal ([ADR-0008](../decisions/adr-0008-farazi-cesitlilik-saf-tahmin.md)) |
| `saat_kaymasi_dk` | int | dk | `-15` | **1.2.** Trafonun bütün abonelerine eklenen saat kayması, ±30 dk (sınıf başına şehir kaymasının üstüne) |
| `tepe_yil_kw` | float | kW | `88.23` | **1.4. Yük haritasının hedefi:** yılın net tepesi (trafodan geçen: tüketim − üretim), üç pencerenin (Nisan 14 gün, yazın en sıcak 7 günü, kışın en soğuk 7 günü) 5 dakikalık adımlarında en büyük |
| `tepe_yil_kva` | float | kVA | `102.20` | **1.4.** Aynı pencerelerde trafonun görünür gücü (yük akışından, kayıplar dahil), en büyük; `kva` ile kıyas: tüketim doluluğu |
| `tepe_saati` | str | SS:DD | `19:55` | **1.4.** `tepe_yil_kw`'nin saati (adımın başı) |
| `tepe_ayi` | int | ay | `8` | **1.4.** `tepe_yil_kw`'nin ayı (1–12) |
| `v_min_tepe_v` | float | V | `201.3` | **1.4.** Üç pencerede en düşük ev gerilimi (akşam düşümü; 207 V kontrolü) |
| `tepe_yaz_kw`, `tepe_kis_kw` | float | kW | `88.23` | **1.4.** Yaz ve kış penceresinin net tepesi; pencere üretilmediyse boş |
| `kva_tavan` | int | 0/1 | `0` | **1.4.** 1 = gereken güç listedeki en büyük trafoyu (1000 kVA) aştı, listeye kesildi; tüketim doluluğu bu trafolarda üreticinin sınırı, ayrı raporlanır |
| `klima_carpani` | float | oran | `1.12` | **1.4.** Trafonun sıcaklık duyarlılığı çarpanı (klima / ısıtma yaygınlığı), U(0,5; 1,5), gizli (mahalle çarpanı gibi) |
| `tepe_yil_brut_kw` | float | kW | `91.40` | **1.4.** Aynı pencerelerde brüt tüketim tepesi (panelsiz); `tepe_yil_kw` ile farkı panelin tepeye etkisi (Can, volkan.md 23:12 sonrası madde 3) |

**"Gerçek kaç ev" tanımı:** panelsiz konut aboneler rastgele sıraya dizilir (Kıb-Tek'in başvuru sırası gibi). Sırayla her birine 6,5 kW panel eklenir (ev tek fazlıysa kendi fazına) [ROADMAP Faz 1: bekleyen başvurular 5–8 kW, orta değer]. Kritik adımlarda (bugünkü en yüksek gerilimli 6 adım + en güçlü güneşli 3 adım) herhangi bir evde gerilim 259 V'u ya da trafo yükü kVA'yı aşarsa o başvuru reddedilir ve **sıradakine geçilir** (ilk retle durulmaz: hat ucundaki bir evin sığmaması trafoya yakın evi engellemez). Onaylanan ev sayısı sonuçtur. Bugün zaten aşıyorsa 0. 7 farklı sıra, ortanca.

### 3b. `yuk_5dk_yaz.csv`, `yuk_5dk_kis.csv` — yaz ve kış penceresi (1.4, Faz 11)

`yuk_5dk.csv` ile aynı satır düzeni, ayrıca `tarih` (ISO), `sicaklik_c` (Open-Meteo Lefkoşa, saatlikten doğrusal) ve `trafo_kva` (trafonun görünür gücü). Sütunlar: `sehir`, `trafo_no`, `gun`, `tarih`, `gun_turu`, `adim`, `saat`, `sicaklik_c`, `tuketim_kw`, `uretim_kw`, `net_kw`, `v_max_v`, `v_min_v`, `trafo_kva`. Pencere: şehrin hava yılında yazın (Haziran–Eylül) ve kışın (Ocak–Şubat) günlük ortalama sıcaklığı en uç 7 ardışık gün; tarihler `ayar.json` `yaz_penceresi` / `kis_penceresi`. Model bu dosyalardan yalnız ölçülü trafoların satırlarını okuyabilir (`yuk_5dk.csv` kuralı). Aynı ağ, aynı abone, aynı tohum; Nisan dosyaları 1.3 ile birebir.

## 4. `ayar.json` — şehrin ayarları (Faz 1)

Zorunlu anahtarlar: `sehir`, `tohum`, `sozlesme_surumu` (bu dosyanın sürümü; 1.2'den metin, ör. `"1.2"`), `uretici_surumu`, `trafo_sayisi`, `tip_sayilari` ({tip: adet}), `ay`, `gun_turleri` (14 elemanlı liste), `profil_kaynagi` (`eac` ya da `yer_tutucu`), `isinim_kaynagi`, `tuketim_carpani` ({sınıf: oran}), `saat_kaymasi_dk` ({sınıf: dakika}), `panel_yayginligi`, `yeni_panel_kw`, `v_sinir_v`, `referans_enlem`, `referans_boylam`, `hava_yili` (yapay ışınımda boş), `sure_sn` (üretim süresi); gerçek veride (800–899) ayrıca `veri_turu` = `gercek` ve `veri_kaynagi`. Ek anahtar serbest. Sürüm 1.2 bilgi anahtarları (üretici yazar, kimse zorunlu okumaz): `veri_turu` (`farazi`), `tarihler`, `bayramlar` (14 gün içindeki resmi tatiller), `mahalle_sigma`, `mahalle_kayma_dk`, `faz_sapma` ({bölge: tek fazlı abone faz ağırlığı sapması}), `kiyi_kontrolu` (`true` = OSM kıyı çizgisiyle trafolar karada), `kva_tavan_sayisi` (gereken güç 1000 kVA'yı aşıp tavana kesilen trafo), `v0_bant_v`, `faz_dengesizlik_ortanca` (hat başına (en büyük faz − ortalama) ÷ ortalama, yıllık enerjiyle; şehrin ortancası). Aynı tohum aynı şehri verir: CSV'ler birebir, `ayar.json`'da yalnız `sure_sn` farklı olabilir.

`profil_kaynagi` = `yer_tutucu` olan şehir Faz 1 geçme sınavına girmez (Can'ın `profiller.py`'si gelmeden üretilmiştir).

---

## 5. `tahmin.csv` — Faz 2 tahmin tablosu

Satır = bir trafo (ölçülü ve ölçülmeyen hepsi).

| Sütun | Tür | Birim | Örnek | Açıklama |
|---|---|---|---|---|
| `sehir`, `trafo_no` | | | | anahtar |
| `olculdu` | int | 0/1 | `0` | öğretici kümede, yani ölçüm cihazı takılı |
| `olculu_sayi` | int | adet | `12` | bu çalıştırmada ölçülü trafo sayısı (dosyada hep aynı) |
| `arketip` | int | — | `2` | 0 … k−1 |
| `arketip_olasilik` | float | oran | `0.74` | atama olasılığı |
| `ogle_min_kw` | float | kW | `11.30` | modelin tahmini (orta değer); ölçülü trafoda bir-trafo-dışarıda tahmini |
| `ogle_min_kw_p10` | float | kW | `7.90` | %80 bandın altı |
| `ogle_min_kw_p90` | float | kW | `15.20` | %80 bandın üstü |
| `ogle_min_kw_olculen` | float | kW | | yalnız ölçülü trafoda, `yuk_5dk.csv`'den ölçülen değer; değilse boş |
| `guven` | str | — | `orta` | `yuksek` / `orta` / `dusuk` |

Deneyler, aynı sütunlar:
- `deney/tahmin_n<ölçülü>_t<tekrar>.csv`: 5 / 10 / 20 ölçülü, 5 tekrar (öğretici küme farklı tohumla).
- `deney/tahmin_capraz_s<AAA>.csv`: şehirler arası. Model AAA şehrinin 12 ölçülüsüyle kuruldu, bu şehrin bütün trafolarını tahmin etti; `olculdu` hepsinde 0, `olculu_sayi` = 12, `arketip` AAA'nın arketip numarasıdır (bu şehrin `arketipler.csv`'siyle karşılaştırılmaz).

**`sablon_ozet.json`** (bilgi, eşiksiz): `fatura_kullanildi` (1.2), `taban` (1.2, hata tabanı), ölçülü trafolar, küme sayısı ve siluetler, arketip adları, ortak ve küme başına abone katsayıları (kW/abone), bir-dışarıda hata, güven sayıları. Sınav okumaz; günlük ve sunum için.

**`arketipler.csv`** (yan dosya; satır = arketip × gün türü × adım): `sehir`, `arketip` (int), `arketip_adi` (str, ör. `aksam_tepeli_konut`), `gun_turu`, `adim`, `oran` (0–1, tepeye bölünmüş eğri; **brüt tüketimden**: ölçülü trafoların `tuketim_kw` gün türü ortalaması, net değil). Harita yan paneli tahmini eğriyi şöyle çizer: `oran` × (`ogle_min_kw` ÷ arketipin öğlen penceresindeki en düşük `oran`). Ölçekleme doğrulanmadı ([ADR-0001](../decisions/adr-0001-sekil-buyukluk-sablon.md)).

## 6. `kac_ev.csv` — Faz 3 kaç ev tablosu

Satır = bir trafo.

| Sütun | Tür | Birim | Örnek | Açıklama |
|---|---|---|---|---|
| `sehir`, `trafo_no` | | | | anahtar |
| `kac_ev_karamsar` | int | ev | `1` | **1.3:** olasılıklı hesabın çekilişlerinin P10'u (ADR-0011); %80 bandın alt ucu, "en az" değil (sınavda gerçek bunun altında %15 trafoda; karar masası 19:13): bekleyen panelsiz konutlar rastgele sırayla 6,5 kW alır, sığmayan atlanır. Panelsiz konut abone sayısıyla sınırlı. (Yedek yol `kac_ev.py`: P10 yük, tek faz, 250 V, paneller hat ucunda.) |
| `kac_ev_iyimser` | int | ev | `6` | **1.3:** çekilişlerin P90'ı; %80 bandın üst ucu, "en çok" değil; aynı sınır. (Yedek: P90 yük, dengeli üç faz, 246 V, hat ortası.) |
| `isil_pay_kw` | float | kW | `142.0` | trafonun ısınmadan alabileceği ek panel (karamsar: P10 yük) |
| `gerilim_pay_kw_karamsar` | float | kW | `8.60` | |
| `gerilim_pay_kw_iyimser` | float | kW | `41.30` | |
| `sinir_karamsar` | str | — | `gerilim` | karamsar senaryoda bağlayan: `gerilim` / `isil` |
| `renk` | str | — | `sari` | `yesil` / `sari` / `kirmizi` ([yöntem](../method/modeling.md) bölüm 5, ADR-0010) |
| `kural40_ev` | int | ev | `9` | %40 kuralının dediği: ⌊max(0, 0,4 × `kva` − `panel_kw`) ÷ 6,5⌋ |
| `p_bugun_asar` | float | oran | `0.125` | **1.3:** bugün (yeni panelsiz, öğlen güneşi, en düşük yük) 259 V ya da kVA'nın aşılma olasılığı; ≥ 0,5 → kırmızı |
| `p_iki_ev_sigar` | float | oran | `0.975` | **1.3:** rastgele ilk iki başvurunun ikisinin de sığma olasılığı; ≥ 0,98 ve güven yüksek → yeşil |
| `kac_ev_orta` | int | ev | `3` | **1.3:** çekilişlerin ortancası (haritada gösterilecek tek sayı: "yaklaşık N ev (karamsar–iyimser)"). Vaat sayıda değil renkte: yeşil = ilk iki başvuru ≥ %98 sığar |

`isil_pay_kw`, `gerilim_pay_kw_karamsar`, `gerilim_pay_kw_iyimser`, `sinir_karamsar`, `kural40_ev` 1.3'te de tek denklemden (`kac_ev.py`); `renk` olasılıklı hesaptan (ADR-0011: kırmızı `p_bugun_asar` ≥ 0,5; yeşil `p_iki_ev_sigar` ≥ 0,98 ve güven yüksek; diğerleri sarı). Var olan sütunların adı ve sırası değişmedi; yeni üçü sonda.

"Ölçülmedi" etiketi = `tahmin.csv`'de `olculdu` = 0. Harita `trafolar.csv`, `tahmin.csv`, `kac_ev.csv`'yi (sehir, trafo_no) ile birleştirir.
