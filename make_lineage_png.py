"""Generate a dark, deck-matching PNG of the CryoSync data lineage.

Layout: SOURCES -> BRONZE -> SILVER -> GOLD -> CONSUMERS (left to right),
matching the diagrams in CryoSync_Architecture.html, styled like the
CryoSync_StemCyte_Presentation deck (deep navy / accent colours).

Run from project root:  python make_lineage_png.py
Output: CryoSync_Data_Lineage.png
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

W, H = 2400, 1350

BG = "#0F172A"
CARD = "#1A233B"
TEAL = "#00B4D8"
BLUE = "#0096D6"
GREEN = "#00C853"
ORANGE = "#FF8C00"
GOLD_TITLE = "#EAB308"
SILVER_TITLE = "#CBD5E1"
WHITE = "#FFFFFF"
GRAY = "#B0C4DE"
DIM = "#8AA3C4"
SLATE = "#94A3B8"

fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.axis("off")


def box(x, y, w, h, edge, title, lines, title_color=None, title_size=15, body_size=10.5, line_h=27,
        title_h=30, pad=16, lw=1.6, fill=CARD):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0,rounding_size=16",
        linewidth=lw, edgecolor=edge, facecolor=fill, zorder=2))
    ty = y + h - title_h
    ax.text(x + pad, ty, title, color=title_color or edge, fontsize=title_size,
            fontweight="bold", va="center", ha="left", zorder=3)
    yy = ty - line_h
    for ln in lines:
        ax.text(x + pad, yy, ln, color=GRAY, fontsize=body_size, va="center", ha="left", zorder=3)
        yy -= line_h


def arrow(p0, p1, color=TEAL, lw=2.4, ls="-", rad=0.0, shrinkA=6, shrinkB=10):
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle="-|>", mutation_scale=22, linewidth=lw,
        color=color, linestyle=ls, zorder=1,
        connectionstyle=f"arc3,rad={rad}", shrinkA=shrinkA, shrinkB=shrinkB))


def label(x, y, s, size=8.5, color=GRAY, weight="normal", ha="center"):
    ax.text(x, y, s, color=color, fontsize=size, fontweight=weight, ha=ha, va="center",
            zorder=4, bbox=dict(boxstyle="round,pad=0.32", fc=BG, ec="none", alpha=0.9))


# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
ax.text(40, 1322, "CryoSync - Data Lineage", color=WHITE, fontsize=24, fontweight="bold",
        va="center", ha="left")
ax.text(40, 1284, "How data flows from every source into Databricks and back out as live answers",
        color=GRAY, fontsize=12, va="center", ha="left")
ax.text(W - 40, 1322, "Unity Catalog: cryosync_catalog  |  Delta Lake",
        color=DIM, fontsize=11, va="center", ha="right")

# Stage headers
for cx, name in [(240, "SOURCES"), (730, "BRONZE - RAW"), (1190, "SILVER - CLEANSED"),
                 (1630, "GOLD - ANALYTICS"), (2140, "CONSUMERS")]:
    ax.text(cx, 1232, name, color=SLATE, fontsize=13, fontweight="bold", ha="center", va="center")

# ---------------------------------------------------------------------------
# SOURCES (left column)
# ---------------------------------------------------------------------------
sources = [
    (TEAL, "Zoho CRM v7", ["OAuth2 refresh, incremental by", "Modified_Time -> bronze.zoho_*"]),
    (TEAL, "SQLite app DB", ["migrate (full) + sync (watermark)", "UPDATE_TRACKED vs APPEND_ONLY"]),
    (TEAL, "Lab report uploads", ["/api/lab-reports/upload -> CSV/", "batch import -> bronze tables"]),
    (TEAL, "Background loops", ["temp scanner (1 min) + CRM sync", "(60 min) feed bronze"]),
]
sy = 1040
for seed, title, lines in sources:
    box(40, sy, 400, 140, seed, title, lines, title_color=TEAL)
    sy -= 170

# ---------------------------------------------------------------------------
# BRONZE / SILVER / GOLD bands (centre ~845, bottom 700)
# ---------------------------------------------------------------------------
box(560, 700, 340, 290, ORANGE, "BRONZE - raw", [
    "cryosync_catalog.bronze",
    "raw, append-only mirrors of every source",
    "MERGE INTO upserts on reload",
    "sync_watermark per table",
], title_color=ORANGE, body_size=10)

box(1040, 700, 300, 290, SILVER_TITLE, "SILVER - cleansed", [
    "cryosync_catalog.silver",
    "validated, conformed, deduplicated",
    "typed joins across sources",
], title_color=SILVER_TITLE)

box(1480, 700, 300, 290, GREEN, "GOLD - analytics", [
    "cryosync_catalog.gold",
    "unit_summary | enrollment_funnel | kpis",
    "gold.v_unit_inventory (Genie view)",
], title_color=GREEN)

# ---------------------------------------------------------------------------
# Sources -> Bronze arrows
# ---------------------------------------------------------------------------
for src_cy, land_y in [(1110, 975), (940, 890), (770, 815), (600, 735)]:
    arrow((440, src_cy), (560, land_y), color=ORANGE, rad=0.05)

# ---------------------------------------------------------------------------
# Bronze -> Silver -> Gold (arrows + drop-line captions below the band)
# ---------------------------------------------------------------------------
arrow((900, 845), (1040, 845), color=TEAL)
ax.plot([970, 970], [845, 672], color=TEAL, lw=1.0, ls=(0, (3, 3)), zorder=1)
label(970, 630, "nightly 02:00 UTC\nbuild_silver_gold (Spark 15.4)", size=8.5)

arrow((1340, 845), (1480, 845), color=TEAL)
ax.plot([1410, 1410], [845, 672], color=TEAL, lw=1.0, ls=(0, (3, 3)), zorder=1)
label(1410, 630, "views: unit_summary\nenrollment_funnel | kpis", size=8.5)

# ---------------------------------------------------------------------------
# Gold -> Consumers
# ---------------------------------------------------------------------------
arrow((1780, 845), (1920, 1110), color=TEAL)
label(1850, 1002, "Genie SELECT", size=8.5)
arrow((1780, 845), (1920, 940), color=BLUE)
label(1850, 906, "gold KPIs", size=8.5)

# Backend SQL connector (dashed path from BRONZE, routed below the bands)
ax.plot([730, 730], [700, 560], color=ORANGE, lw=1.6, ls=(0, (4, 3)), zorder=1)
ax.plot([730, 2140], [560, 560], color=ORANGE, lw=1.6, ls=(0, (4, 3)), zorder=1)
arrow((2140, 560), (2140, 700), color=ORANGE, lw=1.6, ls=(0, (4, 3)))
label(1435, 586, "backend reads/writes bronze directly (CRYOSYNC_DB_BACKEND=databricks)",
      size=8)

# Consumers boxes
cons = [
    (1110, TEAL, "Databricks Genie", ["NL -> SQL over gold tables", "powers Kyra's answers", "incl. v_unit_inventory"]),
    (940, BLUE, "Dashboards & Pages", ["/api/dashboard | /api/pages/*", "gold KPIs -> live charts", "multi-facility rollups"]),
    (770, ORANGE, "Backend SQL connector", ["ops read/write when", "CRYOSYNC_DB_BACKEND=databricks", "MERGE INTO bronze"]),
]
for cy, edge, title, lines in cons:
    box(1920, cy - 70, 440, 140, edge, title, lines, title_color=edge)

# ---------------------------------------------------------------------------
# Footnote
# ---------------------------------------------------------------------------
ax.text(W / 2, 430,
        "SQLite fallback when self-hosted  |  nightly bronze -> silver -> gold job currently paused until bronze is seeded",
        color=DIM, fontsize=10.5, ha="center", va="center")

out = "CryoSync_Data_Lineage.png"
fig.savefig(out, dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
print("wrote", out, f"({fig.get_size_inches()[0]}x{fig.get_size_inches()[1]}in)")