# shellcheck shell=bash
# Sourced by start.sh and doctor.sh. Puts every project tool on PATH and loads the local libs.
# owner: Tomas | canonical path: projects/wedding-invite/scripts/env.sh | review date: 2026-11-09
# rollback: rm -f projects/wedding-invite/scripts/env.sh (then restore the PATH line in start.sh and doctor.sh)
PROJ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$HOME/.local/opt/node-v24.22.1-linux-x64/bin:$HOME/.local/bin:$PROJ/.venv/bin:$PATH"
# Chromium needs libnss3 and libnspr4; no sudo here, so they are unpacked inside the project.
export LD_LIBRARY_PATH="$PROJ/.local-libs/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
_chromes=("$HOME"/.cache/ms-playwright/chromium-*/chrome-linux*/chrome)
if [[ -x ${_chromes[${#_chromes[@]} - 1]} ]]; then export CHROME_PATH="${_chromes[${#_chromes[@]} - 1]}"; fi
unset _chromes
