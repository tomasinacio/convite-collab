# How Tomás works with Claude (copy this behaviour)

Written 2026-11-14 from the working sessions. Maya's Claude should behave the same way, as if it were a second account of Tomás.

- He is on a phone most of the time. Short messages. Never long walls of text.
- Taste decisions go to the people through the option picker (`AskUserQuestion`): few questions, 2 to 3 concrete options, a recommended first. Ask what they might know, not what a designer decides.
- Aesthetics go to an Opus 5.5 agent at high effort. Mechanical work can use any tier.
- Spend tokens frugally. No extra agents or long retries for small things. Stop when a path fails twice and say so.
- Copy (names, dates, wording) is the couple's. Mark placeholders `TODO(user)`; fake data only if marked `FAKE`.
- Each fact appears once on the page. One coherent painted-watercolour look; the face's wheat, lavender and olive are the gold standard.
- Run the reviewers (`red-team`, `consistency-red-team`, `spec-guardian`) before showing a design.
- Register every user instruction in `SPEC.md` verbatim and every observation in `rsvp/OBSERVATIONS.md`.
- Never type or read credentials. Account creation, payments, OAuth consent and sending messages for them need an explicit yes in chat.
- Commit and deploy only when asked. Pushes to the live GitHub Pages site need a clear yes.
- When a session ends with `SESSION S<nn> DONE ...`, paste the contents of the next-prompt file in its own code block.
- Images: Copilot (copilot.com) with Think Deeper worked best; paste prompts, save into `assets/inbox/`, then quality-gate, cut out, tone to the paper (`#F6EFDF`) and log in `assets/LOG.md`. Prompt template: `rsvp/comps/PASTE-PROMPTS-COPILOT.md`. Higgsfield only works through a Claude chat, one image at a time; too costly.
- Quick test page: Cloudflare `convite-test` (see `rsvp/README.md`). Live page: `tomasinacio/convite` on GitHub Pages.

See `START-HERE.md`, `STATE-FOR-MAYA.md`, `DESIGN-SPEC.md`, `SPEC.md`, `HANDOFF.md`.
