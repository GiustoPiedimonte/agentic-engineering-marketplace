# agentic-engineering — a Claude Code plugin

A spec-driven workflow for building with coding agents: **shape → decide →
execute → measure → eval**. It turns a mature production methodology into
portable, invocable tooling — five skills, four subagent roles, and verification
hooks — so the same discipline travels to every repo.

The core rule: **never go prompt → code.** Shape the work into a written spec
first, record the hard decisions, delegate execution to a serialized writer with
an adversarial reviewer as a gate, and let real data — not a green build — decide
what ships.

> Distributed as a Claude Code *marketplace* named `giusto-agentic`, hosting the
> `agentic-engineering` plugin.

## Install

In Claude Code:

```
/plugin marketplace add GiustoPiedimonte/agentic-engineering-marketplace
/plugin install agentic-engineering@giusto-agentic
```

CLI equivalent:

```
claude plugin marketplace add GiustoPiedimonte/agentic-engineering-marketplace
claude plugin install agentic-engineering@giusto-agentic
```

After install, the five commands and four agents are available. New components
load on your next Claude Code session.

## What you get

**Skills** (slash commands)

| Command | What it does |
|---|---|
| `/pitch` | Shape a feature into a Shape Up pitch (the spec / source of truth) via interview, before any code. |
| `/adr` | Record a consequential decision in an append-only `docs/DECISIONS.md`, with optional dark-launch `Gate`/`Flip-criteria`. |
| `/ship` | Execute an approved pitch as a closed-scope cycle: pre-spawn filter, doc-bundle, standard PR format, adversarial review, dark-launch flip. |
| `/measure` | Unblock a decision with a read-only, data-backed flip/keep/cut verdict — never guesses, never writes. |
| `/eval` | Make eval the unit of progress: build the harness from *real* failures, localize where a pipeline breaks (transition-failure matrix), feed flip-criteria. |

**Agents** (roles — *parallelize readers, serialize writers*)

| Agent | Role |
|---|---|
| `executor` | The serialized writer: implements one closed scope, keeps build/tests green, opens a PR, never merges. |
| `researcher` | Fan-out, read-only research with cited, verified findings; prefers current docs over memory. |
| `reviewer` | Adversarial pre-merge gate; 8-check rubric; returns MERGE / ADJUST / REJECT. |
| `measurer` | Read-only data verdicts to unblock measure-gated decisions. |

**Hooks**

- *PostToolUse* — auto-format/lint edited TS/Py files (only if `eslint`/`ruff` are present).
- *Stop* — a gate that requires verification evidence before ending a code turn.

## Typical flow

1. `/pitch "add Google OAuth to login"` — interview → `docs/pitches/oauth.md`. Approve the shape before any code.
2. `/clear`, then `/adr` if a hard decision was made (e.g. session strategy). Behavior-altering work records a `Flip-criteria`.
3. `/clear`, then `/ship oauth` — the executor implements and opens a PR; the reviewer checks the diff against the pitch in a fresh context; you fix real gaps and merge.
4. Behavior-altering changes ship dark (flag-OFF), then `/measure` against the recorded criterion flips them on — on real data, not a green build.

## Requirements

- **Claude Code** (CLI, desktop, or IDE extension).
- **`jq`** on your machine, for the format hook.
- *(optional)* A docs MCP such as [Context7](https://github.com/upstash/context7)
  so `researcher` / `/measure` can pull live library docs:
  `claude mcp add context7 -- npx -y @upstash/context7-mcp`.

## Customize per repo

The skills reference `docs/pitches/` and `docs/DECISIONS.md` by convention. Adapt
the doc-bundle tiers in `plugins/agentic-engineering/skills/ship/references/EXECUTION_PLAYBOOK.md`
and the invariants in the review checklist to your project, and change the paths
if your repo differs. See the [plugin README](plugins/agentic-engineering/README.md)
for details.

## Maintaining

Releasing an update: bump `version` in both
`plugins/agentic-engineering/.claude-plugin/plugin.json` and
`.claude-plugin/marketplace.json`, commit, and push to `main`. Users pick it up
with `/plugin marketplace update giusto-agentic`.

Validate before pushing:

```
claude plugin validate .
claude plugin validate ./plugins/agentic-engineering
```

To host more plugins from this repo, add folders under `plugins/` and list each
in `marketplace.json`'s `plugins` array.

## Layout

```
agentic-engineering-marketplace/
├── .claude-plugin/
│   └── marketplace.json        # lists the plugin(s), schema-validated
├── plugins/
│   └── agentic-engineering/    # the plugin itself
│       ├── .claude-plugin/plugin.json
│       └── skills/  agents/  hooks/  README.md
└── README.md
```

## Links

- [Plugin marketplaces — Claude Code docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [Plugin README](plugins/agentic-engineering/README.md) — full component reference and per-repo customization.

## License

MIT — see [LICENSE](LICENSE).
