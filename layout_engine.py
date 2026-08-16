"""
layout_engine.py
=================
Ye module AI image-generation PAR NIRBHAR NAHI hai. Ye pure Python +
matplotlib se ek EXACT TO-SCALE 2D floor plan banata hai, jisme rooms ki
dimensions hamesha plot ke total width/length ke barabar SUM hoti hain
(guaranteed by construction, kyunki hum ratios ko normalize karke actual
feet me convert karte hain — koi "AI guess" nahi hota).

CORE IDEA (Slicing / Strip Layout):
- Plot ko HORIZONTAL ROWS (strips) me baanta hai, North se South tak.
- Har row ki height = (row's height_ratio / sum of all height_ratios) * plot_length
  => sabhi row heights ka sum hamesha EXACTLY plot_length ke barabar hoga.
- Har row ke andar, room-cells ko VERTICAL columns me baanta hai.
- Har cell ki width = (cell's width_ratio / sum of width_ratios in that row) * plot_width
  => har row ke andar cells ki width ka sum hamesha EXACTLY plot_width ke barabar hoga.

Isliye chahe plot 15x40 ho ya 30x60, dimensions kabhi bhi mismatch nahi
honge — ye sirf ek "visually similar" image nahi, balki real geometry hai.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io


# A pleasant, distinguishable color per room type (purely cosmetic)
ROOM_COLORS = {
    "toilet": "#cfe8f0",
    "bathroom": "#cfe8f0",
    "master bedroom": "#e8d9b8",
    "bedroom": "#f0e6d2",
    "pooja": "#fdf3d0",
    "kitchen": "#d8ecd8",
    "dining": "#f5efe0",
    "living": "#f2ece0",
    "parking": "#d9d9d9",
    "staircase": "#c9c9c9",
    "passage": "#e0e0e0",
    "default": "#f5f0e6",
}


def _color_for(name):
    key = name.strip().lower()
    for k, v in ROOM_COLORS.items():
        if k in key:
            return v
    return ROOM_COLORS["default"]


def default_room_template(plot_width, plot_length):
    """
    India-style 2-3BHK ground-floor template, defined as RATIOS
    (not absolute ft). Ratios auto-normalize to whatever plot size
    is entered, so dimensions always add up correctly.

    Returns: list of dicts -> [{"row": row, "room": name,
                                 "width_ratio": w, "height_ratio": h}, ...]
    Rows are numbered 1 (North / top) to N (South / bottom, road side).
    """
    return [
        {"row": 1, "room": "Toilet",         "width_ratio": 4,  "height_ratio": 7},
        {"row": 1, "room": "Master Bedroom", "width_ratio": 8,  "height_ratio": 7},
        {"row": 1, "room": "Pooja / Store",  "width_ratio": 3,  "height_ratio": 7},

        {"row": 2, "room": "Passage",        "width_ratio": 4,  "height_ratio": 6},
        {"row": 2, "room": "Kitchen",        "width_ratio": 7,  "height_ratio": 6},
        {"row": 2, "room": "Dining",         "width_ratio": 4,  "height_ratio": 6},

        {"row": 3, "room": "Staircase",      "width_ratio": 4,  "height_ratio": 7},
        {"row": 3, "room": "Bedroom 2",      "width_ratio": 11, "height_ratio": 7},

        {"row": 4, "room": "Living",         "width_ratio": 9,  "height_ratio": 12},
        {"row": 4, "room": "Parking",        "width_ratio": 6,  "height_ratio": 12},
    ]


def normalize_layout(room_list, plot_width, plot_length):
    """
    Takes raw ratio-based room_list and converts to ABSOLUTE feet,
    guaranteeing:
      sum(row heights) == plot_length
      sum(cell widths within each row) == plot_width

    Returns: list of rows -> [{"height": ft, "cells": [{"name","width","color"}...]}]
    """
    rows_order = sorted(set(r["row"] for r in room_list))

    # Row height ratio = take the ratio value from first cell in that row
    row_height_ratio = {}
    for r in room_list:
        row_height_ratio.setdefault(r["row"], r["height_ratio"])

    total_height_ratio = sum(row_height_ratio[r] for r in rows_order)

    layout_rows = []
    for row_num in rows_order:
        row_h = (row_height_ratio[row_num] / total_height_ratio) * plot_length

        cells_in_row = [r for r in room_list if r["row"] == row_num]
        total_width_ratio = sum(c["width_ratio"] for c in cells_in_row)

        cells = []
        for c in cells_in_row:
            cell_w = (c["width_ratio"] / total_width_ratio) * plot_width
            cells.append({
                "name": c["room"],
                "width": cell_w,
                "color": _color_for(c["room"]),
            })
        layout_rows.append({"height": row_h, "cells": cells})

    return layout_rows


def render_floorplan(layout_rows, plot_width, plot_length, facing="North", title=None):
    """
    Draws the normalized layout to-scale using matplotlib.
    Returns a matplotlib Figure object.
    Convention: Row 1 = top of drawing = North side (unless facing changes emphasis).
    """
    fig_h = 9
    fig_w = max(6, fig_h * (plot_width / plot_length))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    y = plot_length  # start at top, go down
    for row in layout_rows:
        h = row["height"]
        y -= h
        x = 0
        for cell in row["cells"]:
            w = cell["width"]
            rect = patches.Rectangle(
                (x, y), w, h,
                linewidth=1.6, edgecolor="black",
                facecolor=cell["color"],
            )
            ax.add_patch(rect)
            ax.text(
                x + w / 2, y + h / 2,
                f"{cell['name']}\n{w:.1f}' x {h:.1f}'",
                ha="center", va="center", fontsize=8.5, fontweight="medium",
                wrap=True,
            )
            x += w

    # Outer plot boundary (thick)
    ax.add_patch(patches.Rectangle((0, 0), plot_width, plot_length,
                                    linewidth=3, edgecolor="black", facecolor="none"))

    # Dimension labels
    ax.text(plot_width / 2, plot_length + 0.6, f"{plot_width:.1f}' WIDTH",
            ha="center", fontsize=10, fontweight="bold")
    ax.text(-0.6, plot_length / 2, f"{plot_length:.1f}' LENGTH", ha="center",
            va="center", fontsize=10, fontweight="bold", rotation=90)

    # North arrow (top-right corner, simple)
    nx, ny = plot_width + plot_width * 0.05, plot_length * 0.9
    ax.annotate("N", xy=(nx, ny), xytext=(nx, ny - plot_length * 0.08),
                arrowprops=dict(arrowstyle="-|>", lw=2, color="red"),
                ha="center", fontsize=11, fontweight="bold", color="red")

    ax.set_xlim(-plot_width * 0.15, plot_width * 1.15)
    ax.set_ylim(-plot_length * 0.05, plot_length * 1.12)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        title or f"To-Scale Conceptual Floor Plan — {plot_width:.0f}' x {plot_length:.0f}'  (Facing: {facing})",
        fontsize=12, fontweight="bold",
    )
    fig.tight_layout()
    return fig


def figure_to_png_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
    buf.seek(0)
    return buf.getvalue()


def validate_sums(layout_rows, plot_width, plot_length, tol=0.05):
    """
    Sanity self-check (should always pass since normalize_layout()
    guarantees exact math) — returned for transparency/debug display.
    """
    total_h = sum(r["height"] for r in layout_rows)
    row_checks = []
    for r in layout_rows:
        w_sum = sum(c["width"] for c in r["cells"])
        row_checks.append(round(w_sum, 3))
    ok_height = abs(total_h - plot_length) < tol
    ok_widths = all(abs(w - plot_width) < tol for w in row_checks)
    return {
        "total_height": round(total_h, 2),
        "plot_length": plot_length,
        "height_match": ok_height,
        "row_width_sums": row_checks,
        "plot_width": plot_width,
        "width_match": ok_widths,
    }
