# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for notes/src/fragments/g3_s1.html  ->  notes/img/g3_s1_*.png

Run:  uv run computes/g3_s1_figs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "notes" / "_build"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mpl_style import setup, diagram_ax, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
import matplotlib.patches as mpatches  # noqa: E402

IMG = Path(__file__).resolve().parents[1] / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    p = IMG / f"g3_s1_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ---------------------------------------------------------------- Fig 1.1
# pdf area = probability, and the delta-slab reading
def fig_area():
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.5))

    # bimodal density like L08 slide 2
    x = np.linspace(-0.4, 6.4, 900)
    f = 0.45 * stats.norm.pdf(x, 1.4, 0.62) + 0.55 * stats.norm.pdf(x, 4.0, 0.95)

    ax = axes[0]
    ax.plot(x, f, color=PAL[0], lw=2.2)
    a, b = 0.8, 2.3
    m = (x >= a) & (x <= b)
    ax.fill_between(x[m], 0, f[m], color=PAL[0], alpha=0.28, hatch="///",
                    edgecolor=PAL[0], linewidth=0)
    ax.set_xticks([a, b])
    ax.set_xticklabels(["$a$", "$b$"])
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f_X(x)$")
    ax.set_ylim(0, 0.42)
    ax.set_xlim(-0.4, 6.4)
    ax.set_yticks([])
    ax.set_title("Probability = area under the density")
    ax.annotate(r"$\mathbf{P}(a\leq X\leq b)=\int_a^b f_X(x)\,dx$",
                xy=(1.6, 0.10), xytext=(3.1, 0.33),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1),
                fontsize=10.5, color=INK, ha="left")

    # right: delta slab
    ax = axes[1]
    ax.plot(x, f, color=PAL[0], lw=2.2)
    xs, dl = 3.3, 0.55
    m2 = (x >= xs) & (x <= xs + dl)
    ax.fill_between(x[m2], 0, f[m2], color=PAL[1], alpha=0.30, linewidth=0)
    fx = float(0.45 * stats.norm.pdf(xs, 1.4, 0.62) + 0.55 * stats.norm.pdf(xs, 4.0, 0.95))
    ax.add_patch(mpatches.Rectangle((xs, 0), dl, fx, fill=False,
                                    edgecolor=PAL[1], lw=1.6, ls="--"))
    ax.plot([xs, xs], [0, fx], color=PAL[1], lw=1.2)
    ax.set_xticks([xs, xs + dl])
    ax.set_xticklabels(["$x$", "$x+\\delta$"])
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f_X(x)$")
    ax.set_ylim(0, 0.42)
    ax.set_xlim(-0.4, 6.4)
    ax.set_yticks([])
    ax.set_title("A thin slab: rectangle $\\approx$ area")
    ax.annotate(r"$\mathbf{P}(x\leq X\leq x+\delta)\approx f_X(x)\cdot\delta$",
                xy=(xs + dl / 2, fx), xytext=(0.15, 0.345),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1),
                fontsize=10.5, color=INK, ha="left")
    fig.tight_layout()
    save(fig, "pdf_area")


# ---------------------------------------------------------------- Fig 1.2
def fig_uniform():
    a, b = 2.0, 7.0
    h = 1.0 / (b - a)
    mu = (a + b) / 2
    sd = (b - a) / np.sqrt(12)
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.plot([a - 1.6, a], [0, 0], color=PAL[0], lw=2.2)
    ax.plot([a, a], [0, h], color=PAL[0], lw=2.2)
    ax.plot([a, b], [h, h], color=PAL[0], lw=2.2)
    ax.plot([b, b], [h, 0], color=PAL[0], lw=2.2)
    ax.plot([b, b + 1.6], [0, 0], color=PAL[0], lw=2.2)
    xs = np.linspace(a, b, 200)
    ax.fill_between(xs, 0, h, color=PAL[0], alpha=0.16, linewidth=0)
    ax.plot([mu, mu], [0, h], color=PAL[1], lw=1.6, ls="--")
    ax.annotate("", xy=(mu - sd, h * 0.40), xytext=(mu + sd, h * 0.40),
                arrowprops=dict(arrowstyle="<->", color=PAL[3], lw=1.6))
    ax.text(mu, h * 0.28, r"$\mu\pm\sigma$   ($\sigma=1.443$)", ha="center",
            va="center", color=PAL[3], fontsize=10,
            bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="none"))
    ax.text(mu + 0.18, h * 0.78, r"$\mathbb{E}[X]=(a+b)/2=4.5$", ha="left",
            va="center", color=PAL[1], fontsize=10.5)
    ax.annotate(r"height $=1/(b-a)=0.2$", xy=(3.0, h), xytext=(a - 1.5, h * 1.30),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1),
                ha="left", va="center", color=INK, fontsize=10.5)
    ax.set_xticks([a, mu, b])
    ax.set_xticklabels(["$a=2$", "4.5", "$b=7$"])
    ax.set_yticks([0, h])
    ax.set_yticklabels(["0", "0.2"])
    ax.set_xlim(a - 1.9, b + 1.6)
    ax.set_ylim(0, h * 1.55)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f_X(x)$")
    ax.set_title(r"Uniform on $[2,7]$:  $\mathrm{var}(X)=(b-a)^2/12=25/12\approx2.083$")
    fig.tight_layout()
    save(fig, "uniform")


# ---------------------------------------------------------------- Fig 1.3
def fig_cdf_trio():
    fig, axes = plt.subplots(2, 3, figsize=(10.6, 5.4))

    # --- column 1: continuous (uniform on [1,4])
    a, b = 1.0, 4.0
    h = 1 / (b - a)
    ax = axes[0, 0]
    ax.plot([-0.6, a, a, b, b, 5.2], [0, 0, h, h, 0, 0], color=PAL[0], lw=2.2)
    ax.fill_between(np.linspace(a, b, 100), 0, h, color=PAL[0], alpha=0.16, lw=0)
    ax.set_title("Continuous: uniform pdf")
    ax.set_ylabel("$f_X(x)$")
    ax.set_ylim(0, 0.55)
    ax.set_xlim(-0.6, 5.2)
    ax.set_xticks([a, b])
    ax.set_xticklabels(["$a$", "$b$"])

    ax = axes[1, 0]
    xs = np.linspace(-0.6, 5.2, 400)
    ax.plot(xs, np.clip((xs - a) / (b - a), 0, 1), color=PAL[2], lw=2.2)
    ax.set_title("CDF: a ramp, continuous")
    ax.set_ylabel("$F_X(x)$")
    ax.set_ylim(-0.05, 1.12)
    ax.set_xlim(-0.6, 5.2)
    ax.set_xticks([a, b])
    ax.set_xticklabels(["$a$", "$b$"])
    ax.set_yticks([0, 0.5, 1])

    # --- column 2: discrete (L08 slide 4: 1/6 at 1, 3/6 at 2, 2/6 at 4)
    ks = np.array([1, 2, 4])
    pk = np.array([1 / 6, 3 / 6, 2 / 6])
    ax = axes[0, 1]
    ax.vlines(ks, 0, pk, color=PAL[0], lw=2.2)
    ax.plot(ks, pk, "o", color=PAL[0], ms=6)
    for k, p, lab in zip(ks, pk, ["1/6", "3/6", "2/6"]):
        ax.text(k, p + 0.03, lab, ha="center", color=INK, fontsize=9.5)
    ax.set_title("Discrete: PMF")
    ax.set_ylabel("$p_X(x)$")
    ax.set_ylim(0, 0.68)
    ax.set_xlim(0, 5.2)
    ax.set_xticks([1, 2, 4])

    ax = axes[1, 1]
    lev = np.cumsum(pk)
    edges = [(-0.5, 1, 0.0), (1, 2, lev[0]), (2, 4, lev[1]), (4, 5.2, lev[2])]
    for x0, x1, y in edges:
        ax.plot([x0, x1], [y, y], color=PAL[2], lw=2.2)
    for k, ylo, yhi in zip(ks, [0.0, lev[0], lev[1]], lev):
        ax.plot([k], [yhi], "o", color=PAL[2], ms=5)
        ax.plot([k], [ylo], "o", color="white", mec=PAL[2], mew=1.5, ms=5)
        ax.plot([k, k], [ylo, yhi], color=PAL[2], lw=1.0, ls=":")
    ax.set_title("CDF: right-continuous staircase")
    ax.set_ylim(-0.05, 1.12)
    ax.set_xlim(0, 5.2)
    ax.set_xticks([1, 2, 4])
    ax.set_yticks([0, 1 / 6, 4 / 6, 1])
    ax.set_yticklabels(["0", "1/6", "4/6", "1"])

    # --- column 3: mixed (L08 slide 5): slab 1/2 on [0,1], atom 1/2 at x=1/2
    ax = axes[0, 2]
    ax.plot([-0.35, 0, 0, 1, 1, 1.35], [0, 0, 0.5, 0.5, 0, 0], color=PAL[0], lw=2.2)
    ax.fill_between(np.linspace(0, 1, 60), 0, 0.5, color=PAL[0], alpha=0.16, lw=0)
    ax.annotate("", xy=(0.5, 1.0), xytext=(0.5, 0.0),
                arrowprops=dict(arrowstyle="->", color=PAL[1], lw=2.6))
    ax.text(0.55, 1.0, "atom of mass 1/2", color=PAL[1], fontsize=9.5,
            ha="left", va="center")
    ax.set_title("Mixed: slab + point mass")
    ax.set_ylim(0, 1.35)
    ax.set_xlim(-0.35, 1.35)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5])

    ax = axes[1, 2]
    xs = np.linspace(-0.35, 1.35, 700)
    y = np.where(xs < 0, 0.0,
                 np.where(xs < 0.5, 0.5 * xs,
                          np.where(xs < 1.0, 0.5 + 0.5 * xs, 1.0)))
    ax.plot(xs[xs < 0.5], y[xs < 0.5], color=PAL[2], lw=2.2)
    ax.plot(xs[(xs >= 0.5) & (xs <= 1.0)], y[(xs >= 0.5) & (xs <= 1.0)],
            color=PAL[2], lw=2.2)
    ax.plot(xs[xs > 1.0], y[xs > 1.0], color=PAL[2], lw=2.2)
    ax.plot([0.5, 0.5], [0.25, 0.75], color=PAL[2], lw=1.0, ls=":")
    ax.plot([0.5], [0.75], "o", color=PAL[2], ms=5)
    ax.plot([0.5], [0.25], "o", color="white", mec=PAL[2], mew=1.5, ms=5)
    ax.set_title("CDF: ramps + one jump")
    ax.set_ylim(-0.05, 1.12)
    ax.set_xlim(-0.35, 1.35)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.25, 0.75, 1])
    ax.set_yticklabels(["0", "1/4", "3/4", "1"])

    for ax in axes.flat:
        ax.set_xlabel("$x$")
    fig.tight_layout(h_pad=1.8, w_pad=1.4)
    save(fig, "cdf_trio")


# ---------------------------------------------------------------- Fig 1.4
def fig_taxi():
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    xs = np.linspace(-1.2, 8.0, 900)
    y = np.where(xs < 0, 0.0, np.where(xs < 5, 2 / 3 + xs / 30, 1.0))
    ax.plot(xs[xs < 0], y[xs < 0], color=PAL[2], lw=2.4)
    ax.plot(xs[(xs >= 0) & (xs < 5)], y[(xs >= 0) & (xs < 5)], color=PAL[2], lw=2.4)
    ax.plot(xs[xs >= 5], y[xs >= 5], color=PAL[2], lw=2.4)
    # jumps
    ax.plot([0, 0], [0, 2 / 3], color=PAL[1], lw=1.4, ls=":")
    ax.plot([5, 5], [5 / 6, 1.0], color=PAL[1], lw=1.4, ls=":")
    ax.plot([0], [2 / 3], "o", color=PAL[2], ms=6)
    ax.plot([0], [0], "o", color="white", mec=PAL[2], mew=1.6, ms=6)
    ax.plot([5], [1.0], "o", color=PAL[2], ms=6)
    ax.plot([5], [5 / 6], "o", color="white", mec=PAL[2], mew=1.6, ms=6)

    ax.annotate("jump 2/3\n(taxi already waiting)", xy=(0, 0.33), xytext=(0.72, 0.30),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1),
                fontsize=9.5, color=INK, ha="left")
    ax.annotate("jump 1/6\n(bus at 5 min)", xy=(5, 0.917), xytext=(5.55, 0.63),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1),
                fontsize=9.5, color=INK, ha="left")
    ax.annotate("ramp of slope 1/30\n(taxi arrives before the bus)",
                xy=(2.5, 0.75), xytext=(0.9, 0.90),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1),
                fontsize=9.5, color=INK, ha="left")
    ax.plot([5 / 4, 5 / 4], [0, 0.12], color=PAL[3], lw=1.6, ls="--")
    ax.text(5 / 4 + 0.16, 0.06, r"$\mathbb{E}[X]=5/4$ min", color=PAL[3],
            fontsize=9.8, ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="none"))
    ax.set_xlim(-1.2, 8.0)
    ax.set_ylim(-0.06, 1.14)
    ax.set_xticks([0, 2.5, 5, 7])
    ax.set_xticklabels(["0", "2.5", "5", "7"])
    ax.set_yticks([0, 2 / 3, 5 / 6, 1])
    ax.set_yticklabels(["0", "2/3", "5/6", "1"])
    ax.set_xlabel("$x$ (minutes)")
    ax.set_ylabel("$F_X(x)$")
    ax.set_title("Al's waiting time: a mixed CDF (rec08 P2 / B&T Problem 3.9)")
    fig.tight_layout()
    save(fig, "taxi_cdf")


# ---------------------------------------------------------------- Fig 1.5
def fig_exponential():
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.6))
    x = np.linspace(0, 8, 700)
    for i, lam in enumerate([0.5, 1.0, 2.0]):
        axes[0].plot(x, lam * np.exp(-lam * x), color=PAL[i], lw=2.2,
                     label=fr"$\lambda={lam}$  ($\mathbb{{E}}[X]={1/lam:g}$)")
        axes[1].plot(x, 1 - np.exp(-lam * x), color=PAL[i], lw=2.2,
                     label=fr"$\lambda={lam}$")
    axes[0].plot([0, 0], [0, 2.0], color=PAL[2], lw=2.2)
    axes[0].set_ylabel(r"$f_X(x)=\lambda e^{-\lambda x}$")
    axes[0].set_title("Exponential pdf: intercept $\\lambda$, decay rate $\\lambda$")
    axes[0].set_ylim(0, 2.15)
    axes[0].legend(loc="upper right")
    axes[1].set_ylabel(r"$F_X(x)=1-e^{-\lambda x}$")
    axes[1].set_title("Exponential CDF")
    axes[1].set_ylim(0, 1.08)
    axes[1].axhline(1, color=AXIS_C, lw=1.0, ls="--")
    axes[1].legend(loc="lower right")
    for ax in axes:
        ax.set_xlabel("$x$")
        ax.set_xlim(0, 8)
    fig.tight_layout()
    save(fig, "exponential")


# ---------------------------------------------------------------- Fig 1.6
def fig_memoryless():
    lam = 0.4
    t = 3.0
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.6))

    ax = axes[0]
    x = np.linspace(0, 14, 800)
    ax.plot(x, lam * np.exp(-lam * x), color=PAL[0], lw=2.2, label="pdf of $T$")
    m = x >= t
    ax.fill_between(x[m], 0, lam * np.exp(-lam * x[m]), color=PAL[0],
                    alpha=0.20, lw=0)
    ax.axvline(t, color=PAL[1], lw=1.5, ls="--")
    ax.text(t + 0.15, 0.36, f"$t={t:g}$: still burning", color=PAL[1], fontsize=9.5)
    ax.text(6.4, 0.10, r"$\mathbf{P}(T>t)=e^{-\lambda t}$", color=INK, fontsize=10)
    ax.set_title("Condition on survival past $t$ …")
    ax.set_ylabel("$f_T(x)$")
    ax.set_xlabel("$x$")
    ax.set_ylim(0, 0.44)
    ax.set_xlim(0, 14)
    ax.legend(loc="upper right")

    ax = axes[1]
    xr = np.linspace(0, 11, 700)
    ax.plot(xr, lam * np.exp(-lam * xr), color=PAL[2], lw=3.4, alpha=0.45,
            label="fresh bulb: $\\lambda e^{-\\lambda x}$")
    ax.plot(xr, lam * np.exp(-lam * (t + xr)) / np.exp(-lam * t), color=PAL[1],
            lw=1.9, ls="--", label="residual life given $T>t$")
    ax.set_title("… and the rescaled tail is the original pdf")
    ax.set_ylabel("conditional density of $X=T-t$")
    ax.set_xlabel("$x$ (extra time)")
    ax.set_ylim(0, 0.44)
    ax.set_xlim(0, 11)
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, "memoryless")


# ---------------------------------------------------------------- Fig 1.7
def fig_maxmin():
    lam = 1.0
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.6))
    x = np.linspace(0, 7, 800)

    ax = axes[0]
    ax.plot(x, 2 * lam * np.exp(-2 * lam * x), color=PAL[1], lw=2.2,
            label=r"$W=\min\{X_1,X_2\}$: $2\lambda e^{-2\lambda w}$")
    ax.plot(x, lam * np.exp(-lam * x), color=PAL[0], lw=2.0, ls="--",
            label=r"one $X_i$: $\lambda e^{-\lambda x}$")
    ax.plot(x, 3 * lam * np.exp(-lam * x) * (1 - np.exp(-lam * x)) ** 2,
            color=PAL[2], lw=2.2,
            label=r"$Z=\max\{X_1,X_2,X_3\}$")
    ax.axvline(0.5, color=PAL[1], lw=1.1, ls=":")
    ax.axvline(11 / 6, color=PAL[2], lw=1.1, ls=":")
    ax.text(0.56, 1.72, r"$\mathbb{E}[W]=\frac{1}{2}$", color=PAL[1], fontsize=9.5)
    ax.text(11 / 6 + 0.15, 1.42, r"$\mathbb{E}[Z]=\frac{11}{6}$", color=PAL[2], fontsize=9.5)
    ax.set_ylim(0, 2.15)
    ax.set_xlim(0, 7)
    ax.set_xlabel("value")
    ax.set_ylabel("density")
    ax.set_title(r"Densities ($\lambda=1$): min sharpens, max spreads")
    ax.legend(loc="upper right", fontsize=8.5)

    ax = axes[1]
    ax.plot(x, 1 - np.exp(-2 * lam * x), color=PAL[1], lw=2.2, label=r"$F_W=1-e^{-2\lambda w}$")
    ax.plot(x, 1 - np.exp(-lam * x), color=PAL[0], lw=2.0, ls="--", label=r"$F_{X_i}=1-e^{-\lambda x}$")
    ax.plot(x, (1 - np.exp(-lam * x)) ** 3, color=PAL[2], lw=2.2, label=r"$F_Z=(1-e^{-\lambda z})^3$")
    ax.axhline(1, color=AXIS_C, lw=1.0, ls="--")
    ax.set_ylim(0, 1.08)
    ax.set_xlim(0, 7)
    ax.set_xlabel("value")
    ax.set_ylabel("CDF")
    ax.set_title("CDFs: cube one, square the tail of the other")
    ax.legend(loc="lower right", fontsize=8.5)
    fig.tight_layout()
    save(fig, "maxmin")


# ---------------------------------------------------------------- Fig 1.8
def fig_normal():
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.5))

    ax = axes[0]
    x = np.linspace(-8, 14, 900)
    for i, (mu, sd) in enumerate([(0, 1), (3, 2), (6, 0.8)]):
        ax.plot(x, stats.norm.pdf(x, mu, sd), color=PAL[i], lw=2.2,
                label=fr"$\mu={mu},\ \sigma={sd}$")
        ax.axvline(mu, color=PAL[i], lw=1.0, ls=":")
    ax.set_title("The normal family $N(\\mu,\\sigma^2)$")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f_X(x)$")
    ax.set_xlim(-8, 14)
    ax.set_ylim(0, 0.70)
    ax.legend(loc="upper right", fontsize=8.5)

    ax = axes[1]
    z = np.linspace(-4.2, 4.2, 700)
    for i, (mu, sd) in enumerate([(0, 1), (3, 2), (6, 0.8)]):
        ax.plot(z, stats.norm.pdf(z), color=PAL[i], lw=2.4 - 0.5 * i,
                ls=["-", "--", ":"][i], label=fr"$(X-{mu})/{sd}$")
    ax.set_title(r"Standardized: $Z=(X-\mu)/\sigma\sim N(0,1)$")
    ax.set_xlabel("$z$")
    ax.set_ylabel("$f_Z(z)$")
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(0, 0.47)
    ax.legend(loc="upper right", fontsize=8.5)

    ax = axes[2]
    ax.plot(z, stats.norm.pdf(z), color=PAL[0], lw=2.2)
    m = z <= 0.25
    ax.fill_between(z[m], 0, stats.norm.pdf(z[m]), color=PAL[0], alpha=0.26, lw=0)
    ax.axvline(0.25, color=PAL[1], lw=1.6, ls="--")
    ax.text(0.34, 0.42, "$z=0.25$", color=PAL[1], fontsize=10)
    ax.text(-3.9, 0.20, r"$\Phi(0.25)$" "\n" r"$=0.5987$", color=INK, fontsize=10.5,
            ha="left")
    ax.set_title(r"L08 slide 7: $X\sim N(2,16)$, $\mathbf{P}(X\leq3)$")
    ax.set_xlabel("$z$")
    ax.set_ylabel("$f_Z(z)$")
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(0, 0.47)
    fig.tight_layout()
    save(fig, "normal")


# ---------------------------------------------------------------- Fig 1.9
def fig_flow():
    fig, ax = plt.subplots(figsize=(9.6, 6.0))
    diagram_ax(ax)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 64)

    def box(cx, cy, w, h, text, fc, ec, fs=9.3):
        ax.add_patch(mpatches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.6,rounding_size=1.4",
            linewidth=1.4, facecolor=fc, edgecolor=ec))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=INK)

    def arrow(x0, y0, x1, y1, label="", lx=None, ly=None):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4,
                                    shrinkA=1, shrinkB=1))
        if label:
            ax.text(lx if lx is not None else (x0 + x1) / 2,
                    ly if ly is not None else (y0 + y1) / 2,
                    label, fontsize=8.6, color=MUTED, ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))

    box(50, 59, 44, 6.4, "What are you asked for?", "#f4f3ee", AXIS_C, 10)

    box(15, 46, 26, 8.4, "$\\mathbf{P}(a\\leq X\\leq b)$", "#e8f1fb", PAL[0])
    box(50, 46, 26, 8.4, "$\\mathbb{E}[X]$, $\\mathbb{E}[g(X)]$,\n$\\mathrm{var}(X)$", "#e8f1fb", PAL[0])
    box(85, 46, 26, 8.4, "law of a $\\max$, $\\min$,\nor a mixed r.v.", "#e8f1fb", PAL[0])
    arrow(38, 56.2, 20, 50.5)
    arrow(50, 56.2, 50, 50.5)
    arrow(62, 56.2, 80, 50.5)

    box(15, 31, 30, 11.5,
        "Integrate the pdf:\n$\\int_a^b f_X(x)\\,dx$\n"
        "or difference the CDF:\n$F_X(b)-F_X(a)$", "#fff", PAL[2])
    box(50, 31, 30, 11.5,
        "Integrate against $f_X$:\n$\\int x f_X\\,dx$, $\\int g(x) f_X\\,dx$,\n"
        "$\\int (x-\\mathbb{E}[X])^2 f_X\\,dx$\n(or $\\mathbb{E}[X^2]-(\\mathbb{E}[X])^2$)", "#fff", PAL[2])
    box(85, 31, 30, 11.5,
        "Go through the CDF:\nget $F(x)=\\mathbf{P}(\\cdot\\leq x)$ first,\n"
        "then differentiate\nto recover the pdf", "#fff", PAL[2])
    arrow(15, 41.5, 15, 37)
    arrow(50, 41.5, 50, 37)
    arrow(85, 41.5, 85, 37)

    box(15, 15, 30, 11.5,
        "Named family?\nuniform $\\to$ ratio of lengths\n"
        "exponential $\\to$ $e^{-\\lambda a}-e^{-\\lambda b}$\n"
        "normal $\\to$ standardize, use $\\Phi$", "#fdf6e6", PAL[3])
    box(50, 15, 30, 11.5,
        "Named family? read it off:\nuniform $\\frac{a+b}{2},\\frac{(b-a)^2}{12}$\n"
        "exponential $\\frac{1}{\\lambda},\\frac{1}{\\lambda^2}$\n"
        "normal $\\mu,\\ \\sigma^2$", "#fdf6e6", PAL[3])
    box(85, 15, 30, 11.5,
        "$\\max$: multiply CDFs\n$\\min$: multiply tails\n"
        "mixed: $F=pF_Y+(1-p)F_Z$\n(jumps = point masses)", "#fdf6e6", PAL[3])
    arrow(15, 25.2, 15, 21)
    arrow(50, 25.2, 50, 21)
    arrow(85, 25.2, 85, 21)

    ax.text(50, 4.2, "Always finish with a sanity check:  $f_X\\geq0$,  "
                     "$\\int f_X=1$,  $F_X$ nondecreasing from 0 to 1.",
            ha="center", va="center", fontsize=9.6, color=INK,
            bbox=dict(boxstyle="round,pad=0.5", fc="#f4f3ee", ec=AXIS_C, lw=1.2))
    fig.tight_layout()
    save(fig, "flow")


fig_area()
fig_uniform()
fig_cdf_trio()
fig_taxi()
fig_exponential()
fig_memoryless()
fig_maxmin()
fig_normal()
fig_flow()
print("done")
