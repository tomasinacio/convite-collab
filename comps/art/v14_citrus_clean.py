"""v14 lane C: clear the paper the matting kept between the oranges and the branch.

Owner: Tomas. Date: 2026-11-11. Rollback: delete this file.
Run: .venv/bin/python -I comps/art/v14_citrus_clean.py <citrus-cut.png> <citrus-clean.png>
Inside small polygons (found by eye on a grid, in the turned cut's pixels), light unsaturated
pixels lose their alpha in proportion to how paper-like they are, so the fruit rims stay soft.
"""

import sys

import numpy as np
from PIL import Image, ImageDraw

REGIONS = [  # polygon, saturation limit
    ([(288, 708), (318, 708), (318, 778), (288, 778)], 50),  # wedge: lower-left orange and its leaf
    ([(322, 680), (348, 680), (348, 712), (322, 712)], 50),  # its stalk and its top
    ([(648, 476), (670, 476), (646, 544), (618, 544)], 40),  # wedge: middle orange and the branch
    ([(510, 600), (530, 600), (530, 655), (510, 655)], 70),  # sliver right of the lower-left orange
    ([(438, 618), (462, 618), (462, 640), (438, 640)], 50),  # bit under the lower blossom's petal
]

src = np.asarray(Image.open(sys.argv[1]).convert("RGBA")).astype(np.float32)
rgb, alpha = src[..., :3], src[..., 3].copy()
lum = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
sat = rgb.max(-1) - rgb.min(-1)
for poly, smax in REGIONS:
    m = Image.new("L", (src.shape[1], src.shape[0]), 0)
    ImageDraw.Draw(m).polygon(poly, fill=1)
    m = np.asarray(m).astype(bool)
    paperlike = np.clip((lum - 140) / 60, 0, 1) * np.clip((smax - sat) / 30, 0, 1)
    alpha[m] *= 1 - paperlike[m]
# a translucent grey smear left of the lower blossom: every half-clear, unsaturated pixel goes
sm = np.zeros(alpha.shape, bool)
sm[678:704, 258:300] = True
alpha[sm & (alpha < 200) & (sat < 45)] = 0
out = src.copy()
out[..., 3] = alpha
Image.fromarray(out.round().astype(np.uint8), "RGBA").save(sys.argv[2])
