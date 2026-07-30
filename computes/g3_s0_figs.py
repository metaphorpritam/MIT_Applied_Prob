# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Figures for G3 section 0 (orientation: from sums to integrals).

Fig. 0.1  g3_s0_pmf_to_pdf : three side-by-side panels showing Binomial(n, 1/2)
          PMF stems, standardized and rescaled to a density, converging to the
          standard normal curve.  Visual teaser only -- the theorem is the CLT
          (note G6).  Numbers cross-checked in computes/g3_s0.py.
"""
import io
import sys

sys.path.insert(0, "d:/Python-UV/MIT_Applied_Prob/notes/_build")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import numpy as np
from scipy.stats import binom, norm

from mpl_style import PAL, INK, MUTED, setup

plt, _ = setup()
IMG = "d:/Python-UV/MIT_Applied_Prob/notes/img/"

p = 0.5
NS = [5, 20, 80]
XLIM = 3.6

fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.9), sharey=True)

zz = np.linspace(-XLIM, XLIM, 400)
phi = norm.pdf(zz)

for ax, n in zip(axes, NS):
    mu, sd = n * p, np.sqrt(n * p * (1 - p))
    k = np.arange(0, n + 1)
    pmf = binom.pmf(k, n, p)
    z = (k - mu) / sd
    dens = pmf * sd                      # mass divided by stem spacing 1/sd
    m = np.abs(z) <= XLIM

    # normal curve first (recessive, behind the stems)
    ax.plot(zz, phi, color=PAL[1], linewidth=2.0, zorder=2,
            label=r"$N(0,1)$ density")
    ax.fill_between(zz, 0, phi, color=PAL[1], alpha=0.10, zorder=1)

    # PMF stems, rescaled to density units
    ax.vlines(z[m], 0, dens[m], color=PAL[0], linewidth=1.6, zorder=3)
    ax.plot(z[m], dens[m], "o", color=PAL[0], markersize=3.6, zorder=4,
            label=r"binomial PMF (rescaled)")

    ax.set_title(f"$n = {n}$   (spacing $\\delta = 1/\\sqrt{{np(1-p)}} = {1/sd:.3f}$)",
                 fontsize=10)
    ax.set_xlim(-XLIM - 0.15, XLIM + 0.15)
    ax.set_ylim(0, 0.475)
    ax.set_xlabel(r"standardized value  $z = (x - np)\,/\,\sqrt{np(1-p)}$",
                  fontsize=9)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])

axes[0].set_ylabel(r"mass $/\ \delta$   (density scale)", fontsize=9.5)
axes[0].legend(loc="upper left", fontsize=8.4)

for ax, n in zip(axes, NS):
    mx = binom.pmf(np.arange(0, n + 1), n, p).max()
    ax.text(0.985, 0.955, f"largest single mass\n$\\max_k p_X(k) = {mx:.4f}$",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.2,
            color=MUTED,
            bbox=dict(boxstyle="round,pad=0.32", facecolor="white",
                      edgecolor="#e1e0d9", linewidth=0.8, alpha=0.95))

fig.suptitle("Point masses shrink to zero while the picture converges to a curve",
             fontsize=11.5, fontweight="600", color=INK, y=1.035)
fig.tight_layout()
fig.savefig(IMG + "g3_s0_pmf_to_pdf.png")
plt.close(fig)
print("wrote", IMG + "g3_s0_pmf_to_pdf.png")
