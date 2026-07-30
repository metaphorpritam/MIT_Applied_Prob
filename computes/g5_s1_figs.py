# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for G5 section 1 — Markov model, transition diagrams, n-step
transition probabilities.

Run:  uv run computes/g5_s1_figs.py
"""
from __future__ import annotations

import sys
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

BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL
NODE_FC = "#eaf2fd"


def save(fig, name):
    p = IMG / f"g5_s1_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ---------------------------------------------------------------------------
# state-diagram primitives
# ---------------------------------------------------------------------------
def node(ax, x, y, label, r=0.42, fc=NODE_FC, ec=BLUE, fs=12, lw=1.6, tc=INK):
    ax.add_patch(plt.Circle((x, y), r, fc=fc, ec=ec, lw=lw, zorder=4))
    ax.text(x, y, label, ha="center", va="center", fontsize=fs, color=tc, zorder=6)


def _apex(p1, p2, rad):
    """Apex (t = 0.5 point) of matplotlib's arc3 quadratic Bezier."""
    p1 = np.asarray(p1, float)
    p2 = np.asarray(p2, float)
    d = p2 - p1
    mid = (p1 + p2) / 2
    return mid + 0.5 * rad * np.array([d[1], -d[0]])


def arc(ax, x1, y1, x2, y2, rad=-0.34, r=0.42, label=None, c=MUTED, lw=1.5,
        lab_off=0.26, fs=10.5, lab_c=INK, shrink=None):
    """Curved directed arc between two node centers, trimmed to the circles.

    rad < 0 bows the arc to the LEFT of the travel direction (upward for a
    left-to-right arc); rad > 0 bows it to the right.
    """
    sh = r * 72 if shrink is None else shrink
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>,head_width=0.26,head_length=0.55",
                                color=c, lw=lw,
                                connectionstyle=f"arc3,rad={rad}",
                                shrinkA=sh, shrinkB=sh),
                zorder=2)
    if label is not None:
        mid = np.array([(x1 + x2) / 2, (y1 + y2) / 2])
        a = _apex((x1, y1), (x2, y2), rad)
        u = a - mid
        u = u / (np.linalg.norm(u) + 1e-12)
        pos = a + lab_off * u
        ax.text(pos[0], pos[1], label, ha="center", va="center", fontsize=fs,
                color=lab_c, zorder=7,
                bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.92))


def selfloop(ax, x, y, r=0.42, label=None, where="top", size=0.62, c=MUTED,
             lw=1.5, fs=10.5, lab_c=INK):
    """Self-transition loop bulging `size` units beyond the node rim."""
    ang = {"top": 90, "bottom": 270, "left": 180, "right": 0}[where]
    th = np.deg2rad(ang)
    ux, uy = np.cos(th), np.sin(th)          # outward direction
    px, py = -uy, ux                         # tangential direction
    half = 0.45
    p1 = np.array([x + r * (ux * 0.90 + px * half), y + r * (uy * 0.90 + py * half)])
    p2 = np.array([x + r * (ux * 0.90 - px * half), y + r * (uy * 0.90 - py * half)])
    chord = np.linalg.norm(p2 - p1)
    rad = -2.0 * size / chord                # apex sits `size` beyond the chord
    # p1 -> p2 travels in the -p direction; rad<0 bows away from the node
    ax.annotate("", xy=tuple(p2), xytext=tuple(p1),
                arrowprops=dict(arrowstyle="-|>,head_width=0.26,head_length=0.55",
                                color=c, lw=lw,
                                connectionstyle=f"arc3,rad={rad}",
                                shrinkA=0, shrinkB=0), zorder=2)
    if label is not None:
        d = r * 0.90 + size + 0.30
        ax.text(x + ux * d, y + uy * d, label,
                ha="center", va="center", fontsize=fs, color=lab_c, zorder=7,
                bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.92))


def straight(ax, x1, y1, x2, y2, r=0.42, label=None, c=MUTED, lw=1.5, fs=10.5,
             lab_dy=0.0, lab_dx=0.0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>,head_width=0.26,head_length=0.55",
                                color=c, lw=lw, shrinkA=r * 72, shrinkB=r * 72),
                zorder=2)
    if label is not None:
        ax.text((x1 + x2) / 2 + lab_dx, (y1 + y2) / 2 + lab_dy, label,
                ha="center", va="center", fontsize=fs, color=INK, zorder=7,
                bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.92))


# ===========================================================================
# Fig 1.1 — the two-state chain of L16 slide 5 + diagram conventions
# ===========================================================================
def fig_twostate():
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.2),
                             gridspec_kw={"width_ratios": [1.15, 1.0]})

    ax = diagram_ax(axes[0])
    ax.set_xlim(-1.5, 5.0)
    ax.set_ylim(-2.0, 2.3)
    node(ax, 0, 0, "1")
    node(ax, 3.5, 0, "2")
    selfloop(ax, 0, 0, label="0.5", where="left", size=0.55, c=BLUE, lab_c=BLUE)
    selfloop(ax, 3.5, 0, label="0.8", where="right", size=0.55, c=BLUE, lab_c=BLUE)
    arc(ax, 0, 0, 3.5, 0, rad=-0.34, label="0.5", c=ORANGE, lab_c=ORANGE, lab_off=0.22)
    arc(ax, 3.5, 0, 0, 0, rad=-0.34, label="0.2", c=GREEN, lab_c=DGREEN, lab_off=0.22)
    ax.text(1.75, -1.85, "$p_{11}=0.5,\\;p_{12}=0.5,\\;p_{21}=0.2,\\;p_{22}=0.8$",
            ha="center", va="center", fontsize=11, color=INK)
    ax.set_title("(a)  the two-state chain (L16 slide 5)", fontsize=11, color=INK)

    # ---- (b) the transition matrix, rows highlighted ----------------------
    ax = axes[1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.grid(False)
    P = [[0.5, 0.5], [0.2, 0.8]]
    x0, y0, cw, ch = 0.28, 0.66, 0.24, 0.19
    ax.text(0.5, 0.94, "transition probability matrix", ha="center", fontsize=11,
            color=INK, weight="600")
    for j in range(2):
        ax.text(x0 + cw * (j + 0.5), y0 + ch + 0.03, f"to {j+1}", ha="center",
                fontsize=10, color=MUTED)
    for i in range(2):
        ax.text(x0 - 0.04, y0 - ch * i + ch / 2, f"from {i+1}", ha="right",
                va="center", fontsize=10, color=MUTED)
        for j in range(2):
            xx = x0 + cw * j
            yy = y0 - ch * i
            ax.add_patch(mp.Rectangle((xx, yy), cw, ch, fc="#f4f8fe" if i == 0 else "#fdf3ec",
                                      ec=GRID_C, lw=1.0))
            ax.text(xx + cw / 2, yy + ch / 2, f"{P[i][j]}", ha="center", va="center",
                    fontsize=13, color=INK)
        ax.annotate("", xy=(x0 + 2 * cw + 0.12, y0 - ch * i + ch / 2),
                    xytext=(x0 + 2 * cw + 0.015, y0 - ch * i + ch / 2),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
        ax.text(x0 + 2 * cw + 0.15, y0 - ch * i + ch / 2, "sum $=1$", ha="left",
                va="center", fontsize=10, color=MUTED)
    ax.text(0.5, 0.30,
            "row $i$  =  the whole probability law of the next state,\n"
            "given that the chain is at state $i$ now",
            ha="center", va="center", fontsize=10.5, color=INK, linespacing=1.5)
    ax.text(0.5, 0.10,
            "columns need NOT sum to 1  ($0.5+0.2=0.7$)",
            ha="center", va="center", fontsize=10.5, color=RED)
    ax.set_title("(b)  reading the matrix", fontsize=11, color=INK)

    fig.tight_layout()
    save(fig, "twostate")


# ===========================================================================
# Fig 1.2 — checkout counter chain
# ===========================================================================
def fig_checkout():
    fig, ax = plt.subplots(figsize=(12.0, 3.9))
    diagram_ax(ax)
    ax.set_xlim(-1.3, 15.6)
    ax.set_ylim(-2.0, 2.5)
    xs = [0.0, 2.4, 4.8, 7.2, 10.6, 13.0]
    labs = ["0", "1", "2", "3", "$m\\!-\\!1$", "$m$"]
    for x, lb in zip(xs, labs):
        node(ax, x, 0, lb, r=0.46, fs=11.5)
    ax.text(8.9, 0, "$\\cdots$", ha="center", va="center", fontsize=17, color=MUTED)

    up = "$p(1\\!-\\!q)$"
    dn = "$q(1\\!-\\!p)$"
    # 0 -> 1 is special: p, not p(1-q)
    arc(ax, xs[0], 0, xs[1], 0, rad=-0.40, r=0.46, label="$p$", c=ORANGE, lab_c=ORANGE, lab_off=0.26)
    arc(ax, xs[1], 0, xs[0], 0, rad=-0.40, r=0.46, label=dn, c=GREEN, lab_c=DGREEN, lab_off=0.30)
    for a, b in [(1, 2), (2, 3)]:
        arc(ax, xs[a], 0, xs[b], 0, rad=-0.40, r=0.46, label=up, c=ORANGE, lab_c=ORANGE, lab_off=0.30)
        arc(ax, xs[b], 0, xs[a], 0, rad=-0.40, r=0.46, label=dn, c=GREEN, lab_c=DGREEN, lab_off=0.30)
    arc(ax, xs[4], 0, xs[5], 0, rad=-0.40, r=0.46, label=up, c=ORANGE, lab_c=ORANGE, lab_off=0.30)
    arc(ax, xs[5], 0, xs[4], 0, rad=-0.40, r=0.46, label=dn, c=GREEN, lab_c=DGREEN, lab_off=0.30)
    # dashed stubs into and out of the ellipsis
    for (xa, xb, col) in [(xs[3] + 0.55, 8.25, ORANGE), (9.55, xs[4] - 0.55, ORANGE)]:
        ax.plot([xa, xb], [0.55, 0.55], ls=":", lw=1.4, color=col, zorder=1)
    for (xa, xb, col) in [(8.25, xs[3] + 0.55, GREEN), (xs[4] - 0.55, 9.55, GREEN)]:
        ax.plot([xa, xb], [-0.55, -0.55], ls=":", lw=1.4, color=col, zorder=1)

    selfloop(ax, xs[0], 0, r=0.46, label="$1-p$", where="top", size=0.55, c=BLUE, lab_c=BLUE)
    for k in (1, 2, 3, 4):
        selfloop(ax, xs[k], 0, r=0.46, label="$\\ast$",
                 where="top", size=0.55, c=BLUE, lab_c=BLUE)
    selfloop(ax, xs[5], 0, r=0.46, label="$1-q(1\\!-\\!p)$", where="top", size=0.55,
             c=BLUE, lab_c=BLUE)
    ax.text(4.5, 2.72, "$\\ast\\;=\\;pq+(1-p)(1-q)$", ha="center", fontsize=11, color=BLUE)
    ax.text(7.2, -1.75,
            "arrivals Bernoulli($p$)   ·   service completions geometric($q$)   ·   "
            "state $X_n$ = number of customers at time $n$",
            ha="center", va="center", fontsize=10.5, color=MUTED)
    fig.tight_layout()
    save(fig, "checkout")


# ===========================================================================
# Fig 1.3 — Chapman-Kolmogorov trellis (L16 slide 4)
# ===========================================================================
def fig_trellis():
    fig, ax = plt.subplots(figsize=(10.4, 5.2))
    diagram_ax(ax)
    ax.set_xlim(-1.6, 10.4)
    ax.set_ylim(-4.1, 3.5)
    xL, xM, xR = 0.0, 4.6, 9.2
    ys = [2.2, 0.0, -2.2]
    node(ax, xL, 0, "$i$", r=0.42)
    node(ax, xR, 0, "$j$", r=0.42)
    mid_labs = ["$1$", "$k$", "$m$"]
    for y, lb in zip(ys, mid_labs):
        node(ax, xM, y, lb, r=0.42, fc="#fdf0e8", ec=ORANGE)
    ax.text(xM, 1.15, "$\\vdots$", ha="center", va="center", fontsize=15, color=MUTED)
    ax.text(xM, -1.35, "$\\vdots$", ha="center", va="center", fontsize=15, color=MUTED)

    r_labs = ["$r_{i1}(n-1)$", "$r_{ik}(n-1)$", "$r_{im}(n-1)$"]
    p_labs = ["$p_{1j}$", "$p_{kj}$", "$p_{mj}$"]
    for y, rl, pl in zip(ys, r_labs, p_labs):
        straight(ax, xL, 0, xM, y, r=0.42, c=BLUE)
        t = 0.52
        ax.text(xL + t * (xM - xL), t * y + (0.30 if y >= 0 else -0.30), rl,
                ha="center", va="center", fontsize=10, color=BLUE, zorder=7,
                bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.95))
        straight(ax, xM, y, xR, 0, r=0.42, c=DGREEN)
        ax.text(xM + 0.5 * (xR - xM), 0.5 * y + (0.30 if y >= 0 else -0.30), pl,
                ha="center", va="center", fontsize=10, color=DGREEN, zorder=7,
                bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.95))

    for x, t in [(xL, "Time $0$"), (xM, "Time $n-1$"), (xR, "Time $n$")]:
        ax.text(x, 3.15, t, ha="center", fontsize=11.5, color=INK, weight="600")
    ax.text(4.6, -3.65,
            "$r_{ij}(n)\\;=\\;\\sum_{k=1}^{m} r_{ik}(n-1)\\,p_{kj}$",
            ha="center", va="center", fontsize=13.5, color=INK)
    fig.tight_layout()
    save(fig, "trellis")


# ===========================================================================
# Fig 1.4 — matrix-power convergence for the two-state chain
# ===========================================================================
def fig_convergence():
    P = np.array([[0.5, 0.5], [0.2, 0.8]])
    fig = plt.figure(figsize=(12.2, 4.6))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.35, 1.0, 1.0], wspace=0.32)

    # ---- (a) the filled-in slide table -----------------------------------
    ax = fig.add_subplot(gs[0, 0])
    ax.axis("off")
    ax.grid(False)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    cols = [0, 1, 2, 100, 101]
    rows = [("$r_{11}(n)$", 0, 0), ("$r_{12}(n)$", 0, 1),
            ("$r_{21}(n)$", 1, 0), ("$r_{22}(n)$", 1, 1)]
    x0, cw = 0.19, 0.160
    y0, ch = 0.70, 0.135
    for c, n in enumerate(cols):
        ax.text(x0 + cw * (c + 0.5), y0 + ch + 0.02, f"$n={n}$", ha="center",
                fontsize=9, color=MUTED)
    for r, (lab, i, j) in enumerate(rows):
        ax.text(x0 - 0.02, y0 - ch * r + ch / 2, lab, ha="right", va="center",
                fontsize=10.5, color=INK)
        for c, n in enumerate(cols):
            v = np.linalg.matrix_power(P, n)[i, j]
            xx, yy = x0 + cw * c, y0 - ch * r
            hot = n >= 100
            ax.add_patch(mp.Rectangle((xx, yy), cw, ch, fc="#eef6f1" if hot else "#f7f7f4",
                                      ec=GRID_C, lw=0.9))
            ax.text(xx + cw / 2, yy + ch / 2, f"{v:.4f}" if 0 < n < 100 else f"{v:.4f}",
                    ha="center", va="center", fontsize=9.5,
                    color=DGREEN if hot else INK)
    ax.text(0.5, 0.10, "green: $r_{i1}\\to 2/7=0.2857$, $r_{i2}\\to 5/7=0.7143$,\n"
                       "the same limit from either starting state",
            ha="center", va="center", fontsize=9.5, color=MUTED, linespacing=1.5)
    ax.set_title("(a)  L16 slide 5, filled in", fontsize=11, color=INK)

    # ---- (b) convergence ---------------------------------------------------
    ax = fig.add_subplot(gs[0, 1])
    ns = np.arange(0, 21)
    r11 = [np.linalg.matrix_power(P, n)[0, 0] for n in ns]
    r21 = [np.linalg.matrix_power(P, n)[1, 0] for n in ns]
    ax.plot(ns, r11, "o-", color=BLUE, ms=4.5, label="$r_{11}(n)$  (start at 1)")
    ax.plot(ns, r21, "s-", color=ORANGE, ms=4.5, label="$r_{21}(n)$  (start at 2)")
    ax.axhline(2 / 7, color=DGREEN, ls="--", lw=1.6)
    ax.text(13.5, 2 / 7 + 0.035, "$2/7$", color=DGREEN, fontsize=10.5)
    ax.set_xlabel("$n$")
    ax.set_ylabel("$r_{i1}(n)$")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="upper right", fontsize=9)
    ax.set_title("(b)  both rows converge", fontsize=11, color=INK)

    # ---- (c) geometric error decay ----------------------------------------
    ax = fig.add_subplot(gs[0, 2])
    ns2 = np.arange(0, 26)
    e11 = np.abs(np.array([np.linalg.matrix_power(P, n)[0, 0] for n in ns2]) - 2 / 7)
    e21 = np.abs(np.array([np.linalg.matrix_power(P, n)[1, 0] for n in ns2]) - 2 / 7)
    ax.semilogy(ns2, np.maximum(e11, 1e-18), "o-", color=BLUE, ms=4, label="$|r_{11}(n)-2/7|$")
    ax.semilogy(ns2, np.maximum(e21, 1e-18), "s-", color=ORANGE, ms=4, label="$|r_{21}(n)-2/7|$")
    ax.semilogy(ns2, (5 / 7) * 0.3 ** ns2, "--", color=MUTED, lw=1.4, label="$(5/7)\\,0.3^{\\,n}$")
    ax.set_xlabel("$n$")
    ax.set_ylabel("distance from the limit")
    ax.set_ylim(1e-14, 3)
    ax.legend(loc="upper right", fontsize=8.5)
    ax.set_title("(c)  error $\\propto 0.3^{\\,n}$", fontsize=11, color=INK)

    fig.tight_layout()
    save(fig, "convergence")


# ===========================================================================
# Fig 1.5 — recipe flowchart: is it a Markov chain, and what is the state?
# ===========================================================================
def fig_recipe():
    fig, ax = plt.subplots(figsize=(11.6, 6.4))
    ax.axis("off")
    ax.grid(False)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)

    def box(x, y, w, h, txt, fc="#eef4fc", ec=BLUE, fs=10, tc=INK):
        ax.add_patch(mp.FancyBboxPatch((x, y), w, h,
                                       boxstyle="round,pad=0.02,rounding_size=0.12",
                                       fc=fc, ec=ec, lw=1.3))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs,
                color=tc, linespacing=1.5, zorder=5)

    def ar(x1, y1, x2, y2, lab=None, ldx=0.0, ldy=0.0):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4,
                                    shrinkA=3, shrinkB=3))
        if lab:
            ax.text((x1 + x2) / 2 + ldx, (y1 + y2) / 2 + ldy, lab, ha="center",
                    va="center", fontsize=9.5, color=MUTED,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))

    box(3.4, 6.0, 5.2, 0.8, "Verbal description of a system\nevolving in discrete time steps",
        fc="#f4f4f0", ec=AXIS_C)
    box(3.4, 4.75, 5.2, 0.85,
        "1.  Propose a state $X_n$: the smallest summary of\n"
        "the past that you need in order to predict the future")
    box(0.25, 3.15, 5.1, 1.15,
        "2.  Test the Markov property.\nIs $\\mathbf{P}(X_{n+1}=j\\mid X_n=i,\\;\\text{any past})$\n"
        "the same number for every past?", fc="#fdf0e8", ec=ORANGE)
    box(6.65, 3.15, 5.1, 1.15,
        "2$'$.  NO — enlarge the state.\nAdd whatever the answer depended on\n"
        "(age, phase, last two values, $\\ldots$)", fc="#fdecec", ec=RED)
    box(0.25, 1.45, 5.1, 1.25,
        "3.  Write the transition probabilities $p_{ij}$\nfrom the one-step mechanics.\n"
        "CHECK: $p_{i1}+\\cdots+p_{im}=1$ for every $i$", fc="#eaf6f0", ec=DGREEN)
    box(6.65, 1.45, 5.1, 1.25,
        "4.  Draw the transition diagram:\nnodes = states, arcs = $p_{ij}>0$,\n"
        "self-loops for $p_{ii}>0$", fc="#eaf6f0", ec=DGREEN)
    box(3.4, 0.25, 5.2, 0.8,
        "5.  Compute: $r_{ij}(n)$ by Chapman–Kolmogorov,\nor the matrix power $P^n$",
        fc="#f3effa", ec=PURPLE)

    ar(6.0, 6.0, 6.0, 5.60)
    ar(4.6, 4.75, 2.8, 4.30)
    ar(2.8, 3.15, 2.8, 2.60, "YES", ldx=0.55)
    ar(5.35, 3.72, 6.65, 3.72, "NO")
    ax.annotate("", xy=(8.55, 5.02), xytext=(9.2, 4.30),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5,
                                connectionstyle="arc3,rad=0.45", shrinkA=3, shrinkB=3))
    ax.text(10.25, 4.72, "redefine the state", fontsize=9.5, color=RED, ha="center",
            linespacing=1.4)
    ar(5.35, 2.08, 6.65, 2.08)
    ar(2.8, 1.45, 3.9, 1.05)
    ar(9.2, 1.45, 8.1, 1.05)
    fig.tight_layout()
    save(fig, "recipe")


# ===========================================================================
# Fig 1.6 — spider-and-fly and painting-fish chains
# ===========================================================================
def fig_models():
    fig, axes = plt.subplots(2, 1, figsize=(11.0, 6.6))

    ax = diagram_ax(axes[0])
    ax.set_xlim(-1.6, 11.2)
    ax.set_ylim(-1.5, 2.2)
    xs = [0.0, 3.0, 6.0, 9.0]
    for x, lb in zip(xs, ["1", "2", "3", "4"]):
        node(ax, x, 0, lb, r=0.44)
    selfloop(ax, xs[0], 0, r=0.44, label="1", where="left", size=0.52, c=RED, lab_c=RED)
    selfloop(ax, xs[3], 0, r=0.44, label="1", where="right", size=0.52, c=RED, lab_c=RED)
    for k in (1, 2):
        selfloop(ax, xs[k], 0, r=0.44, label="0.4", where="top", size=0.52, c=BLUE, lab_c=BLUE)
    for a, b in [(1, 0), (1, 2), (2, 1), (2, 3)]:
        col = ORANGE if b > a else GREEN
        arc(ax, xs[a], 0, xs[b], 0, rad=-0.36, r=0.44, label="0.3", c=col,
            lab_c=ORANGE if b > a else DGREEN, lab_off=0.26)
    ax.text(4.5, -1.28, "spider–fly ($m=4$): states 1 and 4 are the spiders, absorbing"
                        "   ·   B&T Example 7.2",
            ha="center", va="center", fontsize=10.5, color=MUTED)
    ax.set_title("(a)  the spider-and-fly chain", fontsize=11, color=INK)

    ax = diagram_ax(axes[1])
    ax.set_xlim(-1.6, 14.0)
    ax.set_ylim(-1.6, 2.2)
    xs = [0.0, 2.9, 5.8, 8.7, 11.6]
    for x, lb in zip(xs, ["0", "1", "2", "3", "4"]):
        node(ax, x, 0, lb, r=0.44)
    selfloop(ax, xs[0], 0, r=0.44, label="1", where="left", size=0.52, c=RED, lab_c=RED)
    for k, lb in zip((1, 2, 3, 4), ["3/4", "1/2", "1/4", "0"]):
        if lb == "0":
            continue
        selfloop(ax, xs[k], 0, r=0.44, label=lb, where="top", size=0.52, c=BLUE, lab_c=BLUE)
    for k, lb in zip((1, 2, 3, 4), ["1/4", "1/2", "3/4", "1"]):
        arc(ax, xs[k], 0, xs[k - 1], 0, rad=-0.34, r=0.44, label=lb, c=GREEN,
            lab_c=DGREEN, lab_off=0.26)
    ax.text(5.8, -1.42, "painting fish, $n=4$: state $=$ number of green fish left; "
                        "$p_{i,i-1}=i/n$, $p_{ii}=(n-i)/n$   ·   rec18 P1",
            ha="center", va="center", fontsize=10.5, color=MUTED)
    ax.set_title("(b)  the painting-fish chain", fontsize=11, color=INK)

    fig.tight_layout()
    save(fig, "models")


# ===========================================================================
# Fig 1.7 — rec18 P3 six-state chain
# ===========================================================================
def fig_rec18():
    fig, ax = plt.subplots(figsize=(11.2, 5.6))
    diagram_ax(ax)
    ax.set_xlim(-1.5, 14.0)
    ax.set_ylim(-4.6, 2.3)
    xs = [0.0, 3.1, 6.2, 9.3, 12.4]
    for x, lb in zip(xs, ["$s_1$", "$s_2$", "$s_3$", "$s_4$", "$s_5$"]):
        node(ax, x, 0, lb, r=0.50, fs=11.5)
    node(ax, 6.2, -3.2, "$s_0$", r=0.50, fs=11.5, fc="#f3effa", ec=PURPLE)

    selfloop(ax, xs[0], 0, r=0.50, label="1", where="top", size=0.62, c=RED, lab_c=RED)
    selfloop(ax, xs[4], 0, r=0.50, label="1", where="top", size=0.62, c=RED, lab_c=RED)
    selfloop(ax, xs[1], 0, r=0.50, label="1/2", where="top", size=0.62, c=BLUE, lab_c=BLUE)
    selfloop(ax, xs[2], 0, r=0.50, label="1/4", where="top", size=0.62, c=BLUE, lab_c=BLUE)
    selfloop(ax, xs[3], 0, r=0.50, label="1/2", where="top", size=0.62, c=BLUE, lab_c=BLUE)

    straight(ax, xs[1], 0, xs[0], 0, r=0.50, label="1/2", c=GREEN, lab_dy=0.34)
    straight(ax, xs[2], 0, xs[1], 0, r=0.50, label="1/4", c=GREEN, lab_dy=0.34)
    straight(ax, xs[2], 0, xs[3], 0, r=0.50, label="1/2", c=ORANGE, lab_dy=0.34)
    straight(ax, xs[3], 0, xs[4], 0, r=0.50, label="1/2", c=ORANGE, lab_dy=0.34)

    for tx, lab, dx in [(xs[0], "1/3", -0.55), (xs[2], "1/3", 0.42), (xs[4], "1/3", 0.55)]:
        ax.annotate("", xy=(tx, -0.50), xytext=(6.2, -3.2),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.26,head_length=0.55",
                                    color=PURPLE, lw=1.5, shrinkA=36, shrinkB=6), zorder=2)
    ax.text(2.35, -1.95, "1/3", fontsize=10.5, color=PURPLE, ha="center",
            bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.95))
    ax.text(6.68, -1.75, "1/3", fontsize=10.5, color=PURPLE, ha="center",
            bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.95))
    ax.text(10.05, -1.95, "1/3", fontsize=10.5, color=PURPLE, ha="center",
            bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.95))
    ax.text(6.2, -4.25, "the process starts at $s_0$ just before the first trial   ·   rec18 P3",
            ha="center", va="center", fontsize=10.5, color=MUTED)
    fig.tight_layout()
    save(fig, "rec18")


if __name__ == "__main__":
    fig_twostate()
    fig_checkout()
    fig_trellis()
    fig_convergence()
    fig_recipe()
    fig_models()
    fig_rec18()
