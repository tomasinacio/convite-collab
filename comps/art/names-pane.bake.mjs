// Bakes comps/art/names-pane.svg: a small 4 x 2 azulejo pane for the names (prototype, r8).
// owner: Tomas | 2026-11-10 | run: node comps/art/names-pane.bake.mjs
// No SVG filters (red team, 2026-11-10): brush strokes are variable-width filled outlines, the glaze is flat tints
// with one highlight edge, the grout is drawn over the paint. Brush model adapted from comps/azulejo-lab.html.
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const OUT = fileURLToPath(new URL('./names-pane.svg', import.meta.url));
const T = 100, COLS = 4, ROWS = 2, W = COLS * T, H = ROWS * T;
const C = {
  line: '#4E6B8D', pool: '#3F5A7C', wash: '#7F9BA8', pale: '#B9C8D3',
  glaze: ['#F4EDE0', '#F2EBDD', '#F5EFE3', '#F1EADC'], grout: '#DBD1BD', bed: '#E5DBC7', chip: '#DED2BB'
};

function RNG(seed){let s=seed>>>0;return()=>{s=(s+0x6D2B79F5)>>>0;let t=s;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296;};}
const rnd = RNG(808);
const f1 = n => Math.round(n * 10) / 10;
const P = (x, y) => f1(x) + ' ' + f1(y);
const smooth = x => x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x);

// sampling: straight line or cubic, about one point per unit
// a hand-ruled line: a gentle bow and a slow waver, never dead straight
function line(a, b, bow = (rnd() - .5) * 1.4){const L=Math.hypot(b[0]-a[0],b[1]-a[1]),n=Math.max(4,Math.ceil(L/3.5)),nx=-(b[1]-a[1])/L,ny=(b[0]-a[0])/L,ph=rnd()*9;const o=[];for(let i=0;i<=n;i++){const t=i/n,d=Math.sin(Math.PI*t)*bow+.35*Math.sin(t*L/23+ph);o.push([a[0]+(b[0]-a[0])*t+nx*d,a[1]+(b[1]-a[1])*t+ny*d]);}return o;}
function cubic(p0,p1,p2,p3){const n=40;const o=[];for(let i=0;i<=n;i++){const t=i/n,u=1-t;o.push([u*u*u*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0],u*u*u*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1]]);}return o;}

// brush: swells after the touch-down, wobbles a little, tapers or pools at the lift
function widths(pts, st){const n=pts.length,ta=st.ta??.07,tb=st.tb??.2,tip=st.tip??.3,ph=rnd()*20,W=[];
  for(let i=0;i<n;i++){const t=i/(n-1);const a=smooth(t/ta);let b=smooth((1-t)/tb);if(st.pool)b=.7+.3*b;const env=tip+(1-tip)*Math.min(a,b);
    W.push(st.w*env*(1+.1*Math.sin(i*.05+ph)+.05*Math.sin(i*.21+ph*1.7)));}return W;}
function outline(pts, W){const n=pts.length,L=[],R=[];
  const tan=i=>{const a=pts[Math.max(0,i-1)],b=pts[Math.min(n-1,i+1)];const dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy)||1;return[dx/l,dy/l];};
  for(let i=0;i<n;i++){const t=tan(i),h=W[i]/2;L.push([pts[i][0]-t[1]*h,pts[i][1]+t[0]*h]);R.push([pts[i][0]+t[1]*h,pts[i][1]-t[0]*h]);}
  const cap=(p,t,h,s)=>{const o=[];for(let k=1;k<5;k++){const a=Math.PI*k/5;o.push([p[0]+(-t[1])*Math.cos(a)*h*s+t[0]*Math.sin(a)*h*s,p[1]+t[0]*Math.cos(a)*h*s+t[1]*Math.sin(a)*h*s]);}return o;};
  const e=cap(pts[n-1],tan(n-1),W[n-1]/2,1), s=cap(pts[0],tan(0),W[0]/2,-1);
  return [...L,...e,...R.reverse(),...s];}
const poly = pts => 'M' + pts.map(p => P(p[0], p[1])).join('L') + 'Z';
const stroke = (pts, st) => poly(outline(pts, widths(pts, st)));

const paths = []; // [d, fill, opacity]
const add = (d, fill, o = 1) => paths.push([d, fill, o]);

// ---- painted frame: a pale wash band, a fuller fillet outside, a fine one inside; each side its own brush stroke
const j = () => (rnd() - .5) * 1.2;
const o1 = 6.5, o2 = 15;
{ // wash band with slightly uneven edges
  const ring = [];
  const edge = (inset) => { const p = []; const N = 24;
    for (let i = 0; i < N; i++) p.push([inset + (W - 2 * inset) * i / N, inset + j() * .5]);
    for (let i = 0; i < N / 2; i++) p.push([W - inset + j() * .5, inset + (H - 2 * inset) * i / (N / 2)]);
    for (let i = 0; i < N; i++) p.push([W - inset - (W - 2 * inset) * i / N, H - inset + j() * .5]);
    for (let i = 0; i < N / 2; i++) p.push([inset + j() * .5, H - inset - (H - 2 * inset) * i / (N / 2)]);
    return p; };
  const outer = edge(o1 + .5), inner = edge(o2 - .5).reverse();
  add(poly(outer) + poly(inner), C.pale, .42);
}
for (const [inset, w] of [[o1, 2.7], [o2, 1.05]]) {
  const x0 = inset, y0 = inset, x1 = W - inset, y1 = H - inset, ov = 2.5;
  add(stroke(line([x0 - ov, y0 + j() * .4], [x1 + ov * .6, y0 + j() * .4]), { w, pool: true }), C.line, .86);
  add(stroke(line([x1 + j() * .4, y0 - ov * .6], [x1 + j() * .4, y1 + ov]), { w, pool: true }), C.line, .86);
  add(stroke(line([x1 + ov, y1 + j() * .4], [x0 - ov * .6, y1 + j() * .4]), { w, pool: true }), C.line, .86);
  add(stroke(line([x0 + j() * .4, y1 + ov * .6], [x0 + j() * .4, y0 - ov]), { w, pool: true }), C.line, .86);
}
// ---- corner rosettes: four soft petals on the band, a dot at the heart
for (const [cx, cy] of [[o1 + 4.2, o1 + 4.2], [W - o1 - 4.2, o1 + 4.2], [W - o1 - 4.2, H - o1 - 4.2], [o1 + 4.2, H - o1 - 4.2]]) {
  const r = 10.5;
  for (let k = 0; k < 4; k++) {
    const a = (45 + 90 * k) * Math.PI / 180, nx = -Math.sin(a), ny = Math.cos(a), w = r * .42;
    const tip = [cx + Math.cos(a) * r, cy + Math.sin(a) * r];
    const m = [cx + Math.cos(a) * r * .3, cy + Math.sin(a) * r * .3];
    const d = `M${P(cx, cy)}C${P(m[0] + nx * w, m[1] + ny * w)} ${P(tip[0] + nx * w * .6, tip[1] + ny * w * .6)} ${P(tip[0], tip[1])}C${P(tip[0] - nx * w * .6, tip[1] - ny * w * .6)} ${P(m[0] - nx * w, m[1] - ny * w)} ${P(cx, cy)}Z`;
    add(d, C.wash, .5);
  }
  paths.push([`M${P(cx + 2.2, cy)}A2.2 2.2 0 1 1 ${P(cx - 2.2, cy)}A2.2 2.2 0 1 1 ${P(cx + 2.2, cy)}Z`, C.pool, .9]);
}

// ---- corner sprays (red team r8): three small cobalt leaves from each inner corner, two along the fillets, one short on the diagonal
const leafD = (x, y, a, L, w) => { const c = Math.cos(a), s = Math.sin(a), mx = x + c * L * .5, my = y + s * L * .5;
  return `M${P(x, y)}Q${P(mx - s * w, my + c * w)} ${P(x + c * L, y + s * L)}Q${P(mx + s * w, my - c * w)} ${P(x, y)}Z`; };
for (const [sx, sy] of [[1, 1], [-1, 1], [-1, -1], [1, -1]]) {
  const x = sx > 0 ? o2 + 2.5 : W - o2 - 2.5, y = sy > 0 ? o2 + 2.5 : H - o2 - 2.5;
  const base = Math.atan2(sy, sx);
  for (const [da, L, w] of [[-.62, 16, 3.6], [.62, 16, 3.6], [0, 9.5, 2.8]]) {
    const a = base + da + (rnd() - .5) * .12;
    add(leafD(x, y, a, L, w), C.wash, .5);
    add(stroke(line([x + Math.cos(a) * 1.5, y + Math.sin(a) * 1.5], [x + Math.cos(a) * L * .78, y + Math.sin(a) * L * .78], 0), { w: .9, tip: .3 }), C.line, .75);
  }
  paths.push([`M${P(x + 1.5, y)}A1.5 1.5 0 1 1 ${P(x - 1.5, y)}A1.5 1.5 0 1 1 ${P(x + 1.5, y)}Z`, C.pool, .8]);
}

// ---- tiles: glaze tints, a hairline highlight on the lit edges, a faint pooled edge on the others; grout over the paint
const tiles = [], gap = 2.2;
for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
  const x = c * T + gap / 2 + (rnd() - .5) * .8, y = r * T + gap / 2 + (rnd() - .5) * .8, rot = (rnd() - .5) * .5;
  tiles.push({ x, y, w: T - gap + (rnd() - .5) * .6, h: T - gap + (rnd() - .5) * .6, rot, fill: C.glaze[Math.floor(rnd() * C.glaze.length)] });
}
const tileRect = t => `<rect x="${f1(t.x)}" y="${f1(t.y)}" width="${f1(t.w)}" height="${f1(t.h)}" rx="1.6" transform="rotate(${t.rot.toFixed(2)} ${f1(t.x + t.w / 2)} ${f1(t.y + t.h / 2)})"`;

// setting bed: lime mortar a little wider than the pane, edges not ruled
const bed = []; { const m = 4.2, N = 18; const q = () => (rnd() - .5) * 1.6;
  for (let i = 0; i <= N; i++) bed.push([-m + (W + 2 * m) * i / N, -m + q()]);
  for (let i = 1; i <= N / 2; i++) bed.push([W + m + q(), -m + (H + 2 * m) * i / (N / 2)]);
  for (let i = 1; i <= N; i++) bed.push([W + m - (W + 2 * m) * i / N, H + m + q()]);
  for (let i = 1; i < N / 2; i++) bed.push([-m + q(), H + m - (H + 2 * m) * i / (N / 2)]); }

let svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -6 ${W + 12} ${H + 12}" width="${W + 12}" height="${H + 12}">\n`;
svg += `<!-- names pane, 4 x 2 azulejo tiles, baked by names-pane.bake.mjs (prototype r8, 2026-11-10). Authored, no filters. -->\n`;
svg += `<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset=".3" stop-color="#fff" stop-opacity="0"/><stop offset=".44" stop-color="#fff" stop-opacity=".5"/><stop offset=".58" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>\n`;
svg += `<path d="${poly(bed)}" fill="${C.bed}"/>\n<rect x="0" y="0" width="${W}" height="${H}" fill="${C.grout}"/>\n`;
svg += tiles.map(t => tileRect(t) + ` fill="${t.fill}"/>`).join('\n') + '\n';
svg += `<g>` + paths.map(([d, f, o]) => `<path d="${d}" fill="${f}"${o < 1 ? ` fill-opacity="${o}"` : ''}/>`).join('') + `</g>\n`;
// grout lines drawn over the paint, so the painting breaks at each joint like real tiles
let grout = '';
for (let c = 1; c < COLS; c++) grout += `M${P(c * T + (rnd() - .5) * .6, -.5)}L${P(c * T + (rnd() - .5) * .6, H + .5)}`;
for (let r = 1; r < ROWS; r++) grout += `M${P(-.5, r * T + (rnd() - .5) * .6)}L${P(W + .5, r * T + (rnd() - .5) * .6)}`;
svg += `<path d="${grout}" stroke="${C.grout}" stroke-width="${gap}" fill="none"/>\n`;
// glaze: one soft diagonal sheen on two tiles only, lit edges, pooled edges
svg += `<g fill="none">` + tiles.map(t => `<path d="M${P(t.x + .8, t.y + t.h - 2)}V${f1(t.y + .8)}H${f1(t.x + t.w - 2)}" stroke="#fff" stroke-opacity=".7" stroke-width="1"/><path d="M${P(t.x + t.w - .7, t.y + 2)}V${f1(t.y + t.h - .7)}H${f1(t.x + 2)}" stroke="#A89C84" stroke-opacity=".22" stroke-width="1"/>`).join('') + `</g>\n`;
for (const i of [1, 6]) { const t = tiles[i]; svg += `<rect x="${f1(t.x)}" y="${f1(t.y)}" width="${f1(t.w)}" height="${f1(t.h)}" fill="url(#g)" opacity=".55"/>\n`; }
// age: a chipped corner on the top edge of the third tile, and two hairline crazes
{ const t = tiles[2]; const x = t.x + t.w - 14, y = t.y;
  svg += `<path d="M${P(x, y - .4)}L${P(x + 9, y - .4)}L${P(x + 7.5, y + 2.6)}L${P(x + 3.5, y + 3.4)}Z" fill="${C.chip}"/>\n`; }
svg += `<path d="M${P(tiles[5].x + 60, tiles[5].y + 6)}l4 7l-1 6l5 8M${P(tiles[0].x + 70, tiles[0].y + 72)}l6 3l3 7" stroke="#8A8170" stroke-opacity=".18" stroke-width=".5" fill="none"/>\n`;
svg += `</svg>\n`;
writeFileSync(OUT, svg);
console.log(OUT, (svg.length / 1024).toFixed(1) + ' KB');
