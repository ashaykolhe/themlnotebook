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

np.random.seed(42)
RAW_X = np.linspace(1, 9, 22)
RAW_Y = np.clip(0.85 * RAW_X + 0.8 + np.random.normal(0, 0.55, 22), 0.5, 9.5)
M_OLS, B_OLS = np.polyfit(RAW_X, RAW_Y, 1)


def make_axes():
    ax = Axes(
        x_range=[0, 10, 2], y_range=[0, 10, 2],
        x_length=9, y_length=5.5,
        axis_config={"color": "#333a4a", "stroke_width": 2},
        tips=False,
    ).shift(DOWN * 0.3)
    xl = Text("House Size (sq ft)", font_size=20, color=MUTED).next_to(ax, DOWN, buff=0.25)
    yl = Text("Price (₹)", font_size=20, color=MUTED).next_to(ax, LEFT, buff=0.2).rotate(PI/2)
    return ax, xl, yl


def make_dots(ax):
    return VGroup(*[
        Dot(ax.c2p(x, y), radius=0.10, color=BLUE_D).set_opacity(0.85)
        for x, y in zip(RAW_X, RAW_Y)
    ])


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 04 — Axes appear, dots scatter in upward trend
# ══════════════════════════════════════════════════════════════════════════════
class Anim04_AxesAndDots(Scene):
    def construct(self):
        self.camera.background_color = BG
        ax, xl, yl = make_axes()
        dots = make_dots(ax)

        self.play(Create(ax), Write(xl), Write(yl), run_time=1.1)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.4) for d in dots],
                        lag_ratio=0.07, run_time=2.5)
        )

        caption = Text("Each dot = one house sale", font_size=22, color=MUTED)\
            .to_edge(UP, buff=0.4)
        self.play(FadeIn(caption), run_time=0.6)
        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 05 — Line sweeps different angles (tilts up, tilts down) then settles
# ══════════════════════════════════════════════════════════════════════════════
class Anim05_LineSweeps(Scene):
    def construct(self):
        self.camera.background_color = BG
        ax, xl, yl = make_axes()
        dots = make_dots(ax)
        self.add(ax, xl, yl, dots)

        # We animate slope by morphing the line endpoints using a ValueTracker
        slope_tracker = ValueTracker(-0.8)   # start with wrong negative slope

        def get_line():
            s = slope_tracker.get_value()
            # intercept chosen so line always passes through centre of plot
            mid_x = 5.0
            mid_y = M_OLS * mid_x + B_OLS   # anchor near real centre
            b_cur = mid_y - s * mid_x
            return Line(
                ax.c2p(0.3,  s * 0.3  + b_cur),
                ax.c2p(9.7,  s * 9.7  + b_cur),
                color=ORANGE_L, stroke_width=3.2
            )

        line = always_redraw(get_line)
        self.add(line)
        self.wait(0.3)

        # Sweep: wrong negative → too steep positive → settle on OLS slope
        self.play(slope_tracker.animate.set_value(2.0),
                  rate_func=rate_functions.ease_in_out_sine, run_time=1.4)
        self.play(slope_tracker.animate.set_value(0.3),
                  rate_func=rate_functions.ease_in_out_sine, run_time=1.0)
        self.play(slope_tracker.animate.set_value(M_OLS),
                  rate_func=rate_functions.ease_in_out_sine, run_time=1.2)

        settle_label = Text("Best-fit line settles here", font_size=21, color=ORANGE_L)\
            .to_edge(UP, buff=0.4)
        self.play(FadeIn(settle_label), run_time=0.6)
        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 06 — Residual dashes appear from each dot to the line
# ══════════════════════════════════════════════════════════════════════════════
class Anim06_ResidualDashes(Scene):
    def construct(self):
        self.camera.background_color = BG
        ax, xl, yl = make_axes()
        dots = make_dots(ax)
        reg_line = Line(
            ax.c2p(0.2, M_OLS * 0.2 + B_OLS),
            ax.c2p(9.8, M_OLS * 9.8 + B_OLS),
            color=ORANGE_L, stroke_width=3.2
        )
        self.add(ax, xl, yl, dots, reg_line)

        residuals = VGroup(*[
            DashedLine(
                ax.c2p(x, y),
                ax.c2p(x, M_OLS * x + B_OLS),
                color=YELLOW_R, stroke_width=2.0, dash_length=0.09
            )
            for x, y in zip(RAW_X, RAW_Y)
        ])

        # Label one residual in the middle
        mid = len(RAW_X) // 2
        res_label = Text("residual", font_size=18, color=YELLOW_R)\
            .next_to(ax.c2p(RAW_X[mid] + 0.4,
                            (RAW_Y[mid] + M_OLS * RAW_X[mid] + B_OLS) / 2), RIGHT, buff=0.05)

        self.play(
            LaggedStart(*[Create(r) for r in residuals],
                        lag_ratio=0.06, run_time=2.0)
        )
        self.play(FadeIn(res_label), run_time=0.5)

        formula = Text("Residual = Actual y  −  Predicted ŷ", font_size=22, color=YELLOW_R)\
            .to_edge(UP, buff=0.4)
        self.play(Write(formula), run_time=1.0)
        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 07 — Residuals glow yellow → shrink as line settles → "Best-fit Line"
# ══════════════════════════════════════════════════════════════════════════════
class Anim07_ResidualsShrink(Scene):
    def construct(self):
        self.camera.background_color = BG
        ax, xl, yl = make_axes()
        dots = make_dots(ax)

        # Start with a slightly wrong line
        m_bad, b_bad = M_OLS - 0.25, B_OLS + 0.8

        def make_residuals(slope, intercept, color=YELLOW_R, opacity=1.0):
            return VGroup(*[
                DashedLine(
                    ax.c2p(x, y),
                    ax.c2p(x, slope * x + intercept),
                    color=color, stroke_width=2.0,
                    dash_length=0.09, stroke_opacity=opacity
                )
                for x, y in zip(RAW_X, RAW_Y)
            ])

        bad_line = Line(ax.c2p(0.2, m_bad * 0.2 + b_bad),
                        ax.c2p(9.8, m_bad * 9.8 + b_bad),
                        color=ORANGE_L, stroke_width=3.2)
        bad_res  = make_residuals(m_bad, b_bad)

        self.add(ax, xl, yl, dots, bad_line)
        self.play(
            LaggedStart(*[Create(r) for r in bad_res], lag_ratio=0.05, run_time=1.2)
        )
        self.wait(0.4)

        # Glow
        self.play(bad_res.animate.set_color(WHITE), run_time=0.4)
        self.play(bad_res.animate.set_color(YELLOW_R), run_time=0.4)

        # Morph line to optimal + residuals shrink
        good_line = Line(ax.c2p(0.2, M_OLS * 0.2 + B_OLS),
                         ax.c2p(9.8, M_OLS * 9.8 + B_OLS),
                         color=ORANGE_L, stroke_width=3.2)
        good_res  = make_residuals(M_OLS, B_OLS)

        self.play(
            Transform(bad_line, good_line),
            Transform(bad_res,  good_res),
            run_time=1.8, rate_func=rate_functions.ease_in_out_sine
        )

        label = Text("Best-fit Line", font_size=24, color=GREEN_G)\
            .to_edge(UP, buff=0.4)
        self.play(FadeIn(label, scale=1.2), run_time=0.7)
        self.wait(1.5)
