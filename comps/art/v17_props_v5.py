#!/usr/bin/env python3
"""Cut, tone and export the Copilot v5 and v6 props for the information page (2026-11-14).

owner: Tomas | review date: 2026-11-28
canonical path: projects/wedding-invite/comps/art/v17_props_v5.py
rollback: rm projects/wedding-invite/comps/art/v17_props_v5.py and its outputs in
comps/art/v17/ (fig-branch, wild-carrot, pebbles, fly-agaric, bee, peppers .webp)

Usage: .venv/bin/python -I comps/art/v17_props_v5.py

Key (paper division, DESIGN-SPEC section 6): each painting lies on a flat paper or grey
ground. The ground is the median of the border; the picture is divided by it, so the
ground becomes white and a wash becomes its own transmittance p. Alpha is how far p is
from white (minus a small floor that drops paper grain), and the colour is un-mixed from
white, so soft wet edges stay soft and no paper film is left round the forms. Then: small
specks (soil crumbs) dropped, noise smoothed, saturation toned, blacks lifted to the page
ink, trimmed, resized to 3x the largest display width, WebP.
"""

import os

import cv2
import numpy as np
from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
INBOX = os.path.join(HERE, "..", "..", "assets", "inbox")
OUT = os.path.join(HERE, "v17")

# out name: (source, width px at 3x, saturation, mirror, speck area floor at full size)
PIECES = {
    "fig-branch": ("l2-fig-branch-v5.jpg", 372, 0.82, False, 400),
    "wild-carrot": ("f3-wild-carrot-v5.jpg", 210, 0.9, False, 120),
    "pebbles": ("r2-pebbles-v5.png", 220, 0.78, False, 400),
    "fly-agaric": ("m5-fly-agaric-v6.jpg", 180, 0.54, False, 700),
    "bee": ("b1-bee-v6.jpg", 96, 0.75, False, 700),
    "peppers": ("p1-peppers-v6.jpg", 108, 0.6, False, 700),
}
FLOOR, GAIN = 0.05, 1.7


def key(rgb):
    rgb = rgb.astype(np.float32)
    b = np.concatenate(
        [
            rgb[:12].reshape(-1, 3),
            rgb[-12:].reshape(-1, 3),
            rgb[:, :12].reshape(-1, 3),
            rgb[:, -12:].reshape(-1, 3),
        ]
    )
    ground = np.median(b, 0)
    p = np.clip(rgb / ground, 0, 1)
    dark = 1 - p.min(-1)
    a = np.clip((dark - FLOOR) * GAIN / (1 - FLOOR), 0, 1)
    c = 1 - (1 - p) / np.maximum(a, 1e-3)[..., None]
    c = np.clip(c, 0, 1) * 255
    return c, a


def despeck(a, floor):
    n, lab, st, _ = cv2.connectedComponentsWithStats(np.uint8(a > 0.12))
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] >= floor
    mask = cv2.dilate(np.uint8(keep[lab]), np.ones((9, 9), np.uint8)).astype(bool)
    return np.where(mask, a, 0)


def build(name, src, width, sat, mirror, floor):
    im = Image.open(os.path.join(INBOX, src)).convert("RGB")
    c, a = key(np.asarray(im))
    a = despeck(a, floor)
    # paper grain belongs to the page, not the asset (DESIGN-SPEC section 3)
    c = cv2.fastNlMeansDenoisingColored(np.uint8(c), None, 7, 7, 7, 21)
    rgb = Image.fromarray(c)
    rgb = ImageEnhance.Color(rgb).enhance(sat)
    arr = np.asarray(rgb, np.float32)
    # lift the blacks: nothing darker than the page ink #3B2F25 (luminance about 48)
    lum = arr @ np.array([0.299, 0.587, 0.114], np.float32)
    lift = np.clip((48 - lum) / 48, 0, 1)[..., None]
    arr = arr * (1 - lift) + np.array([59, 47, 37], np.float32) * lift
    out = Image.fromarray(np.uint8(np.clip(arr, 0, 255)))
    out.putalpha(Image.fromarray(np.uint8(a * 255)))
    ys, xs = np.nonzero(a > 0.03)
    out = out.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    if mirror:
        out = out.transpose(Image.FLIP_LEFT_RIGHT)
    h = round(out.height * width / out.width)
    out = out.resize((width, h), Image.LANCZOS)
    path = os.path.join(OUT, name + ".webp")
    out.save(path, "WEBP", quality=82, method=6)
    hsv = np.asarray(out.convert("RGB").convert("HSV"), np.float32)[..., 1] / 255
    al = np.asarray(out.getchannel("A")) > 128
    kb = os.path.getsize(path) // 1024
    print(f"{name}: {width}x{h} {kb} KB, p95 sat {np.percentile(hsv[al], 95):.2f}")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for n, spec in PIECES.items():
        build(n, *spec)
