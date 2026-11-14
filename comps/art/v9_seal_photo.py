#!/usr/bin/env python3
"""Bake the v9 seal from the user's photographic wax seal: whole seal plus two cracked halves.

owner: Tomas | review date: 2026-11-18
canonical path: projects/wedding-invite/comps/art/v9_seal_photo.py
rollback: rm projects/wedding-invite/comps/art/v9_seal_photo.py, then copy
  comps/art/v9/fallback/seal-*.webp over comps/art/v9/ (the procedural seal from v9_bake.py)

Usage: .venv/bin/python -I comps/art/v9_seal_photo.py
  reads  assets/inbox/seal-v9/seal-cut-ref.webp (matted cut-out of copilot-seal-ref.png)
  writes comps/art/v9/seal-whole.webp, seal-top.webp, seal-bottom.webp

Keeps the asset contract in v9_bake.py: whole 600 x 600 centred with a baked soft resting shadow
to the lower right (the photo is lit from the upper left); halves 600 x 378 cut along a
diagonal, irregular crack within rows 228 to 372. The photo's gloss and sprig are kept: the edge is
cleaned (stray paper fibres at the upper right rim), the wax is nudged toward #9A4C32 in the mid
tones only, so highlights stay photographic. Deterministic (fixed seeds).
"""

import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v9_bake import OUT, blur, reduce, save, unit_noise  # noqa: E402

SRC = os.path.join(HERE, "..", "..", "assets", "inbox", "seal-v9", "seal-cut-ref.webp")
N = 1200  # work at 2x of the 600 px asset
WAX_D = 0.785 * N  # wax diameter in the box, as the procedural seal (about 80 px at --S 100 px)
TARGET = np.array([154, 76, 50], np.float32)  # #9A4C32
GRADE = 0.65  # how far the mid tones move toward TARGET


def clean_cutout(path):
    """Cut-out to (rgb, alpha): smooth wax edge, fibres and halo removed, fringe recoloured."""
    im = np.asarray(Image.open(path).convert("RGBA"), np.float32)
    rgb, a0 = im[..., :3], im[..., 3] / 255
    hard = np.uint8(a0 > 0.5)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    hard = cv2.morphologyEx(hard, cv2.MORPH_OPEN, k)  # fibres are thinner than 9 px
    hard = cv2.morphologyEx(hard, cv2.MORPH_CLOSE, k)
    _, lab, stats, _ = cv2.connectedComponentsWithStats(hard)
    hard = np.uint8(lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    ff = hard.copy()
    cv2.floodFill(ff, None, (0, 0), 2)
    hard[ff == 0] = 1  # fill holes
    hard = cv2.erode(hard, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))  # lose the fringe
    soft = blur(hard.astype(np.float32), 1.6)
    alpha = np.clip((soft - 0.5) * 2.2 + 0.5, 0, 1)
    # fringe pixels (partly matted in the source) take the colour of the wax just inside
    core = (a0 > 0.97).astype(np.float32) * cv2.erode(hard, k).astype(np.float32)
    fill = blur(rgb * core[..., None], 4) / np.maximum(blur(core, 4), 1e-4)[..., None]
    w = np.clip((a0 - 0.6) / 0.37, 0, 1)
    rgb = rgb * w[..., None] + fill * (1 - w[..., None])
    return rgb, alpha


def grade(rgb, alpha):
    """Move the mid tones toward TARGET; highlights and deep shadows keep the photograph."""
    lum = rgb.mean(-1)
    sel = alpha > 0.99
    med = np.median(rgb[sel & (lum > 50) & (lum < 140)], 0)
    gain = (TARGET / med) ** GRADE
    w = np.clip((190 - lum) / 70, 0, 1) * np.clip((lum - 20) / 30, 0, 1)
    return rgb * (1 + (gain - 1) * w[..., None]), med, gain


def place(rgb, alpha):
    """Scale the wax to WAX_D and centre its bounding box in an N x N box."""
    ys, xs = np.nonzero(alpha > 0.5)
    d = max(xs.max() - xs.min(), ys.max() - ys.min())
    s = WAX_D / d
    cx, cy = (xs.max() + xs.min()) / 2, (ys.max() + ys.min()) / 2
    mtx = np.float32([[s, 0, N / 2 - s * cx], [0, s, N / 2 - s * cy]])
    pm = np.dstack([rgb * alpha[..., None], alpha])
    pm = cv2.warpAffine(pm, mtx, (N, N), flags=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    a = np.clip(pm[..., 3], 0, 1)
    return pm[..., :3] / np.maximum(a, 1e-4)[..., None], a


def with_shadow(col, a):
    """Baked resting shadow, soft and contact, to the lower right (as the procedural seal)."""

    def shifted(img, ox, oy):
        return cv2.warpAffine(img, np.float32([[1, 0, ox], [0, 1, oy]]), (N, N))

    s1 = shifted(blur(a, 16), 10, 18) * 0.32
    s2 = shifted(blur(a, 3.5), 2, 5) * 0.45
    sa = 1 - (1 - s1) * (1 - s2)
    oa = a + sa * (1 - a)
    shadow_col = np.array([88, 52, 36], np.float32)
    rgb = (col * a[..., None] + shadow_col * (sa * (1 - a))[..., None]) / np.maximum(oa, 1e-4)[
        ..., None
    ]
    return rgb, oa


def chip_mask(rng, n, line, x0, side, width, depth):
    """A small broken-off flake at the crack: an irregular polygon on one side of the line."""
    m = np.zeros((n, n), np.float32)
    xs = np.linspace(x0 - width / 2, x0 + width / 2, 7)
    prof = np.sin(np.linspace(0, np.pi, 7)) ** 0.7 * depth * rng.uniform(0.6, 1.0, 7)
    prof[0] = prof[-1] = 0
    ys = np.array([line[int(np.clip(x, 0, n - 1))] for x in xs]) - side * prof
    back = np.array([line[int(np.clip(x, 0, n - 1))] for x in xs[::-1]]) + side * 3
    poly = np.concatenate([np.stack([xs, ys], 1), np.stack([xs[::-1], back], 1)])
    cv2.fillPoly(m, [np.int32(poly * 4)], 1.0, cv2.LINE_AA, 2)
    return blur(m, 0.8)


def crack(rgb, alpha, wax, wax_col):
    """Split along a diagonal, off-centre break with two chips and a matte, wax-coloured lip.

    The break falls about 10 degrees from upper left to lower right and passes a little below the
    centre, in straight stretches between kinks, with grit. Along each broken edge a band of matte
    wax (no gloss) shows the fracture face: darker on the upper half, whose face looks away from
    the light, lighter on the lower half. Two flakes have broken off at the edge, one on each half,
    showing deeper, shadowed wax. Under the upper half, the lower half carries 2 px of shadowed
    wax, so a 1 px part shows the inside of the break, never the paper.
    """
    n = alpha.shape[0]
    c = n / 2
    rng = np.random.default_rng(53)
    r0 = WAX_D / 2
    xs = np.arange(n, dtype=np.float32)
    base = c + 0.012 * n + (xs - c) * (0.07 * n / r0)
    kx = c + (np.linspace(-1.0, 1.0, 6) + rng.uniform(-0.1, 0.1, 6)) * r0
    sign = np.where(np.arange(6) % 2 == 0, 1.0, -1.0) * rng.choice([1, -1])
    ky = sign * rng.uniform(0.3, 1.0, 6) * 0.02 * n
    kx = np.concatenate([[0], kx, [n - 1]])
    ky = np.concatenate([[ky[0]], ky, [ky[-1]]])
    line = base + np.interp(xs, kx, ky).astype(np.float32)
    line += unit_noise(rng, (1, n), 10)[0] * 3.0 + unit_noise(rng, (1, n), 1.6)[0] * 1.4
    line = np.clip(line, c - 0.115 * n, c + 0.115 * n)
    yy = np.mgrid[0:n, 0:n][0].astype(np.float32)
    dist = yy - line[None, :]  # > 0 below the break
    up = np.clip(0.5 - dist / 1.5, 0, 1)
    # lip widths along x (hi-res px; 12 px = 1 page px)
    w_up = (9 + unit_noise(rng, (1, n), 3)[0] * 2.5)[None, :]
    w_lo = (7 + unit_noise(rng, (1, n), 3)[0] * 2.0)[None, :]
    w_up, w_lo = np.maximum(w_up, 3), np.maximum(w_lo, 3)
    grit = 1 + 0.09 * unit_noise(rng, (n, n), 1.1)
    face = wax_col[None, None, :] * grit[..., None]
    band_up = np.clip((w_up + dist) / 2 + 0.5, 0, 1) * up * wax
    band_lo = np.clip((w_lo - dist) / 2 + 0.5, 0, 1) * (1 - up) * wax
    edge = np.exp(-((np.abs(dist) / 2.6) ** 2)) * wax  # the shadow right in the crack
    chip_up = chip_mask(rng, n, line, c - 0.42 * r0, 1, 70, 40) * up * wax
    chip_lo = chip_mask(rng, n, line, c + 0.5 * r0, -1, 56, 34) * (1 - up) * wax
    rim = []
    for m in (chip_up, chip_lo):  # each flake's broken outline reads as a fine dark line
        hard = np.uint8(m > 0.5)
        rim.append(blur((hard - cv2.erode(hard, np.ones((5, 5), np.uint8))).astype(np.float32), 1))
    top = rgb * (1 - band_up[..., None]) + face * 0.78 * band_up[..., None]
    top = top * (1 - chip_up[..., None]) + face * 0.6 * chip_up[..., None]
    top *= (1 - 0.45 * edge - 0.35 * rim[0] * up)[..., None]
    bot = rgb * (1 - band_lo[..., None]) + face * 1.06 * band_lo[..., None]
    bot = bot * (1 - chip_lo[..., None]) + face * 0.72 * chip_lo[..., None]
    bot *= (1 - 0.35 * edge - 0.3 * rim[1] * (1 - up))[..., None]
    inside = wax * np.clip((dist + 24) / 2, 0, 1) * up  # 24 px at 2x = 2 page px
    dark = wax_col * 0.5
    bot = bot * (1 - up[..., None]) + dark * up[..., None]
    a_top = alpha * up
    a_bot = np.maximum(alpha * (1 - up), inside)
    hh = int(round(0.63 * n))
    return [
        (top[:hh], a_top[:hh], "seal-top.webp"),
        (bot[n - hh :], a_bot[n - hh :], "seal-bottom.webp"),
    ]


def main():
    rgb, alpha = clean_cutout(SRC)
    rgb, med, gain = grade(rgb, alpha)
    print(f"wax mid tone {med.round()} -> gain {gain.round(3)}")
    col, wax = place(rgb, alpha)
    full, oa = with_shadow(col, wax)
    side = 600
    hh = round(0.63 * side)
    rgb_s, al_s = reduce(full, oa, side, side)
    save(rgb_s, al_s, "seal-whole.webp", 90, OUT)
    lip_col = np.clip(med * gain, 0, 255).astype(np.float32) * 0.92
    for c, a, name in crack(full, oa, wax, lip_col):
        c2, a2 = reduce(c, a, side, hh)
        save(c2, a2, name, 90, OUT)


if __name__ == "__main__":
    main()
