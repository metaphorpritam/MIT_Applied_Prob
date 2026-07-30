# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for note G2 section 2 (Expectation). Sources: L05 slides 6-7, rec05 P2-P4."""
from __future__ import annotations
import random
import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mpl_style import setup, diagram_ax, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon, FancyArrowPatch  # noqa: E402
import numpy as np  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL


def save(fig, name):
    p = IMG / f"g2_s2_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ----------------------------------------------------- Fig 2.1 center of mass
def fig_centermass():
    xs = [1, 2, 3, 6]
    ps = [0.10, 0.50, 0.25, 0.15]
    mean = sum(x * p for x, p in zip(xs, ps))  # 2.75
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 5.6),
                                   gridspec_kw={"height_ratios": [1.15, 1.0]})

    # --- top: the PMF itself
    ax1.vlines(xs, 0, ps, color=BLUE, linewidth=3)
    ax1.plot(xs, ps, "o", color=BLUE, markersize=8)
    for x, p in zip(xs, ps):
        ax1.annotate(f"{p:.2f}", (x, p), textcoords="offset points", xytext=(0, 9),
                     ha="center", fontsize=9, color=INK)
    ax1.axvline(mean, color=ORANGE, linewidth=2, linestyle="--")
    ax1.annotate(f"E[X] = {mean}", (mean + 0.12, 0.545), color=ORANGE, fontsize=10,
                 ha="left", va="bottom", fontweight="bold")
    ax1.set_xlim(0.2, 6.8)
    ax1.set_ylim(0, 0.66)
    ax1.set_xticks([0, 1, 2, 3, 4, 5, 6])
    ax1.set_yticks([0, 0.2, 0.4])
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$p_X(x)$")
    ax1.set_title("PMF: mass 0.10, 0.50, 0.25, 0.15 at $x = 1, 2, 3, 6$")

    # --- bottom: the same masses as weights on a beam
    diagram_ax(ax2)
    ax2.set_aspect("auto")
    ax2.plot([0.4, 6.8], [0, 0], color=INK, linewidth=3, solid_capstyle="round", zorder=3)
    for x, p in zip(xs, ps):
        w = 0.16 + 0.55 * p
        h = 0.10 + 0.72 * p
        ax2.add_patch(Rectangle((x - w / 2, 0.02), w, h, facecolor=BLUE,
                                edgecolor=BLUE, alpha=0.85, zorder=4))
        ax2.text(x, 0.04 + h, f"{p:.2f}", ha="center", va="bottom", fontsize=9, color=INK)
        ax2.text(x, -0.14, f"x={x}", ha="center", va="top", fontsize=9, color=MUTED)
    # fulcrum
    ax2.add_patch(Polygon([[mean, -0.02], [mean - 0.22, -0.42], [mean + 0.22, -0.42]],
                          closed=True, facecolor=ORANGE, edgecolor=ORANGE, zorder=5))
    ax2.text(mean, -0.50, f"fulcrum at E[X] = {mean}", ha="center", va="top",
             fontsize=10, color=ORANGE, fontweight="bold")
    # torque arrows
    ax2.annotate("", xy=(1.05, 1.02), xytext=(2.68, 1.02),
                 arrowprops=dict(arrowstyle="-|>", color=GREEN, linewidth=1.8))
    ax2.text(1.86, 1.10, "left torque  $-0.55$", ha="center", va="bottom",
             fontsize=9.5, color=GREEN)
    ax2.annotate("", xy=(6.0, 1.02), xytext=(2.82, 1.02),
                 arrowprops=dict(arrowstyle="-|>", color=RED, linewidth=1.8))
    ax2.text(4.4, 1.10, "right torque  $+0.55$", ha="center", va="bottom",
             fontsize=9.5, color=RED)
    ax2.plot([mean, mean], [-0.02, 1.02], color=ORANGE, linewidth=1.0, linestyle=":", zorder=2)
    ax2.set_xlim(0.2, 6.8)
    ax2.set_ylim(-0.85, 1.45)
    fig.tight_layout(h_pad=1.4)
    save(fig, "centermass")


# --------------------------------------------------------- Fig 2.2 marksman
def fig_marksman():
    n, p = 10, 0.2
    ks = np.arange(n + 1)
    pmf = np.array([comb(n, int(k)) * p ** int(k) * (1 - p) ** (n - int(k)) for k in ks])
    tail = pmf[6:].sum()
    fig, (ax, axz) = plt.subplots(1, 2, figsize=(8.6, 3.9),
                                  gridspec_kw={"width_ratios": [1.55, 1.0]})

    for k in ks:
        c = RED if k >= 6 else BLUE
        ax.vlines(k, 0, pmf[k], color=c, linewidth=3)
        ax.plot([k], [pmf[k]], "o", color=c, markersize=6.5)
    for k in range(6):
        ax.annotate(f"{pmf[k]:.4f}", (k, pmf[k]), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8, color=MUTED)
    ax.plot([2.0], [-0.004], marker="^", color=ORANGE, markersize=13, clip_on=False, zorder=6)
    ax.annotate("E[X] = 2\n(center of gravity)", xy=(2.05, 0.004), xytext=(3.1, 0.318),
                color=ORANGE, fontsize=9.5, fontweight="bold", ha="left",
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, linewidth=1.4))
    ax.axvspan(5.5, 10.5, color=RED, alpha=0.07)
    ax.annotate(f"more hits than misses\n$X \\geq 6$:  {tail:.6f}",
                xy=(6.0, 0.0056), xytext=(6.4, 0.20), fontsize=9, color=RED,
                ha="left", arrowprops=dict(arrowstyle="-|>", color=RED, linewidth=1.4))
    ax.set_xticks(list(range(11)))
    ax.set_xlim(-0.6, 10.6)
    ax.set_ylim(0, 0.385)
    ax.set_xlabel("$k$ = number of hits")
    ax.set_ylabel("$p_X(k)$")
    ax.set_title("Binomial(10, 0.2) PMF")

    axz.vlines(range(6, 11), 0, pmf[6:], color=RED, linewidth=3)
    axz.plot(range(6, 11), pmf[6:], "o", color=RED, markersize=6.5)
    for k in range(6, 11):
        axz.annotate(f"{pmf[k]:.2e}", (k, pmf[k]), textcoords="offset points",
                     xytext=(0, 8), ha="center", fontsize=8, color=MUTED)
    axz.set_yscale("log")
    axz.set_ylim(3e-8, 9e-2)
    axz.set_xticks(list(range(6, 11)))
    axz.set_xlim(5.4, 10.6)
    axz.set_xlabel("$k$")
    axz.set_ylabel("$p_X(k)$  (log scale)")
    axz.set_title("The upper tail, magnified")
    fig.tight_layout(w_pad=2.0)
    save(fig, "marksman")


# --------------------------------------------------------- Fig 2.3 bus bias
def fig_busbias():
    sizes = [40, 33, 25, 50]
    tot = sum(sizes)
    EX = sum(s * s for s in sizes) / tot
    EY = sum(sizes) / len(sizes)
    fig = plt.figure(figsize=(9.2, 4.6))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.15], height_ratios=[1, 1],
                          hspace=0.75, wspace=0.28)
    axb = fig.add_subplot(gs[:, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, 1])

    # left: the four buses, area proportional to load
    diagram_ax(axb)
    axb.set_aspect("auto")
    y = 0
    for s in reversed(sizes):
        w = s / 50 * 5.4
        axb.add_patch(FancyBboxPatch((0.25, y), w, 0.62,
                                     boxstyle="round,pad=0.02,rounding_size=0.10",
                                     facecolor="#cfe0f6", edgecolor=BLUE, linewidth=1.6))
        axb.text(0.42, y + 0.31, f"{s} students", va="center", ha="left",
                 fontsize=10, color=INK)
        # dots for a couple of students
        axb.text(w + 0.42, y + 0.31, f"{s}/148 of all students",
                 va="center", ha="left", fontsize=8.5, color=MUTED)
        y += 0.92
    axb.set_xlim(0, 8.4)
    axb.set_ylim(-0.35, y + 0.15)
    axb.set_title("4 buses, 148 students (rec05 P3)", pad=8)
    axb.text(0.25, -0.30, "pick a DRIVER: each bus w.p. 1/4\n"
                          "pick a STUDENT: bus of size $x$ w.p. $x/148$",
             fontsize=9, color=MUTED, va="top", ha="left")

    for ax, probs, mean, ttl, col in (
        (ax1, [0.25] * 4, EY, "$p_Y$: driver picked uniformly", GREEN),
        (ax2, [s / tot for s in sizes], EX, "$p_X$: student picked uniformly", PURPLE),
    ):
        xs = sorted(sizes)
        pr = [probs[sizes.index(x)] for x in xs]
        ax.vlines(xs, 0, pr, color=col, linewidth=3)
        ax.plot(xs, pr, "o", color=col, markersize=6.5)
        for x, q in zip(xs, pr):
            ax.annotate(f"{q:.3f}", (x, q), textcoords="offset points", xytext=(0, 7),
                        ha="center", fontsize=8, color=MUTED)
        ax.axvline(mean, color=ORANGE, linewidth=1.8, linestyle="--")
        ax.annotate(f"mean {mean:.2f}", (mean + 0.7, 0.055), color=ORANGE,
                    fontsize=9.5, fontweight="bold", va="center")
        ax.set_xlim(20, 56)
        ax.set_ylim(0, 0.44)
        ax.set_xticks(sorted(sizes))
        ax.set_yticks([0, 0.2, 0.4])
        ax.set_title(ttl, fontsize=10)
        ax.set_xlabel("bus size")
    fig.tight_layout()
    save(fig, "busbias")


# ------------------------------------------------------ Fig 2.4 recipe flow
def fig_flowchart():
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    diagram_ax(ax)
    ax.set_aspect("auto")

    def box(x, y, w, h, txt, fc, ec, fs=9.5, weight="normal", linespacing=1.4):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.02,rounding_size=0.06",
                                    facecolor=fc, edgecolor=ec, linewidth=1.6, zorder=3))
        ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=INK,
                zorder=4, fontweight=weight, linespacing=linespacing)

    def diamond(x, y, w, h, txt, fs=9.5, linespacing=1.5):
        ax.add_patch(Polygon([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]],
                             closed=True, facecolor="#fde7cf", edgecolor=ORANGE,
                             linewidth=1.6, zorder=3))
        ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=INK, zorder=4,
                linespacing=linespacing)

    def arrow(x1, y1, x2, y2, label="", lx=0, ly=0, col=AXIS_C):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                     mutation_scale=13, color=col, linewidth=1.5, zorder=2))
        if label:
            ax.text(lx, ly, label, ha="center", va="center", fontsize=9,
                    color=MUTED, zorder=5,
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))

    box(6.0, 9.35, 5.0, 0.8, "Want $\\mathbb{E}[Y]$ where $Y = g(X)$", "#dbe8fa", BLUE,
        fs=11, weight="bold")
    arrow(6.0, 8.95, 6.0, 8.35)
    diamond(6.0, 7.65, 4.4, 1.25, "Is $g$ linear,\n$g(x) = \\alpha x + \\beta$ ?")
    arrow(3.8, 7.65, 2.75, 7.65, "yes", 3.28, 7.98, GREEN)
    box(1.42, 7.65, 2.6, 0.95, "$\\mathbb{E}[Y] = \\alpha\\,\\mathbb{E}[X] + \\beta$\n(L05 slide 7)",
        "#d5efe4", DGREEN, fs=9)
    arrow(6.0, 7.02, 6.0, 6.45, "no", 6.35, 6.74)
    diamond(6.0, 5.5, 4.4, 1.6,
            "Do you already have $p_X$,\nand is $\\sum_x g(x)p_X(x)$\ndoable?", fs=9,
            linespacing=1.95)
    arrow(3.8, 5.5, 2.75, 5.5, "yes", 3.28, 5.83, GREEN)
    box(1.42, 5.5, 2.6, 1.6,
        "EXPECTED\nVALUE RULE\n$\\mathbb{E}[g(X)] = \\sum_x g(x)p_X(x)$\n(rec05 P1a)",
        "#d5efe4", DGREEN, fs=8.5, linespacing=2.1)
    arrow(6.0, 4.70, 6.0, 4.10, "no", 6.35, 4.40)
    box(6.0, 3.28, 4.4, 1.5,
        "HARD ROUTE: build $p_Y$ first,\n$p_Y(y)=\\!\\!\\sum_{x:\\,g(x)=y}\\!\\! p_X(x)$,\n"
        "then $\\mathbb{E}[Y]=\\sum_y y\\,p_Y(y)$", "#f6dede", RED, fs=9, linespacing=2.5)
    arrow(1.42, 4.68, 1.42, 4.10)
    box(1.42, 3.28, 2.6, 1.5,
        "$g(x)=x^2$ gives the\nsecond moment\n$\\mathbb{E}[X^2]=\\sum_x x^2p_X(x)$\n"
        "$=\\operatorname{var}(X)+(\\mathbb{E}[X])^2$", "#e8e3f7", PURPLE, fs=8.5,
        linespacing=2.0)
    box(3.7, 1.55, 7.6, 0.9,
        "NEVER write $\\mathbb{E}[g(X)] = g(\\mathbb{E}[X])$ unless $g$ is linear\n"
        "(L05 slide 7 caution)", "#fdeaea", RED, fs=10, weight="bold")
    arrow(1.42, 2.50, 1.42, 2.05)
    arrow(6.0, 2.50, 6.0, 2.05)
    ax.set_xlim(-0.3, 8.5)
    ax.set_ylim(0.9, 10.0)
    fig.tight_layout()
    save(fig, "flowchart")


# ---------------------------------------------------- Fig 2.5 St. Petersburg
def fig_petersburg():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.9))

    K = 12
    ks = np.arange(1, K + 1)
    contrib = np.ones(K)
    ax1.bar(ks, contrib, width=0.55, color=BLUE, label="term $2^k\\cdot 2^{-k} = 1$")
    ax1.plot(ks, np.cumsum(contrib), "o-", color=ORANGE, markersize=5,
             label="partial sum $= m$")
    ax1.set_xticks(list(range(1, K + 1)))
    ax1.set_xlim(0.3, K + 0.7)
    ax1.set_ylim(0, 13.4)
    ax1.set_xlabel("$k$ (toss on which the first tail appears)")
    ax1.set_ylabel("dollars")
    ax1.set_title("Every term contributes exactly \\$1")
    ax1.legend(loc="upper left")

    rng = random.Random(6041)

    def play():
        k = 1
        while rng.random() < 0.5:
            k += 1
        return 2 ** k

    N = 20000
    for i, col in enumerate([BLUE, ORANGE, GREEN, PURPLE]):
        pay = np.array([play() for _ in range(N)], dtype=float)
        run = np.cumsum(pay) / np.arange(1, N + 1)
        ax2.plot(np.arange(1, N + 1), run, color=col, linewidth=1.3,
                 label=f"run {i+1}")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlim(1, N)
    ax2.set_xlabel("number of plays (log scale)")
    ax2.set_ylabel("running average payout, \\$ (log)")
    ax2.set_title("Sample averages never settle")
    ax2.legend(loc="lower right", ncol=2)
    fig.tight_layout(w_pad=2.0)
    save(fig, "petersburg")


fig_centermass()
fig_marksman()
fig_busbias()
fig_flowchart()
fig_petersburg()
print("done")
