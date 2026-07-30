# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G3 section 4 — Derived distributions and convolution.

Run:  uv run computes/g3_s4_figs.py
"""
from __future__ import annotations

import math
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


def save(fig, name):
    p = IMG / f"g3_s4_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


def box(ax, x, y, w, h, text, fc="#eef4fc", ec=BLUE, fs=9.5, tc=INK, r=0.02):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.006,rounding_size={r}",
                                   fc=fc, ec=ec, lw=1.3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, zorder=5)


def arrow(ax, x1, y1, x2, y2, c=MUTED, lw=1.4, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=c, lw=lw, shrinkA=2, shrinkB=2))


# =====================================================================
# Fig 4.1 — the CDF method pipeline
# =====================================================================
def fig_cdfpipe():
    fig, ax = plt.subplots(figsize=(9.2, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.8)
    ax.axis("off")
    ax.grid(False)

    ys = 2.25
    box(ax, 0.15, ys, 2.9, 1.1,
        "1.  WRITE THE CDF\n$F_Y(y)=\\mathbf{P}(g(X)\\leq y)$", fc="#eef4fc", ec=BLUE)
    box(ax, 3.55, ys, 2.9, 1.1,
        "2.  INVERT THE EVENT\n$\\{g(X)\\leq y\\}=\\{X\\in A_y\\}$\nthen $F_Y(y)=\\int_{A_y}f_X(x)\\,dx$",
        fc="#fdf1ea", ec=ORANGE, fs=9)
    box(ax, 6.95, ys, 2.9, 1.1,
        "3.  DIFFERENTIATE\n$f_Y(y)=\\dfrac{d}{dy}F_Y(y)$", fc="#eaf7f1", ec=GREEN)
    arrow(ax, 3.10, ys + 0.55, 3.50, ys + 0.55)
    arrow(ax, 6.50, ys + 0.55, 6.90, ys + 0.55)

    ax.text(1.60, 1.95, "one line, always the same", ha="center", va="top",
            fontsize=8.5, color=MUTED, style="italic")
    ax.text(5.00, 1.95, "the only creative step", ha="center", va="top",
            fontsize=8.5, color=MUTED, style="italic")
    ax.text(8.40, 1.95, "chain rule lives here", ha="center", va="top",
            fontsize=8.5, color=MUTED, style="italic")

    # worked strip: Y = 2X + 3, X ~ U(0,1)
    box(ax, 0.15, 0.35, 2.9, 1.05,
        "$\\mathbf{P}(2X+3\\leq y)$", fc="white", ec=GRID_C, fs=10)
    box(ax, 3.55, 0.35, 2.9, 1.05,
        "$=\\mathbf{P}\\!\\left(X\\leq \\frac{y-3}{2}\\right)$\n$=F_X\\!\\left(\\frac{y-3}{2}\\right)$",
        fc="white", ec=GRID_C, fs=10)
    box(ax, 6.95, 0.35, 2.9, 1.05,
        "$f_Y(y)=\\frac{1}{2} f_X\\!\\left(\\frac{y-3}{2}\\right)$\n$=\\frac{1}{2}$ on $[3,5]$",
        fc="white", ec=GRID_C, fs=10)
    arrow(ax, 3.10, 0.88, 3.50, 0.88, c=GRID_C)
    arrow(ax, 6.50, 0.88, 6.90, 0.88, c=GRID_C)
    ax.text(0.15, 1.55, "example:  $Y=2X+3$,  $X\\sim U(0,1)$",
            ha="left", va="center", fontsize=9, color=INK, weight="600")
    save(fig, "cdfpipe")


# =====================================================================
# Fig 4.2 — the monotonic-map slope picture (L11 slide 2, redrawn)
# =====================================================================
def fig_monotone():
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.1))

    def g(t):
        return 0.25 * t ** 2 + 0.3 * t

    def gp(t):
        return 0.5 * t + 0.3

    # ---- left: the slope / interval-stretching picture
    ax = axes[0]
    xs = np.linspace(0.0, 5.0, 400)
    ax.plot(xs, g(xs), color=BLUE, lw=2.2, zorder=3)
    ax.text(4.55, g(4.55) - 1.05, "$g(x)$", color=BLUE, fontsize=12, ha="right")

    x0, d = 2.55, 0.42
    y0, y1 = g(x0), g(x0 + d)
    slope = gp(x0)
    ax.plot([x0, x0], [0, y0], ls=":", color=MUTED, lw=1.1)
    ax.plot([x0 + d, x0 + d], [0, y1], ls=":", color=MUTED, lw=1.1)
    ax.plot([0, x0], [y0, y0], ls=":", color=MUTED, lw=1.1)
    ax.plot([0, x0 + d], [y1, y1], ls=":", color=MUTED, lw=1.1)
    ax.plot([x0, x0 + d], [0.09, 0.09], color=ORANGE, lw=6, solid_capstyle="butt", zorder=4)
    ax.plot([0.05, 0.05], [y0, y1], color=GREEN, lw=6, solid_capstyle="butt", zorder=4)
    tt = np.linspace(x0 - 1.0, x0 + 1.3, 20)
    ax.plot(tt, y0 + slope * (tt - x0), color=RED, lw=1.3, ls="--", zorder=2)
    ax.plot([x0], [y0], "o", color=RED, ms=6, zorder=5)

    ax.annotate(r"slope $\dfrac{dg}{dx}(x)=%.2f$" % slope,
                xy=(x0 + 1.20, y0 + slope * 1.20), xytext=(2.15, 6.9),
                fontsize=9.5, color=RED, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.1))
    ax.annotate(r"$[x,\,x+\delta]$,  width $\delta$", xy=(x0 + d / 2, 0.09),
                xytext=(1.35, 1.30), fontsize=9.5, color=ORANGE, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.1))
    ax.annotate("$[y,\\,y+\\delta|g'(x)|]$\nwider by the factor $|g'|$",
                xy=(0.05, (y0 + y1) / 2), xytext=(0.70, 4.55),
                fontsize=9.5, color=DGREEN, ha="left",
                arrowprops=dict(arrowstyle="-|>", color=DGREEN, lw=1.1))
    ax.set_xlim(0, 5.1)
    ax.set_ylim(0, 8.6)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y=g(x)$")
    ax.set_title("A width-$\\delta$ $x$-interval maps to a\nwidth-$\\delta|g'|$ $y$-interval",
                 fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

    # ---- right: the two densities, drawn on their own axes
    ax = axes[1]
    xg = np.linspace(0.001, 5.1, 900)
    fx = np.exp(-((xg - 2.4) ** 2) / (2 * 0.85 ** 2)) / (0.85 * math.sqrt(2 * math.pi))
    yg = g(xg)
    fy = fx / gp(xg)
    ax.plot(xg, fx, color=ORANGE, lw=2.2, label="$f_X(x)$")
    ax.fill_between(xg, 0, fx, where=(xg >= x0) & (xg <= x0 + d), color=ORANGE, alpha=0.35)
    ax.plot(yg, fy, color=GREEN, lw=2.2, label="$f_Y(y)=f_X(x)/|g'(x)|$")
    ax.fill_between(yg, 0, fy, where=(yg >= y0) & (yg <= y1), color=GREEN, alpha=0.35)
    ax.annotate(r"area $\approx\delta f_X(x)$", xy=(x0 + d / 2, fx.max() * 0.55),
                xytext=(0.35, 0.52), fontsize=9, color="#a8501f",
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.0))
    ax.annotate("same area, spread\nover a wider base\n$\\Rightarrow$ lower height",
                xy=((y0 + y1) / 2, 0.14), xytext=(4.05, 0.40), fontsize=9, color=DGREEN,
                ha="center", arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.0))
    ax.set_xlim(0, 8.6)
    ax.set_ylim(0, 0.62)
    ax.set_xlabel("value  ($x$ for $f_X$,  $y$ for $f_Y$)")
    ax.set_ylabel("density")
    ax.set_title("Equal shaded areas:\n$\\delta f_X(x)=\\delta|g'(x)|\\,f_Y(y)$", fontsize=10)
    ax.legend(loc="upper right", fontsize=8.5)
    fig.tight_layout()
    save(fig, "monotone")


# =====================================================================
# Fig 4.3 — decision flowchart: which method for a derived distribution
# =====================================================================
def fig_methodflow():
    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    ax.grid(False)

    box(ax, 3.05, 5.35, 3.9, 0.72, "You want the distribution of $Y=g(X)$\nor $W=g(X,Y)$",
        fc="#f3f2ec", ec=AXIS_C, fs=9.5)

    box(ax, 0.10, 3.85, 2.35, 1.05, "$X$ is DISCRETE?\n$p_Y(y)=\\!\\!\\sum_{x:g(x)=y}\\!\\!p_X(x)$",
        fc="#eef4fc", ec=BLUE, fs=9)
    box(ax, 2.65, 3.85, 1.90, 1.05,
        "$Y=aX+b$?\n$f_Y(y)=\\frac{1}{|a|}f_X\\!\\left(\\frac{y-b}{a}\\right)$",
        fc="#eaf7f1", ec=GREEN, fs=8.5)
    box(ax, 4.75, 3.85, 2.20, 1.05, "$g$ strictly\nMONOTONIC?", fc="#fdf1ea", ec=ORANGE, fs=9.5)
    box(ax, 7.15, 3.85, 2.75, 1.05, "$W=X+Y$ with $X,Y$\nindependent?", fc="#f6eefc", ec=PURPLE,
        fs=9.5)

    for x in (1.28, 3.60, 5.85, 8.52):
        arrow(ax, 5.0, 5.30, x, 4.95, c=AXIS_C, lw=1.1)

    box(ax, 5.15, 2.10, 1.90, 1.05,
        "$f_Y(y)=\\dfrac{f_X(x)}{|dg/dx\\,(x)|}$\nat $x=g^{-1}(y)$", fc="#fdf1ea", ec=ORANGE, fs=8.5)
    arrow(ax, 6.10, 3.80, 6.10, 3.20, c=ORANGE)
    ax.text(6.22, 3.50, "yes", fontsize=8.5, color=ORANGE, ha="left", va="center")

    box(ax, 7.60, 2.10, 2.00, 1.05, "CONVOLVE\n$f_W=f_X*f_Y$", fc="#f6eefc", ec=PURPLE, fs=9)
    arrow(ax, 8.60, 3.80, 8.60, 3.20, c=PURPLE)
    ax.text(8.72, 3.50, "yes", fontsize=8.5, color=PURPLE, ha="left", va="center")

    box(ax, 1.80, 0.45, 6.40, 1.20,
        "OTHERWISE — THE CDF METHOD (always works)\n"
        "$F_Y(y)=\\mathbf{P}(g(X)\\leq y)$, invert to an $x$-event, integrate $f_X$, differentiate",
        fc="#fbeaea", ec=RED, fs=9.5)
    arrow(ax, 4.95, 3.80, 4.95, 1.70, c=RED)
    ax.text(4.83, 2.75, "no", fontsize=8.5, color=RED, ha="right", va="center")
    arrow(ax, 7.30, 3.80, 7.30, 1.70, c=RED)
    ax.text(7.37, 2.75, "no", fontsize=8.5, color=RED, ha="left", va="center")

    ax.text(4.98, 0.14, "special cases are shortcuts, not substitutes: every box above is the "
                        "CDF method with the work already done",
            ha="center", va="bottom", fontsize=8.5, color=MUTED, style="italic")
    save(fig, "methodflow")


# =====================================================================
# Fig 4.4 — Z = Y/X on the unit square
# =====================================================================
def fig_ratio():
    fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.6))

    for ax, z, ttl in ((axes[0], 0.6, "$0\\leq z\\leq 1$:   $F_Z(z)=z/2$"),
                       (axes[1], 2.0, "$z\\geq 1$:   $F_Z(z)=1-\\dfrac{1}{2z}$")):
        ax.add_patch(mp.Rectangle((0, 0), 1, 1, fc="none", ec=AXIS_C, lw=1.4))
        xs = np.linspace(0, 1, 300)
        ln = np.minimum(z * xs, 1.0)
        ax.fill_between(xs, 0, ln, color=BLUE, alpha=0.30)
        ax.plot(xs, ln, color=BLUE, lw=2.0)
        ax.text(0.02, 0.02, "", fontsize=8)
        ax.set_xlim(-0.12, 1.25)
        ax.set_ylim(-0.12, 1.48)
        ax.set_aspect("equal")
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_title(ttl, fontsize=10)
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.grid(False)
        if z <= 1:
            ax.plot([1, 1], [0, z], color=ORANGE, lw=3, solid_capstyle="butt")
            ax.text(1.04, z / 2, "$z$", color=ORANGE, fontsize=11, va="center")
            ax.text(0.62, 0.12, "area\n$=\\frac{1}{2}\\cdot 1\\cdot z$", fontsize=9,
                    color=INK, ha="center")
        else:
            ax.plot([0, 1 / z], [1, 1], color=ORANGE, lw=3, solid_capstyle="butt")
            ax.text(1 / (2 * z), 1.06, "$1/z$", color=ORANGE, fontsize=10, ha="center")
            ax.annotate("white area $=\\frac{1}{2}\\cdot\\frac{1}{z}\\cdot 1=\\frac{1}{2z}$",
                        xy=(0.13, 0.88), xytext=(-0.14, 1.30), fontsize=8.5, color=INK, ha="left",
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.9))
        ax.annotate("$y=zx$", xy=(0.80 if z <= 1 else 0.42 / z, min(z * (0.80 if z <= 1 else 0.42 / z), 1.0)),
                    xytext=(0.46, 0.90) if z <= 1 else (0.55, 0.42), fontsize=10, color=BLUE,
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0))

    ax = axes[2]
    zz = np.linspace(0.001, 4, 600)
    Fz = np.where(zz <= 1, zz / 2, 1 - 1 / (2 * zz))
    fz = np.where(zz <= 1, 0.5, 1 / (2 * zz ** 2))
    ax.plot(zz, Fz, color=GREEN, lw=2.2, label="$F_Z(z)$")
    ax.plot(zz, fz, color=RED, lw=2.2, label="$f_Z(z)$")
    ax.axvline(1, color=MUTED, ls=":", lw=1.2)
    ax.text(1.05, 0.93, "kink at $z=1$", fontsize=8.5, color=MUTED)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("$z$")
    ax.set_title("CDF and PDF of $Z=Y/X$", fontsize=10)
    ax.legend(loc="center right", fontsize=9)
    fig.tight_layout()
    save(fig, "ratio")


# =====================================================================
# Fig 4.5 — rec11 P3 : the piecewise map and the resulting density
# =====================================================================
def fig_rec11p3():
    fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.6))
    yv = 1.2

    ax = axes[0]
    tl = np.linspace(-3.0, 0, 200)
    tr = np.linspace(0, 3.0, 300)
    ax.plot(tl, -tl, color=BLUE, lw=2.2)
    ax.plot(tr, np.sqrt(tr), color=BLUE, lw=2.2)
    ax.axhline(yv, color=RED, ls="--", lw=1.4)
    ax.text(-2.95, yv + 0.09, "$y$", color=RED, fontsize=11)
    ax.plot([-yv, -yv], [0, yv], ls=":", color=MUTED, lw=1.1)
    ax.plot([yv ** 2, yv ** 2], [0, yv], ls=":", color=MUTED, lw=1.1)
    ax.plot([-yv, yv ** 2], [0.03, 0.03], color=ORANGE, lw=5, solid_capstyle="butt", zorder=4)
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 3.0)
    ax.set_xticks([-yv, 0, yv ** 2])
    ax.set_xticklabels(["$-y$", "0", "$y^2$"])
    ax.set_xlabel("$t$")
    ax.set_ylabel("$g(t)$")
    ax.set_title("$\\{g(X)\\leq y\\}=\\{-y\\leq X\\leq y^2\\}$", fontsize=10)
    ax.text(0.0, 2.55, "$g(t)=-t$", color=BLUE, fontsize=9.5, ha="right")
    ax.text(1.05, 0.60, "$g(t)=\\sqrt{t}$", color=BLUE, fontsize=9.5, ha="left")

    ax = axes[1]
    xg = np.linspace(-3, 3, 600)
    fx = np.exp(-xg ** 2 / 2) / math.sqrt(2 * math.pi)
    ax.plot(xg, fx, color=GREEN, lw=2.2)
    ax.fill_between(xg, 0, fx, where=(xg >= -yv) & (xg <= 0), color=BLUE, alpha=0.32)
    ax.fill_between(xg, 0, fx, where=(xg > 0) & (xg <= yv ** 2), color=ORANGE, alpha=0.32)
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 0.46)
    ax.set_xticks([-yv, 0, yv ** 2])
    ax.set_xticklabels(["$-y$", "0", "$y^2$"])
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f_X(x)$")
    ax.set_title("$F_Y(y)=F_X(y^2)-F_X(-y)$", fontsize=10)
    ax.text(-0.75, 0.13, "left\nbranch", fontsize=8.5, color=BLUE, ha="center")
    ax.text(0.85, 0.10, "right\nbranch", fontsize=8.5, color="#a8501f", ha="center")

    ax = axes[2]
    ys = np.linspace(1e-4, 3.0, 700)
    fy = (2 * ys * np.exp(-ys ** 4 / 2) + np.exp(-ys ** 2 / 2)) / math.sqrt(2 * math.pi)
    part_a = 2 * ys * np.exp(-ys ** 4 / 2) / math.sqrt(2 * math.pi)
    part_b = np.exp(-ys ** 2 / 2) / math.sqrt(2 * math.pi)
    ax.plot(ys, fy, color=RED, lw=2.4, label="$f_Y(y)$")
    ax.plot(ys, part_a, color=ORANGE, lw=1.5, ls="--", label="$2yf_X(y^2)$")
    ax.plot(ys, part_b, color=BLUE, lw=1.5, ls="--", label="$f_X(-y)$")
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 0.95)
    ax.set_xlabel("$y$")
    ax.set_title("$f_Y(y)=\\frac{1}{\\sqrt{2\\pi}}(2ye^{-y^4/2}+e^{-y^2/2})$", fontsize=10)
    ax.legend(loc="upper right", fontsize=8.5)
    fig.tight_layout()
    save(fig, "rec11p3")


# =====================================================================
# Fig 4.6 — discrete convolution mechanics (flip, shift, multiply, add)
# =====================================================================
def fig_discconv():
    pX = {0: 1 / 6, 1: 1 / 3, 2: 1 / 2}
    pY = {0: 1 / 4, 1: 1 / 4, 2: 1 / 2}
    lX = {0: "1/6", 1: "1/3", 2: "1/2"}
    lY = {0: "1/4", 1: "1/4", 2: "1/2"}
    pW = np.convolve([pX[0], pX[1], pX[2]], [pY[0], pY[1], pY[2]])
    lW = ["1/24", "1/8", "7/24", "7/24", "1/4"]

    fig = plt.figure(figsize=(10.4, 6.4))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.05], hspace=0.42, wspace=0.24)

    def stems(ax, ks, vs, color, marker="o", ls="-", lw=2.0, ms=6, label=None):
        for k, v in zip(ks, vs):
            ax.plot([k, k], [0, v], color=color, lw=lw, ls=ls, solid_capstyle="butt", zorder=3)
        ax.plot(ks, vs, marker, color=color, ms=ms, ls="none", zorder=4, label=label)

    ax = fig.add_subplot(gs[0, 0])
    stems(ax, [0, 1, 2], [pX[0], pX[1], pX[2]], BLUE)
    for k in pX:
        ax.text(k, pX[k] + 0.028, lX[k], ha="center", fontsize=9, color=BLUE)
    ax.set_xlim(-2.6, 4.6)
    ax.set_ylim(0, 0.74)
    ax.set_xticks(range(-2, 5))
    ax.set_xlabel("$x$")
    ax.set_title("$p_X(x)$ — leave it alone", fontsize=10)

    ax = fig.add_subplot(gs[0, 1])
    w = 2
    ks = [w - 0, w - 1, w - 2]
    vs = [pY[0], pY[1], pY[2]]
    stems(ax, [k - 0.11 for k in [0, 1, 2]], [pX[0], pX[1], pX[2]], "#9dc0ea", marker="o",
          ls=":", lw=1.8, ms=5, label="$p_X(x)$")
    stems(ax, [k + 0.11 for k in ks], vs, ORANGE, marker="s", label="$p_Y(w-x)$, $w=2$")
    for k, v, lab in zip(ks, vs, [lY[0], lY[1], lY[2]]):
        ax.text(k + 0.11, v + 0.028, lab, ha="center", fontsize=9, color=ORANGE)
    for k in pX:
        ax.text(k - 0.11, pX[k] + 0.028, lX[k], ha="center", fontsize=8.5, color="#6e9fd4")
    ax.set_xlim(-2.6, 4.6)
    ax.set_ylim(0, 0.74)
    ax.set_xticks(range(-2, 5))
    ax.set_xlabel("$x$")
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title("$p_Y(w-x)$ flipped and shifted to $w=2$", fontsize=10)

    ax = fig.add_subplot(gs[1, 0])
    stems(ax, [0, 1, 2, 3, 4], list(pW), GREEN, marker="D")
    for k, lab in enumerate(lW):
        ax.text(k, pW[k] + 0.018, lab, ha="center", fontsize=9, color=DGREEN)
    ax.set_xlim(-0.7, 4.7)
    ax.set_ylim(0, 0.40)
    ax.set_xticks(range(0, 5))
    ax.set_xlabel("$w$")
    ax.set_title("$p_W(w)=\\sum_x p_X(x)p_Y(w-x)$", fontsize=10)

    ax = fig.add_subplot(gs[1, 1])
    ax.axis("off")
    ax.grid(False)
    rows = [
        ["$w$", "cross-products $p_X(x)\\,p_Y(w-x)$", "$p_W(w)$"],
        ["0", r"$\frac{1}{6}\cdot\frac{1}{4}$", r"$\frac{1}{24}$"],
        ["1", r"$\frac{1}{6}\cdot\frac{1}{4}+\frac{1}{3}\cdot\frac{1}{4}$", r"$\frac{1}{8}$"],
        ["2", r"$\frac{1}{6}\cdot\frac{1}{2}+\frac{1}{3}\cdot\frac{1}{4}+\frac{1}{2}\cdot\frac{1}{4}$", r"$\frac{7}{24}$"],
        ["3", r"$\frac{1}{3}\cdot\frac{1}{2}+\frac{1}{2}\cdot\frac{1}{4}$", r"$\frac{7}{24}$"],
        ["4", r"$\frac{1}{2}\cdot\frac{1}{2}$", r"$\frac{1}{4}$"],
        ["", "total", "$1$"],
    ]
    ytop, dy = 0.94, 0.128
    xs = [0.05, 0.20, 0.86]
    for i, row in enumerate(rows):
        y = ytop - i * dy
        wt = "600" if i == 0 or i == len(rows) - 1 else "normal"
        col = INK if i != len(rows) - 1 else DGREEN
        ax.text(xs[0], y, row[0], fontsize=9.5, ha="center", va="center", color=col, weight=wt)
        ax.text(xs[1], y, row[1], fontsize=9.5, ha="left", va="center", color=col, weight=wt)
        ax.text(xs[2], y, row[2], fontsize=9.5, ha="center", va="center", color=col, weight=wt)
        if i == 0 or i == len(rows) - 2:
            ax.plot([0.0, 0.98], [y - dy / 2, y - dy / 2], color=GRID_C, lw=1.0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.02, 1.02)
    ax.set_title("flip · shift · cross-multiply · add", fontsize=10)
    save(fig, "discconv")


# =====================================================================
# Fig 4.7 — sum of two uniforms: moving overlap -> triangle
# =====================================================================
def fig_unifsum():
    fig = plt.figure(figsize=(10.4, 5.9))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.05], hspace=0.48, wspace=0.22)

    for j, w in enumerate((0.4, 1.0, 1.6)):
        ax = fig.add_subplot(gs[0, j])
        xg = np.linspace(-1.4, 2.6, 900)
        fx = np.where((xg >= 0) & (xg <= 1), 1.0, 0.0)
        fy = np.where((w - xg >= 0) & (w - xg <= 1), 1.0, 0.0)
        ax.plot(xg, fx, color=BLUE, lw=2.0, label="$f_X(x)$")
        ax.plot(xg, fy + 0.02, color=ORANGE, lw=2.0, label="$f_Y(w-x)$")
        lo, hi = max(0.0, w - 1), min(1.0, w)
        ax.fill_between(xg, 0, 1.0, where=(xg >= lo) & (xg <= hi), color=GREEN, alpha=0.32)
        ax.set_xlim(-1.4, 2.6)
        ax.set_ylim(0, 1.42)
        ax.set_xlabel("$x$")
        ax.set_title(f"$w={w}$:  overlap $=[{lo:.1f},{hi:.1f}]$,  length ${hi-lo:.1f}$", fontsize=9)
        if j == 0:
            ax.legend(loc="upper right", fontsize=8)
            ax.set_ylabel("density")

    ax = fig.add_subplot(gs[1, :])
    wg = np.linspace(-0.4, 2.4, 700)
    fw = np.where((wg >= 0) & (wg <= 1), wg, np.where((wg > 1) & (wg <= 2), 2 - wg, 0.0))
    ax.plot(wg, fw, color=GREEN, lw=2.4)
    ax.fill_between(wg, 0, fw, color=GREEN, alpha=0.18)
    for w in (0.4, 1.0, 1.6):
        h = w if w <= 1 else 2 - w
        ax.plot([w], [h], "o", color=RED, ms=7, zorder=5)
        ax.plot([w, w], [0, h], color=RED, ls=":", lw=1.2)
        dx, ha = (-0.07, "right") if w < 1 else ((0.07, "left") if w > 1 else (0.0, "center"))
        ax.text(w + dx, h + 0.055, f"$f_W({w})={h:.1f}$", ha=ha, fontsize=9, color=RED)
    ax.set_xlim(-0.4, 2.4)
    ax.set_ylim(0, 1.24)
    ax.set_xlabel("$w$")
    ax.set_ylabel("$f_W(w)$")
    ax.set_title("$f_W(w)=$ length of the overlap $=$ the triangular (Irwin–Hall) density", fontsize=10)
    save(fig, "unifsum")


# =====================================================================
# Fig 4.8 — two independent normals: elliptical contours + the sum
# =====================================================================
def fig_normcontour():
    fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.7))
    sx, sy = 1.0, 2.0

    for ax, (a, b, ttl) in zip(axes[:2],
                               [(1.0, 1.0, "$\\sigma_x=\\sigma_y=1$: circles"),
                                (1.0, 2.0, "$\\sigma_x=1,\\ \\sigma_y=2$: ellipses")]):
        xg = np.linspace(-6, 6, 300)
        yg = np.linspace(-6, 6, 300)
        Xg, Yg = np.meshgrid(xg, yg)
        Z = np.exp(-Xg ** 2 / (2 * a ** 2) - Yg ** 2 / (2 * b ** 2)) / (2 * math.pi * a * b)
        ax.contour(Xg, Yg, Z, levels=6, colors=[BLUE], linewidths=1.2)
        w = 3.0
        ax.plot([-6, 6], [w + 6, w - 6], color=RED, lw=1.8)
        ax.text(3.3, -1.6, "$x+y=w$", color=RED, fontsize=9.5, rotation=-45)
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.set_aspect("equal")
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_title(ttl, fontsize=10)
        ax.grid(False)

    ax = axes[2]
    wg = np.linspace(-8, 8, 700)
    s2 = sx ** 2 + sy ** 2
    ax.plot(wg, np.exp(-wg ** 2 / (2 * sx ** 2)) / (sx * math.sqrt(2 * math.pi)),
            color=BLUE, lw=1.7, ls="--", label="$f_X$, $\\sigma_x=1$")
    ax.plot(wg, np.exp(-wg ** 2 / (2 * sy ** 2)) / (sy * math.sqrt(2 * math.pi)),
            color=ORANGE, lw=1.7, ls="--", label="$f_Y$, $\\sigma_y=2$")
    ax.plot(wg, np.exp(-wg ** 2 / (2 * s2)) / math.sqrt(2 * math.pi * s2),
            color=GREEN, lw=2.4, label="$f_W$, $\\sigma_w=\\sqrt{5}$")
    ax.set_xlim(-8, 8)
    ax.set_ylim(0, 0.44)
    ax.set_xlabel("value")
    ax.set_ylabel("density")
    ax.set_title("$W=X+Y\\sim N(0,\\sigma_x^2+\\sigma_y^2)$", fontsize=10)
    ax.legend(loc="upper right", fontsize=8.5)
    fig.tight_layout()
    save(fig, "normcontour")


# =====================================================================
# Fig 4.9 — covariance: sign of the cloud, and the zero-cov trap
# =====================================================================
def fig_cov():
    rng = np.random.default_rng(41)
    n = 500
    fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.5))

    a = rng.standard_normal(n)
    e = rng.standard_normal(n)
    panels = [
        (a, 0.9 * a + 0.45 * e, "$\\mathrm{cov}(X,Y)>0$", BLUE),
        (a, -0.9 * a + 0.45 * e, "$\\mathrm{cov}(X,Y)<0$", ORANGE),
    ]
    for ax, (u, v, ttl, c) in zip(axes[:2], panels):
        ax.scatter(u, v, s=9, color=c, alpha=0.55, lw=0)
        ax.axhline(0, color=AXIS_C, lw=1.0)
        ax.axvline(0, color=AXIS_C, lw=1.0)
        r = float(np.corrcoef(u, v)[0, 1])
        ax.set_title(f"{ttl}   ($\\rho\\approx{r:+.2f}$)", fontsize=10)
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_xlim(-3.4, 3.4)
        ax.set_ylim(-3.4, 3.4)
        ax.grid(False)

    ax = axes[2]
    u = rng.uniform(-2, 2, n)
    v = u ** 2 + 0.10 * rng.standard_normal(n)
    ax.scatter(u, v, s=9, color=GREEN, alpha=0.6, lw=0)
    ax.axhline(np.mean(v), color=AXIS_C, lw=1.0, ls=":")
    ax.axvline(0, color=AXIS_C, lw=1.0)
    r = float(np.corrcoef(u, v)[0, 1])
    ax.set_title(f"$Y\\approx X^2$: $\\rho\\approx{r:+.2f}$ but dependent", fontsize=10)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_xlim(-2.4, 2.4)
    ax.grid(False)
    fig.tight_layout()
    save(fig, "cov")


for f in (fig_cdfpipe, fig_monotone, fig_methodflow, fig_ratio, fig_rec11p3,
          fig_discconv, fig_unifsum, fig_normcontour, fig_cov):
    f()
print("done")
