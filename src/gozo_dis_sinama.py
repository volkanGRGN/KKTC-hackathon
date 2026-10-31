#!/usr/bin/env python3
"""Gozo hattında dış sınama (Faz 7; karar masası 21:39 madde 2a): tek hat, gösterim.

Kaynak [Kaynaklı: Micallef & Weissenbacher, 14. Symposium Energieinnovation, Graz 2016, Tablo 3 ve metin]
Srug F1 hattı: trafo 500 kVA, 11 kV / 433 V (boşta faz ~250 V), elle kademe ±%5 (2,5 adım), yıllık 106.219 kWh,
panel 26,72 kWp; her panelsiz eve +1 kWp (44,72) ve +2 kWp (62,72). Makalenin sonuçları:
  S1 bugün, normal kademe (250 V): sınırda sorun yok (±%10, EN 50160)
  S2 +1 kWp, normal kademe: sorun var (bir kez kalıcı kademe değişikliği gerekti)
  S3 +1 kWp, bir adım aşağı (243,75 V): sorun yok
  S4 +2 kWp, en alt kademe (237,5 V): sorun var (trafo 433 → 400 V değişimi gerekti)
Bilinmeyenler aralıktan [Yorum]: hat boyu 150–600 m; kablo ABC70 / ABC95 (benzetim) ya da 50 / 100 mm² (Kotsonias
2019, Kıbrıs); panelli ev sayısı 9 (26,72 ÷ ~3 kWp; Malta konut paneli < 3,1 kWp), panelsiz 18 [Hesap: (44,72 − 26,72)
÷ 1]; öğlen en düşük yük 5–10 kW [Hesap: en yüksek anlık panel payı %304 → 26,72 × 0,82 ÷ 3,04 ≈ 7 kW]; faz ağırlığı
1 ± U(0, 0,3); panellerin yeri üçte bir çekilişte hattın ucunda (kac_ev_olasilik ile aynı); OG değişimi yok.
Sınır 253 V (230 V + %10, EN 50160; Malta 230 V). Model-sapma çarpanı s (Faz 7, İngiltere) isteğe bağlı.

Sonuç bir oran: makalenin dört sonucunun hepsini tutturan çekilişlerin payı ve her sonucun ayrı tutma payı.
Hat boyu ve kablo bilinmediği için tek tahmin değil, aralık; "tek hat, gösterim".

Çalıştırma:
  python3 src/gozo_dis_sinama.py            # v1 fizik (s yok) ve v2 (Faz 7 s) yan yana
"""
import math
import random
import sys

_argv, sys.argv = sys.argv, sys.argv[:1]
import trafo_bos_kapasite as tb  # noqa: E402
sys.argv = _argv

CEKILIS = 400
SINIR = 253.0
KADEME = {'normal': 433 / math.sqrt(3), 'bir_asagi': 433 / math.sqrt(3) * 0.975, 'en_alt': 433 / math.sqrt(3) * 0.95}
PANEL = {'bugun': 26.72, 'arti1': 44.72, 'arti2': 62.72}
N_PANELLI, N_PANELSIZ = 9, 18
GUNES = tb.PV_DERATE                     # kWp başına öğlen üretimi (benzetimle aynı)
KABLOLAR = dict(tb.CABLES)
KABLOLAR['Cu/Al 50 mm² (Kotsonias)'] = (complex(0.5419, 0.085), complex(0.69, 0.09))
KABLOLAR['Cu/Al 100 mm² (Kotsonias)'] = (complex(0.2702, 0.08), complex(0.69, 0.09))
SAPMA_MU, SAPMA_SIGMA = 0.172, 0.414     # Faz 7, İngiltere 6 hat
DOGRU = [('bugun', 'normal', False), ('arti1', 'normal', True), ('arti1', 'bir_asagi', False), ('arti2', 'en_alt', True)]


def cekilis(rng, sapma):
    boy = rng.uniform(150, 600)
    kablo = rng.choice(sorted(KABLOLAR))
    zc, znc = KABLOLAR[kablo]
    s = math.exp(rng.gauss(SAPMA_MU, SAPMA_SIGMA)) if sapma else 1.0
    n = N_PANELLI + N_PANELSIZ
    seg = boy / 1000 / n
    zb = 240.0 ** 2 / (500 * 1000 / 3)
    rt = 0.04 * zb / math.sqrt(5)
    d = rng.uniform(0, 0.3)
    fw = [1 + rng.uniform(-d, d) for _ in range(3)]
    evler = [dict(id=k, ph=rng.choices([0, 1, 2], weights=fw)[0], yer=(k + 1) / n) for k in range(n)]
    if rng.random() < 1 / 3:                       # paneller uca toplanmış
        havuz, panelli = evler[:], []
        for _ in range(N_PANELLI):
            h = rng.choices(havuz, weights=[x['yer'] ** 2 for x in havuz])[0]
            havuz.remove(h)
            panelli.append(h)
    else:
        panelli = rng.sample(evler, N_PANELLI)
    pid = {h['id'] for h in panelli}
    toplam_yuk = rng.uniform(5, 10)
    w = [rng.lognormvariate(-0.045, 0.3) for _ in evler]
    yuk = {h['id']: toplam_yuk * x / sum(w) for h, x in zip(evler, w)}
    ag = dict(zt=complex(rt, 2 * rt), kva=500, feeders=[dict(zs=zc * seg * s, zn=znc * seg * s, houses=evler)])
    sonuc = {}
    for pad, kwp in PANEL.items():
        ek = (kwp - PANEL['bugun']) / N_PANELSIZ
        pv = {h['id']: (PANEL['bugun'] / N_PANELLI if h['id'] in pid else ek) for h in evler}
        net = {i: ((yuk[i] - pv[i] * GUNES) * 1000, yuk[i] * 0.33 * 1000) for i in yuk}
        for kad, v0 in KADEME.items():
            ag['v0'] = v0
            V, _ = tb.solve(ag, net, 1.0, None, iters=8)
            sonuc[(pad, kad)] = max(tb.house_voltages(ag, V).values())
    return dict(boy=boy, kablo=kablo, s=s, v=sonuc)


def ozet(sapma, tohum=11):
    rng = random.Random(tohum)
    c = [cekilis(rng, sapma) for _ in range(CEKILIS)]
    tutar = [all((x['v'][(p, k)] > SINIR) == asim for p, k, asim in DOGRU) for x in c]
    print(f"\n== {'v2 (Faz 7 s ile)' if sapma else 'v1 fizik (s yok)'}: {CEKILIS} çekiliş ==")
    for p, k, asim in DOGRU:
        pay = sum((x['v'][(p, k)] > SINIR) == asim for x in c) / len(c)
        vs = sorted(x['v'][(p, k)] for x in c)
        print(f"  {p:6s} {k:9s} makale: {'aşım' if asim else 'sorun yok'} | tutan %{100 * pay:.0f} | en yüksek gerilim P10/50/90 "
              f"{vs[len(vs) // 10]:.1f} / {vs[len(vs) // 2]:.1f} / {vs[9 * len(vs) // 10]:.1f} V")
    print(f"  dördünü birden tutan: %{100 * sum(tutar) / len(c):.0f}")
    t = [x for x, ok in zip(c, tutar) if ok]
    if t:
        b = sorted(x['boy'] for x in t)
        print(f"  tutanlarda hat boyu P10–P90 {b[len(b) // 10]:.0f}–{b[9 * len(b) // 10]:.0f} m; kablolar: "
              + ', '.join(f"{k} {sum(x['kablo'] == k for x in t)}" for k in sorted(KABLOLAR)))
    return sum(tutar) / len(c)


if __name__ == '__main__':
    ozet(False)
    ozet(True)
