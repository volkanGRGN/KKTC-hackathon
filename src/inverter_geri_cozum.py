#!/usr/bin/env python3
"""İnverter geriliminden geri çözüm, benzetimde gerçekten (deneme; Muhittin 4 madde 5B; karar masası 22:56, 23:03).

Sahte kayıt (`sahte_kayit.kayit_uret`) inverter kaydını "gerçek değer + gürültü" diye yazıyor (bara ±1 V, hat ±%20;
iki kat düzeyde ±2 V / ±%40) ve PR #20 sakin anı 05:00–06:30 alıyordu. Ama şebekeye bağlı inverter gece uyur (Faz 10
kartı): kaydında yalnız gündüz var. Bu betik her panelli evin inverterinin göreceği seriyi gerçek ağda üretir (aynı
yük, ışınım, OG; `sahte_kayit.gercek_trafo`) ve **yalnız inverterin bildiğiyle** (kendi ev gerilimi, kendi panel
gücü, saat) geri çözer:
  bara      sabah ilk değer: her gün inverterin ilk uyanık adımındaki gerilim (güneş zayıf), 14 günün ortancası;
            ayrıca gündüz doğrusu V = a + s × P_kendi'nin kesişimi a
  salınım   s: kendi panel gücünün kW'ı başına gerilim (V/kW), gündüz doğrusunun eğimi; günden güne oynaklığı
Gerçekle kıyas: bara hatası = tahmin − trafonun boşta gerilimi (`v0`, modelin bilinmeyeni). Uyanık sayılma:
ışınım > UYANIK_G (STC'nin payı).

Etiket: farazi şehir, gösterim; tek ev, inverter ucu. Resmi hesap ve motor değişmez.

Çalıştırma:
  python3 src/inverter_geri_cozum.py <şehir kökü> --aralik 1-10 [--json cikti.json]
"""
import argparse
import json
import statistics as st
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

_argv, sys.argv = sys.argv, sys.argv[:1]
import sahte_kayit as sk  # noqa: E402
import sehir_uret as su  # noqa: E402
import trafo_bos_kapasite as tb  # noqa: E402
sys.argv = _argv

UYANIK_G = 0.02                 # inverter ışınım STC'nin %2'sini geçince uyanık sayılır [Yorum]
SAKIN = (5 * 12, 6 * 12 + 6)    # PR #20'nin sakin anı 05:00–06:30 (adım 60–77)


def nicel(x, q):
    x = sorted(x)
    return x[min(len(x) - 1, max(0, int(round(q * (len(x) - 1)))))] if x else float('nan')


def dogru(xy):
    """En küçük kareler: y = a + s x. Dönüş (a, s)."""
    n = len(xy)
    mx = sum(x for x, _ in xy) / n
    my = sum(y for _, y in xy) / n
    sxx = sum((x - mx) ** 2 for x, _ in xy)
    s = sum((x - mx) * (y - my) for x, y in xy) / sxx if sxx else 0.0
    return my - s * mx, s


def sehir_coz(klasor):
    sehir = sk.gercek_sehir(Path(klasor))
    g, m = sehir['g'], sehir['m']
    gun_n = len(g) // su.ADIM
    sakin_g = sum(g[d * su.ADIM + i] > UYANIK_G for d in range(gun_n) for i in range(*SAKIN))
    out = []
    for no in sehir['trafolar']:
        tr = sehir['trafolar'][no]
        panelli = [h for h in tr['evler'] if h['pv'] > 0]
        if not panelli:
            continue
        gt = sk.gercek_trafo(sehir, no)
        yuk = gt['yuk']
        seri = {h['id']: [] for h in panelli}
        V = None
        for i in range(len(g)):
            if g[i] <= UYANIK_G:
                V = None
                continue
            V, _ = tb.solve(tr, su.net_guc(tr, i, g, yuk), m[i], V, iters=4 if V else 8)
            hv = tb.house_voltages(tr, V)
            for h in panelli:
                seri[h['id']].append((i, hv[h['id']], h['pv'] * g[i] * tb.PV_DERATE))
        yer = sk.ev_yeri(tr)
        for h in panelli:
            s_ = seri[h['id']]
            ilk = {}
            for i, v, _ in s_:
                ilk.setdefault(i // su.ADIM, (i, v))
            b_sabah = st.median(v for _, v in ilk.values())
            a, egim = dogru([(p, v) for _, v, p in s_])
            gun_egim = []
            for d in range(gun_n):
                xy = [(p, v) for i, v, p in s_ if i // su.ADIM == d]
                if len(xy) > 10 and max(p for p, _ in xy) > 0.3 * h['pv']:
                    gun_egim.append(dogru(xy)[1])
            j, k, n = yer[h['id']]
            out.append(dict(sehir=sehir['tohum'], trafo_no=no, ev=h['id'], ph=h['ph'], pv=h['pv'], hat=j,
                            yer=round((k + 1) / n, 3), hat_boy=tr['feeders'][j]['boy'], v0=tr['v0'],
                            b_sabah=round(b_sabah, 2), b_kesisim=round(a, 2), egim=round(egim, 4),
                            gun_egim=[round(x, 4) for x in gun_egim],
                            ilk_saat=st.median(i % su.ADIM for i, _ in ilk.values()) * 5 / 60))
    return dict(sehir=sehir['tohum'], sakin_uyanik=sakin_g, sakin_n=gun_n * (SAKIN[1] - SAKIN[0]), evler=out)


def ozet(evler, ad, f):
    e = [f(x) for x in evler]
    if not e:
        return f'{ad}: —'
    a1 = sum(abs(x) <= 1 for x in e)
    a2 = sum(abs(x) <= 2 for x in e)
    return (f'{ad}: n {len(e)} | ortanca {st.median(e):+.2f} V | P10–P90 {nicel(e, .1):+.2f} … {nicel(e, .9):+.2f} V | '
            f'|hata| ≤ 1 V %{100 * a1 / len(e):.0f} | ≤ 2 V %{100 * a2 / len(e):.0f}')


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('kok')
    ap.add_argument('--aralik', default='1-10')
    ap.add_argument('--json')
    a = ap.parse_args()
    bas, son = (int(x) for x in a.aralik.split('-'))
    klasorler = [str(Path(a.kok) / f'sehir-{t:03d}') for t in range(bas, son + 1)]
    with ProcessPoolExecutor() as ex:
        sonuc = list(ex.map(sehir_coz, klasorler))
    evler = [x for s in sonuc for x in s['evler']]
    print(f'şehir {a.aralik} — inverter geri çözümü, benzetimde; farazi, gösterim; panelli ev {len(evler)}, '
          f'trafo {len({(x["sehir"], x["trafo_no"]) for x in evler})}')
    su_n = sum(s['sakin_uyanik'] for s in sonuc)
    sn = sum(s['sakin_n'] for s in sonuc)
    print(f'PR #20 sakin anı (05:00–06:30) adımlarının inverterin uyanık olduğu payı: %{100 * su_n / sn:.1f} ({su_n}/{sn}); '
          f'ilk uyanık adım saati ortancası {st.median(x["ilk_saat"] for x in evler):.2f}')
    print('bara hatası = tahmin − v0 (trafonun boşta gerilimi):')
    print('  ' + ozet(evler, 'sabah ilk değer', lambda x: x['b_sabah'] - x['v0']))
    print('  ' + ozet(evler, 'gündüz doğrusu kesişimi', lambda x: x['b_kesisim'] - x['v0']))
    for lo, hi, ad in ((0, 0.34, 'hattın başı (yer ≤ 1/3)'), (0.34, 0.67, 'ortası'), (0.67, 1.01, 'ucu (yer > 2/3)')):
        print('  ' + ozet([x for x in evler if lo < x['yer'] <= hi], f'sabah ilk değer, {ad}', lambda x: x['b_sabah'] - x['v0']))
    cv = [st.pstdev(x['gun_egim']) / abs(st.mean(x['gun_egim'])) for x in evler
          if len(x['gun_egim']) >= 5 and abs(st.mean(x['gun_egim'])) > 1e-3]
    print(f'salınım eğimi (V/kW, kendi paneli): ortanca {st.median(x["egim"] for x in evler):.3f}; günden güne oynaklık '
          f'(std ÷ ort) ortanca %{100 * st.median(cv):.0f}, P90 %{100 * nicel(cv, .9):.0f} (n {len(cv)})')
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(dict(aralik=a.aralik, uyanik_g=UYANIK_G, sehirler=sonuc), fh, ensure_ascii=False)


if __name__ == '__main__':
    main()
