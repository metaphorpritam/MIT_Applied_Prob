# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G4 section 3 — The Poisson process I (L14 + rec14).

Run:  uv run computes/g4_s3_figs.py
"""
from __future__ import annotations

import math
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
    p = IMG / f"g4_s3_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


def pois(k, mu):
    return math.exp(-mu) * mu ** k / math.factorial(k)


def binom(k, n, p):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def box(ax, x, y, w, h, text, fc="#eef4fc", ec=BLUE, fs=9.5, tc=INK, r=0.02, lw=1.3, va="center"):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h,
                                   boxstyle=f"round,pad=0.006,rounding_size={r}",
                                   fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va=va, fontsize=fs, color=tc, zorder=5)


def arrow(ax, x1, y1, x2, y2, c=MUTED, lw=1.4, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=c, lw=lw, shrinkA=2, shrinkB=2))


# =====================================================================
# Fig 3.1 — the three defining properties, as a timeline schematic
# =====================================================================
def fig_smallint():
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(9.4, 5.3),
                                 gridspec_kw={"height_ratios": [1.05, 1.0], "hspace": 0.18})

    # ---------- top: the L14 slide-3 timeline ----------
    ax.axis("off")
    ax.set_xlim(-0.4, 10.6)
    ax.set_ylim(-1.7, 2.5)
    ax.annotate("", xy=(10.45, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.0))
    ax.text(10.5, -0.35, "time", fontsize=9.5, color=MUTED, ha="right", va="top")
    ax.text(0.0, -0.35, "0", fontsize=9.5, color=MUTED, ha="center", va="top")

    arrivals = [0.55, 1.35, 2.15, 3.05, 4.15, 5.30, 6.35, 6.75, 7.95, 9.05, 9.75]
    for a in arrivals:
        ax.plot([a], [0], marker="x", ms=8, mew=2.2, color=INK, zorder=4)

    spans = [(0.20, 2.60, "$t_1$", BLUE), (2.60, 3.60, "$t_2$", ORANGE),
             (4.70, 7.15, "$t_3$", GREEN), (8.85, 9.25, "$\\delta$", RED)]
    for (a, b, lab, c) in spans:
        for e in (a, b):
            ax.plot([e, e], [0, 1.05], color=c, lw=1.1, ls=(0, (3, 3)))
        ax.annotate("", xy=(b, 0.80), xytext=(a, 0.80),
                    arrowprops=dict(arrowstyle="<|-|>", color=c, lw=1.6))
        ax.text((a + b) / 2, 1.18, lab, fontsize=12, color=c, ha="center", va="bottom")

    counts = [(1.40, "3 arrivals", BLUE), (3.10, "1", ORANGE),
              (5.92, "3 arrivals", GREEN), (9.05, "1", RED)]
    for (x, s, c) in counts:
        ax.text(x, -0.62, s, fontsize=8.6, color=c, ha="center", va="top")
    ax.text(5.2, 2.15,
            "counts in disjoint intervals are independent; each depends only on the length",
            fontsize=9.4, color=MUTED, ha="center", va="center")
    ax.text(9.05, -1.15, "one \"slot\" of\nwidth $\\delta$", fontsize=8.6,
            color=RED, ha="center", va="top")

    # ---------- bottom: the delta slot blown up ----------
    bx.axis("off")
    bx.set_xlim(0, 10)
    bx.set_ylim(0, 3.9)
    bx.text(0.05, 3.78, "Zoom on a slot of width $\\delta$  —  small-interval probabilities",
            fontsize=10, color=INK, ha="left", va="top", fontweight="600")
    rows = [("$k=0$  no arrival", "$P(0,\\delta)=1-\\lambda\\delta+o(\\delta)$", "#eef4fc", BLUE),
            ("$k=1$  one arrival", "$P(1,\\delta)=\\lambda\\delta+o_1(\\delta)$", "#fdf0e8", ORANGE),
            ("$k\\geq 2$  two or more", "$P(k,\\delta)=o_k(\\delta)$  (negligible)", "#f3f2ee", MUTED)]
    y = 2.20
    for (lab, form, fc, ec) in rows:
        box(bx, 0.15, y, 3.05, 0.62, lab, fc=fc, ec=ec, fs=9.4)
        box(bx, 3.45, y, 4.55, 0.62, form, fc="white", ec=GRID_C, fs=10)
        y -= 0.78
    bx.text(8.25, 1.62,
            "so a slot is\nalmost a Bernoulli\ntrial with $p=\\lambda\\delta$",
            fontsize=9.0, color=MUTED, ha="left", va="center")
    save(fig, "smallint")


# =====================================================================
# Fig 3.2 — binomial -> Poisson: overlay + error decay
# =====================================================================
def fig_binlimit():
    MU = 2.5
    ks = np.arange(0, 10)
    pk = np.array([pois(int(k), MU) for k in ks])
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10.2, 3.9),
                                 gridspec_kw={"width_ratios": [1.35, 1.0], "wspace": 0.28})

    ns = [5, 10, 100]
    cols = [ORANGE, GOLD, GREEN]
    w = 0.20
    for i, (n, c) in enumerate(zip(ns, cols)):
        vals = [binom(int(k), n, MU / n) if k <= n else 0.0 for k in ks]
        ax.bar(ks + (i - 1.5) * w, vals, width=w * 0.92, color=c, alpha=0.9,
               label=f"binomial $n={n}$, $p={MU/n:g}$", zorder=2)
    ax.plot(ks + 1.5 * w, pk, "o", color=BLUE, ms=6, zorder=4,
            label="Poisson $\\lambda t=2.5$")
    ax.vlines(ks + 1.5 * w, 0, pk, color=BLUE, lw=1.6, zorder=3)
    ax.set_xticks(ks)
    ax.set_xlabel("number of arrivals $k$")
    ax.set_ylabel("probability")
    ax.set_title("Discretize finer, keep $np=\\lambda t=2.5$")
    ax.set_ylim(0, 0.35)
    ax.legend(loc="upper right", fontsize=8.4)

    nn = np.array([5, 10, 20, 50, 100, 200, 500, 1000, 2000])
    dev = [max(abs(binom(int(k), int(n), MU / n) - pois(int(k), MU))
               for k in range(0, min(int(n), 40) + 1)) for n in nn]
    bx.loglog(nn, dev, "o-", color=BLUE, ms=5, label="max$_k|$binom $-$ Poisson$|$")
    bx.loglog(nn, 0.5 / nn, ls=(0, (5, 4)), color=MUTED, lw=1.4, label="reference $0.5/n$")
    bx.set_xlabel("number of slots $n=t/\\delta$")
    bx.set_ylabel("maximum deviation")
    bx.set_title("Error falls like $1/n$")
    bx.legend(loc="lower left", fontsize=8.6)
    bx.grid(True, which="both", color=GRID_C, lw=0.6)
    save(fig, "binlimit")


# =====================================================================
# Fig 3.3 — the Poisson PMF family
# =====================================================================
def fig_poisfam():
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    mus = [0.5, 2.5, 5.0, 10.0]
    cols = [BLUE, ORANGE, GREEN, PURPLE]
    ks = np.arange(0, 21)
    off = [-0.27, -0.09, 0.09, 0.27]
    for mu, c, o in zip(mus, cols, off):
        vals = [pois(int(k), mu) for k in ks]
        ax.vlines(ks + o, 0, vals, color=c, lw=1.7, zorder=2)
        ax.plot(ks + o, vals, "o", color=c, ms=4.2, zorder=3,
                label=f"$\\lambda\\tau={mu:g}$   (mean $=$ var $= {mu:g}$)")
    ax.set_xticks(np.arange(0, 21, 2))
    ax.set_xlim(-0.8, 20.8)
    ax.set_ylim(0, 0.65)
    ax.set_xlabel("number of arrivals $k$ in an interval of length $\\tau$")
    ax.set_ylabel("$P(k,\\tau)$")
    ax.set_title("Poisson PMF $P(k,\\tau)=(\\lambda\\tau)^k e^{-\\lambda\\tau}/k!$")
    ax.legend(loc="upper right", fontsize=9)
    save(fig, "poisfam")


# =====================================================================
# Fig 3.4 — the Erlang family (regenerated from the L14 slide-6 OCW figure)
# =====================================================================
def fig_erlang():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10.2, 3.9), gridspec_kw={"wspace": 0.26})
    lam = 1.0
    y = np.linspace(0, 12, 900)
    cols = [BLUE, ORANGE, GREEN, PURPLE]
    for k, c in zip([1, 2, 3, 6], cols):
        f = lam ** k * y ** (k - 1) * np.exp(-lam * y) / math.factorial(k - 1)
        ax.plot(y, f, color=c, label=f"$k={k}$")
        if k > 1:
            ym = (k - 1) / lam
            ax.plot([ym], [lam ** k * ym ** (k - 1) * math.exp(-lam * ym)
                           / math.factorial(k - 1)], "o", color=c, ms=5)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("$y$  (time of the $k$th arrival)")
    ax.set_ylabel("$f_{Y_k}(y)$")
    ax.set_title("Erlang densities, $\\lambda=1$  (dots mark the peaks at $(k-1)/\\lambda$)")
    ax.legend(loc="upper right", fontsize=9)

    # right panel: Erlang as the sum of k exponential interarrival times
    bx.axis("off")
    bx.set_xlim(0, 10)
    bx.set_ylim(-0.4, 4.6)
    bx.text(0.1, 4.45, "$Y_k=T_1+T_2+\\cdots+T_k$, the $T_i$ i.i.d. $\\mathrm{Exp}(\\lambda)$",
            fontsize=10.2, color=INK, ha="left", va="top", fontweight="600")
    bx.annotate("", xy=(9.7, 1.6), xytext=(0.3, 1.6),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8))
    pts = [0.3, 2.2, 3.3, 6.1, 8.6]
    for i, p in enumerate(pts):
        if i:
            bx.plot([p], [1.6], marker="x", ms=8, mew=2.2, color=BLUE, zorder=4)
            bx.text(p, 1.28, f"$Y_{i}$", fontsize=9.5, color=BLUE, ha="center", va="top")
    for i in range(4):
        a, b = pts[i], pts[i + 1]
        bx.annotate("", xy=(b, 2.25), xytext=(a, 2.25),
                    arrowprops=dict(arrowstyle="<|-|>", color=ORANGE, lw=1.4))
        bx.text((a + b) / 2, 2.42, f"$T_{i+1}$", fontsize=9.8, color=ORANGE,
                ha="center", va="bottom")
    bx.text(0.3, 0.72, "each gap is exponential and independent of the others\n"
                       "(memorylessness) $\\Rightarrow$ $\\mathbb{E}[Y_k]=k/\\lambda$, "
                       "$\\mathrm{var}(Y_k)=k/\\lambda^2$",
            fontsize=9.2, color=MUTED, ha="left", va="top")
    bx.text(0.3, 3.35, "$k=1$: exponential.  Adding independent gaps makes the density\n"
                       "unimodal and, for large $k$, bell-shaped (central limit theorem).",
            fontsize=9.2, color=MUTED, ha="left", va="top")
    save(fig, "erlang")


# =====================================================================
# Fig 3.5 — Bernoulli / Poisson correspondence table
# =====================================================================
def fig_corresp():
    rows = [
        ("times of arrival", "discrete: $n=1,2,\\dots$", "continuous: $t\\geq 0$"),
        ("arrival rate", "$p$ per trial", "$\\lambda$ per unit time"),
        ("arrivals in a window", "binomial $(n,p)$", "Poisson $(\\lambda\\tau)$"),
        ("mean / variance", "$np$  /  $np(1-p)$", "$\\lambda\\tau$  /  $\\lambda\\tau$"),
        ("interarrival time", "geometric $(p)$", "exponential $(\\lambda)$"),
        ("mean interarrival", "$1/p$", "$1/\\lambda$"),
        ("time to $k$th arrival", "Pascal order $k$", "Erlang order $k$"),
        ("mean of that time", "$k/p$", "$k/\\lambda$"),
        ("memoryless?", "yes (fresh start each trial)", "yes (fresh start each instant)"),
        ("merging", "$p_1+p_2-p_1p_2$", "$\\lambda_1+\\lambda_2$"),
        ("splitting w.p. $q$", "Bernoulli $(pq)$", "Poisson $(\\lambda q)$"),
    ]
    fig, ax = plt.subplots(figsize=(9.6, 4.9))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(len(rows) + 1.0 - 0.80 * len(rows) - 0.15, len(rows) + 2.6)
    top = len(rows) + 1.0
    xs = [0.1, 3.35, 6.7]
    ws = [3.15, 3.25, 3.2]
    heads = ["", "BERNOULLI  (discrete time)", "POISSON  (continuous time)"]
    hc = ["white", "#fdf0e8", "#eef4fc"]
    he = [GRID_C, ORANGE, BLUE]
    for x, w, h, fc, ec in zip(xs, ws, heads, hc, he):
        ax.add_patch(mp.Rectangle((x, top), w, 0.72, fc=fc, ec=ec, lw=1.4))
        ax.text(x + w / 2, top + 0.36, h, ha="center", va="center",
                fontsize=9.8, color=INK, fontweight="600")
    for i, (lab, b, p) in enumerate(rows):
        y = top - 0.80 * (i + 1)
        band = "#fbfaf7" if i % 2 == 0 else "white"
        for x, w, txt, col in zip(xs, ws, (lab, b, p), (MUTED, INK, INK)):
            ax.add_patch(mp.Rectangle((x, y), w, 0.72, fc=band, ec=GRID_C, lw=0.7))
            ax.text(x + w / 2, y + 0.36, txt, ha="center", va="center", fontsize=9.2, color=col)
    ax.text(5.0, top + 1.15,
            "$n=t/\\delta$,  $p=\\lambda\\delta$,  $np=\\lambda t$ :  let $\\delta\\to 0$ "
            "and every left-hand entry becomes the right-hand one",
            ha="center", va="center", fontsize=9.6, color=MUTED)
    save(fig, "corresp")


# =====================================================================
# Fig 3.6 — decision flowchart: which Poisson random variable?
# =====================================================================
def fig_flow():
    fig, ax = plt.subplots(figsize=(9.8, 5.0))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.0)

    box(ax, 3.15, 4.20, 3.7, 0.62,
        "Poisson process, rate $\\lambda$.\nWhat is the question about?",
        fc="#f3f2ee", ec=MUTED, fs=9.4)

    box(ax, 0.15, 2.75, 2.9, 0.72,
        "a COUNT in a window\nof total length $\\tau$", fc="#eef4fc", ec=BLUE, fs=9.2)
    box(ax, 3.55, 2.75, 2.9, 0.72,
        "the WAIT to the\nnext single arrival", fc="#fdf0e8", ec=ORANGE, fs=9.2)
    box(ax, 6.95, 2.75, 2.9, 0.72,
        "the WAIT to the\n$k$th arrival", fc="#eaf7f1", ec=GREEN, fs=9.2)

    arrow(ax, 4.4, 4.20, 1.6, 3.47)
    arrow(ax, 5.0, 4.20, 5.0, 3.47)
    arrow(ax, 5.6, 4.20, 8.4, 3.47)

    box(ax, 0.15, 1.35, 2.9, 0.95,
        "$N_\\tau\\sim$ Poisson$(\\lambda\\tau)$\n"
        "$P(k,\\tau)=\\frac{(\\lambda\\tau)^ke^{-\\lambda\\tau}}{k!}$\n"
        "$\\mathbb{E}=\\mathrm{var}=\\lambda\\tau$",
        fc="white", ec=BLUE, fs=9.0)
    box(ax, 3.55, 1.35, 2.9, 0.95,
        "$T\\sim$ Exp$(\\lambda)$\n"
        "$f_T(t)=\\lambda e^{-\\lambda t}$\n"
        "$\\mathbb{E}=1/\\lambda$, var $=1/\\lambda^2$",
        fc="white", ec=ORANGE, fs=9.0)
    box(ax, 6.95, 1.35, 2.9, 0.95,
        "$Y_k\\sim$ Erlang$(k,\\lambda)$\n"
        "$f_{Y_k}(y)=\\frac{\\lambda^ky^{k-1}e^{-\\lambda y}}{(k-1)!}$\n"
        "$\\mathbb{E}=k/\\lambda$, var $=k/\\lambda^2$",
        fc="white", ec=GREEN, fs=9.0)

    for x in (1.6, 5.0, 8.4):
        arrow(ax, x, 2.75, x, 2.30)

    box(ax, 0.05, 0.20, 9.9, 0.80,
        "Cross-checks:   $\\mathbf{P}(Y_k>y)=\\sum_{n=0}^{k-1}P(n,y)$    ·    "
        "$\\mathbf{P}(T>t)=P(0,t)=e^{-\\lambda t}$\n"
        "A window need not be one interval — only its total length matters.    ·    "
        "The past is irrelevant: restart the clock whenever convenient.",
        fc="#fbfaf7", ec=GRID_C, fs=8.5)
    save(fig, "flow")


fig_smallint()
fig_binlimit()
fig_poisfam()
fig_erlang()
fig_corresp()
fig_flow()
print("done")
