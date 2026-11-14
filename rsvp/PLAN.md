# RSVP plan and decision log

Owner: Tomas. Written 2026-11-12. Review date: 2026-11-19. Rollback: `rm -rf projects/wedding-invite/rsvp` and rebuild the site without the RSVP block.

Scope: the RSVP only. The finished face, its opening animation and its timing stay untouched. Copy is the user's: every guest-facing sentence is `TODO(user)` in pt-PT, en and es.

## Recommendation in one paragraph

Keep the invitation on GitHub Pages where it already lives. Add one small `Cloudflare` Worker with a `D1` database (SQLite) that stores the answers. Each family gets a personal link with a private code in the part of the address after the `#`, so the code never reaches any server log. The couple read the answers on a private phone page served by the same Worker, with counts, a list of who has not answered, allergies, messages and a CSV export that opens in any spreadsheet app. Everything fits in the free plan with a very large margin: 150 guests make a few hundred requests in total, against 100 000 a day allowed.

## Backend options compared

| Option | Free | Safe for 150 guests | Easy to read on a phone | Easy to test here | Verdict |
| --- | --- | --- | --- | --- | --- |
| `Cloudflare` Worker plus `D1` | yes | yes: server-side code check, rate limits, hashed codes | good with the admin page below | yes: the logic is plain JavaScript over SQLite, run on `node:sqlite` | **chosen** |
| `Cloudflare` Pages Functions plus `D1` | yes | yes | same | same | needs the site moved off GitHub Pages and a new address; no extra benefit |
| Google Sheet with Apps Script | yes | weaker: the script runs as the owner, the quota and the redirect behaviour are odd, slow on a bad connection | best: the sheet app is already on both phones | no: Apps Script cannot run here, so the tests would prove nothing | rejected for testability |
| `Supabase` | yes | yes | table editor is awkward on a phone | partly | rejected: more moving parts, projects pause when idle |

Why the Worker over the sheet: the user asked for tests that prove a wrong code is refused, floods are handled and nothing leaks. That can only be proven against code that runs locally. The phone-reading gap is closed by the admin page and the CSV export.

## Decisions

### Identification

- One family (or single guest) per personal link. The code is 16 characters of `Crockford` base32 (80 random bits), generated locally by `tools/rsvp_workbook.py`, never invented by hand.
- Link shape: `https://tomasinacio.github.io/convite/?lang=en#CODE`. The language is the query part the face already reads; the code is after the `#`, so it is never sent to any server, never in `Referer`, never in the link preview.
- The database stores only the SHA-256 of each code. A stolen copy of the database cannot rebuild a link.
- A wrong, malformed or missing code gets the same refusal, so nobody can learn which codes exist. A correct code always works, even from an address that has made many wrong guesses (a shared mobile address must not lock real guests out).
- Guests are named people in the guest list. Each person answers yes or no on their own. A family may also have extra seats (a plus-one, a child not yet named): the guest types that name.

### Fields

Per person: attending (yes or no, required), dietary needs and allergies (free text, up to 200 characters, optional), name (extra seats only, required if attending). Per family: one optional message to the couple (up to 600 characters). Nothing else is collected: no phone, no email, no address.

### Answers can change

A new submission replaces the old one for that family until the closing time. Every accepted change is appended to a history table (so a mistake by one family member can be undone from the database), and an identical resubmission changes nothing.

### Deadline

The Worker has one setting, `RSVP_CLOSES_AT`. Proposed value: `2027-05-31T23:59:59.000Z`, about six weeks before the day; change it in `wrangler.toml` and redeploy. After it, the form shows the closed message (`TODO(user)`) and the server refuses changes. The wording of the deadline is the user's.

### Spam, floods and size

- Body limit 8 KB; field limits as above; unknown fields ignored; types checked.
- Wrong codes: 30 an hour per network address (an IPv6 address counts as its /64 block; stored as a salted hash that changes daily), then wrong guesses get 429 with a retry time. A site-wide budget of 600 wrong codes an hour stops all further counter writes, so a flood cannot use up the free database write quota.
- Accepted changes: at most 20 a day per family and 200 history rows in total per family.
- Two saves at once cannot both win: the form sends the revision it loaded, and a save only applies if that is still current. A double tap is a harmless "unchanged"; a stale form gets a clear conflict with the current answer.
- Requests are accepted only from the one allowed site origin (CORS pinned, never `*`).

### Privacy

- A valid code returns only that family's own record. There is no list endpoint for guests.
- Answers carry `Cache-Control: no-store`; the Worker never logs bodies, codes or names.
- The admin page and its data need a separate admin secret, compared in constant time. The secret is set by the user on the `Cloudflare` side; nobody else sees it.
- Guest names and answers live in the user's own `Cloudflare` account. After the wedding, export the CSV and delete the database. Suggested date: 2027-08-31.
- The guest list and the generated codes live in `rsvp/guests/` and are ignored by git.

### Reading the answers

`https://<worker address>/admin`, bookmarked on both phones. It asks for the admin secret once per tab (kept in the tab only), then shows: totals (coming, not coming, no answer yet), a filterable list per family, a "dietary needs" list, the messages, and a button that downloads a CSV (opens in Google Sheets or Excel).

### Data layout

SQL names are `snake_case`; timestamps are UTC with milliseconds (`2027-01-05T10:30:00.000Z`).

| Table | Holds |
| --- | --- |
| `family` | `family_id`, `code_hash`, `label`, `lang` (from the guest list) |
| `person` | `family_id`, `slot`, `name`, `is_extra`; extra seats are unnamed rows with `is_extra` set (from the guest list) |
| `answer` | `family_id`, `slot`, `attending`, `extra_name`, `diet` |
| `response` | `family_id`, `message`, `created_at`, `updated_at`, `revision`, `last_write` (which request won a race) |
| `response_history` | append-only copy of each accepted change |
| `throttle` | counters for the flood limits |
| `setting` | a random salt for the address hash, made on first use |

Reseeding the guest list never touches `answer` or `response`, so edits to the list cannot erase answers.

### Hosting

The Worker answers on a `workers.dev` address. Setup needs a free `Cloudflare` account and one browser login by the user (see "What only you can do"). Nothing is deployed until the user confirms.

## Interface to the form

| Call | Purpose |
| --- | --- |
| `POST /api/lookup` with header `X-Rsvp-Code` | returns the family label, language, people, extra seats, the saved answers, whether the form is open |
| `POST /api/answer` with header `X-Rsvp-Code` and a JSON body | stores or replaces the answers, returns the saved record |
| `GET /api/admin/summary`, `GET /api/admin/export.csv`, `GET /admin` | the couple's view; bearer admin secret |

Codes travel in a header, never in a URL, and every call is `POST` or admin `GET` so nothing is cached.

## Client behaviour (the user-visible part is the designer's)

- The form sits at the end of the scroll, after the gate and the details.
- No JavaScript: a visible `TODO(user)` message says the page needs JavaScript and where to answer instead (WhatsApp).
- Slow or failing network: the typed answers stay in the form and in a local draft, a clear message says nothing was lost and offers a retry; the server confirmation is what counts as saved.
- Errors say what to fix, in the guest's language. Reduced motion is respected.
- No code in the address: the block says to use the personal link (`TODO(user)` wording).

## What only you can do

1. Create (or log into) a free `Cloudflare` account at the `Cloudflare` sign-up page. Never share the password with the assistant.
2. In a terminal in `rsvp/worker`, run the login command that the deploy guide prints; a browser window opens and you approve it.
3. Choose and set the admin secret yourself (the guide prints the one command; you type the secret in the terminal prompt).
4. Fill `rsvp/guests/guests.csv`, wording for the form, the deadline sentence, and pick the form's look.

## Decision log

| Date | Decision | Why |
| --- | --- | --- |
| 2026-11-12 | `Cloudflare` Worker plus `D1`, site stays on GitHub Pages | testable here, free, no site move |
| 2026-11-12 | Code after `#`, hashed in the database | never in logs or previews |
| 2026-11-12 | Per-person yes or no, diet text, one family message | the user's default fields |
| 2026-11-12 | Closing time is a setting, proposed 2027-05-31 | the user delegated the deadline; the wording is theirs |
| 2026-11-12 | Admin page plus CSV, no Google Sheet | readable on phones, no second account |
| 2026-11-12 | Hybrid hosting: the free `Cloudflare` receiver plus the couple's own copy | the user asked for local and free, and the PC is not always on |
| 2026-11-12 | One Excel workbook holds the guest list, links, answers, pending, messages and summary | the user's request; the tool writes real hyperlink cells, not formulas, so no recalculation is needed |
| 2026-11-12 | Skills, tools and subagents researched by free agents, checked at source, added to the project folder | the user's request; see `rsvp/kit/INDEX.md` |
| 2026-11-12 | Codes are 16 characters, plain `SHA-256` | the security review: 60 bits is thin if the database leaks; 80 bits is not |
| 2026-11-12 | A correct code works from any address; only wrong guesses are limited | shared mobile addresses must not lock real guests out; a bot gains nothing |
| 2026-11-12 | Saves carry the revision the form loaded; two saves at once cannot both win | the code review: the first design let a double tap or a stale form overwrite |
| 2026-11-12 | **Deviation from the approved plan:** no native form post for guests without JavaScript | the household's names come from the server, so a static page cannot draw the right form without JavaScript; guests without it see a clear message and the contact route instead (wording is the user's, `TODO(user)`) |
| 2026-11-12 | **Deviation from the repo data rulebook:** numbered `.sql` migrations for `wrangler d1`, not the Python `sqlite-utils` migrations | D1 applies `.sql` files with its own tool; the data dictionary lives in `rsvp/DATA-DICTIONARY.md` and not in `ops/` to keep this work inside its folder |
| 2026-11-12 | Worker logs are off | the privacy research; turn them on briefly only when debugging |
| 2026-11-12 | The RSVP look is the Dolce Vita-style concept A, drawn by the Opus 5.5 designer agent on the five reference invitations; the user approved it with the option picker | the project rule that design is Opus and the user picks |
| 2026-11-12 | The form is built into the site only when `rsvp/rsvp-config.json` has `enabled` true, and not while any `FAKE` placeholder is left | the user allowed fake test data on condition that it is all marked and replaced |
