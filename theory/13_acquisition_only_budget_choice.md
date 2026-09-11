# Theory 13 — Budgeted layouts, posterior moments and their deployment limits

## Scope

Retain the correct acquisition-only expected-risk result, but compare different posterior parameterizations before selecting layouts. Finite-set minimization and Gaussian product projection are established mathematics. Spantini et al. (2015, DOI 10.1137/140977308) and goal-oriented Spantini et al. (2017, DOI 10.1137/16M1082123) are direct predecessors, not peripheral citations.

## 1. Assumptions

For known independent acquisition design, let `beta~N(0,S0)`,
`x=A beta+epsilon`, `epsilon~N(0,R)`, with `S0,R` SPD. Write

\[
J=A^TR^{-1}A,\quad b=A^TR^{-1}x,\quad
\Lambda=S_0^{-1}+J,\quad S=\Lambda^{-1},\quad\mu=Sb.
\]

A fixed candidate retains `J_g` and b, giving
`Q_g=S0^-1+J_g`, `q_g=N(Q_g^-1 b,Q_g^-1)`.
The prior, design, target and candidate set are declared before test events.
This is a plug-in posterior, not automatically the true conditional after compression.

## 2. Lemma: covariance of the exact posterior mean

\[
E[\mu]=0,\qquad\operatorname{Cov}(\mu)=S_0-S.
\]

**Proof.** The tower property gives the mean. Total covariance gives
`S0=E[Cov(beta|x)]+Cov(E[beta|x])`. The Gaussian conditional covariance is the constant S; subtract it. This does not assume a non-Gaussian posterior has constant covariance.

## 3. Theorem: acquisition-only prior-predictive risk

With `D_g=Q_g^-1 Lambda-I`,

\[
\boxed{\overline K_g(J)=\tfrac12[
\operatorname{tr}(Q_gS)-m+\log\det\Lambda-\log\det Q_g
+\operatorname{tr}\{Q_gD_g(S_0-S)D_g^T\}].}
\]

**Proof.** The approximate mean is `Q_g^-1 Lambda mu`, so its displacement is
`D_g mu`. Insert this into the Gaussian KL formula. Only the quadratic mean term depends on x. Use `E[u^TBu]=tr(B Cov(u))` and the preceding lemma.

Minimizing this expression over a fixed finite layout list is optimal only over that list, prior and plug-in decoder. A design-dependent layout code is transmitted or reconstructed from common actual side information. A mask depending on hidden state, unknown poles/noise, or compressed b needs a new analysis. For an actual target L, use target posterior KL or the target denoiser discrepancy in Theory 12; this coefficient criterion is not automatically goal-oriented.

## 4. Existing implementation and evidence

The current four-coefficient experiment has three disjoint pairings:
`(01|23)`, `(02|13)`, `(03|12)`. Each sparse header contains 4 information-vector entries, 4 diagonal values, 2 couplings and 1 layout code: **11 allocated scalars**. Full information uses 15. The padded diagonal header is allocated the same space but contains less information.

Risk and squared-coupling selectors inspect identical full designs and in the retained 24-design study choose identical layouts. This is identical subsequent computation, not independent statistical equivalence. The expensive selector has no demonstrated incremental value in those cells. Neither this observation nor a frequency-rule tie proves selectors are universally useless.

## 5. Theorem: the forward-KL product projection

For any density p and fixed disjoint coordinate groups `G_j`, let
`q_M=product_j p_{G_j}`. For any product density `q=product_j q_j`, assuming the KL terms are finite,

\[
\boxed{KL(p\|q)=KL(p\|q_M)+\sum_j KL(p_{G_j}\|q_j).}
\]

**Proof.** Insert the product of true marginals in the log ratio. Integrate the first term under p. Every remaining logarithm depends only on one group, so its integral uses that marginal. Nonnegativity gives optimality and equality exactly when all retained marginals agree almost everywhere.

For `p=N(mu,S)`, this gives `q_M=N(mu,blockdiag_g(S))`, and

\[
KL(p\|q_M)=\tfrac12\log\frac{\det\operatorname{blockdiag}_g(S)}{\det S}.
\]

For fixed grouping, mean and symmetric block covariance need the same number of scalars as information vector and symmetric precision blocks. Consequently **precision truncation cannot claim pure forward-KL superiority at that storage budget**.

The comparison with `S0^-1+blockdiag(J)` is a product comparison only if the retained prior precision is also block diagonal in those groups. For a dense cross-group prior the plug-in may not belong to this family; do not extend the dominance statement silently.

## 6. Lemma: truncating precision underestimates marginal uncertainty

Partition an SPD posterior precision Q into a group G and its complement. Gaussian elimination gives

\[
S_{GG}=(Q_{GG}-Q_{G,-G}Q_{-G,-G}^{-1}Q_{-G,G})^{-1}.
\]

The subtracted term is PSD. Inversion reverses the SPD order, hence

\[
\boxed{S_{GG}\succeq Q_{GG}^{-1}.}
\]

Thus precision truncation can lose the correct mean, the within-group uncertainty and cross-group dependence. Compare four controls: full posterior, natural blocks, exact mean with the same precision-block covariance, and exact mean with marginal covariance blocks. The first has greater storage; the latter three share a fixed grouping and storage count.

## 7. Modal phase coordinates and a cheaper counterexample

For block rotations `U=diag(U_1,...,U_M)` acting on complete cosine/sine pairs, and groups made from complete pairs,

\[
\mathcal B_g(UJU^T)=U\mathcal B_g(J)U^T.
\]

**Proof.** U has no entries between different modal groups; selecting principal groups commutes with the block congruence. Transform the prior as well:
`Q0'=UQ0U^T`, `h0'=Uh0`. Then inverse congruence and transformed natural parameters give `mu'=Umu`, `S'=USU^T`; moment block projection obeys the same relation.

This does not hold for arbitrary coordinate matchings `(02|13)` or `(03|12)`. Those existing baseline layouts remain useful numerical controls but are not declared phase-covariant physical groups.

The cheaper operator

\[
\mathcal I(J)=\bigoplus_m\tfrac12\operatorname{tr}(J_{mm})I_2
\]

is also phase-covariant: each modal trace is invariant under its rotation, and a scalar identity commutes with it. For three modes it uses 6 information-vector plus 3 trace scalars, not 19. Therefore phase covariance alone cannot justify full blocks. This is a coordinate change, not physical translation invariance of a damped waveform.

## 8. Direct low-rank and goal-oriented controls

Given prior covariance S0 and exact posterior S, form
`D=S0^-1/2(S0-S)S0^-1/2`. With its ordered eigenpairs `(d_i,u_i)`, the covariance

\[
S_r=S_0^{1/2}(I-\sum_{i=1}^r d_i u_i u_i^T)S_0^{1/2}
\]

is the prior-whitened negative-update family studied by Spantini et al. Pair it with the exact mean for the covariance-only control. Its stored factor needs `m*r` scalars, in addition to m mean entries and any nonshared prior/basis description. Degrees of freedom and finite-precision transmission cost are not equated.

For a full-row-rank target L, apply the same construction to
`S_Z0=L S0 L^T` and `S_Z=L S L^T`. This accounts for the goal, unlike blindly projecting a parameter-space truncation. The implemented dense oracle uses the full posterior and is **not** a reproduction of the paper's scalable matrix-free algorithm. All encoder solves are charged. A two-dimensional fixed goal can transmit its exact Gaussian moments in only five scalars; it does not thereby represent every other physical target.

## 9. Costs and stronger deployment boundary

The new six-dimensional reviewer witness uses a fixed, protocol-shared `4+2` grouping: 19 statistics and zero per-event layout entries for all three block controls. A variable grouping needs its identifier; a 19-value statistic vector is then not a 19-value total message. Do not confuse this witness with the existing adaptive 11-scalar four-dimensional study.

Natural likelihood statistics are additive over conditionally independent observation batches and reusable with a changed prior. With a fixed linear block operator, `B(sum J_i)=sum B(J_i)`. This is a standard algebraic property, not proof of a runtime advantage. Correlated views require their joint noise model. Switching the grouping after truncation cannot reconstruct discarded entries. Posterior moments can also support exact information updates if the full covariance is retained; only the constrained block approximation is at issue.

The primary single-window, fixed-prior accuracy comparison uses moment blocks as the default strong reference. Streaming, prior reuse and finite encoder computation are separately measured deployment conditions, not post-hoc excuses to rescue a losing parameterization.

## Witness and admission

The same-stem Notebook retains prior-predictive Monte Carlo, actual header round-trip and full-side-information null checks. New checks cover the product identity, Schur order, mean/variance/dependence decomposition, phase-prior transformation, trace-isotropic control and direct low-rank controls. Target ranking is checked in Theory 12's paired Notebook. No learned-method claim is admitted until the actual frozen LLapDiff target improves against these controls at declared total cost.
