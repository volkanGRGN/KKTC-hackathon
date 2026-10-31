# Can için istekler

Burası Can'ın kutusu; yalnız o işler. Kalıp için [README](README.md).

## UYARI! 31 Eki — Volkan'dan — Faz 1 veri adımı: iki BULAMADIM'a cevap
Ne: (1) **Kıb-Tek trafo/kablo şartnamesi:** bizde de belgesi yok. 30 Ekim'deki araştırmada şartname tarihleri not edilmiş (direk tipi 17.04.2018, yer tipi 24.09.2021) ama bağlantı kaydedilmemiş; bugün iki aramada (Türkçe teknik şartname, site:kibtek.com) bulunamadı. Veri sözlüğündeki "Kıb-Tek trafo şartnameleri [Kaynaklı, hafızadan]" satırını "kaynak bağlantısı yok, doğrulanmadı" diye işaretle; benzetimdeki kVA listesi, 250 V ve kablo dirençleri (r 0,50 / 0,36 Ω/km) "varsayım" etiketiyle kalsın. Bakılabilecek tek ipucu: ODTÜ Kuzey Kıbrıs kampüsünün trafo ihale dosyası (ncc.metu.edu.tr/sites/default/files/ihale-dosyasi-trafo17.pdf), Kıb-Tek'e uygun teknik değer içerebilir, kontrol edilmedi; zamanın kalırsa bak. (2) **Yurt yatak sayısı:** varsayım kararını onaylıyorum (ADR-0004).
Dosya: docs/data/data-dictionary.md, docs/log/2026-10-31-can-faz1-veri.md (kendi günlüğün; yeni girdi olarak)
Neden: kaynaksız rakam "kaynaklı" görünmesin; Faz 1 eleme kararı onayı. Yeni kural: CONTRIBUTING "Bulamadım akışı" — bundan sonra BULAMADIM'ları günlüğün yanında benim kutuma da yaz.
Durum: yapıldı 13:50 (veri sözlüğü işaretlendi; ODTÜ dosyasına erişilemedi, arama izi günlükte)

## UYARI! 31 Eki 12:10 — Civan'dan — veri sözlüğüne OSM satırı
Ne: "Elimizde" altına OSM kasaba satırı ekle: `data/raw/osm-kasaba/` — Girne merkez (~1 km × 1,1 km) bina ve yol geometrisi, OpenStreetMap, ODbL 1.0, indirildi 31 Ekim 2026. Ölçülü değil, gönüllü çizim. [Hesap] 974 bina (278'inde kat bilgisi), 330 yol. Yanlılık: binaların %89'unun türü belirtilmemiş; OSM'de trafo yok (konumlar farazi şehirden). Kullanım: Faz 4 harita altlığı. Lapta elendi (17 bina). Ayrıntı `data/raw/osm-kasaba/KAYNAK.txt`.
Dosya: docs/data/data-dictionary.md
Neden: her indirilen veri sözlükte satır olmalı (ROADMAP Faz 1 geçme sınavı); sözlük senin dosyan.
Durum: yapıldı 13:50
