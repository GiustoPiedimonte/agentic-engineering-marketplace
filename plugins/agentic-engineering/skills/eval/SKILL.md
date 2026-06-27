---
name: eval
description: >
  This skill should be used to make eval the unit of progress: systematize how a
  feature or agent is judged. Trigger with "how do we eval this", "build an eval
  harness", "why is the agent failing", "error analysis", "are we regressing",
  or before flipping an eval-gated dark launch. Builds evals from REAL failures
  (not synthetic), localizes where a pipeline breaks, and feeds flip-criteria.
metadata:
  version: "0.2.0"
---

# /eval — make eval the unit of progress

You don't improve what you don't measure, and you don't measure with invented
test cases. Evals start from **real failures**, get coded into failure modes,
and become the harness that gates change. `$ARGUMENTS` is the feature / agent /
flow to evaluate (or a pointer to a trace dump).

This skill is offline and diagnostic — it builds and runs the harness over
traces/datasets and tells you *where* and *how* things break. Its live sibling
is `/measure` (a one-shot read-only verdict on a gated decision); `/eval` is what
defines what "good" even means, and produces the criteria `/measure` later checks.

## Process

1. **Start from real traces, never synthetic.** Pull actual failing runs (logs,
   recorded sessions, the dev DB). Delegate the wide read to the `researcher`
   subagent and read-only data pulls to the `measurer`. Synthetic cases validate
   the *mechanism*, not the *magnitude* — they cannot tell you what really breaks.

2. **Error-analysis (open-code → axial-code).** Read a sample of failures and
   write a free-text note on what went wrong for each. Then cluster those notes
   into a small set of named **failure modes** (e.g. wrong-tool-selected,
   argument-extraction-error, voice/format-drift, hallucinated-fact). Count them
   — frequency ranks what to fix first. Stop sampling when new traces stop
   producing new modes (theoretical saturation), and say how many you read.

3. **Localize with a transition-failure matrix** (for multi-step / agentic
   flows). For each step boundary, record where the failure first appears, so a
   regression is pinned to a stage (tool-selection vs extraction vs formatting)
   rather than to a vague pass-rate. See `references/EVAL_PLAYBOOK.md`.

4. **Pick the assertion level per mode** — the cheapest that's faithful:
   - **Deterministic / component-level** (code asserts): exact tool chosen,
     schema valid, value in range. Prefer these — fast, free, no judge drift.
   - **LLM-judge / task-level** only where judgment is irreducible (voice,
     helpfulness, end-to-end success). Align the judge to human labels on a
     held-out set before trusting it; report its agreement rate.

5. **Report a diagnosis, not a number.** Ranked failure modes with counts, the
   transition matrix, the few evals worth adding, and — if this gates a dark
   launch — the concrete **flip-criterion** to hand to `/adr` and `/measure`
   (e.g. "flip when wrong-tool-selected < 2% over a 14-day real window").

## Anti-patterns

- Pass-rate as the only signal — it hides *where* the regression is.
- Evals seeded from imagined cases instead of observed failures.
- An LLM-judge trusted without measuring its agreement with human labels.
- Adding evals for modes that never actually occur (YAGNI applies here too).

A feature isn't "done" because tests are green; it's done when the evals that
encode its real failure modes hold on real data.
