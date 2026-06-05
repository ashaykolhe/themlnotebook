# -*- coding: utf-8 -*-
"""
generate_individual_scenes.py

Run this ONCE to create 82 individual scene wrapper files.
Place this file in the SAME folder as linear_regression_video.py, then run:

    python generate_individual_scenes.py

Each generated file is named  scene_sXX_<name>.py  and lives in the
SAME folder -- so Python can always find linear_regression_video.py
via a plain  import linear_regression_video  without any path tricks.

Render one scene:
    manim -pqh scene_s03_scatter.py Scene_s03_scatter

Render all 82 (Linux/Mac):
    ./run_all_scenes.sh

Render all 82 (Windows):
    run_all_scenes.bat
"""

import os

SCENE_METHODS = [
    ("s01_title",             "S01 - Title Card"),
    ("s02_analogy",           "S02 - Real-World Analogy"),
    ("s03_scatter",           "S03 - House Price Scatter + Best Fit Line"),
    ("s04_what_how_why_when", "S04 - What / How / Why / When Grid"),
    ("s05_simple_vs_multiple","S05 - Simple vs Multiple Table"),
    ("s06_overall_pros_cons", "S06 - Overall Pros & Cons"),
    ("s07_math_model",        "S07 - The Mathematical Model"),
    ("s08_symbol_table",      "S08 - Symbol Table"),
    ("s09_matrix_form",       "S09 - Matrix / Vector Form"),
    ("s10_error_term",        "S10 - True Model & Error Term"),
    ("s11_coeff_interp",      "S11 - Coefficient Interpretation"),
    ("s12_ols_cost",          "S12 - OLS Cost Function"),
    ("s13_why_square",        "S13 - Why Square the Errors"),
    ("s14_normal_eq",         "S14 - Normal Equation Derivation"),
    ("s15_normal_eq_pc",      "S15 - Normal Equation Pros & Cons"),
    ("s16_linemo_overview",   "S16 - LINE-MO Assumptions Overview"),
    ("s17_linearity",         "S17 - Linearity Assumption Plots"),
    ("s18_linearity_pc",      "S18 - Linearity Pros & Cons"),
    ("s19_homoscedasticity",  "S19 - Homoscedasticity Equal Variance"),
    ("s20_homo_pc",           "S20 - Homoscedasticity Pros & Cons"),
    ("s21_multicollinearity", "S21 - No Multicollinearity"),
    ("s22_multi_pc",          "S22 - Multicollinearity Pros & Cons"),
    ("s23_independence",      "S23 - Independence of Errors"),
    ("s24_independence_pc",   "S24 - Independence Pros & Cons"),
    ("s25_normality",         "S25 - Normality of Residuals"),
    ("s26_normality_pc",      "S26 - Normality Pros & Cons"),
    ("s27_outliers",          "S27 - Outliers Leverage"),
    ("s28_outliers_pc",       "S28 - Outliers Pros & Cons"),
    ("s29_metrics_overview",  "S29 - Evaluation Metrics Overview"),
    ("s30_mse",               "S30 - MSE Formula"),
    ("s31_mse_pc",            "S31 - MSE Pros & Cons"),
    ("s32_rmse",              "S32 - RMSE Formula"),
    ("s33_rmse_pc",           "S33 - RMSE Pros & Cons"),
    ("s34_mae",               "S34 - MAE Formula"),
    ("s35_mae_pc",            "S35 - MAE Pros & Cons"),
    ("s36_r2",                "S36 - R2 Formula + Bar Visual"),
    ("s37_r2_table",          "S37 - R2 Interpretation Table"),
    ("s38_r2_pc",             "S38 - R2 Pros & Cons"),
    ("s39_adj_r2",            "S39 - Adjusted R2"),
    ("s40_adj_r2_pc",         "S40 - Adjusted R2 Pros & Cons"),
    ("s41_mape",              "S41 - MAPE Formula"),
    ("s42_mape_pc",           "S42 - MAPE Pros & Cons"),
    ("s43_gd_why",            "S43 - Gradient Descent Why"),
    ("s44_gd_update",         "S44 - Gradient Descent Update Rule"),
    ("s45_gd_steps",          "S45 - Gradient Descent Steps"),
    ("s46_learning_rate",     "S46 - Learning Rate Convergence Curves"),
    ("s47_gd_types",          "S47 - GD Types Table"),
    ("s48_gd_pc",             "S48 - Gradient Descent Pros & Cons"),
    ("s49_reg_problem",       "S49 - Regularisation The Problem"),
    ("s50_ridge",             "S50 - Ridge Cost Function"),
    ("s51_ridge_pc",          "S51 - Ridge Pros & Cons"),
    ("s52_lasso",             "S52 - Lasso Cost Function"),
    ("s53_lasso_geometry",    "S53 - Lasso Geometric Intuition"),
    ("s54_lasso_pc",          "S54 - Lasso Pros & Cons"),
    ("s55_elasticnet",        "S55 - ElasticNet"),
    ("s56_enet_pc",           "S56 - ElasticNet Pros & Cons"),
    ("s57_reg_table",         "S57 - Regularisation Comparison Table"),
    ("s58_diagnostics",       "S58 - Residual Diagnostics 4 Plots"),
    ("s59_cooks",             "S59 - Cooks Distance"),
    ("s60_diag_pc",           "S60 - Diagnostics Pros & Cons"),
    ("s61_feat_eng",          "S61 - Feature Engineering Transforms"),
    ("s62_interactions",      "S62 - Interaction Terms"),
    ("s63_encoding",          "S63 - Encoding Categorical Features"),
    ("s64_scaling",           "S64 - Feature Scaling Table"),
    ("s65_overfit",           "S65 - Overfitting Underfitting 3 Curves"),
    ("s66_bias_variance",     "S66 - Bias Variance Decomposition"),
    ("s67_bv_curve",          "S67 - Bias Variance Tradeoff Curve"),
    ("s68_bv_table",          "S68 - Bias Variance Table"),
    ("s69_cv_why",            "S69 - Cross Validation Why"),
    ("s70_cv_diagram",        "S70 - 5-Fold CV Diagram"),
    ("s71_cv_pc",             "S71 - CV Pros & Cons"),
    ("s72_pipeline",          "S72 - Pipelines and Data Leakage"),
    ("s73_pipeline_pc",       "S73 - Pipeline Pros & Cons"),
    ("s74_lr_params",         "S74 - sklearn LinearRegression Params"),
    ("s75_ridge_params",      "S75 - sklearn Ridge Params"),
    ("s76_lasso_params",      "S76 - sklearn Lasso Params"),
    ("s77_enet_params",       "S77 - sklearn ElasticNet Params"),
    ("s78_when_to_use",       "S78 - When to Use Decision Table"),
    ("s79_full_pros_cons",    "S79 - Full Overall Pros and Cons"),
    ("s80_interview_qa",      "S80 - Interview QA Highlights"),
    ("s81_summary",           "S81 - Master Summary"),
    ("s82_end",               "S82 - End Card"),
]

# -----------------------------------------------------------------------
# Wrapper template.
# NOTE: no subdirectory -- file lives next to linear_regression_video.py
# so the import works with zero path manipulation on all platforms.
# -----------------------------------------------------------------------
WRAPPER_TEMPLATE = """\
# -*- coding: utf-8 -*-
# {title}
# Run: manim -pqh scene_{method}.py Scene_{method}
#
# IMPORTANT: keep this file in the SAME folder as linear_regression_video.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linear_regression_video import LinearRegressionVideo

class Scene_{method}(LinearRegressionVideo):
    def construct(self):
        self.{method}()
"""

# Write all wrapper files into the CURRENT directory (same as main script)
this_dir = os.path.dirname(os.path.abspath(__file__))
generated = 0

for method, title in SCENE_METHODS:
    filename = os.path.join(this_dir, f"scene_{method}.py")
    content = WRAPPER_TEMPLATE.format(method=method, title=title)
    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(content)
    generated += 1

print(f"Generated {generated} wrapper files in: {this_dir}")
print()
print("To render ONE scene (example):")
print("  manim -pqh scene_s03_scatter.py Scene_s03_scatter")
print()
print("To render ALL 82 scenes:")
print("  Linux/Mac: chmod +x run_all_scenes.sh && ./run_all_scenes.sh")
print("  Windows:   run_all_scenes.bat")
