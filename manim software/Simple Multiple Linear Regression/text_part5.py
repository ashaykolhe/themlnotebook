"""
text_part5.py
TEXT-H  Gradient Descent 6-step algorithm      (between Anim19 → Anim20)
TEXT-I  GD types comparison table              (between Anim20 → Anim21)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared import *


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-H — Gradient Descent 6-Step Algorithm  (BulletReveal + formula header)
# ══════════════════════════════════════════════════════════════════════════════
class TextH_GDAlgorithm(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Gradient Descent — What the Computer Actually Does",
                     font_size=22, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Update rule formula at top
        update_rule = MathTex(
            r"\beta \;\leftarrow\; \beta - \alpha \cdot \underbrace{\left(-\frac{2}{n}X^\top(y-X\beta)\right)}_{\text{gradient}}",
            font_size=36, color=YELLOW_R
        ).move_to(UP * 1.55)
        self.play(Write(update_rule), run_time=1.0)

        sep = Line(LEFT * 6, RIGHT * 6, color=BORDER, stroke_width=1)\
            .next_to(update_rule, DOWN, buff=0.3)
        self.play(Create(sep), run_time=0.3)

        steps = [
            (MUTED,    "1.",  "Initialise β  (all zeros, or small random values)"),
            (BLUE_D,   "2.",  "Compute predictions:  ŷ = Xβ"),
            (BLUE_D,   "3.",  "Compute residuals:    e  = y − ŷ"),
            (YELLOW_R, "4.",  "Compute gradient:     grad = -(2/n) X'e"),
            (ORANGE_L, "5.",  "Update coefficients:  β  ← β − α × grad"),
            (GREEN_G,  "6.",  "Repeat until  ||grad|| < ε  or  max iterations reached"),
        ]

        y_start = 0.55
        for i, (color, num, text) in enumerate(steps):
            num_mob  = Text(num,  font_size=18, color=color, weight=BOLD)
            text_mob = Text(text, font_size=18, color=BODY)
            row = VGroup(num_mob, text_mob).arrange(RIGHT, buff=0.25)
            row.move_to(UP * (y_start - i * 0.64)).align_to(LEFT * 5.5, LEFT)

            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.42)
            self.wait(1.0)

        self.wait(1.2)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-I — GD Types Comparison  (TableBuild, 3 rows × 3 columns)
# ══════════════════════════════════════════════════════════════════════════════
class TextI_GDTypesTable(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Three Flavours of Gradient Descent",
                     font_size=26, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        col_w   = [2.8, 2.5, 5.2]
        row_h   = 0.88
        headers = ["Type", "Batch Size", "Best For"]
        rows_data = [
            (BLUE_D,    "Batch GD",   "All n samples",
             "Small datasets — stable gradient, smooth convergence"),
            (ORANGE_L,  "SGD",        "1 sample",
             "Huge datasets, online learning — fast but noisy"),
            (GREEN_G,   "Mini-batch", "16–512 samples",
             "Deep learning, GPU training — best of both worlds"),
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
                    txt, font_size=14,
                    color=tc,
                    weight=BOLD if bold else NORMAL,
                ).move_to(cell_bg.get_center())
                grp.add(VGroup(cell_bg, cell_txt))
                x += w + 0.06
            return grp

        y_start = 1.2
        h_row = make_row(
            [(h, HEADING) for h in headers],
            y_start, "#1a1e2a", bold=True
        )
        self.play(FadeIn(h_row), run_time=0.5)

        for i, (color, name, batch, best) in enumerate(rows_data):
            y = y_start - (i + 1) * row_h
            alt = SURFACE if i % 2 == 0 else "#0f1218"
            d_row = make_row(
                [(name, color), (batch, MUTED), (best, BODY)],
                y, alt
            )
            self.play(FadeIn(d_row, shift=RIGHT * 0.2), run_time=0.45)
            self.wait(1.0)

        # Bottom note
        note = Text(
            "sklearn's SGDRegressor uses mini-batch GD.\n"
            "LinearRegression uses the Normal Equation (exact, no iterations).",
            font_size=15, color=MUTED
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(1.5)
