# Pitch — readme-identity-redesign: make /readme speak the project's language

- **Status:** shipped (skill/playbook updated) — e2e proof on a non-dev-tool repo is the open follow-up
- **Appetite:** small batch — the two core pillars only
- **Created:** 2026-06-29
- **PR:** direct-to-main (solo repo); github-keeper 0.4.0
- **ADR:** ADR-001 (fidelity gate)

> Origin: user feedback after trying the shipped skill — "poco versatile," and the
> sharp one: *"le immagini vengono generate troppo secondo quello standard invece
> che prendere la comunicazione del progetto."* The skill imposes a house style
> instead of deriving from the target project.

## Problem

`/readme` (github-keeper) today is a **house-standard elevator**. Two concrete
failures on any repo that isn't a CLI/dev-tool:

1. **It imposes our identity, not the project's.** `ELEVATE_PLAYBOOK.md` Step 3
   says *"Use this marketplace's own `assets/banner.svg` as the template."* So every
   elevated repo tends toward our terminal-card aesthetic and funnel — regardless of
   whether it's a Python library, a UI app, a design tool, or a research artifact.
   The visual/voice/badges should come from the **project's** communication, not
   ours. The badge/section guidance is a fixed "honest-when" checklist, not an
   *adaptive proposal* shaped by what this project and this maintainer actually have.
2. **Only coarse modes.** `audit` / `elevate` / `fix`, each whole-README. No way to
   say "do just this."

**Substrate already present** (build on it):
- The skill already has a *"preserve an existing style / gate big rewrites"* rule
  (`SKILL.md` step 3) — the fidelity gate **extends** it from prose to visuals/brand.
- The **honesty gate** is the model for a cross-cutting principle; fidelity is its
  sibling, ranked below it.
- `ELEVATE_PLAYBOOK.md` has the badge matrix, a hero recipe, and the tier model.
- `assets/banner.svg` stays — demoted from "the template" to *one example* (the
  CLI/dev-tool archetype).

## Appetite

Small batch. Ship the **two core pillars** only. Resist turning this into a full
docs assistant.

## Solution sketch

### Pillar 1 — Fidelity gate (the project's identity, not ours)

A first-class principle, ranked **below** the honesty gate. Before generating any
visual/voice/element, the skill **reads the project's communication**, **proposes a
direction, and confirms** before producing anything.

| Step | What |
|---|---|
| Read identity | existing logo/screenshots, brand palette (logo/CSS/site), wordmark, the current README's tone, the domain & audience, any website |
| Classify archetype | pick the visual language that fits (table below) |
| **Propose + confirm** | present the proposed archetype + palette + voice ("serious library → clean typographic hero, palette from the logo, **no** terminal-card") and wait for the human — never autonomous |
| Generate within it | produce the hero/copy in the project's language; commit only after approval |

**Visual archetypes** (terminal-card is one row):

| Archetype | Fits | Hero |
|---|---|---|
| Terminal-card | CLI, dev-tool, agent | dark card + prompt + chips (our `banner.svg`) |
| Typographic | library, framework, SDK | clean wordmark + type, palette from brand |
| Screenshot-led | UI / app / dashboard | a real current screenshot |
| Diagram-led | infra, protocol, data | an architecture/flow diagram |
| Illustrated | creative / consumer tool | an illustrated/branded hero |
| **Minimal / none** | serious tools (à la ruff/biome) | **no banner** — a clean type hero |

**Restraint is a valid output.** The gate may recommend *no* generated image.

#### Beyond the banner — an adaptive proposal set

The same gate governs **what elements to propose at all** — badges, links, sections
— shaped by the project *and* the maintainer, not a fixed list. Propose from what's
**detected**; ask at most **2–3** high-value things that can't be (R.5).

| Detected / asked | Propose |
|---|---|
| a community (Discord/Slack/forum) | a community badge + a Community section + invite |
| GitHub Sponsors / Open Collective | a sponsor badge + a short support line |
| a docs site | a docs badge + a Documentation link/section |
| published to a registry | version / downloads badges |
| active maintainer socials | a follow link in the footer |
| a company/org behind it | a "built by" line, if wanted |
| screenshots / a CLI demo | a screenshot or asciinema block |

Every proposal bound by the **honesty gate** (only if real) and
**propose-and-confirm**. Output = a menu tailored to this project and person.

### Pillar 2 — Intent-driven targeted edits

`$ARGUMENTS` accepts a **free-form goal** ("add a quickstart", "make the hero
punchier", "just the banner"). The skill does **only that**, at minimal scope.
`audit`/`elevate`/`fix` remain explicit keywords; with a goal and no keyword, the
default is to collaborate on the intent. Adjacent issues are *mentioned*, not
touched.

## Out of scope

- Beyond-README (CONTRIBUTING, `docs/`, guides, translations) — deferred.
- A formal iterative before/after mode — deferred (propose-and-confirm covers the
  needed human-in-loop for visuals).
- A banner-generator script — the agent authors SVG directly.
- Changing `/opensource` or the audit correctness checks.

## Rabbit holes

- **R.1 — Identity/archetype detection is unreliable.** → **Propose-and-confirm**:
  never autonomously generate a visual; a wrong guess costs a sentence, not a rebuild.
- **R.2 — Fidelity vs honesty conflict.** → **Honesty wins, always.** Fidelity is
  subordinate; never adopt an identity that needs a signal the repo can't back.
- **R.3 — Intent edits creep.** → Strict scope: the asked element only; list
  adjacent findings, don't act on them without a new ok.
- **R.4 — Our funnel imposed as structure.** → The funnel becomes guidance adapted
  to the project type, not a fixed mold.
- **R.5 — Over-interrogating the maintainer.** → Propose from what's detectable;
  ask at most 2–3 high-value questions; never block on answers.

## No-gos

- Never generate a banner/visual without confirming the direction first.
- Never default to the terminal-card archetype.
- Never overwrite a project's existing voice; amplify it.
- The honesty gate is **never** subordinate to the fidelity gate.

## Done-when

- [ ] `SKILL.md`: fidelity gate documented as a first-class principle (below
      honesty); `$ARGUMENTS` accepts free-form intent; modes clarified.
- [ ] `ELEVATE_PLAYBOOK.md`: hero recipe is **archetype-driven** (the table, incl.
      "minimal/none"); the *"use our `banner.svg` as the template"* line replaced
      with "derive from the project; our banner is one example for the CLI
      archetype"; a **propose-and-confirm** step added before any generation.
- [ ] `ELEVATE_PLAYBOOK.md`: badge/section guidance becomes an **adaptive proposal
      set** (project+maintainer table), gated by honesty + propose-and-confirm, with
      the "ask at most 2–3" rule.
- [ ] Intent-edit path documented (targeted change, minimal scope, adjacent-on-ok).
- [ ] `claude plugin validate .` and `python3 scripts/ci_validate.py` green;
      github-keeper version bumped; ADR-001 recorded.
- [ ] **End-to-end check (follow-up):** run `/readme` against a **non-dev-tool**
      repo and confirm it **proposes a faithful visual direction — NOT a
      terminal-card** — offers restraint where apt, and proposes context-appropriate
      elements (e.g. a community badge+section when a community exists); plus a
      targeted-intent run that touches only what's asked.

## Reference materials

- `plugins/github-keeper/skills/readme/SKILL.md` (step 3 = the seed of the gate)
- `plugins/github-keeper/skills/readme/references/ELEVATE_PLAYBOOK.md` (Step 3 hero
  recipe = the line to fix; badge matrix; tiers)
- `assets/banner.svg` (the CLI-archetype example)
