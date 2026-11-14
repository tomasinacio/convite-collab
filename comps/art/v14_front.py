#!/usr/bin/env python3
"""Bake the v14 closed front page (lane A, V14-BRIEF task 11): seal, papers, twine, linen.

owner: Tomas | review date: 2026-11-18
canonical path: projects/wedding-invite/comps/art/v14_front.py
rollback: rm -rf projects/wedding-invite/comps/art/v14_front.py \
  projects/wedding-invite/comps/art/v14

Usage: .venv/bin/python -I comps/art/v14_front.py
  reads  assets/inbox/seal-v9/seal-cut-ref.webp (the user's Copilot seal, matted)
         comps/art/v10/src/00-img-paper.webp      (P2 paper tile, the sheet's own paper)
         assets/cutouts/olive-twig-trailing-cut.webp (the user's Copilot olive twig, matted)
  writes comps/art/v14/front/*.webp (sizes below; every one at least 3x its largest CSS box)

  seal-whole 768 x 768, seal-top / seal-bottom 768 x 484: the v9 contract (wax 78.5 % of the box,
    centred, crack within rows .38 to .62, halves .63 of the box), so the opening is unchanged.
  closed-top 1290 x 1100 and closed-bottom 1290 x 1860: the two outer flap faces of a full-bleed
    closed sheet (seam 37 % down the screen), drawn with background-size: cover, one light from
    the upper left across both, the top flap's deckled edge on the seam.
  closed-emboss 860 x 1000: a blind-embossed olive twig, an overlay for the bottom flap's corner.
  closed-deco 1300 x 648: two 2-ply jute strands edge to edge, knotted under the seal (nothing
    loose shows), a whole pressed olive sprig tucked into the knot, the strands over its stem,
    baked soft shadows (closed-deco-nosprig without the sprig).
  linen 768 x 768: seamless plain-weave flax linen, 256 CSS px per tile (3x).
Deterministic (fixed seeds).
"""

import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
sys.path.insert(0, HERE)
import v9_seal_photo as vs  # noqa: E402
from v9_bake import blur, reduce, save, unit_noise  # noqa: E402

OUT = os.path.join(HERE, "v14", "front")
SEAL_SRC = os.path.join(ROOT, "assets", "inbox", "seal-v9", "seal-cut-ref.webp")
PAPER_TILE = os.path.join(HERE, "v10", "src", "00-img-paper.webp")
TWIG = os.path.join(ROOT, "assets", "cutouts", "olive-twig-trailing-cut.webp")
W = 1290  # flap width in px: 3x of a 430 px full-bleed sheet
PH = round(2.17 * W)  # packet height for the light: one phone screen (iPhone 15, 393 x 852)
SEAM = round(0.37 * PH)  # the twine band and seam sit 37 % down the screen
SHADOW = np.array([70, 46, 30], np.float32)  # warm umber, one light from the upper left


def shifted(img, ox, oy):
    h, w = img.shape[:2]
    return cv2.warpAffine(img, np.float32([[1, 0, ox], [0, 1, oy]]), (w, h))


def over(dst_rgb, dst_a, src_rgb, src_a):
    """Straight-alpha 'over'."""
    oa = src_a + dst_a * (1 - src_a)
    rgb = (src_rgb * src_a[..., None] + dst_rgb * (dst_a * (1 - src_a))[..., None]) / np.maximum(
        oa, 1e-5
    )[..., None]
    return rgb, oa


def pnoise(rng, shape, sigma):
    """Periodic (tileable) gaussian-filtered noise, unit std."""
    f = np.fft.fft2(rng.standard_normal(shape))
    ky = np.fft.fftfreq(shape[0])[:, None]
    kx = np.fft.fftfreq(shape[1])[None, :]
    f *= np.exp(-2 * (np.pi * sigma) ** 2 * (kx**2 + ky**2))
    n = np.real(np.fft.ifft2(f)).astype(np.float32)
    return n / (n.std() + 1e-6)


def sharpen(rgb, alpha, sigma, amount):
    d = rgb - blur(rgb, sigma)
    return rgb + d * amount * (alpha > 0.02)[..., None]


# ---------------------------------------------------------------- seal


def seal():
    """The user's photographic seal, deeper and lit: richer brick wax, relief and glints lifted,
    a three-part resting shadow (contact line, short, long). Same geometry as v9."""
    rgb, alpha = vs.clean_cutout(SEAL_SRC)
    lum = rgb.mean(-1)
    sel = alpha > 0.99
    med = np.median(rgb[sel & (lum > 50) & (lum < 140)], 0)
    target = np.array([146, 62, 42], np.float32)  # deeper brick than v9's #9A4C32, still terracotta
    gain = (target / med) ** 0.6
    w = np.clip((200 - lum) / 70, 0, 1) * np.clip((lum - 15) / 30, 0, 1)
    rgb = rgb * (1 + (gain - 1) * w[..., None])
    rgb = 255 * (np.clip(rgb, 0, 255) / 255) ** 1.1  # a touch more body in the mids
    lum = rgb.mean(-1)
    detail = lum - blur(lum, 9)  # relief: leaf ridges and rim pop, flat field stays calm
    rgb += (detail * 0.35)[..., None]
    hi_lo, hi_hi = np.percentile(lum[sel], [93, 99.7])
    hi = np.clip((lum - hi_lo) / (hi_hi - hi_lo), 0, 1) ** 1.6
    glint = np.array([255, 236, 214], np.float32)
    rgb = rgb + (glint - rgb) * (hi * 0.42)[..., None]  # wet glints, warm white
    col, wax = vs.place(rgb, alpha)
    n = vs.N
    s_contact = shifted(blur(wax, 1.4), 0.8, 1.6) * 0.62
    s_mid = shifted(blur(wax, 5.5), 4, 9) * 0.36
    s_long = shifted(blur(wax, 17), 13, 25) * 0.24
    sa = 1 - (1 - s_contact) * (1 - s_mid) * (1 - s_long)
    oa = wax + sa * (1 - wax)
    full = (col * wax[..., None] + SHADOW * (sa * (1 - wax))[..., None]) / np.maximum(oa, 1e-4)[
        ..., None
    ]
    assert oa[:, :4].max() < 0.02 and oa[-4:].max() < 0.02 and oa[:, -4:].max() < 0.02, (
        "shadow clipped"
    )
    side, hh = 768, round(0.63 * 768)
    r_s, a_s = reduce(full, oa, side, side)
    r_s = sharpen(r_s, a_s, 1.2, 0.12)
    save(r_s, a_s, "seal-whole.webp", 88, OUT)
    lip = np.clip(med * gain, 0, 255).astype(np.float32) * 0.88
    for c, a, name in vs.crack(full, oa, wax, lip):
        c2, a2 = reduce(c, a, side, hh)
        save(sharpen(c2, a2, 1.2, 0.12), a2, name, 88, OUT)
    return n


# ---------------------------------------------------------------- paper


def deckle(rng, n, base, amp):
    a = unit_noise(rng, (1, n + 200), 26)[0, 100:-100] * amp
    b = unit_noise(rng, (1, n + 40), 3.5)[0, 20:-20] * amp * 0.4
    c = unit_noise(rng, (1, n + 20), 1.2)[0, 10:-10] * amp * 0.15
    return np.maximum(1.0, base + a + b + c)


def paper_face(h, y0, free, seed, emboss=None):
    """One outer flap face, W x h px; y0 = its top in the packet (px). free = 'top' or 'bottom'."""
    rng = np.random.default_rng(seed)
    tile = np.asarray(Image.open(PAPER_TILE).convert("RGB"), np.float32)
    # the Copilot tile carries 8 px JPEG blocks (gate: 3.4); a light wrap-around blur removes them,
    # the fibres and flecks below bring the fine detail back
    tile = np.pad(tile, ((8, 8), (8, 8), (0, 0)), mode="wrap")
    tile = blur(tile, 1.0)[8:-8, 8:-8]
    ox, oy = rng.integers(0, 1024, 2)
    reps = (h // 1024 + 2, W // 1024 + 2)
    big = np.tile(tile, (reps[0], reps[1], 1))[oy : oy + h, ox : ox + W]
    rgb = big.copy()
    # cotton fibres: long, curved, mostly lighter, a few darker; sized for 3 px per CSS px
    fib = np.zeros((h, W), np.float32)
    for _ in range(int(h * W / 1500)):
        x, y = rng.uniform(-30, W + 30), rng.uniform(-30, h + 30)
        ang, ln = rng.uniform(0, np.pi), rng.uniform(12, 60)
        k = rng.integers(4, 8)
        pts = []
        for _s in range(k):
            ang += rng.normal(0, 0.3)
            pts.append((x, y))
            x += np.cos(ang) * ln / k
            y += np.sin(ang) * ln / k
        v = rng.choice([1.0, -0.7], p=[0.68, 0.32]) * rng.uniform(0.35, 1.0)
        cv2.polylines(fib, [np.int32(np.array(pts) * 4)], False, v, 1, cv2.LINE_AA, 2)
    rgb += blur(fib, 0.45)[..., None] * np.array([3.4, 3.4, 3.0], np.float32)
    # pulp inclusions: a few tiny flecks
    fl = np.zeros((h, W), np.float32)
    for _ in range(int(h * W / 60000)):
        cv2.circle(
            fl,
            (int(rng.uniform(0, W) * 4), int(rng.uniform(0, h) * 4)),
            int(rng.uniform(2, 6)),
            rng.uniform(0.4, 1),
            -1,
            cv2.LINE_AA,
            2,
        )
    rgb -= blur(fl, 0.7)[..., None] * np.array([16, 19, 24], np.float32)
    # paper cloud (formation): very low contrast
    rgb *= (1 + 0.009 * unit_noise(rng, (h, W), 70) + 0.004 * unit_noise(rng, (h, W), 14))[
        ..., None
    ]
    # one light across the packet: upper left bright, lower right a little darker; soft vignette
    yy, xx = np.mgrid[0:h, 0:W].astype(np.float32)
    px, py = xx / W, (yy + y0) / PH  # packet units, 0..1 x 0..1
    light = 1 + 0.03 * (1 - 2 * (0.45 * px + 0.55 * py))
    e = np.minimum.reduce([px, 1 - px, py * PH / W, (1 - py) * PH / W])
    light -= 0.018 * np.exp(-e / 0.06)
    rgb *= light[..., None]
    alpha = np.ones((h, W), np.float32)  # full bleed: the sides are the screen edges
    off = (
        deckle(rng, W, 3.6, 2.6)[None, :] if free == "bottom" else deckle(rng, W, 1.0, 0.6)[None, :]
    )
    d = yy if free == "top" else h - 1 - yy
    alpha *= np.clip((d - off) / 1.6 + 0.5, 0, 1)
    thin = np.exp(
        -np.maximum(d - off, 0) / 7.0
    )  # the torn edge is thinner: lighter, faintly see-through
    rgb += (thin * 5.0)[..., None]
    alpha *= 1 - 0.12 * np.exp(-np.maximum(d - off, 0) / 2.0)
    # the folded edge (the other end) rolls: top fold catches the light, bottom fold turns away
    df = h - 1 - yy if free == "top" else yy
    if free == "bottom":  # the top flap: its fold is the packet's top edge
        rgb *= (1 + 0.05 * np.exp(-df / 3.0) - 0.014 * np.exp(-(((df - 10) / 6) ** 2)))[..., None]
    else:  # the bottom flap: its fold is the packet's bottom edge
        rgb *= (1 - 0.05 * np.exp(-df / 4.0))[..., None]
    if emboss is not None:
        rgb *= (1 + emboss)[..., None]
    # paper tooth (fine, slightly soft grain) plus dither: no banding, no flat areas for blocks
    rgb += (unit_noise(rng, (h, W), 0.65) * 2.2)[..., None]
    rgb += (unit_noise(rng, (h, W), 1.8) * 1.8)[..., None]
    rgb += rng.standard_normal((h, W)).astype(np.float32)[..., None] * 0.9
    return np.clip(rgb, 0, 255), alpha


def emboss_overlay(w=860, h=1000):
    """Blind-embossed olive twig for the lower right of the bottom flap, as its own overlay
    (CSS: right bottom, 66.7 % of the width), so it stays in the corner on any screen height.
    Raised, no ink, lit from the upper left; a relief of the user's own olive twig silhouette.
    Highlights are warm white, shades warm umber, each with alpha, over the paper."""
    im = Image.open(TWIG).convert("RGBA")
    a = np.asarray(im, np.float32)[..., 3] / 255
    ys, xs = np.nonzero(a > 0.3)
    a = a[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
    stem_x = float(np.nonzero(a[2] > 0.3)[0].mean())  # where the cut stem leaves the top row
    s = 0.8 * 1200 / a.shape[0]  # twig length (as approved in the first v14 front)
    ux, uy = -0.56, -0.83  # the twig's 'down' (stem to tip) points up and in, toward the seal
    m = np.float32([[-uy * s, ux * s, 0], [ux * s, uy * s, 0]])  # (0, 1) -> (ux, uy), mirrored
    m[0, 2] = w + 0.035 * W - m[0, 0] * stem_x
    m[1, 2] = h - m[1, 0] * stem_x
    mask = cv2.warpAffine(a, m, (w, h), flags=cv2.INTER_AREA)
    hard = cv2.dilate(np.uint8(mask > 0.5), np.ones((3, 3), np.uint8))
    dist = cv2.distanceTransform(hard, cv2.DIST_L2, 5)
    hgt = blur(np.clip(dist / 8.0, 0, 1) ** 0.7, 2.4) + 0.2 * blur(mask, 5)
    gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=3)
    shade = -(gx * -0.6 + gy * -0.8)  # light from the upper left: + on slopes that face it
    shade = np.clip(shade / (np.percentile(np.abs(shade), 99.5) + 1e-6), -1, 1)
    e = 0.06 * shade + 0.004 * blur(mask, 2)  # relative change of the paper's brightness
    paper = 241.0
    hi, lo = np.array([255, 253, 247], np.float32), np.array([96, 74, 52], np.float32)
    a_hi = np.clip(e * paper / (hi.mean() - paper), 0, 1)
    a_lo = np.clip(-e * paper / (paper - lo.mean()), 0, 1)
    rgb = np.where((e >= 0)[..., None], hi, lo)
    rgb = np.broadcast_to(rgb, (h, w, 3)).astype(np.float32)
    return rgb, np.maximum(a_hi, a_lo)


def papers():
    """Faces for a full-bleed closed sheet, drawn with background-size: cover. The top flap is
    anchored at its bottom (its torn edge on the seam), the bottom flap at its top; the extra
    paper is cropped on shorter or wider screens."""
    ht, hb = 1100, 1860
    r, a = paper_face(ht, SEAM - ht, "bottom", 141)
    save(r, a, "closed-top.webp", 78, OUT)
    r, a = paper_face(hb, SEAM, "top", 142)
    save(r, a, "closed-bottom.webp", 78, OUT)
    r, a = emboss_overlay()
    img = Image.fromarray(
        np.dstack([np.uint8(np.clip(r, 0, 255)), np.uint8(np.clip(a, 0, 1) * 255)])
    )
    path = os.path.join(OUT, "closed-emboss.webp")
    img.save(path, "WEBP", quality=60, alpha_quality=70, method=6)  # smooth shading: light alpha
    print(f"closed-emboss.webp: {img.width}x{img.height} {os.path.getsize(path) // 1024} KB")


# ---------------------------------------------------------------- twine

JUTE = np.array([182, 143, 98], np.float32)


def path_frame(pts):
    d = np.gradient(pts, axis=0)
    t = d / np.maximum(np.linalg.norm(d, axis=1, keepdims=True), 1e-6)
    nrm = np.stack([-t[:, 1], t[:, 0]], 1)  # left of travel; (0, 1) = down for a left-to-right path
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    return t, nrm, s


def cord(shape, pts, r, pitch, seed, fade_end=None):
    """A 2-ply twisted jute cord along pts (dense, ~0.5 px apart). Returns rgb, alpha (H x W)."""
    rng = np.random.default_rng(seed)
    hgt, wid = shape
    t, nrm, s = path_frame(pts)
    x0 = int(max(pts[:, 0].min() - r - 6, 0))
    x1 = int(min(pts[:, 0].max() + r + 6, wid))
    y0 = int(max(pts[:, 1].min() - r - 6, 0))
    y1 = int(min(pts[:, 1].max() + r + 6, hgt))
    bw, bh = x1 - x0, y1 - y0
    src = np.full((bh, bw), 255, np.uint8)
    ip = np.round(pts - [x0, y0]).astype(int)
    ok = (ip[:, 0] >= 0) & (ip[:, 0] < bw) & (ip[:, 1] >= 0) & (ip[:, 1] < bh)
    src[ip[ok, 1], ip[ok, 0]] = 0
    _, lab = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    lab2i = np.zeros(lab.max() + 1, np.int64)
    idx_ok = np.nonzero(ok)[0]
    lab2i[lab[ip[ok, 1], ip[ok, 0]]] = idx_ok
    i = lab2i[lab]
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    dx, dy = xx - pts[i, 0], yy - pts[i, 1]
    sd = dx * nrm[i, 0] + dy * nrm[i, 1]
    u = s[i] + dx * t[i, 0] + dy * t[i, 1]
    v = np.clip(sd / r, -1, 1)
    alpha = np.clip(r - np.abs(sd) + 0.5, 0, 1)
    alpha *= np.clip(u + 0.5, 0, 1) * np.clip(s[-1] - u + 0.5, 0, 1)
    theta = np.arcsin(v)
    jit = unit_noise(rng, (1, int(s[-1]) + 64), 14)[0]
    ju = jit[np.clip(u.astype(int), 0, len(jit) - 1)]
    su = (
        u / pitch + theta / np.pi * 0.55 + 0.09 * ju
    )  # S-twist: ply boundaries lean; hand-spun, uneven
    seg = np.floor(2 * su)
    wply = 2 * su - seg
    bump = np.sin(np.pi * wply) ** 0.55
    groove = np.exp(-((np.minimum(wply, 1 - wply) / 0.09) ** 2))
    nz = np.sqrt(1 - v**2)
    lc = 0.5 + 0.38 * nz - 0.22 * v  # light from above: upper side brighter
    # fibres run along each ply: stripes of constant wply, re-seeded per ply segment
    fn = unit_noise(rng, (1, 4096), 0.8)[0]
    fk = (np.floor(wply * 46).astype(np.int64) + (seg.astype(np.int64) * 131) % 4096) % 4096
    fib = fn[fk]
    pvals = rng.normal(0, 1, 4096).astype(np.float32)
    pv = pvals[(seg.astype(np.int64) + 2048) % 4096]  # each ply turn a touch lighter or darker
    along = unit_noise(rng, (1, int(s[-1]) + 64), 30)[0]
    alu = along[np.clip(u.astype(int), 0, len(along) - 1)]
    lum = (
        lc
        * (0.62 + 0.38 * bump)
        * (1 - 0.4 * groove)
        * (1 + 0.1 * fib)
        * (1 + 0.07 * alu)
        * (1 + 0.05 * pv)
    )
    col = JUTE[None, None, :] * lum[..., None] * 1.18
    spec = np.exp(-(((v + 0.5) / 0.28) ** 2)) * bump**2 * 26
    col += spec[..., None] * np.array([1, 0.94, 0.82], np.float32)
    col += (unit_noise(rng, (bh, bw), 0.6) * 4)[..., None]
    if fade_end is not None:  # the last length untwists: plies thin out into fibre
        k = np.clip((u - (s[-1] - fade_end)) / fade_end, 0, 1)
        alpha *= 1 - k * np.clip(0.55 + 0.6 * fib, 0, 1) * (np.abs(v) > 0.15 * (1 - k))
    R = np.zeros((hgt, wid, 3), np.float32)
    A = np.zeros((hgt, wid), np.float32)
    R[y0:y1, x0:x1] = col
    A[y0:y1, x0:x1] = alpha
    return R, A


def hairs(shape, pts, r, n, seed, spread=None, start=None):
    """Stray fibres: short curved hairs off a cord's sides, or (spread) a fan out of its end."""
    rng = np.random.default_rng(seed)
    t, nrm, s = path_frame(pts)
    R = np.zeros(shape + (3,), np.float32)
    A = np.zeros(shape, np.float32)
    for _ in range(n):
        if spread is None:
            j = rng.integers(0, len(pts))
            side = rng.choice([-1, 1])
            p = pts[j] + nrm[j] * side * r * rng.uniform(0.6, 0.95)
            ang = np.arctan2(nrm[j, 1] * side, nrm[j, 0] * side) + rng.normal(0, 0.9)
            ln = rng.uniform(5, 22)
        else:
            j = len(pts) - 1 - rng.integers(0, start)
            p = pts[j] + nrm[j] * rng.uniform(-0.8, 0.8) * r
            ang = np.arctan2(t[j, 1], t[j, 0]) + rng.normal(0, spread)
            ln = rng.uniform(20, 95)
        q = [p.copy()]
        k = 6
        for _s in range(k):
            ang += rng.normal(0, 0.18)
            p = p + np.array([np.cos(ang), np.sin(ang)]) * ln / k
            q.append(p.copy())
        q = np.array(q)
        bx0, by0 = np.floor(q.min(0) - 4).astype(int)
        bx1, by1 = np.ceil(q.max(0) + 4).astype(int)
        bx0, by0 = max(bx0, 0), max(by0, 0)
        bx1, by1 = min(bx1, shape[1]), min(by1, shape[0])
        if bx1 <= bx0 or by1 <= by0:
            continue
        a = np.zeros((by1 - by0, bx1 - bx0), np.float32)
        th = 1 if spread is None else int(rng.choice([1, 1, 2]))
        cv2.polylines(a, [np.int32((q - [bx0, by0]) * 4)], False, 1.0, th, cv2.LINE_AA, 2)
        tone = rng.uniform(0.7, 1.02)
        a *= rng.uniform(0.45, 0.85)
        c = np.broadcast_to(np.clip(JUTE * tone * 1.05, 0, 255), a.shape + (3,))
        sub_r, sub_a = over(R[by0:by1, bx0:bx1], A[by0:by1, bx0:bx1], c, a)
        R[by0:by1, bx0:bx1], A[by0:by1, bx0:bx1] = sub_r, sub_a
    return R, A


def sprig(shape, tuck, ang, length):
    """A whole pressed olive sprig: the user's twig from its cut stem to its natural tip, the cut
    end tucked under the knot (hidden by the wax), the tip reaching out along the twine.
    tuck = (x, y) of the cut stem end; ang = direction stem -> tip in degrees (0 = right,
    90 = down); length = stem length in px. A light relief from the silhouette (leaf edges
    catch the light from the upper left) so the painted leaves sit as a real, flat object.
    Returns rgb, alpha and t (0 at the stem end, 1 at the tip) for a shadow that lifts."""
    im = Image.open(TWIG).convert("RGBA")
    a = np.asarray(im, np.float32)
    ys, xs = np.nonzero(a[..., 3] > 30)
    a = a[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
    rgb, al = a[..., :3], a[..., 3] / 255
    lum = rgb.mean(-1, keepdims=True)
    rgb = lum + (rgb - lum) * 0.85  # pressed: a little drier
    rgb = rgb * np.array([1.0, 0.99, 0.95], np.float32)
    stem_x = float(np.nonzero(al[2] > 0.3)[0].mean())
    sc = length / a.shape[0]
    ux, uy = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    m = np.float32([[uy * sc, ux * sc, 0], [-ux * sc, uy * sc, 0]])  # a rotation: (0, 1) -> u
    m[0, 2] = tuck[0] - m[0, 0] * stem_x
    m[1, 2] = tuck[1] - m[1, 0] * stem_x
    pm = np.dstack([rgb * al[..., None], al])
    out = cv2.warpAffine(pm, m, (shape[1], shape[0]), flags=cv2.INTER_AREA)
    A = np.clip(out[..., 3], 0, 1)
    R = out[..., :3] / np.maximum(A, 1e-4)[..., None]
    hgt = blur(A, 3.0)
    gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=3)
    sh = -(gx * -0.6 + gy * -0.8)
    sh = np.clip(sh / (np.percentile(np.abs(sh[A > 0.5]), 99) + 1e-6), -1, 1)
    R = R * (1 + 0.1 * sh)[..., None]
    yy, xx = np.mgrid[0 : shape[0], 0 : shape[1]].astype(np.float32)
    t = np.clip(((xx - tuck[0]) * ux + (yy - tuck[1]) * uy) / length, 0, 1)
    return np.clip(R, 0, 255), A, t


def shadow_of(A, k, lift=None):
    """Soft resting shadow to the lower right; where lift > 0 the object stands off the paper
    (the sprig's tip), so its shadow moves out and softens."""
    s1 = shifted(blur(A, 1.6 * k), 1.6 * k, 2.6 * k) * 0.42
    s2 = shifted(blur(A, 6 * k), 5 * k, 9 * k) * 0.22
    sh = 1 - (1 - s1) * (1 - s2)
    if lift is None:
        return sh
    s3 = shifted(blur(A, 4 * k), 5 * k, 8 * k) * 0.34
    s4 = shifted(blur(A, 10 * k), 10 * k, 17 * k) * 0.16
    up = 1 - (1 - s3) * (1 - s4)
    w = blur(lift, 8 * k) ** 1.3
    return sh * (1 - w) + up * w


def deco(with_sprig=True, shadow=True, out=OUT):
    """Two clean jute strands wrapping the sheet edge to edge, pinched together where they are
    knotted under the seal (the knot and its ends are under the wax: nothing loose shows), and
    a whole pressed olive sprig whose cut stem is tucked into the knot, the strands crossing
    over its stem just outside the wax, its tip reaching out to the left."""
    k = 2  # supersample
    w, h = 1300 * k, 648 * k
    cx, cy = w / 2, h / 2
    xs = np.arange(-20, w + 20, 0.5, dtype=np.float32)
    rng = np.random.default_rng(7)
    wob = unit_noise(rng, (1, len(xs)), 260)[0]
    pinch = np.exp(-(((xs - cx) / (0.2 * w)) ** 2))  # held together under the wax
    tilt = (xs - cx) * -0.008  # the twine is not quite level: left end a touch lower
    sep = (8.5 + 7.5 * (1 - pinch)) * k
    yA = cy + tilt - sep / 2 + wob * 2.0 * k
    yB = cy + tilt + sep / 2 - wob * 1.2 * k + 1.5 * k
    r = 7.4 * k
    pitch = 19 * k
    pa = np.stack([xs, yA], 1)
    pb = np.stack([xs, yB], 1)
    stack = []
    if with_sprig:
        R0, A0, t0 = sprig((h, w), (520 * k, cy + 70 * k), 210.0, 470 * k)
        stack.append((R0, A0, t0))
    cA = cord((h, w), pa, r, pitch, 11)
    cB = cord((h, w), pb, r, pitch, 12)
    fA = hairs((h, w), pa, r, 260, 21)
    fB = hairs((h, w), pb, r, 260, 22)
    # each layer's shadow falls on all below: sprig, strand A, its fibres, strand B, its fibres
    stack += [(*cA, None), (*fA, None), (*cB, None), (*fB, None)]
    R = np.zeros((h, w, 3), np.float32)
    A = np.zeros((h, w), np.float32)
    for rr, aa, lift in stack:
        if shadow:
            sh = shadow_of(aa, k, lift)
            R, A = over(R, A, np.broadcast_to(SHADOW, (h, w, 3)), sh * (1 - aa))
        R, A = over(R, A, rr, aa)
    r2, a2 = reduce(R, A, w // k, h // k)
    name = "closed-deco.webp" if with_sprig else "closed-deco-nosprig.webp"
    save(sharpen(r2, a2, 0.8, 0.3), a2, name, 86, out)


# ---------------------------------------------------------------- linen


def linen():
    """Seamless plain-weave flax linen, 1536 px rendered, 768 px saved (256 CSS px per tile)."""
    rng = np.random.default_rng(91)
    n, nt = 1536, 192
    p = n / nt
    base = np.array([214, 206, 189], np.float32)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    xw = xx + 1.6 * pnoise(rng, (n, n), 24)
    yw = yy + 1.6 * pnoise(rng, (n, n), 24)
    i = np.floor(xw / p).astype(np.int64) % nt
    j = np.floor(yw / p).astype(np.int64) % nt
    fx, fy = xw / p % 1, yw / p % 1

    def along(seed, sig):  # per-thread variation along its length (periodic), with slubs
        g = np.random.default_rng(seed)
        f = np.fft.fft(g.standard_normal((nt, n)), axis=1)
        k = np.fft.fftfreq(n)[None, :]
        v = np.real(np.fft.ifft(f * np.exp(-2 * (np.pi * sig * k) ** 2), axis=1)).astype(np.float32)
        v /= v.std()
        slub = np.maximum(v - 1.6, 0) * 1.4
        return v, slub

    va, sa = along(1, 40)
    vb, sb = along(2, 40)
    tw = np.clip(0.62 + 0.07 * va[i, yy.astype(int)] + 0.25 * sa[i, yy.astype(int)], 0.4, 0.98)
    tf = np.clip(0.64 + 0.07 * vb[j, xx.astype(int)] + 0.25 * sb[j, xx.astype(int)], 0.4, 0.98)
    bw = np.clip(1 - ((fx - 0.5) / (tw / 2)) ** 2, 0, 1) ** 0.5
    bf = np.clip(1 - ((fy - 0.5) / (tf / 2)) ** 2, 0, 1) ** 0.5
    up = ((i + j) % 2 == 0).astype(np.float32)
    hw = bw * (0.62 + 0.38 * up) * (0.8 + 0.2 * np.sin(np.pi * fy) * up + 0.2 * (1 - up))
    hf = bf * (0.62 + 0.38 * (1 - up)) * (0.8 + 0.2 * np.sin(np.pi * fx) * (1 - up) + 0.2 * up)
    H = np.maximum(hw, hf)
    warp_on = hw >= hf
    tc_w = rng.normal(0, 1, nt).astype(np.float32)
    tc_f = rng.normal(0, 1, nt).astype(np.float32)
    tone = np.where(
        warp_on,
        0.026 * tc_w[i] + 0.014 * va[i, yy.astype(int)],
        0.03 * tc_f[j] + 0.014 * vb[j, xx.astype(int)],
    )
    gx = np.roll(H, -1, 1) - np.roll(H, 1, 1)
    gy = np.roll(H, -1, 0) - np.roll(H, 1, 0)
    shade = -(gx * -0.6 + gy * -0.8) * 0.5
    gap = np.clip(1 - H / 0.25, 0, 1)
    fuzz = pnoise(rng, (n, n), 0.9) * 0.012
    mott = pnoise(rng, (n, n), 160) * 0.014 + pnoise(rng, (n, n), 40) * 0.008
    lum = (1 + tone + 0.07 * shade - 0.12 * gap + fuzz + mott) * (0.95 + 0.05 * H)
    rgb = base[None, None, :] * lum[..., None]
    rgb = cv2.resize(rgb, (768, 768), interpolation=cv2.INTER_AREA)
    # the cloth lies a few cm below the letter's focus: a touch of depth of field (wrap: seamless)
    rgb = np.pad(rgb, ((8, 8), (8, 8), (0, 0)), mode="wrap")
    rgb = cv2.GaussianBlur(rgb, (0, 0), 0.55)[8:-8, 8:-8]
    img = Image.fromarray(np.uint8(np.clip(rgb, 0, 255)), "RGB")
    path = os.path.join(OUT, "linen.webp")
    img.save(path, "WEBP", quality=74, method=6)
    print(
        f"linen.webp: 768x768 {os.path.getsize(path) // 1024} KB,",
        f"mean {np.asarray(img).mean((0, 1)).round()}",
    )


def main():
    os.makedirs(OUT, exist_ok=True)
    what = sys.argv[1:] or ["seal", "papers", "deco", "linen"]
    if "seal" in what:
        seal()
    if "papers" in what:
        papers()
    if "deco" in what:
        deco(True)
        deco(False)
    if (
        "deco-check" in what
    ):  # the quality gate's halo test, on the cut edges without the baked shadow
        deco(True, False, sys.argv[sys.argv.index("deco-check") + 1])
    if "linen" in what:
        linen()


if __name__ == "__main__":
    main()
