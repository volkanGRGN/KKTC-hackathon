# Kıb-Tek veri isteği — taslak (BUILD, 31 Ekim 2026 gece)

Karar masası 21:39 madde 2 (e): Faz 9'un verisi sunumdan önce gelmez, ama **istek metni şimdi** hazırlanır. **Gönderen Volkan**; ekip göndermez. Köşeli parantezleri Volkan doldurur. Kampta uzmana aynı konular soru 2–4 ve 6–10 olarak sorulur ([plan](../01-plan.md)); cevaba göre metin kısalır.

Gerekçe tek cümle: farazi şehirde "bilginin değeri" denemesi ([Faz 3 günlüğü](../log/2026-10-31-volkan-faz3.md)) panelli abonenin adresi ve fazı bilinince "dolu" dediğimiz trafolarda yanılmanın %27'den %4'e indiğini gösterdi [Hesap: farazi şehir, kusursuz bilgi üst sınırı]. Sarı trafolarda karar başvuru anında verilecekse ([ADR-0012](../decisions/adr-0012-sari-trafoda-karar-basvuru-aninda.md), [ADR-0015](../decisions/adr-0015-basvuru-ani-motoru-durumlu-sari-sayi-konum.md)) aynı kayıt gerekiyor.

Verdiğimiz sözler (tutabileceğimiz kadar):
- **Kişisel veri istemiyoruz.** Ad, soyad, kimlik ve sayaç numarası gerekmez. Abone yerine anonim bir sıra numarası yeter. Adres yerine trafo, hat ve direk numarası yeter.
- Ham veri **yayımlanmaz**: depomuz açık, ham veri depoya hiç girmez (`data/raw/` git dışı). Yalnız trafo düzeyinde toplamlar ve özet rakamlar, Kıb-Tek atfıyla.
- Kullanım: modelin doğrulaması ve pilot önerisi. Ticari kullanım yok.
- Sonuç Kıb-Tek'le paylaşılır: trafo trafo kapasite haritası ve sınama raporu.
- Kıb-Tek isterse önce küçük bir örnekle başlarız (tek bölge, 20–50 trafo).

---

## Metin

> **Konu:** Dağıtım trafolarında çatı güneş paneli kapasitesi — veri işbirliği talebi
>
> Sayın [ad, unvan],
>
> [Ekip / kurum adı] olarak, Kıb-Tek'in dağıtım trafolarına ölçüm cihazı takmadan "bu trafoya kaç ev daha panel bağlanabilir" sorusunu trafo trafo cevaplayan açık bir hesaplama aracı geliştiriyoruz. Araç Kıb-Tek'in zaten elinde olan bilgiyle (trafo başına abone sayısı ve fatura toplamı) çalışıyor. İspanya'da 29 gerçek trafoda, ölçmediğimiz trafolarda öğlen yükünü ortanca %10 hatayla tahmin etti. Gerilim hesabını İngiltere'de 6 gerçek hatta sınadık.
>
> Bekleyen başvuruları güvenle açmanın önündeki en büyük belirsizlik, panelli evlerin hattın neresinde ve hangi fazda olduğu. Bu bilgi bilinince hatalı "dolu" kararları belirgin biçimde azalıyor. Bu yüzden aşağıdaki kayıtları, **kişisel bilgi olmadan**, paylaşmanızı rica ediyoruz:
>
> 1. **Abone–trafo eşleşmesi:** her abonenin bağlı olduğu dağıtım trafosu (ve varsa hat / direk numarası), tarife sınıfıyla. Abone yerine anonim sıra numarası yeterli.
> 2. **Mahsuplaşmalı (panelli) aboneler:** bağlı oldukları trafo ve hat / direk numarası, kurulu güç (kWp), bağlantı tipi (tek faz / üç faz) ve tek fazlıysa hangi faz.
> 3. **Trafo başına fatura toplamı:** son bir yılın aylık ya da yıllık toplamı (kWh), tarife sınıfına göre. Mahsuplaşma sayaçlarında çekilen ve verilen enerji ayrı kayıtlıysa ikisi ayrı.
> 4. **Trafo listesi:** güç (kVA), tip (direk / yer), yaklaşık konum, kısa devre gerilimi (uk, plaka bilgisi). **Her trafonun kendi kademe ayarı:** devreye alma kaydı ya da son ayar kaydı (genel standart değil, trafo başına); kayıt yoksa ayarın nasıl belirlendiği.
> 5. **Hat kaydı:** trafo başına alçak gerilim hat sayısı, hat boyları ve kablo kesitleri; özellikle hat uçlarındaki kesit.
> 6. **Bekleyen başvurular:** trafo bazında sayı ve istenen güç (kWp).
>
> Bu kayıtların tamamı gerekmiyor. Yalnız 1 ve 2 bile, başvuru geldiğinde o ev için "sığar / önce ölç / sığmaz" kararını vermemize yetiyor. Kayıtların hangi biçimde tutulduğunu (dijital, kâğıt, coğrafi bilgi sistemi) öğrenmek de bizim için değerli.
>
> Veriyi yalnız bu çalışmada kullanacağız, yayımlamayacağız ve sonuçları sizinle paylaşacağız. İsterseniz tek bir bölgede 20–50 trafoluk bir örnekle başlayabiliriz.
>
> Saygılarımızla,
> [Ad Soyad, iletişim]

---

## Göndermeden önce (Volkan)
- [ ] Kime: Kıb-Tek dağıtım / planlama birimi; muhatap adı kampta uzmandan (soru 1–2).
- [ ] Kampta uzmanın cevabıyla kısalt: hangi kayıt dijital, hangisi yok (soru 2–4, 6–10).
- [ ] Kişisel veri mevzuatına uygunluk: anonim numara ve trafo / hat düzeyi yeterli; adres istenmiyor.
- [ ] Rakamlar: İspanya %10 [Hesap: PR #10]; "%27 → %4" farazi şehir üst sınırı, metne konmadı, konuşmada etiketiyle.
- Kademe neden trafo başına (BUILD, 31 Ekim 23:15): PV açılma denemesinde (PR #20, gerçekçi şehirler) Kıb-Tek'in iki değerli kademe *standardını* bilmek açmadı (adım 6,25 V, belirsizlik 8 V'tan dar değil); açan, trafonun kendi ayarı. Gerçekçi kayıt hata oranları (kademe kaydı ne kadar doğru, abone–trafo eşleşmesi, faz kaydının doluluğu) kampta uzmana sorulur; sahte kayıt testi bu oranlarla kurulur (ROADMAP Faz 9).
- [ ] Yük haritası öne alındı (karar masası 23:12): tepe kalemleri (Muhittin 4 madde 3: trafo maksimum talep kayıtları ya da yaz yük etüdü, OG fider tepe geçmişi + sıcaklık, ticari / sanayi kayıtlı maksimum talep) bu metne eklensin mi, konu satırı yük + panel mi olsun: karar masasında.
