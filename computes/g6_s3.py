# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Numbers for G6 section 3 - Bayesian inference: priors, posteriors, MAP.

Sources: L21 slides 2-5, rec22 P1(a)-(d), B&T sections 8.1-8.2
(Examples 8.1-8.4, 8.7, 8.8).

Run:  uv run computes/g6_s3.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from math import comb, exp, factorial, log, pi, sqrt
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
from scipy import integrate, optimize, stats

ROOT = Path(__file__).resolve().parent
OUT: dict[str, object] = {}


def rec(key, val, note=""):
    if isinstance(val, Fraction):
        val = float(val)
    if isinstance(val, np.ndarray):
        val = val.tolist()
    OUT[key] = val
    print(f"{key:46s} = {val!r}   {note}")


def head(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# ===========================================================================
head("A. Coin with unknown bias: uniform prior + binomial data (L21 slide 4)")
# f_Theta = 1 on [0,1];  p_{X|Theta}(x|theta) = C(n,x) theta^x (1-theta)^{n-x}
# posterior = Beta(x+1, n-x+1);  marginal p_X(x) = 1/(n+1)

n, k = 10, 7
rec("A_n", n)
rec("A_k", k)

# normalizing integral  int_0^1 theta^k (1-theta)^{n-k} dtheta = k!(n-k)!/(n+1)!
beta_int_exact = Fraction(factorial(k) * factorial(n - k), factorial(n + 1))
beta_int_num = integrate.quad(lambda t: t**k * (1 - t) ** (n - k), 0, 1)[0]
rec("A_beta_integral_exact_str", f"{k}!{n-k}!/{n+1}! = {beta_int_exact}")
rec("A_beta_integral_exact", float(beta_int_exact))
rec("A_beta_integral_quad", beta_int_num)
rec("A_beta_integral_err", abs(float(beta_int_exact) - beta_int_num))

# marginal p_X(k)
pX = comb(n, k) * float(beta_int_exact)
rec("A_comb_n_k", comb(n, k))
rec("A_pX_k", pX, "= 1/(n+1)")
rec("A_pX_k_exact", 1.0 / (n + 1))
# check for all k
rec("A_pX_uniform_max_dev",
    max(abs(comb(n, j) * factorial(j) * factorial(n - j) / factorial(n + 1)
            - 1 / (n + 1)) for j in range(n + 1)))

post = stats.beta(k + 1, n - k + 1)
rec("A_post_alpha", k + 1)
rec("A_post_beta", n - k + 1)
rec("A_MAP", k / n)
rec("A_post_mean", (k + 1) / (n + 2))
rec("A_post_mean_frac", str(Fraction(k + 1, n + 2)))
rec("A_post_var", post.var())
rec("A_post_sd", post.std())
rec("A_post_density_at_MAP", post.pdf(k / n))
rec("A_post_P_gt_half", post.sf(0.5))
rec("A_post_median", post.median())
# numeric check of the mean by quadrature on the explicit density
dens = lambda t: t**k * (1 - t) ** (n - k) / float(beta_int_exact)
rec("A_mean_quad", integrate.quad(lambda t: t * dens(t), 0, 1)[0])
rec("A_dens_integrates_to", integrate.quad(dens, 0, 1)[0])
# mode from derivative condition, numerically
rec("A_MAP_numeric",
    float(optimize.minimize_scalar(lambda t: -dens(t), bounds=(1e-9, 1 - 1e-9),
                                   method="bounded").x))

# narrowing sequence: same frequency 0.7, growing n  (figure 3.3)
narrow = []
for nn in (0, 10, 20, 40, 100):
    kk = int(round(0.7 * nn))
    b = stats.beta(kk + 1, nn - kk + 1)
    narrow.append({"n": nn, "k": kk, "mean": b.mean(), "sd": b.std(),
                   "MAP": (kk / nn if nn else float("nan"))})
    print(f"   n={nn:4d} k={kk:3d}  mean={b.mean():.6f} sd={b.std():.6f}")
rec("A_narrowing", narrow)
rec("A_sd_ratio_100_over_10", narrow[-1]["sd"] / narrow[1]["sd"])
rec("A_sd_ratio_asymptote", 1 / sqrt(10.0), "the 1/sqrt(n) prediction")
rec("A_sd_ratio_100_over_10_rel_err",
    abs(narrow[-1]["sd"] / narrow[1]["sd"] - 1 / sqrt(10.0)) * sqrt(10.0),
    "the +2 in the Beta denominator is what makes n=10 -> 100 a poor decade")
# a decade further out, where the +2 no longer matters
sd_100 = stats.beta(71, 31).std()
sd_1000 = stats.beta(701, 301).std()
rec("A_sd_n1000", sd_1000)
rec("A_sd_ratio_1000_over_100", sd_1000 / sd_100)
rec("A_sd_ratio_1000_over_100_rel_err",
    abs(sd_1000 / sd_100 - 1 / sqrt(10.0)) * sqrt(10.0))

# small-n contrast MAP vs mean
for (nn, kk) in ((1, 1), (2, 2), (4, 3), (10, 7)):
    rec(f"A_contrast_n{nn}_k{kk}", {"MAP": kk / nn, "mean": (kk + 1) / (nn + 2)})

# ===========================================================================
head("B. Normal prior x normal noise (B&T Example 8.3): conjugate update")


def normal_post(x0, v0, xs, vs):
    """Posterior mean/var for Theta ~ N(x0,v0), X_i|theta ~ N(theta, vs_i) indep."""
    prec = 1.0 / v0 + sum(1.0 / v for v in vs)
    m = (x0 / v0 + sum(x / v for x, v in zip(xs, vs))) / prec
    return m, 1.0 / prec


# one observation, hand-checkable numbers
x0, v0, x1, s2 = 1.0, 4.0, 3.0, 1.0
m1, v1 = normal_post(x0, v0, [x1], [s2])
rec("B1_prior_mean", x0)
rec("B1_prior_var", v0)
rec("B1_obs", x1)
rec("B1_noise_var", s2)
rec("B1_prior_precision", 1 / v0)
rec("B1_noise_precision", 1 / s2)
rec("B1_post_precision", 1 / v0 + 1 / s2)
rec("B1_post_mean", m1)
rec("B1_post_var", v1)
rec("B1_post_sd", sqrt(v1))
rec("B1_weight_on_x", (1 / s2) / (1 / v0 + 1 / s2))
rec("B1_weight_on_prior", (1 / v0) / (1 / v0 + 1 / s2))

# brute-force check by quadrature of prior*likelihood
unnorm = lambda t: stats.norm(x0, sqrt(v0)).pdf(t) * stats.norm(t, sqrt(s2)).pdf(x1)
Z = integrate.quad(unnorm, -40, 40)[0]
mq = integrate.quad(lambda t: t * unnorm(t), -40, 40)[0] / Z
vq = integrate.quad(lambda t: (t - mq) ** 2 * unnorm(t), -40, 40)[0] / Z
rec("B1_Z_quad", Z)
rec("B1_post_mean_quad", mq)
rec("B1_post_var_quad", vq)
rec("B1_mean_err", abs(mq - m1))
rec("B1_var_err", abs(vq - v1))
# marginal f_X(x1) should equal N(x0, v0+s2) density at x1
rec("B1_fX_closed_form", stats.norm(x0, sqrt(v0 + s2)).pdf(x1))
rec("B1_fX_err", abs(Z - stats.norm(x0, sqrt(v0 + s2)).pdf(x1)))

# equal-variance, n observations:  m=(x0+sum xi)/(n+1), v=s2/(n+1)
rng = np.random.default_rng(20101116)
sig2 = 1.0
truth = 2.4
xs = list(np.round(rng.normal(truth, sqrt(sig2), 5), 6))
rec("B2_xs", xs)
mn, vn = normal_post(0.0, sig2, xs, [sig2] * 5)   # prior N(0, sigma^2): x0 acts as one more datum
rec("B2_prior_mean", 0.0)
rec("B2_prior_var", sig2)
rec("B2_post_mean", mn)
rec("B2_post_mean_formula", (0.0 + sum(xs)) / (5 + 1))
rec("B2_post_var", vn)
rec("B2_post_var_formula", sig2 / (5 + 1))
rec("B2_post_sd", sqrt(vn))
rec("B2_sample_mean", float(np.mean(xs)))
rec("B2_truth", truth)

# recursive update: first 4 then the 5th
ma, va = normal_post(0.0, sig2, xs[:4], [sig2] * 4)
mb, vb = normal_post(ma, va, xs[4:], [sig2])
rec("B2_after4_mean", ma)
rec("B2_after4_var", va)
rec("B2_recursive_mean", mb)
rec("B2_recursive_var", vb)
rec("B2_recursive_matches_batch", (abs(mb - mn) < 1e-12, abs(vb - vn) < 1e-12))

# sd shrink rate  ~ 1/sqrt(n)
rec("B2_sd_table", [{"n": q, "sd": sqrt(sig2 / (q + 1))} for q in (0, 1, 4, 9, 24, 99)])

# widget default readout
wm, wv = normal_post(0.0, 1.0, [1.5], [0.25])
rec("W_default_prior_mean", 0.0)
rec("W_default_prior_var", 1.0)
rec("W_default_noise_var", 0.25)
rec("W_default_x", 1.5)
rec("W_default_post_mean", wm)
rec("W_default_post_var", wv)
rec("W_default_post_sd", sqrt(wv))
rec("W_default_weight_on_x", (1 / 0.25) / (1 / 1.0 + 1 / 0.25))
rec("W_default_post_peak_density", stats.norm(wm, sqrt(wv)).pdf(wm))
# second widget checkpoint: vague prior
wm2, wv2 = normal_post(0.0, 100.0, [1.5], [0.25])
rec("W_vague_post_mean", wm2)
rec("W_vague_post_var", wv2)

# ===========================================================================
head("C. Multiparameter: quadratic trajectory in noise (L21 slide 3)")
# Z_t = T0 + t T1 + t^2 T2 ; X_t = Z_t + W_t, W_t ~ N(0, sw2) indep
# prior: Theta ~ N(0, sp2 I)
sp2, sw2, N = 4.0, 0.25, 5
A = np.array([[1.0, t, t * t] for t in range(1, N + 1)])
rec("C_design_matrix_A", A)
theta_true = np.array([1.0, 0.5, -0.05])
rng2 = np.random.default_rng(20101121)
xobs = A @ theta_true + rng2.normal(0, sqrt(sw2), N)
xobs = np.round(xobs, 4)
rec("C_theta_true", theta_true)
rec("C_x_obs", xobs)
Sigma = np.linalg.inv(A.T @ A / sw2 + np.eye(3) / sp2)
mu = Sigma @ (A.T @ xobs / sw2)
rec("C_post_cov", np.round(Sigma, 8))
rec("C_post_mean", mu)
rec("C_post_sd", np.sqrt(np.diag(Sigma)))
rec("C_post_corr_01", Sigma[0, 1] / sqrt(Sigma[0, 0] * Sigma[1, 1]))
rec("C_post_corr_02", Sigma[0, 2] / sqrt(Sigma[0, 0] * Sigma[2, 2]))
rec("C_post_corr_12", Sigma[1, 2] / sqrt(Sigma[1, 1] * Sigma[2, 2]))
# MAP = argmax of the quadratic form; check numerically
obj = lambda th: (np.sum((xobs - A @ th) ** 2) / (2 * sw2)
                  + np.sum(np.asarray(th) ** 2) / (2 * sp2))
res = optimize.minimize(obj, np.zeros(3), method="Nelder-Mead",
                        options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 20000})
rec("C_MAP_numeric", res.x)
rec("C_MAP_matches_mean_maxerr", float(np.max(np.abs(res.x - mu))))
# least squares (no prior) for comparison
ls = np.linalg.lstsq(A, xobs, rcond=None)[0]
rec("C_least_squares", ls)
rec("C_shrinkage_pct", list(100 * (1 - mu / ls)))

# ===========================================================================
head("D. Romeo and Juliet (rec22 P1 a-d; B&T Examples 8.2, 8.7)")
# prior Theta ~ U[0,1]; X|theta ~ U[0,theta]; posterior f(t|x)= 1/(t |ln x|), x<=t<=1
x = 0.5
rec("D_x", x)
rec("D_abs_log_x", abs(log(x)))
rj = lambda t, xx: 1.0 / (t * abs(log(xx))) if xx <= t <= 1 else 0.0
rec("D_post_integrates_to", integrate.quad(lambda t: rj(t, x), x, 1)[0])
rec("D_post_at_x", rj(x, x), "the maximum (density decreasing in theta)")
rec("D_post_at_1", rj(1.0, x))
rec("D_MAP", x)
rec("D_LMS_formula", (1 - x) / abs(log(x)))
rec("D_LMS_quad", integrate.quad(lambda t: t * rj(t, x), x, 1)[0])
rec("D_LMS_err", abs((1 - x) / abs(log(x))
                     - integrate.quad(lambda t: t * rj(t, x), x, 1)[0]))
rec("D_gap_LMS_minus_MAP", (1 - x) / abs(log(x)) - x)
# posterior variance / conditional MSEs are section 4's business, but record the mean table
tbl = []
for xx in (0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99):
    lms = (1 - xx) / abs(log(xx))
    tbl.append({"x": xx, "MAP": xx, "LMS": lms, "gap": lms - xx})
    print(f"   x={xx:5.2f}  MAP={xx:.6f}  E[Theta|X=x]={lms:.6f}  gap={lms-xx:.6f}")
rec("D_map_vs_lms_table", tbl)
rec("D_max_gap_x", float(optimize.minimize_scalar(
    lambda xx: -((1 - xx) / abs(log(xx)) - xx), bounds=(1e-6, 0.999999),
    method="bounded").x))
rec("D_max_gap_value", float(-optimize.minimize_scalar(
    lambda xx: -((1 - xx) / abs(log(xx)) - xx), bounds=(1e-6, 0.999999),
    method="bounded").fun))
rec("D_LMS_limit_x_to_0", (1 - 1e-12) / abs(log(1e-12)))
rec("D_LMS_limit_x_to_1", (1 - 0.999999) / abs(log(0.999999)))

# n dates: posterior c(xbar)/theta^n on [xbar,1], c = (n-1)/(xbar^{1-n}-1)
def rj_n(xbar, n):
    if n == 1:
        c = 1.0 / abs(log(xbar))
        mean = (1 - xbar) / abs(log(xbar))
    else:
        c = (n - 1) / (xbar ** (1 - n) - 1)
        if n == 2:
            mean = c * abs(log(xbar))
        else:
            mean = c * (xbar ** (2 - n) - 1) / (n - 2)
    return c, mean


for (xbar, nn) in ((0.5, 1), (0.5, 2), (0.5, 3), (0.5, 5), (0.5, 10), (0.8, 3)):
    c, mean = rj_n(xbar, nn)
    q = integrate.quad(lambda t: t * c / t**nn, xbar, 1)[0]
    z = integrate.quad(lambda t: c / t**nn, xbar, 1)[0]
    print(f"   xbar={xbar} n={nn:3d}  c={c:.6f}  norm={z:.10f}  mean={mean:.6f} (quad {q:.6f})")
    rec(f"D_n{nn}_xbar{xbar}", {"c": c, "norm_check": z, "mean": mean, "mean_quad": q})

rec("D_n3_half_c_frac", str(Fraction(2, 3)))

# ===========================================================================
head("E. When MAP and the posterior mean disagree badly (L21 slide 5)")
w1, mu1, sd1 = 0.45, 0.0, 0.30
w2, mu2, sd2 = 0.55, 4.0, 1.20
mix = lambda t: w1 * stats.norm(mu1, sd1).pdf(t) + w2 * stats.norm(mu2, sd2).pdf(t)
rec("E_mixture_spec", {"w1": w1, "mu1": mu1, "sd1": sd1, "w2": w2, "mu2": mu2, "sd2": sd2})
rec("E_norm_check", integrate.quad(mix, -10, 15)[0])
peak1 = float(optimize.minimize_scalar(lambda t: -mix(t), bounds=(-2, 2), method="bounded").x)
peak2 = float(optimize.minimize_scalar(lambda t: -mix(t), bounds=(2, 9), method="bounded").x)
rec("E_MAP", peak1)
rec("E_density_at_MAP", mix(peak1))
rec("E_local_peak2", peak2)
rec("E_density_at_peak2", mix(peak2))
emean = integrate.quad(lambda t: t * mix(t), -10, 15)[0]
rec("E_post_mean", emean)
rec("E_post_mean_formula", w1 * mu1 + w2 * mu2)
rec("E_density_at_mean", mix(emean))
rec("E_density_ratio_MAP_over_mean", mix(peak1) / mix(emean))
valley = float(optimize.minimize_scalar(mix, bounds=(0.5, 3.5), method="bounded").x)
rec("E_valley_location", valley)
rec("E_P_within_0p5_of_mean", integrate.quad(mix, emean - 0.5, emean + 0.5)[0])
rec("E_P_within_0p5_of_MAP", integrate.quad(mix, peak1 - 0.5, peak1 + 0.5)[0])

# ===========================================================================
head("F. Practice-question numbers")

# P3.2  light bulb: prior Lambda ~ U[1,2], X|lambda ~ Exp(lambda), observe x
xobs_p = 0.4
lam_post = lambda l: l * exp(-l * xobs_p)
Zp = integrate.quad(lam_post, 1, 2)[0]
rec("F_P32_x", xobs_p)
rec("F_P32_Z", Zp)
rec("F_P32_unconstrained_stationary_point", 1 / xobs_p)
rec("F_P32_MAP", 2.0, "boundary: 1/x=2.5 lies outside [1,2] and l e^{-lx} increases on [1,2]")
rec("F_P32_post_at_1", lam_post(1) / Zp)
rec("F_P32_post_at_2", lam_post(2) / Zp)
rec("F_P32_post_mean", integrate.quad(lambda l: l * lam_post(l), 1, 2)[0] / Zp)

# P3.3  normal-normal
m33, v33 = normal_post(70.0, 25.0, [76.0], [9.0])
rec("F_P33_post_mean", m33)
rec("F_P33_post_var", v33)
rec("F_P33_post_sd", sqrt(v33))
rec("F_P33_prior_precision", 1 / 25)
rec("F_P33_noise_precision", 1 / 9)
rec("F_P33_post_precision", 1 / 25 + 1 / 9)
rec("F_P33_weight_on_x", (1 / 9) / (1 / 25 + 1 / 9))
# second reading 68 with same noise variance
m33b, v33b = normal_post(m33, v33, [68.0], [9.0])
rec("F_P33b_post_mean", m33b)
rec("F_P33b_post_var", v33b)
rec("F_P33b_post_sd", sqrt(v33b))
m33c, v33c = normal_post(70.0, 25.0, [76.0, 68.0], [9.0, 9.0])
rec("F_P33b_batch_check", (abs(m33c - m33b) < 1e-12, abs(v33c - v33b) < 1e-12))

# P3.4  discrete hypothesis testing (two hypotheses, continuous observation)
pri = {1: 0.3, 2: 0.7}          # 1 = defective, 2 = good
lik = {1: stats.norm(1.0, 1.0), 2: stats.norm(0.0, 1.0)}
xh = 1.2
num = {m: pri[m] * lik[m].pdf(xh) for m in (1, 2)}
den = sum(num.values())
rec("F_P34_x", xh)
rec("F_P34_numerators", {str(m): num[m] for m in num})
rec("F_P34_fX", den)
rec("F_P34_posteriors", {str(m): num[m] / den for m in num})
rec("F_P34_MAP_hypothesis", 1 if num[1] > num[2] else 2)
rec("F_P34_error_prob_at_x", min(num[1], num[2]) / den)
# threshold where the decision flips
thr = float(optimize.brentq(lambda t: pri[1] * lik[1].pdf(t) - pri[2] * lik[2].pdf(t), -5, 6))
rec("F_P34_threshold", thr)
rec("F_P34_threshold_formula", 0.5 + log(pri[2] / pri[1]))
rec("F_P34_overall_error",
    pri[1] * lik[1].cdf(thr) + pri[2] * lik[2].sf(thr))

# P3.5  Romeo-Juliet numeric practice: xbar = 0.4, n = 4
c45, m45 = rj_n(0.4, 4)
rec("F_P35_c", c45)
rec("F_P35_MAP", 0.4)
rec("F_P35_mean", m45)
rec("F_P35_mean_quad", integrate.quad(lambda t: t * c45 / t**4, 0.4, 1)[0])
rec("F_P35_P_theta_gt_half", integrate.quad(lambda t: c45 / t**4, 0.5, 1)[0])

# Practice 3.2 (gamma posterior): f(theta) = c theta^5 e^{-4 theta} on theta > 0.
# Recognizing Gamma(alpha=6, rate=4) gives c = 4^6/Gamma(6) = 4096/120; the quadrature
# below is the independent check that the fragment cites.
alpha_g, lam_g = 6, 4
gam_int_quad = integrate.quad(lambda t: t**5 * exp(-lam_g * t), 0, np.inf)[0]
gam_int_exact = factorial(alpha_g - 1) / lam_g**alpha_g
rec("F_gamma_alpha", alpha_g)
rec("F_gamma_rate", lam_g)
rec("F_gamma_integral_exact", gam_int_exact, "= 5!/4^6")
rec("F_gamma_integral_quad", gam_int_quad)
rec("F_gamma_integral_err", abs(gam_int_exact - gam_int_quad))
c_gam = lam_g**alpha_g / factorial(alpha_g - 1)
rec("F_gamma_c", c_gam, "= 4^6/120 = 1/integral")
rec("F_gamma_c_from_quad", 1.0 / gam_int_quad)
rec("F_gamma_mean", alpha_g / lam_g)
rec("F_gamma_mean_quad",
    integrate.quad(lambda t: t * c_gam * t**5 * exp(-lam_g * t), 0, np.inf)[0])
rec("F_gamma_sd", sqrt(alpha_g) / lam_g)
rec("F_gamma_sd_quad", sqrt(
    integrate.quad(lambda t: (t - alpha_g / lam_g) ** 2 * c_gam * t**5
                   * exp(-lam_g * t), 0, np.inf)[0]))
rec("F_gamma_norm_check",
    integrate.quad(lambda t: c_gam * t**5 * exp(-lam_g * t), 0, np.inf)[0])

# P3.1 numbers: none (conceptual)

# ===========================================================================
head("G. Figure-support values")
rec("G_fig33_curves", [{"n": d["n"], "k": d["k"]} for d in narrow])
rec("G_fig34_prior", {"mean": 0.0, "var": 1.0})
rec("G_fig34_obs", 1.5)
rec("G_fig34_noise_var", 0.25)
rec("G_fig34_post", {"mean": wm, "var": wv})

# ===========================================================================
head("H. MAP is not invariant under reparametrization (gotcha)")
# posterior of Theta is Beta(8,4) from section A (n=10, k=7 heads, uniform prior)
# theta-scale MAP = 7/10.  Reparametrize phi = g(theta); the density picks up |dtheta/dphi|.
rec("H_theta_MAP", k / n)
# (i) logit scale phi = log(theta/(1-theta)):  f_phi(phi) = f_theta(theta) * theta(1-theta)
g_logit = lambda t: (k + 1) * log(t) + (n - k + 1) * log(1 - t)
t_logit = float(optimize.minimize_scalar(lambda t: -g_logit(t),
                                         bounds=(1e-9, 1 - 1e-9), method="bounded").x)
rec("H_logit_MAP_back_in_theta", t_logit)
rec("H_logit_MAP_exact_(k+1)/(n+2)", (k + 1) / (n + 2))
# (ii) square scale phi = theta^2:  f_phi(phi) = f_theta(sqrt(phi)) / (2 sqrt(phi))
#      propto theta^{k-1}(1-theta)^{n-k}
g_sq = lambda t: (k - 1) * log(t) + (n - k) * log(1 - t)
t_sq = float(optimize.minimize_scalar(lambda t: -g_sq(t),
                                      bounds=(1e-9, 1 - 1e-9), method="bounded").x)
rec("H_square_MAP_back_in_theta", t_sq)
rec("H_square_MAP_exact_(k-1)/(n-1)", (k - 1) / (n - 1))
# (iii) reciprocal scale phi = 1/theta: f_phi = f_theta(1/phi)/phi^2
#      propto theta^{k+2}(1-theta)^{n-k}
g_rec = lambda t: (k + 2) * log(t) + (n - k) * log(1 - t)
t_rec = float(optimize.minimize_scalar(lambda t: -g_rec(t),
                                       bounds=(1e-9, 1 - 1e-9), method="bounded").x)
rec("H_recip_MAP_back_in_theta", t_rec)
rec("H_recip_MAP_exact_(k+2)/(n+2)", (k + 2) / (n + 2))
rec("H_MAPs_differ", sorted({round(k / n, 6), round(t_logit, 6),
                             round(t_sq, 6), round(t_rec, 6)}))
# the posterior MEAN is invariant in the sense that E[g(Theta)|x] is unambiguous:
rec("H_post_mean_theta", (k + 1) / (n + 2))
rec("H_post_mean_theta_sq",
    integrate.quad(lambda t: t * t * dens(t), 0, 1)[0])
rec("H_post_mean_theta_sq_formula",
    ((k + 1) * (k + 2)) / ((n + 2) * (n + 3)))

with open(ROOT / "g6_s3.json", "w", encoding="utf-8") as f:
    json.dump(OUT, f, indent=1, default=float)
print(f"\nwrote {ROOT / 'g6_s3.json'}  ({len(OUT)} keys)")
