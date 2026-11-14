# Start here (Tomás and Maya, and your Claudes)

This is the whole wedding invitation project, shared as if Maya and Tomás were two accounts of the same person. Nothing is withheld: guest list and codes, backlog, hand-off notes, every image generation, older builds, references. Only rebuildable tools (`.venv`, `node_modules`, `.tools`) and secrets that never lived in the project (API keys, the Cloudflare login) are not here. Keep the repo private.

## For Maya (not a programmer)

1. Accept the GitHub invitation and give the repo link to your Claude.
2. Open the live test page on your phone: <https://convite-test.tominacio99.workers.dev/> (placeholder wording).
3. Tell your Claude what you like and do not like, in plain words.
4. Changes land on a branch (`maya/<topic>`) with screenshots. Nothing reaches the live invitation until you both say yes.

## For a Claude opening this folder

1. Read `claude-context/WORKING-STYLE.md` (how Tomás works with Claude), then `CLAUDE.md` (hard rules), `STATE-FOR-MAYA.md` (what exists), `DESIGN-SPEC.md` (fonts, palette, art style, checklist), `SPEC.md` (his exact words), `HANDOFF.md` and `BACKLOG.md`.
2. `claude-context/` holds Tomás's memory notes and global Claude rules, so you can behave like his Claude.
3. Maya built most of the RSVP backend herself. This copy has Tomás's version (`rsvp/`); compare and say what is better and what would clash. Merging the backend comes later.
4. To rebuild the page: set up the Python venv as in `scripts/env.sh` and `rsvp/README.md`, then `comps/art/site_build.py` (see its header).
5. Work on a branch, no pushes to `main`, no deploys, no credentials, no accounts.
6. Tomás refreshes this copy with `scripts/share_with_maya.sh`. Pull before you start.
