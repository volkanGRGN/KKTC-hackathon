// Canlı tahmin haritası (veri ve olaylar: dashboard/canli_harita.py). Kendi çizimimiz, tuval; dış kaynak yok.
// Normal harita: bütün ada (Güney soluk, Kuzey belirgin), Girne'deki şehir canlı, öbür şehirler kasabalarda.
//   Tekerlek / sürükleme / +− / "Girne" "Kıbrıs" ile yakınlaş; trafoya tıkla -> kart (Malta haritası gibi);
//   Girne trafosunun kartında "Ölçülmüş say" -> "tiklama".
// Animasyon (veri.oynat): her yer karanlık, yalnız ölçülen trafonun çevresi küçük bir daire; tahminler karanlıkta
//   belirir ("az ölçüp çoğunu tahmin"); sonra ada açılır, kasabalar dolar; bitince "bitti" ve normal haritaya geçer.
// Ölçülen trafo dolu nokta (kalın kontur), tahmin soluk halka, henüz tahmin yok gri nokta. Etiket her karede.

const PI2 = Math.PI * 2;
const GUNEY_ALFA = 0.5; // Güney Kıbrıs soluk (Volkan)
const KARANLIK = 0.8; // animasyonda ölçülmeyen yerler (Volkan: "karanlık olmalı")
const DAIRE_KM = 0.35; // ölçülen trafonun aydınlık dairesi (Volkan: "küçük bir daire")
const DAIRE_EN_AZ_PX = 14;
const DAIRE_POP = 0.55; // sn
const NOKTA_POP = 0.45;
const KAMERA_SN = 0.9;
const ACILIS_SN = 3.0;
const BEKLE_SN = 1.6;
const KASABA_ARA = 0.85;
const S_ANIM_EN_COK = 320; // px/km: animasyonda en yakın görünüm (bir mahalle)
const S_EN_COK = 2500; // px/km: elle yakınlaşmanın sınırı
const UST_PAY = 64; // px: üstteki etiket ve başlık kutusu, harita altında kalmasın
const AD_ESIK = 45; // px/km: bundan uzakta kasaba adları görünür
const FONT = '"Source Sans Pro", "Source Sans 3", system-ui, -apple-system, sans-serif';

const TEMA = {
  acik: {
    bos: "#eef1f5", deniz: "#d4e4f0", kara: "#fbfaf5", kiyi: "#8ea8be", bina: "#d6cfc0", yol: "#e7e2d7",
    yazi: "#1f2933", soluk: "#5b6875", kontur: "#14181f", kutu: "rgba(255,255,255,0.88)", cember: "rgba(42,120,214,0.6)",
  },
  koyu: {
    bos: "#11151c", deniz: "#13283c", kara: "#3a404a", kiyi: "#5f7f9b", bina: "#4d5460", yol: "#454c57",
    yazi: "#e8edf2", soluk: "#9aa7b4", kontur: "#f4f6f8", kutu: "rgba(20,24,31,0.86)", cember: "rgba(140,190,250,0.7)",
  },
};

const sinirla = (t) => Math.max(0, Math.min(1, t));
const yumusak = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
function geri(t) {
  const c1 = 1.70158, c3 = c1 + 1;
  return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
}
function pop(dt, sure) {
  if (dt <= 0) return 0;
  return dt >= sure ? 1 : Math.max(0, geri(dt / sure));
}
const vurgu = (dt, sure = 0.45) => (dt > 0 && dt < sure ? 0.45 * Math.sin((Math.PI * dt) / sure) : 0);

function hexRgb(h) {
  const n = parseInt(h.slice(1), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}
function karisim(a, b, u) {
  const x = hexRgb(a), y = hexRgb(b);
  return `rgb(${x.map((v, i) => Math.round(v + (y[i] - v) * u)).join(",")})`;
}

function temaBul(el) {
  const c = getComputedStyle(el).getPropertyValue("--st-background-color").trim();
  if (!c) return window.matchMedia("(prefers-color-scheme: dark)").matches ? TEMA.koyu : TEMA.acik;
  const g = document.createElement("canvas").getContext("2d");
  g.fillStyle = "#ffffff";
  g.fillStyle = c;
  const v = g.fillStyle;
  const rgb = v.startsWith("#") ? hexRgb(v) : (v.match(/[\d.]+/g) || [255, 255, 255]).slice(0, 3).map(Number);
  return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2] < 128 ? TEMA.koyu : TEMA.acik;
}

// ---------- kamera ----------

function kutuBul(noktalar, pay = 0) {
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  noktalar.forEach(([x, y, r = 0]) => {
    x0 = Math.min(x0, x - r - pay); y0 = Math.min(y0, y - r - pay);
    x1 = Math.max(x1, x + r + pay); y1 = Math.max(y1, y + r + pay);
  });
  return [x0, y0, x1, y1];
}
function sigdir(k, W, H, pay = 1.2, sMax = S_ANIM_EN_COK) { // kutu, üst pay dışındaki alana sığsın
  const w = Math.max(k[2] - k[0], 0.3), h = Math.max(k[3] - k[1], 0.3);
  const s = Math.min(W / (w * pay), (H - UST_PAY) / (h * pay), sMax);
  return { cx: (k[0] + k[2]) / 2, cy: (k[1] + k[3]) / 2 - UST_PAY / 2 / s, s };
}
function karistir(a, b, u) {
  if (u <= 0) return a;
  if (u >= 1) return b;
  // ölçek üstel, merkez ekranda sabit hızla: yakınlaşırken/uzaklaşırken kayma olmasın
  const s = a.s * Math.pow(b.s / a.s, u);
  const w = Math.abs(b.s - a.s) < 1e-9 ? u : (1 / a.s - 1 / s) / (1 / a.s - 1 / b.s);
  return { cx: a.cx + (b.cx - a.cx) * w, cy: a.cy + (b.cy - a.cy) * w, s };
}
const ekran = (kam, W, H, x, y) => [(x - kam.cx) * kam.s + W / 2, (y - kam.cy) * kam.s + H / 2];
const yaricap = (s) => Math.max(1.9, Math.min(9, 1.4 + s * 0.085));

function adaKutusu(z) {
  const p = [];
  [...z.kuzey, ...z.guney].forEach((h) => { for (let i = 0; i < h.length; i += 2) p.push([h[i], h[i + 1]]); });
  return kutuBul(p);
}
const adaKam = (S) => sigdir(S.adaKutu, S.W, S.H, 1.06);
const girneKam = (S) => sigdir(kutuBul(S.veri.sehir.n.map((t) => [t.x, t.y]), 0.3), S.W, S.H, 1.12);

function kamera(S, simdi) {
  if (!S.kam) S.kam = adaKam(S);
  const g = S.gecisKam;
  if (g) {
    const u = sinirla((simdi - g.t0) / g.sure);
    if (u < 1) return karistir(g.bas, g.hedef, yumusak(u));
    S.gecisKam = null;
  }
  return S.kam;
}
function kameraGit(S, hedef, sure = 700) {
  const simdi = performance.now();
  S.gecisKam = { bas: kamera(S, simdi), hedef, t0: simdi, sure };
  S.kam = hedef;
  S.kirli = true;
  dongu(S);
}
function yakinlas(S, f, mx, my, gecisli = false) {
  const k = kamera(S, performance.now());
  S.gecisKam = null;
  const s = Math.max(adaKam(S).s * 0.6, Math.min(S_EN_COK, k.s * f));
  const wx = k.cx + (mx - S.W / 2) / k.s, wy = k.cy + (my - S.H / 2) / k.s;
  const yeni = { cx: wx - (mx - S.W / 2) / s, cy: wy - (my - S.H / 2) / s, s };
  S.kam = k;
  if (gecisli) kameraGit(S, yeni, 300);
  else { S.kam = yeni; S.kirli = true; dongu(S); }
}

// ---------- çizim ----------

function zeminCiz(S, kam) {
  const { ctx, W, H, tema: T } = S;
  const z = S.veri.zemin;
  const temel = ctx.globalAlpha;
  const yolla = (d) => {
    for (let i = 0; i < d.length; i += 2) {
      const x = (d[i] - kam.cx) * kam.s + W / 2, y = (d[i + 1] - kam.cy) * kam.s + H / 2;
      if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y);
    }
  };
  const halkalar = (liste) => {
    ctx.beginPath();
    liste.forEach((h) => { yolla(h); ctx.closePath(); });
  };
  ctx.fillStyle = T.deniz;
  ctx.fillRect(0, 0, W, H);
  halkalar(z.guney);
  ctx.globalAlpha = temel * GUNEY_ALFA;
  ctx.fillStyle = T.kara; ctx.fill();
  ctx.strokeStyle = T.kiyi; ctx.lineWidth = 1.2; ctx.stroke();
  ctx.globalAlpha = temel;
  halkalar(z.kuzey);
  ctx.fillStyle = T.kara; ctx.fill();
  ctx.strokeStyle = T.kiyi; ctx.lineWidth = 1.2; ctx.stroke();
  if (z.girne_kara) { // ayrıntılı OSM kıyısı, yalnız yama içinde
    const [ax, ay] = ekran(kam, W, H, z.yama[0], z.yama[1]);
    const [bx, by] = ekran(kam, W, H, z.yama[2], z.yama[3]);
    ctx.save();
    ctx.beginPath(); ctx.rect(ax, ay, bx - ax, by - ay); ctx.clip();
    ctx.fillStyle = T.deniz; ctx.fillRect(ax, ay, bx - ax, by - ay);
    halkalar(z.girne_kara);
    ctx.fillStyle = T.kara; ctx.fill();
    ctx.strokeStyle = T.kiyi; ctx.lineWidth = 1.2; ctx.stroke();
    ctx.restore();
  }
  const ba = sinirla((kam.s - 40) / 110);
  if (ba > 0 && z.binalar.length) {
    ctx.globalAlpha = temel * ba;
    ctx.beginPath(); z.yollar.forEach(yolla);
    ctx.strokeStyle = T.yol; ctx.lineWidth = Math.max(1, kam.s * 0.006); ctx.stroke();
    halkalar(z.binalar);
    ctx.fillStyle = T.bina; ctx.fill();
    ctx.globalAlpha = temel;
  }
}

function trafoCiz(S, px, py, r, sinif, olculu, once = undefined, u = 1) {
  if (r <= 0.3) return;
  const { ctx, tema: T } = S;
  const R = S.veri.renk;
  const renk = (s) => R[s] || (olculu ? R.olculdu : R.kapali);
  const c = once !== undefined && u < 1 ? karisim(renk(once), renk(sinif), u) : renk(sinif);
  ctx.beginPath();
  if (olculu) { // dolu, kalın kontur
    ctx.arc(px, py, r * 1.1, 0, PI2);
    ctx.fillStyle = c; ctx.fill();
    ctx.lineWidth = Math.max(1.4, r * 0.34); ctx.strokeStyle = T.kontur; ctx.stroke();
  } else if (sinif) { // tahmin: soluk halka
    ctx.arc(px, py, r, 0, PI2);
    ctx.globalAlpha = 0.22; ctx.fillStyle = c; ctx.fill();
    ctx.globalAlpha = 0.95; ctx.lineWidth = Math.max(1.2, r * 0.36); ctx.strokeStyle = c; ctx.stroke();
    ctx.globalAlpha = 1;
  } else { // henüz tahmin yok
    ctx.arc(px, py, Math.max(1.4, r * 0.62), 0, PI2);
    ctx.globalAlpha = 0.85; ctx.fillStyle = c; ctx.fill(); ctx.globalAlpha = 1;
  }
}

function secimHalkasi(S, x, y, r) {
  const { ctx, tema: T } = S;
  ctx.beginPath(); ctx.arc(x, y, r * 2 + 3, 0, PI2);
  ctx.lineWidth = 2; ctx.strokeStyle = T.yazi; ctx.stroke();
}

function kutuYazi(S, metin, x, y, boy, kalin) {
  const { ctx, tema: T } = S;
  ctx.font = `${kalin ? 650 : 600} ${boy}px ${FONT}`;
  const w = ctx.measureText(metin).width;
  ctx.fillStyle = T.kutu;
  ctx.beginPath(); ctx.roundRect(x, y, w + 16, boy + 12, 7); ctx.fill();
  ctx.fillStyle = kalin ? T.yazi : T.soluk;
  ctx.textBaseline = "middle";
  ctx.fillText(metin, x + 8, y + (boy + 12) / 2 + 0.5);
  return boy + 12;
}

function yazilarCiz(S, baslik) {
  const { ctx, W, H, tema: T, veri: V } = S;
  ctx.save();
  let y = 10;
  y += kutuYazi(S, V.etiket, 10, y, 12.5, false) + 6;
  if (baslik) kutuYazi(S, baslik, 10, y, 17, true);
  // lejant: biçim satırı, renk satırı
  const satirlar = [[["ölçülen (dolu)", null, true], ["tahmin (halka)", null, false]],
    (V.lejant || []).map(([ad, h]) => [ad, h, null])];
  ctx.font = `500 12px ${FONT}`;
  const genislik = satirlar.map((s) => s.reduce((t, [ad]) => t + 22 + ctx.measureText(ad).width + 10, 0));
  const kw = Math.max(...genislik) + 10, kh = satirlar.length * 20 + 10;
  ctx.fillStyle = T.kutu;
  ctx.beginPath(); ctx.roundRect(10, H - kh - 10, kw, kh, 7); ctx.fill();
  satirlar.forEach((satir, i) => {
    let x = 20;
    const yy = H - kh - 10 + 15 + i * 20;
    satir.forEach(([ad, renk, olculu]) => {
      const c = renk || T.soluk;
      ctx.beginPath(); ctx.arc(x + 6, yy, 5.5, 0, PI2);
      if (olculu === false) { ctx.lineWidth = 2; ctx.strokeStyle = c; ctx.stroke(); }
      else {
        ctx.fillStyle = c; ctx.fill();
        if (olculu) { ctx.lineWidth = 2; ctx.strokeStyle = T.kontur; ctx.stroke(); }
      }
      ctx.fillStyle = T.yazi; ctx.textBaseline = "middle";
      ctx.fillText(ad, x + 16, yy + 0.5);
      x += 22 + ctx.measureText(ad).width + 10;
    });
  });
  if (V.zemin.atif) {
    ctx.font = `400 10.5px ${FONT}`; ctx.fillStyle = T.soluk; ctx.textAlign = "right";
    ctx.fillText(`Ada: Natural Earth · Girne: ${V.zemin.atif}`, W - 10, H - 10);
  }
  ctx.restore();
}

function adYaz(S, metin, x, y, alfa) {
  const { ctx, tema: T } = S;
  if (alfa <= 0) return;
  ctx.save();
  ctx.globalAlpha = alfa;
  ctx.font = `600 11.5px ${FONT}`; ctx.textAlign = "center"; ctx.textBaseline = "bottom";
  ctx.lineWidth = 3; ctx.strokeStyle = T.kutu; ctx.strokeText(metin, x, y);
  ctx.fillStyle = T.yazi; ctx.fillText(metin, x, y);
  ctx.restore();
}

function adaBasligi(V, girneOlculu, girneTahmin) { // bütün adanın özeti (animasyonun sonu ve uzak görünüm)
  let olc = girneOlculu, tah = girneTahmin;
  V.kasabalar.forEach((kz) => kz.n.forEach((p) => { if (p.o) olc++; else tah++; }));
  return `Kıbrısçık · ${V.kasabalar.length + 1} şehir · ${olc} trafo ölçüldü, ${tah} trafo tahmin`;
}

function adlarCiz(S, kam, alfa) {
  const { W, H, veri: V } = S;
  if (alfa <= 0) return;
  V.kasabalar.forEach((kz) => {
    const [x, y] = ekran(kam, W, H, kz.x, kz.y - 3.2);
    adYaz(S, kz.ad, x, y, alfa);
  });
  const g = kutuBul(V.sehir.n.map((t) => [t.x, t.y]));
  const [x, y] = ekran(kam, W, H, (g[0] + g[2]) / 2, g[1] - 0.6);
  adYaz(S, V.sehir.ad || "Girne", x, y, alfa);
}

// ---------- normal harita ----------

const ayni = (h, tur, i, ki) => !!h && h.tur === tur && h.i === i && (tur === "sehir" || h.ki === ki);

function etkilesimCiz(S, simdi) {
  const { W, H, veri: V } = S;
  const kam = kamera(S, simdi);
  S.sonKamera = kam;
  zeminCiz(S, kam);
  const r = yaricap(kam.s);
  const gorunur = (x, y) => x > -20 && y > -20 && x < W + 20 && y < H + 20;
  V.kasabalar.forEach((kz, ki) => kz.n.forEach((p, i) => {
    const [x, y] = ekran(kam, W, H, p.x, p.y);
    if (!gorunur(x, y)) return;
    const secili = ayni(S.kart, "kasaba", i, ki);
    if (secili) secimHalkasi(S, x, y, r);
    trafoCiz(S, x, y, r * (secili || ayni(S.uzerinde, "kasaba", i, ki) ? 1.3 : 1), p[V.katman] ?? p.panel, !!p.o);
  }));
  let aktif = !!S.gecisKam;
  let olc = 0, tah = 0;
  V.sehir.n.forEach((t, i) => {
    if (t.o) olc++; else if (t.sinif) tah++;
    const [x, y] = ekran(kam, W, H, t.x, t.y);
    if (!gorunur(x, y)) return;
    const g = S.gecis.get(t.no);
    let once, u = 1, ek = 0;
    if (g) {
      const dt = (simdi - g.t) / 1000;
      u = sinirla(dt / 0.4); ek = vurgu(dt); once = g.sinif;
      if (dt < 0.5) aktif = true; else S.gecis.delete(t.no);
    }
    const secili = ayni(S.kart, "sehir", i);
    if (secili) secimHalkasi(S, x, y, r);
    trafoCiz(S, x, y, r * (1 + ek + (secili || ayni(S.uzerinde, "sehir", i) ? 0.3 : 0)), t.sinif, t.o, once, u);
  });
  adlarCiz(S, kam, sinirla((AD_ESIK - kam.s) / 25));
  yazilarCiz(S, kam.s < AD_ESIK / 2 ? adaBasligi(V, olc, tah) : V.sehir.baslik);
  kartKonumla(S, kam);
  return aktif;
}

function bul(S, ev) { // fare altındaki trafo: {tur: "sehir", i} ya da {tur: "kasaba", ki, i}
  const b = S.tuval.getBoundingClientRect();
  const mx = ev.clientX - b.left, my = ev.clientY - b.top;
  const kam = S.sonKamera;
  if (!kam) return null;
  let en = null, enD = yaricap(kam.s) + 6;
  const dene = (p, h) => {
    const [x, y] = ekran(kam, S.W, S.H, p.x, p.y);
    const d = Math.hypot(x - mx, y - my);
    if (d < enD) { enD = d; en = h; }
  };
  S.veri.kasabalar.forEach((kz, ki) => kz.n.forEach((p, i) => dene(p, { tur: "kasaba", ki, i })));
  S.veri.sehir.n.forEach((t, i) => dene(t, { tur: "sehir", i }));
  return en;
}

function hedefNokta(S, h) {
  if (!h || !S.veri) return null;
  if (h.tur === "sehir") return S.veri.sehir.n[h.i] || null;
  const kz = S.veri.kasabalar[h.ki];
  return kz ? kz.n[h.i] || null : null;
}

function kartYaz(S) {
  const el = S.kart_el;
  const p = hedefNokta(S, S.kart);
  if (!p || !etkilesimde(S)) { S.kart = null; el.style.display = "none"; return; }
  let html = `<div class="ust"><span>${p.baslik}</span><span class="kapat" data-is="kapat">×</span></div><div>${p.metin}</div>`;
  if (S.kart.tur === "sehir") {
    html += p.o ? '<button class="olc kaldir" data-is="olc">Ölçümü kaldır</button>'
      : '<button class="olc" data-is="olc">Ölçülmüş say (cihaz takıldı)</button>';
  }
  el.innerHTML = html;
  el.style.display = "block";
  if (S.sonKamera) kartKonumla(S, S.sonKamera);
}

function kartKonumla(S, kam) {
  const el = S.kart_el;
  const p = hedefNokta(S, S.kart);
  if (!p || el.style.display === "none") return;
  const [x, y] = ekran(kam, S.W, S.H, p.x, p.y);
  const w = el.offsetWidth, h = el.offsetHeight;
  let sol = x + 16;
  if (sol + w > S.W - 8) sol = x - 16 - w;
  el.style.left = `${Math.max(8, sol)}px`;
  el.style.top = `${Math.max(8, Math.min(S.H - h - 8, y - h / 2))}px`;
}

// ---------- animasyon ----------

function cizelgeKur(S) {
  const V = S.veri, A = V.anim, n = V.sehir.n;
  const hiz = V.hiz || 1;
  const K = A.sira.length;
  const sure = A.sira.map((_, k) => (k < 3 ? 3.0 : 8.0 / Math.max(1, K - 3)) * hiz);
  const bas = [];
  let t = 0.6;
  sure.forEach((d) => { bas.push(t); t += d; });
  const acBas = t + BEKLE_SN * hiz, acSon = acBas + ACILIS_SN * hiz;
  const kBas = V.kasabalar.map((_, i) => acSon + 0.2 + i * KASABA_ARA * hiz);
  const son = kBas.length ? kBas[kBas.length - 1] + 1.4 : acSon + 0.5;
  const kutular = A.sira.map((_, k) => kutuBul(n.filter((_, i) => A.mahalle[i] <= k).map((p) => [p.x, p.y]), 0.35));
  const olcAdim = n.map(() => -1);
  A.sira.forEach((i, k) => { olcAdim[i] = k; });
  const gorunen = (k) => n.filter((_, i) => A.mahalle[i] <= k).length;
  const metin = A.sira.map((_, k) => {
    if (k === 0) return "Girne'de bir mahalle · 1 trafo ölçüldü";
    if (k === 1) return "Sağdaki mahalle · 2 trafo ölçüldü";
    if (k === 2) return "Soldaki mahalle · 3 ölçüm: model kuruldu, karanlıktaki trafoları tahmin ediyor";
    return `${k + 1} trafo ölçüldü · ${gorunen(k) - k - 1} trafo tahmin`;
  });
  const uzak = n.map((p, i) => {
    const m = n[A.sira[A.mahalle[i]]];
    return Math.hypot(p.x - m.x, p.y - m.y);
  });
  const enUzak = A.sira.map((_, k) => Math.max(0.01, ...uzak.filter((_, i) => A.mahalle[i] === k)));
  return {
    sure, bas, acBas, acSon, kBas, son, kutular, olcAdim, metin,
    olcT: bas.map((b, k) => b + 0.35 * sure[k]),
    renkT: A.adimlar.map((a, k) => (a ? bas[k] + 0.7 * sure[k] : null)),
    gorT: n.map((_, i) => {
      const k = A.mahalle[i];
      return olcAdim[i] >= 0 ? bas[k] + 0.1 : bas[k] + 0.15 * sure[k] + 0.25 * (uzak[i] / enUzak[k]);
    }),
    kSira: V.kasabalar.map((kz) => {
      let j = 0;
      const no = kz.n.filter((p) => p.o).length || 1;
      return kz.n.map((p) => (p.o ? j++ / no : 0));
    }),
    kUzak: V.kasabalar.map((kz) => {
      const d = kz.n.map((p) => Math.hypot(p.x - kz.x, p.y - kz.y));
      const en = Math.max(...d, 0.01);
      return d.map((v) => v / en);
    }),
  };
}

function sinifAl(adim, katman, i) {
  if (!adim) return null;
  const dizi = adim[katman] || adim.panel;
  return dizi ? dizi[i] : null;
}

function oynatCiz(S, simdi) {
  const { ctx, W, H, veri: V, tema: T } = S;
  const C = S.cizelge, A = V.anim, n = V.sehir.n, katman = V.katman;
  const t = ((S.durdu ?? simdi) - S.t0) / 1000;
  let k = 0;
  while (k + 1 < C.bas.length && C.bas[k + 1] <= t) k++;
  const girneSon = sigdir(C.kutular[C.kutular.length - 1], W, H, 1.15);
  let kam;
  if (t < C.acBas) {
    const hedef = sigdir(C.kutular[k], W, H, 1.3);
    const once = sigdir(C.kutular[Math.max(0, k - 1)], W, H, 1.3);
    kam = k === C.bas.length - 1 && t > C.bas[k] + KAMERA_SN
      ? karistir(hedef, girneSon, yumusak(sinirla((t - C.bas[k] - KAMERA_SN) / 1.2)))
      : karistir(once, hedef, yumusak(sinirla((t - C.bas[k]) / KAMERA_SN)));
  } else {
    kam = karistir(girneSon, adaKam(S), yumusak(sinirla((t - C.acBas) / (C.acSon - C.acBas))));
  }
  S.sonAnimKam = kam;
  const acik = yumusak(sinirla((t - C.acBas) / (C.acSon - C.acBas)));

  // zemin: ölçülmeyen her yer karanlık, ölçülen trafonun çevresi küçük aydınlık daire; adaya açılırken karanlık kalkar
  zeminCiz(S, kam);
  const karanlik = KARANLIK * (1 - acik);
  if (karanlik > 0.001) {
    ctx.fillStyle = `rgba(4,7,11,${karanlik})`;
    ctx.fillRect(0, 0, W, H);
    const daireler = () => {
      ctx.beginPath();
      A.sira.forEach((ti, j) => {
        const p = pop(t - C.olcT[j], DAIRE_POP);
        if (p <= 0) return;
        const [x, y] = ekran(kam, W, H, n[ti].x, n[ti].y);
        const rr = Math.max(DAIRE_EN_AZ_PX, DAIRE_KM * kam.s) * p;
        ctx.moveTo(x + rr, y);
        ctx.arc(x, y, rr, 0, PI2);
      });
    };
    ctx.save(); daireler(); ctx.clip(); zeminCiz(S, kam); ctx.restore();
    ctx.globalAlpha = 1 - acik; daireler(); ctx.lineWidth = 1.5; ctx.strokeStyle = T.cember; ctx.stroke();
    ctx.globalAlpha = 1;
  }

  const r = yaricap(kam.s);
  let renkK = -1;
  C.renkT.forEach((rt, j) => { if (rt !== null && rt <= t) renkK = j; });
  n.forEach((p, i) => {
    const olcek = pop(t - C.gorT[i], NOKTA_POP);
    if (olcek <= 0) return;
    const oa = C.olcAdim[i];
    const olculu = oa >= 0 && t >= C.olcT[oa];
    let sinif = null, once, u = 1, ek = 0;
    if (renkK >= 0) {
      sinif = sinifAl(A.adimlar[renkK], katman, i);
      const onceki = renkK > 0 ? sinifAl(A.adimlar[renkK - 1], katman, i) : null;
      const dt = t - C.renkT[renkK];
      if (onceki !== sinif && dt < 0.5) { once = onceki; u = sinirla(dt / 0.4); ek += vurgu(dt); }
    }
    if (olculu) ek += vurgu(t - C.olcT[oa], 0.5);
    const [x, y] = ekran(kam, W, H, p.x, p.y);
    trafoCiz(S, x, y, r * olcek * (1 + ek), sinif, olculu, once, u);
  });

  let kasaba = -1;
  V.kasabalar.forEach((kz, ki) => {
    const tb = C.kBas[ki];
    if (t < tb) return;
    kasaba = ki;
    kz.n.forEach((p, j) => {
      const gor = p.o ? tb + 0.3 * C.kSira[ki][j] : tb + 0.35 + 0.55 * C.kUzak[ki][j];
      const olcek = pop(t - gor, NOKTA_POP);
      if (olcek <= 0) return;
      const [x, y] = ekran(kam, W, H, p.x, p.y);
      trafoCiz(S, x, y, r * olcek, p[katman] ?? p.panel, !!p.o);
    });
    const [x, y] = ekran(kam, W, H, kz.x, kz.y - 3.2);
    adYaz(S, kz.ad, x, y, sinirla((t - tb) / 0.4));
  });
  if (t > C.acBas) {
    const g = C.kutular[C.kutular.length - 1];
    const [x, y] = ekran(kam, W, H, (g[0] + g[2]) / 2, g[1] - 0.6);
    adYaz(S, V.sehir.ad || "Girne", x, y, acik);
  }

  const girneOlc = A.sira.length, girneTah = n.length - A.sira.length;
  let baslik;
  if (t < C.acBas - BEKLE_SN) baslik = C.metin[k];
  else if (t < C.acBas) baslik = `Girne · ${girneOlc} trafo ölçüldü, ${girneTah} trafo tahmin`;
  else if (kasaba < 0) baslik = "Kıbrısçık · öbür şehirler kasabalara";
  else if (t < C.son) {
    const kz = V.kasabalar[kasaba], o = kz.n.filter((p) => p.o).length;
    baslik = `${kz.ad} · ${o} trafo ölçüldü, ${kz.n.length - o} trafo tahmin`;
  } else baslik = adaBasligi(V, girneOlc, girneTah);
  yazilarCiz(S, baslik);

  if (t >= C.son && S.bittiNo !== S.oynatNo) {
    S.bittiNo = S.oynatNo;
    S.tetik("bitti", { no: S.oynatNo, t: Date.now() });
    dugmeleriGuncelle(S);
  }
  return S.durdu === null && t < C.son + 0.1;
}

// ---------- kabuk ----------

function etkilesimde(S) {
  return !!S.veri && !(S.veri.oynat && S.cizelge);
}

function ciz(S, simdi) {
  const { ctx, W, H, veri: V } = S;
  if (!W || !H || !V) return false;
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = S.tema.bos;
  ctx.fillRect(0, 0, W, H);
  return etkilesimde(S) ? etkilesimCiz(S, simdi) : oynatCiz(S, simdi);
}

function dongu(S) {
  if (S.calisiyor) return;
  S.calisiyor = true;
  const adim = () => {
    if (!S.kok.isConnected) { S.calisiyor = false; return; }
    const aktif = ciz(S, performance.now());
    if (aktif || S.kirli) { S.kirli = false; requestAnimationFrame(adim); } else S.calisiyor = false;
  };
  requestAnimationFrame(adim);
}

function boyutla(S) {
  const W = S.kok.clientWidth, H = S.veri ? S.veri.yukseklik : 600;
  const dpr = window.devicePixelRatio || 1;
  if (W === S.W && H === S.H && dpr === S.dpr) return;
  Object.assign(S, { W, H, dpr });
  S.tuval.width = Math.round(W * dpr);
  S.tuval.height = Math.round(H * dpr);
  S.tuval.style.height = `${H}px`;
  S.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  if (!S.kamElle) S.kam = null; // elle oynanmadıysa açılış görünümü yeni boyuta yeniden sığsın
  S.kirli = true;
  dongu(S);
}

function dugmeleriGuncelle(S) {
  const d = S.dugmeler;
  S.yakinlik.style.display = etkilesimde(S) ? "flex" : "none";
  if (etkilesimde(S) || S.bittiNo === S.oynatNo) { d.style.display = "none"; d.dataset.durum = ""; return; }
  const liste = [[S.durdu ? "devam" : "duraklat", S.durdu ? "▶ Devam" : "❚❚ Duraklat"], ["bastan", "↺ Baştan"]];
  const durum = liste.map(([is]) => is).join(",");
  if (d.dataset.durum !== durum) {
    d.innerHTML = liste.map(([is, ad]) => `<button data-is="${is}">${ad}</button>`).join("");
    d.dataset.durum = durum;
  }
  d.style.display = "flex";
}

function dugmeIsle(S, is) {
  const mx = S.W / 2, my = S.H / 2 + UST_PAY / 2;
  if (is === "duraklat") S.durdu = performance.now();
  else if (is === "devam") { S.t0 += performance.now() - S.durdu; S.durdu = null; }
  else if (is === "art") { S.kamElle = true; yakinlas(S, 1.8, mx, my, true); }
  else if (is === "eks") { S.kamElle = true; yakinlas(S, 1 / 1.8, mx, my, true); }
  else if (is === "girne") { S.kamElle = true; kameraGit(S, girneKam(S)); }
  else if (is === "ada") { S.kamElle = true; kameraGit(S, adaKam(S)); }
  else S.tetik(is, Date.now());
  dugmeleriGuncelle(S);
  S.kirli = true;
  dongu(S);
}

function kur(parent) {
  const kok = document.createElement("div");
  kok.className = "kok";
  const tuval = document.createElement("canvas");
  const kart = document.createElement("div");
  kart.className = "kart";
  const dugmeler = document.createElement("div");
  dugmeler.className = "dugmeler";
  const yakinlik = document.createElement("div");
  yakinlik.className = "yakinlik";
  yakinlik.innerHTML = '<div class="sira"><button class="kare" data-is="art" title="Yakınlaş">+</button>'
    + '<button class="kare" data-is="eks" title="Uzaklaş">−</button></div>'
    + '<div class="sira"><button data-is="girne">Girne</button><button data-is="ada">Kıbrıs</button></div>';
  kok.append(tuval, kart, dugmeler, yakinlik);
  parent.appendChild(kok);
  const S = {
    kok, tuval, ctx: tuval.getContext("2d"), kart_el: kart, dugmeler, yakinlik, veri: null, tema: TEMA.acik,
    W: 0, H: 0, dpr: 0, kam: null, gecisKam: null, kamElle: false, sonKamera: null, sonAnimKam: null, adaKutu: null,
    oynatNo: null, t0: 0, durdu: null, bittiNo: null, cizelge: null, gecis: new Map(), onceki: new Map(),
    kart: null, uzerinde: null, surukle: null, calisiyor: false, kirli: true, tetik: () => {},
  };
  new ResizeObserver(() => boyutla(S)).observe(kok);
  const konum = (ev) => {
    const b = tuval.getBoundingClientRect();
    return [ev.clientX - b.left, ev.clientY - b.top];
  };
  tuval.addEventListener("mousedown", (ev) => {
    if (!etkilesimde(S)) return;
    S.surukle = { x: ev.clientX, y: ev.clientY, kam: kamera(S, performance.now()), hareket: false };
    S.gecisKam = null;
  });
  window.addEventListener("mousemove", (ev) => {
    if (!S.kok.isConnected) return;
    const g = S.surukle;
    if (g) {
      const dx = ev.clientX - g.x, dy = ev.clientY - g.y;
      if (!g.hareket && Math.hypot(dx, dy) > 4) g.hareket = true;
      if (g.hareket) {
        S.kam = { cx: g.kam.cx - dx / g.kam.s, cy: g.kam.cy - dy / g.kam.s, s: g.kam.s };
        S.kamElle = true; S.kirli = true; dongu(S);
      }
      return;
    }
    if (ev.target !== tuval || !etkilesimde(S)) return;
    const h = bul(S, ev);
    if (JSON.stringify(h) !== JSON.stringify(S.uzerinde)) { S.uzerinde = h; S.kirli = true; dongu(S); }
    tuval.style.cursor = h ? "pointer" : "grab";
  });
  window.addEventListener("mouseup", (ev) => {
    const g = S.surukle;
    S.surukle = null;
    if (!g || g.hareket || !etkilesimde(S) || !S.kok.isConnected) return;
    const h = bul(S, ev); // tıklama: trafo kartı aç; aynı trafo ya da boş yer kapatır
    S.kart = h && JSON.stringify(h) !== JSON.stringify(S.kart) ? h : null;
    kartYaz(S);
    S.kirli = true; dongu(S);
  });
  tuval.addEventListener("mouseleave", () => { if (S.uzerinde) { S.uzerinde = null; S.kirli = true; dongu(S); } });
  tuval.addEventListener("wheel", (ev) => {
    if (!etkilesimde(S)) return;
    ev.preventDefault();
    S.kamElle = true;
    yakinlas(S, Math.exp(-ev.deltaY * 0.0015), ...konum(ev));
  }, { passive: false });
  tuval.addEventListener("dblclick", (ev) => {
    if (!etkilesimde(S)) return;
    S.kamElle = true;
    yakinlas(S, 2, ...konum(ev), true);
  });
  kart.addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-is]");
    if (!b) return;
    const p = hedefNokta(S, S.kart);
    if (b.dataset.is === "kapat" || !p) { S.kart = null; kartYaz(S); S.kirli = true; dongu(S); }
    else if (b.dataset.is === "olc") S.tetik("tiklama", { no: p.no, t: Date.now() });
  });
  const dugmeTik = (ev) => {
    const b = ev.target.closest("button");
    if (b) dugmeIsle(S, b.dataset.is);
  };
  dugmeler.addEventListener("click", dugmeTik);
  yakinlik.addEventListener("click", dugmeTik);
  return S;
}

function guncelle(S, veri) {
  const ilk = !S.veri;
  if (ilk || JSON.stringify(S.veri.zemin.yama) !== JSON.stringify(veri.zemin.yama) || !S.adaKutu) {
    S.adaKutu = adaKutusu(veri.zemin);
  }
  S.veri = veri;
  S.kok.style.height = `${veri.yukseklik}px`;
  S.tema = temaBul(S.kok);
  boyutla(S);
  if (veri.oynat && veri.anim) {
    if (veri.oynat_no !== S.oynatNo) {
      S.oynatNo = veri.oynat_no; S.t0 = performance.now(); S.durdu = null; S.cizelge = cizelgeKur(S);
    }
  } else {
    if (S.cizelge && S.sonAnimKam) { S.kam = S.sonAnimKam; S.gecisKam = null; S.kamElle = true; } // bittiği yerden
    S.oynatNo = null; S.cizelge = null; S.durdu = null;
  }
  const simdi = performance.now();
  veri.sehir.n.forEach((t) => {
    const o = S.onceki.get(t.no);
    if (!ilk && o && (o.sinif !== t.sinif || o.o !== t.o)) S.gecis.set(t.no, { sinif: o.sinif, t: simdi });
    S.onceki.set(t.no, { sinif: t.sinif, o: t.o });
  });
  kartYaz(S);
  dugmeleriGuncelle(S);
  S.kirli = true;
  dongu(S);
}

export default function (component) {
  const { data, parentElement, setTriggerValue } = component;
  let S = parentElement.__canliHarita;
  if (!S || !S.kok.isConnected) {
    S = kur(parentElement);
    parentElement.__canliHarita = S;
  }
  S.tetik = setTriggerValue;
  guncelle(S, data);
}
