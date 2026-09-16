# Notation, assumptions and estimands

| Object | Definition |
|---|---|
| $O,a$ | Observations and side information actually available at deployment |
| $F,M_F$ | Frozen encoder output and its valid-history mask |
| $R$ | Complete ordinary code trained with the declared auxiliary supervision |
| $M=T(R)$ | Same-budget statistical-prefix reparameterization; deterministic after training |
| $U_k$ | Target functional for task k, fixed before validation/test comparisons |
| $\mathcal F_c$ | Declared consumer family/capacity; not all measurable predictors |
| $b$ | Message, training and inference budget specification; scalar count alone is not total cost |
| $p$ | Complete frozen policy: representation, predictor, gate/fusion, target and sampling protocol |
| $\rho_p(a;k,c,b)$ | Population loss of fixed p conditional on acquisition a, task, consumer and budget |
| $\widehat\rho_p$ | Empirical estimate from named source or evaluation groups |
| $\Gamma_{M\mid R}$ | Bayes square-risk penalty due to a nested message, not an estimated MI by default |
| $\mathcal H_{hard}$ | Fixed-arm hard-selection headroom; excludes newly trained soft policies |
| $D_p$ | Population paired loss reduction against frozen reference, minus a declared cost difference |
| $\widehat D_p,r_n,\beta$ | Empirical reduction, simultaneous finite-family uncertainty radius, declared shift allowance |

The proposed object is a **task–consumer–budget conditional comparison profile**, not a novel generic information measure. Publish its entries with the defining loss and trained model. Do not average accuracy, Energy Score and regression MSE into one number.

Core assumptions: identical actual observation/side access; independent original groups before windowing; source-only checkpoint selection; shared native loss and target support; fixed policies before calibration; separately priced costs. The nested square-risk proof assumes square integrability and includes acquisition in the conditioning sigma-algebra. The finite-sample rule additionally requires iid calibration groups and a [0,1] group loss. Its target guarantee additionally assumes bounded advantage drift. These assumptions do not follow from unique filenames or frozen parameters.

For classifiers use a fixed ontology and recompute group-balanced pooled confusion metrics. For forecasts use chronological separation and disclose dependence. Nonoverlapping time blocks do not automatically justify iid certification. Use empirical blocked intervals unless a dependence argument is separately supplied. Across domains report both the dataset-level result and the original-unit uncertainty; repeat seeds and posterior draws never inflate the independent sample size.
