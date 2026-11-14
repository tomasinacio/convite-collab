"""Tests for rsvp_workbook.py. Run from projects/wedding-invite:

    .venv/bin/python -I -m unittest discover -s rsvp/tools -p "test_*.py"

All guest names, phone numbers and codes here are made up for the tests.
"""

import contextlib
import io
import json
import os
import re
import shutil
import sqlite3
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rsvp_workbook as w  # noqa: E402
from openpyxl import load_workbook  # noqa: E402

MIGRATION = Path(__file__).resolve().parent.parent / "worker" / "migrations" / "0001-initial.sql"
PROBE = Path(__file__).resolve().parent.parent / "worker" / "tools" / "e2e_probe.mjs"
ALPHABET_RE = re.compile(r"^[0-9A-HJKMNP-TV-Z]{16}$")


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = w.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.saved = (w.GUESTS, w.OUTPUT, w.WORKBOOK, w.SIDECAR)
        w.GUESTS = self.tmp / "guests"
        w.OUTPUT = self.tmp / "output"
        w.WORKBOOK = w.GUESTS / "convite-rsvp.xlsx"
        w.SIDECAR = w.GUESTS / "codes.json"
        self.assertEqual(run("init")[0], 0)

    def tearDown(self):
        w.GUESTS, w.OUTPUT, w.WORKBOOK, w.SIDECAR = self.saved
        shutil.rmtree(self.tmp, ignore_errors=True)

    def fill(self, rows):
        wb = load_workbook(w.WORKBOOK)
        ws = wb["Guests"]
        ws.delete_rows(2, ws.max_row)
        for i, r in enumerate(rows, start=2):
            for c, v in enumerate(r, start=1):
                ws.cell(row=i, column=c).value = v
        wb.save(w.WORKBOOK)

    def sidecar(self):
        return json.loads(w.SIDECAR.read_text(encoding="utf-8"))

    def seeded_db(self):
        con = sqlite3.connect(":memory:")
        con.execute("PRAGMA foreign_keys = ON")
        con.executescript(MIGRATION.read_text())
        con.executescript((w.OUTPUT / "seed.sql").read_text())
        return con


ROWS = [
    ["", "Test Family A", "en", "Alice Test; Bob Test", 1, "+351 912 345 678", "note A"],
    ["", "Test Family B", "es", "Carla Probe", 0, "", ""],
]


class TemplateTests(Base):
    def test_template_sheets_and_headers(self):
        wb = load_workbook(w.WORKBOOK)
        self.assertEqual(wb.sheetnames, w.SHEETS)
        self.assertEqual([c.value for c in wb["Guests"][1]], w.GUEST_HEADERS)
        self.assertEqual(wb["Guests"].max_row, 400)  # only formatting beyond the header
        self.assertTrue(all(c.value is None for r in wb["Guests"].iter_rows(min_row=2) for c in r))

    def test_no_invented_guests(self):
        wb = load_workbook(w.WORKBOOK)
        text = " ".join(str(c.value) for ws in wb for r in ws.iter_rows() for c in r if c.value)
        self.assertNotIn("Maya", text)
        self.assertNotIn("Tom", text)

    def test_init_does_not_overwrite(self):
        self.fill(ROWS)
        code, _, err = run("init")
        self.assertEqual(code, 1)
        self.assertIn("already exists", err)
        self.assertEqual(load_workbook(w.WORKBOOK)["Guests"]["B2"].value, "Test Family A")

    def test_workbook_is_private(self):
        self.assertEqual(stat.S_IMODE(os.stat(w.WORKBOOK).st_mode), 0o600)


class LinkTests(Base):
    def test_links_codes_seed_and_privacy(self):
        self.fill(ROWS)
        code, out, _ = run("links")
        self.assertEqual(code, 0, out)
        fams = self.sidecar()["families"]
        self.assertEqual(sorted(fams), ["g001", "g002"])
        codes = [f["code"] for f in fams.values()]
        self.assertEqual(len(set(codes)), 2)
        for c in codes:
            self.assertRegex(c, ALPHABET_RE)
            self.assertNotIn(c, out)  # the tool never prints a code
        for name in ("Alice", "Test Family"):
            self.assertNotIn(name, out)
        seed = (w.OUTPUT / "seed.sql").read_text()
        for c in codes:
            self.assertNotIn(c, seed)  # only hashes are in the seed
        for private in ("912", "note A"):
            self.assertNotIn(private, seed)
        self.assertEqual(stat.S_IMODE(os.stat(w.SIDECAR).st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(os.stat(w.OUTPUT / "seed.sql").st_mode), 0o600)

    def test_links_sheet_has_real_hyperlinks(self):
        self.fill(ROWS)
        run("links")
        ws = load_workbook(w.WORKBOOK)["Links"]
        code = self.sidecar()["families"]["g001"]["code"]
        cell = ws["E2"]
        self.assertEqual(cell.hyperlink.target, f"{w.DEFAULT_SITE}?lang=en#{code}")
        self.assertEqual(ws["C3"].value, "es")
        self.assertIn("-", ws["D2"].value)  # grouped for typing
        self.assertNotEqual(cell.data_type, "f")

    def test_ids_fill_in_and_codes_are_stable(self):
        self.fill(ROWS)
        run("links")
        first = self.sidecar()["families"]
        self.assertEqual(load_workbook(w.WORKBOOK)["Guests"]["A2"].value, "g001")
        run("links")
        self.assertEqual(self.sidecar()["families"], first)

    def test_reordering_rows_keeps_each_households_code(self):
        self.fill(ROWS)
        run("links")
        first = self.sidecar()["families"]
        wb = load_workbook(w.WORKBOOK)
        ws = wb["Guests"]
        a = [ws.cell(row=2, column=c).value for c in range(1, 8)]
        b = [ws.cell(row=3, column=c).value for c in range(1, 8)]
        for c in range(1, 8):
            ws.cell(row=2, column=c).value = b[c - 1]
            ws.cell(row=3, column=c).value = a[c - 1]
        wb.save(w.WORKBOOK)
        self.assertEqual(run("links")[0], 0)
        self.assertEqual(self.sidecar()["families"], first)

    def test_bad_rows_are_explained_and_nothing_is_written(self):
        self.fill([["", "X", "fr", "", 9, "", ""], ["", "X", "en", "Someone", 0, "", ""]])
        code, _, err = run("links")
        self.assertEqual(code, 1)
        for text in ("lang must be", "members is empty", "extra_seats", "used twice"):
            self.assertIn(text, err)
        self.assertFalse(w.SIDECAR.exists())
        self.assertFalse((w.OUTPUT / "seed.sql").exists())

    def test_removing_or_reordering_people_is_refused(self):
        self.fill(ROWS)
        run("links")
        for members, extra, why in [
            ("Alice Test", 1, "removed"),
            ("Bob Test; Alice Test", 1, "reordered"),
            ("Alice Test; Bob Test", 0, "extra seats were reduced"),
        ]:
            with self.subTest(why):
                rows = [list(r) for r in ROWS]
                rows[0][0], rows[0][3], rows[0][4] = "g001", members, extra
                rows[1][0] = "g002"
                self.fill(rows)
                code, _, err = run("links")
                self.assertEqual(code, 1)
                self.assertIn(why, err)
        self.assertEqual(self.sidecar()["families"]["g001"]["people"][0]["name"], "Alice Test")

    def test_force_allows_the_change(self):
        self.fill(ROWS)
        run("links")
        rows = [list(r) for r in ROWS]
        rows[0][0], rows[0][3], rows[1][0] = "g001", "Alice Test", "g002"
        self.fill(rows)
        self.assertEqual(run("links", "--force")[0], 0)

    def test_adding_people_keeps_existing_slots(self):
        self.fill(ROWS)
        run("links")
        before = self.sidecar()["families"]["g001"]["people"]
        rows = [list(r) for r in ROWS]
        rows[0][0], rows[0][3], rows[0][4], rows[1][0] = (
            "g001",
            "Alice Test; Bob Test; Cleo Test",
            2,
            "g002",
        )
        self.fill(rows)
        self.assertEqual(run("links")[0], 0)
        after = self.sidecar()["families"]["g001"]["people"]
        by_slot = {p["slot"]: p for p in after}
        for p in before:
            self.assertEqual(by_slot[p["slot"]]["extra"], p["extra"])
        self.assertEqual(len(after), 5)
        self.assertEqual(len({p["slot"] for p in after}), 5)
        cleo = next(p for p in after if p["name"] == "Cleo Test")
        self.assertNotIn(cleo["slot"], {p["slot"] for p in before})

    def test_a_spelling_fix_keeps_the_slot(self):
        self.fill(ROWS)
        run("links")
        slot = self.sidecar()["families"]["g002"]["people"][0]["slot"]
        rows = [list(r) for r in ROWS]
        rows[0][0], rows[1][0], rows[1][3] = "g001", "g002", "Carla Probe-Fixed"
        self.fill(rows)
        self.assertEqual(run("links")[0], 0)
        person = self.sidecar()["families"]["g002"]["people"][0]
        self.assertEqual((person["slot"], person["name"]), (slot, "Carla Probe-Fixed"))

    def test_formulas_in_guest_text_stay_text(self):
        evil = '=HYPERLINK("http://x.test","a")'
        self.fill([["", evil, "en", "=1+1; +cmd", 0, "", "@x"]])
        self.assertEqual(run("links")[0], 0)
        ws = load_workbook(w.WORKBOOK)["Links"]
        self.assertEqual(ws["B2"].data_type, "s")
        self.assertEqual(ws["B2"].value, evil)
        con = self.seeded_db()
        self.assertEqual(con.execute("SELECT label FROM family").fetchone()[0], evil)
        names = [r[0] for r in con.execute("SELECT name FROM person ORDER BY slot")]
        self.assertEqual(names, ["=1+1", "+cmd"])

    def test_quotes_in_names_cannot_break_the_seed(self):
        self.fill([["", "O'Brien'); DROP TABLE family;--", "en", "D'Arcy; Zoë Ünal", 0, "", ""]])
        self.assertEqual(run("links")[0], 0)
        con = self.seeded_db()
        self.assertEqual(con.execute("SELECT COUNT(*) FROM family").fetchone()[0], 1)
        self.assertIn("Zoë Ünal", [r[0] for r in con.execute("SELECT name FROM person")])

    def test_seed_is_safe_to_run_twice_and_never_touches_answers(self):
        self.fill(ROWS)
        run("links")
        con = self.seeded_db()
        con.execute(
            "INSERT INTO answer (family_id, slot, attending, diet) VALUES ('g001', 1, 1, 'x')"
        )
        con.executescript((w.OUTPUT / "seed.sql").read_text())
        self.assertEqual(con.execute("SELECT COUNT(*) FROM family").fetchone()[0], 2)
        self.assertEqual(con.execute("SELECT diet FROM answer").fetchone()[0], "x")

    def test_extra_seats_become_unnamed_extra_people(self):
        self.fill(ROWS)
        run("links")
        rows = (
            self.seeded_db()
            .execute(
                "SELECT slot, name, is_extra FROM person WHERE family_id = 'g001' ORDER BY slot"
            )
            .fetchall()
        )
        self.assertEqual(rows, [(1, "Alice Test", 0), (2, "Bob Test", 0), (3, "", 1)])

    def test_the_worker_accepts_a_code_this_tool_made(self):
        """Cross-language check: Python's hash must match what the Worker computes."""
        node = shutil.which("node")
        if not node:
            self.skipTest("node not found")
        self.fill(ROWS)
        run("links")
        code = self.sidecar()["families"]["g001"]["code"]
        typed = code[:4].lower() + "-" + code[4:8] + " " + code[8:]
        for given, expect in [(code, "200 Test Family A 3"), (typed, "200 Test Family A 3")]:
            res = subprocess.run(
                [node, str(PROBE), str(w.OUTPUT / "seed.sql"), given],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            self.assertEqual(res.stdout.strip(), expect, res.stderr)
        res = subprocess.run(
            [node, str(PROBE), str(w.OUTPUT / "seed.sql"), "ZZZZZZZZZZZZZZZZ"],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(res.stdout.strip(), "404 not_found 0")

    def test_site_url_must_be_https_with_a_trailing_slash(self):
        self.fill(ROWS)
        code, _, err = run("links", "--site-url", "http://example.test")
        self.assertEqual(code, 1)
        self.assertIn("site_url", err)


class SyncTests(Base):
    def build_source(self):
        self.fill(ROWS)
        run("links")
        con = self.seeded_db()
        con.execute(
            "INSERT INTO response"
            " (family_id, message, created_at, updated_at, revision, last_write)"
            " VALUES ('g001', '=cmd|x', '2027-01-02T10:00:00.000Z',"
            " '2027-01-02T10:00:00.000Z', 1, 'w')"
        )
        con.executemany(
            "INSERT INTO answer (family_id, slot, attending, extra_name, diet)"
            " VALUES (?, ?, ?, ?, ?)",
            [
                ("g001", 1, 1, "", "=HYPERLINK(1)"),
                ("g001", 2, 0, "", ""),
                ("g001", 3, 1, "Plus One", ""),
            ],
        )
        con.commit()
        path = self.tmp / "source.sqlite"
        disk = sqlite3.connect(path)
        con.backup(disk)
        disk.close()
        return path

    def test_sync_fills_answers_pending_messages_summary(self):
        src = self.build_source()
        wb = load_workbook(w.WORKBOOK)
        wb["Settings"]["B2"].value = "Olá & hello"
        wb["Guests"]["F3"].value = "+351 (91) 111-2222"
        wb.save(w.WORKBOOK)
        guests_before = [
            [c.value for c in r] for r in load_workbook(w.WORKBOOK)["Guests"].iter_rows()
        ]
        links_before = [
            [c.value for c in r] for r in load_workbook(w.WORKBOOK)["Links"].iter_rows()
        ]
        code, out, _ = run("sync", "--from-sqlite", str(src))
        self.assertEqual(code, 0, out)
        wb = load_workbook(w.WORKBOOK)
        ans = [[c.value for c in r] for r in wb["Answers"].iter_rows(min_row=2)]
        self.assertEqual(
            [[x or "" for x in a[:4]] for a in ans],
            [
                ["Test Family A", "Alice Test", "coming", "=HYPERLINK(1)"],
                ["Test Family A", "Bob Test", "not coming", ""],
                ["Test Family A", "Plus One", "coming", ""],
                ["Test Family B", "Carla Probe", "waiting", ""],
            ],
        )
        self.assertEqual(wb["Answers"]["D2"].data_type, "s")  # text, never a formula
        pend = [[c.value for c in r] for r in wb["Pending"].iter_rows(min_row=2)]
        self.assertEqual(pend[0][:3], ["Test Family B", "es", "351911112222"])
        self.assertEqual(
            wb["Pending"]["D2"].hyperlink.target,
            "https://wa.me/351911112222?text=Ol%C3%A1%20%26%20hello",
        )
        self.assertEqual(wb["Messages"]["B2"].value, "=cmd|x")
        self.assertEqual(wb["Messages"]["B2"].data_type, "s")
        summary = {r[0].value: r[1].value for r in wb["Summary"].iter_rows(min_row=2) if r[0].value}
        self.assertEqual(summary["people coming"], 2)
        self.assertEqual(summary["people not coming"], 1)
        self.assertEqual(summary["people waiting"], 1)
        self.assertEqual(summary["households answered"], "1 of 2")
        self.assertEqual(
            [[c.value for c in r] for r in wb["Guests"].iter_rows()], guests_before
        )  # the guest list is never touched
        self.assertEqual([[c.value for c in r] for r in wb["Links"].iter_rows()], links_before)
        self.assertTrue(list((w.GUESTS / "backups").glob("*.xlsx")))
        for private in ("Alice", "351", "Olá"):
            self.assertNotIn(private, out)

    def test_sync_twice_gives_the_same_sheets(self):
        src = self.build_source()
        run("sync", "--from-sqlite", str(src))
        first = [[c.value for c in r] for r in load_workbook(w.WORKBOOK)["Answers"].iter_rows()]
        run("sync", "--from-sqlite", str(src))
        second = [[c.value for c in r] for r in load_workbook(w.WORKBOOK)["Answers"].iter_rows()]
        self.assertEqual(first, second)

    def test_pending_without_a_phone_says_so(self):
        src = self.build_source()
        run("sync", "--from-sqlite", str(src))
        ws = load_workbook(w.WORKBOOK)["Pending"]
        self.assertEqual(ws["D2"].value, "no phone number")
        self.assertIsNone(ws["D2"].hyperlink)

    def test_choose_exactly_one_source(self):
        self.build_source()
        self.assertEqual(run("sync")[0], 1)
        self.assertEqual(run("sync", "--from-sqlite", "a", "--wrangler-db", "b")[0], 1)

    def test_wrangler_source_parses_its_output(self):
        src = self.build_source()
        fake = self.tmp / "fake_wrangler.py"
        fake.write_text(
            "import json, os, sqlite3, sys\n"
            "q = sys.argv[sys.argv.index('--command') + 1]\n"
            "assert sys.argv[1:3] == ['d1', 'execute'] and '--remote' in sys.argv\n"
            "con = sqlite3.connect(os.environ['FAKE_DB']); con.row_factory = sqlite3.Row\n"
            "print(json.dumps([{'results': [dict(r) for r in con.execute(q)], 'success': True}]))\n"
        )
        os.environ["FAKE_DB"] = str(src)
        try:
            code, out, err = run(
                "sync", "--wrangler-db", "rsvp", "--wrangler", f"{sys.executable} {fake}"
            )
        finally:
            del os.environ["FAKE_DB"]
        self.assertEqual(code, 0, err)
        self.assertIn("1 of 2 households answered", out)

    def test_wrangler_missing_or_failing_gives_a_plain_message(self):
        self.build_source()
        code, _, err = run("sync", "--wrangler-db", "rsvp", "--wrangler", "no-such-tool-xyz")
        self.assertEqual(code, 1)
        self.assertIn("wrangler was not found", err)
        code, _, err = run("sync", "--wrangler-db", "rsvp", "--wrangler", "false")
        self.assertEqual(code, 1)
        self.assertIn("logged in", err)
        self.assertNotIn("Traceback", err)


class HelperTests(unittest.TestCase):
    def test_code_helpers(self):
        self.assertEqual(w.normalise_code(" abcd-efgh-jkmn-pqrs "), "ABCDEFGHJKMNPQRS")
        self.assertEqual(w.normalise_code("o1l"), "011")
        self.assertEqual(len(w.new_code(set())), 16)
        self.assertEqual(w.group("ABCDEFGHJKMNPQRS"), "ABCD-EFGH-JKMN-PQRS")
        self.assertEqual(len(w.code_hash("ABCDEFGHJKMNPQRS")), 64)

    def test_clean_removes_invisible_characters(self):
        self.assertEqual(w.clean(" a​b‮c\x00 "), "abc")
        self.assertEqual(w.clean(None), "")

    def test_sql_text_escapes_quotes(self):
        self.assertEqual(w.sql_text("O'Brien"), "'O''Brien'")


if __name__ == "__main__":
    unittest.main()
