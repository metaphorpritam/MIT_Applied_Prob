# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Fig. 0.1 — concept map of the four G1 topics and how they feed each other."""
import io
import sys

sys.path.insert(0, "d:/Python-UV/MIT_Applied_Prob/notes/_build")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from mpl_style import PAL, INK, MUTED, setup, diagram_ax

plt, _ = setup()

OUT = "d:/Python-UV/MIT_Applied_Prob/notes/img/g1_s0_roadmap.png"

fig, ax = plt.subplots(figsize=(9.0, 7.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
diagram_ax(ax)


def box(x, y, w, h, title, sub, color, fill):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.10,rounding_size=0.14",
                                linewidth=1.6, edgecolor=color, facecolor=fill))
    ax.text(x, y + h / 2 - 0.34, title, ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=INK)
    ax.text(x, y - 0.16, sub, ha="center", va="center",
            fontsize=8.8, color=MUTED, linespacing=1.5)


def arrow(p, q, color, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=13,
                                 linewidth=1.4, color=color,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=2, shrinkB=2))


W, H = 4.0, 1.30
XL = 3.0          # main chain column
XR = 7.7          # counting column

box(XL, 7.0, W, H, "§1  Models and axioms",
    "sample space $\\Omega$  +  probability law $\\mathbf{P}$\nnonnegativity · normalization · additivity",
    PAL[0], "#eaf2fc")
box(XL, 4.9, W, H, "§2  Conditioning",
    "$\\mathbf{P}(A\\,|\\,B)$ · multiplication rule\ntotal probability · Bayes' rule",
    PAL[1], "#fdeee7")
box(XL, 2.8, W, H, "§3  Independence",
    "$\\mathbf{P}(A\\cap B)=\\mathbf{P}(A)\\mathbf{P}(B)$\nindependent trials · pairwise vs. full",
    PAL[2], "#e7f6f0")
box(XR, 4.9, 3.5, H, "§4  Counting",
    "permutations · combinations\npartitions · binomial",
    PAL[3], "#fdf3dc")
box(XL, 0.75, W, 1.0, "next note G2  →  Random variables",
    "$X:\\Omega\\to\\mathbb{R}$, PMFs, expectation", MUTED, "#f2f1ec")

# main chain
arrow((XL, 7.0 - H / 2 - 0.10), (XL, 4.9 + H / 2 + 0.10), PAL[0])
ax.text(XL + 0.15, 5.98, "restrict $\\Omega$ to $B$:\na new, legitimate model",
        ha="left", va="center", fontsize=8.5, color=MUTED, linespacing=1.4)

arrow((XL, 4.9 - H / 2 - 0.10), (XL, 2.8 + H / 2 + 0.10), PAL[1])
ax.text(XL + 0.15, 3.88, "special case\n$\\mathbf{P}(A\\,|\\,B)=\\mathbf{P}(A)$",
        ha="left", va="center", fontsize=8.5, color=MUTED, linespacing=1.4)

arrow((XL, 2.8 - H / 2 - 0.10), (XL, 0.75 + 0.5 + 0.10), MUTED)

# counting feeds the uniform law (up to §1) and binomial probabilities (§3)
arrow((XR, 4.9 + H / 2 + 0.10), (XL + W / 2 + 0.15, 7.0 - 0.15), PAL[3], rad=0.22)
ax.text(6.85, 6.72, "equally likely outcomes:\n$\\mathbf{P}(A)=|A|/|\\Omega|$",
        ha="center", va="center", fontsize=8.5, color=MUTED, linespacing=1.4)

arrow((XR, 4.9 - H / 2 - 0.10), (XL + W / 2 + 0.15, 2.8 + 0.15), PAL[2], rad=-0.22)
ax.text(7.05, 2.80, "count the sequences:\nbinomial $\\binom{n}{k}p^k(1-p)^{n-k}$",
        ha="center", va="center", fontsize=8.5, color=MUTED, linespacing=1.4)

ax.text(5.0, 7.85, "How the four topics of this note fit together",
        ha="center", va="center", fontsize=11.5, fontweight="bold", color=INK)

fig.savefig(OUT, dpi=150)
print("wrote", OUT)
