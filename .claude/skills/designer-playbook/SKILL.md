---
name: designer-playbook
description: "Use at the start of the invitation work and whenever art or references must be sourced: how a senior designer approaches a hand-illustrated animated invitation (references, style tile, sourcing order from hand-painted scans to public-domain plates to AI, licensing, finishing) and which scripts apply it. Complements the AI tools, never replaces them. Not for code."
---
<!-- owner: Tomas | canonical path: projects/wedding-invite/.claude/skills/designer-playbook/SKILL.md | review date: 2026-11-10 -->
<!-- rollback: rm -rf projects/wedding-invite/.claude/skills/designer-playbook -->

# Designer playbook

The user is not a web designer and asked for what a top designer would do, added to the AI toolchain and not instead of it. Aesthetic judgement in every step below runs on an Opus 5.5 agent at high effort; the user approves at each gate.

## Steps
1. Gather references (section 1) and write `references/REFS.md`.
2. Make a style tile and get it approved (section 2).
3. Source art in the order of section 3; run `scripts/image_quality.py` on everything.
4. Finish and harmonize the assets (section 5).
5. Hand the approved assets to `illustrated-reveal` stage 4 onward.

## 1. References (a moodboard first, never a blank canvas)
- Collect 12 to 20 references before any asset: Pinterest and Savee for art direction, Behance and Dribbble for illustration, Awwwards and Siteinspire for motion and layout (sources describe these as the usual designer stops; Are.na was not verified).
- Search terms: `watercolor botanical invitation`, `azulejo`, `olive branch watercolor`, `Mediterranean wedding stationery`, `animated envelope invitation`.
- For each reference write what is borrowed: composition, palette, line weight, motion timing. Borrow a quality, never the artwork itself.
- Studios that sell this product do it with a watercolor artist plus an animator and 3 to 5 weeks of revisions (Motion Stamp's own description, a vendor claim). That is the quality bar; the pipeline reaches it with a faster toolchain.

## 2. Style tile
One page before any comp: palette from `DESIGN.md`, one sample of each motif, the wax seal, the paper texture, type sample with `ã ç ñ`, ink line weight. The user approves it; it becomes the reference image for `assets/STYLE.md`.

## 3. Sourcing order (quality first)
| Rank | Source | Why | Tool |
| --- | --- | --- | --- |
| A | Hand-painted by someone, scanned at 600 dpi or photographed flat in daylight | looks like nothing generated; the premium route (a freelance watercolor illustrator is the commission route) | `extract_asset.py` |
| B | Public-domain museum plates, recolored to the palette | real watercolor at 4000 px; verified live on 2026-11-10 | `open_art.py` |
| C | Licensed or CC0 packs (Rawpixel CC0 botanical sets, AITextured textures under its free commercial license) | per-item license must be confirmed on the item page | log in `assets/LOG.md` |
| D | AI generation (Copilot app, keyed routes) for motifs A to C lack | one asset per image, same style lock | `free_image.py`, `copilot-image` |
| E | Keyless free generation | concepts only; it failed the quality gate on 2026-11-09 | `free_image.py` |

- Public-domain plates: `open_art.py search "Pomological Watercolor Citrus limon" --min-long 3000 --sheet assets/sheets/NAME.jpg`, pick by eye on the sheet, then `open_art.py get "File:NAME.jpg" out.jpg`. License and credit are logged automatically. The USDA Pomological collection has lemons, figs, oranges and more; other public-domain botanical collections exist (Rawpixel lists Edwards's Botanical Register).
- Search text matches descriptions, not content: the first lemon search returned a diseased citron and a fig stump. Always choose from a contact sheet.
- Recolor and compose: shift plate hues toward the palette; use plates as the style reference image when prompting an AI so generated pieces match real brushwork.

## 4. Google Images and found images
- Never lift an image because it is pretty. Use search results as references only.
- To use one: Google Images, Tools, Usage rights, then open License details and confirm at the source. Google states the filter relies on what hosting sites report and does not verify licenses; Creative Commons says the user must verify.
- Find the original with a reverse image search and log it. If the license is unclear, do not use it.

## 5. Finish like a designer
- Crop to the subject, clean specks, match white balance across assets, keep one ink line weight, add paper texture once at the composite level, never per asset.
- Check each asset at 390 CSS pixels on a phone emulation and at 3x pixel density (long side at least 1200 px for assets, 1800 for hero art).
- Gate: `scripts/image_quality.py ASSET --role asset|hero|small` must PASS before an asset enters `build/`. The gate rejects fake upscales, grain, JPEG blocking and halos; `--selftest` proves it still does.
