# Decisions

Append-only. One decision per block, dated, never edited. A revised decision is a
new ADR that supersedes the old one. This is the authoritative record of *why* we
decided things — not a plan, not a backlog.

## ADR-001 — The fidelity gate (derive from the project, not from us)
**Date:** 2026-06-29
**Status:** accepted
**Decision:** `/readme` (github-keeper) gains a **fidelity gate**: before generating
any visual, voice, or proposable element, it derives the direction from the target
**project's own communication** (logo, palette, tone, domain, audience) and
**proposes-and-confirms** with the human before producing anything. Our
`assets/banner.svg` terminal-card is demoted from "the template" to one archetype
among several, and "no banner / minimal" is a valid recommendation. The fidelity
gate is ranked **below** the honesty gate.
**Context:** Field feedback: the skill imposed our house style ("le immagini vengono
generate troppo secondo quello standard invece che prendere la comunicazione del
progetto"). The elevate playbook literally told the agent to reuse our banner as the
template, so libraries, UI apps, and research repos all trended toward our terminal
aesthetic. Detecting a project's identity is error-prone.
**Rationale:** Imposing one house look is both low-quality (wrong for most repos) and
a subtle dishonesty (an identity that isn't the project's). Making the gate
propose-and-confirm de-risks the unreliable detection — a wrong guess costs a
sentence, not a rebuild — and matches the "more collaborative" ask. Ranking it below
honesty resolves conflicts: a project's vibe never justifies a signal the repo can't
back.
**Consequences:**
- `elevate` is no longer a one-shot rebuild to a fixed look; it proposes a direction
  first. Slightly more interactive, materially more faithful.
- The badge/section guidance becomes an adaptive proposal set (project + maintainer),
  not a fixed checklist — with an "ask at most 2–3 questions" bound to avoid an
  intake interrogation.
- Extends the existing "preserve an existing style / gate big rewrites" rule from
  prose to visuals and brand.
- Out of scope for this slice: beyond-README docs, a formal iterative mode,
  translations, a banner-generator script.
