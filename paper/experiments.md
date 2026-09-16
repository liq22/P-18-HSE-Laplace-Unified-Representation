# TII experiments — industrial data only

## Primary question

Does M=T(R) improve industrial diagnosis or latent prediction over B1-aux at the same observation access, supervision, selected checkpoint, message size and native consumer? This is the only primary intervention. General multi-domain datasets and finite-policy certification are in `../paper_TPAMI/`.

## I0 — mathematical and component checks

Run the shared theoretical witnesses and the applied `theory_main.ipynb`; run actual native mask/field/loss/gradient checks. These numerical checks are not nonindustrial empirical benchmark tables. Inputs explicitly labelled synthetic cannot establish genuine HSE/reference extraction.

## I1 — PHMFactory reference acceptance

Use the current accepted submodule and unchanged MFPT GlobalAverageLinear config, five CPU epochs and seeds17/18/19. Preserve provider labels, 10/4/6 original-file split, checkpoint selection and independent pooled-window accuracy/F1 recomputation. Reference acceptance is already recorded in `results_native.md`; it does not train this paper's HSE conditioner. Additional industrial datasets must pass their own maintained PHMFactory data/reader/split acceptance; no parent-side alternate reader.

## I2 — minimal learned industrial comparison

Export genuine source-trained HSE/reference targets with original group IDs, acquisition descriptors, masks and source-only preprocessing. Main arms: B1-aux and M from the same checkpoint. Three paired seeds run sequentially on one GPU first. For classification, primary endpoint is recording-balanced pooled-confusion macro-F1 with a fixed full ontology; report pooled-window metrics separately. For native generation, report recording-macro Energy Score separately. Do not substitute a latent score for diagnostic evidence.

Industrial factors: rate, fixed physical duration versus fixed point budget, structured missingness, and sensor/channel changes where documented. Speed/load and machine shifts are separate from acquisition changes. All derived views are generated after original recording/group splitting. MFPT filenames alone do not prove physical bearing or machine independence.

## I3 — practical controls and SOTA candidates

Reference B1 controls auxiliary supervision; the official LLapDiff conditioner B0 controls inherited model capability. Compare the strongest single representation and a source-selected static prediction/distribution fusion before considering a source-only acquisition selector. A route is optional; it must improve the actual industrial endpoint at accounted cost. General hard-selection headroom is not a proof that it beats static fusion.

Industrial strong methods: HSE, compatible official FISHER/TF-ProFM, a matched raw Conv1D/Transformer, physical STFT/wavelet front ends, same linear diagnosis head and one small-MLP capacity control. Gaussian/finite-mixture probability heads receive the same condition as Diffusion. Methods without an accessible compatible implementation remain pending, not silently replaced.

## I4 — focused ablations

| Axis | Industrial contrast | Alternative explanation |
|---|---|---|
| Loss | B1 vs B1-aux; score decomposition; explicit covariance floor | extra supervision or instability |
| Representation | R, M, moment-only, ordinary tail shuffle; oracle moments only in known simulator controls | shape information or moment error |
| Structure | one target dimension/prefix budget change at matched consumer | capacity rather than semantics |
| Fusion/routing | best single, static mixture, optional acquisition selector, descriptor shuffle | complementary predictors or shortcuts |
| Statistics | pooled windows vs recording-balanced confusion | unequal recording counts/pseudoreplication |
| Explanation | prefix/tail intervention and source/unseen residuals | fields stored but not consumed; no causal claim |
| Cost | HSE, trunk/head, denoiser, diagnosis head, draws, all-arm fusion and training updates | unreported computation |

The theoretical and simple simulator controls may diagnose assumptions but do not count as extra empirical datasets. Full general selection experiments belong to the TPAMI workspace.

## Outputs and decision

Preserve per-recording predictions, truth/class probabilities, seed, condition and actual command. Recompute nonlinear F1 after pooling confusion; never average per-window F1. For additive scores use `experiments/p19/statistics.py`; for classification use `phm_metrics.py`. Missing pairs fail rather than disappearing in a join. A null/worse M result or a static mixture matching a route completes the question and favors simplification. No target dataset is replaced to conceal failure.
