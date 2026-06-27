# Eval playbook — error analysis & transition-failure matrices

Adapted from Hamel Husain's error-analysis method for agentic workflows. The goal
is to turn a vague "the agent is flaky" into a ranked, localized diagnosis you can
act on, and to leave behind a harness that gates future change.

## 1. Build the failure dataset (real, not synthetic)

- Collect actual runs: production/dev logs, recorded sessions, the dev DB. Sample
  failing *and* a few passing traces (you need contrast).
- One row per run with: the input, the full step trace, the final output, and the
  expected/ideal outcome. Keep it read-only — never mutate the source.

## 2. Open-code, then axial-code

- **Open-code:** for each failure, write a short free-text note describing what
  went wrong, in plain language. Don't categorize yet.
- **Axial-code:** group the notes into a small set of named failure modes. A good
  set is 4–8 modes, mutually distinct, each with a one-line definition.
- **Count** occurrences per mode → this frequency ranking is your fix order.
- **Saturation:** keep reading traces until new ones stop yielding new modes.
  Record how many you read and the saturation point — that's your confidence.

## 3. Transition-failure matrix (localize the break)

A pass-rate tells you *that* it failed; this tells you *where*. Model the flow as
ordered steps S1 → S2 → … → Sn. For each failed trace, mark the step where the
failure **first** appears. Tabulate:

```
                         failed at →
step (where it broke)    count   share   example trace
-----------------------  -----   -----   -------------
S1 intent / tool-select    14     47%    trace_0093
S2 argument extraction      9     30%    trace_0041
S3 tool execution           3     10%    trace_0118
S4 result integration       2      7%    trace_0072
S5 final format / voice     2      7%    trace_0005
-----------------------  -----   -----
total failures             30    100%
```

Read it as: most breakage is upstream (intent/tool-selection), so fixing final
formatting would move almost nothing. Re-run the matrix after a change — a
regression shows up as a specific row growing, not just a worse aggregate.

For multi-turn flows, add a second axis (turn index) to see whether failures
concentrate early or compound over a session.

## 4. Choose the assertion level per mode

| Mode shape | Assertion | Why |
|---|---|---|
| Exact tool, schema valid, value in range, no-PII | Deterministic code assert (component-level) | Fast, free, no drift — prefer always |
| Voice/tone, helpfulness, "did it actually answer" | LLM-judge (task-level) | Judgment is irreducible |
| End-to-end success on a fixed scenario | Scenario eval (seeded input → asserted outcome) | Guards the whole pipeline |

Rule: reach for an LLM-judge only when no deterministic assert is faithful. When
you do, validate it: label a held-out set by hand, measure the judge's agreement
(e.g. % match / Cohen's κ), and report that number. An unvalidated judge is an
opinion, not an eval.

## 5. Close the loop

- Add only the evals that encode *observed* modes (skip imagined ones).
- Wire the deterministic ones into CI so regressions fail the build.
- If this gates a dark launch, hand the concrete flip-criterion to `/adr`
  (`Flip-criteria`) and `/measure` (the live check). Example:
  "flip when `wrong-tool-selected` < 2% AND end-to-end-success ≥ 90% over a
  14-day real-traffic window."

## Anti-patterns

- Optimizing aggregate pass-rate while the dominant matrix row is untouched.
- Synthetic-only datasets (validate mechanism, not magnitude).
- Trusting an LLM-judge whose human agreement was never measured.
- Eval sprawl: a growing suite for modes that never occur.
