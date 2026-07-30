# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G6 section 2 — the Central Limit Theorem (L20 + rec21).

Run:  uv run computes/g6_s2_figs.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
from mpl_style import setup, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
import matplotlib.patches as mp            # noqa: E402
import numpy as np                          # noqa: E402
from scipy import stats                     # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL
Phi = stats.norm.cdf
phi = stats.norm.pdf


def save(fig, name):
    p = IMG / f"g6_s2_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ===================================================== Fig 1: standardization
def fig_standardize():
    n, p = 36, 0.5
    k = np.arange(0, n + 1)
    pmf = stats.binom.pmf(k, n, p)
    mu, sd = n * p, math.sqrt(n * p * (1 - p))

    fig, axes = plt.subplots(1, 3, figsize=(11.6, 3.5))

    def stems(ax, xs, hs, xlim, title, dens=None, ylab=None):
        ax.vlines(xs, 0, hs, color=BLUE, lw=1.6, alpha=0.9)
        ax.plot(xs, hs, "o", color=BLUE, ms=3.2)
        if dens is not None:
            g = np.linspace(xlim[0], xlim[1], 500)
            ax.plot(g, dens(g), color=ORANGE, lw=2.0, zorder=3)
        ax.set_xlim(*xlim)
        ax.set_ylim(0, max(hs) * 1.32)
        ax.set_title(title, color=INK)
        if ylab:
            ax.set_ylabel(ylab)

    # (a) raw sum
    stems(axes[0], k, pmf, (5, 31),
          "(a)  $S_{36}$: mean 18, sd 3",
          dens=lambda x: stats.norm.pdf(x, mu, sd), ylab="probability / density")
    axes[0].set_xlabel("$s$")
    axes[0].axvline(mu, color=MUTED, lw=1.0, ls="--")
    axes[0].text(18.9, 0.155, "$n\\mathbb{E}[X]=18$", color=MUTED, fontsize=9)

    # (b) centred
    stems(axes[1], k - mu, pmf, (-13, 13),
          "(b)  $S_{36}-18$: mean 0, sd 3",
          dens=lambda x: stats.norm.pdf(x, 0, sd))
    axes[1].set_xlabel("$s-n\\mathbb{E}[X]$")
    axes[1].axvline(0, color=MUTED, lw=1.0, ls="--")

    # (c) standardized
    z = (k - mu) / sd
    dens_h = pmf * sd                      # heights scaled so the envelope is N(0,1)
    stems(axes[2], z, dens_h, (-4.4, 4.4),
          "(c)  $Z_{36}=(S_{36}-18)/3$",
          dens=lambda x: phi(x))
    axes[2].set_xlabel("$z$")
    axes[2].axvline(0, color=MUTED, lw=1.0, ls="--")
    axes[2].text(1.05, 0.365, "$N(0,1)$", color=ORANGE, fontsize=10)

    fig.subplots_adjust(wspace=0.30, top=0.80, bottom=0.19)
    fig.text(0.345, 0.955, "$-\\,n\\mathbb{E}[X]$", ha="center", fontsize=10,
             color=DGREEN)
    fig.text(0.675, 0.955, "$\\div\\,\\sqrt{n}\\,\\sigma$", ha="center", fontsize=10,
             color=DGREEN)
    fig.patches.append(mp.FancyArrowPatch((0.305, 0.94), (0.385, 0.94),
                       transform=fig.transFigure, arrowstyle="-|>",
                       mutation_scale=13, color=DGREEN, lw=1.4))
    fig.patches.append(mp.FancyArrowPatch((0.635, 0.94), (0.715, 0.94),
                       transform=fig.transFigure, arrowstyle="-|>",
                       mutation_scale=13, color=DGREEN, lw=1.4))
    save(fig, "standardize")


# ================================================ Fig 2: convergence panels
def conv_lattice(vals, probs, n):
    """PMF of the sum of n iid lattice rvs, returned standardized."""
    vals = np.asarray(vals, float)
    probs = np.asarray(probs, float)
    lo, hi = int(vals.min()), int(vals.max())
    base = np.zeros(hi - lo + 1)
    for v, q in zip(vals, probs):
        base[int(v) - lo] += q
    f = base.copy()
    for _ in range(n - 1):
        f = np.convolve(f, base)
    supp = np.arange(n * lo, n * hi + 1, dtype=float)
    mu = float((vals * probs).sum())
    var = float((vals ** 2 * probs).sum() - mu ** 2)
    sd = math.sqrt(n * var)
    return (supp - n * mu) / sd, f * sd, sd


def fig_converge():
    unif_v, unif_p = np.arange(1, 9), np.ones(8) / 8
    w = np.array([0.5 ** j for j in range(1, 7)])
    skew_v, skew_p = np.arange(1, 7), w / w.sum()

    ns = [1, 2, 4, 32]
    fig, axes = plt.subplots(2, 4, figsize=(11.8, 5.4))
    g = np.linspace(-4.2, 4.2, 500)

    for row, (vals, probs, name) in enumerate([
            (unif_v, unif_p, "symmetric base: uniform on $\\{1,\\dots,8\\}$"),
            (skew_v, skew_p, "skewed base: $p_x\\propto 2^{-x}$ on $\\{1,\\dots,6\\}$")]):
        for col, n in enumerate(ns):
            ax = axes[row, col]
            z, h, sd = conv_lattice(vals, probs, n)
            m = (z >= -4.2) & (z <= 4.2)
            ax.vlines(z[m], 0, h[m], color=BLUE, lw=1.1 if n > 4 else 1.8, alpha=0.9)
            if n <= 4:
                ax.plot(z[m], h[m], "o", color=BLUE, ms=3.0)
            ax.plot(g, phi(g), color=ORANGE, lw=1.8, zorder=3)
            ax.set_xlim(-4.2, 4.2)
            ax.set_ylim(0, 0.56)
            ax.set_title(f"$n={n}$", fontsize=10, color=INK)
            if col == 0:
                ax.set_ylabel("scaled PMF")
            if row == 1:
                ax.set_xlabel("$z$")

    axes[0, 3].text(1.15, 0.42, "$N(0,1)$", color=ORANGE, fontsize=9.5)
    fig.subplots_adjust(hspace=0.62, wspace=0.24, top=0.855, bottom=0.09)
    fig.text(0.085, 0.955, "symmetric base: uniform on $\\{1,\\dots,8\\}$",
             fontsize=10.5, color=DGREEN, ha="left", va="center")
    fig.text(0.085, 0.475, "skewed base: $p_x\\propto 2^{-x}$ on $\\{1,\\dots,6\\}$",
             fontsize=10.5, color=DGREEN, ha="left", va="center")
    save(fig, "converge")


# ============================================ Fig 3: the CDF is what converges
def fig_cdf():
    n, p = 16, 0.5
    k = np.arange(0, n + 1)
    pmf = stats.binom.pmf(k, n, p)
    mu, sd = n * p, math.sqrt(n * p * (1 - p))
    z = (k - mu) / sd
    cdf = np.cumsum(pmf)

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))

    # (a) PMF vs pdf — heights shrink to 0, no pointwise convergence
    ax = axes[0]
    for nn, c, lbl in [(16, BLUE, "$n=16$"), (64, GREEN, "$n=64$")]:
        kk = np.arange(0, nn + 1)
        pm = stats.binom.pmf(kk, nn, 0.5)
        zz = (kk - nn * 0.5) / math.sqrt(nn * 0.25)
        m = np.abs(zz) <= 4
        ax.vlines(zz[m], 0, pm[m], color=c, lw=1.4, alpha=0.85)
        ax.plot(zz[m], pm[m], "o", color=c, ms=3.0, label=lbl + " PMF of $Z_n$")
    g = np.linspace(-4, 4, 400)
    ax.plot(g, phi(g), color=ORANGE, lw=2.0, label="$N(0,1)$ density")
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(0, 0.44)
    ax.set_xlabel("$z$")
    ax.set_ylabel("probability / density")
    ax.set_title("(a)  PMF values shrink to 0 — no PMF convergence", fontsize=10)
    ax.legend(loc="upper left", fontsize=8.5)

    # (b) CDF staircase vs Phi
    ax = axes[1]
    zs = np.repeat(z, 2)[1:]
    cs = np.repeat(np.concatenate(([0.0], cdf)), 2)[1:-1]
    ax.step(np.concatenate(([-4.2], z, [4.2])),
            np.concatenate(([0.0], cdf, [1.0])), where="post",
            color=BLUE, lw=1.8, label="CDF of $Z_{16}$")
    g = np.linspace(-4.2, 4.2, 500)
    ax.plot(g, Phi(g), color=ORANGE, lw=2.0, label="$\\Phi(z)$")
    # max gap marker
    gaps_r = np.abs(cdf - Phi(z))
    gaps_l = np.abs(np.concatenate(([0.0], cdf[:-1])) - Phi(z))
    i_r, i_l = int(np.argmax(gaps_r)), int(np.argmax(gaps_l))
    if gaps_r[i_r] >= gaps_l[i_l]:
        zg, y1, y2, gv = z[i_r], float(Phi(z[i_r])), float(cdf[i_r]), gaps_r[i_r]
    else:
        zg, y1, y2, gv = (z[i_l], float(Phi(z[i_l])),
                          float(np.concatenate(([0.0], cdf[:-1]))[i_l]), gaps_l[i_l])
    ax.annotate("", xy=(zg, y1), xytext=(zg, y2),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6))
    ax.annotate(f"max gap over all $z$\n$= {gv:.4f}$", xy=(zg, (y1 + y2) / 2),
                xytext=(zg + 1.05, 0.235), color=RED, fontsize=9, va="center",
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.1))
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-0.03, 1.06)
    ax.set_xlabel("$z$")
    ax.set_ylabel("$\\mathbf{P}(Z_n\\leq z)$")
    ax.set_title("(b)  the CDF does converge, uniformly", fontsize=10)
    ax.legend(loc="upper left", fontsize=8.5)

    fig.subplots_adjust(wspace=0.28, top=0.88, bottom=0.15)
    save(fig, "cdf")


# =================================================== Fig 4: the 1/2 correction
def fig_halfcorr():
    n, p = 36, 0.5
    mu, sd = n * p, math.sqrt(n * p * (1 - p))
    k = np.arange(11, 27)
    pmf = stats.binom.pmf(k, n, p)
    g = np.linspace(11, 27, 800)
    dens = stats.norm.pdf(g, mu, sd)

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.0))

    # (a) a single bar vs the strip [k-1/2, k+1/2]
    ax = axes[0]
    ax.bar(k, pmf, width=1.0, color=BLUE, alpha=0.28, edgecolor=BLUE, lw=1.0)
    ax.plot(g, dens, color=ORANGE, lw=2.2, zorder=4)
    strip = (g >= 18.5) & (g <= 19.5)
    ax.fill_between(g[strip], 0, dens[strip], color=ORANGE, alpha=0.55, zorder=3)
    ax.vlines([18.5, 19.5], 0, 0.145, color=RED, lw=1.4, ls="--", zorder=5)
    ax.set_xlim(13.2, 24.8)
    ax.set_ylim(0, 0.175)
    ax.set_xticks([14, 16, 18, 19, 20, 22, 24])
    ax.set_xlabel("$s$")
    ax.set_ylabel("probability / density")
    ax.set_title("(a)  $\\mathbf{P}(S_n=19)\\approx$ area over $[18.5,\\,19.5]$",
                 fontsize=10)
    ax.annotate("bar at 19:\nexact 0.125110", xy=(19, 0.1251), xytext=(21.4, 0.152),
                fontsize=8.8, color=BLUE,
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.1))
    ax.annotate("shaded strip:\n0.125279", xy=(19.05, 0.055), xytext=(14.0, 0.036),
                fontsize=8.8, color="#8a3d16",
                arrowprops=dict(arrowstyle="-|>", color="#8a3d16", lw=1.1))

    # (b) cut at 21 vs 21.5 for the CDF
    ax = axes[1]
    ax.bar(k, pmf, width=1.0, color=BLUE, alpha=0.28, edgecolor=BLUE, lw=1.0)
    ax.plot(g, dens, color=ORANGE, lw=2.2, zorder=4)
    left = g <= 21.0
    sliver = (g >= 21.0) & (g <= 21.5)
    ax.fill_between(g[left], 0, dens[left], color=ORANGE, alpha=0.16, zorder=2)
    ax.fill_between(g[sliver], 0, dens[sliver], color=RED, alpha=0.55, zorder=3)
    ax.vlines(21.0, 0, 0.135, color=MUTED, lw=1.6, ls=":", zorder=5)
    ax.vlines(21.5, 0, 0.135, color=RED, lw=1.6, ls="--", zorder=5)
    ax.set_xlim(13.2, 24.8)
    ax.set_ylim(0, 0.195)
    ax.set_xticks([14, 16, 18, 20, 21, 22, 24])
    ax.set_xlabel("$s$")
    ax.set_title("(b)  cutting at 21 throws away half of the bar at 21", fontsize=10)
    ax.text(13.4, 0.183, "cut at 21:      $\\Phi(1)=0.841345$", color=MUTED,
            fontsize=8.8, ha="left", va="top")
    ax.text(13.4, 0.170, "cut at 21.5:  $\\Phi(1.1667)=0.878327$", color=RED,
            fontsize=8.8, ha="left", va="top")
    ax.text(13.4, 0.157, "exact:          $\\mathbf{P}(S_n\\leq 21)=0.878508$",
            color=INK, fontsize=8.8, ha="left", va="top")
    ax.annotate("missing sliver\n$=0.036982$",
                xy=(21.28, 0.035), xytext=(22.3, 0.098), fontsize=8.8,
                color="#8a1f1f", ha="left",
                arrowprops=dict(arrowstyle="-|>", color="#8a1f1f", lw=1.1))

    fig.subplots_adjust(wspace=0.20, top=0.88, bottom=0.14)
    save(fig, "halfcorr")


# ================================================== Fig 5: which-tool flowchart
def fig_flow():
    fig, ax = plt.subplots(figsize=(11.0, 8.4))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 10.2)
    ax.axis("off")
    ax.grid(False)

    def box(xy, w, h, text, fc="#ffffff", ec=INK, fs=9.4, tc=INK, style="round,pad=0.03"):
        x, y = xy
        ax.add_patch(mp.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                       boxstyle=style, facecolor=fc, edgecolor=ec,
                                       lw=1.4, zorder=3))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc,
                zorder=4, linespacing=1.35)

    def diamond(xy, w, h, text, fs=9.2):
        x, y = xy
        ax.add_patch(mp.Polygon([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2],
                                 [x - w / 2, y]], closed=True, facecolor="#fdf6e6",
                                edgecolor=GOLD, lw=1.5, zorder=3))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
                zorder=4, linespacing=1.35)

    def arrow(a, b, label="", side="right", color=AXIS_C):
        ax.add_patch(mp.FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13,
                                        color=color, lw=1.4, zorder=2,
                                        shrinkA=2, shrinkB=2))
        if label:
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            dx = 0.30 if side == "right" else -0.30
            ax.text(mx + dx, my + 0.10, label, fontsize=8.6, color=DGREEN,
                    ha="left" if side == "right" else "right", va="center")

    ax.text(0.05, 9.95, "Which tool for the tail probability "
            "$\\mathbf{P}(S_n\\geq a)$?", fontsize=12.5,
            color=INK, ha="left", va="center", fontweight="600")

    # start
    box((5.6, 9.05), 8.4, 0.62,
        "$S_n = X_1+\\dots+X_n$ with $X_i$ i.i.d., mean $\\mathbb{E}[X]$, "
        "variance $\\sigma^2$", fc="#eef4fc", ec=BLUE, fs=10)

    # Q1
    diamond((3.4, 7.75), 4.8, 1.25,
            "Do you know the distribution of $X_i$\nexactly, and is $n$ small?")
    arrow((3.4, 8.74), (3.4, 8.375))
    box((9.1, 7.75), 3.4, 0.85, "compute it EXACTLY\n(convolution, binomial table)",
        fc="#eef8f3", ec=GREEN, fs=9.0)
    arrow((5.85, 7.75), (7.35, 7.75), "yes", side="right")

    # Q2
    diamond((3.4, 5.90), 4.8, 1.25,
            "Is $n$ large — or the $X_i$\nclose to symmetric?")
    arrow((3.4, 7.12), (3.4, 6.55), "no", side="right")

    box((8.7, 5.90), 4.4, 1.25,
        "CLT / normal approximation\n"
        "$z = (a - n\\mathbb{E}[X]) / (\\sqrt{n}\\,\\sigma)$\n"
        "$\\mathbf{P}(S_n\\geq a)\\approx 1-\\Phi(z)$",
        fc="#fdf0e9", ec=ORANGE, fs=9.4)
    arrow((5.85, 5.90), (6.45, 5.90))
    ax.text(6.15, 6.16, "yes", fontsize=8.6, color=DGREEN, ha="center")

    # Q3 (bounds branch)
    diamond((3.4, 3.85), 4.4, 1.20, "Do you also know $\\sigma^2$?")
    arrow((3.4, 5.27), (3.4, 4.48), "no", side="right")

    box((1.75, 1.95), 3.1, 0.95, "MARKOV (needs $X_i\\geq 0$)\n"
        "$\\mathbf{P}(S_n\\geq a)\\leq \\mathbb{E}[S_n]/a$",
        fc="#f7eef2", ec=PINK, fs=8.6)
    box((5.05, 1.95), 3.0, 0.95, "CHEBYSHEV\n"
        "$\\leq \\sigma^2_{S_n}/(a-\\mathbb{E}[S_n])^2$",
        fc="#f7eef2", ec=PINK, fs=8.6)
    arrow((2.55, 3.42), (1.75, 2.46), "no", side="left")
    arrow((4.25, 3.42), (5.05, 2.46), "yes", side="right")

    # Q4 (correction)
    diamond((8.7, 3.85), 3.9, 1.15, "Is $S_n$ integer-valued?", fs=9.4)
    arrow((8.7, 5.26), (8.7, 4.45))
    box((9.15, 1.95), 3.9, 0.95,
        "de Moivre–Laplace:\nreplace $a$ by $a-0.5$ in $z$",
        fc="#fdf0e9", ec=ORANGE, fs=9.0)
    arrow((8.7, 3.26), (9.05, 2.45), "yes", side="right")

    ax.text(0.05, 0.75,
            "Markov and Chebyshev are guaranteed upper BOUNDS but usually loose; "
            "the CLT is an APPROXIMATION — sharp, but with no error guarantee.",
            fontsize=9.4, color=MUTED, ha="left", va="center")
    save(fig, "flow")


# ================================================ Fig 6: bound comparison bars
def fig_bounds():
    labels = ["Markov\n$\\mathbb{E}[X]/7$",
              "Chebyshev\n(+ symmetry)",
              "Cantelli\n(one-sided)",
              "CLT\n$1-\\Phi(2.1909)$",
              "EXACT\n(Irwin–Hall)"]
    vals = [5 / 7, 5 / 48, (5 / 6) / ((5 / 6) + 4), 1 - float(Phi(2.190890)),
            24427 / 1814400]
    cols = [PINK, PURPLE, GOLD, ORANGE, BLUE]

    fig, ax = plt.subplots(figsize=(9.4, 4.0))
    y = np.arange(len(vals))[::-1]
    ax.barh(y, vals, height=0.58, color=cols, alpha=0.88)
    for yy, v in zip(y, vals):
        ax.text(v * 1.15, yy, f"{v:.6f}", va="center", fontsize=9.5, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xscale("log")
    ax.set_xlim(0.006, 4.0)
    ax.set_xlabel("upper bound / estimate for $\\mathbf{P}(X_1+\\dots+X_{10}\\geq 7)$"
                  "   (log scale)")
    ax.axvline(24427 / 1814400, color=BLUE, lw=1.2, ls="--", alpha=0.7)
    ax.set_title("rec21 P1: ten uniforms on $[0,1]$ — three bounds, one approximation, one exact answer",
                 fontsize=10.5)
    ax.grid(axis="x")
    ax.set_axisbelow(True)
    fig.subplots_adjust(left=0.20, right=0.97, top=0.87, bottom=0.19)
    save(fig, "bounds")


if __name__ == "__main__":
    fig_standardize()
    fig_converge()
    fig_cdf()
    fig_halfcorr()
    fig_flow()
    fig_bounds()
    print("all figures written")
