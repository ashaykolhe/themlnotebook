# -*- coding: utf-8 -*-
"""
run_parallel.py
Renders all 82 individual scene files in parallel using a worker pool.

Usage
-----
    # Auto-detect CPU cores, high quality (default)
    python run_parallel.py

    # Explicit worker count and quality
    python run_parallel.py --workers 4 --quality h

    # Low quality fast preview
    python run_parallel.py --quality l

    # Only render specific scenes (space-separated scene numbers)
    python run_parallel.py --scenes 1 2 3 53 65

Quality flags
-------------
    l  = 480p15  (fastest, good for previewing)
    m  = 720p30
    h  = 1080p60 (default, YouTube upload quality)
    k  = 2160p60 (4K, very slow)

Output
------
    media/videos/scene_sXX_<name>/<quality>/Scene_sXX_<name>.mp4

How parallelism works
---------------------
    Each scene is a fully independent manim call.
    A pool of N workers (default = CPU core count) runs N scenes at once.
    When one finishes the next queued scene starts immediately.
    On a 4-core machine, ~4x speedup over sequential.
    On an 8-core machine, ~8x speedup over sequential.

Worker count guidance
---------------------
    Each manim render uses 1 CPU core and ~300-600 MB RAM.
    workers = min(cpu_count, available_ram_GB // 0.5)
    If you see memory errors, reduce --workers.

IMPORTANT
---------
    Run this from the folder that contains linear_regression_video.py.
    The wrapper files (scene_sXX_*.py) must exist in the same folder.
    If they don't, run: python generate_individual_scenes.py first.
"""

import argparse
import multiprocessing
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# ---------------------------------------------------------------------------
# All 82 scenes: (number, method_name, class_name, description)
# ---------------------------------------------------------------------------
ALL_SCENES = [
    ( 1, "s01_title",             "Scene_s01_title",             "Title Card"),
    ( 2, "s02_analogy",           "Scene_s02_analogy",           "Real-World Analogy"),
    ( 3, "s03_scatter",           "Scene_s03_scatter",           "House Price Scatter"),
    ( 4, "s04_what_how_why_when", "Scene_s04_what_how_why_when", "What/How/Why/When"),
    ( 5, "s05_simple_vs_multiple","Scene_s05_simple_vs_multiple","Simple vs Multiple"),
    ( 6, "s06_overall_pros_cons", "Scene_s06_overall_pros_cons", "Overall Pros & Cons"),
    ( 7, "s07_math_model",        "Scene_s07_math_model",        "Mathematical Model"),
    ( 8, "s08_symbol_table",      "Scene_s08_symbol_table",      "Symbol Table"),
    ( 9, "s09_matrix_form",       "Scene_s09_matrix_form",       "Matrix Form"),
    (10, "s10_error_term",        "Scene_s10_error_term",        "Error Term"),
    (11, "s11_coeff_interp",      "Scene_s11_coeff_interp",      "Coefficient Interpretation"),
    (12, "s12_ols_cost",          "Scene_s12_ols_cost",          "OLS Cost Function"),
    (13, "s13_why_square",        "Scene_s13_why_square",        "Why Square Errors"),
    (14, "s14_normal_eq",         "Scene_s14_normal_eq",         "Normal Equation"),
    (15, "s15_normal_eq_pc",      "Scene_s15_normal_eq_pc",      "Normal Equation P&C"),
    (16, "s16_linemo_overview",   "Scene_s16_linemo_overview",   "LINE-MO Overview"),
    (17, "s17_linearity",         "Scene_s17_linearity",         "Linearity Plots"),
    (18, "s18_linearity_pc",      "Scene_s18_linearity_pc",      "Linearity P&C"),
    (19, "s19_homoscedasticity",  "Scene_s19_homoscedasticity",  "Homoscedasticity"),
    (20, "s20_homo_pc",           "Scene_s20_homo_pc",           "Homoscedasticity P&C"),
    (21, "s21_multicollinearity", "Scene_s21_multicollinearity", "Multicollinearity"),
    (22, "s22_multi_pc",          "Scene_s22_multi_pc",          "Multicollinearity P&C"),
    (23, "s23_independence",      "Scene_s23_independence",      "Independence"),
    (24, "s24_independence_pc",   "Scene_s24_independence_pc",   "Independence P&C"),
    (25, "s25_normality",         "Scene_s25_normality",         "Normality"),
    (26, "s26_normality_pc",      "Scene_s26_normality_pc",      "Normality P&C"),
    (27, "s27_outliers",          "Scene_s27_outliers",          "Outliers"),
    (28, "s28_outliers_pc",       "Scene_s28_outliers_pc",       "Outliers P&C"),
    (29, "s29_metrics_overview",  "Scene_s29_metrics_overview",  "Metrics Overview"),
    (30, "s30_mse",               "Scene_s30_mse",               "MSE"),
    (31, "s31_mse_pc",            "Scene_s31_mse_pc",            "MSE P&C"),
    (32, "s32_rmse",              "Scene_s32_rmse",              "RMSE"),
    (33, "s33_rmse_pc",           "Scene_s33_rmse_pc",           "RMSE P&C"),
    (34, "s34_mae",               "Scene_s34_mae",               "MAE"),
    (35, "s35_mae_pc",            "Scene_s35_mae_pc",            "MAE P&C"),
    (36, "s36_r2",                "Scene_s36_r2",                "R-squared"),
    (37, "s37_r2_table",          "Scene_s37_r2_table",          "R-squared Table"),
    (38, "s38_r2_pc",             "Scene_s38_r2_pc",             "R-squared P&C"),
    (39, "s39_adj_r2",            "Scene_s39_adj_r2",            "Adjusted R-squared"),
    (40, "s40_adj_r2_pc",         "Scene_s40_adj_r2_pc",         "Adjusted R-squared P&C"),
    (41, "s41_mape",              "Scene_s41_mape",              "MAPE"),
    (42, "s42_mape_pc",           "Scene_s42_mape_pc",           "MAPE P&C"),
    (43, "s43_gd_why",            "Scene_s43_gd_why",            "GD Why"),
    (44, "s44_gd_update",         "Scene_s44_gd_update",         "GD Update Rule"),
    (45, "s45_gd_steps",          "Scene_s45_gd_steps",          "GD Steps"),
    (46, "s46_learning_rate",     "Scene_s46_learning_rate",     "Learning Rate"),
    (47, "s47_gd_types",          "Scene_s47_gd_types",          "GD Types Table"),
    (48, "s48_gd_pc",             "Scene_s48_gd_pc",             "GD P&C"),
    (49, "s49_reg_problem",       "Scene_s49_reg_problem",       "Regularisation Problem"),
    (50, "s50_ridge",             "Scene_s50_ridge",             "Ridge"),
    (51, "s51_ridge_pc",          "Scene_s51_ridge_pc",          "Ridge P&C"),
    (52, "s52_lasso",             "Scene_s52_lasso",             "Lasso"),
    (53, "s53_lasso_geometry",    "Scene_s53_lasso_geometry",    "Lasso Geometry"),
    (54, "s54_lasso_pc",          "Scene_s54_lasso_pc",          "Lasso P&C"),
    (55, "s55_elasticnet",        "Scene_s55_elasticnet",        "ElasticNet"),
    (56, "s56_enet_pc",           "Scene_s56_enet_pc",           "ElasticNet P&C"),
    (57, "s57_reg_table",         "Scene_s57_reg_table",         "Reg Comparison Table"),
    (58, "s58_diagnostics",       "Scene_s58_diagnostics",       "4 Diagnostic Plots"),
    (59, "s59_cooks",             "Scene_s59_cooks",             "Cook's Distance"),
    (60, "s60_diag_pc",           "Scene_s60_diag_pc",           "Diagnostics P&C"),
    (61, "s61_feat_eng",          "Scene_s61_feat_eng",          "Feature Engineering"),
    (62, "s62_interactions",      "Scene_s62_interactions",      "Interaction Terms"),
    (63, "s63_encoding",          "Scene_s63_encoding",          "Encoding Categoricals"),
    (64, "s64_scaling",           "Scene_s64_scaling",           "Feature Scaling"),
    (65, "s65_overfit",           "Scene_s65_overfit",           "Overfit/Underfit Curves"),
    (66, "s66_bias_variance",     "Scene_s66_bias_variance",     "Bias-Variance"),
    (67, "s67_bv_curve",          "Scene_s67_bv_curve",          "Bias-Variance Curve"),
    (68, "s68_bv_table",          "Scene_s68_bv_table",          "Bias-Variance Table"),
    (69, "s69_cv_why",            "Scene_s69_cv_why",            "CV Why"),
    (70, "s70_cv_diagram",        "Scene_s70_cv_diagram",        "5-Fold CV Diagram"),
    (71, "s71_cv_pc",             "Scene_s71_cv_pc",             "CV P&C"),
    (72, "s72_pipeline",          "Scene_s72_pipeline",          "Pipeline"),
    (73, "s73_pipeline_pc",       "Scene_s73_pipeline_pc",       "Pipeline P&C"),
    (74, "s74_lr_params",         "Scene_s74_lr_params",         "LR Hyperparams"),
    (75, "s75_ridge_params",      "Scene_s75_ridge_params",      "Ridge Hyperparams"),
    (76, "s76_lasso_params",      "Scene_s76_lasso_params",      "Lasso Hyperparams"),
    (77, "s77_enet_params",       "Scene_s77_enet_params",       "ElasticNet Hyperparams"),
    (78, "s78_when_to_use",       "Scene_s78_when_to_use",       "When to Use Table"),
    (79, "s79_full_pros_cons",    "Scene_s79_full_pros_cons",    "Full Pros & Cons"),
    (80, "s80_interview_qa",      "Scene_s80_interview_qa",      "Interview Q&A"),
    (81, "s81_summary",           "Scene_s81_summary",           "Master Summary"),
    (82, "s82_end",               "Scene_s82_end",               "End Card"),
]


def render_scene(args):
    """
    Worker function: runs one manim command in a subprocess.
    Returns (scene_num, desc, success, elapsed_seconds, error_msg).
    """
    scene_num, method, cls_name, desc, quality_flag, work_dir = args

    filename  = f"scene_{method}.py"
    filepath  = os.path.join(work_dir, filename)

    if not os.path.exists(filepath):
        return (scene_num, desc, False, 0.0,
                f"File not found: {filepath} -- run generate_individual_scenes.py first")

    cmd = ["manim", "-pql", filepath, cls_name]
    t0 = time.time()
    try:
        result = subprocess.run(
            cmd,
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=600,          # 10-minute timeout per scene
        )
        elapsed = time.time() - t0
        if result.returncode == 0:
            return (scene_num, desc, True, elapsed, "")
        else:
            # Grab last 20 lines of stderr for the error summary
            err_lines = (result.stderr or result.stdout or "").strip().split("\n")
            err_summary = "\n".join(err_lines[-20:])
            return (scene_num, desc, False, elapsed, err_summary)
    except subprocess.TimeoutExpired:
        return (scene_num, desc, False, 600.0, "TIMEOUT after 600s")
    except Exception as exc:
        return (scene_num, desc, False, time.time() - t0, str(exc))


def main():
    parser = argparse.ArgumentParser(
        description="Render all 82 linear regression scenes in parallel."
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=None,
        help="Number of parallel workers (default: CPU core count)"
    )
    parser.add_argument(
        "--quality", "-q",
        choices=["l", "m", "h", "k"],
        default="h",
        help="Manim quality: l=480p, m=720p, h=1080p (default), k=4K"
    )
    parser.add_argument(
        "--scenes", "-s",
        type=int,
        nargs="+",
        default=None,
        help="Only render specific scene numbers e.g. --scenes 1 2 53 65"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be rendered without actually running manim"
    )
    args = parser.parse_args()

    # Resolve worker count
    cpu_count  = multiprocessing.cpu_count() or 1
    workers    = args.workers if args.workers else cpu_count
    workers    = max(1, workers)

    quality_flag = f"-q{args.quality}"
    work_dir     = os.path.dirname(os.path.abspath(__file__))

    # Filter scenes if requested
    scenes_to_run = ALL_SCENES
    if args.scenes:
        requested = set(args.scenes)
        scenes_to_run = [s for s in ALL_SCENES if s[0] in requested]
        if not scenes_to_run:
            print(f"ERROR: No scenes matched numbers {args.scenes}")
            sys.exit(1)

    total = len(scenes_to_run)

    # Quality label
    quality_labels = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}
    q_label = quality_labels[args.quality]

    print("=" * 60)
    print(" Linear Regression -- Parallel Scene Renderer")
    print("=" * 60)
    print(f"  Scenes to render : {total}")
    print(f"  Parallel workers : {workers}  (CPU cores: {cpu_count})")
    print(f"  Quality          : {args.quality}  ({q_label})")
    print(f"  Working dir      : {work_dir}")
    print(f"  Estimated speed  : ~{workers}x faster than sequential")
    print("=" * 60)

    if args.dry_run:
        print("\nDRY RUN -- commands that would be executed:")
        for num, method, cls_name, desc, *_ in [
            (n, m, c, d, None, None) for n, m, c, d in scenes_to_run
        ]:
            print(f"  manim {quality_flag} scene_{method}.py {cls_name}")
        print(f"\nTotal: {total} commands")
        return

    # Build job arguments
    jobs = [
        (num, method, cls_name, desc, quality_flag, work_dir)
        for num, method, cls_name, desc in scenes_to_run
    ]

    # Track results
    done       = 0
    passed     = []
    failed     = []
    start_time = time.time()

    print(f"\nStarting render pool with {workers} worker(s)...\n")

    with ProcessPoolExecutor(max_workers=workers) as executor:
        future_map = {executor.submit(render_scene, job): job for job in jobs}

        for future in as_completed(future_map):
            scene_num, desc, success, elapsed, err_msg = future.result()
            done += 1

            if success:
                passed.append((scene_num, desc, elapsed))
                status = "OK "
                print(f"  [{done:2d}/{total}] {status}  S{scene_num:02d} {desc:<36s}  {elapsed:5.1f}s")
            else:
                failed.append((scene_num, desc, err_msg))
                status = "FAIL"
                print(f"  [{done:2d}/{total}] {status}  S{scene_num:02d} {desc:<36s}  FAILED")

    # Summary
    wall_time = time.time() - start_time
    total_render_time = sum(e for _, _, e in passed)

    print()
    print("=" * 60)
    print(f" DONE  |  {len(passed)}/{total} succeeded  |  {len(failed)} failed")
    print(f" Wall time       : {wall_time:.1f}s  ({wall_time/60:.1f} min)")
    print(f" Total CPU time  : {total_render_time:.1f}s  ({total_render_time/60:.1f} min)")
    if wall_time > 0:
        print(f" Parallelism     : {total_render_time / wall_time:.1f}x")
    print("=" * 60)

    if failed:
        print(f"\nFAILED SCENES ({len(failed)}):")
        for num, desc, err in failed:
            print(f"\n  S{num:02d} {desc}")
            # Print last few lines of error
            for line in err.strip().split("\n")[-8:]:
                print(f"    {line}")
        print()
        print("Re-render only the failed scenes:")
        nums = " ".join(str(n) for n, _, _ in failed)
        print(f"  python run_parallel.py --scenes {nums}")
        sys.exit(1)
    else:
        print(f"\nAll {total} scenes rendered successfully.")
        print(f"Output: media/videos/scene_sXX_*/{ q_label }/Scene_sXX_*.mp4")


if __name__ == "__main__":
    # Required for multiprocessing on Windows
    multiprocessing.freeze_support()
    main()
