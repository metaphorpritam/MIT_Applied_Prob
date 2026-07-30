# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G4 section 1 — Conditional expectation as a r.v., iterated
expectations, law of total variance.

Run:  uv run computes/g4_s1_figs.py
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
    p = IMG / f"g4_s1_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


def box(ax, x, y, w, h, text, fc="#eef4fc", ec=BLUE, fs=9.5, tc=INK, r=0.03, lw=1.3):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h,
                                   boxstyle=f"round,pad=0.004,rounding_size={r}",
                                   fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, zorder=5, linespacing=1.45)


def arrow(ax, x1, y1, x2, y2, c=MUTED, lw=1.4, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=c, lw=lw,
                                shrinkA=2, shrinkB=2))


# ============================================================================
# Fig 1.1 — E[X | Y] is a function of Y, hence a random variable
# ============================================================================
def fig_condexp():
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.3))

    # ---- (a) discrete: two class sections -------------------------------
    ax = axes[0]
    ys = [1, 2]
    gs = [90, 60]
    ps = [1 / 3, 2 / 3]
    ax.plot([0.6, 2.4], [70, 70], color=MUTED, ls="--", lw=1.3, zorder=1)
    ax.text(2.38, 70.9, r"$\mathbb{E}[X]=70$", color=MUTED, fontsize=9.5, ha="right")
    for y, g, p in zip(ys, gs, ps):
        ax.plot([y, y], [50, g], color=GRID_C, lw=1.2, zorder=1)
        ax.plot([y], [g], "o", ms=11, color=BLUE, zorder=3)
        ax.annotate(f"$g({y})={g}$\n$\\mathbf{{P}}(Y={y})={'1/3' if p < .5 else '2/3'}$",
                    xy=(y, g), xytext=(y + (0.28 if y == 1 else -0.28), g + (6 if y == 1 else -12)),
                    ha="left" if y == 1 else "right", fontsize=9.5, color=INK,
                    arrowprops=dict(arrowstyle="-", color=AXIS_C, lw=1))
    ax.set_xlim(0.55, 2.45)
    ax.set_ylim(50, 100)
    ax.set_xticks([1, 2])
    ax.set_xlabel("value $y$ of the section label $Y$")
    ax.set_ylabel(r"$g(y)=\mathbb{E}[X\mid Y=y]$")
    ax.set_title("(a) discrete $Y$: two class sections (L12 slide 4)")

    # ---- (b) continuous: stick breaking ---------------------------------
    ax = axes[1]
    yy = np.linspace(0, 1, 200)
    ax.plot(yy, yy / 2, color=BLUE, lw=2.2, label=r"$g(y)=\mathbb{E}[X\mid Y=y]=y/2$")
    ax.plot([0, 1], [0.25, 0.25], color=MUTED, ls="--", lw=1.3)
    ax.text(0.02, 0.262, r"$\mathbb{E}[X]=\ell/4$", color=MUTED, fontsize=9.5)
    # density of Y along the bottom
    ax.add_patch(mp.Rectangle((0, -0.075), 1, 0.045, fc=ORANGE, alpha=0.35, ec=ORANGE, lw=1))
    ax.text(0.5, -0.053, r"$Y\sim U(0,\ell)$", ha="center", va="center", fontsize=9, color=INK)
    # induced density of E[X|Y] along the left
    ax.add_patch(mp.Rectangle((-0.085, 0), 0.05, 0.5, fc=GREEN, alpha=0.35, ec=GREEN, lw=1))
    ax.text(-0.060, 0.25, r"$\mathbb{E}[X\mid Y]\sim U(0,\ell/2)$", ha="center", va="center",
            rotation=90, fontsize=9, color=INK)
    y0 = 0.72
    ax.plot([y0, y0], [0, y0 / 2], color=PURPLE, lw=1.3, ls=":")
    ax.plot([0, y0], [y0 / 2, y0 / 2], color=PURPLE, lw=1.3, ls=":")
    ax.plot([y0], [y0 / 2], "o", ms=8, color=PURPLE)
    ax.annotate(r"one outcome: $Y=0.72\ell \Rightarrow \mathbb{E}[X\mid Y]=0.36\ell$",
                xy=(y0, y0 / 2), xytext=(0.30, 0.52), fontsize=9, color=INK,
                arrowprops=dict(arrowstyle="-|>", color=AXIS_C, lw=1.1))
    ax.set_xlim(-0.10, 1.03)
    ax.set_ylim(-0.09, 0.62)
    ax.set_xticks([0, 0.5, 1])
    ax.set_xticklabels(["0", r"$\ell/2$", r"$\ell$"])
    ax.set_yticks([0, 0.25, 0.5])
    ax.set_yticklabels(["0", r"$\ell/4$", r"$\ell/2$"])
    ax.set_xlabel("value $y$ of the first-break length $Y$")
    ax.set_ylabel(r"$g(y)=y/2$")
    ax.set_title("(b) continuous $Y$: stick breaking (L12 slide 2)")
    ax.legend(loc="upper left", fontsize=9)

    fig.tight_layout()
    save(fig, "condexp")


# ============================================================================
# Fig 1.2 — the stick-breaking experiment
# ============================================================================
def fig_stick():
    fig = plt.figure(figsize=(11.2, 4.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.24)

    # ---- (a) schematic ---------------------------------------------------
    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(0.0, 1.10)
    ax.axis("off")
    ax.grid(False)

    yv, xv = 0.68, 0.41
    rows = [
        (0.86, 1.0, None, "start: a stick of length $\\ell$"),
        (0.55, 1.0, yv, "break 1 — uniform on $[0,\\ell]$; keep the left piece, length $Y$"),
        (0.24, yv, xv, "break 2 — uniform on $[0,Y]$; keep the left piece, length $X$"),
    ]
    for (yy, length, cut, lab) in rows:
        ax.add_patch(mp.Rectangle((0, yy), length, 0.075, fc="#f2f1ea", ec=AXIS_C, lw=1.2))
        if cut is not None:
            ax.add_patch(mp.Rectangle((0, yy), cut, 0.075, fc=BLUE, alpha=0.30,
                                      ec=BLUE, lw=1.4))
            ax.plot([cut, cut], [yy - 0.030, yy + 0.105], color=RED, lw=2.0)
        ax.text(0.0, yy + 0.135, lab, ha="left", va="bottom", fontsize=8.8, color=MUTED)
    ax.annotate("", xy=(0, 0.515), xytext=(yv, 0.515),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.1))
    ax.text(yv / 2, 0.455, "$Y$", ha="center", fontsize=11, color=INK)
    ax.annotate("", xy=(0, 0.205), xytext=(xv, 0.205),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.1))
    ax.text(xv / 2, 0.145, "$X$", ha="center", fontsize=11, color=INK)
    ax.annotate("", xy=(0, 0.825), xytext=(1.0, 0.825),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.1))
    ax.text(0.5, 0.765, "$\\ell$", ha="center", fontsize=11, color=INK)
    ax.text(0.0, 1.055, "(a) the two-break experiment", ha="left", fontsize=11,
            color=INK, fontweight="600")
    ax.text(0.0, 0.045,
            r"$\mathbb{E}[X\mid Y]=Y/2$,   $\operatorname{var}(X\mid Y)=Y^2/12$",
            ha="left", fontsize=10, color=INK)

    # ---- (b) marginal density of X --------------------------------------
    ax = fig.add_subplot(gs[0, 1])
    xs = np.linspace(0.004, 1, 500)
    ax.plot(xs, np.log(1 / xs), color=BLUE, lw=2.2,
            label=r"$f_X(x)=\ln(1/x)$,  $0<x<1$")
    ax.fill_between(xs, 0, np.log(1 / xs), color=BLUE, alpha=0.13)
    ax.axvline(0.25, color=ORANGE, ls="--", lw=1.5)
    ax.text(0.268, 4.15, r"$\mathbb{E}[X]=\ell/4$", color=ORANGE, fontsize=9.5)
    ax.axvline(0.5, color=GREEN, ls=":", lw=1.5)
    ax.text(0.518, 3.45, r"$\mathbb{E}[Y]=\ell/2$", color=DGREEN, fontsize=9.5)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 5.0)
    ax.set_xlabel(r"$x$  (in units of $\ell$)")
    ax.set_ylabel(r"$f_X(x)$")
    ax.set_title(r"(b) the resulting density of $X$;  $\operatorname{var}(X)=7\ell^2/144$")
    ax.legend(loc="upper right", fontsize=9)

    save(fig, "stick")


# ============================================================================
# Fig 1.3 — variance decomposition: within vs between
# ============================================================================
def fig_vardecomp():
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.3),
                             gridspec_kw={"width_ratios": [1.35, 1.0]})
    rng = np.random.default_rng(41)

    # ---- (a) the 30 students --------------------------------------------
    ax = axes[0]
    s1 = 90 + np.sqrt(10) * np.array([1, 1, 1, 1, 1, -1, -1, -1, -1, -1.0])
    s2 = 60 + np.sqrt(20) * np.array([1] * 10 + [-1] * 10, dtype=float)
    j1 = rng.uniform(-0.16, 0.16, len(s1))
    j2 = rng.uniform(-0.16, 0.16, len(s2))
    ax.plot(1 + j1, s1, "o", ms=6, color=BLUE, alpha=0.8, label="section 1 (10 students)")
    ax.plot(2 + j2, s2, "o", ms=6, color=ORANGE, alpha=0.8, label="section 2 (20 students)")
    ax.plot([0.72, 1.28], [90, 90], color=BLUE, lw=2.4)
    ax.plot([1.72, 2.28], [60, 60], color=ORANGE, lw=2.4)
    ax.axhline(70, color=MUTED, ls="--", lw=1.4)
    ax.text(2.46, 70.8, r"grand mean $\mathbb{E}[X]=70$", color=MUTED, fontsize=9,
            ha="right")
    ax.annotate("", xy=(0.80, 70), xytext=(0.80, 90),
                arrowprops=dict(arrowstyle="<|-|>", color=PURPLE, lw=1.5))
    ax.text(0.76, 80, "between", rotation=90, ha="right", va="center",
            fontsize=9.5, color=PURPLE)
    ax.annotate("", xy=(1.62, 60 - np.sqrt(20)), xytext=(1.62, 60 + np.sqrt(20)),
                arrowprops=dict(arrowstyle="<|-|>", color=DGREEN, lw=1.5))
    ax.text(1.585, 60, "within", rotation=90, ha="right", va="center",
            fontsize=9.5, color=DGREEN)
    ax.set_xlim(0.5, 2.5)
    ax.set_ylim(50, 100)
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["$Y=1$", "$Y=2$"])
    ax.set_xlabel("section")
    ax.set_ylabel("quiz score $x$")
    ax.set_title("(a) scores of 30 students, grouped by section")
    ax.legend(loc="lower left", fontsize=8.6)

    # ---- (b) the stacked decomposition ----------------------------------
    ax = axes[1]
    within, between = 50 / 3, 200.0
    ax.bar([0], [within], width=0.5, color=DGREEN, alpha=0.85,
           label=r"$\mathbb{E}[\operatorname{var}(X\mid Y)]=50/3\approx16.67$")
    ax.bar([0], [between], width=0.5, bottom=[within], color=PURPLE, alpha=0.85,
           label=r"$\operatorname{var}(\mathbb{E}[X\mid Y])=200$")
    ax.bar([1], [within + between], width=0.5, color=BLUE, alpha=0.85,
           label=r"$\operatorname{var}(X)=650/3\approx216.67$")
    ax.text(0, within / 2, "16.67", ha="center", va="center", fontsize=9,
            color="white", fontweight="600")
    ax.text(0, within + between / 2, "200.00", ha="center", va="center", fontsize=10,
            color="white", fontweight="600")
    ax.text(1, (within + between) / 2, "216.67", ha="center", va="center", fontsize=10,
            color="white", fontweight="600")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["within + between", "total"])
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(0, 300)
    ax.set_ylabel("variance (points$^2$)")
    ax.set_title("(b) law of total variance, L12 slide 5")
    ax.legend(loc="upper center", fontsize=8.4, ncol=1)

    fig.tight_layout()
    save(fig, "vardecomp")


# ============================================================================
# Fig 1.4 — the L12 slide 6 two-piece density, solved
# ============================================================================
def fig_twopiece():
    fig, ax = plt.subplots(figsize=(8.4, 4.3))
    ax.add_patch(mp.Rectangle((0, 0), 1, 1 / 3, fc=BLUE, alpha=0.30, ec=BLUE, lw=1.8))
    ax.add_patch(mp.Rectangle((1, 0), 1, 2 / 3, fc=ORANGE, alpha=0.30, ec=ORANGE, lw=1.8))
    ax.plot([0.5], [0], marker="^", ms=10, color=BLUE, clip_on=False, zorder=5)
    ax.plot([1.5], [0], marker="^", ms=10, color=ORANGE, clip_on=False, zorder=5)
    ax.axvline(7 / 6, color=MUTED, ls="--", lw=1.5)
    ax.text(7 / 6 + 0.03, 0.80, r"$\mathbb{E}[X]=7/6\approx1.1667$", color=MUTED, fontsize=10)
    ax.text(0.5, 0.175, "$Y=1$\n$\\mathbf{P}=1/3$", ha="center", va="center",
            fontsize=10, color=INK, linespacing=1.5)
    ax.text(1.5, 0.34, "$Y=2$\n$\\mathbf{P}=2/3$", ha="center", va="center",
            fontsize=10, color=INK, linespacing=1.5)
    ax.text(0.5, -0.105, r"$\mathbb{E}[X\mid Y{=}1]=\frac{1}{2}$" "\n"
                         r"$\operatorname{var}(X\mid Y{=}1)=\frac{1}{12}$",
            ha="center", va="top", fontsize=9.5, color=BLUE, linespacing=1.7)
    ax.text(1.5, -0.105, r"$\mathbb{E}[X\mid Y{=}2]=\frac{3}{2}$" "\n"
                         r"$\operatorname{var}(X\mid Y{=}2)=\frac{1}{12}$",
            ha="center", va="top", fontsize=9.5, color="#b8501f", linespacing=1.7)
    ax.set_xlim(-0.10, 2.18)
    ax.set_ylim(0, 0.95)
    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1 / 3, 2 / 3])
    ax.set_yticklabels(["0", "1/3", "2/3"])
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f_X(x)$")
    ax.set_title(r"$\operatorname{var}(X)=\mathbb{E}[\operatorname{var}(X\mid Y)]"
                 r"+\operatorname{var}(\mathbb{E}[X\mid Y])=\frac{1}{12}+\frac{2}{9}=\frac{11}{36}$")
    fig.subplots_adjust(bottom=0.30)
    save(fig, "twopiece")


# ============================================================================
# Fig 1.5 — decision flowchart: conditioning to get means and variances
# ============================================================================
def fig_recipe():
    fig, ax = plt.subplots(figsize=(11.0, 5.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    ax.grid(False)

    box(ax, 0.15, 4.45, 2.5, 0.85,
        "You want\n$\\mathbb{E}[X]$ or $\\operatorname{var}(X)$,\nbut $X$ is described in stages",
        fc="#f2f1ea", ec=AXIS_C, fs=9)
    box(ax, 3.15, 4.55, 3.0, 0.65,
        "Pick $Y$: the r.v. whose value\nmakes $X$ easy to describe",
        fc="#fdf3e6", ec=ORANGE, fs=9)
    box(ax, 6.75, 4.55, 4.05, 0.65,
        "Write $\\mathbb{E}[X\\mid Y=y]$ and $\\operatorname{var}(X\\mid Y=y)$\n"
        "as formulas in $y$ — call them $g(y)$, $h(y)$", fc="#fdf3e6", ec=ORANGE, fs=9)
    arrow(ax, 2.65, 4.87, 3.15, 4.87)
    arrow(ax, 6.15, 4.87, 6.75, 4.87)

    box(ax, 6.75, 3.55, 4.05, 0.62,
        "Replace $y$ by $Y$:  $\\mathbb{E}[X\\mid Y]=g(Y)$,  $\\operatorname{var}(X\\mid Y)=h(Y)$\n"
        "— these are random variables", fc="#eef4fc", ec=BLUE, fs=9)
    arrow(ax, 8.775, 4.55, 8.775, 4.17)

    box(ax, 1.55, 2.30, 3.6, 0.72,
        "Only the mean is needed?\n$\\mathbb{E}[X]=\\mathbb{E}[g(Y)]$\n(law of iterated expectations)",
        fc="#e9f7f1", ec=DGREEN, fs=9)
    box(ax, 5.95, 2.30, 4.6, 0.72,
        "The variance too?\n$\\operatorname{var}(X)=\\mathbb{E}[h(Y)]+\\operatorname{var}(g(Y))$\n"
        "(law of total variance)", fc="#efeafa", ec=PURPLE, fs=9)
    arrow(ax, 8.10, 3.55, 5.20, 3.06)
    arrow(ax, 9.20, 3.55, 9.20, 3.02)

    box(ax, 1.55, 1.05, 3.6, 0.72,
        "Compute $\\mathbb{E}[g(Y)]$ with the\nexpected-value rule over the\ndistribution of $Y$ alone",
        fc="#ffffff", ec=DGREEN, fs=9)
    box(ax, 5.95, 1.05, 4.6, 0.72,
        "$\\mathbb{E}[h(Y)]$: average the within-group spreads.\n"
        "$\\operatorname{var}(g(Y))$: spread of the group means.\nAdd them.",
        fc="#ffffff", ec=PURPLE, fs=9)
    arrow(ax, 3.35, 2.30, 3.35, 1.77)
    arrow(ax, 8.25, 2.30, 8.25, 1.77)

    box(ax, 3.20, 0.10, 4.6, 0.62,
        "Sanity check: $\\mathbb{E}[h(Y)]\\geq 0$ and $\\operatorname{var}(g(Y))\\geq 0$,\n"
        "so $\\operatorname{var}(X)$ is at least each piece",
        fc="#fdecec", ec=RED, fs=9)
    arrow(ax, 3.35, 1.05, 4.30, 0.72)
    arrow(ax, 8.25, 1.05, 6.90, 0.72)

    save(fig, "recipe")


# ============================================================================
# Fig 1.6 — rec12 P2: region of integration and the Laplace density
# ============================================================================
def fig_laplace():
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.2))

    ax = axes[0]
    z = 0.8
    xs = np.linspace(0, 3.2, 400)
    ax.fill_between(xs, 0, np.maximum(0, np.minimum(3.2, xs - z)),
                    color=BLUE, alpha=0.20, label=r"$\{Z>z\}$")
    ax.fill_between(xs, np.maximum(0, xs - z), 3.2, color=ORANGE, alpha=0.22,
                    label=r"$\{Z\leq z\}=\{x\leq y+z\}$")
    ax.plot(xs, xs - z, color=INK, lw=1.6)
    ax.text(2.55, 1.50, "$y = x - z$", fontsize=10, color=INK, rotation=34)
    ax.annotate(r"integrate $\lambda e^{-\lambda x}\cdot\lambda e^{-\lambda y}$" "\n"
                r"over the orange region",
                xy=(1.0, 2.2), xytext=(0.25, 2.60), fontsize=9.5, color=INK,
                arrowprops=dict(arrowstyle="-|>", color=AXIS_C, lw=1.1))
    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 3.2)
    ax.set_xlabel("$x$  (Romeo's lateness)")
    ax.set_ylabel("$y$  (Juliet's lateness)")
    ax.set_title(r"(a) the event $\{Z\leq z\}$ with $z=0.8>0$")
    ax.legend(loc="lower right", fontsize=8.4)

    ax = axes[1]
    zz = np.linspace(-4, 4, 800)
    lam = 1.0
    ax.plot(zz, lam / 2 * np.exp(-lam * np.abs(zz)), color=BLUE, lw=2.2,
            label=r"$f_Z(z)=\frac{\lambda}{2}e^{-\lambda|z|}$  ($\lambda=1$)")
    ax.fill_between(zz, 0, lam / 2 * np.exp(-lam * np.abs(zz)), color=BLUE, alpha=0.13)
    ax.axvline(0, color=MUTED, ls="--", lw=1.2)
    ax.text(1.35, 0.40, r"$\mathbb{E}[Z]=0$" "\n"
                        r"$\operatorname{var}(Z)=2/\lambda^2=2$",
            color=INK, fontsize=9.5, linespacing=1.6)
    ax.annotate("kink at $z=0$: $f_Z$ is\ncontinuous but not\ndifferentiable there",
                xy=(0, 0.50), xytext=(-3.85, 0.34), fontsize=8.8, color=MUTED,
                linespacing=1.4, va="center",
                arrowprops=dict(arrowstyle="-|>", color=AXIS_C, lw=1.1))
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 0.60)
    ax.set_xlabel("$z$")
    ax.set_ylabel("$f_Z(z)$")
    ax.set_title("(b) the Laplace density of $Z=X-Y$ (rec12 P2)")
    ax.legend(loc="upper right", fontsize=9)

    fig.tight_layout()
    save(fig, "laplace")


# ============================================================================
# Fig 1.7 — rec12 P3: polar coordinates of a standard normal pair
# ============================================================================
def fig_polar():
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.3),
                             gridspec_kw={"width_ratios": [1.0, 1.15]})
    rng = np.random.default_rng(7)

    ax = axes[0]
    n = 1400
    xs, ys = rng.normal(0, 1, n), rng.normal(0, 1, n)
    ax.plot(xs, ys, ".", ms=3, color=BLUE, alpha=0.42)
    for r in (1, 2, 3):
        ax.add_patch(plt.Circle((0, 0), r, fill=False, ec=MUTED, lw=1.0, ls="--"))
    th = 0.9
    rr = 2.4
    ax.annotate("", xy=(rr * math.cos(th), rr * math.sin(th)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.0))
    ax.text(rr * math.cos(th) / 2 - 0.30, rr * math.sin(th) / 2 + 0.16, "$R$",
            fontsize=12, color="#b8501f")
    arc = mp.Arc((0, 0), 1.35, 1.35, theta1=0, theta2=math.degrees(th),
                 color=DGREEN, lw=1.8)
    ax.add_patch(arc)
    ax.text(0.90, 0.24, r"$\Theta$", fontsize=12, color=DGREEN)
    ax.plot([0, 3.3], [0, 0], color=AXIS_C, lw=1.0)
    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-3.4, 3.4)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(r"(a) $(X,Y)$ i.i.d. $N(0,1)$; circular symmetry")

    ax = axes[1]
    rs = np.linspace(0, 5, 500)
    ax.plot(rs, rs * np.exp(-rs ** 2 / 2), color=BLUE, lw=2.2,
            label=r"$f_R(r)=re^{-r^2/2}$ (Rayleigh)")
    ax.fill_between(rs, 0, rs * np.exp(-rs ** 2 / 2), color=BLUE, alpha=0.13)
    ax.axvline(1.0, color=GREEN, ls=":", lw=1.5)
    ax.text(0.90, 0.665, "mode at $r=1$", color=DGREEN, fontsize=9.5, ha="right")
    ax.axvline(math.sqrt(math.pi / 2), color=ORANGE, ls="--", lw=1.5)
    ax.annotate(r"$\mathbb{E}[R]=\sqrt{\pi/2}\approx1.2533$",
                xy=(math.sqrt(math.pi / 2), 0.40), xytext=(2.05, 0.53),
                color="#b8501f", fontsize=9.5,
                arrowprops=dict(arrowstyle="-|>", color=AXIS_C, lw=1.1))
    ax.plot([0, 2 * math.pi], [1 / (2 * math.pi)] * 2, color=PURPLE, lw=2.2,
            label=r"$f_\Theta(\theta)=1/2\pi$ on $[0,2\pi]$")
    ax.text(3.15, 0.255, r"$f_{R,\Theta}(r,\theta)=f_R(r)f_\Theta(\theta)$" "\n"
                        r"$\Rightarrow R$ and $\Theta$ independent", fontsize=9.5,
            color=INK, linespacing=1.5)
    ax.set_xlim(0, 6.4)
    ax.set_ylim(0, 0.78)
    ax.set_xlabel(r"$r$  (or $\theta$, for the flat curve)")
    ax.set_ylabel("density")
    ax.set_title("(b) the two marginals (rec12 P3)")
    ax.legend(loc="upper right", fontsize=9)

    fig.tight_layout()
    save(fig, "polar")


if __name__ == "__main__":
    fig_condexp()
    fig_stick()
    fig_vardecomp()
    fig_twopiece()
    fig_recipe()
    fig_laplace()
    fig_polar()
    print("done")
