# Pitch — <slug>: <one-line summary>

- **Status:** shaping | shaped | building | done | parked
- **Appetite:** <e.g. small batch / big batch — how much effort this is worth>
- **Created:** YYYY-MM-DD
- **PR:** <link when building/done>
- **ADR:** <link if this needed a recorded decision>
- **Graph:** <which of the five graphs this touches — execution / memory / audit / capability / coordination; usually one primary>
- **Gated edges:** <which arcs cross a human gate or an irreversible action — the severity×reversibility calls in this work; "none" if purely additive/read-only>

> Origin: why now. Link to research reports, prior decisions, or the trigger.

## Problem
What's broken or missing, and for whom. Be concrete. Include a short inventory
of the **substrate already present** (existing code/utilities this builds on) so
we extend rather than rebuild.

## Appetite
How much time/effort this is worth. The appetite bounds the solution — if it
doesn't fit, narrow the problem, don't grow the budget.

## Solution sketch
The shape, at the level of "what it does", not line-by-line code. Use tables for
architecture choices and their trade-offs. Slice into independently shippable
pieces where possible.

If the work is a fan-out / audit / review / research job, **draw the graph**: name
the nodes, the edges (what data crosses), the topology (diamond / router / verifier
/ cycle), and which nodes run in parallel. An independent node is one whose input
does not read another node's output.

## Out of scope
What we are deliberately NOT doing in this pitch.

## Rabbit holes
- R.1 — <risk / unknown> -> mitigation or de-risking step
- R.2 — <risk> -> mitigation

## No-gos
Hard prohibitions for this work (architectural lines not to cross).

## Done-when
- [ ] <concrete completion criterion>
- [ ] <criterion with a verification: test / command / screenshot>
- [ ] End-to-end check that proves the feature works: <the single check>

## Reference materials
- <links, research reports, related ADRs/pitches>
