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
  setup-neural) "$PYTHON" -m pip install torch ;;
  setup-native)
    : "${LLAPDIFF_ROOT:?set the absolute path to an independently cloned original LLapDiffusion}"
    test -f "$LLAPDIFF_ROOT/pyproject.toml" || { echo 'LLAPDIFF_ROOT lacks pyproject.toml' >&2; exit 2; }
    "$PYTHON" -m pip install -e "$LLAPDIFF_ROOT" --no-deps ;;
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
  conditioner-tests)
    "$PYTHON" -m unittest experiments.learned_conditioning.test_moment_conditioner experiments.learned_conditioning.test_feature_data -v ;;
  conditioner-probe)
    case "$PROFILE" in smoke) N=25;; full) N=600;; *) echo 'profile must be smoke or full' >&2; exit 2;; esac
    "$PYTHON" -m experiments.learned_conditioning.fit_moment_probe --synthetic --steps "$N" --output-dir "$OUT/conditioner-$PROFILE" ;;
  conditioner-fit) shift; "$PYTHON" -m experiments.learned_conditioning.fit_moment_probe "$@" ;;
  native-component) "$PYTHON" -m experiments.learned_conditioning.native_forward --component-smoke --output-dir "$OUT/native-component" ;;
  native-batch) shift; "$PYTHON" -m experiments.learned_conditioning.native_forward --output-dir "$OUT/native-batch" "$@" ;;
  native-schedule) shift; "$PYTHON" paper/export_llapdiff_schedule.py "$@" ;;
  native-pilot) shift; "$PYTHON" -m experiments.learned_conditioning.run_native_pilot "$@" ;;
  native-figures) shift; "$PYTHON" paper/plot_native.py "$@" ;;
  native-acceptance)
    bash paper/run.sh conditioner-tests
    bash paper/run.sh native-component
    bash paper/run.sh native-schedule --output "$OUT/native-component/schedule.csv" --prediction v --weight none --normalization none
    bash paper/run.sh native-figures alignment "$OUT/native-component/native_loss_alignment.csv" "$OUT/native-component/figures" ;;
  all) bash paper/run.sh theory
       bash paper/run.sh oracle "$PROFILE"
       bash paper/run.sh sampled "$PROFILE"
       bash paper/run.sh parameterization "$PROFILE" ;;
  *) echo 'Usage: bash paper/run.sh setup|setup-neural|setup-native|theory|all [smoke|full]' >&2
     echo 'Experiments: oracle|sampled|parameterization|conditioner-probe [smoke|full]' >&2
     echo 'Native: native-acceptance|native-component|native-batch|native-schedule|native-pilot' >&2
     echo 'Figures: figures|parameterization-figures CSV output; native-figures KIND CSV output' >&2; exit 2 ;;
esac
