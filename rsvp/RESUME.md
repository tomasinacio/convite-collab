# Resume notes (2026-11-12)

Owner: Tomas. Review date: 2026-11-19. Rollback: `rm rsvp/RESUME.md`.

Read this first in a new session started with `./start.sh`. The full record is `SPEC.md` (Messages 32 to 54), `rsvp/OBSERVATIONS.md` (register) and `rsvp/comps/DESIGNER-NOTES.md`.

## Where things stand

- The v16 page (`comps/prototype.v16.src.html` plus `rsvp/page/info.*` and `rsvp.*`) is built and fixed after three reviews. Nothing is deployed; `build/convite-publish` and the live page are untouched. Test links (Cloudflare `convite-test`, `rsvp-test`) still show the old test build.
- Real paintings are missing: the page shows no stand-ins; slots wait for files from `rsvp/comps/ASSET-PROMPTS.md` (rewritten on 2026-11-12 for a looser, more hand-drawn look, user message 54).
- Done so far: `assets/inbox/mush-caesar-pair.*` and `m5-mush-fly-agaric-pair.*` (both judged too realistic by the user, so they are only candidates).
- Copilot hit its daily image limit on 2026-11-12 (resets 12:00am). The free `Pollinations` route is not usable (wrong subject, watermark, small).
- New this session: `start.sh` now loads the OmniRoute router key into `OMNIROUTE_API_KEY` for the session (never printed) at the user's request, and `scripts/router_models.py` lists the router's model ids.

## Scope change (user, 2026-11-13, Message 55)

Focus only on the aesthetics of the invitation. The RSVP backend infrastructure is already built by the user's partner; the user will merge our front page and art with it later. Do no backend, Worker, database, workbook or deploy work until the user reopens it. The Copilot run on 2026-11-13: Chrome reconnected and Copilot was signed in; the M1 prompt (Think Deeper) failed with "Your request couldn't be completed. Refresh to try again." No image made yet. Retry M1 later, one prompt at a time, then M5 and the rest.

Update (user, 2026-11-13): Copilot failed four times from the Chrome tab (an error on every prompt, even short ones), and the `desk` key is not loaded unless the session starts through `./start.sh`. The user chose to paste the prompts into Copilot themselves: `rsvp/comps/PASTE-PROMPTS.md` (21 prompts, generated from `ASSET-PROMPTS.md`). Gemini is not to be used (the user dislikes it). When the user says they are done, take the newest files in `/mnt/c/Users/tomin/Downloads` in the order of that file, then run the quality gate, the cut-out, the `assets/LOG.md` row and the judging rules, and place them in the page slots.

## Next actions

Update (user, 2026-11-12 evening): drop the router idea for now ("fuck it, just wait till midnight and make the new pics"). A one-shot task is scheduled in the open session for about 12:07am on 2026-11-13 to generate the new set in Copilot; if that session was closed, do step 3 by hand. `start.sh` still loads the router key if the user restarts through it.

1. List router models: `.venv/bin/python -I scripts/router_models.py gemini image imagen flux`. Ask the user which Gemini free image combo to use (they said they believe a Gemini free model can make pictures).
2. Set `OMNIROUTE_IMAGE_MODEL` to it and test one asset (M2) with `scripts/free_image.py --route omniroute --no-style --prompt-file FILE OUT` using the style lock from `ASSET-PROMPTS.md`. Judge with the rules in `ASSET-PROMPTS.md`; never use a result that fails them.
3. If it works, make the rest of the set (M2, M3, M4, B1, P1, B2, F1 to F4, T1, T2, L1 to L3, R1 to R3, B3), quality gate, cut out, log in `assets/LOG.md`. If not, Copilot after midnight (Think Deeper, one prompt at a time; stop at any human check or limit; never click upgrade).
4. Put the assets into the page slots (`PENDING` list in `rsvp/page/info.css`), then run `consistency-red-team`, `red-team` and `spec-guardian` again, show screenshots to the user and ask them to approve with the picker before updating the test links.

## User rules that still apply

Picker for taste questions, short messages, each fact once on the page, one coherent painted look, fake data marked and listed in `rsvp/comps/REPLACE-ME.md`, no credentials typed or read, no accounts created, commit and deploy only when asked.
