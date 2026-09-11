# Paper workspace

Start with [GOAL.md](GOAL.md). The active target is one valid native M/B1-aux comparison, not another theory-only round or the full benchmark. The current PR targets `dev`; no automatic merge is authorized.

`main.md` contains the abstract and English Introduction; `introduction_outline.md` explains each paragraph and source. `method.md` defines the shared gradient and freezing paths. `experiments.md` separates acceptance, genuine-export pilot and later ablations. Proofs live only under `../theory/`, each with its same-stem Notebook.

## Install explicitly

```bash
bash paper/run.sh setup
bash paper/run.sh setup-neural
export LLAPDIFF_ROOT=/absolute/path/to/LLapDiffusion
bash paper/run.sh setup-native
```

Use the PyTorch installation appropriate for the intended CPU/CUDA machine. The native source checkout is separate and remains unchanged. Its tested component interface is revision `0631e65`; `setup-native` installs that user-selected checkout without silently switching revisions or pulling all external dataset dependencies.

## Execute separately

```bash
bash paper/run.sh theory
bash paper/run.sh native-acceptance
bash paper/run.sh conditioner-probe full
```

`native-acceptance` runs the existing original-model loss, gradient and field-consumption checks on **explicit synthetic fixture inputs**, exports the native uniform-time schedule, and redraws the alignment CSV. It does not run HSE/reference extraction or prove method advantage. `conditioner-probe` is an explicitly synthetic shared-readout experiment, not a replacement for real exports.

The original analytic tasks remain available:

```bash
bash paper/run.sh oracle full
bash paper/run.sh sampled full
bash paper/run.sh parameterization full
bash paper/run.sh all smoke
```

`all` runs only these analytic tasks plus theory. It never silently starts the real pilot, full five-arm study or external SOTA.

## Genuine frozen exports

Use the schema and original-record provenance requirements in `GOAL.md`. No sample data are substituted when an export is missing.

```bash
bash paper/run.sh native-batch --batch /absolute/train.npz --data-note /absolute/export_note.md
bash paper/run.sh native-pilot --train /absolute/train.npz \
  --validation /absolute/validation.npz --test /absolute/test.npz \
  --data-note /absolute/export_note.md --device cuda:0 --seeds 0 1 2 \
  --anchor-steps 150 --diffusion-steps 200 --draws 8 --sampler-steps 16 \
  --output-dir outputs/native_pilot_01
```

A successful run on exported features is not on-the-fly HSE/VAE execution. Source validation and unseen acquisition tests remain separate. B1-aux and M share the fitted ordinary trunk; the former sends its complete code.

## Redraw without training

```bash
bash paper/run.sh native-figures scores outputs/paper/conditioner-full/score_parts.csv outputs/readout_figures
bash paper/run.sh native-figures alignment outputs/paper/native-component/native_loss_alignment.csv outputs/alignment_figures
bash paper/run.sh native-figures comparison outputs/native_pilot_01/event_scores.csv outputs/pilot_figures
```

Figures use Matplotlib and editable SVG/PDF text, plus PNG previews. Comparison figures require exact paired rows, average within original groups and do not discard missing methods or seeds. Intervals condition on the executed training seeds. A one-group result has no between-group confidence interval.

For upstream official baseline datasets use the separate `run_official_baselines.sh` and installed dependencies. Its syntax check is not a trained baseline. Full benchmark expansion is deferred until the small matched native experiment is interpretable.

## Decoupling

No paper module imports PHMFactory internals or requires its submodule. Any framework export supplies arrays, physical metadata and original recording-level splits. No repository-integrity or figure-governance framework is introduced. The supplied nature-figure reference informs scientific layout and vector exports, not a claim of Nature submission certification.
