#!/usr/bin/env python3
"""Benzetim mahallesi: inverter kaydından trafo grubu bulma + boş panel kapasitesi.

Saf Python (numpy yok). Yapı:
1. Üç trafolu, topolojisi bilinen bir mahalle kurulur (tek fazlı evler, havai hat).
2. 14 bahar günü 5 dakikalık adımlarla dengesiz yük akışı hesaplanır.
3. "Veri" olarak yalnız panelli evlerin inverter kaydı alınır: faz gerilimi + üretim.
4. Bu veriden (a) evler gerilim benzerliğine göre trafolarına gruplanır,
   (b) bulut geçişlerindeki gerilim/üretim değişiminden kW başına volt çıkarılır,
   (c) her grupta sınıra kalan pay -> kaç kW / kaç 5 kW'lık başvuru daha sığar.
5. Tahmin, benzetimde bekleyen evlere tek tek 5 kW eklenerek bulunan gerçek değerle
   karşılaştırılır.
"""
import cmath
import json
import math
import random
import statistics
import sys

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 7)

STEPS_PER_DAY = 288          # 5 dakika
DAYS = 14
V_LIMIT = 259.0              # planlama sınırı: 240 V'un %8 üstü (inverter 264 V'ta kapanır)
MARGIN = 1.0                 # ölçüm payı, V
NEW_KW = 5.0                 # bekleyen başvuru: tek faz 5 kW
PV_DERATE = 0.82             # sıcaklık + inverter kaybı
A = cmath.exp(-2j * math.pi / 3)
PH = [1 + 0j, A, A * A]

CABLES = {  # ohm/km, işletme sıcaklığında; nötr 54,6 mm² taşıyıcı
    'ABC70': (complex(0.50, 0.09), complex(0.69, 0.09)),
    'ABC95': (complex(0.36, 0.085), complex(0.69, 0.09)),
}

# (uzunluk m, kablo, ev sayısı, yön derece) ; pv_p: panel olasılığı (hat başı, hat sonu)
TRAFO_SPECS = [
    dict(ad='T1 Kıyı', kva=250, v0=246.0, xy=(0, 0), pv_p=(0.15, 0.5), phase_w=(0.38, 0.33, 0.29),
         feeders=[(420, 'ABC70', 24, 10), (320, 'ABC70', 16, 200)]),
    dict(ad='T2 Merkez', kva=400, v0=246.0, xy=(700, 120), pv_p=(0.15, 0.25), phase_w=(0.36, 0.33, 0.31),
         feeders=[(260, 'ABC95', 17, 80), (240, 'ABC95', 16, 330), (280, 'ABC95', 18, 160)]),
    dict(ad='T3 Yukarı', kva=160, v0=247.0, xy=(320, 560), pv_p=(0.35, 0.45), phase_w=(0.34, 0.33, 0.33),
         feeders=[(300, 'ABC70', 20, 60), (180, 'ABC70', 10, 250)]),
]


def build():
    trafos, houses = [], []
    for ti, s in enumerate(TRAFO_SPECS):
        zb = 240.0 ** 2 / (s['kva'] * 1000 / 3)
        rt = 0.04 * zb / math.sqrt(5)        # uk %4, X/R = 2
        tr = dict(i=ti, ad=s['ad'], kva=s['kva'], v0=s['v0'], zt=complex(rt, 2 * rt), feeders=[], xy=s['xy'])
        for fi, (length, cable, n, ang) in enumerate(s['feeders']):
            zc, znc = CABLES[cable]
            seg = length / 1000 / n
            f = dict(zs=zc * seg, zn=znc * seg, houses=[])
            for k in range(n):
                pos = (k + 1) / n
                p_pv = s['pv_p'][0] + (s['pv_p'][1] - s['pv_p'][0]) * pos
                has_pv = random.random() < p_pv
                three = random.random() < 0.08
                ph = 3 if three else random.choices([0, 1, 2], weights=s['phase_w'])[0]
                pv_kw = 0.0
                if has_pv:
                    pv_kw = 8.0 if three else random.choice([5.0, 5.0, 5.0, 4.0, 3.0])
                bend = math.radians(ang + 25 * math.sin(pos * 3))
                d = length * pos
                h = dict(id=len(houses), t=ti, f=fi, k=k, ph=ph, pv=pv_kw,
                         scale=random.lognormvariate(0, 0.35),
                         xy=(s['xy'][0] + d * math.cos(bend), s['xy'][1] + d * math.sin(bend)))
                houses.append(h)
                f['houses'].append(h)
            tr['feeders'].append(f)
        trafos.append(tr)
    return trafos, houses


def irradiance():
    kinds = ['açık', 'açık', 'parçalı', 'açık', 'kapalı', 'açık', 'parçalı',
             'açık', 'açık', 'parçalı', 'açık', 'kapalı', 'parçalı', 'açık']
    g, cloud = [], 1.0
    for d in range(DAYS):
        kind = kinds[d % len(kinds)]
        for s in range(STEPS_PER_DAY):
            h = s * 5 / 60
            clear = math.sin(math.pi * (h - 6.6) / 12.5) ** 1.2 if 6.6 < h < 19.1 else 0.0
            if kind == 'açık':
                c = 1 - abs(random.gauss(0, 0.02))
            elif kind == 'kapalı':
                c = min(1, max(0.15, 0.4 + random.gauss(0, 0.08)))
            else:  # parçalı: hızlı bulut geçişleri
                cloud = 0.6 * cloud + 0.4 * random.choice([1.0, 1.0, 0.95, 0.35, 0.5])
                c = cloud
            g.append(clear * c)
    return g, kinds


def mv_factor(g):
    """Orta gerilim (ortak) gerilim çarpanı: adadaki güneşle yavaş yükselir, akşam düşer."""
    n = len(g)
    smooth = []
    w = 12
    for i in range(n):
        lo, hi = max(0, i - w), min(n, i + w + 1)
        smooth.append(sum(g[lo:hi]) / (hi - lo))
    m, ar = [], 0.0
    for i in range(n):
        h = (i % STEPS_PER_DAY) * 5 / 60
        eve = math.exp(-((h - 20) / 1.8) ** 2)
        ar = 0.97 * ar + random.gauss(0, 0.0006)
        m.append(1 + 0.008 * smooth[i] - 0.006 * eve + ar)
    return m


def base_load(h):
    morning = 0.55 * math.exp(-((h - 7.5) / 1.0) ** 2)
    evening = 1.0 * math.exp(-((h - 20.0) / 1.8) ** 2)
    return 0.28 + morning + evening + (0.1 if 9 <= h <= 17 else 0)


def loads_series(houses, n):
    out = {}
    for hs in houses:
        series, ev_left, ev_p = [], 0, 0.0
        for i in range(n):
            h = (i % STEPS_PER_DAY) * 5 / 60
            p = base_load(h) * hs['scale'] * (1 + random.gauss(0, 0.15))
            rate = 0.05 if 17 <= h <= 22 else 0.02
            if ev_left == 0 and random.random() < rate:
                ev_left, ev_p = random.randint(1, 4), random.uniform(1.2, 2.5)
            if ev_left:
                p += ev_p
                ev_left -= 1
            series.append(max(0.05, p))
        out[hs['id']] = series
    return out


def solve(tr, net, m, warm=None, iters=4):
    """Dengesiz radyal yük akışı (ileri-geri tarama). net[id] = (P W, Q var), + tüketim."""
    vs = [tr['v0'] * m * PH[p] for p in range(3)]
    fs = tr['feeders']
    V = warm or [[[vs[0], vs[1], vs[2], 0j] for _ in f['houses']] for f in fs]
    for _ in range(iters):
        itot, cums = [0j, 0j, 0j], []
        for fi, f in enumerate(fs):
            hs = f['houses']
            cum = [None] * len(hs)
            a0 = a1 = a2 = 0j
            for k in range(len(hs) - 1, -1, -1):
                h = hs[k]
                P, Q = net[h['id']]
                v = V[fi][k]
                S = complex(P, Q)
                if h['ph'] == 3:
                    a0 += (S / 3 / (v[0] - v[3])).conjugate()
                    a1 += (S / 3 / (v[1] - v[3])).conjugate()
                    a2 += (S / 3 / (v[2] - v[3])).conjugate()
                else:
                    c = (S / (v[h['ph']] - v[3])).conjugate()
                    if h['ph'] == 0:
                        a0 += c
                    elif h['ph'] == 1:
                        a1 += c
                    else:
                        a2 += c
                cum[k] = (a0, a1, a2)
            cums.append(cum)
            itot = [itot[0] + cum[0][0], itot[1] + cum[0][1], itot[2] + cum[0][2]]
        zt = tr['zt']
        vb = [vs[p] - zt * itot[p] for p in range(3)]
        for fi, f in enumerate(fs):
            zs, zn = f['zs'], f['zn']
            pa, pb, pc, pn = vb[0], vb[1], vb[2], 0j
            for k in range(len(f['houses'])):
                i0, i1, i2 = cums[fi][k]
                pa, pb, pc, pn = pa - zs * i0, pb - zs * i1, pc - zs * i2, pn + zn * (i0 + i1 + i2)
                V[fi][k] = [pa, pb, pc, pn]
    s_tr = abs(sum(vb[p] * itot[p].conjugate() for p in range(3))) / 1000
    return V, s_tr


def house_voltages(tr, V):
    out = {}
    for fi, f in enumerate(tr['feeders']):
        for k, h in enumerate(f['houses']):
            v = V[fi][k]
            if h['ph'] == 3:
                out[h['id']] = max(abs(v[p] - v[3]) for p in range(3))
            else:
                out[h['id']] = abs(v[h['ph']] - v[3])
    return out


def net_at(tr, i, g, loads, extra=None):
    net = {}
    for f in tr['feeders']:
        for h in f['houses']:
            p = loads[h['id']][i]
            pv = (h['pv'] + (extra.get(h['id'], 0) if extra else 0)) * g[i] * PV_DERATE
            net[h['id']] = ((p - pv) * 1000, p * 0.33 * 1000)
    return net


def simulate(trafos, g, m, loads):
    n = len(g)
    volt = {}   # id -> list
    for tr in trafos:
        warm = None
        for f in tr['feeders']:
            for h in f['houses']:
                volt[h['id']] = [0.0] * n
        for i in range(n):
            V, _ = solve(tr, net_at(tr, i, g, loads), m[i], warm, iters=3 if warm else 6)
            warm = V
            for hid, v in house_voltages(tr, V).items():
                volt[hid][i] = v
    return volt


# ---------- veri tarafı: yalnız inverter kayıtları ----------

def corr(x, y):
    mx, my = statistics.fmean(x), statistics.fmean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else 0.0


def residual_diffs(ids, rec_v, rec_p, kwp, day):
    """Gündüz 5 dk gerilim farkları; bütün köyde ortak olan bulut etkisi çıkarılmış."""
    n = len(day)
    sun = []
    for i in range(n):
        vals = sorted(rec_p[h][i] / kwp[h] for h in ids)
        sun.append(vals[len(vals) // 2])
    idx = [i for i in range(1, n) if day[i] and day[i - 1]]
    ds = [sun[i] - sun[i - 1] for i in idx]
    out = {}
    for h in ids:
        dv = [rec_v[h][i] - rec_v[h][i - 1] for i in idx]
        beta = sum(a * b for a, b in zip(ds, dv)) / sum(a * a for a in ds)
        out[h] = [v - beta * a for v, a in zip(dv, ds)]
    return out


def cluster(ids, diffs):
    """Ortalama bağlantılı hiyerarşik gruplama, uzaklık = 1 - korelasyon."""
    D = {}
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            d = 1 - corr(diffs[a], diffs[b])
            D[(a, b)] = D[(b, a)] = d

    def dist(a, b):
        return 0.0 if a == b else D[(a, b)]

    clusters = [[h] for h in ids]
    history = []
    while len(clusters) > 1:
        best = None
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                d = statistics.fmean(dist(a, b) for a in clusters[i] for b in clusters[j])
                if best is None or d < best[0]:
                    best = (d, i, j)
        d, i, j = best
        clusters[i] = clusters[i] + clusters[j]
        del clusters[j]
        history.append(([list(c) for c in clusters], d))

    def silhouette(cs):
        lab = {h: ci for ci, c in enumerate(cs) for h in c}
        vals = []
        for h in ids:
            own = [x for x in cs[lab[h]] if x != h]
            if not own:
                vals.append(0.0)
                continue
            a = statistics.fmean(dist(h, x) for x in own)
            b = min(statistics.fmean(dist(h, x) for x in c) for ci, c in enumerate(cs) if ci != lab[h])
            vals.append((b - a) / max(a, b))
        return statistics.fmean(vals)

    best = None
    for cs, _ in history:
        if 2 <= len(cs) <= 15:
            s = silhouette(cs)
            if best is None or s > best[0]:
                best = (s, cs)
    return best[1], best[0], history


def group_room(group, rec_v, rec_p, mask):
    """Grubun en hassas evi: bulut geçişlerinde kW başına volt ve sınıra kalan kW."""
    n = len(mask)
    pg = [sum(rec_p[h][i] for h in group) for i in range(n)]
    idx = [i for i in range(1, n) if mask[i] and mask[i - 1]]
    dp = [pg[i] - pg[i - 1] for i in idx]
    sxx = sum(a * a for a in dp)
    worst = None
    for h in group:
        dv = [rec_v[h][i] - rec_v[h][i - 1] for i in idx]
        s = sum(a * b for a, b in zip(dp, dv)) / sxx if sxx else 0.0   # V / kW
        vpk = max(rec_v[h])
        room = (V_LIMIT - MARGIN - vpk) / s if s > 0.01 else 999.0
        if worst is None or room < worst['room']:
            worst = dict(h=h, s=s, vpk=vpk, room=room)
    return worst


def trafo_room(members, rec_v, rec_p, mask):
    """Trafo düzeyi: bulut geçişlerinde trafonun toplam panel üretimi düşünce her evin gerilimi
    ne kadar düşüyor (V/kW); en dar evin sınıra kalan payı = trafoya eklenebilecek kW
    (yeni paneller mevcutlar gibi dağılırsa)."""
    return group_room(members, rec_v, rec_p, mask)


def solve_lin(M, y):
    """Gauss eleme (küçük sistemler)."""
    k = len(y)
    a = [row[:] + [y[i]] for i, row in enumerate(M)]
    for c in range(k):
        piv = max(range(c, k), key=lambda r: abs(a[r][c]))
        a[c], a[piv] = a[piv], a[c]
        if abs(a[c][c]) < 1e-12:
            continue
        for r in range(k):
            if r != c:
                f = a[r][c] / a[c][c]
                for cc in range(c, k + 1):
                    a[r][cc] -= f * a[c][cc]
    return [a[i][k] / a[i][i] if abs(a[i][i]) > 1e-12 else 0.0 for i in range(k)]


def sensitivities(members, rec_v, rec_n, day):
    """Her ev için: komşu j'nin şebekeye verdiği 1 kW artınca benim gerilimim kaç V artar.
    5 dk farkları üzerinde çoklu (hafif ridge) regresyon; ev yükleri birbirinden bağımsız
    oynadığı için katkılar ayrışır."""
    n = len(day)
    idx = [i for i in range(1, n) if day[i] and day[i - 1]]
    X = [[rec_n[j][i] - rec_n[j][i - 1] for j in members] for i in idx]
    k = len(members)
    XtX = [[sum(r[a] * r[b] for r in X) for b in range(k)] for a in range(k)]
    lam = 1e-3 * sum(XtX[a][a] for a in range(k)) / k
    for a in range(k):
        XtX[a][a] += lam
    S = {}
    for h in members:
        y = [rec_v[h][i] - rec_v[h][i - 1] for i in idx]
        Xty = [sum(r[a] * yy for r, yy in zip(X, y)) for a in range(k)]
        beta = solve_lin(XtX, Xty)
        S[h] = {j: b for j, b in zip(members, beta)}
    return S


def estimate_fits(members, S, vpk, order, near, rule_n, selective):
    """Doğrusal model: başvuru a eklenince her izlenen ev S[h][near[a]] * kW kadar yükselir."""
    add = {h: 0.0 for h in members}
    ok = 0
    for a in order:
        if ok >= rule_n:
            break
        j = near[a]
        trial = {h: add[h] + S[h][j] * NEW_KW * PV_DERATE for h in members}
        if all(vpk[h] + trial[h] <= V_LIMIT - MARGIN for h in members):
            add = trial
            ok += 1
        elif not selective:
            break
    return ok


def violates(tr, g, m, loads, crit, extra):
    for i in crit:
        V, s_tr = solve(tr, net_at(tr, i, g, loads, extra), m[i], None, iters=8)
        if max(house_voltages(tr, V).values()) > V_LIMIT or s_tr > tr['kva']:
            return True
    return False


def truth(tr, g, m, loads, crit, orders, rule_n):
    """Gerçek: başvuruları verilen sırayla dene; sınırı aşmayanı onayla, aşanı atla."""
    fits = []
    for order in orders:
        extra = {}
        for hid in order:
            if len(extra) >= rule_n:
                break
            extra[hid] = NEW_KW
            if violates(tr, g, m, loads, crit, extra):
                del extra[hid]
        fits.append(len(extra))
    # sırayla: ilk sınır aşımında dur (başvuru sırasına göre onay)
    fifo = []
    for order in orders:
        extra = {}
        for hid in order:
            if len(extra) >= rule_n:
                break
            extra[hid] = NEW_KW
            if violates(tr, g, m, loads, crit, extra):
                del extra[hid]
                break
        fifo.append(len(extra))
    return fits, fifo


def dist2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def main():
    trafos, houses = build()
    g, kinds = irradiance()
    m = mv_factor(g)
    loads = loads_series(houses, len(g))
    volt = simulate(trafos, g, m, loads)
    byid = {h['id']: h for h in houses}
    n = len(g)

    # VERİ: yalnız panelli evlerin inverter kaydı, yalnız gündüz (gece inverter uyur)
    pv_ids = [h['id'] for h in houses if h['pv'] > 0]
    day = [x > 0.03 for x in g]
    rec_v = {h: [round(v + random.gauss(0, 0.2), 1) for v in volt[h]] for h in pv_ids}
    rec_p = {h: [round(byid[h]['pv'] * x * PV_DERATE, 2) for x in g] for h in pv_ids}
    kwp = {h: byid[h]['pv'] for h in pv_ids}
    # inverterin sayacı: evin şebekeye verdiği net güç (panel - ev tüketimi)
    rec_n = {h: [round(byid[h]['pv'] * g[i] * PV_DERATE - loads[h][i], 2) for i in range(n)] for h in pv_ids}

    diffs = residual_diffs(pv_ids, rec_v, rec_p, kwp, day)
    groups, sil, history = cluster(pv_ids, diffs)
    # grubu haritada en yakın trafoya bağla (gerçekte: direk/trafo haritası ya da Kıb-Tek)
    gtr = []
    for c in groups:
        cx = statistics.fmean(byid[h]['xy'][0] for h in c)
        cy = statistics.fmean(byid[h]['xy'][1] for h in c)
        gtr.append(min(range(len(trafos)), key=lambda t: dist2((cx, cy), trafos[t]['xy'])))
    lab = {h: gi for gi, c in enumerate(groups) for h in c}
    right_tr = sum(1 for h in pv_ids if gtr[lab[h]] == byid[h]['t'])
    pure_feeder = 0
    for c in groups:
        cnt = {}
        for h in c:
            key = (byid[h]['t'], byid[h]['f'])
            cnt[key] = cnt.get(key, 0) + 1
        pure_feeder += max(cnt.values())
    print(f'Ev {len(houses)}, panelli (veri veren) {len(pv_ids)} (%{100*len(pv_ids)/len(houses):.0f})')
    print(f'Gruplama: {len(groups)} grup (gerçek {len(trafos)} trafo, '
          f'{sum(len(t["feeders"]) for t in trafos)} hat); trafosu doğru bulunan ev '
          f'{right_tr}/{len(pv_ids)} = %{100*right_tr/len(pv_ids):.0f}; '
          f'hattı aynı olanlar %{100*pure_feeder/len(pv_ids):.0f}; siluet {sil:.2f}')

    for cs, _ in history:
        if len(cs) == len(trafos):
            pur = 0
            for c in cs:
                cnt = {}
                for h in c:
                    cnt[byid[h]['t']] = cnt.get(byid[h]['t'], 0) + 1
                pur += max(cnt.values())
            print(f'Trafo konumu bilinmeseydi (ağacı {len(trafos)} gruba kesince) doğru: %{100*pur/len(pv_ids):.0f}')
    geo = sum(1 for h in pv_ids if min(range(len(trafos)), key=lambda t: dist2(byid[h]['xy'], trafos[t]['xy'])) == byid[h]['t'])
    print(f'Yalnız haritada en yakın trafo: %{100*geo/len(pv_ids):.0f}')

    # bulutlu günlerin gündüzü: kW başına volt buradan
    mask = [kinds[i // STEPS_PER_DAY] == 'parçalı' and 9 <= (i % STEPS_PER_DAY) * 5 / 60 <= 16
            for i in range(n)]
    rooms = [group_room(c, rec_v, rec_p, mask) for c in groups]
    # başvuru sahibinin inverteri yok: en yakın panelli komşunun grubuna say
    results = []
    for t, tr in enumerate(trafos):
        all_ids = [h['id'] for f in tr['feeders'] for h in f['houses']]
        applicants = [h for h in all_ids if byid[h]['pv'] == 0]
        installed_true = sum(byid[h]['pv'] for h in all_ids)
        my_groups = [gi for gi in range(len(groups)) if gtr[gi] == t]
        installed_est = sum(kwp[h] for gi in my_groups for h in groups[gi])
        rule_kw = 0.4 * tr['kva'] - installed_est
        members = [h for gi in my_groups for h in groups[gi]]
        tr_room = trafo_room(members, rec_v, rec_p, mask)
        S = sensitivities(members, rec_v, rec_n, day)
        vpk = {h: max(rec_v[h][i] for i in range(n) if day[i]) for h in members}
        near = {a: min(members, key=lambda h: dist2(byid[a]['xy'], byid[h]['xy'])) for a in applicants}
        rule_est = int(max(0.0, rule_kw) // NEW_KW)
        orders = []
        for _ in range(12):
            o = applicants[:]
            random.shuffle(o)
            orders.append(o)
        est_sel = [estimate_fits(members, S, vpk, o, near, rule_est, True) for o in orders]
        est_fifo = [estimate_fits(members, S, vpk, o, near, rule_est, False) for o in orders]

        vmax_t = [max(volt[h][i] for h in all_ids) for i in range(n)]
        crit = sorted(range(n), key=lambda i: -vmax_t[i])[:6] + sorted(range(n), key=lambda i: -g[i])[:3]
        rule_true = int(max(0.0, 0.4 * tr['kva'] - installed_true) // NEW_KW)
        fits, fifo = truth(tr, g, m, loads, crit, orders, rule_true)
        diag = [S[h][h] for h in members]
        r = dict(trafo=tr['ad'], kva=tr['kva'], ev=len(all_ids), panelli=sum(1 for h in all_ids if byid[h]['pv']),
                 kurulu_kw=installed_true, kural_payi_kw=round(0.4 * tr['kva'] - installed_true, 1),
                 bugunku_tepe_v=round(max(vmax_t), 1),
                 grup_sayisi=len(my_groups),
                 en_dar_ev_tepe_v=round(tr_room['vpk'], 1), v_per_kw_trafo=round(tr_room['s'], 3),
                 gerilim_payi_kw=round(tr_room['room'], 1), kural_payi_tahmin_kw=round(rule_kw, 1),
                 kendi_v_per_kw_ort=round(statistics.fmean(diag), 3),
                 tahmin_secerek=round(statistics.fmean(est_sel), 1), tahmin_sirayla=round(statistics.fmean(est_fifo), 1),
                 gercek_secerek=round(statistics.fmean(fits), 1),
                 gercek_sirayla=round(statistics.fmean(fifo), 1), gercek_sirayla_aralik=[min(fifo), max(fifo)])
        results.append(r)
        print(json.dumps(r, ensure_ascii=False))

    out = dict(houses=[dict(id=h['id'], t=h['t'], f=h['f'], pv=h['pv'],
                            xy=[round(h['xy'][0]), round(h['xy'][1])], grup=lab.get(h['id']))
                       for h in houses],
               trafos=[dict(ad=t['ad'], kva=t['kva'], xy=t['xy']) for t in trafos], sonuc=results)
    with open(sys.argv[2] if len(sys.argv) > 2 else 'trafo_bos_kapasite_sonuc.json', 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
