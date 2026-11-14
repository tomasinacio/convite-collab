// Fixed-window counters in the database. Windows and stamps are UTC RFC 3339.
import { iso, sha256hex, LIMITS } from './lib.js';

// Counts a hit and returns the count in the current window.
export async function hit(env, bucket, windowMs, now) {
  const row = await env.DB.prepare(
    `INSERT INTO throttle (bucket, window_start, n) VALUES (?1, ?2, 1)
     ON CONFLICT (bucket) DO UPDATE SET
         n = CASE WHEN window_start < ?3 THEN 1 ELSE n + 1 END,
         window_start = CASE WHEN window_start < ?3 THEN ?2 ELSE window_start END
     RETURNING n`,
  ).bind(bucket, iso(now), iso(now - windowMs)).first();
  if (row.n === 1) {
    // a new window: sweep rows that are over a day old
    await env.DB.prepare('DELETE FROM throttle WHERE window_start < ?1').bind(iso(now - LIMITS.day_ms)).run();
  }
  return row.n;
}

// Reads a count without writing, so blocked callers cost no writes.
export async function peek(env, bucket, windowMs, now) {
  const row = await env.DB.prepare('SELECT n FROM throttle WHERE bucket = ?1 AND window_start >= ?2')
    .bind(bucket, iso(now - windowMs)).first();
  return row ? row.n : 0;
}

// A random salt created on first use and kept in the database; the address hash also rotates daily.
const saltCache = new WeakMap();

async function salt(env) {
  if (saltCache.has(env.DB)) return saltCache.get(env.DB);
  const value = await readSalt(env);
  saltCache.set(env.DB, value);
  return value;
}

async function readSalt(env) {
  let row = await env.DB.prepare("SELECT value FROM setting WHERE name = 'ip_salt'").first();
  if (!row) {
    const fresh = [...crypto.getRandomValues(new Uint8Array(16))].map((b) => b.toString(16).padStart(2, '0')).join('');
    await env.DB.prepare("INSERT OR IGNORE INTO setting (name, value) VALUES ('ip_salt', ?1)").bind(fresh).run();
    row = await env.DB.prepare("SELECT value FROM setting WHERE name = 'ip_salt'").first();
  }
  return row.value;
}

// An IPv6 user can rotate freely inside a /64 block, so the block is the unit that is counted.
export function addressUnit(ip) {
  if (!ip.includes(':')) return ip;
  const [head, tail = ''] = ip.split('::');
  const a = head ? head.split(':') : [];
  const b = tail ? tail.split(':') : [];
  const full = ip.includes('::') ? [...a, ...Array(Math.max(0, 8 - a.length - b.length)).fill('0'), ...b] : a;
  return `${full.slice(0, 4).map((h) => h.toLowerCase().padStart(4, '0')).join(':')}/64`;
}

export async function ipBucketKey(request, env, now) {
  const ip = addressUnit(request.headers.get('cf-connecting-ip') || 'no-ip');
  const day = Math.floor(now / LIMITS.day_ms);
  return (await sha256hex(`${await salt(env)}|${day}|${ip}`)).slice(0, 24);
}
