"""
text_part6.py
TEXT-J  Normality misconception warning card   (inside Anim24, after histograms)
TEXT-K  LINE-MO detection methods table        (between Anim28 → Anim29)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared import *


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-J — Normality Misconception  (CardFlip, red warning)
# ══════════════════════════════════════════════════════════════════════════════
class TextJ_NormalityMisconception(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("N — Normality of Residuals",
                     font_size=26, color=PURPLE).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Big misconception card
        wrong_bg = RoundedRectangle(
            corner_radius=0.14, width=11.5, height=2.0,
            fill_color="#1a0a0a", fill_opacity=1.0,
            stroke_color=RED_B, stroke_width=2.5,
        ).move_to(UP * 0.8)
        wrong_head = Text("❌  MOST COMMON MISCONCEPTION",
                          font_size=19, color=RED_B, weight=BOLD)\
            .next_to(wrong_bg.get_top(), DOWN, buff=0.25)
        wrong_body = Text(
            '"Linear regression assumes the DATA is normally distributed."\n'
            "→  This is WRONG.",
            font_size=18, color=BODY,
            t2c={"WRONG": RED_B}
        ).next_to(wrong_head, DOWN, buff=0.2)

        self.play(FadeIn(wrong_bg), run_time=0.4)
        self.play(Write(wrong_head), FadeIn(wrong_body), run_time=0.8)
        self.wait(0.7)

        # Correct statement
        right_bg = RoundedRectangle(
            corner_radius=0.14, width=11.5, height=2.2,
            fill_color="#0a1a0a", fill_opacity=1.0,
            stroke_color=GREEN_G, stroke_width=2.5,
        ).move_to(DOWN * 1.1)
        right_head = Text("✅  WHAT IT ACTUALLY MEANS",
                          font_size=19, color=GREEN_G, weight=BOLD)\
            .next_to(right_bg.get_top(), DOWN, buff=0.25)
        right_body = Text(
            "The RESIDUALS (y − ŷ) should be approximately normally distributed.\n"
            "Your input features X can be skewed, uniform — anything at all.\n"
            "With n > 30+, the Central Limit Theorem makes this less critical anyway.",
            font_size=17, color=BODY,
            t2c={"RESIDUALS": GREEN_G, "Central Limit Theorem": YELLOW_R}
        ).next_to(right_head, DOWN, buff=0.2)

        self.play(FadeIn(right_bg), run_time=0.4)
        self.play(Write(right_head), FadeIn(right_body), run_time=0.9)
        self.wait(2.5)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-K — LINE-MO Detection Methods Table  (TableBuild, 6 rows × 2 cols)
# ══════════════════════════════════════════════════════════════════════════════
class TextK_DetectionMethodsTable(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("LINE-MO — Your Diagnostic Checklist",
                     font_size=26, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        letter_colors = {
            "L": GREEN_G, "I": BLUE_D, "N": PURPLE,
            "E": YELLOW_R, "M": ORANGE_L, "O": RED_B
        }

        col_w   = [3.2, 4.0, 4.3]
        row_h   = 0.72
        headers = ["Assumption", "Detect With", "Red Flag"]
        rows_data = [
            ("L", "L  Linearity",
             "Residuals vs. Fitted plot",
             "U-shape or curved pattern"),
            ("I", "I  Independence",
             "Durbin-Watson test",
             "D-W ≠ 2  (near 0 or near 4)"),
            ("N", "N  Normality",
             "Q-Q plot of residuals",
             "Points stray from diagonal"),
            ("E", "E  Equal Variance",
             "Scale-Location plot",
             "Fan / funnel shape appears"),
            ("M", "M  Multicollinearity",
             "VIF (Variance Inflation Factor)",
             "VIF > 5 = warning, > 10 = severe"),
            ("O", "O  No Outliers",
             "Cook's Distance plot",
             "Cook's D > 4/n → investigate"),
        ]

        def make_row(texts_colors, y, bg_color, bold=False):
            grp = VGroup()
            x = -(sum(col_w) + 2 * 0.06) / 2
            for (txt, tc), w in zip(texts_colors, col_w):
                cell_bg = Rectangle(
                    width=w, height=row_h,
                    fill_color=bg_color, fill_opacity=1.0,
                    stroke_color=BORDER, stroke_width=0.8,
                ).move_to([x + w / 2, y, 0])
                cell_txt = Text(
                    txt, font_size=13,
                    color=tc,
                    weight=BOLD if bold else NORMAL,
                ).move_to(cell_bg.get_center())
                grp.add(VGroup(cell_bg, cell_txt))
                x += w + 0.06
            return grp

        y_start = 1.75
        h_row = make_row(
            [(h, HEADING) for h in headers],
            y_start, "#1a1e2a", bold=True
        )
        self.play(FadeIn(h_row), run_time=0.5)

        for i, (letter, assumption, detect, flag) in enumerate(rows_data):
            color = letter_colors[letter]
            y = y_start - (i + 1) * row_h
            alt = SURFACE if i % 2 == 0 else "#0f1218"
            d_row = make_row(
                [(assumption, color), (detect, MUTED), (flag, BODY)],
                y, alt
            )
            self.play(FadeIn(d_row, shift=RIGHT * 0.2), run_time=0.38)
            self.wait(0.8)

        self.wait(1.5)
