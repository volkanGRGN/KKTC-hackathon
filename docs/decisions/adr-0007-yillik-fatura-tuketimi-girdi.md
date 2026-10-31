# ADR-0007: Büyüklük için trafo başına yıllık fatura tüketimi de girdi olur

Tarih: 2026-10-31 · Durum: kabul · ADR-0001'i tamamlar (değiştirmez)

## Bağlam
Şablon modelinin ilk sürümünde (PR #8, geliştirme şehirleri) öğlen en düşük yük hatası ortanca %8,6 ama P90 %32,6 (eşik %30). Hata tek büyük müşterili trafolarda yığılıyor: şehir konutu %4,5, köy %6,7; otel %21,5, yurt %22, çarşı %25, sanayi %22 [Hesap: `docs/log/2026-10-31-volkan-faz2.md`, gösterim]. Sebep: deneme şehrinde her büyük abonenin büyüklüğü rastgele (σ = 0,3) ve "sınıf başına abone sayısı" bunu göstermiyor; bir oteli öbüründen ayıran bilgi girdide yok.

ADR-0001 büyüklüğü "tarife sınıfı başına abone sayısı ile negatif olmayan regresyon" diye kurmuştu. İngiltere'de profil sınıfı yaklaşımı da yalnız müşteri sayısıyla değil müşteri başına tahmini yıllık tüketimle (Elexon "EAC") ölçekler [Yorum: hatırlanan, bağlantı doğrulanmadı].

Kıb-Tek ne bilir: her abonenin faturasını kesinlikle bilir; hangi abonenin hangi trafoda olduğu ise BULAMADIM (uzmana soru 2). Model zaten sınıf başına abone sayısı için bu eşleşmeyi varsayıyor; eşleşme varsa fatura toplamı da aynı anda bilinir. Yani yeni sütun yeni bir varsayım getirmiyor, aynı varsayımın üstüne biner.

Seçenekler: (a) `trafolar.csv`'ye `yillik_tuketim_mwh` ekle, model ölçeği bununla; (b) abone sayısıyla yetin, büyük müşterili trafolarda düşük güven etiketi; (c) sınıf başına kVA sözleşme gücü (Kıb-Tek endüstri II'de kVA'lı tarife var) — ama konut/ticari için yok.

## Karar
(a). Sözleşme §1'e `yillik_tuketim_mwh` (float, MWh, 2 hane): trafodaki abonelerin son 12 ay fatura toplamı; "Kıb-Tek'in bileceği" sütun (ayrım kuralı korunur). Üretici: abone başına yıllık enerjilerin toplamı × fatura sapması (tahmini okuma, farklı yıl) 0,95–1,05 [Yorum]. Model: ölçek regresyonunda sütun **varsa** kullanır, yoksa abone sayılarıyla çalışır (gerçek veri EDP'de fatura yok). Günlükte iki koşu yan yana: sütunlu ve sütunsuz (2d "hangi veri en çok işe yarıyor" bunun için zaten var). (b) ayrıca kalır: güven etiketi büyük müşterili trafoda düşer.

Sıra: PR #8 (sözleşme 1.1) olduğu gibi birleşir; bu değişiklik sözleşme 1.2 + üretici + model olarak ayrı küçük PR (Can ya da Civan onayı). Şehirler o PR ile yeniden üretilir (bayram listesi ve `kva_tavan_sayisi` de aynı üretime girer; can.md 13:55 KARAR).

## Sonuç
- Artı: Büyük müşterili trafoda hata düşmeli (ölçülünce yazılır; hedef P90 ≤ %30). Sunumda "Kıb-Tek'ten istediğimiz veri" listesi net: trafo başına sınıf sayıları + fatura toplamı, ikisi de bugün elinde olan şeyler.
- Eksi: Abone–trafo eşleşmesi varsayımı kalır; pilotta eşleşme yoksa saha sayımı gerekir. Fatura yılı ile Nisan öğleni arasındaki ilişkiyi model öğrenir, veri yoksa sapma [Yorum]. Gerçek veri (EDP) bu sütunu veremez; "sınıfsız ve faturasız" koşu ayrı başlıkta raporlanır.
