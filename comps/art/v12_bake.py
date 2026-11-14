#!/usr/bin/env python3
"""Bake the v12 art: the four dogs (the user's Copilot cut-outs) and the citrus bough (USDA plates).

owner: Tomas | review date: 2026-11-18
canonical path: projects/wedding-invite/comps/art/v12_bake.py
rollback: rm -rf projects/wedding-invite/comps/art/v12_bake.py projects/wedding-invite/comps/art/v12

Usage: .venv/bin/python -I comps/art/v12_bake.py   (writes comps/art/v12/*.webp, prints CSS numbers)

Dogs: each cut-out is defringed (edge pixels take the colour of the fur just inside, so no light
halo shows on the paper), trimmed to its bounding box and reduced to 3x its largest display size
(the column is at most 440 px, so 1u is at most 4.4 px), or to the quality gate's 600 px floor
where that is larger. The blue-roan dog's tail is split off
along a line at its base, so it can wag about that point; the golden's raised arm merges into its
chest fur, so it is not split (a wave would show fur that was never painted).

Citrus: public-domain USDA Pomological Watercolor plates (assets/LOG.md has the URLs). The plate
paper is keyed out by colour distance; the colours are toned toward the page (less saturation,
a little warmth) so the fruit sits with the painted sky and the olive. The twig with two leaves
(POM00007465) is flipped so it enters from the right edge; fruit units are cut
so the top centre of each image is its stem top, the CSS pivot.
"""

import os

import cv2
import numpy as np
from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
INBOX = os.path.join(ROOT, "assets", "inbox")
OUT = os.path.join(HERE, "v12")
UMAX = 4.4  # px per u at the widest column
DOG_W = {"tan": 17, "collie": 18, "golden": 19, "merle": 17}  # display width in u


def save(img, name, q=82):
    path = os.path.join(OUT, name)
    img.save(path, "WEBP", quality=q, method=6)
    print(f"{name}: {img.width}x{img.height} {os.path.getsize(path) // 1024} KB")


def defringe(rgba):
    a = rgba[..., 3].astype(np.float32) / 255
    rgb = rgba[..., :3].astype(np.float32)
    core = (a > 0.97).astype(np.float32)
    core = cv2.erode(core, np.ones((3, 3), np.uint8))
    fill = (
        cv2.GaussianBlur(rgb * core[..., None], (0, 0), 3)
        / np.maximum(cv2.GaussianBlur(core, (0, 0), 3), 1e-4)[..., None]
    )
    w = np.clip((a - 0.55) / 0.42, 0, 1)
    rgb = rgb * w[..., None] + fill * (1 - w[..., None])
    a = np.clip((a - 0.06) / 0.94, 0, 1)  # drop the faintest matte haze
    return np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8)


def dogs():
    for name, wu in DOG_W.items():
        im = np.asarray(
            Image.open(os.path.join(INBOX, "dogs", f"dog-{name}-cut.webp")).convert("RGBA")
        )
        im = defringe(im)
        ys, xs = np.nonzero(im[..., 3] > 8)
        im = im[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
        # 600 px on the long side: the quality gate's floor, about 4x the largest display size
        h = 600
        target = round(im.shape[1] * h / im.shape[0])
        if name == "merle":
            # the tail: everything right of a line through its base, below the haunch
            hh, ww = im.shape[:2]
            yy, xx = np.mgrid[0:hh, 0:ww]
            # base of the tail in the trimmed image: (735, 935) to (752, 1030); the tail runs right
            x0, y0, x1, y1 = 735, 920, 760, 1040
            side = (xx - x0) * (y1 - y0) - (yy - y0) * (x1 - x0)  # > 0 right of the line
            tail = (side > 0) & (yy > 925) & (xx > 700)
            body = im.copy()
            body[tail, 3] = 0
            tl = np.zeros_like(im)
            tl[tail] = im[tail]
            for arr, nm in ((body, "dog-merle.webp"), (tl, "dog-merle-tail.webp")):
                save(Image.fromarray(arr).resize((target, h), Image.LANCZOS), nm)
            s = target / ww
            print(
                f"merle tail pivot: {(x0 + x1) / 2 * s / target * 100:.1f}%"
                f" {(y0 + 40) * s / h * 100:.1f}%"
            )
        else:
            save(Image.fromarray(im).resize((target, h), Image.LANCZOS), f"dog-{name}.webp")
        print(f"  {name}: {wu}u wide, aspect {im.shape[1]}/{im.shape[0]}")


# ---------------------------------------------------------------- citrus


def key_out(rgb, lo=14, hi=40, close=5):
    """Alpha from the colour distance to the plate paper (median of the crop's border)."""
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    border = np.concatenate(
        [lab[:6].reshape(-1, 3), lab[-6:].reshape(-1, 3), lab[:, :6].reshape(-1, 3)]
    )
    paper = np.median(border, 0)
    d = np.sqrt(((lab - paper) ** 2 * np.array([0.6, 1.0, 1.0])).sum(-1))
    a = np.clip((d - lo) / (hi - lo), 0, 1)
    hard = np.uint8(a > 0.5)
    hard = cv2.morphologyEx(
        hard, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close, close))
    )
    n, lab_c, st, _ = cv2.connectedComponentsWithStats(hard)
    keep = np.zeros_like(hard)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 0.02 * st[1:, cv2.CC_STAT_AREA].max():
            keep[lab_c == i] = 1
    ff = keep.copy()
    cv2.floodFill(ff, None, (0, 0), 2)
    keep[ff == 0] = 1  # holes inside the shape stay opaque
    soft = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 1.2)
    a = np.maximum(np.minimum(a, soft), np.clip((soft - 0.5) * 2, 0, 1) * (a > 0.25))
    return np.dstack([rgb, np.uint8(np.clip(a, 0, 1) * 255)])


def tone(img, sat, warm=1.0, bright=1.0):
    rgb = img.convert("RGB")
    rgb = ImageEnhance.Color(rgb).enhance(sat)
    rgb = ImageEnhance.Brightness(rgb).enhance(bright)
    arr = np.asarray(rgb, np.float32)
    arr[..., 0] *= warm
    arr[..., 2] /= warm
    out = Image.fromarray(np.uint8(np.clip(arr, 0, 255)))
    out.putalpha(img.getchannel("A"))
    return out


def trim(img):
    a = np.asarray(img.getchannel("A"))
    ys, xs = np.nonzero(a > 8)
    return img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)), (xs.min(), ys.min())


def citrus():
    # C0 bough: twig with two leaves, above the plate's fruit; flipped to enter from the right
    plate = np.asarray(Image.open(os.path.join(INBOX, "plate-kumquat-twig.jpg")).convert("RGB"))
    box = (820, 460, 1890, 1240)
    twig = Image.fromarray(key_out(np.ascontiguousarray(plate[box[1] : box[3], box[0] : box[2]])))
    twig = tone(twig, 0.82, 1.02, 1.04).transpose(Image.FLIP_LEFT_RIGHT)
    bw = 600  # the gate's floor; about 3.1x the largest display size
    s = bw / twig.width
    twig = twig.resize((bw, round(twig.height * s)), Image.LANCZOS)
    save(twig, "bough.webp")
    # stub stems of the plate (fruit stalks), flipped, in u from the bough's top-left
    for nm, (px, py) in (("stub-a", (1110, 1238)), ("stub-b", (1330, 1240))):
        x = (box[2] - px) * s / (UMAX * 3)
        y = (py - box[1]) * s / (UMAX * 3)
        print(f"  bough {nm}: x {x:.1f}u y {y:.1f}u from the bough box")
    print(f"  bough: 44u wide, aspect {twig.width}/{twig.height}")

    # C2 orange: tangerine with its stem, turned so the stem hangs straight up, stem cut short
    plate = np.asarray(Image.open(os.path.join(INBOX, "plate-tangerine-stem.jpg")).convert("RGB"))
    box = (860, 780, 1900, 1900)
    o = Image.fromarray(
        key_out(np.ascontiguousarray(plate[box[1] : box[3], box[0] : box[2]]), close=7)
    )
    top, calyx = np.array([910, 828]) - box[:2], np.array([1300, 1097]) - box[:2]
    v = top - calyx
    ang = np.degrees(np.arctan2(v[1], v[0]))  # image angle of the stem, y down
    rot = -(-90 - ang)  # PIL rotates counter-clockwise
    o2 = rot_about(o, rot, calyx)
    o2, _ = trim(o2)
    o2 = tone(o2, 0.64, 1.0, 1.04)
    # nudge the hue from red-orange toward orange: a little more green
    arr = np.asarray(o2, np.float32)
    arr[..., 1] = np.clip(arr[..., 1] * 1.24, 0, 255)
    o2 = Image.fromarray(np.uint8(arr), "RGBA")
    a = np.asarray(o2.getchannel("A"))
    # keep only the lower 45% of the stem: find the calyx row (the widest jump in opacity width)
    widths = (a > 128).sum(1)
    fruit_top = int(np.argmax(widths > widths.max() * 0.25))
    stem_len = fruit_top
    cut = int(stem_len * 0.55)
    o3 = o2.crop((0, cut, o2.width, o2.height))
    o3 = hang(o3)
    ow = round(13 * UMAX * 3)
    o3 = o3.resize((ow, round(o3.height * ow / o3.width)), Image.LANCZOS)
    o3 = recentre(o3)
    save(o3, "orange.webp")
    print(f"  orange: 13u wide, aspect {o3.width}/{o3.height}")
    stem_piece = o2.crop((0, 0, o2.width, cut))
    stem_piece, _ = trim(stem_piece)
    # drop the plate's pale cut end at the stalk's top
    stem_piece = stem_piece.crop(
        (0, round(stem_piece.height * 0.22), stem_piece.width, stem_piece.height)
    )

    # C1, C3 lemons: the existing lemon cut-out, toned; C1 hangs on a piece of the orange's stalk
    lemon = Image.open(os.path.join(ROOT, "assets", "cutouts", "lemon-whole.webp")).convert("RGBA")
    lemon, _ = trim(lemon)
    lemon = tone(lemon, 0.72, 1.01, 0.98)
    for nm, wu, stem, mirror, tilt in (
        ("lemon-a.webp", 9, True, False, -6),
        ("lemon-b.webp", 8, False, True, 5),
    ):
        lw = round(wu * UMAX * 3)
        lm = lemon.transpose(Image.FLIP_LEFT_RIGHT) if mirror else lemon
        lm = lm.rotate(tilt, Image.BICUBIC, expand=True)
        lm, _ = trim(lm)
        lm = lm.resize((lw, round(lm.height * lw / lm.width)), Image.LANCZOS)
        if stem:
            sp = stem_piece.resize(
                (max(6, round(stem_piece.width * lw / 120 * 0.35)), round(lw * 0.55)), Image.LANCZOS
            )
            canvas = Image.new("RGBA", (lw, sp.height + lm.height - 6), (0, 0, 0, 0))
            canvas.alpha_composite(lm, (0, sp.height - 6))
            canvas.alpha_composite(sp, ((lw - sp.width) // 2 - round(lw * 0.06), 0))
            lm = canvas
        lm = recentre(lm)
        save(lm, nm)
        print(f"  {nm}: {wu}u wide, aspect {lm.width}/{lm.height}")


def hang(img):
    """Turn a stalk-and-fruit cut-out about its stem top until the fruit hangs straight below."""
    a = np.asarray(img.getchannel("A")).astype(np.float32) / 255
    rows = np.nonzero(a.max(1) > 0.25)[0]
    top = np.array([np.nonzero(a[rows[0]] > 0.25)[0].mean(), rows[0]])
    ys, xs = np.mgrid[0 : a.shape[0], 0 : a.shape[1]]
    c = np.array([(xs * a).sum(), (ys * a).sum()]) / a.sum()
    v = c - top
    ang = np.degrees(np.arctan2(v[0], v[1]))  # 0 when the centre is straight below
    return trim(rot_about(img, -ang, top))[0]


def rot_about(img, deg, pivot):
    """Rotate about a pivot without clipping (PIL clips when center and expand are combined)."""
    px, py = float(pivot[0]), float(pivot[1])
    r = (
        int(np.ceil(max(np.hypot(px - x, py - y) for x in (0, img.width) for y in (0, img.height))))
        + 2
    )
    canvas = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
    canvas.alpha_composite(img, (int(round(r - px)), int(round(r - py))))
    return canvas.rotate(deg, Image.BICUBIC)


def recentre(img):
    """Pad so the topmost opaque pixel (the stem top) sits at the horizontal centre (CSS pivot)."""
    a = np.asarray(img.getchannel("A"))
    rows = np.nonzero(a.max(1) > 60)[0]
    xs = np.nonzero(a[rows[0]] > 60)[0]
    sx = int(xs.mean())
    pad = abs(img.width - 2 * sx)
    canvas = Image.new("RGBA", (img.width + pad, img.height), (0, 0, 0, 0))
    canvas.alpha_composite(img, (pad if sx < img.width / 2 else 0, 0))
    return canvas


def grass():
    """The user's two grass clumps at 2x of their largest display (28u, 30u at 4.4 px/u)."""
    src = os.path.join(HERE, "v10", "src")
    for name, fn, wu in (
        ("grass-a-2x.webp", "10-img-grass-a.webp", 28),
        ("grass-b-2x.webp", "11-img-grass-b.webp", 30),
    ):
        im = Image.open(os.path.join(src, fn)).convert("RGBA")
        w = round(wu * UMAX * 2)
        save(im.resize((w, round(im.height * w / im.width)), Image.LANCZOS), name, 84)


def main():
    os.makedirs(OUT, exist_ok=True)
    dogs()
    citrus()
    grass()


if __name__ == "__main__":
    main()
