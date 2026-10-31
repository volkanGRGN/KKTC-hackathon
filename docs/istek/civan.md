# Civan için istekler

Burası Civan'ın kutusu; yalnız o işler. Kalıp için [README](README.md).

## BİLGİ 31 Eki 13:33 — karar masasından — sözleşme ve üretici main'de; panel yaygınlığı %3–25
Ne: (1) Sözleşme (`docs/data/tablo-bicimi.md`, PR #4) ve gerçek şehir üreticisi (`src/sehir_uret.py`, PR #6) main'e birleşti; Can'ın `profiller.py` ve `sinav.py` de main'de. Kartındaki "birleşene kadar dalda" notu geçersiz, sözleşmeyi main'den oku. İstersen haritayı gerçek şehirle de deneyebilirsin: `python3 src/sehir_uret.py 1` → `data/synthetic/sehir-001/` (EAC Excel'i `data/raw/eac-profil-siniflari/KAYNAK.txt` adresinden indirilmiş olmalı; Lefkoşa ışınım dosyası yoksa yapay ışınımla üretir, `ayar.json` yazar). Harita `cevap_anahtari.csv`'yi okumaz, hatırlatma.
(2) [ADR-0006](../decisions/adr-0006-panel-yayginligi-bugunun-kibrisi.md): Faz 1 şehirlerinde panel yaygınlığı %10–50 → **%3–25** (bugünün Kıbrıs'ı; Kıb-Tek 2023'te güneş üretimi toplamın %5,8'i). Sahte şehirlerinde `panel_sayisi` konut abonelerinin %3–25'i, `panel_kw` ≈ panel sayısı × 4–6,5 kW olsun ki harita bugünkü Kıbrıs'a benzesin; 20 gerçek şehir de bu aralıkla yeniden üretiliyor (BUILD oturumu).
(3) Sözleşmede küçük düzeltmeler oldu: `kva` etiketi varsayım; `kac_ev_tavan` = 1 ve `kac_ev_sinir` tanımları §3'te güncel; `ayar.json` da LF olacak. Harita için değişen sütun yok.
Senden beklenen: bir şey yapman gerekmiyor; sahte veride yaygınlık aralığını uygula, PR'ını açınca ben incelerim (sonucu bu kutuya yazarım).
Durum: bilgi

## KARAR 31 Eki 15:12 — volkan.md'deki "gerçek şehirlerde trafolar denize düşüyor" isteğine
Karar: Evet; `src/sehir_uret.py` `konum()` döngüsüne "karada mı" koşulu girer: senin `app/ornek_veri.py`'deki `kiyi_segmentleri()` + `karada()` olduğu gibi (docstring'de "Civan, app/ornek_veri.py" atfıyla), kıyı dosyası yoksa bugünkü 400 m kuralı + uyarı, `ayar.json`'a `kiyi_kontrolu`. Üretici sürüm 1.2 ile birlikte (fatura sütunu, mahalle çarpanı, bayramlar); şehirler o zaman yeniden üretilir. BUILD kıyı dosyasını KAYNAK.txt'deki komutla indirir.
Neden: Haritada denizdeki trafo ilk göze batan hata; ölçümün (otel %31) doğru. Kod senin dosyandan kopyalanır, sen `src/`'ye dokunmazsın.
Senden beklenen: hiçbir şey. (ana oturum: BUILD.)
Durum: bilgi — iş ana oturumda

## KARAR 31 Eki 15:12 — volkan.md'deki "sözleşme 1.2: gerçek veri şehir no 800–899 haritada nasıl etiketlensin?" isteğine
Karar: 800–899 → şerit "GERÇEK ÖLÇÜM — <veri_kaynagi> (Kıbrıs değil)"; kaynak adı `ayar.json` `veri_kaynagi` anahtarından (ör. "EDP Oviedo 2018, Mendeley CC BY"), anahtar yoksa "gerçek ölçüm verisi". Sözleşme 1.2'ye "800–899 gerçek veri; `ayar.json`'da `veri_kaynagi` ve `veri_turu` = `gercek` zorunlu" satırını BUILD ekler. Not: şu an gerçek veri klasörü üretilmiyor (BUILD İspanya'yı ham veriden koştu, PR #10); bu kural ileride lazım olursa diye, acil değil. `yillik_tuketim_mwh` sahte üreticiye 1.2 gelince, evet.
Neden: Etiket kuralı kartında, aralık sözleşmede; yanlış "farazi" etiketi jüri önünde dürüstlük sorunu olur.
Senden beklenen: `app/harita.py` `etiket()`'e üçüncü dal (tek satır), PR #9'dan sonra doğrudan main; sözleşme 1.2 PR'ı açılınca onay için bak (Can ya da sen).
Durum: yapıldı 16:58 (d617701: etiket() 800–899 dalı; README)

## PR İNCELEME 15:14 — PR #9 "harita: sahte şehir ve harita iskeleti (Civan Faz 1 kartı)"
Sonuç: birleştirilebilir.
+ Mac'te çalıştırdım (Python 3.13, Streamlit 1.x, pydeck): `ornek_veri.py` üç şehri üretiyor, iki çalıştırma birebir aynı (diff), beş CSV başlığı sözleşme §1/§2/§5/§6 ile birebir, UTF-8 + LF + BOM yok; panel/konut oranı %11 (ADR-0006 aralığında), kVA listesi sözleşmeye uygun, üç renk de çıkıyor (901: yeşil 13 / sarı 24 / kırmızı 3), ölçülü 10/40. Kıyı dosyası yokken uyarı verip 400 m kuralına düşüyor.
+ `harita.py` tarayıcıda: "SAHTE VERİ — gösterim" şeridi, renk özeti, tıklama → yan panel (T06: kVA, bölge, abone, panel, öğlen yük + bant, güven, "ölçülmedi", kaç ev karamsar–iyimser, renk, %40 kuralı) ve P10–P90'lı tahmini eğri. Gerçek şehir klasörü (`sehir-001`, tahmin yok) yanına konunca: "örnek veri (farazi şehir)" şeridi, "Renk yok" notu, gri sütunlar, tıklayınca "Eğri yok: … Faz 2" — `cevap_anahtari.csv` okunmuyor. Kartın Mac maddesi sağlandı; günlüğüne "Mac: karar masası doğruladı" yazabilirsin.
+ Kod sözleşmeye sadık: yalnız ölçülü satırlar okunuyor (`olculu_yuk`), `validate="one_to_one"` birleştirme, eksik tabloda çökme yok, `map_style=None` / `map_provider=None` internetsiz yol, "kendin karar ver" kalemleri günlükte.
− (küçük, birleşmeden sonra olur) `egri_ciz()`: `yuk.loc[yuk["gun"] == 0, "gun_turu"].iloc[0]` ölçülü satır hiç yoksa patlar; `if yuk.empty: st.info(...); return` bir satır. Ayrıca `etiket()`'e 800–899 dalı (KARAR 15:12).
? İnternetsiz açılış ve OSM zemin bende denenmedi (kıyı ve bina dosyaları Mac'te yok; zemin Carto'dan geldi). Tıklama süresi senin ölçümün (0,55 sn); bende göz kararı anında.
Senden beklenen: birleştir (kart: Volkan bakar → bakıldı); sonra küçük düzeltmeleri doğrudan main'e. `harita/iskelet` eski dalını silebilirsin.
Durum: yapıldı 16:58 (birleşti e16972e; boş-ölçülü koruması ve etiket d617701; günlükte "Mac: karar masası doğruladı"; eski harita/iskelet dalı şimdilik silinmedi)

## KARAR 16:50 — iş sırası (yeniden planlama; Faz 3 kartı BUILD'den gelecek, beklemeden başla)
Karar: Sıra: (1) PR #9'u birleştir (incelendi, birleştirilebilir); sonra doğrudan main. (2) `etiket()`'e 800–899 dalı + `egri_ciz` boş-ölçülü koruması (PR incelemesi). (3) Yan panel gerçek Faz 3 tablosuna hazır olsun: `kac_ev.csv` gelince karamsar–iyimser, renk, %40 kuralı, "ölçülmedi" etiketi (`olculdu` = 0) ve "aday yok" durumu (`kac_ev_aday` = 0 → "panelsiz konut yok"). (4) Faz 4 sınavı: internet kapalıyken açılış denemesi (OSM zemini var), 2 dakikalık ekran kaydı, 3 şehir seçimi, Mac denemesi (karar masası yaptı, günlüğüne yaz), yan panel sayıları 3 trafoda elle kontrol. (5) Zaman kalırsa kıyı çizgisini zemine çiz, OSM alanını genişlet. Sunumda canlı gösteriyi sen yapacaksın; akış için Can'ın `docs/sunum/` iskeletine bak.
Neden: Sunum yarın; harita jürinin tıklayacağı şey, Faz 3 tablosu gelir gelmez bağlanmalı.
Senden beklenen: yukarıdaki sıra; takılırsan kutu.
Durum: sürüyor — 1 ve 2 yapıldı 16:58; 3–5 sırada

## UYARI! 31 Eki 17:03 — Volkan'dan (BUILD oturumu) — PR #12: sözleşme 1.2 onayı; kıyı kodun üreticide
Ne: PR #12 (https://github.com/volkanGRGN/KKTC-hackathon/pull/12) sözleşme 1.2: `yillik_tuketim_mwh` (sahte üreticine ekleyebilirsin), 800–899 kuralı (`veri_turu` = `gercek`, `veri_kaynagi`; senin etiket dalınla aynı), `v0_v` 244–252, `ayar.json` bilgi anahtarları (`kiyi_kontrolu` senin gibi true/false). Sözleşme kısmını onaylayabilirsin (ya da Can). `kiyi_segmentleri()` ve `karada()` aynen ve atıfla `src/sehir_uret.py`'de; 20 yeni şehirde denizde trafo 0/800. `girne_kiyi.json`'u 16:24'te aynı komutla yeniden indirdim: OSM zaman damgası 2026-10-31T14:24:14Z, 25 yol, 2.141 nokta (seninkiyle aynı). İstersen KAYNAK.txt'ye bu satırı ekle (senin dosyan).
Dosya: docs/data/tablo-bicimi.md (PR #12)
Neden: sözleşme değişikliği Can ya da Civan onayı ister.
Durum: yapıldı (PR #12 Civan onayı GitHub'da, 31 Eki 17:08)
