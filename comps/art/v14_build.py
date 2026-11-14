#!/usr/bin/env python3
"""Build prototype.v14 (the open page, lane B): prepare new art, inline everything into one file.

owner: Tomas | review date: 2026-11-18
canonical path: projects/wedding-invite/comps/art/v14_build.py
rollback: rm projects/wedding-invite/comps/art/v14_build.py

Usage: .venv/bin/python -I comps/art/v14_build.py [--inbox DIR]
  As v13_build.py (it reuses its cutting of assets/inbox/new-art/ into comps/art/v13/), plus:
  every optional DATA?:<path> placeholder whose file exists is inlined and its file name
  (without extension) is added to data-art, so lane outputs (for example
  comps/art/v14/citrus-branch.webp from lane C) switch on by being dropped in place; a missing
  file becomes `none` and its slot stays hidden. Lane A's front-page CSS, when it exists at
  comps/v14-front.css, is inlined at the LANE A MERGE SLOT.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v10_build import inline  # noqa: E402
from v13_build import ROOT, prepare  # noqa: E402

COMPS = os.path.join(HERE, "..")


def main():
    args = sys.argv[1:]
    inbox = (
        args[args.index("--inbox") + 1]
        if "--inbox" in args
        else os.path.join(ROOT, "assets", "inbox", "new-art")
    )
    src = os.path.join(COMPS, "prototype.v14.src.html")
    out = os.path.join(COMPS, "prototype.v14.single.html")
    prepare(inbox)
    text = open(src, encoding="utf-8").read()
    present = []

    def optional(m):
        path = os.path.join(COMPS, m.group(1))
        if os.path.exists(path):
            present.append(os.path.splitext(os.path.basename(path))[0])
            return f'url("DATA:{m.group(1)}")'
        return "none"

    text = re.sub(r'url\("DATA\?:([^"]+)"\)', optional, text)
    text = text.replace("DATA-ART-FLAGS", " ".join(sorted(set(present))))
    front = os.path.join(COMPS, "v14-front.css")
    slot = "/* LANE A MERGE SLOT: comps/v14-front.css is inlined here by v14_build.py */"
    if os.path.exists(front) and slot in text:
        text = text.replace(slot, slot + "\n" + open(front, encoding="utf-8").read())
    text, used = inline(text)
    if re.search(r'url\("?DATA', text):
        sys.exit("unresolved placeholder")
    open(out, "w", encoding="utf-8").write(text)
    print(f"prototype.v14.single.html: {len(text) // 1024} KB, {len(used)} images")
    print(f"slots filled: {' '.join(sorted(set(present)))}")


if __name__ == "__main__":
    main()
