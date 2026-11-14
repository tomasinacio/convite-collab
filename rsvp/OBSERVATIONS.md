# Observations register

Owner: Tomas. Written 2026-11-12. Review date: 2026-11-19. Rollback: `rm rsvp/OBSERVATIONS.md`.

Every observation from the user, the reviewers and the research, so none is lost. The user's exact words are in `SPEC.md` (Messages 32 to 54). Status: done, in progress, open (waiting for the user) or watch. Add a row whenever something new is said or found.

## From the user

| ID | Source | Observation | Status | Where |
| --- | --- | --- | --- | --- |
| O1 | M38 | The five reference invitations are the gold standard for structure and aesthetics, Dolce Vita first | in progress | designer pass, `rsvp/comps/DESIGNER-NOTES.md` |
| O2 | M39 | Venue address from the map link | done, confirm | `rsvp/comps/REPLACE-ME.md` |
| O3 | M40 | Fake data is fine for tests if marked, so the user can replace it | done | `data-fake` marks, `rsvp/comps/REPLACE-ME.md` |
| O4 | M40 | Fake guest data for tests | done | workbook, `rsvp/guests/README.md` |
| O5 | M43 | Spend conservatively: one concept, reuse work | adopted | R36 |
| O6 | M44, M45 | Never repeat the date, place or any fact on the page; the opening itself repeats them (top block and the block under the dogs) | in progress | R34, designer pass, `consistency-red-team` |
| O7 | M45, M49 | Ask what the user might know, with the picker, a few questions at a time, never a long message | adopted | R37 |
| O8 | M45 | A reviewer that finds inconsistencies of aesthetics, color and repetition | done | `.claude/agents/consistency-red-team.md`, to run at each gate |
| O9 | M41 | Remove the replay button | in progress | designer pass |
| O10 | M41, M42 | The opening takes too long (plants, fruit, falling leaf); target about 5 seconds | in progress | designer pass |
| O11 | M41 | Missing a big chunk of content compared with the references; information belongs in the middle | in progress | designer pass |
| O12 | M41 | The page is too light compared with what it should be | in progress | designer pass |
| O13 | M41 | Keep the aesthetic; the Opus designer maintains it | watch | every gate |
| O14 | M41 | The paper tone changes between the opening and the form | in progress | designer pass |
| O15 | M41 | The work was hasty; use the reviewer tools | adopted | reviewers at every gate (R33, R35) |
| O16 | M42 | Sections: countdown, location and map, schedule, dress code, add to calendar, gifts with the IBAN, FAQ | in progress | designer pass |
| O17 | M42 | Answers: schedule (15:00 arrival, 16:00 ceremony, 20:00 dinner, 23:00 cake, then party), formal dress code with no palette, deadline 30 April 2027, IBAN without a holder name, two WhatsApp contacts, FAQ parking, no menu choice, a draft opening line | done, passed to the designer | `rsvp/rsvp-config.json`, `rsvp/worker/wrangler.toml` |
| O18 | M46 | More living, coherent assets: bees, tree trunks, mushrooms (the emphasis), things entering from the sides, falling leaves, swaying leaves and branches; prompts from the designer | in progress | `rsvp/comps/ASSET-PROMPTS.md` |
| O19 | M46 | Add rocks too | in progress | `rsvp/comps/ASSET-PROMPTS.md` |
| O20 | M47 | The flat `azulejo` tiles look cheap; keep one or two; add a researched rodapé and a bigger `azulejo` plaque for information in the style of the names plaque | in progress | designer pass, research job d1 |
| O21 | M48 | Use more researcher agents on what was said, and register every observation | done | `rsvp/kit/swarm-design.jobs`, this file |
| O22 | M42 | The user asked for Portuguese invitation references for the IBAN gift section | in progress | research job d2 |
| O23 | M50 | Long term, one of the final things: the invitation of `Pedro Rodrigues` is invaded by `Shreks` (dancing, ugly, and so on) | backlog, not started | `BACKLOG.md` item B1 |
| O24 | M51 | The user likes three mushroom pictures (grey `inkcap` cluster and spotted cap, red-capped `russula` with gills, red fly agaric pair, tall pink-capped mushroom with dark gills); use that look for the mushrooms | in progress | `references/inspiration/mushrooms/`, designer pass |
| O25 | M51 | More wild flowers, ideally native to Portugal | in progress | designer pass, `rsvp/comps/ASSET-PROMPTS.md` |
| O26 | M52 | Use the better Copilot model for image generation | done | Copilot mode set to Think Deeper (the other choices were Auto and Quick Response) |
| O27 | M52 | Summer: the page and its plants should feel like July in Portugal (read as the season of the wedding; confirm with the user if it meant something else) | in progress | designer pass |
| O28 | M53 | The mushroom pictures guide the shapes and species only; colors and style can change to fit our mood | in progress | designer pass, O24 |
| O29 | M53 | Add one tied bunch of hot peppers, as common in rural Portugal | in progress | designer pass, `rsvp/comps/ASSET-PROMPTS.md` |
| O30 | M54 | The Copilot images (Caesar's mushrooms, fly agaric) are slightly too realistic and AI-glossy; more watercolor and drawing like | in progress | designer rewrites the style lock before the next generation, R41 |
| O31 | M55 (picker) | The user asked to find a working image avenue and thinks free `Gemini` can build pictures; Chrome extension was disconnected when I tried the `Gemini` web app | open | needs the Chrome extension reconnected on the PC |
| O32 | picker | The user chose to load the router key through `start.sh` so images can use the OmniRoute Gemini free combo; a direct read of the key file was blocked and not worked around | in progress, needs a restart with `./start.sh` | `start.sh`, `scripts/router_models.py`, `rsvp/RESUME.md` |
| O33 | chat, 2026-11-14 | The new parts feel too compacted, their assets too small, all over the place and not in line with the progress so far; "it really feels unprofessional now"; compare them with `Dolce Vita` and with the agreed face | done, waiting for the user's look | `rsvp/comps/REVIEW-DOLCE-VITA.md`, `DESIGN-SPEC.md` sections 4 and 6 |
| O34 | chat, 2026-11-14 | Not too crowded; keep the art he added (wheat, lavender, olive, orange branch, swallows, names plaque, `rodapé`); assemble the rest as an experienced web designer would | adopted | same |

## From reviewers and tests

| ID | Finding | Status | Where |
| --- | --- | --- | --- |
| R1 | Spec audit: helper scripts picked up by `node --test`, address unmarked, no recorded final checks | done | `rsvp/worker/tools/`, `rsvp/comps/REPLACE-ME.md`, `rsvp/README.md` |
| R2 | Red-team: draft leaked between households, hung request, reduced-motion rule hit the face, code entry feedback, wrong screens for server replies, long answers overflow, honeypot autofill, draft kept too long, triple announcement, prop over counter, all-decline message | done | `rsvp/page/form-checks.cjs` |
| R3 | First load of the existing page is about 1846 KB against a 1500 KB budget | open, the designer is asked to reduce it | `rsvp/README.md` |
| R4 | Seam between the face paper and the form paper | in progress | O14 |
| R5 | Guests without JavaScript see only a message and the contact buttons | open, assumed fine unless the user objects | `rsvp/PLAN.md` |
| R6 | The venue card has no heading for screen readers in the test copy | in progress | designer pass |
| R7 | Red-team v16 (6/10): living assets are stand-ins (mushroom slot uses a bloom image, bee uses a swallow, peppers use an olive twig) | open, waits for the painted assets | `rsvp/page/info.css` lines 101 to 111 |
| R8 | Red-team v16: the middle sections repeat one centered template seven times; the big chunk is still light | open, to the designer | `v2-count`, `v2-dress`, `v2-gift` |
| R9 | Red-team v16: too many `azulejo` pieces; the address plaque reuses the names frame one screen later (user asked for one or two flat tiles) | open, to the designer | `info.css`, M47 |
| R10 | Red-team v16: schedule items in script type; headings use navy not in the palette; olive only on buttons | open, to the designer | `info.css` |
| R11 | Red-team v16: facts repeat (`Quinta do Grilo` in the hero and on the gate plaque; `Traje formal` heading then body) | open, user decision 5 of the designer list | M44, M45 |
| R12 | Red-team v16: gate wall plus four dogs read as a second hero, with a gap below the FAQ; a squashed terracotta shape at 0 s of the second sequence; the `rodapé` sits on a paler strip (seam) | open, to the designer | `v2-open-compare` |
| R13 | `consistency-red-team` v16 (6/10): the page foot flora never renders (`--pu` is defined only on `.info`, so height is 0); hard straight edges at the gate art, the wheat and the willow; the tile appears 7 times; the rodapé is used as a mid-page divider; the address plaque is the names plaque art; colours outside the tokens (`#1B2556`, `#344680`, `#FBF7EE`, `#8A7358` and others) and the `html` background grey-green; the RSVP card heading is the only serif headline; the pressed seal keeps its box at 200% zoom (sideways scroll); the olive twig covers a label at 195 pixels; wording repeats (`reply` twice in en, July again in the weather answer) | open, to the designer | v16 shots, `info.css` |
| R14 | `spec-guardian` v16: NOT READY. R34 fails (`Quinta do Grilo` on the hero and the gate plaque; `Traje formal` in heading and body); stand-ins stay in place of mushrooms, bees and peppers; the fake opening line on the face was not counted by `site_build.py` (fixed by the main session); research jobs d1 to d5 failed; the README still said 1846 KB (measured 1448 KB before the tap, 1810 KB after) | partly fixed | `site_build.py`, `rsvp/README.md` |
| R15 | User picks (picker, 2026-11-12): keep the painted gate sign `Quinta do Grilo` as art; the Caesar's mushroom style is right, continue the set; include the fly agaric | done | R11 resolved; `rsvp/comps/ASSET-PROMPTS.md` |
| R16 | Designer fix pass on R7 to R14 done (stand-ins removed, tokens only, two tiles, left-aligned schedule, hard edges faded, 200 percent zoom fixed); `consistency-red-team` and `spec-guardian` still to re-run after the real assets are in | in progress | `rsvp/comps/DESIGNER-NOTES.md`, `rsvp/comps/shots/` |
| R17 | Copilot reached its daily image limit on 2026-11-12 ("check back at 12:00am") after M1 and M5 plus two test images; one human-check wall earlier was cleared by the user; no upgrade clicked. Remaining 19 assets (M2, M3, M4, B1, P1, B2, F1 to F4, T1, T2, L1 to L3, R1 to R3, B3) wait for the reset or the free fallback | open, user choice | `assets/LOG.md`, `rsvp/comps/ASSET-PROMPTS.md` |
| R18 | Free fallback tried on 2026-11-12 after the user picked it: `Pollinations` returned a wrong subject, 768 pixels and a watermark for M2; no other route has a key (Cloudflare, Hugging Face, Gemini, OpenRouter, `OmniRoute` all unset), so the free route is not viable for the set | closed, not viable | `assets/LOG.md` |
| R19 | `red-team` on the rebuilt new parts (5/10, 2026-11-14): no centrepiece per section, bare paper between sections, the schedule template-like, edge pieces zigzag, paintings repeat, generic interface, the gate wall the most saturated block | mostly done; declined items and reasons in the review | `rsvp/comps/REVIEW-DOLCE-VITA.md` |
| R20 | `consistency-red-team` on the same (7/10): repeated face paintings, no air round the tile pause, `Como chegar` without a head, RSVP head spacing and tracking, a second rule, units weight, the leaf against the scale rule | done except the script card heads and the button shapes (approved RSVP look) | same |
| R21 | The gate wall's yellow (frozen face) is the strongest colour on the page | open, user decision | same, "For the user to decide" |

## Research (free lanes, hints only, checked at source before use)

| Job | Question | Output |
| --- | --- | --- |
| d1-azulejo-rodape | `rodapé` and `barra` patterns, painted look | failed, no output; the designer researched it directly |
| d2-gift-iban | how Portuguese invitations word and present money gifts with an IBAN | failed, no output (the designer researched it directly) |
| d3-woodland-motifs | watercolor mushrooms, bees, trunks, rocks; Iberian species and colors | failed, no output (the designer researched it directly) |
| d4-prompt-style-lock | prompts that keep a watercolor asset set consistent | failed, no output (the designer researched it directly) |
| d5-ambient-nature-motion | calm ambient motion recipes and performance rules | failed, no output (the designer researched it directly) |
| d6-page-coherence-audit | tools to find repeated facts, color drift and seams | hints only in `rsvp/kit/runs-design/d6-page-coherence-audit.md`; `report.md` there is a failed run's log |

## Still open for the user

Real wording in pt-PT, en and es; the real guest list; the address OK; whether JavaScript-off guests seeing only the contact buttons is fine; approval of the asset prompts; the decision to push the finished page to GitHub Pages.
