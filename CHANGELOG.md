# Changelog

All notable changes to this marketplace and its plugins are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
plugin versions follow [Semantic Versioning](https://semver.org).

## [Unreleased]

### Added
- **README "Staying updated" section** — documents the hands-off path (enable
  auto-update for the marketplace once → Claude Code notifies on new versions and
  prompts `/reload-plugins`) and the manual fallback.
- `CHANGELOG.md` (this file).
- **github-keeper** `/opensource` playbook: a note on documenting the update /
  distribution story as part of a well-made published repo.

### Changed
- **Stop hook is now advisory** (agentic-engineering) — it prints a one-line
  reminder on uncommitted changes but never blocks or re-invokes the model, so it
  can't loop, including with background/dynamic workflows. The verification
  discipline stays in the `/ship` and `executor` prompts.
- Versions: agentic-engineering → 0.2.2, github-keeper → 0.3.3.

## [0.3.2] - 2026-06-28

### Added
- **github-keeper** plugin (renamed from `readme-keeper`): `/readme` audits and
  elevates a README (multi-README sweep by tier — landing vs component reference);
  `/opensource` adds community-health files, an honest CI gate, and repo settings.

### Changed
- Quieter, artifact-neutral **Stop hook** in agentic-engineering — silent on clean
  turns, references the project's own checks instead of assuming typecheck/build/test.
- Honest provenance framing ("a real agentic-engineering practice"); README badge
  row trimmed to the stable, meaningful set (Claude Code · CI · Release · License).
- Badge guidance gains a "stable vs volatile" rule (drop self-undermining badges
  like `last-commit`).
- Plugin versions: agentic-engineering 0.2.1, github-keeper 0.3.2.

## [0.3.0] - 2026-06-28

### Added
- **readme-keeper** plugin — `/readme` audit & maintenance for a public README.
- High-quality public README (SVG banner, clickable live badges, TOC, GitHub
  callouts), MIT `LICENSE`.
- Open-source community health (Code of Conduct, Contributing, Security policy,
  issue/PR templates) and a CI validation workflow.

## [0.2.0] - 2026-06-27

### Added
- Initial public release. **agentic-engineering** plugin — `/pitch`, `/adr`,
  `/ship`, `/measure`, `/eval`; executor / researcher / reviewer / measurer
  subagents; format + verification hooks; the dark-launch eval-gated loop.

[Unreleased]: https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/compare/v0.3.2...HEAD
[0.3.2]: https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/compare/v0.3.0...v0.3.2
[0.3.0]: https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/releases/tag/v0.2.0
