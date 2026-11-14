# Review: `Dolce Vita` against ours, and the new parts against the face

Owner: Tomas. Written 2026-11-14 by the Opus art director. Review date: 2026-11-28. Rollback: `rm rsvp/comps/REVIEW-DOLCE-VITA.md`; the page changes are listed under "What changed".

The user, 2026-11-14: "It feels too compacted and at the same time the assets are too small in the new parts", "really all over the place and not in line with all of the progress that we did so far", "It really feels unprofessional now". Earlier: not too crowded; keep the art he added (wheat, lavender, olive, orange branch, swallows, the `azulejo` names plaque, the `rodapé`).

Verdict in one line: the new parts were a flat web template with stickers on it, hung on a painted face. They now read as the same painted card: one axis, more air, fewer repeats and pieces at the face's own scale. They still carry less painting per section than `Dolce Vita`, because we have no scene paintings.

## How it was measured

- Playwright (`playwright-core` on the project's Chromium 1252, local libraries from `scripts/env.sh`) at 390 x 844 (2x, touch) and 1280 x 900.
- Each invitation was opened as a guest opens it: the seal or envelope tapped, 6.5 to 8 s of wait, then the whole page scrolled so that lazy art and entrances ran. Then one shot per screen and per section, the computed type and boxes from the page, and each prop's painted size from its image alpha (not its box).
- `Dolce Vita` is the invitation inside the shop's demo frame: `https://dolcevita-demo.thedigitalyes.com/`. `Floral` and `Mediterranean Edition` were shot the same way as a second opinion on structure.
- Ours before: the v17 test build of the morning (`rsvp/comps/shots/v5-*.jpg`). Ours after: `rsvp/comps/shots/v6-*.jpg` (390, one per section), `v6-1280-*.jpg` (wide screen) and `v6-full.jpg`.

## Table 1: `Dolce Vita`, measured at 390 x 844

| Section | Height (screens) | Padding top / foot | Painted pieces: size in pixels (share of the 390 width), place |
| --- | --- | --- | --- |
| Hero (video) | 844 (1.00) | 0 / 0 | arch of tiles, lemons and a lake town, full bleed |
| Countdown | 372 (0.44) | 64 / 64 | a painted striped ground across the whole section |
| Pets interlude | 245 (0.29) | 48 / 16 | one group, 240 x 181 (62 %), centred |
| Location | 1484 (1.76) | 20 / 64 | lemon 128 x 140 (33 %, off the left edge); ribbon 390 x 312 (100 %); church 278 x 205 (71 %); rings 112 x 116 (29 %); cocktail 110 x 166 (28 %, off the edge); villa 278 x 190 (71 %); ribbon 390 x 248; beach chair 112 x 162 (29 %) |
| Schedule | 1019 (1.21) | 10 / 40 | a ring rising 102 pixels into the section above; one drawn path of the day 310 x 764 (79 %) |
| Dress code | 782 (0.93) | 50 / 20 | fan 96 x 77 (25 %) top left; parasol 128 x 115 (33 %) top right; guests 326 x 133 (84 %) |
| Accommodation | 902 (1.07) | 64 / 0 | saxophone 140 x 167 (36 %) and violin 94 x 163 (24 %) flanking the head, rising 58 to 69 pixels into the section above; manor 320 x 314 (82 %) |
| Transport | 1294 (1.53) | 0 / 20 | birds 160 x 147 (41 %); bus 320 x 467 (82 %) |
| Gifts | 850 (1.01) | 1 / 64 | globe 128 x 175 (33 %); balloons 96 x 145 (25 %, off the edge); bouquet 96 x 131 (25 %) |
| RSVP | 1559 (1.85) | 0 / 30 | ribbon 390 x 312 framing the head; swans 208 x 129 (53 %); ribbon 390 x 248 |
| Footer | 771 (0.91) | 0 / 0 | couple 208 x 139 (53 %); manor painting 390 x 484 (100 %) |
| Whole page | 10234 pixels, 12.1 screens | | one lead painting per section (53 to 84 %) plus one or two accents (24 to 41 %); art covers 15 to 68 % of each section's area, the countdown 100 % |

- Type: heads `Beth Ellen` 36 pixels over a 41 pixel line (a wide script, so it looks bigger); kickers `Greycliff` 11 pixels, tracking .35em, capitals; body 15 to 16 pixels over 25.5 to 26 (1.6 to 1.7); figures `Meursault` 44 pixels at weight 300; labels 10 to 11 pixels, tracking .25 to .3em; a 60 pixel rule under each head; no rule between sections.
- Rhythm: one section per screen, each 0.9 to 1.9 screens tall; 100 to 330 pixels between the text of two sections, filled with art about half the time.
- Wide screen (1280 x 900): 14481 pixels (16 screens); text column 656 pixels; heads 60 pixels; lead paintings 448 pixels; padding 112.
- Weight: 3603 KB before the tap, 20.4 MB after a full scroll; every section is static (the hero is a video loop).
- `Floral`: 5.7 screens, small wildflower sprays bleeding off both edges (about 25 %), a heart between two hairlines as the divider, heads centred. `Mediterranean Edition`: 9.7 screens, line-art emblems 80 to 130 pixels (25 to 33 %) centred over each head, one framed timeline. Both keep a single centred axis.

## Table 2: ours against `Dolce Vita`, section by section (390 x 844)

Heights in pixels and phone screens; art as the painted width (share of the 390 width).

| Section | `Dolce Vita` | Ours before | Ours after |
| --- | --- | --- | --- |
| Page length | 12.1 screens, 10 sections after the hero | 6.8 screens; the six information sections in 3.3 | 8.1 screens; the six information sections in 4.5 |
| Air between two sections | 64 + 64, plus art | 52 + 60 and a 1 pixel hairline (113) | 72 + 72 (144), art in part of it; no hairline |
| Axis | centred, always | centred, centred, left, left, centred, left, centred (4 changes) | centred, always |
| Where | church 71 %, villa 71 %, two ribbons, accents; 1.76 screens | kicker only, plaque 90 %, two buttons; 0.50 | script head and rule under the face's hanging vine and eucalyptus, plaque 90 %; 0.75 |
| Countdown | painted ground; 0.44, then a 62 % painted interlude | bee 23 pixels (6 %), fly agarics 43 (11 %) at a hairline's end; 0.38 | bee 46 (12 %) above the kicker; fly agarics 116 (30 %) as a centred vignette; 0.64 |
| Schedule | one drawn path 79 % wide; 1.21 | left list with six 44 pixel circled line icons; wheat 66 (17 %) and lavender 47 (12 %); 0.72 | centred printed programme on a twine thread; wheat 127 (33 %) with wild carrot 92 (24 %); 0.91 |
| Pause | none (art carries it) | five hairlines between sections, one tile | one painted tile with 48 pixels of its own each side |
| Dress code | fan 25 %, parasol 33 %, guests 84 %; 0.93 | head, then a 38/62 grid of orange vignette (39 %) and note; 0.41 | orange branch 60u entering from the left edge above the head (193 pixels on screen, 49 %); centred note; 0.51 |
| Gifts | globe 33 %, balloons 25 %, bouquet 25 %; 1.01 | fig 101 (26 %) in the corner; card; 0.67 | fig 64u entering from the right edge above the head (211 on screen, 54 %); card; 0.82 |
| Questions | (no section) | left head; peppers 31 (8 %); 0.52 | centred head; peppers 77 (20 %) hanging above the kicker; 0.66 |
| RSVP | ribbon frame 100 %, swans 53 %; 1.85 | twig 27 pixels painted in a 152 pixel box (7 %), lavender 17 %; rule, lead, rule, card; 1.32 | olive twig 59 x 211 (15 %); lead 36 pixels under the head; no second rule; 1.31 |
| Foot | couple 53 %, painting 100 %; 0.91 | carrot 59 (15 %), lavender 43 (11 %); 0.12 | pebbles 116 (30 %), lavender 81 (21 %) on the `rodapé`; 0.24 |
| Art share of each section's area | 15 to 68 % (countdown 100 %) | 1 to 12 % (the plaque section 31 %) | 6 to 19 % (the where section about 38 % with the face's vine and eucalyptus) |
| Heads | 36 pixel wide script | `Allura` 58.5 pixels (a narrow script) | unchanged; `Como chegar` gains one |
| Kickers | 11 pixels, .35em | 13 pixels, .28em | unchanged |
| Body | 15 to 16 / 1.7 | 19 / 1.6 | unchanged; measure `26rem` |
| Figures | 44 pixels, light | 46.8 pixels, units weight 400 | units at the role's weight 500 |
| Wide screen | text 656, art 448 | text 536 in a 576 column, art at phone scale; the face is a 440 column | everything in the face's 440 column; the cut ends dissolve |
| First load | 3603 KB | 1460 KB | 1463 KB (the art loads one screen ahead) |
| Motion | static below the hero | small pieces enter and sway | the same hooks, now on large pieces; rooted pieces fade only |

## Table 3: the new parts against the old, agreed face

The face (the closed letter, the seal, the opening, the names plaque, wheat, lavender, olive and orange branches, swallows, the land, the gate with the dogs, the `rodapé`) is the gold standard.

| Point | The face (agreed) | New parts before | New parts after |
| --- | --- | --- | --- |
| Spacing and rhythm | one continuous painted world, 1.24 screens, then the gate 0.81 | 0.38 to 0.72 screens a section, 113 pixels between, two or three heads on one screen | 0.51 to 0.91 a section, 144 pixels between, one composition per screen |
| Axis and composition | strictly symmetric: a centred plaque framed by branches in both top corners and grass at both sides | four changes of axis in seven sections; left script heads | one axis; each section framed from one side, the side alternating down the page, as the face's corners |
| Type scale | names 34 pixels, capitals, weight 600; date 19 italic; place 23; village 12.5 capitals .24em; script only on the painted gate sign | `Allura` heads 58.5 everywhere; schedule moments 20 at weight 500 next to app icons | heads unchanged; the schedule now borrows the face's own roles: time as the village line, moment as the place line (22 pixels, weight 400) |
| Paper tone | one tone, `#F6EFDF` with the paper tile | the same (no seam) | the same; sampled at every boundary 239 to 248, 232 to 242, 216 to 226 (grain), within tolerance |
| Ornament weight | painted only; no lines, no interface chrome but the seal and Skip | about 20 thin lines on 3.3 screens: 5 hairlines between sections, 6 head rules, the clock's 2, the timeline's 6 links and circles | head rules, the clock's 2, the programme's 5 thread links, one tile pause; no section divider |
| Colour saturation | olive 95th-percentile saturation 0.44; the oranges carry the colour | pieces too small to carry colour; the page read as cream and brown | new pieces at 0.44 (fig) to 0.68 (fly agarics), under the 0.70 cap; colour in every screen again |
| Prop scale | swallows 4 to 9u, grasses 20 to 30u, lavender 18u, vine 38u, eucalyptus 40u, orange 58u, olive 70u, panel 78u, land 118u | 6 to 26u (bee 6u, peppers 8u, fly agarics 11u, lavender 12u, carrot 15u, wheat 17u, fig 26u) | bee 12u, twig 15u, peppers 20u, lavender 21u, carrot 24u, fly agarics and pebbles 30u, wheat 34u, orange 60u, fig 64u |
| Prop density | about 12 pieces a screen | 1 or 2 small pieces a screen | 1 or 2 large pieces a screen (restraint kept: 10 pieces in the information, RSVP and foot, the same count as before) |
| Repeats | each painting once | lavender four times (face, schedule, RSVP, foot); the schedule's wheat and lavender copied the face panel's right side | no painting twice below the face; the orange branch and the olive twig return once each, mirrored or alone |
| Edges | every cut end dissolves (masks) | cut ends hard at the wide-screen column edge | every bleeding piece dissolves at its cut end; rooted pieces dissolve at the root |
| Motion feel | drawn wipes and settles in 1.2 s; sways 0.6 to 2.2 deg over 4.3 to 7.3 s; the opening in about 5 s | the same hooks on tiny pieces, so the motion barely read | side entrances 1.2 s; sways 0.9 to 1.4 deg over 5.3 to 7.1 s, none in step; mushrooms and pebbles fade only; the bee flies in once from the left |
| Polish | no element touches another | the RSVP twig a 27 pixel sliver; the mushrooms floating at a hairline's end; the address with no head | nothing paints over a text line or a control at 390, 360, 195 and 1280, measured on the painted alpha, the face's vine and eucalyptus included |
| Wide screen | a 440 pixel painted column | a wider 576 column under the face's 440 | the face's 440 column for everything |

## What made the new parts feel unprofessional

Ranked by how much each one cost. Each item names what in our own progress it broke and what was done.

1. **Sticker-scale art (critical).** The pieces were 6 to 26 % of the width (23 to 101 pixels), and art covered 1 to 12 % of each section. The face's pieces run 18u to 118u; `Dolce Vita`'s lead paintings run 53 to 84 %. Broke: `DESIGN-SPEC.md` section 6 ("one lead painted subject per section") and the user's Message 46 ("make it feel alive"). Done: every piece 2 to 3 times larger and re-cut from the user's paintings at 2.3x to 3x display. Branches now 60 and 64u, entering from an edge as the face's own do.
2. **Compressed rhythm (critical).** There were 113 pixels between sections and each section was 0.38 to 0.72 screens tall, so one phone screen held the countdown figures, the whole schedule and the next head. Broke: the "generous air between sections" taken from `Dolce Vita` (`DESIGNER-NOTES.md`). Done: a spacing scale with 72 pixels at each section's top and foot (96 on a wide screen), room for each painted band, and one composition per screen.
3. **The axis flip-flop (high).** The sections went centred, centred, left, left, centred, left, centred, with script heads hung on the left like a blog. Broke: the face's symmetry and Message 14 ("not ... all over the place"). Done: one centred axis; variety now comes from the side each painting enters from, not from the text.
4. **The painted world stopped at the vine (high).** After `Como chegar` the page turned into flat paper and text, with no piece entering from an edge. Broke: Message 41 ("keep with the aesthetic") and observation O13. Done: branches enter from alternating edges above the heads, as the face's corners do. Plants stand at section feet with dissolving roots, as the face's grasses do.
5. **Interface furniture (high).** The schedule had six 44 pixel circled line icons, an app pattern, and there were about 20 thin lines on 3.3 screens. Broke: the flatness the user rejected for the tiles (Message 47, "super cheap looking"). Done: the schedule became a centred printed programme in the face's own type roles, the hairlines between sections went, and one painted tile is the only pause.
6. **The same paintings repeated (medium).** The lavender showed four times. The schedule copied the face panel's wheat and lavender cluster. Broke: the decision log's "the same painting shows three times" limit. Done: the RSVP lavender went, the schedule got the wheat with the user's wild carrot, and the foot got the never-placed pebbles with the lavender's one showing.
7. **Floating and tiny details (medium).** The mushrooms stood on the end of a hairline at 43 pixels, the RSVP twig was a 27 pixel sliver, and the bee was a 23 pixel speck. Broke: section 5 ("standing on a base line, never floating"). Done: the mushrooms became a centred vignette closing the countdown (30u), the twig shows at 15u, and the bee is 12u, mirrored so it flies in from the left.
8. **Wide screen (medium).** The information sat in a 576 column under the face's 440, with phone-scale pieces floating in it and hard cut ends. Done: the face's 440 column for the information, the RSVP and the foot, and every cut end dissolves.
9. **Anatomy slips (low).** `Como chegar` had no head (a kicker 20 pixels over the plaque). The RSVP lead sat 26 pixels under its head with a second rule below it. The countdown units were at weight 400 against the role's 500. Done: all three corrected. The new head sits below the face's hanging vine and eucalyptus, which had painted over it by 846 square pixels.

## What changed

- `rsvp/page/info.html`: one centred anatomy; `Como chegar` as a script head; the schedule without icons; the orange branch as a prop; the fly agarics in the flow under the countdown; the wild carrot in the schedule; no hairline between sections.
- `rsvp/page/info.css`: spacing scale (`--s1` to `--s6`, `--sec`); the 440 pixel column; the prop scale and placements; cut-end and root masks; the countdown units at weight 500; the tile pause with its own air; 200 % zoom keeps only the rooted vignette.
- `rsvp/page/rsvp.html`, `rsvp.css`: the 440 column and `--sec`; the twig at the face's scale; the head's lavender and the hairline after the lead removed; the lead at 36 pixels; the deadline at `.28em`; the foot's pebbles and lavender.
- `comps/art/v17_props_v5.py` and `comps/art/v17/*.webp`: the user's v5 and v6 paintings re-cut at the new sizes (8 to 60 KB each, lossy alpha); `lavender-l.webp` and `olive-twig-l.webp` resized from the face's own mattes. Logged in `assets/LOG.md`.
- `DESIGN-SPEC.md`: the spacing scale, section rhythm, the prop-scale rule, the no-repeat rule, checklist lines and two decision rows. `rsvp/comps/DESIGNER-NOTES.md`: this pass.
- Built into `comps/art/v17-test-site/`. Nothing deployed or committed. The face (`comps/prototype.v16.src.html`) is untouched.

## Reviews and the designer's decisions

`red-team` scored the result 5/10 and `consistency-red-team` 7/10, on the first pass of this redesign. Both ran once.

| Finding | From | Decision |
| --- | --- | --- |
| No centrepiece; pieces 47 to 101 pixels, branches mostly off screen | red team | applied: branches to 60 and 64u, only 10u past the edge (193 and 211 pixels on screen); fly agarics 30u, wheat 34u, peppers 20u |
| 150 to 190 pixels of bare paper between sections | red team | applied: 88 to 72 pixels at each section's top and foot; the art fills part of the rest |
| The schedule is the most template-like block | red team | partly: the programme stays (printed, in the face's roles; the consistency team asked to keep it); the field-edge cluster beside it is larger. A painted scene per moment needs new paintings |
| The zigzag of corner pieces reads as all over the place; drop the bee | red team | declined: the alternating edges are the face's own language and the consistency team asked to keep them; the user chose to keep the bee in the countdown |
| The same paintings repeat; one lavender only | both | applied: no painting twice below the face; the schedule cluster no longer copies the face panel |
| Generic interface: card, pill, plus icons, icons in buttons | both | partly: `Como chegar` head and the second rule in the RSVP fixed; the card, pills, plus and button icons are the RSVP look the user approved (concept A) and stay |
| The yellow gate wall is the most saturated block | red team | not applied: the gate belongs to the frozen face; a question for the user below |
| The tile pause has no air (26 pixels and 1 pixel to the pieces round it) | consistency | applied: 48 pixels of its own each side |
| `Como chegar` breaks the anatomy | both | applied: the script head with its rule, 36 pixels to the plaque |
| RSVP head drift: lead at 26 pixels, deadline tracking, extra hairline; units weight | consistency | applied |
| Card heads are whole sentences in script | consistency | declined: `DESIGN-SPEC.md` section 1 sets card heads in script and an earlier review asked for exactly that; a user taste call if it bothers him |
| Two shapes for the same job (pill and 14 pixel send) | consistency | declined: the approved RSVP form |
| The falling leaf at 4u breaks the "none under 12u" line | consistency | applied: listed as the one exception, as the face's own leaf (3.4u) |

## Checks after the last build

- No painted pixel of any piece (the face's vine and eucalyptus included) over a text line or a control at 390, 360, 195 (200 % zoom) and 1280 pixels; no sideways scroll at any of them.
- First load before the tap 1463 KB (budget 1500); after a full scroll 2935 KB; pieces 8 to 60 KB.
- Only `transform` (`translate`, `rotate`, `scale`) and `opacity` animate; reduced motion leaves every piece at rest and hides the falling leaf; without JavaScript the pieces show at rest.
- `consistency-red-team` measured the paper within tolerance at every boundary, palette tokens only, two fonts only, each fact once in three languages.
- Not checked: a real iPhone, Safari, the `WhatsApp` in-app browser, frame times at CPU 4x, and the `spec-guardian` audit (for the main session).

## For the user to decide

1. The dress code shows the face's orange branch again (mirrored, from the left). Keep it as a deliberate echo of the face, or leave the dress code as a bare pause?
2. The gate wall's yellow is the strongest colour on the page, and it belongs to the frozen face. Leave it, or tone it about 15 % toward sand?

The remaining gap to `Dolce Vita` is painting, not layout: its sections each carry a scene (a church, a villa, a bus). Two or three scene paintings in the face's hand would close it, for example the terrace of the `quinta` or a laid table under the olives. That is a Copilot job for the user when he wants it.
