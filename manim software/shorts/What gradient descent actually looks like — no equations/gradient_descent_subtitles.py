"""
Gradient Descent - YouTube Short (9:16 vertical, 1080x1920)

Layout (frame = 14.22 wide x 8.0 tall, verified at -r 1080,1920):
  Caption zone : Y = +2.8 to +4.0   (top strip)
  Axes zone    : centered at UP*0.8  (top=-0.96 to bot=+2.56, clear of subtitles)
  Subtitle zone: Y = -3.0 (single line) or -3.3/-2.7 (two lines) — no card, white text

Colour palette:
  Blue #4f9eff  Orange #f97316  Green #10b981
  Yellow #fbbf24  Red #f87171  BG #0d0f14

Render:
  manim -pqh gradient_descent.py GradientDescentShort -r 1080,1920
"""

from manim import *
import numpy as np

# ── Palette ───────────────────────────────────────────────────────────────────
BG     = "#0d0f14"
BLUE   = "#4f9eff"
ORANGE = "#f97316"
GREEN  = "#10b981"
YELLOW = "#fbbf24"
RED    = "#f87171"
WHITE  = "#ffffff"
GREY   = "#8899aa"

# ── Layout constants (all verified against 8-unit frame height) ───────────────
AXES_CENTER   = UP * 0.8     # axes group anchor — bottom of axes at Y≈-0.96
CAPTION_Y     = 3.3          # top captions
SUB_Y_1LINE   = -3.0         # single subtitle line
SUB_Y_TOP     = -2.6         # first of two subtitle lines
SUB_Y_BOT     = -3.2         # second of two subtitle lines
SUB_FONT      = 26           # subtitle font size — readable, not huge
SUB_COLOR     = WHITE

# ── Loss function ─────────────────────────────────────────────────────────────
def loss(x):
    return 0.4 * x**2 + 0.6 * np.sin(2.5 * x) + 0.3 * np.cos(5 * x) + 1.2

def loss_deriv(x):
    return 0.8 * x + 1.5 * np.cos(2.5 * x) - 1.5 * np.sin(5 * x)

# ── Shared factories ──────────────────────────────────────────────────────────
def make_axes():
    ax = Axes(
        x_range=[-3.5, 3.5, 1], y_range=[0, 4.5, 1],
        x_length=7, y_length=4,
        axis_config={"color": GREY, "stroke_width": 1.5,
                     "include_ticks": False, "include_tip": True, "tip_length": 0.15},
    )
    x_lbl = Text("Model parameters", font_size=18, color=GREY).next_to(ax.x_axis, DOWN, buff=0.15)
    y_lbl = Text("Loss (error)", font_size=18, color=GREY).rotate(PI/2).next_to(ax.y_axis, LEFT, buff=0.15)
    return ax, x_lbl, y_lbl

def make_curve(ax):
    return ax.plot(loss, x_range=[-3.2, 3.2], color=BLUE, stroke_width=3)

# ── Subtitle helper ───────────────────────────────────────────────────────────
def show_subs(scene, lines, hold=2.5):
    """
    Show 1-2 subtitle lines at the bottom of the frame, no box.
    All lines fade in together instantly, hold, then fade out.
    Max 2 lines to guarantee no overlap with axes.
    """
    assert 1 <= len(lines) <= 2, "Max 2 subtitle lines per call"

    y_positions = [SUB_Y_1LINE] if len(lines) == 1 else [SUB_Y_TOP, SUB_Y_BOT]

    mobs = []
    for line, y in zip(lines, y_positions):
        mob = Text(line, font_size=SUB_FONT, color=SUB_COLOR)
        mob.move_to(np.array([0, y, 0]))
        mobs.append(mob)

    scene.play(*[FadeIn(m) for m in mobs], run_time=0.3)
    scene.wait(hold)
    scene.play(*[FadeOut(m) for m in mobs], run_time=0.25)


# ── Scene ─────────────────────────────────────────────────────────────────────
class GradientDescentShort(Scene):
    """
    Render: manim -pqh gradient_descent.py GradientDescentShort -r 1080,1920
    Preview a segment by calling only that _seg method in construct().
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

    def _subs(self, lines, hold=2.5):
        show_subs(self, lines, hold=hold)

    # ── Seg 01 — Hook ─────────────────────────────────────────────────────────
    def _seg01_hook(self):
        line1 = Text("Every AI you've ever used", font_size=36, color=WHITE)
        line2 = Text("was trained with", font_size=36, color=WHITE)
        line3 = Text("one trick.", font_size=52, color=YELLOW, weight=BOLD)
        stack = VGroup(line1, line2, line3).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(line1), run_time=0.5)
        self.play(FadeIn(line2), run_time=0.4)
        self.play(Write(line3), run_time=0.7)
        self._subs(["GPT, Stable Diffusion, AlphaFold —"], hold=0.3)
        self._subs(["all just functions with billions of knobs.", "Training = finding the right setting."], hold=2.5)

        self.play(FadeOut(stack), run_time=0.4)

    # ── Seg 02 — Loss Surface ─────────────────────────────────────────────────
    def _seg02_loss_surface(self):
        ax, x_lbl, y_lbl = make_axes()
        curve = make_curve(ax)
        group = VGroup(ax, x_lbl, y_lbl, curve).scale(0.88).move_to(AXES_CENTER)

        caption = Text("This is a loss surface.", font_size=30, color=WHITE)\
            .move_to(UP * CAPTION_Y)
        sub_lbl = Text("Height = how wrong your model is.", font_size=22, color=GREY)\
            .next_to(caption, DOWN, buff=0.18)

        self.play(Create(ax), Write(x_lbl), Write(y_lbl), run_time=0.8)
        self.play(Create(curve), run_time=0.8)
        self.play(Write(caption), FadeIn(sub_lbl), run_time=0.6)

        self._subs(["For every weight combo: one number — the loss.", "How badly is the model performing?"], hold=2.5)
        self._subs(["High = guessing randomly.", "The deepest valley = a model that works."], hold=2.5)

        self.play(FadeOut(VGroup(caption, sub_lbl, group)), run_time=0.4)

    # ── Seg 03 — Ball Rolling ─────────────────────────────────────────────────
    def _seg03_ball_rolling(self):
        ax, x_lbl, y_lbl = make_axes()
        curve = make_curve(ax)
        group = VGroup(ax, x_lbl, y_lbl, curve).scale(0.88).move_to(AXES_CENTER)
        self.add(group)

        # start=-2.5, lr=0.05: span~1.9, loss 4.0->0.45 (verified)
        x_val = -2.5
        x_positions = [x_val]
        for _ in range(120):
            x_val -= 0.05 * loss_deriv(x_val)
            x_val = float(np.clip(x_val, -3.2, 3.2))
            x_positions.append(x_val)
        x_smooth = np.interp(np.linspace(0,1,300), np.linspace(0,1,len(x_positions)),
                             np.array(x_positions))
        path_points = [ax.c2p(float(x), float(loss(x))) for x in x_smooth]
        n_pts = len(path_points)

        ball  = Dot(radius=0.14, color=ORANGE).move_to(path_points[0])
        trail = VMobject(stroke_color=ORANGE, stroke_width=2.5, stroke_opacity=0.55)
        trail.set_points_as_corners([path_points[0], path_points[0]])

        caption = Text("Step downhill. Then another. Then another.",
                       font_size=26, color=WHITE).move_to(UP * CAPTION_Y)

        self.play(FadeIn(ball), Write(caption), run_time=0.6)
        self.add(trail)

        t = ValueTracker(0.0)
        def upd_ball(m):
            idx = min(int(t.get_value() * (n_pts-1)), n_pts-1)
            m.move_to(path_points[idx])
        def upd_trail(m):
            idx = min(int(t.get_value() * (n_pts-1)), n_pts-1)
            pts = path_points[:idx+1]
            if len(pts) >= 2:
                m.set_points_as_corners(pts)

        ball.add_updater(upd_ball)
        trail.add_updater(upd_trail)
        self.play(t.animate.set_value(1.0), run_time=2.8, rate_func=linear)
        ball.remove_updater(upd_ball)
        trail.remove_updater(upd_trail)

        self._subs(["Calculus gives you the gradient —"], hold=0.8)
        self._subs(["direction of steepest ascent.", "Go the opposite. Step. Recompute. Repeat."], hold=2.5)

        self.play(FadeOut(VGroup(caption, ball, trail, group)), run_time=0.4)

    # ── Seg 04 — Labelled Surface ─────────────────────────────────────────────
    def _seg04_labelled_surface(self):
        ax, x_lbl, y_lbl = make_axes()
        curve = make_curve(ax)
        group = VGroup(ax, x_lbl, y_lbl, curve).scale(0.88).move_to(AXES_CENTER)
        self.add(group)

        # Global min: x=-0.5866, loss=0.4474 (verified)
        gmin_x  = -0.5866
        gmin_pt = ax.c2p(gmin_x, loss(gmin_x))
        star = Star(n=5, outer_radius=0.18, color=GREEN, fill_opacity=1)\
            .move_to(gmin_pt + UP * 0.25)
        star_lbl = Text("Most accurate\nmodel", font_size=20, color=GREEN, line_spacing=1.2)\
            .next_to(star, RIGHT, buff=0.15)

        surf_lbl = Text("Loss Surface", font_size=26, color=BLUE)\
            .move_to(ax.c2p(-2.0, 3.8))
        arrow = Arrow(surf_lbl.get_bottom(), ax.c2p(-2.5, loss(-2.5)),
                      buff=0.05, color=BLUE, stroke_width=2,
                      max_tip_length_to_length_ratio=0.15)

        self.play(FadeIn(surf_lbl), Create(arrow), run_time=0.7)
        self.play(FadeIn(star), Write(star_lbl), run_time=0.8)

        self._subs(["Each step = every parameter shifts simultaneously."], hold=0.5)
        self._subs(["100 billion numbers. One update.", "The math that makes this work: backpropagation."], hold=2.5)

        self.play(FadeOut(VGroup(surf_lbl, arrow, star, star_lbl, group)), run_time=0.4)

    # ── Seg 05 — Gradient Label ───────────────────────────────────────────────
    def _seg05_gradient_label(self):
        ax, x_lbl, y_lbl = make_axes()
        curve = make_curve(ax)
        group = VGroup(ax, x_lbl, y_lbl, curve).scale(0.88).move_to(AXES_CENTER)
        self.add(group)

        px = -2.2
        slope = loss_deriv(px)
        dx = 0.7
        slope_arrow = Arrow(
            ax.c2p(px-dx, loss(px)-slope*dx),
            ax.c2p(px+dx, loss(px)+slope*dx),
            buff=0, color=YELLOW, stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )
        slope_lbl = Text("gradient (slope)", font_size=22, color=YELLOW)\
            .next_to(slope_arrow, UP, buff=0.15)

        title = Text("Gradient Descent", font_size=40, color=WHITE, weight=BOLD)\
            .move_to(UP * CAPTION_Y)
        sub_lbl = Text("Follow the slope. Go down.", font_size=24, color=GREY)\
            .next_to(title, DOWN, buff=0.18)

        self.play(Write(title), FadeIn(sub_lbl), run_time=0.6)
        self.play(Create(slope_arrow), Write(slope_lbl), run_time=0.8)

        self._subs(["The gradient points uphill."], hold=0.5)
        self._subs(["So we step downhill — every iteration.", "Gradient descent. Simple idea. Absurd scale."], hold=2.5)

        self.play(FadeOut(VGroup(title, sub_lbl, slope_arrow, slope_lbl, group)), run_time=0.4)

    # ── Seg 06 — Learning Rate ────────────────────────────────────────────────
    def _seg06_learning_rate(self):
        caption = Text("Step size = learning rate", font_size=30, color=WHITE)\
            .move_to(UP * CAPTION_Y)
        self.play(Write(caption), run_time=0.5)

        # LEFT: too-large lr
        ax_l, _, _ = make_axes()
        gl = VGroup(ax_l, make_curve(ax_l)).scale(0.40).move_to(LEFT * 3.2 + UP * 0.5)
        lbl_l = Text("Too large", font_size=22, color=RED).next_to(gl, UP, buff=0.12)

        big_x_vals = [-2.5, 2.2, -1.8, 1.4, -0.9]
        big_dots = VGroup(*[Dot(radius=0.10, color=RED).move_to(ax_l.c2p(x, loss(x)))
                             for x in big_x_vals])
        big_arrows = VGroup()
        for i in range(len(big_x_vals)-1):
            big_arrows.add(Arrow(
                ax_l.c2p(big_x_vals[i],   loss(big_x_vals[i])),
                ax_l.c2p(big_x_vals[i+1], loss(big_x_vals[i+1])),
                buff=0.05, color=RED, stroke_width=2, max_tip_length_to_length_ratio=0.2,
            ))

        # RIGHT: just-right lr rolling ball (start=3.0, lr=0.05, verified)
        ax_r, _, _ = make_axes()
        gr = VGroup(ax_r, make_curve(ax_r)).scale(0.40).move_to(RIGHT * 3.2 + UP * 0.5)
        lbl_r = Text("Just right", font_size=22, color=GREEN).next_to(gr, UP, buff=0.12)

        x_val = 3.0
        x_pos = [x_val]
        for _ in range(60):
            x_val -= 0.05 * loss_deriv(x_val)
            x_val = float(np.clip(x_val, -3.2, 3.2))
            x_pos.append(x_val)
        x_sm  = np.interp(np.linspace(0,1,200), np.linspace(0,1,len(x_pos)), np.array(x_pos))
        r_pts = [ax_r.c2p(float(x), float(loss(x))) for x in x_sm]
        n_r   = len(r_pts)

        ball_r  = Dot(radius=0.10, color=GREEN).move_to(r_pts[0])
        trail_r = VMobject(stroke_color=GREEN, stroke_width=2, stroke_opacity=0.55)
        trail_r.set_points_as_corners([r_pts[0], r_pts[0]])

        self.play(Create(gl), Create(gr), run_time=0.7)
        self.play(Write(lbl_l), Write(lbl_r), run_time=0.4)
        self.add(ball_r, trail_r)

        t_r = ValueTracker(0.0)
        def upd_b(m):
            idx = min(int(t_r.get_value()*(n_r-1)), n_r-1)
            m.move_to(r_pts[idx])
        def upd_t(m):
            idx = min(int(t_r.get_value()*(n_r-1)), n_r-1)
            pts = r_pts[:idx+1]
            if len(pts) >= 2:
                m.set_points_as_corners(pts)

        ball_r.add_updater(upd_b)
        trail_r.add_updater(upd_t)
        self.play(
            LaggedStart(*[FadeIn(d) for d in big_dots], lag_ratio=0.3),
            LaggedStart(*[GrowArrow(a) for a in big_arrows], lag_ratio=0.3),
            t_r.animate.set_value(1.0),
            run_time=2.0, rate_func=linear,
        )
        ball_r.remove_updater(upd_b)
        trail_r.remove_updater(upd_t)

        self._subs(["Too large: bounce off the walls, never converge."], hold=0.6)
        self._subs(["Too small: training bill bankrupts you.", "Solution: schedulers. Start bold, get precise."], hold=2.5)

        self.play(FadeOut(VGroup(caption, gl, gr, lbl_l, lbl_r,
                                  big_dots, big_arrows, ball_r, trail_r)), run_time=0.4)

    # ── Seg 07 — Local Minima ─────────────────────────────────────────────────
    def _seg07_local_minima(self):
        ax, x_lbl, y_lbl = make_axes()
        curve = make_curve(ax)
        group = VGroup(ax, x_lbl, y_lbl, curve).scale(0.88).move_to(AXES_CENTER)
        self.add(group)

        # Verified: local=0.5073 (loss=1.63), global=-0.5866 (loss=0.45)
        local_x  =  0.5073
        global_x = -0.5866
        local_pt  = ax.c2p(local_x,  loss(local_x))
        global_pt = ax.c2p(global_x, loss(global_x))

        ball_local = Dot(radius=0.14, color=ORANGE).move_to(local_pt + UP * 0.18)
        local_lbl  = Text("Local min\n(trap!)", font_size=22, color=RED, line_spacing=1.2)\
            .next_to(local_pt,  RIGHT, buff=0.15)
        global_lbl = Text("Global min\n(goal)", font_size=22, color=GREEN, line_spacing=1.2)\
            .next_to(global_pt, LEFT,  buff=0.12)
        local_line  = DashedLine(ax.c2p(local_x,  0), local_pt,
                                  color=RED,   stroke_width=1.5, dash_length=0.08)
        global_line = DashedLine(ax.c2p(global_x, 0), global_pt,
                                  color=GREEN, stroke_width=1.5, dash_length=0.08)

        caption = Text("The ball can get stuck.", font_size=30, color=WHITE)\
            .move_to(UP * CAPTION_Y)

        self.play(Write(caption), run_time=0.5)
        self.play(FadeIn(ball_local), run_time=0.3)
        self.play(ball_local.animate.shift(DOWN * 0.18), rate_func=there_and_back, run_time=0.8)
        self.play(Create(local_line), Write(local_lbl),
                  Create(global_line), Write(global_lbl), run_time=1.0)

        self._subs(["The real trap: saddle points."], hold=0.6)
        self._subs(["Gradient near zero. Model stalls. Thinks it's done.", "Adam uses momentum to roll through."], hold=2.5)

        self.play(FadeOut(VGroup(caption, ball_local, local_line, global_line,
                                  local_lbl, global_lbl, group)), run_time=0.4)

    # ── Seg 08 — Outro ────────────────────────────────────────────────────────
    def _seg08_outro(self):
        title  = Text("Gradient Descent", font_size=48, color=WHITE, weight=BOLD)
        eq     = Text("gradient  +  descent", font_size=26, color=GREY)
        eq2    = Text("slope         go down", font_size=22, color=GREY)
        eq_sep = Text("=  Train any AI.", font_size=32, color=YELLOW)

        VGroup(title, eq, eq2, eq_sep).arrange(DOWN, buff=0.38).move_to(UP * 0.5)

        self.play(Write(title), run_time=0.6)
        self.play(FadeIn(eq), FadeIn(eq2), run_time=0.5)
        self.play(FadeIn(eq_sep), run_time=0.5)

        self._subs(["Months of training. Billions of parameters.", "Trillions of gradient descent steps."], hold=1.5)
        self._subs(["An absurdly complex loss surface.", "And an optimizer finding the bottom."], hold=2.5)

        follow = Text("Follow for more in 60 seconds.", font_size=24, color=BLUE)\
            .move_to(DOWN * 3.0)
        self.play(FadeIn(follow), run_time=0.5)
        self.wait(2.5)
