"""
Polynomial Regression — Complete YouTube Video
Single Manim class: PolynomialRegressionVideo

Render with:
    manim -pqh polynomial_regression_video.py PolynomialRegressionVideo

Requirements:
    pip install manim
    # Windows users: ensure LaTeX (MiKTeX) is installed for MathTex
"""

from manim import *
import numpy as np

# ─────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────
BG       = "#0d0f14"
BLUE_H   = "#4f9eff"
ORANGE_H = "#f97316"
GREEN_H  = "#10b981"
YELLOW_H = "#fbbf24"
RED_H    = "#f87171"
PURPLE_H = "#a855f7"
WHITE_H  = "#FFFFFF"
GRAY_H   = "#8899aa"
DARK_GR  = "#0a2a18"
DARK_RD  = "#2a0a0a"


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def make_subtitle(text, width=11.5):
    """Create a subtitle bar at the bottom of the screen."""
    bg = Rectangle(
        width=width,
        height=0.55,
        fill_color=BLACK,
        fill_opacity=0.92,
        stroke_width=0,
    ).to_edge(DOWN, buff=0.12)
    label = Text(
        text,
        font_size=18,
        color=WHITE,
    ).move_to(bg.get_center())
    if label.width > width - 0.3:
        label.scale((width - 0.3) / label.width)
    return VGroup(bg, label)


def make_section_title(text, color=BLUE_H, font_size=40):
    """Large section title for the top of the screen."""
    return Text(text, font_size=font_size, color=color).to_edge(UP, buff=0.35)


def make_card(title, lines, card_w=3.0, card_h=2.2,
              title_color=BLUE_H, bg_color="#111a2e", border_color=None):
    """Generic info card with a title and bullet lines."""
    if border_color is None:
        border_color = title_color
    box = RoundedRectangle(
        width=card_w, height=card_h,
        corner_radius=0.12,
        fill_color=bg_color,
        fill_opacity=1,
        stroke_color=border_color,
        stroke_width=1.5,
    )
    t_obj = Text(title, font_size=18, color=title_color, weight=BOLD)
    t_obj.next_to(box.get_top(), DOWN, buff=0.18)
    if t_obj.width > card_w - 0.2:
        t_obj.scale((card_w - 0.2) / t_obj.width)
    items = VGroup()
    for line in lines:
        item = Text(line, font_size=14, color=WHITE_H)
        item.set_opacity(0.9)
        if item.width > card_w - 0.25:
            item.scale((card_w - 0.25) / item.width)
        items.add(item)
    items.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    items.next_to(t_obj, DOWN, buff=0.15)
    if items.get_bottom()[1] < box.get_bottom()[1] + 0.1:
        scale_f = (box.height - t_obj.height - 0.45) / items.height
        if scale_f < 1:
            items.scale(scale_f)
        items.next_to(t_obj, DOWN, buff=0.12)
    return VGroup(box, t_obj, items)


def make_pros_cons(pros, cons, width=5.5, height=3.4):
    """Split-screen green/red pros-cons panel."""
    pro_box = RoundedRectangle(
        width=width, height=height,
        corner_radius=0.12,
        fill_color=DARK_GR,
        fill_opacity=1,
        stroke_color=GREEN_H,
        stroke_width=2,
    )
    con_box = RoundedRectangle(
        width=width, height=height,
        corner_radius=0.12,
        fill_color=DARK_RD,
        fill_opacity=1,
        stroke_color=RED_H,
        stroke_width=2,
    )

    def fill_box(box, title, items, t_color):
        t_obj = Text(title, font_size=20, color=t_color, weight=BOLD)
        t_obj.next_to(box.get_top(), DOWN, buff=0.18)
        if t_obj.width > width - 0.2:
            t_obj.scale((width - 0.2) / t_obj.width)
        lines = VGroup()
        for item in items:
            bullet = Text("• " + item, font_size=14, color=WHITE_H)
            bullet.set_opacity(0.9)
            if bullet.width > width - 0.28:
                bullet.scale((width - 0.28) / bullet.width)
            lines.add(bullet)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        lines.next_to(t_obj, DOWN, buff=0.12)
        if lines.get_bottom()[1] < box.get_bottom()[1] + 0.1:
            scale_f = (box.height - t_obj.height - 0.45) / lines.height
            if 0 < scale_f < 1:
                lines.scale(scale_f)
            lines.next_to(t_obj, DOWN, buff=0.1)
        return VGroup(t_obj, lines)

    pro_content = fill_box(pro_box, "Pros", pros, GREEN_H)
    con_content = fill_box(con_box, "Cons", cons, RED_H)

    pro_grp = VGroup(pro_box, pro_content)
    con_grp = VGroup(con_box, con_content)
    pro_grp.shift(LEFT * (width / 2 + 0.15))
    con_grp.shift(RIGHT * (width / 2 + 0.15))
    return VGroup(pro_grp, con_grp)


def make_formula_box(formula_mob, label_text="", width=8.5, height=1.35):
    """Cream-style formula box with optional label."""
    box = RoundedRectangle(
        width=width, height=height,
        corner_radius=0.12,
        fill_color="#1a1f2e",
        fill_opacity=1,
        stroke_color=BLUE_H,
        stroke_width=1.8,
    )
    formula_mob.move_to(box.get_center())
    if formula_mob.width > width - 0.4:
        formula_mob.scale((width - 0.4) / formula_mob.width)
    result = VGroup(box, formula_mob)
    if label_text:
        lbl = Text(label_text, font_size=13, color=GRAY_H)
        lbl.next_to(box, DOWN, buff=0.1)
        if lbl.width > width - 0.2:
            lbl.scale((width - 0.2) / lbl.width)
        result.add(lbl)
    return result


def make_table_mob(headers, rows, col_widths=None, font_size=13):
    """Create a simple aligned table as a VGroup."""
    n_cols = len(headers)
    if col_widths is None:
        col_widths = [10.0 / n_cols] * n_cols

    def clip(text, max_w, fs):
        t = Text(text, font_size=fs, color=WHITE_H)
        if t.width > max_w - 0.12:
            t.scale((max_w - 0.12) / t.width)
        return t

    all_rows = []
    # Header
    hdr_cells = []
    for i, h in enumerate(headers):
        cell = clip(h, col_widths[i], font_size)
        cell.set_color(YELLOW_H)
        hdr_cells.append(cell)
    all_rows.append(hdr_cells)

    for row in rows:
        cells = []
        for i, val in enumerate(row):
            cells.append(clip(str(val), col_widths[i], font_size))
        all_rows.append(cells)

    # Layout
    row_h = 0.38
    result = VGroup()
    for r_idx, row_cells in enumerate(all_rows):
        x_cursor = 0
        for c_idx, cell in enumerate(row_cells):
            cell.move_to(
                RIGHT * (x_cursor + col_widths[c_idx] / 2 - sum(col_widths) / 2)
                + DOWN * r_idx * row_h
            )
            result.add(cell)
            x_cursor += col_widths[c_idx]

        # Row separator (skip last row)
        if r_idx < len(all_rows) - 1:
            sep = Line(
                LEFT * sum(col_widths) / 2,
                RIGHT * sum(col_widths) / 2,
                stroke_width=0.6,
                color=GRAY_H,
            ).shift(DOWN * (r_idx * row_h + row_h / 2))
            result.add(sep)

    # Header underline
    hl = Line(
        LEFT * sum(col_widths) / 2,
        RIGHT * sum(col_widths) / 2,
        stroke_width=1.5,
        color=YELLOW_H,
    ).shift(DOWN * (row_h / 2))
    result.add(hl)

    # Outer border
    border = Rectangle(
        width=sum(col_widths),
        height=len(all_rows) * row_h,
        stroke_color=BLUE_H,
        stroke_width=1.2,
        fill_opacity=0,
    ).move_to(
        DOWN * (len(all_rows) - 1) * row_h / 2
    )
    result.add(border)
    return result


def animate_in(scene, mob, run_time=0.6):
    scene.play(FadeIn(mob), run_time=run_time)


def animate_out(scene, mob, run_time=0.5):
    scene.play(FadeOut(mob), run_time=run_time)


def clear_scene(scene, *mobs, run_time=0.5):
    if mobs:
        scene.play(*[FadeOut(m) for m in mobs], run_time=run_time)


# ─────────────────────────────────────────────
# MAIN VIDEO CLASS
# ─────────────────────────────────────────────

class PolynomialRegressionVideo(Scene):

    def construct(self):
        self.camera.background_color = BG
        self.scene_01_intro()
        self.scene_02_what_is()
        self.scene_03_five_ws()
        self.scene_04_why_linear_fails()
        self.scene_05_overall_pros_cons()
        self.scene_06_hilly_road()
        self.scene_07_feature_engineering()
        self.scene_08_real_world()
        self.scene_09_equation()
        self.scene_10_degree_shapes()
        self.scene_11_why_linear()
        self.scene_12_normal_equations()
        self.scene_13_normal_eq_pros_cons()
        self.scene_14_cost_gd()
        self.scene_15_gd_pros_cons()
        self.scene_16_assumptions_linemo()
        self.scene_17_assumption_linearity()
        self.scene_18_assumption_independence()
        self.scene_19_assumption_normality()
        self.scene_20_assumption_homoscedasticity()
        self.scene_21_assumption_multicollinearity()
        self.scene_22_multicollinearity_pros_cons()
        self.scene_23_assumption_outliers()
        self.scene_24_bias_variance()
        self.scene_25_bv_chart()
        self.scene_26_fitting_cards()
        self.scene_27_overfitting()
        self.scene_28_runge()
        self.scene_29_overfitting_pros_cons()
        self.scene_30_underfitting()
        self.scene_31_visual_inspection()
        self.scene_32_cross_validation()
        self.scene_33_learning_curves()
        self.scene_34_aic_bic()
        self.scene_35_adjusted_r2()
        self.scene_36_error_curve()
        self.scene_37_regularisation_overview()
        self.scene_38_ridge()
        self.scene_39_lasso()
        self.scene_40_elasticnet()
        self.scene_41_reg_comparison()
        self.scene_42_alpha_effect()
        self.scene_43_feature_scaling()
        self.scene_44_standard_scaler()
        self.scene_45_minmax()
        self.scene_46_centering()
        self.scene_47_feature_explosion()
        self.scene_48_explosion_pros_cons()
        self.scene_49_mse_rmse()
        self.scene_50_mae_r2()
        self.scene_51_adj_r2_mape()
        self.scene_52_ci_pi()
        self.scene_53_pipeline()
        self.scene_54_hp_poly()
        self.scene_55_hp_ridge()
        self.scene_56_hp_lasso_enet()
        self.scene_57_overall_pros_cons()
        self.scene_58_when_to_use()
        self.scene_59_alternatives()
        self.scene_60_mistakes()
        self.scene_61_iq_linear()
        self.scene_62_iq_overfit()
        self.scene_63_iq_train_test()
        self.scene_64_iq_scale()
        self.scene_65_iq_lasso_zeros()
        self.scene_66_outro()

    # ─────────────────────────────────────────
    # SCENE 01 — INTRO / TITLE CARD
    # ─────────────────────────────────────────
    def scene_01_intro(self):
        sub = make_subtitle("Polynomial Regression — The Complete Guide")

        title = Text("Polynomial", font_size=64, color=BLUE_H, weight=BOLD)
        title2 = Text("Regression", font_size=64, color=WHITE_H, weight=BOLD)
        tag = Text(
            "Machine Learning · Supervised · Regression",
            font_size=20, color=GRAY_H
        )
        channel = Text("The ML Notebook", font_size=18, color=YELLOW_H)

        title.shift(UP * 0.8)
        title2.next_to(title, DOWN, buff=0.1)
        tag.next_to(title2, DOWN, buff=0.35)
        channel.to_edge(DOWN, buff=1.0)

        deco = Circle(radius=2.2, color=BLUE_H, stroke_width=1.2)
        deco.set_opacity(0.12)
        deco.shift(RIGHT * 5 + UP * 1)
        deco2 = Circle(radius=1.0, color=ORANGE_H, stroke_width=0.8)
        deco2.set_opacity(0.10)
        deco2.shift(LEFT * 5 + DOWN * 1.5)

        self.play(FadeIn(deco), FadeIn(deco2), run_time=0.4)
        self.play(
            Write(title),
            Write(title2),
            run_time=1.2
        )
        self.play(FadeIn(tag), FadeIn(channel), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.4)
        self.wait(3)
        self.play(
            FadeOut(title), FadeOut(title2),
            FadeOut(tag), FadeOut(channel),
            FadeOut(deco), FadeOut(deco2),
            FadeOut(sub),
            run_time=0.7
        )

    # ─────────────────────────────────────────
    # SCENE 02 — WHAT IS POLYNOMIAL REGRESSION
    # ─────────────────────────────────────────
    def scene_02_what_is(self):
        sub = make_subtitle("What is Polynomial Regression?")
        sec_title = make_section_title("What is Polynomial Regression?")

        body1 = Text(
            "Models the relationship between x and y",
            font_size=24, color=WHITE_H
        ).shift(UP * 1.0)
        body2 = Text(
            "as an nth-degree polynomial.",
            font_size=24, color=WHITE_H
        ).next_to(body1, DOWN, buff=0.15)
        body3 = Text(
            "Used when data has a curved pattern that a straight line cannot capture.",
            font_size=20, color=GRAY_H
        ).next_to(body2, DOWN, buff=0.25)

        # Core idea callout box
        box = RoundedRectangle(
            width=9.5, height=1.6,
            corner_radius=0.15,
            fill_color="#111a2e",
            fill_opacity=1,
            stroke_color=BLUE_H,
            stroke_width=2.0,
        ).shift(DOWN * 1.4)
        idea_t = Text("Core Idea:", font_size=17, color=YELLOW_H, weight=BOLD)
        idea_t.next_to(box.get_top(), DOWN, buff=0.15)
        idea_body = Text(
            "Engineer x\u00b2, x\u00b3,\u2026 features, then run ordinary linear regression.",
            font_size=17, color=WHITE_H
        ).next_to(idea_t, DOWN, buff=0.12)
        idea_sub = Text(
            "Same math, different features.",
            font_size=15, color=GREEN_H
        ).next_to(idea_body, DOWN, buff=0.10)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body1), run_time=0.5)
        self.play(FadeIn(body2), run_time=0.4)
        self.play(FadeIn(body3), run_time=0.5)
        self.play(FadeIn(box), run_time=0.4)
        self.play(FadeIn(idea_t), FadeIn(idea_body), FadeIn(idea_sub), run_time=0.6)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title),
            FadeOut(body1), FadeOut(body2), FadeOut(body3),
            FadeOut(box), FadeOut(idea_t),
            FadeOut(idea_body), FadeOut(idea_sub),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 03 — THE FIVE W's
    # ─────────────────────────────────────────
    def scene_03_five_ws(self):
        sub = make_subtitle("What, How, Why, Where, When — The Five W's")
        sec_title = make_section_title("The Five W's + How", font_size=34)

        card_data = [
            ("WHAT", [
                "Fits a curved polynomial",
                "function (degree >= 2)",
                "for non-linear data.",
            ], BLUE_H),
            ("HOW", [
                "Creates [x, x^2, ..., x^n]",
                "features then fits linear",
                "model using OLS.",
            ], GREEN_H),
            ("WHY", [
                "Real-world data is rarely",
                "linear. Reuses the linear",
                "framework.",
            ], ORANGE_H),
            ("WHERE", [
                "Physics, economics,",
                "biology, engineering,",
                "climate science.",
            ], PURPLE_H),
            ("WHEN", [
                "Scatter plot shows curvature.",
                "Linear residuals show",
                "systematic patterns.",
            ], YELLOW_H),
            ("MECHANISM", [
                "Linear in parameters b,",
                "non-linear in x.",
                "Solved by Normal Equations.",
            ], RED_H),
        ]

        cards = VGroup()
        for title, lines, color in card_data:
            c = make_card(title, lines, card_w=3.4, card_h=2.0,
                          title_color=color)
            cards.add(c)

        cards.arrange_in_grid(2, 3, buff=0.28)
        cards.scale(0.88)
        cards.shift(DOWN * 0.25)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        for i, card in enumerate(cards):
            self.play(FadeIn(card), run_time=0.35)
        self.wait(4.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(cards),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 04 — WHY LINEAR REGRESSION FAILS
    # ─────────────────────────────────────────
    def scene_04_why_linear_fails(self):
        sub = make_subtitle("Why a straight line fails on curved data")
        sec_title = make_section_title("Why Linear Regression Fails on Curved Data",
                                       font_size=30)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 14, 4],
            x_length=7.5,
            y_length=4.2,
            axis_config={"color": GRAY_H, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.4)
        x_label = Text("x", font_size=18, color=GRAY_H).next_to(
            axes.x_axis, RIGHT, buff=0.1
        )
        y_label = Text("y", font_size=18, color=GRAY_H).next_to(
            axes.y_axis, UP, buff=0.1
        )

        # True relationship
        np.random.seed(7)
        xs = np.linspace(-2.8, 2.8, 30)
        ys = 1.8 * xs ** 2 - 2.0 * xs + 0.5

        dots = VGroup()
        for xi, yi in zip(xs, ys):
            d = Dot(axes.c2p(xi, yi), radius=0.06, color=BLUE_H)
            dots.add(d)

        # Linear fit (bad)
        m = np.polyfit(xs, ys, 1)
        linear_fn = lambda x: m[0] * x + m[1]
        linear_curve = axes.plot(
            linear_fn, x_range=[-2.8, 2.8],
            color=RED_H, stroke_width=2.5
        )

        # Quadratic fit (good)
        p = np.polyfit(xs, ys, 2)
        poly_fn = lambda x: p[0] * x**2 + p[1] * x + p[2]
        poly_curve = axes.plot(
            poly_fn, x_range=[-2.8, 2.8],
            color=GREEN_H, stroke_width=2.5
        )

        legend_lin = Text("Linear fit (misses curve)",
                          font_size=15, color=RED_H).to_corner(DR, buff=1.2)
        legend_poly = Text("Degree-2 polynomial (fits curve)",
                           font_size=15, color=GREEN_H).next_to(
            legend_lin, UP, buff=0.12
        )

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.6)
        self.play(FadeIn(dots), run_time=0.8)
        self.play(Create(linear_curve), FadeIn(legend_lin), run_time=0.9)
        self.wait(0.8)
        self.play(Create(poly_curve), FadeIn(legend_poly), run_time=0.9)
        self.wait(3)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(axes),
            FadeOut(x_label), FadeOut(y_label), FadeOut(dots),
            FadeOut(linear_curve), FadeOut(poly_curve),
            FadeOut(legend_lin), FadeOut(legend_poly),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 05 — OVERALL PROS AND CONS
    # ─────────────────────────────────────────
    def scene_05_overall_pros_cons(self):
        sub = make_subtitle("Polynomial Regression — Strengths and Weaknesses")
        sec_title = make_section_title("Polynomial Regression: Quick Pros & Cons",
                                       font_size=32)

        pros = [
            "Captures non-linearity",
            "Reuses OLS — no new solver",
            "Interpretable coefficients",
            "Flexible degree hyperparameter",
        ]
        cons = [
            "Overfits easily at high degrees",
            "Extrapolation is catastrophic",
            "Feature explosion with many inputs",
            "Multicollinearity between powers",
        ]
        pc = make_pros_cons(pros, cons, width=5.0, height=2.5)
        pc.shift(DOWN * 0.3)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(pc[0]), run_time=0.6)
        self.play(FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(pc), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 06 — HILLY ROAD ANALOGY
    # ─────────────────────────────────────────
    def scene_06_hilly_road(self):
        sub = make_subtitle("Intuition: Like a bendable ruler")
        sec_title = make_section_title("Intuition — The Hilly Road Analogy",
                                       font_size=34)

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[-1, 5, 2],
            x_length=8.0,
            y_length=3.5,
            axis_config={"color": GRAY_H, "stroke_width": 1.2},
            tips=False,
        ).shift(DOWN * 0.5)
        x_lbl = Text("Distance driven", font_size=16, color=GRAY_H).next_to(
            axes.x_axis, DOWN, buff=0.25
        )
        y_lbl = Text("Elevation", font_size=16, color=GRAY_H).next_to(
            axes.y_axis, UP, buff=0.1
        )

        road_fn = lambda x: 0.5 * np.sin(x * 0.9) + 0.08 * x + 1.0
        linear_fn = lambda x: 0.08 * x + 1.2

        road = axes.plot(road_fn, x_range=[0, 10], color=GREEN_H,
                         stroke_width=3.0)
        linear = DashedVMobject(
            axes.plot(linear_fn, x_range=[0, 10], color=RED_H,
                      stroke_width=2.5),
            num_dashes=28, dashed_ratio=0.6
        )

        lbl_road = Text("Polynomial (follows the hills)",
                        font_size=15, color=GREEN_H).to_corner(DR, buff=1.0)
        lbl_lin = Text("Linear (a straight ramp — wrong!)",
                       font_size=15, color=RED_H).next_to(lbl_road, UP, buff=0.1)

        quote = Text(
            '"Like a bendable ruler, not a rigid straight-edge."',
            font_size=19, color=YELLOW_H, slant=ITALIC
        ).to_edge(DOWN, buff=0.85)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.6)
        self.play(Create(road), FadeIn(lbl_road), run_time=0.9)
        self.play(Create(linear), FadeIn(lbl_lin), run_time=0.7)
        self.play(FadeIn(quote), run_time=0.6)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(axes),
            FadeOut(x_lbl), FadeOut(y_lbl), FadeOut(road),
            FadeOut(linear), FadeOut(lbl_road), FadeOut(lbl_lin),
            FadeOut(quote),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 07 — FEATURE ENGINEERING INSIGHT
    # ─────────────────────────────────────────
    def scene_07_feature_engineering(self):
        sub = make_subtitle(
            "Key trick: we never actually solve a non-linear problem"
        )
        sec_title = make_section_title("The Feature Engineering Insight",
                                       font_size=34)

        step1 = Text("Original input:", font_size=24, color=GRAY_H).shift(UP * 1.5 + LEFT * 3)
        arr1 = MathTex("x", font_size=38, color=BLUE_H).next_to(step1, RIGHT, buff=0.3)

        arrow = Arrow(RIGHT * 0.0, RIGHT * 2.0, buff=0.0,
                      color=YELLOW_H, stroke_width=2.5)
        arrow.next_to(arr1, RIGHT, buff=0.3)

        step2 = Text("Extended features:", font_size=22, color=GRAY_H).shift(
            UP * 1.5 + RIGHT * 2.3
        )
        arr2 = MathTex(
            r"[1,\; x,\; x^2,\; x^3,\; \ldots,\; x^n]",
            font_size=34, color=GREEN_H
        ).next_to(step2, DOWN, buff=0.18)
        if arr2.width > 5.5:
            arr2.scale(5.5 / arr2.width)

        note = Text(
            "The algorithm sees only a linear problem.",
            font_size=20, color=WHITE_H
        ).shift(DOWN * 0.2)

        box = RoundedRectangle(
            width=9.0, height=1.4,
            corner_radius=0.12,
            fill_color="#111a2e",
            fill_opacity=1,
            stroke_color=BLUE_H,
            stroke_width=1.5,
        ).shift(DOWN * 1.5)
        box_text = Text(
            "OLS solves this exactly — same Normal Equations as linear regression.",
            font_size=18, color=WHITE_H
        ).move_to(box.get_center())
        if box_text.width > 8.6:
            box_text.scale(8.6 / box_text.width)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(step1), FadeIn(arr1), run_time=0.5)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(FadeIn(step2), FadeIn(arr2), run_time=0.6)
        self.play(FadeIn(note), run_time=0.5)
        self.play(FadeIn(box), FadeIn(box_text), run_time=0.6)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(step1),
            FadeOut(arr1), FadeOut(arrow), FadeOut(step2),
            FadeOut(arr2), FadeOut(note), FadeOut(box), FadeOut(box_text),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 08 — REAL-WORLD EXAMPLES TABLE
    # ─────────────────────────────────────────
    def scene_08_real_world(self):
        sub = make_subtitle("Where Polynomial Regression Appears in the Real World")
        sec_title = make_section_title("Real-World Examples", font_size=36)

        headers = ["Domain", "x Variable", "y Variable", "Reason"]
        rows = [
            ["Physics", "Time", "Ball height", "Gravity is quadratic"],
            ["Economics", "Ad spend", "Revenue", "Diminishing returns"],
            ["Biology", "Age", "Height", "Growth then plateau"],
            ["HR", "Experience", "Salary", "Rises then levels off"],
            ["Engineering", "Temperature", "Stress", "Non-linear relation"],
            ["Chemistry", "Concentration", "Reaction rate", "Often quadratic"],
        ]
        col_w = [2.2, 2.0, 2.0, 3.6]
        tbl = make_table_mob(headers, rows, col_widths=col_w, font_size=15)
        tbl.scale(0.92)
        tbl.shift(DOWN * 0.35)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(tbl), run_time=0.9)
        self.wait(5)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(tbl), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 09 — THE POLYNOMIAL EQUATION
    # ─────────────────────────────────────────
    def scene_09_equation(self):
        sub = make_subtitle("The Polynomial Equation")
        sec_title = make_section_title("The Polynomial Equation", font_size=36)

        formula = MathTex(
            r"\hat{y} = \beta_0 + \beta_1 x + \beta_2 x^2 + \beta_3 x^3"
            r" + \cdots + \beta_n x^n + \varepsilon",
            font_size=32, color=WHITE_H
        )
        fbox = make_formula_box(
            formula,
            label_text=(
                "b0...bn are coefficients; x is the input; e is irreducible noise"
            ),
            width=10.0, height=1.4
        )
        fbox.shift(UP * 1.3)

        headers = ["Term", "Name", "Meaning"]
        rows = [
            ["y-hat", "Predicted value", "Model output estimate"],
            ["beta_0", "Intercept", "Value of y-hat when x = 0"],
            ["beta_1", "Linear coeff.", "Effect of x on y"],
            ["beta_2", "Quadratic coeff.", "Adds 1 bend (parabola)"],
            ["beta_3", "Cubic coeff.", "Adds up to 2 bends"],
            ["beta_n", "Degree-n coeff.", "Highest-degree term"],
            ["epsilon", "Error term", "Irreducible random noise"],
        ]
        tbl = make_table_mob(headers, rows, col_widths=[2.0, 2.8, 4.5],
                             font_size=14)
        tbl.scale(0.88)
        tbl.shift(DOWN * 1.3)

        key_rule = Text(
            "KEY: A degree-n polynomial has at most n-1 turning points.",
            font_size=16, color=YELLOW_H
        ).to_edge(DOWN, buff=0.75)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(tbl), run_time=0.8)
        self.play(FadeIn(key_rule), run_time=0.5)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox),
            FadeOut(tbl), FadeOut(key_rule),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 10 — DEGREE CONTROLS CURVE SHAPE
    # ─────────────────────────────────────────
    def scene_10_degree_shapes(self):
        sub = make_subtitle("How Degree Controls the Curve Shape")
        sec_title = make_section_title("Degree Controls the Curve Shape",
                                       font_size=34)

        configs = [
            (1, lambda x: 0.5 * x + 0.5, "Degree 1 — 0 bends", BLUE_H),
            (2, lambda x: 0.8 * x**2 - 1.0 * x - 0.5, "Degree 2 — 1 bend",
             GREEN_H),
            (3, lambda x: 0.4 * x**3 - x**2 - 0.3 * x + 1.0,
             "Degree 3 — 2 bends", ORANGE_H),
            (4, lambda x: 0.3 * x**4 - 0.8 * x**3 - 0.3 * x**2 + x + 0.5,
             "Degree 4 — 3 bends", PURPLE_H),
        ]

        ax_grps = VGroup()
        labels = VGroup()
        curves = VGroup()

        positions = [
            LEFT * 4.5 + UP * 0.5,
            LEFT * 1.5 + UP * 0.5,
            RIGHT * 1.5 + UP * 0.5,
            RIGHT * 4.5 + UP * 0.5,
        ]

        for idx, (deg, fn, lbl_text, color) in enumerate(configs):
            ax = Axes(
                x_range=[-2, 2, 1],
                y_range=[-3, 5, 2],
                x_length=2.5,
                y_length=2.5,
                axis_config={"color": GRAY_H, "stroke_width": 1.0},
                tips=False,
            ).move_to(positions[idx])
            try:
                c = ax.plot(fn, x_range=[-1.9, 1.9], color=color,
                            stroke_width=2.5)
            except Exception:
                c = VMobject()
            lbl = Text(lbl_text, font_size=13, color=color).next_to(
                ax, DOWN, buff=0.15
            )
            if lbl.width > 2.6:
                lbl.scale(2.6 / lbl.width)
            ax_grps.add(ax)
            labels.add(lbl)
            curves.add(c)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        for ax, c, lbl in zip(ax_grps, curves, labels):
            self.play(
                Create(ax), Create(c), FadeIn(lbl),
                run_time=0.6
            )
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title),
            FadeOut(ax_grps), FadeOut(curves), FadeOut(labels),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 11 — WHY IT IS STILL "LINEAR"
    # ─────────────────────────────────────────
    def scene_11_why_linear(self):
        sub = make_subtitle("Why is it STILL called 'Linear' Regression?")
        sec_title = make_section_title("Why Is It Still Called 'Linear'?",
                                       font_size=34)

        key = Text(
            '"Linear" means linear in the PARAMETERS b — not linear in x.',
            font_size=20, color=YELLOW_H
        ).shift(UP * 1.6)
        if key.width > 11:
            key.scale(11 / key.width)

        # Left box — linear in beta
        left_box = RoundedRectangle(
            width=5.2, height=2.5,
            corner_radius=0.12,
            fill_color=DARK_GR, fill_opacity=1,
            stroke_color=GREEN_H, stroke_width=2
        ).shift(LEFT * 3.0 + DOWN * 0.3)
        lt = Text("Linear in b (OK for OLS)", font_size=16,
                  color=GREEN_H, weight=BOLD)
        lt.next_to(left_box.get_top(), DOWN, buff=0.15)
        lf = MathTex(
            r"y = \beta_0 + \beta_1 x + \beta_2 x^2",
            font_size=26, color=WHITE_H
        ).next_to(lt, DOWN, buff=0.25)
        ln = Text(
            "OLS solves this exactly.\nSame Normal Equations.",
            font_size=14, color=GRAY_H
        ).next_to(lf, DOWN, buff=0.18)
        if ln.width > 4.8:
            ln.scale(4.8 / ln.width)

        # Right box — non-linear in beta
        right_box = RoundedRectangle(
            width=5.2, height=2.5,
            corner_radius=0.12,
            fill_color=DARK_RD, fill_opacity=1,
            stroke_color=RED_H, stroke_width=2
        ).shift(RIGHT * 3.0 + DOWN * 0.3)
        rt = Text("Non-linear in b (Needs GD)", font_size=16,
                  color=RED_H, weight=BOLD)
        rt.next_to(right_box.get_top(), DOWN, buff=0.15)
        rf = MathTex(
            r"y = \beta_0 \cdot e^{\beta_1 x}",
            font_size=26, color=WHITE_H
        ).next_to(rt, DOWN, buff=0.25)
        rn = Text(
            "b1 is inside an exponent.\nRequires gradient descent.",
            font_size=14, color=GRAY_H
        ).next_to(rf, DOWN, buff=0.18)
        if rn.width > 4.8:
            rn.scale(4.8 / rn.width)

        trap_note = Text(
            "#1 Interview Trap — Do not confuse 'linear in x' with 'linear in b'.",
            font_size=15, color=YELLOW_H
        ).to_edge(DOWN, buff=0.85)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(key), run_time=0.5)
        self.play(
            FadeIn(left_box), FadeIn(lt), FadeIn(lf), FadeIn(ln),
            run_time=0.7
        )
        self.play(
            FadeIn(right_box), FadeIn(rt), FadeIn(rf), FadeIn(rn),
            run_time=0.7
        )
        self.play(FadeIn(trap_note), run_time=0.5)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(key),
            FadeOut(left_box), FadeOut(lt), FadeOut(lf), FadeOut(ln),
            FadeOut(right_box), FadeOut(rt), FadeOut(rf), FadeOut(rn),
            FadeOut(trap_note),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 12 — THE NORMAL EQUATIONS
    # ─────────────────────────────────────────
    def scene_12_normal_equations(self):
        sub = make_subtitle("The Normal Equations — Optimal Solution in One Step")
        sec_title = make_section_title("The Normal Equations", font_size=36)

        intro = Text(
            "After building the design matrix X (columns: 1, x, x^2, ..., x^n):",
            font_size=19, color=GRAY_H
        ).shift(UP * 1.6)
        if intro.width > 11:
            intro.scale(11 / intro.width)

        formula = MathTex(
            r"\hat{\beta} = (X^T X)^{-1} \cdot X^T y",
            font_size=50, color=WHITE_H
        )
        fbox = make_formula_box(
            formula,
            label_text=(
                "Minimises sum of squared residuals exactly — no iteration needed"
            ),
            width=8.0, height=1.5
        )
        fbox.shift(UP * 0.3)

        # Residual visualisation mini axes
        ax = Axes(
            x_range=[-2, 2, 1],
            y_range=[-1, 6, 2],
            x_length=4.5,
            y_length=2.5,
            axis_config={"color": GRAY_H, "stroke_width": 1.0},
            tips=False,
        ).shift(DOWN * 1.8)

        np.random.seed(3)
        xs_d = np.linspace(-1.8, 1.8, 10)
        ys_d = xs_d**2 + 0.5 * xs_d + 0.8

        dts = VGroup(*[
            Dot(ax.c2p(x, y), radius=0.07, color=BLUE_H)
            for x, y in zip(xs_d, ys_d)
        ])
        fit_curve = ax.plot(
            lambda x: x**2 + 0.5 * x + 0.8,
            x_range=[-1.8, 1.8], color=GREEN_H, stroke_width=2.0
        )

        res_label = Text("Residuals minimised by Normal Equations",
                         font_size=13, color=GRAY_H).next_to(ax, DOWN, buff=0.12)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(intro), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.8)
        self.play(Create(ax), FadeIn(dts), Create(fit_curve), run_time=0.9)
        self.play(FadeIn(res_label), run_time=0.4)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(intro),
            FadeOut(fbox), FadeOut(ax), FadeOut(dts),
            FadeOut(fit_curve), FadeOut(res_label),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 13 — NORMAL EQUATIONS PROS/CONS
    # ─────────────────────────────────────────
    def scene_13_normal_eq_pros_cons(self):
        sub = make_subtitle("Normal Equations — Pros and Cons")
        sec_title = make_section_title("Normal Equations: Pros & Cons",
                                       font_size=34)

        pros = [
            "Exact closed-form solution",
            "Globally optimal (one-step)",
            "No convergence issues",
            "Simple to implement",
        ]
        cons = [
            "O(p^3) cost — expensive for high deg",
            "Numerically unstable with multicollinearity",
            "Not suitable for very large datasets",
            "Needs to store a p x p matrix",
        ]
        pc = make_pros_cons(pros, cons, width=5.5, height=3.0)
        pc.shift(DOWN * 0.3)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(pc[0]), run_time=0.6)
        self.play(FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(pc), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 14 — COST FUNCTION AND GRADIENT DESCENT
    # ─────────────────────────────────────────
    def scene_14_cost_gd(self):
        sub = make_subtitle("Cost Function: MSE and Gradient Descent")
        sec_title = make_section_title("Cost Function & Gradient Descent",
                                       font_size=34)

        mse_f = MathTex(
            r"\text{MSE} = \frac{1}{m} \sum_{i=1}^{m} (y_i - \hat{y}_i)^2",
            font_size=38, color=WHITE_H
        )
        mse_box = make_formula_box(
            mse_f,
            label_text="We minimise the squared differences between actual and predicted",
            width=8.5, height=1.4
        )
        mse_box.shift(UP * 1.2)

        label_gd = Text(
            "When dataset is too large for Normal Equations — use Gradient Descent:",
            font_size=18, color=GRAY_H
        ).shift(DOWN * 0.1)
        if label_gd.width > 10.5:
            label_gd.scale(10.5 / label_gd.width)

        gd_f = MathTex(
            r"\beta_j := \beta_j - \alpha \cdot \frac{\partial \text{MSE}}{\partial \beta_j}",
            font_size=36, color=WHITE_H
        )
        gd_box = make_formula_box(
            gd_f,
            label_text="a = learning rate. Repeat until convergence.",
            width=8.0, height=1.4
        )
        gd_box.shift(DOWN * 1.6)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(mse_box), run_time=0.7)
        self.play(FadeIn(label_gd), run_time=0.5)
        self.play(FadeIn(gd_box), run_time=0.7)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(mse_box),
            FadeOut(label_gd), FadeOut(gd_box),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 15 — GRADIENT DESCENT PROS/CONS
    # ─────────────────────────────────────────
    def scene_15_gd_pros_cons(self):
        sub = make_subtitle("Gradient Descent — Pros and Cons")
        sec_title = make_section_title("Gradient Descent: Pros & Cons",
                                       font_size=34)

        pros = [
            "Scales to large datasets",
            "Works even when X^T X not invertible",
            "Memory efficient (no large matrices)",
        ]
        cons = [
            "Requires learning rate tuning",
            "Slower than Normal Eq for small data",
            "Needs convergence monitoring",
        ]
        pc = make_pros_cons(pros, cons, width=5.5, height=2.8)
        pc.shift(DOWN * 0.3)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(pc[0]), run_time=0.6)
        self.play(FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(pc), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 16 — ASSUMPTIONS LINE-MO
    # ─────────────────────────────────────────
    def scene_16_assumptions_linemo(self):
        sub = make_subtitle("Assumptions: The LINE-MO Framework")
        sec_title = make_section_title("Assumptions — LINE-MO Framework",
                                       font_size=34)

        intro = Text(
            "Polynomial regression inherits ALL assumptions of linear regression.",
            font_size=20, color=GRAY_H
        ).shift(UP * 1.6)
        if intro.width > 11:
            intro.scale(11 / intro.width)

        letters = ["L", "I", "N", "E", "M", "O"]
        meanings = [
            "Linearity in parameters",
            "Independence of observations",
            "Normality of residuals",
            "Equal variance (Homoscedasticity)",
            "No severe Multicollinearity",
            "No extreme Outliers",
        ]
        colors = [BLUE_H, GREEN_H, ORANGE_H, YELLOW_H, PURPLE_H, RED_H]

        rows_grp = VGroup()
        for letter, meaning, color in zip(letters, meanings, colors):
            l_obj = Text(letter, font_size=28, color=color, weight=BOLD)
            m_obj = Text(meaning, font_size=19, color=WHITE_H)
            row = VGroup(l_obj, m_obj)
            row.arrange(RIGHT, buff=0.35)
            rows_grp.add(row)

        rows_grp.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rows_grp.shift(DOWN * 0.3)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(intro), run_time=0.5)
        for row in rows_grp:
            self.play(FadeIn(row), run_time=0.35)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title),
            FadeOut(intro), FadeOut(rows_grp),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 17 — ASSUMPTION 1: LINEARITY
    # ─────────────────────────────────────────
    def scene_17_assumption_linearity(self):
        sub = make_subtitle("Assumption 1: Linearity in Parameters")
        sec_title = make_section_title("Assumption 1 — Linearity", font_size=36)

        body = Text(
            "The relationship between polynomial features and y\n"
            "must be a linear combination of parameters b.",
            font_size=19, color=WHITE_H
        ).shift(UP * 1.4)
        if body.width > 11:
            body.scale(11 / body.width)

        detect = Text(
            "Detection: Residuals vs. fitted — look for remaining curves.",
            font_size=16, color=BLUE_H
        ).next_to(body, DOWN, buff=0.28)
        remedy = Text(
            "Remedy: Increase degree; log/sqrt transforms; switch model.",
            font_size=16, color=GREEN_H
        ).next_to(detect, DOWN, buff=0.12)

        pros = ["OLS gives unbiased estimates", "Coefficients are meaningful",
                "Standard errors are correct"]
        cons = ["Systematic residual patterns", "Underfits no matter the degree",
                "Predictions are biased"]
        pc = make_pros_cons(pros, cons, width=5.0, height=2.5)
        pc.shift(DOWN * 1.6)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        self.play(FadeIn(detect), FadeIn(remedy), run_time=0.5)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body),
            FadeOut(detect), FadeOut(remedy), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 18 — ASSUMPTION 2: INDEPENDENCE
    # ─────────────────────────────────────────
    def scene_18_assumption_independence(self):
        sub = make_subtitle("Assumption 2: Independence of Observations")
        sec_title = make_section_title("Assumption 2 — Independence",
                                       font_size=36)

        body = Text(
            "Residuals must be uncorrelated with each other.\n"
            "Violated in time series, spatial data, or grouped measurements.",
            font_size=19, color=WHITE_H
        ).shift(UP * 1.4)

        detect = Text(
            "Detection: Durbin-Watson statistic (near 2 = OK); ACF plot.",
            font_size=16, color=BLUE_H
        ).next_to(body, DOWN, buff=0.28)
        remedy = Text(
            "Remedy: ARIMA for time series; mixed-effects models for grouped data.",
            font_size=16, color=GREEN_H
        ).next_to(detect, DOWN, buff=0.12)
        if remedy.width > 11:
            remedy.scale(11 / remedy.width)

        pros = ["Inference (p-values, CIs) is valid",
                "Standard errors correctly estimated"]
        cons = ["Standard errors underestimated",
                "Overconfident p-values — false significance"]
        pc = make_pros_cons(pros, cons, width=5.0, height=2.2)
        pc.shift(DOWN * 1.7)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        self.play(FadeIn(detect), FadeIn(remedy), run_time=0.5)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body),
            FadeOut(detect), FadeOut(remedy), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 19 — ASSUMPTION 3: NORMALITY
    # ─────────────────────────────────────────
    def scene_19_assumption_normality(self):
        sub = make_subtitle("Assumption 3: Normality of Residuals")
        sec_title = make_section_title("Assumption 3 — Normality of Residuals",
                                       font_size=34)

        body = Text(
            "Residuals should be approximately normally distributed.\n"
            "Only needed for confidence intervals and hypothesis tests.",
            font_size=19, color=WHITE_H
        ).shift(UP * 1.4)

        detect = Text(
            "Detection: Q-Q plot; Shapiro-Wilk test; histogram of residuals.",
            font_size=16, color=BLUE_H
        ).next_to(body, DOWN, buff=0.28)
        remedy = Text(
            "Remedy: Log-transform y; Box-Cox transformation; remove outliers.",
            font_size=16, color=GREEN_H
        ).next_to(detect, DOWN, buff=0.12)

        pros = ["t-tests on coefficients valid",
                "Confidence intervals accurate"]
        cons = ["CIs and p-values unreliable",
                "Predictions still OK with large n"]
        pc = make_pros_cons(pros, cons, width=5.0, height=2.2)
        pc.shift(DOWN * 1.7)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        self.play(FadeIn(detect), FadeIn(remedy), run_time=0.5)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body),
            FadeOut(detect), FadeOut(remedy), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 20 — ASSUMPTION 4: HOMOSCEDASTICITY
    # ─────────────────────────────────────────
    def scene_20_assumption_homoscedasticity(self):
        sub = make_subtitle("Assumption 4: Equal Variance (Homoscedasticity)")
        sec_title = make_section_title("Assumption 4 — Equal Variance",
                                       font_size=34)

        body = Text(
            "Residual variance must be constant across all fitted values.\n"
            "Funnel shape in residuals = heteroscedasticity.",
            font_size=19, color=WHITE_H
        ).shift(UP * 1.6)

        # Funnel animation
        ax = Axes(
            x_range=[0, 5, 1],
            y_range=[-4, 4, 2],
            x_length=4.0,
            y_length=2.5,
            axis_config={"color": GRAY_H, "stroke_width": 1.0},
            tips=False,
        ).shift(DOWN * 0.6)
        np.random.seed(5)
        xs_f = np.linspace(0.3, 4.8, 25)
        spread = xs_f * 0.6
        ys_f = np.array([np.random.uniform(-s, s) for s in spread])
        dots_f = VGroup(*[
            Dot(ax.c2p(x, y), radius=0.07, color=ORANGE_H)
            for x, y in zip(xs_f, ys_f)
        ])
        zero_line = DashedVMobject(
            ax.plot(lambda x: 0, x_range=[0, 5],
                    color=GRAY_H, stroke_width=1.2),
            num_dashes=20, dashed_ratio=0.5
        )
        funnel_lbl = Text("Funnel = Heteroscedasticity",
                          font_size=14, color=RED_H).next_to(ax, DOWN, buff=0.1)

        detect = Text(
            "Detection: Residuals vs Fitted plot; Breusch-Pagan test.",
            font_size=15, color=BLUE_H
        ).next_to(funnel_lbl, DOWN, buff=0.1)
        remedy = Text(
            "Remedy: Log-transform y; Weighted Least Squares; robust SE.",
            font_size=15, color=GREEN_H
        ).next_to(detect, DOWN, buff=0.1)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        self.play(Create(ax), Create(zero_line), run_time=0.5)
        self.play(FadeIn(dots_f), run_time=0.7)
        self.play(FadeIn(funnel_lbl), FadeIn(detect), FadeIn(remedy),
                  run_time=0.5)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body),
            FadeOut(ax), FadeOut(zero_line), FadeOut(dots_f),
            FadeOut(funnel_lbl), FadeOut(detect), FadeOut(remedy),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 21 — ASSUMPTION 5: MULTICOLLINEARITY
    # ─────────────────────────────────────────
    def scene_21_assumption_multicollinearity(self):
        sub = make_subtitle(
            "Assumption 5: No Severe Multicollinearity — Critical for Polynomial!"
        )
        sec_title = make_section_title("Assumption 5 — Multicollinearity",
                                       font_size=33)

        body = Text(
            "x, x^2, x^3 are all derived from the same x — inherently correlated.\n"
            "This makes X^T X nearly singular, causing unstable coefficients.",
            font_size=18, color=WHITE_H
        ).shift(UP * 1.6)

        warn_box = RoundedRectangle(
            width=10.0, height=1.2,
            corner_radius=0.12,
            fill_color="#2a1a00", fill_opacity=1,
            stroke_color=YELLOW_H, stroke_width=2
        ).shift(UP * 0.25)
        warn_text = Text(
            "WARNING: Even if model fits well, individual b values may be meaningless!\n"
            "E.g.: b2 = +10,000,000 and b3 = -9,999,999 tells you nothing individually.",
            font_size=15, color=YELLOW_H
        ).move_to(warn_box.get_center())
        if warn_text.width > 9.6:
            warn_text.scale(9.6 / warn_text.width)

        vif = MathTex(
            r"\text{VIF} = \frac{1}{1 - R_j^2}",
            font_size=28, color=WHITE_H
        ).shift(DOWN * 1.0)
        vif_note = Text(
            "VIF > 5 = moderate multicollinearity    |    VIF > 10 = severe",
            font_size=15, color=ORANGE_H
        ).next_to(vif, DOWN, buff=0.15)

        remedy = Text(
            "Remedy: Center x before computing powers. Apply Ridge. Use orthogonal polynomials.",
            font_size=15, color=GREEN_H
        ).shift(DOWN * 2.0)
        if remedy.width > 11:
            remedy.scale(11 / remedy.width)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        self.play(FadeIn(warn_box), FadeIn(warn_text), run_time=0.6)
        self.play(FadeIn(vif), FadeIn(vif_note), run_time=0.5)
        self.play(FadeIn(remedy), run_time=0.5)
        self.wait(4.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body),
            FadeOut(warn_box), FadeOut(warn_text),
            FadeOut(vif), FadeOut(vif_note), FadeOut(remedy),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 22 — MULTICOLLINEARITY PROS/CONS
    # ─────────────────────────────────────────
    def scene_22_multicollinearity_pros_cons(self):
        sub = make_subtitle("Multicollinearity — Impact on Your Model")
        sec_title = make_section_title("Multicollinearity: Pros & Cons",
                                       font_size=34)

        pros = [
            "Coefficients individually interpretable",
            "Standard errors small and reliable",
            "Coefficient signs make physical sense",
        ]
        cons = [
            "Numerically unstable coefficients",
            "Tiny data changes -> huge coeff changes",
            "Model predicts OK but uninterpretable",
        ]
        pc = make_pros_cons(pros, cons, width=5.5, height=2.8)
        pc.shift(DOWN * 0.3)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(pc[0]), run_time=0.6)
        self.play(FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(pc), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 23 — ASSUMPTION 6: OUTLIERS
    # ─────────────────────────────────────────
    def scene_23_assumption_outliers(self):
        sub = make_subtitle("Assumption 6: No Extreme Outliers or Influential Points")
        sec_title = make_section_title("Assumption 6 — Outliers", font_size=36)

        body = Text(
            "Outliers are AMPLIFIED in polynomial regression.\n"
            "One edge point can pull the entire curve wildly.",
            font_size=19, color=WHITE_H
        ).shift(UP * 1.6)

        # Animation: show a curve distorted by an outlier
        ax = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 12, 4],
            x_length=5.5,
            y_length=2.8,
            axis_config={"color": GRAY_H, "stroke_width": 1.0},
            tips=False,
        ).shift(DOWN * 0.35)

        good_curve = ax.plot(
            lambda x: x**2 - x + 0.5,
            x_range=[-2.8, 2.8], color=GREEN_H, stroke_width=2.5
        )
        outlier_dot = Dot(ax.c2p(2.5, 10.5), radius=0.12, color=RED_H)
        distorted = DashedVMobject(
            ax.plot(
                lambda x: 0.8 * x**2 + 0.4 * x + 2.5 + 0.7 * x**3 * 0.1,
                x_range=[-2.8, 2.8], color=RED_H, stroke_width=2.5,
            ),
            num_dashes=22, dashed_ratio=0.6
        )

        cook = MathTex(
            r"D_i = \frac{(\hat{\beta}_{(i)} - \hat{\beta})^T "
            r"(X^T X)(\hat{\beta}_{(i)} - \hat{\beta})}{p \cdot \text{MSE}}",
            font_size=22, color=WHITE_H
        ).shift(DOWN * 2.2)
        cook_note = Text(
            "Points with Di > 4/n are potentially influential.",
            font_size=14, color=YELLOW_H
        ).next_to(cook, DOWN, buff=0.12)
        if cook_note.width > 10:
            cook_note.scale(10 / cook_note.width)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        self.play(Create(ax), Create(good_curve), run_time=0.7)
        self.play(FadeIn(outlier_dot), run_time=0.4)
        self.play(Create(distorted), run_time=0.7)
        self.play(FadeIn(cook), FadeIn(cook_note), run_time=0.5)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body),
            FadeOut(ax), FadeOut(good_curve), FadeOut(outlier_dot),
            FadeOut(distorted), FadeOut(cook), FadeOut(cook_note),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 24 — BIAS-VARIANCE TRADEOFF
    # ─────────────────────────────────────────
    def scene_24_bias_variance(self):
        sub = make_subtitle("The Bias-Variance Tradeoff")
        sec_title = make_section_title("The Bias-Variance Tradeoff", font_size=36)

        formula = MathTex(
            r"\text{Total Error} = \text{Bias}^2 + \text{Variance}"
            r" + \text{Irreducible Noise}",
            font_size=30, color=WHITE_H
        )
        fbox = make_formula_box(
            formula,
            label_text=(
                "You cannot simultaneously minimise all three"
            ),
            width=10.0, height=1.35
        )
        fbox.shift(UP * 1.5)

        headers = ["Component", "Caused By", "Effect"]
        rows = [
            ["Bias^2", "Model too simple", "Underfitting — always wrong same dir"],
            ["Variance", "Model too complex", "Overfitting — fails on test data"],
            ["Noise", "Measurement error", "Cannot be reduced — accept it"],
        ]
        tbl = make_table_mob(headers, rows,
                             col_widths=[2.2, 3.0, 4.5],
                             font_size=14)
        tbl.scale(0.9)
        tbl.shift(DOWN * 0.4)

        note = Text(
            "The polynomial DEGREE is a direct dial on the bias-variance tradeoff.",
            font_size=17, color=YELLOW_H
        ).to_edge(DOWN, buff=0.8)
        if note.width > 11:
            note.scale(11 / note.width)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(tbl), run_time=0.8)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(4.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox),
            FadeOut(tbl), FadeOut(note),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 25 — BIAS-VARIANCE CHART
    # ─────────────────────────────────────────
    def scene_25_bv_chart(self):
        sub = make_subtitle("Bias and Variance vs. Polynomial Degree")
        sec_title = make_section_title("Bias-Variance vs. Polynomial Degree",
                                       font_size=32)

        ax = Axes(
            x_range=[1, 10, 1],
            y_range=[0, 18, 4],
            x_length=8.0,
            y_length=3.8,
            axis_config={"color": GRAY_H, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.5)
        xl = Text("Polynomial Degree", font_size=16, color=GRAY_H).next_to(
            ax.x_axis, DOWN, buff=0.25
        )
        yl = Text("Error", font_size=16, color=GRAY_H).next_to(
            ax.y_axis, UP, buff=0.08
        )

        # Data
        degrees = list(range(1, 11))
        bias2 = [9, 3.5, 1.2, 0.7, 0.4, 0.28, 0.2, 0.15, 0.12, 0.1]
        vari  = [0.15, 0.4, 0.9, 1.8, 3.3, 5.8, 9.2, 13, 17, 22]
        total = [b + v + 0.5 for b, v in zip(bias2, vari)]

        def make_curve(data, color, dash=None):
            pts = [ax.c2p(d, v) for d, v in zip(degrees, data)
                   if 0 <= v <= 18]
            if len(pts) < 2:
                return VMobject()
            curve = VMobject()
            curve.set_points_smoothly(pts)
            curve.set_color(color)
            curve.set_stroke(width=2.5)
            if dash:
                curve.set_stroke(dash_offset=dash)
            return curve

        bias_c = make_curve(bias2, RED_H)
        var_c  = make_curve(vari, BLUE_H)
        tot_c  = make_curve(total, GREEN_H)

        # Optimal marker
        opt_deg = 3
        opt_v = total[opt_deg - 1]
        opt_pt = ax.c2p(opt_deg, opt_v)
        opt_marker = Dot(opt_pt, radius=0.12, color=YELLOW_H)
        opt_label = Text("Optimal Degree", font_size=13,
                         color=YELLOW_H).next_to(opt_marker, UR, buff=0.1)

        leg_b = MathTex(r"\text{Bias}^2", font_size=30, color=RED_H).to_corner(UR, buff=1.2)
        leg_v = Text("Variance", font_size=14, color=BLUE_H).next_to(leg_b, DOWN,
                                                                      buff=0.1)
        leg_t = Text("Total Error", font_size=14, color=GREEN_H).next_to(leg_v,
                                                                          DOWN,
                                                                          buff=0.1)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.6)
        self.play(Create(bias_c), FadeIn(leg_b), run_time=0.7)
        self.play(Create(var_c), FadeIn(leg_v), run_time=0.7)
        self.play(Create(tot_c), FadeIn(leg_t), run_time=0.7)
        self.play(FadeIn(opt_marker), FadeIn(opt_label), run_time=0.5)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(ax),
            FadeOut(xl), FadeOut(yl),
            FadeOut(bias_c), FadeOut(var_c), FadeOut(tot_c),
            FadeOut(opt_marker), FadeOut(opt_label),
            FadeOut(leg_b), FadeOut(leg_v), FadeOut(leg_t),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 26 — FITTING CARDS
    # ─────────────────────────────────────────
    def scene_26_fitting_cards(self):
        sub = make_subtitle("Underfitting, Good Fit, and Overfitting")
        sec_title = make_section_title("Low / Optimal / High Degree Behaviour",
                                       font_size=32)

        card_data = [
            ("Low Degree — High Bias", [
                "Too rigid to capture the curve",
                "Bad train AND test error",
                "Error is systematic — always off",
                "More data won't fix it",
            ], BLUE_H),
            ("Optimal Degree — Balanced", [
                "Fits signal, ignores noise",
                "Good train AND test error",
                "Generalises well",
                "Found via cross-validation",
            ], GREEN_H),
            ("High Degree — High Variance", [
                "Memorises training noise",
                "Near-zero train, high test error",
                "Predictions change on new data",
                "More data helps significantly",
            ], RED_H),
        ]

        cards = VGroup()
        for title, lines, color in card_data:
            c = make_card(title, lines, card_w=3.8, card_h=2.8,
                          title_color=color)
            cards.add(c)
        cards.arrange(RIGHT, buff=0.35)
        cards.shift(DOWN * 0.2)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        for c in cards:
            self.play(FadeIn(c), run_time=0.5)
        self.wait(4)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(cards), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 27 — OVERFITTING SIGNS
    # ─────────────────────────────────────────
    def scene_27_overfitting(self):
        sub = make_subtitle("Overfitting — Signs and Causes")
        sec_title = make_section_title("Overfitting", font_size=40)

        definition = Text(
            "Model learns training data too well — including noise.\n"
            "Fails to generalise to new data.",
            font_size=20, color=WHITE_H
        ).shift(UP * 1.8)

        headers = ["Signal", "What It Means"]
        rows = [
            ["Train R^2=1.0, Test R^2 << 1.0", "Memorised training noise"],
            ["Huge coefficient magnitudes", "Coefficients cancelling each other"],
            ["Wildly oscillating curve", "Runge's phenomenon"],
            ["Test MSE >> Train MSE", "High variance, poor generalisation"],
            ["Curve shoots to +/-inf at edges", "Extrapolation failure"],
        ]
        tbl = make_table_mob(headers, rows, col_widths=[4.8, 5.0], font_size=14)
        tbl.scale(0.9)
        tbl.shift(DOWN * 0.5)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(definition), run_time=0.5)
        self.play(FadeIn(tbl), run_time=0.8)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title),
            FadeOut(definition), FadeOut(tbl),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 28 — RUNGE'S PHENOMENON
    # ─────────────────────────────────────────
    def scene_28_runge(self):
        sub = make_subtitle("Runge's Phenomenon — Oscillation at High Degrees")
        sec_title = make_section_title("Runge's Phenomenon", font_size=36)

        body = Text(
            "High-degree polynomial interpolation at equally-spaced points\n"
            "oscillates wildly near the edges — even for smooth functions.",
            font_size=19, color=WHITE_H
        ).shift(UP * 1.7)

        ax = Axes(
            x_range=[-5, 5, 2],
            y_range=[-1.5, 4.5, 1],
            x_length=7.5,
            y_length=3.2,
            axis_config={"color": GRAY_H, "stroke_width": 1.2},
            tips=False,
        ).shift(DOWN * 0.55)

        true_fn = lambda x: 1 / (1 + x**2)
        runge_fn = lambda x: (
            1 / (1 + x**2)
            + (0.5 * np.sin(2.1 * x) * max(0, abs(x) - 2.8) ** 1.5)
        )

        true_c = ax.plot(true_fn, x_range=[-4.9, 4.9],
                         color=BLUE_H, stroke_width=2.5)
        runge_c = ax.plot(runge_fn, x_range=[-4.9, 4.9],
                          color=RED_H, stroke_width=2.5)

        pts = list(range(-5, 6))
        eq_pts = VGroup(*[
            Dot(ax.c2p(float(p), true_fn(float(p))), radius=0.08, color=GREEN_H)
            for p in pts
        ])

        leg_t = MathTex(r"\text{True:}\;\tfrac{1}{1+x^2}", font_size=26, color=BLUE_H).to_corner(
            UR, buff=1.0
        )
        leg_r = Text("High-degree poly (oscillates at edges)",
                     font_size=13, color=RED_H).next_to(leg_t, DOWN, buff=0.1)
        leg_p = Text("Equi-spaced training points", font_size=13,
                     color=GREEN_H).next_to(leg_r, DOWN, buff=0.1)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        self.play(Create(ax), run_time=0.5)
        self.play(FadeIn(eq_pts), run_time=0.5)
        self.play(Create(true_c), FadeIn(leg_t), run_time=0.8)
        self.play(Create(runge_c), FadeIn(leg_r), FadeIn(leg_p), run_time=0.8)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body),
            FadeOut(ax), FadeOut(eq_pts), FadeOut(true_c),
            FadeOut(runge_c), FadeOut(leg_t), FadeOut(leg_r), FadeOut(leg_p),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 29 — OVERFITTING PROS/CONS
    # ─────────────────────────────────────────
    def scene_29_overfitting_pros_cons(self):
        sub = make_subtitle("Fixing and Understanding Overfitting")
        sec_title = make_section_title("Overfitting: Fixes & Root Causes",
                                       font_size=34)

        pros = [
            "Reduce polynomial degree (most direct)",
            "Add Ridge or Lasso regularisation",
            "Collect more training data",
            "Use Lasso for feature selection",
            "Cross-validate degree selection",
        ]
        cons = [
            "n+1 parameters for degree-n poly",
            "No built-in penalty in plain OLS",
            "High-degree terms amplify edge effects",
        ]
        pc = make_pros_cons(pros, cons, width=5.5, height=3.2)
        pc[0][0].set_stroke(color=GREEN_H)
        pc.shift(DOWN * 0.3)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(pc[0]), run_time=0.6)
        self.play(FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(pc), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 30 — UNDERFITTING
    # ─────────────────────────────────────────
    def scene_30_underfitting(self):
        sub = make_subtitle("Underfitting — Too Simple to Capture the Pattern")
        sec_title = make_section_title("Underfitting", font_size=40)

        body = Text(
            "Model is too simple to capture the true relationship — High Bias.",
            font_size=20, color=WHITE_H
        ).shift(UP * 1.8)
        if body.width > 11:
            body.scale(11 / body.width)

        headers = ["Signal", "Meaning"]
        rows = [
            ["Both Train & Test R^2 low", "Fails on both — structurally wrong"],
            ["Residuals show systematic curves", "Missed curvature in residuals"],
            ["Both learning curves plateau high", "More data won't help"],
        ]
        tbl = make_table_mob(headers, rows, col_widths=[4.8, 5.0], font_size=14)
        tbl.scale(0.9)
        tbl.shift(UP * 0.2)

        pros = [
            "Increase polynomial degree",
            "Add more input features",
            "Reduce regularisation (lower alpha)",
            "Consider a different model family",
        ]
        cons = [
            "Chosen degree too low",
            "Over-regularised model (alpha too large)",
            "Important features are missing",
        ]
        pc = make_pros_cons(pros, cons, width=5.0, height=2.5)
        pc.shift(DOWN * 1.9)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        self.play(FadeIn(tbl), run_time=0.7)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body),
            FadeOut(tbl), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 31 — VISUAL INSPECTION
    # ─────────────────────────────────────────
    def scene_31_visual_inspection(self):
        sub = make_subtitle("Method 1: Visual Inspection — Start Here")
        sec_title = make_section_title("Degree Selection: Visual Inspection",
                                       font_size=32)

        body = Text(
            "Plot y vs x. Count how many bends the data seems to have.\n"
            "One hill -> degree 2.  S-shape -> degree 3.",
            font_size=19, color=WHITE_H
        ).shift(UP * 1.6)

        # Simple scatter with curvature
        ax = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 8, 2],
            x_length=5.5,
            y_length=2.8,
            axis_config={"color": GRAY_H, "stroke_width": 1.0},
            tips=False,
        ).shift(DOWN * 0.6)

        np.random.seed(1)
        xs_p = np.linspace(-2.5, 2.5, 18)
        ys_p = xs_p**2 - xs_p + 0.5 + np.random.randn(18) * 0.5
        dts = VGroup(*[
            Dot(ax.c2p(x, y), radius=0.07, color=BLUE_H)
            for x, y in zip(xs_p, ys_p)
        ])
        fit = ax.plot(lambda x: x**2 - x + 0.5, x_range=[-2.5, 2.5],
                      color=GREEN_H, stroke_width=2.5)
        hint = Text("1 bend -> Degree 2", font_size=14, color=GREEN_H).next_to(
            ax, DOWN, buff=0.1
        )

        pros = ["Quick and intuitive",
                "Grounds you in the data first"]
        cons = ["Subjective with noisy data",
                "No quantitative validation"]
        pc = make_pros_cons(pros, cons, width=4.5, height=1.8)
        pc.shift(DOWN * 2.2)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        self.play(Create(ax), FadeIn(dts), run_time=0.6)
        self.play(Create(fit), FadeIn(hint), run_time=0.6)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.5)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body),
            FadeOut(ax), FadeOut(dts), FadeOut(fit), FadeOut(hint),
            FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 32 — CROSS-VALIDATION
    # ─────────────────────────────────────────
    def scene_32_cross_validation(self):
        sub = make_subtitle("Method 2: K-Fold Cross-Validation — The Gold Standard")
        sec_title = make_section_title("Degree Selection: Cross-Validation",
                                       font_size=32)

        body = Text(
            "Split data into k folds. For each degree: train on k-1 folds,\n"
            "evaluate on the held-out fold, repeat k times, average the error.",
            font_size=18, color=WHITE_H
        ).shift(UP * 1.7)

        # CV fold visualisation
        n_folds = 5
        fold_rects = VGroup()
        fold_lbls = VGroup()
        for fold_i in range(n_folds):
            for blk in range(n_folds):
                is_val = (blk == fold_i)
                rect = Rectangle(
                    width=1.4, height=0.45,
                    fill_color=RED_H if is_val else BLUE_H,
                    fill_opacity=0.85,
                    stroke_width=0.8, stroke_color=WHITE_H
                ).move_to(
                    RIGHT * (blk - 2) * 1.5
                    + DOWN * (fold_i - 2) * 0.6
                )
                fold_rects.add(rect)
                lbl = Text(
                    "VAL" if is_val else "TR",
                    font_size=10, color=WHITE_H
                ).move_to(rect.get_center())
                fold_lbls.add(lbl)

        fold_grp = VGroup(fold_rects, fold_lbls)
        fold_grp.shift(DOWN * 0.2)

        leg_tr = Text("Train fold", font_size=13, color=BLUE_H).to_corner(
            DR, buff=1.4
        )
        leg_vl = Text("Validation fold", font_size=13,
                      color=RED_H).next_to(leg_tr, UP, buff=0.1)

        pros = [
            "Uses all data for train & val",
            "Low variance estimate",
            "Works for any metric",
            "Tune degree + alpha together",
        ]
        cons = ["k times more expensive",
                "With tiny datasets, each fold is small"]
        pc = make_pros_cons(pros, cons, width=4.8, height=2.0)
        pc.shift(DOWN * 2.0)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        self.play(FadeIn(fold_grp), run_time=0.8)
        self.play(FadeIn(leg_tr), FadeIn(leg_vl), run_time=0.4)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body),
            FadeOut(fold_grp), FadeOut(leg_tr), FadeOut(leg_vl),
            FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 33 — LEARNING CURVES
    # ─────────────────────────────────────────
    def scene_33_learning_curves(self):
        sub = make_subtitle("Method 3: Learning Curves — Diagnose Bias vs Variance")
        sec_title = make_section_title("Degree Selection: Learning Curves",
                                       font_size=32)

        ax = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 5, 1],
            x_length=7.5,
            y_length=3.2,
            axis_config={"color": GRAY_H, "stroke_width": 1.2},
            tips=False,
        ).shift(DOWN * 0.7)
        xl = Text("Training Set Size", font_size=14, color=GRAY_H).next_to(
            ax.x_axis, DOWN, buff=0.2
        )
        yl = Text("Error (RMSE)", font_size=14, color=GRAY_H).next_to(
            ax.y_axis, UP, buff=0.05
        )

        # Good fit learning curves
        train_fn = lambda x: max(0.4, 2.5 * np.exp(-x * 0.4) + 0.4)
        val_fn   = lambda x: max(0.45, 3.5 * np.exp(-x * 0.3) + 0.55)

        train_c = ax.plot(train_fn, x_range=[0.1, 10], color=BLUE_H,
                          stroke_width=2.5)
        val_c   = ax.plot(val_fn, x_range=[0.1, 10], color=RED_H,
                          stroke_width=2.5)

        lbl_tr = Text("Train error", font_size=14, color=BLUE_H).to_corner(
            UR, buff=1.3
        )
        lbl_vl = Text("Validation error", font_size=14, color=RED_H).next_to(
            lbl_tr, DOWN, buff=0.1
        )

        rules = VGroup()
        rule_texts = [
            "Both plateau HIGH  ->  Underfitting  ->  Increase degree",
            "Train low, Val high gap  ->  Overfitting  ->  Regularise",
            "Both converge LOW  ->  Good fit",
        ]
        rule_colors = [ORANGE_H, RED_H, GREEN_H]
        for rt, rc in zip(rule_texts, rule_colors):
            t = Text(rt, font_size=13, color=rc)
            if t.width > 11:
                t.scale(11 / t.width)
            rules.add(t)
        rules.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rules.to_edge(DOWN, buff=0.6)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.5)
        self.play(Create(train_c), FadeIn(lbl_tr), run_time=0.7)
        self.play(Create(val_c), FadeIn(lbl_vl), run_time=0.7)
        self.play(FadeIn(rules), run_time=0.6)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(ax),
            FadeOut(xl), FadeOut(yl), FadeOut(train_c), FadeOut(val_c),
            FadeOut(lbl_tr), FadeOut(lbl_vl), FadeOut(rules),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 34 — AIC AND BIC
    # ─────────────────────────────────────────
    def scene_34_aic_bic(self):
        sub = make_subtitle("Method 4: AIC and BIC — Statistical Criteria")
        sec_title = make_section_title("Degree Selection: AIC & BIC",
                                       font_size=34)

        aic_f = MathTex(
            r"\text{AIC} = 2k - 2\ln(L)",
            font_size=36, color=WHITE_H
        )
        bic_f = MathTex(
            r"\text{BIC} = k \cdot \ln(n) - 2\ln(L)",
            font_size=36, color=WHITE_H
        )
        formulas = VGroup(aic_f, bic_f).arrange(RIGHT, buff=1.2)
        fbox = make_formula_box(
            formulas,
            label_text=(
                "k = number of params, n = sample size, L = max likelihood. Lower = better."
            ),
            width=10.5, height=1.4
        )
        fbox.shift(UP * 0.9)

        body = Text(
            "Both penalise model complexity while rewarding fit.\n"
            "BIC penalises extra parameters more — favours simpler models with large n.",
            font_size=18, color=WHITE_H
        ).shift(DOWN * 0.1)

        pros = [
            "Single comparable number across degrees",
            "Theoretically grounded penalisation",
            "BIC consistent — selects true model as n -> inf",
        ]
        cons = [
            "Requires computing likelihood",
            "Designed for nested model comparison",
            "Not always ideal for prediction",
        ]
        pc = make_pros_cons(pros, cons, width=5.0, height=2.4)
        pc.shift(DOWN * 1.9)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(body), run_time=0.5)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox),
            FadeOut(body), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 35 — ADJUSTED R2
    # ─────────────────────────────────────────
    def scene_35_adjusted_r2(self):
        sub = make_subtitle("Method 5: Adjusted R^2 — Quick Check")
        sec_title = make_section_title("Degree Selection: Adjusted R\u00b2",
                                       font_size=34)

        formula = MathTex(
            r"\text{Adj-}R^2 = 1 - \frac{(1 - R^2)(n-1)}{n-k-1}",
            font_size=42, color=WHITE_H
        )
        fbox = make_formula_box(
            formula,
            label_text="n = samples, k = number of polynomial features",
            width=8.5, height=1.4
        )
        fbox.shift(UP * 0.8)

        body = Text(
            "Only increases if the new polynomial term genuinely improves the model.\n"
            "Decreases if you add a useless term.",
            font_size=19, color=WHITE_H
        ).shift(DOWN * 0.15)

        pros = ["Quick to compute — no refitting",
                "Penalises unnecessary complexity"]
        cons = ["Still uses training data — can overfit",
                "Cross-validation is more reliable"]
        pc = make_pros_cons(pros, cons, width=5.0, height=2.0)
        pc.shift(DOWN * 1.9)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(body), run_time=0.5)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox),
            FadeOut(body), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 36 — TRAIN vs VALIDATION ERROR CHART
    # ─────────────────────────────────────────
    def scene_36_error_curve(self):
        sub = make_subtitle("Train vs. Validation Error — Finding the Optimal Degree")
        sec_title = make_section_title("Train vs. Validation Error by Degree",
                                       font_size=31)

        ax = Axes(
            x_range=[1, 10, 1],
            y_range=[0, 10, 2],
            x_length=8.0,
            y_length=3.8,
            axis_config={"color": GRAY_H, "stroke_width": 1.5},
            tips=False,
        ).shift(DOWN * 0.5)
        xl = Text("Polynomial Degree", font_size=16, color=GRAY_H).next_to(
            ax.x_axis, DOWN, buff=0.25
        )
        yl = Text("MSE", font_size=16, color=GRAY_H).next_to(
            ax.y_axis, UP, buff=0.08
        )

        degs = list(range(1, 11))
        tr_err = [5.2, 2.1, 1.2, 0.8, 0.5, 0.3, 0.2, 0.1, 0.05, 0.02]
        vl_err = [5.4, 2.3, 1.4, 1.3, 1.5, 2.0, 3.1, 4.8, 7.2, 9.5]

        def make_c(data, color):
            clamped = [min(d, 10) for d in data]
            pts = [ax.c2p(d, v) for d, v in zip(degs, clamped)]
            c = VMobject()
            c.set_points_as_corners(pts)
            c.set_color(color)
            c.set_stroke(width=2.5)
            return c

        tr_c = make_c(tr_err, BLUE_H)
        vl_c = make_c(vl_err, RED_H)

        opt_d = 3
        opt_val = vl_err[opt_d - 1]
        opt_pt = ax.c2p(opt_d, opt_val)
        opt_dot = Dot(opt_pt, radius=0.13, color=YELLOW_H)
        opt_lbl = Text("Optimal", font_size=13,
                       color=YELLOW_H).next_to(opt_dot, UR, buff=0.1)

        leg_tr = Text("Train error", font_size=14, color=BLUE_H).to_corner(
            UR, buff=1.1
        )
        leg_vl = Text("Validation error", font_size=14, color=RED_H).next_to(
            leg_tr, DOWN, buff=0.1
        )

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.6)
        self.play(Create(tr_c), FadeIn(leg_tr), run_time=0.7)
        self.play(Create(vl_c), FadeIn(leg_vl), run_time=0.7)
        self.play(FadeIn(opt_dot), FadeIn(opt_lbl), run_time=0.5)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(ax),
            FadeOut(xl), FadeOut(yl), FadeOut(tr_c), FadeOut(vl_c),
            FadeOut(opt_dot), FadeOut(opt_lbl),
            FadeOut(leg_tr), FadeOut(leg_vl),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 37 — REGULARISATION OVERVIEW
    # ─────────────────────────────────────────
    def scene_37_regularisation_overview(self):
        sub = make_subtitle("Regularisation — Controlling Model Complexity")
        sec_title = make_section_title("Regularisation", font_size=40)

        body = Text(
            "Adds a penalty on the SIZE of the coefficients to the cost function.\n"
            "Forces small coefficients -> smoother, better-generalising curves.",
            font_size=20, color=WHITE_H
        ).shift(UP * 1.5)

        cards = VGroup()
        data = [
            ("Ridge (L2)", "Shrinks all towards 0,\nnever exactly zero.", BLUE_H),
            ("Lasso (L1)", "Can set coefficients\nto EXACTLY zero.", GREEN_H),
            ("ElasticNet", "Mix of L1 + L2.\nBest default for poly.", PURPLE_H),
        ]
        for name, desc, color in data:
            box = RoundedRectangle(
                width=3.4, height=1.8,
                corner_radius=0.1,
                fill_color="#111a2e", fill_opacity=1,
                stroke_color=color, stroke_width=2.0
            )
            t = Text(name, font_size=18, color=color, weight=BOLD)
            t.next_to(box.get_top(), DOWN, buff=0.18)
            d = Text(desc, font_size=14, color=WHITE_H)
            d.next_to(t, DOWN, buff=0.18)
            if d.width > 3.0:
                d.scale(3.0 / d.width)
            cards.add(VGroup(box, t, d))

        cards.arrange(RIGHT, buff=0.35)
        cards.shift(DOWN * 0.55)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        for c in cards:
            self.play(FadeIn(c), run_time=0.45)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body), FadeOut(cards),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 38 — RIDGE REGRESSION
    # ─────────────────────────────────────────
    def scene_38_ridge(self):
        sub = make_subtitle("Ridge Regression — L2 Regularisation")
        sec_title = make_section_title("Ridge Regression (L2)", font_size=36)

        formula = MathTex(
            r"\text{Cost} = \text{MSE} + \alpha \sum_j \beta_j^2",
            font_size=40, color=WHITE_H
        )
        fbox = make_formula_box(
            formula,
            label_text="Penalises the sum of SQUARED coefficients. Constraint region = sphere.",
            width=8.5, height=1.4
        )
        fbox.shift(UP * 1.2)

        body = Text(
            "Shrinks all coefficients toward zero but NEVER to exactly zero.\n"
            "Acts as a smoothness enforcer — resists extreme oscillations.",
            font_size=18, color=WHITE_H
        ).shift(DOWN * 0.05)

        pros = [
            "Always has a unique closed-form solution",
            "Smoothly shrinks coefficients",
            "Works when all poly terms contribute",
            "Reduces multicollinearity impact",
        ]
        cons = [
            "Cannot zero out coefficients",
            "Still includes all polynomial terms",
            "Biased estimator",
        ]
        pc = make_pros_cons(pros, cons, width=5.2, height=2.4)
        pc.shift(DOWN * 1.7)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(body), run_time=0.5)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox),
            FadeOut(body), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 39 — LASSO REGRESSION
    # ─────────────────────────────────────────
    def scene_39_lasso(self):
        sub = make_subtitle("Lasso Regression — L1 Regularisation")
        sec_title = make_section_title("Lasso Regression (L1)", font_size=36)

        formula = MathTex(
            r"\text{Cost} = \text{MSE} + \alpha \sum_j |\beta_j|",
            font_size=40, color=WHITE_H
        )
        fbox = make_formula_box(
            formula,
            label_text="Penalises sum of ABSOLUTE values. Constraint region = diamond (L1 ball).",
            width=9.0, height=1.4
        )
        fbox.shift(UP * 1.7)

        geom_note = Text(
            "Why zeros? The L1 diamond has CORNERS on the axes.\n"
            "OLS contours most often hit a corner -> one or more b = 0 exactly.",
            font_size=16, color=YELLOW_H
        ).shift(UP * 0.2)

        pros = [
            "Automatic feature selection",
            "Produces sparse, interpretable models",
            "Zeros out unnecessary poly terms",
        ]
        cons = [
            "No closed-form solution (coordinate descent)",
            "Unstable with correlated poly features",
            "Needs large max_iter for high degree",
        ]
        pc = make_pros_cons(pros, cons, width=5.2, height=2.5)
        pc.shift(DOWN * 1.8)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(geom_note), run_time=0.5)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox),
            FadeOut(geom_note), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 40 — ELASTICNET
    # ─────────────────────────────────────────
    def scene_40_elasticnet(self):
        sub = make_subtitle("ElasticNet — The Best Default for Polynomial Regression")
        sec_title = make_section_title("ElasticNet (L1 + L2)", font_size=36)

        formula = MathTex(
            r"\text{Cost} = \text{MSE} + \alpha \left[\rho \sum|\beta_j|"
            r" + (1-\rho)\sum\beta_j^2\right]",
            font_size=34, color=WHITE_H
        )
        fbox = make_formula_box(
            formula,
            label_text=(
                "rho = l1_ratio: 0 -> Ridge, 1 -> Lasso, 0.5 -> equal mix"
            ),
            width=10.0, height=1.4
        )
        fbox.shift(UP * 1.5)

        body = Text(
            "Inherits Ridge's stability AND Lasso's sparsity.\n"
            "Groups correlated polynomial terms — unlike Lasso which arbitrarily picks one.",
            font_size=17, color=WHITE_H
        ).shift(UP * 0.1)

        pros = [
            "Groups correlated polynomial terms",
            "Can produce sparse solutions",
            "More stable than Lasso for correlated features",
            "Single knob (l1_ratio) to blend L1/L2",
        ]
        cons = [
            "Two hyperparameters to tune (alpha + l1_ratio)",
            "No closed-form solution",
            "More complex to interpret than Ridge alone",
        ]
        pc = make_pros_cons(pros, cons, width=5.2, height=2.4)
        pc.shift(DOWN * 1.7)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(body), run_time=0.5)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox),
            FadeOut(body), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 41 — REGULARISATION COMPARISON TABLE
    # ─────────────────────────────────────────
    def scene_41_reg_comparison(self):
        sub = make_subtitle("Ridge vs. Lasso vs. ElasticNet — Side-by-Side")
        sec_title = make_section_title("Regularisation Comparison", font_size=34)

        headers = ["Property", "Ridge (L2)", "Lasso (L1)", "ElasticNet"]
        rows = [
            ["Coeff behaviour", "Shrinks, never 0", "Can be exactly 0", "Both"],
            ["Feature selection", "No", "Yes", "Partial"],
            ["Correlated feats", "Distributes weight", "Picks one, zeros rest",
             "Groups them"],
            ["Solution type", "Closed form", "Coordinate descent", "Iterative"],
            ["Best for poly", "All terms matter", "Few terms matter",
             "Best default"],
        ]
        tbl = make_table_mob(headers, rows,
                             col_widths=[2.8, 2.5, 2.8, 2.5],
                             font_size=14)
        tbl.scale(0.88)
        tbl.shift(DOWN * 0.2)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(tbl), run_time=0.9)
        self.wait(5)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(tbl), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 42 — ALPHA EFFECT
    # ─────────────────────────────────────────
    def scene_42_alpha_effect(self):
        sub = make_subtitle("The alpha Hyperparameter — Controlling Regularisation Strength")
        sec_title = make_section_title("The alpha Hyperparameter", font_size=34)

        ax = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 10, 4],
            x_length=7.5,
            y_length=3.5,
            axis_config={"color": GRAY_H, "stroke_width": 1.2},
            tips=False,
        ).shift(DOWN * 0.5)

        np.random.seed(9)
        xs_a = np.linspace(-2.8, 2.8, 22)
        ys_a = xs_a**2 - xs_a + 0.5 + np.random.randn(22) * 0.8
        dts = VGroup(*[
            Dot(ax.c2p(x, y), radius=0.07, color=BLUE_H)
            for x, y in zip(xs_a, ys_a)
        ])

        # alpha=0: overfit (wiggly)
        over_c = ax.plot(
            lambda x: x**2 - x + 0.5 + 0.4 * np.sin(5 * x),
            x_range=[-2.8, 2.8], color=RED_H, stroke_width=2.5
        )
        # Good fit
        good_c = ax.plot(
            lambda x: x**2 - x + 0.5,
            x_range=[-2.8, 2.8], color=GREEN_H, stroke_width=2.5
        )
        # High alpha: underfit (nearly flat)
        under_c = DashedVMobject(
            ax.plot(
                lambda x: 0.15 * x + 1.5,
                x_range=[-2.8, 2.8], color=PURPLE_H, stroke_width=2.5,
            ),
            num_dashes=22, dashed_ratio=0.6
        )

        leg_o = MathTex(r"\alpha=0\;\text{(overfit)}", font_size=26, color=RED_H).to_corner(UR, buff=1.0)
        leg_g = MathTex(
            r"\alpha=1.0\;\text{(good fit)}", font_size=26, color=GREEN_H
        ).next_to(leg_o, DOWN, buff=0.1)
        leg_u = MathTex(
            r"\alpha=100\;\text{(underfit)}", font_size=26, color=PURPLE_H
        ).next_to(leg_g, DOWN, buff=0.1)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(Create(ax), FadeIn(dts), run_time=0.6)
        self.play(Create(over_c), FadeIn(leg_o), run_time=0.7)
        self.play(Create(good_c), FadeIn(leg_g), run_time=0.7)
        self.play(Create(under_c), FadeIn(leg_u), run_time=0.7)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(ax), FadeOut(dts),
            FadeOut(over_c), FadeOut(good_c), FadeOut(under_c),
            FadeOut(leg_o), FadeOut(leg_g), FadeOut(leg_u),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 43 — FEATURE SCALING OVERVIEW
    # ─────────────────────────────────────────
    def scene_43_feature_scaling(self):
        sub = make_subtitle("Feature Scaling — Why It Matters")
        sec_title = make_section_title("Feature Scaling", font_size=38)

        problem = Text(
            "When you compute polynomial features:\n"
            "x might be in the hundreds, but x^2 can be in the millions!\n"
            "This massive scale difference causes problems for regularisation.",
            font_size=19, color=WHITE_H
        ).shift(UP * 1.2)

        # Pipeline order diagram
        steps = ["Raw x", "PolynomialFeatures", "StandardScaler", "Model"]
        colors = [GRAY_H, BLUE_H, GREEN_H, ORANGE_H]
        step_grp = VGroup()
        for i, (step, color) in enumerate(zip(steps, colors)):
            box = RoundedRectangle(
                width=2.4, height=0.65,
                corner_radius=0.1,
                fill_color="#111a2e", fill_opacity=1,
                stroke_color=color, stroke_width=2.0
            )
            lbl = Text(step, font_size=14, color=color)
            if lbl.width > 2.1:
                lbl.scale(2.1 / lbl.width)
            lbl.move_to(box.get_center())
            step_grp.add(VGroup(box, lbl))

        arrows_grp = VGroup()
        step_grp.arrange(RIGHT, buff=0.9)
        step_grp.shift(DOWN * 1.3)
        for i in range(len(steps) - 1):
            a = Arrow(
                step_grp[i].get_right(),
                step_grp[i + 1].get_left(),
                buff=0.05, stroke_width=2.0, color=YELLOW_H
            )
            arrows_grp.add(a)

        order_lbl = Text(
            "CORRECT ORDER: Raw x  ->  PolynomialFeatures  ->  StandardScaler  ->  Model",
            font_size=15, color=YELLOW_H
        ).to_edge(DOWN, buff=0.8)
        if order_lbl.width > 11:
            order_lbl.scale(11 / order_lbl.width)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(problem), run_time=0.5)
        self.play(FadeIn(step_grp), run_time=0.6)
        self.play(FadeIn(arrows_grp), run_time=0.5)
        self.play(FadeIn(order_lbl), run_time=0.5)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(problem),
            FadeOut(step_grp), FadeOut(arrows_grp), FadeOut(order_lbl),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 44 — STANDARD SCALER
    # ─────────────────────────────────────────
    def scene_44_standard_scaler(self):
        sub = make_subtitle("StandardScaler — Z-score Normalisation")
        sec_title = make_section_title("StandardScaler", font_size=38)

        formula = MathTex(
            r"x_{\text{scaled}} = \frac{x - \mu}{\sigma}",
            font_size=48, color=WHITE_H
        )
        fbox = make_formula_box(
            formula,
            label_text=(
                "mu = feature mean, sigma = std dev. Fit on TRAIN only. Transform both."
            ),
            width=8.5, height=1.5
        )
        fbox.shift(UP * 1.2)

        body = Text(
            "Transforms each feature to mean=0 and std=1.",
            font_size=19, color=WHITE_H
        ).shift(DOWN * 0.05)

        pros = [
            "Makes regularisation fair for all features",
            "Prevents numerical instability in Normal Eq",
            "Speeds up gradient descent convergence",
            "Reduces multicollinearity (combined with centering)",
        ]
        cons = [
            "Sensitive to outliers (distorts mu and sigma)",
            "Does not preserve original distribution shape",
            "Coefficients in standardised units",
        ]
        pc = make_pros_cons(pros, cons, width=5.2, height=2.4)
        pc.shift(DOWN * 1.6)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(body), run_time=0.4)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox),
            FadeOut(body), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 45 — MINMAX SCALER
    # ─────────────────────────────────────────
    def scene_45_minmax(self):
        sub = make_subtitle("MinMaxScaler vs StandardScaler")
        sec_title = make_section_title("MinMaxScaler", font_size=38)

        formula = MathTex(
            r"x_{\text{scaled}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}",
            font_size=44, color=WHITE_H
        )
        fbox = make_formula_box(
            formula,
            label_text="Scales to the range [0, 1]",
            width=8.0, height=1.4
        )
        fbox.shift(UP * 1.1)

        pros = ["Preserves zero values",
                "Bounded output — easy to reason about"]
        cons = [
            "Very sensitive to outliers",
            "One outlier compresses all other values",
            "For polynomial reg, StandardScaler preferred",
        ]
        pc = make_pros_cons(pros, cons, width=5.2, height=2.4)
        pc.shift(DOWN * 0.9)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 46 — WHY CENTERING REDUCES MULTICOLLINEARITY
    # ─────────────────────────────────────────
    def scene_46_centering(self):
        sub = make_subtitle("Centering x Reduces Multicollinearity Between Powers")
        sec_title = make_section_title("Why Centering Helps", font_size=36)

        body = Text(
            "If x ranges from 10 to 20, then x and x^2 are highly correlated (cor ~ 0.99).",
            font_size=19, color=WHITE_H
        ).shift(UP * 1.6)
        if body.width > 11:
            body.scale(11 / body.width)

        before = RoundedRectangle(
            width=5.0, height=1.6,
            corner_radius=0.1,
            fill_color=DARK_RD, fill_opacity=1,
            stroke_color=RED_H, stroke_width=1.8
        ).shift(LEFT * 3.0 + DOWN * 0.1)
        b_t = Text("Before centering:", font_size=15, color=RED_H, weight=BOLD)
        b_t.next_to(before.get_top(), DOWN, buff=0.15)
        b_c = Text(
            "x in [10, 20]\ncor(x, x^2) ~ 0.99",
            font_size=14, color=WHITE_H
        ).next_to(b_t, DOWN, buff=0.15)

        after = RoundedRectangle(
            width=5.0, height=1.6,
            corner_radius=0.1,
            fill_color=DARK_GR, fill_opacity=1,
            stroke_color=GREEN_H, stroke_width=1.8
        ).shift(RIGHT * 3.0 + DOWN * 0.1)
        a_t = Text("After centering (x - 15):", font_size=15,
                   color=GREEN_H, weight=BOLD)
        a_t.next_to(after.get_top(), DOWN, buff=0.15)
        a_c = Text(
            "x in [-5, 5]\ncor(x, x^2) drops dramatically",
            font_size=14, color=WHITE_H
        ).next_to(a_t, DOWN, buff=0.15)
        if a_c.width > 4.6:
            a_c.scale(4.6 / a_c.width)

        arrow = Arrow(before.get_right(), after.get_left(),
                      buff=0.05, color=YELLOW_H, stroke_width=2.5)

        note = Text(
            "Numerically more stable even before regularisation is applied.",
            font_size=16, color=YELLOW_H
        ).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(body), run_time=0.5)
        self.play(
            FadeIn(before), FadeIn(b_t), FadeIn(b_c),
            run_time=0.6
        )
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(
            FadeIn(after), FadeIn(a_t), FadeIn(a_c),
            run_time=0.6
        )
        self.play(FadeIn(note), run_time=0.5)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(body),
            FadeOut(before), FadeOut(b_t), FadeOut(b_c),
            FadeOut(arrow), FadeOut(after), FadeOut(a_t), FadeOut(a_c),
            FadeOut(note),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 47 — FEATURE EXPLOSION
    # ─────────────────────────────────────────
    def scene_47_feature_explosion(self):
        sub = make_subtitle("Feature Explosion — The Curse of Dimensionality")
        sec_title = make_section_title("Feature Explosion", font_size=36)

        formula = MathTex(
            r"\text{Features after expansion} = \binom{n+d}{d} = "
            r"\frac{(n+d)!}{n! \cdot d!}",
            font_size=30, color=WHITE_H
        )
        fbox = make_formula_box(
            formula,
            label_text="n = original features, d = degree. Grows explosively!",
            width=10.0, height=1.4
        )
        fbox.shift(UP * 1.5)

        headers = ["Orig. Features (n)", "Degree (d)", "After Expansion", "Risk"]
        rows = [
            ["1", "2", "3", "Trivial"],
            ["5", "2", "21", "Manageable"],
            ["10", "3", "286", "High overfit risk"],
            ["50", "2", "1,326", "Use kernel methods"],
            ["100", "3", "176,851", "Avoid — use SVR/NN"],
        ]
        tbl = make_table_mob(headers, rows,
                             col_widths=[2.5, 2.0, 2.5, 3.2],
                             font_size=14)
        tbl.scale(0.88)
        tbl.shift(DOWN * 0.7)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(tbl), run_time=0.8)
        self.wait(4.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox), FadeOut(tbl),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 48 — FEATURE EXPLOSION PROS/CONS
    # ─────────────────────────────────────────
    def scene_48_explosion_pros_cons(self):
        sub = make_subtitle("Feature Explosion — When to Use and When to Avoid")
        sec_title = make_section_title("Feature Explosion: Use vs. Avoid",
                                       font_size=32)

        pros = [
            "Small number of features (<=5)",
            "Low degree (2-3)",
            "Dataset large enough",
            "Regularisation applied (Ridge/Lasso)",
        ]
        cons = [
            "Many original features (n > 10)",
            "High degree (> 3)",
            "Small dataset (fewer rows than features)",
            "Use kernel SVR instead",
        ]
        pc = make_pros_cons(pros, cons, width=5.5, height=3.0)
        pc.shift(UP * 0.2)

        kernel_note = Text(
            "Kernel Trick: SVR with polynomial kernel computes features IMPLICITLY.",
            font_size=15, color=YELLOW_H
        ).to_edge(DOWN, buff=0.75)
        if kernel_note.width > 11:
            kernel_note.scale(11 / kernel_note.width)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.play(FadeIn(kernel_note), run_time=0.5)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(pc), FadeOut(kernel_note),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 49 — MSE AND RMSE
    # ─────────────────────────────────────────
    def scene_49_mse_rmse(self):
        sub = make_subtitle("Evaluation Metrics — MSE and RMSE")
        sec_title = make_section_title("Metrics: MSE & RMSE", font_size=36)

        mse_f = MathTex(
            r"\text{MSE} = \frac{1}{n} \sum (y_i - \hat{y}_i)^2",
            font_size=36, color=WHITE_H
        )
        rmse_f = MathTex(
            r"\text{RMSE} = \sqrt{\text{MSE}}",
            font_size=36, color=WHITE_H
        )
        formulas = VGroup(mse_f, rmse_f).arrange(RIGHT, buff=1.0)
        fbox = make_formula_box(
            formulas,
            label_text=(
                "MSE: units = y^2. RMSE: same units as y. Most interpretable."
            ),
            width=10.5, height=1.4
        )
        fbox.shift(UP * 1.5)

        pros_mse = ["Differentiable — works with gradient descent",
                    "Penalises large errors heavily", "Convex — one global minimum"]
        cons_mse = ["Not in same units as y", "Sensitive to outliers"]

        pros_rmse = ["Same units as y", "Directly interpretable"]
        cons_rmse = ["Still sensitive to outliers",
                     "Not right when all errors matter equally"]

        mse_pc = make_pros_cons(pros_mse, cons_mse, width=5.5, height=2.4)
        mse_pc.shift(DOWN * 1.5)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(mse_pc[0]), FadeIn(mse_pc[1]), run_time=0.6)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox), FadeOut(mse_pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 50 — MAE AND R2
    # ─────────────────────────────────────────
    def scene_50_mae_r2(self):
        sub = make_subtitle("Evaluation Metrics — MAE and R^2")
        sec_title = make_section_title("Metrics: MAE & R\u00b2", font_size=36)

        mae_f = MathTex(
            r"\text{MAE} = \frac{1}{n} \sum |y_i - \hat{y}_i|",
            font_size=34, color=WHITE_H
        )
        r2_f = MathTex(
            r"R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}",
            font_size=34, color=WHITE_H
        )
        formulas = VGroup(mae_f, r2_f).arrange(RIGHT, buff=1.0)
        fbox = make_formula_box(
            formulas,
            label_text="MAE: same units, robust. R^2: (- inf, 1]. 1 = perfect fit.",
            width=10.5, height=1.4
        )
        fbox.shift(UP * 1.5)

        warn = RoundedRectangle(
            width=10.0, height=1.1,
            corner_radius=0.1,
            fill_color="#2a1a00", fill_opacity=1,
            stroke_color=YELLOW_H, stroke_width=2
        ).shift(UP * 0.15)
        warn_t = Text(
            "WARNING: Adding more polynomial terms ALWAYS increases training R^2!\n"
            "Never use it alone to select degree. Always evaluate on test data.",
            font_size=14, color=YELLOW_H
        ).move_to(warn.get_center())
        if warn_t.width > 9.6:
            warn_t.scale(9.6 / warn_t.width)

        pros_mae = ["Robust to outliers", "Intuitive: average absolute mistake",
                    "Same units as y"]
        cons_mae = ["Not differentiable at 0", "Treats all errors equally"]
        pc = make_pros_cons(pros_mae, cons_mae, width=5.2, height=2.2)
        pc.shift(DOWN * 1.9)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(warn), FadeIn(warn_t), run_time=0.5)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox),
            FadeOut(warn), FadeOut(warn_t), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 51 — ADJUSTED R2 AND MAPE
    # ─────────────────────────────────────────
    def scene_51_adj_r2_mape(self):
        sub = make_subtitle("Adjusted R^2 and MAPE")
        sec_title = make_section_title("Metrics: Adj R\u00b2 & MAPE", font_size=36)

        adj_f = MathTex(
            r"\text{Adj-}R^2 = 1 - \frac{(1-R^2)(n-1)}{n-k-1}",
            font_size=32, color=WHITE_H
        )
        mape_f = MathTex(
            r"\text{MAPE} = \frac{100}{n} \sum \frac{|y_i - \hat{y}_i|}{|y_i|}",
            font_size=32, color=WHITE_H
        )
        formulas = VGroup(adj_f, mape_f).arrange(DOWN, buff=0.5)
        fbox = make_formula_box(
            formulas,
            label_text=(
                "Adj R^2: penalises complexity. MAPE: percentage error — undefined when y=0."
            ),
            width=9.5, height=2.0
        )
        fbox.shift(UP * 0.8)

        pros = ["Adj R^2 penalises extra poly terms",
                "MAPE: easy to communicate ('off by X%')",
                "MAPE scale-free — comparable across datasets"]
        cons = [
            "Adj R^2 still a training metric",
            "MAPE undefined when y_i = 0",
            "MAPE asymmetric penalty",
        ]
        pc = make_pros_cons(pros, cons, width=5.2, height=2.2)
        pc.shift(DOWN * 1.8)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(fbox), run_time=0.7)
        self.play(FadeIn(pc[0]), FadeIn(pc[1]), run_time=0.6)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(fbox), FadeOut(pc),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 52 — CONFIDENCE AND PREDICTION INTERVALS
    # ─────────────────────────────────────────
    def scene_52_ci_pi(self):
        sub = make_subtitle("Confidence Intervals vs. Prediction Intervals")
        sec_title = make_section_title("CI vs. Prediction Interval", font_size=34)

        ci_f = MathTex(
            r"\hat{y}_0 \pm t \cdot \hat{\sigma} \cdot "
            r"\sqrt{x_0^T (X^T X)^{-1} x_0}",
            font_size=26, color=WHITE_H
        )
        ci_box = make_formula_box(
            ci_f,
            label_text=(
                "CI: range containing the AVERAGE y at x0. Narrowest at mean of x."
            ),
            width=9.0, height=1.4
        )
        ci_box.shift(UP * 1.7)

        pi_f = MathTex(
            r"\hat{y}_0 \pm t \cdot \hat{\sigma} \cdot "
            r"\sqrt{1 + x_0^T (X^T X)^{-1} x_0}",
            font_size=26, color=WHITE_H
        )
        pi_box = make_formula_box(
            pi_f,
            label_text=(
                "PI: range for ONE NEW individual observation. Always WIDER than CI."
            ),
            width=9.0, height=1.4
        )
        pi_box.shift(UP * 0.0)

        key = Text(
            "The '+1' inside the PI's square root accounts for individual observation variance.",
            font_size=16, color=YELLOW_H
        ).shift(DOWN * 1.15)
        if key.width > 11:
            key.scale(11 / key.width)

        analogy = Text(
            "CI: 'What range contains the AVERAGE salary for 5 yrs experience?'\n"
            "PI: 'What range contains THIS SPECIFIC person's salary at 5 yrs?'",
            font_size=16, color=GRAY_H
        ).shift(DOWN * 2.0)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(ci_box), run_time=0.7)
        self.play(FadeIn(pi_box), run_time=0.7)
        self.play(FadeIn(key), run_time=0.5)
        self.play(FadeIn(analogy), run_time=0.5)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(ci_box), FadeOut(pi_box),
            FadeOut(key), FadeOut(analogy),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 53 — SKLEARN PIPELINE
    # ─────────────────────────────────────────
    def scene_53_pipeline(self):
        sub = make_subtitle("The Correct scikit-learn Pipeline")
        sec_title = make_section_title("scikit-learn Pipeline", font_size=36)

        steps = [
            ("Raw x", GRAY_H),
            ("PolynomialFeatures\n(degree=d)", BLUE_H),
            ("StandardScaler", GREEN_H),
            ("Ridge / Lasso /\nElasticNet", ORANGE_H),
        ]
        boxes = VGroup()
        for label, color in steps:
            box = RoundedRectangle(
                width=2.5, height=0.85,
                corner_radius=0.1,
                fill_color="#111a2e", fill_opacity=1,
                stroke_color=color, stroke_width=2.0
            )
            lbl = Text(label, font_size=13, color=color)
            if lbl.width > 2.2:
                lbl.scale(2.2 / lbl.width)
            lbl.move_to(box.get_center())
            boxes.add(VGroup(box, lbl))

        boxes.arrange(RIGHT, buff=0.7)
        boxes.shift(UP * 0.8)

        arrows_grp = VGroup()
        for i in range(len(boxes) - 1):
            a = Arrow(
                boxes[i].get_right(),
                boxes[i + 1].get_left(),
                buff=0.05, stroke_width=2.0, color=YELLOW_H
            )
            arrows_grp.add(a)

        gs_title = Text("GridSearchCV: Tune degree and regularisation simultaneously",
                        font_size=17, color=YELLOW_H).shift(DOWN * 0.15)

        headers = ["Step", "Key Setting", "Why"]
        rows = [
            ["PolynomialFeatures", "include_bias=False", "Model handles intercept"],
            ["StandardScaler", "Fit on TRAIN only", "Prevent data leakage"],
            ["Ridge", "alpha search: log-spaced", "Controls regularisation"],
            ["GridSearchCV", "cv=5, n_jobs=-1", "Efficient, parallel CV"],
        ]
        tbl = make_table_mob(headers, rows,
                             col_widths=[2.8, 2.8, 3.8],
                             font_size=13)
        tbl.scale(0.88)
        tbl.shift(DOWN * 1.7)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(boxes), run_time=0.7)
        self.play(FadeIn(arrows_grp), run_time=0.5)
        self.play(FadeIn(gs_title), run_time=0.5)
        self.play(FadeIn(tbl), run_time=0.7)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(boxes),
            FadeOut(arrows_grp), FadeOut(gs_title), FadeOut(tbl),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 54 — HYPERPARAMETERS: POLYNOMIALFEATURES
    # ─────────────────────────────────────────
    def scene_54_hp_poly(self):
        sub = make_subtitle("PolynomialFeatures Hyperparameters")
        sec_title = make_section_title("PolynomialFeatures Hyperparameters",
                                       font_size=31)

        params = [
            ("degree", "default=2",
             "Max polynomial degree. Use 2-5. Select via GridSearchCV.",
             BLUE_H),
            ("include_bias", "default=True",
             "Set False when downstream model has fit_intercept=True.",
             GREEN_H),
            ("interaction_only", "default=False",
             "True: only cross-products (x1*x2), not pure powers (x^2).",
             ORANGE_H),
            ("order", "default='C'",
             "Memory layout. Leave as 'C' unless specific perf reason.",
             PURPLE_H),
        ]

        rows_grp = VGroup()
        for param, default, desc, color in params:
            row = VGroup()
            p_box = RoundedRectangle(
                width=2.2, height=0.82,
                corner_radius=0.08,
                fill_color="#111a2e", fill_opacity=1,
                stroke_color=color, stroke_width=1.5
            )
            p_lbl = Text(param, font_size=14, color=color, weight=BOLD)
            p_lbl.move_to(p_box.get_center() + UP * 0.12)
            d_lbl = Text(default, font_size=11, color=GRAY_H)
            d_lbl.move_to(p_box.get_center() + DOWN * 0.18)
            row.add(VGroup(p_box, p_lbl, d_lbl))

            desc_t = Text(desc, font_size=14, color=WHITE_H)
            if desc_t.width > 7.0:
                desc_t.scale(7.0 / desc_t.width)
            desc_t.next_to(row, RIGHT, buff=0.35)
            desc_t.set_y(row.get_center()[1])
            rows_grp.add(VGroup(row, desc_t))

        rows_grp.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rows_grp.shift(DOWN * 0.2)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        for row in rows_grp:
            self.play(FadeIn(row), run_time=0.35)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(rows_grp),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 55 — HYPERPARAMETERS: RIDGE
    # ─────────────────────────────────────────
    def scene_55_hp_ridge(self):
        sub = make_subtitle("Ridge Hyperparameters")
        sec_title = make_section_title("Ridge Hyperparameters", font_size=36)

        params = [
            ("alpha", "default=1.0",
             "Regularisation strength. MOST IMPORTANT. Search: [0.001, 0.01, 0.1, 1, 10, 100]",
             BLUE_H),
            ("solver", "default='auto'",
             "'svd' for stability; 'sag'/'saga' for very large datasets.",
             GREEN_H),
            ("tol", "default=1e-4",
             "Convergence tolerance for iterative solvers.",
             ORANGE_H),
            ("max_iter", "default=None",
             "Max iterations for iterative solvers. Increase if ConvergenceWarning.",
             PURPLE_H),
            ("random_state", "default=None",
             "Seed for 'sag'/'saga' solvers. Set for reproducibility.",
             YELLOW_H),
        ]

        rows_grp = VGroup()
        for param, default, desc, color in params:
            row = VGroup()
            p_box = RoundedRectangle(
                width=2.2, height=0.78,
                corner_radius=0.08,
                fill_color="#111a2e", fill_opacity=1,
                stroke_color=color, stroke_width=1.5
            )
            p_lbl = Text(param, font_size=13, color=color, weight=BOLD)
            p_lbl.move_to(p_box.get_center() + UP * 0.10)
            d_lbl = Text(default, font_size=11, color=GRAY_H)
            d_lbl.move_to(p_box.get_center() + DOWN * 0.17)
            row.add(VGroup(p_box, p_lbl, d_lbl))

            desc_t = Text(desc, font_size=13, color=WHITE_H)
            if desc_t.width > 7.0:
                desc_t.scale(7.0 / desc_t.width)
            desc_t.next_to(row, RIGHT, buff=0.35)
            desc_t.set_y(row.get_center()[1])
            rows_grp.add(VGroup(row, desc_t))

        rows_grp.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rows_grp.shift(DOWN * 0.1)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        for row in rows_grp:
            self.play(FadeIn(row), run_time=0.32)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(rows_grp),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 56 — HYPERPARAMETERS: LASSO AND ELASTICNET
    # ─────────────────────────────────────────
    def scene_56_hp_lasso_enet(self):
        sub = make_subtitle("Lasso and ElasticNet Hyperparameters")
        sec_title = make_section_title("Lasso & ElasticNet Hyperparameters",
                                       font_size=32)

        lasso_params = [
            ("alpha", "default=1.0", "Regularisation strength.", BLUE_H),
            ("max_iter", "default=1000",
             "Set 10000+ for high-degree poly to avoid ConvergenceWarning.", RED_H),
            ("warm_start", "default=False",
             "True: reuse prev solution. Speeds up GridSearchCV.", GREEN_H),
            ("selection", "default='cyclic'",
             "'random' can converge faster on large problems.", ORANGE_H),
        ]
        enet_params = [
            ("alpha", "default=1.0", "Overall regularisation strength.", BLUE_H),
            ("l1_ratio", "default=0.5",
             "0=Ridge, 1=Lasso, 0.5=equal mix. Search: [0.1,0.5,0.9,1.0]",
             PURPLE_H),
        ]

        left_title = Text("Lasso", font_size=20, color=RED_H, weight=BOLD
                          ).shift(UP * 1.7 + LEFT * 3.5)
        right_title = Text("ElasticNet", font_size=20, color=PURPLE_H, weight=BOLD
                           ).shift(UP * 1.7 + RIGHT * 3.0)

        def build_list(params, x_shift):
            grp = VGroup()
            for param, default, desc, color in params:
                p = Text(param, font_size=14, color=color, weight=BOLD)
                d = Text(default, font_size=11, color=GRAY_H)
                de = Text(desc, font_size=12, color=WHITE_H)
                if de.width > 4.8:
                    de.scale(4.8 / de.width)
                row = VGroup(p, d, de)
                row.arrange(DOWN, aligned_edge=LEFT, buff=0.04)
                grp.add(row)
            grp.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            grp.move_to(LEFT * x_shift + DOWN * 0.2)
            return grp

        left_list = build_list(lasso_params, 3.5)
        right_list = build_list(enet_params, -3.0)

        sep = Line(UP * 2.0, DOWN * 2.5, stroke_color=GRAY_H, stroke_width=0.8)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(left_title), FadeIn(right_title), FadeIn(sep), run_time=0.5)
        self.play(FadeIn(left_list), FadeIn(right_list), run_time=0.8)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title),
            FadeOut(left_title), FadeOut(right_title), FadeOut(sep),
            FadeOut(left_list), FadeOut(right_list),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 57 — OVERALL PROS/CONS DETAILED
    # ─────────────────────────────────────────
    def scene_57_overall_pros_cons(self):
        sub = make_subtitle("Overall Pros and Cons of Polynomial Regression")
        sec_title = make_section_title("Polynomial Regression: Full Pros & Cons",
                                       font_size=30)

        pros = [
            "Captures non-linearity (curved relationships)",
            "No new algorithm needed — reuses OLS",
            "Interpretable equation form",
            "Exact closed-form solution (Normal Eq)",
            "Flexible degree hyperparameter",
            "Works with small datasets at low degrees",
            "Provides CI and PI when assumptions hold",
            "Combines well with Ridge/Lasso/ElasticNet",
            "Feature engineering insight generalises",
        ]
        cons = [
            "Overfits easily at high degrees",
            "Catastrophic extrapolation beyond training",
            "Feature explosion with many inputs",
            "Multicollinearity between x, x^2, x^3, ...",
            "Degree selection requires cross-validation",
            "Sensitive to outliers (amplified at high deg)",
            "Normal Eq is O(p^3) — expensive",
            "Runge's phenomenon at high degrees",
            "Not competitive vs RF/XGBoost/Neural Net",
        ]
        pc = make_pros_cons(pros, cons, width=5.5, height=4.0)
        pc.shift(DOWN * 0.3)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(pc[0]), run_time=0.7)
        self.play(FadeIn(pc[1]), run_time=0.7)
        self.wait(5)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(pc), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 58 — WHEN TO USE
    # ─────────────────────────────────────────
    def scene_58_when_to_use(self):
        sub = make_subtitle("When to Use Polynomial Regression")
        sec_title = make_section_title("When to Use", font_size=38)

        pros = [
            "Scatter plot shows clear curvature",
            "Domain theory implies polynomial form",
            "Linear residuals show systematic curves",
            "Interpretability required",
            "Small number of features (<=5)",
            "Degree <=3-4 sufficient",
            "Data stays within training range",
        ]
        cons = [
            "Need extrapolation beyond training",
            "Many input features (>=10)",
            "Truly non-polynomial relationship",
            "Very large dataset",
            "Curvature is localised — use splines",
            "Max predictive accuracy required",
        ]
        pc = make_pros_cons(pros, cons, width=5.5, height=3.8)
        pc.shift(DOWN * 0.3)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(pc[0]), run_time=0.6)
        self.play(FadeIn(pc[1]), run_time=0.6)
        self.wait(4.5)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(pc), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 59 — ALTERNATIVES COMPARISON TABLE
    # ─────────────────────────────────────────
    def scene_59_alternatives(self):
        sub = make_subtitle("Polynomial Regression vs. Alternatives")
        sec_title = make_section_title("Alternatives Comparison", font_size=34)

        headers = ["Alternative", "When to Prefer Over Polynomial Regression"]
        rows = [
            ["Spline Regression", "Local curvature; avoids global oscillation"],
            ["Decision Tree", "Complex non-linear patterns; mixed features"],
            ["Random Forest/XGBoost", "High accuracy, large data, many features"],
            ["SVR (poly kernel)", "High-dim poly without feature explosion"],
            ["Neural Network", "Very complex patterns, large data"],
            ["Log/Box-Cox + Linear", "Multiplicative or exponential relationships"],
            ["LOESS/Splines", "Non-parametric smoothing; no degree to pick"],
        ]
        tbl = make_table_mob(headers, rows,
                             col_widths=[3.2, 6.5],
                             font_size=14)
        tbl.scale(0.88)
        tbl.shift(DOWN * 0.3)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(tbl), run_time=0.9)
        self.wait(5)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(tbl), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 60 — COMMON MISTAKES
    # ─────────────────────────────────────────
    def scene_60_mistakes(self):
        sub = make_subtitle("10 Common Mistakes — And How to Fix Them")
        sec_title = make_section_title("Common Mistakes", font_size=36)

        headers = ["#", "Mistake", "Correct Approach"]
        rows = [
            ["1", "Using train R^2 to select degree", "Use cross-validation R^2"],
            ["2", "Scaling x before poly expansion", "Raw x -> Poly -> Scaler -> Model"],
            ["3", "Fitting scaler on test data", "Fit scaler on train only"],
            ["4", "Extrapolating beyond train range", "Clip to training range"],
            ["5", "High degree without regularisation", "Always pair with Ridge/Lasso"],
            ["6", "Interpreting coefficients at high degree", "Interpret curve shape only"],
            ["7", "Not checking residual plots", "Always plot Residuals vs Fitted"],
            ["8", "include_bias=True + fit_intercept=True", "Set include_bias=False"],
            ["9", "Low max_iter for Lasso", "Set max_iter=10000+"],
            ["10", "Not using Pipeline", "Always use sklearn Pipeline"],
        ]
        tbl = make_table_mob(headers, rows,
                             col_widths=[0.6, 3.6, 4.6],
                             font_size=12)
        tbl.scale(0.85)
        tbl.shift(DOWN * 0.2)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(tbl), run_time=0.9)
        self.wait(5)
        self.play(FadeOut(sub), FadeOut(sec_title), FadeOut(tbl), run_time=0.6)

    # ─────────────────────────────────────────
    # SCENE 61 — INTERVIEW Q: IS IT LINEAR?
    # ─────────────────────────────────────────
    def scene_61_iq_linear(self):
        sub = make_subtitle("Interview Q: Is Polynomial Regression Linear or Non-Linear?")
        sec_title = make_section_title("Interview Q: Linear or Non-Linear?",
                                       font_size=31)

        q = Text(
            "Q: Is polynomial regression a linear or non-linear model?",
            font_size=18, color=YELLOW_H, weight=BOLD
        ).shift(UP * 1.8)
        if q.width > 11:
            q.scale(11 / q.width)

        a_title = Text("A: It IS a linear model — linear in its parameters b.",
                       font_size=18, color=GREEN_H).shift(UP * 1.1)
        if a_title.width > 11:
            a_title.scale(11 / a_title.width)

        points = [
            "'Linear' in ML means linear combination of parameters, not linear in x.",
            "y = b0 + b1*x + b2*x^2 is a LINEAR combination of b0, b1, b2.",
            "x^2 is engineered as a feature — the algorithm sees only a linear problem.",
            "We solve it with OLS Normal Equations — same as linear regression.",
        ]
        body = VGroup()
        for pt in points:
            t = Text("• " + pt, font_size=16, color=WHITE_H)
            if t.width > 11:
                t.scale(11 / t.width)
            body.add(t)
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        body.shift(DOWN * 0.35)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(q), run_time=0.5)
        self.play(FadeIn(a_title), run_time=0.5)
        for item in body:
            self.play(FadeIn(item), run_time=0.35)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(q),
            FadeOut(a_title), FadeOut(body),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 62 — INTERVIEW Q: WHY OVERFIT
    # ─────────────────────────────────────────
    def scene_62_iq_overfit(self):
        sub = make_subtitle("Interview Q: Why Does Polynomial Regression Overfit So Easily?")
        sec_title = make_section_title("Interview Q: Why Overfitting?",
                                       font_size=33)

        q = Text(
            "Q: Why does polynomial regression overfit so much more easily?",
            font_size=18, color=YELLOW_H, weight=BOLD
        ).shift(UP * 1.8)
        if q.width > 11:
            q.scale(11 / q.width)

        reasons = [
            ("1. More parameters:", "Degree-n poly has n+1 coefficients. More free params = "
             "more ability to memorise noise.", BLUE_H),
            ("2. No built-in penalty:", "Plain OLS minimises training error with zero concern "
             "for coefficient magnitude.", ORANGE_H),
            ("3. Runge's phenomenon:", "At degree n-1 for n data points, the polynomial "
             "passes through EVERY point. R^2 = 1.0!", RED_H),
        ]
        grp = VGroup()
        for label, desc, color in reasons:
            l = Text(label, font_size=16, color=color, weight=BOLD)
            d = Text(desc, font_size=15, color=WHITE_H)
            if d.width > 9.0:
                d.scale(9.0 / d.width)
            row = VGroup(l, d).arrange(RIGHT, buff=0.2)
            if row.width > 11:
                row.scale(11 / row.width)
            grp.add(row)
        grp.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        grp.shift(DOWN * 0.3)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(q), run_time=0.5)
        for r in grp:
            self.play(FadeIn(r), run_time=0.45)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(q), FadeOut(grp),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 63 — INTERVIEW Q: TRAIN 0.99 TEST 0.3
    # ─────────────────────────────────────────
    def scene_63_iq_train_test(self):
        sub = make_subtitle("Interview Q: Train R^2=0.99, Test R^2=0.3. What Happened?")
        sec_title = make_section_title("Interview Q: Train 0.99, Test 0.3",
                                       font_size=32)

        q = Text(
            "Q: Train R^2=0.99, Test R^2=0.3. What happened? How to fix it?",
            font_size=18, color=YELLOW_H, weight=BOLD
        ).shift(UP * 1.8)
        if q.width > 11:
            q.scale(11 / q.width)

        diag = Text(
            "Classic OVERFITTING. Model memorised training noise including every random fluctuation.",
            font_size=17, color=RED_H
        ).shift(UP * 1.0)
        if diag.width > 11:
            diag.scale(11 / diag.width)

        bv = Text(
            "Bias-variance: very LOW bias, extremely HIGH variance.",
            font_size=17, color=ORANGE_H
        ).shift(UP * 0.4)

        fixes = [
            "1. Reduce polynomial degree via cross-validation.",
            "2. Add Ridge or Lasso regularisation.",
            "3. Collect more training data.",
            "4. Use Lasso to zero out unnecessary poly terms.",
        ]
        fix_grp = VGroup()
        for f in fixes:
            t = Text(f, font_size=16, color=GREEN_H)
            if t.width > 11:
                t.scale(11 / t.width)
            fix_grp.add(t)
        fix_grp.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        fix_grp.shift(DOWN * 1.0)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(q), run_time=0.5)
        self.play(FadeIn(diag), run_time=0.5)
        self.play(FadeIn(bv), run_time=0.4)
        for f in fix_grp:
            self.play(FadeIn(f), run_time=0.35)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(q),
            FadeOut(diag), FadeOut(bv), FadeOut(fix_grp),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 64 — INTERVIEW Q: WHY SCALE AFTER POLY
    # ─────────────────────────────────────────
    def scene_64_iq_scale(self):
        sub = make_subtitle("Interview Q: Why Scale AFTER Polynomial Expansion?")
        sec_title = make_section_title("Interview Q: Scaling Order", font_size=34)

        q = Text(
            "Q: Why must you scale AFTER polynomial expansion, not before?",
            font_size=18, color=YELLOW_H, weight=BOLD
        ).shift(UP * 1.8)
        if q.width > 11:
            q.scale(11 / q.width)

        points = [
            "StandardScaler needs to see the actual distribution of x^2, x^3 to",
            "compute their correct mean and std.",
            "If you scale x first, poly features are derived from already-scaled x.",
            "Their statistics are different -> inconsistently normalised features.",
            "With regularisation, the penalty must treat all features fairly.",
            "This is only possible if they are on consistent scales.",
        ]
        body = VGroup()
        for pt in points:
            t = Text(pt, font_size=16, color=WHITE_H)
            if t.width > 11:
                t.scale(11 / t.width)
            body.add(t)
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        body.shift(DOWN * 0.3)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(q), run_time=0.5)
        for pt in body:
            self.play(FadeIn(pt), run_time=0.3)
        self.wait(3.5)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(q), FadeOut(body),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 65 — INTERVIEW Q: WHY LASSO PRODUCES ZEROS
    # ─────────────────────────────────────────
    def scene_65_iq_lasso_zeros(self):
        sub = make_subtitle("Interview Q: Why Does Lasso Produce Sparse Solutions?")
        sec_title = make_section_title("Interview Q: Lasso Zeros", font_size=34)

        q = Text(
            "Q: Why does Lasso produce sparse solutions while Ridge doesn't?",
            font_size=18, color=YELLOW_H, weight=BOLD
        ).shift(UP * 1.7)
        if q.width > 11:
            q.scale(11 / q.width)

        # Geometric visualisation: L1 diamond vs L2 sphere
        ax_l = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=2.8,
            y_length=2.8,
            axis_config={"color": GRAY_H, "stroke_width": 1.0},
            tips=False,
        ).shift(LEFT * 3.5 + DOWN * 0.4)

        ax_r = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=2.8,
            y_length=2.8,
            axis_config={"color": GRAY_H, "stroke_width": 1.0},
            tips=False,
        ).shift(RIGHT * 3.5 + DOWN * 0.4)

        # L2 ball (circle in axes coords)
        l2_ball = Circle(radius=0.9, color=BLUE_H, stroke_width=2.0)
        l2_ball.set_fill(color=BLUE_H, opacity=0.1)
        l2_ball.move_to(ax_l.c2p(0, 0))

        # L1 diamond
        l1_pts = [ax_r.c2p(1, 0), ax_r.c2p(0, 1),
                  ax_r.c2p(-1, 0), ax_r.c2p(0, -1)]
        l1_diamond = Polygon(*l1_pts, color=PURPLE_H, stroke_width=2.0)
        l1_diamond.set_fill(color=PURPLE_H, opacity=0.1)

        # Solution point for L2 — not on axis
        sol_l2 = Dot(ax_l.c2p(-0.63, 0.67), radius=0.09, color=RED_H)
        # Solution point for L1 — on axis (corner) -> zero
        sol_l1 = Dot(ax_r.c2p(1, 0), radius=0.09, color=RED_H)

        lbl_l2 = Text("Ridge: L2 (sphere)\nNo corners -> never zero",
                      font_size=13, color=BLUE_H).next_to(ax_l, DOWN, buff=0.15)
        lbl_l1 = Text("Lasso: L1 (diamond)\nCorners -> b2 = 0 exactly!",
                      font_size=13, color=PURPLE_H).next_to(ax_r, DOWN, buff=0.15)

        b1_lbl_r = MathTex(r"\beta_1", font_size=14,
                           color=GRAY_H).next_to(ax_r.x_axis, RIGHT, buff=0.05)
        b2_lbl_r = MathTex(r"\beta_2", font_size=14,
                           color=GRAY_H).next_to(ax_r.y_axis, UP, buff=0.05)
        b1_lbl_l = MathTex(r"\beta_1", font_size=14,
                           color=GRAY_H).next_to(ax_l.x_axis, RIGHT, buff=0.05)
        b2_lbl_l = MathTex(r"\beta_2", font_size=14,
                           color=GRAY_H).next_to(ax_l.y_axis, UP, buff=0.05)

        self.play(FadeIn(sub), FadeIn(sec_title), run_time=0.5)
        self.play(FadeIn(q), run_time=0.5)
        self.play(
            Create(ax_l), Create(ax_r),
            FadeIn(b1_lbl_l), FadeIn(b2_lbl_l),
            FadeIn(b1_lbl_r), FadeIn(b2_lbl_r),
            run_time=0.6
        )
        self.play(
            FadeIn(l2_ball), FadeIn(l1_diamond),
            run_time=0.7
        )
        self.play(
            FadeIn(sol_l2), FadeIn(sol_l1),
            FadeIn(lbl_l2), FadeIn(lbl_l1),
            run_time=0.6
        )
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(sec_title), FadeOut(q),
            FadeOut(ax_l), FadeOut(ax_r),
            FadeOut(b1_lbl_l), FadeOut(b2_lbl_l),
            FadeOut(b1_lbl_r), FadeOut(b2_lbl_r),
            FadeOut(l2_ball), FadeOut(l1_diamond),
            FadeOut(sol_l2), FadeOut(sol_l1),
            FadeOut(lbl_l2), FadeOut(lbl_l1),
            run_time=0.6
        )

    # ─────────────────────────────────────────
    # SCENE 66 — OUTRO / SUMMARY
    # ─────────────────────────────────────────
    def scene_66_outro(self):
        sub = make_subtitle("Polynomial Regression — Summary")

        title = Text("Key Takeaways", font_size=42, color=BLUE_H, weight=BOLD)
        title.to_edge(UP, buff=0.4)

        takeaways = [
            ("Linear in parameters b — not in x.", BLUE_H),
            ("Degree is a direct dial on bias-variance tradeoff.", GREEN_H),
            ("Always scale AFTER polynomial expansion.", YELLOW_H),
            ("Use Ridge / Lasso / ElasticNet for regularisation.", ORANGE_H),
            ("Select degree via cross-validation — never by training R^2.", RED_H),
            ("NEVER extrapolate beyond the training range.", PURPLE_H),
            ("Wrap all steps in a scikit-learn Pipeline.", GRAY_H),
        ]

        grp = VGroup()
        for text, color in takeaways:
            t = Text("✓  " + text, font_size=18, color=color)
            if t.width > 11:
                t.scale(11 / t.width)
            grp.add(t)
        grp.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        grp.shift(DOWN * 0.25)

        deco = Circle(radius=2.5, color=BLUE_H, stroke_width=0.8)
        deco.set_opacity(0.08)
        deco.shift(RIGHT * 5.5)
        deco2 = Circle(radius=1.5, color=GREEN_H, stroke_width=0.6)
        deco2.set_opacity(0.07)
        deco2.shift(LEFT * 5.5 + DOWN * 1.5)

        self.play(FadeIn(sub), FadeIn(deco), FadeIn(deco2), run_time=0.4)
        self.play(Write(title), run_time=0.8)
        for item in grp:
            self.play(FadeIn(item), run_time=0.3)
        self.wait(4)
        self.play(
            FadeOut(sub), FadeOut(title), FadeOut(grp),
            FadeOut(deco), FadeOut(deco2),
            run_time=0.8
        )
