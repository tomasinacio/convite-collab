// The couple's phone page. Static text only; the secret stays in a variable in the open tab.

export const adminHtml = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta name="referrer" content="no-referrer">
<title>RSVP answers</title>
<style>
:root{--paper:#F6EFDF;--ink:#3B2F25;--olive:#4F5F2E;--terra:#8A4129;--line:#D9C9A8;--card:#FBF7EC}
@media (prefers-color-scheme:dark){:root{--paper:#1F1B16;--ink:#EFE6D2;--olive:#B9C98F;--terra:#E0A184;--line:#4A4033;--card:#28231C}}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.5 Georgia,serif}
main{max-width:40rem;margin:0 auto;padding:16px 16px 48px}h1{font-size:1.5rem;color:var(--olive)}
input,button{font:inherit;font-size:16px;min-height:44px;padding:8px 12px;border-radius:6px;border:1px solid var(--line);background:var(--card);color:var(--ink)}
button{cursor:pointer}button[aria-pressed=true]{background:var(--olive);color:var(--paper);border-color:var(--olive)}
.row{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 14px;margin:10px 0}
.card h3{margin:0 0 4px;font-size:1.05rem}.muted{opacity:.8;font-size:.9rem}.err{color:var(--terra)}ul{margin:4px 0;padding-left:1.1rem}
.tot{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.tot div{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 12px}.tot b{display:block;font-size:1.6rem}
</style>
</head>
<body>
<main>
<h1>RSVP answers</h1>
<form id="login" class="row"><label for="secret">Admin secret</label><input id="secret" type="password" autocomplete="off" required><button type="submit">Open</button></form>
<p id="msg" class="err" role="status"></p>
<div id="app" hidden></div>
</main>
<script src="/admin/app.js"></script>
</body>
</html>`;

export const adminJs = String.raw`(function () {
  var secret = '';
  var data = null;
  var filter = 'all';
  var msg = document.getElementById('msg');
  var app = document.getElementById('app');

  function el(tag, text, cls) {
    var e = document.createElement(tag);
    if (text !== undefined) e.textContent = text;
    if (cls) e.className = cls;
    return e;
  }
  function call(path) {
    return fetch(path, { headers: { Authorization: 'Bearer ' + secret }, cache: 'no-store' });
  }
  function status(p) { return p.attending === null ? 'waiting' : (p.attending ? 'coming' : 'not coming'); }
  function keep(f) {
    if (filter === 'waiting') return !f.answered;
    if (filter === 'coming') return f.people.some(function (p) { return p.attending === true; });
    if (filter === 'not') return f.answered && f.people.every(function (p) { return p.attending === false; });
    if (filter === 'diet') return f.people.some(function (p) { return p.diet; });
    if (filter === 'msg') return !!f.message;
    return true;
  }
  function render() {
    app.textContent = '';
    var t = data.totals;
    var tot = el('div', undefined, 'tot');
    [['Coming', t.coming], ['Not coming', t.not_coming], ['Waiting', t.waiting], ['Families answered', t.families_answered + ' of ' + t.families]].forEach(function (x) {
      var d = el('div'); d.appendChild(el('b', String(x[1]))); d.appendChild(el('span', x[0])); tot.appendChild(d);
    });
    app.appendChild(tot);
    var bar = el('div', undefined, 'row');
    [['all', 'All'], ['waiting', 'Waiting'], ['coming', 'Coming'], ['not', 'Not coming'], ['diet', 'Diet'], ['msg', 'Messages']].forEach(function (x) {
      var b = el('button', x[1]); b.type = 'button'; b.setAttribute('aria-pressed', filter === x[0] ? 'true' : 'false');
      b.addEventListener('click', function () { filter = x[0]; render(); });
      bar.appendChild(b);
    });
    var csv = el('button', 'Download CSV'); csv.type = 'button';
    csv.addEventListener('click', download);
    bar.appendChild(csv);
    var again = el('button', 'Refresh'); again.type = 'button';
    again.addEventListener('click', load);
    bar.appendChild(again);
    app.appendChild(bar);
    data.families.filter(keep).forEach(function (f) {
      var c = el('div', undefined, 'card');
      c.appendChild(el('h3', f.label));
      c.appendChild(el('div', f.answered ? 'Answered ' + f.updated_at : 'No answer yet', 'muted'));
      var ul = el('ul');
      f.people.forEach(function (p) {
        ul.appendChild(el('li', p.name + ': ' + status(p) + (p.diet ? ' (' + p.diet + ')' : '')));
      });
      c.appendChild(ul);
      if (f.message) c.appendChild(el('p', f.message));
      app.appendChild(c);
    });
  }
  function load() {
    msg.textContent = 'Loading…';
    call('/api/admin/summary').then(function (r) {
      if (r.status === 401) { msg.textContent = 'Wrong secret.'; return null; }
      if (r.status === 429) { msg.textContent = 'Too many tries. Wait ten minutes.'; return null; }
      if (!r.ok) { msg.textContent = 'Could not load (' + r.status + ').'; return null; }
      return r.json();
    }).then(function (j) {
      if (!j) return;
      data = j; msg.textContent = ''; app.hidden = false; render();
    }).catch(function () { msg.textContent = 'No connection. Try again.'; });
  }
  function download() {
    call('/api/admin/export.csv').then(function (r) {
      if (!r.ok) throw new Error('status ' + r.status);
      return r.blob();
    }).then(function (b) {
      var a = document.createElement('a');
      var u = URL.createObjectURL(b);
      a.href = u; a.download = 'rsvp.csv';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(u); }, 1000);
    }).catch(function () { msg.textContent = 'Download failed.'; });
  }
  document.getElementById('login').addEventListener('submit', function (e) {
    e.preventDefault();
    secret = document.getElementById('secret').value;
    document.getElementById('secret').value = '';
    load();
  });
})();
`;
