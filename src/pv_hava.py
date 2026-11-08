#!/usr/bin/env python3
"""Hava verisinin saati ve panelin sıcaklık kaybı (üretici 1.7, 8 Kasım; KTEMO karşılaştırması 3 Kasım).

1 Saat: Open-Meteo saat sütunu yaz saatsiz, sabit UTC+2 (KTEMO gerçek paneliyle kışın kayma 0, yazın 1 saat;
  docs/log/2026-11-03-volkan-ktemo-pv-karsilastirma.md). Model yerel saatle (Lefkoşa, AB yaz saati) çalışır:
  `om_yerel` etiketi yerel saate çevirir. Saatlik ortalama (ışınım) etiketi L = [L−1 sa, L); anlık değer
  (sıcaklık) L'nin kendisi. Yaz saati kuralı AB'ninki: Mart'ın son pazarı 01:00 UTC – Ekim'in son pazarı 01:00 UTC
  (Kuzey Kıbrıs 2018'den beri aynı; 2016–2017 Türkiye'yle kalıcı yaz saatindeydi, bu dosyalarda o yıllar kullanılmıyor).
  zoneinfo kullanılmaz: Windows'ta tzdata paketi ister.
2 Sıcaklık kaybı: panel gücü = kurulu güç × ışınım ÷ 1000 × 0,82 × `panel_carpani(T, G)`.
  Çarpan = 1 + GAMMA × (hücre sıcaklığı − T_REF), hücre = hava + K_ISINIM × ışınım. GAMMA ve K_ISINIM kristal
  silikon panelin tipik değerleri [Yorum: veri sayfası değeri, KTEMO panelinin modeli bilinmiyor]; T_REF, Nisan'ın
  açık öğle saatlerinde çarpan ortalaması 1 olacak biçimde KTEMO ayar yıllarından (2018–2022) [Hesap: bu betik].
  Böylece Nisan (panel katmanının ayı) eski 0,82 düzeyinde kalır, yaz düşer, kış yükselir.

Ayar: python3 src/pv_hava.py <ktemo gunluk klasörü> <open-meteo klasörü>  → T_REF ve aylara göre gerçek ÷ formül
(eski sabit ↔ sıcaklıklı), ayar 2018–2022, sınav 2023–2026.
"""
import datetime as dt
import sys

GAMMA = -0.004          # güç sıcaklık katsayısı, 1/°C [Yorum: kristal silikon veri sayfası aralığı −0,0035…−0,0045]
K_ISINIM = 0.03         # hücre ısınması, °C / (W/m²) [Yorum: NOCT ~45 °C → (45 − 20) ÷ 800]
T_REF = 50.8            # °C [Hesap: KTEMO 2018–2022 Nisan açık öğle (eğik > 700 W/m²) hücre sıcaklığı ortalaması, 654 saat; bu betik]


def _son_pazar(yil, ay):
    gun = dt.date(yil, ay + 1, 1) - dt.timedelta(days=1) if ay < 12 else dt.date(yil, 12, 31)
    return gun - dt.timedelta(days=(gun.weekday() + 1) % 7)


def yaz_saati_mi(utc):
    """utc: saat dilimsiz UTC zaman. AB kuralı."""
    bas = dt.datetime.combine(_son_pazar(utc.year, 3), dt.time(1))
    son = dt.datetime.combine(_son_pazar(utc.year, 10), dt.time(1))
    return bas <= utc < son


def om_yerel(etiket, ortalama):
    """Open-Meteo etiketi (sabit UTC+2, saat dilimsiz) -> yerel saat (Lefkoşa). ortalama=True: saatlik ortalamanın
    başladığı yerel saat (etiket − 1 sa); False: anlık değerin yerel saati."""
    an = etiket - dt.timedelta(hours=1) if ortalama else etiket
    return an + dt.timedelta(hours=1) if yaz_saati_mi(an - dt.timedelta(hours=2)) else an


def bosluk_doldur(seri):
    """24 değerlik günde yaz saatine geçişte boş kalan saat (nan ya da None): komşuların ortalaması."""
    out = list(seri)
    for i, x in enumerate(out):
        if x is None or x != x:
            komsu = [out[j] for j in (i - 1, i + 1) if 0 <= j < len(out) and out[j] is not None and out[j] == out[j]]
            out[i] = sum(komsu) / len(komsu) if komsu else x
    return out


def panel_carpani(sicaklik_c, isinim_wm2):
    """Eski sabit 0,82'ye göre sıcaklık çarpanı (Nisan açık öğlede ~1)."""
    return 1 + GAMMA * (sicaklik_c + K_ISINIM * isinim_wm2 - T_REF)


def _ayar(gun_klasoru, om_klasoru):
    import csv, glob, json, os
    from collections import defaultdict
    UTC = dt.timezone.utc

    gercek = defaultdict(list)
    for yol in sorted(glob.glob(os.path.join(gun_klasoru, '*.json'))):
        try:
            with open(yol, encoding='utf-8') as fh:
                j = json.load(fh)
        except (json.JSONDecodeError, OSError):
            continue
        toplam = defaultdict(float)
        for s in j['settings']['series']:
            if str(s.get('id', '')).startswith('FromGen'):
                for t, v in s['data']:
                    if v is not None:
                        toplam[t] += v
        for t, v in toplam.items():
            u = dt.datetime.fromtimestamp(t / 1000, UTC).replace(tzinfo=None)
            gercek[u.replace(minute=0, second=0, microsecond=0)].append(v)
    gercek = {k: sum(v) / len(v) for k, v in gercek.items() if len(v) >= 11}

    om = {}   # {UTC saat başı: (eğik W/m², sıcaklık)}; ışınım [L−1, L), sıcaklık L'de → ortalamaya yakın
    for yol in sorted(glob.glob(os.path.join(om_klasoru, 'lefkosa_saatlik_*.csv'))):
        with open(yol, encoding='utf-8') as fh:
            satir = list(csv.reader(fh))
        b = next(i for i, r in enumerate(satir) if r and r[0] == 'time')
        gi = next(i for i, x in enumerate(satir[b]) if x.startswith('global_tilted'))
        si = next(i for i, x in enumerate(satir[b]) if x.startswith('temperature_2m'))
        for r in satir[b + 1:]:
            if r and r[gi] != '' and r[si] != '':
                L = dt.datetime.fromisoformat(r[0])
                om[L - dt.timedelta(hours=3)] = (float(r[gi]), float(r[si]))

    ortak = sorted(set(gercek) & set(om))
    kotu = {k.date() for k in ortak if om[k][0] > 300 and gercek[k] < 50}      # çevrim dışı gün
    rs = [(k, gercek[k], om[k][0], om[k][1]) for k in ortak if k.date() not in kotu]
    acik = lambda r: r[2] > 700
    nisan = [r for r in rs if r[0].year <= 2022 and r[0].month == 4 and acik(r)]
    t_ref = sum(r[3] + K_ISINIM * r[2] for r in nisan) / len(nisan)

    def carpan(r, sicakli):
        return 1 + GAMMA * (r[3] + K_ISINIM * r[2] - t_ref) if sicakli else 1.0

    rapor = {'t_ref': round(t_ref, 1), 'nisan_acik_saat': len(nisan), 'atilan_gun': len(kotu)}
    for ad, sicakli in (('eski_sabit', False), ('sicaklikli', True)):
        ayar = [r for r in rs if r[0].year <= 2022]
        c = sum(r[1] for r in ayar) / sum(r[2] * carpan(r, sicakli) for r in ayar)
        aylar = {}
        for a in range(1, 13):
            x = [r for r in rs if r[0].year >= 2023 and r[0].month == a and acik(r)]
            if x:
                aylar[a] = round(sum(r[1] for r in x) / sum(c * r[2] * carpan(r, sicakli) for r in x), 3)
        sinav = [r for r in rs if r[0].year >= 2023 and r[2] > 100]
        hata = sorted(abs(r[1] - c * r[2] * carpan(r, sicakli)) / (c * r[2] * carpan(r, sicakli)) for r in sinav)
        gun = defaultdict(lambda: [0.0, 0.0])
        for r in sinav:
            gun[r[0].date()][0] += r[1]
            gun[r[0].date()][1] += c * r[2] * carpan(r, sicakli)
        gh = sorted(abs(a - b) / b for a, b in gun.values() if b > 0)
        q = lambda a, p: round(a[min(len(a) - 1, int(p * len(a)))], 3)
        rapor[ad] = {'aya_gore_gercek_bolu_formul_acik_sinav': aylar,
                     'aylar_arasi_yayilim': round(max(aylar.values()) - min(aylar.values()), 3),
                     'saatlik_hata_ortanca_p90': [q(hata, .5), q(hata, .9)], 'gunluk_hata_ortanca_p90': [q(gh, .5), q(gh, .9)],
                     'sinav_saat': len(sinav)}
    print(json.dumps(rapor, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    _ayar(sys.argv[1], sys.argv[2])
