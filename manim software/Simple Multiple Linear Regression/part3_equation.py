from manim import *
import numpy as np

BLUE_D   = "#4f9eff"
ORANGE_L = "#f97316"
YELLOW_R = "#fbbf24"
GREEN_G  = "#10b981"
RED_B    = "#f87171"
PURPLE   = "#a855f7"
BG       = "#0d0f14"
MUTED    = "#8892a4"
HEADING  = "#f8fafc"


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 08 — ŷ highlights in blue  (full equation on screen, ŷ glows)
# ══════════════════════════════════════════════════════════════════════════════
class Anim08_YHatHighlight(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Full equation as individual coloured terms
        eq = MathTex(
            r"\hat{y}", r"=",
            r"\beta_0", r"+",
            r"\beta_1 x_1", r"+",
            r"\beta_2 x_2", r"+",
            r"\cdots", r"+",
            r"\beta_n x_n",
            font_size=54
        ).set_color(MUTED).move_to(UP * 0.5)

        # Start dim, appear all at once
        self.play(FadeIn(eq), run_time=0.7)
        self.wait(0.3)

        # Highlight ŷ in blue
        self.play(eq[0].animate.set_color(BLUE_D).scale(1.25), run_time=0.5)

        ann = VGroup(
            Text("y-hat", font_size=22, color=BLUE_D),
            Text("The model's prediction.\nNot the truth — our best guess.", font_size=19, color=MUTED)
        ).arrange(DOWN, buff=0.15).next_to(eq[0], DOWN, buff=1.0)
        arr = Arrow(ann.get_top(), eq[0].get_bottom(),
                    buff=0.1, color=BLUE_D, stroke_width=2,
                    max_tip_length_to_length_ratio=0.2)

        self.play(FadeIn(ann, shift=DOWN * 0.2), GrowArrow(arr), run_time=0.8)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 09 — β₀ highlights in orange
# ══════════════════════════════════════════════════════════════════════════════
class Anim09_Beta0Highlight(Scene):
    def construct(self):
        self.camera.background_color = BG

        eq = MathTex(
            r"\hat{y}", r"=",
            r"\beta_0", r"+",
            r"\beta_1 x_1", r"+",
            r"\beta_2 x_2", r"+",
            r"\cdots", r"+",
            r"\beta_n x_n",
            font_size=54
        ).move_to(UP * 0.5)
        eq[0].set_color(BLUE_D)
        eq[2].set_color(MUTED)
        self.add(eq)

        # Highlight β₀
        self.play(eq[2].animate.set_color(ORANGE_L).scale(1.25), run_time=0.5)

        ann = VGroup(
            Text("Intercept  (β₀)", font_size=22, color=ORANGE_L),
            Text("Where the line crosses the y-axis.\nPredicted value when all features = 0.",
                 font_size=19, color=MUTED)
        ).arrange(DOWN, buff=0.15).next_to(eq[2], DOWN, buff=1.0)
        arr = Arrow(ann.get_top(), eq[2].get_bottom(),
                    buff=0.1, color=ORANGE_L, stroke_width=2,
                    max_tip_length_to_length_ratio=0.2)

        self.play(FadeIn(ann, shift=DOWN * 0.2), GrowArrow(arr), run_time=0.8)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 10 — β₁, β₂ highlight in green one by one
# ══════════════════════════════════════════════════════════════════════════════
class Anim10_CoeffHighlight(Scene):
    def construct(self):
        self.camera.background_color = BG

        eq = MathTex(
            r"\hat{y}", r"=",
            r"\beta_0", r"+",
            r"\beta_1 x_1", r"+",
            r"\beta_2 x_2", r"+",
            r"\cdots", r"+",
            r"\beta_n x_n",
            font_size=54
        ).move_to(UP * 0.5)
        eq[0].set_color(BLUE_D)
        eq[2].set_color(ORANGE_L)
        self.add(eq)

        # β₁x₁
        self.play(eq[4].animate.set_color(GREEN_G).scale(1.2), run_time=0.5)
        ann1 = Text("β₁  =  change in ŷ per 1-unit rise in x₁\n(all other features fixed)",
                    font_size=19, color=GREEN_G).next_to(eq, DOWN, buff=0.9)
        self.play(FadeIn(ann1, shift=DOWN * 0.15), run_time=0.7)
        self.wait(1.0)

        # β₂x₂
        self.play(eq[6].animate.set_color(GREEN_G).scale(1.2), run_time=0.5)
        ann2 = Text("β₂  =  same idea for x₂,  same logic for all βs",
                    font_size=19, color=GREEN_G).next_to(ann1, DOWN, buff=0.3)
        self.play(FadeIn(ann2, shift=DOWN * 0.15), run_time=0.7)
        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 11 — Example annotation: β₁ = 150 → price interpretation
# ══════════════════════════════════════════════════════════════════════════════
class Anim11_Beta1Example(Scene):
    def construct(self):
        self.camera.background_color = BG

        eq = MathTex(
            r"\hat{y}", r"=",
            r"\beta_0", r"+",
            r"\beta_1 x_1", r"+",
            r"\cdots",
            font_size=56
        ).move_to(UP * 1.5)
        eq[0].set_color(BLUE_D)
        eq[2].set_color(ORANGE_L)
        eq[4].set_color(GREEN_G)
        self.add(eq)

        # Concrete substitution
        substituted = MathTex(
            r"\hat{\text{price}}", r"=",
            r"\beta_0", r"+",
            r"150 \times \text{sqft}", r"+",
            r"\cdots",
            font_size=48
        ).next_to(eq, DOWN, buff=0.6)
        substituted[0].set_color(BLUE_D)
        substituted[2].set_color(ORANGE_L)
        substituted[4].set_color(GREEN_G)

        self.play(Write(substituted), run_time=1.1)

        box = SurroundingRectangle(substituted[4], color=GREEN_G,
                                   corner_radius=0.1, buff=0.1, stroke_width=2)
        self.play(Create(box), run_time=0.5)

        explanation = Text(
            'β₁ = 150  →  "Each extra sq ft adds ₹150 to predicted price\n'
            '              (holding all other features constant)"',
            font_size=20, color=GREEN_G
        ).next_to(substituted, DOWN, buff=0.65)
        self.play(Write(explanation), run_time=1.2)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 12 — Zoom out: full equation reappears + ε error term added below
# ══════════════════════════════════════════════════════════════════════════════
class Anim12_FullEquationAndEpsilon(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("The Complete Model", font_size=28, color=HEADING)\
            .to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)

        # Prediction equation
        eq_pred = MathTex(
            r"\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_n x_n",
            font_size=48, color=HEADING
        ).move_to(UP * 0.9)
        self.play(FadeIn(eq_pred, scale=0.85), run_time=0.9)
        self.wait(0.5)

        # True model with ε
        sep = DashedLine(LEFT * 5.5, RIGHT * 5.5, color="#2d3748",
                         stroke_width=1.2).next_to(eq_pred, DOWN, buff=0.55)
        self.play(Create(sep), run_time=0.4)

        eq_true = MathTex(
            r"y = \beta_0 + \beta_1 x_1 + \cdots + \beta_n x_n + ",
            r"\varepsilon",
            font_size=48
        ).next_to(sep, DOWN, buff=0.45)
        eq_true[0].set_color(HEADING)
        eq_true[1].set_color(YELLOW_R)

        self.play(Write(eq_true), run_time=1.1)

        eps_box = SurroundingRectangle(eq_true[1], color=YELLOW_R,
                                       corner_radius=0.1, buff=0.12)
        eps_ann = VGroup(
            Text("ε  (epsilon)", font_size=20, color=YELLOW_R),
            Text("Everything the model can't explain:\nnoise, missing variables, measurement error.",
                 font_size=17, color=MUTED)
        ).arrange(DOWN, buff=0.15).next_to(eq_true, DOWN, buff=0.6)
        eps_arr = Arrow(eps_ann.get_top(), eq_true[1].get_bottom(),
                        buff=0.1, color=YELLOW_R, stroke_width=2,
                        max_tip_length_to_length_ratio=0.2)

        self.play(Create(eps_box), run_time=0.4)
        self.play(FadeIn(eps_ann, shift=DOWN * 0.2), GrowArrow(eps_arr), run_time=0.8)
        self.wait(2.0)
