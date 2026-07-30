# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G6 section 1 - Markov, Chebyshev, the sample mean, WLLN,
convergence in probability.

Run:  uv run computes/g6_s1_figs.py
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
from scipy import stats  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)

BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL
BOX_FC = "#eaf2fd"


def save(fig, name):
    p = IMG / f"g6_s1_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ===========================================================================
# Fig 1.1 - the Markov inequality picture (B&T Figure 5.1)
# ===========================================================================
def fig_markov():
    a = 1.5
    x = np.linspace(0, 5, 600)
    pdf = np.exp(-x)
    P = float(np.exp(-a))          # P(X >= a)
    EX = 1.0
    EY = a * P

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.5))

    ax = axes[0]
    ax.plot(x, pdf, color=BLUE, lw=2)
    m = x >= a
    ax.fill_between(x[m], 0, pdf[m], color=BLUE, alpha=0.28, lw=0)
    ax.axvline(a, color=ORANGE, lw=1.4, ls="--")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 1.18)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f_X(x)$")
    ax.set_title("(a)  PDF of $X\\geq 0$;  shaded area $=\\mathbf{P}(X\\geq a)$")
    ax.set_xticks([0, a, 2, 3, 4, 5])
    ax.set_xticklabels(["0", "$a$", "2", "3", "4", "5"])
    ax.annotate(f"$\\mathbf{{P}}(X\\geq a)={P:.3f}$", xy=(2.15, 0.10),
                xytext=(2.6, 0.52), color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    ax.text(0.12, 1.06, f"$\\mathbb{{E}}[X]={EX:.0f}$", color=MUTED, fontsize=10)

    ax = axes[1]
    ax.vlines([0, a], 0, [1 - P, P], color=ORANGE, lw=2.2)
    ax.plot([0, a], [1 - P, P], "o", color=ORANGE, ms=7)
    ax.axvline(a, color=ORANGE, lw=1.0, ls=":", alpha=0.6)
    ax.set_xlim(-0.35, 5)
    ax.set_ylim(0, 1.18)
    ax.set_xlabel("$y$")
    ax.set_ylabel("$p_{Y_a}(y)$")
    ax.set_title("(b)  PMF of the shifted-down $Y_a$")
    ax.set_xticks([0, a, 2, 3, 4, 5])
    ax.set_xticklabels(["0", "$a$", "2", "3", "4", "5"])
    ax.text(0.12, 1 - P + 0.05, f"$1-\\mathbf{{P}}(X\\geq a)={1-P:.3f}$",
            fontsize=9.5, color=INK)
    ax.text(a + 0.15, P + 0.05, f"$\\mathbf{{P}}(X\\geq a)={P:.3f}$",
            fontsize=9.5, color=INK)
    ax.text(2.1, 0.72,
            f"$\\mathbb{{E}}[Y_a]=a\\,\\mathbf{{P}}(X\\geq a)={EY:.3f}$\n"
            f"$\\leq\\mathbb{{E}}[X]={EX:.0f}$",
            fontsize=10, color=INK,
            bbox=dict(boxstyle="round,pad=0.4", fc="#fdf2ec", ec=ORANGE, lw=1.0))
    fig.tight_layout()
    save(fig, "markov")


# ===========================================================================
# Fig 1.2 - Chebyshev: tail shading + the g(x) <= (x-mu)^2 picture
# ===========================================================================
def fig_chebyshev():
    mu, sig, c = 0.0, 1.0, 1.6
    x = np.linspace(-4.2, 4.2, 900)
    pdf = stats.norm.pdf(x)

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6))

    ax = axes[0]
    ax.plot(x, pdf, color=BLUE, lw=2)
    for m in (x <= mu - c, x >= mu + c):
        ax.fill_between(x[m], 0, pdf[m], color=RED, alpha=0.30, lw=0)
    ax.axvline(mu, color=MUTED, lw=1.2, ls="--")
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(0, 0.52)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f_X(x)$")
    ax.set_xticks([mu - c, mu, mu + c])
    ax.set_xticklabels(["$\\mu-c$", "$\\mu$", "$\\mu+c$"])
    ax.set_title("(a)  the two tails $\\{|x-\\mu|\\geq c\\}$")
    tail = float(2 * stats.norm.sf(c))
    ax.annotate("", xy=(-2.05, 0.030), xytext=(-3.15, 0.155),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    ax.annotate("", xy=(2.05, 0.030), xytext=(-3.15, 0.155),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1,
                                connectionstyle="arc3,rad=-0.25"))
    ax.text(-4.05, 0.185, f"total shaded area\n"
            f"$=\\mathbf{{P}}(|X-\\mu|\\geq c)={tail:.4f}$",
            fontsize=9.5, color=INK, ha="left", va="bottom")

    ax = axes[1]
    ax.plot(x, (x - mu) ** 2, color=BLUE, lw=2, label="$(x-\\mu)^2$")
    g = np.where(np.abs(x - mu) >= c, c ** 2, 0.0)
    ax.fill_between(x, 0, g, step="mid", color=RED, alpha=0.25, lw=0)
    ax.plot(x, g, color=RED, lw=2, label="$g(x)$  (0 or $c^2$)")
    ax.axvline(mu - c, color=MUTED, lw=1.0, ls=":")
    ax.axvline(mu + c, color=MUTED, lw=1.0, ls=":")
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(0, 9.5)
    ax.set_xlabel("$x$")
    ax.set_xticks([mu - c, mu, mu + c])
    ax.set_xticklabels(["$\\mu-c$", "$\\mu$", "$\\mu+c$"])
    ax.set_title("(b)  $g(x)\\leq(x-\\mu)^2$ everywhere")
    ax.legend(loc="upper center", fontsize=9)
    ax.text(0.0, 4.6, "$\\sigma^2=\\mathbb{E}[(X-\\mu)^2]\\ \\geq\\ \\mathbb{E}[g(X)]"
            "=c^2\\mathbf{P}(|X-\\mu|\\geq c)$",
            ha="center", fontsize=9.5, color=INK,
            bbox=dict(boxstyle="round,pad=0.35", fc="#fdf2ec", ec=ORANGE, lw=1.0))
    fig.tight_layout()
    save(fig, "chebyshev")


# ===========================================================================
# Fig 1.3 - decision flowchart: which bound / approximation
# ===========================================================================
def _box(ax, x, y, w, h, text, fc=BOX_FC, ec=BLUE, fs=9.5, tc=INK):
    ax.add_patch(mp.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                   boxstyle="round,pad=0.02,rounding_size=0.10",
                                   fc=fc, ec=ec, lw=1.5, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, zorder=5)


def _arrow(ax, x1, y1, x2, y2, label=None, lab_dx=0.0, lab_dy=0.0, fs=9,
           ha="center"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4,
                                shrinkA=2, shrinkB=2))
    if label:
        ax.text((x1 + x2) / 2 + lab_dx, (y1 + y2) / 2 + lab_dy, label,
                fontsize=fs, color=MUTED, ha=ha, va="center", zorder=6,
                bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none"))


def fig_bounds():
    fig, ax = plt.subplots(figsize=(10.2, 6.4))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.grid(False)

    _box(ax, 5.1, 6.00, 6.4, 0.62,
         "Want $\\mathbf{P}(X\\geq a)$ or $\\mathbf{P}(|X-\\mu|\\geq c)$",
         fc="#f4f2ea", ec=AXIS_C)

    _box(ax, 5.15, 5.05, 4.3, 0.58, "Is the full distribution of $X$ known\n"
         "and the sum/integral doable?", fc="#fdf6e3", ec=GOLD)
    _arrow(ax, 5.1, 5.69, 5.1, 5.34)

    _box(ax, 1.35, 5.05, 2.3, 0.58, "compute it EXACTLY\n(no bound needed)",
         fc="#e8f6ef", ec=DGREEN)
    _arrow(ax, 3.00, 5.05, 2.50, 5.05, "yes", lab_dy=0.0)

    _box(ax, 5.15, 4.05, 4.3, 0.58, "Is $X$ a sample mean $M_n$ of many i.i.d.\n"
         "terms, and do you want a NUMBER?", fc="#fdf6e3", ec=GOLD)
    _arrow(ax, 5.1, 4.76, 5.1, 4.34, "no", lab_dx=0.28)

    _box(ax, 8.95, 4.05, 2.3, 0.58, "central limit theorem\n(\u00a72) \u2014 approximation",
         fc="#e8f6ef", ec=DGREEN)
    _arrow(ax, 7.30, 4.05, 7.80, 4.05, "yes", lab_dy=0.0)

    _box(ax, 5.15, 3.05, 4.3, 0.58, "Do you know $\\sigma^2$ (or a bound on it)?",
         fc="#fdf6e3", ec=GOLD)
    _arrow(ax, 5.1, 3.76, 5.1, 3.34, "no", lab_dx=0.28)

    _box(ax, 1.35, 3.05, 2.3, 0.72,
         "$X\\geq 0$ only:  MARKOV\n$\\mathbf{P}(X\\geq a)\\leq \\mathbb{E}[X]/a$",
         fc="#fdeaea", ec=RED)
    _arrow(ax, 3.00, 3.05, 2.50, 3.05, "no", lab_dy=0.0)

    _box(ax, 5.1, 1.95, 5.6, 0.72,
         "CHEBYSHEV:  $\\mathbf{P}(|X-\\mu|\\geq c)\\leq \\sigma^2/c^2$,"
         "  equivalently  $\\mathbf{P}(|X-\\mu|\\geq k\\sigma)\\leq 1/k^2$",
         fc="#fdeaea", ec=RED)
    _arrow(ax, 5.1, 2.76, 5.1, 2.31, "yes", lab_dx=0.28)

    _box(ax, 5.1, 0.90, 6.6, 0.62,
         "only the range $[a,b]$ known?  use $\\sigma^2\\leq (b-a)^2/4$"
         "   \u00b7   $X$ a sample mean?  use $\\sigma^2_{M_n}=\\sigma^2/n$",
         fc="#f4f2ea", ec=AXIS_C, fs=9)
    _arrow(ax, 5.1, 1.59, 5.1, 1.21)

    ax.text(5.1, 0.22, "Bounds are always valid but often loose; the CLT is an "
            "approximation but usually far more accurate.",
            ha="center", fontsize=9, color=MUTED, style="italic")
    fig.tight_layout()
    save(fig, "bounds")


# ===========================================================================
# Fig 1.4 - concentration of M_n (Bernoulli(1/2))
# ===========================================================================
def fig_concentration():
    p, eps = 0.5, 0.1
    ns = [4, 16, 64, 256]
    fig, axes = plt.subplots(1, 4, figsize=(11.4, 3.0), sharey=False)
    for ax, n in zip(axes, ns):
        k = np.arange(0, n + 1)
        pmf = stats.binom.pmf(k, n, p)
        m = k / n
        ax.vlines(m, 0, pmf, color=BLUE, lw=1.6 if n <= 16 else 0.9)
        if n <= 16:
            ax.plot(m, pmf, "o", color=BLUE, ms=4.5)
        ax.axvspan(p - eps, p + eps, color=GREEN, alpha=0.16, lw=0)
        ax.axvline(p, color=MUTED, ls="--", lw=1.1)
        out = float(pmf[np.abs(m - p) >= eps - 1e-12].sum())
        cheb = min(1.0, 0.25 / (n * eps ** 2))
        ax.set_xlim(-0.03, 1.03)
        ax.set_ylim(0, max(pmf) * 1.42)
        ax.set_title(f"$n={n}$", fontsize=10.5)
        ax.set_xlabel("value of $M_n$")
        ax.set_xticks([0, 0.5, 1])
        ax.text(0.015, max(pmf) * 1.40,
                f"exact {out:.3g}\nCheb. {cheb:.3g}", ha="left", va="top",
                fontsize=8.6, color=INK,
                bbox=dict(boxstyle="round,pad=0.26", fc="white", ec=GRID_C, lw=0.9))
    axes[0].set_ylabel("$p_{M_n}(m)$")
    fig.suptitle("PMF of $M_n=(X_1+\\cdots+X_n)/n$ for i.i.d. Bernoulli$(1/2)$;"
                 " green band $=[\\mu-0.1,\\ \\mu+0.1]$", fontsize=10.5, y=1.045)
    fig.tight_layout()
    save(fig, "concentration")


# ===========================================================================
# Fig 1.5 - the pollster accuracy curve
# ===========================================================================
def fig_pollster():
    eps = 0.01
    n = np.unique(np.round(np.logspace(3, 6, 260)).astype(int))
    cheb = np.minimum(1.0, 1.0 / (4 * n * eps ** 2))
    clt = 2 * stats.norm.sf(2 * eps * np.sqrt(n))          # f = 1/2, sigma = 1/2
    exact = np.array([2 * stats.binom.cdf(int(np.floor(m * (0.5 - eps))), int(m), 0.5)
                      for m in n])

    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.plot(n, cheb, color=RED, lw=2.2, label="Chebyshev bound  $1/(4n\\epsilon^2)$")
    ax.plot(n, exact, color=DGREEN, lw=3.4,
            label="exact binomial value, $f=1/2$")
    ax.plot(n, clt, color=BLUE, lw=1.5, ls=(0, (5, 4)), zorder=5,
            label="normal (CLT) approximation (lies on top)")
    ax.axhline(0.05, color=MUTED, lw=1.2, ls=":")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(1e-7, 1.6)
    ax.set_xlim(1e3, 1e6)
    ax.set_xlabel("sample size $n$  (log scale)")
    ax.set_ylabel("$\\mathbf{P}(|M_n-f|\\geq 0.01)$  (log scale)")
    ax.set_title("Pollster: $\\epsilon=0.01$ accuracy, target failure probability $0.05$")

    ax.plot([50000], [0.05], "o", color=RED, ms=8, zorder=6)
    ax.annotate("Chebyshev needs\n$n=50{,}000$", xy=(50000, 0.05),
                xytext=(1.1e5, 0.30), fontsize=9.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    ax.plot([9604], [0.05], "o", color=BLUE, ms=8, zorder=6)
    ax.annotate("CLT needs only\n$n=9{,}604$", xy=(9604, 0.05),
                xytext=(1.15e3, 2.5e-3), fontsize=9.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    ax.annotate("true value at $n=50{,}000$\nis $7.9\\times 10^{-6}$",
                xy=(50000, 7.9026e-06), xytext=(1.15e5, 1.6e-6), fontsize=9.5,
                color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    ax.text(9.2e5, 0.062, "target $0.05$", fontsize=9, color=MUTED, ha="right")
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    save(fig, "pollster")


# ===========================================================================
# Fig 1.6 - convergence in probability without convergence of E or of E[.^2]
# ===========================================================================
def fig_convergence():
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.7))

    ax = axes[0]
    for j, (n, col) in enumerate([(4, BLUE), (10, ORANGE), (25, DGREEN)]):
        ax.vlines([0 + 0.35 * j], 0, 1 - 1 / n, color=col, lw=2.4)
        ax.plot([0 + 0.35 * j], [1 - 1 / n], "o", color=col, ms=6)
        ax.vlines([n], 0, 1 / n, color=col, lw=2.4)
        ax.plot([n], [1 / n], "o", color=col, ms=6,
                label=f"$n={n}$:  mass $1/n={1/n:.2f}$ at $y=n$")
    ax.set_xlim(-1.6, 28)
    ax.set_ylim(0, 1.22)
    ax.set_xlabel("$y$")
    ax.set_ylabel("$p_{Y_n}(y)$")
    ax.set_title("(a)  $Y_n=0$ w.p. $1-1/n$,  $Y_n=n$ w.p. $1/n$")
    ax.legend(loc="upper center", fontsize=8.6)
    ax.text(3.0, 0.62, "stems at $y=0$ nudged apart\nso the three are visible",
            fontsize=8.4, color=MUTED)

    ax = axes[1]
    ns = np.arange(2, 201)
    ax.plot(ns, 1 / ns, color=DGREEN, lw=2.2,
            label="$\\mathbf{P}(|Y_n|\\geq\\epsilon)=1/n\\ \\to 0$")
    ax.plot(ns, np.ones_like(ns, dtype=float), color=ORANGE, lw=2.2,
            label="$\\mathbb{E}[Y_n]=1$  (never moves)")
    ax.plot(ns, ns.astype(float), color=RED, lw=2.2,
            label="$\\mathbb{E}[Y_n^2]=n\\ \\to\\infty$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(2, 200)
    ax.set_ylim(3e-3, 4e2)
    ax.set_xlabel("$n$  (log scale)")
    ax.set_title("(b)  converges in probability to 0, and nothing else does")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, "convergence")


for f in (fig_markov, fig_chebyshev, fig_bounds, fig_concentration,
          fig_pollster, fig_convergence):
    f()
print("done")
