#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
cd "$ROOT"
MODE=${1:-help}
if (($#)); then shift; fi
case "$MODE" in
  theory)
    bash paper/run.sh theory
    python - <<'NOTEBOOK'
from pathlib import Path
import nbformat
from nbclient import NotebookClient
nb = nbformat.read("paper/theory_main.ipynb", as_version=4)
NotebookClient(nb, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(Path.cwd())}}).execute()
out = Path("outputs/p19/theory/theory_main.executed.ipynb")
out.parent.mkdir(parents=True, exist_ok=True)
nbformat.write(nb, out)
print("Main-theory witness executed:", out)
NOTEBOOK
    ;;
  toy) python -m experiments.p19.toy_routing "$@" ;;
  phm-prepare)
    PHMFACTORY_ROOT=${PHMFACTORY_ROOT:-$ROOT/external/phmfactory}
    test -d "$PHMFACTORY_ROOT/phmfactory" || { echo 'Initialize external/phmfactory and install it first.' >&2; exit 2; }
    (cd "$PHMFACTORY_ROOT" && python -m scripts.prepare_mfpt_baseline "$@") ;;
  phm)
    PHMFACTORY_ROOT=${PHMFACTORY_ROOT:-$ROOT/external/phmfactory}
    test -d "$PHMFACTORY_ROOT/phmfactory" || { echo 'Initialize external/phmfactory and install it first.' >&2; exit 2; }
    (cd "$PHMFACTORY_ROOT" && python "$ROOT/.github/phmfactory_acceptance.py" "$@") ;;
  phm-metrics) python -m experiments.p19.phm_metrics "$@" ;;
  external)
    DATASET=${1:?choose physionet2012, uci_har, ushcn, ett or japanese_vowels}; shift
    case "$DATASET" in physionet2012|uci_har|ushcn|ett|japanese_vowels) ;; *) echo 'Unknown external family' >&2; exit 2;; esac
    echo "External family: $DATASET; requires real frozen HSE/reference exports from DATA_DOWNLOAD_SOP.md."
    bash paper/run.sh native-pilot "$@" ;;
  sota) bash paper/run_official_baselines.sh "$@" ;;
  ablation)
    KIND=${1:?choose parameterization, sampled or native}; shift
    case "$KIND" in
      parameterization|sampled) bash paper/run.sh "$KIND" "$@" ;;
      native) bash paper/run.sh native-pilot "$@" ;;
      *) echo 'Unsupported ablation; do not substitute a different model.' >&2; exit 2;;
    esac ;;
  statistics) python -m experiments.p19.statistics "$@" ;;
  plot) python -m experiments.p19.plot "$@" ;;
  help|--help|-h)
    echo 'Usage: bash experiments/p19/run.sh theory|toy|phm-prepare|phm|phm-metrics|external|sota|ablation|statistics|plot [arguments]'
    echo 'external uses real frozen exports; it is not a raw-data converter. Native ablation retains the existing two-arm pilot.' ;;
  *) echo 'Unknown mode; use --help.' >&2; exit 2;;
esac
