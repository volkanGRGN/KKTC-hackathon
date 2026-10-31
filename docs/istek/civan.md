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

## KARAR 17:32 — volkan.md'deki "sunum dashboard'un içinde olsun mu?" isteğine (Volkan karar verdi)
Karar: (a) **Evet, sunum haritanın içinde** senin 7 ekranınla; aynı metinden PDF yedeği (Can, docs/sunum). (b) Blender animasyonu **yok**; onun yerine Volkan'ın geçiş fikri, veriden ve ucuz: **"noktalar çoğalıyor"** animasyonu, 3. ekrandan (fikrimiz) 5. ekrana (canlı harita) geçiş. Kurgu (Volkan'ın eskizi): adanın sade bir hat çizimi; önce tek bir trafo ölçülüyor, haritada **bir** nokta beliriyor; sonra ikinci, sonra ortada üçüncü; ardından tahmin yavaşça yayılıyor, bütün mahallelerde noktalar çoğalıyor ve harita dolu hale geliyor; son karede canlı haritaya geçiliyor.
Dürüstlük kuralları (görselde): ölçülen trafo **dolu/kalın** nokta, tahmin edilen **içi boş ya da soluk** nokta; yayılan noktalar tek renk yeşil değil, Faz 3 renkleriyle (yeşil / sarı / kırmızı) çıksın, yoksa "hepsini ölçtük, hepsi yeşil" anlaşılır; köşede "gösterim — farazi şehir" etiketi; ada geneli noktalar temsilidir, gerçek trafo yeri değil.
Uygulama (ucuz, ≤ 1 saat, iş sırası 4–5'ten sonra): Streamlit'te bir ekran, `st.empty()` + zamanlı döngü ya da kaydırıcı; veri gerçek `sehir-001` tablolarından (12 ölçülü → 40 trafo, `olculdu` ve `renk` sütunları); ada hat çizimi için OSM KKTC sınırı (KAYNAK.txt'ye adres) ya da sade SVG; adaya yayılma adımında farazi 20 şehrin noktaları adanın kasabalarına temsili dağıtılır [Yorum, gösterim]. Olmazsa yedek: Can `grafikler.py` ile 4 kare PNG üretir, ekranda sırayla gösterilir. Dosyalar senin (app/), metin Can'ın.
Neden: Tek görsel "birkaçını ölç, gerisini tahmin et" fikrini kelimesiz anlatıyor; Blender zaman yer ve veriye bağlı değil.
Senden beklenen: önce 4–5 (yan panel, internetsiz, ekran kaydı), sonra bu ekran; Can'la 3. ve 5. ekran metnini eşle.
Durum: yapıldı 21:40: `app/pages/noktalar_cogaliyor.py` + `app/animasyon.py` + `app/animasyon.html` (Streamlit içinde HTML/SVG, pop 0 → %115 → %100, 0,35 sn; ölçülen dolu, tahmin soluk halka; Faz 3 renkleri; köşede "gösterim — farazi şehir · noktalar temsili"). sehir-001 Girne'de 3 + 9 ölçülü, 28 tahmin; sonra ada: 20 şehir, 800 trafo, 240 ölçülü, 560 tahmin. Ada çizimi Natural Earth 1:50m (kamu malı, app/ada_kiyi.json). Can'la 3. ve 5. ekran metni eşlenmedi; ekran başlıkları animasyon.html ADIMLAR'da

## EK 17:33 — "noktalar çoğalıyor" animasyonuna Volkan'ın notu: noktalar **pop** ile belirsin
Ne: Her nokta sıfırdan büyüyüp hafif taşıp yerine otursun (pop/bounce), fade değil. Ölçülen trafo tek tek pop (ses yok, 0,3–0,4 sn), tahmin yayılırken noktalar küçük gruplar hâlinde art arda pop (kademeli, dalga gibi). Uygulama önerisi [Yorum]: pydeck'te `ScatterplotLayer` + `transitions={'getRadius': 350}` ile yarıçapı 0 → R, her karede birkaç nokta ekleyerek; ya da `st.components.v1.html` içinde CSS keyframes (scale 0 → 1,15 → 1) ile daha pürüzsüz. Hangisi 20 dakikada çalışıyorsa o.
Senden beklenen: animasyon ekranında bu geçiş; öncelik sırası aynı (önce 4–5).
Durum: bilgi

## KARAR 18:46 — volkan.md'deki "dashboard'da şebeke doluluğu nasıl hesaplansın?" isteğine
Karar: Tek bir "şebeke doluluğu" sayısı yok; sayfa **üç kutu** gösterir, hepsi sözleşme sütunlarından, cevap anahtarı yok:
1. **Trafo renk dağılımı:** yeşil / sarı / kırmızı adet ve yüzde (`kac_ev.csv` `renk`), yanında kaç trafonun ölçülü olduğu (`tahmin.csv` `olculdu`). Manşet bu.
2. **Kaç ev daha sığar, şehir toplamı:** Σ `kac_ev_karamsar` – Σ `kac_ev_iyimser` aralığı ("en az … en çok … ev"); yanında bugünkü %40 kuralının toplamı Σ `kural40_ev` (ürünün kilit kıyası). Sözleşme 1.3 gelirse ortadaki sayı Σ `kac_ev_orta`.
3. **Panel payının dolu kısmı** (asıl "doluluk", ADR-0002): pay = max(0, min(`isil_pay_kw`, `gerilim_pay_kw_karamsar`)) ve iyimseri; doluluk = Σ `panel_kw` ÷ Σ (`panel_kw` + pay); karamsar ve iyimser iki yüzde ("güneş payının %x'i dolu"). `panel_kw` `trafolar.csv`'den.
(a) "öğlen yük ÷ kVA" doluluk **değil**: öğlen yükü düşük trafo panel için daha riskli, sayı "boş" gösterir; istersen küçük yazıyla "öğlen en düşük yük ÷ trafo gücü" diye ayrı, "doluluk" demeden. (c) kWh ile kW karışır, yok.
Neden: Ürün triyaj (ADR-0005): soru "kaç ev daha" ve "hangi renk", kVA doluluğu değil; üç kutu kilit grafikle aynı dili konuşuyor; ek hesap yok.
Senden beklenen: sayfa ≤ 45 dk, öncelik aynı (önce 4–5, sonra animasyon, sonra bu); rakam etiketi "gösterim — farazi şehir". Aynı soru can.md'de de vardı; Can'dan ayrıca cevap gelmeyecek.
Durum: bekliyor

## BİLGİ 18:46 — karar masasından — Faz 3 hesabı olasılıklıya geçiyor (ADR-0011); panelin değişmesi gerekmiyor
Ne: `kac_ev.csv`'nin sütun adları ve yeri aynı kalıyor (karamsar / iyimser / renk), üç ek sütun geliyor: `p_bugun_asar` (bugün sınırı aşma olasılığı), `p_iki_ev_sigar`, `kac_ev_orta`. BUILD yazar; sözleşme 1.3 notu senin ya da Can'ın onayına gelir (PR). Yan panel olduğu gibi çalışır; zaman kalırsa "bugün aşma olasılığı %x" ve orta sayı yan panele. Yeşil artık konut trafolarında da çıkıyor (sınavda yeşil %25); animasyonda renk karışımı doğal olur.
Senden beklenen: PR onayı gelince bak; başka iş yok.
Durum: bilgi

## KARAR 19:13 — yan panelde ve dashboard'da kaç ev sayısının dili: "en az" yok, "yaklaşık N ev (A–B)"
Karar: Can'ın ölçümü: olasılıklı hesapta karamsar sayı (çekilişlerin P10'u) trafoların %15'inde gerçeğin üstünde; yani taban değil, %80 bandın alt ucu. Bu yüzden:
- Yan panel: manşet `kac_ev_orta` ("yaklaşık 4 ev"), yanında "(2–7)" = `kac_ev_karamsar`–`kac_ev_iyimser`; küçük yazı "%80 ihtimalle". `kac_ev_orta` sütunu gelene kadar yalnız "2–7 ev". **"En az" kelimesi hiçbir ekranda yok.**
- Renk cümlesi: yeşil → "ilk 2 başvuru güvenle sığar (≥ %98)"; sarı → "önce ölç"; kırmızı → "ölç ya da güçlendir". Vaat renkte, sayıda değil.
- Dashboard 2. kutu (18:46 kararı düzeltildi): "en az … en çok" değil, "büyük olasılıkla toplam A–B ev" (Σ karamsar – Σ iyimser), ortası varsa "yaklaşık N".
Neden: ADR-0010'un vaadi yeşil kuralında (%98), sayıda değil; P10 "en az" diye yazılırsa trafoların %15'inde yanlış yönde söz vermiş oluruz.
Senden beklenen: metin değişikliği, ≤ 15 dk; öncelik sırası aynı.
Durum: yapıldı 21:26 (20:56 kararıyla birlikte; app/harita.py)

## KONTROL 20:55 — BUILD'den (Mac) — Faz 4 sınavı, Mac kısmı (karar masası 20:47)
Ne ölçüldü: main'deki `app/` (son değişikliğin 17:28), Mac, Python 3.12, streamlit 1.66.1, pydeck 0.9.3. Şehirler sehir-001, -011, -020 (olasılıklı `kac_ev.csv`, sözleşme 1.3). BUILD `app/`'e dokunmadı.
- **+ Sayılar tabloyla birebir.** 6 trafo: 001 T16, T37, T18; 011 T27; 020 T33, T24. Renk, kaç ev aralığı, %40 kuralı, sınırı belirleyen, kVA / bölge / montaj / abone / panel, ölçüldü / güven, öğlen yükü bandı `kac_ev.csv`, `trafolar.csv`, `tahmin.csv` ile aynı. Renk sayıları üç şehirde de aynı (001: 13 / 22 / 5; 011: 15 / 25 / 0; 020: 13 / 27 / 0).
- **+ Tıklama hızlı.** 6 tıklamada yan panel 351–399 ms'de açıldı (sınır 1 sn). 40 trafonun hepsi denenmedi.
- **+ 3 şehir seçilebiliyor;** "örnek veri (farazi şehir) — gösterim" her şehirde.
- **+ İnternetsiz.** OSM zemin dosyası varken sayfa 98 isteğin 98'ini localhost'tan aldı, dışarıya istek yok. Ağ fiilen kapatılmadı. **Dikkat:** `data/raw/osm-kasaba/girne_merkez.json` depoda yok (gitignore). Sunum bilgisayarında önceden indirilmiş olmalı, yoksa zemin internetten gelir. BUILD KAYNAK.txt'deki komutla indirdi: 1.304 öğe, senin sağlamanla aynı.
- **− Dil 19:13 kararına göre değil** (KARAR 19:13 hâlâ "bekliyor"):
  - kaç ev "16–17 ev" diye yazıyor; manşet `kac_ev_orta` yok. Olmalı: "yaklaşık 17 ev (16–17)", küçük yazı "%80 ihtimalle";
  - yeşil cümlesi "En kötü durumda bile yer var". Olmalı: "İlk 2 başvuru güvenle sığar (≥ %98)";
  - %40 karşılaştırma metinleri ("en kötü durumdan bile az", "en iyimser tahminimizden fazla") karamsar ve iyimseri taban ve tavan gibi okuyor. Öneri: "aralığımızın altında / üstünde";
  - sütun boyu karamsar sayı; orta sayı önerilir (karar masasının).
- **− %40 kuralının ev sayısı, panel takabilecek evden fazla çıkabiliyor.** `kural40_ev` = kalan kW payı ÷ 6,5 (sözleşme §6); panelsiz konut sayısıyla kesilmiyor.
  - Örnek sehir-001 T30: 400 kVA, 15 konut abonesi, 2'si panelli, yani aday 13. Panel "Bugünkü kural (%40): 23 ev — en iyimser tahminimizden fazla" diyor; bizim aralık 10–13.
  - 20 şehirde aday > 0 olan 701 trafonun 241'inde kuralın sayısı aday evden fazla [Hesap].
  - Doğru cümle: "kural panelsiz 13 evin hepsine izin veriyor (23 evlik yer)".
  - BUILD önerisi: sözleşme ve sınav değişmeden, panelde min(`kural40_ev`, aday) göster; aşıyorsa "hepsine izin veriyor (N evlik yer)". Sınavın %40 ölçüsü (`kural40_ev` ≥ 1) etkilenmez.
- **? Denenmedi:** Windows, 2 dakikalık ekran kaydı, 40 trafonun hepsi, ağ fiilen kapalıyken açılış.
Dosya: app/harita.py (senin)
Neden: ROADMAP Faz 4 geçme sınavı, karar masası 20:47 (2). Bloklamıyor; dil ve %40 cümlesi sunumda görünen yer.
Durum: dil ve %40 bulguları yapıldı 21:26 (KARAR 20:56); Windows, ekran kaydı, ağ kapalı açılış sırada

## KARAR 20:56 — BUILD'in 20:55 kontrolündeki iki bulgu: %40 kuralının ev sayısı ve panel dili
Karar: (1) **%40 kuralının ev sayısı panelde aday evle kesilir:** gösterilen = min(`kural40_ev`, aday); aday = `abone_konut` − `panel_sayisi` (`trafolar.csv`). Kural sayısı adayı aşıyorsa cümle: "Bugünkü kural panelsiz N evin hepsine izin veriyor (M evlik yer)". Sözleşme §6 ve sınav değişmez (`kural40_ev` olduğu gibi kalır; sınav yalnız ≥ 1'e bakar). (2) **Dil 19:13 kararı aynen, bu gece:** manşet "yaklaşık N ev (A–B)" + küçük yazı "%80 ihtimalle"; yeşilde "İlk 2 başvuru güvenle sığar (≥ %98)"; sarıda "önce ölç"; kırmızıda "ölç ya da güçlendir"; %40 karşılaştırmasında "aralığımızın altında / içinde / üstünde" (taban–tavan dili yok); sütun boyu `kac_ev_orta`. (3) Sunum bilgisayarında zemin dosyası (`data/raw/osm-kasaba/girne_merkez.json`) önceden indirilmiş olsun; README'de bir satır. (4) Kalan sınav maddeleri senin: Windows'ta açılış, 2 dakikalık ekran kaydı, ağ fiilen kapalıyken açılış; sonucu kutuya.
Neden: 241/701 trafoda kuralın ev sayısı panel takabilecek evden fazla; ekranda "23 ev" yazınca jüri kuralı olduğundan cömert okur, kıyas bozulur. Dil kararı 19:13'ten beri bekliyor ve sunumda görünen yer.
Senden beklenen: (1) ve (2) ≤ 30 dk, önce bunlar; sonra (4). Takılırsan kutuya yaz.
Durum: (1) ve (2) yapıldı 21:26: kural sayısı min(kural40_ev, aday), aşınca "panelsiz N evin hepsine izin veriyor (M evlik yer)" (sehir-001 T30: 13 / 23, aralık 10–13); manşet "yaklaşık N ev (A–B)" + "%80 ihtimalle"; renk cümleleri; "aralığımızın altında / içinde / üstünde"; sütun boyu kac_ev_orta. Tarayıcıda T30 ve T39 bakıldı. (3) yapıldı 21:29 (app/README.md "Sunum bilgisayarı" satırı). (4) Windows yapıldı 21:29 (volkan.md KONTROL 21:29); ağ kapalı açılış ve ekran kaydı ertelendi (kontrol katmanı; sunum yerinde internet ve elektrik var, sonra yapılacak)

## KARAR 21:16 — volkan.md'deki "ada veri setleri" (21:20) isteğine
Karar: İyi bulgu; bu gece rakam değişmez. (a) **Evet:** Kotsonias iletken tablosu üretici 1.3'e "ince uç kol (16–22 mm², Rac 1,23–1,91 Ω/km)" senaryosu olarak ve olasılıklı hesabın kol çekilişine (ADR-0011 kol yapısı, ince iletkenle) girer; ROADMAP üretici 1.3 satırı BUILD'de. Uzmana soru 3'e not: "Kıb-Tek uç kollarda hangi kesit?" [Kaynaklı: Kotsonias vd. 2019, Zenodo, CC BY 4.0]. (b) **Sözlük vekili sunum sonrası:** "Kuzey trafo sayısı ~6.400–6.700 (Güney + Korsika vekili)" satırı ve KAYNAK Can'ın (veri sözlüğü onun dosyası), yarından sonra; ekran 6'daki "120–170 trafo" bu gece değişmez (kaynağı araştırma günlüğü §7; iki vekil birlikte sunum sonrası günlüğe). (c) **Evet:** DEVIR / ROADMAP "dış veri istekleri" listesine KIOS yazarları (hat modeli + EAC 60 tüketici) ve Micallef 2015 tezi ("Request a copy", Gozo hat boyu / kablo); mesajı Volkan yazar, ekip yazmaz.
Neden: Kol yapısı İngiltere geri-testinde kaçan hattın sebebiydi; Kıbrıs'tan gerçek iletken tablosu tam o boşluğu dolduruyor. Sunum gecesi rakam ve etiket oynatılmaz (karar masası 20:47).
Senden beklenen: **önce 20:56 KARAR** (panel dili, %40 kuralının ev sayısı; sunumda görünen yer), sonra Windows / ekran kaydı. Bu araştırma için bu gece iş yok.
Durum: bekliyor

## KARAR 21:39 — ertelemeler kalktı (Volkan): sözlük vekili ve Micallef isteği senin, Faz 4 işlerinden sonra
Karar: 21:16'daki "sunum sonrası" ertelemesi kalkıyor. Faz 4 (ağ kapalı açılış, ekran kaydı) bitince: (1) veri sözlüğüne "Kuzey trafo sayısı ~6.400–6.700 (Güney + Korsika vekili)" satırı ve `data/raw/edf-sei-corse/KAYNAK.txt` (sen yazarsın, Can onaylar; sözlük Can'ın dosyası olduğu için PR ya da Can'a satır); (2) Micallef 2015 tezi için "request a copy" ve KIOS yazarları için istek **metinlerini** hazırla (ne istiyoruz, ne için, lisans), `docs/istek/dis-veri-istekleri-taslak.md`; gönderen Volkan. (3) Veri araştırma kartın (docs/gorev/civan-veri-arastirma.md) aynen; bulunca kutuya parti olarak.
Neden: Volkan "sunuma daha var, dediklerimizi uygulayalım"; Gozo dış sınaması ve Korsika vekili fazlara geri alındı (volkan.md 21:39).
Senden beklenen: Faz 4 → (1) → (2); başka iş yok.
Durum: bekliyor

## BAŞLA 21:41 — Volkan: herkes kendi fazına başlasın
Ne: Senin sıran: (1) **Faz 4 kalan iki madde**: internet fiilen kapalıyken açılış ve 2 dakikalık ekran kaydı (KONTROL 20:55; bitince ROADMAP Faz 4 kutuları için BUILD'e satır); (2) sözlük vekili + Korsika KAYNAK ve dış veri istek metinleri (KARAR 21:4x); (3) arkada veri araştırması, kartın [docs/gorev/civan-veri-arastirma.md](../gorev/civan-veri-arastirma.md): her bulgu tüzükteki alanlarla kutuya "veri partisi". Faz 7–8'de sana kod işi yok; Faz 11 kart görünümü Faz 4 bitince. Takılırsan kutu; bloklarsa Volkan'ı ara.
Durum: bilgi
