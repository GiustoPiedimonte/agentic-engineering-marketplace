# Execution playbook

A reproducible recipe for delegating a closed-scope cycle to a subagent.
Standardizes what to read, the pre-implementation filters, and the output format,
so each cycle doesn't reinvent the context.

## 0. Pre-spawn filter (main agent, before spawning)

Three mandatory questions. If ONE is "no", the cycle does NOT go to a subagent:
1. Is it deterministic? (behavior-altering = no)
2. Is the scope closed? (finishable from bundle + pitch, no product judgment)
3. Is risk low / low-medium? (high-risk = no, or split)

Also confirm: the work is shaped + approved, it's within the WIP cap, and a spec
exists. Unshaped or unapproved work stays human-driven.

## 1. Doc-bundle MUST-READ (every subagent reads these BEFORE acting)

Adapt the tiers to the repo. The point: read code + docs before proposing or
changing anything. The FIRST section of the PR must list the files read.

- **Tier 1 — always:** root `CLAUDE.md`, the project's principles/conventions,
  any hard invariants, the live plan/roadmap, and the agent's own memory index.
- **Tier 2 — sub-directory context:** the nearest `CLAUDE.md` / docs for the path
  being touched.
- **Tier 3 — spec + decisions:** the relevant pitch and any related ADRs.
- **Tier 4 — chronicle + reference:** intervention history, operations/reference
  docs as needed.

## 2. Per-cycle contract

The executor declares: SCOPE (exactly what it will touch), does an empirical
pre-check (reproduce / inventory), implements, produces OUTPUT (isolated branch,
idempotent migration if any, doc updates, green build + tests), and states
explicit NON-goals. On any doubt not resolvable from the available context: ask
the user — do not guess.

## 3. Gates

- **Pre-spawn:** cycle in the plan? spec exists? WIP within cap?
- **Post-PR:** docs-read list present? tests green? open verifications concrete?
- **Post-merge:** chronicle updated, decision recorded, plan/pitch status updated.

## 4. Anti-patterns (do not)

- Redo research that already exists — read prior reports, cite, extend.
- Open parallel work beyond the WIP cap.
- Add abstractions "for later" (YAGNI).
- Change behavior inside a cycle labeled refactor/cleanup/kill.
- Auto-merge. The executor opens PRs; a human (or the orchestrator after review)
  merges.
- Skip the doc-bundle. Guess user preferences.

## 5. Wave execution (optional, for many cycles)

Run cycles in parallel **waves of orthogonal files** (e.g. a docs-only wave, a
refactor wave, a capability wave). The human reviews the global pattern between
waves, not every individual cycle. Never run two writers on overlapping files.

**Mind the token cost of fan-out.** Read-only fan-out (researchers, reviewers,
measurers) is cheap and parallelizing it is close to free — fan out freely.
Agent fan-out, by contrast, can cost ~15× the tokens of a single linear pass
(token use dominates the cost variance), so a wide *writer* wave is the expensive
one. The serialized-executor rule already bounds this — one writer at a time —
but size each wave to the value it returns, not to how parallel it *can* be.
