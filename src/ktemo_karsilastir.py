"""KTEMO çatı PV'sinin gerçek üretimi ↔ modelin panel formülü (etkin güç × eğik ışınım ÷ 1000 × 0,82).

Kullanım: python3 src/ktemo_karsilastir.py <ktemo gunluk> <open-meteo klasörü> <pvgis csv> <çıktı klasörü>
Veri: data/raw/ktemo-solarweb, open-meteo-lefkosa, pvgis-lefkosa (KAYNAK.txt); sonuç docs/log/2026-11-03-volkan-ktemo-pv-karsilastirma.md.
Her şey UTC saatine çevrilir; anahtar = gerçek ölçümün saati [hh:00, hh+1:00) UTC.
Tahminciler:
  om_dogru   Open-Meteo eğik ışınım, saat sütunu sabit UTC+2 okunur (doğrusu; DST boşluğu yok)
  om_model   Open-Meteo, modelin bugünkü okuması (yaz saatli yerel saat sanılıyor)
  pvgis_G    PVGIS-SARAH3 (uydu) eğik ışınım, aynı formül
  pvgis_P    PVGIS'in kendi 1 kWp güç hesabı (sıcaklık etkisi dahil)
Tek katsayı (etkin güç) ayar yıllarında (2018–2022) enerji eşitliğiyle bulunur; sınav 2023 (PVGIS 2023'te bitiyor),
Open-Meteo için ayrıca 2023–2026.
"""
import csv, glob, json, os, sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

GUN, OM, PVGIS, CIKTI = sys.argv[1:5]
UTC = timezone.utc
DERATE = 0.82
ACIK = 700          # W/m² eğik: açık gök öğlen saati


def gercek_oku():
    saat = defaultdict(list)
    for yol in sorted(glob.glob(os.path.join(GUN, '*.json'))):
        try:
            j = json.load(open(yol, encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            continue
        toplam = defaultdict(float)
        for s in j['settings']['series']:
            if str(s.get('id', '')).startswith('FromGen'):
                for t, v in s['data']:
                    if v is not None:
                        toplam[t] += v
        for t, v in toplam.items():
            u = datetime.fromtimestamp(t / 1000, UTC)
            saat[u.replace(minute=0, second=0, microsecond=0)].append(v)
    return {k: sum(v) / len(v) for k, v in saat.items() if len(v) >= 11}


def om_oku(model_okumasi):
    """{UTC saat başı: (eğik W/m², sıcaklık)}; satır etiketi L = [L−1 sa, L) ortalaması."""
    yerel = ZoneInfo('Europe/Nicosia')
    out = {}
    for yol in sorted(glob.glob(os.path.join(OM, '*.csv'))):
        satirlar = list(csv.reader(open(yol, encoding='utf-8')))
        b = next(i for i, r in enumerate(satirlar) if r and r[0] == 'time')
        gi = next(i for i, x in enumerate(satirlar[b]) if x.startswith('global_tilted'))
        si = next(i for i, x in enumerate(satirlar[b]) if x.startswith('temperature_2m'))
        for r in satirlar[b + 1:]:
            if not r or r[gi] == '':
                continue
            L = datetime.fromisoformat(r[0])
            if model_okumasi:
                bas = (L - timedelta(hours=1)).replace(tzinfo=yerel).astimezone(UTC)
            else:
                bas = (L - timedelta(hours=3)).replace(tzinfo=UTC)
            out[bas] = (float(r[gi]), float(r[si]))
    return out


def pvgis_oku():
    """{UTC saat başı: (eğik W/m², sıcaklık, P W/kWp)}; hh:09 anlık değerlerden hh:30'a ara değer."""
    ham = {}
    for r in csv.reader(open(PVGIS, encoding='utf-8')):
        if len(r) < 9 or not r[0][:8].isdigit():
            continue
        t = datetime.strptime(r[0], '%Y%m%d:%H%M').replace(tzinfo=UTC)
        ham[t.replace(minute=0)] = (float(r[2]) + float(r[3]) + float(r[4]), float(r[6]), float(r[1]))
    out = {}
    w = 21 / 60   # :09 → :30
    for k, a in ham.items():
        b = ham.get(k + timedelta(hours=1))
        if b:
            out[k] = tuple(x * (1 - w) + y * w for x, y in zip(a, b))
    return out


def degerlendir(ad, gercek, tahmin, sicak, ayar_yil, sinav_yil):
    """tahmin: {saat: bir büyüklük}; tek katsayı ayarda enerji eşitliğiyle."""
    ortak = sorted(set(gercek) & set(tahmin))
    # çevrim dışı / arızalı gün: açık saatte gerçek ≈ 0
    kotu = {k.date() for k in ortak if tahmin[k] > 300 and gercek[k] < 50}
    rs = [(k, gercek[k], tahmin[k], sicak.get(k)) for k in ortak if k.date() not in kotu]
    ayar = [r for r in rs if r[0].year in ayar_yil]
    sinav = [r for r in rs if r[0].year in sinav_yil]
    if not ayar or not sinav:
        return {'ad': ad, 'yetersiz': True}
    c = sum(r[1] for r in ayar) / sum(r[2] for r in ayar)
    m = lambda r: c * r[2]
    q = lambda a, p: sorted(a)[min(len(a) - 1, int(p * len(a)))]
    gunduz = [abs(r[1] - m(r)) / m(r) for r in sinav if r[2] > 100]
    acik = [abs(r[1] - m(r)) / m(r) for r in sinav if r[2] > ACIK]
    gun, ay = defaultdict(lambda: [0.0, 0.0]), defaultdict(lambda: [0.0, 0.0])
    for r in sinav:
        gun[r[0].date()][0] += r[1]; gun[r[0].date()][1] += m(r)
        ay[(r[0].year, r[0].month)][0] += r[1]; ay[(r[0].year, r[0].month)][1] += m(r)
    gh = [abs(a - b) / b for a, b in gun.values() if b > 0]
    ah = [abs(a - b) / b for a, b in ay.values() if b > 0]
    mevsim = {}
    for a in range(1, 13):
        x = [r for r in rs if r[0].month == a and r[2] > ACIK]
        if x:
            mevsim[a] = [round(sum(r[1] for r in x) / sum(m(r) for r in x), 3),
                         round(sum(r[3] for r in x if r[3] is not None) / len(x), 1), len(x)]
    out = {'ad': ad, 'katsayi': round(c, 4), 'gun_atilan': len(kotu), 'saat_ayar': len(ayar), 'saat_sinav': len(sinav),
           'saatlik_hata': [round(q(gunduz, .5), 3), round(q(gunduz, .9), 3)],
           'acik_saat_hata': [round(q(acik, .5), 3), round(q(acik, .9), 3)],
           'gunluk_hata': [round(q(gh, .5), 3), round(q(gh, .9), 3)],
           'aylik_hata': [round(q(ah, .5), 3), round(q(ah, .9), 3), len(ah)],
           'aya_gore_gercek_bolu_tahmin_acik': mevsim}
    nis = [r for r in sinav if r[0].month == 4 and r[2] > ACIK]
    if nis:
        out['nisan_acik_gercek_bolu_tahmin'] = round(sum(r[1] for r in nis) / sum(m(r) for r in nis), 3)
    return out


def main():
    gercek = gercek_oku()
    om_d, om_m, pv = om_oku(False), om_oku(True), pvgis_oku()
    sic_om = {k: v[1] for k, v in om_d.items()}
    sic_pv = {k: v[1] for k, v in pv.items()}
    ayar = set(range(2018, 2023))
    rapor = {'gercek_saat': len(gercek), 'gercek_ilk': str(min(gercek)), 'gercek_son': str(max(gercek)), 'sonuc': []}
    for ad, tah, sic, sinav in [
        ('om_dogru_2023', {k: v[0] * DERATE for k, v in om_d.items()}, sic_om, {2023}),
        ('om_model_2023', {k: v[0] * DERATE for k, v in om_m.items()}, sic_om, {2023}),
        ('pvgis_G_2023', {k: v[0] * DERATE for k, v in pv.items()}, sic_pv, {2023}),
        ('pvgis_P_2023', {k: v[2] for k, v in pv.items()}, sic_pv, {2023}),
        ('om_dogru_2023_2026', {k: v[0] * DERATE for k, v in om_d.items()}, sic_om, {2023, 2024, 2025, 2026}),
        ('om_model_2023_2026', {k: v[0] * DERATE for k, v in om_m.items()}, sic_om, {2023, 2024, 2025, 2026}),
    ]:
        rapor['sonuc'].append(degerlendir(ad, gercek, tah, sic, ayar, sinav))
    # yıllık: gerçek ÷ eğik ışınım (PVGIS, Open-Meteo) — yaşlanma izi
    yil = defaultdict(lambda: [0.0, 0.0, 0.0, 0])
    for k, v in gercek.items():
        if k in om_d:
            yil[k.year][0] += v; yil[k.year][2] += om_d[k][0]; yil[k.year][3] += 1
            yil[k.year][1] += pv[k][0] if k in pv else 0.0
    rapor['yil_gercek_bolu_isinim'] = {y: {'pvgis': round(a / b, 4) if b else None, 'om': round(a / c, 4) if c else None,
                                          'saat': n} for y, (a, b, c, n) in sorted(yil.items())}
    os.makedirs(CIKTI, exist_ok=True)
    json.dump(rapor, open(os.path.join(CIKTI, 'ktemo_karsilastirma.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1, default=str)
    print(json.dumps(rapor, ensure_ascii=False, indent=1, default=str))


main()
