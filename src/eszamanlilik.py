#!/usr/bin/env python3
"""Eşzamanlılık ve tepe–sıcaklık eğimi: 20 Kıbrıs konut prosumer'ı, 2016 (Faz 11, B-Y2 girdisi; KARAR 23:02 m. 2–3,
23:18, 1 Kasım 00:15).

Veri: Zenodo 23043383 (CC BY 4.0), 20 ev, 30 dk, import / export / üretim / tüketim; Lefkoşa saatlik sıcaklık
(Open-Meteo, 2015–2025 dosyasının 2016'sı). KAYNAK.txt'ler data/raw/kibris-20-prosumer/ ve data/raw/open-meteo-lefkosa/.
Birim: sütun başlıkları "kWh" diyor ama değerler 30 dakikalık ortalama güç (W): PV tepesi 2,3–3,0 bin, 2016 Kıbrıs net
ölçüm şemasının 3 kWp sınırıyla tutuyor; kWh olsaydı 3 kWp'lik panel yarım saatte 5,4 kWh üretirdi [Yorum]. kW = değer ÷ 1000.
Ev 4: tüketim sütunu #REF!, export bütün yıl sabit 592 → net = import (export bilinmiyor; akşam tepesinde export 0),
brüt hesaplarına girmez. Ev 15: sondaki boş satırlar atlanır. Yaz saatine geçişin tekrar eden 4 zaman damgası
ortalanır.

Ölçüler (net = import − export; trafoya binen yük; brüt = tüketim yanında bilgi):
  1 Tepe saati: her evin yılın net (ve brüt) tepesinin ayı ve saati (tepe anı saate kilitlenmez; can → civan 23:08 m. 1).
  2 Eşzamanlılık: N = 1…20 ev rastgele altkümeler (CEKILIS), gün kümesi içinde tepe (saat serbest):
    P(N) = max_t Σ x_i(t); ev başına P(N) ÷ N ve CF(N) = P(N) ÷ Σ max_t x_i(t). Gün kümeleri: sıcak akşam (19–22
    ortalaması ≥ yılın SICAK_NICEL'i) ve diğer günler. tepe.py biçimine uydurma (ADR-0018 m. 5, Velander):
    P(N) ÷ N = a × (1 + c ÷ √N), en küçük kareler; a = sonsuz çeşitlilikte ev başına tepe payı.
  3 İki bileşen (KARAR 23:18): sıcak günde P(N)/N = a_taban (1 + c_taban/√N) + k_klima; c_taban diğer günlerden (√N
    çeşitlilik), k_klima N'den bağımsız (hava herkese aynı anda vurur). Uydurmanın artığı klimanın ~doğrusal olup
    olmadığını söyler.
  4 Sıcaklık eğimi: 20 evin akşam (17–24) toplam net tepesi ÷ ev, yaz (Haziran–Eylül) günlerinde, o akşamın 19–22
    ortalama sıcaklığına parçalı doğrusal (eşik T0 ızgarada); eğim kW/°C/ev ve diğer günlerin tepesine göre °C başına
    göreli; belirsizlik evler üzerinden bootstrap (BOOT).
  5 Tasarım akşamı: Lefkoşa 2015–2025'te yılın en sıcak akşamı (19–22), 11 yılın TASARIM_NICEL'i (10 yılda bir [Yorum]).

Çalıştırma:
  python3 src/eszamanlilik.py                     # tablolar ekrana
  python3 src/eszamanlilik.py --cikti ozet.json   # ayrıca özet JSON (tepe.py'ye girecek sayılar)
"""
import argparse
import datetime as dt
import json
import random
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

KOK = Path(__file__).resolve().parent.parent
VERI = KOK / 'data' / 'raw' / 'kibris-20-prosumer' / 'kibris_20_prosumer_2016.xlsx'
SICAKLIK = KOK / 'data' / 'raw' / 'open-meteo-lefkosa' / 'lefkosa_sicaklik_2015_2025.csv'
YIL = 2016
EXPORT_BOZUK = {'4'}                 # export sabit 592, tüketim #REF!
SICAK_NICEL = 0.90                   # sıcak akşam: 19–22 ortalaması yılın P90'ı ve üstü [Yorum]
AKSAM_SAAT = range(19, 23)           # sıcaklığın akşam penceresi (19:00–22:59)
AKSAM_TEPE = range(17, 24)           # akşam tepesinin arandığı saatler
YAZ_AY = (6, 7, 8, 9)
CEKILIS = 300
BOOT = 500
TASARIM_NICEL = 0.9                  # tepe.py ile aynı
ADIM = 48                            # 30 dk


def evleri_oku(yol=VERI):
    """{ev: {'net': {zaman: kW}, 'brut': {zaman: kW} ya da None}}; yalnız değerler okunur (formül çalıştırılmaz)."""
    import openpyxl
    wb = openpyxl.load_workbook(yol, read_only=True, data_only=True)
    out = {}
    for ws in wb.worksheets:
        net, brut = defaultdict(list), defaultdict(list)
        for r in ws.iter_rows(min_row=2, values_only=True):
            z, imp, exp, _, con = r[:5]
            if z is None or not isinstance(imp, (int, float)):
                continue
            e = 0.0 if ws.title in EXPORT_BOZUK or not isinstance(exp, (int, float)) else exp
            net[z].append((imp - e) / 1000)
            if ws.title not in EXPORT_BOZUK and isinstance(con, (int, float)):
                brut[z].append(con / 1000)
        out[ws.title] = dict(net={z: st.fmean(v) for z, v in net.items()},
                             brut={z: st.fmean(v) for z, v in brut.items()} if brut else None)
    return out


def matris(evler, tur):
    """Ortak zaman ızgarası (2016, 30 dk, yerel) × ev; eksik yarım saat ev ortalamasıyla değil, satır atlanarak."""
    adlar = [a for a in evler if evler[a][tur]]
    zaman = sorted(set.intersection(*(set(evler[a][tur]) for a in adlar)))
    X = np.array([[evler[a][tur][z] for a in adlar] for z in zaman])
    return adlar, zaman, X


def sicaklik_oku(yol=SICAKLIK):
    """{tarih: {saat: °C}} (yerel saat, Europe/Nicosia)."""
    import csv
    with open(yol, encoding='utf-8', newline='') as fh:
        satir = list(csv.reader(fh))
    bas = next(i for i, r in enumerate(satir) if r and r[0] == 'time')
    out = defaultdict(dict)
    for r in satir[bas + 1:]:
        if r and r[1]:
            z = dt.datetime.fromisoformat(r[0])
            out[z.date()][z.hour] = float(r[1])
    return out


def aksam_sicakligi(T, gun):
    v = [T[gun][h] for h in AKSAM_SAAT if h in T.get(gun, {})]
    return st.fmean(v) if len(v) == len(AKSAM_SAAT) else None


def eszamanlilik(X, satir, rng):
    """N = 1…n için ev başına P(N)/N ve CF(N) ortalaması (CEKILIS rastgele altküme). satir: kullanılacak zaman satırları."""
    Y = X[satir]
    tek = Y.max(0)
    n = X.shape[1]
    out = {}
    for N in range(1, n + 1):
        pn, cf = [], []
        for _ in range(CEKILIS if N < n else 1):
            s = rng.sample(range(n), N)
            p = float(Y[:, s].sum(1).max())
            pn.append(p / N)
            cf.append(p / float(tek[s].sum()))
        out[N] = (st.fmean(pn), st.fmean(cf))
    return out


def velander(egri):
    """P(N)/N = a (1 + c/√N), en küçük kareler (x = 1/√N doğrusal): -> (a, c, artık RMS göreli)."""
    N = np.array(sorted(egri), float)
    y = np.array([egri[int(k)][0] for k in N])
    A = np.column_stack([np.ones_like(N), 1 / np.sqrt(N)])
    (a, ac), *_ = np.linalg.lstsq(A, y, rcond=None)
    tah = a + ac / np.sqrt(N)
    return float(a), float(ac / a), float(np.sqrt(np.mean(((y - tah) / y) ** 2)))


def iki_bilesen(sicak, c_taban):
    """Sıcak eğri P(N)/N = a_t (1 + c_taban/√N) + k: -> (a_t, k, artık RMS göreli)."""
    N = np.array(sorted(sicak), float)
    y = np.array([sicak[int(k)][0] for k in N])
    A = np.column_stack([1 + c_taban / np.sqrt(N), np.ones_like(N)])
    (a, k), *_ = np.linalg.lstsq(A, y, rcond=None)
    tah = A @ np.array([a, k])
    return float(a), float(k), float(np.sqrt(np.mean(((y - tah) / y) ** 2)))


def parcali(x, y, izgara):
    """y = b0 + k × max(0, x − T0); T0 ızgarada en küçük kareler. -> (T0, b0, k)."""
    x, y = np.asarray(x), np.asarray(y)
    en = None
    for T0 in izgara:
        A = np.column_stack([np.ones_like(x), np.maximum(0.0, x - T0)])
        (b0, k), res, *_ = np.linalg.lstsq(A, y, rcond=None)
        r = float(((A @ np.array([b0, k]) - y) ** 2).sum())
        if en is None or r < en[0]:
            en = (r, float(T0), float(b0), float(k))
    return en[1:]


def egim(X, zaman, T, rng):
    """Yaz akşamları: 20 evin akşam toplam tepesi ÷ ev ~ akşam sıcaklığı. Bootstrap evler üzerinden."""
    gunler = sorted({z.date() for z in zaman if z.month in YAZ_AY})
    gun_sat = defaultdict(list)
    for i, z in enumerate(zaman):
        if z.month in YAZ_AY and z.hour in AKSAM_TEPE:
            gun_sat[z.date()].append(i)
    xs = [aksam_sicakligi(T, g) for g in gunler]
    g_ok = [(g, x) for g, x in zip(gunler, xs) if x is not None and gun_sat[g]]
    izgara = np.arange(22.0, 32.01, 0.5)

    def uydur(evler):
        y = [float(X[gun_sat[g]][:, evler].sum(1).max()) / len(evler) for g, _ in g_ok]
        return parcali([x for _, x in g_ok], y, izgara)

    n = X.shape[1]
    T0, b0, k = uydur(list(range(n)))
    boot = [uydur([rng.randrange(n) for _ in range(n)]) for _ in range(BOOT)]
    kb = [b[2] for b in boot]
    # tepe.py'nin eğimiyle aynı ölçek: Temmuz ortalama akşamında tepeye göre °C başına (tepe.py egim[konut][yaz] ↔ bu)
    Tt = st.fmean(x for g, x in g_ok if g.month == 7)
    gt = lambda T0_, b0_, k_: k_ / (b0_ + k_ * max(0.0, Tt - T0_))      # noqa: E731
    gtb = [gt(*b) for b in boot]
    return dict(gun=len(g_ok), T0=T0, taban_kw=b0, k_kw_c=k, k_P10=float(np.quantile(kb, 0.1)),
                temmuz_aksam_c=Tt, temmuz_goreli=gt(T0, b0, k), temmuz_goreli_P10=float(np.quantile(gtb, 0.1)),
                temmuz_goreli_P90=float(np.quantile(gtb, 0.9)),
                k_P90=float(np.quantile(kb, 0.9)), goreli_c=k / b0, goreli_P10=float(np.quantile([b[2] / b[1] for b in boot], 0.1)),
                goreli_P90=float(np.quantile([b[2] / b[1] for b in boot], 0.9)),
                T0_P10=float(np.quantile([b[0] for b in boot], 0.1)), T0_P90=float(np.quantile([b[0] for b in boot], 0.9)))


def tasarim_aksami(T):
    yillik = defaultdict(list)
    for g in T:
        x = aksam_sicakligi(T, g)
        if x is not None:
            yillik[g.year].append(x)
    uc = [max(v) for y, v in sorted(yillik.items())]
    return dict(yil=len(uc), en_sicak_aksam_ortanca=float(st.median(uc)), tasarim=float(np.quantile(uc, TASARIM_NICEL)),
                y2016=max(yillik[2016]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--cikti', help='özet JSON')
    a = ap.parse_args()
    rng = random.Random('eszamanlilik-2016')
    evler = evleri_oku()
    T = sicaklik_oku()
    ozet = {}

    print('== 1. Yılın tepesi: ay ve saat (ev başına)')
    for tur in ('net', 'brut'):
        adlar, zaman, X = matris(evler, tur)
        tz = [zaman[int(X[:, j].argmax())] for j in range(X.shape[1])]
        ay = st.median(float(X[:, j].max()) for j in range(X.shape[1]))
        aksam = sum(17 <= z.hour or z.hour < 1 for z in tz)
        print(f'   {tur} (n = {len(adlar)}): tepe ortanca {ay:.2f} kW; akşam (17–01) {aksam}, gündüz {len(tz) - aksam}; '
              f'aylar {dict(sorted(Counter(z.month for z in tz).items()))}; saatler {sorted(z.strftime("%H:%M") for z in tz)}')
        ozet[f'tepe_{tur}'] = dict(n=len(adlar), ortanca_kw=round(ay, 2), aksam=aksam,
                                   ay={str(k): v for k, v in sorted(Counter(z.month for z in tz).items())})

    adlar, zaman, X = matris(evler, 'net')
    gunler = sorted({z.date() for z in zaman})
    ax = {g: aksam_sicakligi(T, g) for g in gunler}
    esik = float(np.quantile([v for v in ax.values() if v is not None], SICAK_NICEL))
    sicak_gun = {g for g, v in ax.items() if v is not None and v >= esik}
    s_sicak = np.array([z.date() in sicak_gun for z in zaman])
    print(f'\n== 2. Eşzamanlılık (net, n = {len(adlar)} ev; sıcak akşam: 19–22 ortalaması ≥ {esik:.1f} °C, '
          f'{len(sicak_gun)} gün, aylar {dict(sorted(Counter(g.month for g in sicak_gun).items()))})')
    eg = {'sicak': eszamanlilik(X, s_sicak, rng), 'diger': eszamanlilik(X, ~s_sicak, rng)}
    print('   N   | ev başına P(N)/N kW (sıcak / diğer) | CF (sıcak / diğer)')
    for N in (1, 2, 3, 5, 8, 10, 15, 20):
        print(f'   {N:<3} | {eg["sicak"][N][0]:.2f} / {eg["diger"][N][0]:.2f} | {eg["sicak"][N][1]:.2f} / {eg["diger"][N][1]:.2f}')
    vel = {k: velander(v) for k, v in eg.items()}
    for k, (va, vc, vr) in vel.items():
        print(f'   Velander {k}: a = {va:.2f} kW/ev, c = {vc:.2f}, artık RMS %{100 * vr:.1f}')
    a_t, k_kl, r2 = iki_bilesen(eg['sicak'], vel['diger'][1])
    print(f'\n== 3. İki bileşen (sıcak günde): taban a = {a_t:.2f} kW/ev × (1 + {vel["diger"][1]:.2f}/√N) + klima '
          f'{k_kl:.2f} kW/ev (N\'den bağımsız); artık RMS %{100 * r2:.1f} (tek Velander %{100 * vel["sicak"][2]:.1f}); '
          f'N = 20\'de klima payı %{100 * k_kl / eg["sicak"][20][0]:.0f}')
    ozet['eszamanlilik'] = dict(sicak_esik_c=round(esik, 1), sicak_gun=len(sicak_gun),
                                egri={k: {str(N): [round(p, 3), round(c, 3)] for N, (p, c) in v.items()} for k, v in eg.items()},
                                velander={k: dict(a_kw=round(va, 3), c=round(vc, 3), artik=round(vr, 4)) for k, (va, vc, vr) in vel.items()},
                                iki_bilesen=dict(a_taban_kw=round(a_t, 3), c_taban=round(vel['diger'][1], 3),
                                                 k_klima_kw=round(k_kl, 3), artik=round(r2, 4)))
    # brüt bilgi
    adb, zb, Xb = matris(evler, 'brut')
    sb = np.array([z.date() in sicak_gun for z in zb])
    vb = {k: velander(eszamanlilik(Xb, m, rng)) for k, m in (('sicak', sb), ('diger', ~sb))}
    print(f'   bilgi, brüt (n = {len(adb)}): c sıcak {vb["sicak"][1]:.2f}, diğer {vb["diger"][1]:.2f}; '
          f'a sıcak {vb["sicak"][0]:.2f}, diğer {vb["diger"][0]:.2f} kW/ev')
    ozet['eszamanlilik_brut'] = {k: dict(a_kw=round(va, 3), c=round(vc, 3)) for k, (va, vc, _) in vb.items()}

    e = egim(X, zaman, T, rng)
    print(f'\n== 4. Sıcaklık eğimi (net, yaz akşamları {e["gun"]} gün, 20 evin akşam toplam tepesi ÷ ev): eşik T0 '
          f'{e["T0"]:.1f} °C (P10–P90 {e["T0_P10"]:.1f}–{e["T0_P90"]:.1f}); eşik altı {e["taban_kw"]:.2f} kW/ev; '
          f'eşik üstü {e["k_kw_c"]:.3f} kW/°C/ev (P10–P90 {e["k_P10"]:.3f}–{e["k_P90"]:.3f}) = °C başına '
          f'%{100 * e["goreli_c"]:.1f} (P10–P90 %{100 * e["goreli_P10"]:.1f}–%{100 * e["goreli_P90"]:.1f}); Temmuz ortalama akşamında '
          f'({e["temmuz_aksam_c"]:.1f} °C) tepeye göre °C başına %{100 * e["temmuz_goreli"]:.1f} '
          f'(P10–P90 %{100 * e["temmuz_goreli_P10"]:.1f}–%{100 * e["temmuz_goreli_P90"]:.1f}; tepe.py egim ölçeği)')
    ozet['egim'] = {k: round(v, 4) for k, v in e.items()}

    t = tasarim_aksami(T)
    print(f'\n== 5. Tasarım akşamı (Lefkoşa {t["yil"]} yıl, yılın en sıcak 19–22 ortalaması): ortanca {t["en_sicak_aksam_ortanca"]:.1f} °C, '
          f'10 yılda bir ~{t["tasarim"]:.1f} °C; 2016 {t["y2016"]:.1f} °C. Eşik üstü fark (tasarım − T0) {t["tasarim"] - e["T0"]:.1f} °C → '
          f'akşam tepesi eşik altının ~{1 + e["goreli_c"] * max(0.0, t["tasarim"] - e["T0"]):.2f} katı (20 ev ortalaması)')
    ozet['tasarim'] = {k: round(v, 2) for k, v in t.items()}
    if a.cikti:
        with open(a.cikti, 'w', encoding='utf-8') as fh:
            json.dump(ozet, fh, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
