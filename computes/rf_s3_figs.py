# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for RF section 3 — transforms and Simpson's paradox.

Run:  uv run computes/rf_s3_figs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
from mpl_style import setup, diagram_ax, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
import matplotlib.patches as mp  # noqa: E402
import numpy as np  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL


def save(fig, name):
    p = IMG / f"rf_s3_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


def box(ax, x, y, w, h, text, fc="#eef4fc", ec=BLUE, fs=9.5, tc=INK):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h,
                                   boxstyle="round,pad=0.004,rounding_size=0.02",
                                   fc=fc, ec=ec, lw=1.3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=tc, zorder=5)


def arrow(ax, x1, y1, x2, y2, c=MUTED, ls="-", lw=1.3):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=lw, linestyle=ls,
                                shrinkA=1, shrinkB=1))


# =====================================================================
# Fig 3.1 — the two roads from (f_X, f_Y) to f_{X+Y}
# =====================================================================
fig, ax = plt.subplots(figsize=(9.8, 3.6))
diagram_ax(ax)
ax.set_xlim(0, 9.8)
ax.set_ylim(0, 3.6)
ax.set_aspect("auto")

box(ax, 0.10, 1.62, 1.35, 0.66, "$f_X,\\ f_Y$\nindependent", fc="#f3f2ec", ec=AXIS_C)
box(ax, 8.30, 1.62, 1.35, 0.66, "$f_{X+Y}$", fc="#f3f2ec", ec=AXIS_C)

# --- hard road (top lane) ---
box(ax, 2.00, 2.62, 2.55, 0.70, "convolution integral\n$\\int f_X(x)f_Y(w-x)\\,dx$",
    fc="#fdeee7", ec=ORANGE)
box(ax, 4.95, 2.62, 2.90, 0.70, "complete the square, do the\nGaussian integral, simplify",
    fc="#fdeee7", ec=ORANGE)
arrow(ax, 1.45, 2.20, 2.00, 2.85, ORANGE)
arrow(ax, 4.55, 2.97, 4.95, 2.97, ORANGE)
arrow(ax, 7.85, 2.85, 8.55, 2.28, ORANGE)
ax.text(5.40, 2.34, "convolution road (G3 §4): five steps of algebra",
        ha="center", fontsize=9, color=ORANGE)

# --- transform road (bottom lane) ---
box(ax, 2.00, 0.72, 2.15, 0.70, "look up $M_X(t),M_Y(t)$\nin the table", fc="#e9f6f0", ec=DGREEN)
box(ax, 4.55, 0.72, 1.55, 0.70, "multiply\n$M_XM_Y$", fc="#e9f6f0", ec=DGREEN)
box(ax, 6.50, 0.72, 1.70, 0.70, "recognize\nthe product", fc="#e9f6f0", ec=DGREEN)
arrow(ax, 1.45, 1.70, 2.00, 1.15, DGREEN)
arrow(ax, 4.15, 1.07, 4.55, 1.07, DGREEN)
arrow(ax, 6.10, 1.07, 6.50, 1.07, DGREEN)
arrow(ax, 8.20, 1.15, 8.75, 1.62, DGREEN)
ax.text(5.10, 1.62, "transform road: one line", ha="center", fontsize=9, color=DGREEN)

ax.text(4.9, 0.24, "The last step needs no work: the MGF determines the distribution, "
                   "so recognizing the product IS inverting it.",
        ha="center", fontsize=9, color=MUTED, style="italic")

save(fig, "roads")

# =====================================================================
# Fig 3.2 — Simpson's paradox, three panels
# =====================================================================
succ = {("PN", "small"): 234, ("PN", "large"): 55, ("OS", "small"): 81, ("OS", "large"): 192}
tot = {("PN", "small"): 270, ("PN", "large"): 80, ("OS", "small"): 87, ("OS", "large"): 263}
rate = {k: succ[k] / tot[k] for k in succ}
agg = {t_: (succ[(t_, "small")] + succ[(t_, "large")]) / 350 for t_ in ("PN", "OS")}
wsm = {t_: tot[(t_, "small")] / 350 for t_ in ("PN", "OS")}

fig, axes = plt.subplots(1, 3, figsize=(12.4, 3.9))

# --- panel A: the rates -------------------------------------------------
ax = axes[0]
groups = ["Small stones", "Large stones", "All patients"]
os_vals = [rate[("OS", "small")], rate[("OS", "large")], agg["OS"]]
pn_vals = [rate[("PN", "small")], rate[("PN", "large")], agg["PN"]]
xs = np.arange(3)
w = 0.36
b1 = ax.bar(xs - w / 2, os_vals, w, color=BLUE, label="Open surgery")
b2 = ax.bar(xs + w / 2, pn_vals, w, color=ORANGE, label="PN")
for b, v in list(zip(b1, os_vals)) + list(zip(b2, pn_vals)):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.3f}",
            ha="center", fontsize=8.5, color=INK)
ax.set_ylim(0, 1.34)
ax.set_xticks(xs)
ax.set_xticklabels(groups)
ax.set_ylabel("success rate")
ax.set_title("Open surgery wins twice, then loses")
ax.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.02))
ax.annotate("reversal", xy=(2.18, agg["PN"] + 0.05), xytext=(1.62, 1.06),
            fontsize=9, color=RED,
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
ax.grid(axis="x", visible=False)

# --- panel B: the case mix ---------------------------------------------
ax = axes[1]
for i, t_ in enumerate(["OS", "PN"]):
    y = 1 - i
    ax.barh(y, wsm[t_], height=0.42, color=GREEN, label="small stones" if i == 0 else None)
    ax.barh(y, 1 - wsm[t_], height=0.42, left=wsm[t_], color=PURPLE,
            label="large stones" if i == 0 else None)
    ax.text(wsm[t_] / 2, y, f"{tot[(t_,'small')]}\n({wsm[t_]:.3f})", ha="center", va="center",
            fontsize=8.5, color="white")
    ax.text(wsm[t_] + (1 - wsm[t_]) / 2, y, f"{tot[(t_,'large')]}\n({1-wsm[t_]:.3f})",
            ha="center", va="center", fontsize=8.5, color="white")
ax.set_yticks([1, 0])
ax.set_yticklabels(["Open surgery", "PN"])
ax.set_xlim(0, 1)
ax.set_xlabel("share of the 350 patients")
ax.set_title("The lurking variable is unbalanced")
ax.legend(loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.42))
ax.grid(axis="y", visible=False)

# --- panel C: aggregate as a weighted average --------------------------
ax = axes[2]
ws = np.linspace(0, 1, 200)
for t_, c, lab in (("OS", BLUE, "Open surgery"), ("PN", ORANGE, "PN")):
    line = rate[(t_, "large")] + ws * (rate[(t_, "small")] - rate[(t_, "large")])
    ax.plot(ws, line, color=c, label=lab)
    ax.plot([wsm[t_]], [agg[t_]], "o", color=c, ms=8, zorder=5)
    ax.annotate(f"{agg[t_]:.3f}", xy=(wsm[t_], agg[t_]), xytext=(wsm[t_] - 0.02, agg[t_] + 0.028),
                fontsize=9, color=c, ha="right")
ax.axvline(0.51, color=MUTED, ls="--", lw=1.1)
ax.text(0.515, 0.665, "common mix\n$w=0.510$", fontsize=8.5, color=MUTED)
ax.set_xlim(0, 1)
ax.set_ylim(0.66, 0.96)
ax.set_xlabel("$w=\\mathbf{P}(\\mathrm{small\\ stone}\\mid\\mathrm{treatment})$")
ax.set_ylabel("aggregate success rate")
ax.set_title("The aggregate is a weighted average")
ax.legend(loc="upper left")

fig.tight_layout()
save(fig, "simpson")
