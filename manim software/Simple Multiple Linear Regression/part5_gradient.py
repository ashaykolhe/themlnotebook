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
# ANIM 18 — Hilly landscape with a blindfolded figure on the hillside
# ══════════════════════════════════════════════════════════════════════════════
class Anim18_HillyLandscape(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Draw a hilly terrain using a curve
        axes = Axes(
            x_range=[0, 10, 2], y_range=[0, 6, 2],
            x_length=10, y_length=5,
            axis_config={"color": "#222730", "stroke_width": 1.5}, tips=False,
        ).shift(DOWN * 0.8)

        # Multi-hill landscape for a neural network (contrast later)
        def landscape(x):
            return (2.2 + 1.4 * np.sin(x * 0.9 + 0.5)
                    + 0.7 * np.cos(x * 2.1)
                    + 0.3 * np.sin(x * 3.5))

        terrain = axes.plot(landscape, x_range=[0.1, 9.9],
                            color="#4a5568", stroke_width=2.5)
        # Fill under the terrain
        terrain_fill = axes.get_area(terrain, x_range=[0.1, 9.9],
                                     color="#1e2433", opacity=0.7)

        self.play(Create(terrain_fill), Create(terrain), run_time=1.2)

        # Person represented as a simple stick figure at x=7.5 (on a hill)
        px = 7.5
        py = landscape(px)
        pos = axes.c2p(px, py)

        head = Circle(radius=0.18, color=YELLOW_R, fill_opacity=0.9,
                      fill_color=YELLOW_R).move_to(pos + UP * 0.55)
        body = Line(pos + UP * 0.37, pos + DOWN * 0.18,
                    color=YELLOW_R, stroke_width=3)
        left_arm  = Line(pos + UP * 0.15, pos + LEFT * 0.28 + DOWN * 0.05,
                         color=YELLOW_R, stroke_width=2.5)
        right_arm = Line(pos + UP * 0.15, pos + RIGHT * 0.28 + DOWN * 0.05,
                         color=YELLOW_R, stroke_width=2.5)
        left_leg  = Line(pos + DOWN * 0.18, pos + LEFT * 0.2 + DOWN * 0.45,
                         color=YELLOW_R, stroke_width=2.5)
        right_leg = Line(pos + DOWN * 0.18, pos + RIGHT * 0.2 + DOWN * 0.45,
                         color=YELLOW_R, stroke_width=2.5)
        blindfold = Line(pos + UP * 0.48, pos + UP * 0.62,
                         color=RED_B, stroke_width=4)
        figure = VGroup(head, body, left_arm, right_arm,
                        left_leg, right_leg, blindfold)

        self.play(FadeIn(figure, scale=0.8), run_time=0.7)

        # Downhill arrow
        target_x = 5.0
        target_y = landscape(target_x)
        down_arr = Arrow(
            axes.c2p(px, py + 0.5),
            axes.c2p(target_x, target_y + 0.5),
            color=GREEN_G, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.18
        )
        self.play(GrowArrow(down_arr), run_time=0.8)

        caption = Text("Analogy: \"Feel which way is downhill. Step. Repeat.\"",
                       font_size=20, color=MUTED).to_edge(UP, buff=0.4)
        self.play(Write(caption), run_time=0.9)
        self.wait(1.2)

        # KEY CORRECTION: show that linear regression has only ONE valley — no local traps
        contrast_label = Text(
            "⚠  But this landscape has LOCAL MINIMA — gradient descent could get stuck!",
            font_size=18, color=RED_B
        ).to_edge(DOWN, buff=0.65)
        self.play(Write(contrast_label), run_time=0.8)
        self.wait(0.5)

        correction = Text(
            "For linear regression: MSE is CONVEX → only ONE valley → always finds global min",
            font_size=18, color=GREEN_G
        ).next_to(contrast_label, UP, buff=0.25)
        self.play(Write(correction), run_time=0.9)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 19 — Figure fades → cost bowl reappears → ball steps down with labels
# ══════════════════════════════════════════════════════════════════════════════
class Anim19_GradientSteps(Scene):
    def construct(self):
        self.camera.background_color = BG

        axes = Axes(
            x_range=[-3.2, 3.2, 1], y_range=[0, 10, 2],
            x_length=8.5, y_length=5.2,
            axis_config={"color": "#444a5a", "stroke_width": 2}, tips=False,
        ).shift(DOWN * 0.6)
        xl = Text("β₁", font_size=20, color=MUTED).next_to(axes, DOWN, buff=0.2)
        yl = Text("MSE", font_size=20, color=MUTED).next_to(axes, LEFT, buff=0.15).rotate(PI/2)

        bowl = axes.plot(lambda x: x**2 + 0.4, x_range=[-3.0, 3.0],
                         color=BLUE_D, stroke_width=3.2)
        self.play(FadeIn(axes), Write(xl), Write(yl), Create(bowl), run_time=1.0)

        # Step positions along the parabola
        step_xs = [-2.8, -2.0, -1.3, -0.7, -0.2, 0.0]
        step_dots = [
            Dot(axes.c2p(x, x**2 + 0.4), color=YELLOW_R, radius=0.12)
            for x in step_xs
        ]
        step_labels_text = [
            "Start", "Step 1", "Step 2", "Step 3", "Step 4", "Converged ✓"
        ]

        update_eq = MathTex(
            r"\beta \leftarrow \beta - \alpha \cdot \frac{\partial \text{MSE}}{\partial \beta}",
            font_size=36, color=YELLOW_R
        ).to_edge(UP, buff=0.4)
        self.play(Write(update_eq), run_time=0.9)

        prev_dot = None
        for i, (x, dot, lbl_text) in enumerate(
                zip(step_xs, step_dots, step_labels_text)):
            color = ORANGE_L if i == len(step_xs) - 1 else YELLOW_R
            dot.set_color(color)
            lbl = Text(lbl_text, font_size=14, color=color)\
                .next_to(dot, UP + RIGHT, buff=0.08)

            if prev_dot is not None:
                arrow = Arrow(
                    prev_dot.get_center(), dot.get_center(),
                    buff=0.12, color=GREEN_G, stroke_width=2,
                    max_tip_length_to_length_ratio=0.22
                )
                self.play(GrowArrow(arrow), FadeIn(dot, scale=1.3),
                          FadeIn(lbl), run_time=0.55)
            else:
                self.play(FadeIn(dot, scale=1.3), FadeIn(lbl), run_time=0.55)
            prev_dot = dot
            self.wait(0.2)

        self.wait(1.5)


# ══════════════════════════════════════════════════════════════════════════════
# ANIM 20 — Three learning rate curves: optimal, too-high, too-low
# ══════════════════════════════════════════════════════════════════════════════
class Anim20_LearningRateCurves(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Effect of Learning Rate α", font_size=28, color=HEADING)\
            .to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.6)

        axes = Axes(
            x_range=[0, 50, 10], y_range=[0, 10, 2],
            x_length=9, y_length=4.8,
            axis_config={"color": "#444a5a", "stroke_width": 2}, tips=False,
        ).shift(DOWN * 0.5)
        xl = Text("Iterations →", font_size=19, color=MUTED).next_to(axes, DOWN, buff=0.25)
        yl = Text("Cost (MSE)", font_size=19, color=MUTED).next_to(axes, LEFT, buff=0.2).rotate(PI/2)
        self.play(Create(axes), Write(xl), Write(yl), run_time=0.8)

        def optimal(t):  return 0.5 + 8.5 * np.exp(-0.12 * t)
        def too_high(t): return 5 + 4 * np.exp(-0.03 * t) * np.cos(0.6 * t)
        def too_low(t):  return 1.5 + 7.5 * np.exp(-0.018 * t)

        curves_data = [
            (optimal,  GREEN_G,  "Optimal α  →  smooth convergence",    UR),
            (too_high, RED_B,    "Too high α  →  oscillates / diverges", UR),
            (too_low,  YELLOW_R, "Too low α  →  painfully slow",         UR),
        ]

        label_anchor = axes.c2p(49, 9.5)   # top-right area
        label_y_offset = 0

        for fn, color, text, _ in curves_data:
            curve = axes.plot(fn, x_range=[0, 49], color=color, stroke_width=2.8)
            lbl = Text(text, font_size=17, color=color)\
                .move_to(label_anchor + DOWN * label_y_offset)\
                .align_to(axes.c2p(26, 0), LEFT)
            self.play(Create(curve), run_time=1.3)
            self.play(FadeIn(lbl, shift=LEFT * 0.2), run_time=0.5)
            self.wait(0.5)
            label_y_offset += 0.55

        self.wait(1.5)
