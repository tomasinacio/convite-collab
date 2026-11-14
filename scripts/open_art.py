#!/usr/bin/env python3
"""Find and download real public-domain artwork from Wikimedia Commons (no key).

owner: Tomas | review date: 2026-11-10
canonical path: projects/wedding-invite/scripts/open_art.py
rollback: rm -f projects/wedding-invite/scripts/open_art.py

Usage:
  open_art.py search "Pomological Watercolor lemon" [--limit 12] [--min-long 2400] [--sheet OUT.jpg]
  open_art.py get "File:Pomological Watercolor POM00006810.jpg" lemon-plate.jpg

Only public-domain and CC0 files are downloaded by default. Files that need credit
(CC BY, CC BY-SA) need --allow-attribution, and the credit is logged. Everything
downloaded goes to assets/inbox/ and gets a row in assets/LOG.md with source URL,
license and author. Good starting collections: the USDA Pomological Watercolor
Collection (fruit, 4000 px tall), Edwards's Botanical Register, Redoute plates.
"""

import argparse
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import date

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "wedding-invite-open-art/1.0 (personal wedding project)"}
HERE = os.path.dirname(os.path.abspath(__file__))
INBOX = os.path.join(HERE, "..", "assets", "inbox")
LOG = os.path.join(HERE, "..", "assets", "LOG.md")
FREE = re.compile(r"^(public domain|pd\b|pd-|cc0)", re.I)
ATTR = re.compile(r"^cc[ -]by(-sa)?\b", re.I)


def call(params):
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json"})
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def _val(m, k):
    return html.unescape(re.sub(r"<[^>]+>", "", m.get(k, {}).get("value", ""))).strip()


def info(pages):
    out = []
    for p in pages:
        ii = (p.get("imageinfo") or [None])[0]
        if not ii:
            continue
        m = ii.get("extmetadata", {})
        out.append(
            {
                "title": p["title"],
                "w": ii["width"],
                "h": ii["height"],
                "url": ii["url"],
                "page": ii.get("descriptionurl", ""),
                "license": _val(m, "LicenseShortName"),
                "artist": _val(m, "Artist")[:80],
                "mime": ii.get("mime", ""),
                "thumb": ii.get("thumburl", ""),
            }
        )
    return out


def search(a):
    d = call(
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": a.query + " filetype:bitmap",
            "gsrnamespace": 6,
            "gsrlimit": a.limit,
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "iiurlwidth": 280,
        }
    )
    rows = info(d.get("query", {}).get("pages", {}).values())
    rows = [r for r in rows if max(r["w"], r["h"]) >= a.min_long]
    for r in sorted(rows, key=lambda r: r["title"]):
        ok = (
            "free" if FREE.match(r["license"]) else ("credit" if ATTR.match(r["license"]) else "no")
        )
        print(f"{r['title']} | {r['w']}x{r['h']} | {r['license']} [{ok}] | {r['artist']}")
    if not rows:
        print("no results at that size; lower --min-long or change the query")
    elif a.sheet:
        sheet(sorted(rows, key=lambda r: r["title"]), a.sheet)
    return 0


def sheet(rows, out):
    """Contact sheet: thumbnails with file names, so the picker can choose by eye."""
    import io

    from PIL import Image, ImageDraw

    cols, tw, th, pad = 4, 280, 380, 8
    n = len(rows)
    img = Image.new(
        "RGB",
        (cols * (tw + pad) + pad, ((n + cols - 1) // cols) * (th + 34 + pad) + pad),
        "#F6EFDF",
    )
    d = ImageDraw.Draw(img)
    for i, r in enumerate(rows):
        x, y = pad + (i % cols) * (tw + pad), pad + (i // cols) * (th + 34 + pad)
        try:
            with urllib.request.urlopen(
                urllib.request.Request(r["thumb"], headers=UA), timeout=60
            ) as resp:
                im = Image.open(io.BytesIO(resp.read())).convert("RGB")
            im.thumbnail((tw, th))
            img.paste(im, (x + (tw - im.width) // 2, y))
        except OSError:
            d.text((x + 10, y + 10), "thumbnail failed", fill="#9A4C32")
        d.text((x, y + th + 4), r["title"].replace("File:", "")[:44], fill="#3B2F25")
        d.text((x, y + th + 18), f"{r['w']}x{r['h']}  {r['license']}"[:44], fill="#6B4F34")
    img.save(out, quality=90)
    print(f"contact sheet: {out}")


def get(a):
    d = call(
        {
            "action": "query",
            "titles": a.title,
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
        }
    )
    rows = info(d.get("query", {}).get("pages", {}).values())
    if not rows:
        print("file not found", file=sys.stderr)
        return 1
    r = rows[0]
    free, attr = bool(FREE.match(r["license"])), bool(ATTR.match(r["license"]))
    if not (free or (attr and a.allow_attribution)):
        print(f"refused: license is '{r['license']}'", file=sys.stderr)
        return 2
    os.makedirs(INBOX, exist_ok=True)
    dst = os.path.join(INBOX, a.out)
    req = urllib.request.Request(r["url"], headers=UA)
    with urllib.request.urlopen(req, timeout=180) as resp, open(dst, "wb") as f:
        f.write(resp.read())
    note = "no credit needed" if free else f"CREDIT REQUIRED: {r['artist']} ({r['license']})"
    row = (
        f"| `inbox/{a.out}` | Wikimedia Commons | {r['title']} | {date.today()} | n/a (found, "
        f"{r['w']}x{r['h']}) | {r['license']}; {note}; {r['page']} | candidate |\n"
    )
    with open(LOG, "a") as f:
        f.write(row)
    print(f"{dst}: {r['w']}x{r['h']} {r['license']} (logged)")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=12)
    s.add_argument("--min-long", type=int, default=2000)
    s.add_argument("--sheet", help="write a contact sheet image of the results")
    g = sub.add_parser("get")
    g.add_argument("title")
    g.add_argument("out")
    g.add_argument("--allow-attribution", action="store_true")
    a = ap.parse_args()
    return search(a) if a.cmd == "search" else get(a)


if __name__ == "__main__":
    sys.exit(main())
