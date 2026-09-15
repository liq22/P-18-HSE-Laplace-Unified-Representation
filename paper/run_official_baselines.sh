#!/usr/bin/env bash
# Execute the separately installed official package, not a renamed reimplementation.
set -euo pipefail
MODE=${1:-help}
case "$MODE" in help|--help|-h)
  echo 'Usage: run_official_baselines.sh train|forecasting|imputation DATASET_KEY'
  echo 'Requires a separately installed LLAPDIFF_ROOT and the upstream-supported dataset; this is not a five-domain converter.'
  exit 0;; esac
DATASET=${2:?supply an explicit supported upstream dataset key}
: "${LLAPDIFF_ROOT:?set the external pixelhero98/LLapDiffusion checkout}"
cd "$LLAPDIFF_ROOT"
OUT=${BASELINE_OUTPUT:-ldt/results/hse_reference}
mkdir -p "$OUT"
case "$MODE" in
  train) command -v llapdiff-train >/dev/null
    llapdiff-train --dataset-key "$DATASET" --summary-json "$OUT/llapdiff-$DATASET.json" ;;
  forecasting) : "${BASELINE_SOURCE_ROOT:?set the external official baseline checkout directory}"
    command -v llapdiff-baselines >/dev/null
    llapdiff-baselines practical-extrapolation --baseline all --dataset "$DATASET" --baseline-source-root "$BASELINE_SOURCE_ROOT" --output-dir "$OUT/forecasting" ;;
  imputation) : "${BASELINE_SOURCE_ROOT:?set the external official baseline checkout directory}"
    command -v llapdiff-baselines >/dev/null
    llapdiff-baselines csdi-imputation --dataset "$DATASET" --baseline-source-root "$BASELINE_SOURCE_ROOT" --imputation-random-mask-ratio 0.30 --output-dir "$OUT/imputation" ;;
  *) echo 'Unknown official baseline task' >&2; exit 2 ;;
esac
