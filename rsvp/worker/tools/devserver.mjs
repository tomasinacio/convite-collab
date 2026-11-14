// Local test server: the real Worker code over a node:sqlite D1 stand-in, seeded from a seed file (the FAKE guests).
// Usage: node tools/devserver.mjs SEED.sql [PORT] [ORIGIN] [CLOSES_AT]. Test use only; never deployed.
import { createServer } from 'node:http';
import { readFileSync } from 'node:fs';
import { makeDb } from '../test/helpers.js';
import { handle } from '../src/core.js';

const [seed, port = '8787', origin = 'http://localhost:8765', closes = '2099-01-01T00:00:00.000Z'] = process.argv.slice(2);
const db = makeDb();
db.sqlite.exec(readFileSync(seed, 'utf8'));
const env = { DB: db, ALLOWED_ORIGIN: 'https://site.test', RSVP_CLOSES_AT: closes, ADMIN_SECRET: 'dev-admin-secret-not-real-0000' };
createServer(async (req, res) => {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  // the Worker only accepts an https origin, so the local page's origin is mapped to a pinned stand-in on the way in and back out
  const headers = { ...req.headers, 'cf-connecting-ip': '203.0.113.50' };
  if (headers.origin === origin) headers.origin = 'https://site.test';
  const init = { method: req.method, headers };
  if (!['GET', 'HEAD'].includes(req.method)) init.body = Buffer.concat(chunks);
  const r = await handle(new Request(`http://localhost:${port}${req.url}`, init), env, Date.now());
  const out = Object.fromEntries(r.headers);
  if (out['access-control-allow-origin'] === 'https://site.test') out['access-control-allow-origin'] = origin;
  res.writeHead(r.status, out);
  res.end(Buffer.from(await r.arrayBuffer()));
}).listen(Number(port), () => console.log(`dev worker on ${port}`));
