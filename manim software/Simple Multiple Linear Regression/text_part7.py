"""
text_part7.py
TEXT-L  R² interpretation table         (between Anim30 → Anim31)
TEXT-M  MAE vs RMSE decision            (between Anim31 → Anim32)
"""
from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from shared import *


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-L — R² Interpretation Table  (TableBuild, 6 rows, colour-coded)
# ══════════════════════════════════════════════════════════════════════════════
class TextL_R2InterpretationTable(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("What Does Your R² Score Actually Mean?",
                     font_size=24, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        col_w   = [2.2, 3.4, 4.9]
        row_h   = 0.70
        headers = ["R² Value", "Interpretation", "Context"]
        rows_data = [
            (RED_B,    "< 0",    "Worse than predicting the mean!",
             "Model is broken, leakage, or wrong data split"),
            (RED_B,    "0.0",    "No better than baseline (ȳ)",
             "Features explain nothing about the target"),
            (YELLOW_R, "0.3–0.5","Moderate",
             "Social science, economics — expected range"),
            (GREEN_G,  "0.7–0.9","Good",
             "Typical ML regression task"),
            (GREEN_G,  "0.95+",  "Excellent",
             "Engineering, physics — tight physical laws"),
            (RED_B,    "1.0",    "Perfect — highly suspicious!",
             "Very likely data leakage or degenerate setup"),
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

        y_start = 1.85
        h_row = make_row(
            [(h, HEADING) for h in headers],
            y_start, "#1a1e2a", bold=True
        )
        self.play(FadeIn(h_row), run_time=0.5)

        for i, (color, val, interp, ctx) in enumerate(rows_data):
            y = y_start - (i + 1) * row_h
            alt = SURFACE if i % 2 == 0 else "#0f1218"
            d_row = make_row(
                [(val, color), (interp, color), (ctx, BODY)],
                y, alt
            )
            self.play(FadeIn(d_row, shift=RIGHT * 0.2), run_time=0.38)
            self.wait(0.75)

        note = Text(
            "R² can be negative on the TEST set — it means the model\nis actively harmful compared to just predicting ȳ",
            font_size=14, color=YELLOW_R
        ).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# TEXT-M — MAE vs RMSE Decision  (SplitReveal, two panels with bullet rows)
# ══════════════════════════════════════════════════════════════════════════════
class TextM_MAEvsRMSE(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Which Metric Should You Use?",
                     font_size=26, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Divider
        div = Line(UP * 2.8, DOWN * 3.2, color=BORDER, stroke_width=1.5)
        self.play(Create(div), run_time=0.4)

        # Panel headers
        mae_head  = Text("USE MAE WHEN…",  font_size=20, color=BLUE_D, weight=BOLD)\
            .move_to(LEFT * 3.2 + UP * 2.3)
        rmse_head = Text("USE RMSE WHEN…", font_size=20, color=ORANGE_L, weight=BOLD)\
            .move_to(RIGHT * 3.2 + UP * 2.3)
        self.play(Write(mae_head), Write(rmse_head), run_time=0.6)

        mae_bullets = [
            ("Outliers exist and shouldn't dominate", BLUE_D),
            ("All error sizes matter equally", BLUE_D),
            ("Explaining to non-technical stakeholders", BLUE_D),
            ("Delivery times, counts, demand forecasting", MUTED),
        ]
        rmse_bullets = [
            ("Large errors are disproportionately costly", ORANGE_L),
            ("Engineering, finance, structural prediction", ORANGE_L),
            ("Kaggle competitions (RMSE is the standard)", ORANGE_L),
            ("When differentiability of the loss matters", MUTED),
        ]

        y_start = 1.55
        for i, ((mae_txt, mc), (rmse_txt, rc)) in enumerate(
                zip(mae_bullets, rmse_bullets)):
            y = y_start - i * 0.88

            mae_row = VGroup(
                Text("•", font_size=16, color=mc),
                Text(mae_txt, font_size=16, color=BODY)
            ).arrange(RIGHT, buff=0.18).move_to(LEFT * 3.2 + UP * y)
            mae_row.align_to(LEFT * 6.0, LEFT)

            rmse_row = VGroup(
                Text("•", font_size=16, color=rc),
                Text(rmse_txt, font_size=16, color=BODY)
            ).arrange(RIGHT, buff=0.18).move_to(RIGHT * 3.2 + UP * y)
            rmse_row.align_to(RIGHT * 6.0 - RIGHT * 5.7, LEFT)

            self.play(
                FadeIn(mae_row,  shift=RIGHT * 0.2),
                FadeIn(rmse_row, shift=LEFT  * 0.2),
                run_time=0.45
            )
            self.wait(0.9)

        # Tie-breaker note
        note_bg = RoundedRectangle(
            corner_radius=0.12, width=11.5, height=0.65,
            fill_color=SURFACE, fill_opacity=1.0,
            stroke_color=YELLOW_R, stroke_width=1.8,
        ).to_edge(DOWN, buff=0.3)
        note_txt = Text(
            "Tip: train with RMSE (OLS is optimal), report MAE if you want outlier-robust reporting.",
            font_size=16, color=YELLOW_R
        ).move_to(note_bg.get_center())
        self.play(FadeIn(note_bg), FadeIn(note_txt), run_time=0.5)
        self.wait(1.5)
