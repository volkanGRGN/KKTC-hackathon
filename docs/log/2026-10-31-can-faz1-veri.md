# 2026-10-31 — Can: Faz 1 veri adımı

## Hipotez / amaç
ROADMAP Faz 1 "Yapılacaklar — veri" listesindeki adayları indirmek, sağlamak, KAYNAK.txt ve veri sözlüğüne yazmak. Eleme kararlarını Volkan onaylar.

## Yaptıklarım
Her aday için beş soru: (1) Kıbrıs/Akdeniz mi · (2) ölçülmüş mü · (3) ≤ 1 saat mi · (4) kaynak ve lisans var mı · (5) bu fazda kullanımı belli mi. Üçten az "evet" → elenir.

| Aday | 1 | 2 | 3 | 4 | 5 | Karar | Nerede |
|---|---|---|---|---|---|---|---|
| Open-Meteo Lefkoşa saatlik 2024–2025 | E | H (yeniden analiz) | E | E (CC BY 4.0) | E (hava yılı) | **alındı** 4/5 | `data/raw/open-meteo-lefkosa/` |
| EAC injection profilleri | E | E (Güney filosu) | E | yarım (lisans yok, kaynak var) | E (panel eğrisi sağlaması) | **alındı** 4/5 | `data/raw/eac-profil-siniflari/` |
| SimBench AG şebekeleri | H (Almanya) | H (temsili şebeke) | E | E (ODbL) | E (hat boyu, ev sayısı) | **alındı** 3/5, yalnız ölçü | `data/raw/simbench/` |
| Kıb-Tek kablo/trafo şartnamesi | E | – | H (internette yok) | H | E | **BULAMADIM** → Volkan'a soru | — |
| Otel doluluk aylık | E | E | E | E | E | elimizde (araştırma günlüğü bölüm 2) | — |
| Yurt yatak sayısı | E | – | H | H | E | BULAMADIM → varsayım (ADR-0004) | — |

## Sonuç
- [Hesap] Lefkoşa yatay yıllık ışınım 1.908 kWh/m² (2024), 1.929 (2025); Nisan 11–14 ortalaması 787 / 769 W/m²; Haziran tepe saati 12 (yerel saat doğru).
- [Hesap] EAC çatı güneşi (PVs_ROOFTOPS) Nisan iş günü tepesi 0,629 pu (13:00), 12:00 = 0,610 pu. Büyük güneş (PV_SYSTEMS) 0,706 pu.
- [Hesap] SimBench: trafodan en uzak eve 0,23–0,57 km, ortalama eve 0,09–0,20 km; trafo başına 13–118 yük; 160–630 kVA; kablo yer altı NAYY 150/240 (r 0,207 / 0,127 Ω/km). Aynı tipin kopyaları (40–111 adet) birebir aynı → 6 farklı şebeke var, fazlası değil.
- Benzetimle kıyas [Yorum]: benzetimdeki hatlar 180–420 m, hat başına 10–24 ev; SimBench'in kırsal/banliyö aralığına düşüyor. Kablo direnci SimBench'ten alınmamalı (yer altı, Kıbrıs havai ABC).
- Kıb-Tek şartnamesi: kibtek.com'da ve aramada ABC 70/95 direnci ya da kVA listesi bulunamadı. Veri sözlüğündeki "[Kaynaklı, hafızadan]" satırının belgesi BULAMADIM.

## Karar / sıradaki adım
- Volkan onayı bekleniyor: üç alınan, iki BULAMADIM.
- Soru (Volkan): Kıb-Tek trafo şartnamesi (25–400 kVA, 433 V) ve ABC kablo bilgisi hangi belgeden? Belge varsa `data/raw/kibtek-sartname/` açılır; yoksa benzetimdeki r 0,50 / 0,36 Ω/km "varsayım" etiketiyle kalır.
- Sıradaki: `src/profiller.py`.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
