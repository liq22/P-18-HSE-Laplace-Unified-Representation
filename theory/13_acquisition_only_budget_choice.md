# Theory 13 — Choosing a coupling layout without reading hidden targets

## Status and relation to prior work

This is an exact prior-predictive calculation in a declared Gaussian oracle. Selecting the minimum of a finite candidate set is elementary; it is not a novel global optimization theorem. Bayesian low-rank and goal-oriented approximation already optimize posterior losses (Spantini et al., 2015, DOI 10.1137/140977308; 2017, DOI 10.1137/16M1082123). Our distinct constraint is a directly decodable, fixed-layout acquisition header, not a free low-rank update.

## 1. Assumptions

The latent coefficient prior is `beta~N(0,S0)`, `S0` SPD, fixed from declared source information or the known simulator. The acquisition is `x=A beta+epsilon`, with known SPD noise covariance R independent of beta. Define

$$J=A^TR^{-1}A,\quad b=A^TR^{-1}x,\quad
\Lambda=S_0^{-1}+J,\quad\Sigma=\Lambda^{-1}.$$

A candidate layout s retains `J_s` and all b. Its approximate precision is `Q_s=S0^-1+J_s`, required SPD. It produces `q_s=N(Q_s^-1 b,Q_s^-1)`. This is a plug-in model, not automatically the true conditional given the compressed header. Both posterior laws refer to the same beta and same observation.

The candidate layout may depend on the acquisition design J and declared prior, not the realized coefficient, task label or validation/test loss. Data-dependent masks would require conditioning the joint law on the selection mechanism; here all mask/timestamp designs are fixed independently of beta.

## 2. Lemma 13.1 — covariance of the full posterior mean

For `mu=E[beta|x,A,R]`,

$$E_x[\mu]=0,\qquad\operatorname{Cov}_x(\mu)=S_0-\Sigma.$$

### Proof

The tower property gives `E[mu]=E[beta]=0`. The law of total covariance gives

$$S_0=E_x[\operatorname{Cov}(\beta|x,A,R)]+\operatorname{Cov}_x(E[\beta|x,A,R]).$$

The correctly specified Gaussian posterior covariance is the constant Sigma. Subtract it to obtain the statement. For non-Gaussian priors the posterior covariance generally depends on x and this exact constant formula is unavailable. QED.

## 3. Theorem 13.1 — design-only expected posterior KL

Let `D_s=Q_s^-1 Lambda-I`. Then

$$\boxed{
\overline K_s(J)=E_x\operatorname{KL}(p(\beta|x,A,R)\|q_s)
=\frac12\left[
\operatorname{tr}(Q_s\Sigma)-m+\log\det\Lambda-\log\det Q_s
+\operatorname{tr}\{Q_sD_s(S_0-\Sigma)D_s^T\}
\right].
}$$

### Detailed proof

The approximate mean is `Q_s^-1 b=Q_s^-1 Lambda mu`, so its displacement from mu is `D_s mu`. The Gaussian KL is

$$\tfrac12[\operatorname{tr}(Q_s\Sigma)-m+\log\det\Lambda-\log\det Q_s
+\mu^TD_s^TQ_sD_s\mu].$$

Only the last term depends on x. Use `E[u^TBu]=tr(B Cov(u))+(Eu)^TB(Eu)` and Lemma 13.1. Cyclic invariance of trace yields the displayed formula. It requires neither the hidden beta nor an observed task label. QED.

## 4. Corollary — finite-budget choice and its strict limits

For a predeclared finite layout set S with equal encoded storage, choose

$$s^*(J)=\arg\min_{s\in S}\overline K_s(J).$$

Then `Kbar_s* <= Kbar_s` for every candidate. Ties use the first listed layout. This is optimal only for this prior, forward model, approximate decoder, loss and candidate family. It is not a bound for arbitrary neural HSEs, an optimum over all token encodings, or a guarantee under prior shift.

The selected layout identifier must be transmitted or inferable from the same actual side input. Otherwise the decoder cannot reconstruct the intended matrix and the premise fails. If the layout identifier reveals acquisition information, that information is part of H, not a hidden free resource.

## 5. Implemented equal-layout-budget experiment

For two oscillatory modes beta has four coordinates. The three layouts are perfect matchings:

```
0: (0,1), (2,3) — within-mode cosine/sine
1: (0,2), (1,3)
2: (0,3), (1,2)
```

Each retains diagonal J and two off-diagonal entries. Permuting coordinates makes each retained matrix two principal 2x2 blocks, so it is PSD when J is PSD. Adding the prior makes its precision SPD. The actual header contains 4 score entries, 4 diagonal entries, 2 coupling entries and 1 layout code: 11 stored scalars. The full oracle uses 15 including its code and is not budget-matched. A padded diagonal baseline has the same allocated storage but less informative content.

Two selectors are compared: the above risk oracle and the simpler maximum retained squared-coupling rule. Both inspect the same full design at the encoder and send the same header layout. Their compute is not matched: the risk oracle solves three small posterior problems. If they select the same layouts, prefer the cheaper rule; do not claim a new practical benefit for the risk oracle.

## 6. Full-side-input control and physical scope

If all decoders actually receive A and R, they can reconstruct full J regardless of the header. Their Bayes-information advantage is zero. The implementation explicitly makes this reconstruction instead of pretending the side inputs were unused.

The finite sampled designs evaluate damped sinusoids at fixed-P,K timestamps, with optional jitter and missing entries. They do not resample an acquired noisy high-rate record, model anti-alias filter hardware, or establish a PHM label relation. Noise is independently generated for separate acquisitions and shared across methods within an acquisition.

## 7. Witness and interpretation

The Notebook verifies the design-only expectation by independent prior-predictive Monte Carlo, header round-trip without hidden J, exact finite-family choice, and the full-side-input null. The 24-cell waveform sweep is separately reported in `paper/results_sampled.md`. Its risk oracle and magnitude selector select identical layouts in every cell. This is retained as a negative result for additional selector complexity.

Any future learned contribution must exceed the simpler selector at fixed P,K,D, include layout information in the budget, account for encoder computation, and use the same LLapDiff architecture and targets. Theorem 12 bounds the resulting Gaussian plug-in distortion; it does not make the plug-in the exact compressed posterior.

## 8. Strong same-storage control: match posterior moments, not likelihood precision

For a fixed partition into the two declared coordinate pairs, consider all Gaussian q whose covariance is block diagonal in that partition. For any full Gaussian p=N(mu,Sigma), the forward-KL minimizer is

$$q_{\rm moment}=N(\mu,\operatorname{blockdiag}(\Sigma)).$$

**Proof.** Write its block means and covariances as `(a_b,V_b)`. The q-dependent part of twice the KL is a sum of

$$\log\det V_b+\operatorname{tr}(V_b^{-1}\Sigma_{bb})
+(a_b-\mu_b)^TV_b^{-1}(a_b-\mu_b).$$

For fixed V_b the unique minimizing mean is mu_b. Writing `V_b=Sigma_bb^(1/2) B Sigma_bb^(1/2)`, the remaining variable part is `logdet B+tr(B^-1)`. Every eigenvalue lambda>0 minimizes `log(lambda)+1/lambda` at lambda=1. Thus V_b=Sigma_bb. Substitution gives

$$\boxed{\operatorname{KL}(p\|q_{\rm moment})=
\tfrac12\log\frac{\det\operatorname{blockdiag}(\Sigma)}{\det\Sigma}.}$$

It follows that moment matching is no worse in forward KL than the precision plug-in for the same partition, preserves the exact mean and all univariate marginals, but generally loses cross-block dependence. This is the standard information-projection property, not a new theorem of Gaussian families. It explains why marginal calibration alone does not establish joint sufficiency.

The implemented control transmits four exact posterior means, four variances, two selected covariances and one pattern code: still 11 scalars. It requires full posterior computation at the encoder, so equal header storage does not mean equal computation or a learned-model advantage. The best moment partition minimizes the displayed log-determinant ratio over the same three partitions. Unknown priors, unknown operators and non-Gaussian posteriors are not covered. This strong baseline must be retained before proposing a learned posterior token.
