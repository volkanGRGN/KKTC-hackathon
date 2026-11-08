# 1 Kasım 2026 — Can — `sinav.py`: faz1 gerilim maddesi yılın tepesini görüyor; faz2 şehirler arası yalnız kümedeki şehirlerle (KARAR 11:12)

Windows, üretici 1.5 şehirleri (31–40 ve 41–50 bu makinede üretildi), farazi, gösterim [Hesap: Can].

## 1. faz1 madde 4: en düşük gerilim (ADR-0016 m. 3)
- Önce: yalnız `v_min_bugun_v` (Nisan). Sonra: trafo başına Nisan ile `v_min_tepe_v` (yılın tepe penceresi, üretici 1.4+) küçüğü; satırda hangi pencere olduğu yazılır; `v_min_tepe_v` boşsa yalnız Nisan ve sayısı yazılır. Bilgi satırı: yalnız Nisan'ın en düşüğü. Eşikler aynı (≤ %1 ve ≥ 200 V); oynatılmadı.

| Küme | önce (yalnız Nisan) | sonra (Nisan + yıl tepesi) |
|---|---|---|
| 31–40 | GEÇTİ, en düşük 222,3 V, 207 altı 0/400 | GEÇTİ, en düşük **201,1 V** (sehir-036 T03, yıl tepesi), 207 altı 2/400 (%0,5) |
| 41–50 | GEÇTİ, en düşük 216,9 V, 0/400 | **KALDI**, en düşük **175,0 V** (sehir-047 T23, yıl tepesi), 207 altı 3/400 (%0,8; 202,9 ve 203,1 V) |

- 31–40'taki 201,1 V karar masasının 1.5 Mac rakamıyla aynı (KARAR 01:20): madde artık karar masasının raporladığını görüyor.
- **Yeni bulgu, 41–50:** sehir-047 T23 köy, 100 kVA, 760 m ABC95, 3 hat; 24 abone (19 konut), fatura 300,0 MWh/yıl, yıl tepesi 71,1 kW; Nisan en düşüğü 216,9 V, yılın tepesinde 175,0 V. Ölçülü trafo (yük kartlarının ölçülmeyen 280'inde değil). Abone başına bu kadar büyük fatura gizli mahalle yükü demek [Yorum] → BUILD 1'in 1.6'da düzelttiği "hat tasarımı mahalle yükünü saymıyor" mekanizmasıyla aynı görünüyor (1.6 + hat düzeltmesinde 1–10 en düşük 200,9 V). Mac teyidi yok.

## 2. faz2 madde 4: şehirler arası hata ÷ şehir içi
- `sablon.py capraz()` her şehri kökteki sıradan bir önceki şehrin modeliyle tahmin eder; kökte başka şehirler (ya da eski koşulardan kalmış `tahmin_capraz_s*` dosyaları) varsa aralığın ilk şehri kümenin dışındaki bir modelle sayılıyordu → oran köke bağlı (#43'te BUILD 1 0,75, TEST 0,79).
- Sonra: yalnız modeli kuran şehir de `--aralik` kümesinde olan dosyalar sayılır; bilgi satırı çiftleri yazar ("041→042, …") ve kümenin dışından gelenleri "sayılmadı" diye listeler; maddede n = şehir.
- Sınama (geçici kök, 040–043 kopyası, `sablon.py` tam kip): `--aralik 41-43` → 041→042, 042→043, oran 0,95, "040 → 041 sayılmadı"; `--aralik 40-43` → dört çift, 0,90. Ana kökte (`--yalniz-ana` koşuları) dosya yok, madde eskisi gibi KALDI ("kaynağı bu kümede olan dosya yok").
- Kalan köke bağlılık: aralığın ilk şehrinin çifti ancak kökte aralıktan bir önceki şehir aralıktaysa sayılır; kökte yalnız aralık varsa halka kapanır (son → ilk). Raporda çiftler yazdığı için iki koşu karşılaştırılabilir.

## Diğer çıktılar
faz1 ve faz2'nin öbür satırları 31–40 ve 41–50'de bayt bayt aynı (önce / sonra `Compare-Object`; yalnız madde 4 satırları ve yeni bilgi satırları değişti).
