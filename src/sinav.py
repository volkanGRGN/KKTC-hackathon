#!/usr/bin/env python3
"""Geçme sınavı ölçüleri: üretilen şehirleri ROADMAP eşiklerine göre ölçer.

Modeli ya da üreteci yazan sınavı yazmaz (CONTRIBUTING); bu dosya Can'ın. Okuduğu dosyalar ve sütunlar
docs/data/tablo-bicimi.md sözleşmesinde.

Çalıştırma: python3 src/sinav.py faz1 data/synthetic
           python3 src/sinav.py faz2 data/synthetic [--aralik 11-20]   (tahmin.csv: src/sablon.py)
Her madde için GEÇTİ / KALDI ve rakam yazar; hepsi geçerse çıkış kodu 0.
"""
import csv
import json
import statistics as st
import sys
from collections import Counter
from pathlib import Path

TIPLER = ['sehir_konutu', 'koy', 'carsi', 'otel', 'sanayi', 'sulama', 'yurt']
V_SINIR = 259.0                # planlama sınırı (en az bir trafo bunu aşmalı: yöntemin görecek şeyi var)
V_ALT = 207.0                  # EN 50160 alt sınırı (230 V −%10); bunun altı = benzetim bozuk (karar masası 13:55)
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

    # 4. Hiçbir trafoda V_ALT (207 V) altı yok.
    v_min = [(float(r['v_min_bugun_v']), s['ad'], r['trafo_no']) for s in sehirler for r in s['cevap']]
    en_dusuk = min(v_min)
    alti = [x for x in v_min if x[0] < V_ALT]
    _madde(m, not alti, f'hiçbir trafoda v_min_bugun_v < {V_ALT:g} V',
           f'en düşük {en_dusuk[0]:.1f} V ({en_dusuk[1]} {en_dusuk[2]}); altında {len(alti)} trafo')

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


def faz2(sehirler):
    """ROADMAP Faz 2 geçme sınavı + ADR-0008 saf tahmin. Yalnız ölçülmeyen trafolar (`olculdu` = 0)."""
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
    _madde(m, KAPSAMA[0] <= orta <= KAPSAMA[1], f'%80 bant kapsama ortanca %{100 * KAPSAMA[0]:g}–{100 * KAPSAMA[1]:g}',
           f'ortanca {_yuzde(orta)}; şehirler {_yuzde(dusuk[1])} ({dusuk[0]}) – {_yuzde(yuksek[1])} ({yuksek[0]}); '
           f'dışarıda kalan: P10 altı {alt}, P90 üstü {ust}')

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
    _madde(m, True, f'düşük güven oranı raporlandı (hedef ≤ %{100 * DUSUK_GUVEN_MAX:g})',
           ayr + ('' if o <= DUSUK_GUVEN_MAX else '; UYARI: hedefin üstünde, sebep BUILD günlüğünde'))

    # 6. Saf tahmin (ADR-0008): Σ öğlen ÷ Σ abone × abone.
    s_ort, s_p90 = {}, {}
    for s in sehirler:
        abone = {r['trafo_no']: _abone(r) for r in s['trafolar']}
        saf = _saf(s, abone)
        if saf:
            h = _hatalar(saf, s['gercek'])[0]
            s_ort[s['ad']], s_p90[s['ad']] = st.median(h), _p90(h)
    mo, mp = st.median(h_ort.values()), st.median(h_p90.values())
    so, sp = st.median(s_ort.values()), st.median(s_p90.values())
    _madde(m, mo <= (1 - SAF_FARK) * so and mp <= (1 - SAF_FARK) * sp,
           f'model saf tahminden (Σ öğlen ÷ Σ abone × abone) ortanca ve P90\'da ≥ %{100 * SAF_FARK:g} düşük',
           f'model {_yuzde(mo)} / {_yuzde(mp)}, saf {_yuzde(so)} / {_yuzde(sp)} '
           f'(fark {_yuzde(1 - mo / so)} / {_yuzde(1 - mp / sp)})')

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

    # Bilgi (eşiksiz): saf tahminin iki başka tanımı (BUILD önerisi, volkan.md 17:03; karar gelene kadar madde
    # ADR-0008 tanımıyla). Aynı ≥ %25 ölçütü yanında yazılır.
    def _saf_bilgi(ad, olcu_fn):
        d = {}
        for s in sehirler:
            olcu = olcu_fn(s)
            saf = _saf(s, olcu) if olcu else None
            if saf:
                h = _hatalar(saf, s['gercek'])[0]
                d[s['ad']] = (st.median(h), _p90(h))
        if not d:
            return f'saf tahmin {ad}: veri yok (sözleşme 1.2 öncesi şehir)'
        fo, fp = st.median(v[0] for v in d.values()), st.median(v[1] for v in d.values())
        gecer = mo <= (1 - SAF_FARK) * fo and mp <= (1 - SAF_FARK) * fp
        return (f'saf tahmin {ad}: {_yuzde(fo)} / {_yuzde(fp)}; model bundan {_yuzde(1 - mo / fo)} / '
                f'{_yuzde(1 - mp / fp)} düşük → ≥ %{100 * SAF_FARK:g} ölçütü {"geçer" if gecer else "geçmez"} ({len(d)} şehir)')

    def _tarife(s):
        return {r['trafo_no']: sum(int(r.get(a) or 0) * MWH_ABONE[a] for a in ABONE) for r in s['trafolar']}

    def _fatura(s):
        f = {r['trafo_no']: float(r['yillik_tuketim_mwh']) for r in s['trafolar'] if r.get('yillik_tuketim_mwh')}
        return f if len(f) == len(s['trafolar']) else None

    bilgi.append(_saf_bilgi('tarife enerjisiyle (Σ öğlen ÷ Σ abone × Kıb-Tek sınıf ortalaması)', _tarife))
    bilgi.append(_saf_bilgi('faturayla (Σ öğlen ÷ Σ yillik_tuketim_mwh × fatura)', _fatura))
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


def main():
    sys.stdout.reconfigure(encoding='utf-8')  # Windows'ta boruya yazarken cp1254 '≥' karakterinde çöküyordu
    if len(sys.argv) < 3 or sys.argv[1] not in ('faz1', 'faz2'):
        sys.exit('Kullanım: python3 src/sinav.py faz1|faz2 <şehir kökü, ör. data/synthetic> [--aralik 11-20]')
    faz = sys.argv[1]
    sehirler, atlanan = sehirleri_oku(sys.argv[2])
    if '--aralik' in sys.argv:
        a, b = map(int, sys.argv[sys.argv.index('--aralik') + 1].split('-'))
        sehirler = [s for s in sehirler if a <= s['no'] <= b]
    if faz == 'faz2':
        kalan = []
        for s in sehirler:
            eksik = faz2_oku(s)
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
          + (' — gösterim, farazi şehirler' if faz == 'faz2' else '') + '\n')
    maddeler, bilgi = (faz1 if faz == 'faz1' else faz2)(sehirler)
    for gecti, ad, ayrinti in maddeler:
        print(f"[{'GEÇTİ' if gecti else 'KALDI'}] {ad}: {ayrinti}")
    print('\nBilgi:')
    for satir in bilgi:
        print('  ' + satir)
    sys.exit(0 if all(g for g, _, _ in maddeler) else 1)


if __name__ == '__main__':
    main()
