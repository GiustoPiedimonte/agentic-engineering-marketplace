# Changelog

All notable changes to this marketplace and its plugins are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
plugin versions follow [Semantic Versioning](https://semver.org).

## [Unreleased]

## [0.5.0] - 2026-07-29

### Added
- **agentic-engineering — the right-size gate** (0.4.0): `/ship` opens with a new
  §0 that asks whether the cycle is warranted *at all*, before the pre-spawn
  filter asks who should run it. Severity × reversibility — the rule the practice
  already applies to what an agent may do alone — turned on the process itself:
  small and reversible gets done directly, wide or hard to undo earns the full
  cycle. A process that has proved itself starts to feel free, and it isn't;
  three contexts plus the human attention to arbitrate them is the bill.
- **agentic-engineering — `path:line` verification hook** (0.4.0): a PostToolUse
  hook that checks the `file:line` references it can resolve in written markdown.
  Deliberately conservative — it reports only references whose path resolves on
  disk and whose line is out of range or blank, so a clean run is silent and a
  report is never a guess. Paths that don't resolve (examples, other repos,
  planned files), absolute paths, line numbers over six digits, and refs
  immediately followed by a word character, `.` or `-` are skipped rather than
  flagged: it is a floor on correctness, not a proof of it. Needs
  `python3`; silently inert without it. Covered by `scripts/test_verify_refs.py`
  in the same CI gate — this is the plugin's own advice applied to itself, and a
  checker no command checks would be the exact defect it exists to catch.
- **agentic-engineering — scope sizing and reader fan-out in `/ship`** (0.4.0):
  three defects found using the skill on a real cycle. A pitch slice is not a PR
  slice (`/pitch` carves conceptual slices worth two to four PRs each, and serial
  reliability compounds at roughly 0.85 per step); the readers are the half that
  gets skipped, so the substrate inventory belongs in `/graph` *before* the writer
  is spawned; and a delegated writer is judged by its branch, not by its silence.

### Changed
- **agentic-engineering — `/ship` is user-invoked only** (0.4.0): the skill now
  sets `disable-model-invocation: true`. A cycle spawns a writer and opens a PR,
  which is the archetype the field exists for — you decide when it starts, not
  the model reading your code and concluding it looks ready. Its description also
  leaves every session's context as a side effect.
- **agentic-engineering — a reviewer is not an oracle** (0.4.0): `/ship` §3 now
  states where adversarial review belongs (scope, blast radius, whether this was
  the decision to make) and where it doesn't (anything a command can settle).
  Adding a second and third reviewer to a verifiable claim buys correlated
  agreement, not coverage; when a review keeps catching the same class of defect,
  that is a check waiting to be written.

## [0.4.0] - 2026-07-23

### Added
- **agentic-engineering — graph engineering** (0.3.0): a new `/graph` skill that
  turns a straight-line task into an execution graph — fan out independent work
  across a fleet of subagents, verify findings, and converge — built on dynamic
  workflows (coordination costs zero model tokens). Ships `GRAPH_MODEL.md` (the
  node/edge grammar, the diamond/router/verifier/cycle topologies, the five
  graphs, topology-first principles) and a copy-ready `WORKFLOW_LIBRARY.md` with
  six starter scripts (security-sweep, pr-review, cited-research, consistency-sweep,
  ecosystem-scan, discovery-until-dry). Adds a general **`verifier`** agent (a
  single-claim adversarial node, fan-out safe) alongside the PR-level `reviewer`.
  `/pitch` now names the **graph** a piece of work touches and its **gated edges**
  (severity×reversibility) before any code. See ADR-002.

### Changed
- **github-keeper `/readme` — the fidelity gate** (0.4.0): elevate now derives the
  hero archetype (typographic / screenshot / diagram / terminal-card / **none**),
  palette, voice, badges, and sections from the **target project's own identity**
  and **proposes-and-confirms** before generating — instead of imposing our
  terminal-card house style. Adds an **adaptive proposal set** (badges/links/sections
  from the project + maintainer) and **free-form intent** edits ("do just this").
  Our `assets/banner.svg` is now one archetype example, not the template. See
  ADR-001. (skill 0.3.0)

## [0.3.3] - 2026-06-29

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

[Unreleased]: https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/compare/v0.3.3...v0.4.0
[0.3.3]: https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/compare/v0.3.0...v0.3.2
[0.3.0]: https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/GiustoPiedimonte/agentic-engineering-marketplace/releases/tag/v0.2.0
