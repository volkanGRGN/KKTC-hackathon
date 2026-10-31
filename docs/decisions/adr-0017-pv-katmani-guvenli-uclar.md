# ADR-0017: Panel katmanı "güvenli uçlar" olarak gösterilir — kesin yeşil azınlık, "büyük olasılıkla dolu" bayrağı, arası renksiz ("başvuruda bakılır")

Tarih: 2026-11-01 · Durum: kabul · ADR-0010, ADR-0011, ADR-0012, ADR-0015, ADR-0016 üstüne · kaynak: Muhittin'in dördüncü cevabı madde 1 ([günlük](../log/2026-10-31-muhittin-cevap-4-odak-tepe-kademe.md)) · karar masası 1 Kasım 00:25

## Bağlam
Panel haritası bugün üç renk: yeşil (`p_iki_ev_sigar` ≥ 0,98 ve yük güveni yüksek; ADR-0010), kırmızı (`p_bugun_asar` ≥ 0,5; ADR-0011), arası sarı. Gerçekçi şehirlerde (üretici 1.3) kapılar tutuyor ama kırmızının yarısında yer var (ADR-0016 bunu kalibrasyon ölçüsü olarak kabul etti). Muhittin: PV haritası bugünkü hâliyle bir **kapasite haritası** diye okunursa zarar verir; yer olan trafoya "dolu" demek Kıb-Tek'in güvenini yakar. PV'nin güvenilir yaptığı tek şey asla yanlış yeşil dememek; belirsiz kısım renklendirilmemeli, başvuruda bakılmalı.

Aynı eşiklerle ölçüm (aday evi olan trafolar; üretici 1.3, K_YUK 1,47) [Hesap: karar masası 00:20, BUILD'in yerel şehirleri, sınav kodunun tanımıyla: dolu = `kac_ev_gercek` 0]:

| | Geliştirme 1–10 (354 trafo, dolu 47) | Sınav 21–30 (349, dolu 44; daha önce görüldü, bilgi) |
|---|---|---|
| Yeşil / yanlış yeşil | 20 / 0 | 17 / 0 |
| Kırmızı (≥ 0,5) / gerçekte dolu | 53 / 29 (%55) | 61 / 30 (%49) |
| Bayrak (≥ 0,7) / gerçekte dolu | 20 / 15 (%75) | 26 / 18 (%69) |
| Bayrak (≥ 0,8) / gerçekte dolu | 8 / 7 (%88) | 13 / 10 (%77) |
| Renksiz kalan (bayrak 0,7) | %89 | %88 |

## Karar
1. **Panel katmanı iki güvenli uçla gösterilir, "boş yer haritası" olarak değil.**
   - **Kesin yeşil (azınlık):** bugünkü yeşil kuralı aynen (ADR-0010; yanlış yeşil kapısı ≤ %2, tüzük madde 2). Dil: "ilk 2 başvuru güvenle sığar".
   - **"Büyük olasılıkla dolu" bayrağı:** `p_bugun_asar` ≥ **0,7**. Kırmızı dolgu değil, uyarı işareti. Dil: "büyük olasılıkla dolu; başvuruda ölçüm ya da güçlendirme gerekir". Bayrak ret değildir (ADR-0005).
   - **Arası renklendirilmez:** "başvuruda bakılır" (başvuru anı motoru, ADR-0012 / ADR-0015). Bugünkü 0,5–0,7 arası kırmızılar da buraya girer.
2. **Eşik 0,7 ilkeden** ("olasılık yüksek"), sınav şehirlerine bakılarak seçilmedi; 21–30 rakamı Civan'ın kartında önceden görüldüğü için yalnız bilgi. Eşik değişirse yalnız 1–10'da; dokunulmamış ilk sınav üretici 1.5 şehirleri 31–40.
3. **Ölçü (her sınavda):** (a) yanlış yeşil (kapı, değişmez); (b) **bayrak isabeti**: bayraklıların gerçekte dolu payı ≥ ortalama `p_bugun_asar`'larının n toleranslısı (ADR-0016'daki kırmızı kovası ölçüsünün bayrak sürümü; 0,7 için yaklaşık ≥ %70 − 2·√(0,21 ÷ n)); (c) bilgi: bayrağın yakaladığı dolu payı ve renksiz kalan pay. "Yanlış kırmızı" panel katmanında artık gösterilen bir şey değildir.
4. **Tek kaynak:** üç durum modelin çıktısında bir sütun olur (`kac_ev.csv` sözleşme 1.4 adayı `pv_uc` = `yesil` / `dolu_bayrak` / `bos`), harita eşiği kendisi hesaplamaz. `renk` sütunu geriye uyum için kalır.
5. **Konumlama (Muhittin):** yük **lider katman** (bugün yapılabildiği için; Kıb-Tek'in verisiyle kalibre); panel **müşteri değeri**, "ağ / faz kaydı ve başvuru anında karar geldikçe açılır". "Paneli bıraktık" denmez. Yükte güçlü olmamızın sebebi basit yöntemin (fatura × oran) iyi ve kalibre olması; arkada gizli bir model ima edilmez.
6. **Sunumda** panel anlatılmıyor (karar masası 23:12) kararı değişmez; soru gelirse cevap bu ADR'nin cümlesi: "Panelde yalnız emin olduğumuz uçları gösteriyoruz: kesin yer var ve büyük olasılıkla dolu; gerisine başvuru geldiğinde o evin yeriyle bakıyoruz."

## Sonuçlar
- BUILD 2 (panel): `kac_ev_olasilik.py` `pv_uc` sütununu yazar, sözleşme 1.4 notu (Civan ya da Can onayı); bayrak isabetini 1–10'da ölçer, sahte kayıtlı görünümde (PR #22) aynı ölçüyü yan yana verir.
- Civan: harita panel katmanı `pv_uc`'den (yeşil dolgu, bayrak işareti, renksiz), yan panelde üç cümle; kart civan.md'de.
- Can: `sinav.py faz3`'e bayrak isabeti maddesi (3b) ve bilgi satırları; kırmızı kovası ölçüsü bilgi satırına iner.
- Feda edilen: haritada "kırmızı" görüntüsü ve trafoların %88–89'unun renksiz kalması. Kazanılan: haritada gösterilen her renk ya güvenli (yeşil) ya da büyük olasılıkla doğru (bayrak, dörtte üç).
- Açık risk: bayrak isabeti farazi şehirde ölçüldü; gerçek veride (Faz 10 pilotu, İngiltere hatları) sınanmadı.

<!--
KURAL: Bu dosyayı sonradan DÜZENLEME. Karar değişirse yeni bir ADR yaz
ve bu dosyanın durumunu "superseded by ADR-XXXX" yap.
-->
