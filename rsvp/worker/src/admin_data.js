// What the couple see: totals, one card per family, and a CSV that opens cleanly in a spreadsheet.

export async function buildSummary(env) {
  const families = (await env.DB.prepare('SELECT family_id, label, lang FROM family ORDER BY label').all()).results;
  const people = (await env.DB.prepare('SELECT family_id, slot, name, is_extra FROM person ORDER BY family_id, slot').all()).results;
  const answers = (await env.DB.prepare('SELECT family_id, slot, attending, extra_name, diet FROM answer').all()).results;
  const responses = (await env.DB.prepare('SELECT family_id, message, updated_at, revision FROM response').all()).results;
  const ans = new Map(answers.map((a) => [`${a.family_id}:${a.slot}`, a]));
  const resp = new Map(responses.map((r) => [r.family_id, r]));
  const totals = { families: families.length, families_answered: 0, coming: 0, not_coming: 0, waiting: 0 };
  const rows = families.map((f) => {
    const r = resp.get(f.family_id);
    if (r) totals.families_answered += 1;
    const ppl = [];
    for (const p of people.filter((x) => x.family_id === f.family_id)) {
      const a = ans.get(`${p.family_id}:${p.slot}`);
      if (!r) {
        if (!p.is_extra) {
          totals.waiting += 1;
          ppl.push({ name: p.name, is_extra: false, attending: null, diet: '' });
        }
        continue;
      }
      if (!a && !p.is_extra) { // added after the family answered
        totals.waiting += 1;
        ppl.push({ name: p.name, is_extra: false, attending: null, diet: '' });
        continue;
      }
      const attending = !!(a && a.attending);
      if (attending) totals.coming += 1;
      else if (!p.is_extra) totals.not_coming += 1;
      if (p.is_extra && !attending) continue; // an unused extra seat is not a person
      ppl.push({ name: p.is_extra ? a.extra_name : p.name, is_extra: !!p.is_extra, attending, diet: a ? a.diet : '' });
    }
    return { label: f.label, lang: f.lang, answered: !!r, updated_at: r ? r.updated_at : null, message: r ? r.message : '', people: ppl };
  });
  return { totals, families: rows };
}

// Spreadsheet apps run a cell that starts with = + - @ as a formula.
function cell(v) {
  let s = String(v ?? '');
  if (/^\s*[=+\-@]|^[\t\r]/.test(s)) s = `'${s}`;
  return `"${s.replace(/"/g, '""')}"`;
}

export function toCsv(summary) {
  const head = ['family', 'person', 'status', 'diet_or_allergy', 'message', 'answered_at'];
  const lines = [head.map(cell).join(',')];
  for (const f of summary.families) {
    f.people.forEach((p, i) => {
      const status = p.attending === null ? 'waiting' : p.attending ? 'coming' : 'not_coming';
      lines.push([f.label, p.name, status, p.diet, i === 0 ? f.message : '', f.updated_at || ''].map(cell).join(','));
    });
  }
  return `\uFEFF${lines.join('\r\n')}\r\n`;
}
