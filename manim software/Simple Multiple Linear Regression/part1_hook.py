from manim import *
import numpy as np

# ── Shared palette ─────────────────────────────────────────────────────────────
BLUE_D   = "#4f9eff"
ORANGE_L = "#f97316"
YELLOW_R = "#fbbf24"
GREEN_G  = "#10b981"
RED_B    = "#f87171"
BG       = "#0d0f14"
MUTED    = "#8892a4"
HEADING  = "#f8fafc"

np.random.seed(42)
RAW_X = np.linspace(1, 9, 28)
RAW_Y = np.clip(0.85 * RAW_X + 0.8 + np.random.normal(0, 0.55, 28), 0.5, 9.5)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 01 — Black screen, single dot appears, more dots, scatter plot forms
# ══════════════════════════════════════════════════════════════════════════════
class Anim01_DotsByOne(Scene):
    def construct(self):
        self.camera.background_color = BG

        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=9, y_length=5.5,
            axis_config={"color": "#333a4a", "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.3)

        dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.10, color=BLUE_D).set_opacity(0.85)
            for x, y in zip(RAW_X, RAW_Y)
        ])

        # Black screen hold
        self.wait(0.6)
        # Axes draw in
        self.play(Create(axes), run_time=1.0)
        # Dots appear one by one with stagger
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.3) for d in dots],
                        lag_ratio=0.09, run_time=3.5)
        )
        self.wait(1.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 02 — Use-case labels flash ("Bank", "Real Estate", "Healthcare")
#            then dissolve back to the scatter plot
# ══════════════════════════════════════════════════════════════════════════════
class Anim02_UseCaseLabels(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Background scatter (faded, stays throughout)
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=9, y_length=5.5,
            axis_config={"color": "#1e2230", "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.3)
        dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.09, color=BLUE_D).set_opacity(0.28)
            for x, y in zip(RAW_X, RAW_Y)
        ])
        self.add(axes, dots)

        use_cases = [
            ("🏦  Bank", BLUE_D,   "Predicts loan repayment risk"),
            ("🏠  Real Estate", ORANGE_L, "Prices houses before listing"),
            ("🏥  Healthcare", GREEN_G,  "Estimates hospital stay length"),
        ]

        for icon_text, color, sub in use_cases:
            big   = Text(icon_text, font_size=52, color=color, weight=BOLD)
            small = Text(sub, font_size=24, color=MUTED).next_to(big, DOWN, buff=0.25)
            grp   = VGroup(big, small).move_to(ORIGIN)

            self.play(FadeIn(grp, scale=1.15), run_time=0.55)
            self.wait(1.1)
            self.play(FadeOut(grp, scale=0.85), run_time=0.45)
            self.wait(0.2)

        # Dots brighten back
        self.play(dots.animate.set_opacity(0.85), run_time=0.7)
        self.wait(0.8)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 03 — Orange line draws itself through the scatter plot left → right
# ══════════════════════════════════════════════════════════════════════════════
class Anim03_LineDraws(Scene):
    def construct(self):
        self.camera.background_color = BG

        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=9, y_length=5.5,
            axis_config={"color": "#333a4a", "stroke_width": 2},
            tips=False,
        ).shift(DOWN * 0.3)
        dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.10, color=BLUE_D).set_opacity(0.85)
            for x, y in zip(RAW_X, RAW_Y)
        ])
        self.add(axes, dots)

        m, b = np.polyfit(RAW_X, RAW_Y, 1)
        reg_line = Line(
            axes.c2p(0.2, m * 0.2 + b),
            axes.c2p(9.8, m * 9.8 + b),
            color=ORANGE_L, stroke_width=3.5
        )
        label = Text("Best-fit Line (ŷ)", font_size=22, color=ORANGE_L)\
            .next_to(reg_line.get_end(), UP + LEFT, buff=0.15)

        self.play(Create(reg_line), run_time=2.0)
        self.play(FadeIn(label, shift=UP * 0.15), run_time=0.6)
        self.wait(1.5)
