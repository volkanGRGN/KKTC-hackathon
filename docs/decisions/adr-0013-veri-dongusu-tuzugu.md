# ADR-0013: Veri döngüsü tüzüğü — hold-out ayrımı, iki kapı (yanlış yeşil, kalibrasyon), gerçeğe karşı kalibrasyon, sürümlü yeniden-fit

Tarih: 2026-10-31 · Durum: kabul (sunum sonrası uygulanır) · ADR-0009, ADR-0010, ADR-0011 üstüne · kaynak: Muhittin'in üçüncü cevabı ([günlük](../log/2026-10-31-muhittin-cevap-3-veri-dongusu.md)) · karar masası 21:15

## Bağlam
Sunumdan sonra iş, modeli gerçek veriyle iyileştirmek. Bilginin değeri denemesi kusursuz bilgide bant kapsamasının %80'den %57'ye düştüğünü gösterdi (hesap kendinden fazla emin). Önerdiğimiz sırada aynı ölçüm hem modeli hem deneme şehri üreticisini ayarlıyordu; Muhittin bunun test setini modele sızdıracağını söyledi.

## Karar (değişmezler; her görev kartı buna referans verir)
1. **Hold-out ayrımı.** Gelen her ölçülü trafo partisi ikiye bölünür: **ayar** (model + üretici) ve **doğrulama** (hiç dokunulmaz). İspanya, İngiltere ve pilotun doğrulama payı dokunulmaz kalır. Gerçek hold-out'a her bakış günlüğe yazılır ("istatistik gücü harcar").
2. **İki kapı, sonra iyileştirme.** "Model iyileşti" ancak dokunulmamış gerçek trafolarda (ya da modelin görmediği yeni üretilmiş şehirlerde): (1) yanlış yeşil ≤ %2 **ve** (2) kalibrasyon toleransta ise; sonra sarı + yanlış kırmızı küçülmüşse. Kapı tutmazsa iyileşme sayılmaz. Aynı şehirlerde metrik oynaması iyileşme değildir.
3. **Kalibrasyon gerçeğe karşı.** Bant kapsaması, PIT histogramı ve nominal–ampirik kapsama eğrisi gerçek doğrulama verisinde ölçülür; yalnız üreticiyle ölçülmez. Fazla eminlik düzeltilmeden bant yayınlanmaz: gerçek artıklardan model-sapma terimi (Kennedy–O'Hagan) ya da hold-out'ta konformal / şişirme katsayısıyla post-hoc kalibrasyon.
4. **Güncelleme periyodik ve sürümlü.** Sessiz online daraltma yok; sayı ya da sapma tetiklediğinde yeniden-fit, sürüm numarasıyla. Tüm ham veri saklanır. Çerçeve hiyerarşik: popülasyon dağılımı + ölçülen trafonun kendi değeri (ölçülen noktaya çöker, popülasyon öncülü ölçülmeyenler için güncellenir).
5. **Her rakam kaynağa iner:** ham veri kimliği + betik + commit + tohum; model + üretici + veri birlikte sürümlenir, her sonuç üçlüyü anar.
6. **Hedefler türetilir:** doğrulama hedefi istatistiksel (0 ihlalle %95 güvenle "< %2" için ~150 bağımsız karar noktası, 3/n kuralı); ayar hedefi plato (gerçek – üretilen dağılım mesafesi düzleşene kadar), sayı değil.
7. **Sıra:** trafo çıkış gerilimi ucuz ilk adım ama ~%19 yanlış kırmızıda platoya oturur; büyük kazanç abone–trafo, adres ve faz kaydında (ADR-0012 başvuru-anı kararıyla). Ucuz inverter verisi gece kör; yük tarafı için ayrı (ADR-0014).

## Sonuçlar
- `docs/tuzuk.md` (ana oturum yazar): yukarıdaki yedi madde + veri partisi görev kartı şablonu (Muhittin'in 3. maddesinin devamı gelince tamamlanır).
- `src/kalibrasyon.py` adayı: PIT, kapsama eğrisi, şişirme katsayısı (sunum sonrası).
- ROADMAP "sunum sonrası" fazları bu tüzüğe göre (karar masası 21:15, volkan.md).
