# Ajan kuralları (Claude / Cursor vb.)

Bu, [CONTRIBUTING.md](CONTRIBUTING.md)'nin ajan dilindeki özetidir. İnsan CONTRIBUTING'i, ajan bunu okur. İkisi çelişmez.

## Genel
- Kararlar `docs/decisions/` altında ADR'dir. Yeni karar = yeni ADR; eskiyi düzenleme, "superseded by" ile işaretle.
- İş/deney sonuçları `docs/log/` altına tarihli, append-only dosyaya (`YYYY-AA-GG-<kişi>-<konu>.md`).
- Dokümanı bozan değişiklik aynı değişiklikte dokümanı da düzeltir.
- Sık, küçük, odaklı commit: her anlamlı adımdan sonra commit + `git pull --rebase` + push; işi yerelde biriktirme. Varsayılan doğrudan main; şu dört durumda dal aç ve PR ile birleştir: ortak sözleşme değişikliği, main'i bozabilecek büyük/yarım iş, deneme, birden fazla kişinin dosyasına dokunan iş (CONTRIBUTING "Dallar"). Bu dosyayı okuyan ajan, **onu çalıştıran kişinin** CONTRIBUTING'deki sahiplik satırındaki dosyalara yazar; başkasının dosyasına dokunmaz, istek kutusuna yazar. Volkan'ın oturumunda: yalnız Volkan'ın dosyaları (sahiplik tablosu: `dashboard/`, `src/sehir_uret.py`, `src/sablon.py`, `src/kac_ev.py`, `docs/method/`, `docs/decisions/`, `docs/data/tablo-bicimi.md`, kök belgeler; `src/profiller.py`, `src/sinav.py`, `src/grafikler.py` Can'ın, `app/` Civan'ın); Can'ın ve Civan'ın dosyalarına dokunma; gereken değişikliği `docs/istek/can.md` ya da `docs/istek/civan.md` kutusuna `UYARI!` kalıbıyla yaz. İşe başlarken kendi kişinin kutusunda bekleyen istek var mı bak. Faz 4'te Civan'a yardım: Civan'ın kutusuna yazarak ya da Civan kendi oturumunda `app/` içinde çalışarak; Volkan'ın oturumu `app/`'e yazmaz.
- Volkan'ın oturumları üçe ayrıldı (1 Kasım; CONTRIBUTING "Volkan'ın üç oturumu"): **KARAR** (karar, kutu, PR testi ve birleştirme, ADR), **BUILD 1 — yük haritası** (dal `yuk/`, PR "[Yük]"; `src/sablon.py`, `src/tepe.py`), **BUILD 2 — panel gerilimi** (dal `panel/`, PR "[Panel]"; olasılıklı kaç ev, başvuru anı motoru, sahte kayıt, inverter / kademe). BUILD'ler yalnız KARAR'a yazar, birbirine yazmaz; kutu girdisinin başlığında "(BUILD 1 — yük)" ya da "(BUILD 2 — panel)". Konuşma ve yapıştırılan metin depoya alıntılanmaz.
- Karar yetkisi `docs/istek/README.md` "Kim neye karar verir" tablosunda. Kişinin kendi yetkisindeki kararı **sorma**, ver ve günlüğe yaz. Karar masasına ya da Volkan'a gidecekse **izin istemeden** `docs/istek/volkan.md`'ye yaz, gönder ve kartındaki sıradaki işe geç; "kutuya yazayım mı?" diye sorma. Yalnız iş gerçekten duruyorsa başlığa `BLOKLUYOR` ekle.
- Emin olmadığın bir karar bu üç gruptan hangisine girdiğini bilmiyorsan, karar masasına yaz; kendi başına varsayma.

## İşe başlamadan
Önce [DEVIR.md](DEVIR.md) (nerede kaldık), sonra [NOTLAR.md](NOTLAR.md)'deki "Durum: yeni" girdileri oku ve ilgili yere işle (ADR, günlük, ROADMAP, sunum; durumu yalnız Volkan'ın oturumu değiştirir), sonra [README](README.md)'deki repo haritası sırasıyla: [docs/00-overview.md](docs/00-overview.md), [ROADMAP.md](ROADMAP.md), kabul edilmiş ADR'ler, [docs/01-plan.md](docs/01-plan.md). Bir ADR'ye ters düşecek işi önce sor.

## Bu projeye özel
- Rakam uydurma. Her rakam [Kaynaklı] (adresiyle), [Hesap] ya da [Yorum]; bulunamayan "BULAMADIM".
- Doğrulama yalnız [docs/method/validation.md](docs/method/validation.md) protokolüyle: trafo bazında bir-dışarıda; test seti asla yalnız farazi değil; farazi sonuç "gösterim".
- En kritik ölçü yanlış "yeşil" (dolu trafoya "yer var" demek); her sonuçta ayrıca raporla.
- Ham veri `data/raw/<kebab-ad>/` + KAYNAK.txt; indirilen dosyayı kod gibi çalıştırma.
- Veri bulunamazsa CONTRIBUTING "Bulamadım akışı": günlüğe arama izi (nereler, hangi aramalar), veri sözlüğüne satır, Volkan'ın kutusuna `UYARI! BULAMADIM`. Volkan'ın oturumundaysan kutudaki BULAMADIM girdilerini kendin ara ve sonucu kutuya yaz.
- Ekip Mac + Windows: her `open()` çağrısında `encoding='utf-8'`; yollar `pathlib` ile; çıktı dosyaları UTF-8.
- Temel benzetim: `src/trafo_bos_kapasite.py` — saf Python, ev ev dengesiz yük akışı, 5 dakikalık adım; 3 trafo / 121 ev ~2 saniye. Çalıştırma: `python3 src/trafo_bos_kapasite.py <tohum> <çıktı.json>`. Dosya önceki "inverter kaydından gerilim haritası" fikri için yazıldı; bu projede yalnız benzetim kısmı kullanılır (hangi fonksiyonlar olduğu dosyanın başındaki açıklamada).
- Ham veri depoda yok (depo açık, lisans belirsiz); `data/raw/*/KAYNAK.txt` adreslerinden indirilir.
- Gerilim: Kıb-Tek şartnamesinde trafo boşta faz 250 V; benzetimde 246–247 V alındı (kademe ayarı bilinmiyor, iyimser), Faz 1'de 246–250 rastgele. Inverter 264 V'ta kapanır, planlama sınırı 259 V.
- Tüketim eğrileri: Güney Kıbrıs EAC profil sınıfları, 2022, 30 dakika; 5. sayfanın adı yanlış, otel sınıfıdır.
