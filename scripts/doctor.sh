#!/usr/bin/env bash
# Health check for every tool in the wedding-invite workspace.
# owner: Tomas | canonical path: projects/wedding-invite/scripts/doctor.sh | review date: 2026-11-09
# rollback: rm -f projects/wedding-invite/scripts/doctor.sh
#
# Prints PASS, WARN or FAIL per line with the fix. Exit 1 only if a FAIL exists.
# Reads no key files. Touches nothing outside /tmp.
cd "$(dirname "$0")/.." || exit 2
# shellcheck disable=SC1091
source scripts/env.sh
fails=0

row() {
  printf '%-5s %-26s %s\n' "$1" "$2" "$3"
  if [[ $1 == FAIL ]]; then fails=$((fails + 1)); fi
}

# check LEVEL NAME OK-MESSAGE BAD-MESSAGE -- COMMAND...   (LEVEL is FAIL or WARN when the command fails)
check() {
  local level=$1 name=$2 ok=$3 bad=$4
  shift 5
  if "$@" >/dev/null 2>&1; then row PASS "$name" "$ok"; else row "$level" "$name" "$bad"; fi
}

# skills resolve
bad=0
n=0
for l in .claude/skills/*; do
  n=$((n + 1))
  if [[ ! -f $l/SKILL.md ]]; then
    bad=$((bad + 1))
    echo "      broken: $l"
  fi
done
if [[ $bad == 0 ]]; then row PASS "skills ($n)" "all .claude/skills resolve"; else row FAIL "skills" "$bad broken link(s)"; fi

# vendored rules and the Taste pin
rules=vendor/web-design-guidelines/command.md
check FAIL "vercel rules" "$rules" "file missing" -- test -s "$rules"
T=$HOME/.local/share/design-skills/taste-skill
if [[ -d $T/.git ]]; then
  sha=$(git -C "$T" rev-parse HEAD 2>/dev/null)
  if [[ $sha == f6b76575f949707b4e3c37cd86cb44b0b98643e8 ]]; then
    row PASS "taste skill" "pinned f6b7657"
  else
    row WARN "taste skill" "unexpected commit $sha"
  fi
else
  row FAIL "taste skill" "clone missing: see vendor/SOURCES.md"
fi

# runtimes
check FAIL "node" "$(node -v 2>/dev/null) (taste needs 22+)" "not on PATH" -- node -v
if [[ -x .venv/bin/python ]]; then
  miss=""
  for m in gradio_client rembg PIL cv2; do
    .venv/bin/python -c "import $m" 2>/dev/null || miss="$miss $m"
  done
  if [[ -z $miss ]]; then
    row PASS "python venv" "gradio_client rembg PIL cv2 import"
  else
    row FAIL "python venv" "missing:$miss -> .venv/bin/pip install gradio_client 'rembg[cpu]' pillow opencv-python-headless"
  fi
else
  row FAIL "python venv" "no .venv -> python3 -m venv .venv"
fi

# browser tooling
check FAIL "playwright-cli" "$(command -v playwright-cli)" "npm install -g @playwright/cli@latest" -- command -v playwright-cli
if [[ -n ${CHROME_PATH:-} && -x $CHROME_PATH ]]; then
  if ldd "$CHROME_PATH" 2>/dev/null | grep -q "not found"; then
    row FAIL "chromium" "missing libs: unpack libnss3 and libnspr4 into .local-libs (see README)"
  else
    row PASS "chromium" "$CHROME_PATH"
  fi
else
  row FAIL "chromium" "not installed: node \$(npm prefix -g)/lib/node_modules/@playwright/cli/node_modules/playwright-core/cli.js install chromium"
fi

# desk (PC MCP, drives the Copilot app)
desk_bin=$HOME/.local/bin/desk
if [[ -x $desk_bin ]]; then
  out=$(timeout 25 "$desk_bin" status 2>&1 | head -3 | tr '\n' ' ')
  case $out in
    *Unauthorized*) row WARN "desk (Copilot control)" "Unauthorized: start with ./start.sh so the key is loaded" ;;
    *"cannot reach"*) row WARN "desk (Copilot control)" "server down: run start-desktop-mcp.ps1 on Windows" ;;
    "") row WARN "desk (Copilot control)" "no output" ;;
    *) row PASS "desk (Copilot control)" "${out:0:70}" ;;
  esac
else
  row WARN "desk" "CLI not found at $desk_bin"
fi

# free image routes
code=$(curl -s -o /dev/null -m 20 -w '%{http_code}' -I https://image.pollinations.ai/ 2>/dev/null)
if [[ $code =~ ^[234] ]]; then
  row PASS "pollinations (free)" "reachable (http $code); rate limited, mark in corner"
else
  row WARN "pollinations (free)" "unreachable"
fi
for pair in "CF_API_TOKEN:cloudflare" "HF_TOKEN:hf" "GEMINI_API_KEY:gemini" "OPENROUTER_API_KEY:openrouter" "OMNIROUTE_API_KEY:omniroute"; do
  v=${pair%%:*}
  r=${pair##*:}
  if [[ -n ${!v:-} ]]; then row PASS "route $r" "env set"; else row WARN "route $r" "env $v not set (optional)"; fi
done

# image quality gate must still reject bad images
check FAIL "quality gate selftest" "rejects bad images, accepts the real scan" "run scripts/image_quality.py --selftest" -- .venv/bin/python scripts/image_quality.py --selftest

# palette contrast
check FAIL "palette contrast" "all text pairs >= 4.5:1" "run scripts/contrast.py" -- .venv/bin/python scripts/contrast.py

echo
if [[ $fails == 0 ]]; then echo "doctor: no FAIL"; else echo "doctor: $fails FAIL"; fi
[[ $fails == 0 ]]
