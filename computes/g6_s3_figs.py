# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G6 section 3 - Bayesian inference: priors, posteriors, MAP.

Run:  uv run computes/g6_s3_figs.py
"""
from __future__ import annotations

import sys
from math import log, sqrt
from pathlib import Path

import numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
from mpl_style import setup, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
import matplotlib.patches as mp  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL


def save(fig, name):
    p = IMG / f"g6_s3_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ------------------------------------------------------------------ helpers
def box(ax, x, y, w, h, text, fc="#eef4fc", ec=BLUE, fs=10, tc=INK, lw=1.5,
        style="round,pad=0.02,rounding_size=0.03"):
    ax.add_patch(mp.FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=style,
                                   fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, zorder=4)


def arrow(ax, p, q, color=MUTED, lw=1.5, label=None, lpos=0.5, dx=0.0, dy=0.035,
          fs=9.5, rad=0.0, ha="center"):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                connectionstyle=f"arc3,rad={rad}",
                                shrinkA=0, shrinkB=0, mutation_scale=13), zorder=2)
    if label:
        mx = p[0] + (q[0] - p[0]) * lpos + dx
        my = p[1] + (q[1] - p[1]) * lpos + dy
        ax.text(mx, my, label, ha=ha, va="center", fontsize=fs, color=INK, zorder=4)


# =====================================================================
# Fig 3.1 - classical vs Bayesian pipeline (L21 slide 2)
# =====================================================================
fig, ax = plt.subplots(figsize=(8.4, 4.3))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.2)
ax.axis("off")
ax.grid(False)

# --- classical row (top)
ax.text(0.05, 4.95, "Classical:  $\\theta$ is an unknown constant",
        fontsize=11, color=INK, weight="600", ha="left", va="center")
box(ax, 3.05, 3.85, 2.3, 0.78, "model  $p_X(x;\\theta)$", fc="#f6f5f0", ec=AXIS_C)
box(ax, 7.30, 3.85, 1.9, 0.78, "Estimator", fc="#f6f5f0", ec=AXIS_C)
arrow(ax, (0.45, 3.85), (1.90, 3.85), label="$\\theta$", dy=0.30)
arrow(ax, (3.05, 4.75), (3.05, 4.24), label="noise $N$", dx=0.78, dy=0.0)
arrow(ax, (4.20, 3.85), (6.35, 3.85), label="data $X$", dy=0.30)
arrow(ax, (8.25, 3.85), (9.65, 3.85), label="$\\hat\\Theta$", dy=0.30)

ax.plot([0.05, 9.95], [3.02, 3.02], color=GRID_C, lw=1.2)

# --- Bayesian row (bottom)
ax.text(0.05, 2.72, "Bayesian:  $\\Theta$ is a random variable with a prior",
        fontsize=11, color=INK, weight="600", ha="left", va="center")
box(ax, 3.05, 1.45, 2.3, 0.78, "model  $p_{X|\\Theta}(x\\,|\\,\\theta)$")
box(ax, 7.30, 1.45, 1.9, 0.78, "Estimator")
arrow(ax, (0.45, 1.45), (1.90, 1.45), color=BLUE, label="$\\Theta$", dy=0.30)
ax.text(1.18, 1.02, "prior $p_\\Theta$ or $f_\\Theta$", fontsize=9.5,
        color=BLUE, ha="center", va="center")
arrow(ax, (3.05, 2.35), (3.05, 1.84), label="noise $N$", dx=0.78, dy=0.0)
arrow(ax, (4.20, 1.45), (6.35, 1.45), color=BLUE, label="data $X$", dy=0.30)
arrow(ax, (8.25, 1.45), (9.65, 1.45), color=BLUE, label="$\\hat\\Theta$", dy=0.30)
ax.text(7.30, 0.72, "Bayes' rule $\\rightarrow$ posterior $f_{\\Theta|X}(\\theta\\,|\\,x)$",
        fontsize=9.5, color=BLUE, ha="center", va="center")
ax.text(7.30, 0.28, "then MAP or $\\mathbb{E}[\\Theta\\,|\\,X=x]$",
        fontsize=9.5, color=MUTED, ha="center", va="center")
fig.tight_layout()
save(fig, "pipeline")

# =====================================================================
# Fig 3.2 - which version of Bayes' rule
# =====================================================================
fig, ax = plt.subplots(figsize=(8.6, 4.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.6)
ax.axis("off")
ax.grid(False)

box(ax, 5.0, 5.15, 4.3, 0.62, "Is the unknown $\\Theta$ discrete or continuous?",
    fc="#fdf6e8", ec=GOLD)
box(ax, 2.6, 3.75, 2.4, 0.55, "$\\Theta$ discrete: prior $p_\\Theta$", fc="#f6f5f0", ec=AXIS_C)
box(ax, 7.4, 3.75, 2.6, 0.55, "$\\Theta$ continuous: prior $f_\\Theta$", fc="#f6f5f0", ec=AXIS_C)
arrow(ax, (4.2, 4.84), (2.9, 4.03), rad=0.0)
arrow(ax, (5.8, 4.84), (7.1, 4.03), rad=0.0)

box(ax, 2.6, 2.75, 3.0, 0.5, "Is the data $X$ discrete or continuous?",
    fc="#fdf6e8", ec=GOLD, fs=9)
box(ax, 7.4, 2.75, 3.0, 0.5, "Is the data $X$ discrete or continuous?",
    fc="#fdf6e8", ec=GOLD, fs=9)
arrow(ax, (2.6, 3.47), (2.6, 3.02))
arrow(ax, (7.4, 3.47), (7.4, 3.02))

lab = ["$p_{\\Theta|X}(\\theta|x)=\\dfrac{p_\\Theta(\\theta)p_{X|\\Theta}(x|\\theta)}"
       "{\\sum_{\\theta'}p_\\Theta(\\theta')p_{X|\\Theta}(x|\\theta')}$",
       "$p_{\\Theta|X}(\\theta|x)=\\dfrac{p_\\Theta(\\theta)f_{X|\\Theta}(x|\\theta)}"
       "{\\sum_{\\theta'}p_\\Theta(\\theta')f_{X|\\Theta}(x|\\theta')}$",
       "$f_{\\Theta|X}(\\theta|x)=\\dfrac{f_\\Theta(\\theta)p_{X|\\Theta}(x|\\theta)}"
       "{\\int f_\\Theta(\\theta')p_{X|\\Theta}(x|\\theta')d\\theta'}$",
       "$f_{\\Theta|X}(\\theta|x)=\\dfrac{f_\\Theta(\\theta)f_{X|\\Theta}(x|\\theta)}"
       "{\\int f_\\Theta(\\theta')f_{X|\\Theta}(x|\\theta')d\\theta'}$"]
bx = [1.28, 3.78, 6.22, 8.72]
cols = ["#eef4fc", "#eef4fc", "#eafaf3", "#eafaf3"]
ecs = [BLUE, BLUE, GREEN, GREEN]
tags = ["$X$ discrete", "$X$ cont.", "$X$ discrete", "$X$ cont."]
for i in range(4):
    box(ax, bx[i], 1.15, 2.25, 1.35, lab[i], fc=cols[i], ec=ecs[i], fs=8.2)
    ax.text(bx[i], 2.08, tags[i], ha="center", va="center", fontsize=9, color=MUTED)
arrow(ax, (2.1, 2.50), (1.38, 2.28))
arrow(ax, (3.1, 2.50), (3.68, 2.28))
arrow(ax, (6.9, 2.50), (6.32, 2.28))
arrow(ax, (7.9, 2.50), (8.62, 2.28))
ax.text(5.0, 0.16, "The denominator never depends on $\\theta$: for MAP you may skip it entirely.",
        ha="center", va="center", fontsize=9.5, color=INK)
fig.tight_layout()
save(fig, "bayes4")

# =====================================================================
# Fig 3.3 - prior -> posterior narrowing (coin, uniform prior, freq 0.7)
# =====================================================================
fig, ax = plt.subplots(figsize=(7.4, 4.2))
th = np.linspace(1e-4, 1 - 1e-4, 1200)
combos = [(0, 0), (10, 7), (20, 14), (40, 28), (100, 70)]
for i, (nn, kk) in enumerate(combos):
    d = stats.beta(kk + 1, nn - kk + 1).pdf(th)
    lbl = "prior (n = 0)" if nn == 0 else f"n = {nn}, k = {kk}"
    ax.plot(th, d, color=PAL[i % 8], lw=2.0 if nn else 2.4,
            ls="--" if nn == 0 else "-", label=lbl)
ax.axvline(0.7, color=MUTED, lw=1.1, ls=":")
ax.text(0.775, 7.30, "observed\nfrequency 0.7", fontsize=9, color=MUTED,
        ha="left", va="center")
ax.set_xlim(0, 1)
ax.set_ylim(0, 9.2)
ax.set_xlabel("$\\theta$  (probability of heads)")
ax.set_ylabel("posterior density $f_{\\Theta|X}(\\theta\\,|\\,k)$")
ax.set_title("Uniform prior, binomial data: the posterior concentrates as $n$ grows")
ax.legend(loc="upper left", fontsize=8.6)
fig.tight_layout()
save(fig, "narrowing")

# =====================================================================
# Fig 3.4 - Romeo & Juliet posterior for three observed latenesses
# =====================================================================
fig, axes = plt.subplots(1, 3, figsize=(9.8, 3.6), sharey=True)
for ax, x in zip(axes, (0.2, 0.5, 0.8)):
    L = abs(log(x))
    t = np.linspace(x, 1, 600)
    ax.plot(t, 1 / (t * L), color=BLUE, lw=2.2)
    ax.fill_between(t, 0, 1 / (t * L), color=BLUE, alpha=0.12)
    ax.plot([0, x], [0, 0], color=BLUE, lw=2.2)
    m = (1 - x) / L
    ax.axvline(x, color=ORANGE, lw=1.8, ls="-")
    ax.axvline(m, color=GREEN, lw=1.8, ls="--")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 8.2)
    ax.set_title(f"$x = {x}$\nMAP $= {x:.2f}$,   mean $= {m:.3f}$", fontsize=9.8)
    ax.set_xlabel("$\\theta$")
axes[0].set_ylabel("$f_{\\Theta|X}(\\theta\\,|\\,x)$")
fig.suptitle("Romeo & Juliet posterior  $f_{\\Theta|X}(\\theta\\,|\\,x)=1/(\\theta\\,|\\ln x|)$"
             "  on  $[x,1]$\nsolid orange line = MAP,   dashed green line = posterior mean",
             fontsize=10.5, y=1.10)
fig.tight_layout()
save(fig, "rjposterior")

# =====================================================================
# Fig 3.5 - MAP vs conditional expectation as functions of x
# =====================================================================
fig, ax = plt.subplots(figsize=(6.9, 4.2))
xs = np.linspace(1e-4, 0.9999, 3000)
lms = (1 - xs) / np.abs(np.log(xs))
ax.plot(xs, xs, color=ORANGE, lw=2.2, ls="--", label="MAP estimate  $\\hat\\theta = x$")
ax.plot(xs, lms, color=GREEN, lw=2.4,
        label="LMS estimate  $\\mathbb{E}[\\Theta|X=x]=(1-x)/|\\ln x|$")
ax.fill_between(xs, xs, lms, color=GREEN, alpha=0.10)
xg = 0.166414
ax.plot([xg], [(1 - xg) / abs(log(xg))], "o", color=DGREEN, ms=6, zorder=5)
ax.annotate("widest gap 0.2984 at $x = 0.1664$",
            xy=(xg, (1 - xg) / abs(log(xg))), xytext=(0.30, 0.30),
            fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.02)
ax.set_xlabel("observed lateness $x$ (hours)")
ax.set_ylabel("estimate of $\\Theta$")
ax.set_title("Romeo & Juliet: the LMS estimate always exceeds the MAP estimate")
ax.legend(loc="upper left", fontsize=9)
fig.tight_layout()
save(fig, "mapvslms")

# =====================================================================
# Fig 3.6 - bimodal posterior: MAP and posterior mean both mislead
# =====================================================================
fig, ax = plt.subplots(figsize=(7.2, 4.2))
w1, mu1, sd1 = 0.45, 0.0, 0.30
w2, mu2, sd2 = 0.55, 4.0, 1.20
t = np.linspace(-2.0, 9.0, 3000)
d = w1 * stats.norm(mu1, sd1).pdf(t) + w2 * stats.norm(mu2, sd2).pdf(t)
ax.plot(t, d, color=BLUE, lw=2.3, label="posterior $f_{\\Theta|X}(\\theta\\,|\\,x)$")
ax.fill_between(t, 0, d, color=BLUE, alpha=0.10)
MAP, MEAN = 0.0, 2.2
dm = w1 * stats.norm(mu1, sd1).pdf(MEAN) + w2 * stats.norm(mu2, sd2).pdf(MEAN)
ax.axvline(MAP, color=ORANGE, lw=1.9, ls="--")
ax.axvline(MEAN, color=RED, lw=1.9, ls="-.")
ax.plot([MEAN], [dm], "o", color=RED, ms=6, zorder=5)
ax.text(MAP + 0.62, 0.600, "MAP $= 0$\ndensity 0.5991", color=ORANGE, fontsize=9.2,
        ha="left", va="top",
        bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="none", alpha=0.85))
ax.text(MEAN + 0.15, 0.35, "$\\mathbb{E}[\\Theta|X=x] = 2.2$\ndensity 0.0594\n"
        "(10.1$\\times$ lower than at the MAP)",
        color=RED, fontsize=9.2, ha="left", va="top")
ax.set_xlim(-2, 9)
ax.set_ylim(0, 0.66)
ax.set_xlabel("$\\theta$")
ax.set_ylabel("posterior density")
ax.set_title("A bimodal posterior: neither single number describes it")
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
save(fig, "bimodal")

# =====================================================================
# Fig 3.7 - which point estimate?
# =====================================================================
fig, ax = plt.subplots(figsize=(8.6, 4.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.4)
ax.axis("off")
ax.grid(False)

box(ax, 5.0, 5.00, 4.6, 0.58, "You have the posterior. What single number?",
    fc="#fdf6e8", ec=GOLD)
box(ax, 2.3, 3.70, 3.6, 0.62, "$\\Theta$ takes finitely many values\n(hypothesis testing)",
    fc="#f6f5f0", ec=AXIS_C, fs=9.2)
box(ax, 7.5, 3.70, 3.6, 0.62, "$\\Theta$ continuous\n(estimation)",
    fc="#f6f5f0", ec=AXIS_C, fs=9.2)
arrow(ax, (4.0, 4.70), (2.7, 4.03))
arrow(ax, (6.0, 4.70), (7.1, 4.03))

box(ax, 2.3, 2.35, 3.6, 0.72,
    "MAP: maximize $p_\\Theta(\\theta)p_{X|\\Theta}(x|\\theta)$\n"
    "minimizes $\\mathbf{P}(\\text{error})$", fc="#eef4fc", ec=BLUE, fs=9.2)
arrow(ax, (2.3, 3.38), (2.3, 2.72))

box(ax, 7.5, 2.35, 3.9, 0.72,
    "cost = squared error?  $\\rightarrow$  $\\mathbb{E}[\\Theta\\,|\\,X=x]$\n"
    "want the most likely value?  $\\rightarrow$  MAP", fc="#eafaf3", ec=GREEN, fs=9.2)
arrow(ax, (7.5, 3.38), (7.5, 2.72))

box(ax, 5.0, 0.95, 8.6, 0.82,
    "Posterior symmetric and unimodal (e.g. normal)?  Then MAP $=\\mathbb{E}[\\Theta\\,|\\,X=x]$"
    " and the choice is moot.\nBimodal or strongly skewed?  Report the whole posterior — "
    "a single number is misleading.", fc="#fdeeee", ec=RED, fs=9.2)
arrow(ax, (2.3, 1.99), (3.6, 1.40))
arrow(ax, (7.5, 1.99), (6.4, 1.40))
fig.tight_layout()
save(fig, "estimator")

print("done")
