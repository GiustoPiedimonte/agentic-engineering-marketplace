# agentic-engineering (Claude Code plugin)

Spec-driven agentic engineering as an installable plugin — and, underneath, as
**graph engineering**. Generalized from a real, opinionated practice: the workflows
that lived there as prose conventions are turned into **invocable skills**, the
bespoke subagents into **portable roles**, and the "build+test green" rule into a
**deterministic hook** — so the same discipline travels to every repo.

Philosophy: never go prompt -> code, and never queue in a straight line what could
run as a graph. Shape -> decide -> execute, with research and review delegated to
isolated subagents (nodes), verification as a gate (an edge), and breadth work
fanned out across a fleet instead of chained one-at-a-time. See
[skills/graph/references/GRAPH_MODEL.md](skills/graph/references/GRAPH_MODEL.md).

## Components

**Skills** (invocable)
- `/pitch` — shape a feature into a Shape Up pitch (the spec / source of truth)
  via interview, before any code. Now names the **graph** the work touches and its
  **gated edges** (severity×reversibility) up front.
- `/adr` — record a consequential decision in an append-only `docs/DECISIONS.md`.
- `/graph` — turn a straight-line task into an execution graph: fan out independent
  work across a fleet of subagents, verify findings, converge. Built on dynamic
  workflows (coordination costs zero model tokens). Ships a copy-ready
  [workflow library](skills/graph/references/WORKFLOW_LIBRARY.md).
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
- `reviewer` (opus) — adversarial pre-merge gate over a whole PR diff; 8-check
  rubric; MERGE/ADJUST/REJECT.
- `verifier` (sonnet) — general adversarial verifier node: given one finding/claim,
  tries to kill it and returns a real/not-real verdict. Fan-out safe (run N in
  parallel, or with distinct lenses) as a gate on a graph edge.
- `measurer` (sonnet) — read-only data verdicts to unblock measure-gated decisions.

**Hooks**
- PostToolUse: auto-format/lint edited TS/Py files (only if eslint/ruff present).
- Stop: an advisory reminder — when a turn leaves uncommitted changes, it prints a
  one-line nudge to run the repo's own checks before declaring done. Never blocks,
  never re-invokes the model (can't loop, even with background workflows), silent on
  clean turns, artifact-neutral (no assumed typecheck/build/test).

## The five graphs

The skills map onto five graphs: **execution** (the cycle + `/graph`), **memory**
(what the repo knows), **audit/provenance** (dark-launch, flip-criteria, the ADR
log), **capability/tools** (the human gate as a conditional edge), and
**coordination** (readers fan out, writers serialize). Governance lives on the
edges: the gate is a conditional edge, and every acting node should project a row
into the audit graph.

## Install

Accept the `.plugin` file in chat, or in Claude Code run `/plugin` and install it
from a marketplace/local path. After install, `/pitch` `/adr` `/graph` `/ship`
`/measure` `/eval` appear as commands and the five agents show under `/agents`.

Requires `jq` for the format hook. For the `researcher` to pull live library
docs, connect a docs MCP (e.g. Context7):

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

## Usage (typical flow)

1. `/pitch "add Google OAuth to login"` — interview -> `docs/pitches/oauth.md`,
   naming the graph + gated edges. Approve.
2. `/clear`, then `/adr` if a hard decision was made (e.g. session strategy).
3. `/clear`, then `/graph` if the work has breadth to fan out (audit every route,
   research N angles) — draw the graph, run it as a workflow, verify findings.
4. `/clear`, then `/ship oauth` — executor implements + opens PR; reviewer checks
   the diff vs the pitch in a fresh context; fix real gaps; merge; move pitch to
   `docs/pitches/done/`.

Golden rules (from Claude Code best practices): separate exploration from
implementation; always give a verifiable check; delegate wide reading to
subagents; `/clear` between tasks; keep CLAUDE.md short.

## Customize per repo

Adapt the doc-bundle tiers in `skills/ship/references/EXECUTION_PLAYBOOK.md` to
your repo's docs, and the invariants in the review checklist to your project. Save
the workflow templates you use into `.claude/workflows/` to run them by name. The
skills reference `docs/pitches/`, `docs/DECISIONS.md` by convention — change the
paths if your repo differs.
