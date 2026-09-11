# Goal 02 — Theory and manuscript synchronization

## Scope

Maintain one chain: `problem → theory → method → estimand → experiment → claim`. Do not add another generic theorem unless an existing statement is mathematically insufficient for the implemented method.

## Deliverables

- `notation.md` defines all main random objects and risks;
- `theory_main.md` contains nested-message risk, routing headroom and plug-in routing regret;
- detailed existing Theory 12/13 remain the proof authority for Gaussian/statistical controls;
- `main.md`, `contributions.md`, `method.md`, `experiments.md`, `results_native.md` use the same objects.

## Acceptance

- M is never described as creating information relative to R;
- empirical source risk is never called population risk;
- router claims are conditional on headroom and source-only acquisition descriptors;
- no numerical PHM/SOTA result appears without an executed result file;
- negative routing/M results have explicit simplify/stop decisions.

## Commands

```bash
bash experiments/p19/run.sh theory
bash experiments/p19/run.sh toy
```

## Failure handling

A failed toy/theory invariant blocks the dependent manuscript claim. Fix the mathematical statement or implementation; do not weaken the counterexample or delete the negative case.
