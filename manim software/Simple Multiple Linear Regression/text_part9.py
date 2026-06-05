"""
text_part9.py
TEXT-Q  Error decomposition table            (between Anim37 → Anim38)
TEXT-R  Regularisation-bias-variance link    (between Anim38 → Anim39)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared import *


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-Q — Error Decomposition Table  (TableBuild, 3 rows × 3 cols)
# ══════════════════════════════════════════════════════════════════════════════
class TextQ_ErrorDecomposition(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Every Model's Error Breaks Into Three Parts",
                     font_size=24, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Formula first
        formula = MathTex(
            r"\mathbb{E}[(y-\hat{y})^2] = \underbrace{\text{Bias}^2}_\text{systematic} + \underbrace{\text{Variance}}_\text{sensitivity} + \underbrace{\sigma^2}_\text{irreducible}",
            font_size=34, color=HEADING
        ).move_to(UP * 1.6)
        self.play(Write(formula), run_time=1.0)

        col_w   = [2.8, 3.5, 4.2]
        row_h   = 0.80
        headers = ["Component", "Caused By", "Reduced By"]
        rows_data = [
            (BLUE_D,   "Bias²",
             "Too simple model, wrong assumptions",
             "More features, polynomial terms, less λ"),
            (ORANGE_L, "Variance",
             "Too complex model, overfitting, too many features",
             "Regularisation (Ridge/Lasso), more data"),
            (MUTED,    "Irreducible Noise",
             "True randomness — measurement error, missing vars",
             "Cannot be reduced — it is the floor"),
        ]

        def _wrap(text, max_chars=35):
            words = text.split()
            lines, cur, cur_len = [], [], 0
            for w in words:
                added = len(w) + (1 if cur else 0)
                if cur_len + added > max_chars:
                    lines.append(' '.join(cur))
                    cur, cur_len = [w], len(w)
                else:
                    cur.append(w)
                    cur_len += added
            if cur:
                lines.append(' '.join(cur))
            return '\n'.join(lines)

        def make_row(tc_pairs, y, bg_color, bold=False):
            grp = VGroup()
            x = -(sum(col_w) + 2 * 0.06) / 2
            for col_idx, ((txt, tc), w) in enumerate(zip(tc_pairs, col_w)):
                # Wrap the "Caused By" column (index 1) to fit within its cell
                display_txt = _wrap(txt) if col_idx == 1 else txt
                cell_bg = Rectangle(
                    width=w, height=row_h,
                    fill_color=bg_color, fill_opacity=1.0,
                    stroke_color=BORDER, stroke_width=0.8,
                ).move_to([x + w / 2, y, 0])
                cell_txt = Text(
                    display_txt, font_size=13,
                    color=tc,
                    weight=BOLD if bold else NORMAL,
                ).move_to(cell_bg.get_center())
                grp.add(VGroup(cell_bg, cell_txt))
                x += w + 0.06
            return grp

        y_start = 0.55
        h_row = make_row([(h, HEADING) for h in headers], y_start,
                         "#1a1e2a", bold=True)
        self.play(FadeIn(h_row), run_time=0.4)

        for i, (color, comp, caused, reduced) in enumerate(rows_data):
            y = y_start - (i + 1) * row_h
            alt = SURFACE if i % 2 == 0 else "#0f1218"
            d_row = make_row(
                [(comp, color), (caused, BODY), (reduced, BODY)], y, alt
            )
            self.play(FadeIn(d_row, shift=RIGHT * 0.2), run_time=0.42)
            self.wait(1.0)

        self.wait(1.2)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-R — Regularisation Controls the Bias-Variance Tradeoff  (BulletReveal)
# ══════════════════════════════════════════════════════════════════════════════
class TextR_RegularisationBiasVariance(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("How to Navigate the Bias-Variance Tradeoff in Practice",
                     font_size=22, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # λ slider visual
        slider_track = Line(LEFT * 4.5, RIGHT * 4.5,
                            color=MUTED, stroke_width=3).move_to(UP * 1.5)
        label_left  = Text("λ = 0  (OLS)", font_size=15, color=MUTED)\
            .next_to(slider_track.get_left(), DOWN, buff=0.18)
        label_right = Text("λ → ∞  (all β → 0)", font_size=15, color=MUTED)\
            .next_to(slider_track.get_right(), DOWN, buff=0.18)
        bias_label  = Text("← Low bias,  High variance",
                           font_size=14, color=BLUE_D)\
            .next_to(slider_track, UP, buff=0.12).align_to(slider_track, LEFT)
        var_label   = Text("High bias,  Low variance →",
                           font_size=14, color=ORANGE_L)\
            .next_to(slider_track, UP, buff=0.12).align_to(slider_track, RIGHT)

        self.play(
            Create(slider_track),
            FadeIn(label_left), FadeIn(label_right),
            FadeIn(bias_label), FadeIn(var_label),
            run_time=0.7
        )

        sep = Line(LEFT * 6, RIGHT * 6, color=BORDER, stroke_width=1)\
            .move_to(UP * 0.7)
        self.play(Create(sep), run_time=0.3)

        # Practical scenarios
        scenarios = [
            (RED_B,    "OLS + few features + non-linear data",
             "→  High Bias  →  add polynomial features"),
            (ORANGE_L, "OLS + many features, p ≈ n",
             "→  High Variance  →  use Ridge or Lasso"),
            (BLUE_D,   "Ridge with high λ",
             "→  Moderate Bias, Low Variance\n    →  reduce λ via cross-validation"),
            (GREEN_G,  "Ridge with λ ≈ 0",
             "→  Very Low Bias, High Variance  →  increase λ"),
        ]

        y_pos = 0.15
        for color, situation, action in scenarios:
            sit_mob = Text(situation, font_size=16, color=color, weight=BOLD)
            act_mob = Text(action,    font_size=16, color=BODY)
            row = VGroup(sit_mob, act_mob).arrange(RIGHT, buff=0.3)\
                .move_to(UP * y_pos).align_to(LEFT * 5.8, LEFT)
            self.play(FadeIn(row, shift=RIGHT * 0.25), run_time=0.45)
            self.wait(1.0)
            y_pos -= 0.78

        takeaway = Text(
            "The optimal λ is NOT guesswork — find it with cross-validation.",
            font_size=17, color=YELLOW_R
        ).to_edge(DOWN, buff=0.35)
        self.play(Write(takeaway), run_time=0.7)
        self.wait(1.5)
