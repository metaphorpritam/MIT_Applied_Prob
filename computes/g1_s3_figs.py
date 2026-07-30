# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for G1 section 3 — Independence.  uv run computes/g1_s3_figs.py"""
from __future__ import annotations

import sys
from math import comb
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
from mpl_style import setup, diagram_ax, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
import matplotlib.patches as mp  # noqa: E402
import numpy as np  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    p = IMG / f"g1_s3_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ============================================================ Fig 3.1  3-toss tree
def fig_tree3():
    p = 0.6
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    ax.axis("off")
    leaves = ["HHH", "HHT", "HTH", "HTT", "THH", "THT", "TTH", "TTT"]
    ys3 = [7 - i for i in range(8)]
    ys2 = [(ys3[0] + ys3[1]) / 2, (ys3[2] + ys3[3]) / 2, (ys3[4] + ys3[5]) / 2, (ys3[6] + ys3[7]) / 2]
    ys1 = [(ys2[0] + ys2[1]) / 2, (ys2[2] + ys2[3]) / 2]
    y0 = (ys1[0] + ys1[1]) / 2
    hl = {"HTT", "THT", "TTH"}

    def edge(x0, ya, x1, yb, lab, up):
        ax.plot([x0, x1], [ya, yb], color=AXIS_C, lw=1.4, zorder=1)
        ax.text((x0 + x1) / 2, (ya + yb) / 2 + (0.16 if up else -0.16), lab,
                ha="center", va="bottom" if up else "top", fontsize=9,
                color=PAL[0] if up else PAL[1])

    for i, y in enumerate(ys1):
        edge(0.05, y0, 1.0, y, "$p$" if i == 0 else "$1-p$", i == 0)
    for i, y in enumerate(ys2):
        edge(1.0, ys1[i // 2], 2.0, y, "$p$" if i % 2 == 0 else "$1-p$", i % 2 == 0)
    for i, y in enumerate(ys3):
        edge(2.0, ys2[i // 2], 3.0, y, "$p$" if i % 2 == 0 else "$1-p$", i % 2 == 0)

    for x, ys in ((0.05, [y0]), (1.0, ys1), (2.0, ys2)):
        for y in ys:
            ax.plot([x], [y], "o", ms=6, color=INK, zorder=3)
    probs = [p ** 3, p ** 2 * (1 - p), p ** 2 * (1 - p), p * (1 - p) ** 2,
             p ** 2 * (1 - p), p * (1 - p) ** 2, p * (1 - p) ** 2, (1 - p) ** 3]
    for lab, y, pr in zip(leaves, ys3, probs):
        c = PAL[2] if lab in hl else INK
        ax.plot([3.0], [y], "o", ms=6, color=c, zorder=3)
        ax.text(3.12, y, lab, ha="left", va="center", fontsize=10.5,
                color=c, fontweight="600" if lab in hl else "normal")
        ax.text(3.72, y, f"{pr:.3f}", ha="left", va="center", fontsize=9.5, color=MUTED)
    ax.text(3.72, 7.75, "prob. ($p{=}0.6$)", ha="left", va="center", fontsize=9, color=MUTED)
    ax.text(3.12, 7.75, "outcome", ha="left", va="center", fontsize=9, color=MUTED)
    ax.text(0.05, 7.75, "toss 1", ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(1.0, 7.75, "toss 2", ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(2.0, 7.75, "toss 3", ha="center", va="center", fontsize=9, color=MUTED)
    ax.annotate("green leaves = exactly one head:\n"
                "$\\mathbf{P}=3p(1-p)^2 = 3(0.096) = 0.288$",
                xy=(2.93, 1.0), xytext=(1.05, -1.15), fontsize=10, color=PAL[2],
                ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color=PAL[2], lw=1.3,
                                connectionstyle="arc3,rad=-0.14"))
    ax.set_xlim(-0.35, 4.6)
    ax.set_ylim(-1.9, 8.2)
    save(fig, "tree3")


# ================================================= Fig 3.2  independence vs disjoint
def fig_indep_disjoint():
    fig, axs = plt.subplots(1, 2, figsize=(9.2, 4.3))
    for ax in axs:
        diagram_ax(ax)
        ax.set_xlim(-0.06, 1.06)
        ax.set_ylim(-0.30, 1.40)

    ax = axs[0]
    ax.add_patch(mp.Rectangle((0, 0), 1, 1, fc="white", ec=AXIS_C, lw=1.2))
    ax.add_patch(mp.Circle((0.28, 0.55), 0.20, fc=PAL[0], ec=PAL[0], alpha=0.30, lw=1.6))
    ax.add_patch(mp.Circle((0.72, 0.45), 0.18, fc=PAL[1], ec=PAL[1], alpha=0.30, lw=1.6))
    ax.text(0.28, 0.55, "$A$\n$\\mathbf{P}=0.3$", ha="center", va="center", fontsize=10.5)
    ax.text(0.72, 0.45, "$B$\n$\\mathbf{P}=0.25$", ha="center", va="center", fontsize=10.5)
    ax.text(0.5, 1.30, "DISJOINT  (mutually exclusive)", ha="center", va="center",
            fontsize=10.5, fontweight="600", color=PAL[7])
    ax.text(0.5, -0.10, "$\\mathbf{P}(A\\cap B)=0$", ha="center", va="center", fontsize=10.5)
    ax.text(0.5, -0.23, "$\\mathbf{P}(A)\\mathbf{P}(B)=0.075\\neq 0$ , so NOT independent",
            ha="center", va="center", fontsize=10, color=PAL[7])

    ax = axs[1]
    a, b = 0.4, 0.5
    ax.add_patch(mp.Rectangle((0, 0), 1, 1, fc="white", ec=AXIS_C, lw=1.2))
    ax.add_patch(mp.Rectangle((0, 0), a, 1, fc=PAL[0], ec=PAL[0], alpha=0.22, lw=1.6))
    ax.add_patch(mp.Rectangle((0, 0), 1, b, fc=PAL[1], ec=PAL[1], alpha=0.22, lw=1.6))
    ax.add_patch(mp.Rectangle((0, 0), a, b, fc=PAL[2], ec=PAL[2], alpha=0.45, lw=1.8))
    ax.text(0.20, 0.80, "$A$", ha="center", va="center", fontsize=12, color=PAL[0])
    ax.text(0.80, 0.24, "$B$", ha="center", va="center", fontsize=12, color=PAL[1])
    ax.text(0.20, 0.24, "$A\\cap B$", ha="center", va="center", fontsize=10.5, color="#0a5c3f")
    ax.plot([0, a], [1.05, 1.05], color=PAL[0], lw=2)
    ax.text(a / 2, 1.09, "$\\mathbf{P}(A)=0.4$", ha="center", va="bottom", fontsize=9.5, color=PAL[0])
    ax.plot([1.03, 1.03], [0, b], color=PAL[1], lw=2)
    ax.text(1.05, b / 2, "$\\mathbf{P}(B)=0.5$", ha="left", va="center", fontsize=9.5,
            color=PAL[1], rotation=90)
    ax.text(0.5, 1.30, "INDEPENDENT  (overlap is exactly the product)", ha="center",
            va="center", fontsize=10.5, fontweight="600", color=PAL[5])
    ax.text(0.5, -0.10, "$\\mathbf{P}(A\\cap B)=0.2$", ha="center", va="center", fontsize=10.5)
    ax.text(0.5, -0.23, "$\\mathbf{P}(A)\\mathbf{P}(B)=0.4\\cdot 0.5=0.2$ , so independent",
            ha="center", va="center", fontsize=10, color=PAL[5])
    fig.subplots_adjust(wspace=0.25)
    save(fig, "indep_disjoint")


# ================================================= Fig 3.3  conditioning kills indep.
def fig_cond_venn():
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    diagram_ax(ax)
    ax.set_xlim(-0.05, 1.42)
    ax.set_ylim(-0.42, 1.14)
    ax.add_patch(mp.Rectangle((0, 0), 1.25, 1, fc="white", ec=AXIS_C, lw=1.2))
    ax.add_patch(mp.Ellipse((0.35, 0.55), 0.56, 0.52, fc=PAL[0], ec=PAL[0], alpha=0.22, lw=1.6))
    ax.add_patch(mp.Ellipse((0.88, 0.48), 0.64, 0.56, fc=PAL[1], ec=PAL[1], alpha=0.22, lw=1.6))
    ax.add_patch(mp.Ellipse((0.60, 0.70), 1.02, 0.10, fc=PAL[3], ec="#8a5f00",
                            alpha=0.45, lw=1.6))
    ax.text(0.22, 0.44, "$A$", ha="center", va="center", fontsize=13, color=PAL[0])
    ax.text(1.03, 0.32, "$B$", ha="center", va="center", fontsize=13, color=PAL[1])
    ax.annotate("$A\\cap B$", xy=(0.59, 0.47), xytext=(0.60, 0.10), fontsize=10,
                color="#7a4a12", ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color="#7a4a12", lw=1.1))
    # C is labelled off to the right of the sliver's tip, clear of the B∩C leader
    ax.annotate("$C$", xy=(1.11, 0.695), xytext=(1.33, 0.50), fontsize=13, color="#8a5f00",
                ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color="#8a5f00", lw=1.1))
    # the sliver is only 0.10 tall, so both labels sit outside it on short leader lines
    ax.annotate("$A\\cap C$", xy=(0.27, 0.705), xytext=(0.16, 0.92), fontsize=9.5,
                color="#8a5f00", ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color="#8a5f00", lw=1.0))
    ax.annotate("$B\\cap C$", xy=(0.93, 0.705), xytext=(1.00, 0.92), fontsize=9.5,
                color="#8a5f00", ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color="#8a5f00", lw=1.0))
    ax.text(0.62, -0.16, "Inside the sliver $C$ the $A$-part and the $B$-part never meet:",
            ha="center", va="center", fontsize=10)
    ax.text(0.62, -0.31,
            "$\\mathbf{P}(A\\cap B\\,|\\,C)=0$ while $\\mathbf{P}(A|C)\\,\\mathbf{P}(B|C)>0$.",
            ha="center", va="center", fontsize=10.5, color=PAL[7])
    save(fig, "cond_venn")


# ================================================= Fig 3.4  two unfair coins tree
def fig_twocoin_tree():
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ax.axis("off")
    ys3 = [7 - i for i in range(8)]
    ys2 = [(ys3[2 * i] + ys3[2 * i + 1]) / 2 for i in range(4)]
    ys1 = [(ys2[0] + ys2[1]) / 2, (ys2[2] + ys2[3]) / 2]
    y0 = (ys1[0] + ys1[1]) / 2

    def edge(x0, ya, x1, yb, lab, up, col):
        ax.plot([x0, x1], [ya, yb], color=AXIS_C, lw=1.4, zorder=1)
        ax.text((x0 + x1) / 2, (ya + yb) / 2 + (0.16 if up else -0.16), lab,
                ha="center", va="bottom" if up else "top", fontsize=9, color=col)

    edge(0.05, y0, 1.0, ys1[0], "$0.5$", True, MUTED)
    edge(0.05, y0, 1.0, ys1[1], "$0.5$", False, MUTED)
    biases = [0.9, 0.1]
    for c in (0, 1):
        q = biases[c]
        for j in (0, 1):
            k = 2 * c + j
            edge(1.35, ys1[c], 2.2, ys2[k], f"${q if j == 0 else round(1 - q, 1)}$",
                 j == 0, PAL[0] if j == 0 else PAL[1])
            for m in (0, 1):
                edge(2.2, ys2[k], 3.1, ys3[2 * k + m],
                     f"${q if m == 0 else round(1 - q, 1)}$", m == 0,
                     PAL[0] if m == 0 else PAL[1])
    ax.plot([0.05], [y0], "o", ms=6, color=INK, zorder=3)
    ax.text(1.18, ys1[0], "Coin $A$", ha="center", va="center", fontsize=10.5,
            color=PAL[0], bbox=dict(fc="white", ec=PAL[0], lw=1.2, boxstyle="round,pad=0.25"))
    ax.text(1.18, ys1[1], "Coin $B$", ha="center", va="center", fontsize=10.5,
            color=PAL[1], bbox=dict(fc="white", ec=PAL[1], lw=1.2, boxstyle="round,pad=0.25"))
    for y in ys2:
        ax.plot([2.2], [y], "o", ms=5, color=INK, zorder=3)
    labs = ["HH", "HT", "TH", "TT"] * 2
    pr = [0.5 * 0.81, 0.5 * 0.09, 0.5 * 0.09, 0.5 * 0.01,
          0.5 * 0.01, 0.5 * 0.09, 0.5 * 0.09, 0.5 * 0.81]
    for i, y in enumerate(ys3):
        ax.plot([3.1], [y], "o", ms=5, color=INK, zorder=3)
        ax.text(3.22, y, labs[i], ha="left", va="center", fontsize=10)
        ax.text(3.68, y, f"{pr[i]:.3f}", ha="left", va="center", fontsize=9.5, color=MUTED)
    ax.text(0.05, 7.8, "pick coin", ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(2.2, 7.8, "toss 1", ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(3.1, 7.8, "toss 2", ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(3.68, 7.8, "prob.", ha="left", va="center", fontsize=9, color=MUTED)
    ax.text(1.7, -0.7, "$\\mathbf{P}(H_1\\cap H_2)=0.5(0.81)+0.5(0.01)=0.41"
                       "\\;\\neq\\;0.25=\\mathbf{P}(H_1)\\mathbf{P}(H_2)$",
            ha="center", va="center", fontsize=10.5, color=PAL[7])
    ax.set_xlim(-0.3, 4.5)
    ax.set_ylim(-1.2, 8.2)
    save(fig, "twocoin_tree")


# ================================================= Fig 3.5  posterior / predictive
def fig_posterior():
    q, prior = 0.9, 0.5
    ks = np.arange(0, 13)
    post = np.array([prior * q ** k / (prior * q ** k + (1 - prior) * (1 - q) ** k) for k in ks])
    pred = post * q + (1 - post) * (1 - q)
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    ax.plot(ks, post, "o-", color=PAL[0], label="$\\mathbf{P}(\\mathrm{coin}\\,A \\mid k$ heads$)$")
    ax.plot(ks, pred, "s-", color=PAL[1],
            label="$\\mathbf{P}(\\mathrm{toss}\\;k{+}1 = H \\mid k$ heads$)$")
    ax.axhline(0.5, color=MUTED, ls="--", lw=1.2)
    ax.text(11.8, 0.53, "unconditional $\\mathbf{P}(H)=0.5$", ha="right", va="bottom",
            fontsize=9, color=MUTED)
    ax.axhline(0.9, color=GRID_C, lw=1.0)
    ax.annotate("$k=10$:  $0.9000$ (to 4 d.p.)", xy=(10, pred[10]), xytext=(6.0, 0.70),
                fontsize=9.5, color=PAL[1],
                arrowprops=dict(arrowstyle="->", color=PAL[1], lw=1.2))
    ax.set_xlabel("$k$ = number of heads observed in the first $k$ tosses")
    ax.set_ylabel("probability")
    ax.set_ylim(0.4, 1.06)
    ax.set_xlim(-0.4, 12.4)
    ax.set_xticks(range(0, 13, 2))
    ax.legend(loc="lower right")
    save(fig, "posterior")


# ================================================= Fig 3.6  2x2 grid pairwise
def fig_grid22():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.6))
    cells = {"HH": (0, 1), "HT": (1, 1), "TH": (0, 0), "TT": (1, 0)}
    sets = [("$A$ = 1st toss $H$", {"HH", "HT"}, PAL[0]),
            ("$B$ = 2nd toss $H$", {"HH", "TH"}, PAL[1]),
            ("$C$ = same result", {"HH", "TT"}, PAL[2])]
    for ax, (title, S, col) in zip(axs, sets):
        diagram_ax(ax)
        ax.set_xlim(-0.08, 2.08)
        ax.set_ylim(-0.42, 2.30)
        for name, (cx, cy) in cells.items():
            inside = name in S
            ax.add_patch(mp.Rectangle((cx, cy), 1, 1, fc=col if inside else "white",
                                      alpha=0.32 if inside else 1.0, ec=AXIS_C, lw=1.2))
            ax.text(cx + 0.5, cy + 0.58, name, ha="center", va="center", fontsize=11,
                    fontweight="600" if inside else "normal",
                    color=INK if inside else MUTED)
            ax.text(cx + 0.5, cy + 0.30, "$1/4$", ha="center", va="center", fontsize=9,
                    color=MUTED)
        ax.text(1.0, 2.14, title, ha="center", va="center", fontsize=10.5, color=col,
                fontweight="600")
        ax.text(1.0, -0.28, "$\\mathbf{P}=1/2$", ha="center", va="center", fontsize=10)
    fig.subplots_adjust(wspace=0.12)
    save(fig, "grid22")


# ================================================= Fig 3.7  decision flowchart
def fig_flow():
    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    ax.axis("off")
    ax.set_xlim(-0.45, 10.45)
    ax.set_ylim(-0.2, 10.2)

    def box(x, y, w, h, txt, fc, ec, fs=9.5):
        ax.add_patch(mp.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                       boxstyle="round,pad=0.14", fc=fc, ec=ec, lw=1.4))
        ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=INK)

    def arrow(x0, y0, x1, y1, lab="", dx=0.0, dy=0.0):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4,
                                    shrinkA=2, shrinkB=2))
        if lab:
            ax.text((x0 + x1) / 2 + dx, (y0 + y1) / 2 + dy, lab, ha="center", va="center",
                    fontsize=9, color=PAL[7],
                    bbox=dict(fc="white", ec="none", pad=1.2))

    box(5, 9.2, 6.4, 1.0, "How many events?", "#f6f5f0", AXIS_C, 10.5)
    box(2.1, 7.0, 3.6, 1.2, "two: $A,B$", "white", PAL[0])
    box(7.6, 7.0, 4.0, 1.2, "a collection\n$A_1,\\dots,A_n$", "white", PAL[2])
    arrow(3.6, 8.7, 2.1, 7.65)
    arrow(6.4, 8.7, 7.6, 7.65)

    box(2.1, 4.6, 4.2, 1.5,
        "check ONE equation\n$\\mathbf{P}(A\\cap B)=\\mathbf{P}(A)\\mathbf{P}(B)$", "white", PAL[0])
    arrow(2.1, 6.35, 2.1, 5.4)
    box(7.6, 4.6, 4.4, 1.5,
        "check ALL $2^n-n-1$ subsets\n(pairwise is NOT enough)", "white", PAL[2])
    arrow(7.6, 6.35, 7.6, 5.4)

    box(5, 2.4, 8.6, 1.5,
        "Is the question conditional on some $C$?\nIf yes, redo the SAME check with "
        "$\\mathbf{P}(\\cdot\\,|\\,C)$ everywhere.", "#fdf6e6", PAL[3])
    arrow(2.1, 3.85, 4.0, 3.2)
    arrow(7.6, 3.85, 6.0, 3.2)
    box(5, 0.55, 8.6, 0.9,
        "Never conclude independence from “disjoint” or from a picture — compute.",
        "#fdeeee", PAL[7], 9.5)
    arrow(5, 1.6, 5, 1.05)
    save(fig, "flow")


# ================================================= Fig 3.8  random-walk paths
def fig_walk():
    p = 0.6
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.set_axisbelow(True)
    seqs = [(a, b, c) for a in "FB" for b in "FB" for c in "FB"]
    hl = {("F", "F", "B"), ("F", "B", "F"), ("B", "F", "F")}
    for s in seqs:
        ys = [0]
        for st in s:
            ys.append(ys[-1] + (1 if st == "F" else -1))
        end = ys[-1]
        if s in hl:
            col = PAL[0] if s[0] == "F" else PAL[1]
            ax.plot(range(4), ys, "-o", color=col, lw=2.2, ms=5, zorder=3, alpha=0.95)
            # stack the three labels clear of the y = 1 guide line
            ax.text(3.12, end + (0.95 if s == ("F", "F", "B") else
                                 (0.40 if s == ("F", "B", "F") else -0.40)),
                    "".join(s) + f":  ${p}^2({1 - p:.1f})=0.144$",
                    ha="left", va="center", fontsize=9.5, color=col,
                    bbox=dict(fc="white", ec="none", pad=1.6))
        else:
            ax.plot(range(4), ys, "-", color=GRID_C, lw=1.6, zorder=1)
            ax.plot(range(4), ys, "o", color=GRID_C, ms=4, zorder=1)
    # stop the guide line at the last path node so it never runs through the label column
    ax.plot([-0.45, 3.05], [1, 1], color=PAL[2], ls="--", lw=1.3, zorder=0)
    ax.text(-0.35, 1.28, "target: $+1$", fontsize=9.5, color=PAL[2])
    ax.set_xlabel("step number")
    ax.set_ylabel("position on the rope")
    ax.set_xticks(range(4))
    ax.set_yticks(range(-3, 4))
    ax.set_xlim(-0.45, 5.6)
    ax.set_ylim(-3.6, 3.6)
    ax.set_title("All $2^3=8$ three-step paths;  the three reaching $+1$ are highlighted "
                 "($2$ of them start with $F$)")
    ax.text(3.08, -2.4, "$\\mathbf{P}(+1\\text{ after }3)=3(0.144)=0.432$",
            fontsize=10, color=INK)
    ax.text(3.08, -3.0, "$\\mathbf{P}(\\text{1st step }F\\mid +1)=2/3$",
            fontsize=10, color=INK)
    save(fig, "walk")


# ================================================= Fig 3.9  channel diagram
def fig_channel():
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    diagram_ax(ax)
    ax.set_xlim(-0.9, 5.2)
    ax.set_ylim(-1.15, 2.7)
    xs, xr = 0.0, 4.0
    for y, lab in ((2.0, "0"), (0.0, "1")):
        ax.text(xs, y, lab, ha="center", va="center", fontsize=13,
                bbox=dict(fc="white", ec=PAL[0], lw=1.5, boxstyle="circle,pad=0.30"))
        ax.text(xr, y, lab, ha="center", va="center", fontsize=13,
                bbox=dict(fc="white", ec=PAL[2], lw=1.5, boxstyle="circle,pad=0.30"))

    def arr(y0, y1, col, lab, lx, ly, va="center"):
        ax.annotate("", xy=(xr - 0.42, y1), xytext=(xs + 0.42, y0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6))
        ax.text(lx, ly, lab, ha="center", va=va, fontsize=10, color=col,
                bbox=dict(fc="white", ec="none", pad=1.5))

    arr(2.0, 2.0, PAL[5], "$1-\\epsilon_0 = 0.95$", 2.0, 2.20, "bottom")
    arr(0.0, 0.0, PAL[5], "$1-\\epsilon_1 = 0.90$", 2.0, -0.22, "top")
    arr(2.0, 0.0, PAL[7], "$\\epsilon_0 = 0.05$", 1.15, 1.35)
    arr(0.0, 2.0, PAL[7], "$\\epsilon_1 = 0.10$", 1.15, 0.68)
    ax.text(xs, 2.62, "transmitted", ha="center", va="center", fontsize=9.5, color=MUTED)
    ax.text(xr, 2.62, "received", ha="center", va="center", fontsize=9.5, color=MUTED)
    ax.text(xs - 0.80, 2.0, "$p=0.6$", ha="center", va="center", fontsize=9.5, color=MUTED)
    ax.text(xs - 0.80, 0.0, "$1-p=0.4$", ha="center", va="center", fontsize=9.5, color=MUTED)
    ax.text(2.0, -0.95, "Errors in different transmissions are independent.",
            ha="center", va="center", fontsize=9.5, color=MUTED)
    save(fig, "channel")


# ================================================= Fig 3.10  repetition-code curve
def fig_repcode():
    def err(n, eps):
        return sum(comb(n, k) * eps ** k * (1 - eps) ** (n - k)
                   for k in range((n + 1) // 2, n + 1))

    ns = list(range(1, 16, 2))
    fig, ax = plt.subplots(figsize=(6.9, 4.2))
    for i, eps in enumerate([0.45, 0.30, 0.20, 0.10, 0.05]):
        ys = [err(n, eps) for n in ns]
        ax.semilogy(ns, ys, "o-", color=PAL[[7, 1, 3, 0, 5][i]], ms=5,
                    label=f"$\\epsilon = {eps:.2f}$")
    ax.set_xlabel("$n$ = number of repetitions (odd)")
    ax.set_ylabel("$\\mathbf{P}(\\text{majority decoder wrong})$")
    ax.set_xticks(ns)
    ax.set_ylim(1e-7, 1.0)
    ax.grid(True, which="both", axis="y")
    ax.legend(loc="lower left", ncols=2)
    ax.set_title("Repetition coding: error falls geometrically iff $\\epsilon < 1/2$")
    save(fig, "repcode")


fig_tree3()
fig_indep_disjoint()
fig_cond_venn()
fig_twocoin_tree()
fig_posterior()
fig_grid22()
fig_flow()
fig_walk()
fig_channel()
fig_repcode()
print("done")
