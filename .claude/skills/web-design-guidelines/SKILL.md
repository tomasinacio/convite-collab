---
name: web-design-guidelines
description: "Use when reviewing invitation or page code against the Vercel Web Interface Guidelines: accessibility, focus states, forms, animation and reduced motion, touch, typography, images, performance, i18n. Reads a pinned local copy of the rules; never fetches them from the internet. Not for creating designs."
---
<!-- owner: Tomas | canonical path: projects/wedding-invite/.claude/skills/web-design-guidelines/SKILL.md | review date: 2026-11-09 -->
<!-- rollback: rm -rf projects/wedding-invite/.claude/skills/web-design-guidelines -->

# Web Interface Guidelines review (local pinned rules)

This replaces Vercel's upstream skill of the same name. Upstream fetches its rules from a URL at every review; that makes a remote file part of the instructions. Here the rules are a reviewed local file.

## Steps
1. Read `~/agent-config/projects/wedding-invite/vendor/web-design-guidelines/command.md` (191 lines, pinned 2026-11-09). Do not fetch anything.
2. Read the files named by the user, or ask which files if none were named.
3. Check every rule in that file against those files.
4. Output findings as `file:line  rule  fix`, one per line, most severe first. Group by the file's own headings. Say `no findings` only after all headings were checked.
5. Stop. Do not edit code unless the user asks.

For this project also check, in addition to the file's rules: the `Skip` control is the first focusable element; the tap target is a `<button>`; every language variant sets `lang`; reduced motion shows the fallback; first load is under 1500 KB.
