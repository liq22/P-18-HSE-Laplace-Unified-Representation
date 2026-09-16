# Applied theoretical statement for the industrial conditioner

The general fixed-policy and routing analysis has moved to `../paper_TPAMI/theory_main.md`. TII retains only the statement needed to interpret its actual industrial intervention. The shared detailed derivations are in `../theory/09_conditioning_information_loss.md` and `../theory/10_conditioning_denoising_projection.md`; they are classical analytical support, not newly claimed general inventions.

## Industrial setup

Freeze source-trained HSE, the reference encoder, shared auxiliary trunk and global moment head. Let R be the complete ordinary code and M=T(R) its deterministic statistical-prefix message. Both arms receive the same actual side information. Let X include the noisy reference latent, diffusion time, acquisition condition A and common masks/side inputs. V is one common square-integrable native regression target, with the same weighting/reduction. An unweighted proof is not silently applied to a different batch-normalized objective.

Write $f_R=\mathbb E[V\mid X,R]$ and $f_M=\mathbb E[V\mid X,M]$. For fixed fitted consumers $d_R,d_M$, define their square risks and excess errors conditional on A. Almost surely in a,

$$
\rho_M(a)-\rho_R(a)
=\underbrace{\mathbb E[\|f_R-f_M\|^2\mid A=a]}_{\Gamma(a)\ge0}
+\mathcal E_M(a)-\mathcal E_R(a).
$$

## Derivation

Since M is a function of R, the corresponding conditional sigma-algebras are nested. Expand $V-f_M=(V-f_R)+(f_R-f_M)$; the conditional expectation of the cross term is zero. For each fitted consumer expand $V-d_j=(V-f_j)+(f_j-d_j)$ and eliminate that cross term in the same manner. Subtract the two identities. Including A in X permits conditioning the orthogonality relation on the declared acquisition stratum.

## Meaning and boundaries

M cannot add Bayes information beyond R. It helps only when finite-model error decreases more than the possible information penalty. This is not a guarantee about classification macro-F1, Energy Score, finite-step sampling, or target-domain calibration. The Gaussian auxiliary score concerns conditional moments at its actual global readout; it does not identify an entire non-Gaussian posterior, and finite optimization need not reach its population optimum.

The matching Notebook gives a finite numerical witness, not industrial performance. Real industrial acceptance and learned-conditioner performance remain different evidence levels. All TII empirical method tables use industrial recordings through PHMFactory; generic routing examples are no longer a TII Results table.
