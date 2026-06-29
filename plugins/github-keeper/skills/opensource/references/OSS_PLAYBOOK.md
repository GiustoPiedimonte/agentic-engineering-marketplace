# Open-source readiness playbook

Make a repository a *well-made* public project: the community-health files, an
honest CI gate, and the repo settings that should actually be there — no more, no
less. Same honesty gate as the rest of this plugin: never add a signal the repo
can't back, and never fabricate a contact, a guarantee, or a check.

The reference for "done well" is this marketplace's own repo: it sits at GitHub
community-health **100%** with a green CI gate and private vulnerability reporting.

## The two hard gates

1. **Outward/irreversible actions need explicit human confirmation.** Making a
   repo public, creating a GitHub release, changing visibility or settings, and
   pushing are outward actions — confirm before doing them. **Never flip a repo to
   public without the human explicitly saying so.**
2. **Contact details are the human's call.** A Code of Conduct and a Security
   policy need a reporting channel. Don't guess or expose a personal email by
   default — ask. The privacy-preserving default is GitHub's *private
   vulnerability reporting* (no address exposed).

## Step 1 — Establish ground truth

- Is it a git repo with a GitHub remote? Public or private? (`gh repo view`)
- Current community profile and gaps (`gh api repos/{owner}/{repo}/community/profile`).
- What already exists: `LICENSE`, `README.md`, `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md`, `SECURITY.md`, `.github/` templates, `.github/workflows/`.
- Repo type (drives the CI check and the install docs): detect stack/package
  manager as in `../../readme/references/ELEVATE_PLAYBOOK.md`.
- Existing settings: issues, wiki, projects, discussions, delete-branch-on-merge,
  description, topics, license.

## Step 2 — Report the gap, then confirm the plan

List present vs missing against the checklist below. Group the work into
**files** (safe, in-repo) and **settings / outward actions** (need confirmation).
Confirm contact method and CI choice before generating anything.

## Step 3 — Community-health files

Generate from `templates/`, filling placeholders (`{{OWNER}}`, `{{REPO}}`,
`{{PROJECT}}`, `{{CONTACT}}`, `{{VALIDATE_COMMAND}}`). Match the repo's voice; if a
file already exists, improve it rather than overwrite (and gate big rewrites on
confirmation, per the `/readme` rule).

| File | Purpose | Notes |
|---|---|---|
| `LICENSE` | legal reuse terms | if absent, ask which license (don't assume) |
| `README.md` | the front door | hand off to the `/readme` skill to audit/elevate |
| `CONTRIBUTING.md` | how to contribute + how to validate | real validate command |
| `CODE_OF_CONDUCT.md` | behavior standard + reporting | Contributor Covenant 2.1; `{{CONTACT}}` |
| `SECURITY.md` | disclosure policy | default: GitHub private reporting |
| `.github/ISSUE_TEMPLATE/*` | bug + feature forms + `config.yml` | `config.yml` links security privately |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR checklist | mirror the repo's real checks |
| `.gitignore` | ignore OS/editor/build cruft | only entries that apply |

## Step 4 — Honest CI gate

A CI badge is only honest if a workflow exists and means something. Add
`.github/workflows/validate.yml` running the repo's **real, deterministic** check:

- code repo → its test + lint command (`npm test`, `pytest`, `cargo test`, …);
- markdown/JSON/config repo → a validation script (manifests parse, structure
  holds, README links resolve). Keep it network-free so the badge isn't flaky.

Only after the workflow is committed, add the CI badge (linking to the workflow).
Verify it doesn't render `unknown`.

### If the repo is itself a distributable package/plugin

Document **how users get updates** — it's part of being well-made, and easy to
forget. State the project's release/versioning convention and, crucially, how an
installed user stays current (e.g. for a Claude Code plugin marketplace: users
don't auto-update by default — tell them they can enable per-marketplace
auto-update for hands-off updates + reload notifications, or pull manually). Pair
it with a `CHANGELOG.md` and versioned releases so an "update available" actually
means something. Bumping the version on each release is what makes update
detection work at all.

## Step 5 — Repo settings (with confirmation)

Apply via `gh`, confirming outward changes:

- `gh repo edit {owner}/{repo} --enable-issues --delete-branch-on-merge` — issues
  on, tidy merges.
- `gh repo edit … --enable-wiki=false --enable-projects=false` — off unless used.
- Sync metadata: `--description "<one-liner matching the README>"` and
  `--add-topic …` (real, searchable topics).
- Enable private vulnerability reporting:
  `gh api --method PUT repos/{owner}/{repo}/private-vulnerability-reporting`.
- License/description/topics should agree with the README and manifest.
- Branch protection on `main` is optional; suggest it for multi-maintainer repos,
  don't impose it on a solo project.

## Step 6 — Verify, don't assert

- Community profile health (`…/community/profile` → `health_percentage`) — aim 100%.
- CI run is green (`gh run list`).
- CI/badge targets resolve and aren't `unknown`.
- README one-liner matches the GitHub `About`; license agrees across README,
  `LICENSE`, manifest.

## Checklist (GitHub community profile + beyond)
- [ ] Description (About) set and matches the README one-liner
- [ ] README present and high-quality (`/readme`)
- [ ] LICENSE present (SPDX), agrees everywhere
- [ ] CODE_OF_CONDUCT.md with a real reporting channel
- [ ] CONTRIBUTING.md with the real validate command
- [ ] SECURITY.md (private reporting enabled)
- [ ] Issue templates + PR template
- [ ] CI workflow + honest CI badge
- [ ] Settings: issues on, wiki/projects off unless used, delete-branch-on-merge
- [ ] Topics set (searchable, true)
- [ ] If distributable (package/plugin): update/versioning story documented + CHANGELOG
