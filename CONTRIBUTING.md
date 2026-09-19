# Contributing [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

Thanks for considering contributing. Please read carefully before opening an issue or PR.

## What this repo is

A place to share and document local [Claude Code](https://code.claude.com) configurations — `settings.json`, `PreToolUse` hooks, and the decisions behind them. It's not a library or a service; it's configuration and documentation.

## What's accepted as a contribution

- Fixes or improvements to the example configs (`settings.example.json`)
- New hook rules, or improvements to existing ones
- Fixes and improvements to the documentation
- Reports of issues using these configs on a different machine/setup

## Before opening a PR

Open an issue first. Any change needs to be discussed before proceeding — this avoids rework.

## Sanitization rule

**Never commit real machine or company data.** This includes:

- Tokens, API keys, credentials
- Machine-specific absolute paths (`/Users/<name>/...`)
- URLs of private repositories, internal organization/company names
- Anything from `.claude/settings.local.json` (that file is local by definition — it should never be versioned)

Example configs must be generic enough for anyone to copy and adapt.

## Commit convention

[Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`). No `Co-Authored-By` from AI tools — the commit is yours.

## Where to understand the decisions

The reasoning behind the hooks (rule contract, output format, known limits) is documented in `.claude/plans/ideia.md` — it's an idea under evaluation, not yet implemented in this repo.

## Checklist before the PR

- [ ] No sensitive or machine/company-specific data was committed
- [ ] If you changed `settings.example.json`, validate it with `python3 -m json.tool settings.example.json`
- [ ] Referenced the related issue in the PR (`closes #XXXX`)
