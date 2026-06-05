# -*- coding: utf-8 -*-
"""
Linear Regression - Complete YouTube Video
Single-class Manim script. Run with:
    manim -pqh linear_regression_video.py LinearRegressionVideo
Output: media/videos/linear_regression_video/1080p60/LinearRegressionVideo.mp4
"""

from manim import *
import numpy as np

# Fallback for LIGHT_GRAY in case Manim version does not export it
try:
    _ = LIGHT_GRAY
except NameError:
    LIGHT_GRAY = "#BBBBBB"

# Fallback for NORMAL (used in make_table wt variable)
try:
    _ = NORMAL
except NameError:
    NORMAL = "NORMAL"  # Pango weight name fallback

# - Colour Palette ----------------------------------------------------------
BLUE_H   = "#4f9eff"
ORANGE_H = "#f97316"
GREEN_H  = "#10b981"
YELLOW_H = "#fbbf24"
RED_H    = "#f87171"
PURPLE_H = "#a855f7"
BG       = "#0d0f14"
CARD_BG  = "#1a1d2e"
CARD2_BG = "#12152b"

# -- Unicode characters via chr() -- pure ASCII source, correct glyphs at runtime
EM     = chr(0x2014)  # em dash
SUP2   = chr(0x00B2)  # superscript 2
MDOT   = chr(0x00B7)  # middle dot
ARROW  = chr(0x2192)  # right arrow
BULL   = chr(0x2022)  # bullet
MINUS  = chr(0x2212)  # minus sign
APPROX = chr(0x2248)  # approximately



# - Helper: Subtitle bar ----------------------------------------------------
def make_subtitle(text_str, font_size=26, width=11.0):
    """Return a subtitle VGroup: black rect + white text."""
    txt = Text(text_str, font_size=font_size, color=WHITE)
    txt.set_width(min(txt.width, width))
    pad_w = txt.width + 0.4
    pad_h = txt.height + 0.22
    rect = RoundedRectangle(
        width=pad_w, height=pad_h,
        corner_radius=0.12,
        fill_color=BLACK, fill_opacity=0.88,
        stroke_opacity=0
    )
    rect.move_to(txt)
    grp = VGroup(rect, txt)
    grp.to_edge(DOWN, buff=0.18)
    return grp


# - Helper: Section title banner --------------------------------------------
def section_banner(title_str, sub_str="", color=BLUE_H):
    t = Text(title_str, font_size=44, color=color)
    t.to_edge(UP, buff=0.35)
    items = [t]
    if sub_str:
        s = Text(sub_str, font_size=24, color=LIGHT_GRAY)
        s.next_to(t, DOWN, buff=0.18)
        items.append(s)
    return VGroup(*items)


# - Helper: Two-column card (Pros / Cons) -----------------------------------
def make_pros_cons(pros_list, cons_list, title="", font_size=22):
    """Build a full-screen split pros/cons layout."""
    card_w = 5.8
    card_h = 0.52

    def make_col(items, label, col_color, sign):
        header = Text(f"{sign} {label}", font_size=26,
                      color=col_color)
        rows = VGroup()
        for item in items:
            # wrap at 38 chars so text fits inside card width
            words = item.split()
            lines = []
            cur = ""
            for w in words:
                test = (cur + " " + w).strip()
                if len(test) > 38:
                    lines.append(cur)
                    cur = w
                else:
                    cur = test
            if cur:
                lines.append(cur)
            line_text = "\n".join(lines)
            n_lines = line_text.count("\n") + 1
            row_txt = Text(line_text, font_size=font_size - 1,
                           color=WHITE, line_spacing=0.85)
            # Height: at least 0.58 per line
            needed_h = max(0.62, 0.56 * n_lines + 0.22)
            bg = RoundedRectangle(
                width=card_w,
                height=needed_h,
                corner_radius=0.1,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=col_color, stroke_opacity=0.4,
                stroke_width=1
            )
            # Scale text if it still overflows
            max_txt_w = card_w - 0.25
            if row_txt.width > max_txt_w:
                row_txt.set_width(max_txt_w)
            row_txt.move_to(bg)
            row_txt.align_to(bg, LEFT)
            row_txt.shift(RIGHT * 0.18)
            rows.add(VGroup(bg, row_txt))
        rows.arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        col = VGroup(header, rows)
        col.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        return col

    pros_col = make_col(pros_list, "Pros", GREEN_H, "+")
    cons_col = make_col(cons_list, "Cons", RED_H,   "-")
    pros_col.set_width(min(pros_col.width, 5.6))
    cons_col.set_width(min(cons_col.width, 5.6))

    both = VGroup(pros_col, cons_col)
    both.arrange(RIGHT, buff=0.5, aligned_edge=UP)

    if title:
        banner = Text(title, font_size=34, color=YELLOW_H)
        banner.to_edge(UP, buff=0.32)
        # Position body below the banner with clearance
        both.next_to(banner, DOWN, buff=0.30)
        both.set_x(0)  # centre horizontally
        # If body overflows bottom of frame, scale it down
        if both.get_bottom()[1] < -3.5:
            max_h = 3.5 + banner.get_bottom()[1] - 0.25
            both.set_height(max_h)
            both.next_to(banner, DOWN, buff=0.25)
            both.set_x(0)
        return VGroup(banner, both)

    both.center()
    both.shift(DOWN * 0.2)
    return both


# - Helper: Simple data table -----------------------------------------------
def make_table(headers, rows_data, col_colors=None, font_size=20):
    """Build a styled VGroup table. Cells are positioned relative to
    row_bg after it is placed, so columns are always properly aligned."""
    all_rows = [headers] + rows_data
    n_col = len(headers)
    col_w = [0.0] * n_col

    # First pass: measure every cell to get column widths
    cell_texts = []
    for r_i, row in enumerate(all_rows):
        r_cells = []
        for c_i, cell in enumerate(row):
            fs = font_size + 2 if r_i == 0 else font_size
            wt = None  # weight param removed for Pango compatibility
            col = col_colors[c_i] if col_colors else (
                YELLOW_H if r_i == 0 else WHITE)
            t = Text(str(cell), font_size=fs, color=col)
            col_w[c_i] = max(col_w[c_i], t.width)
            r_cells.append(t)
        cell_texts.append(r_cells)

    # Add padding to each column
    col_w = [w + 0.40 for w in col_w]
    total_w = sum(col_w)
    row_h = 0.60

    table_grp = VGroup()
    for r_i, r_cells in enumerate(cell_texts):
        row_bg_color = CARD2_BG if r_i % 2 == 0 else CARD_BG
        row_bg = Rectangle(
            width=total_w,
            height=row_h,
            fill_color=row_bg_color, fill_opacity=1,
            stroke_opacity=0
        )
        # Position cells: x measured from the LEFT edge of row_bg
        # We place row_bg at ORIGIN temporarily to get its left edge,
        # then move each cell. After arrange() shifts row_bg, cells move with it.
        row_bg.move_to(ORIGIN)
        left_edge_x = -total_w / 2      # x of row_bg left edge at ORIGIN
        for c_i, cell_txt in enumerate(r_cells):
            # Centre of this column relative to row_bg centre
            col_center_x = left_edge_x + sum(col_w[:c_i]) + col_w[c_i] / 2
            cell_txt.move_to(row_bg.get_center() + RIGHT * col_center_x)
            # Scale down text that overflows its column
            max_txt_w = col_w[c_i] - 0.1
            if cell_txt.width > max_txt_w:
                cell_txt.set_width(max_txt_w)
        table_grp.add(VGroup(row_bg, *r_cells))

    table_grp.arrange(DOWN, buff=0)
    table_grp.center()
    return table_grp


# ===========================================================================
#  MAIN VIDEO SCENE
# ===========================================================================
class LinearRegressionVideo(Scene):

    def setup(self):
        self.camera.background_color = BG
        self._sub = None  # current subtitle mobject

    # - subtitle helpers ------------------------------------------------
    def show_sub(self, text_str, wait=3.5):
        sub = make_subtitle(text_str)
        if self._sub:
            self.play(
                FadeOut(self._sub, run_time=0.3),
                FadeIn(sub, run_time=0.4)
            )
        else:
            self.play(FadeIn(sub, run_time=0.4))
        self._sub = sub
        self.wait(wait)

    def hide_sub(self):
        if self._sub:
            self.play(FadeOut(self._sub, run_time=0.3))
            self._sub = None

    def clear_scene(self, keep=None):
        self.hide_sub()
        mobs = [m for m in self.mobjects
                if keep is None or m not in keep]
        if mobs:
            self.play(*[FadeOut(m, run_time=0.4) for m in mobs])

    # -------------------------------------------------------------------
    # S01 - Title Card
    # -------------------------------------------------------------------
    def s01_title(self):
        badge = RoundedRectangle(
            width=3.8, height=0.55, corner_radius=0.12,
            fill_color=BLUE_H, fill_opacity=0.25,
            stroke_color=BLUE_H, stroke_width=1.5
        )
        badge_txt = Text("Chapter 1 " + MDOT + " Supervised Learning",
                         font_size=20, color=BLUE_H)
        badge_txt.move_to(badge)
        badge_grp = VGroup(badge, badge_txt)
        badge_grp.to_edge(UP, buff=0.5)

        title = Text("Linear Regression",
                     font_size=68, color=WHITE)
        sub = Text(
            "Every concept " + MDOT + " All pros & cons " + MDOT + " Full sklearn code " + MDOT + " Interview Q&A",
            font_size=22, color=LIGHT_GRAY
        )

        icons = Text("[Math]  [sklearn]  [Diagnostics]  [Interview]",
                     font_size=20, color=YELLOW_H)

        content = VGroup(title, sub, icons)
        content.arrange(DOWN, buff=0.35)
        content.center()

        self.play(FadeIn(badge_grp, shift=DOWN * 0.2, run_time=0.7))
        self.play(Write(title, run_time=1.4))
        self.play(FadeIn(sub, shift=UP * 0.15, run_time=0.7))
        self.play(FadeIn(icons, shift=UP * 0.1, run_time=0.6))
        self.show_sub("Welcome! This is the complete guide to Linear Regression.", wait=3.0)
        self.clear_scene()

    # -------------------------------------------------------------------
    # S02 - Real-World Analogy
    # -------------------------------------------------------------------
    def s02_analogy(self):
        banner = section_banner("What Is Linear Regression?",
                                "A real-world analogy first")
        self.play(FadeIn(banner, run_time=0.6))
        self.show_sub("Imagine you are a real estate agent.", wait=2.0)

        lines = [
            "You notice: bigger houses cost more.",
            "You collect data on 100 houses.",
            "You plot them and draw the best-fit line.",
            "A client asks: 'How much is a 2,000 sq ft house?'",
            "You trace to the line " + EM + " that's Linear Regression.",
        ]
        cards = VGroup()
        for i, line in enumerate(lines):
            bg = RoundedRectangle(
                width=9.2, height=0.72, corner_radius=0.12,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=BLUE_H, stroke_opacity=0.5,
                stroke_width=1.2
            )
            num = Text(f"{i+1}.", font_size=22,
                       color=YELLOW_H)
            txt = Text(line, font_size=22, color=WHITE)
            num.move_to(bg.get_left() + RIGHT * 0.4)
            txt.move_to(bg).shift(RIGHT * 0.25)
            txt.align_to(num, LEFT)
            txt.shift(RIGHT * 0.3)
            cards.add(VGroup(bg, num, txt))

        cards.arrange(DOWN, buff=0.14)
        cards.next_to(banner, DOWN, buff=0.35)

        for card in cards:
            self.play(FadeIn(card, shift=RIGHT * 0.2, run_time=0.45))
            self.wait(0.3)

        self.show_sub(
            "The line that best fits all points is what linear regression finds.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S03 - House Price Scatter + Best Fit Line
    # -------------------------------------------------------------------
    def s03_scatter(self):
        banner = section_banner("House Price Scatter Plot",
                                "Visualising the regression line")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Let us visualise the regression line on house data.", wait=2.5)

        axes = Axes(
            x_range=[800, 3200, 400],
            y_range=[80, 520, 80],
            x_length=7.5,
            y_length=4.2,
            axis_config={"color": LIGHT_GRAY, "stroke_width": 1.5},
            tips=False
        )
        axes.shift(DOWN * 0.5)

        x_label = Text("House Size (sq ft)", font_size=18, color=LIGHT_GRAY)
        y_label = Text("Sale Price ($k)", font_size=18, color=LIGHT_GRAY)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)
        y_label.next_to(axes.y_axis, LEFT, buff=0.2).rotate(PI / 2)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))

        # Scatter data: true line is y = 30 + 0.13*x, with noise
        np.random.seed(42)
        base_xs = list(range(900, 3100, 100))
        data = [
            (x, max(80, 30 + 0.13 * x + np.random.normal(0, 18)))
            for x in base_xs
        ]

        dots = VGroup()
        for x_val, y_val in data:
            dot = Dot(
                axes.coords_to_point(x_val, y_val),
                radius=0.07, color=BLUE_H, fill_opacity=0.85
            )
            dots.add(dot)

        self.play(LaggedStart(
            *[FadeIn(d, scale=1.4) for d in dots],
            lag_ratio=0.06, run_time=1.8
        ))
        self.show_sub("Each dot is one house observation.", wait=2.0)

        # Best-fit line: y = 30 + 0.13*x  (matches the data generation)
        def line_fn(x):
            return 30 + 0.13 * x

        fit_line = axes.plot(
            line_fn,
            x_range=[850, 3150],
            color=GREEN_H,
            stroke_width=2.5
        )
        # Label: "Best-fit Line" as Text + hat{y} as MathTex
        line_label = VGroup(
            Text("Best-fit Line (", font_size=18, color=GREEN_H),
            MathTex(r"\hat{y}", font_size=22, color=GREEN_H),
            Text(")", font_size=18, color=GREEN_H),
        )
        line_label.arrange(RIGHT, buff=0.05)
        line_label.next_to(fit_line.get_end(), RIGHT, buff=0.1)

        self.play(Create(fit_line, run_time=1.4))
        self.play(FadeIn(line_label, run_time=0.5))
        self.show_sub(
            "The regression line minimises the sum of squared distances to all points.",
            wait=3.5
        )

        # Show residuals for a few actual data points.
        # Pick 4 spread-out points from the real data list and draw
        # a dashed line from the actual dot (y_val) to the predicted line (y_pred).
        residual_grp = VGroup()
        residual_indices = [0, 2, 3, 6, 7, 8, 10, 13, 14, 16, 19, 20]   # indices into the data list
        for idx in residual_indices:
            x_val, y_val = data[idx]
            y_pred = line_fn(x_val)
            # Only draw if there is a visible gap between point and line
            if abs(y_val - y_pred) < 5:
                continue
            p_data = axes.coords_to_point(x_val, y_val)   # actual dot position
            p_pred = axes.coords_to_point(x_val, y_pred)  # point on the line
            arr = DashedLine(
                p_data, p_pred,
                color=RED_H, stroke_width=1.8, dash_length=0.08
            )
            residual_grp.add(arr)

        self.play(Create(residual_grp, run_time=1.0))
        res_label = Text("residuals", font_size=16, color=RED_H)
        res_label.next_to(residual_grp, RIGHT, buff=0.15)
        self.play(FadeIn(res_label))
        self.show_sub(
            "Residuals are the vertical gaps between actual and predicted values.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S04 - What / How / Why / When Grid
    # -------------------------------------------------------------------
    def s04_what_how_why_when(self):
        banner = section_banner("What / How / Why / When",
                                "Four dimensions of linear regression")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Let us look at the four key dimensions.", wait=2.0)

        items = [
            ("What", BLUE_H,
             "Models input features vs.\na continuous target\nas a linear function."),
            ("How", GREEN_H,
             "Minimises sum of squared\ndifferences between actual\nand predicted values (OLS)."),
            ("Why", YELLOW_H,
             "Interpretable, extremely fast,\nclosed-form solution,\ncanonical baseline model."),
            ("When", PURPLE_H,
             "Target is continuous.\nRelationship is ~linear.\nInterpretability needed.\nAs a baseline first."),
        ]

        cards = VGroup()
        for label, color, body in items:
            bg = RoundedRectangle(
                width=5.5, height=2.1, corner_radius=0.18,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=color, stroke_width=2.0, stroke_opacity=0.7
            )
            lbl = Text(label, font_size=28, color=color)
            bdy = Text(body, font_size=19, color=WHITE,
                       line_spacing=1.1)
            lbl.move_to(bg.get_top() + DOWN * 0.35)
            bdy.move_to(bg).shift(DOWN * 0.25)
            cards.add(VGroup(bg, lbl, bdy))

        cards.arrange_in_grid(rows=2, cols=2, buff=0.25)
        cards.next_to(banner, DOWN, buff=0.35)
        cards.set_width(12.0)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.15, run_time=0.5))
            self.wait(0.4)

        self.show_sub(
            "When: target is continuous, relationship is roughly linear, and you need interpretability.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S05 - Simple vs Multiple Table
    # -------------------------------------------------------------------
    def s05_simple_vs_multiple(self):
        banner = section_banner("Simple vs Multiple Linear Regression")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("There are two types: simple and multiple.", wait=2.5)

        headers = ["Type", "Features", "Example", "Geometry"]
        rows = [
            ["Simple", "1 feature", "Price ~ Size", "A line in 2D"],
            ["Multiple", "2+ features",
             "Price ~ Size + Beds + Location", "Hyperplane in N-D"],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, BLUE_H, GREEN_H, ORANGE_H])
        tbl.center().shift(DOWN * 0.3)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.15, run_time=0.5))
            self.wait(0.5)

        self.show_sub(
            "Simple: one feature, one line. Multiple: many features, a hyperplane.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S06 - Overall Pros & Cons
    # -------------------------------------------------------------------
    def s06_overall_pros_cons(self):
        pros = [
            "Highly interpretable coefficients",
            "Blazing fast " + EM + " closed-form O(np" + SUP2 + ")",
            "No hyperparameters (base OLS)",
            "BLUE estimator under Gauss-Markov",
            "Statistical inference via p-values",
            "Great baseline model",
            "Memory efficient",
        ]
        cons = [
            "Assumes linearity " + EM + " wrong for curves",
            "Sensitive to outliers (squared loss)",
            "Multicollinearity " + ARROW + " unstable coefficients",
            "No automatic interaction terms",
            "Struggles when p > n",
            "Scale sensitive " + EM + " requires scaling",
            "Strict assumptions for valid inference",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Overall Pros & Cons " + EM + " Linear Regression",
                                font_size=19)

        banner = layout[0]
        body = layout[1]
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Let us look at the overall strengths and weaknesses.", wait=2.5)
        self.play(FadeIn(body[0], shift=RIGHT * 0.3, run_time=0.7))
        self.play(FadeIn(body[1], shift=LEFT * 0.3, run_time=0.7))
        self.show_sub(
            "Pros: fast, interpretable, BLUE. Cons: linearity assumption, outlier sensitivity.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S07 - The Mathematical Model
    # -------------------------------------------------------------------
    def s07_math_model(self):
        banner = section_banner("The Mathematical Model",
                                "Building the equation term by term")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Any straight line is y = mx + b. In ML notation:", wait=2.5)

        eq1 = MathTex(
            r"\hat{y}", "=",
            r"\beta_0",
            "+",
            r"\beta_1 x_1",
            "+",
            r"\beta_2 x_2",
            "+",
            r"\cdots",
            "+",
            r"\beta_n x_n",
            font_size=42, color=WHITE
        )
        eq1.set_color_by_tex(r"\hat{y}", YELLOW_H)
        eq1.set_color_by_tex(r"\beta_0", GREEN_H)
        eq1.set_color_by_tex(r"\beta_1", BLUE_H)
        eq1.set_color_by_tex(r"\beta_2", BLUE_H)
        eq1.set_color_by_tex(r"\beta_n", BLUE_H)
        eq1.next_to(banner, DOWN, buff=0.5)

        self.play(Write(eq1, run_time=2.0))
        self.show_sub(
            "y-hat is the predicted value. Beta-zero is the intercept. Beta-i are the coefficients.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S08 - Symbol Table
    # -------------------------------------------------------------------
    def s08_symbol_table(self):
        banner = section_banner("Symbol Reference Table")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Here is what each symbol means in the equation.", wait=2.5)

        # Build rows as VGroups with MathTex for symbol column
        sym_data = [
            (r"\hat{y}",                     YELLOW_H, "Predicted value",
             "Model output " + EM + " best guess for y"),
            (r"\beta_0",                     GREEN_H,  "Intercept / bias",
             "Value when all features = 0"),
            (r"\beta_1 \ldots \beta_n",      BLUE_H,   "Coefficients",
             "Change in y-hat per unit of feature"),
            (r"x_1 \ldots x_n",              BLUE_H,   "Features / predictors",
             "Inputs to the model"),
            (r"\varepsilon",                 RED_H,    "Error term",
             "Noise the model cannot explain"),
        ]

        col_widths = [1.8, 2.6, 4.8]  # symbol, name, meaning
        total_w = sum(col_widths)
        row_h = 0.62
        hdr_bg_col = CARD2_BG

        tbl_grp = VGroup()

        # Header row
        hdr_texts = ["Symbol", "Name", "Meaning"]
        hdr_colors = [YELLOW_H, BLUE_H, WHITE]
        hdr_bg = Rectangle(width=total_w, height=row_h,
                            fill_color=hdr_bg_col, fill_opacity=1,
                            stroke_opacity=0)
        hdr_bg.move_to(ORIGIN)
        hdr_cells = VGroup()
        left_x = -total_w / 2
        for c_i, (hdr, col) in enumerate(zip(hdr_texts, hdr_colors)):
            cx = left_x + sum(col_widths[:c_i]) + col_widths[c_i] / 2
            t = Text(hdr, font_size=22, color=col)
            t.move_to(hdr_bg.get_center() + RIGHT * cx)
            hdr_cells.add(t)
        tbl_grp.add(VGroup(hdr_bg, hdr_cells))

        for r_i, (sym_tex, sym_col, name_str, meaning_str) in enumerate(sym_data):
            row_bg = Rectangle(width=total_w, height=row_h,
                               fill_color=CARD_BG if r_i % 2 else CARD2_BG,
                               fill_opacity=1, stroke_opacity=0)
            row_bg.move_to(ORIGIN)

            sym_mt = MathTex(sym_tex, font_size=28, color=sym_col)
            cx_sym = -total_w / 2 + col_widths[0] / 2
            sym_mt.move_to(row_bg.get_center() + RIGHT * cx_sym)

            name_t = Text(name_str, font_size=19, color=WHITE)
            cx_name = -total_w / 2 + col_widths[0] + col_widths[1] / 2
            name_t.move_to(row_bg.get_center() + RIGHT * cx_name)
            if name_t.width > col_widths[1] - 0.1:
                name_t.set_width(col_widths[1] - 0.1)

            meaning_t = Text(meaning_str, font_size=18, color=LIGHT_GRAY)
            cx_mean = -total_w / 2 + col_widths[0] + col_widths[1] + col_widths[2] / 2
            meaning_t.move_to(row_bg.get_center() + RIGHT * cx_mean)
            if meaning_t.width > col_widths[2] - 0.1:
                meaning_t.set_width(col_widths[2] - 0.1)

            tbl_grp.add(VGroup(row_bg, sym_mt, name_t, meaning_t))

        tbl_grp.arrange(DOWN, buff=0)
        tbl_grp.center()
        tbl_grp.next_to(banner, DOWN, buff=0.35)
        tbl_grp.set_width(11.0)

        self.play(FadeIn(tbl_grp[0], run_time=0.5))
        for row in tbl_grp[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.3)

        self.show_sub(
            "Each coefficient tells us how much y-hat changes per one-unit increase in that feature.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S09 - Matrix / Vector Form
    # -------------------------------------------------------------------
    def s09_matrix_form(self):
        banner = section_banner("Matrix (Vector) Form",
                                "The compact form computers actually use")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("We can write the model compactly as y-hat = X times beta.", wait=3.0)

        eq = MathTex(
            r"\hat{y}", "=", r"X", r"\beta",
            font_size=64, color=WHITE
        )
        eq.set_color_by_tex(r"\hat{y}", YELLOW_H)
        eq.set_color_by_tex("X", BLUE_H)
        eq.set_color_by_tex(r"\beta", GREEN_H)
        eq.next_to(banner, DOWN, buff=0.5)
        self.play(Write(eq, run_time=1.2))

        desc_lines = [
            ("X", BLUE_H,
             "Design matrix (n x p+1). First column = ones for the intercept."),
            (r"\beta", GREEN_H,
             "Coefficient vector (p+1 x 1). What we solve for."),
        ]
        descs = VGroup()
        for sym, col, desc in desc_lines:
            sym_t = MathTex(sym, font_size=28, color=col)
            desc_t = Text(desc, font_size=20, color=LIGHT_GRAY)
            row = VGroup(sym_t, desc_t)
            row.arrange(RIGHT, buff=0.25)
            descs.add(row)

        descs.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        descs.next_to(eq, DOWN, buff=0.5)

        self.play(FadeIn(descs, shift=UP * 0.1, run_time=0.8))
        self.show_sub(
            "X is the design matrix. Each row is one sample. Beta is the column vector we solve for.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S10 - True Model & Error Term
    # -------------------------------------------------------------------
    def s10_error_term(self):
        banner = section_banner("The True Model " + EM + " Error Term")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("The true model includes an error term epsilon.", wait=2.5)

        eq = MathTex(
            r"y", "=",
            r"\beta_0 + \beta_1 x_1 + \cdots + \beta_n x_n",
            "+", r"\varepsilon",
            font_size=38, color=WHITE
        )
        eq.set_color_by_tex(r"\varepsilon", RED_H)
        eq.set_color_by_tex("y", YELLOW_H)
        eq.next_to(banner, DOWN, buff=0.45)
        self.play(Write(eq, run_time=1.5))

        eps_label = MathTex(
            r"\varepsilon \sim \mathcal{N}(0, \sigma^2)",
            font_size=34, color=RED_H
        )
        eps_label.next_to(eq, DOWN, buff=0.35)
        self.play(FadeIn(eps_label, run_time=0.7))

        points = [
            "Captures noise, measurement error, missing variables.",
            "Assumed normally distributed with mean 0.",
            "Constant variance (homoscedasticity).",
            "This assumption is about RESIDUALS, not raw data.",
        ]
        pts_grp = VGroup()
        for pt in points:
            txt = Text("* " + pt, font_size=20, color=LIGHT_GRAY)
            pts_grp.add(txt)
        pts_grp.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        pts_grp.next_to(eps_label, DOWN, buff=0.35)

        for pt in pts_grp:
            self.play(FadeIn(pt, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.3)

        self.show_sub(
            "Epsilon captures everything the model cannot explain. It is assumed N(0, sigma-squared).",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S11 - Coefficient Interpretation
    # -------------------------------------------------------------------
    def s11_coeff_interp(self):
        banner = section_banner("Interpreting Coefficients",
                                "What does beta = 150 mean?")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Let us interpret a coefficient in a house price model.", wait=2.5)

        box = RoundedRectangle(
            width=10.5, height=1.4, corner_radius=0.18,
            fill_color=CARD_BG, fill_opacity=1,
            stroke_color=GREEN_H, stroke_width=2.0
        )
        box.next_to(banner, DOWN, buff=0.5)

        eq = MathTex(r"\beta_1 = 150", font_size=36, color=GREEN_H)
        eq.move_to(box.get_left() + RIGHT * 1.5)

        meaning = Text(
            "Every extra sq ft raises predicted price by $150,\n"
            "holding all other features constant.",
            font_size=22, color=WHITE, line_spacing=1.15
        )
        meaning.move_to(box).shift(RIGHT * 0.9)

        self.play(Create(box, run_time=0.5))
        self.play(Write(eq, run_time=0.8))
        self.play(FadeIn(meaning, run_time=0.7))

        warn_bg = RoundedRectangle(
            width=10.5, height=1.1, corner_radius=0.14,
            fill_color="#2a1a0a", fill_opacity=1,
            stroke_color=ORANGE_H, stroke_width=1.5
        )
        warn_bg.next_to(box, DOWN, buff=0.3)
        warn_txt = Text(
            "Warning: Coefficients are NOT comparable if features are unscaled.\n"
            "Always standardise before comparing importance.",
            font_size=19, color=ORANGE_H, line_spacing=1.1
        )
        warn_txt.move_to(warn_bg)
        self.play(Create(warn_bg), FadeIn(warn_txt))
        self.show_sub(
            "Each coefficient is a partial effect " + EM + " the impact of one feature while others stay fixed.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S12 - OLS Cost Function
    # -------------------------------------------------------------------
    def s12_ols_cost(self):
        banner = section_banner("Ordinary Least Squares",
                                "Minimising the Mean Squared Error")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "OLS finds beta by minimising the Mean Squared Error.", wait=2.5
        )

        mse_eq = MathTex(
            r"\text{MSE}(\beta) = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2",
            r"= \frac{1}{n}\|y - X\beta\|^2",
            font_size=32, color=WHITE
        )
        mse_eq.next_to(banner, DOWN, buff=0.4)
        self.play(Write(mse_eq, run_time=1.6))
        self.show_sub(
            "MSE is the average squared difference between actual and predicted values.", wait=3.0
        )

        # Convex bowl plot
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 9, 2],
            x_length=5.5,
            y_length=3.2,
            axis_config={"color": LIGHT_GRAY, "stroke_width": 1.5},
            tips=False
        )
        axes.shift(DOWN * 1.2)
        x_lbl = VGroup(
            MathTex(r"\beta_1", font_size=20, color=LIGHT_GRAY),
            Text(" (coefficient value)", font_size=17, color=LIGHT_GRAY),
        )
        x_lbl.arrange(RIGHT, buff=0.08)
        x_lbl.next_to(axes.x_axis, DOWN, buff=0.2)
        y_lbl = Text("MSE Cost", font_size=17, color=LIGHT_GRAY)
        y_lbl.next_to(axes.y_axis, LEFT, buff=0.2).rotate(PI / 2)

        bowl = axes.plot(lambda x: x ** 2,
                         color=BLUE_H, stroke_width=2.5)

        min_dot = Dot(axes.coords_to_point(0, 0),
                      radius=0.1, color=GREEN_H)
        min_lbl = Text("Global Minimum", font_size=15, color=GREEN_H)
        min_lbl.next_to(min_dot, RIGHT, buff=0.15)

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl))
        self.play(Create(bowl, run_time=1.2))
        self.play(FadeIn(min_dot), FadeIn(min_lbl))

        bowl_note = Text(
            "MSE is convex " + EM + " one unique global minimum, no local minima!",
            font_size=19, color=YELLOW_H
        )
        # Place above the graph, below the equations
        bowl_note.next_to(mse_eq, DOWN, buff=0.22)
        self.play(FadeIn(bowl_note))
        self.show_sub(
            "The MSE bowl is convex. Gradient descent will always find the global minimum.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S13 - Why Square the Errors
    # -------------------------------------------------------------------
    def s13_why_square(self):
        banner = section_banner("Why Square the Errors?",
                                "Four good reasons")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Why not just sum raw errors? Here are four reasons.", wait=2.5)

        reasons = [
            ("1", BLUE_H,
             "Raw errors are +/- and cancel out. Squaring makes all positive."),
            ("2", GREEN_H,
             "Large errors penalised more than small ones " + EM + " desirable behaviour."),
            ("3", YELLOW_H,
             "Squared loss is differentiable everywhere " + EM + " needed for calculus."),
            ("4", PURPLE_H,
             "Leads to a clean closed-form solution via the Normal Equation."),
        ]
        cards = VGroup()
        for num, col, text in reasons:
            bg = RoundedRectangle(
                width=10.5, height=0.82, corner_radius=0.12,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=col, stroke_width=1.8
            )
            n_txt = Text(num + ".", font_size=26,
                         color=col)
            n_txt.move_to(bg.get_left() + RIGHT * 0.45)
            txt = Text(text, font_size=21, color=WHITE)
            txt.move_to(bg).align_to(n_txt, LEFT).shift(RIGHT * 0.4)
            cards.add(VGroup(bg, n_txt, txt))

        cards.arrange(DOWN, buff=0.18)
        cards.next_to(banner, DOWN, buff=0.35)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.15, run_time=0.5))
            self.wait(0.4)

        self.show_sub(
            "Squaring errors ensures they are positive, penalises large errors, and enables calculus.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S14 - Normal Equation Derivation
    # -------------------------------------------------------------------
    def s14_normal_eq(self):
        banner = section_banner("The Normal Equation",
                                "Closed-form solution to OLS")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "By setting the derivative of MSE to zero, we get an exact formula for beta.",
            wait=3.0
        )

        steps = [
            (r"J = \frac{1}{n}(y-X\beta)^\top(y-X\beta)",
             "Write the cost function"),
            (r"\frac{\partial J}{\partial \beta} = \frac{1}{n}(-2X^\top y + 2X^\top X\beta)",
             "Differentiate w.r.t. beta"),
            (r"-2X^\top y + 2X^\top X\beta = 0",
             "Set derivative to zero"),
            (r"X^\top X\beta = X^\top y",
             "Rearrange (the Normal Equations)"),
            (r"\beta = (X^\top X)^{-1} X^\top y",
             "Solve for beta"),
        ]

        # Use a small, fixed font size.
        # Do NOT call set_width() -- that scales equations after rendering
        # and can push them into the banner.
        EQ_FS   = 22   # MathTex font size
        NOTE_FS = 14   # side-note font size

        step_grp = VGroup()
        for eq_str, note_str in steps:
            eq   = MathTex(eq_str,   font_size=EQ_FS,   color=WHITE)
            note = Text(note_str,    font_size=NOTE_FS,  color=LIGHT_GRAY)
            row  = VGroup(eq, note)
            row.arrange(RIGHT, buff=0.35)
            # If a row is wider than the frame, scale it down individually
            if row.width > 12.5:
                row.set_width(12.5)
            step_grp.add(row)

        step_grp.arrange(DOWN, buff=0.28, aligned_edge=LEFT)

        # Anchor the group below the banner with enough clearance
        step_grp.next_to(banner, DOWN, buff=0.45)

        # If total height overflows the bottom of the frame, compress spacing
        if step_grp.get_bottom()[1] < -3.4:
            step_grp.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            step_grp.next_to(banner, DOWN, buff=0.40)

        for i, row in enumerate(step_grp):
            self.play(FadeIn(row, shift=RIGHT * 0.15, run_time=0.55))
            self.wait(0.55)
            if i == len(step_grp) - 1:
                self.play(row[0].animate.set_color(GREEN_H))

        self.show_sub(
            "Beta = (X-transpose X) inverse times X-transpose y. This is the closed-form solution.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S15 - Normal Equation Pros & Cons
    # -------------------------------------------------------------------
    def s15_normal_eq_pc(self):
        pros = [
            "Exact solution in one shot " + EM + " no iterations",
            "Deterministic " + EM + " same answer every run",
            "Works well when n is large and p is small",
        ]
        cons = [
            "O(p^3) " + EM + " matrix inversion is very slow for many features",
            "Fails if X-transpose X is singular (multicollinearity or p > n)",
            "Memory intensive " + EM + " must hold p x p matrix in RAM",
            "Not suited for online / streaming learning",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Pros & Cons " + EM + " Normal Equation / OLS",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.show_sub("sklearn uses SVD " + EM + " numerically safer than direct matrix inversion.", wait=3.0)
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "The Normal Equation is exact but slow for large feature sets.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S16 - LINE-MO Assumptions Overview
    # -------------------------------------------------------------------
    def s16_linemo_overview(self):
        banner = section_banner("LINE-MO Assumptions",
                                "Six assumptions for statistical validity")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "Linear regression has six assumptions. Remember them with LINE-MO.",
            wait=3.0
        )

        letters = [
            ("L", BLUE_H,   "Linearity"),
            ("I", GREEN_H,  "Independence"),
            ("N", YELLOW_H, "Normality of Residuals"),
            ("E", ORANGE_H, "Equal Variance"),
            ("M", PURPLE_H, "No Multicollinearity"),
            ("O", RED_H,    "No Outliers / Leverage"),
        ]

        hexagons = VGroup()
        for letter, col, label in letters:
            hex_bg = RegularPolygon(n=6, radius=1.05,
                                    fill_color=CARD_BG, fill_opacity=1,
                                    stroke_color=col, stroke_width=2.5)
            let_txt = Text(letter, font_size=34, color=col)
            lab_txt = Text(label, font_size=12, color=WHITE)
            let_txt.move_to(hex_bg).shift(UP * 0.15)
            lab_txt.move_to(hex_bg).shift(DOWN * 0.35)
            # Scale label if it spills outside hexagon width (~1.8)
            if lab_txt.width > 1.7:
                lab_txt.set_width(1.7)
            hexagons.add(VGroup(hex_bg, let_txt, lab_txt))

        hexagons.arrange_in_grid(rows=2, cols=3, buff=0.22)
        hexagons.next_to(banner, DOWN, buff=0.4)

        for hx in hexagons:
            self.play(FadeIn(hx, scale=0.85, run_time=0.45))
            self.wait(0.2)

        self.show_sub(
            "Linearity, Independence, Normality, Equal Variance, No Multicollinearity, No Outliers.",
            wait=4.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S17 - Linearity Assumption (Plots)
    # -------------------------------------------------------------------
    def s17_linearity(self):
        banner = section_banner("L " + EM + " Linearity",
                                "Residuals vs Fitted plots")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "Linearity: the mean of y is a linear function of X.",
            wait=2.5
        )

        # Good plot - random scatter
        ax_good = Axes(
            x_range=[0, 10, 2], y_range=[-3, 3, 1],
            x_length=4.5, y_length=2.8,
            axis_config={"color": LIGHT_GRAY, "stroke_width": 1.2},
            tips=False
        )
        ax_good.shift(LEFT * 3.4 + DOWN * 0.5)

        good_lbl = Text("Random Scatter (Good)",
                        font_size=18, color=GREEN_H)
        good_lbl.next_to(ax_good, UP, buff=0.12)

        np.random.seed(7)
        good_pts = VGroup()
        for xi in np.linspace(0.5, 9.5, 28):
            yi = np.random.normal(0, 1.0)
            good_pts.add(Dot(ax_good.coords_to_point(xi, yi),
                             radius=0.055, color=BLUE_H))

        zero_line_good = DashedVMobject(
            ax_good.plot(lambda x: 0, color=RED_H, stroke_width=1.5),
            num_dashes=18, dashed_ratio=0.5
        )

        # Bad plot - U-shape
        ax_bad = Axes(
            x_range=[0, 10, 2], y_range=[-3, 3, 1],
            x_length=4.5, y_length=2.8,
            axis_config={"color": LIGHT_GRAY, "stroke_width": 1.2},
            tips=False
        )
        ax_bad.shift(RIGHT * 3.4 + DOWN * 0.5)

        bad_lbl = Text("U-Shape Pattern (Bad)",
                       font_size=18, color=RED_H)
        bad_lbl.next_to(ax_bad, UP, buff=0.12)

        bad_pts = VGroup()
        for xi in np.linspace(0.5, 9.5, 28):
            yi = -1.5 + 0.62 * (xi - 5) ** 2 / 5 + np.random.normal(0, 0.3)
            bad_pts.add(Dot(ax_bad.coords_to_point(xi, yi),
                            radius=0.055, color=ORANGE_H))

        zero_line_bad = DashedVMobject(
            ax_bad.plot(lambda x: 0, color=RED_H, stroke_width=1.5),
            num_dashes=18, dashed_ratio=0.5
        )

        self.play(
            Create(ax_good), Create(ax_bad),
            FadeIn(good_lbl), FadeIn(bad_lbl)
        )
        self.play(
            LaggedStart(
                *[FadeIn(d) for d in good_pts], lag_ratio=0.04
            ),
            LaggedStart(
                *[FadeIn(d) for d in bad_pts], lag_ratio=0.04
            )
        )
        self.play(
            Create(zero_line_good), Create(zero_line_bad)
        )
        self.show_sub(
            "Left: residuals scattered randomly " + EM + " linearity holds. Right: U-shape " + EM + " violated.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S18 - Linearity Pros & Cons
    # -------------------------------------------------------------------
    def s18_linearity_pc(self):
        pros = [
            "OLS is theoretically optimal (BLUE)",
            "Coefficients are easily interpretable",
            "Extrapolation is reasonable",
        ]
        cons = [
            "Predictions are systematically biased if violated",
            "Residuals show curved patterns " + EM + " visible in diagnostics",
            "Must add polynomial features or switch models",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Linearity Assumption " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.show_sub("Remedy: add polynomial features or log/sqrt transformations.", wait=3.0)
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "When linearity holds, OLS is BLUE. When violated, add polynomial features.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S19 - Homoscedasticity (Equal Variance)
    # -------------------------------------------------------------------
    def s19_homoscedasticity(self):
        banner = section_banner("E " + EM + " Equal Variance (Homoscedasticity)",
                                "Residual spread must be constant")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "Homoscedasticity: Var(epsilon | X) = sigma-squared. Constant residual variance.",
            wait=3.0
        )

        # Good - random spread
        ax_good = Axes(
            x_range=[0, 10, 2], y_range=[-4, 4, 2],
            x_length=4.5, y_length=2.8,
            axis_config={"color": LIGHT_GRAY, "stroke_width": 1.2},
            tips=False
        )
        ax_good.shift(LEFT * 3.4 + DOWN * 0.6)
        good_lbl = Text("Homoscedastic (Good)",
                        font_size=17, color=GREEN_H)
        good_lbl.next_to(ax_good, UP, buff=0.12)

        np.random.seed(42)
        good_pts = VGroup()
        for xi in np.linspace(0.5, 9.5, 30):
            yi = np.random.normal(0, 1.0)
            good_pts.add(Dot(ax_good.coords_to_point(xi, yi),
                             radius=0.055, color=BLUE_H))

        # Bad - fan shape
        ax_bad = Axes(
            x_range=[0, 10, 2], y_range=[-4, 4, 2],
            x_length=4.5, y_length=2.8,
            axis_config={"color": LIGHT_GRAY, "stroke_width": 1.2},
            tips=False
        )
        ax_bad.shift(RIGHT * 3.4 + DOWN * 0.6)
        bad_lbl = Text("Heteroscedastic " + EM + " Fan Out (Bad)",
                       font_size=17, color=RED_H)
        bad_lbl.next_to(ax_bad, UP, buff=0.12)

        bad_pts = VGroup()
        for xi in np.linspace(0.5, 9.5, 30):
            spread = 0.2 + 0.35 * xi
            yi = np.random.normal(0, spread)
            bad_pts.add(Dot(ax_bad.coords_to_point(xi, yi),
                            radius=0.055, color=ORANGE_H))

        self.play(
            Create(ax_good), Create(ax_bad),
            FadeIn(good_lbl), FadeIn(bad_lbl)
        )
        self.play(
            LaggedStart(*[FadeIn(d) for d in good_pts], lag_ratio=0.04),
            LaggedStart(*[FadeIn(d) for d in bad_pts], lag_ratio=0.04)
        )
        self.show_sub(
            "Left: constant spread (good). Right: spread grows with fitted value (fan shape " + EM + " bad).",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S20 - Homoscedasticity Pros & Cons
    # -------------------------------------------------------------------
    def s20_homo_pc(self):
        pros = [
            "OLS is efficient (BLUE) when variance is constant",
            "Standard errors, p-values, CIs are valid",
            "Residual plots are clean",
        ]
        cons = [
            "Standard errors are biased if violated (bad p-values)",
            "Confidence intervals are too narrow or too wide",
            "OLS is no longer the most efficient estimator",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Homoscedasticity " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.show_sub("Remedy: log-transform y, use WLS, or use HC3 standard errors.", wait=3.0)
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Heteroscedasticity makes standard errors wrong " + EM + " p-values become unreliable.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S21 - No Multicollinearity
    # -------------------------------------------------------------------
    def s21_multicollinearity(self):
        banner = section_banner("M " + EM + " No Multicollinearity",
                                "Predictors should not be highly correlated")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "Multicollinearity: predictor variables are highly correlated with each other.",
            wait=3.0
        )

        analogy = Text(
            "Analogy: predicting salary from\n"
            "height in cm AND height in inches.\n"
            "They are the same thing " + EM + " the model\n"
            "has infinite ways to split the weight.",
            font_size=22, color=WHITE, line_spacing=1.2
        )
        analogy.next_to(banner, DOWN, buff=0.45)
        self.play(FadeIn(analogy, run_time=0.7))

        vif_eq = MathTex(
            r"\text{VIF}(\beta_j) = \frac{1}{1 - R^2_j}",
            font_size=36, color=PURPLE_H
        )
        vif_eq.next_to(analogy, DOWN, buff=0.4)
        self.play(Write(vif_eq, run_time=1.2))

        thresholds = VGroup(
            Text("VIF > 5 : Warning", font_size=21, color=YELLOW_H),
            Text("VIF > 10 : Severe " + EM + " remove or combine features",
                 font_size=21, color=RED_H),
        )
        thresholds.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        thresholds.next_to(vif_eq, DOWN, buff=0.35)
        self.play(FadeIn(thresholds, run_time=0.7))

        self.show_sub(
            "VIF measures how much one predictor is explained by the others. VIF > 10 is severe.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S22 - Multicollinearity Pros & Cons
    # -------------------------------------------------------------------
    def s22_multi_pc(self):
        pros = [
            "Stable and interpretable coefficients",
            "Standard errors are small",
            "Can compare feature importance meaningfully",
        ]
        cons = [
            "Coefficient estimates flip sign with small data changes",
            "Standard errors inflate " + EM + " wide confidence intervals",
            "Normal Equation may become numerically singular",
        ]
        layout = make_pros_cons(pros, cons,
                                title="No Multicollinearity " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.show_sub("Remedies: remove correlated features, PCA, or use Ridge regression.", wait=3.0)
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "High VIF makes coefficients unstable and potentially meaningless.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S23 - Independence of Errors
    # -------------------------------------------------------------------
    def s23_independence(self):
        banner = section_banner("I " + EM + " Independence of Errors",
                                "No autocorrelation in residuals")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "Independence: the error for observation i tells us nothing about observation j.",
            wait=3.0
        )

        points = [
            ("Cov(eps_i, eps_j) = 0 for i != j",
             BLUE_H,
             "No correlation between errors"),
            ("Common violation: time-series data",
             ORANGE_H,
             "Yesterday's error predicts today's"),
            ("Detect: Durbin-Watson test",
             GREEN_H,
             "Value ~2: none   ~0: positive   ~4: negative"),
            ("Remedy: ARIMA / GLS / lag features",
             YELLOW_H,
             "Handle sequential data structure"),
        ]

        rows = VGroup()
        for i_row, (eq_str, col, note_str) in enumerate(points):
            bg = RoundedRectangle(
                width=10.5, height=0.72, corner_radius=0.12,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=col, stroke_width=1.5
            )
            if i_row == 0:
                # Use MathTex for the covariance notation row
                txt = MathTex(
                    r"\text{Cov}(\varepsilon_i,\,\varepsilon_j)=0"
                    r"\;\text{ for }i\neq j",
                    font_size=24, color=col
                )
            else:
                txt = Text(eq_str, font_size=20, color=col)
            note = Text(note_str, font_size=17, color=LIGHT_GRAY)
            txt.move_to(bg.get_left() + RIGHT * 0.25).align_to(bg, LEFT)
            txt.shift(RIGHT * 0.25)
            note.move_to(bg.get_right() + LEFT * 0.2).align_to(bg, RIGHT)
            note.shift(LEFT * 0.25)
            rows.add(VGroup(bg, txt, note))

        rows.arrange(DOWN, buff=0.18)
        rows.next_to(banner, DOWN, buff=0.35)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.5))
            self.wait(0.4)

        self.show_sub(
            "Autocorrelation underestimates standard errors " + EM + " inflated t-stats and false significance.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S24 - Independence Pros & Cons
    # -------------------------------------------------------------------
    def s24_independence_pc(self):
        pros = [
            "Standard errors are correctly estimated",
            "No systematic patterns in residuals over time",
        ]
        cons = [
            "Standard errors underestimated " + EM + " inflated t-stats",
            "Predictions are poor for sequential data",
            "Model is systematically wrong in structured ways",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Independence of Errors " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.show_sub("Use Durbin-Watson test to detect autocorrelation.", wait=2.5)
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "For time-series data, use ARIMA or GLS instead of plain linear regression.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S25 - Normality of Residuals
    # -------------------------------------------------------------------
    def s25_normality(self):
        banner = section_banner("N " + EM + " Normality of Residuals",
                                "Residuals (not data) should be normal")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "The residuals should follow an approximate normal distribution.",
            wait=2.5
        )

        warn_bg = RoundedRectangle(
            width=10.5, height=0.85, corner_radius=0.14,
            fill_color="#1a1000", fill_opacity=1,
            stroke_color=YELLOW_H, stroke_width=1.8
        )
        warn_bg.next_to(banner, DOWN, buff=0.4)
        warn_txt = Text(
            "This is about the RESIDUALS " + EM + " not the raw features or target.",
            font_size=20, color=YELLOW_H
        )
        warn_txt.move_to(warn_bg)
        self.play(Create(warn_bg), FadeIn(warn_txt))

        points = [
            ("Detect: Q-Q plot", "Points on diagonal = normally distributed residuals"),
            ("Detect: Shapiro-Wilk test", "For small samples (n < 50)"),
            ("Detect: KS test", "For large samples"),
            ("Remedy: log/sqrt transform y", "Or remove extreme outliers"),
            ("CLT saves you for large n", "n > 30 makes this assumption less critical"),
        ]

        rows = VGroup()
        for lft, rgt in points:
            bg = RoundedRectangle(
                width=10.5, height=0.65, corner_radius=0.1,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=BLUE_H, stroke_opacity=0.35,
                stroke_width=1
            )
            lt = Text(lft, font_size=19, color=BLUE_H)
            rt = Text(rgt, font_size=17, color=LIGHT_GRAY)
            lt.move_to(bg.get_left() + RIGHT * 0.25).align_to(bg, LEFT)
            lt.shift(RIGHT * 0.25)
            rt.move_to(bg.get_right() + LEFT * 0.25).align_to(bg, RIGHT)
            rt.shift(LEFT * 0.25)
            rows.add(VGroup(bg, lt, rt))

        rows.arrange(DOWN, buff=0.12)
        rows.next_to(warn_bg, DOWN, buff=0.28)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.3)

        self.show_sub(
            "For large n, the Central Limit Theorem makes predictions fine even if residuals are not normal.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S26 - Normality Pros & Cons
    # -------------------------------------------------------------------
    def s26_normality_pc(self):
        pros = [
            "t-tests and F-tests on coefficients are exactly valid",
            "Confidence intervals are correctly sized",
            "Small-sample inference is reliable",
        ]
        cons = [
            "p-values and CIs may be inaccurate (especially for small n)",
            "For large n: CLT saves you " + EM + " predictions still fine",
            "For small n: use bootstrap confidence intervals",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Normality of Residuals " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.show_sub("Use Q-Q plots to visually assess residual normality.", wait=2.5)
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "This assumption mainly matters for inference, not prediction accuracy.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S27 - Outliers / Leverage
    # -------------------------------------------------------------------
    def s27_outliers(self):
        banner = section_banner("O " + EM + " No Extreme Outliers / Leverage",
                                "Three types of problematic points")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "Not all unusual points are equal. There are three distinct types.",
            wait=2.5
        )

        types = [
            ("Outlier", RED_H,
             "Unusual y value " + EM + " far from the regression line (high residual)."),
            ("High-Leverage Point", ORANGE_H,
             "Unusual X value " + EM + " far from the centroid of predictor space."),
            ("Influential Point", PURPLE_H,
             "High leverage + high residual = changes coefficients when removed.\n"
             "Measured by Cook's Distance."),
        ]

        cards = VGroup()
        CARD_W  = 10.5
        LBL_SLOT  = 2.4              # fixed px for label column
        DESC_SLOT = CARD_W - LBL_SLOT - 0.3  # remaining for description

        for name, col, desc in types:
            lbl = Text(name, font_size=19, color=col)
            desc_txt = Text(desc, font_size=16, color=WHITE, line_spacing=1.0)
            if desc_txt.width > DESC_SLOT:
                desc_txt.set_width(DESC_SLOT)
            needed_h = max(0.95, desc_txt.height + 0.34)
            bg = RoundedRectangle(
                width=CARD_W, height=needed_h, corner_radius=0.14,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=col, stroke_width=2.0
            )
            bg.move_to(ORIGIN)
            left = bg.get_left()[0]
            # Label centred in its slot
            lbl.move_to([left + LBL_SLOT / 2, 0, 0])
            if lbl.width > LBL_SLOT - 0.1:
                lbl.set_width(LBL_SLOT - 0.1)
            # Desc left-aligned immediately after label slot
            desc_txt.align_to([left + LBL_SLOT + 0.12, 0, 0], LEFT)
            cards.add(VGroup(bg, lbl, desc_txt))

        cards.arrange(DOWN, buff=0.2)
        cards.next_to(banner, DOWN, buff=0.35)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.15, run_time=0.55))
            self.wait(0.5)

        self.show_sub(
            "Influential points have both unusual X and unusual y " + EM + " they dominate the fit.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S28 - Outliers Pros & Cons
    # -------------------------------------------------------------------
    def s28_outliers_pc(self):
        pros = [
            "Coefficients represent the typical relationship",
            "MSE is a faithful measure of model error",
        ]
        cons = [
            "A single point can dominate the entire regression line",
            "Coefficients may be completely distorted",
            "RMSE is artificially inflated by outliers",
        ]
        layout = make_pros_cons(pros, cons,
                                title="No Outliers " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.show_sub("Remedy: investigate first, then transform y or use Huber regression.", wait=3.0)
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Never blindly remove outliers " + EM + " always understand why they exist.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S29 - Evaluation Metrics Overview
    # -------------------------------------------------------------------
    def s29_metrics_overview(self):
        banner = section_banner("Evaluation Metrics",
                                "Six ways to measure regression performance")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("There are six key metrics for evaluating regression models.", wait=2.5)

        metrics = [
            ("MSE",      BLUE_H,   "Mean Squared Error",          "0 = perfect, lower better"),
            ("RMSE",     GREEN_H,  "Root Mean Squared Error",      "Same units as y"),
            ("MAE",      YELLOW_H, "Mean Absolute Error",          "Robust to outliers"),
            ("R" + SUP2,       PURPLE_H, "Coefficient of Determination", MINUS + "inf to 1, higher better"),
            ("Adj R" + SUP2,   ORANGE_H, "Adjusted R" + SUP2,                  "Penalises useless features"),
            ("MAPE",     RED_H,    "Mean Abs. % Error",            "Percentage " + EM + " avoid if y~0"),
        ]

        cards = VGroup()
        for short, col, full, note in metrics:
            bg = RoundedRectangle(
                width=5.6, height=1.22, corner_radius=0.14,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=col, stroke_width=2.0
            )
            sh_txt = Text(short, font_size=26, color=col)
            fl_txt = Text(full, font_size=17, color=WHITE)
            nt_txt = Text(note, font_size=15, color=LIGHT_GRAY)
            sh_txt.move_to(bg.get_top() + DOWN * 0.32)
            fl_txt.move_to(bg).shift(DOWN * 0.08)
            nt_txt.move_to(bg.get_bottom() + UP * 0.28)
            cards.add(VGroup(bg, sh_txt, fl_txt, nt_txt))

        cards.arrange_in_grid(rows=2, cols=3, buff=0.15)
        cards.next_to(banner, DOWN, buff=0.25)
        # Ensure grid fits in frame width
        if cards.width > 13.0:
            cards.set_width(13.0)

        for card in cards:
            self.play(FadeIn(card, scale=0.9, run_time=0.45))
            self.wait(0.25)

        self.show_sub(
            "Each metric has strengths and weaknesses. Use multiple metrics together.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S30 - MSE Formula
    # -------------------------------------------------------------------
    def s30_mse(self):
        banner = section_banner("MSE " + EM + " Mean Squared Error")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("MSE is the average of squared prediction errors.", wait=2.5)

        eq = MathTex(
            r"\text{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2",
            font_size=44, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.5)
        self.play(Write(eq, run_time=1.5))
        self.show_sub(
            "Squaring penalises large errors heavily. Units are squared (e.g. dollars-squared).",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S31 - MSE Pros & Cons
    # -------------------------------------------------------------------
    def s31_mse_pc(self):
        pros = [
            "Differentiable " + EM + " mathematically clean for optimisation",
            "Penalises large errors more " + EM + " good for costly mistakes",
            "Convex " + EM + " unique global minimum",
        ]
        cons = [
            "Units are squared " + EM + " not directly interpretable",
            "Very sensitive to outliers",
            "Two models with different error distributions can have same MSE",
        ]
        layout = make_pros_cons(pros, cons, title="MSE " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.show_sub("MSE is the standard training objective for linear regression.", wait=2.5)
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "The squared units make MSE hard to interpret directly. Use RMSE for reporting.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S32 - RMSE Formula
    # -------------------------------------------------------------------
    def s32_rmse(self):
        banner = section_banner("RMSE " + EM + " Root Mean Squared Error")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("RMSE brings MSE back to the original units of y.", wait=2.5)

        eq = MathTex(
            r"\text{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}",
            font_size=42, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.5)
        self.play(Write(eq, run_time=1.5))

        example = Text(
            "Example: RMSE = 25,000 on house prices means\n"
            "predictions are off by approximately $25,000 on average.",
            font_size=21, color=YELLOW_H, line_spacing=1.2
        )
        example.next_to(eq, DOWN, buff=0.5)
        self.play(FadeIn(example, run_time=0.7))
        self.show_sub(
            "RMSE is the most widely used metric in regression. Same units as the target.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S33 - RMSE Pros & Cons
    # -------------------------------------------------------------------
    def s33_rmse_pc(self):
        pros = [
            "Same units as y " + EM + " directly interpretable",
            "Still penalises large errors (from squared term)",
            "Most widely used metric in regression competitions",
        ]
        cons = [
            "Still sensitive to outliers (inherited from MSE)",
            "Not scale-invariant " + EM + " cannot compare across different targets",
        ]
        layout = make_pros_cons(pros, cons, title="RMSE " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "RMSE is interpretable and widely used, but outliers can inflate it significantly.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S34 - MAE Formula
    # -------------------------------------------------------------------
    def s34_mae(self):
        banner = section_banner("MAE " + EM + " Mean Absolute Error")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("MAE treats all errors equally " + EM + " robust to outliers.", wait=2.5)

        eq = MathTex(
            r"\text{MAE} = \frac{1}{n}\sum_{i=1}^{n}|y_i - \hat{y}_i|",
            font_size=44, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.5)
        self.play(Write(eq, run_time=1.3))

        note = Text(
            "A $1,000 error is 10x worse than a $100 error " + EM + " not 100x as in MSE.",
            font_size=21, color=LIGHT_GRAY
        )
        note.next_to(eq, DOWN, buff=0.45)
        self.play(FadeIn(note, run_time=0.6))
        self.show_sub(
            "MAE is robust to outliers because absolute values do not amplify extreme errors.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S35 - MAE Pros & Cons
    # -------------------------------------------------------------------
    def s35_mae_pc(self):
        pros = [
            "Robust to outliers " + EM + " extremes do not dominate",
            "Same units as y " + EM + " easy to explain to stakeholders",
            "More interpretable average error than RMSE",
        ]
        cons = [
            "Not differentiable at 0 " + EM + " subgradient needed",
            "Treats all errors equally " + EM + " may underweight serious large errors",
            "Less mathematically clean than MSE for derivations",
        ]
        layout = make_pros_cons(pros, cons, title="MAE " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Choose MAE when outliers are real and you do not want them to dominate the metric.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S36 - R2 Formula + Bar Visual
    # -------------------------------------------------------------------
    def s36_r2(self):
        t = MathTex(r"R^2", font_size=44, color=BLUE_H)
        t_label = Text(" " + EM + " Coefficient of Determination",
                       font_size=44, color=BLUE_H)
        banner_row = VGroup(t, t_label)
        banner_row.arrange(RIGHT, buff=0.05)
        banner_row.to_edge(UP, buff=0.35)
        banner = banner_row
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("R-squared measures how much variance the model explains.", wait=2.5)

        eq = MathTex(
            r"R^2 = 1 - \frac{SS_{res}}{SS_{tot}}"
            r"= 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}",
            font_size=36, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.4)
        self.play(Write(eq, run_time=1.6))

        # Bar chart: SS_tot vs SS_res
        bar_grp = VGroup()
        bar_labels = [
            ("SS_tot", 3.2, BLUE_H, "Total variance"),
            ("SS_res", 0.7, RED_H,  "Unexplained"),
        ]
        for i, (name, height, col, note) in enumerate(bar_labels):
            bar = Rectangle(width=1.2, height=height,
                            fill_color=col, fill_opacity=0.85,
                            stroke_opacity=0)
            lbl = Text(name, font_size=17, color=col)
            nlbl = Text(note, font_size=15, color=LIGHT_GRAY)
            lbl.next_to(bar, UP, buff=0.08)
            nlbl.next_to(bar, DOWN, buff=0.08)
            grp = VGroup(lbl, bar, nlbl)
            bar_grp.add(grp)

        bar_grp.arrange(RIGHT, buff=1.2, aligned_edge=DOWN)
        bar_grp.next_to(eq, DOWN, buff=0.4)
        bar_grp.shift(LEFT * 2.5)

        r2_note = Text("R" + SUP2 + " = 1 " + MINUS + " (0.7 / 3.2) " + APPROX + " 0.78",
                       font_size=22, color=GREEN_H)
        r2_note.next_to(bar_grp, RIGHT, buff=0.8)

        self.play(FadeIn(bar_grp, run_time=0.8))
        self.play(FadeIn(r2_note, run_time=0.6))
        self.show_sub(
            "R-squared = 1 minus the ratio of unexplained to total variance. Closer to 1 is better.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S37 - R2 Interpretation Table
    # -------------------------------------------------------------------
    def s37_r2_table(self):
        banner = section_banner("R^2 " + EM + " Interpretation Guide")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("How to interpret different R-squared values.", wait=2.5)

        headers = ["R" + SUP2 + " Value", "Interpretation", "Context"]
        rows = [
            ["< 0",    "Worse than predicting the mean!", "Model is broken"],
            ["0.0",    "No better than baseline",         "Features explain nothing"],
            ["0.3-0.5","Moderate",                        "Social science, economics"],
            ["0.7-0.9","Good",                            "Typical ML regression task"],
            ["0.95+",  "Excellent",                       "Engineering, physics"],
            ["1.0",    "Perfect " + EM + " highly suspicious",     "Likely data leakage"],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, WHITE, LIGHT_GRAY])
        tbl.next_to(banner, DOWN, buff=0.35)
        tbl.set_width(11.5)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.3)

        self.show_sub(
            "R-squared of 1.0 is suspicious " + EM + " likely data leakage. Context determines what is good.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S38 - R2 Pros & Cons
    # -------------------------------------------------------------------
    def s38_r2_pc(self):
        pros = [
            "Scale-independent " + EM + " 0 to 1 range comparable across datasets",
            "Intuitive: model explains X% of the variance in y",
            "Widely understood " + EM + " good for reporting to stakeholders",
        ]
        cons = [
            "Always increases when you add features " + EM + " even useless ones",
            "Says nothing about assumption violations",
            "Can be negative on test sets if model is worse than baseline",
        ]
        layout = make_pros_cons(pros, cons, title="R" + SUP2 + " " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "R-squared always rises with more features. Use Adjusted R-squared for model selection.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S39 - Adjusted R2
    # -------------------------------------------------------------------
    def s39_adj_r2(self):
        t = MathTex(r"\text{Adjusted }R^2", font_size=40, color=BLUE_H)
        t_label = Text(" " + EM + " The Honest R" + SUP2,
                       font_size=40, color=BLUE_H)
        banner_row = VGroup(t, t_label)
        banner_row.arrange(RIGHT, buff=0.05)
        banner_row.to_edge(UP, buff=0.35)
        sub = Text("Penalises for adding useless features",
                   font_size=24, color=LIGHT_GRAY)
        sub.next_to(banner_row, DOWN, buff=0.18)
        banner = VGroup(banner_row, sub)
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Adjusted R-squared only improves if a new feature genuinely helps.", wait=3.0)

        eq = MathTex(
            r"\text{Adj } R^2 = 1 - (1 - R^2) \cdot \frac{n-1}{n-p-1}",
            font_size=38, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.5)
        self.play(Write(eq, run_time=1.5))

        note = Text(
            "n = number of samples    p = number of features\n"
            "Decreases when useless features are added.",
            font_size=20, color=LIGHT_GRAY, line_spacing=1.2
        )
        note.next_to(eq, DOWN, buff=0.4)
        self.play(FadeIn(note, run_time=0.6))
        self.show_sub(
            "Use Adjusted R-squared " + EM + " not plain R-squared " + EM + " when comparing models with different numbers of features.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S40 - Adjusted R2 Pros & Cons
    # -------------------------------------------------------------------
    def s40_adj_r2_pc(self):
        pros = [
            "Penalises model complexity " + EM + " prevents feature inflation",
            "Better for comparing models with different feature counts",
            "Decreases when useless features are added",
        ]
        cons = [
            "Still does not check assumption validity",
            "Does not measure predictive accuracy like CV does",
            "Can still be gamed by heavy training-set tuning",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Adjusted R" + SUP2 + " " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Adjusted R-squared is better than plain R-squared for comparing models.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S41 - MAPE Formula
    # -------------------------------------------------------------------
    def s41_mape(self):
        banner = section_banner("MAPE " + EM + " Mean Absolute Percentage Error")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("MAPE gives errors as percentages " + EM + " easily understood by business teams.", wait=3.0)

        eq = MathTex(
            r"\text{MAPE} = \frac{100}{n}\sum_{i=1}^{n}\frac{|y_i - \hat{y}_i|}{|y_i|}",
            font_size=40, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.5)
        self.play(Write(eq, run_time=1.5))

        note_line1 = Text(
            "MAPE = 5% means predictions are off by 5% on average.",
            font_size=21, color=YELLOW_H
        )
        warn_grp = VGroup(
            Text("Warning: undefined if any ", font_size=21, color=YELLOW_H),
            MathTex(r"y_i = 0", font_size=26, color=RED_H),
            Text("!", font_size=21, color=YELLOW_H),
        )
        warn_grp.arrange(RIGHT, buff=0.05)
        note_block = VGroup(note_line1, warn_grp)
        note_block.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        note_block.next_to(eq, DOWN, buff=0.45)
        self.play(FadeIn(note_block, run_time=0.6))
        self.show_sub(
            "MAPE is percentage-based " + EM + " great for business communication. Avoid when y can be zero.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S42 - MAPE Pros & Cons
    # -------------------------------------------------------------------
    def s42_mape_pc(self):
        pros = [
            "Percentage-based " + EM + " easily communicated to non-technical teams",
            "Scale-independent " + EM + " compare across different products",
            "Intuitive: MAPE = 5% is immediately meaningful",
        ]
        cons = [
            "Undefined when y_i = 0 (division by zero)",
            "Asymmetric " + EM + " over/under predictions penalised differently",
            "Heavily penalises underestimates when y is small",
        ]
        layout = make_pros_cons(pros, cons, title="MAPE " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Do not use MAPE when any target value is near zero " + EM + " it becomes undefined.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S43 - Gradient Descent: Why
    # -------------------------------------------------------------------
    def s43_gd_why(self):
        banner = section_banner("Gradient Descent",
                                "Iterative alternative to the Normal Equation")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "For millions of rows or thousands of features, the Normal Equation becomes impractical.",
            wait=3.0
        )

        analogy_bg = RoundedRectangle(
            width=10.5, height=2.0, corner_radius=0.18,
            fill_color=CARD_BG, fill_opacity=1,
            stroke_color=BLUE_H, stroke_width=1.5
        )
        analogy_bg.next_to(banner, DOWN, buff=0.4)
        analogy_txt = Text(
            "Analogy: You are blindfolded on a hilly landscape,\n"
            "trying to find the valley.\n"
            "At each step you feel which direction is downhill\n"
            "and take one step that way. Repeat until you stop going down.",
            font_size=20, color=WHITE, line_spacing=1.2
        )
        analogy_txt.move_to(analogy_bg)
        self.play(Create(analogy_bg), FadeIn(analogy_txt))
        self.show_sub(
            "Gradient descent is the algorithm behind all of deep learning too.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S44 - Gradient Descent Update Rule
    # -------------------------------------------------------------------
    def s44_gd_update(self):
        banner = section_banner("Gradient Descent Update Rule")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("At each step we move beta in the direction opposite to the gradient.", wait=3.0)

        eq1 = MathTex(
            r"\beta_{\text{new}} := \beta_{\text{old}} - \alpha \cdot \frac{\partial \text{MSE}}{\partial \beta}",
            font_size=38, color=WHITE
        )
        eq1.set_color_by_tex(r"\alpha", YELLOW_H)
        eq1.next_to(banner, DOWN, buff=0.45)
        self.play(Write(eq1, run_time=1.5))

        eq2 = MathTex(
            r"\frac{\partial \text{MSE}}{\partial \beta} = -\frac{2}{n}X^\top(y - X\beta)",
            font_size=34, color=LIGHT_GRAY
        )
        eq2.next_to(eq1, DOWN, buff=0.35)
        self.play(FadeIn(eq2, run_time=0.8))

        alpha_note = Text(
            "alpha = learning rate (step size). Most critical hyperparameter.",
            font_size=21, color=YELLOW_H
        )
        alpha_note.next_to(eq2, DOWN, buff=0.4)
        self.play(FadeIn(alpha_note, run_time=0.6))
        self.show_sub(
            "Alpha controls how large each step is. Too large and it diverges; too small and it is slow.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S45 - Gradient Descent Steps
    # -------------------------------------------------------------------
    def s45_gd_steps(self):
        banner = section_banner("Gradient Descent " + EM + " Algorithm Steps")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Here is the gradient descent algorithm step by step.", wait=2.5)

        # Each step: (prefix text, MathTex part, suffix text)
        step_data = [
            ("1. Initialise ",
             r"\beta",
             " (zeros or random small values)"),
            ("2. Predictions:  ",
             r"\hat{y} = X\beta",
             ""),
            ("3. Residuals:  ",
             r"e = y - \hat{y}",
             ""),
            ("4. Gradient:  ",
             r"\nabla = -\frac{2}{n} X^{\top} e",
             ""),
            ("5. Update:  ",
             r"\beta \leftarrow \beta - \alpha \cdot \nabla",
             ""),
            ("6. Repeat until  ",
             r"|\nabla| < \varepsilon",
             "  or max iterations reached"),
        ]

        cards = VGroup()
        for pre, math_str, post in step_data:
            bg = RoundedRectangle(
                width=10.5, height=0.68, corner_radius=0.1,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=BLUE_H, stroke_opacity=0.35, stroke_width=1
            )
            pre_t  = Text(pre,  font_size=19, color=WHITE)
            math_t = MathTex(math_str, font_size=24, color=YELLOW_H)
            post_t = Text(post, font_size=19, color=WHITE)
            row_inner = VGroup(pre_t, math_t, post_t)
            row_inner.arrange(RIGHT, buff=0.06)
            row_inner.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.18)
            if row_inner.width > 10.1:
                row_inner.set_width(10.1)
            cards.add(VGroup(bg, row_inner))

        cards.arrange(DOWN, buff=0.14)
        cards.next_to(banner, DOWN, buff=0.35)

        for i, card in enumerate(cards):
            col = BLUE_H if i < 4 else GREEN_H
            card[0].set_stroke(color=col, opacity=0.6)
            self.play(FadeIn(card, shift=RIGHT * 0.1, run_time=0.45))
            self.wait(0.3)

        self.show_sub(
            "Repeat these six steps until convergence. For linear regression, convergence is guaranteed.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S46 - Learning Rate Convergence Curves
    # -------------------------------------------------------------------
    def s46_learning_rate(self):
        banner = section_banner("Effect of Learning Rate (alpha)",
                                "Too high, too low, or just right")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("The learning rate alpha is the most critical hyperparameter in gradient descent.", wait=3.0)

        # -- Axes ----------------------------------------------------------
        axes = Axes(
            x_range=[0, 60, 10],
            y_range=[0, 2.4, 0.4],
            x_length=8.5,
            y_length=4.0,
            axis_config={"color": LIGHT_GRAY, "stroke_width": 1.5},
            tips=False
        )
        axes.shift(LEFT * 0.5 + DOWN * 0.8)

        x_lbl = Text("Iterations", font_size=17, color=LIGHT_GRAY)
        y_lbl = Text("Cost (MSE)", font_size=17, color=LIGHT_GRAY)
        x_lbl.next_to(axes.x_axis, DOWN, buff=0.22)
        y_lbl.next_to(axes.y_axis, LEFT, buff=0.22).rotate(PI / 2)

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl))

        # -- Curve 1: Good / Optimal alpha --------------------------------
        # Smooth fast exponential decay, converges to near-zero minimum
        optimal = axes.plot(
            lambda x: 2.1 * np.exp(-0.11 * x) + 0.08,
            x_range=[0, 60], color=GREEN_H, stroke_width=2.8
        )

        # -- Curve 2: Too low alpha ----------------------------------------
        # Same start, decays but very slowly. At iter 60 still around 0.8.
        slow = axes.plot(
            lambda x: 2.1 * np.exp(-0.022 * x) + 0.08,
            x_range=[0, 60], color=BLUE_H, stroke_width=2.5
        )

        # -- Curve 3: Too high alpha - sawtooth zigzag --------------------
        # Reference image behaviour:
        #   - Starts smooth like the others (drops cleanly for ~8 iterations)
        #   - THEN zigzag kicks in once it overshoots
        #   - Overall trend is downward, plateaus higher than optimal
        high_pts = []
        xs = np.linspace(0, 60, 800)
        zigzag_start = 8.0   # smooth drop before this, zigzag after
        for xi in xs:
            # Underlying downward trend (higher plateau than optimal)
            trend = 1.9 * np.exp(-0.055 * xi) + 0.35
            if xi < zigzag_start:
                # Smooth section: follow the trend closely (no zigzag yet)
                y = trend
            else:
                # Zigzag section: sawtooth on top of the trend
                t = xi - zigzag_start
                cycle = 3.2
                phase = (t % cycle) / cycle      # 0..1 per tooth
                amp = 0.28
                # Asymmetric tooth: 40% rise, 60% sharp drop
                if phase < 0.40:
                    tooth = amp * (phase / 0.40)
                else:
                    tooth = amp * (1.0 - (phase - 0.40) / 0.60)
                y = trend + tooth - amp * 0.5
            y = np.clip(y, 0.05, 2.35)
            high_pts.append(axes.coords_to_point(xi, y))
        high = VMobject(stroke_color=RED_H, stroke_width=2.5)
        high.set_points_as_corners(high_pts)

        # -- Legend: top-right, BELOW the banner title -----------------
        # Place it so it sits below the subtitle line, not over the title
        legend_items = VGroup(
            VGroup(
                Line(ORIGIN, RIGHT * 0.45, stroke_color=GREEN_H, stroke_width=3),
                Text(" Optimal alpha", font_size=15, color=GREEN_H),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Line(ORIGIN, RIGHT * 0.45, stroke_color=BLUE_H, stroke_width=3),
                Text(" Too low alpha", font_size=15, color=BLUE_H),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Line(ORIGIN, RIGHT * 0.45, stroke_color=RED_H, stroke_width=3),
                Text(" Too high alpha", font_size=15, color=RED_H),
            ).arrange(RIGHT, buff=0.1),
        )
        legend_items.arrange(DOWN, buff=0.20, aligned_edge=LEFT)
        # Position: right edge of frame, vertically between subtitle and graph
        legend_items.to_edge(RIGHT, buff=0.35)
        legend_items.set_y(banner.get_bottom()[1] - legend_items.height / 2 - 0.35)

        # -- Animate ---------------------------------------------------
        self.play(Create(optimal, run_time=1.8))
        self.play(FadeIn(legend_items[0]))
        self.show_sub("Optimal alpha: cost drops smoothly and converges.", wait=2.0)

        self.play(Create(slow, run_time=1.8))
        self.play(FadeIn(legend_items[1]))
        self.show_sub("Too low alpha: converging but painfully slow.", wait=2.0)

        self.play(Create(high, run_time=1.8))
        self.play(FadeIn(legend_items[2]))
        self.show_sub(
            "Too high alpha: looks promising for 3-4 steps, then explodes and never recovers.",
            wait=3.5
        )
        self.show_sub(
            "Optimal alpha gives smooth convergence. Too high diverges. Too low wastes time.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S47 - GD Types Table
    # -------------------------------------------------------------------
    def s47_gd_types(self):
        banner = section_banner("Types of Gradient Descent")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("There are three variants of gradient descent.", wait=2.5)

        headers = ["Type", "Batch Size", "Pros", "Cons", "When"]
        rows = [
            ["Batch GD",    "All n",   "Stable, exact gradient",
             "Slow per iter, needs all data in RAM",  "Small datasets"],
            ["Stoch. GD",   "1",       "Very fast updates",
             "Noisy, needs LR schedule",              "Huge datasets, online"],
            ["Mini-batch GD","16-512", "Best of both, GPU-friendly",
             "Extra batch size hyperparameter",       "Standard for deep learning"],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, BLUE_H, GREEN_H, RED_H, PURPLE_H],
                         font_size=18)
        tbl.next_to(banner, DOWN, buff=0.35)
        tbl.set_width(12.5)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.5))
            self.wait(0.5)

        self.show_sub(
            "Mini-batch gradient descent is the standard choice for most modern deep learning.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S48 - Gradient Descent Pros & Cons
    # -------------------------------------------------------------------
    def s48_gd_pc(self):
        pros = [
            "Scales to millions of samples and thousands of features",
            "Can use mini-batches " + EM + " memory efficient",
            "Foundation for deep learning",
            "Online learning capable",
        ]
        cons = [
            "Requires choosing learning rate alpha",
            "No single closed-form answer " + EM + " needs convergence check",
            "Sensitive to feature scaling " + EM + " must standardise first",
            "Not needed for linear regression with small p",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Gradient Descent " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.show_sub("For linear regression, GD always converges because MSE is convex.", wait=3.0)
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Gradient descent scales to big data where the Normal Equation would be too slow.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S49 - Regularisation: The Problem
    # -------------------------------------------------------------------
    def s49_reg_problem(self):
        banner = section_banner("Regularisation",
                                "Solving overfitting and large coefficients")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "When a model has many features, OLS can produce very large coefficients to fit noise.",
            wait=3.5
        )

        # Good fit vs overfit curves
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 6, 2],
            x_length=5.2,
            y_length=3.5,
            axis_config={"color": LIGHT_GRAY, "stroke_width": 1.5},
            tips=False
        )
        axes.shift(DOWN * 0.8)

        np.random.seed(10)
        xs = np.linspace(-2.5, 2.5, 10)
        ys = xs ** 2 + np.random.normal(0, 0.4, 10)

        dots = VGroup(*[
            Dot(axes.coords_to_point(x, y),
                radius=0.07, color=BLUE_H)
            for x, y in zip(xs, ys)
        ])

        good_fit = axes.plot(lambda x: x ** 2,
                             color=GREEN_H, stroke_width=2.5, x_range=[-2.8, 2.8])

        # Overfit polynomial (degree 9 oscillation approximated)
        def overfit_fn(x):
            return (x ** 2 - 0.9 * np.cos(3 * x) * x
                    + 0.2 * np.sin(5 * x))

        overfit_curve = axes.plot(
            overfit_fn, color=RED_H, stroke_width=2.0, x_range=[-2.8, 2.8]
        )

        good_lbl = Text("Good Fit (Green)", font_size=17, color=GREEN_H)
        over_lbl = Text("Overfit (Red)", font_size=17, color=RED_H)
        good_lbl.to_corner(UR, buff=0.5).shift(DOWN * 0.5)
        over_lbl.next_to(good_lbl, DOWN, buff=0.2)

        self.play(Create(axes), FadeIn(dots))
        self.play(Create(good_fit, run_time=1.0), FadeIn(good_lbl))
        self.play(Create(overfit_curve, run_time=1.2), FadeIn(over_lbl))
        self.show_sub(
            "The overfit model memorises training noise. It will fail on new data.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S50 - Ridge Cost Function
    # -------------------------------------------------------------------
    def s50_ridge(self):
        banner = section_banner("Ridge Regression (L2 Regularisation)")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Ridge adds the sum of squared coefficients as a penalty.", wait=2.5)

        eq = MathTex(
            r"\text{Cost} = \text{MSE}"
            r"+ \lambda \sum_j \beta_j^2"
            r"\quad (\text{L2 penalty})",
            font_size=38, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.45)
        self.play(Write(eq, run_time=1.6))

        closed_form = MathTex(
            r"\beta_{\text{Ridge}} = (X^\top X + \lambda I)^{-1} X^\top y",
            font_size=34, color=BLUE_H
        )
        closed_form.next_to(eq, DOWN, buff=0.4)
        self.play(FadeIn(closed_form, run_time=0.8))

        note_items = [
            (r"\lambda = 0",         ARROW + "  plain OLS"),
            (r"\lambda \to \infty",  ARROW + "  all betas to 0"),
            (None,                   "Adding lambda*I ensures the matrix is always invertible!"),
        ]
        notes_grp = VGroup()
        for math_part, text_part in note_items:
            if math_part:
                mt = MathTex(math_part, font_size=22, color=PURPLE_H)
                tt = Text("  " + text_part, font_size=20, color=LIGHT_GRAY)
                row = VGroup(Text("* ", font_size=20,
                                  color=LIGHT_GRAY), mt, tt)
                row.arrange(RIGHT, buff=0.05)
            else:
                # Render lambda*I as MathTex so lambda is a proper symbol
                row = VGroup(
                    Text("* Adding ", font_size=20, color=LIGHT_GRAY),
                    MathTex(r"\lambda I", font_size=24, color=PURPLE_H),
                    Text(" ensures the matrix is always invertible!",
                         font_size=20, color=LIGHT_GRAY),
                )
                row.arrange(RIGHT, buff=0.05)
            notes_grp.add(row)
        notes_grp.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        notes_grp.next_to(closed_form, DOWN, buff=0.35)
        self.play(FadeIn(notes_grp, run_time=0.8))
        self.show_sub(
            "Ridge shrinks all coefficients toward zero but never to exactly zero.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S51 - Ridge Pros & Cons
    # -------------------------------------------------------------------
    def s51_ridge_pc(self):
        pros = [
            "Handles multicollinearity " + EM + " distributes weight across correlated features",
            "Always has a unique, stable solution",
            "Closed-form " + EM + " still very fast to compute",
            "Keeps all features " + EM + " good when all features matter",
        ]
        cons = [
            "No feature selection " + EM + " all coefficients stay non-zero",
            "Coefficients are biased (trades bias for lower variance)",
            "Lambda must be tuned via cross-validation",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Ridge Regression " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Ridge is ideal when features are correlated. Use RidgeCV to tune lambda.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S52 - Lasso Cost Function
    # -------------------------------------------------------------------
    def s52_lasso(self):
        banner = section_banner("Lasso Regression (L1 Regularisation)")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Lasso adds absolute value of coefficients as penalty " + EM + " enabling feature selection.", wait=3.0)

        eq = MathTex(
            r"\text{Cost} = \text{MSE} + \lambda \sum_j |\beta_j|",
            font_size=42, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.5)
        self.play(Write(eq, run_time=1.3))

        key_note = Text(
            "Unlike Ridge, L1 can drive some coefficients to EXACTLY zero\n"
            "- performing automatic feature selection.",
            font_size=22, color=YELLOW_H, line_spacing=1.2
        )
        key_note.next_to(eq, DOWN, buff=0.45)
        self.play(FadeIn(key_note, run_time=0.7))
        self.show_sub(
            "Lasso performs automatic feature selection by pushing unimportant coefficients to zero.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S53 - Lasso Geometric Intuition
    # -------------------------------------------------------------------
    def s53_lasso_geometry(self):
        banner = section_banner("Why Lasso Creates Sparsity",
                                "Geometric intuition")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("The constraint regions have different shapes for Ridge and Lasso.", wait=2.5)

        # -------------------------------------------------------------------
        # Layout constants
        # -------------------------------------------------------------------
        unit     = 4.5 / 5.0            # scene units per axis unit
        c_r_ax   = 1.0                  # constraint radius in axis coords
        c_r_sc   = c_r_ax * unit        # constraint radius in scene units (0.9)
        ols_ax   = np.array([1.4, 1.6]) # OLS unconstrained solution (axis coords)

        # Contour scales chosen so:
        #   - Smallest contours sit inside and near the OLS point
        #   - r=1.85 is tangent to the circle at (~0.41, 0.91)
        #   - r=3.20 is tangent to the diamond at (1.0, 0.0)
        #   These are drawn as concentric ellipses: semi-axes a=r*0.8, b=r*0.5
        CONTOUR_SCALES = [0.4, 0.75, 1.15, 1.60, 2.10, 2.70, 3.20]

        # -------------------------------------------------------------------
        # Helper: build one panel
        # -------------------------------------------------------------------
        def make_panel(shift_x, constraint_mob, title_str,
                       intersect_ax, on_axis):
            ax = Axes(
                x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
                x_length=4.5, y_length=4.5,
                axis_config={"color": "#888888", "stroke_width": 1.2},
                tips=False
            )
            ax.shift(RIGHT * shift_x + DOWN * 0.55)

            b1_lbl = MathTex(r"\beta_1", font_size=18, color=LIGHT_GRAY)
            b1_lbl.next_to(ax.x_axis, DOWN, buff=0.18)
            b2_lbl = MathTex(r"\beta_2", font_size=18, color=LIGHT_GRAY)
            b2_lbl.next_to(ax.y_axis, LEFT, buff=0.15)
            title = Text(title_str, font_size=16, color="#00C8D4")
            title.next_to(ax, UP, buff=0.12)

            # MSE contours centred at OLS point
            ols_scene = ax.coords_to_point(*ols_ax)
            contours  = VGroup()
            for r in CONTOUR_SCALES:
                a_sc = r * unit * 0.8
                b_sc = r * unit * 0.5
                ell = Ellipse(
                    width=a_sc * 2, height=b_sc * 2,
                    stroke_color=WHITE, stroke_width=1.4,
                    stroke_opacity=0.90, fill_opacity=0
                )
                ell.move_to(ols_scene)
                contours.add(ell)

            # Constraint region at axis origin
            constraint_mob.move_to(ax.get_origin())

            # Grey OLS dot (upper-right, like reference)
            ols_dot = Dot(ols_scene, radius=0.09, color="#CCCCCC")

            # Orange intersection dot
            int_scene = ax.coords_to_point(*intersect_ax)
            int_dot   = Dot(int_scene, radius=0.11, color=ORANGE)

            # Label
            if on_axis:
                lbl = MathTex(r"\beta_2 = 0", font_size=15, color=ORANGE)
                lbl.next_to(int_dot, RIGHT, buff=0.10)
            else:
                lbl = Text("optimal", font_size=13, color=ORANGE)
                lbl.next_to(int_dot, UR, buff=0.07)

            return (VGroup(ax, b1_lbl, b2_lbl, title),
                    contours, constraint_mob, ols_dot, int_dot, lbl)

        # -------------------------------------------------------------------
        # Ridge panel (left)
        # -------------------------------------------------------------------
        ridge_c = Circle(
            radius=c_r_sc,
            stroke_color="#00C8D4", stroke_width=2.5,
            fill_color="#00B4C8", fill_opacity=0.55
        )
        r_base, r_contours, r_c, r_ols, r_int, r_lbl = make_panel(
            shift_x       = -3.3,
            constraint_mob = ridge_c,
            title_str      = "L2 regularisation (Ridge)",
            intersect_ax   = (0.94, 0.34),   # right side of circle, r=2.58 contour tangent
            on_axis        = False
        )

        # -------------------------------------------------------------------
        # Lasso panel (right)
        # -------------------------------------------------------------------
        d_side = c_r_sc * np.sqrt(2)
        lasso_c = Square(side_length=d_side)
        lasso_c.rotate(PI / 4)
        lasso_c.set_stroke(color="#00C8D4", width=2.5)
        lasso_c.set_fill(color="#00B4C8", opacity=0.55)

        l_base, l_contours, l_c, l_ols, l_int, l_lbl = make_panel(
            shift_x        = 3.3,
            constraint_mob = lasso_c,
            title_str      = "L1 regularisation (Lasso)",
            intersect_ax   = (1.0, 0.0),    # right corner of diamond; r=3.20 contour tangent here
            on_axis        = True
        )

        # -------------------------------------------------------------------
        # Animate
        # -------------------------------------------------------------------
        self.play(
            Create(r_base[0]), FadeIn(r_base[1:]),
            Create(l_base[0]), FadeIn(l_base[1:]),
            run_time=0.8
        )
        self.play(
            FadeIn(r_c, scale=0.5), FadeIn(l_c, scale=0.5),
            run_time=0.8
        )
        self.show_sub("Teal region: the constraint. Solution must stay inside.", wait=2.0)

        self.play(
            LaggedStart(*[Create(c) for c in r_contours], lag_ratio=0.10),
            LaggedStart(*[Create(c) for c in l_contours], lag_ratio=0.10),
            run_time=2.0
        )
        self.show_sub("Ellipses are MSE cost contours centred at the OLS solution.", wait=2.5)

        self.play(FadeIn(r_ols), FadeIn(l_ols))
        self.play(
            FadeIn(r_int), FadeIn(r_lbl),
            FadeIn(l_int), FadeIn(l_lbl),
        )

        explain = VGroup(
            Text("Ridge: contour meets circle OFF-axis  => both betas non-zero",
                 font_size=16, color=GREEN_H),
            VGroup(
                Text("Lasso: contour hits CORNER  ", font_size=16, color=RED_H),
                MathTex(r"\Rightarrow \beta_2 = 0", font_size=20, color=RED_H),
            ).arrange(RIGHT, buff=0.08),
        )
        explain.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        explain.to_edge(DOWN, buff=0.38)
        self.play(FadeIn(explain))

        self.show_sub(
            "Ridge shrinks both betas. Lasso hits the corner and sets one beta to exactly zero.",
            wait=4.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S54 - Lasso Pros & Cons
    # -------------------------------------------------------------------
    def s54_lasso_pc(self):
        pros = [
            "Built-in feature selection " + EM + " zero coefficients remove irrelevant features",
            "Produces sparse models " + EM + " easier to interpret",
            "Good when true model is sparse (few features truly matter)",
        ]
        cons = [
            "No closed form " + EM + " iterative coordinate descent required",
            "Arbitrarily picks one feature from a correlated group",
            "Lambda must be tuned; too high zeroes out important features",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Lasso Regression " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Lasso is great for feature selection. Use ElasticNet when features are correlated.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S55 - ElasticNet
    # -------------------------------------------------------------------
    def s55_elasticnet(self):
        banner = section_banner("ElasticNet (L1 + L2 Combined)")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("ElasticNet combines Ridge and Lasso " + EM + " best of both worlds.", wait=2.5)

        eq = MathTex(
            r"\text{Cost} = \text{MSE} + \alpha "
            r"\Big[r\sum|\beta_j| + \frac{1-r}{2}\sum\beta_j^2\Big]",
            font_size=34, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.45)
        self.play(Write(eq, run_time=1.6))

        params = VGroup(
            Text("alpha = overall penalty strength", font_size=20, color=BLUE_H),
            Text("l1_ratio (r): 0 = pure Ridge    1 = pure Lasso    0.5 = equal mix",
                 font_size=20, color=GREEN_H),
        )
        params.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        params.next_to(eq, DOWN, buff=0.45)
        self.play(FadeIn(params, run_time=0.8))
        self.show_sub(
            "l1_ratio controls the mix: 0 is Ridge, 1 is Lasso. Tune both alpha and l1_ratio.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S56 - ElasticNet Pros & Cons
    # -------------------------------------------------------------------
    def s56_enet_pc(self):
        pros = [
            "Best of both worlds " + EM + " sparsity from L1 + stability from L2",
            "Handles groups of correlated features better than Lasso alone",
            "More robust than Lasso in high-dimensional settings",
        ]
        cons = [
            "Two hyperparameters to tune (alpha and l1_ratio)",
            "No closed form " + EM + " iterative, slower than Ridge",
            "Often overkill if setting is clear",
        ]
        layout = make_pros_cons(pros, cons,
                                title="ElasticNet " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "ElasticNet is useful when you have both correlated features and want some sparsity.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S57 - Regularisation Comparison Table
    # -------------------------------------------------------------------
    def s57_reg_table(self):
        banner = section_banner("Regularisation Comparison",
                                "OLS vs Ridge vs Lasso vs ElasticNet")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Here is a side-by-side comparison of all four methods.", wait=2.5)

        headers = ["Property", "OLS", "Ridge (L2)", "Lasso (L1)", "ElasticNet"]
        rows = [
            ["Penalty",           "None",   "Sum beta" + SUP2, "Sum |beta|",  "Both"],
            ["Feature selection", "No",     "No",              "Yes (zeros)", "Partial"],
            ["Multicollinearity", "Poorly", "Yes",             "Partially",   "Yes"],
            ["Sparsity",          "No",     "No",              "Yes",         "Partial"],
            ["Closed form",       "Yes",    "Yes",             "No",          "No"],
            ["Hyperparameters",   "0",      "1 (alpha)",       "1 (alpha)",   "2 (alpha+r)"],
        ]

        # Build a compact table manually so we can control row_h precisely.
        # 7 rows x row_h + banner ~ 8 units, so row_h must be <= 0.46
        FS       = 13    # cell font size
        FS_HDR   = 15    # header font size
        ROW_H    = 0.46  # row height -- keeps 7 rows + banner inside the frame
        COL_PAD  = 0.30  # padding per column

        all_rows_data = [headers] + rows
        n_col = len(headers)
        col_colors = [YELLOW_H, LIGHT_GRAY, BLUE_H, RED_H, PURPLE_H]

        # Measure column widths
        col_w = [0.0] * n_col
        cell_texts = []
        for r_i, row in enumerate(all_rows_data):
            r_cells = []
            for c_i, cell in enumerate(row):
                fs  = FS_HDR if r_i == 0 else FS
                wt  = None  # weight param removed for Pango compatibility
                col = col_colors[c_i]
                t   = Text(str(cell), font_size=fs, color=col)
                col_w[c_i] = max(col_w[c_i], t.width)
                r_cells.append(t)
            cell_texts.append(r_cells)

        col_w   = [w + COL_PAD for w in col_w]
        total_w = sum(col_w)

        tbl = VGroup()
        for r_i, r_cells in enumerate(cell_texts):
            bg_col = CARD2_BG if r_i % 2 == 0 else CARD_BG
            row_bg = Rectangle(width=total_w, height=ROW_H,
                               fill_color=bg_col, fill_opacity=1,
                               stroke_opacity=0)
            row_bg.move_to(ORIGIN)
            left_x = -total_w / 2
            for c_i, cell_txt in enumerate(r_cells):
                cx = left_x + sum(col_w[:c_i]) + col_w[c_i] / 2
                cell_txt.move_to(row_bg.get_center() + RIGHT * cx)
                max_w = col_w[c_i] - 0.08
                if cell_txt.width > max_w:
                    cell_txt.set_width(max_w)
            tbl.add(VGroup(row_bg, *r_cells))

        tbl.arrange(DOWN, buff=0)
        # Scale width to fit frame without exceeding it
        if tbl.width > 13.0:
            tbl.set_width(13.0)
        # Position: clear the banner by at least 0.5 units
        tbl.next_to(banner, DOWN, buff=0.50)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.3)

        self.show_sub(
            "Only Lasso and ElasticNet perform feature selection by setting coefficients to zero.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S58 - Residual Diagnostics: 4 Plots
    # -------------------------------------------------------------------
    def s58_diagnostics(self):
        banner = section_banner("Residual Diagnostics",
                                "Run these 4 plots after every fit")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("After fitting, always run four diagnostic plots.", wait=2.5)

        panels_info = [
            ("1. Residuals vs Fitted",
             "Random scatter = linearity + homoscedasticity OK",
             GREEN_H),
            ("2. Normal Q-Q",
             "Points on diagonal = residuals normally distributed",
             BLUE_H),
            ("3. Scale-Location",
             "Flat red line = homoscedastic (good)",
             YELLOW_H),
            ("4. Cook's Distance",
             "High Cook's D = investigate that point",
             RED_H),
        ]

        panels = VGroup()
        for title_str, note_str, col in panels_info:
            bg = RoundedRectangle(
                width=5.5, height=2.1, corner_radius=0.15,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=col, stroke_width=2.0
            )
            t = Text(title_str, font_size=18, color=col)
            n = Text(note_str, font_size=15, color=WHITE,
                     line_spacing=1.1)
            t.move_to(bg.get_top() + DOWN * 0.38)
            n.move_to(bg).shift(DOWN * 0.25)
            panels.add(VGroup(bg, t, n))

        panels.arrange_in_grid(rows=2, cols=2, buff=0.22)
        panels.next_to(banner, DOWN, buff=0.3)

        for panel in panels:
            self.play(FadeIn(panel, scale=0.9, run_time=0.5))
            self.wait(0.35)

        self.show_sub(
            "These four plots reveal violations of linearity, normality, homoscedasticity, and influence.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S59 - Cook's Distance
    # -------------------------------------------------------------------
    def s59_cooks(self):
        banner = section_banner("Cook's Distance",
                                "Measuring influence of each observation")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "Cook's Distance measures how much all fitted values change when one point is removed.",
            wait=3.5
        )

        eq = MathTex(
            r"D_i = \frac{(\hat{y}_{(-i)} - \hat{y})^\top(\hat{y}_{(-i)} - \hat{y})}{p \cdot \text{MSE}}",
            font_size=36, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.5)
        self.play(Write(eq, run_time=1.5))

        thresholds = VGroup(
            Text("Cook's D > 4/n   ->   investigate the point",
                 font_size=22, color=YELLOW_H),
            Text("Cook's D > 1     ->   very high influence",
                 font_size=22, color=RED_H),
        )
        thresholds.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        thresholds.next_to(eq, DOWN, buff=0.45)
        self.play(FadeIn(thresholds, run_time=0.7))
        self.show_sub(
            "An influential point has both unusual X and unusual y. Investigate it before removing.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S60 - Diagnostics Pros & Cons (Influence)
    # -------------------------------------------------------------------
    def s60_diag_pc(self):
        pros = [
            "No single point dominates the regression",
            "Coefficients are representative of the full dataset",
            "Robust and reliable estimates",
        ]
        cons = [
            "A single point could be controlling the entire model",
            "Removing it drastically changes predictions",
            "Model is not capturing the general pattern",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Influential Points " + EM + " Impact",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.show_sub("Always use Cook's Distance plot to identify influential observations.", wait=3.0)
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Never blindly remove influential points. Investigate their cause first.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S61 - Feature Engineering: Transforms Table
    # -------------------------------------------------------------------
    def s61_feat_eng(self):
        banner = section_banner("Feature Engineering",
                                "Extending linear regression to handle non-linearity")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub(
            "Linear regression only captures linear relationships. Feature engineering extends it.",
            wait=3.0
        )

        headers = ["Transform", "When to Use", "Effect"]
        rows = [
            ["log(x)",  "Right-skewed features (income, population)", "Compresses large values"],
            ["log(y)",  "Right-skewed target (house prices)",         "Fixes heteroscedasticity"],
            ["sqrt(x)", "Count data, moderate skew",                  "Gentler compression"],
            ["x" + SUP2,     "U-shape or inverted-U relationship",         "Adds curvature"],
            ["1/x",     "Inverse relationships (speed ~ 1/time)",     "Captures hyperbolic patterns"],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, LIGHT_GRAY, GREEN_H],
                         font_size=18)
        tbl.next_to(banner, DOWN, buff=0.35)
        tbl.set_width(12.0)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.35)

        self.show_sub(
            "Log transformation is the most common fix for skewed features and heteroscedasticity.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S62 - Interaction Terms
    # -------------------------------------------------------------------
    def s62_interactions(self):
        banner = section_banner("Interaction Terms",
                                "When effect of one feature depends on another")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Interaction terms let the effect of one feature depend on another.", wait=3.0)

        eq = MathTex(
            r"\hat{y} = \beta_0 + \beta_1 x_{\text{ad}} + \beta_2 x_{\text{peak}}"
            r"+ \beta_3 (x_{\text{ad}} \times x_{\text{peak}})",
            font_size=30, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.45)
        self.play(Write(eq, run_time=1.6))

        note_row = VGroup(
            MathTex(r"\beta_3", font_size=28, color=YELLOW_H),
            Text(" captures the extra boost advertising gets during peak season.",
                 font_size=22, color=YELLOW_H),
        )
        note_row.arrange(RIGHT, buff=0.06)
        note_row.next_to(eq, DOWN, buff=0.4)
        self.play(FadeIn(note_row, run_time=0.6))

        warnings = VGroup(
            Text("Pros: captures conditional effects, model stays linear in parameters.",
                 font_size=19, color=GREEN_H),
            Text("Cons: combinatorial explosion with many features; hard to interpret.",
                 font_size=19, color=RED_H),
        )
        warnings.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        warnings.next_to(note_row, DOWN, buff=0.35)
        self.play(FadeIn(warnings, run_time=0.7))
        self.show_sub(
            "Interaction terms allow linear regression to capture conditional effects.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S63 - Encoding Categorical Features
    # -------------------------------------------------------------------
    def s63_encoding(self):
        banner = section_banner("Encoding Categorical Features",
                                "Linear regression requires all numeric inputs")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Categorical features must be encoded as numbers.", wait=2.5)

        headers = ["Method", "What It Does", "When to Use", "Trap"]
        rows = [
            ["One-Hot Encoding",
             "Creates k-1 binary columns",
             "Nominal categories",
             "Drop one column " + EM + " dummy variable trap"],
            ["Ordinal Encoding",
             "Assigns integers 0,1,2...",
             "Ordered categories",
             "Implies equal spacing"],
            ["Target Encoding",
             "Replace with mean of y",
             "High-cardinality categories",
             "Data leakage risk"],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, LIGHT_GRAY, GREEN_H, RED_H],
                         font_size=17)
        tbl.next_to(banner, DOWN, buff=0.35)
        tbl.set_width(13.0)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.4)

        warn = Text(
            "Warning: Dummy Variable Trap " + EM + " always drop one category to avoid perfect multicollinearity.",
            font_size=18, color=ORANGE_H
        )
        warn.next_to(tbl, DOWN, buff=0.25)
        self.play(FadeIn(warn, run_time=0.6))
        self.show_sub(
            "One-hot encoding is most common. Always drop one column to avoid the dummy variable trap.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S64 - Feature Scaling Table
    # -------------------------------------------------------------------
    def s64_scaling(self):
        banner = section_banner("Feature Scaling",
                                "Required for regularisation and gradient descent")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Feature scaling is mandatory for Ridge, Lasso, and gradient descent.", wait=3.0)

        headers = ["Method", "Formula", "Pros", "Cons", "Use When"]
        rows = [
            ["StandardScaler",
             "(x - mu) / sigma",
             "Works for most algorithms",
             "Does not bound to [0,1]",
             "Default choice"],
            ["MinMaxScaler",
             "(x - min) / (max - min)",
             "Bounded [0,1]",
             "Sensitive to outliers",
             "Image data, NNs"],
            ["RobustScaler",
             "(x - median) / IQR",
             "Robust to outliers",
             "Not bounded",
             "Data with many outliers"],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, BLUE_H, GREEN_H, RED_H, PURPLE_H],
                         font_size=17)
        tbl.next_to(banner, DOWN, buff=0.35)
        tbl.set_width(13.5)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.4)

        self.show_sub(
            "StandardScaler is the default. RobustScaler is better when your data has many outliers.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S65 - Overfitting / Underfitting - 3 Curves
    # -------------------------------------------------------------------
    def s65_overfit(self):
        banner = section_banner("Overfitting, Underfitting & Bias-Variance",
                                "The three regimes")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("There are three regimes: underfitting, good fit, and overfitting.", wait=3.0)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 2],
            x_length=7.0,
            y_length=3.8,
            axis_config={"color": LIGHT_GRAY, "stroke_width": 1.2},
            tips=False
        )
        axes.shift(DOWN * 0.8)

        np.random.seed(42)
        xs = np.linspace(-2.5, 2.5, 12)
        ys = xs ** 2 + np.random.normal(0, 0.5, 12)
        dots = VGroup(*[
            Dot(axes.coords_to_point(x, y), radius=0.07, color=WHITE)
            for x, y in zip(xs, ys)
        ])

        underfit = axes.plot(
            lambda x: 4.5 + 0 * x,
            color=ORANGE_H, stroke_width=2.2, x_range=[-2.8, 2.8]
        )
        good = axes.plot(
            lambda x: x ** 2,
            color=GREEN_H, stroke_width=2.5, x_range=[-2.8, 2.8]
        )
        overfit_fn = (
            lambda x: x ** 2
            - 0.7 * np.cos(4 * x) * x
            + 0.3 * np.sin(6 * x)
        )
        over = axes.plot(
            overfit_fn,
            color=RED_H, stroke_width=2.0, x_range=[-2.7, 2.7]
        )

        labels = VGroup(
            Text("Underfit " + EM + " High Bias", font_size=16, color=ORANGE_H),
            Text("Good Fit", font_size=16, color=GREEN_H),
            Text("Overfit " + EM + " High Variance", font_size=16, color=RED_H),
        )
        labels.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        labels.to_corner(UR, buff=0.35)
        labels.shift(DOWN * 0.5)

        self.play(Create(axes), FadeIn(dots))
        self.play(Create(underfit, run_time=1.0), FadeIn(labels[0]))
        self.show_sub("Underfit: flat line misses the curve " + EM + " high bias.", wait=2.0)
        self.play(Create(good, run_time=1.0), FadeIn(labels[1]))
        self.show_sub("Good fit: captures the true pattern, generalises well.", wait=2.0)
        self.play(Create(over, run_time=1.2), FadeIn(labels[2]))
        self.show_sub("Overfit: passes through every point " + EM + " will fail on new data.", wait=3.0)
        self.clear_scene()

    # -------------------------------------------------------------------
    # S66 - Bias-Variance Decomposition
    # -------------------------------------------------------------------
    def s66_bias_variance(self):
        banner = section_banner("Bias-Variance Tradeoff",
                                "Every model's error has three components")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Every model's expected error decomposes into three parts.", wait=2.5)

        eq = MathTex(
            r"E[(y-\hat{y})^2] = \text{Bias}^2 + \text{Variance} + \text{Irreducible Noise}",
            font_size=32, color=WHITE
        )
        eq.next_to(banner, DOWN, buff=0.5)
        self.play(Write(eq, run_time=1.8))

        headers = ["Component", "Meaning", "Caused By", "Reduced By"]
        rows = [
            ["Bias" + SUP2,
             "Systematic error " + EM + " consistently wrong",
             "Model too simple",
             "More features, polynomial terms"],
            ["Variance",
             "Sensitivity " + EM + " changes with training data",
             "Model too complex",
             "Regularisation, more data"],
            ["Irreducible Noise",
             "Inherent randomness in y",
             "Measurement error, missing vars",
             "Cannot be reduced"],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, WHITE, ORANGE_H, GREEN_H],
                         font_size=17)
        tbl.next_to(eq, DOWN, buff=0.35)
        tbl.set_width(13.0)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.35)

        self.show_sub(
            "Regularisation trades off bias for variance " + EM + " the optimal lambda minimises total error.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S67 - Bias-Variance Tradeoff Curve
    # -------------------------------------------------------------------
    def s67_bv_curve(self):
        banner = section_banner("Bias-Variance Tradeoff Curve")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("As model complexity increases, bias drops but variance rises.", wait=3.0)

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 5, 1],
            x_length=8.0,
            y_length=3.8,
            axis_config={"color": LIGHT_GRAY, "stroke_width": 1.5},
            tips=False
        )
        axes.shift(DOWN * 0.8)

        x_lbl = Text("Model Complexity", font_size=17, color=LIGHT_GRAY)
        y_lbl = Text("Error", font_size=17, color=LIGHT_GRAY)
        x_lbl.next_to(axes.x_axis, DOWN, buff=0.2)
        y_lbl.next_to(axes.y_axis, LEFT, buff=0.2).rotate(PI / 2)

        bias_sq  = axes.plot(lambda x: 4 * np.exp(-0.45 * x) + 0.1,
                             color=BLUE_H, stroke_width=2.5, x_range=[0.1, 9.9])
        variance = axes.plot(lambda x: 0.08 * x ** 2 + 0.1,
                             color=RED_H, stroke_width=2.5, x_range=[0.1, 9.9])
        total    = axes.plot(lambda x: 4 * np.exp(-0.45 * x) + 0.08 * x ** 2 + 0.2,
                             color=GREEN_H, stroke_width=2.5, x_range=[0.1, 9.9])

        # Sweet spot line at x ~= 3.5
        sweet_x = 3.5
        sweet_y = 4 * np.exp(-0.45 * sweet_x) + 0.08 * sweet_x ** 2 + 0.2
        sweet_line = DashedLine(
            axes.coords_to_point(sweet_x, 0),
            axes.coords_to_point(sweet_x, sweet_y + 0.3),
            color=YELLOW_H, stroke_width=1.8
        )
        sweet_lbl = Text("Sweet Spot", font_size=15, color=YELLOW_H)
        sweet_lbl.next_to(axes.coords_to_point(sweet_x, sweet_y + 0.3), UP, buff=0.1)

        labels = VGroup(
            Text("Bias" + SUP2, font_size=16, color=BLUE_H),
            Text("Variance", font_size=16, color=RED_H),
            Text("Total Error", font_size=16, color=GREEN_H),
        )
        labels.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        labels.to_corner(UR, buff=0.35)
        labels.shift(DOWN * 0.4)

        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl))
        self.play(Create(bias_sq, run_time=1.2), FadeIn(labels[0]))
        self.play(Create(variance, run_time=1.2), FadeIn(labels[1]))
        self.play(Create(total, run_time=1.2), FadeIn(labels[2]))
        self.play(Create(sweet_line), FadeIn(sweet_lbl))
        self.show_sub(
            "The sweet spot minimises total error. It is found using cross-validation.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S68 - Bias-Variance Table (Linear Regression Specific)
    # -------------------------------------------------------------------
    def s68_bv_table(self):
        banner = section_banner("Bias-Variance " + EM + " Linear Regression Specifics")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("How bias and variance manifest in linear regression scenarios.", wait=3.0)

        headers = ["Situation", "Bias", "Variance", "Fix"]
        rows = [
            ["OLS, few features, true is non-linear",
             "High", "Low", "Add polynomial features"],
            ["OLS with many features, p near n",
             "Low",  "High", "Regularise with Ridge/Lasso"],
            ["Ridge with high lambda",
             "Moderate", "Low", "Reduce lambda via CV"],
            ["Ridge with lambda near 0",
             "Very low", "Higher", "Increase lambda"],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, BLUE_H, RED_H, GREEN_H],
                         font_size=18)
        tbl.next_to(banner, DOWN, buff=0.35)
        tbl.set_width(13.0)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.4)

        self.show_sub(
            "Regularisation increases bias but decreases variance. The optimal lambda balances both.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S69 - Cross-Validation: Why
    # -------------------------------------------------------------------
    def s69_cv_why(self):
        banner = section_banner("Cross-Validation",
                                "A more reliable performance estimate")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("A single train/test split can be lucky or unlucky.", wait=2.5)

        single_bg = RoundedRectangle(
            width=10.5, height=1.1, corner_radius=0.14,
            fill_color=CARD_BG, fill_opacity=1,
            stroke_color=ORANGE_H, stroke_width=1.5
        )
        single_bg.next_to(banner, DOWN, buff=0.4)
        single_txt = Text(
            "Single train/test split: high variance in performance estimate.\n"
            "You might get lucky " + EM + " or unlucky " + EM + " with how the split falls.",
            font_size=20, color=ORANGE_H, line_spacing=1.1
        )
        single_txt.move_to(single_bg)
        self.play(Create(single_bg), FadeIn(single_txt))

        cv_bg = RoundedRectangle(
            width=10.5, height=1.1, corner_radius=0.14,
            fill_color=CARD_BG, fill_opacity=1,
            stroke_color=GREEN_H, stroke_width=1.5
        )
        cv_bg.next_to(single_bg, DOWN, buff=0.28)
        cv_txt = Text(
            "Cross-validation averages over many splits " + EM + " much more reliable.\n"
            "Final score = mean of k fold scores.",
            font_size=20, color=GREEN_H, line_spacing=1.1
        )
        cv_txt.move_to(cv_bg)
        self.play(Create(cv_bg), FadeIn(cv_txt))
        self.show_sub(
            "Cross-validation gives a reliable performance estimate by using all data for both training and testing.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S70 - 5-Fold CV Diagram
    # -------------------------------------------------------------------
    def s70_cv_diagram(self):
        banner = section_banner("5-Fold Cross-Validation")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("In 5-fold CV, each fold takes a turn as the test set.", wait=2.5)

        fold_colors = [BLUE_H, GREEN_H, YELLOW_H, ORANGE_H, PURPLE_H]
        fold_w = 2.1
        fold_h = 0.55
        labels_l = VGroup()
        folds_grp = VGroup()

        for fold_i in range(5):
            fold_row = VGroup()
            row_lbl = Text(f"Fold {fold_i + 1}", font_size=17, color=WHITE)
            for col_i in range(5):
                is_test = (col_i == fold_i)
                rect = Rectangle(
                    width=fold_w, height=fold_h,
                    fill_color=fold_colors[col_i] if is_test else CARD_BG,
                    fill_opacity=0.85 if is_test else 1.0,
                    stroke_color=fold_colors[col_i],
                    stroke_width=1.2
                )
                cell_txt = Text(
                    "TEST" if is_test else "Train",
                    font_size=13,
                    color=WHITE if is_test else LIGHT_GRAY
                )
                cell_txt.move_to(rect)
                fold_row.add(VGroup(rect, cell_txt))

            fold_row.arrange(RIGHT, buff=0)
            row_lbl.next_to(fold_row, LEFT, buff=0.25)
            folds_grp.add(VGroup(row_lbl, fold_row))
            labels_l.add(row_lbl)

        folds_grp.arrange(DOWN, buff=0.14)
        folds_grp.next_to(banner, DOWN, buff=0.4)
        folds_grp.center()

        score_note = Text(
            "Final score = average of 5 test scores",
            font_size=21, color=GREEN_H
        )
        score_note.next_to(folds_grp, DOWN, buff=0.3)

        for row in folds_grp:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.5))
            self.wait(0.25)

        self.play(FadeIn(score_note, run_time=0.6))
        self.show_sub(
            "Each of the 5 folds acts as the test set exactly once. Average all 5 scores.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S71 - CV Pros & Cons
    # -------------------------------------------------------------------
    def s71_cv_pc(self):
        pros = [
            "More reliable performance estimate",
            "Uses all data for both training and testing",
            "Detects overfitting " + EM + " gap between train and CV score",
            "Required for tuning hyperparameters without leakage",
        ]
        cons = [
            "k times more expensive " + EM + " fits k models instead of 1",
            "Should not be used for time-series data (use TimeSeriesSplit)",
            "For very large datasets CV may be too slow",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Cross-Validation " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Cross-validation is essential for hyperparameter tuning without test set leakage.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S72 - Pipelines & Data Leakage
    # -------------------------------------------------------------------
    def s72_pipeline(self):
        banner = section_banner("Pipelines " + EM + " Preventing Data Leakage",
                                "The most common mistake in ML")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Data leakage inflates metrics " + EM + " the model secretly sees the test set.", wait=3.0)

        # WRONG block
        wrong_lbl = Text("WRONG " + EM + " leaks test data into scaler:",
                         font_size=17, color=RED_H)
        wrong_code = Text(
            "scaler = StandardScaler()\n"
            "X_scaled = scaler.fit_transform(X)\n"
            "X_train, X_test = train_test_split(X_scaled)",
            font_size=15, color=LIGHT_GRAY, line_spacing=1.15
        )
        wrong_inner = VGroup(wrong_lbl, wrong_code)
        wrong_inner.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        wrong_bg = RoundedRectangle(
            width=11.5,
            height=wrong_inner.height + 0.42,
            corner_radius=0.14,
            fill_color="#1a0a0a", fill_opacity=1,
            stroke_color=RED_H, stroke_width=2.0
        )
        wrong_bg.next_to(banner, DOWN, buff=0.30)
        wrong_inner.move_to(wrong_bg)
        self.play(Create(wrong_bg), FadeIn(wrong_inner))

        # CORRECT block
        right_lbl = Text("CORRECT " + EM + " scaler only sees training data:",
                         font_size=17, color=GREEN_H)
        right_code = Text(
            "pipeline = Pipeline([\n"
            "    ('scaler', StandardScaler()),\n"
            "    ('model',  LinearRegression())\n"
            "])\n"
            "pipeline.fit(X_train, y_train)",
            font_size=15, color=LIGHT_GRAY, line_spacing=1.15
        )
        right_inner = VGroup(right_lbl, right_code)
        right_inner.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        right_bg = RoundedRectangle(
            width=11.5,
            height=right_inner.height + 0.42,
            corner_radius=0.14,
            fill_color="#0a1a0a", fill_opacity=1,
            stroke_color=GREEN_H, stroke_width=2.0
        )
        right_bg.next_to(wrong_bg, DOWN, buff=0.22)
        right_inner.move_to(right_bg)
        self.play(Create(right_bg), FadeIn(right_inner))

        self.show_sub(
            "Always use a Pipeline. It ensures the scaler only sees training data.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S73 - Pipeline Pros & Cons
    # -------------------------------------------------------------------
    def s73_pipeline_pc(self):
        pros = [
            "Eliminates data leakage by design",
            "One object to fit, transform, and predict",
            "Works seamlessly with GridSearchCV and cross_val_score",
            "Serialise the whole workflow with one joblib.dump()",
        ]
        cons = [
            "Slightly harder to debug individual steps",
            "Parameter names need stepname__param prefix in GridSearch",
            "Custom transforms require writing a custom sklearn transformer",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Pipelines " + EM + " Pros & Cons",
                                font_size=20)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Pipelines are best practice. Always wrap your preprocessing inside one.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S74 - sklearn Hyperparams: LinearRegression
    # -------------------------------------------------------------------
    def s74_lr_params(self):
        banner = section_banner("sklearn Hyperparameters",
                                "LinearRegression")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("LinearRegression has four key parameters.", wait=2.5)

        headers = ["Parameter", "Default", "Effect", "Recommendation"]
        rows = [
            ["fit_intercept", "True",
             "Whether to compute beta_0",
             "Always True " + EM + " use False only with domain justification"],
            ["copy_X", "True",
             "Copy X before computation",
             "True is safe " + EM + " False saves memory but risky"],
            ["n_jobs", "None",
             "CPU cores " + EM + " -1 uses all",
             "Only helps for multi-output regression"],
            ["positive", "False",
             "Force all beta >= 0 (NNLS)",
             "True only if domain requires non-negative effects"],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, BLUE_H, LIGHT_GRAY, GREEN_H],
                         font_size=17)
        tbl.next_to(banner, DOWN, buff=0.35)
        tbl.set_width(13.5)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.45))
            self.wait(0.4)

        self.show_sub(
            "Base LinearRegression has essentially zero hyperparameters to tune.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S75 - sklearn Hyperparams: Ridge
    # -------------------------------------------------------------------
    def s75_ridge_params(self):
        banner = section_banner("sklearn Hyperparameters", "Ridge")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Ridge has one main hyperparameter: alpha (lambda).", wait=2.5)

        headers = ["Parameter", "Default", "Effect", "When to Change"]
        rows = [
            ["alpha",        "1.0",
             "L2 penalty. Higher = smaller coefficients.",
             "Always tune. Try logspace(-3,3,100)."],
            ["fit_intercept","True",
             "Same as LinearRegression.",
             "Leave True."],
            ["solver",       "'auto'",
             "svd: small, cholesky: medium, sag: large n.",
             "Use sag/saga for n > 100k."],
            ["tol",          "1e-4",
             "Convergence tolerance.",
             "Decrease for precision."],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, BLUE_H, LIGHT_GRAY, GREEN_H],
                         font_size=17)
        tbl.next_to(banner, DOWN, buff=0.35)
        tbl.set_width(13.5)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.45))
            self.wait(0.4)

        self.show_sub(
            "Always tune Ridge's alpha using RidgeCV or GridSearchCV.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S76 - sklearn Hyperparams: Lasso
    # -------------------------------------------------------------------
    def s76_lasso_params(self):
        banner = section_banner("sklearn Hyperparameters", "Lasso")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Lasso has alpha plus coordinate descent parameters.", wait=2.5)

        headers = ["Parameter", "Default", "Effect", "When to Change"]
        rows = [
            ["alpha",    "1.0",
             "L1 penalty. Higher = more zeros.",
             "Always tune. Use LassoCV for path search."],
            ["max_iter", "1000",
             "Max coordinate descent iterations.",
             "Increase to 10000 if ConvergenceWarning."],
            ["tol",      "1e-4",
             "Stop when dual gap < tol.",
             "Decrease for stricter convergence."],
            ["selection","'cyclic'",
             "cyclic: ordered. random: random order.",
             "random + higher max_iter for large datasets."],
            ["warm_start","False",
             "Reuse previous fit as starting point.",
             "True when scanning many alpha values."],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, BLUE_H, LIGHT_GRAY, GREEN_H],
                         font_size=16)
        tbl.next_to(banner, DOWN, buff=0.35)
        tbl.set_width(13.5)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.35)

        self.show_sub(
            "Increase max_iter if Lasso gives a ConvergenceWarning.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S77 - sklearn Hyperparams: ElasticNet
    # -------------------------------------------------------------------
    def s77_enet_params(self):
        banner = section_banner("sklearn Hyperparameters", "ElasticNet")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("ElasticNet has two hyperparameters: alpha and l1_ratio.", wait=2.5)

        headers = ["Parameter", "Default", "Effect", "Tip"]
        rows = [
            ["alpha",    "1.0",
             "Overall penalty strength.",
             "Try logspace(-3,2,50)."],
            ["l1_ratio", "0.5",
             "Mix: 0=Ridge, 1=Lasso.",
             "Try [0.1,0.3,0.5,0.7,0.9,1.0]."],
            ["max_iter", "1000",
             "Coordinate descent iterations.",
             "Increase to 10000 if warnings."],
            ["warm_start","False",
             "Reuse previous solution.",
             "True for regularisation path scanning."],
        ]
        tbl = make_table(headers, rows,
                         col_colors=[YELLOW_H, BLUE_H, LIGHT_GRAY, GREEN_H],
                         font_size=17)
        tbl.next_to(banner, DOWN, buff=0.35)
        tbl.set_width(13.5)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.45))
            self.wait(0.4)

        self.show_sub(
            "If l1_ratio approaches 1, just use Lasso. If it approaches 0, just use Ridge.",
            wait=3.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S78 - When to Use - Decision Table
    # -------------------------------------------------------------------
    def s78_when_to_use(self):
        banner = section_banner("When to Use What",
                                "Choosing the right model")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Here is a decision guide for choosing between models.", wait=2.5)

        headers = ["Situation", "Best Choice", "Why"]
        rows = [
            ["Interpretability required (banking, medical)",
             "Linear Regression",
             "Coefficients have direct interpretation"],
            ["Fast baseline needed",
             "Linear Regression",
             "Trains in milliseconds"],
            ["Strong non-linear relationships",
             "Gradient Boosting / NN",
             "Linear model will underfit"],
            ["Correlated features, no selection needed",
             "Ridge",
             "Distributes weight stably"],
            ["Many features, only a few matter",
             "Lasso",
             "Auto-zeros irrelevant features"],
            ["Correlated features + sparse model needed",
             "ElasticNet",
             "Handles groups better than Lasso"],
            ["Lots of outliers in y",
             "HuberRegressor",
             "Robust to outliers"],
            ["Massive dataset (millions of rows)",
             "SGDRegressor",
             "Mini-batch updates"],
        ]

        # 9 rows x row_h + banner ~1.4 must fit in 8-unit frame.
        # 9 x 0.42 = 3.78 + 1.4 banner + 0.5 buff + 0.55 subtitle = 6.23 -- safe.
        FS      = 13
        FS_HDR  = 15
        ROW_H   = 0.42
        COL_PAD = 0.30
        col_colors = [YELLOW_H, BLUE_H, GREEN_H]

        all_rows_data = [headers] + rows
        n_col = len(headers)
        col_w = [0.0] * n_col
        cell_texts = []
        for r_i, row in enumerate(all_rows_data):
            r_cells = []
            for c_i, cell in enumerate(row):
                fs  = FS_HDR if r_i == 0 else FS
                wt  = None  # weight param removed for Pango compatibility
                col = col_colors[c_i]
                t   = Text(str(cell), font_size=fs, color=col)
                col_w[c_i] = max(col_w[c_i], t.width)
                r_cells.append(t)
            cell_texts.append(r_cells)

        col_w   = [w + COL_PAD for w in col_w]
        total_w = sum(col_w)

        tbl = VGroup()
        for r_i, r_cells in enumerate(cell_texts):
            bg_col = CARD2_BG if r_i % 2 == 0 else CARD_BG
            row_bg = Rectangle(width=total_w, height=ROW_H,
                               fill_color=bg_col, fill_opacity=1,
                               stroke_opacity=0)
            row_bg.move_to(ORIGIN)
            left_x = -total_w / 2
            for c_i, cell_txt in enumerate(r_cells):
                cx = left_x + sum(col_w[:c_i]) + col_w[c_i] / 2
                cell_txt.move_to(row_bg.get_center() + RIGHT * cx)
                max_w = col_w[c_i] - 0.08
                if cell_txt.width > max_w:
                    cell_txt.set_width(max_w)
            tbl.add(VGroup(row_bg, *r_cells))

        tbl.arrange(DOWN, buff=0)
        if tbl.width > 13.5:
            tbl.set_width(13.5)
        tbl.next_to(banner, DOWN, buff=0.50)

        self.play(FadeIn(tbl[0], run_time=0.5))
        for row in tbl[1:]:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.3)

        self.show_sub(
            "Always start with plain linear regression as your baseline before trying complex models.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S79 - Full Overall Pros & Cons
    # -------------------------------------------------------------------
    def s79_full_pros_cons(self):
        pros = [
            "Coefficients directly state effect in real units",
            "OLS closed form " + EM + " fits in seconds",
            "No hyperparameters (base OLS)",
            "Statistical inference via p-values (statsmodels)",
            "Convex loss " + EM + " guaranteed global optimum",
            "Memory efficient " + EM + " stores only p+1 numbers",
            "Scales to huge data with SGDRegressor",
        ]
        cons = [
            "Cannot capture non-linear patterns without engineering",
            "MSE amplifies outliers heavily",
            "Unstable coefficients with multicollinearity",
            "Feature interactions must be added manually",
            "Strict assumptions for valid inference",
            "No automatic feature selection (OLS/Ridge)",
            "Performance ceiling for complex relationships",
        ]
        layout = make_pros_cons(pros, cons,
                                title="Overall Pros & Cons " + EM + " Final Summary",
                                font_size=18)
        self.play(FadeIn(layout[0], run_time=0.5))
        self.show_sub("Linear regression is fast, interpretable, and a mandatory baseline.", wait=3.0)
        self.play(FadeIn(layout[1], run_time=0.7))
        self.show_sub(
            "Its main limitations are the linearity assumption and sensitivity to outliers.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S80 - Interview Q&A Highlights
    # -------------------------------------------------------------------
    def s80_interview_qa(self):
        banner = section_banner("Tricky Interview Questions",
                                "Key answers to remember")
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Let us go through the most important interview questions.", wait=2.5)

        qas = [
            ("Q: Does linear regression assume the data is normally distributed?",
             "No! It assumes RESIDUALS are normal " + EM + " not the raw X or y data."),
            ("Q: Can R-squared be negative?",
             "Yes " + EM + " when SS_res > SS_tot, i.e., model is worse than predicting the mean."),
            ("Q: Does OLS need feature scaling?",
             "For predictions: No. For regularisation (Ridge/Lasso): Yes, mandatory."),
            ("Q: Why does Lasso produce sparsity but Ridge does not?",
             "L1 diamond has corners on axes " + EM + " MSE ellipse hits a corner = exact zero."),
            ("Q: Does GD always find the global minimum for linear regression?",
             "Yes " + EM + " MSE for linear regression is strictly convex (bowl-shaped)."),
            ("Q: What is the Gauss-Markov theorem?",
             "Under OLS assumptions, OLS is BLUE: Best Linear Unbiased Estimator."),
        ]

        cards = VGroup()
        for q_str, a_str in qas:
            bg = RoundedRectangle(
                width=12.5, height=1.05, corner_radius=0.12,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=BLUE_H, stroke_opacity=0.45, stroke_width=1.2
            )
            q_txt = Text(q_str, font_size=17, color=YELLOW_H)
            a_txt = Text(a_str, font_size=17, color=GREEN_H)
            q_txt.move_to(bg).shift(UP * 0.22).align_to(bg, LEFT).shift(RIGHT * 0.2)
            a_txt.move_to(bg).shift(DOWN * 0.2).align_to(bg, LEFT).shift(RIGHT * 0.2)
            cards.add(VGroup(bg, q_txt, a_txt))

        cards.arrange(DOWN, buff=0.08)
        cards.next_to(banner, DOWN, buff=0.25)
        cards.set_width(13.0)
        # Ensure cards don't run off bottom of frame
        if cards.get_bottom()[1] < -3.6:
            cards.scale_to_fit_height(6.2)
            cards.next_to(banner, DOWN, buff=0.2)

        for card in cards:
            self.play(FadeIn(card, shift=RIGHT * 0.1, run_time=0.4))
            self.wait(0.35)

        self.show_sub(
            "Memorise these answers. They come up in almost every data science interview.",
            wait=4.0
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S81 - Master Summary
    # -------------------------------------------------------------------
    def s81_summary(self):
        banner = section_banner("Master Summary",
                                "Everything you need to remember",
                                color=GREEN_H)
        self.play(FadeIn(banner, run_time=0.5))
        self.show_sub("Let us put it all together.", wait=2.0)

        # Each bullet: (label, content_mobject_or_string)
        def make_summary_row(label_str, content_mob):
            bg = RoundedRectangle(
                width=12.8, height=0.62, corner_radius=0.1,
                fill_color=CARD_BG, fill_opacity=1,
                stroke_color=GREEN_H, stroke_opacity=0.3, stroke_width=1
            )
            lbl = Text(label_str, font_size=16, color=GREEN_H)
            bg.move_to(ORIGIN)
            lbl.move_to(bg.get_left() + RIGHT * 0.2).align_to(bg, LEFT)
            lbl.shift(RIGHT * 0.18)
            content_mob.next_to(lbl, RIGHT, buff=0.18)
            max_cnt_w = 12.8 - lbl.width - 0.55
            if content_mob.width > max_cnt_w:
                content_mob.set_width(max_cnt_w)
            return VGroup(bg, lbl, content_mob)

        def txt(s, col=WHITE, fs=16):
            return Text(s, font_size=fs, color=col)

        def math_row(*parts):
            """Alternating Text/MathTex items arranged in a row."""
            mobs = []
            for p in parts:
                if p[0] == "$":
                    mobs.append(MathTex(p[1:], font_size=22, color=YELLOW_H))
                else:
                    mobs.append(Text(p, font_size=16, color=WHITE))
            grp = VGroup(*mobs)
            grp.arrange(RIGHT, buff=0.04)
            return grp

        rows = VGroup(
            make_summary_row("Equation:",
                math_row("$" + r"\hat{y} = X\beta",
                         ", minimises MSE = ",
                         "$\\tfrac{1}{n}\\|y - X\\beta\\|^2")),
            make_summary_row("Closed form:",
                math_row("$" + r"\beta = (X^{\top}X)^{-1}X^{\top}y",
                         EM + " sklearn uses SVD for stability")),
            make_summary_row("LINE-MO:",
                txt("Linearity, Independence, Normality, Equal Var, No Multi, No Outliers")),
            make_summary_row("Metrics:",
                math_row("RMSE (interpretable), MAE (robust), ",
                         r"$R^2", " (variance explained)")),
            make_summary_row("Regularisation:",
                txt("Ridge (L2, no zeros), Lasso (L1, exact zeros), ElasticNet (both)")),
            make_summary_row("Bias-Variance:",
                txt("Regularisation increases bias, reduces variance " + EM + " tune with CV")),
            make_summary_row("Pipeline:",
                txt("Always wrap preprocessing " + EM + " prevents data leakage")),
            make_summary_row("Diagnostics:",
                txt("Residuals vs Fitted, Q-Q, Scale-Location, Cook's D")),
            make_summary_row("Pros:",
                txt("Interpretable, fast, BLUE, no hyperparams, great baseline")),
            make_summary_row("Cons:",
                txt("Linearity assumption, outlier sensitivity, strict assumptions")),
        )

        rows.arrange(DOWN, buff=0.08)
        rows.next_to(banner, DOWN, buff=0.25)
        if rows.get_bottom()[1] < -3.6:
            rows.scale_to_fit_height(6.0)
            rows.next_to(banner, DOWN, buff=0.2)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.1, run_time=0.30))
            self.wait(0.12)

        self.show_sub(
            "You now have a complete understanding of linear regression from theory to production.",
            wait=4.5
        )
        self.clear_scene()

    # -------------------------------------------------------------------
    # S82 - End Card
    # -------------------------------------------------------------------
    def s82_end(self):
        title = Text("Linear Regression", font_size=58,
                     color=BLUE_H)
        sub = Text("Complete Guide", font_size=30, color=WHITE)
        cta = Text("Like " + MDOT + " Subscribe " + MDOT + " Comment below your questions",
                   font_size=22, color=YELLOW_H)
        stats = VGroup(
            Text("15 Sections  " + MDOT + "  All Pros & Cons  " + MDOT + "  Full sklearn Code  " + MDOT + "  12 Interview Q&As",
                 font_size=17, color=LIGHT_GRAY),
        )

        content = VGroup(title, sub, cta, stats)
        content.arrange(DOWN, buff=0.38)
        content.center()

        self.play(FadeIn(title, shift=UP * 0.3, run_time=1.0))
        self.play(FadeIn(sub, run_time=0.6))
        self.play(FadeIn(cta, run_time=0.6))
        self.play(FadeIn(stats, run_time=0.5))
        self.show_sub(
            "Thank you for watching! All code in the description. See you in the next video.",
            wait=5.0
        )
        self.hide_sub()
        self.wait(1.5)

    # ===================================================================
    # MAIN CONSTRUCT - calls all scenes in order
    # ===================================================================
    def construct(self):
        self.s01_title()
        self.s02_analogy()
        self.s03_scatter()
        self.s04_what_how_why_when()
        self.s05_simple_vs_multiple()
        self.s06_overall_pros_cons()
        self.s07_math_model()
        self.s08_symbol_table()
        self.s09_matrix_form()
        self.s10_error_term()
        self.s11_coeff_interp()
        self.s12_ols_cost()
        self.s13_why_square()
        self.s14_normal_eq()
        self.s15_normal_eq_pc()
        self.s16_linemo_overview()
        self.s17_linearity()
        self.s18_linearity_pc()
        self.s19_homoscedasticity()
        self.s20_homo_pc()
        self.s21_multicollinearity()
        self.s22_multi_pc()
        self.s23_independence()
        self.s24_independence_pc()
        self.s25_normality()
        self.s26_normality_pc()
        self.s27_outliers()
        self.s28_outliers_pc()
        self.s29_metrics_overview()
        self.s30_mse()
        self.s31_mse_pc()
        self.s32_rmse()
        self.s33_rmse_pc()
        self.s34_mae()
        self.s35_mae_pc()
        self.s36_r2()
        self.s37_r2_table()
        self.s38_r2_pc()
        self.s39_adj_r2()
        self.s40_adj_r2_pc()
        self.s41_mape()
        self.s42_mape_pc()
        self.s43_gd_why()
        self.s44_gd_update()
        self.s45_gd_steps()
        self.s46_learning_rate()
        self.s47_gd_types()
        self.s48_gd_pc()
        self.s49_reg_problem()
        self.s50_ridge()
        self.s51_ridge_pc()
        self.s52_lasso()
        self.s53_lasso_geometry()
        self.s54_lasso_pc()
        self.s55_elasticnet()
        self.s56_enet_pc()
        self.s57_reg_table()
        self.s58_diagnostics()
        self.s59_cooks()
        self.s60_diag_pc()
        self.s61_feat_eng()
        self.s62_interactions()
        self.s63_encoding()
        self.s64_scaling()
        self.s65_overfit()
        self.s66_bias_variance()
        self.s67_bv_curve()
        self.s68_bv_table()
        self.s69_cv_why()
        self.s70_cv_diagram()
        self.s71_cv_pc()
        self.s72_pipeline()
        self.s73_pipeline_pc()
        self.s74_lr_params()
        self.s75_ridge_params()
        self.s76_lasso_params()
        self.s77_enet_params()
        self.s78_when_to_use()
        self.s79_full_pros_cons()
        self.s80_interview_qa()
        self.s81_summary()
        self.s82_end()