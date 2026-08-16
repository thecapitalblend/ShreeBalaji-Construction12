"""
layout_engine.py (v2 — STRUCTURAL GRID ENGINE)
================================================
V1 BUG (fixed now): Har row ki cells independently ratio se normalize hoti
thi. Isse row-1 ka column boundary row-2 ke column boundary se ALIGN nahi
hota tha — bilkul wahi galti jo uploaded "30x50 bungalow" plan me dikhi
(Master Bedroom/Kitchen boundary 16' pe, lekin Pooja/Dining boundary 22'
pe — column line seedhi nahi). Real RCC building me ye galat hai kyunki
column foundation se roof tak ek hi vertical line me hona chahiye.

V2 FIX — SHARED STRUCTURAL GRID:
- Poore plot ke liye EK hi set of vertical grid-lines (x_lines, West→East)
  aur EK hi set of horizontal grid-lines (y_lines, North→South) define
  hoti hai.
- HAR room in SAME shared lines ka use karke banta hai (jaise Excel me
  merged cells) — isliye koi bhi do room jo adjacent hain, unki common
  wall/column line hamesha ek hi grid-line pe hogi. Column alignment
  ab MATHEMATICALLY GUARANTEED hai, kisi extra check ki zarurat nahi.
- Har room ka width & height compute karke MAX_BEAM_SPAN (default 15 ft)
  se check kiya jata hai. Agar exceed karta hai, warning milti hai
  (real RCC beams 15-16 ft se zyada span par bahut mehenge/impractical
  ho jate hain bina beam depth badhaye).
- Column markers (C1 = perimeter/corner column, C2 = interior junction
  column) automatically un exact grid-points par draw hote hain jaha
  do ya zyada room-boundaries milti hain — bilkul jaise ek real column
  schedule banta hai.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
from collections import Counter

MAX_BEAM_SPAN_DEFAULT = 15.0  # ft — safe practical RCC beam span for residential

ROOM_COLORS = {
    "toilet": "#cfe8f0",
    "bathroom": "#cfe8f0",
    "master bedroom": "#e8d9b8",
    "bedroom": "#f0e6d2",
    "guest": "#f0e6d2",
    "pooja": "#fdf3d0",
    "kitchen": "#d8ecd8",
    "dining": "#f5efe0",
    "living": "#f2ece0",
    "parking": "#d9d9d9",
    "staircase": "#c9c9c9",
    "passage": "#e0e0e0",
    "store": "#e6ded0",
    "default": "#f5f0e6",
}


def _color_for(name):
    key = name.strip().lower()
    for k, v in ROOM_COLORS.items():
        if k in key:
            return v
    return ROOM_COLORS["default"]


# ---------------------------------------------------------------------------
# DEFAULT TEMPLATE — corrected 30x50 North-facing bungalow
# ---------------------------------------------------------------------------
# All coordinates below are RATIOS (auto-scaled to actual plot_width /
# plot_length). x_ratios go West->East, y_ratios go North->South.
# Every room's col_start/col_end/row_start/row_end are INDEXES into the
# grid-line arrays (0-based), so alignment is guaranteed by construction.
#
# Fixes applied vs the uploaded plan:
#  1. Shared grid -> columns line up top to bottom (structural continuity).
#  2. No room spans more than 15 ft in either direction (safe beam spans).
#  3. Entrance/Parking placed on the SAME side as "facing" (North here) —
#     fixes the north-facing-label-but-south-entrance contradiction.
#  4. Vastu zoning corrected: Pooja=NE, Kitchen=SE, Master Bedroom=SW.
def default_grid_template():
    return {
        "x_ratios": [8, 7, 8, 7],       # West -> East bay widths (sum = plot width)
        "y_ratios": [11, 11, 13, 15],   # North -> South bay heights (sum = plot length)
        "rooms": [
            {"name": "Parking",        "col_start": 0, "col_end": 2, "row_start": 0, "row_end": 1},
            {"name": "Living",         "col_start": 2, "col_end": 3, "row_start": 0, "row_end": 1},
            {"name": "Pooja (NE)",     "col_start": 3, "col_end": 4, "row_start": 0, "row_end": 1},

            {"name": "Toilet",         "col_start": 0, "col_end": 1, "row_start": 1, "row_end": 2},
            {"name": "Passage",        "col_start": 1, "col_end": 2, "row_start": 1, "row_end": 2},
            {"name": "Guest Bedroom",  "col_start": 2, "col_end": 4, "row_start": 1, "row_end": 2},

            {"name": "Staircase",      "col_start": 0, "col_end": 1, "row_start": 2, "row_end": 3},
            {"name": "Dining",         "col_start": 1, "col_end": 3, "row_start": 2, "row_end": 3},
            {"name": "Store",          "col_start": 3, "col_end": 4, "row_start": 2, "row_end": 3},

            {"name": "Master Bedroom (SW)", "col_start": 0, "col_end": 2, "row_start": 3, "row_end": 4},
            {"name": "Kitchen (SE)",        "col_start": 2, "col_end": 4, "row_start": 3, "row_end": 4},
        ],
    }


def compute_grid_lines(ratios, total):
    """Convert relative ratios into absolute cumulative coordinates (0..total)."""
    s = sum(ratios)
    lines = [0.0]
    acc = 0.0
    for r in ratios:
        acc += (r / s) * total
        lines.append(acc)
    return lines


def compute_rooms_geometry(template, plot_width, plot_length):
    """
    Resolves the ratio-based template into actual room rectangles for the
    given plot size. Because every room references the SAME x_lines/y_lines
    array, any two adjacent rooms will always share an exact coordinate —
    i.e. columns are guaranteed to be structurally continuous.
    """
    x_lines = compute_grid_lines(template["x_ratios"], plot_width)
    y_lines = compute_grid_lines(template["y_ratios"], plot_length)

    rooms_geo = []
    for r in template["rooms"]:
        x0, x1 = x_lines[r["col_start"]], x_lines[r["col_end"]]
        y0, y1 = y_lines[r["row_start"]], y_lines[r["row_end"]]
        rooms_geo.append({
            "name": r["name"],
            "x": x0, "y": y0,
            "width": x1 - x0, "height": y1 - y0,
            "color": _color_for(r["name"]),
        })
    return rooms_geo, x_lines, y_lines


def validate_spans(rooms_geo, max_span=MAX_BEAM_SPAN_DEFAULT):
    """
    Structural sanity check: flags any room whose clear width or height
    exceeds the safe RCC beam span limit (default 15 ft). A real senior
    engineer would insist on either an intermediate column or a deeper
    beam section for anything beyond this.
    """
    warnings = []
    for r in rooms_geo:
        if r["width"] > max_span + 1e-6:
            warnings.append(
                f"⚠️ {r['name']}: width {r['width']:.1f}' > {max_span:.0f}' max safe beam span — "
                f"needs intermediate column or deeper beam section."
            )
        if r["height"] > max_span + 1e-6:
            warnings.append(
                f"⚠️ {r['name']}: depth {r['height']:.1f}' > {max_span:.0f}' max safe beam span — "
                f"needs intermediate column or deeper beam section."
            )
    return warnings


def _find_column_points(rooms_geo, plot_width, plot_length, tol=0.02):
    """
    Derives real structural column positions from the grid geometry:
    - C1 = perimeter/corner columns (on the outer boundary)
    - C2 = interior junction columns (where 2+ room-corners meet)
    This mirrors how an actual column schedule is derived from a grid.
    """
    corners = []
    for r in rooms_geo:
        corners += [
            (r["x"], r["y"]),
            (r["x"] + r["width"], r["y"]),
            (r["x"], r["y"] + r["height"]),
            (r["x"] + r["width"], r["y"] + r["height"]),
        ]
    rounded = [(round(x, 2), round(y, 2)) for x, y in corners]
    counts = Counter(rounded)

    columns = []
    for (x, y), cnt in counts.items():
        on_boundary = (
            abs(x - 0) < tol or abs(x - plot_width) < tol or
            abs(y - 0) < tol or abs(y - plot_length) < tol
        )
        if on_boundary:
            columns.append((x, y, "C1"))
        elif cnt >= 2:
            columns.append((x, y, "C2"))
    return columns


def render_grid_floorplan(rooms_geo, x_lines, y_lines, plot_width, plot_length,
                           facing="North", title=None, show_grid_lines=True):
    fig_h = 10
    fig_w = max(6, fig_h * (plot_width / plot_length))
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    # NOTE ON ORIENTATION: room["y"] / y_lines are measured as distance from
    # the NORTH edge (row_start=0 = North, increasing southward) — matching
    # how the template is authored (Vastu zones: row 0 = North strip).
    # matplotlib draws with y increasing UPWARD, so to keep North at the TOP
    # of the image (matching the North arrow), we flip: draw_y = plot_length - south_edge.

    # Faint background grid to visually prove the shared structural grid
    if show_grid_lines:
        for x in x_lines:
            ax.plot([x, x], [0, plot_length], color="#cccccc", lw=0.6, linestyle=":", zorder=0)
        for y in y_lines:
            draw_y = plot_length - y
            ax.plot([0, plot_width], [draw_y, draw_y], color="#cccccc", lw=0.6, linestyle=":", zorder=0)

    # Rooms
    for r in rooms_geo:
        draw_y = plot_length - (r["y"] + r["height"])  # flip so North (y=0) is at top
        rect = patches.Rectangle(
            (r["x"], draw_y), r["width"], r["height"],
            linewidth=1.6, edgecolor="black", facecolor=r["color"], zorder=1,
        )
        ax.add_patch(rect)
        ax.text(
            r["x"] + r["width"] / 2, draw_y + r["height"] / 2,
            f"{r['name']}\n{r['width']:.1f}' x {r['height']:.1f}'",
            ha="center", va="center", fontsize=8.3, fontweight="medium", zorder=2,
        )

    # Outer boundary
    ax.add_patch(patches.Rectangle((0, 0), plot_width, plot_length,
                                    linewidth=3, edgecolor="black", facecolor="none", zorder=3))

    # Real structural columns (C1/C2), derived from actual grid junctions
    # (column points from _find_column_points are in original North=0 coords,
    # flip them the same way as rooms so they line up visually)
    columns = _find_column_points(rooms_geo, plot_width, plot_length)
    for x, y, label in columns:
        draw_y = plot_length - y
        ax.add_patch(patches.Rectangle((x - 0.35, draw_y - 0.35), 0.7, 0.7,
                                        facecolor="red", edgecolor="black", zorder=4))

    # Dimension labels
    ax.text(plot_width / 2, plot_length + 0.7, f"{plot_width:.1f}' WIDTH",
            ha="center", fontsize=10, fontweight="bold")
    ax.text(-0.9, plot_length / 2, f"{plot_length:.1f}' LENGTH", ha="center",
            va="center", fontsize=10, fontweight="bold", rotation=90)

    # North arrow — Row index 0 (top of drawing) = North, consistent with facing
    nx, ny = plot_width + plot_width * 0.06, plot_length * 0.92
    ax.annotate("N", xy=(nx, ny), xytext=(nx, ny - plot_length * 0.08),
                arrowprops=dict(arrowstyle="-|>", lw=2, color="red"),
                ha="center", fontsize=11, fontweight="bold", color="red")

    ax.set_xlim(-plot_width * 0.16, plot_width * 1.18)
    ax.set_ylim(-plot_length * 0.05, plot_length * 1.12)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        title or f"Structurally-Aligned To-Scale Plan — {plot_width:.0f}' x {plot_length:.0f}'  (Facing: {facing})",
        fontsize=12, fontweight="bold",
    )
    fig.tight_layout()
    return fig


def figure_to_png_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
    buf.seek(0)
    return buf.getvalue()


def alignment_self_check(rooms_geo, x_lines, y_lines, tol=0.02):
    """
    Proves that every room boundary actually sits ON a shared grid line
    (i.e. no 'floating' boundaries like in the flawed uploaded plan).
    """
    bad = []
    for r in rooms_geo:
        x_ok = any(abs(r["x"] - xl) < tol for xl in x_lines) and \
               any(abs(r["x"] + r["width"] - xl) < tol for xl in x_lines)
        y_ok = any(abs(r["y"] - yl) < tol for yl in y_lines) and \
               any(abs(r["y"] + r["height"] - yl) < tol for yl in y_lines)
        if not (x_ok and y_ok):
            bad.append(r["name"])
    return {"all_aligned": len(bad) == 0, "misaligned_rooms": bad}
