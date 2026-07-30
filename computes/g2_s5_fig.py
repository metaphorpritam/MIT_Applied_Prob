# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""G2 section 5 figures: (1) concept map of the discrete toolbox,
(2) decision flowchart for picking the right named PMF / tool."""
import io
import sys

sys.path.insert(0, r"d:/Python-UV/MIT_Applied_Prob/notes/_build")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from mpl_style import setup, PAL, INK, MUTED  # noqa: E402

plt, _ = setup()
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon  # noqa: E402

IMG = r"d:/Python-UV/MIT_Applied_Prob/notes/img/"
ARROW_C = "#7a7973"
BLUE, ORANGE, GREEN, GOLD, PURPLE, RED = PAL[0], PAL[1], PAL[2], PAL[3], PAL[6], PAL[7]
LB, LO, LG, LGD, LP, LR = "#eaf2fc", "#fdeee7", "#e8f7f1", "#fdf4de", "#eeecf8", "#fdecea"


def canvas(figsize, xlim, ylim):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    ax.grid(False)
    return fig, ax, {}


def helpers(ax, boxes):
    def box(key, x, y, w, h, title, sub, edge, fill, tfs=9.4, sfs=8.5):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.4,rounding_size=1.0",
                                    linewidth=1.4, edgecolor=edge, facecolor=fill,
                                    zorder=3))
        if sub:
            ax.text(x, y + h * 0.23, title, ha="center", va="center", fontsize=tfs,
                    fontweight="600", color=INK, zorder=4)
            ax.text(x, y - h * 0.25, sub, ha="center", va="center", fontsize=sfs,
                    color=MUTED, zorder=4)
        else:
            ax.text(x, y, title, ha="center", va="center", fontsize=tfs,
                    fontweight="600", color=INK, zorder=4)
        boxes[key] = (x, y, w, h)

    def anchor(key, side):
        x, y, w, h = boxes[key]
        return {"top": (x, y + h / 2), "bottom": (x, y - h / 2),
                "left": (x - w / 2, y), "right": (x + w / 2, y)}[side]

    def raw(p, q, label=None, lx=0, ly=0, dashed=False, rad=0.0):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12,
                                     linewidth=1.3, color=ARROW_C, zorder=2,
                                     linestyle="--" if dashed else "-",
                                     connectionstyle=f"arc3,rad={rad}",
                                     shrinkA=1.0, shrinkB=1.0))
        if label:
            ax.text((p[0] + q[0]) / 2 + lx, (p[1] + q[1]) / 2 + ly, label,
                    ha="center", va="center", fontsize=7.8, color=ARROW_C,
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"),
                    zorder=5)

    def arrow(a, b, sa="bottom", sb="top", **kw):
        raw(anchor(a, sa), anchor(b, sb), **kw)

    return box, arrow, raw, anchor


# =====================================================================
# Figure 1 — concept map (three parallel chains descending from the PMF)
# =====================================================================
fig, ax, B = canvas((12.4, 8.4), (0, 110), (0, 112))
box, arrow, raw, anchor = helpers(ax, B)

box("rv", 55, 102, 56, 9,
    r"Random variable   $X:\Omega\rightarrow\mathbb{R}$   (L05 s2)",
    r"a number attached to every outcome; the randomness sits in $\omega$, not in $X$",
    BLUE, LB)
box("pmf", 55, 87, 56, 9, r"PMF   $p_X(x)=\mathbf{P}(X=x)$   (L05 s3)",
    r"$p_X(x)\geq 0$,   $\sum_x p_X(x)=1$", BLUE, LB)
box("zoo", 13, 87, 24, 9, "Named PMFs (L05 s3, s5)",
    "Bernoulli · uniform\nbinomial · geometric", GOLD, LGD, tfs=8.8, sfs=8.2)

box("cond", 18, 70, 32, 9, "Conditional PMF   (L06 s5)",
    r"$p_{X|A}(x)$,   $\mathbb{E}[X\mid A]$", GREEN, LG, tfs=9.0)
box("exp", 55, 70, 32, 9, "Expectation   (L05 s6)",
    r"$\mathbb{E}[X]=\sum_x x\,p_X(x)$", ORANGE, LO, tfs=9.0)
box("joint", 92, 70, 32, 9, "Joint PMF   (L06 s8)",
    r"$p_{X,Y}(x,y)$,   $p_X(x)=\sum_y p_{X,Y}$", GREEN, LG, tfs=9.0, sfs=8.2)

box("tot", 18, 55, 32, 9, "Total expectation   (L06 s7)",
    r"$\mathbb{E}[X]=\sum_i \mathbf{P}(A_i)\mathbb{E}[X\mid A_i]$", GREEN, LG,
    tfs=9.0, sfs=8.2)
box("evr", 55, 55, 32, 9, "Expected-value rule   (L05 s7)",
    r"$\mathbb{E}[g(X)]=\sum_x g(x)\,p_X(x)$", ORANGE, LO, tfs=9.0, sfs=8.2)
box("indep", 92, 55, 32, 9, "Independence   (L07 s3)",
    r"$p_{X,Y}=p_X\,p_Y$  for all $x,y$", PURPLE, LP, tfs=9.0, sfs=8.2)

box("var", 55, 40, 32, 9, "Variance   (L05 s8)",
    r"$\mathbb{E}[X^2]-(\mathbb{E}[X])^2$", RED, LR, tfs=9.0)
box("lsum", 92, 40, 32, 9, "Linearity & sums (L07 s4-s5)",
    r"$\mathbb{E}[X{+}Y]=\mathbb{E}[X]{+}\mathbb{E}[Y]$   (always)",
    ORANGE, LO, tfs=8.8, sfs=8.0)

box("ind2", 76, 25, 40, 9, "Indicator method   (L07 s6, s7)",
    r"$X=\sum_i X_i$,  $X_i\in\{0,1\}$   $\Rightarrow$   "
    r"$\mathbb{E}[X]=\sum_i\mathbf{P}(X_i{=}1)$", ORANGE, LO, tfs=9.0, sfs=8.0)

box("g3", 55, 9, 76, 9, "Next  —  G3: continuous random variables",
    r"$\sum_x\;\rightarrow\;\int dx$,     $p_X(x)\;\rightarrow\;f_X(x)$,     "
    r"$\mathbf{P}(X=x)=0$", BLUE, LB)

arrow("rv", "pmf",
      label=r"collect the outcomes with $X(\omega)=x$, add their probabilities (L05 s4)")
arrow("pmf", "zoo", sa="left", sb="right")
arrow("pmf", "cond", sa="bottom", sb="top", rad=0.0)
arrow("pmf", "exp")
arrow("pmf", "joint", sa="bottom", sb="top", rad=0.0)
arrow("cond", "tot", label="partition of $\\Omega$", lx=-9)
arrow("exp", "evr", label="$Y=g(X)$", lx=-7)
arrow("joint", "indep", label="factorization?", lx=-9)
arrow("evr", "var", label=r"$g(x)=(x-\mathbb{E}[X])^2$", lx=-9.5)
arrow("indep", "lsum")
arrow("lsum", "ind2", sa="bottom", sb="top", rad=0.1)
arrow("tot", "g3", sa="bottom", sb="left", rad=-0.12)
arrow("var", "g3")
arrow("ind2", "g3", sa="bottom", sb="right", rad=0.1)

ax.text(55, 111, "The discrete toolbox: how the G2 tools compose", ha="center",
        va="top", fontsize=13, fontweight="600", color=INK)
fig.savefig(IMG + "g2_s5_conceptmap.png", dpi=150)
print("wrote g2_s5_conceptmap.png")
plt.close(fig)

# =====================================================================
# Figure 2 — decision flowchart
# =====================================================================
fig, ax, B2 = canvas((11.6, 9.4), (0, 100), (0, 114))
box, arrow, raw, anchor = helpers(ax, B2)


def diamond(key, x, y, w, h, text, fs=9.0):
    ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2),
                          (x - w / 2, y)], closed=True, linewidth=1.4,
                         edgecolor=BLUE, facecolor=LB, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
            fontweight="600", zorder=4)
    B2[key] = (x, y, w, h)


box("start", 50, 102, 60, 7,
    "You have an experiment and a numerical quantity of interest", "", GREEN, LG,
    tfs=9.6)
diamond("q1", 50, 89, 50, 13,
        "Is the quantity a number attached\nto each outcome?")
box("notrv", 88, 89, 20, 9, "Stay in G1", "it is an event,\nnot a r.v.", MUTED,
    "#f2f1ec", tfs=9.0, sfs=8.0)
diamond("q2", 50, 72, 56, 13,
        "Does it come from one of the four\nstandard mechanisms?")

box("bern", 12.5, 56, 23, 11, "Bernoulli($p$)",
    "one trial, 0/1\n$\\mathbb{E}=p$,  var $=p(1{-}p)$", GOLD, LGD, tfs=9.0, sfs=8.0)
box("unif", 37.5, 56, 23, 11, "Uniform $\\{a,\\ldots,b\\}$",
    "no value preferred\n$\\mathbb{E}=(a{+}b)/2$", GOLD, LGD, tfs=9.0, sfs=8.0)
box("bino", 62.5, 56, 23, 11, "Binomial($n,p$)",
    "count successes in $n$\n$\\mathbb{E}=np$,  var $=np(1{-}p)$", GOLD, LGD,
    tfs=9.0, sfs=8.0)
box("geom", 87.5, 56, 23, 11, "Geometric($p$)",
    "wait for 1st success\n$\\mathbb{E}=1/p$,  var $=\\frac{1-p}{p^2}$", GOLD, LGD,
    tfs=9.0, sfs=8.0)

box("build", 50, 41, 62, 8, "Either way, you now hold a PMF $p_X(x)$",
    "if no family fits: list the outcomes with $X(\\omega)=x$ and add "
    "their probabilities (L05 s4)", GREEN, LG, tfs=9.4, sfs=8.2)

diamond("q3", 20, 18, 36, 16, "What is the\nquestion asking for?", fs=9.4)
box("mean", 70, 32, 52, 8, "a mean of a function of $X$",
    "expected-value rule $\\sum_x g(x)p_X(x)$ — never rebuild the PMF of $g(X)$",
    ORANGE, LO, tfs=9.0, sfs=8.0)
box("sum", 70, 23, 52, 8, "a mean of a sum of many pieces",
    "linearity + indicators; independence not needed", ORANGE, LO, tfs=9.0, sfs=8.0)
box("spread", 70, 14, 52, 8, "a spread",
    "$\\operatorname{var}(X)=\\mathbb{E}[X^2]-(\\mathbb{E}[X])^2$,  "
    "$\\sigma_X=\\sqrt{\\operatorname{var}(X)}$", RED, LR, tfs=9.0, sfs=8.0)
box("scen", 70, 5, 52, 8, "a mean you only know per scenario",
    "total expectation over a partition (L06 s7)", GREEN, LG, tfs=9.0, sfs=8.0)

arrow("start", "q1")
arrow("q1", "notrv", sa="right", sb="left", label="no", ly=1.8)
arrow("q1", "q2", label="yes", lx=-3.2)
raw(anchor("q2", "left"), (12.5, 61.5), label="yes", lx=-1, ly=3.2, rad=-0.2)
raw((36, 66.5), (37.5, 61.5), rad=-0.1)
raw((64, 66.5), (62.5, 61.5), rad=0.1)
raw(anchor("q2", "right"), (87.5, 61.5), rad=0.2)
raw(anchor("q2", "bottom"), (50, 45))
ax.text(50, 64.2, "no", ha="center", va="center", fontsize=7.8, color=ARROW_C,
        bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"), zorder=5)
raw((12.5, 50.5), (26, 45), rad=0.0)
raw((37.5, 50.5), (39, 45), rad=0.0)
raw((62.5, 50.5), (61, 45), rad=0.0)
raw((87.5, 50.5), (74, 45), rad=0.0)
raw((36, 37), anchor("q3", "top"), rad=-0.1)
for k in ("mean", "sum", "spread", "scen"):
    raw(anchor("q3", "right"), anchor(k, "left"), rad=0.0)

ax.text(50, 113, "Recipe: which discrete tool do I reach for?", ha="center",
        va="top", fontsize=13, fontweight="600", color=INK)
fig.savefig(IMG + "g2_s5_flowchart.png", dpi=150)
print("wrote g2_s5_flowchart.png")
