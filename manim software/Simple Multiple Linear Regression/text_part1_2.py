"""
text_part1_2.py
TEXT-A  What / How / Why cards          (between Anim02 → Anim03)
TEXT-B  Simple vs Multiple table        (between Anim03 → Anim04)
TEXT-C  Residual definition card        (between Anim06 → Anim07)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared import *


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-A — What / How / Why  (CardFlip, 3 sequential cards)
# ══════════════════════════════════════════════════════════════════════════════
class TextA_WhatHowWhy(Scene):
    def construct(self):
        self.camera.background_color = BG

        section = Text("Linear Regression — In 3 Lines",
                       font_size=26, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(section), run_time=0.6)

        cards_data = [
            (
                "WHAT",
                BLUE_D,
                [
                    "Finds the best-fit line between input features (X)",
                    "and a continuous target (y).",
                    "Uses that line to predict on unseen data.",
                ],
                UP * 1.5,
            ),
            (
                "HOW",
                GREEN_G,
                [
                    "Minimises the sum of squared differences between",
                    "actual y and predicted ŷ  (Ordinary Least Squares).",
                    "Solved analytically (Normal Eq) or iteratively (GD).",
                ],
                ORIGIN,
            ),
            (
                "WHY USE IT",
                ORANGE_L,
                [
                    "Interpretable, blazing fast, no hyperparameters.",
                    "The mandatory baseline before any complex model.",
                    "If it works well — you don't need XGBoost.",
                ],
                DOWN * 1.5,
            ),
        ]

        card_mobs = []
        for label, color, lines, pos in cards_data:
            bg = RoundedRectangle(
                corner_radius=0.13, width=11.5, height=1.55,
                fill_color=SURFACE, fill_opacity=1.0,
                stroke_color=color, stroke_width=2.2,
            ).move_to(pos)

            label_mob = Text(label, font_size=20, color=color, weight=BOLD)\
                .next_to(bg.get_left(), RIGHT, buff=0.35)

            sep = Line(
                label_mob.get_right() + RIGHT * 0.2,
                label_mob.get_right() + RIGHT * 0.2 + DOWN * bg.height * 0.55,
                color=color, stroke_width=1.2, stroke_opacity=0.5
            ).move_to(
                [label_mob.get_right()[0] + 0.25,
                 bg.get_center()[1], 0]
            )

            body_mobs = VGroup(*[
                Text(line, font_size=17, color=BODY) for line in lines
            ]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)\
              .next_to(sep, RIGHT, buff=0.25)

            grp = VGroup(bg, label_mob, sep, body_mobs)
            card_mobs.append(grp)

        # Cards slide in from right one at a time
        self.play(
            LaggedStart(
                *[FadeIn(g, shift=LEFT * 0.4) for g in card_mobs],
                lag_ratio=0.35, run_time=2.0
            )
        )
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-B — Simple vs Multiple Linear Regression  (TableBuild)
# ══════════════════════════════════════════════════════════════════════════════
class TextB_SimpleVsMultiple(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Simple  vs  Multiple Linear Regression",
                     font_size=26, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        col_w   = [3.0, 2.5, 2.8, 3.2]
        row_h   = 0.78
        headers = ["Type", "Features", "Example", "Geometry"]
        rows    = [
            ["Simple",   "1 feature",  "Price ~ Size",
             "A straight line in 2D"],
            ["Multiple", "2+ features", "Price ~ Size + Beds + Location",
             "A hyperplane in N-D space"],
        ]
        col_colors = [BLUE_D, GREEN_G]

        def make_row_group(texts, bg_color, text_colors, y_pos, bold=False):
            grp = VGroup()
            x = -(sum(col_w) + 3 * 0.06) / 2
            for txt, w, tc in zip(texts, col_w, text_colors):
                cell_bg = Rectangle(
                    width=w, height=row_h,
                    fill_color=bg_color, fill_opacity=1.0,
                    stroke_color=BORDER, stroke_width=0.8,
                ).move_to([x + w / 2, y_pos, 0])
                cell_txt = Text(
                    txt, font_size=15,
                    color=tc,
                    weight=BOLD if bold else NORMAL,
                ).move_to(cell_bg.get_center())
                grp.add(VGroup(cell_bg, cell_txt))
                x += w + 0.06
            return grp

        y_start = 1.2
        h_row = make_row_group(
            headers, "#1a1e2a",
            [HEADING] * 4, y_start, bold=True
        )
        self.play(FadeIn(h_row), run_time=0.5)

        for i, (row, color) in enumerate(zip(rows, col_colors)):
            y = y_start - (i + 1) * row_h
            alt = SURFACE if i % 2 == 0 else "#0f1218"
            text_cols = [color] + [BODY] * 3
            d_row = make_row_group(row, alt, text_cols, y)
            self.play(FadeIn(d_row, shift=RIGHT * 0.25), run_time=0.45)
            self.wait(0.9)

        # Geometric note below table
        note = Text(
            "Simple LR: one X → line in 2D\n"
            "Multiple LR: many X → hyperplane in N-dimensional space",
            font_size=16, color=MUTED
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-C — Residual Definition  (CardFlip, yellow border)
# ══════════════════════════════════════════════════════════════════════════════
class TextC_ResidualDefinition(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("What Is a Residual?",
                     font_size=26, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Main formula
        formula = MathTex(
            r"\text{Residual} = y_i - \hat{y}_i",
            font_size=54, color=YELLOW_R
        ).move_to(UP * 0.9)
        self.play(Write(formula), run_time=0.9)

        # Three explanation cards stacked
        lines = [
            (YELLOW_R, "Actual y  −  Predicted ŷ  =  the gap the model didn't close"),
            (BLUE_D,   "The model optimises β to make the SUM of squared residuals as small as possible"),
            (MUTED,    "ε in the true model (y = Xβ + ε) is the population-level equivalent"),
        ]

        for i, (color, text) in enumerate(lines):
            bg = RoundedRectangle(
                corner_radius=0.12, width=11.5, height=0.72,
                fill_color=SURFACE, fill_opacity=1.0,
                stroke_color=color, stroke_width=1.8,
            ).move_to(DOWN * (0.2 + i * 0.82))
            txt = Text(text, font_size=17, color=BODY)\
                .move_to(bg.get_center())
            self.play(FadeIn(bg), FadeIn(txt, shift=RIGHT * 0.15), run_time=0.5)
            self.wait(0.9)

        self.wait(1.5)
