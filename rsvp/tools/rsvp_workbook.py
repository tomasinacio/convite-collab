#!/usr/bin/env python3
"""The couple's workbook: guest list in, personal links out, answers back.

owner: Tomas | review date: 2026-11-19
canonical path: projects/wedding-invite/rsvp/tools/rsvp_workbook.py
rollback: rm projects/wedding-invite/rsvp/tools/rsvp_workbook.py (the workbook is a plain .xlsx)

Run from projects/wedding-invite with: .venv/bin/python -I rsvp/tools/rsvp_workbook.py COMMAND

  init    create guests/convite-rsvp.xlsx (template; never overwrites without --force)
  links   read the Guests sheet, keep or create one private code per household, write the Links
          sheet and output/seed.sql (families and people, with only a SHA-256 of each code)
  sync    pull the answers (from D1 through the user's own wrangler login, or from a SQLite file)
          into the Answers, Pending, Messages and Summary sheets

Private data never leaves guests/ and output/ (both git-ignored). The tool prints counts, never
codes, names or phone numbers. It never reads or asks for credentials: wrangler uses the user's
own login. Guest-provided text is always written as text, never as a formula.
"""

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import sqlite3
import subprocess
import sys
import urllib.parse
from datetime import UTC, datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent  # .../rsvp
GUESTS = ROOT / "guests"
OUTPUT = ROOT / "output"
WORKBOOK = GUESTS / "convite-rsvp.xlsx"
SIDECAR = GUESTS / "codes.json"

ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"  # Crockford base32: no I, L, O, U
CODE_LEN = 16  # 80 random bits
LANGS = ("pt-PT", "en", "es")
DEFAULT_SITE = "https://tomasinacio.github.io/convite/"
MAX_EXTRA = 6

GUEST_HEADERS = ["id", "label", "lang", "members", "extra_seats", "phone", "notes"]
SHEETS = ["README", "Settings", "Guests", "Links", "Answers", "Pending", "Messages", "Summary"]
CONTROL = re.compile(r"[\u0000-\u001F\u007F​-‏‪-‮⁠-⁤⁦-⁩﻿]")


class ToolError(Exception):
    """A problem the user can fix; printed without a stack trace."""


# ---- small helpers -------------------------------------------------------------------------


def clean(value):
    """Plain text without control, zero-width or direction characters."""
    return CONTROL.sub("", "" if value is None else str(value)).strip()


def normalise_code(raw):
    s = re.sub(r"[\s-]", "", str(raw).upper())
    return s.replace("O", "0").replace("I", "1").replace("L", "1")


def code_hash(code):
    return hashlib.sha256(normalise_code(code).encode()).hexdigest()


def new_code(taken):
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LEN))
        if code not in taken:
            return code


def group(code):
    return "-".join(code[i : i + 4] for i in range(0, len(code), 4))


def put(ws, row, col, value, bold=False):
    """Write a cell. Text is forced to be text, so a name that starts with = is not a formula."""
    cell = ws.cell(row=row, column=col)
    cell.value = value
    if isinstance(value, str):
        cell.data_type = "s"
    if bold:
        cell.font = Font(bold=True)
    return cell


def link_cell(ws, row, col, text, url):
    cell = put(ws, row, col, text)
    cell.hyperlink = url
    cell.font = Font(color="0563C1", underline="single")
    return cell


def now_iso():
    t = datetime.now(UTC)
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}Z"


def sql_text(value):
    return "'" + clean(value).replace("'", "''") + "'"


def write_private(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)


def backup(path):
    if not path.exists():
        return None
    dest = GUESTS / "backups" / f"{path.stem}-{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}.xlsx"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest)
    return dest


def style_header(ws, widths):
    fill = PatternFill("solid", fgColor="E6D6B8")
    for i, w in enumerate(widths, start=1):
        c = ws.cell(row=1, column=i)
        c.font = Font(bold=True)
        c.fill = fill
        ws.column_dimensions[c.column_letter].width = w
    ws.freeze_panes = "A2"


# ---- the workbook --------------------------------------------------------------------------

README_LINES = [
    "How this workbook works",
    "",
    "1. Fill the Guests sheet: one row per household. label is how you name them (only you",
    "   see it), lang is pt-PT, en or es, members are the people's names separated by ; and",
    "   extra_seats is the",
    "   number of unnamed plus-ones. phone and notes are optional and never leave this computer.",
    "2. Run the links command. It fills the id column, creates one private code per household and",
    "   writes the Links sheet. Paste each link into WhatsApp.",
    "3. After guests answer, run the sync command. It refreshes Answers, Pending, Messages and",
    "   Summary. Do not type in those four sheets; they are rewritten each time.",
    "4. Settings: site_url is the invitation address; reminder_text is the text WhatsApp opens",
    "   with on the Pending sheet. You write it. TODO(user)",
    "",
    "Edit people only in place (spelling) or add new ones at the end of members. Removing or",
    "reordering people after the links went out would mix up answers; the tool refuses unless",
    "you pass --force.",
    "",
    "This file is private. It is ignored by git. Keep it out of shared folders.",
]


def build_template():
    wb = Workbook()
    wb.remove(wb.active)
    sheets = {name: wb.create_sheet(name) for name in SHEETS}
    for i, line in enumerate(README_LINES, start=1):
        put(sheets["README"], i, 1, line, bold=(i == 1))
    sheets["README"].column_dimensions["A"].width = 110

    st = sheets["Settings"]
    put(st, 1, 1, "site_url", True)
    put(st, 1, 2, DEFAULT_SITE)
    put(st, 2, 1, "reminder_text", True)
    put(st, 2, 2, "")
    put(st, 2, 3, "TODO(user): the text WhatsApp opens with on the Pending sheet")
    st.column_dimensions["A"].width = 18
    st.column_dimensions["B"].width = 60

    g = sheets["Guests"]
    for i, h in enumerate(GUEST_HEADERS, start=1):
        put(g, 1, i, h)
    style_header(g, [8, 28, 8, 50, 12, 18, 30])
    dv_lang = DataValidation(type="list", formula1='"pt-PT,en,es"', allow_blank=True)
    dv_extra = DataValidation(
        type="whole", operator="between", formula1="0", formula2=str(MAX_EXTRA), allow_blank=True
    )
    g.add_data_validation(dv_lang)
    g.add_data_validation(dv_extra)
    dv_lang.add("C2:C400")
    dv_extra.add("E2:E400")
    for r in range(2, 401):
        g.cell(row=r, column=1).font = Font(color="808080")
        for c in (2, 4):
            g.cell(row=r, column=c).alignment = Alignment(wrap_text=True, vertical="top")

    heads = {
        "Links": (["id", "label", "lang", "code", "link"], [8, 28, 8, 24, 70]),
        "Answers": (
            ["family", "person", "status", "diet_or_allergy", "answered_at"],
            [28, 28, 12, 40, 26],
        ),
        "Pending": (["family", "lang", "phone", "send a reminder"], [28, 8, 18, 30]),
        "Messages": (["family", "message", "answered_at"], [28, 80, 26]),
        "Summary": (["what", "number"], [34, 12]),
    }
    for name, (cols, widths) in heads.items():
        for i, h in enumerate(cols, start=1):
            put(sheets[name], 1, i, h)
        style_header(sheets[name], widths)
    return wb


def cmd_init(args):
    if WORKBOOK.exists() and not args.force:
        raise ToolError(
            f"{WORKBOOK.name} already exists. Use --force to replace it (a backup is made)."
        )
    backup(WORKBOOK)
    GUESTS.mkdir(parents=True, exist_ok=True)
    build_template().save(WORKBOOK)
    os.chmod(WORKBOOK, 0o600)
    print(f"Created {WORKBOOK}. Fill the Guests sheet, then run: links")


def open_workbook():
    if not WORKBOOK.exists():
        raise ToolError("No workbook yet. Run: init")
    return load_workbook(WORKBOOK)


def setting(wb, name):
    if "Settings" not in wb.sheetnames:
        return ""
    for row in wb["Settings"].iter_rows(min_row=1, max_col=2, values_only=True):
        if row[0] == name:
            return clean(row[1])
    return ""


# ---- guests, slots and codes ---------------------------------------------------------------


def read_guests(wb):
    ws = wb["Guests"]
    rows, problems, labels = [], [], set()
    for r in range(2, ws.max_row + 1):
        vals = [ws.cell(row=r, column=c).value for c in range(1, len(GUEST_HEADERS) + 1)]
        if not any(v not in (None, "") for v in vals[1:]):
            continue
        rec = dict(zip(GUEST_HEADERS, vals, strict=True))
        rec["row"] = r
        rec["label"] = clean(rec["label"])
        rec["lang"] = clean(rec["lang"]) or "pt-PT"
        names = re.split(r"[;\n]", str(rec["members"] or ""))
        rec["members"] = [clean(n) for n in names if clean(n)]
        try:
            rec["extra_seats"] = int(rec["extra_seats"] or 0)
        except (TypeError, ValueError):
            rec["extra_seats"] = -1
        if not rec["label"]:
            problems.append(f"Guests row {r}: label is empty")
        if rec["lang"] not in LANGS:
            problems.append(f"Guests row {r}: lang must be one of {', '.join(LANGS)}")
        if not rec["members"]:
            problems.append(f"Guests row {r}: members is empty")
        if not 0 <= rec["extra_seats"] <= MAX_EXTRA:
            problems.append(
                f"Guests row {r}: extra_seats must be a whole number from 0 to {MAX_EXTRA}"
            )
        if rec["label"] in labels:
            problems.append(f"Guests row {r}: the label is used twice")
        labels.add(rec["label"])
        rows.append(rec)
    return rows, problems


def load_sidecar():
    if not SIDECAR.exists():
        return {"families": {}}
    return json.loads(SIDECAR.read_text(encoding="utf-8"))


def plan_people(old, members, extra_seats, force):
    """Stable slots: named people keep their slot by position, new ones get new slots at the end."""
    problems = []
    people = [dict(p) for p in old] if old else []
    named = [p for p in people if not p["extra"]]
    extras = [p for p in people if p["extra"]]
    old_names = [p["name"] for p in named]
    if old:
        if len(members) < len(named):
            problems.append("a person was removed")
        elif members[: len(named)] != old_names and sorted(members[: len(named)]) == sorted(
            old_names
        ):
            problems.append("people were reordered")
        if extra_seats < len(extras):
            problems.append("extra seats were reduced")
    if problems and not force:
        return None, problems
    next_slot = max([p["slot"] for p in people], default=0) + 1
    out = []
    for i, name in enumerate(members):
        if i < len(named):
            out.append({"slot": named[i]["slot"], "name": name, "extra": False})
        else:
            out.append({"slot": next_slot, "name": name, "extra": False})
            next_slot += 1
    for i in range(extra_seats):
        if i < len(extras):
            out.append({"slot": extras[i]["slot"], "name": "", "extra": True})
        else:
            out.append({"slot": next_slot, "name": "", "extra": True})
            next_slot += 1
    return sorted(out, key=lambda p: p["slot"]), []


def build_seed(families):
    lines = [
        "-- Generated by rsvp_workbook.py. Private: holds names. Safe to run again.",
        "-- It only writes family and person rows; answers are never touched.",
    ]
    for f in families:
        lines.append(
            "INSERT INTO family (family_id, code_hash, label, lang) VALUES "
            f"({sql_text(f['id'])}, {sql_text(f['hash'])}, {sql_text(f['label'])}, "
            f"{sql_text(f['lang'])}) "
            "ON CONFLICT (family_id) DO UPDATE SET code_hash = excluded.code_hash, "
            "label = excluded.label, lang = excluded.lang;"
        )
        for p in f["people"]:
            lines.append(
                "INSERT INTO person (family_id, slot, name, is_extra) VALUES "
                f"({sql_text(f['id'])}, {p['slot']}, {sql_text(p['name'])}, {int(p['extra'])}) "
                "ON CONFLICT (family_id, slot) DO UPDATE SET name = excluded.name, "
                "is_extra = excluded.is_extra;"
            )
    return "\n".join(lines) + "\n"


def cmd_links(args):
    wb = open_workbook()
    rows, problems = read_guests(wb)
    if problems:
        raise ToolError("Fix these first:\n  " + "\n  ".join(problems))
    if not rows:
        raise ToolError("The Guests sheet has no households yet.")
    state = load_sidecar()
    fams = state["families"]
    site = clean(args.site_url) or setting(wb, "site_url") or DEFAULT_SITE
    if not site.startswith("https://") or not site.endswith("/"):
        raise ToolError("site_url must start with https:// and end with /")

    used_ids = {clean(r["id"]) for r in rows if clean(r["id"])}
    counter = 0
    taken_codes = {f["code"] for f in fams.values()}
    blockers, ready = [], []
    created = 0
    for rec in rows:
        fid = clean(rec["id"])
        if not fid:
            while True:
                counter += 1
                fid = f"g{counter:03d}"
                if fid not in used_ids and fid not in fams:
                    break
            used_ids.add(fid)
            rec["id"] = fid
        old = fams.get(fid)
        people, why = plan_people(
            old["people"] if old else None, rec["members"], rec["extra_seats"], args.force
        )
        if why:
            blockers.append(f"Guests row {rec['row']} ({fid}): {', '.join(why)}")
            continue
        if not old:
            created += 1
        code = old["code"] if old else new_code(taken_codes)
        taken_codes.add(code)
        ready.append(
            {
                "id": fid,
                "label": rec["label"],
                "lang": rec["lang"],
                "code": code,
                "people": people,
                "row": rec["row"],
            }
        )
    if blockers:
        raise ToolError(
            "These changes could mix up answers that already came in, so nothing was changed:\n  "
            + "\n  ".join(blockers)
            + "\nRestore the old members, or run again with --force if no answers exist yet."
        )

    backup(WORKBOOK)
    ws = wb["Guests"]
    for f in ready:
        put(ws, f["row"], 1, f["id"])
    links = wb["Links"]
    links.delete_rows(2, max(links.max_row, 2))
    for i, f in enumerate(ready, start=2):
        for col, v in enumerate([f["id"], f["label"], f["lang"], group(f["code"])], start=1):
            put(links, i, col, v)
        url = f"{site}?lang={urllib.parse.quote(f['lang'])}#{f['code']}"
        link_cell(links, i, 5, url, url)
    for f in ready:
        fams[f["id"]] = {"code": f["code"], "people": f["people"]}
    write_private(SIDECAR, json.dumps(state, indent=1, ensure_ascii=False))
    seed = build_seed([{**f, "hash": code_hash(f["code"])} for f in ready])
    write_private(OUTPUT / "seed.sql", seed)
    wb.save(WORKBOOK)
    print(
        f"{len(ready)} households ready ({created} new codes). "
        "Links sheet and output/seed.sql written."
    )


# ---- answers -------------------------------------------------------------------------------

QUERIES = {
    "family": "SELECT family_id, label, lang FROM family ORDER BY family_id",
    "person": "SELECT family_id, slot, name, is_extra FROM person ORDER BY family_id, slot",
    "answer": "SELECT family_id, slot, attending, extra_name, diet FROM answer",
    "response": "SELECT family_id, message, updated_at FROM response",
}


def rows_from_sqlite(path):
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    try:
        return {k: [dict(r) for r in con.execute(q)] for k, q in QUERIES.items()}
    finally:
        con.close()


def rows_from_wrangler(db_name, wrangler):
    """Reads the live database with the user's own wrangler login. No secret passes through here."""
    out = {}
    for key, query in QUERIES.items():
        cmd = [
            *wrangler.split(),
            "d1",
            "execute",
            db_name,
            "--remote",
            "--json",
            "--command",
            query,
        ]
        try:
            res = subprocess.run(
                cmd, cwd=ROOT / "worker", capture_output=True, text=True, timeout=120, check=False
            )
        except FileNotFoundError as e:
            raise ToolError(
                "wrangler was not found. See rsvp/README.md for the one-time setup."
            ) from e
        if res.returncode != 0:
            raise ToolError(
                "wrangler could not read the database. Are you logged in? (wrangler login)"
            )
        try:
            out[key] = json.loads(res.stdout)[0]["results"]
        except (ValueError, KeyError, IndexError) as e:
            raise ToolError("wrangler returned something unexpected.") from e
    return out


def summarise(data, phones, reminder):
    people_by = {}
    for p in data["person"]:
        people_by.setdefault(p["family_id"], []).append(p)
    ans = {(a["family_id"], a["slot"]): a for a in data["answer"]}
    resp = {r["family_id"]: r for r in data["response"]}
    out = {
        "answers": [],
        "pending": [],
        "messages": [],
        "diets": [],
        "totals": {
            "families": len(data["family"]),
            "answered": 0,
            "coming": 0,
            "not_coming": 0,
            "waiting": 0,
        },
    }
    for f in data["family"]:
        r = resp.get(f["family_id"])
        plist = people_by.get(f["family_id"], [])
        if not r:
            out["pending"].append(f)
            for p in plist:
                if not p["is_extra"]:
                    out["totals"]["waiting"] += 1
                    out["answers"].append([f["label"], p["name"], "waiting", "", ""])
            continue
        out["totals"]["answered"] += 1
        for p in plist:
            a = ans.get((f["family_id"], p["slot"]))
            attending = bool(a and a["attending"])
            if p["is_extra"] and not attending:
                continue
            name = a["extra_name"] if p["is_extra"] else p["name"]
            diet = a["diet"] if a else ""
            out["answers"].append(
                [f["label"], name, "coming" if attending else "not coming", diet, r["updated_at"]]
            )
            out["totals"]["coming" if attending else "not_coming"] += 1
            if attending and diet:
                out["diets"].append([f["label"], name, diet])
        if r["message"]:
            out["messages"].append([f["label"], r["message"], r["updated_at"]])
    return out


def clear_below_header(ws):
    ws.delete_rows(2, max(ws.max_row, 2))


def phone_digits(raw):
    return re.sub(r"\D", "", clean(raw))


def cmd_sync(args):
    wb = open_workbook()
    if bool(args.from_sqlite) == bool(args.wrangler_db):
        raise ToolError("Choose one source: --from-sqlite FILE or --wrangler-db NAME")
    data = (
        rows_from_sqlite(args.from_sqlite)
        if args.from_sqlite
        else rows_from_wrangler(args.wrangler_db, args.wrangler)
    )
    rows, _ = read_guests(wb)
    phones = {clean(r["id"]): phone_digits(r["phone"]) for r in rows}
    reminder = setting(wb, "reminder_text")
    s = summarise(data, phones, reminder)
    backup(WORKBOOK)

    for name in ("Answers", "Pending", "Messages", "Summary"):
        clear_below_header(wb[name])
    for i, row in enumerate(s["answers"], start=2):
        for c, v in enumerate(row, start=1):
            put(wb["Answers"], i, c, v)
    for i, f in enumerate(s["pending"], start=2):
        digits = phones.get(f["family_id"], "")
        put(wb["Pending"], i, 1, f["label"])
        put(wb["Pending"], i, 2, f["lang"])
        put(wb["Pending"], i, 3, digits)
        if digits:
            url = f"https://wa.me/{digits}"
            if reminder:
                url += "?text=" + urllib.parse.quote(reminder)
            link_cell(wb["Pending"], i, 4, "open in WhatsApp", url)
        else:
            put(wb["Pending"], i, 4, "no phone number")
    for i, row in enumerate(s["messages"], start=2):
        for c, v in enumerate(row, start=1):
            put(wb["Messages"], i, c, v)
    t = s["totals"]
    summary = [
        ("synced at", now_iso()),
        ("households answered", f"{t['answered']} of {t['families']}"),
        ("people coming", t["coming"]),
        ("people not coming", t["not_coming"]),
        ("people waiting", t["waiting"]),
        ("", ""),
        ("food needs and allergies (for the caterer)", ""),
        *[(f"{a} / {b}", c) for a, b, c in s["diets"]],
    ]
    for i, (k, v) in enumerate(summary, start=2):
        put(wb["Summary"], i, 1, k, bold=(k.startswith("food")))
        put(wb["Summary"], i, 2, v)
    wb.save(WORKBOOK)
    print(
        f"Synced: {t['answered']} of {t['families']} households answered, "
        f"{t['coming']} people coming, {t['not_coming']} not coming, {t['waiting']} waiting."
    )


# ---- entry ---------------------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("--force", action="store_true")
    p = sub.add_parser("links")
    p.add_argument("--site-url", default="")
    p.add_argument("--force", action="store_true", help="allow removing or reordering people")
    p = sub.add_parser("sync")
    p.add_argument("--from-sqlite", default="")
    p.add_argument("--wrangler-db", default="")
    p.add_argument("--wrangler", default=os.environ.get("WRANGLER", "wrangler"))
    args = ap.parse_args(argv)
    try:
        {"init": cmd_init, "links": cmd_links, "sync": cmd_sync}[args.cmd](args)
    except ToolError as e:
        print(str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
