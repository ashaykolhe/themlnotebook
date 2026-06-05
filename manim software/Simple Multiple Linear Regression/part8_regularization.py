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
# ANIM 32 — Good fit (smooth line) vs overfit (wiggly curve) side by side
# ══════════════════════════════════════════════════════════════════════════════
class Anim32_GoodFitVsOverfit(Scene):
    def construct(self):
        self.camera.background_color = BG
        np.random.seed(7)

        title = Text("The Overfitting Problem", font_size=28, color=HEADING)\
            .to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Shared data
        xs = np.linspace(0.5, 9, 8)
        ys = 0.7 * xs + 1.5 + np.random.normal(0, 0.5, 8)

        def make_ax(center):
            return Axes(x_range=[0, 10, 2], y_range=[0, 10, 2],
                        x_length=4.5, y_length=4.0,
                        axis_config={"color": "#3a4050", "stroke_width": 1.5},
                        tips=False).move_to(center)

        ax_l = make_ax(LEFT * 3.0 + DOWN * 0.4)
        ax_r = make_ax(RIGHT * 3.0 + DOWN * 0.4)

        ok_label  = Text("✅ Good fit — generalises", font_size=18, color=GREEN_G)\
            .next_to(ax_l, UP, buff=0.2)
        bad_label = Text("❌ Overfit — memorised noise", font_size=18, color=RED_B)\
            .next_to(ax_r, UP, buff=0.2)

        dots_l = VGroup(*[Dot(ax_l.c2p(x, y), radius=0.10, color=BLUE_D) for x, y in zip(xs, ys)])
        dots_r = VGroup(*[Dot(ax_r.c2p(x, y), radius=0.10, color=BLUE_D) for x, y in zip(xs, ys)])

        self.play(
            Create(ax_l), Create(ax_r),
            FadeIn(ok_label), FadeIn(bad_label),
            run_time=0.8
        )
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_l], lag_ratio=0.1, run_time=0.8),
            LaggedStart(*[FadeIn(d) for d in dots_r], lag_ratio=0.1, run_time=0.8),
        )

        # Good fit: straight OLS line
        m, b = np.polyfit(xs, ys, 1)
        good_line = Line(ax_l.c2p(0.3, m*0.3+b), ax_l.c2p(9.7, m*9.7+b),
                         color=GREEN_G, stroke_width=3)
        self.play(Create(good_line), run_time=0.9)

        # Overfit: high-degree polynomial passing through all 8 points
        poly_coeffs = np.polyfit(xs, ys, 7)
        poly_fn = np.poly1d(poly_coeffs)
        overfit_curve = ax_r.plot(
            lambda x: np.clip(poly_fn(x), 0.1, 9.9),
            x_range=[0.5, 9.0], color=RED_B, stroke_width=2.8
        )
        self.play(Create(overfit_curve), run_time=1.2)
        self.wait(0.5)

        caption = Text(
            "Overfit model: perfect on training data — fails completely on new data",
            font_size=18, color=RED_B
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(caption), run_time=0.9)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 33 — OLS cost formula shown, then λ penalty term fades in (Ridge)
# ══════════════════════════════════════════════════════════════════════════════
class Anim33_PenaltyTermAppears(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Regularisation — Adding a Penalty", font_size=28, color=HEADING)\
            .to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Plain OLS cost
        ols_cost = MathTex(
            r"\text{Cost}_{\text{OLS}} = \underbrace{\frac{1}{n}\sum(y_i - \hat{y}_i)^2}_{\text{MSE}}",
            font_size=44, color=HEADING
        ).move_to(UP * 0.8)
        self.play(Write(ols_cost), run_time=1.1)
        self.wait(0.5)

        # Arrow down
        arr = Arrow(ols_cost.get_bottom(), ols_cost.get_bottom() + DOWN * 0.6,
                    color=MUTED, buff=0, stroke_width=2,
                    max_tip_length_to_length_ratio=0.25)
        self.play(GrowArrow(arr), run_time=0.4)

        # Ridge cost with penalty appearing
        ridge_cost = MathTex(
            r"\text{Cost}_{\text{Ridge}} = ",
            r"\underbrace{\frac{1}{n}\sum(y_i - \hat{y}_i)^2}_{\text{MSE}}",
            r" + ",
            r"\underbrace{\lambda \sum_j \beta_j^2}_{\text{L2 Penalty}}",
            font_size=42
        ).next_to(arr, DOWN, buff=0.2)
        ridge_cost[0].set_color(HEADING)
        ridge_cost[1].set_color(HEADING)
        ridge_cost[2].set_color(HEADING)
        ridge_cost[3].set_color(RED_B)

        self.play(Write(ridge_cost[0]), Write(ridge_cost[1]), Write(ridge_cost[2]),
                  run_time=0.8)
        self.wait(0.3)
        # Penalty fades in dramatically
        self.play(FadeIn(ridge_cost[3], scale=1.3), run_time=0.8)

        # λ explanation
        lambda_box = SurroundingRectangle(ridge_cost[3], color=RED_B,
                                          corner_radius=0.1, buff=0.12)
        self.play(Create(lambda_box), run_time=0.4)

        ann = Text(
            "λ = 0  →  plain OLS     |     λ → ∞  →  all β → 0\n"
            "Larger λ = stronger shrinkage = less overfitting",
            font_size=19, color=RED_B
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(ann), run_time=0.9)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 34 — Ridge: circle constraint + MSE ellipses expanding and touching it
# ══════════════════════════════════════════════════════════════════════════════
class Anim34_RidgeGeometry(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Ridge (L2) — Circle Constraint", font_size=26, color=BLUE_D)\
            .to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=5.5, y_length=5.5,
            axis_config={"color": "#2d3748", "stroke_width": 1.5}, tips=False,
        ).shift(LEFT * 1.5)
        xl = Text("β₁", font_size=17, color=MUTED).next_to(axes, RIGHT, buff=0.08)
        yl = Text("β₂", font_size=17, color=MUTED).next_to(axes, UP, buff=0.08)
        self.play(Create(axes), Write(xl), Write(yl), run_time=0.8)

        # OLS optimum star
        ols_pt = axes.c2p(1.6, 1.4)
        ols_star = Star(n=5, outer_radius=0.16, inner_radius=0.08,
                        color=YELLOW_R, fill_opacity=1).move_to(ols_pt)
        ols_lbl = Text("OLS β*", font_size=14, color=YELLOW_R).next_to(ols_star, UR, buff=0.05)
        self.play(FadeIn(ols_star, scale=1.4), FadeIn(ols_lbl), run_time=0.6)

        # MSE ellipses expanding from OLS optimum
        ellipses = VGroup()
        for rx in [0.3, 0.6, 1.0, 1.5, 2.0]:
            ry = rx * 0.75
            cx, cy = 1.6, 1.4
            e = Ellipse(
                width=rx * axes.get_x_unit_size() * 2,
                height=ry * axes.get_y_unit_size() * 2,
                color="#3a5a7a", stroke_width=1.2, stroke_opacity=0.55
            ).move_to(axes.c2p(cx, cy))
            ellipses.add(e)

        self.play(
            LaggedStart(*[Create(e) for e in ellipses], lag_ratio=0.2, run_time=1.2)
        )

        # Ridge circle
        r_data = 1.5
        circle = Circle(
            radius=r_data * axes.get_x_unit_size(),
            color=BLUE_D, stroke_width=2.8,
            fill_color=BLUE_D, fill_opacity=0.08
        ).move_to(axes.c2p(0, 0))
        self.play(Create(circle), run_time=0.9)

        # Ridge solution point (where ellipse meets circle, off-axis)
        ridge_sol = axes.c2p(0.95, 1.12)
        ridge_dot = Dot(ridge_sol, color=GREEN_G, radius=0.13)
        ridge_lbl = Text("β̂ Ridge\n(both non-zero)", font_size=14, color=GREEN_G)\
            .next_to(ridge_dot, LEFT + DOWN, buff=0.1)
        self.play(FadeIn(ridge_dot, scale=1.5), Write(ridge_lbl), run_time=0.7)

        # Side annotation
        ann = VGroup(
            Text("Ridge shrinks all β toward 0", font_size=19, color=BLUE_D),
            Text("but NEVER exactly to 0", font_size=19, color=BLUE_D),
            Text("→ No feature selection", font_size=18, color=MUTED),
        ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.5)
        self.play(FadeIn(ann, shift=LEFT * 0.2), run_time=0.7)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 35 — Lasso: diamond constraint + ellipses touch corner → β₂ = 0
# ══════════════════════════════════════════════════════════════════════════════
class Anim35_LassoGeometry(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Lasso (L1) — Diamond Constraint", font_size=26, color=ORANGE_L)\
            .to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=5.5, y_length=5.5,
            axis_config={"color": "#2d3748", "stroke_width": 1.5}, tips=False,
        ).shift(LEFT * 1.5)
        xl = Text("β₁", font_size=17, color=MUTED).next_to(axes, RIGHT, buff=0.08)
        yl = Text("β₂", font_size=17, color=MUTED).next_to(axes, UP, buff=0.08)
        self.play(Create(axes), Write(xl), Write(yl), run_time=0.8)

        # OLS optimum
        ols_pt = axes.c2p(1.6, 1.4)
        ols_star = Star(n=5, outer_radius=0.16, inner_radius=0.08,
                        color=YELLOW_R, fill_opacity=1).move_to(ols_pt)
        ols_lbl = Text("OLS β*", font_size=14, color=YELLOW_R)\
            .next_to(ols_star, UR, buff=0.05)
        self.play(FadeIn(ols_star, scale=1.4), FadeIn(ols_lbl), run_time=0.6)

        # Expanding ellipses
        ellipses = VGroup()
        for rx in [0.3, 0.6, 1.0, 1.5, 2.0]:
            e = Ellipse(
                width=rx * axes.get_x_unit_size() * 2,
                height=rx * 0.75 * axes.get_y_unit_size() * 2,
                color="#3a5a7a", stroke_width=1.2, stroke_opacity=0.55
            ).move_to(axes.c2p(1.6, 1.4))
            ellipses.add(e)
        self.play(LaggedStart(*[Create(e) for e in ellipses], lag_ratio=0.2, run_time=1.2))

        # Lasso diamond
        r = 1.5
        diamond = Polygon(
            axes.c2p(0,  r), axes.c2p(r, 0),
            axes.c2p(0, -r), axes.c2p(-r, 0),
            color=ORANGE_L, stroke_width=2.8,
            fill_color=ORANGE_L, fill_opacity=0.08
        )
        self.play(Create(diamond), run_time=0.9)

        # Lasso solution: corner on β₁-axis (β₂ = 0)
        lasso_sol = axes.c2p(r, 0)
        lasso_dot = Dot(lasso_sol, color=GREEN_G, radius=0.13)
        lasso_lbl = Text("β̂ Lasso\nβ₂ = exactly 0 !", font_size=14, color=GREEN_G)\
            .next_to(lasso_dot, RIGHT + UP, buff=0.1)
        corner_ring = Circle(radius=0.23, color=RED_B, stroke_width=2.5)\
            .move_to(lasso_sol)

        self.play(FadeIn(lasso_dot, scale=1.5), Create(corner_ring),
                  Write(lasso_lbl), run_time=0.8)

        # Side annotation
        ann = VGroup(
            Text("Lasso drives some β", font_size=19, color=ORANGE_L),
            Text("to EXACTLY zero", font_size=19, color=ORANGE_L),
            Text("→ Built-in feature selection!", font_size=18, color=GREEN_G),
            Text("The diamond CORNERS are why.", font_size=16, color=MUTED),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 3.5)
        self.play(FadeIn(ann, shift=LEFT * 0.2), run_time=0.7)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 36 — Summary table: Ridge vs Lasso comparison
# ══════════════════════════════════════════════════════════════════════════════
class Anim36_RidgeLassoTable(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Ridge vs Lasso — When to Use Which",
                     font_size=26, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        headers = ["Property", "Ridge (L2)", "Lasso (L1)"]
        rows = [
            ["Penalty term",        "λ Σ bj²",    "λ Σ |bj|"],
            ["Zeros out features?", "No",           "Yes"],
            ["Feature selection?",  "No",           "Yes"],
            ["Handles correlated\nfeatures?", "Yes (shares weight)", "No (picks one)"],
            ["Use when…",           "All features\nmatter", "Few features\ntruly relevant"],
        ]

        col_w  = [3.6, 2.8, 2.8]
        row_h  = 0.72
        start_y = 1.8
        start_x = -sum(col_w) / 2

        # Header row
        for j, (txt, w) in enumerate(zip(headers, col_w)):
            color = [MUTED, BLUE_D, ORANGE_L][j]
            x = start_x + sum(col_w[:j]) + w / 2
            header_rect = Rectangle(width=w, height=row_h,
                                     fill_color="#1a1e2a", fill_opacity=1,
                                     stroke_color="#252a38", stroke_width=1.2)\
                .move_to([x, start_y, 0])
            header_text = Text(txt, font_size=18, color=color, weight=BOLD)\
                .move_to(header_rect.get_center())
            self.add(header_rect, header_text)

        self.play(FadeIn(Group(*self.mobjects[2:])), run_time=0.5)

        # Data rows animate in one by one
        for i, row in enumerate(rows):
            y = start_y - (i + 1) * row_h
            row_group = VGroup()
            for j, (txt, w) in enumerate(zip(row, col_w)):
                x = start_x + sum(col_w[:j]) + w / 2
                color = "#e2e8f0"
                if j == 1:   # Ridge column
                    color = GREEN_G if txt not in ["No", "No (picks one)"] else RED_B
                elif j == 2:  # Lasso column
                    if "Yes" in txt and "No" not in txt:
                        color = GREEN_G
                    elif txt in ["No (picks one)"]:
                        color = RED_B   # weakness: unstable with correlated features
                    elif txt == "Yes":
                        color = GREEN_G
                    else:
                        color = MUTED

                cell_rect = Rectangle(width=w, height=row_h,
                                       fill_color="#13161e" if i % 2 == 0 else "#0f1218",
                                       fill_opacity=1,
                                       stroke_color="#252a38", stroke_width=0.8)\
                    .move_to([x, y, 0])
                cell_text = Text(txt, font_size=15, color=color)\
                    .move_to(cell_rect.get_center())
                row_group.add(VGroup(cell_rect, cell_text))

            self.play(FadeIn(row_group, shift=RIGHT * 0.3), run_time=0.4)

        self.wait(2.0)
