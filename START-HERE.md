# Start here (Tomás and Maya, and your Claudes)

This folder is a shared copy of the wedding invitation work. It holds no guest list, no codes, no keys.

## For Maya (not a programmer)

1. Open the live test page on your phone: <https://convite-test.tominacio99.workers.dev/>. It has placeholder guests and wording.
2. Tell your Claude what you like and what you do not, in plain words. It knows how to read this folder.
3. Your Claude proposes changes on its own branch and sends you screenshots. Nothing reaches the live invitation until you and Tomás both say yes.

## For a Claude opening this folder

1. Read `CLAUDE.md` (hard rules), then `STATE-FOR-MAYA.md` (what exists), `DESIGN-SPEC.md` (fonts, palette, art style, checklist) and `SPEC.md` (Tomás's exact words).
2. Maya already built most of the RSVP backend. This copy has Tomás's version (`rsvp/`); compare, and say where yours is better and what would clash. Merging the backend comes later.
3. Aesthetic taste decisions go to the people, as a short picker question with 2 to 3 options. Do not guess.
4. Work on a branch named `maya/<topic>`. Do not push to `main`, deploy, or touch the live GitHub Pages page. No credentials, no accounts.
5. Copy (names, wording) is the couple's. Mark placeholders `TODO(user)`. Do not invent it.
6. New art follows the one canonical style lock in `DESIGN-SPEC.md` section 6.

## What was left out on purpose

Guest list and codes, API keys, large raw image generations, older build versions, photos of people, private backlog notes. Ask Tomás if you need any of them.
