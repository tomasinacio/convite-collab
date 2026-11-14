#!/usr/bin/env python3
"""Build the single-file v10 page: inline every DATA:<path> placeholder as a base64 data URI.

owner: Tomas | review date: 2026-11-18
canonical path: projects/wedding-invite/comps/art/v10_build.py
rollback: rm projects/wedding-invite/comps/art/v10_build.py

Usage: .venv/bin/python -I comps/art/v10_build.py [SRC] [OUT]
  SRC defaults to comps/prototype.v10.opening.src.html (readable working source)
  OUT defaults to comps/prototype.v10.opening.single.html
  Placeholders look like url("DATA:art/v10/src/05-img-sky.webp"); paths are relative to comps/.
  Check: building the untouched upload's source reproduces comps/prototype.v10.orig.single.html.
"""

import base64
import os
import re
import sys

COMPS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MIME = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml"}


def inline(src_text):
    cache = {}

    def uri(m):
        rel = m.group(1)
        if rel not in cache:
            data = open(os.path.join(COMPS, rel), "rb").read()
            mime = MIME[os.path.splitext(rel)[1]]
            cache[rel] = f"data:{mime};base64," + base64.b64encode(data).decode()
        return cache[rel]

    out = re.sub(r"DATA:([A-Za-z0-9_./-]+)", uri, src_text)
    return out, cache


def main():
    args = sys.argv[1:]
    src = args[0] if args else os.path.join(COMPS, "prototype.v10.opening.src.html")
    out = args[1] if len(args) > 1 else os.path.join(COMPS, "prototype.v10.opening.single.html")
    text, used = inline(open(src, encoding="utf-8").read())
    left = re.search(r"url\(\"?DATA", text)
    if left:
        sys.exit(f"unresolved placeholder at {left.start()}")
    open(out, "w", encoding="utf-8").write(text)
    print(f"{os.path.relpath(out, COMPS)}: {len(text) // 1024} KB, {len(used)} images inlined")


if __name__ == "__main__":
    main()
