# v12 choreography: one painting that settles, not stickers that pop

Owner: Tomas. Date: 2026-11-11. Adviser: Opus 5.5 high. Scope: the reveal after the hand-over, the ambient loops and the overlaps of the art. Proposal only: nothing here is approved. Base: `comps/prototype.v11.src.html`; v12 positions (dogs, citrus) come from the screenshots in `comps/art/v12/shots/` only. Skills applied: `choreograph`, `animate`, `emil-design-eng`, `animation-performance`, `accessible-animation`. Demo motion numbers come from `comps/V10-ATMOSPHERE-ADVICE.md` (measured there); the free research reports were used as leads only.

The user's words: "very one at a time, popping out of nowhere", "slower and more stuff at slightly different rhythms", "things that oscillate undulating slowly", "more intertwined, messier", "really smooth, not super chaotic".

## 1. Diagnosis: why v11 reads as pop-in

| Measure (v11, seconds from the tap) | Value | Effect |
| --- | --- | --- |
| Scenery on screen when the names finish (3.85 s) | wash, sky, panel, opening line only | the stage is bare paper when the message lands |
| Scenery arrivals after the names | 9, from 4.3 s to 8.8 s | the set is dressed after the actor has spoken |
| Layers in flight, 2 to 8 s | mean 2.0, maximum 4 | "one at a time" |
| Time with nothing entering, 2.5 to 9 s | 0.75 s | the queue even pauses |
| Mean entrance length | 1.1 s | short |
| Opacity curve | `--ease-out` (quintic): 90% opaque at 36% of the duration | a "1.3 s" olive is 90% there in 0.47 s; the 0.6 s texts in 0.22 s: a pop, then an unseen creep |
| Travel | 6 to `14px` for everything | no depth: far mist and near grass move alike (`choreograph` rule 3) |
| Order by depth | near grass 5.4 s, far mist and land 6.8 s | back to front is inverted |
| Ambient start | everything wakes at 10.5 to 14 s, three plants share 6.8 s | they visibly sync; the `gust-s` rest (18% of each cycle) adds a stop-start |

Three causes: the scenery waits for the names, each piece arrives alone onto empty paper, and opacity on a strong ease-out turns every entrance into a pop.

## 2. New reveal timeline

Principle: a painter lays the big washes first and adds near detail last. Layers arrive back to front in four waves; within a wave the starts are unequal; each wave starts when the previous one is 32 to 58% through (overlap 42 to 68%). Travel grows with nearness (parallax): far 0 to `5px`, middle 10 to `12px`, near 14 to `26px`. Decoration fades only.

Two animations per element: opacity on `--ease-glaze` (near-linear, 50% at 41% of the time), movement on `--ease-out` (quintic settle). The fade then lasts as long as it looks, and the move still lands softly. The sheet keeps v11 exactly: fully open at 2.2 s, world up from 1.7 s, sheet gone 2.2 to 2.9 s. Everything that starts before 2.9 s arrives *through* the dissolving sheet, which hides any start.

| Element | Start | Fade | Move | Easing | Travel | Why |
| --- | --- | --- | --- | --- | --- | --- |
| Wash, sky, `sky-b` | 1.70 | 0.8 | none | glaze | none | hand-over unchanged; the sky drift starts here from rest, so the flap match holds |
| Cloud C1, far (new) | 1.90 | 2.4 | none | glaze | fade only, already drifting | decoration, far |
| Mist and far hills | 2.00 | 2.4 | 2.8 | glaze / out | rise `5px` | far: barely moves |
| Panel | 2.15 | 1.0 | 1.4 | glaze / out | rise `10px`, `scale` .985 to 1 | carries the lead; 89% opaque at 2.85 |
| Opening line | 2.55 | 0.9 | 1.0 | glaze / out | rise `4px` | start unchanged |
| **Names** | **2.85 to 3.85** | glyph 0.16 | none | as r8b | write-on | the lead, unchanged |
| Land | 2.95 | 2.2 | 2.8 | glaze / out | rise `12px` | middle; below the date, away from the names |
| Cloud C2, low (new) | 3.05 | 2.6 | none | glaze | fade only | decoration behind the panel top |
| Olive A, then B +0.22 | 3.80 | 1.6 | 3.0 | glaze / out | `translate(-16px,-12px) rotate(-2.5deg)` about `0 0` | near; starts on the last letter, 35u from it |
| Back grass L | 3.85 | 1.6 | 2.4 | glaze / out | rise `14px`, `scaleY(.94)` about the root | behind the panel |
| Date, place, village | 3.95, 4.07, 4.15 | 0.9 | 1.0 | glaze / out | rise 5, 4, `3px` | starts unchanged |
| Back grass R | 4.12 | 1.6 | 2.4 | glaze / out | rise `12px` | behind the panel |
| `grass-l` | 4.30 | 1.6 | 2.6 | glaze / out | rise `22px`, `scaleY(.92)` | near |
| Bloom | 4.62 | 1.4 | 2.4 | glaze / out | rise `14px`, `scale(.96)` | near |
| Citrus bough and fruit | 4.70 | 1.8 | 3.4 | glaze / out | `translate(18px,-14px) rotate(1.5deg)` about `100% 0`; fruit swing 4°, -2°, 0.8°, 0 | near, top right |
| `grass-r` | 4.95 | 1.6 | 3.0 | glaze / out | rise `26px`, `scaleY(.92)` | nearest: travels furthest |
| Small bloom L | 5.08 | 1.4 | 2.2 | glaze / out | rise `10px` | near |
| Wildflower strip (new) | 5.45 | 1.6 | 2.8 | glaze / out | rise `18px` | closes the meadow |
| Swallows `t1`, `t2` | 5.60, 6.15 | 1.6 | none | glaze | fade only | decoration |
| Crossing swallow | 8.00 | path | 2.6 | `--ease-fold` | as v11 | slower glide (was 2.1 s) |

Result: mean entrance 2.2 s (v11 1.1 s); layers in flight from 2 to 8 s average 7.2 (v11 2.0); never a moment with nothing arriving; at most 6 elements in the fast first third of their move at once (at 4.2 s). During the names only far layers move fast (mist, land, the C2 fade); olive and back grass start in the last 50 ms. Screen-1 scenery settles at 8.25 s; the crossing swallow ends at **10.6 s** (v11 10.3 s). Skip holds to 10.6 s on the animation clock. Below the fold, art is present at the hand-over (no entrance on scroll, so nothing pops while scrolling); v12's dog entrance can stay if it uses the same split curves.

## 3. Ambient

Every loop is a sine: `--ease-sine: cubic-bezier(.37,0,.63,1)` (easeInOutSine, from easings.net), `infinite alternate`. The CSS duration is half the period. All loops start at the tap with negative delays, so each piece is mid-cycle and already moving when it fades in: no start jolt. The exception is the two sky planes, which start at 1.70 s from rest to keep the flap match.

| Layer | Property | Amplitude | Period (CSS duration) | Delay | Origin |
| --- | --- | --- | --- | --- | --- |
| Sky | `translate` X; wrapper `translate` Y | `-36px`; `-4px` | 118 (59); 46 (23) | 1.70; 1.70 | none |
| `sky-b` | X; wrapper Y | `+28px`; `+3px` | 94 (47); 62 (31) | 1.70; 1.70 | none |
| C1 far | X; wrapper Y | �`�20px`; �`�4px` | 74 (37); 34 (17) | -11; -5 | none |
| C2 low | X, opposite way; wrapper Y | �`�28px`; �`�5px` | 58 (29); 26 (13) | -19; -8 | none |
| Olive A | wrapper `rotate`; image `rotate` | ±0.6°; ±0.4° | 14.6 (7.3); 9.4 (4.7) | -3.1; -6.2 | `0 0`; `35% 30%` |
| Olive B | `rotate` | ±0.7° | 11.8 (5.9) | -2.3 | `0 0` |
| Citrus bough | `rotate` | ±0.5° | 16.2 (8.1) | -6.0 | `100% 0` |
| Orange, lemon A, lemon B | `rotate` (children of the bough) | ±1.4°, ±1.8°, ±1.6° | 7.4, 7.9, 8.3 | -1.0, -2.9, -4.4 | `50% 0` |
| West meadow: `grass-l`, back L, small bloom | `rotate`; `grass-l` wrapper `rotate` | ±1.0°, ±0.7°, ±0.5°; ±0.4° | 9.1 (4.55); 21.4 (10.7) | -2.30, -2.42, -2.36; -7 | `50% 100%` |
| East meadow: bloom, `grass-r`, back R | `rotate`; `grass-r` wrapper | ±0.7°, ±1.2°, ±0.7°; ±0.4° | 9.1; 21.4 | -1.30, -1.24, -1.27; -15 | `40% 80%`, `50% 100%` |
| Land meadow, `grass-p`, foot grass | `rotate` | ±1.0° | 9.1 | lag 0.15 s per 10u, west first | `50% 100%` |
| Swallows `t3`, `t4` | wrapper X; image Y and `rotate` | �`�6px`; �`�3px`, ±2° about their set angle | 26.8; 17.2 | -4.1, -9.7 | centre |
| Vine | `rotate` | ±0.8° | 15.8 (7.9) | -4.0 | `0 0` |
| Eucalyptus | wrapper; image | ±1.0°; ±0.5° | 12.2; 7.4 | -9.0; -2.2 | `100% 0`; `60% 40%` |
| Dogs breathing | `scale: 1 1.016` | about `1px` | 2.6, 2.9, 3.3, 3.7 | -0.4, -1.1, -2.0, -0.7 | `50% 100%` |
| Blue-roan tail | `rotate` | ±4° | 3.1 | -0.9 | tail base |
| Glint; rare swallow | as v11 | as v11 | 63.5; 52 | as v11 | none |

Why these numbers: the demos swing at 2 to 3 s (`dolce-vita` fruit 2.0 s, `nautical` boat 3 s, measured in v10); the user wants calmer, so plants run 7 to 22 s at a third of the angle. No two periods on one screen are near a simple ratio. One wind per group (the meadow shares 9.1 s, lagged west to east), so it reads as a breeze; the 21.4 s wrapper makes the breeze rise and fall. Dogs breathe faster than 7 s because breathing is a body rhythm; at `1px` it is felt, not seen.

Technique: separate `translate`, `rotate` and `scale` properties for loops; entrances use `transform` and `opacity`, so they stack without overriding. Two periods on one piece need two elements: a wrapper `<i>` and the image, each with its own `rotate`. Keep a fixed key-frame set per amplitude (`sw04`, `sw05` up to `sw18`), not `var()` inside `@keyframes`, as v10 advised. Example:

```css
@keyframes sw10{from{rotate:-1deg}to{rotate:1deg}}
@keyframes rise22{from{transform:translateY(22px) scaleY(.92)}}
@keyframes fade{from{opacity:0}}
.js .go .grass-l{animation:fade 1.6s var(--ease-glaze) 4.3s both, rise22 2.6s var(--ease-out) 4.3s both,
  sw10 4.55s var(--ease-sine) -2.3s infinite alternate}
.js .go .grass-l-w{animation:sw04 10.7s var(--ease-sine) -7s infinite alternate}
```

Caps: at most 10 moving objects per screen. Screen 1: sky, `sky-b`, C1, C2, olive, citrus, west meadow, east meadow, plus the rare glint and swallow. Still on purpose: mist, land, panel, every word, `t1` and `t2`, the wildflower strip, the gate and plaque. No loop under 7 s except the dogs; peak speed under `1.5px` per second for clouds and under 0.5° per second for plants. Nothing animates `clip-path`, `filter` or masks (masks stay static). Each wrapper is watched by the `IntersectionObserver` and paused out of view; add `sw`, `bob`, `soar`, `breath`, `tail` to the `AMBIENT` pattern so `hurry()` leaves them alone. Reduced motion: no loops, all art and text fade together in 0.2 s at the hand-over, as v11.

## 4. Composition: intertwined, not blocks

Anchors: `y0` is the panel's bottom; the panel spans 11 to 89u; the names box (keep clear) is 23 to 77u by `panel-top` + 11u to `y0` - 12u. `G` is the gate-box top (v11 `y0` + 176u); the plaque lettering (keep clear) is 31 to 67u by `G` + 36u to `G` + 57u; `F` is the dogs' feet line (about `G` + 93u in the v12 screenshot). Reuse costs 0 KB.

| Piece | Box: left, top, width | Layer | What it crosses |
| --- | --- | --- | --- |
| Olive B (reuse olive, `rotate(38deg)`) | -4u, -6u, 36u | behind olive A | crosses A in the corner; tips end near (12u, 40u), above the opening line |
| C1 (new) | 26u, 2u, 48u, opacity .55 | over `sky-b`, under the boughs | shows between olive and citrus |
| C2 (new) | 60u, `panel-top` - 22u, 56u, opacity .6 | behind the panel | the panel's top right sits in a cloud bank; measure the opening line over it at 4.5:1, else move it right of 74u |
| Back grass L (reuse `grass-a`, mirrored) | -2u, `y0` - 50u, 20u | behind the panel | heads rise beside the left edge |
| Back grass R (reuse `grass-b`, mirrored) | 82u, `y0` - 56u, 20u | behind the panel | heads rise beside the right edge |
| `grass-l`, bloom, `grass-r` | unchanged | in front | `grass-l` right edge stays under 23u |
| Small bloom L (reuse bloom, mirrored) | 0u, `y0` - 8u, 16u | in front of `grass-l` | colour on the left corner |
| Wildflower strip (new), two crops | 4 to 42u and 58 to 96u, top `y0` - 7u, at most 9u tall | in front of the panel | crosses the bottom border; centre medallion stays clear; nothing reaches the date's glaze |
| Bindweed (new) | 78u, `y0` - 30u, 16u | in front | wraps the lower right border, right of 79u |
| `grass-l2`, `grass-r2` | up 6u: `y0` + 85u, `y0` + 93u | in front of the land | roots sit in the land's foreground |
| Vine | -6u, `G` - 34u, 38u | in front of the gate | grapes over the wall's top-left coping; left of 30u below `G` + 28u |
| Eucalyptus | 66u, `G` - 44u, 40u | in front of the gate | over the wall's top right, beside the painted fronds |
| `grass-p` | 9u (was 17u), `G` + 52u | in front | crosses the plaque frame's lower-left corner, not the lettering |
| Bindweed copy, mirrored | 66u, `G` + 50u, 12u | in front | the plaque frame's lower-right corner |
| Strip copies at the dogs | two 30u crops, bottom `F` + 4u | in front of the dogs | at most 7u above `F`: paws only, never chest or face |

Optional: a pre-blurred copy of the land and the mist (a quarter size, about `8px` blur) fades in first and the sharp image over it 0.4 s later: a wet wash, then detail, with opacity only.

## 5. New `Copilot` images

Ranked by impact. Essential: 1 to 3. The clouds use a mid blue-grey background, because white cloud on off-white cannot be cut out; the key then keeps their soft edges as alpha.

1. **Two clouds** (essential; C1 and C2, screen 1). Run twice: once "long and low, three times as wide as tall", once "a rounder heaped cloud with a flat base".

    ```text
    Loose botanical watercolour of one single soft summer cumulus cloud, [SHAPE], warm cream-white tops lit from the upper left, pale violet-grey shading underneath, soft wet-in-wet edges that fade out, a few thin broken dark-brown ink lines on the upper outline only. Warm cotton paper, visible paper grain, soft muted Mediterranean palette. One element, isolated and centred with wide margins. Plain flat even medium blue-grey background, no gradient, no sky, no birds, no text, no frame. Landscape 3:1, high resolution.
    ```

2. **Wildflower strip** (essential; the panel's foot and the dogs' paws).

    ```text
    Loose botanical watercolour of one low horizontal strip of Portuguese summer meadow: dry golden wild oats and short grasses, three white chamomile daisies, two small red poppies, one blue chicory flower, stems leaning slightly right in a light breeze, the bottom edge cut straight. Warm cotton paper, thin uneven dark-brown ink lines, soft muted Mediterranean palette of straw, olive, sage and faded red, visible paper grain, soft wash edges, light from the upper left. One element, isolated and centred. Plain flat off-white background, no ground, no shadow, no text, no frame. Wide landscape 4:1, high resolution.
    ```

3. **Bindweed tendril** (essential; the panel and plaque corners).

    ```text
    Loose botanical watercolour of one long curling field bindweed tendril, a thin twining stem in an S curve with six arrow-shaped leaves, two pale pink-and-white trumpet flowers and one closed bud, the stem end cut cleanly. Warm cotton paper, thin uneven dark-brown ink lines, soft muted Mediterranean palette, visible paper grain, soft wash edges, white of the paper for highlights, light from the upper left. One element, isolated and centred. Plain flat off-white background, no shadow, no text, no frame. Portrait 2:3, high resolution.
    ```

4. **Trailing olive twig** (optional; replaces the reused olive B with a longer hanging tip).

    ```text
    Loose botanical watercolour of one long thin olive twig hanging straight down, fourteen narrow silver-green leaves, three small green and black olives, the cut end at the top edge. Warm cotton paper, thin uneven dark-brown ink lines, soft muted Mediterranean palette, visible paper grain, soft wash edges, light from the upper left. One element, isolated. Plain flat off-white background, no shadow, no text, no frame. Tall portrait 1:3, high resolution.
    ```

5. **Loose olive leaves** (optional; the falling leaf skipped in v11 because it would not cut cleanly). Same style; subject: "four separate single olive leaves, each whole and slightly curled, well apart, not touching". Square 1:1.
6. **Second swallow pose** (optional; five birds share one pose now). Same style; subject: "one barn swallow in flight seen from below, wings raised in a V, forked tail open". Landscape 3:2.
7. **Portuguese lavender** (optional; behind the panel's right edge in place of the mirrored grass). Same style; subject: "three tall stems of Portuguese lavender, `rosmaninho`, with purple heads and violet bracts". Portrait 2:3.

Not worth it: tile shards (read as debris; the panel and plaque carry the `azulejo`), more birds, butterflies.

## 6. Costs and decisions

- Weight: the three essential images about 140 KB, eager (clouds 60, strip 50, bindweed 30; estimates). Reused pieces 0 KB. v11's eager screen-1 art is 1209 KB plus about 210 KB of letter, so this fits under 1500 KB only with v12's 2x grass re-cuts (`grass-a` 310 to 83 KB). Pre-blurred land and mist: about 20 KB, lazy.
- Layers: 15 moving layers on screen 1 (8 objects); about 18 MB of GPU texture at DPR 3, 10 MB of it the two sky planes (upper bound, estimate). If a weak phone stutters, drop the sky Y wrappers first, then the `sky-b` drift.
- Frames: compositor only. More layers start while the sheet dissolves, where v11 already had its long frames (2.3 to 2.6 s); measure CPU 4x as in round 3, target p95 at or under 16.8 ms.
- Feel check on a recording: 2.9 s (one dissolve, not a queue?), 3.85 s (meadow beginning, not done?), 4.2 to 5.5 s (the busiest: a wave, not a swarm?), 30 s idle (any two plants in step?).

Decisions for the user:

1. **New images.** (a) Make the three essential ones now (recommended). (b) All seven. (c) None: reuse only, with cloud veils cut from `sky-b`.
2. **Citrus timing.** (a) With the meadow at 4.7 s, Skip's pill sitting over its top right until 10.6 s (recommended). (b) After Skip leaves, as in v12.
3. **Lower page.** (a) Move the gate, dogs and foot up 18u and hang the vine and eucalyptus across the land-gate gap (recommended). (b) Keep the positions; only re-hang the vine and eucalyptus.

Not checked: no live render of this plan, the demos were not re-opened this round, the opening line's contrast over C2, v12's exact positions, byte sizes of images not yet made, any real phone.
