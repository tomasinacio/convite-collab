#!/usr/bin/env python3
"""Quality gate for artwork: rejects small, grainy, blocky or fake-upscaled images.

owner: Tomas | review date: 2026-11-10
canonical path: projects/wedding-invite/scripts/image_quality.py
rollback: rm -f projects/wedding-invite/scripts/image_quality.py

Usage:
  image_quality.py IMAGE [--role hero|asset|small] [--metrics]
  image_quality.py --selftest        proves the gate rejects bad images and accepts a good one

Roles set the minimum long side in pixels: hero 1800 (full-screen art, retina phones),
asset 1200, small 600. Checks: resolution; noise (grain); sharpness (soft or smeared);
fake upscaling (little fine detail for the pixel count); JPEG blocking; for cutouts with
alpha, a light or dark halo on semi-transparent edge pixels. Exit 0 pass, 1 fail.
This gate checks TECHNICAL quality only. It cannot see mangled forms, smeared motifs or
an 'AI look'; that judgement belongs to an Opus 5.5 high agent plus the user at the asset
gate (see designer-playbook). Thresholds were calibrated on a real public-domain scan
and degraded copies of it; change them only by re-running --selftest.
"""

import argparse
import os
import sys

import cv2
import numpy as np
from PIL import Image

MIN_LONG = {"hero": 1800, "asset": 1200, "small": 600}
WORK = 1200  # evaluate at roughly delivery scale
HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "..", "tests", "data", "reference-watercolor.jpg")
SAMPLE2 = os.path.join(
    HERE, "..", "tests", "data", "reference-lemon.jpg"
)  # not used for calibration

# thresholds (calibrated, see selftest)
MAX_NOISE = 2.3  # Immerkaer sigma on the working-scale grayscale (good scan 1.98, +4 grain 2.43)
MIN_DETAIL = (
    0.045  # fine-band energy share, native crop (good 0.076, 2x upscale 0.031, free-route 0.026)
)
MAX_BLOCK = 1.40  # block-edge to inner gradient (good 1.23, q12 2.13, free-route 1.53)
MAX_HALO = 0.18  # fraction of edge pixels far brighter or darker than their opaque neighbours


def load(path):
    im = Image.open(path)
    alpha = None
    if im.mode in ("RGBA", "LA") or "transparency" in im.info:
        im = im.convert("RGBA")
        alpha = np.array(im.getchannel("A"))
    rgb = np.array(im.convert("RGB"))
    return rgb, alpha


def noise_sigma(gray):
    """Immerkaer fast noise estimate on a float grayscale image (0..255)."""
    k = np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]], dtype=np.float32)
    h, w = gray.shape
    conv = cv2.filter2D(gray, -1, k)[1:-1, 1:-1]
    return float(np.sum(np.abs(conv)) * np.sqrt(0.5 * np.pi) / (6.0 * (w - 2) * (h - 2)))


def detail_ratio(gray_native):
    """Share of spectral energy in the fine band, from a native-resolution center crop."""
    h, w = gray_native.shape
    s = min(512, h, w)
    y0, x0 = (h - s) // 2, (w - s) // 2
    crop = gray_native[y0 : y0 + s, x0 : x0 + s].astype(np.float32)
    crop = (crop - crop.mean()) * np.outer(np.hanning(s), np.hanning(s))
    mag = np.abs(np.fft.fftshift(np.fft.fft2(crop))) ** 2
    yy, xx = np.indices(mag.shape)
    r = np.hypot(yy - s / 2, xx - s / 2) / (s / 2)
    total = mag[r > 0.02].sum() + 1e-9
    return float(mag[r > 0.30].sum() / total)


def block_ratio(gray_native):
    g = gray_native.astype(np.float32)
    dx = np.abs(np.diff(g, axis=1))
    cols = np.arange(dx.shape[1])
    edge = dx[:, cols % 8 == 7].mean()
    inner = dx[:, cols % 8 != 7].mean() + 1e-6
    return float(edge / inner)


def halo_fraction(rgb, alpha):
    """Share of mid-transparency edge pixels far off the nearby subject colour."""
    if alpha is None:
        return 0.0
    solid = alpha > 245
    edge = (alpha >= 40) & (alpha <= 245)
    if edge.sum() < 50 or solid.sum() < 50:
        return 0.0
    lum = (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]).astype(np.float32)
    weight = cv2.GaussianBlur(solid.astype(np.float32), (0, 0), 12)
    local = cv2.GaussianBlur(np.where(solid, lum, 0).astype(np.float32), (0, 0), 12)
    local = local / np.maximum(weight, 1e-3)
    sel = edge & (weight > 0.05)
    if not sel.any():
        return 0.0
    return float((np.abs(lum - local)[sel] > 50).mean())


def analyze(path, role="asset"):
    rgb, alpha = load(path)
    h, w = rgb.shape[:2]
    long_side = max(h, w)
    mask = alpha > 200 if alpha is not None else None
    gray_native = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    if mask is not None and mask.sum() > 100:
        ys, xs = np.where(mask)
        gray_native = gray_native[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]
    scale = WORK / max(gray_native.shape)
    work = (
        cv2.resize(gray_native, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        if scale < 1
        else gray_native
    )
    m = {
        "size": f"{w}x{h}",
        "long_side": long_side,
        "noise": noise_sigma(work.astype(np.float32)),
        "detail": detail_ratio(gray_native),
        "block": block_ratio(gray_native),
        "halo": halo_fraction(rgb, alpha),
    }
    problems = []
    if long_side < MIN_LONG[role]:
        problems.append(f"too small: {long_side}px long side, {role} needs {MIN_LONG[role]}")
    if m["noise"] > MAX_NOISE:
        problems.append(f"grainy: noise {m['noise']:.2f} > {MAX_NOISE}")
    if m["detail"] < MIN_DETAIL:
        problems.append(f"soft or upscaled: detail {m['detail']:.4f} < {MIN_DETAIL}")
    if m["block"] > MAX_BLOCK:
        problems.append(f"JPEG blocking: {m['block']:.2f} > {MAX_BLOCK}")
    if m["halo"] > MAX_HALO:
        problems.append(f"edge halo on cutout: {m['halo']:.2f} > {MAX_HALO}")
    return m, problems


def selftest():
    if not os.path.exists(SAMPLE):
        print(f"selftest needs {SAMPLE}", file=sys.stderr)
        return 2
    import tempfile

    base = Image.open(SAMPLE).convert("RGB")
    base.thumbnail((2400, 2400))
    cases = {}
    tmp = tempfile.mkdtemp(prefix="iq-")

    def save(name, im, **kw):
        p = os.path.join(tmp, name)
        im.save(p, **kw)
        return p

    cases["good scan"] = (save("good.png", base), "asset", True)
    small = base.resize((base.width // 3, base.height // 3), Image.LANCZOS)
    up = small.resize(base.size, Image.BICUBIC)
    if os.path.exists(SAMPLE2):
        lemon = Image.open(SAMPLE2).convert("RGB")
        cases["good scan (independent)"] = (save("lemon.png", lemon), "asset", True)
        cases["real scan, 3x upscaled"] = (
            save(
                "lemon-up.png",
                lemon.resize((lemon.width // 3, lemon.height // 3), Image.LANCZOS).resize(
                    lemon.size, Image.BICUBIC
                ),
            ),
            "asset",
            False,
        )
    # cutouts: a soft-edged subject with clean edge colour (PASS) and with a white fringe (FAIL)
    h, w = base.height, base.width
    yy, xx = np.mgrid[0:h, 0:w]
    inside = (((xx - w / 2) / (w * 0.40)) ** 2 + ((yy - h / 2) / (h * 0.42)) ** 2) < 1
    soft = cv2.GaussianBlur(inside.astype(np.float32), (0, 0), 5)
    alpha = np.clip(soft * 255, 0, 255).astype(np.uint8)
    rgb = (np.array(base).astype(np.float32) * 0.45).astype(
        np.uint8
    )  # darker subject, as real motifs are
    clean = np.dstack([rgb, alpha])
    mix = (1 - soft)[..., None]
    fringe_rgb = np.clip(rgb * (1 - mix) + 255 * mix, 0, 255).astype(np.uint8)
    fringed = np.dstack([fringe_rgb, alpha])
    cases["cutout, clean edge"] = (
        save("cut-clean.png", Image.fromarray(clean, "RGBA")),
        "asset",
        True,
    )
    cases["cutout, white fringe"] = (
        save("cut-halo.png", Image.fromarray(fringed, "RGBA")),
        "asset",
        False,
    )
    cases["fake upscale"] = (save("up.png", up), "asset", False)
    arr = np.array(base).astype(np.float32)
    noisy = np.clip(arr + np.random.default_rng(3).normal(0, 9, arr.shape), 0, 255).astype(np.uint8)
    cases["grainy"] = (save("noisy.png", Image.fromarray(noisy)), "asset", False)
    cases["jpeg q12"] = (save("q12.jpg", base, quality=12), "asset", False)
    cases["too small"] = (save("tiny.png", base.resize((500, 500))), "asset", False)
    smoke = os.path.join(HERE, "..", "assets", "inbox", "_smoke-pollinations.jpg")
    if os.path.exists(smoke):
        cases["free-route smoke image"] = (smoke, "asset", False)
    bad = 0
    for name, (p, role, expect_pass) in cases.items():
        _, problems = analyze(p, role)
        passed = not problems
        ok = passed == expect_pass
        bad += not ok
        print(
            f"{'ok  ' if ok else 'WRONG'} {name:24s} expected {'PASS' if expect_pass else 'FAIL'} "
            f"got {'PASS' if passed else 'FAIL'}  {'; '.join(problems)[:90]}"
        )
    print("selftest:", "all verdicts correct" if bad == 0 else f"{bad} wrong verdict(s)")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image", nargs="?")
    ap.add_argument("--role", default="asset", choices=MIN_LONG)
    ap.add_argument("--metrics", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.image:
        ap.error("need IMAGE or --selftest")
    m, problems = analyze(a.image, a.role)
    if a.metrics:
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items()})
    if problems:
        print("FAIL " + a.image)
        for p in problems:
            print("  -", p)
        return 1
    print(f"PASS {a.image} ({m['size']}, {a.role})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
