# Volkan — Faz 9 / 11 — Kıb-Tek tepe verisi (veri partisi kartı)
Amaç (1 cümle): Kıb-Tek'ten trafo tepe kayıtları ve OG fider tepesi gelince yük haritasına (`src/tepe.py`) tüzüğe uygun girsin: kayıtlı trafo kendi kaydına otursun, popülasyon ve bant sürümlü yeniden-fitle değişsin, fider aşağıdan yukarı toplamı sınasın.

```
Tüzük: geçerli (docs/tuzuk.md)
Parti kimliği: P9-kibtek-tepe-<gelis tarihi>
Kaynak ve çekim tarihi: Kıb-Tek (docs/istek/kibtek-veri-istegi-taslak.md madde 7–10); data/raw/kibtek-tepe/KAYNAK.txt, SHA-256 veri gelince
Kapsam: MD göstergesi olan trafolar (beklenen: yer tipi ağırlıklı; temsilî değil), yaz yük etüdü örneklemi,
   OG fider / merkez SCADA tepe geçmişi; gözlem penceresi en az bir yaz (Haziran–Eylül); eksik: direk tipi trafoların çoğu
Veri sözleşmesi: kibtek_tepe.csv, kibtek_fider.csv (docs/data/tablo-bicimi.md §9); kW ya da A (en yüklü faz);
   saat dilimi Europe/Nicosia; boş zaman = MD (sezon tepesi). Bilinen yanlılık: MD büyük trafoda; eski / sıfırlanmamış
   MD az gösterir; etüt tek okuma (tepe değil); fider tepesi kayıplı ve trafo listesi Kıb-Tek'in eşleşmesine bağlı
Kullanım bölünmesi (DONDURULACAK <tarih saat>, değer görülmeden): kayıtlı trafolar trafo no karmasıyla ikiye:
   ayar = yarısı (popülasyon R ve bant yeniden-fit), doğrulama = yarısı (dokunulmaz; tepe bandının kapsaması);
   fiderler bölünmez (kontrol, fit girdisi değil)
Hipotez ve beklenen etki: kayıtlı trafoda tahmin kayda çöker; kayıtsız trafoda değişmez, popülasyon R'si ve bant
   yalnız sürümlü yeniden-fitle; fider mutabakatı aşağıdan yukarı toplamı ±%15 içinde tutar
Kapılar: (1) doğrulama trafolarında gerçeğin P90 tepenin üstünde payı ≤ %10 (yük tarafının yanlış yeşili: "yük için
   boş" dediğimiz kVA gerçekte yok); (2) %80 bant kapsama %70–90; sonra hata ortancası ve P90
Sürüm: tepe ön v0 (PR #24) → v1 (yaz kayıtlarıyla yeniden-fit); ebeveyn v0
```

Girdi: Kıb-Tek kayıtları §9 biçiminde, şehir (bölge) klasörüne; Open-Meteo Lefkoşa saatlik dosyası kayıt yılı için.
Çıktı: `tepe.csv` (`tepe_kaynagi` = `kayit_md` / `kayit_etut`), `tepe_ozet.json` `kibtek` bölümü (kayıt R'leri, yeniden-fit önerisi, fider tablosu).

Adımlar:
1. Kaydı §9'a çevir (A → kW notu), KAYNAK.txt + SHA-256, kullanım bölünmesini veri açılmadan yaz ve dondur.
2. `python3 src/tepe.py <kök>`: ayar payıyla koş; `tepe_ozet.json` `yeniden_fit_onerisi` (MD R ortancası ↔ Nisan R; bant P10 / P90) ve fider oranları.
3. Yeniden-fit kararı KARAR'da (sürüm v1): popülasyon R'si montaj tipi içinde mi, bant kayıt artıklarından mı. Sonra doğrulama payında kapılar bir kez; hold-out defterine satır.
4. Fider oranı |ln| > 0,15 olan fiderde eşleşme (abone → trafo → fider) ve kayıp önce kontrol edilir; model düzeltilmez.

Nasıl denenir (bugün, sahte kayıtla): `python3 src/sahte_tepe_kaydi.py <kök> --aralik 1-10` sonra `python3 src/tepe.py <kök> --aralik 1-10`. Beklenen (üretici 1.4, şehir 1–10): MD kaydı olan 83 trafoda hata ortanca %3,7, gerçek P90 üstünde 0; kayıtsız trafolar kayıtsız koşuyla birebir; fider kayıt ÷ tahmin ortanca 1,00 (P10 0,91, P90 1,14).

Bitti sayılması için: (1) kayıtlı doğrulama trafolarında P90 üstü ≤ %10; (2) %80 bant %70–90; (3) fider tablosu günlükte; (4) sürüm v1 ADR'si ya da "yeniden-fit yok" kararı.
Dokunulmayacak dosyalar: `src/sinav.py`, `src/profiller.py`, `src/grafikler.py` (Can), `app/` (Civan); cevap anahtarı.
Kendin karar ver (sorma, günlüğe yaz): A → kW dönüşümü, eksik / bozuk satırın atılması (sayıyla).
Karar masasına yaz (volkan.md, bekleme, sıradaki işe geç): popülasyon R'si ve bant yeniden-fiti (sürüm), `--fider-duzelt`'in açılması.
Takılırsan: önce sahte kayıtla aynı komutu koş (kod mu veri mi); sonra istek kutusu.

**Pilotta ölçüm cihazı net ölçer (KARAR 00:57 madde 3):** trafo başındaki cihaz brüt tüketimi değil trafodan geçen net yükü görür (tüketim − o trafodaki panellerin üretimi). `sablon.py` ölçülü trafodan brüt (`tuketim_kw`) okuyor, `tepe.py` net (`net_kw`) okuyor. Gerçek ölçümde öğlen hesabı için ölçülünün üretimi geri eklenir: panel kW (Kıb-Tek kaydı) × o günün ışınımı (Open-Meteo) × PR; bunun hatası (yön, gölge, kirlilik, inverter kapanması) ölçülmedi. Akşam tepesi güneş battıktan sonra olduğu için orada fark küçük. Faz 10 pilot kartında ölçüm sırası buna göre: panelli ölçülü trafoda ayrıca bir inverter kaydı (PR #19 okuyucusu) üretimi ölçer.

Sahte kayıtla ölçülen (1 Kasım, [günlük](../log/2026-11-01-volkan-yuk-kibtek-tepe.md)) [Hesap; farazi, gösterim]: kayıtlardan popülasyona doğrudan aktarım tahmini −%2 / −%4 kaydırdı (güvensiz yön; MD büyük trafoda), fider oranıyla yukarıdan aşağı düzeltme hatayı %6 → %13 artırdı; ikisi de kapalı, karar sürümlü yeniden-fitte.
