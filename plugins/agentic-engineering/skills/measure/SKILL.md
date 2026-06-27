---
name: measure
description: >
  This skill should be used to unblock a decision that needs data. Trigger with
  "measure this", "do users actually...", "check the numbers before we cut/keep",
  "did the change land". Runs a read-only measurement and returns a data-backed
  flip/keep/cut verdict — never guesses, never writes.
metadata:
  version: "0.2.0"
---

# /measure — turn a gated decision into a data verdict

When a decision is blocked on "what do the data actually say?", measure instead
of guessing. `$ARGUMENTS` is the question to answer.

## Process

1. **State the question precisely** and what verdict each outcome implies
   (e.g. "if <1% of sessions hit this path -> cut; otherwise keep").
2. **Delegate to the `measurer` subagent** (or run directly if trivial). All
   access is **read-only** — open databases read-only, query logs/metrics
   without mutation. Never print secrets (no env dumps / token values).
3. **Report:** the question, the exact read-only command(s) run, the raw result,
   and a clear verdict (flip / keep / cut) with the reasoning.
4. **If the data isn't ready** (the runtime window hasn't matured, or the metric
   isn't populated), say so explicitly and state what window/data would settle
   it. Do not invent a verdict.

Distinguish what the data shows from what you infer from it. A measure-gated
decision stays open until the measurement is real.

## Flip-gate for dark launches

This is the mechanism that flips a dark-launched change ON (see `/ship` §4 and
the `Flip-criteria` field in `/adr`). When a decision was merged dormant with a
recorded flip-criterion, `/measure` is what closes it: run the read-only check
against that exact criterion and window, then return flip / keep / cut. Flip
only on a real flip verdict — never on a green build or a synthetic check, which
validate the mechanism, not the magnitude.
