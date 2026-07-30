# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""G5 §0 figures: (1) independence -> memory-in-a-state, (2) concept map."""
import io
import sys

sys.path.insert(0, "d:/Python-UV/MIT_Applied_Prob/notes/_build")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import numpy as np  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch  # noqa: E402

from mpl_style import PAL, INK, MUTED, diagram_ax, setup  # noqa: E402

plt, _ = setup()
IMG = "d:/Python-UV/MIT_Applied_Prob/notes/img/"


def node(ax, xy, label, color, r=0.46):
    ax.add_patch(Circle(xy, r, facecolor="white", edgecolor=color, lw=2.0, zorder=3))
    ax.text(xy[0], xy[1], label, ha="center", va="center", fontsize=12,
            color=INK, zorder=4)


def _apex(p1, p2, rad):
    """Apex (t = 0.5 point) of matplotlib's arc3 quadratic Bezier."""
    p1, p2 = np.asarray(p1, float), np.asarray(p2, float)
    d = p2 - p1
    return (p1 + p2) / 2 + 0.5 * rad * np.array([d[1], -d[0]])


def arc(ax, a, b, rad, color, r=0.46, lw=1.7):
    """Bowed directed arc between circle centers a,b, trimmed to the rims.

    Same primitive as Fig. 1.1: the arrowhead lands ON the destination rim, so
    the direction of travel is unambiguous.  Returns the bow apex so a label
    can be parked just past it.
    """
    (x1, y1), (x2, y2) = a, b
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>,head_width=0.26,head_length=0.55",
                                color=color, lw=lw,
                                connectionstyle=f"arc3,rad={rad}",
                                shrinkA=r * 72, shrinkB=r * 72),
                zorder=5)
    return _apex(a, b, rad)


def selfloop(ax, xy, color, r=0.46, lw=1.7, size=0.62, where="left"):
    """Self-transition loop bulging `size` beyond the rim; returns its label anchor."""
    x, y = xy
    th = np.deg2rad({"top": 90, "bottom": 270, "left": 180, "right": 0}[where])
    ux, uy = np.cos(th), np.sin(th)      # outward direction
    px, py = -uy, ux                     # tangential direction
    half = 0.45
    p1 = (x + r * (ux * 0.90 + px * half), y + r * (uy * 0.90 + py * half))
    p2 = (x + r * (ux * 0.90 - px * half), y + r * (uy * 0.90 - py * half))
    chord = np.hypot(p2[0] - p1[0], p2[1] - p1[1])
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="-|>,head_width=0.26,head_length=0.55",
                                color=color, lw=lw,
                                connectionstyle=f"arc3,rad={-2.0 * size / chord}",
                                shrinkA=0, shrinkB=0), zorder=2)
    d = r * 0.90 + size + 0.30
    return (x + ux * d, y + uy * d)


# ============================================================ Fig 0.1
fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.0))

# --- left: independent trials (Bernoulli), no memory
ax = axes[0]
diagram_ax(ax)
ax.set_xlim(-0.6, 9.4)
ax.set_ylim(-3.9, 3.3)
xs = np.arange(9)
bits = [1, 0, 0, 1, 0, 1, 1, 0, 0]
ax.plot([-0.3, 8.5], [0, 0], color=MUTED, lw=1.1, zorder=1)
for x, bxx in zip(xs, bits):
    ax.plot([x, x], [-0.16, 0.16], color=MUTED, lw=1.1, zorder=1)
    ax.text(x, -0.62, str(bxx), ha="center", va="center", fontsize=11, color=INK)
    if bxx:
        ax.plot([x], [0.55], marker="v", ms=8, color=PAL[1], zorder=3)
ax.text(4.1, 2.75, "each slot: fresh coin, $\\mathbf{P}(X_t=1)=p$",
        ha="center", fontsize=10, color=INK)
ax.text(4.1, 2.05, "$X_1,\\dots,X_t$ independent — the past is worth nothing",
        ha="center", fontsize=10, color=MUTED)
ax.text(4.1, -2.55, "state carried forward: none", ha="center", fontsize=10, color=MUTED)
ax.text(4.1, -3.30, "G4:  Bernoulli / Poisson process", ha="center", fontsize=10.5,
        color=PAL[1], weight="600")

# --- right: a two-state chain, memory compressed into X_n
ax = axes[1]
diagram_ax(ax)
ax.set_xlim(-3.0, 6.4)
ax.set_ylim(-3.9, 3.3)
A, B = (0.0, -0.20), (3.4, -0.20)
node(ax, A, "1", PAL[0])
node(ax, B, "2", PAL[0])
up = arc(ax, A, B, -0.34, PAL[0])          # 1 -> 2 bows above
dn = arc(ax, B, A, -0.34, PAL[0])          # 2 -> 1 bows below
la = selfloop(ax, A, PAL[0], where="left")
lb = selfloop(ax, B, PAL[0], where="right")
ax.text(up[0], up[1] + 0.26, "$p_{12}=0.5$", ha="center", va="bottom",
        fontsize=10.5, color=PAL[0])
ax.text(dn[0], dn[1] - 0.26, "$p_{21}=0.2$", ha="center", va="top",
        fontsize=10.5, color=PAL[0])
ax.text(la[0] - 0.10, la[1], "$p_{11}=0.5$", ha="right", va="center",
        fontsize=10.5, color=PAL[0])
ax.text(lb[0] + 0.10, lb[1], "$p_{22}=0.8$", ha="left", va="center",
        fontsize=10.5, color=PAL[0])
ax.text(1.7, 2.75, "$p_{ij}=\\mathbf{P}(X_{n+1}=j\\mid X_n=i)$",
        ha="center", fontsize=10.5, color=INK)
ax.text(1.7, 2.05, "the whole past enters only through $X_n$",
        ha="center", fontsize=10, color=MUTED)
ax.text(1.7, -2.55, "state carried forward: $X_n$", ha="center",
        fontsize=10, color=MUTED)
ax.text(1.7, -3.30, "G5:  Markov chain", ha="center", fontsize=10.5,
        color=PAL[0], weight="600")

fig.subplots_adjust(wspace=0.10)
fig.savefig(IMG + "g5_s0_memory.png")
plt.close(fig)
print("wrote g5_s0_memory.png")

# ============================================================ Fig 0.2 concept map
fig, ax = plt.subplots(figsize=(11.6, 7.2))
ax.set_aspect("equal")
ax.axis("off")
ax.grid(False)
ax.set_xlim(0, 116)
ax.set_ylim(0, 72)


def box(x, y, w, h, lines, fc, ec, fs=9.4, tc=INK, weight="normal", ls=1.45):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.9,rounding_size=1.6",
                                facecolor=fc, edgecolor=ec, lw=1.4, zorder=2))
    ax.text(x + w / 2, y + h / 2, "\n".join(lines), ha="center", va="center",
            fontsize=fs, color=tc, zorder=3, weight=weight, linespacing=ls)
    return (x + w / 2, y, x + w / 2, y + h, x, y + h / 2, x + w, y + h / 2)


def link(p, q, color=MUTED, style="-|>", rad=0.0, lw=1.4, dash=None):
    pa = FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=12, lw=lw,
                         color=color, zorder=1,
                         connectionstyle=f"arc3,rad={rad}")
    if dash:
        pa.set_linestyle(dash)
    ax.add_patch(pa)


tint = {0: "#eaf2fc", 1: "#fdefe8", 2: "#e8f6f0", 3: "#fdf4e0", 6: "#eeecf7"}

# top: the model
top = box(30, 61, 56, 8.5, ["§1  THE MODEL — states, $p_{ij}$, the Markov property",
                            "$n$-step $r_{ij}(n)$ and Chapman–Kolmogorov"],
          tint[0], PAL[0], fs=9.8, weight="600")
ax.text(58, 71.2, "G5 — Markov chains:  compress the past into a STATE",
        ha="center", fontsize=11.5, color=INK, weight="600")

# middle: classification
mid = box(30, 47.5, 56, 8.0, ["§2  CLASSIFY THE STATES — recurrent / transient,",
                              "periodic; does $r_{ij}(n)$ converge, and to what?"],
          tint[1], PAL[1], fs=9.8, weight="600")
link((top[0], top[1]), (mid[0], mid[1] + 8.0), PAL[0])

# three questions row
q1 = box(3, 30, 32, 11.5, ["QUESTION A — short run",
                           "where am I after $n$ steps?",
                           "$r_{11}(2)=0.35$, $r_{11}(3)=0.305$"],
         "#ffffff", PAL[0], fs=9.0)
q2 = box(41, 30, 34, 11.5, ["QUESTION B — long run",
                            "a single aperiodic recurrent class",
                            "$r_{ij}(n)\\to\\pi_j$: $\\;(2/7,\\,5/7)$"],
         "#ffffff", PAL[2], fs=9.0)
q3 = box(81, 30, 32, 11.5, ["QUESTION C — endgame",
                            "several recurrent classes:",
                            "which one, and how soon?"],
         "#ffffff", PAL[3], fs=9.0)
link((mid[4], mid[5]), (q1[0], q1[1] + 12.5), PAL[1], rad=0.25)
link((mid[0], mid[1]), (q2[0], q2[1] + 12.5), PAL[1])
link((mid[6], mid[5]), (q3[0], q3[1] + 12.5), PAL[1], rad=-0.25)

# answers row
# NOTE: mathtext sets \sum with limits above/below, whose glyph box overruns the
# line leading inside a compact flowchart box.  Use the upright sigma with a
# side subscript so all three lines clear each other (style contract: no
# overlapping text).
a2 = box(41, 12.5, 34, 12.0, ["§3  STEADY STATE",
                           "balance: $\\pi_j=\\Sigma_k\\,\\pi_k p_{kj}$,  $\\Sigma_j\\,\\pi_j=1$",
                           "plus birth–death cut equations"],
         tint[2], PAL[2], fs=9.0, weight="600", ls=1.7)
a3 = box(81, 14, 32, 9.0, ["§4  ABSORPTION",
                           "first-step equations for $a_i$",
                           "and for $\\mu_i=\\mathbb{E}[\\text{time}]$"],
         tint[3], PAL[3], fs=9.0, weight="600")
a1 = box(3, 14, 32, 9.0, ["matrix powers $R(n)=P^n$",
                          "(no closed form needed —",
                          "just iterate the recursion)"],
         "#f7f6f2", MUTED, fs=9.0)
link((q1[0], q1[1]), (a1[2], a1[3] + 1.0), PAL[0])
link((q2[0], q2[1]), (a2[2], a2[3] + 1.0), PAL[2])
link((q3[0], q3[1]), (a3[2], a3[3] + 1.0), PAL[3])

bot = box(24, 2.5, 68, 7.0, ["§5  SYNTHESIS + CHECKPOINT — pick the right equation system,",
                             "plus a continuous-RV / Poisson review (G3, G4)"],
          tint[6], PAL[6], fs=9.4, weight="600")
link((a1[0], a1[1]), (bot[4] - 1.2, bot[5]), MUTED, rad=0.20)
link((a2[0], a2[1]), (bot[0], bot[1] + 8.0), MUTED)
link((a3[0], a3[1]), (bot[6] + 1.2, bot[5]), MUTED, rad=-0.20)

fig.savefig(IMG + "g5_s0_conceptmap.png")
plt.close(fig)
print("wrote g5_s0_conceptmap.png")
