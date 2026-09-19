# Goal 01 — PHMFactory child-first implementation and synchronization

## Purpose

The paper repository owns scientific formulation, basic closed-form/interface checks, manuscript mappings and the PHMFactory gitlink. The executable learned method, data adapters/configurations, training, evaluation and experiment artifacts belong to `external/phmfactory` (`PHMbench/PHM-Vibench`). Do not create a second reader, trainer or experiment runtime in the paper repository.

## Current boundary

The parent `dev` pins `external/phmfactory` to an accepted historical revision. A newer PHMFactory `dev` or open PR is not automatically accepted for this paper. Research implementation must be validated at an exact child commit before the parent gitlink moves.

## Synchronization order

```text
paper formulation / basic witness
→ child PHMFactory research branch
→ child focused tests + exact config + real source batch
→ child PR → PHMFactory dev
→ re-run the paper-specific acceptance at that exact child commit
→ parent gitlink + paper evidence mapping PR
→ parent dev
```

Never move the parent gitlink first and repair the child later.

## Read-only start

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git submodule status external/phmfactory
git -C external/phmfactory status --short
git -C external/phmfactory branch --show-current
git -C external/phmfactory rev-parse HEAD
git -C external/phmfactory remote -v
```

Check active PRs in both repositories. Preserve unrelated dirty files. Do not stash, reset, clean, force-push or delete branches.

## Child implementation rule

Use PHMFactory's maintained public path:

```text
resolved config
→ Data Factory
→ Model Factory
→ Task Factory
→ Trainer Factory
→ selected checkpoint
→ evaluation artifacts
```

A P18 model must enter through the existing `Model(args_model, metadata)` resolution; objectives/metrics belong to Task Factory; data remain owned by Data Factory. Fix a real owner defect at its boundary rather than bypassing it from the paper repository.

## Acceptance before parent sync

The candidate child commit must have:

1. focused component tests for the changed model/task/data owner;
2. `phmfactory preflight` on each retained P18 config family;
3. at least one real source-batch execution using the local PHM data path;
4. checkpoint reload producing the same evaluation prediction within declared tolerance;
5. no target-data fitting, silent task/model substitution or sample dropping;
6. actual config, seed, dependency and failure records retained.

Only after that exact commit is remotely available may the parent gitlink advance. The parent PR records the child commit and the evidence scope; it does not relabel a child smoke as a paper result.

## Failure handling

If child `dev` contains unrelated or incompatible changes, create a bounded P18 branch from the intended accepted base and merge normally after review. If a required dataset/task contract is invalid, stop that scientific path; do not edit upstream data/splits to manufacture eligibility. A negative method result is not a synchronization failure.
