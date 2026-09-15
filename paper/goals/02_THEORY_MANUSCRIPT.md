# Goal 02 — close the scientific argument

## Scope

Maintain `M=T(R)`, matched statistical supervision, actual consumed condition and native target. Keep fixed-arm hard selection distinct from soft fusion. Do not rename standard usable-information or multi-expert-routing theory as an independent invention.

## Products

`main.md`, `notation.md`, `method.md`, `theory_main.md` + `theory_main.ipynb`, `related_work.md`, `contributions.md`; preserve the historical numbered proofs and their finite counterexamples.

## Commands

```bash
bash experiments/p19/run.sh theory
bash experiments/p19/run.sh toy --events 1024 --seed 0 --output outputs/p19/toy_routing.csv
```

## Acceptance

General assumptions/proofs and same-stem Notebook agree. Verify the 0.075 hard-headroom algebra, the zero-hard-headroom fusion counterexample, conditional transport-error regret, and source/test separation. Citation keys resolve in the existing bibliography. Read primary method/theorem sections before changing novelty claims. The Results section reports observed simulation scores without treating them as learned HSE results.

## Failure handling

A proof or witness fails: narrow/correct that statement before experiment promotion. An existing theorem is background: keep attribution and test its method-specific consequence. Do not increase the theorem count or retitle the paper to hide a null method result.
