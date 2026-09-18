# Industrial TII manuscript

The current manuscript is assembled in this order:

- `main.md` and `related_work.md`: Introduction and its Related Work subsection.
- `formulation.md`: Chapter 2, prior foundations, problem variables, gap and objective.
- `method.md`: Chapter 3, source-target construction, conditioning, velocity training, restricted DDIM, coherent sampling and fixed-readout diagnosis.

`theory_main.md/.ipynb` hold supporting derivations and finite examples. `experiments.md` specifies E1–E5. `contributions.md` and `figures/README.md` map mechanism → equation → figure → algorithm → experiment. They are author material, not additional manuscript chapters.

```bash
bash paper/build_frontmatter.sh outputs/tii_support
```

The retained entry now builds Chapters 1–3 as `tii_manuscript.pdf`, renders the problem and method figures, executes the same-stem Notebook, and checks citation resolution, editable SVGs and retained/new finite values. Source SVGs are tracked; PDF/600-dpi PNG are regenerated. The original 14-row support witness is preserved; the additional method witness tests conversion, non-diagonal support, the explicit oracle update and posterior dependence.

The accepted native pilot still provides conditioner comparisons, not the newly specified restricted posterior or fixed-readout industrial experiment. The next implementation uses a genuine source reference/paired batch, validates the induced support, and connects the declared velocity objective and basis update to the original native model. No second reader/trainer, guessed physical mask or target fitting is introduced. Industrial data/labels/splits remain owned by PHMFactory. General theory and nonindustrial experiments remain in `../paper_TPAMI/`.
