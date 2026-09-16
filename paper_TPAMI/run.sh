#!/usr/bin/env bash
# General-paper entry. Shared implementations are reused, never copied.
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
  statistics) python -m experiments.p19.policy_certificate "$@" ;;
  group-statistics) python -m experiments.p19.statistics "$@" ;;
  plot) python -m experiments.p19.plot_certified_selection "$@" ;;
  group-plot) python -m experiments.p19.plot "$@" ;;
  native-pilot) python -m experiments.learned_conditioning.run_native_pilot "$@" ;;
  external)
    DATASET=${1:?choose a declared external family}; shift
    case "$DATASET" in physionet2012|uci_har|ushcn_monthly|ett|japanese_vowels) ;; *) echo 'Unknown declared external family' >&2; exit 2;; esac
    echo "$DATASET: native generation requires genuine feature/reference exports; this does not convert raw data or run its classification benchmark." >&2
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
    echo 'Usage: paper_TPAMI/run.sh setup|theory|toy|fixed-policy-toy|statistics|plot|group-statistics|group-plot|external|native-pilot|sota|phm|ablation|all-cpu'
    echo 'statistics: bounded independent-group certificate; group-statistics: empirical additive group effects.'
    echo 'external/native-pilot accept genuine frozen exports only; classifier training/raw conversion is not implied.' ;;
  *) echo 'Unknown mode; use --help' >&2; exit 2;;
esac
