"""v14 lane C: the orange branch and the four dogs as page-ready WebP layers.

Owner: Tomas. Date: 2026-11-11. Rollback: delete this file and assets/inbox/v14/.
Run: .venv/bin/python -I comps/art/v14_lane_c.py <citrus-clean.png>
  <citrus-clean.png>: citrus-branch.png turned 90 degrees anticlockwise (cut end top right,
  fruit below the branch), extract_asset.py --matting, then v14_citrus_clean.py.
Outputs in assets/inbox/v14/: citrus-branch.webp, dog-tan.webp, dog-collie.webp,
dog-golden.webp, dog-merle.webp, dog-merle-tail.webp, about 3x the largest display
(u capped at 4.4 px). Straight alpha is resized with an area filter and saved exact, so
the paper grain is not sharpened into noise and no dark fringe enters the edges.
"""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
DOGS = ROOT / "assets/inbox/dogs"
OUT = ROOT / "assets/inbox/v14"
OUT.mkdir(parents=True, exist_ok=True)


def bbox(im, pad=6):
    x0, y0, x1, y1 = im.getchannel("A").point(lambda v: 255 if v > 6 else 0).getbbox()
    return (max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad))


def save(im, size, name):
    a = cv2.resize(np.asarray(im), size, interpolation=cv2.INTER_AREA)
    if name.endswith("tail.webp"):
        # the tail layer is mostly clear: its hidden colour (the whole dog) is flattened to the
        # tail's mean away from its edge, so it costs 7 KB, not 50
        near = cv2.dilate((a[..., 3] > 0).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        a[~near, :3] = a[a[..., 3] > 128][:, :3].mean(0).astype(np.uint8)
    p = OUT / name
    Image.fromarray(a, "RGBA").save(p, "WEBP", quality=82, method=6, alpha_quality=90, exact=True)
    print(f"{name} {size[0]}x{size[1]} {p.stat().st_size // 1024} KB")


# the orange branch: 760 px wide (3.2x of its 54u display at 440 px)
cit = Image.open(sys.argv[1]).convert("RGBA")
cit = cit.crop(bbox(cit))
save(cit, (760, round(cit.height * 760 / cit.width)), "citrus-branch.webp")

# the dogs: 760 px tall (3x of a 31u-wide dog at 440 px); the merle 900, its speckled coat
# reads as grain to the gate below that; its tail on a layer of its own
for n in ("tan", "collie", "golden", "merle"):
    H = 900 if n == "merle" else 760
    im = Image.open(DOGS / f"dog-{n}-cut.webp").convert("RGBA")
    box = bbox(im)
    size = (round((box[2] - box[0]) * H / (box[3] - box[1])), H)
    if n != "merle":
        save(im.crop(box), size, f"dog-{n}.webp")
        continue
    # tail mask in the cut's own pixels: it leaves the hip at x ~765, y 930-1050, tip (870, 1190)
    m = Image.new("L", im.size, 0)
    tail_poly = [(772, 925), (im.width, 925), (im.width, 1235), (782, 1235)]
    tail_poly += [(792, 1062), (762, 1012), (764, 958)]
    ImageDraw.Draw(m).polygon(tail_poly, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(2))
    a = im.getchannel("A")
    zero = Image.new("L", im.size, 0)
    tail, body = im.copy(), im.copy()
    tail.putalpha(Image.composite(a, zero, m))
    body.putalpha(Image.composite(zero, a, m))
    save(body.crop(box), size, "dog-merle.webp")
    save(tail.crop(box), size, "dog-merle-tail.webp")
    ox = (767 - box[0]) / (box[2] - box[0]) * 100
    oy = (978 - box[1]) / (box[3] - box[1]) * 100
    print(f"tail origin {ox:.1f}% {oy:.1f}%")
