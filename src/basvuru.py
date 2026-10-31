#!/usr/bin/env python3
"""Başvuru anı motoru (deneme; ADR-0012, ADR-0015; karar masası 23:18; Muhittin 3–4): bu ev, bu trafoda, şimdi
panel takabilir mi.

Haritanın olasılıklı hesabıyla aynı fizik ve aynı kapı (`kac_ev_olasilik.py`, ADR-0011; ADR-0015 m. 3); farkı:
  - **durumlu:** o ana kadar onaylanmış ama kurulmamış başvurular (taahhüt) de ağa konur (ADR-0015 m. 1, ADR-0010 m. 2);
  - **kayda koşullu:** Kıb-Tek kaydı varsa (`sahte_kayit.kayit_oku`) bilinmeyenin çekilişi kayda koşullanır, kaydın
    kendi hata payıyla (kayıt öncülü daraltır, sıfırlamaz); kayıt yoksa bugünkü aralık:
      bara      inverter kaydı varsa sakin an gerilimi ± inverter payı (`inv_bara_hata` verilirse ölçülmüş geri çözüm
                hatası dağılımından: `inverter_geri_cozum.py`); yoksa kademe kaydı varsa kayıtlı kademenin
                ±3,125 V penceresi (OG payı [Yorum]) olasılık p_dogru ile, değilse 244–252 V; kayıt yoksa 244–252 V
      hatlar    hat boyu kaydı × e^U(±hat payı) (bugün: en uzun hat × e^U(±0,47), diğerleri rastgele)
      yer, faz  kaydı olan panelli ev, taahhüt ve başvuran kayıtlı hattına ve yerine (direk sırası ÷ hattaki ev);
                faz kaydı p_dogru ile, değilse diğer iki fazdan biri; kaydı olmayanlar bugünkü gibi rastgele
      empedans  inverterin olduğu hatta kaydın eşdeğer boyu × e^U(±inverter payı), model-sapma çarpanı yok; diğer
                hatlarda model-sapma s (Faz 7, İngiltere)
  - **karar:** P(başvuru + taahhütler + bugünkü paneller sığar) ≥ 0,98 ve güven yüksek → `evet`;
    P(aşar) ≥ 0,5 → `hayir` (güçlendir / önce ölç değil, bugünkü durum bile taşımıyor); arası `once_olc`.
Model kayıt hatalarını **iki kat** varsayar (`VARSAYILAN_HATA`; karar masası 23:47, tüzük madde 2): Kıb-Tek kayıtlarının
doğruluğu sahada bir örnekle ölçülene kadar; ölçülünce varsayım ölçülen orana iner. Testte veri daha iyi ya da daha kötü
olabilir.

Saf Python; `kac_ev_olasilik` ile aynı benzetim (`trafo_bos_kapasite.solve`).
"""
import math
import random
import sys

_argv, sys.argv = sys.argv, sys.argv[:1]
import kac_ev_olasilik as ko  # noqa: E402
import kac_ev as ke  # noqa: E402
import sahte_kayit as sk  # noqa: E402
sys.argv = _argv

CEKILIS = ko.CEKILIS
KADEME_PENCERE_V = sk.KADEME_ADIM_V / 2           # ±3,125 V: kademe bilinince kalan OG payı [Yorum]
VARSAYILAN_HATA = 'iki_kat'                       # kayıt kalitesi ölçülene kadar en kötü kayıt hatası (23:47)


def _faz_cek(kayitli, hp, rng, uc_p, fw):
    """Kayıtlı faz (A/B/C/3 ya da boş) -> faz no. Kayıt hata payıyla; yoksa bugünkü çekiliş."""
    if kayitli:
        p = sk.FAZ_NO[kayitli]
        if p == 3 or rng.random() >= hp['faz_yanlis']:          # dolu kaydın yanlış olma payı
            return p
        return rng.choice([q for q in (0, 1, 2) if q != p])
    return 3 if rng.random() < uc_p else rng.choices([0, 1, 2], weights=fw)[0]


def ag_kur_kayitli(tr, kayit, konumlu, hp, rng):
    """Bir çekiliş. kayit: sahte_kayit biçimi (None = kayıtsız). konumlu: [(rol, kayıt ya da None, kW)], rol
    'basvuran' / 'taahhut'; kaydı None olan rastgele panelsiz bir konuta konur. Dönüş: ag, evler, {rol sırası: ev id}."""
    if kayit is None:                                   # bugünkü hesap + başvurular rastgele konutlarda
        ag, evler = ko.ag_kur(tr, rng)
        bos = [h for h in evler if h['sinif'] == 'abone_konut' and h['pv'] == 0] or [h for h in evler if h['pv'] == 0]
        sec = rng.sample(bos, min(len(bos), len(konumlu)))
        return ag, evler, {i: h['id'] for i, h in enumerate(sec)}, set()
    kva = tr['kva']
    zb = 240.0 ** 2 / (kva * 1000 / 3)
    rt = 0.04 * zb / math.sqrt(5)
    boylar = [b * math.exp(rng.uniform(math.log(1 - hp['hat']), math.log(1 + hp['hat']))) for b in kayit['hat_boy_m']]
    n_hat = len(boylar)
    inv_hat = {}
    for v in kayit['inverter'].values():                 # aynı hatta birden çok inverter: ilki yeter
        inv_hat.setdefault(v['hat'], v)
    for j, v in inv_hat.items():
        e = hp['inv_empedans']
        boylar[j] = v['esdeger_boy_m'] * math.exp(rng.uniform(math.log(1 - e), math.log(1 + e)))
    # konumu kayıtlı evler: panelli (kaydı olan), taahhüt ve başvuran (formu olan)
    yerli = [('panelli', hid, p, p['kw']) for hid, p in kayit['panelli'].items()]
    yerli += [(i, None, k, kw) for i, (rol, k, kw) in enumerate(konumlu) if k is not None]
    n_konut_yerli = len(yerli)
    aboneler = [c for c in ko.ABONE for _ in range(int(tr[c]))]
    for _ in range(n_konut_yerli):                       # yerli evler konut sayısından düşülür
        if 'abone_konut' in aboneler:
            aboneler.remove('abone_konut')
    rng.shuffle(aboneler)
    hatlar = [[] for _ in range(n_hat)]
    for c in aboneler:
        hatlar[rng.randrange(n_hat)].append(c)
    if rng.random() < ko.BUYUK_BASTA_P:
        for hat in hatlar:
            hat.sort(key=lambda c: c not in ko.BUYUK)
    d = rng.uniform(0, ko.FAZ_SAPMA.get(tr['bolge'], 0.3))
    fw = [1 + rng.uniform(-d, d) for _ in range(3)]
    uc = {c: rng.uniform(*ko.UC_FAZ[c]) for c in ko.UC_FAZ}
    # yerli evleri kayıtlı yerlerine sok (yer: 0–1, hattaki sıra ÷ ev sayısı)
    hat_ev = [[dict(sinif=c, yerli=None) for c in hat] for hat in hatlar]
    for rol, hid, k, kw in sorted(yerli, key=lambda x: x[2]['yer']):
        j = min(max(0, k['hat']), n_hat - 1)
        i = max(0, min(len(hat_ev[j]), round(k['yer'] * (len(hat_ev[j]) + 1)) - 1))
        hat_ev[j].insert(i, dict(sinif='abone_konut', yerli=(rol, k, kw)))
    zc, znc = ko.tb.CABLES[tr['kablo']]
    if kayit.get('kademe_v') is not None and not inv_hat:
        p_dogru = (1 - hp['kademe_yanlis'] - hp['kademe_eksik']) / (1 - hp['kademe_eksik'] or 1)
        if rng.random() < p_dogru:
            lo = max(ko.V0[0], kayit['kademe_v'] - KADEME_PENCERE_V)
            hi = min(ko.V0[1], kayit['kademe_v'] + KADEME_PENCERE_V)
            v0 = rng.uniform(lo, hi) if lo < hi else rng.uniform(*ko.V0)
        else:
            v0 = rng.uniform(*ko.V0)
    elif inv_hat:
        b = statistics_mean([v['bara_v'] for v in kayit['inverter'].values()])
        if hp.get('inv_bara_hata'):                     # ölçülmüş geri çözüm hatası (tahmin − gerçek), 1–10'dan
            v0 = b - rng.choice(hp['inv_bara_hata'])
        else:
            v0 = b + rng.uniform(-hp['inv_bara_v'], hp['inv_bara_v'])
    else:
        v0 = rng.uniform(*ko.V0)
    ag = dict(v0=v0, zt=complex(rt, 2 * rt), kva=kva, feeders=[])
    evler, roller, sapmasiz = [], {}, set()
    for j, (boy, hat) in enumerate(zip(boylar, hat_ev)):
        if not hat:
            continue
        seg = boy / 1000 / len(hat)
        f = dict(zs=zc * seg, zn=znc * seg, houses=[], boy=boy)
        if j in inv_hat:
            f['sapmasiz'] = True
        for k, e in enumerate(hat):
            c = e['sinif']
            if e['yerli'] is None:
                ph = 3 if rng.random() < uc.get(c, 1.0) else rng.choices([0, 1, 2], weights=fw)[0]
                pv = 0.0
            else:
                rol, kk, kw = e['yerli']
                ph = _faz_cek(kk.get('faz', ''), hp, rng, uc.get('abone_konut', 0.0), fw)
                pv = kw if rol == 'panelli' else 0.0
            h = dict(id=len(evler), sinif=c, ph=ph, pv=pv, yer=(k + 1) / len(hat))
            if e['yerli'] is not None and e['yerli'][0] != 'panelli':
                roller[e['yerli'][0]] = h['id']
            f['houses'].append(h)
            evler.append(h)
        ag['feeders'].append(f)
    # kaydı olmayan panelliler (abone → trafo eşleşmesi kayıp): bugünkü gibi rastgele konutlarda
    kalan_n = int(tr['panel_sayisi']) - len(kayit['panelli'])
    kalan_kw = tr['panel_kw'] - sum(p['kw'] for p in kayit['panelli'].values())
    bos = [h for h in evler if h['sinif'] == 'abone_konut' and h['pv'] == 0 and h['id'] not in roller.values()]
    if kalan_n > 0 and kalan_kw > 0 and bos:
        for h in rng.sample(bos, min(kalan_n, len(bos))):
            h['pv'] = kalan_kw / kalan_n
    # formu olmayan başvuran / taahhüt: rastgele panelsiz konut
    bos = [h for h in evler if h['sinif'] == 'abone_konut' and h['pv'] == 0 and h['id'] not in roller.values()]
    for i, (rol, k, kw) in enumerate(konumlu):
        if k is None and bos:
            h = bos.pop(rng.randrange(len(bos)))
            roller[i] = h['id']
    sapmasiz = {id(f) for f in ag['feeders'] if f.get('sapmasiz')}
    return ag, evler, roller, sapmasiz


def statistics_mean(x):
    return sum(x) / len(x)


def karar(tr, t, kayit, basvuran, taahhut, rng, hp=None):
    """basvuran: başvuru formu kaydı (None = konumu bilinmiyor); taahhut: [form kaydı ya da None] (her biri 6,5 kW).
    Dönüş: (karar, P(sığar))."""
    hp = hp or sk.hata_payi(VARSAYILAN_HATA)
    p10, p90 = ke.sayi(t['ogle_min_kw_p10']), ke.sayi(t['ogle_min_kw_p90'])
    olculen = ke.sayi(t['ogle_min_kw_olculen'])
    konumlu = [('taahhut', k, ke.YENI_PANEL_KW) for k in taahhut] + [('basvuran', basvuran, ke.YENI_PANEL_KW)]
    srng = random.Random(f'sapma-{tr["sehir"]}-{tr["trafo_no"]}')
    sigar = 0
    for _ in range(CEKILIS):
        ag, evler, roller, sapmasiz = ag_kur_kayitli(tr, kayit, konumlu, hp, rng)
        sapma = math.exp(srng.gauss(ko.SAPMA_MU, ko.SAPMA_SIGMA)) if (ko.SAPMA_MU or ko.SAPMA_SIGMA) else 1.0
        for f in ag['feeders']:
            if id(f) not in sapmasiz:
                f['zs'], f['zn'] = f['zs'] * sapma, f['zn'] * sapma
        if not evler:
            sigar += 1
            continue
        if t['olculdu'] == '1' and not math.isnan(olculen):
            toplam = olculen
        else:
            mu = (math.log(max(p10, 0.01)) + math.log(max(p90, 0.01))) / 2
            sd = max(1e-6, (math.log(max(p90, 0.01)) - math.log(max(p10, 0.01))) / (2 * 1.2816))
            toplam = math.exp(rng.gauss(mu, sd))
        yuk = ko.yuk_dagit(evler, toplam, rng)
        m = 1 + rng.uniform(*ko.OG)
        ek = {roller[i]: kw for i, (_, _, kw) in enumerate(konumlu) if i in roller}
        _, vmax, s_tr = ko.durum(ag, evler, yuk, ek, m)
        sigar += not (vmax > ke.V_SINIR or s_tr > ag['kva'])
    p = sigar / CEKILIS
    if p >= ko.YESIL_P and t['guven'] == 'yuksek':
        return 'evet', p
    if 1 - p >= ko.KIRMIZI_P:
        return 'hayir', p
    return 'once_olc', p


def harita_rengi(tr, t, kayit, rng, hp=None):
    """Haritanın rengi kayıtlarla (ADR-0011 kuralı): bugün aşma olasılığı ve konumu bilinmeyen ilk iki başvuru."""
    hp = hp or sk.hata_payi(VARSAYILAN_HATA)
    p10, p90 = ke.sayi(t['ogle_min_kw_p10']), ke.sayi(t['ogle_min_kw_p90'])
    olculen = ke.sayi(t['ogle_min_kw_olculen'])
    srng = random.Random(f'sapma-{tr["sehir"]}-{tr["trafo_no"]}')
    bugun_n, iki_n = 0, 0
    for _ in range(CEKILIS):
        ag, evler, roller, sapmasiz = ag_kur_kayitli(tr, kayit, [('b1', None, 0), ('b2', None, 0)], hp, rng)
        sapma = math.exp(srng.gauss(ko.SAPMA_MU, ko.SAPMA_SIGMA)) if (ko.SAPMA_MU or ko.SAPMA_SIGMA) else 1.0
        for f in ag['feeders']:
            if id(f) not in sapmasiz:
                f['zs'], f['zn'] = f['zs'] * sapma, f['zn'] * sapma
        if not evler:
            iki_n += 1
            continue
        if t['olculdu'] == '1' and not math.isnan(olculen):
            toplam = olculen
        else:
            mu = (math.log(max(p10, 0.01)) + math.log(max(p90, 0.01))) / 2
            sd = max(1e-6, (math.log(max(p90, 0.01)) - math.log(max(p10, 0.01))) / (2 * 1.2816))
            toplam = math.exp(rng.gauss(mu, sd))
        yuk = ko.yuk_dagit(evler, toplam, rng)
        m = 1 + rng.uniform(*ko.OG)
        _, vmax, s_tr = ko.durum(ag, evler, yuk, {}, m)
        bugun = vmax > ke.V_SINIR or s_tr > ag['kva']
        bugun_n += bugun
        if not bugun and len(roller) == 2:
            ek = {roller[0]: ke.YENI_PANEL_KW, roller[1]: ke.YENI_PANEL_KW}
            _, v2, s2 = ko.durum(ag, evler, yuk, ek, m)
            iki_n += not (v2 > ke.V_SINIR or s2 > ag['kva'])
    p_bugun, p_iki = bugun_n / CEKILIS, iki_n / CEKILIS
    if p_bugun >= ko.KIRMIZI_P:
        return 'kirmizi', p_bugun, p_iki
    if p_iki >= ko.YESIL_P and t['guven'] == 'yuksek':
        return 'yesil', p_bugun, p_iki
    return 'sari', p_bugun, p_iki
