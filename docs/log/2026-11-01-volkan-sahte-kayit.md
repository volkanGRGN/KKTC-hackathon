# 2026-11-01 — Sahte Kıb-Tek kayıtları ve başvuru anı motoru (deneme)

**Amaç:** Karar masası 23:02, 23:03, 23:18 (Muhittin 3–4; ADR-0012, ADR-0015). Panel katmanı bırakılmıyor. Kıb-Tek'in vereceği kayıtlar (kademe, hat boyu, panelli abonenin hattı / yeri / fazı, inverter) deneme şehrinde **kusurlarıyla** taklit edilir; karar haritada değil başvuru anında, başvuranın kayıtlı yeriyle ve o ana kadar onaylanmış başvurularla verilir. Soru: kayıtlar gelirse kaç başvuruya hemen "evet" denir ve yanlış "evet" sınırın (%2) altında kalır mı. Resmi hesap ve resmi rakamlar değişmez.

## Yöntem
- **Gerçek ağ:** şehir üreticisinin ağı aynı tohumla yeniden kurulur (`sahte_kayit.gercek_sehir`; `sehir_kur` + `uretici13`), yük aynı akıştan. Sağlama: cevap anahtarının "gerçek kaç ev"i aynı yoldan yeniden hesaplandı, **şehir 1–2'de 78/80, 21–30'da 396/400 trafoda birebir**; farklılar bir–iki ev (kritik anlar yük dosyasının 0,1 V'a yuvarlanmış geriliminden sıralanıyor). `bilgi_degeri.py`'deki eski kurulum üretici 1.3'ün faz dengesini (`uretici13`) içermiyordu; burada içeriyor.
- **Sahte kayıt** (`src/sahte_kayit.py`, `kayitlar.csv`, sözleşme 1.4 adayı §7). Kusurlar [Yorum; gerçek oranlar Kıb-Tek'e sorulur]: kademe kaydı %80 doğru (%10 komşu kademe, %10 eksik); abone → trafo %95 doğru (yanlışsa kayıt bu trafoda yok); direk sırası ±2; faz kaydı %70 dolu, dolunun %90'ı doğru; hat boyu ±%15; inverter panelli evlerin %20'sinde (bara ±1 V, o hattın empedansı ±%20). Düzeyler: hatalar yarı / aynen / iki kat; kusursuz (hata yok, faz hep dolu; inverter yine %20). Başvuru formu (başvuranın hattı, yeri, fazı) aynı kusurlarla. Kayıt dosyası yazılıp geri okununca 40 trafoda fark 0.
- **Motor** (`src/basvuru.py`): olasılıklı hesabın aynı fiziği ve kapısı. Çekiliş kayda koşullu, kaydın hata payıyla: bara (inverter varsa sakin an gerilimi ±1 V, yoksa kademenin ±3,125 V penceresi %89 olasılıkla, yoksa 244–252 V), hat boyları kayıt × ±%15, kayıtlı evler kayıtlı hat ve yerde, faz kaydı %90 doğru, inverterli hatta empedans ölçülü ve model-sapma çarpanı yok (PR #20'deki iki düzeltme: inverter panelli evlerin %20'sinde, empedans yalnız inverterin hattında). Durumlu: onaylanmış başvurular ağda. Karar: P(sığar) ≥ 0,98 ve yük tahmininin güveni yüksek → evet; P(aşar) ≥ 0,5 → hayır; arası önce ölç. Model kayıt hatasını hep beklenen düzeyde varsayar (kusursuzda sıfır).
- **Test** (`src/basvuru_testi.py`): her trafoda panelsiz konutlardan rastgele sıralı başvuru akışı, 3 sıra × en çok 8 başvuru; evet alan sonrakine taahhüt olarak girer; gerçek: bu başvuru öncekilerle birlikte gerçek ağda 259 V ya da kVA'yı aşıyor mu (cevap anahtarının tanımı, 14 günün kritik anları). Aynı akışta %40 kuralı (onaylanan sayısı `kural40_ev`'e kadar evet) ve harita (yeşilse ilk iki başvuru evet). Ayar yok: eşikler resmi hesabınki. Şehir 1–10'da kuruldu, 21–30 bir kez koşuldu (üretici 1.3, model v2b, K_YUK 1,47).

## Sonuç: sınav 21–30 (bir kez) [Hesap; farazi şehir, gösterim]
| Senaryo | Hemen evet | Yanlış evet (evetlerin) | Önce ölç | Hayır (gerçekte sığan) | Harita yeşil / kırmızı | Kırmızıda gerçekte aşan |
|---|---|---|---|---|---|---|
| Kayıtsız (bugün) | %3,8 (276/7.179) | %0,7 (2/276) | %67,6 | %28,6 (1.016 sığıyordu) | 17 / 61 | %49 |
| Sahte, hatalar yarı | %11,9 | %0,2 (2/851) | %69,2 | %19,0 | 29 / 34 | %79 |
| **Sahte, beklenen** | **%10,5** (751) | **%0,1** (1/751) | %67,5 | %22,0 (550) | 30 / 41 | %63 |
| Sahte, hatalar iki kat | %10,7 | **%2,6** (20/770) | %68,8 | %20,5 | 35 / 41 | %63 |
| Kusursuz bilgi | %18,0 | %0,4 (5/1.295) | %61,1 | %20,9 | 26 / 38 | %84 |

- Aynı başvuru akışında **%40 kuralı evetlerinin %13,4'ü yanlış** (495/3.699); harita politikası (yeşilse ilk iki) yanlış evet 0–3.
- Harita kayıtlarla: yanlış yeşil her senaryoda 0.
- Hemen evet, şehir konutunda: kayıtsız 6/3.408 → beklenen 257/3.408 (%7,5) → kusursuz 680 (%20). Köy 0 → 42/1.344.
- **Yük tahmininin güvenine göre** (beklenen): güveni yüksek trafolarda başvuruların %20,6'sı hemen evet (kayıtsız %7,6, kusursuz %35,5); güveni yüksek olmayanlarda hiç evet yok (kural gereği), başvuruların yarısı (3.531/7.179) orada.

Geliştirme 1–10 (kurulduğu şehirler) aynı yön: hemen evet %4,2 → %12,9 (beklenen) → %20,9 (kusursuz); yanlış evet %0,0 / %0,6 / %1,5 (iki kat) / %0,3; %40 kuralı %14,3.

## Bulgular
1. **Kayıtlar gelirse hemen evet alan başvuru yaklaşık üç katına çıkıyor (%3,8 → %10,5), yanlış evet sınırın altında (%0,1).** Kırmızı trafo 61 → 41, kırmızıların gerçekte aşan payı %49 → %63 (yanlış kırmızı yarıya yakın iner).
2. **Eksi: kayıt hataları beklenenin iki katıysa yanlış evet %2,6, sınır %2'yi aşıyor** (geliştirmede %1,5). Model kayıtların hata payını bilmeli; Kıb-Tek kayıtlarının doğruluğu pilotta bir örnekle sahada ölçülmeden motor evet demez.
3. **Eksi: başvuruların üçte ikisi yine "önce ölç".** Yarısı, öğlen yükü tahmini yüksek güvenli olmayan trafolarda; orada kural gereği evet yok. Bu ağ kaydının değil yük tarafının (ölçüm, Faz 2 güveni) sınırı.
4. Hayır denenlerin bir kısmı gerçekte sığıyor (beklenen 550/1.581): motor güvenli tarafta; "hayır" kesin ret değil, önce ölçülür.
5. Yüksek güvenli trafolarda kusursuz bilgiyle bile evet %35,5: kalan belirsizlik öğlen yükü ve OG değişimi.

## Ne kaldı
- Sarı trafoda konum payı (`yesil_konum_payi`, ADR-0015 m. 4: "hattın ilk %x'inde başvuru yeşil") hesaplanmadı.
- Kaç ev bandı kayıtlarla ölçülmedi (yalnız renk ve başvuru kararı).
- Abone → trafo yanlışlığı yalnız kayıp olarak taklit edildi; başka trafonun abonesinin bu trafoya yanlış yazılması yok.
- Kayıt kusur oranları ve kademe penceresi (±3,125 V) varsayım; Kıb-Tek ve uzmana soru (istek taslağı).

## Deney defteri
| Tarih | Sürüm | Tohum | Hipotez | Sonuç | Karar |
|---|---|---|---|---|---|
| 31 Eki ~23:38 | motor v1, sahte kayıt NOMINAL | 1–10 | kayıtlar başvuru anında evet payını artırır, yanlış evet < %2 | %4,2 → %12,9; yanlış evet ≤ %1,5 | 21–30 bir kez |
| 31 Eki ~23:41 | aynı | 21–30 | aynı | %3,8 → %10,5, yanlış evet %0,1; iki kat hatada %2,6 | eksi bulgu karar masasına |
| 1 Kas ~00:10 | motor iki kat hata varsayar (karar masası 23:47) | 21–30 | iki kat kayıtta yanlış evet < %2 | %2,6 → %1,9 (14/722, 6 trafo); hemen evet %10,5 → %9,7 | [ayrı günlük](2026-11-01-volkan-panel-iki-kat-hata.md) |

<!-- Append-only: eskiyi değiştirme, yeni tarihli dosya ekle. -->
