# ADR-0019: Yeşil ve başvuru anı "evet" kapısında "yük güveni yüksek" şartı kalkar; kalibre yük bandı yeter, güven bilgi etiketi olarak kalır

Tarih: 2026-11-01 · Durum: kabul (koşullu: madde 3'teki sınav tutarsa yürürlüğe girer) · ADR-0010, ADR-0011, ADR-0013, ADR-0015, ADR-0017 üstüne · kaynak: BUILD 1 ölçümü (volkan.md UYARI, main 5c88e24), BUILD 2 bulguları (PR #28, #30) · karar masası 1 Kasım 01:30

## Bağlam
Panel katmanında yeşil (ve başvuru anı motorunda "hemen evet") bugün iki şart ister: iki başvurunun bant çekilişleriyle %98 sığması **ve** öğlen yük tahmininin güveninin "yüksek" olması (ADR-0010). İki ayrı ölçüm aynı yeri gösterdi: evet'in darboğazı ağ kaydı değil bu güven şartı. Trafoların %57'sinde güven yüksek değil (PR #28); renksiz trafoyu yeşile çeviren tek ölçüm trafo başında öğlen yükü ve yeşile dönenlerin hepsi bugün güveni orta / düşük trafolar (PR #30).

BUILD 1 güven etiketini ölçtü [Hesap; farazi üretici 1.4 ve İspanya gerçek veri]:
- **Etiket hatayı ayırmıyor:** 21–30'da yüksek / orta / düşük güvende hata ortancası %11,1 / %11,1 / %13,0; İspanya'da (girdi c, tabakalı) yüksek %13,9, orta %8,7, yani ters. Etiketin girdisi arketip olasılığı; hatayı abone sayısı ve büyük abone haber veriyor.
- **Güvenlik zaten bantta:** panel için tehlikeli yan (gerçek öğlen yükü < P10) her güven sınıfında nominal %10'un altında: 21–30 %9,2 / %2,7 / %0, İspanya %2,4 / %2,1 / %6,0. Güven şartı güvenlik eklemiyor, yalnız seçiyor.
- **Karşı-olgu** (panel kodu değişmeden, var olan çıktılarla): şart orta + düşük güvene açılınca yeşil 1–10'da 20 → 47, 21–30'da 17 → 47; yanlış yeşil 0, ilk iki başvuru sözü bozulan 0 (%95 üst sınır ~%6). Konut yeşili değişmiyor (0–1): konutta darboğaz gerilim fiziği ve ağ bilgisi.

## Karar
1. **Kapı:** yeşil ve başvuru anı "hemen evet" için iki başvurunun (ya da bu başvuru + taahhütlerin) yük bandından çekilen 40 senaryonun %98'inde sığması yeter; "güven yüksek" şartı kalkar. Kırmızı / bayrak kuralı değişmez.
2. **Ön şart bant kalibrasyonudur:** kapı ancak yük bandının tehlikeli yanı (gerçek < P10) her güven sınıfında nominal %10 + n toleransı içinde kaldıkça geçerli; gerçek veride (İspanya; pilot gelince Kıb-Tek) her yeniden-fitte ölçülür (tüzük m. 3). Bozulursa güven şartı (ya da o sınıf için bant şişirme) geri gelir.
3. **Sınav (yürürlük şartı):** BUILD 2 uygular (`kac_ev_olasilik.py`, `basvuru.py`); 1–10'da kurulur, **dokunulmamış üretici 1.5 şehirleri 31–40'ta bir kez** ölçülür: yanlış yeşil (kapı ≤ %2, en kötü şehirde ≤ %10), ADR-0017 bayrak isabeti, başvuru akışında yanlış evet; TEST oturumu bağımsız tekrarlar. 21–30 bilgi (daha önce görüldü).
4. **Güven etiketi** yan panelde bilgi olarak kalır. Yeniden tasarımı (abone sayısı, büyük abone, fatura) ayrı iş; bu kararın şartı değil.

## Sonuçlar
- Beklenen (farazi, karşı-olgu): yeşil yaklaşık %5 → %13; konutta değişmez. Başvuru anında hemen evet artar, 31–40'ta ölçülecek.
- Feda edilen: etiketle yapılan "emin olmadığımız yerde evet deme" seçimi. Kazanılan: kapı ölçülen güvenliğe (bant) dayanır, haber vermeyen bir etikete değil.
- Açık risk: yeşil sayısı küçük (47); yanlış yeşil < %2'yi %95 güvenle göstermek ~150 bağımsız yeşil ister (tüzük m. 6). Canlıda yeşil yine pilotla sınanır.

<!--
KURAL: Bu dosyayı sonradan DÜZENLEME. Karar değişirse yeni bir ADR yaz
ve bu dosyanın durumunu "superseded by ADR-XXXX" yap.
-->
