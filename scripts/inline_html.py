#!/usr/bin/env python3
"""Inline local images into an HTML file as data URIs so it works as one shareable page.

owner: Tomas | review date: 2026-11-10
canonical path: projects/wedding-invite/scripts/inline_html.py
rollback: rm -f projects/wedding-invite/scripts/inline_html.py

Usage: inline_html.py IN.html OUT.html [--max-width 900]
Every src="relative/path.(webp|png|jpg)" is resized to at most --max-width pixels wide
(keeps alpha) and embedded. Remote URLs are left alone. Prints the output size.
"""

import argparse
import base64
import io
import os
import re
import sys

from PIL import Image

MIME = {"webp": "image/webp", "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}


def encode(path, max_width):
    im = Image.open(path)
    if im.width > max_width:
        im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)
    ext = path.rsplit(".", 1)[-1].lower()
    buf = io.BytesIO()
    if ext in ("webp", "png"):
        im.save(buf, "WEBP", quality=88, method=6)
        ext = "webp"
    else:
        im.convert("RGB").save(buf, "JPEG", quality=90)
    return f"data:{MIME[ext]};base64," + base64.b64encode(buf.getvalue()).decode()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--max-width", type=int, default=900)
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.src))
    text = open(a.src).read()

    def repl(m):
        rel = m.group(2)
        if re.match(r"^(https?:|data:|//)", rel):
            return m.group(0)
        path = os.path.normpath(os.path.join(base, rel))
        if not os.path.exists(path):
            print(f"missing: {rel}", file=sys.stderr)
            return m.group(0)
        return f'{m.group(1)}"{encode(path, a.max_width)}"'

    out = re.sub(r"""(src=)["']([^"']+\.(?:webp|png|jpe?g))["']""", repl, text)
    out = re.sub(
        r"""(url\()["']?(\.\./[^"')]+\.(?:webp|png|jpe?g))["']?\)""",
        lambda m: f'url("{encode(os.path.normpath(os.path.join(base, m.group(2))), a.max_width)}")',
        out,
    )
    with open(a.dst, "w") as f:
        f.write(out)
    print(f"{a.dst}: {len(out) / 1e6:.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
