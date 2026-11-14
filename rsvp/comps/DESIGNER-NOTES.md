# Designer notes: v16, the information page

Owner: Tomas. Written 2026-11-12 by the Opus designer. Review date: 2026-11-19. Rollback: `rm comps/prototype.v16.src.html rsvp/page/info.*` and `git checkout` the other files listed under "Files".

The user's feedback (Messages 41 to 53): the replay button goes, the opening is too slow (plants, the falling leaf), the page is light next to the five reference invitations, the information belongs in the middle where the grapes hang, keep the painted look, one paper tone, each fact said once, no flat vector tiles, and more painted life (mushrooms, bees, rocks, July wildflowers, dried peppers). This pass answers all of it in one build; `v15` stays untouched.

## `Dolce Vita` review and rebuild of the new parts (2026-11-14, later)

- The user: the new parts felt "too compacted", their assets "too small", "all over the place", "unprofessional". The measured comparison with `Dolce Vita` and with the face, the ranked causes and every decision are in `rsvp/comps/REVIEW-DOLCE-VITA.md`.
- One centred axis for every section (the left-composed schedule, dress code and questions are retired). Space separates the sections, 72 pixels at each one's top and foot, never a hairline. One painted tile is the pause, after the schedule.
- Pieces at the face's own scale: bee 12u, fly agarics 30u (a centred vignette closing the countdown), wheat 34u with the wild carrot 24u at the schedule's foot, the orange branch 60u above the dress head from the left edge, the fig 64u above the gifts head from the right edge, the peppers 20u above the questions kicker, the olive twig 15u at the RSVP head, the pebbles 30u and the lavender 21u on the `rodapé`. No painting shows twice below the face.
- The schedule is a centred printed programme: time in the face's village role over the moment in its place role, on a twine thread; the circled icons are gone. `Como chegar` gets the script head and rule, below the face's hanging vine and eucalyptus.
- Wide screens use the face's 440 pixel column for the information, the RSVP and the foot; every cut end dissolves.
- Reviews: `red-team` 5/10 and `consistency-red-team` 7/10 on the first pass; their findings and the decisions are in the review file. Checked after the last build: nothing paints over text or a control at 390, 360, 195 and 1280; first load 1463 KB.
- Shots: `rsvp/comps/shots/v6-where.jpg`, `v6-count.jpg`, `v6-day.jpg`, `v6-dress.jpg`, `v6-gift.jpg`, `v6-faq.jpg`, `v6-rsvp.jpg`, `v6-foot.jpg`, the `v6-1280-*.jpg` set and `v6-full.jpg`.

## Props from the user's new paintings (2026-11-14)

- Restraint first: four new pieces, two sections bare. Countdown: fly agarics at the hairline's left end and the bee top right (it faces left, so it flies in from the right). Gifts: fig branch top right. Questions: dried peppers top right (user). Page foot: wild carrot left, lavender right. Where carries nothing.
- Dropped and why: `DESIGN-SPEC.md` decision log. One `consistency-red-team` pass: applied the mirrored RSVP lavender, the log rows, the saturation and black floor, the floating mushroom; the fig veins and the carrot's fine line were kept as taste.
- Shots: `rsvp/comps/shots/v5-where.jpg`, `v5-count.jpg`, `v5-day.jpg`, `v5-dress.jpg`, `v5-gift.jpg`, `v5-faq.jpg`, `v5-foot.jpg`, `v5-rsvp.jpg`, `v5-1280.jpg`. First load 1451 KB.

## Polish pass with the face's art only (2026-11-14)

- Hidden while they are repainted: the fly agarics, the Caesar's, the bee and the fennel (`PENDING` in `info.css`; slots and motion hooks kept). The test build no longer ships their files.
- Dress code: the head spans the column (it broke into two lines beside the vignette); the vignette and the note sit under it; the falling leaf starts below the head.
- Gifts: the empty confirmation line no longer leaves a blank band under the copy button.
- RSVP: the lavender stood over the code field and `Abrir`, the leaf over the card edge; both now hang on parts that do not change with the state (lavender at the head's right on the rule's line, leaf at the hairline's left end). Deadline label at the 13 pixel, 500 small-capital role. In the no-link card `Abrir` is the one solid button; WhatsApp is the outlined pill.
- Checked: no prop over text or a button at 390, 360 and 195; no sideways scroll; first load 1451 KB. Shots: `rsvp/comps/shots/v4-count.jpg`, `v4-day.jpg`, `v4-dress.jpg`, `v4-gift.jpg`, `v4-faq.jpg`, `v4-foot.jpg`, `v4-rsvp.jpg`.

## v17 props and spec fixes (2026-11-14)

- Placed: fly agarics at the countdown foot, left, 12u (`.lv-mush-a`); Caesar's under the gifts card, right, 12u (`.lv-mush-c`); the bee in the countdown, top right, 5u, flying in once from the right (`.lv-bee`); wild fennel at the page foot, left, 14u (`.lv-fennel`). Mushrooms fade in only and never sway.
- Two props per section at most (user): the old single mushroom slot left the schedule (it made three there); the rock slot left the gifts (Caesar's took its spot); the peppers moved from the countdown to the questions, right top, still pending; the foot lost its wheat, carrot and stones slots, so it carries fennel and lavender only.
- Bugs fixed: the page-foot props never showed (the foot sits outside `.info` and `.rsvp`, so `--ease` was missing and the entrance shorthand was invalid); the `PENDING` hide rule lost to `.lv{display:block}`, so empty slots took space.
- Spec fixes: one 14 pixel radius (`--r` in `rsvp.css`: cards, choices, notices, inputs, send); error-summary links 48 pixels; input edge figure corrected to 3.47:1. The face's Skip (44 pixels) and the names font were not touched: both are open questions in `DESIGN-SPEC.md`.
- Shots at 390 x 844 after the tap: `rsvp/comps/shots/v3-count.jpg`, `v3-day.jpg`, `v3-dress.jpg`, `v3-gift.jpg`, `v3-faq.jpg`, `v3-foot.jpg`. First load before the tap: 1450 KB.

## Fix pass (reviews R7 to R14, 2026-11-12)

- **Page foot flora** now renders: the column unit `--pu` is set on both wrappers (`.info-wrap`, `.rsvp-wrap`); the foot is 101 pixels tall at 390 wide, with the wheat (94) and lavender (115) standing on the `rodapé`.
- **No stand-ins.** The swallows posing as a bee and a bird, the olive twigs posing as peppers and a branch, the rock-rose posing as a mushroom and the meadow strip posing as stones are gone; the swallow on the RSVP is gone too. Their slots and motion hooks stay, empty and hidden (`PENDING` in `info.css`) until the paintings from `ASSET-PROMPTS.md` arrive. What is shown is the face's own art as itself: wheat, lavender, the olive leaf, the orange branch.
- **Facts once.** The dress note no longer says formal; the weather answer no longer says July; the English RSVP subtitle no longer says reply (the kicker does). The gate's painted `Quinta do Grilo` waits for the user.
- **`Azulejo`, one or two.** The small painted tile appears in two places only: the divider after the schedule, and the top of the RSVP card. Every other divider is a twine hairline. The `rodapé` is only the page foot, multiplied onto the paper from a copy with its glaze lifted to white, so only the cobalt paint shows (sampled: the band's glaze reads 246, 239, 223, the paper's own value). The address plaque has its own frame (above).
- **Colours: palette tokens only.** The two `azulejo` blues are documented tokens, sampled from the painted names plaque: `--az-ink` `#1B2556` (lettering on tiles) and `--az-cobalt` `#344680` (focus rings). They appear only on `azulejo` things and focus. Section heads, the countdown figures, the family name and every RSVP card head are olive; every small-capital label is brown; card and input grounds are the paper itself; edges are the brown at 40 to 72 per cent; the chosen-answer grounds are olive or brown at 8 per cent; the error ground is terracotta at 8 per cent. The `html` background is the paper (pulling past the top or bottom no longer shows grey-green), and so is the browser's theme colour.
- **Type.** `Allura` only for the names and section and card heads; schedule items are `EB Garamond`; the RSVP card heads ("we could not find your invitation" and the rest) are script heads in olive like the others.
- **Hard edges.** The gate art dissolves at its top (the willow fronds) and at its foot; the foreground wheat by the dogs melts into the ground; each seal half fades as its flap starts to turn, so no squashed wax is seen edge-on at 1 s.
- **Composition.** Centred: the plaque, the countdown, the gifts. Composed on the left: the schedule timeline, the dress code beside its vignette, the questions.
- **200% zoom (195 pixels wide).** The pressed seal leaves the layout once the letter opens (no sideways scroll); the address uses `max(1rem, 6.2cqw)`; the RSVP twig is hidden under 340 pixels. Measured: no horizontal scroll at 195, 360 and 390.

## Structure

One scroll, in this order. The face keeps its hero; the information sits in the gap between the land and the gate, where the grapevine (left) and the eucalyptus (right) hang over it; then the gate with the dogs closes the information and leads into the reply form.

1. The opening face (world 1): sky, olive and orange branches, the names plaque, date, venue and town, the land.
2. **`Como chegar`**: an `azulejo` plaque framed in painted `barra` tiles (the same cobalt hand as the names plaque, a different and simpler frame), holding the street address, with the Maps and calendar buttons under it. The vine and the eucalyptus frame it.
3. **`Faltam`** (centred): the countdown, three olive figures with twine hairlines (days, hours, minutes; numbers only).
4. **`Programa`** (composed on the left): a timeline, a twine stem with a small ink drawing on it for each moment (gate, rings, glass, cutlery, cake, music), the time in small capitals and the moment in `EB Garamond`; the wheat and lavender stand at the right base.
5. **`Traje formal`** (composed): the orange branch as a painted vignette on the left, the head and one short note on the right; the note does not say "formal" again.
6. **`Prendas`**: a short warm note, then a card with the IBAN as Portuguese invitations print it, and a copy button with a spoken confirmation.
7. **`Antes do dia`** (composed on the left): three questions as native disclosures.
8. The gate with the `Quinta do Grilo` plaque and the four dogs (world 2).
9. The RSVP (unchanged form; its venue card moved into section 2), then the painted `rodapé` with wheat and lavender standing on it as the page's foot (the one place the `rodapé` is used).

## What came from which reference

- `Dolce Vita` (the lead): the section order (countdown, location, schedule, dress code, gifts, RSVP), the section anatomy (tracked small-capital kicker, large script heading, short rule, then content), one painted subject per section, generous air between sections, the gifts note before a card.
- `Nautical`: the schedule as a centred column of times and moments joined by a vertical line, and the questions block as a list of disclosures right before the RSVP.
- `Floral`: a small ornament between two hairlines as the divider, here our painted tile.
- `Secret Garden` and `Mediterranean Edition`: the quiet countdown of figures with tiny tracked labels, and the IBAN shown in its own card. `Mediterranean Edition` hides the IBAN behind "tap to reveal"; ours is shown, with a copy button, because the couple want it seen.
- Portuguese practice for the gift note (`casamentos.pt` articles): thank the guests for coming first, then a discreet line that money is welcome, then the IBAN; no amounts.

Nothing was copied: no art, no wording.

## Opening timing, before and after

Measured with Playwright on an iPhone 15 profile, full motion tier forced (`?motion=full`; on this loaded test machine the frame probe otherwise picks the lite tier, which skips the entrances). Frames: `rsvp/comps/shots/v2-open-0s.jpg` to `v2-open-6s.jpg`, and `v2-open-compare.jpg` (top row v15, bottom row v16, 1 to 6 s).

| Moment after the tap | v15 | v16 |
| --- | --- | --- |
| Letter fully open | 2.20 s | 1.85 s |
| Sheet gone | 2.90 s | 2.45 s |
| Meadow starts | 2.30 s | 1.90 s |
| Olive and orange branches in place | 5.65 and 5.80 s | 4.25 and 4.40 s |
| Clouds and swallows in place | 7.00 s | 4.40 s |
| Last entrance ends (measured from the animations) | 7.00 s | 4.40 s |
| Skip leaves | 7.00 s | 4.80 s |
| Falling leaf | 10 s fall from 8 s, every 50 s | 2.6 s fall from 3.3 s, every 40 s |

The same pieces, order and curves: the waves overlap more, wipes are 20 to 25% shorter, every loop starts from rest when its piece lands, and the five pieces that come last (two clouds, two swallows, bindweed) load at the tap. The fold keeps its feel at about 85% of its length.

## One paper

The tone changed at the RSVP because the RSVP wrapper drew the paper tile at 600 pixels from its own top, and the face's world ended in a straw tint (`230 214 184 / .2`). Now the body carries the face's tile at 341 pixels in the face's phase, the world's straw foot is gone, and every section below the face is transparent over that one sheet. Sampled on the rendered page at every section boundary: 244 to 245, 237 to 239, 221 to 223 (RGB), the same as open paper elsewhere.

## `Azulejo`, painted only

The flat vector tile band and the vector tile emblem are gone (the user, Message 47). In their place, all cut from the painted names plaque, so they are one hand-painted family:

- The address plaque: a 4 by 1 tile panel framed in `barra` tiles made from the plaque's bottom flower border (turned for the sides), its centre flower as the four corner tiles, the field in the border tiles' own glaze (`comps/art/v16/plaque-address.webp`).
- The `rodapé`: the plaque's bottom flower border, mirrored into one tile (flower in the middle, the scroll arms meeting the next tile), two tiles per repeat with the second slightly warmer. Only at the page foot.
- The small tile: a square crop of the plaque's centre flower, in two places (after the schedule, on the RSVP card).

## Each fact once

Counted on the rendered text after opening, in pt-PT, en and es: date 1, year 1, venue 1, town 1, street 1, postcode 1, deadline 1, IBAN 1, each time 1. Two exceptions to know about:

- The gate's painted plaque reads `Quinta do Grilo`. It is the sign itself (art the user asked for), hidden from screen readers so they hear the venue once.
- The two WhatsApp buttons are labelled `Tomás` and `Maya`, as asked; the names also stand in the hero.

The lower date and village under the dogs are gone; the RSVP deadline drops its year; the address on the plaque drops the town.

## The mushroom plan and the new art

Style correction (the user, Message 54: the first two mushrooms looked "a bit too AI slop realistic"): they came out as glossy scientific plates (3D shading, highlight dots, a hundred even gill lines, photographic earth, one crisp even outline, no bare paper). The style lock in `ASSET-PROMPTS.md` now asks for a fast pen-and-watercolour sketchbook page instead: a wobbly line of uneven weight, a handful of detail strokes, flat pale washes that bleed past the line, white paper inside the forms, no shading, gloss or gradients. It adds an optional step that attaches the user's pictures as a style reference (untested: the daily limit was reached) and a reject list for judging each result. The two existing images are rejected by that list.

`rsvp/comps/ASSET-PROMPTS.md` holds 21 prompts with one style lock. Mushrooms lead: Caesar's mushroom pair, dark `porcini` trio, a tall parasol, grey `inkcaps`, an optional fly agaric pair, in the ink-outline and transparent-wash look of the user's three mushroom pictures, coloured in our palette, in small clusters at the foot of sections and never over text. Then bees (one flying in, one on lavender), a cicada, a cork-oak trunk (stripped red, as in the July cork harvest) and an olive trunk at the sides, olive and fig branches entering from the sides, falling leaves, July wildflowers (Spanish oyster thistle, wild fennel, wild carrot, a wheat sheaf), three rocks and a hanging bunch of dried peppers. Spring flowers that are over by July are left out, with the reason. The motion hooks are live and empty: each slot is hidden (`PENDING` in `info.css`) until its painting arrives, then needs only its slot line and its class taken out of `PENDING`.

## Weight

First load (everything fetched before the tap, Playwright): v15 1898 KB, v16 1457 KB after the fix pass (budget 1500). How: six heavy first-screen images re-encoded (sky, sky veil at half size since it shows at 20%, mist, land, names panel, olive: 778 KB to 442 KB, mean difference under 2.6 of 255 on paper), and the five late pieces fetched at the tap. Everything in the information sections reuses art the face already ships or loads one screen ahead of its section.

## Checks run

- `axe-core` (WCAG 2.2 AA and best practice) on the opened page with all questions open: no violations, in the no-link and the saved states.
- Keyboard: after the opening, Tab goes Maps, calendar, copy IBAN, the three questions, then the RSVP; focus is visible on each.
- Contrast: olive heads and figures on paper 6.1:1, brown labels 6.5:1, ink 11.2:1, paper on olive 6.1:1, `azulejo` ink on the plaque glaze 11.8:1, input edges (brown at 72 per cent) 3.47:1, above the 3:1 for UI edges (corrected 2026-11-14; was given as 3.9).
- No horizontal scroll at 390, 360 and 195 (200% zoom on a 390 phone; the countdown wraps there).
- No JavaScript: the information shows (countdown, copy and calendar buttons hidden), the RSVP shows its no-JavaScript card.
- Reduced motion: everything settles at once; props stay at rest; the falling leaf is hidden.
- RSVP end to end against the local test Worker: load, error summary, save, reload, edit.
- Self-check for the reviewer: one font pair (`Allura` for the names and the heads, `EB Garamond` for the rest), no computed colour outside the palette and the two documented `azulejo` blues, card radius 14 pixels and button radius 999 pixels everywhere, one small-capital style (13 pixels, 500, brown) for every kicker and label, the paper the same at every section boundary.
- The default build (RSVP off) of `v15` is byte-identical to `build/convite-publish` (apart from `.git` and `.nojekyll`, which the build never writes).

Not tested: a real iPhone, iPhone Safari, the WhatsApp in-app browser, the calendar file on iOS and Android, a slow phone at the full motion tier.

## Files

- `comps/prototype.v16.src.html` (new, copy of v15): replay button and the lower date and village removed; opening given its new timing; world split into world 1, the information slot and world 2; one paper; image slots for the re-encodes; the late pieces load at the tap; the opening line is a draft.
- `comps/art/v16/` (new): the six re-encodes, `rodape.webp`, `az-tile.webp` (logged in `assets/LOG.md`).
- `rsvp/page/info.html`, `info.css`, `info.js` (new): the six sections, the countdown, the calendar file, copy IBAN, the prop hooks (pending slots hidden).
- `rsvp/page/rsvp.html`, `rsvp.css`, `rsvp.js`: venue card moved out, vector tiles replaced by the painted tile and `rodapé`, WhatsApp buttons from the config, one paper, deadline without the year, the props take the same entrance.
- `comps/art/site_build.py`: builds `info.*` in with the RSVP, the `@@INFO@@` slot, `@@ART:path@@` images, WhatsApp as a list with names.
- `rsvp/comps/REPLACE-ME.md`, `ASSET-PROMPTS.md`, this file; shots in `rsvp/comps/shots/v2-*.jpg`.

## For the user to decide

1. The opening line draft above the names (three languages).
2. The two invented questions (partners and children, weather) and every draft sentence in `REPLACE-ME.md`.
3. The new paintings: approve the prompts in `ASSET-PROMPTS.md` (and whether the late-summer fly agaric may stay).
4. The address on the plaque without the town (it is in the hero): keep, or add `Milharado` back.
