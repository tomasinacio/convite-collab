---
name: asset-factory
description: "Use when producing the invitation artwork: generating one asset per image in a locked style, cutting each out with a matting model, splitting a composition into layers with Qwen-Image-Layered, tracing ink to single-stroke SVG, and logging every asset's source and license. Not for deciding the aesthetic; that goes to the Opus 5.5 high-effort agent."
---
<!-- owner: Tomas | canonical path: projects/wedding-invite/.claude/skills/asset-factory/SKILL.md | review date: 2026-11-09 -->
<!-- rollback: rm -rf projects/wedding-invite/.claude/skills/asset-factory -->

# Asset factory

Goal: assets that look like one hand made them, and do not look AI-generated. Aesthetic judgement (prompts, style, what is good enough) is done by an Opus 5.5 agent at high effort (`model: "opus"`, `effort: "high"`). This skill is the mechanics.

## Steps
1. Style lock: write `assets/STYLE.md` once (one paragraph plus one approved reference image path). Paste it verbatim into every generation prompt.
2. Generate one asset per image, flat solid background, no shadow, no paper texture. Ink line art and color wash are separate generations. Routes in order (details in "Generation routes"): (a) Copilot app via `desk`; (b) Hugging Face, Cloudflare or Gemini key through `scripts/free_image.py`; (c) an image model on OmniRoute or OpenRouter; (d) Pollinations, keyless, concepts only. Before generating, check whether `designer-playbook` sources A to C already supply the motif.
3. Cut out: `.venv/bin/python scripts/extract_asset.py IN.png OUT.webp --matting`. The model downloads on first run.
4. Optional, whole compositions only: `.venv/bin/python scripts/qwen_layers.py --view-api`, then run with the printed signature. Details in "Qwen-Image-Layered".
5. Trace ink for the drawing effect: centerline, not outline (`autotrace -centerline`, KDRAW or svgo centerline), then clean paths by hand. Set `pathLength="1"` on each path for the stroke animation.
6. Log every file in `assets/LOG.md`: file, tool, model, date, prompt, license terms. An asset with no log line is not used.
7. Show all assets side by side to the user. They approve or reject each; rejected ones are regenerated.

## Look rules (anti-AI)
- Uneven wash edges, visible ink weight changes, small asymmetries.
- No airbrushed gradients, no perfect symmetry, no text inside images, no hands or faces.
- Three leaf shapes at most per branch; vary them by hand after tracing.
- Compare against the approved comps from `illustrated-reveal` stage 2. Anything off-style is regenerated, never patched.

## Generation routes
- **Copilot app via `desk`:** `~/.local/bin/desk see`, then act on coordinates it prints; re-run `see` after every change. On 2026-11-09 `desk see` returned `Unauthorized` from `http://127.0.0.1:8932/mcp`; the server needs to be restarted by the user (`start-desktop-mcp.ps1` on Windows). Never type credentials. Downloads from the app are saved to a fresh folder and logged.
- **OmniRoute / OpenRouter:** image output uses chat completions with `modalities: ["image","text"]`. No image-capable model appears in `delegate/models.ro.txt` or `delegate/models.rw.txt` on 2026-11-09. Add one only after the user supplies a key through the gateway; never read key files.
- **Free tiers:** quotas change; read the current terms before relying on one and log them.
- **Pollinations (keyless):** tested 2026-11-09; 768 px, a corner mark, rate limited, and it fails `scripts/image_quality.py` (too small, soft, JPEG blocking). Use it for concepts only. Final art comes from Copilot, a keyed route, or the sourcing ranks A to C.
- Every generated image gets `scripts/image_quality.py` run on it; `free_image.py` runs it automatically.

## Qwen-Image-Layered
- Splits one image into several transparent RGBA layers; Apache 2.0; model is `Qwen/Qwen-Image-Layered`.
- This machine has no GPU (`nvidia-smi` missing on 2026-11-09). Use the Hugging Face Space `Qwen/Qwen-Image-Layered` through `scripts/qwen_layers.py` (free, ZeroGPU quota limited: reports show a daily quota message for free accounts), Comfy Cloud or RunComfy (about $0.05 per image), or a rented GPU.
- The Space's API signature is unconfirmed: run `--view-api` first and pass the printed endpoint with `--api-name` and `--args-json`.
- Use it on the full keyframe comps (stage 2) to get a layer stack for motion; use per-asset extraction (step 3) for the final assets.
