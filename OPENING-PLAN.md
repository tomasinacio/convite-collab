# Opening plan: seal and two-fold letter (state of 2026-11-10)

Owner: Tomas. Review date: 2026-11-17. Rollback: `rm -f projects/wedding-invite/OPENING-PLAN.md`.

## Scope (user, 2026-11-10)

Only the opening: wax seal plus a folded letter (two folds, top lifts then bottom drops; not a triangular envelope), from the tap until the sheet is fully open (about 0 to 2.45 s in `comps/prototype.html`, r8b). Folds, dynamic content and timings must add up with the pack: see `MOTION-NOTES.md` section r8b and `DESIGN.md` Opening. After the sheet is open the work is not mine.

## User decisions

- Seal that looks like a photograph, made for free.
- Use what the Digital Yes site used where it makes sense: their opening is a pre-rendered 3 to 4 s portrait mp4 (nautical 1.4 MB HEVC, floral 2.2 MB H.264) on a React and Vite page. Plain flat CSS would look cheap.
- Research with free model agents (`delegate/batch.sh`, the `researcher` agent, run on the VM), not paid parallel agents.
- Copilot app first: test it through `desk` before any art work.

## Proposed approach (needs the user's go)

A/B on the same 0 to 2.45 s beat, the user picks by looking:

- A: layered code. Each fold is a separate textured image (like a photograph paper, seal, baked shading) moved with 3D transforms; live text and any later layout stay in code.
- B: rendered mp4 like the Digital Yes site, on a fixed-ratio stage ending on an empty open sheet; live names, date and place fade in over its last frame. Poster image first, muted `playsinline`, H.264 fallback, Skip, reduced-motion fallback.

One Opus 5.5 high design adviser re-times the window first (the user said the r8b timings are off), using `choreograph`, `animate`, `review-animations`. Then red team and `spec-guardian`, then the user approves.

## Research findings (free lane, 2026-11-10; Reddit threads were never read, 502 errors)

- iOS auto-play needs muted plus `playsinline`; Low Power Mode blocks auto-play completely. Android Chrome allows muted plus inline. WhatsApp in-app browser behaviour is undocumented: test on real phones.
- 1 MB at 720x1280 for 3 to 5 s is feasible with H.264 (CRF 25 to 27, or two-pass); ladder AV1, VP9, HEVC, H.264. Poster plus `preload="none"` defers the video. WCAG 2.2.2: auto-play over 5 s needs a pause control.
- Guests tolerate about 3 s of intro (Reddit snippets, unverified). Reference: GSAP Vault wedding template (3D flap, about 1.2 s tap, opens once, reduced motion starts open, drag to open).
- AI video: `Kling` free tier about 66 credits a day, watermark, 720p; free output is personal use only; `Kling` and `Luma` take start and end frames; paper and seal warping is the usual failure.
- Blender: no benchmark found for this class of machine. Poly Haven is CC0. No free wax seal model found. The Blender MCP server runs arbitrary code.
- Gaps: no example of a two-fold top-then-bottom opening; no mid-range phone frame-rate data.

## Skills and tools added today

Pinned in `vendor/SOURCES.md`: `accessibility`, `performance`, `core-web-vitals` (web-quality-skills), `accessible-animation` (web-animation-skills), and `vendor/axe-core/axe.min.js` (axe-core 4.10.2, MPL-2.0). Linked in `.claude/skills/`, listed in `CLAUDE.md`. New skills load at the next session start. No runner for axe yet.

## Machines

- This WSL box: 2 GB RAM cap (`.wslconfig`), 4 cores.
- Windows PC: i5-8250U, 8 GB RAM, Intel UHD 620 (no real GPU), 41 GB free. Blender official Windows build is portable and free; CPU stills only.
- VM (`ubuntu@100.120.13.126`): aarch64, 4 cores, 24 GB. Blender publishes no Linux arm64 build, so it would need apt or snap (root). Tailscale SSH can ask for re-auth (`vm.sh` exit 3).

## Blockers and next steps

1. `desk` returns Unauthorized in the agent shell (`scripts/doctor.sh`). The session was not started with `./start.sh`. The user restarts through `./start.sh` in this folder; then test Copilot end to end (skill `copilot-image`, test prompt: terracotta wax seal with olive sprig on cream paper).
2. Judge the Copilot seal for photographic realism with the Opus adviser. If it fails or a transparent controlled render is needed, render on the Windows PC with portable Blender (free, no account).
3. Adviser re-times the beat, then A and B are built, measured (4x throttle, iPhone 15 emulation, real phone, WhatsApp), reviewed and shown to the user.

## Status (2026-11-11, morning)

- Page: `comps/prototype.v9.standalone.html` (one file, 412 KB, opens by double-click; fonts come from Google Fonts). Source: `comps/prototype.v9.html` with layers in `comps/art/v9/`. r8b (`comps/prototype.html`) is untouched.
- Seal: the user made it in the Copilot app (prompt 1 of the advice); cut out with `extract_asset.py --matting`; two crack halves baked by `comps/art/v9_seal_photo.py`. The procedural seal stays in `comps/art/v9/fallback/`.
- Done: adviser (`OPENING-ADVICE.md`), two red-team rounds and one `spec-guardian` pass (`REDTEAM.md`). Open at 1.68 s; names write from 2.45 s as in r8b; date, tile mark and place from 3.5 s.
- Measured at 4x CPU, iPhone 15 emulation: about 60 fps, p95 16.8 ms, 0 to 1 frames over 33 ms. Not checked on a real phone or in WhatsApp.
- Open: fold faces are soft stand-ins (deck crops, quality gate says soft; not for `build/`); fold edges look blocky while moving in Chromium (`?sharp=1` tests a sharper mode); user decisions in `OPENING-ADVICE.md` section 7 (twine, seal on tap, pace) were taken as the recommended options, not confirmed by the user.
- Environment: run Claude from the Ubuntu terminal via `./start.sh`; `.wslconfig` change suggested (memory 4 GB, `vmIdleTimeout=-1`) but not applied.

## Status (2026-11-11, evening)

- Files sent to the user: `comps/prototype.v9.standalone.html` (opening only), `prototype.v10.opening.single.html`, `prototype.v11.single.html`, `prototype.v12.single.html` (dogs, citrus), `prototype.v13.single.html` (slower overlapping reveal, new art). Sources `prototype.vNN.src.html`, builds `comps/art/v10_build.py` and `v13_build.py`. The user's own page is the v10 upload; `comps/prototype.v10.orig.single.html` is untouched.
- Advice files: `OPENING-ADVICE.md`, `V10-ATMOSPHERE-ADVICE.md`, `V12-CHOREOGRAPHY-ADVICE.md`; decisions in `REDTEAM.md`.
- Queued: `V14-BRIEF.md` (user feedback on v13: remove the crossing swallow, bigger dolce-vita style dogs, orange branch instead of dangling fruit, new falling-leaf rhythm, reveal performance). The Opus designer (agent `a28da0c9cf52d7a22`) is blocked by the usage limit until 20:00 Lisbon; a session-only job sends it the brief at 20:07. If the session closed, resume the designer by hand.
- Measured (quiet machine, CPU 4x, iPhone 15 emulation): v12 46 to 60 fps throughout; v13 57 to 60 fps idle but 12 to 28 fps during the reveal (2.5 to 10 s). Scripts in `comps/art/perf/`.
- Art made by the user in Copilot is in `assets/inbox/` (`dogs/`, `new-art/`, `seal-v9/`), logged in `assets/LOG.md`.
- Desk key: `scratchpad` wrapper only; the free research lane runs on this PC when the VM needs a Tailscale sign-in.
