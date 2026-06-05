"""
pc_part2_linemo.py
PC04  L — Linearity             (after Anim22)
PC05  I — Independence          (after Anim23)
PC06  N — Normality             (after TextJ / Anim24)
PC07  E — Equal Variance        (after Anim25)
PC08  M — Multicollinearity     (after Anim26)
PC09  O — No Outliers           (after Anim27)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pc_shared import *


# ══════════════════════════════════════════════════════════════════════════════
# PC04 — L: Linearity
# ══════════════════════════════════════════════════════════════════════════════
class PC04_Linearity(Scene):
    def construct(self):
        pros = [
            "OLS is theoretically optimal (BLUE)",
            "Coefficients are easily interpretable",
            "Extrapolation is reasonable",
        ]
        cons = [
            "Predictions are systematically biased",
            "Residuals show curved patterns — visible in plots",
            "Must add polynomial features or switch models",
        ]
        pc_scene(self,
                 "L — Linearity: When It Holds vs. When Violated",
                 GREEN_G, pros, cons,
                 pro_head="✅  When it holds",
                 con_head="❌  When violated")


# ══════════════════════════════════════════════════════════════════════════════
# PC05 — I: Independence
# ══════════════════════════════════════════════════════════════════════════════
class PC05_Independence(Scene):
    def construct(self):
        pros = [
            "Standard errors are correctly estimated",
            "No systematic patterns in residuals over time",
        ]
        cons = [
            "Standard errors underestimated → inflated t-stats",
            "False significance — p-values are untrustworthy",
            "Model is systematically wrong in structured ways",
        ]
        pc_scene(self,
                 "I — Independence: When It Holds vs. When Violated",
                 BLUE_D, pros, cons,
                 pro_head="✅  When it holds",
                 con_head="❌  When violated (autocorrelation)")


# ══════════════════════════════════════════════════════════════════════════════
# PC06 — N: Normality of Residuals
# ══════════════════════════════════════════════════════════════════════════════
class PC06_Normality(Scene):
    def construct(self):
        pros = [
            "t-tests and F-tests on coefficients exactly valid",
            "Confidence intervals are correctly sized",
            "Small-sample inference is reliable",
        ]
        cons = [
            "p-values and CIs may be inaccurate (small n)",
            "For large n: CLT saves you — predictions still fine",
            "For small n: use bootstrap CIs as alternative",
        ]
        pc_scene(self,
                 "N — Normality of Residuals: When It Holds vs. Violated",
                 PURPLE, pros, cons,
                 pro_head="✅  When it holds",
                 con_head="❌  When violated")


# ══════════════════════════════════════════════════════════════════════════════
# PC07 — E: Equal Variance (Homoscedasticity)
# ══════════════════════════════════════════════════════════════════════════════
class PC07_EqualVariance(Scene):
    def construct(self):
        pros = [
            "OLS is efficient (BLUE — Best Linear Unbiased)",
            "Standard errors, p-values, and CIs are valid",
            "Residual plots are clean and interpretable",
        ]
        cons = [
            "Standard errors biased → bad p-values",
            "Confidence intervals too narrow or too wide",
            "OLS no longer the most efficient estimator",
        ]
        pc_scene(self,
                 "E — Equal Variance: When It Holds vs. Violated",
                 YELLOW_R, pros, cons,
                 pro_head="✅  When it holds (homoscedastic)",
                 con_head="❌  When violated (heteroscedastic)")


# ══════════════════════════════════════════════════════════════════════════════
# PC08 — M: No Multicollinearity
# ══════════════════════════════════════════════════════════════════════════════
class PC08_Multicollinearity(Scene):
    def construct(self):
        pros = [
            "Coefficients are stable and interpretable",
            "Standard errors are small and trustworthy",
            "Can meaningfully compare feature importance",
        ]
        cons = [
            "Coefficients unstable — flip sign with small changes",
            "Standard errors inflate → wide confidence intervals",
            "Coefficients become uninterpretable individually",
            "Normal Equation may become numerically singular",
        ]
        pc_scene(self,
                 "M — Multicollinearity: When Absent vs. Present",
                 ORANGE_L, pros, cons,
                 pro_head="✅  When absent (low VIF)",
                 con_head="❌  When present (high VIF > 10)")


# ══════════════════════════════════════════════════════════════════════════════
# PC09 — O: No Outliers / Leverage Points
# ══════════════════════════════════════════════════════════════════════════════
class PC09_Outliers(Scene):
    def construct(self):
        pros = [
            "Coefficients represent the typical relationship",
            "MSE is a faithful measure of model error",
        ]
        cons = [
            "A single point can dominate the entire regression line",
            "Coefficients may be completely distorted",
            "RMSE is artificially inflated by that one extreme point",
        ]
        pc_scene(self,
                 "O — Outliers: When Absent vs. When Influential",
                 RED_B, pros, cons,
                 pro_head="✅  When outliers are absent",
                 con_head="❌  When influential outliers present")
