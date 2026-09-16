# General time-series representation study — IEEE TPAMI candidate

This workspace receives the general analysis and multi-domain experiments from the industrial TII paper. Read [scope](../PAPER_SCOPE.md), [manuscript](main.md), [experiment design](experiments.md), [observed results](results.md) and [goals](goals/README.md).

The question is **target- and consumer-dependent representation utility under an explicit budget**, followed by source-only comparison of single, static-fusion and dynamic policies. HSE–LLapDiff is one inherited instantiation, not a universal architecture or a newly trained foundation model.

General fixed-policy proofs are in `theory_main.md` and its matching Notebook. The finite-sample specialization is in `theory/policy_certificate.md` and `.ipynb`. They build on V-information, multi-expert deferral and Learn then Test; no generic novelty is inferred from running the witnesses.

```bash
bash paper_TPAMI/run.sh setup
bash paper_TPAMI/run.sh theory
bash paper_TPAMI/run.sh toy
bash paper_TPAMI/run.sh plot --csv paper_TPAMI/assets/selection_summary.csv --output-dir outputs/tpami/figures
```

Five external-domain protocols are specified, but raw conversion, source-trained feature/target checkpoints and multi-domain learned experiments remain pending. The genuine local GPU boundary is Goal 06. PHMFactory is unchanged and optional for the general paper; TII owns industrial method tables. No two-GPU training.
