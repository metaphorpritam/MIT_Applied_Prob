# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy"]
# ///
"""Recomputes every number in notes/src/fragments/qb_s6.html (Q115-Q134).

Section 6 of the question bank: limit theorems (Markov, Chebyshev, WLLN, CLT)
and Bayesian inference (posteriors, MAP, LMS / linear LMS).

Run:  uv run computes/qb_s6.py
"""

import json
import math
import sys
from fractions import Fraction

import numpy as np
from scipy import stats
from scipy.special import gammaln

sys.stdout.reconfigure(encoding="utf-8")

R = {}          # results dict, dumped to JSON
rng = np.random.default_rng(20250614)


def rec(key, val, label=""):
    R[key] = val
    print(f"{key:38s} = {val!r}   {label}")
    return val


def hdr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


PHI = stats.norm.cdf

# ---------------------------------------------------------------- Q115
hdr("Q115 - Markov vs Chebyshev on downtime: mu=6, var=9, a=15")
mu, var = 6.0, 9.0
a = 15.0
rec("q115_markov", mu / a)
rec("q115_dev", a - mu, "the deviation |X-mu| >= 30-? ; here a-mu")
rec("q115_cheb", var / (a - mu) ** 2)
rec("q115_ratio", (mu / a) / (var / (a - mu) ** 2))
rec("q115_sigma", math.sqrt(var))
rec("q115_ksigma", (a - mu) / math.sqrt(var), "deviation in sigma units")

# ---------------------------------------------------------------- Q116
hdr("Q116 - does Chebyshev always beat Markov?  same X, threshold a=7")
a2 = 7.0
rec("q116_markov", mu / a2)
rec("q116_cheb", var / (a2 - mu) ** 2, "vacuous, > 1")
# crossover: mu/a = var/(a-mu)^2  ->  mu(a-mu)^2 = var*a
# 6(a-6)^2 = 9a  ->  6a^2 - 81a + 216 = 0
coef = [6.0, -81.0, 216.0]
roots = np.roots(coef)
rec("q116_roots", sorted(float(r) for r in roots))
a_star = max(float(r) for r in roots)
rec("q116_crossover", a_star, "Chebyshev is the tighter of the two only for a above this")
rec("q116_check_markov_at_star", mu / a_star)
rec("q116_check_cheb_at_star", var / (a_star - mu) ** 2)
rec("q116_markov_at_10", mu / 10.0)
rec("q116_cheb_at_10", var / (10.0 - mu) ** 2)

# ---------------------------------------------------------------- Q117
hdr("Q117 - how loose are the bounds?  X ~ Poisson(4), P(X >= 10)")
lam = 4.0
rec("q117_markov", lam / 10.0)
rec("q117_cheb", lam / (10.0 - lam) ** 2)
p_exact = float(stats.poisson.sf(9, lam))       # P(X >= 10) = 1 - F(9)
rec("q117_exact", p_exact)
rec("q117_markov_over_exact", (lam / 10.0) / p_exact)
rec("q117_cheb_over_exact", (lam / 36.0) / p_exact)
# Monte-Carlo cross-check of the exact tail
mc = rng.poisson(lam, 4_000_000)
rec("q117_exact_mc", float(np.mean(mc >= 10)))
# far tail: a = 20
rec("q117_markov_20", lam / 20.0)
rec("q117_cheb_20", lam / (20.0 - lam) ** 2)
rec("q117_exact_20", float(stats.poisson.sf(19, lam)))
rec("q117_cheb_over_exact_20", (lam / 256.0) / float(stats.poisson.sf(19, lam)))
rec("q117_markov_over_exact_20", (lam / 20.0) / float(stats.poisson.sf(19, lam)))
# --- how tight are the two bounds over the class {mean 4, var 4, X >= 0}? ---
# The sharp value for P(X >= 10) is the one-sided (Cantelli) bound s2/(s2+c^2).
rec("q117_sharp_onesided", lam / (lam + (10.0 - lam) ** 2), "= 4/40, the attainable value")
# Cantelli's extremal two-point law: mass p at 10, mass 1-p at mu - s2/c = 4 - 4/6.
p_hi = lam / (lam + (10.0 - lam) ** 2)
x_lo = 10.0 / 3.0
rec("q117_extremal_mass_hi", p_hi)
rec("q117_extremal_atom_lo", x_lo, "the other support point, = 10/3")
rec("q117_extremal_mean", p_hi * 10.0 + (1 - p_hi) * x_lo)
rec("q117_extremal_var",
    p_hi * (10.0 - lam) ** 2 + (1 - p_hi) * (x_lo - lam) ** 2)
# Markov's extremal law (mass 0.4 at 10, 0.6 at 0) has the right mean but the wrong variance.
rec("q117_markov_extremal_var", 0.4 * (10.0 - lam) ** 2 + 0.6 * (0.0 - lam) ** 2,
    "= 24, not 4 -- so Markov's 0.4 is unattainable in this class")

# ---------------------------------------------------------------- Q118
hdr("Q118 - one-sided Chebyshev (Cantelli): P(X-mu >= c) <= s2/(s2+c^2)")
s2, c = 4.0, 6.0
t_opt = s2 / c
rec("q118_t_opt", t_opt, "optimal shift t = sigma^2/c")
one_sided = s2 / (s2 + c * c)
rec("q118_one_sided", one_sided)
rec("q118_two_sided", s2 / c ** 2)
rec("q118_improvement", (s2 / c ** 2) / one_sided)
rec("q118_exact_poisson", p_exact, "same event as Q117, X~Poisson(4)")
rec("q118_one_sided_over_exact", one_sided / p_exact)
# generic-t bound value, to show t_opt really is the minimizer
ts = np.linspace(0.01, 20, 200001)
gen = (s2 + ts ** 2) / (c + ts) ** 2
rec("q118_min_over_t_numeric", float(gen.min()))
rec("q118_argmin_numeric", float(ts[int(gen.argmin())]))

# ---------------------------------------------------------------- Q119
hdr("Q119 - sample size: Chebyshev vs CLT.  sigma^2=0.09, eps=0.05, delta=0.02")
sig2, eps, delta = 0.09, 0.05, 0.02
sig = math.sqrt(sig2)
rec("q119_sigma", sig)
n_cheb = sig2 / (eps ** 2 * delta)
rec("q119_n_cheb_raw", n_cheb)
rec("q119_n_cheb", int(math.ceil(n_cheb)))
z = float(stats.norm.ppf(1 - delta / 2))
rec("q119_z", z, "z_{0.99}")
n_clt_raw = (z * sig / eps) ** 2
rec("q119_sqrt_n_clt", z * sig / eps)
rec("q119_n_clt_raw", n_clt_raw)
n_clt = int(math.ceil(n_clt_raw))
rec("q119_n_clt", n_clt)
rec("q119_ratio", n_cheb / n_clt)
rec("q119_cheb_bound_at_n_clt", sig2 / (n_clt * eps ** 2))
rec("q119_clt_prob_at_n_cheb", 2 * (1 - PHI(eps * math.sqrt(n_cheb) / sig)))
rec("q119_z_at_n_cheb", eps * math.sqrt(n_cheb) / sig)

# ---------------------------------------------------------------- Q120
hdr("Q120 - WLLN misreading: relative vs absolute deviation, fair coin")
for n in (100, 10_000, 1_000_000):
    sd = 0.5 * math.sqrt(n)
    rec(f"q120_sd_S_{n}", sd)
    rec(f"q120_mean_abs_dev_approx_{n}", sd * math.sqrt(2 / math.pi))
for n in (100, 10_000):
    k = np.arange(0, n + 1)
    pmf = stats.binom.pmf(k, n, 0.5)
    rec(f"q120_mean_abs_dev_exact_{n}", float(np.sum(np.abs(k - n / 2) * pmf)))
n = 10_000
rec("q120_P_dev_ge_100_exact",
    float(stats.binom.cdf(4900, n, 0.5) + stats.binom.sf(5099, n, 0.5)))
rec("q120_P_dev_ge_100_clt", 2 * (1 - PHI(100 / (0.5 * math.sqrt(n)))))
rec("q120_P_Mn_within_eps", 1 - float(stats.binom.cdf(4900, n, 0.5)
                                      + stats.binom.sf(5099, n, 0.5)))
rec("q120_P_S_equals_5000", float(stats.binom.pmf(5000, n, 0.5)))
mc = rng.binomial(n, 0.5, 2_000_000)
rec("q120_mean_abs_dev_mc", float(np.mean(np.abs(mc - n / 2))))
rec("q120_sqrt_2_over_pi", math.sqrt(2 / math.pi))
rec("q120_growth_ratio", 39.89323069691078 / 3.9794618693589356, "n x100 -> gap x10")

# ---------------------------------------------------------------- Q121
hdr("Q121 - which tool for a guarantee at n=30?  sigma^2=0.25, eps=0.2")
rec("q121_cheb_bound", 0.25 / (30 * 0.2 ** 2))
rec("q121_clt_number", 2 * (1 - PHI(0.2 * math.sqrt(30) / 0.5)))
rec("q121_clt_z", 0.2 * math.sqrt(30) / 0.5)
rec("q121_n_for_cheb_005", 0.25 / (0.2 ** 2 * 0.05))

# ---------------------------------------------------------------- Q122
hdr("Q122 - M_n^2 -> mu^2 in probability.  X~U[0,2], mu=1, sigma^2=1/3")
mu2, s2u = 1.0, 1.0 / 3.0
epsq = 0.1
d = math.sqrt(1 + epsq) - 1          # delta(2mu+delta) = eps with mu=1
rec("q122_delta", d)
rec("q122_delta_check", d * (2 * mu2 + d), "must equal eps = 0.1")
n122 = 10_000
rec("q122_bound_coeff", s2u / d ** 2, "bound = coeff / n")
rec("q122_bound_at_n", s2u / (n122 * d ** 2))
sd_M = math.sqrt(s2u / n122)
rec("q122_sd_Mn", sd_M)
z_up = (math.sqrt(1 + epsq) - 1) / sd_M
z_dn = (1 - math.sqrt(1 - epsq)) / sd_M
rec("q122_z_up", z_up)
rec("q122_z_dn", z_dn)
true_p = float(stats.norm.sf(z_up) + stats.norm.cdf(-z_dn))
rec("q122_true_prob_clt", true_p)
rec("q122_bound_over_truth", (s2u / (n122 * d ** 2)) / true_p)
mcM = rng.uniform(0, 2, size=(200_000, 100)).mean(axis=1)   # n=100 pilot
rec("q122_mc_n100_prob", float(np.mean(np.abs(mcM ** 2 - 1) >= epsq)))
rec("q122_bound_at_100", s2u / (100 * d ** 2))
mcM4 = rng.uniform(0, 2, size=(4_000, 10_000)).mean(axis=1)
rec("q122_mc_n10000_hits", int(np.sum(np.abs(mcM4 ** 2 - 1) >= epsq)))

# ------------------------------------------------- Q122(c): the L19 counterexample
hdr("Q122(c) - Y_n = 0 w.p. 1-1/n, = n w.p. 1/n:  Y_n -> 0 in probability, E[Y_n] = 1")
rng_yn = np.random.default_rng(11223344)          # own stream: leaves the main rng untouched
for nyn in (100, 10_000):
    rec(f"q122c_E_Y_{nyn}", nyn * (1.0 / nyn), "n * (1/n) = 1 for every n")
    rec(f"q122c_E_Y2_{nyn}", float(nyn ** 2 * (1.0 / nyn)), "n^2 * (1/n) = n")
    rec(f"q122c_var_Y_{nyn}", float(nyn ** 2 * (1.0 / nyn) - 1.0), "= n - 1")
    rec(f"q122c_sd_Y_{nyn}", math.sqrt(nyn - 1.0))
    rec(f"q122c_P_dev_{nyn}", 1.0 / nyn, "P(|Y_n - 0| >= eps) = 1/n for any 0 < eps <= n")
    draws = rng_yn.random(4_000_000) < (1.0 / nyn)
    rec(f"q122c_E_Y_mc_{nyn}", float(np.mean(draws * nyn)))
rec("q122c_P_dev_at_1e6", 1.0 / 1_000_000, "still exactly 1/n; E[Y_n] still 1")
rec("q122c_E_limit", 0.0, "E of the limit r.v. Y = 0")
rec("q122c_limit_of_E", 1.0, "lim E[Y_n] = 1  !=  E[lim Y_n] = 0")

# ---------------------------------------------------------------- Q123
hdr("Q123 - plain CLT: 200 service times, mean 3, sd 2; P(total > 620)")
n123, m123, sd123 = 200, 3.0, 2.0
rec("q123_mean", n123 * m123)
rec("q123_sd", sd123 * math.sqrt(n123))
z123 = (620 - n123 * m123) / (sd123 * math.sqrt(n123))
rec("q123_z", z123)
rec("q123_prob", float(stats.norm.sf(z123)))
rec("q123_Phi_z", float(PHI(z123)))
rec("q123_prob_600", float(stats.norm.sf(0.0)), "sanity: P(total>600)=1/2")

# ---------------------------------------------------------------- Q124
hdr("Q124 - de Moivre-Laplace, n=100, p=0.4")
n124, p124 = 100, 0.4
m124, s124 = n124 * p124, math.sqrt(n124 * p124 * (1 - p124))
rec("q124_mean", m124)
rec("q124_sd", s124)
rec("q124_exact_pmf_45", float(stats.binom.pmf(45, n124, p124)))
zl = (45.5 - m124) / s124
zk = (44.5 - m124) / s124
rec("q124_z_hi", zl)
rec("q124_z_lo", zk)
rec("q124_approx_pmf_45", float(PHI(zl) - PHI(zk)))
rec("q124_pmf_relerr", abs(float(PHI(zl) - PHI(zk)) - float(stats.binom.pmf(45, n124, p124)))
    / float(stats.binom.pmf(45, n124, p124)))
rec("q124_exact_35_45", float(stats.binom.cdf(45, n124, p124) - stats.binom.cdf(34, n124, p124)))
rec("q124_z_45p5", (45.5 - m124) / s124)
rec("q124_z_34p5", (34.5 - m124) / s124)
rec("q124_approx_35_45_corr", float(PHI((45.5 - m124) / s124) - PHI((34.5 - m124) / s124)))
rec("q124_approx_35_45_nocorr", float(PHI((45 - m124) / s124) - PHI((35 - m124) / s124)))
rec("q124_err_corr", abs(float(PHI((45.5 - m124) / s124) - PHI((34.5 - m124) / s124))
                         - float(stats.binom.cdf(45, n124, p124) - stats.binom.cdf(34, n124, p124))))
rec("q124_err_nocorr", abs(float(PHI((45 - m124) / s124) - PHI((35 - m124) / s124))
                           - float(stats.binom.cdf(45, n124, p124) - stats.binom.cdf(34, n124, p124))))
rec("q124_z_uncorr", (45 - m124) / s124)
rec("q124_err_ratio", 0.04600718439664486 / 0.00014525448319890888)
rec("q124_half_bars", 0.5 * (float(stats.binom.pmf(35, n124, p124))
                             + float(stats.binom.pmf(45, n124, p124))),
    "half the two end bars ~ the uncorrected error")
# The local (de Moivre-Laplace) form phi(z)/sigma is an equally valid route to P(S=45).
rec("q124_local_phi", float(stats.norm.pdf((45 - m124) / s124)))
rec("q124_local_limit", float(stats.norm.pdf((45 - m124) / s124)) / s124,
    "phi(z)/sigma_S -- the local limit approximation to p_S(45)")
rec("q124_wrong_shift_34p5_44p5",
    float(PHI((44.5 - m124) / s124) - PHI((34.5 - m124) / s124)),
    "the both-endpoints-shifted trap: drops the bar at 45")
rec("q124_local_relerr",
    abs(float(stats.norm.pdf((45 - m124) / s124)) / s124
        - float(stats.binom.pmf(45, n124, p124))) / float(stats.binom.pmf(45, n124, p124)))

# ---------------------------------------------------------------- Q125
hdr("Q125 - where the normal approximation is poor: n=200, p=0.01, P(S>=6)")
n125, p125 = 200, 0.01
m125 = n125 * p125
s125 = math.sqrt(n125 * p125 * (1 - p125))
rec("q125_mean", m125)
rec("q125_sd", s125)
rec("q125_exact", float(stats.binom.sf(5, n125, p125)))
z125 = (5.5 - m125) / s125
rec("q125_z_corr", z125)
rec("q125_normal_corr", float(stats.norm.sf(z125)))
rec("q125_normal_nocorr", float(stats.norm.sf((6 - m125) / s125)))
rec("q125_poisson", float(stats.poisson.sf(5, m125)))
rec("q125_exact_over_normal", float(stats.binom.sf(5, n125, p125)) / float(stats.norm.sf(z125)))
rec("q125_poisson_relerr", abs(float(stats.poisson.sf(5, m125)) - float(stats.binom.sf(5, n125, p125)))
    / float(stats.binom.sf(5, n125, p125)))
rec("q125_np", n125 * p125)
rec("q125_n_for_np_ge_5", 5 / p125, "rule of thumb np>=5 needs this many trials")
mc = rng.binomial(n125, p125, 4_000_000)
rec("q125_exact_mc", float(np.mean(mc >= 6)))
rec("q125_z_nocorr", (6 - m125) / s125)
rec("q125_skewness", (1 - 2 * p125) / s125)

# ---------------------------------------------------------------- Q126
hdr("Q126 - spot the error: sum of 50 Exp(1), P(S >= 65)")
n126 = 50
rec("q126_mean", 50.0)
rec("q126_sd_sum", math.sqrt(50.0))
z126 = (65 - 50) / math.sqrt(50.0)
rec("q126_z_correct", z126)
rec("q126_clt_correct", float(stats.norm.sf(z126)))
z_wrong = (65 - 50) / (1 / math.sqrt(50.0))
rec("q126_z_wrong", z_wrong, "student divided by sigma/sqrt(n)")
rec("q126_clt_wrong", float(stats.norm.sf(z_wrong)))
rec("q126_exact_gamma", float(stats.gamma.sf(65, a=n126, scale=1.0)))
rec("q126_clt_over_exact", float(stats.norm.sf(z126)) / float(stats.gamma.sf(65, a=n126, scale=1.0)))
mc = rng.gamma(shape=n126, scale=1.0, size=4_000_000)
rec("q126_exact_mc", float(np.mean(mc >= 65)))
rec("q126_bogus_halfcorr", float(stats.norm.sf((64.5 - 50) / math.sqrt(50.0))),
    "illegitimate 1/2 correction on a continuous sum")
rec("q126_skew_sum", 2.0 / math.sqrt(n126))

# ---------------------------------------------------------------- Q127
hdr("Q127 - capacity design, 50 Exp(mean 5) loads, 1% overflow")
n127, mean127 = 50, 5.0
mu127 = n127 * mean127
sd127 = mean127 * math.sqrt(n127)
rec("q127_mean", mu127)
rec("q127_sd", sd127)
z127 = float(stats.norm.ppf(0.99))
rec("q127_z99", z127)
C = mu127 + z127 * sd127
rec("q127_C_clt", C)
rec("q127_true_overflow_at_C", float(stats.gamma.sf(C, a=n127, scale=mean127)))
C_exact = float(stats.gamma.ppf(0.99, a=n127, scale=mean127))
rec("q127_C_exact", C_exact)
rec("q127_C_shortfall", C_exact - C)
rec("q127_overflow_ratio", float(stats.gamma.sf(C, a=n127, scale=mean127)) / 0.01)
rec("q127_skew_summand", 2.0, "skewness of an exponential")
rec("q127_skew_sum", 2.0 / math.sqrt(n127))
mc = rng.gamma(shape=n127, scale=mean127, size=4_000_000)
rec("q127_overflow_mc", float(np.mean(mc > C)))
rec("q127_margin_term", z127 * sd127)
rec("q127_shortfall_pct", 100 * (C_exact - C) / C)

# ---------------------------------------------------------------- Q128
hdr("Q128 - discrete Bayesian posterior: Theta in {1,2,3}, X~Poisson(Theta), x=4")
thetas = np.array([1.0, 2.0, 3.0])
prior = np.array([0.5, 0.3, 0.2])
x128 = 4
lik = np.exp(-thetas) * thetas ** x128 / math.factorial(x128)
rec("q128_lik", [float(v) for v in lik])
unnorm = prior * lik
rec("q128_unnorm", [float(v) for v in unnorm])
rec("q128_pX", float(unnorm.sum()))
post = unnorm / unnorm.sum()
rec("q128_posterior", [float(v) for v in post])
rec("q128_map", float(thetas[int(post.argmax())]))
rec("q128_post_mean", float((thetas * post).sum()))
rec("q128_prior_mean", float((thetas * prior).sum()))
rec("q128_post_var", float((thetas ** 2 * post).sum() - ((thetas * post).sum()) ** 2))
rec("q128_perr_map", float(1 - post.max()))
rec("q128_perr_prior_map", float(1 - post[int(prior.argmax())]),
    "error prob if you ignored the data and said Theta=1")

# ---------------------------------------------------------------- Q129
hdr("Q129 - conjugate coin bias: Beta(2,2) prior, 7 heads in 10")
a0, b0, k, n129 = 2, 2, 7, 10
a1, b1 = a0 + k, b0 + n129 - k
rec("q129_post_a", a1)
rec("q129_post_b", b1)
rec("q129_norm_const",
    float(math.exp(gammaln(a1 + b1) - gammaln(a1) - gammaln(b1))), "1/B(9,5)")
rec("q129_prior_mean", a0 / (a0 + b0))
rec("q129_post_mean", a1 / (a1 + b1))
rec("q129_post_map", (a1 - 1) / (a1 + b1 - 2))
rec("q129_mle", k / n129)
rec("q129_post_var", a1 * b1 / ((a1 + b1) ** 2 * (a1 + b1 + 1)))
rec("q129_prior_var", a0 * b0 / ((a0 + b0) ** 2 * (a0 + b0 + 1)))
rec("q129_post_sd", math.sqrt(a1 * b1 / ((a1 + b1) ** 2 * (a1 + b1 + 1))))
rec("q129_post_mean_frac", str(Fraction(a1, a1 + b1)))
rec("q129_shrinkage_weight", (a0 + b0) / (a0 + b0 + n129),
    "posterior mean = w*prior_mean + (1-w)*MLE")
rec("q129_shrink_check", ((a0 + b0) / (a0 + b0 + n129)) * (a0 / (a0 + b0))
    + (n129 / (a0 + b0 + n129)) * (k / n129))
rec("q129_P_theta_gt_half", float(stats.beta.sf(0.5, a1, b1)))
mc = rng.beta(a1, b1, 4_000_000)
rec("q129_post_mean_mc", float(mc.mean()))
rec("q129_odds_head_biased", float(stats.beta.sf(0.5, a1, b1)) / float(stats.beta.cdf(0.5, a1, b1)))
rec("q129_prior_weight", (a0 + b0) / (a0 + b0 + n129))
rec("q129_data_weight", n129 / (a0 + b0 + n129))
rec("q129_binom_coeff", math.comb(n129, k))
# Beta-to-binomial identity: P(Beta(a,b) > 1/2) = P(Bin(a+b-1, 1/2) <= a-1).
n_id = a1 + b1 - 1
rec("q129_identity_n", n_id, "a+b-1 = 13")
rec("q129_identity_num", sum(math.comb(n_id, j) for j in range(a1)), "sum_{j=0}^{8} C(13,j)")
rec("q129_identity_den", 2 ** n_id)
rec("q129_identity_value",
    sum(math.comb(n_id, j) for j in range(a1)) / 2 ** n_id,
    "must equal q129_P_theta_gt_half")

# ---------------------------------------------------------------- Q130
hdr("Q130 - MAP vs conditional mean: posterior 4*theta*exp(-2theta)")
rec("q130_norm_integral", 1 / 4.0, "int theta e^{-2theta} dtheta = 1/4")
rec("q130_const", 4.0)
rec("q130_map", 0.5)
rec("q130_mean", 1.0)
rec("q130_var", 0.5)
rec("q130_median", float(stats.gamma.ppf(0.5, a=2, scale=0.5)))
rec("q130_mse_at_mean", 0.5)
rec("q130_mse_at_map", 0.5 + (1.0 - 0.5) ** 2)
rec("q130_mse_ratio", (0.5 + 0.25) / 0.5)
rec("q130_mse_at_median", 0.5 + (1.0 - float(stats.gamma.ppf(0.5, a=2, scale=0.5))) ** 2)
rec("q130_perr_check", 0.0, "P(hatTheta = Theta) = 0 for continuous Theta")
mc = rng.gamma(shape=2, scale=0.5, size=4_000_000)
rec("q130_mean_mc", float(mc.mean()))
rec("q130_mse_at_map_mc", float(np.mean((mc - 0.5) ** 2)))

# ---------------------------------------------------------------- Q131
hdr("Q131 - MAP is not reparametrization-invariant: Phi = 1/Theta")
# f_Phi(phi) = f_Theta(1/phi)/phi^2 = 4 phi^{-3} e^{-2/phi}
phis = np.linspace(1e-4, 20, 4_000_001)
dens = 4 * phis ** (-3) * np.exp(-2 / phis)
rec("q131_map_phi_numeric", float(phis[int(dens.argmax())]))
rec("q131_map_phi_exact", 2.0 / 3.0)
rec("q131_reciprocal_of_map_theta", 1 / 0.5)
rec("q131_E_phi", 2.0, "E[1/Theta] = 4*int e^{-2theta} dtheta = 2")
rec("q131_one_over_E_theta", 1 / 1.0)
rec("q131_density_check_integral", float(np.trapezoid(dens, phis)))
mc = rng.gamma(shape=2, scale=0.5, size=4_000_000)
rec("q131_E_phi_mc", float(np.mean(1 / mc)))
rec("q131_ratio_map", (2.0 / 3.0) / (1 / 0.5))

# ---------------------------------------------------------------- Q132
hdr("Q132 - no data: the baseline estimate and its MSE")
rec("q132_estimate", 8.0)
rec("q132_mse", 5.0)
rec("q132_mse_at_9", 5.0 + (9.0 - 8.0) ** 2)
rec("q132_penalty", (5.0 + 1.0) / 5.0)
rec("q132_mse_at_c_general", "var + (c - mean)^2")
rec("q132_best_c", 8.0)

# ---------------------------------------------------------------- Q133
hdr("Q133 - linear LMS with a scaled observation X = 2*Theta + W")
vT, mT = 8.0, 70.0
vW, cscale = 2.0, 2.0
mX = cscale * mT
vX = cscale ** 2 * vT + vW
cov = cscale * vT
rec("q133_EX", mX)
rec("q133_varX", vX)
rec("q133_cov", cov)
aa = cov / vX
bb = mT - aa * mX
rec("q133_a", aa)
rec("q133_b", bb)
rho2 = cov ** 2 / (vX * vT)
rec("q133_rho2", rho2)
rec("q133_rho", math.sqrt(rho2))
rec("q133_mse", (1 - rho2) * vT)
rec("q133_mse_closed_form", vT * vW / (cscale ** 2 * vT + vW))
rec("q133_baseline_mse", vT)
rec("q133_variance_removed_pct", 100 * rho2)
rec("q133_estimate_at_x_150", aa * 150 + bb)
rec("q133_wrong_a_forget_scale", vT / vX, "the trap: cov taken as var(Theta)")
rec("q133_wrong_estimate_at_x_150", (vT / vX) * 150 + (mT - (vT / vX) * mX))
# Monte-Carlo: least squares fit
T = rng.normal(mT, math.sqrt(vT), 4_000_000)
W = rng.normal(0, math.sqrt(vW), 4_000_000)
X = cscale * T + W
A = np.vstack([X, np.ones_like(X)]).T
sol, *_ = np.linalg.lstsq(A, T, rcond=None)
rec("q133_a_mc", float(sol[0]))
rec("q133_b_mc", float(sol[1]))
rec("q133_mse_mc", float(np.mean((T - (sol[0] * X + sol[1])) ** 2)))

# ---------------------------------------------------------------- Q134
hdr("Q134 - orthogonality does not mean independence: Theta|X ~ U[-|X|,|X|]")
rec("q134_E_theta_given_x", 0.0)
rec("q134_var_theta", 1 / 9)
rec("q134_mse_lms", 1 / 9)
rec("q134_var_hat", 0.0, "hatTheta is identically 0")
rec("q134_cond_var_at_0p9", 0.9 ** 2 / 3)
rec("q134_cond_var_at_0p1", 0.1 ** 2 / 3)
rec("q134_cond_var_ratio", (0.9 ** 2 / 3) / (0.1 ** 2 / 3))
rec("q134_E_err2_X2", (1 / 5) / 3, "E[Theta^2 X^2] = E[X^4]/3 = (1/5)/3")
rec("q134_E_err2_times_E_X2", (1 / 9) * (1 / 3))
rec("q134_dependence_gap", (1 / 5) / 3 - (1 / 9) * (1 / 3))
Xs = rng.uniform(-1, 1, 4_000_000)
Th = rng.uniform(-1, 1, 4_000_000) * np.abs(Xs)
rec("q134_var_theta_mc", float(np.var(Th)))
rec("q134_cov_theta_X_mc", float(np.cov(Th, Xs)[0, 1]))
rec("q134_E_thX2_mc", float(np.mean(Th * Xs ** 2)), "orthogonality with h(x)=x^2")
rec("q134_E_th2X2_mc", float(np.mean(Th ** 2 * Xs ** 2)))

# ---------------------------------------------------------------- dump
with open("d:/Python-UV/MIT_Applied_Prob/computes/qb_s6.json", "w", encoding="utf-8") as fh:
    json.dump(R, fh, indent=1, sort_keys=True)
print("\nwrote computes/qb_s6.json with", len(R), "keys")
