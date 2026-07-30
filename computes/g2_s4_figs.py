# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for G2 section 4 — Joint PMFs and multiple random variables.

Run:  uv run computes/g2_s4_figs.py
"""
from __future__ import annotations

import sys
from fractions import Fraction as F
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
    p = IMG / f"g2_s4_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


def fs(x: F) -> str:
    if x == 0:
        return "0"
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


BLUE, ORANGE, GREEN, GOLD = PAL[0], PAL[1], PAL[2], PAL[3]

NUM = {
    (1, 4): 1, (2, 4): 2, (3, 4): 2, (4, 4): 0,
    (1, 3): 2, (2, 3): 4, (3, 3): 1, (4, 3): 2,
    (1, 2): 0, (2, 2): 1, (3, 2): 3, (4, 2): 1,
    (1, 1): 0, (2, 1): 1, (3, 1): 0, (4, 1): 0,
}
JOINT = {k: F(v, 20) for k, v in NUM.items()}


def raw20(x, y) -> str:
    """Cell label kept over the slide's common denominator 20."""
    n = NUM[(x, y)]
    return f"{n}/20" if n else "0"


def shade(p: F, pmax: F):
    """Light blue tint proportional to probability."""
    t = float(p / pmax) if pmax else 0.0
    return (1 - 0.72 * t, 1 - 0.42 * t, 1 - 0.13 * t)


# ============================================== Fig 4.1  joint grid with marginals
def fig_grid():
    fig, ax = plt.subplots(figsize=(7.4, 6.2))
    diagram_ax(ax)
    pmax = max(JOINT.values())
    pX = {x: sum(JOINT[(x, y)] for y in range(1, 5)) for x in range(1, 5)}
    pY = {y: sum(JOINT[(x, y)] for x in range(1, 5)) for y in range(1, 5)}

    for x in range(1, 5):
        for y in range(1, 5):
            p = JOINT[(x, y)]
            ax.add_patch(mp.Rectangle((x - 0.5, y - 0.5), 1, 1,
                                      facecolor=shade(p, pmax), edgecolor=AXIS_C, lw=1.0))
            ax.text(x, y, raw20(x, y),
                    ha="center", va="center", fontsize=11,
                    color=INK if p > 0 else "#b6b5ac",
                    fontweight="600" if p > 0 else "normal")
    # marginal of X : strip below (y from -0.9 to -0.1)
    for x in range(1, 5):
        ax.add_patch(mp.Rectangle((x - 0.5, -1.05), 1, 0.8,
                                  facecolor="#fdf0e8", edgecolor=ORANGE, lw=1.0))
        ax.text(x, -0.65, f"{sum(NUM[(x, yy)] for yy in range(1, 5))}/20",
                ha="center", va="center",
                fontsize=10.5, color=ORANGE, fontweight="600")
    ax.text(-0.05, -0.65, r"$p_X(x)\;\rightarrow$", ha="right", va="center",
            fontsize=11, color=ORANGE)
    # marginal of Y : strip right
    for y in range(1, 5):
        ax.add_patch(mp.Rectangle((4.7, y - 0.4), 0.8, 0.8,
                                  facecolor="#e8f6f0", edgecolor=GREEN, lw=1.0))
        ax.text(5.1, y, f"{sum(NUM[(xx, y)] for xx in range(1, 5))}/20",
                ha="center", va="center",
                fontsize=10.5, color=GREEN, fontweight="600")
    ax.text(5.1, 4.75, r"$p_Y(y)$", ha="center", va="center", fontsize=11, color=GREEN)
    # axis ticks
    for x in range(1, 5):
        ax.text(x, 4.62, str(x), ha="center", va="center", fontsize=10, color=MUTED)
    ax.text(2.5, 5.05, r"$x$", ha="center", va="center", fontsize=12, color=INK)
    for y in range(1, 5):
        ax.text(0.3, y, str(y), ha="center", va="center", fontsize=10, color=MUTED)
    ax.text(0.0, 2.5, r"$y$", ha="center", va="center", fontsize=12, color=INK)
    ax.text(2.5, -1.45, "cells: $p_{X,Y}(x,y)$   ·   orange strip: $p_X$   ·   green strip: $p_Y$",
            ha="center", va="center", fontsize=9.5, color=MUTED, style="italic")
    ax.set_xlim(-1.6, 5.8)
    ax.set_ylim(-1.8, 5.3)
    save(fig, "grid")


# ============================================== Fig 4.2  renormalization before/after
def fig_renorm():
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.6))
    pmax = max(JOINT.values())
    B = [(x, y) for (x, y) in JOINT if x <= 2 and y >= 3]
    PB = sum(JOINT[c] for c in B)

    ax = axes[0]
    diagram_ax(ax)
    for x in range(1, 5):
        for y in range(1, 5):
            p = JOINT[(x, y)]
            inB = (x, y) in B
            ax.add_patch(mp.Rectangle((x - 0.5, y - 0.5), 1, 1,
                                      facecolor=shade(p, pmax) if not inB else "#fdeee6",
                                      edgecolor=ORANGE if inB else AXIS_C,
                                      lw=1.8 if inB else 1.0, zorder=2 if inB else 1))
            ax.text(x, y, raw20(x, y), ha="center", va="center",
                    fontsize=10.5, zorder=3,
                    color=ORANGE if inB else (INK if p > 0 else "#b6b5ac"),
                    fontweight="600" if inB else "normal")
    ax.add_patch(mp.Rectangle((0.5, 2.5), 2, 2, fill=False,
                              edgecolor=ORANGE, lw=2.4, zorder=4))
    ax.set_title("before: full joint PMF,  $\\mathbf{P}(B)=9/20$", color=INK)
    ax.text(2.5, 5.02, r"$B=\{X\leq 2,\ Y\geq 3\}$ outlined", ha="center",
            fontsize=9.5, color=ORANGE)
    for x in range(1, 5):
        ax.text(x, 0.18, str(x), ha="center", fontsize=9, color=MUTED)
    for y in range(1, 5):
        ax.text(0.3, y, str(y), ha="center", va="center", fontsize=9, color=MUTED)
    ax.set_xlim(0.0, 5.0)
    ax.set_ylim(0.0, 5.4)

    ax = axes[1]
    diagram_ax(ax)
    cmax = max(JOINT[c] / PB for c in B)
    for x in range(1, 5):
        for y in range(1, 5):
            inB = (x, y) in B
            p = JOINT[(x, y)] / PB if inB else F(0)
            ax.add_patch(mp.Rectangle((x - 0.5, y - 0.5), 1, 1,
                                      facecolor=shade(p, cmax) if inB else "#f6f6f2",
                                      edgecolor=ORANGE if inB else AXIS_C,
                                      lw=1.8 if inB else 1.0))
            ax.text(x, y, fs(p) if inB else "0", ha="center", va="center",
                    fontsize=10.5,
                    color=INK if inB else "#c6c5bc",
                    fontweight="600" if inB else "normal")
    ax.set_title("after: divide each surviving cell by $9/20$", color=INK)
    ax.text(2.5, 5.02, "the four entries now sum to 1", ha="center",
            fontsize=9.5, color=MUTED)
    for x in range(1, 5):
        ax.text(x, 0.18, str(x), ha="center", fontsize=9, color=MUTED)
    for y in range(1, 5):
        ax.text(0.3, y, str(y), ha="center", va="center", fontsize=9, color=MUTED)
    ax.set_xlim(0.0, 5.0)
    ax.set_ylim(0.0, 5.4)
    fig.tight_layout()
    save(fig, "renorm")


# ============================================== Fig 4.3  decision flowchart
def fig_flow():
    fig, ax = plt.subplots(figsize=(9.0, 6.4))
    ax.axis("off")
    ax.grid(False)

    def box(x, y, w, h, txt, fc, ec, fs_=10, style="round,pad=0.02"):
        ax.add_patch(mp.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                       boxstyle=style, facecolor=fc,
                                       edgecolor=ec, lw=1.4))
        ax.text(x, y, txt, ha="center", va="center", fontsize=fs_, color=INK)

    def arrow(x0, y0, x1, y1, lab="", dx=0.0, dy=0.0, col=AXIS_C):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.4,
                                    shrinkA=2, shrinkB=2))
        if lab:
            ax.text((x0 + x1) / 2 + dx, (y0 + y1) / 2 + dy, lab, ha="center",
                    va="center", fontsize=9, color=MUTED,
                    bbox=dict(fc="white", ec="none", pad=1.2))

    box(4.5, 9.3, 5.6, 0.9, "You have a joint PMF $p_{X,Y}(x,y)$ (a table)",
        "#eef4fc", BLUE, 10.5)
    box(4.5, 7.9, 4.6, 0.8, "What is being asked?", "#ffffff", AXIS_C, 10.5)
    arrow(4.5, 8.85, 4.5, 8.3)

    box(1.35, 6.2, 2.5, 1.15,
        "law of ONE\nvariable alone", "#fdf0e8", ORANGE, 10)
    box(4.5, 6.2, 2.6, 1.15, "law given\n$\\{Y=y\\}$", "#e8f6f0", GREEN, 10)
    box(7.75, 6.2, 2.7, 1.15, "law given a general\nevent $A$", "#fdf6e4", GOLD, 10)
    arrow(3.4, 7.55, 1.9, 6.85)
    arrow(4.5, 7.5, 4.5, 6.85)
    arrow(5.6, 7.55, 7.2, 6.85)

    box(1.35, 4.5, 3.0, 1.0,
        "MARGINALIZE\n$p_X(x)=\\sum_y p_{X,Y}(x,y)$", "#ffffff", ORANGE, 9.8)
    box(4.5, 4.5, 3.0, 1.0,
        "CONDITION\n$p_{X|Y}(x|y)=\\dfrac{p_{X,Y}(x,y)}{p_Y(y)}$", "#ffffff", GREEN, 9.8)
    box(7.75, 4.5, 3.1, 1.0,
        "RESTRICT + RENORMALIZE\n$p_{X,Y|A}=\\dfrac{p_{X,Y}}{\\mathbf{P}(A)}$ on $A$",
        "#ffffff", GOLD, 9.5)
    arrow(1.35, 5.6, 1.35, 5.05)
    arrow(4.5, 5.6, 4.5, 5.05)
    arrow(7.75, 5.6, 7.75, 5.05)

    box(4.5, 2.85, 7.4, 0.95,
        "Sum a row / column / sub-block, then divide by that sum.\n"
        "Every PMF you produce must add to exactly 1 — check it.",
        "#f4f2ea", AXIS_C, 10)
    arrow(1.35, 3.95, 2.6, 3.35)
    arrow(4.5, 3.95, 4.5, 3.35)
    arrow(7.75, 3.95, 6.4, 3.35)

    box(4.5, 1.15, 7.4, 1.05,
        "Need a number instead of a PMF?  $\\mathbb{E}[g(X,Y)]=\\sum_x\\sum_y g(x,y)\\,p_{X,Y}(x,y)$\n"
        "— never plug means into $g$; use the whole table.",
        "#eef4fc", BLUE, 9.8)
    arrow(4.5, 2.35, 4.5, 1.7)

    ax.set_xlim(-0.4, 9.6)
    ax.set_ylim(0.3, 10.0)
    save(fig, "flow")


# ============================================== Fig 4.4  indicator variables
def fig_indicator():
    fig, ax = plt.subplots(figsize=(9.0, 3.9))
    ax.axis("off")
    ax.grid(False)
    outcomes = ["S", "F", "S", "S", "F", "F", "S", "F"]
    n = len(outcomes)
    for i, o in enumerate(outcomes):
        x = i * 1.05
        succ = o == "S"
        ax.add_patch(mp.FancyBboxPatch((x, 1.55), 0.9, 0.9,
                                       boxstyle="round,pad=0.02",
                                       facecolor="#e8f6f0" if succ else "#f6f6f2",
                                       edgecolor=GREEN if succ else AXIS_C, lw=1.4))
        ax.text(x + 0.45, 2.0, "success" if succ else "fail",
                ha="center", va="center", fontsize=8.5,
                color=GREEN if succ else MUTED)
        ax.text(x + 0.45, 2.72, f"trial {i+1}", ha="center", fontsize=8.5, color=MUTED)
        ax.text(x + 0.45, 0.95, f"$X_{{{i+1}}}=" + ("1$" if succ else "0$"),
                ha="center", va="center", fontsize=10.5,
                color=GREEN if succ else MUTED, fontweight="600" if succ else "normal")
        ax.annotate("", xy=(x + 0.45, 1.2), xytext=(x + 0.45, 1.5),
                    arrowprops=dict(arrowstyle="-|>", color=AXIS_C, lw=1.1))
    tot = sum(o == "S" for o in outcomes)
    ax.text(n * 1.05 / 2 - 0.05, 0.3,
            "$X=X_1+X_2+\\cdots+X_{%d}=%d$" % (n, tot),
            ha="center", va="center", fontsize=12, color=INK)
    ax.text(n * 1.05 / 2 - 0.05, 3.3,
            "each trial has $\\mathbf{P}(\\text{success})=p$, independently",
            ha="center", fontsize=10, color=MUTED)
    ax.text(n * 1.05 / 2 - 0.05, -0.25,
            "$\\mathbb{E}[X_i]=p \\;\\Rightarrow\\; \\mathbb{E}[X]=np$   (linearity, no independence needed)\n"
            "$\\operatorname{var}(X_i)=p(1-p) \\;\\Rightarrow\\; \\operatorname{var}(X)=np(1-p)$   (independence needed)",
            ha="center", va="top", fontsize=9.5, color=INK)
    ax.set_xlim(-0.4, n * 1.05 + 0.2)
    ax.set_ylim(-1.3, 3.6)
    save(fig, "indicator")


# ============================================== Fig 4.5  rec06 P1
def fig_rec06p1():
    jNK = {}
    for n_ in range(4):
        for k in range(n_ + 1):
            jNK[(n_, k)] = F(1, 4) * F(comb(n_, k), 2 ** n_)
    pK = {k: sum(jNK.get((n_, k), F(0)) for n_ in range(4)) for k in range(4)}

    fig = plt.figure(figsize=(10.6, 3.9))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.45, 1, 1], wspace=0.36)

    ax = fig.add_subplot(gs[0, 0])
    diagram_ax(ax)
    pmax = max(jNK.values())
    for n_ in range(4):
        for k in range(4):
            p = jNK.get((n_, k), F(0))
            ax.add_patch(mp.Rectangle((k - 0.5, n_ - 0.5), 1, 1,
                                      facecolor=shade(p, pmax), edgecolor=AXIS_C, lw=1.0))
            ax.text(k, n_, fs(p), ha="center", va="center", fontsize=9.5,
                    color=INK if p > 0 else "#b8b7ae")
        ax.text(-0.95, n_, str(n_), ha="center", va="center", fontsize=9, color=MUTED)
    for k in range(4):
        ax.text(k, -1.0, str(k), ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(-1.5, 1.5, "$n$", ha="center", va="center", fontsize=11, color=INK)
    ax.text(1.5, -1.55, "$k$", ha="center", va="center", fontsize=11, color=INK)
    ax.set_title("$p_{N,K}(n,k)$", color=INK)
    ax.set_xlim(-1.9, 3.7)
    ax.set_ylim(-1.9, 3.8)

    ax = fig.add_subplot(gs[0, 1])
    ks = [0, 1, 2]
    vs = [0.25, 0.5, 0.25]
    ax.stem(ks, vs, basefmt=" ", linefmt=BLUE, markerfmt="o")
    for a, b in zip(ks, vs):
        ax.text(a, b + 0.035, ["1/4", "1/2", "1/4"][a], ha="center", fontsize=9, color=INK)
    ax.set_xticks([0, 1, 2])
    ax.set_ylim(0, 0.62)
    ax.set_xlim(-0.6, 2.6)
    ax.set_xlabel("$k$")
    ax.set_title("$p_{K|N}(k\\mid 2)$", color=INK)

    ax = fig.add_subplot(gs[0, 2])
    ns = [2, 3]
    vs = [0.4, 0.6]
    ax.stem(ns, vs, basefmt=" ", linefmt=ORANGE, markerfmt="o")
    for a, b, lab in zip(ns, vs, ["2/5", "3/5"]):
        ax.text(a, b + 0.035, lab, ha="center", fontsize=9, color=INK)
    ax.set_xticks([2, 3])
    ax.set_ylim(0, 0.75)
    ax.set_xlim(1.5, 3.5)
    ax.set_xlabel("$n$")
    ax.set_title("$p_{N|K}(n\\mid 2)$", color=INK)
    for a in fig.axes[1:]:
        for c in a.get_children():
            pass
    fig.tight_layout()
    save(fig, "rec06p1")


# ============================================== Fig 4.6  rec06 P2
def fig_rec06p2():
    pts = [(0, 3), (4, 3), (2, 2), (4, 2), (0, 1), (2, 1), (4, 1), (4, 0)]
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.2))

    ax = axes[0]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=70, color=BLUE, zorder=3)
    for (x, y) in pts:
        ax.annotate("1/8", (x, y), textcoords="offset points", xytext=(0, 9),
                    ha="center", fontsize=8.5, color=MUTED)
    condmeans = {0: 2.0, 2: 1.5, 4: 1.5}
    for i, (x, m) in enumerate(condmeans.items()):
        ax.plot([x - 0.42, x + 0.42], [m, m], color=ORANGE, lw=2.6, zorder=4,
                label="conditional mean $\\mathbb{E}[Y\\mid X=x]$" if i == 0 else None)
    ax.text(-0.75, -0.95,
            "$\\mathbb{E}[Y\\mid X=0]=2$,   $\\mathbb{E}[Y\\mid X=2]="
            "\\mathbb{E}[Y\\mid X=4]=3/2$",
            fontsize=9, color=ORANGE, ha="left", va="center")
    ax.legend(loc="upper left", fontsize=8.5)
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_yticks([0, 1, 2, 3])
    ax.set_xlim(-0.9, 4.9)
    ax.set_ylim(-1.4, 4.3)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("eight equally likely points, with $\\mathbb{E}[Y\\mid X=x]$", color=INK)

    ax = axes[1]
    rs = [0, 1, 2, 3]
    vs = [3 / 8, 1 / 4, 1 / 4, 1 / 8]
    labs = ["3/8", "1/4", "1/4", "1/8"]
    ax.stem(rs, vs, basefmt=" ", linefmt=GREEN, markerfmt="o")
    for a, b, l in zip(rs, vs, labs):
        ax.text(a, b + 0.02, l, ha="center", fontsize=9, color=INK)
    ax.set_xticks(rs)
    ax.set_xlim(-0.6, 3.6)
    ax.set_ylim(0, 0.48)
    ax.set_xlabel("$r$")
    ax.set_title("$p_R(r)$ for $R=\\min(X,Y)$", color=INK)
    fig.tight_layout()
    save(fig, "rec06p2")


# ============================================== Fig 4.7  rec07 P2 dot diagram
def fig_rec07p2():
    labs = {(1, 3): "1/12", (2, 3): "1/12", (3, 3): "*",
            (1, 2): "2/12", (2, 2): "*", (3, 2): "*",
            (1, 1): "1/12", (2, 1): "2/12", (3, 1): "0"}
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.3))

    ax = axes[0]
    for (x, y), l in labs.items():
        star = l == "*"
        ax.scatter([x], [y], s=80, color=GOLD if star else BLUE, zorder=3)
        ax.annotate("*" if star else l, (x, y), textcoords="offset points",
                    xytext=(0, 14 if star else 11),
                    ha="center", va="center" if star else "baseline",
                    fontsize=15 if star else 10,
                    color=GOLD if star else INK,
                    fontweight="600" if star else "normal")
    ax.set_xticks([1, 2, 3])
    ax.set_yticks([1, 2, 3])
    ax.set_xlim(0.4, 3.6)
    ax.set_ylim(0.4, 3.7)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("given data ($*$ = unspecified)", color=INK)

    ax = axes[1]
    ys = [1, 2, 3]
    vs = [0.25, 0.5, 0.25]
    ax.stem(ys, vs, basefmt=" ", linefmt=BLUE, markerfmt="o")
    for a, b, l in zip(ys, vs, ["1/4", "1/2", "1/4"]):
        ax.text(a, b + 0.03, l, ha="center", fontsize=9.5, color=INK)
    ax.plot([2.0], [0.0], marker="^", ms=11, color=ORANGE, clip_on=False, zorder=5)
    ax.text(0.03, 0.93, "$\\blacktriangle$ = $\\mathbb{E}[Y\\mid X=1]=2$",
            transform=ax.transAxes, color=ORANGE, fontsize=9.5,
            ha="left", va="top")
    ax.set_xticks([1, 2, 3])
    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0, 0.66)
    ax.set_xlabel("$y$")
    ax.set_title("$p_{Y|X}(y\\mid 1)$", color=INK)
    fig.tight_layout()
    save(fig, "rec07p2")


if __name__ == "__main__":
    fig_grid()
    fig_renorm()
    fig_flow()
    fig_indicator()
    fig_rec06p1()
    fig_rec06p2()
    fig_rec07p2()
    print("done")
