// Validation of a submitted answer against the family's people. Pure: it never changes its input.
import { LIMITS, clean, len } from './lib.js';

export function validateSubmission(body, people) {
  const fields = [];
  const bad = (field, code) => fields.push({ field, code });
  if (!body || typeof body !== 'object' || Array.isArray(body)) return { ok: false, fields: [{ field: 'body', code: 'bad_type' }] };

  const slots = new Map(people.map((p) => [p.slot, p]));
  const out = new Map();
  const seen = new Set(); // slots that were addressed, even if their answer was invalid
  if (!Array.isArray(body.answers)) bad('answers', 'required');
  else {
    body.answers.forEach((a, i) => {
      const f = `answers.${i}`;
      if (!a || typeof a !== 'object' || Array.isArray(a)) return bad(f, 'bad_type');
      if (!Number.isInteger(a.slot) || !slots.has(a.slot)) return bad(`${f}.slot`, 'unknown_slot');
      if (seen.has(a.slot)) return bad(`${f}.slot`, 'duplicate_slot');
      seen.add(a.slot);
      const person = slots.get(a.slot);
      let attending = a.attending;
      if (typeof attending !== 'boolean') {
        if (attending === undefined && person.is_extra) attending = false;
        else return bad(`${f}.attending`, 'required');
      }
      const row = { slot: a.slot, attending, name: '', diet: '' };
      if (attending) {
        if (a.diet !== undefined && a.diet !== null) {
          if (typeof a.diet !== 'string') bad(`${f}.diet`, 'bad_type');
          else {
            row.diet = clean(a.diet);
            if (len(row.diet) > LIMITS.diet) bad(`${f}.diet`, 'too_long');
          }
        }
        if (person.is_extra) {
          row.name = typeof a.name === 'string' ? clean(a.name) : '';
          if (!row.name) bad(`${f}.name`, 'name_required');
          else if (len(row.name) > LIMITS.extra_name) bad(`${f}.name`, 'too_long');
        }
      }
      out.set(a.slot, row);
    });
    for (const p of people) {
      if (!p.is_extra && !seen.has(p.slot)) bad(`answers.slot.${p.slot}`, 'required');
      if (p.is_extra && !out.has(p.slot)) out.set(p.slot, { slot: p.slot, attending: false, name: '', diet: '' });
    }
  }

  // the revision the form was loaded with, so a stale form cannot overwrite a newer answer
  if (!Number.isInteger(body.revision) || body.revision < 0) bad('revision', 'required');

  let message = '';
  if (body.message !== undefined && body.message !== null) {
    if (typeof body.message !== 'string') bad('message', 'bad_type');
    else {
      message = clean(body.message, { multiline: true });
      if (len(message) > LIMITS.message) bad('message', 'too_long');
    }
  }
  if (fields.length) return { ok: false, fields };
  return { ok: true, revision: body.revision, answers: [...out.values()].sort((a, b) => a.slot - b.slot), message };
}
