// Canlı tahmin haritası (veri ve olaylar: dashboard/canli_harita.py). Kendi çizimimiz, tuval; dış kaynak yok.
// Etkileşim: trafoya tıkla -> "tiklama". Animasyon (veri.oynat): Girne'de mahalle mahalle ölçüm, sonra ada; bitince
// "bitti". Düğmeler: "bastan", "don". Etiket ("gösterim — farazi şehir · noktalar temsili") her karede.
// Ölçülen trafo dolu nokta (kalın kontur), tahmin soluk halka, henüz tahmin yok gri nokta.

const PI2 = Math.PI * 2;
const GUNEY_ALFA = 0.5; // Güney Kıbrıs soluk (Volkan)
const MAHALLE_POP = 0.55; // sn
const NOKTA_POP = 0.45;
const KAMERA_SN = 0.9;
const ACILIS_SN = 3.0;
const BEKLE_SN = 1.6;
const KASABA_ARA = 0.85;
const S_EN_COK = 320; // px/km: en yakın görünüm (bir mahalle)
const UST_PAY = 64; // px: üstteki etiket ve başlık kutusu, harita altında kalmasın
const FONT = '"Source Sans Pro", "Source Sans 3", system-ui, -apple-system, sans-serif';

const TEMA = {
  acik: {
    bos: "#eef1f5", deniz: "#d4e4f0", kara: "#fbfaf5", kiyi: "#8ea8be", bina: "#d6cfc0", yol: "#e7e2d7",
    yazi: "#1f2933", soluk: "#5b6875", kontur: "#14181f", kutu: "rgba(255,255,255,0.88)", cember: "rgba(42,120,214,0.35)",
  },
  koyu: {
    bos: "#11151c", deniz: "#13283c", kara: "#3a404a", kiyi: "#5f7f9b", bina: "#4d5460", yol: "#454c57",
    yazi: "#e8edf2", soluk: "#9aa7b4", kontur: "#f4f6f8", kutu: "rgba(20,24,31,0.86)", cember: "rgba(110,170,240,0.4)",
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
function sigdir(k, W, H, pay = 1.2, sMax = S_EN_COK) { // kutu, üst pay dışındaki alana sığsın
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

// ---------- etkileşim görünümü ----------

function etkilesimCiz(S, simdi) {
  const { W, H, veri: V } = S;
  const n = V.sehir.n;
  const kam = sigdir(kutuBul(n.map((t) => [t.x, t.y]), 0.3), W, H, 1.12);
  S.sonKamera = kam;
  zeminCiz(S, kam);
  const r = yaricap(kam.s);
  let aktif = false;
  n.forEach((t, i) => {
    const [px, py] = ekran(kam, W, H, t.x, t.y);
    const g = S.gecis.get(t.no);
    let once, u = 1, ek = 0;
    if (g) {
      const dt = (simdi - g.t) / 1000;
      u = sinirla(dt / 0.4); ek = vurgu(dt); once = g.sinif;
      if (dt < 0.5) aktif = true; else S.gecis.delete(t.no);
    }
    trafoCiz(S, px, py, r * (1 + ek + (S.uzerinde === i ? 0.25 : 0)), t.sinif, t.o, once, u);
  });
  yazilarCiz(S, V.sehir.baslik);
  return aktif;
}

// ---------- animasyon ----------

function cizelgeKur(S) {
  const A = S.veri.anim, n = S.veri.sehir.n, z = S.veri.zemin;
  const hiz = S.veri.hiz || 1;
  const K = A.sira.length;
  const sure = A.sira.map((_, k) => (k < 3 ? 3.0 : 8.0 / Math.max(1, K - 3)) * hiz);
  const bas = [];
  let t = 0.3;
  sure.forEach((d) => { bas.push(t); t += d; });
  const acBas = t + BEKLE_SN * hiz, acSon = acBas + ACILIS_SN * hiz;
  const kBas = A.kasabalar.map((_, i) => acSon + 0.2 + i * KASABA_ARA * hiz);
  const son = kBas.length ? kBas[kBas.length - 1] + 1.4 : acSon + 0.5;
  const mahalle = A.sira.map((_, k) => {
    const uye = n.filter((_, i) => A.mahalle[i] === k);
    const x = uye.reduce((a, p) => a + p.x, 0) / uye.length, y = uye.reduce((a, p) => a + p.y, 0) / uye.length;
    const r = Math.max(0.6, Math.max(...uye.map((p) => Math.hypot(p.x - x, p.y - y))) + 0.35);
    return { x, y, r };
  });
  const kutular = mahalle.map((_, k) => kutuBul(mahalle.slice(0, k + 1).map((m) => [m.x, m.y, m.r])));
  const olcAdim = n.map(() => -1);
  A.sira.forEach((i, k) => { olcAdim[i] = k; });
  const gorunen = (k) => n.filter((_, i) => A.mahalle[i] <= k).length;
  const metin = A.sira.map((_, k) => {
    if (k === 0) return "Girne'de bir mahalle · 1 trafo ölçüldü";
    if (k === 1) return "Sağdaki mahalle · 2 trafo ölçüldü";
    if (k === 2) return "Soldaki mahalle · 3 ölçüm: model kuruldu, görünen trafoları tahmin ediyor";
    return `${k + 1} trafo ölçüldü · ${gorunen(k) - k - 1} trafo tahmin`;
  });
  const olcToplam = K + A.kasabalar.reduce((a, kz) => a + kz.n.filter((p) => p.o).length, 0);
  const toplam = n.length + A.kasabalar.reduce((a, kz) => a + kz.n.length, 0);
  return {
    sure, bas, acBas, acSon, kBas, son, mahalle, kutular, olcAdim, metin,
    olcT: bas.map((b, k) => b + 0.45 * sure[k]),
    renkT: A.adimlar.map((a, k) => (a ? bas[k] + 0.7 * sure[k] : null)),
    gecikme: n.map((p, i) => {
      const m = mahalle[A.mahalle[i]];
      return Math.min(0.3, (0.3 * Math.hypot(p.x - m.x, p.y - m.y)) / m.r);
    }),
    kSira: A.kasabalar.map((kz) => {
      let j = 0;
      const no = kz.n.filter((p) => p.o).length || 1;
      return kz.n.map((p) => (p.o ? j++ / no : 0));
    }),
    kUzak: A.kasabalar.map((kz) => {
      const d = kz.n.map((p) => Math.hypot(p.x - kz.x, p.y - kz.y));
      const en = Math.max(...d, 0.01);
      return d.map((v) => v / en);
    }),
    ada: kutuBul([...z.kuzey, ...z.guney].flatMap((h) => {
      const p = [];
      for (let i = 0; i < h.length; i += 2) p.push([h[i], h[i + 1]]);
      return p;
    })),
    sonYazi: `Ada · ${A.kasabalar.length + 1} deneme şehri · ${olcToplam} trafo ölçüldü, ${toplam - olcToplam} trafo tahmin`,
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
  const ada = sigdir(C.ada, W, H, 1.06);
  let kam;
  if (t < C.acBas) {
    const hedef = sigdir(C.kutular[k], W, H, 1.3);
    const once = sigdir(C.kutular[Math.max(0, k - 1)], W, H, 1.3);
    kam = k === C.bas.length - 1 && t > C.bas[k] + KAMERA_SN
      ? karistir(hedef, girneSon, yumusak(sinirla((t - C.bas[k] - KAMERA_SN) / 1.2)))
      : karistir(once, hedef, yumusak(sinirla((t - C.bas[k]) / KAMERA_SN)));
  } else {
    kam = karistir(girneSon, ada, yumusak(sinirla((t - C.acBas) / (C.acSon - C.acBas))));
  }
  const acik = yumusak(sinirla((t - C.acBas) / (C.acSon - C.acBas)));

  // zemin: dışı kapalı, açılan mahalleler pencere gibi; adaya açılırken her yer belirir
  if (acik > 0) { ctx.globalAlpha = acik; zeminCiz(S, kam); ctx.globalAlpha = 1; }
  if (acik < 1) {
    const cember = () => {
      ctx.beginPath();
      C.mahalle.forEach((m, j) => {
        const p = pop(t - C.bas[j], MAHALLE_POP);
        if (p <= 0) return;
        const [x, y] = ekran(kam, W, H, m.x, m.y);
        ctx.moveTo(x + m.r * kam.s * p, y);
        ctx.arc(x, y, m.r * kam.s * p, 0, PI2);
      });
    };
    ctx.save(); cember(); ctx.clip(); zeminCiz(S, kam); ctx.restore();
    ctx.globalAlpha = 1 - acik; cember(); ctx.lineWidth = 1.5; ctx.strokeStyle = T.cember; ctx.stroke();
    ctx.globalAlpha = 1;
  }

  const r = yaricap(kam.s);
  let renkK = -1;
  C.renkT.forEach((rt, j) => { if (rt !== null && rt <= t) renkK = j; });
  n.forEach((p, i) => {
    const olcek = pop(t - (C.bas[A.mahalle[i]] + 0.2 + C.gecikme[i]), NOKTA_POP);
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
  A.kasabalar.forEach((kz, ki) => {
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
    adYaz(S, "Girne", x, y, acik);
  }

  let baslik;
  if (t < C.acBas - BEKLE_SN) baslik = C.metin[k];
  else if (t < C.acBas) baslik = `Girne · ${C.olcAdim.filter((o) => o >= 0).length} trafo ölçüldü, ${n.length - A.sira.length} trafo tahmin`;
  else if (kasaba < 0) baslik = "Kıbrıs · öbür deneme şehirleri kasabalara";
  else if (t < C.son) {
    const kz = A.kasabalar[kasaba], o = kz.n.filter((p) => p.o).length;
    baslik = `${kz.ad} · ${o} trafo ölçüldü, ${kz.n.length - o} trafo tahmin`;
  } else baslik = C.sonYazi;
  yazilarCiz(S, baslik);

  if (t >= C.son && S.bittiNo !== S.oynatNo) {
    S.bittiNo = S.oynatNo;
    S.tetik("bitti", { no: S.oynatNo, t: Date.now() });
    dugmeleriGuncelle(S);
  }
  return S.durdu === null && t < C.son + 0.1;
}

// ---------- kabuk ----------

function ciz(S, simdi) {
  const { ctx, W, H, veri: V } = S;
  if (!W || !H || !V) return false;
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = S.tema.bos;
  ctx.fillRect(0, 0, W, H);
  return V.oynat && S.cizelge ? oynatCiz(S, simdi) : etkilesimCiz(S, simdi);
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
  S.kirli = true;
  dongu(S);
}

function dugmeleriGuncelle(S) {
  const d = S.dugmeler;
  if (!S.veri.oynat || !S.cizelge) { d.style.display = "none"; d.dataset.durum = ""; return; }
  const bitti = S.bittiNo === S.oynatNo;
  const liste = bitti ? [["bastan", "↺ Baştan oynat"], ["don", "Girne'ye dön"]]
    : [[S.durdu ? "devam" : "duraklat", S.durdu ? "▶ Devam" : "❚❚ Duraklat"], ["bastan", "↺ Baştan"]];
  const durum = liste.map(([is]) => is).join(",");
  if (d.dataset.durum !== durum) {
    d.innerHTML = liste.map(([is, ad]) => `<button data-is="${is}">${ad}</button>`).join("");
    d.dataset.durum = durum;
  }
  d.style.display = "flex";
}

function dugmeIsle(S, is) {
  if (is === "duraklat") S.durdu = performance.now();
  else if (is === "devam") { S.t0 += performance.now() - S.durdu; S.durdu = null; }
  else S.tetik(is, Date.now());
  dugmeleriGuncelle(S);
  S.kirli = true;
  dongu(S);
}

const etkilesimde = (S) => S.veri && !(S.veri.oynat && S.cizelge) && S.sonKamera;

function enYakin(S, ev) { // fare altındaki trafo (sırası) ya da null
  const b = S.tuval.getBoundingClientRect();
  const mx = ev.clientX - b.left, my = ev.clientY - b.top;
  const kam = S.sonKamera;
  let en = null, enD = yaricap(kam.s) + 6;
  S.veri.sehir.n.forEach((t, i) => {
    const [x, y] = ekran(kam, S.W, S.H, t.x, t.y);
    const d = Math.hypot(x - mx, y - my);
    if (d < enD) { enD = d; en = i; }
  });
  return [en, mx, my];
}

function fareHareket(S, ev) {
  const ip = S.ipucu;
  if (!etkilesimde(S)) { ip.style.display = "none"; return; }
  const [en, mx, my] = enYakin(S, ev);
  if (en !== S.uzerinde) { S.uzerinde = en; S.kirli = true; dongu(S); }
  S.tuval.style.cursor = en === null ? "default" : "pointer";
  if (en === null) { ip.style.display = "none"; return; }
  const t = S.veri.sehir.n[en];
  ip.innerHTML = `<b>${t.baslik}</b><br/>${t.metin}`;
  ip.style.display = "block";
  const sag = mx + 16 + ip.offsetWidth > S.W;
  ip.style.left = `${sag ? mx - 16 - ip.offsetWidth : mx + 16}px`;
  ip.style.top = `${Math.min(my + 12, S.H - ip.offsetHeight - 8)}px`;
}

function kur(parent) {
  const kok = document.createElement("div");
  kok.className = "kok";
  const tuval = document.createElement("canvas");
  const ipucu = document.createElement("div");
  ipucu.className = "ipucu";
  const dugmeler = document.createElement("div");
  dugmeler.className = "dugmeler";
  kok.append(tuval, ipucu, dugmeler);
  parent.appendChild(kok);
  const S = {
    kok, tuval, ctx: tuval.getContext("2d"), ipucu, dugmeler, veri: null, tema: TEMA.acik, W: 0, H: 0, dpr: 0,
    oynatNo: null, t0: 0, durdu: null, bittiNo: null, cizelge: null, gecis: new Map(), onceki: new Map(),
    uzerinde: null, sonKamera: null, calisiyor: false, kirli: true, tetik: () => {},
  };
  new ResizeObserver(() => boyutla(S)).observe(kok);
  tuval.addEventListener("mousemove", (ev) => fareHareket(S, ev));
  tuval.addEventListener("mouseleave", () => {
    S.uzerinde = null; ipucu.style.display = "none"; S.kirli = true; dongu(S);
  });
  tuval.addEventListener("click", (ev) => {
    if (!etkilesimde(S)) return;
    const [en] = enYakin(S, ev);
    if (en !== null) S.tetik("tiklama", { no: S.veri.sehir.n[en].no, t: Date.now() });
  });
  dugmeler.addEventListener("click", (ev) => {
    const b = ev.target.closest("button");
    if (b) dugmeIsle(S, b.dataset.is);
  });
  return S;
}

function guncelle(S, veri) {
  const ilk = !S.veri;
  S.veri = veri;
  S.kok.style.height = `${veri.yukseklik}px`;
  S.tema = temaBul(S.kok);
  if (veri.oynat && veri.anim) {
    if (veri.oynat_no !== S.oynatNo) {
      S.oynatNo = veri.oynat_no; S.t0 = performance.now(); S.durdu = null; S.cizelge = cizelgeKur(S);
      S.ipucu.style.display = "none";
    }
  } else {
    S.oynatNo = null; S.cizelge = null; S.durdu = null;
  }
  const simdi = performance.now();
  veri.sehir.n.forEach((t) => {
    const o = S.onceki.get(t.no);
    if (!ilk && o && (o.sinif !== t.sinif || o.o !== t.o)) S.gecis.set(t.no, { sinif: o.sinif, t: simdi });
    S.onceki.set(t.no, { sinif: t.sinif, o: t.o });
  });
  dugmeleriGuncelle(S);
  boyutla(S);
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
