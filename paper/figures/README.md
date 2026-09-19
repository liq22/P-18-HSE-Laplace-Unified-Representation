# Chapter 2 concept and Chapter 3 overview

```bash
python paper/figures/motivation.py --output-dir paper/figures
```

One source generates `motivation` (180×64 mm) and `overview` (180×132 mm), each as independently editable SVG, vector PDF and 600-dpi PNG. Text remains SVG text; boxes, arrows and labels have separate IDs. No raster is embedded. The diagrams describe a problem and a proposed inference procedure, not performance measurements.

## Figure 1 — problem only, Section 2.4

Purpose: show why the source observation law, not feature availability alone, determines the conditional target. The figure contains the C/P/M/N0 support matrix and the two common-view binary worlds. It contains no HSE, generator or proposed update block. Section 2.4 gives the caption, source-law explanation and connection to the missing joint target; Section 2.2 defines the underlying spaces.

## Figure 2 — method, Section 3.1

Purpose: separate source-only target construction from deployment, and expose exactly where the new restriction enters an inherited conditional denoiser. Neutral boxes denote inherited mechanisms; colored boxes denote the selected target and restricted process. Dashed arrows supply source preparation/frozen definitions, not target-time clean evidence. Source targets do not enter deployment. The observed branch is shared, and each observed-state draw is held fixed within its conditional reverse path.

| Mechanism / object ID | Formula or variable | Section | Algorithm | Experiment |
|---|---|---|---|---|
| `qualified-target` | paired (C_F,z_o,w_0), B_e, G_e; Eq.6 | 3.2 | A1–A2 | E4/E5 |
| `hse-condition` | shared R and H_R/H_A/H_M; Eqs.7–8 | 3.2 | A3 | E3 |
| `temporal-denoiser` | velocity objective and modal branch; Eqs.9–10 | 3.3 | A4/A6 | E2/E5 |
| `velocity-conversion` | clean/noise conversion; Eq.11 | 3.3 | A6 | E2 parameterization control |
| `restricted-update`, `reverse-loop` | basis DDIM; Eq.12 | 3.4 | A5–A6 | E2/E4 |
| `observed-readout`, `observed-draw-to-sampler` | q_o and same z_o per draw; Eq.13 | 3.4 | A3/A5–A6 | E2 joint-dependence control |
| `coherent-tuple`, `fixed-diagnostic-head` | fixed source h_psi, retained R; Eq.14 | 3.4 | A3/A7 | E1/E2/E3 |
| restriction/temporal labels | intervention (r,l,c), Eq.5 | 2.3/3.5 | A4–A7 | E2 factorial |

Both figures have section-specific captions and prose explanations. The full manuscript build renders them from this file; PDFs and PNGs are build products, not extra tracked drawing sources.

The 2026-09-19 label revision retains both layouts. Figure 1 writes equality of the complete source-observation laws explicitly; the actual conditionals still differ. Figure 2 places the constructive `Q_e null(A_e Q_e)` basis at target qualification and names the trainable generator versus fixed readouts. The ordinary/Laplace block remains inherited and refers to physical time, not a different perturbation distribution. “Conditional draw” describes the factorized sampling construction, not verified agreement with the true joint law. No new performance figure is introduced.
