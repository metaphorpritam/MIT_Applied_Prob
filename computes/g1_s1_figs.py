# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for note fragment g1_s1 (L01 + rec01). Writes notes/img/g1_s1_*.png."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mpl_style import setup, diagram_ax, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, PAL = setup()
from matplotlib.patches import Circle, Polygon, Rectangle, FancyArrowPatch, FancyBboxPatch  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL


def save(fig, name):
    p = IMG / f"g1_s1_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ---------------------------------------------------------------- Fig 1.1
def fig_die_grid_tree():
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.0, 4.4),
                                   gridspec_kw={"width_ratios": [1, 1.25]})
    # --- left: 4x4 grid
    axL.set_aspect("equal")
    axL.grid(False)
    for i in range(4):
        for j in range(4):
            axL.add_patch(Rectangle((i, j), 1, 1, fc="white", ec=AXIS_C, lw=1.0))
            axL.text(i + 0.5, j + 0.5, f"({i+1},{j+1})", ha="center", va="center",
                     fontsize=7.5, color=MUTED)
    axL.set_xlim(-0.15, 4.15)
    axL.set_ylim(-0.15, 4.15)
    axL.set_xticks(np.arange(4) + 0.5)
    axL.set_xticklabels([1, 2, 3, 4])
    axL.set_yticks(np.arange(4) + 0.5)
    axL.set_yticklabels([1, 2, 3, 4])
    axL.set_xlabel("$X$ = first roll")
    axL.set_ylabel("$Y$ = second roll")
    axL.set_title("(a) sample space as a grid: 16 outcomes")
    for s in axL.spines.values():
        s.set_visible(False)
    axL.tick_params(length=0)

    # --- right: tree
    diagram_ax(axR)
    axR.set_aspect("auto")
    root = (0.0, 0.0)
    ys1 = np.array([3.0, 1.0, -1.0, -3.0])   # first-roll nodes, 1 at top
    leaf_off = np.array([0.6, 0.2, -0.2, -0.6])
    for k, y1 in enumerate(ys1):
        axR.plot([root[0], 1.0], [root[1], y1], color=AXIS_C, lw=1.1, zorder=1)
        axR.plot([1.0], [y1], marker="o", ms=5, color=BLUE, zorder=3)
        axR.text(0.90, y1 + (0.28 if k < 3 else -0.34), str(k + 1),
                 ha="right", va="bottom" if k < 3 else "top",
                 fontsize=10, color=INK, fontweight="600")
        for m, dy in enumerate(leaf_off):
            y2 = y1 + dy
            axR.plot([1.0, 2.0], [y1, y2], color=AXIS_C, lw=1.0, zorder=1)
            axR.plot([2.0], [y2], marker="o", ms=3.6, color=MUTED, zorder=3)
            if k == 0:
                axR.text(2.08, y2, f"$({k+1},{m+1})$", ha="left", va="center",
                         fontsize=8.5, color=INK)
            elif k == 3 and m == 3:
                axR.text(2.08, y2, "$(4,4)$", ha="left", va="center",
                         fontsize=8.5, color=INK)
    axR.plot([root[0]], [root[1]], marker="o", ms=6, color=INK, zorder=3)
    axR.text(-0.06, 0.0, "start", ha="right", va="center", fontsize=9, color=MUTED)
    axR.text(1.0, 4.15, "1st roll", ha="center", va="center", fontsize=9, color=MUTED)
    axR.text(2.0, 4.15, "2nd roll", ha="center", va="center", fontsize=9, color=MUTED)
    axR.set_xlim(-0.85, 2.95)
    axR.set_ylim(-4.2, 4.6)
    axR.set_title("(b) same space, sequential (tree) description")
    fig.tight_layout()
    save(fig, "die_grid_tree")


# ---------------------------------------------------------------- Fig 1.2
def fig_unit_square():
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(9.2, 4.2))
    for ax in (a0, a1):
        ax.set_aspect("equal")
        ax.grid(False)
        ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec=INK, lw=1.4, zorder=2))
        ax.set_xlim(-0.08, 1.22)
        ax.set_ylim(-0.08, 1.22)
        ax.set_xticks([0, 0.5, 1])
        ax.set_yticks([0, 0.5, 1])
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        for s in ax.spines.values():
            s.set_visible(False)
    a0.plot([0.5], [0.3], marker="o", ms=6, color=ORANGE, zorder=4)
    a0.annotate("outcome $(0.5,\\,0.3)$", xy=(0.5, 0.3), xytext=(0.62, 0.72),
                fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    a0.set_title("(a) $\\Omega=\\{(x,y): 0\\leq x,y\\leq 1\\}$")

    tri = Polygon([[0, 0], [0.5, 0], [0, 0.5]], closed=True, fc=BLUE, alpha=0.28,
                  ec=BLUE, lw=1.6, zorder=3)
    a1.add_patch(tri)
    a1.plot([0, 1], [1, 0], color=MUTED, lw=1.0, ls="--", zorder=3)
    a1.text(0.155, 0.135, "area\n$=1/8$", ha="center", va="center", fontsize=9,
            color=INK, zorder=5)
    a1.annotate("$x+y=1/2$", xy=(0.35, 0.15), xytext=(0.60, 0.42), fontsize=9,
                color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.1))
    a1.text(0.86, 0.06, "$x+y=1$", fontsize=8.5, color=MUTED, ha="right")
    a1.set_title("(b) event $\\{X+Y\\leq 1/2\\}$")
    fig.tight_layout()
    save(fig, "unit_square")


# ---------------------------------------------------------------- Fig 1.3
def fig_venn_choc():
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    diagram_ax(ax)
    ax.add_patch(Rectangle((-2.6, -1.9), 5.2, 3.8, fc="#f7f6f1", ec=AXIS_C, lw=1.2))
    ax.add_patch(Circle((-0.55, 0.0), 1.25, fc=BLUE, alpha=0.22, ec=BLUE, lw=1.6))
    ax.add_patch(Circle((0.55, 0.0), 1.25, fc=ORANGE, alpha=0.22, ec=ORANGE, lw=1.6))
    ax.text(-1.25, 0.0, "0.2", ha="center", va="center", fontsize=13, color=INK, fontweight="600")
    ax.text(0.0, 0.0, "0.4", ha="center", va="center", fontsize=13, color=INK, fontweight="600")
    ax.text(1.25, 0.0, "0.3", ha="center", va="center", fontsize=13, color=INK, fontweight="600")
    ax.text(2.05, -1.5, "0.1", ha="center", va="center", fontsize=13, color=INK, fontweight="600")
    ax.text(-1.25, -0.42, "$A\\cap B^c$", ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(0.0, -0.42, "$A\\cap B$", ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(1.25, -0.42, "$A^c\\cap B$", ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(2.05, -1.12, "$A^c\\cap B^c$", ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(-1.62, 1.20, "$A$: genius (0.6)", ha="center", va="center", fontsize=10, color=BLUE)
    ax.text(1.62, 1.20, "$B$: chocolate (0.7)", ha="center", va="center", fontsize=10, color=ORANGE)
    ax.text(-2.45, 1.70, "$\\Omega$", ha="left", va="center", fontsize=11, color=MUTED)
    ax.set_xlim(-2.75, 2.75)
    ax.set_ylim(-2.05, 2.05)
    ax.set_title("Four disjoint pieces of $\\Omega$; the four numbers sum to 1")
    fig.tight_layout()
    save(fig, "venn_choc")


# ---------------------------------------------------------------- Fig 1.4
def fig_geometric():
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(9.6, 3.9))
    ns = np.arange(1, 9)
    p = 2.0 ** (-ns)
    a0.stem(ns, p, basefmt=" ", linefmt="-", markerfmt="o")
    for ln in a0.get_lines():
        ln.set_color(MUTED if ln.get_linestyle() == "-" else MUTED)
    a0.stem(ns, p, basefmt=" ")
    a0.cla()
    a0.grid(True)
    a0.vlines(ns, 0, p, color=AXIS_C, lw=1.4, zorder=2)
    a0.plot(ns, p, "o", color=MUTED, ms=5, zorder=3)
    ev = ns[ns % 2 == 0]
    a0.vlines(ev, 0, 2.0 ** (-ev.astype(float)), color=BLUE, lw=2.4, zorder=4)
    a0.plot(ev, 2.0 ** (-ev.astype(float)), "o", color=BLUE, ms=6, zorder=5)
    for n in [1, 2, 3, 4]:
        a0.text(n, 2.0 ** (-n) + 0.022, f"$1/{2**n}$", ha="center", fontsize=8.5,
                color=BLUE if n % 2 == 0 else MUTED)
    a0.set_xlabel("$n$")
    a0.set_ylabel("$\\mathbf{P}(n)=2^{-n}$")
    a0.set_xticks(ns)
    a0.set_ylim(0, 0.60)
    a0.set_title("(a) mass $2^{-n}$; even $n$ highlighted")

    k = np.arange(1, 9)
    partial = np.cumsum(0.25 ** k)
    a1.plot(k, partial, "-o", color=BLUE, ms=5, label="partial sum $S_N$")
    a1.axhline(1 / 3, color=ORANGE, lw=1.6, ls="--", label="limit $1/3$")
    a1.set_xlabel("$N$ (number of terms)")
    a1.set_ylabel("$S_N=\\sum_{k=1}^{N}(1/4)^k$")
    a1.set_ylim(0.22, 0.36)
    a1.set_xticks(k)
    a1.legend(loc="lower right")
    a1.set_title("(b) $S_N=\\frac{1}{3}\\left(1-4^{-N}\\right)\\to 1/3$")
    fig.tight_layout()
    save(fig, "geometric")


# ---------------------------------------------------------------- Fig 1.5
def fig_nested_sets():
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(9.6, 4.3))
    diagram_ax(a0)
    diagram_ax(a1)
    rr = [0.55, 0.95, 1.30, 1.58]
    cols = [BLUE, GREEN, GOLD, ORANGE]
    for r, c in zip(rr, cols):
        a0.add_patch(Circle((0, 0), r, fc="none", ec=c, lw=1.8))
    a0.add_patch(Circle((0, 0), 1.85, fc="none", ec=MUTED, lw=1.6, ls="--"))
    labs = ["$A_1$", "$A_2$", "$A_3$", "$A_4$"]
    prev = 0.0
    for r, c, lb in zip(rr, cols, labs):
        a0.text(0, (prev + r) / 2, lb, ha="center", va="center", fontsize=10, color=c)
        prev = r
    a0.text(0, (1.58 + 1.85) / 2, "$\\cdots$", ha="center", va="center", fontsize=10, color=MUTED)
    a0.text(0, -2.10, "$A=A_1\\cup A_2\\cup A_3\\cup\\cdots$", ha="center", va="center",
            fontsize=10.5, color=INK)
    a0.set_xlim(-2.3, 2.3)
    a0.set_ylim(-2.45, 2.15)
    a0.set_title("(a) increasing $A_1\\subset A_2\\subset\\cdots$")

    # right: annulus decomposition B_n, drawn largest-first so the shells read
    # as clean rings with no polygon seam
    tint = {BLUE: "#cfe1f7", GREEN: "#c6ecdd", GOLD: "#f8e4b4", ORANGE: "#f9d5c3"}
    for i in (3, 2, 1, 0):
        a1.add_patch(Circle((0, 0), rr[i], fc=tint[cols[i]], ec=cols[i], lw=1.3,
                            zorder=2 + (3 - i)))
    a1.text(0, 0, "$B_1=A_1$", ha="center", va="center", fontsize=9, color=INK,
            zorder=8)
    for i in range(1, 4):
        a1.text(0, (rr[i - 1] + rr[i]) / 2, f"$B_{i+1}$", ha="center", va="center",
                fontsize=9, color=INK, zorder=8)
    a1.text(0, -2.10, "$B_n=A_n\\cap A_{n-1}^c$  are disjoint,  $\\bigcup_{k\\leq n}B_k=A_n$",
            ha="center", va="center", fontsize=9.5, color=INK)
    a1.set_xlim(-2.3, 2.3)
    a1.set_ylim(-2.45, 2.15)
    a1.set_title("(b) disjoint shells used in the proof")
    fig.tight_layout()
    save(fig, "nested_sets")


# ---------------------------------------------------------------- Fig 1.6
def fig_grid_events():
    events = [
        ("$\\{(1,1),(1,2)\\}$", lambda x, y: (x, y) in [(1, 1), (1, 2)], "$\\mathbf{P}=2/16=1/8$"),
        ("$\\{X=1\\}$", lambda x, y: x == 1, "$\\mathbf{P}=4/16=1/4$"),
        ("$\\{X+Y\\ \\mathrm{odd}\\}$", lambda x, y: (x + y) % 2 == 1, "$\\mathbf{P}=8/16=1/2$"),
        ("$\\{\\min(X,Y)=2\\}$", lambda x, y: min(x, y) == 2, "$\\mathbf{P}=5/16$"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(12.4, 3.5))
    for ax, (title, f, sub) in zip(axes, events):
        ax.set_aspect("equal")
        ax.grid(False)
        for i in range(4):
            for j in range(4):
                on = f(i + 1, j + 1)
                ax.add_patch(Rectangle((i, j), 1, 1, fc=BLUE if on else "white",
                                       alpha=0.42 if on else 1.0, ec=AXIS_C, lw=0.9))
        ax.set_xlim(-0.1, 4.1)
        ax.set_ylim(-0.1, 4.1)
        ax.set_xticks(np.arange(4) + 0.5)
        ax.set_xticklabels([1, 2, 3, 4])
        ax.set_yticks(np.arange(4) + 0.5)
        ax.set_yticklabels([1, 2, 3, 4])
        ax.set_xlabel("$X$")
        ax.set_ylabel("$Y$")
        ax.set_title(title + "\n" + sub, fontsize=10)
        ax.tick_params(length=0)
        for s in ax.spines.values():
            s.set_visible(False)
    fig.tight_layout()
    save(fig, "grid_events")


# ---------------------------------------------------------------- Fig 1.7
def fig_romeo():
    fig, (a0, a1) = plt.subplots(1, 2, figsize=(9.6, 4.3))
    w = 0.25
    for ax in (a0, a1):
        ax.set_aspect("equal")
        ax.grid(False)
        ax.set_xlim(-0.10, 1.18)
        ax.set_ylim(-0.10, 1.18)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
        ax.set_xlabel("$x$ = Romeo's delay (hours)")
        ax.set_ylabel("$y$ = Juliet's delay (hours)")
        for s in ax.spines.values():
            s.set_visible(False)
        ax.add_patch(Rectangle((0, 0), 1, 1, fc="white", ec=INK, lw=1.4, zorder=2))

    band = Polygon([[0, 0], [1 - w, 1], [1, 1], [1, 1 - w], [w, 0]], closed=True,
                   fc=GREEN, alpha=0.30, ec=GREEN, lw=1.6, zorder=3)
    a0.add_patch(band)
    a0.plot([0, 1], [0, 1], color=MUTED, lw=1.0, ls=":", zorder=4)
    a0.text(0.86, 0.79, "$y=x$", ha="left", va="center", fontsize=8.5, color=MUTED,
            rotation=45, zorder=5)
    a0.text(0.50, 0.62, "$M$: they meet", ha="center", va="center", fontsize=9.5,
            color=INK, rotation=45, rotation_mode="anchor", zorder=6)
    a0.annotate("$y=x+\\frac{1}{4}$", xy=(0.30, 0.55), xytext=(0.02, 0.90), fontsize=8.5,
                color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))
    a0.annotate("$y=x-\\frac{1}{4}$", xy=(0.68, 0.43), xytext=(0.80, 0.14), fontsize=8.5,
                color=GREEN, ha="center",
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))
    a0.set_title("(a) meeting event $M=\\{|x-y|\\leq 1/4\\}$")

    t1 = Polygon([[0, w], [0, 1], [1 - w, 1]], closed=True, fc=ORANGE, alpha=0.30,
                 ec=ORANGE, lw=1.4, zorder=3)
    t2 = Polygon([[w, 0], [1, 0], [1, 1 - w]], closed=True, fc=ORANGE, alpha=0.30,
                 ec=ORANGE, lw=1.4, zorder=3)
    a1.add_patch(t1)
    a1.add_patch(t2)
    a1.text(0.235, 0.80, "area\n$\\frac{1}{2}(\\frac{3}{4})^2=\\frac{9}{32}$", ha="center",
            va="center", fontsize=8.5, color=INK, zorder=5)
    a1.text(0.79, 0.205, "area\n$\\frac{1}{2}(\\frac{3}{4})^2=\\frac{9}{32}$", ha="center",
            va="center", fontsize=8.5, color=INK, zorder=5)
    a1.text(0.50, 0.44, "$\\mathbf{P}(M)=1-\\frac{9}{16}=\\frac{7}{16}$", ha="center",
            va="center", fontsize=10, color=INK, rotation=45, zorder=5)
    a1.set_title("(b) complement = two corner triangles")
    fig.tight_layout()
    save(fig, "romeo_band")


# ---------------------------------------------------------------- Fig 1.8
def fig_flowchart():
    fig, ax = plt.subplots(figsize=(10.4, 5.8))
    diagram_ax(ax)
    ax.set_aspect("auto")

    def box(x, y, w, h, text, fc, ec, fs=9.5):
        ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h,
                               fc=fc, ec=ec, lw=1.4, zorder=2))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
                zorder=3)

    def arrow(p, q, label="", dx=0.0, dy=0.0):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12,
                                     color=MUTED, lw=1.2, shrinkA=2, shrinkB=2))
        if label:
            ax.text((p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, label,
                    ha="center", va="center", fontsize=8.5, color=MUTED,
                    bbox=dict(fc="white", ec="none", pad=1.2))

    box(0.50, 0.935, 0.46, 0.09, "List $\\Omega$: mutually exclusive,\ncollectively exhaustive", "#eef4fc", BLUE)
    box(0.50, 0.765, 0.40, 0.09,
        "Classify $\\Omega$: finite, countably\ninfinite, or continuous?", "#fdf3ec", ORANGE)
    box(0.155, 0.545, 0.27, 0.09, "Are all outcomes\nequally likely?", "#fdf3ec", ORANGE)
    box(0.855, 0.545, 0.27, 0.09, "Assign areas /\nlengths to regions", "#eef4fc", BLUE)
    box(0.095, 0.305, 0.20, 0.115,
        "Discrete uniform law\n$\\mathbf{P}(A)=\\frac{|A|}{|\\Omega|}$\n(finite $\\Omega$ only)", "#eaf7f1", DGREEN, 8.5)
    box(0.475, 0.305, 0.32, 0.115,
        "Sum the given masses\n$\\mathbf{P}(A)=\\sum_{s\\in A}\\mathbf{P}(s)$\n(countable additivity)",
        "#eaf7f1", DGREEN, 8.5)
    box(0.855, 0.305, 0.26, 0.115, "Uniform law:\n$\\mathbf{P}(A)=\\mathrm{area}(A)$", "#eaf7f1", DGREEN, 9)
    box(0.50, 0.075, 0.86, 0.075,
        "Stuck? Try the complement, or split $A$ into disjoint pieces and add (Axiom 3).",
        "#f7f6f1", AXIS_C, 9)

    arrow((0.50, 0.890), (0.50, 0.812))
    arrow((0.40, 0.722), (0.20, 0.592), "finite", dy=0.012)
    arrow((0.50, 0.718), (0.50, 0.365), "countably\ninfinite", dx=0.058)
    arrow((0.60, 0.722), (0.81, 0.592), "continuous", dy=0.012)
    arrow((0.085, 0.499), (0.085, 0.365), "yes", dx=-0.032)
    arrow((0.235, 0.499), (0.345, 0.365), "no", dx=0.032)
    arrow((0.855, 0.489), (0.855, 0.365))
    arrow((0.095, 0.247), (0.26, 0.115))
    arrow((0.475, 0.247), (0.49, 0.115))
    arrow((0.855, 0.247), (0.72, 0.115))

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(0.0, 1.0)
    ax.set_title("Which probability law do I use?")
    fig.tight_layout()
    save(fig, "flowchart")


for f in [fig_die_grid_tree, fig_unit_square, fig_venn_choc, fig_geometric,
          fig_nested_sets, fig_grid_events, fig_romeo, fig_flowchart]:
    f()
print("done")
