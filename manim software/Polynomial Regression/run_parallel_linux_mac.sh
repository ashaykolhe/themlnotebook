#!/usr/bin/env bash
# ============================================================
# run_parallel_linux_mac.sh
# Renders all 66 scenes in parallel.
# Uses GNU parallel if available; falls back to bash & background jobs.
#
# USAGE:
#   bash run_parallel_linux_mac.sh                  # low quality, 4 workers
#   bash run_parallel_linux_mac.sh medium           # medium quality
#   bash run_parallel_linux_mac.sh high             # high quality
#   bash run_parallel_linux_mac.sh low 8            # low quality, 8 workers
#   bash run_parallel_linux_mac.sh medium 6         # medium quality, 6 workers
#
# NOTES:
#   - Workers=4 is safe default for 4-core systems.
#   - Install GNU parallel for best results: sudo apt install parallel
#   - Logs saved to logs/SceneXX.log
# ============================================================

QUALITY="${1:-low}"
WORKERS="${2:-4}"

case "$QUALITY" in
  high)   Q="-qh" ;;
  medium) Q="-qm" ;;
  low)    Q="-ql" ;;
  *)      Q="-ql" ;;
esac

FILE="per_scene_classes.py"
LOG_DIR="logs"
mkdir -p "$LOG_DIR"

SCENES=(
  Scene01Intro
  Scene02WhatIs
  Scene03FiveWs
  Scene04WhyLinearFails
  Scene05OverallProsCons
  Scene06HillyRoad
  Scene07FeatureEngineering
  Scene08RealWorld
  Scene09Equation
  Scene10DegreeShapes
  Scene11WhyLinear
  Scene12NormalEquations
  Scene13NormalEqProsCons
  Scene14CostGd
  Scene15GdProsCons
  Scene16AssumptionsLinemo
  Scene17AssumptionLinearity
  Scene18AssumptionIndependence
  Scene19AssumptionNormality
  Scene20AssumptionHomoscedasticity
  Scene21AssumptionMulticollinearity
  Scene22MulticollinearityProsCons
  Scene23AssumptionOutliers
  Scene24BiasVariance
  Scene25BvChart
  Scene26FittingCards
  Scene27Overfitting
  Scene28Runge
  Scene29OverfittingProsCons
  Scene30Underfitting
  Scene31VisualInspection
  Scene32CrossValidation
  Scene33LearningCurves
  Scene34AicBic
  Scene35AdjustedR2
  Scene36ErrorCurve
  Scene37RegularisationOverview
  Scene38Ridge
  Scene39Lasso
  Scene40Elasticnet
  Scene41RegComparison
  Scene42AlphaEffect
  Scene43FeatureScaling
  Scene44StandardScaler
  Scene45Minmax
  Scene46Centering
  Scene47FeatureExplosion
  Scene48ExplosionProsCons
  Scene49MseRmse
  Scene50MaeR2
  Scene51AdjR2Mape
  Scene52CiPi
  Scene53Pipeline
  Scene54HpPoly
  Scene55HpRidge
  Scene56HpLassoEnet
  Scene57OverallProsCons
  Scene58WhenToUse
  Scene59Alternatives
  Scene60Mistakes
  Scene61IqLinear
  Scene62IqOverfit
  Scene63IqTrainTest
  Scene64IqScale
  Scene65IqLassoZeros
  Scene66Outro
)

TOTAL=${#SCENES[@]}
START_TIME=$(date +%s)

echo ""
echo "============================================"
echo " Polynomial Regression - Parallel Render"
echo "============================================"
echo " Scenes  : $TOTAL"
echo " Workers : $WORKERS"
echo " Quality : $Q"
echo " File    : $FILE"
echo " Logs    : ./$LOG_DIR/"
echo "============================================"
echo ""

# ─── Method 1: GNU parallel (preferred) ──────────────────
if command -v parallel &>/dev/null; then
  echo "[INFO] Using GNU parallel"
  echo ""

  render_scene() {
    local SCENE="$1"
    local Q="$2"
    local FILE="$3"
    local LOG_DIR="$4"
    manim $Q "$FILE" "$SCENE" > "$LOG_DIR/$SCENE.log" 2>&1
    if [ $? -eq 0 ]; then
      echo "  DONE  $SCENE"
    else
      echo "  FAIL  $SCENE  (see $LOG_DIR/$SCENE.log)"
    fi
  }
  export -f render_scene

  printf '%s\n' "${SCENES[@]}" | \
    parallel -j "$WORKERS" render_scene {} "$Q" "$FILE" "$LOG_DIR"

# ─── Method 2: Bash background jobs (fallback) ───────────
else
  echo "[INFO] GNU parallel not found — using bash background jobs"
  echo ""

  FAILED=()
  PIDS=()
  SCENE_OF_PID=()
  RUNNING=0
  IDX=0

  while [ $IDX -lt $TOTAL ] || [ ${#PIDS[@]} -gt 0 ]; do

    # Start new jobs up to worker limit
    while [ $IDX -lt $TOTAL ] && [ $RUNNING -lt $WORKERS ]; do
      SCENE="${SCENES[$IDX]}"
      (
        manim $Q "$FILE" "$SCENE" > "$LOG_DIR/$SCENE.log" 2>&1
        exit $?
      ) &
      PID=$!
      PIDS+=($PID)
      SCENE_OF_PID+=("$SCENE")
      RUNNING=$((RUNNING + 1))
      IDX=$((IDX + 1))
      echo "  START  $SCENE  (pid=$PID)"
    done

    # Poll for finished jobs
    NEW_PIDS=()
    NEW_SCENES=()
    NEW_RUNNING=0
    for i in "${!PIDS[@]}"; do
      PID="${PIDS[$i]}"
      SCENE="${SCENE_OF_PID[$i]}"
      if ! kill -0 "$PID" 2>/dev/null; then
        wait "$PID"
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
          echo "  DONE   $SCENE"
        else
          echo "  FAIL   $SCENE  (see $LOG_DIR/$SCENE.log)"
          FAILED+=("$SCENE")
        fi
        RUNNING=$((RUNNING - 1))
      else
        NEW_PIDS+=($PID)
        NEW_SCENES+=("$SCENE")
        NEW_RUNNING=$((NEW_RUNNING + 1))
      fi
    done
    PIDS=("${NEW_PIDS[@]}")
    SCENE_OF_PID=("${NEW_SCENES[@]}")

    sleep 0.5
  done
fi

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
MINS=$((ELAPSED / 60))
SECS=$((ELAPSED % 60))

echo ""
echo "============================================"
echo " RENDER COMPLETE"
echo "============================================"
echo " Total   : $TOTAL scenes"
printf " Elapsed : %02d:%02d\n" $MINS $SECS
echo " Output  : media/videos/per_scene_classes/"
if [ ${#FAILED[@]} -eq 0 ]; then
  echo " Status  : All scenes OK"
else
  echo " FAILED  : ${#FAILED[@]} scenes"
  for S in "${FAILED[@]}"; do
    echo "   - $S  (log: $LOG_DIR/$S.log)"
  done
fi
echo "============================================"
