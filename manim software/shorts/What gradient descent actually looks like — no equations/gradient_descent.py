"""
Gradient Descent - YouTube Short (9:16 vertical, 1080x1920)
All scenes are composited in GradientDescentShort.

Colour palette (project standard):
  Blue   #4f9eff   Orange #f97316   Green  #10b981
  Yellow #fbbf24   Red    #f87171   Purple #a855f7
  BG     #0d0f14

Render command (Windows-safe):
  manim -pqh gradient_descent.py GradientDescentShort --pixel_width 1080 --pixel_height 1920
"""

from manim import *
import numpy as np

# ── Palette ──────────────────────────────────────────────────────────────────
BG      = "#0d0f14"
BLUE    = "#4f9eff"
ORANGE  = "#f97316"
GREEN   = "#10b981"
YELLOW  = "#fbbf24"
RED     = "#f87171"
PURPLE  = "#a855f7"
WHITE   = "#ffffff"
GREY    = "#8899aa"

# ── Loss function (2-D cross-section shown as a curve) ───────────────────────
def loss(x):
    """Bumpy convex-ish curve with one local min and one global min."""
    return 0.4 * x**2 + 0.6 * np.sin(2.5 * x) + 0.3 * np.cos(5 * x) + 1.2

def loss_deriv(x):
    return 0.8 * x + 1.5 * np.cos(2.5 * x) - 1.5 * np.sin(5 * x)

# ── Shared axes factory ───────────────────────────────────────────────────────
def make_axes():
    ax = Axes(
        x_range=[-3.5, 3.5, 1],
        y_range=[0, 4.5, 1],
        x_length=7,
        y_length=4,
        axis_config={"color": GREY, "stroke_width": 1.5,
                     "include_ticks": False, "include_tip": True,
                     "tip_length": 0.15},
    )
    x_lbl = Text("Model parameters", font_size=18, color=GREY).next_to(ax.x_axis, DOWN, buff=0.15)
    y_lbl = Text("Loss (error)", font_size=18, color=GREY).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.15)
    return ax, x_lbl, y_lbl

def make_curve(ax):
    return ax.plot(loss, x_range=[-3.2, 3.2], color=BLUE, stroke_width=3)

# ── Single Scene — all segments inlined ──────────────────────────────────────
class GradientDescentShort(Scene):
    """
    Single flat Scene — all 8 segments run inside one construct().
    Render:
      manim -pqh gradient_descent.py GradientDescentShort --pixel_width 1080 --pixel_height 1920

    Preview individual segments by commenting out the self._segNN() calls below.
    """

    def construct(self):
        self.camera.background_color = BG
        self._seg01_hook()
        self._seg02_loss_surface()
        self._seg03_ball_rolling()
        self._seg04_labelled_surface()
        self._seg05_gradient_label()
        self._seg06_learning_rate()
        self._seg07_local_minima()
        self._seg08_outro()

    # ── Seg 01 — Hook Title ───────────────────────────────────────────────────
    def _seg01_hook(self):
        line1 = Text("Every AI you've ever used", font_size=36, color=WHITE)
        line2 = Text("was trained with", font_size=36, color=WHITE)
        line3 = Text("one trick.", font_size=52, color=YELLOW, weight=BOLD)
        stack = VGroup(line1, line2, line3).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(line1), run_time=0.6)
        self.play(FadeIn(line2), run_time=0.5)
        self.play(Write(line3), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(stack), run_time=0.4)

    # ── Seg 02 — Loss Surface intro ───────────────────────────────────────────
    def _seg02_loss_surface(self):
        ax, x_lbl, y_lbl = make_axes()
        curve = make_curve(ax)
        group = VGroup(ax, x_lbl, y_lbl, curve).scale(0.88).move_to(ORIGIN + DOWN * 0.3)

        caption = Text("This is a loss surface.", font_size=30, color=WHITE)\
            .to_edge(UP, buff=0.5)
        sub = Text("Height = how wrong your model is.", font_size=24, color=GREY)\
            .next_to(caption, DOWN, buff=0.2)

        self.play(Create(ax), Write(x_lbl), Write(y_lbl), run_time=1.0)
        self.play(Create(curve), run_time=1.0)
        self.play(Write(caption), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(VGroup(caption, sub, group)), run_time=0.4)

    # ── Seg 03 — Ball rolling down ────────────────────────────────────────────
    def _seg03_ball_rolling(self):
        ax, x_lbl, y_lbl = make_axes()
        curve = make_curve(ax)
        group = VGroup(ax, x_lbl, y_lbl, curve).scale(0.88).move_to(ORIGIN + DOWN * 0.3)
        self.add(group)

        # Gradient descent: start=-2.5, lr=0.05 gives clear downhill traverse
        # Loss drops 4.0 -> 0.45 over a span of ~1.9 x-units (verified)
        x_val = -2.5
        lr = 0.05
        x_positions = [x_val]
        for _ in range(120):
            x_val -= lr * loss_deriv(x_val)
            x_val = float(np.clip(x_val, -3.2, 3.2))
            x_positions.append(x_val)
        x_arr = np.array(x_positions)

        # Dense smooth path: 300 evenly-spaced alphas interpolated from the 121 steps
        alphas = np.linspace(0, 1, 300)
        step_alphas = np.linspace(0, 1, len(x_arr))
        x_smooth = np.interp(alphas, step_alphas, x_arr)
        path_points = [ax.c2p(float(x), float(loss(x))) for x in x_smooth]
        n_points = len(path_points)  # 300

        ball = Dot(radius=0.14, color=ORANGE).move_to(path_points[0])
        trail = VMobject(stroke_color=ORANGE, stroke_width=2.5, stroke_opacity=0.55)
        trail.set_points_as_corners([path_points[0], path_points[0]])

        caption = Text("Take a step downhill.\nThen another.\nThen another.",
                       font_size=28, color=WHITE, line_spacing=1.3)\
            .to_edge(UP, buff=0.4)

        self.play(FadeIn(ball), run_time=0.3)
        self.play(Write(caption), run_time=0.6)
        self.add(trail)

        t = ValueTracker(0.0)

        def update_ball(mob):
            idx = min(int(t.get_value() * (n_points - 1)), n_points - 1)
            mob.move_to(path_points[idx])

        def update_trail(mob):
            idx = min(int(t.get_value() * (n_points - 1)), n_points - 1)
            pts = path_points[:idx + 1]
            if len(pts) >= 2:
                mob.set_points_as_corners(pts)

        ball.add_updater(update_ball)
        trail.add_updater(update_trail)

        self.play(t.animate.set_value(1.0), run_time=3.5, rate_func=linear)

        ball.remove_updater(update_ball)
        trail.remove_updater(update_trail)

        self.wait(0.8)
        self.play(FadeOut(VGroup(caption, ball, trail, group)), run_time=0.4)

    # ── Seg 04 — Labelled surface ─────────────────────────────────────────────
    def _seg04_labelled_surface(self):
        ax, x_lbl, y_lbl = make_axes()
        curve = make_curve(ax)
        group = VGroup(ax, x_lbl, y_lbl, curve).scale(0.88).move_to(ORIGIN + DOWN * 0.3)
        self.add(group)

        # Global minimum verified: x=-0.5866, loss=0.4474
        gmin_x = -0.5866
        gmin_pt = ax.c2p(gmin_x, loss(gmin_x))
        star = Star(n=5, outer_radius=0.18, color=GREEN, fill_opacity=1)\
            .move_to(gmin_pt + UP * 0.25)
        star_lbl = Text("Global minimum\n(most accurate model)", font_size=20,
                        color=GREEN, line_spacing=1.2).next_to(star, RIGHT, buff=0.2)

        surf_lbl = Text("Loss Surface", font_size=26, color=BLUE)\
            .move_to(ax.c2p(-2.0, 3.8))
        arrow = Arrow(surf_lbl.get_bottom(), ax.c2p(-2.5, loss(-2.5)),
                      buff=0.05, color=BLUE, stroke_width=2,
                      max_tip_length_to_length_ratio=0.15)

        self.play(FadeIn(surf_lbl), Create(arrow), run_time=0.7)
        self.play(FadeIn(star), Write(star_lbl), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(VGroup(surf_lbl, arrow, star, star_lbl, group)), run_time=0.4)

    # ── Seg 05 — Gradient label + slope arrow ────────────────────────────────
    def _seg05_gradient_label(self):
        ax, x_lbl, y_lbl = make_axes()
        curve = make_curve(ax)
        group = VGroup(ax, x_lbl, y_lbl, curve).scale(0.88).move_to(ORIGIN + DOWN * 0.3)
        self.add(group)

        px = -2.2
        py = loss(px)
        slope = loss_deriv(px)
        dx = 0.7
        slope_arrow = Arrow(
            ax.c2p(px - dx, py - slope * dx),
            ax.c2p(px + dx, py + slope * dx),
            buff=0, color=YELLOW, stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )
        slope_lbl = Text("gradient\n(slope)", font_size=22, color=YELLOW, line_spacing=1.2)\
            .next_to(slope_arrow, UP, buff=0.15)

        title = Text("Gradient Descent", font_size=40, color=WHITE, weight=BOLD)\
            .to_edge(UP, buff=0.4)
        sub = Text("Follow the slope. Go down.", font_size=26, color=GREY)\
            .next_to(title, DOWN, buff=0.2)

        self.play(Write(title), run_time=0.6)
        self.play(FadeIn(sub), run_time=0.4)
        self.play(Create(slope_arrow), Write(slope_lbl), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(VGroup(title, sub, slope_arrow, slope_lbl, group)), run_time=0.4)

    # ── Seg 06 — Learning rate comparison ────────────────────────────────────
    def _seg06_learning_rate(self):
        caption = Text("The step size = learning rate", font_size=30, color=WHITE)\
            .to_edge(UP, buff=0.45)
        self.play(Write(caption), run_time=0.6)

        # ── LEFT chart: too-large lr — bouncing overshoot dots + arrows ──────
        ax_l, _, _ = make_axes()
        curve_l = make_curve(ax_l)
        gl = VGroup(ax_l, curve_l).scale(0.42).to_edge(LEFT, buff=0.3).shift(DOWN * 0.6)
        lbl_l = Text("Too large", font_size=22, color=RED).next_to(gl, UP, buff=0.1)

        big_x_vals = [-2.5, 2.2, -1.8, 1.4, -0.9]
        big_dots = VGroup(*[
            Dot(radius=0.1, color=RED).move_to(ax_l.c2p(x, loss(x)))
            for x in big_x_vals
        ])
        big_arrows = VGroup()
        for i in range(len(big_x_vals) - 1):
            big_arrows.add(Arrow(
                ax_l.c2p(big_x_vals[i], loss(big_x_vals[i])),
                ax_l.c2p(big_x_vals[i+1], loss(big_x_vals[i+1])),
                buff=0.05, color=RED, stroke_width=2,
                max_tip_length_to_length_ratio=0.2,
            ))

        # ── RIGHT chart: just-right lr — smooth rolling ball ─────────────────
        ax_r, _, _ = make_axes()
        curve_r = make_curve(ax_r)
        gr = VGroup(ax_r, curve_r).scale(0.42).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.6)
        lbl_r = Text("Just right", font_size=22, color=GREEN).next_to(gr, UP, buff=0.1)

        # start=3.0, lr=0.05: span=1.24, smooth convergence (verified)
        x_val = 3.0
        lr_sm = 0.05
        x_positions = [x_val]
        for _ in range(60):
            x_val -= lr_sm * loss_deriv(x_val)
            x_val = float(np.clip(x_val, -3.2, 3.2))
            x_positions.append(x_val)
        x_arr = np.array(x_positions)
        alphas     = np.linspace(0, 1, 200)
        step_alpha = np.linspace(0, 1, len(x_arr))
        x_smooth   = np.interp(alphas, step_alpha, x_arr)
        r_pts = [ax_r.c2p(float(x), float(loss(x))) for x in x_smooth]
        n_r   = len(r_pts)

        ball_r  = Dot(radius=0.10, color=GREEN).move_to(r_pts[0])
        trail_r = VMobject(stroke_color=GREEN, stroke_width=2, stroke_opacity=0.55)
        trail_r.set_points_as_corners([r_pts[0], r_pts[0]])

        # Draw both charts first
        self.play(Create(gl), Create(gr), run_time=0.7)
        self.play(Write(lbl_l), Write(lbl_r), run_time=0.5)

        # Animate left (bouncing dots) and right (rolling ball) simultaneously
        self.add(ball_r, trail_r)
        t_r = ValueTracker(0.0)

        def upd_ball(mob):
            idx = min(int(t_r.get_value() * (n_r - 1)), n_r - 1)
            mob.move_to(r_pts[idx])

        def upd_trail(mob):
            idx = min(int(t_r.get_value() * (n_r - 1)), n_r - 1)
            pts = r_pts[:idx + 1]
            if len(pts) >= 2:
                mob.set_points_as_corners(pts)

        ball_r.add_updater(upd_ball)
        trail_r.add_updater(upd_trail)

        self.play(
            LaggedStart(*[FadeIn(d) for d in big_dots], lag_ratio=0.3),
            LaggedStart(*[GrowArrow(a) for a in big_arrows], lag_ratio=0.3),
            t_r.animate.set_value(1.0),
            run_time=2.5,
            rate_func=linear,
        )

        ball_r.remove_updater(upd_ball)
        trail_r.remove_updater(upd_trail)

        self.wait(1.2)
        self.play(FadeOut(VGroup(caption, gl, gr, lbl_l, lbl_r,
                                  big_dots, big_arrows, ball_r, trail_r)), run_time=0.4)

    # ── Seg 07 — Local Minima ─────────────────────────────────────────────────
    def _seg07_local_minima(self):
        ax, x_lbl, y_lbl = make_axes()
        curve = make_curve(ax)
        group = VGroup(ax, x_lbl, y_lbl, curve).scale(0.88).move_to(ORIGIN + DOWN * 0.5)
        self.add(group)

        # Verified minima: local trap at x=0.5073 (loss=1.63), global at x=-0.5866 (loss=0.45)
        local_x  =  0.5073
        global_x = -0.5866
        local_pt  = ax.c2p(local_x,  loss(local_x))
        global_pt = ax.c2p(global_x, loss(global_x))

        ball_local = Dot(radius=0.14, color=ORANGE).move_to(local_pt + UP * 0.18)

        local_lbl = Text("Local minimum\n(a trap!)", font_size=22, color=RED,
                         line_spacing=1.2).next_to(local_pt, RIGHT, buff=0.15)
        global_lbl = Text("Global minimum\n(the goal)", font_size=22, color=GREEN,
                          line_spacing=1.2).next_to(global_pt, LEFT, buff=0.12)

        local_line = DashedLine(
            ax.c2p(local_x, 0), local_pt, color=RED, stroke_width=1.5, dash_length=0.08
        )
        global_line = DashedLine(
            ax.c2p(global_x, 0), global_pt, color=GREEN, stroke_width=1.5, dash_length=0.08
        )

        caption = Text("The ball can get stuck.", font_size=30, color=WHITE)\
            .to_edge(UP, buff=0.4)
        sub = Text("Not every valley is the deepest.", font_size=22, color=GREY)\
            .next_to(caption, DOWN, buff=0.15)

        self.play(Write(caption), FadeIn(sub), run_time=0.7)
        self.play(FadeIn(ball_local), run_time=0.3)
        self.play(ball_local.animate.shift(DOWN * 0.18), rate_func=there_and_back, run_time=0.8)
        self.play(
            Create(local_line), Write(local_lbl),
            Create(global_line), Write(global_lbl),
            run_time=1.0,
        )
        self.wait(2.0)
        self.play(FadeOut(VGroup(caption, sub, ball_local, local_line, global_line,
                                  local_lbl, global_lbl, group)), run_time=0.4)

    # ── Seg 08 — Outro ────────────────────────────────────────────────────────
    def _seg08_outro(self):
        title  = Text("Gradient Descent", font_size=48, color=WHITE, weight=BOLD)
        eq     = Text("gradient  +  descent", font_size=26, color=GREY)
        eq2    = Text("slope       go down",  font_size=22, color=GREY)
        arrow  = Text("=", font_size=30, color=GREY)
        result = Text("Train any AI.", font_size=34, color=YELLOW)

        VGroup(title, eq, eq2, arrow, result).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        follow = Text("Follow for more in 60 seconds.", font_size=22, color=BLUE)\
            .to_edge(DOWN, buff=0.6)

        self.play(Write(title), run_time=0.7)
        self.play(FadeIn(eq), FadeIn(eq2), run_time=0.6)
        self.play(FadeIn(arrow), FadeIn(result), run_time=0.6)
        self.play(FadeIn(follow), run_time=0.5)
        self.wait(2.5)
