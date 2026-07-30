# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for note G1 section 2 (conditioning, total probability, Bayes)."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mpl_style import setup, diagram_ax, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse, FancyArrowPatch  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
import matplotlib.patches as mpatches  # noqa: E402
import numpy as np  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL


def save(fig, name):
    p = IMG / f"g1_s2_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# --------------------------------------------------------------- Fig 2.1 grid
def fig_grid():
    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    diagram_ax(ax)
    B = {(2, 2), (2, 3), (2, 4), (3, 2), (4, 2)}
    for x in range(1, 5):
        for y in range(1, 5):
            if (x, y) == (2, 2):
                fc, ec, lw = BLUE, BLUE, 2.0
            elif (x, y) in B:
                fc, ec, lw = "#f7d3c0", ORANGE, 2.0
            else:
                fc, ec, lw = "white", AXIS_C, 1.0
            ax.add_patch(Rectangle((x - .5, y - .5), 1, 1, facecolor=fc,
                                   edgecolor=ec, linewidth=lw, zorder=2))
            if (x, y) in B:
                m = max(x, y)
                col = "white" if (x, y) == (2, 2) else INK
                ax.text(x, y, f"M={m}", ha="center", va="center",
                        fontsize=10.5, color=col, zorder=3)
    for x in range(1, 5):
        ax.text(x, 0.28, str(x), ha="center", va="top", fontsize=10, color=MUTED)
        ax.text(0.28, x, str(x), ha="right", va="center", fontsize=10, color=MUTED)
    ax.text(2.5, -0.15, "$X$ = first roll", ha="center", va="top", fontsize=11, color=INK)
    ax.text(-0.35, 2.5, "$Y$ = second roll", ha="center", va="center",
            rotation=90, fontsize=11, color=INK)
    ax.add_patch(Rectangle((0.5, 0.5), 4, 4, fill=False, edgecolor=INK, linewidth=1.6, zorder=4))
    handles = [mpatches.Patch(facecolor="#f7d3c0", edgecolor=ORANGE, label=r"$B=\{\min(X,Y)=2\}$,  5 cells"),
               mpatches.Patch(facecolor=BLUE, edgecolor=BLUE, label=r"$\{M=2\}\cap B$,  1 cell")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.06),
              fontsize=9.5, frameon=True)
    ax.set_xlim(-0.75, 4.8)
    ax.set_ylim(-0.55, 4.8)
    ax.set_title("Two rolls of a fair 4-sided die: 16 equally likely cells", pad=10)
    save(fig, "diegrid")


# ------------------------------------------------- Fig 2.2 multiplication tree
def fig_multtree():
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    ax.axis("off"); ax.grid(False)

    def node(x, y, r=0.045):
        ax.add_patch(plt.Circle((x, y), r, color=INK, zorder=5))

    def branch(x0, y0, x1, y1, lab, col=INK, up=True, fs=9.5):
        ax.plot([x0, x1], [y0, y1], color=col, lw=1.4, zorder=2)
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        dy = 0.10 if up else -0.10
        ax.text(xm, ym + dy, lab, ha="center",
                va="bottom" if up else "top", fontsize=fs, color=col, zorder=6,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9))

    x0, x1, x2, x3 = 0.0, 1.5, 3.2, 5.1
    node(x0, 0)
    yA, yAc = 2.1, -2.1
    branch(x0, 0, x1, yA, r"$\mathbf{P}(A)$", BLUE, True)
    branch(x0, 0, x1, yAc, r"$\mathbf{P}(A^c)$", MUTED, False)
    node(x1, yA); node(x1, yAc)
    ax.text(x1 - 0.10, yA + 0.16, "$A$", fontsize=11, color=BLUE, ha="right")
    ax.text(x1 - 0.10, yAc - 0.16, "$A^c$", fontsize=11, color=MUTED, ha="right", va="top")

    lvl2 = [(yA, 3.1, 1.15, r"$\mathbf{P}(B\mid A)$", r"$\mathbf{P}(B^c\mid A)$",
             r"$A\cap B$", r"$A\cap B^c$", BLUE),
            (yAc, -1.15, -3.1, r"$\mathbf{P}(B\mid A^c)$", r"$\mathbf{P}(B^c\mid A^c)$",
             r"$A^c\cap B$", r"$A^c\cap B^c$", MUTED)]
    leaves = []
    for yp, yu, yd, lu, ld, nu, nd, col in lvl2:
        for yy, lab, nm, up in ((yu, lu, nu, True), (yd, ld, nd, False)):
            branch(x1, yp, x2, yy, lab, col, up)
            node(x2, yy)
            ax.text(x2 - 0.08, yy + (0.17 if up else -0.17), nm, fontsize=10, color=col,
                    ha="right", va="bottom" if up else "top")
            leaves.append((yy, nm, col))

    for yy, nm, col in leaves:
        base = nm.rstrip("$")
        for sgn, sub in ((+1, "C"), (-1, "C^c")):
            ye = yy + sgn * 0.42
            ax.plot([x2, x3], [yy, ye], color=col, lw=1.2, zorder=2)
            ax.text(x3 + 0.06, ye, base + r"\cap " + sub + "$", fontsize=9.5,
                    color=INK, ha="left", va="center")
            node(x3, ye, r=0.035)
    ax.text(x2 + 0.75, 3.50, r"$\mathbf{P}(C\mid A\cap B)$", fontsize=9, color=BLUE,
            ha="center", va="bottom",
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.95))
    ax.text(x2 + 0.75, 2.58, r"$\mathbf{P}(C^c\mid A\cap B)$", fontsize=9, color=BLUE,
            ha="center", va="top",
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.95))
    ax.text(2.55, -4.15,
            r"leaf probability $=$ product of the branch probabilities on the root-to-leaf path",
            ha="center", fontsize=10, color=MUTED)
    ax.set_xlim(-0.5, 6.9); ax.set_ylim(-4.5, 4.3)
    ax.set_title("Multiplication (chain) rule: a sequential tree for three events", pad=6)
    save(fig, "multtree")


# ----------------------------------------------------- Fig 2.3 partition / TPT
def fig_partition():
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.axis("off"); ax.grid(False)
    ax.add_patch(Rectangle((0, 0), 10, 6, fill=False, edgecolor=INK, lw=1.8, zorder=4))
    # curve 1: left edge -> top edge  (separates A1 above from A2 below)
    t = np.linspace(0, 1, 200)
    c1x = 0 + 6.0 * t
    c1y = 1.6 + 4.4 * t ** 1.6
    # curve 2: top edge -> bottom edge (A3 to the right)
    s = np.linspace(0, 1, 200)
    c2x = 7.0 + 0.9 * np.sin(np.pi * s) * -1 + 0.0
    c2y = 6 - 6 * s
    ax.add_patch(Rectangle((0, 0), 10, 6, facecolor="#fbe6da", edgecolor="none", zorder=0))
    ax.fill_between(c1x, c1y, 6, color="#dceaf9", zorder=1)
    ax.fill_betweenx(c2y, c2x, 10, color="#d9f2e7", zorder=1)
    ax.plot(c1x, c1y, color=INK, lw=1.5, zorder=4)
    ax.plot(c2x, c2y, color=INK, lw=1.5, zorder=4)
    ell = Ellipse((5.0, 3.0), 8.0, 1.9, facecolor="#9e9d97", alpha=0.55,
                  edgecolor=INK, lw=1.5, zorder=3)
    ax.add_patch(ell)
    ax.text(1.4, 5.1, "$A_1$", fontsize=15, color=BLUE, ha="center", zorder=6)
    ax.text(1.4, 0.9, "$A_2$", fontsize=15, color=ORANGE, ha="center", zorder=6)
    ax.text(8.9, 0.9, "$A_3$", fontsize=15, color=GREEN, ha="center", zorder=6)
    ax.text(9.55, 5.55, r"$\Omega$", fontsize=14, color=INK, ha="center", zorder=6)
    ax.text(2.2, 3.0, r"$A_1\!\cap\! B$", fontsize=10.5, ha="center", va="center", zorder=6)
    ax.text(5.2, 3.0, r"$A_2\!\cap\! B$", fontsize=10.5, ha="center", va="center", zorder=6)
    ax.text(8.2, 3.0, r"$A_3\!\cap\! B$", fontsize=10.5, ha="center", va="center", zorder=6)
    ax.annotate("$B$", xy=(5.0, 3.95), xytext=(5.0, 7.0), ha="center", fontsize=14,
                color=INK, arrowprops=dict(arrowstyle="->", color=INK, lw=1.3), zorder=6)
    ax.text(5.0, -1.15,
            r"$\mathbf{P}(B)=\mathbf{P}(A_1\cap B)+\mathbf{P}(A_2\cap B)+\mathbf{P}(A_3\cap B)"
            r"=\sum_i \mathbf{P}(A_i)\mathbf{P}(B\mid A_i)$",
            ha="center", fontsize=11.5, color=INK)
    ax.set_xlim(-0.6, 10.6); ax.set_ylim(-1.9, 7.6)
    save(fig, "partition")


# ------------------------------------------------------- Fig 2.4 radar tree
def fig_radar():
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.axis("off"); ax.grid(False)

    def node(x, y, r=0.055, c=INK):
        ax.add_patch(plt.Circle((x, y), r, color=c, zorder=5))

    x0, x1, x2 = 0.0, 1.9, 4.2
    node(x0, 0)
    yA, yAc = 1.7, -1.7
    for (yy, lab, col, up) in ((yA, r"$\mathbf{P}(A)=0.05$", BLUE, True),
                               (yAc, r"$\mathbf{P}(A^c)=0.95$", MUTED, False)):
        ax.plot([x0, x1], [0, yy], color=col, lw=1.6, zorder=2)
        ax.text((x0 + x1) / 2, yy / 2 + (0.16 if up else -0.16), lab, fontsize=10,
                color=col, ha="center", va="bottom" if up else "top",
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.92))
        node(x1, yy, c=col)
    ax.text(x1 - 0.12, yA + 0.30, "$A$: plane above", fontsize=10.5, color=BLUE,
            ha="right", va="bottom")
    ax.text(x1 - 0.12, yAc - 0.30, "$A^c$: no plane", fontsize=10.5, color=MUTED,
            ha="right", va="top")

    rows = [(yA, 2.75, r"$\mathbf{P}(B\mid A)=0.99$", BLUE, r"$A\cap B$", "0.05 · 0.99 = 0.0495", True),
            (yA, 0.95, r"$\mathbf{P}(B^c\mid A)=0.01$", BLUE, r"$A\cap B^c$", "0.05 · 0.01 = 0.0005", False),
            (yAc, -0.95, r"$\mathbf{P}(B\mid A^c)=0.10$", MUTED, r"$A^c\cap B$", "0.95 · 0.10 = 0.0950", True),
            (yAc, -2.75, r"$\mathbf{P}(B^c\mid A^c)=0.90$", MUTED, r"$A^c\cap B^c$", "0.95 · 0.90 = 0.8550", False)]
    for yp, yl, lab, col, leaf, val, up in rows:
        ax.plot([x1, x2], [yp, yl], color=col, lw=1.6, zorder=2)
        ax.text((x1 + x2) / 2, (yp + yl) / 2 + (0.16 if up else -0.16), lab, fontsize=10,
                color=col, ha="center", va="bottom" if up else "top",
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.92))
        node(x2, yl, c=col)
        hl = ORANGE if r"\cap B$" in leaf else GRID_C
        # box height 0.90 with the two text lines at +/-0.19 leaves ~0.55 of a
        # line height between them and equal padding above/below (see Fig 2.4 review)
        ax.add_patch(FancyBboxPatch((x2 + 0.22, yl - 0.45), 2.95, 0.90,
                                    boxstyle="round,pad=0.04", fc="#fdf3ec" if hl == ORANGE else "#f6f6f3",
                                    ec=hl, lw=1.4, zorder=3))
        ax.text(x2 + 0.36, yl + 0.19, leaf, fontsize=10.5, color=INK, ha="left", va="center", zorder=6)
        ax.text(x2 + 0.36, yl - 0.19, val, fontsize=9.5, color=MUTED, ha="left", va="center", zorder=6)

    ax.annotate("", xy=(7.9, -0.95), xytext=(7.9, 2.75),
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=1.6))
    ax.plot([7.75, 7.9], [2.75, 2.75], color=ORANGE, lw=1.6)
    ax.plot([7.75, 7.9], [-0.95, -0.95], color=ORANGE, lw=1.6)
    ax.text(8.05, 0.9, "$\\mathbf{P}(B)=0.0495+0.0950$\n$\\qquad\\;\\; =0.1445$",
            fontsize=10.5, color=ORANGE, ha="left", va="center")
    ax.text(2.4, -3.85, r"$\mathbf{P}(A\mid B)=\dfrac{0.0495}{0.1445}\approx 0.3426$",
            fontsize=12.5, color=INK, ha="center", va="center")
    ax.set_xlim(-0.5, 11.4); ax.set_ylim(-4.5, 3.5)
    ax.set_title("Radar model (L02 slide 5): every branch and leaf value", pad=6)
    save(fig, "radartree")


# ------------------------------------------------------- Fig 2.5 Monty tree
def fig_monty():
    fig, ax = plt.subplots(figsize=(10.6, 5.6))
    ax.axis("off"); ax.grid(False)

    def node(x, y, r=0.05, c=INK):
        ax.add_patch(plt.Circle((x, y), r, color=c, zorder=5))

    x0, x1, x2 = 0.0, 2.1, 5.0
    node(x0, 0)
    prize_y = {1: 2.4, 2: 0.0, 3: -2.4}
    cols = {1: BLUE, 2: ORANGE, 3: GREEN}
    for i, yy in prize_y.items():
        ax.plot([x0, x1], [0, yy], color=cols[i], lw=1.6, zorder=2)
        ax.text((x0 + x1) / 2, yy / 2 + (0.16 if yy >= 0 else -0.16), r"$1/3$",
                fontsize=10, color=cols[i], ha="center",
                va="bottom" if yy >= 0 else "top",
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.92))
        node(x1, yy, c=cols[i])
        if i == 1:
            ax.text(x1 - 0.12, yy + 0.22, f"$P_{i}$: prize behind {i}", fontsize=10,
                    color=cols[i], ha="right", va="bottom")
        else:
            ax.text(x1 - 0.12, yy - 0.22, f"$P_{i}$: prize behind {i}", fontsize=10,
                    color=cols[i], ha="right", va="top")

    # branches: you always choose door 1 (C_1)
    leaf_rows = [
        (1, 2.4, 3.0, r"$\mathbf{P}(O_2\mid P_1\cap C_1)=q$", "$O_2$", "q/3", "W", "L", "W"),
        (1, 2.4, 1.8, r"$\mathbf{P}(O_3\mid P_1\cap C_1)=1-q$", "$O_3$", "(1−q)/3", "W", "L", "L"),
        (2, 0.0, 0.0, r"$\mathbf{P}(O_3\mid P_2\cap C_1)=1$", "$O_3$", "1/3", "L", "W", "W"),
        (3, -2.4, -2.4, r"$\mathbf{P}(O_2\mid P_3\cap C_1)=1$", "$O_2$", "1/3", "L", "W", "L"),
    ]
    for i, yp, yl, lab, leaf, prob, s_a, s_b, s_c in leaf_rows:
        up = yl >= yp
        ax.plot([x1, x2], [yp, yl], color=cols[i], lw=1.5, zorder=2)
        ax.text((x1 + x2) / 2, (yp + yl) / 2 + (0.15 if up else -0.15), lab, fontsize=9,
                color=cols[i], ha="center", va="bottom" if up else "top",
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.92))
        node(x2, yl, c=cols[i])
        ax.text(x2 + 0.16, yl, leaf, fontsize=10, color=INK, ha="left", va="center")
        ax.text(x2 + 1.05, yl, prob, fontsize=10, color=MUTED, ha="left", va="center")
        for k, (s, xcol) in enumerate(zip((s_a, s_b, s_c), (7.6, 8.8, 10.0))):
            c = DGREEN if s == "W" else RED
            ax.add_patch(Rectangle((xcol - 0.30, yl - 0.22), 0.60, 0.44,
                                   facecolor="#e2f2e2" if s == "W" else "#fbe3e2",
                                   edgecolor=c, lw=1.2, zorder=3))
            ax.text(xcol, yl, s, fontsize=10, color=c, ha="center", va="center", zorder=4)
    for xcol, lab in ((7.6, "(a) stick"), (8.8, "(b) switch"), (10.0, "(c) mixed")):
        ax.text(xcol, 3.62, lab, fontsize=10.5, color=INK, ha="center", va="bottom")
    ax.text(x2 + 0.16, 3.62, "opened", fontsize=10, color=MUTED, ha="left", va="bottom")
    ax.text(x2 + 1.05, 3.62, "leaf prob.", fontsize=10, color=MUTED, ha="left", va="bottom")
    ax.plot([x2 + 0.10, 10.55], [3.50, 3.50], color=AXIS_C, lw=1.0)
    ax.text(5.2, -3.55,
            "you always choose door 1 ($C_1$);  $q=\\mathbf{P}(O_2\\mid P_1\\cap C_1)$ is the host's tie-break rule\n"
            "(a) $1/3$    (b) $2/3$    (c) $q/3+1/3$  = $2/3$ if $q=1$, $1/2$ if $q=1/2$",
            fontsize=10.5, color=INK, ha="center", va="center")
    ax.set_xlim(-0.5, 10.7); ax.set_ylim(-4.3, 4.1)
    ax.set_title("Monty Hall: one tree, three strategies", pad=6)
    save(fig, "montytree")


# ------------------------------------------------------ Fig 2.6 decision flow
def fig_flow():
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    ax.axis("off"); ax.grid(False)

    def box(x, y, w, h, txt, fc, ec, fs=10):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.06", fc=fc, ec=ec, lw=1.5, zorder=3))
        ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=INK, zorder=4)

    def arrow(x0, y0, x1, y1, lab=None, lx=None, ly=None):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                     mutation_scale=13, color=MUTED, lw=1.3, zorder=2,
                                     shrinkA=2, shrinkB=4))
        if lab:
            ax.text(lx, ly, lab, fontsize=9, color=MUTED, ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none"), zorder=5)

    box(5.0, 9.2, 6.6, 0.95, "What is given, and what is asked?", "#f2f1ec", AXIS_C, 11)
    box(1.55, 6.6, 3.0, 1.5,
        "given: $\\mathbf{P}(A)$ and the\nstage-by-stage $\\mathbf{P}(B\\mid A)$\nwant: $\\mathbf{P}(A\\cap B)$",
        "#dceaf9", BLUE, 9.5)
    box(5.0, 6.6, 3.0, 1.5,
        "given: a partition $A_i$\nwith $\\mathbf{P}(A_i),\\ \\mathbf{P}(B\\mid A_i)$\nwant: $\\mathbf{P}(B)$",
        "#fbe6da", ORANGE, 9.5)
    box(8.45, 6.6, 3.0, 1.5,
        "given: same data,\n$B$ has been observed\nwant: $\\mathbf{P}(A_i\\mid B)$",
        "#d9f2e7", GREEN, 9.5)
    arrow(5.0, 8.72, 1.55, 7.40, "chain forward", 2.35, 8.30)
    arrow(5.0, 8.72, 5.0, 7.40, "sum over causes", 5.0, 8.06)
    arrow(5.0, 8.72, 8.45, 7.40, "invert", 7.85, 8.30)
    box(1.55, 4.0, 3.15, 1.25,
        "Multiplication rule\n$\\mathbf{P}(A\\cap B)=\\mathbf{P}(A)\\mathbf{P}(B\\mid A)$",
        "white", BLUE, 9.5)
    box(5.0, 4.0, 3.15, 1.25,
        "Total probability\n$\\mathbf{P}(B)=\\sum_i \\mathbf{P}(A_i)\\mathbf{P}(B\\mid A_i)$",
        "white", ORANGE, 9.5)
    box(8.45, 4.0, 3.15, 1.25,
        "Bayes' rule\n$\\mathbf{P}(A_i\\mid B)=\\dfrac{\\mathbf{P}(A_i)\\mathbf{P}(B\\mid A_i)}{\\mathbf{P}(B)}$",
        "white", GREEN, 9.5)
    for x in (1.55, 5.0, 8.45):
        arrow(x, 5.85, x, 4.65)
    arrow(1.55, 3.02, 4.55, 3.02)
    ax.text(3.05, 2.74, "one term per branch", fontsize=8.5, color=MUTED, ha="center", va="top")
    arrow(5.0, 3.02, 8.00, 3.02)
    ax.text(6.50, 2.74, "supplies the denominator", fontsize=8.5, color=MUTED, ha="center", va="top")
    # wrapped onto two lines so the string fits inside the rounded rect with padding
    box(5.0, 1.30, 6.6, 1.30,
        "Always check: do the branch probabilities\n"
        "out of each node sum to 1, and do the\n"
        "leaf probabilities sum to 1?", "#f2f1ec", AXIS_C, 9.5)
    ax.set_xlim(-0.35, 10.35); ax.set_ylim(0.4, 10.0)
    save(fig, "toolflow")


fig_grid()
fig_multtree()
fig_partition()
fig_radar()
fig_monty()
fig_flow()
print("done")
