#!/usr/bin/env python3
"""Kalibrasyon gerçeğe karşı (Faz 7; ADR-0013 madde 3; karar masası 21:32): ölçüler ve katsayılar.

Tüzük (docs/tuzuk.md): katsayılar yalnız GERÇEK artıklardan; farazi şehre bakarak seçilmez.

Bant log ölçeğinde okunur: tahmin t, %80 bant [p10, p90], gerçek y; artık r = ln(y / t). Bant iki parçalı:
yarım genişlik üstte ln(p90 / t), altta ln(t / p10). Birim artık u = r ÷ (artığın düştüğü taraftaki yarım
genişlik); |u| ≤ 1 ise gerçek %80 bandın içinde.
  - şişirme katsayısı k = |u|'nun %80 yüzdeliği. k = 1 kalibre; k > 1 bant dar ("fazla emin"), bant log ölçekte
    k ile genişletilir: p10' = t · (p10 / t)^k, p90' = t · (p90 / t)^k.
  - kapsama eğrisi: nominal q bandı = %80 bandın z((1+q)/2) ÷ z(0,9) katı (iki parçalı normal varsayımı [Yorum]);
    ampirik kapsama = |u| ≤ o kat olan payı.
  - PIT: iki parçalı normal: Φ(1,2816 · u). Kalibre bantta PIT düzdür (10 kovada her biri ~%10).
  - bir-dışarıda k: her grup (trafo) için k o grup dışındakilerden; o grubun kapsaması o k ile. Katsayının
    ayarlandığı veride ölçülen "iç örnek" kapsamadan farklı olarak dürüst tahmindir.
Model-sapma (gerilim, İngiltere): her hat için model çekilişleri o = model eğimi ÷ ölçülen eğim. Ölçülen, modelin
exp(δ) katı: δ_i ≈ −ortalama(ln o). Moment tahmini: μ = ortalama(δ_i), σ² = max(0, var(δ_i) − ortalama(var(ln o))).
Çekiliş başına çarpan s = exp(N(μ, σ)), modelin gerilim duyarlılığını (empedansları) çarpar.

Saf Python (statistics), bağımlılık yok.

Çalıştırma:
  python3 src/kalibrasyon.py --deneme                                 # bilinen dağılım: k ≈ 1 ve ≈ 1,5
  python3 src/kalibrasyon.py ispanya edp_satirlar.csv [--girdi c] [--n 10,15] [--yol tabakali]   # src/edp_test.py --kalibrasyonsuz --cikti çıktısı;
                                                                     # --n: sevk yapılandırmasına (12 ölçülü) en yakın denemeler;
                                                                     # --yol: ölçülecek trafoyu seçme yöntemi, ürününki tabakalı (2b)
                                                                     # (K_YUK'lu satırlarla k ≈ 1 çıkmalı: sağlama)
  python3 src/kalibrasyon.py ingiltere ukpn_cekilis.json [--durum "faz bilinmeyen"]   # ukpn_olasilik CEKILIS_JSON
  ... --cikti ozet.json                                               # özet JSON'a da
"""
import argparse
import csv
import json
import math
import random
import statistics as st
from statistics import NormalDist

N = NormalDist()
Z80 = N.inv_cdf(0.9)                    # %80 iki yanlı bandın yarım genişliği, standart normal birimde
NOMINALLER = (0.5, 0.8, 0.9, 0.95)


def nicel(x, q):
    """Doğrusal aradeğerli yüzdelik (numpy 'linear' ile aynı)."""
    x = sorted(x)
    if not x:
        return float('nan')
    h = (len(x) - 1) * q
    a = math.floor(h)
    b = min(a + 1, len(x) - 1)
    return x[a] + (x[b] - x[a]) * (h - a)


def birim_artik(t, p10, p90, y):
    """u = ln(y/t) ÷ ilgili taraftaki yarım genişlik. Geçersiz satırda None."""
    if min(t, p10, p90, y) <= 0 or not (p10 <= t <= p90):
        return None
    r = math.log(y / t)
    yarim = math.log(p90 / t) if r >= 0 else math.log(t / p10)
    if yarim <= 0:
        return None
    return r / yarim


def sisirme_k(u, hedef=0.8):
    return nicel([abs(x) for x in u], hedef)


def kapsama(u, k=1.0, nominaller=NOMINALLER):
    """{nominal: ampirik kapsama} — bant k ile genişletilmiş hâliyle."""
    out = {}
    for q in nominaller:
        kat = k * N.inv_cdf((1 + q) / 2) / Z80
        out[q] = sum(abs(x) <= kat for x in u) / len(u)
    return out


def pit(u, k=1.0):
    return [N.cdf(Z80 * x / k) for x in u]


def pit_kovalari(p, kova=10):
    say = [0] * kova
    for x in p:
        say[min(kova - 1, int(x * kova))] += 1
    pay = [s / len(p) for s in say]
    return pay, max(abs(x - 1 / kova) for x in pay)


def bir_disarida_k(gruplu, hedef=0.8):
    """gruplu: {grup: [u, ...]}. Her grup için k diğerlerinden; dönüş: [(u, k_dışarıda)], {grup: k}."""
    satir, kler = [], {}
    for g, ug in gruplu.items():
        diger = [x for h, uh in gruplu.items() if h != g for x in uh]
        k = sisirme_k(diger, hedef)
        kler[g] = k
        satir += [(x, k) for x in ug]
    return satir, kler


def kapsama_dis(satir, q=0.8):
    kat = N.inv_cdf((1 + q) / 2) / Z80
    return sum(abs(x) <= k * kat for x, k in satir) / len(satir)


def model_sapma(siteler):
    """siteler: {site: [o, ...]} (o = model ÷ ölçülen). Dönüş: μ, σ, site başına δ ve iç yayılım."""
    d, v = {}, {}
    for s, o in siteler.items():
        lo = [math.log(x) for x in o if x > 0]
        d[s] = -st.mean(lo)
        v[s] = st.pvariance(lo)
    mu = st.mean(d.values())
    sig2 = max(0.0, st.variance(d.values()) - st.mean(v.values())) if len(d) > 1 else 0.0
    return mu, math.sqrt(sig2), d, v


def p98_kapsar(o, mu, sig, rng, tekrar=20):
    """Model çekilişleri × s = exp(N(μ, σ)) dağılımının P98'i ölçüleni (oran 1) kapsıyor mu."""
    x = [oi * math.exp(rng.gauss(mu, sig)) for oi in o for _ in range(tekrar)] if sig > 0 or mu != 0 else list(o)
    return nicel(x, 0.98) >= 1.0, nicel(x, 0.98), sum(xi < 1.0 for xi in x) / len(x)


def en_kucuk_sigma(siteler, mu, adim=0.01, ust=1.5, tohum=1):
    """Bütün hatlarda P98 kapsaması için gereken en küçük σ (μ sabit) — "6 hatla ayarlandı" aralığının ucu."""
    s = 0.0
    while s <= ust:
        rng = random.Random(tohum)
        if all(p98_kapsar(o, mu, s, rng)[0] for o in siteler.values()):
            return round(s, 3)
        s += adim
    return None


# ---------- veri kaynakları ----------

def ispanya(yol, girdi='c', olculu=('10', '15'), secim='tabakali'):
    """olculu: hangi ölçülü sayısı denemeleri (sevk yapılandırması 12 ölçülü → 10 ve 15; karar masası 22:0x).
    secim: ölçülecek trafoyu seçme yöntemi; ürün tabakalı seçer (sablon.py ogretici_sec), sevk yapılandırması onun
    (karar masası 23:13). Rastgele ile havuzlanmaz: iki yolun hatası ters yönde (rastgele k 1,07, tabakalı 1,47)."""
    with open(yol, encoding='utf-8', newline='') as fh:
        rows = [r for r in csv.DictReader(fh) if r['girdi'] == girdi and (not olculu or r['n'] in olculu)
                and (not secim or r['yol'] == secim)]
    gruplu = {}
    for r in rows:
        u = birim_artik(float(r['tah']), float(r['alt']), float(r['ust']), float(r['y']))
        if u is not None:
            gruplu.setdefault(r['ct'], []).append(u)
    u = [x for g in gruplu.values() for x in g]
    k = sisirme_k(u)
    dis, kler = bir_disarida_k(gruplu)
    p_once, sap_once = pit_kovalari(pit(u))
    p_sonra, sap_sonra = pit_kovalari(pit(u, k))
    return dict(
        kaynak=f'EDP Oviedo 2018, {len(gruplu)} trafo, bir-dışarıda tahminler (src/edp_test.py girdi {girdi}, ölçülü {"+".join(olculu) if olculu else "hepsi"}, seçim {secim or "iki yol"})',
        satir=len(u), trafo=len(gruplu), k=round(k, 3),
        kapsama_once={str(q): round(v, 3) for q, v in kapsama(u).items()},
        kapsama_sonra_ic_ornek={str(q): round(v, 3) for q, v in kapsama(u, k).items()},
        kapsama80_sonra_bir_disarida=round(kapsama_dis(dis), 3),
        k_bir_disarida_aralik=[round(min(kler.values()), 3), round(max(kler.values()), 3)],
        pit_once=[round(x, 3) for x in p_once], pit_sapma_once=round(sap_once, 3),
        pit_sonra=[round(x, 3) for x in p_sonra], pit_sapma_sonra=round(sap_sonra, 3),
        u_ortanca=round(st.median(u), 3))


def ingiltere(yol, durum='faz bilinmeyen'):
    with open(yol, encoding='utf-8') as fh:
        j = json.load(fh)
    siteler = {s: v[durum] for s, v in j['siteler'].items()}
    mu, sig, d, v = model_sapma(siteler)
    rng = random.Random(7)
    once = {s: p98_kapsar(o, 0.0, 0.0, rng) for s, o in siteler.items()}
    sonra = {s: p98_kapsar(o, mu, sig, random.Random(7)) for s, o in siteler.items()}
    # bir-dışarıda: her hat için μ, σ diğer 5 hattan
    dis = {}
    for s in siteler:
        diger = {h: o for h, o in siteler.items() if h != s}
        m2, s2, _, _ = model_sapma(diger)
        dis[s] = dict(mu=round(m2, 3), sigma=round(s2, 3), kapsar=p98_kapsar(siteler[s], m2, s2, random.Random(7))[0])
    sig_min = en_kucuk_sigma(siteler, max(mu, 0.0))
    return dict(
        kaynak=f'UKPN 2014, {len(siteler)} hat, durum "{durum}", hat boyu belirsizliği ±{j["boy_belirsiz"]}, '
               f'{j["cekilis"]} çekiliş (src/ukpn_olasilik.py)',
        mu=round(mu, 3), sigma=round(sig, 3),
        site_delta={s: round(x, 3) for s, x in d.items()}, site_ic_sd={s: round(math.sqrt(x), 3) for s, x in v.items()},
        p98_once={s: dict(kapsar=k[0], p98=round(k[1], 2), olculenin_sirasi=round(1 - k[2], 2)) for s, k in once.items()},
        p98_sonra={s: dict(kapsar=k[0], p98=round(k[1], 2)) for s, k in sonra.items()},
        kapsanan_once=sum(k[0] for k in once.values()), kapsanan_sonra=sum(k[0] for k in sonra.values()),
        bir_disarida=dis, kapsanan_bir_disarida=sum(x['kapsar'] for x in dis.values()),
        sigma_6da6_icin_en_az=sig_min)


def deneme():
    rng = random.Random(42)
    out = {}
    for gercek_sd_kat in (1.0, 1.5):
        u = []
        for _ in range(4000):
            t = math.exp(rng.gauss(3, 1))
            sd = 0.2                                    # modelin söylediği log sd
            p10, p90 = t * math.exp(-Z80 * sd), t * math.exp(Z80 * sd)
            y = t * math.exp(rng.gauss(0, sd * gercek_sd_kat))
            u.append(birim_artik(t, p10, p90, y))
        out[f'gerçek yayılım × {gercek_sd_kat}'] = dict(k=round(sisirme_k(u), 3),
                                                        kapsama=round(kapsama(u)[0.8], 3),
                                                        pit_sapma=round(pit_kovalari(pit(u))[1], 3))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('kaynak', nargs='?', choices=['ispanya', 'ingiltere'])
    ap.add_argument('dosya', nargs='?')
    ap.add_argument('--girdi', default='c')
    ap.add_argument('--n', default='10,15', help='ölçülü sayısı kesiti (sevk 12 ölçülü); "hepsi" = süzme yok')
    ap.add_argument('--yol', default='tabakali', help='seçim yöntemi (ürününki tabakalı); "hepsi" = iki yol birlikte')
    ap.add_argument('--durum', default='faz bilinmeyen')
    ap.add_argument('--deneme', action='store_true')
    ap.add_argument('--cikti')
    a = ap.parse_args()
    if a.deneme:
        ozet = deneme()
    elif a.kaynak == 'ispanya':
        ozet = ispanya(a.dosya, a.girdi, None if a.n == 'hepsi' else tuple(a.n.split(',')), None if a.yol == 'hepsi' else a.yol)
    elif a.kaynak == 'ingiltere':
        ozet = ingiltere(a.dosya, a.durum)
    else:
        ap.error('--deneme ya da ispanya / ingiltere <dosya>')
    print(json.dumps(ozet, ensure_ascii=False, indent=1))
    if a.cikti:
        with open(a.cikti, 'w', encoding='utf-8') as fh:
            json.dump(ozet, fh, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
