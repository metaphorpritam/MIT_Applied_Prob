# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for G6 section 5 (synthesis + bridge).

Fig 5.1  g6_s5_whichbound   - decision flowchart: Markov / Chebyshev / WLLN / CLT
Fig 5.2  g6_s5_tightness    - how loose the bounds are, and what that costs a pollster
Fig 5.3  g6_s5_whichest     - decision flowchart: posterior / MAP / LMS / linear LMS
"""
import io
import sys

import numpy as np

sys.path.insert(0, "d:/Python-UV/MIT_Applied_Prob/notes/_build")
from mpl_style import PAL, INK, MUTED, GRID_C, diagram_ax, setup  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
plt, _ = setup()

IMG = "d:/Python-UV/MIT_Applied_Prob/notes/img/"


def box(ax, x, y, w, h, text, fc="white", ec=None, fs=8.0, weight="normal"):
    ec = ec or GRID_C
    ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, facecolor=fc,
                               edgecolor=ec, linewidth=1.2, zorder=2,
                               joinstyle="round"))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
            zorder=3, linespacing=1.5, fontweight=weight)


def arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=1.2,
                                shrinkA=0, shrinkB=2), zorder=1)


def flowchart(path, root, mid_left, mid_right, leaves, title):
    """4-leaf two-level tree; leaves = list of 4 strings (3 under left, 1 under right)."""
    fig, ax = plt.subplots(figsize=(9.4, 5.0))
    diagram_ax(ax)
    ax.set_aspect("auto")
    ax.set_xlim(-0.2, 12.2)
    ax.set_ylim(1.4, 9.4)

    box(ax, 6.0, 8.5, 7.6, 0.9, root, fc="#f4f6fa", fs=9.5, weight="bold")
    box(ax, 3.0, 6.4, 4.6, 1.0, mid_left, fc="#eef4fb", fs=8.8)
    box(ax, 9.0, 6.4, 4.6, 1.0, mid_right, fc="#fdf1ea", fs=8.8)
    arrow(ax, 5.2, 8.05, 3.0, 6.95)
    arrow(ax, 6.8, 8.05, 9.0, 6.95)

    xs = [1.6, 4.6, 7.6, 10.6]
    for i, (x, txt) in enumerate(zip(xs, leaves)):
        box(ax, x, 3.3, 2.95, 2.5, txt, fs=7.0,
            ec=PAL[0] if i < 3 else PAL[1])
        arrow(ax, 3.0 if i < 3 else 9.0, 5.9, x, 4.6)
    ax.set_title(title, fontsize=11, color=INK, pad=6)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print("wrote", path)


# ------------------------------------------------------------------ Fig 5.1
flowchart(
    IMG + "g6_s5_whichbound.png",
    root="You need $\\mathbf{P}$(something is far from its mean)",
    mid_left="A GUARANTEE, valid for every $n$\n(an upper bound, never wrong)",
    mid_right="A NUMBER, $n$ large\n(an approximation, can be wrong)",
    leaves=[
        "MARKOV\n$\\mathbf{P}(X\\geq a)\\leq \\mathbb{E}[X]/a$\n\nneeds: $X\\geq 0$\nand the mean only\n\nB&T \u00a75.1 (book only)",
        "CHEBYSHEV\n$\\mathbf{P}(|X-\\mu|\\geq c)\\leq \\sigma^2/c^2$\n\nneeds: mean and\nvariance\n\nB&T \u00a75.1 / L19 slide 2",
        "WLLN\n$\\mathbf{P}(|M_n-\\mu|\\geq\\epsilon)\\leq\\frac{\\sigma^2}{n\\epsilon^2}\\to 0$\n\nneeds: i.i.d., finite\nvariance; gives a usable $n$\n\nB&T \u00a75.2 / L19 slide 5",
        "CLT\n$\\mathbf{P}(S_n\\leq s)\\approx\\Phi\\!\\left(\\frac{s-n\\mu}{\\sigma\\sqrt{n}}\\right)$\n\nneeds: i.i.d., finite\nvariance, $n$ large\n\nB&T \u00a75.4 / L19 slide 8",
    ],
    title="Which inequality or limit theorem?",
)

# ------------------------------------------------------------------ Fig 5.3
flowchart(
    IMG + "g6_s5_whichest.png",
    root="Unknown $\\Theta$ with prior, data $X=x$ observed",
    mid_left="The posterior is available\n(you can do the Bayes integral)",
    mid_right="Only means, variances\nand $\\mathrm{cov}(X,\\Theta)$ are known",
    leaves=[
        "FULL POSTERIOR\n$f_{\\Theta|X}(\\theta\\,|\\,x)$\n\nthe complete answer;\nreport spread too\n\nB&T \u00a78.1 / L21 slide 3",
        "MAP\n$\\hat\\theta=\\arg\\max_\\theta f_{\\Theta|X}(\\theta|x)$\n\nminimizes $\\mathbf{P}$(error);\nuse for discrete $\\Theta$\n\nB&T \u00a78.2 / L21 slide 5",
        "LMS\n$\\hat\\Theta=\\mathbb{E}[\\Theta\\,|\\,X]$\n\nminimizes $\\mathbb{E}[(\\Theta-\\hat\\Theta)^2]$;\nMSE $=\\mathbb{E}[\\mathrm{var}(\\Theta|X)]$\n\nB&T \u00a78.3 / L22 slide 1",
        "LINEAR LMS\n$\\hat\\Theta_L=\\mathbb{E}[\\Theta]+\\frac{\\mathrm{cov}(X,\\Theta)}{\\mathrm{var}(X)}(X-\\mathbb{E}[X])$\n\nMSE $=(1-\\rho^2)\\,\\mathrm{var}(\\Theta)$\n\nB&T \u00a78.4 / L22 slide 5",
    ],
    title="Which Bayesian estimator?",
)

# ------------------------------------------------------------------ Fig 5.2
fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 4.0),
                               gridspec_kw=dict(width_ratios=[1.35, 1.0], wspace=0.32))

a = np.linspace(1.6, 6.0, 400)
axL.semilogy(a, 1.0 / a, color=PAL[1], label="Markov  $1/a$")
ac = a[a > 2.0]
axL.semilogy(ac, 1.0 / (ac - 1) ** 2, color=PAL[3],
             label=r"Chebyshev  $1/(a-1)^2$")
axL.semilogy(a, np.exp(-a), color=PAL[0], label=r"exact  $e^{-a}$")
for x0 in (4.0,):
    axL.plot([x0, x0], [np.exp(-x0), 1.0 / x0], color=MUTED, lw=1.0, ls=":")
    axL.annotate(f"Markov at $a=4$: {1.0/x0:.2f}\nvs truth {np.exp(-x0):.4f}"
                 f"  ({(1.0/x0)/np.exp(-x0):.0f}$\\times$)",
                 xy=(x0, np.sqrt(np.exp(-x0) / x0)), xytext=(4.2, 0.034),
                 va="top", fontsize=8.5, color=MUTED)
axL.set_xlabel("threshold $a$")
axL.set_ylabel(r"$\mathbf{P}(X\geq a)$")
axL.set_title(r"Bounds vs truth for $X\sim\mathrm{Exp}(1)$  ($\mu=\sigma=1$)")
axL.set_ylim(2e-3, 1.3)
axL.legend(loc="lower left")

names = ["Chebyshev\n(WLLN bound)", "CLT\napproximation"]
vals = [50000, 9604]
bars = axR.bar(names, vals, color=[PAL[3], PAL[0]], width=0.55)
for b, v in zip(bars, vals):
    axR.text(b.get_x() + b.get_width() / 2, v + 1400, f"$n={v:,}$",
             ha="center", fontsize=10, color=INK)
axR.set_ylim(0, 59000)
axR.set_ylabel("respondents needed")
axR.set_title("Poll: $\\pm1\\%$ error, $95\\%$ confidence")
axR.grid(axis="x", visible=False)
axR.annotate("5.2$\\times$ the cost\nfor the same promise",
             xy=(0.5, 30000), ha="center", fontsize=9, color=MUTED)

fig.savefig(IMG + "g6_s5_tightness.png", dpi=150)
plt.close(fig)
print("wrote", IMG + "g6_s5_tightness.png")
