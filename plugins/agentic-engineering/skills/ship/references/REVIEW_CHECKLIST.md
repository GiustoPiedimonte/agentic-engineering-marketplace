# Adversarial review checklist

The reviewer's default is skepticism: look for the reason NOT to merge. Read-only
on code — report, don't fix. Return a verdict per check plus an overall
MERGE / ADJUST / REJECT, with `file:line` specifics. No "seems ok".

1. **Docs read** — does the PR list the files read before implementing? No list -> reject.
2. **Filters argued** — are simple-is-better and the project conventions actually
   argued, or cosmetic hand-waving?
3. **Root cause vs workaround** — does the change remove the cause, or just move a
   number / suppress a symptom? (Hardcoded value -> const or delete, not "raise the limit".)
4. **Scope** — only what was declared? Zero scope-creep, no unrelated changes,
   no new parallel work smuggled in.
5. **Invariants / schema** — destructive ops avoided (no DROP/delete without a
   caller grep); additive migrations safe and idempotent; project invariants respected.
6. **Undeclared behavior change** — any behavior change not in the pitch -> reject
   (or escalate).
7. **Tests** — green AND actually covering the change (not just plumbing/imports).
   Edge cases named in the pitch have tests.
8. **Security** — injection, secret/credential leaks, unsafe shell/tool usage,
   authz gaps, resource leaks.

Report only gaps that affect correctness or stated requirements. Do not flag
style, and do not recommend extra abstraction or defensive code for impossible
states — that is the over-engineering trap. If the work is sound, say so plainly.
