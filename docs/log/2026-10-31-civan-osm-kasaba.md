# 2026-10-31 — Civan: haritanın altlığı için OSM kasaba verisi

## Hipotez / amaç
Faz 4 haritası (ROADMAP "Yapılacaklar — veri (Civan)") gerçek bir KKTC mahallesinin sokak ve bina haritası üzerine kurulacak. Aday Lapta ya da Girne'den bir mahalle; hangisinin OSM'de yeterince çizildiğini görmek ve indirmek. Tablo biçimi sözleşmesine bağlı değil, o yüzden sözleşme beklenirken yapıldı.

## Yaptıklarım
- Overpass API ile dört aday alanda (~1 km × 1 km) bina, yol ve trafo sayıldı.
- En dolu alan (Girne merkez) bina + yol geometrisiyle indirildi: `data/raw/osm-kasaba/girne_merkez.json`; adres ve sorgu `KAYNAK.txt`'de.
- Dosya Python ile okunup sayıldı (UTF-8).

## Sonuç
[Hesap] Aday karşılaştırması (bina / yol / trafo):
- Lapta merkez: 17 / 51 / 0
- Lapta sahil: 2 / 59 / 0
- Girne merkez: 973 / 330 / 0
- Girne Karaoğlanoğlu: 22 / 107 / 0

[Hesap] İndirilen Girne merkez: 974 bina, 330 yol; binaların 278'inde kat bilgisi var, %89'unun türü belirtilmemiş.

OSM'de hiçbir aday alanda trafo işaretli değil.

## Karar / sıradaki adım
- Girne merkez seçildi; Lapta OSM'de neredeyse boş.
- Trafo konumları farazi şehirden gelecek; haritada "örnek veri — gösterim" etiketiyle.
- Veri sözlüğüne satır Can'dan istendi (`docs/istek/can.md`).
- Sıradaki: tablo biçimi sözleşmesi gelince `app/ornek_veri.py`.

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
