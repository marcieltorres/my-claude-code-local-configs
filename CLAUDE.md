# CLAUDE.md

Instructions for AI agents working in this repository.

## What this repo is

A place to share and document local Claude Code configurations (`settings.json`,
`PreToolUse` hooks, and the reasoning behind each decision). There is no application,
server, or library here — the content is configuration and documentation.

## Where things live

- `settings.example.json` — sanitized version of the real `settings.json`, ready to copy/adapt
- `.claude/hooks/` — versioned hook scripts (once they exist)

## Sanitization rule (the most important one)

Never commit to this repo:
- Tokens, API keys, credentials
- Machine-specific absolute paths (`/Users/<name>/...`)
- URLs of private repositories or internal company/organization names
- Anything coming from `.claude/settings.local.json` (it's local by definition)

Before proposing a change to any example config file, double-check that nothing
personal or machine-specific leaked in.

## Contribution flow

1. Open an issue before any PR (see `CONTRIBUTING.md`)
2. Follow `.github/PULL_REQUEST_TEMPLATE`
3. CI (`.github/workflows/pull_request.yml`) must pass — today it only validates that the
   repo's `.json` files are valid JSON
4. Commits follow Conventional Commits, no AI attribution

## Style

- Markdown and JSON use 2-space indentation (see `.editorconfig`)
- No `//` comments in `.json` — that's not valid JSON
