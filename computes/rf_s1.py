# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Every number quoted in R (reference) section 1 — the consolidated tables.

Blocks:
  A  discrete zoo: mean and variance of every row, closed form vs brute-force
     summation over the PMF (Bernoulli, discrete uniform, binomial, geometric,
     Pascal, Poisson, hypergeometric)
  B  continuous zoo: mean and variance of every row by quadrature
     (uniform, exponential, Erlang, normal, beta) + the two beyond-syllabus
     rows (chi-square, Student-t)
  C  the geometric-convention gap: trials-until vs failures-before
  D  master-sheet constants: normal percentiles z, the |rho| <= 1 witness,
     the three-set inclusion-exclusion check, Bayes odds form, the 1/2
     correction, and a two-state Markov steady state
  F  the multinomial row (joint PMF, means, variances, covariances, marginals),
     the four classic waiting times (first success, kth success, pattern HH,
     coupon collector), and the random walk / gambler's ruin closed forms
"""
import io
import json
import sys
from fractions import Fraction
from math import comb, exp, factorial, sqrt

import numpy as np
from scipy import integrate, stats
from scipy.special import gammaln

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
R = {}


def rec(key, val):
    R[key] = val
    print(f"  {key:44s} = {val}")


def moments_discrete(pmf, support):
    """(sum, mean, E[X^2], var) by brute force over an explicit support."""
    tot = sum(pmf(k) for k in support)
    m1 = sum(k * pmf(k) for k in support)
    m2 = sum(k * k * pmf(k) for k in support)
    return tot, m1, m2, m2 - m1 * m1


def moments_cont(pdf, lo, hi):
    tot = integrate.quad(pdf, lo, hi, limit=400)[0]
    m1 = integrate.quad(lambda x: x * pdf(x), lo, hi, limit=400)[0]
    m2 = integrate.quad(lambda x: x * x * pdf(x), lo, hi, limit=400)[0]
    return tot, m1, m2, m2 - m1 * m1


r6 = lambda v: round(float(v), 6)

# ----------------------------------------------------------------- A
print("--- A  discrete zoo: closed form vs brute force ---")

# Bernoulli(p), p = 0.3   (G2 §1)
p = 0.3
tot, m1, _, v = moments_discrete(lambda k: p if k == 1 else 1 - p, [0, 1])
rec("A_bern_p", p)
rec("A_bern_total", r6(tot))
rec("A_bern_mean_bf", r6(m1))
rec("A_bern_mean_cf", r6(p))
rec("A_bern_var_bf", r6(v))
rec("A_bern_var_cf", r6(p * (1 - p)))

# Discrete uniform on {a..b}, a = 2, b = 7   (G2 §1; var (b-a)(b-a+2)/12)
a, b = 2, 7
n_u = b - a + 1
tot, m1, _, v = moments_discrete(lambda k: 1.0 / n_u, range(a, b + 1))
rec("A_dunif_ab", [a, b])
rec("A_dunif_total", r6(tot))
rec("A_dunif_mean_bf", r6(m1))
rec("A_dunif_mean_cf", r6((a + b) / 2))
rec("A_dunif_var_bf", r6(v))
rec("A_dunif_var_cf", r6((b - a) * (b - a + 2) / 12))

# Binomial(n, p), n = 10, p = 0.3   (G2 §1)
n, p = 10, 0.3
tot, m1, _, v = moments_discrete(
    lambda k: comb(n, k) * p**k * (1 - p) ** (n - k), range(0, n + 1))
rec("A_binom_np", [n, p])
rec("A_binom_total", r6(tot))
rec("A_binom_mean_bf", r6(m1))
rec("A_binom_mean_cf", r6(n * p))
rec("A_binom_var_bf", r6(v))
rec("A_binom_var_cf", r6(n * p * (1 - p)))

# Geometric(p) on {1,2,...}, p = 0.2   (G2 §3) — summed far into the tail
p = 0.2
KMAX = 6000
tot, m1, _, v = moments_discrete(
    lambda k: (1 - p) ** (k - 1) * p, range(1, KMAX + 1))
rec("A_geom_p", p)
rec("A_geom_total", round(float(tot), 12))
rec("A_geom_mean_bf", round(float(m1), 12))
rec("A_geom_mean_cf", r6(1 / p))
rec("A_geom_var_bf", round(float(v), 10))
rec("A_geom_var_cf", r6((1 - p) / p**2))

# Pascal of order k, p = 0.3, k = 3   (G4 §2)
k_ord, p = 3, 0.3
tot, m1, _, v = moments_discrete(
    lambda t: comb(t - 1, k_ord - 1) * p**k_ord * (1 - p) ** (t - k_ord),
    range(k_ord, KMAX + 1))
rec("A_pascal_kp", [k_ord, p])
rec("A_pascal_total", round(float(tot), 12))
rec("A_pascal_mean_bf", round(float(m1), 10))
rec("A_pascal_mean_cf", r6(k_ord / p))
rec("A_pascal_var_bf", round(float(v), 8))
rec("A_pascal_var_cf", r6(k_ord * (1 - p) / p**2))

# Poisson(lam), lam = 2.5   (G4 §3)
lam = 2.5
tot, m1, _, v = moments_discrete(
    lambda k: exp(-lam + k * np.log(lam) - float(gammaln(k + 1))),
    range(0, 120))
rec("A_pois_lam", lam)
rec("A_pois_total", round(float(tot), 12))
rec("A_pois_mean_bf", round(float(m1), 12))
rec("A_pois_var_bf", round(float(v), 12))
rec("A_pois_meanvar_cf", lam)

# Hypergeometric: n balls, m red, draw k   (G1 §4, rec04 P3)
N_, M_, K_ = 20, 8, 5
tot, m1, _, v = moments_discrete(
    lambda i: comb(M_, i) * comb(N_ - M_, K_ - i) / comb(N_, K_),
    range(max(0, K_ - (N_ - M_)), min(K_, M_) + 1))
hyp_mean = K_ * M_ / N_
hyp_var = K_ * (M_ / N_) * (1 - M_ / N_) * (N_ - K_) / (N_ - 1)
rec("A_hyper_nmk", [N_, M_, K_])
rec("A_hyper_total", r6(tot))
rec("A_hyper_mean_bf", r6(m1))
rec("A_hyper_mean_cf", r6(hyp_mean))
rec("A_hyper_var_bf", r6(v))
rec("A_hyper_var_cf", r6(hyp_var))
rec("A_hyper_var_exact_frac", str(Fraction(hyp_var).limit_denominator(10**6)))
# the binomial cousin, same draw with replacement: variance shaved by (n-k)/(n-1)
rec("A_hyper_binom_var", r6(K_ * (M_ / N_) * (1 - M_ / N_)))
rec("A_hyper_fpc", r6((N_ - K_) / (N_ - 1)))

# ----------------------------------------------------------------- B
print("\n--- B  continuous zoo: closed form vs quadrature ---")

# Uniform[a,b], a = 2, b = 7   (G3 §1)
a, b = 2.0, 7.0
tot, m1, _, v = moments_cont(lambda x: 1 / (b - a), a, b)
rec("B_unif_ab", [a, b])
rec("B_unif_total", r6(tot))
rec("B_unif_mean_quad", r6(m1))
rec("B_unif_mean_cf", r6((a + b) / 2))
rec("B_unif_var_quad", r6(v))
rec("B_unif_var_cf", r6((b - a) ** 2 / 12))

# Exponential(lam), lam = 2   (G3 §1)
lam = 2.0
tot, m1, _, v = moments_cont(lambda x: lam * exp(-lam * x), 0, 60)
rec("B_exp_lam", lam)
rec("B_exp_total", r6(tot))
rec("B_exp_mean_quad", r6(m1))
rec("B_exp_mean_cf", r6(1 / lam))
rec("B_exp_var_quad", r6(v))
rec("B_exp_var_cf", r6(1 / lam**2))

# Erlang(k, lam), k = 3, lam = 2   (G4 §3)
k_ord, lam = 3, 2.0
erl = lambda y: lam**k_ord * y ** (k_ord - 1) * exp(-lam * y) / factorial(k_ord - 1)
tot, m1, _, v = moments_cont(erl, 0, 80)
rec("B_erlang_klam", [k_ord, lam])
rec("B_erlang_total", r6(tot))
rec("B_erlang_mean_quad", r6(m1))
rec("B_erlang_mean_cf", r6(k_ord / lam))
rec("B_erlang_var_quad", r6(v))
rec("B_erlang_var_cf", r6(k_ord / lam**2))
# Gamma(a, lam) with non-integer a agrees with Erlang at integer a
rec("B_gamma_noninteger_mean", r6(stats.gamma.mean(2.5, scale=1 / lam)))
rec("B_gamma_noninteger_var", r6(stats.gamma.var(2.5, scale=1 / lam)))
rec("B_gamma_matches_erlang_mean",
    r6(stats.gamma.mean(k_ord, scale=1 / lam)))

# Normal(mu, sigma^2), mu = 2, sigma^2 = 16   (G3 §1)
mu, sig = 2.0, 4.0
nrm = lambda x: exp(-((x - mu) ** 2) / (2 * sig**2)) / (sig * sqrt(2 * np.pi))
tot, m1, _, v = moments_cont(nrm, mu - 40 * sig, mu + 40 * sig)
rec("B_norm_musig2", [mu, sig**2])
rec("B_norm_total", r6(tot))
rec("B_norm_mean_quad", r6(m1))
rec("B_norm_var_quad", r6(v))

# Beta(alpha, beta) = the coin-bias posterior of G6 §3: n = 10, k = 7
al, be = 8.0, 4.0
bet = lambda q: stats.beta.pdf(q, al, be)
tot, m1, _, v = moments_cont(bet, 0, 1)
rec("B_beta_ab", [al, be])
rec("B_beta_total", r6(tot))
rec("B_beta_mean_quad", r6(m1))
rec("B_beta_mean_cf", r6(al / (al + be)))
rec("B_beta_var_quad", r6(v))
rec("B_beta_var_cf", r6(al * be / ((al + be) ** 2 * (al + be + 1))))
rec("B_beta_mean_frac", str(Fraction(al / (al + be)).limit_denominator(1000)))

# Beyond 6.041: chi-square(k) and Student-t(nu)
kdf = 5
rec("B_chi2_df", kdf)
rec("B_chi2_mean", r6(stats.chi2.mean(kdf)))
rec("B_chi2_var", r6(stats.chi2.var(kdf)))
nu = 9
rec("B_t_df", nu)
rec("B_t_mean", r6(stats.t.mean(nu)))
rec("B_t_var_quad", r6(stats.t.var(nu)))
rec("B_t_var_cf", r6(nu / (nu - 2)))
rec("B_t_crit_975_df9", r6(stats.t.ppf(0.975, nu)))
rec("B_z_crit_975", r6(stats.norm.ppf(0.975)))
rec("B_t_over_z_df9", r6(stats.t.ppf(0.975, nu) / stats.norm.ppf(0.975)))
rec("B_t_crit_975_df100", r6(stats.t.ppf(0.975, 100)))

# ----------------------------------------------------------------- C
print("\n--- C  the two geometric conventions ---")
for pv in (0.3, 0.2, 0.5):
    tag = str(pv).replace(".", "")
    trials = 1 / pv                       # our notes / B&T: X in {1,2,...}
    fails = (1 - pv) / pv                 # Chen–Blitzstein: Y = X-1 in {0,1,...}
    rec(f"C_p{tag}_mean_trials", r6(trials))
    rec(f"C_p{tag}_mean_failures", r6(fails))
    rec(f"C_p{tag}_gap", r6(trials - fails))
    rec(f"C_p{tag}_var_both", r6((1 - pv) / pv**2))
# scipy follows the trials convention
rec("C_scipy_geom_pmf_at_0", r6(stats.geom.pmf(0, 0.3)))
rec("C_scipy_geom_pmf_at_1", r6(stats.geom.pmf(1, 0.3)))
rec("C_scipy_geom_mean", r6(stats.geom.mean(0.3)))
rec("C_scipy_geom_loc_m1_mean", r6(stats.geom.mean(0.3, loc=-1)))
rec("C_scipy_nbinom_1_p_mean", r6(stats.nbinom.mean(1, 0.3)))

# ----------------------------------------------------------------- D
print("\n--- D  master-sheet constants ---")
for lvl, alpha in ((90, 0.10), (95, 0.05), (99, 0.01)):
    rec(f"D_z_{lvl}", round(float(stats.norm.ppf(1 - alpha / 2)), 6))

# Three-set inclusion-exclusion, verified on an explicit finite model
rng = np.random.default_rng(6041)
w = rng.random(64)
w /= w.sum()
A = np.zeros(64, bool); A[:32] = True                 # bit 0
B_ = np.array([(i // 2) % 2 == 0 for i in range(64)])  # bit 1 pattern
C_ = np.array([(i // 4) % 2 == 0 for i in range(64)])
P = lambda ev: float(w[ev].sum())
lhs = P(A | B_ | C_)
rhs = (P(A) + P(B_) + P(C_) - P(A & B_) - P(A & C_) - P(B_ & C_)
       + P(A & B_ & C_))
rec("D_incl_excl3_lhs", round(lhs, 12))
rec("D_incl_excl3_rhs", round(rhs, 12))
rec("D_incl_excl3_maxdev", float(abs(lhs - rhs)))

# Bayes in odds form — the radar of G1 §2, reproduced
prior, sens, fa = 0.05, 0.99, 0.10
prior_odds = prior / (1 - prior)
lr = sens / fa
post_odds = prior_odds * lr
rec("D_bayes_prior_odds", r6(prior_odds))
rec("D_bayes_LR", r6(lr))
rec("D_bayes_post_odds", r6(post_odds))
rec("D_bayes_post_prob", r6(post_odds / (1 + post_odds)))
rec("D_bayes_direct", r6(prior * sens / (prior * sens + (1 - prior) * fa)))

# |rho| <= 1 with the equality witness, and the signal+noise instance of G3 §4
rec("D_rho_signal_noise", r6(1 / sqrt(2)))
rec("D_rho_linear_pos", 1.0)
rec("D_rho_linear_neg", -1.0)
# linear-LMS error (1 - rho^2) var(Theta) at that rho
rec("D_lms_error_factor", r6(1 - 0.5))

# CLT with the 1/2 correction on Binomial(36, 1/2), the L20 example
n, p = 36, 0.5
exact = float(stats.binom.cdf(21, n, p))
plain = float(stats.norm.cdf((21 - n * p) / sqrt(n * p * (1 - p))))
corr = float(stats.norm.cdf((21 + 0.5 - n * p) / sqrt(n * p * (1 - p))))
rec("D_clt_exact", r6(exact))
rec("D_clt_uncorrected", r6(plain))
rec("D_clt_corrected", r6(corr))
rec("D_clt_err_uncorrected", r6(abs(exact - plain)))
rec("D_clt_err_corrected", r6(abs(exact - corr)))

# Two-state Markov steady state of G5 §3 (pi = (2/7, 5/7))
Pm = np.array([[0.5, 0.5], [0.2, 0.8]])
vals, vecs = np.linalg.eig(Pm.T)
pi = np.real(vecs[:, np.argmin(abs(vals - 1))])
pi = pi / pi.sum()
rec("D_markov_pi", [r6(pi[0]), r6(pi[1])])
rec("D_markov_pi_exact", ["2/7", "5/7"])
rec("D_markov_recurrence_times", [r6(1 / pi[0]), r6(1 / pi[1])])
rec("D_markov_P50_row0", [r6(x) for x in np.linalg.matrix_power(Pm, 50)[0]])
# detailed balance check for this chain
rec("D_markov_detailed_balance_lhs", r6(pi[0] * Pm[0, 1]))
rec("D_markov_detailed_balance_rhs", r6(pi[1] * Pm[1, 0]))

# ----------------------------------------------------------------- E
print("\n--- E  the two practice problems ---")
# Practice 1.1: the same defect story on six rows of the tables
pd_, nd_ = 0.02, 500
rec("E_p11a_binom_mean", r6(nd_ * pd_))
rec("E_p11a_binom_var", r6(nd_ * pd_ * (1 - pd_)))
rec("E_p11b_geom_mean_trials", r6(1 / pd_))
rec("E_p11b_geom_mean_failures", r6((1 - pd_) / pd_))
rec("E_p11c_pascal_mean", r6(3 / pd_))
rec("E_p11c_pascal_var", r6(3 * (1 - pd_) / pd_**2))
N2, M2, K2 = 500, 10, 20
rec("E_p11d_hyper_mean", r6(K2 * M2 / N2))
rec("E_p11d_hyper_fpc", r6((N2 - K2) / (N2 - 1)))
rec("E_p11e_pois_meanvar", r6(pd_ * nd_))
rec("E_p11f_erlang_mean", r6(3 / pd_))
rec("E_p11f_erlang_var", r6(3 / pd_**2))
rec("E_p11_pascal_over_erlang_var", r6((3 * (1 - pd_) / pd_**2) / (3 / pd_**2)))

# Practice 1.2: five answers from five moments
EX, EY, vX, vY, cXY = 3.0, 5.0, 4.0, 9.0, -3.0
rec("E_p12i_mean", r6(2 * EX - EY + 1))
var_2XmY = 4 * vX + vY + 2 * (2) * (-1) * cXY
rec("E_p12ii_var", r6(var_2XmY))
rec("E_p12ii_var_if_indep_wrongly", r6(4 * vX + vY))
rec("E_p12ii_understatement_pct",
    r6(100 * (var_2XmY - (4 * vX + vY)) / var_2XmY))
rho12 = cXY / (sqrt(vX) * sqrt(vY))
rec("E_p12iii_rho", r6(rho12))
rec("E_p12iv_EXY", r6(cXY + EX * EY))
rec("E_p12v_lms_mse", r6((1 - rho12**2) * vY))
# t vs z width, quoted as a percentage in §1.5
rec("E_t9_over_z_pct", r6(100 * (stats.t.ppf(0.975, 9) / stats.norm.ppf(0.975) - 1)))
rec("E_t100_over_z_pct", r6(100 * (stats.t.ppf(0.975, 100) / stats.norm.ppf(0.975) - 1)))


# ----------------------------------------------------------------- F
print("\n--- F  multinomial row, waiting times, random walk ---")

# --- F1  Multinomial(n, theta), n = 10, r = 3, theta = (0.5, 0.3, 0.2)
# Full enumeration of the joint PMF over every count vector, then the three
# closed forms E[N_k] = n t_k, var(N_k) = n t_k (1-t_k), cov = -n t_i t_j.
nm, th = 10, (0.5, 0.3, 0.2)
rec("F_mn_n", nm)
rec("F_mn_theta", list(th))
cells = []
for n1 in range(nm + 1):
    for n2 in range(nm + 1 - n1):
        n3 = nm - n1 - n2
        pr = (factorial(nm) / (factorial(n1) * factorial(n2) * factorial(n3))
              * th[0] ** n1 * th[1] ** n2 * th[2] ** n3)
        cells.append(((n1, n2, n3), pr))
rec("F_mn_num_cells", len(cells))
rec("F_mn_total_mass", r6(sum(pr for _, pr in cells)))
# the single cell quoted in G1 4.6 (rec04 P5)
rec("F_mn_coeff_532", factorial(10) // (factorial(5) * factorial(3) * factorial(2)))
rec("F_mn_p_532", r6(dict(cells)[(5, 3, 2)]))
for kk in range(3):
    mk = sum(c[kk] * pr for c, pr in cells)
    m2k = sum(c[kk] ** 2 * pr for c, pr in cells)
    rec(f"F_mn_mean_bf_{kk+1}", r6(mk))
    rec(f"F_mn_mean_cf_{kk+1}", r6(nm * th[kk]))
    rec(f"F_mn_var_bf_{kk+1}", r6(m2k - mk * mk))
    rec(f"F_mn_var_cf_{kk+1}", r6(nm * th[kk] * (1 - th[kk])))
for i_, j_ in ((0, 1), (0, 2), (1, 2)):
    mi = sum(c[i_] * pr for c, pr in cells)
    mj = sum(c[j_] * pr for c, pr in cells)
    mij = sum(c[i_] * c[j_] * pr for c, pr in cells)
    rec(f"F_mn_cov_bf_{i_+1}{j_+1}", r6(mij - mi * mj))
    rec(f"F_mn_cov_cf_{i_+1}{j_+1}", r6(-nm * th[i_] * th[j_]))
    rec(f"F_mn_rho_{i_+1}{j_+1}",
        r6((mij - mi * mj) / sqrt(nm * th[i_] * (1 - th[i_])
                                  * nm * th[j_] * (1 - th[j_]))))
# var(N1+N2+N3) must be 0: the counts are pinned to n
var_sum = (sum(nm * t * (1 - t) for t in th)
           + sum(-2 * nm * th[i_] * th[j_] for i_, j_ in ((0, 1), (0, 2), (1, 2))))
rec("F_mn_var_of_total", r6(var_sum))
rgm = np.random.default_rng(20260819)
sim = rgm.multinomial(nm, th, size=400000)
rec("F_mn_sim_mean_1", r6(sim[:, 0].mean()))
rec("F_mn_sim_var_1", r6(sim[:, 0].var()))
rec("F_mn_sim_cov_12", r6(np.cov(sim[:, 0], sim[:, 1])[0, 1]))
# marginal of N_1 is Binomial(n, theta_1)
rec("F_mn_marginal_max_dev_binom",
    max(abs(sum(pr for c, pr in cells if c[0] == k) - stats.binom.pmf(k, nm, th[0]))
        for k in range(nm + 1)))

# --- F2  The four classic waiting times
pw = 0.5
rec("F_wt_p", pw)
rec("F_wt_first_success", r6(1 / pw))                       # geometric, G2 3
rec("F_wt_third_success", r6(3 / pw))                       # Pascal k=3, G4 2
rec("F_wt_HH_closed", r6((1 + pw) / pw**2))                 # (1+p)/p^2, G2 3
# HH by first-step analysis solved as a 2x2 linear system: A = 1 + pB + qA,
# B = 1 + qA  (state A = no banked head, B = one banked head)
Aw = np.array([[1 - (1 - pw), -pw], [-(1 - pw), 1.0]])
bw = np.array([1.0, 1.0])
solw = np.linalg.solve(Aw, bw)
rec("F_wt_HH_firststep", r6(solw[0]))
rec("F_wt_HHH_closed", r6((1 + pw + pw**2) / pw**3))
# coupon collector n H_n  (G4 3, Example 3.9)
for nn in (6, 10, 52):
    Hn = sum(Fraction(1, k) for k in range(1, nn + 1))
    rec(f"F_wt_H_{nn}", r6(float(Hn)))
    rec(f"F_wt_nH_{nn}", r6(float(nn * Hn)))
rec("F_wt_6H6_exact_fraction",
    str(6 * sum(Fraction(1, k) for k in range(1, 7))))
# Monte-Carlo: fair die, draws until all six faces seen
rgw = np.random.default_rng(41)
tot_draws = 0
TRIALS = 200000
for _ in range(TRIALS):
    seen, cnt = 0, 0
    while seen != 0b111111:
        seen |= 1 << int(rgw.integers(6))
        cnt += 1
    tot_draws += cnt
rec("F_wt_die_sim_mean", r6(tot_draws / TRIALS))
# Monte-Carlo: tosses of a fair coin until HH
rgh = np.random.default_rng(7)
tot_h, run = 0, 0
for _ in range(200000):
    prev, cnt = 0, 0
    while True:
        c = int(rgh.integers(2))
        cnt += 1
        if c == 1 and prev == 1:
            break
        prev = c
    tot_h += cnt
rec("F_wt_HH_sim_mean", r6(tot_h / 200000))

# --- F3  Random walk / gambler's ruin  (G5 4.3)
def ruin_solve(p_, m_):
    """Direct linear solve of a_i and D_i on the (m-1) transient states."""
    A = np.zeros((m_ - 1, m_ - 1))
    ba = np.zeros(m_ - 1)
    bd = np.ones(m_ - 1)
    for i in range(1, m_):
        A[i - 1, i - 1] = 1.0
        if i + 1 <= m_ - 1:
            A[i - 1, i] = -p_
        else:
            ba[i - 1] += p_          # a_m = 1
        if i - 1 >= 1:
            A[i - 1, i - 2] = -(1 - p_)
        # a_0 = 0, D_0 = D_m = 0 contribute nothing
    return np.linalg.solve(A, ba), np.linalg.solve(A, bd)

for p_, m_, i_ in ((0.5, 20, 10), (0.45, 20, 10), (0.6, 20, 10), (0.5, 100, 40)):
    a_num, d_num = ruin_solve(p_, m_)
    if p_ == 0.5:
        a_cf, d_cf = i_ / m_, i_ * (m_ - i_)
    else:
        rho = (1 - p_) / p_
        a_cf = (1 - rho**i_) / (1 - rho**m_)
        d_cf = (i_ - m_ * a_cf) / (1 - 2 * p_)
    tag = f"F_rw_p{int(p_*100)}_m{m_}_i{i_}"
    rec(tag + "_a_cf", r6(a_cf))
    rec(tag + "_a_num", r6(a_num[i_ - 1]))
    rec(tag + "_D_cf", r6(d_cf))
    rec(tag + "_D_num", r6(d_num[i_ - 1]))
# symmetric-walk simulation, m = 20 starting at i = 10
rgr = np.random.default_rng(1234)
wins, steps = 0, 0
for _ in range(50000):
    x, t = 10, 0
    while 0 < x < 20:
        x += 1 if rgr.integers(2) else -1
        t += 1
    wins += (x == 20)
    steps += t
rec("F_rw_sim_a_p50_m20_i10", r6(wins / 50000))
rec("F_rw_sim_D_p50_m20_i10", r6(steps / 50000))

with open("d:/Python-UV/MIT_Applied_Prob/computes/rf_s1.json", "w",
          encoding="utf-8") as f:
    json.dump(R, f, indent=1)
print("\nwrote computes/rf_s1.json  (%d keys)" % len(R))
