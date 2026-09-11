# Notation, assumptions, and estimands

This file is the notation authority for the TII manuscript. Older analytical files may use additional symbols; the main paper should translate them to this table rather than introduce aliases.

## Random objects and conditions

| Symbol | Meaning |
|---|---|
| \(O\) | Current observed history before HSE compression |
| \(a\) | Acquisition descriptor actually available at inference, e.g. sampling rate, observed duration, channel/mask summary; never target labels |
| \(F=HSE_0(O,a_{enc})\) | Frozen HSE features |
| \(M_F\) | Valid-history mask used before global pooling |
| \(C_F=(F,M_F,a)\) | Complete input available to the paper conditioner |
| \(Z_0\) | Frozen reference-encoder latent trajectory generated/predicted by LLapDiff |
| \(U=L\operatorname{vec}(Z_0)\) | Declared low-dimensional target functional used for statistical supervision |
| \(Y\) | Fault/diagnostic label used only in downstream PHM evaluation unless a supervised experiment explicitly says otherwise |
| \(V_\tau\) | Native diffusion regression target at time τ (v, ε or \(x_0\) according to the experiment) |

## Representations

| Symbol | Meaning |
|---|---|
| \(R=g_\theta(C_F)\in\mathbb R^q\) | Ordinary source-supervised code, transmitted by B1-aux |
| \(m_\psi(R),S_\psi(R)\) | Predicted conditional moments of \(U\mid R\) under the declared Gaussian score |
| \(M=T(R)\in\mathbb R^q\) | Statistical-prefix message: moments plus the remaining ordinary coordinates |
| \(H_{\alpha}\) | Static equal-budget fusion of standardized R and M with one source-selected global coefficient α |
| \(H_{g(a)}\) | Acquisition-conditioned route/fusion using only source-learned gate \(g(a)\) |

## Risks

For an arm \(j\) and acquisition condition \(A=a\), define the population evaluation risk

\[
\mathcal R_j(a)=\mathbb E[\ell_j\mid A=a],
\]

where the loss, target support and trained model are fixed before evaluating the test law. The global risk is ℛ_j=E_A[ℛ_j(A)]. Empirical source-validation estimates are written \(\widehat{\mathcal R}_j(a)\); they are not interchangeable with population risks.

For the nested pair R/M and a common square-integrable diffusion target, define the Bayes information penalty

\[
\Gamma_{M\mid R}(a)=
\mathbb E\!\left[\|\mathbb E[V_\tau\mid X,R,A=a]-\mathbb E[V_\tau\mid X,M,A=a]\|^2\mid A=a\right]\ge0.
\]

If \(A_R(a)\) and \(A_M(a)\) are finite-predictor excess risks relative to their Bayes predictors, the **conditional accessibility gain** of M over R is

\[
\Delta_{\mathrm{acc}}(a)=A_R(a)-A_M(a)-\Gamma_{M\mid R}(a).
\]

Positive Δacc means the finite fitting advantage of M exceeds the information penalty under that condition.

For a set of fixed trained arms \(\mathcal J\), define **routing headroom**

\[
\boxed{\mathcal H_{\mathrm{route}}
=\min_{j\in\mathcal J}\mathbb E_A\mathcal R_j(A)
-\mathbb E_A\min_{j\in\mathcal J}\mathcal R_j(A)\ge0.}
\]

It is zero when one arm is conditionally best almost everywhere. It is positive only when conditional risk crossings create a genuine opportunity for condition-dependent selection.

## Main assumptions

A1. **Same information access.** Compared arms receive the same \(O,a,M_F\); target/reference variables are supervision, not hidden decoder inputs.

A2. **Source-only model selection.** Checkpoints, static-fusion coefficients, router parameters and thresholds are selected without target-test labels or target-test normalization.

A3. **Independent unit before windows.** Machine/run/recording or declared latent event is split before windowing/resampling. Windows and posterior draws are not independent experimental units.

A4. **Fixed target and native objective.** \(Z_0,L\), prediction parameterization, diffusion schedule, target mask reduction and loss weighting are shared across representation comparisons.

A5. **Known acquisition descriptor for routing.** Any dynamic gate consumes only acquisition variables available at deployment. Dataset identity is excluded unless it is itself the declared physical descriptor being tested.

A6. **Budget accounting.** Message size, conditioner parameters, gate parameters, denoiser parameters, training updates, latency and memory are reported separately. Equal \(q\) alone is not called equal compute.

A7. **Conditional guarantee boundary.** Source-domain risk estimates do not imply unseen-acquisition calibration. Target results are reported separately and never used to refit the conditioner or router.

## Failure conditions

The statistical-prefix idea is demoted if B1-aux is non-inferior at lower cost. Dynamic routing is not retained if \(\mathcal H_{route}\) is practically zero or if source-only routing fails on unseen acquisition conditions. A failure is a scientific result; it is not repaired by silently adding more branches.
