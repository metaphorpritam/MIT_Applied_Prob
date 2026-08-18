# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy"]
# ///
"""Recompute every number used in notes/src/fragments/qb_s7.html (Q135-Q150).

Section 7 of the question bank: classical statistical inference.
Run:  uv run computes/qb_s7.py
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8")

J: dict[str, object] = {}


def rec(key, val, note=""):
    J[key] = val
    if isinstance(val, float):
        print(f"{key:28s} = {val:.10g}   {note}")
    else:
        print(f"{key:28s} = {val}   {note}")


rng = np.random.default_rng(60417)

# ----------------------------------------------------------------- Q135
print("\n=== Q135  bias / consistency / MSE of two shifted sample means ===")
sig, n = 2.0, 25
v = sig**2
rec("Q135_v", v, "sigma^2")
rec("Q135_varMn", v / n, "var(M_n) = sigma^2/n")
bias_A = 3.0 / n
rec("Q135_biasA", bias_A, "bias of M_n + 3/n")
mse_A = v / n + bias_A**2
rec("Q135_mseA", mse_A)
bias_B = 3.0
rec("Q135_biasB", bias_B, "bias of M_n + 3")
mse_B = v / n + bias_B**2
rec("Q135_mseB", mse_B)
rec("Q135_ratio", mse_B / mse_A, "MSE(B)/MSE(A)")
# limits of the bias as n grows
rec("Q135_biasA_n100", 3.0 / 100)
rec("Q135_mseA_n100", v / 100 + (3.0 / 100) ** 2)
# Monte Carlo cross-check (theta = 7, normal data)
theta = 7.0
N = 400_000
X = rng.normal(theta, sig, size=(N, n))
Mn = X.mean(axis=1)
rec("Q135_mc_mseA", float(np.mean((Mn + 3 / n - theta) ** 2)), "MC check of mseA")
rec("Q135_mc_mseB", float(np.mean((Mn + 3 - theta) ** 2)), "MC check of mseB")

# ----------------------------------------------------------------- Q136
print("\n=== Q136  linearly weighted estimator (2/(n(n+1))) sum i X_i ===")
n = 10
w = np.arange(1, n + 1) * 2.0 / (n * (n + 1))
rec("Q136_sum_w", float(w.sum()), "weights sum to 1 -> unbiased")
sum_i2 = n * (n + 1) * (2 * n + 1) / 6
rec("Q136_sum_i2", sum_i2, "sum_{i=1}^{10} i^2")
coef = 4 * sum_i2 / (n * (n + 1)) ** 2
rec("Q136_var_coef", coef, "var = coef * v ; closed form 2(2n+1)/(3n(n+1))")
rec("Q136_var_coef_closed", 2 * (2 * n + 1) / (3 * n * (n + 1)))
rec("Q136_var_Mn_coef", 1.0 / n, "var(M_n) = v/n")
rec("Q136_efficiency_ratio", coef / (1.0 / n), "weighted var / sample-mean var")
rec("Q136_var_coef_n100", 2 * (2 * 100 + 1) / (3 * 100 * 101), "same coef at n=100")
# How much MORE data does the weighted estimator need to match var(M_10) = v/10?
# Solve 2(2m+1)/(3m(m+1)) = 1/10  <=>  0.3 m^2 - 3.7 m - 2 = 0.
_a, _b, _c = 0.3, -3.7, -2.0
m_star = (-_b + math.sqrt(_b * _b - 4 * _a * _c)) / (2 * _a)
rec("Q136_m_for_equal_precision", float(m_star), "n such that weighted var = v/10")
rec("Q136_data_penalty_at_n10", float(m_star / n - 1), "fractional extra data at n=10")
rec("Q136_data_penalty_asymptotic", 1.0 / 3.0,
    "var ~ 4v/(3n) vs v/n, so asymptotically 1/3 more data")
rec("Q136_var_coef_check_mstar", 2 * (2 * m_star + 1) / (3 * m_star * (m_star + 1)),
    "check: equals 0.1")
# with v = 9 (sigma = 3)
rec("Q136_var_num", coef * 9.0, "v = 9")
rec("Q136_varMn_num", 9.0 / n)
# MC cross-check
Xq = rng.normal(5.0, 3.0, size=(300_000, n))
est = Xq @ w
rec("Q136_mc_mean", float(est.mean()), "MC E[estimator], theta = 5")
rec("Q136_mc_var", float(est.var()), "MC var, expect 1.145454")

# ----------------------------------------------------------------- Q137
print("\n=== Q137  uniform[0,theta]: biased c*M beats the unbiased one in MSE ===")
n = 8
E_M = n / (n + 1)          # in units of theta
E_M2 = n / (n + 2)         # in units of theta^2
rec("Q137_EM", E_M, "E[M]/theta,  n=8")
rec("Q137_EM2", E_M2, "E[M^2]/theta^2")
var_M = E_M2 - E_M**2
rec("Q137_varM", var_M, "var(M)/theta^2")
mse_ML = 2.0 / ((n + 1) * (n + 2))
rec("Q137_mse_ML", mse_ML, "MSE(M)/theta^2 = 2/((n+1)(n+2))")
c_unb = (n + 1) / n
rec("Q137_c_unb", c_unb, "unbiasing constant (n+1)/n")
mse_unb = c_unb**2 * var_M
rec("Q137_mse_unb", mse_unb, "MSE of unbiased estimator /theta^2")
c_star = E_M / E_M2
rec("Q137_c_star", c_star, "MSE-minimizing c = E[M]/E[M^2] = (n+2)/(n+1)")
rec("Q137_c_star_closed", (n + 2) / (n + 1))
mse_star = 1.0 - E_M**2 / E_M2
rec("Q137_mse_star", mse_star, "MSE at c* /theta^2")
rec("Q137_ratio_star_unb", mse_star / mse_unb, "c* MSE / unbiased MSE")
rec("Q137_pct_saved", 100 * (1 - mse_star / mse_unb), "percent MSE saved")
rec("Q137_ratio_unb_ML", mse_unb / mse_ML, "unbiased MSE / ML MSE")
# MC cross-check with theta = 3
th = 3.0
U = rng.uniform(0, th, size=(400_000, n))
M = U.max(axis=1)
rec("Q137_mc_EM", float(M.mean() / th))
rec("Q137_mc_mseML", float(np.mean((M - th) ** 2) / th**2))
rec("Q137_mc_mse_unb", float(np.mean((c_unb * M - th) ** 2) / th**2))
rec("Q137_mc_mse_star", float(np.mean((c_star * M - th) ** 2) / th**2))

# ----------------------------------------------------------------- Q138
print("\n=== Q138  conservative Bernoulli 1/4 bound, CI and sample size ===")
n, k = 900, 108
that = k / n
rec("Q138_thetahat", that)
z95 = stats.norm.ppf(0.975)
rec("Q138_z95", float(z95))
se_cons = math.sqrt(0.25 / n)
rec("Q138_se_cons", se_cons, "sqrt(1/(4n))")
m_cons = z95 * se_cons
rec("Q138_margin_cons", float(m_cons))
rec("Q138_ci_cons_lo", float(that - m_cons))
rec("Q138_ci_cons_hi", float(that + m_cons))
v_plug = that * (1 - that)
rec("Q138_v_plug", v_plug)
se_plug = math.sqrt(v_plug / n)
rec("Q138_se_plug", se_plug)
m_plug = z95 * se_plug
rec("Q138_margin_plug", float(m_plug))
rec("Q138_ci_plug_lo", float(that - m_plug))
rec("Q138_ci_plug_hi", float(that + m_plug))
rec("Q138_margin_ratio", float(m_cons / m_plug))
n_need = (z95**2 * 0.25) / 0.02**2
rec("Q138_n_need_raw", float(n_need))
rec("Q138_n_need", int(math.ceil(n_need)), "round up")
rec("Q138_margin_at_n", float(z95 * math.sqrt(0.25 / math.ceil(n_need))))
rec("Q138_max_var", 0.25, "max of theta(1-theta) at theta=1/2")
# MC coverage check of the conservative interval at the true theta = 0.12
S = rng.binomial(n, 0.12, size=200_000) / n
cov = np.mean(np.abs(S - 0.12) <= m_cons)
rec("Q138_mc_coverage_cons", float(cov), "coverage >= 0.95 (conservative)")
covp = np.mean(np.abs(S - 0.12) <= z95 * np.sqrt(S * (1 - S) / n))
rec("Q138_mc_coverage_plug", float(covp), "plug-in coverage ~ 0.95")

# ----------------------------------------------------------------- Q139
print("\n=== Q139  interpreting a 95% CI: 20 independent intervals ===")
m = 20
rec("Q139_expected_hits", 0.95 * m, "E[number covering theta]")
p_all = 0.95**m
rec("Q139_p_all", p_all, "P(all 20 cover)")
rec("Q139_p_atleast_one_miss", 1 - p_all)
rec("Q139_sd_hits", math.sqrt(m * 0.95 * 0.05))
rec("Q139_p_exactly19", float(stats.binom.pmf(19, m, 0.95)))
rec("Q139_p_le18", float(stats.binom.cdf(18, m, 0.95)))

# ----------------------------------------------------------------- Q140
print("\n=== Q140  bounded data on [0,10]: worst-case variance and sample size ===")
a, b = 0.0, 10.0
var_max = ((b - a) / 2) ** 2
rec("Q140_var_max", var_max, "max variance of a rv on [0,10] (two-point at ends)")
rec("Q140_sigma_max", math.sqrt(var_max))
z99 = stats.norm.ppf(0.995)
rec("Q140_z99", float(z99))
n_raw = (z99 * math.sqrt(var_max) / 0.5) ** 2
rec("Q140_n_raw", float(n_raw))
n140 = int(math.ceil(n_raw))
rec("Q140_n", n140)
rec("Q140_halfwidth_at_n", float(z99 * math.sqrt(var_max / n140)))
# the two tempting wrong answers
n_wrong_sigma10 = (z99 * 10 / 0.5) ** 2
rec("Q140_n_wrong_sigma10", float(math.ceil(n_wrong_sigma10)), "using sigma=10 (range as sd)")
var_unif = (b - a) ** 2 / 12
rec("Q140_var_unif", var_unif, "uniform variance -- NOT the worst case")
n_wrong_unif = int(math.ceil((z99 * math.sqrt(var_unif) / 0.5) ** 2))
rec("Q140_n_wrong_unif", n_wrong_unif)
# what that invalid n actually delivers if the truth is the worst case
rec("Q140_halfwidth_if_unif_n_but_worst_case",
    float(z99 * math.sqrt(var_max / n_wrong_unif)),
    "delivered half-width at n=222 when var is really 25")
rec("Q140_waste_factor_sigma10",
    float(math.ceil(n_wrong_sigma10) / n140),
    "how many times more data the sigma=10 shortcut demands")
rec("Q140_n_at_95", int(math.ceil((z95 * math.sqrt(var_max) / 0.5) ** 2)), "same job at 95%")
# check the two-point extremal claim numerically
ps = np.linspace(0, 1, 100001)
vv = ps * (1 - ps) * (b - a) ** 2
rec("Q140_check_extremal", float(vv.max()), "max over two-point laws = 25")

# ----------------------------------------------------------------- Q141
print("\n=== Q141  Bernoulli ML + invariance (odds) ===")
n, k = 40, 13
th_ml = k / n
rec("Q141_n", n)
rec("Q141_k", k)
rec("Q141_theta_ml", th_ml)
rec("Q141_odds_ml", th_ml / (1 - th_ml))
rec("Q141_loglik_at_ml", float(k * math.log(th_ml) + (n - k) * math.log(1 - th_ml)))
rec("Q141_loglik_at_half", float(n * math.log(0.5)))
rec("Q141_lik_ratio_ml_half",
    float(math.exp(k * math.log(th_ml) + (n - k) * math.log(1 - th_ml) - n * math.log(0.5))))
rec("Q141_p_two_more_ml", th_ml**2, "ML estimate of P(two successes in a row)")
rec("Q141_var_ml", th_ml * (1 - th_ml) / n)
rec("Q141_se_ml", math.sqrt(th_ml * (1 - th_ml) / n))

# ----------------------------------------------------------------- Q142
print("\n=== Q142  normal ML for (mu, v) on five readings, plus invariance ===")
x142 = np.array([9.8, 10.4, 9.1, 10.9, 10.3])
n = x142.size
rec("Q142_n", int(n))
rec("Q142_sum", float(x142.sum()))
mu_ml = float(x142.mean())
rec("Q142_mu_ml", mu_ml)
dev = x142 - mu_ml
rec("Q142_devs", [round(float(d), 6) for d in dev])
ss = float((dev**2).sum())
rec("Q142_sumsq_dev", ss)
v_ml = ss / n
rec("Q142_v_ml", v_ml)
s2 = ss / (n - 1)
rec("Q142_s2_unbiased", s2)
rec("Q142_ratio_s2_vml", s2 / v_ml, "= n/(n-1)")
sd_ml = math.sqrt(v_ml)
rec("Q142_sd_ml", sd_ml)
zc = (11.0 - mu_ml) / sd_ml
rec("Q142_z_for_11", zc)
rec("Q142_p_gt_11_ml", float(1 - stats.norm.cdf(zc)), "ML estimate of P(X>11) by invariance")
rec("Q142_bias_factor", (n - 1) / n, "E[v_ML] = ((n-1)/n) v")
# MC: bias of the ML variance
sims = rng.normal(0.0, 2.0, size=(300_000, 5))
vml_sim = ((sims - sims.mean(axis=1, keepdims=True)) ** 2).sum(axis=1) / 5
rec("Q142_mc_E_vml_over_v", float(vml_sim.mean() / 4.0), "expect 0.8 = (n-1)/n")

# ----------------------------------------------------------------- Q143
print("\n=== Q143  shifted exponential: ML is a corner solution at min(x_i) ===")
x143 = np.array([3.2, 4.7, 3.9, 5.1, 3.5])
n = x143.size
rec("Q143_n", int(n))
theta_ml = float(x143.min())
rec("Q143_theta_ml", theta_ml, "ML = min of the data")
rec("Q143_sum", float(x143.sum()))
rec("Q143_loglik_at_ml", float(n * theta_ml - x143.sum()), "l(theta)= n*theta - sum x")
rec("Q143_loglik_at_3", float(n * 3.0 - x143.sum()))
rec("Q143_loglik_at_2", float(n * 2.0 - x143.sum()))
rec("Q143_dl_dtheta", float(n), "derivative is +n everywhere: never zero")
rec("Q143_bias", 1.0 / n, "E[min] = theta + 1/n")
rec("Q143_E_min", theta_ml + 1.0 / n, "illustrative, at theta = theta_ml")
rec("Q143_corrected", theta_ml - 1.0 / n, "unbiased estimator min - 1/n")
rec("Q143_var_min", 1.0 / n**2)
rec("Q143_mse_ml", 1.0 / n**2 + (1.0 / n) ** 2, "MSE of the ML estimator")
rec("Q143_mse_corrected", 1.0 / n**2)
rec("Q143_mse_ratio", (1.0 / n**2 + (1.0 / n) ** 2) / (1.0 / n**2))
# MC cross-check: min of n shifted exponentials
th0 = 3.0
E = rng.exponential(1.0, size=(400_000, 5)) + th0
mins = E.min(axis=1)
rec("Q143_mc_E_min_minus_theta", float(mins.mean() - th0), "expect 1/n = 0.2")
rec("Q143_mc_var_min", float(mins.var()), "expect 1/n^2 = 0.04")

# ----------------------------------------------------------------- Q144
print("\n=== Q144  ML vs MAP vs posterior mean, 5 heads in 6 tosses ===")
n, k = 6, 5
rec("Q144_n", n)
rec("Q144_k", k)
ml = k / n
rec("Q144_ml", ml, "ML = k/n")
rec("Q144_map_flat", ml, "MAP under uniform prior = ML")
# Beta(2,2) prior:  f(theta) ∝ theta(1-theta);  posterior ∝ theta^{k+1}(1-theta)^{n-k+1}
map_beta = (k + 1) / (n + 2)
rec("Q144_map_beta22", map_beta, "argmax theta^6 (1-theta)^2 = 6/8")
pm_flat = (k + 1) / (n + 2)
rec("Q144_postmean_flat", pm_flat, "posterior mean under flat prior = (k+1)/(n+2)")
pm_beta = (k + 2) / (n + 4)
rec("Q144_postmean_beta22", pm_beta, "= (k+2)/(n+4)")
rec("Q144_ml_minus_pmflat", ml - pm_flat)
# verify the MAP maximizations numerically
tt = np.linspace(1e-9, 1 - 1e-9, 2_000_001)
post_flat = tt**k * (1 - tt) ** (n - k)
rec("Q144_check_map_flat", float(tt[np.argmax(post_flat)]))
post_b = tt ** (k + 1) * (1 - tt) ** (n - k + 1)
rec("Q144_check_map_beta", float(tt[np.argmax(post_b)]))
# verify the posterior mean by numerical integration (flat prior)
num = np.trapezoid(tt * post_flat, tt)
den = np.trapezoid(post_flat, tt)
rec("Q144_check_postmean_flat", float(num / den))

# ----------------------------------------------------------------- Q145
print("\n=== Q145  least-squares fit on five (x,y) pairs ===")
x145 = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y145 = np.array([2.1, 3.9, 6.2, 7.8, 10.0])
n = x145.size
xb, yb = float(x145.mean()), float(y145.mean())
rec("Q145_n", int(n))
rec("Q145_sumx", float(x145.sum()))
rec("Q145_sumy", float(y145.sum()))
rec("Q145_xbar", xb)
rec("Q145_ybar", yb)
Sxx = float(((x145 - xb) ** 2).sum())
Sxy = float(((x145 - xb) * (y145 - yb)).sum())
Syy = float(((y145 - yb) ** 2).sum())
rec("Q145_Sxx", Sxx)
rec("Q145_Sxy", Sxy)
rec("Q145_Syy", Syy)
th1 = Sxy / Sxx
th0 = yb - th1 * xb
rec("Q145_theta1", th1)
rec("Q145_theta0", th0)
fit = th0 + th1 * x145
res = y145 - fit
rec("Q145_fitted", [round(float(f), 6) for f in fit])
rec("Q145_residuals", [round(float(r), 6) for r in res])
rec("Q145_sum_residuals", float(res.sum()), "must be 0")
rec("Q145_sum_x_residuals", float((x145 * res).sum()), "must be 0")
SSE = float((res**2).sum())
rec("Q145_SSE", SSE)
rec("Q145_SSE_shortcut", Syy - Sxy**2 / Sxx, "= Syy - Sxy^2/Sxx")
rec("Q145_R2", 1 - SSE / Syy)
rec("Q145_pred_x6", float(th0 + th1 * 6))
rec("Q145_pred_xbar", float(th0 + th1 * xb), "equals ybar")
rec("Q145_sigma_hat2", SSE / (n - 2), "unbiased noise-variance estimate")
rec("Q145_sigma_hat", math.sqrt(SSE / (n - 2)))
# cross-check with numpy's own least squares
A = np.vstack([np.ones_like(x145), x145]).T
sol, *_ = np.linalg.lstsq(A, y145, rcond=None)
rec("Q145_np_theta0", float(sol[0]))
rec("Q145_np_theta1", float(sol[1]))

# ----------------------------------------------------------------- Q146
print("\n=== Q146  spot the error: uncentered slope formula ===")
sum_xy = float((x145 * y145).sum())
sum_x2 = float((x145**2).sum())
sum_y2 = float((y145**2).sum())
rec("Q146_sum_xy", sum_xy)
rec("Q146_sum_x2", sum_x2)
rec("Q146_sum_y2", sum_y2)
b_bad = sum_xy / sum_x2
rec("Q146_slope_uncentered", b_bad, "Sum xy / Sum x^2 -- the no-intercept slope")
rec("Q146_slope_correct", th1)
rec("Q146_slope_gap", b_bad - th1)
res_bad = y145 - b_bad * x145
SSE_bad = float((res_bad**2).sum())
rec("Q146_SSE_noint", SSE_bad)
rec("Q146_SSE_full", SSE)
rec("Q146_SSE_noint_shortcut", sum_y2 - sum_xy**2 / sum_x2)
rec("Q146_SSE_excess", SSE_bad - SSE)
# the identity Sxy = sum xy - n xbar ybar, Sxx = sum x^2 - n xbar^2
rec("Q146_Sxy_from_raw", sum_xy - n * xb * yb)
rec("Q146_Sxx_from_raw", sum_x2 - n * xb**2)
# what happens if you also mis-report the intercept as zero at x = 0
rec("Q146_pred0_full", th0)
rec("Q146_pred0_noint", 0.0)

# ----------------------------------------------------------------- Q147
print("\n=== Q147  what the fitted line does NOT claim ===")
rec("Q147_R2", 1 - SSE / Syy, "same fit as Q145")
rec("Q147_slope", th1)
rec("Q147_pred_x12", float(th0 + th1 * 12), "extrapolation")
rec("Q147_resid_sd", math.sqrt(SSE / (n - 2)))
# CI for the slope with sigma unknown: t_{n-2}
tcrit = float(stats.t.ppf(0.975, n - 2))
rec("Q147_t_crit", tcrit)
se_slope = math.sqrt(SSE / (n - 2) / Sxx)
rec("Q147_se_slope", se_slope)
rec("Q147_slope_ci_lo", th1 - tcrit * se_slope)
rec("Q147_slope_ci_hi", th1 + tcrit * se_slope)
# regressing x on y gives a different line
b1_rev = Sxy / Syy
rec("Q147_slope_x_on_y", b1_rev)
rec("Q147_product_of_slopes", th1 * b1_rev, "= R^2, not 1")
rec("Q147_one_over_slope", 1 / th1)

# ----------------------------------------------------------------- Q148
print("\n=== Q148  binomial LRT: H0 p=0.1 vs H1 p=0.3, n=10 ===")
n, p0, p1 = 10, 0.1, 0.3
xobs = 4
Lx = ((p1 / p0) ** xobs) * (((1 - p1) / (1 - p0)) ** (n - xobs))
rec("Q148_ratio_p", p1 / p0)
rec("Q148_ratio_q", (1 - p1) / (1 - p0))
rec("Q148_L_at_4", float(Lx))
rec("Q148_L_at_4_check",
    float(stats.binom.pmf(xobs, n, p1) / stats.binom.pmf(xobs, n, p0)))
rec("Q148_L_at_0", float(((1 - p1) / (1 - p0)) ** n))
rec("Q148_L_at_2", float((p1 / p0) ** 2 * ((1 - p1) / (1 - p0)) ** 8))
rec("Q148_L_at_3", float((p1 / p0) ** 3 * ((1 - p1) / (1 - p0)) ** 7))
rec("Q148_L_growth_factor", float((p1 / p0) * ((1 - p0) / (1 - p1))), "L(k+1)/L(k)")
for k in range(0, 7):
    rec(f"Q148_tail_H0_ge{k}", float(1 - stats.binom.cdf(k - 1, n, p0)))
rec("Q148_pmf3_H0", float(stats.binom.pmf(3, n, p0)))
rec("Q148_pmf4_H0", float(stats.binom.pmf(4, n, p0)))
kstar = min(k for k in range(0, n + 1) if 1 - stats.binom.cdf(k - 1, n, p0) <= 0.05)
rec("Q148_kstar", int(kstar), "smallest k with exact tail <= 0.05")
alpha_star = float(1 - stats.binom.cdf(kstar - 1, n, p0))
rec("Q148_alpha_star", alpha_star)
beta_star = float(stats.binom.cdf(kstar - 1, n, p1))
rec("Q148_beta_star", beta_star)
rec("Q148_power_star", 1 - beta_star)
# the k = 3 alternative (tail slightly above 0.05)
rec("Q148_alpha_k3", float(1 - stats.binom.cdf(2, n, p0)))
rec("Q148_beta_k3", float(stats.binom.cdf(2, n, p1)))
# Threshold xi on L corresponding to R = {L(X) > xi} = {X >= 4}.
# L is strictly increasing, so {L(X) > xi} = {X >= 4} iff L(3) <= xi < L(4):
# the admissible set is the HALF-OPEN interval [L(3), L(4)).  At xi = L(4)
# exactly, the strict inequality gives {X >= 5} (alpha = 0.0016349) instead.
rec("Q148_xi_range_lo", float((p1 / p0) ** 3 * ((1 - p1) / (1 - p0)) ** 7),
    "L(3): INCLUDED endpoint of [L(3), L(4))")
rec("Q148_xi_range_hi", float(Lx), "L(4): EXCLUDED endpoint of [L(3), L(4))")
# MC cross-check
b0 = rng.binomial(n, p0, size=400_000)
b1 = rng.binomial(n, p1, size=400_000)
rec("Q148_mc_alpha", float(np.mean(b0 >= kstar)))
rec("Q148_mc_beta", float(np.mean(b1 < kstar)))

# ----------------------------------------------------------------- Q149
print("\n=== Q149  'not rejected' does not mean 'true': the beta of the test ===")
n, sigma = 9, 1.0
alpha = 0.05
z_a = float(stats.norm.ppf(1 - alpha))
rec("Q149_z_alpha", z_a)
thresh = z_a * sigma / math.sqrt(n)
rec("Q149_threshold_on_Mn", thresh, "reject if M_n > this")
mu1 = 0.5
shift = mu1 * math.sqrt(n) / sigma
rec("Q149_shift", shift, "mu1*sqrt(n)/sigma")
beta = float(stats.norm.cdf(z_a - shift))
rec("Q149_beta", beta, "P(fail to reject | mu = 0.5)")
rec("Q149_power", 1 - beta)
# how big must n be to push beta to 0.10?
z_b = float(stats.norm.ppf(0.90))
n_need = ((z_a + z_b) * sigma / mu1) ** 2
rec("Q149_n_for_beta10_raw", n_need)
rec("Q149_n_for_beta10", int(math.ceil(n_need)))
rec("Q149_beta_at_that_n",
    float(stats.norm.cdf(z_a - mu1 * math.sqrt(math.ceil(n_need)) / sigma)))
# MC cross-check
Mn9 = rng.normal(0.5, sigma / math.sqrt(n), size=500_000)
rec("Q149_mc_beta", float(np.mean(Mn9 <= thresh)))
Mn0 = rng.normal(0.0, sigma / math.sqrt(n), size=500_000)
rec("Q149_mc_alpha", float(np.mean(Mn0 > thresh)))

# ----------------------------------------------------------------- Q150
print("\n=== Q150  exponential LRT: lambda=1 vs lambda=1/2, n=10 ===")
n, lam0, lam1 = 10, 1.0, 0.5
rec("Q150_n", n)
xi = float(stats.gamma.ppf(0.95, a=n, scale=1 / lam0))
rec("Q150_xi", xi, "0.95 quantile of Gamma(10, rate 1)")
rec("Q150_check_alpha", float(1 - stats.gamma.cdf(xi, a=n, scale=1 / lam0)))
beta150 = float(stats.gamma.cdf(xi, a=n, scale=1 / lam1))
rec("Q150_beta", beta150)
rec("Q150_power", 1 - beta150)
rec("Q150_mean_H0", n / lam0)
rec("Q150_mean_H1", n / lam1)
rec("Q150_xi_over_n", xi / n, "equivalent threshold on the sample mean")
# threshold on the likelihood ratio itself
xi_L = float((lam1 / lam0) ** n * math.exp((lam0 - lam1) * xi))
rec("Q150_xi_on_L", xi_L, "L(x) = (1/2)^n exp(S/2) at S = xi")
rec("Q150_L_factor", 0.5**n)
# alpha = 0.01 version, showing the trade-off
xi_01 = float(stats.gamma.ppf(0.99, a=n, scale=1 / lam0))
rec("Q150_xi_alpha01", xi_01)
rec("Q150_beta_alpha01", float(stats.gamma.cdf(xi_01, a=n, scale=1 / lam1)))
xi_10 = float(stats.gamma.ppf(0.90, a=n, scale=1 / lam0))
rec("Q150_xi_alpha10", xi_10)
rec("Q150_beta_alpha10", float(stats.gamma.cdf(xi_10, a=n, scale=1 / lam1)))
# smallest n with beta <= 0.05 at alpha = 0.05
nn = n
while True:
    x_ = stats.gamma.ppf(0.95, a=nn, scale=1 / lam0)
    b_ = stats.gamma.cdf(x_, a=nn, scale=1 / lam1)
    if b_ <= 0.05:
        break
    nn += 1
rec("Q150_n_for_beta05", int(nn))
rec("Q150_beta_at_that_n", float(b_))
rec("Q150_xi_at_that_n", float(x_))
# MC cross-check at n = 10
S0 = rng.exponential(1 / lam0, size=(300_000, n)).sum(axis=1)
S1 = rng.exponential(1 / lam1, size=(300_000, n)).sum(axis=1)
rec("Q150_mc_alpha", float(np.mean(S0 > xi)))
rec("Q150_mc_beta", float(np.mean(S1 <= xi)))

# ------------------------------------------------- extra numbers quoted in prose
print("\n=== extra values quoted in the solutions ===")
rec("Q135_bias_share_n25", 0.0144 / 0.1744, "squared-bias share of MSE at n=25")
rec("Q135_bias_share_n100", 0.0009 / 0.0409, "squared-bias share at n=100")
rec("Q136_excess_pct", 100 * (0.1272727272727 / 0.1 - 1), "percent extra MSE")
rec("Q137_ML_over_unb", 1 / 0.5625, "MSE(M)/MSE(unbiased)")
rec("Q138_z_sq", float(z95**2))
rec("Q138_n_if_guess012", int(math.ceil(z95**2 * 0.1056 / 0.02**2)), "wrong design n")
rec("Q138_margin_if_theta_half",
    float(z95 * math.sqrt(0.25 / math.ceil(z95**2 * 0.1056 / 0.02**2))),
    "delivered margin if theta near 1/2")
rec("Q139_z99_over_z95", float(z99 / z95), "how much wider a 99% interval is")
rec("Q140_cost_99_over_95", float((z99 / z95) ** 2), "data cost of 99% vs 95%")
rec("Q140_n_forget_rescale", int(math.ceil((z99 * 0.5 / 0.5) ** 2)), "the 1/4-bound slip")
rec("Q141_loglik_diff", float(-25.2232411 - (-27.7258872)))
rec("Q142_wrong_sd", math.sqrt(0.465))
rec("Q142_wrong_z", float(0.9 / math.sqrt(0.465)))
rec("Q142_wrong_tail", float(1 - stats.norm.cdf(0.9 / math.sqrt(0.465))))
rec("Q142_wrong_tail_excess", float((1 - stats.norm.cdf(0.9 / math.sqrt(0.465))) / 0.0700245606 - 1))
rec("Q144_int_num", math.factorial(6) * math.factorial(1) / math.factorial(8))
rec("Q144_int_den", math.factorial(5) * math.factorial(1) / math.factorial(7))
rec("Q146_slope_shift50", float((109.7 + 50 * 15) / 55), "y shifted up by 50, uncentered slope")
rec("Q146_pred3_spliced", float(0.09 + 1.994545455 * 3), "spliced line at x=3, vs ybar=6")
rec("Q148_ratio_q_inv", float(0.9 / 0.7))
rec("Q148_power_gain_k3", float((1 - 0.3827827864) - (1 - 0.6496107184)), "power gained by k=3")
rec("Q149_z90", float(stats.norm.ppf(0.90)))
rec("Q149_sqrtn_shift35", float(0.5 * math.sqrt(35)))
rec("Q150_exp_half_xi", float(math.exp(15.70521642 / 2)))
rec("Q150_sd_H1", float(math.sqrt(10) / 0.5))
rec("Q150_sd_gap", float((20 - 15.70521642) / (math.sqrt(10) / 0.5)), "threshold is this many sd below H1 mean")

# ----------------------------------------------------------------- Q151
print("\n=== Q151  least squares = ML under normal noise (G7 sect.3.5) ===")
x151 = np.array([2.0, 4.0, 6.0, 8.0, 10.0, 12.0])
y151 = np.array([5.0, 6.2, 7.5, 8.4, 9.9, 11.0])
n151 = len(x151)
rec("Q151_n", n151)
rec("Q151_sum_x", float(x151.sum()))
rec("Q151_sum_y", float(y151.sum()))
xb151, yb151 = float(x151.mean()), float(y151.mean())
rec("Q151_xbar", xb151)
rec("Q151_ybar", yb151)
Sxx151 = float(((x151 - xb151) ** 2).sum())
Sxy151 = float(((x151 - xb151) * (y151 - yb151)).sum())
Syy151 = float(((y151 - yb151) ** 2).sum())
rec("Q151_Sxx", Sxx151)
rec("Q151_Sxy", Sxy151)
rec("Q151_Syy", Syy151)
th1_151 = Sxy151 / Sxx151
th0_151 = yb151 - th1_151 * xb151
rec("Q151_theta1", float(th1_151))
rec("Q151_theta0", float(th0_151))
fit151 = th0_151 + th1_151 * x151
res151 = y151 - fit151
rec("Q151_fitted", [round(float(t), 7) for t in fit151])
rec("Q151_residuals", [round(float(t), 7) for t in res151])
SSE151 = float((res151**2).sum())
rec("Q151_SSE", SSE151)
rec("Q151_SSE_shortcut", Syy151 - Sxy151**2 / Sxx151, "Syy - Sxy^2/Sxx")
rec("Q151_R2", 1 - SSE151 / Syy151)
rec("Q151_sigma2_ML", SSE151 / n151, "SSE/n")
rec("Q151_sigma2_unb", SSE151 / (n151 - 2), "SSE/(n-2)")
rec("Q151_sigma_ML", float(math.sqrt(SSE151 / n151)))
rec("Q151_sigma_unb", float(math.sqrt(SSE151 / (n151 - 2))))
rec("Q151_ML_bias_factor", (n151 - 2) / n151, "E[sigma2_ML] = (n-2)/n * sigma^2")
rec("Q151_ML_underestimate_pct", 1 - (n151 - 2) / n151)
# numpy least squares cross-check
A151 = np.vstack([np.ones(n151), x151]).T
sol151 = np.linalg.lstsq(A151, y151, rcond=None)[0]
rec("Q151_lstsq_theta0", float(sol151[0]))
rec("Q151_lstsq_theta1", float(sol151[1]))
# direct grid maximization of the log-likelihood, to show ML = LS numerically
gv = np.linspace(0.001, 2.0, 400_000)
ll_v = -n151 / 2 * np.log(2 * np.pi * gv) - SSE151 / (2 * gv)
rec("Q151_grid_vhat", float(gv[int(np.argmax(ll_v))]), "argmax over v of profile loglik")
rec("Q151_loglik_max", float(ll_v.max()))
# weighted (heteroskedastic) variant: variances proportional to x
wts151 = 1.0 / x151
Sw = wts151.sum()
xw = float((wts151 * x151).sum() / Sw)
yw = float((wts151 * y151).sum() / Sw)
th1w = float((wts151 * (x151 - xw) * (y151 - yw)).sum()
             / (wts151 * (x151 - xw) ** 2).sum())
th0w = yw - th1w * xw
rec("Q151_wls_theta1", th1w, "weights 1/x_i (sigma_i^2 prop to x_i)")
rec("Q151_wls_theta0", th0w)

# ----------------------------------------------------------------- Q152
print("\n=== Q152  multiple / polynomial regression (G7 sect.3.7) ===")
x152 = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
y152 = np.array([2.0, 4.6, 8.1, 12.9, 18.7, 25.9])
n152 = len(x152)
rec("Q152_n", n152)
xb152, yb152 = float(x152.mean()), float(y152.mean())
rec("Q152_xbar", xb152)
rec("Q152_ybar", yb152)
Sxx152 = float(((x152 - xb152) ** 2).sum())
Sxy152 = float(((x152 - xb152) * (y152 - yb152)).sum())
Syy152 = float(((y152 - yb152) ** 2).sum())
rec("Q152_Sxx", Sxx152)
rec("Q152_Sxy", Sxy152)
rec("Q152_Syy", Syy152)
lin_t1 = Sxy152 / Sxx152
lin_t0 = yb152 - lin_t1 * xb152
rec("Q152_line_theta1", float(lin_t1))
rec("Q152_line_theta0", float(lin_t0))
lin_res = y152 - (lin_t0 + lin_t1 * x152)
SSE_lin = float((lin_res**2).sum())
rec("Q152_line_SSE", SSE_lin)
rec("Q152_line_R2", 1 - SSE_lin / Syy152)
rec("Q152_line_residuals", [round(float(t), 7) for t in lin_res])
# quadratic fit: design matrix [1, x, x^2]
A152 = np.vstack([np.ones(n152), x152, x152**2]).T
q = np.linalg.lstsq(A152, y152, rcond=None)[0]
rec("Q152_quad_theta0", float(q[0]))
rec("Q152_quad_theta1", float(q[1]))
rec("Q152_quad_theta2", float(q[2]))
quad_fit = A152 @ q
quad_res = y152 - quad_fit
rec("Q152_quad_fitted", [round(float(t), 7) for t in quad_fit])
rec("Q152_quad_residuals", [round(float(t), 7) for t in quad_res])
SSE_quad = float((quad_res**2).sum())
rec("Q152_quad_SSE", SSE_quad)
rec("Q152_quad_R2", 1 - SSE_quad / Syy152)
rec("Q152_SSE_drop", SSE_lin - SSE_quad)
# the three normal-equation sums used in the write-up
rec("Q152_sum_x", float(x152.sum()))
rec("Q152_sum_x2", float((x152**2).sum()))
rec("Q152_sum_x3", float((x152**3).sum()))
rec("Q152_sum_x4", float((x152**4).sum()))
rec("Q152_sum_y", float(y152.sum()))
rec("Q152_sum_xy", float((x152 * y152).sum()))
rec("Q152_sum_x2y", float((x152**2 * y152).sum()))
# orthogonality of the quadratic residuals to each column
rec("Q152_orth_1", float(quad_res.sum()))
rec("Q152_orth_x", float((x152 * quad_res).sum()))
rec("Q152_orth_x2", float((x152**2 * quad_res).sum()))
rec("Q152_line_orth_x2", float((x152**2 * lin_res).sum()),
    "the LINE's residuals are NOT orthogonal to x^2")
# adjusted R^2, to make the model-choice point quantitative
rec("Q152_line_adjR2", 1 - (SSE_lin / (n152 - 2)) / (Syy152 / (n152 - 1)))
rec("Q152_quad_adjR2", 1 - (SSE_quad / (n152 - 3)) / (Syy152 / (n152 - 1)))
# a degree-5 polynomial through all six points: SSE = 0 exactly, R^2 = 1
A5 = np.vander(x152, 6, increasing=True)
c5 = np.linalg.solve(A5, y152)
rec("Q152_deg5_SSE", float(((y152 - A5 @ c5) ** 2).sum()), "interpolates: SSE = 0")

# ----------------------------------------------------------------- Q153
print("\n=== Q153  LRT on a normal variance: N(0,4) vs N(0,9), n=8 (G7 sect.4.4) ===")
n153, v0, v1 = 8, 4.0, 9.0
rec("Q153_n", n153)
rec("Q153_const_ratio", float((math.sqrt(v0) / math.sqrt(v1)) ** n153),
    "(sigma0/sigma1)^n, the constant in L(x)")
coef153 = 0.5 / v0 - 0.5 / v1
rec("Q153_exp_coef", float(coef153), "1/(2 v0) - 1/(2 v1) > 0 -> upper tail")
chi95_8 = float(stats.chi2.ppf(0.95, n153))
rec("Q153_chi2_8_q95", chi95_8)
xi153 = v0 * chi95_8
rec("Q153_xi_prime", float(xi153), "threshold on sum x_i^2")
rec("Q153_alpha_check",
    float(1 - stats.chi2.cdf(xi153 / v0, n153)), "= 0.05")
beta153 = float(stats.chi2.cdf(xi153 / v1, n153))
rec("Q153_beta", beta153)
rec("Q153_power", 1 - beta153)
rec("Q153_beta_arg", float(xi153 / v1), "xi'/9, the chi^2_8 argument for beta")
# threshold on the likelihood ratio itself
xi_L153 = float((math.sqrt(v0 / v1)) ** n153 * math.exp(coef153 * xi153))
rec("Q153_xi_on_L", xi_L153)
# observed data value asked about in part (b)
rec("Q153_obs_sum_sq", 60.0, "the observed sum of squares in the stem")
rec("Q153_obs_L", float((math.sqrt(v0 / v1)) ** n153 * math.exp(coef153 * 60.0)))
rec("Q153_obs_pvalue", float(1 - stats.chi2.cdf(60.0 / v0, n153)))
# MC cross-check
z153 = rng.normal(0.0, 1.0, size=(300_000, n153))
s0 = (math.sqrt(v0) * z153) ** 2
s1 = (math.sqrt(v1) * z153) ** 2
rec("Q153_mc_alpha", float(np.mean(s0.sum(axis=1) > xi153)))
rec("Q153_mc_beta", float(np.mean(s1.sum(axis=1) <= xi153)))
# part (d): if H1 said N(0,1) instead, the coefficient flips sign -> lower tail
rec("Q153_flip_coef", float(0.5 / v0 - 0.5 / 1.0), "negative -> LOWER tail")
xi_lo = v0 * float(stats.chi2.ppf(0.05, n153))
rec("Q153_flip_xi_prime", float(xi_lo))
rec("Q153_flip_beta", float(1 - stats.chi2.cdf(xi_lo / 1.0, n153)))

# ----------------------------------------------------------------- Q154
print("\n=== Q154  composite H1: significance test + p-value (G7 sect.4.7) ===")
n154, th0_154, s154 = 500, 0.20, 88
rec("Q154_n", n154)
rec("Q154_mean_H0", n154 * th0_154)
var154 = n154 * th0_154 * (1 - th0_154)
rec("Q154_var_H0", float(var154))
sd154 = math.sqrt(var154)
rec("Q154_sd_H0", float(sd154))
z975 = float(stats.norm.ppf(0.975))
rec("Q154_z975", z975)
xi154 = z975 * sd154
rec("Q154_xi_raw", float(xi154), "CLT critical deviation")
xi154_int = math.ceil(xi154)
rec("Q154_xi_int", int(xi154_int), "rounded UP, so the region never grows")
rec("Q154_obs_dev", abs(s154 - n154 * th0_154))
lo154 = n154 * th0_154 - xi154_int
hi154 = n154 * th0_154 + xi154_int
rec("Q154_region_lo", int(lo154), "reject iff S <= this")
rec("Q154_region_hi", int(hi154), "reject iff S >= this")
rec("Q154_exact_alpha",
    float(stats.binom.cdf(lo154 - 1, n154, th0_154)
          + 1 - stats.binom.cdf(hi154 - 1, n154, th0_154)),
    "exact binomial level of the integer region")
rec("Q154_pvalue_exact", float(2 * stats.binom.cdf(s154, n154, th0_154)))
rec("Q154_pvalue_clt", float(2 * (1 - stats.norm.cdf(12.0 / sd154))))
rec("Q154_pvalue_clt_cc", float(2 * (1 - stats.norm.cdf(11.5 / sd154))),
    "with continuity correction")
# power against three specific alternatives (exact binomial)


def _pow154(th):
    return float(stats.binom.cdf(lo154 - 1, n154, th)
                 + 1 - stats.binom.cdf(hi154 - 1, n154, th))


for th in (0.16, 0.17, 0.24):
    rec(f"Q154_power_at_{str(th).replace('.', 'p')}", _pow154(th))
rec("Q154_beta_at_0p17", 1 - _pow154(0.17))

# ----------------------------------------------------------------- Q155
print("\n=== Q155  chi-square goodness of fit, non-uniform null (G7 sect.4.8) ===")
counts155 = np.array([168.0, 66.0, 71.0, 15.0])
theta155 = np.array([9 / 16, 3 / 16, 3 / 16, 1 / 16])
n155 = float(counts155.sum())
m155 = len(counts155)
rec("Q155_n", n155)
rec("Q155_m", m155)
exp155 = n155 * theta155
rec("Q155_expected", [round(float(t), 7) for t in exp155])
rec("Q155_min_expected", float(exp155.min()), "rule of thumb wants >= 5")
terms155 = (counts155 - exp155) ** 2 / exp155
rec("Q155_terms", [round(float(t), 7) for t in terms155])
T155 = float(terms155.sum())
rec("Q155_T", T155)
rec("Q155_T_scipy", float(stats.chisquare(counts155, exp155).statistic))
rec("Q155_df", m155 - 1)
crit155 = float(stats.chi2.ppf(0.95, m155 - 1))
rec("Q155_crit_05", crit155)
rec("Q155_pvalue", float(1 - stats.chi2.cdf(T155, m155 - 1)))
# the exact generalized log-likelihood-ratio statistic, for comparison
S155 = float((counts155 * np.log(counts155 / exp155)).sum())
rec("Q155_S", S155)
rec("Q155_2S", 2 * S155)
rec("Q155_2S_pvalue", float(1 - stats.chi2.cdf(2 * S155, m155 - 1)))
# part (d): one parameter estimated from the data costs one more degree of freedom
rec("Q155_df_estimated", m155 - 2)
rec("Q155_crit_05_estimated", float(stats.chi2.ppf(0.95, m155 - 2)))
rec("Q155_pvalue_estimated", float(1 - stats.chi2.cdf(T155, m155 - 2)))
# MC cross-check of the null distribution of T
mc155 = rng.multinomial(int(n155), theta155, size=200_000).astype(float)
Tmc = ((mc155 - exp155) ** 2 / exp155).sum(axis=1)
rec("Q155_mc_crit_05", float(np.quantile(Tmc, 0.95)))
rec("Q155_mc_pvalue", float(np.mean(Tmc > T155)))
rec("Q155_mc_mean", float(Tmc.mean()), "theory: df = 3")
rec("Q155_mc_var", float(Tmc.var()), "theory: 2 df = 6")

# ----------------------------------------------------------------- Q156
print("\n=== Q156  which test? the four boxes of the G7 sect.4.9 decision guide ===")
prior1 = 0.05
rec("Q156_prior_odds", float((1 - prior1) / prior1), "MAP threshold on L(x)")
rec("Q156_z99", float(stats.norm.ppf(0.99)), "one-sided LRT threshold at alpha=0.01")
rec("Q156_lrt_threshold_x", float(stats.norm.ppf(0.99) * 2.0),
    "sigma = 2: reject when X > sigma z_0.99")
rec("Q156_lrt_beta", float(stats.norm.cdf((stats.norm.ppf(0.99) * 2.0 - 3.0) / 2.0)),
    "beta at mu1 = 3, sigma = 2")
rec("Q156_ks_crit", float(1.36 / math.sqrt(150)), "KS critical D_n at n=150")
rec("Q156_ks_crit_exact", float(stats.ksone.ppf(1 - 0.05 / 2, 150)),
    "exact two-sided 5% critical value of D_150")
rec("Q156_sig_z975", float(stats.norm.ppf(0.975)), "two-sided significance test")
rec("Q156_sig_xi", float(stats.norm.ppf(0.975) * 6.0 / math.sqrt(64)),
    "sigma=6, n=64: critical deviation of the sample mean")

print("\n=== step-level intermediates written out in the solutions ===")
rec("Q135_bias_sq_n25", 0.12 ** 2)
rec("Q137_EM_sq_n8", (8 / 9) ** 2, "E[M]^2 / theta^2 at n=8")
rec("Q137_c_unb_sq", 1.125 ** 2)
rec("Q138_plugin_var_over_n", 0.1056 / 900, "plug-in variance / n")
rec("Q140_sqrt_varmax_over_n", float(math.sqrt(25 / 664)))
rec("Q140_z_times_sigma_max", float(z99 * 5 / 0.5), "z*sigma_max/halfwidth, squared to get n_raw")
rec("Q141_neg_loglik_hat", float(-(13 * math.log(0.325) + 27 * math.log(0.675))))
rec("Q141_neg_loglik_half", float(-40 * math.log(0.5)))
rec("Q145_SSE_e2_4", 0.17 ** 2)
rec("Q145_SSE_e5_2", 0.06 ** 2)
rec("Q145_SSE_over_Syy", 0.091 / 38.90)
rec("Q146_Sxy_from_raw", 19.7 ** 2 / 10, "Sxy^2/Sxx used in the SSE shortcut")
rec("Q146_no_int_second_term", 109.7 ** 2 / 55)
rec("Q146_spliced_slope_times_xbar", float(1.9945454545454545 * 3))
rec("Q147_slope_ci_halfwidth", float(3.1824463052837078 * 0.055075705472861024))
rec("Q147_power_complement_a01", 1 - 0.4640388082, "1-beta at alpha=0.01 (Q150 table)")
rec("Q147_power_complement_a10", 1 - 0.1801000006, "1-beta at alpha=0.10 (Q150 table)")
rec("Q148_L4_tail_factor", float((7 / 9) ** 6), "(0.7777778)^6")
rec("Q149_stderr", 1 / 3.0, "sigma/sqrt(n) at n=9")
rec("Q149_beta_z_arg", float((0.5482845423 - 0.5) / (1 / 3.0)))
rec("Q149_check_z_at_n35", float(0.5 * math.sqrt(35) - 1.6448536269514722))
rec("Q149_sqrtn_needed", float((1.6448536269514722 + 1.2815515655446004) / 0.5))
rec("Q150_half_xi", float(15.70521642 / 2))
# the alpha-beta tradeoff, stated as ratios (the table has ONE factor-of-five step)
rec("Q150_beta_ratio_10_to_05", float(0.2652645 / 0.1801000),
    "alpha halved (0.10 -> 0.05): beta multiplied by this")
rec("Q150_beta_ratio_05_to_01", float(0.4640388 / 0.2652645),
    "alpha / 5 (0.05 -> 0.01): beta multiplied by this")
rec("Q150_beta_ratio_10_to_01", float(0.4640388 / 0.1801000),
    "alpha / 10 (0.10 -> 0.01), the full span of the table: beta multiplied by this")

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(J, indent=1, sort_keys=True), encoding="utf-8")
print(f"\nWrote {out}  ({len(J)} keys)")
