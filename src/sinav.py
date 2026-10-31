#!/usr/bin/env python3
"""Geçme sınavı ölçüleri: üretilen şehirleri ROADMAP eşiklerine göre ölçer.

Modeli ya da üreteci yazan sınavı yazmaz (CONTRIBUTING); bu dosya Can'ın. Okuduğu dosyalar ve sütunlar
docs/data/tablo-bicimi.md sözleşmesinde.

Çalıştırma: python3 src/sinav.py faz1 data/synthetic
Her madde için GEÇTİ / KALDI ve rakam yazar; hepsi geçerse çıkış kodu 0.
"""
import csv
import json
import statistics as st
import sys
from collections import Counter
from pathlib import Path

TIPLER = ['sehir_konutu', 'koy', 'carsi', 'otel', 'sanayi', 'sulama', 'yurt']
V_SINIR = 259.0                # planlama sınırı (en az bir trafo bunu aşmalı: yöntemin görecek şeyi var)
V_ALT = 216.0                  # bunun altı = benzetim bozuk
TIP_SEHIR_MIN = 3              # her şehirde her tipten
TIP_TOPLAM_MIN = 60            # bütün şehirlerde her tipten (20 şehir için)
SURE_MAX_SN = 60.0


def _csv(yol):
    with open(yol, encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


def sehirleri_oku(kok):
    """kok altındaki sehir-NNN klasörleri. (sayılan, atlanan) listeleri döner.
    Atlanan: profil_kaynagi = yer_tutucu ya da eksik dosya; (klasör adı, neden)."""
    sayilan, atlanan = [], []
    for k in sorted(Path(kok).glob('sehir-*')):
        if not k.is_dir():
            continue
        eksik = [d for d in ('trafolar.csv', 'cevap_anahtari.csv', 'ayar.json') if not (k / d).exists()]
        if eksik:
            atlanan.append((k.name, 'eksik dosya: ' + ', '.join(eksik)))
            continue
        with open(k / 'ayar.json', encoding='utf-8') as fh:
            ayar = json.load(fh)
        if ayar.get('profil_kaynagi') == 'yer_tutucu':
            atlanan.append((k.name, 'profil_kaynagi = yer_tutucu'))
            continue
        sayilan.append(dict(ad=k.name, ayar=ayar,
                            trafolar=_csv(k / 'trafolar.csv'),
                            cevap=_csv(k / 'cevap_anahtari.csv')))
    return sayilan, atlanan


def _madde(sonuc, gecti, ad, ayrinti):
    sonuc.append((gecti, ad, ayrinti))


def faz1(sehirler):
    """ROADMAP Faz 1 geçme sınavı. (maddeler, bilgi satırları) döner."""
    m, bilgi = [], []

    # 1. Her şehirde 7 tipin her biri en az 3 trafo.
    eksikler = []
    toplam = Counter()
    for s in sehirler:
        say = Counter(r['tip'] for r in s['cevap'])
        toplam.update(say)
        az = {t: say.get(t, 0) for t in TIPLER if say.get(t, 0) < TIP_SEHIR_MIN}
        if az:
            eksikler.append(f"{s['ad']} {az}")
    _madde(m, not eksikler, f'her şehirde her tipten ≥ {TIP_SEHIR_MIN} trafo',
           f'{len(sehirler) - len(eksikler)}/{len(sehirler)} şehir' + (f"; eksik: {'; '.join(eksikler[:5])}" if eksikler else ''))

    # 2. Bütün şehirlerde her tipten en az 60 trafo.
    en_az = min(TIPLER, key=lambda t: toplam.get(t, 0))
    _madde(m, all(toplam.get(t, 0) >= TIP_TOPLAM_MIN for t in TIPLER),
           f'bütün şehirlerde her tipten ≥ {TIP_TOPLAM_MIN} trafo',
           f'en az {en_az} {toplam.get(en_az, 0)}; ' + ', '.join(f'{t} {toplam.get(t, 0)}' for t in TIPLER))
    bilinmeyen = set(toplam) - set(TIPLER)
    if bilinmeyen:
        bilgi.append(f'UYARI: sözleşmede olmayan tip adı: {sorted(bilinmeyen)}')

    # 3. Her şehirde en az bir trafo bugün 259 V üstü.
    asan = {s['ad']: sum(float(r['v_max_bugun_v']) > V_SINIR for r in s['cevap']) for s in sehirler}
    sifir = [a for a, n in asan.items() if n == 0]
    _madde(m, not sifir, f'her şehirde en az bir trafoda v_max_bugun_v > {V_SINIR:g} V',
           f'{len(sehirler) - len(sifir)}/{len(sehirler)} şehir; toplam {sum(asan.values())} trafo'
           + (f"; hiç aşmayan: {', '.join(sifir[:5])}" if sifir else ''))

    # 4. Hiçbir trafoda 216 V altı yok.
    v_min = [(float(r['v_min_bugun_v']), s['ad'], r['trafo_no']) for s in sehirler for r in s['cevap']]
    en_dusuk = min(v_min)
    alti = [x for x in v_min if x[0] < V_ALT]
    _madde(m, not alti, f'hiçbir trafoda v_min_bugun_v < {V_ALT:g} V',
           f'en düşük {en_dusuk[0]:.1f} V ({en_dusuk[1]} {en_dusuk[2]}); altında {len(alti)} trafo')

    # 5. Üretim süresi.
    sureler = [(s['ayar'].get('sure_sn'), s['ad']) for s in sehirler]
    yok = [a for v, a in sureler if v is None]
    var = [(float(v), a) for v, a in sureler if v is not None]
    ayrinti = []
    if var:
        en_uzun = max(var)
        ayrinti.append(f'en uzun {en_uzun[0]:.1f} sn ({en_uzun[1]}), ortanca {st.median(v for v, _ in var):.1f} sn')
    if yok:
        ayrinti.append(f"ayar.json'da sure_sn yok: {len(yok)} şehir")
    _madde(m, not yok and max(var)[0] <= SURE_MAX_SN, f'üretim süresi ≤ {SURE_MAX_SN:g} sn', '; '.join(ayrinti))

    # Bilgi (eşiksiz).
    bilgi.append('tip başına ogle_min_kw ortancası (kW): ' + ', '.join(
        f"{t} {st.median(float(r['ogle_min_kw']) for s in sehirler for r in s['cevap'] if r['tip'] == t):.2f}"
        for t in TIPLER if toplam.get(t)))
    kac = [int(r['kac_ev_gercek']) for s in sehirler for r in s['cevap']]
    q = st.quantiles(kac, n=4) if len(kac) > 1 else [kac[0]] * 3
    bilgi.append(f'kac_ev_gercek: en az {min(kac)}, çeyrekler {q[0]:g} / {q[1]:g} / {q[2]:g}, en çok {max(kac)}; '
                 f'sıfır olan {sum(k == 0 for k in kac)}/{len(kac)}')
    sinir = Counter(r['kac_ev_sinir'] for s in sehirler for r in s['cevap'])
    bilgi.append('kac_ev_sinir: ' + ', '.join(f'{k} {sinir.get(k, 0)}' for k in ('gerilim', 'isil', 'yok')))
    tavan = sum(int(r['kac_ev_tavan']) for s in sehirler for r in s['cevap'])
    bilgi.append(f'kac_ev_tavan = 1 oranı: {tavan / len(kac):.3f} ({tavan}/{len(kac)})')
    return m, bilgi


def main():
    if len(sys.argv) < 3 or sys.argv[1] != 'faz1':
        sys.exit('Kullanım: python3 src/sinav.py faz1 <şehir kökü, ör. data/synthetic>')
    sehirler, atlanan = sehirleri_oku(sys.argv[2])
    for ad, neden in atlanan:
        print(f'UYARI: {ad} sayılmadı ({neden})')
    if not sehirler:
        sys.exit(f'{sys.argv[2]} altında sınava girecek şehir yok.')
    trafo = sum(len(s['cevap']) for s in sehirler)
    print(f'Faz 1 geçme sınavı: {len(sehirler)} şehir, {trafo} trafo\n')
    maddeler, bilgi = faz1(sehirler)
    for gecti, ad, ayrinti in maddeler:
        print(f"[{'GEÇTİ' if gecti else 'KALDI'}] {ad}: {ayrinti}")
    print('\nBilgi:')
    for satir in bilgi:
        print('  ' + satir)
    sys.exit(0 if all(g for g, _, _ in maddeler) else 1)


if __name__ == '__main__':
    main()
