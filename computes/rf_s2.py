# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy"]
# ///
"""All numbers for R (reference/enrichment) section 2 — universality of the
uniform, the 2-D change-of-variables (Jacobian) rule, and order statistics.

These are enrichment topics beyond the 6.041 syllabus; the anchors in the notes
are G3 s1 (Gaussian integral, max/min by the CDF method), G3 s4 (derived
distributions, the one-dimensional Jacobian), G4 s1 (polar coordinates of a
normal pair) and G7 s2 (the max of n uniforms).

Run:  uv run computes/rf_s2.py
"""
from __future__ import annotations

import io
import json
import math
import sys

import numpy as np
from scipy import integrate, special, stats

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

R: dict = {}


def put(k, v):
    R[k] = v
    return v


def head(t):
    print()
    print("=" * 74)
    print(t)
    print("=" * 74)


rng = np.random.default_rng(6041)

# =====================================================================
head("2.1  Universality of the uniform: inverse-CDF sampling of Exp(lambda)")

LAM = put("u_lambda", 1.5)
N = put("u_N", 2_000_000)

U = rng.random(N)
X = -np.log(1.0 - U) / LAM                      # inverse-CDF construction

put("u_mean_sim", float(X.mean()))
put("u_mean_true", 1.0 / LAM)
put("u_var_sim", float(X.var(ddof=1)))
put("u_var_true", 1.0 / LAM**2)
print(f"N = {N:,} draws of X = -ln(1-U)/lambda with lambda = {LAM}")
print(f"  sample mean {X.mean():.6f}  vs  1/lambda      = {1/LAM:.6f}")
print(f"  sample var  {X.var(ddof=1):.6f}  vs  1/lambda^2 = {1/LAM**2:.6f}")

# Kolmogorov-Smirnov distance between the empirical CDF of X and Exp(lambda)
ks = stats.kstest(X, "expon", args=(0.0, 1.0 / LAM))
put("u_ks_stat", float(ks.statistic))
put("u_ks_pvalue", float(ks.pvalue))
print(f"  KS distance to Exp({LAM}) CDF: {ks.statistic:.6f}  (p = {ks.pvalue:.3f})")

# A single tail probability, simulated vs exact
t_q = put("u_tail_t", 2.0)
put("u_tail_sim", float((X > t_q).mean()))
put("u_tail_true", math.exp(-LAM * t_q))
print(f"  P(X > {t_q}): simulated {(X>t_q).mean():.6f}  vs  e^-lambda*t = "
      f"{math.exp(-LAM*t_q):.6f}")

# Forward direction: F(X) must be Unif(0,1).  Feed in a NON-uniform variable.
head("2.1b  Forward direction: F(X) ~ Unif(0,1) for X ~ Exp(lambda)")
Y = rng.exponential(scale=1.0 / LAM, size=N)     # fresh exponential sample
FY = 1.0 - np.exp(-LAM * Y)                      # F(Y)
put("u_fwd_mean_sim", float(FY.mean()))
put("u_fwd_var_sim", float(FY.var(ddof=1)))
put("u_fwd_var_true", 1.0 / 12.0)
ks2 = stats.kstest(FY, "uniform")
put("u_fwd_ks_stat", float(ks2.statistic))
put("u_fwd_ks_pvalue", float(ks2.pvalue))
print(f"  mean of F(Y): {FY.mean():.6f}  vs  1/2")
print(f"  var  of F(Y): {FY.var(ddof=1):.6f}  vs  1/12 = {1/12:.6f}")
print(f"  KS distance to Unif(0,1): {ks2.statistic:.6f}  (p = {ks2.pvalue:.3f})")

# Practice: Cauchy by inverse CDF, F(x) = 1/2 + arctan(x)/pi
head("2.1c  Practice — Cauchy by inverse CDF, and the logistic")
C = np.tan(math.pi * (rng.random(N) - 0.5))
put("c_median_sim", float(np.median(C)))
put("c_iqr_sim", float(np.quantile(C, 0.75) - np.quantile(C, 0.25)))
put("c_iqr_true", 2.0)
put("c_frac_absgt10", float((np.abs(C) > 10).mean()))
put("c_frac_absgt10_true", 2.0 * (0.5 - math.atan(10.0) / math.pi))
print(f"  Cauchy: sample median {np.median(C):.6f} (true 0); "
      f"IQR {np.quantile(C,0.75)-np.quantile(C,0.25):.6f} (true 2)")
print(f"  P(|C| > 10): simulated {(np.abs(C)>10).mean():.6f}  vs  "
      f"{2*(0.5-math.atan(10)/math.pi):.6f}")
# mean is undefined: show the running average refusing to settle
run = np.cumsum(C) / np.arange(1, N + 1)
put("c_runmean_1e4", float(run[9_999]))
put("c_runmean_1e5", float(run[99_999]))
put("c_runmean_2e6", float(run[-1]))
print(f"  running mean at 1e4 / 1e5 / 2e6 draws: {run[9_999]:.4f} / "
      f"{run[99_999]:.4f} / {run[-1]:.4f}  (no limit — E[C] undefined)")

put("log_q", math.log(0.9 / 0.1))
print(f"  logistic inverse CDF at u = 0.9: ln(u/(1-u)) = {math.log(0.9/0.1):.6f}")

# =====================================================================
head("2.2  Jacobian: polar coordinates of a standard normal pair (Box-Muller)")

M = put("bm_N", 1_000_000)
U1 = rng.random(M)
U2 = rng.random(M)
Rr = np.sqrt(-2.0 * np.log(U1))          # F_R(r) = 1 - e^{-r^2/2}, inverted
Th = 2 * math.pi * U2
Zx = Rr * np.cos(Th)
Zy = Rr * np.sin(Th)

put("bm_meanx", float(Zx.mean()))
put("bm_meany", float(Zy.mean()))
put("bm_varx", float(Zx.var(ddof=1)))
put("bm_vary", float(Zy.var(ddof=1)))
put("bm_corr", float(np.corrcoef(Zx, Zy)[0, 1]))
ks3 = stats.kstest(Zx, "norm")
put("bm_ks_stat", float(ks3.statistic))
put("bm_ks_pvalue", float(ks3.pvalue))
put("bm_ks_crit5", 1.36 / math.sqrt(M))          # 5% KS critical distance
print(f"  KS 5% critical distance 1.36/sqrt(M) = {1.36/math.sqrt(M):.6f}")
print(f"M = {M:,} Box-Muller pairs")
print(f"  means  {Zx.mean():+.6f}, {Zy.mean():+.6f}   (true 0)")
print(f"  vars   {Zx.var(ddof=1):.6f}, {Zy.var(ddof=1):.6f}  (true 1)")
print(f"  correlation {np.corrcoef(Zx,Zy)[0,1]:+.6f}  (true 0)")
print(f"  KS distance of X to N(0,1): {ks3.statistic:.6f} (p = {ks3.pvalue:.3f})")

# Rayleigh radius: mean sqrt(pi/2), and the normalization of r e^{-r^2/2}
put("ray_mean_sim", float(Rr.mean()))
put("ray_mean_true", math.sqrt(math.pi / 2))
ray_norm, _ = integrate.quad(lambda r: r * math.exp(-r * r / 2), 0, np.inf)
put("ray_norm", float(ray_norm))
put("ray_mode", 1.0)
print(f"  Rayleigh radius: sample mean {Rr.mean():.6f} vs sqrt(pi/2) = "
      f"{math.sqrt(math.pi/2):.6f};  integral of r e^{{-r^2/2}} = {ray_norm:.6f}")

# Example: (X+Y, X/(X+Y)) for iid exponentials -> Gamma(2,lambda) x Unif(0,1)
head("2.2b  Jacobian example: S = X+Y, V = X/(X+Y) for i.i.d. Exp(lambda)")
LAM2 = put("gv_lambda", 1.0)
Xe = rng.exponential(1 / LAM2, M)
Ye = rng.exponential(1 / LAM2, M)
S = Xe + Ye
V = Xe / S
put("gv_S_mean_sim", float(S.mean()))
put("gv_S_mean_true", 2.0 / LAM2)
put("gv_S_var_sim", float(S.var(ddof=1)))
put("gv_S_var_true", 2.0 / LAM2**2)
put("gv_V_mean_sim", float(V.mean()))
put("gv_V_var_sim", float(V.var(ddof=1)))
put("gv_V_var_true", 1 / 12)
put("gv_corr", float(np.corrcoef(S, V)[0, 1]))
ks4 = stats.kstest(V, "uniform")
put("gv_V_ks_stat", float(ks4.statistic))
ks5 = stats.kstest(S, "gamma", args=(2.0, 0.0, 1 / LAM2))
put("gv_S_ks_stat", float(ks5.statistic))
print(f"  S: mean {S.mean():.6f} (true {2/LAM2:.6f}), var {S.var(ddof=1):.6f} "
      f"(true {2/LAM2**2:.6f}), KS to Gamma(2,{LAM2}) = {ks5.statistic:.6f}")
print(f"  V: mean {V.mean():.6f} (true 0.5), var {V.var(ddof=1):.6f} "
      f"(true {1/12:.6f}), KS to Unif(0,1) = {ks4.statistic:.6f}")
print(f"  correlation of S and V: {np.corrcoef(S,V)[0,1]:+.6f}  (independent -> 0)")

# Practice: rotation (X,Y) iid N(0,1) -> (X+Y, X-Y), |det J| = 1/2
head("2.2c  Practice — the rotation (X+Y, X-Y) of an i.i.d. standard normal pair")
Zn1 = rng.standard_normal(M)
Zn2 = rng.standard_normal(M)
Ur, Vr = Zn1 + Zn2, Zn1 - Zn2
put("rot_detJ_inv", 0.5)
put("rot_var_sim", [float(Ur.var(ddof=1)), float(Vr.var(ddof=1))])
put("rot_var_true", 2.0)
put("rot_corr", float(np.corrcoef(Ur, Vr)[0, 1]))
print(f"  vars of X+Y, X-Y: {Ur.var(ddof=1):.6f}, {Vr.var(ddof=1):.6f} (true 2)")
print(f"  correlation {np.corrcoef(Ur,Vr)[0,1]:+.6f} (true 0); |det J^-1| = 1/2")

# =====================================================================
head("2.3  Order statistics of n = 5 i.i.d. Unif(0,1)")

NO = put("os_n", 5)
K = put("os_reps", 400_000)
Usamp = rng.random((K, NO))
Osort = np.sort(Usamp, axis=1)

os_mean_sim, os_mean_true, os_sd_sim, os_sd_true = [], [], [], []
for j in range(1, NO + 1):
    col = Osort[:, j - 1]
    a, b = j, NO - j + 1
    mu = a / (a + b)
    var = a * b / ((a + b) ** 2 * (a + b + 1))
    os_mean_sim.append(float(col.mean()))
    os_mean_true.append(float(mu))
    os_sd_sim.append(float(col.std(ddof=1)))
    os_sd_true.append(float(math.sqrt(var)))
    print(f"  U_({j}) ~ Beta({a},{b}):  mean sim {col.mean():.6f} vs {mu:.6f} = "
          f"{j}/{NO+1};  sd sim {col.std(ddof=1):.6f} vs {math.sqrt(var):.6f}")
put("os_mean_sim", os_mean_sim)
put("os_mean_true", os_mean_true)
put("os_sd_sim", os_sd_sim)
put("os_sd_true", os_sd_true)
put("os_median_sd_true", os_sd_true[2])
put("os_max_mean_true", os_mean_true[-1])

# Range of n uniforms
rng_vals = Osort[:, -1] - Osort[:, 0]
put("os_range_sim", float(rng_vals.mean()))
put("os_range_true", (NO - 1) / (NO + 1))
print(f"  range X_(n) - X_(1): sim {rng_vals.mean():.6f} vs (n-1)/(n+1) = "
      f"{(NO-1)/(NO+1):.6f}")

# Worked example: P(U_(3) > 0.7), n = 5 — Beta tail vs binomial tail
head("2.3b  Worked example: P(U_(3) > 0.7) with n = 5")
p07 = put("os_p3_gt", 0.7)
beta_tail = float(stats.beta.sf(p07, 3, 3))
binom_tail = float(sum(math.comb(NO, i) * p07**i * (1 - p07) ** (NO - i)
                       for i in range(0, 3)))
put("os_p3_beta_tail", beta_tail)
put("os_p3_binom_tail", binom_tail)
put("os_p3_sim", float((Osort[:, 2] > p07).mean()))
put("os_p3_exact_frac", 1 - (10 * p07**3 * (1 - p07) ** 2 + 5 * p07**4 * (1 - p07)
                             + p07**5))
print(f"  1 - F_(3)(0.7) via Beta(3,3) survival : {beta_tail:.6f}")
print(f"  same via binomial 'fewer than 3 below': {binom_tail:.6f}")
print(f"  closed form 1 - [10p^3q^2 + 5p^4q + p^5]: {R['os_p3_exact_frac']:.6f}")
print(f"  simulated fraction                     : {(Osort[:,2]>p07).mean():.6f}")

# the three binomial terms of that tail, for display in the worked example
terms = [math.comb(NO, i) * p07**i * (1 - p07) ** (NO - i) for i in range(3)]
put("os_p3_terms", [float(t) for t in terms])
print(f"  terms i=0,1,2: {terms[0]:.6f} + {terms[1]:.6f} + {terms[2]:.6f} = "
      f"{sum(terms):.6f}")

# Density of the k-th order statistic integrates to 1 (n=5, k=3, uniform)
f3_norm, _ = integrate.quad(
    lambda x: math.factorial(5) / (math.factorial(2) * math.factorial(2))
    * x**2 * (1 - x) ** 2, 0, 1)
put("os_f3_norm", float(f3_norm))
put("os_f3_peak", 30 * 0.5**2 * 0.5**2)
print(f"  integral of f_(3)(x) = 30 x^2 (1-x)^2 over [0,1]: {f3_norm:.6f}; "
      f"peak height 30/16 = {30*0.5**2*0.5**2:.4f}")

# =====================================================================
head("2.3c  Order statistics of exponentials: E[X_(k)], lambda = 1, n = 5")
LAM3 = put("eo_lambda", 1.0)
Es = rng.exponential(1 / LAM3, (K, NO))
Esort = np.sort(Es, axis=1)
eo_true, eo_sim = [], []
for k in range(1, NO + 1):
    mu = sum(1.0 / (LAM3 * (NO - i + 1)) for i in range(1, k + 1))
    eo_true.append(float(mu))
    eo_sim.append(float(Esort[:, k - 1].mean()))
    print(f"  E[X_({k})] = {mu:.6f}   simulated {Esort[:, k-1].mean():.6f}")
put("eo_true", eo_true)
put("eo_sim", eo_sim)
put("eo_min_mean_true", 1.0 / (NO * LAM3))
put("eo_max_mean_true", eo_true[-1])
put("eo_harmonic5", sum(1.0 / i for i in range(1, NO + 1)))
print(f"  min mean 1/(n*lambda) = {1/(NO*LAM3):.6f}; "
      f"max mean H_5 = {sum(1.0/i for i in range(1,NO+1)):.6f}")

# Cross-check against G7 s2: E[max of n Unif(0,theta)] = n/(n+1) theta, theta=8
head("2.3d  Cross-check with G7 section 2 (uniform ML example, n = 5, theta = 8)")
put("xcheck_theta", 8.0)
put("xcheck_max_mean", 8.0 * NO / (NO + 1))
print(f"  Beta(n,1) mean n/(n+1) = {NO/(NO+1):.6f}; times theta = 8 gives "
      f"{8*NO/(NO+1):.6f}  (G7 s2 prints 6.667)")

# =====================================================================
head("Writing JSON")
with open("computes/rf_s2.json", "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1, default=float)
print(f"wrote computes/rf_s2.json with {len(R)} keys")
