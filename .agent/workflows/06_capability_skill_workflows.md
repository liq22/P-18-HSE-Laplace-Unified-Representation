# 06 Capability Skill Workflows

Capability skills help the selected primary create the requested product. They do
not replace the primary with another plan, review, record, or process layer.

## High-value placements

| Capability | Usually supports | Primary product effect |
|---|---|---|
| `scientific-brainstorming` | Card 1A | structurally distinct idea candidates |
| `hypothesis-generation` | Card 1B | competing mechanisms and decisive test |
| `literature-review` / lookup tools | Card 3 | literature map or verified source support for a target section |
| `code-change` + ML/data tools | Card 4I | executable source and relevant tests |
| `experimental-design` / statistics | Card 4E | executable protocol, metrics, and actual results |
| `scientific-visualization` / schematics | Card 5 | actual figure/table asset and caption |
| `scientific-writing` | Card 6 | one domain-native manuscript section |
| `citation-management` | explicit citation task | corrected citations and BibTeX |
| `peer-review` / critical thinking | explicit review task | concrete findings, not default support for creation |
| document tools | bounded file task | converted or edited document |
| `repository-self-evolution` | Card 9 | approved repository change or explicit plan_only output |

## Code distinction

```text
understand existing code -> code-module-xray -> MODULE_MAP
implement/fix/refactor code -> code-change -> source + tests
```

Do not use comprehension output as completion for implementation.

## Experiment distinction

```text
execute experiment -> 06-experiment-ops -> results + metrics
independently inspect experiment -> 07-experiment-audit -> findings
```

Do not attach independent audit automatically to every run.

## Figure distinction

```text
plan figure -> design + caption draft
produce figure -> actual asset + editable source + caption
check figure -> corrected asset or concrete findings
```

A manifest is a supporting record, not the generated figure.

## Language boundary

Capability tools may use internal records and IDs while working. Their product
must use the register of the target surface:

- academic language for manuscript and captions;
- engineering language for source code and comments;
- protocol/result language for experiment summaries;
- governance language only for explicit governance tasks.

## Safety

External network, paid compute, credentials, remote writes, or submission require
operation-specific authorization and `14-agent-safety`. A safety pass returns to
the selected product task and does not become the final output.