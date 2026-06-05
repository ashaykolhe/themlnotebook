"""
pc_part3_metrics.py
PC10  MSE metric                (paired with metric cards in Anim29)
PC11  RMSE metric               (paired with metric cards in Anim29)
PC12  MAE metric                (paired with metric cards in Anim29)
PC13  R² metric                 (after TextL, before Anim31)
PC14  Adjusted R²               (after Anim31, before Anim32)
PC15  MAPE metric               (after PC12, before TextL)

Note: PC10/11/12 are shown as a combined 3-metric scene to avoid
5 separate metric scenes slowing the video pace. PC13/14/15 are
separate because they appear at different points in the video.
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pc_shared import *


# ══════════════════════════════════════════════════════════════════════════════
# PC10 — MSE: Mean Squared Error
# ══════════════════════════════════════════════════════════════════════════════
class PC10_MSE(Scene):
    def construct(self):
        pros = [
            "Differentiable everywhere — clean for gradient optimisation",
            "Penalises large errors more — good when big mistakes costly",
            "Convex — unique global minimum guaranteed",
        ]
        cons = [
            "Units are squared (dollars²) — not directly interpretable",
            "Very sensitive to outliers — one extreme error dominates",
            "Two different error distributions can give the same MSE",
        ]
        pc_scene(self, "MSE — Mean Squared Error: Pros & Cons",
                 MUTED, pros, cons)


# ══════════════════════════════════════════════════════════════════════════════
# PC11 — RMSE: Root Mean Squared Error
# ══════════════════════════════════════════════════════════════════════════════
class PC11_RMSE(Scene):
    def construct(self):
        pros = [
            "Same units as y — directly interpretable",
            "Still penalises large errors (inherited from MSE)",
            "Most widely used metric in regression competitions",
        ]
        cons = [
            "Still sensitive to outliers (inherited from MSE)",
            "Not scale-invariant — can't compare across target scales",
        ]
        pc_scene(self, "RMSE — Root Mean Squared Error: Pros & Cons",
                 ORANGE_L, pros, cons)


# ══════════════════════════════════════════════════════════════════════════════
# PC12 — MAE: Mean Absolute Error
# ══════════════════════════════════════════════════════════════════════════════
class PC12_MAE(Scene):
    def construct(self):
        pros = [
            "Robust to outliers — extreme errors don't dominate",
            "Same units as y — easy to explain to stakeholders",
            "More interpretable average error than RMSE",
        ]
        cons = [
            "Not differentiable at 0 — subgradient needed",
            "Treats all errors equally — may underweight large errors",
            "Less clean than MSE for theoretical derivations",
        ]
        pc_scene(self, "MAE — Mean Absolute Error: Pros & Cons",
                 BLUE_D, pros, cons)


# ══════════════════════════════════════════════════════════════════════════════
# PC13 — R²: Coefficient of Determination
# ══════════════════════════════════════════════════════════════════════════════
class PC13_R2(Scene):
    def construct(self):
        pros = [
            "Scale-independent — 0–1 range comparable across datasets",
            'Intuitive: "model explains X% of variance in y"',
            "Widely understood — great for stakeholder reporting",
        ]
        cons = [
            "Always increases with more features — even random noise",
            "Says nothing about assumption violations",
            "High R² on log(y) doesn't translate directly to raw y",
            "Can be negative on test set — model worse than predicting ȳ",
        ]
        pc_scene(self, "R² — Coefficient of Determination: Pros & Cons",
                 GREEN_G, pros, cons)


# ══════════════════════════════════════════════════════════════════════════════
# PC14 — Adjusted R²
# ══════════════════════════════════════════════════════════════════════════════
class PC14_AdjR2(Scene):
    def construct(self):
        pros = [
            "Penalises model complexity — prevents feature inflation",
            "Better for comparing models with different feature counts",
            "Decreases when useless features are added",
        ]
        cons = [
            "Still doesn't check assumption validity",
            "Doesn't measure predictive accuracy like CV does",
            "Can still be gamed by tuning heavily on training data",
        ]
        pc_scene(self, "Adjusted R² — The Honest R²: Pros & Cons",
                 PURPLE, pros, cons)


# ══════════════════════════════════════════════════════════════════════════════
# PC15 — MAPE: Mean Absolute Percentage Error
# ══════════════════════════════════════════════════════════════════════════════
class PC15_MAPE(Scene):
    def construct(self):
        pros = [
            "Percentage-based — easily communicated to any team",
            "Scale-independent — compare across different products",
            'Intuitive: "MAPE = 5%" is immediately meaningful',
        ]
        cons = [
            None,   # placeholder — built manually below using MathTex
            "Asymmetric — over/under predictions penalised differently",
            "Heavily penalises underestimates when y is small",
            "Not suitable for targets near zero",
        ]

        # Use pc_scene for everything except the first con which needs MathTex
        # We build the scene manually here to inject the MathTex bullet

        self.camera.background_color = BG
        from pc_shared import _wrap, _line_count, BULLET_FS, ROW_GAP_1, ROW_GAP_2

        title = Text("MAPE — Mean Abs. Percentage Error: Pros & Cons",
                     font_size=23, color=YELLOW_R, weight=BOLD).to_edge(UP, buff=0.28)
        self.play(Write(title), run_time=0.55)

        div = Line(UP * 2.65, DOWN * 3.5, color=BORDER, stroke_width=1.5)
        self.play(Create(div), run_time=0.28)

        pro_h = Text("✅  Pros", font_size=18, color=PRO_COL, weight=BOLD)\
            .move_to(LEFT * 3.2 + UP * 2.15)
        con_h = Text("❌  Cons", font_size=18, color=CON_COL, weight=BOLD)\
            .move_to(RIGHT * 3.2 + UP * 2.15)
        self.play(Write(pro_h), Write(con_h), run_time=0.45)

        # Build cons rows — first one uses MathTex inline
        def make_yi_bullet():
            """Bullet with proper y_i subscript via MathTex."""
            dot   = Text("●", font_size=14, color=CON_COL)
            part1 = Text("Undefined when ", font_size=BULLET_FS, color=BODY)
            yi    = MathTex(r"y_i", font_size=17, color=BODY)
            part2 = Text(" = 0 — division by zero", font_size=BULLET_FS, color=BODY)
            body  = VGroup(part1, yi, part2)\
                .arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
            row   = VGroup(dot, body)\
                .arrange(RIGHT, buff=0.18, aligned_edge=UP)
            return row

        cons_rows = [make_yi_bullet()]
        for txt in cons[1:]:
            dot  = Text("●", font_size=14, color=CON_COL)
            body = Text(_wrap(txt), font_size=BULLET_FS, color=BODY, line_spacing=1.25)
            cons_rows.append(VGroup(dot, body).arrange(RIGHT, buff=0.18, aligned_edge=UP))

        pro_texts = pros
        n = max(len(pro_texts), len(cons_rows))
        row_heights = []
        for i in range(n):
            p_lines = _line_count(pro_texts[i]) if i < len(pro_texts) else 1
            c_lines = cons_rows[i].height / 0.145 if i < len(cons_rows) else 1
            max_lines = max(p_lines, 2 if c_lines > 1.5 else 1)
            row_heights.append(ROW_GAP_2 if max_lines >= 2 else ROW_GAP_1)

        y = 1.52
        y_positions = []
        for h in row_heights:
            y_positions.append(y)
            y -= h

        left_x_pro = -3.2 - 2.85
        left_x_con =  3.2 - 2.85

        for i in range(n):
            anims = []
            if i < len(pro_texts):
                dot  = Text("●", font_size=14, color=PRO_COL)
                body = Text(_wrap(pro_texts[i]), font_size=BULLET_FS,
                            color=BODY, line_spacing=1.25)
                p_row = VGroup(dot, body).arrange(RIGHT, buff=0.18, aligned_edge=UP)
                p_row.move_to([-3.2, y_positions[i], 0])
                p_row.align_to([left_x_pro, 0, 0], LEFT)
                anims.append(FadeIn(p_row, shift=RIGHT * 0.22))
            if i < len(cons_rows):
                c_row = cons_rows[i]
                c_row.move_to([3.2, y_positions[i], 0])
                c_row.align_to([left_x_con, 0, 0], LEFT)
                anims.append(FadeIn(c_row, shift=LEFT * 0.22))
            self.play(*anims, run_time=0.40)
            self.wait(0.80)

        self.wait(1.2)
