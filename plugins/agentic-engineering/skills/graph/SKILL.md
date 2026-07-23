---
name: graph
description: >
  This skill should be used to design or run a task as a graph instead of a
  linear chain — fan out independent work across a fleet of subagents, verify
  findings, and converge. Trigger with "run this as a graph", "fan this out",
  "parallelize this", "orchestrate this with subagents", "audit every X",
  "sweep the codebase for Y", or any breadth job one context can't hold. Turns
  a straight-line agent into an execution graph (diamond / router / verifier /
  cycle) built on dynamic workflows.
metadata:
  version: "0.1.0"
---

# /graph — draw the work as a graph, then run it

Most multi-step agents are a straight line: step one, step two, step three, each
waiting politely for the last, until the context window fills and the agent forgets
what it was doing. Half those steps never needed to wait. This skill turns the line
into a graph: nodes do the thinking, edges carry the results, and independent work
runs at once.

`$ARGUMENTS` is the objective (e.g. "audit every route under src/ for missing auth").
Read `references/GRAPH_MODEL.md` for the grammar and `references/WORKFLOW_LIBRARY.md`
for copy-ready scripts.

## Process

1. **Draw the graph before running it.** Sketch nodes and edges. For every "and
   then", apply the edge test: does the next step read the last step's output? If
   not, cut the arrow — those nodes are independent and will run in parallel. Name
   the topology (diamond / router / verifier / cycle) — see the model reference.

2. **Give every node a contract.** Bounded input, validated output, one job. When
   the work should return structured data, hand the `agent()` call a JSON `schema`
   so the sub-agent is *forced* to return validated data — no free text to parse.

3. **Choose the runtime.**
   - **Dynamic workflow** (default for real fan-out) — describe the objective and
     let Claude write a plain-JavaScript orchestration script that spawns a
     coordinated fleet of subagents. The coordination costs **zero model tokens**
     because it's code, not a conversation, and each subagent carries its own
     context so the session never drowns. Say the word "workflow", run a saved one
     from `.claude/workflows/`, or adapt a template from the library.
   - **Inline subagents** — for a one-off diamond of a few nodes, spawn the
     researcher / reviewer / verifier / measurer agents directly.

4. **Put the reduce in code, not in an agent.** Flatten, dedupe, filter, rank-by-key
   are `results.flatMap(...)` and a `Set` — deterministic, instant, zero tokens.
   Save agents for judgment, not for plumbing.

5. **Gate confidence with a verifier.** Before a finding is allowed downstream, run
   the `verifier` agent (or a parallel panel) to try to kill it. Ship only what
   survives. This is the `/ship` adversarial review generalized to any finding.

6. **Tier the models and pick the topology deliberately.** Route repetitive nodes
   (extract, classify) to a cheaper model; keep the merge/judgment node high.
   Default to `pipeline()` (streams items, no barrier); reach for a `parallel()`
   barrier only when a stage genuinely needs every prior result at once.

## Guardrails

- **Few steps per cycle.** A long serial chain is a scope problem, not a model
  problem (reliability compounds ~0.85^steps). Split it.
- **Self-routing is for research, not for consequential action.** Letting Claude
  write the graph is great for scoped read/analysis work; anything that acts on the
  world stays explicit, gated (`/ship` §4), and audited — a node that self-routes
  around a human gate is a bug.
- **Worktree isolation only when nodes write in parallel.** `isolation: 'worktree'`
  is the seatbelt for parallel writers (e.g. file-by-file porting); it's a real cost
  otherwise — don't tax every run with it.
- **Fan-out is not free of judgment cost.** Spend it for breadth one context can't
  hold or for an independent perspective — never for decoration.

This skill is the **execution graph** of agentic-engineering. It composes with the
cycle: `/pitch` shapes, `/graph` fans out the reading/auditing/review inside a
cycle, `/ship` serializes the one writer, `/eval` and `/measure` verify on real data.
