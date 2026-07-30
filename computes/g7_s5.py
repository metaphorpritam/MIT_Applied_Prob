# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Every number quoted in G7 section 5 (synthesis + course finale).

Blocks:
  A  normal percentiles z for the standard confidence levels
  B  confidence-interval coverage: Monte-Carlo over repeated experiments
  C  the biased ML variance estimator  (n-1)/n * sigma^2
  D  MAP -> ML as the prior flattens / as n grows  (matching pair 1)
  E  Bayesian posterior mean -> sample mean as the prior variance -> infinity
     (matching pair 2), and the credible interval vs the confidence interval
     (matching pair 3)
  F  likelihood is not a probability density in theta
  G  alpha/beta trade-off for the LRT  N(0,1) vs N(1,1), n data points
  H  L25 composite test: is my coin fair?  S = 472 heads in n = 1000
  I  regression slope with a pure confounder: strong slope, zero causal link
"""
import io
import json
import sys

import numpy as np
from scipy import stats

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
R = {}


def rec(k, v):
    R[k] = v
    print(f"{k:38s} = {v}")


# ------------------------------------------------------------------ A: z values
print("\n--- A  normal percentiles ---")
for alpha in (0.10, 0.05, 0.01):
    z = stats.norm.ppf(1 - alpha / 2)
    rec(f"z_alpha{alpha:.2f}", round(float(z), 6))
rec("Phi_1p96", round(float(stats.norm.cdf(1.96)), 6))

# ------------------------------------------------------------------ B: coverage
print("\n--- B  confidence-interval coverage ---")
rng = np.random.default_rng(20250729)
THETA_TRUE, SIGMA, N_OBS = 5.0, 2.0, 25
N_REP = 400_000
z95 = stats.norm.ppf(0.975)
samp = rng.normal(THETA_TRUE, SIGMA, size=(N_REP, N_OBS))
mhat = samp.mean(axis=1)
half = z95 * SIGMA / np.sqrt(N_OBS)
cover = np.abs(mhat - THETA_TRUE) <= half
rec("ci_theta_true", THETA_TRUE)
rec("ci_sigma", SIGMA)
rec("ci_n_obs", N_OBS)
rec("ci_halfwidth", round(float(half), 6))
rec("ci_mc_coverage", round(float(cover.mean()), 6))
rec("ci_mc_reps", N_REP)
# the 20 intervals drawn in Fig 5.2 (right panel): pick the first seed whose
# 20 replications miss exactly once -- the modal outcome at 95% coverage.
for seed in range(1000):
    demo = np.random.default_rng(seed).normal(
        THETA_TRUE, SIGMA, size=(20, N_OBS)).mean(axis=1)
    if int(np.sum(np.abs(demo - THETA_TRUE) > half)) == 1:
        break
rec("ci_demo_seed", seed)
rec("ci_demo_misses", int(np.sum(np.abs(demo - THETA_TRUE) > half)))
rec("ci_demo_miss_index", int(np.argmax(np.abs(demo - THETA_TRUE) > half)) + 1)
rec("ci_demo_first_lo", round(float(demo[0] - half), 4))
rec("ci_demo_first_hi", round(float(demo[0] + half), 4))
# unknown-sigma version: Ŝ_n uses the n-1 divisor
shat2 = samp.var(axis=1, ddof=1)
rec("ci_Shat2_mean", round(float(shat2.mean()), 6))     # -> sigma^2 = 4
sml2 = samp.var(axis=1, ddof=0)
rec("ci_MLvar_mean", round(float(sml2.mean()), 6))      # -> (n-1)/n * 4

# ------------------------------------------------------------------ C: ML variance bias
print("\n--- C  ML variance is biased ---")
for n in (2, 5, 10, 100):
    factor = (n - 1) / n
    rec(f"mlvar_factor_n{n}", round(factor, 6))
    rec(f"mlvar_bias_n{n}_sig1", round(factor - 1.0, 6))
n_mc, sig2 = 5, 1.0
s = rng.normal(0.0, np.sqrt(sig2), size=(2_000_000, n_mc))
rec("mlvar_mc_n5", round(float(s.var(axis=1, ddof=0).mean()), 6))
rec("mlvar_unb_mc_n5", round(float(s.var(axis=1, ddof=1).mean()), 6))

# ------------------------------------------------------------------ D: MAP -> ML
print("\n--- D  MAP vs ML (matching pair 1) ---")
# coin, k heads in n tosses; Beta(a,b) prior -> Beta(a+k, b+n-k) posterior
def map_beta(a, b, k, n):
    A, B = a + k, b + n - k
    return (A - 1) / (A + B - 2)          # mode of Beta(A,B), A,B > 1


rec("ml_coin_k3_n10", round(3 / 10, 6))
rec("map_uniform_k3_n10", round(map_beta(1, 1, 3, 10), 6))       # = ML exactly
rec("map_beta22_k3_n10", round(map_beta(2, 2, 3, 10), 6))
rec("map_beta22_k30_n100", round(map_beta(2, 2, 30, 100), 6))
rec("map_beta22_k300_n1000", round(map_beta(2, 2, 300, 1000), 6))
rec("map_beta22_gap_n10", round(abs(map_beta(2, 2, 3, 10) - 0.3), 6))
rec("map_beta22_gap_n1000", round(abs(map_beta(2, 2, 300, 1000) - 0.3), 6))

# ------------------------------------------------------------------ E: LMS -> sample mean
print("\n--- E  posterior mean vs sample mean (matching pairs 2 and 3) ---")
MU0, N_E, SIG = 0.0, 10, 2.0          # prior mean, sample size, obs sd
XBAR = 5.0                            # observed sample mean
for s0 in (1.0, 5.0, 20.0, 1e6):
    w_prior = (1 / s0 ** 2) / (1 / s0 ** 2 + N_E / SIG ** 2)
    post_mean = w_prior * MU0 + (1 - w_prior) * XBAR
    post_var = 1.0 / (1 / s0 ** 2 + N_E / SIG ** 2)
    tag = "flat" if s0 > 1e3 else f"s0{s0:g}"
    rec(f"postmean_{tag}", round(float(post_mean), 6))
    rec(f"postsd_{tag}", round(float(np.sqrt(post_var)), 6))
rec("samplemean_xbar", XBAR)
rec("classical_se", round(float(SIG / np.sqrt(N_E)), 6))
rec("classical_CI_lo", round(float(XBAR - z95 * SIG / np.sqrt(N_E)), 6))
rec("classical_CI_hi", round(float(XBAR + z95 * SIG / np.sqrt(N_E)), 6))
w1 = (1 / 5.0 ** 2) / (1 / 5.0 ** 2 + N_E / SIG ** 2)
pm1 = w1 * MU0 + (1 - w1) * XBAR
pv1 = 1.0 / (1 / 5.0 ** 2 + N_E / SIG ** 2)
rec("credible_s05_lo", round(float(pm1 - z95 * np.sqrt(pv1)), 6))
rec("credible_s05_hi", round(float(pm1 + z95 * np.sqrt(pv1)), 6))

# ------------------------------------------------------------------ F: likelihood not a density
print("\n--- F  the likelihood does not integrate to 1 over theta ---")
# X ~ Exp(theta), one observation x = 2:  L(theta) = theta e^{-2 theta}
rec("lik_exp_integral_x2", round(1 / 2 ** 2, 6))          # int_0^inf t e^{-xt} dt = 1/x^2
rec("lik_exp_integral_x05", round(1 / 0.5 ** 2, 6))
rec("lik_exp_ML_x2", round(1 / 2.0, 6))
# n = 3 iid exponential, sum = 6: L = theta^3 e^{-6 theta}, int = 3!/6^4
from math import factorial
rec("lik_exp_integral_n3_s6", round(factorial(3) / 6 ** 4, 8))
rec("lik_exp_ML_n3_s6", round(3 / 6, 6))

# ------------------------------------------------------------------ G: alpha/beta
print("\n--- G  LRT error trade-off, H0: N(0,1) vs H1: N(1,1) ---")
N_G = 10                              # data points
sqn = np.sqrt(N_G)
tab = []
for alpha in (0.20, 0.10, 0.05, 0.01, 0.001):
    xi = stats.norm.ppf(1 - alpha) * sqn          # reject if sum X_i > xi
    beta = float(stats.norm.cdf((xi - N_G) / sqn))
    tab.append(dict(alpha=alpha, xi=round(float(xi), 4), beta=round(beta, 6)))
    rec(f"lrt_n10_alpha{alpha}", (round(float(xi), 4), round(beta, 6)))
R["lrt_table"] = tab
# same alpha = 0.05, more data
for n in (10, 40, 160):
    xi = stats.norm.ppf(0.95) * np.sqrt(n)
    zz = (xi - n) / np.sqrt(n)
    beta = float(stats.norm.sf(-zz))          # = Phi(zz), computed in the tail
    rec(f"lrt_alpha05_z_n{n}", round(float(zz), 4))
    rec(f"lrt_alpha05_beta_n{n}", f"{beta:.3e}")
# the ROC curve for Fig 5.3
al = np.linspace(1e-4, 0.9999, 400)
xi = stats.norm.ppf(1 - al) * sqn
R["roc_alpha"] = [round(float(a), 6) for a in al[::40]]
R["roc_power"] = [round(float(1 - stats.norm.cdf((x - N_G) / sqn)), 6) for x in xi[::40]]

# ------------------------------------------------------------------ H: L25 coin
print("\n--- H  L25 composite test: is my coin fair? ---")
N_H, S_H = 1000, 472
sd_H = np.sqrt(N_H * 0.25)
rec("coin_n", N_H)
rec("coin_S", S_H)
rec("coin_sd", round(float(sd_H), 6))
rec("coin_xi_CLT", round(float(z95 * sd_H), 6))
rec("coin_xi_rounded", 31)
rec("coin_dev", abs(S_H - N_H // 2))
rec("coin_reject", bool(abs(S_H - N_H // 2) > 31))
exact = float(stats.binom.cdf(531, N_H, 0.5) - stats.binom.cdf(468, N_H, 0.5))
rec("coin_exact_cover_31", round(exact, 6))
pval = float(2 * stats.binom.cdf(S_H, N_H, 0.5))
rec("coin_pvalue_exact", round(pval, 6))

# ------------------------------------------------------------------ I: confounder
print("\n--- I  regression slope with no causal link ---")
# Z ~ N(0,1) common cause;  X = Z + U,  Y = Z + V,  U,V ~ N(0,1) independent.
# cov(X,Y) = var(Z) = 1;  var(X) = 2  =>  population slope = 1/2, rho = 1/2.
rec("conf_slope_theory", 0.5)
rec("conf_rho_theory", 0.5)
z = rng.normal(size=200_000)
x = z + rng.normal(size=200_000)
y = z + rng.normal(size=200_000)
slope, icept = np.polyfit(x, y, 1)
rec("conf_slope_mc", round(float(slope), 6))
rec("conf_rho_mc", round(float(np.corrcoef(x, y)[0, 1]), 6))
# intervene: force X to a new value w/o touching Z -> Y unchanged, slope 0
x_do = rng.normal(size=200_000)        # X set by the experimenter, ignores Z
slope_do, _ = np.polyfit(x_do, y, 1)
rec("conf_slope_intervention", round(float(slope_do), 6))

with open("d:/Python-UV/MIT_Applied_Prob/computes/g7_s5.json", "w",
          encoding="utf-8") as f:
    json.dump(R, f, indent=1)
print("\nwrote computes/g7_s5.json  (%d keys)" % len(R))
