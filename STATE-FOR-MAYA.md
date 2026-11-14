# Wedding invitation: what exists today (for Maya's Claude)

Written 2026-11-14. Source: the project folder `projects/wedding-invite` on Tomás's machine. This file only describes what is built. It makes no judgement. Please compare it with your own build, point out where you do things better, and say what would clash on a merge. A reply template is at the end.

Private data (guest list, codes, phone numbers, bank details, account ids) is deliberately left out.

## 1. One paragraph

A static invitation page for Maya e Tomás, 10 July 2027, `Quinta do Grilo`, `Milharado`. The guest sees a closed folded sheet with a wax seal. One tap opens it in two vertical folds, then painted art draws in and the guest scrolls down through the details and an RSVP form. It is plain HTML, CSS and JS (no framework, no bundler). It is hosted on GitHub Pages. The RSVP receiver is a small `Cloudflare` Worker with a `D1` (SQLite) database. Languages: pt-PT (default), en, es.

## 2. Architecture

```text
Guest phone (WhatsApp link with personal code after #)
   |
   v
GitHub Pages (static site, public repo, noindex)
   index.html + app.<hash>.css/js + info.* + rsvp.* + img/*.webp + fonts/*.woff2
   |  fetch() POST, header X-Rsvp-Code
   v
Cloudflare Worker "rsvp"  --->  D1 database "rsvp" (EU jurisdiction)
   /api/lookup  /api/answer   (guests)
   /admin  /api/admin/*       (the couple, bearer secret)
```

Status: the live page is the finished face only (RSVP switched off). The Worker and form are tested locally and on a throwaway Cloudflare test deployment with fake guests. A real production Worker has not been deployed.

## 3. The face (animation)

- Closed state: one tall folded paper sheet, photographic wax seal as the tap target (a real `<button>` with a per-language name). A visible Skip button is first in focus order.
- Opening: vertical only. The top fold lifts, then the bottom fold drops, then the sheet grows downward into the scroll. No side opening. The seal cracks on tap.
- After opening: painted page, names panel in an `azulejo` frame (`Allura` script for names, EB Garamond for text), olive branch, dogs, meadow, a painted gate. Names write on, a sprig draws, leaves take colour and one drifts down. The whole reveal is about 7 s.
- Motion is hand-coded CSS and JS. Only `transform` and `opacity` are animated, except a few ink lines that use `stroke-dashoffset`. Rive, Lottie and `SVGator` were considered but not used.
- Reduced motion: the sheet opens and the art fades in with no drawing. JavaScript off: the painted page shows and the names appear as plain text.
- Accessibility rules in force: text pairs at least 4.5:1, real buttons, `lang` per language, focus moves to the invitation after the opening.
- Palette tokens: paper `#F6EFDF`, ink `#3B2F25`, olive `#4F5F2E`, terracotta `#9A4C32`, brown `#6B4F34`, plus decorative sage, twine, clay, lemon, `azulejo` blue. Pale tones never carry words.

## 4. Information sections between the face and the form

Built from `rsvp/page/info.html`, `info.css`, `info.js`:

- Where: address plaque, a map link, and an "add to calendar" button that builds a small `.ics` file in the browser (no outside service).
- Countdown to 10 July 2027, 15:00 Lisbon (days, hours, minutes, updated every 20 s).
- Schedule of the day, dress code, gifts, FAQ.
- A page foot ("rodapé") in painted `azulejo` style.
- All guest-facing wording here is still draft, marked `data-fake` in the markup and listed in `rsvp/comps/REPLACE-ME.md`. The build refuses to publish while any marker remains.

## 5. Build and hosting

- Source of the face: `comps/prototype.v15.src.html` (v16 and v17 add the information sections). Build: `.venv/bin/python -I comps/art/site_build.py --base-url https://tomasinacio.github.io/convite/` writes `site/`.
- Output: `index.html`, content-hashed CSS and JS, WebP images, local `woff2` fonts (Latin subset, SIL OFL), `_headers`, `robots.txt`, `404.html`, `og-image.jpg`. All URLs are relative. No external scripts, no Google Fonts.
- Publish: copy `site/` to a separate git repo (`tomasinacio/convite`, public, GitHub Pages from `main` root, `.nojekyll`), push, wait about a minute.
- Unlisted, not private: `noindex` meta, `robots.txt`. GitHub Pages ignores `_headers`, so no custom response headers and no CSP.
- Sizes (checked 2026-11-14): `site/` is 3.6 MB on disk (45 WebP files = 3.28 MB, fonts 96 KB, CSS 43 KB, JS 14 KB, HTML 11 KB). Largest image: the gate, 452 KB. First load before the tap measured at about 1448 KB (budget 1500 KB); about 1810 KB after the tap with the form (the form adds about 34 KB).
- The RSVP block is only built in when `rsvp/rsvp-config.json` has `enabled: true` and `api` set to the Worker origin. Otherwise the site is exactly the finished face.
- Art: painted watercolour-and-ink look, made with Microsoft Copilot image generation (by Tomás, by hand), cut out with a matting step, quality-gated (size, grain, blur, halo), each asset logged in `assets/LOG.md`.

## 6. Guest identification

- One personal link per household: `https://tomasinacio.github.io/convite/?lang=en#CODE`. Language comes from the query, the code from the URL fragment, so the code never reaches a server log, `Referer` header or link preview.
- Code: 16 characters, `Crockford` base32 (no I, L, O, U), 80 random bits, generated locally. Input is normalised (case, spaces, hyphens ignored; O reads as 0, I and L as 1).
- The page reads the fragment, keeps the code in `sessionStorage`, and removes it from the address bar with `history.replaceState`. If there is no code the form asks the guest to type it.
- Database stores only SHA-256 of each code. Wrong, malformed and missing codes get the same 404.

## 7. Worker API (the contract our form uses)

All calls are `POST` with header `X-Rsvp-Code: <code>` and JSON bodies. Responses carry `Cache-Control: no-store`. CORS allows only the one configured origin (`ALLOWED_ORIGIN`), never `*`; any other `Origin` gets 403.

`POST /api/lookup` (no body) returns the household's own record only:

```json
{
  "family": {"label": "...", "lang": "pt-PT"},
  "people": [{"slot": 1, "name": "...", "is_extra": false,
              "answer": {"attending": true, "name": "", "diet": ""} }],
  "message": "", "answered": true, "updated_at": "ISO", "revision": 3,
  "open": true, "closes_at": "ISO"
}
```

`answer` is `null` before the first save. Extra seats are unnamed people with `is_extra: true` (a plus-one or a child) that the guest names.

`POST /api/answer` body:

```json
{"revision": 3, "message": "optional", "website": "",
 "answers": [{"slot": 1, "attending": true, "diet": "", "name": ""}]}
```

- `revision` must equal the stored one (0 for the first save). A stale form gets `409 conflict` with the current record.
- `website` is a honeypot: if non-empty the Worker pretends to save and stores nothing.
- Success: `200 {"status":"saved"|"unchanged", ...same shape as lookup}`. An identical resubmission is `unchanged`, not an error.
- Errors: `404 not_found`, `429 too_many_attempts` (with `Retry-After`), `403 forbidden_origin` or `closed`, `413 too_big`, `400 invalid` with `fields:[{field,code}]`, `409 conflict`, `429 too_many_changes`, `500 server_error`, `503 not_configured`.
- Limits: body 8 KB, diet 200 chars, extra name 80, message 600, at most 6 extra seats per household (workbook rule). Each named person must answer yes or no; extra seats default to no.

Couple's side (bearer `ADMIN_SECRET`, at least 24 characters, compared by digest):

- `GET /admin` and `/admin/app.js`: a phone page (strict CSP) with totals, who has not answered, diet notes, messages, CSV download.
- `GET /api/admin/summary` (JSON) and `GET /api/admin/export.csv`.

## 8. Data model (D1, SQLite STRICT tables, `snake_case`, UTC timestamps with milliseconds)

| Table | Purpose |
| --- | --- |
| `family` | `family_id`, `code_hash` (64 hex, unique), `label` (couple's own name for it), `lang` (`pt-PT`, `en`, `es`) |
| `person` | `family_id`, `slot`, `name`, `is_extra`; seeded from the guest list |
| `answer` | `family_id`, `slot`, `attending` (0/1), `extra_name`, `diet` |
| `response` | one row per household that answered: `message`, `created_at`, `updated_at`, `revision`, `last_write` |
| `response_history` | append-only JSON copy of every accepted change |
| `throttle` | flood counters keyed by a salted, daily-rotating hash of the network address (IPv6 counted per /64) |
| `setting` | the random salt, made on first use |

Reseeding the guest list never touches `answer` or `response`. Migration: `rsvp/worker/migrations/0001-initial.sql` (plain `.sql` for `wrangler d1 migrations`). Data dictionary: `rsvp/DATA-DICTIONARY.md`.

## 9. Protections already in the Worker

- Wrong-code limit: 30 an hour per address, 600 an hour site-wide (after that no more counter writes, to protect the free write quota). A correct code always works, even from a busy address.
- Accepted changes: 20 a day per household, 200 history rows per household.
- Two saves at once cannot both win: the write applies only if its own random `last_write` id is the one stored; the loser gets `conflict` or `unchanged`.
- Body is read with a hard byte cap regardless of headers. Unknown fields are ignored. Types checked. Control characters stripped from text.
- Admin brute-force limits (8 failures per 10 minutes per address, 200 an hour site-wide). Worker logs are off.
- Closing time: setting `RSVP_CLOSES_AT` = `2027-04-30T22:59:59.000Z` (30 April 2027, 23:59:59 Lisbon). After it, saves are refused with `closed`. (Older notes in `rsvp/PLAN.md` and `rsvp/README.md` say 31 May; the config file is the truth.)

## 10. The form in the page (`rsvp/page/rsvp.html`, `rsvp.css`, `rsvp.js`)

- Sits after the information sections, painted in the same style. Shows the household name, one yes/no per named person, diet text per attending person, extra-seat names, one optional message with a counter.
- States: loading, form, sending, saved, error summary, network error (answers kept, retry), conflict (keep the saved one or send mine), closed, no link (type the code), no JavaScript (message plus WhatsApp contact buttons).
- Nothing counts as saved until the server confirms. Drafts go to `localStorage` per household (keyed by a short fingerprint of the code), expire, and are dropped on a revision change. 15 s request timeout with `AbortController`. Honeypot field. Language follows the page's `lang`.
- There is no privacy notice or consent line on the form yet, and no retention wording (the deletion date is still `TODO(user)`; proposed 2027-08-31).

## 11. The couple's tools

- `rsvp/tools/rsvp_workbook.py` (Python, `openpyxl`): `init` makes an Excel workbook (sheets README, Settings, Guests, Links, Answers, Pending, Messages, Summary). `links` gives each household a code, writes the personal links and a `seed.sql` with code hashes only. `sync` pulls live answers through the user's own `wrangler` login. Existing codes never change; removing or reordering people after links went out is refused. The workbook, codes and seed are git-ignored.
- Everything uses the user's own `Cloudflare` login. The assistant never sees credentials.

## 12. Tests (re-run 2026-11-14)

- Worker: `cd rsvp/worker && npm test`: 45 of 45 pass (Node `node:sqlite` stands in for D1, including a stand-in that interleaves queries to prove concurrent saves).
- Python tools: 28 of 28 pass, including a check that the Worker accepts a code the tool made.
- Browser: `rsvp/page/form-checks.cjs` (Playwright, iPhone 15 size, local Worker): 13 checks. Also run by hand: save, reload, edit; two phones at once; closed; rate-limited; server error; JavaScript off; Spanish; `axe-core` with no violations in the form states.
- Dependencies: Worker has no runtime dependencies (dev only: `wrangler` 4.160.1, Node 24 or newer). Python: `openpyxl` 3.1.5.

## 13. Not done or not tested

- iPhone Safari and WhatsApp's in-app browser (never tested; WebKit is not available on the build machine).
- A production `Cloudflare` deployment with real guests, real D1 timing and limits.
- Screen reader on a real phone; phones narrower than 360 pixels apart from a 196-pixel stand-in for 200% zoom.
- All guest-facing wording (pt-PT, en, es) is placeholder. Opening line, link-preview text and venue copy are still `TODO(user)`.
- Some painted assets (mushrooms, bee, peppers, plants) are still being made; slots are hidden until then.
- No privacy notice, no retention date, no email or WhatsApp confirmation to guests after saving.

## 14. File map

| Path | What |
| --- | --- |
| `comps/prototype.v15.src.html`, `v16`, `v17` | readable source of the face and later versions |
| `comps/art/site_build.py` | static site build |
| `site/` | generated output (do not edit) |
| `rsvp/worker/src/` | Worker: `core.js` (routes), `validate.js`, `throttle.js`, `lib.js`, `admin_*.js` |
| `rsvp/worker/migrations/` | D1 schema |
| `rsvp/worker/wrangler.toml` | Worker config (no secrets; `ADMIN_SECRET` is set with `wrangler secret put`) |
| `rsvp/page/` | form and information sections (HTML, CSS, JS) |
| `rsvp/rsvp-config.json` | on/off switch and Worker address for the build |
| `rsvp/PLAN.md`, `README.md`, `DATA-DICTIONARY.md` | decisions, run guide, tables |

## 15. What Tomás said about merging

On 2026-11-13: Maya has already set up most of the RSVP infrastructure, and the plan is to merge this front page and art with her backend. Our RSVP backend work is paused until the merge is decided.

What would need to match on a merge, from our side:

- The form talks to one origin through two calls (section 7). Swapping in another backend means either keeping this contract or editing the `call()` function and the response mapping in `rsvp/page/rsvp.js` (about 25 KB, the only file that knows the API).
- The form expects the household (names, extra seats, language) to come from the server for a personal code, not from the page.
- The invitation origin must be allowed by the backend's CORS, and the code reaches the backend as a header, never in a URL.

## 16. Reply template for Maya's Claude

Please fill this in, then send it back to Tomás:

1. Stack and hosting of your front end and back end.
2. How guests are identified (link shape, token, where the household and seat count come from).
3. Data model: tables or sheets, fields per person and per household.
4. API: endpoints, request and response shapes, error handling, how a stale or double save is handled.
5. Where answers are stored, who can read them, how the couple reads them.
6. Protection against wrong codes, spam and floods; privacy and retention choices.
7. Languages and wording already written.
8. What you tested, and on which devices and browsers.
9. Where our approach is weaker than yours, where yours is weaker than ours, and your recommended way to merge.
