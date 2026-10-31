#!/usr/bin/env python3
"""Tek panelli evin inverter gerilim kaydı (bir hafta): gece seviyesi, öğlen yükselmesi, 253 / 259 V aşımları.

Faz 10 (pilot A, ucuz ölçüm; kart docs/gorev/volkan-faz10-pilot-a.md), veri partisi P6. Etiket: TEK EV, GÖSTERİM.
Kişisel bilgi (ad, adres, seri no) bu betiğe ve çıktıya girmez; ham kayıt depo dışında durur (tüzük §2, KAYNAK.txt
kişisel bilgisiz). Marka marka dışa aktarma ve gece boşluğu: Faz 10 kartı.

Kullanım (ham kayıt depo dışında; yolu ver):
  python3 src/inverter_kaydi.py <kayıt.csv>                     # sütunları kendisi bulmaya çalışır
  python3 src/inverter_kaydi.py <kayıt.xlsx> --zaman "Time" --gerilim "Grid Voltage(V)"
  python3 src/inverter_kaydi.py <kayıt.csv> --gerilim "Vac1" --gerilim "Vac2" --gerilim "Vac3"   # üç faz

Modelin aynı tip trafo için verdiği (üretici 1.3, geliştirme şehirleri 1–10, panelli şehir konutu trafosu, 134 trafo;
cevap anahtarı) [Hesap]:
  bara (gece seviyesine yakın) P10/50/90 245,1 / 247,6 / 250,6 V
  trafonun en yüksek ev gerilimi, 14 gün P10/50/90 249,5 / 253,8 / 260,0 V; bara üstü 3,4 / 5,6 / 10,5 V
  253 V'u aşan trafo 79/134, 259 V'u aşan 17/134
Tek ev trafonun en kötü evi olmayabilir: ölçülen en yüksek değer bu dağılımın altında kalabilir.
"""
import argparse
import csv
import statistics as st
import sys
from datetime import datetime
from pathlib import Path

GECE = (0, 5)          # 00:00–04:59: yük en düşük, panel yok → bara seviyesine en yakın
OGLE = (11, 14)        # 11:00–13:59: güneş tepede
SINIRLAR = (253.0, 259.0)   # EN 50160 üst sınırı (230 V + %10); Kıb-Tek planlama sınırı [CLAUDE.md]
MODEL = dict(bara=(245.1, 247.6, 250.6), vmax=(249.5, 253.8, 260.0), yukselme=(3.4, 5.6, 10.5))   # üretici 1.3, 1–10
ZAMAN_ADAY = ('time', 'zaman', 'date', 'tarih', 'timestamp', 'update', 'collect')
GERILIM_ADAY = ('grid voltage', 'vac', 'ac voltage', 'phase voltage', 'gerilim', 'u_ac', 'uac', 'ua', 'ub', 'uc',
                'l1', 'l2', 'l3', 'voltage')
ZAMAN_BICIM = ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%d.%m.%Y %H:%M:%S', '%d.%m.%Y %H:%M', '%d/%m/%Y %H:%M:%S',
               '%d/%m/%Y %H:%M', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M', '%Y/%m/%d %H:%M:%S', '%Y/%m/%d %H:%M',
               '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%SZ')


def satirlar(yol):
    yol = Path(yol)
    if yol.suffix.lower() in ('.xlsx', '.xlsm'):
        import openpyxl
        ws = openpyxl.load_workbook(yol, read_only=True, data_only=True).active
        rows = [[('' if c is None else c) for c in r] for r in ws.iter_rows(values_only=True)]
    else:
        ham = yol.read_bytes()
        metin = next(ham.decode(e) for e in ('utf-8-sig', 'utf-16', 'cp1254', 'latin-1') if _cozulur(ham, e))
        ayrac = max((',', ';', '\t'), key=metin.splitlines()[0].count)
        rows = list(csv.reader(metin.splitlines(), delimiter=ayrac))
    # başlık satırı: zaman adayı içeren ilk satır (bazı dışa aktarımlarda üstte başlık bilgisi olur)
    for i, r in enumerate(rows[:30]):
        if any(any(a in str(c).lower() for a in ZAMAN_ADAY) for c in r):
            return [str(c).strip() for c in rows[i]], rows[i + 1:]
    sys.exit('Başlık satırı bulunamadı; --zaman ve --gerilim ile sütun adlarını verin.')


def _cozulur(ham, e):
    try:
        ham.decode(e)
        return True
    except UnicodeDecodeError:
        return False


def zaman_oku(x):
    if isinstance(x, datetime):
        return x
    s = str(x).strip()
    for b in ZAMAN_BICIM:
        try:
            return datetime.strptime(s, b)
        except ValueError:
            pass
    return None


def sayi(x):
    try:
        return float(str(x).replace(',', '.'))
    except ValueError:
        return None


def nicel(x, q):
    x = sorted(x)
    return x[min(len(x) - 1, max(0, int(round(q * (len(x) - 1)))))] if x else float('nan')


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('dosya')
    ap.add_argument('--zaman')
    ap.add_argument('--gerilim', action='append')
    a = ap.parse_args()
    baslik, rows = satirlar(a.dosya)
    low = [b.lower() for b in baslik]
    zi = baslik.index(a.zaman) if a.zaman else next(i for i, b in enumerate(low) if any(z in b for z in ZAMAN_ADAY))
    if a.gerilim:
        gi = [baslik.index(g) for g in a.gerilim]
    else:
        gi = [i for i, b in enumerate(low) if i != zi and any(g in b for g in GERILIM_ADAY)
              and not any(y in b for y in ('pv', 'dc', 'bat', 'mppt', 'string', 'bus'))]
    if not gi:
        sys.exit(f'Gerilim sütunu bulunamadı. Başlıklar: {baslik}')
    print(f'zaman sütunu: {baslik[zi]!r}; gerilim sütunları: {[baslik[i] for i in gi]}')
    for i in gi:
        veri = []
        for r in rows:
            if len(r) <= max(zi, i):
                continue
            t, v = zaman_oku(r[zi]), sayi(r[i])
            if t and v and 150 < v < 300:          # 0 ve boş: inverter uyuyor ya da kayıt yok
                veri.append((t, v))
        veri.sort()
        if not veri:
            print(f'\n{baslik[i]}: geçerli değer yok')
            continue
        adim = st.median((b[0] - a_[0]).total_seconds() / 60 for a_, b in zip(veri, veri[1:])) if len(veri) > 1 else 0
        gece = [v for t, v in veri if GECE[0] <= t.hour < GECE[1]]
        ogle = [v for t, v in veri if OGLE[0] <= t.hour < OGLE[1]]
        gunler = sorted({t.date() for t, _ in veri})
        print(f'\n== {baslik[i]} — TEK EV, GÖSTERİM ==')
        print(f'kayıt: {veri[0][0]} … {veri[-1][0]}, {len(veri)} nokta, {len(gunler)} gün, adım ~{adim:g} dk')
        if not gece:
            print('gece kaydı YOK: inverter gece uyuyor; gece seviyesi yerine her sabahın ilk değeri:')
            ilk = [min((x for x in veri if x[0].date() == g), key=lambda x: x[0])[1] for g in gunler]
            print(f'  sabah ilk değer ortanca {st.median(ilk):.1f} V (güneş zayıf, yük az: bara seviyesine yakın sayılabilir)')
            gece_seviye = st.median(ilk)
        else:
            gece_seviye = st.median(gece)
            print(f'gece 00–05: ortanca {gece_seviye:.1f} V, P10–P90 {nicel(gece, .1):.1f}–{nicel(gece, .9):.1f} V '
                  f'(model bara P10/50/90 {MODEL["bara"]})')
        if ogle:
            print(f'öğlen 11–14: ortanca {st.median(ogle):.1f} V, en yüksek {max(ogle):.1f} V; '
                  f'gece seviyesinin üstü: ortanca {st.median(ogle) - gece_seviye:+.1f} V, en yüksek {max(ogle) - gece_seviye:+.1f} V '
                  f'(model trafonun en kötü evi: bara üstü {MODEL["yukselme"]})')
        print(f'haftanın en yüksek değeri {max(v for _, v in veri):.1f} V (model trafonun en kötü evi P10/50/90 {MODEL["vmax"]})')
        for s in SINIRLAR:
            n = sum(v > s for _, v in veri)
            gun = len({t.date() for t, v in veri if v > s})
            print(f'> {s:g} V: {n} nokta (~{n * adim:g} dk), {gun}/{len(gunler)} gün')
        # 10 dakikalık ortalama (EN 50160 ölçüsü) 253 V üstü
        kova = {}
        for t, v in veri:
            k = t.replace(minute=t.minute - t.minute % 10, second=0, microsecond=0)
            kova.setdefault(k, []).append(v)
        on = {k: st.mean(x) for k, x in kova.items()}
        print(f'10 dk ortalaması > 253 V: {sum(x > 253 for x in on.values())} pencere / {len(on)}')
        print('gün gün: gece ortanca | öğlen en yüksek | > 253 nokta')
        for g in gunler:
            gv = [v for t, v in veri if t.date() == g]
            gg = [v for t, v in veri if t.date() == g and GECE[0] <= t.hour < GECE[1]]
            go = [v for t, v in veri if t.date() == g and OGLE[0] <= t.hour < OGLE[1]]
            print(f'  {g}: {st.median(gg) if gg else float("nan"):.1f} | {max(go) if go else float("nan"):.1f} | '
                  f'{sum(v > 253 for v in gv)}')


if __name__ == '__main__':
    main()
