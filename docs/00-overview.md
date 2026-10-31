# Genel Bakış

Tarih: 2026-10-31

## Amaç

**Ürün (MVP):** Kıb-Tek'in bugün göremediği mahalle trafolarını az sayıda ölçümden öğrenen bir modelle haritada görünür kılmak: her trafo için öğlen doluluk, tahminin aralığı ve güveni. Az sayıda trafo ölçülür, gerisi İngiltere'nin "ağ şablonları" yöntemiyle tahmin edilir.

**İlk uygulama ve sunum hikâyesi:** çatı güneşi. Harita her trafo için "kaç ev daha panel takabilir" der ve başvuruyu ayırır (yeşil / sarı / kırmızı). Aynı harita başka sorulara da açılabilir (akşam yükü, trafo yenileme önceliği); hackathonda yalnız panel katmanı yapılır.

## Neden şimdi

- [Kaynaklı] Kuzey'de ~2.670 çatı başvurusu bekliyor; Kıb-Tek'in alçak/orta gerilim izleme sistemi yok (KTTO, Mart 2023).
- [Kaynaklı] Güney bağladı, 2025'te dağıtıma bağlı güneşin %47,44'ünü kıstı, Ocak–Mayıs 2026 %65 (pv magazine).
- [Kaynaklı] İngiltere 824 trafoyu (%2,6) ölçüp gerisini ~%80 doğrulukla tahmin etti; başka şirketlerin 284 trafosunda %80–90.

## Kullanıcı ve karar

Kıb-Tek planlama birimi. Araç **ret vermez**: yeşil → hızlı onay, kırmızı → işaret, sarı ya da düşük güven → ölçüm cihazı (ya da esnek onay). Son karar insanın; itiraz eden gerçek ölçüm isteyebilir.

## Kapsam (hackathon, 48 saat)

Fazlar ve geçme sınavları [ROADMAP.md](../ROADMAP.md)'de; burada yalnız başlıklar:
- Faz 1, deneme şehirleri: 20–30 rastgeleleştirilmiş farazi Kıbrıs şehri (her biri ~40 trafo, 7 tip).
- Faz 2, modeli eğitme ve sınama: kümeleme → atama → ölçekleme; hedef bahar öğleni en düşük yük; bant, kalibrasyon, güven etiketi.
- Faz 3, panel katmanı: kaç ev sığar; trafo ısıl payı ve hat ucu gerilim payının küçüğü; yeşil/sarı/kırmızı.
- Faz 4, ürün: trafo görünürlük haritası.
- Faz 5, sunum ve prova.

## Kapsam dışı

- Gerçek Kıb-Tek verisi (elimizde yok; pilot önerisi olarak sunulur).
- Derin öğrenme, Fourier katsayıları, havaya bağlı dinamik model, saat altı çözünürlük.
- pandapower'a geçiş (saf Python benzetim yeterli).
- Esnek Onay'ın kodu (tek slayt seçenek).
- Kıb-Tek'e başvuru yapan vatandaş arayüzü.

## Başarı ölçütü

- Sunumdan önce: her trafo için sayı + bant + güven + renk veren, uçtan uca çalışan hat ve onu gösteren panel.
- Farazi şehirlerde **yanlış yeşil oranı** şehirler arası aralıkla raporlanmış (önerilen hedef ≤ %5, [Yorum]).
- %80 bandın gerçekte ~%80'i kapsadığı kontrol edilmiş.
- Varsa İspanya'nın gerçek trafolarında bir-dışarıda sonucu; yoksa açıkça "gerçek doğrulama yok, kanıt İngiltere".
- Jüri ölçütleri (eşit): inovasyon, sürdürülebilirlik etkisi, teknik uygulanabilirlik, pazar, sunum.

## Paydaşlar

- Lider: Volkan
- Ekip: Can Şahin, Civan Orak
- Muhatap/müşteri: Kıb-Tek planlama birimi (hedef kullanıcı); hackathon jürisi
- Danışman: Muhittin
