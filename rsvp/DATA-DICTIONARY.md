# RSVP data dictionary

Owner: Tomas. Written 2026-11-12. Review date: 2026-11-19. Rollback: `rm rsvp/DATA-DICTIONARY.md`.

Every table and column in `worker/migrations/0001-initial.sql`. Data class for all of it: private personal data (class P2): names, answers, and health-related dietary text. It stays on the user's `Cloudflare` account and the couple's own machine. Retention: **`TODO(user)`**: the user decides the deletion date (proposed 2027-08-31, after exporting to the workbook). Backup: `wrangler d1 export` before any risky change, and the workbook snapshots in `rsvp/guests/backups/`.

Timestamps are UTC [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) with milliseconds. Names are `snake_case`.

| Table | Column | Meaning |
| --- | --- | --- |
| `family` | `family_id` | stable id of a household, made by the tool (`g001`) |
| `family` | `code_hash` | `SHA-256` of the household's private code; the code itself is never stored here |
| `family` | `label` | the couple's own name for the household |
| `family` | `lang` | `pt-PT`, `en` or `es`: the language of the personal link |
| `person` | `family_id`, `slot` | the household and a stable position number |
| `person` | `name` | the person's name; empty for an extra seat |
| `person` | `is_extra` | 1 for an unnamed extra seat the guest may fill in |
| `answer` | `family_id`, `slot` | whose answer |
| `answer` | `attending` | 1 yes, 0 no |
| `answer` | `extra_name` | the name typed for an extra seat |
| `answer` | `diet` | optional food needs or allergies (health-related) |
| `response` | `family_id` | one row per household that answered |
| `response` | `message` | optional message to the couple |
| `response` | `created_at`, `updated_at` | first and latest save |
| `response` | `revision` | counts accepted changes; a save must name the revision it saw |
| `response` | `last_write` | random id of the request that wrote last; resolves two saves at once |
| `response_history` | `history_id`, `family_id`, `at`, `revision`, `payload` | an append-only copy of each accepted change, kept so a mistake can be undone |
| `throttle` | `bucket`, `window_start`, `n` | counters for the flood limits; holds a salted, daily-changing hash of a network address, never an address |
| `setting` | `name`, `value` | the random salt for that hash, made on first use |
