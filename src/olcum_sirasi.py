#!/usr/bin/env python3
"""Faz 10 ölçüm sırası (karar masası 01:01): her renksiz trafo için hangi tek ucuz ölçüm onu yeşile ya da "büyük
olasılıkla dolu" bayrağına en çok taşır; pilot için ilk 20 trafo. `bilgi_degeri.py`'nin gerçekçi ve ölçüm öncesi sürümü.

Ölçümler (gerçek tarafı benzetimin kendi dosyalarından; model yalnız ölçüm sonucunu görür):
  gece    akıllı priz, gece 00:00–05:00: trafodaki bir evin gece gerilimi, 14 gecenin ortancası. Gerçek tarafı:
          `yuk_5dk.csv`'nin o adımdaki en düşük ve en yüksek ev gerilimi arasında trafoya özgü sabit bir yer (prizin
          evi hattın neresinde bilinmez) [Yorum]. Model: bara = ölçüm − hata, hata 1–10'da ölçülen nicelik
          dağılımından, **tarife grubuna göre** (`GECE_HATA_Q`, `--kalibrasyon`; karar masası 02:5x, TEST'in bulgusu:
          gece hatası trafonun abone karışımına göre çok farklı). Grup yalnız Kıb-Tek'in bildiğinden (`trafolar.csv`):
          tahmini enerjisi en büyük tarife (su motoru, sanayi, turizm, ticari, konut) ve konutta en uzun hat
          ≥ KONUT_HAT_M (kırsal) ya da değil. Cevap anahtarının trafo tipi kullanılmaz (sınav sızar).
  yuk     trafo başında bir haftalık öğlen yükü: ilk 7 günün 11:00–14:00 tüketiminin en düşüğü. Trafo ölçülü sayılır
          (`sablon.py`'nin kuralı: öğlen yükü = ölçülen, güven yüksek).
  kademe  plaka / kademe fotoğrafı: trafonun kendi kademesi (5 pozisyon, ±2 × %2,5; boşta gerilime en yakın). Bara bu
          kademenin ±3,125 V penceresinde (başvuru motorunun kademe kaydı gibi; fotoğraf doğru sayılır) [Yorum].
Renk kuralı resmi hesabınki (ADR-0010 / 0011 / 0017 / 0019): yeşil = ilk iki başvuru ≥ %98 sığar (ADR-0019'dan beri güven
şartı yok; `kac_ev_olasilik.YESIL_GUVEN_SARTI`); bayrak =
bugün aşma olasılığı ≥ 0,7, ama gece prizi ve kademe fotoğrafından sonra bayrak yok (yalnız yeşil yönü; karar masası
01:22); açılan ev = yeşile dönen trafonun karamsar kaç evi (çekilişlerin P10'u).

**Ölçüm öncesi** (sıralama; cevap anahtarına bakılmaz): her ölçüm için modelin kendi öncülünden K varsayımsal sonuç
çekilir (bara U(244, 252) + gece hatası; öğlen yükü Faz 2 bandından; kademe baradan), her biriyle renk yeniden
hesaplanır; beklenen yeşile dönme, bayrağa dönme ve açılan ev. Trafonun en iyi ölçümü = beklenen açılan ev en büyük
(eşitlikte bayrak olasılığı). **Ölçüm sonrası** (doğrulama, cevap anahtarıyla): gerçek ölçüm sonucuyla renk; yanlış
yeşil (kapı), bayrak isabeti, gerçekleşen açılan ev; ilk 20 trafo ↔ rastgele 20 renksiz trafo (ortalama).
Çekilişler resmi hesabın rastgele akışıyla (bilgi ayrı akıştan): bilgisiz koşum `kac_ev.csv` ile birebir.

Etiket: farazi şehir, gösterim. Çalıştırma:
  python3 src/olcum_sirasi.py data/synthetic/u13 --aralik 1-10 --kalibrasyon      # GECE_HATA_Q'yu yazar
  python3 src/olcum_sirasi.py data/synthetic/u13 --aralik 1-10 [--json cikti.json]
"""
import argparse
import csv
import json
import math
import random
import statistics as st
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

_argv, sys.argv = sys.argv, sys.argv[:1]
import kac_ev_olasilik as ko  # noqa: E402
sys.argv = _argv

OLCUMLER = ('gece', 'yuk', 'kademe')
K = 8                                            # ölçüm başına varsayımsal sonuç
KADEME_V = [250 + 6.25 * k for k in (-2, -1, 0, 1, 2)]
KADEME_PENCERE_V = 3.125
GECE = range(0, 60)                              # 00:00–04:55
OGLE = range(132, 168)                           # 11:00–13:55
# Gece prizi ölçümü − gerçek boşta gerilim (V), %0, %5, …, %100; geliştirme 1–10'dan (`--kalibrasyon`) [Hesap].
# Havuz (tek dağılım; grup ayrımından önce ve küçük grupların kaydırma tabanı):
GECE_HATA_Q = [-8.03, -3.92, -2.79, -2.39, -2.06, -1.84, -1.66, -1.54, -1.39, -1.26, -1.16, -1.09, -1.02, -0.93, -0.82,
               -0.77, -0.69, -0.63, -0.53, -0.41, -0.03]      # üretici 1.5, 400 trafo; hep aşağı, ortanca −1,16 V
# (üretici 1.3 kalibrasyonu ortanca −1,64 V idi)
KONUT_HAT_M = 400.0                      # konutta kırsal / kısa hat ayrımı (1–10'da seçildi) [Yorum]
KUCUK_GRUP = 30                          # bundan az trafolu grupta havuz dağılımı grubun ortancasına kaydırılır
# {tarife grubu: 21 nicelik}; üretici 1.5, 1–10, `--kalibrasyon` [Hesap]. Ortancalar: sulama −3,75, sanayi −2,06,
# turizm −1,31, konut kırsal −1,16, ticari −1,01, konut kısa −0,83 V (n 37 / 34 / 42 / 104 / 89 / 94)
GECE_HATA_GRUP = {
    'konut_kirsal': [-5.07, -3.55, -2.65, -2.38, -2.07, -1.88, -1.75, -1.59, -1.43, -1.27, -1.12, -1.01, -0.91, -0.8,
                     -0.78, -0.71, -0.65, -0.6, -0.41, -0.31, -0.03],
    'konut_kisa': [-3.52, -2.2, -1.75, -1.6, -1.52, -1.36, -1.11, -1.06, -1.02, -0.95, -0.83, -0.77, -0.71, -0.66, -0.63,
                   -0.55, -0.51, -0.47, -0.43, -0.34, -0.28],
    'sanayi': [-4.02, -3.11, -3.08, -2.73, -2.68, -2.56, -2.49, -2.38, -2.37, -2.24, -2.12, -2.0, -1.93, -1.89, -1.82,
               -1.6, -1.58, -1.55, -1.39, -1.29, -0.87],
    'sulama': [-8.03, -6.78, -6.13, -6.01, -5.01, -4.74, -4.33, -4.17, -4.06, -3.92, -3.75, -3.28, -3.0, -2.96, -2.79,
               -2.68, -2.34, -2.24, -2.19, -2.05, -1.39],
    'ticari': [-2.32, -1.7, -1.47, -1.41, -1.24, -1.18, -1.16, -1.12, -1.1, -1.06, -1.01, -0.94, -0.9, -0.83, -0.8,
               -0.74, -0.71, -0.64, -0.59, -0.5, -0.12],
    'turizm': [-2.35, -1.82, -1.78, -1.73, -1.56, -1.54, -1.45, -1.4, -1.39, -1.36, -1.32, -1.26, -1.1, -1.05, -1.03,
               -1.02, -1.0, -0.88, -0.82, -0.69, -0.67],
}


def tarife_grubu(tr):
    """Trafonun tarife grubu, yalnız Kıb-Tek'in bildiğinden: tahmini enerjisi en büyük abone sınıfı (abone sayısı ×
    sınıfın ortalama yıllık MWh'i, `kac_ev_olasilik.MWH`); konutta en uzun hat KONUT_HAT_M'den uzunsa kırsal."""
    en = {c: float(tr[c]) * ko.MWH[c] for c in ko.ABONE}
    b = max(en, key=en.get)
    if b == 'abone_su_motoru':
        return 'sulama'
    if b in ('abone_sanayi1', 'abone_sanayi2'):
        return 'sanayi'
    if b == 'abone_turizm':
        return 'turizm'
    if b in ('abone_ticari1', 'abone_ticari2'):
        return 'ticari'
    return 'konut_kirsal' if float(tr['hat_boyu_max_m']) >= KONUT_HAT_M else 'konut_kisa'


def gece_q(grup):
    """Grubun gece hatası nicelikleri; grup kalibre edilmemişse havuz."""
    return (GECE_HATA_GRUP or {}).get(grup) or GECE_HATA_Q


def _csv(yol):
    with open(yol, encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


def _nicelden(q, rng):
    u = rng.random() * (len(q) - 1)
    i = int(u)
    return q[i] + (q[min(i + 1, len(q) - 1)] - q[i]) * (u - i)


def cek(tr, t, rng, vrng, v0=None, yuk=None):
    """Resmi `trafo_cek` (aynı çekilişler), bilgi ayrı akıştan (vrng): v0 = callable(vrng) ya da None, yuk = ölçülen
    öğlen yükü ya da None. Dönüş (p_bugun, p_iki, karamsar kaç ev)."""
    p_bugun, p_iki, kac = ko.cekilis_ozeti(tr, ko.trafo_cek(tr, t, rng, v0=v0, vrng=vrng, yuk=yuk))
    return p_bugun, p_iki, ko.nicel(kac, 0.1)


def uc(p_bugun, p_iki, guven, olcum=None):
    """Ölçüm sonrası durum. Gece prizi ve kademe fotoğrafından sonra yalnız yeşil yönü, bayrak yok (karar masası
    01:22: bu ölçümlerden sonraki bayraklar 21–30'da 3/15 ve 0/7 doğruydu)."""
    if p_iki >= ko.YESIL_P and (not ko.YESIL_GUVEN_SARTI or guven == 'yuksek'):      # ADR-0019
        return 'yesil'
    if olcum in ('gece', 'kademe'):
        return 'bos'
    return 'dolu_bayrak' if p_bugun >= getattr(ko, 'BAYRAK_P', 0.7) else 'bos'


def gercek_olcumler(klasor):
    """Gerçek tarafı: {trafo_no: dict(gece=V, yuk=kW, kademe=V, v0=V)} (cevap anahtarı ve 5 dk dosyası)."""
    cevap = {r['trafo_no']: r for r in _csv(klasor / 'cevap_anahtari.csv')}
    gece, ogle = {}, {}
    sehir = None
    for r in _csv(klasor / 'yuk_5dk.csv'):
        sehir = r['sehir']
        a, no = int(r['adim']), r['trafo_no']
        if a in GECE:
            u = random.Random(f'priz-{sehir}-{no}').random()      # prizin evi: trafoya özgü sabit yer
            lo, hi = float(r['v_min_v']), float(r['v_max_v'])
            gece.setdefault(no, []).append(lo + u * (hi - lo))
        elif a in OGLE and int(r['gun']) < 7:
            ogle[no] = min(ogle.get(no, 1e9), float(r['tuketim_kw']))
    out = {}
    for no, c in cevap.items():
        v0 = float(c['v0_v'])
        out[no] = dict(v0=v0, gece=st.median(gece[no]) if no in gece else None, yuk=ogle.get(no),
                       kademe=min(KADEME_V, key=lambda v: abs(v - v0)))
    return out


def bilgi(olcum, deger, grup=None):
    """Ölçüm sonucu → cek()'in v0 / yuk argümanları."""
    if olcum == 'gece':
        q = gece_q(grup)
        return dict(v0=lambda r, b=deger, q=q: b - _nicelden(q, r))
    if olcum == 'kademe':
        lo, hi = max(ko.V0[0], deger - KADEME_PENCERE_V), min(ko.V0[1], deger + KADEME_PENCERE_V)
        return dict(v0=lambda r, a=lo, b=hi: r.uniform(a, b))
    return dict(yuk=deger)


def varsayimsal(olcum, t, rng, grup=None):
    """Modelin öncülünden bir varsayımsal ölçüm sonucu (cevap anahtarına bakmadan)."""
    if olcum == 'gece':
        return rng.uniform(*ko.V0) + _nicelden(gece_q(grup), rng)
    if olcum == 'kademe':
        v0 = rng.uniform(*ko.V0)
        return min(KADEME_V, key=lambda v: abs(v - v0))
    mu, sd = ko.yuk_bandi(t)
    return math.exp(rng.gauss(mu, sd))


def sehir_isle(is_):
    klasor, kalibrasyon = Path(is_[0]), is_[1]
    gercek = gercek_olcumler(klasor)
    trafolar = _csv(klasor / 'trafolar.csv')
    if kalibrasyon:
        grup = {r['trafo_no']: tarife_grubu(r) for r in trafolar}
        return dict(sehir=klasor.name, gece_hata=[(grup[no], g['gece'] - g['v0']) for no, g in gercek.items() if g['gece']])
    tahmin = {r['trafo_no']: r for r in _csv(klasor / 'tahmin.csv')}
    resmi = {r['trafo_no']: r for r in _csv(klasor / 'kac_ev.csv')}
    cevap = {r['trafo_no']: r for r in _csv(klasor / 'cevap_anahtari.csv')}
    out = []
    for r in trafolar:
        no = r['trafo_no']
        if resmi[no]['pv_uc'] != 'bos' or int(cevap[no]['kac_ev_aday']) <= 0:
            continue
        tr = ko.trafo_satiri(r)
        t = tahmin[no]
        rng_ad = f'olasilik-{r["sehir"]}-{no}'                      # resmi akış
        grup = tarife_grubu(r)
        satir = dict(sehir=int(r['sehir']), trafo_no=no, guven=t['guven'], grup=grup, p_bugun=float(resmi[no]['p_bugun_asar']),
                     dolu=int(cevap[no]['kac_ev_gercek']) == 0, kac_ev_gercek=int(cevap[no]['kac_ev_gercek']), olcum={})
        for o in OLCUMLER:
            t_o = dict(t, guven='yuksek') if o == 'yuk' else t
            beklenen = []
            vr = random.Random(f'olcum-oncesi-{o}-{r["sehir"]}-{no}')
            for k in range(K):
                d = varsayimsal(o, t, vr, grup)
                pb, pi, kar = cek(tr, t_o, random.Random(rng_ad), random.Random(f'bilgi-{o}-{k}-{r["sehir"]}-{no}'),
                                  **bilgi(o, d, grup))
                u_ = uc(pb, pi, t_o['guven'], o)
                beklenen.append((u_, kar if u_ == 'yesil' else 0))
            g = gercek[no][o]
            pb, pi, kar = cek(tr, t_o, random.Random(rng_ad), random.Random(f'bilgi-{o}-g-{r["sehir"]}-{no}'),
                              **bilgi(o, g, grup))
            u_ = uc(pb, pi, t_o['guven'], o)
            satir['olcum'][o] = dict(
                p_yesil=sum(x[0] == 'yesil' for x in beklenen) / K, p_bayrak=sum(x[0] == 'dolu_bayrak' for x in beklenen) / K,
                beklenen_ev=sum(x[1] for x in beklenen) / K, deger=round(g, 2), uc=u_, ev=kar if u_ == 'yesil' else 0)
        en = max(OLCUMLER, key=lambda o: (satir['olcum'][o]['beklenen_ev'], satir['olcum'][o]['p_bayrak']))
        satir['en_iyi'] = en
        out.append(satir)
    return dict(sehir=klasor.name, trafolar=out)


def ozet(satirlar, ad, sec):
    """sec(satır) → ölçüm adı ya da None."""
    n = yes = yy = bay = bay_d = ev = 0
    for s in satirlar:
        o = sec(s)
        if o is None:
            continue
        x = s['olcum'][o]
        n += 1
        yes += x['uc'] == 'yesil'
        yy += x['uc'] == 'yesil' and s['dolu']
        bay += x['uc'] == 'dolu_bayrak'
        bay_d += x['uc'] == 'dolu_bayrak' and s['dolu']
        ev += x['ev']
    print(f'{ad} | {n} | {yes} | {yy}/{yes} | {bay} ({bay_d} dolu) | {ev}')
    return dict(n=n, yesil=yes, yanlis_yesil=yy, bayrak=bay, bayrak_dolu=bay_d, ev=ev)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('kok')
    ap.add_argument('--aralik', default='1-10')
    ap.add_argument('--kalibrasyon', action='store_true', help='GECE_HATA_Q yaz (yalnız 1–10)')
    ap.add_argument('--json')
    a = ap.parse_args()
    bas, son = (int(x) for x in a.aralik.split('-'))
    klasorler = [str(Path(a.kok) / f'sehir-{t:03d}') for t in range(bas, son + 1)]
    if not a.kalibrasyon and not GECE_HATA_Q:
        sys.exit('GECE_HATA_Q boş: önce 1–10 --kalibrasyon.')
    with ProcessPoolExecutor() as ex:
        sonuc = list(ex.map(sehir_isle, [(k, a.kalibrasyon) for k in klasorler]))
    if a.kalibrasyon:
        e = sorted(x for s in sonuc for _, x in s['gece_hata'])
        q = [round(ko.nicel(e, k / 20), 2) for k in range(21)]
        print(f'gece prizi hatası (ölçüm − v0), şehir {a.aralik}, {len(e)} trafo: ortanca {st.median(e):+.2f} V, '
              f'P10–P90 {ko.nicel(e, .1):+.2f} … {ko.nicel(e, .9):+.2f} V')
        print(f'GECE_HATA_Q = {q}')
        gruplar = {}
        for s_ in sonuc:
            for g_, x in s_['gece_hata']:
                gruplar.setdefault(g_, []).append(x)
        ort = st.median(e)
        tablo_g = {}
        for g_, xs in sorted(gruplar.items()):
            xs.sort()
            if len(xs) >= KUCUK_GRUP:
                tablo_g[g_] = [round(ko.nicel(xs, k / 20), 2) for k in range(21)]
                yol = 'kendi nicelikleri'
            else:
                kay = st.median(xs) - ort
                tablo_g[g_] = [round(v + kay, 2) for v in q]
                yol = f'havuz {kay:+.2f} V kaydırıldı'
            print(f'  {g_}: n {len(xs)}, ortanca {st.median(xs):+.2f} V, P10–P90 {ko.nicel(xs, .1):+.2f} … '
                  f'{ko.nicel(xs, .9):+.2f} V ({yol})')
        print(f'GECE_HATA_GRUP = {tablo_g}')
        return
    satirlar = [s for x in sonuc for s in x['trafolar']]
    print(f'şehir {a.aralik} — Faz 10 ölçüm sırası, renksiz trafolar (aday evi olan) {len(satirlar)}; farazi, gösterim')
    print('ölçüm sonrası (gerçek sonuçla): seçim | trafo | yeşile dönen | yanlış yeşil | bayrağa dönen | açılan ev (karamsar)')
    tablo = {o: ozet(satirlar, f'hepsine {o}', lambda s, o=o: o) for o in OLCUMLER}
    tablo['en_iyi'] = ozet(satirlar, 'her trafoya kendi en iyi ölçümü (beklenen)', lambda s: s['en_iyi'])
    sira = sorted(satirlar, key=lambda s: (-s['olcum'][s['en_iyi']]['beklenen_ev'], -s['olcum'][s['en_iyi']]['p_bayrak']))
    ilk = {(s['sehir'], s['trafo_no']) for s in sira[:20]}
    tablo['ilk20'] = ozet(satirlar, 'ilk 20 (beklenen değere göre)', lambda s: s['en_iyi'] if (s['sehir'], s['trafo_no']) in ilk else None)
    n = len(satirlar)
    r_ev = tablo['en_iyi']['ev'] * 20 / n if n else 0
    r_y = tablo['en_iyi']['yesil'] * 20 / n if n else 0
    print(f'rastgele 20 renksiz trafo (kendi en iyi ölçümüyle, ortalama): yeşile dönen {r_y:.1f}, açılan ev {r_ev:.1f}')
    print('beklenen ↔ gerçekleşen (bütün renksiz trafolar): ' + '; '.join(
        f"{o} yeşil {sum(s['olcum'][o]['p_yesil'] for s in satirlar):.1f} → {sum(s['olcum'][o]['uc'] == 'yesil' for s in satirlar)}, "
        f"ev {sum(s['olcum'][o]['beklenen_ev'] for s in satirlar):.0f} → {sum(s['olcum'][o]['ev'] for s in satirlar)}"
        for o in OLCUMLER))
    gruplar = sorted({s['grup'] for s in satirlar})
    print('gece prizi, tarife grubuna göre (beklenen → gerçekleşen yeşil): ' + ', '.join(
        f"{g_} {sum(s['olcum']['gece']['p_yesil'] for s in satirlar if s['grup'] == g_):.1f} → "
        f"{sum(s['olcum']['gece']['uc'] == 'yesil' for s in satirlar if s['grup'] == g_)} (n {sum(s['grup'] == g_ for s in satirlar)})"
        for g_ in gruplar))
    faydali = [s for s in satirlar if s['olcum'][s['en_iyi']]['beklenen_ev'] > 0 or s['olcum'][s['en_iyi']]['p_bayrak'] > 0]
    print(f'tek ölçümün renk değiştirebileceği {len(faydali)} trafoda en iyi ölçüm: '
          + ', '.join(f"{o} {sum(s['en_iyi'] == o for s in faydali)}" for o in OLCUMLER)
          + f'; kalan {len(satirlar) - len(faydali)} trafoda hiçbir tek ölçüm rengi beklenen olarak değiştirmiyor (öneri yok)')
    print('\nilk 20: şehir trafo | güven | ölçüm | P(yeşil) | P(bayrak) | beklenen ev → gerçekleşen renk, ev | gerçekte dolu')
    for s in sira[:20]:
        x = s['olcum'][s['en_iyi']]
        print(f"  {s['sehir']} {s['trafo_no']} | {s['guven']} | {s['en_iyi']} | {x['p_yesil']:.2f} | {x['p_bayrak']:.2f} | "
              f"{x['beklenen_ev']:.1f} → {x['uc']}, {x['ev']} | {'evet' if s['dolu'] else 'hayır'}")
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(dict(aralik=a.aralik, K=K, tablo=tablo, trafolar=satirlar), fh, ensure_ascii=False)


if __name__ == '__main__':
    main()
