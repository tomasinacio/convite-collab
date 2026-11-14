#!/usr/bin/env python3
"""Bake the bottom flap's outside for prototype.v10.opening: v10's paper (P2), torn free edge.

owner: Tomas | review date: 2026-11-18
canonical path: projects/wedding-invite/comps/art/v10_bake.py
rollback: rm projects/wedding-invite/comps/art/v10_bake.py
  projects/wedding-invite/comps/art/v10/fold-bottom-out.webp

Usage: .venv/bin/python -I comps/art/v10_bake.py
  reads  comps/art/v10/src/00-img-paper.webp (P2 paper tile, extracted from the user's v10 upload)
  writes comps/art/v10/fold-bottom-out.webp (800 x 784: 2x of the 400 x 392 px flap, Hb = .98 W)

Why: in the new opening the two flaps' free edges meet under the seal, so the bottom flap is
.98 W tall, and v10's closed-bottom image (a v9 stand-in with a crease baked at a quarter of its
height) no longer fits. The flap's outside is shown only while closed and folding, so the tile
phase does not matter; the torn edge sits at the top of the image, the flap's free edge once folded.
"""

import os
import sys

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v9_bake import deckle_offsets  # noqa: E402

TILE = os.path.join(HERE, "v10", "src", "00-img-paper.webp")
OUT = os.path.join(HERE, "v10", "fold-bottom-out.webp")
W, H = 800, 784
T = 682  # the page shows the tile at 341 px; 2x


def main():
    # the source tile has JPEG blocking (gate: 3.4); a light blur before reducing softens it
    tile = Image.open(TILE).convert("RGB").filter(ImageFilter.GaussianBlur(0.7))
    tile = tile.resize((T, T), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H))
    for y in range(0, H, T):
        for x in range(0, W, T):
            canvas.paste(tile, (x, y))
    rgb = np.asarray(canvas, np.float32)
    rng = np.random.default_rng(21)
    yy = np.mgrid[0:H, 0:W][0].astype(np.float32)
    off = deckle_offsets(rng, W, 3.2, 2.0)[None, :]
    alpha = np.clip((yy - off) / 1.5 + 0.5, 0, 1)
    thin = np.exp(-np.maximum(yy - off, 0) / 5.0)  # a torn edge is thinner, a touch lighter
    rgb = np.clip(rgb + (thin * 5.0)[..., None], 0, 255)
    img = Image.fromarray(np.dstack([np.uint8(rgb), np.uint8(alpha * 255)]), "RGBA")
    img.save(OUT, "WEBP", quality=92, method=6)
    print(f"{os.path.basename(OUT)}: {W}x{H} {os.path.getsize(OUT) // 1024} KB")


if __name__ == "__main__":
    main()
