#!/usr/bin/env python3
"""Kaç ev daha sığar (Faz 3): trafo başına ısıl ve gerilim payı, karamsar ve iyimser senaryo, renk.

Yöntem: docs/method/modeling.md bölüm 4–5; gerekçe ADR-0002 (gerilim), ADR-0005 (triyaj), ADR-0010 (yeşil kararı).
Okur: trafolar.csv (Kıb-Tek'in bildiği: kVA, hat sayısı ve boyu, kablo, abone ve panel sayıları) ve tahmin.csv
(Faz 2: öğlen en düşük yükün P10 / P90'ı ve güven). cevap_anahtari.csv'yi okumaz.
Yazar (sözleşme §6): kac_ev.csv. ADR-0011'den beri yedek yol: resmi hesap src/kac_ev_olasilik.py, o da pay sütunlarını
(isil_pay_kw, gerilim_pay_kw_*, sinir_karamsar, kural40_ev) bu dosyanın sehir_hesapla()'sından alır.

Fizik, şehir üreticisinin ev ev benzetimiyle (src/trafo_bos_kapasite.py solve) aynı empedanslar, tek denklemde:
  hat ucundaki gerilim = trafo çıkışı × (1 + OG yükselmesi) + trafo yükselmesi + hat yükselmesi
  trafo yükselmesi = r_trafo × faz akımı;   hat yükselmesi = (r_faz [+ r_nötr, tek faz]) × akım × mesafe
  akım = (panel kW × öğlen ışınımı − yük) ÷ gerilim
Her yeni ev (6,5 kW) bu gerilimi sabit bir miktar artırır; sınıra (259 V) kalan pay ÷ ev başına artış = kaç ev.
  karamsar: P10 yük, trafo çıkışı 250 V + OG öğlen yükselmesi, yeni paneller hattın UCUNDA ve tek fazda (UKPN:
            paneller uca toplanınca eşit yayılmış model yükselmeyi 2–4 kat az gösterdi; karar masası 16:27),
            mevcut panellerin yarısı aynı fazda, hat üstünde yük indirimi yok.
  iyimser:  P90 yük, 246 V, yeni ve mevcut paneller hat boyunun yarısında, dengeli üç faz.
Renk (ADR-0010; okuma karar masası 17:26): yeşil = karamsar en az 1 ev + marj (marj = payın %10'u, en az 1 ev)
ve güven yüksek; kırmızı = karamsar senaryoda BUGÜN, yeni panel olmadan, sınır aşılıyor ya da ısıl pay eksi
("önce ölç ya da güçlendir"); sarı = karamsar bugün aşmıyor ama bekleyen ev sığmıyor, ya da güven orta / düşük.

Çalıştırma:
  python3 src/kac_ev.py data/synthetic            # her şehir: kac_ev.csv
  python3 src/kac_ev.py data/synthetic --sehir 7
"""
import argparse
import csv
import math
import sys
from pathlib import Path

# Eski benzetim içe alınırken komut satırından tohum okuyor; bizim komut satırımız ona karışmasın.
_argv, sys.argv = sys.argv, sys.argv[:1]
import trafo_bos_kapasite as tb  # noqa: E402
sys.argv = _argv

KOK = Path(__file__).resolve().parent.parent
V_SINIR = tb.V_LIMIT                    # 259 V planlama sınırı
YENI_PANEL_KW = 6.5                     # bekleyen başvuruların orta değeri [ROADMAP Faz 1]
V_HESAP = 250.0                         # akım = güç ÷ bu gerilim (faz–nötr)
# Nisan öğleni en güçlü güneş: 2023–2025 Nisan'ında en yüksek saatlik eğik (30°, güney) ışınım 998 W/m²
# [Hesap: Open-Meteo Lefkoşa]; panel kW başına üretim = ışınım × kayıp katsayısı (benzetimle aynı, 0,82).
GUNES_KW_KWP = 1.0 * tb.PV_DERATE
R_NOTR = tb.CABLES['ABC70'][1].real     # nötr taşıyıcı 54,6 mm², Ω/km (iki kabloda aynı)

SENARYO = {
    # v0: trafo çıkışı (boşta faz gerilimi). Şartname 250 V; kademe bilinmiyor [ADR-0010, karar masası 16:27].
    # og: orta gerilimde öğlen güneşiyle yükselme, trafo çıkışına oran [Yorum: benzetimin OG çarpanı ~%0,8].
    # yuk: Faz 2 tahmininin hangi ucu. faz: mevcut panellerin en kötü fazdaki payı. yeni_tek_faz: yeni paneller
    # tek fazda (akım nötrden döner) ya da dengeli üç fazda. yeni_mesafe / mevcut_mesafe: hat boyuna oran.
    'karamsar': dict(v0=250.0, og=0.008, yuk='ogle_min_kw_p10', faz=0.5, yeni_tek_faz=True,
                     yeni_mesafe=1.0, mevcut_mesafe=2 / 3, hat_yuk_indirimi=False),
    'iyimser': dict(v0=246.0, og=0.0, yuk='ogle_min_kw_p90', faz=1 / 3, yeni_tek_faz=False,
                    yeni_mesafe=0.5, mevcut_mesafe=0.5, hat_yuk_indirimi=True),
    # beklenen: her belirsizliğin ortası; yalnız KIRMIZI_KURALI = 'beklenen_bugun' seçilirse renge girer.
    # v0 248 V (bandın ortası, UKPN tasarım varsayımı), mevcut panellerin %40'ı en kötü fazda, hat ortasında [Yorum].
    'beklenen': dict(v0=248.0, og=0.008, yuk='ogle_min_kw', faz=0.4, yeni_tek_faz=True,
                     yeni_mesafe=0.5, mevcut_mesafe=0.5, hat_yuk_indirimi=True),
}
# Kırmızı kuralı. ADR-0010 metni: "kırmızı = karamsar sınırı aşıyor". 'karamsar_yeni_ev': karamsar senaryoda (bekleyen
# panel hattın ucunda) 1 ev bile sığmıyor (metnin düz okuması). 'karamsar_bugun': karamsar senaryoda yeni panel olmadan
# bugün aşıyor (karar masası 17:26 seçti). 'beklenen_bugun': beklenen senaryoda bugün aşıyor. Ölçüler Faz 3 günlüğünde.
KIRMIZI_KURALI = 'karamsar_bugun'
MARJ_ORAN, MARJ_EV = 0.10, 1.0          # yeşil marjı: gerilim payının %10'u, en az 1 ev [ADR-0010, Yorum]
KURAL40 = 0.40                          # bugünkü kural: bağlı panel ≤ trafo gücünün %40'ı


def r_trafo(kva):
    """Trafo direnci, Ω: uk %4, X/R = 2 (şehir üreticisi ve eski benzetimle aynı) [varsayım]."""
    zb = 240.0 ** 2 / (kva * 1000 / 3)
    return 0.04 * zb / math.sqrt(5)


def senaryo_hesap(tr, yuk_kw, s):
    """Bir trafo, bir senaryo -> gerilim ve ısıl pay (kW), kaç ev (ondalıklı), bugünkü hat ucu gerilimi ve ev başına
    artış (V). tr: trafolar.csv satırı (dict, sayılar float). yuk_kw: öğlen en düşük yük (brüt)."""
    rt = r_trafo(tr['kva'])
    r_faz = tb.CABLES[tr['kablo']][0].real
    L = tr['hat_boyu_max_m'] / 1000
    # en uzun hattın trafodaki payı: karamsarda büyüğü (boya oranlı ya da eşit), iyimserde eşit [Yorum]
    pay_esit = 1 / max(tr['hat_sayisi'], 1)
    pay_boy = tr['hat_boyu_max_m'] / tr['hat_boyu_toplam_m'] if tr['hat_boyu_toplam_m'] > 0 else 1.0
    f = max(pay_esit, pay_boy) if s['yeni_tek_faz'] else pay_esit
    pv = tr['panel_kw'] * GUNES_KW_KWP                  # mevcut panellerin öğlen üretimi, kW

    if s['yeni_tek_faz']:
        # en kötü faz: mevcut panellerin s['faz'] kadarı bu fazda, yük üç faza eşit; akım nötrden döner
        i_tr = (s['faz'] * pv - yuk_kw / 3) * 1000 / V_HESAP
        i_hat = f * (s['faz'] * pv - (yuk_kw / 3 if s['hat_yuk_indirimi'] else 0)) * 1000 / V_HESAP
        r_hat = r_faz + R_NOTR
        taban = s['v0'] * (1 + s['og']) + rt * i_tr + r_hat * i_hat * s['mevcut_mesafe'] * L
        ev_basi = YENI_PANEL_KW * GUNES_KW_KWP * 1000 / V_HESAP * (rt + r_hat * s['yeni_mesafe'] * L)
    else:
        # dengeli üç faz: nötr akımı yok, faz başına üçte bir
        net = pv - yuk_kw
        i_tr = net / 3 * 1000 / V_HESAP
        i_hat = f * (net if s['hat_yuk_indirimi'] else pv) / 3 * 1000 / V_HESAP
        taban = s['v0'] * (1 + s['og']) + rt * i_tr + r_faz * i_hat * s['mevcut_mesafe'] * L
        ev_basi = YENI_PANEL_KW * GUNES_KW_KWP / 3 * 1000 / V_HESAP * (rt + r_faz * s['yeni_mesafe'] * L)

    ev_v = (V_SINIR - taban) / ev_basi                  # eksi = bugün zaten aşıyor
    gerilim_pay_kw = ev_v * YENI_PANEL_KW
    # ısıl: ters akış trafo gücünü aşmasın (güç katsayısı 1 sayıldı)
    isil_pay_kw = (tr['kva'] + yuk_kw - pv) / GUNES_KW_KWP
    return dict(gerilim_pay_kw=gerilim_pay_kw, isil_pay_kw=isil_pay_kw, ev_gerilim=ev_v,
                ev_isil=isil_pay_kw / YENI_PANEL_KW, bugun_v=taban, ev_basi_v=ev_basi)


def renk(ev_karamsar, guven, sonuc, kural=None):
    """ADR-0010. ev_karamsar: karamsar senaryoda sığan ev (ondalıklı, ısıl ve gerilimin küçüğü).
    sonuc: senaryo_hesap sonuçları (kırmızı kuralı 'bugun' ise bugünkü hat ucu gerilimi oradan)."""
    kural = kural or KIRMIZI_KURALI
    if kural == 'karamsar_yeni_ev':
        kirmizi = ev_karamsar < 1
    elif kural == 'karamsar_bugun':
        kirmizi = sonuc['karamsar']['bugun_v'] > V_SINIR or sonuc['karamsar']['ev_isil'] < 0
    else:
        kirmizi = sonuc['beklenen']['bugun_v'] > V_SINIR or sonuc['beklenen']['ev_isil'] < 0
    if kirmizi:
        return 'kirmizi'
    marj = max(MARJ_ORAN * ev_karamsar, MARJ_EV)
    if ev_karamsar - marj >= 1 and guven == 'yuksek':
        return 'yesil'
    return 'sari'


def sayi(x):
    return float(x) if x not in ('', None) else math.nan


SUTUNLAR = ['sehir', 'trafo_no', 'kac_ev_karamsar', 'kac_ev_iyimser', 'isil_pay_kw', 'gerilim_pay_kw_karamsar',
            'gerilim_pay_kw_iyimser', 'sinir_karamsar', 'renk', 'kural40_ev']


def sehir_hesapla(klasor):
    """Tek denklem: sözleşme §6 satırları (yazmadan). kac_ev_olasilik.py pay sütunlarını buradan alır."""
    with open(klasor / 'trafolar.csv', encoding='utf-8', newline='') as fh:
        trafolar = list(csv.DictReader(fh))
    with open(klasor / 'tahmin.csv', encoding='utf-8', newline='') as fh:
        tahmin = {r['trafo_no']: r for r in csv.DictReader(fh)}
    satirlar = []
    for r in trafolar:
        tr = {k: (r[k] if k in ('trafo_no', 'kablo', 'bolge', 'montaj') else sayi(r[k])) for k in r}
        t = tahmin[r['trafo_no']]
        olculen = sayi(t['ogle_min_kw_olculen'])
        aday = max(0, int(tr['abone_konut'] - tr['panel_sayisi']))   # panelsiz konut abone (başvurabilecek ev)
        sonuc = {}
        for ad, s in SENARYO.items():
            yuk = olculen if t['olculdu'] == '1' and not math.isnan(olculen) else sayi(t[s['yuk']])
            sonuc[ad] = senaryo_hesap(tr, yuk, s)
        k, i = sonuc['karamsar'], sonuc['iyimser']
        gk, ik, evk_v, evk_i = k['gerilim_pay_kw'], k['isil_pay_kw'], k['ev_gerilim'], k['ev_isil']
        gi, evi_v, evi_i = i['gerilim_pay_kw'], i['ev_gerilim'], i['ev_isil']
        ev_k = min(evk_v, evk_i)
        ev_i = min(evi_v, evi_i)
        satirlar.append(dict(
            sehir=int(tr['sehir']), trafo_no=r['trafo_no'],
            kac_ev_karamsar=min(aday, max(0, math.floor(ev_k))),
            kac_ev_iyimser=min(aday, max(0, math.floor(ev_i))),
            isil_pay_kw=round(ik, 2),
            gerilim_pay_kw_karamsar=round(gk, 2), gerilim_pay_kw_iyimser=round(gi, 2),
            sinir_karamsar='gerilim' if evk_v <= evk_i else 'isil',
            renk=renk(ev_k, t['guven'], sonuc),
            kural40_ev=max(0, math.floor((KURAL40 * tr['kva'] - tr['panel_kw']) / YENI_PANEL_KW))))
    return satirlar


def csv_yaz(yol, sutunlar, satirlar):
    with open(yol, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=sutunlar, lineterminator='\n')
        w.writeheader()
        w.writerows(satirlar)


def sehir_calistir(klasor):
    """Yedek yol (ADR-0011): tek denklemle kac_ev.csv. Resmi hesap kac_ev_olasilik.py."""
    satirlar = sehir_hesapla(klasor)
    csv_yaz(klasor / 'kac_ev.csv', SUTUNLAR, satirlar)
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
    if not klasorler:
        raise SystemExit(f'{a.kok} altında tahmin.csv olan şehir yok (önce: python3 src/sablon.py {a.kok})')
    for k in klasorler:
        s = sehir_calistir(k)
        renkler = {c: sum(1 for x in s if x['renk'] == c) for c in ('yesil', 'sari', 'kirmizi')}
        print(f"{k.name}: {renkler}; karamsar ortanca {sorted(x['kac_ev_karamsar'] for x in s)[len(s) // 2]} ev, "
              f"iyimser {sorted(x['kac_ev_iyimser'] for x in s)[len(s) // 2]} ev")


if __name__ == '__main__':
    main()
