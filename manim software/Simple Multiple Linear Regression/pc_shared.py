"""
pc_shared.py — palette + reusable ProsCons builder
All bullets are word-wrapped at 48 chars, font_size=15 to prevent overflow.
"""
from manim import *

BG      = "#0d0f14"
SURFACE = "#13161e"
SURFACE2= "#0f1218"
BORDER  = "#252a38"
BLUE_D  = "#4f9eff"
ORANGE_L= "#f97316"
YELLOW_R= "#fbbf24"
GREEN_G = "#10b981"
RED_B   = "#f87171"
PURPLE  = "#a855f7"
MUTED   = "#8892a4"
HEADING = "#f8fafc"
BODY    = "#c8d0dc"

PRO_COL = GREEN_G
CON_COL = RED_B

BULLET_FS   = 15     # font size for bullet body text
WRAP_CHARS  = 44     # max chars per line before wrapping
PANEL_GAP   = 0.18   # vertical gap between wrapped lines inside one bullet
ROW_GAP_1   = 0.75   # row gap when no bullet wraps (1-line bullets)
ROW_GAP_2   = 1.25   # row gap when any bullet in the pair has 2 lines
ROW_GAP_3   = 1.72   # row gap when any bullet has 3 lines


def _wrap(text: str, max_chars: int = WRAP_CHARS) -> str:
    """Word-wrap text to max_chars per line, return \n-joined string."""
    words = text.split()
    lines, cur, cur_len = [], [], 0
    for w in words:
        added = len(w) + (1 if cur else 0)
        if cur_len + added > max_chars:
            lines.append(' '.join(cur))
            cur, cur_len = [w], len(w)
        else:
            cur.append(w)
            cur_len += added
    if cur:
        lines.append(' '.join(cur))
    return '\n'.join(lines)


def _line_count(text: str) -> int:
    return _wrap(text).count('\n') + 1


def _make_bullet(text: str, color, x_center: float, y: float) -> VGroup:
    """
    Build one bullet row (dot + wrapped body text) positioned at (x_center, y).
    The row is left-aligned from x_center - 2.85.
    """
    dot  = Text("●", font_size=BULLET_FS - 1, color=color)
    body = Text(_wrap(text), font_size=BULLET_FS, color=BODY,
                line_spacing=1.25)
    row  = VGroup(dot, body).arrange(RIGHT, buff=0.18, aligned_edge=UP)
    # Pin left edge to panel left boundary
    left_x = x_center - 2.85
    row.align_to([left_x, 0, 0], LEFT)
    row.move_to([row.get_center()[0], y, 0])
    return row


def pc_scene(scene, title_str: str, title_color,
             pros: list, cons: list,
             pro_head: str = "✅  Pros",
             con_head: str = "❌  Cons"):
    """
    Render a full split-screen pros/cons animation inside `scene`.
    Bullets are word-wrapped so they never overflow the half-panel.
    """
    scene.camera.background_color = BG

    # ── Title ────────────────────────────────────────────────────────────────
    title = Text(title_str, font_size=23, color=title_color,
                 weight=BOLD).to_edge(UP, buff=0.28)
    scene.play(Write(title), run_time=0.55)

    # ── Divider ───────────────────────────────────────────────────────────────
    div = Line(UP * 2.65, DOWN * 3.5, color=BORDER, stroke_width=1.5)
    scene.play(Create(div), run_time=0.28)

    # ── Panel headers ─────────────────────────────────────────────────────────
    pro_h = Text(pro_head, font_size=18, color=PRO_COL, weight=BOLD) \
        .move_to(LEFT  * 3.2 + UP * 2.15)
    con_h = Text(con_head, font_size=18, color=CON_COL, weight=BOLD) \
        .move_to(RIGHT * 3.2 + UP * 2.15)
    scene.play(Write(pro_h), Write(con_h), run_time=0.45)

    # ── Pre-compute row heights so bullets don't collide ─────────────────────
    n = max(len(pros), len(cons))
    row_heights = []
    for i in range(n):
        p_lines = _line_count(pros[i]) if i < len(pros) else 1
        c_lines = _line_count(cons[i]) if i < len(cons) else 1
        max_lines = max(p_lines, c_lines)
        if max_lines >= 3:
            row_heights.append(ROW_GAP_3)
        elif max_lines == 2:
            row_heights.append(ROW_GAP_2)
        else:
            row_heights.append(ROW_GAP_1)

    # ── Build y positions from top down ──────────────────────────────────────
    y_start = 1.52
    y_positions = []
    y = y_start
    for h in row_heights:
        y_positions.append(y)
        y -= h

    # ── Animate bullets interleaved ──────────────────────────────────────────
    for i in range(n):
        anims = []
        if i < len(pros):
            r = _make_bullet(pros[i], PRO_COL, -3.2, y_positions[i])
            anims.append(FadeIn(r, shift=RIGHT * 0.22))
        if i < len(cons):
            r = _make_bullet(cons[i], CON_COL,  3.2, y_positions[i])
            anims.append(FadeIn(r, shift=LEFT  * 0.22))
        scene.play(*anims, run_time=0.40)
        scene.wait(0.80)

    scene.wait(1.2)
