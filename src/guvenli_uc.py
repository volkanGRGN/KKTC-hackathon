#!/usr/bin/env python3
"""Panel katmanı "güvenli uçlar" ölçüsü (ADR-0017 madde 3; Muhittin 4 madde 1).

Üç durum `kac_ev.csv` `pv_uc`'den (`kac_ev_olasilik.pv_uc`): `yesil` (ilk 2 başvuru güvenle sığar), `dolu_bayrak`
(bugün aşma olasılığı ≥ 0,7: "büyük olasılıkla dolu"), `bos` (renksiz, "başvuruda bakılır"). Ölçüler, aday evi olan
trafolarda (ADR-0017 tablosu); dolu = cevap anahtarında `kac_ev_gercek` 0 (sınavın tanımı):
  (a) yanlış yeşil: yeşil ve dolu (kapı, ≤ %2);
  (b) bayrak isabeti: bayraklıların gerçekte dolu payı ≥ ort(p) − 2·√(ort(p)·(1 − ort(p)) ÷ n), ort(p) bayraklıların
      ortalama `p_bugun_asar`'ı, n bayraklı sayısı (ADR-0016 kırmızı kovası ölçüsünün bayrak sürümü);
  (c) bilgi: bayraklıların bugün 259 V'u aşan payı (`v_max_bugun_v`), bayrağın yakaladığı dolu payı, renksiz pay.
Sınav maddesi Can'ın (`sinav.py faz3`, 3b); bu betik BUILD 2'nin geliştirme ölçüsü. Eşik değişirse yalnız 1–10'da.

`--kayitli <düzey>`: aynı ölçü sahte Kıb-Tek kayıtlarıyla (harita kayıtlı görünüm): renk ve bugün aşma olasılığı
`basvuru.harita_rengi`'den, `basvuru_testi.py`'nin tohumlarıyla (renkler o tablonun aynısı). PR #22 kodu
(`basvuru.py`, `sahte_kayit.py`) gerekir. Etiket: farazi şehir, gösterim.

`--konum`: konum payı analizi (ADR-0015 m. 4; `kac_ev_olasilik.konum_payi`, `kac_ev.csv`'ye yazılmaz — karar masası
01:01): payı > 0 olan trafolarda hattın ilk x'indeki her panelsiz konutun tek başvurusu (6,5 kW) gerçek ağda kritik
anlarda sığıyor mu (`sahte_kayit.gercekte_asar`, cevap anahtarının tanımı). Ölçü: konum payı yanlış evet (kapı ≤ %2),
bilgi verilen başvuru payı. PR #22 kodu gerekir.

Çalıştırma:
  python3 src/guvenli_uc.py data/synthetic/u13 --aralik 1-10
  python3 src/guvenli_uc.py data/synthetic/u13 --aralik 1-10 --konum
  python3 src/guvenli_uc.py data/synthetic/u13 --aralik 1-10 --kayitli aynen,iki_kat
"""
import argparse
import csv
import math
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

_argv, sys.argv = sys.argv, sys.argv[:1]
import kac_ev as ke  # noqa: E402
import kac_ev_olasilik as ko  # noqa: E402
sys.argv = _argv


def _csv(yol):
    with open(yol, encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


def resmi(klasor):
    """Resmi hesabın üç durumu: [(trafo_no, pv_uc, p_bugun_asar, renk)]."""
    return [(r['trafo_no'], r['pv_uc'], float(r['p_bugun_asar']), r['renk']) for r in _csv(klasor / 'kac_ev.csv')]


def kayitli(is_):
    """Sahte kayıtlı görünüm (PR #22): basvuru_testi.sehir_senaryo ile aynı tohumlar."""
    klasor, duzey = Path(is_[0]), is_[1]
    try:
        import basvuru as bv
        import sahte_kayit as sk
    except ImportError:
        sys.exit('--kayitli için PR #22 kodu (src/basvuru.py, src/sahte_kayit.py) gerekir.')
    sehir = sk.gercek_sehir(klasor)
    tohum = sehir['tohum']
    tahmin = {r['trafo_no']: r for r in _csv(klasor / 'tahmin.csv')}
    hp_veri = sk.hata_payi(duzey)
    hp_model = sk.hata_payi('kusursuz' if duzey == 'kusursuz' else bv.VARSAYILAN_HATA)
    out = []
    for r in _csv(klasor / 'trafolar.csv'):
        no = r['trafo_no']
        tr = {k: (r[k] if k in ('trafo_no', 'kablo', 'bolge', 'montaj') else ke.sayi(r[k])) for k in r}
        gtr = sk.gercek_trafo(sehir, no)['tr']
        kayit = sk.kayit_uret(gtr, hp_veri, random.Random(f'kayit-{duzey}-{tohum}-{no}'))
        renk, p_bugun, _ = bv.harita_rengi(tr, tahmin[no], kayit, random.Random(f'harita-{duzey}-{tohum}-{no}'),
                                           hp_model)
        out.append((no, ko.pv_uc(renk, p_bugun), p_bugun, renk))
    return out


def konum_dogrula(klasor):
    """Bir şehir: [(trafo_no, pv_uc, konum payı, aday sayısı, [(yer, gerçekte aşar mı) payın içindeki adaylar])]."""
    try:
        import sahte_kayit as sk
    except ImportError:
        sys.exit('--konum için PR #22 kodu (src/sahte_kayit.py) gerekir.')
    klasor = Path(klasor)
    sehir = sk.gercek_sehir(klasor)
    trafolar = {r['trafo_no']: r for r in _csv(klasor / 'trafolar.csv')}
    tahmin = {r['trafo_no']: r for r in _csv(klasor / 'tahmin.csv')}
    out = []
    for r in _csv(klasor / 'kac_ev.csv'):
        tr = {k: (v if k in ('trafo_no', 'kablo', 'bolge', 'montaj') else ke.sayi(v)) for k, v in trafolar[r['trafo_no']].items()}
        x = 0.0 if float(r['p_bugun_asar']) > 1 - ko.YESIL_P else ko.konum_payi(     # haritayla çelişmesin
            tr, tahmin[r['trafo_no']], random.Random(f'konum-{trafolar[r["trafo_no"]]["sehir"]}-{r["trafo_no"]}'))
        gtr = sehir['trafolar'][r['trafo_no']]
        ad = sk.adaylar(gtr)
        icinde = []
        if x > 0 and ad:
            gt = sk.gercek_trafo(sehir, r['trafo_no'])
            yer = sk.ev_yeri(gtr)
            for hid in ad:
                j, k, n = yer[hid]
                if (k + 1) / n <= x + 1e-9:
                    icinde.append(((k + 1) / n, sk.gercekte_asar(sehir, gt, {hid: ke.YENI_PANEL_KW})))
        out.append((r['trafo_no'], r['pv_uc'], x, len(ad), icinde))
    return out


def konum_yaz(klasorler):
    with ProcessPoolExecutor() as ex:
        sonuc = list(ex.map(konum_dogrula, [str(k) for k in klasorler]))
    print('\nkonum payı (ADR-0015 m. 4) — gerçek ağda tek başvuru: durum | trafo | payı > 0 | pay ortancası | '
          'payın içindeki aday / tüm aday | yanlış evet (gerçekte aşan) | yanlış evetli trafo')
    for uc in ('bos', 'yesil', 'dolu_bayrak', 'hepsi'):
        satir = [x for s in sonuc for x in s if uc == 'hepsi' or x[1] == uc]
        pozitif = [x for x in satir if x[2] > 0]
        icinde = [a for x in pozitif for a in x[4]]
        yanlis = sum(a[1] for a in icinde)
        tr_y = sum(1 for x in pozitif if any(a[1] for a in x[4]))
        tum = sum(x[3] for x in satir)
        orta = sorted(x[2] for x in pozitif)[len(pozitif) // 2] if pozitif else float('nan')
        print(f'{uc} | {len(satir)} | {len(pozitif)} | {orta:.1f} | {yuzde(len(icinde), tum)} | '
              f'{yuzde(yanlis, len(icinde))} | {tr_y}/{len(pozitif)}')


def olc(klasorler, durumlar):
    """durumlar: {klasör adı: [(trafo_no, pv_uc, p_bugun, renk)]}."""
    n = dolu = yesil = yy = bayrak = b_dolu = b_asan = bos = kir = k_dolu = 0
    b_p = 0.0
    for k in klasorler:
        cevap = {r['trafo_no']: r for r in _csv(k / 'cevap_anahtari.csv')}
        for no, uc, p, renk in durumlar[k.name]:
            c = cevap[no]
            if int(c['kac_ev_aday']) <= 0:
                continue
            d = int(c['kac_ev_gercek']) == 0
            n += 1
            dolu += d
            kir += renk == 'kirmizi'
            k_dolu += renk == 'kirmizi' and d
            if uc == 'yesil':
                yesil += 1
                yy += d
            elif uc == 'dolu_bayrak':
                bayrak += 1
                b_dolu += d
                b_asan += float(c['v_max_bugun_v']) > ke.V_SINIR
                b_p += p
            else:
                bos += 1
    ort_p = b_p / bayrak if bayrak else float('nan')
    esik = ort_p - 2 * math.sqrt(ort_p * (1 - ort_p) / bayrak) if bayrak else float('nan')
    return dict(n=n, dolu=dolu, yesil=yesil, yanlis_yesil=yy, bayrak=bayrak, bayrak_dolu=b_dolu,
                bayrak_bugun_asan=b_asan, bayrak_ort_p=ort_p, bayrak_esik=esik,
                bayrak_gecer=bool(bayrak) and b_dolu / bayrak >= esik, bos=bos, kirmizi=kir, kirmizi_dolu=k_dolu)


def yuzde(a, b):
    return f'%{100 * a / b:.1f} ({a}/{b})' if b else '— (0/0)'


def yaz(ad, o):
    print(f"{ad} | {o['n']} | {o['dolu']} | {o['yesil']} | {o['yanlis_yesil']}/{o['yesil']} | {o['bayrak']} | "
          f"{yuzde(o['bayrak_dolu'], o['bayrak'])} | ≥ %{100 * o['bayrak_esik']:.0f} (ort p {o['bayrak_ort_p']:.2f}) "
          f"{'GEÇER' if o['bayrak_gecer'] else 'KALIR'} | {yuzde(o['bayrak_bugun_asan'], o['bayrak'])} | "
          f"{yuzde(o['bayrak_dolu'], o['dolu'])} | {yuzde(o['bos'], o['n'])} | {yuzde(o['kirmizi_dolu'], o['kirmizi'])}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('kok')
    ap.add_argument('--aralik', default='1-10')
    ap.add_argument('--kayitli', help='virgülle: yari, aynen, iki_kat, kusursuz (PR #22 kodu gerekir)')
    ap.add_argument('--konum', action='store_true', help='konum payı doğrulaması (PR #22 kodu gerekir)')
    a = ap.parse_args()
    bas, son = (int(x) for x in a.aralik.split('-'))
    klasorler = [Path(a.kok) / f'sehir-{t:03d}' for t in range(bas, son + 1)]
    print(f'şehir {a.aralik} — panel katmanı güvenli uçlar (ADR-0017), aday evi olan trafolar; farazi, gösterim')
    print('görünüm | trafo | dolu | yeşil | yanlış yeşil | bayrak | bayrak isabeti (gerçekte dolu) | ölçü | '
          'bayrak bugün aşan | bayrağın yakaladığı dolu | renksiz | (eski kırmızı: gerçekte dolu)')
    yaz('resmi (kayıtsız)', olc(klasorler, {k.name: resmi(k) for k in klasorler}))
    if a.kayitli:
        duzeyler = a.kayitli.split(',')
        with ProcessPoolExecutor() as ex:
            sonuc = list(ex.map(kayitli, [(str(k), d) for d in duzeyler for k in klasorler]))
        for i, d in enumerate(duzeyler):
            parca = sonuc[i * len(klasorler):(i + 1) * len(klasorler)]
            yaz(f'sahte kayıt, {d}', olc(klasorler, {k.name: s for k, s in zip(klasorler, parca)}))
    if a.konum:
        konum_yaz(klasorler)


if __name__ == '__main__':
    main()
