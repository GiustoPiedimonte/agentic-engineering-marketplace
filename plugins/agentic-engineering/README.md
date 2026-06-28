# agentic-engineering (Claude Code plugin)

Spec-driven agentic engineering as an installable plugin. Generalized from a
real, opinionated agentic-engineering practice: the workflows that lived there as
prose conventions are turned into **invocable skills**, the bespoke subagents
into **portable roles**, and the "build+test green" rule into a **deterministic
hook** — so the same discipline travels to every repo, including new/simpler ones.

Philosophy: never go prompt -> code. Shape -> decide -> execute, with research
and review delegated to isolated subagents, and verification as a gate.

## Components

**Skills** (invocable)
- `/pitch` — shape a feature into a Shape Up pitch (the spec / source of truth)
  via interview, before any code.
- `/adr` — record a consequential decision in an append-only `docs/DECISIONS.md`.
- `/ship` — execute an approved pitch as a closed-scope cycle: pre-spawn filter,
  doc-bundle, standard PR format, then adversarial review before "done".
- `/measure` — unblock a decision with a read-only, data-backed flip/keep/cut
  verdict (never guesses, never writes).
- `/eval` — make eval the unit of progress: build the harness from REAL failures,
  localize where a pipeline breaks (transition-failure matrix), feed flip-criteria.

**Agents** (roles — "parallelize readers, serialize writers")
- `executor` (sonnet) — the serialized writer: implements one closed scope,
  keeps build/tests green, opens a PR, never merges.
- `researcher` (sonnet) — fan-out, read-only research with cited, verified
  findings; prefers current docs over memory.
- `reviewer` (opus) — adversarial pre-merge gate; 8-check rubric; MERGE/ADJUST/REJECT.
- `measurer` (sonnet) — read-only data verdicts to unblock measure-gated decisions.

**Hooks**
- PostToolUse: auto-format/lint edited TS/Py files (only if eslint/ruff present).
- Stop: prompt gate that requires verification evidence before ending a code turn.

## Install

Accept the `.plugin` file in chat, or in Claude Code run `/plugin` and install it
from a marketplace/local path. After install, `/pitch` `/adr` `/ship` `/measure`
`/eval` appear as commands and the four agents show under `/agents`.

Requires `jq` for the format hook. For the `researcher` to pull live library
docs, connect a docs MCP (e.g. Context7): `claude mcp add context7 -- npx -y @upstash/context7-mcp`.

## Usage (typical flow)

1. `/pitch "add Google OAuth to login"` — interview -> `docs/pitches/oauth.md`. Approve.
2. `/clear`, then `/adr` if a hard decision was made (e.g. session strategy).
3. `/clear`, then `/ship oauth` — executor implements + opens PR; reviewer checks
   the diff vs the pitch in a fresh context; fix real gaps; merge; move pitch to
   `docs/pitches/done/`.

Golden rules (from Claude Code best practices): separate exploration from
implementation; always give a verifiable check; delegate wide reading to
subagents; `/clear` between tasks; keep CLAUDE.md short.

## Customize per repo

Adapt the doc-bundle tiers in `skills/ship/references/EXECUTION_PLAYBOOK.md` to
your repo's docs, and the invariants in the review checklist to your project. The
skills reference `docs/pitches/`, `docs/DECISIONS.md` by convention — change the
paths if your repo differs.
