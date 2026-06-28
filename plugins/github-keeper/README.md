# github-keeper (Claude Code plugin)

Make a public GitHub repository **well-made and honest** — not just the README, but
everything a project is judged and trusted by. Two skills, one principle: never
show a signal the repo can't back, and confirm anything outward before doing it.

A repo is a contract. README *rot*, a missing security policy, a CI badge with no
CI, a repo with no contributing guide — each erodes trust. This plugin closes
those gaps, with every signal derived from the actual repo.

## Skills

- **`/readme`** — audit *and* elevate the README. Rebuilds a thin/generic one into
  a polished, **repo-specific** README: an SVG banner, honest live badges, custom
  chips (a true fact linked to its proof), cognitive-funnel structure, and a
  quickstart lifted from real code. Preserves an existing voice; gates big rewrites
  on confirmation.
- **`/opensource`** — make the repo public-ready: the community-health files
  (Code of Conduct, Contributing, Security, issue/PR templates), an **honest CI
  gate**, and the right repo settings (issues, private vulnerability reporting,
  delete-branch-on-merge, topics). Never flips a repo public or changes settings
  without explicit confirmation.

## The honesty gate

The rule above all others: **never show a signal you cannot back.** No CI badge
without a workflow, no version badge a release will outdate, no registry badge
without a published package, no security policy without a working reporting
channel, no fabricated contact or adoption. A broken or dishonest signal is worse
than none.

## Install

```text
/plugin marketplace add GiustoPiedimonte/agentic-engineering-marketplace
/plugin install github-keeper@giusto-agentic
```

After install, `/readme` and `/opensource` are available as commands.

## Usage

```text
/readme                 # audit README.md, report ranked findings, offer to fix
/readme elevate         # rebuild to a polished, repo-specific README
/opensource             # report OSS-readiness gap, then close it (with confirmation)
```

## References

- [`README_CHECKLIST.md`](skills/readme/references/README_CHECKLIST.md) — README audit checklist, funnel, badge conventions, rot failure modes.
- [`ELEVATE_PLAYBOOK.md`](skills/readme/references/ELEVATE_PLAYBOOK.md) — repo detection, badge decision matrix, SVG banner recipe.
- [`OSS_PLAYBOOK.md`](skills/opensource/references/OSS_PLAYBOOK.md) — community-profile checklist, repo settings, CI patterns, the confirmation gates, and `templates/` for every file.
