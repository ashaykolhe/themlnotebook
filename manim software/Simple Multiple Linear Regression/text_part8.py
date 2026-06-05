"""
text_part8.py
TEXT-N  Ridge key facts              (between Anim33 → Anim34)
TEXT-O  Lasso key facts              (between Anim34 → Anim35)
TEXT-P  L1 sparsity explanation      (between Anim35 → Anim36)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared import *


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-N — Ridge Regression Key Facts  (BulletReveal, 4 bullets)
# ══════════════════════════════════════════════════════════════════════════════
class TextN_RidgeKeyFacts(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Ridge Regression (L2) — What It Does",
                     font_size=26, color=BLUE_D).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Cost formula
        cost = MathTex(
            r"\text{Cost}_\text{Ridge} = \underbrace{\frac{1}{n}\sum(y_i-\hat{y}_i)^2}_\text{MSE}"
            r"+ \underbrace{\lambda\sum_j\beta_j^2}_\text{L2 penalty}",
            font_size=36, color=HEADING
        ).move_to(UP * 1.5)
        self.play(Write(cost), run_time=1.0)

        # Closed-form highlight
        cf = MathTex(
            r"\hat{\beta}_\text{Ridge} = (X^\top X + \lambda I)^{-1} X^\top y",
            font_size=32, color=BLUE_D
        ).next_to(cost, DOWN, buff=0.35)
        cf_note = Text("Always invertible — even with multicollinearity",
                       font_size=16, color=MUTED).next_to(cf, DOWN, buff=0.12)
        self.play(Write(cf), FadeIn(cf_note), run_time=0.8)

        sep = Line(LEFT * 6, RIGHT * 6, color=BORDER, stroke_width=1)\
            .next_to(cf_note, DOWN, buff=0.25)
        self.play(Create(sep), run_time=0.3)

        bullets = [
            (BLUE_D,   "λ = 0  →  plain OLS.    λ → ∞  →  all β → 0"),
            (GREEN_G,  "Distributes weight across correlated features — doesn't pick one"),
            (YELLOW_R, "Never produces exact zeros — all features stay in the model"),
            (ORANGE_L, "Lower variance than OLS when features are correlated"),
        ]
        y_pos = -0.85
        for color, text in bullets:
            row = VGroup(
                Text("●", font_size=17, color=color),
                Text(text, font_size=18, color=BODY)
            ).arrange(RIGHT, buff=0.22).move_to(UP * y_pos).align_to(LEFT * 5.8, LEFT)
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.45)
            self.wait(0.9)
            y_pos -= 0.72

        self.wait(1.0)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-O — Lasso Regression Key Facts  (BulletReveal, 4 bullets)
# ══════════════════════════════════════════════════════════════════════════════
class TextO_LassoKeyFacts(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Lasso Regression (L1) — What It Does Differently",
                     font_size=24, color=ORANGE_L).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Cost formula
        cost = MathTex(
            r"\text{Cost}_\text{Lasso} = \underbrace{\frac{1}{n}\sum(y_i-\hat{y}_i)^2}_\text{MSE}"
            r"+ \underbrace{\lambda\sum_j|\beta_j|}_\text{L1 penalty}",
            font_size=36, color=HEADING
        ).move_to(UP * 1.5)
        self.play(Write(cost), run_time=1.0)

        # Key contrast with Ridge
        contrast = Text(
            "L1 uses |β| (absolute value), NOT β²  →  this tiny change has a huge consequence",
            font_size=17, color=YELLOW_R
        ).next_to(cost, DOWN, buff=0.3)
        self.play(FadeIn(contrast), run_time=0.6)

        sep = Line(LEFT * 6, RIGHT * 6, color=BORDER, stroke_width=1)\
            .next_to(contrast, DOWN, buff=0.22)
        self.play(Create(sep), run_time=0.3)

        bullets = [
            (GREEN_G,  "Can drive β exactly to ZERO → automatic feature selection"),
            (GREEN_G,  "Sparse models — great for thousands of features (genomics, text)"),
            (RED_B,    "No closed form — requires iterative coordinate descent (slower)"),
            (RED_B,    "With correlated features: picks one arbitrarily, zeros the rest — unstable"),
        ]
        y_pos = -0.85
        for color, text in bullets:
            row = VGroup(
                Text("●", font_size=17, color=color),
                Text(text, font_size=18, color=BODY)
            ).arrange(RIGHT, buff=0.22).move_to(UP * y_pos).align_to(LEFT * 5.8, LEFT)
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.45)
            self.wait(0.95)
            y_pos -= 0.72

        self.wait(1.0)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-P — Why L1 Creates Sparsity But L2 Doesn't  (SplitReveal)
# ══════════════════════════════════════════════════════════════════════════════
class TextP_L1SparsityExplained(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Why Does L1 Create Sparsity But L2 Doesn't?",
                     font_size=24, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Divider
        div = Line(UP * 2.5, DOWN * 3.3, color=BORDER, stroke_width=1.5)
        self.play(Create(div), run_time=0.35)

        # Panel headers
        geo_head = Text("GEOMETRIC ANSWER", font_size=18, color=BLUE_D, weight=BOLD)\
            .move_to(LEFT * 3.3 + UP * 2.0)
        calc_head = Text("CALCULUS ANSWER", font_size=18, color=ORANGE_L, weight=BOLD)\
            .move_to(RIGHT * 3.3 + UP * 2.0)
        self.play(Write(geo_head), Write(calc_head), run_time=0.6)

        # Geometric panel
        geo_points = [
            (BLUE_D,   "L2 constraint = CIRCLE  (smooth, no corners)"),
            (BLUE_D,   "MSE ellipse hits the circle at a smooth off-axis point"),
            (GREEN_G,  "→ both β₁ and β₂ are non-zero"),
        ]
        # Calculus panel — each bullet is ONE line so arrow aligns correctly
        # βj written as "2β" or "sign(β)" — j index is implicit in context
        calc_points = [
            (ORANGE_L, "L2 penalty derivative  =  2β"),
            (ORANGE_L, "Shrinks proportionally → approaches 0, never reaches it"),
            (GREEN_G,  "L1 penalty derivative  =  sign(β)"),
            (GREEN_G,  "Constant push → can reach exactly 0 → feature removed"),
        ]

        def make_bullet(color, text, x_centre, y, direction):
            arrow = Text("→", font_size=16, color=color)
            body  = Text(text, font_size=15, color=BODY)
            row   = VGroup(arrow, body).arrange(RIGHT, buff=0.15, aligned_edge=UP)
            row.move_to([x_centre, y, 0])
            row.align_to([x_centre - 2.8, 0, 0], LEFT)
            return row

        # Animate geo bullets on left
        y_geo = 1.1
        for color, text in geo_points:
            row = make_bullet(color, text, -3.3, y_geo, RIGHT)
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.4)
            self.wait(0.7)
            y_geo -= 0.72

        # Animate calc bullets on right
        y_calc = 1.1
        for color, text in calc_points:
            row = make_bullet(color, text, 3.3, y_calc, LEFT)
            self.play(FadeIn(row, shift=LEFT * 0.15), run_time=0.4)
            self.wait(0.7)
            y_calc -= 0.72

        # L1 diamond + corner visual reminder
        diamond_lbl = Text("L1 constraint = DIAMOND  (corners on axes!)",
                           font_size=15, color=ORANGE_L)\
            .move_to(LEFT * 3.3 + DOWN * 1.1)
        corner_lbl = Text("MSE ellipse hits CORNER → β = exactly 0",
                          font_size=15, color=GREEN_G)\
            .next_to(diamond_lbl, DOWN, buff=0.18)
        self.play(FadeIn(diamond_lbl), FadeIn(corner_lbl), run_time=0.5)

        # Summary bar
        summary_bg = RoundedRectangle(
            corner_radius=0.12, width=11.5, height=0.65,
            fill_color=SURFACE, fill_opacity=1.0,
            stroke_color=GREEN_G, stroke_width=1.8,
        ).to_edge(DOWN, buff=0.28)
        summary_txt = Text(
            "L2 (Ridge): smooth penalty → shrinks → never zero.   "
            "L1 (Lasso): non-smooth at 0 → constant push → exact zero.",
            font_size=15, color=GREEN_G
        ).move_to(summary_bg.get_center())
        self.play(FadeIn(summary_bg), FadeIn(summary_txt), run_time=0.5)
        self.wait(2.0)
