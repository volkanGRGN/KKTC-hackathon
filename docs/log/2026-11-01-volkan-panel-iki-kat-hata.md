# 2026-11-01 — Başvuru anı motoru "iki kat kayıt hatası" varsayarken (PR #22, panel)

**Amaç:** Karar masası 23:47 (volkan.md "PR #22 iki soru"): Kıb-Tek kayıtlarının doğruluğu sahada ölçülene kadar motor **iki kat hata varsayar**. Soru: bu kural kayıtlar gerçekten iki kat hatalıyken yanlış evet'i sınırın (%2) altına indiriyor mu, ve kayıtlar beklenen ya da yarı hatalıyken bedeli ne (hemen evet ne kadar düşüyor). İlk koşum: [sahte kayıt günlüğü](2026-11-01-volkan-sahte-kayit.md) (motor hatayı "beklenen" varsayıyordu).

## Yöntem
- **Tek değişiklik:** `src/basvuru.py` `VARSAYILAN_HATA = 'iki_kat'`: motor kayıt hata payını `sahte_kayit.hata_payi('iki_kat')` alır (kademe kaydı doğru olasılığı %89 → %75, hat boyu ±%30, direk sırası ±4, faz kaydının doğru payı %80, inverter barası ±2 V, empedans ±%40). Veri tarafı (sahte kayıtların kendi hatası) değişmedi. `src/basvuru_testi.py --model-hata iki_kat|aynen` (varsayılan motorunki; `aynen` ilk koşumu verir). Fizik, kapı ve eşikler aynı; ayar yok.
- **Platform:** BUILD 2 klasörü (Mac, Python 3.12.13, `trafo-sablonu-build/.venv`), üretici 1.3 şehirleri BUILD klasöründen kopya (K_YUK 1,47 `tahmin.csv` / `kac_ev.csv`). Sağlama: geliştirme 1–10'da `--model-hata aynen` ilk koşumun rakamlarını birebir verdi (hemen evet %4,2 / %12,9 / %20,9; yanlış evet %0,0 / %0,6 / %1,5 / %0,3).
- Geliştirme 1–10'da koşuldu, **sınav 21–30 bir kez** (1 Kasım ~00:10). Resmi rakam karar masasının Mac tekrarından.

## Sonuç: sınav 21–30 (bir kez) [Hesap; farazi şehir, sahte kayıt, gösterim]
Satır = kayıtların gerçek hata düzeyi; motor her satırda iki kat varsayar (kusursuz satırında sıfır). Parantezde ilk koşum (motor beklenen varsayarken).

| Kayıtların gerçek hatası | Hemen evet | Yanlış evet (evetlerin) | Yanlış evet, 95% aralık | Yanlış evetli trafo | Önce ölç | Harita yeşil / kırmızı | Yanlış yeşil |
|---|---|---|---|---|---|---|---|
| Kayıtsız (bugün) | %3,8 (276/7.179) | %0,7 (2/276) | %0,2–2,6 | 1 | %67,6 | 17 / 61 | 0/17 |
| Yarı | %10,7 (%11,9) | %0,1 (1/766) (%0,2) | %0,02–0,7 | 1 / 84 | %70,7 | 27 / 33 | 0/27 |
| **Beklenen** | **%9,7** (%10,5) | **%0,0** (0/694) (%0,1) | %0–0,55 | 0 / 85 | %70,0 | 27 / 40 | 0/27 |
| **İki kat** | %10,1 (%10,7) | **%1,9** (14/722) (%2,6, 20/770) | **%1,2–3,2** | **6 / 94** | %70,8 | 33 / 37 | 0/33 |
| Kusursuz bilgi | %18,0 | %0,4 (5/1.295) | %0,2–0,9 | 3 / 104 | %61,1 | 26 / 38 | 0/26 |

95% aralık: Wilson, evetler bağımsız sayılarak (değiller: aynı trafonun sıraları; gerçek aralık daha geniş). "Yanlış evetli trafo": yanlış evet çıkan trafo / evet veren trafo.

Geliştirme 1–10 aynı yön: beklenen kayıtta hemen evet %12,9 → %11,6, yanlış evet %0,6 → %0,7 (6/844, 3 trafo); iki kat kayıtta yanlış evet %1,5 → %1,1 (9/827, 5 trafo; aralık %0,6–2,1).

- Aynı akışta %40 kuralının evetlerinin %13,4'ü yanlış (495/3.699), değişmedi (kayıt kullanmıyor).
- Harita politikası (yeşilse ilk iki başvuru evet) iki kat kayıtta %1,5 (3/198); yanlış yeşil her satırda 0.
- Şehir konutunda hemen evet: beklenen kayıtta 257 → 217 / 3.408.

## Bulgular
1. **Kural yanlış evet'i sınırın hemen altına indiriyor ama güvenle değil.** Kayıtlar iki kat hatalıyken %2,6 → %1,9; aralığın üst ucu %3,2 ve 14 yanlış evet 6 trafoda toplanmış (biri 5). Tüzük madde 6'ya göre "%2'nin altında" demek için ~150 bağımsız karar noktasında 0 ihlal gerekir; burada 94 evet veren trafonun 6'sında ihlal var. **Kapı bu satırda tutmuş sayılmaz** [Yorum].
2. **Bedel küçük:** kayıtlar beklenen düzeydeyse hemen evet %10,5 → %9,7 (751 → 694 başvuru), yarı hatalıysa %11,9 → %10,7. Yanlış evet beklenen kayıtta 1 → 0.
3. **Kalan yanlış evetlerin bir kısmı kayıttan değil:** kusursuz bilgide de 5 yanlış evet (3 trafo) var; taban öğlen yükü ve OG değişimi. Bu yüzden hata payını büyütmek yanlış evet'i sıfıra indirmez.
4. Harita ve renkler kayıt varsayımıyla az oynuyor (iki kat kayıtta yeşil 35 → 33); yanlış yeşil 0.

## Ne kaldı / soru
- Kayıt kalitesi ölçülmeden motorun yanlış evet'i, kayıtlar gerçekten iki kat kötüyse sınırda kalıyor. Seçenekler karar masasında (BUILD ayar yapmadı, eşik değiştirmedi): (a) kural yeterli say (kusur oranları zaten [Yorum], iki kat kötümser uç); (b) pilot şartı: sahada 20–30 kayıt ölçülene kadar motor yalnız "önce ölç / hayır" der, hemen evet yok; (c) yeni bir koşum: iki kat varsayım + kayda koşullu evetlerde daha yüksek kapı (bu sınavda değil, 1–10'da kurulup yeni bir sınavla).
- Sarıda konum payı (`yesil_konum_payi`, ADR-0015 m. 4) ve kayıtlarla kaç ev bandı hâlâ ölçülmedi.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas ~00:06 | motor v1, `--model-hata aynen` | 1–10 | ilk koşumun sağlaması | birebir | ortam doğru |
| 1 Kas ~00:08 | motor v1.1, `VARSAYILAN_HATA` iki kat | 1–10 | iki kat kayıt hatasında yanlış evet < %2, bedel küçük | yanlış evet %1,5 → %1,1; hemen evet %12,9 → %11,6 | 21–30 bir kez |
| 1 Kas ~00:10 | aynı | 21–30 | aynı | yanlış evet %2,6 → %1,9 (14/722, 6 trafo, aralık %1,2–3,2); hemen evet %10,5 → %9,7; yanlış yeşil 0 | sınırda; karar masasına |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
