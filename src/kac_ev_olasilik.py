#!/usr/bin/env python3
"""Kaç ev, olasılıklı (Faz 3 denemesi): bilinmeyenler aralıktan çekilir, ev ev benzetim her çekilişte koşar.

Tek denklemli `kac_ev.py` bilmediği her şey için tek bir "en kötü" değer seçer; Faz 3 varsayım envanteri
(docs/log/2026-10-31-volkan-faz3-varsayimlar.md) bu değerlerin kırmızıyı yalnız kaydırdığını, sıralamayı
düzeltmediğini gösterdi. Burada her trafo için ağ, Kıb-Tek'in bildikleriyle (abone sayıları, hat sayısı ve
boyu, kablo, kVA, panel sayısı ve gücü) yeniden kurulur; bilinmeyenler her çekilişte aralığından çekilir ve
eski benzetimin `solve()`'u koşar:
  - bara gerilimi, öğlen orta gerilim değişimi, abonelerin hattı ve sırası, fazı, panellerin hangi evde
    olduğu, trafonun öğlen yükü (Faz 2 bandından) ve abonelere dağılımı.
Aralıklar ölçümden ya da envanterdeki gerçek veri karşılaştırmasından; şehir üreticisinin kendi değerlerinden
değil (ADR-0009). Bu yüzden üreticiyle bilerek aynı değil: paneller çekilişlerin üçte birinde hattın ucuna
toplanır (UKPN: 6 hattın 2'si), yoksa düz; büyük aboneler yarı yarıya trafoya yakın ya da rastgele (veri yok);
OG değişimi UKPN ile eski benzetim arası.

Çıktı her çekilişte: bugün (yeni panelsiz, öğlen güneşi + en düşük yük) sınır aşılıyor mu; bekleyen panelsiz
konutlar rastgele sırayla 6,5 kW alırsa kaçı sığar (sığmayan atlanır, cevap anahtarıyla aynı tanım); ilk iki
başvuru sığıyor mu. Renk (ADR-0010 olasılıkla):
  kırmızı = bugün aşma olasılığı ≥ KIRMIZI_P;  yeşil = ilk iki başvurunun sığma olasılığı ≥ YESIL_P ve güven
  yüksek (marj = 1 ev);  diğerleri sarı.
Sayılar: kac_ev_karamsar = çekilişlerin P10'u, kac_ev_iyimser = P90'ı, kac_ev_orta = ortanca.

Okur: trafolar.csv, tahmin.csv. cevap_anahtari.csv'yi okumaz.
Yazar: kac_ev_olasilik.csv (deneme; sözleşmede değil).

Çalıştırma:
  python3 src/kac_ev_olasilik.py data/synthetic --sehir 3
  python3 src/kac_ev_olasilik.py data/synthetic           # 20 şehir, ~birkaç dakika
"""
import argparse
import csv
import math
import random
import sys
from pathlib import Path

_argv, sys.argv = sys.argv, sys.argv[:1]
import trafo_bos_kapasite as tb  # noqa: E402
sys.argv = _argv
import kac_ev as ke  # noqa: E402

KOK = Path(__file__).resolve().parent.parent
CEKILIS = 40
KIRMIZI_P = 0.5                         # bugün aşma olasılığı bunun üstündeyse kırmızı [Yorum]
YESIL_P = 0.98                          # ilk iki başvurunun sığma olasılığı (canlı bütçe %2, ADR-0010)

ABONE = ['abone_konut', 'abone_ticari1', 'abone_ticari2', 'abone_turizm', 'abone_sanayi1', 'abone_sanayi2',
         'abone_su_motoru']
# Abone başına yıllık MWh (Kıb-Tek 2023, sablon.py ile aynı kaynak): yalnız trafonun yükünü abonelere bölmek için.
MWH = {'abone_konut': 648494 / 175577, 'abone_ticari1': 210978 / 20950, 'abone_ticari2': 169496 / 494,
       'abone_turizm': 215147 / 171, 'abone_sanayi1': 22391 / 1227, 'abone_sanayi2': 95996 / 352,
       'abone_su_motoru': 51256 / 3250}

# Aralıklar (Faz 3 varsayım envanteri)
V0 = (244.0, 252.0)                     # bara gerilimi, düz [karar masası 16:27 bandı; Kıbrıs BULAMADIM]
OG = (-0.004, 0.008)                    # öğlen OG değişimi: UKPN −%0,4 (öğlen bara geceden ~1 V düşük) ile eski
#                                         benzetimin +%0,8'i arası [Yorum]
FAZ_SAPMA = {'kentsel': 0.30, 'turistik': 0.30, 'sanayi': 0.30, 'kirsal': 0.50}  # tek fazlı faz ağırlığı 1 ± U(0, x):
#                                         UKPN dengesizlik kentsel P84 %30, kırsal ~%50 [Hesap, PR #11]
UC_FAZ = {'abone_konut': (0.0, 0.2), 'abone_ticari1': (0.0, 0.4)}   # üç fazlı abone payı; diğerleri üç faz [Yorum]
PANEL_UCTA_P = 2 / 6                    # paneller hattın ucuna toplanmış [Hesap: UKPN 6 hat ucu evden 2'si, PR #11]
BUYUK_BASTA_P = 0.5                     # büyük aboneler trafoya yakın [Yorum: veri yok, iki durum eşit]
BUYUK = {'abone_ticari2', 'abone_turizm', 'abone_sanayi2'}
BIREY_SIGMA = 0.3                       # abone yükünün ortalamadan farkı, log-normal [Yorum]
Q_ORAN = 0.33                           # yükün reaktif gücü (benzetimle aynı)


def ag_kur(tr, rng):
    """Bir çekiliş: trafo sözlüğü (solve için) + ev listesi (sınıf, panel)."""
    kva = tr['kva']
    zb = 240.0 ** 2 / (kva * 1000 / 3)
    rt = 0.04 * zb / math.sqrt(5)
    n_hat = max(1, int(tr['hat_sayisi']))
    lmax = tr['hat_boyu_max_m']
    kalan = max(0.0, tr['hat_boyu_toplam_m'] - lmax)
    boylar = [lmax]
    if n_hat > 1:
        w = [rng.random() + 0.1 for _ in range(n_hat - 1)]
        boylar += [min(lmax, max(20.0, kalan * x / sum(w))) for x in w]
    aboneler = [c for c in ABONE for _ in range(int(tr[c]))]
    rng.shuffle(aboneler)
    hatlar = [[] for _ in boylar]
    for c in aboneler:
        hatlar[rng.randrange(n_hat)].append(c)
    if rng.random() < BUYUK_BASTA_P:
        for hat in hatlar:
            hat.sort(key=lambda c: c not in BUYUK)
    d = rng.uniform(0, FAZ_SAPMA.get(tr['bolge'], 0.3))
    fw = [1 + rng.uniform(-d, d) for _ in range(3)]
    uc = {c: rng.uniform(*UC_FAZ[c]) for c in UC_FAZ}
    zc, znc = tb.CABLES[tr['kablo']]
    ag = dict(v0=rng.uniform(*V0), zt=complex(rt, 2 * rt), kva=kva, feeders=[])
    evler = []
    for boy, hat in zip(boylar, hatlar):
        if not hat:
            continue
        seg = boy / 1000 / len(hat)
        f = dict(zs=zc * seg, zn=znc * seg, houses=[])
        for k, c in enumerate(hat):
            uc_faz = rng.random() < uc.get(c, 1.0)
            h = dict(id=len(evler), sinif=c, ph=3 if uc_faz else rng.choices([0, 1, 2], weights=fw)[0], pv=0.0,
                     yer=(k + 1) / len(hat))
            f['houses'].append(h)
            evler.append(h)
        ag['feeders'].append(f)
    konut = [h for h in evler if h['sinif'] == 'abone_konut']
    n_panel = min(int(tr['panel_sayisi']), len(konut))
    if n_panel:
        if rng.random() < PANEL_UCTA_P:          # uca toplanmış: hat üstündeki yerin karesiyle ağırlıklı çekiliş
            havuz, secilen = konut[:], []
            for _ in range(n_panel):
                h = rng.choices(havuz, weights=[x['yer'] ** 2 for x in havuz])[0]
                havuz.remove(h)
                secilen.append(h)
        else:
            secilen = rng.sample(konut, n_panel)
        for h in secilen:
            h['pv'] = tr['panel_kw'] / n_panel
    return ag, evler


def yuk_dagit(evler, toplam, rng):
    """Trafonun öğlen yükünü abonelere: tarife enerjisi × kişisel fark, toplamı korunur."""
    w = [MWH[h['sinif']] * rng.lognormvariate(-BIREY_SIGMA ** 2 / 2, BIREY_SIGMA) for h in evler]
    s = sum(w) or 1.0
    return {h['id']: toplam * x / s for h, x in zip(evler, w)}


def durum(ag, evler, yuk, ek, m, warm=None, iters=6):
    gunes = ke.GUNES_KW_KWP
    net = {h['id']: ((yuk[h['id']] - (h['pv'] + ek.get(h['id'], 0.0)) * gunes) * 1000,
                     yuk[h['id']] * Q_ORAN * 1000) for h in evler}
    V, s_tr = tb.solve(ag, net, m, warm, iters=iters)
    return V, max(tb.house_voltages(ag, V).values()), s_tr


def trafo_cek(tr, t, rng):
    """Bir trafo için CEKILIS kez: (bugün aşar mı, kaç ev, ilk iki sığar mı) listesi."""
    p10, p90 = ke.sayi(t['ogle_min_kw_p10']), ke.sayi(t['ogle_min_kw_p90'])
    olculen = ke.sayi(t['ogle_min_kw_olculen'])
    sonuc = []
    for _ in range(CEKILIS):
        ag, evler = ag_kur(tr, rng)
        if not evler:
            sonuc.append((False, 0, True))
            continue
        if t['olculdu'] == '1' and not math.isnan(olculen):
            toplam = olculen
        else:
            mu = (math.log(max(p10, 0.01)) + math.log(max(p90, 0.01))) / 2
            sd = max(1e-6, (math.log(max(p90, 0.01)) - math.log(max(p10, 0.01))) / (2 * 1.2816))
            toplam = math.exp(rng.gauss(mu, sd))
        yuk = yuk_dagit(evler, toplam, rng)
        m = 1 + rng.uniform(*OG)
        V, vmax, s_tr = durum(ag, evler, yuk, {}, m)
        bugun = vmax > ke.V_SINIR or s_tr > ag['kva']
        adaylar = [h['id'] for h in evler if h['sinif'] == 'abone_konut' and h['pv'] == 0]
        if not adaylar:                       # başvuru ticari aboneden de gelebilir: renk için sanal aday
            adaylar = [h['id'] for h in evler if h['pv'] == 0]
        rng.shuffle(adaylar)
        ek, kabul, ilk_iki = {}, 0, not bugun
        if not bugun:
            for j, hid in enumerate(adaylar):
                ek[hid] = ke.YENI_PANEL_KW
                V2, vmax2, s2 = durum(ag, evler, yuk, ek, m, [[list(v) for v in hat] for hat in V], iters=4)
                if vmax2 > ke.V_SINIR or s2 > ag['kva']:
                    del ek[hid]
                    if j < 2:
                        ilk_iki = False
                else:
                    kabul += 1
                    V = V2
        sonuc.append((bugun, kabul, ilk_iki))
    return sonuc


def nicel(x, q):
    x = sorted(x)
    return x[min(len(x) - 1, max(0, int(round(q * (len(x) - 1)))))]


def sehir_calistir(klasor):
    with open(klasor / 'trafolar.csv', encoding='utf-8', newline='') as fh:
        trafolar = list(csv.DictReader(fh))
    with open(klasor / 'tahmin.csv', encoding='utf-8', newline='') as fh:
        tahmin = {r['trafo_no']: r for r in csv.DictReader(fh)}
    satirlar = []
    for r in trafolar:
        tr = {k: (r[k] if k in ('trafo_no', 'kablo', 'bolge', 'montaj') else ke.sayi(r[k])) for k in r}
        t = tahmin[r['trafo_no']]
        rng = random.Random(f'olasilik-{r["sehir"]}-{r["trafo_no"]}')
        s = trafo_cek(tr, t, rng)
        aday = max(0, int(tr['abone_konut'] - tr['panel_sayisi']))
        p_bugun = sum(b for b, _, _ in s) / len(s)
        p_iki = sum(i for _, _, i in s) / len(s)
        kac = [min(k, aday) for _, k, _ in s]
        if p_bugun >= KIRMIZI_P:
            renk = 'kirmizi'
        elif p_iki >= YESIL_P and t['guven'] == 'yuksek':
            renk = 'yesil'
        else:
            renk = 'sari'
        satirlar.append(dict(sehir=int(tr['sehir']), trafo_no=r['trafo_no'], p_bugun_asar=round(p_bugun, 3),
                             p_iki_ev_sigar=round(p_iki, 3), kac_ev_karamsar=nicel(kac, 0.1),
                             kac_ev_orta=nicel(kac, 0.5), kac_ev_iyimser=nicel(kac, 0.9), renk=renk))
    sutunlar = list(satirlar[0])
    with open(klasor / 'kac_ev_olasilik.csv', 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=sutunlar, lineterminator='\n')
        w.writeheader()
        w.writerows(satirlar)
    return satirlar


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('kok', nargs='?', default=str(KOK / 'data' / 'synthetic'))
    ap.add_argument('--sehir', type=int, help='yalnız bu tohum')
    a = ap.parse_args()
    klasorler = sorted(k for k in Path(a.kok).glob('sehir-*')
                       if (k / 'trafolar.csv').exists() and (k / 'tahmin.csv').exists())
    if a.sehir is not None:
        klasorler = [k for k in klasorler if k.name == f'sehir-{a.sehir:03d}']
    for k in klasorler:
        s = sehir_calistir(k)
        renkler = {c: sum(1 for x in s if x['renk'] == c) for c in ('yesil', 'sari', 'kirmizi')}
        print(f'{k.name}: {renkler}')


if __name__ == '__main__':
    main()
