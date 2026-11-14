# RSVP kit: what was found and what was taken

Owner: Tomas. Written 2026-11-12. Review date: 2026-11-19. Rollback: `rm -rf rsvp/kit` and the entries named in `vendor/SOURCES.md`.

Eight free-model research jobs (`rsvp/kit/swarm.jobs`, raw answers in `rsvp/kit/runs/`) proposed candidates. Free models can invent details, so each candidate was checked at its source on 2026-11-12: the repository cloned at depth 1, the licence file read, every taken file read and grepped, and `tools/injection_screen.py` run. Pins and results are in `vendor/SOURCES.md`; which agent uses what is in `rsvp/SUBAGENTS.md`.

## Taken

| Question | Taken | Licence | Note |
| --- | --- | --- | --- |
| Cloudflare Workers and D1 | official `cloudflare/skills`: `wrangler`, `workers-best-practices`, `workers-development`, `cloudflare` (D1, `miniflare`, observability, bindings, secrets references) | Apache-2.0 | the feedback files were removed because they tell the agent to open public issues |
| Security | `claude-code-owasp` skill; `security-auditor` agent | MIT | the agent is read-only and runs on Opus |
| Testing | `tdd`, `property-testing`, `api-testing` skills; `qa-expert` agent | MIT | `property-testing` uses `fast-check`, which is a dev dependency to approve later |
| Accessibility | `accessibility-tester` agent | MIT | the project already has the `accessibility` skill and the `axe-core` engine |
| Localisation | `translating-portuguese`, `translating-spanish`, `translating-core`, `reviewing-translations` | MIT | review of the user's wording only; never writes copy |
| Privacy and data | `data-privacy-compliance` skill; `database-administrator`, `sqlite-expert` agents | MIT | the skill is enterprise-scale; the proportionate checklist is in `rsvp/PLAN.md` |
| Excel | `xlsx-manipulation` skill | MIT | the workbook uses real hyperlink cells, not formulas, so no recalculation step is needed |
| Code review | `code-reviewer` agent | MIT | read-only |

## Rejected after checking the source

| Candidate | Why |
| --- | --- |
| `zivtech/accessibility-skills` | the free agent said Apache-2.0; the licence file is GPL-3.0 |
| `mgifford/accessibility-skills` | AGPL-3.0 |
| `tiffanymwr15/Threat-Model-Skill-for-Claude-Code` | no licence file |
| `lackeyjb/playwright-skill` | ships a code executor; the project already drives Playwright directly |
| Anthropic `xlsx` skill | Apache-2.0, but needs LibreOffice (not installed) and carries unrelated validators |
| `semgrep/semgrep-rules` | `Semgrep Rules License`, not open source |

## Skipped without checking the source (from the free agents' own descriptions only)

These were not cloned or read by Claude, so nothing here is verified:

- `alirezarezvani/claude-skills` i18n-localization and `daymade/claude-code-skills` i18n-expert: reported to ship Python scripts; one reported without a licence. The markdown-only localisation skills above cover the need.
- `Yeachan-Heo/oh-my-claudecode` security-reviewer, `afiqiqmal/claude-security-audit`, `OneWave-AI` skills: overlap with what was taken, or the free agent gave the licence only as "implied".

## Collections and MCP servers (from the last job; not verified by Claude)

- `VoltAgent/awesome-claude-code-subagents` came out best, as expected; six of its agents were taken (see `rsvp/SUBAGENTS.md`).
- `wshobson/agents` (MIT per the free agent): a large multi-tool plugin with about 200 agents. Not taken: it overlaps with the above and is much bigger than this job needs.
- MCP servers named, none added: `microsoft/playwright-mcp` (local), `panasenco/mcp-sqlite` (local file only), `cloudflare/mcp-server-cloudflare` (needs Cloudflare API tokens), `cloudflare/playwright-mcp` (reported archived in October 2026). Adding any MCP server changes settings and needs the user's separate yes.

## Found but not taken (for later)

- `vinidlidoo` translation editor subagent and `senshinji` translation pipeline: personal projects without a clear licence.
- The `jezweb` D1 skill: licence not stated; the official `Cloudflare` references cover D1.
- MCP servers (Cloudflare, SQLite, Playwright): not added. Adding one changes settings and needs the user's separate yes.

## Gaps this kit does not fill

- No Workers-specific security-review agent; `security-auditor` plus `owasp-security` plus `workers-best-practices` cover it.
- No tool that tests inside WhatsApp's browser or on an iPhone; this needs real phones.
- The `spec-guardian` agent does not yet know the RSVP requirements; they are added to `SPEC.md` in stage 0.
