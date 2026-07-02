---
name: readme
description: >
  This skill should be used to audit OR elevate the README of a public repository.
  Trigger with "improve the README", "make the readme high quality", "elevate this
  readme", "audit the readme", "add badges", "is our README good", or before
  publishing/releasing a repo. Elevate rebuilds a thin/generic README to a polished,
  repo-specific one (banner, honest live badges, custom chips, cognitive-funnel
  structure) — every signal derived from the actual repo. Honesty-first: never adds
  a signal the repo can't back. Produces a verifiable result, then re-verifies.
metadata:
  version: "0.3.0"
---

# /readme — audit & elevate a public README

A README is a contract: every claim — version, install command, link, badge — is
implicitly promised true. This skill keeps that contract honest **and** raises the
README to a high standard.

`$ARGUMENTS` is an optional path plus either a mode keyword or a **free-form goal**.
**With no path, discover and handle every README in the repo**, not just the root
one. Match files whose *basename* is
`README.md` (or `README.<lang>.md` for translations) — not a substring match, which
would wrongly pull in reference docs like `README_CHECKLIST.md`:

```bash
git ls-files | grep -E '(^|/)README(\.[a-z]{2})?\.md$'
```

This finds the root README plus nested ones (`plugins/*/README.md`,
`packages/*/README.md`, `docs/**/README.md`, …). Apply the **right tier** to each
(see below); don't impose the landing-page look on a component reference. Pass a
path to target a single file.

Modes — a keyword, **or a free-form goal**:

- **A free-form intent** (e.g. "add a quickstart", "make the hero punchier", "just
  the banner", "add an FAQ") — do **only that**, at minimal scope. Mention adjacent
  issues you notice; don't touch them without a fresh ok. This is the default when a
  goal is given without a keyword — collaborate on the intent, don't audit-everything
  or rebuild-everything.
- **`audit`** — report only: ranked pass/fail findings, no edits.
- **`elevate`** (default for a thin/generic/empty README) — rebuild it to a
  polished, **project-faithful** README (see the fidelity gate): a *fitting* hero,
  honest badges, an adaptive element set, funnel structure, real examples.
- **`fix`** — apply the audit's fixes to an already-good README without a full
  rebuild.

The governing rule across all modes is the **honesty gate**: never show a signal
you cannot back. No CI badge without a workflow, no version badge a release will
outdate, no registry badge without a published package, no "used by" without real
users, no vanity chip without a link to its proof. A broken or dishonest badge is
worse than none — when in doubt, drop it.

## The fidelity gate (speak the project's language, not ours)

Second only to the honesty gate. **The visual, the voice, and the set of elements
must come from the target project's own communication — not from this marketplace's
house style.** A Python library, a UI app, an infra tool, and a CLI each speak a
different language; imposing our terminal-card banner and funnel on all of them is
both low-quality and a quiet dishonesty (an identity that isn't theirs).

So, before generating anything:

1. **Read the project's identity** — existing logo/screenshots, brand palette (from
   a logo, CSS, or site), wordmark, the current README's tone, the domain and
   audience, any website. (See the detection table in `ELEVATE_PLAYBOOK.md`.)
2. **Propose a direction, then confirm.** Present the archetype + palette + voice
   ("serious library → clean typographic hero, palette from the logo, **no**
   terminal-card") and **wait for the human**. Never autonomously generate a visual —
   a wrong guess should cost a sentence, not a rebuild.
3. **Generate within that language**, only after approval.

Two hard rules:
- **Restraint is a valid output.** For a serious tool the faithful choice may be
  *no banner* — a clean typographic hero. Recommending less is fidelity, not laziness.
- **Honesty outranks fidelity.** If a project's vibe would invite a dishonest signal
  (a fake "used by", an overclaiming banner), honesty wins — always.

Our `assets/banner.svg` is **one archetype** (CLI/dev-tool), not the template. The
same gate governs the whole **adaptive proposal set** — badges, links, sections —
tailored to the project *and* the maintainer (see `ELEVATE_PLAYBOOK.md`).

## README tiers (not every README is the front page)

Hold each README to the standard that fits its role — don't put a hero banner on a
sub-page:

- **Landing** (one per repo — the root `README.md`): the full standard — hero
  banner, badge row, tagline, nav, TOC, the cognitive funnel. This is the project's
  front door.
- **Component reference** (`plugins/*/README.md`, `packages/*/README.md`,
  `docs/**/README.md`): a clean, accurate reference — one clear H1, correct
  structure, language-tagged fences, resolving links, honest content. **No banner,
  no hero, no badge row** (those belong to the landing page). Excellence here is
  clarity and accuracy, not decoration.

When sweeping a repo, classify each README first, then apply its tier's bar. A
plain component reference is *correct*, not a defect; a plain landing page is a gap.

## Process

1. **Establish ground truth — read, don't assume.** Detect what the repo *is*
   before generating anything: stack / package manager, whether it's published to
   a registry, CI workflows, tags/releases, license, the GitHub `About` /
   topics / homepage, what it actually does, and a *real* minimal usage example.
   See the detection table in `references/ELEVATE_PLAYBOOK.md`. This decides which
   badges are honest and what the hero says.

2. **Audit against the checklist** (`references/README_CHECKLIST.md`) — content
   accuracy, link & anchor integrity, badge integrity, metadata consistency,
   style/structure, accessibility, freshness. Use the portable `git`/`curl`/`grep`
   snippets (no installs required); reach for `lychee`/`markdownlint`/`cspell` only
   if present. Delegate wide reads or live-URL checks to a read-only research
   subagent when one is available.

3. **Respect what's already there — and gate big rewrites.** Before elevating,
   judge the blast radius:
   - **If the README already has a deliberate style/voice**, improve *within* it —
     keep its tone, structure, and identity; fix and strengthen rather than
     replace. Don't impose this marketplace's look on a repo that already has one.
   - **Estimate how much would change.** A light pass (badges, a TOC, a few
     callouts, tightened prose, fixed links) can proceed directly.
   - **If elevate would substantially transform the README** — replace the voice,
     restructure most sections, drop existing content, or add a banner where none
     existed — **STOP and get explicit human confirmation first.** Present the
     plan: what's detected, the proposed hero/badges/sections, and a summary of
     what would be removed or rewritten. Apply only after the human approves.
   Default to asking when unsure. A large rewrite without sign-off is the failure
   mode to avoid — the human owns the project's voice.

4. **Elevate (project-faithful generation).** Once the direction is agreed (fidelity
   gate — propose-and-confirm), follow `references/ELEVATE_PLAYBOOK.md`:
   - **Hero — the fitting archetype, not ours by default.** Pick the archetype that
     matches the project (typographic for a library, screenshot for a UI, diagram for
     infra, terminal-card for a CLI, illustrated for a creative tool — or **none**,
     a clean type hero, when that's the faithful choice). Generate it in the
     project's palette/voice, committed to `assets/`. The terminal-card
     `assets/banner.svg` here is one example (the CLI archetype), not the template.
   - **Adaptive proposal set** — badges, links, and sections proposed from what the
     project *and* maintainer actually have (a community → a community badge +
     section; a docs site → a docs badge; sponsors → a support line; …). Propose from
     what's detectable; ask at most 2–3 things you can't detect. Every element bound
     by the honesty gate (only if real, live click target `[![alt](img)](target)`)
     and confirmed before adding. See the proposal-set table in the playbook.
   - **Funnel** — hero → why-this-exists (claim + real proof) → TOC (if ≥100 lines
     or 5+ sections) → install (the *real* command) → quickstart (a *real* example)
     → features (from actual capabilities) → requirements → maintaining →
     contributing → license. Convert load-bearing notes to GitHub callouts
     (`> [!NOTE]/[!TIP]/[!IMPORTANT]`). Clean headings for reliable anchors.

5. **Report specifics.** For audit: ranked pass/fail with `file:line`. For elevate:
   the detected signals, every badge/chip with its justified link target, and the
   sections rebuilt. No "looks fine" — passed or failed. **When sweeping a repo,
   report per-README with its tier** (landing vs component reference), so a clean
   sub-page reads as "passed for its tier," not as a miss.

6. **Verify the result, don't assert it.** Re-run link/anchor/badge checks and
   render-check the banner after editing; show the output. Confirm one H1, every
   fence language-tagged, version consistent across README and manifest(s), and the
   README one-liner matching the GitHub `About`. A badge that reads `unknown` or a
   dead link means it isn't done.

## What to add only if real
Release/version badge → only with a tag or registry release. CI badge → only with a
workflow. Registry version/downloads → only if published. Community badge → only
with a live invite. Screenshots → only current ones. Custom chip → only a true fact
with a link to its proof. Everything else honest-by-default: license, stars,
last-commit are live and safe; a banner and an ASCII/diagram are always fair game.

## Output
Audit: a ranked findings report (passed/failed checks with specifics).
Elevate: the rebuilt README plus a short rationale — detected stack, the honest
badge/chip set with link targets, the banner, and the re-verification output.
