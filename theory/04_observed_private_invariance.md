# Theorem 4 — Pathwise invariance of observed-private modes

## Status

**Proved under the fixed-projector block conditions stated below.**

## Purpose

Observed-private information is available in the current acquisition domain but
not common to every source domain. The representation must not erase it in the
name of canonicalization. This theorem gives a structural guarantee: the
observed-private coordinate remains constant along the transport path.

## 1. Assumptions

Let

\[
P_c,
P_p,
P_m,
P_0
\]

be mutually orthogonal constant projectors satisfying

\[
P_c+P_p+P_m+P_0=I.
\]

Consider the Itô process

\[
dZ_t=b_t(Z_t)dt+\sigma_t(Z_t)dW_t.
\]

Assume the private block receives neither drift nor diffusion:

\[
P_pb_t(z)=0,
\tag{4.1}
\]

\[
P_p\sigma_t(z)=0
\tag{4.2}
\]

for all admissible \((t,z)\). The second condition means every column of the
diffusion matrix is orthogonal to the private subspace.

## 2. Lemma 4.1 — a constant projection commutes with the stochastic differential

For the linear map \(f(z)=P_pz\),

\[
d(P_pZ_t)=P_p\,dZ_t.
\]

### Proof

The Jacobian of \(f\) is \(P_p\), and its Hessian is zero. Itô's formula
therefore has no second-order correction. ∎

## 3. Theorem 4 — private coordinates are pathwise constant

Under Equations (4.1)--(4.2),

\[
\boxed{
P_pZ_t=P_pZ_0
\quad
\text{for all }t\in[0,1]
\quad
\text{almost surely}.
}
\]

### Detailed proof

Lemma 4.1 gives

\[
d(P_pZ_t)
=
P_pb_t(Z_t)dt
+
P_p\sigma_t(Z_t)dW_t.
\]

Both terms vanish by assumption, hence

\[
d(P_pZ_t)=0.
\]

Integrating from zero to \(t\) proves the result. ∎

## 4. Corollary 4.1 — private statistics are preserved

For any measurable function \(g\) for which the expectation exists,

\[
g(P_pZ_t)=g(P_pZ_0)
\quad\text{almost surely},
\]

and therefore their expectations agree.

## 5. Corollary 4.2 — private mutual information is preserved

For any jointly distributed task variable \(Y\),

\[
I(Y;P_pZ_t)=I(Y;P_pZ_0)
\]

whenever the mutual information is well-defined, because the two coordinates
are almost surely identical.

## 6. Corollary 4.3 — deterministic Flow form

For

\[
\dot Z_t=v_t(Z_t)
\]

with \(P_pv_t=0\), the same argument gives

\[
P_pZ_t=P_pZ_0.
\]

## 7. Approximate implementation bound

If

\[
\|P_pb_t(Z_t)\|
\leq
\varepsilon_b(t)
\]

and

\[
\|P_p\sigma_t(Z_t)\|_F
\leq
\varepsilon_\sigma(t),
\]

then Itô isometry and Cauchy--Schwarz give

\[
\mathbb E\|
P_pZ_t-P_pZ_0
\|^2
\leq
2t\int_0^t\varepsilon_b(s)^2ds
+
2\int_0^t\varepsilon_\sigma(s)^2ds.
\]

This is the declared tolerance target when a numerical implementation does not
obtain exact zero.

## 8. Relation to the other blocks

The theorem permits non-zero shared and recoverable-missing dynamics. The
global-null block is separately excluded from data-driven transport. Private
identity does not require the shared and missing generators to commute.

## 9. Failure boundaries

1. If \(P_p\) depends on the state, derivatives of the projector enter Itô's
   formula.
2. A downstream projection can mix the preserved private coordinate with other
   blocks after this theorem has been applied.
3. Identity protects whatever was assigned to the private block; it does not
   prove that the assignment is physically correct.
4. Quantization and finite precision can introduce non-zero drift.
5. The theorem does not imply that identity transport is unconstrained-optimal
   for correlated shared/private distributions; Theorem 11 treats only a
   product special case.

## 10. Experimental implication

Every implementation must report

\[
\Delta_p
=
\max_i
\|
P_pZ_1^{(i)}-P_pZ_0^{(i)}
\|.
\]

The structural method requires \(\Delta_p\) to be zero up to a declared
numerical tolerance. A soft penalty with non-zero residual defines a different
method and cannot cite this theorem unchanged.
