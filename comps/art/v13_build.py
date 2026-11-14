#!/usr/bin/env python3
"""Build prototype.v13: prepare any new art that has arrived, then inline everything into one file.

owner: Tomas | review date: 2026-11-18
canonical path: projects/wedding-invite/comps/art/v13_build.py
rollback: rm projects/wedding-invite/comps/art/v13_build.py

Usage: .venv/bin/python -I comps/art/v13_build.py [--inbox DIR]
  DIR defaults to assets/inbox/new-art/. For each of cloud-long, cloud-round, meadow-strip and
  bindweed found there (.png or .jpg), the background is cut away and comps/art/v13/<name>.webp
  is written.
  The page then gets data-art="<names>" so its CSS swaps the fallbacks (sky-b cloud veils, no strip,
  no bindweed) for the new art. DATA?:<path> placeholders become `none` when the file is absent.

Keying: the clouds are painted on a flat mid blue-grey, so alpha comes from the distance to that
colour and the colour is un-mixed from it (soft cloud edges stay soft); the strip and the bindweed
are on off-white, keyed like the citrus plates (v12_bake.key_out). Every new file still needs a
row in assets/LOG.md and a look by eye.
"""

import os
import re
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v10_build import inline  # noqa: E402
from v12_bake import key_out  # noqa: E402

COMPS = os.path.join(HERE, "..")
ROOT = os.path.join(COMPS, "..")
OUT = os.path.join(HERE, "v13")
# name: (long side in px, about 2x its largest display, how it is cut)
#   cloud: keyed against its flat blue-grey ground; paper: keyed against the off-white paper;
#   matte: the extract_asset.py --matting cut-out, assets/cutouts/<name>-cut.webp (else paper)
NEW = {
    "cloud-long": (440, "cloud"),
    "cloud-round": (500, "cloud"),
    "meadow-strip": (400, "paper-unmix"),  # matting kept only a 607 x 168 fragment of the strip
    "bindweed": (450, "matte"),
    "lavender": (400, "matte"),
    "swallow-below": (200, "matte"),
    "olive-twig-trailing": (360, "matte"),
    "olive-leaf": (120, "leaf"),  # one leaf of olive-leaves-loose, cut out on its own
}
SOURCE = {"olive-leaf": "olive-leaves-loose"}
CUTOUTS = os.path.join(ROOT, "assets", "cutouts")


def key_cloud(rgb, lo=10, span=70):
    """Alpha from the distance to the flat ground colour; colour un-mixed from it (no pale film)."""
    rgb = rgb.astype(np.float32)
    border = np.concatenate(
        [rgb[:8].reshape(-1, 3), rgb[-8:].reshape(-1, 3), rgb[:, :8].reshape(-1, 3)]
    )
    bg = np.median(border, 0)
    d = np.sqrt(((rgb - bg) ** 2).sum(-1))
    a = np.clip((d - lo) / span, 0, 1)
    col = (rgb - (1 - a[..., None]) * bg) / np.maximum(a, 0.05)[..., None]
    return np.dstack([np.clip(col, 0, 255), a * 255]).astype(np.uint8)


def first_leaf(img):
    """The top-most of the separate leaves in a cut-out (each leaf is its own opaque island)."""
    a = np.asarray(img)[..., 3]
    n, lab, st, _ = cv2.connectedComponentsWithStats(np.uint8(a > 40))
    big = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 2000]
    i = min(big, key=lambda j: (st[j, cv2.CC_STAT_TOP], st[j, cv2.CC_STAT_LEFT]))
    keep = cv2.dilate(np.uint8(lab == i), np.ones((5, 5), np.uint8)).astype(bool)
    arr = np.asarray(img).copy()
    arr[~keep, 3] = 0
    return Image.fromarray(arr)


def prepare(inbox):
    present = []
    os.makedirs(OUT, exist_ok=True)
    for name, (long_side, kind) in NEW.items():
        base = SOURCE.get(name, name)
        found = [os.path.join(inbox, base + e) for e in (".png", ".jpg", ".jpeg", ".webp")]
        found = [f for f in found if os.path.exists(f)]
        if not found:
            continue
        rgb = np.asarray(Image.open(found[0]).convert("RGB"))
        matte = os.path.join(CUTOUTS, base + "-cut.webp")
        if kind == "leaf" and os.path.exists(matte):
            img = first_leaf(Image.open(matte).convert("RGBA"))
        elif kind == "matte" and os.path.exists(matte):
            img = Image.open(matte).convert("RGBA")
        elif kind == "cloud":
            img = Image.fromarray(key_cloud(rgb), "RGBA")
        elif kind == "paper-unmix":
            img = Image.fromarray(key_cloud(rgb, lo=22, span=40), "RGBA")
        else:
            img = Image.fromarray(key_out(np.ascontiguousarray(rgb), lo=8, hi=30), "RGBA")
        a = np.asarray(img.getchannel("A"))
        ys, xs = np.nonzero(a > 6)
        img = img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        s = long_side / max(img.size)
        img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
        out = os.path.join(OUT, name + ".webp")
        img.save(
            out, "WEBP", quality=70 if name == "meadow-strip" else 82, method=6
        )  # strip: weight
        print(f"new art: {name} {img.width}x{img.height} {os.path.getsize(out) // 1024} KB")
        present.append(name)
    return present


def main():
    args = sys.argv[1:]
    inbox = (
        args[args.index("--inbox") + 1]
        if "--inbox" in args
        else os.path.join(ROOT, "assets", "inbox", "new-art")
    )
    src = os.path.join(COMPS, "prototype.v13.src.html")
    out = os.path.join(COMPS, "prototype.v13.single.html")
    present = prepare(inbox)
    text = open(src, encoding="utf-8").read()
    text = text.replace("DATA-ART-FLAGS", " ".join(present))

    def optional(m):
        path = os.path.join(COMPS, m.group(1))
        name = os.path.splitext(os.path.basename(path))[0]
        return f'url("DATA:{m.group(1)}")' if name in present and os.path.exists(path) else "none"

    text = re.sub(r'url\("DATA\?:([^"]+)"\)', optional, text)
    text, used = inline(text)
    if re.search(r'url\("?DATA', text):
        sys.exit("unresolved placeholder")
    open(out, "w", encoding="utf-8").write(text)
    got = present or "none yet"
    print(f"prototype.v13.single.html: {len(text) // 1024} KB, {len(used)} images, new art: {got}")


if __name__ == "__main__":
    main()
