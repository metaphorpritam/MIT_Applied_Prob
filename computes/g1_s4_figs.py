# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for §4 Counting (g1_s4_*.png)."""
from __future__ import annotations
import sys
from math import comb, factorial

sys.path.insert(0, r"d:/Python-UV/MIT_Applied_Prob/notes/_build")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mpl_style import setup, diagram_ax, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle  # noqa: E402

OUT = r"d:/Python-UV/MIT_Applied_Prob/notes/img/"

# ----------------------------------------------------------------- Fig 4.1
# Basic counting principle: 3-stage tree, n1=4, n2=3, n3=2 -> 24 leaves
fig, ax = plt.subplots(figsize=(7.6, 5.2))
ax.axis("off")
ax.grid(False)
X = [0.0, 1.9, 3.6, 4.9]          # x of root, stage-1 nodes, stage-2 nodes, leaves
n1, n2, n3 = 4, 3, 2
root = (X[0], 0.0)
span1, span2, span3 = 4.6, 0.60, 0.165
s1 = [(X[1], (i - (n1 - 1) / 2) * span1 / (n1 - 1) * 1.0) for i in range(n1)]
for (x, y) in s1:
    ax.plot([root[0], x], [root[1], y], color=PAL[0], lw=1.6, zorder=1)
s2 = []
for (x1, y1) in s1:
    for j in range(n2):
        y2 = y1 + (j - (n2 - 1) / 2) * span2
        ax.plot([x1, X[2]], [y1, y2], color=PAL[1], lw=1.3, zorder=1)
        s2.append((X[2], y2))
for (x2, y2) in s2:
    for kk in range(n3):
        y3 = y2 + (kk - (n3 - 1) / 2) * span3
        ax.plot([x2, X[3]], [y2, y3], color=PAL[2], lw=1.1, zorder=1)
        ax.plot([X[3]], [y3], marker="o", ms=2.6, color=PAL[2], zorder=3)
ax.plot([root[0]], [root[1]], marker="o", ms=8, color=INK, zorder=4)
for (x, y) in s1:
    ax.plot([x], [y], marker="o", ms=5.5, color=PAL[0], zorder=3)
for (x, y) in s2:
    ax.plot([x], [y], marker="o", ms=3.4, color=PAL[1], zorder=3)
ax.text(root[0] - 0.18, 0.0, "start", ha="right", va="center", fontsize=10, color=INK)
top = 3.35
for xx, lab, col in [(X[1], "stage 1\n$n_1 = 4$", PAL[0]),
                     (X[2], "stage 2\n$n_2 = 3$", PAL[1]),
                     (X[3], "stage 3\n$n_3 = 2$", PAL[2])]:
    ax.text(xx, top, lab, ha="center", va="bottom", fontsize=10, color=col, weight="600")
ax.text((X[0] + X[3]) / 2, -3.45,
        r"leaves $= n_1 n_2 n_3 = 4\cdot 3\cdot 2 = 24$",
        ha="center", va="top", fontsize=12, color=INK)
ax.set_xlim(-0.9, 5.5)
ax.set_ylim(-4.3, 4.5)
fig.savefig(OUT + "g1_s4_stages.png")
plt.close(fig)
print("wrote g1_s4_stages.png")

# ----------------------------------------------------------------- Fig 4.2
# Pascal triangle of C(n,k), n = 0..8, shaded by magnitude
N = 8
fig, ax = plt.subplots(figsize=(7.4, 4.6))
ax.axis("off")
ax.grid(False)
vals = [[comb(n, k) for k in range(n + 1)] for n in range(N + 1)]
vmax = max(max(r) for r in vals)
for n in range(N + 1):
    for k in range(n + 1):
        x = k - n / 2.0
        y = -n
        v = vals[n][k]
        shade = 0.10 + 0.75 * (v / vmax) ** 0.45
        ax.add_patch(Rectangle((x - 0.44, y - 0.34), 0.88, 0.68,
                               facecolor=PAL[0], alpha=shade, edgecolor="white", lw=1.0))
        ax.text(x, y, str(v), ha="center", va="center", fontsize=9.5,
                color="white" if shade > 0.5 else INK, weight="600")
for n in range(N + 1):
    ax.text(-n / 2.0 - 1.35, -n, f"$n={n}$", ha="right", va="center",
            fontsize=9, color=MUTED)
    ax.text(n / 2.0 + 1.35, -n, f"$\\sum_k={2**n}$", ha="left", va="center",
            fontsize=9, color=PAL[1], weight="600")
ax.text(0, 1.15, r"$\binom{n}{k}$  —  each entry is the sum of the two above it",
        ha="center", va="bottom", fontsize=11, color=INK)
ax.text(0, -N - 1.05, r"row sum $=\sum_{k=0}^{n}\binom{n}{k}=2^n$ (all subsets)",
        ha="center", va="top", fontsize=10.5, color=PAL[1])
ax.set_xlim(-7.6, 7.6)
ax.set_ylim(-N - 2.0, 1.9)
fig.savefig(OUT + "g1_s4_pascal.png")
plt.close(fig)
print("wrote g1_s4_pascal.png")

# ----------------------------------------------------------------- Fig 4.3
# Decision flowchart: which counting object?
fig, ax = plt.subplots(figsize=(8.0, 6.4))
ax.axis("off")
ax.grid(False)


def box(cx, cy, w, h, text, fc, ec, fs=9.5, tc=INK):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0.06,rounding_size=0.12",
                                facecolor=fc, edgecolor=ec, lw=1.3, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=tc, zorder=3)


def arrow(x1, y1, x2, y2, label="", lx=None, ly=None, col=AXIS_C):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=13, color=col, lw=1.3, zorder=1,
                                 shrinkA=1, shrinkB=3))
    if label:
        ax.text(lx, ly, label, ha="center", va="center", fontsize=9,
                color=MUTED, zorder=4,
                bbox=dict(fc="white", ec="none", pad=1.4))


LIGHT, CREAM, MINT = "#eef4fc", "#fdf3e6", "#eaf7f1"
box(6.0, 9.60, 6.0, 0.90, "Count the outcomes of a selection\nfrom $n$ distinct items", "#f6f5f0", AXIS_C, 10)
arrow(6.0, 9.15, 6.0, 8.55)
box(6.0, 8.10, 4.6, 0.85, "Are the items split into\n$r$ labeled GROUPS?", CREAM, PAL[3], 9.5)
arrow(6.0, 7.68, 3.2, 6.94, "no", 4.15, 7.42)
arrow(6.0, 7.68, 9.9, 7.20, "yes", 8.30, 7.55)

box(3.2, 6.50, 4.0, 0.80, "Does ORDER matter?", CREAM, PAL[3], 9.5)
box(9.9, 6.50, 4.4, 1.35,
    "PARTITION into sizes $n_1,\\dots,n_r$\n" + r"$n!\,/\,(n_1!\cdots n_r!)$",
    LIGHT, PAL[0], 9.5)

arrow(3.2, 6.10, 1.6, 5.06, "yes", 1.95, 5.68)
arrow(3.2, 6.10, 5.6, 5.28, "no", 4.95, 5.80)

box(1.6, 4.60, 2.8, 0.88, "Repetition\nallowed?", CREAM, PAL[3], 9.5)
box(5.6, 4.60, 3.4, 1.25, "SUBSET\n" + r"$\binom{n}{k}=\dfrac{n!}{k!\,(n-k)!}$",
    LIGHT, PAL[0], 9.5)

arrow(1.6, 4.16, 1.0, 3.28, "yes", 0.72, 3.76)
arrow(1.6, 4.16, 4.0, 3.30, "no", 3.05, 3.86)

box(1.0, 2.70, 2.0, 1.05, "SEQUENCE\n$n^k$", LIGHT, PAL[0], 9.5)
box(4.0, 2.70, 3.0, 1.15, "$k$-PERMUTATION\n" + r"$\dfrac{n!}{(n-k)!}$", LIGHT, PAL[0], 9.5)
box(7.9, 2.70, 3.0, 1.05, "$k=n$: PERMUTATION\n$n!$", MINT, PAL[2], 9.5)
arrow(5.52, 2.70, 6.38, 2.70)
box(9.9, 4.60, 2.4, 1.00, "sum over all $k$:\n$2^n$ subsets", MINT, PAL[2], 9)
arrow(7.32, 4.60, 8.68, 4.60)

ax.set_xlim(-0.4, 12.4)
ax.set_ylim(1.9, 10.3)
fig.savefig(OUT + "g1_s4_flowchart.png")
plt.close(fig)
print("wrote g1_s4_flowchart.png")

# ----------------------------------------------------------------- Fig 4.4
# Birthday problem: linear + log panels
D = 365


def pdist(n):
    x = 1.0
    for i in range(n):
        x *= (D - i) / D
    return x


ns = np.arange(1, 101)
ps = np.array([pdist(int(n)) for n in ns])
nsL = np.arange(1, 131)
psL = np.array([pdist(int(n)) for n in nsL])

fig, axs = plt.subplots(2, 1, figsize=(7.2, 6.4))
a = axs[0]
a.plot(ns, ps, color=PAL[0], lw=2.0, label=r"$P(\mathrm{all\ distinct})$")
a.plot(ns, 1 - ps, color=PAL[1], lw=2.0, ls="--", label=r"$P(\mathrm{some\ match})$")
a.axhline(0.5, color=MUTED, lw=1.0, ls=":")
a.axvline(23, color=PAL[5], lw=1.3, ls="-.")
a.plot([23], [pdist(23)], marker="o", ms=7, color=PAL[5], zorder=5)
a.annotate("n = 23:  P(distinct) = 0.4927\n              P(match) = 0.5073",
           xy=(23, 0.4927), xytext=(28.5, 0.30), fontsize=9, color=INK,
           arrowprops=dict(arrowstyle="->", color=PAL[5], lw=1.2,
                           shrinkA=2, shrinkB=4))
a.set_xlim(0, 100)
a.set_ylim(0, 1.03)
a.set_xlabel("$n$  (number of people)")
a.set_ylabel("probability")
a.set_title("Birthday problem, 365 equally likely birthdays")
a.legend(loc="lower right", bbox_to_anchor=(0.995, 0.06), framealpha=1.0)

b = axs[1]
b.semilogy(nsL, psL, color=PAL[0], lw=2.0)
b.axvline(23, color=PAL[5], lw=1.3, ls="-.")
b.set_xlim(0, 130)
b.set_ylim(1e-11, 2.0)
b.set_yticks([10.0 ** e for e in range(0, -11, -2)])
b.set_xlabel("$n$")
b.set_ylabel(r"$P(\mathrm{all\ distinct})$")
b.set_title("same curve, logarithmic scale (rec04 Extra Handout)")
b.text(100, 3e-4, r"$P\approx 10^{-10}$ at $n\approx 122$", fontsize=9,
       color=MUTED, ha="center")
fig.tight_layout()
fig.savefig(OUT + "g1_s4_birthday.png")
plt.close(fig)
print("wrote g1_s4_birthday.png")

# ----------------------------------------------------------------- Fig 4.5
# Chessboard with 8 non-attacking rooks
fig, axs = plt.subplots(1, 2, figsize=(8.2, 4.3))
perm_good = [0, 4, 7, 5, 2, 6, 1, 3]     # a permutation: non-attacking
perm_bad = [0, 4, 7, 5, 2, 6, 1, 1]      # two rooks share column 1


def board(ax, cols, title, ok):
    ax.grid(False)
    ax.set_aspect("equal")
    for r in range(8):
        for c in range(8):
            ax.add_patch(Rectangle((c, 7 - r), 1, 1,
                                   facecolor="#f2efe6" if (r + c) % 2 == 0 else "#d8d3c4",
                                   edgecolor="none"))
    seen = {}
    for r, c in enumerate(cols):
        seen.setdefault(c, []).append(r)
    for r, c in enumerate(cols):
        clash = len(seen[c]) > 1
        col = PAL[7] if clash else PAL[0]
        cx, cy = c + 0.5, 7 - r + 0.5
        # simple rook silhouette: crenellated top + tapered body + base
        px = [-.30, -.16, -.16, -.06, -.06, .06, .06, .16, .16, .30,
              .30, .18, .16, .28, .28, -.28, -.28, -.16, -.18, -.30]
        py = [.30, .30, .18, .18, .30, .30, .18, .18, .30, .30,
              .06, .00, -.18, -.24, -.32, -.32, -.24, -.18, .00, .06]
        ax.fill([cx + t for t in px], [cy + t for t in py], color=col, zorder=4)
    if not ok:
        cbad = [c for c, rs in seen.items() if len(rs) > 1][0]
        ax.add_patch(Rectangle((cbad, 0), 1, 8, facecolor=PAL[7], alpha=0.16,
                               edgecolor=PAL[7], lw=1.5))
    ax.add_patch(Rectangle((0, 0), 8, 8, facecolor="none", edgecolor=AXIS_C, lw=1.4))
    ax.set_xlim(-0.15, 8.15)
    ax.set_ylim(-0.15, 8.15)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, fontsize=10, color=PAL[0] if ok else PAL[7])


board(axs[0], perm_good, "safe: one rook per row AND per column\n(column pattern = a permutation of 1..8)", True)
board(axs[1], perm_bad, "not safe: rows 7 and 8 share a column\n(column pattern is not a permutation)", False)
fig.tight_layout()
fig.savefig(OUT + "g1_s4_rooks.png")
plt.close(fig)
print("wrote g1_s4_rooks.png")

# ----------------------------------------------------------------- Fig 4.6
# Hypergeometric PMF, n=20 balls, m=8 red, k=5 drawn (rec04 P3)
nH, mH, kH = 20, 8, 5
iv = np.arange(0, kH + 1)
pmf = np.array([comb(mH, int(i)) * comb(nH - mH, kH - int(i)) / comb(nH, kH) for i in iv])
fig, ax = plt.subplots(figsize=(6.6, 3.8))
ax.bar(iv, pmf, width=0.42, color=PAL[0], zorder=3)
for i, p in zip(iv, pmf):
    ax.text(i, p + 0.012, f"{p:.4f}", ha="center", va="bottom", fontsize=9, color=INK)
ax.axvline(kH * mH / nH, color=PAL[1], lw=1.4, ls="--", zorder=2,
           label=r"mean $= km/n = 2$")
ax.set_xticks(iv)
ax.set_xlabel("$i$  (number of red balls drawn)")
ax.set_ylabel("probability")
ax.set_ylim(0, 0.46)
ax.set_title("Hypergeometric PMF:  $n=20$ balls, $m=8$ red, $k=5$ drawn")
ax.legend(loc="upper right")
fig.tight_layout()
fig.savefig(OUT + "g1_s4_hyper.png")
plt.close(fig)
print("wrote g1_s4_hyper.png")
