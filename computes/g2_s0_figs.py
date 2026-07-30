# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Figures for G2 section 0.

Fig. 0.1  g2_s0_rv_function : a random variable as a function Omega -> R
          (L05 slide 2), on the two-fair-coin-tosses sample space.
Fig. 0.2  g2_s0_roadmap     : how sections 1-5 of this note chain together
          (built from the lecture outlines L05 slide 1, L06 slide 1, L07 slide 1).
"""
import io
import sys

sys.path.insert(0, "d:/Python-UV/MIT_Applied_Prob/notes/_build")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch
from mpl_style import PAL, INK, MUTED, AXIS_C, setup, diagram_ax

plt, _ = setup()
IMG = "d:/Python-UV/MIT_Applied_Prob/notes/img/"

# ---------------------------------------------------------------- Fig. 0.1 --
fig, ax = plt.subplots(figsize=(9.6, 4.8))
ax.set_xlim(0, 12.0)
ax.set_ylim(0, 6.0)
diagram_ax(ax)

# sample space blob (wide ellipse across the top)
ax.add_patch(Ellipse((6.0, 4.35), 9.9, 2.30, linewidth=1.6,
                     edgecolor=PAL[0], facecolor="#eaf2fc"))
ax.text(6.0, 5.72, r"sample space  $\Omega$  —  two independent tosses of a fair coin",
        ha="center", va="center", fontsize=10.2, fontweight="bold", color=PAL[0])

outcomes = [("TT", 2.35, 0), ("TH", 4.75, 1), ("HT", 7.15, 1), ("HH", 9.60, 2)]
OY = 4.35
for name, x, _v in outcomes:
    ax.plot([x], [OY], marker="o", markersize=6.5, color=PAL[0], zorder=3)
    ax.text(x, OY + 0.52, name, ha="center", va="center", fontsize=10.5,
            color=INK, fontfamily="monospace")
    ax.text(x, OY - 0.52, r"$1/4$", ha="center", va="center", fontsize=8.6,
            color=MUTED)

# real line
LY = 1.55
ax.annotate("", xy=(11.55, LY), xytext=(1.15, LY),
            arrowprops=dict(arrowstyle="-|>", color=AXIS_C, linewidth=1.6))
ax.text(11.55, LY + 0.42, r"$\mathbb{R}$", ha="center", va="center",
        fontsize=11, color=MUTED)

vx = {0: 2.35, 1: 5.95, 2: 9.60}
for v, x in vx.items():
    ax.plot([x], [LY], marker="|", markersize=14, markeredgewidth=2.0,
            color=INK, zorder=3)
    ax.text(x, LY - 0.48, f"${v}$", ha="center", va="center", fontsize=11,
            color=INK)

# arrows outcome -> value
for name, x, v in outcomes:
    ax.add_patch(FancyArrowPatch((x, OY - 0.80), (vx[v], LY + 0.26),
                                 arrowstyle="-|>", mutation_scale=11,
                                 linewidth=1.3, color=PAL[1],
                                 shrinkA=3, shrinkB=4))

ax.text(1.05, 3.00, r"$X$", ha="center", va="center", fontsize=13,
        fontweight="bold", color=PAL[1])
ax.text(1.05, 2.45, "number\nof heads", ha="center", va="center", fontsize=8.4,
        color=PAL[1], linespacing=1.4)
ax.text(5.95, 0.55,
        r"two outcomes land on $1$:  $p_X(1)=\frac{1}{4}+\frac{1}{4}=\frac{1}{2}$",
        ha="center", va="center", fontsize=9.2, color=MUTED)
ax.text(9.85, 2.95, "the random variable\nis the whole assignment\nof arrows",
        ha="left", va="center", fontsize=8.4, color=MUTED, linespacing=1.4)

fig.savefig(IMG + "g2_s0_rv_function.png", dpi=150)
plt.close(fig)
print("wrote g2_s0_rv_function.png")

# ---------------------------------------------------------------- Fig. 0.2 --
fig, ax = plt.subplots(figsize=(7.8, 10.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 13.0)
diagram_ax(ax)


def box(x, y, w, h, title, sub, color, fill):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.10,rounding_size=0.14",
                                linewidth=1.6, edgecolor=color, facecolor=fill))
    ax.text(x, y + h / 2 - 0.30, title, ha="center", va="center",
            fontsize=10.2, fontweight="bold", color=INK)
    ax.text(x, y - 0.17, sub, ha="center", va="center",
            fontsize=8.6, color=MUTED, linespacing=1.5)


def arrow(p, q, color):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=13,
                                 linewidth=1.4, color=color,
                                 shrinkA=2, shrinkB=2))


W, X = 6.4, 3.4
# §3 now carries three topic lines, so it gets a taller box; the others keep
# the two-line height. Centres are derived from the heights so the vertical
# gaps (and hence the link labels) stay uniform.
hs = [1.30, 1.30, 1.78, 1.30, 1.30]
GAP, TOP = 0.80, 11.75
ys = []
_edge = TOP
for _h in hs:
    ys.append(_edge - _h / 2)
    _edge -= _h + GAP
specs = [
    ("§1  Random variables and PMFs",
     r"$X:\Omega\to\mathbb{R}$,  $p_X(x)=\mathbf{P}(X=x)$" "\nBernoulli · uniform · binomial · geometric",
     PAL[0], "#eaf2fc"),
    ("§2  Expectation",
     r"$\mathbb{E}[X]$ = weighted average of the values" "\n" r"expected value rule for $g(X)$ · $\mathbb{E}[\alpha X+\beta]=\alpha\mathbb{E}[X]+\beta$",
     PAL[1], "#fdeee7"),
    ("§3  Variance, conditioning, geometric",
     r"$\operatorname{var}(X)=\mathbb{E}[X^2]-(\mathbb{E}[X])^2$ · $\operatorname{var}(\alpha X+\beta)=\alpha^2\operatorname{var}(X)$"
     "\n" r"$p_{X\mid A}(x)$ · total expectation theorem"
     "\ngeometric r.v. and memorylessness",
     PAL[2], "#e7f6f0"),
    ("§4  Joint PMFs, several random variables",
     r"joint $p_{X,Y}(x,y)$ · marginals · independence" "\n" r"linearity of $\mathbb{E}$ · variance of a sum · indicators",
     PAL[3], "#fdf3dc"),
    ("§5  Synthesis: the discrete toolbox",
     "PMF zoo · identity table · top gotchas\nbridge to G3",
     PAL[4], "#fdeef4"),
]
for y, h, (t, s, c, f) in zip(ys, hs, specs):
    box(X, y, W, h, t, s, c, f)

links = [
    "attach numbers $\\Rightarrow$ average them",
    "measure the spread, then re-average\nunder partial information",
    "one r.v. is never enough",
    "collect the toolbox on one page",
]
for i, txt in enumerate(links):
    arrow((X, ys[i] - hs[i] / 2 - 0.12), (X, ys[i + 1] + hs[i + 1] / 2 + 0.12),
          MUTED)
    ax.text(X + 0.25, (ys[i] - hs[i] / 2 + ys[i + 1] + hs[i + 1] / 2) / 2, txt,
            ha="left", va="center", fontsize=8.4, color=MUTED, linespacing=1.35)

# context arrows: G1 behind, continuous r.v.'s ahead
CT, CB = 12.35, 0.45
ax.add_patch(FancyBboxPatch((X - W / 2, CT - 0.32), W, 0.64,
                            boxstyle="round,pad=0.08,rounding_size=0.12",
                            linewidth=1.3, edgecolor=MUTED, facecolor="#f2f1ec"))
ax.text(X, CT, "note G1:  $(\\Omega,\\mathbf{P})$, conditioning, independence, counting",
        ha="center", va="center", fontsize=8.6, color=MUTED)
arrow((X, CT - 0.44), (X, ys[0] + hs[0] / 2 + 0.12), MUTED)

ax.add_patch(FancyBboxPatch((X - W / 2, CB - 0.32), W, 0.64,
                            boxstyle="round,pad=0.08,rounding_size=0.12",
                            linewidth=1.3, edgecolor=MUTED, facecolor="#f2f1ec"))
ax.text(X, CB, "next:  continuous r.v.'s — PDFs replace PMFs, $\\int$ replaces $\\sum$",
        ha="center", va="center", fontsize=8.6, color=MUTED)
arrow((X, ys[4] - hs[4] / 2 - 0.12), (X, CB + 0.44), MUTED)

fig.savefig(IMG + "g2_s0_roadmap.png", dpi=150)
plt.close(fig)
print("wrote g2_s0_roadmap.png")
