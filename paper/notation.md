# Industrial notation and endpoints

| Symbol | Meaning |
|---|---|
|$O,a,M_F$|Current industrial history, actual deployment acquisition descriptors and valid-history mask|
|$F=HSE_0(O,a_{enc})$|Source-trained frozen HSE feature|
|$C_F=(F,M_F,a)$|Complete conditioner input|
|$Z_0=E_{ref}(X_{ref})$|Frozen reference latent target, not identified physical coefficients|
|$U=L\operatorname{vec}(Z_0)$|Predeclared target functional for source moment supervision|
|$R\in\mathbb R^q$|Complete statistically supervised ordinary code|
|$M=T(R)\in\mathbb R^q$|Same-budget global statistical prefix and ordinary tail|
|$\rho_j(a)$|Population risk of a fixed trained industrial arm under condition a|
|$\widehat\rho_j(a)$|Empirical source-validation/evaluation risk, with its actual group count|
|$\Gamma(a)$|Nonnegative Bayes square-risk information penalty for nested M|
|$\mathcal E_j(a)$|Finite consumer error above its own conditional expectation|

The primary fault endpoint is recording-balanced pooled-confusion macro-F1. Group windows receive weights summing to one per original recording; compute F1 after pooling the confusion matrix across the fixed label ontology. Do not average per-window F1 or single-class recording F1. Reference pooled-window metrics remain separate. Six MFPT files are not automatically six independent machines.

The applied square-risk decomposition concerns its native regression target and integrability/conditioning assumptions; it is not a macro-F1 theorem. General fixed-policy headroom, independent certification and multi-domain target/consumer notation are owned by `../paper_TPAMI/`.
