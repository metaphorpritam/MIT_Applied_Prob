# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""G7 §0 figure.

  Fig 0.1  g7_s0_map.png — concept map of note G7: the classical setup of
           L23 slide 2 (theta -> p_X(x;theta) -> X -> Estimator -> hat-Theta)
           on top, then the two branches (estimation / hypothesis testing)
           and the five sections underneath.
"""
import io
import sys

sys.path.insert(0, "d:/Python-UV/MIT_Applied_Prob/notes/_build")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402
from mpl_style import PAL, INK, MUTED  # noqa: E402
from mpl_style import setup  # noqa: E402

plt, _ = setup()
IMG = "d:/Python-UV/MIT_Applied_Prob/notes/img/"
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL

fig, ax = plt.subplots(figsize=(11.4, 8.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.grid(False)


def box(x, y, w, h, title, lines, color, fs_t=10.2, fs_b=8.6, alpha=0.10,
        gap=4.4):
    for face, z in ((color, 1), ("none", 3)):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.4",
            linewidth=1.4, edgecolor=color, facecolor=face,
            alpha=(alpha if face != "none" else 1.0), zorder=z))
    ax.text(x + w / 2, y + h - 2.2, title, ha="center", va="top",
            fontsize=fs_t, color=color, fontweight="600", zorder=4)
    ax.text(x + w / 2, y + h - gap - 1.4, "\n".join(lines), ha="center",
            va="top", fontsize=fs_b, color=INK, linespacing=1.62, zorder=4)


def plain(x, y, w, h, lines, color, fs=9.4, alpha=0.09):
    for face, z in ((color, 1), ("none", 3)):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.0",
            linewidth=1.4, edgecolor=color, facecolor=face,
            alpha=(alpha if face != "none" else 1.0), zorder=z))
    ax.text(x + w / 2, y + h / 2, "\n".join(lines), ha="center", va="center",
            fontsize=fs, color=INK, linespacing=1.5, zorder=4)


def arrow(x1, y1, x2, y2, color=MUTED, style="-|>", rad=0.0, lw=1.3):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle=style, mutation_scale=13,
        linewidth=lw, color=color, zorder=2,
        connectionstyle=f"arc3,rad={rad}", shrinkA=1, shrinkB=1))


# ------------------------------------------------------- title
ax.text(50, 99.0, "G7  ·  classical statistical inference:  "
        r"$\theta$ is a fixed unknown constant",
        ha="center", va="top", fontsize=13.0, color=INK, fontweight="600")

# ------------------------------------------------------- top band: L23 slide 2
BY = 79.0          # baseline of the block-diagram row
ax.text(3, 93.6, "the classical setup   (L23 slide 2; B&T §9.1, its Figure 9.1)",
        ha="left", va="center", fontsize=10.2, color=RED, fontweight="600")

arrow(24, 90.2, 24, 85.6, color=RED, lw=1.5)
ax.text(25.4, 88.0, r"$\theta$  —  not a random variable", ha="left",
        va="center", fontsize=10.0, color=RED)

arrow(4, BY, 14.5, BY, color=MUTED, lw=1.5)
plain(15, BY - 4.6, 18, 9.2, [r"$p_X(x;\theta)$"], RED, fs=11.5)
ax.text(24, BY - 5.3, "one model per $\\theta$", ha="center", va="top",
        fontsize=8.4, color=MUTED)

arrow(34.2, BY, 45.5, BY, color=MUTED, lw=1.5)
ax.text(39.8, BY + 1.4, r"$X$", ha="center", va="bottom", fontsize=11,
        color=INK)
ax.text(39.8, BY - 1.6, "data", ha="center", va="top", fontsize=8.4,
        color=MUTED)

plain(46, BY - 4.6, 17, 9.2, ["Estimator", "or test"], MUTED, fs=10.0)

arrow(63.6, BY, 75, BY, color=MUTED, lw=1.5)
ax.text(69.3, BY + 1.4, r"$\hat\Theta$", ha="center", va="bottom",
        fontsize=11.5, color=BLUE)
ax.text(69.3, BY - 1.6, "random", ha="center", va="top", fontsize=8.4,
        color=MUTED)

ax.text(99, BY, "no prior, no posterior;\n"
        "every question is a probability\n"
        r"question about $X$, for each fixed $\theta$",
        ha="right", va="center", fontsize=9.0, color=MUTED, linespacing=1.5)

ax.plot([3, 99], [70.4, 70.4], color="#e1e0d9", lw=1.2, zorder=0)

# ------------------------------------------------------- two branches
ax.text(26, 67.1, r"$\theta$ ranges over a continuum  →  ESTIMATION",
        ha="center", va="center", fontsize=10.0, color=BLUE,
        fontweight="600")
ax.text(77, 67.1, r"$\theta \in \{H_0,H_1\}$  →  TESTING",
        ha="center", va="center", fontsize=10.0, color=PURPLE,
        fontweight="600")

arrow(50.0, 74.0, 45.0, 66.4, color=BLUE, rad=0.12)
arrow(59.0, 74.0, 63.0, 66.4, color=PURPLE, rad=-0.12)

box(2, 52.0, 49, 13.2, "§1   estimators, bias, consistency, CIs   (L23, rec23)",
    [r"$\hat\Theta_n=g(X_1,\dots,X_n)$ is a random variable",
     r"bias $\mathbf{E}[\hat\Theta_n]-\theta$ — MSE = var + bias$^2$",
     r"sample mean — $\hat\Theta_n\pm z\sigma/\sqrt{n}$"],
    BLUE, gap=3.6)

box(2, 35.4, 49, 13.2, "§2   maximum likelihood   (L24, rec23, rec24)",
    [r"$\hat\theta_{\mathsf{ML}}=\arg\max_\theta\, p_X(x;\theta)$",
     "log-likelihood, i.i.d. products, invariance",
     "the classical cousin of Bayesian MAP (G6 §3)"],
    ORANGE, gap=3.6)

box(2, 18.8, 49, 13.2, "§3   linear regression   (L24)",
    [r"data pairs $(x_i,y_i)$, fit $y\approx\theta_0+\theta_1 x$",
     "least squares = ML under Gaussian noise",
     "the estimate is a formula in the data"],
    GREEN, gap=3.6)

box(54, 33.0, 44, 32.2, "§4   binary hypothesis testing   (L25)",
    [r"$H_0:\ X\sim p_X(x;H_0)$",
     r"$H_1:\ X\sim p_X(x;H_1)$", "",
     "two error types:",
     "false rejection  ·  false acceptance",
     "",
     r"likelihood ratio test:  reject $H_0$ when",
     r"$L(x)=\dfrac{p_X(x;H_1)}{p_X(x;H_0)}>\xi$", "",
     r"choose $\xi$ to fix the false-rejection rate"],
    PURPLE, gap=4.2, fs_b=8.6)

arrow(26.5, 51.4, 26.5, 49.2, color=ORANGE)
arrow(26.5, 34.8, 26.5, 32.6, color=GREEN)

box(14, 1.2, 72, 13.2, "§5   synthesis  ·  and the G1 → G7 course finale",
    ["classical or Bayesian? which estimator? which test?",
     "the whole arc: sample space → random variables → limit theorems → inference",
     "L23–L25, rec23–rec24, B&T Chapter 9"],
    GOLD)

arrow(26.5, 17.8, 40, 15.2, color=GOLD, rad=-0.10)
arrow(74.0, 32.2, 62, 15.2, color=GOLD, rad=0.12)

# link back to G6
ax.text(88, 25.0, "G6 §3–§4 was the\nother philosophy:\n"
        r"a prior on $\Theta$, then a posterior",
        ha="center", va="center", fontsize=8.6, color=MUTED, linespacing=1.5)

fig.savefig(IMG + "g7_s0_map.png", dpi=150)
plt.close(fig)
print("wrote", IMG + "g7_s0_map.png")
