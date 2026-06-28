# readme-keeper (Claude Code plugin)

Make a public repository's README **high-quality and honest**. One skill,
`/readme`, that audits *and* elevates the document a project is judged by — before
a release, or any time the README and reality have drifted apart.

A README is a contract: every claim in it — version, install command, link, badge
— is implicitly promised true. README *rot* is when reality moves and the README
doesn't. This plugin treats that drift as a bug — and rebuilds a thin or generic
README into a polished one, with every signal derived from the actual repo.

## The skill

`/readme` first establishes ground truth (stack, package manager, CI, releases,
license, what the repo does, a real usage example), then runs in one of three modes:

- **`audit`** — verifiable pass/fail findings with `file:line` specifics, no edits.
- **`elevate`** (default for a thin/generic README) — rebuild it to a polished,
  **repo-specific** README: an SVG banner, honest live badges, **custom chips**
  (a true fact linked to its proof), cognitive-funnel structure, and a quickstart
  lifted from real code.
- **`fix`** — apply the audit's fixes to an already-good README.

## The honesty gate

The rule above all others: **never show a signal you cannot back.** No CI badge
without a workflow, no version badge a release will outdate, no community badge
without a live invite, no "used by" without real users. A broken or dishonest
badge signals neglect — worse than no badge. When in doubt, drop it.

## Install

```text
/plugin marketplace add GiustoPiedimonte/agentic-engineering-marketplace
/plugin install readme-keeper@giusto-agentic
```

After install, `/readme` is available as a command.

## Usage

```text
/readme                 # audit README.md, report ranked findings, offer to fix
/readme elevate         # rebuild to a polished, repo-specific README
/readme audit docs/X.md # report only, on a specific file
```

The audit uses portable `git` / `curl` / `grep` checks (no installs required) and
will use `lychee`, `markdownlint`, or `cspell` if they happen to be present.

References:
- [`README_CHECKLIST.md`](skills/readme/references/README_CHECKLIST.md) — the full
  audit checklist, section-order funnel, badge link-target conventions, and the top
  README-rot failure modes with their detection.
- [`ELEVATE_PLAYBOOK.md`](skills/readme/references/ELEVATE_PLAYBOOK.md) — the
  repo-detection table, the badge decision matrix (repo type → honest badges + link
  targets), the SVG banner recipe, and the repo-specific generation workflow.
