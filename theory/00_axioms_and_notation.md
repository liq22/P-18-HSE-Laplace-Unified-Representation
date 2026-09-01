# Axioms and notation

## Status

This document fixes the mathematical universe used by the remaining theory files. It is not itself an empirical claim. Every theorem in this repository is conditional on the axioms that it explicitly imports from this file.

## 1. Spaces

### Axiom A0 — finite-dimensional modal state

The local physical state over one analysis window is represented in a finite-dimensional real Hilbert space

\[
\mathcal H = \mathbb R^m
\]

with Euclidean inner product \(\langle x,y\rangle=x^\top y\) and norm \(\|x\|_2\).

This is a local approximation. It does not assert that an entire machine is globally finite-dimensional or globally linear.

### Axiom A1 — acquisition domains

There is a finite source-domain set

\[
\mathcal D_s=\{1,\ldots,D\}.
\]

For each domain \(d\), the observation space is \(\mathcal Y_d=\mathbb R^{n_d}\), and the locally linearized acquisition model is

\[
Y_d=A_d\Theta+\varepsilon_d,
\]

where \(A_d:\mathcal H\to\mathcal Y_d\) is a bounded linear operator, \(\Theta\in\mathcal H\) is the modal state, and \(\varepsilon_d\) is measurement error.

The operator \(A_d\) may represent sensor response, channel selection, anti-alias filtering, sampling times, missing observations, and a local decoder Jacobian.

### Axiom A2 — observation-noise model

For each source domain, the noise covariance \(\Sigma_d\in\mathbb R^{n_d\times n_d}\) is symmetric positive definite. The noise-weighted Gramian is

\[
G_d=A_d^\top\Sigma_d^{-1}A_d.
\]

Positive definiteness is used only to define a non-degenerate observation metric. If a covariance is singular, the model must first be restricted to its supported observation subspace; the implementation does not silently use a pseudoinverse.

### Axiom A3 — observable threshold

A fixed source-only threshold \(\tau_o>0\) defines the effectively observable modal subspace

\[
\mathcal H_d^o
=
\operatorname{Range}
\left(
\mathbf 1_{[\tau_o,\infty)}(G_d)
\right).
\]

The threshold is part of the scientific protocol. It cannot be selected using a held-out target domain.

## 2. Laplace modal coordinates

### Axiom A4 — local stable modal approximation

On a finite physical window \([0,T]\), the latent physical trajectory admits

\[
s(t)=\Phi(t;\Lambda)\Theta+r(t),
\]

where \(\Phi\) is a finite stable Laplace-modal dictionary, \(\Lambda\) contains modal poles, and

\[
\sup_{t\in[0,T]}\|r(t)\|_2
\leq
\varepsilon_{\mathrm{modal}}.
\]

For an oscillatory transient, a real modal block is

\[
A_k=
\begin{bmatrix}
-\rho_k&-\omega_k\\
\omega_k&-\rho_k
\end{bmatrix},
\qquad
\rho_k>0,
\quad
\omega_k\geq0.
\]

### Axiom A5 — band-indexed pole chart

Each modal slot has a declared physical-frequency interval \([\omega_k^-,\omega_k^+]\) with \(\omega_k^-<\omega_k^+\). Unconstrained parameters \((a_k,\nu_k)\in\mathbb R^2\) are decoded by

\[
\rho_k=\rho_{\min}+\operatorname{softplus}(a_k),
\]

\[
\omega_k=\omega_k^-+(\omega_k^+-\omega_k^-)\sigma(\nu_k),
\]

where \(\rho_{\min}>0\). This removes unstable poles and cross-slot frequency permutation from the admissible parameter space.

## 3. Probability and transport

### Axiom A6 — finite second moments

All modal distributions used by the transport theory belong to

\[
\mathcal P_2(\mathcal H),
\]

the probability measures with finite second moment.

### Axiom A7 — regular conditional posterior

The latent state and observations take values in standard Borel spaces. Therefore a regular conditional distribution

\[
q_d(d\theta\mid\mathcal O_d)
\]

exists, up to observation-null sets.

### Axiom A8 — well-posed velocity and score fields

Every ODE velocity used in a theorem is measurable in time, locally Lipschitz in state, and satisfies a linear-growth bound. Every SDE drift and diffusion coefficient satisfies the conditions stated in its theorem for existence and uniqueness. A theorem that needs a density assumes that density is positive and sufficiently differentiable on the relevant active subspace.

### Axiom A9 — task Markov condition

For posterior sufficiency results, the downstream variable \(Y\) satisfies

\[
Y\perp\!\!\!\perp\mathcal O_d\mid\Theta.
\]

This says that the observation affects the task only through the latent physical state. It is not assumed for tasks whose labels directly encode acquisition identity.

## 4. Observable decomposition notation

For domain \(d\):

\[
\mathcal H_c
=
\bigcap_{j\in\mathcal D_s}\mathcal H_j^o
\]

is the common observable subspace,

\[
\mathcal H_{p,d}
=
\mathcal H_d^o\cap\mathcal H_c^\perp
\]

is the observed-private subspace, and

\[
\mathcal H_{u,d}
=
(\mathcal H_d^o)^\perp
\]

is the unobserved subspace. Their orthogonal projectors are \(P_c\), \(P_{p,d}\), and \(P_{u,d}\).

The modal state is decomposed as

\[
\Theta
=
\Theta_c+\Theta_{p,d}+\Theta_{u,d},
\]

where \(\Theta_c=P_c\Theta\), \(\Theta_{p,d}=P_{p,d}\Theta\), and \(\Theta_{u,d}=P_{u,d}\Theta\).

## 5. Unified representation

The ideal representation for acquisition domain \(d\) is the conditional law

\[
\mu_d^U
=
\operatorname{Law}
\left(
T_d\Theta_c,
\Theta_{p,d},
\Theta_{u,d}
\mid\mathcal O_d
\right),
\]

where:

- \(T_d\) maps common observable modes to a source-only canonical distribution;
- the observed-private block is unchanged;
- the unobserved block remains a conditional posterior.

The method does not define a single deterministic vector as the full theoretical representation. A tensor interface may store samples, moments, masks, and canonical coordinates, but these are a finite encoding of \(\mu_d^U\).

## 6. Proof-status convention

Each theory document uses one of three labels:

- **proved under stated assumptions** — a mathematical implication is derived;
- **constructive definition** — an object is explicitly defined but empirical adequacy is unknown;
- **conjecture or empirical hypothesis** — the statement requires experiments or stronger assumptions.

A proof of existence does not prove identifiability, learnability, statistical efficiency, or usefulness on PHM data.

## 7. Dependency graph

```text
Axioms
├── observable decomposition
│   ├── constructive existence
│   ├── observed-private invariance
│   └── shared estimation bound
├── probability-path regularity
│   ├── diffusion–flow marginal equivalence
│   ├── posterior sufficiency
│   └── representation risk bound
├── stable modal chart
│   ├── Laplace modal stability
│   └── sampling-gap shift bound
└── product/transport assumptions
    ├── private-preserving optimal transport
    └── commuting block generators
```

## 8. Non-claims

These axioms do not establish that:

1. the true machine has a globally fixed finite pole set;
2. \(A_d\) is known exactly;
3. the common observable subspace is non-trivial;
4. a neural network can recover the exact posterior;
5. marginal distribution alignment preserves fault semantics;
6. the proposed representation improves any downstream metric.

Those issues are explicit failure boundaries, not hidden assumptions.
