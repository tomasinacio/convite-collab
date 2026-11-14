# What to replace before the page goes live

Owner: Tomas. Written 2026-11-12 (v16). Review date: 2026-11-19. Rollback: `git checkout rsvp/comps/REPLACE-ME.md`.

Every invented value carries `data-fake` (HTML) or a `FAKE` comment (JS). The site build counts them and refuses a real build while any are left (`--allow-fake` lets a test build through; the v16 test build reports 72).

## Real and kept (no action)

- Names Maya e Tomás, the date 10 July 2027, `Quinta do Grilo`, `Milharado`: in the opening face only, once each.
- Street address `R. Vale de São Gião, 2665-382`, on the information plaque. The town is not repeated there, because the face already says it. The Maps button opens the full address.
- Map link, the IBAN `PT50 0023 0000 4582 0590 0509 4` (checksum checked: valid), the reply deadline 30 April (shown once, without the year, which the face already gives).
- Schedule times 15:00, 16:00, 17:30, 20:00, 23:00 (the user, 2026-11-12; Maya reviews them).
- Dress code: formal, no colour palette. Parking at the venue: yes.
- WhatsApp contacts: two buttons, `Tomás` and `Maya`, from `rsvp/rsvp-config.json` (`whatsapp`, `whatsapp_names`).

## Draft wording to approve or replace

| What | File and key | Status |
| --- | --- | --- |
| Opening line above the names plaque, three languages | `comps/prototype.v16.src.html`, `kicker` in `T` and the `.kicker` paragraph | draft, needs your approval |
| Section kickers and headings (where, countdown, day, dress, gifts, questions) | `rsvp/page/info.js` `T` and `info.html` `data-it` | draft |
| Schedule moment names (arrival, ceremony, cocktail, dinner, cake, party) and the word in place of the party time | `info.js` keys `s1` to `s6`, `s6t` | the moments are yours; the wording is a draft |
| Dress code sentence | `dressText` | draft (says formal, and shoes to dance in) |
| Gift note | `giftText` | draft: short and warm, money welcome, never pushy |
| Copy button and its two messages | `copy`, `copied`, `copyFail` | draft |
| Questions and answers | `q1` to `q3`, `a1` to `a3` | `q1` parking: your fact, draft wording. `q2` partners and children, `q3` weather: invented, for you and Maya to rewrite or drop |
| Button labels Maps and calendar | `maps`, `cal` | draft |
| Calendar event title | `icsTitle` | draft |
| RSVP wording (all states), three languages | `rsvp/page/rsvp.js` `T`, `rsvp.html` `data-i18n` | draft, as before |

## Invented values (not wording)

| What | File | What you supply |
| --- | --- | --- |
| Calendar end time 03:00 (Lisbon) | `info.js`, `DTEND` | the real end of the party, or keep a late guess |
| Countdown target 15:00 on the day | `info.js`, `START` | real (arrival time); change only if the start moves |

## Art waiting for its paintings (not wording)

No stand-in is shown. Each slot below is empty and hidden in `rsvp/page/info.css` (`ASSET SLOTS`, `PENDING`) until its painting from `rsvp/comps/ASSET-PROMPTS.md` arrives; then its slot gets the file and its class leaves the `PENDING` list.

| Slot | Final asset | Where |
| --- | --- | --- |
| `--ia-mush` | mushroom cluster (M1 to M5) | schedule, right base |
| `--ia-bee` | flying bee (B1) | countdown, flies in, then hovers |
| `--ia-peppers` | tied bunch of dried peppers (P1) | countdown, hangs from the top left |
| `--ia-branch-l` | olive branch from the left (L1) | gifts, top left |
| `--ia-rock` | a single stone (R1) | gifts, right base |
| `--ia-fennel`, `--ia-carrot`, `--ia-stones` | wild fennel (F2), wild carrot (F3), pebbles (R2) | page foot, on the `rodapé` |

Shown today, as themselves (the face's own art): the wheat, the lavender, the olive leaf and the orange branch.

## Wording changed in the fix pass

- Dress note: no longer repeats "formal" (pt, en, es).
- Weather answer: no longer repeats "July".
- English RSVP subtitle: "Please let us know by 30 April" (the kicker already says reply).
