# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for note fragment g2_s1 (L05 slides 2-5). Writes notes/img/g2_s1_*.png."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mpl_style import setup, diagram_ax, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, PAL = setup()
from matplotlib.patches import Rectangle, FancyArrowPatch, FancyBboxPatch  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL


def save(fig, name):
    p = IMG / f"g2_s1_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ------------------------------------------------------------------ Fig 1.1
def fig_die_min():
    """L05 slide 4: the 4x4 grid mapped through X = min(F,S), plus the PMF."""
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.6, 4.6),
                                   gridspec_kw={"width_ratios": [1.05, 1]})
    axL.set_aspect("equal")
    axL.grid(False)
    for i in range(4):        # i -> F = i+1 (column)
        for j in range(4):    # j -> S = j+1 (row)
            f, s = i + 1, j + 1
            m = min(f, s)
            hit = (m == 2)
            axL.add_patch(Rectangle((i, j), 1, 1,
                                    fc=(ORANGE if hit else "white"),
                                    alpha=(0.30 if hit else 1.0),
                                    ec=(ORANGE if hit else AXIS_C),
                                    lw=(2.0 if hit else 1.0), zorder=1))
            axL.text(i + 0.5, j + 0.62, f"({f},{s})", ha="center", va="center",
                     fontsize=7.5, color=MUTED, zorder=3)
            axL.text(i + 0.5, j + 0.30, f"min = {m}", ha="center", va="center",
                     fontsize=8.5, color=(ORANGE if hit else INK),
                     fontweight=("bold" if hit else "normal"), zorder=3)
    axL.set_xlim(-0.1, 4.1)
    axL.set_ylim(-0.1, 4.65)
    axL.set_xticks(np.arange(4) + 0.5)
    axL.set_xticklabels([1, 2, 3, 4])
    axL.set_yticks(np.arange(4) + 0.5)
    axL.set_yticklabels([1, 2, 3, 4])
    axL.set_xlabel("$F$ = first roll")
    axL.set_ylabel("$S$ = second roll")
    axL.set_title("$\\Omega$: 16 equally likely cells, each $1/16$", pad=8)
    axL.text(2.0, 4.28, "shaded: the 5 cells with $\\min(F,S)=2$",
             ha="center", va="center", fontsize=9, color=ORANGE, fontweight="600")
    for sp in ("left", "bottom"):
        axL.spines[sp].set_visible(False)
    axL.tick_params(length=0)

    ks = np.array([1, 2, 3, 4])
    pk = np.array([7, 5, 3, 1]) / 16
    cols = [BLUE, ORANGE, BLUE, BLUE]
    axR.vlines(ks, 0, pk, color=cols, lw=3)
    axR.scatter(ks, pk, s=55, color=cols, zorder=3)
    for k, v, c in zip(ks, pk, cols):
        axR.annotate(f"{int(v*16)}/16", (k, v), textcoords="offset points",
                     xytext=(0, 9), ha="center", fontsize=9, color=c, fontweight="600")
    axR.set_xlim(0.4, 4.6)
    axR.set_ylim(0, 0.55)
    axR.set_xticks(ks)
    axR.set_xlabel("$x$")
    axR.set_ylabel("$p_X(x)$")
    axR.set_title("PMF of $X=\\min(F,S)$   (total $16/16=1$)", pad=8)
    fig.tight_layout(w_pad=2.2)
    save(fig, "die_min")


# ------------------------------------------------------------------ Fig 1.2
def fig_named_pmfs():
    """Stem plots of the four named PMFs of L05 (slides 3, 5, 6)."""
    fig, axes = plt.subplots(2, 2, figsize=(10.4, 6.6))

    # (a) Bernoulli p = 0.3
    ax = axes[0, 0]
    p = 0.3
    ks, pk = np.array([0, 1]), np.array([1 - p, p])
    ax.vlines(ks, 0, pk, color=BLUE, lw=3)
    ax.scatter(ks, pk, s=55, color=BLUE, zorder=3)
    for k, v in zip(ks, pk):
        ax.annotate(f"{v:.2f}", (k, v), textcoords="offset points", xytext=(0, 9),
                    ha="center", fontsize=9, color=BLUE, fontweight="600")
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(0, 0.92)
    ax.set_xticks([0, 1])
    ax.set_title("(a) Bernoulli($p$),  $p=0.3$", pad=8)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$p_X(x)$")
    ax.text(1.02, 0.80, "$p_X(1)=p$\n$p_X(0)=1-p$", fontsize=9, color=MUTED,
            ha="center", va="top")

    # (b) discrete uniform on 0..n, n = 8
    ax = axes[0, 1]
    n = 8
    ks = np.arange(0, n + 1)
    pk = np.full(n + 1, 1 / (n + 1))
    ax.vlines(ks, 0, pk, color=GREEN, lw=3)
    ax.scatter(ks, pk, s=45, color=GREEN, zorder=3)
    ax.axhline(1 / (n + 1), color=GREEN, lw=1, ls="--", alpha=0.6)
    ax.text(n + 0.15, 1 / (n + 1) + 0.006, "$1/(n+1)$", fontsize=9, color=GREEN,
            ha="right", va="bottom", fontweight="600")
    ax.set_xlim(-0.7, n + 0.7)
    ax.set_ylim(0, 0.175)
    ax.set_xticks(ks)
    ax.set_title("(b) discrete uniform on $\\{0,\\dots,n\\}$,  $n=8$", pad=8)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$p_X(x)$")

    # (c) binomial n = 10, three p values
    ax = axes[1, 0]
    n = 10
    ks = np.arange(0, n + 1)
    for p, c, dx in [(0.2, GOLD, -0.16), (0.5, BLUE, 0.0), (0.8, PINK, 0.16)]:
        pk = np.array([math.comb(n, int(k)) * p ** k * (1 - p) ** (n - k) for k in ks])
        ax.vlines(ks + dx, 0, pk, color=c, lw=2.4)
        ax.scatter(ks + dx, pk, s=26, color=c, zorder=3, label=f"$p={p}$")
    ax.set_xlim(-0.7, n + 0.7)
    ax.set_ylim(0, 0.40)
    ax.set_xticks(ks)
    ax.set_title("(c) binomial($n,p$),  $n=10$", pad=8)
    ax.set_xlabel("$k$ = number of heads")
    ax.set_ylabel("$p_X(k)$")
    ax.legend(loc="upper center", ncol=3, fontsize=8.5)

    # (d) geometric, two p values
    ax = axes[1, 1]
    ks = np.arange(1, 13)
    for p, c, dx in [(0.3, ORANGE, -0.1), (0.5, PURPLE, 0.1)]:
        pk = (1 - p) ** (ks - 1) * p
        ax.vlines(ks + dx, 0, pk, color=c, lw=2.6)
        ax.scatter(ks + dx, pk, s=30, color=c, zorder=3, label=f"$p={p}$")
    ax.set_xlim(0.3, 12.7)
    ax.set_ylim(0, 0.62)
    ax.set_xticks(ks)
    ax.set_title("(d) geometric($p$): tosses until first head", pad=8)
    ax.set_xlabel("$k$ = number of tosses")
    ax.set_ylabel("$p_X(k)$")
    ax.legend(loc="upper right", fontsize=8.5)
    ax.text(6.6, 0.40, "each bar is $(1-p)$ times the one\nbefore it — geometric decay",
            fontsize=8.8, color=MUTED, ha="center", va="center")

    fig.tight_layout(h_pad=2.4, w_pad=2.4)
    save(fig, "named_pmfs")


# ------------------------------------------------------------------ Fig 1.3
def fig_flowchart():
    """Decision guide: which named PMF (if any) fits the experiment?"""
    fig, ax = plt.subplots(figsize=(10.4, 6.9))
    ax.set_xlim(0, 103)
    ax.set_ylim(0, 68)
    ax.axis("off")
    ax.grid(False)

    def box(x, y, w, h, text, fc, ec, fs=9.3, bold=False):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.6,rounding_size=1.4",
                                    fc=fc, ec=ec, lw=1.4, zorder=2))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
                zorder=3, fontweight=("600" if bold else "normal"))

    def arrow(x1, y1, x2, y2, label="", lx=0, ly=0, color=AXIS_C):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                     mutation_scale=13, color=color, lw=1.3,
                                     shrinkA=2, shrinkB=3, zorder=1))
        if label:
            ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, ha="center",
                    va="center", fontsize=8.6, color=MUTED, fontweight="600",
                    bbox=dict(fc="white", ec="none", pad=1.4), zorder=4)

    box(50, 64, 64, 6.4,
        "Experiment described.  What number does $X$ record?", "#f3f6fb", BLUE, 10, True)

    box(14, 50, 22, 8.0,
        "One yes/no trial;\n$X\\in\\{0,1\\}$ flags\nsuccess", "#fdf1ea", ORANGE, 8.8)
    box(38, 50, 22, 8.0,
        "Finitely many values,\nall equally likely", "#edf8f3", GREEN, 8.8)
    box(75, 50, 42, 8.0,
        "Repeated independent trials,\nsame success probability $p$ each", "#f3f6fb", BLUE, 8.8)

    arrow(30, 60.5, 16, 54.5)
    arrow(44, 60.5, 39, 54.5)
    arrow(66, 60.5, 73, 54.5)

    box(14, 35, 22, 9.0, "$\\mathbf{Bernoulli}(p)$\n$p_X(1)=p$\n$p_X(0)=1-p$",
        "#fdf1ea", ORANGE, 9.0)
    box(38, 35, 22, 9.0, "$\\mathbf{uniform}$ on $\\{a,\\dots,b\\}$\n$p_X(k)=\\dfrac{1}{b-a+1}$",
        "#edf8f3", GREEN, 9.0)
    arrow(14, 45.5, 14, 40.0)
    arrow(38, 45.5, 38, 40.0)

    box(75, 35.5, 32, 7.4,
        "Is the number of trials\nfixed in advance?", "#ffffff", AXIS_C, 9.0)
    arrow(75, 45.5, 75, 39.7)

    box(62, 18, 26, 10.0,
        "$\\mathbf{binomial}(n,p)$\n$p_X(k)=\\binom{n}{k}p^k(1-p)^{n-k}$\n$k=0,1,\\dots,n$",
        "#f3f6fb", BLUE, 8.8)
    box(90, 18, 18, 10.0,
        "$\\mathbf{geometric}(p)$\n$p_X(k)=(1-p)^{k-1}p$\n$k=1,2,\\dots$",
        "#f6f2fb", PURPLE, 8.4)
    arrow(70, 31.2, 63, 24.0)
    ax.text(52.5, 27.5, "yes — $n$ fixed,\n$X$ = #successes", ha="center", va="center",
            fontsize=8.4, color=MUTED, fontweight="600")
    arrow(80, 31.2, 88, 24.0)
    ax.text(94.5, 28.0, "no — stop at the\nfirst success,\n$X$ = #trials", ha="center",
            va="center", fontsize=8.4, color=MUTED, fontweight="600")

    box(26, 7.0, 48, 9.0,
        "$\\mathbf{Otherwise}$ (trials dependent, $p$ changes trial to trial,\n"
        "values unequally likely, \u2026): use the general recipe \u2014 collect\n"
        "the outcomes with $X=x$ and add their probabilities.",
        "#faf6ec", GOLD, 8.8)

    ax.text(80, 3.0, "L05 slides 3, 5, 6 \u00b7 B&T \u00a72.2 (Bernoulli)",
            ha="center", fontsize=8.4, color=MUTED)
    fig.tight_layout()
    save(fig, "flowchart")


fig_die_min()
fig_named_pmfs()
fig_flowchart()
print("done")
