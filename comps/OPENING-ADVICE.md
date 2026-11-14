# Opening advice: seal and two-fold letter (approach A)

Owner: Tomas. Date: 2026-11-10. Adviser: Opus 5.5 high. Scope: tap until the sheet is fully open.

## Why r8b feels off (inference, `comps/prototype.html`)

- 300 ms with no reaction: the seal only fades (lines 103, 109).
- Both folds share curve and duration; the bottom starts 50 ms after the top lands (lines 72, 74). A queue, not one gesture.
- The sky fades in during the drop (line 418): two leads.
- Static `drop-shadow` filters on rotating panels (lines 79 to 82).

## Beat table (ms from the click)

Curves already in the file: `--ease-io` for folds, `--ease-out` for the rest.

| t | Dur | Element: motion (ease) |
| --- | --- | --- |
| press | 120 | seal: `scale(.97)` (out), feedback |
| 0 | 0 | whole seal swaps to two aligned halves: the crack |
| 0 | 180 | halves part: upper `translateY(-2px) rotate(-1.5deg)`, lower `translateY(1.5px)` (out) |
| 0 | 200 | label and twine: opacity 0 (out) |
| 140 | 1000 | top fold `rotateX(-180deg)` to 0 (io): lead, lifts against gravity |
| 140 | 1000 | `.move` `translateY(-D)` to 0 (io): carried with the lift |
| 140 | 1000 | top shade opacity 0, .14 at 50%, 0; hinge shadow 0, .2 at 40%, 0 (io) |
| 960 | 850 | bottom fold `rotateX(180deg)` to 0 (io), starts at 82% of the lift, falls faster; its shade as above |

Fully open at **1.81 s** (r8b 2.45 s). Inner content may start at 1.65 s; nothing else moves during the folds. Slower option: multiply all times by 1.25 (2.26 s).

## Seal

It sits on the top fold's free edge, over the bottom fold, and cracks along that edge. The upper half belongs to the top fold's outer face, the lower half to the bottom fold's. Each rides its fold and hides by `backface-visibility` past 90°: no fade, no leftover wax. The `<button>` stays a transparent hit area.

## Perspective and shading

Keep `perspective: 3200px; perspective-origin: 50% 50%` on `.move` (line 65; shorter flares past the screen). Origins: top `50% 100%`, bottom `50% 0` (lines 71, 73). `rotateX` only. Bake resting shadows into images; live shading is one gradient layer per face, opacity only.

## Skip and reduced motion

- Skip stays until the whole sequence ends (r8b hides it at the tap, line 424, so the drawing cannot be skipped). Mid-fold, Skip jumps to the end state.
- Reduced motion and weak phones: closed sheet fades out (200 ms), open sheet fades in (300 ms), no rotation.

## Asset layers (WebP, 2x of the 400 px sheet)

| Name | Size | Alpha |
| --- | --- | --- |
| `fold-top-out`, `fold-top-in` | 800 x 300 | yes, deckled edge |
| `sheet-mid` | 800 x 864 | no |
| `fold-bottom-out`, `fold-bottom-in` | 800 x 622 | yes |
| `seal-whole` | 228 x 228 | yes, baked shadow |
| `seal-top`, `seal-bottom` | 228 x 120 | yes, cut from `seal-whole` |

Estimate (inference): 200 to 330 KB plus r8b's 130 KB, far under 1500 KB. Text stays live. Use `<img>` so `decode()` runs before the tap (line 458).

## Five risks on a mid-range phone

1. Layer promotion stalls the first frame: `will-change: transform` on load, removed once open.
2. Filters or `mix-blend-mode` (sprig, line 99) on a rotating face repaint every frame.
3. iOS backface flicker where the folds overlap: `translateZ(.1px)` per face.
4. `.sheet` height changes at the tap (line 63): reflow; WhatsApp resizes `svh`.
5. Timers drift from transitions (lines 426 to 428): chain on `transitionend`.

Not verified: feel on a phone; byte sizes.
