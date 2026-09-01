# scientific-agent-skills — upstream source reference

This page records the provenance of the capability skills ported into this repo's
`.agent/skills/` directory. It exists for traceability: the upstream project releases
frequently, so the port is pinned to a specific tag/commit rather than `main`.

## Upstream

- Repository: https://github.com/K-Dense-AI/scientific-agent-skills
- Description: "Turn any AI agent into an AI Scientist" — a library of ~148 scientific
  agent skills (Agent Skills standard; compatible with Cursor, Claude Code, Codex, …).
- Upstream repo license: MIT.
- Pinned ref: **`v2.53.0`** (latest tag at port time, released 2026-06-23).
- Resolved commit: `9c9bd2e92af12311ecd0c1a643e0931643f9ea04`
  (also recorded verbatim in `scientific_agent_skills_upstream_commit.txt` alongside this file).
- Port date: **2026-07-02**.

## Port mode

**Adapted house-format canonical skills — not a verbatim copy.** For each ported skill:

1. Frontmatter reduced to `name` + `description` only (upstream `allowed-tools`,
   `license`, `metadata`, `required_environment_variables` are stripped).
2. `description` rewritten as a narrow positive trigger + explicit negative trigger
   ("Do not use for …"), 80–350 chars.
3. Body reorganized into this repo's fixed 9-section contract
   (`## Purpose / Use When / Required Inputs / Workflow / Output Contract / Validation /
   Boundaries / Stop With / References`).
4. Outputs/artifacts mapped onto the local `paper/` workspace.
5. Bundled assets copied through an allowlist/denylist (no secrets, no large binaries,
   no heavy-ML executable training scripts).
6. Required upstream env vars (e.g. `OPENROUTER_API_KEY`) demoted to a
   `## Required Inputs` note ("user must provide; never hardcode").

## Tiering (port-local)

Ported skills are classified into three tiers (not equal-weight) — see
`.agent/skills/PORT_MANIFEST.yaml` and `.agent/skills/ROUTING_MATRIX.md`:

- **Core (Tier A)** — default-available, primary capability skills for the single-paper workflow.
- **Tool (Tier B)** — implementation-only supporting skills; invoked by a primary skill, not directly by user intent.
- **External (Tier C)** — depend on external APIs / network / user credentials; strong `Boundaries` + `Stop With`.

## Scope ported (48 skills)

- Paper writing / scientific communication core (14)
- Research methodology (4)
- Data analysis / visualization (11)
- ML / AI (9)
- Document processing / utilities (10)

Per-skill declared licenses are enumerated in `../../../NOTICE.md`.

## Re-port / sync

- Re-generate Claude/Codex wrappers only:
  `bash .agent/scripts/sync_agent_skill_wrappers.sh . both`
- Re-port a skill from a newer upstream ref: change the pin in this file and
  `.agent/references/scientific_agent_skills_upstream_commit.txt`, re-run the adapt
  step for that skill, then re-sync wrappers. Do not mix skills from different upstream refs.

## Known upstream issues carried into the port

- `bgpt-paper-search`: upstream `allowed-tools` vs MCP-search workflow mismatch — local `## Boundaries` notes the caution.
- `pptx-posters`: upstream checklist incomplete — local `## Boundaries` instructs the user to verify the export checklist.
