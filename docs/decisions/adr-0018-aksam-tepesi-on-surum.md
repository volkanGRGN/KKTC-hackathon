# ADR-0018: Akşam tepesi ön sürümü — şablon yöntemi, İspanya-Mayıs artıklarından geniş bant, açık kör nokta etiketleri, sıcaklık düzeltme terimi, iki bileşenli eşzamanlılık

Tarih: 2026-11-01 · Durum: kabul (ön sürüm; yaz verisi gelince yeni ADR) · ADR-0001, ADR-0013, ADR-0014 üstüne · kaynak: Muhittin'in dördüncü cevabı madde 2 ve 4 ([günlük](../log/2026-10-31-muhittin-cevap-4-odak-tepe-kademe.md)) · karar masası 1 Kasım 00:30

## Bağlam
ADR-0014 yük katmanını ayrı bir tepe modeline bağladı. Üretici 1.4 (PR #21) deneme şehirlerine yılın tepesini ekledi (yaz ve kış haftası; tepe ayı çoğunlukla Ağustos / Temmuz, konutta akşam). Tek gerçek tepe verimiz İspanya EDP (Mayıs). Muhittin şablon yöntemini (ölçülü trafolardan eğri şekli, faturadan büyüklük; ADR-0001) **ön sürüm** olarak kabul etti, iki şart ve bir yapısal uyarıyla: şablon tepeyi sabit bir eğri gibi gömer, oysa tasarım tepesi bir kuyruk olayıdır (sıcak dalga akşamı); bu yüzden yöntem tepeyi **sistematik olarak az gösterir**, yani güvensiz yönde yanılır. Öğlen için ise "yük = fatura × oran + kalibre bant" yöntemi doğru (taban vadisi, davranış farkı az); öğlen net yükünü faturadan ayıran tek şey panelli evin kendi tüketimi.

## Karar
1. **Ön sürüm = şablon yöntemi, akşam penceresi.** Trafo tepesi, sınıf şablonunun akşam en yükseği × faturadan büyüklük. Çıktı ayrı dosya `tepe.csv` (sözleşme 1.4 adayı; sütunlar Can'ın önerisiyle: `tepe_kw`, P10 / P90, `tepe_saati`, `tepe_ayi`, `pf_varsayim` 0,95 [varsayım], `tepe_kva`, `bos_kva` + P10 / P90, `guven` = `on`).
2. **Bant İspanya-Mayıs artıklarından ve geniş:** gerçek Mayıs tepesine karşı trafo bazında bir-dışarıda artıklar; bant bu artıkların dağılımı + eğim belirsizliği (madde 4). Farazi şehre uydurulmaz (tüzük madde 3).
3. **Kör noktalar açık etiketli,** her tepe sayısının yanında: "Mayıs ≠ Temmuz" (gerçek veri bahar, Kıbrıs'ın bağlayıcı tepesi yaz akşamı) ve "klima kuyruğu (sıcak dalga) ölçülmedi". Etiket kalkması yaz ölçümüyle (Kıb-Tek tepe kayıtları ya da yaz yük etüdü; Faz 9 istek listesi).
4. **Sıcaklık düzeltme terimi:** tepe, şablon gününün akşam sıcaklığından **tasarım sıcaklığına** (Lefkoşa uzun seri, 10 yılda bir sıcak akşam) tepe–sıcaklık eğimiyle taşınır; eğim klima yükü payına uygulanır. Eğim Güney Kıbrıs sınıf verisinin sıcaklık aralığından ya da Kıbrıs ev / trafo verisinden; gelene kadar geniş aralık [Yorum] ve bu aralığın belirsizliği banda girer.
5. **İki bileşenli eşzamanlılık:** taban konut yükü √N çeşitlilikle (Velander tipi: N·a + b·√(N·a)), klima yükü yüksek eşzamanlılıkla (klimalı ev sayısıyla yaklaşık doğrusal; sıcak akşam herkesi aynı anda açtırır). Parametreler ölçülü trafolardan doğrudan (CF(N)) ya da Kıbrıs ev verisinden fit; gelene kadar Velander varsayılanı [Yorum], "ön".
6. **Güvenli yön haritada:** az gösterme eğilimi yüzünden haritanın "yük için boş" sayısı **P90 tepeden** (`bos_kva_p10` = `kva` − `tepe_kva_p90`); orta değer yan panelde.
7. **Öğlen yükü:** "fatura × oran + kalibre bant" (K_YUK 1,47) öğlen için üretim yöntemi olarak kalır; değeri bantta ve karara çevirmede. Panelli abonede öğlen net yükü ayrıca panelin kendi tüketimiyle düşülür (fatura net ise iki kez düşülmez). Modelin iddiası akşam tepesinde.
8. **Sınav:** hedef deneme şehirlerinin net yıl tepesi (`tepe_yil_kw`, üretici 1.4; 1.5 gelince yeni sınav şehirleri 31–40) ve İspanya Mayıs gerçek tepe (Can'ın maddesi: ortanca ≤ %15, P90 ≤ %35, %80 bant %70–90 [Yorum]). Ayar yalnız 1–10'da; sınav şehirleri her yöntem değişikliğinden sonra bir kez. Öneren ≠ puanlayan; resmi rakam karar masasının Mac koşusu.
9. **Kim yazar (üç oturum düzeni, DEVIR):** `src/tepe.py` ön sürümünü (madde 1–4, 6, 7) BUILD 1 yazar; iki bileşenli eşzamanlılık ve sıcaklık eğimi fitleri (madde 4–5) Can'ın B-Y2 PR'ı olarak aynı dosyaya gelir, BUILD 1 inceler. Tepe sınav kodu Can'ın; Can'ın yazdığı kısmı Civan ya da BUILD 1 puanlar.

## Sonuçlar
- Haritanın yük sayısı "ön, düşük güven, yaz verisiyle güncellenecek" etiketiyle ve geniş bantla çıkar (ADR-0014 m. 4); sunumda yalnız "sıradaki katman" cümlesi.
- Feda edilen: bugün dar bant. Kazanılan: bandın gerçek veriden gelmesi ve güvenli yönde okunması.
- Açık risk: İspanya Mayıs artıkları Kıbrıs Temmuz akşamını temsil etmez; eğim fit edilene kadar sıcaklık terimi varsayım. Kıb-Tek tepe verisi (istek listesi, Faz 9) gelince yeniden fit, sürüm numarasıyla (tüzük madde 4).

<!--
KURAL: Bu dosyayı sonradan DÜZENLEME. Karar değişirse yeni bir ADR yaz
ve bu dosyanın durumunu "superseded by ADR-XXXX" yap.
-->
