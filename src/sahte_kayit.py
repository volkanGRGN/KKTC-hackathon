#!/usr/bin/env python3
"""Sahte ama gerçeğe yakın Kıb-Tek kayıtları (deneme; karar masası 23:02, 23:03, 23:18; Muhittin 4 madde 5).

Kıb-Tek'in vereceği kayıtlar deneme şehrinde **kusurlarıyla** taklit edilir: kayıt, şehir üreticisinin gerçek ağından
(cevap anahtarının bildiği) bozularak yazılır. Model kayıtları okur (`src/basvuru.py`); gerçek kayıt gelince yalnız
`kayitlar.csv` değişir. Bu dosya deney içindir: resmi hesap cevap anahtarını ve üreticiyi okumaz.

Kayıtlar (satır = trafo ya da abone, `tur` sütunu):
  kademe    trafonun kademe pozisyonunun gerilimi (5 kademe, ±2 × %2,5, boşta 250 V merkez); boş = kayıt yok
  hat       her alçak gerilim hattının boyu (coğrafi bilgi sistemi)
  panelli   mahsuplaşmalı abone: hattı, hattaki yeri (direk sırası ÷ hattaki direk sayısı), fazı (A / B / C / 3 ya da
            boş), kurulu güç (kWp)
  inverter  izin veren panelli evin inverter kaydından geri çözüm: sakin an gerilimi → trafo barası (V), öğlen
            salınımı → o hattın empedansına eşdeğer boy (m)
Başvuru formu (`basvuru_kaydi`): başvuranın hattı, yeri, fazı; aynı kusurlarla.

Kusurlar (`NOMINAL`, [Yorum]; gerçek oranlar Kıb-Tek'e sorulur, istek taslağı): kademe kaydı %80 doğru (%10 komşu
kademe, %10 eksik); abone → trafo eşleşmesi %95 doğru (yanlışsa kayıt bu trafoda yok); direk sırası ±2; faz kaydı %70
dolu, dolunun %90'ı doğru; hat boyu ±%15; inverter panelli evlerin %20'sinde, gürültü bara ±1 V, empedans ±%20.
Düzeyler: `yari` (hatalar yarı), `aynen`, `iki_kat`; `kusursuz` (hata yok, faz hep dolu; inverter kapsaması yine %20).

Gerçek ağ şehir üreticisinin kendi tohumuyla yeniden kurulur (`sehir_uret.sehir_kur` + `uretici13`, aynı çağrı
sırası); yük `yuk_serisi` ile aynı akıştan. `sinama()` cevap anahtarının `kac_ev_gercek`'ini aynı yoldan yeniden
hesaplar (yeniden kurmanın sağlaması).

Çalıştırma:
  python3 src/sahte_kayit.py <şehir kökü> --aralik 1-10            # her şehre kayitlar.csv (düzey aynen)
  python3 src/sahte_kayit.py <şehir kökü> --aralik 1-10 --sinama   # yeniden kurma sağlaması
"""
import argparse
import csv
import json
import math
import random
import sys
from pathlib import Path

_argv, sys.argv = sys.argv, sys.argv[:1]
import sehir_uret as su  # noqa: E402
import trafo_bos_kapasite as tb  # noqa: E402
sys.argv = _argv

KADEME_ADIM_V = 250 * 0.025                              # 6,25 V
KADEME_V = [250 + KADEME_ADIM_V * k for k in (-2, -1, 0, 1, 2)]
NOMINAL = dict(kademe_yanlis=0.10, kademe_eksik=0.10, abone_trafo=0.05, direk=2, faz_eksik=0.30, faz_yanlis=0.10,
               hat=0.15, inverter_pay=0.20, inv_bara_v=1.0, inv_empedans=0.20)
DUZEY_CARPANI = {'kusursuz': 0.0, 'yari': 0.5, 'aynen': 1.0, 'iki_kat': 2.0}
FAZ_AD = {0: 'A', 1: 'B', 2: 'C', 3: '3'}
FAZ_NO = {v: k for k, v in FAZ_AD.items()}


def hata_payi(duzey):
    """Düzeyin kusur oranları. Kapsama (inverter %20) düzeyle değişmez; gürültüsü değişir."""
    f = DUZEY_CARPANI[duzey]
    h = {k: (v * f if k not in ('inverter_pay',) else v) for k, v in NOMINAL.items()}
    h['direk'] = round(NOMINAL['direk'] * f)
    return h


# ---------- gerçek ağ ----------

def gercek_sehir(klasor):
    """Şehrin gerçek ağı ve 14 günlük benzetim girdileri, üreticinin aynı tohum ve çağrı sırasıyla."""
    klasor = Path(klasor)
    tohum = int(klasor.name.split('-')[1])
    with open(klasor / 'ayar.json', encoding='utf-8') as fh:
        ayar_dosya = json.load(fh)
    rng = random.Random(f'yapi-{tohum}')
    egriler, tepe_orani, _ = su.egrileri_yukle()
    siniflar = list(su.SINIFLAR)
    kayma_ust = rng.uniform(30, 60)
    ayar = dict(tuketim_carpani={s: round(rng.uniform(0.8, 1.2), 3) for s in siniflar},
                saat_kaymasi_dk={s: 5 * round(rng.uniform(-kayma_ust, kayma_ust) / 5) for s in siniflar},
                panel_yayginligi=round(rng.uniform(0.03, 0.25), 3), mahalle_sigma=su.MAHALLE_SIGMA)
    rng.choice(su.HAVA_YILLARI)
    rng.randint(1, 30 - su.GUN_SAYISI + 1)
    trafolar, _, _ = su.sehir_kur(rng, 40, ayar, tepe_orani, su.kiyi_segmentleri())
    su.uretici13(trafolar, tohum)
    tarihler = [__import__('datetime').date.fromisoformat(d) for d in ayar_dosya['tarihler']]
    saatlik = su.isinim_oku([y for y in su.ISINIM_DOSYALARI if y.exists()])
    g = [x for t in tarihler for x in su.gunun_isinimi(saatlik, t)]
    og_ogle = random.Random(f'og13-{tohum}').uniform(*su.OG_OGLE_BANT)
    m = su.og_carpani(g, random.Random(f'og-{tohum}'), og_ogle)
    vmax = {}
    with open(klasor / 'yuk_5dk.csv', encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            vmax.setdefault(r['trafo_no'], []).append(float(r['v_max_v']))
    return dict(tohum=tohum, trafolar={tr['no']: tr for tr in trafolar}, ayar=ayar, egriler=egriler, g=g, m=m,
                gun_turleri=ayar_dosya['gun_turleri'], vmax=vmax)


def gercek_trafo(sehir, no):
    """Bir trafonun gerçek yükü, kritik adımları ve o adımların bugünkü çözümü (cevap anahtarıyla aynı tanım)."""
    tr = sehir['trafolar'][no]
    trng = random.Random(f'yuk-{sehir["tohum"]}-{no}')
    yuk = su.yuk_serisi(tr, sehir['ayar'], sehir['egriler'], sehir['gun_turleri'], trng)
    g, m, vm = sehir['g'], sehir['m'], sehir['vmax'][no]
    n = len(g)
    kritik = sorted(range(n), key=lambda i: -vm[i])[:6]
    kritik += [i for i in sorted(range(n), key=lambda i: -g[i])[:3] if i not in kritik]
    taban = {i: tb.solve(tr, su.net_guc(tr, i, g, yuk), m[i], None, iters=8)[0] for i in kritik}
    return dict(tr=tr, yuk=yuk, kritik=kritik, taban=taban, trng=trng)


def gercekte_asar(sehir, gt, ek):
    """ek = {ev id: kW} yeni paneller; bugünkü panellerle birlikte kritik adımlarda 259 V ya da kVA aşılıyor mu."""
    return su.asim(gt['tr'], sehir['g'], sehir['m'], gt['yuk'], gt['kritik'], ek, gt['taban']) is not None


def adaylar(tr):
    return [h['id'] for h in tr['evler'] if h['sinif'] == 'konut' and h['pv'] == 0]


def ev_yeri(tr):
    """{ev id: (hat no, hattaki sıra 0.., hattaki ev sayısı)}"""
    out = {}
    for j, f in enumerate(tr['feeders']):
        for k, h in enumerate(f['houses']):
            out[h['id']] = (j, k, len(f['houses']))
    return out


# ---------- kayıt üretimi ----------

def _yer_kaydi(j, k, n, hp, rng):
    d = rng.randint(-hp['direk'], hp['direk']) if hp['direk'] else 0
    return j, min(1.0, max(1 / n, (k + 1 + d) / n))


def _faz_kaydi(ph, hp, rng):
    if rng.random() < hp['faz_eksik']:
        return ''
    if ph != 3 and rng.random() < hp['faz_yanlis']:
        return FAZ_AD[rng.choice([p for p in (0, 1, 2) if p != ph])]
    return FAZ_AD[ph]


def kayit_uret(tr, hp, rng, inv_bara=None, inv_ham=None):
    """Bir trafonun kayıtları (düzeyin kusurlarıyla). Dönüş sözlüğü kayit_oku ile aynı biçim.
    inv_bara: {ev id: V} inverter barası dışarıdan (`inverter_geri_cozum.py`'nin benzetimde geri çözdüğü sabah ilk
    değer); verilirse gerçek + gürültü yerine o yazılır (rastgele akış aynı kalır).
    inv_ham: {ev id: (bara_olcum_v, egim_v_kw)} inverterin ham özeti (`inverter_kaydi.geri_coz`, benzetimde); verilirse
    inverter kaydı türetilmiş değil ham özet olur, bara ve hat boyu motorda çözülür (karar masası 00:27)."""
    kad = min(KADEME_V, key=lambda v: abs(v - tr['v0']))
    u = rng.random()
    if u < hp['kademe_eksik']:
        kademe = None
    elif u < hp['kademe_eksik'] + hp['kademe_yanlis']:
        i = KADEME_V.index(kad)
        kademe = KADEME_V[i + (1 if i == 0 or (i < 4 and rng.random() < 0.5) else -1)]
    else:
        kademe = kad
    hat = [f['boy'] * math.exp(rng.uniform(math.log(1 - hp['hat']), math.log(1 + hp['hat']))) if hp['hat'] else f['boy']
           for f in tr['feeders']]
    yer = ev_yeri(tr)
    panelli, inverter = {}, {}
    for h in tr['evler']:
        if h['pv'] <= 0:
            continue
        if rng.random() < hp['abone_trafo']:          # kayıt başka trafoda: bu trafo için yok
            continue
        j, k, n = yer[h['id']]
        hj, y = _yer_kaydi(j, k, n, hp, rng)
        panelli[h['id']] = dict(hat=hj, yer=y, faz=_faz_kaydi(h['ph'], hp, rng), kw=h['pv'])
        if rng.random() < hp['inverter_pay']:
            f = tr['feeders'][j]
            e = hp['inv_empedans']
            bara = tr['v0'] + (rng.uniform(-hp['inv_bara_v'], hp['inv_bara_v']) if hp['inv_bara_v'] else 0.0)
            boy = f['boy'] * (math.exp(rng.uniform(math.log(1 - e), math.log(1 + e))) if e else 1.0)
            if inv_ham is not None:
                if h['id'] in inv_ham:
                    b, eg = inv_ham[h['id']]
                    inverter[h['id']] = dict(hat=hj, bara_olcum_v=b, egim_v_kw=eg)
            else:
                inverter[h['id']] = dict(bara_v=inv_bara[h['id']] if inv_bara and h['id'] in inv_bara else bara,
                                         hat=j, esdeger_boy_m=boy)
    return dict(kademe_v=kademe, hat_boy_m=hat, panelli=panelli, inverter=inverter)


def basvuru_kaydi(tr, hid, hp, rng):
    """Başvuru formu: hattı, yeri, fazı; abone → trafo yanlışsa (ya da adres eşleşmezse) None."""
    if rng.random() < hp['abone_trafo']:
        return None
    h = next(x for x in tr['evler'] if x['id'] == hid)
    j, k, n = ev_yeri(tr)[hid]
    hj, y = _yer_kaydi(j, k, n, hp, rng)
    return dict(hat=hj, yer=y, faz=_faz_kaydi(h['ph'], hp, rng))


# ---------- dosya ----------

SUTUNLAR = ['sehir', 'trafo_no', 'tur', 'abone_no', 'hat_no', 'yer', 'faz', 'kw', 'deger']


def kayit_yaz(yol, sehir, kayitlar):
    """kayitlar: {trafo_no: kayit_uret çıktısı} -> kayitlar.csv (UTF-8, LF)."""
    satir = []
    for no, k in kayitlar.items():
        satir.append([sehir, no, 'kademe', '', '', '', '', '', '' if k['kademe_v'] is None else f"{k['kademe_v']:.2f}"])
        for j, b in enumerate(k['hat_boy_m']):
            satir.append([sehir, no, 'hat', '', j, '', '', '', f'{b:.1f}'])
        for hid, p in k['panelli'].items():
            satir.append([sehir, no, 'panelli', hid, p['hat'], f"{p['yer']:.4f}", p['faz'], f"{p['kw']:.2f}", ''])
        for hid, v in k['inverter'].items():
            if 'egim_v_kw' in v:
                eg = '' if v['egim_v_kw'] is None else f"{v['egim_v_kw']:.4f}"
                satir.append([sehir, no, 'inverter_ham', hid, v['hat'], '', '', '', f"{v['bara_olcum_v']:.2f};{eg}"])
            else:
                satir.append([sehir, no, 'inverter', hid, v['hat'], '', '', '',
                              f"{v['bara_v']:.2f};{v['esdeger_boy_m']:.1f}"])
    with open(yol, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(SUTUNLAR)
        w.writerows(satir)


def kayit_oku(yol):
    """kayitlar.csv -> {trafo_no: kayıt sözlüğü}. Gerçek Kıb-Tek kaydı aynı biçimde gelirse model değişmez."""
    out = {}
    with open(yol, encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            k = out.setdefault(r['trafo_no'], dict(kademe_v=None, hat_boy_m=[], panelli={}, inverter={}))
            if r['tur'] == 'kademe':
                k['kademe_v'] = float(r['deger']) if r['deger'] else None
            elif r['tur'] == 'hat':
                j = int(r['hat_no'])
                k['hat_boy_m'] += [None] * (j + 1 - len(k['hat_boy_m']))
                k['hat_boy_m'][j] = float(r['deger'])
            elif r['tur'] == 'panelli':
                k['panelli'][int(r['abone_no'])] = dict(hat=int(r['hat_no']), yer=float(r['yer']), faz=r['faz'],
                                                        kw=float(r['kw']))
            elif r['tur'] == 'inverter':
                b, e = r['deger'].split(';')
                k['inverter'][int(r['abone_no'])] = dict(hat=int(r['hat_no']), bara_v=float(b), esdeger_boy_m=float(e))
            elif r['tur'] == 'inverter_ham':
                b, e = r['deger'].split(';')
                k['inverter'][int(r['abone_no'])] = dict(hat=int(r['hat_no']), bara_olcum_v=float(b),
                                                         egim_v_kw=float(e) if e else None)
    return out


# ---------- sağlama ----------

def sinama(klasor):
    """Cevap anahtarının kac_ev_gercek'i yeniden kurulan ağdan (aynı akış, aynı sıralar) birebir mi."""
    sehir = gercek_sehir(klasor)
    with open(Path(klasor) / 'cevap_anahtari.csv', encoding='utf-8', newline='') as fh:
        cevap = {r['trafo_no']: r for r in csv.DictReader(fh)}
    tutan, fark = 0, []
    for no, tr in sehir['trafolar'].items():
        c = cevap[no]
        faz = [sum(1 for h in tr['evler'] if h['ph'] == p) for p in range(4)]
        ayni_yapi = (abs(tr['v0'] - float(c['v0_v'])) < 0.05
                     and faz == [int(c['faz_a_ev']), int(c['faz_b_ev']), int(c['faz_c_ev']), int(c['uc_faz_ev'])])
        gt = gercek_trafo(sehir, no)
        ad = adaylar(tr)
        bugun = gercekte_asar(sehir, gt, {})
        sonuc = []
        for _ in range(su.SIRA_SAYISI):
            sira = ad[:]
            gt['trng'].shuffle(sira)
            ek = {}
            if not bugun:
                for hid in sira:
                    ek[hid] = su.YENI_PANEL_KW
                    if gercekte_asar(sehir, gt, ek):
                        del ek[hid]
            sonuc.append(len(ek))
        orta = sorted(sonuc)[su.SIRA_SAYISI // 2]
        if ayni_yapi and orta == int(c['kac_ev_gercek']):
            tutan += 1
        else:
            fark.append((no, ayni_yapi, orta, c['kac_ev_gercek']))
    return tutan, len(sehir['trafolar']), fark


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('kok')
    ap.add_argument('--aralik', default='1-10')
    ap.add_argument('--duzey', default='aynen', choices=list(DUZEY_CARPANI))
    ap.add_argument('--sinama', action='store_true')
    a = ap.parse_args()
    bas, son = (int(x) for x in a.aralik.split('-'))
    for t in range(bas, son + 1):
        k = Path(a.kok) / f'sehir-{t:03d}'
        if a.sinama:
            tutan, n, fark = sinama(k)
            print(f'{k.name}: kac_ev_gercek ve yapı {tutan}/{n} trafoda birebir' + (f'; fark {fark[:5]}' if fark else ''))
            continue
        sehir = gercek_sehir(k)
        hp = hata_payi(a.duzey)
        kay = {no: kayit_uret(tr, hp, random.Random(f'kayit-{a.duzey}-{t}-{no}')) for no, tr in sehir['trafolar'].items()}
        kayit_yaz(k / 'kayitlar.csv', t, kay)
        print(f'{k.name}: kayitlar.csv ({a.duzey}): {sum(len(x["panelli"]) for x in kay.values())} panelli kaydı, '
              f'{sum(len(x["inverter"]) for x in kay.values())} inverter, '
              f'{sum(x["kademe_v"] is not None for x in kay.values())}/{len(kay)} kademe')


if __name__ == '__main__':
    main()
