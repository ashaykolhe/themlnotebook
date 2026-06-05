# Run Commands — Polynomial Regression Video

Place all files in the **same folder** before running anything:

```
polynomial_regression_video.py   ← main video (66 scenes, one class)
per_scene_classes.py             ← 66 individual wrapper classes
run_all_scenes_sequential.bat    ← Windows sequential batch
run_all_scenes_sequential.sh     ← Linux / Mac sequential batch
run_parallel_windows.ps1         ← Windows parallel (PowerShell)
run_parallel_linux_mac.sh        ← Linux / Mac parallel
```

---

## Setup (one time)

```bash
pip install manim
```

> **Windows only:** also install [MiKTeX](https://miktex.org) for LaTeX / MathTex rendering.

---

## Quality flags

| Flag | Resolution | FPS | Use for |
|------|-----------|-----|---------|
| `-ql` | 854 × 480 | 15 | Fast checking (default) |
| `-qm` | 1280 × 720 | 30 | Review |
| `-qh` | 1920 × 1080 | 60 | Final production |
| `-qk` | 3840 × 2160 | 60 | 4K, very slow |

Add `-p` to any command to auto-open the video after rendering.

---

## 1. Full video — one command, one output file

```bash
# Low quality (fast check)
manim -ql polynomial_regression_video.py PolynomialRegressionVideo

# Medium quality
manim -qm polynomial_regression_video.py PolynomialRegressionVideo

# High quality (final upload)
manim -qh polynomial_regression_video.py PolynomialRegressionVideo

# High quality + auto-preview
manim -pqh polynomial_regression_video.py PolynomialRegressionVideo
```

Output: `media/videos/polynomial_regression_video/[quality]/PolynomialRegressionVideo.mp4`

---

## 2. Individual scenes — one at a time

```bash
manim -ql per_scene_classes.py Scene01Intro
manim -ql per_scene_classes.py Scene02WhatIs
manim -ql per_scene_classes.py Scene03FiveWs
manim -ql per_scene_classes.py Scene04WhyLinearFails
manim -ql per_scene_classes.py Scene05OverallProsCons
manim -ql per_scene_classes.py Scene06HillyRoad
manim -ql per_scene_classes.py Scene07FeatureEngineering
manim -ql per_scene_classes.py Scene08RealWorld
manim -ql per_scene_classes.py Scene09Equation
manim -ql per_scene_classes.py Scene10DegreeShapes
manim -ql per_scene_classes.py Scene11WhyLinear
manim -ql per_scene_classes.py Scene12NormalEquations
manim -ql per_scene_classes.py Scene13NormalEqProsCons
manim -ql per_scene_classes.py Scene14CostGd
manim -ql per_scene_classes.py Scene15GdProsCons
manim -ql per_scene_classes.py Scene16AssumptionsLinemo
manim -ql per_scene_classes.py Scene17AssumptionLinearity
manim -ql per_scene_classes.py Scene18AssumptionIndependence
manim -ql per_scene_classes.py Scene19AssumptionNormality
manim -ql per_scene_classes.py Scene20AssumptionHomoscedasticity
manim -ql per_scene_classes.py Scene21AssumptionMulticollinearity
manim -ql per_scene_classes.py Scene22MulticollinearityProsCons
manim -ql per_scene_classes.py Scene23AssumptionOutliers
manim -ql per_scene_classes.py Scene24BiasVariance
manim -ql per_scene_classes.py Scene25BvChart
manim -ql per_scene_classes.py Scene26FittingCards
manim -ql per_scene_classes.py Scene27Overfitting
manim -ql per_scene_classes.py Scene28Runge
manim -ql per_scene_classes.py Scene29OverfittingProsCons
manim -ql per_scene_classes.py Scene30Underfitting
manim -ql per_scene_classes.py Scene31VisualInspection
manim -ql per_scene_classes.py Scene32CrossValidation
manim -ql per_scene_classes.py Scene33LearningCurves
manim -ql per_scene_classes.py Scene34AicBic
manim -ql per_scene_classes.py Scene35AdjustedR2
manim -ql per_scene_classes.py Scene36ErrorCurve
manim -ql per_scene_classes.py Scene37RegularisationOverview
manim -ql per_scene_classes.py Scene38Ridge
manim -ql per_scene_classes.py Scene39Lasso
manim -ql per_scene_classes.py Scene40Elasticnet
manim -ql per_scene_classes.py Scene41RegComparison
manim -ql per_scene_classes.py Scene42AlphaEffect
manim -ql per_scene_classes.py Scene43FeatureScaling
manim -ql per_scene_classes.py Scene44StandardScaler
manim -ql per_scene_classes.py Scene45Minmax
manim -ql per_scene_classes.py Scene46Centering
manim -ql per_scene_classes.py Scene47FeatureExplosion
manim -ql per_scene_classes.py Scene48ExplosionProsCons
manim -ql per_scene_classes.py Scene49MseRmse
manim -ql per_scene_classes.py Scene50MaeR2
manim -ql per_scene_classes.py Scene51AdjR2Mape
manim -ql per_scene_classes.py Scene52CiPi
manim -ql per_scene_classes.py Scene53Pipeline
manim -ql per_scene_classes.py Scene54HpPoly
manim -ql per_scene_classes.py Scene55HpRidge
manim -ql per_scene_classes.py Scene56HpLassoEnet
manim -ql per_scene_classes.py Scene57OverallProsCons
manim -ql per_scene_classes.py Scene58WhenToUse
manim -ql per_scene_classes.py Scene59Alternatives
manim -ql per_scene_classes.py Scene60Mistakes
manim -ql per_scene_classes.py Scene61IqLinear
manim -ql per_scene_classes.py Scene62IqOverfit
manim -ql per_scene_classes.py Scene63IqTrainTest
manim -ql per_scene_classes.py Scene64IqScale
manim -ql per_scene_classes.py Scene65IqLassoZeros
manim -ql per_scene_classes.py Scene66Outro
```

Output: `media/videos/per_scene_classes/[quality]/SceneXX.mp4`

---

## 3. All 66 scenes sequential (batch scripts)

### Windows — cmd.exe

```bat
run_all_scenes_sequential.bat            rem  low quality (default)
run_all_scenes_sequential.bat medium     rem  medium quality
run_all_scenes_sequential.bat high       rem  high quality
```

### Linux / Mac — bash

```bash
bash run_all_scenes_sequential.sh           # low quality (default)
bash run_all_scenes_sequential.sh medium    # medium quality
bash run_all_scenes_sequential.sh high      # high quality
```

---

## 4. Parallel render — fastest for bulk checking

### Windows — PowerShell

If the execution policy blocks the script, run this first (one time):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then render:

```powershell
.\run_parallel_windows.ps1                           # low quality, 4 workers
.\run_parallel_windows.ps1 -Quality qm               # medium quality, 4 workers
.\run_parallel_windows.ps1 -Quality ql -Workers 6    # low quality, 6 workers
.\run_parallel_windows.ps1 -Quality qh -Workers 2    # high quality, 2 workers
```

### Linux / Mac — bash

Install GNU parallel first for best results:

```bash
sudo apt install parallel    # Ubuntu / Debian
brew install parallel        # Mac
```

Then render:

```bash
bash run_parallel_linux_mac.sh                  # low quality, 4 workers
bash run_parallel_linux_mac.sh medium 4         # medium quality, 4 workers
bash run_parallel_linux_mac.sh low 8            # low quality, 8 workers
bash run_parallel_linux_mac.sh high 2           # high quality, 2 workers
```

---

## 5. Render a specific range of scenes

Useful after fixing a bug — re-render only the affected scenes.

### Windows — cmd.exe

```bat
for %S in (Scene38Ridge Scene39Lasso Scene40Elasticnet Scene41RegComparison Scene42AlphaEffect) do manim -ql per_scene_classes.py %S
```

### Linux / Mac — bash

```bash
for S in Scene38Ridge Scene39Lasso Scene40Elasticnet Scene41RegComparison Scene42AlphaEffect; do
    manim -ql per_scene_classes.py $S
done
```

---

## 6. Save last frame only — fastest visual check

Saves a PNG image of the final frame, no video encoding. Much faster than a full render.

```bash
manim --save_last_frame per_scene_classes.py Scene09Equation
manim --save_last_frame per_scene_classes.py Scene57OverallProsCons
```

Output: `media/images/per_scene_classes/SceneXX_ManimCE_v0.jpg`

---

## 7. Output file locations

```
Full video:
  media/videos/polynomial_regression_video/480p15/PolynomialRegressionVideo.mp4   ← -ql
  media/videos/polynomial_regression_video/720p30/PolynomialRegressionVideo.mp4   ← -qm
  media/videos/polynomial_regression_video/1080p60/PolynomialRegressionVideo.mp4  ← -qh

Individual scenes:
  media/videos/per_scene_classes/480p15/Scene01Intro.mp4
  media/videos/per_scene_classes/720p30/Scene09Equation.mp4
  (etc.)

Parallel render logs:
  logs/Scene01Intro.log
  logs/Scene09Equation.log
  (etc.)
```

---

## 8. Recommended workflow

**Step 1 — Quick check all scenes in parallel (low quality):**

```bash
# Windows
.\run_parallel_windows.ps1 -Quality ql -Workers 4

# Linux / Mac
bash run_parallel_linux_mac.sh low 4
```

**Step 2 — Fix any broken scenes, re-render only those:**

```bash
manim -ql per_scene_classes.py Scene09Equation
manim -ql per_scene_classes.py Scene25BvChart
```

**Step 3 — Render the full final video at high quality:**

```bash
manim -qh polynomial_regression_video.py PolynomialRegressionVideo
```

**Step 4 — Upload the single MP4 to YouTube.**
