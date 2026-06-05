#!/bin/bash
# run_all_scenes.sh  --  Linux / Mac
# Renders all 82 scenes one by one.
#
# Usage:
#   chmod +x run_all_scenes.sh
#   ./run_all_scenes.sh          # 1080p60 (default)
#   ./run_all_scenes.sh -ql      # 480p15  (fast preview)
#   ./run_all_scenes.sh -qm      # 720p30  (medium)
#
# Output: media/videos/scene_sXX_*/1080p60/Scene_sXX_*.mp4
#
# IMPORTANT: run this from the folder that contains linear_regression_video.py

set -e
QUALITY=${1:--qh}
TOTAL=82
COUNT=0

echo "========================================"
echo " Linear Regression -- Rendering 82 Scenes"
echo " Quality flag : $QUALITY"
echo " Working dir  : $(pwd)"
echo "========================================"

# Generate wrapper files if not present yet
if [ ! -f "scene_s01_title.py" ]; then
    echo "Generating wrapper files..."
    python generate_individual_scenes.py
fi

run_scene() {
    local file=$1
    local cls=$2
    local label=$3
    COUNT=$((COUNT+1))
    echo "[$COUNT/$TOTAL] Rendering: $label"
    manim $QUALITY "$file" "$cls"
}

run_scene scene_s01_title.py                 Scene_s01_title                "S01 - Title Card"
run_scene scene_s02_analogy.py               Scene_s02_analogy               "S02 - Analogy"
run_scene scene_s03_scatter.py               Scene_s03_scatter               "S03 - Scatter Plot"
run_scene scene_s04_what_how_why_when.py     Scene_s04_what_how_why_when     "S04 - What/How/Why/When"
run_scene scene_s05_simple_vs_multiple.py    Scene_s05_simple_vs_multiple    "S05 - Simple vs Multiple"
run_scene scene_s06_overall_pros_cons.py     Scene_s06_overall_pros_cons     "S06 - Overall Pros & Cons"
run_scene scene_s07_math_model.py            Scene_s07_math_model            "S07 - Math Model"
run_scene scene_s08_symbol_table.py          Scene_s08_symbol_table          "S08 - Symbol Table"
run_scene scene_s09_matrix_form.py           Scene_s09_matrix_form           "S09 - Matrix Form"
run_scene scene_s10_error_term.py            Scene_s10_error_term            "S10 - Error Term"
run_scene scene_s11_coeff_interp.py          Scene_s11_coeff_interp          "S11 - Coefficient Interp"
run_scene scene_s12_ols_cost.py              Scene_s12_ols_cost              "S12 - OLS Cost"
run_scene scene_s13_why_square.py            Scene_s13_why_square            "S13 - Why Square"
run_scene scene_s14_normal_eq.py             Scene_s14_normal_eq             "S14 - Normal Equation"
run_scene scene_s15_normal_eq_pc.py          Scene_s15_normal_eq_pc          "S15 - Normal Eq P&C"
run_scene scene_s16_linemo_overview.py       Scene_s16_linemo_overview       "S16 - LINE-MO Overview"
run_scene scene_s17_linearity.py             Scene_s17_linearity             "S17 - Linearity"
run_scene scene_s18_linearity_pc.py          Scene_s18_linearity_pc          "S18 - Linearity P&C"
run_scene scene_s19_homoscedasticity.py      Scene_s19_homoscedasticity      "S19 - Homoscedasticity"
run_scene scene_s20_homo_pc.py               Scene_s20_homo_pc               "S20 - Homoscedasticity P&C"
run_scene scene_s21_multicollinearity.py     Scene_s21_multicollinearity     "S21 - Multicollinearity"
run_scene scene_s22_multi_pc.py              Scene_s22_multi_pc              "S22 - Multicollinearity P&C"
run_scene scene_s23_independence.py          Scene_s23_independence          "S23 - Independence"
run_scene scene_s24_independence_pc.py       Scene_s24_independence_pc       "S24 - Independence P&C"
run_scene scene_s25_normality.py             Scene_s25_normality             "S25 - Normality"
run_scene scene_s26_normality_pc.py          Scene_s26_normality_pc          "S26 - Normality P&C"
run_scene scene_s27_outliers.py              Scene_s27_outliers              "S27 - Outliers"
run_scene scene_s28_outliers_pc.py           Scene_s28_outliers_pc           "S28 - Outliers P&C"
run_scene scene_s29_metrics_overview.py      Scene_s29_metrics_overview      "S29 - Metrics Overview"
run_scene scene_s30_mse.py                   Scene_s30_mse                   "S30 - MSE"
run_scene scene_s31_mse_pc.py                Scene_s31_mse_pc                "S31 - MSE P&C"
run_scene scene_s32_rmse.py                  Scene_s32_rmse                  "S32 - RMSE"
run_scene scene_s33_rmse_pc.py               Scene_s33_rmse_pc               "S33 - RMSE P&C"
run_scene scene_s34_mae.py                   Scene_s34_mae                   "S34 - MAE"
run_scene scene_s35_mae_pc.py                Scene_s35_mae_pc                "S35 - MAE P&C"
run_scene scene_s36_r2.py                    Scene_s36_r2                    "S36 - R2"
run_scene scene_s37_r2_table.py              Scene_s37_r2_table              "S37 - R2 Table"
run_scene scene_s38_r2_pc.py                 Scene_s38_r2_pc                 "S38 - R2 P&C"
run_scene scene_s39_adj_r2.py                Scene_s39_adj_r2                "S39 - Adjusted R2"
run_scene scene_s40_adj_r2_pc.py             Scene_s40_adj_r2_pc             "S40 - Adjusted R2 P&C"
run_scene scene_s41_mape.py                  Scene_s41_mape                  "S41 - MAPE"
run_scene scene_s42_mape_pc.py               Scene_s42_mape_pc               "S42 - MAPE P&C"
run_scene scene_s43_gd_why.py                Scene_s43_gd_why                "S43 - GD Why"
run_scene scene_s44_gd_update.py             Scene_s44_gd_update             "S44 - GD Update Rule"
run_scene scene_s45_gd_steps.py              Scene_s45_gd_steps              "S45 - GD Steps"
run_scene scene_s46_learning_rate.py         Scene_s46_learning_rate         "S46 - Learning Rate"
run_scene scene_s47_gd_types.py              Scene_s47_gd_types              "S47 - GD Types"
run_scene scene_s48_gd_pc.py                 Scene_s48_gd_pc                 "S48 - GD P&C"
run_scene scene_s49_reg_problem.py           Scene_s49_reg_problem           "S49 - Reg Problem"
run_scene scene_s50_ridge.py                 Scene_s50_ridge                 "S50 - Ridge"
run_scene scene_s51_ridge_pc.py              Scene_s51_ridge_pc              "S51 - Ridge P&C"
run_scene scene_s52_lasso.py                 Scene_s52_lasso                 "S52 - Lasso"
run_scene scene_s53_lasso_geometry.py        Scene_s53_lasso_geometry        "S53 - Lasso Geometry"
run_scene scene_s54_lasso_pc.py              Scene_s54_lasso_pc              "S54 - Lasso P&C"
run_scene scene_s55_elasticnet.py            Scene_s55_elasticnet            "S55 - ElasticNet"
run_scene scene_s56_enet_pc.py               Scene_s56_enet_pc               "S56 - ElasticNet P&C"
run_scene scene_s57_reg_table.py             Scene_s57_reg_table             "S57 - Reg Table"
run_scene scene_s58_diagnostics.py           Scene_s58_diagnostics           "S58 - Diagnostics"
run_scene scene_s59_cooks.py                 Scene_s59_cooks                 "S59 - Cooks Distance"
run_scene scene_s60_diag_pc.py               Scene_s60_diag_pc               "S60 - Diag P&C"
run_scene scene_s61_feat_eng.py              Scene_s61_feat_eng              "S61 - Feature Eng"
run_scene scene_s62_interactions.py          Scene_s62_interactions          "S62 - Interactions"
run_scene scene_s63_encoding.py              Scene_s63_encoding              "S63 - Encoding"
run_scene scene_s64_scaling.py               Scene_s64_scaling               "S64 - Scaling"
run_scene scene_s65_overfit.py               Scene_s65_overfit               "S65 - Overfit"
run_scene scene_s66_bias_variance.py         Scene_s66_bias_variance         "S66 - Bias Variance"
run_scene scene_s67_bv_curve.py              Scene_s67_bv_curve              "S67 - BV Curve"
run_scene scene_s68_bv_table.py              Scene_s68_bv_table              "S68 - BV Table"
run_scene scene_s69_cv_why.py                Scene_s69_cv_why                "S69 - CV Why"
run_scene scene_s70_cv_diagram.py            Scene_s70_cv_diagram            "S70 - CV Diagram"
run_scene scene_s71_cv_pc.py                 Scene_s71_cv_pc                 "S71 - CV P&C"
run_scene scene_s72_pipeline.py              Scene_s72_pipeline              "S72 - Pipeline"
run_scene scene_s73_pipeline_pc.py           Scene_s73_pipeline_pc           "S73 - Pipeline P&C"
run_scene scene_s74_lr_params.py             Scene_s74_lr_params             "S74 - LR Params"
run_scene scene_s75_ridge_params.py          Scene_s75_ridge_params          "S75 - Ridge Params"
run_scene scene_s76_lasso_params.py          Scene_s76_lasso_params          "S76 - Lasso Params"
run_scene scene_s77_enet_params.py           Scene_s77_enet_params           "S77 - ElasticNet Params"
run_scene scene_s78_when_to_use.py           Scene_s78_when_to_use           "S78 - When to Use"
run_scene scene_s79_full_pros_cons.py        Scene_s79_full_pros_cons        "S79 - Full Pros Cons"
run_scene scene_s80_interview_qa.py          Scene_s80_interview_qa          "S80 - Interview QA"
run_scene scene_s81_summary.py               Scene_s81_summary               "S81 - Summary"
run_scene scene_s82_end.py                   Scene_s82_end                   "S82 - End Card"

echo ""
echo "========================================"
echo " All $TOTAL scenes rendered successfully!"
echo " Output: media/videos/scene_sXX_*/1080p60/"
echo "========================================"
