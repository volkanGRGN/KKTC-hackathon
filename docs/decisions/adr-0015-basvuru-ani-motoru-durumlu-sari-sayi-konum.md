# ADR-0015: Başvuru-anı motoru durumlu ve haritayla aynı model; sarı düz renk değil sayı + konum; işletme kaldıraçları ayrı kategori

Tarih: 2026-10-31 · Durum: kabul (sunum sonrası, Faz 9) · ADR-0012 üstüne (onu tamamlar) · kaynak: Muhittin'in üçüncü cevabı, 4. madde ([günlük](../log/2026-10-31-muhittin-cevap-3-veri-dongusu.md)) · karar masası 21:20

## Bağlam
ADR-0012 sarı trafoda kararı başvuru anında, başvuranın adresiyle vermeyi seçti (sınanmadı). Muhittin güçlü onayladı: sarının %41 tabanı model cehaleti değil gerçek konumsal serbestlik; hiçbir trafo düzeyi veri bunu kaldırmaz, ancak başvuranın gerçek konumu kaldırır. Üç dikkat noktası ve tamamlayıcı yollar ekledi.

## Karar
1. **Motor durumlu:** başvuru-anı hesabı, taahhüt edilmiş ama henüz kurulmamış bağlantıları da sayar (ADR-0010 madde 2 kümülatif düşüm bu motorda yaşar); aksi hâlde tek tek sığan başvurular toplamda sığmaz.
2. **Aynı kapı, konuma koşullu:** yanlış yeşil < %2 bütçesi başvuru anında da geçerli; farazi şehirde ölçüsü "başvuru-anı yanlış evet oranı".
3. **Aynı model:** harita rengi ve başvuru-anı kararı aynı hesaptan çıkar (ADR-0011), gizli farklı kural yok; her karar sürüm + girdi + tohumla loglanır (ADR-0013 madde 5).
4. **Sarı düz renk değil, sayı + konum:** sarı trafoda harita "hattın ilk %x'inde yeşil, uçta kısıtlı" der; faz / konum verisi (bilginin değeri S4) sarının çoğunu "konuma bağlı yeşil"e çevirir. Sözleşme 1.4 adayı: `yesil_konum_payi` (hat boyunun yüzdesi).
5. **İşletme kaldıraçları ayrı kategori:** izin varsa kademe ayarı, faz dengeleme, inverter volt-var ile "sarı → ucuz aksiyonla yeşil"; ürün bunu ayrı etiketle gösterir, vaat etmez. Uzmana soru 10: Kıb-Tek'te bu üç kaldıraç için izin / uygulama var mı?

## Sonuçlar
- ROADMAP Faz 9 (Kıb-Tek kayıtları + başvuru-anı) bu beş maddeyle; Faz 11 kartına sarı "sayı + konum" gösterimi (Civan).
- Sunumda değişiklik yok; jüri cevabındaki "sınanmadı" etiketi kalır.
