# Goal02 — method-specific controls

**Scope:** existing projection analysis plus the implemented affine mean head, exact R→T composition and transported ridge regularization. Keep policy/drift bounds secondary sensitivity tools. **Products:** update the existing theory_main.md and same-stem Notebook, Method and contribution boundary; no new theory folder or numbering.

```bash
bash paper_TPAMI/run.sh theory
python -m unittest discover -s tests -p 'test_scientific_input_contract.py' -v
python -m unittest discover -s tests -p 'test_affine_controls.py' -v
# Installed torch is required; exercises the actual shared conditioner:
bash paper/run.sh conditioner-tests
```

**Acceptance:** malformed Gaussian means and common-seed omissions fail; full-q transported ridge predictions coincide; unchanged isotropic whitening is recognized as changed regularization. The actual frozen T composition equals M, and the mean-only affine consumer collapses to an R affine function. General identities do not imply a statistical-message advantage or macro-F1 guarantee.

**Failure:** correct the offending input or narrow the scientific statement. Do not introduce a new theory family, relax a threshold to conceal an error, or infer novelty from a passing witness.
