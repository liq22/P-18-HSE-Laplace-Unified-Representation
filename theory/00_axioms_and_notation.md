# Axioms and notation

## Status

This document fixes the mathematical universe of the project. Every theorem is
conditional on the axioms it explicitly imports. The object under study is not
an arbitrary collection of heterogeneous time series; it is a set of
acquisition operators observing a shared local dynamical process.

## 1. Local modal state and acquisition model

### Axiom A0 — finite-dimensional local modal state

Over one declared analysis window \([0,T]\), the latent physical state belongs
to a finite-dimensional real Hilbert space

\[
\mathcal H=\mathbb R^m
\]

with Euclidean inner product and norm. This is a local approximation. It does
not assert that an entire machine is globally finite-dimensional or globally
linear.

### Axiom A1 — structural acquisition operator

There is a finite source-domain set

\[
\mathcal D_s=\{1,\ldots,D\}.
\]

Each acquisition domain has a structural operator

\[
A_d:\mathcal H\rightarrow\mathcal Y_d,
\]

and a sample \(i\) is observed as

\[
Y_{d,i}=R_{d,i}A_d\Theta_i+\varepsilon_{d,i}.
\]

The fixed operator \(A_d\) represents acquisition capabilities such as sensor
response, channel selection, anti-alias filtering and nominal sampling support.
The sample-dependent operator \(R_{d,i}\) represents realized coverage,
timestamps, valid masks and other instance-level evidence loss.

Structural support is defined from \(A_d\). Instance reliability derived from
\(R_{d,i}\) changes posterior precision or token confidence; it does not silently
relabel the structural subspaces for every sample.

### Axiom A2 — observation-noise metric

For each source domain, the structural noise covariance
\(\Sigma_d\in\mathbb R^{n_d\times n_d}\) is symmetric positive definite. The
noise-weighted structural Gramian is

\[
G_d=A_d^\top\Sigma_d^{-1}A_d.
\]

If a covariance is singular or indefinite, the statistical model must be
redefined on a supported observation space. The implementation does not use a
pseudoinverse as a silent repair.

### Axiom A3 — effective structural observability

A source-only threshold \(\tau_o>0\) defines the ideal hard observable
subspace

\[
\mathcal H_d^o
=
\operatorname{Range}
\left[
\mathbf 1_{[\tau_o,\infty)}(G_d)
\right].
\]

The threshold cannot be selected using a held-out acquisition domain.

For a fixed modal-slot implementation in which \(G_d\) is approximately
diagonal in the declared modal basis, slot \(k\) may instead carry the soft
structural weight

\[
o_{d,k}
=
\sigma\left(
\frac{g_{d,k}-\tau_o}{T_o}
\right),
\qquad
T_o>0,
\]

where \(g_{d,k}\) is the corresponding diagonal or Rayleigh quotient. Soft
weights express threshold uncertainty; they do not change the exact subspace
theorems below.

### Definition A3.1 — instance reliability

For sample \(i\), modal slot \(k\) has an instance reliability

\[
r_{d,i,k}\in[0,1],
\]

computed from timestamp coverage, valid observations, signal quality or
estimated SNR. Structural observability \(o_{d,k}\) asks whether the acquisition
design can observe the slot. Reliability \(r_{d,i,k}\) asks how much evidence
this particular sample provides.

## 2. Laplace modal coordinates

### Axiom A4 — local stable modal approximation

On \([0,T]\), the latent trajectory admits

\[
s(t)=\Phi(t;\Lambda)\Theta+r(t),
\]

where \(\Phi\) is a finite Laplace-modal dictionary and

\[
\sup_{t\in[0,T]}\|r(t)\|_2
\leq
\varepsilon_{\mathrm{modal}}.
\]

A transient oscillatory block is

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

The main paper initially targets event-local damped transients. A bounded
forced component is a baseline used to test model misspecification, not an
automatic expansion to arbitrary nonlinear dynamics.

### Axiom A5 — band-indexed stable pole chart

Every modal slot has a declared angular-frequency interval
\([\omega_k^-,\omega_k^+]\), measured in \(\mathrm{rad\,s^{-1}}\), with
\(\omega_k^-<\omega_k^+\). Unconstrained parameters are decoded by

\[
\rho_k
=
\rho_{\min}
+
\operatorname{softplus}(a_k),
\]

\[
\omega_k
=
\omega_k^-
+
(\omega_k^+-\omega_k^-)\sigma(\nu_k),
\]

where \(\rho_{\min}>0\). Frequencies reported in hertz use
\(f_k=\omega_k/(2\pi)\).

## 3. Probability and transport

### Axiom A6 — finite second moments

All modal distributions used by transport belong to

\[
\mathcal P_2(\mathcal H).
\]

### Axiom A7 — regular conditional distributions

The latent state and observations take values in standard Borel spaces.
Regular conditional distributions therefore exist up to
observation-null sets.

### Axiom A8 — well-posed dynamics

Every ODE velocity is measurable in transport time, locally Lipschitz in state
and of at most linear growth. Every SDE drift and diffusion satisfies the
regularity stated in its theorem. A score-based result assumes a positive,
sufficiently differentiable density on the active subspace.

### Axiom A9 — downstream Markov condition

For posterior-sufficiency results,

\[
Y\perp\!\!\!\perp\mathcal O_d\mid\Theta.
\]

The assumption is inappropriate when the target directly encodes sensor or
dataset identity.

## 4. Four-way source-supported decomposition

Define the common observable subspace

\[
\mathcal H_c
=
\bigcap_{j\in\mathcal D_s}\mathcal H_j^o,
\]

and the source-observable span

\[
\mathcal H_\cup
=
\sum_{j\in\mathcal D_s}\mathcal H_j^o.
\]

For domain \(d\), define

\[
\mathcal H_{p,d}
=
\mathcal H_d^o\cap\mathcal H_c^\perp
\]

as observed-private support,

\[
\mathcal H_{m,d}
=
\mathcal H_\cup\cap(\mathcal H_d^o)^\perp
\]

as recoverable-missing support, and

\[
\mathcal H_0
=
\mathcal H_\cup^\perp
\]

as the global-null support.

The modal state has the unique decomposition

\[
\Theta
=
\Theta_c
+
\Theta_{p,d}
+
\Theta_{m,d}
+
\Theta_0.
\]

The associated projectors are
\(P_c,P_{p,d},P_{m,d},P_0\).

## 5. Unified representation

The data-supported representation for domain \(d\) is

\[
\mu_d^U(\cdot\mid o)
=
\operatorname{Law}
\left(
T_d\Theta_c,
\Theta_{p,d},
\Theta_{m,d}
\mid
\mathcal O_d=o
\right),
\]

together with \(P_0\) as an unsupported-support marker.

The roles are

\[
\begin{aligned}
\Theta_c
&\longrightarrow
T_d\Theta_c
&&\text{population-level canonical flow},\\
\Theta_{p,d}
&\longrightarrow
\Theta_{p,d}
&&\text{identity preservation},\\
\Theta_{m,d}
&\longrightarrow
q_\theta(
\Theta_{m,d}\mid
T_d\Theta_c,\Theta_{p,d},\mathcal O_d)
&&\text{conditional posterior},\\
\Theta_0
&\longrightarrow
\text{unsupported}
&&\text{no data-driven recovery claim}.
\end{aligned}
\]

The source-domain population marginal of \(T_d\Theta_c\) may be canonical.
The conditional law for one observation is not asserted to equal the
population barycenter.

## 6. Proof-status convention

Each theory document uses one of:

- **proved under stated assumptions** — a mathematical implication is derived;
- **constructive definition** — an object is well-defined but its empirical
  adequacy is unknown;
- **empirical hypothesis** — a result requires experiments.

Existence does not imply identifiability, learnability, calibration or
usefulness.

## 7. Dependency graph

```text
Axioms
├── four-way observable decomposition
│   ├── source-supported representation existence
│   ├── observed-private invariance
│   └── GLS shared-estimation bound
├── probability-path regularity
│   ├── flow–diffusion marginal equivalence
│   ├── posterior sufficiency
│   └── paired representation-risk bound
├── stable modal chart
│   ├── modal stability
│   └── sampling-gap shift bound
└── transport assumptions
    ├── product-case private-identity optimality
    └── decoupled generator null model
```

## 8. Non-claims

These axioms do not establish that:

1. arbitrary heterogeneous time series share one latent process;
2. the machine has a globally fixed finite pole set;
3. the structural operators \(A_d\) are known exactly;
4. the common support is non-trivial;
5. global-null modes can be recovered from source data;
6. a neural network can learn the exact missing-mode posterior;
7. marginal canonicalization preserves fault semantics;
8. Diffusion is needed when a Gaussian or mixture posterior is sufficient;
9. Flow is needed when an affine calibration is sufficient;
10. the representation improves a real PHM metric.
