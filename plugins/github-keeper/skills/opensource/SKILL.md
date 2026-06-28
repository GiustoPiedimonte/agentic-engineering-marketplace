---
name: opensource
description: >
  This skill should be used to make a repository a well-made public/open-source
  project. Trigger with "make this repo public-ready", "set up open source",
  "add a code of conduct / contributing / security policy", "add issue and PR
  templates", "add CI", "fix the repo settings", or "get this ready to share".
  Adds the community-health files, an honest CI gate, and the right repo settings
  — honesty-first, and never flips a repo public or changes settings without
  explicit confirmation.
metadata:
  version: "0.3.0"
---

# /opensource — make a repository well-made and public-ready

A public repo is judged on more than its README: the community-health files, an
honest CI signal, a security policy, and sane settings are what make it a project
people trust and can contribute to. This skill establishes the gap and closes it.
`$ARGUMENTS` is the target repo (default: the current one).

Two gates govern everything:

- **Outward/irreversible actions need explicit confirmation.** Making a repo
  public, creating a release, changing visibility or settings, and pushing are
  outward — confirm first. **Never flip a repo to public without the human saying
  so.**
- **Contact details are the human's call.** A Code of Conduct and a Security
  policy need a reporting channel — ask; don't expose a personal email by default.
  The privacy-preserving default is GitHub's private vulnerability reporting.

## Process

1. **Establish ground truth — read, don't assume.** Is it a GitHub repo? Public
   or private? Pull the community profile and existing files/settings, and detect
   the repo type (it drives the CI check and the install docs). See
   `references/OSS_PLAYBOOK.md`.

2. **Report the gap, then confirm the plan.** Present present-vs-missing against
   the checklist, split into **files** (safe, in-repo) and **settings / outward
   actions** (need confirmation). Ask the two questions: contact method, and
   whether to add CI. Don't generate until the plan is agreed.

3. **Generate the community-health files** from `references/templates/`, filling
   placeholders (`{{OWNER}}`, `{{REPO}}`, `{{PROJECT}}`, `{{CONTACT}}`,
   `{{VALIDATE_COMMAND}}`). Match the repo's voice. If a file already exists,
   improve it instead of overwriting — and gate a big rewrite on confirmation
   (same rule as `/readme`).

4. **Add an honest CI gate.** Commit `.github/workflows/validate.yml` running the
   repo's real, deterministic check (tests/lint for a code repo; a structure/link
   validation script for a markdown/config repo). Only *after* it exists, add the
   CI badge — never a CI badge without a workflow.

5. **Apply repo settings (with confirmation).** Via `gh`: issues on,
   wiki/projects off unless used, delete-branch-on-merge, enable private
   vulnerability reporting, and sync description/topics to match the README. Don't
   impose branch protection on a solo repo.

6. **Hand the README to `/readme`.** README quality is that skill's job — invoke
   it to audit/elevate rather than duplicating the work here.

7. **Verify, don't assert.** Re-check: community-profile health (aim 100%), CI run
   green, badges not `unknown`, About matches the README one-liner, license agrees
   across README/LICENSE/manifest. Show the output.

## What to add only if real
CI badge → only with a workflow. Security policy → only with a working reporting
channel (enable private reporting first). License → ask which one; never assume.
Topics → true and searchable. Branch protection → suggest, don't force. Never
fabricate a contact, a guarantee, or adoption.

## Output
The gap report (present vs missing), the files generated, the settings changed
(each confirmed), the CI result, and the final community-profile health — with the
verification output, not assertions.
