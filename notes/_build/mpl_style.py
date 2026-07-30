"""Shared matplotlib style for all 6.041 note figures. Import and call setup().

Palette + mark rules follow the dataviz method (validated categorical order,
recessive grid, thin marks). Figures must be checked visually after generation.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# dataviz validated categorical palette (light mode), fixed order
PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
       "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
INK, MUTED, GRID_C, AXIS_C = "#1a1a1a", "#52514e", "#e1e0d9", "#c3c2b7"


def setup():
    plt.rcParams.update({
        "figure.dpi": 150,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.08,
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.titleweight": "600",
        "axes.labelsize": 10,
        "axes.labelcolor": INK,
        "axes.edgecolor": AXIS_C,
        "axes.linewidth": 1.0,
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.prop_cycle": plt.cycler(color=PAL),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.color": GRID_C,
        "grid.linewidth": 0.7,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.frameon": True,
        "legend.framealpha": 0.92,
        "legend.edgecolor": GRID_C,
        "legend.fontsize": 9,
        "lines.linewidth": 2.0,
        "lines.markersize": 6,
        "mathtext.fontset": "dejavusans",
    })
    return plt, PAL


def diagram_ax(ax):
    """For flowcharts/trees/Venn: no axes, equal aspect."""
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    return ax
