# Goal04 — direct simple controls before a learned general claim

**Scope:** actual ordinary/PCA/orthogonal/whitening reference first, then a genuine same-supervision R/M comparison. **Products:** source-only transformation/selection records, restored coefficients, real prediction CSVs and Result updates. The CPU reference does not train a conditional-moment head.

```bash
bash paper_TPAMI/run.sh vowels-reference --archive /absolute/vowels.zip --output-dir outputs/tpami/vowels-reference-02
bash paper_TPAMI/run.sh reference-plot --csv outputs/tpami/vowels-reference-02/affine_summary.csv --output-dir outputs/tpami/vowels-reference-02/figures
# Subsequent native generation, once actual HSE/reference exports exist:
CUDA_VISIBLE_DEVICES=0 bash paper_TPAMI/run.sh native-pilot --train /absolute/train.npz --validation /absolute/validation.npz --test /absolute/test.npz --data-note /absolute/export_note.md --device cuda:0 --seeds 0 1 2 --output-dir outputs/tpami/native
```

**Acceptance:** freeze task, primary metric, checkpoint criterion, HPO grid/trials, normalizer, seeds, q/dtype and update budgets on source data. For classification require direct R/M linear and MLP heads; for generation require matched native target and simple probability heads. Exact T composition is an identity check; PCA/whitening/orthogonal and generic learned bottlenecks are competing controls. Static fusion is required before optional routing.

**Failure:** M tying PCA/MLP does not establish statistical specificity; direct classification matching diffusion removes a necessity claim. Null/negative results are deliverable. Do not retrofit a classification dataset into the existing two-arm generator CLI or label it a completed SOTA run. Four other raw converters and expanded learned arms remain explicit prerequisites.
