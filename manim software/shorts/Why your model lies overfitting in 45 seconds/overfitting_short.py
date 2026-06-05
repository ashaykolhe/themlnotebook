from manim import *

# ─────────────────────────────────────────────
#  Colour palette
# ─────────────────────────────────────────────
BG     = "#0d0f14"
BLUE   = "#4f9eff"
ORANGE = "#f97316"
GREEN  = "#10b981"
RED    = "#f87171"
YELLOW = "#fbbf24"
PURPLE = "#a855f7"
LGRAY  = "#8899aa"


class OverfittingShort(Scene):

    _sub = None

    def show_sub(self, text, font_size=25):
        """Fade out old subtitle, fade in new one — one subtitle on screen at a time."""
        bg = Rectangle(
            width=config.frame_width,
            height=0.80,
            fill_color="#000000",
            fill_opacity=0.75,
            stroke_width=0,
        ).to_edge(DOWN, buff=0)

        label = Text(text, font_size=font_size, color=WHITE, font="Arial")
        label.move_to(bg.get_center())
        if label.width > config.frame_width - 0.4:
            label.scale_to_fit_width(config.frame_width - 0.4)

        new_sub = VGroup(bg, label)

        if self._sub is not None:
            self.play(FadeOut(self._sub), run_time=0.22)
        self.play(FadeIn(new_sub), run_time=0.28)
        self._sub = new_sub

    def clear_sub(self):
        if self._sub is not None:
            self.play(FadeOut(self._sub), run_time=0.28)
            self._sub = None

    def construct(self):
        self.camera.background_color = BG

        # ────────────────────────────────────────────────────────
        # 0.  HOOK  (~5 s)
        #     Visual: bold 99% number + contradiction line
        #     Script: the student-who-memorised-answers analogy
        # ────────────────────────────────────────────────────────
        hook_line1 = Text("Your model scored",          font_size=36, color=WHITE,  font="Arial")
        hook_line2 = Text("99% accuracy.",              font_size=54, color=GREEN,  font="Arial", weight=BOLD)
        hook_line3 = Text("Here's why that's terrible.",font_size=32, color=RED,    font="Arial")
        hook = VGroup(hook_line1, hook_line2, hook_line3).arrange(DOWN, buff=0.28).move_to(ORIGIN)

        self.play(FadeIn(hook, shift=UP * 0.3), run_time=0.7)
        self.show_sub("99% accuracy sounds amazing -- until you test it on real data.")
        self.wait(2.2)
        self.show_sub("It's like a student who memorised the answers, not the concept.")
        self.wait(2.2)
        self.play(FadeOut(hook), run_time=0.4)

        # ────────────────────────────────────────────────────────
        # 1.  AXES  (~2 s)
        #     Script: frame the chart — what each axis means
        # ────────────────────────────────────────────────────────
        axes = Axes(
            x_range=[1, 10, 1],
            y_range=[0, 1.05, 0.25],
            x_length=8,
            y_length=4.0,
            axis_config={"color": LGRAY, "stroke_width": 2},
            tips=False,
        ).shift(UP * 0.35)

        x_label = Text("Model complexity  -->", font_size=21, color=LGRAY, font="Arial")
        x_label.next_to(axes.x_axis, DOWN, buff=0.35)

        y_label = Text("Accuracy", font_size=21, color=LGRAY, font="Arial")
        y_label.next_to(axes.y_axis, LEFT, buff=0.2).rotate(PI / 2)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.1)
        self.show_sub("More complexity = more parameters = model can fit more patterns.")
        self.wait(1.5)

        # ────────────────────────────────────────────────────────
        # 2.  TRAINING CURVE  (~5 s)
        #     Script: WHY it rises — more params always reduce
        #             training loss, even by fitting noise
        # ────────────────────────────────────────────────────────
        train_curve = axes.plot(
            lambda x: 0.50 + 0.48 * (1 - 1 / (0.9 * x + 0.5)),
            x_range=[1, 10],
            color=BLUE,
            stroke_width=4,
        )

        train_dot = Dot(color=BLUE, radius=0.10)
        train_txt = Text("Training accuracy", font_size=20, color=BLUE, font="Arial")
        train_legend = VGroup(train_dot, train_txt).arrange(RIGHT, buff=0.15)
        train_legend.to_corner(UR, buff=0.5).shift(DOWN * 0.15)

        self.play(Create(train_curve), run_time=1.6)
        self.play(FadeIn(train_legend), run_time=0.3)
        self.show_sub("Training accuracy always rises -- the model sees this data every epoch.")
        self.wait(1.8)
        self.show_sub("With enough parameters it can memorise every single training example.")
        self.wait(1.8)

        # ────────────────────────────────────────────────────────
        # 3.  TEST CURVE  (~5 s)
        #     Script: WHY it peaks then drops — generalisation
        #             breaks when the model latches onto noise
        # ────────────────────────────────────────────────────────
        def test_acc(x):
            peak    = 0.82
            rising  = 0.40 + (peak - 0.40) * (x - 1) / 3
            falling = peak - 0.055 * max(0.0, x - 4) ** 1.3
            t       = max(0.0, min(1.0, (x - 3.8) / 0.4))
            return max(0.05, (1 - t) * rising + t * falling)

        test_curve = axes.plot(test_acc, x_range=[1, 10], color=ORANGE, stroke_width=4)

        test_dot = Dot(color=ORANGE, radius=0.10)
        test_txt = Text("Test accuracy", font_size=20, color=ORANGE, font="Arial")
        test_legend = VGroup(test_dot, test_txt).arrange(RIGHT, buff=0.15)
        test_legend.next_to(train_legend, DOWN, buff=0.18, aligned_edge=LEFT)

        self.play(Create(test_curve), run_time=1.6)
        self.play(FadeIn(test_legend), run_time=0.3)
        self.show_sub("Test accuracy is different -- the model has NEVER seen this data.")
        self.wait(1.8)
        self.show_sub("It peaks, then falls. The model learned noise, not signal.")
        self.wait(1.8)

        # ────────────────────────────────────────────────────────
        # 4.  OVERFIT ZONE + UNDERFIT ZONE  (~7 s)
        #     Visual: sweet spot line, overfit shading,
        #             underfit label on the left
        #     Script: name both failure modes
        # ────────────────────────────────────────────────────────
        sweet_x = 4

        sweet_line = DashedLine(
            axes.c2p(sweet_x, 0), axes.c2p(sweet_x, 1.0),
            color=GREEN, dash_length=0.14, stroke_width=2.5,
        )
        sweet_label = Text("sweet spot", font_size=18, color=GREEN, font="Arial")
        sweet_label.next_to(sweet_line, UP, buff=0.10)

        # underfit region (left of sweet spot)
        underfit_region = axes.get_area(
            test_curve, x_range=[1, sweet_x], color=PURPLE, opacity=0.10,
        )
        underfit_label = Text("UNDERFIT", font_size=22, color=PURPLE, font="Arial", weight=BOLD)
        underfit_label.move_to(axes.c2p(2.2, 0.75))

        # overfit region (right of sweet spot)
        overfit_region = axes.get_area(
            test_curve, x_range=[sweet_x, 10], color=RED, opacity=0.13,
        )
        overfit_label = Text("OVERFIT", font_size=22, color=RED, font="Arial", weight=BOLD)
        overfit_label.move_to(axes.c2p(7.2, 0.75))

        self.play(Create(sweet_line), Write(sweet_label), run_time=0.8)
        self.play(
            FadeIn(underfit_region), Write(underfit_label),
            FadeIn(overfit_region),  Write(overfit_label),
            run_time=0.7,
        )
        self.show_sub("Left of the line: underfitting -- model too simple to learn anything.")
        self.wait(2.2)
        self.show_sub("Right of the line: overfitting -- model too complex, learns the noise.")
        self.wait(2.2)

        # ────────────────────────────────────────────────────────
        # 4.5  BIAS-VARIANCE ANNOTATION  (~4 s)
        #      Add small callout arrows on the chart
        #      Script: name the underlying tradeoff
        # ────────────────────────────────────────────────────────
        bv_title = Text("The Bias-Variance Tradeoff", font_size=22, color=YELLOW, font="Arial", weight=BOLD)
        bv_line1 = Text("Underfit  =  high bias, low variance",  font_size=19, color=PURPLE, font="Arial")
        bv_line2 = Text("Overfit   =  low bias, high variance",  font_size=19, color=RED,    font="Arial")
        bv_block = VGroup(bv_title, bv_line1, bv_line2).arrange(DOWN, buff=0.18, aligned_edge=LEFT)

        bv_bg = SurroundingRectangle(
            bv_block, color=LGRAY, stroke_width=1,
            fill_color=BG, fill_opacity=0.92,
            corner_radius=0.12, buff=0.2,
        )
        bv_card = VGroup(bv_bg, bv_block)
        bv_card.to_corner(UL, buff=0.4)

        self.play(FadeIn(bv_card, shift=DOWN * 0.15), run_time=0.6)
        self.show_sub("This is the bias-variance tradeoff -- every ML model faces it.")
        self.wait(2.0)
        self.show_sub("Goal: find the sweet spot where generalisation is highest.")
        self.wait(2.0)

        # ────────────────────────────────────────────────────────
        # 5.  CLEAR CHART -> KEY INSIGHT CARD  (~5 s)
        # ────────────────────────────────────────────────────────
        self.clear_sub()
        self.play(
            FadeOut(train_curve), FadeOut(test_curve),
            FadeOut(train_legend), FadeOut(test_legend),
            FadeOut(sweet_line),   FadeOut(sweet_label),
            FadeOut(underfit_region), FadeOut(underfit_label),
            FadeOut(overfit_region),  FadeOut(overfit_label),
            FadeOut(bv_card),
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
            run_time=0.7,
        )

        insight = VGroup(
            Text("High train accuracy",  font_size=32, color=BLUE,   font="Arial"),
            Text("+",                    font_size=38, color=WHITE,   font="Arial"),
            Text("Low test accuracy",    font_size=32, color=ORANGE,  font="Arial"),
            Text("=",                    font_size=38, color=WHITE,   font="Arial"),
            Text("Overfitting",          font_size=46, color=RED,     font="Arial", weight=BOLD),
        ).arrange(DOWN, buff=0.20).move_to(ORIGIN)

        self.play(FadeIn(insight, shift=UP * 0.2), run_time=0.8)
        self.show_sub("The model fit the training data's noise -- not the underlying pattern.")
        self.wait(2.2)
        self.show_sub("On unseen data, that noise is different, so predictions collapse.")
        self.wait(2.2)

        # ────────────────────────────────────────────────────────
        # 6.  FIXES  (~10 s)
        #     Each fix gets its own subtitle explaining WHY it works
        # ────────────────────────────────────────────────────────
        self.play(FadeOut(insight), run_time=0.4)
        self.clear_sub()

        fix_title = Text("3 ways to fix it:", font_size=32, color=YELLOW, font="Arial", weight=BOLD)

        fix1 = Text("1. More training data",       font_size=25, color=WHITE, font="Arial")
        fix2 = Text("2. Regularisation (L1 / L2)", font_size=25, color=WHITE, font="Arial")
        fix3 = Text("3. Simpler model / dropout",  font_size=25, color=WHITE, font="Arial")

        fixes = VGroup(fix1, fix2, fix3).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        block = VGroup(fix_title, fixes).arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(ORIGIN)

        self.play(Write(fix_title), run_time=0.55)

        self.play(FadeIn(fix1, shift=RIGHT * 0.2), run_time=0.35)
        self.show_sub("More data: harder to memorise thousands of varied examples.")
        self.wait(2.0)

        self.play(FadeIn(fix2, shift=RIGHT * 0.2), run_time=0.35)
        self.show_sub("Regularisation: penalises large weights, forces the model to stay general.")
        self.wait(2.0)

        self.play(FadeIn(fix3, shift=RIGHT * 0.2), run_time=0.35)
        self.show_sub("Simpler model / dropout: fewer parameters = less room to memorise noise.")
        self.wait(2.0)

        # ────────────────────────────────────────────────────────
        # 7.  CTA OUTRO  (~4 s)
        # ────────────────────────────────────────────────────────
        self.play(FadeOut(block), run_time=0.4)
        self.clear_sub()

        cta = VGroup(
            Text("Follow for more",            font_size=32, color=WHITE, font="Arial"),
            Text("data science in 60 seconds", font_size=36, color=BLUE,  font="Arial", weight=BOLD),
        ).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        self.play(FadeIn(cta, shift=UP * 0.2), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(cta), run_time=0.5)
        self.clear_sub()
