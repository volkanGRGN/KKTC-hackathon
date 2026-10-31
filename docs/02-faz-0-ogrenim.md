# Faz 0 — Öğrenim: projeyi sıfırdan anlamak

Kime: ekibin üç üyesi. Süre: 1–1,5 saat okuma + 15 dakika uygulama. Bitince aşağıdaki sorulara kendi cümlelerinle cevap verebiliyorsun; kimseye bir şey ezberletmiyoruz, her adımda "neden" var.

## 1. Sorun, üç cümlede

- Kuzey Kıbrıs'ta ~2.670 çatı güneş paneli başvurusu bekliyor, çünkü Kıb-Tek bir mahalle trafosuna kaç panel daha sığdığını bilmiyor: trafonun gerçek yükünü ve hattın ucundaki gerilimi ölçen bir sistemi yok.
- Güney Kıbrıs tersini yaptı, panelleri bağladı; 2025'te ürettikleri güneşin %47'sini şebekeye sığmadığı için attı.
- Biz, trafoların küçük bir kısmını ölçüp gerisini tahmin eden ve her trafo için "öğlen ne kadar dolu, kaç ev daha panel takabilir, ne kadar eminiz" diyen bir araç yapıyoruz. İngiltere bunu 2011–2014'te 800 trafoyla yaptı ve %80 isabet aldı.

## 2. Öğrenme sırası

Her adımda: ne, neden önemli, nereden okunur, kendine soracağın soru.

**Adım 1 — Elektrik eve nasıl gelir.** Santral → yüksek gerilim hattı → ana indirici merkez → orta gerilim → **mahalle trafosu** → alçak gerilim hattı → ev. Mahalle trafosu direkte küçük (25–400 kVA) ya da yerde büyük (50–2.500 kVA) olur; kVA taşıyabileceği güçtür. Oku: [sözlük](glossary.md) ilk 5 satır.
Soru: *Kıb-Tek bir trafo hakkında neyi biliyor, neyi bilmiyor?* (Gücünü ve bağlı panel toplamını biliyor; gerçek yükünü ve hat ucu gerilimini görmüyor.)

**Adım 2 — Panel neden sığmaz.** İki sınır var. Isıl sınır: trafo fazla güç taşırsa ısınır. Gerilim sınırı: panel şebekeye elektrik verince hattın ucundaki evde gerilim yükselir; Kıbrıs'ta trafo boşta 250 V veriyor, panelin cihazı (inverter) 264 V'ta kendini kapatıyor; arada yalnız 14 V var. (Benzetimimizde trafo çıkışı 246–247 V alındı, yani benzetim gerçeğe göre biraz iyimser; Faz 1'de 246–250 arası rastgele olacak.) Kıbrıs gibi küçük, dışarıya bağlantısız, uzun köy hatlı adalarda **önce gerilim dolar**. Bir de "faz" var: hattaki üç telden biri; paneller aynı tele yığılırsa gerilim altı kat hızlı yükselir. Kıb-Tek'in bugünkü kuralı ise yalnız güce bakıyor: panel toplamı trafo gücünün %40'ını geçmesin. Oku: [ADR-0002](decisions/adr-0002-gerilim-ilk-surumde.md).
Soru: *%40 kuralı neden dolu bir trafoya "yer var" diyebilir?*

**Adım 3 — Öğlen en düşük yük.** Güneş öğlen üretir; trafo o saatte ne kadar az elektrik çekiyorsa panelin fazlası o kadar az yer bulur. En tehlikeli an bahar öğleni: klima yok, güneş güçlü. Bu yüzden bizim tahmin etmek istediğimiz şey akşam tepesi değil, bahar öğlenindeki en düşük yük. Oku: [yöntem](method/modeling.md) bölüm 3.
Soru: *Neden akşam tepesi değil, öğlen?*

**Adım 4 — Şablon yöntemi (İngiltere).** Dört adım: birkaç trafoyu ölç → günlük eğrisi benzeyenleri grupla (şekil) → ölçülmeyen trafoyu abone karışımına bakıp bir gruba koy → abone sayısıyla büyüt (büyüklük). Evler akşam, dükkânlar öğlen, sanayi gün boyu düz çeker; şekli abone karışımı belirler. **Tipler önceden bilinmez, ölçümden çıkar**; İngiltere'de 10 çıktı, bizim tahminimiz Kıbrıs'ta ~7. %80 rakamı yöntemin İngiltere'nin kendi içindeki isabeti; İngiltere verisinin Kıbrıs'a benzerliği değil. Oku: [ADR-0001](decisions/adr-0001-sekil-buyukluk-sablon.md), [araştırma günlüğü bölüm 6](log/2026-10-31-kapsamli-arastirma.md).
Soru: *"%80" ne demek, ne demek değil?*

**Adım 5 — Kaç trafo ölçülür, ölçme nerede durur.** Tipleri bilmeden seçim, tipleri tahmin ettiren ipuçlarıyla yapılır: abone karışımı, büyüklük, direk/yer, şehir/köy/turistik/sanayi, panel sayısı. İlk turda her yönden çeşitli 20–50 trafo; sonra tur tur: az örneği kalan tipe ve sistemin "emin değilim" dediği trafoya. Durma: her tipte 5–10 ölçülü trafo var, yeni ölçümler sürpriz çıkarmıyor, hata hedefin altında. Bütün Kuzey için kaba hesap 120–170 trafo (%2–2,6). Oku: [doğrulama](method/validation.md) "temsil yanlılığı".
Soru: *Tek bir mahalleyi ölçmek neden yetmez?*

**Adım 6 — Doğrulama ve dürüstlük.** Sınav trafo bazında yapılır: bir trafo hiç ölçülmemiş gibi tahmin edilir, gerçeğiyle karşılaştırılır, her trafo için tekrar. Sınav asla yalnız farazi veriyle yapılmaz. Sonuç tek sayı değil bant ("3–7 ev") ve güven etiketi. En pahalı hata **yanlış yeşil**: dolu trafoya "yer var" demek. Oku: [doğrulama](method/validation.md), [ADR-0003](decisions/adr-0003-rastgele-farazi-sehirler.md).
Soru: *Farazi şehirde çıkan %90 isabet ne anlama gelir?* (Yöntem çalışıyor; Kıbrıs'taki doğruluk hakkında hiçbir şey söylemiyor.)

**Adım 7 — Araç ne yapar, ne yapmaz.** Haritada her trafo bir sütun: boyu doluluk, rengi karar. Yeşil → hızlı onay, kırmızı → işaret, sarı ya da düşük güven → **ret değil, ölçüm cihazı tak**. Son karar insanın; itiraz eden gerçek ölçüm isteyebilir. Oku: [ADR-0005](decisions/adr-0005-triyaj-ret-degil.md).
Soru: *Araç bir başvuruyu reddeder mi?*

**Adım 8 — Farazi şehir neden ve nasıl.** Gerçek Kıbrıs trafo ölçümü elimizde yok; hackathon kaynağı belli benzetim verisine izin veriyor. Tüketim eğrileri Güney Kıbrıs'ın 2022'de gerçek sayaçlarla ölçtüğü resmi eğriler; şebeke ölçüleri Almanya'nın açık veri setinden; güneş Lefkoşa'nın gerçek verisi. Tek şehir değil 20–30 şehir, çünkü tek şehirde model şehri değil bizim varsayımlarımızı öğrenir. Oku: [ADR-0004](decisions/adr-0004-veri-eac-profil-siniflari.md), [veri sözlüğü](data/data-dictionary.md).
Soru: *Güney'in verisini kullanmanın zararı var mı?* (Yok; "gösterim" diye etiketlendiği ve kanıt diye sunulmadığı sürece.)

## 3. Projede neler var — okuma sırası

1. [README](../README.md) — 5 dakika, ön kapı.
2. [Genel bakış](00-overview.md) — amaç, kapsam dışı, başarı ölçütü.
3. [Sözlük](glossary.md) — takılınca dön.
4. [Kararlar](decisions/) — ADR-0001'den 0005'e; "neden böyle" burada.
5. [Plan](01-plan.md) — iş kolları ve takvim.
6. [Yöntem](method/modeling.md) ve [doğrulama](method/validation.md).
7. [Veri sözlüğü](data/data-dictionary.md).
8. [Kapsamlı araştırma](log/2026-10-31-kapsamli-arastirma.md) — uzun; kaynak lazım olunca.
9. [Benzetim kodu](../src/trafo_bos_kapasite.py) — kodu okumak şart değil. Dosya önceki bir fikir için yazıldı; baştaki açıklama, bu projede hangi kısmının kullanıldığını söylüyor.

## 4. Uygulama (15 dakika)

1. Depoyu klonla, benzetimi çalıştır:
   ```bash
   python3 src/trafo_bos_kapasite.py 7 cikti.json
   ```
   2 saniyede üç trafonun sonucu gelir. `bugunku_tepe_v` alanına bak: T1 Kıyı 261 V, yani bugün bile sınırın üstünde; `kural_payi_kw` ise %40 kuralının hâlâ "yer var" dediği güç. İkisini yan yana gör: Adım 2'nin cevabı bu.
2. Güney'in eğrilerini `data/raw/eac-profil-siniflari/KAYNAK.txt` adresinden indir; Excel'de DOMESTIC ve otel sayfasını (adı yanlış yazılmış: `L._COMM._STORES`) aç; Nisan iş günü sütununda öğlen 12:00 ile akşam 21:00 değerini karşılaştır. Evin öğlen yükü akşamın ~%70'i; otelinki yazın kışın 4 katı. Adım 3 ve 4'ün cevabı bu.
3. [CONTRIBUTING](../CONTRIBUTING.md) oku; bir dal açıp küçük bir değişiklikle PR açmayı dene (ör. sözlüğe bir terim).

## 5. Ne yapacağız

Fazlar [yol haritasında](../ROADMAP.md). Faz 1 ve sonrasını Volkan yazacak; şimdilik yalnız bu fazı çalışın. Ayrıntılı iş kolları ve takvim [planda](01-plan.md).

## 6. Faz 0 bitti sayılması için

- [ ] 8 soruya kendi cümlelerinle cevap verebiliyorsun.
- [ ] Benzetimi çalıştırdın, T1'in 261 V'unu gördün.
- [ ] EAC verisini indirdin, ev ve otel eğrisine baktın.
- [ ] Bir dal açıp PR açmayı biliyorsun.
