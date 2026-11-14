import { test } from 'node:test';
import assert from 'node:assert/strict';
import { makeWorld, call, answerBody, CODE_A, CODE_B, NOW } from './helpers.js';

const j = async (r) => r.json();

test('lookup with a valid code returns only that family', async () => {
  const { env } = await makeWorld();
  const r = await call(env, '/api/lookup', { code: CODE_A });
  assert.equal(r.status, 200);
  assert.equal(r.headers.get('cache-control'), 'no-store');
  const v = await j(r);
  assert.equal(v.family.label, 'Test Family A');
  assert.deepEqual(v.people.map((p) => p.name), ['Alice Test', 'Bob Test', '']);
  assert.equal(v.answered, false);
  assert.equal(v.open, true);
});

test('a valid answer is stored, with its history row', async () => {
  const { env, db } = await makeWorld();
  const r = await call(env, '/api/answer', { code: CODE_A, body: answerBody() });
  assert.equal(r.status, 200);
  const v = await j(r);
  assert.equal(v.status, 'saved');
  assert.equal(v.revision, 1);
  assert.equal(v.people[0].answer.attending, true);
  assert.equal(v.people[0].answer.diet, 'no nuts');
  assert.equal(v.people[2].answer.attending, false); // unused extra seat
  assert.equal(db.sqlite.prepare('SELECT COUNT(*) AS c FROM answer').get().c, 3);
  assert.equal(db.sqlite.prepare('SELECT COUNT(*) AS c FROM response_history').get().c, 1);
  assert.match(db.sqlite.prepare('SELECT created_at FROM response').get().created_at, /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/);
});

test('a changed answer updates in place and keeps the history', async () => {
  const { env, db } = await makeWorld();
  await call(env, '/api/answer', { code: CODE_A, body: answerBody() });
  const second = answerBody({ revision: 1, answers: [{ slot: 1, attending: false }, { slot: 2, attending: true, diet: 'vegan' }], message: 'changed' });
  const v = await j(await call(env, '/api/answer', { code: CODE_A, body: second, now: NOW + 60000 }));
  assert.equal(v.status, 'saved');
  assert.equal(v.revision, 2);
  assert.equal(v.message, 'changed');
  assert.equal(db.sqlite.prepare('SELECT COUNT(*) AS c FROM response').get().c, 1);
  const hist = db.sqlite.prepare('SELECT revision FROM response_history ORDER BY history_id').all().map((x) => x.revision);
  assert.deepEqual(hist, [1, 2]);
});

test('an identical resubmission changes nothing', async () => {
  const { env, db } = await makeWorld();
  await call(env, '/api/answer', { code: CODE_A, body: answerBody() });
  const v = await j(await call(env, '/api/answer', { code: CODE_A, body: answerBody(), now: NOW + 5000 }));
  assert.equal(v.status, 'unchanged');
  assert.equal(v.revision, 1);
  assert.equal(db.sqlite.prepare('SELECT COUNT(*) AS c FROM response_history').get().c, 1);
});

test('wrong, malformed and missing codes get the same refusal', async () => {
  const { env } = await makeWorld();
  const bodies = [];
  for (const code of ['ZZZZZZZZZZZZZZZZ', 'short', '', undefined, 'ABCDEFGHJKMNPQR!']) {
    const r = await call(env, '/api/lookup', { code });
    assert.equal(r.status, 404);
    bodies.push(await r.text());
  }
  assert.equal(new Set(bodies).size, 1);
  assert.equal(bodies[0], JSON.stringify({ error: 'not_found' }));
});

test('a code typed in lower case with hyphens and look-alikes still works', async () => {
  const { env } = await makeWorld();
  const typed = 'abcd-efgh jkmn-pqrs';
  assert.equal((await call(env, '/api/lookup', { code: typed })).status, 200);
  const lookalike = '0123-4567-89TV-WXYZ'.replace('0', 'O').replace('1', 'l');
  assert.equal((await call(env, '/api/lookup', { code: lookalike })).status, 200);
});

test('one family can never see or change another', async () => {
  const { env, db } = await makeWorld();
  await call(env, '/api/answer', { code: CODE_B, body: { revision: 0, answers: [{ slot: 1, attending: true, diet: 'secret allergy' }], message: 'private B' } });
  const a = await call(env, '/api/lookup', { code: CODE_A });
  const text = await a.text();
  for (const leak of ['Carla', 'Family B', 'secret allergy', 'private B', 'fam_b']) assert.ok(!text.includes(leak), `leaked ${leak}`);
  // A cannot address B's slot: B only has slot 1, A has 1 to 3, and unknown slots are refused
  const bad = await call(env, '/api/answer', { code: CODE_A, body: { revision: 0, answers: [{ slot: 1, attending: true }, { slot: 2, attending: true }, { slot: 9, attending: true }] } });
  assert.equal(bad.status, 400);
  await call(env, '/api/answer', { code: CODE_A, body: answerBody() });
  const b = db.sqlite.prepare("SELECT diet FROM answer WHERE family_id = 'fam_b'").get();
  assert.equal(b.diet, 'secret allergy');
});

test('the database keeps only code hashes', async () => {
  const { env, db } = await makeWorld();
  await call(env, '/api/answer', { code: CODE_A, body: answerBody() });
  for (const t of ['family', 'person', 'answer', 'response', 'response_history', 'throttle', 'setting']) {
    const dump = JSON.stringify(db.sqlite.prepare(`SELECT * FROM ${t}`).all());
    assert.ok(!dump.includes(CODE_A) && !dump.includes(CODE_B), `${t} holds a plain code`);
  }
  assert.match(db.sqlite.prepare('SELECT code_hash FROM family LIMIT 1').get().code_hash, /^[0-9a-f]{64}$/);
});

test('the hidden field catches bots: reported saved, nothing stored', async () => {
  const { env, db } = await makeWorld();
  const r = await call(env, '/api/answer', { code: CODE_A, body: { ...answerBody(), website: 'http://spam.test' } });
  assert.equal(r.status, 200);
  assert.equal(db.sqlite.prepare('SELECT COUNT(*) AS c FROM answer').get().c, 0);
});

test('an extra seat needs a name when it is used', async () => {
  const { env } = await makeWorld();
  const noName = await call(env, '/api/answer', { code: CODE_A, body: { revision: 0, answers: [{ slot: 1, attending: true }, { slot: 2, attending: true }, { slot: 3, attending: true }] } });
  assert.equal(noName.status, 400);
  const f = (await j(noName)).fields;
  assert.deepEqual(f, [{ field: 'answers.2.name', code: 'name_required' }]);
  const ok = await call(env, '/api/answer', { code: CODE_A, body: { revision: 0, answers: [{ slot: 1, attending: true }, { slot: 2, attending: true }, { slot: 3, attending: true, name: '  Guest Plus  ' }] } });
  const v = await j(ok);
  assert.equal(v.people[2].answer.name, 'Guest Plus');
});

test('invisible and direction-changing characters are stripped', async () => {
  const { env } = await makeWorld();
  const v = await j(await call(env, '/api/answer', { code: CODE_A, body: { revision: 0, answers: [{ slot: 1, attending: true, diet: 'no‮ nuts​' }, { slot: 2, attending: false }], message: 'a\u0000b' } }));
  assert.equal(v.people[0].answer.diet, 'no nuts');
  assert.equal(v.message, 'a b');
});

test('the batch is atomic: a statement that fails part-way undoes the earlier ones', async () => {
  const { env, db } = await makeWorld();
  const real = db.batch;
  // a real rule violation (no such person), not a fake throw: the earlier writes must roll back
  db.batch = async (stmts) => real(stmts.length > 3
    ? [...stmts, db.prepare("INSERT INTO answer (family_id, slot, attending) VALUES ('fam_a', 99, 1)")]
    : stmts);
  const r = await call(env, '/api/answer', { code: CODE_A, body: answerBody() });
  assert.equal(r.status, 500);
  assert.equal(await r.text(), JSON.stringify({ error: 'server_error' }));
  for (const t of ['answer', 'response', 'response_history']) assert.equal(db.sqlite.prepare(`SELECT COUNT(*) AS c FROM ${t}`).get().c, 0);
});

test('three identical taps at the same moment store one answer', async () => {
  const { env, db } = await makeWorld({}, { yieldBetween: true });
  const rs = await Promise.all([1, 2, 3].map(() => call(env, '/api/answer', { code: CODE_A, body: answerBody() })));
  const out = await Promise.all(rs.map((r) => r.json()));
  assert.deepEqual(rs.map((r) => r.status), [200, 200, 200]);
  assert.equal(out.filter((o) => o.status === 'saved').length, 1);
  assert.equal(out.filter((o) => o.status === 'unchanged').length, 2);
  assert.equal(db.sqlite.prepare('SELECT revision FROM response').get().revision, 1);
  assert.equal(db.sqlite.prepare('SELECT COUNT(*) AS c FROM response_history').get().c, 1);
});

test('two different answers at the same moment: one wins, the other is told', async () => {
  const { env, db } = await makeWorld({}, { yieldBetween: true });
  const x = answerBody({ message: 'from X' });
  const y = answerBody({ message: 'from Y', answers: [{ slot: 1, attending: false }, { slot: 2, attending: true }] });
  const rs = await Promise.all([call(env, '/api/answer', { code: CODE_A, body: x }), call(env, '/api/answer', { code: CODE_A, body: y })]);
  assert.deepEqual(rs.map((r) => r.status).sort(), [200, 409]);
  const loser = await (rs[0].status === 409 ? rs[0] : rs[1]).json();
  assert.equal(loser.error, 'conflict');
  assert.ok(['from X', 'from Y'].includes(loser.message)); // the current saved answer comes back
  assert.equal(db.sqlite.prepare('SELECT revision FROM response').get().revision, 1);
  assert.equal(db.sqlite.prepare('SELECT COUNT(*) AS c FROM response_history').get().c, 1);
  // the stored answers are one request's whole answer, never a mix
  const msg = db.sqlite.prepare('SELECT message FROM response').get().message;
  const a1 = db.sqlite.prepare('SELECT attending FROM answer WHERE slot = 1').get().attending;
  assert.equal(a1, msg === 'from X' ? 1 : 0);
});

test('a stale form cannot overwrite a newer answer', async () => {
  const { env } = await makeWorld();
  await call(env, '/api/answer', { code: CODE_A, body: answerBody() });
  await call(env, '/api/answer', { code: CODE_A, body: answerBody({ revision: 1, message: 'newer' }) });
  const stale = await call(env, '/api/answer', { code: CODE_A, body: answerBody({ revision: 1, message: 'stale' }) });
  assert.equal(stale.status, 409);
  const v = await stale.json();
  assert.equal(v.message, 'newer');
  assert.equal(v.revision, 2);
});

test('the revision is required', async () => {
  const { env } = await makeWorld();
  const { revision, ...rest } = answerBody();
  const r = await call(env, '/api/answer', { code: CODE_A, body: rest });
  assert.equal(r.status, 400);
  assert.deepEqual((await r.json()).fields, [{ field: 'revision', code: 'required' }]);
});
