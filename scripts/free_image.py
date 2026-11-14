#!/usr/bin/env python3
"""Generate one image from a prompt through a free or key-based route.

owner: Tomas | review date: 2026-11-09
canonical path: projects/wedding-invite/scripts/free_image.py
rollback: rm -f projects/wedding-invite/scripts/free_image.py

Usage:
  free_image.py --prompt "olive branch, ink outline" OUT.png [--route ROUTE]
  ROUTE is auto, pollinations, cloudflare, hf, gemini, openrouter or omniroute.
  free_image.py --prompt-file p.txt OUT.png --no-style
By default assets/STYLE.md (the locked style paragraph) is prepended to the prompt.

Routes (status checked 2026-11-09):
  pollinations  no key. TESTED 2026-11-09: works in bursts, then HTTP 402/404 (quota);
                768 px; a small
                "pollinations.ai" mark in the corner (crop it). Treat as a bonus, not a supply.
  cloudflare    env CF_ACCOUNT_ID + CF_API_TOKEN. FLUX.1 schnell on the free tier. Untested.
  hf            env HF_TOKEN. FLUX.1 schnell via the Hugging Face router. Untested.
  gemini        env GEMINI_API_KEY (+ optional GEMINI_IMAGE_MODEL).
                Sources disagree whether a free tier exists. Untested.
  openrouter    env OPENROUTER_API_KEY + OPENROUTER_IMAGE_MODEL.
                Needs an image-output model. Untested.
  omniroute     env OMNIROUTE_BASE_URL + OMNIROUTE_API_KEY + OMNIROUTE_IMAGE_MODEL.
                Untested; no image model was listed in
                delegate/models.*.txt on 2026-11-09.
Keys are read from the environment only. Never pass them on the command line. Standard library only.
"""

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = os.path.join(HERE, "..", "assets", "STYLE.md")
UA = {"User-Agent": "wedding-invite-free-image/1.0"}


def http(url, data=None, headers=None, timeout=120):
    req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("content-type", "")


def pollinations(prompt, a):
    """Anonymous use is rate limited: one request alternates 200 and 402/404. Retry."""
    q = urllib.parse.urlencode(
        {"width": a.size, "height": a.size, "seed": a.seed, "model": "flux", "nologo": "true"}
    )
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?{q}"
    last = None
    for attempt in range(4):
        try:
            body, ctype = http(url)
            if ctype.startswith("image/"):
                return body
            last = RuntimeError(f"not an image: {ctype}")
        except urllib.error.HTTPError as e:
            last = RuntimeError(f"HTTP {e.code} (anonymous quota or rate limit)")
        time.sleep(10 * (attempt + 1))
    raise last


def cloudflare(prompt, a):
    acc, tok = os.environ["CF_ACCOUNT_ID"], os.environ["CF_API_TOKEN"]
    url = f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    body, _ = http(
        url,
        json.dumps({"prompt": prompt[:2000], "steps": 4}).encode(),
        {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
    )
    return base64.b64decode(json.loads(body)["result"]["image"])


def hf(prompt, a):
    tok = os.environ["HF_TOKEN"]
    body, _ = http(
        "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell",
        json.dumps({"inputs": prompt}).encode(),
        {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
    )
    return body


def gemini(prompt, a):
    key = os.environ["GEMINI_API_KEY"]
    model = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    body, _ = http(
        url,
        json.dumps(payload).encode(),
        {"x-goog-api-key": key, "Content-Type": "application/json"},
    )
    for part in json.loads(body)["candidates"][0]["content"]["parts"]:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline:
            return base64.b64decode(inline["data"])
    raise RuntimeError("no image part in the response")


def chat_image(base, key, model, prompt):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
    }
    body, _ = http(
        base.rstrip("/") + "/chat/completions",
        json.dumps(payload).encode(),
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    msg = json.loads(body)["choices"][0]["message"]
    for im in msg.get("images", []):
        m = re.match(r"data:image/[a-z]+;base64,(.*)", im["image_url"]["url"], re.S)
        if m:
            return base64.b64decode(m.group(1))
    raise RuntimeError("no image in the response")


def openrouter(prompt, a):
    return chat_image(
        "https://openrouter.ai/api/v1",
        os.environ["OPENROUTER_API_KEY"],
        os.environ["OPENROUTER_IMAGE_MODEL"],
        prompt,
    )


def omniroute(prompt, a):
    return chat_image(
        os.environ["OMNIROUTE_BASE_URL"],
        os.environ["OMNIROUTE_API_KEY"],
        os.environ["OMNIROUTE_IMAGE_MODEL"],
        prompt,
    )


ROUTES = {
    "pollinations": pollinations,
    "cloudflare": cloudflare,
    "hf": hf,
    "gemini": gemini,
    "openrouter": openrouter,
    "omniroute": omniroute,
}
NEEDS = {
    "cloudflare": ["CF_ACCOUNT_ID", "CF_API_TOKEN"],
    "hf": ["HF_TOKEN"],
    "gemini": ["GEMINI_API_KEY"],
    "openrouter": ["OPENROUTER_API_KEY", "OPENROUTER_IMAGE_MODEL"],
    "omniroute": ["OMNIROUTE_BASE_URL", "OMNIROUTE_API_KEY", "OMNIROUTE_IMAGE_MODEL"],
}


def gate(path):
    """Run the quality gate and say plainly whether the image is usable as final art."""
    try:
        sys.path.insert(0, HERE)
        import image_quality

        _, problems = image_quality.analyze(path, "asset")
    except Exception as e:  # the gate must never hide a generated file
        print(f"quality gate could not run: {e}", file=sys.stderr)
        return
    if problems:
        print("QUALITY: FAIL, not usable as final art (concept only):")
        for p in problems:
            print("  -", p)
    else:
        print("QUALITY: PASS")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--prompt")
    ap.add_argument("--prompt-file")
    ap.add_argument("--route", default="auto")
    ap.add_argument("--size", type=int, default=768)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--no-style", action="store_true")
    a = ap.parse_args()
    prompt = a.prompt or (open(a.prompt_file).read() if a.prompt_file else "")
    if not prompt.strip():
        print("need --prompt or --prompt-file", file=sys.stderr)
        return 2
    if not a.no_style and os.path.exists(STYLE):
        prompt = open(STYLE).read().strip() + "\n\n" + prompt
    order = (
        [r for r in ROUTES if r == "pollinations" or all(os.environ.get(k) for k in NEEDS[r])]
        if a.route == "auto"
        else [a.route]
    )
    # keyed routes first, keyless last
    order.sort(key=lambda r: r == "pollinations")
    last = None
    for r in order:
        try:
            img = ROUTES[r](prompt, a)
            os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
            with open(a.out, "wb") as f:
                f.write(img)
            print(f"{a.out}: {len(img)} bytes via {r}")
            print(f"LOG: route={r} file={a.out} (add a row to assets/LOG.md: prompt, terms)")
            gate(a.out)
            return 0
        except KeyError as e:
            last = f"{r}: missing env {e}"
        except (urllib.error.URLError, RuntimeError, ValueError) as e:
            last = f"{r}: {e}"
        print("route failed:", last, file=sys.stderr)
    print("no route succeeded:", last, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
