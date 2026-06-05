from manim import *
import numpy as np

# ─── Colour palette ───────────────────────────────────────────────
BG     = "#0d0f14"
BLUE   = "#4f9eff"
ORANGE = "#f97316"
GREEN  = "#10b981"
YELLOW = "#fbbf24"
RED    = "#f87171"
PURPLE = "#a855f7"
WHITE  = "#e2e8f0"
GREY   = "#64748b"
DARK   = "#1e2130"

# ─── Subtitle helper ──────────────────────────────────────────────
def make_subtitle(text, font_size=26):
    label = Text(text, font_size=font_size, color=WHITE, font="Monospace")
    label.move_to(DOWN * 3.3)
    bg = Rectangle(
        width=config.frame_width, height=0.68,
        fill_color="#000000", fill_opacity=0.72, stroke_width=0,
    ).move_to(DOWN * 3.3)
    return VGroup(bg, label)

def make_formula_box(tex_str, color=BLUE, width=5.5, height=0.9):
    """A coloured rounded box wrapping a LaTeX formula."""
    box = RoundedRectangle(
        corner_radius=0.15, width=width, height=height,
        fill_color=color, fill_opacity=0.12,
        stroke_color=color, stroke_width=2,
    )
    formula = MathTex(tex_str, color=color, font_size=34)
    formula.move_to(box.get_center())
    return VGroup(box, formula)


# ══════════════════════════════════════════════════════════════════
class NeuralNetShortV2(Scene):
    """
    YouTube Short v2  —  deeper script + richer animations  (~58 s)

    Scene map
    ─────────
    0  Hook            "Every AI you've used runs on 4 steps."          ~4 s
    1  Network         Build network, label neurons + weights            ~6 s
    2  Forward pass    Weighted sum z=wx+b, activation, ripple signals   ~8 s
    3  Loss            MSE formula, squared-error bar visualised         ~7 s
    4  Gradient        Tangent slope, gradient arrow, learning rate      ~9 s
    5  Backprop        Error signal flows backwards, colour magnitude    ~7 s
    6  Weight update   w = w - lr*grad with real numbers                 ~6 s
    7  Convergence     Epoch 1 vs Epoch 1000 side-by-side                ~6 s
    8  Payoff          Loop cycles x3, loss counter, final card          ~5 s
    """

    def construct(self):
        self.camera.background_color = BG
        self.scene_hook()
        self.scene_network()
        self.scene_forward_pass()
        self.scene_loss()
        self.scene_gradient_descent()
        self.scene_backprop()
        self.scene_weight_update()
        self.scene_convergence()
        self.scene_payoff()

    # ─────────────────────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────────────────────
    def _build_network(self, layers=(2, 3, 1),
                       x_positions=(-3.5, 0, 3.5),
                       layer_colors=(GREEN, BLUE, ORANGE),
                       node_radius=0.30):
        """Returns (all_nodes list-of-lists, edge_group, node_group, label_group)."""
        all_nodes = []
        for li, (n, xp, col) in enumerate(zip(layers, x_positions, layer_colors)):
            ys = np.linspace(-(n - 1) * 0.85, (n - 1) * 0.85, n)
            row = []
            for y in ys:
                c = Circle(radius=node_radius, color=col,
                           fill_color=BG, fill_opacity=1, stroke_width=3)
                c.move_to([xp, y, 0])
                row.append(c)
            all_nodes.append(row)

        edges = []
        for li in range(len(layers) - 1):
            for src in all_nodes[li]:
                for dst in all_nodes[li + 1]:
                    e = Line(src.get_center(), dst.get_center(),
                             color=GREY, stroke_width=1.4, stroke_opacity=0.45)
                    edges.append(e)

        lnames = ["Input", "Hidden", "Output"]
        labels = []
        for name, xp, col in zip(lnames, x_positions, layer_colors):
            t = Text(name, font_size=20, color=col).move_to([xp, -2.2, 0])
            labels.append(t)

        edge_group  = VGroup(*edges)
        node_group  = VGroup(*[n for row in all_nodes for n in row])
        label_group = VGroup(*labels)
        return all_nodes, edge_group, node_group, label_group

    # ─────────────────────────────────────────────────────────────
    # SCENE 0 — Hook  (~4 s)
    # ─────────────────────────────────────────────────────────────
    def scene_hook(self):
        line1 = Text("Every AI you've used", font_size=40, color=WHITE)
        line2 = Text("runs on just 4 steps.", font_size=40, color=YELLOW, weight=BOLD)
        line3 = Text("Here they are.", font_size=32, color=BLUE)
        vg = VGroup(line1, line2, line3).arrange(DOWN, buff=0.28).move_to(ORIGIN)

        sub = make_subtitle("GPT, image AI, recommendations — all the same 4 steps")

        self.play(FadeIn(line1, shift=UP * 0.25), run_time=0.5)
        self.play(FadeIn(line2), run_time=0.4)
        self.play(FadeIn(line3), run_time=0.4)
        self.add(sub)
        self.wait(2.0)
        self.play(FadeOut(VGroup(vg, sub)), run_time=0.35)

    # ─────────────────────────────────────────────────────────────
    # SCENE 1 — Network with weight labels  (~6 s)
    # ─────────────────────────────────────────────────────────────
    def scene_network(self):
        all_nodes, edges, nodes, labels = self._build_network()

        sub = make_subtitle("Each connection has a weight  —  a number the model learns")

        self.play(
            Create(edges),
            LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.07),
            run_time=1.2,
        )
        self.play(FadeIn(labels), run_time=0.4)
        self.add(sub)
        self.wait(0.6)

        # Show a few weight labels on edges
        sample_edges_idx = [0, 2, 4]
        sample_weights   = [" 0.73", "-0.42", " 1.18"]
        w_labels = []
        all_edges_list = edges.submobjects
        for idx, wstr in zip(sample_edges_idx, sample_weights):
            edge = all_edges_list[idx]
            mid  = edge.get_center()
            lbl  = Text(wstr, font_size=18, color=ORANGE)
            lbl.move_to(mid + UP * 0.22)
            w_labels.append(lbl)

        self.play(LaggedStart(*[FadeIn(w) for w in w_labels], lag_ratio=0.25), run_time=0.8)
        self.wait(1.8)
        self.play(FadeOut(VGroup(*w_labels, sub)), run_time=0.3)

        self._all_nodes  = all_nodes
        self._edges      = edges
        self._nodes_vg   = nodes
        self._labels_vg  = labels
        self._net_all    = VGroup(edges, nodes, labels)

    # ─────────────────────────────────────────────────────────────
    # SCENE 2 — Forward pass with weighted sum  (~8 s)
    # ─────────────────────────────────────────────────────────────
    def scene_forward_pass(self):
        sub = make_subtitle("Step 1 — Forward pass: z = wx + b  then  activation(z)")
        self.add(sub)

        # Flash each edge in sequence to simulate signal propagation
        all_edges = self._edges.submobjects
        n_l0_to_l1 = len(self._all_nodes[0]) * len(self._all_nodes[1])  # 6 edges
        l0l1_edges = all_edges[:n_l0_to_l1]
        l1l2_edges = all_edges[n_l0_to_l1:]

        # Wave 1: input -> hidden
        flash_anims_1 = []
        for e in l0l1_edges:
            flash_anims_1.append(
                ShowPassingFlash(
                    e.copy().set_color(YELLOW).set_stroke(width=4),
                    time_width=0.5,
                    run_time=0.9,
                )
            )
        self.play(LaggedStart(*flash_anims_1, lag_ratio=0.12))

        # Hidden nodes light up with activation
        for node in self._all_nodes[1]:
            self.play(
                node.animate.set_fill(BLUE, opacity=0.55),
                run_time=0.12,
            )

        # Show weighted sum formula near hidden layer
        formula1 = MathTex(r"z = \sum w_i x_i + b", font_size=30, color=BLUE)
        formula1.move_to(UP * 2.8)
        formula2 = MathTex(r"\hat{y} = \sigma(z) = \frac{1}{1+e^{-z}}", font_size=28, color=PURPLE)
        formula2.next_to(formula1, DOWN, buff=0.25)

        self.play(Write(formula1), run_time=0.7)
        self.play(FadeIn(formula2), run_time=0.5)

        # Wave 2: hidden -> output
        flash_anims_2 = []
        for e in l1l2_edges:
            flash_anims_2.append(
                ShowPassingFlash(
                    e.copy().set_color(YELLOW).set_stroke(width=4),
                    time_width=0.5,
                    run_time=0.9,
                )
            )
        self.play(LaggedStart(*flash_anims_2, lag_ratio=0.18))

        # Output node fires
        out_node = self._all_nodes[2][0]
        self.play(out_node.animate.set_fill(ORANGE, opacity=0.6), run_time=0.2)

        pred_lbl = MathTex(r"\hat{y} = 0.83", font_size=36, color=ORANGE)
        pred_lbl.next_to(out_node, RIGHT, buff=0.45)
        self.play(FadeIn(pred_lbl, shift=RIGHT * 0.15), run_time=0.4)
        self.wait(1.4)

        self.play(FadeOut(VGroup(formula1, formula2, pred_lbl, sub)), run_time=0.3)
        # Reset node fills
        for node in self._all_nodes[1]:
            node.set_fill(BG, opacity=1)
        out_node.set_fill(BG, opacity=1)

    # ─────────────────────────────────────────────────────────────
    # SCENE 3 — Loss: MSE formula + visual bar  (~7 s)
    # ─────────────────────────────────────────────────────────────
    def scene_loss(self):
        sub = make_subtitle("Step 2 — Loss: how wrong is our prediction? (squared error)")
        self.add(sub)

        # Slide network small
        self.play(self._net_all.animate.scale(0.42).to_corner(UL, buff=0.35), run_time=0.4)

        # Number line showing prediction vs truth
        nl = NumberLine(
            x_range=[0, 1, 0.25], length=6,
            color=GREY, stroke_width=2,
            include_numbers=True, font_size=22,
        ).shift(DOWN * 0.2)
        self.play(Create(nl), run_time=0.5)

        pred_dot = Dot(color=ORANGE, radius=0.18).move_to(nl.n2p(0.83))
        true_dot = Dot(color=GREEN,  radius=0.18).move_to(nl.n2p(1.00))
        pred_lbl = MathTex(r"\hat{y}=0.83", font_size=26, color=ORANGE).next_to(pred_dot, UP, buff=0.2)
        true_lbl = MathTex(r"y=1.00",       font_size=26, color=GREEN ).next_to(true_dot, UP, buff=0.2)

        self.play(
            GrowFromCenter(pred_dot), FadeIn(pred_lbl),
            GrowFromCenter(true_dot), FadeIn(true_lbl),
            run_time=0.6,
        )

        # Bracket showing the error gap
        brace = BraceBetweenPoints(nl.n2p(0.83), nl.n2p(1.00), direction=DOWN)
        err_lbl = Text("error = 0.17", font_size=22, color=RED).next_to(brace, DOWN, buff=0.15)
        self.play(Create(brace), FadeIn(err_lbl), run_time=0.5)

        # MSE formula box
        mse_box = make_formula_box(
            r"\mathcal{L} = (y - \hat{y})^2 = (0.17)^2 = 0.029",
            color=RED, width=7.2, height=0.95,
        )
        mse_box.move_to(UP * 2.3)
        self.play(FadeIn(mse_box), run_time=0.5)
        self.wait(1.8)

        self.play(
            FadeOut(VGroup(nl, pred_dot, pred_lbl, true_dot, true_lbl,
                           brace, err_lbl, mse_box, sub)),
            self._net_all.animate.scale(1 / 0.42).move_to(ORIGIN),
            run_time=0.5,
        )

    # ─────────────────────────────────────────────────────────────
    # SCENE 4 — Gradient descent with tangent line  (~9 s)
    # ─────────────────────────────────────────────────────────────
    def scene_gradient_descent(self):
        self.play(self._net_all.animate.scale(0.40).to_corner(UL, buff=0.35), run_time=0.4)

        sub = make_subtitle("Step 3 — Gradient descent: follow the slope downhill")
        self.add(sub)

        ax = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.1, 0.2],
            x_length=6.8, y_length=3.4,
            axis_config={"color": GREY, "stroke_width": 2},
            tips=False,
        ).shift(RIGHT * 0.7 + DOWN * 0.25)

        x_lbl = Text("Weights (w)", font_size=19, color=GREY).next_to(ax, DOWN, buff=0.12)
        y_lbl = Text("Loss", font_size=19, color=GREY).next_to(ax, LEFT, buff=0.12)

        def loss_fn(x):
            return 0.88 * np.exp(-0.38 * x) + 0.06

        curve = ax.plot(loss_fn, x_range=[0, 10], color=RED, stroke_width=3)

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.5)
        self.play(Create(curve), run_time=0.8)

        # Rolling ball with tangent line at 3 positions
        positions = [1.0, 3.5, 7.0]
        ball = Dot(color=YELLOW, radius=0.18).move_to(ax.c2p(positions[0], loss_fn(positions[0])))
        self.add(ball)

        # Learning rate label
        lr_box = make_formula_box(r"\eta = 0.01 \ \text{(learning rate)}", color=YELLOW, width=4.5, height=0.75)
        lr_box.move_to(ax.c2p(6.5, 0.85))
        self.play(FadeIn(lr_box), run_time=0.4)

        tangent_line = None
        grad_arrow   = None
        grad_lbl     = None

        for xi in positions:
            yi  = loss_fn(xi)
            # Numerical derivative
            dx  = 0.01
            dydx = (loss_fn(xi + dx) - loss_fn(xi - dx)) / (2 * dx)

            # Tangent line spanning +-0.8 in x
            dx_span = 0.9
            x1, x2  = xi - dx_span, xi + dx_span
            y1, y2  = yi + dydx * (-dx_span), yi + dydx * dx_span

            new_tangent = Line(
                ax.c2p(x1, y1), ax.c2p(x2, y2),
                color=YELLOW, stroke_width=2.5,
            )
            # Gradient arrow pointing in descent direction
            arrow_dx = -0.6 * np.sign(dydx)
            new_arrow = Arrow(
                ax.c2p(xi, yi),
                ax.c2p(xi + arrow_dx, yi + dydx * arrow_dx * 0.5),
                color=GREEN, buff=0,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.35,
            )
            grad_str  = f"grad = {dydx:.2f}"
            new_lbl   = Text(grad_str, font_size=18, color=GREEN).next_to(new_arrow, DOWN, buff=0.12)

            anims = [ball.animate.move_to(ax.c2p(xi, yi))]
            if tangent_line:
                anims += [ReplacementTransform(tangent_line, new_tangent)]
            else:
                anims += [Create(new_tangent)]
            if grad_arrow:
                anims += [ReplacementTransform(grad_arrow, new_arrow),
                           ReplacementTransform(grad_lbl,  new_lbl)]
            else:
                anims += [GrowArrow(new_arrow), FadeIn(new_lbl)]

            self.play(*anims, run_time=0.9)
            self.wait(0.55)
            tangent_line = new_tangent
            grad_arrow   = new_arrow
            grad_lbl     = new_lbl

        # Update rule formula
        update_box = make_formula_box(
            r"w \leftarrow w - \eta \cdot \nabla L",
            color=BLUE, width=4.8, height=0.85,
        )
        update_box.move_to(ax.c2p(5.5, 0.62))
        self.play(FadeIn(update_box), run_time=0.5)
        self.wait(1.4)

        self.play(
            FadeOut(VGroup(ax, curve, ball, x_lbl, y_lbl,
                           tangent_line, grad_arrow, grad_lbl,
                           lr_box, update_box, sub)),
            self._net_all.animate.scale(1 / 0.40).move_to(ORIGIN),
            run_time=0.5,
        )

    # ─────────────────────────────────────────────────────────────
    # SCENE 5 — Backprop: error flows backwards  (~7 s)
    # ─────────────────────────────────────────────────────────────
    def scene_backprop(self):
        sub = make_subtitle("Backprop: chain rule sends gradients BACKWARDS through layers")
        self.add(sub)

        all_edges = self._edges.submobjects
        n_l0l1    = len(self._all_nodes[0]) * len(self._all_nodes[1])
        l1l2_edges = all_edges[n_l0l1:]
        l0l1_edges = all_edges[:n_l0l1]

        # Gradient magnitude colours: stronger near output, weaker toward input
        grad_colors_back = [RED, ORANGE, YELLOW]

        # Output node pulses red (large gradient)
        out_node = self._all_nodes[2][0]
        self.play(out_node.animate.set_fill(RED, opacity=0.7), run_time=0.25)

        # Wave backward: output->hidden
        flash_back_1 = []
        for e in l1l2_edges:
            flash_back_1.append(
                ShowPassingFlash(
                    e.copy().set_color(RED).set_stroke(width=5),
                    time_width=0.55,
                    run_time=0.85,
                )
            )
        self.play(LaggedStart(*flash_back_1, lag_ratio=0.15))

        # Hidden nodes glow orange (smaller gradient)
        for node in self._all_nodes[1]:
            self.play(node.animate.set_fill(ORANGE, opacity=0.45), run_time=0.1)

        # Wave backward: hidden->input
        flash_back_2 = []
        for e in l0l1_edges:
            flash_back_2.append(
                ShowPassingFlash(
                    e.copy().set_color(ORANGE).set_stroke(width=4),
                    time_width=0.55,
                    run_time=0.85,
                )
            )
        self.play(LaggedStart(*flash_back_2, lag_ratio=0.10))

        # Input nodes glow yellow (smallest gradient)
        for node in self._all_nodes[0]:
            self.play(node.animate.set_fill(YELLOW, opacity=0.35), run_time=0.1)

        # Gradient magnitude legend
        legend_items = [
            ("Large gradient",  RED),
            ("Medium gradient", ORANGE),
            ("Small gradient",  YELLOW),
        ]
        legend_group = VGroup()
        for txt, col in legend_items:
            dot  = Dot(color=col, radius=0.14)
            lbl  = Text(txt, font_size=20, color=col)
            row  = VGroup(dot, lbl).arrange(RIGHT, buff=0.18)
            legend_group.add(row)
        legend_group.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        legend_group.to_corner(UR, buff=0.5)

        self.play(FadeIn(legend_group), run_time=0.5)
        self.wait(1.5)

        # Chain rule annotation
        chain_box = make_formula_box(
            r"\frac{\partial L}{\partial w} = \frac{\partial L}{\partial z} \cdot \frac{\partial z}{\partial w}",
            color=PURPLE, width=6.0, height=0.95,
        )
        chain_box.move_to(UP * 2.8)
        self.play(FadeIn(chain_box), run_time=0.5)
        self.wait(1.2)

        # Reset fills
        self.play(FadeOut(VGroup(legend_group, chain_box, sub)), run_time=0.35)
        for row in self._all_nodes:
            for node in row:
                node.set_fill(BG, opacity=1)

    # ─────────────────────────────────────────────────────────────
    # SCENE 6 — Weight update with actual numbers  (~6 s)
    # ─────────────────────────────────────────────────────────────
    def scene_weight_update(self):
        sub = make_subtitle("Step 4 — Update every weight: w = w - lr * gradient")
        self.add(sub)

        all_edges_list = self._edges.submobjects
        target_edge    = all_edges_list[2]

        highlight = target_edge.copy().set_color(YELLOW).set_stroke(width=5)
        self.play(Create(highlight), run_time=0.35)

        # Show the update equation with real numbers filling in
        eq1 = MathTex(r"w = w - \eta \cdot \frac{\partial L}{\partial w}",
                      font_size=34, color=WHITE).move_to(UP * 2.5)
        self.play(Write(eq1), run_time=0.6)

        eq2 = MathTex(r"w = -0.42 - 0.01 \times 7.1",
                      font_size=32, color=BLUE).next_to(eq1, DOWN, buff=0.28)
        self.play(FadeIn(eq2, shift=DOWN * 0.1), run_time=0.5)

        eq3 = MathTex(r"w = -0.42 - 0.071",
                      font_size=32, color=BLUE).next_to(eq2, DOWN, buff=0.22)
        self.play(FadeIn(eq3, shift=DOWN * 0.1), run_time=0.4)

        eq4 = MathTex(r"\mathbf{w = -0.491}",
                      font_size=36, color=GREEN).next_to(eq3, DOWN, buff=0.22)
        self.play(FadeIn(eq4, scale=1.1), run_time=0.4)

        # Animate weight label on the edge changing
        old_w = Text("-0.42", font_size=20, color=ORANGE).move_to(target_edge.get_center() + UP * 0.25)
        new_w = Text("-0.49", font_size=20, color=GREEN,  weight=BOLD).move_to(target_edge.get_center() + UP * 0.25)
        self.play(FadeIn(old_w), run_time=0.3)
        self.wait(0.5)
        self.play(ReplacementTransform(old_w, new_w), run_time=0.4)
        self.wait(1.4)

        self.play(
            FadeOut(VGroup(eq1, eq2, eq3, eq4, highlight, new_w, sub)),
            run_time=0.35,
        )

    # ─────────────────────────────────────────────────────────────
    # SCENE 7 — Convergence: epoch 1 vs epoch 1000  (~6 s)
    # ─────────────────────────────────────────────────────────────
    def scene_convergence(self):
        self.play(FadeOut(self._net_all), run_time=0.35)

        sub = make_subtitle("After millions of updates — predictions get sharper")
        self.add(sub)

        def make_scatter(ax, points, color, label_tex, epoch_str):
            dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.10, color=color)
                            for x, y in points])
            # ideal line y=x
            ideal = ax.plot(lambda x: x, x_range=[0, 1], color=GREY,
                            stroke_width=1.5, stroke_opacity=0.5)
            title = Text(epoch_str, font_size=20, color=color, weight=BOLD)
            title.next_to(ax, UP, buff=0.15)
            lbl = MathTex(label_tex, font_size=22, color=GREY)
            lbl.next_to(ax, DOWN, buff=0.12)
            return VGroup(dots, ideal, title, lbl)

        # Epoch 1: scattered predictions
        np.random.seed(7)
        xs_true = np.linspace(0.1, 0.9, 8)
        ep1_preds = np.clip(xs_true + np.random.uniform(-0.35, 0.35, 8), 0.05, 0.95)
        ep1000_preds = np.clip(xs_true + np.random.uniform(-0.06, 0.06, 8), 0.05, 0.95)

        ax_left = Axes(
            x_range=[0, 1, 0.5], y_range=[0, 1, 0.5],
            x_length=3.0, y_length=3.0,
            axis_config={"color": GREY, "stroke_width": 1.5, "include_tip": False},
            tips=False,
        ).shift(LEFT * 2.8 + UP * 0.1)

        ax_right = Axes(
            x_range=[0, 1, 0.5], y_range=[0, 1, 0.5],
            x_length=3.0, y_length=3.0,
            axis_config={"color": GREY, "stroke_width": 1.5, "include_tip": False},
            tips=False,
        ).shift(RIGHT * 2.8 + UP * 0.1)

        sc_left  = make_scatter(ax_left,  list(zip(xs_true, ep1_preds)),    RED,   r"y_{\text{true}}\ \text{vs}\ \hat{y}", "Epoch 1  |  Loss: 0.34")
        sc_right = make_scatter(ax_right, list(zip(xs_true, ep1000_preds)), GREEN, r"y_{\text{true}}\ \text{vs}\ \hat{y}", "Epoch 1000  |  Loss: 0.003")

        divider = DashedLine(UP * 2.5, DOWN * 2.5, color=GREY,
                             stroke_width=1.5, stroke_opacity=0.45)

        self.play(Create(ax_left), Create(ax_right), Create(divider), run_time=0.5)
        self.play(FadeIn(sc_left), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(sc_right), run_time=0.6)
        self.wait(2.0)

        self.play(FadeOut(VGroup(ax_left, ax_right, sc_left, sc_right, divider, sub)), run_time=0.4)

    # ─────────────────────────────────────────────────────────────
    # SCENE 8 — Payoff: loop + loss counter + final card  (~5 s)
    # ─────────────────────────────────────────────────────────────
    def scene_payoff(self):
        sub = make_subtitle("4 steps. Repeated. That is the entire training algorithm.")
        self.add(sub)

        steps       = ["Forward", "Loss", "Backprop", "Update"]
        step_colors = [GREEN, RED, PURPLE, BLUE]
        boxes = []
        for s, col in zip(steps, step_colors):
            rect  = RoundedRectangle(corner_radius=0.16, width=2.3, height=0.72,
                                     fill_color=col, fill_opacity=0.16,
                                     stroke_color=col, stroke_width=2)
            label = Text(s, font_size=22, color=col)
            label.move_to(rect.get_center())
            boxes.append(VGroup(rect, label))

        boxes[0].move_to(LEFT  * 1.4 + UP   * 1.0)
        boxes[1].move_to(RIGHT * 1.4 + UP   * 1.0)
        boxes[2].move_to(RIGHT * 1.4 + DOWN * 0.45)
        boxes[3].move_to(LEFT  * 1.4 + DOWN * 0.45)

        a1 = Arrow(boxes[0].get_right(), boxes[1].get_left(), color=GREY, buff=0.08,
                   stroke_width=2, max_tip_length_to_length_ratio=0.22)
        a2 = Arrow(boxes[1].get_bottom(), boxes[2].get_top(), color=GREY, buff=0.08,
                   stroke_width=2, max_tip_length_to_length_ratio=0.22)
        a3 = Arrow(boxes[2].get_left(), boxes[3].get_right(), color=GREY, buff=0.08,
                   stroke_width=2, max_tip_length_to_length_ratio=0.22)
        a4 = Arrow(boxes[3].get_top(), boxes[0].get_bottom(), color=GREY, buff=0.08,
                   stroke_width=2, max_tip_length_to_length_ratio=0.22)

        all_boxes   = VGroup(*boxes)
        all_arrows  = VGroup(a1, a2, a3, a4)

        # Live loss counter
        loss_vals = [0.340, 0.185, 0.072, 0.018, 0.003]
        loss_counter = Text(f"Loss: {loss_vals[0]:.3f}", font_size=28,
                            color=RED, weight=BOLD).move_to(DOWN * 2.0)

        self.play(
            LaggedStart(*[FadeIn(b, shift=UP * 0.12) for b in boxes], lag_ratio=0.12),
            run_time=0.8,
        )
        self.play(
            LaggedStart(*[Create(a) for a in [a1, a2, a3, a4]], lag_ratio=0.12),
            run_time=0.6,
        )
        self.add(loss_counter)

        # Cycle highlight around the loop 3 times, updating loss
        for cycle in range(3):
            for bi, box in enumerate(boxes):
                new_loss_idx = min(cycle * 4 + bi + 1, len(loss_vals) - 1)
                highlight = box[0].copy().set_stroke(color=YELLOW, width=4).set_fill(opacity=0.35)
                new_counter = Text(f"Loss: {loss_vals[new_loss_idx]:.3f}",
                                   font_size=28, color=RED, weight=BOLD).move_to(DOWN * 2.0)
                self.play(
                    FadeIn(highlight), run_time=0.13,
                )
                self.play(
                    FadeOut(highlight),
                    ReplacementTransform(loss_counter, new_counter),
                    run_time=0.18,
                )
                loss_counter = new_counter

        self.wait(0.5)
        self.play(FadeOut(VGroup(all_boxes, all_arrows, loss_counter, sub)), run_time=0.4)

        # Final punch card
        final  = Text("No magic.", font_size=58, color=YELLOW, weight=BOLD)
        line2  = Text("Just 4 operations.", font_size=36, color=WHITE)
        line3  = Text("Repeated until it works.", font_size=30, color=BLUE)
        vg_end = VGroup(final, line2, line3).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        sub2   = make_subtitle("Follow for more data science explained visually")

        self.play(FadeIn(final, scale=1.12), run_time=0.45)
        self.play(FadeIn(line2), run_time=0.35)
        self.play(FadeIn(line3), run_time=0.35)
        self.add(sub2)
        self.wait(2.5)
        self.play(FadeOut(VGroup(vg_end, sub2)), run_time=0.4)
