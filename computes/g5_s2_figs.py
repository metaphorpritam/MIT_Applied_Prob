# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Figures for G5 section 2 — classification of states.

Run:  uv run computes/g5_s2_figs.py
"""
from __future__ import annotations

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

R = 0.30          # node radius, data units
ARROW = "-|>"


def save(fig, name):
    p = IMG / f"g5_s2_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


# ---------------------------------------------------------------- primitives
def node(ax, xy, label, fc="#ffffff", ec=INK, fs=11, r=R, lw=1.6, tc=INK):
    ax.add_patch(plt.Circle(xy, r, facecolor=fc, edgecolor=ec, lw=lw, zorder=4))
    ax.text(xy[0], xy[1], label, ha="center", va="center", fontsize=fs,
            color=tc, zorder=5)


def _unit(v):
    n = float(np.hypot(v[0], v[1]))
    return np.array(v) / n, n


def edge(ax, p, q, label=None, rad=0.16, c=MUTED, lw=1.5, r=R, fs=9.5,
         loff=0.0, lpad=0.20, tc=INK, zorder=3):
    """Curved arrow p -> q, shrunk to the circle boundaries, label on the bulge."""
    p, q = np.array(p, float), np.array(q, float)
    u, L = _unit(q - p)
    a, b = p + u * r, q - u * r
    ax.annotate("", xy=b, xytext=a, zorder=zorder,
                arrowprops=dict(arrowstyle=ARROW, color=c, lw=lw,
                                connectionstyle=f"arc3,rad={rad}",
                                shrinkA=0, shrinkB=0, mutation_scale=13))
    if label is None:
        return
    perp = np.array([-u[1], u[0]])          # 90 deg CCW: side the arc bulges to
    mid = (a + b) / 2 + perp * (rad * L / 2)
    pos = mid + perp * (lpad if rad >= 0 else -lpad) + u * loff
    ax.text(pos[0], pos[1], label, ha="center", va="center", fontsize=fs,
            color=tc, zorder=6,
            bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.85))


def selfloop(ax, xy, label=None, ang=90, c=MUTED, lw=1.5, r=R, fs=9.5, size=0.62):
    """Loop hanging off the node in direction `ang` (degrees)."""
    x, y = xy
    th = np.radians(ang)
    d = np.array([np.cos(th), np.sin(th)])
    perp = np.array([-d[1], d[0]])
    a = np.array([x, y]) + d * r * 0.75 + perp * r * 0.55
    b = np.array([x, y]) + d * r * 0.75 - perp * r * 0.55
    ax.annotate("", xy=b, xytext=a, zorder=3,
                arrowprops=dict(arrowstyle=ARROW, color=c, lw=lw,
                                connectionstyle="arc3,rad=-2.6",
                                shrinkA=0, shrinkB=0, mutation_scale=13))
    if label is not None:
        pos = np.array([x, y]) + d * (r + 0.52)
        ax.text(pos[0], pos[1], label, ha="center", va="center", fontsize=fs,
                color=INK, zorder=7,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9))


def classbox(ax, pts, color, label, pad=0.62, lab_dy=0.0, fs=10,
             padl=None, padr=None, padt=None, padb=None):
    """Dashed class rectangle. Side pads may be widened to enclose self-loops."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1 = min(xs) - (padl or pad), max(xs) + (padr or pad)
    y0, y1 = min(ys) - (padb or pad), max(ys) + (padt or pad)
    ax.add_patch(mp.FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                                   boxstyle="round,pad=0.02,rounding_size=0.25",
                                   fc=color + "1f", ec=color, lw=1.2,
                                   linestyle=(0, (5, 3)), zorder=1))
    ax.text((x0 + x1) / 2, y1 + 0.12 + lab_dy, label, ha="center", va="bottom",
            fontsize=fs, color=color, zorder=6)


def box(ax, x, y, w, h, text, fc="#eef4fc", ec=BLUE, fs=9.5, tc=INK, r=0.03):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h,
                                   boxstyle=f"round,pad=0.008,rounding_size={r}",
                                   fc=fc, ec=ec, lw=1.3, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=tc, zorder=5)


def farrow(ax, x1, y1, x2, y2, c=MUTED, lw=1.4):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=3,
                arrowprops=dict(arrowstyle=ARROW, color=c, lw=lw,
                                shrinkA=1, shrinkB=1, mutation_scale=13))


# ================================================================= Fig 2.1
def fig_warmup():
    fig, ax = plt.subplots(figsize=(9.8, 4.3))
    ax.set_xlim(-0.60, 10.0)
    ax.set_ylim(-0.15, 4.75)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)

    P = {3: (1.0, 3.2), 4: (3.0, 3.2), 5: (1.0, 1.7),
         1: (3.0, 0.55), 2: (5.1, 1.7), 8: (5.1, 3.2),
         6: (7.4, 2.5), 7: (9.0, 2.5), 9: (7.9, 0.55)}

    # wider on the left/top so the self-loops of states 5 and 3 sit inside the class box
    classbox(ax, [P[3], P[4], P[5]], GREEN, "recurrent class $\\{3,4,5\\}$", pad=0.55,
             padl=1.32, padt=1.05)
    classbox(ax, [P[6], P[7]], BLUE, "recurrent class $\\{6,7\\}$", pad=0.55)

    for k in (3, 4, 5):
        node(ax, P[k], str(k), fc="#e8f6f0", ec=GREEN)
    for k in (6, 7):
        node(ax, P[k], str(k), fc="#e6effb", ec=BLUE)
    for k in (1, 2, 8, 9):
        node(ax, P[k], str(k), fc="#f4f3ee", ec=MUTED)

    selfloop(ax, P[3], "0.2", ang=90)
    selfloop(ax, P[5], "0.4", ang=180)
    selfloop(ax, P[6], "0.3", ang=250)

    edge(ax, P[3], P[4], "0.5", rad=0.20)
    edge(ax, P[4], P[3], "1", rad=0.20)
    edge(ax, P[3], P[5], "0.3", rad=0.22)
    edge(ax, P[5], P[3], "0.6", rad=0.22)
    edge(ax, P[6], P[7], "0.7", rad=0.22)
    edge(ax, P[7], P[6], "1", rad=0.22, lpad=0.26)

    edge(ax, P[1], P[5], "0.2", rad=0.14)
    edge(ax, P[1], P[2], "0.5", rad=0.16, lpad=0.24)
    edge(ax, P[1], P[8], "0.3", rad=0.16, lpad=0.28)
    edge(ax, P[2], P[1], "0.4", rad=0.16, lpad=0.24)
    edge(ax, P[2], P[6], "0.6", rad=0.14)
    edge(ax, P[8], P[4], "0.5", rad=0.14)
    edge(ax, P[8], P[2], "0.5", rad=0.14)
    edge(ax, P[9], P[7], "1", rad=0.14, loff=-0.45, lpad=0.26)

    ax.text(4.05, -0.05, "transient states  1, 2, 8, 9", ha="center", va="bottom",
            fontsize=10, color=MUTED)
    save(fig, "warmup")


# ================================================================= Fig 2.2
def fig_recipe():
    fig, ax = plt.subplots(figsize=(9.9, 6.4))
    ax.set_xlim(-0.15, 10.25)
    ax.set_ylim(0, 6.8)
    ax.axis("off")
    ax.grid(False)

    box(ax, 0.3, 6.0, 9.4, 0.62,
        "START: draw the diagram; keep only the ARCS $p_{ij}>0$ — the numbers do not matter yet",
        fc="#f4f3ee", ec=MUTED)
    box(ax, 0.3, 4.95, 9.4, 0.72,
        "Step 1.  For the state $i$ in question, list $A(i)$ = every state reachable from $i$\n"
        "in $0,1,2,\\dots$ steps (follow arrows forward until nothing new appears)")
    farrow(ax, 5.0, 6.0, 5.0, 5.67)
    farrow(ax, 5.0, 4.95, 5.0, 4.55)

    box(ax, 1.9, 3.85, 6.2, 0.70,
        "Step 2.  Is there some $j\\in A(i)$ with $i\\notin A(j)$\n"
        "(you can get out and not come back)?", fc="#fdf3e8", ec=ORANGE)

    farrow(ax, 8.1, 4.20, 9.15, 4.20)
    ax.text(8.62, 4.30, "YES", ha="center", va="bottom", fontsize=9, color=ORANGE)
    box(ax, 8.05, 2.95, 1.9, 0.75, "$i$ is\nTRANSIENT", fc="#fdecea", ec=RED, fs=9.5)
    farrow(ax, 9.0, 3.85, 9.0, 3.70)

    farrow(ax, 5.0, 3.85, 5.0, 3.42)
    ax.text(5.12, 3.62, "NO", ha="left", va="center", fontsize=9, color=ORANGE)
    box(ax, 1.9, 2.70, 6.2, 0.72,
        "$i$ is RECURRENT.  Its recurrent class is exactly $A(i)$\n"
        "(closed: no arc leaves it; all its states communicate)", fc="#e8f6f0", ec=GREEN)

    farrow(ax, 5.0, 2.70, 5.0, 2.28)
    box(ax, 1.35, 1.50, 7.3, 0.75,
        "Step 3 (period).  $d=\\mathrm{gcd}\\{n\\geq 1: r_{ii}(n)>0\\}=\\mathrm{gcd}$ of the lengths of all\n"
        "cycles through $i$.  Shortcut: a self-loop anywhere in the class $\\Rightarrow d=1$",
        fc="#fdf3e8", ec=ORANGE)

    farrow(ax, 3.0, 1.50, 3.0, 1.12)
    farrow(ax, 7.0, 1.50, 7.0, 1.12)
    box(ax, 0.75, 0.32, 4.0, 0.78,
        "$d=1$: APERIODIC.\nEquivalently $r_{ij}(n)>0$ for all $i,j$ in\nthe class, all large $n$",
        fc="#e8f6f0", ec=GREEN, fs=9)
    box(ax, 5.25, 0.32, 4.0, 0.78,
        "$d>1$: PERIODIC.\nStates split into $d$ groups; transitions\ngo group $1\\to 2\\to\\cdots\\to d\\to 1$",
        fc="#fdecea", ec=RED, fs=9)
    save(fig, "recipe")


# ================================================================= Fig 2.3
def fig_period():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.4))
    for a in axes:
        a.set_aspect("equal")
        a.axis("off")
        a.grid(False)

    # (a) grouping picture, d = 3
    ax = axes[0]
    ax.set_xlim(-0.2, 6.4)
    ax.set_ylim(-0.4, 5.6)
    G = {1: (1.3, 4.3), 2: (5.0, 4.3), 3: (3.15, 1.1)}
    cols = {1: BLUE, 2: ORANGE, 3: GREEN}
    for k, (x, y) in G.items():
        ax.add_patch(mp.FancyBboxPatch((x - 0.85, y - 0.62), 1.7, 1.24,
                                       boxstyle="round,pad=0.02,rounding_size=0.35",
                                       fc=cols[k] + "22", ec=cols[k], lw=1.5, zorder=2))
        ax.text(x, y, f"$S_{k}$", ha="center", va="center", fontsize=13,
                color=cols[k], zorder=5)
    edge(ax, G[1], G[2], None, rad=0.0, r=0.95, lw=1.8, c=INK)
    edge(ax, G[2], G[3], None, rad=0.0, r=0.95, lw=1.8, c=INK)
    edge(ax, G[3], G[1], None, rad=0.0, r=0.95, lw=1.8, c=INK)
    ax.set_title("(a)  a periodic class with $d=3$:\nevery transition steps to the next group",
                 fontsize=10.5, color=INK)
    ax.text(3.15, 5.15, "$S_1\\to S_2\\to S_3\\to S_1\\to\\cdots$", ha="center",
            fontsize=10, color=MUTED)

    # (b) two cycles of lengths 6 and 4 sharing node 0
    ax = axes[1]
    ax.set_xlim(-3.0, 3.3)
    ax.set_ylim(-2.4, 3.5)
    Q = {0: (0.0, -1.75),
         1: (-1.45, -1.35), 2: (-2.20, -0.15), 3: (-1.70, 1.25),
         4: (-0.40, 2.10), 5: (0.55, 1.05),
         6: (1.60, -1.35), 7: (2.45, -0.15), 8: (1.55, 1.15)}
    even = {0, 2, 4, 7}
    for k, xy in Q.items():
        c = BLUE if k in even else ORANGE
        fcc = "#e6effb" if k in even else "#fdf3e8"
        node(ax, xy, str(k), fc=fcc, ec=c, r=0.26, fs=10)
    left = [0, 1, 2, 3, 4, 5, 0]
    right = [0, 6, 7, 8, 0]
    for a, b in zip(left, left[1:]):
        edge(ax, Q[a], Q[b], None, rad=0.06, r=0.26, c=MUTED)
    for a, b in zip(right, right[1:]):
        edge(ax, Q[a], Q[b], None, rad=0.06, r=0.26, c=MUTED)
    ax.text(-2.95, 2.75, "cycle of length 6", fontsize=9.5, color=ORANGE, ha="left")
    ax.text(1.15, 2.15, "cycle\nof length 4", fontsize=9.5, color=BLUE, ha="left")
    ax.text(0.0, -2.32, "$\\gcd(6,4)=2$   $\\Rightarrow$   period $d=2$;  groups = blue / orange",
            ha="center", fontsize=10, color=INK)
    ax.set_title("(b)  L17 slide 4: two cycles sharing one state", fontsize=10.5, color=INK)
    fig.tight_layout()
    save(fig, "period")


# ================================================================= Fig 2.4
def fig_failures():
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.1))
    for a in axes:
        a.set_aspect("equal")
        a.axis("off")
        a.grid(False)

    ax = axes[0]
    ax.set_xlim(-0.6, 5.6)
    ax.set_ylim(-0.85, 2.05)
    A = {1: (0.5, 0.9), 2: (2.5, 0.9), 3: (4.5, 0.9)}
    node(ax, A[1], "1", fc="#e6effb", ec=BLUE)
    node(ax, A[2], "2", fc="#fdf3e8", ec=ORANGE)
    node(ax, A[3], "3", fc="#e6effb", ec=BLUE)
    edge(ax, A[1], A[2], "1", rad=-0.25)
    edge(ax, A[2], A[1], "0.5", rad=-0.25)
    edge(ax, A[2], A[3], "0.5", rad=-0.25)
    edge(ax, A[3], A[2], "1", rad=-0.25)
    ax.set_title("(a)  single recurrent class, but PERIODIC ($d=2$)",
                 fontsize=10.5, color=INK)
    ax.text(2.5, -0.62, "$r_{22}(n)$ alternates $0,1,0,1,\\dots$ — no limit",
            ha="center", fontsize=10, color=MUTED)

    ax = axes[1]
    ax.set_xlim(-0.6, 6.6)
    ax.set_ylim(-0.85, 2.05)
    B = {1: (0.4, 0.9), 2: (2.2, 0.9), 3: (4.0, 0.9), 4: (5.8, 0.9)}
    node(ax, B[1], "1", fc="#e8f6f0", ec=GREEN)
    node(ax, B[2], "2", fc="#f4f3ee", ec=MUTED)
    node(ax, B[3], "3", fc="#e6effb", ec=BLUE)
    node(ax, B[4], "4", fc="#e6effb", ec=BLUE)
    selfloop(ax, B[1], "1", ang=135)
    selfloop(ax, B[2], "0.4", ang=90)
    selfloop(ax, B[3], "0.5", ang=135)
    selfloop(ax, B[4], "0.5", ang=45)
    edge(ax, B[2], B[1], "0.3", rad=-0.22)
    edge(ax, B[2], B[3], "0.3", rad=-0.22)
    edge(ax, B[3], B[4], "0.5", rad=-0.25)
    edge(ax, B[4], B[3], "0.5", rad=-0.25)
    ax.set_title("(b)  TWO recurrent classes $\\{1\\}$ and $\\{3,4\\}$",
                 fontsize=10.5, color=INK)
    ax.text(3.0, -0.62, "$r_{11}(n)=1$, $r_{31}(n)=0$ — the limit depends on the start",
            ha="center", fontsize=10, color=MUTED)
    fig.tight_layout()
    save(fig, "failures")


# ================================================================= Fig 2.5
def fig_convergence():
    A3 = np.array([[0.0, 1.0, 0.0], [0.5, 0.0, 0.5], [0.0, 1.0, 0.0]])
    B4 = np.array([[1.0, 0.0, 0.0, 0.0], [0.3, 0.4, 0.3, 0.0],
                   [0.0, 0.0, 0.5, 0.5], [0.0, 0.0, 0.5, 0.5]])
    ns = np.arange(0, 15)
    r22 = [np.linalg.matrix_power(A3, n)[1, 1] for n in ns]
    r12 = [np.linalg.matrix_power(A3, n)[0, 1] for n in ns]
    r11 = [np.linalg.matrix_power(B4, n)[0, 0] for n in ns]
    r21 = [np.linalg.matrix_power(B4, n)[1, 0] for n in ns]
    r31 = [np.linalg.matrix_power(B4, n)[2, 0] for n in ns]

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.7))
    ax = axes[0]
    ax.plot(ns, r22, "o-", color=PAL[0], label="$r_{22}(n)$  (start at 2)")
    ax.plot(ns, r12, "s--", color=PAL[1], label="$r_{12}(n)$  (start at 1)")
    ax.axhline(0.5, color=MUTED, lw=1.0, ls=":")
    ax.text(0.15, 0.545, "time average $=\\pi_2=1/2$", ha="left", fontsize=9,
            color=MUTED, zorder=8,
            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="none", alpha=0.92))
    ax.set_xlabel("$n$")
    ax.set_ylabel("probability of being in state 2")
    ax.set_ylim(-0.06, 1.12)
    ax.set_title("(a) periodic chain: no convergence", fontsize=10.5)
    ax.legend(loc="center right")

    ax = axes[1]
    ax.plot(ns, r11, "o-", color=PAL[2], label="$r_{11}(n)$  (start at 1)")
    ax.plot(ns, r21, "s-", color=PAL[1], label="$r_{21}(n)$  (start at 2)")
    ax.plot(ns, r31, "^-", color=PAL[0], label="$r_{31}(n)$  (start at 3)")
    ax.axhline(0.5, color=MUTED, lw=1.0, ls=":")
    ax.text(0.15, 0.535, "$1/2$", ha="left", fontsize=9, color=MUTED)
    ax.set_xlabel("$n$")
    ax.set_ylabel("probability of being in state 1")
    ax.set_ylim(-0.06, 1.12)
    ax.set_title("(b) two classes: three different limits", fontsize=10.5)
    ax.legend(loc="center right")
    fig.tight_layout()
    save(fig, "convergence")


# ================================================================= Fig 2.6
def fig_rec18():
    fig, axes = plt.subplots(2, 1, figsize=(9.6, 6.6))
    for a in axes:
        a.set_aspect("equal")
        a.axis("off")
        a.grid(False)

    # (a) fish chain, n = 4
    ax = axes[0]
    ax.set_xlim(-0.6, 9.4)
    ax.set_ylim(-0.9, 1.9)
    F = {i: (0.6 + 2.0 * i, 0.55) for i in range(5)}
    node(ax, F[0], "0", fc="#e8f6f0", ec=GREEN)
    for i in range(1, 5):
        node(ax, F[i], str(i), fc="#f4f3ee", ec=MUTED)
    selfloop(ax, F[0], "1", ang=90)
    # labels in lowest terms, matching Fig. 1.2(b) which draws the same chain
    selfloop(ax, F[1], "3/4", ang=90)
    selfloop(ax, F[2], "1/2", ang=90)
    selfloop(ax, F[3], "1/4", ang=90)
    for i, lb in zip(range(1, 5), ["1/4", "1/2", "3/4", "1"]):
        edge(ax, F[i], F[i - 1], lb, rad=0.0, lpad=0.32)
    ax.text(0.6, -0.42, "recurrent (absorbing)", ha="center", fontsize=9, color=GREEN)
    ax.text(5.6, -0.42, "transient states 1, 2, 3, 4", ha="center", fontsize=9, color=MUTED)
    ax.set_title("(a) rec18 P1 — painting fish, $n=4$: state = number of green fish left",
                 fontsize=10.5, color=INK)

    # (b) rec18 P3 six-state chain
    ax = axes[1]
    ax.set_xlim(-0.6, 9.4)
    ax.set_ylim(-1.7, 2.0)
    S = {1: (0.9, 0.9), 2: (2.7, 0.9), 3: (4.5, 0.9), 4: (6.3, 0.9), 5: (8.1, 0.9),
         0: (4.5, -1.1)}
    node(ax, S[1], "$s_1$", fc="#e8f6f0", ec=GREEN)
    node(ax, S[5], "$s_5$", fc="#e6effb", ec=BLUE)
    for k in (2, 3, 4, 0):
        node(ax, S[k], f"$s_{k}$", fc="#f4f3ee", ec=MUTED)
    selfloop(ax, S[1], "1", ang=135)
    selfloop(ax, S[2], "1/2", ang=90)
    selfloop(ax, S[3], "1/4", ang=90)
    selfloop(ax, S[4], "1/2", ang=90)
    selfloop(ax, S[5], "1", ang=45)
    edge(ax, S[2], S[1], "1/2", rad=0.0, lpad=0.30)
    edge(ax, S[3], S[2], "1/4", rad=0.0, lpad=0.30)
    edge(ax, S[3], S[4], "1/2", rad=0.0, lpad=0.30)
    edge(ax, S[4], S[5], "1/2", rad=0.0, lpad=0.30)
    edge(ax, S[0], S[1], "1/3", rad=0.0, lpad=0.28)
    edge(ax, S[0], S[3], "1/3", rad=0.0, lpad=0.28)
    edge(ax, S[0], S[5], "1/3", rad=0.0, lpad=0.28)
    ax.text(0.9, -0.35, "class $\\{s_1\\}$", ha="center", fontsize=9, color=GREEN)
    ax.text(8.1, -0.35, "class $\\{s_5\\}$", ha="center", fontsize=9, color=BLUE)
    ax.text(4.5, -1.62, "transient: $s_0,s_2,s_3,s_4$", ha="center", fontsize=9,
            color=MUTED)
    ax.set_title("(b) rec18 P3 — two recurrent classes, four transient states",
                 fontsize=10.5, color=INK)
    fig.tight_layout()
    save(fig, "rec18")


for f in (fig_warmup, fig_recipe, fig_period, fig_failures, fig_convergence, fig_rec18):
    f()
print("done")
