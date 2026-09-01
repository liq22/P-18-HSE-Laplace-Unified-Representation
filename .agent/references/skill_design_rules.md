# Skill Design Rules

## Minimal skill contract

Every canonical `.agent/skills/<name>/SKILL.md` needs YAML frontmatter with:

```yaml
name: <directory-name>
description: <when to use the skill and what usable product it changes>
```

The body needs only four substantive sections:

1. `## Purpose`
2. `## Workflow`
3. `## Output Contract`
4. `## Boundaries`

Add `Use When`, `Required Inputs`, `Validation`, `Stop With`, `References`, or
examples only when they clarify real behavior. Do not add empty sections to
satisfy a template. Section order, description length, example count, and a
`paper/` path reference are not quality criteria.

## Content-first rule

The first operational step of every skill must work on the requested content or
behavior. A normal skill follows:

```text
inspect the minimum necessary context
-> modify or produce the primary product
-> run one direct check
-> stop
```

Do not begin with formatting, report generation, checklist completion, matrix
maintenance, Python scans, broad repository validation, or process narration.

## Primary product

A skill's primary product is one of:

- manuscript reasoning or prose;
- source code behavior and relevant tests;
- experiment output and interpretation;
- figure/table asset and caption;
- submission material;
- a concrete research decision;
- governance only when explicitly requested.

Supporting records may be updated once when the product makes them stale. They do
not replace the product.

## Content before form

Use this priority:

```text
correctness and scientific substance
-> argument or implementation structure
-> reader/user clarity
-> minimum necessary formatting
```

Formatting or stylistic refinement may be primary only when explicitly requested.
Never add headings, tables, prose, visual decoration, or formal process merely to
make an output appear complete.

## Python and tool use

Use Python or another tool only when it directly creates or tests the product:
implementation, statistics, experiments, data processing, plotting, targeted
regression tests, compilation, or requested file generation.

Do not use Python to count document features, score prose, check routine Markdown,
generate proof-of-work reports, calculate hashes, or enumerate hypothetical edge
cases. For writing, direct reading and source verification are usually the right
checks.

## No custom integrity layer

Skills must not request or generate:

- SHA-256 or other file hashes;
- artifact or tree digests;
- hash chains or receipts;
- custom manifest integrity checks;
- cryptographic proof language.

Research reproducibility uses understandable fields: code version, config, data
version, command, seed, environment, metric, output path, and date.

## Validation rule

Validation answers one question:

> What is the smallest check that directly tests the changed product?

Examples:

- manuscript: reread target and adjacent context; verify changed citations/numbers;
- code: closest targeted test;
- experiment: inspect actual outputs and primary metrics;
- figure/table: open asset and check data, labels, units, caption, readability;
- LaTeX: one compile;
- skill/validator rule: affected validator or behavior case.

Do not copy a full repository command block into every skill. The complete suite
runs once during final PR review.

## Corner-case threshold

Defensive logic or tests are justified only for an observed bug, common user
error, or high-impact failure affecting scientific conclusions, data, credentials,
cost, publication, or remote work. Do not encode every theoretically possible
state combination.

## Audit and safety

Audit skills are explicit primaries and report only decision-changing findings.
Safety middleware is limited to credentials/private-data egress, paid remote
compute, destructive remote writes, publication, and submission. Routine local
work proceeds directly.

## Language boundary

Internal IDs, paths, state fields, approvals, and backend details are consumed
silently. Product outputs use the vocabulary of the target discipline or
programming environment.

## Behavioral evaluation

Evaluate whether:

- the requested product changed;
- content work preceded formatting and validation;
- one direct validation was used;
- governance-only work was not accepted as product completion;
- audit was not inferred without explicit intent;
- custom hashes and low-value corner-case defenses were absent.
