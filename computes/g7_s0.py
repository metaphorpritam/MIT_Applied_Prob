# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy"]
# ///
"""G7 §0 — orientation numbers for the classical turn.

Everything quoted in notes/src/fragments/g7_s0.html comes from here.

(a) L23 slide 3 exponential ML estimator: the estimate is a number, the
    estimator is a random variable — two data sets, two answers.
(b) L23 slide 4 bias/consistency of that estimator: exact E[hat-Theta_n]
    = n*theta/(n-1) via the Gamma(n, theta) law of the sum, checked by
    Monte Carlo.
(c) The "one model per theta" family: p_X(7; theta) for a Binomial(10, theta),
    which is the classical likelihood, contrasted with the G6 Bayesian
    posterior for the same data.
(d) A confidence interval is a probability statement about the DATA:
    exact binomial coverage of the +-1.96*sigma/sqrt(n) interval.
"""
import io
import json
import math
import sys

import numpy as np
from scipy import stats

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

R = {}


def show(key, val, fmt="{}"):
    R[key] = val
    print(f"{key:34s} = " + fmt.format(val))


# ---------------------------------------------------------------- (a)
# X_1..X_n i.i.d. exponential(theta); hat-Theta_n = n / (X_1 + ... + X_n).
THETA = 0.5          # the true (fixed, unknown-to-the-statistician) parameter
N = 20               # number of observations in one data set
show("theta_true", THETA)
show("n_obs", N)

rng = np.random.default_rng(20101202)
d1 = rng.exponential(scale=1 / THETA, size=N)
d2 = rng.exponential(scale=1 / THETA, size=N)
for tag, d in (("A", d1), ("B", d2)):
    show(f"dataset{tag}_sum", float(d.sum()), "{:.4f}")
    show(f"dataset{tag}_mean", float(d.mean()), "{:.4f}")
    show(f"dataset{tag}_mlest", float(N / d.sum()), "{:.4f}")
show("dataset_gap", abs(float(N / d1.sum()) - float(N / d2.sum())), "{:.4f}")

# ---------------------------------------------------------------- (b)
# S_n = X_1+...+X_n ~ Gamma(n, theta), so E[1/S_n] = theta/(n-1) for n >= 2
# and therefore E[hat-Theta_n] = n*theta/(n-1) exactly.
exact_mean = {}
for n in (1, 2, 5, 20, 100):
    if n == 1:
        exact_mean[n] = math.inf
    else:
        exact_mean[n] = n * THETA / (n - 1)
    show(f"E_hatTheta_n{n}", exact_mean[n], "{}")
for n in (2, 5, 20, 100):
    show(f"bias_n{n}", exact_mean[n] - THETA, "{:.6f}")
    show(f"relbias_pct_n{n}", 100 * (exact_mean[n] - THETA) / THETA, "{:.4f}")

# Monte Carlo confirmation of the n = 20 case
M = 400_000
sums = rng.gamma(shape=N, scale=1 / THETA, size=M)
mc = float(np.mean(N / sums))
show("mc_E_hatTheta_n20", mc, "{:.5f}")
show("mc_sd_hatTheta_n20", float(np.std(N / sums)), "{:.5f}")
show("mc_reps", M)

# ---------------------------------------------------------------- (c)
# One model per theta: X ~ Binomial(n_toss, theta), observed x_obs heads.
n_toss, x_obs = 10, 7
show("n_toss", n_toss)
show("x_obs", x_obs)
lik = {}
for th in (0.3, 0.5, 0.7, 0.9):
    lik[th] = float(stats.binom.pmf(x_obs, n_toss, th))
    show(f"lik_theta_{th}", lik[th], "{:.6f}")
show("lik_ratio_07_over_05", lik[0.7] / lik[0.5], "{:.4f}")
show("lik_ratio_07_over_03", lik[0.7] / lik[0.3], "{:.4f}")
show("ml_theta", x_obs / n_toss, "{:.4f}")
# G6's Bayesian answers for the identical data with a uniform prior:
show("bayes_map", x_obs / n_toss, "{:.6f}")
show("bayes_lms", (x_obs + 1) / (n_toss + 2), "{:.6f}")
show("bayes_marginal_pX7", 1 / (n_toss + 1), "{:.10f}")

# ---------------------------------------------------------------- (d)
# CI coverage: X_i i.i.d. Bernoulli(theta), sigma = sqrt(theta(1-theta)) known,
# interval M_n +- z*sigma/sqrt(n). Exact coverage by binomial enumeration.
z = float(stats.norm.ppf(1 - 0.05 / 2))
show("z_975", z, "{:.6f}")
show("Phi_1p96", float(stats.norm.cdf(1.96)), "{:.6f}")
nb, tb = 100, 0.5
sigma = math.sqrt(tb * (1 - tb))
half = z * sigma / math.sqrt(nb)
show("ci_n", nb)
show("ci_theta", tb)
show("ci_sigma", sigma)
show("ci_halfwidth", half, "{:.6f}")
k = np.arange(nb + 1)
mn = k / nb
inside = np.abs(mn - tb) <= half + 1e-12
cov = float(stats.binom.pmf(k, nb, tb)[inside].sum())
show("ci_exact_coverage", cov, "{:.6f}")
show("ci_lo_at_x50", 0.50 - half, "{:.4f}")
show("ci_hi_at_x50", 0.50 + half, "{:.4f}")
show("ci_lo_at_x58", 0.58 - half, "{:.4f}")
show("ci_hi_at_x58", 0.58 + half, "{:.4f}")

# ---------------------------------------------------------------- (e)
# "for all theta" (L23 slide 4 and slide 6): the same recipe, different theta.
# Coverage of the SAME interval rule when sigma is not known and is replaced
# by the ad hoc estimate sqrt(M_n(1-M_n)) of L23 slide 7, option 2.
show("P_Xge7_theta_half", float(stats.binom.sf(x_obs - 1, n_toss, 0.5)),
     "{:.6f}")
show("P_Xge7_theta_07", float(stats.binom.sf(x_obs - 1, n_toss, 0.7)), "{:.6f}")

tg = np.linspace(0.0, 1.0, 1_000_001)
show("max_theta_1_minus_theta", float(np.max(tg * (1 - tg))), "{:.6f}")
show("sigma_bound_bernoulli", float(np.sqrt(np.max(tg * (1 - tg)))), "{:.6f}")


def coverage_adhoc(nn, th, zz=z):
    kk = np.arange(nn + 1)
    m = kk / nn
    hw = zz * np.sqrt(m * (1 - m) / nn)
    ok = (m - hw <= th) & (th <= m + hw)
    return float(np.sum(stats.binom.pmf(kk, nn, th) * ok))


for th in (0.5, 0.3, 0.1, 0.05, 0.02):
    show(f"cov_adhoc_n100_theta{th}", coverage_adhoc(100, th), "{:.6f}")

tg2 = np.linspace(0.01, 0.99, 981)
covs = np.array([coverage_adhoc(100, float(t)) for t in tg2])
show("cov_adhoc_n100_min", float(covs.min()), "{:.6f}")
show("cov_adhoc_n100_argmin_theta", float(tg2[int(np.argmin(covs))]), "{:.4f}")
show("cov_adhoc_n100_max", float(covs.max()), "{:.6f}")

with open("d:/Python-UV/MIT_Applied_Prob/computes/g7_s0.json", "w",
          encoding="utf-8") as fh:
    json.dump(R, fh, indent=1, default=str)
print("\nwrote computes/g7_s0.json")
