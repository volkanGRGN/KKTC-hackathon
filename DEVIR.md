# Devir notu — şu an nerede kaldık

Bu dosya tek sayfa, anlık durum. Her faz sonunda ve iş devrederken Volkan (+ Claude) günceller; eski hali silinir, geçmiş [docs/log/](docs/log/) altında. Yeni gelen ya da yeni oturum: önce bunu, sonra [README](README.md) ve [Faz 0](docs/02-faz-0-ogrenim.md).

**Güncellendi:** 31 Ekim 2026, öğleden sonra (BUILD oturumu)

## Durum
- Fikir: trafo görünürlük haritası (MVP), güneş paneli ilk uygulama katmanı. Gerekçeler [docs/decisions/](docs/decisions/).
- **Faz 1 bitti.**
  - 20 deneme şehri gerçek girdilerle üretildi: EAC eğrileri, Lefkoşa ışınımı, panel yaygınlığı %3–25 ([ADR-0006](docs/decisions/adr-0006-panel-yayginligi-bugunun-kibrisi.md)).
  - Geçme sınavının beş maddesi geçti. Altıncı madde açık: 3 trafo 216 V altında (karar masasında, bloklamıyor).
  - Konut ve köy trafolarının %27'si bugünden 259 V üstünde.
  - Ayrıntı: [Faz 1 günlüğü](docs/log/2026-10-31-volkan-faz1.md), ek girdi.
- **Faz 2 sürüyor.**
  - Şablon modeli `src/sablon.py` [PR #8](https://github.com/volkanGRGN/KKTC-hackathon/pull/8)'de; sözleşme 1.1 aynı PR'da, Can ya da Civan onayı bekliyor.
  - Ön bakış, şehir 11–20 (ayar yapılmadan bir kez ölçüldü):
    - doğru arketip %93;
    - öğlen hatası ortanca %8,6, P90 %32,6 (eşik %30);
    - bant kapsama %82;
    - düşük güven %18.
  - Ayrıntı: [Faz 2 günlüğü](docs/log/2026-10-31-volkan-faz2.md) (PR dalında).

## Açık faz ve kim nerede
- **Volkan + Claude:**
  - PR #8 birleşsin.
  - 2i: İspanya EDP gerçek verisinde model (Can veriyi hazırladı; tarife sınıfı yok, girdi toplam müşteri + kVA).
  - Sonra Faz 3 (`src/kac_ev.py`). Faz 3 kartına not: 264 V üstü benzetim değeri fiziksel değil, inverter kapanır.
- **Can:** [Faz 2 kartı](docs/gorev/can-faz2-sinav-grafikler.md).
  - `sinav.py faz2` resmi ölçüm.
  - `grafikler.py` (kalibrasyon, kaç trafo ölçmeli).
  - EDP incelendi, kullanılabilir.
- **Civan:** harita iskeleti (`harita/iskelet` dalı). Yan panel `tahmin.csv` / `arketipler.csv`'yi sahte veriyle gösterir ([kartının sonu](docs/gorev/civan-faz1-ornek-veri-harita.md)).

## Bekleyen istekler
- Karar masasında (volkan.md):
  - 216 V eşiği;
  - Kıb-Tek'in trafo başına yıllık fatura tüketimi (büyük müşterili trafolarda kalan hatayı kapatır);
  - Can'ın EDP bildirimi ve PR #6 notları (bayram günleri, 1000 kVA tavanı).
- Can'ın "arketip oranı brüt mü" sorusu: brüt; PR #8'de sözleşmeye yazıldı.
- Kontrol: `grep -n "Durum: bekliyor" docs/istek/*.md`

## Bilinen sorunlar ve kararlar
- Ham veri depoda yok; KAYNAK.txt adreslerinden indirilir.
- **Sanal ortam şart** (`pip install -r requirements.txt`). `openpyxl` yoksa üretici sessizce yer tutucu eğriye düşer; `ayar.json`'da `profil_kaynagi` = `eac` olduğuna bak.
- Trafo çıkışı 246–250 V rastgele (şartname 250, belgesi yok).
- Model ayarları yalnız şehir 1–10'da denendi. 11–20 sınav için ayrı tutuluyor; yeni deneme yaparken 11–20'ye bakarak ayar değiştirme.
- Sunum saati bilinmiyor; sıra var, saat yok.

## Sıradaki üç adım
1. PR #8'i Can onaylasın, birleşsin. Can `sinav.py faz2`'yi gerçek `tahmin.csv` ile koşsun, ROADMAP Faz 2 kutuları rakamla dolsun.
2. Karar masası fatura tüketimi önerisine karar versin. Evetse üreticiye ve sözleşmeye sütun eklenir, model yeniden ölçülür.
3. Faz 3 kartları ve `src/kac_ev.py`: kaç ev daha sığar, yeşil/sarı/kırmızı, %40 kuralıyla yan yana.
