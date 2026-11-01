#!/usr/bin/env python3
"""Bilginin değeri denemesi (Faz 3, karar masası 19:44): bir bilinmeyen bilinseydi renkler ne kadar düzelirdi.

Olasılıklı hesap (`kac_ev_olasilik.py`, resmi hesap, ADR-0011) bu betikte değişmez. Her çekilişte resmi kod ağı
kendi rastgelesiyle kurar; bu betik ardından bilinen bilgiyi o ağa yerleştirir ve benzetim öyle koşar. Rastgele
akış senaryolar arasında aynı kalsın diye bilgi, resmi çekilişten SONRA ve ayrı bir rastgeleyle eklenir.

Senaryolar (bilginin kaynağı günlükte):
  S0  bugün: resmi hesap (kac_ev.csv ile birebir aynı renk çıkmalı; betiğin doğruluk sınaması)
  S1  bara gerilimi bilinir: trafonun boşta çıkış gerilimi = cevap anahtarındaki v0_v (öğlen OG değişimi yine
      bilinmez, −%0,4…+%0,8 çekilir)
  S2  panelli evlerin yeri bilinir: her panelli ev gerçek hattında ve hattaki gerçek göreli sırasında (hat boyu
      ve panelsiz abonelerin yeri yine bilinmez); bu durumda "panelli evler yüksüz kolda" bilinmeyeni de kalkar
  S3  her abonenin fazı bilinir (panelli abone dahil; yeri bilinmez): sınıf sınıf gerçek fazlar abonelere
  S4  hepsi (S1 + S2 + S3; panelli evin gerçek yeri gerçek fazıyla)
  S5  ek, teşhis için: S4 + trafonun öğlen en düşük yükü bilinir (cevap anahtarı ogle_min_kw; ölçülmüş trafo gibi,
      güven yüksek). Sarının ne kadarının yükten geldiğini ayırır.
  S6  ek, teşhis için: ağın tamamı bilinir (hat kaydı: hat boyları, her abonenin hattı, sırası, fazı, panel gücü;
      bara) + öğlen yükü. Bilinmeyen yalnız sıradaki başvurunun kimden geleceği, öğlen OG değişimi ve yükün
      abonelere dağılımı kalır: sarının bilgiyle inemeyecek tabanı.
Sarı ayrıca sebebine göre dökülür (cevap anahtarıyla): gerçekte dolu; gerçekte ilk iki başvuru her sırada sığmıyor
(kac_ev_gercek_min < 2); güven yüksek değil (kural gereği yeşil olamaz); "yeşil olabilirdi" (geri kalan).
Gerçek ağ şehir üreticisinin kendi tohumuyla yeniden kurulur (`sehir_uret.sehir_kur`, aynı çağrı sırası); 80
trafoda trafolar.csv ve cevap anahtarıyla birebir tuttuğu sınandı. Bu yalnız deney içindir: resmi hesap cevap
anahtarını ve üreticiyi okumaz.

Etiket: ÜST SINIR (kusursuz bilgi, farazi şehir, gösterim). Gerçek ölçüm gürültülü olur.
Ayar yok: eşikler (kırmızı 0,5, yeşil 0,98) ve aralıklar resmi hesabınki.

Çalıştırma:
  python3 src/bilgi_degeri.py data/synthetic --aralik 1-10
  python3 src/bilgi_degeri.py data/synthetic --aralik 11-20     # sınav: her yöntem değişikliğinden sonra bir kez
"""
import argparse
import json
import random
import statistics as st
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

_argv, sys.argv = sys.argv, sys.argv[:1]
import kac_ev_olasilik as ko  # noqa: E402
import kac_ev as ke  # noqa: E402
import sehir_uret as su  # noqa: E402
import sinav  # noqa: E402  (Can'ın; yalnız okunur: faz3 tanımları ve okuyucu)
sys.argv = _argv

KOK = Path(__file__).resolve().parent.parent
SENARYOLAR = {
    'S0': (),
    'S1': ('bara',),
    'S2': ('yer',),
    'S3': ('faz',),
    'S4': ('bara', 'yer', 'faz'),
    'S5': ('bara', 'yer', 'faz', 'yuk'),
    'S6': ('ag', 'yuk'),
}
SINIF_SUTUN = {s: v[1] for s, v in su.SINIFLAR.items()}      # üretici sınıfı -> Kıb-Tek tarife sütunu


def sehir_dosyalari(klasor):
    """(trafolar, tahmin {trafo: satır}, cevap {trafo: satır}); `sinav.py`'nin okuyucusuyla."""
    return (sinav._csv(klasor / 'trafolar.csv'), {r['trafo_no']: r for r in sinav._csv(klasor / 'tahmin.csv')},
            {r['trafo_no']: r for r in sinav._csv(klasor / 'cevap_anahtari.csv')})


def renk_sayilar(tr, t, rng):
    """Resmi çekilişle (`kac_ev_olasilik`) renk ve kaç ev. Bu iki eski deneme (bilginin değeri, PV açılma) rengi
    ADR-0019 öncesi güven şartlı kuralla verir (çıktıları kayıttakiyle birebir kalsın); bu yüzden S0 bugünkü resmi
    `kac_ev.csv` ile (güven şartsız) birebir değildir."""
    p_bugun, p_iki, kac = ko.cekilis_ozeti(tr, ko.trafo_cek(tr, t, rng))
    return dict(renk=ko.renk_ver(p_bugun, p_iki, t['guven'], guven_sarti=True), kar=ko.nicel(kac, 0.1),
                orta=ko.nicel(kac, 0.5), iyi=ko.nicel(kac, 0.9), p_bugun=p_bugun, p_iki=p_iki)


def faz3_satirlari(klasorler, sonuclar, ad):
    """`sinav.py` faz3 kümesi (kac_ev_aday > 0); her trafoya gerçek kaç ev (dolu = 0), tavan, en az, bugün aşar mı, tip."""
    satir = []
    for k in klasorler:
        for c in sinav._csv(k / 'cevap_anahtari.csv'):
            if int(c['kac_ev_aday']) == 0:
                continue
            satir.append(dict(sonuclar[(str(k), ad)][c['trafo_no']], sehir=k.name, gercek=int(c['kac_ev_gercek']),
                              tavan=int(c['kac_ev_tavan']), gercek_min=int(c['kac_ev_gercek_min']),
                              asar=float(c['v_max_bugun_v']) > ke.V_SINIR, tip=c['tip']))
    return satir


def s0_farki(klasorler, sonuclar):
    """S0 doğruluk sınaması: resmi kac_ev.csv ile renk farkı olan trafo sayısı."""
    return sum(sonuclar[(str(k), 'S0')][r['trafo_no']]['renk'] != r['renk']
               for k in klasorler for r in sinav._csv(k / 'kac_ev.csv'))


def gercek_ag(tohum):
    """Şehir üreticisinin ağı, aynı tohum ve aynı çağrı sırasıyla (sehir_uret.sehir_uret'in başı)."""
    rng = random.Random(f'yapi-{tohum}')
    _, tepe_orani, _ = su.egrileri_yukle()
    siniflar = list(su.SINIFLAR)
    kayma_ust = rng.uniform(30, 60)
    ayar = dict(tuketim_carpani={s: round(rng.uniform(0.8, 1.2), 3) for s in siniflar},
                saat_kaymasi_dk={s: 5 * round(rng.uniform(-kayma_ust, kayma_ust) / 5) for s in siniflar},
                panel_yayginligi=round(rng.uniform(0.03, 0.25), 3), mahalle_sigma=su.MAHALLE_SIGMA)
    rng.choice(su.HAVA_YILLARI)
    rng.randint(1, 30 - su.GUN_SAYISI + 1)
    trafolar, _, _ = su.sehir_kur(rng, 40, ayar, tepe_orani, su.kiyi_segmentleri())
    return {tr['no']: tr for tr in trafolar}


def _segment_yenile(ag, zc, znc):
    for f in ag['feeders']:
        seg = f['boy'] / 1000 / len(f['houses'])
        f['zs'], f['zn'] = zc * seg, znc * seg
        for k, h in enumerate(f['houses']):
            h['yer'] = (k + 1) / len(f['houses'])


def panel_yerlestir(ag, evler, gercek, kablo, panel_kw_ev):
    """S2: model ağındaki panelleri sil, her gerçek panelli evi gerçek hattına ve göreli sırasına koy.
    Hatlar boy sırasıyla eşlenir (gerçek en uzun hat = modelin en uzun hattı). Döner: {model ev id: gerçek ev}."""
    for h in evler:
        h['pv'] = 0.0
    g_hat = sorted(range(len(gercek['feeders'])), key=lambda j: -gercek['feeders'][j]['boy'])
    m_hat = sorted(ag['feeders'], key=lambda f: -f['boy'])
    esle = {gj: m_hat[i % len(m_hat)] for i, gj in enumerate(g_hat)}
    eslesen, tasindi = {}, False
    for gj, gf in enumerate(gercek['feeders']):
        n = len(gf['houses'])
        for k, gh in enumerate(gf['houses']):
            if gh['pv'] <= 0:
                continue
            hedef = (k + 1) / n
            mf = esle[gj]
            bos = [h for h in mf['houses'] if h['sinif'] == 'abone_konut' and h['id'] not in eslesen]
            if bos:
                h = min(bos, key=lambda x: abs(x['yer'] - hedef))
            else:      # o hatta boş konut yok: başka hattan en yakın sıradaki konutu taşı
                aday = [(f, x) for f in ag['feeders'] for x in f['houses']
                        if x['sinif'] == 'abone_konut' and x['id'] not in eslesen]
                if not aday:
                    continue
                f0, h = min(aday, key=lambda fx: abs(fx[1]['yer'] - hedef))
                f0['houses'].remove(h)
                i = max(0, min(len(mf['houses']), round(hedef * (len(mf['houses']) + 1)) - 1))
                mf['houses'].insert(i, h)
                tasindi = True
            h['pv'] = panel_kw_ev
            eslesen[h['id']] = gh
    if tasindi:                # hat başına ev sayısı değişti: boş hat düşer, parça empedansı ve sıra yeniden
        ag['feeders'] = [f for f in ag['feeders'] if f['houses']]
        zc, znc = ko.tb.CABLES[kablo]
        _segment_yenile(ag, zc, znc)
    return eslesen


def tam_ag(ag, gercek):
    """S6: modelin ağı yerine gerçek ağ (aynı empedans hesabı; üretici ve model aynı formülü kullanır)."""
    evler, feeders = [], []
    for gf in gercek['feeders']:
        n = len(gf['houses'])
        f = dict(zs=gf['zs'], zn=gf['zn'], boy=gf['boy'], houses=[])
        for k, g in enumerate(gf['houses']):
            h = dict(id=len(evler), sinif=SINIF_SUTUN[g['sinif']], ph=g['ph'], pv=g['pv'], yer=(k + 1) / n)
            f['houses'].append(h)
            evler.append(h)
        feeders.append(f)
    ag.update(feeders=feeders, v0=gercek['v0'], zt=gercek['zt'])
    return evler


def faz_ata(evler, gercek, eslesen, frng):
    """S3: her abonenin gerçek fazı. Yeri bilinen panelli ev kendi gerçek fazını alır; diğerleri sınıf sınıf
    (konutta panelli / panelsiz ayrı) gerçek fazların karıştırılmış listesinden."""
    havuz = {}
    eslesen_gercek = {id(g) for g in eslesen.values()}
    for f in gercek['feeders']:
        for g in f['houses']:
            if id(g) in eslesen_gercek:
                continue
            havuz.setdefault((SINIF_SUTUN[g['sinif']], g['pv'] > 0), []).append(g['ph'])
    for v in havuz.values():
        frng.shuffle(v)
    for h in evler:
        if h['id'] in eslesen:
            h['ph'] = eslesen[h['id']]['ph']
            continue
        anahtar = (h['sinif'], h['pv'] > 0)
        if havuz.get(anahtar):
            h['ph'] = havuz[anahtar].pop()


def sehir_senaryo(is_):
    """(şehir klasörü, senaryo) -> trafo başına renk ve sayılar."""
    klasor, ad = Path(is_[0]), is_[1]
    bilgi = SENARYOLAR[ad]
    tohum = int(klasor.name.split('-')[1])
    trafolar, tahmin, cevap = sehir_dosyalari(klasor)
    gercek = gercek_ag(tohum) if {'yer', 'faz', 'ag'} & set(bilgi) else {}
    asil_ag_kur, asil_kol = ko.ag_kur, ko.KOL_P
    if 'yer' in bilgi:
        ko.KOL_P = 0.0          # panellerin yeri biliniyorsa "yüksüz kolda mı" da bilinir (çekiliş akışı aynı kalır)
    sonuc = {}
    try:
        for r in trafolar:
            tr = ko.trafo_satiri(r)
            no = r['trafo_no']
            frng = random.Random(f'bilgi-{tohum}-{no}')
            n_panel = int(tr['panel_sayisi'])

            def ag_kur(tr_, rng, no=no, frng=frng, n_panel=n_panel):
                ag, evler = asil_ag_kur(tr_, rng)
                if 'ag' in bilgi:
                    return ag, tam_ag(ag, gercek[no])
                if 'bara' in bilgi:
                    ag['v0'] = float(cevap[no]['v0_v'])
                eslesen = {}
                if 'yer' in bilgi and n_panel:
                    eslesen = panel_yerlestir(ag, evler, gercek[no], tr_['kablo'], tr_['panel_kw'] / n_panel)
                if 'faz' in bilgi:
                    faz_ata(evler, gercek[no], eslesen, frng)
                return ag, evler

            ko.ag_kur = ag_kur
            rng = random.Random(f'olasilik-{r["sehir"]}-{no}')       # resmi hesapla aynı tohum
            t = tahmin[no]
            if 'yuk' in bilgi:
                t = dict(t, olculdu='1', ogle_min_kw_olculen=cevap[no]['ogle_min_kw'], guven='yuksek')
            sonuc[no] = dict(renk_sayilar(tr, t, rng), guven=t['guven'])
    finally:                   # işçi süreç sıradaki senaryoya temiz geçsin
        ko.ag_kur, ko.KOL_P = asil_ag_kur, asil_kol
    return str(klasor), ad, sonuc


def olc(klasorler, sonuclar, ad):
    """sinav.py faz3 ile aynı tanımlar: küme kac_ev_aday > 0; dolu = kac_ev_gercek = 0."""
    satir = faz3_satirlari(klasorler, sonuclar, ad)
    n = len(satir)
    kir = [x for x in satir if x['renk'] == 'kirmizi']
    yes = [x for x in satir if x['renk'] == 'yesil']
    dolu = [x for x in satir if x['gercek'] == 0]
    kes = [x for x in satir if not x['tavan']]
    sari = [x for x in satir if x['renk'] == 'sari']
    s_dolu = [x for x in sari if x['gercek'] == 0]
    s_az = [x for x in sari if x['gercek'] >= 1 and x['gercek_min'] < 2]
    s_guven = [x for x in sari if x['gercek_min'] >= 2 and x['guven'] != 'yuksek']
    s_olurdu = [x for x in sari if x['gercek_min'] >= 2 and x['guven'] == 'yuksek']
    return dict(
        sari_dolu=len(s_dolu), sari_iki_sigmaz=len(s_az), sari_guven=len(s_guven), sari_yesil_olabilirdi=len(s_olurdu),
        n=n, dolu=len(dolu),
        kirmizi=len(kir), yanlis_kirmizi=sum(x['gercek'] >= 1 for x in kir),
        dolu_kirmizi=sum(x['gercek'] == 0 for x in kir),
        yesil=len(yes), yanlis_yesil=sum(x['gercek'] == 0 for x in yes),
        sari=sum(x['renk'] == 'sari' for x in satir),
        hata_orta=st.median(abs(x['orta'] - x['gercek']) for x in kes),
        hata_karamsar=st.median(abs(x['kar'] - x['gercek']) for x in kes),
        kapsama=sum(x['kar'] <= x['gercek'] <= x['iyi'] for x in kes) / len(kes),
    )


def yuzde(a, b):
    return f'%{100 * a / b:.0f} ({a}/{b})' if b else '— (0/0)'


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('kok', nargs='?', default=str(KOK / 'data' / 'synthetic'))
    ap.add_argument('--aralik', default='1-10')
    ap.add_argument('--json', help='sonuçları bu dosyaya da yaz')
    a = ap.parse_args()
    bas, son = (int(x) for x in a.aralik.split('-'))
    klasorler = [Path(a.kok) / f'sehir-{t:03d}' for t in range(bas, son + 1)]
    isler = [(str(k), ad) for ad in SENARYOLAR for k in klasorler]
    with ProcessPoolExecutor() as ex:
        sonuclar = {(k, ad): s for k, ad, s in ex.map(sehir_senaryo, isler)}

    fark = s0_farki(klasorler, sonuclar)       # S0 doğruluk sınaması (renk_sayilar'daki nota bak)
    print(f'S0 ile resmi kac_ev.csv arasında renk farkı: {fark} trafo')

    tablo = {}
    print(f'şehir {a.aralik} — ÜST SINIR (kusursuz bilgi, farazi şehir, gösterim)')
    print('senaryo | yanlış kırmızı | kırmızı payı | dolu yakalanan | sarı | yeşil | yanlış yeşil | kaç ev hatası '
          'orta / karamsar | aralık kapsaması')
    for ad, bilgi in SENARYOLAR.items():
        o = olc(klasorler, sonuclar, ad)
        tablo[ad] = o
        print(f'{ad} {"+".join(bilgi) or "bugün"} | {yuzde(o["yanlis_kirmizi"], o["kirmizi"])} | '
              f'{yuzde(o["kirmizi"], o["n"])} | {o["dolu_kirmizi"]}/{o["dolu"]} | {yuzde(o["sari"], o["n"])} | '
              f'{yuzde(o["yesil"], o["n"])} | {o["yanlis_yesil"]}/{o["yesil"]} | '
              f'{o["hata_orta"]:g} / {o["hata_karamsar"]:g} | %{100 * o["kapsama"]:.0f}')
    print('sarının sebebi (cevap anahtarıyla): gerçekte dolu | ilk iki her sırada sığmıyor | güven yüksek değil | '
          'yeşil olabilirdi')
    for ad, o in tablo.items():
        print(f'{ad} | {o["sari_dolu"]} | {o["sari_iki_sigmaz"]} | {o["sari_guven"]} | {o["sari_yesil_olabilirdi"]} '
              f'(sarı {o["sari"]}/{o["n"]})')
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(dict(aralik=a.aralik, s0_renk_farki=fark, tablo=tablo), fh, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
