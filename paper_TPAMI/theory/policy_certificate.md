# Finite-policy improvement after independent calibration

## Status and connection to the method

This is a paired, finite-family Hoeffding/Bonferroni specialization of established risk-control methodology, not a new distribution-free theorem. Learn then Test [@angelopoulos2025ltt] already supplies a much more general calibration/testing framework. The purpose here is to implement an honest rule for the **same frozen single, static-fusion and routed policies**. Neither a new directory nor this corollary establishes TPAMI-level novelty.

## Definitions and assumptions

Let training and model-selection data determine one reference policy $p_0$ and $J$ candidate policies $p_1,\ldots,p_J$. A policy includes its feature path, predictor(s), gate/fusion weights, target, preprocessing, and any posterior-draw protocol. All these objects, the family size, cost penalties $c_j$, margin $\delta\ge0$, and confidence level $\alpha\in(0,1)$ are fixed **before** viewing the certification sample. A static-fusion reference may be selected on an earlier disjoint source set. Conditional on that earlier training result:

A1. The $n$ calibration observations are iid original groups from a declared source law. All compared policies are evaluated on exactly the same groups. Windows and draws are averaged **within** each group before this analysis.

A2. The common group loss satisfies $0\le L_j(G)\le1$. Binary Brier loss meets this condition. Multiclass Brier divided by two also does. Raw Energy Score, cross-entropy, Gaussian NLL and macro-F1 do not meet it automatically. Clipping a score changes the target functional and may destroy propriety; this implementation never clips.

A3. $c_j$ are fixed, declared utility penalties. They are not noisy timings measured on these groups. For random latency, add a separate justified bound instead of inserting a sample mean as a known constant.

A4. For a target-law claim only, a declared $\beta\ge0$ satisfies, for all candidates,

$$
\mathbb E_t[L_0-L_j]\ge \mathbb E_s[L_0-L_j]-\beta.
$$

Costs are unchanged across these two laws. Source calibration does not establish A4. Without A4 the conclusion is source-law only; arbitrary domain shift has no certificate here.

Define the group-paired net improvement

$$
D_j=\mathbb E_s[L_0-L_j]-(c_j-c_0),\qquad
\widehat D_j=\frac1n\sum_{i=1}^n(L_0(G_i)-L_j(G_i))-(c_j-c_0).
$$

This comparison is of **fixed policy risks**, not a decomposition of the Bayes information term. A policy family can include a single arm, a real predictive-distribution mixture, or an acquisition-only fixed-arm selector. Its members need not be nested function classes.

## Lemma 1 — one-policy lower confidence bound

For $t>0$,

$$
\Pr\{D_j<\widehat D_j-t\}\le \exp(-nt^2/2).
$$

**Proof.** Each $L_0(G_i)-L_j(G_i)$ lies in $[-1,1]$, a range of width two. One-sided Hoeffding gives $\Pr(\overline X-\mathbb EX>t)\le\exp(-2nt^2/2^2)$. Subtracting the known constant cost difference from both means leaves the event unchanged. ∎

## Theorem 1 — simultaneous certification and a retain-reference decision

Set

$$
r_n=\sqrt{\frac{2\log(J/\alpha)}{n}},\qquad
B_j=\widehat D_j-r_n-\beta.
$$

Select a maximizer of $B_j$ only when $\max_j B_j>\delta$; otherwise return reference $p_0$. Under A1–A4, with probability at least $1-\alpha$ over the calibration groups,

$$
\boxed{
\mathcal R_t(p_{\rm selected})+c_{\rm selected}
\le\mathcal R_t(p_0)+c_0-\delta\,\mathbf1\{p_{\rm selected}\ne p_0\}.
}
$$

For $\delta=0$, the strict test still requires a positive bound before replacing the reference. The conservative decision is part of the specified statistical method, not a silent software fallback.

### Detailed proof

1. Substitute $r_n$ into Lemma 1. Each failure probability is at most $\alpha/J$.
2. A union bound ensures $D_j\ge\widehat D_j-r_n$ simultaneously for every frozen candidate, except on a set of probability at most $\alpha$.
3. A4 makes each target net improvement at least $D_j-\beta\ge B_j$ on that event.
4. Since all candidates share the event, selecting the largest **data-dependent** bound does not require an additional post-selection assumption. A selected candidate has net improvement greater than $\delta$.
5. If no bound passes, the deployed policy is the reference itself, whose net improvement is exactly zero. This yields the displayed weak inequality. ∎

## What is not guaranteed

The theorem bounds the population net risk of a selected fixed policy, not the realized finite test score. It is conservative and may fail to select a beneficial candidate. It does not certify an unrestricted neural router, optimize the representation, or establish target calibration. Selecting features, policies, loss clipping or hyperparameters on the certification sample invalidates A1's conditional setup; freeze them first or use a new independent calibration split. Repeated adaptive use of the same split is not covered.

The underlying earlier training randomness is conditioned on. Across five domains, separate per-domain $\alpha$ values do not yield a simultaneous 95% claim over all domains; preallocate their error budget or report separate guarantees. Adjacent chronological blocks are not iid just because their IDs differ. The iid certificate is not applied to ETT/USHCN unless a justified sampling/dependence extension is separately established; their blocked evaluation remains empirical.

## Executable falsification and interpretation

The same-stem Notebook checks the constant and selection algebra. `experiments/p19/certified_selection_demo.py` runs actual independent Bernoulli-event draws, a source-fitted static probability reference, two single predictors and an acquisition-conditioned hard selector. Four settings are executed: same best arm, complementarity, target-order reversal with an incorrect zero-shift assumption, and the **identical reversal observations** with an explicit shift allowance.

The output scores are binary Brier losses. The small declared cost penalties are toy utilities, not GPU timing results. Each setting has 512 source-fit events, 64 or 2048 independent calibration events, and 4096 independent test events. Three simulator seeds describe repeatability; they do not provide a separate population confidence interval.

The reversal control can exhibit negative test net gain when A4 is violated. This is an assumption failure, not a contradiction. The counterpart with a sufficient declared shift allowance retains the reference; it is not evidence that $\beta$ can be learned without target information.

## References

- Hoeffding (1963), *Probability Inequalities for Sums of Bounded Random Variables*, JASA 58(301):13–30.
- Angelopoulos, Bates, Candès, Jordan and Lei (2025), *Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control*, Annals of Applied Statistics, DOI 10.1214/24-AOAS1998; inspected preprint arXiv:2110.01052, Sections 2.1–2.3.
- The comparison with fixed and joint expert learning is in `../related_work.md`; no H-consistency theorem from that literature is silently inherited.
