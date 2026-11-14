import { test } from 'node:test';
import assert from 'node:assert/strict';
import { makeWorld, call, answerBody, CODE_A, NOW } from './helpers.js';
import { LIMITS } from '../src/lib.js';
import { addressUnit } from '../src/throttle.js';

test('too many wrong codes lock the guessing from that address, not the guests on it', async () => {
  const { env } = await makeWorld();
  const wrong = { code: 'ZZZZZZZZZZZZZZZZ', ip: '198.51.100.1' };
  for (let i = 0; i < LIMITS.fail_per_ip; i++) assert.equal((await call(env, '/api/lookup', wrong)).status, 404);
  const locked = await call(env, '/api/lookup', wrong);
  assert.equal(locked.status, 429);
  assert.ok(Number(locked.headers.get('retry-after')) > 0);
  // a real family behind the same shared address still gets in
  assert.equal((await call(env, '/api/lookup', { code: CODE_A, ip: '198.51.100.1' })).status, 200);
  assert.equal((await call(env, '/api/lookup', { ...wrong, ip: '198.51.100.2' })).status, 404);
});

test('the lock lifts after the window', async () => {
  const { env } = await makeWorld();
  const wrong = { code: 'ZZZZZZZZZZZZZZZZ' };
  for (let i = 0; i < LIMITS.fail_per_ip; i++) await call(env, '/api/lookup', wrong);
  assert.equal((await call(env, '/api/lookup', wrong)).status, 429);
  assert.equal((await call(env, '/api/lookup', { ...wrong, now: NOW + LIMITS.fail_window_ms + 1000 })).status, 404);
});

test('an IPv6 user cannot dodge the limit by changing the end of the address', async () => {
  assert.equal(addressUnit('2001:db8::1'), '2001:0db8:0000:0000/64');
  assert.equal(addressUnit('2001:DB8:0:0:ffff:1:2:3'), '2001:0db8:0000:0000/64');
  assert.equal(addressUnit('203.0.113.7'), '203.0.113.7');
  const { env } = await makeWorld();
  for (let i = 0; i < LIMITS.fail_per_ip; i++) await call(env, '/api/lookup', { code: 'ZZZZZZZZZZZZZZZZ', ip: `2001:db8::${i + 1}` });
  assert.equal((await call(env, '/api/lookup', { code: 'ZZZZZZZZZZZZZZZZ', ip: '2001:db8::ffff' })).status, 429);
  assert.equal((await call(env, '/api/lookup', { code: 'ZZZZZZZZZZZZZZZZ', ip: '2001:db9::1' })).status, 404);
});

test('good requests never count against the limit', async () => {
  const { env } = await makeWorld();
  for (let i = 0; i < 100; i++) assert.equal((await call(env, '/api/lookup', { code: CODE_A })).status, 200);
});

test('past the site-wide failure budget wrong codes are refused and nothing more is written', async () => {
  const { env, db } = await makeWorld();
  db.sqlite.prepare("INSERT INTO throttle (bucket, window_start, n) VALUES ('fail:all', ?, ?)").run(new Date(NOW).toISOString(), LIMITS.fail_global);
  const before = db.sqlite.prepare('SELECT COUNT(*) AS c FROM throttle').get().c;
  assert.equal((await call(env, '/api/lookup', { code: 'ZZZZZZZZZZZZZZZZ', ip: '192.0.2.77' })).status, 429);
  assert.equal(db.sqlite.prepare('SELECT COUNT(*) AS c FROM throttle').get().c, before);
  assert.equal((await call(env, '/api/lookup', { code: CODE_A, ip: '192.0.2.77' })).status, 200); // real guests unaffected
});

test('the daily change cap per family', async () => {
  const { env } = await makeWorld();
  for (let i = 0; i < LIMITS.changes_per_day; i++) {
    assert.equal((await call(env, '/api/answer', { code: CODE_A, body: answerBody({ revision: i, message: `m${i}` }) })).status, 200);
  }
  const r = await call(env, '/api/answer', { code: CODE_A, body: answerBody({ revision: LIMITS.changes_per_day, message: 'one too many' }) });
  assert.equal(r.status, 429);
  assert.equal((await r.json()).error, 'too_many_changes');
  // the next day it works again
  assert.equal((await call(env, '/api/answer', { code: CODE_A, body: answerBody({ revision: LIMITS.changes_per_day, message: 'next day' }), now: NOW + LIMITS.day_ms })).status, 200);
});

test('the history cap stops runaway rewriting', async () => {
  const { env, db } = await makeWorld();
  const ins = db.sqlite.prepare("INSERT INTO response_history (family_id, at, revision, payload) VALUES ('fam_a', ?, 1, '{}')");
  for (let i = 0; i < LIMITS.history_rows; i++) ins.run(new Date(NOW).toISOString());
  const r = await call(env, '/api/answer', { code: CODE_A, body: answerBody() });
  assert.equal(r.status, 429);
});

test('oversize bodies are refused', async () => {
  const { env } = await makeWorld();
  const big = answerBody({ message: 'x'.repeat(LIMITS.body_bytes + 10) });
  assert.equal((await call(env, '/api/answer', { code: CODE_A, body: big })).status, 413);
  const tooMany = { revision: 0, answers: Array.from({ length: 700 }, (_, i) => ({ slot: i, attending: true })) };
  assert.equal((await call(env, '/api/answer', { code: CODE_A, body: tooMany })).status, 413);
  // no Content-Length (a chunked upload): the cap still holds while reading
  const chunk = new TextEncoder().encode(JSON.stringify({ revision: 0, answers: [], message: 'y'.repeat(4000) }));
  const stream = new ReadableStream({ start(c) { c.enqueue(chunk); c.enqueue(chunk); c.enqueue(chunk); c.close(); } });
  assert.equal((await call(env, '/api/answer', { code: CODE_A, stream })).status, 413);
});

test('broken JSON and wrong shapes give clear 400s', async () => {
  const { env } = await makeWorld();
  assert.equal((await call(env, '/api/answer', { code: CODE_A, raw: '{not json' })).status, 400);
  for (const raw of ['null', '[]', '"x"', '42']) assert.equal((await call(env, '/api/answer', { code: CODE_A, raw })).status, 400);
});

test('field problems say which field and why', async () => {
  const { env } = await makeWorld();
  const send = async (b) => (await call(env, '/api/answer', { code: CODE_A, body: { revision: 0, ...b } })).json();
  const ok = [{ slot: 1, attending: true }, { slot: 2, attending: false }];
  assert.deepEqual((await send({ answers: [{ slot: 1, attending: true }] })).fields, [{ field: 'answers.slot.2', code: 'required' }]);
  assert.deepEqual((await send({ answers: [{ slot: 1, attending: 'yes' }, ok[1]] })).fields, [{ field: 'answers.0.attending', code: 'required' }]);
  assert.deepEqual((await send({ answers: [ok[0], ok[0], ok[1]] })).fields, [{ field: 'answers.1.slot', code: 'duplicate_slot' }]);
  assert.deepEqual((await send({ answers: [{ slot: 1, attending: true, diet: 'x'.repeat(201) }, ok[1]] })).fields, [{ field: 'answers.0.diet', code: 'too_long' }]);
  assert.deepEqual((await send({ answers: ok, message: 'x'.repeat(601) })).fields, [{ field: 'message', code: 'too_long' }]);
  assert.deepEqual((await send({ answers: ok, message: 5 })).fields, [{ field: 'message', code: 'bad_type' }]);
  assert.deepEqual((await send({})).fields, [{ field: 'answers', code: 'required' }]);
});

test('after the closing time answers are refused but still readable', async () => {
  const { env } = await makeWorld({ RSVP_CLOSES_AT: '2027-01-01T00:00:00.000Z' });
  const r = await call(env, '/api/answer', { code: CODE_A, body: answerBody() });
  assert.equal(r.status, 403);
  assert.equal((await r.json()).error, 'closed');
  const v = await (await call(env, '/api/lookup', { code: CODE_A })).json();
  assert.equal(v.open, false);
});

test('a missing or malformed closing time closes the form', async () => {
  for (const bad of [undefined, '', 'tomorrow', '2027-05-31', '2027-05-31T23:59:59Z', '2027-13-45T99:99:99.000Z']) {
    const { env } = await makeWorld({ RSVP_CLOSES_AT: bad });
    const r = await call(env, '/api/answer', { code: CODE_A, body: answerBody() });
    assert.equal(r.status, 403, String(bad));
    assert.equal((await (await call(env, '/api/lookup', { code: CODE_A })).json()).open, false);
  }
});

test('only the one allowed site may call the API', async () => {
  const { env } = await makeWorld();
  assert.equal((await call(env, '/api/lookup', { code: CODE_A, origin: 'https://evil.test' })).status, 403);
  assert.equal((await call(env, '/api/lookup', { code: CODE_A, origin: null })).status, 403);
  assert.equal((await call(env, '/api/lookup', { code: CODE_A, origin: 'https://site.test.evil.test' })).status, 403);
  const pre = await call(env, '/api/answer', { method: 'OPTIONS', ip: null });
  assert.equal(pre.status, 204);
  assert.equal(pre.headers.get('access-control-allow-origin'), 'https://site.test');
  assert.match(pre.headers.get('access-control-allow-headers'), /x-rsvp-code/);
  assert.notEqual(pre.headers.get('access-control-allow-origin'), '*');
  assert.equal((await call(env, '/api/lookup', { method: 'GET' })).status, 405);
  const bare = await makeWorld({ ALLOWED_ORIGIN: undefined });
  assert.equal((await call(bare.env, '/api/lookup', { code: CODE_A })).status, 503);
  const http = await makeWorld({ ALLOWED_ORIGIN: 'http://site.test' });
  assert.equal((await call(http.env, '/api/lookup', { code: CODE_A, origin: 'http://site.test' })).status, 503);
});

test('unknown paths are plain not found', async () => {
  const { env } = await makeWorld();
  for (const p of ['/', '/api', '/api/families', '/api/lookup/extra', '/.env']) assert.equal((await call(env, p)).status, 404);
});
