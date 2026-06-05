from manim import *
import numpy as np

BLUE_D   = "#4f9eff"
ORANGE_L = "#f97316"
YELLOW_R = "#fbbf24"
GREEN_G  = "#10b981"
RED_B    = "#f87171"
BG       = "#0d0f14"
MUTED    = "#8892a4"
HEADING  = "#f8fafc"


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 13 — Cost bowl appears (smooth parabola on β₁ vs MSE axes)
# ══════════════════════════════════════════════════════════════════════════════
class Anim13_CostBowlAppears(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("MSE Cost Function — Convex Bowl",
                     font_size=28, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.7)

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 9, 2],
            x_length=8.5, y_length=5.0,
            axis_config={"color": "#444a5a", "stroke_width": 2}, tips=False,
        ).shift(DOWN * 0.5)
        xl = Text("β₁  (coefficient value)", font_size=19, color=MUTED)\
            .next_to(axes, DOWN, buff=0.25)
        yl = Text("MSE Cost", font_size=19, color=MUTED)\
            .next_to(axes, LEFT, buff=0.2).rotate(PI/2)

        self.play(Create(axes), Write(xl), Write(yl), run_time=1.0)

        bowl = axes.plot(lambda x: x**2 + 0.4, x_range=[-2.85, 2.85],
                         color=BLUE_D, stroke_width=3.2)
        self.play(Create(bowl), run_time=1.5)

        mse_formula = MathTex(
            r"\text{MSE}(\beta) = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2",
            font_size=38, color=YELLOW_R
        ).to_edge(UP, buff=0.4).shift(DOWN * 0.1)

        # Replace title with formula
        self.play(FadeOut(title), FadeIn(mse_formula), run_time=0.7)
        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 14 — A point appears high on the bowl and slides down toward minimum
# ══════════════════════════════════════════════════════════════════════════════
class Anim14_BallSlidesDown(Scene):
    def construct(self):
        self.camera.background_color = BG

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 9, 2],
            x_length=8.5, y_length=5.0,
            axis_config={"color": "#444a5a", "stroke_width": 2}, tips=False,
        ).shift(DOWN * 0.5)
        bowl = axes.plot(lambda x: x**2 + 0.4, x_range=[-2.85, 2.85],
                         color=BLUE_D, stroke_width=3.2)
        self.add(axes, bowl)

        t = ValueTracker(-2.6)
        ball = always_redraw(lambda: Dot(
            axes.c2p(t.get_value(), t.get_value()**2 + 0.4),
            color=YELLOW_R, radius=0.14
        ))
        trail = TracedPath(ball.get_center, stroke_color=YELLOW_R,
                           stroke_width=2.5, stroke_opacity=0.5)
        self.add(trail, ball)
        self.wait(0.3)

        self.play(t.animate.set_value(0.0),
                  rate_func=rate_functions.ease_in_out_sine, run_time=2.5)
        # small bounce
        self.play(t.animate.set_value(0.35), run_time=0.3)
        self.play(t.animate.set_value(0.0),  run_time=0.3)
        self.wait(1.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 15 — Positive errors up, Negative errors down, then they cancel → 0
# ══════════════════════════════════════════════════════════════════════════════
class Anim15_ErrorsCancel(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Why Square the Errors?", font_size=30, color=HEADING)\
            .to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)

        np.random.seed(5)
        n = 12
        xs = np.linspace(0.8, 8.5, n)
        errors = np.array([0.9, -1.1, 0.6, -0.7, 1.3, -0.5,
                            0.8, -1.2, 0.4, -0.9, 1.1, -0.6])

        axes = Axes(
            x_range=[0, 9.5, 2], y_range=[-2.5, 2.5, 1],
            x_length=8.5, y_length=4.5,
            axis_config={"color": "#444a5a", "stroke_width": 2}, tips=False,
        ).shift(DOWN * 0.4)
        zero_line = axes.plot(lambda x: 0, x_range=[0, 9.5],
                              color="#444a5a", stroke_width=1.5, stroke_opacity=0.7)
        self.play(Create(axes), Create(zero_line), run_time=0.7)

        # Separate positive and negative — store (bar, x) tuples to keep xs aligned
        pos_bar_data = []   # list of (Arrow, x_position)
        neg_bar_data = []
        for x, e in zip(xs, errors):
            bar = Arrow(axes.c2p(x, 0), axes.c2p(x, e),
                        buff=0, stroke_width=3,
                        color=GREEN_G if e > 0 else RED_B,
                        max_tip_length_to_length_ratio=0.2)
            if e > 0:
                pos_bar_data.append((bar, x))
            else:
                neg_bar_data.append((bar, x))
        pos_bars = VGroup(*[b for b, _ in pos_bar_data])
        neg_bars = VGroup(*[b for b, _ in neg_bar_data])
        all_bar_data = pos_bar_data + neg_bar_data   # (bar, correct_x) pairs

        pos_label = Text("Positive errors  ↑", font_size=20, color=GREEN_G)\
            .move_to(LEFT * 3 + UP * 1.8)
        neg_label = Text("Negative errors  ↓", font_size=20, color=RED_B)\
            .move_to(RIGHT * 3 + DOWN * 1.8)

        self.play(
            LaggedStart(*[GrowArrow(b) for b in pos_bars], lag_ratio=0.1, run_time=1.0),
            FadeIn(pos_label),
        )
        self.play(
            LaggedStart(*[GrowArrow(b) for b in neg_bars], lag_ratio=0.1, run_time=1.0),
            FadeIn(neg_label),
        )
        self.wait(0.6)

        # Sum = ~0 demonstration
        sum_text = Text("Raw sum  ≈  0  →  looks like a perfect model! ✗",
                        font_size=22, color=YELLOW_R).to_edge(DOWN, buff=0.5)
        self.play(Write(sum_text), run_time=0.9)
        self.wait(0.7)

        # All bars collapse to zero — use correct x for each bar
        self.play(
            *[b.animate.put_start_and_end_on(
                axes.c2p(x, 0), axes.c2p(x, 0.001)
              ) for b, x in all_bar_data],
            run_time=1.2
        )

        fix = Text("Fix: square each error — all become positive",
                   font_size=22, color=GREEN_G).next_to(sum_text, UP, buff=0.3)
        self.play(Write(fix), run_time=0.9)
        self.wait(1.8)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 16 — Ball reaches minimum, "Global Minimum" marker appears
# ══════════════════════════════════════════════════════════════════════════════
class Anim16_GlobalMinimum(Scene):
    def construct(self):
        self.camera.background_color = BG

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[0, 9, 2],
            x_length=8.5, y_length=5.0,
            axis_config={"color": "#444a5a", "stroke_width": 2}, tips=False,
        ).shift(DOWN * 0.5)
        bowl = axes.plot(lambda x: x**2 + 0.4, x_range=[-2.85, 2.85],
                         color=BLUE_D, stroke_width=3.2)
        self.add(axes, bowl)

        # Ball already at minimum
        min_pt = axes.c2p(0, 0.4)
        ball = Dot(min_pt, color=YELLOW_R, radius=0.14)
        self.add(ball)

        # Animate marker appearing
        vline = DashedLine(min_pt, axes.c2p(0, 0),
                           color=ORANGE_L, stroke_width=1.8, dash_length=0.12)
        dot_marker = Dot(min_pt, color=ORANGE_L, radius=0.13)
        label = Text("Global Minimum\n(optimal β₁)", font_size=19, color=ORANGE_L)\
            .next_to(dot_marker, RIGHT + UP, buff=0.15)

        self.play(Create(vline), FadeIn(dot_marker, scale=1.6), run_time=0.7)
        self.play(Write(label), run_time=0.6)

        insight = Text("One unique minimum — no local traps.\nThis is the power of convexity.",
                       font_size=20, color=GREEN_G).to_edge(DOWN, buff=0.45)
        self.play(Write(insight), run_time=0.9)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 17 — Normal Equation appears + warning card about its limits
# ══════════════════════════════════════════════════════════════════════════════
class Anim17_NormalEquation(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Closed-Form Solution — The Normal Equation",
                     font_size=26, color=HEADING).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.7)

        formula = MathTex(
            r"\beta = (X^\top X)^{-1} X^\top y",
            font_size=64, color=YELLOW_R
        ).move_to(UP * 0.6)
        self.play(Write(formula), run_time=1.3)

        desc = Text("Exact analytical answer in one step — no iterations needed.",
                    font_size=21, color=MUTED).next_to(formula, DOWN, buff=0.45)
        self.play(FadeIn(desc, shift=DOWN * 0.1), run_time=0.7)
        self.wait(0.6)

        # Warning card
        warn_box = RoundedRectangle(corner_radius=0.15, width=9.5, height=2.1,
                                    fill_color="#1a1400", fill_opacity=1,
                                    stroke_color=YELLOW_R, stroke_width=2)\
            .next_to(desc, DOWN, buff=0.5)
        # Warning badge: yellow pill + "Limitations" text — no special Unicode chars
        warn_badge_bg = RoundedRectangle(
            corner_radius=0.08, width=0.52, height=0.38,
            fill_color=YELLOW_R, fill_opacity=1.0, stroke_width=0
        )
        warn_badge_txt = Text("!", font_size=16, color="#0d0f14", weight=BOLD)\
            .move_to(warn_badge_bg.get_center())
        warn_badge = VGroup(warn_badge_bg, warn_badge_txt)
        warn_label = Text("Limitations", font_size=19, color=YELLOW_R, weight=BOLD)
        warn_title = VGroup(warn_badge, warn_label)\
            .arrange(RIGHT, buff=0.18)\
            .next_to(warn_box.get_top(), DOWN, buff=0.22)
        warn_body = Text(
            "• Fails if X'X is singular  (multicollinearity or p > n)\n"
            "• O(p³) — matrix inversion slow with 10k+ features\n"
            "• Must hold full X'X (p×p) matrix in RAM\n"
            "• sklearn uses SVD, not direct inversion — numerically safer",
            font_size=15, color=MUTED
        ).next_to(warn_title, DOWN, buff=0.18)

        self.play(FadeIn(warn_box), run_time=0.5)
        self.play(Write(warn_title), Write(warn_body), run_time=0.9)
        self.wait(2.0)
