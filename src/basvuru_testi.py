#!/usr/bin/env python3
"""Başvuru anı motorunun testi, sahte Kıb-Tek kayıtlarıyla (deneme; karar masası 23:18, 23:02, 23:03).

Her trafoda cevap anahtarının panelsiz konutlarından rastgele sıralı başvuru akışı (SIRA sıra, her birinde en çok
EN_COK başvuru; tanım cevap anahtarındaki "gerçek kaç ev" gibi: 6,5 kW, sırayla). Her başvuruya motor karar verir
(`basvuru.karar`); `evet` alanlar sonrakine taahhüt olarak girer. Gerçek: şehir üreticisinin ağı aynı tohumdan
(`sahte_kayit.gercek_trafo`), bu başvuru öncekilerle birlikte 259 V ya da kVA'yı aşıyor mu.

Senaryolar: kayıtsız (bugün) / sahte kayıt, hatalar yarı / beklenen / iki kat / kusursuz bilgi. Model kayıt hatasını
`--model-hata` düzeyinde varsayar (varsayılan motorunki, iki kat: karar masası 23:47; `aynen` = ilk koşum, 31 Ekim
23:46); kusursuzda sıfır.
Aynı akışta iki kıyas politikası: %40 kuralı (onaylanan sayısı `kural40_ev`'e kadar evet) ve harita (trafo yeşilse ilk
iki başvuru evet; o senaryonun haritasıyla).
Ölçüler: başvuru anında **yanlış evet** (kapı: evet alanların < %2'si), hemen evet alan pay, önce ölç, hayır;
haritanın renkleri ve yanlış yeşili kayıtlarla.

Etiket: sahte kayıtlarla, gösterim; gerçek kayıtlar Kıb-Tek'ten. Ayar yok: eşikler resmi hesabınki.

Çalıştırma:
  python3 src/basvuru_testi.py <şehir kökü> --aralik 1-10 [--model-hata iki_kat|aynen] [--json cikti.json]
  # inverter barası benzetimde geri çözülmüş (Muhittin 5B); motor hata dağılımını 1–10'un ölçümünden alır:
  python3 src/basvuru_testi.py <kök> --aralik 1-10 --inverter-bara igc.json [--bara-hata igc_1-10.json]
  # inverter kaydı ham özet (bara ölçümü, eğim), çözüm motorda (karar masası 00:27):
  python3 src/basvuru_testi.py <kök> --aralik 1-10 --inverter-ham igc.json
"""
import argparse
import csv
import json
import random
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

_argv, sys.argv = sys.argv, sys.argv[:1]
import basvuru as bv  # noqa: E402
import kac_ev as ke  # noqa: E402
import sahte_kayit as sk  # noqa: E402
sys.argv = _argv

SENARYOLAR = ['kayitsiz', 'yari', 'aynen', 'iki_kat', 'kusursuz']
AD = {'kayitsiz': 'kayıtsız (bugün)', 'yari': 'sahte kayıt, hatalar yarı', 'aynen': 'sahte kayıt, beklenen',
      'iki_kat': 'sahte kayıt, hatalar iki kat', 'kusursuz': 'kusursuz bilgi'}
SIRA = 3
BAYRAK_P = getattr(bv.ko, 'BAYRAK_P', 0.7)          # ADR-0017 "büyük olasılıkla dolu" (kac_ev_olasilik, PR #23)
EN_COK = 8


def _csv(yol):
    with open(yol, encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


def sehir_senaryo(is_):
    klasor, senaryo, model_hata, inv_bara, bara_hata, inv_ham = (Path(is_[0]), is_[1], is_[2], is_[3], is_[4],
                                                                  is_[5])
    sehir = sk.gercek_sehir(klasor)
    tohum = sehir['tohum']
    trafolar = _csv(klasor / 'trafolar.csv')
    tahmin = {r['trafo_no']: r for r in _csv(klasor / 'tahmin.csv')}
    resmi = {r['trafo_no']: r for r in _csv(klasor / 'kac_ev.csv')}
    hp_veri = None if senaryo == 'kayitsiz' else sk.hata_payi(senaryo)
    hp_model = sk.hata_payi('kusursuz' if senaryo == 'kusursuz' else model_hata)
    if senaryo == 'kusursuz':
        inv_bara = inv_ham = None
    elif bara_hata:
        hp_model['inv_bara_hata'] = bara_hata
    out = []
    for r in trafolar:
        no = r['trafo_no']
        tr = {k: (r[k] if k in ('trafo_no', 'kablo', 'bolge', 'montaj') else ke.sayi(r[k])) for k in r}
        t = tahmin[no]
        gt = sk.gercek_trafo(sehir, no)
        gtr = gt['tr']
        kayit = None if hp_veri is None else sk.kayit_uret(gtr, hp_veri, random.Random(f'kayit-{senaryo}-{tohum}-{no}'),
                                                           (inv_bara or {}).get(no),
                                                           None if inv_ham is None else inv_ham.get(no, {}))
        if kayit is None:
            renk, p_bugun = resmi[no]['renk'], float(resmi[no]['p_bugun_asar'])
        else:
            renk, p_bugun, _ = bv.harita_rengi(tr, t, kayit, random.Random(f'harita-{senaryo}-{tohum}-{no}'), hp_model)
        # inverterli trafo: "beklenen" düzeyin kaydında en az bir inverter (her senaryoda aynı alt küme)
        inverterli = bool(sk.kayit_uret(gtr, sk.hata_payi('aynen'), random.Random(f'kayit-aynen-{tohum}-{no}'))['inverter'])
        kural40 = int(resmi[no]['kural40_ev'])
        akis = []
        ad = sk.adaylar(gtr)
        for s in range(SIRA if ad else 0):
            sira = ad[:]
            random.Random(f'akis-{tohum}-{no}-{s}').shuffle(sira)
            sira = sira[:EN_COK]
            onay, taahhut = {}, []
            k40, h_onay = {}, {}
            for j, hid in enumerate(sira):
                form = None if hp_veri is None else sk.basvuru_kaydi(
                    gtr, hid, hp_veri, random.Random(f'form-{senaryo}-{tohum}-{no}-{hid}'))
                k, p = bv.karar(tr, t, kayit, form, taahhut,
                                random.Random(f'motor-{senaryo}-{tohum}-{no}-{s}-{j}'), hp_model)
                asar = sk.gercekte_asar(sehir, gt, {**onay, hid: ke.YENI_PANEL_KW})
                satir = dict(sira=s, j=j, karar=k, p=p, asar=asar)
                if k == 'evet':
                    onay[hid] = ke.YENI_PANEL_KW
                    taahhut.append(form)
                if len(k40) < kural40:                       # %40 kuralı: sayısına kadar evet
                    satir['k40_asar'] = sk.gercekte_asar(sehir, gt, {**k40, hid: ke.YENI_PANEL_KW})
                    k40[hid] = ke.YENI_PANEL_KW
                if renk == 'yesil' and len(h_onay) < 2:      # harita: yeşilse ilk iki başvuru evet
                    satir['harita_asar'] = sk.gercekte_asar(sehir, gt, {**h_onay, hid: ke.YENI_PANEL_KW})
                    h_onay[hid] = ke.YENI_PANEL_KW
                akis.append(satir)
        out.append(dict(trafo_no=no, renk=renk, p_bugun=p_bugun, inverterli=inverterli, resmi_renk=resmi[no]['renk'],
                        resmi_p=float(resmi[no]['p_bugun_asar']), guven=t['guven'], akis=akis))
    return str(klasor), senaryo, out


def ozet(klasorler, sonuc, senaryo):
    n = evet = yevet = olc = hayir = hayir_sigar = 0
    k40 = k40_y = h = h_y = 0
    renk = {'yesil': 0, 'sari': 0, 'kirmizi': 0}
    yanlis_yesil = kir_asan = 0
    uc = {g: {'yesil': 0, 'dolu_bayrak': 0, 'bos': 0, 'yanlis_yesil': 0, 'bayrak_dolu': 0} for g in ('kayitli', 'resmi')}
    tip_evet, tip_n = {}, {}
    for k in klasorler:
        cevap = {r['trafo_no']: r for r in _csv(k / 'cevap_anahtari.csv')}
        for x in sonuc[(str(k), senaryo)]:
            c = cevap[x['trafo_no']]
            if int(c['kac_ev_aday']) > 0 and x['inverterli']:          # inverterli trafolarda panel katmanı (ADR-0017)
                dolu = int(c['kac_ev_gercek']) == 0
                for g_, (r_, p_) in (('kayitli', (x['renk'], x['p_bugun'])), ('resmi', (x['resmi_renk'], x['resmi_p']))):
                    u_ = 'yesil' if r_ == 'yesil' else ('dolu_bayrak' if p_ >= BAYRAK_P else 'bos')
                    uc[g_][u_] += 1
                    uc[g_]['yanlis_yesil'] += u_ == 'yesil' and dolu
                    uc[g_]['bayrak_dolu'] += u_ == 'dolu_bayrak' and dolu
            if int(c['kac_ev_aday']) > 0:
                renk[x['renk']] += 1
                yanlis_yesil += x['renk'] == 'yesil' and int(c['kac_ev_gercek']) == 0
                kir_asan += x['renk'] == 'kirmizi' and float(c['v_max_bugun_v']) > ke.V_SINIR
            for a in x['akis']:
                n += 1
                tip_n[c['tip']] = tip_n.get(c['tip'], 0) + 1
                if a['karar'] == 'evet':
                    evet += 1
                    yevet += a['asar']
                    tip_evet[c['tip']] = tip_evet.get(c['tip'], 0) + 1
                elif a['karar'] == 'once_olc':
                    olc += 1
                else:
                    hayir += 1
                    hayir_sigar += not a['asar']
                if 'k40_asar' in a:
                    k40 += 1
                    k40_y += a['k40_asar']
                if 'harita_asar' in a:
                    h += 1
                    h_y += a['harita_asar']
    return dict(basvuru=n, evet=evet, yanlis_evet=yevet, once_olc=olc, hayir=hayir, hayir_ama_sigar=hayir_sigar,
                k40_evet=k40, k40_yanlis=k40_y, harita_evet=h, harita_yanlis=h_y, renk=renk, yanlis_yesil=yanlis_yesil,
                kirmizi_asan=kir_asan, tip_evet=tip_evet, tip_n=tip_n, inverterli_uc=uc)


def yuzde(a, b):
    return f'%{100 * a / b:.1f} ({a}/{b})' if b else '— (0/0)'


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('kok')
    ap.add_argument('--aralik', default='1-10')
    ap.add_argument('--senaryo', help='virgülle; yoksa hepsi')
    ap.add_argument('--model-hata', default=bv.VARSAYILAN_HATA, choices=['aynen', 'iki_kat'],
                    help='motorun varsaydığı kayıt hatası düzeyi')
    ap.add_argument('--inverter-bara', help='inverter_geri_cozum.py JSON: kayıttaki inverter barası geri çözümden')
    ap.add_argument('--bara-hata', help='inverter_geri_cozum.py JSON (1–10): motor bara hatasını bu dağılımdan çeker')
    ap.add_argument('--inverter-ham', help='inverter_geri_cozum.py JSON: inverter kaydı ham özet, çözüm motorda')
    ap.add_argument('--json')
    ap.add_argument('--surum-zorla', action='store_true',
                    help='şehrin üretici sürümü farklıysa da yeniden kur (yalnız uyar; sonuç güvenilmez)')
    a = ap.parse_args()
    sk.surum_zorla(a.surum_zorla)
    bas, son = (int(x) for x in a.aralik.split('-'))
    klasorler = [Path(a.kok) / f'sehir-{t:03d}' for t in range(bas, son + 1)]
    senaryolar = a.senaryo.split(',') if a.senaryo else SENARYOLAR
    inv = {}
    if a.inverter_bara:
        with open(a.inverter_bara, encoding='utf-8') as fh:
            for s_ in json.load(fh)['sehirler']:
                for x in s_['evler']:
                    inv.setdefault(s_['sehir'], {}).setdefault(x['trafo_no'], {})[x['ev']] = x['b_sabah']
    ham = {}
    if a.inverter_ham:
        with open(a.inverter_ham, encoding='utf-8') as fh:
            for s_ in json.load(fh)['sehirler']:
                for x in s_['evler']:
                    ham.setdefault(s_['sehir'], {}).setdefault(x['trafo_no'], {})[x['ev']] = (x['b_sabah'], x['egim'])
    bara_hata = None
    if a.bara_hata:
        with open(a.bara_hata, encoding='utf-8') as fh:
            bara_hata = [x['b_sabah'] - x['v0'] for s_ in json.load(fh)['sehirler'] for x in s_['evler']]
    with ProcessPoolExecutor() as ex:
        sonuc = {(k, s): o for k, s, o in ex.map(sehir_senaryo,
                                                  [(str(k), s, a.model_hata, inv.get(int(k.name.split('-')[1])),
                                                    bara_hata,
                                                    ham.get(int(k.name.split('-')[1]), {}) if a.inverter_ham else None)
                                                   for s in senaryolar for k in klasorler])}
    tablo = {s: ozet(klasorler, sonuc, s) for s in senaryolar}
    print(f'şehir {a.aralik} — sahte kayıtlarla, gösterim; {SIRA} sıra × en çok {EN_COK} başvuru; '
          f'motor kayıt hatasını {a.model_hata} varsayar'
          + ('; inverter barası benzetimde geri çözülmüş' if a.inverter_bara else '')
          + ('; inverter kaydı ham özet, çözüm motorda' if a.inverter_ham else '')
          + (f'; motor bara hatasını ölçülmüş dağılımdan çeker (n {len(bara_hata)})' if bara_hata else ''))
    print('senaryo | başvuru | hemen evet | yanlış evet (evetlerin) | önce ölç | hayır (gerçekte sığan) | '
          '%40 kuralı yanlış evet | harita yanlış evet | renk y / s / k | yanlış yeşil | kırmızıda aşan')
    for s, o in tablo.items():
        r = o['renk']
        nt = sum(r.values())
        print(f"{AD[s]} | {o['basvuru']} | {yuzde(o['evet'], o['basvuru'])} | {yuzde(o['yanlis_evet'], o['evet'])} | "
              f"{yuzde(o['once_olc'], o['basvuru'])} | {yuzde(o['hayir'], o['basvuru'])} ({o['hayir_ama_sigar']}) | "
              f"{yuzde(o['k40_yanlis'], o['k40_evet'])} | {yuzde(o['harita_yanlis'], o['harita_evet'])} | "
              f"{r['yesil']} / {r['sari']} / {r['kirmizi']} (n {nt}) | {o['yanlis_yesil']}/{r['yesil']} | "
              f"{yuzde(o['kirmizi_asan'], r['kirmizi'])}")
    print('\ninverterli trafolarda panel katmanı (aday evi olan; ADR-0017): görünüm | yeşil (yanlış) | bayrak (gerçekte dolu) | renksiz')
    for s, o in tablo.items():
        for g_ in ('resmi', 'kayitli'):
            u_ = o['inverterli_uc'][g_]
            n_ = u_['yesil'] + u_['dolu_bayrak'] + u_['bos']
            print(f"{AD[s]} — {'kayıtsız (resmi)' if g_ == 'resmi' else 'kayıtlı'} | {u_['yesil']} ({u_['yanlis_yesil']}) | "
                  f"{u_['dolu_bayrak']} ({u_['bayrak_dolu']}) | {yuzde(u_['bos'], n_)}")
    print('\nhemen evet, türe göre:')
    for s, o in tablo.items():
        print(f"{AD[s]} | " + ', '.join(f"{t} {o['tip_evet'].get(t, 0)}/{o['tip_n'][t]}" for t in sorted(o['tip_n'])))
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(dict(aralik=a.aralik, sira=SIRA, en_cok=EN_COK, model_hata=a.model_hata, tablo=tablo,
                           trafo={f'{Path(k).name}|{s}': o for (k, s), o in sonuc.items()}), fh, ensure_ascii=False)


if __name__ == '__main__':
    main()
