# 2026-11-01 — Yük haritası: ilk sürüm ↔ bugünkü, aynı şehirlerde (BUILD 1)

**Amaç:** Volkan sunum için yük haritasının ilk sürümüyle bugünkünü panoda yan yana görmek istedi. Gece rakamları farklı şehirlerde ölçülmüştü (ilk sürüm üretici 1.4, sınav 21–30; bugünkü üretici 1.5, sınav 31–40); fark hem dünyadan hem modelden geliyordu. Burada iki kod aynı şehirlerde koşuldu, fark yalnız modelden.

**Etiket:** farazi şehir, gösterim. Rakamlar [Hesap: BUILD 1 koşusu]; resmi rakam KARAR / TEST'in Mac koşusu. Yöntem değişikliği yok, ayar yok.

## Yöntem
- **İlk sürüm:** `src/` 0991064'teki hâli (PR #24 birleşmesi, gece 01:58; Velander varsayılanı ve 10 yıllık tasarım sıcaklığı dahil). `git archive 0991064 src` ile ayrı klasöre çıkarıldı.
- **Bugünkü:** ana dal 7b0b836 (PR #26 Kıb-Tek kaydı girişi, #29 akşam gerilimi, #32 tepe saati sonrası).
- `sehir_uret.py`, `sablon.py`, `profiller.py`, `trafo_bos_kapasite.py` 0991064 ile ana dal arasında aynı (git diff boş): şehirler, ölçülü küme ve öğlen tahmini ikisinde de birebir; fark yalnız `tepe.py`.
- Şehirler üretici 1.5, tohum 1–10 (ayar) ve 31–40 (sınav), sıfırdan; Kıb-Tek kaydı yok (iki kod da kayıtsız aynı yoldan geçiyor). `--hava yil` (varsayılan).
- Ölçüler cevap anahtarına karşı, ölçülmeyen 280 trafoda. Dönem tanımı `tepe.py` `donem()`: gece 20–04, sabah 04–10, öğle 10–14, öğleden sonra 14–20; ilk sürümün saatine de aynısı uygulandı.

## Sonuç — sınav şehirleri 31–40 (bir kez üretildi; karşılaştırma koşusu, hiçbir şey ayarlanmadı)
| Ölçü | İlk sürüm | Bugünkü |
|---|---|---|
| Yılın tepesi hata ortanca / P90 | %6,7 / %15,3 | %5,8 / %15,1 |
| Sapma (ortanca, + = fazla tahmin) | +%1,4 | +%0,2 |
| %80 bant kapsama; gerçek P90 üstü | %99,6; 0 | %99,6; 0 |
| En kötü tek trafo | %31,7 | %31,4 |
| Tepe saati ±60 dk | %47,5 | %52,1 |
| İki aday saatten biri | — | %60,0 |
| Tepe dönemi | %60,7 | %69,3 |
| Yurt (35): hata / saat / dönem | %8,4 / %17,1 / %8,6 | %5,3 / %57,1 / %77,1 |
| Çarşı (58): hata ortanca / P90 | %15,5 / %25,8 | %13,8 / %25,7 |
| Doluluk hatası ortanca / P90 (yüzde puan) | 2,7 / 8,1 | 2,6 / 8,0 |
| ≥ %80 dolu: gerçek / P90 ile yakalanan / uyarı | 16 / 16 / 92 | 16 / 16 / 87 |
| ≥ %100 dolu: gerçek / yakalanan / uyarı; orta tahminle | 2 / 2 / 37; 0 | 2 / 2 / 34; 0 |
| Boş kapasitesi (temkinli) eksi trafo | 37 | 34 |
| Akşam gerilimi | yok | hata 3,5 V (P90 8,9); 207 V altı 2 / 2; "yeterli" 233'te 0 yanlış; 47 uyarı |

Geliştirme 1–10 aynı yönde: tepe %7,5 / %18,4 → %6,3 / %16,8; saat %42,1 → %48,2; dönem %58,9 → %68,9; yurt hata %10,2 → %4,2; ≥ %80 uyarı 119 → 114 (gerçek 17 / 17 ikisinde de); akşam gerilimi 207 V altı 1 / 1, "yeterli" 225'te 0 yanlış, 55 uyarı.

**Yeniden üretim tuttu:** bugünkü sürümün 31–40 rakamları tepe saati günlüğüyle birebir; ilk sürümün 31–40 rakamları üretici 1.5 yük günlüğünün (#29 kodu) rakamlarıyla birebir.

## Sütun sütun ve harita düzeyinde
- `tepe.csv`'de tepe, P90 ve boş kVA değişen trafo: 31–40'ta 262 / 400 (TEST'in 01:5x bulgusuyla aynı), 1–10'da 261 / 400. Değişimin ortancası %0,9 (1–10'da %0,7), en çok %19,9. Tepe ayı hiçbir trafoda değişmedi.
- Boş kapasitesi 5 kVA'dan ve trafo gücünün %5'inden fazla değişen: 31–40'ta 19 (yurt 14, çarşı 5), 1–10'da 21 (hepsi yurt); hepsinde boş kapasite arttı.
- "%80'den dolu olabilir" uyarısı: 31–40'ta 5 uyarı kalktı (çarşı 2, yurt 2, şehir konutu 1), hiçbiri gerçekte dolu değildi; eklenen uyarı yok. 1–10'da 5 kalktı, 0 eklendi.
- Tepe dönemi değişen: 31–40'ta 32 trafo (yurt 27, çarşı 5); bunlarda doğru dönem ilk sürümde 3, bugünküde 27.

## Bulgular
1. **+** Bugünkü sürüm her ölçüde ilk sürüm kadar ya da daha iyi; güvenli yön korunuyor (gerçek P90 üstü 0, dolu trafo kaçmıyor).
2. **?** Yurt kuralı (ticari II abonesi ve öğlen arketipi "akşam tepeli" ise konut eğrisi) 31–40'ta 5 çarşıya da dokundu; 1–10'da hiçbir çarşıya dokunmuyordu (PR #32 günlüğü 0 / 41). Dördünde tepe gerçeğe yaklaştı (ör. sehir-032 T10 +%11,5 → −%1,2); birinde (sehir-032 T24) tepe daha az tahmin ediliyor: −%15,9 → −%25,6, gerçek tepe yine bandın içinde. Dönem: 2 doğruya döndü, 2 yanlışa döndü, 1 ikisinde de yanlış. Kural değiştirilmedi; çarşı genelinde hata %15,5 → %13,8.
3. **?** KARAR'ın 1 Kasım 02:12 doluluk ölçümü (92 uyarı, 37 uyarı) PR #32 birleşmeden önceki kodla yapılmış; bugünkü kodla 87 ve 34. Pano içeriği buna göre güncellendi.
4. İspanya Mayıs tepesi (%15,4 / %36,1) iki sürümde aynı: `edp_test.py` 0991064'ten beri değişmedi.

## Panoda
- `dashboard/icerik.json`: akşam gerilimi kartı 1.5 şehirlerine (2 / 2, 233 "yeterli", 47 uyarı; önceki kart üretici 1.4'tendi), "%80'den dolu" kartı bugünkü koda (87 uyarı); rakam notuna sunum sürümü 1.5. Pano kodu değişmedi. Karşılaştırma kart olarak eklenmedi: sürümleri harita üzerinde yan yana gösteren canlı tahmin sayfası pano oturumunda yapılıyor (dal `dashboard/canli-tahmin`, eski sürümü depo tarihçesinden çalıştırıyor).
- İki modelin çıktısı iki veri seti olarak (yerel, git dışı): `data/synthetic/yuk-kiyas/1-ilk-surum-gece` ve `2-bugunku-ana-dal`, şehir 31–40 (trafolar, tahmin, kac_ev, tepe; cevap anahtarı kopyalanmadı). Açmak için: `DASHBOARD_VERI=data/synthetic/yuk-kiyas streamlit run dashboard/dashboard.py`, sol menüden veri seti.

## Yeniden üretim
```
git archive 0991064 src | tar -x -C <eski>; ln -s <depo>/data <eski>/data
.venv/bin/python src/sehir_uret.py 31 40 --cikti <kök>        # 1 10 aynı
.venv/bin/python src/sablon.py <kök> --yalniz-ana
.venv/bin/python <eski>/src/tepe.py <kök>                      # tepe.csv → tepe_eski.csv olarak sakla
.venv/bin/python src/tepe.py <kök> --aralik 31-40
.venv/bin/python src/kac_ev_olasilik.py <kök> --sehir 31       # pano panel bölümü için, her şehir
```

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
