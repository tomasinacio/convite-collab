# Red team: style tile

Owner: Tomas. Date: 2026-11-10. Reviewed: `comps/style-tile.html` r3 (folded sheet). Pre-change copy: `comps/style-tile.v3.html`. Result: `comps/style-tile.v4pre.html` (red-team fixes only).

Reviewer: clean-slate Opus that saw only the brief and the deck. Score 5/10.

Keep (red team): the fold rotates up only; the single terracotta seal is the only colour on the closed face, with the label `Toca para abrir`; two type families (olive script names, EB Garamond for the rest).

Designer decisions (the user's words in `SPEC.md` outrank the critic; the bar is clean and elegant, not contrasty):

| # | Finding | Decision | Why |
| --- | --- | --- | --- |
| 1 | The whole lemon takes over the open face and runs past the edge | APPLY | Names must lead. One lemon at about half size, inside the edge; the half lemon dropped. |
| 2 | The art looks pasted on: shadows, stem and leaf off the sheet | APPLY | Watercolour is pigment in paper. Shadows removed, art multiplied into the paper tone, every element inside the sheet. |
| 3 | Two drawing styles on one sprig; four leaf tones | APPLY DIFFERENTLY | Kept the real plate leaves and removed the hollow outline leaves. The stem stays one plain ink line; taper waits for traced ink in stage 3. Dropped the pale leaf. |
| 4 | Double digital grain (page, stage, paper) | APPLY DIFFERENTLY | Grain removed from every page ground. The paper filter is unchanged because the user is judging it in `grain-compare.html`. |
| 5 | Empty gap above the closed sheet; two green "horns" under the seal | APPLY | Closed, the sheet sits at the top; on opening it moves down as the flap lifts, so the paper grows downward. One angled leaf under the seal. |
| 6 | Opening-line placeholder too small (`12px` uppercase) | APPLY | Now `16px` italic, sentence case. |
| 7a | Ink draw uses `stroke-dashoffset` | ASK USER | `DESIGN.md` allows only transform and opacity; the brief asks for drawings "drawn in real time". The user decides. |
| 7b | Skip stays visible after opening | APPLY | Bug. Skip hides once the sheet is open and returns on "Fold it again". |

The same art fixes were made in `type-concepts.html`, so the comparison stays fair. In `grain-compare.html`, only the grounds and the seal sprig changed; its two paper filters did not.

Follow-up, same day: the user asked to follow their deck closely, so `style-tile.html` became r4 "deck-faithful" (crops from the deck as stand-ins). It keeps decisions 1 to 6 and 7b: the art sits in the paper with no shadows, there is one drawing language (line and wash), no double grain, no gap above the closed sheet, a readable opening line, and Skip hides once the sheet is open.

User picks, same day (r5, `style-tile.v4.html` kept): a fuller scene like the deck; `stroke-dashoffset` allowed for the few ink lines (7a closed); the fold confirmed; type `Allura` with EB Garamond; grain still open, so soft stays the default.

## 2026-11-10: guest prototype `comps/prototype.html` r8 to r8b

Reviewer: clean-slate Opus, score 5/10 on r8. The same day the red team also reviewed `comps/azulejo-lab.html`: details tiles close to finished, plaque and names panels still prototype (frame, crest, bottom cut off, letter weight), vegetation not joined to the tiles, page too heavy for a phone. The user then said `azulejo` was not a priority, so the lab was not revised.

| # | Finding on r8 | Decision | Why |
| --- | --- | --- | --- |
| 1 | Second fold cannot be seen | APPLY DIFFERENTLY | Shorter top fold, longer perspective, panel content fades in while the bottom fold drops. No edge shadow added. |
| 2 | Land panel looks pasted and Italian | APPLY DIFFERENTLY | Hills, olive tree and plaque only, feathered edges. Hills are stand-in. |
| 3 | Closed sprig crop dirty | APPLY | Soft fade at the edges, emboss moved. |
| 4 | Weeds clip-art | APPLY | Soft brown ink, uneven grass, no curl. |
| 5 | Tile pane bare | APPLY | Warmer glaze, small cobalt corner leaves. |
| 6 | Third font | APPLY | Princess Sofia removed. |
| 7 to 9 | Leaf placement, early scroll, grey pass | APPLY | Leaf lands in the grass; land reveals on view; grey pass dropped. |
| 10 | Plaque placeholder | APPLY | Cut-tile placeholder on paper, labelled. |
| 11 | Grain, swallow, filters | APPLY, filters SKIP | Grain halved, swallow cut; filters measured 60 fps. |

Spec guardian items a to f: all applied (year `TODO(user)`, asset log rows, `lang="pt-PT"`, monogram line, notes heading, lint). Not yet re-reviewed after r8b.

## v9 opening, 2026-11-10

Red team (clean slate, brief only) on `comps/prototype.v9.html`, seal plus two folds, 390 x 844. Frames seen: closed, 60, 300, 500, 700, 900 ms and the open end state. Not seen: the drop at 960 to 1810 ms (the capture tripped the 3 s safety timer, then WSL stopped responding).

1. Lower seal half floats about `32px` below the bottom fold's free edge, with a flat top (500 to 900 ms). Lines 38, 42, 140. Make the fold edges meet at the seal with `--Hb: calc(var(--Hm) - var(--Ht))`. The `.half-lo` formula then lands it on the deckle.
2. The crack looks like a straight saw cut with a paper-white gap, and the upper half's edge stair-steps while it rotates. Lines 138 to 143, 237, 252. Bake an irregular crack with a dark wax lip and part the halves by only `1px`.
3. The seal is the only saturated mass, and at `120px` it outweighs a "lightly decorated" sheet. Lines 41, 265. Use `--S:100px`, with the photographic seal matched to `#9A4C32` and softer highlights.
4. Crease lines read as hard tan rules that box the open sheet into three bands. Line 84. Set the alpha to .15, or use a `6px` soft shade.
5. Between the folds, a cropped "M" and a blue tile corner peek under the bottom fold (700 to 900 ms). Line 33. Set `--t-drop:820ms`.

## 2026-11-11: designer decisions on the v9 findings

Designer: Opus 5.5 high. Applied to `comps/prototype.v9.html`; paper faces re-baked by `comps/art/v9_bake.py`, seal by `comps/art/v9_seal_photo.py`.

| # | Finding on v9 | Decision | Why |
| --- | --- | --- | --- |
| 1 | Lower seal half floats below the bottom fold's edge | APPLY | `--Hb: calc(var(--Hm) - var(--Ht))`: the free edges meet under the seal, so the lower half lands on the deckle. Bottom faces re-baked at 800 x 536. The open sheet now fits a 390 x 844 screen. |
| 2 | Straight saw cut, paper-white gap, stair-steps | APPLY DIFFERENTLY | Irregular crack with chips and a matte lip, part of `1px` plus a .4deg tip. The white gap was the top fold's paper over the lower half, so both halves now ride copies of their folds drawn above both papers. The lower half carries `2px` of dark wax under the upper half. Stair-steps stay in Chromium: any `perspective` on a moving fold renders it at low resolution (tested). |
| 3 | Seal outweighs a lightly decorated sheet | APPLY | `--S: 100px`. Every seal size follows `--S` and `--hh`. The user's Copilot seal is graded toward `#9A4C32` in the mid tones only, so its gloss stays. |
| 4 | Crease lines read as hard rules | APPLY | A `6px` soft valley: a faint shade on one side and a faint light on the other, no rule. |
| 5 | Cropped "M" and tile corner between the folds | APPLY DIFFERENTLY | `--t-drop: 820ms` with an 860 ms drop: fully open at 1680 ms. The panel content also waits until 1650 ms, and the names until 2450 ms, so nothing shows cropped. This follows `OPENING-ADVICE.md` and the r8b pack timing. |

Measured on iPhone 15 emulation (Chromium, CPU 4x, three runs of 0 to 2450 ms): 59.6, 59.6 and 60.0 fps, p95 frame gap 16.8 ms, frames over 33 ms 1, 1 and 0. First load 342 KB. Shots: `comps/art/v9/shots/`. Not checked on a real phone.

## 2026-11-11: round 2 on v9, designer decisions

Fresh Opus critic (`6/10`) and spec guardian on `comps/prototype.v9.html`. Designer: Opus 5.5 high. Faces re-baked by `comps/art/v9_bake.py`, seal by `comps/art/v9_seal_photo.py`.

| # | Finding | Decision | Why |
| --- | --- | --- | --- |
| 1 | Closed sheet is square, not tall | APPLY | `--Hm: calc(var(--W) * 1.4)` from the width; the top fold is `.42 W` (120 to `168px`). Faces re-baked at `1200px` wide. A short phone scrolls; on 393 x 659 the bottom fold drops partly below the screen. |
| 2 | Blank paper, then an empty tile frame | APPLY DIFFERENTLY | Nothing shows before 1650 ms, as `OPENING-ADVICE.md` says, so the bottom fold is the only motion. The pane washes in from 1650 ms and is complete exactly when the pen starts at 2450 ms, so it never waits empty. |
| 3 | Folds look like flat board | APPLY DIFFERENTLY | Perspective `1600px`, between the advice's 3200 and the suggested 1400, on a folds box that clips the sheet's width, so no fold pokes past the sides. A soft sheen crosses each face as it turns. |
| 4 | Break looks cut, twine only fades | APPLY | The crack falls about 10 degrees, passes below the centre and has two broken flakes. Halves are now `--hh: .63`, 600 x 378, procedural fallback too. The cut twine ends slip out `4px` and drop as they fade. |
| 5 | Blurry sky, Skip over the art, coarse moving folds | APPLY DIFFERENTLY | Faces baked at `1200px`. The cloud crop itself is only `375px` wide, so the stand-in sky stays soft. The open sheet starts `68px` down, clear of Skip. Coarse folds: `will-change` on the face or image, `perspective()` and perspective on `.sheet` did not help. Laying faces out at 3x and scaling them to a third did fix it, but cost 4 to 14 frames over 33 ms per run. So the default is 1x and `?sharp=1` turns 3x on for a real-phone test. |
| a | Content order after 2450 ms | APPLY | The r8b order: opening line and pane 1650 ms, names write letter by letter (r8b spans, `85ms` apart) 2450 to 3460 ms, date, tile mark, place, village 3500 to 4500 ms. Transitions, so Skip lands the end state. |
| b | Hidden content in the accessibility tree | APPLY | `.card` is `visibility: hidden` until 1650 ms. Checked: closed, the region is empty; open, it lists the text and the heading. |
| c | Asset log gaps | APPLY | Both seal prompts verbatim, a row for `Allura` and EB Garamond (SIL OFL, CDN dependency). Self-hosting is a later step. Deck crops stay flagged as stand-in. |
| d | Skip and reduced motion | APPLY | Skip comment added. The `@media` net now stops rotation, slides and the sheen, leaving fades. Reduced motion, emulated live: open in 643 ms, all content visible, no rotation, focus on the card. |

Measured on iPhone 15 emulation (Chromium, CPU 4x, three runs of 0 to 2450 ms): 59.6, 60.0 and 60.4 fps, p95 frame gap 16.7 to 16.8 ms, frames over 33 ms 1, 0 and 0. First load 430 KB. Shots: `comps/art/v9/shots/`. Not checked on a real phone.

## 2026-11-11: round 3 on v10, designer decisions (v11)

A fresh Opus critic reviewed `comps/prototype.v10.opening.single.html` live, and an adviser wrote `comps/V10-ATMOSPHERE-ADVICE.md`. Designer: Opus 5.5 high. Result: `comps/prototype.v11.src.html`, built to `comps/prototype.v11.single.html` by `comps/art/v10_build.py`; the v10 opening files are untouched. The sheet stays fully open at 2.2 s, as the user asked.

| # | Finding | Decision | Why |
| --- | --- | --- | --- |
| 1 | Blank sheet before the world, two skies that do not match | APPLY | The world comes up at 1.7 s, when the bottom flap is about 70% down, instead of 2.2 s. The sheet dissolves 2.2 to 2.9 s instead of 2.45 to 3.15 s. The flap sky now carries the world's two wash gradients and the paler second cloud run at `.2`, in the world's own geometry. The panel glazes at 2.4 s and the opening line arrives at 2.55 s; names unchanged at 2.85 s. |
| 2 | Lower seal half alone on bare paper | APPLY DIFFERENTLY | The bottom flap starts at 0.84 s, as the top one passes upright, and takes 1.36 s, so it is still open at 2.2 s. The half moves with its flap almost at once. No fade: the wax belongs to the paper. |
| 3 | Order of arrival jumps | APPLY | The critic's order: date 3.95, olive 4.3, small swallows 4.9 and 5.1, grass 5.4 and 5.8, bloom 6.3, mist and land glaze together 6.8 to 8.8 (land has its own entrance now), crossing swallow 8.2 to 10.3. Names stay 2.85 to 3.85. |
| 4 | Still after 10.25 s | APPLY | Part 2: continuous ambient, below. |
| 5 | Two landscapes with a seam, empty band, repeated footer | APPLY DIFFERENTLY | The land rises 15u and fades in over its top 30% (was 10 to 44%), so the mist hills read as its distance and the tree tops are not cut. The grass and the two small birds under it rise with it. Everything from the vine down moves up 20u and the page is 20u shorter, which keeps the user's composition around the gate. The footer lines stay: they are the user's copy and closing signature, a question for the user. |
| Skip | Gone by 3.0 s in 2 of 5 runs | APPLY | Not reproduced in 6 conditions: plain, CPU 4x, early tap, keyboard, scroll at 2.6 s, animations slowed 4x within 4 s. Cause: Skip left on a wall-clock timer while the reveal runs on the animation clock, so any capture that slows animations sees Skip leave early. Skip now leaves on the animation clock (a WAAPI hold of 10 s). With animations at `.3x`, Skip is still there at 3 s of animation time. |

Part 2, ambient (adviser ranks 1, 5, 6). The user chose continuous motion like the demos: infinite loops, no pause button. WCAG 2.2.2 would normally want one; the source says so.

- Grass, bloom: `gust-s` (push to 1deg, smaller return, rest), 6.8 s, from 13 s, lagging west to east; olive ±0.6deg, 9.7 s. Each uses the separate `rotate` property, so it stacks on the entrance.
- Clouds drift `36px` and `28px` over 60 and 48 s (were `12px` and `18px`).
- Rare swallow first at 18 s, then every 52 s.
- One glaze glint across the panel at 11.5 s, then every 63.5 s, under the names, lightening only.
- Falling olive leaf: SKIP. The leaf in the olive art overlaps a translucent neighbour leaf and joins the twig, so it does not cut cleanly.
- Out of view, each group pauses (IntersectionObserver); `hurry()` leaves the ambient alone; reduced motion has none.

Measured on v11 (Chromium, CPU 4x, three runs each of 0 to 3.5 s): p95 frame gap 16.8 ms in 8 of 9 runs (50 ms in one), 4 to 10 frames over 33 ms per run, average 39 to 53 fps. The long frames fall at the tap, about 0.5 s and 2.3 to 2.6 s, as in the user's untouched v10. The flap sky matches the world sky within `0.4px` and 1.5 to 2.5 of 255 (was 4.5 to 6.0). Date, place and village keep 5.6:1 or better over the risen land. Not checked on a real phone.

## 2026-11-11: v13, where the build went against `V12-CHOREOGRAPHY-ADVICE.md`

The rest follows the advice and the user's decisions taken for them: citrus with the meadow at 4.7 s, lower page 18u higher, the vine and eucalyptus across the gap.

| Advice | Decision | Why |
| --- | --- | --- |
| One meadow period, 9.1 s, lagged west to east | APPLY DIFFERENTLY | Each plant keeps its own period, 8.3 to 12.3 s: with one period and small lags, neighbours moved in step (measured correlation of their angles). |
| Fruit at 7.4, 7.9 and 8.3 s | APPLY DIFFERENTLY | 7.4, 9.6 and 11.2 s: at the advised periods two lemons swung together for minutes (r 0.93 over 30 s). |
| Loops start at the tap with negative delays | APPLY DIFFERENTLY | They still start mid-cycle, but are held frozen until the sheet is open (2.2 s): running under the invisible world during the folds cost long frames. |
| Sky planes drift on X and Y | APPLY DIFFERENTLY | X only, the advice's own first cut for a weak phone. |
| Strip crops at most 9u tall | APPLY DIFFERENTLY | Each piece shows the whole strip, the right one mirrored, its straight bottom faded by a static mask: a 9u crop showed stems without flowers. |
| Strip copies at the dogs' paws | REJECT | On the page they read as a pasted patch on the path; the gate's own flower bed frames the dogs. |
| C2 at 60u | APPLY DIFFERENTLY | Moved right of 74u, as the advice allows: at 60u the cloud's ink outline sat in the opening line's box. Behind the glyphs it is 6.1:1 or better. |
| Trailing olive twig in olive B's box | APPLY DIFFERENTLY | Hung at the left edge (0.5u): in the advised box olive A hid it completely. |
| Bough pivot `100% 0` | APPLY DIFFERENTLY | Pivot where the twig enters the page (`100% 64%`), as in v12. |
| Promote every moving layer up front | REJECT (tried) | `will-change` on every moving piece made the frames worse (up to 36 long frames per run). |
