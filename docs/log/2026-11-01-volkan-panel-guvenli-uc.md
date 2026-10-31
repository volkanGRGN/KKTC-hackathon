# 2026-11-01 — Panel katmanı "güvenli uçlar": `pv_uc` sütunu ve bayrak isabeti (BUILD 2 — panel)

**Amaç:** Muhittin'in dördüncü cevabı madde 1, PV kısmı; [ADR-0017](../decisions/adr-0017-pv-katmani-guvenli-uclar.md) (karar masası 00:12). Panel katmanı "boş yer haritası" değil iki güvenli uç: kesin yeşil (azınlık) ve "büyük olasılıkla dolu" bayrağı; arası renksiz ("başvuruda bakılır"); asla yanlış yeşil. Bu iş veriyi üretir (`kac_ev.csv` `pv_uc`); haritada gösterim Civan'ın.

## Yöntem
- `src/kac_ev_olasilik.py`: `BAYRAK_P = 0.7`, `pv_uc(renk, p_bugun)`: yeşil = bugünkü yeşil (ADR-0010 kuralı aynen); `dolu_bayrak` = bugün aşma olasılığı ≥ 0,7; diğerleri `bos`. `kac_ev.csv`'nin sonuna `pv_uc` (sözleşme §6, 1.4 adayı). Diğer sütunlar değişmedi: 1–10'da yeniden koşuldu, eski `kac_ev.csv` ile 400 satırın hepsinde ilk 13 sütun birebir.
- `src/guvenli_uc.py`: ADR-0017 madde 3'ün ölçüsü, aday evi olan trafolarda; dolu = cevap anahtarında `kac_ev_gercek` 0. (a) yanlış yeşil; (b) bayrak isabeti ≥ ort(p) − 2·√(ort(p)(1 − ort(p)) ÷ n); (c) bilgi: bayraklıların bugün aşan payı, bayrağın yakaladığı dolu payı, renksiz pay. `--kayitli`: aynı ölçü sahte Kıb-Tek kayıtlarıyla (PR #22'nin `basvuru.harita_rengi`'si, motor iki kat hata varsayar; `basvuru_testi.py` tohumları, renkler o tablonunkiyle aynı).
- Eşik 0,7 ADR-0017'de ilkeden; **ayar yok**. Yalnız geliştirme 1–10 ölçüldü; 21–30 karar masasının ADR tablosunda önceden görüldü (bilgi), dokunulmamış ilk sınav üretici 1.5 şehirleri 31–40.
- Platform: BUILD 2 klasörü, Mac, Python 3.12.13; üretici 1.3 şehirleri (K_YUK 1,47); kayıtlı görünüm PR #22 kodu 858a999.

## Sonuç: geliştirme 1–10 [Hesap; farazi şehir, gösterim]
354 trafo (aday evi olan), 47'si gerçekte dolu.

| Görünüm | Yeşil / yanlış yeşil | Bayrak | Bayrak isabeti (gerçekte dolu) | Ölçü (b) | Bayrağın yakaladığı dolu | Renksiz |
|---|---|---|---|---|---|---|
| **Resmi (kayıtsız)** | **20 / 0** | 20 | **%75 (15/20)** | ≥ %59 (ort p 0,78) geçer | %32 (15/47) | %89 (314/354) |
| Sahte kayıt, hatalar yarı | 31 / 0 | 19 | %89 (17/19) | ≥ %67 geçer | %36 (17/47) | %86 |
| Sahte kayıt, beklenen | 28 / 0 | 19 | %84 (16/19) | ≥ %65 geçer | %34 (16/47) | %87 |
| Sahte kayıt, iki kat | 32 / 0 | 19 | %79 (15/19) | ≥ %68 geçer | %32 (15/47) | %86 |
| Kusursuz bilgi | 32 / 0 | 28 | %96 (27/28) | ≥ %80 geçer | %57 (27/47) | %83 |

Bayraklıların bugün 259 V'u aşan payı her satırda isabetle sayıca aynı çıktı (aynı trafolar olduğu ayrıca bakılmadı). Kıyas: eski kırmızı (≥ 0,5) 53 trafo, gerçekte dolu %55 (29/53).

## Bulgular
1. **Resmi hesapla iki uç güvenli:** yeşil 20, yanlış yeşil 0; bayrak 20 trafoda, dörtte üçü gerçekten dolu (eski kırmızıda yarısı). ADR-0017'nin karar masası tablosuyla birebir.
2. **Bedeli açık:** trafoların %89'u renksiz, ve gerçekte dolu 47 trafonun yalnız üçte biri bayraklı; kalan 32 dolu trafo "başvuruda bakılır"da. Bayrak "dolu trafoların listesi" değil, "dolu dediğimiz yerde büyük olasılıkla haklıyız" demek.
3. **Kayıtlar gelince iki uç da güçleniyor:** yeşil 20 → 28–32, bayrak isabeti %75 → %79–89 (kusursuz bilgide %96), yanlış yeşil yine 0. Renksiz pay az düşüyor (%89 → %86): sarının tabanı başvurunun yeri (ADR-0012 / 0015), harita düzeyinde kayıt bunu çözmez.

## Ne kaldı
- Harita gösterimi Civan'da (civan.md UYARI); sınav maddesi (3b) Can'da (`sinav.py faz3`).
- 21–30 ve diğer şehirlerin `kac_ev.csv`'si yeniden üretilince `pv_uc` gelir (resmi koşum karar masasında).
- Bayrak isabeti farazi şehirde; gerçek veride (Faz 10 pilotu, İngiltere hatları) sınanmadı (ADR-0017 açık risk).

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas ~00:20 | v2b + `pv_uc` (bayrak 0,7), ayar yok | 1–10 | resmi sütunlar değişmez; yanlış yeşil 0, bayrak isabeti ölçüyü geçer | ilk 13 sütun birebir; 20/0, bayrak %75 (15/20) ≥ %59; renksiz %89 | PR, harita Civan'a |
| 1 Kas ~00:21 | aynı + sahte kayıt (PR #22, iki kat varsayım) | 1–10 | kayıtla iki uç güçlenir, yanlış yeşil 0 | yeşil 28–32, bayrak %79–89, yanlış yeşil 0 | bilgi |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
