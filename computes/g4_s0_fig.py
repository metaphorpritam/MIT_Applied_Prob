# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Figure for G4 section 0 (orientation).

Fig. 0.1  g4_s0_conceptmap : concept map of note G4 -- two parallel themes
          (conditioning as a computational tool; random processes), the random-sum
          bridge between them, and the terminus in Markov chains.
          Sources: L12 slides 1-3, L13 slides 1-3, L14 slides 1/7, L15 slide 1.
"""
import io
import sys

sys.path.insert(0, "d:/Python-UV/MIT_Applied_Prob/notes/_build")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from mpl_style import INK, MUTED, PAL, setup

plt, _ = setup()
IMG = "d:/Python-UV/MIT_Applied_Prob/notes/img/"

fig, ax = plt.subplots(figsize=(10.4, 6.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 66)
ax.set_aspect("equal")
ax.axis("off")
ax.grid(False)

BLUE, ORANGE, GREEN, PURPLE = PAL[0], PAL[1], PAL[2], PAL[6]


def box(xc, yc, w, h, text, edge, face, fs=8.2, weight="normal", tc=None):
    ax.add_patch(FancyBboxPatch((xc - w / 2, yc - h / 2), w, h,
                                boxstyle="round,pad=0.6,rounding_size=1.2",
                                linewidth=1.3, edgecolor=edge, facecolor=face,
                                zorder=2))
    ax.text(xc, yc, text, ha="center", va="center", fontsize=fs,
            color=tc or INK, fontweight=weight, zorder=3, linespacing=1.45)


def arrow(x0, y0, x1, y1, color=MUTED, dashed=False, lw=1.3):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                                 arrowstyle="-|>", mutation_scale=11,
                                 linewidth=lw, color=color, zorder=1,
                                 linestyle=(0, (4, 2.5)) if dashed else "solid",
                                 shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------- title
box(50, 62, 62, 5.4,
    "G4  —  Iterated Expectations & Arrival Processes   (L12–L15)",
    INK, "#f4f3ee", fs=10.5, weight="bold")

# ---------------------------------------------------------------- theme headers
AX, BX = 23, 77           # column centers
W = 38                    # box width
arrow(50, 59.1, AX, 55.3)
arrow(50, 59.1, BX, 55.3)

box(AX, 52.4, W, 5.6,
    "THEME A  ·  conditioning as a computational tool",
    BLUE, "#eaf2fc", fs=9.2, weight="bold", tc=BLUE)
box(BX, 52.4, W, 5.6,
    "THEME B  ·  processes = infinite families of r.v.'s",
    ORANGE, "#fdeee6", fs=9.2, weight="bold", tc="#a8451c")

# ---------------------------------------------------------------- theme A chain
A_ITEMS = [
    (43.0, "$\\mathbf{E}[X\\,|\\,Y]$  is a  RANDOM VARIABLE\nthe conceptual jump of this note   ·   §1"),
    (33.5, "Law of iterated expectations\n$\\mathbf{E}[\\,\\mathbf{E}[X\\,|\\,Y]\\,]=\\mathbf{E}[X]$   ·   §1"),
    (24.0, "Law of total variance\n$\\mathrm{var}(X)=\\mathbf{E}[\\mathrm{var}(X|Y)]+\\mathrm{var}(\\mathbf{E}[X|Y])$   ·   §1"),
]
for y, txt in A_ITEMS:
    box(AX, y, W, 7.4, txt, BLUE, "white")
arrow(AX, 52.4 - 3.4, AX, 43.0 + 4.3)
arrow(AX, 43.0 - 4.3, AX, 33.5 + 4.3)
arrow(AX, 33.5 - 4.3, AX, 24.0 + 4.3)

# ---------------------------------------------------------------- theme B chain
B_ITEMS = [
    (43.0, "BERNOULLI process  —  discrete time\nslot success prob. $p$; binomial / geometric / Pascal   ·   §2"),
    (33.5, "POISSON process  —  continuous time\nrate $\\lambda$; Poisson / exponential / Erlang   ·   §3"),
    (24.0, "Merging · splitting · random incidence\nthe structural properties   ·   §4"),
]
for y, txt in B_ITEMS:
    box(BX, y, W, 7.4, txt, ORANGE, "white")
arrow(BX, 52.4 - 3.4, BX, 43.0 + 4.3)
arrow(BX, 43.0 - 4.3, BX, 33.5 + 4.3)
arrow(BX, 33.5 - 4.3, BX, 24.0 + 4.3)

# --------------------------------------------- the bridge: random sums (Theme A -> B)
# Drawn as TWO directed segments so that both halves of the dashed bridge carry an
# arrowhead: total-variance box -> label, label -> Bernoulli box.  A single long
# arrow would be hidden behind the label's white bbox for its middle stretch and the
# lower-left half would read as an unfinished line.
arrow(AX + W / 2 + 0.9, 24.0, 46.9, 29.7, color=GREEN, dashed=True, lw=1.6)
arrow(53.1, 37.3, BX - W / 2 - 0.9, 43.0, color=GREEN, dashed=True, lw=1.6)
ax.text(50, 33.5, "random sums\n$Y=X_1+\\cdots+X_N$\n§2", ha="center", va="center",
        fontsize=8.0, color=GREEN, fontweight="bold", zorder=4, linespacing=1.4,
        bbox=dict(boxstyle="round,pad=0.36", facecolor="white",
                  edgecolor=GREEN, linewidth=1.1))

# ---------------------------------------------------------------- memorylessness note
box(50, 15.0, 74, 5.8,
    "shared engine:  MEMORYLESSNESS  —  at any time the process restarts fresh, "
    "independent of its past",
    PURPLE, "#eeecf8", fs=8.6, tc=PURPLE)
arrow(AX, 24.0 - 4.3, 40, 15.0 + 3.5)
arrow(BX, 24.0 - 4.3, 60, 15.0 + 3.5)

# ---------------------------------------------------------------- terminus
box(50, 5.4, 74, 5.8,
    "§5  synthesis · checkpoint · bridge to MARKOV CHAINS (memory across time — note G5)",
    INK, "#f4f3ee", fs=8.8, weight="bold")
arrow(50, 15.0 - 3.5, 50, 5.4 + 3.5)

fig.savefig(IMG + "g4_s0_conceptmap.png")
plt.close(fig)
print("wrote", IMG + "g4_s0_conceptmap.png")
