# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G7 section 1 - estimators, bias, consistency, confidence intervals.

Run:  uv run computes/g7_s1_figs.py
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
from scipy import stats  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)

BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL
BOX_FC = "#eaf2fd"
BOX_FC2 = "#fdf0e6"
BOX_FC3 = "#e8f7f1"


def save(fig, name):
    p = IMG / f"g7_s1_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


def box(ax, x, y, w, h, text, fc=BOX_FC, ec=BLUE, fs=9.2, lw=1.3, style="round,pad=0.02"):
    ax.add_patch(mp.FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=style,
                                   fc=fc, ec=ec, lw=lw, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK, zorder=3)


def arrow(ax, x0, y0, x1, y1, color=MUTED, lw=1.4, rad=0.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=1,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0,
                                connectionstyle=f"arc3,rad={rad}"))


# ===========================================================================
# Fig 1.1 - MSE = bias^2 + variance
# ===========================================================================
def fig_msedecomp():
    n, v = 10, 1.0
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.9))

    # ---- panel (a): the two sampling distributions at theta = 3 -----------
    ax = axes[0]
    th = 3.0
    sd_M = np.sqrt(v / n)
    sd_T = np.sqrt(n * v) / (n + 1)
    mu_T = n * th / (n + 1)
    xs = np.linspace(th - 1.5, th + 1.5, 800)
    ax.plot(xs, stats.norm.pdf(xs, th, sd_M), color=BLUE, lw=2.0,
            label=r"$M_n=S_n/n$  (unbiased)")
    ax.plot(xs, stats.norm.pdf(xs, mu_T, sd_T), color=ORANGE, lw=2.0,
            label=r"$T_n=S_n/(n{+}1)$  (biased)")
    ax.axvline(th, color=INK, lw=1.3, ls="--")
    ax.text(th + 0.04, 1.80, r"true $\theta=3$", fontsize=9, color=INK, ha="left")
    # bias arrow
    ax.annotate("", xy=(th, 0.30), xytext=(mu_T, 0.30),
                arrowprops=dict(arrowstyle="<|-|>", color=ORANGE, lw=1.6))
    ax.text((th + mu_T) / 2, 0.36, "bias\n$-0.273$", fontsize=8.6, color=ORANGE,
            ha="center", va="bottom")
    # spread arrows
    ax.annotate("", xy=(th - sd_M, 1.45), xytext=(th + sd_M, 1.45),
                arrowprops=dict(arrowstyle="<|-|>", color=BLUE, lw=1.3))
    ax.text(th, 1.50, r"$\pm\sigma_{M}=0.316$", fontsize=8.4, color=BLUE,
            ha="center", va="bottom")
    ax.set_xlim(th - 1.5, th + 1.5)
    ax.set_ylim(0, 2.05)
    ax.set_xlabel("value of the estimator")
    ax.set_ylabel("sampling density")
    ax.set_title("(a) bias = shift of centre,  variance = width", loc="left")
    ax.legend(loc="upper left", fontsize=8.4)

    # ---- panel (b): MSE curves vs theta ----------------------------------
    ax = axes[1]
    ths = np.linspace(0, 3.0, 400)
    mse_M = np.full_like(ths, v / n)
    var_T = n * v / (n + 1) ** 2
    bias2_T = (ths / (n + 1)) ** 2
    mse_T = var_T + bias2_T
    ax.fill_between(ths, 0, var_T, color=ORANGE, alpha=0.20, lw=0,
                    label=r"$\operatorname{var}(T_n)=0.0826$")
    ax.fill_between(ths, var_T, mse_T, color=RED, alpha=0.22, lw=0,
                    label=r"$\mathrm{bias}^2(T_n)=\theta^2/121$")
    ax.plot(ths, mse_T, color=ORANGE, lw=2.2, label=r"$\mathrm{MSE}(T_n)$")
    ax.plot(ths, mse_M, color=BLUE, lw=2.2, label=r"$\mathrm{MSE}(M_n)=v/n=0.1$")
    cross = np.sqrt(v * (2 * n + 1) / n)
    ax.axvline(cross, color=MUTED, lw=1.2, ls="--")
    ax.plot([cross], [v / n], "o", color=INK, ms=5, zorder=5)
    ax.annotate("crossover at\n" r"$|\theta|=\sqrt{v(2n{+}1)/n}=1.449$",
                xy=(cross, v / n), xytext=(cross - 0.10, 0.038),
                fontsize=8.2, color=INK, ha="right", va="bottom",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=1.0))
    ax.text(2.45, 0.030, r"$M_n$ wins", fontsize=9, color=DGREEN, ha="center")
    ax.text(2.45, 0.014, r"($T_n$ wins to the left)", fontsize=7.6, color=DGREEN,
            ha="center")
    ax.set_xlim(0, 3.0)
    ax.set_ylim(0, 0.205)
    ax.set_xlabel(r"true parameter $\theta$")
    ax.set_ylabel("mean squared error")
    ax.set_title(r"(b) $\mathrm{MSE}=\mathrm{bias}^2+\mathrm{variance}$,  $n=10,\ v=1$", loc="left")
    ax.legend(loc="upper left", fontsize=8.0, ncol=1)

    fig.tight_layout()
    save(fig, "msedecomp")


# ===========================================================================
# Fig 1.2 - 100 confidence intervals, coverage picture
# ===========================================================================
def fig_coverage():
    mu, sig, n, reps = 10.0, 2.0, 25, 100
    rng = np.random.default_rng(2010)
    samp = rng.normal(mu, sig, size=(reps, n))
    mn = samp.mean(axis=1)
    hw = 1.96 * sig / np.sqrt(n)
    lo, hi = mn - hw, mn + hw
    hit = (lo <= mu) & (mu <= hi)

    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    for i in range(reps):
        c = BLUE if hit[i] else RED
        a = 0.75 if hit[i] else 1.0
        ax.plot([lo[i], hi[i]], [i, i], color=c, lw=1.5, alpha=a, solid_capstyle="butt")
        ax.plot([mn[i]], [i], "o", color=c, ms=2.8, alpha=a)
    ax.axvline(mu, color=INK, lw=1.6)
    ax.text(mu + 0.05, reps + 1.5, r"true $\mu=10$ (fixed, not random)",
            fontsize=9.5, color=INK, ha="left", va="bottom")
    ax.set_xlim(8.3, 11.75)
    ax.set_ylim(-2, reps + 20)
    ax.set_yticks([0, 25, 50, 75, 99])
    ax.set_yticklabels(["1", "26", "51", "76", "100"])
    ax.set_xlabel("value")
    ax.set_ylabel("replication number")
    ax.set_title(r"100 independent 95% CIs, $M_n\pm 1.96\sigma/\sqrt{n}$"
                 "  ($n=25$, $\\sigma=2$, half-width $0.784$)", loc="left")
    ax.grid(axis="y", visible=False)
    ax.text(8.36, reps + 15.5, "96 intervals cover the true $\\mu$  (blue)",
            fontsize=9.0, color=BLUE, ha="left", va="center", zorder=7)
    ax.text(8.36, reps + 8.5, "4 intervals miss it entirely  (red)",
            fontsize=9.0, color=RED, ha="left", va="center", zorder=7)
    fig.tight_layout()
    save(fig, "coverage")


# ===========================================================================
# Fig 1.3 - CI construction pipeline
# ===========================================================================
def fig_pipeline():
    fig, ax = plt.subplots(figsize=(10.4, 4.4))
    ax.set_xlim(0, 104)
    ax.set_ylim(0, 44)
    ax.axis("off")
    ax.grid(False)

    W, H = 29, 11
    y1, y2 = 32, 9
    xs = [18, 52, 86]

    box(ax, xs[0], y1, W, H,
        "1.  DATA\n$X_1,\\dots,X_n$ i.i.d.\nmean $\\theta$ (unknown), var $\\sigma^2$",
        fc=BOX_FC, ec=BLUE)
    box(ax, xs[1], y1, W, H,
        "2.  ESTIMATOR\n$\\hat\\Theta_n=M_n=\\frac{X_1+\\cdots+X_n}{n}$\n"
        "$\\mathbb{E}[\\hat\\Theta_n]=\\theta$,  var $=\\sigma^2/n$",
        fc=BOX_FC, ec=BLUE)
    box(ax, xs[2], y1, W, H,
        "3.  STANDARDIZE\n$Z_n=\\dfrac{\\hat\\Theta_n-\\theta}{\\sigma/\\sqrt{n}}$\n"
        "$\\approx N(0,1)$ by the CLT",
        fc=BOX_FC2, ec=ORANGE)
    box(ax, xs[2], y2, W, H,
        "4.  PICK $\\alpha$, INVERT $\\Phi$\nfind $z$ with $\\Phi(z)=1-\\alpha/2$\n"
        "$\\alpha=0.05\\Rightarrow z=1.96$",
        fc=BOX_FC2, ec=ORANGE)
    box(ax, xs[1], y2, W, H,
        "5.  PROBABILITY STATEMENT\n$\\mathbf{P}(|\\hat\\Theta_n-\\theta|\\leq "
        "z\\sigma/\\sqrt{n})\\approx 1-\\alpha$",
        fc=BOX_FC3, ec=DGREEN)
    box(ax, xs[0], y2, W, H,
        "6.  SOLVE FOR $\\theta$\n$[\\,\\hat\\Theta_n-z\\sigma/\\sqrt{n},\\ "
        "\\hat\\Theta_n+z\\sigma/\\sqrt{n}\\,]$",
        fc=BOX_FC3, ec=DGREEN)

    arrow(ax, xs[0] + W / 2, y1, xs[1] - W / 2, y1)
    arrow(ax, xs[1] + W / 2, y1, xs[2] - W / 2, y1)
    arrow(ax, xs[2], y1 - H / 2, xs[2], y2 + H / 2)
    arrow(ax, xs[2] - W / 2, y2, xs[1] + W / 2, y2)
    arrow(ax, xs[1] - W / 2, y2, xs[0] + W / 2, y2)

    ax.text(52, 41.5, "Building a $1-\\alpha$ confidence interval for a mean  (L23 slide 6)",
            ha="center", va="center", fontsize=10.5, color=INK, weight="600")
    ax.text(xs[2] - 1.5, (y1 + y2) / 2, "the only\napproximation\nlives here",
            ha="right", va="center", fontsize=8.2, color=ORANGE)
    ax.text(18, 1.4, "$\\sigma$ unknown?  see Figure 1.4",
            ha="center", va="center", fontsize=8.6, color=MUTED, style="italic")
    fig.tight_layout()
    save(fig, "pipeline")


# ===========================================================================
# Fig 1.4 - which variance do I plug in?
# ===========================================================================
def fig_whichvar():
    fig, ax = plt.subplots(figsize=(10.4, 5.2))
    ax.set_xlim(0, 104)
    ax.set_ylim(0, 55)
    ax.axis("off")
    ax.grid(False)

    box(ax, 52, 47, 34, 7, "Need a CI for a mean $\\theta$", fc="#f2f1ea", ec=AXIS_C)
    box(ax, 52, 37, 30, 7, "Is $\\sigma^2$ known?", fc=BOX_FC, ec=BLUE)
    box(ax, 15, 26, 26, 9,
        "use $\\sigma$ itself\n$\\hat\\Theta_n\\pm z\\sigma/\\sqrt{n}$", fc=BOX_FC3, ec=DGREEN)
    box(ax, 63, 26, 32, 7, "Are the $X_i$ Bernoulli($\\theta$)?", fc=BOX_FC, ec=BLUE)

    box(ax, 88, 13, 28, 11,
        "generic sample variance\n$\\hat S_n^2=\\frac{1}{n-1}\\sum_i (X_i-\\hat\\Theta_n)^2$\n"
        "(unbiased; use $z$ when $n\\geq 50$)", fc=BOX_FC3, ec=DGREEN, fs=8.6)
    box(ax, 52, 13, 26, 11,
        "tightest interval:\nplug in $\\hat\\Theta_n(1-\\hat\\Theta_n)$\n"
        "(needs $n$ large and $\\hat\\Theta_n$\nnot near $0$ or $1$)", fc=BOX_FC3, ec=DGREEN, fs=8.6)
    box(ax, 18, 13, 26, 11,
        "guaranteed coverage /\nsample-size design:\nbound $\\sigma^2\\leq 1/4$\n"
        "$\\Rightarrow\\ \\pm z/(2\\sqrt{n})$", fc=BOX_FC3, ec=DGREEN, fs=8.6)

    arrow(ax, 52, 43.5, 52, 40.5)
    arrow(ax, 37, 37, 15, 37); arrow(ax, 15, 37, 15, 30.5)
    arrow(ax, 67, 37, 79, 37); arrow(ax, 79, 37, 79, 29.5)
    ax.text(80.5, 33, "no", fontsize=9, color=MUTED, ha="left")
    ax.text(26, 38.4, "yes", fontsize=9, color=MUTED, ha="center")

    arrow(ax, 79, 29.5, 79, 29.5)  # (no-op guard)
    arrow(ax, 63, 22.5, 88, 18.5, rad=-0.10)
    arrow(ax, 60, 22.5, 52, 18.5)
    arrow(ax, 52, 22.5, 18, 18.5, rad=0.08)
    ax.text(89, 23.0, "no", fontsize=9, color=MUTED, ha="left")
    ax.text(58.6, 20.6, "yes", fontsize=9, color=MUTED, ha="left", va="center")
    ax.text(30, 21.6, "yes", fontsize=9, color=MUTED, ha="center")

    ax.text(52, 3.2, "At $n=1200$ with $\\hat\\theta_n=0.57$ all three give the same interval to "
                     "three decimals: $[0.542,\\,0.598]$ vs $[0.542,\\,0.598]$ vs $[0.542,\\,0.598]$ "
                     "(rec23 P3).",
            ha="center", va="center", fontsize=8.6, color=MUTED, style="italic")
    ax.text(52, 53.2, "Which variance goes under the square root?  (L23 slide 7; B&T \u00a79.1)",
            ha="center", va="center", fontsize=10.5, color=INK, weight="600")
    fig.tight_layout()
    save(fig, "whichvar")


# ===========================================================================
# Fig 1.5 - half-width vs n for the three variance choices (B&T its Fig 9.4)
# ===========================================================================
def fig_halfwidth():
    that = 0.57
    plug = that * (1 - that)
    ns = np.logspace(1, 4, 400)
    hb = 1.96 * np.sqrt(plug / ns)
    hc = 1.96 * np.sqrt(0.25 / ns)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.8))

    ax = axes[0]
    ax.plot(ns, hc, color=ORANGE, lw=2.2, label=r"bound $v=1/4$")
    ax.plot(ns, hb, color=BLUE, lw=2.2, label=r"plug-in $v=\hat\theta_n(1-\hat\theta_n)=0.2451$")
    ax.axvline(1200, color=MUTED, lw=1.2, ls="--")
    ax.text(1320, 0.115, "$n=1200$\n(rec23 P3)", fontsize=8.4, color=MUTED,
            ha="left", va="top")
    ax.plot([1200], [1.96 * np.sqrt(0.25 / 1200)], "o", color=ORANGE, ms=5)
    ax.plot([1200], [1.96 * np.sqrt(plug / 1200)], "o", color=BLUE, ms=5)
    ax.set_xscale("log")
    ax.set_xlim(10, 10000)
    ax.set_ylim(0, 0.34)
    ax.set_xlabel("sample size $n$  (log scale)")
    ax.set_ylabel("half-width of the 95% CI")
    ax.set_title("(a) half-width $1.96\\sqrt{v/n}$", loc="left")
    ax.legend(loc="upper right", fontsize=8.6)

    ax = axes[1]
    ax.plot(ns, hc - hb, color=RED, lw=2.2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(7, 17000)
    ax.set_ylim(6e-5, 7e-3)
    ax.set_xlabel("sample size $n$  (log scale)")
    ax.set_ylabel("extra half-width of the bound")
    ax.set_title("(b) price of being conservative", loc="left")
    for nn, txt in ((10, "0.00305"), (100, "0.00097"), (1200, "0.00028"), (10000, "0.000097")):
        y = 1.96 * (np.sqrt(0.25 / nn) - np.sqrt(plug / nn))
        ax.plot([nn], [y], "o", color=RED, ms=5)
        ax.annotate(txt, xy=(nn, y), xytext=(6, 9), textcoords="offset points",
                    fontsize=8.2, color=RED, ha="left")
    fig.tight_layout()
    save(fig, "halfwidth")


fig_msedecomp()
fig_coverage()
fig_pipeline()
fig_whichvar()
fig_halfwidth()
print("done")
