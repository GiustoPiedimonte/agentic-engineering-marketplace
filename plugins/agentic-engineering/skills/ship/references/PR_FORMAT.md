# Standard PR output format

Every executor PR uses this structure. It makes review fast and makes "done"
verifiable rather than asserted.

```markdown
## Summary
<one paragraph: what this cycle did and why>

## Docs read
- [ ] <file 1 read before implementing>
- [ ] <file 2>
(No list = the PR is rejected. Reading before changing is non-negotiable.)

## Filter check (pre-implementation)
- Simple-is-better: <how the simplest viable approach was chosen>
- Invariants / conventions: <which ones apply and how they were honored>
- Scope: <exactly what was touched; confirm zero scope-creep>

## What was done
- <change 1>
- <change 2>

## Test plan (evidence, not claims)
- [ ] Typecheck clean — <command + result>
- [ ] Build clean — <command + result>
- [ ] Tests: N passed, 0 regressions — <command + result>
- [ ] Lint clean — <command + result>
- Open post-merge verifications (concrete, executable):
  - <query / command to run after deploy, with expected result>

## Merge decision
NO autonomous merge — awaiting human/orchestrator review.

Co-Authored-By: <model> (subagent)
```
