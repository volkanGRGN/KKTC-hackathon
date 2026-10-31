# Tablo biçimi sözleşmesi

Sürüm 1 · 31 Ekim 2026 · sahibi Volkan (+ Claude) · değişiklik yalnız dal + PR ile, Can ya da Civan onayıyla ([CONTRIBUTING](../../CONTRIBUTING.md) "Dallar").

Dosyalar arasında geçen tabloların **tek tanımı**. Kod buna uyar. Sütun eksik ya da yanlış geliyorsa önce bu dosyaya bak; değişiklik gerekiyorsa [Volkan'ın kutusuna](../istek/volkan.md) yaz. Örnek değerler biçimi göstermek içindir; ölçüm ya da sonuç değildir.

## Genel kurallar

- **Klasör:** her şehir `data/synthetic/sehir-<NNN>/` (NNN = tohum, üç hane: `sehir-007`). Depoya girmez (`.gitignore`), tohumla yeniden üretilir.
- **Sahte şehir** (Civan'ın `app/ornek_veri.py`'si): tohum 900–999, aynı klasör düzeni (`sehir-901/`). Harita bu şehirlerde "SAHTE VERİ" yazar.
- **CSV:** UTF-8 (BOM yok), ayırıcı virgül, **ondalık nokta** (`12.5`; `12,5` değil), ilk satır başlık, satır sonu LF. Python'da `open(yol, 'w', encoding='utf-8', newline='')` + `csv`, ya da `pandas.to_csv(yol, index=False)`.
- **Adlar:** sütun adları ve kategorik değerler ASCII küçük harf ve alt çizgi; Türkçe harf yok (`koy`, `carsi`, `isgunu`). Doğru/yanlış = `1`/`0`. Boş hücre = değer yok.
- **Anahtar:** her tabloda `sehir` (int) ve `trafo_no` (str, `T01`…`T40`). (sehir, trafo_no) bütün dosyalarda aynı trafodur. Satırlar `trafo_no` sırasında.
- **Yuvarlama:** kW 2 hane, V 1 hane, metre tam sayı, derece 6 hane, oran 3 hane.
- **Zaman:** yerel saat (EAC eğrileriyle aynı). `adim` 0–287; adım i = [i×5, i×5+5) dakika; `saat` adımın başı, `"HH:MM"`. **Öğlen penceresi** 11:00–14:00 = adım 132–167 (36 adım).
- **Benzetilen günler (sürüm 1):** Nisan, 14 gün = 10 iş günü + 4 tatil. Nisan, Kıb-Tek'in 2023'te en az tükettiği ay [Kaynaklı: Kıb-Tek 2023 istatistik, aylık tüketim, Nisan 101.671 MWh; `data/raw/kibtek-istatistik/`].

## Dosyalar: kim yazar, kim okur

| Dosya | Yazan | Okuyan | Faz |
|---|---|---|---|
| `trafolar.csv` | `src/sehir_uret.py` (Volkan) | `sablon.py`, `kac_ev.py`, `sinav.py`, harita | 1 |
| `yuk_5dk.csv` | `src/sehir_uret.py` | `sablon.py` (**yalnız ölçülü trafoların satırları**), harita yan paneli, `sinav.py` | 1 |
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
| `kva` | int | kVA | `250` | direk 25/50/100/250/400 [Kaynaklı: Kıb-Tek şartnamesi, veri sözlüğü]; yer 630/1000 [Yorum] |
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
| `tip` | str | — | `sehir_konut` | `sehir_konut` / `koy` / `carsi` / `otel` / `sanayi` / `sulama` / `yurt` ([sözlük](../glossary.md) "Tip") |
| `v0_v` | float | V | `247.6` | trafo çıkış faz gerilimi, boşta; 246–250 rastgele (kademe bilinmiyor) |
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
| `kac_ev_tavan` | int | 0/1 | `0` | 1 = adayların hepsi sığdı; gerçek kapasite daha yüksek olabilir (sayı alttan kesik) |
| `kac_ev_sinir` | str | — | `gerilim` | ortanca sırada ilk aşımın nedeni: `gerilim` / `isil` / `yok` (tavan) |

**"Gerçek kaç ev" tanımı:** panelsiz konut aboneler rastgele sıraya dizilir (Kıb-Tek'in başvuru sırası gibi). Sırayla her birine 6,5 kW panel eklenir (ev tek fazlıysa kendi fazına) [ROADMAP Faz 1: bekleyen başvurular 5–8 kW, orta değer]. Kritik adımlarda (bugünkü en yüksek gerilimli 6 adım + en güçlü güneşli 3 adım) herhangi bir evde gerilim 259 V'u ya da trafo yükü kVA'yı aşınca durulur; o ana kadar eklenen ev sayısı sonuçtur. Bugün zaten aşıyorsa 0. 7 farklı sıra, ortanca.

## 4. `ayar.json` — şehrin ayarları (Faz 1)

Zorunlu anahtarlar: `sehir`, `tohum`, `sozlesme_surumu` (bu dosyanın sürümü), `uretici_surumu`, `trafo_sayisi`, `tip_sayilari` ({tip: adet}), `ay`, `gun_turleri` (14 elemanlı liste), `profil_kaynagi` (`eac` ya da `yer_tutucu`), `isinim_kaynagi`, `tuketim_carpani` ({sınıf: oran}), `saat_kaymasi_dk` ({sınıf: dakika}), `panel_yayginligi`, `yeni_panel_kw`, `v_sinir_v`, `referans_enlem`, `referans_boylam`. Ek anahtar serbest.

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

Deneyler (5 / 10 / 20 ölçülü, tekrarlar): `deney/tahmin_n<ölçülü>_t<tekrar>.csv`, aynı sütunlar.

**`arketipler.csv`** (yan dosya; satır = arketip × gün türü × adım): `sehir`, `arketip` (int), `arketip_adi` (str, ör. `aksam_tepeli_konut`), `gun_turu`, `adim`, `oran` (0–1, tepeye bölünmüş eğri). Harita yan paneli tahmini eğriyi şöyle çizer: `oran` × (`ogle_min_kw` ÷ arketipin öğlen penceresindeki en düşük `oran`). Ölçekleme doğrulanmadı ([ADR-0001](../decisions/adr-0001-sekil-buyukluk-sablon.md)).

## 6. `kac_ev.csv` — Faz 3 kaç ev tablosu

Satır = bir trafo.

| Sütun | Tür | Birim | Örnek | Açıklama |
|---|---|---|---|---|
| `sehir`, `trafo_no` | | | | anahtar |
| `kac_ev_karamsar` | int | ev | `1` | P10 yük, tek faz, trafo çıkışı 250 V |
| `kac_ev_iyimser` | int | ev | `6` | P90 yük, dengeli üç faz, 246 V |
| `isil_pay_kw` | float | kW | `142.0` | trafonun ısınmadan alabileceği ek panel |
| `gerilim_pay_kw_karamsar` | float | kW | `8.60` | |
| `gerilim_pay_kw_iyimser` | float | kW | `41.30` | |
| `sinir_karamsar` | str | — | `gerilim` | karamsar senaryoda bağlayan: `gerilim` / `isil` |
| `renk` | str | — | `sari` | `yesil` / `sari` / `kirmizi` ([yöntem](../method/modeling.md) bölüm 5) |
| `kural40_ev` | int | ev | `9` | %40 kuralının dediği: ⌊max(0, 0,4 × `kva` − `panel_kw`) ÷ 6,5⌋ |

"Ölçülmedi" etiketi = `tahmin.csv`'de `olculdu` = 0. Harita `trafolar.csv`, `tahmin.csv`, `kac_ev.csv`'yi (sehir, trafo_no) ile birleştirir.
