# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""G1 §5 figure: concept map of how the G1 tools compose."""
import io
import sys

sys.path.insert(0, r"d:/Python-UV/MIT_Applied_Prob/notes/_build")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from mpl_style import setup, PAL, INK, MUTED  # noqa: E402

plt, _ = setup()
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

OUT = r"d:/Python-UV/MIT_Applied_Prob/notes/img/g1_s5_conceptmap.png"
ARROW_C = "#7a7973"

fig, ax = plt.subplots(figsize=(11.6, 7.6))
ax.set_xlim(0, 100)
ax.set_ylim(2, 106)
ax.axis("off")
ax.grid(False)

BOXES = {}


def box(key, x, y, w, h, title, sub, edge, fill):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.5,rounding_size=1.2",
                                linewidth=1.4, edgecolor=edge, facecolor=fill,
                                zorder=3))
    ax.text(x, y + h * 0.22, title, ha="center", va="center", fontsize=9.4,
            fontweight="600", color=INK, zorder=4)
    ax.text(x, y - h * 0.24, sub, ha="center", va="center", fontsize=8.7,
            color=MUTED, zorder=4)
    BOXES[key] = (x, y, w, h)


def anchor(key, side):
    x, y, w, h = BOXES[key]
    return {"top": (x, y + h / 2), "bottom": (x, y - h / 2),
            "left": (x - w / 2, y), "right": (x + w / 2, y)}[side]


def arrow(a, b, sa="bottom", sb="top", label=None, lx=0, ly=0, dashed=False):
    p, q = anchor(a, sa), anchor(b, sb)
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12,
                                 linewidth=1.3, color=ARROW_C, zorder=2,
                                 linestyle="--" if dashed else "-",
                                 # The boxes are drawn with boxstyle pad=0.5 (data
                                 # units) and zorder 3, so a connector that stops at
                                 # the nominal box edge has its arrowhead hidden
                                 # under the visible border. Shrink enough (in
                                 # points) that every head lands clear of the box.
                                 shrinkA=5.0, shrinkB=8.0))
    if label:
        ax.text((p[0] + q[0]) / 2 + lx, (p[1] + q[1]) / 2 + ly, label,
                ha="center", va="center", fontsize=7.8, color=ARROW_C,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"),
                zorder=5)


BLUE, ORANGE, GREEN, GOLD, PURPLE = PAL[0], PAL[1], PAL[2], PAL[3], PAL[6]
LB, LO, LG, LGD, LP = "#eaf2fc", "#fdeee7", "#e8f7f1", "#fdf4de", "#eeecf8"

# ---------------------------------------------------------------- layout
box("model", 50, 92, 64, 10, "Probabilistic model   (L01 slides 4-7)",
    r"sample space $\Omega$: mutually exclusive, collectively exhaustive  $+$  probability law",
    BLUE, LB)
box("ax", 50, 76, 64, 10, "The axioms   (L01 slide 7, $\\S$1.2)",
    r"$\mathbf{P}(A)\geq 0$ ;  $\mathbf{P}(\Omega)=1$ ;  "
    r"$\mathbf{P}(A_1\cup A_2\cup\cdots)=\mathbf{P}(A_1)+\mathbf{P}(A_2)+\cdots$ (disjoint)",
    BLUE, LB)

box("cond", 26, 60, 40, 10, "Conditional probability   (L02 s3)",
    r"$\mathbf{P}(A\mid B)=\mathbf{P}(A\cap B)\,/\,\mathbf{P}(B)$,   $\mathbf{P}(B)>0$",
    ORANGE, LO)
box("unif", 80, 60, 32, 10, "Uniform law   (L01 s9-10)",
    r"$\mathbf{P}(A)=|A|\,/\,|\Omega|$   (or area)", GREEN, LG)

box("mult", 26, 45, 40, 10, "Multiplication rule   (L02 s6)",
    r"$\mathbf{P}(A\cap B\cap C)=\mathbf{P}(A)\mathbf{P}(B\mid A)\mathbf{P}(C\mid A\cap B)$",
    ORANGE, LO)
box("count", 80, 45, 32, 10, "Counting   (L04 s3-5, $\\S$1.6)",
    r"$n_1\cdots n_r$ ;  $n!$ ;  $n!/(n-k)!$ ;  $\binom{n}{k}$", GREEN, LG)

box("tpt", 21, 29, 34, 10, "Total probability   (L02 s7)",
    r"$\mathbf{P}(B)=\sum_i \mathbf{P}(A_i)\mathbf{P}(B\mid A_i)$", ORANGE, LO)
box("indep", 57, 29, 26, 10, "Independence   (L03 s3)",
    r"$\mathbf{P}(A\cap B)=\mathbf{P}(A)\mathbf{P}(B)$", PURPLE, LP)
box("binom", 88, 29, 20, 10, "Binomial   (L04 s6)",
    r"$\binom{n}{k}p^k(1-p)^{n-k}$", GOLD, LGD)

box("bayes", 22, 12, 40, 10, "Bayes' rule   (L02 s8)",
    r"$\mathbf{P}(A_i\mid B)=\mathbf{P}(A_i)\mathbf{P}(B\mid A_i)\,/\,\mathbf{P}(B)$",
    ORANGE, LO)
box("g2", 72, 12, 40, 10, "Next  —  G2: random variables",
    r"PMF $p_X(x)$,  $\mathbb{E}[X]$,  $\operatorname{var}(X)$", BLUE, LB)

# ---------------------------------------------------------------- arrows
arrow("model", "ax")
arrow("ax", "cond")
arrow("ax", "unif")
arrow("cond", "mult", label="rearrange", lx=-10)
arrow("unif", "count", label="probability = counting", lx=-13)
arrow("mult", "tpt", label="sum over a partition", lx=-12)
arrow("cond", "indep", sa="right", sb="top", label="special case", lx=4, ly=1.5)
arrow("tpt", "bayes")
arrow("count", "binom", sa="bottom", sb="top", label="$k$-head sequences", lx=-3.5, ly=1.2)
arrow("indep", "binom", sa="right", sb="left")
arrow("bayes", "g2", sa="right", sb="left")
arrow("binom", "g2", sa="bottom", sb="top", dashed=True, label="becomes a PMF", lx=12)

ax.text(50, 104, "How the G1 tools compose", ha="center", va="top",
        fontsize=13, fontweight="600", color=INK)

fig.savefig(OUT, dpi=150)
print("wrote", OUT)
