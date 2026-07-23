# Workflow library — copy-ready graph scripts

Six starter graphs for the dynamic **Workflow tool**. Each is a plain-JavaScript
orchestration script: it spawns a coordinated fleet of subagents, and the
coordination costs zero model tokens because it's code, not conversation. Save a
script into `.claude/workflows/<name>.js` to run it by name and version it in the
repo; or hand it to `/graph` as a starting point and adapt.

API in one paragraph: `agent(prompt, {schema, label, phase, model, isolation})`
runs one node (with a JSON `schema` it returns validated data). `parallel(thunks)`
is a barrier — runs all, waits for all, a failed thunk becomes `null` (so
`.filter(Boolean)`). `pipeline(items, stage1, stage2, …)` streams each item through
all stages with no barrier (the default — fastest wall-clock). `phase(title)` groups
progress; `log(msg)` narrates. The reduce between stages is plain code — zero tokens.

---

## 1. Security sweep — diamond + verify (breadth one context can't hold)

```javascript
export const meta = {
  name: 'security-sweep',
  description: 'One agent per file/route hunts a class of bug; verify each finding.',
  phases: [{ title: 'Find' }, { title: 'Verify' }],
}
const FINDING = { type:'object', additionalProperties:false,
  properties:{ file:{type:'string'}, line:{type:'number'}, issue:{type:'string'},
    severity:{type:'string', enum:['high','medium','low']} },
  required:['file','issue','severity'] }
const VERDICT = { type:'object', properties:{ real:{type:'boolean'}, why:{type:'string'} }, required:['real'] }

// args = array of file paths to audit (scout them inline first, then pass in)
const files = args
const results = await pipeline(
  files,
  f => agent(`Audit ${f} for missing authorization / injection / secret leaks. Report findings.`,
        { label:`find:${f}`, phase:'Find', schema:{ type:'object', properties:{ findings:{type:'array', items:FINDING} }, required:['findings'] } }),
  (r, f) => parallel((r?.findings||[]).map(bug => () =>
        agent(`Adversarially verify this is a REAL vulnerability, default real=false if unsure: ${JSON.stringify(bug)}`,
          { label:`verify:${bug.file}:${bug.line}`, phase:'Verify', schema:VERDICT })
          .then(v => ({ ...bug, verdict:v })))),
)
const confirmed = results.flat().filter(Boolean).filter(x => x.verdict?.real)
return { confirmed, scanned: files.length }
```

---

## 2. PR review — router on diff size (judgment at the node, branch in code)

```javascript
export const meta = {
  name: 'pr-review',
  description: 'Route on diff size: small → one pass; large → parallel audit + judge.',
  phases: [{ title: 'Classify' }, { title: 'Review' }],
}
// args = { diff: '<unified diff>', files: ['a.ts', ...] }
const { severity } = await agent(`Classify this diff's risk as low or high:\n${args.diff}`,
  { phase:'Classify', schema:{ type:'object', properties:{ severity:{enum:['low','high']} }, required:['severity'] } })

let review
if (severity === 'high') {
  const lenses = ['correctness','security','contracts/invariants']
  review = await parallel(lenses.map(lens => () =>
    agent(`Review this diff through the ${lens} lens. Default to skepticism; report only real gaps with file:line.\n${args.diff}`,
      { label:`review:${lens}`, phase:'Review' })))
  review = await agent(`You are the judge. Synthesize a MERGE/ADJUST/REJECT verdict from these lens reviews:\n${JSON.stringify(review)}`,
      { phase:'Review' })
} else {
  review = await agent(`Quick adversarial pass on this small diff — MERGE/ADJUST/REJECT with file:line.\n${args.diff}`, { phase:'Review' })
}
return { severity, review }
```

---

## 3. Cited research — scope → parallel search → verify → synthesize

```javascript
export const meta = {
  name: 'cited-research',
  description: 'Decompose a question, search angles in parallel, verify claims, synthesize.',
  phases: [{ title:'Scope' }, { title:'Search' }, { title:'Verify' }, { title:'Synthesize' }],
}
// args = the research question (string)
const { angles } = await agent(`Decompose into 4-6 distinct research angles: ${args}`,
  { phase:'Scope', schema:{ type:'object', properties:{ angles:{type:'array', items:{type:'string'}} }, required:['angles'] } })

const found = (await parallel(angles.map(a => () =>
  agent(`Research this angle with current sources; return claims with URLs: ${a}`,
    { label:`search:${a.slice(0,24)}`, phase:'Search',
      schema:{ type:'object', properties:{ claims:{ type:'array', items:{ type:'object',
        properties:{ claim:{type:'string'}, url:{type:'string'} }, required:['claim','url'] } } }, required:['claims'] } })
))).filter(Boolean).flatMap(r => r.claims)

const verified = (await parallel(found.map(c => () =>
  agent(`Try to refute this claim from its source. Keep only if it holds: ${JSON.stringify(c)}`,
    { label:'verify', phase:'Verify', schema:{ type:'object', properties:{ holds:{type:'boolean'} }, required:['holds'] } })
    .then(v => v?.holds ? c : null)))).filter(Boolean)

return await agent(`Write a cited synthesis answering "${args}" from these verified claims:\n${JSON.stringify(verified)}`,
  { phase:'Synthesize' })
```

---

## 4. Cross-source consistency sweep — the "continuity" diamond

```javascript
export const meta = {
  name: 'consistency-sweep',
  description: 'Fan out over sources of truth, find contradictions, converge on one report.',
  phases: [{ title:'Read' }, { title:'Reconcile' }],
}
// args = [{ key:'board', prompt:'read TASKS.md and summarize open commitments' }, ...]
const CLAIMS = { type:'object', properties:{ claims:{ type:'array', items:{ type:'object',
  properties:{ subject:{type:'string'}, statement:{type:'string'}, source:{type:'string'} },
  required:['subject','statement','source'] } } }, required:['claims'] }

const perSource = (await parallel(args.map(s => () =>
  agent(s.prompt + ' Return atomic claims with subject+statement+source.',
    { label:`read:${s.key}`, phase:'Read', schema:CLAIMS })))).filter(Boolean).flatMap(r => r.claims)

// reduce is plain code, then one barrier node that needs the whole set to spot conflicts
const contradictions = await agent(
  `These claims come from different sources of truth. List only genuine contradictions (same subject, incompatible statements), each with the two sources:\n${JSON.stringify(perSource)}`,
  { phase:'Reconcile', schema:{ type:'object', properties:{ conflicts:{type:'array', items:{type:'object',
      properties:{ subject:{type:'string'}, a:{type:'string'}, b:{type:'string'} }, required:['subject','a','b'] } } }, required:['conflicts'] } })
return { sources: args.length, ...contradictions }
```

---

## 5. Ecosystem scan — scheduled, rank by impact at a barrier

```javascript
export const meta = {
  name: 'ecosystem-scan',
  description: 'Check dependencies/sources in parallel, rank by impact, write a digest.',
  phases: [{ title:'Scan' }, { title:'Rank' }],
}
// args = [{ name:'langgraph', prompt:'check latest release + breaking changes' }, ...]
const items = (await parallel(args.map(d => () =>
  agent(d.prompt + ` for "${d.name}". Report version, notable changes, and whether action is needed.`,
    { label:`scan:${d.name}`, phase:'Scan', model:'haiku',
      schema:{ type:'object', properties:{ name:{type:'string'}, version:{type:'string'},
        change:{type:'string'}, actionNeeded:{type:'boolean'} }, required:['name','actionNeeded'] } })
))).filter(Boolean)
// barrier is correct here: rank needs the whole set
const digest = await agent(`Rank these by impact and write a short digest; flag anything needing a deliberate update:\n${JSON.stringify(items)}`,
  { phase:'Rank' })
return { digest, checked: items.length }
```

---

## 6. Discovery until dry — a cycle that converges

```javascript
export const meta = {
  name: 'discovery-until-dry',
  description: 'Loop finders until K empty rounds; dedupe against everything SEEN.',
  phases: [{ title:'Discover' }],
}
const BUGS = { type:'object', properties:{ bugs:{ type:'array', items:{ type:'object',
  properties:{ id:{type:'string'}, desc:{type:'string'} }, required:['id','desc'] } } }, required:['bugs'] }
const FINDERS = args // array of { prompt } finder specs
const seen = new Set(), confirmed = []
let dry = 0
while (dry < 2) {                                  // stop after 2 empty rounds
  const found = (await parallel(FINDERS.map(f => () =>
    agent(f.prompt, { phase:'Discover', schema:BUGS })))).filter(Boolean).flatMap(r => r.bugs)
  const fresh = found.filter(b => !seen.has(b.id)) // dedupe vs SEEN, not confirmed
  if (!fresh.length) { dry++; continue }
  dry = 0
  fresh.forEach(b => seen.add(b.id))
  const judged = await parallel(fresh.map(b => () =>
    agent(`Is this a real, actionable finding? Default false if unsure: ${b.desc}`,
      { phase:'Discover', schema:{ type:'object', properties:{ real:{type:'boolean'} }, required:['real'] } })
      .then(v => ({ b, real: !!v?.real }))))
  confirmed.push(...judged.filter(j => j.real).map(j => j.b))
  log(`${confirmed.length} confirmed, ${seen.size} seen`)
}
return { confirmed }
```

---

## Governance note (for consequential graphs)

These templates read and analyze — safe to self-route. A graph that *acts on the
world* (writes data, sends messages, changes state) keeps the action explicit and
behind the human gate (see `/ship` §4): the gate is a conditional edge, and every
acting node should project a row into the audit graph. Never let a self-routing
research graph grow an edge that takes a consequential action without a gate.
