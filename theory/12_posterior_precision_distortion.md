# Theory 12 — Posterior error, statistical semantics, and shape across a diffusion schedule

## Scope and notation

This file retains the Gaussian precision/natural-parameter calculation and its tightened bound. The added results address statistical meaning and non-Gaussian shape; they use standard Gaussian scoring, conditional expectation, and Gaussian convolution, not a new general information theory. The same-stem Notebook gives finite witnesses for the results; finite execution is not a proof or novelty assessment. Spantini et al. (2015, 2017), Oko et al. (2025), Gneiting and Raftery (2007), and Seitzer et al. (ICLR 2022) are direct antecedents.

The full decoder condition is C=(H,a_consumed), including every consumed field. The physical coefficient beta, reference latent Z0, and a chosen target functional U=L vec(Z0) are distinct random variables. In the Gaussian oracle only, a target may instead be U=L beta. A fixed reference encoder and source-fitted normalization define Z0 before comparisons. No statement below identifies physical coefficients with arbitrary learned latent coordinates.

## 1. Retained Gaussian posterior discrepancy

Let

\[
P=N(\mu,\Lambda^{-1}),\quad\mu=\Lambda^{-1}\eta,
\qquad Q=N(\widetilde\Lambda^{-1}\widetilde\eta,\widetilde\Lambda^{-1}),
\quad\Lambda,\widetilde\Lambda\succ0.
\]

Both use the same observation, prior, coordinates and base measure. Define symmetric roots and

\[
E=\Lambda^{-1/2}(\widetilde\Lambda-\Lambda)\Lambda^{-1/2},\quad
r=\Lambda^{-1/2}(\widetilde\eta-\eta),\quad v=\Lambda^{-1/2}\eta,
\quad w=r-Ev,\quad\kappa=\lambda_{\min}(I+E)>0.
\]

### Lemma 12.1: whitening

Under y=Lambda^(1/2)(beta-mu), P becomes N(0,I) and Q becomes

\[
N((I+E)^{-1}w,(I+E)^{-1}).
\]

**Proof.** Factor the approximate precision as Lambda^(1/2)(I+E)Lambda^(1/2). Inverse congruence gives the transformed covariance. Its mean is `(I+E)^-1(v+r)-v=(I+E)^-1w`. Common invertible coordinate changes preserve KL. No commutativity is assumed.

### Proposition 12.1: exact error and tighter bound

\[
\boxed{2KL(P\|Q)=\operatorname{tr}E-\log\det(I+E)+w^T(I+E)^{-1}w.}
\]

**Proof.** Average the two Gaussian log densities in the whitened coordinates. The expectation of y is zero and of yy^T is I. Expanding the quadratic leaves the displayed trace, determinant and mean-displacement terms.

For e>-1,

\[
e-\log(1+e)=e^2\int_0^1\frac{t}{1+te}\,dt
\leq\frac{e^2}{2\min(1,1+e)}.
\]

Every point of the integration segment has denominator at least min(1,1+e). Sum over eigenvalues of E and use `(I+E)^-1 <= I/kappa` to obtain

\[
\boxed{KL(P\|Q)\leq
\frac{\|E\|_F^2}{4\min(1,\kappa)}+\frac{\|r-Ev\|^2}{2\kappa}.}
\]

The older denominator min(1,kappa)^2 is valid but looser; historical CSVs retain that older evaluation. For ||E||_2<1, kappa may be bounded by 1-||E||_2. The mean error in the Lambda norm is at most ||w||/kappa. Setting r=Ev cancels it; r=-Ev amplifies it. Large offline bounds do not imply useful online certification. Computing a full whitening is charged to the encoder/oracle; it is not an extra free decoder input.

## 2. Retained target-space Gaussian denoiser calculation

For a frozen full-row-rank L, transform the exact and approximate coefficient laws to `P_U=N(m,V)` and `Q_U=N(mq,W)`. For a common forward perturbation

\[
z_t=\alpha_tU+\sigma_t\epsilon,\quad\epsilon\sim N(0,I),\quad\sigma_t>0,
\]

let M=alpha^2 V+sigma^2 I, N=alpha^2 W+sigma^2 I, B=M^-1-N^-1 and delta=mq-m. Gaussian conditioning gives

\[
f_P(z)=\sigma M^{-1}(z-\alpha m),\qquad
f_Q(z)=\sigma N^{-1}(z-\alpha m_q).
\]

Writing y=z-alpha*m, which has mean zero and covariance M under P,

\[
f_P-f_Q=\sigma(By+\alpha N^{-1}\delta).
\]

The cross term vanishes on expectation, hence

\[
\boxed{D_t^{\epsilon}(P,Q;L)=\sigma^2[
\operatorname{tr}(BMB^T)+\alpha^2\delta^TN^{-2}\delta].}
\]

For a variance-preserving schedule and alpha>0, the x0 discrepancy is sigma^2*D_epsilon/alpha^2 and the v discrepancy is D_epsilon/alpha^2. At alpha=0 use the conditional means directly rather than divide by zero. This is a plug-in prediction discrepancy unless Q is the true induced compressed conditional. It is not a finite-sampler error bound.

Data processing does not preserve approximation rankings: for P=N(0,I2), Q_A=N((0,.9),I2), Q_B=N((1,0),I2), full KL is .405 versus .5. Projection to the second coordinate gives .405 versus 0. A better beta approximation can be worse for the declared target.

## 3. Statistical semantics do not follow from end-to-end denoising

### Proposition 12.2: reparameterization ambiguity

Let f(z,t,m(O),S(O)) be an arbitrary conditional network. For constants a,b>0 define m'=a*m, S'=b*S and f'(z,t,m',S')=f(z,t,m'/a,S'/b). The predictions and every loss depending only on them agree exactly. Positive definiteness is retained but mean/covariance semantics generally are not.

**Proof.** Substitute the definitions; f' equals f pointwise. Nothing in the end-to-end denoising objective selects a=1 or b=1.

This is a limitation of an unconstrained interpretation, not proof that the network fails. Without a statistical objective and fixed readout, call these **structured condition features**, not posterior moments.

### Proposition 12.3: what a Gaussian score does identify

Fix an input information set F, for example the frozen HSE token set and declared side information. Assume finite conditional second moments and a strictly positive-definite conditional covariance

\[
\mu_F=E[U|F],\quad V_F=\operatorname{Cov}(U|F)\succ0.
\]

For F-measurable m and S>0 define

\[
\ell_G(U;m,S)=\tfrac12[\log\det S+(U-m)^TS^{-1}(U-m)].
\]

The conditional excess expected score is

\[
\boxed{E[\ell_G(U;m,S)-\ell_G(U;\mu_F,V_F)|F]
=KL(N(\mu_F,V_F)\|N(m,S)).}
\]

**Detailed proof.** Expand U-m as `(U-mu_F)+(mu_F-m)`. The conditional cross term is zero and the quadratic expectation is `tr(S^-1 V_F)+(mu_F-m)^T S^-1(mu_F-m)`. Subtract the optimum expression `logdet V_F + dim(U)` and divide by two. This is the Gaussian forward-KL formula. Nonnegativity and equality characterize m=mu_F, S=V_F almost surely.

U need not be Gaussian. The score is strictly consistent for its first two moments, **not strictly proper for the unrestricted target distribution**. It cannot distinguish different conditional shapes with identical moments. Degenerate V_F, limited capacity, imperfect optimization and distribution shift need separate treatment. An auxiliary loss with a finite weight jointly optimized against denoising does not ensure its isolated population minimum is attained.

The implemented candidate therefore first fits and validates the fixed moment readout, then freezes the entire input feature path and the moment head before denoising. If the HSE continues changing, freezing only the final head is insufficient. With frozen HSE input F=H0(O,a), these are moments conditional on F, not automatically the full O posterior. No finite probe proves exact calibration.

## 4. Same moments can lose conditional shape at every nontrivial noise level

Let O be balanced binary, and

\[
p(U|O=0)=N(0,1),\qquad
p(U|O=1)=\tfrac12N(-.95,.0975)+\tfrac12N(.95,.0975).
\]

Both have mean 0 and variance 1. A true moment-only code S(O) is constant. The exact compressed law is their mixture, not a Gaussian plug-in.

### Proposition 12.4: exact shape-loss expression

Write p_j,t for the Gaussian-smoothed target density at observation type j and f_j,t for its optimal epsilon prediction. Let p_t=(p_0,t+p_1,t)/2 and pi_j(z)=p_j,t(z)/(p_0,t(z)+p_1,t(z)). Then

\[
\boxed{R_S^*(t)-R_O^*(t)
=\int p_t(z)\pi_0(z)\pi_1(z)
\|f_{0,t}(z)-f_{1,t}(z)\|^2\,dz.}
\]

**Proof.** The optimal compressed predictor is `pi_0 f_0+pi_1 f_1` by conditional expectation. For two vectors a,b with weights pi_0,pi_1, their weighted variance is pi_0*pi_1*||a-b||^2. Apply the nested-information projection identity in Theory 10 and integrate over z. Both weights are positive because Gaussian-smoothed densities are positive.

For any alpha>0, sigma>0, and distinct target probability laws with finite denoising risk, the integral is strictly positive. To see this, zero gap would make f_0=f_1 almost everywhere. The conditional score identity `f_j=-sigma*grad log p_j,t` then makes the log-density ratio constant; normalization makes the smoothed densities equal. Their Fourier transforms are the original characteristic functions evaluated at alpha times frequency, multiplied by the nonzero Gaussian characteristic function. Equality therefore implies identical original laws, a contradiction. Smoothness of the Gaussian convolution justifies the score argument; the finite-risk assumption rules out undefined integrals.

For alpha=.8 and sigma=.6 the independent numerical integral is approximately **0.0224274361995**. This is a finite witness, not a trained LLapDiff score. If extra side information or a residual code distinguishes O, the moment-only collision no longer applies to the whole condition. The theorem also does not apply to arbitrary approximate moment fields: finite estimation errors may themselves encode condition identity. Use oracle-moment replacement and route-specific probes to avoid crediting such leakage to correct moment semantics.

### Corollary: why an additional residual is a legitimate hypothesis

For a *fixed* S and additional R, nested conditioning gives

\[
R_S^*(t)-R_{S,R}^*(t)
=E\|E[\epsilon|z_t,S,R,a]-E[\epsilon|z_t,S,a]\|^2\geq0.
\]

This does not prove dominance under a fixed total budget: allocating space to S may remove useful coordinates from R. It also does not promise that a neural residual learns the missing shape. Those are the primary experiments, not assumptions.

## 5. A complete schedule, not a selected time

For declared training-time distribution p_train, nonnegative weights w and prediction parameterization U_t, evaluate

\[
\boxed{\mathcal D_{train}=\sum_t p_{train}(t)w(t)D_t^{U}.}
\]

Integrating the exact nested-projection identities preserves equality when integrable. Use per-coordinate reduction when the native loss averages coordinates. Time probabilities, parameterization, target masks and weight normalization must match training. Batch-normalized weights depend on the batch: replace the scalar formula by expectation over actual batches; do not silently substitute a uniform-time average.

A ranking reversal is already visible for true N(0,1), Q_A=N(0,.2), Q_B=N(.5,1). At alpha^2=.1 epsilon discrepancy is .0068053 versus .0225; at alpha^2=.9 it is .6612245 versus .0225. Neither row determines the training-average ranking.

The source-translated cosine diagnostic explicitly chooses uniform t=1..999, unweighted v prediction. `paper/export_llapdiff_schedule.py` instead imports the installed native scheduler and exports explicit uniform-time/non-batch-normalized weights. It does not export reverse-sampling times or infer a configuration silently. A discrepancy between these two routes must be reported, not hidden by rescaling.

## 6. Shared supervision does not order arbitrary encoders, but it orders this pair

Fix the trained checkpoint and the data law. The complete available feature input is `C_F=(F,mask,side)`. Let `R=g_theta(C_F)` be the source-supervised ordinary code consumed by B1-aux, and let

\[
H_M=T(R)=[m(R),\operatorname{vech}(\operatorname{chol}S(R)),R_{s+1:q}].
\]

The moment-head scoring gradient passes through the same g_theta. At stage two both g_theta and the head are fixed. Proposition 12.3 is then interpreted conditionally on **R**, not automatically on the richer C_F or raw observation. During source training R itself is learned, so fixed-R consistency is not a guarantee of joint optimization.

### Proposition 12.5: nested Bayes loss and finite-predictor decomposition

Let X include the actual noisy latent, diffusion time and any common consumed side inputs. Let V be the square-integrable native regression target. Assume all fitted functions are evaluated on an independent test event, conditionally on the fixed training outcome. Put

\[
f_R=E[V|X,R],\quad f_M=E[V|X,H_M],\quad
A_j=E\|\widehat f_j-f_j\|^2.
\]

Then

\[
\boxed{\mathcal R(\widehat f_M)-\mathcal R(\widehat f_R)
=E\|f_R-f_M\|^2+A_M-A_R.}
\]

**Detailed proof.** Since H_M is measurable with respect to R, the sigma-algebras generated by `(X,H_M)` are contained in those generated by `(X,R)`. Expand `V-f_M=(V-f_R)+(f_R-f_M)`. The expectation of the cross term is zero because `E[V-f_R|X,R]=0`. Thus the difference of Bayes risks is the first nonnegative term. For either actual predictor expand `V-hat f_j=(V-f_j)+(f_j-hat f_j)` and condition on its own information set; the cross term again vanishes. Subtract the two equalities. This proves the identity. The losses must use the same target, schedule, mask reduction and measure; arbitrary differently weighted training scores are not comparable by this equation.

When mutual informations are defined and finite, data processing similarly gives `I(Z0;H_M|a) <= I(Z0;R|a)`. M cannot recover Bayes information absent from this comparator. Its possible advantage is lower finite fitting/accessibility error that outweighs any additional Bayes loss. This is not an ordering between arbitrary independently learned equal-dimensional messages. It does not contradict the possibility that two non-nested encoders retain different amounts of target information.

A finite witness illustrates the distinction: R is uniform on `{-1,0,1}`, V=R^2 and M=R^2. Both unrestricted Bayes risks are zero. An affine predictor using R has risk 2/9, while an affine predictor using M has risk zero. This illustrates computational accessibility only; it is not evidence about LLapDiff. If instead V=R and M=R^2, the Bayes loss is 2/3 and cannot be repaired from M alone.

## 7. Explicit covariance constraints and native batch weighting

### Lemma 12.3: the covariance floor changes the statistical optimum

For fixed R, mean mu, covariance V positive semidefinite and lambda>0, minimize the conditional Gaussian score over m and the **closed** family `S >= lambda I`. Its minimizer is

\[
m^*=\mu,\quad S^*=U\operatorname{diag}(\max(v_i,\lambda))U^T,
\quad V=U\operatorname{diag}(v_i)U^T.
\]

**Detailed proof.** For fixed S the positive quadratic mean-error term is minimized by m=mu. Set P=S^-1, so `0<P<=lambda^-1 I`. The remaining objective is `-logdet P+tr(PV)`, strictly convex in P. In the eigenbasis of V, averaging P over coordinate sign flips preserves feasibility and the trace term and cannot increase the objective by convexity. The optimum is therefore diagonal in that basis. Each coordinate minimizes `-log p_i+v_i p_i` on `0<p_i<=lambda^-1`, giving `p_i=1/max(v_i,lambda)`. Invert to obtain S*. Uniqueness follows from strict convexity.

The implementation `S=BB^T+lambda I` with strictly positive triangular diagonal lies in the open interior. It can approach but need not attain a boundary eigenvalue lambda. The floor is part of the model, in target-squared units; do not add an undeclared jitter or interpret the constrained optimum as the unconstrained covariance where the floor is active.

At finite training samples, exact interpolation of the mean with `S=epsilon I` gives `.5*d*log(epsilon) -> -infinity`. Positive definiteness alone does not prevent likelihood collapse. A rising validation score is not sufficient to diagnose its cause; logdet, Mahalanobis and eigenvalues distinguish potential variance failure from other overfitting.

### Finite batch-weighting counterexample

Take independent batch draws with `(w,D)=(1,0)` or `(9,1)`, each with probability one half. For a batch of size two, normalized weighted losses are `0,.9,.9,1` in the four equally likely outcomes. Therefore

\[
E\left[\frac{\sum_iw_iD_i}{\sum_iw_i}\right]=.7
\ne .9=\frac{E[wD]}{E[w]}.
\]

The original native loss must consequently be reconstructed with the realized batch denominator. An exported one-dimensional schedule does not certify a batch-normalized objective. This counterexample is an execution check, not a new model or theorem contribution.

## 8. Contribution and failure boundary

The proposed intervention is a global statistically supervised prefix plus an ordinary tail within fixed K*D. Its primary comparator sends the full shared-supervised R from the same selected checkpoint. This deliberate nesting isolates accessibility rather than added information. Its value is unestablished until the same original LLapDiff improves under matched actual access and measured costs. The Gaussian score, projection identity, convolution injectivity, reparameterization argument and matrix bound are supporting tools and boundary results, not separately advertised method innovations.

No result here establishes unseen-system identifiability, superiority of diffusion over mixtures, calibrated finite-network predictions, or a foundation model for unrelated time series. Flow Matching remains outside the active method.
