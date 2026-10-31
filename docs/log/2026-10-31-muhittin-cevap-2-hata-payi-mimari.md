# 2026-10-31 — Muhittin'in ikinci cevabı: hata payı önceliği, çapalama, mimari, yeşil kararı

**Amaç:** Karar masasının dört sorusuna (docs/istek/muhittin.md, 16:50; Volkan iletti) Muhittin'in cevabını kaydetmek ve karara bağlamak. Cevap Volkan tarafından 17:05'te yapıştırıldı; metin aşağıda özetlendi, kararlar ADR-0009 ve ADR-0010'da.

## Cevabın özeti (Muhittin, 31 Ekim)
1. **Öncelik: girdi (fatura) > dış değişken > daha çok ölçüm.** 5→15 ölçümün hatayı kımıldatmaması ve faturanın 2,5 kat düşürmesi "etiket kıtlığı değil ayırt edici bilgi kıtlığı" demek. Fatura ağ genelinde zaten var; yalnız toplamı değil dağılımı da kullan (yüksek tüketen abone oranı, tarife karışımı, mevsimsellik). Dış değişken faturanın artığını kapatır; **her trafoda olmayan değişkeni modele koyma** (klima bireysel bilinmez, tarife/iklim bölgesi vekil). Daha çok ölçüm doğruluk için değil, dürüst doğrulama ve kalibrasyon için: "özellik değil sınav kâğıdı".
2. **Çapalama: tek tek dağılım yetmez; ilişkiler ve kuyruk.** Ortak dağılım (yük ↔ PV konumu, büyüklük ↔ şekil korelasyonları; en azından korelasyon matrisi), kuyruk (müşteri başına yük ve hat empedansının P90/P95), hat üzerinde PV konum dağılımı + faz ("uca kümelenme" olasılığı girdi olsun), trafo içi çeşitlilik (eşzamanlılık / ADMD). Aşırı uydurma: **İspanya donuk sınav, eğitim hedefi değil**; mutlak kW değil boyutsuz çapala (CV, şekil oranları, korelasyon işaretleri, metre başına empedans); nokta değil aralık çapala (CV 0,3–0,6 bandının her yerinde test); "farazi 8,6 / İspanya 10" farkı aşırı uydurma ölçeri, izlenmeye devam.
3. **Mimari dağınık değil, güven merdiveni.** Tek cümle: "Kıbrıs'ı ölçemiyoruz; yöntemi ölçebildiğimiz her şeyde kanıtlıyoruz, sonra uyguluyoruz." Basamaklar: farazi şehir (kontrollü gerçek) → İspanya (dış geçerlilik, yük) → İngiltere (dış geçerlilik, gerilim) → Kıbrıs pilotu (sahada kalibrasyon). Her basamağa tek iddia + tek rakam, hepsi aynı cins: **saf tahmine göre ne kadar iyi**. Manşet rakam **İspanya %25 → %10** (gerçek, örneklem dışı, Kıbrıs'ta ağ genelinde var olan girdiyle). İkinci vurgu dürüstlük rakamı: gerilimde 6 hattın 4'ü ±%40, 2 ıskalama uca kümelenme, zaten karamsar senaryoyla karar.
4. **Yanlış yeşil: karamsar senaryo gerekli ama yetmez; karamsar + kalibre güven + ölçüm tetiği.** Kural asimetrik: yeşil ancak karamsar tahmin limiti **marjla** geçiyorsa ve güven yüksekse; sarı = sınırda ya da güven düşük → sınırlı onay ya da ucuz/geçici ölçüm; kırmızı = karamsar aşıyor. Ölçümsüz yeşil verilir ama yalnız yüksek güven, rahat marj. Ölçüm cihazı rastgele değil sarılara. Ek: (a) **kümülatif**: yeşili o anki kalan paya karşı ver, onaylananı düş, mahalle birlikte taktığı için onayları bağımsız sayma; (b) **geri-test**: İspanya/İngiltere'de "yalnız ön bilgiyle yeşil deseydik kaç trafo aşardı", yanlış yeşil bütçesi (<%1–2) koy, eşikleri ona göre.

## Ne değişti
- ADR-0009: doğruluk önceliği ve çapalama kuralları (1, 2).
- ADR-0010: yeşil kararı — karamsar + güven + marj, üç kademe, kümülatif düşüm, yanlış yeşil bütçesi ve geri-test (4; ADR-0005 ve ADR-0002'yi tamamlar).
- Faz 5 hikâyesi "güven merdiveni" ve manşet rakam İspanya %25 → %10 (karar masası → BUILD, volkan.md).
- Bugün yapılacak / sunum sonrası ayrımı volkan.md KARAR'ında.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
