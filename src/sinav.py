#!/usr/bin/env python3
"""Geçme sınavı ölçüleri: üretilen şehirleri ROADMAP eşiklerine göre ölçer.

Modeli ya da üreteci yazan sınavı yazmaz (CONTRIBUTING); bu dosya Can'ın. Okuduğu dosyalar ve sütunlar
docs/data/tablo-bicimi.md sözleşmesinde.

Çalıştırma: python3 src/sinav.py faz1 data/synthetic
           python3 src/sinav.py faz2 data/synthetic [--aralik 11-20] [--ispanya <csv>]   (tahmin.csv: src/sablon.py;
               --ispanya: src/edp_test.py --cikti çıktısı, kalibrasyonun gerçek veri ölçüsü;
               --ispanya-tepe: aynı biçimde İspanya tepe satırları, yük haritasının gerçek veri ölçüsü)
           python3 src/sinav.py faz3 data/synthetic [--aralik 11-20]   (kac_ev.csv: src/kac_ev.py)
Her madde için GEÇTİ / KALDI ve rakam yazar; hepsi geçerse çıkış kodu 0.
"""
import csv
import json
import math
import statistics as st
import sys
from collections import Counter
from pathlib import Path

TIPLER = ['sehir_konutu', 'koy', 'carsi', 'otel', 'sanayi', 'sulama', 'yurt']
V_SINIR = 259.0                # planlama sınırı (en az bir trafo bunu aşmalı: yöntemin görecek şeyi var)
V_ALT = 207.0                  # EN 50160 alt sınırı (230 V −%10) (karar masası 13:55)
V_ALT_PAY, V_EN_DUSUK = 0.01, 200.0   # ADR-0016 m. 3: 207 V altı trafo ≤ %1 ve en düşük ≥ 200 V (uzun köy hattı gerçekçi)
TIP_SEHIR_MIN = 3              # her şehirde her tipten; bütün şehirlerde 3 x şehir sayısı (20 şehirde 60)
ROADMAP_SEHIR = 20             # ROADMAP eşikleri bu şehir sayısı için yazıldı
SURE_MAX_SN = 60.0             # şehirlerin üretildiği makinede (karar masası 31 Ekim)


def _csv(yol):
    with open(yol, encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


def sehirleri_oku(kok):
    """kok altındaki sehir-NNN klasörleri. (sayılan, atlanan) listeleri döner.
    Atlanan: profil_kaynagi = yer_tutucu ya da eksik dosya; (klasör adı, neden)."""
    sayilan, atlanan = [], []
    for k in sorted(Path(kok).glob('sehir-*')):
        if not k.is_dir():
            continue
        eksik = [d for d in ('trafolar.csv', 'cevap_anahtari.csv', 'ayar.json') if not (k / d).exists()]
        if eksik:
            atlanan.append((k.name, 'eksik dosya: ' + ', '.join(eksik)))
            continue
        with open(k / 'ayar.json', encoding='utf-8') as fh:
            ayar = json.load(fh)
        if ayar.get('profil_kaynagi') == 'yer_tutucu':
            atlanan.append((k.name, 'profil_kaynagi = yer_tutucu'))
            continue
        if ayar.get('veri_turu') == 'gercek':
            atlanan.append((k.name, 'veri_turu = gercek (farazi şehir sınavına girmez)'))
            continue
        sayilan.append(dict(ad=k.name, no=int(ayar.get('sehir', k.name[6:])), klasor=k, ayar=ayar,
                            trafolar=_csv(k / 'trafolar.csv'),
                            cevap=_csv(k / 'cevap_anahtari.csv')))
    return sayilan, atlanan


UYARI = 'UYARI'                 # "raporla" maddeleri: hedef aşıldı, ama ROADMAP'e göre geçmeyi bozmaz


def _fark(model, saf):
    """Model hatasının saf tahmine göre farkı: '%31 düşük' ya da '%218 yüksek'."""
    f = 1 - model / saf
    return f'%{100 * abs(f):.1f} ' + ('düşük' if f >= 0 else 'yüksek')


def _madde(sonuc, gecti, ad, ayrinti):
    sonuc.append((gecti, ad, ayrinti))


def faz1(sehirler):
    """ROADMAP Faz 1 geçme sınavı. (maddeler, bilgi satırları) döner."""
    m, bilgi = [], []

    # 1. Her şehirde 7 tipin her biri en az 3 trafo.
    eksikler = []
    toplam = Counter()
    for s in sehirler:
        say = Counter(r['tip'] for r in s['cevap'])
        toplam.update(say)
        az = {t: say.get(t, 0) for t in TIPLER if say.get(t, 0) < TIP_SEHIR_MIN}
        if az:
            eksikler.append(f"{s['ad']} {az}")
    _madde(m, not eksikler, f'her şehirde her tipten ≥ {TIP_SEHIR_MIN} trafo',
           f'{len(sehirler) - len(eksikler)}/{len(sehirler)} şehir' + (f"; eksik: {'; '.join(eksikler[:5])}" if eksikler else ''))

    # 2. Bütün şehirlerde her tipten en az 3 x şehir sayısı trafo.
    esik = TIP_SEHIR_MIN * len(sehirler)
    en_az = min(TIPLER, key=lambda t: toplam.get(t, 0))
    _madde(m, all(toplam.get(t, 0) >= esik for t in TIPLER),
           f'bütün şehirlerde her tipten ≥ {esik} trafo ({TIP_SEHIR_MIN} × {len(sehirler)} şehir)',
           f'en az {en_az} {toplam.get(en_az, 0)}; ' + ', '.join(f'{t} {toplam.get(t, 0)}' for t in TIPLER))
    if len(sehirler) < ROADMAP_SEHIR:
        bilgi.append(f'UYARI: ROADMAP eşiği {ROADMAP_SEHIR} şehir için; burada {len(sehirler)} şehir var')
    bilinmeyen = set(toplam) - set(TIPLER)
    if bilinmeyen:
        bilgi.append(f'UYARI: sözleşmede olmayan tip adı: {sorted(bilinmeyen)}')

    # 3. En az bir trafo bugün 259 V üstü (toplamda; düşük yaygınlıklı şehirde hiç aşan olmayabilir).
    asan = {s['ad']: sum(float(r['v_max_bugun_v']) > V_SINIR for r in s['cevap']) for s in sehirler}
    sifir = [a for a, n in asan.items() if n == 0]
    _madde(m, sum(asan.values()) >= 1, f'en az bir trafoda v_max_bugun_v > {V_SINIR:g} V',
           f'toplam {sum(asan.values())}/{sum(len(s["cevap"]) for s in sehirler)} trafo')
    bilgi.append(f'259 V üstü trafo olan şehir: {len(sehirler) - len(sifir)}/{len(sehirler)}'
                 + (f"; hiç aşmayan: {', '.join(sifir[:5])}" if sifir else ''))

    # 4. Gerilim alt sınırı (ADR-0016 m. 3): V_ALT (207 V) altı trafo payı ≤ %1 ve en düşük ≥ 200 V.
    v_min = [(float(r['v_min_bugun_v']), s['ad'], r['trafo_no']) for s in sehirler for r in s['cevap']]
    en_dusuk = min(v_min)
    alti = [x for x in v_min if x[0] < V_ALT]
    _madde(m, len(alti) / len(v_min) <= V_ALT_PAY and en_dusuk[0] >= V_EN_DUSUK,
           f'v_min_bugun_v < {V_ALT:g} V olan trafo ≤ %{100 * V_ALT_PAY:g} ve en düşük ≥ {V_EN_DUSUK:g} V',
           f'en düşük {en_dusuk[0]:.1f} V ({en_dusuk[1]} {en_dusuk[2]}); {V_ALT:g} V altında {_oran(len(alti), len(v_min))}'
           + (': ' + ', '.join(f'{a} {b} {v:.1f} V' for v, a, b in sorted(alti)[:5]) if alti else ''))

    # 5. Üretim süresi.
    sureler = [(s['ayar'].get('sure_sn'), s['ad']) for s in sehirler]
    yok = [a for v, a in sureler if v is None]
    var = [(float(v), a) for v, a in sureler if v is not None]
    kaynak = Counter(f"profil {s['ayar'].get('profil_kaynagi', '?')}, ışınım {s['ayar'].get('isinim_kaynagi', '?')}"
                     for s in sehirler)
    ayrinti = []
    if var:
        en_uzun = max(var)
        ayrinti.append(f'en uzun {en_uzun[0]:.1f} sn ({en_uzun[1]}), ortanca {st.median(v for v, _ in var):.1f} sn')
    if yok:
        ayrinti.append(f"ayar.json'da sure_sn yok: {len(yok)} şehir")
    ayrinti.append('; '.join(f'{k} ({n} şehir)' for k, n in kaynak.items()))
    _madde(m, not yok and max(var)[0] <= SURE_MAX_SN, f'üretim süresi ≤ {SURE_MAX_SN:g} sn', '; '.join(ayrinti))

    # Bilgi (eşiksiz).
    bilgi.append('tip başına ogle_min_kw ortancası (kW): ' + ', '.join(
        f"{t} {st.median(float(r['ogle_min_kw']) for s in sehirler for r in s['cevap'] if r['tip'] == t):.2f}"
        for t in TIPLER if toplam.get(t)))
    # Aday = 0 trafoda kaç ev sütunları bilgi taşımaz (sözleşme §3): ayrı sayılır, gerisi aday > 0 üzerinden.
    hepsi = [r for s in sehirler for r in s['cevap']]
    adaysiz = [r for r in hepsi if int(r['kac_ev_aday']) == 0]
    adayli = [r for r in hepsi if int(r['kac_ev_aday']) > 0]
    bilgi.append(f'aday = 0 trafo: {len(adaysiz)}/{len(hepsi)}'
                 + (' (' + ', '.join(f'{t} {n}' for t, n in Counter(r['tip'] for r in adaysiz).most_common()) + ')'
                    if adaysiz else ''))
    if adayli:
        kac = [int(r['kac_ev_gercek']) for r in adayli]
        q = st.quantiles(kac, n=4) if len(kac) > 1 else [kac[0]] * 3
        bilgi.append(f'kac_ev_gercek (aday > 0): en az {min(kac)}, çeyrekler {q[0]:g} / {q[1]:g} / {q[2]:g}, '
                     f'en çok {max(kac)}; sıfır olan {sum(k == 0 for k in kac)}/{len(kac)}')
        sinir = Counter(r['kac_ev_sinir'] for r in adayli)
        bilgi.append('kac_ev_sinir (aday > 0): ' + ', '.join(f'{k} {sinir.get(k, 0)}' for k in ('gerilim', 'isil', 'yok')))
        tavan = sum(int(r['kac_ev_tavan']) for r in adayli)
        bilgi.append(f'kac_ev_tavan = 1 oranı (aday > 0): {tavan / len(adayli):.3f} ({tavan}/{len(adayli)})')

    # ADR-0008: konut trafolarında abone başına öğlen yükünün trafodan trafoya değişimi (hedef CV 0,3–0,4).
    cv_sehir, havuz = [], []
    for s in sehirler:
        abone = {r['trafo_no']: _abone(r) for r in s['trafolar']}
        x = [float(r['ogle_min_kw']) / abone[r['trafo_no']] for r in s['cevap']
             if r['tip'] == 'sehir_konutu' and abone.get(r['trafo_no'])]
        havuz += x
        if len(x) > 1:
            cv_sehir.append(_cv(x))
    if cv_sehir:
        bilgi.append(f'şehir konutu trafolarında abone başına öğlen yükü CV (ADR-0008, hedef 0,3–0,4): '
                     f'şehir içi ortanca {st.median(cv_sehir):.2f} (şehirler {min(cv_sehir):.2f}–{max(cv_sehir):.2f}), '
                     f'havuz {_cv(havuz):.2f}; abone başına ortanca {1000 * st.median(havuz):.0f} W')
    return m, bilgi


ABONE = ['abone_konut', 'abone_ticari1', 'abone_ticari2', 'abone_turizm', 'abone_sanayi1', 'abone_sanayi2',
         'abone_su_motoru']
# Abone başına yıllık MWh: Kıb-Tek 2023 tarife sınıfı tüketimi ÷ abone [Kaynaklı: Kıb-Tek 2023 istatistik,
# data/raw/kibtek-istatistik/; sablon.py ile aynı kaynak, sınav kendi kopyasını tutar]. Yalnız saf tahmin bilgisi.
MWH_ABONE = {'abone_konut': 648494 / 175577, 'abone_ticari1': 210978 / 20950, 'abone_ticari2': 169496 / 494,
             'abone_turizm': 215147 / 171, 'abone_sanayi1': 22391 / 1227, 'abone_sanayi2': 95996 / 352,
             'abone_su_motoru': 51256 / 3250}
GERCEK_MIN_KW = 1.0             # gerçek öğlen yükü bunun altındaysa göreli hata anlamsız: atla, say
ARKETIP_MIN = 0.75
HATA_ORTANCA_MAX, HATA_P90_MAX = 0.15, 0.30
KAPSAMA = (0.70, 0.90)
CAPRAZ_MAX = 1.5
DUSUK_GUVEN_MAX = 0.25
SAF_FARK = 0.25                 # ADR-0008: model, saf tahminden ortanca ve P90'da en az %25 düşük
# Kalibrasyon (Faz 7, karar masası 21:32; ADR-0013): nominal bant ↔ ampirik kapsama ve PIT düzlüğü.
NOMINAL = (0.50, 0.80, 0.90, 0.95)
KAPSAMA_95_MIN = 0.90
KAPSAMA_95_N_MIN = 150             # karar masası 22:13: n < 150 trafoda %95 ölçütü bilgi (29 trafoda SH ±5 puan)
PIT_KOVA, PIT_SAPMA_MAX = 10, 0.05


def pit_tolerans(n):
    """Karar masası 21:51 (tüzük madde 2): max(0,05; 2·√(0,09 ÷ n)), n = trafo sayısı; 29 trafoda 0,11."""
    return max(PIT_SAPMA_MAX, 2 * math.sqrt(0.09 / n))


# Resmi ölçü: faturalı girdi (ADR-0007), 10 ölçülü (PR #10 ana tablosu), tabakalı seçim (ürünün seçimi). Rastgele ile
# havuzlanmaz: iki yolun hatası ters yönde, havuzda birbirini götürüyor (PIT 0,046 ↔ ayrı ayrı 0,068 / 0,108).
ISPANYA_GIRDI, ISPANYA_N, ISPANYA_YOL = 'c', '10', 'tabakali'
_Z80 = st.NormalDist().inv_cdf(0.90)
# Yük haritası (Faz 11, ADR-0014; karar masası 23:02 m. 4, 23:12): yıl tepesi (net) tahmini. Geçici eşik [Yorum].
TEPE_HATA_ORTANCA_MAX, TEPE_HATA_P90_MAX = 0.15, 0.35
TEPE_SAAT_TOLERANS_DK = 60
V_AKSAM_MIN = V_ALT             # yük tarafının gerilim sorusu: akşam (tepe) en düşük ev gerilimi ≥ 207 V (karar masası 23:12)


def _abone(r):
    return sum(int(r.get(a) or 0) for a in ABONE)


def _cv(x):
    return st.pstdev(x) / st.mean(x) if len(x) > 1 and st.mean(x) else float('nan')


def _p90(x):
    return st.quantiles(x, n=10, method='inclusive')[-1] if len(x) > 1 else x[0]


def _yuzde(x):
    return f'%{100 * x:.1f}'


def _hatalar(tahmin, gercek):
    """Ölçülmeyen trafolarda göreli hata. (hata listesi, atlanan sayısı)."""
    h, atla = [], 0
    for r in tahmin:
        if int(r['olculdu']):
            continue
        g = gercek[r['trafo_no']]
        if g < GERCEK_MIN_KW:
            atla += 1
            continue
        h.append(abs(float(r['ogle_min_kw']) - g) / g)
    return h, atla


def kalibrasyon(uclar):
    """[(P10, P90, gerçek)] -> nominal bantların ampirik kapsaması ve PIT kovaları.

    Bant log uzayında normal sayılır [Yorum]: orta = P10 ile P90'ın log ortası, σ = log genişlik ÷ (2 × 1,2816).
    %50 / 90 / 95 bantlar ve PIT (gerçeğin tahmin dağılımındaki yüzdeliği) bundan türetilir; %80 bant P10–P90'ın
    kendisidir. sablon.py bandı log uzayında simetrik (orta tam ortada); edp_test.py bandı değil, o yüzden orta
    tahmin değil bandın kendi ortası alınır.
    """
    nd = st.NormalDist()
    kap, kova, n, atla = dict.fromkeys(NOMINAL, 0), [0] * PIT_KOVA, 0, 0
    for lo, hi, g in uclar:
        if not (0 < lo < hi) or g <= 0:
            atla += 1
            continue
        z = (math.log(g) - (math.log(lo) + math.log(hi)) / 2) / ((math.log(hi) - math.log(lo)) / (2 * _Z80))
        for q in NOMINAL:
            kap[q] += abs(z) <= nd.inv_cdf(0.5 + q / 2)
        kova[min(int(nd.cdf(z) * PIT_KOVA), PIT_KOVA - 1)] += 1
        n += 1
    pay = [k / n for k in kova]
    return dict(n=n, atla=atla, kapsama={q: kap[q] / n for q in NOMINAL}, pit=pay,
                sapma=max(abs(p - 1 / PIT_KOVA) for p in pay),
                yon='fazla emin' if pay[0] + pay[-1] > 2 / PIT_KOVA else 'fazla geniş',
                alt=sum(pay[:PIT_KOVA // 2]))


def _kal_metin(k):
    return ('nominal ' + ' / '.join(f'%{100 * q:g}' for q in NOMINAL) + ' → ampirik '
            + ' / '.join(_yuzde(k['kapsama'][q]) for q in NOMINAL)
            + f"; PIT en büyük sapma {k['sapma']:.3f} (uçlarda {_yuzde(k['pit'][0] + k['pit'][-1])} → {k['yon']}; "
            + f"gerçek tahmin ortasının altında {_yuzde(k['alt'])}), kovalar "
            + ' '.join(f'{100 * p:.0f}' for p in k['pit'])
            + f"; n = {k['n']}" + (f", atlanan {k['atla']}" if k['atla'] else ''))


def _dakika_fark(a, b):
    """İki "HH:MM" arasındaki fark, dakika, gün çevresinde (23:30 ↔ 00:15 = 45)."""
    da, db = (int(x[:2]) * 60 + int(x[3:5]) for x in (a, b))
    d = abs(da - db) % 1440
    return min(d, 1440 - d)


def _donem(a):
    """"HH:MM" → tepe dönemi; sınırlar `tepe.py` donem() ile aynı (sözleşme §8 `tepe_donemi`)."""
    s = int(a[:2])
    return 'gece' if s >= 20 or s < 4 else 'sabah' if s < 10 else 'ogle' if s < 14 else 'ogleden_sonra'


def faz2_oku(s):
    """Faz 2 dosyalarını şehir sözlüğüne ekler; eksikse eksik dosya adını döner."""
    k = s['klasor']
    if not (k / 'tahmin.csv').exists() or not (k / 'arketipler.csv').exists():
        return 'tahmin.csv / arketipler.csv yok'
    s['tahmin'] = _csv(k / 'tahmin.csv')
    s['arketip'] = {}
    for r in _csv(k / 'arketipler.csv'):
        if r['gun_turu'] == 'isgunu':
            s['arketip'].setdefault(int(r['arketip']), [0.0] * 288)[int(r['adim'])] = float(r['oran'])
    s['deney'] = {p.stem: _csv(p) for p in sorted((k / 'deney').glob('tahmin_*.csv'))}
    # Sözleşme 1.4 (öneri, volkan.md 23:12 sonrası): yük haritası tahmini ayrı dosyada; yoksa tepe bölümü "ölçülmedi".
    s['tepe'] = _csv(k / 'tepe.csv') if (k / 'tepe.csv').exists() else None
    ozet = k / 'sablon_ozet.json'
    if ozet.exists():
        with open(ozet, encoding='utf-8') as fh:
            s['fatura_kullanildi'] = bool(json.load(fh).get('fatura_kullanildi'))
    else:
        s['fatura_kullanildi'] = False   # 1.2 öncesi model: fatura yok
    # Gerçek küme için iş günü ortalama tüketim eğrisi (yalnız ölçülmeyen trafolar).
    olcusuz = {r['trafo_no'] for r in s['tahmin'] if not int(r['olculdu'])}
    top = {t: [0.0] * 288 for t in olcusuz}
    gun = {t: set() for t in olcusuz}
    with open(k / 'yuk_5dk.csv', encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            t = r['trafo_no']
            if t in top and r['gun_turu'] == 'isgunu':
                top[t][int(r['adim'])] += float(r['tuketim_kw'])
                gun[t].add(r['gun'])
    s['egri'] = {t: [v / len(gun[t]) for v in e] for t, e in top.items() if gun[t]}
    return None


def _gercek_kume(egri, arketip):
    tepe = max(egri) or 1.0
    e = [v / tepe for v in egri]
    return min(arketip, key=lambda a: sum((x - y) ** 2 for x, y in zip(e, arketip[a])))


def _saf(s, olcu):
    """ADR-0008 saf tahmini: ölçülülerde Σ öğlen ÷ Σ olcu × trafonun olcu'su. olcu: trafo_no -> sayı."""
    olculu = [r['trafo_no'] for r in s['tahmin'] if int(r['olculdu'])]
    pay = sum(s['gercek'][t] for t in olculu)
    payda = sum(olcu[t] for t in olculu)
    if not payda:
        return None
    k = pay / payda
    return [dict(trafo_no=t, olculdu='0', ogle_min_kw=k * olcu[t]) for t in s['gercek']
            if t not in olculu]


def _ozet(sehir_deger):
    """{şehir: değer} -> (ortanca, (en kötü değer, şehir)) ; en kötü = en büyük."""
    v = list(sehir_deger.values())
    kotu = max(sehir_deger.items(), key=lambda x: x[1])
    return st.median(v), (kotu[1], kotu[0])


def faz2(sehirler, ispanya=None, ispanya_tepe=None):
    """ROADMAP Faz 2 geçme sınavı + ADR-0008 saf tahmin + Faz 7 kalibrasyon. Yalnız ölçülmeyen trafolar (`olculdu` = 0).

    ispanya: src/edp_test.py --cikti CSV'si (sütunlar girdi, n, yol, y, alt, ust); yoksa kalibrasyon maddesi UYARI.
    """
    m, bilgi = [], []
    for s in sehirler:
        s['gercek'] = {r['trafo_no']: float(r['ogle_min_kw']) for r in s['cevap']}
        s['tip'] = {r['trafo_no']: r['tip'] for r in s['cevap']}

    # 1. Doğru arketip oranı.
    dogru = {}
    for s in sehirler:
        n = [int(r['arketip']) == _gercek_kume(s['egri'][r['trafo_no']], s['arketip'])
             for r in s['tahmin'] if not int(r['olculdu']) and r['trafo_no'] in s['egri']]
        if n:
            dogru[s['ad']] = sum(n) / len(n)
    orta = st.median(dogru.values())
    kotu = min(dogru.items(), key=lambda x: x[1])
    _madde(m, orta >= ARKETIP_MIN, f'doğru arketip oranı ortanca ≥ %{100 * ARKETIP_MIN:g}',
           f'ortanca {_yuzde(orta)}, en kötü {_yuzde(kotu[1])} ({kotu[0]})')

    # 2. Öğlen en düşük yük hatası: şehir başına ortanca ve P90, sonra şehirlerin ortancası ve en kötüsü.
    h_ort, h_p90, atla_top, havuz = {}, {}, 0, []
    for s in sehirler:
        h, atla = _hatalar(s['tahmin'], s['gercek'])
        atla_top += atla
        s['hata'] = h
        havuz += h
        h_ort[s['ad']], h_p90[s['ad']] = st.median(h), _p90(h)
    o, k = _ozet(h_ort)
    p, kp = _ozet(h_p90)
    _madde(m, o <= HATA_ORTANCA_MAX and p <= HATA_P90_MAX,
           f'öğlen en düşük yük hatası ortanca ≤ %{100 * HATA_ORTANCA_MAX:g}, P90 ≤ %{100 * HATA_P90_MAX:g}',
           f'ortanca {_yuzde(o)} (en kötü {_yuzde(k[0])} {k[1]}), P90 {_yuzde(p)} (en kötü {_yuzde(kp[0])} {kp[1]}); '
           f'n = {len(havuz)}, gerçek < {GERCEK_MIN_KW:g} kW atlanan {atla_top}')

    # 3. %80 bant kapsama.
    kap, alt, ust = {}, 0, 0
    for s in sehirler:
        ic = []
        for r in s['tahmin']:
            if int(r['olculdu']):
                continue
            g = s['gercek'][r['trafo_no']]
            lo, hi = float(r['ogle_min_kw_p10']), float(r['ogle_min_kw_p90'])
            ic.append(lo <= g <= hi)
            alt += g < lo
            ust += g > hi
        kap[s['ad']] = sum(ic) / len(ic)
    orta = st.median(kap.values())
    dusuk = min(kap.items(), key=lambda x: x[1])
    yuksek = max(kap.items(), key=lambda x: x[1])
    # Karar masası 21:51: farazi kapsama bilgi satırı; kapı gerçek veride (İspanya, madde 3b).
    bilgi.append(f'%80 bant kapsama, farazi (eski madde, hedef %{100 * KAPSAMA[0]:g}–{100 * KAPSAMA[1]:g}; '
                 f'kapı İspanya): ortanca {_yuzde(orta)}; şehirler {_yuzde(dusuk[1])} ({dusuk[0]}) – '
                 f'{_yuzde(yuksek[1])} ({yuksek[0]}); dışarıda kalan: P10 altı {alt}, P90 üstü {ust} → '
                 + ('geçer' if KAPSAMA[0] <= orta <= KAPSAMA[1] else 'geçmez'))

    # 3b. Kalibrasyon (Faz 7, karar masası 21:32): resmi ölçü gerçek veride (İspanya); farazi şehir bilgi.
    uclar = [(float(r['ogle_min_kw_p10']), float(r['ogle_min_kw_p90']), s['gercek'][r['trafo_no']])
             for s in sehirler for r in s['tahmin'] if not int(r['olculdu'])]
    kf = kalibrasyon(uclar)
    bilgi.append('kalibrasyon, farazi (gösterim, havuz): ' + _kal_metin(kf)
                 + f"; %95 bant ≥ %{100 * KAPSAMA_95_MIN:g} → {'geçer' if kf['kapsama'][0.95] >= KAPSAMA_95_MIN else 'geçmez'}"
                 + f"; PIT ≤ {pit_tolerans(kf['n']):.3f} (n = {kf['n']} trafo) → "
                 + ('geçer' if kf['sapma'] <= pit_tolerans(kf['n']) else 'geçmez'))
    if ispanya:
        satir = _csv(Path(ispanya))

        def _sec(girdi, n=ISPANYA_N, yol=None):
            return [r for r in satir if r['girdi'] == girdi and r['n'] == n and (yol is None or r['yol'] == yol)]

        def _kal(rows):
            k = kalibrasyon([(float(r['alt']), float(r['ust']), float(r['y'])) for r in rows])
            k['trafo'] = len({r['ct'] for r in rows})       # PIT toleransının n'i: tekrar değil, trafo
            k['tol'] = pit_tolerans(k['trafo'])
            return k

        ki = _kal(_sec(ISPANYA_GIRDI, yol=ISPANYA_YOL))
        etiket = f'gerçek veri — İspanya (girdi {ISPANYA_GIRDI}, {ISPANYA_N} ölçülü, {ISPANYA_YOL}, bütün tekrarlar)'
        k95_olcut = ki['trafo'] >= KAPSAMA_95_N_MIN
        k95_tutar = ki['kapsama'][0.95] >= KAPSAMA_95_MIN
        _madde(m, KAPSAMA[0] <= ki['kapsama'][0.80] <= KAPSAMA[1] and (k95_tutar or not k95_olcut),
               f'kalibrasyon, {etiket}: %80 bant %{100 * KAPSAMA[0]:g}–{100 * KAPSAMA[1]:g}'
               + (f' ve %95 bant ≥ %{100 * KAPSAMA_95_MIN:g}' if k95_olcut else ''),
               _kal_metin(ki))
        if not k95_olcut:
            bilgi.append(f"%95 bant, İspanya (bilgi: {ki['trafo']} trafo < {KAPSAMA_95_N_MIN}, karar masası 22:13): "
                         f"{_yuzde(ki['kapsama'][0.95])} → ölçüt (≥ %{100 * KAPSAMA_95_MIN:g}) "
                         + ('tutar' if k95_tutar else 'tutmaz'))
        _madde(m, True if ki['sapma'] <= ki['tol'] else UYARI,
               f'PIT düzlüğü, {etiket}: {PIT_KOVA} kovada en büyük sapma ≤ max(0,05; 2·√(0,09 ÷ n))',
               f"{ki['sapma']:.3f}, tolerans {ki['tol']:.3f} (n = {ki['trafo']} trafo; karar masası 21:51)"
               + ('' if ki['sapma'] <= ki['tol'] else f"; {ki['yon']}"))
        for g in ('a', 'b', 'c'):
            for n in ('5', '10', '15'):
                for yol in ('rastgele', 'tabakali'):
                    u = _sec(g, n, yol)
                    if u:
                        k = _kal(u)
                        bilgi.append(f'kalibrasyon, İspanya girdi {g}, {n} ölçülü, {yol}: %80 {_yuzde(k["kapsama"][0.80])}, '
                                     f'%95 {_yuzde(k["kapsama"][0.95])}, PIT sapma {k["sapma"]:.3f} ({k["yon"]}; tolerans {k["tol"]:.3f}), n = {k["n"]} ({k["trafo"]} trafo)')
    else:
        _madde(m, UYARI, 'kalibrasyon, gerçek veri — İspanya', 'ölçülmedi: --ispanya <src/edp_test.py --cikti çıktısı> verilmedi')

    # 3c. Yük haritası (Faz 11): yıl tepesi, net, kW. Farazi bilgi; gerçek veri (İspanya Mayıs tepesi) madde.
    #     Ölçü kW ile: pf varsayımı (kVA) hatayı kirletmesin. Saat isabeti ±60 dk (bilgi).
    #     Yıl tepesi boş şehir (yaz / kış penceresi üretilemedi, `ayar.json` yil_tepe_kaynagi boş) sayılmaz.
    tepe_sat, tepe_bos = [], []
    for s in sehirler:
        if not s.get('tepe') or 'tepe_yil_kw' not in s['cevap'][0]:
            continue
        if any(r['tepe_yil_kw'] == '' for r in s['cevap']):
            tepe_bos.append(s['ad'])
            continue
        cevap = {r['trafo_no']: r for r in s['cevap']}
        for r in s['tepe']:
            if not int(r['olculdu']):
                g = cevap[r['trafo_no']]
                tepe_sat.append(dict(t=float(r['tepe_kw']), lo=float(r['tepe_kw_p10']), hi=float(r['tepe_kw_p90']),
                                     g=float(g['tepe_yil_kw']), ts=r.get('tepe_saati'), gs=g.get('tepe_saati'),
                                     ts2=r.get('tepe_saati_2'), dn=r.get('tepe_donemi'),
                                     vt=float(r['v_min_tepe_v']) if r.get('v_min_tepe_v') else None,
                                     # "yeterli" kararı karamsar uçtan (BUILD 1, 01:10; ADR-0018 m. 6); yoksa ortanca
                                     vk=float(r.get('v_min_tepe_v_p10') or r.get('v_min_tepe_v') or 0) or None,
                                     pa=float(r['p_aksam_207']) if r.get('p_aksam_207') else None,
                                     vg=float(g['v_min_tepe_v']) if g.get('v_min_tepe_v') else None))
    if tepe_bos:
        bilgi.append(f'yük haritası: yıl tepesi boş, sayılmadı: {", ".join(tepe_bos)} (yaz / kış penceresi üretilemedi)')
    if tepe_sat:
        h = [abs(x['t'] - x['g']) / x['g'] for x in tepe_sat if x['g'] >= GERCEK_MIN_KW]
        kt = kalibrasyon([(x['lo'], x['hi'], x['g']) for x in tepe_sat])
        saat = [_dakika_fark(x['ts'], x['gs']) for x in tepe_sat if x['ts'] and x['gs']]
        # Sözleşme §8 (PR #32, BUILD 1 01:36 önerisi): ikinci aday saat ve dönem; sütun yoksa satır yazılmaz (bilgi).
        iki = [min(_dakika_fark(x['ts'], x['gs']), _dakika_fark(x['ts2'], x['gs']) if x['ts2'] else 1440)
               for x in tepe_sat if x['ts'] and x['gs'] and x['ts2'] is not None]
        dnm = [x['dn'] == _donem(x['gs']) for x in tepe_sat if x['dn'] and x['gs']]
        bilgi.append(f'yük haritası (tepe, net), farazi (gösterim): hata ortanca {_yuzde(st.median(h))}, P90 {_yuzde(_p90(h))} '
                     f'(geçici eşik ≤ %{100 * TEPE_HATA_ORTANCA_MAX:g} / %{100 * TEPE_HATA_P90_MAX:g}); '
                     f"%80 bant kapsama {_yuzde(kt['kapsama'][0.80])}, %95 {_yuzde(kt['kapsama'][0.95])}"
                     + (f'; tepe saati ±{TEPE_SAAT_TOLERANS_DK} dk isabet '
                        f'{_oran(sum(d <= TEPE_SAAT_TOLERANS_DK for d in saat), len(saat))}' if saat else '')
                     + (f', iki adaydan biri {_oran(sum(d <= TEPE_SAAT_TOLERANS_DK for d in iki), len(iki))}' if iki else '')
                     + (f'; dönem aynı {_oran(sum(dnm), len(dnm))}' if dnm else '')
                     + f'; n = {len(tepe_sat)}')
        # Akşam gerilimi: "yeterli" (≥ 207 V) dediğimiz trafoda gerçekte altına iniyorsa yük tarafının yanlış yeşili.
        v = [x for x in tepe_sat if x['vt'] is not None and x['vg'] is not None]
        if v:
            dusuk = [x for x in v if x['vg'] < V_AKSAM_MIN]
            yeter = [x for x in v if x['vk'] >= V_AKSAM_MIN]
            pa = [x['pa'] for x in dusuk if x['pa'] is not None]
            bilgi.append(f'akşam en düşük gerilim ≥ {V_AKSAM_MIN:g} V (farazi, gösterim; "yeterli" = P10 ≥ {V_AKSAM_MIN:g} V): '
                         f'gerçekte altında {_oran(len(dusuk), len(v))}, yakalanan {sum(x["vk"] < V_AKSAM_MIN for x in dusuk)}/{len(dusuk)}; '
                         f'"yeterli" dediğimiz {len(yeter)} trafodan gerçekte altında {sum(x["vg"] < V_AKSAM_MIN for x in yeter)}; '
                         f'hata ortanca (orta) {st.median(abs(x["vt"] - x["vg"]) for x in v):.1f} V'
                         + (f'; gerçekte altında olanlarda p_aksam_207 ortanca {_yuzde(st.median(pa))}' if pa else ''))
    else:
        bilgi.append('yük haritası (tepe), farazi: ölçülmedi (tepe.csv ya da cevap anahtarında tepe_yil_kw yok; sözleşme 1.4)')
    if ispanya_tepe and not Path(ispanya_tepe).exists():
        print(f'UYARI: --ispanya-tepe {ispanya_tepe} bulunamadı; yük haritası gerçek veri maddesi ölçülmedi.')
        ispanya_tepe = None
    if ispanya_tepe:
        rows = [r for r in _csv(Path(ispanya_tepe))
                if r.get('girdi', ISPANYA_GIRDI) == ISPANYA_GIRDI and r.get('n', ISPANYA_N) == ISPANYA_N
                and r.get('yol', ISPANYA_YOL) == ISPANYA_YOL and r['alt'] and r['ust']]
        h = [abs(float(r['tah']) - float(r['y'])) / float(r['y']) for r in rows if float(r['y']) > 0]
        kt = kalibrasyon([(float(r['alt']), float(r['ust']), float(r['y'])) for r in rows])
        ho, hp, k80 = st.median(h), _p90(h), kt['kapsama'][0.80]
        _madde(m, ho <= TEPE_HATA_ORTANCA_MAX and hp <= TEPE_HATA_P90_MAX and KAPSAMA[0] <= k80 <= KAPSAMA[1],
               f'yük haritası, gerçek veri — İspanya Mayıs tepesi ({ISPANYA_N} ölçülü, {ISPANYA_YOL}): hata ortanca '
               f'≤ %{100 * TEPE_HATA_ORTANCA_MAX:g}, P90 ≤ %{100 * TEPE_HATA_P90_MAX:g}, %80 bant %{100 * KAPSAMA[0]:g}–{100 * KAPSAMA[1]:g}',
               f'hata {_yuzde(ho)} / {_yuzde(hp)}; ' + _kal_metin(kt) + f" ({len({r['ct'] for r in rows})} trafo)")
    else:
        _madde(m, UYARI, 'yük haritası, gerçek veri — İspanya Mayıs tepesi',
               'ölçülmedi: --ispanya-tepe <tepe satırları> verilmedi (B-Y2 çıktısı bekleniyor)')

    # 4. Şehirler arası: capraz hata ortancası ÷ şehir içi hata ortancası.
    oran = {}
    for s in sehirler:
        h = []
        for ad, d in s['deney'].items():
            if ad.startswith('tahmin_capraz_'):
                h += _hatalar(d, s['gercek'])[0]
        if h and h_ort[s['ad']]:
            oran[s['ad']] = st.median(h) / h_ort[s['ad']]
    if oran:
        o, k = _ozet(oran)
        _madde(m, o <= CAPRAZ_MAX, f'şehirler arası hata ÷ şehir içi hata ≤ {CAPRAZ_MAX:g}',
               f'ortanca {o:.2f}, en kötü {k[0]:.2f} ({k[1]}); {CAPRAZ_MAX:g} üstü {sum(v > CAPRAZ_MAX for v in oran.values())} şehir')
    else:
        _madde(m, False, f'şehirler arası hata ÷ şehir içi hata ≤ {CAPRAZ_MAX:g}', 'deney/tahmin_capraz_*.csv yok')

    # 5. Düşük güven oranı (aşarsa UYARI, KALDI değil; kart).
    dg = {s['ad']: sum(r['guven'] == 'dusuk' for r in s['tahmin'] if not int(r['olculdu']))
          / sum(not int(r['olculdu']) for r in s['tahmin']) for s in sehirler}
    o, k = _ozet(dg)
    ayr = f'ortanca {_yuzde(o)}, en kötü {_yuzde(k[0])} ({k[1]})'
    _madde(m, True if o <= DUSUK_GUVEN_MAX else UYARI, f'düşük güven oranı raporlandı (hedef ≤ %{100 * DUSUK_GUVEN_MAX:g})',
           ayr + ('' if o <= DUSUK_GUVEN_MAX else '; hedefin üstünde, sebep BUILD günlüğünde'))

    # 6. Saf tahmin (ADR-0008, karar masası 17:26): model hangi bilgiyle koştuysa o saf tahminle karşılaştırılır.
    #    faturasız: Σ öğlen ÷ Σ tarife enerjisi × tarife enerjisi; faturalı: Σ öğlen ÷ Σ fatura × fatura.
    def _tarife(s):
        return {r['trafo_no']: sum(int(r.get(a) or 0) * MWH_ABONE[a] for a in ABONE) for r in s['trafolar']}

    def _fatura(s):
        f = {r['trafo_no']: float(r['yillik_tuketim_mwh']) for r in s['trafolar'] if r.get('yillik_tuketim_mwh')}
        return f if len(f) == len(s['trafolar']) else None

    def _saf_ozet(olcu_fn):
        d = {}
        for s in sehirler:
            olcu = olcu_fn(s)
            saf = _saf(s, olcu) if olcu else None
            if saf:
                h = _hatalar(saf, s['gercek'])[0]
                d[s['ad']] = (st.median(h), _p90(h))
        if not d:
            return None
        return st.median(v[0] for v in d.values()), st.median(v[1] for v in d.values()), len(d)

    mo, mp = st.median(h_ort.values()), st.median(h_p90.values())
    faturali = sum(bool(s['fatura_kullanildi']) for s in sehirler) > len(sehirler) / 2
    saflar = {'fatura': ('Σ öğlen ÷ Σ yillik_tuketim_mwh × fatura', _saf_ozet(_fatura)),
              'tarife': ('Σ öğlen ÷ Σ tarife enerjisi × tarife enerjisi', _saf_ozet(_tarife))}
    for ad, (tanim, oz) in saflar.items():
        kendi = (ad == 'fatura') == faturali
        if oz is None:
            bilgi.append(f'saf tahmin ({ad}): veri yok (sözleşme 1.2 öncesi şehir)')
            continue
        so, sp, n = oz
        gecer = mo <= (1 - SAF_FARK) * so and mp <= (1 - SAF_FARK) * sp
        ayr = (f'model {_yuzde(mo)} / {_yuzde(mp)}, saf {_yuzde(so)} / {_yuzde(sp)} '
               f'(model {_fark(mo, so)} / {_fark(mp, sp)}; {n} şehir)')
        if kendi:   # ADR-0016 m. 1: geçme şartı değil, bilgi (öğlen yükünü fatura söyler)
            bilgi.append(f'saf tahmin ({ad}: {tanim}), modelin koştuğu (ADR-0016: bilgi): {ayr}; '
                         f"model {'faturalı' if faturali else 'faturasız'} koşmuş (sablon_ozet.json) → "
                         f'eski ölçüt (≥ %{100 * SAF_FARK:g} düşük) ' + ('geçer' if gecer else 'geçmez'))
        else:
            bilgi.append(f'saf tahmin ({ad}: {tanim}), modelin koşmadığı bilgi: {ayr} → ölçüt '
                         + ('geçer' if gecer else 'geçmez'))

    # 7. Ölçülü / ölçülmeyen tip dağılımı (bilgi; ROADMAP: karşılaştırılmış, günlükte).
    olc, olcz = Counter(), Counter()
    fark = {}
    for s in sehirler:
        a = Counter(s['tip'][r['trafo_no']] for r in s['tahmin'] if int(r['olculdu']))
        b = Counter(s['tip'][r['trafo_no']] for r in s['tahmin'] if not int(r['olculdu']))
        olc.update(a)
        olcz.update(b)
        na, nb = sum(a.values()), sum(b.values())
        fark[s['ad']] = sum(abs(a[t] / na - b[t] / nb) for t in TIPLER) / 2   # toplam varyasyon uzaklığı
    o, k = _ozet(fark)
    _madde(m, True, 'ölçülü / ölçülmeyen tip dağılımı karşılaştırıldı',
           'ölçülü ' + ', '.join(f'{t} {olc[t]}' for t in TIPLER) + ' | ölçülmeyen '
           + ', '.join(f'{t} {olcz[t]}' for t in TIPLER)
           + f'; şehir başına fark (TV uzaklığı) ortanca {o:.2f}, en çok {k[0]:.2f} ({k[1]})')

    bilgi.append(f'havuz (bütün ölçülmeyenler): ortanca {_yuzde(st.median(havuz))}, P90 {_yuzde(_p90(havuz))}, n = {len(havuz)}')
    guv = {}
    for s in sehirler:
        hata = iter(s['hata'])
        for r in s['tahmin']:
            if not int(r['olculdu']) and s['gercek'][r['trafo_no']] >= GERCEK_MIN_KW:
                guv.setdefault(r['guven'], []).append(next(hata))
    bilgi.append('güvene göre hata ortancası (yüksek < orta < düşük olmalı): ' + ', '.join(
        f'{g} {_yuzde(st.median(guv[g]))} (n {len(guv[g])})' for g in ('yuksek', 'orta', 'dusuk') if g in guv))
    tip_h = {}
    for s in sehirler:
        hata = iter(s['hata'])
        for r in s['tahmin']:
            if not int(r['olculdu']) and s['gercek'][r['trafo_no']] >= GERCEK_MIN_KW:
                tip_h.setdefault(s['tip'][r['trafo_no']], []).append(next(hata))
    bilgi.append('tip başına hata ortancası: ' + ', '.join(
        f'{t} {_yuzde(st.median(tip_h[t]))} (n {len(tip_h[t])})' for t in TIPLER if t in tip_h))
    return m, bilgi


YANLIS_YESIL_MAX, YANLIS_YESIL_SEHIR_MAX = 0.05, 0.10
CANLI_BUTCE = 0.02              # ADR-0010: canlıya geçiş bütçesi (bilgi)
KIRMIZI_ASAN_MIN = 0.50         # ADR-0016 m. 2: kırmızı kovasında gerçekte aşan pay ≥ %50 (eski "yanlış kırmızı ≤ %20" kalktı)
BAYRAK_P = 0.7                  # ADR-0017: "büyük olasılıkla dolu" bayrağı p_bugun_asar ≥ 0,7 (kırmızı dolgu değil)
P_KOVA = (0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0001)   # p_bugun_asar kovaları; kırmızı 0,5 üstü (ADR-0011)
KAC_EV_HATA_MAX = 2.0
SARI_HEDEF = 0.30


def faz3_oku(s):
    k = s['klasor'] / 'kac_ev.csv'
    if not k.exists():
        return 'kac_ev.csv yok'
    s['kac_ev'] = {r['trafo_no']: r for r in _csv(k)}
    return None


def _oran(pay, payda):
    return f'{_yuzde(pay / payda)} ({pay}/{payda})' if payda else '— (0/0)'


def faz3(sehirler):
    """ROADMAP Faz 3 geçme sınavı. Küme: kac_ev_aday > 0 (aday = 0 ayrı sayılır); dolu = kac_ev_gercek = 0."""
    m, bilgi = [], []
    satir, adaysiz = [], 0
    for s in sehirler:
        for r in s['cevap']:
            if int(r['kac_ev_aday']) == 0:
                adaysiz += 1
                continue
            k = s['kac_ev'][r['trafo_no']]
            kar, iyi = int(k['kac_ev_karamsar']), int(k['kac_ev_iyimser'])
            # Ortası: sözleşme 1.3 `kac_ev_orta` (olasılıklı hesabın çekiliş ortancası) varsa o, yoksa (karamsar + iyimser) ÷ 2.
            orta = float(k['kac_ev_orta']) if k.get('kac_ev_orta') not in (None, '') else (kar + iyi) / 2
            satir.append(dict(sehir=s['ad'], tip=r['tip'], gercek=int(r['kac_ev_gercek']),
                              tavan=int(r['kac_ev_tavan']), renk=k['renk'], kar=kar, iyi=iyi, orta=orta,
                              k40=int(k['kural40_ev']), sinir=k['sinir_karamsar'],
                              p=float(k['p_bugun_asar']) if k.get('p_bugun_asar') not in (None, '') else None,
                              pv_uc=k.get('pv_uc')))
    dolu = [x for x in satir if x['gercek'] == 0]
    orta_ad = 'ortası (kac_ev_orta)' if any(k.get('kac_ev_orta') not in (None, '')
                                            for s in sehirler for k in s['kac_ev'].values()) else 'ortası'

    def yanlis_yesil(yer_var):
        """(yanlış, yer var denen, şehir başına {şehir: (yanlış, yer var)})"""
        ys = [x for x in satir if yer_var(x)]
        sehir = {}
        for x in ys:
            a, b = sehir.get(x['sehir'], (0, 0))
            sehir[x['sehir']] = (a + (x['gercek'] == 0), b + 1)
        return sum(x['gercek'] == 0 for x in ys), len(ys), sehir

    # 1. Yanlış yeşil (model): yeşil denip gerçekte dolu.
    yy, ny, sehir = yanlis_yesil(lambda x: x['renk'] == 'yesil')
    kotu = max(sehir.items(), key=lambda x: x[1][0] / x[1][1]) if sehir else None
    kotu_oran = kotu[1][0] / kotu[1][1] if kotu else 0.0
    _madde(m, ny > 0 and yy / ny <= YANLIS_YESIL_MAX and kotu_oran <= YANLIS_YESIL_SEHIR_MAX,
           f'yanlış yeşil ≤ %{100 * YANLIS_YESIL_MAX:g}, en kötü şehirde ≤ %{100 * YANLIS_YESIL_SEHIR_MAX:g}',
           f'{_oran(yy, ny)}; en kötü şehir ' + (f'{_oran(*kotu[1])} {kotu[0]}' if kotu else '— (yeşil yok)')
           + f'; yeşili olan şehir {len(sehir)}/{len(sehirler)}; dolu trafoya yeşil {_oran(yy, len(dolu))}')
    bilgi.append(f'canlı bütçe (ADR-0010) yanlış yeşil < %{100 * CANLI_BUTCE:g}: '
                 + ('tutuyor' if ny and yy / ny < CANLI_BUTCE else 'tutmuyor' if ny else 'yeşil yok')
                 + f' ({_oran(yy, ny)}; farazi şehir, gösterim)')

    # 2. %40 kuralı aynı ölçüyle: "yer var" = kural40_ev ≥ 1.
    ky, nk, sehir40 = yanlis_yesil(lambda x: x['k40'] >= 1)
    kotu40 = max(sehir40.items(), key=lambda x: x[1][0] / x[1][1]) if sehir40 else None
    _madde(m, True, '%40 kuralının yanlış yeşili aynı trafolarda, yan yana',
           f'%40 kuralı {_oran(ky, nk)} (en kötü şehir ' + (f'{_oran(*kotu40[1])} {kotu40[0]}' if kotu40 else '—')
           + f'), model {_oran(yy, ny)}; dolu trafoya "yer var": %40 kuralı {_oran(ky, len(dolu))}, model {yy}/{len(dolu)}')

    # 3. Kırmızı kovası (ADR-0016 m. 2, karar masası 22:21): kırmızı = bugün aşma olasılığı ≥ 0,5 (ADR-0011); olasılık
    #    kalibreyse kırmızıların bir kısmı aşmaz. Gerçekte aşan = dolu (kac_ev_gercek = 0; eski yanlış kırmızının tersi).
    #    Eşik 0,5 − 2·√(0,25 ÷ n), n = kırmızı trafo sayısı (PIT ve %95 maddeleriyle aynı mantık).
    kir = [x for x in satir if x['renk'] == 'kirmizi']
    asan = sum(x['gercek'] == 0 for x in kir)
    if kir:
        esik = KIRMIZI_ASAN_MIN - 2 * math.sqrt(0.25 / len(kir))
        ps = [x['p'] for x in kir if x['p'] is not None]
        yon = ''
        if ps:
            ort = st.mean(ps)
            yon = (f'; ortalama olasılık {_yuzde(ort)} → '
                   + ('olasılık karamsar (aşan, söylenenden az)' if asan / len(kir) < ort else 'olasılık iyimser'))
        bilgi.append('kırmızı kovası (ADR-0017: bilgi; madde bayrak isabeti): gerçekte dolu '
                     f'{_oran(asan, len(kir))}, eski eşik {esik:.2f} → ' + ('geçer' if asan / len(kir) >= esik else 'geçmez')
                     + f'; yanlış kırmızı {_oran(len(kir) - asan, len(kir))}; kırmızı payı {_oran(len(kir), len(satir))}' + yon)

    # 3b. Bayrak isabeti (ADR-0017 m. 3): p_bugun_asar ≥ 0,7 ("büyük olasılıkla dolu") olanların gerçekte dolu payı
    #     ≥ ortalama olasılık − 2·√(p̄(1 − p̄) ÷ n) (kırmızı kovasının bayrak sürümü). `pv_uc` varsa ondan, yoksa eşikten.
    def _uc(x):
        if x.get('pv_uc'):
            return x['pv_uc']
        return 'dolu_bayrak' if x['p'] is not None and x['p'] >= BAYRAK_P else ('yesil' if x['renk'] == 'yesil' else 'bos')
    bay = [x for x in satir if _uc(x) == 'dolu_bayrak']
    if bay and all(x['p'] is not None for x in bay):
        pbar = st.mean(x['p'] for x in bay)
        esik_b = pbar - 2 * math.sqrt(pbar * (1 - pbar) / len(bay))
        db = sum(x['gercek'] == 0 for x in bay)
        _madde(m, db / len(bay) >= esik_b, 'bayrak isabeti (p ≥ 0,7): gerçekte dolu pay ≥ p̄ − 2·√(p̄(1 − p̄) ÷ n)',
               f'{_oran(db, len(bay))}, ortalama olasılık {_yuzde(pbar)}, eşik {esik_b:.2f} (n = {len(bay)} bayrak)')
    else:
        _madde(m, UYARI, 'bayrak isabeti (p ≥ 0,7)', 'bayraklı trafo yok' if not bay else 'p_bugun_asar yok (sözleşme 1.3 öncesi)')
    renksiz = [x for x in satir if _uc(x) == 'bos']
    bilgi.append(f'güvenli uçlar (ADR-0017): yeşil {sum(_uc(x) == "yesil" for x in satir)}, bayrak {len(bay)}, renksiz '
                 f'{_oran(len(renksiz), len(satir))}; bayrağın yakaladığı dolu {_oran(sum(x["gercek"] == 0 for x in bay), len(dolu))}, '
                 f'renksizde kalan dolu {_oran(sum(x["gercek"] == 0 for x in renksiz), len(dolu))}')
    if any(x['p'] is not None for x in satir):
        kova = []
        for a, b in zip(P_KOVA, P_KOVA[1:]):
            ic = [x for x in satir if x['p'] is not None and a <= x['p'] < b]
            if ic:
                kova.append(f'{a:g}–{min(b, 1):g}: n {len(ic)}, ortalama olasılık {_yuzde(st.mean(x["p"] for x in ic))}, '
                            f'gerçekte dolu {_yuzde(sum(x["gercek"] == 0 for x in ic) / len(ic))}')
        bilgi.append('bugün aşma olasılığı kovaları (p_bugun_asar ↔ gerçekte dolu; kalibreyse ikisi yakın): '
                     + ' | '.join(kova))

    # 4. Kaç ev hatası (tavan = 1 olanlar ayrı: gerçek alttan kesik).
    kes = [x for x in satir if not x['tavan']]
    hata = {ad: st.median(abs(f(x) - x['gercek']) for x in kes) for ad, f in
            (('karamsar', lambda x: x['kar']), ('iyimser', lambda x: x['iyi']), (orta_ad, lambda x: x['orta']))}
    gecen = [ad for ad, h in hata.items() if h <= KAC_EV_HATA_MAX]
    _madde(m, bool(gecen), f'kaç ev hatası ortanca ≤ {KAC_EV_HATA_MAX:g} ev (en az bir sayı)',
           ', '.join(f'{ad} {h:g}' for ad, h in hata.items()) + f' ev; eşiği geçen: {", ".join(gecen) or "yok"}; '
           f'n = {len(kes)}, tavan = 1 ayrı {len(satir) - len(kes)}')
    bilgi.append('kaç ev hatası ortancası, tavan = 1 dahil (gerçek alttan kesik): ' + ', '.join(
        f'{ad} {st.median(abs(f(x) - x["gercek"]) for x in satir):g}' for ad, f in
        (('karamsar', lambda x: x['kar']), ('iyimser', lambda x: x['iyi']), (orta_ad, lambda x: x['orta'])))
        + f' ev (n = {len(satir)})')

    # 5. Sarı oranı (hedef; aşarsa UYARI).
    sari = sum(x['renk'] == 'sari' for x in satir)
    asti = sari / len(satir) > SARI_HEDEF
    _madde(m, UYARI if asti else True, f'sarı oranı raporlandı (hedef ≤ %{100 * SARI_HEDEF:g})',
           _oran(sari, len(satir)) + ('; hedefin üstünde, sebep BUILD günlüğünde' if asti else ''))

    # Bilgi.
    bilgi.append(f'küme: kac_ev_aday > 0 {len(satir)} trafo ({len(dolu)} dolu); aday = 0 ayrı {adaysiz}')
    renk = Counter(x['renk'] for x in satir)
    bilgi.append('renk: ' + ', '.join(f'{r} {renk.get(r, 0)}' for r in ('yesil', 'sari', 'kirmizi')))
    for t in TIPLER:
        xs = [x for x in satir if x['tip'] == t]
        if xs:
            c = Counter(x['renk'] for x in xs)
            bilgi.append(f'  {t} (n {len(xs)}, dolu {sum(x["gercek"] == 0 for x in xs)}): '
                         + ', '.join(f'{r} {c.get(r, 0)}' for r in ('yesil', 'sari', 'kirmizi'))
                         + f'; ortanca gerçek / karamsar / iyimser {st.median(x["gercek"] for x in xs):g} / '
                         f'{st.median(x["kar"] for x in xs):g} / {st.median(x["iyi"] for x in xs):g} ev')
    ic = sum(x['kar'] <= x['gercek'] <= x['iyi'] for x in kes)
    bilgi.append(f'aralık kapsaması (gerçek kac_ev_gercek [karamsar, iyimser] içinde; tavan = 0): {_oran(ic, len(kes))}; '
                 f'gerçek < karamsar {sum(x["gercek"] < x["kar"] for x in kes)}, gerçek > iyimser {sum(x["gercek"] > x["iyi"] for x in kes)}')
    # Kaç ev bandı kalibrasyonu (karar masası 19:13): karamsar/iyimser %80 bandın uçlarıdır, taban değil; Faz 2 bandıyla aynı ölçü.
    alti = [x for x in kes if x['gercek'] < x['kar']]
    ustu = [x for x in kes if x['gercek'] > x['iyi']]
    alti_tip = Counter(x['tip'] for x in alti)
    bilgi.append(f'kaç ev bandı (tavan = 0; beklenen ~%10 / ~%10): P10 altı {_oran(len(alti), len(kes))}, '
                 f'P90 üstü {_oran(len(ustu), len(kes))}; P10 altı tipe göre: '
                 + (', '.join(f'{t} {n} (fark ortanca {st.median(x["kar"] - x["gercek"] for x in alti if x["tip"] == t):g} ev)'
                              for t, n in alti_tip.most_common()) or '—')
                 + f'; P10 altı yeşil {sum(x["renk"] == "yesil" for x in alti)}, bunlardan dolu {sum(x["renk"] == "yesil" and x["gercek"] == 0 for x in alti)}')
    sn = Counter(x['sinir'] for x in satir)
    bilgi.append('sinir_karamsar: ' + ', '.join(f'{k} {n}' for k, n in sn.most_common()))
    return m, bilgi


def main():
    sys.stdout.reconfigure(encoding='utf-8')  # Windows'ta boruya yazarken cp1254 '≥' karakterinde çöküyordu
    if len(sys.argv) < 3 or sys.argv[1] not in ('faz1', 'faz2', 'faz3'):
        sys.exit('Kullanım: python3 src/sinav.py faz1|faz2|faz3 <şehir kökü, ör. data/synthetic> [--aralik 11-20] '
                 '[--ispanya <edp_test.py --cikti CSV>] [--ispanya-tepe <tepe satırları CSV>]')
    faz = sys.argv[1]
    sehirler, atlanan = sehirleri_oku(sys.argv[2])
    if '--aralik' in sys.argv:
        a, b = map(int, sys.argv[sys.argv.index('--aralik') + 1].split('-'))
        sehirler = [s for s in sehirler if a <= s['no'] <= b]
    if faz != 'faz1':
        oku = faz2_oku if faz == 'faz2' else faz3_oku
        kalan = []
        for s in sehirler:
            eksik = oku(s)
            if eksik:
                atlanan.append((s['ad'], eksik))
            else:
                kalan.append(s)
        sehirler = kalan
    for ad, neden in atlanan:
        print(f'UYARI: {ad} sayılmadı ({neden})')
    if not sehirler:
        sys.exit(f'{sys.argv[2]} altında sınava girecek şehir yok.')
    trafo = sum(len(s['cevap']) for s in sehirler)
    print(f"Faz {faz[-1]} geçme sınavı: {len(sehirler)} şehir ({sehirler[0]['ad']}…{sehirler[-1]['ad']}), {trafo} trafo"
          + ('' if faz == 'faz1' else ' — gösterim, farazi şehirler') + '\n')
    if faz == 'faz2':
        ispanya = sys.argv[sys.argv.index('--ispanya') + 1] if '--ispanya' in sys.argv else None
        ispanya_tepe = sys.argv[sys.argv.index('--ispanya-tepe') + 1] if '--ispanya-tepe' in sys.argv else None
        maddeler, bilgi = faz2(sehirler, ispanya, ispanya_tepe)
    else:
        maddeler, bilgi = {'faz1': faz1, 'faz3': faz3}[faz](sehirler)
    for gecti, ad, ayrinti in maddeler:
        print(f"[{UYARI if gecti == UYARI else 'GEÇTİ' if gecti else 'KALDI'}] {ad}: {ayrinti}")
    print('\nBilgi:')
    for satir in bilgi:
        print('  ' + satir)
    sys.exit(0 if all(g for g, _, _ in maddeler) else 1)


if __name__ == '__main__':
    main()
