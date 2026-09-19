# Goal 03 — Gate 0: industrial data and scientific task qualification

## Scientific question

Do the available industrial datasets actually instantiate the paper's jointly source-qualified partial-latent inference problem, rather than merely providing vibration windows and class labels?

## No performance estimand

Gate 0 does not estimate accuracy or posterior quality. Its output is a per-dataset, per-contribution decision:

```text
GO      = scientific object and evaluation target are available
PARTIAL = only a bounded subset of claims/metrics is supported
NO-GO   = this dataset cannot test that contribution
```

## Required tuple

For every candidate experiment unit, identify or explicitly mark unavailable:

$$
\mathcal T_i=(x_i^{obs},x_i^{ref},\Gamma_i,B_i,y_i,g_i),
$$

where `g_i` is the highest reliable independent original unit (machine / acquisition run / raw recording), not a window.

## Mandatory qualification table

For each local dataset answer all fields before any multi-seed training:

| Field | Required question |
|---|---|
| Common label ontology | Can labels be mapped without target-specific fitting or semantic guessing? |
| Independent unit | What is the highest reliable recording/run/machine key? |
| Reference origin | Extra measurement, controlled high-fidelity view, or deterministic feature of the same waveform? |
| Pairing | Are observed/reference views from the same state/recording or a calibrated joint acquisition? |
| Joint evidence | Why is the required joint block justified, beyond each coordinate appearing somewhere? |
| Eligible set | Are eligible and ineligible missing components both present? |
| Evaluation truth | Is the missing target observed at evaluation time? |
| Observed uncertainty | Is $q_o$ non-degenerate, point-mass, or unavailable? |
| Source-only usability | Can all fitting/selection be done without target labels/features? |
| Contribution scope | C1 / C2 / C3: GO, PARTIAL or NO-GO |

Geometric support is not conditional identification. A deterministic DCT/HSE transform of one waveform is a `reference-feature target`, not automatically a true mechanical state.

## Local inputs

Use the user-supplied local PHMFactory data root, metadata and HDF5 files through the existing PHMFactory Data Factory only. Machine paths belong in a local config or shell variable; do not commit them to the repository.

```bash
export PHM_DATA_ROOT=/absolute/local/PHM-Vibench
```

Read `metadata.xlsx` and the local data README through the existing maintained data path. Do not create another Pandas/HDF5 loader merely for P18.

## Execution

1. Read the paper `formulation.md`, `method.md`, `experiments.md` and the exact PHMFactory gitlink.
2. Read PHMFactory `CORE.md`, `AGENTS.md`, Data/Model/Task/Trainer READMEs and the selected reader/adapter.
3. Enumerate the provided datasets from metadata, not from filenames alone.
4. Establish label ontology, independent-unit key, channels, units, sample rates and acquisition metadata.
5. For each candidate reference/view construction, state `reference origin`, `pairing`, `Gamma/A`, `Q`, `B`, and whether missing target truth is actually observable.
6. Produce `DATA_TASK_GATE.md` with GO/PARTIAL/NO-GO and exact blockers.
7. Select one **source-internal development cohort** for Gate 1. Do not inspect an outer LODO target to choose the method.

## Acceptance

Gate 0 is complete when every planned experiment cell is `ready`, `blocked` or `NA` for a stated scientific reason. Full LODO is forbidden until label ontology, independent units and source-only selection are valid. C1/C2 restriction claims additionally require a nontrivial eligible/ineligible target or a controlled paired-view experiment with known qualification truth.

## Failure handling

- No paired reference → continue only experiments that do not require posterior truth.
- All missing components eligible → this dataset cannot show restriction benefit; keep it for diagnosis/posterior-family tests if otherwise valid.
- No target truth → diagnosis can be evaluated, posterior score cannot.
- Too few independent recordings → do not replace them by windows as statistical units.
- Dataset semantics incompatible → stop that fold instead of remapping labels after seeing performance.

No Results prose is written at Gate 0.
