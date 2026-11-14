import { test } from 'node:test';
import assert from 'node:assert/strict';
import { makeWorld, call, answerBody, CODE_A, CODE_B, ADMIN } from './helpers.js';

const get = (env, path, secret, extra = {}) => call(env, path, { method: 'GET', origin: null, headers: secret === undefined ? {} : { authorization: `Bearer ${secret}` }, ...extra });

test('the admin data needs the secret', async () => {
  const { env } = await makeWorld();
  assert.equal((await get(env, '/api/admin/summary')).status, 401);
  assert.equal((await get(env, '/api/admin/summary', 'wrong')).status, 401);
  assert.equal((await get(env, '/api/admin/summary', ADMIN)).status, 200);
  assert.equal((await get(env, '/api/admin/export.csv', ADMIN)).status, 200);
  assert.equal((await get(env, '/api/admin/export.csv')).status, 401);
});

test('admin is off when the secret is missing or short', async () => {
  for (const s of [undefined, '', 'short']) {
    const { env } = await makeWorld({ ADMIN_SECRET: s });
    assert.equal((await get(env, '/api/admin/summary', s ?? 'x')).status, 404);
  }
});

test('guessing the admin secret locks the address', async () => {
  const { env } = await makeWorld();
  for (let i = 0; i < 8; i++) assert.equal((await get(env, '/api/admin/summary', `guess${i}`)).status, 401);
  assert.equal((await get(env, '/api/admin/summary', ADMIN)).status, 429);
});

test('the guest endpoints never accept the admin secret and vice versa', async () => {
  const { env } = await makeWorld();
  assert.equal((await call(env, '/api/lookup', { code: ADMIN })).status, 404);
  assert.equal((await get(env, '/api/admin/summary', CODE_A)).status, 401);
});

test('the summary counts people, waiting and extras', async () => {
  const { env } = await makeWorld();
  const before = await (await get(env, '/api/admin/summary', ADMIN)).json();
  assert.deepEqual(before.totals, { families: 2, families_answered: 0, coming: 0, not_coming: 0, waiting: 3 });
  await call(env, '/api/answer', { code: CODE_A, body: { revision: 0, answers: [{ slot: 1, attending: true, diet: 'no nuts' }, { slot: 2, attending: false }, { slot: 3, attending: true, name: 'Guest Plus' }], message: 'see you' } });
  const s = await (await get(env, '/api/admin/summary', ADMIN)).json();
  assert.deepEqual(s.totals, { families: 2, families_answered: 1, coming: 2, not_coming: 1, waiting: 1 });
  const a = s.families.find((f) => f.label === 'Test Family A');
  assert.deepEqual(a.people.map((p) => [p.name, p.attending]), [['Alice Test', true], ['Bob Test', false], ['Guest Plus', true]]);
  assert.equal(a.message, 'see you');
});

test('an unused extra seat is not listed', async () => {
  const { env } = await makeWorld();
  await call(env, '/api/answer', { code: CODE_A, body: answerBody() });
  const s = await (await get(env, '/api/admin/summary', ADMIN)).json();
  assert.equal(s.families.find((f) => f.label === 'Test Family A').people.length, 2);
});

test('the CSV opens cleanly and cannot run formulas', async () => {
  const { env } = await makeWorld();
  await call(env, '/api/answer', { code: CODE_B, body: { revision: 0, answers: [{ slot: 1, attending: true, diet: '=HYPERLINK("http://x.test","a")' }], message: '+cmd|calc, "quoted"' } });
  const r = await get(env, '/api/admin/export.csv', ADMIN);
  assert.match(r.headers.get('content-type'), /text\/csv/);
  const bytes = new Uint8Array(await r.clone().arrayBuffer());
  assert.deepEqual([...bytes.slice(0, 3)], [0xef, 0xbb, 0xbf]); // UTF-8 byte-order mark, so Excel reads accents
  const text = await r.text();
  assert.ok(text.startsWith('"family"'));
  assert.ok(text.includes(`"'=HYPERLINK(""http://x.test"",""a"")"`));
  assert.ok(text.includes(`"'+cmd|calc, ""quoted"""`));
});

test('the admin page is private and locked down', async () => {
  const { env } = await makeWorld();
  const page = await get(env, '/admin');
  assert.equal(page.status, 200);
  assert.match(page.headers.get('content-security-policy'), /script-src 'self'/);
  assert.match(page.headers.get('x-robots-tag'), /noindex/);
  assert.equal(page.headers.get('cache-control'), 'no-store');
  const html = await page.text();
  assert.ok(!html.includes(ADMIN));
  assert.equal((await get(env, '/admin/app.js')).status, 200);
  assert.equal((await call(env, '/admin', { method: 'POST' })).status, 405);
});
