#!/usr/bin/env python3
"""Build the hosting-ready static site: site/ from comps/prototype.v15.src.html.

owner: Tomas | review date: 2026-11-19
canonical path: projects/wedding-invite/comps/art/site_build.py
rollback: rm projects/wedding-invite/comps/art/site_build.py && rm -rf projects/wedding-invite/site comps/art/site

Usage: .venv/bin/python -I comps/art/site_build.py [--inbox DIR] [--base-url https://example.pt/]
  Same preparation as v15_build.py (v13_build.prepare, the optional DATA?: slots, lane A's
  comps/v14-front.css at its slot) but nothing is inlined. Output, all under site/:
    index.html            the page; the head has the tiny tier script inline, the rest is linked
    app.<hash>.css        the page CSS (comments stripped) with the @font-face rules in front
    app.<hash>.js         the page script (blobArt, which swapped base64 for blob: URLs, is removed)
    img/<name>.<hash>.webp  every url("DATA:path") of the source, relative URLs (works at a root or a sub-path)
    fonts/*.<hash>.woff2  Allura and EB Garamond, Latin subset, from comps/art/site/fonts/ (SIL OFL 1.1)
    _headers robots.txt 404.html favicon.png apple-touch-icon.png og-image.jpg
  site/README.md is hand-written and survives a rebuild; everything else in site/ is regenerated.
  With the RSVP on, rsvp/page/info.{html,css,js} (the information sections) are built in with it: the html replaces the
  face's <!--@@INFO@@--> slot (prototype.v16.src.html), or goes after </main> before the RSVP for a face without the slot.
  A default build (RSVP off) only drops the empty slot.
  comps/art/site/og-image.jpg (1200 x 630, cropped from the closed front) is a stored input.
  --base-url makes og:image and og:url absolute (needed once the domain is known).
"""

# ruff: noqa: E501
import hashlib
import html
import json
import os
import re
import shutil
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v13_build import COMPS, ROOT, prepare  # noqa: E402

SITE = os.path.join(ROOT, "site")
RSVP_DIR = os.path.join(ROOT, "rsvp")
SRC = os.path.join(COMPS, "prototype.v15.src.html")
STATIC = os.path.join(HERE, "site")
KEEP = {"README.md"}
# the closed front: what the guest sees before the tap (preloaded, then decoded by app.js)
CLOSED = ("paper", "closed-top", "closed-bottom", "closed-emboss", "closed-deco", "seal", "linen")
FONTS = [  # file, family, style, weight range, preloaded (the italic seal label is above the fold)
    ("allura-latin", "Allura", "normal", "400", False),
    ("ebgaramond-latin", "EB Garamond", "normal", "400 600", False),
    ("ebgaramond-italic-latin", "EB Garamond", "italic", "400", True),
]

# if the closed front's art fails to load, the names printed on the middle sheet must not show through the bare flaps
FAILSAFE_CSS = ".art-failed .page:not(.opened) .print{visibility:hidden}\n"
# JavaScript off: the painted page shows (html:not(.js) in the CSS); the names, which the script draws letter by letter, show as plain text
NOSCRIPT = """<noscript><style>
.vh{position:static;width:auto;height:auto;overflow:visible;clip-path:none;white-space:normal;display:flex;flex-direction:column;align-items:center;
  font-family:var(--serif);font-weight:600;color:var(--az-ink);font-size:11.2cqw;line-height:1.05;letter-spacing:.04em;text-transform:uppercase}
.vh span:nth-child(2){font-style:italic;font-weight:400;font-size:.8em;text-transform:none}
.skip,.seal,.sheet,.again{display:none}
</style></noscript>
"""


def digest(data):
    return hashlib.sha256(data).hexdigest()[:8]


def must_sub(pattern, repl, text, flags=0):
    new, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        sys.exit(f"site_build: expected one match for {pattern[:60]!r}")
    return new


def write(rel, data):
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(
        path,
        "wb" if isinstance(data, bytes) else "w",
        **({} if isinstance(data, bytes) else {"encoding": "utf-8"}),
    ) as f:
        f.write(data)


def clean():
    os.makedirs(SITE, exist_ok=True)
    for name in os.listdir(SITE):
        if name in KEEP:
            continue
        p = os.path.join(SITE, name)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)


def rsvp_load(args):
    """The RSVP section (rsvp/page/*) is built in only when rsvp/rsvp-config.json has enabled true.
    --rsvp-config PATH uses another config (for tests). A real build refuses while any FAKE placeholder is left;
    --allow-fake lets a test build through."""
    path = (
        args[args.index("--rsvp-config") + 1]
        if "--rsvp-config" in args
        else os.path.join(RSVP_DIR, "rsvp-config.json")
    )
    if not os.path.exists(path):
        return None
    cfg = json.load(open(path, encoding="utf-8"))
    if cfg.get("enabled") is not True:
        return None
    api = str(cfg.get("api", ""))
    if not (api == "" and "--allow-fake" in args) and not re.fullmatch(
        r"(https://[A-Za-z0-9.-]+|http://(localhost|127\.0\.0\.1):\d+|http://[a-z0-9-]+(\.[a-z0-9-]+)*\.ts\.net)",
        api,
    ):
        sys.exit(
            "site_build: rsvp-config.json api must be https://host (no path, no slash at the end)"
        )
    page = os.path.join(RSVP_DIR, "page")
    parts = {
        n: open(os.path.join(page, n), encoding="utf-8").read()
        for n in ("rsvp.css", "rsvp.html", "rsvp.js", "info.css", "info.html", "info.js")
    }
    parts["wa_html"], parts["whatsapp_ok"] = whatsapp_links(cfg)
    left = (
        sum(parts[n].count("data-fake") for n in ("rsvp.html", "info.html"))
        + sum(parts[n].count("FAKE") for n in ("rsvp.js", "info.js"))
        + (0 if parts["whatsapp_ok"] else 1)
    )
    if left and "--allow-fake" not in args:
        sys.exit(
            f"site_build: the RSVP still has {left} FAKE placeholders (see rsvp/comps/REPLACE-ME.md); replace them or pass --allow-fake for a test build"
        )
    if left:
        print(f"warning: RSVP built with {left} FAKE placeholders (test build)")
    parts["cfg"] = json.dumps({"api": api})
    return parts


def whatsapp_links(cfg):
    """The contact buttons that replace @@WA@@ in rsvp.html. whatsapp is one https address or a list of them, whatsapp_names
    the label of each (a first name). Anything missing gives one placeholder button, counted as a FAKE."""
    urls = cfg.get("whatsapp", "")
    urls = urls if isinstance(urls, list) else [urls]
    names = cfg.get("whatsapp_names", [])
    names = names if isinstance(names, list) else [names]
    ok = bool(urls) and all(
        isinstance(u, str) and re.fullmatch(r"https://wa\.me/\d{6,15}", u) for u in urls
    )
    if not ok:
        return (
            '<a class="btn solid" href="#whatsapp-TODO" data-i18n="wa" data-fake>WhatsApp</a>',
            False,
        )
    icon = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
        '<path d="M4.5 19.5l1.2-3.6A7.5 7.5 0 1 1 8.4 18.6z"/></svg>'
    )
    out = []
    for i, u in enumerate(urls):
        name = html.escape(str(names[i])) if i < len(names) else "WhatsApp"
        out.append(
            f'<a class="btn{" solid" if i == 0 else ""} wa" href="{html.escape(u)}" target="_blank" rel="noopener">'
            f'{icon}<span class="rvh">WhatsApp: </span><span translate="no">{name}</span></a>'
        )
    return "".join(out), True


def art_ref(rel):
    """@@ART:path@@ in info.css names a file under comps/ that the face may not ship (new painted assets)."""
    path = os.path.join(COMPS, rel)
    if not os.path.isfile(path):
        sys.exit(f"site_build: info.css names art {rel!r}, which is missing")
    data = open(path, "rb").read()
    stem, ext = os.path.splitext(os.path.basename(rel))
    return f"img/{stem}.{digest(data)}{ext}", data


def main():
    global SITE
    args = sys.argv[1:]
    if "--out" in args:
        SITE = os.path.abspath(args[args.index("--out") + 1])
    rsvp = rsvp_load(args)
    inbox = (
        args[args.index("--inbox") + 1]
        if "--inbox" in args
        else os.path.join(ROOT, "assets", "inbox", "new-art")
    )
    base = args[args.index("--base-url") + 1].rstrip("/") + "/" if "--base-url" in args else ""
    prepare(inbox)
    src = (
        args[args.index("--src") + 1] if "--src" in args else SRC
    )  # --src PATH builds another face source (for example prototype.v16.src.html)
    text = open(src, encoding="utf-8").read()
    face_fake = text.count("data-fake")
    if rsvp and face_fake and "--allow-fake" not in args:
        sys.exit(
            f"site_build: the face source still has {face_fake} data-fake marker(s) (see rsvp/comps/REPLACE-ME.md); replace them or pass --allow-fake for a test build"
        )

    # --- the optional DATA?: slots, as v15_build.py ---
    present = []

    def optional(m):
        path = os.path.join(COMPS, m.group(1))
        if os.path.exists(path):
            present.append(os.path.splitext(os.path.basename(path))[0])
            return f'url("DATA:{m.group(1)}")'
        return "none"

    text = re.sub(r'url\("DATA\?:([^"]+)"\)', optional, text)
    text = text.replace("DATA-ART-FLAGS", " ".join(sorted(set(present))))

    # --- split the source: css, blobArt script (dropped), main script ---
    css = re.search(r"<style>\n(.*?)</style>", text, re.S).group(1)
    front = os.path.join(COMPS, "v14-front.css")
    slot = "/* LANE A MERGE SLOT: comps/v14-front.css is inlined here by v15_build.py */"
    if os.path.exists(front) and slot in css:
        css = css.replace(slot, slot + "\n" + open(front, encoding="utf-8").read())
    text = must_sub(
        r"<style>\n.*?</style>\n<script>\n/\* v15 \(critic 4\).*?</script>\n",
        "@@CSS@@\n",
        text,
        re.S,
    )
    text = must_sub(
        r"[ \t]*if \(!page\.classList\.contains\('opened'\)\) blobArt\(\);[^\n]*\n", "", text
    )
    main_js = re.search(r"<script>\n(\(function\(\)\{\n  var T = .*?)</script>", text, re.S).group(
        1
    )
    text = text.replace("<script>\n" + main_js + "</script>", "@@JS@@")
    if "blobArt" in text or "blobArt" in main_js:
        sys.exit("site_build: blobArt still referenced")
    # decode the closed front's art on its real URLs the moment the script runs (before the tap)
    names = ", ".join(f"'--img-{n}'" for n in CLOSED + ("seal-top", "seal-bottom"))
    predecode = (
        "  /* static build: decode the closed front's art on its real URLs as soon as the script runs, so the letter's first paint\n"
        "     and the tap frame do no decode (the files are preloaded by index.html) */\n"
        "  (function(){ var cs = getComputedStyle(document.documentElement);\n"
        f"    [{names}].forEach(function(v){{\n"
        "      var m = /url\\([\"']?([^\"')]+)[\"']?\\)/.exec(cs.getPropertyValue(v)); if (!m) return;\n"
        "      var im = new Image(); im.onerror = function(){ document.documentElement.classList.add('art-failed'); };\n"
        "      im.src = new URL(m[1], document.baseURI).href; if (im.decode) im.decode().catch(function(){}); }); })();\n"
    )
    main_js = must_sub(r"  var timed = false;\n", lambda m: predecode + m.group(0), main_js)

    # --- images: url("DATA:path") -> img/<stem>.<hash>.<ext>, relative ---
    copied = {}

    def img(m):
        rel = m.group(1)
        if rel not in copied:
            data = open(os.path.join(COMPS, rel), "rb").read()
            stem, ext = os.path.splitext(os.path.basename(rel))
            copied[rel] = (f"img/{stem}.{digest(data)}{ext}", data)
        return copied[rel][0]

    css = re.sub(r"DATA:([A-Za-z0-9_./-]+)", img, css)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\n\s*\n+", "\n", css).strip() + "\n"
    css += FAILSAFE_CSS
    if re.search(r"DATA|data:|blob:|base64", css + main_js):
        sys.exit("site_build: data/blob/placeholder left in css or js")

    # --- fonts: self-hosted, font-display swap ---
    clean()
    faces, preload = [], []
    for stem, family, style, weight, early in FONTS:
        data = open(os.path.join(STATIC, "fonts", stem + ".woff2"), "rb").read()
        rel = f"fonts/{stem}.{digest(data)}.woff2"
        write(rel, data)
        faces.append(
            f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};"
            f"font-display:swap;src:url({rel}) format('woff2')}}\n"
        )
        if early:
            preload.append(
                f'<link rel="preload" href="{rel}" as="font" type="font/woff2" crossorigin>\n'
            )
    css = "".join(faces) + css
    for rel, data in copied.values():
        write(rel, data)
    css_name = f"app.{digest(css.encode())}.css"
    js_name = f"app.{digest(main_js.encode())}.js"
    write(css_name, css)
    write(js_name, main_js)
    rsvp_tags = ("", "")
    if rsvp:

        def rimg(m):
            hits = [
                r for r, _ in copied.values() if os.path.basename(r).startswith(m.group(1) + ".")
            ]
            if not hits:
                sys.exit(
                    f"site_build: RSVP css needs image {m.group(1)!r}, which the face does not ship"
                )
            return hits[0]

        def aimg(m):
            rel, data = art_ref(m.group(1))
            write(rel, data)
            return rel

        rcss = re.sub(r"@@IMG:([a-z0-9-]+)@@", rimg, rsvp["rsvp.css"])
        rcss = re.sub(r"@@ART:([A-Za-z0-9_./-]+)@@", aimg, rcss)
        rjs = rsvp["rsvp.js"].replace("@@CFG@@", rsvp["cfg"])
        icss = re.sub(r"@@IMG:([a-z0-9-]+)@@", rimg, rsvp["info.css"])
        icss = re.sub(r"@@ART:([A-Za-z0-9_./-]+)@@", aimg, icss)
        ijs = rsvp["info.js"]
        rcss_name, rjs_name = f"rsvp.{digest(rcss.encode())}.css", f"rsvp.{digest(rjs.encode())}.js"
        icss_name, ijs_name = f"info.{digest(icss.encode())}.css", f"info.{digest(ijs.encode())}.js"
        for name, data in ((rcss_name, rcss), (rjs_name, rjs), (icss_name, icss), (ijs_name, ijs)):
            write(name, data)
        rsvp_tags = (
            f'<link rel="stylesheet" href="{icss_name}">\n<link rel="stylesheet" href="{rcss_name}">\n',
            f'<script src="{ijs_name}"></script>\n<script src="{rjs_name}"></script>\n',
        )

    # --- closed-front preloads, from the first :root block ---
    for n in CLOSED:
        rel = re.findall(rf'--img-{n}:url\("(img/[^"]+)"\)', css)[-1]  # the last slot wins (lane A)
        preload.append(f'<link rel="preload" href="{rel}" as="image" type="image/webp">\n')

    # --- head: fonts and favicon, noindex, share previews ---
    desc = re.search(r'<meta name="description" content="([^"]*)">', text).group(1)
    text = must_sub(
        r'<link rel="icon" href="data:,">\n',
        '<link rel="icon" type="image/png" href="favicon.png">\n<link rel="apple-touch-icon" href="apple-touch-icon.png">\n<meta name="robots" content="noindex,nofollow">\n',
        text,
    )
    og_img = base + "og-image.jpg"
    share = (
        "<!-- Share preview. og:image must be an absolute URL (your domain plus /og-image.jpg) for WhatsApp, iMessage and the rest:\n"
        "     rebuild with --base-url (the full https address) once the domain is known. TODO(user): the preview line (the description) is the dev note from the prototype. -->\n"
        '<meta property="og:type" content="website">\n'
        '<meta property="og:title" content="Maya e Tomás">\n'
        f'<meta property="og:description" content="{desc}">\n'
        '<meta property="og:locale" content="pt_PT">\n'
        f'<meta property="og:image" content="{og_img}">\n'
        '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
        + (f'<meta property="og:url" content="{base}">\n' if base else "")
        + '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="twitter:title" content="Maya e Tomás">\n'
        f'<meta name="twitter:description" content="{desc}">\n'
        f'<meta name="twitter:image" content="{og_img}">\n'
    )
    text = must_sub(r"(<meta name=\"description\"[^>]*>\n)", lambda m: m.group(1) + share, text)
    text = re.sub(r"<!-- owner: Tomas \| prototype v10.*?-->\n", "", text, count=1, flags=re.S)
    text = must_sub(
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n<link rel="preconnect"[^\n]*\n<link rel="stylesheet" href="https://fonts[^\n]*\n',
        "",
        text,
    )
    text = text.replace(
        "@@CSS@@\n", "".join(preload) + f'<link rel="stylesheet" href="{css_name}">\n' + NOSCRIPT
    )
    text = text.replace("@@JS@@", f'<script src="{js_name}"></script>')
    if (
        re.search(r"https?://|data:|blob:|DATA", re.sub(r"<meta[^>]*og:url[^>]*>", "", text))
        and not base
    ):
        left = re.findall(r"https?://[^\s\"')]+|data:|blob:|DATA\S*", text)
        sys.exit(f"site_build: external or data reference left in index.html: {left[:5]}")
    slot = "  <!--@@INFO@@-->\n"
    if rsvp:
        frag = rsvp["rsvp.html"].replace("@@WA@@", rsvp["wa_html"])
        info = rsvp["info.html"]
        if slot in text:
            text = text.replace(slot, info + "\n", 1)
        else:
            frag = info + "\n" + frag
        text = must_sub(r"</main>\n", lambda m: "</main>\n\n" + frag + "\n", text)
        text = must_sub(
            r'(<link rel="stylesheet" href="app\.[0-9a-f]{8}\.css">\n)',
            lambda m: m.group(1) + rsvp_tags[0],
            text,
        )
        text = must_sub(
            r'(<script src="app\.[0-9a-f]{8}\.js"></script>\n)',
            lambda m: m.group(1) + rsvp_tags[1],
            text,
        )
    text = text.replace(slot, "")
    write("index.html", text)

    # --- static files ---
    write("robots.txt", "User-agent: *\nDisallow: /\n")
    write(
        "_headers",
        """# Cloudflare Pages and Netlify. Hashed files never change under their name; the page itself is always re-checked.
/
  Cache-Control: no-cache
/index.html
  Cache-Control: no-cache
/img/*
  Cache-Control: public, max-age=31536000, immutable
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
/app.*
  Cache-Control: public, max-age=31536000, immutable
"""
        + (
            "/rsvp.*\n  Cache-Control: public, max-age=31536000, immutable\n"
            "/info.*\n  Cache-Control: public, max-age=31536000, immutable\n"
            if rsvp
            else ""
        )
        + """/*
  X-Robots-Tag: noindex, nofollow
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
""",
    )
    write(
        "404.html",
        """<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#E3E2D6">
<title>Maya e Tomás</title>
<link rel="icon" type="image/png" href="/favicon.png">
<style>
html,body{height:100%;margin:0}
body{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.6em;background:#E3E2D6;color:#3B2F25;font:18px/1.5 Georgia,'Times New Roman',serif;text-align:center}
p{margin:0;font-size:3em;line-height:1}
a{color:#3B2F25;font-style:italic;padding:.6em 1em}
</style>
</head>
<body>
<p>404</p>
<a href="/">Maya e Tomás</a>
</body>
</html>
""",
    )
    # favicon and touch icon: the wax seal, squared on its alpha
    seal = Image.open(os.path.join(COMPS, "art", "v9", "seal-whole.webp")).convert("RGBA")
    box = seal.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox() or (0, 0, *seal.size)
    side = max(box[2] - box[0], box[3] - box[1])
    cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
    sq = seal.crop((cx - side // 2, cy - side // 2, cx - side // 2 + side, cy - side // 2 + side))
    for name, px in (("favicon.png", 64), ("apple-touch-icon.png", 180)):
        out = os.path.join(SITE, name)
        sq.resize((px, px), Image.LANCZOS).save(out, "PNG", optimize=True)
    og = os.path.join(STATIC, "og-image.jpg")
    if os.path.exists(og):
        shutil.copy(og, os.path.join(SITE, "og-image.jpg"))
    else:
        print("warning: comps/art/site/og-image.jpg is missing (see the docstring)")

    total = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(SITE) for f in fs)
    print(
        f"site/: {len(copied)} images, {len(FONTS)} fonts, {total // 1024} KB; slots: {' '.join(sorted(set(present)))}"
    )


if __name__ == "__main__":
    main()
