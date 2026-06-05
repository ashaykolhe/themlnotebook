# Complete Video Assembly Guide
## Every scene in exact playback order

All scenes verified against HTML. Render each file, then
assemble clips in DaVinci Resolve in the order below.

Render command for any single scene:
  manim -ql <file>.py <ClassName>

Render entire file (all scenes in it):
  manim -ql <file>.py

---

## FULL SEQUENCE — 65 SCENES TOTAL

| # | Scene Class | File | Content | Duration |
|---|-------------|------|---------|----------|
| 1 | Anim01_DotsByOne | part1_hook.py | Black screen → dots form scatter | ~8s |
| 2 | Anim02_UseCaseLabels | part1_hook.py | Bank / Real Estate / Healthcare cards | ~7s |
| 3 | TextA_WhatHowWhy | text_part1_2.py | WHAT / HOW / WHY cards | ~8s |
| 4 | Anim03_LineDraws | part1_hook.py | Orange line draws through scatter | ~6s |
| 5 | TextB_SimpleVsMultiple | text_part1_2.py | Simple vs Multiple table | ~6s |
| 6 | PC01_OverallLinearRegression | pc_part1.py | 8 pros / 8 cons overall LR | ~18s |
| 7 | Anim04_AxesAndDots | part2_whatislinreg.py | Axes + house price scatter | ~8s |
| 8 | Anim05_LineSweeps | part2_whatislinreg.py | Line sweeps angles then settles | ~7s |
| 9 | Anim06_ResidualDashes | part2_whatislinreg.py | Residual dashes appear | ~6s |
| 10 | TextC_ResidualDefinition | text_part1_2.py | Residual = y − ŷ card | ~7s |
| 11 | Anim07_ResidualsShrink | part2_whatislinreg.py | Residuals shrink → best-fit line | ~7s |
| 12 | Anim08_YHatHighlight | part3_equation.py | ŷ highlights in blue | ~5s |
| 13 | Anim09_Beta0Highlight | part3_equation.py | β₀ highlights in orange | ~5s |
| 14 | Anim10_CoeffHighlight | part3_equation.py | β₁ β₂ highlight green | ~5s |
| 15 | TextD_SymbolTable | text_part3.py | Symbol table ŷ β₀ β₁ x | ~10s |
| 16 | Anim11_Beta1Example | part3_equation.py | β₁ = 150 → ₹150/sqft | ~7s |
| 17 | TextE_CoefficientScaling | text_part3.py | ⚠ 0.01 income vs 2.5 rooms warning | ~8s |
| 18 | Anim12_FullEquationAndEpsilon | part3_equation.py | Full equation + ε error term | ~8s |
| 19 | Anim13_CostBowlAppears | part4_ols.py | MSE cost bowl draws | ~6s |
| 20 | Anim14_BallSlidesDown | part4_ols.py | Ball rolls to minimum | ~7s |
| 21 | TextF_WhySquareErrors | text_part4.py | 4 reasons to square errors | ~10s |
| 22 | Anim15_ErrorsCancel | part4_ols.py | Positive/negative errors cancel | ~8s |
| 23 | Anim16_GlobalMinimum | part4_ols.py | Global minimum marker appears | ~6s |
| 24 | TextG_NormalEquationDerivation | text_part4.py | 6-step Normal Eq derivation | ~12s |
| 25 | Anim17_NormalEquation | part4_ols.py | β=(XᵀX)⁻¹Xᵀy + warning card | ~7s |
| 26 | PC02_OLS | pc_part1.py | 4 pros / 4 cons Normal Equation | ~10s |
| 27 | Anim18_HillyLandscape | part5_gradient.py | Hilly landscape + blindfolded figure | ~8s |
| 28 | Anim19_GradientSteps | part5_gradient.py | Ball steps down bowl with labels | ~8s |
| 29 | TextH_GDAlgorithm | text_part5.py | GD 6-step algorithm + formula | ~12s |
| 30 | Anim20_LearningRateCurves | part5_gradient.py | 3 learning rate curves | ~8s |
| 31 | TextI_GDTypesTable | text_part5.py | Batch / SGD / Mini-batch table | ~8s |
| 32 | PC03_GradientDescent | pc_part1.py | 5 pros / 5 cons GD | ~12s |
| 33 | Anim21_LINEMOLetters | part6_linemo.py | L-I-N-E-M-O letters appear | ~6s |
| 34 | Anim22_L_Linearity | part6_linemo.py | L split screen residual plots | ~7s |
| 35 | PC04_Linearity | pc_part2_linemo.py | 3 pros / 3 cons L | ~8s |
| 36 | Anim23_I_Independence | part6_linemo.py | I split screen timelines | ~7s |
| 37 | PC05_Independence | pc_part2_linemo.py | 2 pros / 3 cons I | ~7s |
| 38 | Anim24_N_Normality | part6_linemo.py | N histograms (normal vs skewed) | ~7s |
| 39 | TextJ_NormalityMisconception | text_part6.py | ⚠ RESIDUALS not raw data | ~8s |
| 40 | PC06_Normality | pc_part2_linemo.py | 3 pros / 3 cons N | ~8s |
| 41 | Anim25_E_EqualVariance | part6_linemo.py | E fan shape vs uniform | ~7s |
| 42 | PC07_EqualVariance | pc_part2_linemo.py | 3 pros / 3 cons E | ~8s |
| 43 | Anim26_M_Multicollinearity | part6_linemo.py | M correlation heatmap | ~7s |
| 44 | PC08_Multicollinearity | pc_part2_linemo.py | 3 pros / 4 cons M | ~9s |
| 45 | Anim27_O_Outliers | part6_linemo.py | O outlier pulls regression line | ~8s |
| 46 | PC09_Outliers | pc_part2_linemo.py | 2 pros / 3 cons O | ~7s |
| 47 | Anim28_LINEMOGlow | part6_linemo.py | All 6 letters glow | ~5s |
| 48 | TextK_DetectionMethodsTable | text_part6.py | Detection methods table | ~12s |
| 49 | Anim29_MetricCards | part7_metrics.py | 6 metric formula cards slide in | ~8s |
| 50 | PC10_MSE | pc_part3_metrics.py | 3 pros / 3 cons MSE | ~8s |
| 51 | PC11_RMSE | pc_part3_metrics.py | 3 pros / 2 cons RMSE | ~7s |
| 52 | PC12_MAE | pc_part3_metrics.py | 3 pros / 3 cons MAE | ~8s |
| 53 | PC15_MAPE | pc_part3_metrics.py | 3 pros / 4 cons MAPE | ~8s |
| 54 | Anim30_R2Warning | part7_metrics.py | R² warning: always increases | ~6s |
| 55 | TextL_R2InterpretationTable | text_part7.py | R² benchmark table (0 to 1.0) | ~10s |
| 56 | PC13_R2 | pc_part3_metrics.py | 3 pros / 4 cons R² | ~9s |
| 57 | Anim31_R2VsAdjR2 | part7_metrics.py | R² ticks up vs Adj R² drops | ~8s |
| 58 | PC14_AdjR2 | pc_part3_metrics.py | 3 pros / 3 cons Adj R² | ~8s |
| 59 | TextM_MAEvsRMSE | text_part7.py | MAE vs RMSE decision split | ~10s |
| 60 | Anim32_GoodFitVsOverfit | part8_regularization.py | Good fit vs overfit scatter | ~7s |
| 61 | Anim33_PenaltyTermAppears | part8_regularization.py | MSE → penalty term fades in | ~7s |
| 62 | TextN_RidgeKeyFacts | text_part8.py | Ridge facts + closed-form | ~8s |
| 63 | PC16_Ridge | pc_part4_reg_cv.py | 5 pros / 4 cons Ridge | ~11s |
| 64 | Anim34_RidgeGeometry | part8_regularization.py | Circle constraint + ellipses | ~8s |
| 65 | TextO_LassoKeyFacts | text_part8.py | Lasso facts + coordinate descent | ~8s |
| 66 | PC17_Lasso | pc_part4_reg_cv.py | 4 pros / 5 cons Lasso | ~11s |
| 67 | Anim35_LassoGeometry | part8_regularization.py | Diamond corners + β=0 | ~8s |
| 68 | TextP_L1SparsityExplained | text_part8.py | Geometric + calculus sparsity | ~10s |
| 69 | Anim36_RidgeLassoTable | part8_regularization.py | Ridge vs Lasso comparison table | ~8s |
| 70 | PC18_ElasticNet | pc_part4_reg_cv.py | 4 pros / 4 cons ElasticNet | ~10s |
| 71 | Anim37_BiasVarianceCurves | part9_10_biasvar_cv_outro.py | Bias/Variance/Total curves | ~8s |
| 72 | TextQ_ErrorDecomposition | text_part9.py | Error decomposition table | ~8s |
| 73 | Anim38_SweetSpotPulse | part9_10_biasvar_cv_outro.py | Sweet spot pulses | ~6s |
| 74 | TextR_RegularisationBiasVariance | text_part9.py | Regularisation-BV connection | ~10s |
| 75 | Anim39_CVFolds | part9_10_biasvar_cv_outro.py | 5-fold CV bar | ~7s |
| 76 | PC19_CrossValidation | pc_part4_reg_cv.py | 4 pros / 3 cons CV | ~9s |
| 77 | Anim40_DataLeakage | part9_10_biasvar_cv_outro.py | Wrong approach red leakage | ~7s |
| 78 | TextS_LeakageForms | text_part10_outro.py | 4 leakage forms | ~8s |
| 79 | Anim41_CorrectPipeline | part9_10_biasvar_cv_outro.py | Correct pipeline green | ~6s |
| 80 | TextT_PipelineBenefits | text_part10_outro.py | 4 pipeline benefits | ~8s |
| 81 | PC20_Pipeline | pc_part4_reg_cv.py | 4 pros / 3 cons Pipeline | ~9s |
| 82 | Anim42_PipelineDiagram | part9_10_biasvar_cv_outro.py | [Scaler → Model] diagram | ~6s |
| 83 | Anim43_OutroSummary | part9_10_biasvar_cv_outro.py | All concepts summary screen | ~8s |
| 84 | TextU_ProductionWorkflow | text_part10_outro.py | 9-step production workflow | ~14s |
| 85 | Anim44_EndCard | part9_10_biasvar_cv_outro.py | Subscribe end card | ~6s |

**Estimated total runtime: ~26–28 minutes**
(44 anim scenes + 21 text scenes + 20 PC scenes = 85 clips)

---

## PC SCENE PLACEMENT — WHY EACH GOES WHERE IT DOES

**PC01** after TextB (Simple vs Multiple), before Anim04.
The viewer knows what linear regression is. Now show the trade-offs
before diving into mechanics. Sets expectations for the whole video.

**PC02** after TextG (Normal Eq derivation), before Anim17.
The derivation just showed HOW the Normal Equation works. The pros/cons
immediately answer: "when should you actually use it?"

**PC03** after TextI (GD types table), before Anim21.
Gradient descent and its three variants have been covered.
Pros/cons closes the section before moving to assumptions.

**PC04–PC09** each directly after their assumption's visual anim.
Pattern: See the violation visually (split screen anim) →
understand the consequences (pros/cons). The PC card is the
"so what?" that follows each visual demonstration.

**PC10–PC12 (MSE/RMSE/MAE)** immediately after Anim29 metric cards.
The metric cards show formulas; the PC scenes show when to use each.
These three run consecutively — they're quick (7-8s each).

**PC15 (MAPE)** after PC12, before the R² section.
Groups all four individual metric pros/cons together before
moving on to the R²/AdjR² pair.

**PC13 (R²)** after TextL (R² interpretation table).
The benchmark table already showed what the numbers mean.
The pros/cons answers: "why might R² mislead you?"

**PC14 (Adj R²)** after Anim31 (R² vs Adj R² counter).
The counter just showed R² ticking up with useless features.
The pros/cons explains WHY Adj R² is better for model comparison.

**PC16 (Ridge)** after TextN (Ridge key facts), before Anim34.
Facts first (TextN), then pros/cons, then geometry (Anim34).
This order: know it → evaluate it → see why it works.

**PC17 (Lasso)** after TextO (Lasso key facts), before Anim35.
Same pattern as Ridge.

**PC18 (ElasticNet)** after Anim36 (Ridge vs Lasso table).
The comparison table already placed ElasticNet. Pros/cons
expands on it without needing a dedicated geometry anim.

**PC19 (CV)** after Anim39 (5-fold bar), before Anim40.
CV folds just shown visually. Pros/cons asks: "when is CV
not the right choice?" (time-series, very large datasets).

**PC20 (Pipeline)** after TextT (Pipeline benefits), before Anim42.
Benefits were shown positively (TextT). Pros/cons adds the
honest limitations — harder to debug, prefix naming — so the
viewer gets a balanced view before the diagram (Anim42).

---

## FILES NEEDED (all in same folder)

```
pc_shared.py           ← import this in all PC files
pc_part1.py            ← PC01, PC02, PC03
pc_part2_linemo.py     ← PC04–PC09
pc_part3_metrics.py    ← PC10–PC15
pc_part4_reg_cv.py     ← PC16–PC20
```

Plus all existing anim and text files. `pc_shared.py` and
`shared.py` (for text files) must be in the same folder.

---

## RENDERING ALL PC SCENES AT ONCE

```powershell
# Low quality preview (fast)
manim -ql pc_part1.py
manim -ql pc_part2_linemo.py
manim -ql pc_part3_metrics.py
manim -ql pc_part4_reg_cv.py

# Final 1080p export
manim -qh pc_part1.py
manim -qh pc_part2_linemo.py
manim -qh pc_part3_metrics.py
manim -qh pc_part4_reg_cv.py
```
