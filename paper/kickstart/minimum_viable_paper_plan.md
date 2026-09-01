# Minimum Viable Research-to-Paper Plan

A minimum viable paper is the smallest research loop that can support or reject a
meaningful claim. It is not a quota of claims, references, experiments, figures,
files, or simulated reviewers.

> 中文说明：目标是尽快暴露真实 failure、竞争解释、决定性实验和 claim 边界。简单但可证伪的闭环优于内容很多、机制不清、证据分散的“完整论文”。

## Entry state

Establish only:

```text
Research question
Object / Environment / Observation / Task
Observed failure or unresolved contradiction
Current strongest result
Favored mechanism
Strongest competing explanation
Highest-value missing experiment
```

If the failure or question is not real and bounded, do not manufacture a paper
skeleton.

## Minimum scientific loop

### 1. Verify the problem and closest explanations

- confirm the failure from an actual baseline, observation, or verified source;
- identify the strongest current approach and its key assumption;
- state the favored and competing mechanisms;
- derive an observation that differs between them.

Product: a bounded research question and a small Claim Tree. Use only the claims
the paper needs.

### 2. Design the minimal intervention

- change one scientific object, constraint, representation, objective, protocol,
  or task definition that targets the failure;
- name assumptions, expected signature, rejection signature, and failure
  boundary;
- compare with the simplest valid alternative;
- remove components without an independent role or deletion test.

Product: a concise method/theory specification, not an architecture stack.

### 3. Run the decisive evidence

- use the true independent unit;
- make data access, split, preprocessing, target access, metric, and budget fair;
- measure both task behavior and the proposed mechanism/property when possible;
- preserve negative, null, unstable, invalid, and contradictory outcomes;
- estimate uncertainty according to the design.

Product: actual result files, metrics, uncertainty, and a claim decision.

### 4. Identify the boundary

Break the assumption most likely to delimit the method. Use one stress, OOD,
shift, ablation, or controlled intervention that distinguishes real mechanism
from extra capacity, tuning, leakage, or chance.

Product: a boundary or revised mechanism, even when the method loses its
advantage.

### 5. Write evidence-first

Recommended order:

```text
Method
-> Experiments
-> Results
-> Limitations
-> Discussion
-> Related Work
-> Introduction
-> Abstract
-> Conclusion
```

Write only what the actual theory, code, results, and verified sources support.
Use `hypothesis-only` rather than success language when the mechanism remains
unresolved.

### 6. Review and revise

Ask only the objections that can change the conclusion:

```text
Is the failure real?
Does the method target the stated mechanism?
Is the comparison fair?
Is the independent unit correct?
What alternative explanation remains?
Where does the claim fail?
What new understanding survives?
```

Address each through an experiment, analysis, theory change, or manuscript
revision. If new evidence rejects the claim, revise the claim.

## Completion criterion

The minimum paper loop is complete when it can answer:

1. What scientific problem is studied?
2. Why are current methods insufficient under the stated conditions?
3. What minimal idea changes the relevant mechanism or constraint?
4. Why should that change matter?
5. What evidence shows when it works and fails?
6. What bounded understanding is gained?

It is not complete because it contains a fixed number of claim rows, reference
rows, run records, figures, checklists, or reviewer reports.

## Stop conditions

Stop and state the missing item when:

- dataset, label, metadata, split, objective, metric, or protocol meaning is
  ambiguous;
- no fair baseline or true independent unit can be established;
- the required original source or actual result is unavailable;
- the proposed intervention has no observable or rejection signature;
- external credentials, paid compute, destructive remote work, publication, or
  submission require authorization.

Do not create a blocker package. State the affected decision and the smallest
next action.
