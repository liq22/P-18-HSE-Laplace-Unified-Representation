# Theorem 21 — Perturbation of observable-support projectors

## Status

**Davis–Kahan-type finite-dimensional perturbation bound.**

## Purpose

Exact intersections of estimated dense projectors can collapse under small
operator errors. The relevant stability quantity is the spectral gap around the
observable/unobservable split.

## 1. Setup

Let \(G\) be a symmetric structural Gramian with ordered eigenvalues. Let
\(P\) project onto the selected observable eigenspace. Let

\[
\widehat G=G+E
\]

and let \(\widehat P\) be the corresponding projector with the same selected
dimension.

Assume the selected and unselected spectra of \(G\) are separated by

\[
\gamma
=
\min_{\lambda\in\Lambda_{\mathrm{sel}},
      \mu\in\Lambda_{\mathrm{unsel}}}
|\lambda-\mu|
>0.
\]

## 2. Theorem 21.1 — projector perturbation

If

\[
\|E\|_2<\frac{\gamma}{2},
\]

then

\[
\boxed{
\|\widehat P-P\|_2
\leq
\frac{2\|E\|_2}{\gamma}.
}
\]

### Proof sketch with the key steps

The spectral separation ensures that the perturbed selected cluster remains
separated from the perturbed unselected cluster by Weyl's eigenvalue bound.
The Davis–Kahan sin-\(\Theta\) theorem gives

\[
\|\sin\Theta(\widehat{\mathcal U},\mathcal U)\|_2
\leq
\frac{\|E\|_2}{\gamma-\|E\|_2}.
\]

For orthogonal projectors onto equal-dimensional subspaces,

\[
\|\widehat P-P\|_2
=
\|\sin\Theta\|_2.
\]

Because \(\|E\|_2<\gamma/2\),

\[
\frac{\|E\|_2}{\gamma-\|E\|_2}
\leq
\frac{2\|E\|_2}{\gamma}.
\]

This proves the bound. ∎

## 3. Lemma 21.1 — fixed-slot Rayleigh-score perturbation

For a unit modal vector \(u_k\),

\[
g_k=u_k^\top Gu_k,
\qquad
\widehat g_k=u_k^\top\widehat Gu_k.
\]

Then

\[
\boxed{
|\widehat g_k-g_k|
\leq
\|E\|_2.
}
\]

### Proof

\[
|\widehat g_k-g_k|
=
|u_k^\top Eu_k|
\leq
\|E\|_2\|u_k\|_2^2
=
\|E\|_2.
\]
∎

## 4. Corollary 21.1 — soft-weight perturbation

Combining Lemma 21.1 with Theory 15,

\[
\boxed{
|\widehat o_{d,k}-o_{d,k}|
\leq
\frac{\|E\|_2}{4T_o}.
}
\]

## 5. Implication for intersections and unions

The four-way roles depend on multiple domain projectors. A small per-domain
error does not guarantee stable intersection dimension when the common
directions have a small multi-domain spectral margin. Therefore the experiment
must report:

- per-domain spectral gap;
- common-support margin;
- projector distance;
- slot-role flips.

The fixed-slot implementation avoids uncontrolled basis rotation but still
needs the Rayleigh-score margin.

## 6. Failure boundaries

1. The bound is vacuous when \(\gamma\) is small.
2. The selected dimension can change when perturbations cross the threshold.
3. The bound assumes symmetric Gramian perturbations.
4. It does not estimate \(E\) from data.
5. Exact projector intersections can be unstable even when individual
   projectors are moderately accurate.

## 7. Experimental implication

Perturb sensor response, noise covariance and sampling support by controlled
amounts. Verify that observed projector error scales with
\(\|E\|_2/\gamma\). Near-threshold slots should be reported as uncertain rather
than assigned a confident role.
