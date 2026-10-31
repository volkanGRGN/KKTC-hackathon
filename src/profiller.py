#!/usr/bin/env python3
"""EAC profil sınıfları: Excel'den okuma, 30 dk -> 5 dk açma, tip eğrileri, sağlama.

Girdi: data/raw/eac-profil-siniflari/Offtake_Profile_Classes.xlsx (KAYNAK.txt'deki adresten indirilir).
Birim: abonenin yük hakkına (kVA) göre birim değer (pu). Mutlak kW'a çevirmek şehir üreticisinin işi.

Katmanlar:
1. oku(): 12 sınıfın 24 tipik günü (12 ay x iş günü / tatil).
   Excel yavaş okunur; ilk çalıştırmada aynı klasöre _onbellek.json yazılır (depoya girmez).
2. bes_dakika(): 48 yarım saatlik değer -> 288 beş dakikalık değer.
3. sinif_egrisi() / tip_egrisi(): sınıfın ya da 7 trafo tipinin günlük eğrisi.
4. saglama(): ROADMAP Faz 1 "veri sağlaması" rakamları.

Sözleşme (docs/data/tablo-bicimi.md, Can'ın Faz 1 kartı): şehir üreticisi oku() ve sinif_egrisi()'ni
çağırır; adları, imzaları ve sınıf adlarını değiştirmeden önce Volkan'ın kutusu. pu -> kW çevirisi ve
tiplerin abone karışımı şehir üreticisinde, burada değil.

Çalıştırma: python3 src/profiller.py [xlsx yolu]
"""
import datetime as dt
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
XLSX = KOK / 'data' / 'raw' / 'eac-profil-siniflari' / 'Offtake_Profile_Classes.xlsx'

# Excel sayfası -> kısa ad. 5. sayfanın adı yanlış yazılmış, otel sınıfıdır (ADR-0004).
SAYFALAR = {
    'DOMESTIC': 'konut',
    'DOMESTIC_with_NM': 'konut_panelli',      # net ölçüm: şebekeden çekilen eksi verilen
    'SMALL_COMMERCIAL': 'kucuk_ticari',
    'L._COMM._SHOPS_STORES': 'buyuk_ticari',
    'L._COMM._STORES': 'otel',
    'SMALL_INDUSTRIAL': 'kucuk_sanayi',
    'LARGE_INDUSTRIAL': 'buyuk_sanayi',
    'COMM._with_NB': 'ticari_panelli',
    'IND._with_NB': 'sanayi_panelli',
    'STREET_LIGHTING': 'sokak',
    'WATER_PUMPS': 'su_pompasi',             # ölçülmemiş, EAC kuralından türetilmiş
    'THERMAL_ENERGY_STORAGE': 'isi_depolama',
}
AYLAR = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
YARIM_SAAT = 48
ADIM = 288                                   # 5 dakika

# Yalnız sağlama için. Şehir üreticisi trafo başına abone sayısını kendi kurar ve sınıf eğrilerini
# toplar (ROADMAP Faz 1).
# 7 trafo tipi = sınıf karışımı (ağırlıklar toplamı 1). Eğriler panelsiz sınıflardan;
# panel üretimi şehir üreticisinde Open-Meteo ışınımıyla ayrıca eklenir (iki kez sayılmasın).
TIPLER = {
    'sehir_konutu': {'konut': 0.90, 'kucuk_ticari': 0.10},
    'koy': {'konut': 0.80, 'kucuk_ticari': 0.10, 'su_pompasi': 0.10},
    'carsi': {'kucuk_ticari': 0.50, 'buyuk_ticari': 0.40, 'konut': 0.10},
    'otel': {'otel': 0.85, 'kucuk_ticari': 0.15},
    'sanayi': {'kucuk_sanayi': 0.60, 'buyuk_sanayi': 0.40},
    'sulama': {'su_pompasi': 0.90, 'konut': 0.10},
    'yurt': {'konut': 1.00},                 # BULAMADIM: öğrenci yurdu eğrisi yok, konuttan
}


def _saat_indeksi(t):
    """Excel'in TIME sütunu (00:30 ... 00:00) -> 0..47. 00:30 = ilk yarım saat (00:00–00:30)."""
    dakika = t.hour * 60 + t.minute
    return (dakika // 30 - 1) % YARIM_SAAT


def _excelden_oku(yol):
    import openpyxl
    wb = openpyxl.load_workbook(yol, read_only=True, data_only=True)
    out = {}
    for sayfa, ad in SAYFALAR.items():
        rows = wb[sayfa].iter_rows(values_only=True)
        bas = next(rows)
        tipik_sut = {h: i for i, h in enumerate(bas) if i >= 9 and h}
        tipik = {h: [None] * YARIM_SAAT for h in tipik_sut}
        for r in rows:
            if not isinstance(r[8], dt.time):
                break
            k = _saat_indeksi(r[8])
            for h, i in tipik_sut.items():
                tipik[h][k] = float(r[i])
        out[ad] = tipik
    return out


def oku(yol=XLSX):
    """{sınıf: {'Apr_WD': [48], 'Apr_NWD': [48], ...}}"""
    yol = Path(yol)
    onbellek = yol.parent / '_onbellek.json'
    if onbellek.exists() and onbellek.stat().st_mtime >= yol.stat().st_mtime:
        with open(onbellek, encoding='utf-8') as fh:
            return json.load(fh)
    veri = _excelden_oku(yol)
    with open(onbellek, 'w', encoding='utf-8') as fh:
        json.dump(veri, fh)
    return veri


def bes_dakika(seri):
    """48 yarım saat ortalaması -> 288 beş dakika. Değerler yarım saatin ortasına konur,
    aralar doğrusal doldurulur (gün başı ve sonu birbirine bağlanır)."""
    out = []
    for s in range(ADIM):
        x = (s + 0.5) / 6 - 0.5               # 5 dk adımın ortası, yarım saat ortası biriminde
        i = int(x // 1)
        w = x - i
        out.append(seri[i % YARIM_SAAT] * (1 - w) + seri[(i + 1) % YARIM_SAAT] * w)
    return out


def sinif_egrisi(veri, sinif, ay, gun='is'):
    """ay: 1–12; gun: 'is' (iş günü) ya da 'tatil' (cumartesi, pazar, bayram). 288 değer.
    EAC'nin tam yıl serisi bu iki tipik günün tekrarı; cumartesi ve pazar ayrı değil."""
    return bes_dakika(veri[sinif][f"{AYLAR[ay - 1]}_{'WD' if gun == 'is' else 'NWD'}"])


def tip_egrisi(veri, tip, ay, gun='is'):
    """7 trafo tipinden birinin abone başına birim eğrisi (288 değer, pu)."""
    out = [0.0] * ADIM
    for sinif, w in TIPLER[tip].items():
        for s, v in enumerate(sinif_egrisi(veri, sinif, ay, gun)):
            out[s] += w * v
    return out


def _saat(s):
    return f'{s * 5 // 60:02d}:{s * 5 % 60:02d}'


def _ort(eg, bas_saat, bit_saat):
    sl = eg[bas_saat * 12: bit_saat * 12]
    return sum(sl) / len(sl)


def saglama(veri):
    """ROADMAP Faz 1 veri sağlaması. (ad, değer, alt, üst) listesi döner."""
    sonuc = []
    konut = sinif_egrisi(veri, 'konut', 4)
    oran = konut[12 * 12] / konut[21 * 12]
    sonuc.append(('konut Nisan iş günü öğlen/akşam (12:00 / 21:00)', oran, 0.6, 0.8))

    carsi = tip_egrisi(veri, 'carsi', 4)
    tepe = max(range(ADIM), key=carsi.__getitem__)
    sonuc.append((f'çarşı Nisan iş günü tepe saati ({_saat(tepe)})', tepe * 5 / 60, 11.0, 14.0))

    gun_ort = lambda eg: sum(eg) / len(eg)
    otel = gun_ort(sinif_egrisi(veri, 'otel', 7)) / gun_ort(sinif_egrisi(veri, 'otel', 1))
    sonuc.append(('otel iş günü ortalaması Temmuz / Ocak', otel, 3.0, 5.0))

    # 5 dk açma günlük enerjiyi koruyor mu: her sınıf x 24 tipik gün, en uzak oran.
    oranlar = [sum(bes_dakika(seri)) / ADIM / (sum(seri) / YARIM_SAAT)
               for gunler in veri.values() for seri in gunler.values() if sum(seri)]
    en_uzak = max(oranlar, key=lambda o: abs(o - 1))
    sonuc.append((f'5 dk açma enerji oranı, {len(oranlar)} gün içinde en uzak', en_uzak, 0.99, 1.01))

    # ROADMAP "pazar"; EAC'de pazar ayrı yok, tatil tipik günü kullanılır.
    tatil = _ort(tip_egrisi(veri, 'carsi', 4, 'tatil'), 11, 14)
    is_gunu = _ort(carsi, 11, 14)
    sonuc.append(('çarşı Nisan tatil öğleni / iş günü öğleni (11–14)', tatil / is_gunu, 0.0, 0.5))
    return sonuc


def main():
    yol = Path(sys.argv[1]) if len(sys.argv) > 1 else XLSX
    if not yol.exists():
        sys.exit(f'{yol} yok; data/raw/eac-profil-siniflari/KAYNAK.txt adresinden indirin.')
    veri = oku(yol)
    print(f'{len(veri)} sınıf okundu: {", ".join(veri)}')
    print('\nNisan iş günü, 11–14 ortalaması (pu, abone başına):')
    for tip in TIPLER:
        print(f'  {tip:13s} {_ort(tip_egrisi(veri, tip, 4), 11, 14):.3f}')
    print('\nSağlama (ROADMAP Faz 1):')
    hepsi = True
    for ad, deger, alt, ust in saglama(veri):
        gecti = alt <= deger <= ust
        hepsi &= gecti
        print(f"  [{'GEÇTİ' if gecti else 'KALDI'}] {ad}: {deger:.2f} (aralık {alt}–{ust})")
    sys.exit(0 if hepsi else 1)


if __name__ == '__main__':
    main()
