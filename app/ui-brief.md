# UI brief — trafo haritası (Civan, 31 Ekim 2026)

Bu belge, **harita sayfasını** (`app/harita.py`) yeniden tasarlayacak ajan (Gemini) için tek kaynaktır. Okuyan başka bir şeye bakmadan işe başlayabilmeli. **Veri mantığı hazır ve doğru; iş yalnız görünüm ve düzen.**

> **Senin işin yalnız harita sayfası (bölüm 1–6, 8–10).** Dashboard ve sunum ekranları (bölüm 7) Claude'da, `app/sunum.py` ve `app/dashboard.py` dosyalarında; o dosyalara dokunma. `app/ornek_veri.py`'ye de dokunma.

## 1. Amaç

Jüri (teknik olmayan, Kıbrıs'ı ve elektrik şebekesini bilmeyen insanlar) ekrana baktığında 10 saniyede şunu anlamalı:

> "Kıb-Tek, evlerin bağlı olduğu mahalle şebekesini göremiyor. Bu harita onu görünür kılıyor: her direkteki kutu (trafo) yeşil, sarı ya da kırmızı; bugünkü %40 kuralı ise çoğu yerde yanlış söylüyor."

Bugünkü ekranın sorunları: sol menüde yalnız şehir seçici var; harita küçük ve dağınık; renklerin ve sütun boylarının ne anlama geldiği yazmıyor; gerçek şehirde sütunların çoğu aynı kısa boyda; panel metin yığını.

## 2. Değişmez kurallar (çiğnenirse iş geçersiz)

1. **Yalnız `app/` içinde çalış.** `src/`, `docs/data/tablo-bicimi.md`, `data/raw/` (osm-* hariç) ve kök belgelere dokunma.
2. **Veri sözleşmesi:** tablolar [docs/data/tablo-bicimi.md](../docs/data/tablo-bicimi.md) sürüm 1.2'ye göre okunur. Yeni sütun uydurma; gereken sütun yoksa çizme, bildir.
3. **`cevap_anahtari.csv` asla okunmaz.** `yuk_5dk.csv`'den yalnız `tahmin.csv`'de `olculdu = 1` olan trafoların satırları okunur (bugünkü `olculu_yuk()` aynen kullanılsın).
4. **İnternetsiz çalışmalı:** dış CDN, Google Fonts, harita karo sunucusu yok. Zemin `data/raw/osm-kasaba/girne_merkez.json` (yoksa Streamlit'in varsayılan zemini).
5. **Dürüstlük etiketi her ekranda:** şehir no ≥ 900 → "SAHTE VERİ — gösterim"; 800–899 → "GERÇEK ÖLÇÜM — <veri_kaynagi> (Kıbrıs değil)"; diğerleri → "örnek veri (farazi şehir) — gösterim". Bugünkü `etiket()` aynen.
6. **Gerçek şehir gelince kod değişmez:** yalnız `data/synthetic/<şehir>/` klasörü değişir. Eksik tablo (`tahmin.csv`, `kac_ev.csv` yok) çökme değil, sade görünüm.
7. Türkçe arayüz metni, teknik terim yok (arketip, kVA, P10, karamsar yerine düz Türkçe; teknik ad yalnız küçük "ayrıntı" satırında). UTF-8, `pathlib`, `open(..., encoding="utf-8")`.
8. Tıklamadan panelin açılmasına ≤ 1 saniye (bugün 0,37 sn).

## 3. Teknik zemin

- Python 3.10+, **Streamlit ≥ 1.39 + pydeck** (bugünkü yığın; değiştirme). Kurulum ve komutlar: [app/README.md](README.md).
- Veri üretmek: `python app/ornek_veri.py` (sahte 901–903; bütün sözleşme tablolarını içerir, tasarım için yeter). Gerçek kaç ev tablolu şehir (sehir-011, -012) yalnız Civan'ın bilgisayarında; yoksa sahte şehirle çalış, Civan gerçek şehirde dener.
- Bugünkü kod: `app/harita.py`. Veri fonksiyonlarını **yeniden kullan** (`birlesik_tablo`, `olculu_yuk`, `tahmini_egri`, `olculen_egri`, `osm_zemin`, `etiket`, `kac_ev_metni` mantığı). Dosyayı bölmek serbest (ör. `app/ui/stil.py`, `app/ui/panel.py`); `streamlit run app/harita.py` çalışmaya devam etmeli.
- Streamlit menüsünü ve "Deploy" düğmesini gizle (`.streamlit/config.toml` depoya girmiyor → `st.set_page_config` + CSS ile).

## 4. Ekran düzeni (harita ekranı)

```
┌───────────────────────────────────────────────────────────────────────┐
│ Mahalle şebekesi haritası · Girne    [şehir: ▾ sehir-011]  [SAHTE VERİ]│  üst şerit
├───────────────────────────────────────────────┬───────────────────────┤
│                                               │  Trafo T37            │
│                                               │  ● YEŞİL              │
│              3D harita (≈ %65)                 │  En kötü durumda      │
│                                               │  bile yer var         │
│                                               │  ───────────────      │
│                                               │  Kaç ev daha: 2–7     │
│                                               │  Bugünkü kural: 61 ⚠  │
│  ┌ Lejant ─────────────────┐                  │  ───────────────      │
│  │ ● yeşil ● sarı ● kırmızı │                  │  [gün boyu eğri]      │
│  │ sütun boyu = trafo gücü  │                  │  ayrıntı (küçük)      │
│  └─────────────────────────┘                  │                       │
├───────────────────────────────────────────────┴───────────────────────┤
│  40 trafo · yeşil 1 · sarı 14 · kırmızı 25 · %40 kuralı 23'ünde fazla söz veriyor │  alt şerit
└───────────────────────────────────────────────────────────────────────┘
```

- **Sol menü (sidebar) kaldırılır.** Şehir seçici üst şeride, yatay.
- Hiçbir trafo seçili değilken sağ panel boş durmaz: şehrin özeti ve "Bir direğe tıkla" yönlendirmesi.
- Alt şerit: şehrin tek satırlık özeti; "%40 kuralı kaç trafoda bizim en iyimser tahminden fazla söylüyor" sayısı (yalnız `kac_ev.csv` varsa; `kural40_ev > kac_ev_iyimser`).

## 5. Harita katmanları

| Katman | Veri | Görünüm |
|---|---|---|
| Binalar | `girne_merkez.json`, kat × 3 m | koyu gri-mavi, hafif saydam, 3D |
| Yollar | aynı dosya | ince, açık gri |
| Kıyı (yeni) | `data/raw/osm-kasaba/girne_kiyi.json` (yoksa çizilmez) | denizi ayıran ince, açık mavi çizgi (`PathLayer`); denizi dolgu olarak boyamak isteğe bağlı |
| Trafolar | `trafolar.csv` + `kac_ev.csv` | silindir; **renk = karar** (`renk`), **boy = trafo gücü** (`kva`, ör. 1000 kVA ≈ 250 m) [Civan'ın kararı: kaç ev çoğu gerçek trafoda 0, boy anlamını yitiriyor]; seçili trafo beyaz halka ya da parlama |
| Ölçülü trafolar | `tahmin.csv` `olculdu = 1` | renkli silindirin üstünde küçük işaret (ör. beyaz nokta) — "burada ölçüm cihazı var" |

- Kamera: açılışta şehrin bütün trafolarını kapsayacak şekilde (bugünkü ortalama merkez yetmiyor; sınır kutusuna sığdır), eğim 45°.
- Renk paleti (renk körü dostu, koyu zeminde okunur): yeşil `#2EA043`, sarı `#F0B41E`, kırmızı `#D2322D`, gri (karar yok) `#969696`. Zemin `#0E1117` (Streamlit koyu).
- Tooltip: "T37 · yeşil · 2–7 ev".

## 6. Yan panel (mantık hazır, yalnız görünüm)

Sıra ve metin [Faz 3 kartı](../docs/gorev/civan-faz3-yan-panel.md) ve bugünkü `yan_panel()` ile aynı:
1. Büyük renk rozeti + tek cümle (yeşil "En kötü durumda bile yer var", sarı "Sınırda ya da emin değiliz, önce ölç", kırmızı "En kötü durumda yer yok").
2. "Kaç ev daha panel takabilir: 2–7 ev" büyük; altında "Bugünkü kural (%40): 61 ev" — farklıysa vurgulu kutu (kırmızı: kural fazla söz veriyor; mavi: kural gereksiz bekletiyor).
3. "ölçüldü / ölçülmedi" ve güven rozeti.
4. Gün boyu eğri (ölçülü: ölçülen; ölçülmeyen: tahmin + bant gölgesi). Eğri başlığı düz Türkçe: "Bu trafonun gün boyu yükü (tahmin, %80 aralık)".
5. Küçük "ayrıntı": güç (kVA), bölge, abone, panel, bağlayan sınır.

## 7. Bilgi: dashboard ve sunum (Claude'un işi — Gemini bu bölümü UYGULAMAZ)

- **Dashboard = veri ve hesap.** Şebeke doluluğu, kaç trafo yeşil/sarı/kırmızı, %40 kuralıyla fark, ölçülen/tahmin edilen sayısı gibi rakamlar ve grafikler. Ayrı sayfa (`st.navigation`), haritadan bağımsız. Sunumun 7 ekranı da burada (Volkan 17:32: "sunum dashboard'un içinde, 7 ekran"; metin Can'ın, `docs/sunum/`).
- **Harita = görsel.** Aynı veriyi 3D gösterir (bölüm 4–6). Gerçekçi direk/trafo/ev modelleri Blender'da yapılıp glTF olarak haritaya konabilir (Civan'ın kararı; Volkan 17:32'de "Blender animasyonu yok" dedi — bu, animasyon içindi; modeller için Volkan'a ayrıca söylenmeli).
- Biri ötekinin yerine geçmez; ikisi de yapılır.
- Geçiş ekranı (Volkan 17:32): 3. ekrandan 5. ekrana **"noktalar çoğalıyor"** animasyonu: adanın sade hat çizimi (OSM KKTC sınırı ya da sade SVG); önce tek ölçülen nokta, sonra ikinci, üçüncü; ardından tahmin dalga gibi yayılır, bütün mahallelerde noktalar çoğalır; son karede canlı haritaya geçilir.
- Animasyon kuralları: ölçülen trafo **dolu/kalın**, tahmin edilen **içi boş ya da soluk**; yayılan noktalar Faz 3 renkleriyle (yeşil / sarı / kırmızı), hepsi yeşil değil; köşede "gösterim — farazi şehir"; ada geneli noktalar temsilidir, gerçek trafo yeri değil. Noktalar **pop** ile belirir (0 → %115 → %100, 0,3–0,4 sn; tahminler küçük gruplar hâlinde dalga gibi), fade değil.
- Uygulama önerisi: pydeck `ScatterplotLayer` + `transitions={"getRadius": 350}`, ya da `st.components.v1.html` içinde CSS keyframes; hangisi 20 dakikada çalışırsa. Veri: bir şehrin `tahmin.csv` (`olculdu`) ve `kac_ev.csv` (`renk`). Yedek: Can'ın 4 kare PNG'si sırayla.

## 8. Yapılmayacaklar

Yeni veri ya da indirme, `src/`'de değişiklik, sözleşmede olmayan sütun, internetten yüklenen font/ikon/karo, cevap anahtarı. Blender modelleri ayrı iş (Civan): bu brief'te trafolar silindir kalır; glTF model gelince yalnız katman değişir.

## 9. Bitti sayılması için

- [ ] Sidebar yok; şehir seçici üst şeritte; etiket her ekranda.
- [ ] Lejant renkleri ve sütun boyunu açıklıyor; alt şeritte şehir özeti.
- [ ] sehir-901 (sahte), sehir-011 (gerçek kaç ev), sehir-001 (yalnız trafolar) üçü de hatasız açılıyor; eksik tabloda gri ve sade.
- [ ] Yan panel: sehir-011 T37 → yeşil, 2–7 ev, kural 61 vurgulu; sehir-012 T05 → "panelsiz konut yok".
- [ ] Tıklama → panel ≤ 1 sn; tarayıcı yalnız `localhost` istiyor (Geliştirici araçları → Ağ).
- [ ] 1280×800 ve 1920×1080'de taşma yok.
- [ ] Ekran görüntüsü (önce / sonra) günlükte: `docs/log/2026-10-31-civan-ui.md`.

## 10. Çalışma düzeni

- Dal: `harita/ui` (main'e PR; Civan bakar). Sık commit, `git pull --rebase` yalnız kendi dalına; main'i almak için `git merge origin/main`.
- Commit mesajı: `harita: ne yaptı`; imza satırı (Co-Authored-By vb.) yok.
- Emin olmadığın bir karar: kod yazmadan Civan'a sor.
