# TII: source-supported posterior inference, industrial data only

Current manuscript: `main.md` (abstract/Introduction), `related_work.md`, `method.md`, `theory_main.md` with its finite Notebook, and `experiments.md`. The author-facing `introduction_outline.md`, `literature_matrix.md` and `contributions.md` record the scientific chain and evidence boundaries, not additional authorities or new results.

## This revision

The main question is now cross-dataset partial-observation posterior inference. HSE plus support-restricted Latent Laplace Diffusion is the proposed mechanism; ordinary/affine/moment message comparisons remain mechanism ablations. Laplace denotes stable modal dynamics, not Laplace noise. Current source code implements those message controls and an unrestricted native component/pilot, **not** the newly proposed physical support-restricted generative path.

The source-reference correspondence, conditional identifiability and the full projected native path are named prerequisites. Mathematical support projection, a source-global-null marker or an updated Introduction is not a learned-method validation. The prior coordinate results remain unchanged and retain their original scope. PHMFactory and `paper_TPAMI/` are not modified in this writing slice.

## Reproduce this writing/theory slice

```bash
python -m pip install numpy nbformat nbclient ipykernel cairosvg
bash paper/build_frontmatter.sh outputs/tii_support
```

This executes the same-stem theoretical Notebook in a fresh kernel, writes an executed copy and finite-witness CSV, regenerates editable SVG/vector PDF/600-dpi PNG, and builds a cited manuscript preview with pandoc/XeLaTeX. No data download, neural training or synthetic replacement for real HSE features occurs. Missing pandoc/XeLaTeX is a build dependency, not an experiment failure.

## Next substantive implementation

Use the existing source-only industrial data path and local GPU goal. First establish an interpretable source modal/latent reference and its acquisition support; then implement the declared eligibility projection in the actual native forward and reverse paths, testing observed-evidence preservation and empty eligibility. Only after a real paired-source batch passes should the E2 posterior comparison and E1 industrial LODO run. Keep R/head_affine/M as E3, with their original checkpoint and supervision contracts. The 8×4090 machine begins with one card; two-card training remains prohibited. This README does not claim those new method commands already exist.
