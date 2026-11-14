"""List the model ids the local OmniRoute router offers (ids only, never the key).

Needs OMNIROUTE_API_KEY and OMNIROUTE_BASE_URL in the environment (start through ./start.sh).
Usage: .venv/bin/python -I scripts/router_models.py [word ...]   words filter the ids (default: all)
Owner: Tomas | review date: 2026-11-19 | rollback: rm scripts/router_models.py
"""

import json
import os
import sys
import urllib.request


def main() -> int:
    key = os.environ.get("OMNIROUTE_API_KEY")
    base = os.environ.get("OMNIROUTE_BASE_URL", "http://127.0.0.1:20128/v1").rstrip("/")
    if not key:
        print(
            "router_models: OMNIROUTE_API_KEY is not set; start through ./start.sh", file=sys.stderr
        )
        return 2
    if not base.startswith("http://127.0.0.1:"):
        print("router_models: only the local router is allowed", file=sys.stderr)
        return 2
    req = urllib.request.Request(base + "/models", headers={"Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=15) as r:  # noqa: S310 (fixed local http address)
        data = json.load(r)
    words = [w.lower() for w in sys.argv[1:]]
    for m in data.get("data", []):
        mid = str(m.get("id", ""))
        if not words or any(w in mid.lower() for w in words):
            print(mid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
