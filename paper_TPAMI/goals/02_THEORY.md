# Goal02 — general theoretical argument

**Scope:** target/consumer/budget profile, nested-message loss, hard selection versus fusion, independent finite-policy calibration. **Products:** main.md, notation.md, method.md, theory_main.md/ipynb, theory/policy_certificate.md/ipynb, and cited novelty boundaries.

```bash
bash paper_TPAMI/run.sh theory
python -m unittest discover -s tests -p 'test_policy_certificate.py' -v
bash paper_TPAMI/run.sh toy --seeds 0 1 2 --calibration-groups 64 2048
```

**Acceptance:** statements include iid/boundedness/frozen-family/shift assumptions; finite examples distinguish valid source risk control from target reversal and static fusion from hard selection. Genuine task metrics are not silently clipped to fit the theorem. New proofs are not claimed as first general results over Learn then Test/V-information/MoE.

**Failure:** correct/narrow the offending statement and preserve counterexample. Do not add another theorem family or reinterpret a failed numerical witness as passed. Generic theory plus more datasets alone does not complete a TPAMI contribution.
