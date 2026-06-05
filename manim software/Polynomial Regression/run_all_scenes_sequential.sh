#!/usr/bin/env bash
# ============================================================
# run_all_scenes_sequential.sh
# Renders ALL 66 scenes one after another (sequential).
# Default: low quality (-ql) for fast checking.
# Usage:
#   bash run_all_scenes_sequential.sh          <- low quality
#   bash run_all_scenes_sequential.sh medium   <- medium quality
#   bash run_all_scenes_sequential.sh high     <- high quality (slow)
# ============================================================

QUALITY="-ql"
case "$1" in
  high)   QUALITY="-qh" ;;
  medium) QUALITY="-qm" ;;
  low)    QUALITY="-ql" ;;
esac

FILE="per_scene_classes.py"
echo "[INFO] Rendering all 66 scenes | quality=$QUALITY"
echo "[INFO] Output: media/videos/per_scene_classes/"
echo ""

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
DONE=0
FAILED=()

for SCENE in "${SCENES[@]}"; do
  DONE=$((DONE + 1))
  echo "[$DONE/$TOTAL] Rendering $SCENE ..."
  if manim $QUALITY "$FILE" "$SCENE"; then
    echo "  -> OK"
  else
    echo "  -> FAILED: $SCENE"
    FAILED+=("$SCENE")
  fi
done

echo ""
echo "=============================="
echo "Done: $TOTAL scenes attempted"
if [ ${#FAILED[@]} -eq 0 ]; then
  echo "All scenes rendered successfully."
else
  echo "FAILED scenes (${#FAILED[@]}):"
  for S in "${FAILED[@]}"; do echo "  $S"; done
fi
echo "Output: media/videos/per_scene_classes/"
