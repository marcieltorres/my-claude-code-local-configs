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

## Adding a new hook rule

`.claude/hooks/pre_tool_use.py` follows a simple contract: each rule is a function
`check_<name>(tool_name, tool_input, cwd)` that returns a reason string to block the tool
call, or `None` to allow it. To add one:

1. Write the `check_<name>` function in `pre_tool_use.py`.
2. Add it to the `RULES` list.
3. Add test cases (at least one blocking, one passing) to `tests/test_pre_tool_use.py`.
4. Run `python3 tests/test_pre_tool_use.py` — it must pass before opening the PR.

Keep the one-script-per-event convention — no new file, no rules package, no changes to
`settings.example.json` needed for a new rule (only for a new hook event like `PostToolUse`).

## Checklist before the PR

- [ ] No sensitive or machine/company-specific data was committed
- [ ] If you changed `.claude/settings.example.json`, validate it with `python3 -m json.tool .claude/settings.example.json`
- [ ] If you changed a hook, run `python3 tests/test_pre_tool_use.py`
- [ ] Referenced the related issue in the PR (`closes #XXXX`)
