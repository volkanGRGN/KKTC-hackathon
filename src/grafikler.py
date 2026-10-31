#!/usr/bin/env python3
"""Faz 2 grafikleri: kalibrasyon ve "kaç trafo ölçmeli". Her grafikte "gösterim — farazi şehirler".

Bu dosya Can'ın (kart: docs/gorev/can-faz2-sinav-grafikler.md). Okuduğu dosyalar sözleşmede
(docs/data/tablo-bicimi.md §5); ölçü tanımları src/sinav.py ile aynı (oradan alınır).

Çalıştırma: python3 src/grafikler.py faz2 data/synthetic outputs/ [--aralik 11-20]
"""
import re
import statistics as st
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

import sinav  # noqa: E402

ETIKET = 'gösterim — farazi şehirler'


def _kapsama(tahmin, gercek):
    """Ölçülmeyen trafolarda (kapsama, P10 altı payı, P90 üstü payı)."""
    ic = alt = ust = n = 0
    for r in tahmin:
        if int(r['olculdu']):
            continue
        g = gercek[r['trafo_no']]
        lo, hi = float(r['ogle_min_kw_p10']), float(r['ogle_min_kw_p90'])
        n += 1
        ic += lo <= g <= hi
        alt += g < lo
        ust += g > hi
    return ic / n, alt / n, ust / n


def kalibrasyon(sehirler, cikti):
    ad = [s['ad'].replace('sehir-', '') for s in sehirler]
    k = [_kapsama(s['tahmin'], s['gercek']) for s in sehirler]
    x = range(len(sehirler))
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.5), gridspec_kw=dict(width_ratios=[3, 2]))
    a1.axhspan(100 * sinav.KAPSAMA[0], 100 * sinav.KAPSAMA[1], color='#2e7d32', alpha=0.12,
               label=f'hedef %{100 * sinav.KAPSAMA[0]:g}–{100 * sinav.KAPSAMA[1]:g}')
    a1.axhline(80, color='#2e7d32', lw=0.8, ls='--')
    a1.plot(x, [100 * v[0] for v in k], 'o', color='#1565c0', label='şehrin bant kapsaması')
    a1.set_xticks(list(x), ad, fontsize=8)
    a1.set_xlabel('şehir')
    a1.set_ylabel('gerçek değer %80 bandın içinde (%)')
    a1.set_ylim(0, 105)
    a1.set_title('Kalibrasyon: %80 bant gerçeği ne sıklıkla kapsıyor')
    a1.legend(loc='lower left', fontsize=8)
    alt = [100 * v[1] for v in k]
    ust = [100 * v[2] for v in k]
    a2.bar([0, 1], [st.median(alt), st.median(ust)], color=['#ef6c00', '#6a1b9a'], width=0.5)
    a2.plot([0] * len(alt), alt, 'k.', alpha=0.4)
    a2.plot([1] * len(ust), ust, 'k.', alpha=0.4)
    a2.axhline(10, color='grey', lw=0.8, ls='--', label='beklenen %10')
    a2.set_xticks([0, 1], ['gerçek < P10\n(tahmin fazla)', 'gerçek > P90\n(tahmin az)'])
    a2.set_ylabel('ölçülmeyen trafoların payı (%)')
    a2.set_title('Bandın dışı: iki taraf dengeli mi (çubuk = ortanca)')
    a2.legend(fontsize=8)
    fig.suptitle(ETIKET, color='#b71c1c', fontsize=10)
    fig.tight_layout()
    yol = Path(cikti) / 'faz2_kalibrasyon.png'
    fig.savefig(yol, dpi=130)
    plt.close(fig)
    return yol


def kac_trafo(sehirler, cikti):
    """x = ölçülü sayısı, y = hata ortancası (tekrarların ve şehirlerin ortancası, P10–P90 gölgesi) + kapsama."""
    nokta = {}   # n -> [(şehir başına hata ortancası, kapsama)]
    for s in sehirler:
        for ad, d in s['deney'].items():
            m = re.fullmatch(r'tahmin_n(\d+)_t\d+', ad)
            if m:
                nokta.setdefault(int(m.group(1)), []).append(d)
        nokta.setdefault(int(s['tahmin'][0]['olculu_sayi']), []).append(s['tahmin'])
    n_list = sorted(nokta)
    gercek = {s['no']: s['gercek'] for s in sehirler}
    orta, p10, p90, kap = [], [], [], []
    for n in n_list:
        hata, kp = [], []
        for d in nokta[n]:            # her dosya bir şehrin; şehir satırdaki `sehir`den
            g = gercek[int(d[0]['sehir'])]
            h = sinav._hatalar(d, g)[0]
            if h:
                hata.append(st.median(h))
                kp.append(_kapsama(d, g)[0])
        q = st.quantiles(hata, n=10, method='inclusive') if len(hata) > 1 else [hata[0]] * 9
        orta.append(100 * st.median(hata))
        p10.append(100 * q[0])
        p90.append(100 * q[-1])
        kap.append(100 * st.median(kp))
    fig, a1 = plt.subplots(figsize=(8, 4.8))
    a1.fill_between(n_list, p10, p90, color='#1565c0', alpha=0.15, label='hata P10–P90 (şehir × tekrar)')
    a1.plot(n_list, orta, 'o-', color='#1565c0', label='öğlen yük hatası, ortanca')
    a1.axhline(100 * sinav.HATA_ORTANCA_MAX, color='#1565c0', lw=0.8, ls='--', label='eşik: ortanca %15')
    a1.set_xlabel('ölçülü trafo sayısı (şehir başına, 40 trafodan)')
    a1.set_ylabel('öğlen en düşük yük hatası (%)')
    a1.set_xticks(n_list)
    a1.set_ylim(bottom=0)
    a2 = a1.twinx()
    a2.plot(n_list, kap, 's--', color='#2e7d32', label='%80 bant kapsama, ortanca')
    a2.axhspan(100 * sinav.KAPSAMA[0], 100 * sinav.KAPSAMA[1], color='#2e7d32', alpha=0.07)
    a2.set_ylabel('bant kapsama (%)', color='#2e7d32')
    a2.set_ylim(0, 105)
    h1, l1 = a1.get_legend_handles_labels()
    h2, l2 = a2.get_legend_handles_labels()
    a1.legend(h1 + h2, l1 + l2, fontsize=8, loc='center right')
    a1.set_title('Kaç trafo ölçmeli: ölçülü sayısı arttıkça hata ve kapsama')
    fig.suptitle(ETIKET, color='#b71c1c', fontsize=10)
    fig.tight_layout()
    yol = Path(cikti) / 'faz2_kac_trafo.png'
    fig.savefig(yol, dpi=130)
    plt.close(fig)
    return yol, list(zip(n_list, orta, p10, p90, kap))


def kilit(sehirler, cikti, aralik):
    """Sunumun kilit grafiği: dolu trafoya "yer var" — model yeşili ile %40 kuralı, aynı trafolarda."""
    yer = {'Bizim yöntem\n(yeşil)': lambda k: k['renk'] == 'yesil',
           '%40 kuralı\n(bugünkü pratik)': lambda k: int(k['kural40_ev']) >= 1}
    yanlis, toplam, dolu_yer, sehir_oran = {}, {}, {}, {}
    dolu = 0
    for ad, f in yer.items():
        yanlis[ad] = toplam[ad] = dolu_yer[ad] = 0
        sehir_oran[ad] = []
    for s in sehirler:
        say = {ad: [0, 0] for ad in yer}
        for r in s['cevap']:
            if int(r['kac_ev_aday']) == 0:
                continue
            k = s['kac_ev'][r['trafo_no']]
            d = int(r['kac_ev_gercek']) == 0
            dolu += d
            for ad, f in yer.items():
                if f(k):
                    say[ad][0] += d
                    say[ad][1] += 1
                    dolu_yer[ad] += d
        for ad in yer:
            yanlis[ad] += say[ad][0]
            toplam[ad] += say[ad][1]
            if say[ad][1]:
                sehir_oran[ad].append(100 * say[ad][0] / say[ad][1])
    renk = ['#2e7d32', '#c62828']
    adlar = list(yer)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.8))
    oran = [100 * yanlis[a] / toplam[a] if toplam[a] else 0 for a in adlar]
    a1.bar([0, 1], oran, color=renk, width=0.55)
    for i, a in enumerate(adlar):
        a1.plot([i] * len(sehir_oran[a]), sehir_oran[a], 'k.', alpha=0.45)
        ust = max([oran[i]] + sehir_oran[a])
        a1.text(i, ust + 1, f'%{oran[i]:.0f}\n{yanlis[a]} / {toplam[a]}', ha='center', va='bottom', fontsize=11)
    a1.set_xticks([0, 1], adlar)
    a1.set_ylabel('"yer var" dediklerinden gerçekte dolu (%)')
    a1.set_title('Yanlış yeşil: "yer var" dedi, trafo doluydu\n(nokta = şehir)')
    a1.set_ylim(0, max(30, max(max(v, default=0) for v in sehir_oran.values()) + 12))
    pay = [100 * dolu_yer[a] / dolu if dolu else 0 for a in adlar]
    a2.bar([0, 1], pay, color=renk, width=0.55)
    for i, a in enumerate(adlar):
        a2.text(i, pay[i] + 1.5, f'{dolu_yer[a]} / {dolu}', ha='center', va='bottom', fontsize=11)
    a2.set_xticks([0, 1], adlar)
    a2.set_ylabel('dolu trafoların "yer var" denen payı (%)')
    a2.set_title(f'Dolu {dolu} trafodan kaçına "yer var" dendi')
    a2.set_ylim(0, 100)
    fig.suptitle(f'Dolu trafoya "yer var" demek — farazi şehir, gösterim ({aralik})', color='#b71c1c', fontsize=11)
    fig.tight_layout()
    yol = Path(cikti) / 'kilit_yanlis_yesil.png'
    fig.savefig(yol, dpi=150)
    plt.close(fig)
    return yol, {a: (yanlis[a], toplam[a], dolu_yer[a], dolu) for a in adlar}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 4 or sys.argv[1] not in ('faz2', 'faz3'):
        sys.exit('Kullanım: python3 src/grafikler.py faz2|faz3 <şehir kökü> <çıktı klasörü> [--aralik 11-20]')
    sehirler, _ = sinav.sehirleri_oku(sys.argv[2])
    aralik = 'şehir ' + (sys.argv[sys.argv.index('--aralik') + 1] if '--aralik' in sys.argv else 'hepsi')
    if '--aralik' in sys.argv:
        a, b = map(int, sys.argv[sys.argv.index('--aralik') + 1].split('-'))
        sehirler = [s for s in sehirler if a <= s['no'] <= b]
    if sys.argv[1] == 'faz3':
        sehirler = [s for s in sehirler if not sinav.faz3_oku(s)]
        if not sehirler:
            sys.exit('kac_ev.csv olan şehir yok (önce src/kac_ev.py).')
        cikti = Path(sys.argv[3])
        cikti.mkdir(parents=True, exist_ok=True)
        yol, s = kilit(sehirler, cikti, aralik)
        print(yol)
        for a, (y, t, dy, d) in s.items():
            print(f"  {a.splitlines()[0]}: yanlış yeşil {y}/{t}, dolu trafoya yer var {dy}/{d}")
        return
    sehirler = [s for s in sehirler if not sinav.faz2_oku(s)]
    if not sehirler:
        sys.exit('tahmin.csv olan şehir yok (önce src/sablon.py).')
    for s in sehirler:
        s['gercek'] = {r['trafo_no']: float(r['ogle_min_kw']) for r in s['cevap']}
    cikti = Path(sys.argv[3])
    cikti.mkdir(parents=True, exist_ok=True)
    print(kalibrasyon(sehirler, cikti))
    yol, satir = kac_trafo(sehirler, cikti)
    print(yol)
    for n, o, lo, hi, k in satir:
        print(f'  ölçülü {n:2d}: hata ortanca %{o:.1f} (P10–P90 %{lo:.1f}–{hi:.1f}), kapsama %{k:.0f}')


if __name__ == '__main__':
    main()
