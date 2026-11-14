# DESIGN-SPEC: design decisions, one source of truth

Owner: Tomas. Written 2026-11-14 by the Opus designer. Review date: 2026-11-28. Rollback: `rm DESIGN-SPEC.md`.

Order of authority: `SPEC.md` (the user's words) first, then this file, then `DESIGN.md` (seed of 2026-11-10; where it differs from this file, this file holds the live value). Every value below was read from the live source named beside it on 2026-11-14. `M` numbers are `SPEC.md` messages. Unknowns are `TODO(user)`.

Reviewers (`red-team`, `consistency-red-team`, `spec-guardian`): read this file, then run the checklist at the end.

## 1. Type

Fonts: `Allura` and `EB Garamond` (regular, italic), self-hosted WOFF2, Latin subset, in `site/fonts/` (`assets/LOG.md`). Pair chosen by the user, 2026-11-10 (`comps/REDTEAM.md` r5). One pair only; no third face.

| Role | Font, weight, size / line height | Colour | Defined in |
| --- | --- | --- | --- |
| Names (face) | `EB Garamond` 600, `11.2cqw` / 1, tracking `.04em`, capitals; the joining word italic 400 at `.9em` (designer choice since v10, lettered like a tile house sign; kept by the user, 2026-11-14) | `--az-ink` | `comps/prototype.v16.src.html` `.names` |
| `Quinta do Grilo` on the painted plaque | `Allura` 400, `30cqw` and `26cqw` / `.82` | `--az-ink` | same, `.plaque-text` |
| Section and card heads | `Allura` 400, `clamp(3rem,15vw,4.25rem)` / 1.05; card heads `2.25rem` to `2.75rem` | `--olive` | `rsvp/page/info.css` `.ih`, `rsvp/page/rsvp.css` `.h-script`, `.card h3` |
| Kicker and small-capital label | `EB Garamond` 500, `.8125rem` (13 pixels), tracking `.28em` (`.2em` for units and times), uppercase | `--brown` | `info.css` `.ikick`, `.ilabel`; `rsvp.css` `.rkick` |
| Lead text (information) | `EB Garamond` 400, `1.1875rem` (19 pixels) / 1.6, measure `28rem` | `--brown` | `info.css` `.itext` |
| Body (face / RSVP) | 18 pixels / 1.5; `1.125rem` / 1.55 | `--ink` | `body`; `rsvp.css` `.rsvp` |
| Date / place / village (face) | 19 pixels italic; 23 pixels; 12.5 pixels capitals tracking `.24em` | `--ink`, `--warm-ink`, `--brown` | `.date`, `.place`, `.village` |
| Countdown figures | `EB Garamond` 400, `clamp(2.5rem,12vw,3.25rem)` / 1, tabular lining figures | `--olive` | `info.css` `.iclock .n` |
| Buttons | send `1.1875rem` 500; pill `1.0625rem`; Skip 16 pixels tracking `.04em`, 48 pixels tall | `--paper` on olive; `--ink` | `rsvp.css` `.send`, `.btn`; face `.skip` |
| Inputs | 16 pixels (stops iOS zoom) / 1.4 | `--ink` | `rsvp.css` |

Note on the names: `DESIGN.md` (2026-11-10) planned `Allura` for the names. Since v10 the face sets them in `EB Garamond` capitals inside the painted panel; `SPEC.md` has no user message choosing either, and the finished face stays untouched. The user chose to keep `EB Garamond` (2026-11-14).

Rules: script only for the plaque name and heads, never for anything a guest must read closely (`DESIGN.md`). Glyphs `ã ç ñ á é í ó ú ü` must render in all three languages: Latin subset covers them; a recorded glyph test is `TODO(user)` evidence.

## 2. Colour

| Token | Hex | Role | On `--paper` | Source |
| --- | --- | --- | --- | --- |
| `--paper` | `#F6EFDF` | the one page ground, cards, inputs, theme colour | n/a | `SPEC.md` Derived; M41 one paper |
| `--sand` | `#E6D6B8` | envelope body | decoration | `SPEC.md` Derived |
| `--ink` | `#3B2F25` | body text, ink lines | 11.32:1 | same |
| `--warm-ink` | `#4A3B2E` | place name over the far hills | 9.37:1 | `prototype.v16.src.html` |
| `--olive` | `#4F5F2E` | heads, figures, send button, chosen state | 6.09:1 | `SPEC.md` Derived |
| `--brown` | `#6B4F34` | kickers, labels, lead text, edges | 6.56:1 | same |
| `--terracotta` | `#9A4C32` | wax seal, errors | 5.31:1 | same |
| `--az-ink` | `#1B2556` | lettering on tiles | 12.68:1 (12.57:1 on `--az-glaze`) | sampled from the painted plaque, v16 |
| `--az-cobalt` | `#344680` | focus ring only | 7.85:1 | same |
| `--az-glaze` | `#F3EEE5` | tile glaze | n/a | same |
| `--sage` `--twine` `--clay` `--lemon` | `#9DAE82` `#B8946A` `#C98B6B` `#EBDDA0` | washes, hairlines, schedule ring | 2.08, 2.45, 2.48, 1.19:1: never carry words | `SPEC.md` Derived |
| `--shade` | `#E3E2D6` | face `body` before the open | ink on it 9.95:1 | face source |

- Alphas of brown only: card edge 40 %, rule 26 %, input edge 72 % (3.47:1 on paper; WCAG 1.4.11 asks 3:1 for UI edges, so it passes; the older 3.9 figure in the notes and in `rsvp.css` was corrected on 2026-11-14), chosen ground 8 %; error ground terracotta 8 %.
- `#7F9BA8` (`--azulejo` in `DESIGN.md`) is retired, not a token: the painted cobalt replaced it (M47) and no live CSS uses it. Do not bring it back.
- Colour split, from the user's deck (slide 4): 60 % paper, stone, mist; 25 % sage, olive, warm brown; 15 % flowers, birds, sky.
- Run `scripts/contrast.py` after any colour change. Text pairs at least 4.5:1 (`CLAUDE.md`).

## 3. Paper

- One tone for the whole scroll: `--paper` `#F6EFDF` plus the face's paper tile at 341 pixels; sections below the face are transparent over it (M41; `DESIGNER-NOTES.md` "One paper").
- Sampled at every section boundary: RGB 244 to 245, 237 to 239, 221 to 223. Tolerance: each channel within 3 of those values, no visible step.
- Grain soft (user, 2026-11-10). Paper texture is added once at the page, never inside an asset (`designer-playbook`).

## 4. Layout and spacing

| Rule | Value | Source |
| --- | --- | --- |
| Phone first; column unit | `u` = `min(100vw, 440px) / 100` (face `--u`, sections `--pu`) | face source, `info.css` |
| Column | max `36rem`; text measure `28rem`; cards `24rem` | `info.css`, `rsvp.css` |
| Side gutter | `1.25rem` (20 pixels) | same |
| Section rhythm | `3.25rem` top, `3.75rem` bottom (information); `4.5rem` top (RSVP) | same |
| Section anatomy | kicker, script head, short rule, content; centred (plaque, countdown, gifts) or composed left (schedule, dress code, questions) | `DESIGNER-NOTES.md` (`Dolce Vita`, M38) |
| Radii | 14 pixels for cards, choices, notices, inputs and send (`--r` in `rsvp.css`; `.icard` in `info.css`); pill buttons 999 pixels; focus 6 pixels; small tile 2 pixels | `rsvp.css`, `info.css` |
| Tap targets | 48 pixels minimum (inputs, `.btn`, `.ibtn`, error-summary links; question rows and send 56 pixels); seal 100 pixels; the face's Skip 48 pixels (2026-11-14) | `CLAUDE.md` |
| Reflow | no sideways scroll at 390, 360 and 195 pixels (200 % zoom) | `DESIGNER-NOTES.md` |
| Opening | vertical only: top flap lifts, bottom drops, page scrolls down; no side opening | M12, M13, M27 |

## 5. Ornament and motif vocabulary

| Motif | Where | Rule |
| --- | --- | --- |
| Olive branch, orange branch | face corners; dress-code vignette | the reference pieces for the art style (section 6) |
| Swallows | face sky | rare crossings, not loops (deck slide 28) |
| Lavender, wheat | schedule base (wheat and lavender); page foot (lavender) | standing on a base line, never floating |
| Wild carrot | page foot, left, on the `rodapé` (in the fennel's place) | sways like the other plants |
| Mushrooms | fly agarics only, at the left end of the hairline under the countdown | one piece on the page (not too many mushrooms); static, fade in only |
| Fig branch | gifts, top right, entering from the right edge | sways about its cut end |
| Bee | countdown, top right | faces left, so it flies in once from the right, then bobs |
| Meadow strip, bindweed, clouds | face land, panel corners, sky | clouds soft-edged, no outline |
| `Azulejo` names plaque | face hero | painted, cobalt; names inside it (M31) |
| Address plaque (`barra` frame) | `Como chegar` | same cobalt hand, simpler frame (M47) |
| Small painted tile | two places only: after the schedule, top of the RSVP card | M47 "keep one or two" |
| `Rodapé` | page foot only, multiplied onto paper | M47 |
| Wax seal | closed letter, tap target | terracotta `#9A4C32`, olive sprig, no letters (M26) |
| Dogs | the gate | the user's four dogs, one group |
| Dividers | twine hairline everywhere else | `DESIGNER-NOTES.md` |
| Never | monogram, flat vector tiles, emoji, gradients, identical card grids, `Inter` | M26, M47, `DESIGN.md` Never |

## 6. Art style

### Canonical style lock (paste for every new painting)

```text
Loose botanical watercolour of [SUBJECT]. Warm cotton paper, soft muted Mediterranean palette of olive, sage, straw, dusty terracotta and faded lemon, restrained saturation. Translucent layered washes with soft wet edges, colour that fades out rather than stopping at a line, white of the paper for highlights, light from the upper left. Only a few thin broken dark-brown ink lines, in places, never a closed outline around a shape. Few details: no hatching, no stippling, no texture strokes, no soil or crumbs, no gloss, no 3D modelling; a natural slightly asymmetric pose, not a catalogue plate. One element, isolated with wide margins. Plain flat off-white background, no ground, no shadow, no people, no text, no frame. [ASPECT], high resolution.
```

- Background variant: white or cream subjects (clouds, wild carrot, cream fur) take `Plain flat even light grey background` instead, so the cut-out keeps their edges (V12 section 5, V10 dogs).
- Reference to attach in `Copilot`: `comps/art/v16/olive.webp`. Prompts ready to paste: `rsvp/comps/PASTE-PROMPTS.md`.
- `assets/STYLE.md` holds the same words in prefix form ("of the subject below"), because `scripts/free_image.py` prepends that whole file, heading included, to each prompt; subject and aspect follow it.
- No other lock is valid. Older wordings (section below) are history, not options.

### What the lock changes (2026-11-14)

| Against | Change | Why |
| --- | --- | --- |
| `STYLE.md` of 2026-11-09 | "ink outlines" becomes "a few broken ink lines, never a closed outline"; guards added; "visible paper grain" removed | the word "outlines" gave a crisp contour and a 3D plate (`mushroom-test-01`) |
| V12 section 5 (the batch closest to the face) | same opening; ink lines limited; palette named in full; "restrained saturation"; guards added | bindweed, citrus and the round cloud came back with closed contours; citrus 95th-percentile saturation 0.95 against the olive's 0.44 (`V14-CRITIC.md`) |
| Sketchbook lock v1 (`ASSET-PROMPTS.md`, 2026-11-12) | retired: no pen, no sketchbook, no wobbly outline | it drew a heavy dark pen line round every form, hatched gills and crumbs: a different hand (user, 2026-11-14) |
| `PASTE-PROMPTS.md` version 2 | ink line moved after the washes and limited; "soft wash edges" becomes translucent layered washes; "colours pale" becomes restrained saturation; paper grain removed; "no people" added | the face's art is muted, not pale (dark olives); the line must follow the wash, not lead it |

### How each wording rendered

| Wording | Made | How it looks |
| --- | --- | --- |
| Deck slide 36 "Hand-painted European pastoral watercolor ... loose line-and-wash, translucent glazing" (probable; the v10 prompts were not logged) | olive, orange bough, swallow, bloom, sky, land, grass, names plaque, gate, vine, eucalyptus | no outline; soft wet edges; muted (olive saturation 0.44); medium detail. **The face's look** |
| `STYLE.md` "thin hand-drawn dark-brown ink outlines" | `mushroom-test-01` (`porcini`) | even fine contour, full 3D shading, dense texture |
| V10 "loose watercolour, thin uneven dark-brown ink lines" + photo | the four dogs | broken fine lines in places, washes lead, much white paper: on target; blacks too dark |
| V12 section 5 "Loose botanical watercolour of ... thin uneven dark-brown ink lines" | clouds, meadow, bindweed, olive twig, loose leaves, swallow, lavender (and the citrus branch) | mostly no visible line; bindweed and citrus have thin closed contours; citrus over-saturated; round cloud outlined |
| `ASSET-PROMPTS.md` lock of 2026-11-12 (wording not kept) | `mush-caesar-pair`, `m5-mush-fly-agaric-pair` | glossy scientific plates, hundreds of gills (M54 "too AI") |
| Sketchbook lock v1 | four `-v2` mushrooms of 2026-11-14 | heavy broken dark pen outline everywhere, about 40 gill strokes, crumbs; `porcini` 3D, parasol symmetric |

### Allowed and forbidden

| Allowed | Forbidden |
| --- | --- |
| translucent washes, soft wet edges, blooms | closed dark outline round a form; pen-and-ink sketch look |
| a few fine broken lines, no darker than `--ink` | hatching, stippling, dense gills or bark |
| white paper inside the forms | gloss, highlight dots, rim light, glow |
| muted colour; flowers and birds may carry the most | saturated or neon colour; 95th-percentile saturation above 0.70 |
| natural, slightly asymmetric pose | catalogue symmetry, 3D modelling, photographic texture |
| one subject per image | text, frames, cast shadows, soil crumbs |

### Toning a new piece at cut-out

1. Cut out: `scripts/extract_asset.py --matting`, or key against the flat ground with colour un-mixing (`comps/art/v13_build.py`). Trim.
2. Saturation × 0.65 to 0.85, brightness × 1.0 to 1.04 (`tone()` in `comps/art/v12_bake.py`). Target 95th-percentile saturation at or under 0.70; the olive is 0.44 (`V14-CRITIC.md`).
3. Lift the blacks: 1st-percentile luminance at or above about 48 of 255, the page ink `#3B2F25` (the dogs at 21 to 32 were the darkest marks on the page).
4. Pen outline (only the two kept `v2` mushrooms): lighten the line toward `--ink` until it reads no heavier than the bindweed stem. Applied 2026-11-14 as blacks lifted to 45 of 255 at cut-out (`assets/LOG.md`).
5. Flat-ground paintings that must sit in the paper (`rodapé` method): divide by the ground mean, then `mix-blend-mode: multiply` on the paper.
6. Size: `WebP` at 3x display, 15 to 45 KB a piece. `scripts/image_quality.py` PASS before `build/`. No runtime `filter`.
7. Log the row in `assets/LOG.md` (tool, date, prompt, terms).

### Pieces per section and placement

- One lead painted subject per section (`Dolce Vita` anatomy); supporting props at its sides or base. At most two painted props per section (user).
- Shown now (2026-11-14): where: none (the face's vine and eucalyptus frame it); countdown: fly agarics (hairline's left end, 11u) and bee (right top, 6u); schedule: wheat and lavender (right base); dress code: orange branch vignette and falling leaf; gifts: fig branch (right top, 26u); questions: dried peppers (right top, 8u, 1.2 deg sway from the string); RSVP: olive twig (head, left), lavender (head, right, mirrored); page foot: wild carrot (left, 15u) and lavender (right).
- Slot kept but hidden (`PENDING`, `info.css`): the left olive branch (gifts). Cut but not placed: `comps/art/v17/pebbles.webp`.
- Scale 5u to 34u; never over the text column, a button or the plaque.
- Sides alternate down the page (`ASSET-PROMPTS.md` placement rules).
- Mushrooms: at most two pieces on the whole page: the fly agaric and the Caesar's pair (user, 2026-11-14). At section feet, rooted, static or 1 deg sway at most.
- Rooted things do not sway (trunks, rocks, mushrooms); plants sway 0.6 to 2.2 deg over 4.3 to 7.3 s, no two in step.
- Each piece loads one screen before its section (`.near`); empty slots stay hidden (`PENDING`), never a stand-in.

## 7. Motion

| Rule | Value | Source |
| --- | --- | --- |
| Properties | `transform` and `opacity` only; the few ink lines may use `stroke-dashoffset` | `CLAUDE.md`, user 2026-11-10 |
| Opening length | about 5 s (v16: letter open 1.85 s, last entrance 4.40 s, Skip leaves 4.80 s); supersedes the 8 to 12 s of `DESIGN.md` | M42 |
| Folds | lift `1100ms`, drop `1150ms`, `--ease-fold` `cubic-bezier(.77,0,.175,1)` | face source |
| Curves | `--ease-out` `cubic-bezier(.23,1,.32,1)`; `--ease-sine` `cubic-bezier(.37,0,.63,1)`; sections `--ease` `cubic-bezier(.22,.8,.24,1)` | face, `info.css` |
| Plays | once, visible Skip, no replay (M41) | M41 |
| Ambient | starts when seen, pauses off screen, loops start from rest | `ASSET-PROMPTS.md` |
| Falling leaf | 2.6 s fall from 3.3 s, every 40 s | `DESIGNER-NOTES.md` |
| Props | plants sway; mushrooms static (fade in only); the bee flies in once, then bobs | user, 2026-11-14 |
| Reduced motion | letter opens, art fades in, no drawing; props at rest; falling leaf hidden | `DESIGN.md`, `info.css` |
| Long motion | motion over 5 s that starts by itself needs pause, stop or hide (WCAG 2.2.2); state on the live page `TODO(user)` evidence | `V10-ATMOSPHERE-ADVICE.md` |

## 8. Copy and language

- All copy is the user's; invented test text is marked `FAKE` (M40) or `TODO(user)`.
- Names: Maya e Tomás (`e` pt-PT, `and` en, `y` es). Date: 10 July 2027. Place: `Quinta do Grilo`, `Milharado`. No monogram. Opening line: `TODO(user)`.
- Languages: `pt-PT` (default), `en`, `es`; `lang` on `html` and on every language variant.
- Each fact once on the rendered page, every language (M44, M45): date, year, venue, town, street, postcode, deadline, IBAN, each time. Known exceptions: the painted gate plaque (`aria-hidden`), the two WhatsApp buttons named `Tomás` and `Maya`.
- No text inside generated images.

## 9. Accessibility

- Seal is a real `<button>` with a name per language; Skip first in focus order and visible.
- Focus ring 3 pixels `--az-cobalt`, offset 3 pixels.
- Text 4.5:1; UI edges 3:1; tap targets 48 pixels.
- `axe-core` (WCAG 2.2 AA): no violations; keyboard path through every control; no-JavaScript path shows the information and a no-JavaScript RSVP card.

## 10. Performance

- First load under 1500 KB (stretch 500); v16 measured 1457 KB; the v17 test build 1451 KB before the tap (2026-11-14) (props load later, one screen ahead).
- Fonts self-hosted, three WOFF2 files. Images `WebP`. Props 15 to 45 KB each, loaded one screen ahead.
- Compositor-only frames; p95 frame at or under 16.8 ms at CPU 4x (`V12-CHOREOGRAPHY-ADVICE.md`).

## 11. Decision log

| Date | Decision | Who | Source |
| --- | --- | --- | --- |
| 2026-11-09 | Closed envelope opens on a tap; drawings draw in; accessible to all 150 guests | user | M1 |
| 2026-11-09 | Pastel, beige, greenish, light brown, summery Mediterranean countryside | user | M2 |
| 2026-11-09 | Art and aesthetics by an Opus agent; the user picks | user | M6, M14, M18 |
| 2026-11-09 | Names Maya e Tomás; clean and elegant; red-team loop; vertical only | user | M12 |
| 2026-11-10 | Follow the user's deck as closely as possible | user | M19 |
| 2026-11-10 | Folded sheet with a wax seal; two folds, top then bottom | user | M20, M27 |
| 2026-11-10 | `Allura` with `EB Garamond`; `stroke-dashoffset` for ink lines; fuller scene | user | `comps/REDTEAM.md` r5 |
| 2026-11-10 | 10 July, `Quinta do Grilo`, `Milharado`; `azulejo` details | user | M24 |
| 2026-11-10 | No monogram | user | M26 |
| 2026-11-10 | Names inside a multi-tile `azulejo` panel; plaque smaller than names | user | M31 |
| 2026-11-11 | Year 2027 | user | `CLAUDE.md` |
| 2026-11-12 | One paper tone; keep the aesthetic; replay removed | user | M41 |
| 2026-11-12 | Sections countdown, location, schedule, dress code, calendar, gifts, questions; opening about 5 s | user | M42 |
| 2026-11-12 | Each fact once; consistency red team | user | M44, M45 |
| 2026-11-12 | More life: bees, trunks, mushrooms first, things from the sides | user | M46 |
| 2026-11-12 | Painted `azulejo` only, one or two small tiles, a `rodapé`, an information plaque | user | M47 |
| 2026-11-12 | Mushrooms as a format guide; Portuguese wildflowers; a pepper bunch; summer | user | M51, M52, M53 |
| 2026-11-12 | Less AI-realistic, more watercolour and drawing | user | M54 |
| 2026-11-12 | Aesthetics only; backend later | user | M55 |
| 2026-11-14 | Mushrooms at most two; fly agaric and Caesar's kept; `porcini` and parasol rejected as too detailed | user | chat, 2026-11-14 |
| 2026-11-14 | Pen outline dropped for new art; one canonical lock (section 6); this file | user, Opus designer | chat, 2026-11-14 |
| 2026-11-14 | At most two painted props per section; never over text or a button; sides alternate; mushrooms static or 1 deg sway | user | chat, 2026-11-14 |
| 2026-11-14 | Fly agarics, Caesar's, bee and fennel placed; foot wheat, carrot, stones and the gifts rock slot removed; peppers moved to the questions | Opus art director, Opus designer | `rsvp/comps/DESIGNER-NOTES.md` |
| 2026-11-14 | One radius of 14 pixels; error-summary links 48 pixels; `#7F9BA8` retired; input edge figure corrected to 3.47:1 | Opus designer | same |
| 2026-11-14 | New props (mushrooms, bee, fennel) hidden while they are repainted; only the face's own art shows | user | chat, 2026-11-14 |
| 2026-11-14 | Names stay in `EB Garamond` capitals | user | chat, 2026-11-14 |
| 2026-11-14 | Face Skip raised from 44 to 48 pixels (`min-height` only), to match every other tap target; minimal change to the frozen face | Opus designer, delegated by the user | `comps/prototype.v16.src.html` `.skip` |
| 2026-11-14 | Page foot keeps one lavender, right: a mirrored second copy of the same cut-out would read as a stamp, and one plant at the end of the `rodapé` keeps the sides alternating; the fennel slot returns on the left when repainted | Opus designer, delegated by the user | same |
| 2026-11-14 | Props from the user's new paintings, chosen for restraint: used Copilot v5 fig branch and wild carrot and Copilot v6 fly agarics and bee (same hand as the face; toned by `comps/art/v17_props_v5.py`). Dropped: cork oak (heavy, saturated bark texture, would dominate), cicada (one insect is enough), pebbles (gifts already has the fig; kept as a cut), peppers v6 (they would sit top right just after the fig, breaking the side rhythm; questions left bare), every `Higgsfield` piece (softer, different hand; v6 replaced them), the older v17 cut-outs (pen outline), RSVP leaf (clutter). Lavender in the RSVP head mirrored (the same painting shows three times) | Opus designer, delegated by the user | chat, 2026-11-14; `consistency-red-team` |
| 2026-11-14 | Peppers v6 hung in the questions, toned to terracotta (saturation x0.6), small, gentle sway; bee and fly agarics kept in the countdown | user | chat, 2026-11-14 |
| 2026-11-14 | Polish pass: dress head spans the column; IBAN card loses its blank band; RSVP lavender and leaf moved off the fields and buttons; deadline label at the small-capital role; one solid button in the no-link card | Opus designer | `rsvp/comps/DESIGNER-NOTES.md` |

## 12. Red-team checklist

Answer yes or no; every "no" is a finding with its place and the smallest fix.

### Any new painting

- [ ] Made with the canonical lock (or its grey-background variant), logged in `assets/LOG.md`?
- [ ] No closed outline; no line heavier or darker than the bindweed stem; no pen-sketch look?
- [ ] No hatching, stippling, dense gills or bark, soil crumbs?
- [ ] No gloss, highlight dots, rim light, 3D shading, photographic texture?
- [ ] 95th-percentile saturation at or under 0.70; 1st-percentile luminance at or above about 48?
- [ ] White paper left inside the forms; washes lead, line follows?
- [ ] Beside `olive.webp` at phone size, does it read as the same hand?
- [ ] No halo on paper at 3x; `image_quality.py` PASS; 15 to 45 KB?

### The rendered page

- [ ] Paper within 3 per channel of RGB 244, 237, 221 at the top, every section boundary and the foot; no seam?
- [ ] Every text and accent colour is a token in section 2?
- [ ] Only `Allura` and `EB Garamond`; each role in section 1 has one size and colour across sections?
- [ ] Radii, edges and dividers match section 4 and 5; the small tile appears exactly twice, the `rodapé` once?
- [ ] At most two mushroom pieces on the page?
- [ ] At most two props per section; none over text, a button or the plaque; sides alternate?
- [ ] Each fact once per language (script over `innerText`), exceptions as in section 8?
- [ ] Names, date, year, place exactly as section 8; opening line still `TODO(user)` unless the user gave it?
- [ ] `lang` set per language; no mixed languages in a section?
- [ ] Only `transform` and `opacity` animate (plus `stroke-dashoffset` on ink lines)?
- [ ] Opening done by about 5 s; reduced motion settles at once with props at rest?
- [ ] Seal is a `<button>`; Skip first in focus order; every tap target at least 48 pixels?
- [ ] Text pairs at least 4.5:1; focus ring visible on every control?
- [ ] No sideways scroll at 390, 360 and 195 pixels?
- [ ] First load under 1500 KB?
