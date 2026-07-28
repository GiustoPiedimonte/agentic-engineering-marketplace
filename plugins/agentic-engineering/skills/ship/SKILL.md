---
name: ship
description: >
  This skill should be used to execute an approved pitch/spec as a delegated,
  closed-scope cycle with verification and adversarial review. Trigger with
  "ship this", "implement the pitch", "run this cycle", "build <shaped feature>".
  Enforces the execution playbook: pre-spawn filter, doc-bundle, PR format, review.
metadata:
  version: "0.2.0"
---

# /ship — execute a shaped cycle, verify, review

Turn an approved pitch into production-quality code through a disciplined cycle.
The organizing law: **parallelize readers, serialize writers** — research and
review can fan out; only one writer touches the code at a time.

`$ARGUMENTS` points to the approved pitch/spec. Read it first.

## 1. Pre-spawn filter (decide who does the work)

Before delegating to an executor subagent, answer three questions. If any is
"no", do NOT delegate — keep it human-driven / main-agent-driven:

1. **Deterministic?** Cleanup, inventory, zero-behavior refactor = yes.
   Behavior-altering (changes product behavior, identity, core flow) = no.
2. **Closed scope?** Finishable from a doc-bundle + this pitch without needing
   product judgment or user confirmations mid-flight.
3. **Low / low-medium risk?** High-risk (schema break, destructive migration) =
   no, or split into safe steps first.

See `references/EXECUTION_PLAYBOOK.md` for the full recipe.

### A pitch slice is not a PR slice

The most common way this filter passes and the cycle still fails: `/pitch` carves
the work into **conceptual** slices — coherent chunks of product thinking — and
those are usually two to four PRs each. Handing one to an executor as a single
scope looks fine (it *is* closed, it *is* shaped) and then the agent spends an
hour understanding half the codebase before it can write a line.

Size the scope by **steps that must happen in order**, not by how the pitch
reads. Reliability compounds at roughly 0.85 per serial step: four steps is
~52%, six is ~38%. A long serial chain is a scope problem, not a model problem —
the same guardrail `/graph` states for fan-out applies to the single writer.

Practical test: *could one PR of a few hundred lines close this, and would a
reviewer read it in one sitting?* If not, cut. Ship the narrowest version that
proves the shape works — one path end to end, one tool, one route — and let the
rest follow as its own cycle. If the shape is wrong you find out on two hundred
lines instead of two thousand.

## 2. Execute (delegated or direct)

- **Fan out the reading before you spawn the writer.** "Parallelize readers,
  serialize writers" is the law at the top of this skill, and the readers are
  the half people skip. An executor handed a bare pitch spends its first stretch
  doing breadth work in series — inventorying the substrate, reading the local
  conventions, grepping for what already exists — while the writer's context
  fills with material it will mostly not need. That reading is independent, so
  it belongs in `/graph`: a few researchers with distinct mandates, converging
  into a doc-bundle the writer receives already assembled.
- For a qualifying cycle, delegate to the `executor` subagent. It reads the
  doc-bundle first, implements ONE closed scope, commits as it goes, keeps the
  build + tests green, and opens a PR — **it never merges**.
- Otherwise implement directly, same discipline: TDD where feasible (write the
  failing test that encodes a "Done-when" item, make it pass), follow existing
  patterns, address root causes (never suppress an error to pass a check).
- Show evidence, not assertions: paste the commands run and their output.

### Watching a delegated writer

A background executor is quiet by design, and quiet is easy to misread as
stuck — which leads to killing an agent that was minutes from done. Know where
the real signals are before you need them:

- **`git log` in its worktree** is the honest one. An executor commits as it
  goes, so the branch moves long before anything else does.
- **The working tree** (`git status`) shows work in flight that hasn't been
  committed yet.
- **The transcript or output file is usually written on completion**, so an
  empty one says nothing at all about progress.
- **A message you send arrives on its next tool call.** Asking "are you alive?"
  is answered by exactly the agent that doesn't need asking, and ignored by the
  one that does.

Judge by the branch, not by the silence. And if a writer really has stalled,
the useful question is whether its scope was one closed scope or four —
resurrecting it unchanged tends to reproduce the stall.

## 3. Adversarial review (before "done")

Delegate to the `reviewer` subagent in a fresh context. Give it the diff, the
pitch, and the review checklist (`references/REVIEW_CHECKLIST.md`). It defaults to
skepticism and returns MERGE / ADJUST / REJECT with `file:line` specifics. Fix
real gaps (correctness / stated requirements) and re-review. Ignore
over-engineering suggestions (extra abstraction, defensive code for impossible
states).

If a measurement is needed to unblock a decision, delegate to the `measurer`
subagent (read-only data verdict) rather than guessing.

## 4. Dark launch & flip (behavior-altering changes)

A change that alters product behavior does **not** go live on merge. It ships
**dormant** — flag-OFF or dark-launched — and flips ON only after a real measure
window says it should. Green tests validate the mechanism, not the magnitude.

- **Ship dormant.** Merge behind a flag/dark path. The diff lands; the behavior
  doesn't, yet.
- **Record the gate with `/adr`.** The decision block carries `Gate (dormancy)`
  (how it ships dormant) and `Flip-criteria` (the measurable condition, the
  owner, and the observation window). No flip-criteria → it's not eval-gated, so
  either it's a trivial change or it isn't ready to merge.
- **Flip with `/measure`, not by assertion.** When the window matures, delegate
  to the `measurer` for a read-only verdict against the criterion. Flip ON only
  on a real flip verdict; otherwise keep dormant or cut. The decision stays open
  until the measurement is real.

Deterministic / zero-behavior cycles (cleanup, refactor, inventory) skip this —
they have no behavior to gate.

## 5. Close out

The PR uses the structure in `references/PR_FORMAT.md` (docs read, filter check,
what changed, test plan with evidence, no autonomous merge). On merge: move the
pitch to `docs/pitches/done/` with the PR link, record any decision (with its
`Gate`/`Flip-criteria` if behavior-altering) via `/adr`, and update the relevant
CLAUDE.md / docs in the same change.

Fill in "docs read" for real. It is the field most often left blank and the one
that pays: listing what you read is how a reviewer sees what you *didn't*, and
the doc you skipped is usually the one that already documented the trap you just
walked into.

Ask who outside this repo needs to know, and answer it when the PR opens rather
than later — whoever it is has the most context on it now and the least in a
week. "Nobody" is a fine answer and worth stating; the point is that it gets
asked. This is not a notification for every PR: a channel that receives all of
them stops being read, which costs more than the silence it replaced.

If you correct the same thing more than twice, stop — context is polluted.
Suggest `/clear` and a restart with a sharper prompt.
