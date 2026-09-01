---
name: transformers
description: 'Hugging Face Transformers implementation skill: reference docs for loading Hub models, pipeline inference, text generation, and Trainer fine-tuning whose results feed paper/experiments/. Implementation-only; prefer pytorch-lightning as primary. Do not use for classical ML, plotting, Bayesian modeling, or running training as an execution engine.'
---

# transformers

## Purpose

Provide implementation guidance and reference material for the Hugging Face
Transformers library v5: loading pre-trained Hub models (`AutoModel`,
`AutoTokenizer`), running pipeline inference, text generation with various
decoding strategies, tokenization, and `Trainer`-based fine-tuning on NLP,
computer vision, audio, and multimodal tasks. In Auto-01-tiny-research this is a
TIER B (tool) implementation-only supporting skill: it ships reference
documentation so the analytic recipes that back the paper's claims can be
written correctly, and it maps every model result onto the
`paper/experiments/` ledger so downstream skills (`08-markdown-draft`,
`09-tex-freeze-formalize`, `13-reviewer-response`) can cite it. It defers to
pytorch-lightning as the primary deep-learning training-engineering skill, and
to scientific-visualization for figure rendering.

## Use When

- A claim in `paper/experiments/evidence_matrix.md` needs a transformer-based
  result: zero-shot / few-shot inference, embeddings for a downstream baseline,
  text classification, NER, question answering, summarization, generation, or
  an LLM-as-judge score.
- The paper compares a fine-tuned transformer baseline against the proposed
  method, and the run must be recorded in `paper/experiments/run_ledger.md` with
  fixed seed, config, and checkpoint provenance.
- A reviewer (`paper/reviews/response_to_reviewers.md`) asks for an additional
  transformer baseline, an ablation over decoding hyperparameters, or a
  different checkpoint, reported under `paper/experiments/ablation.md`.
- You need to cite a specific Hub model card / checkpoint in
  `paper/refs/references.bib` and document its license / gating in
  `paper/experiments/reproducibility.md`.

Do not use this skill for classical tabular ML (defer to scikit-learn),
Bayesian inference (pymc), figure plotting (scientific-visualization),
distributed GPU training engineering at scale (pytorch-lightning owns the
training-loop / accelerator concerns), or non-Python ML stacks. It is also not
an execution harness: in this repo it documents and recipes analyses; it does
not run production training jobs or ship executable training/inference scripts.

## Required Inputs

- The claim ID(s) this analysis must support, from
  `paper/experiments/evidence_matrix.md`, and the target metric / protocol
  mandated by `paper/refs/target_journal.md` and
  `paper/experiments/statistics.md`.
- A dataset path already logged in `paper/experiments/run_ledger.md`, or a Hub
  dataset id; do not invent or fabricate data.
- The exact Hub model id(s) and revision / commit hash to use (pinned for
  reproducibility in `paper/experiments/reproducibility.md`).
- A target output path for any persisted result under `paper/experiments/` or
  `paper/assets/tables/`.
- transformers 5.x with PyTorch 2.4+ on Python 3.10+; optional `timm`/`pillow`
  (vision) and `librosa`/`soundfile` (audio). The user is responsible for
  installing these; this skill does not pin or ship a runtime.
- A Hugging Face access token for any gated or private model. The user must
  provide it via `hf auth login` or the `HF_TOKEN` environment variable; never
  hardcode or store tokens in notebooks, repos, scripts, or shell profiles. If
  a credential is needed and not supplied, stop (see Stop With) rather than
  substituting an ungated substitute.

## Workflow

1. Read the target claim and its required metric from
   `paper/experiments/evidence_matrix.md` and `paper/refs/target_journal.md`.
   Do not pick a metric the journal or the claim does not sanction.
2. Load only data referenced by `paper/experiments/run_ledger.md`; if absent or
   unlogged, stop rather than substituting.
3. Pin the model id and revision; record the commit hash and license in
   `paper/experiments/reproducibility.md`. For gated or custom-architecture
   models, confirm the user has accepted the license on the Hub before loading
   with `trust_remote_code=True`, and only when the model card requires custom
   code you have reviewed.
4. Choose the API surface from the references: `pipeline()` for quick
   inference (`references/pipelines.md`); explicit
   `AutoModel`/`AutoTokenizer` for custom control (`references/models.md`);
   decoding strategies for generation (`references/generation.md`);
   tokenization patterns for preprocessing (`references/tokenizers.md`).
5. For fine-tuning, follow the `Trainer` / `TrainingArguments` workflow in
   `references/training.md`; fix `seed`, `data_seed`, batch size, learning
   rate, epochs, and precision, and log every candidate configuration in
   `paper/experiments/ablation.md`. Prefer pytorch-lightning for non-trivial
   custom training loops / multi-accelerator orchestration.
6. Evaluate with the journal-mandated metrics; for generation use the
   task-appropriate metric (BLEU/ROUGE/chrF as the journal requires) and report
   a CI per `paper/experiments/statistics.md`.
7. Persist: append a run row to `paper/experiments/run_ledger.md` (model id +
   revision, dataset ref, hyperparameters, seed, metric + CI, claim ID); update
   `paper/experiments/evidence_matrix.md` status
   (`supported` / `partial` / `refuted`); record versions and seed in
   `paper/experiments/reproducibility.md`.
8. Surface non-trivial decisions in `paper/logs/decision_log.md`; record
   negative results honestly in `paper/experiments/dead_ends.md` instead of
   suppressing them.

## Output Contract

- A run row in `paper/experiments/run_ledger.md` with: model id + revision
  hash, dataset ref, hyperparameter config, seed, point metric + CI, and the
  claim ID(s) it supports.
- Updated status in `paper/experiments/evidence_matrix.md` for every claim the
  run addresses (`supported` / `partial` / `refuted` / `unsupported`).
- An ablation table under `paper/assets/tables/` when more than one checkpoint
  or decoding configuration was compared; mirror it into
  `paper/experiments/ablation.md`.
- A reproducibility note in `paper/experiments/reproducibility.md` covering the
  transformers / torch / tokenizers library versions, model id + revision,
  seed, and exact data ref.
- A citation entry for the model card / checkpoint in
  `paper/refs/references.bib` when the model is named in the draft.
- Optional decision / dead-end entries in `paper/logs/decision_log.md` and
  `paper/experiments/dead_ends.md`.
- No executable training/inference scripts and no model weight blobs
  (`.bin` / `.safetensors` / `.pt` / `.ckpt`) shipped into the repo; code stays
  as documented recipes in the references.

## Validation

- `python .agent/scripts/validate_agent_skills.py --skills-dir .agent/skills --strict --only transformers`
- `python src/S03_Scripts/validate_project.py`
- Confirm every run referenced by `paper/experiments/evidence_matrix.md` has a
  matching row in `paper/experiments/run_ledger.md` (no orphan claims).
- Confirm no metric is reported for a claim the matrix marks `unsupported`,
  `missing_evidence`, or `refuted`.
- Confirm the model id and revision hash are recorded in
  `paper/experiments/reproducibility.md` for every transformer run.
- Confirm no `HF_TOKEN` value (or any other credential) appears in any file
  under `.agent/skills/transformers/` or `paper/` — only the env-var name.
- Confirm no `.bin` / `.safetensors` / `.pt` / `.ckpt` / `.pth` weight file was
  copied into the repo.

## Boundaries

- Do not run distributed / multi-GPU training engineering here; defer the
  training-loop and accelerator orchestration to pytorch-lightning. This skill
  covers the transformers API surface (model loading, pipelines, generation,
  the `Trainer` config), not custom training infrastructure.
- Do not fabricate metrics, datasets, prompts, or benchmark numbers; if a
  result is missing, mark the claim `missing_evidence` and stop.
- Do not copy the upstream `scripts/` executable training/inference code into
  this repo; this skill ships `references/` documentation only.
- Do not persist model weight blobs (`.bin`, `.safetensors`, `.pt`, `.ckpt`,
  `.pth`) or tokenizer caches into the paper repo; record recipes and metrics,
  not weights.
- Do not write outputs anywhere except `paper/experiments/`,
  `paper/assets/tables/`, `paper/refs/references.bib`, and the designated
  logs; never into `paper/tex/`, `paper/submission/`, or `paper/checklists/`
  (those are owned by other stages).
- Do not paste `HF_TOKEN` or any access token into notebooks, scripts, shell
  profiles, or committed configs; use `hf auth login` or pass it via the
  environment, never hardcoded.
- Use the narrowest token scope that works (`read` for gated downloads, `write`
  only for Hub uploads the user explicitly requested).

## Stop With

- The dataset needed to compute a claim is not present in
  `paper/experiments/run_ledger.md` and the user has not supplied it.
- A gated or private model is required but the user has not provided an
  `HF_TOKEN` / accepted the model license on the Hub; do not silently
  substitute an ungated model.
- The required metric, CV protocol, or generation-evaluation metric is
  unspecified by `paper/refs/target_journal.md` /
  `paper/experiments/statistics.md` and the user has not disambiguated.
- transformers, torch, or a required extra (timm, librosa) is unavailable and
  the user cannot install it; do not silently fall back to a different library.
- The result would contradict the claim's required direction and the user has
  not authorized reporting a `refuted` finding — surface it in
  `paper/logs/decision_log.md` and wait.
- The model card forbids the intended use, or the license is incompatible with
  the target journal's redistribution terms noted in
  `paper/refs/target_journal.md`.

## References

- Pipelines & quick inference: `.agent/skills/transformers/references/pipelines.md`
- Model loading & management: `.agent/skills/transformers/references/models.md`
- Text generation strategies: `.agent/skills/transformers/references/generation.md`
- Training & fine-tuning (Trainer API): `.agent/skills/transformers/references/training.md`
- Tokenization & preprocessing: `.agent/skills/transformers/references/tokenizers.md`
- Invocation scenarios: `.agent/skills/transformers/examples/prompts.md`
- Workspace artifacts: `paper/experiments/evidence_matrix.md`,
  `paper/experiments/run_ledger.md`, `paper/experiments/statistics.md`,
  `paper/experiments/ablation.md`, `paper/experiments/reproducibility.md`,
  `paper/experiments/dead_ends.md`, `paper/experiments/insights.md`,
  `paper/assets/tables/`, `paper/refs/references.bib`,
  `paper/refs/target_journal.md`, `paper/logs/decision_log.md`
- Provenance: Ported (adapted) from K-Dense-AI/scientific-agent-skills v2.53.0
  (MIT); see NOTICE.md and
  `.agent/references/scientific_agent_skills_source.md`.
- Upstream docs: https://huggingface.co/docs/transformers/index ,
  https://github.com/huggingface/transformers/blob/main/MIGRATION_GUIDE_V5.md
