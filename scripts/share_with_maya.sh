#!/usr/bin/env bash
# Copy the whole wedding-invite project (everything except rebuildable tools) into the shared repo and push it.
# owner: Tomas | review date: 2026-11-21 | rollback: rm scripts/share_with_maya.sh
# Usage: scripts/share_with_maya.sh "what changed"   (the repo is ~/convite-collab, private, shared with Maya)
set -euo pipefail
SRC="$(cd "$(dirname "$0")/.." && pwd)"
DST="${SHARE_DIR:-$HOME/convite-collab}"
MSG="${1:-Update from Tomas}"
[[ -d $DST/.git ]] || { echo "no git repo at $DST" >&2; exit 1; }
rsync -a --delete \
  --exclude='.git/' --exclude='.venv/' --exclude='.tools/' --exclude='node_modules/' --exclude='__pycache__/' \
  --exclude='*.zip' --exclude='*Zone.Identifier*' --exclude='.DS_Store' \
  --exclude='/START-HERE.md' --exclude='/.gitignore' --exclude='/claude-context/' \
  "$SRC/" "$DST/"
cd "$DST"
git add -A
if git diff --cached --quiet; then echo "nothing new to share"; exit 0; fi
git -c user.name="$(git -C "$SRC" config user.name)" -c user.email="$(git -C "$SRC" config user.email)" commit -q -m "$MSG"
git push -q origin main
echo "shared: $(git log --oneline | head -1)"
