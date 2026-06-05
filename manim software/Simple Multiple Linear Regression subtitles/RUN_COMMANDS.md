# LINEAR REGRESSION VIDEO — RUN COMMANDS REFERENCE

## File Structure Required
```
your_folder/
├── linear_regression_video.py     ← main script (all 82 scenes)
├── generate_individual_scenes.py  ← generates scene wrapper files
├── run_all_scenes.sh              ← Linux/Mac: render all 82 individually
├── run_all_scenes.bat             ← Windows: render all 82 individually
└── scenes/                        ← auto-created by generate_individual_scenes.py
    ├── scene_s01_title.py
    ├── scene_s02_analogy.py
    └── ... (82 wrapper files total)
```

---

## QUALITY FLAGS
| Flag | Quality     | Resolution | Speed  | Use for         |
|------|-------------|------------|--------|-----------------|
| -ql  | Low         | 480p15     | Fast   | Quick preview   |
| -qm  | Medium      | 720p30     | Medium | Draft review    |
| -qh  | High        | 1080p60    | Slow   | Final render    |
| -qk  | 4K          | 2160p60    | Slow   | Ultra quality   |

Add `-p` to auto-open the video after rendering (e.g. `-pqh`).

---

## ═══════════════════════════════════════════
## OPTION A — RENDER FULL VIDEO (ONE COMMAND)
## ═══════════════════════════════════════════

### High quality (1080p60) — RECOMMENDED for final output
```
manim -pqh linear_regression_video.py LinearRegressionVideo
```

### Medium quality (720p30) — faster render, good for drafts
```
manim -pqm linear_regression_video.py LinearRegressionVideo
```

### Low quality (480p15) — fastest, for quick preview
```
manim -pql linear_regression_video.py LinearRegressionVideo
```

### 4K output
```
manim -pqk linear_regression_video.py LinearRegressionVideo
```

**Output location:**
```
media/videos/linear_regression_video/1080p60/LinearRegressionVideo.mp4
```

---

## ═══════════════════════════════════════════
## OPTION B — RENDER EACH SCENE INDIVIDUALLY
## ═══════════════════════════════════════════

### Step 1 — Generate the 82 wrapper files (one time only)
```
python generate_individual_scenes.py
```
This creates `scenes/scene_sXX_*.py` files in a `scenes/` subfolder.

### Step 2 — Render all 82 scenes at once (Linux/Mac)
```
chmod +x run_all_scenes.sh
./run_all_scenes.sh
```

### Step 2 — Render all 82 scenes at once (Windows)
```
run_all_scenes.bat
```

### Step 2 — Render all 82 at low quality (for preview)
```
./run_all_scenes.sh -ql        # Linux/Mac
```
Edit `set QUALITY=-ql` in `run_all_scenes.bat` for Windows.

---

## ═══════════════════════════════════════════
## OPTION C — RENDER ONE SPECIFIC SCENE
## ═══════════════════════════════════════════

Pattern:
```
manim -pqh scenes/scene_<method>.py Scene_<method>
```

### All 82 individual scene commands:

```
manim -pqh scenes/scene_s01_title.py                 Scene_s01_title
manim -pqh scenes/scene_s02_analogy.py               Scene_s02_analogy
manim -pqh scenes/scene_s03_scatter.py               Scene_s03_scatter
manim -pqh scenes/scene_s04_what_how_why_when.py     Scene_s04_what_how_why_when
manim -pqh scenes/scene_s05_simple_vs_multiple.py    Scene_s05_simple_vs_multiple
manim -pqh scenes/scene_s06_overall_pros_cons.py     Scene_s06_overall_pros_cons
manim -pqh scenes/scene_s07_math_model.py            Scene_s07_math_model
manim -pqh scenes/scene_s08_symbol_table.py          Scene_s08_symbol_table
manim -pqh scenes/scene_s09_matrix_form.py           Scene_s09_matrix_form
manim -pqh scenes/scene_s10_error_term.py            Scene_s10_error_term
manim -pqh scenes/scene_s11_coeff_interp.py          Scene_s11_coeff_interp
manim -pqh scenes/scene_s12_ols_cost.py              Scene_s12_ols_cost
manim -pqh scenes/scene_s13_why_square.py            Scene_s13_why_square
manim -pqh scenes/scene_s14_normal_eq.py             Scene_s14_normal_eq
manim -pqh scenes/scene_s15_normal_eq_pc.py          Scene_s15_normal_eq_pc
manim -pqh scenes/scene_s16_linemo_overview.py       Scene_s16_linemo_overview
manim -pqh scenes/scene_s17_linearity.py             Scene_s17_linearity
manim -pqh scenes/scene_s18_linearity_pc.py          Scene_s18_linearity_pc
manim -pqh scenes/scene_s19_homoscedasticity.py      Scene_s19_homoscedasticity
manim -pqh scenes/scene_s20_homo_pc.py               Scene_s20_homo_pc
manim -pqh scenes/scene_s21_multicollinearity.py     Scene_s21_multicollinearity
manim -pqh scenes/scene_s22_multi_pc.py              Scene_s22_multi_pc
manim -pqh scenes/scene_s23_independence.py          Scene_s23_independence
manim -pqh scenes/scene_s24_independence_pc.py       Scene_s24_independence_pc
manim -pqh scenes/scene_s25_normality.py             Scene_s25_normality
manim -pqh scenes/scene_s26_normality_pc.py          Scene_s26_normality_pc
manim -pqh scenes/scene_s27_outliers.py              Scene_s27_outliers
manim -pqh scenes/scene_s28_outliers_pc.py           Scene_s28_outliers_pc
manim -pqh scenes/scene_s29_metrics_overview.py      Scene_s29_metrics_overview
manim -pqh scenes/scene_s30_mse.py                   Scene_s30_mse
manim -pqh scenes/scene_s31_mse_pc.py                Scene_s31_mse_pc
manim -pqh scenes/scene_s32_rmse.py                  Scene_s32_rmse
manim -pqh scenes/scene_s33_rmse_pc.py               Scene_s33_rmse_pc
manim -pqh scenes/scene_s34_mae.py                   Scene_s34_mae
manim -pqh scenes/scene_s35_mae_pc.py                Scene_s35_mae_pc
manim -pqh scenes/scene_s36_r2.py                    Scene_s36_r2
manim -pqh scenes/scene_s37_r2_table.py              Scene_s37_r2_table
manim -pqh scenes/scene_s38_r2_pc.py                 Scene_s38_r2_pc
manim -pqh scenes/scene_s39_adj_r2.py                Scene_s39_adj_r2
manim -pqh scenes/scene_s40_adj_r2_pc.py             Scene_s40_adj_r2_pc
manim -pqh scenes/scene_s41_mape.py                  Scene_s41_mape
manim -pqh scenes/scene_s42_mape_pc.py               Scene_s42_mape_pc
manim -pqh scenes/scene_s43_gd_why.py                Scene_s43_gd_why
manim -pqh scenes/scene_s44_gd_update.py             Scene_s44_gd_update
manim -pqh scenes/scene_s45_gd_steps.py              Scene_s45_gd_steps
manim -pqh scenes/scene_s46_learning_rate.py         Scene_s46_learning_rate
manim -pqh scenes/scene_s47_gd_types.py              Scene_s47_gd_types
manim -pqh scenes/scene_s48_gd_pc.py                 Scene_s48_gd_pc
manim -pqh scenes/scene_s49_reg_problem.py           Scene_s49_reg_problem
manim -pqh scenes/scene_s50_ridge.py                 Scene_s50_ridge
manim -pqh scenes/scene_s51_ridge_pc.py              Scene_s51_ridge_pc
manim -pqh scenes/scene_s52_lasso.py                 Scene_s52_lasso
manim -pqh scenes/scene_s53_lasso_geometry.py        Scene_s53_lasso_geometry
manim -pqh scenes/scene_s54_lasso_pc.py              Scene_s54_lasso_pc
manim -pqh scenes/scene_s55_elasticnet.py            Scene_s55_elasticnet
manim -pqh scenes/scene_s56_enet_pc.py               Scene_s56_enet_pc
manim -pqh scenes/scene_s57_reg_table.py             Scene_s57_reg_table
manim -pqh scenes/scene_s58_diagnostics.py           Scene_s58_diagnostics
manim -pqh scenes/scene_s59_cooks.py                 Scene_s59_cooks
manim -pqh scenes/scene_s60_diag_pc.py               Scene_s60_diag_pc
manim -pqh scenes/scene_s61_feat_eng.py              Scene_s61_feat_eng
manim -pqh scenes/scene_s62_interactions.py          Scene_s62_interactions
manim -pqh scenes/scene_s63_encoding.py              Scene_s63_encoding
manim -pqh scenes/scene_s64_scaling.py               Scene_s64_scaling
manim -pqh scenes/scene_s65_overfit.py               Scene_s65_overfit
manim -pqh scenes/scene_s66_bias_variance.py         Scene_s66_bias_variance
manim -pqh scenes/scene_s67_bv_curve.py              Scene_s67_bv_curve
manim -pqh scenes/scene_s68_bv_table.py              Scene_s68_bv_table
manim -pqh scenes/scene_s69_cv_why.py                Scene_s69_cv_why
manim -pqh scenes/scene_s70_cv_diagram.py            Scene_s70_cv_diagram
manim -pqh scenes/scene_s71_cv_pc.py                 Scene_s71_cv_pc
manim -pqh scenes/scene_s72_pipeline.py              Scene_s72_pipeline
manim -pqh scenes/scene_s73_pipeline_pc.py           Scene_s73_pipeline_pc
manim -pqh scenes/scene_s74_lr_params.py             Scene_s74_lr_params
manim -pqh scenes/scene_s75_ridge_params.py          Scene_s75_ridge_params
manim -pqh scenes/scene_s76_lasso_params.py          Scene_s76_lasso_params
manim -pqh scenes/scene_s77_enet_params.py           Scene_s77_enet_params
manim -pqh scenes/scene_s78_when_to_use.py           Scene_s78_when_to_use
manim -pqh scenes/scene_s79_full_pros_cons.py        Scene_s79_full_pros_cons
manim -pqh scenes/scene_s80_interview_qa.py          Scene_s80_interview_qa
manim -pqh scenes/scene_s81_summary.py               Scene_s81_summary
manim -pqh scenes/scene_s82_end.py                   Scene_s82_end
```

---

## ═══════════════════════════════════════════
## OPTION D — RENDER A SECTION GROUP
## ═══════════════════════════════════════════
Render a logical group of scenes in one go (no wrapper files needed —
just run the full script from the terminal and it renders all of them
back-to-back). Alternatively, edit construct() in linear_regression_video.py
to only call the scenes you want for that session.

### Example: render only the Regularisation section (S49–S57)
Edit construct() temporarily to:
```python
def construct(self):
    self.s49_reg_problem()
    self.s50_ridge()
    self.s51_ridge_pc()
    self.s52_lasso()
    self.s53_lasso_geometry()
    self.s54_lasso_pc()
    self.s55_elasticnet()
    self.s56_enet_pc()
    self.s57_reg_table()
```
Then run:
```
manim -pqh linear_regression_video.py LinearRegressionVideo
```

---

## ═══════════════════════════════════════════
## TIPS
## ═══════════════════════════════════════════

### Preview mode (no file saved, just opens window)
```
manim -p --disable_caching linear_regression_video.py LinearRegressionVideo
```

### Save to a custom output directory
```
manim -qh --media_dir ./output linear_regression_video.py LinearRegressionVideo
```

### Render with transparent background (for compositing)
```
manim -qh --transparent linear_regression_video.py LinearRegressionVideo
```

### Render as GIF instead of MP4
```
manim -qm --format gif linear_regression_video.py LinearRegressionVideo
```

### Skip cache (force full re-render)
```
manim -qh --disable_caching linear_regression_video.py LinearRegressionVideo
```

### Install Manim CE (if not installed)
```
pip install manim
```
Requires: Python 3.8+, LaTeX (MiKTeX on Windows / TeX Live on Linux/Mac), ffmpeg.

---

## OUTPUT FILE LOCATIONS

| Render type       | Output path                                                          |
|-------------------|----------------------------------------------------------------------|
| Full video        | media/videos/linear_regression_video/1080p60/LinearRegressionVideo.mp4 |
| Individual scene  | media/videos/scenes/scene_sXX_*/1080p60/Scene_sXX_*.mp4             |
| GIF               | media/videos/linear_regression_video/480p15/LinearRegressionVideo.gif |


python run_parallel.py --scenes 14 27 53 57 62 74 75 76 77 78