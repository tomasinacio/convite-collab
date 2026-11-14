# RSVP: how to run it

Owner: Tomas. Written 2026-11-12. Review date: 2026-11-19. Rollback: `rm -rf projects/wedding-invite/rsvp`.

The design and the decisions are in `PLAN.md`. This file is the practical guide. Nothing here has been run against a real `Cloudflare` account yet; the Worker and the tools are tested locally only (see "What is tested").

## What you need to do yourself

Nobody else can do these, and the assistant never creates an account or sees a password:

1. Create (or log into) a free `Cloudflare` account in a browser. No card is needed for the free plan.
2. Log in from the terminal once (step 2 below). A browser window asks you to approve.
3. Choose the admin secret yourself (step 6): a long phrase of at least 24 characters that you keep in your password manager.
4. Fill the guest list in the workbook, write the wording, pick the look, confirm the closing date.

## The local tools

Run from `projects/wedding-invite`, after `source scripts/env.sh`:

```bash
.venv/bin/python -I rsvp/tools/rsvp_workbook.py init
```

This creates `rsvp/guests/convite-rsvp.xlsx` (private; ignored by git). Open it, read the `README` sheet, and fill the `Guests` sheet: one row per household with a label only you see, the language, the members' names separated by `;`, the number of unnamed extra seats, and optionally a phone number.

```bash
.venv/bin/python -I rsvp/tools/rsvp_workbook.py links
```

This gives each household one private code, fills the `Links` sheet with a personal link to paste into WhatsApp, and writes `rsvp/output/seed.sql` (names and a hash of each code, no phone numbers). Run it again after any edit: existing codes never change. Adding people at the end of a household is fine; removing or reordering people after the links went out is refused, because it would mix up answers.

## Putting the form on the site

The finished face is unchanged until you switch the form on. `rsvp/rsvp-config.json` holds three settings: `enabled` (false for now), `api` (the Worker address from the setup below) and `whatsapp` (the link guests use to reach you). The form's styles, markup and script are in `rsvp/page/`.

With `enabled` false the site builds exactly as before. With it true, the build puts the form after the invitation, but only once the invitation is opened, and it refuses to continue while any `FAKE` placeholder wording is left. To rebuild:

```bash
source scripts/env.sh && .venv/bin/python -I comps/art/site_build.py --base-url https://tomasinacio.github.io/convite/
```

A local test of the whole flow (the real Worker code over a stand-in database, seeded with the `FAKE` guests) is `node rsvp/worker/tools/devserver.mjs rsvp/output/seed.sql`. The personal link is `https://tomasinacio.github.io/convite/?lang=en#CODE`; the page removes the code from the address bar as soon as it loads.

## The test deployment (FAKE guests)

A test copy runs on the free `Cloudflare` account: the backend `rsvp-test` (database `rsvp-test`, created in the EU, with the `FAKE` households) and the page `convite-test` (the invitation with the form on). Their settings are `worker/wrangler.test.toml` and `test-site/wrangler.toml`. The admin page has no secret set, so it shows nothing. Remove it all with `wrangler delete --config wrangler.test.toml`, `wrangler delete` in `test-site`, and `wrangler d1 delete rsvp-test`. The real backend is separate: database `rsvp` and `worker/wrangler.toml`.

## Setting up the receiver (once)

All commands run in `rsvp/worker`. The pinned `wrangler` version is fetched by `npx` on first use.

1. Check the setup: `npm test` (all tests must pass).
2. Log in: `npx wrangler@4.160.1 login`
3. Create the database in the EU: `npx wrangler@4.160.1 d1 create rsvp --jurisdiction eu`. It prints a `database_id`. Paste it into `wrangler.toml` in place of the `TODO(user)` text. The EU setting can only be chosen now, not later.
4. Create the tables: `npx wrangler@4.160.1 d1 migrations apply rsvp --remote`
5. Load the guests: `npx wrangler@4.160.1 d1 execute rsvp --remote --file ../output/seed.sql`. It is safe to run again after `links`.
6. Set the admin secret: `npx wrangler@4.160.1 secret put ADMIN_SECRET`, then type your phrase at the prompt. It is never written to a file.
7. Check `RSVP_CLOSES_AT` in `wrangler.toml` (UTC, with milliseconds). After that moment the form refuses changes. Proposed: `2027-05-31T23:59:59.000Z`.
8. Deploy: `npx wrangler@4.160.1 deploy`. It prints the address of the Worker.
9. Open `https://YOUR-WORKER-ADDRESS/admin` on your phone, type the secret, and bookmark the page.

The invitation page needs the Worker's address; the form stage of the build reads it from a config file and ships switched off until you say so.

## Reading the answers

- On a phone: the `/admin` page. Totals, who has not answered, diet notes, messages, and a CSV download.
- In Excel: `WRANGLER="npx wrangler@4.160.1" .venv/bin/python -I rsvp/tools/rsvp_workbook.py sync --wrangler-db rsvp` refreshes the `Answers`, `Pending`, `Messages` and `Summary` sheets from the live database. It uses your own `wrangler` login. The `Pending` sheet has a WhatsApp link per household that opens a chat with the reminder text from the `Settings` sheet (you write that text).
- A dated copy of the workbook is saved in `rsvp/guests/backups/` before each change.

## Costs and limits

The free `Cloudflare` plan gives 100,000 Worker requests a day and 5 million D1 row reads and 100,000 row writes a day; 150 households need a tiny fraction. If a daily limit were ever passed, requests fail until 00:00 UTC; nothing is charged.

## After the wedding

Run `sync` once more, keep the workbook, then delete the database: `npx wrangler@4.160.1 d1 delete rsvp`. The `D1` history (Time Travel) keeps deleted rows for 7 days. The deletion date is `TODO(user)`; proposed 2027-08-31.

## What is tested

- Worker: `cd rsvp/worker && npm test` (45 tests on Node's `node:sqlite` standing in for D1, with a stand-in that interleaves queries to prove two saves at once cannot both win).
- Tools: `.venv/bin/python -I -m unittest discover -s rsvp/tools -p "test_*.py"` (28 tests, including a check that the Worker accepts a code the tool made).
- The form in a browser: `rsvp/page/form-checks.cjs` (Playwright at iPhone 15 size against the local test Worker and a test build, 13 checks: drafts do not leak between households, a hung request ends in an error with the answers kept, wrong and pasted codes give feedback, odd server replies show the right screen, long answers fit, the face is unchanged). Also run by hand: the whole save, reload and edit round trip, two phones saving at once, closed, rate-limited, server error, JavaScript off, Spanish, `axe-core` (no violations in the form, error and saved states), and a clean-slate Opus review whose 13 findings were fixed.
- Not tested: a real `Cloudflare` deployment, real D1 timing and limits, the live `wrangler` commands above, iPhone Safari, WhatsApp's in-app browser, any phone narrower than 360 pixels apart from a 196-pixel stand-in for 200% zoom, and a screen reader on a real phone. The v16 page loads about 1448 KB before the tap (budget 1500 KB) and about 1810 KB after it, measured in the test browser; the form adds about 34 KB.
