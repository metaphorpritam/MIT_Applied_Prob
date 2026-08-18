# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for G5 section 4 - absorption probabilities and expected time to absorption.

Run:  uv run computes/g5_s4_figs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
from mpl_style import setup, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
import matplotlib.patches as mp  # noqa: E402
import numpy as np  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL

ABS_FC, ABS_EC = "#fdece3", ORANGE      # absorbing states
TR_FC, TR_EC = "#e9f1fb", BLUE          # transient states
NEU_FC, NEU_EC = "#f2f1ec", MUTED


def save(fig, name):
    p = IMG / f"g5_s4_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ---------------------------------------------------------------- primitives
def node(ax, c, label, r=0.62, fc=TR_FC, ec=TR_EC, fs=11.5, sub=None, subcol=MUTED,
         subdy=None, lw=1.6):
    ax.add_patch(mp.Circle(c, r, fc=fc, ec=ec, lw=lw, zorder=4))
    ax.text(c[0], c[1], label, ha="center", va="center", fontsize=fs, color=INK, zorder=6)
    if sub:
        dy = subdy if subdy is not None else -(r + 0.34)
        ax.text(c[0], c[1] + dy, sub, ha="center", va="center", fontsize=9.5,
                color=subcol, zorder=6)


def _ctrl(p1, p2, rad):
    x1, y1 = p1
    x2, y2 = p2
    xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    return np.array([xm + rad * dy, ym - rad * dx])


def edge(ax, p1, p2, label=None, rad=0.22, r1=0.62, r2=0.62, color=MUTED, lw=1.5,
         loff=0.30, fs=10.5, lcol=INK, ldx=0.0, ldy=0.0, ha="center", va="center"):
    """Curved arrow from circle at p1 to circle at p2, label on the outside of the arc."""
    p1, p2 = np.array(p1, float), np.array(p2, float)
    C = _ctrl(p1, p2, rad)
    u1 = (C - p1) / np.linalg.norm(C - p1)
    u2 = (C - p2) / np.linalg.norm(C - p2)
    a, b = p1 + r1 * u1, p2 + r2 * u2
    ax.add_patch(mp.FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}",
                                    arrowstyle="-|>,head_length=7,head_width=3.6",
                                    color=color, lw=lw, zorder=3,
                                    shrinkA=0, shrinkB=0))
    if label is not None:
        Cb = _ctrl(a, b, rad)
        M = 0.5 * ((a + b) / 2) + 0.5 * Cb          # point on the quadratic Bezier at t=1/2
        d = b - a
        n = np.array([d[1], -d[0]])
        n = n / np.linalg.norm(n) * (1 if rad >= 0 else -1)
        pos = M + loff * n + np.array([ldx, ldy])
        ax.text(pos[0], pos[1], label, ha=ha, va=va, fontsize=fs, color=lcol, zorder=7,
                bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.86))


def selfloop(ax, c, label=None, r=0.62, ang=90, color=MUTED, lw=1.5, size=0.95,
             fs=10.5, lcol=INK):
    """Loop leaving and re-entering the circle at c, bulging in direction `ang` (degrees)."""
    c = np.array(c, float)
    th = np.deg2rad(ang)
    half = np.deg2rad(26)
    a = c + r * np.array([np.cos(th + half), np.sin(th + half)])
    b = c + r * np.array([np.cos(th - half), np.sin(th - half)])
    d = np.linalg.norm(b - a)
    rad = -2.0 * size * r / d                       # sign chosen so the loop bulges outward
    ax.add_patch(mp.FancyArrowPatch(a, b, connectionstyle=f"arc3,rad={rad}",
                                    arrowstyle="-|>,head_length=7,head_width=3.6",
                                    color=color, lw=lw, zorder=3, shrinkA=0, shrinkB=0))
    if label is not None:
        pos = c + (r + size * r + 0.30) * np.array([np.cos(th), np.sin(th)])
        ax.text(pos[0], pos[1], label, ha="center", va="center", fontsize=fs, color=lcol,
                zorder=7, bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none",
                                    alpha=0.86))


def box(ax, x, y, w, h, text, fc="#eef4fc", ec=BLUE, fs=10, tc=INK, lw=1.3, ha="center"):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h,
                                   boxstyle="round,pad=0.02,rounding_size=0.10",
                                   fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(x + w / 2 if ha == "center" else x + 0.16, y + h / 2, text,
            ha=ha, va="center", fontsize=fs, color=tc, zorder=5)


def barrow(ax, p1, p2, color=MUTED, lw=1.5, label=None, ldx=0.0, ldy=0.0, fs=9.5):
    ax.add_patch(mp.FancyArrowPatch(p1, p2,
                                    arrowstyle="-|>,head_length=7,head_width=3.6",
                                    color=color, lw=lw, shrinkA=0, shrinkB=0, zorder=3))
    if label:
        ax.text((p1[0] + p2[0]) / 2 + ldx, (p1[1] + p2[1]) / 2 + ldy, label,
                ha="center", va="center", fontsize=fs, color=INK, zorder=7,
                bbox=dict(boxstyle="round,pad=0.13", fc="white", ec="none", alpha=0.9))


def canvas(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    return fig, ax


# =====================================================================
# Fig 4.1 - first-step analysis: "one step, then start over"
# =====================================================================
def fig_firststep():
    fig, ax = plt.subplots(figsize=(9.8, 5.2))
    ax.set_xlim(-0.4, 13.2)
    ax.set_ylim(-3.6, 5.9)
    ax.axis("off")
    ax.grid(False)

    # the "future" panel behind everything
    ax.add_patch(mp.FancyBboxPatch((7.5, -1.35), 5.4, 5.3,
                                   boxstyle="round,pad=0.04,rounding_size=0.25",
                                   fc="#f7f6f1", ec=GRID_C, lw=1.4, zorder=1))
    ax.text(10.2, 5.25, "the rest of the trip — by the Markov property it", ha="center",
            va="center", fontsize=9.5, color=MUTED, zorder=5)
    ax.text(10.2, 4.72, "depends on the past only through where you are now",
            ha="center", va="center", fontsize=9.5, color=MUTED, zorder=5)

    i = (0.9, 1.3)
    node(ax, i, "$i$", r=0.62, fc=TR_FC, ec=TR_EC, fs=14)
    ax.text(0.9, 2.5, "today", ha="center", va="center", fontsize=9.5, color=MUTED)

    js = [(4.9, 3.3), (4.9, 1.3), (4.9, -0.7)]
    labs = ["$j_1$", "$j_2$", "$j_3$"]
    probs = ["$p_{ij_1}$", "$p_{ij_2}$", "$p_{ij_3}$"]
    futs = ["$a_{j_1}$   or   $\\mu_{j_1}$",
            "$a_{j_2}$   or   $\\mu_{j_2}$",
            "$a_{j_3}$   or   $\\mu_{j_3}$"]
    for jp, lb, pb, ft in zip(js, labs, probs, futs):
        node(ax, jp, lb, r=0.62, fc=NEU_FC, ec=NEU_EC, fs=14)
        u = np.array(jp, float) - np.array(i, float)
        u = u / np.linalg.norm(u)
        a = np.array(i, float) + 0.62 * u
        b = np.array(jp, float) - 0.62 * u
        barrow(ax, tuple(a), tuple(b), color=BLUE, lw=1.6)
        mid = (a + b) / 2
        ax.text(mid[0], mid[1] + 0.42, pb, ha="center", va="center", fontsize=12,
                color=BLUE, zorder=7,
                bbox=dict(boxstyle="round,pad=0.13", fc="white", ec="none", alpha=0.9))
        barrow(ax, (jp[0] + 0.68, jp[1]), (8.05, jp[1]), color=AXIS_C, lw=1.3)
        ax.text(8.35, jp[1], ft, ha="left", va="center", fontsize=13, color=INK, zorder=6)
    ax.text(4.9, 4.5, "one transition later", ha="center", va="center",
            fontsize=9.5, color=MUTED)

    ax.plot([-0.2, 13.0], [-1.9, -1.9], color=GRID_C, lw=1.0)
    ax.text(0.2, -2.45, "$a_i=\\sum_j p_{ij}\\,a_j$", ha="left", va="center",
            fontsize=15, color=BLUE)
    ax.text(0.2, -3.25, "the step itself costs nothing", ha="left", va="center",
            fontsize=9.5, color=MUTED)
    ax.text(6.6, -2.45, "$\\mu_i=1+\\sum_j p_{ij}\\,\\mu_j$", ha="left", va="center",
            fontsize=15, color=ORANGE)
    ax.text(6.6, -3.25, "the step itself costs one time unit", ha="left", va="center",
            fontsize=9.5, color=MUTED)
    save(fig, "firststep")


# =====================================================================
# Fig 4.2 - L18 slide 5 chain (absorption probabilities)
# =====================================================================
def fig_chain_abs():
    fig, ax = canvas(9.4, 5.6, (-3.7, 6.2), (-3.0, 3.6))
    s4 = (-1.6, 2.6)
    s1 = (0.6, 0.8)
    s2 = (-0.2, -1.7)
    s3 = (3.0, -1.7)
    s5 = (4.9, 1.0)
    node(ax, s4, "4", fc=ABS_FC, ec=ABS_EC, sub="absorbing\n$a_4=1$", subcol=ORANGE,
         subdy=-1.05)
    node(ax, s5, "5", fc=ABS_FC, ec=ABS_EC, sub="absorbing\n$a_5=0$", subcol=ORANGE,
         subdy=-1.05)
    node(ax, s1, "1", sub="$a_1=13/28$", subcol=BLUE, subdy=0.98)
    node(ax, s2, "2", sub="$a_2=5/14$", subcol=BLUE, subdy=-1.0)
    node(ax, s3, "3", sub="$a_3=2/7$", subcol=BLUE, subdy=-1.0)
    selfloop(ax, s4, "1", ang=155, color=ORANGE)
    selfloop(ax, s5, "1", ang=25, color=ORANGE)
    edge(ax, s1, s4, "0.2", rad=0.0, loff=0.34)
    edge(ax, s1, s2, "0.5", rad=0.24, loff=0.30)
    edge(ax, s2, s1, "0.4", rad=0.24, loff=0.30)
    edge(ax, s1, s3, "0.3", rad=-0.35, loff=0.32)
    edge(ax, s2, s3, "0.6", rad=0.30, loff=0.30)
    edge(ax, s3, s2, "0.8", rad=0.18, loff=0.30, ldx=0.55)
    edge(ax, s3, s5, "0.2", rad=0.0, loff=0.34)
    save(fig, "chain_abs")


# =====================================================================
# Fig 4.3 - L18 slide 6 chain (expected time to absorption)
# =====================================================================
def fig_chain_time():
    fig, ax = canvas(9.0, 5.0, (-2.6, 6.3), (-3.0, 3.0))
    s1 = (0.4, 1.4)
    s2 = (-0.4, -1.4)
    s3 = (2.9, -1.4)
    s5 = (4.9, 1.4)
    node(ax, s5, "5", fc=ABS_FC, ec=ABS_EC, sub="absorbing\n$\\mu_5=0$", subcol=ORANGE,
         subdy=-1.05)
    node(ax, s1, "1", sub="$\\mu_1=111/8=13.875$", subcol=BLUE, subdy=1.02)
    node(ax, s2, "2", sub="$\\mu_2=55/4=13.75$", subcol=BLUE, subdy=-1.0)
    node(ax, s3, "3", sub="$\\mu_3=12$", subcol=BLUE, subdy=-1.0)
    selfloop(ax, s5, "1", ang=40, color=ORANGE)
    edge(ax, s1, s2, "0.5", rad=0.24, loff=0.30)
    edge(ax, s2, s1, "0.4", rad=0.24, loff=0.30)
    edge(ax, s1, s3, "0.5", rad=-0.34, loff=0.32)
    edge(ax, s2, s3, "0.6", rad=0.30, loff=0.30)
    edge(ax, s3, s2, "0.8", rad=0.18, loff=0.30, ldx=0.55)
    edge(ax, s3, s5, "0.2", rad=0.0, loff=0.34)
    save(fig, "chain_time")


# =====================================================================
# Fig 4.4 - decision flowchart: which linear system?
# =====================================================================
def fig_recipe():
    fig, ax = plt.subplots(figsize=(9.6, 6.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.6)
    ax.axis("off")
    ax.grid(False)

    box(ax, 3.4, 7.5, 5.2, 0.85,
        "What are you asked for?", fc="#f2f1ec", ec=MUTED, fs=11.5)

    box(ax, 0.15, 5.5, 3.5, 1.15,
        "WHERE it ends up\n(which absorbing state / class)", fc="#e9f1fb", ec=BLUE, fs=10)
    box(ax, 4.2, 5.5, 3.5, 1.15,
        "HOW LONG until it gets\nanywhere absorbing", fc="#fdece3", ec=ORANGE, fs=10)
    box(ax, 8.3, 5.5, 3.5, 1.15,
        "HOW LONG until it hits\none particular state $s$", fc="#e6f6ef", ec=DGREEN, fs=10)
    barrow(ax, (5.0, 7.45), (1.9, 6.7), color=MUTED, lw=1.3)
    barrow(ax, (6.0, 7.45), (5.95, 6.7), color=MUTED, lw=1.3)
    barrow(ax, (7.0, 7.45), (10.05, 6.7), color=MUTED, lw=1.3)

    box(ax, 0.15, 3.3, 3.5, 1.55,
        "Fix the target $s$.  Solve\n$a_s=1$,  $a_i=0$ (other absorbing),\n"
        "$a_i=\\sum_j p_{ij}a_j$ (transient)",
        fc="white", ec=BLUE, fs=10)
    box(ax, 4.2, 3.3, 3.5, 1.55,
        "Solve\n$\\mu_i=0$ (absorbing),\n$\\mu_i=1+\\sum_j p_{ij}\\mu_j$",
        fc="white", ec=ORANGE, fs=10)
    box(ax, 8.3, 3.3, 3.5, 1.55,
        "Make $s$ absorbing, then solve\n$t_s=0$,\n$t_i=1+\\sum_j p_{ij}t_j$",
        fc="white", ec=DGREEN, fs=10)
    for x in (1.9, 5.95, 10.05):
        barrow(ax, (x, 5.45), (x, 4.9), color=MUTED, lw=1.3)

    box(ax, 0.15, 1.35, 3.5, 1.3,
        "Conditioned on absorption\nat $s$?  Re-weight:\n$\\tilde p_{ij}=a_jp_{ij}/a_i$,"
        " then re-solve",
        fc="#f7f6f1", ec=GRID_C, fs=9.5, tc=INK)
    box(ax, 8.3, 1.35, 3.5, 1.3,
        "Return time to $s$?\n$t_s^{*}=1+\\sum_j p_{sj}t_j$\nand $\\pi_s=1/t_s^{*}$",
        fc="#f7f6f1", ec=GRID_C, fs=9.5, tc=INK)
    barrow(ax, (1.9, 3.25), (1.9, 2.65), color=MUTED, lw=1.3)
    barrow(ax, (10.05, 3.25), (10.05, 2.65), color=MUTED, lw=1.3)

    box(ax, 2.55, 0.15, 6.8, 0.85,
        "In every case: one unknown per state, one equation per state.",
        fc="#f2f1ec", ec=MUTED, fs=9.5)
    save(fig, "recipe")


# =====================================================================
# Fig 4.5 - spider and fly, m = 4  (B&T Example 7.2 / 7.12)
# =====================================================================
def fig_spiderfly():
    fig, ax = canvas(9.4, 3.9, (-1.3, 12.1), (-2.0, 2.6))
    xs = [0.6, 4.0, 7.4, 10.8]
    pts = [(x, 0.0) for x in xs]
    node(ax, pts[0], "1", fc=ABS_FC, ec=ABS_EC, sub="spider\n(absorbing)", subcol=ORANGE,
         subdy=-1.15)
    node(ax, pts[3], "4", fc=ABS_FC, ec=ABS_EC, sub="spider\n(absorbing)", subcol=ORANGE,
         subdy=-1.15)
    node(ax, pts[1], "2", sub="$\\mu_2=10/3$", subcol=BLUE, subdy=-1.05)
    node(ax, pts[2], "3", sub="$\\mu_3=10/3$", subcol=BLUE, subdy=-1.05)
    selfloop(ax, pts[1], "0.4", ang=90)
    selfloop(ax, pts[2], "0.4", ang=90)
    selfloop(ax, pts[0], "1", ang=90, color=ORANGE)
    selfloop(ax, pts[3], "1", ang=90, color=ORANGE)
    edge(ax, pts[1], pts[0], "0.3", rad=0.26, loff=0.28)
    edge(ax, pts[1], pts[2], "0.3", rad=-0.26, loff=0.28)
    edge(ax, pts[2], pts[1], "0.3", rad=-0.26, loff=0.28)
    edge(ax, pts[2], pts[3], "0.3", rad=0.26, loff=0.28)
    ax.text(5.7, 2.25, "fly's position; spiders sit at 1 and 4",
            ha="center", va="center", fontsize=9.5, color=MUTED)
    save(fig, "spiderfly")


# =====================================================================
# Fig 4.6 - gambler's ruin chain
# =====================================================================
def fig_gambler_chain():
    fig, ax = canvas(9.6, 3.6, (-1.2, 13.2), (-2.0, 2.3))
    xs = [0.6, 3.0, 5.4, 7.8, 10.2, 12.6]
    pts = [(x, 0.0) for x in xs]
    labs = ["0", "1", "2", "$\\cdots$", "$m\\!-\\!1$", "$m$"]
    for k, (p, lb) in enumerate(zip(pts, labs)):
        if k in (0, 5):
            node(ax, p, lb, fc=ABS_FC, ec=ABS_EC)
        elif k == 3:
            node(ax, p, lb, fc="white", ec=GRID_C, fs=12)
        else:
            node(ax, p, lb)
    selfloop(ax, pts[0], "1", ang=90, color=ORANGE)
    selfloop(ax, pts[5], "1", ang=90, color=ORANGE)
    for k in range(1, 5):
        edge(ax, pts[k], pts[k + 1], "$p$", rad=-0.28, loff=0.26)
    for k in range(0, 4):
        edge(ax, pts[k + 1], pts[k], "$1-p$", rad=-0.28, loff=0.26)
    ax.text(0.6, -1.35, "ruin", ha="center", va="center", fontsize=10, color=ORANGE)
    ax.text(12.6, -1.35, "target", ha="center", va="center", fontsize=10, color=ORANGE)
    ax.text(6.6, 2.0, "fortune after each \\$1 bet; $p$ = probability of winning a round",
            ha="center", va="center", fontsize=9.5, color=MUTED)
    save(fig, "gambler_chain")


# =====================================================================
# Fig 4.7 - gambler's ruin: ruin curves and expected duration
# =====================================================================
def ruin_a(p, m):
    i = np.arange(m + 1, dtype=float)
    if abs(p - 0.5) < 1e-12:
        return i / m
    rho = (1 - p) / p
    return (1 - rho ** i) / (1 - rho ** m)


def ruin_D(p, m):
    i = np.arange(m + 1, dtype=float)
    if abs(p - 0.5) < 1e-12:
        return i * (m - i)
    return (i - m * ruin_a(p, m)) / (1 - 2 * p)


def fig_gambler_curves():
    m = 20
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.0))
    i = np.arange(m + 1)
    for k, p in enumerate([0.40, 0.45, 0.50, 0.55, 0.60]):
        axes[0].plot(i, ruin_a(p, m), color=PAL[k], marker="o", ms=3.2,
                     label=f"$p={p:.2f}$")
        axes[1].plot(i, ruin_D(p, m), color=PAL[k], marker="o", ms=3.2,
                     label=f"$p={p:.2f}$")
    axes[0].set_xlabel("starting fortune $i$")
    axes[0].set_ylabel("$a_i=\\mathbf{P}(\\mathrm{reach}\\ m\\ \\mathrm{first})$")
    axes[0].set_title(f"Probability of hitting the target $m={m}$")
    axes[0].legend(loc="upper left")
    axes[0].set_ylim(-0.03, 1.03)
    axes[1].set_xlabel("starting fortune $i$")
    axes[1].set_ylabel("$D_i$ = expected number of rounds")
    axes[1].set_title("Expected duration of the game")
    axes[1].legend(loc="upper left")
    fig.tight_layout()
    save(fig, "gambler_curves")


# =====================================================================
# Fig 4.8 - rec19 P1(a) chain
# =====================================================================
def rec19_layout(ax, p9lab="1", p15lab="1", c9=ABS_FC, e9=ABS_EC,
                 c15=ABS_FC, e15=ABS_EC, extra=None):
    n9 = (-3.6, 3.3)
    n15 = (3.6, 3.3)
    n1 = (0.0, 0.9)
    n3 = (-3.0, -1.9)
    n2 = (3.0, -1.9)
    node(ax, n9, "9", fc=c9, ec=e9)
    node(ax, n15, "15", fc=c15, ec=e15, fs=10.5)
    node(ax, n1, "6-1", fs=10.5)
    node(ax, n3, "6-3", fs=10.5)
    node(ax, n2, "6-2", fs=10.5)
    selfloop(ax, n1, "1/2", ang=90)
    if p9lab:
        selfloop(ax, n9, p9lab, ang=145, color=e9)
    if p15lab:
        selfloop(ax, n15, p15lab, ang=35, color=e15)
    edge(ax, n1, n9, "1/8", rad=0.0, loff=0.34)
    edge(ax, n1, n15, "1/8", rad=0.0, loff=0.34)
    edge(ax, n1, n3, "1/8", rad=0.20, loff=0.30)
    edge(ax, n3, n1, "3/8", rad=0.20, loff=0.30)
    edge(ax, n1, n2, "1/8", rad=-0.20, loff=0.30)
    edge(ax, n2, n1, "3/8", rad=-0.20, loff=0.30)
    edge(ax, n3, n9, "1/4", rad=-0.30, loff=0.32)
    edge(ax, n2, n15, "1/2", rad=0.30, loff=0.32)
    edge(ax, n3, n2, "3/8", rad=-0.09, loff=0.28, ldy=-0.62)
    edge(ax, n2, n3, "1/8", rad=-0.34, loff=0.28)
    return n9, n15, n1, n3, n2


def fig_rec19_chain():
    fig, ax = canvas(9.6, 6.6, (-6.0, 6.0), (-5.4, 5.2))
    n9, n15, n1, n3, n2 = rec19_layout(ax)
    ax.text(n9[0], n9[1] - 1.05, "absorbing", ha="center", va="center", fontsize=9.5,
            color=ORANGE)
    ax.text(n15[0], n15[1] - 1.05, "absorbing", ha="center", va="center", fontsize=9.5,
            color=ORANGE)
    ax.text(0.0, -4.3, "$a_{6\\text{-}1}=105/184=0.5707$   ·   "
                       "$a_{6\\text{-}2}=143/184=0.7772$   ·   "
                       "$a_{6\\text{-}3}=93/184=0.5054$",
            ha="center", va="center", fontsize=10.5, color=BLUE)
    ax.text(0.0, -4.9, "$\\mu_{6\\text{-}1}=81/23=3.5217$   ·   "
                       "$\\mu_{6\\text{-}2}=63/23=2.7391$   ·   "
                       "$\\mu_{6\\text{-}3}=77/23=3.3478$",
            ha="center", va="center", fontsize=10.5, color=ORANGE)
    save(fig, "rec19_chain")


# =====================================================================
# Fig 4.9 - rec19 P1(e): the chain conditioned on absorption at 15
# =====================================================================
def fig_rec19_cond():
    fig, ax = canvas(9.2, 6.4, (-5.0, 5.6), (-5.4, 4.6))
    n15 = (3.6, 3.1)
    n1 = (0.0, 0.9)
    n3 = (-3.0, -1.9)
    n2 = (3.0, -1.9)
    node(ax, n15, "15", fc=ABS_FC, ec=ABS_EC, fs=10.5)
    node(ax, n1, "6-1", fs=10.5)
    node(ax, n3, "6-3", fs=10.5)
    node(ax, n2, "6-2", fs=10.5)
    selfloop(ax, n1, "1/2", ang=125)
    selfloop(ax, n15, "1", ang=40, color=ORANGE)
    edge(ax, n1, n15, "23/105", rad=0.0, loff=0.38)
    edge(ax, n1, n3, "31/280", rad=0.20, loff=0.34)
    edge(ax, n3, n1, "105/248", rad=0.20, loff=0.36)
    edge(ax, n1, n2, "143/840", rad=-0.20, loff=0.36)
    edge(ax, n2, n1, "315/1144", rad=-0.20, loff=0.40)
    edge(ax, n2, n15, "92/143", rad=0.30, loff=0.34)
    edge(ax, n3, n2, "143/248", rad=-0.09, loff=0.30, ldy=-0.62)
    edge(ax, n2, n3, "93/1144", rad=-0.34, loff=0.32)
    ax.text(-4.9, 4.2, "conditioned on eventual absorption at course 15:"
                       "  $\\tilde p_{ij}=a_j\\,p_{ij}/a_i$",
            ha="left", va="center", fontsize=10, color=MUTED)
    ax.text(-4.9, 3.6, "course 9 has $a_9=0$, so it drops out of the chain entirely",
            ha="left", va="center", fontsize=10, color=MUTED)
    ax.text(0.0, -4.6, "$\\tilde\\mu_{6\\text{-}1}=1763/483=3.6501$   ·   "
                       "$\\tilde\\mu_{6\\text{-}2}=2.3208$   ·   "
                       "$\\tilde\\mu_{6\\text{-}3}=3.8836$",
            ha="center", va="center", fontsize=10.5, color=BLUE)
    save(fig, "rec19_cond")


# =====================================================================
# Fig 4.10 - rec19 P1(f) chain (course 15 removed)
# =====================================================================
def fig_rec19_f():
    fig, ax = canvas(9.0, 6.2, (-5.0, 5.0), (-5.2, 4.6))
    n9 = (-3.4, 3.1)
    n1 = (0.0, 0.9)
    n3 = (-3.0, -1.9)
    n2 = (3.0, -1.9)
    node(ax, n9, "9", fc=ABS_FC, ec=ABS_EC)
    node(ax, n1, "6-1", fs=10.5)
    node(ax, n3, "6-3", fs=10.5)
    node(ax, n2, "6-2", fs=10.5)
    selfloop(ax, n1, "1/2", ang=55)
    selfloop(ax, n9, "1", ang=190, color=ORANGE)
    edge(ax, n1, n9, "1/6", rad=0.0, loff=0.34)
    edge(ax, n1, n3, "1/6", rad=0.20, loff=0.32)
    edge(ax, n3, n1, "3/8", rad=0.20, loff=0.32)
    edge(ax, n1, n2, "1/6", rad=-0.20, loff=0.32)
    edge(ax, n2, n1, "3/4", rad=-0.20, loff=0.32)
    edge(ax, n3, n9, "1/4", rad=-0.30, loff=0.32)
    edge(ax, n3, n2, "3/8", rad=-0.09, loff=0.28, ldy=-0.62)
    edge(ax, n2, n3, "1/4", rad=-0.34, loff=0.28)
    ax.text(-4.9, 4.3, "part (f): course 15 deleted, rows renormalized;"
                       " 9 is the only absorbing state",
            ha="left", va="center", fontsize=10, color=MUTED)
    ax.text(0.0, -4.5, "$\\mu_{6\\text{-}1}=86/13=6.6154$   ·   "
                       "$\\mu_{6\\text{-}2}=98/13=7.5385$   ·   "
                       "$\\mu_{6\\text{-}3}=82/13=6.3077$",
            ha="center", va="center", fontsize=10.5, color=BLUE)
    save(fig, "rec19_f")


# =====================================================================
# Fig 4.11 - random-walk sample paths: symmetric vs drifting
# =====================================================================
def fig_randomwalk():
    n = 200
    rng = np.random.default_rng(4711)
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.0), sharey=True)
    steps = np.arange(n + 1)
    for ax, p, title in ((axes[0], 0.50, "symmetric  $p=1/2$:  no drift"),
                         (axes[1], 0.60, "drifting  $p=0.6$:  $\mathbb{E}[\mathrm{step}]=p-q=0.2$")):
        for k in range(7):
            inc = np.where(rng.random(n) < p, 1, -1)
            path = np.concatenate([[0], np.cumsum(inc)])
            ax.plot(steps, path, color=PAL[k % 8], lw=1.1, alpha=0.85)
        ax.axhline(0, color=AXIS_C, lw=1.0)
        ax.plot(steps, (2 * p - 1) * steps, color=INK, lw=1.8, ls="--",
                label="mean $(p-q)\,n$")
        sd = np.sqrt(4 * p * (1 - p) * steps)
        ax.plot(steps, (2 * p - 1) * steps + sd, color=MUTED, lw=1.2, ls=":",
                label="mean $\pm\,\sqrt{4pq\,n}$")
        ax.plot(steps, (2 * p - 1) * steps - sd, color=MUTED, lw=1.2, ls=":")
        ax.set_title(title)
        ax.set_xlabel("number of steps $n$")
        ax.legend(loc="upper left")
    axes[0].set_ylabel("position $X_n$")
    axes[0].set_ylim(-38, 62)
    fig.tight_layout()
    save(fig, "randomwalk")


for f in (fig_firststep, fig_chain_abs, fig_chain_time, fig_recipe, fig_spiderfly,
          fig_gambler_chain, fig_gambler_curves, fig_rec19_chain, fig_rec19_cond,
          fig_rec19_f, fig_randomwalk):
    f()
print("done")
