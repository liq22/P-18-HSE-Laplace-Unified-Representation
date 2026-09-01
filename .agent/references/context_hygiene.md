# Context Hygiene

Context management must reduce work, not become work.

## Default read budget

For one task, read:

- one primary Skill;
- at most one supporting Skill or tool;
- the target file or subsystem;
- only the sources, configs, tests, or results needed for the decision.

Read `paper/paper.yaml` only when stage, active source, claim state, or author approval changes the action. Do not begin a bounded task with a repository-wide scan.

## Source priority

Use direct, current information first:

1. target manuscript, code, experiment, figure, or submission file;
2. completed results and verified original sources;
3. current method, config, data, and protocol;
4. concise supporting records;
5. temporary notes only after verification.

Ignore stale drafts, unrelated logs, generated wrappers, and the full ARIS checkout unless one is the explicit target.

## Product boundary

Internal paths, IDs, state fields, routing choices, and backend details remain internal. They do not become manuscript prose, code comments, captions, or normal user summaries.

A normal response contains the substantive change, direct result, one relevant validation, and one material remaining issue only when present.

## Escalation

Expand context only when the direct attempt exposes a concrete missing dependency. When progress requires unavailable data, credentials, author approval, paid compute, publication, or submission, state the missing action and stop. Do not create a handoff package.

## Boundaries

- No custom context packet for routine tasks.
- No whole-repository scan for a bounded product change.
- No Python context inventory, token accounting, or proof-of-work report.
- No manifest, hash, receipt, or blocker package.
- No repeated rereading or validation without a changed product.
