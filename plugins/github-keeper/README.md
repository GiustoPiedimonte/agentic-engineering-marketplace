# github-keeper (Claude Code plugin)

Make a public GitHub repository **well-made and honest** — not just the README, but
everything a project is judged and trusted by. Two skills, one principle: never
show a signal the repo can't back, and confirm anything outward before doing it.

A repo is a contract. README *rot*, a missing security policy, a CI badge with no
CI, a repo with no contributing guide — each erodes trust. This plugin closes
those gaps, with every signal derived from the actual repo.

## Skills

- **`/readme`** — audit *and* elevate a README, **in the project's own language**.
  The **fidelity gate** derives the hero archetype (typographic, screenshot,
  diagram, terminal-card, or *none*), palette, voice, badges, and sections from the
  target project's identity — proposing a direction and confirming before it
  generates, never imposing a house style. Accepts a **free-form goal** ("add a
  quickstart", "just the banner") to do only that. Honest, live signals only;
  preserves an existing voice.
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
