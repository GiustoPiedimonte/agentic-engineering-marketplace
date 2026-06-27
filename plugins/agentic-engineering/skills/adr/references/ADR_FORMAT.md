# ADR block format

Append blocks to `docs/DECISIONS.md` in this shape:

```markdown
## ADR-NNN — <short title>
**Date:** YYYY-MM-DD
**Status:** accepted | superseded by ADR-XXX
**Decision:** <what was decided, in one or two sentences>
**Context:** <the forces / constraints / options that led here>
**Rationale:** <why this option over the alternatives>
**Consequences:**
- <downstream effect, including any new constraints or follow-ups>
- <what becomes easier / harder>
[**Gate (dormancy):** <how it ships dormant: flag-OFF / dark-launched / behind a measure window — omit if the decision takes effect immediately>]
[**Flip-criteria (owner + eval-gated):** <the measurable condition that flips it ON, who owns the call, and the observation window — e.g. "owner: G; flip when ≥X over a 14-day window via /measure">]
[**Supersedes:** ADR-XXX]
```

Rules:
- One decision per block. Dated. Never edited after writing.
- A revision is a new, higher-numbered ADR that supersedes the old one.
- Record only consequential, hard-to-reverse decisions — not routine choices.
- Numbers are monotonic; allocate the next free integer.
- **Eval-gated / dark-launched decisions carry both `Gate (dormancy)` and
  `Flip-criteria`.** The flip is owned and measured, not assumed: the decision
  stays dormant until `/measure` shows the criterion is met. Synthetic checks
  validate the mechanism, not the magnitude — flip on real data, not on a green
  build.
