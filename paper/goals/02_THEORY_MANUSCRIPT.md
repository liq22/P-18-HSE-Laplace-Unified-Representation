# Goal02 — formulation and explicit method

Maintain Chapters 2 and 3 as separate scientific roles: prior foundations/problem/estimands, then the proposed source-qualified inference algorithm. Related Work stays within Introduction. The concept figure contains only problem variables; the overview figure maps mechanisms to Eqs. (6)–(14) and A1–A7.

```bash
bash paper/build_frontmatter.sh outputs/tii_support
bash experiments/p19/run.sh theory
```

The first command builds the cited Chapters 1–3, executes the existing Notebook and regenerates both editable figures. Keep the 14 original support values and new method witness separate. Check velocity/clean loss weighting, non-diagonal intrinsic DDIM, score restriction versus marginalization, and coherent covariance. These validate finite mathematical statements, not trained industrial inference.

Read experiments.md and contributions.md for the next real-data contrast. Use the existing native implementation rather than copying a denoiser. Source-reference calibration and the actual eligible-only native loss/update remain necessary before learned posterior or LODO claims. Do not reopen already resolved affine, unpaired-source or correlated-prior arguments without a new counterexample.
