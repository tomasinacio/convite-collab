# Motion notes: style tile and guest prototype

Owner: Tomas. Date: 2026-11-10. Tile: `comps/style-tile.html` (r5 with the paper switch). Pre-change copy: `comps/style-tile.v5b.html`.

## How it was measured

Headless Chromium, iPhone 15 emulation, CPU throttled 4x. Each scenario was recorded twice:

- A `requestAnimationFrame` gap recorder: frames per second, the 95th-percentile frame gap, and the number of frames over 33 ms.
- A Chrome trace: main-thread style, paint and decode time.

Scenarios: the fold (1.7 s after the tap), the draw-in (the next 4.3 s), cloud drift and bird crossing (6 s), and scroll parallax (30 wheel steps over 3 s).

Limits: headless draws its layers on the CPU, so these numbers say nothing about GPU raster on a real phone. That needs stage 6 (phones) and stage 8 (WhatsApp on real devices).

## Before and after (3 runs each)

| Scenario | Before (v5b) | After |
| --- | --- | --- |
| Fold | 60 fps, p95 16.7 ms, 0 long frames | 60 fps, p95 16.7 ms, 0 long frames |
| Draw-in | 60 fps, p95 16.7 ms | 60 fps, p95 16.7 ms |
| Drift and bird | 60 fps, no main-thread work | same |
| Scroll parallax | 51 to 58 fps, p95 33 ms, 2 to 10 long frames | 58 to 60 fps, p95 16.7 ms, 0 to 3 long frames |
| Scroll, style recalculation (trace) | 521 ms per 3 s | 99 to 135 ms per 3 s |
| Fold, image decode on the first frame (trace) | 17 ms | 1 ms |

## Causes found, and fixes

| Cause | Avoidable? | Fix |
| --- | --- | --- |
| Parallax wrote an inherited CSS variable on the sheet every frame. Each scroll frame restyled every descendant: the review skill's style "storm". | Yes | Each plane's own transform is set directly and only when it changes by half a pixel or more. |
| The scene started at 1000 ms while the fold was still moving (it lands at 1450 ms). Two motions competed. | Yes | The scene starts at 1400 ms, when the fold has landed (choreography). |
| Hidden scene images were decoded on the first reveal frame. | Yes | They are decoded after page load, before the tap. |
| Draw-in paint is about 1 ms per frame at 4x throttle, all from the `stroke-dashoffset` ink. | Within budget | Kept, as the user allowed. |
| My own attempt to promote the 12 filtered paper layers with `will-change` dropped the fold to 45 fps. | Yes | Reverted, with a note in the CSS. Measured, not guessed. |

## r6 check (names written by hand, soft paper only)

Choreography, checked with the `animate`, `choreograph` and `review-animations` skills: one focus at a time, top to bottom. Times run from when the fold lands, 1.4 s after the tap:

1. Sky: 0 to 1.2 s.
2. Names write letter by letter: 0.7 to 1.8 s.
3. Sprig draws: 1.8 to 3 s.
4. Sprig leaves take colour: 2.95 to 3.95 s.
5. The land below: 3 to 6.5 s.
6. One leaf drifts: 6.4 to 9.8 s.
7. One bird crosses: from 10 s.

The main sequence is about 11 s from the tap; the brief asks for 8 to 12 s.

Measured at 4x throttle, 3 runs:

| Scenario | fps | p95 frame gap | Frames over 33 ms |
| --- | --- | --- | --- |
| Fold | 59 to 61 | 16.8 ms | 0 to 1 |
| Draw-in | 58 to 61 | 16.8 ms | 0 to 2 |
| Drift, leaf and bird | 60 | 16.8 ms | 0 to 1 |
| Scroll | 57 to 60 | 16.8 ms | 0 to 3 |

## What is prototype-only (pipeline stages 3 to 6 not done)

- **The art:** 1280x720 JPEG crops from the deck, enlarged up to 3 times on a phone, so they look soft.
- **The line pass:** a machine-thresholded copy of each crop, so the line-to-colour cross-fade can ghost and look blotchy. Real layered line and wash art comes in stage 3.
- **No authored storyboard:** timings are tile guesses, not stage 4 beats.
- **No motion tool bake-off:** stage 5 has not chosen between GSAP, Rive and Lottie.
- **No real-phone tests:** stages 6 and 8 have not run.
- **The tile page itself:** it plays a second, static open sheet on load and draws the SVG paper grain on the CPU in headless. The build will use one sheet and a pre-rendered paper texture.

## Two-fold concepts (fold-concepts.html)

At 4x throttle, 3 runs, each of the three demos ran at 60 fps with p95 16.7 to 16.8 ms and 0 frames over 33 ms. The motion is transform and opacity only, on three panels with backface-visibility.

## Lower part consolidated (r7c; before copy `style-tile.v7b.html`)

The user said: "the bottom part has animations all over the place". These are the causes the measurement showed.

Before (r7): what moved and when, in seconds after the fold lands:

| What | Trigger | Timing | Problem |
| --- | --- | --- | --- |
| Sky planes, each with its own delay | fold lands | 0 to 2.6 | four staggered starts |
| Three ink birds in the sky | fold lands | 0.6 to 1.4 | drawn while the names write |
| Villa, tree, three flower clusters | fold lands, fixed delays | 3 to 6.5 | ran off screen while the guest read the names |
| Line and colour passes | per plane | 2.4 s and 1.8 s, two curves | durations and curves mixed |
| Cloud drift | fold lands | 3 to 29 | ran under everything else |
| Falling leaf | fold lands | 6.4 to 9.8 | moved beside the date while it was read |
| Bird crossing | fold lands | 10 to 19 | on top of the drift |
| Second, reference sheet | page load | about 10 s | whole sequence played off screen on load |
| Scroll depth | scroll | all 9 planes, 6 speeds | everything slid while scrolling |

After (r7c): one sequence, one curve (ease-out), one duration family (line 0.6 s, colour 0.9 s, text 0.6 s):

| Step | Trigger | Timing |
| --- | --- | --- |
| Sky as one picture, ink birds with it | fold lands | 0 to 1.5 |
| Opening line, names, date and place | timed | 0.9 to 2.95 |
| Sprig draws, its leaves take colour, one leaf falls | timed | 2.8 to 5.9, then still |
| Villa, then tree, then the flower bed | each in view, one at a time, after the names | 1.5 s each |
| One bird crosses, once | 3 s after the names, sky in view, nothing else moving | 7 s |
| Reference sheet | none | shown finished |
| Scroll depth | scroll | two depths only: far clouds and the near flower bed |

Measured at 4x throttle: tap, 4 s reading, then a slow scroll through the lower part (16 s window, 4 runs before, 3 after).

| Metric | Before | After |
| --- | --- | --- |
| Animations running before the tap | 12 to 15 | 0 |
| Most animations running at once | 60 to 65 | 41 (mostly the letters of the names) |
| Animations running off screen | up to 18 | 0, except a step still finishing as it scrolls away |
| Seconds with 3 or more things moving on screen | 6.5 to 7 | 3.25 to 4.25 (all in the names section) |
| Frames over 33 ms | 30 to 39 in 3 of 4 runs | 1 to 11 |
| Average fps | 41 to 60 | 48 to 60 |

## r8b: guest prototype (`comps/prototype.html`)

What a guest sees, in one page at phone width, revised after the red team and spec guardian of r8. Same rules as r7c: one curve family, one focus at a time, transform and opacity only, plus `stroke-dashoffset` for the ink stems. The grey line pass on the deck crops and the late swallow flight are gone. Times run from the tap.

| Step | Trigger | Timing (s) |
| --- | --- | --- |
| Seal and twine fade | tap | 0 to 0.45 |
| Top fold lifts; the sheet moves down only as far as the screen needs | tap | 0.3 to 1.4 |
| Sky fades in, three ink birds draw | top fold landed | 1.3 to 2.2 |
| Bottom fold drops, in view; opening line and tile pane fade in with it | timed | 1.45 to 2.45 |
| Names write letter by letter | timed | 2.45 to 3.5 |
| Date, tile mark, place, village | timed | 3.5 to 4.5 |
| Weeds: stems draw, then heads and leaves in ink | timed | 4.6 to 6.45 |
| Weeds take colour, faint shadow on the glaze | timed | 6.5 to 7.3 |
| One leaf drifts into the grass | timed | 7.3 to 9, then still |
| Hills, then olive tree, then the plaque placeholder | each as it enters the view, one at a time, 1.1 s apart, never waiting on the names | 1 s each |

Measured with the CPU slowed 4x, cold load, iPhone 15 emulation, 3 runs: fold, names and scroll at 60 fps, p95 frame gap 16.7 to 16.8 ms, 0 to 2 frames over 33 ms. 197 elements, about 130 KB transferred, the load event at 0.26 to 0.67 s on localhost. Headless draws on the CPU, so a mid-range phone still has to be checked.
