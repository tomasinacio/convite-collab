#!/usr/bin/env python3
"""Split an image into RGBA layers with the Qwen-Image-Layered Hugging Face Space.

owner: Tomas | review date: 2026-11-09
canonical path: projects/wedding-invite/scripts/qwen_layers.py
rollback: rm -f projects/wedding-invite/scripts/qwen_layers.py

The Space's API signature is unconfirmed (2026-11-09). Discover it first:
  qwen_layers.py --view-api
Then call it. "{IMAGE}" in --args-json is replaced by the uploaded image:
  qwen_layers.py IN.png OUTDIR --api-name /NAME --args-json '["{IMAGE}", 4]'
Free usage is ZeroGPU quota limited. Sends the image to huggingface.co; use only art
the user approved for that. Never pass tokens on the command line.
"""

import argparse
import json
import os
import shutil
import sys

from gradio_client import Client, handle_file

SPACE = "Qwen/Qwen-Image-Layered"


def collect(result):
    """Flatten any nested result into a list of existing file paths."""
    if isinstance(result, str) and os.path.exists(result):
        return [result]
    if isinstance(result, dict):
        out = []
        for v in result.values():
            out += collect(v)
        return out
    if isinstance(result, (list, tuple)):
        out = []
        for v in result:
            out += collect(v)
        return out
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?")
    ap.add_argument("outdir", nargs="?")
    ap.add_argument("--view-api", action="store_true")
    ap.add_argument("--api-name")
    ap.add_argument("--args-json", default='["{IMAGE}"]')
    a = ap.parse_args()

    client = Client(SPACE)  # HF_TOKEN, if needed, is read from the environment by the library
    if a.view_api:
        client.view_api()
        return 0
    if not (a.src and a.outdir and a.api_name):
        print("need SRC OUTDIR --api-name (run --view-api first)", file=sys.stderr)
        return 2
    args = [handle_file(a.src) if x == "{IMAGE}" else x for x in json.loads(a.args_json)]
    result = client.predict(*args, api_name=a.api_name)
    files = collect(result)
    if not files:
        print("no files in result:", result, file=sys.stderr)
        return 1
    os.makedirs(a.outdir, exist_ok=True)
    for i, f in enumerate(files):
        dst = os.path.join(a.outdir, f"layer-{i:02d}{os.path.splitext(f)[1] or '.png'}")
        shutil.copy(f, dst)
        print(dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
