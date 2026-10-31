# Can — Faz 3 — kaç ev sınavı ve kilit grafik

Kartı yazan: Volkan (+ Claude, BUILD), 31 Ekim 2026 akşam. Sözleşme: [docs/data/tablo-bicimi.md](../data/tablo-bicimi.md) §3 (`kac_ev_gercek`, `kac_ev_aday`, `kac_ev_tavan`) ve §6 (`kac_ev.csv`). Yöntem: [modeling.md](../method/modeling.md) bölüm 4–5, [ADR-0010](../decisions/adr-0010-yesil-karari-marj-guven-kumulatif.md).

**Amaç (1 cümle):**
- `src/kac_ev.py`'nin (Volkan + Claude, [PR #13](https://github.com/volkanGRGN/KKTC-hackathon/pull/13)) renk ve sayılarını cevap anahtarıyla karşılaştırıp ROADMAP Faz 3 geçme sınavını ölçmek.
- Aynı ölçüleri bugünkü %40 kuralına uygulamak, sunumun kilit grafiğini çizmek.
- Modeli yazan sınavı yazmaz.

**Girdi:**
- Şehirler ve model çıktısı:
  - `python3 src/sehir_uret.py 1 20`
  - `python3 src/sablon.py data/synthetic`
  - `python3 src/kac_ev.py data/synthetic`
  - PR #8 → #12 → #13 birleşene kadar `kac-ev/ilk-surum` dalından çalıştır. Üretici 1.2 iki indirme ister: kıyı ve Open-Meteo 2023 (README).
- `kac_ev.csv` sütunları: `kac_ev_karamsar`, `kac_ev_iyimser`, `isil_pay_kw`, `gerilim_pay_kw_karamsar`, `gerilim_pay_kw_iyimser`, `sinir_karamsar`, `renk`, `kural40_ev`.

**Çıktı:**
- `src/sinav.py faz3 <kök>` → madde satırları + bilgi satırları, Faz 1 / Faz 2 gibi.
- `src/grafikler.py` kilit grafik → `docs/sunum/` altına PNG.
- Günlük: `docs/log/2026-10-31-can-faz3.md`.

**Ölçüler** (trafo kümesi: `kac_ev_aday` > 0; aday = 0 ayrı sayılır):
1. **Yanlış yeşil**:
   - `renk` = `yesil` olup `kac_ev_gercek` = 0 olanların yeşillere oranı.
   - Eşik ≤ %5, en kötü şehirde ≤ %10 (gösterim). Canlı bütçe < %2 (ADR-0010) bilgi satırı.
   - Yanına "dolu trafoların yeşil denen payı" (÷ dolu).
2. **%40 kuralı aynı ölçüyle:**
   - "Yer var" = `kural40_ev` ≥ 1; yanlış yeşili aynı tanımla.
   - Yan yana satır; sunumun kilit rakamı.
3. **Yanlış kırmızı**: `kirmizi` olup gerçek ≥ 1 olanların kırmızılara oranı. Hedef ≤ %20, raporla.
4. **Kaç ev hatası**:
   - |tahmin − gerçek| ortancası, üç sayı için: karamsar, iyimser, ortası.
   - Eşik ≤ 2 ev; hangisinin eşiği geçtiğini yaz.
   - `kac_ev_tavan` = 1 olanlar ayrı (gerçek alttan kesik).
5. **Sarı oranı**: hedef ≤ %30, aşarsa sebep.
6. **Bilgi:**
   - tip başına renk dağılımı;
   - gerçeğin [karamsar, iyimser] aralığında olma oranı;
   - `sinir_karamsar` dağılımı.

**Kilit grafik:**
- İki çubuk: "dolu trafoya yer var dedi": bizim yeşil vs %40 kuralı.
- Hem oran hem sayı; şehir başına nokta ya da aralık.
- Etiket: "farazi şehir, gösterim".
- Benim ölçümüm (sınav şehirleri 11–20): biz 0/21, %40 kuralı 41/284 (%14). Dolu 74 trafonun 41'ine %40 kuralı "yer var" diyor.

**Adımlar** (her biri ≤ 1 saat):
1. `faz3()` ölçüleri.
2. Kilit grafik.
3. Günlük.

**Nasıl denenir:**
- `python3 src/sinav.py faz3 data/synthetic` → 5 madde + bilgi.
- Benim geliştirme betiğimle karşılaştır: [Faz 3 günlüğü](../log/2026-10-31-volkan-faz3.md) tablosu, şehir 1–10 ve 11–20.

**Bitti sayılması için:**
- `faz3` 20 şehirde koşuyor.
- Yanlış yeşil iki kural için yan yana.
- Grafik PNG `docs/sunum/`'da.
- Günlükte rakamlar.

**Dokunulmayacak dosyalar:** `src/kac_ev.py`, `src/sablon.py`, `src/sehir_uret.py`, `docs/data/tablo-bicimi.md`.

**Kendin karar ver** (sorma, günlüğe yaz): grafik biçimi, şehir başına gösterim, aday = 0 trafoların raporu.

**Karar masasına yaz** (volkan.md, bekleme): kırmızı kuralı okuması (varsayılan `karamsar_yeni_ev`; karar bekliyor, volkan.md "kırmızı kuralı" UYARI'sı). Karar değişirse BUILD `KIRMIZI_KURALI`'nı değiştirir, sen yeniden koşarsın.

**Takılırsan:** önce Faz 3 günlüğündeki tanımlara bak; sonra can.md'ye yazmadan önce volkan.md'ye UYARI.
