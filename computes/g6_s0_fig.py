# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""G6 §0 figures.

  Fig 0.1  g6_s0_scalings.png   — the three scalings of L19 slide 7, drawn with
                                  the exact densities of sums of i.i.d. U(0,1)
                                  variables (numerical convolution, no sampling).
  Fig 0.2  g6_s0_twoviews.png   — classical vs Bayesian block diagram (L21 slide 2).
  Fig 0.3  g6_s0_conceptmap.png — concept map of note G6 (two arcs, five sections).
"""
import io
import sys

sys.path.insert(0, "d:/Python-UV/MIT_Applied_Prob/notes/_build")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402
from mpl_style import PAL, INK, MUTED, setup  # noqa: E402

plt, _ = setup()
IMG = "d:/Python-UV/MIT_Applied_Prob/notes/img/"
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL

# =====================================================================
# Fig 0.1 — the three scalings
# =====================================================================
DX = 0.0025
base = np.ones(int(round(1 / DX)) + 1)          # U(0,1) density on [0,1]

dens = {1: base.copy()}
cur = base.copy()
for k in range(2, 65):
    cur = np.convolve(cur, base) * DX
    cur = cur / np.trapezoid(cur, dx=DX)        # kill the O(dx) quadrature drift
    if k in (2, 4, 16, 64):
        dens[k] = cur.copy()


def grid_for(n):
    return np.arange(len(dens[n])) * DX


NS = [1, 4, 16, 64]
COLS = [BLUE, ORANGE, GREEN, PURPLE]

fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.9))

ax = axes[0]
for n, c in zip(NS, COLS):
    ax.plot(grid_for(n), dens[n], color=c, lw=1.8, label=f"$n={n}$")
ax.set_xlim(0, 45)
ax.set_ylim(0, 1.15)
ax.set_xlabel(r"value of $S_n$")
ax.set_ylabel("density")
ax.set_title(r"$S_n=X_1+\cdots+X_n$   —   spreads out")
ax.legend(loc="upper right")
ax.text(0.5, 0.62, r"$\operatorname{sd}=\sigma\sqrt{n}\to\infty$",
        transform=ax.transAxes, fontsize=9.5, color=MUTED, ha="center")

ax = axes[1]
for n, c in zip(NS, COLS):
    x = grid_for(n)
    ax.plot(x / n, dens[n] * n, color=c, lw=1.8, label=f"$n={n}$")
ax.set_xlim(0, 1)
ax.set_ylim(0, 12.5)
ax.set_xlabel(r"value of $M_n$")
ax.set_ylabel("density")
ax.set_title(r"$M_n=S_n/n$   —   concentrates at $\mu$")
ax.axvline(0.5, color=MUTED, lw=1.0, ls=":")
ax.text(0.505, 11.6, r"$\mu=1/2$", fontsize=9, color=MUTED, ha="left", va="top")
ax.legend(loc="upper left")

ax = axes[2]
for n, c in zip(NS, COLS):
    x = grid_for(n)
    z = (x - n * 0.5) / np.sqrt(n)
    ax.plot(z, dens[n] * np.sqrt(n), color=c, lw=1.8, label=f"$n={n}$")
zz = np.linspace(-1.25, 1.25, 400)
sig = np.sqrt(1 / 12)
ax.plot(zz, np.exp(-zz ** 2 / (2 * sig ** 2)) / (sig * np.sqrt(2 * np.pi)),
        color=INK, lw=1.3, ls="--", label=r"$N(0,\sigma^2)$")
ax.set_xlim(-1.25, 1.25)
ax.set_ylim(0, 1.55)
ax.set_xlabel(r"value of $(S_n-n\mu)/\sqrt{n}$")
ax.set_ylabel("density")
ax.set_title(r"$(S_n-n\mu)/\sqrt{n}$   —   settles into a shape")
ax.legend(loc="upper right", fontsize=8)

fig.tight_layout()
fig.savefig(IMG + "g6_s0_scalings.png", dpi=150)
plt.close(fig)
print("wrote", IMG + "g6_s0_scalings.png")

# =====================================================================
# Fig 0.2 — classical vs Bayesian block diagram (L21 slide 2)
# =====================================================================
fig, ax = plt.subplots(figsize=(11.0, 5.3))
ax.set_xlim(0, 112)
ax.set_ylim(0, 52)
ax.axis("off")
ax.grid(False)


def blk(x, y, w, h, lines, color, fs=10.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.5,rounding_size=1.0",
                                lw=1.5, edgecolor=color, facecolor=color,
                                alpha=0.09, zorder=1))
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.5,rounding_size=1.0",
                                lw=1.5, edgecolor=color, facecolor="none", zorder=3))
    ax.text(x + w / 2, y + h / 2, "\n".join(lines), ha="center", va="center",
            fontsize=fs, color=INK, linespacing=1.5, zorder=4)


def arr(x1, y1, x2, y2, color=MUTED, lw=1.4):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=13, lw=lw, color=color, zorder=2))


def row(y, title, tcol, in_lab, in_sub, box1, box2lab, out_lab, note):
    ax.text(2, y + 21.5, title, ha="left", va="center", fontsize=11.5,
            color=tcol, fontweight="600")
    # incoming arrow
    arr(6, y + 8, 24, y + 8, color=tcol, lw=1.6)
    ax.text(14.5, y + 10.0, in_lab, ha="center", va="bottom", fontsize=11, color=tcol)
    if in_sub:
        ax.text(14.5, y + 6.0, in_sub, ha="center", va="top", fontsize=9.2, color=MUTED)
    blk(24, y + 1, 24, 14, box1, tcol)
    # noise arrow into the top of box 1
    arr(36, y + 21, 36, y + 15.6, color=MUTED, lw=1.2)
    ax.text(37.2, y + 18.5, "$N$", ha="left", va="center", fontsize=10, color=MUTED)
    arr(48.6, y + 8, 62, y + 8, color=MUTED, lw=1.6)
    ax.text(55.3, y + 10.0, "$X$", ha="center", va="bottom", fontsize=11, color=INK)
    blk(62, y + 1, 20, 14, box2lab, MUTED)
    arr(82.6, y + 8, 95, y + 8, color=MUTED, lw=1.6)
    ax.text(88.5, y + 10.0, out_lab, ha="center", va="bottom", fontsize=11, color=INK)
    ax.text(111, y + 8, note, ha="right", va="center", fontsize=9.0,
            color=MUTED, linespacing=1.5)


row(28, "CLASSICAL  (L21 slide 2; B&T Ch. 8 preamble)", RED,
    r"$\theta$", "a constant, not a r.v.",
    [r"$p_X(x;\theta)$"], ["Estimator"], r"$\hat\Theta$",
    "one model per $\\theta$;\nno prior is written down")

row(2, "BAYESIAN  (L21 slide 2; this note, §3–§4)", GREEN,
    r"$\Theta$", r"prior $f_\Theta(\theta)$",
    [r"$f_{X\mid\Theta}(x\mid\theta)$"], ["Estimator"], r"$\hat\Theta$",
    "one joint model;\nBayes rule gives $f_{\\Theta\\mid X}$")

ax.plot([2, 110], [26.5, 26.5], color="#e1e0d9", lw=1.2, zorder=0)
fig.tight_layout()
fig.savefig(IMG + "g6_s0_twoviews.png", dpi=150)
plt.close(fig)
print("wrote", IMG + "g6_s0_twoviews.png")

# =====================================================================
# Fig 0.3 — concept map
# =====================================================================
fig, ax = plt.subplots(figsize=(10.4, 6.9))
ax.set_xlim(0, 100)
ax.set_ylim(0, 68)
ax.axis("off")
ax.grid(False)


def box(x, y, w, h, title, lines, color, fs_t=10.5, fs_b=8.8, alpha=0.10):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.4",
        linewidth=1.4, edgecolor=color, facecolor=color, alpha=alpha, zorder=1))
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.4",
        linewidth=1.4, edgecolor=color, facecolor="none", zorder=3))
    ax.text(x + w / 2, y + h - 2.6, title, ha="center", va="top",
            fontsize=fs_t, color=color, fontweight="600", zorder=4)
    ax.text(x + w / 2, y + h - 6.6, "\n".join(lines), ha="center", va="top",
            fontsize=fs_b, color=INK, linespacing=1.45, zorder=4)


def arrow(x1, y1, x2, y2, color=MUTED, style="-|>", rad=0.0, lw=1.3):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle=style, mutation_scale=13,
        linewidth=lw, color=color, zorder=2,
        connectionstyle=f"arc3,rad={rad}", shrinkA=1, shrinkB=1))


ax.text(50, 66.5, "G6  ·  from computing probabilities to drawing conclusions",
        ha="center", va="top", fontsize=12.5, color=INK, fontweight="600")

box(29, 52.5, 42, 11.5, "the setup you already own",
    [r"$X_1,\dots,X_n$ i.i.d., mean $\mu$, variance $\sigma^2$",
     r"$S_n=X_1+\cdots+X_n$,   $M_n=S_n/n$"],
    MUTED, fs_t=10.0, alpha=0.07)

ax.text(24.5, 48.4, "ARC A   what happens as  n → ∞", ha="center", va="center",
        fontsize=10.0, color=BLUE, fontweight="600")
ax.text(75.5, 48.4, "ARC B   the unknown becomes random", ha="center", va="center",
        fontsize=10.0, color=GREEN, fontweight="600")

arrow(43, 51.2, 30, 49.7, color=BLUE, rad=0.12)
arrow(57, 51.2, 70, 49.7, color=GREEN, rad=-0.12)

box(3, 33.5, 43, 13.0, "§1   inequalities + WLLN   (L19, rec20)",
    [r"Markov · Chebyshev · $\operatorname{var}(M_n)=\sigma^2/n$",
     r"$M_n\to\mu$ in probability",
     "bounds that need only mean and variance"],
    BLUE)

box(3, 17.0, 43, 13.0, "§2   central limit theorem   (L20, rec21)",
    [r"$Z_n=(S_n-n\mu)/(\sigma\sqrt{n})\ \Rightarrow\ \Phi$",
     "the shape, not just the spread",
     "sharp approximation where §1 only bounds"],
    ORANGE)

arrow(24.5, 33.0, 24.5, 30.5, color=ORANGE)
ax.text(26.0, 31.7, "same $M_n$, finer question", ha="left", va="center",
        fontsize=8.2, color=MUTED)

box(54, 33.5, 43, 13.0, "§3   prior → posterior → MAP   (L21, rec22)",
    [r"$f_{\Theta|X}\propto f_\Theta\cdot p_{X|\Theta}$   (Bayes, G1 §2)",
     "the posterior is the whole answer",
     "MAP = the most probable value"],
    GREEN)

box(54, 17.0, 43, 13.0, "§4   LMS + linear LMS   (L22, rec22)",
    [r"$\mathbf{E}[\Theta\mid X]$ minimizes $\mathbf{E}[(\Theta-g(X))^2]$",
     r"linear: $\hat\Theta=\mathbf{E}[\Theta]+\frac{\operatorname{cov}(\Theta,X)}{\operatorname{var}(X)}(X-\mathbf{E}[X])$",
     "one number out of the posterior"],
    GOLD, fs_b=8.2)

arrow(75.5, 33.0, 75.5, 30.5, color=GOLD)
ax.text(74.0, 31.7, "which single number?", ha="right", va="center",
        fontsize=8.2, color=MUTED)

box(22, 1.5, 56, 13.5, "§5   synthesis and bridge",
    ["which bound / which approximation / which estimator",
     "limit theorems are what make an estimate trustworthy;",
     "the classical view keeps the unknown deterministic"],
    PURPLE)

arrow(24.5, 16.5, 38, 15.4, color=PURPLE, rad=-0.10)
arrow(75.5, 16.5, 62, 15.4, color=PURPLE, rad=0.10)

arrow(46.6, 23.5, 53.4, 23.5, color=MUTED, style="<|-|>", rad=0.0, lw=1.1)
ax.text(50, 25.4, "how good\nis it?", ha="center", va="bottom",
        fontsize=8.2, color=MUTED, linespacing=1.3)

fig.savefig(IMG + "g6_s0_conceptmap.png", dpi=150)
plt.close(fig)
print("wrote", IMG + "g6_s0_conceptmap.png")
