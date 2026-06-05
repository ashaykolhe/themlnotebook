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
# ANIM 37 — Bias², Variance, Total Error curves draw in sequence
# ══════════════════════════════════════════════════════════════════════════════
class Anim37_BiasVarianceCurves(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Bias–Variance Tradeoff", font_size=28, color=HEADING)\
            .to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=8.5, y_length=4.8,
            axis_config={"color": "#444a5a", "stroke_width": 2}, tips=False,
        ).shift(DOWN * 0.55)
        xl = Text("Model Complexity →", font_size=18, color=MUTED)\
            .next_to(axes, DOWN, buff=0.25)
        yl = Text("Error", font_size=18, color=MUTED)\
            .next_to(axes, LEFT, buff=0.2).rotate(PI/2)
        self.play(Create(axes), Write(xl), Write(yl), run_time=0.8)

        def bias_sq(x):  return 8.5 * np.exp(-0.48 * x) + 0.3
        def variance(x): return 0.32 + 0.52 * x ** 1.4
        def total(x):    return bias_sq(x) + variance(x)

        xs = np.linspace(0.2, 9.8, 400)
        sweet_x = xs[np.argmin([total(x) for x in xs])]

        c_bias = axes.plot(bias_sq, x_range=[0.3, 9.8], color=BLUE_D,   stroke_width=3)
        c_var  = axes.plot(variance, x_range=[0.3, 9.8], color=ORANGE_L, stroke_width=3)
        c_tot  = axes.plot(total,   x_range=[0.3, 9.8], color=GREEN_G,  stroke_width=3.5)

        lbl_bias = Text("Bias²  (decreases with complexity)",
                        font_size=16, color=BLUE_D).to_corner(UR, buff=0.5).shift(DOWN * 0.3)
        lbl_var  = Text("Variance  (increases with complexity)",
                        font_size=16, color=ORANGE_L).next_to(lbl_bias, DOWN, buff=0.22, aligned_edge=LEFT)
        lbl_tot  = Text("Total Error  (U-shape — find the dip!)",
                        font_size=16, color=GREEN_G).next_to(lbl_var, DOWN, buff=0.22, aligned_edge=LEFT)

        for curve, lbl in [(c_bias, lbl_bias), (c_var, lbl_var), (c_tot, lbl_tot)]:
            self.play(Create(curve), run_time=1.1)
            self.play(FadeIn(lbl, shift=LEFT * 0.15), run_time=0.5)
            self.wait(0.4)

        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 38 — Sweet spot pulses + "Found by cross-validation" caption
# ══════════════════════════════════════════════════════════════════════════════
class Anim38_SweetSpotPulse(Scene):
    def construct(self):
        self.camera.background_color = BG

        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 10, 2],
            x_length=8.5, y_length=4.8,
            axis_config={"color": "#444a5a", "stroke_width": 2}, tips=False,
        ).shift(DOWN * 0.55)

        def bias_sq(x):  return 8.5 * np.exp(-0.48 * x) + 0.3
        def variance(x): return 0.32 + 0.52 * x ** 1.4
        def total(x):    return bias_sq(x) + variance(x)

        xs = np.linspace(0.2, 9.8, 400)
        sweet_x = xs[np.argmin([total(x) for x in xs])]
        sweet_y = total(sweet_x)

        c_bias = axes.plot(bias_sq, x_range=[0.3, 9.8], color=BLUE_D,   stroke_width=2.5)
        c_var  = axes.plot(variance, x_range=[0.3, 9.8], color=ORANGE_L, stroke_width=2.5)
        c_tot  = axes.plot(total,   x_range=[0.3, 9.8], color=GREEN_G,  stroke_width=3)
        self.add(axes, c_bias, c_var, c_tot)

        sweet_pt   = Dot(axes.c2p(sweet_x, sweet_y), color=YELLOW_R, radius=0.14)
        sweet_line = DashedLine(axes.c2p(sweet_x, 0),
                                axes.c2p(sweet_x, sweet_y),
                                color=YELLOW_R, stroke_width=1.8, dash_length=0.12)
        sweet_lbl  = Text("Sweet Spot\n(optimal complexity)",
                          font_size=17, color=YELLOW_R)\
            .next_to(axes.c2p(sweet_x, sweet_y), UP + RIGHT, buff=0.15)

        self.play(FadeIn(sweet_pt, scale=1.6), Create(sweet_line),
                  Write(sweet_lbl), run_time=0.9)

        # Pulse three times
        for _ in range(3):
            self.play(sweet_pt.animate.scale(1.8).set_color(WHITE), run_time=0.25)
            self.play(sweet_pt.animate.scale(1/1.8).set_color(YELLOW_R), run_time=0.25)

        caption = Text("Found by cross-validation — not intuition",
                       font_size=20, color=YELLOW_R).to_edge(DOWN, buff=0.4)
        self.play(Write(caption), run_time=0.9)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 39 — Data bar splits into 5 folds, each fold takes turn as test set
# ══════════════════════════════════════════════════════════════════════════════
class Anim39_CVFolds(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("5-Fold Cross-Validation", font_size=28, color=HEADING)\
            .to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        n = 5
        bw, bh, gap = 1.6, 0.7, 0.06
        total_w = n * bw + (n-1) * gap

        fold_labels = VGroup(*[
            Text(f"Fold {i+1}", font_size=17, color=MUTED)
            .move_to([-total_w/2 - 0.85, 1.5 - i * 1.2, 0])
            for i in range(n)
        ])
        self.play(FadeIn(fold_labels), run_time=0.4)

        score_strs = ["R² = 0.83", "R² = 0.85", "R² = 0.81", "R² = 0.86", "R² = 0.84"]

        for fold_idx in range(n):
            row_y = 1.5 - fold_idx * 1.2
            row = VGroup()
            for j in range(n):
                x_pos = -total_w/2 + j*(bw+gap) + bw/2
                color   = ORANGE_L if j == fold_idx else BLUE_D
                opacity = 0.9     if j == fold_idx else 0.35
                rect = Rectangle(width=bw, height=bh,
                                  fill_color=color, fill_opacity=opacity,
                                  stroke_width=0).move_to([x_pos, row_y, 0])
                lbl_txt = "TEST" if j == fold_idx else "train"
                lbl_clr = WHITE  if j == fold_idx else "#3a4050"
                lbl = Text(lbl_txt, font_size=11, color=lbl_clr)\
                    .move_to(rect.get_center())
                row.add(VGroup(rect, lbl))

            score = Text(score_strs[fold_idx], font_size=16, color=GREEN_G)\
                .move_to([total_w/2 + 1.15, row_y, 0])

            self.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.45)
            self.play(FadeIn(score, shift=LEFT * 0.1), run_time=0.3)

        # Legend and average
        self.wait(0.3)
        avg_line = Line(LEFT*5, RIGHT*5, color="#252a38", stroke_width=1)\
            .to_edge(DOWN, buff=0.75)
        avg_text = Text(
            "Final CV R² = avg(0.83, 0.85, 0.81, 0.86, 0.84) = 0.838",
            font_size=17, color=YELLOW_R
        ).next_to(avg_line, DOWN, buff=0.2)
        self.play(Create(avg_line), Write(avg_text), run_time=0.9)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 40 — Wrong approach: red arrow shows test data leaking into scaler
# ══════════════════════════════════════════════════════════════════════════════
class Anim40_DataLeakage(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("❌ WRONG — Data Leakage", font_size=26, color=RED_B)\
            .to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        def box(label, color, w=2.6, h=0.85):
            bg   = RoundedRectangle(corner_radius=0.12, width=w, height=h,
                                     fill_color=color, fill_opacity=0.12,
                                     stroke_color=color, stroke_width=2)
            txt  = Text(label, font_size=17, color=color)
            return VGroup(bg, txt)

        full_data  = box("Full Dataset\n(train + test)", RED_B, w=2.5)
        scaler     = box("StandardScaler\n.fit_transform(X)", RED_B, w=2.8)
        split      = box("train_test_split", RED_B, w=2.4)
        model      = box("Model\n.fit(X_train)", RED_B, w=2.2)

        flow = VGroup(full_data, scaler, split, model)\
            .arrange(RIGHT, buff=0.6).move_to(UP * 0.8)

        arrows = VGroup(*[
            Arrow(flow[i].get_right(), flow[i+1].get_left(),
                  buff=0.08, color=RED_B, stroke_width=2.2,
                  max_tip_length_to_length_ratio=0.2)
            for i in range(3)
        ])

        self.play(
            LaggedStart(*[FadeIn(b, shift=RIGHT*0.15) for b in flow],
                        lag_ratio=0.15, run_time=1.1)
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15, run_time=0.7)
        )

        # Leakage back-arrow from split to scaler
        leak_path = VMobject()
        leak_path.set_points_as_corners([
            split.get_bottom() + DOWN * 0.05,
            split.get_bottom() + DOWN * 0.55,
            scaler.get_bottom() + DOWN * 0.55,
            scaler.get_bottom() + DOWN * 0.05,
        ])
        leak_path.set_color(YELLOW_R).set_stroke(width=2.2)
        leak_arr  = Arrow(scaler.get_bottom() + DOWN * 0.55,
                          scaler.get_bottom() + DOWN * 0.05,
                          buff=0.03, color=YELLOW_R, stroke_width=2.2,
                          max_tip_length_to_length_ratio=0.25)
        leak_text = Text("⚠  Test statistics contaminate the scaler!",
                         font_size=18, color=YELLOW_R)\
            .next_to(leak_path, DOWN, buff=0.18)

        self.play(Create(leak_path), GrowArrow(leak_arr), run_time=0.8)
        self.play(FadeIn(leak_text, shift=UP*0.1), run_time=0.6)

        consequence = Text(
            "Result: inflated metrics — model looks better than it really is",
            font_size=18, color=RED_B
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(consequence), run_time=0.8)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 41 — Correct approach: Pipeline shown in green
# ══════════════════════════════════════════════════════════════════════════════
class Anim41_CorrectPipeline(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("✅ CORRECT — sklearn Pipeline Prevents Leakage",
                     font_size=22, color=GREEN_G).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.7)

        def box(label, color, w=2.6, h=0.85):
            bg  = RoundedRectangle(corner_radius=0.12, width=w, height=h,
                                    fill_color=color, fill_opacity=0.12,
                                    stroke_color=color, stroke_width=2)
            txt = Text(label, font_size=17, color=color)
            return VGroup(bg, txt)

        train = box("X_train\ny_train", GREEN_G, w=1.9)
        pipe  = box("Pipeline\n[Scaler → Model]", GREEN_G, w=2.8)
        test  = box("X_test", GREEN_G, w=1.7)
        pred  = box("predict(X_test)\n(uses train stats)", GREEN_G, w=2.8)

        flow = VGroup(train, pipe, test, pred)\
            .arrange(RIGHT, buff=0.6).move_to(UP * 0.5)

        arrows = VGroup(*[
            Arrow(flow[i].get_right(), flow[i+1].get_left(),
                  buff=0.08, color=GREEN_G, stroke_width=2.2,
                  max_tip_length_to_length_ratio=0.2)
            for i in range(3)
        ])

        self.play(
            LaggedStart(*[FadeIn(b, shift=RIGHT*0.15) for b in flow],
                        lag_ratio=0.15, run_time=1.1)
        )
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15, run_time=0.7)
        )

        # Annotation under the pipe box
        note = Text(
            "Scaler.fit() only sees X_train\nScaler.transform() applied to X_test with train stats",
            font_size=16, color=GREEN_G
        ).next_to(pipe, DOWN, buff=0.4)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 42 — Pipeline diagram: [StandardScaler → LinearRegression] in a box
# ══════════════════════════════════════════════════════════════════════════════
class Anim42_PipelineDiagram(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("sklearn Pipeline — One Object, No Leakage",
                     font_size=24, color=HEADING).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        # Outer pipeline box
        outer = RoundedRectangle(corner_radius=0.2, width=9.5, height=2.8,
                                  fill_color="#0a0f14", fill_opacity=1,
                                  stroke_color=GREEN_G, stroke_width=2.5)\
            .move_to(DOWN * 0.2)
        pipe_lbl = Text("Pipeline", font_size=20, color=GREEN_G, weight=BOLD)\
            .next_to(outer.get_top(), DOWN, buff=0.22)

        # Inner steps
        scaler_box = RoundedRectangle(corner_radius=0.12, width=3.0, height=1.35,
                                       fill_color=BLUE_D, fill_opacity=0.15,
                                       stroke_color=BLUE_D, stroke_width=2)\
            .move_to(LEFT * 2.5 + DOWN * 0.2)
        scaler_lbl = Text("StandardScaler\n('scaler')", font_size=17, color=BLUE_D)\
            .move_to(scaler_box.get_center())

        inner_arr = Arrow(scaler_box.get_right(), scaler_box.get_right() + RIGHT * 1.4,
                          buff=0.05, color=MUTED, stroke_width=2,
                          max_tip_length_to_length_ratio=0.25)

        model_box = RoundedRectangle(corner_radius=0.12, width=3.0, height=1.35,
                                      fill_color=ORANGE_L, fill_opacity=0.15,
                                      stroke_color=ORANGE_L, stroke_width=2)\
            .move_to(RIGHT * 2.5 + DOWN * 0.2)
        model_lbl = Text("LinearRegression\n('model')", font_size=17, color=ORANGE_L)\
            .move_to(model_box.get_center())

        # Input / output arrows
        in_arr = Arrow(outer.get_left() + LEFT * 1.2, outer.get_left(),
                       buff=0.05, color=GREEN_G, stroke_width=2.2,
                       max_tip_length_to_length_ratio=0.2)
        in_lbl = Text("X_train, y_train", font_size=14, color=GREEN_G)\
            .next_to(in_arr, UP, buff=0.1)

        out_arr = Arrow(outer.get_right(), outer.get_right() + RIGHT * 1.2,
                        buff=0.05, color=GREEN_G, stroke_width=2.2,
                        max_tip_length_to_length_ratio=0.2)
        out_lbl = Text("ŷ predictions", font_size=14, color=GREEN_G)\
            .next_to(out_arr, UP, buff=0.1)

        self.play(Create(outer), Write(pipe_lbl), run_time=0.6)
        self.play(
            FadeIn(scaler_box), Write(scaler_lbl),
            GrowArrow(inner_arr),
            FadeIn(model_box), Write(model_lbl),
            run_time=0.9
        )
        self.play(
            GrowArrow(in_arr), FadeIn(in_lbl),
            GrowArrow(out_arr), FadeIn(out_lbl),
            run_time=0.7
        )

        # One-liner code hint
        code = Text(
            'pipeline = Pipeline([\n'
            '    ("scaler", StandardScaler()),  ("model", LinearRegression())])',
            font_size=13, color=YELLOW_R, font="Courier New"
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(code), run_time=1.0)
        self.wait(2.0)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 43 — Outro: summary screen with all major concepts as labelled icons
# ══════════════════════════════════════════════════════════════════════════════
class Anim43_OutroSummary(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("What You Now Know", font_size=32, color=HEADING)\
            .to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.7)

        concepts = [
            ("📈", "Best-fit line\nminimises MSE",   BLUE_D,    LEFT*4.2  + UP*1.5),
            ("🔢", "ŷ = β₀ + β₁x₁+…\nEquation",     ORANGE_L,  LEFT*1.4  + UP*1.5),
            ("🥣", "Cost bowl\nconvex — 1 min",      GREEN_G,   RIGHT*1.4 + UP*1.5),
            ("📉", "Gradient descent\nfinds min",     YELLOW_R,  RIGHT*4.2 + UP*1.5),
            ("✅", "LINE-MO\n6 assumptions",           PURPLE,    LEFT*4.2  + DOWN*1.0),
            ("📏", "MAE/RMSE/R²\nmetrics",            BLUE_D,    LEFT*1.4  + DOWN*1.0),
            ("🔷", "Ridge & Lasso\nregularisation",   ORANGE_L,  RIGHT*1.4 + DOWN*1.0),
            ("🔁", "Pipeline +\nCross-validation",    GREEN_G,   RIGHT*4.2 + DOWN*1.0),
        ]

        cards = VGroup()
        for emoji, text, color, pos in concepts:
            icon = Text(emoji, font_size=26)
            lbl  = Text(text, font_size=15, color=color)
            bg   = RoundedRectangle(corner_radius=0.15, width=2.4, height=1.55,
                                     fill_color="#13161e", fill_opacity=1,
                                     stroke_color=color, stroke_width=1.5)
            content = VGroup(icon, lbl).arrange(DOWN, buff=0.1)
            # Scale content to fit inside card if needed
            if content.width > 2.1:
                content.scale(2.1 / content.width)
            grp  = VGroup(bg, content).move_to(pos)
            cards.add(grp)

        self.play(
            LaggedStart(*[FadeIn(c, scale=0.8) for c in cards],
                        lag_ratio=0.12, run_time=2.2)
        )
        self.wait(1.0)

        # All cards glow
        self.play(
            *[c[0].animate.set_stroke(color=WHITE, width=2.5) for c in cards],
            run_time=0.35
        )
        self.play(
            *[c[0].animate.set_stroke(
                color=concepts[i][2], width=1.5)
              for i, c in enumerate(cards)],
            run_time=0.35
        )
        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 44 — Screen fades to channel logo / end card
# ══════════════════════════════════════════════════════════════════════════════
class Anim44_EndCard(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Fade everything to black with a subscribe nudge
        circle = Circle(radius=1.7, fill_color="#1a1e2a",
                        fill_opacity=1, stroke_color=BLUE_D, stroke_width=3)
        channel_lbl = Text("The ML Notebook", font_size=24,
                           color=HEADING, weight=BOLD).move_to(circle.get_center())
        logo = VGroup(circle, channel_lbl)

        subscribe_btn = RoundedRectangle(corner_radius=0.2, width=3.2, height=0.75,
                                          fill_color=RED_B, fill_opacity=1,
                                          stroke_width=0)\
            .next_to(logo, DOWN, buff=0.5)
        sub_text = Text("SUBSCRIBE", font_size=22, color=WHITE, weight=BOLD)\
            .move_to(subscribe_btn.get_center())
        subscribe = VGroup(subscribe_btn, sub_text)

        thanks = Text("Thanks for watching!", font_size=26, color=MUTED)\
            .next_to(subscribe, DOWN, buff=0.5)

        self.play(FadeIn(logo, scale=0.8), run_time=0.9)
        self.play(FadeIn(subscribe, scale=0.9), run_time=0.6)
        self.play(Write(thanks), run_time=0.8)
        self.wait(1.5)

        # Final fade to black
        black = Rectangle(width=20, height=20, fill_color=BLACK,
                          fill_opacity=0, stroke_width=0)
        self.add(black)
        self.play(black.animate.set_fill(opacity=1), run_time=1.5)
        self.wait(0.5)
