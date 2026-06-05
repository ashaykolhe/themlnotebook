"""
text_part3.py
TEXT-D  Symbol table (ŷ β x)                 (between Anim10 → Anim11)
TEXT-E  Coefficient scaling warning card      (between Anim11 → Anim12)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared import *


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-D — Symbol Table: ŷ, β₀, β₁…β_n, x₁…x_n  (TableBuild, 4 rows)
# ══════════════════════════════════════════════════════════════════════════════
class TextD_SymbolTable(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Every Symbol in the Equation",
                     font_size=26, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Column widths
        col_w   = [2.2, 3.0, 5.8]
        row_h   = 0.80
        headers = ["Symbol", "Name", "Meaning"]
        rows_data = [
            (BLUE_D,   "ŷ",       "y-hat  (predicted)",
             "Model output — our best guess, NOT the true y"),
            (ORANGE_L, "β₀",      "Intercept / bias",
             "ŷ when ALL features = 0  (where line crosses y-axis)"),
            (GREEN_G,  "β₁ … βn",  "Coefficients / weights",
             "Change in ŷ per 1-unit rise in that feature, all else fixed"),
            (PURPLE,   "x₁ … xn",  "Features / predictors",
             "The input variables fed into the model"),
        ]

        def make_cell(txt, w, h, bg_color, txt_color, bold=False):
            cell_bg = Rectangle(
                width=w, height=h,
                fill_color=bg_color, fill_opacity=1.0,
                stroke_color=BORDER, stroke_width=0.8,
            )
            cell_txt = Text(
                txt, font_size=15,
                color=txt_color,
                weight=BOLD if bold else NORMAL,
            ).move_to(cell_bg.get_center())
            return VGroup(cell_bg, cell_txt)

        def make_row(texts_and_colors, y_pos, bg_color, bold=False):
            row = VGroup()
            x = -(sum(col_w) + 2 * 0.06) / 2
            for (txt, tc), w in zip(texts_and_colors, col_w):
                cell = make_cell(txt, w, row_h, bg_color, tc, bold)
                cell.move_to([x + w / 2, y_pos, 0])
                row.add(cell)
                x += w + 0.06
            return row

        y_start = 1.5
        # Header
        h_row = make_row(
            [(h, HEADING) for h in headers],
            y_start, "#1a1e2a", bold=True
        )
        self.play(FadeIn(h_row), run_time=0.5)

        for i, (color, sym, name, meaning) in enumerate(rows_data):
            y = y_start - (i + 1) * row_h
            alt = SURFACE if i % 2 == 0 else "#0f1218"
            d_row = make_row(
                [(sym, color), (name, color), (meaning, BODY)],
                y, alt
            )
            self.play(FadeIn(d_row, shift=RIGHT * 0.2), run_time=0.4)
            self.wait(1.0)

        self.wait(1.0)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-E — Coefficient Scaling Warning  (CardFlip, yellow warning border)
# ══════════════════════════════════════════════════════════════════════════════
class TextE_CoefficientScaling(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Warning badge in title — yellow pill + "!" (no special Unicode)
        warn_badge_bg = RoundedRectangle(
            corner_radius=0.08, width=0.48, height=0.40,
            fill_color=YELLOW_R, fill_opacity=1.0, stroke_width=0
        )
        warn_badge_txt = Text("!", font_size=16, color="#0d0f14", weight=BOLD)\
            .move_to(warn_badge_bg.get_center())
        warn_badge = VGroup(warn_badge_bg, warn_badge_txt)
        title_txt = Text("A Very Common Trap", font_size=26, color=YELLOW_R)
        title = VGroup(warn_badge, title_txt).arrange(RIGHT, buff=0.22)\
            .to_edge(UP, buff=0.35)
        self.play(FadeIn(warn_badge, scale=1.2), Write(title_txt), run_time=0.6)

        # Bad example — height sized to fit label + 2-line body with padding
        bad_bg = RoundedRectangle(
            corner_radius=0.13, width=11.5, height=1.72,
            fill_color=SURFACE, fill_opacity=1.0,
            stroke_color=RED_B, stroke_width=2.2,
        ).move_to(UP * 1.05)

        # Wrong label — red badge with "X" + text (no special Unicode)
        wrong_badge_bg = RoundedRectangle(
            corner_radius=0.07, width=0.44, height=0.36,
            fill_color=RED_B, fill_opacity=1.0, stroke_width=0
        )
        wrong_badge_txt = Text("X", font_size=14, color="#0d0f14", weight=BOLD)\
            .move_to(wrong_badge_bg.get_center())
        wrong_badge = VGroup(wrong_badge_bg, wrong_badge_txt)
        wrong_text = Text("WRONG INTERPRETATION", font_size=17, color=RED_B, weight=BOLD)
        bad_label = VGroup(wrong_badge, wrong_text)\
            .arrange(RIGHT, buff=0.18)\
            .next_to(bad_bg.get_top(), DOWN, buff=0.25)\
            .align_to(bad_bg, LEFT).shift(RIGHT * 0.3)
        bad_body  = Text(
            'β = 0.01 for "income (dollars)"  vs  β = 2.5 for "rooms"\n'
            '→ rooms do NOT matter 250× more than income',
            font_size=17, color=BODY,
            t2c={"β = 0.01": RED_B, "β = 2.5": RED_B}
        ).next_to(bad_label, DOWN, buff=0.18)\
         .align_to(bad_label, LEFT)

        self.play(FadeIn(bad_bg), run_time=0.4)
        self.play(Write(bad_label), FadeIn(bad_body), run_time=0.7)
        self.wait(0.8)

        # Explanation
        reason_bg = RoundedRectangle(
            corner_radius=0.13, width=11.5, height=0.75,
            fill_color=SURFACE, fill_opacity=1.0,
            stroke_color=MUTED, stroke_width=1.5,
        ).move_to(DOWN * 0.385)
        reason_txt = Text(
            "Income is in large units — its coefficient is small\nbecause the unit is large, not because it matters less.",
            font_size=16, color=MUTED,
        ).next_to(reason_bg.get_top(), DOWN, buff=0.18)\
         .align_to(reason_bg, LEFT).shift(RIGHT * 0.3)
        self.play(FadeIn(reason_bg), FadeIn(reason_txt), run_time=0.5)
        self.wait(0.5)

        # Fix
        fix_bg = RoundedRectangle(
            corner_radius=0.13, width=11.5, height=1.15,
            fill_color=SURFACE, fill_opacity=1.0,
            stroke_color=GREEN_G, stroke_width=2.2,
        ).move_to(DOWN * 1.535)
        fix_label = Text("FIX", font_size=17, color=GREEN_G, weight=BOLD)\
            .next_to(fix_bg.get_top(), DOWN, buff=0.22)\
            .align_to(fix_bg, LEFT).shift(RIGHT * 0.3)
        fix_body  = Text(
            "StandardScaler before fitting  →  all features on same scale\n"
            "→  coefficients become directly comparable for feature importance",
            font_size=17, color=BODY,
        ).next_to(fix_label, DOWN, buff=0.12)\
         .align_to(fix_bg, LEFT).shift(RIGHT * 0.3)
        self.play(FadeIn(fix_bg), run_time=0.3)
        self.play(Write(fix_label), FadeIn(fix_body), run_time=0.7)
        self.wait(2.0)
