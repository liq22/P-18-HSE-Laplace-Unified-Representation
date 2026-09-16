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
print("Applied industrial-theory witness executed:", out)
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
  external) bash paper_TPAMI/run.sh external "$@" ;;
  sota) bash paper_TPAMI/run_official_baselines.sh "$@" ;;
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
    echo 'Shared implementation: TII industrial goals in paper/; general external/policy goals in paper_TPAMI/.'
    echo 'external requires actual frozen generation exports; it is not a raw converter or classifier run.' ;;
  *) echo 'Unknown mode; use --help.' >&2; exit 2;;
esac
