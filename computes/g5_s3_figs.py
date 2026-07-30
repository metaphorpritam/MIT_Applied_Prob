# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for G5 section 3 - steady-state probabilities and birth-death chains.

Run:  uv run computes/g5_s3_figs.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
from mpl_style import setup, PAL, INK, MUTED, GRID_C, AXIS_C  # noqa: E402

plt, _ = setup()
import matplotlib.patches as mp  # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
BLUE, ORANGE, GREEN, GOLD, PINK, DGREEN, PURPLE, RED = PAL

R = 0.40          # default node radius, data units


def save(fig, name):
    p = IMG / f"g5_s3_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ---------------------------------------------------------------- primitives
def node(ax, x, y, label, r=R, fc="#eef4fc", ec=BLUE, fs=11, tc=INK, lw=1.6):
    ax.add_patch(mp.Circle((x, y), r, fc=fc, ec=ec, lw=lw, zorder=4))
    if label:
        ax.text(x, y, label, ha="center", va="center", fontsize=fs, color=tc, zorder=5)


def _pt(c, r, deg):
    a = np.deg2rad(deg)
    return (c[0] + r * np.cos(a), c[1] + r * np.sin(a))


def arc(ax, cA, cB, degA, degB, rad, label=None, rA=R, rB=R,
        color=MUTED, lw=1.5, fs=10.5, pad=0.13, labcolor=INK, labshift=0.0):
    """Curved arrow from circle cA to circle cB. rad>0 bends to the LEFT of travel.

    (matplotlib's arc3 bends to the RIGHT for positive rad, hence the sign flip.)
    """
    s = _pt(cA, rA, degA)
    e = _pt(cB, rB, degB)
    ax.annotate("", xy=e, xytext=s,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                connectionstyle=f"arc3,rad={-rad}",
                                shrinkA=0, shrinkB=0,
                                mutation_scale=13), zorder=3)
    if label:
        d = np.array([e[0] - s[0], e[1] - s[1]])
        L = np.hypot(*d)
        u = d / L
        perp = np.array([-u[1], u[0]])          # left of travel
        mid = np.array([(s[0] + e[0]) / 2, (s[1] + e[1]) / 2])
        pos = mid + perp * (0.5 * rad * L + np.sign(rad if rad else 1) * pad) + u * labshift
        ax.text(pos[0], pos[1], label, ha="center", va="center",
                fontsize=fs, color=labcolor, zorder=6,
                bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.92))


def selfloop(ax, c, label=None, r=R, up=True, color=MUTED, lw=1.5, fs=10.5, gap=0.16,
             rad=2.1):
    """Loop from state back to itself, drawn above (up=True) or below the node."""
    sgn = 1 if up else -1
    a1, a2 = (118, 62) if up else (-118, -62)
    s, e = _pt(c, r, a1), _pt(c, r, a2)
    if up:
        ax.annotate("", xy=e, xytext=s,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                    connectionstyle=f"arc3,rad={-rad}",
                                    shrinkA=0, shrinkB=0, mutation_scale=13), zorder=3)
    else:
        ax.annotate("", xy=s, xytext=e,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                    connectionstyle=f"arc3,rad={-rad}",
                                    shrinkA=0, shrinkB=0, mutation_scale=13), zorder=3)
    # apex of the quadratic Bezier, measured from the node center
    chord = 2 * r * np.sin(np.deg2rad(28))
    apex = r * np.cos(np.deg2rad(28)) + 0.5 * rad * chord
    if label:
        ax.text(c[0], c[1] + sgn * (apex + gap), label, ha="center",
                va="bottom" if up else "top", fontsize=fs, color=INK, zorder=6)
    return apex


def box(ax, x, y, w, h, text, fc="#eef4fc", ec=BLUE, fs=9.8, tc=INK, lw=1.3, ha="center"):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h,
                                   boxstyle="round,pad=0.010,rounding_size=0.03",
                                   fc=fc, ec=ec, lw=lw, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha=ha, va="center",
            fontsize=fs, color=tc, zorder=5)


def sarrow(ax, p, q, c=MUTED, lw=1.4, label=None, dx=0.0, dy=0.0, fs=9.5):
    ax.annotate("", xy=q, xytext=p,
                arrowprops=dict(arrowstyle="-|>", color=c, lw=lw,
                                shrinkA=2, shrinkB=2, mutation_scale=13), zorder=3)
    if label:
        ax.text((p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, label,
                ha="center", va="center", fontsize=fs, color=INK, zorder=6,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))


# ======================================================================
# Fig 3.1 - the two-state chain of L17 slide 7 / L18 slide 3
# ======================================================================
def fig_twostate():
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    ax.set_xlim(-1.5, 5.0)
    ax.set_ylim(-1.5, 2.5)
    ax.set_aspect("equal"); ax.axis("off"); ax.grid(False)

    c1, c2 = (0.0, 0.0), (3.4, 0.0)
    node(ax, *c1, "1", r=0.52)
    node(ax, *c2, "2", r=0.52, fc="#fdf0e8", ec=ORANGE)
    selfloop(ax, c1, r"$p_{11}=0.5$", r=0.52, up=True)
    selfloop(ax, c2, r"$p_{22}=0.8$", r=0.52, up=True, color=MUTED)
    arc(ax, c1, c2, 35, 145, 0.30, r"$p_{12}=0.5$", rA=0.52, rB=0.52)
    arc(ax, c2, c1, -145, -35, 0.30, r"$p_{21}=0.2$", rA=0.52, rB=0.52)

    ax.text(0.0, -1.30, r"$\pi_1=2/7\approx0.2857$", ha="center", va="center",
            fontsize=10.5, color=BLUE)
    ax.text(3.4, -1.30, r"$\pi_2=5/7\approx0.7143$", ha="center", va="center",
            fontsize=10.5, color=ORANGE)
    save(fig, "twostate")


# ======================================================================
# Fig 3.2 - convergence of r_ij(n)
# ======================================================================
def fig_converge():
    P = np.array([[0.5, 0.5], [0.2, 0.8]])
    ns = np.arange(0, 21)
    r11 = np.array([np.linalg.matrix_power(P, n)[0, 0] for n in ns])
    r21 = np.array([np.linalg.matrix_power(P, n)[1, 0] for n in ns])
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.9))

    a = axes[0]
    a.plot(ns, r11, "o-", color=BLUE, ms=4.5, label=r"$r_{11}(n)$  (start in 1)")
    a.plot(ns, r21, "s-", color=ORANGE, ms=4.0, label=r"$r_{21}(n)$  (start in 2)")
    a.axhline(2 / 7, color=DGREEN, lw=1.4, ls="--")
    a.text(14.5, 2 / 7 + 0.035, r"$\pi_1=2/7$", color=DGREEN, fontsize=10)
    a.set_xlabel("$n$ (number of transitions)")
    a.set_ylabel(r"$r_{i1}(n)$")
    a.set_title("Both rows converge to the same limit")
    a.set_ylim(0, 1.02)
    a.legend(loc="upper right")

    b = axes[1]
    b.semilogy(ns, np.abs(r11 - 2 / 7) + 1e-18, "o-", color=BLUE, ms=4.5,
               label=r"$|r_{11}(n)-\pi_1|$")
    b.semilogy(ns, np.abs(r21 - 2 / 7) + 1e-18, "s-", color=ORANGE, ms=4.0,
               label=r"$|r_{21}(n)-\pi_1|$")
    b.semilogy(ns, (5 / 7) * 0.3 ** ns, "--", color=MUTED, lw=1.3,
               label=r"$\frac{5}{7}(0.3)^n$")
    b.set_xlabel("$n$")
    b.set_ylabel("distance to the limit")
    b.set_title(r"Geometric decay at rate $|\lambda_2| = 0.3$")
    b.set_ylim(1e-12, 1)
    b.legend(loc="upper right")
    fig.tight_layout()
    save(fig, "converge")


# ======================================================================
# Fig 3.3 - frequency interpretation of the balance equation
# ======================================================================
def fig_flowj():
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.set_xlim(-0.6, 10.4)
    ax.set_ylim(-2.5, 2.9)
    ax.set_aspect("equal"); ax.axis("off"); ax.grid(False)

    cj = (5.0, 0.0)
    node(ax, *cj, "$j$", r=0.55, fc="#e8f6f1", ec=DGREEN, fs=12)
    selfloop(ax, cj, r"$\pi_j p_{jj}$", r=0.55, up=True)

    ks = [(0.9, 1.7), (0.9, 0.0), (0.9, -1.7)]
    labs = [r"$\pi_{k_1}p_{k_1 j}$", r"$\pi_{k_2}p_{k_2 j}$", r"$\pi_{k_3}p_{k_3 j}$"]
    names = ["$k_1$", "$k_2$", "$k_3$"]
    for c, lab, nm in zip(ks, labs, names):
        node(ax, *c, nm, r=0.42, fc="#eef4fc", ec=BLUE, fs=10.5)
        d = np.array([cj[0] - c[0], cj[1] - c[1]])
        u = d / np.hypot(*d)
        s = (c[0] + 0.42 * u[0], c[1] + 0.42 * u[1])
        e = (cj[0] - 0.58 * u[0], cj[1] - 0.58 * u[1])
        sarrow(ax, s, e, c=BLUE, lw=1.6)
        ax.text((s[0] + e[0]) / 2, (s[1] + e[1]) / 2 + (0.30 if c[1] >= 0 else -0.34),
                lab, ha="center", va="center", fontsize=10, color=BLUE, zorder=6,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.92))

    outs = [(9.1, 1.7), (9.1, 0.0), (9.1, -1.7)]
    olabs = [r"$\pi_j p_{j\ell_1}$", r"$\pi_j p_{j\ell_2}$", r"$\pi_j p_{j\ell_3}$"]
    for c, lab in zip(outs, olabs):
        d = np.array([c[0] - cj[0], c[1] - cj[1]])
        u = d / np.hypot(*d)
        s = (cj[0] + 0.58 * u[0], cj[1] + 0.58 * u[1])
        sarrow(ax, s, c, c=ORANGE, lw=1.6)
        ax.text(c[0] + 0.05, c[1] + (0.34 if c[1] >= 0 else -0.36), lab,
                ha="center", va="center", fontsize=10, color=ORANGE, zorder=6)

    ax.text(2.6, 2.55, "flow IN", fontsize=11, color=BLUE, ha="center", weight="600")
    ax.text(7.7, 2.55, "flow OUT", fontsize=11, color=ORANGE, ha="center", weight="600")
    ax.text(5.0, -2.05,
            r"$\sum_k \pi_k p_{kj}\;=\;\pi_j\;=\;\pi_j\sum_\ell p_{j\ell}$",
            ha="center", va="center", fontsize=13, color=INK)
    ax.text(5.0, -2.50, "total flow into $j$   =   long-run frequency of $j$"
                        "   =   total flow out of $j$",
            ha="center", va="center", fontsize=9.5, color=MUTED)
    save(fig, "flowj")


# ======================================================================
# Fig 3.4 - recipe flowchart
# ======================================================================
def fig_recipe():
    fig, ax = plt.subplots(figsize=(10.4, 6.6))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 6.9)
    ax.axis("off"); ax.grid(False)

    box(ax, 2.6, 6.05, 5.2, 0.66,
        "START: chain with transition probabilities $p_{ij}$\n"
        "you want long-run behavior", fc="#f2f2ee", ec=AXIS_C)
    box(ax, 2.3, 5.02, 5.8, 0.62,
        "How many recurrent classes?  (§2)", fc="#fdf7e6", ec=GOLD)
    sarrow(ax, (5.2, 6.05), (5.2, 5.64))

    box(ax, 0.05, 3.85, 3.05, 0.86,
        "TWO OR MORE\nlimit depends on $X_0$: first find the\nabsorption probabilities (§4), then\napply steady state inside each class",
        fc="#fdeeee", ec=RED, fs=8.6)
    sarrow(ax, (2.6, 5.33), (1.6, 4.71))

    box(ax, 3.9, 3.85, 4.3, 0.62, "EXACTLY ONE — is it periodic? (§2)",
        fc="#fdf7e6", ec=GOLD)
    sarrow(ax, (6.05, 5.02), (6.05, 4.47))

    box(ax, 7.1, 2.62, 3.25, 0.86,
        "PERIODIC\n$r_{ij}(n)$ does NOT converge, but the\nbalance equations still have a unique\nsolution = long-run visit frequencies",
        fc="#fdeeee", ec=RED, fs=8.6)
    sarrow(ax, (8.2, 3.85), (8.7, 3.48))

    box(ax, 2.7, 2.62, 4.0, 0.62,
        "APERIODIC — steady state exists:\n$r_{ij}(n)\\to\\pi_j$ for every $i$", fc="#e8f6f1", ec=DGREEN, fs=9.4)
    sarrow(ax, (5.4, 3.85), (5.0, 3.24))

    box(ax, 2.3, 1.68, 4.8, 0.55,
        "Are ALL transitions to nearest neighbors only?", fc="#fdf7e6", ec=GOLD)
    sarrow(ax, (4.7, 2.62), (4.7, 2.23))

    box(ax, 0.05, 0.20, 4.55, 1.10,
        "YES — birth-death chain\nUse LOCAL balance across each cut:\n"
        "$\\pi_i p_i=\\pi_{i+1}q_{i+1}$, telescope to\n"
        "$\\pi_i=\\pi_0\\prod_{k=1}^{i}(p_{k-1}/q_k)$, then normalize",
        fc="#eef4fc", ec=BLUE, fs=8.8)
    sarrow(ax, (3.4, 1.68), (2.4, 1.30))

    box(ax, 5.15, 0.20, 5.15, 1.10,
        "NO — general chain\nSolve the $m\\times m$ linear system:\n"
        "keep $m-1$ of the balance equations $\\pi_j=\\sum_k\\pi_k p_{kj}$\n"
        "(they are dependent — drop any one) plus $\\sum_j\\pi_j=1$",
        fc="#eef4fc", ec=BLUE, fs=8.8)
    sarrow(ax, (6.0, 1.68), (7.0, 1.30))

    ax.text(1.90, 5.04, "$\\geq 2$", fontsize=9, color=RED, ha="center")
    ax.text(6.35, 4.75, "$1$", fontsize=9, color=DGREEN, ha="center")
    ax.text(8.75, 3.68, "yes", fontsize=9, color=RED, ha="center")
    ax.text(5.55, 3.55, "no", fontsize=9, color=DGREEN, ha="center")
    ax.text(2.55, 1.52, "yes", fontsize=9, color=BLUE, ha="center")
    ax.text(6.85, 1.52, "no", fontsize=9, color=BLUE, ha="center")
    save(fig, "recipe")


# ======================================================================
# Fig 3.5 - birth-death chain with the cut (signature figure, L17 slide 8)
# ======================================================================
def fig_bdchain():
    fig, ax = plt.subplots(figsize=(12.4, 5.4))
    ax.set_xlim(-1.0, 15.6)
    ax.set_ylim(-4.6, 2.9)
    ax.set_aspect("equal"); ax.axis("off"); ax.grid(False)

    xs = [0.0, 2.4, 5.6, 8.0, 11.2, 13.6]
    lab = ["$0$", "$1$", "$i$", "$i{+}1$", "$m{-}1$", "$m$"]
    cs = [(x, 0.0) for x in xs]
    for c, L in zip(cs, lab):
        node(ax, *c, L, r=0.52, fs=10.5)

    for xe in [4.0, 9.6]:
        ax.text(xe, 0.0, r"$\cdots$", ha="center", va="center", fontsize=17,
                color=MUTED, zorder=6,
                bbox=dict(boxstyle="round,pad=0.20", fc="white", ec="none"))

    pairs = [(0, 1, "$p_0$", "$q_1$"),
             (2, 3, "$p_i$", "$q_{i+1}$"),
             (4, 5, "$p_{m-1}$", "$q_m$")]
    for a, b, pl, ql in pairs:
        arc(ax, cs[a], cs[b], 35, 145, 0.30, pl, rA=0.52, rB=0.52, color=BLUE)
        arc(ax, cs[b], cs[a], -145, -35, 0.30, ql, rA=0.52, rB=0.52, color=ORANGE)
    # neighbour links across the ellipses (unlabeled)
    for a, b in [(1, 2), (3, 4)]:
        arc(ax, cs[a], cs[b], 32, 148, 0.22, None, rA=0.52, rB=0.52, color=GRID_C)
        arc(ax, cs[b], cs[a], -148, -32, 0.22, None, rA=0.52, rB=0.52, color=GRID_C)

    selfloop(ax, cs[0], "$1-p_0$", r=0.52)
    selfloop(ax, cs[1], "$1-p_1-q_1$", r=0.52)
    selfloop(ax, cs[2], "$1-p_i-q_i$", r=0.52)
    selfloop(ax, cs[3], "$1-p_{i+1}-q_{i+1}$", r=0.52)
    selfloop(ax, cs[4], None, r=0.52)
    selfloop(ax, cs[5], "$1-q_m$", r=0.52)

    # the cut
    xc = (xs[2] + xs[3]) / 2
    ax.plot([xc, xc], [-4.2, 2.30], ls=(0, (6, 5)), color=RED, lw=1.7, zorder=1)
    ax.text(xc, 2.45, "CUT", ha="center", va="bottom", fontsize=10.5, color=RED,
            weight="600")
    ax.text(xc - 2.0, -1.45, r"states $\{0,\dots,i\}$", ha="center", fontsize=10,
            color=MUTED)
    ax.text(xc + 2.2, -1.45, r"states $\{i{+}1,\dots,m\}$", ha="center", fontsize=10,
            color=MUTED)

    # flow-balance annotation across the cut
    ax.annotate("", xy=(xc + 1.15, -2.45), xytext=(xc - 1.15, -2.45),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.0, mutation_scale=15))
    ax.text(xc, -2.15, r"frequency of $i\to i{+}1$ crossings $=\pi_i p_i$",
            ha="center", va="bottom", fontsize=10, color=BLUE, zorder=7,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))
    ax.annotate("", xy=(xc - 1.15, -3.30), xytext=(xc + 1.15, -3.30),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.0, mutation_scale=15))
    ax.text(xc, -3.62, r"frequency of $i{+}1\to i$ crossings $=\pi_{i+1}q_{i+1}$",
            ha="center", va="top", fontsize=10, color=ORANGE, zorder=7,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))

    ax.add_patch(mp.FancyBboxPatch((11.35, -3.65), 3.6, 0.95,
                                   boxstyle="round,pad=0.10,rounding_size=0.10",
                                   fc="#e8f6f1", ec=DGREEN, lw=1.4, zorder=4))
    ax.text(13.15, -3.17, "LOCAL BALANCE\n$\\pi_i p_i=\\pi_{i+1}q_{i+1}$",
            ha="center", va="center", fontsize=11, color=INK, zorder=6)
    save(fig, "bdchain")


# ======================================================================
# Fig 3.6 - pi for several load factors
# ======================================================================
def fig_pirho():
    m = 10
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.7), sharey=True)
    cases = [(0.5, BLUE, r"$\rho=0.5$  ($p=0.2,\ q=0.4$)"),
             (1.0, DGREEN, r"$\rho=1$  ($p=q=0.3$)"),
             (1.5, RED, r"$\rho=1.5$  ($p=0.45,\ q=0.30$)")]
    ii = np.arange(m + 1)
    for ax, (rho, col, ttl) in zip(axes, cases):
        if abs(rho - 1) < 1e-12:
            pi = np.full(m + 1, 1 / (m + 1))
        else:
            pi = (1 - rho) / (1 - rho ** (m + 1)) * rho ** ii
        ax.vlines(ii, 0, pi, color=col, lw=1.6)
        ax.plot(ii, pi, "o", color=col, ms=6)
        ax.set_title(ttl, fontsize=10)
        ax.set_xlabel("state $i$ = number in system")
        ax.set_xticks(range(0, m + 1, 2))
        EX = float(np.dot(ii, pi))
        ax.text(0.96, 0.90, f"$\\mathbb{{E}}[X]={EX:.3f}$", transform=ax.transAxes,
                ha="right", va="top", fontsize=10, color=INK,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=GRID_C))
    axes[0].set_ylabel(r"$\pi_i$")
    axes[0].set_ylim(0, 0.56)
    fig.tight_layout()
    save(fig, "pirho")


# ======================================================================
# Fig 3.7 - the load blow-up
# ======================================================================
def fig_loadblow():
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    rr = np.linspace(0.01, 0.985, 400)
    ax.plot(rr, rr / (1 - rr), color=BLUE, lw=2.4, label=r"infinite buffer: $\rho/(1-\rho)$")
    for m, col, ls in [(10, ORANGE, "--"), (30, DGREEN, "-."), (100, PURPLE, ":")]:
        vals = []
        for rho in rr:
            vals.append(rho / (1 - rho) - (m + 1) * rho ** (m + 1) / (1 - rho ** (m + 1)))
        ax.plot(rr, vals, ls, color=col, lw=1.8, label=f"buffer $m={m}$")
    for rho in [0.5, 0.8, 0.9, 0.95]:
        ax.plot([rho], [rho / (1 - rho)], "o", color=BLUE, ms=5.5)
        ax.annotate(f"$\\rho={rho}$\n$\\mathbb{{E}}[X]={rho/(1-rho):.0f}$",
                    xy=(rho, rho / (1 - rho)), xytext=(rho - 0.30, rho / (1 - rho) + 2.0),
                    fontsize=9, color=MUTED,
                    arrowprops=dict(arrowstyle="-", color=GRID_C, lw=1.0))
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 24)
    ax.set_xlabel(r"load factor $\rho=p/q$")
    ax.set_ylabel(r"$\mathbb{E}[X]$ in steady state")
    ax.set_title(r"Expected queue length blows up as $\rho\to1$")
    ax.legend(loc="upper left")
    fig.tight_layout()
    save(fig, "loadblow")


# ======================================================================
# Fig 3.8 - the phone-company chain (L18 slide 4)
# ======================================================================
def fig_phonechain():
    fig, ax = plt.subplots(figsize=(12.0, 3.9))
    ax.set_xlim(-1.0, 14.6)
    ax.set_ylim(-2.6, 2.7)
    ax.set_aspect("equal"); ax.axis("off"); ax.grid(False)

    xs = [0.0, 2.4, 5.4, 7.8, 10.8, 13.2]
    lab = ["$0$", "$1$", "$i{-}1$", "$i$", "$B{-}1$", "$B$"]
    cs = [(x, 0.0) for x in xs]
    for c, L in zip(cs, lab):
        node(ax, *c, L, r=0.55, fs=10.5, fc="#fdf7e6", ec=GOLD)
    ax.text(3.9, 0.0, r"$\cdots$", ha="center", va="center", fontsize=16, color=MUTED)
    ax.text(9.3, 0.0, r"$\cdots$", ha="center", va="center", fontsize=16, color=MUTED)

    pairs = [(0, 1, r"$\lambda\delta$", r"$1\cdot\mu\delta$"),
             (2, 3, r"$\lambda\delta$", r"$i\mu\delta$"),
             (4, 5, r"$\lambda\delta$", r"$B\mu\delta$")]
    for a, b, pl, ql in pairs:
        arc(ax, cs[a], cs[b], 35, 145, 0.28, pl, rA=0.55, rB=0.55, color=BLUE)
        arc(ax, cs[b], cs[a], -145, -35, 0.28, ql, rA=0.55, rB=0.55, color=ORANGE)
    for a, b in [(1, 2), (3, 4)]:
        arc(ax, cs[a], cs[b], 32, 148, 0.20, None, rA=0.55, rB=0.55, color=GRID_C)
        arc(ax, cs[b], cs[a], -148, -32, 0.20, None, rA=0.55, rB=0.55, color=GRID_C)
    for c in cs:
        selfloop(ax, c, None, r=0.55)

    ax.text(6.6, 2.30, r"up = a new call arrives in the slot  ($\lambda\delta$)",
            ha="center", fontsize=10, color=BLUE)
    ax.text(6.6, -2.20,
            r"down = one of the $i$ calls in progress ends  ($i\mu\delta$)",
            ha="center", fontsize=10, color=ORANGE)
    ax.text(13.2, 1.55, "state $B$: all lines busy\n$\\to$ next call is BLOCKED",
            ha="center", va="bottom", fontsize=9.5, color=RED)
    save(fig, "phonechain")


# ======================================================================
# Fig 3.9 - Erlang-B blocking probability
# ======================================================================
def fig_erlangb():
    def block(a, B):
        E = 1.0
        for k in range(1, B + 1):
            E = a * E / (k + a * E)
        return E

    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    Bs = np.arange(1, 16)
    for a, col, mk in [(3.0, BLUE, "o"), (5.0, ORANGE, "s"), (8.0, PURPLE, "^")]:
        ax.semilogy(Bs, [block(a, B) for B in Bs], mk + "-", color=col, ms=5,
                    label=f"offered load $a=\\lambda/\\mu={a:.0f}$ erlangs")
    ax.axhline(0.01, color=DGREEN, ls="--", lw=1.3)
    ax.text(1.2, 0.0125, "1% target", color=DGREEN, fontsize=9.5, ha="left")
    ax.plot([8], [block(3.0, 8)], "o", color=RED, ms=9, mfc="none", mew=2)
    ax.annotate("$a=3$: $B=8$ lines gives\n$\\mathbf{P}(\\mathrm{block})=0.00813$",
                xy=(8, block(3.0, 8)), xytext=(3.6, 6e-4), fontsize=9, color=MUTED,
                ha="left", arrowprops=dict(arrowstyle="-", color=GRID_C, lw=1.0))
    ax.set_xlabel("$B$ = number of lines")
    ax.set_ylabel(r"$\pi_B=\mathbf{P}(\text{call blocked})$")
    ax.set_title("Erlang-B blocking probability (L18 slide 4)")
    ax.set_ylim(1e-5, 1.2)
    ax.set_xticks(range(1, 16, 2))
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, "erlangb")


if __name__ == "__main__":
    fig_twostate()
    fig_converge()
    fig_flowj()
    fig_recipe()
    fig_bdchain()
    fig_pirho()
    fig_loadblow()
    fig_phonechain()
    fig_erlangb()
    print("done")
