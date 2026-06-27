# giusto-agentic — Claude Code plugin marketplace

A public marketplace exposing the **agentic-engineering** plugin: a spec-driven
shape → decide → execute → measure → eval workflow (`/pitch`, `/adr`, `/ship`,
`/measure`, `/eval`) with executor / researcher / reviewer / measurer subagents
and verification hooks.

## Install (for anyone)

In Claude Code:

```
/plugin marketplace add GiustoPiedimonte/agentic-engineering-marketplace
/plugin install agentic-engineering@giusto-agentic
```

That's it — `/pitch` `/adr` `/ship` `/measure` `/eval` and the four agents become
available. (CLI equivalent: `claude plugin marketplace add GiustoPiedimonte/agentic-engineering-marketplace`
then `claude plugin install agentic-engineering@giusto-agentic`.)

## Publish (one-time)

1. Create a **public GitHub repo**, e.g. `agentic-engineering-marketplace`.
2. Copy this folder's contents to the repo root (keep the layout below).
3. Commit and push to `main`.
4. Share the install commands above. Updates: bump `version` in
   `plugins/agentic-engineering/.claude-plugin/plugin.json` and in
   `.claude-plugin/marketplace.json`, push — users get them on
   `/plugin marketplace update giusto-agentic`.

## Layout

```
agentic-engineering-marketplace/
├── .claude-plugin/
│   └── marketplace.json        # lists the plugin(s), schema-validated
├── plugins/
│   └── agentic-engineering/    # the plugin itself
│       ├── .claude-plugin/plugin.json
│       ├── skills/  agents/  hooks/  README.md
└── README.md
```

To host multiple plugins from one repo, add more folders under `plugins/` and
list each in `marketplace.json`'s `plugins` array.

## Notes

- The plugin's format hook needs `jq` on the user's machine.
- For the `researcher`/`/measure` to pull live library docs, connect a docs MCP
  (e.g. Context7): `claude mcp add context7 -- npx -y @upstash/context7-mcp`.
- Schema reference: https://code.claude.com/docs/en/plugin-marketplaces
