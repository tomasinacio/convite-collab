---
name: copilot-image
description: "Use when the invitation needs an image made in the Microsoft Copilot app on the user's Windows PC: drives the app through the desk CLI (PC MCP), submits the prompt, saves the result into assets/inbox, logs it, and falls back to free routes when credits run out. Not for text work or for any sign-in, purchase or upgrade prompt."
---
<!-- owner: Tomas | canonical path: projects/wedding-invite/.claude/skills/copilot-image/SKILL.md | review date: 2026-11-09 -->
<!-- rollback: rm -rf projects/wedding-invite/.claude/skills/copilot-image -->

# Copilot image generation through `desk`

The user approved this in chat on 2026-11-09: use the Copilot app on their PC to write prompts, generate pictures, and download and manage them for the invitation. That approval covers pressing Enter on an invitation-art prompt and saving results. It does not cover sign-in, upgrade, purchase, credits top-up or any other dialog.

Status on 2026-11-09: **untested end to end.** `desk` returned `Unauthorized` from the agent shell because its key is read from an environment variable the shell did not have. Run `./start.sh` so the session has it, then `scripts/doctor.sh`.

## Steps
1. `scripts/doctor.sh`. Continue only if the `desk` line says PASS. If it says `Unauthorized`, tell the user to restart through `./start.sh`; do not look for key files.
2. `desk windows`, then `desk app launch "Copilot"` or `desk app switch "Copilot"`. Run `desk see --grep "Copilot"` and confirm the focused window is the Copilot app.
3. Open a new chat in the app. Put the prompt text on the clipboard with `desk clip set "<prompt>"` (full prompt = `assets/STYLE.md` + the asset description) and paste with `desk key ctrl+v`. Check the field with `desk see --grep "Message"`.
4. Submit with `desk key enter`. Wait: `desk waitfor --text "<text shown when done>" --timeout 120`; if no text is known, `desk shot assets/inbox/_wait.png` every 20 s and look.
5. Find the save control: `desk see --grep "Download"`, then `--grep "Save"`. Click it by coordinate from the latest `see`. If a Save As dialog opens, type a file name under `C:\Users\tomin\Downloads\` and confirm.
6. Copy the file into the project: `cp /mnt/c/Users/tomin/Downloads/<file> assets/inbox/<asset-name>.png`. Add a line to `assets/LOG.md` (tool `Copilot app`, date, prompt, license terms shown in the app).
7. Judge the image with Opus 5.5 high against `assets/STYLE.md` and the look rules. Regenerate with a changed prompt if it fails; never patch in code.

## When Copilot stops
Signs: a message about limits, boosts, or credits; a disabled prompt box. Stop driving the app. Do not click upgrade or buy. Use `scripts/free_image.py` (Pollinations needs no key) and say so to the user.

## Safety (from `desktop-control`)
- `desk` refuses credential and UAC dialogs (exit 2). Treat exit 2 as a wall.
- If the user moves the mouse, stop. One agent drives the desktop at a time.
- Re-run `desk see` after every action; coordinates go stale.
- Never type or copy credentials, tokens or cookies.
