// Used by rsvp/tools/test_rsvp_workbook.py: loads a generated seed into the real migration and asks the
// real Worker code for the family behind a code. Prints "STATUS label" on one line.
import { readFileSync } from 'node:fs';
import { makeDb, CODE_A } from '../test/helpers.js';
import { handle } from '../src/core.js';

const [seedPath, code] = process.argv.slice(2);
const db = makeDb();
db.sqlite.exec(readFileSync(seedPath, 'utf8'));
const env = {
  DB: db, ALLOWED_ORIGIN: 'https://site.test', RSVP_CLOSES_AT: '2099-01-01T00:00:00.000Z',
};
const r = await handle(new Request('https://api.test/api/lookup', {
  method: 'POST', headers: { origin: 'https://site.test', 'x-rsvp-code': code || CODE_A, 'cf-connecting-ip': '203.0.113.9' },
  body: '{}',
}), env);
const v = await r.json();
console.log(r.status, v.family ? v.family.label : v.error, v.people ? v.people.length : 0);
