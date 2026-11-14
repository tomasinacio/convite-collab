#!/usr/bin/env python3
"""Cut one generated asset out of its flat background and save it as WebP with alpha.

owner: Tomas | review date: 2026-11-09
canonical path: projects/wedding-invite/scripts/extract_asset.py
rollback: rm -f projects/wedding-invite/scripts/extract_asset.py

Usage: extract_asset.py IN.png OUT.webp [--model NAME] [--matting] [--pad PX]
Needs: .venv with rembg[cpu] and pillow. First run downloads the model (network).
"""

import argparse
import sys

from PIL import Image
from rembg import new_session, remove


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--model", default="isnet-general-use")
    ap.add_argument(
        "--matting", action="store_true", help="alpha matting for soft watercolor edges"
    )
    ap.add_argument("--pad", type=int, default=8)
    a = ap.parse_args()

    session = new_session(a.model)
    img = Image.open(a.src).convert("RGBA")
    out = remove(
        img,
        session=session,
        alpha_matting=a.matting,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
    )
    bbox = out.getchannel("A").getbbox()
    if bbox is None:
        print("empty cutout: nothing found", file=sys.stderr)
        return 1
    x0, y0, x1, y1 = bbox
    x0, y0 = max(x0 - a.pad, 0), max(y0 - a.pad, 0)
    x1, y1 = min(x1 + a.pad, out.width), min(y1 + a.pad, out.height)
    out = out.crop((x0, y0, x1, y1))
    out.save(a.dst, "WEBP", lossless=True, quality=90, method=6)
    print(f"{a.dst}: {out.width}x{out.height}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
