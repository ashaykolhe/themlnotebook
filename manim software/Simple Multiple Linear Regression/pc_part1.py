"""
pc_part1.py
PC01  Overall Linear Regression pros/cons   (after TextB → before Anim04)
PC02  OLS / Normal Equation pros/cons       (after TextG → before Anim17)
PC03  Gradient Descent pros/cons            (after TextI → before Anim21)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pc_shared import *


# ══════════════════════════════════════════════════════════════════════════════
# PC01 — Overall Linear Regression  (8 pros, 8 cons — show top 5 each)
# ══════════════════════════════════════════════════════════════════════════════
class PC01_OverallLinearRegression(Scene):
    def construct(self):
        pros = [
            "Highly interpretable — coefficients in real units",
            "Blazing fast — closed-form solution O(np²)",
            "No hyperparameters (base OLS) — ready out of the box",
            "Theoretically optimal — BLUE under Gauss-Markov",
            "Statistical inference — p-values and CIs via statsmodels",
            "Great baseline — if it works, you don't need complex models",
            "Memory efficient — stores only p coefficients",
            "Extrapolates — can predict beyond training range (risky)",
        ]
        cons = [
            "Assumes linearity — wrong for non-linear relationships",
            "Sensitive to outliers — squared loss amplifies extremes",
            "Multicollinearity — unstable, uninterpretable coefficients",
            "No automatic interactions — unlike tree models",
            "Struggles when p > n — Normal Equation fails",
            "Scale sensitive — coefficients not comparable unscaled",
            "Strict assumptions — violated → p-values untrustworthy",
            "Not robust — one influential point shifts the whole line",
        ]
        pc_scene(self,
                 "Linear Regression — Pros & Cons",
                 BLUE_D, pros, cons)


# ══════════════════════════════════════════════════════════════════════════════
# PC02 — OLS / Normal Equation  (4 pros, 4 cons)
# ══════════════════════════════════════════════════════════════════════════════
class PC02_OLS(Scene):
    def construct(self):
        pros = [
            "Exact solution in one shot — no iterations",
            "Deterministic — same answer every run",
            "Works well for small datasets (n large, p small)",
            "No convergence criterion needed",
        ]
        cons = [
            "O(p³) — cubically slow with 10,000+ features",
            "Fails if X'X is singular (multicollinearity or p > n)",
            "Memory intensive — must hold X'X (p×p) in RAM",
            "Not suitable for online/streaming learning",
        ]
        pc_scene(self,
                 "Normal Equation / OLS — Pros & Cons",
                 YELLOW_R, pros, cons)


# ══════════════════════════════════════════════════════════════════════════════
# PC03 — Gradient Descent  (5 pros, 5 cons)
# ══════════════════════════════════════════════════════════════════════════════
class PC03_GradientDescent(Scene):
    def construct(self):
        pros = [
            "Scales to millions of rows and thousands of features",
            "Memory efficient — works with mini-batches",
            "Foundation for deep learning — same algorithm in neural nets",
            "Online learning — update model as new data arrives",
            "Extends to non-convex losses easily",
        ]
        cons = [
            "Must choose learning rate α — wrong choice = divergence",
            "Iterative — needs convergence criterion, not exact",
            "Sensitive to feature scaling — must standardise first",
            "Slower than Normal Equation for small datasets",
            "May oscillate without a decaying LR schedule (SGD)",
        ]
        pc_scene(self,
                 "Gradient Descent — Pros & Cons",
                 GREEN_G, pros, cons)
