# 2026-11-01 — Can: kod envanteri, gerçek araçlarla (clean review adım 1, "öncesi" ölçümünün resmi hâli)

**Etiket: ölçüm, salt okur.** Kod değişmedi. [Kurulumsuz ilk ölçüm](2026-11-01-can-kod-envanteri.md) "tahmini"ydi; bu, aynı ölçünün planın araçlarıyla (plan §2) hâli. "Sonrası" ölçümü aynı komutlarla yapılır.

## Hipotez / amaç
Plan §2'nin araçları (lizard, jscpd, vulture) kuruldu (Can'ın isteğiyle, 1 Kas; Volkan'ın izin sorusu kutuda). Tahmini ölçüm araçlarla tutuyor mu; temizlikten önceki resmi rakamlar.

## Yaptıklarım
- Araçlar: lizard 1.24.3 ve vulture 2.16 depo kökündeki `.venv`'de (git dışı); jscpd 4.3.0 `npx` önbelleğinde. Semgrep kurulmadı (plan: isteğe bağlı).
- Ölçülen: main **7b0b836**'nın `git archive` kopyası (`src/` + `app/`, 28 `.py`). Çalışma kopyası kullanılmadı: aynı klasörde başka bir oturumun `src/sinav.py`'de commit edilmemiş değişikliği vardı.
- Komutlar (kopyanın kökünde):
  - `lizard src app --csv` (fonksiyon başına CCN, NLOC, parametre, başlangıç–bitiş satırı); `lizard src app -w` (uyarı: CCN > 15)
  - `npx jscpd@4 src app --format python --min-tokens 50 --reporters json` (birebir kopya, varsayılan "mild" mod)
  - `vulture src app --min-confidence 60` ve `vulture src app`
  - sıcak nokta: `git log --since=31.days --name-only` (dosyanın değiştiği commit sayısı) × dosyadaki Σ(CCN − 1)

## Sonuç [Hesap: araç çıktıları]

| ölçü | araçla (7b0b836) | tahmini ilk ölçüm (35d5445) |
|---|---|---|
| dosya / satır | 28 / 9.158 (`src/` 8.324) | 27 / 8.632 |
| fonksiyon | 366 (NLOC toplamı 5.915) | 352 (iç fonksiyonlar dış fonksiyona da sayılmıştı) |
| CCN > 15 / > 30 | 44 / 10 | 37 / 9 |
| NLOC > 100 | 5 | (satır > 100: 6) |
| kopya | **%2,05 satır** (188 satır, 24 klon; jeton %2,68) — birebir | %6,8 — adı değişmiş kopya dahil, 60 jeton |
| ölü kod (%60 güven) | 2 aday | 0 (gevşek yöntem) |

Arada main ilerledi (PR #25: `inverter_geri_cozum.py` yeni, `basvuru.py` 224 → 293, `sahte_kayit.py`, `olcum_sirasi.py` büyüdü); farkın bir kısmı bu. `sinav.py` fonksiyonlarında iki ölçüm birebir: `faz2` 126 (tahmini "iç hariç ~126"), `faz3` 94 (~94), `faz1` 63.

**Sıcak noktalar** (commit × Σ(CCN − 1)):

| sıra | dosya | satır | commit (31 gün) | dal | sıcaklık | en büyük CCN |
|---|---|---|---|---|---|---|
| 1 | `src/sinav.py` | 816 | 16 | 388 | 6.208 — ikinciden 1,8 kat | 126 |
| 2 | `src/sehir_uret.py` | 990 | 12 | 287 | 3.444 | 76 |
| 3 | `src/basvuru.py` | 293 | 9 | 121 | 1.089 | 75 |
| 4 | `src/tepe.py` | 611 | 6 | 180 | 1.080 | 63 |
| 5 | `src/kac_ev_olasilik.py` | 328 | 9 | 102 | 918 | 30 |
| 6 | `src/sablon.py` | 599 | 8 | 110 | 880 | 17 |
| 7 | `src/trafo_bos_kapasite.py` | 530 | 3 | 201 | 603 | 58 |
| 8 | `src/sahte_kayit.py` | 346 | 5 | 95 | 475 | 20 |
| 9 | `src/olcum_sirasi.py` | 354 | 4 | 116 | 464 | 43 |
| 10 | `app/harita.py` | 375 | 9 | 49 | 441 | 9 |

Yeni giren: `basvuru.py` 3. sıraya çıktı (PR #22 / #25 / #33 zinciri), `sahte_kayit.py` ve `olcum_sirasi.py` ilk ona girdi.

**En karmaşık 10 fonksiyon (lizard CCN):**

| fonksiyon | satır | CCN | NLOC | param |
|---|---|---|---|---|
| `sinav.py` `faz2` | 337–606 | 126 | 217 | 3 |
| `sinav.py` `faz3` | 630–771 | 94 | 111 | 1 |
| `inverter_kaydi.py` `main` | 142–223 | 76 | 81 | 0 |
| `sehir_uret.py` `sehir_uret` | 793–973 | 76 | 166 | 3 |
| `basvuru.py` `ag_kur_kayitli` | 95–213 | 75 | 109 | 5 |
| `sinav.py` `faz1` | 74–168 | 63 | 79 | 1 |
| `tepe.py` `sehir_calistir` | 422–579 | 63 | 143 | 8 |
| `trafo_bos_kapasite.py` `main` | 423–526 | 58 | 93 | 0 |
| `olcum_sirasi.py` `main` | 280–350 | 43 | 71 | 0 |
| `bilgi_degeri.py` `olc` | 218–249 | 32 | 31 | 3 |

**Kopya, dosya başına (jscpd):** `pv_acilma.py` %26,4 · `bilgi_degeri.py` %16,8 · `kac_ev_olasilik.py` %16,5 · `basvuru.py` %15,0 · `olcum_sirasi.py` %13,8 · `inverter_geri_cozum.py` %6,6 · `app/ornek_veri.py` %4,8 · `sehir_uret.py` %3,7. `sinav.py`'de birebir kopya yok (S-05'teki sözlük kopyası satır kırılımı farklı olduğu için birebir sayılmıyor).

**En büyük klonlar:**
- `kac_ev_olasilik.py` 181–193 ↔ `olcum_sirasi.py` 122–134 (13 satır); aynı çift 205–214 ↔ 148–157, 199–205 ↔ 142–148, 237–247 ↔ 127+: `olcum_sirasi.py` olasılıklı çekilişin parçalarını kopyalamış.
- `bilgi_degeri.py` ↔ `pv_acilma.py`: beş klon (200–212 ↔ 92–104, 161–170 ↔ 53–62, 269–277 ↔ 136–143, 291–298 ↔ 167–174, 174–179 ↔ 63–68) — iki betik büyük ölçüde aynı iskelet (ilk ölçümdeki işaretle aynı).
- `basvuru.py` dosya içi: 271–281 ↔ 236–246, 265–271 ↔ 230–236.
- `sehir_uret.py` dosya içi 681–690 ↔ 728–738; `sehir_uret.py` 402–420 ↔ `app/ornek_veri.py` 93–111 (iki klon).
- `bilgi_degeri.py` 65–74 ↔ `sahte_kayit.py` 96–105; `kac_ev.py` 183–192 ↔ `sablon.py` 564+.

**Ölü kod (vulture, %60 güven; düşük güvende de aynı iki satır):**
- `src/sahte_kayit.py:252` `kayit_oku` — kodda çağrılmıyor, yalnız `basvuru.py:7` docstring'i anıyor. Neden var: docstring'e göre "gerçek Kıb-Tek kaydı aynı biçimde gelirse" okuyucu (karar masası 01:22). Ölü değil, gelecekteki giriş noktası; **bırak**.
- `src/trafo_bos_kapasite.py:479` `rooms = [group_room(…) for c in groups]` — hesaplanıyor, hiç kullanılmıyor. `group_room` (304) saf fonksiyon, yan etkisi yok: satır silinirse çıktı aynı, yalnız süre kısalır. Satır ilk commit'ten (e05c9fa, 31 Eki); dosyanın eski "inverter kaydından gerilim haritası" bölümünde (`main`), projede kullanılmayan kısım (CLAUDE.md). Gerçek ölü kod adayı.

## Karar / sıradaki adım
- Bu tablo temizlikten önceki resmi "öncesi" rakamı; tahmini ölçüm yalnız yöntem denemesi olarak kalır.
- `sinav.py` bulguları (S-01…S-12) değişmedi; araç ölçüsü S-01 / S-02'nin rakamlarını doğruladı.
- Adım 3 sırası için işaret: `basvuru.py` (3. sıra, %15 kopya, `ag_kur_kayitli` CCN 75), `olcum_sirasi.py` ↔ `kac_ev_olasilik.py` kopyası, `bilgi_degeri.py` ↔ `pv_acilma.py`, `trafo_bos_kapasite.py:479`. Hepsi Volkan / BUILD dosyaları → kutu.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
