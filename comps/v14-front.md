# v14 front: merge note (lane A, task 11)

Owner: Tomas. Date: 2026-11-11 (round 2). Designer: Opus 5.5 high. Status: for the user's gate.

## Merge

Paste `comps/v14-front.css` as one block after `.crack .half-lo{...}` in `prototype.v14.src.html`, before THE WORLD. No markup change is needed: the block reuses the v13 ids, classes, timings and fold geometry, and adds three pseudo-elements. Optional: set `<meta name="theme-color">` to `#CDC6B5`.

| Selector | Change |
| --- | --- |
| `:root` | 6 slots point to `art/v14/front/`; new `--img-closed-emboss`, `--img-linen`, `--linen`; `--seal: calc(var(--W) * .44)` |
| `.tp:not(.ride) .face-out` | round 2: `cover`, anchored at the torn edge on the seam |
| `.bt:not(.ride) .face-out` | round 2: emboss overlay in the lower right over the paper, `cover`, anchored at the top |
| `.js .page::before` | linen surface (a fallback behind a full-bleed sheet); hidden at 2.6 s |
| `.move::before` | contact shadow; opacity to 0 in 600 ms at the tap |
| `.tp .cast` | a softer cast shadow under the torn edge |
| `.closed-deco` | aspect 1300/648, strands centred on `--sy`, edge to edge |
| `.seal-label` | tracked small capitals between two hairlines, 8.3:1 |
| `.skip` | a printed tab, still 44 pixels tall, 9.5:1 |

Round 2 (user, 2026-11-11: "the olive branch is weird and cut short and there is some loose rope"):

- The twine is two clean strands from edge to edge, knotted under the wax. There are no tails and nothing loose.
- The sprig is the whole twig. Its cut stem is hidden under the wax and its natural tip reaches out. The strands cross over its stem, and its shadow softens toward the tip.
- The flap faces are ready for a full-bleed sheet with the seam 37 % down the screen. On any phone they fill their boxes with `cover`. `closed-bottom-plain.webp` is gone: with `--img-closed-emboss: none` the flap is plain.

Files (WebP, first load): seal-whole 77 KB, seal-top 43, seal-bottom 44, closed-top 39, closed-bottom 58, closed-emboss 26, closed-deco 58, linen 45. Total 390 KB (v13 front: 233). Not loaded: `closed-deco-nosprig.webp`. Rebuild: `.venv/bin/python -I comps/art/v14_front.py`.

The crack halves still line up with the whole seal at 3x. The opening runs in `comps/v14-front-preview.html` (default full-bleed; `?fit=card` shows the v13 card).

## Questions for the user (picker, still open)

1. Blind-embossed olive twig: keep (recommended) / plain.
2. Pressed sprig: keep (recommended) / twine and seal only.
3. Linen behind the sheet: flax (recommended) / warmer oat / the old sage.

## Optional Copilot art (only if the user wants more realism; not blocking)

The seal and papers pass the gate; the twine passes size, grain and blocking, and its halo flag reads the baked shadow. A real photo would beat the procedural twine. Ask the user to run this prompt once and send the 1254-pixel output:

- Twine: `Top-down macro photograph of two strands of natural jute twine lying side by side across cream handmade cotton paper, two-ply twist clearly visible, a few stray fibres, soft window daylight from the upper left, short soft shadow to the lower right, 100 mm macro, f/8, all sharp, true colour, no knots, no loose ends, no props, no text, plain paper filling the frame.`
