# MASTER SEQUENCE GUIDE
## Polynomial Regression — Complete YouTube Video
## Single Manim Class: PolynomialRegressionVideo

---

## How to Render

Run the single Python file:

```
manim -pqh polynomial_regression_video.py PolynomialRegressionVideo
```

Flags:
- `-p`   : preview after rendering
- `-q h` : high quality (1920x1080, 60fps)
- `-q m` : medium quality (1280x720, 30fps) — faster for testing
- `-q l` : low quality (854x480) — fastest for previewing

---

## Scene Sequence (all in one class, plays in order)

| # | Scene Method | Topic | Duration |
|---|---|---|---|
| 01 | scene_01_intro | Title Card | ~8s |
| 02 | scene_02_what_is | What is Polynomial Regression | ~20s |
| 03 | scene_03_five_ws | The Five W's Overview Cards | ~25s |
| 04 | scene_04_why_linear_fails | Why Linear Regression Fails (Chart) | ~20s |
| 05 | scene_05_overall_pros_cons | Overall Pros and Cons | ~20s |
| 06 | scene_06_hilly_road | Intuition — Hilly Road Analogy | ~18s |
| 07 | scene_07_feature_engineering | Feature Engineering Insight | ~18s |
| 08 | scene_08_real_world | Real-World Examples Table | ~20s |
| 09 | scene_09_equation | The Polynomial Equation | ~22s |
| 10 | scene_10_degree_shapes | Degree Controls the Curve Shape | ~20s |
| 11 | scene_11_why_linear | Why It Is Still Linear | ~18s |
| 12 | scene_12_normal_equations | The Normal Equations | ~18s |
| 13 | scene_13_normal_eq_pros_cons | Normal Equations Pros and Cons | ~18s |
| 14 | scene_14_cost_gd | Cost Function and Gradient Descent | ~18s |
| 15 | scene_15_gd_pros_cons | Gradient Descent Pros and Cons | ~18s |
| 16 | scene_16_assumptions_linemo | Assumptions — LINE-MO Framework | ~18s |
| 17 | scene_17_assumption_linearity | Assumption 1: Linearity | ~18s |
| 18 | scene_18_assumption_independence | Assumption 2: Independence | ~16s |
| 19 | scene_19_assumption_normality | Assumption 3: Normality | ~16s |
| 20 | scene_20_assumption_homoscedasticity | Assumption 4: Homoscedasticity | ~16s |
| 21 | scene_21_assumption_multicollinearity | Assumption 5: Multicollinearity | ~20s |
| 22 | scene_22_multicollinearity_pros_cons | Multicollinearity Pros and Cons | ~16s |
| 23 | scene_23_assumption_outliers | Assumption 6: Outliers | ~16s |
| 24 | scene_24_bias_variance | Bias-Variance Tradeoff | ~22s |
| 25 | scene_25_bv_chart | Bias-Variance Chart | ~20s |
| 26 | scene_26_fitting_cards | Under/Optimal/Overfit Cards | ~20s |
| 27 | scene_27_overfitting | Overfitting Signs | ~20s |
| 28 | scene_28_runge | Runge's Phenomenon | ~18s |
| 29 | scene_29_overfitting_pros_cons | Overfitting Fixes | ~18s |
| 30 | scene_30_underfitting | Underfitting | ~16s |
| 31 | scene_31_visual_inspection | Degree Selection: Visual Inspection | ~16s |
| 32 | scene_32_cross_validation | Degree Selection: Cross-Validation | ~20s |
| 33 | scene_33_learning_curves | Degree Selection: Learning Curves | ~16s |
| 34 | scene_34_aic_bic | Degree Selection: AIC and BIC | ~16s |
| 35 | scene_35_adjusted_r2 | Degree Selection: Adjusted R² | ~14s |
| 36 | scene_36_error_curve | Train vs Validation Error Chart | ~18s |
| 37 | scene_37_regularisation_overview | Regularisation Overview | ~16s |
| 38 | scene_38_ridge | Ridge Regression | ~18s |
| 39 | scene_39_lasso | Lasso Regression | ~18s |
| 40 | scene_40_elasticnet | ElasticNet | ~18s |
| 41 | scene_41_reg_comparison | Regularisation Comparison Table | ~18s |
| 42 | scene_42_alpha_effect | Alpha Hyperparameter Effect | ~16s |
| 43 | scene_43_feature_scaling | Feature Scaling Overview | ~16s |
| 44 | scene_44_standard_scaler | StandardScaler | ~16s |
| 45 | scene_45_minmax | MinMaxScaler Pros and Cons | ~14s |
| 46 | scene_46_centering | Why Centering Reduces Multicollinearity | ~14s |
| 47 | scene_47_feature_explosion | Feature Explosion | ~18s |
| 48 | scene_48_explosion_pros_cons | Feature Explosion Pros and Cons | ~16s |
| 49 | scene_49_mse_rmse | Metrics: MSE and RMSE | ~18s |
| 50 | scene_50_mae_r2 | Metrics: MAE and R² | ~18s |
| 51 | scene_51_adj_r2_mape | Metrics: Adjusted R² and MAPE | ~16s |
| 52 | scene_52_ci_pi | Confidence and Prediction Intervals | ~20s |
| 53 | scene_53_pipeline | scikit-learn Pipeline | ~20s |
| 54 | scene_54_hp_poly | Hyperparameters: PolynomialFeatures | ~18s |
| 55 | scene_55_hp_ridge | Hyperparameters: Ridge | ~18s |
| 56 | scene_56_hp_lasso_enet | Hyperparameters: Lasso and ElasticNet | ~18s |
| 57 | scene_57_overall_pros_cons | Overall Pros and Cons Detailed | ~22s |
| 58 | scene_58_when_to_use | When to Use | ~18s |
| 59 | scene_59_alternatives | Alternatives Comparison Table | ~18s |
| 60 | scene_60_mistakes | Common Mistakes Table | ~20s |
| 61 | scene_61_iq_linear | Interview: Is It Linear? | ~18s |
| 62 | scene_62_iq_overfit | Interview: Why Does It Overfit? | ~18s |
| 63 | scene_63_iq_train_test | Interview: Train 0.99, Test 0.3 | ~18s |
| 64 | scene_64_iq_scale | Interview: Why Scale After Poly? | ~16s |
| 65 | scene_65_iq_lasso_zeros | Interview: Why Lasso Produces Zeros | ~16s |
| 66 | scene_66_outro | Outro / Summary | ~12s |

---

## Colour Palette
- Blue:       #4f9eff
- Orange:     #f97316
- Green:      #10b981
- Yellow:     #fbbf24
- Red:        #f87171
- Purple:     #a855f7
- Background: #0d0f14
- White:      #FFFFFF
- Subtitle BG: #000000 (with white text)

## Notes
- All subtitles use black background with white text
- Subtitles appear at bottom of screen, never overlapping animations
- All symbols (β, ε, ŷ, etc.) use MathTex
- All tables use word-wrap to prevent cell overflow
- Pros/cons always displayed as split-screen green/red panels
