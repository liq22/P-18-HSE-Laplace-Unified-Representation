# awesome-ai-research-writing Adoption Notes

This note records how this repository absorbs useful workflow ideas from `Leey21/awesome-ai-research-writing` without copying its prompt library verbatim.

## Reference checked

- Repository: `https://github.com/Leey21/awesome-ai-research-writing`
- Checked file: `README.md`
- Observed focus: practical prompt templates, approachable skill usage, OpenSkills/Cursor/Claude workflow, paper writing, translation/polish, figure/table titles, experiment analysis, reviewer-style review, humanizer, doc coauthoring, and concept/canvas design.

## Adopted ideas

| Observed pattern | Local equivalent | Local rule |
|---|---|---|
| Copy-ready writing prompts | `QUICKSTART_NEW_PROJECT.md`, `.agent/workflows/`, selected skills | Users should not need to remember prompt engineering; they should state the task and let router produce a context packet. |
| Skills tutorial for Cursor/Claude | `README.md`, `AGENTS.md`, `.agent/README.md` | Onboarding must show exact files to read, exact commands, and example agent prompts. |
| Chinese-English / LaTeX / Word polish prompts | `10-language-polish`, `docx`, `09-tex-freeze-formalize` | Translation/polish must preserve scientific meaning, active source, and format target. |
| Humanizer / remove AI smell | `10-language-polish` | Remove mechanical style only after evidence is stable; never alter claim strength. |
| Figure/table title and caption prompts | `15-figure-table-design`, `scientific-visualization` | Captions/titles must bind to claim, evidence, source artifact, and first callout. |
| Experiment-analysis prompt | `07-experiment-audit`, `statistical-analysis`, `08-markdown-draft` | Experimental analysis must be based on registered runs and statistics, not raw pasted numbers alone. |
| Reviewer-perspective prompt | `peer-review`, `scientific-critical-thinking`, `13-reviewer-response` | Reviewer simulation becomes a gate with actionable P0/P1/P2 issues. |
| Doc coauthoring staged flow | `08-markdown-draft`, `paper/draft/00_paragraph_map.md` | Drafting should proceed by section/paragraph contracts rather than all-at-once prose. |
| Concept/canvas design | `15-figure-table-design`, `scientific-schematics`, `markdown-mermaid-writing` | Concept figures are allowed only when separated from evidence/data figures. |

## Deliberate non-adoption

- Do not copy large prompt blocks into this repo; they create prompt drift and dirty context.
- Do not treat model rankings or tool preference claims as stable repo facts.
- Do not introduce OpenSkills as a hard dependency; this repo already maintains `.agent/skills` plus generated `.claude`/`.codex` wrappers.
- Do not let prompt-style shortcuts bypass `reading_matrix.md`, `evidence_matrix.md`, `run_ledger.md`, figure/table manifests, or human gates.

## Skill-system updates implied

1. `10-language-polish` should explicitly support target modes: LaTeX English, Word English, Chinese academic prose, direct translation, and AI-smell cleanup.
2. `ROUTING_MATRIX.md` should route translation, humanization, figure/table title, experiment analysis, reviewer review, and Word template tasks to the correct local skills.
3. Onboarding docs should show copy-ready user prompts, but these prompts should invoke router/context hygiene rather than bypass local contracts.
4. `NOTICE.md` should attribute this repository as workflow inspiration only, with no verbatim prompt import.
