# 2026-10-31 — Volkan (+ Claude, BUILD): olasılıklı hesabın gerçek veride geri-testi (İngiltere UKPN, 6 hat)

**Etiket: gerçek veri — İngiltere (UKPN), yaz 2014, 1 dk.** Kıbrıs değil; taşınan şey fizik ve yöntem.

## Hipotez / amaç
Olasılıklı kaç ev hesabı ([günlük](2026-10-31-volkan-faz3-olasilik.md), PR #15), farazi şehirde 97 yeşilin hiçbirinde yanılmadı. Ama hesap, şehri üreten benzetimle aynı fiziği kullanıyor. ADR-0010 madde 3: canlıya geçmeden yeşil kuralı gerçek veride geri-test edilir.

Soru:
- Yeşil kuralı "%98 güvenli" diyor. Gerçek bir hatta ölçülen panel kaynaklı gerilim yükselmesi, hesabın çekiliş dağılımının 98. yüzdeliğinin (P98) altında mı?
- Üstündeyse hesap riski küçük görüyor; bu yanlış yeşil yönü.

## Yaptıklarım
- `src/ukpn_olasilik.py`. Veriyi yalnız okur.
  - Hat modeli UKPN testinden ([PR #11](2026-10-31-volkan-ukpn-gerilim.md)): tek fider, 30 düğüm + uçta ev, bara gerilimi ölçülen, hat boyu akşam düşümünden.
- Ölçülen: UKPN'in tanımıyla öğlen eğimi (ΔV'nin evin birim üretimine, V/pu), Haziran–Ağustos 11–13.
- Çekilenler, olasılıklı hesapla aynı aralıklar; site başına 60 çekiliş:
  - panellerin hattaki yeri: üçte bir uca toplanmış, yoksa düz;
  - faz: iki durum, faz ölçümü bilinen ve Kıb-Tek gibi bilinmeyen;
  - hat boyu: akşam kestirimi kesin, ya da ×0,6–1,6 belirsiz.
  - Fiderdeki PV payı, fider faz gücünün evin birim üretimine eğiminden [Hesap].
- Gerçek bir hatta tek ölçülen değer var. Bu yüzden kural sınanırken bakılan şey şu: ölçülen değer çekilişlerin P98'inin altında mı?

## Sonuç

Model ÷ ölçülen oranı, çekilişlerin dağılımı. 1 = ölçülenle aynı; P98 ≥ 1 = ölçülen kapsandı.

**Faz bilinmiyor (Kıb-Tek'in durumu), hat boyu ×0,6–1,6 belirsiz:**

| Site | Düz model (eski) | P10 | Ortanca | P90 | P98 | Ölçülen P98'in altında mı | Ölçülenin sırası |
|---|---|---|---|---|---|---|---|
| Alverston Close | 0,52 | 0,70 | 1,03 | 1,52 | 1,84 | evet | %45 |
| **Bancroft Close** | 0,20 | 0,30 | 0,46 | 0,70 | **0,78** | **hayır** (ölçülen P98'in 1,3 katı) | %100 |
| Forest Road | 0,95 | 0,64 | 1,01 | 1,48 | 1,66 | evet | %48 |
| Maple Drive East | 0,78 | 1,40 | 1,98 | 2,99 | 3,15 | evet (hesap fazla karamsar) | %0 |
| Suffolk Road | 0,70 | 0,29 | 0,48 | 1,08 | 1,54 | evet | %87 |
| YMCA | 1,09 | 0,45 | 0,78 | 1,14 | 1,45 | evet | %80 |

- **Hat boyu kesin sayılınca** (akşam kestirimi) 6'nın 4'ü kapsanıyor. Suffolk da kaçıyor (P98 0,98).
- **Faz biliniyorken** (fiderin faz ölçümüyle) 6'nın 4'ü kapsanıyor; Alverston ve Bancroft kaçıyor.
  - Ölçülen faz gücünde diğer evlerin paneli neredeyse görünmüyor (eğim ~0). Panel yerini çekmek bir şey değiştirmiyor.
- Eski düz model 6 hattın 2'sinde yükselmeyi yarıdan az gösteriyordu (0,52, 0,20). Olasılıklı hesap Alverston'u kapsıyor, Bancroft'u kapsamıyor.

### Okuma
- **− Yeşil kuralı gerçek veride doğrulanmış sayılmaz.**
  - 6 hattın 1'inde (Bancroft) ölçülen yükselme hesabın "%98 güvenli" sınırının 1,3 katı. Kural %2 bütçe vaat ediyor, 6 hatta 1 ıskalama var.
  - 6 hat çok az; oran kesin değil. Ama "bütçe tutuyor" demek için kanıt yok.
- **Bancroft'un sebebi** (PR #11 günlüğü; [Yorum], kanıtı var): ev, yükün olmadığı ama panellerin olduğu bir kolda.
  - Akşam düşümü küçük (etkin boy 77 m), öğlen yükselmesi büyük.
  - Tek hatlı model bu kol yapısını göstermiyor. Kol yapısı ve hat boyu Kıb-Tek kaydında var mı, BULAMADIM (uzmana soru 3).
- **+ Hat boyu belirsizliğini katmak kapsamayı artırıyor** (4/6 → 5/6). Olasılıklı hesap şu an hat boyunu kesin alıyor; bu aralık ona da girmeli.
- **+ Maple'da hesap fazla karamsar** (ölçülen dağılımın altında). Faz bilinmeyince yük ve paneli fazlara rastgele dağıtmak orada yükselmeyi abartıyor. Güvenli yön.

## Karar / sıradaki adım
- Olasılıklı hesaba iki ekleme önerisi [Yorum]:
  - hat boyu belirsizliği (×0,6–1,6);
  - kol yapısı: çekilişlerin bir kısmında panelli evler yüksüz bir kolda.
  - Eklenirse farazi şehirde yeşil azalır. Ne kadar azaldığı ölçülecek.
- Canlı için: yeşil kuralının bütçesi (< %2) 6 hatla sınanamaz. Pilotta sarı trafoların ucunda öğlen gerilimi ölçülecek; ölçülen her hat bu geri-teste eklenir.
- Sunum: "yeşil dediğimiz farazi şehirde hiç yanılmadı; İngiltere'nin 6 gerçek hattında gerilim tahminimiz 5'ini kapsadı, birinde yükselmeyi küçük gördü. Bu yüzden canlıda yeşil önce pilotla sınanır."
- Karar masasına (volkan.md).

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
