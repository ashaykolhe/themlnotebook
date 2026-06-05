from manim import *

# ── Colour palette ──────────────────────────────────────────────────────────
BG        = "#0d0f14"
BLUE      = "#4f9eff"
ORANGE    = "#f97316"
GREEN     = "#10b981"
YELLOW    = "#fbbf24"
RED       = "#f87171"
PURPLE    = "#a855f7"
GREY      = "#3a3f4b"
WHITE_TXT = "#e8eaf0"
DIM_TXT   = "#7b8394"

# ── Subtitle helper ──────────────────────────────────────────────────────────
def make_subtitle(line1, line2=""):
    """One or two line subtitle pinned to bottom of frame."""
    items = [line1]
    if line2:
        items.append(line2)
    texts = VGroup(*[
        Text(t, font="Arial", font_size=21, color=WHITE_TXT if i == 0 else DIM_TXT)
        for i, t in enumerate(items)
    ]).arrange(DOWN, buff=0.10)
    texts.set_width(min(texts.width, config.frame_width - 0.7))
    bg = RoundedRectangle(
        corner_radius=0.13,
        width=texts.width + 0.55,
        height=texts.height + 0.32,
        fill_color="#0a0c10",
        fill_opacity=0.92,
        stroke_width=0,
    )
    group = VGroup(bg, texts).arrange(ORIGIN)
    group.to_edge(DOWN, buff=0.20)
    return group


# ── Node / leaf factories ────────────────────────────────────────────────────
def make_node(line1, line2="", color=BLUE, width=2.6, height=0.70, font_size=20):
    box = RoundedRectangle(
        corner_radius=0.15, width=width, height=height,
        fill_color=color, fill_opacity=0.16,
        stroke_color=color, stroke_width=2.2,
    )
    if line2:
        t1 = Text(line1, font="Arial", font_size=font_size,     color=color)
        t2 = Text(line2, font="Arial", font_size=font_size - 3, color=color)
        label = VGroup(t1, t2).arrange(DOWN, buff=0.05)
    else:
        label = Text(line1, font="Arial", font_size=font_size, color=color)
    label.set_width(min(label.width, width - 0.22))
    return VGroup(box, label).arrange(ORIGIN)


def make_leaf(text, color, font_size=19):
    box = RoundedRectangle(
        corner_radius=0.16, width=2.1, height=0.65,
        fill_color=color, fill_opacity=0.30,
        stroke_color=color, stroke_width=2.5,
    )
    label = Text(text, font="Arial", font_size=font_size, color=color)
    label.set_width(min(label.width, 1.9))
    return VGroup(box, label).arrange(ORIGIN)


def make_edge(start_mob, end_mob, label_text="", color=GREY):
    start = start_mob.get_bottom()
    end   = end_mob.get_top()
    arr = Arrow(
        start, end, buff=0.08,
        stroke_color=color, stroke_width=2.0,
        max_tip_length_to_length_ratio=0.18, color=color,
    )
    group = VGroup(arr)
    if label_text:
        mid = (start + end) / 2
        lbl = Text(label_text, font="Arial", font_size=16, color=color)
        lbl.move_to(mid + LEFT * 0.42)
        group.add(lbl)
    return group


def make_bar(label, frac, color, width=1.6, height=0.32):
    """Small horizontal progress bar with label."""
    bg   = Rectangle(width=width, height=height,
                     fill_color=GREY, fill_opacity=0.35, stroke_width=0)
    fill = Rectangle(width=width * frac, height=height,
                     fill_color=color, fill_opacity=0.85, stroke_width=0)
    fill.align_to(bg, LEFT)
    lbl = Text(label, font="Arial", font_size=16, color=DIM_TXT)
    lbl.next_to(bg, LEFT, buff=0.18)
    pct = Text(f"{int(frac*100)}%", font="Arial", font_size=16, color=color)
    pct.next_to(bg, RIGHT, buff=0.14)
    return VGroup(bg, fill, lbl, pct)


# ════════════════════════════════════════════════════════════════════════════
class DecisionTreeShort(Scene):
    """
    YouTube Short – 9:16
    Scenes:
      1. Hook
      2. What is a feature? (data table)
      3. How the tree picks the best split (Gini impurity concept)
      4. Building the tree live – root + two child nodes
      5. Tracing a real example through the tree
      6. Gini impurity score shown numerically
      7. Overfitting warning
      8. Outro / takeaway
    """

    def construct(self):
        self.camera.background_color = BG

        # ════════════════════════════════════════════════════════════════
        # SCENE 1 – HOOK
        # ════════════════════════════════════════════════════════════════
        h1 = Text("Your brain uses", font="Arial",
                  font_size=44, color=WHITE_TXT, weight=BOLD).move_to(UP * 1.5)
        h2 = Text("decision trees daily.", font="Arial",
                  font_size=44, color=BLUE, weight=BOLD).next_to(h1, DOWN, buff=0.14)
        h3 = Text("Here is the math behind it.", font="Arial",
                  font_size=28, color=DIM_TXT).next_to(h2, DOWN, buff=0.38)

        sub = make_subtitle("A decision tree splits data using yes/no questions.",
                            "Each split is chosen to be as pure as possible.")
        self.play(FadeIn(h1, shift=UP * 0.25), run_time=0.5)
        self.play(FadeIn(h2, shift=UP * 0.20), run_time=0.45)
        self.play(FadeIn(h3), run_time=0.4)
        self.play(FadeIn(sub), run_time=0.35)
        self.wait(2.0)
        self.play(FadeOut(h1), FadeOut(h2), FadeOut(h3), FadeOut(sub), run_time=0.4)

        # ════════════════════════════════════════════════════════════════
        # SCENE 2 – FEATURES TABLE
        # ════════════════════════════════════════════════════════════════
        sub2 = make_subtitle("The model receives a row of features per applicant.",
                             "It must predict: Approved or Rejected?")

        # header
        headers = ["Age", "Income", "History", "Label"]
        h_colors = [BLUE, ORANGE, GREEN, PURPLE]
        rows_data = [
            ("34", "$45k", "Good",  "?"),
            ("22", "$28k", "Poor",  "?"),
            ("45", "$80k", "Good",  "?"),
            ("29", "$52k", "Fair",  "?"),
        ]

        col_w = 1.28
        row_h = 0.42
        table_top = UP * 2.4

        header_row = VGroup()
        for i, (h, c) in enumerate(zip(headers, h_colors)):
            cell_bg = Rectangle(width=col_w, height=row_h,
                                fill_color=c, fill_opacity=0.18,
                                stroke_color=c, stroke_width=1.2)
            cell_lbl = Text(h, font="Arial", font_size=18, color=c)
            cell = VGroup(cell_bg, cell_lbl).arrange(ORIGIN)
            cell.move_to(LEFT * (1.5 * col_w) + RIGHT * (i * col_w) + table_top)
            header_row.add(cell)

        data_rows = VGroup()
        for r_idx, row in enumerate(rows_data):
            row_group = VGroup()
            for c_idx, (val, col) in enumerate(zip(row, [BLUE, ORANGE, GREEN, PURPLE])):
                c = WHITE_TXT if c_idx < 3 else YELLOW
                cell_bg = Rectangle(width=col_w, height=row_h,
                                    fill_color=BG, fill_opacity=0,
                                    stroke_color=GREY, stroke_width=0.6)
                cell_lbl = Text(val, font="Arial", font_size=17, color=c)
                cell = VGroup(cell_bg, cell_lbl).arrange(ORIGIN)
                cell.move_to(
                    LEFT * (1.5 * col_w) + RIGHT * (c_idx * col_w) +
                    table_top + DOWN * (row_h * (r_idx + 1))
                )
                row_group.add(cell)
            data_rows.add(row_group)

        self.play(FadeIn(sub2), FadeIn(header_row), run_time=0.5)
        self.play(LaggedStart(
            *[FadeIn(r, shift=DOWN * 0.1) for r in data_rows],
            lag_ratio=0.18
        ), run_time=0.9)
        self.wait(1.8)

        # highlight the question marks
        q_marks = VGroup(*[r[-1] for r in data_rows])
        self.play(q_marks.animate.set_color(YELLOW), run_time=0.4)
        self.wait(0.8)
        self.play(FadeOut(sub2), FadeOut(header_row), FadeOut(data_rows), run_time=0.4)

        # ════════════════════════════════════════════════════════════════
        # SCENE 3 – GINI IMPURITY CONCEPT
        # ════════════════════════════════════════════════════════════════
        # Custom subtitle: top line plain text, bottom line proper LaTeX formula
        sub3_line1 = Text(
            "The tree picks the split with lowest Gini Impurity.",
            font="Arial", font_size=21, color=WHITE_TXT,
        )
        sub3_line2 = MathTex(
            r"\text{Gini} = 1 - (p_{\text{yes}}^{2} + p_{\text{no}}^{2})"
            r"\quad [0 = \text{pure},\ 0.5 = \text{worst}]",
            font_size=22, color=DIM_TXT,
        )
        sub3_lines = VGroup(sub3_line1, sub3_line2).arrange(DOWN, buff=0.12)
        sub3_lines.set_width(min(sub3_lines.width, config.frame_width - 0.7))
        sub3_bg = RoundedRectangle(
            corner_radius=0.13,
            width=sub3_lines.width + 0.55,
            height=sub3_lines.height + 0.32,
            fill_color="#0a0c10", fill_opacity=0.92, stroke_width=0,
        )
        sub3 = VGroup(sub3_bg, sub3_lines).arrange(ORIGIN)
        sub3.to_edge(DOWN, buff=0.20)

        title3 = Text("What is Gini Impurity?", font="Arial",
                      font_size=30, color=BLUE, weight=BOLD).move_to(UP * 2.8)

        # two buckets: impure vs pure
        impure_label = Text("Before split", font="Arial", font_size=19, color=DIM_TXT)
        pure_label   = Text("After split",  font="Arial", font_size=19, color=DIM_TXT)

        # dots representing class labels  G = green approved  R = red rejected
        def dot_grid(pattern, cols=5):
            dots = VGroup()
            for i, c in enumerate(pattern):
                d = Circle(radius=0.12,
                           fill_color=GREEN if c == "G" else RED,
                           fill_opacity=0.85, stroke_width=0)
                dots.add(d)
            dots.arrange_in_grid(rows=2, cols=cols, buff=0.10)
            return dots

        impure_dots = dot_grid(["G","R","G","R","G","R","G","R","G","R"])
        impure_box  = SurroundingRectangle(impure_dots, color=GREY,
                                           corner_radius=0.12, buff=0.18)
        impure_gini = Text("Gini = 0.50  (worst)", font="Arial",
                           font_size=17, color=RED)
        impure_grp  = VGroup(impure_label, impure_box, impure_dots, impure_gini)
        impure_label.move_to(UP * 1.4 + LEFT * 2.4)
        impure_dots.move_to(UP * 0.5 + LEFT * 2.4)
        impure_box.move_to(impure_dots.get_center())
        impure_gini.next_to(impure_box, DOWN, buff=0.14)

        pure_dots_left  = dot_grid(["G","G","G","G","G","G","G","G","G","G"])
        pure_dots_right = dot_grid(["R","R","R","R","R","R","R","R","R","R"])
        pure_box_l = SurroundingRectangle(pure_dots_left,  color=GREEN,
                                          corner_radius=0.12, buff=0.14)
        pure_box_r = SurroundingRectangle(pure_dots_right, color=RED,
                                          corner_radius=0.12, buff=0.14)
        pure_gini  = Text("Gini = 0.00  (best)", font="Arial",
                          font_size=17, color=GREEN)
        pure_label.move_to(UP * 1.4 + RIGHT * 2.0)
        pure_dots_left.move_to(UP * 0.5 + RIGHT * 1.2)
        pure_box_l.move_to(pure_dots_left.get_center())
        pure_dots_right.move_to(UP * 0.5 + RIGHT * 2.9)
        pure_box_r.move_to(pure_dots_right.get_center())
        pure_gini.next_to(VGroup(pure_box_l, pure_box_r), DOWN, buff=0.14)

        arrow_split = Arrow(LEFT * 0.4, RIGHT * 0.4,
                            color=YELLOW, stroke_width=2.5,
                            max_tip_length_to_length_ratio=0.25)
        split_lbl = Text("split", font="Arial", font_size=16, color=YELLOW)
        split_lbl.next_to(arrow_split, UP, buff=0.06)
        arrow_split.move_to(UP * 0.5)
        split_lbl.move_to(UP * 0.88)

        self.play(FadeIn(sub3), FadeIn(title3), run_time=0.45)
        self.play(
            FadeIn(impure_label), FadeIn(impure_box),
            FadeIn(impure_dots),  FadeIn(impure_gini),
            run_time=0.6
        )
        self.wait(1.0)
        self.play(GrowArrow(arrow_split), FadeIn(split_lbl), run_time=0.5)
        self.play(
            FadeIn(pure_label),
            FadeIn(pure_box_l), FadeIn(pure_dots_left),
            FadeIn(pure_box_r), FadeIn(pure_dots_right),
            FadeIn(pure_gini),
            run_time=0.7
        )
        self.wait(2.0)
        self.play(
            FadeOut(title3), FadeOut(sub3),
            FadeOut(impure_grp),
            FadeOut(arrow_split), FadeOut(split_lbl),
            FadeOut(pure_label), FadeOut(pure_box_l), FadeOut(pure_dots_left),
            FadeOut(pure_box_r), FadeOut(pure_dots_right), FadeOut(pure_gini),
            run_time=0.4
        )

        # ════════════════════════════════════════════════════════════════
        # SCENE 4 – BUILD THE TREE
        # ════════════════════════════════════════════════════════════════
        sub4 = make_subtitle("Root split: Age > 30 gives the lowest Gini.",
                             "So the tree starts by asking about Age.")

        root = make_node("Age > 30?", "Root Node", color=BLUE, width=2.7, height=0.80)
        root.move_to(UP * 3.0)

        gini_root = Text("Gini before: 0.50", font="Arial", font_size=16, color=DIM_TXT)
        gini_root.next_to(root, RIGHT, buff=0.3)

        self.play(FadeIn(sub4), GrowFromCenter(root), run_time=0.6)
        self.play(FadeIn(gini_root), run_time=0.3)
        self.wait(1.2)

        # child nodes
        child_yes = make_node("Income > $50k?", "n=62 samples", color=ORANGE, width=2.7, height=0.80)
        child_no  = make_node("Credit Score?",  "n=38 samples", color=PURPLE, width=2.7, height=0.80)
        child_yes.move_to(LEFT * 2.6 + UP * 1.0)
        child_no.move_to(RIGHT * 2.6 + UP * 1.0)

        arr_yes = make_edge(root, child_yes, "YES", GREEN)
        arr_no  = make_edge(root, child_no,  "NO",  RED)

        gini_yes = Text("Gini: 0.31", font="Arial", font_size=15, color=ORANGE)
        gini_no  = Text("Gini: 0.38", font="Arial", font_size=15, color=PURPLE)
        gini_yes.next_to(child_yes, DOWN, buff=0.10)
        gini_no.next_to(child_no,  DOWN, buff=0.10)

        self.play(FadeOut(sub4), run_time=0.2)
        sub4b = make_subtitle("Each child node gets a new feature to split on.",
                              "The tree keeps splitting until nodes are pure.")
        self.play(FadeIn(sub4b), run_time=0.3)
        self.play(
            LaggedStart(GrowArrow(arr_yes[0]), GrowArrow(arr_no[0]), lag_ratio=0.3),
            run_time=0.6
        )
        if len(arr_yes) > 1: self.play(FadeIn(arr_yes[1]), FadeIn(arr_no[1]), run_time=0.25)
        self.play(GrowFromCenter(child_yes), GrowFromCenter(child_no), run_time=0.6)
        self.play(FadeIn(gini_yes), FadeIn(gini_no), run_time=0.35)
        self.wait(1.6)
        self.play(FadeOut(sub4b), FadeOut(gini_root), FadeOut(gini_yes), FadeOut(gini_no), run_time=0.3)

        # ════════════════════════════════════════════════════════════════
        # SCENE 5 – LEAVES
        # ════════════════════════════════════════════════════════════════
        sub5 = make_subtitle("Leaf nodes hold the final class prediction.",
                             "No more splits — just an answer.")

        leaf_yy = make_leaf("APPROVED", GREEN)
        leaf_yn = make_leaf("REJECTED", RED)
        leaf_ny = make_leaf("APPROVED", GREEN)
        leaf_nn = make_leaf("REJECTED", RED)

        leaf_yy.move_to(LEFT * 3.8 + DOWN * 0.65)
        leaf_yn.move_to(LEFT * 1.4 + DOWN * 0.65)
        leaf_ny.move_to(RIGHT * 1.4 + DOWN * 0.65)
        leaf_nn.move_to(RIGHT * 3.8 + DOWN * 0.65)

        conf_yy = Text("conf: 91%", font="Arial", font_size=14, color=GREEN)
        conf_yn = Text("conf: 78%", font="Arial", font_size=14, color=RED)
        conf_ny = Text("conf: 84%", font="Arial", font_size=14, color=GREEN)
        conf_nn = Text("conf: 95%", font="Arial", font_size=14, color=RED)
        for conf, leaf in zip([conf_yy, conf_yn, conf_ny, conf_nn],
                              [leaf_yy, leaf_yn, leaf_ny, leaf_nn]):
            conf.next_to(leaf, DOWN, buff=0.08)

        arr_yy = make_edge(child_yes, leaf_yy, "YES", GREEN)
        arr_yn = make_edge(child_yes, leaf_yn, "NO",  RED)
        arr_ny = make_edge(child_no,  leaf_ny, "YES", GREEN)
        arr_nn = make_edge(child_no,  leaf_nn, "NO",  RED)

        self.play(FadeIn(sub5), run_time=0.3)
        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(arr_yy[0]), GrowArrow(arr_yn[0])),
                AnimationGroup(GrowArrow(arr_ny[0]), GrowArrow(arr_nn[0])),
                lag_ratio=0.3
            ), run_time=0.8
        )
        for arr in [arr_yy, arr_yn, arr_ny, arr_nn]:
            if len(arr) > 1: self.add(arr[1])
        self.play(
            LaggedStart(
                GrowFromCenter(leaf_yy), GrowFromCenter(leaf_yn),
                GrowFromCenter(leaf_ny), GrowFromCenter(leaf_nn),
                lag_ratio=0.2
            ), run_time=0.7
        )
        self.play(
            FadeIn(conf_yy), FadeIn(conf_yn),
            FadeIn(conf_ny), FadeIn(conf_nn),
            run_time=0.4
        )
        self.wait(1.4)
        self.play(FadeOut(sub5), run_time=0.3)

        # ════════════════════════════════════════════════════════════════
        # SCENE 6 – TRACE EXAMPLE PERSON
        # ════════════════════════════════════════════════════════════════
        sub6 = make_subtitle("Person: Age 34, Income $45k, Credit Poor.",
                             "Watch how the tree routes the prediction.")

        # dim everything first, then highlight path
        all_tree = VGroup(
            root, arr_yes, arr_no, child_yes, child_no,
            arr_yy, arr_yn, arr_ny, arr_nn,
            leaf_yy, leaf_yn, leaf_ny, leaf_nn,
            conf_yy, conf_yn, conf_ny, conf_nn,
        )
        self.play(FadeIn(sub6), all_tree.animate.set_opacity(0.22), run_time=0.5)

        # step 1 – root
        self.play(root.animate.set_opacity(1.0), run_time=0.35)
        step1 = Text("34 > 30?  YES", font="Arial", font_size=20, color=GREEN)
        step1.next_to(root, RIGHT, buff=0.3)
        self.play(FadeIn(step1), run_time=0.3)
        self.wait(0.6)

        # step 2 – yes branch
        self.play(arr_yes.animate.set_opacity(1.0), child_yes.animate.set_opacity(1.0), run_time=0.4)
        step2 = Text("$45k > $50k?  NO", font="Arial", font_size=20, color=RED)
        step2.next_to(child_yes, RIGHT, buff=0.3)
        self.play(FadeIn(step2), run_time=0.3)
        self.wait(0.6)

        # step 3 – rejected leaf
        self.play(arr_yn.animate.set_opacity(1.0), leaf_yn.animate.set_opacity(1.0),
                  conf_yn.animate.set_opacity(1.0), run_time=0.4)
        self.play(
            leaf_yn[0].animate.set_fill(RED, opacity=0.65),
            leaf_yn[0].animate.set_stroke(RED, width=3.5),
            run_time=0.5
        )
        self.wait(1.2)
        self.play(
            FadeOut(step1), FadeOut(step2), FadeOut(sub6),
            all_tree.animate.set_opacity(1.0),
            run_time=0.4
        )

        # ════════════════════════════════════════════════════════════════
        # SCENE 7 – OVERFITTING WARNING
        # ════════════════════════════════════════════════════════════════
        tree_all = VGroup(
            root, arr_yes, arr_no, child_yes, child_no,
            arr_yy, arr_yn, arr_ny, arr_nn,
            leaf_yy, leaf_yn, leaf_ny, leaf_nn,
            conf_yy, conf_yn, conf_ny, conf_nn,
        )
        self.play(FadeOut(tree_all), run_time=0.4)

        sub7 = make_subtitle("Danger: too many splits = overfitting.",
                             "The tree memorises noise, not patterns.")

        warn_title = Text("Overfitting", font="Arial",
                          font_size=38, color=RED, weight=BOLD).move_to(UP * 2.5)

        # two bar comparisons: train acc vs test acc
        bar_train = make_bar("Train acc", 0.99, GREEN, width=2.2)
        bar_test  = make_bar("Test acc",  0.61, RED,   width=2.2)
        bars = VGroup(bar_train, bar_test).arrange(DOWN, buff=0.38)
        bars.move_to(UP * 1.2)

        fix_label = Text("Fix: set max_depth or min_samples_leaf",
                         font="Arial", font_size=19, color=YELLOW)
        fix_label.move_to(DOWN * 0.1)

        code_bg = RoundedRectangle(
            corner_radius=0.14, width=5.6, height=0.56,
            fill_color="#161b22", fill_opacity=1.0, stroke_color=GREY, stroke_width=1.2
        )
        code_txt = Text("DecisionTreeClassifier(max_depth=4)",
                        font="Courier New", font_size=16, color=GREEN)
        code_mob = VGroup(code_bg, code_txt).arrange(ORIGIN).next_to(fix_label, DOWN, buff=0.28)

        self.play(FadeIn(sub7), FadeIn(warn_title), run_time=0.45)
        self.play(FadeIn(bar_train), FadeIn(bar_test), run_time=0.6)
        self.wait(1.0)
        self.play(FadeIn(fix_label), GrowFromCenter(code_mob), run_time=0.55)
        self.wait(1.8)
        self.play(
            FadeOut(warn_title), FadeOut(bars),
            FadeOut(fix_label), FadeOut(code_mob), FadeOut(sub7),
            run_time=0.4
        )

        # ════════════════════════════════════════════════════════════════
        # SCENE 8 – OUTRO
        # ════════════════════════════════════════════════════════════════
        sub8 = make_subtitle("Decision trees: interpretable, fast, powerful.",
                             "Base for Random Forests and XGBoost.")

        bullets = [
            ("Split by lowest Gini Impurity",    BLUE),
            ("Recurse until leaves are pure",     GREEN),
            ("Limit depth to avoid overfitting",  YELLOW),
            ("Ensemble: combine many trees",      PURPLE),
        ]
        bul_group = VGroup()
        for text, color in bullets:
            dot  = Circle(radius=0.07, fill_color=color, fill_opacity=1, stroke_width=0)
            line = Text(text, font="Arial", font_size=22, color=WHITE_TXT)
            row  = VGroup(dot, line).arrange(RIGHT, buff=0.22)
            bul_group.add(row)
        bul_group.arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        bul_group.move_to(UP * 1.3)

        cta = Text("Follow for more data science!", font="Arial",
                   font_size=22, color=DIM_TXT).next_to(bul_group, DOWN, buff=0.55)

        self.play(FadeIn(sub8), run_time=0.3)
        self.play(LaggedStart(
            *[FadeIn(r, shift=RIGHT * 0.18) for r in bul_group],
            lag_ratio=0.22
        ), run_time=1.1)
        self.play(FadeIn(cta), run_time=0.4)
        self.wait(2.4)
        self.play(FadeOut(bul_group), FadeOut(cta), FadeOut(sub8), run_time=0.5)
