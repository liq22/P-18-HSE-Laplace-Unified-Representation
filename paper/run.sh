#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"
PYTHON=${PYTHON:-python}
MODE=${1:-all}
PROFILE=${2:-smoke}
OUT=${OUTPUT_ROOT:-outputs/paper}
case "$MODE" in
  setup) "$PYTHON" -m pip install -e '.[notebooks,experiments]' ;;
  theory) "$PYTHON" -m unittest discover -s tests -v
          "$PYTHON" theory/run_notebooks.py --timeout 180 ;;
  oracle)
    case "$PROFILE" in smoke) N=64; B=64; SEEDS=(0);; full) N=2048; B=1000; SEEDS=(0 1 2);; *) echo 'profile must be smoke or full' >&2; exit 2;; esac
    "$PYTHON" -m experiments.synthetic_known_pole.run_compression --events-per-seed "$N" --seeds "${SEEDS[@]}" --bootstrap "$B" --output-dir "$OUT/oracle-$PROFILE" ;;
  sampled|ablation) "$PYTHON" -m experiments.sampled_conditioning.run --profile "$PROFILE" --output-dir "$OUT/sampled-$PROFILE"
           "$PYTHON" paper/plot_results.py --csv "$OUT/sampled-$PROFILE/sampled_summary.csv" --output-dir "$OUT/sampled-$PROFILE/figures" ;;
  parameterization)
    case "$PROFILE" in smoke) N=128;; full) N=2048;; *) echo 'profile must be smoke or full' >&2; exit 2;; esac
    "$PYTHON" -m experiments.sampled_conditioning.parameterization_controls --events "$N" --output-dir "$OUT/parameterization-$PROFILE"
    "$PYTHON" -m experiments.sampled_conditioning.parameterization_controls --plot-only "$OUT/parameterization-$PROFILE/parameterization.csv" --output-dir "$OUT/parameterization-$PROFILE/figures" ;;
  figures) "$PYTHON" paper/plot_results.py --csv "${2:?supply CSV}" --output-dir "${3:?supply figure directory}" ;;
  parameterization-figures)
    "$PYTHON" -m experiments.sampled_conditioning.parameterization_controls --plot-only "${2:?supply CSV}" --output-dir "${3:?supply figure directory}" ;;
  all) bash paper/run.sh theory
       bash paper/run.sh oracle "$PROFILE"
       bash paper/run.sh sampled "$PROFILE"
       bash paper/run.sh parameterization "$PROFILE" ;;
  *) echo 'Usage: bash paper/run.sh setup|theory|oracle|sampled|ablation|parameterization|all [smoke|full]' >&2
     echo '       bash paper/run.sh figures|parameterization-figures CSV output-directory' >&2; exit 2 ;;
esac
