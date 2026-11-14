== run_id: 20261112-171526-1600761-nvidia_nvidia_nemotron-3-ultra-550b-a55b ==
jail: WARNING using the MAIN router key; run delegate/set-key.sh with a dedicated one
[0m
> researcher · nvidia/nvidia/nemotron-3-ultra-550b-a55b
[0m
[0m→ [0mSkill "grounded-citations"
[0m% [0mWebFetch http://127.0.0.1:8790/search?q=Playwright+getComputedStyle+design+audit+color+extraction+CSS+stats+free+tool
[0m% [0mWebFetch http://127.0.0.1:8790/search?q=CSS-stats+design-lint+free+tool+audit+colors+fonts+spacing+rhythm
[0m% [0mWebFetch http://127.0.0.1:8790/search?q=visual+diff+Playwright+pixelmatch+resemble.js+free+tool+color+palette+extraction+library
[0m% [0mWebFetch http://127.0.0.1:8790/search?q=color+extraction+library+JavaScript+getComputedStyle+palette+CSS+color+analysis+free+open+source
[0m% [0mWebFetch http://127.0.0.1:8790/search?q=CSS+stats+design+audit+CLI+tool+colors+fonts+spacing+rhythm+open+source+free
[0m✗ [0mWebFetch https://www.smashingmagazine.com/2021/03/css-auditing-tools failed
[91m[1mError: [0mTransport error (GET https://www.smashingmagazine.com/2021/03/css-auditing-tools)
[0m✗ [0mWebFetch https://css-tricks.com/a-quick-css-audit-and-general-notes-about-design-systems failed
[91m[1mError: [0mTransport error (GET https://css-tricks.com/a-quick-css-audit-and-general-notes-about-design-systems)
[0m✗ [0mWebFetch https://www.projectwallace.com failed
[91m[1mError: [0mTransport error (GET https://www.projectwallace.com)
[0m% [0mWebFetch http://127.0.0.1:8790/fetch?url=https%3A%2F%2Fcss-tricks.com%2Fa-quick-css-audit-and-general-notes-about-design-systems
[0m% [0mWebFetch http://127.0.0.1:8790/fetch?url=https%3A%2F%2Fwww.smashingmagazine.com%2F2021%2F03%2Fcss-auditing-tools
[0m✗ [0mWebFetch https://github.com/bartveneman/wallace-cli failed
[91m[1mError: [0mTransport error (GET https://github.com/bartveneman/wallace-cli)
[0m% [0mWebFetch http://127.0.0.1:8790/fetch?url=https%3A%2F%2Fgithub.com%2Fbartveneman%2Fwallace-cli
[0m✗ [0mWebFetch https://github.com/bartveneman/gromit-cli failed
[91m[1mError: [0mTransport error (GET https://github.com/bartveneman/gromit-cli)
[0m% [0mWebFetch http://127.0.0.1:8790/fetch?url=https%3A%2F%2Fgithub.com%2Fbartveneman%2Fgromit-cli
[0m✗ [0mWebFetch https://github.com/mapbox/pixelmatch failed
[91m[1mError: [0mTransport error (GET https://github.com/mapbox/pixelmatch)
[0m% [0mWebFetch http://127.0.0.1:8790/fetch?url=https%3A%2F%2Fgithub.com%2Fmapbox%2Fpixelmatch
[0m✗ [0mWebFetch https://playwrightsolutions.com/what-the-hex-or-how-i-check-colors-with-playwright failed
[91m[1mError: [0mTransport error (GET https://playwrightsolutions.com/what-the-hex-or-how-i-check-colors-with-playwright)
[0m% [0mWebFetch http://127.0.0.1:8790/fetch?url=https%3A%2F%2Fplaywrightsolutions.com%2Fwhat-the-hex-or-how-i-check-colors-with-playwright
[0m% [0mWebFetch http://127.0.0.1:8790/search?q=Playwright+font+detection+getComputedStyle+spacing+rhythm+audit+script+free
[0m✗ [0mWebFetch https://pashaschool.github.io/design-auditor failed
[91m[1mError: [0mTransport error (GET https://pashaschool.github.io/design-auditor)
[0m% [0mWebFetch http://127.0.0.1:8790/fetch?url=https%3A%2F%2Fpashaschool.github.io%2Fdesign-auditor
[0m% [0mWebFetch http://127.0.0.1:8790/search?q=Yellow+Lab+Tools+CSS+audit+free+tool+colors+duplicated+selectors
[0m✗ [0mWebFetch https://github.com/YellowLabTools/YellowLabTools failed
[91m[1mError: [0mTransport error (GET https://github.com/YellowLabTools/YellowLabTools)
[0m% [0mWebFetch http://127.0.0.1:8790/fetch?url=https%3A%2F%2Fgithub.com%2FYellowLabTools%2FYellowLabTools
[0m✗ [0mWebFetch https://github.com/lokesh/color-thief failed
[91m[1mError: [0mTransport error (GET https://github.com/lokesh/color-thief)
[0m% [0mWebFetch http://127.0.0.1:8790/fetch?url=https%3A%2F%2Fgithub.com%2Flokesh%2Fcolor-thief
Now I have all the sources needed. Let me compile the answer.

---

**6 free tools/articles for auditing a single web page's design coherence**

| # | Tool / Article | What it does | Licence | URL |
|---|----------------|--------------|---------|-----|
| 1 | **design-auditor** | Zero-config CLI (`npx design-auditor <url>`). Uses Playwright + `getComputedStyle` on every element. 9 modules, 30+ checks: typography (font-family count, modular scale, line-height), colours (delta-E clustering, WCAG AA/AAA, CSS-variable coverage), spacing (4 px / 8 px grid, vertical rhythm), components (touch targets, hover/focus states, border-radius/shadow system), headings, images, links, breakpoints. Outputs terminal score + JSON for CI. | MIT | https://pashaschool.github.io/design-auditor |
| 2 | **CSS Stats** (web & API) | Audits all CSS requested by a page. Dashboard of rules, selectors, declarations; breaks styles into groups: layout, spacing, typography (font stacks, unique `font-size` count), colours (unique `color`/`background-color` list, declaration-order view). Good for spotting colour/size bloat. | Free (web UI) | https://www.smashingmagazine.com/2021/03/css-auditing-tools (see “CSS Stats” section) |
| 3 | **Yellow Lab Tools** | Free, open-source (GPL-2.0). Loads page in headless browser; scores CSS complexity, duplicated selectors/properties, old vendor prefixes, colour usage. Also checks HTML/JS/fonts/images. Available as online tool, CLI, Docker, Node package, public API. | GPL-2.0 | https://github.com/YellowLabTools/YellowLabTools |
| 4 | **wallace-cli** | CLI (`npx wallace <file.css>` or pipe CSS). Pretty terminal tables + JSON: unique colours, font-sizes, shadows, spacing values, custom properties, specificity, complexity score. Tracks history in CI via Project Wallace. | MIT | https://github.com/bartveneman/wallace-cli |
| 5 | **pixelmatch** | Tiny (≈150 LOC), dependency-free pixel-diff library. Perceptual colour difference in OKLab, anti-aliasing detection. Used internally by Playwright’s `toHaveScreenshot()`. CLI + Node/browser API. Ideal for visual-regression “seam” detection between section backgrounds. | ISC | https://github.com/mapbox/pixelmatch |
| 6 | **color-thief** | Extracts dominant colour / palette / semantic swatches (Vibrant, Muted, etc.) from `<img>`/`<canvas>`/`<video>`/`ImageBitmap`. Returns rich Color objects (hex, rgb, oklch, WCAG contrast ratios). Works in browser & Node; CLI (`npx colorthief-cli`). Use on section screenshots to compare extracted palette against your design tokens. | MIT | https://github.com/lokesh/color-thief |
| 7 | **“What the Hex, or How I Check Colors With Playwright”** (article) | Walk-through: `locator.toHaveCSS('background-color', 'rgb(...)')` requires RGB; shows a `convertHexToRGB` helper and a reusable `checkColor(element, property, rgb)` wrapper. Demonstrates exact computed-colour assertions in Playwright tests. | Free article | https://playwrightsolutions.com/what-the-hex-or-how-i-check-colors-with-playwright |

---

**Short Playwright script outline** (single file, runs with `npx playwright test`)

```ts
// design-audit.spec.ts
import { test, expect } from '@playwright/test';
import pixelmatch from 'pixelmatch';
import { PNG } from 'pngjs';
import fs from 'fs';

// ── CONFIG ──────────────────────────────────────────────
const URL = 'http://localhost:3000';           // your page
const PALETTE = ['#6B8E23','#E67E22','#9B59B6','#F1C40F','#87CEEB','#F5F0E1']; // design tokens
const TOLERANCE = 0.05;                        // delta-E-ish threshold
// ────────────────────────────────────────────────────────

test('full design coherence audit', async ({ page }) => {
  await page.goto(URL, { waitUntil: 'networkidle' });

  // 1️⃣  Repeated phrases / facts in rendered text
  const bodyText = await page.locator('body').innerText();
  const sentences = bodyText.split(/[.!?]\s+/).map(s => s.trim().toLowerCase());
  const freq = new Map<string, number>();
  sentences.forEach(s => freq.set(s, (freq.get(s) ?? 0) + 1));
  const duplicates = [...freq.entries()].filter(([,c]) => c > 1);
  console.log('🔁 Repeated sentences:', duplicates);

  // 2️⃣  Colours & fonts per element role (via getComputedStyle)
  const elements = await page.locator('body *').all();
  const report: Record<string, {colors: Set<string>; fonts: Set<string>; sizes: Set<string>; spacing: Set<string>}> = {};

  for (const el of elements) {
    const role = (await el.getAttribute('data-role')) ?? (await el.evaluate(e => e.tagName.toLowerCase()));
    const style = await el.evaluate(e => getComputedStyle(e));
    const key = role;
    if (!report[key]) report[key] = { colors: new Set(), fonts: new Set(), sizes: new Set(), spacing: new Set() };
    report[key].colors.add(style.color);
    report[key].colors.add(style.backgroundColor);
    report[key].fonts.add(style.fontFamily);
    report[key].sizes.add(style.fontSize);
    report[key].spacing.add(style.paddingTop);
    report[key].spacing.add(style.marginTop);
  }
  console.table(Object.fromEntries(
    Object.entries(report).map(([k,v]) => [k, {
      colors: [...v.colors],
      fonts: [...v.fonts],
      sizes: [...v.sizes],
      spacing: [...v.spacing]
    }]))
  );

  // 3️⃣  Compare extracted colours against PALETTE (delta-E placeholder)
  const allColors = new Set<string>();
  Object.values(report).forEach(r => r.colors.forEach(c => allColors.add(c)));
  const offPalette = [...allColors].filter(c => {
    // very naive: check if rgb() string roughly matches one token
    return !PALETTE.some(token => c.includes(token.replace('#','')));
  });
  console.log('⚠️ Colours not in palette:', offPalette);

  // 4️⃣  Background seams between sections (visual diff)
  const sections = await page.locator('section, [data-section]').all();
  const shots: Buffer[] = [];
  for (const sec of sections) {
    shots.push(await sec.screenshot());
  }
  for (let i = 1; i < shots.length; i++) {
    const img1 = PNG.sync.read(shots[i-1]);
    const img2 = PNG.sync.read(shots[i]);
    const diff = new PNG({ width: img1.width, height: img1.height });
    const nDiff = pixelmatch(img1.data, img2.data, diff.data, img1.width, img1.height, { threshold: 0.1 });
    if (nDiff > img1.width * img1.height * 0.02) { // >2% different
      console.log(`🔎 Seam detected between section ${i-1} and ${i}: ${nDiff} px differ`);
      fs.writeFileSync(`seam-${i-1}-${i}.png`, PNG.sync.write(diff));
    }
  }

  // 5️⃣  Spacing rhythm (8 px grid check)
  const spacings = new Set<string>();
  Object.values(report).forEach(r => r.spacing.forEach(s => spacings.add(s)));
  const offGrid = [...spacings].filter(v => {
    const px = parseFloat(v);
    return !isNaN(px) && px % 8 !== 0;
  });
  console.log('📏 Spacing values off 8px grid:', offGrid);

  // 6️⃣  Assert colour expectations (example)
  const primaryBtn = page.locator('[data-role="primary-button"]');
  await expect(primaryBtn).toHaveCSS('background-color', 'rgb(107, 142, 35)'); // #6B8E23
});
```

**Run:**  
```bash
npm i -D @playwright/test pixelmatch pngjs
npx playwright install chromium
npx playwright test design-audit.spec.ts
```

The script emits console tables/logs for every check and writes seam-diff PNGs when background steps are detected. Extend with JSON report output for CI.
EXIT 0
