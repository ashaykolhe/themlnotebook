"""
text_part10_outro.py
TEXT-S  Data leakage forms              (between Anim40 → Anim41)
TEXT-T  Pipeline benefits               (between Anim41 → Anim42)
TEXT-U  9-step production workflow      (between Anim43 → Anim44)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared import *


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-S — Data Leakage Forms  (BulletReveal, warning style)
# ══════════════════════════════════════════════════════════════════════════════
class TextS_LeakageForms(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("/!\ Data Leakage Is Bigger Than Just Scaling",
                     font_size=23, color=RED_B).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Main warning card
        warn_bg = RoundedRectangle(
            corner_radius=0.13, width=11.5, height=0.72,
            fill_color="#1a0a0a", fill_opacity=1.0,
            stroke_color=RED_B, stroke_width=2.2,
        ).move_to(UP * 1.4)
        warn_txt = Text(
            "Leakage = model secretly learns from test data → unrealistically good metrics",
            font_size=17, color=RED_B
        ).move_to(warn_bg.get_center())
        self.play(FadeIn(warn_bg), FadeIn(warn_txt), run_time=0.5)

        leakage_forms = [
            (RED_B,    "StandardScaler.fit() on full dataset before split",
             "→ scaler knows test set mean and std"),
            (ORANGE_L, "Target encoding computed on full data",
             "→ target statistics leak from test rows"),
            (YELLOW_R, "Feature selection using all rows before split",
             "→ selected features 'know' test patterns"),
            (ORANGE_L, "Imputing missing values with full-dataset mean",
             "→ test set influences imputed values"),
        ]

        y_pos = 0.6
        for color, form, consequence in leakage_forms:
            form_mob = Text(form,        font_size=16, color=color, weight=BOLD)
            cons_mob = Text(consequence, font_size=15, color=MUTED)
            row = VGroup(
                Text("✗", font_size=16, color=color),
                VGroup(form_mob, cons_mob).arrange(DOWN, buff=0.06,
                                                    aligned_edge=LEFT)
            ).arrange(RIGHT, buff=0.2).move_to(UP * y_pos)\
             .align_to(LEFT * 5.5, LEFT)
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.48)
            self.wait(0.95)
            y_pos -= 0.88

        fix = Text(
            "The single fix for ALL of these:  sklearn Pipeline  +  fit only on X_train",
            font_size=17, color=GREEN_G
        ).to_edge(DOWN, buff=0.35)
        self.play(Write(fix), run_time=0.7)
        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-T — Why Pipeline Is Not Optional  (BulletReveal, green positive)
# ══════════════════════════════════════════════════════════════════════════════
class TextT_PipelineBenefits(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("sklearn Pipeline — Four Reasons It Is Mandatory",
                     font_size=24, color=GREEN_G).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        benefits = [
            (GREEN_G,  "Prevents leakage by design",
             "Scaler.fit() sees only X_train.  Scaler.transform() uses train stats on X_test."),
            (BLUE_D,   "One object to fit, transform, and predict",
             "pipeline.fit(X_train)  then  pipeline.predict(X_test) — clean, readable code."),
            (ORANGE_L, "Seamless with GridSearchCV and cross_val_score",
             "Hyperparameter search is automatically applied inside each CV fold correctly."),
            (PURPLE,   "Serialise the entire workflow with one line",
             "joblib.dump(pipeline, 'model.pkl') — scaler + model saved together for production."),
        ]

        y_pos = 1.55
        for color, heading, detail in benefits:
            bg = RoundedRectangle(
                corner_radius=0.11, width=11.5, height=1.15,
                fill_color=SURFACE, fill_opacity=1.0,
                stroke_color=color, stroke_width=1.8,
            ).move_to(UP * y_pos)
            # Align both texts to a fixed left margin inside the card
            left_margin = RIGHT * 0.3
            head_mob = Text(heading, font_size=17, color=color, weight=BOLD)\
                .next_to(bg.get_top(), DOWN, buff=0.2)\
                .align_to(bg, LEFT).shift(left_margin)
            detail_mob = Text(detail, font_size=15, color=MUTED)\
                .next_to(head_mob, DOWN, buff=0.1)\
                .align_to(bg, LEFT).shift(left_margin)

            self.play(FadeIn(bg), run_time=0.3)
            self.play(Write(head_mob), FadeIn(detail_mob), run_time=0.5)
            self.wait(0.7)
            y_pos -= 1.3

        self.wait(1.2)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-U — 9-Step Production Workflow  (BulletReveal, numbered, fast paced)
# ══════════════════════════════════════════════════════════════════════════════
class TextU_ProductionWorkflow(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Building a Production-Ready Linear Regression Model",
                     font_size=22, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        steps = [
            (BLUE_D,   "1. EDA",
             "Distributions, correlations, missing\nvalues, outlier detection, target shape"),
            (BLUE_D,   "2. Preprocessing",
             "Impute → encode → log-transform\n→ StandardScaler → Pipeline"),
            (GREEN_G,  "3. Baseline",
             "Fit OLS. Get 5-fold CV: R², RMSE, MAE"),
            (YELLOW_R, "4. Diagnostics",
             "Residuals vs Fitted, Q-Q, Scale-Loc,\nCook's Distance"),
            (ORANGE_L, "5. Fix violations",
             "Transform features/target, remove\nor combine collinear features"),
            (ORANGE_L, "6. Regularise",
             "RidgeCV, LassoCV, ElasticNetCV.\nCompare 5-fold CV performance"),
            (PURPLE,   "7. Interpret",
             "Standardised coefficients, CIs\nvia statsmodels"),
            (GREEN_G,  "8. Final evaluation",
             "Test set EXACTLY ONCE.\nReport RMSE, MAE, R²"),
            (MUTED,    "9. Deploy",
             "joblib.dump(pipeline). Monitor\ndata drift post-launch"),
        ]

        # Two-column layout to fit 9 steps without crowding
        col_left  = steps[:5]
        col_right = steps[5:]

        y_start = 1.5
        row_gap = 0.72

        # Left column
        for i, (color, step, detail) in enumerate(col_left):
            step_mob   = Text(step,   font_size=15, color=color, weight=BOLD)
            detail_mob = Text(detail, font_size=13, color=MUTED)
            row = VGroup(step_mob, detail_mob).arrange(DOWN, buff=0.05,
                                                        aligned_edge=LEFT)\
                .move_to(LEFT * 3.3 + UP * (y_start - i * row_gap))\
                .align_to(LEFT * 6.3, LEFT)
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.38)
            self.wait(0.65)

        # Right column (starts at same y as left, offset right)
        for i, (color, step, detail) in enumerate(col_right):
            step_mob   = Text(step,   font_size=15, color=color, weight=BOLD)
            detail_mob = Text(detail, font_size=13, color=MUTED)
            row = VGroup(step_mob, detail_mob).arrange(DOWN, buff=0.05,
                                                        aligned_edge=LEFT)\
                .move_to(RIGHT * 3.0 + UP * (y_start - i * row_gap))\
                .align_to(RIGHT * 6.3 - RIGHT * 6.6, LEFT)
            self.play(FadeIn(row, shift=LEFT * 0.2), run_time=0.38)
            self.wait(0.65)

        # Final takeaway bar
        bar_bg = RoundedRectangle(
            corner_radius=0.12, width=11.5, height=0.62,
            fill_color=SURFACE, fill_opacity=1.0,
            stroke_color=GREEN_G, stroke_width=2.0,
        ).to_edge(DOWN, buff=0.28)
        bar_txt = Text(
            "Follow this order every single time — skipping steps is how models fail silently in production.",
            font_size=15, color=GREEN_G
        ).move_to(bar_bg.get_center())
        self.play(FadeIn(bar_bg), FadeIn(bar_txt), run_time=0.5)
        self.wait(2.0)
