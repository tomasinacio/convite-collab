# v10 atmosphere: half painting, half alive

Owner: Tomas. Date: 2026-11-11. Adviser: Opus 5.5 high. Scope: ambient motion, hanging citrus, the dogs, flowers behind the names panel, on `comps/prototype.v10.opening.src.html`. Proposal only: nothing here is approved.

Sources: the four demos, studied live on 2026-11-11 (iPhone 15 emulation, Playwright, `document.getAnimations()`, computed styles, and frame-by-frame tracking of their hero videos with `OpenCV`). Technique only: their art, text and code are not ours to copy.

## (a) What each demo does that feels alive

The pattern is the same in all four: **one AI image-to-video loop in the hero, motion only at the frame's edges, the words dead still, everything below static.** No canvas, no Lottie. The live pages run almost no CSS or WAAPI animation.

| Demo | Mechanism | Measured |
| --- | --- | --- |
| `dolce-vita` top fruit and leaves | looping MP4 behind live text (H.264, 960 x 1280, 24 fps, 7.04 s, 611 KB), `object-fit: cover` | fruit swings sideways, 7 to 13 CSS pixels peak to peak, about ±3 to ±7° (inference: pivot one fruit above). Period **2.0 s** for all (one wind); about 0.6 s still, then a 1.4 s swing; phase spread 0.25 to 0.5 s; 2 of 7 tracked fruits never move; the arch interior is still. Loop seam pops (9x a normal frame step) |
| `dolce-vita` animals | one static PNG, 945 x 712 with alpha, 870 KB, shown 240 x `181 px` (61 % of the width), centered on plain paper straight after the hero | no animation, no entrance. The charm is the idea: the pets in watercolor and light ink, the dog carrying the bouquet with two rings on its collar |
| `floral` flowers around a plaque | looping MP4 (HEVC, 1080 x 1920, 30 fps, 10.07 s, **9.7 MB**); names and date are live HTML over a blank paper plaque shaped like a stadium | stems sway and drift; tendrils grow in at the lower left from 4 to 10 s; 1 to 3 butterflies from 1.7 s; crescent heavier top-right and lower-left; seam jump. Headless Chromium has no HEVC: **blank hero** |
| `floral` edges | one border PNG (469 x 1536, 328 KB) repeated 11 times down both edges, 79 to 107 pixels wide | static; a `float` animation (0 to -10 pixels) exists but is unused |
| `nautical` | hero loop MP4 (5.04 s, 8.4 MB): boat rocks, couple dances, gulls cross | CSS `boat-bob` 3 s `ease-in-out` infinite, `translateY(0)` to `-6px` with `rotate(-1deg)` to `1deg`, origin at the center; one `sail-across` 14 s linear; shells and pearls bleed off the edges, static |
| `secret-garden` | hero MP4 that plays **once** (6.04 s, 25 MB): beaded curtains part over a garden table, then hold | before the tap, the tap pill pulses opacity .65 to 1, 2.4 s; nothing else moves |

What we take: motion lives at the edges and the words never move; one wind for a group; a still pause inside each cycle; most elements calm, a few alive. What we beat: their videos cost 0.6 to 25 MB, pop at every loop seam, fail without HEVC, and cannot be stopped. Ours is CSS on cut-outs: a few KB of code, no seam, each element controlled, reduced motion honored.

## (b) Ambient spec for v10

Rules: animate `rotate` only (the separate property, so it stacks on the existing `transform` entrances and on `translate`, which the clouds already use). Each group shares one breeze period; inside a group the phase lags 0.15 s per 10u from west to east. Amplitude grows with stem length. At most about 10 moving layers per screen, all at or under ±3.5°. A sway is about one third of the speed and half the swing of `dolce-vita`, because the user asked for "very light".

```css
/* the measured dolce-vita shape, slowed: a push, a smaller return, rest */
@keyframes gust-m{0%{rotate:0deg}30%{rotate:2.5deg}52%{rotate:-1.1deg}70%{rotate:.4deg}82%,100%{rotate:0deg}}
/* gust-s (A = 1deg) and gust-l (A = 3.5deg) are the same five stops; three keyframes, no var() in keyframes */
```

### Citrus bough, top right (screen 1)

The olive holds the top-left corner, so oranges and lemons hang from a bough entering at the right edge: two corners, not mirrored. The bough enters at 9.9 s, as Skip leaves, because Skip covers 77 to 97u by 3 to 14u until then. Move the swallows `t1` to (44u, `S` x .17) and `t2` to (55u, `S` x .23), out of the fruit.

| Layer | Pivot (stem top) | Box (w x h) | Swing | Period | Lag |
| --- | --- | --- | --- | --- | --- |
| C0 bough with leaves (painted, static) | `transform-origin: 100% 0`, spans 56 to 104u, -5 to 12u | 48 x 17u | ±0.4° | 9.6 s | 0 |
| C1 lemon, 6u stem, 2 leaves | (63u, 4u) | 9 x 19u | `gust-m` | 6.4 s | 0 |
| C2 orange, short stem, 3 leaves | (76u, 2u) | 13 x 22u | `gust-s` (heavier) | 6.4 s | 0.2 s |
| C3 lemon, long stem | (88u, 5u) | 8 x 21u | `gust-l` | 6.4 s | 0.4 s |
| C4 loose leaf pair | (70u, 6u) | 7 x 9u | ±4° sine | 3.2 s | 0.1 s |

Each fruit unit sets `transform-origin: 50% 0` (its stem top). No box crosses 0 or 100u at full swing, so nothing animates off screen. Entrance: the bough glazes in (opacity, 0.7 s), the fruit settles with one damped swing (5°, -2.5°, 1°, 0 over 2.6 s), then the gust loop starts at 12.8 s.

### Small doses elsewhere

| Item | Spec | Start |
| --- | --- | --- |
| Grass `grass-l`, `grass-r` | `gust-s`, origin already `50% 100%`, 6.8 s, lag 0.3 s | 13.0 s |
| Bloom and the olive | bloom `gust-s` 6.8 s; olive ±0.6° about `0 0`, 9.7 s | 13.0 s |
| One olive leaf falls | cut from the olive; falls down the left margin (x 2 to 10u), never over the kicker or panel; 3 swings, ±3u, ±25°, 7.5 s, fades into `grass-l` | 12 s, 58 s, 118 s |
| Glaze glint | one pale band (alpha .16) crosses the tile panel in 1.6 s, clipped to it; the names stay above 4.5:1 because the band only lightens the glaze | 11.5 s, 75 s |

Do not add: video loops, canvas or particle systems, scroll parallax, petal showers, sparkles, bobbing swallows (a swallow never hovers), anything that moves the names, date or gate wall, scale pulses, loops faster than 3 s (except the leaf pair), or all elements in step.

### Cost, rules, timeline

- Weight: citrus about 110 KB, leaf 3 KB, glint 0 KB. The eager art is already about 1.45 MB against the 1500 KB rule in `CLAUDE.md`. Re-encoding `grass-a` and `grass-b` at 2x (now 3x, 525 KB) saves about 230 KB (inference). Not measured.
- Frames: compositor only, no paint per frame. About 8 MB of GPU layers at DPR 3 (inference). Check on a real phone.
- `hurry()` fast-forwards every animation not named `drift`, `cross-rare` or `sweep`. Add `gust`, `sway`, `leaf`, `glint`, `breath` to that pattern, or scrolling away ends the ambient in 300 ms.
- Off screen: an `IntersectionObserver` sets `animation-play-state: paused` on groups out of view.
- Finite, as v10: iteration counts end each group at rest by about 2.6 min (citrus 22 x 6.4 s). Reduced motion: no ambient, entrances fade only. `SPEC.md` says the reveal plays once; this ambient is new and runs after it.
- WCAG 2.2.2: motion that starts by itself and lasts over 5 s needs pause, stop or hide. Ending after 2.6 min does not meet it. See decision 1.

## (c) The dogs

`dolce-vita` paints the pets as one static group and gives them a job (ring bearer). We do the same with the user's four dogs, plus breath. Photo notes: the shot looks down from above with a wide lens; the golden retriever sits up with the right paw high; its body hides the border collie's chest; the small tan dog's face is motion-blurred, so the painter must invent it; person, shoes and furniture go.

Separate the collie and the golden: paint each dog alone, then overlap them by about 15 % in the layout (collie behind, retriever's raised paw in front). That gives per-dog motion and lets us move them. Paint the group as well, as the fallback composition. Attach the photo, cropped to that dog for the single-dog prompts.

Group prompt:

```text
Using the attached photo only as reference for the four dogs' breeds, colours, markings and poses, paint a new loose botanical watercolour illustration of the four dogs sitting together at eye level, three-quarter view. Remove the room, floor, person, shoes and furniture. Left to right: a small scruffy wheaten-tan wire-haired dog with floppy ears, dark eyes and a thin dark collar, calm and friendly; a black-and-white border collie with black ears, a white blaze, white chest, amber eyes, mouth open in a smile; a pale cream golden retriever sitting up on its haunches, right front paw raised high as if waving, mouth open, pink tongue, slightly in front of the collie's shoulder; a small blue-roan dog, black head with a grey muzzle, black-and-white speckled body, small collar tag, head turned to the left. Loose watercolour on warm cotton paper, thin uneven dark-brown ink lines, soft muted Mediterranean palette of olive, sage, cream and faded ochre, visible paper grain, soft wash edges, white of the paper for highlights, light from the upper left. Plain flat light grey background, no ground, no shadow, no text, no signature, no frame. Landscape 4:3, high resolution.
```

Single-dog prompt, run once per dog with its line from the group prompt pasted at `[DOG]`:

```text
Using the attached photo only as reference, paint [DOG] alone, whole body including tail and all four paws, sitting at eye level, three-quarter view; paint the parts hidden in the photo as they naturally are. Same style: loose watercolour on warm cotton paper, thin uneven dark-brown ink lines, soft muted Mediterranean palette, visible paper grain, soft wash edges. Plain flat light grey background, no ground, no shadow, no text, no frame. Portrait 3:4, high resolution.
```

Then: `scripts/image_quality.py`, `scripts/extract_asset.py IN OUT.webp --matting` (grey, not paper, so the cream fur does not vanish), a row in `assets/LOG.md`. The style lock says "no faces"; the dogs are a logged exception.

Placement: at the gate, sitting on the path in front of the flower bed, below the plaque. Group 64u wide, left 26u, feet at `y0 + 290u`; extend `--world-h` by 34u and move `.foot` to `y0 + 332u`. Lazy, like the gate. Weight 90 to 160 KB.

Motion possible with cut-outs: breath (`scale` 1 to 1.015 about `50% 100%`; 3.4 s golden, 2.9 s collie, 2.3 s small dogs; 30 cycles); one entrance (fade, rise `6 px`, 120 ms stagger) when the dogs come into view; one wave of the retriever's paw (±6°, 2 cycles, 1.6 s) if the paw is cut as its own layer about the shoulder; a short tail wag (±8°, 4 x 0.35 s) for the small blue-roan dog if its tail is painted clear of the body. A blink needs hand-painted closed-eye patches: not worth it. No head bobbing.

Fallback if `Copilot` is poor: retry with one dog per cropped photo; then an ink-line version with flat washes (easier for AI, matches the ink language); best of all, a hand-painted watercolor pet portrait from an illustrator (first in the `designer-playbook` sourcing order). `scripts/free_image.py` takes no image input, so it cannot use the photo.

## (d) Flowers behind the names panel

`floral` paints a wildflower crescent around a blank plaque, heavier top-right and lower-left, and lets it sway and keep growing. We build it from cut-outs: one sprig per image, each root hidden behind the panel edge. They sit **before** `.names-block` in the DOM, so the opaque tile covers their roots and never touches a letter. The kicker box (about 17 to 83u, `panel-top` minus `34 px`) and the date's glaze stay clear.

| Sprig | Root behind panel | Reach | Grows at | Sway |
| --- | --- | --- | --- | --- |
| W1 Portuguese lavender (`rosmaninho`), tall | (84u, `panel-top` + 6u) | up and right to 100u, 14u above | 5.55 s | `gust-s`, 7.6 s |
| W2 wild chicory, slender | (86u, `panel-top` + 30u) | right to 98u | 5.75 s | `gust-m`, 7.6 s, lag 0.2 s |
| W3 corn poppies, 2 blooms, 1 bud | (14u, `panel-top` + 18u) | left to -2u, 4u above | 4.95 s | `gust-m`, 7.6 s |
| W4 chamomile cluster, low | (16u, `y0` - 6u) | down-left to 0u | 5.15 s | `gust-s`, 7.6 s |
| W5 bindweed tendril | (80u, `y0` - 4u) | curls right | 18 s, unfurls once (scale .85 to 1, -6° to 0, 4 s) | none after |

Existing `grass-l` 5.25 s, `grass-r` 5.85 s and the rock-rose `bloom` 6.45 s complete the crescent. Growth key frames: from opacity 0, `8 px` toward the panel, `scale(.9)` about the root, to rest, 1.2 s `--ease-out`, no overshoot. Cost: 5 sprigs, 120 to 180 KB.

Prompt, once per sprig with `[SUBJECT]` filled:

```text
Loose botanical watercolour of [SUBJECT], one single sprig, isolated and centred, the stem cut cleanly at the bottom edge. Warm cotton paper, thin uneven dark-brown ink lines, soft muted Mediterranean palette of olive, sage and the flower's own colours, visible paper grain, soft wash edges, white of the paper for highlights, light from the upper left. Plain flat off-white background, no shadow, no text, no frame. Portrait 2:3, high resolution.
```

Subjects: "Portuguese lavender, `Lavandula stoechas`, three purple flower heads with violet bracts on tall stems"; "wild chicory, a slender stem with four pale blue flowers and buds"; "two red corn poppies and one drooping bud on curved hairy stems"; "a low cluster of wild chamomile daisies with feathery leaves"; "a curling field bindweed tendril with two pale pink trumpet flowers".

## (e) Ranked suggestions

| Rank | Suggestion | Cost | Risk |
| --- | --- | --- | --- |
| 1 | Sway on the grass, bloom and olive | 0 KB | low |
| 2 | Citrus bough, three fruits swaying | ~110 KB | low to medium: Skip timing, swallows move |
| 3 | Flowers behind the panel, grow then sway | 120 to 180 KB | medium: crowding the names |
| 4 | Dogs at the gate, breathing, one paw wave | 90 to 160 KB, lazy | medium to high: likeness |
| 5 | One falling olive leaf, 3 times | 3 KB | low (already the user's pick) |
| 6 | Glaze glint on the panel | 0 KB | low |
| 7 | Late tendril unfurl at 18 s | ~25 KB | low to medium |
| 8 | One white butterfly visits a sprig once | ~6 KB | medium: fast flaps look cheap |
| 9 | Pollen motes in the light | ~1 KB | high: reads as dirt on the glass. Skip |

## (f) Decisions for the user

1. **Stopping the motion.** (a) A small round pause button, bottom right, shown only while the ambient runs (like the demos' sound button; meets WCAG 2.2.2). (b) Keep v10's finite 2.6 min with no control.
2. **Where the citrus hangs.** (a) Its own bough, top right, arriving as Skip leaves. (b) Tucked behind the olive, top left, so one corner holds everything. (c) Both corners.
3. **Where the dogs sit.** (a) At the gate, below the plaque, "waiting for you". (b) In the meadow under the land on screen 2. (c) Beside the closing words at the foot.
4. **How the dogs are painted.** (a) Four separate dogs arranged by us (each can breathe and move). (b) One painted group, like `dolce-vita`.

Not verified: feel on a real phone, final byte sizes, GPU memory, and whether `Copilot` keeps the dogs recognizable.
