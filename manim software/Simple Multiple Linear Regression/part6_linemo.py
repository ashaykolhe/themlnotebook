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

LETTER_COLORS = {
    "L": GREEN_G, "I": BLUE_D, "N": PURPLE,
    "E": YELLOW_R, "M": ORANGE_L, "O": RED_B,
}


def mini_ax(x_range, y_range, x_len=3.6, y_len=2.5):
    return Axes(x_range=x_range, y_range=y_range,
                x_length=x_len, y_length=y_len,
                axis_config={"color": "#3a4050", "stroke_width": 1.5},
                tips=False)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 21 — Letters L-I-N-E-M-O appear one by one in their colours
# ══════════════════════════════════════════════════════════════════════════════
class Anim21_LINEMOLetters(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("The 6 Assumptions of Linear Regression",
                     font_size=26, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.7)

        # Two rows of 3 — gives each label enough horizontal space
        # Row 1 (top):    L  I  N
        # Row 2 (bottom): E  M  O
        letters_and_names = [
            ("L", "Linearity"),
            ("I", "Independence"),
            ("N", "Normality of Residuals"),
            ("E", "Equal Variance"),
            ("M", "No Multicollinearity"),
            ("O", "No Outliers"),
        ]

        # x positions for 3 columns, y positions for 2 rows
        col_xs = [-4.2, 0.0, 4.2]
        row_ys = [1.0, -1.5]

        letter_mobs = []
        for i, (letter, name) in enumerate(letters_and_names):
            color   = LETTER_COLORS[letter]
            row     = i // 3
            col     = i  % 3
            big     = Text(letter, font_size=62, color=color, weight=BOLD)
            small   = Text(name,   font_size=18, color=MUTED)
            grp     = VGroup(big, small).arrange(DOWN, buff=0.20)
            grp.move_to([col_xs[col], row_ys[row], 0])
            letter_mobs.append(grp)

        self.play(
            LaggedStart(*[FadeIn(g, scale=0.6) for g in letter_mobs],
                        lag_ratio=0.18, run_time=2.5)
        )
        self.wait(1.5)

        # All letters pulse simultaneously
        self.play(
            *[g[0].animate.scale(1.25) for g in letter_mobs],
            run_time=0.4
        )
        self.play(
            *[g[0].animate.scale(1/1.25) for g in letter_mobs],
            run_time=0.4
        )
        self.wait(1.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 22 — L highlights + split screen: random residuals vs U-shape
# ══════════════════════════════════════════════════════════════════════════════
class Anim22_L_Linearity(Scene):
    def construct(self):
        self.camera.background_color = BG
        np.random.seed(1)

        badge = Text("L", font_size=48, color=GREEN_G, weight=BOLD).to_corner(UL, buff=0.4)
        name  = Text("— Linearity", font_size=28, color=HEADING)\
            .next_to(badge, RIGHT, buff=0.2).align_to(badge, DOWN)
        self.play(FadeIn(badge, scale=1.4), Write(name), run_time=0.7)

        div = Line(UP * 3, DOWN * 3, color="#2d3748", stroke_width=1.5)
        ok  = Text("✓ Holds — random residuals", font_size=17, color=GREEN_G)\
            .move_to(LEFT * 3.2 + UP * 2.5)
        bad = Text("✗ Violated — U-shape pattern", font_size=17, color=RED_B)\
            .move_to(RIGHT * 3.2 + UP * 2.5)
        self.play(Create(div), FadeIn(ok), FadeIn(bad), run_time=0.5)

        xs = np.linspace(1, 9, 14)
        ax_l = mini_ax([0, 10], [-3, 3]).move_to(LEFT * 3.2 + DOWN * 0.3)
        ax_r = mini_ax([0, 10], [-3, 3]).move_to(RIGHT * 3.2 + DOWN * 0.3)

        zero_l = ax_l.plot(lambda x: 0, x_range=[0, 10], color=BLUE_D, stroke_width=1.5)
        zero_r = ax_r.plot(lambda x: 0, x_range=[0, 10], color=BLUE_D, stroke_width=1.5)

        res_good = np.random.uniform(-1.8, 1.8, 14)
        res_bad  = -1.6 * np.sin(xs * 0.6) + np.random.uniform(-0.2, 0.2, 14)
        curve_bad = ax_r.plot(lambda x: -1.6 * np.sin(x * 0.6),
                              x_range=[0, 10], color=RED_B,
                              stroke_width=2.0, stroke_opacity=0.6)

        dots_l = VGroup(*[Dot(ax_l.c2p(x, r), radius=0.08, color=BLUE_D)
                          for x, r in zip(xs, res_good)])
        dots_r = VGroup(*[Dot(ax_r.c2p(x, r), radius=0.08, color=RED_B)
                          for x, r in zip(xs, res_bad)])

        self.play(Create(ax_l), Create(ax_r), Create(zero_l), Create(zero_r),
                  Create(curve_bad), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_l], lag_ratio=0.07, run_time=0.9),
            LaggedStart(*[FadeIn(d) for d in dots_r], lag_ratio=0.07, run_time=0.9),
        )

        # Axis labels — HTML Fig 4.1: "Residuals vs. Fitted plots"
        xl_l = Text("Fitted Values (ŷ)", font_size=12, color=MUTED).next_to(ax_l, DOWN, buff=0.12)
        yl_l = Text("Residuals", font_size=12, color=MUTED).next_to(ax_l, LEFT, buff=0.08).rotate(PI/2)
        xl_r = Text("Fitted Values (ŷ)", font_size=12, color=MUTED).next_to(ax_r, DOWN, buff=0.12)
        yl_r = Text("Residuals", font_size=12, color=MUTED).next_to(ax_r, LEFT, buff=0.08).rotate(PI/2)
        self.play(FadeIn(xl_l), FadeIn(yl_l), FadeIn(xl_r), FadeIn(yl_r), run_time=0.4)

        fix = Text("Fix: add polynomial features or log-transform X",
                   font_size=16, color=YELLOW_R).to_edge(DOWN, buff=0.4)
        self.play(Write(fix), run_time=0.7)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 23 — I highlights + independence timelines (random vs autocorrelated)
# ══════════════════════════════════════════════════════════════════════════════
class Anim23_I_Independence(Scene):
    def construct(self):
        self.camera.background_color = BG
        np.random.seed(2)

        badge = Text("I", font_size=48, color=BLUE_D, weight=BOLD).to_corner(UL, buff=0.4)
        name  = Text("— Independence", font_size=28, color=HEADING)\
            .next_to(badge, RIGHT, buff=0.2).align_to(badge, DOWN)
        self.play(FadeIn(badge, scale=1.4), Write(name), run_time=0.7)

        div = Line(UP * 3, DOWN * 3, color="#2d3748", stroke_width=1.5)
        ok  = Text("✓ Independent observations", font_size=17, color=GREEN_G)\
            .move_to(LEFT * 3.2 + UP * 2.5)
        bad = Text("✗ Autocorrelated (time-series)", font_size=17, color=RED_B)\
            .move_to(RIGHT * 3.2 + UP * 2.5)
        self.play(Create(div), FadeIn(ok), FadeIn(bad), run_time=0.5)

        xs = np.linspace(0, 20, 20)
        ax_l = mini_ax([0, 20], [-3, 3]).move_to(LEFT * 3.2 + DOWN * 0.3)
        ax_r = mini_ax([0, 20], [-3, 3]).move_to(RIGHT * 3.2 + DOWN * 0.3)

        zero_l = ax_l.plot(lambda x: 0, x_range=[0, 20], color="#3a4050", stroke_width=1.2)
        res_indep = np.random.normal(0, 1.2, 20)
        res_auto  = 1.8 * np.sin(xs * 0.7)
        wave = ax_r.plot(lambda x: 1.8 * np.sin(x * 0.7),
                         x_range=[0, 20], color=RED_B, stroke_width=2)

        dots_l = VGroup(*[Dot(ax_l.c2p(x, r), radius=0.08, color=BLUE_D)
                          for x, r in zip(xs, res_indep)])
        dots_r = VGroup(*[Dot(ax_r.c2p(x, r), radius=0.08, color=RED_B)
                          for x, r in zip(xs, res_auto + np.random.normal(0, 0.2, 20))])

        self.play(Create(ax_l), Create(ax_r), Create(zero_l), Create(wave), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_l], lag_ratio=0.05, run_time=0.9),
            LaggedStart(*[FadeIn(d) for d in dots_r], lag_ratio=0.05, run_time=0.9),
        )
        fix = Text("Fix: use time-series models (ARIMA, etc.)",
                   font_size=16, color=YELLOW_R).to_edge(DOWN, buff=0.4)
        self.play(Write(fix), run_time=0.7)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 24 — N highlights + normality histograms (bell vs skewed)
# ══════════════════════════════════════════════════════════════════════════════
class Anim24_N_Normality(Scene):
    def construct(self):
        self.camera.background_color = BG
        np.random.seed(3)

        badge = Text("N", font_size=48, color=PURPLE, weight=BOLD).to_corner(UL, buff=0.4)
        name  = Text("— Normality of Residuals", font_size=28, color=HEADING)\
            .next_to(badge, RIGHT, buff=0.2).align_to(badge, DOWN)
        self.play(FadeIn(badge, scale=1.4), Write(name), run_time=0.7)

        div = Line(UP * 3, DOWN * 3, color="#2d3748", stroke_width=1.5)
        ok  = Text("✓ Normal (bell curve)", font_size=17, color=GREEN_G)\
            .move_to(LEFT * 3.2 + UP * 2.5)
        bad = Text("✗ Skewed / heavy-tailed", font_size=17, color=RED_B)\
            .move_to(RIGHT * 3.2 + UP * 2.5)
        self.play(Create(div), FadeIn(ok), FadeIn(bad), run_time=0.5)

        ax_l = mini_ax([0, 10], [0, 6]).move_to(LEFT * 3.2 + DOWN * 0.3)
        ax_r = mini_ax([0, 10], [0, 6]).move_to(RIGHT * 3.2 + DOWN * 0.3)
        self.play(Create(ax_l), Create(ax_r), run_time=0.6)

        # Axis labels — critical: HTML says this is about RESIDUALS not raw data
        xl_l = Text("Residuals (ε)", font_size=12, color=MUTED).next_to(ax_l, DOWN, buff=0.12)
        xl_r = Text("Residuals (ε)", font_size=12, color=MUTED).next_to(ax_r, DOWN, buff=0.12)
        note = Text("This assumption is about RESIDUALS — not raw data or features!",
                    font_size=15, color=YELLOW_R).to_edge(DOWN, buff=0.65)
        self.play(FadeIn(xl_l), FadeIn(xl_r), Write(note), run_time=0.6)

        bins = np.linspace(1, 9, 16)
        norm_vals = np.random.normal(5, 1.1, 600)
        skew_vals = np.clip(np.random.exponential(1.1, 600) + 0.5, 0, 9)

        def make_bars(axes_obj, vals, color):
            counts, _ = np.histogram(vals, bins=bins)
            bars = VGroup()
            for lo, hi, c in zip(bins, bins[1:], counts):
                h = c / 60 * axes_obj.get_y_unit_size()
                w = (hi - lo) * axes_obj.get_x_unit_size() * 0.88
                bar = Rectangle(width=w, height=max(h, 0.01),
                                 fill_color=color, fill_opacity=0.75, stroke_width=0)\
                    .align_to(axes_obj.c2p(lo, 0), DOWN + LEFT)
                bars.add(bar)
            return bars

        bars_l = make_bars(ax_l, norm_vals, BLUE_D)
        bars_r = make_bars(ax_r, skew_vals, RED_B)

        self.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_l], lag_ratio=0.04, run_time=1.1),
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_r], lag_ratio=0.04, run_time=1.1),
        )
        fix = Text("Fix: log-transform skewed features or target",
                   font_size=16, color=YELLOW_R).to_edge(DOWN, buff=0.4)
        self.play(Write(fix), run_time=0.7)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 25 — E highlights + homoscedasticity: uniform spread vs fan shape
# ══════════════════════════════════════════════════════════════════════════════
class Anim25_E_EqualVariance(Scene):
    def construct(self):
        self.camera.background_color = BG
        np.random.seed(4)

        badge = Text("E", font_size=48, color=YELLOW_R, weight=BOLD).to_corner(UL, buff=0.4)
        name  = Text("— Equal Variance (Homoscedasticity)", font_size=26, color=HEADING)\
            .next_to(badge, RIGHT, buff=0.2).align_to(badge, DOWN)
        self.play(FadeIn(badge, scale=1.4), Write(name), run_time=0.7)

        div = Line(UP * 3, DOWN * 3, color="#2d3748", stroke_width=1.5)
        ok  = Text("✓ Constant spread", font_size=17, color=GREEN_G)\
            .move_to(LEFT * 3.2 + UP * 2.5)
        bad = Text("✗ Fan shape (heteroscedasticity)", font_size=17, color=RED_B)\
            .move_to(RIGHT * 3.2 + UP * 2.5)
        self.play(Create(div), FadeIn(ok), FadeIn(bad), run_time=0.5)

        xs = np.linspace(1, 9, 20)
        ax_l = mini_ax([0, 10], [-3, 3]).move_to(LEFT * 3.2 + DOWN * 0.3)
        ax_r = mini_ax([0, 10], [-4, 4]).move_to(RIGHT * 3.2 + DOWN * 0.3)

        zero_l = ax_l.plot(lambda x: 0, x_range=[0, 10], color="#3a4050", stroke_width=1.2)
        zero_r = ax_r.plot(lambda x: 0, x_range=[0, 10], color="#3a4050", stroke_width=1.2)

        spread = np.linspace(0.2, 2.8, 20)
        dots_l = VGroup(*[Dot(ax_l.c2p(x, r), radius=0.08, color=BLUE_D)
                          for x, r in zip(xs, np.random.uniform(-1.4, 1.4, 20))])
        dots_r = VGroup(*[Dot(ax_r.c2p(x, r), radius=0.08, color=RED_B)
                          for x, r in zip(xs, np.random.uniform(-1, 1, 20) * spread)])

        fan_top = ax_r.plot(lambda x: 0.28 * x, x_range=[1, 9],
                            color=RED_B, stroke_width=1.5, stroke_opacity=0.5)
        fan_bot = ax_r.plot(lambda x: -0.28 * x, x_range=[1, 9],
                            color=RED_B, stroke_width=1.5, stroke_opacity=0.5)

        self.play(Create(ax_l), Create(ax_r), Create(zero_l), Create(zero_r),
                  Create(fan_top), Create(fan_bot), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_l], lag_ratio=0.05, run_time=0.9),
            LaggedStart(*[FadeIn(d) for d in dots_r], lag_ratio=0.05, run_time=0.9),
        )
        fix = Text("Fix: log-transform the target variable",
                   font_size=16, color=YELLOW_R).to_edge(DOWN, buff=0.4)
        self.play(Write(fix), run_time=0.7)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 26 — M highlights + correlation heatmap (2 highly correlated features)
# ══════════════════════════════════════════════════════════════════════════════
class Anim26_M_Multicollinearity(Scene):
    def construct(self):
        self.camera.background_color = BG

        badge = Text("M", font_size=48, color=ORANGE_L, weight=BOLD).to_corner(UL, buff=0.4)
        name  = Text("— No Multicollinearity", font_size=28, color=HEADING)\
            .next_to(badge, RIGHT, buff=0.2).align_to(badge, DOWN)
        self.play(FadeIn(badge, scale=1.4), Write(name), run_time=0.7)

        # Correlation matrix as coloured grid
        features = ["Size", "Rooms", "Age", "Price/m²", "Dist"]
        n = len(features)
        corr = np.array([
            [1.0,  0.82, -0.3,  0.91,  -0.2],
            [0.82, 1.0,  -0.2,  0.78,  -0.15],
            [-0.3, -0.2,  1.0, -0.25,   0.4],
            [0.91, 0.78, -0.25, 1.0,   -0.18],
            [-0.2, -0.15, 0.4, -0.18,   1.0],
        ])

        cell_size = 0.82
        grid = VGroup()
        labels_top  = VGroup()
        labels_left = VGroup()

        for i in range(n):
            for j in range(n):
                v = corr[i, j]
                # Colour: red for high positive, blue for negative, grey for ~0
                if abs(v) > 0.7 and i != j:
                    col = RED_B
                    opacity = 0.85
                elif v > 0.4:
                    col = ORANGE_L
                    opacity = 0.6
                elif v < -0.2:
                    col = BLUE_D
                    opacity = 0.5
                else:
                    col = "#3a4050"
                    opacity = 0.4

                rect = Square(side_length=cell_size,
                              fill_color=col, fill_opacity=opacity,
                              stroke_color="#1a1e2a", stroke_width=0.8)\
                    .move_to([j * cell_size - (n-1)*cell_size/2,
                               -i * cell_size + (n-1)*cell_size/2 - 0.3, 0])
                val_text = Text(f"{v:.2f}", font_size=12,
                                color=WHITE if opacity > 0.55 else MUTED)\
                    .move_to(rect.get_center())
                grid.add(VGroup(rect, val_text))

            # Labels
            labels_top.add(Text(features[i], font_size=13, color=MUTED)
                           .move_to([i * cell_size - (n-1)*cell_size/2,
                                     (n-1)*cell_size/2 + 0.5 - 0.3, 0]))
            labels_left.add(Text(features[i], font_size=13, color=MUTED)
                            .move_to([-(n-1)*cell_size/2 - 0.6,
                                      -i * cell_size + (n-1)*cell_size/2 - 0.3, 0]))

        self.play(
            LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.03, run_time=1.4),
            FadeIn(labels_top), FadeIn(labels_left),
        )

        # Highlight the two high-correlation cells
        hi_cells = [grid[0*n+1], grid[0*n+3], grid[1*n+3]]
        rings = VGroup(*[
            SurroundingRectangle(c, color=RED_B, stroke_width=2.5, buff=0.02)
            for c in hi_cells
        ])
        self.play(Create(rings), run_time=0.6)

        warn = Text("VIF > 10  →  serious multicollinearity\nFix: Ridge regression or remove one feature",
                    font_size=17, color=YELLOW_R).to_edge(DOWN, buff=0.4)
        self.play(Write(warn), run_time=0.8)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 27 — O highlights + outlier pulling the regression line toward it
# ══════════════════════════════════════════════════════════════════════════════
class Anim27_O_Outliers(Scene):
    def construct(self):
        self.camera.background_color = BG
        np.random.seed(6)

        badge = Text("O", font_size=48, color=RED_B, weight=BOLD).to_corner(UL, buff=0.4)
        name  = Text("— No Outliers", font_size=28, color=HEADING)\
            .next_to(badge, RIGHT, buff=0.2).align_to(badge, DOWN)
        self.play(FadeIn(badge, scale=1.4), Write(name), run_time=0.7)

        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=8.5, y_length=4.8,
            axis_config={"color": "#444a5a", "stroke_width": 2}, tips=False,
        ).shift(DOWN * 0.5)
        self.play(Create(axes), run_time=0.6)

        base_x = np.array([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7])
        base_y = 0.75 * base_x + 1 + np.random.normal(0, 0.35, len(base_x))

        dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.10, color=BLUE_D)
                        for x, y in zip(base_x, base_y)])
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.08, run_time=1.0))

        # Clean line
        m_clean, b_clean = np.polyfit(base_x, base_y, 1)
        clean_line = Line(axes.c2p(0.5, m_clean*0.5+b_clean),
                          axes.c2p(8.0, m_clean*8.0+b_clean),
                          color=GREEN_G, stroke_width=3)
        clean_lbl = Text("Without outlier", font_size=18, color=GREEN_G)\
            .next_to(clean_line.get_end(), RIGHT, buff=0.1)
        self.play(Create(clean_line), FadeIn(clean_lbl), run_time=0.8)
        self.wait(0.5)

        # Outlier appears
        out_x, out_y = 9.0, 0.8
        out_dot = Dot(axes.c2p(out_x, out_y), radius=0.15, color=RED_B)
        out_ring = Circle(radius=0.24, color=RED_B, stroke_width=2.5)\
            .move_to(axes.c2p(out_x, out_y))
        out_lbl = Text("Outlier!", font_size=18, color=RED_B)\
            .next_to(axes.c2p(out_x, out_y), UP, buff=0.2)
        self.play(FadeIn(out_dot, scale=1.6), Create(out_ring),
                  FadeIn(out_lbl), run_time=0.7)
        self.wait(0.4)

        # Pulled line
        all_x = np.append(base_x, out_x)
        all_y = np.append(base_y, out_y)
        m_pull, b_pull = np.polyfit(all_x, all_y, 1)
        pulled_line = Line(axes.c2p(0.5, m_pull*0.5+b_pull),
                           axes.c2p(9.5, m_pull*9.5+b_pull),
                           color=RED_B, stroke_width=3)
        pull_lbl = Text("Pulled by outlier", font_size=18, color=RED_B)\
            .next_to(pulled_line.get_center(), UP, buff=0.15)

        self.play(Transform(clean_line, pulled_line),
                  Transform(clean_lbl, pull_lbl), run_time=1.2)
        self.wait(1.5)

        fix = Text("Fix: investigate, cap, or use robust regression (HuberRegressor)",
                   font_size=16, color=YELLOW_R).to_edge(DOWN, buff=0.3)
        self.play(Write(fix), run_time=0.8)
        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 28 — All six LINE-MO letters glow simultaneously
# ══════════════════════════════════════════════════════════════════════════════
class Anim28_LINEMOGlow(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Your Pre-Flight Checklist", font_size=28, color=HEADING)\
            .to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)

        letters_names = [
            ("L", "Linearity"),
            ("I", "Independence"),
            ("N", "Normality"),
            ("E", "Equal Variance"),
            ("M", "No Multicollinearity"),
            ("O", "No Outliers"),
        ]

        # Two rows of 3 — same layout as Anim21 for visual consistency
        col_xs = [-4.2, 0.0, 4.2]
        row_ys = [0.8, -1.4]

        letter_groups = []
        for i, (letter, name) in enumerate(letters_names):
            color = LETTER_COLORS[letter]
            row   = i // 3
            col   = i  % 3
            big   = Text(letter, font_size=62, color=color, weight=BOLD)
            small = Text(name,   font_size=18, color=MUTED)
            grp   = VGroup(big, small).arrange(DOWN, buff=0.15)
            grp.move_to([col_xs[col], row_ys[row], 0])
            letter_groups.append(grp)

        self.play(
            LaggedStart(*[FadeIn(g, scale=0.7) for g in letter_groups],
                        lag_ratio=0.12, run_time=2.0)
        )
        self.wait(0.4)

        # All glow: scale up then back down simultaneously
        for _ in range(2):
            self.play(
                *[g[0].animate.scale(1.3).set_color(WHITE)
                  for g in letter_groups],
                run_time=0.35
            )
            self.play(
                *[g[0].animate.scale(1/1.3).set_color(LETTER_COLORS[g[0].text])
                  for g in letter_groups],
                run_time=0.35
            )
        self.wait(1.5)
