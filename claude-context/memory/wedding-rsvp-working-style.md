---
name: wedding-rsvp-working-style
description: How the user wants the wedding invitation work run: picker questions, cost, no repeated facts, coherent aesthetic, reviewers, a register of observations
metadata:
  type: feedback
---

The user (on a phone, cannot run bash) gave these rules during the RSVP work on 2026-11-12. Verbatim words are in `projects/wedding-invite/SPEC.md` Messages 38 to 49; the running register is `projects/wedding-invite/rsvp/OBSERVATIONS.md`.

- Ask open questions with the tap picker (AskUserQuestion), a few at a time with sensible options, never a long message to answer. Ask what they might know (times, schedule, contacts) before inventing.
- Spend conservatively: one design concept at a gate, reuse earlier work, do not repeat captures or rebuilds.
- No fact is said twice on the page (date, place, names, address, deadline). The face itself repeats the date and place; keep one.
- Keep one coherent painted aesthetic (paper tone, azulejo style, type); flat vector azulejo tiles looked cheap. Run `consistency-red-team` at every design gate.
- The Opus designer owns taste; the user picks. Use the reviewer agents on the whole page, not only on code.
- Fake test data is fine if every piece is marked (`data-fake`) and listed in `rsvp/comps/REPLACE-ME.md`.
- Write every user message and every finding into SPEC.md or OBSERVATIONS.md so nothing is lost.

**Why:** the user got frustrated when the date and place repeated, when a heads-up was missed, and when work looked hasty and thin compared with the reference invitations.

**How to apply:** before building or replying on this project, re-read the register and the Messages in SPEC.md; check each new design against them.
