# transformers — invocation scenarios

Realistic prompts for invoking the transformers implementation (tool) skill
inside the Auto-01-tiny-research workspace. Each scenario shows the kind of
request that should trigger this skill, the artifacts it reads, and the
workspace outputs it must produce.

## Scenario 1: Zero-shot transformer baseline for a claim

> The paper claims our method beats a zero-shot `roberta-large-mnli` baseline at
> macro-F1 on the test split logged in `paper/experiments/run_ledger.md`
> (run `R-014`). The target journal (`paper/refs/target_journal.md`) wants a
> 95% bootstrap CI over macro-F1. Run the pipeline baseline, pin the model
> revision, report the metric with CI, and update claim `C-05` in
> `paper/experiments/evidence_matrix.md`.

This triggers transformers because the request is a pre-trained language-model
inference task — `pipeline("text-classification", model=...)` over a fixed test
split. The skill reads the data ref and claim requirements, pins the model id
and revision hash (recorded in `paper/experiments/reproducibility.md`), runs the
zero-shot inference with a fixed seed, computes macro-F1 with a bootstrap CI per
`paper/experiments/statistics.md`, and writes a run row to
`paper/experiments/run_ledger.md` plus an updated `C-05` row in
`paper/experiments/evidence_matrix.md`. Do NOT use scikit-learn for the model
itself (only for the metric/CI helper if needed); do NOT persist a `.safetensors`
weight blob — record the model id + revision, not the weights. Prefer
pytorch-lightning only if a custom training loop were needed (it is not here).

## Scenario 2: Generation ablation over decoding hyperparameters

> For the ablation table in `paper/assets/tables/ablation_decoding.tex` and
> `paper/experiments/ablation.md`, compare greedy, beam search (k=4), and
> nucleus sampling (top_p=0.9, temp=0.7) on `Qwen/Qwen2.5-1.5B` (pinned
> revision) over the validation prompts from run `R-014`. Report ROUGE-L and
> chrF per the journal protocol, with a multiple-comparison correction noted in
> `paper/experiments/statistics.md`.

This triggers transformers: text-generation decoding-strategy comparison — the
core of `references/generation.md`. The skill loads the model once with
`AutoModelForCausalLM` + `AutoTokenizer`, runs the three decoding configs over
the same prompts and seed, computes ROUGE-L / chrF, applies the
multiple-comparison correction, and emits both the LaTeX table into
`paper/assets/tables/` and a mirrored markdown table in
`paper/experiments/ablation.md`. Each decoding config gets its own run row in
`paper/experiments/run_ledger.md` (same model id + revision, varying only the
decoding kwargs). Honest negative results (a decoding config that underperforms)
go to `paper/experiments/dead_ends.md`. Figures are NOT produced here — hand any
plot request off to scientific-visualization.

## Scenario 3: Fine-tuned transformer baseline via Trainer

> Reviewer 2 (`paper/reviews/response_to_reviewers.md`) wants a
> `distilbert-base-uncased` fine-tuned on our training split as a stronger
> baseline for claim `C-05`. Use the `Trainer` API, 3 epochs, batch size 16,
> lr 2e-5, seed 42, fp16, and report macro-F1 with CI on the same test split as
> the other baselines so the comparison is fair.

This triggers transformers for the `Trainer` / `TrainingArguments` workflow
(`references/training.md`). The skill pins the model id + revision, fixes all
hyperparameters and the seed, tokenizes via `AutoTokenizer` with consistent
truncation/padding, runs `Trainer.train()` with `fp16`, evaluates on the test
split, and records a run row in `paper/experiments/run_ledger.md` with the full
config (lr, batch size, epochs, seed, precision, model id + revision, dataset
ref). Versions and seed go to `paper/experiments/reproducibility.md`; the
reviewer-response entry is drafted into `paper/reviews/response_to_reviewers.md`.
For non-trivial custom training-loop changes, multi-node orchestration, or
complex accelerator sharding, defer to pytorch-lightning instead of the
built-in `Trainer`. Do NOT checkpoint `.bin`/`.safetensors` weights into the
repo — log the Hub-local output dir path in the run ledger, not the binary.
