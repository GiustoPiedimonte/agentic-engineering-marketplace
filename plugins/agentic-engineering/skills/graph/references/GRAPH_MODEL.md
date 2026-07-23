# The graph model

The organizing idea behind this plugin: **the shape of the work is a graph.** What
runs before what, what can run at the same time, what has to wait for everything
else — that shape is a graph. Nodes do the thinking; edges carry the results.

A prompt is a sentence. A loop is a cycle. A harness is the floor the agent stands
on. But the *work itself* is a graph — and most linear agents are just a degenerate
graph: one unbranching chain where half the arrows carry no data and every wait is
wasted.

## Grammar

- **Node** — one unit of work: one `agent()` call, one bounded job, one input in,
  one output out. A node can be a deterministic code step, a single LLM call, or a
  full sub-agent run.
- **Edge** — a *dependency*: this node's output feeds that node's input. Nothing
  more. "And then" is **not** an edge. The edge exists only when data actually
  moves across it. For every "and then", ask: *does the next step read the last
  step's output?* If not, there is no edge, and the wait is wasted.

Draw it as boxes and arrows. A box is an `agent()` call; an arrow is a variable
passed from one call's return into another's prompt. If you can't draw the arrow,
the two boxes are independent — and independence is what you exploit to go wider.

## Contracts (the discipline that makes a graph reliable)

- **Node contract:** bounded input, validated output, exactly one job. In a
  workflow this is enforced with a JSON `schema` on the `agent()` call — the
  sub-agent is *forced* to return validated structured data (retry on mismatch),
  not free text you parse and pray over.
- **Edge contract:** name the edge by its *data*, not its order. A → produces this
  shape; B is built to consume it. Then you can see instantly whether the edge is
  real, and swap either node as long as the shape holds. The reduce between stages
  (flatten, dedupe, filter) is **plain code — zero tokens**. A huge amount of what
  people burn model tokens on is really an edge, and edges are free.

## Core topologies

| Topology | Shape | Use it for |
|---|---|---|
| **Chain** | A→B→C | Genuinely sequential work only (each step reads the last). |
| **Diamond** | split → fan-out → reduce → synthesize | The workhorse: market scan, dependency audit, code review, research report. |
| **Router** | classify → branch | Path depends on what a node found (diff size, ticket class, risk). |
| **Verifier** | finding → skeptics → gate | Confidence: a node whose only job is to try to kill a finding before it passes. |
| **Cycle** | work → check → loop-until-dry | Unknown-size discovery (bug sweep, exhaustive audit). |

**Diamond** — `fan out → reduce → synthesize`. Fan out for breadth, reduce with
plain code to compress, synthesize with a final agent to write the answer. Once you
see the diamond you stop asking "how do I make the agent do more steps" and start
asking "where's the split, where's the merge" — the question that scales.

**Router** — an agent classifies (judgment at the node), **code** picks the edge
(`if`/`switch` on validated output). Determinism becomes a feature: the branch runs
the same way every time for the same classification. No emergent "it decided to
skip the audit" — the skip would have to be written into the graph.

**Verifier** — three patterns worth having in hand: *adversarial* (N independent
skeptics prompted to refute; keep only if a majority survive), *perspective-diverse*
(each verifier a distinct lens — correctness, security, does-it-reproduce), *judge
panel* (N attempts, parallel judges, synthesize from the winner).

**Cycle** — `loop-until-dry`: keep spawning finders until K consecutive rounds turn
up nothing new. The one detail that makes or breaks it: **dedupe against everything
seen, not just against confirmed results** — otherwise rejected findings reappear
every round and the loop never converges.

## The five graphs

Any agentic system decomposes into five graphs. Four are the standard axes of
graph-augmented agents; the fifth is what a *governed* system adds.

1. **Execution** — how the work runs (workflows, subagents, the pitch→ship cycle).
2. **Memory** — what the system knows (notes, retrieval, entities & relations).
3. **Audit / provenance** — what happened and who validated it. *The governance
   axis: every traversal of the execution graph should project a row here.*
4. **Capability / tools** — what an agent can do (tools, MCP, policy, the human
   gate as a conditional edge).
5. **Coordination** — how multiple agents/people divide work (handoff, delegation,
   one-writer-per-scope as an edge constraint).

## Principles (topology-first)

1. **Topology-first.** Optimize the graph's shape before tweaking prompts. A wrong
   behavior is usually a missing edge, not bad wording.
2. **Guided determinism.** The graph constrains; the LLM decides *inside* nodes.
   Spend autonomy where judgment lives, not by default.
3. **Nodes are thin and swappable.** A node that leaks its framework is a rewrite.
4. **Edges are contracts.** No arc without a shape, even a stub one.
5. **The gate is a conditional edge, not a line in a prompt.**
6. **Every traversal leaves an audit row.** Execution projects into provenance.
7. **Cycles, yes — but few steps.** At 85%/step, a 10-step chain succeeds ~20% of
   the time. Narrow scope = demonstrable reliability.
8. **Compose sub-agents as nodes, in clean context.** Context is state that flows;
   prune it, don't accumulate it.
9. **Entities and relations before the heavy graph.** Grow memory additively;
   adopt a full knowledge graph only when a real multi-hop case pays for it.
10. **The team is a graph.** Delegation follows the fractures in the work, not
    "one thing each."

## When NOT to reach for a graph

- Genuinely sequential work (each step truly reads the last) — a chain is correct.
- A single bounded question one agent can answer in its own context.
- "Multi-agent for its own sake" — fan-out costs real tokens; spend it for breadth
  one context can't hold, or for an independent perspective, never for decoration.
