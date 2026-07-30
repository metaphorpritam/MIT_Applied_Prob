# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G3 §5 (synthesis + rec10 checkpoint).

Outputs (notes/img/):
  g3_s5_zoo.png       — the four continuous families: pdf (top) / CDF (bottom)
  g3_s5_flowchart.png — which derived-distribution method to use
  g3_s5_gotchas.png   — density>1, triangle non-independence, missing |dg/dx|
  g3_s5_casino.png    — rec10 P3 PMFs (basic game X, conditional, extended Y)
"""
import io
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "notes" / "_build"))
from mpl_style import setup, diagram_ax, PAL, INK, MUTED, GRID_C  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
plt, _ = setup()
IMG = Path(__file__).resolve().parents[1] / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    p = IMG / f"{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ------------------------------------------------------------------ zoo ----
def fig_zoo():
    fig, axes = plt.subplots(2, 4, figsize=(13.6, 5.6))

    # uniform [2,7]
    a, b = 2.0, 7.0
    x = np.linspace(0, 9, 1200)
    pdf = np.where((x >= a) & (x <= b), 1 / (b - a), 0.0)
    cdf = np.clip((x - a) / (b - a), 0, 1)
    axes[0, 0].plot(x, pdf, color=PAL[0])
    axes[0, 0].fill_between(x, 0, pdf, color=PAL[0], alpha=0.16)
    axes[0, 0].set_title("Uniform$[a,b]$,  $a=2$, $b=7$")
    axes[0, 0].set_ylim(0, 0.32)
    axes[0, 0].annotate(r"height $\frac{1}{b-a}=0.2$", xy=(4.5, 0.2),
                        xytext=(4.0, 0.28), ha="center", fontsize=9, color=MUTED,
                        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
    axes[1, 0].plot(x, cdf, color=PAL[0])

    # exponential lam=2
    lam = 2.0
    x = np.linspace(0, 3, 1200)
    axes[0, 1].plot(x, lam * np.exp(-lam * x), color=PAL[1])
    axes[0, 1].fill_between(x, 0, lam * np.exp(-lam * x), color=PAL[1], alpha=0.16)
    axes[0, 1].set_title(r"Exponential$(\lambda)$,  $\lambda=2$")
    axes[0, 1].annotate(r"$f(0)=\lambda=2>1$", xy=(0.0, 2.0), xytext=(0.75, 1.75),
                        fontsize=9, color=MUTED,
                        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
    axes[1, 1].plot(x, 1 - np.exp(-lam * x), color=PAL[1])

    # normal N(2,16)
    mu, sg = 2.0, 4.0
    x = np.linspace(mu - 4 * sg, mu + 4 * sg, 1200)
    axes[0, 2].plot(x, stats.norm.pdf(x, mu, sg), color=PAL[2])
    axes[0, 2].fill_between(x, 0, stats.norm.pdf(x, mu, sg), color=PAL[2], alpha=0.16)
    axes[0, 2].set_title(r"Normal$(\mu,\sigma^2)$,  $\mu=2$, $\sigma^2=16$")
    axes[0, 2].axvline(mu, color=MUTED, lw=0.9, ls="--")
    axes[0, 2].annotate(r"$\mu\pm\sigma$", xy=(mu + sg, stats.norm.pdf(mu + sg, mu, sg)),
                        xytext=(mu + 2.2 * sg, 0.075), fontsize=9, color=MUTED,
                        arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
    axes[1, 2].plot(x, stats.norm.cdf(x, mu, sg), color=PAL[2])

    # beta(2,1) and beta(2,3)
    x = np.linspace(0, 1, 1200)
    axes[0, 3].plot(x, stats.beta.pdf(x, 2, 1), color=PAL[3], label=r"$\alpha=2,\beta=1$")
    axes[0, 3].plot(x, stats.beta.pdf(x, 2, 3), color=PAL[4], label=r"$\alpha=2,\beta=3$")
    axes[0, 3].set_title(r"Beta$(\alpha,\beta)$")
    axes[0, 3].legend(loc="upper left", fontsize=8)
    axes[1, 3].plot(x, stats.beta.cdf(x, 2, 1), color=PAL[3])
    axes[1, 3].plot(x, stats.beta.cdf(x, 2, 3), color=PAL[4])

    for j in range(4):
        axes[0, j].set_ylabel("$f_X(x)$" if j == 0 else "")
        axes[1, j].set_ylabel("$F_X(x)$" if j == 0 else "")
        axes[1, j].set_ylim(-0.03, 1.06)
        axes[1, j].set_xlabel("$x$")
        axes[1, j].set_title("CDF", fontsize=9, color=MUTED)
    fig.tight_layout(h_pad=1.6, w_pad=1.2)
    save(fig, "g3_s5_zoo")


# ------------------------------------------------------------ flowchart ----
def box(ax, x, y, w, h, text, fc="#ffffff", ec=None, fs=9.5, bold=False):
    ec = ec or GRID_C
    ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, facecolor=fc,
                               edgecolor=ec, linewidth=1.2, zorder=2,
                               joinstyle="round"))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
            zorder=3, linespacing=1.35,
            fontweight="600" if bold else "normal")


def arrow(ax, p, q, label=None, lx=0.0, ly=0.0, fs=8.5):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2,
                                shrinkA=2, shrinkB=3))
    if label:
        mx, my = (p[0] + q[0]) / 2 + lx, (p[1] + q[1]) / 2 + ly
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                color=MUTED, bbox=dict(boxstyle="round,pad=0.18", fc="white",
                                       ec="none"))


def fig_flowchart():
    fig, ax = plt.subplots(figsize=(11.6, 8.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 80)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)

    box(ax, 50, 75, 52, 6.0,
        "You need something about $Y=g(X)$ or $Y=g(X_1,\\dots,X_n)$",
        fc="#eef4fc", bold=True)
    box(ax, 50, 65, 44, 7.0,
        "Do you actually need the whole distribution,\nor only $\\mathbb{E}[Y]$?",
        fc="#fdf6e6")
    arrow(ax, (50, 72.0), (50, 68.6))

    box(ax, 15, 53, 28, 9.0,
        "Expected-value rule\n$\\mathbb{E}[g(X)]=\\int g(x)f_X(x)\\,dx$\n"
        "— no derived PDF needed", fc="#eaf7f1")
    arrow(ax, (28, 63.0), (19, 57.8), "only the mean", ly=1.8, lx=-2.0)

    box(ax, 64, 54, 32, 6.0, "Is $X$ discrete or continuous?", fc="#fdf6e6")
    arrow(ax, (56, 61.4), (61, 57.2), "full law", lx=5.5, ly=0.8)

    box(ax, 85, 40, 26, 12.0, "", fc="#eaf7f1")
    ax.text(85, 44.6, "Discrete:", ha="center", va="center", fontsize=9.5,
            color=INK, zorder=3)
    ax.text(85, 40.2, "$p_Y(y)=\\sum_{x:\\,g(x)=y}\\,p_X(x)$", ha="center",
            va="center", fontsize=9.5, color=INK, zorder=3)
    ax.text(85, 35.6, "then check $\\sum_y p_Y(y)=1$ — done", ha="center",
            va="center", fontsize=9.5, color=INK, zorder=3)
    ax.text(85, 31.4, "(terminal branch: no calculus,\nno support integral)",
            ha="center", va="center", fontsize=8.5, color=MUTED, zorder=3)
    arrow(ax, (76, 51.0), (83, 46.2), "discrete", lx=4.5, ly=1.2)

    box(ax, 42, 41, 38, 6.0,
        "Continuous. Is $g$ of one variable, strictly monotonic?",
        fc="#fdf6e6")
    arrow(ax, (58, 50.9), (46, 44.2))

    box(ax, 14, 27, 26, 10.0,
        "Monotonic formula\n$f_Y(y)=f_X(x)\\,/\\,|dg/dx\\,(x)|$\nwith $x=g^{-1}(y)$",
        fc="#eaf7f1")
    arrow(ax, (25, 38.0), (16, 32.2), "yes", lx=-2.0, ly=1.4)

    box(ax, 57, 27, 32, 7.0,
        "Is it $X_1+X_2$ with\n$X_1,X_2$ independent?", fc="#fdf6e6")
    arrow(ax, (48, 38.0), (54, 30.7), "no", lx=3.2, ly=0.6)

    box(ax, 85, 13, 26, 10.0,
        "Convolution\n$f_W(w)=\\int f_X(x)f_Y(w-x)\\,dx$", fc="#eaf7f1")
    arrow(ax, (73, 25.0), (82, 18.2), "yes", lx=3.4, ly=1.2)

    box(ax, 42, 13, 36, 10.0,
        "CDF method (always works)\n1. $F_Y(y)=\\mathbf{P}(g(X)\\leq y)$ as an\n"
        "area or integral of $f_X$\n2. $f_Y(y)=dF_Y/dy$", fc="#eaf7f1")
    arrow(ax, (50, 23.4), (45, 18.2), "no", lx=3.0, ly=0.4)

    box(ax, 33, 3.0, 58, 5.0,
        "Finish (continuous branches): state the support of $Y$ and check "
        "$\\int f_Y(y)\\,dy=1$",
        fc="#fbeceb")
    arrow(ax, (42, 8.0), (40, 5.6))
    arrow(ax, (14, 22.0), (20, 5.6))
    arrow(ax, (72, 10.5), (63, 4.0))
    fig.tight_layout()
    save(fig, "g3_s5_flowchart")


# -------------------------------------------------------------- gotchas ----
def fig_gotchas():
    fig, axes = plt.subplots(1, 3, figsize=(13.4, 4.2))

    # (a) densities above 1
    ax = axes[0]
    x = np.linspace(-0.35, 1.05, 1400)
    u = np.where((x >= 0) & (x <= 0.5), 2.0, 0.0)
    ax.plot(x, u, color=PAL[0], label=r"Uniform$[0,\frac{1}{2}]$:  $f=2$")
    ax.fill_between(x, 0, u, color=PAL[0], alpha=0.16)
    ax.plot(x, stats.norm.pdf(x, 0.5, 0.1), color=PAL[1],
            label=r"$N(0.5,\,0.1^2)$:  peak $3.99$")
    ax.axhline(1.0, color=MUTED, ls="--", lw=1.0)
    ax.text(-0.32, 1.08, "height 1", fontsize=8.5, color=MUTED)
    ax.set_title("(a) a density may exceed 1")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f_X(x)$")
    ax.set_ylim(0, 4.5)
    ax.legend(loc="upper right", fontsize=8)

    # (b) triangle: support is not a rectangle
    ax = axes[1]
    ax.fill([0, 1, 1], [0, 0, 1], color=PAL[2], alpha=0.22, zorder=1)
    ax.plot([0, 1, 1, 0], [0, 0, 1, 0], color=PAL[2], lw=1.6, zorder=2)
    ax.text(0.66, 0.22, r"$f_{X,Y}=2$", fontsize=10, color=INK, zorder=3)
    ax.plot([0.2], [0.8], marker="x", ms=9, mew=2.2, color=PAL[7], zorder=4)
    ax.annotate(r"$f_{X,Y}(0.2,0.8)=0$" "\n" r"but $f_X(0.2)f_Y(0.8)=0.16$",
                xy=(0.2, 0.8), xytext=(0.02, 1.02), fontsize=8.5, color=INK,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
    ax.set_xlim(-0.05, 1.25)
    ax.set_ylim(-0.05, 1.3)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("(b) triangular support $\\Rightarrow$ dependent")

    # (c) missing |dg/dx|
    ax = axes[2]
    y = np.linspace(0.004, 1, 1400)
    ax.plot(y, 1 / (2 * np.sqrt(y)), color=PAL[0],
            label=r"correct  $f_Y(y)=\frac{1}{2\sqrt{y}}$")
    ax.plot(y, np.ones_like(y), color=PAL[7], ls="--",
            label=r"wrong  $f_X(\sqrt{y})=1$")
    ax.set_ylim(0, 6)
    ax.set_xlabel("$y$")
    ax.set_ylabel("$f_Y(y)$")
    ax.set_title(r"(c) $Y=X^2$, $X\sim$Uniform$[0,1]$")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout(w_pad=2.0)
    save(fig, "g3_s5_gotchas")


# --------------------------------------------------------------- casino ----
def fig_casino():
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 3.9))

    ax = axes[0]
    xs = [1, 2, 3, 4, 5, 6]
    ps = [1 / 4, 1 / 4, 5 / 16, 1 / 16, 1 / 16, 1 / 16]
    ax.stem(xs, ps, linefmt=f"-", markerfmt="o", basefmt=" ")
    for ln in ax.get_children():
        pass
    ax.axvline(21 / 8, color=PAL[1], ls="--", lw=1.4)
    ax.annotate(r"$\mathbb{E}[X]=21/8=2.625$", xy=(21 / 8, 0.415),
                xytext=(4.05, 0.415), color=PAL[1], fontsize=10, va="center",
                arrowprops=dict(arrowstyle="->", color=PAL[1], lw=1.0))
    for x_, p_, lab in zip(xs, ps, ["1/4", "1/4", "5/16", "1/16", "1/16", "1/16"]):
        ax.text(x_, p_ + 0.012, lab, ha="center", fontsize=8.5, color=MUTED)
    ax.set_ylim(0, 0.46)
    ax.set_xlim(0.3, 6.7)
    ax.set_xticks(xs)
    ax.set_xlabel("$x$ (payoff, dollars)")
    ax.set_ylabel("$p_X(x)$")
    ax.set_title("rec10 P3.1 — basic game")

    ax = axes[1]
    ax.stem([3, 4], [4 / 5, 1 / 5], linefmt="-", markerfmt="o", basefmt=" ")
    ax.text(3, 0.82, "4/5", ha="center", fontsize=9, color=MUTED)
    ax.text(4, 0.22, "1/5", ha="center", fontsize=9, color=MUTED)
    ax.set_xlim(2.4, 4.6)
    ax.set_ylim(0, 1.0)
    ax.set_xticks([3, 4])
    ax.set_xlabel("$z$ (first roll)")
    ax.set_ylabel("$p_{Z\\mid B}(z)$")
    ax.set_title("rec10 P3.3 — first roll given $X=3$")

    ax = axes[2]
    vals, pr = [], []
    for k in range(0, 6):
        for last in (1, 2, 3):
            vals.append(2 * k + last)
            pr.append((1 / 4) ** k * (1 / 4))
    agg = {}
    for v_, p_ in zip(vals, pr):
        agg[v_] = agg.get(v_, 0) + p_
    ks = sorted(agg)
    ax.stem(ks, [agg[k] for k in ks], linefmt="-", markerfmt="o", basefmt=" ")
    ax.axvline(8 / 3, color=PAL[1], ls="--", lw=1.4)
    ax.annotate(r"$\mathbb{E}[Y]=8/3\approx 2.667$", xy=(8 / 3, 0.62),
                xytext=(4.6, 0.62), color=PAL[1], fontsize=10, va="center",
                arrowprops=dict(arrowstyle="->", color=PAL[1], lw=1.0))
    ax.set_yscale("log")
    ax.set_ylim(1e-6, 3.0)
    ax.set_xlabel("$y$ (payoff, dollars)")
    ax.set_ylabel("$p_Y(y)$  (log scale)")
    ax.set_title("rec10 P3.4 — extended game")
    fig.tight_layout(w_pad=2.2)
    save(fig, "g3_s5_casino")


fig_zoo()
fig_flowchart()
fig_gotchas()
fig_casino()
