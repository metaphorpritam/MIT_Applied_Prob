# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G7 section 4 - binary hypothesis testing and the likelihood ratio test.

Run:  uv run computes/g7_s4_figs.py

Every number drawn here is re-derived from the same formulas as computes/g7_s4.py
(and spot-checked against computes/g7_s4.json at the end of the script).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
from mpl_style import setup, PAL, INK, MUTED, GRID_C, AXIS_C, diagram_ax  # noqa: E402

plt, _ = setup()
import matplotlib.patches as mp  # noqa: E402
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL
J = json.loads((ROOT / "computes" / "g7_s4.json").read_text(encoding="utf-8"))
Phi, Phinv = stats.norm.cdf, stats.norm.ppf
z95 = Phinv(0.95)


def save(fig, name):
    p = IMG / f"g7_s4_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print(f"wrote {p.relative_to(ROOT)}")


# =====================================================================
# Fig 4.1 - the two error types as a 2x2 table diagram
# =====================================================================
fig, ax = plt.subplots(figsize=(8.4, 4.0))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis("off")
ax.grid(False)

# grid geometry
x0, y0, cw, ch = 2.5, 0.55, 3.4, 1.55
cols = ["$H_0$ is true", "$H_1$ is true"]
rows = ["Reject $H_0$\n(data in $R$)", "Do not reject $H_0$\n(data in $R^c$)"]
cells = [
    # (row, col): (text, colour, ok?)
    [("FALSE REJECTION\n" + r"prob. $\alpha(R)=\mathbf{P}(X\in R;H_0)$" + "\ntype I error",
      RED, False),
     ("correct detection\n" + r"prob. $1-\beta(R)$" + "\n(the power of the test)", DGREEN, True)],
    [("correct\n" + r"prob. $1-\alpha(R)$", DGREEN, True),
     ("FALSE ACCEPTANCE\n" + r"prob. $\beta(R)=\mathbf{P}(X\notin R;H_1)$" + "\ntype II error",
      ORANGE, False)],
]
for r in range(2):
    for c in range(2):
        txt, col, ok = cells[r][c]
        xx, yy = x0 + c * cw, y0 + (1 - r) * ch
        ax.add_patch(mp.FancyBboxPatch((xx + 0.06, yy + 0.06), cw - 0.12, ch - 0.12,
                                       boxstyle="round,pad=0.02,rounding_size=0.08",
                                       facecolor=col, alpha=0.13 if ok else 0.22,
                                       edgecolor=col, linewidth=1.4))
        ax.text(xx + cw / 2, yy + ch / 2, txt, ha="center", va="center",
                fontsize=8.6, color=INK, linespacing=1.5)
for c in range(2):
    ax.text(x0 + c * cw + cw / 2, y0 + 2 * ch + 0.22, cols[c], ha="center", va="bottom",
            fontsize=10.5, color=INK, fontweight="600")
for r in range(2):
    ax.text(x0 - 0.18, y0 + (1 - r) * ch + ch / 2, rows[r], ha="right", va="center",
            fontsize=9.5, color=INK, linespacing=1.5)
ax.text(x0 + cw, y0 + 2 * ch + 0.78, "the unknown truth  (not random — no prior)",
        ha="center", va="bottom", fontsize=9.5, color=MUTED, style="italic")
ax.text(0.28, y0 + ch, "your\ndecision", ha="center", va="center", rotation=90,
        fontsize=9.5, color=MUTED, style="italic", linespacing=1.4)
ax.set_title("The two error types of a binary test (L25 slide 2; B&T §9.3)", pad=10)
save(fig, "errortable")

# =====================================================================
# Fig 4.2 - two densities, threshold, shaded alpha and beta
#   n = 4 i.i.d. N(0,1) vs N(1,1); statistic S = sum X_i ~ N(0,4) vs N(4,4)
# =====================================================================
n = 4
sd = np.sqrt(n)
xip = np.sqrt(n) * z95            # 3.2897
alpha = 1 - stats.norm.cdf(xip, 0, sd)
beta = stats.norm.cdf(xip, n, sd)
xs = np.linspace(-7, 11, 900)
f0 = stats.norm.pdf(xs, 0, sd)
f1 = stats.norm.pdf(xs, n, sd)

fig, ax = plt.subplots(figsize=(8.6, 4.4))
ax.plot(xs, f0, color=BLUE, lw=2.0, label=r"$f_S(s;H_0)=N(0,4)$")
ax.plot(xs, f1, color=ORANGE, lw=2.0, label=r"$f_S(s;H_1)=N(4,4)$")
m = xs >= xip
ax.fill_between(xs[m], 0, f0[m], color=BLUE, alpha=0.38, lw=0)
m2 = xs <= xip
ax.fill_between(xs[m2], 0, f1[m2], color=ORANGE, alpha=0.30, lw=0)
ax.axvline(xip, color=INK, lw=1.6, ls="--")
ax.annotate(r"$\xi'=\sqrt{n}\,z_{0.95}=3.290$", xy=(xip, 0.205), xytext=(xip + 1.1, 0.216),
            fontsize=9.5, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
ax.annotate(r"$\alpha=0.050$", xy=(4.35, 0.012), xytext=(6.4, 0.075), fontsize=10,
            color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))
ax.annotate(r"$\beta=0.361$", xy=(1.9, 0.030), xytext=(-4.4, 0.105), fontsize=10,
            color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
ax.text(-4.6, 0.192, "accept $H_0$", fontsize=9.5, color=MUTED)
ax.text(6.0, 0.192, "reject $H_0$", fontsize=9.5, color=MUTED)
ax.set_xlabel(r"value of the statistic $s=\sum_{i=1}^{4} x_i$")
ax.set_ylabel("density")
ax.set_ylim(0, 0.235)
ax.set_xlim(-7, 11)
ax.legend(loc="upper left", fontsize=9)
ax.set_title("Where $\\alpha$ and $\\beta$ live: one threshold, two tails "
             "(L25 slide 3, $n=4$)", pad=8)
save(fig, "twodensity")

# =====================================================================
# Fig 4.3 - the alpha/beta tradeoff as xi moves (B&T Figure 9.9)
#   left: continuous case (n = 4 normal mean test)
#   right: discrete case (B&T Example 9.10 loaded die, one roll)
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.0))
ax = axes[0]
xi = np.exp(np.linspace(-6, 6, 700))          # xi > 0
xip_g = np.log(xi) + n / 2                    # threshold on sum X_i
a_g = 1 - stats.norm.cdf(xip_g, 0, sd)
b_g = stats.norm.cdf(xip_g, n, sd)
lx = np.log(xi)
ax.plot(lx, a_g, color=BLUE, lw=2.0, label=r"$\alpha(\xi)$  false rejection")
ax.plot(lx, b_g, color=ORANGE, lw=2.0, label=r"$\beta(\xi)$  false acceptance")
ax.axvline(np.log(np.exp(xip - n / 2)), color=INK, ls="--", lw=1.3)
ax.plot([np.log(3.6317)], [0.05], "o", color=BLUE, ms=6, zorder=5)
ax.plot([np.log(3.6317)], [0.3612], "o", color=ORANGE, ms=6, zorder=5)
ax.annotate(r"$\xi=3.632$", xy=(np.log(3.6317), 0.62), xytext=(np.log(3.6317) + 0.5, 0.72),
            fontsize=9, color=INK, arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
ax.set_xlabel(r"$\log \xi$   (threshold on the likelihood ratio)")
ax.set_ylabel("error probability")
ax.set_ylim(-0.03, 1.03)
ax.legend(loc="lower left", bbox_to_anchor=(0.01, 0.20), fontsize=8.6)
ax.set_title("continuous $L(X)$: every $\\alpha$ is reachable", fontsize=10)

ax = axes[1]
# one roll of the B&T 9.10 die: L takes only 3/4 and 3/2
gg = np.linspace(0.2, 2.2, 600)
a_d = np.where(gg < 0.75, 1.0, np.where(gg < 1.5, 1 / 3, 0.0))
b_d = np.where(gg < 0.75, 0.0, np.where(gg < 1.5, 0.5, 1.0))
ax.plot(gg, a_d, color=BLUE, lw=2.2, label=r"$\alpha(\xi)$")
ax.plot(gg, b_d, color=ORANGE, lw=2.2, label=r"$\beta(\xi)$")
for xv in (0.75, 1.5):
    ax.axvline(xv, color=AXIS_C, lw=1.0, ls=":")
ax.plot([0.75, 1.5], [1 / 3, 1 / 3], "o", color=BLUE, ms=5, mfc="white", mew=1.6, zorder=5)
ax.text(0.79, 0.07, r"only $\alpha\in\{0,\frac{1}{3},1\}$" + "\nis attainable",
        fontsize=9, color=MUTED, linespacing=1.4)
ax.text(0.30, 0.86, r"$\xi<\frac{3}{4}$", fontsize=9, color=MUTED)
ax.text(0.92, 0.86, r"$\frac{3}{4}<\xi<\frac{3}{2}$", fontsize=9, color=MUTED)
ax.text(1.60, 0.86, r"$\xi>\frac{3}{2}$", fontsize=9, color=MUTED)
ax.set_xlabel(r"$\xi$   (threshold on the likelihood ratio)")
ax.set_ylabel("error probability")
ax.set_ylim(-0.03, 1.03)
ax.legend(loc="center right", fontsize=8.6)
ax.set_title("discrete $L(X)$: $\\alpha=0.05$ is unreachable", fontsize=10)
fig.suptitle("Raising $\\xi$ shrinks $R$: $\\alpha$ falls, $\\beta$ rises "
             "(B&T §9.3 and its Figure 9.9)", y=1.02, fontsize=11, fontweight="600")
fig.tight_layout()
save(fig, "tradeoff")

# =====================================================================
# Fig 4.4 - ROC curves
#   left : normal shift family, power = Phi(d - z_{1-alpha})
#   right: the discrete die, 4 rolls, staircase of attainable points
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.3))
ax = axes[0]
aa = np.linspace(1e-5, 1 - 1e-5, 1200)
for d, col, lab in [(0.5, GOLD, r"$d=0.5$"), (1.0, GREEN, r"$d=1$"),
                    (2.0, ORANGE, r"$d=2$"), (np.sqrt(10), BLUE, r"$d=\sqrt{10}$  ($n=10$)")]:
    ax.plot(aa, 1 - Phi(Phinv(1 - aa) - d), color=col, lw=2.0, label=lab)
    ax.plot([0.05], [1 - Phi(z95 - d)], "o", color=col, ms=5.5, zorder=5)
ax.plot([0, 1], [0, 1], color=MUTED, lw=1.2, ls="--")
ax.text(0.55, 0.47, "useless test ($d=0$)", fontsize=8.6, color=MUTED, rotation=32)
ax.axvline(0.05, color=AXIS_C, lw=1.0, ls=":")
# opaque bbox: this label sits on top of the dashed "useless test" diagonal
ax.text(0.075, 0.055, r"$\alpha=0.05$", fontsize=8.6, color=MUTED,
        bbox=dict(boxstyle="round,pad=0.20", fc="white", ec="none", alpha=0.92))
ax.set_xlabel(r"$\alpha$  = false rejection probability")
ax.set_ylabel(r"power $1-\beta$")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.02)
ax.legend(loc="lower right", fontsize=8.6)
ax.set_title("ROC of the normal-shift LRT", fontsize=10)

ax = axes[1]
aK = [1.0, 0.802469, 0.407407, 0.111111, 0.0123457, 0.0]
bK = [0.0, 0.0625, 0.3125, 0.6875, 0.9375, 1.0]
pw = [1 - b for b in bK]
ax.plot(aK, pw, color=BLUE, lw=1.6, ls="--", zorder=2)
ax.plot(aK, pw, "o", color=BLUE, ms=7, zorder=3, label=r"LRT points $\{K\geq k\}$")
# every label here risks landing on the dashed diagonal, the blue frontier or the
# y = 0 gridline, so each is offset away from its neighbouring line AND given an
# opaque bbox so no line can strike through the glyphs
labs = [("$k=0$", (-46, 4)), ("$k=1$", (-8, -16)), ("$k=2$", (14, -13)),
        ("$k=3$", (12, -3)), ("$k=4$", (15, 9)), ("never reject", (16, -15))]
for a_, p_, (k, off) in zip(aK, pw, labs):
    ax.annotate(k, xy=(a_, p_), xytext=off, textcoords="offset points",
                fontsize=8.4, color=MUTED,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.92))
# a deliberately bad region: reject when K <= 1 (the wrong tail)
aBad = 1 - stats.binom.sf(1, 4, 1 / 3)
pBad = 1 - stats.binom.sf(1, 4, 0.5)
ax.plot([aBad], [pBad], "s", color=RED, ms=7, zorder=4, label=r"a bad region $\{K\leq 1\}$")
ax.plot([0, 1], [0, 1], color=MUTED, lw=1.2, ls="--")
ax.set_xlabel(r"$\alpha$")
ax.set_ylabel(r"power $1-\beta$")
ax.set_xlim(-0.03, 1.03)
ax.set_ylim(-0.11, 1.05)   # headroom below y = 0 for the "never reject" label
ax.legend(loc="lower right", fontsize=8.6)
ax.set_title("discrete case: 4 rolls of the B&T 9.10 die", fontsize=10)
fig.suptitle("Neyman-Pearson: nothing lies above the LRT curve "
             "(B&T §9.3, Figure 9.12)", y=1.02, fontsize=11, fontweight="600")
fig.tight_layout()
save(fig, "roc")

# =====================================================================
# Fig 4.5 - the coin significance test (L25 slide 5)
# =====================================================================
nC = 1000
sdC = np.sqrt(250)
ks = np.arange(430, 571)
pmf = stats.binom.pmf(ks, nC, 0.5)
fig, ax = plt.subplots(figsize=(8.8, 4.2))
inR = np.abs(ks - 500) > 31
ax.bar(ks[~inR], pmf[~inR], width=1.0, color=BLUE, alpha=0.55, lw=0,
       label=r"$|s-500|\leq 31$: do not reject")
ax.bar(ks[inR], pmf[inR], width=1.0, color=RED, alpha=0.85, lw=0,
       label=r"rejection region $|s-500|>31$")
xx = np.linspace(430, 570, 600)
ax.plot(xx, stats.norm.pdf(xx, 500, sdC), color=INK, lw=1.6,
        label=r"CLT approximation $N(500,250)$")
ax.axvline(472, color=DGREEN, lw=2.0)
ax.annotate("observed $s=472$\n$|s-500|=28<31$", xy=(472, 0.0175), xytext=(432, 0.0215),
            fontsize=9.2, color=DGREEN, linespacing=1.4,
            arrowprops=dict(arrowstyle="->", color=DGREEN, lw=1.2))
# the region is |s-500| > 31 and s is an integer, so the extreme *rejected*
# counts are 468 and 532 (469 and 531 are still inside the acceptance region)
for xv, lab in ((468, r"$468$"), (532, r"$532$")):
    ax.annotate(lab, xy=(xv, 0.0016), xytext=(xv + (-16 if xv < 500 else 6), 0.0072),
                fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
ax.set_xlabel("number of heads $s$ in $n=1000$ tosses")
ax.set_ylabel("probability / density")
ax.set_xlim(430, 570)
ax.set_ylim(0, 0.0285)
ax.legend(loc="upper right", fontsize=8.8)
ax.set_title(r"Is my coin fair? $H_0:\theta=1/2$ at the 5% level (L25 slide 5; B&T Example 9.15)",
             pad=8)
save(fig, "coin")

# =====================================================================
# Fig 4.6 - chi-square goodness of fit for the die (L25 slide 6, B&T Ex. 9.18)
# =====================================================================
fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.1))
ax = axes[0]
counts = np.array([92, 120, 88, 98, 95, 107])
faces = np.arange(1, 7)
ax.bar(faces - 0.19, counts, width=0.36, color=BLUE, alpha=0.85, lw=0, label="observed $n_k$")
ax.bar(faces + 0.19, [100] * 6, width=0.36, color=MUTED, alpha=0.45, lw=0,
       label=r"expected $n\theta_k^*=100$")
for f, c in zip(faces, counts):
    ax.text(f - 0.19, c + 3, str(c), ha="center", fontsize=8.4, color=INK)
ax.set_xticks(faces)
ax.set_xlabel("face $k$")
ax.set_ylabel("count in $n=600$ rolls")
ax.set_ylim(0, 168)
ax.legend(loc="upper center", ncol=2, fontsize=8.6)
ax.set_title("the data (B&T Example 9.18)", fontsize=10)

ax = axes[1]
t = np.linspace(0, 22, 800)
ax.plot(t, stats.chi2.pdf(t, 5), color=BLUE, lw=2.0, label=r"$\chi^2_5$ density")
crit = stats.chi2.ppf(0.95, 5)
m = t >= crit
ax.fill_between(t[m], 0, stats.chi2.pdf(t[m], 5), color=RED, alpha=0.35, lw=0)
ax.axvline(crit, color=RED, lw=1.5, ls="--")
ax.axvline(6.86, color=DGREEN, lw=2.0)
ax.plot([stats.chi2.ppf(0.75, 5)], [0], marker="^", color=GOLD, ms=10,
        clip_on=False, zorder=6)
# the green label goes in the gap BETWEEN the green line at 6.86 and the red
# dashed line at 11.07, so no dash can strike through it
ax.annotate(r"$T=6.86$", xy=(6.86, 0.040), xytext=(7.05, 0.132), fontsize=9.4, color=DGREEN,
            ha="left",
            arrowprops=dict(arrowstyle="->", color=DGREEN, lw=1.1))
# the red label drops well clear of the orange block above it
ax.annotate(r"$\xi=11.07$" + "\n" + r"($\alpha=0.05$)", xy=(crit, 0.022), xytext=(12.7, 0.046),
            fontsize=9, color=RED, linespacing=1.4,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
# one ax.text per line, on a fixed pitch: mixing mathtext and plain lines inside a
# single multi-line string gives visibly uneven leading
gold_lines = [r"$\blacktriangle = 6.63$,", r"the $\alpha = 0.25$", r"critical value:",
              r"$T > 6.63$, so at", r"the 25% level", r"$H_0$ IS rejected"]
for i, ln in enumerate(gold_lines):
    ax.text(14.6, 0.138 - 0.0118 * i, ln, fontsize=8.2, color=GOLD, va="center", ha="left")
ax.set_xlabel(r"value of $T=\sum_k (N_k-n\theta_k^*)^2/(n\theta_k^*)$")
ax.set_ylabel("density")
ax.set_ylim(0, 0.165)
ax.legend(loc="upper right", fontsize=8.6)
ax.set_title(r"reject iff $T>\xi$; here $6.86<11.07$", fontsize=10)
fig.suptitle("Is my die fair? the chi-square goodness-of-fit test (L25 slide 6)",
             y=1.02, fontsize=11, fontweight="600")
fig.tight_layout()
save(fig, "chisq")

# =====================================================================
# Fig 4.7 - Kolmogorov-Smirnov (L25 slide 7, redrawn)
# =====================================================================
good = np.load(ROOT / "computes" / "g7_s4_kssample.npy")
bad = np.load(ROOT / "computes" / "g7_s4_ksbad.npy")


def ks_panel(ax, samp, title, col, tx=None):
    xs = np.sort(samp)
    nn = len(xs)
    hi = np.arange(1, nn + 1) / nn
    lo = np.arange(0, nn) / nn
    F = Phi(xs)
    gaps = np.maximum(hi - F, F - lo)
    j = int(np.argmax(gaps))
    D = float(gaps[j])
    grid = np.linspace(-3.6, 3.6, 500)
    ax.plot(grid, Phi(grid), color=MUTED, lw=1.8, ls="--", label=r"hypothesized $F_X$ ($N(0,1)$)")
    ax.step(np.concatenate([[-3.6], xs, [3.6]]),
            np.concatenate([[0], hi, [1]]), where="post",
            color=col, lw=1.6, label=r"empirical CDF $\widehat F_X$")
    yb, yt = sorted([F[j], hi[j] if (hi[j] - F[j]) >= (F[j] - lo[j]) else lo[j]])
    ax.annotate("", xy=(xs[j], yt), xytext=(xs[j], yb),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=2.0))
    mid = (yb + yt) / 2
    tpos = tx if tx is not None else (xs[j] + 0.40, mid - 0.26)
    ax.annotate(rf"$D_n={D:.3f}$" + "\n" + rf"$\sqrt{{n}}D_n={np.sqrt(nn)*D:.2f}$",
                xy=(xs[j], mid), xytext=tpos,
                fontsize=9.2, color=RED, linespacing=1.5,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(-0.02, 1.05)
    ax.set_xlabel("$x$")
    ax.set_ylabel("cumulative probability")
    ax.legend(loc="upper left", fontsize=8.4)
    ax.set_title(title, fontsize=10)


fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.2))
ks_panel(axes[0], good, r"100 genuine $N(0,1)$ draws: $\sqrt{n}D_n=0.57<1.36$" + "\nnot rejected", BLUE)
ks_panel(axes[1], bad, r"100 centered exponential draws: $\sqrt{n}D_n=1.60>1.36$" + "\nrejected",
         ORANGE, tx=(1.15, 0.32))
fig.suptitle(r"Kolmogorov-Smirnov: reject when $\sqrt{n}\,D_n\geq 1.36$ (L25 slide 7)",
             y=1.02, fontsize=11, fontweight="600")
fig.tight_layout()
save(fig, "ks")

# =====================================================================
# Fig 4.8 - decision flowchart: which test?
# =====================================================================
fig, ax = plt.subplots(figsize=(9.8, 7.6))
ax.set_xlim(0, 10)
ax.set_ylim(0.4, 9.9)
ax.axis("off")
ax.grid(False)


def box(x, y, w, h, text, fc, ec, fs=9.0, weight="normal"):
    ax.add_patch(mp.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                   boxstyle="round,pad=0.04,rounding_size=0.12",
                                   facecolor=fc, edgecolor=ec, linewidth=1.4, alpha=0.95))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK,
            linespacing=1.45, fontweight=weight)


def diamond(x, y, w, h, text, fs=8.8):
    ax.add_patch(mp.Polygon([[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]],
                            closed=True, facecolor="#f7f6f0", edgecolor=MUTED, linewidth=1.3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=INK, linespacing=1.4)


def arrow(x1, y1, x2, y2, label="", lx=0, ly=0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4,
                                shrinkA=2, shrinkB=2))
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, fontsize=8.4,
                color=MUTED, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))


SP = 2.55            # x of the decision spine
OX = 7.35            # x of the outcome column
DW, DH = 4.5, 1.35   # diamond width / height
OW = 4.9             # outcome box width

box(SP, 9.35, 4.9, 0.72,
    "You must choose between competing\nprobabilistic explanations of the data",
    "#eef3fb", BLUE, 9.2, "600")
arrow(SP, 8.99, SP, 8.42)

diamond(SP, 7.74, DW, DH,
        "Is there a genuine PRIOR\nprobability on the hypotheses?")
arrow(SP + DW / 2, 7.74, OX - OW / 2, 7.74, "yes", ly=0.24)
box(OX, 7.74, OW, 1.05,
    "Bayesian MAP test  (G6 §3)\n"
    r"decide $H_1$ iff $L(x)>\mathbf{P}(H_0)/\mathbf{P}(H_1)$" + "\n"
    "minimizes the overall error probability", "#eef7f2", DGREEN, 8.3)
arrow(SP, 7.06, SP, 6.32, "no", lx=0.34)

diamond(SP, 5.64, DW, DH,
        "Are BOTH hypotheses SIMPLE\n(one fully specified distribution each)?")
arrow(SP + DW / 2, 5.64, OX - OW / 2, 5.64, "yes", ly=0.24)
box(OX, 5.64, OW, 1.25,
    "Likelihood ratio test  (§4.2–4.6)\n"
    r"reject $H_0$ iff $L(x)=p_X(x;H_1)/p_X(x;H_0)>\xi$" + "\n"
    r"fix $\xi$ by $\mathbf{P}(L(X)>\xi;H_0)=\alpha$" + "\n"
    "optimal by Neyman-Pearson", "#fdf1ea", ORANGE, 8.3)
arrow(SP, 4.96, SP, 4.22, "no", lx=0.34)

diamond(SP, 3.54, DW, 1.55,
        "Does $H_0$ fix ONE scalar parameter\n"
        r"($\theta=\theta^*$), with $H_1$ just $\theta\neq\theta^*$?")
arrow(SP + DW / 2, 3.54, OX - OW / 2, 3.54, "yes", ly=0.24)
box(OX, 3.54, OW, 1.25,
    "Significance test  (§4.7)\n"
    r"pick a statistic $S$, pick the shape of $R$," + "\n"
    r"set $\xi$ from $\mathbf{P}(\mathrm{reject}\,H_0;H_0)=\alpha$" + "\n"
    r"example: $|S-n/2|>\xi$ for a fair coin", "#fdf7e8", GOLD, 8.3)
arrow(SP, 2.76, SP, 2.02, "no", lx=0.34)

box(SP, 1.35, 4.9, 1.35,
    "Goodness of fit  (§4.8)\n"
    r"$H_0$ names a whole distribution, $H_1$ = 'anything else'" + "\n"
    r"generalized LRT $\Rightarrow$ chi-square $T$ (binned/discrete)" + "\n"
    r"or Kolmogorov-Smirnov $D_n$ (continuous CDF)",
    "#f4eefb", PURPLE, 8.3)
ax.set_title("Which test? A decision guide for L25 (B&T §9.3–9.4)", pad=8, fontsize=11.5)
save(fig, "flow")

# =====================================================================
# consistency checks against computes/g7_s4.json
# =====================================================================
print("\nconsistency checks:")
checks = [
    ("MEAN_n4_XIP", xip), ("MEAN_n4_BETA", beta),
    ("Z_0950", z95), ("DIE_T", 6.86),
    ("DIE10N4_ALPHA_K2", stats.binom.sf(1, 4, 1 / 3)),
    ("KS_DN", float(np.max(np.maximum(np.arange(1, 101) / 100 - Phi(np.sort(good)),
                                      Phi(np.sort(good)) - np.arange(0, 100) / 100)))),
]
ok = True
for k, v in checks:
    d = abs(J[k] - v)
    ok &= d < 1e-9
    print(f"  {k:24s} json={J[k]!r:>22}  fig={v!r:>22}  |diff|={d:.2e}")
print("all figure numbers agree with computes/g7_s4.json" if ok else "MISMATCH!")
