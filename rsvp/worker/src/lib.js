// Small helpers shared by the Worker modules. Web-standard APIs only.

const enc = new TextEncoder();

export const LIMITS = Object.freeze({
  body_bytes: 8192,
  diet: 200,
  extra_name: 80,
  message: 600,
  fail_per_ip: 30, // failed code checks per address per window
  fail_window_ms: 60 * 60 * 1000,
  fail_global: 600, // past this many failures an hour nothing more is written
  admin_fail: 8,
  admin_fail_global: 200,
  admin_global_window_ms: 60 * 60 * 1000,
  admin_window_ms: 10 * 60 * 1000,
  changes_per_day: 20,
  history_rows: 200,
  day_ms: 24 * 60 * 60 * 1000,
  admin_secret_min: 24,
});

// Crockford base32 without I, L, O, U. 16 characters carry 80 random bits.
export const CODE_RE = /^[0-9A-HJKMNP-TV-Z]{16}$/;

export async function sha256hex(text) {
  const buf = await crypto.subtle.digest('SHA-256', enc.encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

// Ignore case, spaces and hyphens; O reads as 0, I and L read as 1.
export function normaliseCode(raw) {
  return String(raw ?? '').toUpperCase().replace(/[\s-]/g, '').replace(/O/g, '0').replace(/[IL]/g, '1');
}

export const iso = (ms) => new Date(ms).toISOString();

export function json(body, status = 200, extra = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...extra },
  });
}

export function withHeaders(response, extra) {
  const h = new Headers(response.headers);
  for (const [k, v] of Object.entries(extra)) h.set(k, v);
  return new Response(response.body, { status: response.status, headers: h });
}

// Zero-width and bidirectional controls can spoof text in the admin page and the CSV.
const INVISIBLE = /[\u200B-\u200F\u202A-\u202E\u2060-\u2064\u2066-\u2069\uFEFF]/g;

export function clean(value, { multiline = false } = {}) {
  let s = String(value).normalize('NFC').replace(INVISIBLE, '');
  s = multiline
    ? s.replace(/\r\n?/g, '\n').replace(/[\u0000-\u0009\u000B-\u001F\u007F]/g, ' ')
    : s.replace(/[\u0000-\u001F\u007F]/g, ' ');
  return s.trim();
}

export const len = (s) => [...s].length;

// Settings fail closed: a missing or malformed value closes the form.
const RFC3339_MS = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/;

export function closesAtMs(env) {
  const v = env.RSVP_CLOSES_AT;
  if (typeof v !== 'string' || !RFC3339_MS.test(v)) return null;
  const ms = Date.parse(v);
  return Number.isNaN(ms) ? null : ms;
}

// The closing time as sent to the client, or null when the setting is unusable.
export function closesAtIso(env) {
  return closesAtMs(env) === null ? null : env.RSVP_CLOSES_AT;
}

export function isOpen(env, now) {
  const closes = closesAtMs(env);
  return closes !== null && now < closes;
}

export function allowedOrigin(env) {
  const v = env.ALLOWED_ORIGIN;
  try {
    const u = new URL(v);
    return u.protocol === 'https:' && u.origin === v ? v : null;
  } catch {
    return null;
  }
}
