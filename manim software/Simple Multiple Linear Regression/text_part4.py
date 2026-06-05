"""
text_part4.py
TEXT-F  Why square errors — 4 reasons          (between Anim14 → Anim15)
TEXT-G  Normal Equation 6-step derivation      (between Anim16 → Anim17)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared import *


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-F — Why Square the Errors  (BulletReveal, 4 bullets)
# ══════════════════════════════════════════════════════════════════════════════
class TextF_WhySquareErrors(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Why Square the Errors and Not Just Sum Them?",
                     font_size=24, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        bullets = [
            (RED_B,    "1.",
             "Raw errors cancel out — positive and negative offset each other perfectly"),
            (YELLOW_R, "2.",
             "Squaring makes every error positive — they can no longer cancel"),
            (ORANGE_L, "3.",
             "Squaring penalises LARGE errors far more than small ones (2² = 4, 10² = 100)"),
            (GREEN_G,  "4.",
             "The squared function is differentiable everywhere — essential for calculus"),
        ]

        # MSE formula appears first for context
        mse = MathTex(
            r"\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2",
            font_size=40, color=BLUE_D
        ).move_to(UP * 1.3)
        self.play(Write(mse), run_time=0.8)
        self.wait(0.3)

        # Build all rows first, find widest, then pin all to same left edge
        rows = []
        for color, num, text in bullets:
            num_mob  = Text(num,  font_size=20, color=color, weight=BOLD)
            text_mob = Text(text, font_size=19, color=BODY)
            row = VGroup(num_mob, text_mob).arrange(RIGHT, buff=0.25)
            rows.append(row)

        left_anchor = -max(r.width for r in rows) / 2

        for i, row in enumerate(rows):
            row.move_to(UP * (0.25 - i * 0.78))
            row.align_to([left_anchor, 0, 0], LEFT)
            self.play(FadeIn(row, shift=RIGHT * 0.35), run_time=0.5)
            self.wait(1.2)

        self.wait(1.0)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-G — Normal Equation 6-Step Derivation  (BulletReveal, numbered math)
# ══════════════════════════════════════════════════════════════════════════════
class TextG_NormalEquationDerivation(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Title uses VGroup(Text + MathTex + Text) — formula rendered via LaTeX
        title = VGroup(
            Text("Deriving  β = ", font_size=23, color=HEADING),
            MathTex(r"(X^\top X)^{-1} X^\top y", font_size=28, color=YELLOW_R),
            Text("  — Step by Step", font_size=23, color=HEADING),
        ).arrange(RIGHT, buff=0.1).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        steps = [
            (MUTED,    "1. Write cost:",
             r"J = \frac{1}{n}(y - X\beta)^\top(y - X\beta)"),
            (MUTED,    "2. Expand:",
             r"J = \frac{1}{n}\bigl(y^\top y - 2\beta^\top X^\top y + \beta^\top X^\top X\beta\bigr)"),
            (YELLOW_R, "3. Differentiate w.r.t. β:",
             r"\frac{\partial J}{\partial \beta} = \frac{1}{n}\bigl(-2X^\top y + 2X^\top X\beta\bigr)"),
            (YELLOW_R, "4. Set to zero:",
             r"-2X^\top y + 2X^\top X\beta = 0"),
            (ORANGE_L, "5. Rearrange:",
             r"X^\top X\,\beta = X^\top y \quad \text{(the normal equations)}"),
            (GREEN_G,  "6. Solve  ✓",
             r"\beta = (X^\top X)^{-1} X^\top y"),
        ]

        y_pos = 1.7
        spacing = 0.72

        for i, (color, label, formula) in enumerate(steps):
            label_mob = Text(label, font_size=16, color=color, weight=BOLD)
            eq_mob    = MathTex(formula, font_size=26, color=BODY)
            row = VGroup(label_mob, eq_mob).arrange(RIGHT, buff=0.3)
            row.move_to(UP * (y_pos - i * spacing))

            self.play(FadeIn(row, shift=RIGHT * 0.25), run_time=0.45)
            self.wait(1.2)

        # Highlight the final answer
        final_box = SurroundingRectangle(
            self.mobjects[-1], color=GREEN_G,
            corner_radius=0.1, buff=0.1, stroke_width=2
        )
        self.play(Create(final_box), run_time=0.5)
        self.wait(1.5)
