"""
pc_part4_reg_cv.py
PC16  Ridge Regression          (after TextN → before Anim34)
PC17  Lasso Regression          (after TextO → before Anim35)
PC18  ElasticNet                (after Anim36, before TextQ)
PC19  Cross-Validation          (after Anim39 → before Anim40)
PC20  Pipeline                  (after TextT → before Anim42)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pc_shared import *


# ══════════════════════════════════════════════════════════════════════════════
# PC16 — Ridge Regression (L2)
# ══════════════════════════════════════════════════════════════════════════════
class PC16_Ridge(Scene):
    def construct(self):
        pros = [
            "Handles multicollinearity — distributes weight evenly",
            "Always unique, stable solution (X'X + λI invertible)",
            "Closed-form — still very fast to compute",
            "Keeps all features — good when all features matter",
            "Lower variance than OLS with correlated features",
        ]
        cons = [
            "No feature selection — all coefficients stay non-zero",
            "Coefficients are biased (trades bias for variance)",
            "λ must be tuned via cross-validation",
            "Less interpretable than OLS when λ is large",
        ]
        pc_scene(self, "Ridge (L2) Regression — Pros & Cons",
                 BLUE_D, pros, cons)


# ══════════════════════════════════════════════════════════════════════════════
# PC17 — Lasso Regression (L1)
# ══════════════════════════════════════════════════════════════════════════════
class PC17_Lasso(Scene):
    def construct(self):
        pros = [
            "Built-in feature selection — zero coefficients drop features",
            "Sparse models — interpretable with thousands of features",
            "Good when only a few features truly matter",
            "Useful in genomics, text, high-dimensional data",
        ]
        cons = [
            "No closed form — iterative coordinate descent required",
            "With correlated features: arbitrarily picks one, zeros others",
            "Poor at handling groups of correlated predictors",
            "Too high λ → important features get zeroed out too",
            "Slower than Ridge for large datasets",
        ]
        pc_scene(self, "Lasso (L1) Regression — Pros & Cons",
                 ORANGE_L, pros, cons)


# ══════════════════════════════════════════════════════════════════════════════
# PC18 — ElasticNet (L1 + L2)
# ══════════════════════════════════════════════════════════════════════════════
class PC18_ElasticNet(Scene):
    def construct(self):
        pros = [
            "Best of both worlds — L1 sparsity + L2 stability",
            "Handles groups of correlated features better than Lasso",
            "More robust in high-dimensional settings",
            "Flexible: l1_ratio=0 → Ridge, l1_ratio=1 → Lasso",
        ]
        cons = [
            "Two hyperparameters to tune (alpha + l1_ratio)",
            "No closed form — iterative, slower than Ridge",
            "Interpretation slightly more complex",
            "Often overkill — pick Ridge or Lasso when problem is clear",
        ]
        pc_scene(self, "ElasticNet (L1 + L2) — Pros & Cons",
                 PURPLE, pros, cons)


# ══════════════════════════════════════════════════════════════════════════════
# PC19 — Cross-Validation
# ══════════════════════════════════════════════════════════════════════════════
class PC19_CrossValidation(Scene):
    def construct(self):
        pros = [
            "More reliable estimate — averages out lucky/unlucky splits",
            "Uses all data for both training and testing (efficient)",
            "Detects overfitting — gap between train and CV score",
            "Required for hyperparameter tuning without test leakage",
        ]
        cons = [
            "k× more expensive — fits k models instead of 1",
            "Time-series data: use TimeSeriesSplit instead",
            "Very large datasets: single large holdout may be faster",
        ]
        pc_scene(self, "Cross-Validation — Pros & Cons",
                 GREEN_G, pros, cons)


# ══════════════════════════════════════════════════════════════════════════════
# PC20 — sklearn Pipeline
# ══════════════════════════════════════════════════════════════════════════════
class PC20_Pipeline(Scene):
    def construct(self):
        pros = [
            "Eliminates data leakage by design",
            "One object to fit, transform, and predict — cleaner code",
            "Works seamlessly with GridSearchCV / cross_val_score",
            "Serialise whole workflow with one joblib.dump()",
        ]
        cons = [
            "Slightly harder to debug individual steps",
            "GridSearch param names need 'stepname__param' prefix",
            "Advanced transforms need a custom sklearn transformer",
        ]
        pc_scene(self, "sklearn Pipeline — Pros & Cons",
                 GREEN_G, pros, cons)
