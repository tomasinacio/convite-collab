import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateSubmission } from '../src/validate.js';
import { LIMITS, normaliseCode, CODE_RE, clean, closesAtMs } from '../src/lib.js';

const people = [{ slot: 1, name: 'A', is_extra: 0 }, { slot: 2, name: 'B', is_extra: 0 }, { slot: 3, name: '', is_extra: 1 }];

// a tiny seeded generator, so a failure can be replayed
function rng(seed) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 2 ** 32);
}
function junk(r, depth = 0) {
  const k = Math.floor(r() * 9);
  if (depth > 3 || k < 3) return [undefined, null, true, false, 0, -1, 1e999, NaN, 'x', '', '‮', 'a'.repeat(Math.floor(r() * 900))][Math.floor(r() * 12)];
  if (k < 6) return Array.from({ length: Math.floor(r() * 5) }, () => junk(r, depth + 1));
  const o = {};
  for (const key of ['answers', 'slot', 'attending', 'diet', 'name', 'message', '__proto__', 'constructor']) if (r() < 0.5) o[key] = junk(r, depth + 1);
  return o;
}

test('random input never throws and always returns a verdict', () => {
  const r = rng(12345);
  for (let i = 0; i < 3000; i++) {
    const v = validateSubmission(junk(r), people);
    assert.equal(typeof v.ok, 'boolean');
    if (!v.ok) assert.ok(Array.isArray(v.fields) && v.fields.length > 0);
  }
});

test('random answer lists that pass always respect the limits', () => {
  const r = rng(99);
  let passed = 0;
  for (let i = 0; i < 3000; i++) {
    const body = {
      revision: 0,
      answers: people.map((p) => ({ slot: p.slot, attending: r() < 0.6, diet: r() < 0.5 ? 'd'.repeat(Math.floor(r() * 260)) : undefined, name: r() < 0.7 ? 'n'.repeat(Math.floor(r() * 120)) : undefined })),
      message: r() < 0.5 ? 'm'.repeat(Math.floor(r() * 700)) : undefined,
    };
    const v = validateSubmission(body, people);
    if (!v.ok) continue;
    passed += 1;
    assert.ok(v.message.length <= LIMITS.message);
    for (const a of v.answers) {
      assert.ok(a.diet.length <= LIMITS.diet && a.name.length <= LIMITS.extra_name);
      if (!a.attending) assert.ok(a.diet === '' && a.name === '');
      if (a.slot === 3 && a.attending) assert.ok(a.name !== '');
    }
  }
  assert.ok(passed > 50);
});

test('validation does not change its input and is repeatable', () => {
  const body = { revision: 0, answers: [{ slot: 1, attending: true, diet: ' x ' }, { slot: 2, attending: false }], message: ' hi ' };
  const copy = structuredClone(body);
  const a = validateSubmission(body, people);
  assert.deepEqual(body, copy);
  assert.deepEqual(validateSubmission(body, people), a);
});

test('a leading prototype key in the body is harmless', () => {
  const v = validateSubmission(JSON.parse('{"__proto__":{"polluted":true},"revision":0,"answers":[{"slot":1,"attending":true},{"slot":2,"attending":false}]}'), people);
  assert.equal(v.ok, true);
  assert.equal({}.polluted, undefined);
});

test('code reading rules', () => {
  assert.equal(normaliseCode(' abcd-efgh-jkmn-pqrs '), 'ABCDEFGHJKMNPQRS');
  assert.equal(normaliseCode('o1lI'), '0111');
  assert.ok(CODE_RE.test('ABCDEFGHJKMNPQRS'));
  for (const bad of ['ABCDEFGHJKMNPQR', 'ABCDEFGHJKMNPQRSS', 'ABCDEFGHJKMNPQRU', 'ABCDEFGHJKMNPQR!']) assert.ok(!CODE_RE.test(bad));
});

test('text cleaning', () => {
  assert.equal(clean('  a​b‮c  '), 'abc');
  assert.equal(clean('line1\r\nline2\u0000', { multiline: true }), 'line1\nline2');
  assert.equal(clean('é'), 'é');
});

test('the closing time must be exact UTC with milliseconds', () => {
  assert.equal(closesAtMs({ RSVP_CLOSES_AT: '2027-05-31T23:59:59.000Z' }), Date.UTC(2027, 4, 31, 23, 59, 59));
  assert.equal(closesAtMs({ RSVP_CLOSES_AT: '2027-05-31T23:59:59+01:00' }), null);
  assert.equal(closesAtMs({}), null);
});
