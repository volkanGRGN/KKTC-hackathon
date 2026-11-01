# 2026-11-01 — Can: sunum için kaba maliyet hesabı (ölçüm ve pilot)

**Etiket: [Hesap], kaba.** Amaç kesinlik değil, sunumda ve pitch şablonunun maliyet kutusunda kaynaklı bir mertebe (Can, 1 Kas: "mükemmel doğru olmasına gerek yok").

## Hipotez / amaç
Civan'ın pitch şablonunda "geliştirme / bakım maliyeti, toplam, geri ödeme" kutuları boş (volkan.md 09:46). Depoda hangi maliyet verisi var, onunla ne söylenebilir.

## Yaptıklarım
1. Depo tarandı: [Civan'ın ölçüm maliyeti günlüğü](2026-11-01-civan-olcum-maliyeti.md) (KTEMO birim fiyatları, EMO mühendis saati, Fluke 1736 fiyatı, TCMB kuru), [kapsamlı araştırma §5](2026-10-31-kapsamli-arastirma.md) (İngiltere izleme ve trafo maliyetleri), ADR-0006 (Kıb-Tek PV üretimi), KTEMO PİD Ekim 2024.
2. KTEMO'nun bu makinedeki dört belgesi okundu (`data/raw/ktemo-birim-fiyat/`): PİD birim fiyat listesi bina içi tesisat ve tek PV satırı (J1, "KW başına 800 €"); Rev.13 bina projesi ve kontrollük ücretleri; vize ücretleri; laboratuvar deney kapsamı. Trafo / OG donanımı, elektrik tarifesi, emisyon yok.
3. Birim: trafo başına ölçüm **18.589 TL** (taşınabilir kaydedici, cihaz 3 yılda 78 ölçüm, 2 gidiş × 2 saat mühendis) [Hesap: Civan'ın günlüğü, A tablosu]. Kur 55,8153 TL/€ (TCMB 30.10.2026) → **~333 €**.

## Sonuç [Hesap]

| Senaryo | Trafo | TL | € |
|---|---|---|---|
| Modelin ölçülü kümesi (n = 12) | 12 | 223.068 | ~4.000 |
| Ölçüm sırasının ilk 20'si (BUILD 2, ROADMAP Faz 10) | 20 | 371.780 | ~6.700 |
| Kıbrıs pilotu (konuşma notu: 120–170 trafo) | 120–170 | 2.230.680 – 3.160.130 | ~40.000 – 56.600 |
| Kıyas: her trafoya kalıcı cihaz (Civan, B tablosu) | ~6.400–6.700 | ~300 – 419 milyon | ~5,4 – 7,5 milyon |

- **Pilot, her trafoya kalıcı cihazın ~%1'i:** 3,16 milyon ÷ 300 milyon = %1,05; 2,23 ÷ 419 = %0,53.
- **Bir trafoyu ölçmek, bir evin panelinin ~%6'sı:** 6,5 kW [Yorum: ev başına güç, kaynaksız] × 800 €/kW [Kaynaklı: KTEMO PİD Ekim 2024, J1] = 5.200 €; 333 ÷ 5.200 = %6,4.
- **Başlangıç nakdi:** 18.589 TL, cihaz parasının 3 yıla bölünmüş hâli. İşe başlarken 3 cihaz = 3 × 344.046 = 1.032.138 TL (~18.500 €) [Hesap: Fluke 6.164 € × kur].
- Konuşma notundaki "~20 bin € + pens" (araştırma §5: 10 Hioki cihazı, yalnız donanım) ile bu tablo farklı şeyi sayıyor; tablo işçiliği de içeriyor. Sunumda tablo kullanılır, not düzeltildi.

**Dahil değil:** geliştirme ve bakım maliyeti (depoda yok; ekibin varsayımı olur, karar Volkan), Kıb-Tek personelinin eşlik süresi ve aracı, KDV / gümrük / nakliye, enflasyon (KTEMO fiyatları Ekim 2024).

**Hesaplanamayan:** geri ödeme (Kıb-Tek tarifesi / mahsuplaşma fiyatı yok), emisyon etkisi (Kıb-Tek şebeke emisyon katsayısı yok), trafo büyütmekten kaçınılan maliyet (Kıb-Tek trafo değişim maliyeti BULAMADIM, araştırma §5; yalnız İngiltere rakamı var). Okunmamış aday: KTEMO'nun "Kıb-Tek Yakıt Değişim Fizibilite" sunumu (346 MB, `data/raw/ktemo-dokumanlar/KAYNAK.txt`, kimse açmadı).

## Karar / sıradaki adım
- Sunum: [slaytlar.md](../sunum/slaytlar.md) "Maliyet" bölümü ve [konuşma notu](../sunum/konusma-notu.md) jüri sorusu 4 bu tabloyla.
- Civan'a (pitch maliyet kutusu) ve Volkan'a (dashboard `icerik.json`, Volkan'ın dosyası) kutu.
- Geri ödeme ve emisyon istenirse: tarife, emisyon katsayısı, Kıb-Tek trafo maliyeti aranır (Bulamadım akışı).

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
