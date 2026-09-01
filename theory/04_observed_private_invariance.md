# Theorem 4 — Pathwise invariance of observed-private modes

## Status

**Proved under the block-projection assumptions stated below.**

## Purpose

Observed-private information is physically available in the current acquisition domain but not common to all domains. The method should not erase it in the name of invariance. This theorem gives a structural guarantee: the private coordinate is constant along the unified transport path.

## 1. Assumptions

Let

\[
P_c,
P_p,
P_u
\]

be mutually orthogonal projectors satisfying

\[
P_c+P_p+P_u=I.
\]

Consider the Itô process

\[
dZ_t=b_t(Z_t)dt+\sigma_t(Z_t)dW_t.
\]

Assume the private block receives neither drift nor diffusion:

\[
P_pb_t(z)=0
\quad
\text{for all }(t,z),
\tag{4.1}
\]

\[
P_p\sigma_t(z)=0
\quad
\text{for all }(t,z).
\tag{4.2}
\]

The second condition means every column of the diffusion matrix is orthogonal to the private subspace.

## 2. Lemma 4.1 — projection commutes with the stochastic differential

### Statement

For a constant linear projector \(P_p\),

\[
d(P_pZ_t)=P_p\,dZ_t.
\]

### Proof

The map \(f(z)=P_pz\) is linear. Its Jacobian is the constant matrix \(P_p\), and its Hessian is zero. Itô's formula therefore gives

\[
df(Z_t)
=P_pdZ_t
+\frac12\operatorname{tr}
\left(
\sigma_t\sigma_t^\top\nabla^2f
\right)dt.
\]

The Hessian term vanishes, so

\[
d(P_pZ_t)=P_pdZ_t.
\]

∎

## 3. Theorem 4 — private coordinates are pathwise constant

### Statement

Under Equations (4.1)–(4.2),

\[
\boxed{
P_pZ_t=P_pZ_0
\quad\text{for all }t\in[0,1]
\quad\text{almost surely}
}
\]

### Detailed proof

By Lemma 4.1,

\[
d(P_pZ_t)
=
P_pb_t(Z_t)dt
+
P_p\sigma_t(Z_t)dW_t.
\]

Using the two block conditions,

\[
d(P_pZ_t)=0\,dt+0\,dW_t=0.
\]

Integrating from \(0\) to \(t\),

\[
P_pZ_t-P_pZ_0
=
\int_0^t0\,ds
+
\int_0^t0\,dW_s
=0.
\]

Thus \(P_pZ_t=P_pZ_0\) almost surely for every time. ∎

## 4. Corollary 4.1 — exact preservation of every private statistic

For any measurable function \(g\) for which the expectation exists,

\[
g(P_pZ_t)=g(P_pZ_0)
\quad\text{almost surely},
\]

and therefore

\[
\mathbb E[g(P_pZ_t)]
=
\mathbb E[g(P_pZ_0)].
\]

Means, covariances, class probes, and reconstruction functions of the private coordinate are preserved in the exact mathematical model.

## 5. Corollary 4.2 — mutual information is preserved

Let \(Y\) be any random variable jointly distributed with \(Z_0\). Because

\[
P_pZ_t=P_pZ_0
\quad\text{almost surely},
\]

the generated sigma-algebras coincide up to null sets:

\[
\sigma(P_pZ_t)=\sigma(P_pZ_0).
\]

Hence

\[
\boxed{
I(Y;P_pZ_t)=I(Y;P_pZ_0)
}
\]

whenever the mutual information is well defined.

This is stronger than a penalty that merely encourages the two values to be close.

## 6. Corollary 4.3 — deterministic flow form

For an ODE

\[
\dot Z_t=v_t(Z_t)
\]

with \(P_pv_t(z)=0\), the same proof without stochastic terms gives

\[
P_pZ_t=P_pZ_0.
\]

## 7. Approximate implementation bound

A numerical implementation may leak a small private update. Suppose

\[
\|P_pb_t(Z_t)\|
\leq
\varepsilon_b(t),
\]

and

\[
\|P_p\sigma_t(Z_t)\|_F
\leq
\varepsilon_\sigma(t).
\]

Then

\[
P_pZ_t-P_pZ_0
=
\int_0^tP_pb_sds
+
\int_0^tP_p\sigma_sdW_s.
\]

Using \(\|a+b\|^2\leq2\|a\|^2+2\|b\|^2\), Cauchy–Schwarz, and Itô isometry,

\[
\mathbb E\|P_pZ_t-P_pZ_0\|^2
\leq
2t\int_0^t\varepsilon_b(s)^2ds
+
2\int_0^t\varepsilon_\sigma(s)^2ds.
\]

This gives a direct numerical tolerance target.

## 8. Failure boundaries

1. If the projector is learned as a state-dependent function \(P_p(Z_t)\), Itô derivatives of the projector appear; exact invariance no longer follows.
2. If shared and private blocks are mixed by a downstream projection before the invariant is checked, private preservation may be lost after the transport.
3. Identity preservation protects information already assigned to the private block. It does not prove the assignment is physically correct.
4. Quantization or finite precision can change a coordinate even when the continuous model does not.

## 9. Experimental implication

Every implementation must report

\[
\Delta_p
=
\max_i
\|P_pZ_1^{(i)}-P_pZ_0^{(i)}\|.
\]

The scientific contract requires this quantity to be zero up to declared numerical tolerance for the structural model. A soft loss with a non-zero residual is a different method and cannot use the theorem unchanged.
