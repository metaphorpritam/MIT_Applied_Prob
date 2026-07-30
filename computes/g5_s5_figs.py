# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for G5 §5 (synthesis + checkpoint). Writes notes/img/g5_s5_*.png."""
import io
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path("notes/_build").resolve()))
from mpl_style import setup, diagram_ax, PAL, INK, MUTED  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
plt, PAL = setup()
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch  # noqa: E402

OUT = Path("notes/img")
OUT.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, AMBER, PINK, DGREEN, PURPLE, RED = PAL


# ---------------------------------------------------------------- helpers
def node(ax, x, y, label, r=0.42, fc="white", ec=INK, fs=11, lw=1.6):
    ax.add_patch(Circle((x, y), r, facecolor=fc, edgecolor=ec, lw=lw, zorder=3))
    ax.text(x, y, label, ha="center", va="center", fontsize=fs, color=INK, zorder=4)
    return (x, y, r)


def arc(ax, a, b, rad=0.28, label=None, color=INK, lp=0.5, off=(0, 0), fs=10, lw=1.5):
    """Curved arrow from node a to node b (tuples (x,y,r)), shrunk to circle edges."""
    (x1, y1, r1), (x2, y2, r2) = a, b
    ar = FancyArrowPatch((x1, y1), (x2, y2), connectionstyle=f"arc3,rad={rad}",
                         arrowstyle="-|>", mutation_scale=13, lw=lw, color=color,
                         shrinkA=r1 * 72 / 1.0 * 0 + 0, shrinkB=0, zorder=2)
    # manual shrink: recompute endpoints on the circle boundaries
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    # matplotlib's arc3 with rad>0 bows to the RIGHT of the a->b direction:
    # place the endpoints on that same side so the arrow never crosses itself
    th0 = math.atan2(uy, ux)
    d = math.atan(2 * rad)
    sx, sy = x1 + r1 * math.cos(th0 - d), y1 + r1 * math.sin(th0 - d)
    ex, ey = x2 + r2 * math.cos(th0 + math.pi + d), y2 + r2 * math.sin(th0 + math.pi + d)
    ar.set_positions((sx, sy), (ex, ey))
    ax.add_patch(ar)
    if label is not None:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        nx, ny = uy, -ux
        px, py = mx + nx * rad * L * lp + off[0], my + ny * rad * L * lp + off[1]
        ax.text(px, py, label, ha="center", va="center", fontsize=fs, color=color, zorder=5,
                bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.92))


def selfloop(ax, n, label=None, up=True, color=INK, fs=10, dy=0.72, fw=0.34):
    x, y, r = n
    s = 1 if up else -1
    ar = FancyArrowPatch((x - fw, y + s * r * 0.85), (x + fw, y + s * r * 0.85),
                         connectionstyle=f"arc3,rad={-s * 1.55}", arrowstyle="-|>",
                         mutation_scale=13, lw=1.5, color=color, zorder=2)
    ax.add_patch(ar)
    if label is not None:
        ax.text(x, y + s * (r + dy), label, ha="center", va="center", fontsize=fs, color=color,
                zorder=5, bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.92))


def box(ax, x, y, w, h, text, fc="white", ec=INK, fs=10, style="round,pad=0.12", lw=1.4,
        tc=INK, weight="normal", ls=2.0):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=style,
                                facecolor=fc, edgecolor=ec, lw=lw, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, zorder=3,
            weight=weight, linespacing=ls)


def diamond(ax, x, y, w, h, text, fs=10, ec=BLUE):
    ax.add_patch(plt.Polygon([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]],
                             closed=True, facecolor="#eef4fc", edgecolor=ec, lw=1.5, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK, zorder=3,
            linespacing=1.35)


def link(ax, p, q, label=None, color=MUTED, fs=9, off=(0, 0)):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12, lw=1.3,
                                 color=color, zorder=1))
    if label:
        ax.text((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1], label, ha="center",
                va="center", fontsize=fs, color=color, zorder=4,
                bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.95))


def save(fig, name):
    p = OUT / f"g5_s5_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ================================================================ Fig 5.1
# Decision flowchart: which equation system?
fig, ax = plt.subplots(figsize=(10.6, 8.4))
diagram_ax(ax)
ax.set_xlim(0, 21)
ax.set_ylim(0, 16.6)
ax.set_aspect("auto")

box(ax, 10.5, 15.8, 12.4, 1.1, "What are you asked for?", fc="#f4f2ea", fs=12, weight="bold")

diamond(ax, 10.5, 13.6, 9.0, 1.9,
        "Is a specific finite time $n$ named\n(\"after 3 steps\", \"at $n=2$\")?", fs=10.5)
link(ax, (10.5, 15.25), (10.5, 14.55))

box(ax, 4.1, 11.1, 7.4, 2.9,
    "$n$-STEP\n$r_{ij}(n)=\\sum_k r_{ik}(n-1)\\,p_{kj}$\n$r_{ij}(0)=\\delta_{ij}$\nmatrix form $R(n)=P^{\\,n}$",
    fc="#eaf2fb", ec=BLUE, fs=10.5)
link(ax, (7.2, 13.2), (5.4, 12.65), "yes")

diamond(ax, 13.8, 10.7, 9.8, 2.2,
        "Absorbing states (or a target\nyou stop at), and you want what\nhappens before the long run?", fs=10.0)
link(ax, (11.8, 13.0), (13.2, 11.85), "no")

box(ax, 17.6, 7.3, 6.2, 4.0,
    "ABSORPTION\n$a_i=\\sum_j p_{ij}a_j$\n$a_i=1$ at target,\n$a_i=0$ at other absorbing states\n\nTIME: $\\mu_i=1+\\sum_j p_{ij}\\mu_j$\n$\\mu_i=0$ at absorbing states",
    fc="#fdf0e8", ec=ORANGE, fs=9.6, ls=1.9)
link(ax, (16.4, 10.0), (17.4, 9.45), "yes")

diamond(ax, 9.0, 7.2, 9.2, 2.0,
        "Single recurrent class,\nand aperiodic?", fs=10.5)
link(ax, (11.6, 9.8), (9.9, 8.3), "no")

box(ax, 4.4, 3.2, 8.0, 3.0,
    "STEADY STATE\n$\\pi_j=\\sum_k \\pi_k p_{kj}$  for all $j$\n$\\sum_j \\pi_j = 1$   (never omit)\n$\\pi_j=0$ on every transient state",
    fc="#e9f7f1", ec=GREEN, fs=10.5)
link(ax, (6.6, 6.4), (5.2, 4.85), "yes")

box(ax, 14.6, 2.6, 8.4, 3.0,
    "NO LIMIT $\\pi_j$ of the form asked\n\u2022 periodic: $r_{ij}(n)$ oscillates\n\u2022 several recurrent classes: the\n   limit depends on the start, so\n   first do absorption into classes",
    fc="#fbeceb", ec=RED, fs=9.8, ls=1.7)
link(ax, (11.5, 6.4), (13.4, 4.4), "no")

ax.text(10.5, 0.28, "All four systems come from ONE move: condition on the first step "
                    "(or on the state at time $n-1$).",
        ha="center", fontsize=10.5, color=MUTED, style="italic")
save(fig, "qtypes")

# ================================================================ Fig 5.2
# Flowchart: classify a state / will r_ij(n) converge?
fig, ax = plt.subplots(figsize=(10.2, 7.6))
diagram_ax(ax)
ax.set_xlim(0, 20)
ax.set_ylim(0, 15)
ax.set_aspect("auto")

box(ax, 10, 14.2, 13.5, 1.05, "Pick a state $i$. Follow every arrow out of $i$.",
    fc="#f4f2ea", fs=11.5, weight="bold")
diamond(ax, 10, 11.7, 10.6, 2.0,
        "From EVERY state reachable from $i$,\ncan you get back to $i$?", fs=10.5)
link(ax, (10, 13.65), (10, 12.75))

box(ax, 3.6, 8.6, 6.8, 1.9, "$i$ is TRANSIENT\n$\\mathbf{P}(X_n=i)\\to 0$, and $\\pi_i=0$",
    fc="#fbeceb", ec=RED, fs=10.3)
link(ax, (6.6, 11.2), (4.4, 9.7), "no")

box(ax, 15.2, 8.6, 7.8, 1.9, "$i$ is RECURRENT\nits class is closed and communicating",
    fc="#e9f7f1", ec=GREEN, fs=10.3)
link(ax, (13.4, 11.2), (15.0, 9.7), "yes")

diamond(ax, 10, 5.9, 12.4, 2.0,
        "Take all cycle lengths through the class.\nIs their gcd equal to 1?", fs=10.3)
link(ax, (15.2, 7.8), (11.4, 6.9))

box(ax, 3.9, 2.3, 7.4, 2.8,
    "PERIODIC ($d=\\gcd>1$)\n$r_{ij}(n)$ does NOT converge;\nbalance equations still solvable,\n$\\pi_j$ = long-run frequency only",
    fc="#fdf6e6", ec=AMBER, fs=9.8, ls=1.8)
link(ax, (6.2, 5.2), (4.4, 3.8), "no")

box(ax, 15.4, 2.3, 7.8, 2.8,
    "APERIODIC\nif this is the only recurrent class,\n$r_{ij}(n)\\to\\pi_j$ for every start $i$\n(steady state exists and is unique)",
    fc="#eaf2fb", ec=BLUE, fs=9.8, ls=1.8)
link(ax, (13.8, 5.2), (15.4, 3.8), "yes")
save(fig, "classify")

# ================================================================ Fig 5.3
# The three gotcha chains (state-transition diagrams)
# Stacked vertically so the three chains are drawn at the same node scale as Fig. 5.2
# (a wide 1x3 strip forced the circles to about half the diameter used elsewhere).
fig, axes = plt.subplots(3, 1, figsize=(8.4, 10.8))
titles = ["(a) periodic: no limit",
          "(b) transient state: $\\pi_1=0$",
          "(c) two recurrent classes: limit depends on the start"]
NR, NFS, AFS = 0.52, 13, 11.5
for a in axes:
    diagram_ax(a)
    a.set_xlim(-1.35, 7.95)
    a.set_ylim(-1.95, 1.70)
    a.set_aspect("equal")

# (a) 3-state periodic chain (L16 slide 6) — centered on the shared x-range
a = axes[0]
n1 = node(a, 1.1, 0.0, "1", r=NR, fs=NFS)
n2 = node(a, 3.3, 0.0, "2", r=NR, fs=NFS)
n3 = node(a, 5.5, 0.0, "3", r=NR, fs=NFS)
arc(a, n1, n2, rad=-0.40, label="1", lp=1.0, fs=AFS)
arc(a, n2, n1, rad=-0.40, label="0.5", lp=1.0, fs=AFS)
arc(a, n2, n3, rad=-0.40, label="0.5", lp=1.0, fs=AFS)
arc(a, n3, n2, rad=-0.40, label="1", lp=1.0, fs=AFS)
a.text(3.3, -1.72, "$r_{22}(n)=1$ ($n$ even), $0$ ($n$ odd)", ha="center", fontsize=10,
       color=RED)

# (b) a genuinely transient state feeding a recurrent class {2,3}
a = axes[1]
m1 = node(a, 1.1, 0.0, "1", r=NR, fs=NFS)
m2 = node(a, 3.3, 0.0, "2", r=NR, fs=NFS)
m3 = node(a, 5.5, 0.0, "3", r=NR, fs=NFS)
selfloop(a, m1, "0.5", fs=AFS, dy=0.52)
selfloop(a, m2, "0.4", fs=AFS, dy=0.52)
selfloop(a, m3, "0.5", fs=AFS, dy=0.52)
arc(a, m1, m2, rad=0.0, label="0.5", lp=0, off=(0, 0.34), fs=AFS)
arc(a, m2, m3, rad=-0.40, label="0.6", lp=1.0, fs=AFS)
arc(a, m3, m2, rad=-0.40, label="0.5", lp=1.0, fs=AFS)
a.text(3.3, -1.72, "no arrow ever returns to 1, so $\\mathbf{P}(X_n=1)\\to 0$ and $\\pi_1=0$",
       ha="center", fontsize=9.5, color=MUTED)

# (c) two recurrent classes with a transient state in the middle (L16 slide 6).
# The arcs inside {3,4} are UNLABELLED on the slide; 0.5 each way is the adopted
# convention (same one the g5_s0 computes use) — flagged in the caption.
a = axes[2]
q1 = node(a, 0.0, 0.0, "1", r=NR, fs=NFS)
q2 = node(a, 2.2, 0.0, "2", r=NR, fs=NFS)
q3 = node(a, 4.4, 0.0, "3", r=NR, fs=NFS)
q4 = node(a, 6.6, 0.0, "4", r=NR, fs=NFS)
selfloop(a, q1, "1", fs=AFS, dy=0.52)
selfloop(a, q2, "0.4", fs=AFS, dy=0.52)
selfloop(a, q3, "0.5*", fs=AFS, dy=0.52)
selfloop(a, q4, "0.5*", fs=AFS, dy=0.52)
arc(a, q2, q1, rad=0.0, label="0.3", lp=0, off=(0, 0.34), fs=AFS)
arc(a, q2, q3, rad=0.0, label="0.3", lp=0, off=(0, 0.34), fs=AFS)
arc(a, q3, q4, rad=-0.40, label="0.5*", lp=1.0, fs=AFS)
arc(a, q4, q3, rad=-0.40, label="0.5*", lp=1.0, fs=AFS)
a.text(3.3, -1.42, "$r_{11}(n)=1$, $r_{31}(n)=0$, $r_{21}(n)\\to 1/2$", ha="center",
       fontsize=10, color=RED)
a.text(3.3, -1.80, "* unlabelled on L16 slide 6; symmetric $0.5$ adopted throughout",
       ha="center", fontsize=9, color=MUTED)

for a, t in zip(axes, titles):
    a.set_title(t, fontsize=11.5, color=INK, pad=4)
fig.tight_layout(h_pad=0.6)
save(fig, "gotchas")

# ================================================================ Fig 5.4
# rec16 P1(a): f_X and f_Y = 2X+1
fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.7))
a = axes[0]
a.plot([1, 2], [0, 0], color=BLUE, lw=2)
a.plot([2, 2], [0, 2 / 3], color=BLUE, lw=2)
a.plot([2, 3], [2 / 3, 2 / 3], color=BLUE, lw=2)
a.plot([3, 3], [2 / 3, 1 / 3], color=BLUE, lw=2)
a.plot([3, 4], [1 / 3, 1 / 3], color=BLUE, lw=2)
a.plot([4, 4], [1 / 3, 0], color=BLUE, lw=2)
a.plot([4, 5], [0, 0], color=BLUE, lw=2)
a.fill_between([2, 3], 0, 2 / 3, color=BLUE, alpha=0.13)
a.fill_between([3, 4], 0, 1 / 3, color=BLUE, alpha=0.13)
a.set_yticks([1 / 3, 2 / 3])
a.set_yticklabels(["$c=1/3$", "$2c=2/3$"])
a.set_xticks([1, 2, 3, 4, 5])
a.set_xlabel("$x$")
a.set_ylabel("$f_X(x)$")
a.set_title("PDF of $X$  (area $=2c+c=1$)")
a.set_ylim(0, 0.82)
a.axvline(17 / 6, color=ORANGE, lw=1.4, ls="--")
a.text(17 / 6 + 0.06, 0.72, "$\\mathbb{E}[X]=17/6$", fontsize=9, color=ORANGE)

a = axes[1]
a.plot([3, 5], [0, 0], color=GREEN, lw=2)
a.plot([5, 5], [0, 1 / 3], color=GREEN, lw=2)
a.plot([5, 7], [1 / 3, 1 / 3], color=GREEN, lw=2)
a.plot([7, 7], [1 / 3, 1 / 6], color=GREEN, lw=2)
a.plot([7, 9], [1 / 6, 1 / 6], color=GREEN, lw=2)
a.plot([9, 9], [1 / 6, 0], color=GREEN, lw=2)
a.plot([9, 10], [0, 0], color=GREEN, lw=2)
a.fill_between([5, 7], 0, 1 / 3, color=GREEN, alpha=0.13)
a.fill_between([7, 9], 0, 1 / 6, color=GREEN, alpha=0.13)
a.set_yticks([1 / 6, 1 / 3])
a.set_yticklabels(["$c/2=1/6$", "$c=1/3$"])
a.set_xticks([3, 5, 7, 9])
a.set_xlabel("$y$")
a.set_ylabel("$f_Y(y)$")
a.set_title("PDF of $Y=2X+1$  (twice as wide, half as tall)")
a.set_ylim(0, 0.82)
a.axvline(20 / 3, color=ORANGE, lw=1.4, ls="--")
a.text(20 / 3 + 0.1, 0.72, "$\\mathbb{E}[Y]=20/3$", fontsize=9, color=ORANGE)
fig.tight_layout()
save(fig, "rec16_pdf")

# ================================================================ Fig 5.5
# rec16 P1(b): joint density + region X <= W
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4))
for a in (axes[0], axes[1]):
    a.set_xlim(1.6, 4.5)
    a.set_ylim(1.6, 4.5)
    a.set_xlabel("$x$  (Xavier)")
    a.set_ylabel("$w$  (Wasima)")
    a.set_aspect("equal")
    a.set_xticks([2, 3, 4])
    a.set_yticks([2, 3, 4])

a = axes[0]
a.add_patch(plt.Rectangle((2, 2), 1, 2, facecolor=BLUE, alpha=0.30, edgecolor=INK, lw=1.3))
a.add_patch(plt.Rectangle((3, 2), 1, 2, facecolor=BLUE, alpha=0.13, edgecolor=INK, lw=1.3))
a.text(2.5, 3.0, "$c_1=1/3$", ha="center", fontsize=10.5)
a.text(3.5, 3.0, "$c_2=1/6$", ha="center", fontsize=10.5)
a.set_title("Joint PDF $f_{X,W}$: two flat slabs")

a = axes[1]
a.add_patch(plt.Rectangle((2, 2), 1, 2, facecolor="white", edgecolor=INK, lw=1.3))
a.add_patch(plt.Rectangle((3, 2), 1, 2, facecolor="white", edgecolor=INK, lw=1.3))
a.add_patch(plt.Polygon([[2, 2], [3, 3], [3, 4], [2, 4]], facecolor=BLUE, alpha=0.32,
                        edgecolor="none"))
a.add_patch(plt.Polygon([[3, 3], [4, 4], [3, 4]], facecolor=ORANGE, alpha=0.32,
                        edgecolor="none"))
a.plot([1.6, 4.5], [1.6, 4.5], color=INK, lw=1.4)
a.text(4.1, 4.28, "$x=w$", fontsize=10)
a.text(2.42, 3.45, "area $3/2$\n$\\times\\, c_1$", ha="center", fontsize=9.5)
a.text(3.30, 3.75, "area $1/2$\n$\\times\\, c_2$", ha="center", fontsize=9.5)
a.set_title("Event $X \\leq W$:   $\\frac{3}{2}\\cdot\\frac{1}{3}+\\frac{1}{2}\\cdot\\frac{1}{6}=\\frac{7}{12}$")
fig.tight_layout()
save(fig, "rec16_joint")

# ================================================================ Fig 5.6
# rec16 P2(b): mixture PDF and posterior
aa = np.linspace(-4, 8, 1200)
c1_ = (1 / 3) * np.exp(-(aa - 1) ** 2 / 2) / np.sqrt(2 * np.pi)
c2_ = (2 / 3) * np.exp(-(aa - 2) ** 2 / 4) / np.sqrt(4 * np.pi)
fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.8))
a = axes[0]
a.plot(aa, c1_, color=BLUE, lw=1.7, ls="--", label="$(1/3)\\,N(1,1)$ term")
a.plot(aa, c2_, color=ORANGE, lw=1.7, ls="--", label="$(2/3)\\,N(2,2)$ term")
a.plot(aa, c1_ + c2_, color=INK, lw=2.2, label="$f_A(a)$ (mixture)")
a.set_xlabel("$a$")
a.set_ylabel("density")
a.set_title("Mixture PDF of $A$ when $N\\in\\{1,2\\}$")
a.legend(loc="upper right")
a = axes[1]
a.plot(aa, c1_ / (c1_ + c2_), color=PURPLE, lw=2.2)
a.axhline(1 / 3, color=MUTED, lw=1.2, ls=":")
a.text(-3.8, 1 / 3 + 0.08, "prior $\\mathbf{P}(N=1)=1/3$", fontsize=9, color=MUTED, ha="left",
       bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.92))
for a0, lbl in [(0.0, "0.538"), (2.0, "0.300"), (4.0, "0.021")]:
    y = ((1 / 3) * math.exp(-(a0 - 1) ** 2 / 2) / math.sqrt(2 * math.pi)) / (
        (1 / 3) * math.exp(-(a0 - 1) ** 2 / 2) / math.sqrt(2 * math.pi)
        + (2 / 3) * math.exp(-(a0 - 2) ** 2 / 4) / math.sqrt(4 * math.pi))
    a.plot([a0], [y], "o", color=PURPLE, ms=6)
    a.annotate(f"$a={a0:.0f}$: {lbl}", (a0, y), textcoords="offset points",
               xytext=(8, 10), fontsize=9, color=PURPLE)
a.set_xlabel("$a$")
a.set_ylabel("$\\mathbf{P}(N=1\\mid A=a)$")
a.set_title("Posterior on the count $N$ given the sum $A=a$")
a.set_ylim(0, 1.02)
fig.tight_layout()
save(fig, "rec16_mix")

# ================================================================ Fig 5.7
# rec17 P1(d): hypoexponential density
lam_c, lam_s = 1.5, 0.5
x = np.linspace(0, 12, 1400)
fx = lam_s * lam_c / (lam_s - lam_c) * (np.exp(-lam_c * x) - np.exp(-lam_s * x))
fig, ax = plt.subplots(figsize=(7.6, 4.0))
ax.plot(x, lam_s * np.exp(-lam_s * x), color=BLUE, lw=1.6, ls="--",
        label="$X_s\\sim\\mathrm{Exp}(\\lambda_s=0.5)$")
ax.plot(x, lam_c * np.exp(-lam_c * x), color=ORANGE, lw=1.6, ls="--",
        label="$X_c\\sim\\mathrm{Exp}(\\lambda_c=1.5)$")
ax.plot(x, fx, color=INK, lw=2.3, label="$X=X_s+X_c$ (convolution)")
ax.axvline(1 / lam_s + 1 / lam_c, color=GREEN, lw=1.4, ls=":")
ax.text(1 / lam_s + 1 / lam_c + 0.14, 0.62,
        "$E[X]=1/\\lambda_s+1/\\lambda_c=2.6667$", fontsize=9.5,
        color=GREEN)
ax.plot([math.log(lam_s / lam_c) / (lam_s - lam_c)], [0.28755], "o", color=INK, ms=6)
ax.annotate("mode $=1.0986$", (1.0986, 0.28755), textcoords="offset points", xytext=(-58, 26), fontsize=9,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.9))
ax.set_xlabel("$x$  (minutes)")
ax.set_ylabel("density")
ax.set_title("Time to the first conscious response preceded by a subconscious one")
ax.legend()
fig.tight_layout()
save(fig, "rec17_hypo")

# ================================================================ Fig 5.8
# rec17 P3: random incidence, Erlang-2 -> Erlang-3
lam = 1.0
l = np.linspace(0, 12, 1400)
f2 = lam**2 * l * np.exp(-lam * l)
f3 = lam**3 * l**2 * np.exp(-lam * l) / 2
fig, ax = plt.subplots(figsize=(7.8, 4.1))
ax.plot(l, f2, color=BLUE, lw=2.2, label="typical interval: Erlang(2, $\\lambda$), mean $2/\\lambda$")
ax.plot(l, f3, color=ORANGE, lw=2.2,
        label="interval containing $t$: Erlang(3, $\\lambda$), mean $3/\\lambda$")
ax.fill_between(l, 0, f2, color=BLUE, alpha=0.10)
ax.fill_between(l, 0, f3, color=ORANGE, alpha=0.10)
ax.axvline(2 / lam, color=BLUE, lw=1.3, ls=":")
ax.axvline(3 / lam, color=ORANGE, lw=1.3, ls=":")
ax.text(2 / lam - 0.1, 0.375, "$2/\\lambda$", color=BLUE, ha="right", fontsize=10)
ax.text(3 / lam + 0.1, 0.375, "$3/\\lambda$", color=ORANGE, fontsize=10)
ax.set_xlabel("interval length $\\ell$   ($\\lambda=1$)")
ax.set_ylabel("density")
ax.set_title("Random incidence: length-biasing $f_L(\\ell)=\\ell f(\\ell)/\\mathbb{E}[L]$")
ax.legend(loc="upper right")
fig.tight_layout()
save(fig, "rec17_incid")

print("done")
