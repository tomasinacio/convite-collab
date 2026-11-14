// Test harness: a D1-shaped wrapper over node:sqlite, the real migrations, and request helpers.
import { DatabaseSync } from 'node:sqlite';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { handle } from '../src/core.js';
import { sha256hex, normaliseCode } from '../src/lib.js';

const MIGRATIONS = fileURLToPath(new URL('../migrations/', import.meta.url));

// yieldBetween makes every query wait a turn, so parallel requests really interleave like on D1.
export function makeDb({ yieldBetween = false } = {}) {
  const sqlite = new DatabaseSync(':memory:');
  sqlite.exec('PRAGMA foreign_keys = ON');
  for (const f of readdirSync(MIGRATIONS).sort()) sqlite.exec(readFileSync(MIGRATIONS + f, 'utf8'));
  const tick = async () => { if (yieldBetween) await new Promise((r) => setImmediate(r)); };
  const wrap = (sql, params = []) => ({
    bind: (...p) => wrap(sql, p),
    first: async () => { await tick(); return sqlite.prepare(sql).get(...params) ?? null; },
    all: async () => { await tick(); return { results: sqlite.prepare(sql).all(...params) }; },
    run: async () => { await tick(); return { meta: { changes: sqlite.prepare(sql).run(...params).changes } }; },
    allSync: () => sqlite.prepare(sql).all(...params),
  });
  return {
    sqlite,
    prepare: (sql) => wrap(sql),
    // like D1: all statements in one transaction, one result per statement
    batch: async (stmts) => {
      await tick();
      sqlite.exec('BEGIN');
      try {
        const out = stmts.map((s) => ({ results: s.allSync() }));
        sqlite.exec('COMMIT');
        return out;
      } catch (e) {
        sqlite.exec('ROLLBACK');
        throw e;
      }
    },
  };
}

export const NOW = Date.UTC(2027, 0, 15, 12, 0, 0);
export const ORIGIN = 'https://site.test';
export const ADMIN = 'admin-secret-that-is-long-enough-1234';
export const CODE_A = 'ABCDEFGHJKMNPQRS';
export const CODE_B = '0123456789TVWXYZ';

export async function seedFamily(db, { id, code, label, lang = 'pt-PT', people }) {
  db.sqlite.prepare('INSERT INTO family (family_id, code_hash, label, lang) VALUES (?, ?, ?, ?)')
    .run(id, await sha256hex(normaliseCode(code)), label, lang);
  people.forEach((p, i) => db.sqlite.prepare('INSERT INTO person (family_id, slot, name, is_extra) VALUES (?, ?, ?, ?)')
    .run(id, i + 1, p.name, p.is_extra ? 1 : 0));
}

// Two fictional families. The names are test data only.
export async function makeWorld(over = {}, dbOptions = {}) {
  const db = makeDb(dbOptions);
  await seedFamily(db, {
    id: 'fam_a', code: CODE_A, label: 'Test Family A', lang: 'en',
    people: [{ name: 'Alice Test' }, { name: 'Bob Test' }, { name: '', is_extra: true }],
  });
  await seedFamily(db, {
    id: 'fam_b', code: CODE_B, label: 'Test Family B', lang: 'es',
    people: [{ name: 'Carla Probe' }],
  });
  const env = { DB: db, ALLOWED_ORIGIN: ORIGIN, RSVP_CLOSES_AT: '2027-05-31T23:59:59.000Z', ADMIN_SECRET: ADMIN, ...over };
  return { db, env };
}

export function call(env, path, { code, body, origin = ORIGIN, method = 'POST', ip = '203.0.113.7', headers = {}, now = NOW, raw, stream } = {}) {
  const h = { ...headers };
  if (origin) h.origin = origin;
  if (code !== undefined) h['x-rsvp-code'] = code;
  if (ip) h['cf-connecting-ip'] = ip;
  const init = { method, headers: h };
  if (method !== 'GET' && method !== 'OPTIONS') init.body = raw ?? JSON.stringify(body ?? { revision: 0 });
  if (stream) { init.body = stream; init.duplex = 'half'; }
  return handle(new Request(`https://api.test${path}`, init), env, now);
}

export const answerBody = (over = {}) => ({
  revision: 0,
  answers: [{ slot: 1, attending: true, diet: 'no nuts' }, { slot: 2, attending: false }],
  message: 'hello',
  ...over,
});
