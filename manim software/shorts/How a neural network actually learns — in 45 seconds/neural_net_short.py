from manim import *
import numpy as np

# ─── Colour palette ───────────────────────────────────────────────
BG      = "#0d0f14"
BLUE    = "#4f9eff"
ORANGE  = "#f97316"
GREEN   = "#10b981"
YELLOW  = "#fbbf24"
RED     = "#f87171"
PURPLE  = "#a855f7"
WHITE   = "#e2e8f0"
GREY    = "#64748b"

# ─── Subtitle helper ──────────────────────────────────────────────
def make_subtitle(text, font_size=28):
    """Centred subtitle bar at the bottom of the frame."""
    label = Text(
        text,
        font_size=font_size,
        color=WHITE,
        font="Monospace",
    )
    label.move_to(DOWN * 3.3)
    bg = Rectangle(
        width=config.frame_width,
        height=0.65,
        fill_color="#000000",
        fill_opacity=0.65,
        stroke_width=0,
    ).move_to(DOWN * 3.3)
    return VGroup(bg, label)


class NeuralNetShort(Scene):
    """
    YouTube Short  —  'How a neural network actually learns in 45 seconds'
    Scenes
      0  Hook title card
      1  Simple 3-layer network diagram
      2  Forward pass  —  prediction bubble
      3  Loss  —  error arrow
      4  Gradient descent  —  loss-curve animation
      5  Weight update  —  one weight changes colour
      6  Loop + improvement  —  loss drops
      7  Payoff card
    Total runtime ≈ 45 s
    """

    def construct(self):
        self.camera.background_color = BG

        self.scene_hook()
        self.scene_network()
        self.scene_forward_pass()
        self.scene_loss()
        self.scene_gradient_descent()
        self.scene_weight_update()
        self.scene_payoff()

    # ──────────────────────────────────────────────────────────────
    # SCENE 0 — Hook  (~4 s)
    # ──────────────────────────────────────────────────────────────
    def scene_hook(self):
        line1 = Text("Forget the hype.", font_size=52, color=YELLOW, weight=BOLD)
        line2 = Text("This is literally all", font_size=38, color=WHITE)
        line3 = Text("a neural net does.", font_size=38, color=BLUE, weight=BOLD)
        vg = VGroup(line1, line2, line3).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        sub = make_subtitle("What does a neural network actually do?")

        self.play(FadeIn(line1, shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(line2), FadeIn(line3), run_time=0.6)
        self.add(sub)
        self.wait(2.2)
        self.play(FadeOut(VGroup(vg, sub)), run_time=0.4)

    # ──────────────────────────────────────────────────────────────
    # SCENE 1 — Network diagram  (~5 s)
    # ──────────────────────────────────────────────────────────────
    def scene_network(self):
        sub = make_subtitle("3 layers: input  ->  hidden  ->  output")

        layers = [2, 3, 1]          # neurons per layer
        x_positions = [-3.5, 0, 3.5]
        layer_colors = [GREEN, BLUE, ORANGE]

        all_nodes = []
        for li, (n, xp, col) in enumerate(zip(layers, x_positions, layer_colors)):
            ys = np.linspace(-(n - 1) * 0.8, (n - 1) * 0.8, n)
            row = []
            for y in ys:
                c = Circle(radius=0.32, color=col, fill_color=BG,
                           fill_opacity=1, stroke_width=3)
                c.move_to([xp, y, 0])
                row.append(c)
            all_nodes.append(row)

        # Layer labels
        lnames = ["Input", "Hidden", "Output"]
        lcolor = [GREEN, BLUE, ORANGE]
        labels = []
        for i, (name, xp, col) in enumerate(zip(lnames, x_positions, lcolor)):
            t = Text(name, font_size=22, color=col)
            t.move_to([xp, -2.1, 0])
            labels.append(t)

        # Edges (connections)
        edges = []
        for li in range(len(layers) - 1):
            for src in all_nodes[li]:
                for dst in all_nodes[li + 1]:
                    e = Line(
                        src.get_center(), dst.get_center(),
                        color=GREY, stroke_width=1.5, stroke_opacity=0.5
                    )
                    edges.append(e)

        edge_group = VGroup(*edges)
        node_group = VGroup(*[n for row in all_nodes for n in row])
        label_group = VGroup(*labels)

        self.play(
            Create(edge_group),
            LaggedStart(*[GrowFromCenter(n) for n in node_group], lag_ratio=0.08),
            run_time=1.4,
        )
        self.play(FadeIn(label_group), run_time=0.4)
        self.add(sub)
        self.wait(2.8)

        # keep network for next scenes
        self._net_edges = edge_group
        self._net_nodes = all_nodes
        self._net_labels = label_group
        self._net_all = VGroup(edge_group, node_group, label_group)
        self._sub_ref = sub

    # ──────────────────────────────────────────────────────────────
    # SCENE 2 — Forward pass  (~5 s)
    # ──────────────────────────────────────────────────────────────
    def scene_forward_pass(self):
        self.play(FadeOut(self._sub_ref), run_time=0.2)
        sub = make_subtitle("Step 1: feed data in, get a prediction out")
        self.add(sub)

        # Animate a 'signal' moving left -> right
        signal = Dot(color=YELLOW, radius=0.18)
        signal.move_to(self._net_nodes[0][0].get_center())

        path_pts = [
            self._net_nodes[0][0].get_center(),
            self._net_nodes[1][1].get_center(),
            self._net_nodes[2][0].get_center(),
        ]
        path = VMobject()
        path.set_points_as_corners(path_pts)

        pred_label = Text("Prediction: 0.83", font_size=26, color=YELLOW)
        pred_label.next_to(self._net_nodes[2][0], RIGHT, buff=0.4)

        self.play(MoveAlongPath(signal, path), run_time=1.2)
        self.play(FadeIn(pred_label, shift=RIGHT * 0.2), run_time=0.4)
        self.wait(2.0)

        self.play(FadeOut(sub), FadeOut(pred_label), FadeOut(signal), run_time=0.3)

        self._pred_label = pred_label
        self._pred_scene = VGroup(pred_label, signal)

    # ──────────────────────────────────────────────────────────────
    # SCENE 3 — Loss  (~5 s)
    # ──────────────────────────────────────────────────────────────
    def scene_loss(self):
        sub = make_subtitle("Step 2: measure the mistake (the 'loss')")
        self.add(sub)

        out_node = self._net_nodes[2][0]

        pred_dot = Dot(color=YELLOW, radius=0.15).move_to(out_node.get_center() + UP * 0.7)
        true_dot = Dot(color=GREEN, radius=0.15).move_to(out_node.get_center() + DOWN * 0.7)

        pred_t = Text("Predicted: 0.83", font_size=22, color=YELLOW).next_to(pred_dot, RIGHT, buff=0.2)
        true_t = Text("Actual:      1.00", font_size=22, color=GREEN).next_to(true_dot, RIGHT, buff=0.2)

        error_line = DashedLine(
            pred_dot.get_center(), true_dot.get_center(),
            color=RED, dash_length=0.12, stroke_width=3
        )
        loss_label = Text("Loss = 0.17", font_size=28, color=RED, weight=BOLD)
        loss_label.move_to(out_node.get_center() + RIGHT * 2.6)

        self.play(
            FadeIn(pred_dot), FadeIn(pred_t),
            FadeIn(true_dot), FadeIn(true_t),
            run_time=0.6,
        )
        self.play(Create(error_line), run_time=0.5)
        self.play(Write(loss_label), run_time=0.5)
        self.wait(2.2)

        self.play(
            FadeOut(VGroup(pred_dot, pred_t, true_dot, true_t,
                           error_line, loss_label, sub)),
            run_time=0.4,
        )

    # ──────────────────────────────────────────────────────────────
    # SCENE 4 — Gradient descent curve  (~8 s)
    # ──────────────────────────────────────────────────────────────
    def scene_gradient_descent(self):
        # Slide the network out, show the loss curve full width
        self.play(
            self._net_all.animate.scale(0.45).to_corner(UL, buff=0.4),
            run_time=0.5,
        )

        sub = make_subtitle("Step 3: slide DOWN the loss curve (gradient descent)")
        self.add(sub)

        # Axes
        ax = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.1, 0.2],
            x_length=7,
            y_length=3.5,
            axis_config={"color": GREY, "stroke_width": 2},
            tips=False,
        ).shift(RIGHT * 0.8 + DOWN * 0.3)

        x_lbl = Text("Training steps", font_size=20, color=GREY).next_to(ax, DOWN, buff=0.15)
        y_lbl = Text("Loss", font_size=20, color=GREY).next_to(ax, LEFT, buff=0.15)

        # Loss curve  y = 0.9 * e^(-0.4x) + 0.05
        curve = ax.plot(
            lambda x: 0.9 * np.exp(-0.4 * x) + 0.05,
            x_range=[0, 10],
            color=RED,
            stroke_width=3,
        )

        self.play(
            Create(ax), FadeIn(x_lbl), FadeIn(y_lbl),
            run_time=0.6,
        )
        self.play(Create(curve), run_time=1.0)

        # Ball rolling down the curve
        ball = Dot(color=YELLOW, radius=0.18)
        ball.move_to(ax.c2p(0, 0.9 * np.exp(0) + 0.05))

        def ball_updater(mob, alpha):
            x = alpha * 10
            y = 0.9 * np.exp(-0.4 * x) + 0.05
            mob.move_to(ax.c2p(x, y))

        self.add(ball)

        # Dashed vertical drop lines to show steps
        step_xs = [0, 2, 4, 7]
        step_dots = []
        for sx in step_xs:
            sy = 0.9 * np.exp(-0.4 * sx) + 0.05
            d = Dot(color=BLUE, radius=0.12).move_to(ax.c2p(sx, sy))
            step_dots.append(d)

        self.play(
            UpdateFromAlphaFunc(ball, ball_updater),
            LaggedStart(*[GrowFromCenter(d) for d in step_dots], lag_ratio=0.25),
            run_time=3.0,
            rate_func=rate_functions.ease_in_out_sine,
        )

        # Annotation at minimum
        min_lbl = Text("Minimum loss!", font_size=22, color=GREEN, weight=BOLD)
        min_lbl.next_to(ax.c2p(9.5, 0.07), UP, buff=0.25)
        arrow_to_min = Arrow(
            min_lbl.get_bottom(), ax.c2p(9.5, 0.07),
            color=GREEN, stroke_width=2, buff=0.05,
            max_tip_length_to_length_ratio=0.25
        )
        self.play(FadeIn(min_lbl), Create(arrow_to_min), run_time=0.5)
        self.wait(1.8)

        self.play(
            FadeOut(VGroup(ax, curve, ball, x_lbl, y_lbl,
                           min_lbl, arrow_to_min, sub,
                           *step_dots)),
            self._net_all.animate.scale(1 / 0.45).move_to(ORIGIN),
            run_time=0.5,
        )

    # ──────────────────────────────────────────────────────────────
    # SCENE 5 — Weight update  (~6 s)
    # ──────────────────────────────────────────────────────────────
    def scene_weight_update(self):
        sub = make_subtitle("Step 4: nudge every weight to reduce the loss")
        self.add(sub)

        # Highlight one specific edge
        src = self._net_nodes[0][1]
        dst = self._net_nodes[1][0]

        highlight_edge = Line(
            src.get_center(), dst.get_center(),
            color=YELLOW, stroke_width=5
        )

        weight_before = Text("w = -0.42", font_size=26, color=GREY)
        weight_before.move_to(UP * 2.5 + LEFT * 0.5)

        weight_after = Text("w = -0.35", font_size=26, color=GREEN, weight=BOLD)
        weight_after.move_to(UP * 2.5 + LEFT * 0.5)

        delta = Text("Nudged by gradient!", font_size=22, color=YELLOW)
        delta.next_to(weight_after, DOWN, buff=0.2)

        self.play(Create(highlight_edge), run_time=0.4)
        self.play(FadeIn(weight_before), run_time=0.3)
        self.wait(0.8)
        self.play(
            FadeOut(weight_before),
            FadeIn(weight_after),
            run_time=0.5,
        )
        self.play(FadeIn(delta), run_time=0.3)
        self.wait(1.8)

        self.play(FadeOut(VGroup(highlight_edge, weight_after, delta, sub)), run_time=0.3)

    # ──────────────────────────────────────────────────────────────
    # SCENE 6 — Payoff card  (~6 s)
    # ──────────────────────────────────────────────────────────────
    def scene_payoff(self):
        self.play(FadeOut(self._net_all), run_time=0.4)

        sub = make_subtitle("Repeat millions of times = a trained neural network")
        self.add(sub)

        # Loop diagram: Forward -> Loss -> Backward -> Update -> repeat
        steps = ["Forward pass", "Compute loss", "Backprop", "Update weights"]
        step_colors = [GREEN, RED, PURPLE, BLUE]
        boxes = []
        for i, (s, col) in enumerate(zip(steps, step_colors)):
            rect = RoundedRectangle(
                corner_radius=0.18,
                width=2.6, height=0.75,
                fill_color=col, fill_opacity=0.18,
                stroke_color=col, stroke_width=2,
            )
            label = Text(s, font_size=22, color=col)
            label.move_to(rect.get_center())
            box = VGroup(rect, label)
            boxes.append(box)

        # Arrange in a 2x2 grid
        boxes[0].move_to(LEFT * 1.5 + UP * 1.1)
        boxes[1].move_to(RIGHT * 1.5 + UP * 1.1)
        boxes[2].move_to(RIGHT * 1.5 + DOWN * 0.5)
        boxes[3].move_to(LEFT * 1.5 + DOWN * 0.5)

        # Arrows between boxes
        a1 = Arrow(boxes[0].get_right(), boxes[1].get_left(), color=GREY, buff=0.1,
                   stroke_width=2, max_tip_length_to_length_ratio=0.25)
        a2 = Arrow(boxes[1].get_bottom(), boxes[2].get_top(), color=GREY, buff=0.1,
                   stroke_width=2, max_tip_length_to_length_ratio=0.25)
        a3 = Arrow(boxes[2].get_left(), boxes[3].get_right(), color=GREY, buff=0.1,
                   stroke_width=2, max_tip_length_to_length_ratio=0.25)
        a4 = Arrow(boxes[3].get_top(), boxes[0].get_bottom(), color=GREY, buff=0.1,
                   stroke_width=2, max_tip_length_to_length_ratio=0.25)

        loop_label = Text("x 1,000,000", font_size=30, color=YELLOW, weight=BOLD)
        loop_label.move_to(ORIGIN + UP * 0.3)

        all_boxes = VGroup(*boxes)
        all_arrows = VGroup(a1, a2, a3, a4)

        self.play(
            LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in boxes], lag_ratio=0.15),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[Create(a) for a in [a1, a2, a3, a4]], lag_ratio=0.15),
            run_time=0.8,
        )
        self.play(Write(loop_label), run_time=0.4)
        self.wait(1.0)

        # Final punch line
        self.play(FadeOut(VGroup(all_boxes, all_arrows, loop_label, sub)), run_time=0.4)

        final = Text("That's it.", font_size=64, color=YELLOW, weight=BOLD)
        sub2 = Text(
            "No magic. Just math, repeated.",
            font_size=30, color=WHITE,
        ).next_to(final, DOWN, buff=0.35)
        follow = Text(
            "Follow for more data science in 60 sec",
            font_size=22, color=BLUE,
        ).next_to(sub2, DOWN, buff=0.5)

        self.play(FadeIn(final, scale=1.15), run_time=0.5)
        self.play(FadeIn(sub2), run_time=0.4)
        self.play(FadeIn(follow), run_time=0.4)
        self.wait(2.8)

        self.play(FadeOut(VGroup(final, sub2, follow)), run_time=0.5)
