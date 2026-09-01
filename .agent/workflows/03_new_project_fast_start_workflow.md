# 03 New Project Fast Start Workflow

Goal: convert a rough direction into auditable state without generating
unsupported prose.

```text
direction open
  new_project_intake.yaml
  + idea_candidates.yaml
→ Card 1A generate
→ Card 1B formalize one
→ Card 1C G1–G5 + human approval
→ Card 1 migrate to project.yaml / paper.yaml

direction fixed
  new_project_intake.yaml
→ Card 1 migrate directly

then
  Card 3 literature
→ Card 2 claim–evidence
→ Card 4 experiments
→ Card 5 figures/tables
→ story spine + paragraph map
→ Card 6 drafting
```

## File roles

| File | Role | Not allowed |
|---|---|---|
| `new_project_intake.yaml` | one-page intake | long candidate database |
| `idea_candidates.yaml` | progressive-disclosure candidate workspace | evidence or manuscript claims |
| `story_spine.md` | narrative scaffold | unsupported prose |
| `minimum_viable_paper_plan.md` | temporary planning | canonical scientific truth |
| `08_fast_paper_gate.md` | pre-draft gate | subjective checking without ledger evidence |

## Invariants

- Unknowns remain `TODO`/`unknown`.
- Candidate ideas do not enter `paper.yaml` before explicit promotion approval.
- Literature, runs, figures, and tables enter their matrices/ledgers before
  drafting.
- Planned or failed runs are never positive evidence.
- Each action uses one card, one primary skill, and one canonical output.
- Human gates are never auto-approved.
