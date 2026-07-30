# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for G4 section 2 — random sums and the Bernoulli process.

Run:  uv run computes/g4_s2_figs.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
from mpl_style import setup, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
import matplotlib.patches as mp  # noqa: E402
import numpy as np  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL


def save(fig, name):
    p = IMG / f"g4_s2_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


def box(ax, x, y, w, h, text, fc="#eef4fc", ec=BLUE, fs=9.5, tc=INK, r=0.02, va="center"):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h,
                                   boxstyle=f"round,pad=0.006,rounding_size={r}",
                                   fc=fc, ec=ec, lw=1.3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va=va, fontsize=fs, color=tc, zorder=5)


def arrow(ax, x1, y1, x2, y2, c=MUTED, lw=1.4, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=c, lw=lw, shrinkA=2, shrinkB=2))


# =====================================================================
# Fig 2.1 — Recipe flowchart for random sums
# =====================================================================
def fig_rsrecipe():
    fig, ax = plt.subplots(figsize=(9.4, 4.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.grid(False)

    box(ax, 0.2, 4.15, 9.6, 0.85,
        "START:  $Y = X_1+\\cdots+X_N$   with  $N$ a nonnegative-integer r.v.\n"
        "($Y=0$ when $N=0$);  $X_1,X_2,\\ldots$ i.i.d., and $N,X_1,X_2,\\ldots$ all independent",
        fc="#f4f2ea", ec=AXIS_C, fs=9.5)
    arrow(ax, 2.5, 4.13, 2.5, 3.78)
    arrow(ax, 7.5, 4.13, 7.5, 3.78)

    box(ax, 0.2, 2.85, 4.6, 0.9,
        "1.  CONDITION ON $N=n$\n$Y$ becomes a FIXED sum of $n$ terms\n"
        "$\\mathbf{E}[Y\\,|\\,N=n]=n\\,\\mathbf{E}[X]$", fc="#eef4fc", ec=BLUE, fs=9)
    box(ax, 5.2, 2.85, 4.6, 0.9,
        "2.  CONDITION ON $N=n$, VARIANCE\n$\\mathrm{var}(Y\\,|\\,N=n)=n\\,\\mathrm{var}(X)$\n"
        "(needs the $X_i$ independent of each other)", fc="#fdf1ea", ec=ORANGE, fs=9)
    arrow(ax, 2.5, 2.83, 2.5, 2.48)
    arrow(ax, 7.5, 2.83, 7.5, 2.48)

    box(ax, 0.2, 1.55, 4.6, 0.9,
        "3.  UN-FIX $n$: replace $n$ by $N$\n$\\mathbf{E}[Y\\,|\\,N]=N\\,\\mathbf{E}[X]$\n"
        "(a random variable, a function of $N$)", fc="#eef4fc", ec=BLUE, fs=9)
    box(ax, 5.2, 1.55, 4.6, 0.9,
        "4.  UN-FIX $n$\n$\\mathrm{var}(Y\\,|\\,N)=N\\,\\mathrm{var}(X)$\n"
        "(also a random variable)", fc="#fdf1ea", ec=ORANGE, fs=9)
    arrow(ax, 2.5, 1.53, 2.5, 1.18)
    arrow(ax, 7.5, 1.53, 7.5, 1.18)

    box(ax, 0.2, 0.25, 4.6, 0.9,
        "5.  ITERATED EXPECTATIONS\n$\\mathbf{E}[Y]=\\mathbf{E}[N\\,\\mathbf{E}[X]]$\n"
        "$\\;=\\;\\mathbf{E}[N]\\,\\mathbf{E}[X]$", fc="#eaf7f1", ec=GREEN, fs=9)
    box(ax, 5.2, 0.25, 4.6, 0.9,
        "6.  TOTAL VARIANCE\n$\\mathrm{var}(Y)=\\mathbf{E}[N\\,\\mathrm{var}(X)]"
        "+\\mathrm{var}(N\\,\\mathbf{E}[X])$\n"
        "$\\;=\\;\\mathbf{E}[N]\\mathrm{var}(X)+(\\mathbf{E}[X])^2\\mathrm{var}(N)$",
        fc="#eaf7f1", ec=GREEN, fs=8.6)

    ax.text(0.25, 3.95, "mean track", ha="left", va="top", fontsize=8.5,
            color=BLUE, style="italic")
    ax.text(9.75, 3.95, "variance track", ha="right", va="top", fontsize=8.5,
            color=ORANGE, style="italic")
    save(fig, "rsrecipe")


# =====================================================================
# Fig 2.2 — random-sum simulation: histogram + the two variance terms
# =====================================================================
def fig_rsim():
    rng = np.random.default_rng(41)
    EX, varX = 100.0, 400.0
    half = math.sqrt(3 * varX)
    M = 400_000
    Ns = rng.integers(1, 6, size=M)
    Xs = EX + (rng.random((M, 5)) * 2 - 1) * half
    mask = np.arange(5)[None, :] < Ns[:, None]
    Ys = (Xs * mask).sum(axis=1)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.9),
                             gridspec_kw={"width_ratios": [1.55, 1]})
    ax = axes[0]
    ax.hist(Ys, bins=140, range=(0, 620), density=True, color=BLUE, alpha=0.75,
            edgecolor="none")
    for n in range(1, 6):
        ax.axvline(100 * n, color=AXIS_C, lw=0.9, ls=":", zorder=1)
        ax.text(100 * n, 0.00905, f"$n{{=}}{n}$", ha="center", va="bottom",
                fontsize=8, color=MUTED)
    ax.axvline(300, color=ORANGE, lw=2.0)
    ax.text(300, 0.00755, "$\\mathbf{E}[Y]=300$", ha="center", va="bottom",
            fontsize=9.5, color=ORANGE,
            bbox=dict(fc="white", ec=ORANGE, lw=0.8, pad=2.2))
    ax.set_xlim(0, 620)
    ax.set_ylim(0, 0.0102)
    ax.set_xlabel("$y$   (dollars spent in total)")
    ax.set_ylabel("simulated density of $Y$")
    ax.set_title("$Y=X_1+\\cdots+X_N$:  a mixture of five conditional distributions\n"
                 "(dotted lines: the conditional means $\\mathbf{E}[Y|N=n]=100n$)",
                 fontsize=10.5)

    ax = axes[1]
    labels = ["within\n$\\mathbf{E}[N]\\mathrm{var}(X)$",
              "between\n$(\\mathbf{E}[X])^2\\mathrm{var}(N)$"]
    vals = [3.0 * 400.0, 100.0 ** 2 * 2.0]
    bars = ax.bar([0, 1], vals, width=0.55, color=[BLUE, ORANGE], alpha=0.9)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 500, f"{v:,.0f}",
                ha="center", va="bottom", fontsize=10, color=INK)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, 24000)
    ax.set_ylabel("contribution to $\\mathrm{var}(Y)$")
    ax.set_title("$\\mathrm{var}(Y)=1200+20000=21200$", fontsize=10.5)
    ax.grid(axis="x", visible=False)
    fig.tight_layout(w_pad=2.2)
    save(fig, "rsim")


# =====================================================================
# Fig 2.3 — Bernoulli process sample paths
# =====================================================================
def fig_paths():
    rng = np.random.default_rng(13)
    n = 30
    ps = [0.15, 0.35, 0.70]
    fig, axes = plt.subplots(3, 1, figsize=(9.6, 4.7), sharex=True)
    for ax, p in zip(axes, ps):
        x = (rng.random(n) < p).astype(int)
        ax.set_xlim(0.3, n + 0.7)
        ax.set_ylim(-0.86, 1.0)
        ax.axhline(0, color=AXIS_C, lw=1.2, zorder=1)
        for i in range(1, n + 1):
            ax.plot([i - 0.5, i - 0.5], [-0.12, 0.12], color=AXIS_C, lw=0.8, zorder=1)
        ax.plot([n + 0.5, n + 0.5], [-0.12, 0.12], color=AXIS_C, lw=0.8, zorder=1)
        idx = np.flatnonzero(x) + 1
        ax.vlines(idx, 0, 0.62, color=BLUE, lw=2.0, zorder=3)
        ax.plot(idx, np.full(idx.size, 0.62), "o", ms=6, color=BLUE, zorder=4)
        # interarrival braces for the first three gaps
        prev = 0
        for j, t in enumerate(idx[:3]):
            ax.annotate("", xy=(prev + 0.5, -0.46), xytext=(t + 0.5, -0.46),
                        arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.2))
            ty = -0.78 if j % 2 == 0 else -0.38
            ax.text((prev + t + 1) / 2, ty, f"$T_{{{j+1}}}={t - prev}$",
                    ha="center", va="bottom", fontsize=8.5, color=ORANGE)
            prev = t
        ax.text(0.35, 0.92, f"$p={p}$   ({idx.size} arrivals in $n=30$ slots,"
                            f"  $\\mathbf{{E}}[S]={p*n:.1f}$)",
                ha="left", va="top", fontsize=9.5, color=INK, transform=ax.transData)
        ax.set_yticks([])
        ax.grid(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_visible(False)
    axes[-1].set_xticks([1, 5, 10, 15, 20, 25, 30])
    axes[-1].set_xlabel("trial (time slot) $i$")
    axes[0].set_title("Three sample paths of a Bernoulli process")
    fig.tight_layout(h_pad=0.6)
    save(fig, "paths")


# =====================================================================
# Fig 2.4 — fresh start / memorylessness
# =====================================================================
def fig_fresh():
    fig, axes = plt.subplots(2, 1, figsize=(9.6, 4.6),
                             gridspec_kw={"height_ratios": [1.05, 1]})
    n = 24
    obs = [3, 4, 9, 14]          # observed arrivals in slots 1..12
    fut = [15, 19, 20, 24]       # future arrivals
    ax = axes[0]
    ax.set_xlim(0.3, n + 0.7)
    ax.set_ylim(-1.05, 1.35)
    ax.axhline(0, color=AXIS_C, lw=1.2)
    for i in range(1, n + 2):
        ax.plot([i - 0.5, i - 0.5], [-0.1, 0.1], color=AXIS_C, lw=0.8)
    ax.add_patch(mp.Rectangle((0.5, -0.95), 14.0, 2.15, fc="#eef4fc",
                              ec=BLUE, lw=1.1, zorder=0))
    ax.add_patch(mp.Rectangle((14.5, -0.95), 10.0, 2.15, fc="#eaf7f1",
                              ec=GREEN, lw=1.1, zorder=0))
    for t in obs:
        ax.vlines(t, 0, 0.6, color=BLUE, lw=2.0, zorder=3)
        ax.plot(t, 0.6, "o", ms=6, color=BLUE, zorder=4)
    for t in fut:
        ax.vlines(t, 0, 0.6, color=GREEN, lw=2.0, zorder=3)
        ax.plot(t, 0.6, "o", ms=6, color=GREEN, zorder=4)
    ax.text(7.5, 1.12, "PAST: $X_1,\\ldots,X_{14}$ observed", ha="center", va="top",
            fontsize=9.5, color=BLUE)
    ax.text(19.5, 1.12, "FUTURE: $X_{15},X_{16},\\ldots$", ha="center", va="top",
            fontsize=9.5, color=DGREEN)
    ax.text(19.5, -0.55, "independent of the past, and again Bernoulli($p$)",
            ha="center", va="center", fontsize=9, color=DGREEN, style="italic")
    ax.text(7.5, -0.55, "whatever it was", ha="center", va="center",
            fontsize=9, color=BLUE, style="italic")
    ax.set_yticks([])
    ax.grid(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.set_xticks([1, 5, 10, 14, 15, 20, 24])
    ax.set_title("Fresh-start property: cut anywhere, the future is a brand-new "
                 "Bernoulli process")

    # bottom: memorylessness of the geometric
    ax = axes[1]
    p = 0.3
    ts = np.arange(1, 16)
    pmf = (1 - p) ** (ts - 1) * p
    ax.stem(ts, pmf, linefmt="-", markerfmt="o", basefmt=" ")
    for line in ax.get_lines():
        line.set_color(BLUE)
    (mk,) = ax.plot(ts, pmf, "o", ms=8, color=BLUE, alpha=0.35,
                    label="$p_{T_1}(t)=(1-p)^{t-1}p$   (fresh start)")
    cond = pmf.copy()   # P(T - k = t | T > k) = same geometric
    ax.plot(ts, cond, "o", ms=3.6, color=ORANGE,
            label="$\\mathbf{P}(T-k=t\\mid T>k)$   ($k=5$ failures seen)")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, p * 1.25)
    ax.set_xticks([1, 3, 5, 7, 9, 11, 13, 15])
    ax.set_xlabel("$t$ = number of FURTHER trials until the next success")
    ax.set_ylabel("probability")
    ax.legend(loc="upper right")
    ax.set_title("Memorylessness: the two PMFs coincide exactly ($p=0.3$)",
                 fontsize=10.5)
    fig.tight_layout(h_pad=1.1)
    save(fig, "fresh")


# =====================================================================
# Fig 2.5 — Pascal PMF family
# =====================================================================
def fig_pascal():
    def pas(t, k, p):
        return math.comb(t - 1, k - 1) * p ** k * (1 - p) ** (t - k)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.9))
    ax = axes[0]
    p = 0.3
    for j, k in enumerate([1, 2, 3, 5]):
        ts = np.arange(k, 41)
        ys = [pas(t, k, p) for t in ts]
        ax.plot(ts, ys, "o-", ms=3.4, lw=1.5, color=PAL[j],
                label=f"$k={k}$   ($\\mathbf{{E}}[Y_k]={k/p:.2f}$)")
        ax.axvline(k / p, color=PAL[j], lw=0.9, ls=":", alpha=0.8)
    ax.set_xlim(0, 41)
    ax.set_ylim(0, 0.32)
    ax.set_xlabel("$t$ = trial of the $k$th success")
    ax.set_ylabel("$p_{Y_k}(t)$")
    ax.set_title("Pascal PMF of order $k$, $p=0.3$\n(dotted lines: the means $k/p$)",
                 fontsize=10.5)
    ax.legend(loc="upper right")

    ax = axes[1]
    k = 3
    for j, p in enumerate([0.15, 0.30, 0.50]):
        ts = np.arange(k, 41)
        ys = [pas(t, k, p) for t in ts]
        ax.plot(ts, ys, "o-", ms=3.4, lw=1.5, color=PAL[j],
                label=f"$p={p}$   ($\\mathbf{{E}}[Y_3]={k/p:.2f}$)")
        ax.axvline(k / p, color=PAL[j], lw=0.9, ls=":", alpha=0.8)
    ax.set_xlim(0, 41)
    ax.set_ylim(0, 0.20)
    ax.set_xlabel("$t$ = trial of the 3rd success")
    ax.set_ylabel("$p_{Y_3}(t)$")
    ax.set_title("Order $k=3$ fixed, $p$ varying", fontsize=10.5)
    ax.legend(loc="upper right")
    fig.tight_layout(w_pad=2.0)
    save(fig, "pascal")


# =====================================================================
# Fig 2.6 — splitting and merging (redraw of L13 slides 7-8)
# =====================================================================
def fig_splitmerge():
    orig = [2, 4, 7, 8, 12]
    top = [2, 7, 8]
    bot = [4, 12]
    ns = 14

    def axis_line(ax, y, arrivals, color, label, lx=-0.4):
        ax.annotate("", xy=(ns + 1.15, y), xytext=(0.5, y),
                    arrowprops=dict(arrowstyle="-|>", color=AXIS_C, lw=1.3))
        for i in range(1, ns + 2):
            ax.plot([i - 0.5, i - 0.5], [y - 0.1, y + 0.1], color=AXIS_C, lw=0.8)
        for t in arrivals:
            ax.plot(t, y, "o", ms=7.5, mfc="white", mec=color, mew=1.9, zorder=4)
        ax.text(lx, y, label, ha="right", va="center", fontsize=9, color=color)

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))

    ax = axes[0]
    ax.set_xlim(-3.5, ns + 1.6)
    ax.set_ylim(-2.15, 1.55)
    axis_line(ax, 1.0, top, GREEN, "stream 1\n(kept, $pq$)")
    axis_line(ax, 0.0, orig, BLUE, "original\nBernoulli($p$)")
    axis_line(ax, -1.0, bot, ORANGE, "stream 2\n(discarded, $p(1-q)$)")
    for t in top:
        ax.annotate("", xy=(t, 0.88), xytext=(t, 0.14),
                    arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.2))
    for t in bot:
        ax.annotate("", xy=(t, -0.88), xytext=(t, -0.14),
                    arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.2))
    ax.set_title("SPLITTING: each arrival is routed by an independent coin\n"
                 "(heads w.p. $q$ $\\rightarrow$ stream 1)", fontsize=10.5)
    ax.axis("off")
    ax.grid(False)

    ax = axes[1]
    ax.set_xlim(-3.5, ns + 1.6)
    ax.set_ylim(-2.15, 1.55)
    axis_line(ax, 1.0, [2, 7, 8], GREEN, "process 1\nBernoulli($p$)")
    axis_line(ax, 0.0, orig, BLUE, "merged\nBernoulli($p{+}q{-}pq$)")
    axis_line(ax, -1.0, [4, 7, 12], ORANGE, "process 2\nBernoulli($q$)")
    for t in [2, 7, 8]:
        ax.annotate("", xy=(t, 0.14), xytext=(t, 0.88),
                    arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.2))
    for t in [4, 7, 12]:
        ax.annotate("", xy=(t, -0.14), xytext=(t, -0.88),
                    arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.2))
    ax.plot([7], [0], "o", ms=13, mfc="none", mec=RED, mew=1.4, zorder=5)
    ax.annotate("collision in slot 7:\ncounted as ONE arrival",
                xy=(7.25, -0.06), xytext=(11.2, -1.85), fontsize=8.5, color=RED,
                ha="center",
                arrowprops=dict(arrowstyle="-", color=RED, lw=0.9))
    ax.set_title("MERGING: an arrival in EITHER input is an arrival\n"
                 "in the output stream", fontsize=10.5)
    ax.axis("off")
    ax.grid(False)
    fig.tight_layout(w_pad=1.4)
    save(fig, "splitmerge")


if __name__ == "__main__":
    fig_rsrecipe()
    fig_rsim()
    fig_paths()
    fig_fresh()
    fig_pascal()
    fig_splitmerge()
