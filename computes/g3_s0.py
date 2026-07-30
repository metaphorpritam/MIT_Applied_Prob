# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Numbers used in G3 section 0 (orientation: from sums to integrals).

Every numeric value printed in notes/src/fragments/g3_s0.html is produced here.

Sources
-------
L08 slides 2-3 (pdf, the delta-interval interpretation, E and var as integrals)
L09 slide 1     (the discrete/continuous correspondence table)
B&T Example 1.4 (wheel of fortune: continuous uniform law on [0,1])
B&T 3.1         (P(X = x) = 0 for a continuous r.v.)

Three quantitative threads:
 (A) the wheel-of-fortune / equal-cells argument that forces P(X = x) = 0;
 (B) sums literally turning into integrals: discrete uniform on n midpoints of
     [0,1] versus the continuous uniform on [0,1] (mean, variance);
 (C) the CLT teaser used in Fig. 0.1: scaled binomial PMF stems against the
     standard normal density (max deviation, and the vanishing peak mass).
"""
import io
import json
import sys
from fractions import Fraction

import numpy as np
from scipy.stats import binom, norm

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

out: dict = {}

# --------------------------------------------------------------------------
# (A) Wheel of fortune (B&T Example 1.4): Omega = [0,1], continuous uniform.
#     Cut [0,1] into n equal cells; by symmetry each has probability 1/n.
#     A single point lies inside every one of these cells, so P({x}) <= 1/n
#     for every n, hence P({x}) = 0.
# --------------------------------------------------------------------------
cells = [10, 100, 10**6]
out["wheel_cells"] = cells
out["wheel_cell_prob"] = [f"1/{n}" for n in cells]
out["wheel_cell_prob_dec"] = [1.0 / n for n in cells]

# the interval law itself: P([a,b]) = b - a
out["wheel_interval_a"] = 0.25
out["wheel_interval_b"] = 0.50
out["wheel_interval_prob"] = 0.50 - 0.25

# delta-slab reading of a density (L08 slide 2): P(x <= X <= x+delta) ~ f(x)*delta
out["deltas"] = [0.1, 0.01, 0.001]
out["uniform_delta_probs"] = [d * 1.0 for d in out["deltas"]]   # f = 1 on [0,1]

# a density value bigger than 1: uniform on [0, 1/4] has height 1/(1/4) = 4
out["narrow_uniform_b"] = 0.25
out["narrow_uniform_height"] = 1.0 / 0.25
out["narrow_uniform_total_area"] = (1.0 / 0.25) * 0.25          # must be 1

# --------------------------------------------------------------------------
# (B) Sums -> integrals.  Discrete uniform Y_n on the n midpoints
#     x_k = (k - 1/2)/n, k = 1..n, each with mass 1/n, versus the continuous
#     uniform X on [0,1].  E[Y_n] = sum x_k p(x_k)   ->   int_0^1 x dx.
#     Exact rational arithmetic, then decimals.
# --------------------------------------------------------------------------
ns = [4, 10, 100, 1000]
disc = {}
for n in ns:
    xs = [Fraction(2 * k - 1, 2 * n) for k in range(1, n + 1)]
    p = Fraction(1, n)
    mean = sum(x * p for x in xs)
    var = sum((x - mean) ** 2 * p for x in xs)
    disc[n] = {
        "mean_exact": str(mean),
        "mean": float(mean),
        "var_exact": str(var),
        "var": float(var),
        "var_closed_form": float(Fraction(n * n - 1, 12 * n * n)),  # (1-1/n^2)/12
        "mass_each": f"1/{n}",
    }
out["discrete_uniform_midpoints"] = disc
out["cont_uniform_mean"] = 0.5                 # int_0^1 x dx = [x^2/2] = 1/2
out["cont_uniform_var"] = 1.0 / 12.0           # int_0^1 (x-1/2)^2 dx = 1/12
out["cont_uniform_var_str"] = "1/12"

# --------------------------------------------------------------------------
# (C) CLT teaser (Fig. 0.1).  X_n ~ Binomial(n, 1/2); standardize
#     Z = (X_n - np)/sqrt(np(1-p)).  The stems sit at spacing
#     delta = 1/sqrt(np(1-p)); dividing each mass by delta turns the stem
#     heights into a density scale, comparable with the N(0,1) curve.
# --------------------------------------------------------------------------
p = 0.5
clt = {}
for n in [5, 20, 80, 320]:
    mu, sd = n * p, np.sqrt(n * p * (1 - p))
    k = np.arange(0, n + 1)
    pmf = binom.pmf(k, n, p)
    z = (k - mu) / sd
    dens = pmf * sd                     # mass / spacing = density height
    keep = np.abs(z) <= 4.0             # window shown in the figure
    dev = np.max(np.abs(dens[keep] - norm.pdf(z[keep])))
    clt[n] = {
        "sd": float(sd),
        "spacing_delta": float(1.0 / sd),
        "pmf_sum": float(pmf.sum()),
        "max_pmf": float(pmf.max()),           # largest single-point mass
        "max_pmf_at_k": int(k[np.argmax(pmf)]),
        "peak_density": float(dens.max()),     # -> 1/sqrt(2 pi) = 0.3989
        "max_abs_dev_from_normal": float(dev),
    }
out["clt_binomial"] = clt
out["normal_peak"] = float(norm.pdf(0.0))       # 1/sqrt(2 pi)

# a two-sided probability that survives the limit while point masses die:
# P(|Z| <= 1) for binomial n=80 vs the normal value
n = 80
mu, sd = n * p, np.sqrt(n * p * (1 - p))
k = np.arange(0, n + 1)
z = (k - mu) / sd
out["binom80_P_absZ_le_1"] = float(binom.pmf(k[np.abs(z) <= 1], n, p).sum())
out["normal_P_absZ_le_1"] = float(norm.cdf(1) - norm.cdf(-1))

for key, val in out.items():
    print(f"{key:32s} = {val}")

with open("d:/Python-UV/MIT_Applied_Prob/computes/g3_s0.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
print("\nwrote computes/g3_s0.json")
