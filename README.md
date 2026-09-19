# my-claude-code-local-configs

Local [Claude Code](https://code.claude.com) configurations I use day to day — shared and documented for reference.

## Settings

[`.claude/settings.example.json`](.claude/settings.example.json) is a sanitized copy of the
`settings.json` I use. Copy the keys you want into your own `settings.json` (global at
`~/.claude/settings.json`, or project-level at `.claude/settings.json`) — don't overwrite your
file blindly. Full field-by-field reference: https://code.claude.com/docs/en/settings-reference.

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

*Note: whether Claude Code expands `$HOME` in the `hooks[].hooks[].command` field is
unverified — if it doesn't, use an absolute path instead.*

## Hooks

[`.claude/hooks/pre_tool_use.py`](.claude/hooks/pre_tool_use.py) is a `PreToolUse` hook: a
script Claude Code runs before every tool call, that can allow, block, or stay silent.

**Contract:**
- Claude Code sends the tool call as JSON on stdin (`tool_name`, `tool_input`, `cwd`, ...)
- Exit code `0` → allow, no opinion
- Exit code `2` → block the tool call; whatever was printed to stderr is shown to Claude as
  the reason
- A rule that raises an exception fails open — it's skipped, never blocks unrelated work

**Current rule:** `check_no_commit_on_main` — blocks `git commit` when the current branch is
`main` or `master` (including indirect forms like `git add . && git commit ...` or
`git -C . commit ...`).

**Install:**
1. Copy `.claude/hooks/pre_tool_use.py` to `~/.claude/hooks/` (global) or your project's
   `.claude/hooks/` (project-scoped)
2. `chmod +x` it
3. Add the `hooks` block from `.claude/settings.example.json` above to your own `settings.json`
4. Restart your Claude Code session — hooks are only read at session start

**Adding a new rule:** write a function `check_<name>(tool_name, tool_input, cwd) -> str | None`
in `pre_tool_use.py` and append it to the `RULES` list. See `CONTRIBUTING.md` for the full
steps, including tests.

**Limitations:** this is a guard-rail against carelessness, not a sandbox — the detection is
syntactic (it inspects the command Claude is about to run), so sufficiently indirect commands
aren't caught. It also only affects Claude's own `Bash` tool calls, not your terminal.

## Links

- [Contributing](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [License](LICENSE)

---

The hooks structure in this repo is inspired by
[claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery).
