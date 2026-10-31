# Volkan (+ Claude, BUILD) — Faz 8 — Üretici çapalama ve yeni sınav şehirleri (üretici 1.3)

Tüzük: geçerli ([docs/tuzuk.md](../tuzuk.md)). Karar: karar masası 21:25 (yeni Faz 8), 21:51 (PR #16 dalının üstünde başla). Dal `uretici/1.3` (taban `kalibrasyon/faz7`), PR.

Amaç (1 cümle): Farazi şehri gerçek dünyaya yaklaştırmak, yani üreticinin dağılımlarını gerçek veriye çapalayıp mesafe düzleşene kadar ayarlamak; sonra yeni tohumla yeni sınav şehirleri üretip Faz 2–3 rakamlarını sürüm üçlüsüyle yeniden ölçmek.

Veri partileri (tüzük §2; hepsi **ayar** payında kullanılır, çünkü üretici ayarı modelin ayarı değil, dünyanın tarifi):
- **P1-edp-2018** (İspanya, 29 trafo): trafo eğrilerinin benzerliği 0,93, müşteri başına öğlen yükü CV 0,45, öğlen en düşük 285 W/müşteri, saf tahmin hatası %25,5 / P90 %53,4 (`src/edp_kiyas.py`); faturalı model hatası ~%10 (`src/edp_test.py`).
- **P2-ukpn-2014** (İngiltere, 6 hat + 40 kent fideri): kent faz dengesizliği ortanca %14,4, P84 %30,3; öğlen bara geceden ~1 V düşük; gündüz en düşük talep 205–355 W/müşteri (PR #11 günlüğü).
- **P4-malta-2026** (Enemalta, 1.331 merkez): talep ÷ güç P10/50/90 0,13 / 0,42 / 0,74 (yıl tepesi). **P5-kotsonias-2019** (Kıbrıs AG iletken tablosu). Bu ikisi bu turda kullanılmadı (aşağıda).
- Kullanım bölünmesi (DONDURULDU 31 Ekim 22:05): üretici ayarı yalnız şehir 1–10'da. Eski sınav şehirleri 11–20 hiçbir ayara girmez. **Yeni sınav şehirleri 21–30**, yeni tohum, bir kez ölçülür. Modelin katsayıları (Faz 7: k_yük, s) bu fazda değişmez.

Hipotez ve beklenen etki: üretici gerçek kadar dağınık olunca farazi şehir "fazla iyi" görünmeyi bırakır. Faturalı model hatası farazide %4'ten İspanya'ya (~%10) yaklaşır; Faz 7 bantlarının farazi kapsaması %96'dan ~%80'e iner; Faz 3'te yeşil ve yanlış kırmızı yeniden dengelenir.

Kapılar: yanlış yeşil ≤ %2 (sınav 21–30); kalibrasyon İspanya'da (Faz 7, değişmez); farazi kapsama bilgi. Sonra işletme ölçüleri.

Sürüm: üretici 1.3 (ebeveyn 1.2); model v2 (Faz 7); veri P1, P2; tohumlar 1–10 ayar, 21–30 sınav.

Adımlar:
1. Üç düğme (`src/sehir_uret.py`, ayrı rastgele akışlar, şehir yapısı aynı):
   - öğlen evde olma farkı (trafo ve abone başına çarpan, günlük enerji korunur) → İspanya;
   - faz dengesi (sırayla bağlanan pay) → UKPN kent;
   - öğlen OG değişimi şehir başına −%0,4…+%0,8 → UKPN.
2. Şehir 1–10'da ayar; mesafe tablosu her denemede; plato.
3. Yeni sınav şehirleri 21–30; `sablon.py`, `kac_ev_olasilik.py`, `sinav.py faz2 / faz3` bir kez.
4. Günlük `docs/log/2026-11-01-volkan-faz8-uretici.md`, ROADMAP Faz 8, DEVIR, PR.

Bu turda yok (sıradaki tur, günlükte): Malta trafo boyutu çapası (Nisan / yıl tepe oranı EAC'den türetilmeli), Kotsonias ince uç kol senaryosu (yaygınlığı BULAMADIM), panel yeri dağılımı, mahsuplaşmalı faturanın net yazılması (uzmana soru 7).

Dokunulmayacak: `src/sinav.py`, `src/grafikler.py`, `src/edp_kiyas.py` (Can; edp_kiyas yalnız içe alınıp okunur), `app/` (Civan), model katsayıları (Faz 7).

Kendin karar ver: çan eğrisinin merkezi ve genişliği, deneme değerleri, sınav tohumları.
Karar masasına yaz: yanlış yeşil 0'dan çıkarsa; mesafe düzleşmezse; sunum rakamlarını değiştirecek bir şey.
