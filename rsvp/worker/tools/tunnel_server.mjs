// Temporary test server for a shared test link: serves a built site and the real Worker code (stand-in database, seeded with the FAKE guests)
// on one address, so one public https origin does both. Test use only; never deployed. The admin routes are blocked here.
// Usage: node tools/tunnel_server.mjs SEED.sql SITE_DIR PORT https://the-public-origin [CLOSES_AT]
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync } from 'node:fs';
import { extname, join, normalize } from 'node:path';
import { makeDb } from '../test/helpers.js';
import { handle } from '../src/core.js';

const [seed, site, port, origin, closes = '2099-01-01T00:00:00.000Z'] = process.argv.slice(2);
const db = makeDb();
db.sqlite.exec(readFileSync(seed, 'utf8'));
// the Worker only accepts an https origin; over the private tailnet the page is plain http, so its origin is mapped to a pinned stand-in on the way in and back out
const env = { DB: db, ALLOWED_ORIGIN: 'https://site.test', RSVP_CLOSES_AT: closes, ADMIN_SECRET: '' };
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.woff2': 'font/woff2', '.png': 'image/png', '.jpg': 'image/jpeg', '.txt': 'text/plain' };
createServer(async (req, res) => {
  try {
    console.log(new Date().toISOString().slice(11, 19), req.method, req.url.split('#')[0].slice(0, 60), String(req.headers['user-agent'] || '').slice(0, 40)); // path only: no codes travel in the path
    const url = new URL(req.url, origin);
    if (url.pathname.startsWith('/admin') || url.pathname.startsWith('/api/admin')) { res.writeHead(404); return res.end(); }
    if (url.pathname.startsWith('/api/')) {
      const chunks = [];
      for await (const c of req) chunks.push(c);
      const headers = { ...req.headers, 'cf-connecting-ip': String(req.headers['x-forwarded-for'] || req.socket.remoteAddress).split(',')[0].trim() };
      const seen = headers.origin; // any origin of this test server (tunnel name, tailnet name or address) is mapped
      if (seen) headers.origin = 'https://site.test';
      const init = { method: req.method, headers };
      if (!['GET', 'HEAD'].includes(req.method)) init.body = Buffer.concat(chunks);
      const r = await handle(new Request(origin + req.url, init), env, Date.now());
      const out = Object.fromEntries(r.headers);
      if (out['access-control-allow-origin'] === 'https://site.test') out['access-control-allow-origin'] = seen;
      res.writeHead(r.status, out);
      return res.end(Buffer.from(await r.arrayBuffer()));
    }
    let p = normalize(join(site, url.pathname === '/' ? 'index.html' : url.pathname));
    if (!p.startsWith(normalize(site)) || !existsSync(p) || !statSync(p).isFile()) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'content-type': TYPES[extname(p)] || 'application/octet-stream', 'cache-control': 'no-cache' });
    res.end(readFileSync(p));
  } catch (e) { res.writeHead(500); res.end('error'); }
}).listen(Number(port), '127.0.0.1', () => console.log('test server on', port));
