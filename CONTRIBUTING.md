# Contributing

Thanks for your interest in improving this marketplace. It hosts Claude Code
plugins — `agentic-engineering` (a spec-driven engineering workflow) and
`readme-keeper` (README maintenance). Contributions of all sizes are welcome: a
bug report, a sharper skill prompt, a doc fix, or a new role/skill that fits.

## Ways to contribute

- **Report a bug or rough edge** — [open an issue](https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/issues/new/choose).
- **Suggest a feature** — open a feature-request issue describing the problem
  first, then the idea.
- **Open a pull request** — for anything non-trivial, open or comment on an issue
  first so we agree on the shape before you build.

## What this repo is

Plugins here are **markdown and JSON** — skill prompts (`SKILL.md`), agent
definitions, hooks, and manifests. There is no application runtime or test suite;
correctness is verified structurally. Keep changes additive and honest, and match
the existing voice (terse, principled, evidence over assertion).

## Before opening a PR

1. **Validate the plugins:**
   ```bash
   claude plugin validate .
   claude plugin validate ./plugins/agentic-engineering
   claude plugin validate ./plugins/readme-keeper
   ```
2. **Keep manifests in sync** — if you change a plugin, bump its `version` in both
   its `plugin.json` and the matching entry in `.claude-plugin/marketplace.json`.
3. **Keep the README honest** — if you change behavior, update the relevant README
   in the same change. Don't add a badge or claim the repo can't back.
4. **One focused change per PR.** Fill in the PR template.

## Layout

See the [repo layout](README.md#maintaining) in the README. Each plugin lives
under `plugins/<name>/` with its own `plugin.json`, `skills/`, `agents/`, and
`README.md`.

## Code of Conduct

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
