# my-claude-code-local-configs

Local [Claude Code](https://code.claude.com) configurations I use day to day — shared and documented for reference.

## Settings

[`.claude/settings.example.json`](.claude/settings.example.json) is a sanitized copy of the
`settings.json` I use. Copy the keys you want into your own `settings.json` (global at
`~/.claude/settings.json`, or project-level at `.claude/settings.json`) — don't overwrite your
file blindly. Full field-by-field reference: https://code.claude.com/docs/en/settings-reference.

**Intentionally excluded:** `hooks`, `enabledPlugins`, `extraKnownMarketplaces` — out of scope
for this file (see `CONTRIBUTING.md`).

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

## Links

- [Contributing](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [License](LICENSE)
