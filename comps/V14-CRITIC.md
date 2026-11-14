# v14 critic: what still hurts the invitation, ranked

Owner: Tomas. Date: 2026-11-11. Critic: Opus 5.5 (fresh agent, not the designer). Page: `comps/prototype.v14.single.html` (source `comps/prototype.v14.src.html`). Read-only review: no other file was changed.

## How I looked

- Rendered in Playwright Chromium, iPhone 15 emulation, at 393 x 852, 360 x 740 and 430 x 932 (DPR 3), plus the designer's captures in `comps/art/v14/shots/` (those are 393 x 659 and 360 x 740).
- My frames are in the session scratchpad, `/tmp/claude-1000/-home-tomin-agent-config-projects-wedding-invite/503ea22b-06ae-4431-8fab-b986ea8fc1f2/scratchpad/critic/` (written below as `critic/`):
  - `critic/f/b-*.png`: `?motion=full`, frames sought on the animation clock at 1.75 to 4.0 s every 0.25 s, then 4.5, 5, 6, 8, 10 and 15 s;
  - `critic/f/a-*.png`: the same sweep without a flag, which on this 4-core machine is the lite tier (see problem 3);
  - `critic/rt/r-*.png` and `critic/rt/q-*.png`: real-time screenshots from the tap (default and full tier), with the time in the file name;
  - `critic/r/`: rest frames at three sizes and in en and es, reduced motion, `?motion=lite`, the scroll steps, idle frames 2 s apart (`critic/idle-diff.png`), replay;
  - contact sheets `critic/a1.png`, `a2.png`, `q1.png`, `wipes.png`, `r1.png` to `r3.png`, crops `critic/a025crop.png`, `full-gap.png`, `full-gate.png`, `full-dogs.png`, `milh.png`, and the `dolce-vita` comparison `critic/dv.png`, `critic/dv-dogs.png`;
  - scripts `critic/seq.js`, `rt.js`, `rest.js`, `perf.js`, `perf2.js`, `net.js`.
- Performance: CPU 4x, 393 x 852, 3 runs per tier, windows fold 0 to 2.2 s, reveal 2.2 to 7 s, idle 12 to 18 s; long-frame timestamps; first paint under network throttling over a local HTTP server.

The main session's known issues (the empty band between land and gate, the date and `Milharado` twice, Skip over an orange until 7 s, dogs denser than `dolce-vita`) are taken as given; below I add only what goes beyond them, or give them values.

## Ranked problems

### 1. The date and place are printed on the outside of the closed letter as soon as the seal is tapped

- **What:** from the tap until the bottom flap has dropped (0.0 to about 1.6 s), `10 de julho de 2027 / Quinta do Grilo / MILHARADO` sits dark and crisp on the outer face of the closed bottom flap, over the blind-embossed olive, under the cracking seal.
- **Where:** `.print .when` inside `.mid`; real-time frame `critic/rt/r-000-0.17.png` (0.17 s after the tap), crop `critic/a025crop.png`, sweep `critic/a1.png` (0.25 to 1.5 s).
- **Why it hurts:** it is the very first frame of the opening. The guest reads the date stamped on the back of a sealed letter before anything opens; it looks like a rendering fault and spoils the reveal of the hero block.
- **Cause:** `.when{position:absolute;z-index:1}` has no stacking context of its own inside the clone, so it joins the `.move` stacking context and paints above `.folds` (z-index auto). `.is-open .print{visibility:visible}` turns it on at the tap.
- **Fix:** `.mid{isolation:isolate}` (or `.print{z-index:0}`). Then `.print` can be visible from load (the two closed flaps cover the whole middle panel), which also takes its raster out of the tap frame (problem 4). Check frames at 0.2, 0.8 and 1.2 s.

### 2. First paint waits for the whole 4.4 MB file

- **What:** 99.6 % of the file (4,570 KB of 4,591 KB) is in `<head>`: 46 base64 `data:` images in the `:root` custom properties of the one `<style>` block. No pixel paints until all of it has arrived and been parsed. The `LAZY` slots save decode time only; their bytes are downloaded first, like everything else.
- **Measured** (`critic/net.js`, uncompressed, first paint): **5.1 s** of blank screen at 9 `Mbps` and 60 ms; **23.5 s** at 1.6 `Mbps` and 150 ms. Gzip shrinks the file only to 3.4 MB (base64 of WebP barely compresses), so a compressing host still gives about 3.8 s and 17.5 s. Project rule: first load under 1500 KB.
- **Why it hurts:** a guest taps the WhatsApp link and sees an empty grey-beige screen for 4 to 20 s. Many will close it before the letter appears.
- **Dead weight sent to every guest** (base64 KB): the v9 and v10 front slots that lane A overrides (seal 69, seal halves 39 + 39, closed top 26, closed bottom 38, twine 70: **282**); `--img-grass-a` and `--img-grass-b` inlined twice because `:root.warm.lite` repeats the same files (**206**); the lite-only cut-outs of sky, mist and gate (78 + 108 + 281 = **467**). About **955 KB** that a default visitor never uses.
- **Fix, in order of effect:**
  1. Ship the closed letter only in the HTML: the seven front images (about 340 KB of WebP), paper tile, fonts link. Everything under `:root.warm` becomes separate WebP files referenced by URL. Target HTML at or under 500 KB, first paint under 1 s at 9 `Mbps`.
  2. If one file is mandatory, move the whole `:root.warm,html:not(.js){...}` block (and the lite block) into a second `<style>` placed just before `</body>`, so the letter can paint before the art arrives; measure first paint again.
  3. In `v14_build.py`, inline only the last definition of each `--img-*` name (drops the 282 KB), delete the two repeated grass lines in `:root.warm.lite` (206 KB), and drop the lite swaps for sky, mist and gate, or serve them as files (467 KB).

### 3. Every iPhone, and many mid-range Android phones, get the lite tier: they never see the drawn reveal

- **What:** the head script sets `html.lite-motion` when `navigator.hardwareConcurrency <= 4` or `navigator.deviceMemory <= 4`. WebKit reports `numberOfProcessorCores() < 8 ? 4 : 8` (`Source/WebCore/page/NavigatorBase.cpp`, read 2026-11-11), and with tracking protection on it reports 4. Every iPhone has 6 cores, so every iPhone reports 4: lite. WhatsApp's in-app view on iOS is WebKit too. Chrome on Android reports `deviceMemory` 4 for most 4 GB phones: also lite.
- **Effect:** in lite the whole painting is simply there under the dissolving sheet: no meadow painted from the ground up, no olive growing from its edge, no wipes (frames `critic/r/lite-2300.png`, `critic/f/a-0225.png`, `a-0250.png`). Tasks 8 and 10 of `V14-BRIEF.md` (drawn, not faded; vegetation bottom up, branches inward) are invisible to most guests. Note for whoever measures: this 4-core test machine also falls into lite unless the URL says `?motion=full`.
- **Fix:** drop the core count from the decision; use `navigator.deviceMemory && navigator.deviceMemory < 4` and `saveData` only, and trust the frame-time probe that already runs while the letter waits (median frame over 20 ms during 600 ms). Then fix problem 4, so the full tier is affordable. Confirm on a real iPhone and one 4 GB Android phone with a one-line probe that prints `hardwareConcurrency`, `deviceMemory` and the `html` class.

### 4. Hitches: a frozen tap frame, and a long frame at every script checkpoint

- **Measured** (`critic/perf.js`, CPU 4x, 393 x 852, `?motion=full`, 3 runs): fold window 0 to 2.2 s at **39, 14 and 15 fps** (p95 83, 517, 367 ms); reveal 2.2 to 7 s at 42, 44 and 41 fps (p95 17 to 33 ms); idle 12 to 18 s at 48 to 60 fps. Lite: fold 15, 52 and 33 fps; reveal 28, 54 and 52 fps.
- **Where the long frames are** (`critic/perf2.js`, start + duration in ms from the tap):

  | Run | Long frames |
  | --- | --- |
  | 1 | 540+100, 2373+283, 3557+133, 4073+83, 4607+167, 5707+267, 7007+133 |
  | 2 | -29+**667**, 638+83, 2388+200, 2588+100, 3638+133, 4621+150, 5721+317, 7021+100 |
  | 3 | -26+**533**, 507+133, 2274+100, 2374+100, 2474+367, 2841+117, 3557+200, 4607+100, 5707+300, 7007+167 |

- **Why it hurts:** the tap is the one moment that must feel instant. A 0.5 to 0.7 s freeze (about 0.15 to 0.2 s on a real mid-range phone) swallows the press scale and the crack. Then a visible hitch lands at 2.4, 3.6, 4.6, 5.7 and 7.0 s, the exact times of `wake()`, `watch()` and the `pass()` checkpoints: each `pass()` calls `document.getAnimations()` and `commitStyles()` (a forced style flush) on the main thread mid-reveal. The "half alive, calm" feeling is broken once a second.
- **Fix:**
  1. Tap frame: make `.print` visible from load (after problem 1's fix); in `open()` add only `is-open` and `crack` on the tap and add `go` two animation frames later (`requestAnimationFrame` twice), so the creation of about 120 CSS animations leaves the tap frame.
  2. Delete the checkpoints at 3600, 4600 and 5700 ms. Give each loop a positive delay equal to its own landing time (for example `.olive > .in` sw04 at 5.65 s, `.grass-l > .in` sw10 at 4.45 s). A sine loop that starts at its `from` key frame starts at zero speed, so it needs no mid-cycle trick and no script. Run a single `commitStyles` pass in `requestIdleCallback` (`setTimeout` 0 on Safari) after 8 s.
  3. `.land` is on screen 1 at 852 pixels and taller (its top at 634 pixels) but is lazy: its image is applied by `watch()` at 2.35 s and decoded in the hand-over (the 2.27 to 2.6 s frames). Remove `data-lazy` and the `.near` gate from `.land`, so it decodes with the other screen-1 art while the letter waits.
  4. Re-measure the same three windows; target fold p95 at or under 33 ms, no frame over 100 ms.

### 5. The "drawn" entrances read as quick fades, not as painting

- **What:** each wiped piece pairs a 0.5 to 0.6 s linear opacity fade with a 2.0 to 2.6 s wipe on `--ease-out` (`cubic-bezier(.23,1,.32,1)`, quintic). About 80 % of the wipe travel happens in its first 25 % of time, under the fade. The olive starts at 3.05 s, is a pale, complete branch at 3.5 s and finished at 3.75 s (`critic/wipes.png`, frames `b-0325` to `b-0400`); the rest of its 2.6 s is an invisible creep. The moving edge is a straight `linear-gradient` feather: a slide-show wipe, not a wet brush front.
- **Why it hurts:** the user asked for things to be "drawn, almost as if in real time" (brief task 8). As built, the eye sees fades.
- **Fix:**
  - One painting curve for the wipe transforms: `--ease-paint: cubic-bezier(.45,.05,.55,.95)` (or `linear(0, .06 15%, .5 50%, .94 85%, 1)`), so the front travels at a readable, nearly steady speed.
  - Opacity on wiped pieces: 0.25 s linear at the start only, so the brush front, not the fade, reveals the art.
  - Durations: olive 2.4 s, citrus 2.4 s, olive twig 2.0 s, grass-l 1.8 s, grass-r 1.8 s, lavender 2.0 s.
  - Replace the gradient masks with a painted edge: two grayscale WebP masks, a horizontal and a vertical, about 512 x 128, a ragged wet-watercolour bleed over the extra fifth of the box (3 to 6 KB each, static, never animated), used as `mask-image:url(...)` with `mask-size:100% 100%`. Still transform only.

### 6. The reveal is front-loaded, ends at 7 s and leaves the sky bare first

- **What:** every entrance starts between 2.30 and 3.40 s, so the meadow, olive and orange land in one 1.1 s burst and are visually done by about 4 s. From 4 to 7 s nothing perceptible arrives except two 20-pixel swallows (4.8, 5.2 s) and the faint cloud veils; Skip waits to 7 s. Meanwhile the top 40 % of the screen is a bare sky over an empty paper band from 2.0 to 3.5 s (frames `critic/rt/q-011-2.50.png` to `q-016-3.43.png`): the user's v13 complaint, moved up the screen. `SPEC.md` (derived) and `DESIGN.md` ask for 8 to 12 s; v14 ends at 7.0 s.
- **Fix:** spread the starts over 2.3 to 6.0 s with the new curve (problem 5), ending at about 8.5 s:

  | Piece | Start (s) | Length (s) |
  | --- | --- | --- |
  | Strip s1, s2 | 2.30 | 2.0 |
  | Back grass L | 2.35 | 2.0 |
  | Grass L (wipe) | 2.45 | 1.8 |
  | Olive (wipe from the left edge) | 2.60 | 2.4 |
  | Cloud C2 (fade to .45) | 2.60 | 2.6 |
  | Lavender (wipe) | 2.90 | 2.0 |
  | Grass R (wipe) | 3.20 | 1.8 |
  | Citrus (wipe from the right edge) | 3.40 | 2.4 |
  | Bloom, bloom-l (grow) | 3.60, 4.00 | 1.6 |
  | Olive twig (wipe down) | 4.20 | 2.0 |
  | Bindweed b1 | 4.40 | 1.6 |
  | Cloud C1 (fade) | 4.60 | 2.4 |
  | Swallows t2, t1 | 5.40, 6.20 | 1.6 |
  | Skip out, loops awake | 8.40 | |
  | Falling leaf, first fall | 9.00 | 10 |

- Branches now enter through the dissolving sheet, so the sky is never alone, and something arrives every 0.2 to 0.8 s until 6.2 s.

### 7. The hand-over shows linen through the sky and the letter's frame

- **What:** from 1.7 to 2.5 s the world fades in over the fixed linen, so in the 16 pixels side margins and above the sheet the linen weave shows through the sky and the branches: a grey double exposure (`critic/rt/q-009-2.07.png`, `q-010-2.25.png`; in lite it crosses the olive, `critic/a200top.png`). The sheet's `--lie` shadow and the bottom flap's crease stay visible as thin vertical and horizontal lines until about 2.8 s (`q-011-2.50.png`).
- **Fix:** fade the linen out before the world comes up: `.js .page.opened::before{opacity:0;transition:opacity .45s linear 1.25s}` and give `.page.opened` the paper colour underneath. Fade the resting shadows with the dissolve: `.is-open .ground{opacity:0;transition:opacity .4s linear 1.8s}`. Shorten the dissolve: `.sheet.is-open{transition:opacity .5s linear 2.15s, visibility 0s linear 2.65s}`.

### 8. The lower page is separate pictures, not one world (beyond the known gap)

- **Floating grass:** `grass-l2` (top y0+85u, bottom y0+127u) and `grass-r2` (bottom y0+132u) end 24 to 29u below the land's last painted edge (y0+102.8u), so both clumps stand on bare paper with their roots faded into nothing (`critic/full-gap.png`, left and right).
- **Eucalyptus from wheat:** the `.euca` spray (left 66u, top G-44u) starts exactly under the `grass-r2` clump and reads as growing out of it.
- **Hem on the gate:** the gate image's own willow fronds are cut by the 13 % top mask into a horizontal hem at G (`critic/full-gap.png`, bottom right), right beside the separately painted, larger-leaved eucalyptus: two eucalyptus paintings at two leaf scales.
- **Two landscapes:** the land (white farmhouse, umbrella pines) and the gate's backdrop (cypresses, villa) are two horizons 100u apart.
- **Birds on blank paper:** `soar.s3`, `soar.s4` and `t5` (5 to 6u) float in the empty band with no sky and read as specks.
- **Fix with values:** `--G: y0 + 122u` (from 158u; land to gate gap from 67u to 31u, about 122 pixels at 393) and `--world-h: y0 + 336u` (from 372u). `grass-l2` top y0+64u; `grass-r2` top y0+66u (both rooted in the land's fringe). `.euca` left 70u, top G-36u, so its cut end bleeds off the right edge behind the grass. Gate mask `linear-gradient(transparent 4%, #000 24%)` so the backdrop horizon melts into the land above. Delete `soar.s3`, `soar.s4` and `bird.t5`, or move one swallow into the land's sky (y0+30u, 70u).

### 9. The same two grass clumps and one rock-rose are stamped all over the page

- **What:** `--img-grass-a` appears five times (`bgrass-l`, `grass-l`, `grass-l2`, `grass-f1`, dog tuft `t-r`), `--img-grass-b` five times (`grass-r`, `grass-r2`, `grass-p`, `grass-f2`, dog tuft `t-l`), each with the same blue chicory heads; `--img-bloom` three times (both panel corners, mirrored, and the dogs' posy). On the full page (`comps/art/v14/shots/s393-full.png`) the identical wheat silhouette closes five zones.
- **Why it hurts:** repetition is the quickest tell of a template or of AI art; a hand-painted page never repeats a clump.
- **Fix:** delete `grass-f1` and `grass-f2` (the foot ends better on paper, problem 18); replace the dog tufts with two crops of `--img-meadow-strip` (`background-size:250% auto`, positions `0 100%` and `100% 100%`, height at most 6u); give the remaining copies different crops and scales (`grass-p` at 0.8 scale, `rotate:-4deg`); replace the dogs' posy with the bouquet the brief suggested (prompt in problem 10) or a poppy crop of the meadow strip.

### 10. The dogs (beyond "denser and less loose")

- **What:**
  - A lineup, not a group: tan 96 pixels wide, collie 94, golden 99, blue-roan 100 (`critic/r/` measurements). A wire-haired terrier and a small blue-roan sit at nearly the height of a golden retriever.
  - No shared ground: the four feet lines sit at 1726, 1703, 1711 and 1724 pixels, with no contact between them.
  - The blacks of the collie and the blue-roan are the darkest values on the page (1st percentile luminance 32, 0.2nd 21, against 47 for the `azulejo` ink and about 50 for the page ink), so the eye lands on the bottom vignette harder than on the plaque.
  - The posy is the rock-rose cut-out turned -62°; its stems point up and right and read as dropped, not held.
  - `dolce-vita` (`critic/dv-dogs.png`): ink contour, flat light washes, most of the body left white; a clear size hierarchy (big dog at the apex, two small animals at the flanks); each animal holds a bouquet.
- **Fix with values:** sizes golden 27u, collie 23u, blue-roan 20u, tan 19u. Arrange a triangle: collie left 27u bottom 7u (back), golden left 42u bottom 6u (back, centre), tan left 15u bottom 0 (front, overlaps the collie by about 30 %), blue-roan left 58u bottom 0.5u (front, overlaps the golden by about 25 %). Re-bake the four cut-outs with the black point lifted to luminance 45 (about `#3B2F25`, the page ink) and saturation 0.9. Ground them with one meadow-strip crop across all paws (70u wide, at most 5u tall, ends masked), not ellipses.
- **If the couple want the looser look** (one Copilot run, reference: the user's dog photo):

  ```text
  Using the attached photo only for the four dogs' breeds, colours and markings, draw a new loose wedding-stationery illustration of the four dogs sitting together as one group: a large pale golden retriever sitting up in the centre and slightly behind, a black-and-white border collie behind on the left, a small wheaten wire-haired terrier in front on the left, a small blue-roan dog in front on the right; the golden holds a small bouquet of chamomile, lavender and two poppies in its mouth. Thin uneven dark-brown ink contour, flat light watercolour washes, most of the fur left as white paper, blacks softened to warm dark grey, a few dry-brush marks at the paws, no ground, no shadow. Warm off-white paper, plain flat off-white background, no text, no frame. Landscape 4:3, high resolution.
  ```

### 11. The oranges are the loudest thing on the first screen

- **What:** 95th-percentile saturation in the citrus corner is **0.95**, against 0.44 for the olive, 0.42 for the land and 0.78 for the cobalt panel (`critic/f/b-1500.png`). Three hot orange discs at the top right pull the eye from the names to the corner, under Skip for most of the reveal.
- **Fix:** re-bake `art/v14/citrus-branch.webp` with saturation times 0.7 on hues 15 to 45° and lightness +4 %, target 95th percentile at or under 0.70; width 57.6u to 52u. Do not use a runtime `filter`.

### 12. The closed letter: better, still four tells of cheapness

The seal now reads as real wax (`comps/art/v14/shots/front-seal-100pct-3x.png`). What still reads cheap (`front-closed-iphone15-3x.png`):

- **The emboss reads as white ink.** The olive on the lower flap has a light side only. A blind emboss needs both: a highlight offset (-1, -1) CSS pixels at +8 % lightness and a shade offset (+1, +1) pixels at -6 %. Bake both into `closed-bottom.webp`. Move it fully inside the sheet (it is cut by the right edge now) and centre it on the empty lower flap at 62 % of the sheet height, at 45 % of the sheet width.
- **The twine is pasted, not tied.** Both cords run dead straight and stop flush at the sheet edges. Let them pass 3 pixels beyond each edge and turn down, 15 % darker, as if wrapping round; add a contact shadow under the cords (`0 1px 1.5px rgb(48 34 22 / .25)`, baked). Where the cords pass under the seal, add a 1 to 2 pixels bulge of wax over them.
- **Skip outranks the call to action.** A boxed tab with its own shadow and 13 pixels tracked capitals, the same size as `TOCA PARA ABRIR`. Fix: `.skip{box-shadow:none;border-color:rgb(107 79 52 / .16);font-size:12px;letter-spacing:.18em}`, keep `background:rgb(247 241 227 / .94)` (`#4A3B2E` on the bare linen is only 6.3:1 and `#6B4F34` 4.4:1, so the paper ground stays).
- **The linen is cool grey-green** (`#CDC6B5`) under warm paper. Warm oat `#D8CCB4` reads richer and closer to the painting. The weave is a visibly regular grid at 256 pixels; scale the tile to 320 pixels.
- **The sheet edges are cut-card edges.** The top and bottom of the packet are folds: add a 1.5 pixels highlight (`rgb(255 252 242 / .5)`) just inside each fold edge and a 1 pixels shade under it.

### 13. Accessibility: the hidden page is reachable by Tab and announced before the letter

- **Tab order before the tap** (measured): Skip, then `Fechar e ver de novo` (inside the world at opacity 0, invisible), then the seal. A screen-reader user also hears the `h1` names, the date and the place before the seal, and the replay button is the second stop. After a replay the order is the same.
- **Fix:** `world.inert = true` at load; `false` at the start of `open()` and of `finish()`; `true` again in the replay handler.
- **Reduced motion clouds:** `.js .go .go-art{animation:washin ...}` overrides `fade55` and `fade60`, so C1 and C2 end at opacity 1 (measured `1, 1`): the veils are 1.7 to 1.8 times heavier than designed, and C2's ink outline sits closer to the opening line. Fix inside the reduced-motion block: `.js .go .c1{animation:fade55 .2s linear both !important}` and `.js .go .c2{animation:fade60 .2s linear both !important}`.
- **Reduced motion gets lower-resolution art:** the head script adds `lite` for `prefers-reduced-motion`, which swaps in the smaller sky, mist and gate. A guest who turns off motion should not get softer pictures on a 3x screen. Keep `lite` for `saveData` only.
- Skip first in focus order, real buttons, `lang` per language and `lang="pt-PT"` on the place names all pass.

### 14. Typography

- **`MILHAR ADO`:** in `.village` (both under the panel and in the foot) the R to A gap reads as a word space at every size (`critic/milh.png`). Fix: `.village{letter-spacing:.17em;padding-left:.17em;font-kerning:normal;font-feature-settings:"kern" 1,"cpsp" 1}`; if the gap persists, wrap the R in a span with `margin-right:-.05em` (markup only, copy unchanged).
- **Container units with no fallback:** `.names{font-size:11.2cqw}` and `.plaque-text .q/.g` (30 and 26 `cqw`). Safari before 16 (iPhone 7 and older stay on iOS 15; likely among 150 guests of mixed ages) drops the declaration, and the names render at the inherited 18 pixels inside a 306 pixels panel. Fix: put `font-size:clamp(30px, 8.7vw, 38px)` before the `cqw` line, and `font-size:clamp(28px, 7.8vw, 36px)` for the plaque.
- Contrast passes where measured: hint `#56412F` on paper 8.4:1; date and place on the paper glaze above 4.5:1 (the designer's measurement, not repeated here).
- Line breaks are clean in pt-PT, en (`MAYA / and / TOMÁS`) and es (`critic/r1.png`). `<title>` stays `Maya e Tomás` in en and es (should follow `join`).

### 15. The falling leaf still swings against its own travel

- **What:** sway 4.6 s period, turn 3.4 s period (plus or minus 30°), flip 5.3 s, all unrelated. Half the time the leaf tilts against the way it moves, which reads as spinning, not gliding: the "oof" the user named. Sway amplitude plus or minus 3u is plus or minus 12 pixels, below the research's 20 to 50 pixels.
- **Fix:** keep the constant fall. Couple turn to sway: same period, `leaf-r 2.3s var(--ease-sine) -0.575s infinite alternate`, amplitude plus or minus 22° (the tip trails the motion: check the sign by eye), so the leaf banks into each swing. Add a lift at the ends of each swing: `@keyframes leaf-y{from{translate:0 -5px}to{translate:0 5px}}` at 1.15 s alternate on a fourth wrapper. Sway plus or minus 4.5u (`--sa` 3.8 to 5.0). Keep the flip at 5.3 s.

### 16. What WhatsApp shows before the page opens

- **What:** WhatsApp builds the link preview from `<title>` and `<meta name="description">`. The description is a design note (`Invitation face, round 2 (v10): a closed folded sheet...`); there is no `og:image`, `og:title` or `og:description`. If this file is served as is, every guest's preview shows that note and no picture. `theme-color` `#E3E2D6` matches neither the linen nor the paper.
- **Fix:** `og:title`, `og:description` (copy: `TODO(user)`), `og:image` = a 1200 x 630 JPEG of the sealed letter at or under 300 KB, `theme-color` `#CDC6B5` (linen), switched to `#F6EFDF` at open. If the couple's site serves the page, the tags belong there; say so to the user.

### 17. Screen 1 composition at rest

- **The empty band:** the sky's bottom edge is a horizontal line at about 23 % of the screen; the band from there to the opening line (about 200 to 315 pixels at 852) holds only two small swallows. The page reads as stacked strips (sky, empty band, panel, words, land) where `dolce-vita` encloses everything in one frame with fruit and leaves down both sides (`critic/dv.png`).
- **C2 is a sticker:** the round cloud (left 74u, opacity .6) has an ink outline and a crisp left edge on bare paper, unlike the sky's soft clouds.
- **t1 touches the cloud:** swallow `t1` (250 to 286 pixels) sits on C2's left edge (291 pixels), against task 7's "clear of every cloud edge".
- **Symmetry:** olive top left and orange top right at the same height make the two-corners symmetry `DESIGN.md` lists under Never.
- **Fix:** C2 at opacity .45, `top: panel-top - 30u`, so its flat base tucks behind the panel's top edge. `t1` at left 48u, `top: panel-top - 27u`. Let the trailing olive twig hang to 46 % of S on the left edge (`.olive-b` top 6u, width 14u), so the left side carries down toward the panel. Keep the citrus higher and smaller (problem 11), so the two corners differ.

### 18. The page ends on a button and empty paper

- **What:** the last screen is the dogs, the repeated `MILHARADO / date` (known), the `Fechar e ver de novo` pill, then about 130 pixels of paper and two corner grass clumps (`critic/r/scroll-2.png`). A UI control is the last image.
- **Fix:** delete `grass-f1` and `grass-f2`; set `--world-h` so the page ends 48 pixels under the last element; if the replay stays, make it a text link (15 pixels, `text-decoration-thickness:1px`, `text-underline-offset:3px`, colour `--brown`), not a pill.

## Keep, do not touch

- The seal's crack and the two halves riding their folds; the new seal art.
- The `azulejo` panel with the live names already in place when the folds open (the v13 empty-sky complaint is answered).
- The gate wall, plaque and the painted frond shadows on the wall.
- Lavender behind the panel's right edge; bindweed b1 at the panel corner.
- Ambient amplitudes (plus or minus 0.4 to 1.2°) and the 0.6 pixels per second sky drift: idle moves only the edges, every word stays still (`critic/idle-diff.png`).
- Reduced motion: whole page in 0.2 s, no loops. Lite tier: a complete, calm first frame (a good fallback, once it is only for weak phones).
- pt-PT, en, es joins and dates; `lang` attributes; Skip first in focus order; replay resets cleanly (checked twice).
- The orange branch's shape and hang (cut end at the edge, fruit below the branch) as the olive's counterpart.

## Questions only the couple can answer

1. The opening line above the names (`TODO(user)`): what should it say, in the three languages?
2. The end of the page: finish on the dogs with no repeated date and place, or keep the repeat as a closing line?
3. The dogs: keep the detailed painted-portrait look, or ask Copilot for a looser ink-and-wash group like `dolce-vita` (prompt in problem 10)?
4. The WhatsApp preview: which picture (the sealed letter, or the names panel) and which one-line text?
5. The replay button: keep it on the guests' page, or remove it after testing?

## What I could not verify

- Any real phone, and WhatsApp's in-app browser on iOS or Android: all numbers are Chromium emulation on a 4-core WSL machine with CPU throttling, which over-states the cost of decode and style work and under-states GPU limits.
- The WebKit core-count claim is from the current WebKit source, not from a device; the probe in problem 3 settles it.
- Network numbers are uncompressed from a local server; the couple's real host (compression, HTTP/2, CDN) is unknown.
- Safari before 16 behaviour (problem 14) is from the specification support tables, not tested.
- The plaque's fidelity to `references/quinta-do-grilo-sign.jpg` was not re-compared this round.
- GPU memory at DPR 3 and battery drain of the continuous ambient were not measured.
