@echo off
REM run_all_scenes.bat  --  Windows
REM Renders all 82 scenes one by one.
REM
REM Usage: Double-click or run from Command Prompt:
REM   run_all_scenes.bat
REM
REM For faster preview, change -qh to -ql below.
REM
REM IMPORTANT: run from the folder that contains linear_regression_video.py

set QUALITY=-ql
set TOTAL=82
set COUNT=0

echo ========================================
echo  Linear Regression - Rendering 82 Scenes
echo  Quality : %QUALITY%
echo  Folder  : %CD%
echo ========================================

REM Generate wrapper files if not present yet
if not exist scene_s01_title.py (
    echo Generating wrapper files...
    python generate_individual_scenes.py
)

manim %QUALITY% scene_s01_title.py                 Scene_s01_title
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S01 Title Card

manim %QUALITY% scene_s02_analogy.py               Scene_s02_analogy
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S02 Analogy

manim %QUALITY% scene_s03_scatter.py               Scene_s03_scatter
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S03 Scatter Plot

manim %QUALITY% scene_s04_what_how_why_when.py     Scene_s04_what_how_why_when
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S04 What How Why When

manim %QUALITY% scene_s05_simple_vs_multiple.py    Scene_s05_simple_vs_multiple
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S05 Simple vs Multiple

manim %QUALITY% scene_s06_overall_pros_cons.py     Scene_s06_overall_pros_cons
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S06 Overall Pros Cons

manim %QUALITY% scene_s07_math_model.py            Scene_s07_math_model
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S07 Math Model

manim %QUALITY% scene_s08_symbol_table.py          Scene_s08_symbol_table
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S08 Symbol Table

manim %QUALITY% scene_s09_matrix_form.py           Scene_s09_matrix_form
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S09 Matrix Form

manim %QUALITY% scene_s10_error_term.py            Scene_s10_error_term
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S10 Error Term

manim %QUALITY% scene_s11_coeff_interp.py          Scene_s11_coeff_interp
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S11 Coefficient Interpretation

manim %QUALITY% scene_s12_ols_cost.py              Scene_s12_ols_cost
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S12 OLS Cost

manim %QUALITY% scene_s13_why_square.py            Scene_s13_why_square
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S13 Why Square

manim %QUALITY% scene_s14_normal_eq.py             Scene_s14_normal_eq
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S14 Normal Equation

manim %QUALITY% scene_s15_normal_eq_pc.py          Scene_s15_normal_eq_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S15 Normal Eq PC

manim %QUALITY% scene_s16_linemo_overview.py       Scene_s16_linemo_overview
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S16 LINE-MO Overview

manim %QUALITY% scene_s17_linearity.py             Scene_s17_linearity
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S17 Linearity

manim %QUALITY% scene_s18_linearity_pc.py          Scene_s18_linearity_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S18 Linearity PC

manim %QUALITY% scene_s19_homoscedasticity.py      Scene_s19_homoscedasticity
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S19 Homoscedasticity

manim %QUALITY% scene_s20_homo_pc.py               Scene_s20_homo_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S20 Homoscedasticity PC

manim %QUALITY% scene_s21_multicollinearity.py     Scene_s21_multicollinearity
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S21 Multicollinearity

manim %QUALITY% scene_s22_multi_pc.py              Scene_s22_multi_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S22 Multicollinearity PC

manim %QUALITY% scene_s23_independence.py          Scene_s23_independence
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S23 Independence

manim %QUALITY% scene_s24_independence_pc.py       Scene_s24_independence_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S24 Independence PC

manim %QUALITY% scene_s25_normality.py             Scene_s25_normality
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S25 Normality

manim %QUALITY% scene_s26_normality_pc.py          Scene_s26_normality_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S26 Normality PC

manim %QUALITY% scene_s27_outliers.py              Scene_s27_outliers
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S27 Outliers

manim %QUALITY% scene_s28_outliers_pc.py           Scene_s28_outliers_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S28 Outliers PC

manim %QUALITY% scene_s29_metrics_overview.py      Scene_s29_metrics_overview
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S29 Metrics Overview

manim %QUALITY% scene_s30_mse.py                   Scene_s30_mse
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S30 MSE

manim %QUALITY% scene_s31_mse_pc.py                Scene_s31_mse_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S31 MSE PC

manim %QUALITY% scene_s32_rmse.py                  Scene_s32_rmse
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S32 RMSE

manim %QUALITY% scene_s33_rmse_pc.py               Scene_s33_rmse_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S33 RMSE PC

manim %QUALITY% scene_s34_mae.py                   Scene_s34_mae
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S34 MAE

manim %QUALITY% scene_s35_mae_pc.py                Scene_s35_mae_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S35 MAE PC

manim %QUALITY% scene_s36_r2.py                    Scene_s36_r2
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S36 R2

manim %QUALITY% scene_s37_r2_table.py              Scene_s37_r2_table
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S37 R2 Table

manim %QUALITY% scene_s38_r2_pc.py                 Scene_s38_r2_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S38 R2 PC

manim %QUALITY% scene_s39_adj_r2.py                Scene_s39_adj_r2
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S39 Adjusted R2

manim %QUALITY% scene_s40_adj_r2_pc.py             Scene_s40_adj_r2_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S40 Adjusted R2 PC

manim %QUALITY% scene_s41_mape.py                  Scene_s41_mape
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S41 MAPE

manim %QUALITY% scene_s42_mape_pc.py               Scene_s42_mape_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S42 MAPE PC

manim %QUALITY% scene_s43_gd_why.py                Scene_s43_gd_why
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S43 GD Why

manim %QUALITY% scene_s44_gd_update.py             Scene_s44_gd_update
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S44 GD Update Rule

manim %QUALITY% scene_s45_gd_steps.py              Scene_s45_gd_steps
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S45 GD Steps

manim %QUALITY% scene_s46_learning_rate.py         Scene_s46_learning_rate
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S46 Learning Rate

manim %QUALITY% scene_s47_gd_types.py              Scene_s47_gd_types
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S47 GD Types

manim %QUALITY% scene_s48_gd_pc.py                 Scene_s48_gd_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S48 GD PC

manim %QUALITY% scene_s49_reg_problem.py           Scene_s49_reg_problem
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S49 Reg Problem

manim %QUALITY% scene_s50_ridge.py                 Scene_s50_ridge
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S50 Ridge

manim %QUALITY% scene_s51_ridge_pc.py              Scene_s51_ridge_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S51 Ridge PC

manim %QUALITY% scene_s52_lasso.py                 Scene_s52_lasso
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S52 Lasso

manim %QUALITY% scene_s53_lasso_geometry.py        Scene_s53_lasso_geometry
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S53 Lasso Geometry

manim %QUALITY% scene_s54_lasso_pc.py              Scene_s54_lasso_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S54 Lasso PC

manim %QUALITY% scene_s55_elasticnet.py            Scene_s55_elasticnet
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S55 ElasticNet

manim %QUALITY% scene_s56_enet_pc.py               Scene_s56_enet_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S56 ElasticNet PC

manim %QUALITY% scene_s57_reg_table.py             Scene_s57_reg_table
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S57 Reg Table

manim %QUALITY% scene_s58_diagnostics.py           Scene_s58_diagnostics
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S58 Diagnostics

manim %QUALITY% scene_s59_cooks.py                 Scene_s59_cooks
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S59 Cooks Distance

manim %QUALITY% scene_s60_diag_pc.py               Scene_s60_diag_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S60 Diagnostics PC

manim %QUALITY% scene_s61_feat_eng.py              Scene_s61_feat_eng
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S61 Feature Eng

manim %QUALITY% scene_s62_interactions.py          Scene_s62_interactions
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S62 Interactions

manim %QUALITY% scene_s63_encoding.py              Scene_s63_encoding
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S63 Encoding

manim %QUALITY% scene_s64_scaling.py               Scene_s64_scaling
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S64 Scaling

manim %QUALITY% scene_s65_overfit.py               Scene_s65_overfit
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S65 Overfit

manim %QUALITY% scene_s66_bias_variance.py         Scene_s66_bias_variance
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S66 Bias Variance

manim %QUALITY% scene_s67_bv_curve.py              Scene_s67_bv_curve
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S67 BV Curve

manim %QUALITY% scene_s68_bv_table.py              Scene_s68_bv_table
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S68 BV Table

manim %QUALITY% scene_s69_cv_why.py                Scene_s69_cv_why
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S69 CV Why

manim %QUALITY% scene_s70_cv_diagram.py            Scene_s70_cv_diagram
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S70 CV Diagram

manim %QUALITY% scene_s71_cv_pc.py                 Scene_s71_cv_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S71 CV PC

manim %QUALITY% scene_s72_pipeline.py              Scene_s72_pipeline
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S72 Pipeline

manim %QUALITY% scene_s73_pipeline_pc.py           Scene_s73_pipeline_pc
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S73 Pipeline PC

manim %QUALITY% scene_s74_lr_params.py             Scene_s74_lr_params
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S74 LR Params

manim %QUALITY% scene_s75_ridge_params.py          Scene_s75_ridge_params
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S75 Ridge Params

manim %QUALITY% scene_s76_lasso_params.py          Scene_s76_lasso_params
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S76 Lasso Params

manim %QUALITY% scene_s77_enet_params.py           Scene_s77_enet_params
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S77 ElasticNet Params

manim %QUALITY% scene_s78_when_to_use.py           Scene_s78_when_to_use
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S78 When to Use

manim %QUALITY% scene_s79_full_pros_cons.py        Scene_s79_full_pros_cons
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S79 Full Pros Cons

manim %QUALITY% scene_s80_interview_qa.py          Scene_s80_interview_qa
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S80 Interview QA

manim %QUALITY% scene_s81_summary.py               Scene_s81_summary
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S81 Summary

manim %QUALITY% scene_s82_end.py                   Scene_s82_end
set /a COUNT+=1 & echo [%COUNT%/%TOTAL%] Done: S82 End Card

echo.
echo ========================================
echo  All %TOTAL% scenes rendered!
echo  Output: media\videos\scene_sXX_*\1080p60\
echo ========================================
pause
