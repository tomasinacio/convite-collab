# v14 draw-in research: painting elements on instead of fading

Owner: Tomas. Date: 2026-11-11. Status: thin. Of three free research runs, one finished (scene choreography) and two timed out (raster paint-on masks, pre-rendered options). The designer must do the missing checks itself.

## What the free run found (unverified, sources not opened by the main session)

- Grow from the base: scale from the bottom (`transform-origin: 50% 100%`), tiny per-element stagger (20 to 40 ms), from the center outward.
- Branches: start at the edge they come from and move inward along their direction; leaves scale from the stem point.
- Sketch then fill: ink outline drawn with `stroke-dashoffset` (`pathLength`), then a colour wash fades in under it.
- Timing for about 10 s: outline 0 to 0.8 s, ground growth 0.4 to 1.6 s, branches 1.0 to 2.5 s, flowers 2.0 to 4.0 s, wash 3.5 to 5.5 s, settle 5 to 8 s; overlap 10 to 20 percent so nothing animates alone. Treat these as a starting shape, not data.
- Doubt: the run suggested a `cubic-bezier(0.34, 1.56, 0.64, 1)` overshoot easing. That bounces; the brief is calm, so do not use it.
- Cited pages, to open and confirm: Josh `Comeau` "friendly introduction to SVG" (`pathLength`), `Codrops` "SVG drawing animation", `Codrops` SVG mask transitions (2026), CSS-Tricks "SVG line animation works". The claimed `Awwwards` "SEATED" example was not confirmed.

## Main session's assessment (inference, not verified in a browser)

| Technique | What animates | Compositor only | Phone cost | Fit |
| --- | --- | --- | --- | --- |
| Grow from the base (`scale` Y on a cut-out, origin at its foot, plus opacity) | transform, opacity | yes | low | best for grass, lavender, bindweed, flowers: the plant rises from the ground |
| Grow inward from the edge (`translate` plus slight `scale` from the cut end, plus opacity) | transform, opacity | yes | low | olive from the left, orange from the right |
| Mask wipe with a soft brush edge (`mask-image` gradient, animate `mask-position`) | mask-position | no, repaints | medium to high on big layers | a few small or medium hero pieces only; test on the 4x throttle |
| `clip-path` growth | clip-path | no | medium | avoid on large layers |
| Ink outline then wash (SVG, `stroke-dashoffset`) | stroke-dashoffset, opacity | partly | low for few paths | the user allowed this exception for a few ink lines; needs traced outline art |
| Alpha video or animated WebP | decoded frames | n/a | size and decode cost, iOS needs HEVC alpha | likely too heavy for 8 pieces in a 1.5 MB first load; avoid |
| SVG `feTurbulence` bloom | filter | no, repaints every frame | high | avoid |

Recommendation to test first: transform-based growth for most pieces (cheap, calm, can look painted when combined with a slightly staggered unfold and a soft fade of the edge), and one soft brush-edge mask wipe (`mask-position`) on one or two hero pieces (for example the `azulejo` panel wash, the gate wall) only if the reveal still holds 30 fps.

## Open questions for the designer to settle by trying

1. Does a mask wipe on a 3x asset hold 30 fps at CPU 4x on the reveal, or only when applied to one piece at a time?
2. Can a pre-baked soft-edge mask in the asset itself (an alpha ramp painted into the cut-out, then moved with `translate` inside an `overflow: hidden` wrapper) give a compositor-only wipe? This is the likely best trick: the mask edge is part of the moving image, nothing repaints.
3. Which three or four elements read best drawn, and which stay as fades.
