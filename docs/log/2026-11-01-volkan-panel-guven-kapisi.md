# 2026-11-01 — Yeşil ve "hemen evet" kapısında güven şartı kalkar (ADR-0019; BUILD 2 — panel)

**Amaç:** [ADR-0019](../decisions/adr-0019-yesil-kapisinda-guven-sarti-kalkar.md) (karar masası 01:22; BUILD 1'in ölçümü: güven etiketi hatayı ayırmıyor, güvenlik zaten bantta). Yürürlük şartı (m. 3): BUILD 2 uygular, 1–10'da kurulur, **dokunulmamış üretici 1.5 şehirleri 31–40'ta bir kez**: yanlış yeşil (≤ %2, en kötü şehirde ≤ %10), ADR-0017 bayrak isabeti, başvuru akışında yanlış evet; 21–30 bilgi.

## Yöntem
- `src/kac_ev_olasilik.py`: `YESIL_GUVEN_SARTI = False`; yeşil = ilk iki başvurunun 40 çekilişin %98'inde sığması (güven şartı yok; sabit True yapılınca eski kural döner, m. 2). Kırmızı ve bayrak aynı.
- `src/basvuru.py`: başvuru anı "hemen evet" ve kayıtlı haritanın yeşili aynı sabitle (güven şartı yok).
- Ölçü: `guvenli_uc.py --guven-kiyas` aynı `kac_ev.csv`'den iki görünüm (şartlı = eski kural, p'ler aynı) ve şehir başına en kötü yanlış yeşil; `basvuru_testi.py --guven-sarti` eski kuralla akış (kayıtsız, sahte kayıt beklenen ve iki kat; motor iki kat hata varsayar, inverter satırı sahte).
- Şehirler: üretici 1.5 (main, PR #27) 1–10 ve 31–40 BUILD 2 klasöründe sıfırdan üretildi, `sablon.py --yalniz-ana` (K_YUK 1,47), `kac_ev_olasilik.py`. Sahte kaydın gerçek ağı yeniden kurması 1.5'te sınandı: şehir 1'de 40 trafonun 38'inde `kac_ev_gercek` birebir, ikisinde bir ev fark (1.3'teki gibi). 21–30: üretici 1.3 şehirleri (bilgi).
- Platform: Mac, Python 3.12.13; makine yüklü (yük ~60), sonuçlar deterministik. Taban PR #25 (motor), içine main (üretici 1.5) ve PR #23 (`pv_uc`, `guvenli_uc.py`) birleştirildi.

## Sonuç [Hesap; farazi şehir, gösterim]
**Harita (kayıtsız, aday evi olan trafolar):**

| | Geliştirme 1–10 (1.5; 354 trafo, 43 dolu) | **Sınav 31–40 (1.5; 347 trafo, 46 dolu)** | 21–30 (1.3, bilgi; 349 trafo) |
|---|---|---|---|
| Yeşil, güven şartlı → şartsız | 27 → **65** | 28 → **60** | 17 → 47 |
| Yanlış yeşil (şartsız) | 0/65 | **0/60** | 0/47 |
| En kötü şehirde yanlış yeşil | %0 | **%0** | %0 |
| Bayrak / gerçekte dolu (ölçü) | 15 / 11 = %73 ≥ %56 geçer | 22 / 15 = **%68 ≥ %60 geçer** | 26 / 18 = %69 ≥ %63 |
| Renksiz, şartlı → şartsız | %88 → %77 | %86 → %76 | %88 → %79 |

**Başvuru akışı** (3 sıra × en çok 8 başvuru; yanlış evet: evetlerin gerçekte aşan payı; parantezde 95% aralık ve yanlış evetli trafo / evet veren trafo):

| Kayıt | Kural | 1–10: hemen evet / yanlış evet | **31–40: hemen evet / yanlış evet** |
|---|---|---|---|
| Kayıtsız (bugün) | güven şartlı | %5,5 / 0/402 | %4,6 / 0/326 (%0–1,2) |
| Kayıtsız (bugün) | **şartsız** | %14,3 / 2/1.042 | **%12,2 / 4/865 = %0,5** (%0,2–1,2; 3/124) |
| Sahte, beklenen | güven şartlı | %10,4 / 3/761 | %11,0 / 2/783 |
| Sahte, beklenen | **şartsız** | %25,5 / 13/1.858 = %0,7 | **%22,9 / 2/1.624 = %0,1** (%0,03–0,45) |
| Sahte, iki kat | güven şartlı | %10,4 / 2/761 | %10,6 / 9/751 = %1,2 (%0,6–2,3) |
| Sahte, iki kat | **şartsız** | %24,0 / 9/1.753 = %0,5 | **%22,8 / 10/1.618 = %0,6** (%0,3–1,1; 4/201) |

Harita politikası (yeşilse ilk iki başvuru evet) 31–40'ta şartsız: kayıtsız 0/336, beklenen 1/426, iki kat 4/468 (%0,9). Türe göre hemen evet (31–40, kayıtsız): çarşı 192 → 325 / 765, otel 83 → 291 / 489, yurt 44 → 236 / 663, **şehir konutu 7 → 13 / 3.432**, köy ve sulama 0.

## Bulgular
1. **Yürürlük şartı tutuyor (31–40, bir kez):** yanlış yeşil 0/60, hiçbir şehirde yok; bayrak isabeti %68 ölçüyü geçiyor; başvuru akışında yanlış evet en çok %0,6 (aralık üst ucu %1,2), sınırın güvenle altında.
2. **Yeşil iki katından fazla:** 28 → 60 (31–40), 17 → 47 (21–30, BUILD 1'in karşı-olgusuyla birebir); renksiz %86 → %76. Kayıt yokken başvuru anında hemen evet %4,6 → %12,2.
3. **Yanlış evet oranı düşüyor, artmıyor:** iki kat hatalı kayıtta %1,2 → %0,6; artan evetler güvenli trafolarda (yük bandı zaten kalibre).
4. **Konutta değişiklik yok denecek kadar az** (şehir konutu 7 → 13 / 3.432): açılan trafolar çarşı, otel, yurt. Konutta darboğaz gerilim fiziği ve ağ bilgisi (ADR-0019 bağlamıyla aynı).
5. Örnek hâlâ küçük: 60 yeşil; tüzük madde 6'ya göre "%2'nin altında" demek için ~150 bağımsız yeşil gerekir.

## Ne kaldı
- Güven şartını kendi kuralında kullanan iki deneme betiği bu karara bağlanmadı: `olcum_sirasi.py` (PR #30; öğlen yükü ölçümünün değeri büyük ölçüde "güveni yüksek yapmak"tı, ADR-0019'la değeri değişir) ve `kac_ev_olasilik.konum_payi` (PR #28, analiz). Karar masasına.
- Ön şart (m. 2): bant kalibrasyonu (gerçek < P10 her güven sınıfında nominal %10 + tolerans) gerçek veride her yeniden-fitte ölçülür; BUILD 1 / Can.
- TEST'in bağımsız tekrarı.

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 1 Kas ~01:55 | v2b + ADR-0019 (güven şartı yok), üretici 1.5 | 1–10 | yeşil artar, yanlış yeşil 0, akışta yanlış evet < %2 | yeşil 27 → 65, 0/65; akış en çok %0,7 | 31–40 bir kez |
| 1 Kas ~02:00 | aynı | 31–40 | aynı | yeşil 28 → 60, 0/60, en kötü şehir %0; bayrak %68 geçer; akış kayıtsız %0,5, iki kat %0,6 | yürürlük şartı tuttu; karar masasına |
| 1 Kas ~02:03 | aynı | 21–30 (1.3, bilgi) | — | yeşil 17 → 47, 0/47; bayrak %69 | bilgi |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
