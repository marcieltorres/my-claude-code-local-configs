# CLAUDE.md

Instructions for AI agents working in this repository.

## What this repo is

A place to share and document local Claude Code configurations (`settings.json`, `PreToolUse` hooks, and the reasoning behind each decision). There is no application, server, or library here — the content is configuration and documentation.

## Where things live

- `.claude/settings.example.json` — sanitized version of the real `settings.json`, ready to copy/adapt
- `.claude/hooks/pre_tool_use.py` — versioned `PreToolUse` hook, one script per hook event with rules as functions inside it
- `tests/test_pre_tool_use.py` — regression suite for the hook, run via CI

## Sanitization rule (the most important one)

Never commit to this repo:
- Tokens, API keys, credentials
- Machine-specific absolute paths (`/Users/<name>/...`)
- URLs of private repositories or internal company/organization names
- Anything coming from `.claude/settings.local.json` (it's local by definition)

Before proposing a change to any example config file, double-check that nothing personal or machine-specific leaked in.

## Contribution flow

1. Open an issue before any PR (see `CONTRIBUTING.md`)
2. Follow `.github/PULL_REQUEST_TEMPLATE`
3. CI (`.github/workflows/pull_request.yml`) must pass — it runs tests and validations
4. Commits follow Conventional Commits, no AI attribution

## Adding a new PreToolUse rule

Rules live inside `.claude/hooks/pre_tool_use.py`, one function per rule:

1. Write `check_<name>(tool_name, tool_input, cwd) -> str | None` — return a reason string to block, or `None` to allow.
2. Append it to the `RULES` list at the bottom of the file.
3. Add at least one blocking case and one passing case to `tests/test_pre_tool_use.py`.
4. Run `python3 tests/test_pre_tool_use.py` before opening the PR.
5. Document the rule in `README.md`'s rule table for that hook (e.g. the `pre_tool_use.py` section) — every rule needs a row describing what it blocks.

Do not create a new file per rule, and do not add a rules registry/package for this — the convention here is one script per hook event, with rules as functions inside it. Each rule must fail open (never raise past its own `check_*` call) — `main()` already wraps each rule in `try/except`, so a broken rule can't block unrelated work.

## Style

- Markdown and JSON use 2-space indentation (see `.editorconfig`)
- No `//` comments in `.json` — that's not valid JSON
