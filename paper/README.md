# Industrial TII manuscript

The current manuscript is assembled in this order:

- `main.md` and `related_work.md`: Introduction and its Related Work subsection.
- `formulation.md`: Chapter 2, prior foundations, problem variables, gap and objective.
- `method.md`: Chapter 3, source-target construction, conditioning, velocity training, restricted DDIM, conditional sampling and fixed-readout diagnosis.

`theory_main.md/.ipynb` hold supporting derivations and finite examples. `experiments.md` specifies E1–E5. `contributions.md` and `figures/README.md` map mechanism → equation → figure → algorithm → experiment. They are author material, not additional manuscript chapters.

```bash
bash paper/build_frontmatter.sh outputs/tii_support
```

The retained entry now builds Chapters 1–3 as `tii_manuscript.pdf`, renders the problem and method figures, executes the same-stem Notebook, and checks citation resolution, editable SVGs and retained/new finite values. Source SVGs are tracked; PDF/600-dpi PNG are regenerated. The original 14-row support witness is preserved; the additional method witness tests conversion, non-diagonal support, the explicit oracle update and posterior dependence.

The existing coordinate pilot remains an E3 control. The intrinsic native loss and reverse loop now have a separate real exported-source batch entry. Its deterministic reference-feature acquisition is an implementation experiment, not calibrated HSE or cross-dataset evidence. Industrial data/labels/splits remain owned by PHMFactory; no second reader or trainer is introduced. General theory and nonindustrial experiments remain in `../paper_TPAMI/`.

Current intrinsic training/reverse functions and the real exported-source batch entry are described in `GOAL.md`. The default batch reference is explicit DCT features, not HSE or physical modal calibration. Its source-only implementation checks are separate from the pending factorial and LODO study.
