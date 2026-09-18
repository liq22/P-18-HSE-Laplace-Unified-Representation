#!/usr/bin/env bash
# General-paper entry; shared implementations are not copied.
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"
MODE=${1:-help}; if (($#)); then shift; fi
OUT=${TPAMI_OUTPUT_ROOT:-outputs/tpami}
case "$MODE" in
  setup) python -m pip install -e '.[notebooks,experiments]' ;;
  theory)
    python - <<'PY'
from pathlib import Path
import nbformat
from nbclient import NotebookClient
root=Path.cwd()
for path in [Path('paper_TPAMI/theory_main.ipynb'),Path('paper_TPAMI/theory/policy_certificate.ipynb')]:
    assert path.with_suffix('.md').is_file(), path
    nb=nbformat.read(path,as_version=4)
    NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
    out=Path('outputs/tpami/theory')/(path.stem+'.executed.ipynb')
    out.parent.mkdir(parents=True,exist_ok=True);nbformat.write(nb,out)
    print('Executed',path)
PY
    ;;
  toy) python -m experiments.p19.certified_selection_demo --output-dir "$OUT/selection" "$@" ;;
  fixed-policy-toy) python -m experiments.p19.toy_routing --output "$OUT/routing_controls.csv" "$@" ;;
  vowels-reference) python -m experiments.p19.japanese_vowels "$@" ;;
  reference-plot) python -m experiments.p19.plot_affine_reference "$@" ;;
  prediction-check) python -m experiments.p19.prediction_agreement "$@" ;;
  statistics) python -m experiments.p19.policy_certificate "$@" ;;
  group-statistics) python -m experiments.p19.statistics "$@" ;;
  plot) python -m experiments.p19.plot_certified_selection "$@" ;;
  group-plot) python -m experiments.p19.plot "$@" ;;
  native-pilot) python -m experiments.learned_conditioning.run_native_pilot "$@" ;;
  external)
    DATASET=${1:?choose a declared external family}; shift
    case "$DATASET" in physionet2012|uci_har|ushcn_monthly|ett|japanese_vowels) ;; *) echo 'Unknown declared external family' >&2; exit 2;; esac
    echo "$DATASET: native generation requires genuine feature/reference exports; use vowels-reference for the implemented raw UCI classification reference." >&2
    python -m experiments.learned_conditioning.run_native_pilot "$@" ;;
  phm) bash experiments/p19/run.sh phm "$@" ;;
  sota) bash paper_TPAMI/run_official_baselines.sh "$@" ;;
  ablation)
    KIND=${1:?choose parameterization, sampled or native}; shift
    case "$KIND" in
      parameterization|sampled) OUTPUT_ROOT="$OUT/ablation" bash paper/run.sh "$KIND" "$@" ;;
      native) python -m experiments.learned_conditioning.run_native_pilot "$@" ;;
      *) echo 'No implemented ablation with this name' >&2; exit 2;;
    esac ;;
  all-cpu)
    bash paper_TPAMI/run.sh theory
    bash paper_TPAMI/run.sh toy
    bash paper_TPAMI/run.sh plot --csv "$OUT/selection/selection_summary.csv" --output-dir "$OUT/figures" ;;
  help|--help|-h)
    echo 'Usage: paper_TPAMI/run.sh setup|theory|toy|fixed-policy-toy|vowels-reference|reference-plot|prediction-check|statistics|plot|group-statistics|group-plot|external|native-pilot|sota|phm|ablation|all-cpu'
    echo 'vowels-reference --archive FILE --output-dir NEW_DIR: official native-length conversion + affine CPU reference.'
    echo 'reference-plot --csv FILE --output-dir DIR: actual reference CSV only.'
    echo 'prediction-check --predictions CSV --output-dir NEW_DIR: paired-label agreement and validation-only static control.'
    echo 'prediction-check --plot-only CSV --output-dir DIR: plots retained summary without refitting.'
    echo 'statistics: bounded independent-group certificate; group-statistics: additive group effects, with --expected-seeds for formal runs.'
    echo 'all-cpu runs existing mathematical studies, not automatic data downloads or learned models.' ;;
  *) echo 'Unknown mode; use --help' >&2; exit 2;;
esac
