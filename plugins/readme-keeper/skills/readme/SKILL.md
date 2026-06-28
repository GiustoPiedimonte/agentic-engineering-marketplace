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
  version: "0.2.0"
---

# /readme — audit & elevate a public README

A README is a contract: every claim — version, install command, link, badge — is
implicitly promised true. This skill keeps that contract honest **and** raises the
README to a high standard. `$ARGUMENTS` is the target (a path, default `README.md`)
and a mode:

- **`audit`** — report only: ranked pass/fail findings, no edits.
- **`elevate`** (default for a thin/generic/empty README) — rebuild it to a
  polished, **repo-specific** README: banner, honest badges, custom chips, funnel
  structure, real examples.
- **`fix`** — apply the audit's fixes to an already-good README without a full
  rebuild.

The governing rule across all modes is the **honesty gate**: never show a signal
you cannot back. No CI badge without a workflow, no version badge a release will
outdate, no registry badge without a published package, no "used by" without real
users, no vanity chip without a link to its proof. A broken or dishonest badge is
worse than none — when in doubt, drop it.

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

4. **Elevate (repo-aware generation).** Once the scope is agreed, follow
   `references/ELEVATE_PLAYBOOK.md`:
   - **Badges from reality** — emit only badges with a real backing artifact and a
     live click target (`[![alt](img)](target)`), one consistent style. Add
     **custom chips** specific to this repo (a true static fact → linked to its
     proof, e.g. `skills-5` → the `skills/` dir).
   - **Hero** — a centered `<h1>`, badge row, plain-English tagline, nav row. For
     the signature look, generate an SVG **banner** parameterized to the repo
     (wordmark, palette, and a chips row = the repo's real commands / modules /
     pipeline), committed to `assets/`. Use this marketplace's own
     `assets/banner.svg` as the template.
   - **Funnel** — hero → why-this-exists (claim + real proof) → TOC (if ≥100 lines
     or 5+ sections) → install (the *real* command) → quickstart (a *real* example)
     → features (from actual capabilities) → requirements → maintaining →
     contributing → license. Convert load-bearing notes to GitHub callouts
     (`> [!NOTE]/[!TIP]/[!IMPORTANT]`). Clean headings for reliable anchors.

5. **Report specifics.** For audit: ranked pass/fail with `file:line`. For elevate:
   the detected signals, every badge/chip with its justified link target, and the
   sections rebuilt. No "looks fine" — passed or failed.

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
