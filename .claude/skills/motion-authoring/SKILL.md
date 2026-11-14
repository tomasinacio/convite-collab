---
name: motion-authoring
description: "Use when choosing and building the invitation's animation tooling: a measured bake-off between hand-coded SVG with GSAP, SVGator, Rive and Lottie Creator for each motion beat, then embedding the winner with accessibility controls. Not for deciding how the motion should feel; that comes from STORYBOARD.md."
---
<!-- owner: Tomas | canonical path: projects/wedding-invite/.claude/skills/motion-authoring/SKILL.md | review date: 2026-11-09 -->
<!-- rollback: rm -rf projects/wedding-invite/.claude/skills/motion-authoring -->

# Motion authoring (bake-off, then use the winner)

The user asked for the best of Rive, SVGator and Lottie Creator to be used. Do not pick by reputation: build the same beat in each, measure, and write the result to `motion/BAKEOFF.md`.

## Steps
1. Read `STORYBOARD.md` and pick the three beats that differ most: (A) ink draw of one traced branch, (B) wax seal tap plus flap lift, (C) small vector sparkle or petal drift.
2. Build each beat in four ways: hand-coded SVG with CSS or GSAP; SVGator export; Rive file with a state machine; Lottie Creator export. Keep the same art and the same duration.
3. Measure each build on an emulated phone with `playwright-cli` (see `illustrated-reveal` stage 6): added transfer size in KB, first frame time, frame drops with CPU throttled if the tool supports it, and result under reduced motion.
4. Fill `motion/BAKEOFF.md`: one row per beat and tool, with the numbers, a look score from the user, and the winner.
5. Use the winner per beat. A mixed result is fine; each extra runtime must justify its KB in the table.
6. Embed with the controls from the pipeline: real `<button>` tap target, visible Skip, `prefers-reduced-motion` fallback, `lang` per language, play once.

## What to check about each tool (unverified until measured)
| Tool | Expected role | Check before using |
| --- | --- | --- |
| Hand-coded SVG + GSAP | ink draw, washes, sequencing | GSAP license for plugins such as DrawSVG on the current terms |
| SVGator | visual authoring of the stroke draw-on, exports SVG, Lottie or JS | whether the free plan watermarks exports (one source says it does); do not ship a watermark |
| Rive | seal and flap as a state machine with an idle pulse | runtime size added to first load; canvas has no semantics, so the button stays HTML |
| Lottie Creator | small vector motion | JSON size and player size; it cannot carry raster washes |

## Rules
- Animate `transform` and `opacity` only. Use the vendored Emil skills in `.claude/skills/` for easing and timing.
- Every runtime library is pinned to an exact version and loaded from the project, not a CDN at runtime.
- If a tool needs an account or a license key, stop and ask the user; never create accounts or enter keys.
