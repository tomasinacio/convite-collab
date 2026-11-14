// RSVP core: Web-standard Request and Response over a D1-shaped database.
// The Worker (index.js) and the tests (test/) both call handle().

import { adminHtml, adminJs } from './admin_page.js';
import { buildSummary, toCsv } from './admin_data.js';
import { hit, peek, ipBucketKey } from './throttle.js';
import { validateSubmission } from './validate.js';
import {
  LIMITS, CODE_RE, normaliseCode, sha256hex, json, withHeaders, iso, isOpen, allowedOrigin, closesAtIso,
} from './lib.js';

const retryAfter = (ms) => ({ 'retry-after': String(Math.ceil(ms / 1000)) });

function corsHeaders(origin) {
  return {
    'access-control-allow-origin': origin,
    'access-control-allow-headers': 'content-type, x-rsvp-code',
    'access-control-allow-methods': 'POST, OPTIONS',
    'access-control-expose-headers': 'retry-after',
    'access-control-max-age': '86400',
    vary: 'Origin',
  };
}

// ---- reading a family ----------------------------------------------------------------------

// One round trip for all four reads.
async function loadFamily(env, familyId) {
  const [family, people, answers, response] = await env.DB.batch([
    env.DB.prepare('SELECT family_id, label, lang FROM family WHERE family_id = ?1').bind(familyId),
    env.DB.prepare('SELECT slot, name, is_extra FROM person WHERE family_id = ?1 ORDER BY slot').bind(familyId),
    env.DB.prepare('SELECT slot, attending, extra_name, diet FROM answer WHERE family_id = ?1 ORDER BY slot').bind(familyId),
    env.DB.prepare('SELECT message, updated_at, revision, last_write FROM response WHERE family_id = ?1').bind(familyId),
  ]);
  return { family: family.results[0], people: people.results, answers: answers.results, response: response.results[0] ?? null };
}

// The only shape a guest ever receives: their own family.
function publicView(env, data, now) {
  const byslot = new Map(data.answers.map((a) => [a.slot, a]));
  return {
    family: { label: data.family.label, lang: data.family.lang },
    people: data.people.map((p) => {
      const a = byslot.get(p.slot);
      return {
        slot: p.slot,
        name: p.name,
        is_extra: !!p.is_extra,
        answer: a ? { attending: !!a.attending, name: a.extra_name, diet: a.diet } : null,
      };
    }),
    message: data.response ? data.response.message : '',
    answered: !!data.response,
    updated_at: data.response ? data.response.updated_at : null,
    revision: data.response ? data.response.revision : 0,
    open: isOpen(env, now),
    closes_at: closesAtIso(env),
  };
}

function sameAsStored(data, submitted) {
  if (!data.response || data.response.message !== submitted.message) return false;
  const stored = new Map(data.answers.map((a) => [a.slot, a]));
  return submitted.answers.every((a) => {
    const s = stored.get(a.slot);
    return s && !!s.attending === a.attending && s.extra_name === a.name && s.diet === a.diet;
  });
}

// ---- routes: guest -------------------------------------------------------------------------

// A correct code always works, even from a busy address. A wrong code is refused once its address
// or the whole site is over the failure budget, and from then on nothing more is written.
async function authenticate(request, env, now) {
  const ip = await ipBucketKey(request, env, now);
  const code = normaliseCode(request.headers.get('x-rsvp-code'));
  const row = CODE_RE.test(code)
    ? await env.DB.prepare('SELECT family_id FROM family WHERE code_hash = ?1').bind(await sha256hex(code)).first()
    : null;
  if (row) return { familyId: row.family_id };
  const [mine, all] = await Promise.all([
    peek(env, `fail:${ip}`, LIMITS.fail_window_ms, now),
    peek(env, 'fail:all', LIMITS.fail_window_ms, now),
  ]);
  if (mine >= LIMITS.fail_per_ip || all >= LIMITS.fail_global) {
    return { response: json({ error: 'too_many_attempts' }, 429, retryAfter(LIMITS.fail_window_ms)) };
  }
  await hit(env, `fail:${ip}`, LIMITS.fail_window_ms, now);
  await hit(env, 'fail:all', LIMITS.fail_window_ms, now);
  return { response: json({ error: 'not_found' }, 404) };
}

// Reads at most body_bytes, whatever the headers claim.
async function readBody(request) {
  if (Number(request.headers.get('content-length') || 0) > LIMITS.body_bytes) return { tooBig: true };
  const reader = request.body ? request.body.getReader() : null;
  if (!reader) return { invalid: true };
  const chunks = [];
  let total = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    total += value.byteLength;
    if (total > LIMITS.body_bytes) {
      await reader.cancel().catch(() => {});
      return { tooBig: true };
    }
    chunks.push(value);
  }
  const bytes = new Uint8Array(total);
  let at = 0;
  for (const c of chunks) {
    bytes.set(c, at);
    at += c.byteLength;
  }
  try {
    return { value: JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)) };
  } catch {
    return { invalid: true };
  }
}

async function lookup(request, env, now, cors) {
  const auth = await authenticate(request, env, now);
  if (auth.response) return withHeaders(auth.response, cors);
  return json(publicView(env, await loadFamily(env, auth.familyId), now), 200, cors);
}

async function answer(request, env, now, cors) {
  const auth = await authenticate(request, env, now);
  if (auth.response) return withHeaders(auth.response, cors);
  if (!isOpen(env, now)) return json({ error: 'closed', closes_at: closesAtIso(env) }, 403, cors);

  const body = await readBody(request);
  if (body.tooBig) return json({ error: 'too_big' }, 413, cors);
  if (body.invalid) return json({ error: 'invalid', fields: [{ field: 'body', code: 'bad_json' }] }, 400, cors);

  const f = auth.familyId;
  const data = await loadFamily(env, f);

  // hidden field that only a bot fills: look saved, store nothing
  if (body.value && typeof body.value.website === 'string' && body.value.website.trim() !== '') {
    return json({ status: 'saved', ...publicView(env, data, now) }, 200, cors);
  }

  const checked = validateSubmission(body.value, data.people);
  if (!checked.ok) return json({ error: 'invalid', fields: checked.fields }, 400, cors);
  // the same answer sent again (a double tap) is a success, not a conflict
  if (sameAsStored(data, checked)) return json({ status: 'unchanged', ...publicView(env, data, now) }, 200, cors);

  const current = data.response ? data.response.revision : 0;
  if (checked.revision !== current) return json({ error: 'conflict', ...publicView(env, data, now) }, 409, cors);

  const day = Math.floor(now / LIMITS.day_ms);
  const chg = `chg:${f}:${day}`;
  if ((await peek(env, chg, LIMITS.day_ms, now)) >= LIMITS.changes_per_day) {
    return json({ error: 'too_many_changes' }, 429, { ...cors, ...retryAfter(LIMITS.day_ms) });
  }
  const hist = await env.DB.prepare('SELECT COUNT(*) AS c FROM response_history WHERE family_id = ?1').bind(f).first();
  if (hist.c >= LIMITS.history_rows) return json({ error: 'too_many_changes' }, 429, cors);

  // Every write after the first only applies if this request's own write won: two requests at the
  // same moment cannot both change the same family (the other sees last_write differ).
  const mine = [...crypto.getRandomValues(new Uint8Array(12))].map((b) => b.toString(16).padStart(2, '0')).join('');
  const at = iso(now);
  const first = data.response
    ? env.DB.prepare(
      `UPDATE response SET message = ?2, updated_at = ?3, revision = revision + 1, last_write = ?4
       WHERE family_id = ?1 AND revision = ?5`,
    ).bind(f, checked.message, at, mine, current)
    : env.DB.prepare(
      `INSERT INTO response (family_id, message, created_at, updated_at, revision, last_write)
       VALUES (?1, ?2, ?3, ?3, 1, ?4) ON CONFLICT (family_id) DO NOTHING`,
    ).bind(f, checked.message, at, mine);
  await env.DB.batch([
    first,
    env.DB.prepare(
      `INSERT INTO response_history (family_id, at, revision, payload)
       SELECT ?1, ?2, revision, ?3 FROM response WHERE family_id = ?1 AND last_write = ?4`,
    ).bind(f, at, JSON.stringify({ answers: checked.answers, message: checked.message }), mine),
    ...checked.answers.map((a) => env.DB.prepare(
      `INSERT INTO answer (family_id, slot, attending, extra_name, diet)
       SELECT ?1, ?2, ?3, ?4, ?5
       WHERE EXISTS (SELECT 1 FROM response WHERE family_id = ?1 AND last_write = ?6)
       ON CONFLICT (family_id, slot) DO UPDATE SET attending = ?3, extra_name = ?4, diet = ?5`,
    ).bind(f, a.slot, a.attending ? 1 : 0, a.name, a.diet, mine)),
  ]);

  const fresh = await loadFamily(env, f);
  if (!fresh.response || fresh.response.last_write !== mine) { // another request got there first
    if (sameAsStored(fresh, checked)) return json({ status: 'unchanged', ...publicView(env, fresh, now) }, 200, cors);
    return json({ error: 'conflict', ...publicView(env, fresh, now) }, 409, cors);
  }
  await hit(env, chg, LIMITS.day_ms, now); // counted once the change is really stored
  return json({ status: 'saved', ...publicView(env, fresh, now) }, 200, cors);
}

// ---- routes: the couple --------------------------------------------------------------------

async function adminAuth(request, env, now) {
  const secret = env.ADMIN_SECRET;
  if (typeof secret !== 'string' || secret.length < LIMITS.admin_secret_min) return json({ error: 'not_found' }, 404);
  const ip = await ipBucketKey(request, env, now);
  const [mine, all] = await Promise.all([
    peek(env, `adminfail:${ip}`, LIMITS.admin_window_ms, now),
    peek(env, 'adminfail:all', LIMITS.admin_global_window_ms, now),
  ]);
  if (mine >= LIMITS.admin_fail || all >= LIMITS.admin_fail_global) {
    return json({ error: 'too_many_attempts' }, 429, retryAfter(LIMITS.admin_window_ms));
  }
  const given = (request.headers.get('authorization') || '').replace(/^Bearer\s+/i, '');
  // compare digests so the time taken does not depend on how much of the secret matches
  const [a, b] = await Promise.all([sha256hex(given), sha256hex(secret)]);
  let diff = given ? 0 : 1;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  if (diff !== 0) {
    await hit(env, `adminfail:${ip}`, LIMITS.admin_window_ms, now);
    await hit(env, 'adminfail:all', LIMITS.admin_global_window_ms, now);
    return json({ error: 'unauthorized' }, 401);
  }
  return null;
}

const PAGE_HEADERS = {
  'cache-control': 'no-store',
  'x-robots-tag': 'noindex, nofollow',
  'x-content-type-options': 'nosniff',
  'referrer-policy': 'no-referrer',
};
const ADMIN_CSP = "default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'";
const ADMIN_DATA = new Set(['/api/admin/summary', '/api/admin/export.csv']);

async function admin(request, env, url, now) {
  if (request.method !== 'GET') return json({ error: 'method_not_allowed' }, 405);
  if (url.pathname === '/admin') {
    return new Response(adminHtml, { headers: { ...PAGE_HEADERS, 'content-type': 'text/html; charset=utf-8', 'content-security-policy': ADMIN_CSP } });
  }
  if (url.pathname === '/admin/app.js') {
    return new Response(adminJs, { headers: { ...PAGE_HEADERS, 'content-type': 'text/javascript; charset=utf-8' } });
  }
  if (!ADMIN_DATA.has(url.pathname)) return json({ error: 'not_found' }, 404);
  const denied = await adminAuth(request, env, now);
  if (denied) return denied;
  const summary = await buildSummary(env);
  if (url.pathname === '/api/admin/summary') return json(summary, 200);
  return new Response(toCsv(summary), {
    headers: { ...PAGE_HEADERS, 'content-type': 'text/csv; charset=utf-8', 'content-disposition': 'attachment; filename="rsvp.csv"' },
  });
}

// ---- entry ---------------------------------------------------------------------------------

export async function handle(request, env, now = Date.now()) {
  let cors = {};
  try {
    const url = new URL(request.url);
    if (url.pathname === '/admin' || url.pathname.startsWith('/admin/') || url.pathname.startsWith('/api/admin/')) {
      return await admin(request, env, url, now);
    }
    if (url.pathname !== '/api/lookup' && url.pathname !== '/api/answer') return json({ error: 'not_found' }, 404);

    const allowed = allowedOrigin(env);
    if (!allowed) return json({ error: 'not_configured' }, 503);
    // a browser always sends Origin on a cross-site request; anything else is refused
    if (request.headers.get('origin') !== allowed) return json({ error: 'forbidden_origin' }, 403);
    cors = corsHeaders(allowed);
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (request.method !== 'POST') return json({ error: 'method_not_allowed' }, 405, cors);
    return url.pathname === '/api/lookup' ? await lookup(request, env, now, cors) : await answer(request, env, now, cors);
  } catch {
    return json({ error: 'server_error' }, 500, cors);
  }
}
