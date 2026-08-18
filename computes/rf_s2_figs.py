# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "matplotlib"]
# ///
r"""Figures for R section 2 — universality of the uniform and order statistics.

Run:  uv run computes/rf_s2_figs.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "notes" / "_build"))
from mpl_style import setup, PAL, INK, MUTED  # noqa: E402

plt, _ = setup()
import numpy as np                    # noqa: E402
from scipy import stats               # noqa: E402

IMG = ROOT / "notes" / "img"
IMG.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(6041)

LAM = 1.5
N = 200_000

# ---------------------------------------------------------------- Fig 2.1
U = rng.random(N)
X = -np.log(1 - U) / LAM
Y = rng.exponential(1 / LAM, N)
FY = 1 - np.exp(-LAM * Y)

fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.5))

ax = axes[0]
ax.hist(X, bins=80, range=(0, 5), density=True, color=PAL[0], alpha=0.35,
        edgecolor="none", label="simulated $-\\ln(1-U)/\\lambda$")
xs = np.linspace(0, 5, 400)
ax.plot(xs, LAM * np.exp(-LAM * xs), color=PAL[1], lw=2.0,
        label="$\\lambda e^{-\\lambda x}$, $\\lambda=1.5$")
ax.set_xlabel("x")
ax.set_ylabel("density")
ax.set_title("(a) $F^{-1}(U)$ has the target density")
ax.set_xlim(0, 5)
ax.legend(loc="upper right")

ax = axes[1]
ax.hist(FY, bins=50, range=(0, 1), density=True, color=PAL[2], alpha=0.35,
        edgecolor="none", label="simulated $F(Y)$, $Y\\sim\\mathrm{Exp}(1.5)$")
ax.plot([0, 1], [1, 1], color=PAL[1], lw=2.0, label="Unif(0,1) density")
ax.set_xlabel("u")
ax.set_ylabel("density")
ax.set_title("(b) $F(X)$ is uniform, whatever $X$ was")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.45)
ax.legend(loc="upper center")

fig.tight_layout()
fig.savefig(IMG / "rf_s2_universality.png")
plt.close(fig)
print("wrote rf_s2_universality.png")

# ---------------------------------------------------------------- Fig 2.2
n = 5
K = 200_000
S = np.sort(rng.random((K, n)), axis=1)

fig, ax = plt.subplots(figsize=(8.2, 3.6))
xs = np.linspace(0, 1, 500)
ax.hist(S[:, 2], bins=60, range=(0, 1), density=True, color=MUTED, alpha=0.20,
        edgecolor="none", label="simulated $U_{(3)}$ (200k samples)")
for j in range(1, n + 1):
    a, b = j, n - j + 1
    ax.plot(xs, stats.beta.pdf(xs, a, b), color=PAL[(j - 1) % 8], lw=1.8,
            label=f"$U_{{({j})}}\\sim$ Beta({a},{b})")
    ax.plot([j / (n + 1)], [0], marker="^", ms=6, color=PAL[(j - 1) % 8],
            clip_on=False)
ax.set_xlabel("x")
ax.set_ylabel("density")
ax.set_xlim(0, 1)
ax.set_ylim(0, 3.6)
ax.set_title("Order statistics of $n=5$ i.i.d. Unif(0,1) draws")
ax.legend(loc="upper center", ncol=2, fontsize=8)
fig.tight_layout()
fig.savefig(IMG / "rf_s2_orderstats.png")
plt.close(fig)
print("wrote rf_s2_orderstats.png")
