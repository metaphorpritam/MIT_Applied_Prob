# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
"""Figure for G4 §5 (synthesis + bridge).

Output (notes/img/):
  g4_s5_bridge.png — the Bernoulli -> Poisson limit: (a) slot discretization
                     schematic with n = t/delta, p = lambda*delta, np = lambda*t;
                     (b) binomial PMFs collapsing onto Poisson(lambda t) as delta -> 0.
All numbers shown are the ones printed by computes/g4_s5.py.
"""
import io
import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "notes" / "_build"))
from mpl_style import setup, diagram_ax, PAL, INK, MUTED, GRID_C  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
plt, _ = setup()

OUT = Path(__file__).resolve().parents[1] / "notes" / "img"
OUT.mkdir(parents=True, exist_ok=True)

LAM, T = 2.0, 1.0
# the same arrival instants on every row; 0.81 and 0.865 share a slot when
# delta = 0.1, so the coarse clock miscounts them as one arrival
ARRIVALS = [0.12, 0.37, 0.44, 0.81, 0.865]

fig = plt.figure(figsize=(11.4, 4.3))
gs = fig.add_gridspec(1, 2, width_ratios=[1.18, 1.0], wspace=0.24)

# ---------------------------------------------------------------- panel (a)
ax = fig.add_subplot(gs[0, 0])
ax.axis("off")
ax.set_xlim(-0.06, 1.30)
ax.set_ylim(-0.10, 1.06)

rows = [(0.86, 10, "coarse slots:  $\\delta = 0.1$,  $n = t/\\delta = 10$"),
        (0.50, 25, "finer:  $\\delta = 0.04$,  $n = 25$"),
        (0.14, None, "limit  $\\delta \\to 0$:  continuous time")]

for y, n, label in rows:
    ax.annotate("", xy=(1.06, y), xytext=(0.0, y),
                arrowprops=dict(arrowstyle="-|>", color=INK, linewidth=1.4))
    if n is not None:
        for i in range(n + 1):
            x = i / n
            ax.plot([x, x], [y - 0.035, y + 0.035], color=GRID_C,
                    linewidth=0.9, solid_capstyle="butt", zorder=1)
        counts = {}
        for a in ARRIVALS:
            slot = min(int(a * n), n - 1)
            counts[slot] = counts.get(slot, 0) + 1
        for slot, c in counts.items():
            xc = (slot + 0.5) / n
            ax.plot([xc], [y], marker="o", markersize=6, markerfacecolor="white",
                    markeredgecolor=PAL[0], markeredgewidth=1.6, zorder=3)
            if c > 1:
                ax.text(xc, y + 0.055, f"{c} in one slot", fontsize=8.5,
                        color=PAL[7], ha="right", va="bottom")
    else:
        for a in ARRIVALS:
            ax.plot([a], [y], marker="x", markersize=8, color=PAL[1],
                    markeredgewidth=2.0, zorder=3)
    ax.text(0.0, y + 0.115, label, fontsize=9.5, color=INK, ha="left", va="center")
    ax.text(1.09, y, "$t$", fontsize=10, color=MUTED, ha="left", va="center")

ax.annotate("", xy=(0.53, 0.62), xytext=(0.53, 0.76),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=1.1))
ax.annotate("", xy=(0.53, 0.26), xytext=(0.53, 0.40),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, linewidth=1.1))

ax.text(0.0, -0.03,
        "each slot is a Bernoulli trial with  $p = \\lambda\\delta$,\n"
        "so  $np = (t/\\delta)(\\lambda\\delta) = \\lambda t$  is held fixed",
        fontsize=9.5, color=INK, ha="left", va="top")
ax.set_title("(a) one process, two clocks", loc="left")

# ---------------------------------------------------------------- panel (b)
ax2 = fig.add_subplot(gs[0, 1])
k = np.arange(0, 9)
styles = [(0.25, PAL[2], "--"), (0.1, PAL[3], "-."), (0.01, PAL[0], "-")]
for delta, col, ls in styles:
    n = int(round(T / delta))
    p = LAM * delta
    ax2.plot(k, stats.binom.pmf(k, n, p), ls, color=col, linewidth=1.8, marker="o",
             markersize=4, label=f"binomial $n={n}$, $p={p:g}$")
ax2.vlines(k, 0, stats.poisson.pmf(k, LAM * T), color=PAL[1], linewidth=2.4,
           zorder=1, alpha=0.85)
ax2.plot(k, stats.poisson.pmf(k, LAM * T), "o", color=PAL[1], markersize=7,
         label="Poisson $\\lambda t = 2$", zorder=2)
ax2.set_xlabel("number of arrivals $k$ in $[0,t]$")
ax2.set_ylabel("probability")
ax2.set_title("(b) binomial $\\to$ Poisson, $np=\\lambda t=2$ fixed", loc="left")
ax2.set_ylim(0, 0.42)
ax2.legend(loc="upper right", fontsize=8.5)

fig.savefig(OUT / "g4_s5_bridge.png", dpi=150)
print("wrote", OUT / "g4_s5_bridge.png")
