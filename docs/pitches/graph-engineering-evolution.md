# Pitch — graph-engineering-evolution: make the plugin's graph explicit

- **Status:** shipped
- **Appetite:** small batch (one cycle — additive skill + agent + refs + manifests)
- **Created:** 2026-07-23
- **PR:** [#1](https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/pull/1) (implementation), [#2](https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/pull/2) (root README/CHANGELOG catch-up), released as v0.4.0
- **ADR:** ADR-002 (agentic engineering is graph engineering)
- **Graph:** execution (adds the `/graph` runtime); touches coordination + audit at the edges
- **Gated edges:** none new — this is additive tooling. The *content* it ships makes existing gates explicit (the human gate as a conditional edge; acting nodes project into audit).

> Origin: the plugin already worked as a graph without naming it, and Claude Code
> shipped dynamic workflows (the missing execution-graph runtime). Convergent
> external work (LangGraph, graph-augmented LLM agents, Agentforce guided
> determinism) points the same way.

## Problem
The cycle (`/pitch → /adr → /ship → /measure → /eval`) is a graph, the subagents are
nodes, adversarial review is a verifier, dark-launch + flip-criteria is an audit
projection — but nothing **names** the graph, and there is no first-class way to
**fan breadth work** (audit every route, review a large diff, research N angles)
across a fleet. Users default to straight-line chains that fill one context window.

Substrate already present: 5 skills, 4 agents (executor/researcher/reviewer/measurer),
2 hooks, the pitch template, the DECISIONS log. All of it stays; this extends it.

## Appetite
One small cycle. Additive only — no change to the existing skills' behavior beyond a
new `/pitch` step. If it grows past that, cut scope, not budget.

## Solution sketch
Add the execution-graph runtime and the shared vocabulary; reframe, don't replace.

| Piece | What it is | Kind |
|---|---|---|
| `skills/graph/SKILL.md` | `/graph` — draw the work as a graph, run it as a workflow | new |
| `skills/graph/references/GRAPH_MODEL.md` | grammar (node/edge), diamond/router/verifier/cycle, the five graphs, topology-first principles | new |
| `skills/graph/references/WORKFLOW_LIBRARY.md` | 6 copy-ready workflow scripts | new |
| `agents/verifier.md` | general single-claim adversarial node (fan-out safe) | new |
| `skills/pitch/*` | name the **graph** + **gated edges** before code | edit |
| manifests / README / CHANGELOG / DECISIONS | version bump + ADR-002 | edit |

The graph: `/pitch` shapes and names the graph → `/graph` fans out reading/auditing/
review inside a cycle → `/ship` serializes the one writer → `/eval`+`/measure` verify
on real data. Fan-out lives in code the model wrote (zero-token coordination); each
subagent keeps its own context.

## Out of scope
- Renaming the plugin (keeps `agentic-engineering` so every `settings.json` keeps
  working — a rename is a separate ADR).
- A graph-DB-backed memory (kept additive/light; reassessed only when a real
  multi-hop case pays for it).
- Distributing runnable workflows as first-class plugin assets (shipped as
  copy-ready templates for now).

## Rabbit holes
- R.1 — CI is strict (JSON parses, plugin.json ↔ marketplace versions match, SKILL
  frontmatter, README one-H1 + fenced-lang + resolving links). → run `ci_validate.py`
  before commit; new README links point at files that exist in this change.
- R.2 — "graph for its own sake" scope creep. → the model doc states when NOT to use
  a graph; `/graph`'s guardrails cap cycles and forbid self-routing consequential acts.

## No-gos
- No behavior change to `/adr`, `/ship`, `/measure`, `/eval` semantics.
- No new dependency. No breaking the plugin name or command names.

## Done-when
- [x] `python scripts/ci_validate.py` → "✓ all checks passed".
- [x] `/graph`, `/pitch` … `/eval` all appear; five agents under `/agents`.
- [ ] End-to-end: `/graph "audit every file under X for Y"` produces a workflow that
      fans out one node per file and verifies findings before reporting. *(not yet
      run in a live session — open follow-up, same as the readme-identity-redesign
      pitch's e2e proof.)*

## Reference materials
- ADR-002 · `hq/foundations/AGENTIC-GRAPH-ENGINEERING.md` (the Centria doctrine this
  distills the generic parts from) · the workflow library scripts.
