#!/usr/bin/env python3
"""WCAG contrast check for the invitation palette.

owner: Tomas | review date: 2026-11-09
canonical path: projects/wedding-invite/scripts/contrast.py
rollback: rm -f projects/wedding-invite/scripts/contrast.py

Usage: contrast.py            check the built-in text pairs (exit 1 if any is under 4.5)
       contrast.py FG BG      print one ratio, e.g. contrast.py '#4F5F2E' '#F6EFDF'
"""

import sys


def lum(h: str) -> float:
    h = h.lstrip("#")
    c = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a: str, b: str) -> float:
    x, y = lum(a), lum(b)
    if x < y:
        x, y = y, x
    return (x + 0.05) / (y + 0.05)


TEXT_PAIRS = [
    ("ink on paper", "#3B2F25", "#F6EFDF"),
    ("deep olive on paper", "#4F5F2E", "#F6EFDF"),
    ("brown on paper", "#6B4F34", "#F6EFDF"),
    ("terracotta on paper", "#9A4C32", "#F6EFDF"),
    ("ink on sand", "#3B2F25", "#E6D6B8"),
    ("brown on sand", "#6B4F34", "#E6D6B8"),
    ("paper on deep olive", "#F6EFDF", "#4F5F2E"),
    ("paper on terracotta", "#F6EFDF", "#9A4C32"),
]


def main() -> int:
    if len(sys.argv) == 3:
        print(f"{ratio(sys.argv[1], sys.argv[2]):.2f}:1")
        return 0
    bad = 0
    for name, fg, bg in TEXT_PAIRS:
        r = ratio(fg, bg)
        ok = r >= 4.5
        bad += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {r:5.2f}:1  {name}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
