#!/usr/bin/env python3
"""Olasılıklı kaç ev hesabının (src/kac_ev_olasilik.py) gerilim tarafı, gerçek veride geri-test: İngiltere UKPN,
6 hat ucu ev, yaz 2014, 1 dk (ADR-0010 madde 3).

Soru: ölçülen PV kaynaklı yükselme (ΔV'nin evin birim üretimine eğimi, V/pu; UKPN'in tanımı), olasılıklı hesabın
çekiliş dağılımının neresinde? Yeşil kuralı "%98 güvenli" dediği için ölçülen, dağılımın P98'inin altında
kalmalı; üstündeyse hesap riski küçük görüyor (yanlış yeşil yönü).

Hat modeli src/ukpn_test.py'den (tek fider, 30 düğüm + uçta ev, bara ölçülen, boy akşam düşümünden). Çekilenler,
kac_ev_olasilik.py ile aynı aralıklar: panellerin hattaki yeri (üçte bir uca toplanmış [UKPN 2/6], yoksa düz),
faz (iki durum: faz ölçümü bilinen / Kıb-Tek gibi bilinmeyen, faz ağırlığı 1 ± U(0, 0,3)), hat boyu (BOY ortam
değişkeni: log-düz ±BOY; 0 = akşam kestirimi kesin). Fiderdeki PV payı, fider faz gücünün evin birim üretimine
eğiminden. Veriyi yalnız okur, dosya yazmaz.

Çalıştırma (sanal ortam; ~35 sn):
  BOY=0.47 python3 src/ukpn_olasilik.py data/raw/ukpn-pv-dogrulama
  BOY=0.47 CEKILIS_JSON=cekilis.json python3 src/ukpn_olasilik.py data/raw/ukpn-pv-dogrulama   # Faz 7: çekilişler
CEKILIS_JSON verilirse her sitenin (model eğimi ÷ ölçülen eğim) çekilişleri o dosyaya yazılır (src/kalibrasyon.py
ingiltere girdisi); verilmezse dosya yazılmaz.
"""
import sys, random
from pathlib import Path
veri = Path(sys.argv[1]); sys.argv = sys.argv[:1]
sys.path.insert(0, 'src')
import numpy as np, pandas as pd
import ukpn_test as ut
tb = ut.tb
CEKILIS, DAKIKA, PANEL_UCTA_P = 60, 300, 2 / 6
import os, math
BOY_BELIRSIZ = float(os.environ.get('BOY', '0'))   # hat boyu çarpanı log-düz ±

def kur(boy_m, r_km, faz_ev):
    return ut.kur(boy_m, r_km, faz_ev)

def model_egim(tr, og, faz_ev, b, agirlik, pu, dengeli_faz=None):
    """Yük düğümlere eşit, PV payı (b_p × pu) düğüm ağırlığıyla. agirlik: faz başına düğüm ağırlıkları (toplam 1).
    dengeli_faz: None = fiderin faz faz ölçümü; yoksa (yük ve PV faz payları) çekilişten."""
    out, warm = [], None
    for (_, s), u in zip(og.iterrows(), pu):
        pe, qe = s['P_IMPORT'] * 1000, s['Q_IMPORT'] * 1000
        net = {'ev': (pe, qe)}
        top = (s['PA'] + s['PB'] + s['PC']) * 1000; topq = (s['QA'] + s['QB'] + s['QC']) * 1000
        btop = sum(b) * 1000
        for p in range(3):
            if dengeli_faz is None:
                kp, kq, bp = s[f'P{ut.FAZ[p]}'] * 1000 - (pe if p == faz_ev else 0), s[f'Q{ut.FAZ[p]}'] * 1000 - (qe if p == faz_ev else 0), b[p] * 1000
            else:
                yp, vp = dengeli_faz
                kp, kq, bp = (top - pe) * yp[p], (topq - qe) * yp[p], btop * vp[p]
                # yükü ve PV'yi ayrı paylaştır: kp = yük payı + PV payı
                kp = (top - pe - btop * u) * yp[p] + btop * u * vp[p]
                bp = btop * vp[p]
            pv = bp * u                      # PV kaynaklı kısım (eksi)
            yuk = kp - pv
            dug = list(range(p, ut.DUGUM, 3))
            for k, w in zip(dug, agirlik[p]):
                net[k] = (yuk / len(dug) + pv * w, kq / len(dug))
        tr['v0'] = s['bara']
        V, _ = tb.solve(tr, net, 1.0, warm, iters=4 if warm else 6)
        warm = V
        v = V[0][-1]
        out.append(abs(v[faz_ev] - v[3]) - s['bara'])
    return ut.egim(pu, np.array(out))[0]

def agirliklar(rng, uc):
    a = []
    for p in range(3):
        dug = list(range(p, ut.DUGUM, 3))
        w = [((k + 1) / (ut.DUGUM + 1)) ** 2 if uc else 1.0 for k in dug]
        if uc:   # uca toplanmış: ağırlıklı rastgele seçim gibi, gürültülü
            w = [x * rng.uniform(0.5, 1.5) for x in w]
        s = sum(w); a.append([x / s for x in w])
    return a

mus = ut.oku_musteri(veri); fid = ut.oku_fider(veri)
satir, cekilis = [], {}
for site, a in ut.SITELER.items():
    rng = random.Random(f'ukpn-{site}')
    ev = mus[mus.Substation == site].drop(columns='Substation').groupby('datetime').mean()
    to, ph, r = ut.eslestir(site, ev, fid); p = ut.FAZ.index(ph)
    fs = fid[(fid.Substation == site) & (fid.To == to)].drop(columns=['Substation', 'To'])
    j = ev.join(fs.groupby('datetime').mean(), how='inner')
    j['bara'] = j[f'V{ph}_Filtered']; j['dv'] = j.V_Filtered - j.bara
    j = j.dropna(subset=['dv', 'P_GEN', 'P_IMPORT', 'Q_IMPORT', 'PA', 'PB', 'PC', 'QA', 'QB', 'QC'])
    saat = j.index.hour
    r_orta = ut.KABLO_R[a['kablo'] or '185 Al']
    ak = j[(saat >= ut.AKSAM[0]) & (saat < ut.AKSAM[1])]
    k, c, _ = ut.egim(ut.model_dv(kur(300, r_orta, p), ak, p), ak.dv); L = k * 300
    og = j[(saat >= ut.OGLE[0]) & (saat < ut.OGLE[1]) & (j.index.month <= 8)]
    pu_hep = og.P_GEN / a['ev_pv_kw']
    e_olc = ut.egim(pu_hep, og.dv)[0]
    # fiderin faz gücünün PV payı: faz gücünün eve ait birim üretime eğimi (kW/pu), evin kendisi hariç
    b = []
    for X in ut.FAZ:
        y = og[f'P{X}'] - (og.P_IMPORT if X == ph else 0)
        b.append(min(0.0, ut.egim(pu_hep, y)[0]))
    ornek = og.sample(min(DAKIKA, len(og)), random_state=1)
    pu = (ornek.P_GEN / a['ev_pv_kw']).values
    duz = model_egim(kur(L, r_orta, p), ornek, p, b, agirliklar(rng, False), pu)
    oran_bilinen, oran_bilinmeyen = [], []
    for d in range(CEKILIS):
        uc = rng.random() < PANEL_UCTA_P
        e = model_egim(kur(L * math.exp(rng.uniform(-BOY_BELIRSIZ, BOY_BELIRSIZ)), r_orta, p), ornek, p, b, agirliklar(rng, uc), pu)
        oran_bilinen.append(e / e_olc)
        # faz bilinmiyor (Kıb-Tek gibi): yük ve PV fazlara çekilen ağırlıkla, ev fazı rastgele değil (ölçülen ΔV o fazda)
        dsap = rng.uniform(0, 0.3)
        yp = np.array([1 + rng.uniform(-dsap, dsap) for _ in range(3)]); yp /= yp.sum()
        vp = np.array([1 + rng.uniform(-dsap, dsap) for _ in range(3)]); vp /= vp.sum()
        Ld = L * math.exp(rng.uniform(-BOY_BELIRSIZ, BOY_BELIRSIZ))
        e2 = model_egim(kur(Ld, r_orta, p), ornek, p, b, agirliklar(rng, uc), pu, dengeli_faz=(yp, vp))
        oran_bilinmeyen.append(e2 / e_olc)
    cekilis[site] = {'faz bilinen': oran_bilinen, 'faz bilinmeyen': oran_bilinmeyen, 'olculen_V_pu': e_olc}
    for ad, o in (('faz bilinen', oran_bilinen), ('faz bilinmeyen', oran_bilinmeyen)):
        o = np.array(o)
        satir.append(dict(site=site, durum=ad, olculen_V_pu=round(e_olc, 2), duz_oran=round(duz / e_olc, 2),
                          P10=round(np.quantile(o, .1), 2), ortanca=round(np.median(o), 2), P90=round(np.quantile(o, .9), 2),
                          P98=round(np.quantile(o, .98), 2), olculen_kapsandi_P98=bool(np.quantile(o, .98) >= 1.0),
                          olculenin_sirasi=round(float(np.mean(o < 1.0)), 2)))
    print(site, 'bitti', flush=True)
D = pd.DataFrame(satir); pd.set_option('display.width', 220); print(D.to_string(index=False))
if os.environ.get('CEKILIS_JSON'):
    import json
    with open(os.environ['CEKILIS_JSON'], 'w', encoding='utf-8') as fh:
        json.dump(dict(boy_belirsiz=BOY_BELIRSIZ, cekilis=CEKILIS, siteler=cekilis), fh, ensure_ascii=False)
