# DESIGN: the invitation face (seed, status DRAFT)

Seeded from the research chat of 2026-11-09. The Opus 5.5 high agent refines this in pipeline stage 1; the user approves it at the gate. Placeholders are `TODO(user)`.

## Subject and job

Closed handmade-paper envelope, lightly decorated, with a wax seal. One tap opens it. Ink line art then watercolor washes draw in. Phone-first, 150 guests, ages mixed, links arrive on WhatsApp. This file covers the face only, not the site.

## Mood

Southern Italy and Portugal, summer, countryside (`campestre`): sun-washed paper, olive and lemon, whitewashed stone, faded `azulejo` blue. Quiet, not busy.

## Palette (tokens)

| Token | Hex | Role | On paper |
| --- | --- | --- | --- |
| `--paper` | `#F6EFDF` | card and page ground | n/a |
| `--sand` | `#E6D6B8` | envelope body | decoration |
| `--ink` | `#3B2F25` | body text, ink lines | 11.32:1 |
| `--olive` | `#4F5F2E` | names, headings | 6.09:1 |
| `--terracotta` | `#9A4C32` | wax seal, accents | 5.31:1 |
| `--brown` | `#6B4F34` | captions | 6.56:1 |
| `--sage` | `#9DAE82` | leaf washes | decoration only (2.08:1) |
| `--twine` | `#B8946A` | twine, borders | decoration only |
| `--clay` | `#C98B6B` | blush wash, fruit | decoration only |
| `--lemon` | `#EBDDA0` | wash highlights | decoration only |
| `--azulejo` | `#7F9BA8` | tile motifs | decoration only |

Pale tones never carry words. Check with `scripts/contrast.py`.

## Type (to confirm by glyph test for ã ç ñ á é í ó ú ü)

Candidates tested on the mood board: A Great Vibes with Lora; B `Allura` with EB Garamond; C Pinyon Script with Cormorant Garamond. Script for the names only; a plain serif for everything a guest must read. Choice (user, 2026-11-10): B, `Allura` with EB Garamond.

## Motifs

Olive branch, lemons and leaves, fig leaf, chamomile and wild herbs, poppies, cypress and farmhouse scene, faded `azulejo` tile border. Scene or landmark: TODO(user).

## Copy

Names: Maya e Tomás (Portuguese `e`; `and` in English, `y` in Spanish). Date: 10 July (`10 de julho`, `10 July`, `10 de julio`); place: `Quinta do Grilo`, `Milharado` (user, 2026-11-10). Year, opening line: TODO(user). No monogram: the user finds the names alone better (2026-11-10). Languages: `pt-PT` (default), `en`, `es`. Seal labels: `Toca para abrir`, `Tap to open`, `Toca para abrir`; skip: `Saltar`, `Skip`, `Saltar`.

## Chosen by the user (2026-11-10)

Closed state is one tall folded sheet of paper with a wax seal as the tap target. Look follows the user's deck, fuller than the first tile but still mostly paper. Paper grain is soft. The names section is "written by hand": the names write on, an ink olive sprig draws beside them, its leaves take color, and one leaf drifts down. Date and place are set as on the `quinta` sign (concept D3). `Azulejo` details wanted: B4 the `quinta` plaque closing the invitation and B3 a tile lining under the lifting panel, each to be seen separately before the final pick.

## Never (generic-AI defaults to reject)

Cream plus serif plus terracotta used by reflex; identical card grids; purple or blue gradients; Inter or Space `Grotesk` by default; perfect symmetry; airbrushed gradients in the art; text inside generated images; emoji as ornament; everything centered with the same radius and shadow.

## Opening

Vertical only: the flap opens upward and the invitation continues downward, so the guest then scrolls down the page. No side opening, no card sliding out sideways. Two folds, one at the top and one at the bottom (user, 2026-11-10; concept 2 of `comps/fold-concepts.html`): the top lifts first, then the bottom drops, one motion at a time, and the sheet grows downward with the seal on the outer flap.

## Motion

See `STORYBOARD.md`. Only `transform` and `opacity`, except the few ink lines, which may draw with `stroke-dashoffset` (user, 2026-11-10). 8 to 12 s. Plays once. Visible Skip. Reduced motion and weak phones: envelope opens, art fades in, no drawing.

## Accessibility

Real `<button>` tap target with a per-language name; Skip first in focus order; focus into the intro then to the invitation; `lang` on every language variant; text pairs at least 4.5:1; first load under 1500 KB (stretch 500 KB).
