# Claude Wrapper (Home Assistant conversation agent)

Bridges Home Assistant Assist to an official Claude Code CLI session, one per phone call.
Part of the "bel Claude" project (see the Obsidian vault: project-claude-auto-voice).

Not a general-purpose integration: it expects `claude-auto-voice-wrapper` (the sibling
`wrapper-service/`) running on the network, already logged in via `claude login`.

## Install (HACS custom repository)

1. HACS → Integrations → ⋮ → Custom repositories → add this repo URL, category "Integration".
2. Install "Claude Wrapper", restart Home Assistant.
3. Settings → Devices & services → Add integration → "Claude Wrapper" → enter the
   wrapper service's URL (e.g. `http://192.168.1.30:8765`).
4. In the Assist pipeline, set the conversation agent to "Claude".
