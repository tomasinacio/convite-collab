# Wedding invitation face: start here

Everything for the invitation's face lives in this folder. Nothing here loads in normal `~/agent-config` sessions.

## Start work (30 seconds)

```bash
cd ~/agent-config/projects/wedding-invite
./start.sh
```

`start.sh` puts every tool on PATH, loads the `desk` key for this session only (so Claude can drive the Copilot app), prints the health check, and opens Claude Code. Then say: `Run illustrated-reveal from stage 0.`

Health check any time: `scripts/doctor.sh` (exit 0 means no FAIL; WARN lines are optional or need you).

## What was tested on 2026-11-09

| Piece | Result |
| --- | --- |
| 15 skills in `.claude/skills/` (Taste, Emil x8, Vercel rules, pipeline, asset factory, Copilot, motion) | all resolve |
| Taste Skill scripts (`shoot.mjs`) with local Chromium | works |
| `playwright-cli` with iPhone 15 emulation, reduced motion, screenshot | works (needs `--config .playwright/cli.config.json`, serve pages over `http://127.0.0.1`) |
| `scripts/extract_asset.py` (matting cutout to WebP alpha) | works; clean cutout |
| `scripts/free_image.py` via `Pollinations` (keyless) | works in bursts, then HTTP 402/404; 768 pixels with a corner mark; **fails the quality gate, so concept art only** |
| `scripts/image_quality.py --selftest` | correct verdicts on two independent real scans (PASS), clean cutout (PASS), and fake enlargements, grain, heavy JPEG, tiny, white-fringed cutout and free-route images (FAIL). It checks technical quality only; "AI-sloppy" (mangled forms, smearing) is judged by an Opus 5.5 high agent and by you at the asset gate |
| `scripts/open_art.py` public-domain plates from `Wikimedia` Commons, with contact sheets | works; real 4000 pixels watercolor lemons found (`assets/sheets/`) |
| Real scan to cutout to quality gate | works: fig plate cut out, PASS, edges clean |
| `scripts/contrast.py` | all palette text pairs pass 4.5:1 |
| Palette, mood board | `DESIGN.md`; live page published earlier in the research chat |

## What needs you (5 minutes each, optional but recommended)

| Need | Why | How |
| --- | --- | --- |
| Run via `./start.sh` | the `desk` key rotates daily and agents cannot read it | just use the script |
| `desk` server up | Copilot control | if `scripts/doctor.sh` says down: run `C:\Users\tomin\.windows-mcp\start-desktop-mcp.ps1` on Windows |
| A free key for one image route | the keyless route fails the quality gate and Copilot credits end; this is needed, not optional, for generated art | Hugging Face token (free) as `HF_TOKEN`, or Cloudflare Workers AI (`CF_ACCOUNT_ID`, `CF_API_TOKEN`), or Gemini (`GEMINI_API_KEY`). Export it before `./start.sh`. Never paste keys in chat. |
| OmniRoute or OpenRouter image model | free-model route | add an image-output model, then set `OMNIROUTE_BASE_URL`, `OMNIROUTE_API_KEY`, `OMNIROUTE_IMAGE_MODEL` (none is listed in `delegate/models.*.txt` today) |
| Qwen-Image-Layered | no GPU on this machine | use the Hugging Face Space through `scripts/qwen_layers.py` (free quota is limited), or a paid host; see `asset-factory` |
| Rive, `SVGator`, Lottie Creator accounts | the bake-off | create accounts yourself; the agent stops and asks |

## Not tested

- Driving the Copilot app end to end (`copilot-image`): blocked on the `desk` key from the agent shell until you start through `./start.sh`.
- Qwen-Image-Layered Space call (API signature unconfirmed; run `scripts/qwen_layers.py --view-api`).
- OpenRouter, OmniRoute, Cloudflare, Hugging Face and Gemini routes in `free_image.py` (written from documented request formats, no keys to test with).
- Video recording with `playwright-cli`.
- The final invitation itself: nothing is built yet. `build/` is empty by design.

## How it is organised

- `CLAUDE.md` rules and model routing: artwork and aesthetics go to an Opus 5.5 agent at high effort.
- `SPEC.md` your exact words; `.claude/agents/spec-guardian.md` audits the work against them.
- `DESIGN.md`, `STORYBOARD.md`, `assets/STYLE.md`, `motion/BAKEOFF.md` seeded drafts; the pipeline refines and you approve at each gate.
- `vendor/` pinned third-party rules and Emil's skills (`vendor/SOURCES.md`); Taste Skill is a pinned clone at `~/.local/share/design-skills/taste-skill`.
