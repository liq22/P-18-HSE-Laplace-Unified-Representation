# Conditional accessibility: fixed representations, selection and fusion

## Objects and scope

Fix the source-trained HSE, reference encoder, supervised conditioner checkpoint and each downstream predictor before the following population comparison. Write $R=g_\theta(C_F)$ for the complete ordinary message and $M=T_\psi(R)$ for its statistically anchored reparameterization. Both use the same actual side inputs. Let $A$ be the deployment-available acquisition descriptor. Let $X$ include the noisy latent, diffusion time, **A**, and common side information. A target mask or random native weight must either be part of this declared information or be handled under the native weighted population measure; an unweighted identity is not silently applied to a different batch-normalized objective.

Population expectations below integrate over an independent evaluation event and any stated diffusion noise, conditional on the fixed training result. Finite source-validation averages carry hats. The prediction family and training budget are fixed; a newly trained fusion model is a different arm.

The results use standard conditional projection and fixed-expert selection arguments. They specialize these tools to the actual matched HSE messages; they are not new general information or routing theory. Predictive V-information already formalizes observer-dependent usable information (Xu et al., ICLR 2020); multi-expert regression/deferral and cost-aware two-stage routing are direct precedents (Mao, Mohri and Zhong, ICML 2024/2025).

## Proposition 1 — nested-message finite-risk decomposition

Assume $\mathbb E\|V\|^2<\infty$ for a common regression target $V$. Put

$$
f_R=\mathbb E[V\mid X,R],\qquad f_M=\mathbb E[V\mid X,M].
$$

The fitted predictors $d_R,d_M$ are measurable in their respective inputs and square-integrable. Define

$$
\Gamma(a)=\mathbb E[\|f_R-f_M\|^2\mid A=a],\quad
\mathcal E_j(a)=\mathbb E[\|d_j-f_j\|^2\mid A=a].
$$

For almost every $a$,

$$
\boxed{\rho_M(a)-\rho_R(a)=\Gamma(a)+\mathcal E_M(a)-\mathcal E_R(a),\qquad \Gamma(a)\ge0.}
$$

### Proof

Since $M=T(R)$, $\sigma(X,M)\subseteq\sigma(X,R)$. Conditional on $(X,R)$, $V-f_R$ has zero mean. Expanding

$$
\|V-f_M\|^2=\|V-f_R\|^2+\|f_R-f_M\|^2
+2\langle V-f_R,f_R-f_M\rangle
$$

and conditioning on $A$ eliminates the cross term by the tower property; this is valid because $A$ was included in $X$. For each $j$, expand $V-d_j=(V-f_j)+(f_j-d_j)$ and eliminate its cross term in the same way. Subtract the two resulting identities. These conditional expectations are defined almost surely, not pointwise at every unsupported acquisition value. ∎

### Consequence and boundary

An M-over-R gain requires $\mathcal E_R(a)-\mathcal E_M(a)>\Gamma(a)$. The statistical message does not create new observation information. This identity concerns the stated square-loss target; it is not an Energy Score, macro-F1 or finite reverse-sampler guarantee. Gaussian-score moment identification and the same-moment/non-Gaussian counterexample remain in the existing detailed theory files.

## Definition — a fixed-system conditional risk profile

For a finite set of fixed trained arms $\mathcal J$, define

$$
\rho_j(a)=\mathbb E[\ell_j\mid A=a],\qquad
\mathcal R_j=\mathbb E_{A\sim\pi}\rho_j(A).
$$

The acquisition weighting $\pi$ is declared. A balanced-condition benchmark and a prevalence-weighted deployment are different estimands. Loss must be integrable and common across arms. For diagnostic routing, use a declared per-event proper/classification loss to fit the selector; recompute macro-F1 from final predictions instead of treating it as an additive event loss.

## Proposition 2 — hard-selection headroom, not a fusion theorem

Define

$$
\mathcal H_{\rm hard}=\min_j\mathbb E_\pi\rho_j(A)
-\mathbb E_\pi\min_j\rho_j(A).
$$

Then $\mathcal H_{\rm hard}\ge0$. For finite $\mathcal J$ it is zero exactly when at least one globally best arm is also conditionwise optimal almost surely (ties allowed).

### Proof

For every fixed $j$, $\min_k\rho_k(a)\le\rho_j(a)$. Integrate and minimize the right-hand side. If equality holds, choose a global minimizer $j_0$, which exists because the set is finite. The nonnegative integrable gap $\rho_{j_0}(A)-\min_k\rho_k(A)$ has expectation zero and thus vanishes almost surely. The converse is immediate. ∎

### Counterexample — zero hard headroom can coexist with a fusion gain

Let $A$ have two equally likely values, target $Y=0.25$ or $0.40$, and fixed predictions $f_R=0,f_M=1$. R is better under both conditions, so $\mathcal H_{\rm hard}=0$. Its MSE is $0.11125$. Static prediction fusion $f_\alpha=(1-\alpha)f_R+\alpha f_M$ with $\alpha=0.325$ has MSE $0.005625$. Conditional weights $\alpha(A)=Y(A)$ have zero MSE in this constructed example. Therefore a zero hard headroom does **not** rule out static or soft fusion; a positive one does **not** prove a router beats static fusion.

These are fixed scalar-predictor witnesses. For probability forecasts, define a mixture distribution and evaluate its proper score. Interpolating two diffusion latent samples or two condition tokens is not automatically that mixture.

## Proposition 3 — plug-in regret with an explicit transportability error

Let $\widehat\rho^s_j(a)$ be source-only estimates and suppose, on the target support,

$$
|\widehat\rho^s_j(a)-\rho^s_j(a)|\le\epsilon(a),\quad
|\rho^s_j(a)-\rho^t_j(a)|\le b(a)
$$

for every arm. Both bounds are assumptions unless separately established. Use the same declared target weighting $\pi$ when evaluating the quantities below. Set $e=\epsilon+b$ and $\widehat j(a)=\arg\min_j\widehat\rho^s_j(a)$ with a fixed tie rule. Then

$$
\boxed{\mathcal R_t(\widehat j)-\mathcal R_t(j_t^*)\le2\mathbb E_\pi e(A).}
$$

Moreover,

$$
|\widehat{\mathcal H}_{s,\pi}-\mathcal H_{t,\pi}|\le2\mathbb E_\pi e(A).
$$

### Proof

By the triangle inequality, each estimated risk differs from the target risk by at most $e(a)$. Add and subtract the estimated risks of the selected and target-optimal arms. Their estimated difference is nonpositive, leaving at most $2e(a)$. Integrate. For headroom, the minimum of finitely many real numbers is 1-Lipschitz in the sup norm. Apply that fact once to the minimum of global risks and once to the conditionwise minimum, then add the two bounds. ∎

If the selector incurs additional cost $c_g(A)$ priced by a declared $\lambda$, its gain over the target-best fixed arm is at least

$$
\widehat{\mathcal H}_{s,\pi}-4\mathbb E_\pi e(A)-\lambda\mathbb E_\pi c_g(A).
$$

This is a conditional lower bound, not a claim that target errors or a universal cost conversion are known. Arm-dependent cost must be included in each risk before selection. No unseen-condition guarantee is invoked when source conditional order reverses.

## Empirical selection and falsification

Use disjoint source groups for fitting predictors, selecting checkpoints/gates, and evaluating the final comparison. A positive in-sample $\min\widehat\rho$ gap is upward-biased evidence for selection because the same noise chooses the winner. An independent held-out source evaluation or group cross-fitting is required before promotion. Target test groups never choose a gate, threshold, fusion coefficient or covariance floor.

The same-stem Notebook executes the finite hard/soft distinction and the regret algebra. `experiments/p19/toy_routing.py` additionally generates independent source/test events, fits selectors on source predictions, and evaluates no-crossing, crossing, fusion-only and target-reversal controls. It is not a simulation of the complete HSE or LLapDiff architecture. The existing two-arm native pilot remains the first learned experiment.

## References and originality boundary

- Xu et al. (2020), *A Theory of Usable Information under Computational Constraints*, ICLR; arXiv:2002.10689, Definitions 1–3.
- Mao, Mohri and Zhong (2024), *Regression with Multi-Expert Deferral*, ICML/PMLR 235:34738–34759.
- Mao, Mohri and Zhong (2025), *Mastering Multiple-Expert Routing: Realizable H-Consistency and Strong Guarantees for Learning to Defer*, ICML/PMLR 267:43035–43066, Section 2.

The candidate contribution is a statistically anchored **industrial conditioning intervention**, tested against its fully supervised ordinary code. Conditional profiles and the bounds above define falsifiable interpretation and selection criteria; merely renaming standard routing headroom is not an independent theoretical invention.
