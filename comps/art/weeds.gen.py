#!/usr/bin/env python3
# ruff: noqa: E501  (SVG path data and markup lines are long by nature)
"""Weeds around the names pane in comps/prototype.html (prototype r8b). owner: Tomas | 2026-11-10

Authored by the designer as control points; this script only turns them into SVG paths.
Units are pane units: one tile = 100, the pane is 0..400 x 0..200; the weeds svg viewBox is -60 -46 520 300.
Run: python3 -I comps/art/weeds.gen.py > out.svgpart, then paste between <!--WEEDS--> and </svg> in prototype.html.
Order of the reveal: stems draw (stroke-dashoffset), small ink details fade in, then colour and a faint shadow on the glaze.
"""

import math
import random
import re
import sys

R = random.Random(8)


def f(n):
    return f"{n:.1f}".rstrip("0").rstrip(".")


def cub(p0, p1, p2, p3, t):
    u = 1 - t
    return [
        u * u * u * p0[i] + 3 * u * u * t * p1[i] + 3 * u * t * t * p2[i] + t * t * t * p3[i]
        for i in (0, 1)
    ]


def parse(d):
    nums = list(map(float, re.findall(r"-?\d*\.?\d+", d)))
    p = nums[:2]
    segs = []
    k = 2
    while k + 6 <= len(nums):
        c = nums[k : k + 6]
        segs.append((p, c[0:2], c[2:4], c[4:6]))
        p = c[4:6]
        k += 6
    return segs


def at(segs, s):
    x = s * len(segs)
    i = min(int(x), len(segs) - 1)
    t = x - i
    a = cub(*segs[i], t)
    b = cub(*segs[i], min(1, t + 0.02))
    c = cub(*segs[i], max(0, t - 0.02))
    return a, math.atan2(b[1] - c[1], b[0] - c[0])


def leaf(p, ang, L, w, bend=0.18):
    tip = (p[0] + math.cos(ang) * L, p[1] + math.sin(ang) * L)
    m = (p[0] + math.cos(ang) * L * 0.5, p[1] + math.sin(ang) * L * 0.5)
    nx, ny = -math.sin(ang) * w, math.cos(ang) * w
    bx, by = -math.sin(ang) * L * bend, math.cos(ang) * L * bend
    return (
        f"M{f(p[0])} {f(p[1])}Q{f(m[0] + nx + bx)} {f(m[1] + ny + by)} {f(tip[0])} {f(tip[1])}"
        f"Q{f(m[0] - nx + bx * 0.5)} {f(m[1] - ny + by * 0.5)} {f(p[0])} {f(p[1])}Z"
    )


def blade(x, y, h, lean, droop=0.0):
    """a grass blade from (x, y), height h, leaning by lean, its tip drooping"""
    c1 = (x + lean * 0.15, y - h * 0.45)
    c2 = (x + lean * 0.7, y - h * 0.85)
    tip = (x + lean + droop, y - h + abs(droop) * 0.6)
    return f"M{f(x)} {f(y)}C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(tip[0])} {f(tip[1])}"


def sliver(d, k=3.2):
    n = list(map(float, re.findall(r"-?\d*\.?\d+", d)))
    x0, y0, x1, y1, x2, y2, x3, y3 = n
    return (
        f"M{f(x0 - k * 0.4)} {f(y0)}C{f(x1 - k * 0.3)} {f(y1)} {f(x2)} {f(y2)} {f(x3)} {f(y3)}"
        f"C{f(x2 + k * 0.5)} {f(y2 + 1)} {f(x1 + k * 0.6)} {f(y1)} {f(x0 + k * 0.6)} {f(y0)}Z"
    )


def petals(cx, cy, n, r0, r1, w, squash, rot, droop=0.0):
    out = []
    for k in range(n):
        a = rot + 2 * math.pi * k / n + R.uniform(-0.12, 0.12)
        L = r1 * R.uniform(0.82, 1.08)
        ca, sa = math.cos(a), math.sin(a)
        b = (cx + ca * r0, cy + sa * r0 * squash)
        tip = (cx + ca * L, cy + sa * L * squash + droop * (1 - abs(sa)) * L * 0.25)
        nx, ny = -sa * w, ca * w * squash
        m1 = (b[0] + (tip[0] - b[0]) * 0.55 + nx, b[1] + (tip[1] - b[1]) * 0.55 + ny)
        m2 = (b[0] + (tip[0] - b[0]) * 0.55 - nx, b[1] + (tip[1] - b[1]) * 0.55 - ny)
        out.append(
            f"M{f(b[0])} {f(b[1])}Q{f(m1[0])} {f(m1[1])} {f(tip[0])} {f(tip[1])}Q{f(m2[0])} {f(m2[1])} {f(b[0])} {f(b[1])}Z"
        )
    return "".join(out)


def reflexed(cx, cy, n, L):
    """a chamomile seen from the side: the petals fold down under the dome"""
    out = []
    for k in range(n):
        x = cx - 4.2 + 8.4 * k / (n - 1)
        a = math.radians(90 + (x - cx) * 9 + R.uniform(-8, 8))
        tip = (x + math.cos(a) * L * R.uniform(0.8, 1.05), cy + 1 + math.sin(a) * L)
        out.append(f"M{f(x)} {f(cy + 1)}L{f(tip[0])} {f(tip[1])}")
    return "".join(out)


# ---------- left: grass at the foot of the wall, uneven, some blades bent over ----------
GR = [
    blade(-2, 226, 64, -16, -6),
    blade(8, 222, 40, 9),
    blade(15, 228, 74, -4, -10),
    blade(22, 224, 30, 13, 4),
    blade(31, 227, 52, 15, 7),
    blade(46, 225, 26, -8),
    blade(55, 229, 44, 22, 9),
    blade(70, 226, 22, 12),
]
OAT = "M37 228C41 196 47 156 45 118"
CH_A = "M60 228C58 202 66 176 79 152"  # frontal head, tilted
CH_B = "M63 205C56 197 51 188 49 179"  # profile head, petals folded down
BUD = "M66 214C76 209 84 202 89 192"
# right: two blades, the wild pea climbing the side and nodding over the top corner (no curl)
RG = [blade(404, 230, 30, -14, -4), blade(414, 232, 22, 10), blade(424, 230, 36, 18, 6)]
PEA = "M413 232C419 206 411 184 416 160C421 136 408 116 412 92C415 70 404 50 400 34C396 18 386 6 374 3C367 1 361 3 357 8"

ink = [(d, 0.32 + 0.004 * abs(len(d)), 2.6 + 0.05 * i) for i, d in enumerate(GR)]
ink += [(OAT, 0.6, 2.85), (CH_A, 0.55, 3.0), (CH_B, 0.35, 3.2), (BUD, 0.35, 3.25)]
ink += [(d, 0.35, 3.35 + 0.05 * i) for i, d in enumerate(RG)]
ink.append((PEA, 0.95, 3.5))

headA = (80.5, 148.5)
headB = (48.5, 176)
petA = petals(*headA, 12, 3.6, 12.5, 2.3, 0.55, 0.15)
petB = reflexed(*headB, 7, 7.5)
domeA = f"M{f(headA[0] - 4.6)} {f(headA[1])}C{f(headA[0] - 4)} {f(headA[1] - 4.6)} {f(headA[0] + 4)} {f(headA[1] - 4.6)} {f(headA[0] + 4.6)} {f(headA[1])}C{f(headA[0] + 3)} {f(headA[1] + 2.4)} {f(headA[0] - 3)} {f(headA[1] + 2.4)} {f(headA[0] - 4.6)} {f(headA[1])}Z"
domeB = f"M{f(headB[0] - 4.4)} {f(headB[1] + 1)}C{f(headB[0] - 4)} {f(headB[1] - 5.4)} {f(headB[0] + 4)} {f(headB[1] - 5.4)} {f(headB[0] + 4.4)} {f(headB[1] + 1)}Z"
fern = (
    "M60 214L53 210M57 212L56 206M59 201L52 198M64 191L71 186M67 189L68 183M66 181L60 178"
    "M71 168L77 164M74 166L74 160M54 189L48 187M82 202L86 197"
)
oat_segs = parse(OAT)
oat_sp = []
for s, side, L in [(0.99, 1, 9), (0.93, -1, 10), (0.86, 1, 10), (0.79, -1, 9), (0.72, 1, 8)]:
    p, a = at(oat_segs, s)
    q = (p[0] + side * 3.2, p[1] + 1.5)
    oat_sp.append(
        f"M{f(p[0])} {f(p[1])}L{f(q[0])} {f(q[1])}"
        + leaf(q, math.radians(90 + side * -28), L, 2.4, 0)
    )
oat_sp = "".join(oat_sp)
pea_segs = parse(PEA)
pea_leaves = []
for s, side, L, w in [
    (0.05, -1, 13, 3.4),
    (0.11, 1, 12, 3.3),
    (0.19, -1, 12, 3.2),
    (0.26, 1, 11, 3.1),
    (0.36, -1, 11, 3),
    (0.45, 1, 9, 2.7),
    (0.6, -1, 8, 2.5),
    (0.72, 1, 8, 2.4),
    (0.86, -1, 7, 2.2),
]:
    p, a = at(pea_segs, s)
    pea_leaves.append(leaf(p, a + side * math.radians(50) + R.uniform(-0.2, 0.2), L, w))
pea_leaves = "".join(pea_leaves)
fp, fa = at(pea_segs, 0.4)
flower = (
    f"M{f(fp[0])} {f(fp[1])}C{f(fp[0] + 5)} {f(fp[1] - 9)} {f(fp[0] + 15)} {f(fp[1] - 10)} {f(fp[0] + 15)} {f(fp[1] - 3)}"
    f"C{f(fp[0] + 16)} {f(fp[1] + 3)} {f(fp[0] + 8)} {f(fp[1] + 5)} {f(fp[0])} {f(fp[1])}Z"
)
keel = (
    f"M{f(fp[0])} {f(fp[1])}C{f(fp[0] + 6)} {f(fp[1] + 2)} {f(fp[0] + 10)} {f(fp[1] + 6)} {f(fp[0] + 8)} {f(fp[1] + 9)}"
    f"C{f(fp[0] + 5)} {f(fp[1] + 8)} {f(fp[0] + 2)} {f(fp[1] + 5)} {f(fp[0])} {f(fp[1])}Z"
)

o = []
o.append(
    '<g class="shadow" fill="none" stroke="#3B2F25" stroke-opacity=".06" stroke-width="2.6" stroke-linecap="round" transform="translate(2.4 3.2)">'
)
o.append(
    '<path d="M42 200C45 170 47 140 45 118"/><path d="M64 200C66 184 71 166 79 152"/><path d="M412 92C415 70 404 50 400 34C396 18 386 6 374 3"/>'
)
o.append("</g>")
o.append('<g class="wash">')
for i, d in enumerate(GR + RG):
    o.append(
        f'<path fill="{"#9DAE82" if i % 3 else "#B5C29A"}" fill-opacity="{0.4 + 0.1 * (i % 3)}" d="{sliver(d)}"/>'
    )
o.append(
    f'<path fill="#FBF8F0" stroke="#FBF8F0" stroke-width="1" stroke-linejoin="round" d="{petA}"/>'
)
o.append(
    f'<path fill="#E2C36A" d="{domeA}{domeB}"/><circle cx="88.6" cy="191" r="2.4" fill="#C7D09F"/>'
)
o.append(
    f'<path fill="#9DAE82" fill-opacity=".7" d="{pea_leaves}"/><path fill="#D8C68C" fill-opacity=".65" d="{oat_sp}"/>'
)
o.append(f'<path fill="#E7C3B2" d="{flower}"/><path fill="#C98B6B" fill-opacity=".65" d="{keel}"/>')
o.append("</g>")
o.append('<g class="ink drawable" data-px=".9">')
for d, t, dl in ink:
    o.append(f'<path pathLength="1" style="--t:{t:.2f}s;--d:{dl:.2f}s" d="{d}"/>')
o.append("</g>")
o.append('<g class="det" fill="none" style="--d:3.45s">')
o.append(
    f'<path d="{oat_sp}" stroke-opacity=".7"/><path d="{petA}" stroke-opacity=".35"/><path d="{petB}" stroke-opacity=".6"/>'
)
o.append(
    f'<path d="{domeA}{domeB}" stroke-opacity=".45"/><path d="M86.5 193.5L85 196M90.8 193.5L92.3 196" stroke-opacity=".6"/>'
)
o.append(f'<path d="{fern}" stroke-opacity=".7"/>')
o.append("</g>")
o.append('<g class="det" fill="none" style="--d:4.45s">')
o.append(
    f'<path d="{pea_leaves}" stroke-opacity=".6"/><path d="{flower}{keel}" stroke-opacity=".6"/>'
)
o.append("</g>")
sys.stdout.write("\n".join(o) + "\n")
