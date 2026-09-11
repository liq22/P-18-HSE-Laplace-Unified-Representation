#!/usr/bin/env bash
# Use the separately installed official LLapDiff package, not a reimplementation.
set -euo pipefail
: "${LLAPDIFF_ROOT:?set to the external pixelhero98/LLapDiffusion checkout}"
cd "$LLAPDIFF_ROOT"
MODE=${1:-train}
DATASET=${2:-crypto}
OUT=${BASELINE_OUTPUT:-ldt/results/hse_reference}
mkdir -p "$OUT"
case "$MODE" in
  train) command -v llapdiff-train >/dev/null
         llapdiff-train --dataset-key "$DATASET" --summary-json "$OUT/llapdiff-$DATASET.json" ;;
  forecasting) : "${BASELINE_SOURCE_ROOT:?set the external upstream baseline checkout directory}"
         command -v llapdiff-baselines >/dev/null
         llapdiff-baselines practical-extrapolation --baseline all --dataset "$DATASET" --baseline-source-root "$BASELINE_SOURCE_ROOT" --output-dir "$OUT/forecasting" ;;
  imputation) : "${BASELINE_SOURCE_ROOT:?set the external upstream baseline checkout directory}"
         command -v llapdiff-baselines >/dev/null
         llapdiff-baselines csdi-imputation --dataset "$DATASET" --baseline-source-root "$BASELINE_SOURCE_ROOT" --imputation-random-mask-ratio 0.30 --output-dir "$OUT/imputation" ;;
  *) echo 'Usage: run_official_baselines.sh train|forecasting|imputation dataset-key' >&2; exit 2 ;;
esac
