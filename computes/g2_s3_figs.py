# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for notes/src/fragments/g2_s3.html  (L06 + rec06 P3 + rec07 P3).

Run:  uv run computes/g2_s3_figs.py
Writes notes/img/g2_s3_*.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "notes" / "_build"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mpl_style import setup, diagram_ax, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Ellipse, Circle, Rectangle  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    p = IMG / f"g2_s3_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


def stem_pmf(ax, xs, ys, color=0, lw=2.4, ms=6):
    c = PAL[color] if isinstance(color, int) else color
    ax.vlines(xs, 0, ys, color=c, lw=lw)
    ax.plot(xs, ys, "o", color=c, ms=ms)
    return c


# =====================================================================
# Fig 3.1  Random speed  (L06 slides 3-4)
# =====================================================================
fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.5))

ax = axes[0]
stem_pmf(ax, [1, 200], [0.5, 0.5], 0)
ax.set_xlim(-18, 235)
ax.set_ylim(0, 0.72)
ax.set_xticks([1, 200])
ax.set_yticks([0, 0.25, 0.5])
ax.set_yticklabels(["0", "", "1/2"])
ax.set_xlabel("speed $v$  (mph)")
ax.set_ylabel("$p_V(v)$")
ax.set_title("(a) PMF of the speed $V$")
ax.plot([100.5, 100.5], [0, 0.55], color=PAL[3], lw=1.3, ls="--", zorder=1)
ax.text(100.5, 0.60, "$\\mathbf{E}[V]=100.5$", ha="center", color=PAL[3], fontsize=9)

ax = axes[1]
stem_pmf(ax, [1, 200], [0.5, 0.5], 1)
ax.set_xlim(-18, 235)
ax.set_ylim(0, 0.72)
ax.set_xticks([1, 200])
ax.set_yticks([0, 0.25, 0.5])
ax.set_yticklabels(["0", "", "1/2"])
ax.set_xlabel("time $t$  (hours)")
ax.set_ylabel("$p_T(t)$")
ax.set_title("(b) PMF of $T=200/V$")
ax.plot([100.5, 100.5], [0, 0.55], color=PAL[3], lw=1.3, ls="--", zorder=1)
ax.text(100.5, 0.60, "$\\mathbf{E}[T]=100.5$", ha="center", color=PAL[3], fontsize=9)

ax = axes[2]
labels = ["$200/\\mathbf{E}[V]$\n(wrong)", "$\\mathbf{E}[T]$\n(right)"]
vals = [200 / 100.5, 100.5]
bars = ax.barh([1, 0], vals, height=0.5, color=[PAL[7], PAL[2]])
ax.set_yticks([1, 0])
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlim(0, 128)
ax.set_xlabel("hours for the 200-mile trip")
ax.set_title("(c) $\\mathbf{E}[g(V)]\\neq g(\\mathbf{E}[V])$")
ax.grid(axis="y", visible=False)
for b, v in zip(bars, vals):
    ax.text(v + 3, b.get_y() + b.get_height() / 2, f"{v:.3f} h" if v < 10 else f"{v:.1f} h",
            va="center", ha="left", fontsize=9, color=INK)
ax.text(64, -0.62, "off by a factor of 50.5", ha="center", fontsize=9, color=MUTED)
ax.set_ylim(-0.9, 1.55)

fig.tight_layout()
save(fig, "speed")

# =====================================================================
# Fig 3.2  Conditional PMF, uniform on {1,2,3,4} given A = {X >= 2}  (L06 slide 5)
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.3))

ax = axes[0]
stem_pmf(ax, [1, 2, 3, 4], [0.25] * 4, 0)
ax.set_xlim(0.3, 4.7)
ax.set_ylim(0, 0.54)
ax.set_xticks([1, 2, 3, 4])
ax.set_yticks([0, 0.25, 1 / 3])
ax.set_yticklabels(["0", "1/4", "1/3"])
ax.set_xlabel("$x$")
ax.set_ylabel("$p_X(x)$")
ax.set_title("(a) unconditional:  $\\mathbf{E}[X]=5/2$")
ax.axvspan(1.5, 4.7, color=PAL[2], alpha=0.10, zorder=0)
ax.text(3.1, 0.46, "$A=\\{X\\geq 2\\}$", ha="center", fontsize=9.5, color=PAL[2])
ax.plot([2.5, 2.5], [0, 0.40], color=PAL[3], ls="--", lw=1.2, zorder=1)
ax.text(2.5, 0.415, "$\\mathbf{E}[X]$", ha="center", fontsize=8.5, color=PAL[3])

ax = axes[1]
ax.vlines([1], 0, [0.25], color=GRID_C, lw=2.4, zorder=1)
ax.plot([1], [0.25], "o", color=GRID_C, ms=6, zorder=1)
ax.text(1.0, 0.27, "removed", ha="center", fontsize=8, color=MUTED)
stem_pmf(ax, [2, 3, 4], [1 / 3] * 3, 2)
ax.set_xlim(0.3, 4.7)
ax.set_ylim(0, 0.54)
ax.set_xticks([1, 2, 3, 4])
ax.set_yticks([0, 0.25, 1 / 3])
ax.set_yticklabels(["0", "1/4", "1/3"])
ax.set_xlabel("$x$")
ax.set_ylabel("$p_{X\\mid A}(x)$")
ax.set_title("(b) conditional on $A$:  $\\mathbf{E}[X\\mid A]=3$")
ax.plot([3.0, 3.0], [0, 0.40], color=PAL[3], ls="--", lw=1.2, zorder=1)
ax.text(3.0, 0.415, "$\\mathbf{E}[X\\mid A]$", ha="center", fontsize=8.5, color=PAL[3])
ax.annotate("each surviving bar rescaled\nby $1/\\mathbf{P}(A)=4/3$", xy=(2, 1 / 3),
            xytext=(2.75, 0.505), ha="center", fontsize=8.5, color=MUTED,
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0))

fig.tight_layout()
save(fig, "condpmf")

# =====================================================================
# Fig 3.3  Geometric PMF, tail, and memorylessness  (L06 slide 6)
# =====================================================================
p = 0.3
K = 12
ks = np.arange(1, K + 1)
pmf = (1 - p) ** (ks - 1) * p

fig = plt.figure(figsize=(11.4, 6.0))
gs = fig.add_gridspec(2, 3, hspace=0.52, wspace=0.30)

# top-left: full PMF with tail P(X > 2) shaded
ax = fig.add_subplot(gs[0, 0])
stem_pmf(ax, ks[:2], pmf[:2], 0)
stem_pmf(ax, ks[2:], pmf[2:], 1)
ax.set_xlim(0.3, K + 0.7)
ax.set_ylim(0, 0.36)
ax.set_xticks([1, 2, 3, 5, 7, 9, 11])
ax.set_xlabel("$k$")
ax.set_ylabel("$p_X(k)$")
ax.set_title(f"(a) geometric PMF, $p={p}$")
ax.axvspan(2.5, K + 0.7, color=PAL[1], alpha=0.10, zorder=0)
ax.text(7.6, 0.30, "$\\mathbf{P}(X>2)=(1-p)^2$\n$=0.49$", ha="center",
        fontsize=8.5, color=PAL[1])
ax.annotate("$p$", xy=(1, pmf[0]), xytext=(1.0, pmf[0] + 0.035), ha="center",
            fontsize=9, color=INK)
ax.annotate("$p(1-p)^2$", xy=(3, pmf[2]), xytext=(5.0, 0.185), fontsize=8.5,
            color=INK, arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0))

# top-middle: conditional PMF of X given X > 2 (renormalized, still on k)
ax = fig.add_subplot(gs[0, 1])
cond = pmf[2:] / (1 - p) ** 2
stem_pmf(ax, ks[2:], cond, 1)
ax.set_xlim(0.3, K + 0.7)
ax.set_ylim(0, 0.36)
ax.set_xticks([1, 3, 5, 7, 9, 11])
ax.set_xlabel("$k$")
ax.set_ylabel("$p_{X\\mid X>2}(k)$")
ax.set_title("(b) condition on $X>2$: renormalize")
ax.annotate("$p$", xy=(3, cond[0]), xytext=(3.0, cond[0] + 0.035), ha="center",
            fontsize=9, color=INK)

# top-right: shifted variable X - 2 given X > 2
ax = fig.add_subplot(gs[0, 2])
stem_pmf(ax, ks[2:] - 2, cond, 2)
ax.set_xlim(0.3, K + 0.7)
ax.set_ylim(0, 0.36)
ax.set_xticks([1, 3, 5, 7, 9, 11])
ax.set_xlabel("$n$")
ax.set_ylabel("$p_{X-2\\mid X>2}(n)$")
ax.set_title("(c) shift back: identical to (a)")
ax.annotate("$p$", xy=(1, cond[0]), xytext=(1.0, cond[0] + 0.035), ha="center",
            fontsize=9, color=INK)

# bottom-left: overlay proving (a) and (c) coincide
ax = fig.add_subplot(gs[1, 0])
ax.vlines(ks, 0, pmf, color=PAL[0], lw=4.5, alpha=0.35)
ax.plot(ks, pmf, "o", color=PAL[0], ms=8, alpha=0.35, label="$p_X(n)$")
ax.plot(ks[: K - 2], cond, "o", color=PAL[2], ms=4.5, label="$p_{X-2\\mid X>2}(n)$")
ax.set_xlim(0.3, K + 0.7)
ax.set_ylim(0, 0.36)
ax.set_xticks([1, 3, 5, 7, 9, 11])
ax.set_xlabel("$n$")
ax.set_ylabel("probability")
ax.set_title("(d) overlay: the two coincide")
ax.legend(fontsize=8, loc="upper right")

# bottom-middle: tail function P(X > k)
ax = fig.add_subplot(gs[1, 1])
kk = np.arange(0, K + 1)
tail = (1 - p) ** kk
ax.plot(kk, tail, "o-", color=PAL[1], ms=4)
ax.set_xlim(-0.4, K + 0.4)
ax.set_ylim(0, 1.06)
ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
ax.set_xlabel("$k$")
ax.set_ylabel("$\\mathbf{P}(X>k)$")
ax.set_title("(e) tail $=(1-p)^k$, pure exponential decay")
ax.annotate("area under the dots\n$=\\sum_{k\\geq 0}\\mathbf{P}(X>k)=\\mathbf{E}[X]=1/p$",
            xy=(4, tail[4]), xytext=(6.6, 0.72), fontsize=8, color=MUTED, ha="center",
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0))

# bottom-right: mean and sd vs p
ax = fig.add_subplot(gs[1, 2])
pv = np.linspace(0.05, 1.0, 300)
ax.plot(pv, 1 / pv, color=PAL[0], label="$\\mathbf{E}[X]=1/p$")
ax.plot(pv, np.sqrt((1 - pv) / pv ** 2), color=PAL[3],
        label="$\\sigma_X=\\sqrt{1-p}/p$")
ax.set_xlim(0, 1.02)
ax.set_ylim(0, 20.5)
ax.set_xlabel("$p$")
ax.set_ylabel("tosses")
ax.set_title("(f) mean and standard deviation")
ax.legend(fontsize=8.5, loc="upper right")

save(fig, "geometric")

# =====================================================================
# Fig 3.4  Total expectation theorem: partition picture  (L06 slide 7)
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.0))

ax = axes[0]
diagram_ax(ax)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
ax.add_patch(Rectangle((0.4, 0.5), 9.2, 4.6, fc="white", ec=AXIS_C, lw=1.6))
# three regions
ax.plot([0.4, 4.4], [3.4, 3.4], color=AXIS_C, lw=1.4)
ax.plot([4.4, 4.4], [0.5, 5.1], color=AXIS_C, lw=1.4)
ax.add_patch(Rectangle((0.4, 3.4), 4.0, 1.7, fc=PAL[0], alpha=0.10, ec="none"))
ax.add_patch(Rectangle((0.4, 0.5), 4.0, 2.9, fc=PAL[1], alpha=0.10, ec="none"))
ax.add_patch(Rectangle((4.4, 0.5), 5.2, 4.6, fc=PAL[2], alpha=0.10, ec="none"))
ax.text(1.2, 4.7, "$A_1$", fontsize=12, color=PAL[0], ha="center")
ax.text(1.2, 1.0, "$A_2$", fontsize=12, color=PAL[1], ha="center")
ax.text(9.0, 1.0, "$A_3$", fontsize=12, color=PAL[2], ha="center")
ax.text(0.4, 5.45, "$\\Omega$", fontsize=12, color=MUTED)
ax.add_patch(Ellipse((5.0, 2.9), 7.4, 1.5, angle=-8, fc=MUTED, alpha=0.30,
                     ec=INK, lw=1.2))
ax.text(7.9, 3.55, "$B$", fontsize=12, color=INK)
ax.text(5.0, 0.0, "$\\mathbf{P}(B)=\\sum_i \\mathbf{P}(A_i)\\,\\mathbf{P}(B\\mid A_i)$",
        fontsize=10, ha="center", color=INK)
ax.set_title("Partition of $\\Omega$: slice the event $B$")

ax = axes[1]
diagram_ax(ax)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
# bar-chart style: three conditional means averaged
ws = [0.5, 0.3, 0.2]
ms = [2.0, 5.0, 9.0]
x0 = 0.6
tot = 0.0
for i, (w, m) in enumerate(zip(ws, ms)):
    wdt = w * 8.2
    ax.add_patch(Rectangle((x0, 0.9), wdt, 3.4, fc=PAL[i], alpha=0.18, ec=PAL[i], lw=1.3))
    ax.text(x0 + wdt / 2, 3.85, f"$A_{i+1}$", fontsize=11, color=PAL[i], ha="center")
    ax.text(x0 + wdt / 2, 3.15, f"$\\mathbf{{P}}(A_{i+1})={w}$", fontsize=8.5,
            color=INK, ha="center")
    ax.text(x0 + wdt / 2, 2.35, f"$\\mathbf{{E}}[X\\mid A_{i+1}]$", fontsize=8.5,
            color=INK, ha="center")
    ax.text(x0 + wdt / 2, 1.55, f"$={m}$", fontsize=9.5, color=INK, ha="center")
    tot += w * m
    x0 += wdt
ax.text(5.0, 5.05, "weight each conditional mean by its probability", fontsize=9.5,
        ha="center", color=MUTED)
ax.annotate("", xy=(0.6, 4.55), xytext=(8.8, 4.55),
            arrowprops=dict(arrowstyle="<->", color=AXIS_C, lw=1.2))
ax.text(4.7, 0.15,
        f"$\\mathbf{{E}}[X]=0.5(2)+0.3(5)+0.2(9)={tot:.1f}$",
        fontsize=10, ha="center", color=INK)
ax.set_title("Total expectation theorem as a weighted average")

fig.tight_layout()
save(fig, "partition")

# =====================================================================
# Fig 3.5  State diagrams for the two "two-in-a-row" recursions
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.4))


def node(ax, xy, label, color, r=0.52, fs=10.5, fc_alpha=0.14):
    ax.add_patch(Circle(xy, r, fc=color, alpha=fc_alpha, ec=color, lw=1.8, zorder=3))
    ax.text(xy[0], xy[1], label, ha="center", va="center", fontsize=fs,
            color=INK, zorder=4)


def arrow(ax, a, b, color, rad=0.0, lab=None, label="", fs=9, shrink=19):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13,
                                 color=color, lw=1.5,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=shrink, shrinkB=shrink, zorder=2))
    if label and lab is not None:
        ax.text(lab[0], lab[1], label, ha="center", va="center", fontsize=fs,
                color=color, zorder=5,
                bbox=dict(boxstyle="round,pad=0.20", fc="white", ec="none", alpha=0.95))


# --- left: HH or TT (rec07 P3 / Problem 2.33)
ax = axes[0]
diagram_ax(ax)
ax.set_xlim(-0.6, 9.4)
ax.set_ylim(-1.7, 5.2)
node(ax, (1.0, 2.7), "start", PAL[4], r=0.58)
node(ax, (4.4, 4.9), "last = $H$", PAL[0], r=0.78)
node(ax, (4.4, 0.5), "last = $T$", PAL[1], r=0.78)
node(ax, (8.1, 2.7), "STOP", PAL[2], r=0.62)
arrow(ax, (1.0, 2.7), (4.4, 4.9), PAL[0], rad=0.0, lab=(2.35, 4.18), label="$p$")
arrow(ax, (1.0, 2.7), (4.4, 0.5), PAL[1], rad=0.0, lab=(2.35, 1.22), label="$q$")
# H <-> T return arcs: each bows OUTWARD on its own side, so the two never meet.
# H->T bows to the LEFT of the node column, T->H bows to the RIGHT; the label of
# each sits on its own arc's side of the gap.
arrow(ax, (4.4, 4.9), (4.4, 0.5), PAL[1], rad=0.52, lab=(2.95, 2.70), label="$q$",
      shrink=22)
arrow(ax, (4.4, 0.5), (4.4, 4.9), PAL[0], rad=0.52, lab=(5.85, 2.70), label="$p$",
      shrink=22)
arrow(ax, (4.4, 4.9), (8.1, 2.7), PAL[2], rad=0.0, lab=(6.55, 4.32), label="$p$ (HH)")
arrow(ax, (4.4, 0.5), (8.1, 2.7), PAL[2], rad=0.0, lab=(6.55, 1.08), label="$q$ (TT)")
ax.text(4.4, -0.80,
        "$a=\\mathbf{E}[X\\mid H_1]=2p+q(1+b)$,   $b=\\mathbf{E}[X\\mid T_1]=2q+p(1+a)$",
        ha="center", fontsize=9, color=INK)
ax.text(4.4, -1.45, "$\\mathbf{E}[X]=pa+qb=(2+pq)/(1-pq)$", ha="center",
        fontsize=9.5, color=PAL[2])
ax.set_title("(a) stop at HH or TT   (rec07 P3 = B&T Problem 2.33)")

# --- right: HH only
ax = axes[1]
diagram_ax(ax)
ax.set_xlim(-0.6, 9.4)
ax.set_ylim(-1.7, 5.2)
node(ax, (1.3, 2.5), "$S_0$\nno $H$", PAL[4], r=0.75, fs=9.5)
node(ax, (5.0, 2.5), "$S_1$\none $H$", PAL[0], r=0.75, fs=9.5)
node(ax, (8.4, 2.5), "STOP", PAL[2], r=0.62)
arrow(ax, (1.3, 2.5), (5.0, 2.5), PAL[0], rad=0.0, lab=(3.15, 2.86), label="$p$")
arrow(ax, (5.0, 2.5), (8.4, 2.5), PAL[2], rad=0.0, lab=(6.70, 2.86), label="$p$ (HH)")
arrow(ax, (5.0, 2.5), (1.3, 2.5), PAL[1], rad=0.40, lab=(3.15, 4.05),
      label="$q$  (a tail wipes the streak)")
# self-loop on S0
ax.add_patch(FancyArrowPatch((0.98, 1.85), (1.62, 1.85), arrowstyle="-|>",
                             mutation_scale=13, color=PAL[1], lw=1.5,
                             connectionstyle="arc3,rad=2.4", shrinkA=2, shrinkB=2))
ax.text(1.3, 0.68, "$q$", ha="center", fontsize=9, color=PAL[1])
ax.text(4.9, -0.55, "$A=1+pB+qA$,   $B=1+p\\cdot 0+qA$", ha="center",
        fontsize=9.5, color=INK)
ax.text(4.9, -1.30, "$\\Rightarrow\\ A=\\mathbf{E}[N]=(1+p)/p^{2}$  $(=6$ for $p=1/2)$",
        ha="center", fontsize=9.5, color=PAL[2])
ax.set_title("(b) stop at HH only   ($q = 1-p$)")

fig.tight_layout()
save(fig, "states")

# =====================================================================
# Fig 3.6  Recipe flowchart: which tool computes E[X]?
# =====================================================================
fig, ax = plt.subplots(figsize=(10.4, 6.6))
diagram_ax(ax)
ax.set_aspect("auto")
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)


def box(x, y, w, h, text, color, fs=9.2, style="round,pad=0.02,rounding_size=1.6"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=style,
                                fc=color, alpha=0.13, ec=color, lw=1.6, zorder=2))
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=style,
                                fc="none", ec=color, lw=1.6, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK, zorder=4)


def diamond(x, y, w, h, text, color, fs=9.2):
    ax.add_patch(plt.Polygon([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2],
                              [x - w / 2, y]], fc=color, alpha=0.13, ec=color,
                             lw=1.6, zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK, zorder=4)


def link(x1, y1, x2, y2, label="", color=AXIS_C, lab_dx=0, lab_dy=0, fs=8.5):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=12, color=color, lw=1.4,
                                 shrinkA=1, shrinkB=1, zorder=1))
    if label:
        ax.text((x1 + x2) / 2 + lab_dx, (y1 + y2) / 2 + lab_dy, label, fontsize=fs,
                ha="center", va="center", color=MUTED,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))


box(50, 95, 46, 8, "You need $\\mathbf{E}[X]$ (or $\\operatorname{var}(X)$)", PAL[4], fs=10)
diamond(50, 82, 42, 11, "Is the full PMF $p_X$ already in hand?", PAL[3])
box(16, 66, 30, 11,
    "Sum it directly:\n$\\mathbf{E}[X]=\\sum_x x\\,p_X(x)$\n"
    "$\\operatorname{var}(X)=\\mathbf{E}[X^2]-(\\mathbf{E}[X])^2$", PAL[2], fs=8.6)
link(38, 78, 22, 72, "yes", lab_dx=-1.5, lab_dy=1.6)
diamond(64, 63, 40, 12, "Does the experiment restart\nafter a first step?", PAL[3], fs=8.8)
link(62, 77, 64, 69, "no", lab_dx=3.0, lab_dy=0.5)

box(84, 44, 30, 13,
    "Condition on step 1 and use\ntotal expectation:\n"
    "$\\mathbf{E}[X]=\\sum_i\\mathbf{P}(A_i)\\mathbf{E}[X\\mid A_i]$\n"
    "Solve the resulting equation.", PAL[0], fs=8.4)
link(74, 58, 84, 51, "yes", lab_dx=2.4, lab_dy=1.2)

diamond(40, 44, 38, 12, "Is $X=g(Y)$ for a simpler $Y$?", PAL[3], fs=8.8)
link(54, 58, 44, 50, "no", lab_dx=-2.4, lab_dy=1.2)

box(16, 25, 32, 12,
    "Expected-value rule:\n$\\mathbf{E}[g(Y)]=\\sum_y g(y)\\,p_Y(y)$\n"
    "NEVER $g(\\mathbf{E}[Y])$", PAL[1], fs=8.6)
link(30, 39, 20, 32, "yes", lab_dx=-2.4, lab_dy=1.2)

box(58, 22, 32, 11,
    "Split $X$ into indicator or\ncomponent pieces and use\nlinearity of expectation.", PAL[5], fs=8.6)
link(48, 39, 58, 28, "no", lab_dx=2.6, lab_dy=1.0)

box(50, 6, 74, 9,
    "Memorize the geometric answers: $\\mathbf{E}[X]=1/p$,   "
    "$\\operatorname{var}(X)=(1-p)/p^{2}$,   $\\mathbf{E}[X\\mid X>k]=k+1/p$", PAL[2], fs=9)

fig.tight_layout()
save(fig, "flow")

print("done")
