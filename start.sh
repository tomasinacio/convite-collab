#!/usr/bin/env bash
# Launch Claude Code in the wedding-invite workspace with every tool reachable.
# owner: Tomas | canonical path: projects/wedding-invite/start.sh | review date: 2026-11-09
# rollback: rm -f projects/wedding-invite/start.sh
#
# Usage: ./start.sh            start with the desk (PC MCP) key loaded, so Copilot can be driven
#        ./start.sh --no-desk  start without it
#        ./start.sh --no-router  start without the OmniRoute key (see below)
# The desk key is read from the Windows file into this process's environment only; it is never
# printed or written anywhere. It rotates daily, so start through this script each day.
set -euo pipefail
cd "$(dirname "$0")"

# shellcheck disable=SC1091
source scripts/env.sh

use_desk=1
skip_router=0
args=()
for a in "$@"; do
  if [[ $a == --no-desk ]]; then
    use_desk=0
  elif [[ $a == --no-router ]]; then
    skip_router=1
  else
    args+=("$a")
  fi
done

KEY_FILE=/mnt/c/Users/tomin/.windows-mcp/auth.key
if [[ $use_desk == 1 && -r $KEY_FILE ]]; then
  DESK_MCP_AUTH_KEY="$(tr -d '\r\n' < "$KEY_FILE")"
  export DESK_MCP_AUTH_KEY
  echo "desk key loaded for this session (not shown)"
elif [[ $use_desk == 1 ]]; then
  echo "desk key file not readable: Copilot driving will not work this session" >&2
fi

# The OmniRoute router key (the one `delegate/` uses) goes into this process's environment only, as
# OMNIROUTE_API_KEY, so scripts/free_image.py can use the router's image models. Never printed.
# Loaded on 2026-11-12 at the user's request (picker answer). Skip with --no-router.
ROUTER_ENV="$HOME/.config/agent-secrets/delegate.env"
if [[ $skip_router == 0 && -r $ROUTER_ENV ]]; then
  OMNIROUTE_API_KEY="$(sed -n 's/^DELEGATE_ROUTER_KEY=//p' "$ROUTER_ENV" | head -1 | tr -d '\r\n')"
  if [[ -n $OMNIROUTE_API_KEY ]]; then
    export OMNIROUTE_API_KEY
    export OMNIROUTE_BASE_URL="${OMNIROUTE_BASE_URL:-http://127.0.0.1:20128/v1}"
    echo "router key loaded for this session (not shown)"
  else
    echo "router key not found in delegate.env: router images will not work this session" >&2
  fi
fi

bash scripts/doctor.sh || true
exec claude "${args[@]}"
