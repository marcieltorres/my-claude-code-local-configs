# my-claude-code-local-configs

Local [Claude Code](https://code.claude.com) configurations I use day to day — shared and documented for reference.

## Settings

[`.claude/settings.example.json`](.claude/settings.example.json) is a sanitized copy of the `settings.json` I use. Copy the keys you want into your own `settings.json` (global at `~/.claude/settings.json`, or project-level at `.claude/settings.json`) — don't overwrite your file blindly. Full field-by-field reference: https://code.claude.com/docs/en/settings-reference.

```json
{
  "theme": "dark",
  "model": "sonnet",
  "spinnerTipsEnabled": false,
  "autoUpdatesChannel": "stable",
  "preferredNotifChannel": "terminal_bell",
  "attribution": {
    "commit": "",
    "pr": "",
    "sessionUrl": false
  },
  "statusLine": {
    "type": "command",
    "command": "jq -r '\"[\\(.model.display_name)] \\(.context_window.used_percentage // 0)% context\"'",
    "padding": 2
  },
  "plansDirectory": "./.claude/plans",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.claude/hooks/pre_tool_use.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

| Key | What it does |
|---|---|
| `theme` | UI color theme (e.g. `dark`, `light`). Not listed on the settings-reference page above; kept here as a commonly-set field. |
| `model` | Default model Claude Code starts new sessions with. |
| `spinnerTipsEnabled` | Hide tips shown in the spinner while Claude works. |
| `autoUpdatesChannel` | Release channel to follow (`stable` instead of `latest`). |
| `preferredNotifChannel` | How task completion is signaled (terminal bell or desktop notification). |
| `attribution.commit` | Customize or hide the trailer Claude Code adds to commits. |
| `attribution.pr` | Customize or hide the attribution line in pull request descriptions. |
| `attribution.sessionUrl` | Omit the claude.ai session link from cloud/Remote Control commits. |
| `statusLine.type` | Status line source type (`command` runs a shell command). |
| `statusLine.command` | Shell command that renders the status line; receives session JSON on stdin. |
| `statusLine.padding` | Left padding (in spaces) applied to the rendered status line. |
| `plansDirectory` | Where plan mode writes plan files. |
| `hooks` | Shell commands Claude Code runs around tool calls — see [Hooks](#hooks) below. |

*Note: whether Claude Code expands `$HOME` in the `hooks[].hooks[].command` field is unverified — if it doesn't, use an absolute path instead.*

## Hooks

Claude Code hooks are scripts that run around tool calls and session lifecycle events. Every hook here follows the same shape: a small, dependency-free Python script that reads a JSON payload from stdin and decides whether to allow, block, or stay silent — one script per hook event, with rules as plain functions inside it (never one file per rule).

### Available hooks

| Event | Script | Purpose |
|---|---|---|
| `PreToolUse` | [`pre_tool_use.py`](.claude/hooks/pre_tool_use.py) | Runs before a tool call; can block it |

More events (`PostToolUse`, `SessionStart`, ...) get their own row here as they're added.

### Contract

- Claude Code sends the event payload as JSON on stdin (`tool_name`, `tool_input`, `cwd`, ...)
- Exit code `0` → allow, no opinion
- Exit code `2` → block; whatever was printed to stderr is shown to Claude as the reason
- A rule that raises an exception fails open — it's skipped, it never blocks unrelated work

### `pre_tool_use.py`

Runs before every tool call. Rules are functions inside the script, checked in order; the first one that returns a reason wins.

| Rule | Blocks |
|---|---|
| `check_no_commit_on_main` | `git commit` — direct or indirect (`&&`, `-C`, `-c`, `--git-dir`, `--work-tree`) — when the current branch is `main` or `master` |

### Install

1. Copy the hook script(s) you want to `~/.claude/hooks/` (global) or your project's `.claude/hooks/` (project-scoped)
2. `chmod +x` them
3. Add the matching entry from the `hooks` block in `.claude/settings.example.json` to your own `settings.json`
4. Restart your Claude Code session — hooks are only read at session start

### Adding a new rule or hook

- **New rule for an existing hook:** write `check_<name>(tool_name, tool_input, cwd) -> str | None` inside that hook's script and append it to its `RULES` list.
- **New hook event:** add a new script (e.g. `post_tool_use.py`) following the same contract, and add a row for it in the tables above.

See `CONTRIBUTING.md` for the full steps, including tests.

### Limitations

This is a guard-rail against carelessness, not a sandbox. Detection is syntactic — each hook inspects the payload Claude is about to act on, so sufficiently indirect actions aren't caught. It also only affects Claude's own tool calls, not your terminal.

## Links

- [Contributing](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [License](LICENSE)

---

The hooks structure in this repo is inspired by [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery).
