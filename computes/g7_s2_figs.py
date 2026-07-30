# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
r"""Figures for G7 section 2 — maximum likelihood estimation.

Run:  uv run computes/g7_s2_figs.py
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


def save(fig, name):
    p = IMG / f"g7_s2_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# =====================================================================
# Fig 2.1 — likelihood is a function of theta, not a density in theta
# =====================================================================
def fig_likelihood_vs_density():
    n, kobs = 10, 7
    ks = np.arange(0, n + 1)
    thetas = [0.3, 0.5, 0.7, 0.9]
    cols = [BLUE, GREEN, ORANGE, PURPLE]

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.0),
                             gridspec_kw={"width_ratios": [1.25, 1.0]})

    ax = axes[0]
    off = [-0.30, -0.10, 0.10, 0.30]
    for t, c, o in zip(thetas, cols, off):
        pm = stats.binom.pmf(ks, n, t)
        ax.vlines(ks + o, 0, pm, color=c, lw=2.6, alpha=0.9,
                  label=rf"$\theta={t}$")
        ax.plot(ks + o, pm, "o", color=c, ms=3.4)
    ax.axvspan(kobs - 0.45, kobs + 0.45, color=GOLD, alpha=0.16, zorder=0)
    ax.text(kobs, 0.315, "observed\n$k=7$", ha="center", va="top",
            fontsize=9, color=INK, fontweight="600")
    ax.set_xticks(ks)
    ax.set_xlim(-0.7, 10.7)
    ax.set_ylim(0, 0.40)
    ax.set_xlabel("data value $k$ (number of heads in $n=10$ tosses)")
    ax.set_ylabel(r"$p_X(k;\theta)$")
    ax.set_title(r"Four models, one for each $\theta$: each set of stems sums to 1")
    ax.legend(loc="upper left", fontsize=8.5)

    ax = axes[1]
    tt = np.linspace(0.001, 0.999, 600)
    L = stats.binom.pmf(kobs, n, tt)
    ax.plot(tt, L, color=RED, lw=2.4)
    ax.fill_between(tt, 0, L, color=RED, alpha=0.12)
    for t, c in zip(thetas, cols):
        ax.plot([t], [stats.binom.pmf(kobs, n, t)], "o", color=c, ms=7,
                zorder=5, markeredgecolor="white", markeredgewidth=1.0)
    ax.axvline(0.7, color=MUTED, ls="--", lw=1.2)
    ax.annotate(r"$\hat\theta_{ML}=k/n=0.7$", xy=(0.7, 0.2668),
                xytext=(0.245, 0.205), fontsize=9.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    # keep this box in the empty upper-left corner: over the interior it hid the
    # left flank of the likelihood curve (roughly theta = 0.30 to 0.60)
    ax.text(0.028, 0.301,
            "shaded area $=1/11=0.0909$\n" r"(not 1 — no density in $\theta$)",
            ha="left", va="top", fontsize=9, color=INK,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=GRID_C))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.31)
    ax.set_xlabel(r"parameter $\theta$")
    ax.set_ylabel(r"$L(\theta)=p_X(7;\theta)$")
    ax.set_title("The likelihood: read the same number across models")

    fig.suptitle(r"Fixing the data and sweeping $\theta$ gives the likelihood function",
                 fontsize=11.5, fontweight="600", y=1.02)
    fig.tight_layout()
    save(fig, "likelihood_vs_density")


# =====================================================================
# Fig 2.2 — decision flowchart
# =====================================================================
def fig_flow():
    # Roomier than it needs to look: stacked mathtext limits (the theta under
    # "max", the i under "max") used to drop onto the following line, so the
    # line spacing is generous and the labels avoid \max_ subscripts entirely.
    fig, ax = plt.subplots(figsize=(11.2, 9.8))
    ax.axis("off")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 126)
    ax.set_aspect("auto")

    def box(x, y, w, h, text, fc="white", ec=AXIS_C, fs=9.0, bold=False):
        ax.add_patch(mp.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                       boxstyle="round,pad=0.5,rounding_size=1.4",
                                       fc=fc, ec=ec, lw=1.3, zorder=2))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
                fontweight="600" if bold else "normal", zorder=3, linespacing=1.75)

    def diamond(x, y, w, h, text, fs=8.8):
        ax.add_patch(mp.Polygon([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2],
                                 [x - w / 2, y]], closed=True, fc="#fdf6e3",
                                ec=GOLD, lw=1.4, zorder=2))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
                zorder=3, linespacing=1.55)

    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4,
                                    shrinkA=0, shrinkB=0), zorder=1)

    def line(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1, y2], color=MUTED, lw=1.4, zorder=1,
                solid_capstyle="round")

    def tag(x, y, t):
        ax.text(x, y, t, fontsize=8.6, color=MUTED, ha="center", va="center",
                fontweight="600", zorder=4, linespacing=1.35)

    box(50, 120, 62, 8, "Unknown quantity + data $x$.  Produce an estimate.",
        fc="#eef4fc", ec=BLUE, bold=True, fs=9.8)
    arrow(50, 116, 50, 110.8)
    diamond(50, 104, 38, 13,
            "Are you willing to put a" "\n"
            "PROBABILITY DISTRIBUTION" "\n"
            "on the unknown?")

    line(31, 104, 21, 104)
    arrow(21, 104, 21, 98.9)
    tag(26.0, 107.0, "yes")
    box(21, 91.5, 38, 14,
        "Bayesian  (G6 §3–§4)" "\n"
        r"$\Theta$ is a random variable, prior $p_\Theta$" "\n"
        r"MAP: maximize $p_{\Theta|X}(\theta\mid x)$ in $\theta$" "\n"
        r"LMS: $\mathbb{E}[\Theta\mid X=x]$",
        fc="#f3f0fb", ec=PURPLE, fs=8.6)

    line(69, 104, 79, 104)
    arrow(79, 104, 79, 98.9)
    tag(74.0, 107.0, "no")
    box(79, 91.5, 38, 14,
        "Classical  (this note)" "\n"
        r"$\theta$ is a fixed unknown constant" "\n"
        r"one model per $\theta$:  $p_X(x;\theta)$" "\n"
        "no prior, no posterior",
        fc="#eef7f2", ec=DGREEN, fs=8.6)

    line(21, 84.5, 21, 71)
    arrow(21, 71, 25.4, 71)
    ax.text(23.2, 80.6, "flat / uniform prior\n" r"$\Rightarrow$ MAP $=$ ML",
            fontsize=8.6, color=MUTED, ha="left", va="center",
            fontweight="600", linespacing=1.45)
    line(79, 84.5, 79, 71)
    arrow(79, 71, 74.6, 71)
    box(50, 71, 48, 11,
        "Maximum likelihood:" "\n"
        r"$\hat\theta_{ML}$ maximizes $p_X(x;\theta)$ over $\theta$",
        fc="#eef7f2", ec=DGREEN, bold=True, fs=9.6)

    arrow(50, 65.5, 50, 61.3)
    box(50, 56, 48, 10,
        r"Take logs:  $\ell(\theta)=\log p_X(x;\theta)$" "\n"
        r"products $\to$ sums, same maximizer", fs=9.2)
    arrow(50, 51, 50, 47.8)
    diamond(50, 41, 48, 13,
            r"Does the RANGE of the data depend on $\theta$?" "\n"
            r"(equivalently: is $\ell$ smooth, with an" "\n"
            "interior maximum?)")

    line(26, 41, 18, 41)
    arrow(18, 41, 18, 33.0)
    tag(21.0, 44.8, "no —\nsmooth")
    box(20, 27, 34, 11.5,
        r"Set $d\ell/d\theta=0$, solve," "\n"
        "and CHECK it is a maximum" "\n"
        r"(sign of $\ell'$, or $\ell''<0$)", ec=BLUE, fs=8.8)

    line(74, 41, 82, 41)
    arrow(82, 41, 82, 33.0)
    tag(79.5, 44.8, "yes —\nrange moves")
    box(80, 27, 38, 11.5,
        "Calculus fails — argue directly." "\n"
        r"$L(\theta)=\theta^{-n}$ on $\theta\geq\max\{x_1,\dots,x_n\}$" "\n"
        r"decreases $\Rightarrow\ \hat\theta=\max\{x_1,\dots,x_n\}$",
        ec=ORANGE, fs=8.8)

    line(20, 21.25, 20, 10.5)
    arrow(20, 10.5, 27.4, 10.5)
    line(80, 21.25, 80, 10.5)
    arrow(80, 10.5, 72.6, 10.5)
    box(50, 10.5, 44, 11.5,
        r"Report the ESTIMATOR $\hat\Theta_n$, not only" "\n"
        r"the number $\hat\theta$.  Then ask: bias?" "\n"
        "consistency?  confidence interval (§1)?",
        ec=BLUE, fs=8.8)

    ax.text(50, 1.8, "Decision guide for §2  (L23 slides 2–3, L24 slide 2; B&T §9.1)",
            ha="center", fontsize=8.8, color=MUTED, style="italic")
    fig.tight_layout()
    save(fig, "flow")


# =====================================================================
# Fig 2.3 — log-likelihood curves
# =====================================================================
def fig_loglik():
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.0))

    # (a) Bernoulli: relative log-likelihood sharpens with n
    ax = axes[0]
    tt = np.linspace(0.02, 0.98, 700)
    for n, c in [(10, BLUE), (50, GREEN), (200, ORANGE)]:
        k = 0.7 * n
        ll = k * np.log(tt) + (n - k) * np.log(1 - tt)
        ll -= k * math.log(0.7) + (n - k) * math.log(0.3)
        ax.plot(tt, ll, color=c, lw=2.2, label=f"$n={n}$")
    ax.axvline(0.7, color=MUTED, ls="--", lw=1.2)
    ax.plot([0.7], [0.0], "o", color=RED, ms=7, zorder=5,
            markeredgecolor="white")
    # place the label in the clear band above the peak (at -1.3 it was struck
    # through by the n = 50 and n = 200 curves and by the dashed vertical line)
    ax.annotate(r"$\hat\theta_{ML}=0.7$", xy=(0.7, 0.05), xytext=(0.755, 1.5),
                fontsize=9, color=INK, ha="left", va="center",
                bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=GRID_C),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
    ax.set_ylim(-14, 2.6)
    ax.set_xlim(0.15, 1.0)
    ax.set_xlabel(r"$\theta$")
    ax.set_ylabel(r"$\ell(\theta)-\ell(\hat\theta)$")
    ax.set_title(r"(a) Bernoulli, $k/n=0.7$ fixed: more data, sharper peak")
    ax.legend(loc="lower left", fontsize=8.5)

    # (b) normal (mu, v) log-likelihood contours
    ax = axes[1]
    x = np.array([4.62, 6.28, 3.31, 7.05, 5.44, 2.87, 5.91, 4.03, 6.77, 3.52])
    n = len(x)
    mus = np.linspace(3.6, 6.4, 240)
    vs = np.linspace(0.8, 6.5, 240)
    M, V = np.meshgrid(mus, vs)
    SS = ((x[:, None, None] - M[None]) ** 2).sum(axis=0)
    LL = -n / 2 * np.log(2 * np.pi) - n / 2 * np.log(V) - SS / (2 * V)
    ax.contourf(M, V, LL, levels=np.linspace(-30, -17.8, 26), cmap="Blues",
                alpha=0.30)
    cs = ax.contour(M, V, LL, levels=[-26, -22, -20, -18.5],
                    colors=[BLUE], linewidths=1.1)
    ax.clabel(cs, fmt="%.1f", fontsize=7.2, inline=True)
    ax.plot([4.98], [2.06602], "o", color=RED, ms=8, zorder=6,
            markeredgecolor="white", markeredgewidth=1.2)
    ax.annotate(r"$(\hat\mu,\hat v)=(4.980,\ 2.066)$", xy=(4.98, 2.066),
                xytext=(6.30, 5.60), fontsize=8.8, color=INK, ha="right",
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
    ax.axhline(2.2956, color=DGREEN, ls=":", lw=1.6)
    ax.text(3.70, 2.42, r"unbiased $\hat s_n^2=2.296$", fontsize=8.2,
            color=DGREEN, ha="left", va="bottom", fontweight="600")
    ax.set_xlim(3.6, 6.4)
    ax.set_ylim(0.8, 6.5)
    ax.set_xlabel(r"mean $\mu$")
    ax.set_ylabel(r"variance $v$")
    ax.set_title(r"(b) Normal $\ell(\mu,v)$, $n=10$ (rec23 P2)")

    # (c) exponential
    ax = axes[2]
    xs = np.array([0.42, 1.31, 0.08, 2.05, 0.64])
    tt = np.linspace(0.05, 4.0, 500)
    ll = len(xs) * np.log(tt) - tt * xs.sum()
    ax.plot(tt, ll, color=PURPLE, lw=2.4)
    hat = len(xs) / xs.sum()
    ax.axvline(hat, color=MUTED, ls="--", lw=1.2)
    ax.plot([hat], [len(xs) * math.log(hat) - hat * xs.sum()], "o", color=RED,
            ms=7, zorder=5, markeredgecolor="white")
    ax.annotate(rf"$\hat\theta_{{ML}}=n/\sum x_i={hat:.4f}$", xy=(hat, -4.47),
                xytext=(1.35, -9.8), fontsize=8.8, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    ax.set_xlim(0, 4)
    ax.set_ylim(-16, -3)
    ax.set_xlabel(r"rate $\theta$")
    ax.set_ylabel(r"$\ell(\theta)=n\log\theta-\theta\sum x_i$")
    ax.set_title(r"(c) Exponential, $n=5$ (L23 slide 3)")

    fig.tight_layout()
    save(fig, "loglik")


# =====================================================================
# Fig 2.4 — uniform [0, theta]: the corner solution
# =====================================================================
def fig_uniform():
    data = [3.1, 7.4, 2.2, 6.9, 5.3]
    mx = max(data)
    n = len(data)

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.1))

    ax = axes[0]
    tt = np.linspace(mx, 13, 400)
    L = tt ** (-n)
    ax.plot(tt, L, color=BLUE, lw=2.6)
    ax.plot([0.5, mx], [0, 0], color=BLUE, lw=2.6)
    ax.plot([mx], [0], "o", color="white", ms=7, markeredgecolor=BLUE,
            markeredgewidth=1.8, zorder=5)
    ax.plot([mx], [mx ** -n], "o", color=RED, ms=8, zorder=6,
            markeredgecolor="white", markeredgewidth=1.2)
    ax.vlines(data, 0, 1.1e-5, color=MUTED, lw=1.2)
    for d in data:
        ax.plot([d], [0], "|", color=MUTED, ms=10)
    ax.text(4.75, 1.35e-5, "the five data points", fontsize=8.6, color=MUTED,
            ha="center")
    ax.annotate(r"$\hat\theta_{ML}=\max_i x_i=7.4$" "\n"
                r"$L=7.4^{-5}=4.51\times10^{-5}$",
                xy=(mx, mx ** -n), xytext=(0.9, 5.5e-5), fontsize=9,
                color=INK, va="top", ha="left",
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
    ax.text(10.3, 3.75e-5,
            r"$\dfrac{dL}{d\theta}=-5\theta^{-6}<0$" "\n"
            "never zero — the peak sits\nat the edge of the support",
            fontsize=8.6, color=INK, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=GRID_C))
    ax.set_xlim(0.5, 13)
    ax.set_ylim(0, 6.0e-5)
    ax.set_xlabel(r"$\theta$")
    ax.set_ylabel(r"likelihood $L(\theta)$")
    ax.set_title(r"(a) $L$ is zero below $\max_i x_i$, then decays")

    ax = axes[1]
    th = 8.0
    m = np.linspace(0, th, 400)
    dens = n * m ** (n - 1) / th ** n
    ax.plot(m, dens, color=ORANGE, lw=2.4)
    ax.fill_between(m, 0, dens, color=ORANGE, alpha=0.15)
    ax.axvline(th, color=DGREEN, lw=1.8)
    ax.axvline(th * n / (n + 1), color=RED, ls="--", lw=1.6)
    ax.text(0.25, 0.71, r"true $\theta=8$  (solid green)", color=DGREEN,
            fontsize=9.2, ha="left", va="top", fontweight="600")
    ax.text(0.25, 0.635,
            r"$\mathbb{E}[\hat\Theta_5]=\frac{5}{6}\theta=6.667$  (dashed red)",
            color=RED, fontsize=9.2, ha="left", va="top", fontweight="600")
    ax.text(0.25, 0.545, r"bias $=\mathbb{E}[\hat\Theta_5]-\theta=-\theta/6=-1.333$",
            color=INK, fontsize=9.2, ha="left", va="top", fontweight="600")
    ax.annotate("", xy=(th, 0.14), xytext=(th * n / (n + 1), 0.14),
                arrowprops=dict(arrowstyle="<|-|>", color=INK, lw=1.3))
    ax.text((th + th * n / (n + 1)) / 2, 0.175, r"$-1.333$",
            ha="center", fontsize=8.8, color=INK)
    ax.set_xlim(0, 9.3)
    ax.set_ylim(0, 0.75)
    ax.set_xlabel(r"value of $\hat\Theta_n=\max_i X_i$")
    ax.set_ylabel("density")
    ax.set_title(r"(b) $\hat\Theta_n$ always under-shoots: $f(m)=5m^4/8^5$, $n=5$")

    fig.tight_layout()
    save(fig, "uniform")


# =====================================================================
# Fig 2.5 — rec24 P1: photon counts
# =====================================================================
def fig_photon():
    counts = np.array([53, 132, 8, 214, 61, 97, 19, 156, 44, 88, 3, 121])
    n = len(counts)
    sn = counts.mean()

    def muK(t):
        return 1.0 / (np.exp(1.0 / t) - 1.0)

    fig, axes = plt.subplots(1, 3, figsize=(12.4, 4.0))

    ax = axes[0]
    ks = np.arange(0, 400)
    for t, c in [(5.0, BLUE), (30.0, GREEN), (100.0, ORANGE)]:
        p = 1 - math.exp(-1 / t)
        ax.plot(ks, p * np.exp(-ks / t), color=c, lw=2.0,
                label=rf"$\theta={t:.0f}$  ($\mu_K={muK(t):.1f}$)")
    ax.set_yscale("log")
    ax.set_ylim(1e-6, 0.5)
    ax.set_xlim(0, 400)
    ax.set_xlabel("photon count $k$")
    ax.set_ylabel(r"$p_K(k;\theta)$  (log scale)")
    ax.set_title(r"(a) The model: geometric decay at rate $1/\theta$")
    ax.legend(fontsize=8.4, loc="upper right")

    ax = axes[1]
    tt = np.linspace(45, 190, 600)
    ll = n * np.log(1 - np.exp(-1 / tt)) - counts.sum() / tt
    ax.plot(tt, ll, color=PURPLE, lw=2.4)
    hat = 1 / math.log(1 + 1 / sn)
    llhat = n * math.log(1 - math.exp(-1 / hat)) - counts.sum() / hat
    ax.plot([hat], [llhat], "o", color=RED, ms=8, zorder=6,
            markeredgecolor="white", markeredgewidth=1.2)
    ax.axvline(sn, color=DGREEN, ls="--", lw=1.5)
    # two short lines anchored inside the axes: the one-line version overflowed
    # the right spine and bled into the gutter before panel (c)
    ax.annotate("exact $\\hat\\theta_{12}=1/\\log(1+1/s_n)$\n$=83.499$",
                xy=(hat, llhat), xytext=(103, -64.68), fontsize=8.4, color=INK,
                va="top", ha="left",
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
    ax.text(sn - 3, -66.75, r"hot-body $s_n=83$", color=DGREEN, fontsize=8.6,
            rotation=90, ha="right", va="bottom", fontweight="600")
    ax.set_xlim(45, 190)
    ax.set_ylim(-67.0, -64.55)
    ax.set_xlabel(r"temperature $\theta$")
    ax.set_ylabel(r"$\ell(\theta)$")
    ax.set_title("(b) Log-likelihood of the 12 counts (rec24 P1c)")

    ax = axes[2]
    s = np.linspace(0.3, 20, 500)
    ex = 1 / np.log(1 + 1 / s)
    ax.plot(s, ex, color=BLUE, lw=2.4, label=r"exact $\hat\theta=1/\log(1+1/s_n)$")
    ax.plot(s, s, color=ORANGE, lw=2.0, ls="--",
            label=r"hot-body approximation $\hat\theta\approx s_n$")
    ax.fill_between(s, s, ex, color=GOLD, alpha=0.25)
    ax.annotate("gap $\\to 1/2$ as $s_n$ grows\n(relative error $\\to 0$)",
                xy=(12, 12.5), xytext=(5.6, 17.6), fontsize=8.6, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 21)
    ax.set_xlabel(r"sample mean $s_n$")
    # horizontal, so the circumflex stays glued to the theta (rotated mathtext
    # detached the hat and it read as a stray apostrophe)
    ax.set_ylabel(r"$\hat\theta$", rotation=0, labelpad=14, ha="right",
                  va="center")
    ax.set_title(r"(c) When is $\hat\theta\approx s_n$ safe?")
    ax.legend(fontsize=8.2, loc="lower right")

    fig.tight_layout()
    save(fig, "photon")


# =====================================================================
# Fig 2.6 — rec24 P2: least squares as ML
# =====================================================================
def fig_regression():
    xs = np.array([0.8, 2.5, 5.0, 7.3, 9.1])
    ys = np.array([-2.3, 20.9, 103.5, 215.8, 334.0])
    th1, th0 = 40.534760, -65.861716
    b1, b0 = 4.091151, -3.074505

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.2),
                             gridspec_kw={"width_ratios": [1.35, 1.0]})

    ax = axes[0]
    g = np.linspace(0, 10.2, 300)
    ax.plot(g, th0 + th1 * g, color=ORANGE, lw=2.2, ls="--",
            label=r"first order  $y=40.53x-65.86$")
    ax.plot(g, b0 + b1 * g ** 2, color=PURPLE, lw=2.2,
            label=r"second order  $y=4.09x^2-3.07$")
    for x, y in zip(xs, ys):
        ax.plot([x, x], [y, th0 + th1 * x], color=ORANGE, lw=1.0, alpha=0.55)
    ax.plot(xs, ys, "o", color=DGREEN, ms=8, markerfacecolor="white",
            markeredgewidth=2.0, label="the five data pairs", zorder=5)
    ax.set_xlim(0, 10.2)
    ax.set_ylim(-110, 430)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("(a) Two ML fits of the rec24 P2 data")
    ax.legend(fontsize=8.6, loc="upper left")

    ax = axes[1]
    r1 = ys - (th0 + th1 * xs)
    r2 = ys - (b0 + b1 * xs ** 2)
    w = 0.32
    ax.bar(np.arange(5) - w / 2 - 0.02, r1, width=w, color=ORANGE,
           label="first order (SSE $=3455.0$)")
    ax.bar(np.arange(5) + w / 2 + 0.02, r2, width=w, color=PURPLE,
           label="second order (SSE $=28.07$)")
    ax.axhline(0, color=AXIS_C, lw=1.2)
    for i, v in enumerate(r1):
        ax.text(i - w / 2 - 0.02, v + (4 if v > 0 else -4), f"{v:.1f}",
                ha="center", va="bottom" if v > 0 else "top", fontsize=8,
                color=INK)
    for i, v in enumerate(r2):
        ax.text(i + w / 2 + 0.02, v + (4 if v > 0 else -4), f"{v:.1f}",
                ha="center", va="bottom" if v > 0 else "top", fontsize=8,
                color=INK)
    ax.set_xticks(np.arange(5))
    ax.set_xticklabels([f"$x={v}$" for v in xs], fontsize=8.6)
    ax.set_ylim(-52, 52)
    ax.set_ylabel(r"residual $y_i-\hat y_i$")
    ax.set_title("(b) Residuals: what the ML criterion actually squares")
    ax.legend(fontsize=8.4, loc="lower right")

    fig.tight_layout()
    save(fig, "regression")


fig_likelihood_vs_density()
fig_flow()
fig_loglik()
fig_uniform()
fig_photon()
fig_regression()
print("done")
