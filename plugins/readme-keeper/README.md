# readme-keeper (Claude Code plugin)

Keep a public repository's README **high-quality and honest**. One skill,
`/readme`, that audits and maintains the document a project is judged by — before
a release, or any time the README and reality have drifted apart.

A README is a contract: every claim in it — version, install command, link, badge
— is implicitly promised true. README *rot* is when reality moves and the README
doesn't. This plugin treats that drift as a bug.

## The skill

- `/readme` — establish ground truth (repo name, manifest version/license, real
  infrastructure), audit against a verifiable checklist (content accuracy, link &
  anchor integrity, badge integrity, metadata consistency, style, accessibility,
  freshness), report findings as pass/fail with `file:line` specifics, then fix to
  the cognitive funnel and re-verify.

## The honesty gate

The rule above all others: **never show a signal you cannot back.** No CI badge
without a workflow, no version badge a release will outdate, no community badge
without a live invite, no "used by" without real users. A broken or dishonest
badge signals neglect — worse than no badge. When in doubt, drop it.

## Install

```
/plugin marketplace add GiustoPiedimonte/agentic-engineering-marketplace
/plugin install readme-keeper@giusto-agentic
```

After install, `/readme` is available as a command.

## Usage

```
/readme                 # audit README.md, report ranked findings, offer to fix
/readme fix             # audit then apply the high-quality structure + fixes
/readme audit docs/X.md # report only, on a specific file
```

The audit uses portable `git` / `curl` / `grep` checks (no installs required) and
will use `lychee`, `markdownlint`, or `cspell` if they happen to be present. See
[`README_CHECKLIST.md`](skills/readme/references/README_CHECKLIST.md) for the full
checklist, the section-order funnel, badge link-target conventions, and the top
README-rot failure modes with their detection.
