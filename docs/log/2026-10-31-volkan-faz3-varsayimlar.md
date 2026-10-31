# 2026-10-31 — Volkan (+ Claude, BUILD): Faz 3 varsayım envanteri ve etkileri

## Hipotez / amaç
Faz 3'ün kırmızısı ve kaç ev sayısı yanlış çıkıyor:
- yanlış kırmızı %42, sarı %63, kaç ev hatası 3,5 ev ([Faz 3 günlüğü](2026-10-31-volkan-faz3.md));
- bara gerilimini bilmek de az düzeltiyor (yanlış kırmızı %42 → %37).

Kural (Volkan'ın kod inceleme rehberinden, 31 Ekim): ölçülmemiş sayı tahminle yazılmaz. Her varsayım ya ölçümden gelir ya "ölçülmedi" diye işaretlenip etkisi ölçülür. Amaç, hangi varsayımın sonucu ne kadar oynattığını görmek ve olasılıklı hesaba aralıkları buradan vermek.

## Yaptıklarım
- `src/kac_ev.py`'deki (PR #13) bütün sayıları ve yapı varsayımlarını listeledim.
- Her birini makul aralığında **tek tek** oynattım; diğerleri karamsar varsayılanda.
- Yalnız geliştirme şehirleri 1–10'da ölçtüm (354 trafo, 56'sı dolu). Sınav şehirlerine bakılmadı. Betik scratchpad'de (`duyarlilik.py`), dosya yazmaz.
- Ölçüler:
  - kırmızı kuralı (b) ile kırmızı payı, yanlış kırmızı, yakalanan dolu;
  - sarı ve yeşil payı, yanlış yeşil;
  - karamsar "bugünkü hat ucu gerilimi"nin gerçek en yüksek gerilimden sapması (ortanca) ve sıra uyumu (Spearman);
  - kaç ev hatası (tavansızlarda).

## Sonuç

### Envanter: sayılar nereden geliyor

| No | Varsayım | Değer (karamsar / iyimser) | Kaynak | Ölçümle karşılaştırma |
|---|---|---|---|---|
| K1 | Trafo çıkış (bara) gerilimi | 250 / 246 V | karar masası 16:27 [Yorum] | UKPN: siteler arası yayılım 12 V, ss 3,3 V; Kıbrıs BULAMADIM |
| K2 | Öğlen orta gerilim yükselmesi | +%0,8 / 0 | eski benzetimin OG çarpanı [Yorum] | **UKPN'le çelişiyor:** öğlen bara ortancası 244,0 V, gece 245,0 V. Öğlen ~1 V (−%0,4) düşük, yükselmiyor [Hesap, PR #11]. Aynı +%0,8 şehir üreticisinde de var |
| K3 | Yükün ucu | P10 / P90 | Faz 2 bandı | ölçülü (Faz 2 sınavı) |
| K4 | Mevcut panelin en kötü fazdaki payı | 0,5 / ⅓ | [Yorum] | UKPN dengesizliği kentsel ortanca %14, P84 %30 → pay 0,38 / 0,43; kırsal ~%50 → 0,5 [Hesap] |
| K5 | Mevcut panelin hattaki yeri | hat boyunun ⅔'ü / ½'si | [Yorum] | UKPN: 6 hattın 2'sinde paneller uçta toplanmış; dağılım BULAMADIM |
| K6 | Hat üstündeki yük panel akımını azaltır mı | hayır / evet | [Yorum] | ölçülmedi |
| K7 | En uzun hattın trafodaki payı | eşit pay ile boy payının büyüğü / eşit | [Yorum] | Kıb-Tek'te hat başına abone BULAMADIM (uzmana soru 2) |
| K8 | Öğlen güneşi | 998 W/m² × 0,82 | [Hesap: Open-Meteo Nisan en yüksek saat] | ölçülü |
| K9 | Yeni panelin yeri | hat ucu / ortası | karar masası 16:27 (UKPN) | UKPN 2/6 hat |
| K10 | Yeşil marjı | payın %10'u, en az 1 ev | ADR-0010 [Yorum] | ölçülmedi |
| — | Trafo direnci (uk %4, X/R 2), kablo dirençleri | — | benzetimle aynı; kablo [Kaynaklı: SimBench] | ölçülü (kablo); trafo [varsayım] |
| — | Yapı: tek denklem, yalnız en uzun hat, evler eşit aralıklı, reaktif güç yok | — | [Yorum] | ölçülmedi |

### Etki (şehir 1–10, tek tek oynatma)

| Varsayım → değer | Kırmızı | Yanlış kırmızı | Yakalanan dolu | Sarı | Yeşil | Yanlış yeşil | Bugünkü gerilim sapması | Sıra uyumu |
|---|---|---|---|---|---|---|---|---|
| **Şimdiki karamsar** | %25 | %53 | %73 | %71 | %4 | 0 | +2,3 V | 0,75 |
| K1 bara 244 V | %10 | %29 | %43 | %69 | %21 | 0 | −3,7 V | 0,75 |
| K1 bara 248 V | %18 | %46 | %63 | %73 | %9 | 0 | +0,3 V | 0,75 |
| K1 bara 252 V | %35 | %62 | %84 | %63 | %2 | 0 | +4,3 V | 0,75 |
| K2 OG 0 | %18 | %46 | %63 | %73 | %9 | 0 | +0,3 V | 0,75 |
| K2 OG −%0,4 (UKPN gibi) | %16 | %40 | %59 | %72 | %12 | 0 | −0,7 V | 0,75 |
| K2 OG +%1,2 | %32 | %60 | %80 | %66 | %2 | 0 | +3,3 V | 0,75 |
| K4 faz payı ⅓ | %13 | %40 | %50 | %83 | %4 | 0 | +0,7 V | 0,75 |
| K4 faz payı 0,43 (UKPN kentsel P84) | %21 | %51 | %64 | %75 | %4 | 0 | +1,7 V | 0,75 |
| K4 faz payı 0,6 | %33 | %60 | %82 | %64 | %4 | 0 | +2,8 V | 0,75 |
| K5 panel yeri ½ | %18 | %46 | %63 | %78 | %4 | 0 | +1,4 V | 0,75 |
| K5 panel yeri 1 (uçta) | %36 | %63 | %84 | %61 | %3 | 0 | +3,5 V | 0,75 |
| K6 hat yükü azaltır | %13 | %47 | %45 | %62 | **%25** | 0 | −2,9 V | 0,71 |
| K7 eşit pay | %21 | %48 | %70 | %75 | %4 | 0 | +1,8 V | 0,76 |
| K8 güneş 900 / 1050 W/m² | %22 / %26 | %52 / %54 | %68 / %75 | %73 / %71 | %5 / %3 | 0 | +1,9 / +2,5 V | 0,75 |
| K9 yeni panel hat ortasında | %25 | %53 | %73 | %54 | **%22** | 0 | +2,3 V | 0,75 |
| K9 yeni panel ¾'te | %25 | %53 | %73 | %66 | %9 | 0 | +2,3 V | 0,75 |
| K10 marj %0 / %20 | aynı | | | | | | | |

- Yük ucu (K3) neredeyse hiç etki etmiyor: karamsarda yük yalnız trafo direncinden geçiyor, o da küçük.
- Kaç ev hatası (iyimser 3, karamsar 9 ev) hiçbir karamsar varsayımıyla değişmiyor.
  - İyimser bara 250 V'ta 4 ev oluyor.
  - İyimser yeni paneli tek faza koyunca 7 ev oluyor.
  - Hata hesabın yapısından geliyor.

### Okuma
- **− Kırmızıyı hiçbir ayar düzeltmiyor.**
  - K1, K2, K4, K5 aynı "bugünkü gerilim" tahminini birkaç volt yukarı ya da aşağı kaydırıyor. Hangisini oynatsak aynı eğri üzerinde kayıyoruz: kırmızı azalınca yakalanan dolu da azalıyor.
  - Trafoları doğru sıraya dizme gücü (Spearman 0,75) hiçbirinde değişmiyor.
  - Kırmızının kalitesini artırmak için **yeni bilgi** gerekiyor, ayar değil:
    - panelin hattaki yeri (Kıb-Tek panelli abonenin adresini biliyor);
    - fazı;
    - bara gerilimi (tek başına az: yanlış kırmızı %42 → %37, sınav şehirleri).
- **− Ölçümle çelişen bir varsayım var: K2.**
  - Öğlen orta gerilimin yükseldiğini (+%0,8) varsayıyoruz. İngiltere'de öğlen bara gerilimi geceden ~1 V düşük.
  - Aynı varsayım şehir üreticisinde de var, yani deneme şehirlerinin "gerçeği" de bunu içeriyor.
  - Üreticiden ve hesaptan çıkarmak üretici 1.3'e aday. Sonucu: deneme şehirlerinde gerilimler ~2 V düşer, kırmızı azalır.
- **+ Ölçümle desteklenen:**
  - güneş (K8);
  - faz payı (K4): UKPN kentsel P84 → 0,43; kırsal ~0,5.
  - Karamsarın 0,5'i kırsal için ölçüme uyuyor, kentsel için biraz karamsar.
- **? Yeşil iki varsayıma çok duyarlı, ikisi de karar masasının kararı.**
  - Yeni panel hat ortasında (K9) ya da hat yükü panel akımını azaltır (K6) desek yeşil %4 → %22–25 oluyor. Şehir 1–10'da yanlış yeşil yine 0.
  - Ama karamsar senaryonun amacı "bir sonraki başvuru hattın neresinde olursa olsun sığar". UKPN'de 6 hattın 2'sinde paneller uçta toplanmıştı.
  - Gevşetmek yanlış yeşil bütçesini (< %2) gerçek veride sınamadan yapılmamalı.
- **Olasılıklı hesaba girdi:**
  - Her ölçülmemiş varsayım tek değer yerine bir aralıkla çekilecek. Aralıklar yukarıdaki "ölçümle karşılaştırma" sütunundan, mümkünse gerçek veriden; şehir üreticisinin kendi değerinden değil (ADR-0009: farazi şehre uydurma yok).
  - Aksi hâlde olasılıklı hesap deneme şehirlerinde, üreticiyi bildiği için, olduğundan iyi görünür.

## Karar / sıradaki adım
- Kendi yetkimde, şimdi: hiçbir sayıyı değiştirmedim. Bu ölçüm ayar için değil, envanter için.
- Karar masasına:
  - K2'yi (OG öğlen yükselmesi) üretici 1.3'te ve hesapta UKPN'e göre 0 ya da eksi yapmak;
  - K9 / K6 (yeşil gevşetme) gerçek veride geri-test olmadan değişmez.
- Sıradaki: olasılıklı hesap, ayrı dalda (Volkan, 31 Ekim akşam). Aralıklar bu envanterden.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
