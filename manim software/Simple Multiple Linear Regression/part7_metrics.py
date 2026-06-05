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
# ANIM 29 — Three formula cards slide in from the left (MAE, RMSE, R²)
# ══════════════════════════════════════════════════════════════════════════════
class Anim29_MetricCards(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Evaluation Metrics — All 6", font_size=30, color=HEADING)\
            .to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        cards_data = [
            # Row 1
            (r"\text{MSE} = \frac{1}{n}\sum(y_i - \hat{y}_i)^2",
             "MSE — Mean Squared Error",
             "Units are squared. Penalises large errors heavily. Used in OLS cost function.",
             MUTED),
            (r"\text{RMSE} = \sqrt{\frac{1}{n}\sum(y_i-\hat{y}_i)^2}",
             "RMSE — Root Mean Squared Error",
             "Same units as y. Still punishes large errors. Most used in competitions.",
             ORANGE_L),
            (r"\text{MAE} = \frac{1}{n}\sum|y_i - \hat{y}_i|",
             "MAE — Mean Absolute Error",
             "Robust to outliers. Equal penalty for all errors. Easy to explain.",
             BLUE_D),
            # Row 2
            (r"R^2 = 1 - \frac{SS_{res}}{SS_{tot}}",
             "R² — Coefficient of Determination",
             "Variance explained. Always increases with more features — use Adj R² instead.",
             GREEN_G),
            (r"\text{Adj } R^2 = 1 - \frac{(1-R^2)(n-1)}{n-p-1}",
             "Adjusted R² — Honest R²",
             "Penalises useless features. Use when comparing models with different # of features.",
             PURPLE),
            (r"\text{MAPE} = \frac{100}{n}\sum\frac{|y_i - \hat{y}_i|}{|y_i|}",
             "MAPE — Mean Abs. Percentage Error",
             "Percentage error — intuitive for stakeholders. Avoid when y ≈ 0.",
             YELLOW_R),
        ]

        def _wrap_desc(text, max_chars=45):
            """Word-wrap description to fit inside card width."""
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

        def metric_card(formula_str, name, description, color, width=4.3):
            card_bg = RoundedRectangle(corner_radius=0.12, width=width, height=2.0,
                                       fill_color="#13161e", fill_opacity=1.0,
                                       stroke_color=color, stroke_width=1.8)
            formula = MathTex(formula_str, font_size=22, color=color)\
                .next_to(card_bg.get_top(), DOWN, buff=0.22)
            name_t = Text(name, font_size=13, color=color, weight=BOLD)\
                .next_to(formula, DOWN, buff=0.10)
            desc_t = Text(_wrap_desc(description), font_size=11,
                          color=MUTED, line_spacing=1.2)\
                .next_to(name_t, DOWN, buff=0.08)
            return VGroup(card_bg, formula, name_t, desc_t)

        row1 = VGroup(*[metric_card(*d) for d in cards_data[:3]])\
            .arrange(RIGHT, buff=0.25).move_to(UP * 0.9)
        row2 = VGroup(*[metric_card(*d) for d in cards_data[3:]])\
            .arrange(RIGHT, buff=0.25).move_to(DOWN * 1.2)

        # Slide in row 1 from left, row 2 from right
        row1.shift(LEFT * 13)
        row2.shift(RIGHT * 13)

        self.play(row1.animate.shift(RIGHT * 13), run_time=1.1)
        self.wait(0.3)
        self.play(row2.animate.shift(LEFT * 13), run_time=1.1)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 30 — R² warning label flashes: "always increases with more features"
# ══════════════════════════════════════════════════════════════════════════════
class Anim30_R2Warning(Scene):
    def construct(self):
        self.camera.background_color = BG

        r2_formula = MathTex(r"R^2 = 1 - \frac{SS_{res}}{SS_{tot}}",
                              font_size=52, color=GREEN_G).move_to(UP * 1.5)
        self.play(Write(r2_formula), run_time=0.8)

        # Warning box
        warn_bg = RoundedRectangle(corner_radius=0.15, width=9.5, height=2.2,
                                    fill_color="#1a1200", fill_opacity=1,
                                    stroke_color=YELLOW_R, stroke_width=2.5)\
            .move_to(DOWN * 0.5)
        # Warning icon — yellow pill badge with '!' (no Triangle, no special chars)
        warn_badge_bg = RoundedRectangle(
            corner_radius=0.08, width=0.52, height=0.42,
            fill_color=YELLOW_R, fill_opacity=1.0, stroke_width=0
        ).next_to(warn_bg.get_left(), RIGHT, buff=0.35)
        warn_badge_txt = Text("!", font_size=18, color="#0d0f14", weight=BOLD)\
            .move_to(warn_badge_bg.get_center())
        warn_icon = VGroup(warn_badge_bg, warn_badge_txt)
        warn_text = Text(
            "R² ALWAYS increases when you add more features\n"
            "— even if those features are pure random noise!",
            font_size=21, color=YELLOW_R
        ).next_to(warn_icon, RIGHT, buff=0.3)

        self.play(FadeIn(warn_bg), run_time=0.3)
        self.play(Write(warn_icon), Write(warn_text), run_time=0.9)

        # Flash the warning box twice
        for _ in range(2):
            self.play(warn_bg.animate.set_stroke(color=WHITE, width=3.5), run_time=0.25)
            self.play(warn_bg.animate.set_stroke(color=YELLOW_R, width=2.5), run_time=0.25)

        solution = Text("Solution: always report Adjusted R² when comparing models",
                        font_size=20, color=GREEN_G).next_to(warn_bg, DOWN, buff=0.4)
        self.play(Write(solution), run_time=0.9)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 31 — R² counter ticks up as random features are added; Adj R² stays flat
# ══════════════════════════════════════════════════════════════════════════════
class Anim31_R2VsAdjR2(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("R²  vs  Adjusted R²  as Useless Features Are Added",
                     font_size=22, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.7)

        # Feature counts and fake values
        n_feats = list(range(1, 11))
        r2_vals    = [0.72, 0.74, 0.755, 0.768, 0.779, 0.787, 0.793, 0.798, 0.803, 0.807]
        adj_r2_vals= [0.72, 0.73, 0.735, 0.736, 0.733, 0.726, 0.718, 0.710, 0.702, 0.694]

        axes = Axes(
            x_range=[1, 10, 1], y_range=[0.60, 0.85, 0.05],
            x_length=7.5, y_length=4.5,
            axis_config={"color": "#444a5a", "stroke_width": 2}, tips=False,
        ).shift(DOWN * 0.5)
        xl = Text("Number of features →", font_size=18, color=MUTED)\
            .next_to(axes, DOWN, buff=0.25)
        self.play(Create(axes), Write(xl), run_time=0.8)

        # Tick labels on x-axis
        for n in n_feats:
            lbl = Text(str(n), font_size=13, color=MUTED)\
                .next_to(axes.c2p(n, 0.60), DOWN, buff=0.15)
            self.add(lbl)

        r2_dots    = VGroup()
        adj_r2_dots = VGroup()
        r2_line_segs    = VGroup()
        adj_r2_line_segs = VGroup()

        # Labels placed next_to the last dots — avoids overlap with graph
        r2_label  = Text("R²",     font_size=18, color=RED_B)
        adj_label = Text("Adj R²", font_size=18, color=GREEN_G)

        for i in range(len(n_feats)):
            d1 = Dot(axes.c2p(n_feats[i], r2_vals[i]),    color=RED_B,   radius=0.10)
            d2 = Dot(axes.c2p(n_feats[i], adj_r2_vals[i]), color=GREEN_G, radius=0.10)
            r2_dots.add(d1)
            adj_r2_dots.add(d2)

            if i > 0:
                seg1 = Line(axes.c2p(n_feats[i-1], r2_vals[i-1]),
                            axes.c2p(n_feats[i],   r2_vals[i]),
                            color=RED_B, stroke_width=2.5)
                seg2 = Line(axes.c2p(n_feats[i-1], adj_r2_vals[i-1]),
                            axes.c2p(n_feats[i],   adj_r2_vals[i]),
                            color=GREEN_G, stroke_width=2.5)
                r2_line_segs.add(seg1)
                adj_r2_line_segs.add(seg2)

        # Animate feature-by-feature
        self.play(FadeIn(r2_dots[0]), FadeIn(adj_r2_dots[0]), run_time=0.4)
        for i in range(1, len(n_feats)):
            self.play(
                FadeIn(r2_dots[i]),
                FadeIn(adj_r2_dots[i]),
                Create(r2_line_segs[i-1]),
                Create(adj_r2_line_segs[i-1]),
                run_time=0.35
            )

        # Position labels next to the final data points, clear of the graph
        r2_label.next_to(r2_dots[-1],    RIGHT, buff=0.22)
        adj_label.next_to(adj_r2_dots[-1], RIGHT, buff=0.22)
        self.play(FadeIn(r2_label), FadeIn(adj_label), run_time=0.5)

        note = Text("R² keeps climbing — Adj R² reveals the truth: model is getting worse",
                    font_size=17, color=YELLOW_R).to_edge(DOWN, buff=0.4)
        self.play(Write(note), run_time=0.9)
        self.wait(2.0)
