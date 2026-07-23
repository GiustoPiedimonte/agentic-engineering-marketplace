---
name: pitch
description: >
  This skill should be used to shape a feature into a written spec before any
  code. Trigger when the user says "shape this", "write a pitch", "spec this
  out", "let's plan <feature>", or starts non-trivial work without an agreed
  approach. Produces a Shape Up style pitch (the source of truth) via interview.
metadata:
  version: "0.2.0"
---

# /pitch — shape the spec before the code

A pitch is the **source of truth** for a piece of work: it captures the problem,
the appetite, the shaped solution, and the boundaries. Code is downstream. Never
go prompt -> code for non-trivial work; shape first.

`$ARGUMENTS` is a short description of the feature/problem.

## Process

1. **Interview the user** with the `AskUserQuestion` tool. Skip obvious
   questions; dig into the hard parts they may not have considered:
   - The problem: what's broken / missing, for whom, why now.
   - Appetite: how much time/effort this is worth (this bounds the solution).
   - The shape of the solution at a high level (not implementation detail).
   - Explicit out-of-scope and hard no-gos.
   - Rabbit holes: the risky unknowns, and how to de-risk them.
   - "Done-when": the concrete checklist that closes the work.
   Ask in short rounds. One question at a time when possible.

2. **Ground it in the codebase** (read-only). Delegate wide reading to the
   `researcher` subagent so the main context stays clean. Inventory what already
   exists ("substrate already present") so the pitch builds on it, not over it.

3. **Name the graph.** State which of the five graphs this work touches (execution
   / memory / audit / capability / coordination — usually one primary) and which
   edges cross a human gate or an irreversible action (the severity×reversibility
   calls). If the work is a fan-out / audit / review / research job, sketch the
   nodes and edges — see the `graph` skill's `GRAPH_MODEL.md`. This makes the gate
   question explicit before any code, not after.

4. **Write the pitch** to `docs/pitches/<slug>.md` using the structure in
   `references/PITCH_TEMPLATE.md` (including the `Graph` and `Gated edges` fields).
   The pitch must be self-contained: name the files/interfaces involved, state
   what's out of scope, and end with a "Done-when" checklist that includes an
   end-to-end verification.

5. **Stop for review.** Show the pitch, ask for gaps/corrections. Do not start
   planning or coding until the user approves. Fix the shape, not the code.

Lifecycle convention: active pitches live in `docs/pitches/` (keep WIP low,
ideally 1). On completion they move to `docs/pitches/done/` with a link to the
PR. Parked work goes to `docs/pitches/parked/`.

Time spent making the pitch precise pays off more than time spent watching the
implementation. When in doubt, ask rather than assume.
