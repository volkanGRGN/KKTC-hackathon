#!/usr/bin/env python3
"""Kaç ev, olasılıklı (Faz 3 denemesi): bilinmeyenler aralıktan çekilir, ev ev benzetim her çekilişte koşar.

Tek denklemli `kac_ev.py` bilmediği her şey için tek bir "en kötü" değer seçer; Faz 3 varsayım envanteri
(docs/log/2026-10-31-volkan-faz3-varsayimlar.md) bu değerlerin kırmızıyı yalnız kaydırdığını, sıralamayı
düzeltmediğini gösterdi. Burada her trafo için ağ, Kıb-Tek'in bildikleriyle (abone sayıları, hat sayısı ve
boyu, kablo, kVA, panel sayısı ve gücü) yeniden kurulur; bilinmeyenler her çekilişte aralığından çekilir ve
eski benzetimin `solve()`'u koşar:
  - bara gerilimi, öğlen orta gerilim değişimi, abonelerin hattı ve sırası, fazı, panellerin hangi evde
    olduğu, trafonun öğlen yükü (Faz 2 bandından) ve abonelere dağılımı.
Aralıklar ölçümden ya da envanterdeki gerçek veri karşılaştırmasından; şehir üreticisinin kendi değerlerinden
değil (ADR-0009). Bu yüzden üreticiyle bilerek aynı değil: paneller çekilişlerin üçte birinde hattın ucuna
toplanır (UKPN: 6 hattın 2'si), yoksa düz; büyük aboneler yarı yarıya trafoya yakın ya da rastgele (veri yok);
OG değişimi UKPN ile eski benzetim arası. İngiltere geri-testinden sonra: hat boyu ×0,6–1,6 belirsiz, çekilişlerin
altıda birinde panelli evler yüksüz ayrı bir kolda.

Çıktı her çekilişte: bugün (yeni panelsiz, öğlen güneşi + en düşük yük) sınır aşılıyor mu; bekleyen panelsiz
konutlar rastgele sırayla 6,5 kW alırsa kaçı sığar (sığmayan atlanır, cevap anahtarıyla aynı tanım); ilk iki
başvuru sığıyor mu. Renk (ADR-0010 olasılıkla):
  kırmızı = bugün aşma olasılığı ≥ KIRMIZI_P;  yeşil = ilk iki başvurunun sığma olasılığı ≥ YESIL_P (marj = 1 ev;
  ADR-0019: "güven yüksek" şartı kalktı, kalibre yük bandı yeter; YESIL_GUVEN_SARTI ile geri açılır);  diğerleri sarı.
Panel katmanı "güvenli uçlar" (ADR-0017, Muhittin 4 madde 1; `pv_uc`): yeşil = yukarıdaki yeşil; `dolu_bayrak` = bugün
  aşma olasılığı ≥ BAYRAK_P ("büyük olasılıkla dolu", ret değil); arası `bos` (renksiz, "başvuruda bakılır").
Konum payı (ADR-0015 m. 4; yalnız analiz, `kac_ev.csv`'ye yazılmaz — karar masası 01:01; `guvenli_uc.py --konum`):
  tek başvurunun (6,5 kW) hattı ve hattaki yeri biliniyor, gerisi aynı çekilişlerle; bütün hatlarda o yerdeki ev için
  sığma olasılığı ≥ YESIL_P ve güven yüksekse o yer "büyük olasılıkla evet". Renksiz trafoda neredeyse hep 0 çıktı.
Sayılar: kac_ev_karamsar = çekilişlerin P10'u, kac_ev_iyimser = P90'ı, kac_ev_orta = ortanca.

Öğlen güneşi saat ve sıcaklıkla hizalı (8 Kasım; üretici 1.7'nin saat düzeltmesinden sonra): eskiden tam güneş
(1 kW/kWp × PV_DERATE) öğlenin en düşük yüküyle aynı anda sayılıyordu. Yerel saatle Nisan güneşi 12:30'da tepe yapıyor,
öğlen penceresinin (11:00–14:00) en düşük yükü çoğu trafoda pencerenin başında; ikisi aynı anda gelmiyor. Şimdi her
gündüz adımında güneş = Nisan açık gün zarfı (`pv_hava.gunes_zarfi`, Open-Meteo Lefkoşa 2018–2022, yerel saat, sıcaklıklı;
dünyanın hava yılları 2023–2025 kullanılmaz) ve yük = çekilen öğlen en düşük yük × trafonun arketip biçimi (`arketipler.csv`,
`sablon.py`; öğlenin en düşüğüne bölünmüş, iş günü ve tatilin küçüğü). Her çözümde iki an değerlendirilir: toplam net
vermenin en büyük olduğu adım ve güneşin tepesi (hat sonundaki panelli evin en kötü anı ikincisi olabilir); kötüsü sayılır.
Çekilişler (rastgele akış) değişmez. `--eski-gunes` eski kural; `trafo_cek(..., bicim=None)` çağıran eski betikler
(`olcum_sirasi`, `bilgi_degeri`, `pv_acilma`, `basvuru`, `konum_payi`) eski kuralda kalır.

Faz 3'ün resmi hesabı (ADR-0011, karar masası 18:46).
Okur: trafolar.csv, tahmin.csv. cevap_anahtari.csv'yi okumaz.
Yazar: kac_ev.csv, sözleşme §6 (1.3): karamsar / iyimser / renk bu hesaptan; isil_pay_kw, gerilim_pay_kw_*,
sinir_karamsar, kural40_ev tek denklemden (kac_ev.py); ek sütunlar p_bugun_asar, p_iki_ev_sigar, kac_ev_orta;
1.4 adayı: sonda pv_uc (ADR-0017).

Çalıştırma:
  python3 src/kac_ev_olasilik.py data/synthetic --sehir 3
  python3 src/kac_ev_olasilik.py data/synthetic           # 20 şehir, ~1,5 dakika; her şehirde kac_ev.csv
"""
import argparse
import csv
import math
import random
import sys
from pathlib import Path

_argv, sys.argv = sys.argv, sys.argv[:1]
import trafo_bos_kapasite as tb  # noqa: E402
sys.argv = _argv
import kac_ev as ke  # noqa: E402
import pv_hava  # noqa: E402

KOK = Path(__file__).resolve().parent.parent
OGLE = range(132, 168)                  # 11:00–14:00 (sözleşme), 5 dakikalık adım
ADIM = 288
# Nisan açık gün zarfı için hava: Open-Meteo Lefkoşa 2018–2022 (KTEMO ayar yılları; dünyanın 2023–2025'i değil) [Hesap: zarfın
# tepesi 1,011 kW/kWp 12:30'da, 11:00'de 0,901; pv_hava.gunes_zarfi]
GUNES_DOSYALARI = [KOK / 'data' / 'raw' / 'open-meteo-lefkosa' / 'lefkosa_saatlik_2018_2022.csv']
ESKI_GUNES = False                      # True: eski kural (tam güneş + öğlen en düşük yük aynı anda); --eski-gunes
_ZARF = {}
CEKILIS = 40
KIRMIZI_P = 0.5                         # bugün aşma olasılığı bunun üstündeyse kırmızı [Yorum]
YESIL_P = 0.98                          # ilk iki başvurunun sığma olasılığı (canlı bütçe %2, ADR-0010)
BAYRAK_P = 0.7                          # "büyük olasılıkla dolu" bayrağı (ADR-0017; ilkeden, sınava bakılmadan)
YESIL_GUVEN_SARTI = False               # ADR-0019: yeşil / hemen evet için yük güveni yüksek şartı kalktı; bant
                                        # kalibrasyonu bozulursa (gerçek < P10 nominal %10 + tolerans dışı) True

ABONE = ['abone_konut', 'abone_ticari1', 'abone_ticari2', 'abone_turizm', 'abone_sanayi1', 'abone_sanayi2',
         'abone_su_motoru']
# Abone başına yıllık MWh [Hesap: Kıb-Tek 2023 istatistiği, sınıfın yıllık tüketimi ÷ abone sayısı; sablon.py ile aynı
# kaynak, data/raw/kibtek-istatistik/]: yalnız trafonun yükünü abonelere bölmek için.
MWH = {'abone_konut': 648494 / 175577, 'abone_ticari1': 210978 / 20950, 'abone_ticari2': 169496 / 494,
       'abone_turizm': 215147 / 171, 'abone_sanayi1': 22391 / 1227, 'abone_sanayi2': 95996 / 352,
       'abone_su_motoru': 51256 / 3250}

# Aralıklar (Faz 3 varsayım envanteri)
V0 = (244.0, 252.0)                     # bara gerilimi, düz [karar masası 16:27 bandı; Kıbrıs BULAMADIM]
OG = (-0.004, 0.008)                    # öğlen OG değişimi: UKPN −%0,4 (öğlen bara geceden ~1 V düşük) ile eski
#                                         benzetimin +%0,8'i arası [Yorum]
FAZ_SAPMA = {'kentsel': 0.30, 'turistik': 0.30, 'sanayi': 0.30, 'kirsal': 0.50}  # tek fazlı faz ağırlığı 1 ± U(0, x):
#                                         UKPN dengesizlik kentsel P84 %30, kırsal ~%50 [Hesap, PR #11]
UC_FAZ = {'abone_konut': (0.0, 0.2), 'abone_ticari1': (0.0, 0.4)}   # üç fazlı abone payı; diğerleri üç faz [Yorum]
PANEL_UCTA_P = 2 / 6                    # paneller hattın ucuna toplanmış [Hesap: UKPN 6 hat ucu evden 2'si, PR #11]
BUYUK_BASTA_P = 0.5                     # büyük aboneler trafoya yakın [Yorum: veri yok, iki durum eşit]
BUYUK = {'abone_ticari2', 'abone_turizm', 'abone_sanayi2'}
# Gerçek veri geri-testinden (İngiltere 6 hat, docs/log/2026-10-31-volkan-faz3-ukpn-geritest.md): hat boyu kesin
# sayılınca ölçülen yükselme 6'nın 4'ünde kapsandı, boy belirsiz sayılınca 5'inde; kaçan Bancroft'ta ev, yüksüz ama
# panelli bir koldaydı. İkisi de aralığa girer. KOL_P aynı 6 hattan (1/6), o hatlarda sınanamaz.
BOY_BELIRSIZ = 0.47                     # hat boyu × e^U(−0,47, 0,47) ≈ ×0,6–1,6 [Yorum; kayıt BULAMADIM]
KOL_P = 1 / 6                           # panelli evler yüksüz bir kolda [Hesap: UKPN 6 hattın 1'i]
BIREY_SIGMA = 0.3                       # abone yükünün ortalamadan farkı, log-normal [Yorum]
# Faz 7 (karar masası 21:32; ADR-0013 madde 3): gerilim tarafı GERÇEĞE karşı. Model-sapma çarpanı s = exp(N(μ, σ)),
# çekiliş başına, hat empedanslarını (zs, zn) çarpar; trafo empedansına dokunmaz (UKPN ölçümü baradan eve yükselme).
# Parametreler İngiltere'nin 6 hattından (src/ukpn_olasilik.py, faz bilinmeyen, hat boyu ±0,47, 60 çekiliş;
# src/kalibrasyon.py ingiltere): her hatta δ = −ortalama ln(model ÷ ölçülen); μ = ortalama δ, σ² = var(δ) − ortalama
# iç varyans (moment tahmini). Sonuç: 6 hatta P98 kapsaması 5/6 → 6/6, bir-dışarıda da 6/6. 6/6 için en küçük σ 0,12
# (μ sabit); aralık σ 0,12–0,41, burada moment tahmini. "6 hatla ayarlandı, pilotta yeniden." Farazi şehre bakılarak
# seçilmedi. Not: KOL_P aynı 6 hattan (Bancroft); s de Bancroft'u içeriyor, ikisi birlikte temkinli yönde çift sayar.
SAPMA_MU = 0.172                        # [Hesap: UKPN 2014, 6 hat]
SAPMA_SIGMA = 0.414                     # [Hesap: UKPN 2014, 6 hat; aralık 0,12–0,41]
Q_ORAN = 0.33                           # yükün reaktif gücü (benzetimle aynı)


def ag_kur(tr, rng):
    """Bir çekiliş: trafo sözlüğü (solve için) + ev listesi (sınıf, panel)."""
    kva = tr['kva']
    zb = 240.0 ** 2 / (kva * 1000 / 3)
    rt = 0.04 * zb / math.sqrt(5)
    n_hat = max(1, int(tr['hat_sayisi']))
    carpan = math.exp(rng.uniform(-BOY_BELIRSIZ, BOY_BELIRSIZ))
    lmax = tr['hat_boyu_max_m'] * carpan
    kalan = max(0.0, tr['hat_boyu_toplam_m'] * carpan - lmax)
    boylar = [lmax]
    if n_hat > 1:
        w = [rng.random() + 0.1 for _ in range(n_hat - 1)]
        boylar += [min(lmax, max(20.0, kalan * x / sum(w))) for x in w]
    aboneler = [c for c in ABONE for _ in range(int(tr[c]))]
    rng.shuffle(aboneler)
    hatlar = [[] for _ in boylar]
    for c in aboneler:
        hatlar[rng.randrange(n_hat)].append(c)
    if rng.random() < BUYUK_BASTA_P:
        for hat in hatlar:
            hat.sort(key=lambda c: c not in BUYUK)
    d = rng.uniform(0, FAZ_SAPMA.get(tr['bolge'], 0.3))
    fw = [1 + rng.uniform(-d, d) for _ in range(3)]
    uc = {c: rng.uniform(*UC_FAZ[c]) for c in UC_FAZ}
    zc, znc = tb.CABLES[tr['kablo']]
    ag = dict(v0=rng.uniform(*V0), zt=complex(rt, 2 * rt), kva=kva, feeders=[])
    evler = []
    for boy, hat in zip(boylar, hatlar):
        if not hat:
            continue
        seg = boy / 1000 / len(hat)
        f = dict(zs=zc * seg, zn=znc * seg, houses=[], boy=boy)
        for k, c in enumerate(hat):
            uc_faz = rng.random() < uc.get(c, 1.0)
            h = dict(id=len(evler), sinif=c, ph=3 if uc_faz else rng.choices([0, 1, 2], weights=fw)[0], pv=0.0,
                     yer=(k + 1) / len(hat))
            f['houses'].append(h)
            evler.append(h)
        ag['feeders'].append(f)
    konut = [h for h in evler if h['sinif'] == 'abone_konut']
    n_panel = min(int(tr['panel_sayisi']), len(konut))
    if n_panel:
        if rng.random() < PANEL_UCTA_P:          # uca toplanmış: hat üstündeki yerin karesiyle ağırlıklı çekiliş
            havuz, secilen = konut[:], []
            for _ in range(n_panel):
                h = rng.choices(havuz, weights=[x['yer'] ** 2 for x in havuz])[0]
                havuz.remove(h)
                secilen.append(h)
        else:
            secilen = rng.sample(konut, n_panel)
        for h in secilen:
            h['pv'] = tr['panel_kw'] / n_panel
        if rng.random() < KOL_P:                 # panelli evler yüksüz bir kolda: trafodan en uzun hat boyunda ayrı kol
            for f in ag['feeders']:
                f['houses'] = [h for h in f['houses'] if h['pv'] == 0]
            rng.shuffle(secilen)
            ag['feeders'].append(dict(houses=secilen, boy=lmax))
            ag['feeders'] = [f for f in ag['feeders'] if f['houses']]
            for f in ag['feeders']:
                seg = f['boy'] / 1000 / len(f['houses'])
                f['zs'], f['zn'] = zc * seg, znc * seg
    return ag, evler


def yuk_dagit(evler, toplam, rng):
    """Trafonun öğlen yükünü abonelere: tarife enerjisi × kişisel fark, toplamı korunur."""
    w = [MWH[h['sinif']] * rng.lognormvariate(-BIREY_SIGMA ** 2 / 2, BIREY_SIGMA) for h in evler]
    s = sum(w) or 1.0
    return {h['id']: toplam * x / s for h, x in zip(evler, w)}


def durum(ag, evler, yuk, ek, m, warm=None, iters=6, an=None):
    """an = (adım, güneş kW/kWp, yük çarpanı); None: eski kural (tam güneş, öğlen en düşük yük)."""
    gunes, c = (ke.GUNES_KW_KWP, 1.0) if an is None else (an[1] * tb.PV_DERATE, an[2])
    net = {h['id']: ((yuk[h['id']] * c - (h['pv'] + ek.get(h['id'], 0.0)) * gunes) * 1000,
                     yuk[h['id']] * c * Q_ORAN * 1000) for h in evler}
    V, s_tr = tb.solve(ag, net, m, warm, iters=iters)
    return V, max(tb.house_voltages(ag, V).values()), s_tr


def gunes_zarfi():
    """Nisan açık gün zarfı (288 adım, kW/kWp) ve gündüz adımları; dosya yoksa None (eski kural)."""
    if 'z' not in _ZARF:
        yollar = [y for y in GUNES_DOSYALARI if y.exists()]
        z = pv_hava.gunes_zarfi(yollar) if yollar else None
        if z is None:
            print('UYARI: Open-Meteo 2018–2022 dosyası yok; öğlen güneşi eski kuralla (tam güneş, en düşük yük aynı anda)')
        _ZARF['z'] = z
        _ZARF['gunduz'] = [i for i in range(ADIM) if z and z[i] > 0.01]
        _ZARF['tepe'] = max(range(ADIM), key=lambda i: z[i]) if z else None
    return _ZARF['z']


def yuk_bicimleri(klasor):
    """arketipler.csv (sablon.py) -> {arketip: 288 çarpan}: arketip eğrisi ÷ öğlen (11:00–14:00) en düşüğü; iş günü ve
    tatilin her adımda küçüğü (temkinli: düşük yük → çok verme). Dosya yoksa {}."""
    yol = klasor / 'arketipler.csv'
    if not yol.exists():
        return {}
    egri = {}
    with open(yol, encoding='utf-8', newline='') as fh:
        for r in csv.DictReader(fh):
            egri.setdefault((r['arketip'], r['gun_turu']), [0.0] * ADIM)[int(r['adim'])] = float(r['oran'])
    out = {}
    for (a, _), e in egri.items():
        alt = min(e[i] for i in OGLE)
        if alt <= 0:
            continue
        b = [x / alt for x in e]
        out[a] = b if a not in out else [min(x, y) for x, y in zip(out[a], b)]
    return out


def anlar(p_kw, l_kw, bicim):
    """Değerlendirilecek anlar: toplam net vermenin (panel kWp × güneş × PV_DERATE − öğlen en düşük yük × biçim) en büyük
    olduğu gündüz adımı ve güneşin tepesi. bicim None ya da zarf yoksa [None] (eski kural)."""
    z = gunes_zarfi() if bicim is not None else None
    if z is None:
        return [None]
    t1 = max(_ZARF['gunduz'], key=lambda i: p_kw * tb.PV_DERATE * z[i] - l_kw * bicim[i])
    return [(i, z[i], bicim[i]) for i in dict.fromkeys((t1, _ZARF['tepe']))]


def durumlar(ag, evler, yuk, ek, m, an_listesi, onceki=None):
    """Her anda durum(); (anlara göre V, en yüksek ev gerilimi, en büyük trafo yükü). onceki: anlara göre ılık başlangıç
    (kopyası verilir; solve() yerinde değiştirir). Tek an ve None ise eski durum() çağrısıyla birebir."""
    Vs, vmax, s_tr = {}, 0.0, 0.0
    for an in an_listesi:
        k = None if an is None else an[0]
        bas = onceki.get(k) if onceki else None
        if bas is not None:
            V, v, s = durum(ag, evler, yuk, ek, m, [[list(x) for x in hat] for hat in bas], iters=4, an=an)
        else:
            V, v, s = durum(ag, evler, yuk, ek, m, an=an)
        Vs[k], vmax, s_tr = V, max(vmax, v), max(s_tr, s)
    return Vs, vmax, s_tr


def trafo_satiri(r):
    """trafolar.csv satırı → hesap sözlüğü (metin alanlar dışında sayı)."""
    return {k: (r[k] if k in ('trafo_no', 'kablo', 'bolge', 'montaj') else ke.sayi(r[k])) for k in r}


def yuk_bandi(t):
    """Trafonun öğlen yükü için Faz 2 bandından log-normal (mu, sd): P10 ve P90 ±1,2816 sd."""
    p10, p90 = ke.sayi(t['ogle_min_kw_p10']), ke.sayi(t['ogle_min_kw_p90'])
    mu = (math.log(max(p10, 0.01)) + math.log(max(p90, 0.01))) / 2
    sd = max(1e-6, (math.log(max(p90, 0.01)) - math.log(max(p10, 0.01))) / (2 * 1.2816))
    return mu, sd


def cekilis_ozeti(tr, s):
    """trafo_cek çıktısı → (bugün aşma olasılığı, ilk iki sığma olasılığı, aday sayısıyla kesilmiş kaç ev listesi)."""
    aday = max(0, int(tr['abone_konut'] - tr['panel_sayisi']))
    return sum(b for b, _, _ in s) / len(s), sum(i for _, _, i in s) / len(s), [min(k, aday) for _, k, _ in s]


def renk_ver(p_bugun, p_iki, guven, guven_sarti=None):
    """Harita rengi (ADR-0010 / 0011 / 0019). guven_sarti None ise YESIL_GUVEN_SARTI; eski deneme betikleri True."""
    sart = YESIL_GUVEN_SARTI if guven_sarti is None else guven_sarti
    if p_bugun >= KIRMIZI_P:
        return 'kirmizi'
    if p_iki >= YESIL_P and (not sart or guven == 'yuksek'):
        return 'yesil'
    return 'sari'


def trafo_cek(tr, t, rng, v0=None, vrng=None, yuk=None, bicim=None):
    """Bir trafo için CEKILIS kez: (bugün aşar mı, kaç ev, ilk iki sığar mı) listesi. Ölçüm denemeleri için
    (`olcum_sirasi.py`): v0 = callable(vrng) bara gerilimini, yuk = ölçülen öğlen yükünü verir; bilgi ayrı akıştan,
    resmi çekilişlerin akışı değişmez. bicim: trafonun yük biçimi (`yuk_bicimleri`); None ise eski öğlen kuralı."""
    olculen = ke.sayi(t['ogle_min_kw_olculen'])
    mu, sd = yuk_bandi(t)
    sonuc = []
    srng = random.Random(f'sapma-{tr["sehir"]}-{tr["trafo_no"]}')   # ayrı akış: diğer çekilişler v1 ile aynı kalır
    for _ in range(CEKILIS):
        ag, evler = ag_kur(tr, rng)
        if v0 is not None:
            ag['v0'] = v0(vrng)
        sapma = math.exp(srng.gauss(SAPMA_MU, SAPMA_SIGMA)) if (SAPMA_MU or SAPMA_SIGMA) else 1.0
        for f in ag['feeders']:
            f['zs'], f['zn'] = f['zs'] * sapma, f['zn'] * sapma
        if not evler:
            sonuc.append((False, 0, True))
            continue
        if t['olculdu'] == '1' and not math.isnan(olculen):
            toplam = olculen
        else:
            toplam = math.exp(rng.gauss(mu, sd))
        if yuk is not None:
            toplam = yuk
        yk = yuk_dagit(evler, toplam, rng)
        m = 1 + rng.uniform(*OG)
        p0 = sum(h['pv'] for h in evler)
        Vs, vmax, s_tr = durumlar(ag, evler, yk, {}, m, anlar(p0, toplam, bicim))
        bugun = vmax > ke.V_SINIR or s_tr > ag['kva']
        adaylar = [h['id'] for h in evler if h['sinif'] == 'abone_konut' and h['pv'] == 0]
        if not adaylar:                       # başvuru ticari aboneden de gelebilir: renk için sanal aday
            adaylar = [h['id'] for h in evler if h['pv'] == 0]
        rng.shuffle(adaylar)
        ek, kabul, ilk_iki = {}, 0, not bugun
        if not bugun:
            for j, hid in enumerate(adaylar):
                ek[hid] = ke.YENI_PANEL_KW
                an_listesi = anlar(p0 + sum(ek.values()), toplam, bicim)
                V2s, vmax2, s2 = durumlar(ag, evler, yk, ek, m, an_listesi, Vs)
                if vmax2 > ke.V_SINIR or s2 > ag['kva']:
                    del ek[hid]
                    if j < 2:
                        ilk_iki = False
                else:
                    kabul += 1
                    Vs.update(V2s)
        sonuc.append((bugun, kabul, ilk_iki))
    return sonuc


KONUM_Y = [k / 10 for k in range(1, 11)]      # başvuranın hattaki yeri, hat boyunun payı


def konum_payi(tr, t, rng):
    """Hattın ilk x'i (ADR-0015 m. 4): x'e kadar her yerdeki evden tek başvuru, bütün hatlarda ve bütün çekilişlerde
    sığıyor (P ≥ YESIL_P; güven şartı yeşilinkiyle aynı, ADR-0019'dan beri yok); haritanın bugün aşma olasılığı da
    ≤ 1 − YESIL_P olmalı (çağıran bakar). Yer = (hattaki sıra + 1) ÷ hattaki ev; y için o hattın y'yi geçen ilk evi
    (temkinli). Yalnız panelli evlerden oluşan kol (çekilişlerin bir kısmı) atlanır: başvuran panelsiz."""
    if YESIL_GUVEN_SARTI and t['guven'] != 'yuksek':                 # ADR-0019: şart yeşilinkiyle birlikte kalktı
        return 0.0
    olculen = ke.sayi(t['ogle_min_kw_olculen'])
    mu, sd = yuk_bandi(t)
    srng = random.Random(f'konum-sapma-{tr["sehir"]}-{tr["trafo_no"]}')
    x = 1.0
    for _ in range(CEKILIS):
        ag, evler = ag_kur(tr, rng)
        sapma = math.exp(srng.gauss(SAPMA_MU, SAPMA_SIGMA)) if (SAPMA_MU or SAPMA_SIGMA) else 1.0
        for f in ag['feeders']:
            f['zs'], f['zn'] = f['zs'] * sapma, f['zn'] * sapma
        if not evler:
            continue
        if t['olculdu'] == '1' and not math.isnan(olculen):
            toplam = olculen
        else:
            toplam = math.exp(rng.gauss(mu, sd))
        yuk = yuk_dagit(evler, toplam, rng)
        m = 1 + rng.uniform(*OG)
        V, vmax, s_tr = durum(ag, evler, yuk, {}, m)
        if vmax > ke.V_SINIR or s_tr > ag['kva']:
            return 0.0
        for f in ag['feeders']:
            n = len(f['houses'])
            if all(h['pv'] > 0 for h in f['houses']):
                continue
            for y in KONUM_Y:
                if y > x + 1e-9:
                    break
                h = f['houses'][min(n - 1, max(0, math.ceil(y * n - 1e-9) - 1))]
                _, v2, s2 = durum(ag, evler, yuk, {h['id']: ke.YENI_PANEL_KW}, m,
                                  [[list(v) for v in hat] for hat in V], iters=4)
                if v2 > ke.V_SINIR or s2 > ag['kva']:
                    x = round(y - 0.1, 1)
                    break
            if x <= 0:
                return 0.0
    return x


def nicel(x, q):
    x = sorted(x)
    return x[min(len(x) - 1, max(0, int(round(q * (len(x) - 1)))))]


def sehir_calistir(klasor):
    with open(klasor / 'trafolar.csv', encoding='utf-8', newline='') as fh:
        trafolar = list(csv.DictReader(fh))
    with open(klasor / 'tahmin.csv', encoding='utf-8', newline='') as fh:
        tahmin = {r['trafo_no']: r for r in csv.DictReader(fh)}
    tek = {x['trafo_no']: x for x in ke.sehir_hesapla(klasor)}     # pay sütunları ve %40 kuralı tek denklemden
    bicimler = None if ESKI_GUNES or gunes_zarfi() is None else yuk_bicimleri(klasor)
    satirlar = []
    for r in trafolar:
        tr = trafo_satiri(r)
        t = tahmin[r['trafo_no']]
        rng = random.Random(f'olasilik-{r["sehir"]}-{r["trafo_no"]}')
        bicim = None if bicimler is None else bicimler.get(t['arketip'], [1.0] * ADIM)   # arketip yoksa düz yük
        p_bugun, p_iki, kac = cekilis_ozeti(tr, trafo_cek(tr, t, rng, bicim=bicim))
        renk = renk_ver(p_bugun, p_iki, t['guven'])
        satirlar.append({**tek[r['trafo_no']], 'kac_ev_karamsar': nicel(kac, 0.1), 'kac_ev_iyimser': nicel(kac, 0.9),
                         'renk': renk, 'p_bugun_asar': round(p_bugun, 3), 'p_iki_ev_sigar': round(p_iki, 3),
                         'kac_ev_orta': nicel(kac, 0.5), 'pv_uc': pv_uc(renk, p_bugun)})
    ke.csv_yaz(klasor / 'kac_ev.csv', SUTUNLAR, satirlar)
    return satirlar


def pv_uc(renk, p_bugun):
    """Panel katmanının üç durumu (ADR-0017): yeşil / büyük olasılıkla dolu bayrağı / renksiz."""
    if renk == 'yesil':
        return 'yesil'
    return 'dolu_bayrak' if p_bugun >= BAYRAK_P else 'bos'


SUTUNLAR = ke.SUTUNLAR + ['p_bugun_asar', 'p_iki_ev_sigar', 'kac_ev_orta', 'pv_uc']   # sözleşme §6, 1.3; pv_uc 1.4 adayı


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('kok', nargs='?', default=str(KOK / 'data' / 'synthetic'))
    ap.add_argument('--sehir', type=int, help='yalnız bu tohum')
    ap.add_argument('--eski-gunes', action='store_true',
                    help='eski öğlen kuralı: tam güneş ve öğlen en düşük yük aynı anda (8 Kasım öncesi)')
    a = ap.parse_args()
    global ESKI_GUNES
    ESKI_GUNES = a.eski_gunes
    klasorler = sorted(k for k in Path(a.kok).glob('sehir-*')
                       if (k / 'trafolar.csv').exists() and (k / 'tahmin.csv').exists())
    if a.sehir is not None:
        klasorler = [k for k in klasorler if k.name == f'sehir-{a.sehir:03d}']
    for k in klasorler:
        s = sehir_calistir(k)
        renkler = {c: sum(1 for x in s if x['renk'] == c) for c in ('yesil', 'sari', 'kirmizi')}
        uclar = {c: sum(1 for x in s if x['pv_uc'] == c) for c in ('yesil', 'dolu_bayrak', 'bos')}
        print(f'{k.name}: {renkler}; panel katmanı {uclar}')


if __name__ == '__main__':
    main()
