# Motivation figure

```bash
python paper/figures/motivation.py --output-dir paper/figures
```

The sole drawing source is `motivation.py`. It exports independently editable SVG objects with real text, vector PDF and a 4252×3260 PNG (approximately600dpi at180×138mm). No raster is embedded in the SVG. PDF/PNG are regenerated locally or by the existing manuscript workflow rather than tracked as redundant binaries.

| Panel / object | Meaning | Manuscript / experiment |
|---|---|---|
| a: C,P,M,N0 columns and source rows | Aligned reference support, not paired events or measured sensor calibration. | Introduction1–5; Method1–2; E4/E5. |
| b: two binary worlds | Equal source pair laws do not identify the conditional after private evidence is included. | Proposition2 and executable common-view witness; E4. |
| b: (I_e,C_T),G_e | Target qualified together with complete condition; fixed admitted projector. | Method2; Algorithm1 step2. |
| c: HSE | Observed/private evidence plus source-trained moment anchor. | Method3; E3 same-head controls. |
| c: restricted LLapDiff | Gaussian latent diffusion with a stable temporal parameterization. | Method4; E2. |
| c: observed bypass and posterior samples | Preserve observed uncertainty and sample the identified joint, not independent marginal blocks. | Method4–5; Algorithm1 steps5–6. |
| c: excluded outputs | Unidentified missing and global-null coordinates have no recovered-value output. | Propositions3–4; E4 coverage/utility. |
| d: outcomes and factorial | Separate posterior/diagnosis; cross restriction with temporal parameterization. | E1/E2/E4; interaction estimand. |

The two-world example is an analytical counterexample. The diagram contains no expected performance curves or trained-model results. Its caption defines the independent fair bits and explains why common-view overlap does not identify the full-input conditional. The actual source-qualified native sampler remains to be implemented; existing coordinate controls retain their original scope.
