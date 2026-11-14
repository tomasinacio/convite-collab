#!/usr/bin/env python3
"""Bake the v9 opening layers: paper faces and a rendered wax seal (with its two cracked halves).

owner: Tomas | review date: 2026-11-17
canonical path: projects/wedding-invite/comps/art/v9_bake.py
rollback: rm -rf projects/wedding-invite/comps/art/v9 projects/wedding-invite/comps/art/v9_bake.py

Usage: .venv/bin/python comps/art/v9_bake.py
  writes the paper faces to comps/art/v9/ and the procedural seal to comps/art/v9/fallback/.
  The live seal in comps/art/v9/ comes from the photograph (comps/art/v9_seal_photo.py); to fall
  back, copy comps/art/v9/fallback/seal-*.webp over it (same names, same contract).

Why baked: comps/OPENING-ADVICE.md says no filters or blend modes on rotating faces, resting
shadows baked into images. The paper grain, deckled free edges and the stand-in art (deck crops
multiplied into the paper, as r8b did live) are therefore drawn here once.

The fallback seal here is a height-field render (lit wax, olive sprig in relief), not a
photograph. Deterministic (fixed seeds).

Seal asset contract (every seal, procedural or photographic, keeps it, same filenames):
  seal-whole.webp   600 x 600, the wax centred, baked resting shadow, alpha
  seal-top.webp     600 x 378, rows 0 to 378 of the cracked seal (0.63 of its height), alpha
  seal-bottom.webp  600 x 378, rows 222 to 600 of the cracked seal, alpha
  The crack stays within rows 228 to 372 (centre plus or minus 12%, room for a diagonal break).
  The page shows the box at --S (100 px) and the halves at --hh: .63 of --S.
  600 px is the quality gate's floor (small).
"""

import os

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "v9")
CROPS = os.path.join(HERE, "..", "deck-crops")
PAPER = np.array([246, 239, 223], np.float32)
W = 1200  # 3x of the 400 px sheet: sharp on a DPR 3 phone
K = W / 800  # every length below was tuned at 800 px wide


def blur(a, s):
    return cv2.GaussianBlur(a, (0, 0), s) if s > 0 else a


def unit_noise(rng, shape, s):
    n = blur(rng.standard_normal(shape).astype(np.float32), s)
    return n / (n.std() + 1e-6)


# ---------------------------------------------------------------- paper


def deckle_offsets(rng, n, base, amp):
    """Distance (px) the torn edge sits inside the box, along one edge of n pixels."""
    a = unit_noise(rng, (1, n + 200), 22)[0, 100:-100] * amp
    b = unit_noise(rng, (1, n + 40), 3)[0, 20:-20] * amp * 0.35
    return np.maximum(0.6, base + a + b)


def paper(h, seed, free=None, tone=0.0):
    """Cream cotton paper, h x W. free = 'top' or 'bottom' gets a deckled edge; sides a cut edge."""
    rng = np.random.default_rng(seed)
    rgb = np.broadcast_to(PAPER, (h, W, 3)).copy()
    lum = 1 + 0.011 * unit_noise(rng, (h, W), 46 * K) + 0.006 * unit_noise(rng, (h, W), 9 * K)
    rgb *= lum[..., None] * (1 + tone)
    fib = np.zeros((h, W), np.float32)
    for _ in range(int(h * W / (420 * K * K))):
        x, y = rng.uniform(-20, W + 20), rng.uniform(-20, h + 20)
        ang, ln = rng.uniform(0, np.pi), rng.uniform(6, 34) * K
        k = rng.integers(3, 6)
        pts = []
        for _step in range(k):
            ang += rng.normal(0, 0.35)
            pts.append((x, y))
            x += np.cos(ang) * ln / k
            y += np.sin(ang) * ln / k
        v = rng.choice([1.0, -0.6], p=[0.7, 0.3]) * rng.uniform(0.4, 1.0)
        cv2.polylines(fib, [np.int32(np.array(pts) * 4)], False, v, 1, cv2.LINE_AA, 2)
    rgb += blur(fib, 0.5)[..., None] * 3.2
    rgb += (unit_noise(rng, (h, W), 0.7) * 1.5)[..., None]
    # alpha: deckle on the free edge, a slightly uneven cut on the sides
    yy, xx = np.mgrid[0:h, 0:W].astype(np.float32)
    alpha = np.ones((h, W), np.float32)
    for side in ("left", "right"):
        off = deckle_offsets(rng, h, 0.9 * K, 0.25 * K)[:, None]
        d = xx if side == "left" else (W - 1 - xx)
        alpha *= np.clip(d - off + 0.5, 0, 1)
    if free:
        off = deckle_offsets(rng, W, 3.2 * K, 2.0 * K)[None, :]
        d = yy if free == "top" else (h - 1 - yy)
        alpha *= np.clip((d - off) / (1.5 * K) + 0.5, 0, 1)
        thin = np.exp(-np.maximum(d - off, 0) / (5.0 * K))  # torn edge is thinner, a touch lighter
        rgb += (thin * 4.0)[..., None]
    return rgb, alpha


def multiply_art(rgb, name, left, top, width, opacity, feather=False, rotate=0.0):
    im = Image.open(os.path.join(CROPS, name)).convert("RGB")
    hgt = width * im.height / im.width
    im = im.resize((round(width), round(hgt)), Image.LANCZOS)
    m = None
    if feather:  # CSS radial-gradient(closest-side, #000 58%, transparent 100%)
        yy, xx = np.mgrid[0 : im.height, 0 : im.width].astype(np.float32)
        r = np.hypot((xx - im.width / 2) / (im.width / 2), (yy - im.height / 2) / (im.height / 2))
        m = np.clip((1 - r) / 0.42, 0, 1)
    art = np.asarray(im, np.float32) / 255
    if m is None:  # soft rectangular edge so the crop's border never shows
        e = 16.0 * K
        yy, xx = np.mgrid[0 : im.height, 0 : im.width].astype(np.float32)
        dist = np.minimum.reduce([xx, yy, im.width - 1 - xx, im.height - 1 - yy])
        m = np.clip(dist / e, 0, 1) ** 1.5
    if rotate:
        cx, cy = left + width / 2, top + hgt / 2
        rim = Image.fromarray(np.uint8(np.dstack([art, m[..., None]]) * 255), "RGBA")
        rim = rim.rotate(-rotate, Image.BICUBIC, expand=True)  # CSS rotate is clockwise
        a = np.asarray(rim, np.float32) / 255
        art, m = a[..., :3], a[..., 3]
        left, top = cx - rim.width / 2, cy - rim.height / 2
    h, w = rgb.shape[:2]
    x0, y0 = int(round(left)), int(round(top))
    sx0, sy0 = max(0, -x0), max(0, -y0)
    x1, y1 = min(w, x0 + art.shape[1]), min(h, y0 + art.shape[0])
    if x1 <= max(x0, 0) or y1 <= max(y0, 0):
        return
    a = art[sy0 : sy0 + y1 - max(y0, 0), sx0 : sx0 + x1 - max(x0, 0)]
    mm = m[sy0 : sy0 + a.shape[0], sx0 : sx0 + a.shape[1]][..., None] * opacity
    reg = rgb[max(y0, 0) : y1, max(x0, 0) : x1]
    reg *= 1 - mm + mm * a


def save(rgb, alpha, name, q=86, out=OUT):
    a = np.uint8(np.clip(alpha, 0, 1) * 255)
    im = np.dstack([np.uint8(np.clip(rgb, 0, 255)), a])
    mode = "RGBA" if a.min() < 255 else None
    img = Image.fromarray(im if mode else im[..., :3], mode or "RGB")
    path = os.path.join(out, name)
    img.save(path, "WEBP", quality=q, method=6)
    print(f"{name}: {img.width}x{img.height} {os.path.getsize(path) // 1024} KB")


def faces():
    # a tall sheet (red-team round 2): Hm 1.4 W, Ht .42 W; the two fold edges meet at the seal,
    # so Hb = Hm - Ht. The page clamps Ht between 120 and 168 px, so a face may stretch a little.
    ht, hm = round(0.42 * W), round(1.4 * W)
    hb = hm - ht
    rgb, al = paper(ht, 11, "top")
    multiply_art(rgb, "clouds.jpg", 80 * K, ht / 2 - 124.8 * K, 640 * K, 1.0)
    multiply_art(rgb, "branch.jpg", -24 * K, -0.16 * ht, 120 * K, 1.0, rotate=-148)
    multiply_art(rgb, "swallows.jpg", W - 208 * K, 0.46 * ht, 168 * K, 1.0)
    save(rgb, al, "fold-top-in.webp")
    rgb, _ = paper(ht, 12, None, -0.006)
    save(rgb, al[::-1], "fold-top-out.webp")  # the back of the same sheet: same torn edge
    rgb, al = paper(hm, 13)
    save(rgb, al, "sheet-mid.webp")
    rgb, al = paper(hb, 14, "bottom")
    multiply_art(rgb, "hills.jpg", 16 * K, 0.1 * hb, 768 * K, 0.82, feather=True)
    tw = 304 * K
    multiply_art(rgb, "tree.jpg", W - tw, hb - 0.06 * hb - tw * 172 / 222, tw, 0.82, True)
    save(rgb, al, "fold-bottom-in.webp")
    rgb, _ = paper(hb, 15, None, -0.006)
    save(rgb, al[::-1], "fold-bottom-out.webp")


# ---------------------------------------------------------------- seal


def leaf(mask, rib, x, y, ang, ln, wd):
    t = np.linspace(0, 1, 40)
    bend = 0.08 * ln * np.sin(np.pi * t)
    half = wd / 2 * np.sin(np.pi * t) ** 0.75 * (1 - 0.25 * t)
    ux, uy = np.cos(ang), np.sin(ang)
    px, py = -uy, ux
    cx, cy = x + ux * ln * t + px * bend, y + uy * ln * t + py * bend
    poly = np.concatenate(
        [
            np.stack([cx + px * half, cy + py * half], 1),
            np.stack([cx - px * half, cy - py * half], 1)[::-1],
        ]
    )
    cv2.fillPoly(mask, [np.int32(poly * 4)], 1.0, cv2.LINE_AA, 2)
    cv2.polylines(rib, [np.int32(np.stack([cx, cy], 1)[4:-6] * 4)], False, 1.0, 3, cv2.LINE_AA, 2)


def sprig(n, c, size):
    """An olive sprig in the stamp: a curved stem, five leaf pairs, two olives."""
    mask, rib = np.zeros((n, n), np.float32), np.zeros((n, n), np.float32)
    t = np.linspace(0, 1, 60)
    p0, p1, p2 = np.array([-0.55, 0.5]), np.array([0.0, 0.18]), np.array([0.5, -0.55])
    stem = ((1 - t) ** 2)[:, None] * p0 + (2 * (1 - t) * t)[:, None] * p1 + (t**2)[:, None] * p2
    stem = c + stem * size
    cv2.polylines(mask, [np.int32(stem * 4)], False, 1.0, int(4 * size * 0.022), cv2.LINE_AA, 2)
    for i, s in enumerate([0.14, 0.34, 0.54, 0.74]):
        k = int(s * 59)
        x, y = stem[k]
        dx, dy = stem[min(k + 1, 59)] - stem[k]
        a = np.arctan2(dy, dx)
        ln = size * (0.56 - 0.07 * i)
        wd = ln * 0.3
        side = 1 if i % 2 == 0 else -1
        leaf(mask, rib, x, y, a - side * 0.75, ln, wd)
        leaf(mask, rib, x, y, a + side * 0.62, ln * 0.85, wd * 0.95)
    leaf(mask, rib, *stem[-1], np.arctan2(*(stem[-1] - stem[-3])[::-1]), size * 0.3, size * 0.075)
    for ox, oy, r in ((-0.16, 0.4, 0.085), (0.12, 0.3, 0.078)):
        cv2.ellipse(
            mask,
            (int((c[0] + ox * size) * 4), int((c[1] + oy * size) * 4)),
            (int(r * size * 4), int(r * size * 5.2)),
            20,
            0,
            360,
            1.0,
            -1,
            cv2.LINE_AA,
            2,
        )
    return mask, rib


def seal():
    rng = np.random.default_rng(5)
    n = 1200  # rendered at 2x of the 600 px asset, then reduced
    c = n / 2
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    dx, dy = xx - c, yy - c
    rho, th = np.hypot(dx, dy), np.arctan2(dy, dx)
    r0 = 0.385 * n
    edge = np.ones_like(th)
    for k in range(2, 8):
        edge += rng.uniform(0.004, 0.012) / k**0.4 * np.cos(k * th + rng.uniform(0, 6.3))
    for ang, wid, amp in (
        (0.5, 0.16, 0.05),
        (2.3, 0.22, 0.035),
        (3.9, 0.12, 0.06),
        (5.3, 0.2, 0.03),
    ):
        dd = np.angle(np.exp(1j * (th - ang)))
        edge += amp * np.exp(-((dd / wid) ** 2))
    d = r0 * edge - rho  # inside distance, px
    h = np.tanh(np.maximum(d, 0) / (0.045 * n))
    # the stamp: pressed disc, squeezed ridge, a fine bead ring
    sx, sy = c + 6, c - 4
    rs = 0.6 * r0
    rr = np.hypot(xx - sx, yy - sy)
    h -= 0.42 * 0.5 * (1 + np.tanh((rs - rr) / 5.2))
    h += 0.2 * np.exp(-(((rr - rs - 16) / 15) ** 2)) * np.clip(d / 40, 0, 1)
    h += 0.05 * np.exp(-(((rr - 0.88 * rs) / 3.2) ** 2))
    m, rib = sprig(n, np.array([sx, sy]), rs * 0.92)
    dt = cv2.distanceTransform(np.uint8(m > 0.5), cv2.DIST_L2, 5)
    h += 0.17 * blur(np.clip(dt / 7, 0, 1) ** 0.6 * (m > 0.5), 1.4) * (rr < rs)
    h -= 0.035 * blur(rib, 1.0) * (rr < rs)
    # wax surface: slow undulation, fine roughness, a few tiny bubbles
    h += 0.025 * unit_noise(rng, (n, n), 38) * np.clip(d / 30, 0, 1)
    h += 0.0011 * unit_noise(rng, (n, n), 1.6)
    pits = np.zeros((n, n), np.float32)
    for _ in range(55):
        a, r = rng.uniform(0, 6.3), r0 * np.sqrt(rng.uniform(0, 0.9))
        cv2.circle(
            pits, (int(c + r * np.cos(a)), int(c + r * np.sin(a))), int(rng.uniform(2, 6)), 1.0, -1
        )
    h -= 0.012 * blur(pits, 1.6)
    # light from the upper left, satin wax
    k = 62.0
    gy, gx = np.gradient(h)
    nx, ny, nz = -k * gx, -k * gy, np.ones_like(h)
    ln = np.sqrt(nx**2 + ny**2 + nz**2)
    nx, ny, nz = nx / ln, ny / ln, nz / ln
    lv = np.array([-0.45, -0.55, 0.7])
    lv /= np.linalg.norm(lv)
    hv = lv + np.array([0, 0, 1.0])
    hv /= np.linalg.norm(hv)
    ndl = nx * lv[0] + ny * lv[1] + nz * lv[2]
    ndh = np.clip(nx * hv[0] + ny * hv[1] + nz * hv[2], 0, 1)
    wrap = np.clip((ndl + 0.35) / 1.35, 0, 1)
    ao = np.clip(1 - 2.4 * (blur(h, 12) - h), 0.55, 1.0)
    # #9A4C32 (red-team 2026-11-11, finding 3): a quieter terracotta, satin not gloss
    base = np.array([154, 76, 50], np.float32)
    thin = np.array([184, 104, 74], np.float32)
    tmix = np.exp(-np.maximum(d, 0) / 26)[..., None]
    alb = base * (1 - tmix) + thin * tmix
    alb *= (1 + 0.04 * unit_noise(rng, (n, n), 18))[..., None]
    alb *= np.where(rr < rs - 2, 0.95, 1.0)[..., None]
    shade = (0.48 + 0.6 * wrap) * ao
    spec = 0.3 * ndh**110 + 0.06 * ndh**16
    col = alb * shade[..., None] + (spec * 255)[..., None] * np.array([1.0, 0.96, 0.9])
    a = np.clip(d / 2.0 + 0.5, 0, 1)

    # baked resting shadow: soft and contact
    def shifted(img, ox, oy):
        mtx = np.float32([[1, 0, ox], [0, 1, oy]])
        return cv2.warpAffine(img, mtx, (n, n))

    s1 = shifted(blur(a, 16), 10, 16) * 0.3
    s2 = shifted(blur(a, 3.5), 2, 5) * 0.42
    sa = 1 - (1 - s1) * (1 - s2)
    oa = a + sa * (1 - a)
    shadow_col = np.array([88, 52, 36], np.float32)
    rgb = (col * a[..., None] + shadow_col * (sa * (1 - a))[..., None]) / np.maximum(oa, 1e-4)[
        ..., None
    ]
    return rgb, oa, a, r0


def reduce(rgb, alpha, w, h):
    """Area-reduce on premultiplied colour, so cut edges stay clean."""
    pm = cv2.resize(
        np.dstack([rgb * alpha[..., None], alpha]), (w, h), interpolation=cv2.INTER_AREA
    )
    return pm[..., :3] / np.maximum(pm[..., 3], 1e-4)[..., None], pm[..., 3]


def crack(rgb, alpha, wax, r0):
    """Two halves along an angular, uneven fracture through the centre (red-team finding 2).

    The fracture runs in straight stretches between six kinks that wander up to 3.5% of the asset
    above and below the centre line, with fine grit on top. Each half gets a dark matte lip (the
    broken face, seen nearly edge on). Under the upper half, the lower half also carries the dark
    inside of the crack, 2 px of the page deep: when the halves part by 1 px the gap shows shadowed
    wax, never the paper. A faint hairline runs off the crack into the lower half.
    """
    n = alpha.shape[0]
    c = n / 2
    rng = np.random.default_rng(31)
    kx = c + (np.linspace(-1.0, 1.0, 6) + rng.uniform(-0.1, 0.1, 6)) * r0
    sign = np.where(np.arange(6) % 2 == 0, 1.0, -1.0) * rng.choice([1, -1])
    sign[rng.integers(1, 5)] *= -1  # break the zigzag once
    ky = sign * rng.uniform(0.35, 1.0, 6) * 0.03 * n
    kx = np.concatenate([[0], kx, [n - 1]])
    ky = np.concatenate([[ky[0]], ky, [ky[-1]]])
    xs = np.arange(n, dtype=np.float32)
    line = np.interp(xs, kx, ky).astype(np.float32)
    line += unit_noise(rng, (1, n), 10)[0] * 3.0 + unit_noise(rng, (1, n), 1.6)[0] * 1.3
    line = np.clip(line, -0.04 * n, 0.04 * n) + c
    yy = np.mgrid[0:n, 0:n][0].astype(np.float32)
    dist = yy - line[None, :]  # > 0 below the crack
    up = np.clip(0.5 - dist / 1.5, 0, 1)
    e = np.abs(dist)
    # hairline: from the kink nearest the right of centre, down into the lower half
    hair = np.zeros((n, n), np.float32)
    k = int(np.argmin(np.abs(kx - (c + 0.35 * r0))))
    x0, y0 = kx[k], line[int(kx[k])]
    pts = [(x0, y0)]
    ang = np.deg2rad(58)
    for _ in range(5):
        ang += rng.normal(0, 0.4)
        x0, y0 = x0 + np.cos(ang) * 0.05 * r0, y0 + np.sin(ang) * 0.05 * r0
        pts.append((x0, y0))
    cv2.polylines(hair, [np.int32(np.array(pts) * 4)], False, 1.0, 6, cv2.LINE_AA, 2)
    hair = blur(hair, 1.0) * np.clip((yy - line[None, :]) / 6, 0, 1)
    dark = np.array([74, 36, 24], np.float32)  # the shadowed inside of the break
    hh = int(round(0.63 * n))
    # upper half: its own wax above the crack, a dark lip along the break
    lip = np.exp(-((e / 14) ** 1.6)) * 0.42 * wax
    top = rgb * (1 - lip[..., None])
    a_top = alpha * up
    # lower half: its wax below the crack, a lighter lip, the hairline, and the dark inside above
    lip = np.exp(-((e / 9) ** 1.6)) * 0.3 * wax
    bot = rgb * (1 - lip[..., None]) * (1 - 0.3 * hair * wax)[..., None]
    inside = wax * np.clip((dist + 26) / 2, 0, 1) * up  # 26 px at 4x = 2 page px
    bot = bot * (1 - up[..., None]) + dark * up[..., None]
    a_bot = np.maximum(alpha * (1 - up), inside)
    return [
        (top[:hh], a_top[:hh], "seal-top.webp"),
        (bot[n - hh :], a_bot[n - hh :], "seal-bottom.webp"),
    ]


def main():
    fallback = os.path.join(OUT, "fallback")
    os.makedirs(fallback, exist_ok=True)
    faces()
    rgb, alpha, wax, r0 = seal()
    # the asset contract a photographic seal must keep (see the module docstring)
    side = 600
    hh = round(0.63 * side)
    rgb_s, al_s = reduce(rgb, alpha, side, side)
    save(rgb_s, al_s, "seal-whole.webp", 90, fallback)
    for col, al, name in crack(rgb, alpha, wax, r0):
        c2, a2 = reduce(col, al, side, hh)
        save(c2, a2, name, 90, fallback)


if __name__ == "__main__":
    main()
