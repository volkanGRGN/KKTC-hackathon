#!/usr/bin/env python3
"""PV'yi tamamen bırakmadan ne kadar açılır: inverter geri çözümü ve kademe öncülü (deneme; karar masası 22:56,
Muhittin cevap 4 madde 5). Resmi hesap (`kac_ev_olasilik.py`, v2b) ve resmi rakamlar değişmez.

Gerçekçi `bilgi_degeri.py`: kusursuz bilgi yerine eldeki ucuz verinin gürültülü hâli. Her çekilişte resmi kod ağı kendi
rastgelesiyle kurar; bu betik ardından bilineni yerleştirir. Yeni gürültüler ayrı bir rastgele akıştan (`acilma-`);
diğer çekilişler resmi hesapla aynı kalır (S0 = resmi `kac_ev.csv`, sınanır).

Senaryolar:
  S0          bugün (v2b).
  S-kademe    bara gerilimi sürekli 244–252 V yerine AYRIK öncül. Kademe 5 pozisyon, ±2 × %2,5 (boşta 250 V merkez:
              237,5 / 243,75 / 250 / 256,25 / 262,5 V); Kıb-Tek politikası iki değer kullanır, trafonun hangisinde
              olduğu bilinmez [Yorum, varsayım; gerçek standart Kıb-Tek'ten istenecek]. Üretici 1.3'te gerçek bara
              sürekli olduğu için politika bilgisi şöyle taklit edilir: model, gerçek değer ile bir kademe ötesindeki
              değerin (±6,25 V; gerçek ≥ 248 V ise aşağı, değilse yukarı) hangisi olduğunu bilmez, yarı yarıya;
              üstüne OG / ölçüm payı U(−1, +1) V [Yorum].
  S-inverter  trafoda en az bir panelli ev varsa (Kıb-Tek biliyor: `panel_sayisi`), o evin inverter kaydından:
              sakin an (05:00–06:30) ortancası → bara, gürültü U(−1, +1) V; öğlen salınımı → hat empedansı, gürültü
              ×e^U(ln 0,8; ln 1,2) (±%20), model-sapma çarpanı s yerine (empedans ölçüldü). Hangi evin verisi olduğu
              rastgele; ±%20 bunu da taşır [Yorum, sadeleştirme]. Panelli evi olmayan trafoda S0.
  S-ikisi     ikisi (panelli evi olan trafoda inverter, olmayanda kademe).
Ölçüler (`sinav.py faz3` tanımları + ADR-0016): yanlış yeşil (kapı), yeşil, sarı, kırmızı ve kırmızı kovasında
gerçekte bugün aşan (259 V) pay ≥ 0,5 − 2·√(0,25 ÷ n), kaç ev bandı; tüm trafolar ve panelli evi olanlar ayrı.

Etiket: gösterim; inverter verisi her panelli evden gelmez, pilotta ev sahibi izniyle.

Çalıştırma:
  python3 src/pv_acilma.py <şehir kökü> --aralik 1-10
"""
import argparse
import json
import math
import random
import statistics as st
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

_argv, sys.argv = sys.argv, sys.argv[:1]
import bilgi_degeri as bd  # noqa: E402
import kac_ev_olasilik as ko  # noqa: E402
import sinav  # noqa: E402  (Can'ın; yalnız okunur)
sys.argv = _argv

SENARYOLAR = {'S0': (), 'S-kademe': ('kademe',), 'S-inverter': ('inverter',), 'S-ikisi': ('kademe', 'inverter')}
KADEME_ADIM_V = 250 * 0.025              # 6,25 V
KADEME_PAY_V = 1.0                       # OG / ölçüm payı ±1 V [Yorum]
INV_BARA_V = 1.0                         # inverter sakin an → bara, ±1 V [Yorum: ölçüm doğruluğu + gece OG]
INV_EMPEDANS = 0.20                      # öğlen salınımı → hat empedansı ±%20 [Yorum]


def sehir_senaryo(is_):
    klasor, ad = Path(is_[0]), is_[1]
    bilgi = SENARYOLAR[ad]
    tohum = int(klasor.name.split('-')[1])
    trafolar, tahmin, cevap = bd.sehir_dosyalari(klasor)
    asil = (ko.ag_kur, ko.SAPMA_MU, ko.SAPMA_SIGMA)
    sonuc = {}
    try:
        for r in trafolar:
            tr = ko.trafo_satiri(r)
            no = r['trafo_no']
            frng = random.Random(f'acilma-{tohum}-{no}')
            panelli = int(tr['panel_sayisi']) > 0
            inv = 'inverter' in bilgi and panelli
            kad = 'kademe' in bilgi and not inv
            v_gercek = float(cevap[no]['v0_v'])
            diger = v_gercek - KADEME_ADIM_V if v_gercek >= 248.0 else v_gercek + KADEME_ADIM_V

            def ag_kur(tr_, rng, frng=frng, inv=inv, kad=kad, v_gercek=v_gercek, diger=diger):
                ag, evler = asil[0](tr_, rng)
                if kad:
                    ag['v0'] = (v_gercek if frng.random() < 0.5 else diger) + frng.uniform(-KADEME_PAY_V, KADEME_PAY_V)
                if inv:
                    ag['v0'] = v_gercek + frng.uniform(-INV_BARA_V, INV_BARA_V)
                    hedef = tr_['hat_boyu_max_m'] * math.exp(frng.uniform(math.log(1 - INV_EMPEDANS), math.log(1 + INV_EMPEDANS)))
                    simdi = max(f['boy'] for f in ag['feeders'])
                    k = hedef / simdi if simdi > 0 else 1.0
                    for f in ag['feeders']:
                        f['boy'], f['zs'], f['zn'] = f['boy'] * k, f['zs'] * k, f['zn'] * k
                return ag, evler

            ko.ag_kur = ag_kur
            ko.SAPMA_MU, ko.SAPMA_SIGMA = (0.0, 0.0) if inv else asil[1:]
            rng = random.Random(f'olasilik-{r["sehir"]}-{no}')       # resmi hesapla aynı tohum
            sonuc[no] = dict(bd.renk_sayilar(tr, tahmin[no], rng), panelli=panelli)
    finally:
        ko.ag_kur, ko.SAPMA_MU, ko.SAPMA_SIGMA = asil
    return str(klasor), ad, sonuc


def olc(satirlar):
    n = len(satirlar)
    kir = [x for x in satirlar if x['renk'] == 'kirmizi']
    yes = [x for x in satirlar if x['renk'] == 'yesil']
    kes = [x for x in satirlar if not x['tavan']]
    sinir = sinav.KIRMIZI_ASAN_MIN - 2 * math.sqrt(0.25 / len(kir)) if kir else float('nan')   # sinav.py faz3 ile aynı
    asan = sum(x['asar'] for x in kir) / len(kir) if kir else float('nan')
    return dict(n=n, dolu=sum(x['gercek'] == 0 for x in satirlar),
                yesil=len(yes), yanlis_yesil=sum(x['gercek'] == 0 for x in yes),
                sari=sum(x['renk'] == 'sari' for x in satirlar), kirmizi=len(kir),
                yanlis_kirmizi=sum(x['gercek'] >= 1 for x in kir), kirmizi_asan=asan, kirmizi_sinir=sinir,
                p10_alti=sum(x['gercek'] < x['kar'] for x in kes) / len(kes),
                p90_ustu=sum(x['gercek'] > x['iyi'] for x in kes) / len(kes),
                hata_orta=st.median(abs(x['orta'] - x['gercek']) for x in kes))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('kok')
    ap.add_argument('--aralik', default='1-10')
    ap.add_argument('--json')
    a = ap.parse_args()
    bas, son = (int(x) for x in a.aralik.split('-'))
    klasorler = [Path(a.kok) / f'sehir-{t:03d}' for t in range(bas, son + 1)]
    with ProcessPoolExecutor() as ex:
        sonuclar = {(k, ad): s for k, ad, s in ex.map(sehir_senaryo, [(str(k), ad) for ad in SENARYOLAR for k in klasorler])}
    fark = bd.s0_farki(klasorler, sonuclar)
    print(f'S0 ile resmi kac_ev.csv arasında renk farkı: {fark} trafo')
    tablo = {}
    for ad in SENARYOLAR:
        satir = bd.faz3_satirlari(klasorler, sonuclar, ad)
        tablo[ad] = dict(tum=olc(satir), panelli=olc([x for x in satir if x['panelli']]),
                         tip_yesil={t: sum(1 for x in satir if x['tip'] == t and x['renk'] == 'yesil')
                                    for t in sorted({x['tip'] for x in satir})},
                         tip_n={t: sum(1 for x in satir if x['tip'] == t) for t in sorted({x['tip'] for x in satir})})
    print(f'şehir {a.aralik} — gösterim (inverter verisi her panelli evden gelmez)')
    for alt in ('tum', 'panelli'):
        print(f'\n[{alt}] senaryo | yeşil | yanlış yeşil | sarı | kırmızı (yanlış) | kırmızıda gerçekte aşan (sınır) | kaç ev P10 altı / P90 üstü | hata orta')
        for ad in SENARYOLAR:
            o = tablo[ad][alt]
            print(f"{ad:10s} | {o['yesil']} (%{100 * o['yesil'] / o['n']:.0f}) | {o['yanlis_yesil']}/{o['yesil']} | %{100 * o['sari'] / o['n']:.0f} | "
                  f"{o['kirmizi']} ({o['yanlis_kirmizi']}) | %{100 * o['kirmizi_asan']:.0f} (%{100 * o['kirmizi_sinir']:.0f}) | "
                  f"%{100 * o['p10_alti']:.1f} / %{100 * o['p90_ustu']:.1f} | {o['hata_orta']:g}  [n {o['n']}, dolu {o['dolu']}]")
    print('\nyeşil, türe göre (n):')
    for ad in SENARYOLAR:
        print(f"{ad:10s} | " + ', '.join(f"{t} {tablo[ad]['tip_yesil'][t]}/{tablo[ad]['tip_n'][t]}" for t in tablo[ad]['tip_n']))
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(dict(aralik=a.aralik, s0_renk_farki=fark, tablo=tablo), fh, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
