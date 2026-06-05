@echo off
REM ============================================================
REM run_all_scenes_sequential.bat
REM Renders ALL 66 scenes one after another (sequential).
REM Uses medium quality (-ql) for fast checking.
REM Change -ql to -qh for high quality final render.
REM ============================================================
REM USAGE:
REM   run_all_scenes_sequential.bat
REM   run_all_scenes_sequential.bat high     <- high quality
REM ============================================================

SET QUALITY=-ql
IF "%1"=="high" SET QUALITY=-qh
IF "%1"=="medium" SET QUALITY=-qm
IF "%1"=="low" SET QUALITY=-ql

SET FILE=per_scene_classes.py
echo [INFO] Rendering all 66 scenes with quality: %QUALITY%
echo [INFO] Output: media\videos\per_scene_classes\
echo.

manim %QUALITY% %FILE% Scene01Intro
manim %QUALITY% %FILE% Scene02WhatIs
manim %QUALITY% %FILE% Scene03FiveWs
manim %QUALITY% %FILE% Scene04WhyLinearFails
manim %QUALITY% %FILE% Scene05OverallProsCons
manim %QUALITY% %FILE% Scene06HillyRoad
manim %QUALITY% %FILE% Scene07FeatureEngineering
manim %QUALITY% %FILE% Scene08RealWorld
manim %QUALITY% %FILE% Scene09Equation
manim %QUALITY% %FILE% Scene10DegreeShapes
manim %QUALITY% %FILE% Scene11WhyLinear
manim %QUALITY% %FILE% Scene12NormalEquations
manim %QUALITY% %FILE% Scene13NormalEqProsCons
manim %QUALITY% %FILE% Scene14CostGd
manim %QUALITY% %FILE% Scene15GdProsCons
manim %QUALITY% %FILE% Scene16AssumptionsLinemo
manim %QUALITY% %FILE% Scene17AssumptionLinearity
manim %QUALITY% %FILE% Scene18AssumptionIndependence
manim %QUALITY% %FILE% Scene19AssumptionNormality
manim %QUALITY% %FILE% Scene20AssumptionHomoscedasticity
manim %QUALITY% %FILE% Scene21AssumptionMulticollinearity
manim %QUALITY% %FILE% Scene22MulticollinearityProsCons
manim %QUALITY% %FILE% Scene23AssumptionOutliers
manim %QUALITY% %FILE% Scene24BiasVariance
manim %QUALITY% %FILE% Scene25BvChart
manim %QUALITY% %FILE% Scene26FittingCards
manim %QUALITY% %FILE% Scene27Overfitting
manim %QUALITY% %FILE% Scene28Runge
manim %QUALITY% %FILE% Scene29OverfittingProsCons
manim %QUALITY% %FILE% Scene30Underfitting
manim %QUALITY% %FILE% Scene31VisualInspection
manim %QUALITY% %FILE% Scene32CrossValidation
manim %QUALITY% %FILE% Scene33LearningCurves
manim %QUALITY% %FILE% Scene34AicBic
manim %QUALITY% %FILE% Scene35AdjustedR2
manim %QUALITY% %FILE% Scene36ErrorCurve
manim %QUALITY% %FILE% Scene37RegularisationOverview
manim %QUALITY% %FILE% Scene38Ridge
manim %QUALITY% %FILE% Scene39Lasso
manim %QUALITY% %FILE% Scene40Elasticnet
manim %QUALITY% %FILE% Scene41RegComparison
manim %QUALITY% %FILE% Scene42AlphaEffect
manim %QUALITY% %FILE% Scene43FeatureScaling
manim %QUALITY% %FILE% Scene44StandardScaler
manim %QUALITY% %FILE% Scene45Minmax
manim %QUALITY% %FILE% Scene46Centering
manim %QUALITY% %FILE% Scene47FeatureExplosion
manim %QUALITY% %FILE% Scene48ExplosionProsCons
manim %QUALITY% %FILE% Scene49MseRmse
manim %QUALITY% %FILE% Scene50MaeR2
manim %QUALITY% %FILE% Scene51AdjR2Mape
manim %QUALITY% %FILE% Scene52CiPi
manim %QUALITY% %FILE% Scene53Pipeline
manim %QUALITY% %FILE% Scene54HpPoly
manim %QUALITY% %FILE% Scene55HpRidge
manim %QUALITY% %FILE% Scene56HpLassoEnet
manim %QUALITY% %FILE% Scene57OverallProsCons
manim %QUALITY% %FILE% Scene58WhenToUse
manim %QUALITY% %FILE% Scene59Alternatives
manim %QUALITY% %FILE% Scene60Mistakes
manim %QUALITY% %FILE% Scene61IqLinear
manim %QUALITY% %FILE% Scene62IqOverfit
manim %QUALITY% %FILE% Scene63IqTrainTest
manim %QUALITY% %FILE% Scene64IqScale
manim %QUALITY% %FILE% Scene65IqLassoZeros
manim %QUALITY% %FILE% Scene66Outro

echo.
echo [DONE] All 66 scenes rendered.
echo Output folder: media\videos\per_scene_classes\
