# Tüzük — veri döngüsünün değişmezleri

Bu dosya [ADR-0013](decisions/adr-0013-veri-dongusu-tuzugu.md)'ün işletme hâli ve Muhittin'in şablonu ([cevap 3](log/2026-10-31-muhittin-cevap-3-veri-dongusu.md), ek girdi 21:20). Her görev kartı bu dosyaya referans verir ("Tüzük: geçerli"). Buradaki maddeler **direktif**: her zaman açık, karttan karta değişmez. Bir maddeyi değiştirmek yeni ADR ister.

Yazan: BUILD (31 Ekim gece, karar masası 21:20 ve 21:32). Sahibi Volkan.

## 1. Değişmezler (ADR-0013)
1. **Hold-out ayrımı.** Gelen her ölçülü trafo partisi ikiye bölünür: **ayar** (model + üretici) ve **doğrulama** (hiç dokunulmaz). Bölünme değer görülmeden önce yazılır ve dondurulur. İspanya, İngiltere ve pilotun doğrulama payı dokunulmaz kalır. Gerçek hold-out'a her bakış [hold-out defterine](log/holdout-defteri.md) bir satır (istatistik gücü harcar).
2. **İki kapı, sonra iyileştirme.** "Model iyileşti" ancak dokunulmamış gerçek trafolarda (ya da modelin görmediği yeni üretilmiş şehirlerde) söylenir: (1) yanlış yeşil ≤ %2 **ve** (2) kalibrasyon toleransta; ancak ondan sonra sarı ve yanlış kırmızı küçülmüşse. Kapı tutmazsa iyileşme sayılmaz. Aynı şehirlerde metriğin oynaması iyileşme değildir.
   - **Kalibrasyon toleransı örnek büyüklüğüne bağlı:** PIT düzlüğünde 10 kovada en büyük sapma ≤ max(0,05; 2·√(0,09 ÷ n)), n = bağımsız trafo ya da karar noktası sayısı (İspanya 29; `edp_test.py` satırları aynı 29 trafonun tekrarlarıdır, n değil; İngiltere 6 hat). n = 29'da 0,11; 0,05 ancak n ≥ ~150'de anlamlı (madde 6 ile tutarlı). %80 bant kapsaması %70–90 (karar masası 21:51).
3. **Kalibrasyon gerçeğe karşı.** Bant kapsaması, PIT histogramı ve nominal–ampirik kapsama eğrisi gerçek doğrulama verisinde ölçülür, yalnız üreticiyle değil. Fazla eminlik düzeltilmeden bant yayınlanmaz: model-sapma terimi ya da şişirme katsayısı (`src/kalibrasyon.py`). **Kalibrasyon modelin sevk edildiği yapılandırmada ölçülür**, ölçülü sayısı ve ölçülecek trafoyu seçme yöntemi dahil (ör. şehir başına 12 ölçülü trafo, tabakalı seçim); başka yapılandırmanın (ör. 5 ölçülü, rastgele seçim) hatası katsayıya karışmaz; yapılandırma değişirse katsayı yeniden (karar masası 22:0x, 23:13).
4. **Güncelleme periyodik ve sürümlü.** Sessiz, sürekli daraltma yok. Sayı ya da sapma tetikleyince yeniden-fit, sürüm numarasıyla. Ham veri saklanır. Çerçeve hiyerarşik: popülasyon dağılımı + ölçülen trafonun kendi değeri.
5. **Her rakam kaynağa iner:** ham veri kimliği + betik + commit + tohum. Model, üretici ve veri birlikte sürümlenir; her sonuç bu üçlüyü (+ tohum) anar.
   - **Platform:** resmi rakamlar karar masasının Mac koşumundan. Başka platformda yeniden üretilen şehirler gösterim içindir, sınav için değil: aynı tohumla Mac ↔ Windows'ta bir trafo farklı çıktı, Mac kendi içinde deterministik (karar masası 21:44). Sebep Faz 6'da aranır (Python 3.14 ↔ 3.12, kayan nokta); sonuç satırı platformu ve Python sürümünü de anar.
6. **Hedefler türetilir.** Doğrulama: 0 ihlalle %95 güvenle "< %2" için ~150 bağımsız karar noktası (3/n kuralı). Ayar: plato, yani gerçek ile üretilen dağılım arasındaki mesafe düzleşene kadar; sayı değil.
7. **Sıra.** Trafo çıkış gerilimi ucuz ilk adım ama yanlış kırmızıda ~%19'da platoya oturur. Büyük kazanç abone–trafo, adres ve faz kaydında (ADR-0012, ADR-0015). Ucuz inverter verisi gece kör; yük tarafı ayrı (ADR-0014).

Projeden gelen eski kurallar da geçerli ([CLAUDE.md](../CLAUDE.md)): rakam uydurma, her rakam [Kaynaklı] / [Hesap] / [Yorum]; en kritik ölçü yanlış yeşil; geliştirme şehirleri 1–10, sınav şehirleri 11–20, sınav şehrine göre ayar yok.

## 2. Veri partisi görev kartı
Gelen her veri partisi için `docs/gorev/` altında bir kart; [görev kartı kalıbına](gorev/README.md) şu alanlar eklenir:

```
Tüzük: geçerli (docs/tuzuk.md)
Parti kimliği: P<n>-<kaynak>-<tarih>
Kaynak ve çekim tarihi: adres, KAYNAK.txt, SHA-256
Kapsam: hangi trafolar / hatlar, gözlem penceresi, eksik ne
Veri sözleşmesi: şema, birim, saat dilimi, boş değerin anlamı, bilinen yanlılık
   (ör. "yalnız panelli evler", "gerilim inverter ucunda")
Kullanım bölünmesi (DONDURULDU <tarih saat>, değer görülmeden): ayar = …, doğrulama = …
Hipotez ve beklenen etki:
Kapılar: yanlış yeşil ≤ %2, kalibrasyon toleransı, sonra işletme ölçüleri
Sürüm: üreteceği vN+1, ebeveyni vN
```

## 3. Deney günlüğü
- `docs/log/` altında, **append-only**: eskisi silinmez, düzeltme yeni satırdır.
- Koşu başına bir satır: tarih, sürümler (model / üretici / veri), tohum, hipotez, bütün kapı ve işletme ölçüleri, kapı geçti / kaldı, karar (terfi / ret / daha çok veri), artefakt bağlantısı (commit, dosya).
- **Olumsuz sonuçlar da yazılır.**

## 4. Ajan ayrımı
- Değişmezler (bu dosya) direktif; parti ayrıntısı görev kartında.
- Ajan modeli sessizce değiştiremez. Model değişikliği önerisi bir ADR açar (önce / sonra ölçü + kapı kontrolü); terfi kapılar geçerse.
- **Öneren ≠ puanlayan:** modeli değiştiren adım ile hold-out'ta puanlayan adım ayrı. Projede: BUILD modeli yazar ve katsayıyı üretir; Can sınavı yazar ve resmi koşumu yapar (karar masası 21:32).

## 5. "Bitti" iki seviye
- **Parti bitti:** kartın kapıları değerlendirildi, günlük yazıldı, model terfi ya da ret edildi, harcanan hold-out gücü defterde. **Bitti ≠ iyileşti.**
- **Faz bitti:** taze hold-out'ta kapılar ve kalibrasyon tutuyor, yeni ölçülen trafo ölçüyü artık oynatmıyor (plato). Yanlış yeşil oranı güven aralığıyla söylenebiliyor ve politikayı karşılıyor; "sayı bir kez güzel göründü" değil.
