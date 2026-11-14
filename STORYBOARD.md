# STORYBOARD (seed, status DRAFT)

Timings are a starting proposal. The Opus 5.5 high agent rewrites this in pipeline stage 4; the user approves it at the gate. Total target 10 s (allowed 8 to 12 s).

| # | Beat | Start ms | Duration ms | Element | Property | Easing | Reduced motion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Idle pulse on the seal | 0 | loop | seal | `box-shadow` ring via `opacity` of a pseudo-element | ease-in-out | off |
| 1 | Tap: seal presses and fades | 0 (on tap) | 500 | seal | `transform: scale`, `opacity` | ease-out | fade only |
| 2 | Flap lifts | 400 | 1000 | flap | `transform: rotateX` | ease-in-out | skipped |
| 3 | Card rises | 1300 | 1000 | card | `transform: translateY` | ease-out | cross-fade 400 ms |
| 4 | Ink draws: stem, then leaves in a stagger | 2300 | 3500 | SVG strokes | `stroke-dashoffset` | ease-in-out | whole art fades in 600 ms |
| 5 | Wash blooms under the ink | 4300 | 3000 | WebP washes | `opacity`, `transform: scale` | ease-out | included in the fade |
| 6 | Monogram or names write on | 6500 | 2500 | SVG strokes | `stroke-dashoffset` | ease-in-out | included in the fade |
| 7 | Settle, focus moves to the invitation | 9000 | 1000 | all | none | n/a | immediate |

Controls: `Skip` visible from 0 ms and first in focus order. Plays once, then `localStorage` (wrapped in try/catch) shows the finished invitation on later visits, with a replay link.

Total reduced-motion path: at most 1600 ms.

Approved comps this storyboard is checked against: `comps/` (empty until stage 2).
