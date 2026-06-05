"""
shared.py  —  Shared palette, helpers and reusable builders
for all 21 TEXT-A … TEXT-U scenes.
Import everything from here so every file stays consistent.
"""

from manim import *

# ── Palette (matches HTML guide exactly) ──────────────────────────────────────
BG      = "#0d0f14"
SURFACE = "#13161e"
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

# ── Reusable builders ──────────────────────────────────────────────────────────

def card(body_lines, color, title=None, width=11.5, line_h=0.58):
    """
    Returns a VGroup: coloured-border RoundedRectangle + optional bold title
    + body text.  body_lines is a list of strings.
    """
    n_lines = len(body_lines) + (1 if title else 0)
    height  = max(1.4, n_lines * line_h + 0.55)

    bg = RoundedRectangle(
        corner_radius=0.15, width=width, height=height,
        fill_color=SURFACE, fill_opacity=1.0,
        stroke_color=color, stroke_width=2.2
    )

    items = VGroup()
    if title:
        t = Text(title, font_size=19, color=color, weight=BOLD)
        items.add(t)
    for line in body_lines:
        items.add(Text(line, font_size=18, color=BODY))

    items.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    items.move_to(bg.get_center()).shift(RIGHT * 0.15)

    return VGroup(bg, items)


def bullet_row(dot_color, text_str, font_size=19, dot_char="●"):
    """Single bullet row: coloured dot + text."""
    dot  = Text(dot_char, font_size=font_size - 2, color=dot_color)
    body = Text(text_str, font_size=font_size, color=BODY)
    return VGroup(dot, body).arrange(RIGHT, buff=0.22)


def table_scene(scene, title_str, headers, rows,
                col_widths=None, header_color=HEADING,
                row_colors=None, title_color=HEADING):
    """
    Draw an animated table inside `scene`.
    headers : list of column header strings
    rows    : list of lists (each inner list = one row of strings)
    col_widths : list of floats (pixel widths per column)
    row_colors : list of colours parallel to rows (defaults to BODY for all)
    """
    n_cols = len(headers)
    if col_widths is None:
        col_widths = [3.8] * n_cols
    if row_colors is None:
        row_colors = [BODY] * len(rows)

    row_h   = 0.68
    total_w = sum(col_widths) + (n_cols - 1) * 0.05
    start_x = -total_w / 2

    # Title
    title = Text(title_str, font_size=24, color=title_color).to_edge(UP, buff=0.35)
    scene.play(Write(title), run_time=0.6)

    # Header row
    def make_row(texts, bg_color, text_color, y, bold=False):
        row_group = VGroup()
        x = start_x
        for txt, w in zip(texts, col_widths):
            cell_bg = Rectangle(
                width=w, height=row_h,
                fill_color=bg_color, fill_opacity=1.0,
                stroke_color=BORDER, stroke_width=0.8
            ).move_to([x + w / 2, y, 0])
            cell_txt = Text(
                txt, font_size=15,
                color=text_color,
                weight=BOLD if bold else NORMAL
            ).move_to(cell_bg.get_center())
            row_group.add(VGroup(cell_bg, cell_txt))
            x += w + 0.05
        return row_group

    # Calculate vertical positions
    n_rows  = len(rows)
    total_h = (n_rows + 1) * row_h
    y_start = total_h / 2 - row_h / 2 - 0.3   # leave room for title

    header_row = make_row(headers, "#1a1e2a", header_color, y_start, bold=True)
    scene.play(FadeIn(header_row), run_time=0.5)

    for i, (row_data, rcolor) in enumerate(zip(rows, row_colors)):
        y = y_start - (i + 1) * row_h
        alt_bg = SURFACE if i % 2 == 0 else "#0f1218"
        data_row = make_row(row_data, alt_bg, rcolor, y)
        scene.play(FadeIn(data_row, shift=RIGHT * 0.2), run_time=0.38)
        scene.wait(0.7)
