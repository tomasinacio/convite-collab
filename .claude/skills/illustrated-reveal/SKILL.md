---
name: illustrated-reveal
description: "Use when building an animated illustrated intro for a web page: an envelope or card that opens on tap, hand-drawn ink lines and watercolor washes that draw in, phone-first, accessible to all ages. Runs the full pipeline from art direction through free image generation, asset extraction, storyboard, build, phone verification and audit. Not for ordinary page layout or for full-site design."
---
<!-- owner: Tomas | canonical path: projects/wedding-invite/.claude/skills/illustrated-reveal/SKILL.md | review date: 2026-11-09 -->
<!-- rollback: rm -rf projects/wedding-invite (the whole project is self-contained) -->

# Illustrated reveal (art-led pipeline)

One pipeline, not a pile of skills: each stage has an owner, a tool, an output file and a gate. Do not start a stage before the previous gate is passed by the user.

## Steps
Work through these sections in order: "Who does what", "0. Brief", "1. Direction", "2. Keyframe comps", "3. Art sourcing and asset factory", "4. Motion storyboard", "5. Build", "6. Verify on phones", "7. Audit", "8. Real-device test". Stages 1, 2 and 4 are aesthetic: they run on an Opus 5.5 agent at high effort. Stop after each gate and report in 5 lines or fewer.

## Who does what
- **Aesthetic and artwork (stages 1, 2, 3 prompts, 4): Opus 5.5, high effort.** Art direction, palette, keyframe prompts, asset prompts, style judging, motion feel. In Claude Code: Agent tool with `model: "opus"` and `effort: "high"`. The same rule is in the project `CLAUDE.md`. Never hand these to a smaller model.
- **Mechanical work (stage 3 extraction, 5 build, 6 capture):** any tier. Brief it with the stage output contract.
- **The user decides taste.** Every gate is a user choice between shown options, never a self-approval.
- A subagent brief names this skill, the stage, the files to read, and a reply cap (`shared/SUBAGENT-BRIEF.md`).

## 0. Brief
Inputs to collect once, then freeze in `DESIGN.md`: palette tokens with hex, type pairing, copy (names, dates, venue: written by the user, never invented), languages, the tap target, the sequence length (8 to 12 s), the fallback.
- Gate: user confirms the frozen brief.

## 1. Direction
First gather references and a style tile (`designer-playbook` sections 1 and 2).
Opus writes `DESIGN.md` in the project root: tokens, type roles, motifs, a "never" list of generic-AI defaults (cream-plus-serif-plus-terracotta used by reflex, identical card grids, purple gradients, Inter by default), contrast rules (text 4.5:1 minimum), and motion rules.
- Method: one concrete aesthetic direction before any code; check it against the "never" list; revise once.
- Reference material: `vendor/emil-skills/emil-design-eng/SKILL.md` for taste on motion; `vendor/SOURCES.md` for what else is vendored.
- Gate: user approves `DESIGN.md`.

## 2. Keyframe comps
Generate 6 stills of the sequence: sealed, flap lifting, card rising, ink half-drawn, wash blooming, finished. Approved stills are the target the build is compared against.
- Same style lock for all 6 (see stage 3), same canvas ratio (9:19.5 phone portrait).
- Gate: user picks or rejects each still. Rejected stills are regenerated, never patched in code.

## 2b. Red team (after stage 2, again before stage 8)
A clean-slate Opus 5.5 high agent (`.claude/agents/red-team.md`) gets only the brief (`SPEC.md`, `DESIGN.md`) and the rendered face: no designer rationale. It reports divergence from the brief, contrast and noise, and anything not clean and elegant. The designer Opus then decides, item by item, what to implement and why, and both are written to `comps/REDTEAM.md`. Gate: the user sees the decisions.

## 3. Art sourcing and asset factory
Goal: assets that look hand-made and pass the quality gate. Two skills do the work; this stage only sequences them.
1. `designer-playbook`: references, style tile, and the sourcing order (A hand-painted scan, B public-domain plates, C licensed packs, D AI generation, E keyless concepts). Prefer A to C; use D only for motifs they cannot supply.
2. `asset-factory`: generation routes (Copilot, keyed, free), extraction, Qwen-Image-Layered, ink tracing, logging. It holds the single list of routes.
3. Every asset passes `scripts/image_quality.py ASSET --role asset|hero|small` before it enters `build/`. A FAIL means regenerate or re-source, never patch in code.
4. Gate: the user approves the asset sheet (all assets side by side on the paper color).

## 4. Motion storyboard
Opus writes `STORYBOARD.md`: a table of beats with start ms, duration ms, element, easing and reduced-motion behaviour. Total 8000 to 12000 ms.
- Apply `vendor/emil-skills/animate/SKILL.md`, `choreograph/SKILL.md` and `animation-vocabulary/SKILL.md`. Animate only `transform` and `opacity`.
- Opening is vertical: flap lifts up, the invitation continues downward into a scroll; no side opening.
- Required beats: tap target pulse (stops under reduced motion), flap, card rise, ink draw by stroke, wash bloom, names write-on, settle.
- Required controls: visible Skip, plays once then remembers (`localStorage`, wrapped in try/catch), replay link.
- Fallback for weak phones and reduced motion: envelope opens, art fades in, no drawing motion.
- Gate: user approves `STORYBOARD.md`.

## 5. Build
- Stack by default: SVG stroke drawing (`stroke-dashoffset` with `pathLength="1"`), washes as WebP revealed by masks, GSAP timeline if the storyboard needs sequencing. Rive or SVGator only for one asset that needs a state machine or visual editing; Lottie Creator does not suit raster washes (inference).
- The tap target is a real `<button>` with an accessible name per language and a `lang` attribute on it. Focus moves into the intro on open and to the invitation on end. Skip is a real button reachable first.
- Page weight: first load under 1500 KB, stretch 500 KB. Measure; do not guess.
- Per-guest language and greeting come from an unguessable code in the link; never put names in the URL.

## 6. Verify on phones
Use `playwright-cli --config .playwright/cli.config.json` (installed and tested 2026-11-09; run `source scripts/env.sh` first). Serve the build over `http://127.0.0.1`; `file:` URLs are blocked.
1. `playwright-cli open --device="iPhone 15"` and one Android device; screenshot each storyboard beat.
2. `video-start` and `video-stop` over the full sequence; review frames against the approved comps.
3. Run once with reduced motion on and confirm the fallback; run once with the animation skipped.
- Chromium is installed under `~/.cache/ms-playwright` and its two missing system libraries are unpacked in `.local-libs/` (no sudo needed). `scripts/env.sh` wires both.
- Gate: frames match comps within the user's tolerance; user signs off.

## 7. Audit
1. Vercel rules: read `vendor/web-design-guidelines/command.md` and apply every rule to the changed files; output `file:line` findings. This is a pinned local copy: do not fetch the rules from the internet.
2. Motion review: `vendor/emil-skills/review-animations/SKILL.md`.
3. Contrast: every text and background pair measured, 4.5:1 minimum.
4. Copy check: every name, date and place on the page matches the user's brief exactly.
5. Slop check: compare against the "never" list in `DESIGN.md`; list each hit.
- Gate: zero open findings, or each one accepted by the user.

## 8. Real-device test
Send the real link through WhatsApp to one iPhone and one Android phone, open it from the chat, and test once on Low Power Mode and once with a slow connection. Ask one older relative to open it without help. Record results in `TEST-LOG.md`.

## Taste Skill (installed, scoped)
Installed as `design-taste-frontend` from a pinned clone (`f6b76575f949707b4e3c37cd86cb44b0b98643e8`, `vendor/SOURCES.md`). Use it in stage 1 for its plan-then-check loop and in stages 6 and 7 for its scripts: `shoot.mjs` (screenshots at set widths, reduced motion), `consistency.mjs`, `perf.mjs`, `copy-lint.mjs`. Run them with `source scripts/env.sh` first so `CHROME_PATH` and the local libs are set. Its company-site house rules (one section per screen, no captions, shader limits) do not apply to the invitation face; `DESIGN.md` wins. Its Stop-hook gate runs only when a `.taste-skill/build.json` exists in the working folder; do not run `start.mjs deal` here.
