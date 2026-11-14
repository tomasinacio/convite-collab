-- RSVP schema for SQLite and Cloudflare D1.
-- Names are snake_case. Timestamps are UTC RFC 3339 with milliseconds.
-- family and person come from the guest list (tools/make_links.py writes the
-- seed). answer, response and response_history come from the guests and are
-- never touched by a reseed.

CREATE TABLE IF NOT EXISTS family (
    family_id TEXT NOT NULL PRIMARY KEY,
    code_hash TEXT NOT NULL UNIQUE
    CHECK (length(code_hash) = 64),
    label TEXT NOT NULL,
    lang TEXT NOT NULL DEFAULT 'pt-PT'
    CHECK (lang IN ('pt-PT', 'en', 'es'))
) STRICT;

CREATE TABLE IF NOT EXISTS person (
    family_id TEXT NOT NULL REFERENCES family (family_id),
    slot INTEGER NOT NULL,
    name TEXT NOT NULL,
    is_extra INTEGER NOT NULL DEFAULT 0
    CHECK (is_extra IN (0, 1)),
    PRIMARY KEY (family_id, slot)
) STRICT;

CREATE TABLE IF NOT EXISTS answer (
    family_id TEXT NOT NULL,
    slot INTEGER NOT NULL,
    attending INTEGER NOT NULL
    CHECK (attending IN (0, 1)),
    extra_name TEXT NOT NULL DEFAULT '',
    diet TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (family_id, slot),
    FOREIGN KEY (family_id, slot) REFERENCES person (family_id, slot)
) STRICT;

CREATE TABLE IF NOT EXISTS response (
    family_id TEXT NOT NULL PRIMARY KEY REFERENCES family (family_id),
    message TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
    CHECK (created_at GLOB '????-??-??T??:??:??.???Z'),
    updated_at TEXT NOT NULL
    CHECK (updated_at GLOB '????-??-??T??:??:??.???Z'),
    revision INTEGER NOT NULL
    CHECK (revision >= 1),
    last_write TEXT NOT NULL DEFAULT ''
) STRICT;

CREATE TABLE IF NOT EXISTS response_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    family_id TEXT NOT NULL REFERENCES family (family_id),
    at TEXT NOT NULL
    CHECK (at GLOB '????-??-??T??:??:??.???Z'),
    revision INTEGER NOT NULL
    CHECK (revision >= 1),
    payload TEXT NOT NULL
    CHECK (json_valid(payload))
) STRICT;

CREATE INDEX IF NOT EXISTS response_history_family
ON response_history (family_id);

CREATE TABLE IF NOT EXISTS throttle (
    bucket TEXT NOT NULL PRIMARY KEY,
    window_start TEXT NOT NULL
    CHECK (window_start GLOB '????-??-??T??:??:??.???Z'),
    n INTEGER NOT NULL
) STRICT;

CREATE INDEX IF NOT EXISTS throttle_window
ON throttle (window_start);

CREATE TABLE IF NOT EXISTS setting (
    name TEXT NOT NULL PRIMARY KEY,
    value TEXT NOT NULL
) STRICT;
