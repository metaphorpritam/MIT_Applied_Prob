# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figures for G4 section 4 — Poisson II: merging, splitting, random incidence.

Run:  uv run computes/g4_s4_figs.py
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


def save(fig, name):
    p = IMG / f"g4_s4_{name}.png"
    fig.savefig(p)
    plt.close(fig)
    print("wrote", p)


def box(ax, x, y, w, h, text, fc="#eef4fc", ec=BLUE, fs=9.5, tc=INK, r=0.02, ha="center"):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.006,rounding_size={r}",
                                   fc=fc, ec=ec, lw=1.3))
    ax.text(x + w / 2, y + h / 2, text, ha=ha, va="center", fontsize=fs, color=tc, zorder=5)


def arrow(ax, x1, y1, x2, y2, c=MUTED, lw=1.5, style="-|>", ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=c, lw=lw, ls=ls, shrinkA=2, shrinkB=2))


def timeline(ax, x0, x1, y, marks, color, label=None, ms=8, lw=1.2, marker="x"):
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=AXIS_C, lw=lw))
    ax.plot(marks, [y] * len(marks), marker, color=color, ms=ms, mew=2.0, clip_on=False)
    if label:
        ax.text(x0 - 0.12, y, label, ha="right", va="center", fontsize=9.5, color=INK)


# =====================================================================
# Fig 4.1 — merging of two Poisson processes
# =====================================================================
def fig_merge():
    fig, ax = plt.subplots(figsize=(9.0, 3.9))
    ax.set_xlim(-0.2, 10.4)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    ax.grid(False)

    m1 = [1.55, 3.1, 5.4, 8.5]
    m2 = [2.0, 2.6, 4.4, 6.3, 7.1, 9.3]
    timeline(ax, 1.3, 10.3, 3.75, m1, BLUE)
    timeline(ax, 1.3, 10.3, 2.65, m2, ORANGE)
    timeline(ax, 1.3, 10.3, 1.15, sorted(m1 + m2), PURPLE)

    ax.text(0.05, 3.75, "red bulb\nflashes", ha="left", va="center", fontsize=9.5, color=BLUE)
    ax.text(1.25, 4.05, r"rate $\lambda_1$", ha="left", va="bottom", fontsize=9.5, color=BLUE)
    ax.text(0.05, 2.65, "green bulb\nflashes", ha="left", va="center", fontsize=9.5, color=ORANGE)
    ax.text(1.25, 2.95, r"rate $\lambda_2$", ha="left", va="bottom", fontsize=9.5, color=ORANGE)
    ax.text(0.05, 1.15, "all flashes\n(merged)", ha="left", va="center", fontsize=9.5, color=PURPLE)
    ax.text(1.25, 1.45, r"rate $\lambda_1+\lambda_2$", ha="left", va="bottom",
            fontsize=9.5, color=PURPLE)
    ax.text(10.3, 0.75, "time", ha="right", va="top", fontsize=9, color=MUTED)

    # dashed drop lines from each parent mark to the merged line
    for m, c in [(x, BLUE) for x in m1] + [(x, ORANGE) for x in m2]:
        ax.plot([m, m], [1.28, 3.62 if c == BLUE else 2.52], ls=":", lw=0.9, color=c, alpha=0.55,
                zorder=0)

    # highlight the first merged arrival
    first = min(m1 + m2)
    ax.annotate("first merged arrival:\ncomes from stream 1 w.p. "
                r"$\lambda_1/(\lambda_1+\lambda_2)$",
                xy=(first, 1.05), xytext=(3.4, 0.28),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2),
                fontsize=9, color=INK, ha="left", va="bottom")
    ax.set_title("Merging: superpose the marks, the rates add", loc="left", pad=6)
    save(fig, "merge")


# =====================================================================
# Fig 4.2 — splitting of a Poisson process
# =====================================================================
def fig_split():
    fig, ax = plt.subplots(figsize=(9.0, 4.1))
    ax.set_xlim(-0.2, 10.4)
    ax.set_ylim(0, 4.7)
    ax.axis("off")
    ax.grid(False)

    marks = [1.7, 2.5, 3.4, 4.9, 6.2, 7.0, 8.4, 9.4]
    keep = [True, False, False, True, False, True, False, False]  # coin outcomes
    timeline(ax, 1.3, 10.3, 3.5, marks, PURPLE)
    ax.text(0.05, 3.5, "all email\nleaving MIT", ha="left", va="center", fontsize=9.5, color=PURPLE)
    ax.text(1.25, 3.82, r"rate $\lambda$", ha="left", va="bottom", fontsize=9.5, color=PURPLE)

    up = [m for m, k in zip(marks, keep) if k]
    dn = [m for m, k in zip(marks, keep) if not k]
    timeline(ax, 1.3, 10.3, 2.15, up, BLUE)
    timeline(ax, 1.3, 10.3, 0.95, dn, ORANGE)
    ax.text(0.05, 2.15, "to USA", ha="left", va="center", fontsize=9.5, color=BLUE)
    ax.text(1.25, 2.45, r"rate $p\lambda$", ha="left", va="bottom", fontsize=9.5, color=BLUE)
    ax.text(0.05, 0.95, "to foreign", ha="left", va="center", fontsize=9.5, color=ORANGE)
    ax.text(1.25, 1.25, r"rate $(1-p)\lambda$", ha="left", va="bottom", fontsize=9.5, color=ORANGE)
    ax.text(10.3, 0.55, "time", ha="right", va="top", fontsize=9, color=MUTED)

    for m, k in zip(marks, keep):
        c = BLUE if k else ORANGE
        y2 = 2.15 if k else 0.95
        ax.annotate("", xy=(m, y2 + 0.13), xytext=(m, 3.37),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=1.1, ls=":", alpha=0.75))
        ax.text(m, 2.95, "H" if k else "T", ha="center", va="center", fontsize=8.5, color=c,
                bbox=dict(boxstyle="circle,pad=0.18", fc="white", ec=c, lw=0.9))

    ax.text(5.3, 4.35, "independent coin per arrival:  heads (prob. $p$) → USA,   "
                       "tails (prob. $1-p$) → foreign",
            ha="center", va="center", fontsize=9.2, color=MUTED)
    ax.set_title("Splitting: flip a coin at each mark, each stream is Poisson", loc="left", pad=6)
    save(fig, "split")


# =====================================================================
# Fig 4.3 — three light bulbs: merging + memorylessness staircase
# =====================================================================
def fig_bulbs():
    fig, ax = plt.subplots(figsize=(9.0, 3.4))
    ax.set_xlim(-0.3, 10.3)
    ax.set_ylim(0, 3.5)
    ax.axis("off")
    ax.grid(False)

    xs = [0.2, 3.4, 6.6]
    ws = 2.9
    labels = [("3 bulbs alive", r"merged rate $3\lambda$", r"$\mathbb{E}[T_1]=\dfrac{1}{3\lambda}$", BLUE),
              ("2 bulbs alive", r"merged rate $2\lambda$", r"$\mathbb{E}[T_2]=\dfrac{1}{2\lambda}$", ORANGE),
              ("1 bulb alive", r"rate $\lambda$", r"$\mathbb{E}[T_3]=\dfrac{1}{\lambda}$", GREEN)]
    fcs = ["#eef4fc", "#fdf1ea", "#eaf7f1"]
    for x, (t, r, e, c), fc in zip(xs, labels, fcs):
        box(ax, x, 1.45, ws, 1.35, f"{t}\n{r}\n{e}", fc=fc, ec=c, fs=10)
    arrow(ax, xs[0] + ws + 0.03, 2.12, xs[1] - 0.03, 2.12)
    arrow(ax, xs[1] + ws + 0.03, 2.12, xs[2] - 0.03, 2.12)
    ax.text(xs[0] + ws + 0.25, 2.92, "a bulb dies", ha="center", va="bottom", fontsize=8.5,
            color=MUTED)
    ax.text(xs[1] + ws + 0.25, 2.92, "a bulb dies", ha="center", va="bottom", fontsize=8.5,
            color=MUTED)
    ax.text(5.0, 0.85, r"$\mathbb{E}[\text{time until last bulb dies}]"
                       r"=\dfrac{1}{3\lambda}+\dfrac{1}{2\lambda}+\dfrac{1}{\lambda}"
                       r"=\dfrac{11}{6\lambda}$",
            ha="center", va="center", fontsize=12, color=INK)
    ax.text(5.0, 0.22, "memorylessness restarts the clock at every death, so $T_1,T_2,T_3$ "
                       "are independent",
            ha="center", va="center", fontsize=8.8, color=MUTED, style="italic")
    ax.set_title("Three light bulbs (L15 slide 5)", loc="left", pad=6)
    save(fig, "bulbs")


# =====================================================================
# Fig 4.4 — random incidence: timeline + the two densities
# =====================================================================
def fig_incidence():
    fig = plt.figure(figsize=(9.4, 6.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.15], hspace=0.42)

    # --- top: the timeline picture ---
    ax = fig.add_subplot(gs[0])
    ax.set_xlim(-0.2, 10.4)
    ax.set_ylim(-0.1, 3.0)
    ax.axis("off")
    ax.grid(False)
    marks = [0.9, 1.9, 2.6, 6.9, 8.0, 9.3]
    U, V, tstar = 2.6, 6.9, 4.6
    timeline(ax, 0.2, 10.3, 1.25, marks, PURPLE, ms=9)
    ax.text(10.3, 0.95, "time", ha="right", va="top", fontsize=9, color=MUTED)

    for x, lab in [(U, "$U$ (last arrival\nbefore $t^*$)"), (V, "$V$ (first arrival\nafter $t^*$)")]:
        ax.plot([x, x], [1.25, 2.15], lw=1.0, ls=":", color=MUTED)
    ax.annotate("", xy=(V, 2.15), xytext=(U, 2.15),
                arrowprops=dict(arrowstyle="<|-|>", color=PURPLE, lw=1.6))
    ax.text((U + V) / 2, 2.28, r"$L=V-U$  (the interval you land in)", ha="center", va="bottom",
            fontsize=10, color=PURPLE)
    ax.text(U, 0.95, "$U$", ha="center", va="top", fontsize=10, color=INK)
    ax.text(V, 0.95, "$V$", ha="center", va="top", fontsize=10, color=INK)

    ax.plot([tstar], [1.25], "v", color=RED, ms=9, clip_on=False)
    ax.annotate("chosen instant $t^*$", xy=(tstar, 1.18), xytext=(tstar, 0.25),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.3),
                ha="center", va="bottom", fontsize=9.5, color=RED)
    ax.annotate("", xy=(tstar, 1.72), xytext=(U, 1.72),
                arrowprops=dict(arrowstyle="<|-|>", color=ORANGE, lw=1.4))
    ax.annotate("", xy=(V, 1.72), xytext=(tstar, 1.72),
                arrowprops=dict(arrowstyle="<|-|>", color=BLUE, lw=1.4))
    ax.text((U + tstar) / 2, 1.80, r"$t^*-U\sim\mathrm{Exp}(\lambda)$", ha="center", va="bottom",
            fontsize=9, color=ORANGE)
    ax.text((tstar + V) / 2, 1.80, r"$V-t^*\sim\mathrm{Exp}(\lambda)$", ha="center", va="bottom",
            fontsize=9, color=BLUE)
    ax.set_title("A fixed instant $t^*$ splits its interval into backward + forward waits",
                 loc="left", pad=4)

    # --- bottom: exponential vs Erlang-2 ---
    ax2 = fig.add_subplot(gs[1])
    lam = 0.5
    x = np.linspace(0, 16, 500)
    fe = lam * np.exp(-lam * x)
    fg = lam ** 2 * x * np.exp(-lam * x)
    ax2.plot(x, fe, color=GREEN, lw=2.2, label=r"a numbered interval: $\mathrm{Exp}(\lambda)$")
    ax2.plot(x, fg, color=PURPLE, lw=2.2, label=r"the interval containing $t^*$: Erlang(2)")
    ax2.axvline(1 / lam, color=GREEN, ls="--", lw=1.2, alpha=0.8)
    ax2.axvline(2 / lam, color=PURPLE, ls="--", lw=1.2, alpha=0.8)
    ax2.text(1 / lam + 0.15, 0.47, r"mean $1/\lambda=2$", color=GREEN, fontsize=9,
             ha="left", va="top")
    ax2.text(2 / lam + 0.15, 0.40, r"mean $2/\lambda=4$", color=PURPLE, fontsize=9,
             ha="left", va="top")
    ax2.set_xlim(0, 16)
    ax2.set_ylim(0, 0.52)
    ax2.set_xlabel(r"interval length  (units of time, $\lambda=0.5$)")
    ax2.set_ylabel("density")
    ax2.legend(loc="upper right")
    ax2.set_title("Random incidence doubles the mean", loc="left", pad=4)
    save(fig, "incidence")


# =====================================================================
# Fig 4.5 — length-biased sampling, the 5/10-minute bus line
# =====================================================================
def fig_lengthbias():
    fig = plt.figure(figsize=(9.4, 5.0))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.95], hspace=0.55)

    ax = fig.add_subplot(gs[0])
    lens = [5, 10, 5, 5, 10, 10, 5, 10]
    edges = np.cumsum([0] + lens)
    total = edges[-1]
    ax.set_xlim(-1, total + 1)
    ax.set_ylim(-0.9, 1.5)
    ax.axis("off")
    ax.grid(False)
    for i, (x0, x1) in enumerate(zip(edges[:-1], edges[1:])):
        c = ORANGE if lens[i] == 5 else BLUE
        fc = "#fdf1ea" if lens[i] == 5 else "#eef4fc"
        ax.add_patch(mp.Rectangle((x0, 0), x1 - x0, 0.62, fc=fc, ec=c, lw=1.3))
        ax.text((x0 + x1) / 2, 0.31, f"{lens[i]}", ha="center", va="center", fontsize=9.5, color=c)
    ax.plot(edges, [0] * len(edges), "|", color=INK, ms=14, mew=1.6)
    rng = np.random.default_rng(7)
    pins = rng.uniform(0, total, 26)
    ax.plot(pins, [-0.30] * len(pins), "^", color=RED, ms=6)
    ax.text(-1, -0.62, "random instants sprinkled uniformly on the time axis — "
                       "two-thirds of them land in a 10-minute gap",
            ha="left", va="center", fontsize=9, color=MUTED)
    ax.text(-1, 1.15, "bus interarrival gaps (minutes): 5 or 10, equally likely",
            ha="left", va="center", fontsize=9.5, color=INK)

    ax2 = fig.add_subplot(gs[1])
    labels = ["5-minute gap", "10-minute gap"]
    xs = np.arange(2)
    unb = [0.5, 0.5]
    bias = [1 / 3, 2 / 3]
    w = 0.34
    ax2.bar(xs - w / 2, unb, width=w, color=GREEN, alpha=0.9,
            label="pick a gap by its number:  1/2, 1/2")
    ax2.bar(xs + w / 2, bias, width=w, color=PURPLE, alpha=0.9,
            label="pick a gap by dropping a pin:  1/3, 2/3")
    for xx, v in zip(xs - w / 2, unb):
        ax2.text(xx, v + 0.02, f"{v:.3f}", ha="center", va="bottom", fontsize=9, color=GREEN)
    for xx, v in zip(xs + w / 2, bias):
        ax2.text(xx, v + 0.02, f"{v:.3f}", ha="center", va="bottom", fontsize=9, color=PURPLE)
    ax2.set_xticks(xs)
    ax2.set_xticklabels(labels)
    ax2.set_ylim(0, 0.85)
    ax2.set_ylabel("probability")
    ax2.legend(loc="upper left", fontsize=8.6)
    ax2.set_title("Two different sampling mechanisms, two different distributions",
                  loc="left", pad=4)
    save(fig, "lengthbias")


# =====================================================================
# Fig 4.6 — decision flowchart
# =====================================================================
def fig_recipe():
    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.8)
    ax.axis("off")
    ax.grid(False)

    box(ax, 3.1, 4.95, 3.8, 0.66, "Poisson question in front of you", fc="#f3f2ec", ec=AXIS_C,
        fs=10)
    qs = [
        (0.15, 3.55, "Several independent\nstreams, one clock?", BLUE, "#eef4fc",
         "MERGE: rate $\\lambda_1+\\cdots+\\lambda_n$.\nOrigin of each arrival is\nindependent, "
         "$\\lambda_i/\\sum_j\\lambda_j$."),
        (3.45, 3.55, "One stream, arrivals\nlabeled by a coin?", ORANGE, "#fdf1ea",
         "SPLIT: rates $p\\lambda$, $(1-p)\\lambda$.\nThe two output streams\nare independent."),
        (6.75, 3.55, "\"Who arrives first?\"\nor $\\min$ of exponentials?", GREEN, "#eaf7f1",
         "COMPETING EXPONENTIALS:\n$\\min\\sim\\mathrm{Exp}(\\sum\\lambda_i)$,\n"
         "winner is $i$ w.p. $\\lambda_i/\\sum\\lambda_j$."),
    ]
    for x, y, q, c, fc, a in qs:
        box(ax, x, y, 3.1, 0.95, q, fc=fc, ec=c, fs=9.5)
        arrow(ax, x + 1.55, y - 0.03, x + 1.55, y - 0.72, c=c)
        box(ax, x, y - 1.85, 3.1, 1.1, a, fc="white", ec=c, fs=8.6)

    arrow(ax, 4.0, 4.92, 1.70, 4.55, c=MUTED)
    arrow(ax, 5.0, 4.92, 5.00, 4.55, c=MUTED)
    arrow(ax, 6.0, 4.92, 8.30, 4.55, c=MUTED)

    box(ax, 2.0, 0.15, 6.0, 1.0,
        "\"I showed up at an arbitrary instant — how long is MY gap?\"\n"
        "RANDOM INCIDENCE: length-bias it. For Poisson, $L\\sim$ Erlang(2), mean $2/\\lambda$;\n"
        "in general $\\mathbf{P}(\\text{gap of length }\\ell)\\propto \\ell\\, p_L(\\ell)$.",
        fc="#f6effa", ec=PURPLE, fs=9.2)
    ax.text(5.0, 1.32, "none of the above — the question is about the observer, not the process",
            ha="center", va="bottom", fontsize=8.6, color=MUTED, style="italic")
    ax.set_title("Which Poisson tool? (L15)", loc="left", pad=6)
    save(fig, "recipe")


if __name__ == "__main__":
    fig_merge()
    fig_split()
    fig_bulbs()
    fig_incidence()
    fig_lengthbias()
    fig_recipe()
    print("done")
