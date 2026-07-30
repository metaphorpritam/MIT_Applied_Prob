# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for G6 section 4 - LMS and linear LMS estimation.

Run:  uv run computes/g6_s4_figs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
from mpl_style import setup, PAL, INK, MUTED, GRID_C, AXIS_C, diagram_ax  # noqa: E402

plt, _ = setup()
import matplotlib.patches as mp  # noqa: E402
import numpy as np  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL
rng = np.random.default_rng(4122)


def save(fig, name):
    p = IMG / f"g6_s4_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# =====================================================================
# model helpers (L22 running example)
# =====================================================================
def lms(x):
    x = np.asarray(x, dtype=float)
    lo = np.maximum(4.0, x - 1.0)
    hi = np.minimum(10.0, x + 1.0)
    return 0.5 * (lo + hi)


def cvar(x):
    x = np.asarray(x, dtype=float)
    lo = np.maximum(4.0, x - 1.0)
    hi = np.minimum(10.0, x + 1.0)
    return (hi - lo) ** 2 / 12.0


A_LIN, B_LIN = 0.9, 0.7


# =====================================================================
# Fig 1 - the joint support, one vertical slice, and the posterior it gives
# =====================================================================
def fig_slice():
    fig, ax = plt.subplots(1, 2, figsize=(10.6, 4.1),
                           gridspec_kw={"width_ratios": [1.25, 1]})

    a = ax[0]
    poly = np.array([[3, 4], [5, 4], [11, 10], [9, 10]])
    a.add_patch(mp.Polygon(poly, closed=True, fc="#dbe8f8", ec=BLUE, lw=1.6, zorder=2))
    a.annotate(r"$f_{\Theta,X}(\theta,x)=\frac{1}{12}$", xy=(8.5, 8.0),
               xytext=(11.0, 5.4), ha="center", fontsize=11, color=INK, zorder=5,
               arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    for xv, col in ((4.0, ORANGE), (7.0, GREEN), (10.0, PURPLE)):
        lo, hi = max(4.0, xv - 1), min(10.0, xv + 1)
        a.plot([xv, xv], [lo, hi], color=col, lw=3.0, zorder=6, solid_capstyle="butt")
        a.plot([xv], [0.5 * (lo + hi)], "o", color=col, ms=6, zorder=7)
        a.annotate(f"$x={xv:.0f}$", xy=(xv, lo), xytext=(xv, 2.35), ha="center",
                   fontsize=9.5, color=col,
                   arrowprops=dict(arrowstyle="-", color=col, lw=1.0, ls=":"))
    a.set_xlim(1.5, 12.5)
    a.set_ylim(2.0, 11.4)
    a.set_xticks([3, 5, 7, 9, 11])
    a.set_yticks([4, 6, 8, 10])
    a.set_xlabel(r"observation  $x$")
    a.set_ylabel(r"parameter  $\theta$")
    a.set_title("Support of the joint density (L22 slide 2)")

    b = ax[1]
    for xv, col, lab in ((4.0, ORANGE, "$x=4$   (truncated slice)"),
                         (7.0, GREEN, "$x=7$   (full slice)"),
                         (10.0, PURPLE, "$x=10$  (truncated slice)")):
        lo, hi = max(4.0, xv - 1), min(10.0, xv + 1)
        h = 1.0 / (hi - lo)
        b.plot([lo, lo, hi, hi], [0, h, h, 0], color=col, lw=2.0, label=lab)
        b.plot([0.5 * (lo + hi)], [h], "o", color=col, ms=6)
        b.annotate(r"$\hat\theta=%.1f$" % (0.5 * (lo + hi)),
                   xy=(0.5 * (lo + hi), h), xytext=(0.5 * (lo + hi), h + 0.085),
                   ha="center", fontsize=9, color=col)
    b.set_xlim(3.2, 11.3)
    b.set_ylim(0, 1.62)
    b.set_xlabel(r"$\theta$")
    b.set_ylabel(r"posterior  $f_{\Theta\mid X}(\theta\mid x)$")
    b.set_title("Posterior = uniform on the slice")
    b.legend(loc="upper center", fontsize=8.5)
    fig.tight_layout()
    save(fig, "slice")


# =====================================================================
# Fig 2 - conditional mean squared error var(Theta | X = x)
# =====================================================================
def fig_condmse():
    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    xs = np.linspace(3, 11, 1601)
    ax.plot(xs, cvar(xs), color=BLUE, lw=2.2,
            label=r"$\mathrm{var}(\Theta\mid X=x)$")
    ax.axhline(1 / 3, color=MUTED, lw=1.1, ls="--")
    ax.text(7.0, 1 / 3 + 0.012, r"$1/3$", ha="center", fontsize=9.5, color=MUTED)
    ax.axhline(5 / 18, color=ORANGE, lw=1.4, ls=":",
               label=r"overall LMS error $=5/18=0.2778$")
    ax.axhline(0.3, color=GREEN, lw=1.4, ls=":",
               label=r"overall error of the best line $=0.3$")
    ax.plot([3], [0], "o", color=BLUE, ms=6)
    ax.annotate("$x=3$ pins $\\Theta=4$:\nzero error", xy=(3.02, 0.004),
                xytext=(5.6, 0.075), fontsize=9, color=INK, ha="center",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    ax.set_xlim(2.7, 11.3)
    ax.set_ylim(-0.02, 0.52)
    ax.set_xticks([3, 5, 7, 9, 11])
    ax.set_xlabel(r"observation  $x$")
    ax.set_ylabel("conditional MSE")
    ax.set_title(r"Conditional mean squared error of $\hat\Theta=\mathbb{E}[\Theta\mid X]$")
    ax.legend(loc="upper left", fontsize=8.6)
    fig.tight_layout()
    save(fig, "condmse")


# =====================================================================
# Fig 3 - projection / orthogonality diagram
# =====================================================================
def fig_projection():
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    diagram_ax(ax)

    # the plane of all functions of X
    plane = np.array([[0.2, 0.35], [7.4, 0.35], [9.2, 2.35], [2.0, 2.35]])
    ax.add_patch(mp.Polygon(plane, closed=True, fc="#eef4fc", ec=BLUE, lw=1.4, zorder=1))
    ax.text(8.55, 0.66, "all estimators $g(X)$", ha="right", fontsize=10, color=BLUE, zorder=5)

    # the line of linear estimators, inside the plane
    ax.plot([1.35, 8.0], [1.05, 1.05], color=GREEN, lw=2.4, zorder=3)
    ax.text(8.15, 1.02, "$aX+b$", ha="left", va="center", fontsize=10, color=GREEN, zorder=5)

    O = np.array([2.6, 1.05])          # foot: the linear estimator
    H = np.array([5.0, 1.62])          # foot: the LMS estimator E[Theta|X]
    T = np.array([5.0, 4.30])          # Theta itself

    for p, c, lab, dy in ((T, ORANGE, r"$\Theta$", 0.24),
                          (H, BLUE, r"$\hat\Theta=\mathbb{E}[\Theta\mid X]$", -0.42),
                          (O, GREEN, r"$\hat\Theta_L$", -0.42)):
        ax.plot([p[0]], [p[1]], "o", color=c, ms=8, zorder=6)
        ax.text(p[0], p[1] + dy, lab, ha="center", fontsize=11, color=c, zorder=6)

    ax.annotate("", xy=H, xytext=T, arrowprops=dict(arrowstyle="->", color=RED, lw=2.0))
    ax.text(5.16, 2.95, r"error $\tilde\Theta$", ha="left", fontsize=10.5, color=RED)
    ax.annotate("", xy=O, xytext=T, arrowprops=dict(arrowstyle="->", color=MUTED,
                                                    lw=1.4, ls=(0, (5, 4))))
    ax.plot([O[0], H[0]], [O[1], H[1]], color=MUTED, lw=1.2, ls=(0, (2, 3)))

    # right-angle marker at H
    s = 0.26
    u = np.array([-1.0, 0.0]) * s          # along the plane
    v = np.array([0.0, 1.0]) * s           # along the error
    ax.plot([H[0] + u[0], H[0] + u[0] + v[0], H[0] + v[0]],
            [H[1] + u[1], H[1] + u[1] + v[1], H[1] + v[1]],
            color=RED, lw=1.2, zorder=6)

    ax.text(5.0, 4.95, r"$\mathbb{E}[\,\tilde\Theta\,h(X)\,]=0$  for every $h$"
                       "\n(the error is orthogonal to every function of the data)",
            ha="center", fontsize=10, color=INK)
    ax.set_xlim(-0.2, 10.6)
    ax.set_ylim(0.0, 5.7)
    fig.tight_layout()
    save(fig, "projection")


# =====================================================================
# Fig 4 - LMS curve vs best line, uniform example
# =====================================================================
def fig_curve_vs_line():
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    poly = np.array([[3, 4], [5, 4], [11, 10], [9, 10]])
    ax.add_patch(mp.Polygon(poly, closed=True, fc="#f0f0ec", ec=GRID_C, lw=1.2, zorder=1))
    xs = np.linspace(3, 11, 1601)
    ax.plot(xs, lms(xs), color=BLUE, lw=2.4,
            label=r"LMS  $\mathbb{E}[\Theta\mid X=x]$   (MSE $=5/18=0.2778$)")
    ax.plot(xs, A_LIN * xs + B_LIN, color=ORANGE, lw=2.2, ls="--",
            label=r"linear LMS  $0.9x+0.7$   (MSE $=0.3$)")
    ax.axhline(7, color=MUTED, lw=1.0, ls=":")
    ax.text(2.85, 7.12, r"$\mathbb{E}[\Theta]=7$", fontsize=9, color=MUTED, ha="left")
    ax.plot([7], [7], "o", color=INK, ms=5, zorder=6)
    ax.annotate("both pass through\n$(\\mathbb{E}[X],\\mathbb{E}[\\Theta])=(7,7)$",
                xy=(7, 7), xytext=(7.55, 5.15), fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    ax.annotate("", xy=(11, 10), xytext=(11, 10.6),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.4))
    ax.text(10.82, 10.62, "gap 0.6", ha="right", fontsize=9, color=RED)
    ax.set_xlim(2.6, 11.6)
    ax.set_ylim(3.2, 11.3)
    ax.set_xticks([3, 5, 7, 9, 11])
    ax.set_xlabel(r"observation  $x$")
    ax.set_ylabel(r"estimate of $\theta$")
    ax.set_title("The optimal estimator bends; the best line cannot")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, "curveline")


# =====================================================================
# Fig 5 - jointly normal: E[Theta|X] IS the line
# =====================================================================
def fig_normal():
    mu_t, sd_t, mu_x, sd_x, rho = 2.0, 1.5, 5.0, 2.0, 0.8
    a, b = rho * sd_t / sd_x, mu_t - rho * sd_t / sd_x * mu_x
    n = 4000
    z1, z2 = rng.standard_normal(n), rng.standard_normal(n)
    X = mu_x + sd_x * z1
    T = mu_t + sd_t * (rho * z1 + np.sqrt(1 - rho ** 2) * z2)

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.scatter(X, T, s=5, color=BLUE, alpha=0.20, edgecolors="none", zorder=2)
    xs = np.linspace(mu_x - 3.4 * sd_x, mu_x + 3.4 * sd_x, 200)
    ax.plot(xs, a * xs + b, color=ORANGE, lw=2.6, zorder=5,
            label=r"$a x+b=0.6x-1$   (linear LMS)")
    # empirical conditional means in bins
    edges = np.linspace(mu_x - 2.8 * sd_x, mu_x + 2.8 * sd_x, 15)
    ctr, mean = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (X >= lo) & (X < hi)
        if m.sum() > 25:
            ctr.append(0.5 * (lo + hi))
            mean.append(T[m].mean())
    ax.plot(ctr, mean, "o", color=DGREEN, ms=6, zorder=6,
            label=r"empirical $\mathbb{E}[\Theta\mid X\approx x]$")
    ax.set_xlim(mu_x - 3.6 * sd_x, mu_x + 3.6 * sd_x)
    ax.set_ylim(mu_t - 4.0 * sd_t, mu_t + 4.0 * sd_t)
    ax.set_xlabel(r"observation  $x$")
    ax.set_ylabel(r"parameter  $\theta$")
    ax.set_title(r"Jointly normal ($\rho=0.8$): the LMS estimator is exactly the line")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, "normal")


# =====================================================================
# Fig 6 - decision flowchart: which estimator
# =====================================================================
def fig_choose():
    fig, ax = plt.subplots(figsize=(9.6, 6.4))
    diagram_ax(ax)

    def box(x, y, w, h, txt, fc, ec, fs=9.6, r=0.16):
        ax.add_patch(mp.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                       boxstyle=f"round,pad=0.02,rounding_size={r}",
                                       fc=fc, ec=ec, lw=1.5, zorder=3))
        ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=INK, zorder=5)

    def dia(x, y, w, h, txt, fs=9.4):
        ax.add_patch(mp.Polygon([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2],
                                 [x - w / 2, y]], closed=True,
                                fc="#fdf3e3", ec=GOLD, lw=1.5, zorder=3))
        ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=INK, zorder=5)

    def arr(p, q, lab=None, dx=0.0, dy=0.0, col=MUTED):
        ax.annotate("", xy=q, xytext=p,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5,
                                    shrinkA=2, shrinkB=3))
        if lab:
            ax.text((p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, lab,
                    ha="center", va="center", fontsize=9, color=col, zorder=6,
                    bbox=dict(fc="white", ec="none", pad=1.2))

    SP, RB = 3.5, 8.6           # spine x ; right-hand outcome box centre x

    box(SP, 11.4, 5.2, 0.95, "You must guess $\\Theta$ and you will be\n"
                             "charged $(\\Theta-\\hat\\Theta)^2$", "#eef4fc", BLUE)
    dia(SP, 9.6, 4.4, 1.4, "Any data $X$ at all?")
    box(RB, 9.6, 3.0, 1.0, "$\\hat\\theta=\\mathbb{E}[\\Theta]$\nMSE $=\\mathrm{var}(\\Theta)$",
        "#e8f5ee", DGREEN)
    dia(SP, 7.3, 5.0, 1.6,
        "Full joint law available,\nand $\\mathbb{E}[\\Theta\\mid X]$ computable?")
    box(RB, 7.3, 3.0, 1.25, "$\\hat\\Theta=\\mathbb{E}[\\Theta\\mid X]$\n"
                            "smallest MSE of all\n(L22 slide 1)", "#e8f5ee", DGREEN)
    dia(SP, 4.9, 5.0, 1.6,
        "$\\Theta,X$ jointly normal\n(or $\\mathbb{E}[\\Theta\\mid X]$ linear)?")
    box(RB, 4.9, 3.0, 1.25, "the two coincide:\n$\\hat\\Theta_L=\\mathbb{E}[\\Theta\\mid X]$\n"
                            "(L22 slide 8)", "#e8f5ee", DGREEN)
    box(SP, 2.6, 5.6, 1.3,
        "$\\hat\\Theta_L=\\mathbb{E}[\\Theta]+\\frac{\\mathrm{cov}(\\Theta,X)}{\\mathrm{var}(X)}"
        "(X-\\mathbb{E}[X])$\nMSE $=(1-\\rho^2)\\sigma_\\Theta^2$\nneeds only 5 numbers",
        "#fdece3", ORANGE)
    box(5.6, 0.6, 8.6, 0.95, "MSE still too big?  Enlarge the family: feed "
                             "$X,X^2,X^3,\\ldots$ in as\nseparate observations "
                             "(L22 slide 9) — still only means and covariances",
        "#f4f2fb", PURPLE, fs=9.0)

    arr((SP, 10.92), (SP, 10.32))
    arr((SP + 2.2, 9.6), (RB - 1.5, 9.6), "no", dy=0.30)
    arr((SP, 8.90), (SP, 8.12), "yes", dx=0.42)
    arr((SP + 2.5, 7.3), (RB - 1.5, 7.3), "yes", dy=0.30)
    arr((SP, 6.50), (SP, 5.72), "no", dx=0.40)
    arr((SP + 2.5, 4.9), (RB - 1.5, 4.9), "yes", dy=0.30)
    arr((SP, 4.10), (SP, 3.27), "no", dx=0.40)
    arr((SP, 1.93), (SP, 1.10))
    ax.set_xlim(-0.2, 10.4)
    ax.set_ylim(0.0, 12.2)
    fig.tight_layout()
    save(fig, "choose")


# =====================================================================
# Fig 7 - rec22 Romeo & Juliet: three estimators and their conditional MSEs
# =====================================================================
def fig_romeo():
    a_rj, b_rj = 6 / 7, 2 / 7
    x = np.linspace(0.005, 0.995, 2000)
    L = np.abs(np.log(x))
    lmsx = (1 - x) / L
    E2 = (1 - x ** 2) / (2 * L)

    def cm(t):
        return t ** 2 - 2 * t * lmsx + E2

    fig, ax = plt.subplots(2, 1, figsize=(7.6, 6.4), sharex=True,
                           gridspec_kw={"height_ratios": [1.05, 1]})
    a = ax[0]
    a.plot(x, x, color=GREEN, lw=2.0, ls="--", label=r"MAP  $\hat\theta=x$")
    a.plot(x, lmsx, color=BLUE, lw=2.4, label=r"LMS  $(1-x)/|\ln x|$")
    a.plot(x, a_rj * x + b_rj, color=ORANGE, lw=2.0, ls="-.",
           label=r"linear LMS  $\frac{6}{7} x+\frac{2}{7}$")
    a.axhline(1.0, color=RED, lw=1.0, ls=":")
    a.text(0.02, 1.03, r"$\Theta$ never exceeds 1, but the line does, from $x=5/6$ on",
           fontsize=8.8, color=RED)
    a.plot([5 / 6], [1.0], "o", color=RED, ms=5)
    a.set_ylim(0, 1.22)
    a.set_ylabel("estimate")
    a.set_title("rec22 P1: three estimators of $\\Theta$ from one observation")
    a.legend(loc="upper left", fontsize=9, bbox_to_anchor=(0.015, 0.82))

    b = ax[1]
    b.plot(x, cm(x), color=GREEN, lw=2.0, ls="--", label="MAP  (overall $1/9=0.1111$)")
    b.plot(x, cm(lmsx), color=BLUE, lw=2.4,
           label="LMS  (overall $1/3-\\ln(4/3)=0.04565$)")
    b.plot(x, cm(a_rj * x + b_rj), color=ORANGE, lw=2.0, ls="-.",
           label="linear LMS  (overall $1/21=0.04762$)")
    b.set_ylim(0, 0.20)
    b.set_xlim(0, 1)
    b.set_xlabel(r"observed lateness  $x$")
    b.set_ylabel("conditional MSE")
    b.set_title("Conditional mean squared errors")
    b.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, "romeo")


fig_slice()
fig_condmse()
fig_projection()
fig_curve_vs_line()
fig_normal()
fig_choose()
fig_romeo()
print("done")
