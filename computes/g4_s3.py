# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""G4 section 3 (The Poisson process I) — every number that appears in the fragment.

Run:  uv run computes/g4_s3.py
Writes computes/g4_s3.json
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy import integrate, special, stats

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict = {}


def show(key, val, note=""):
    if isinstance(val, F):
        R[key] = [val.numerator, val.denominator]
        txt = f"{val}  = {float(val):.6f}"
    elif isinstance(val, float):
        R[key] = val
        txt = f"{val:.8f}"
    elif isinstance(val, (list, tuple)):
        R[key] = list(val)
        txt = "[" + ", ".join(f"{v:.6f}" if isinstance(v, float) else str(v) for v in val) + "]"
    else:
        R[key] = val
        txt = str(val)
    print(f"{key:40s} = {txt}   {note}")


def pois(k, mu):
    return math.exp(-mu) * mu ** k / math.factorial(k)


def binom(k, n, p):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


# =====================================================================
# 3.1  Small-interval probabilities: how good is 1 - lambda*delta ?
# =====================================================================
print("\n=== 3.1  small-interval probabilities, lambda = 2 per unit time ===")
lam = 2.0
show("si_lam", lam)
for d in (0.5, 0.1, 0.01, 0.001):
    tag = str(d).replace("0.", "").replace(".", "")
    show(f"si_P0_exact_{tag}", pois(0, lam * d), f"exact P(0,delta), delta={d}")
    show(f"si_P0_lin_{tag}", 1 - lam * d, "linear approx 1 - lambda*delta")
    show(f"si_P0_err_{tag}", abs(pois(0, lam * d) - (1 - lam * d)), "o(delta) size")
    show(f"si_P1_exact_{tag}", pois(1, lam * d), f"exact P(1,delta), delta={d}")
    show(f"si_P1_lin_{tag}", lam * d, "linear approx lambda*delta")
    show(f"si_Pge2_{tag}", 1 - pois(0, lam * d) - pois(1, lam * d), "P(k>=2, delta)")
    show(f"si_ratio_ge2_{tag}", (1 - pois(0, lam * d) - pois(1, lam * d)) / d, "P(k>=2)/delta -> 0")

# =====================================================================
# 3.2  Binomial -> Poisson limit.  Fixed lambda*t = 2.5
# =====================================================================
print("\n=== 3.2  binomial(n, p=mu/n) -> Poisson(mu), mu = 2.5 ===")
MU = 2.5
show("lim_mu", MU)
KS = list(range(0, 9))
show("lim_ks", KS)
show("lim_pois", [pois(k, MU) for k in KS])
for n in (5, 10, 25, 100, 1000):
    p = MU / n
    vals = [binom(k, n, p) if k <= n else 0.0 for k in KS]
    dev = max(abs(vals[k] - pois(k, MU)) for k in KS)
    show(f"lim_binom_n{n}", vals, f"p = {p}")
    show(f"lim_maxdev_n{n}", dev, "max |binomial - Poisson| over k=0..8")
# the three limit factors at k = 2, n = 100
n, k, p = 100, 2, MU / 100
show("lim_factor_falling_n100_k2", (n * (n - 1)) / n ** 2, "n(n-1)/n^2 -> 1")
show("lim_factor_pow_n100", (1 - p) ** n, "(1-mu/n)^n -> e^-mu")
show("lim_factor_expmu", math.exp(-MU))
show("lim_factor_corr_n100_k2", (1 - p) ** (-k), "(1-mu/n)^-k -> 1")
show("lim_exact_binom_n100_k2", binom(2, 100, p))
show("lim_pois_k2", pois(2, MU))

# B&T Example 6.6 (Kasparov) — accuracy of the Poisson approximation
print("\n=== 3.2b  B&T Example 6.6, n=100 p=0.01 (mu=1) and n=5 p=0.1 (mu=0.5) ===")
for k in (0, 2, 5, 10):
    show(f"kas_binom_k{k}", binom(k, 100, 0.01))
    show(f"kas_pois_k{k}", pois(k, 1.0))
show("kas5_binom", [binom(k, 5, 0.1) for k in range(6)])
show("kas5_pois", [pois(k, 0.5) for k in range(6)])
show("kas5_maxdev", max(abs(binom(k, 5, 0.1) - pois(k, 0.5)) for k in range(6)))
show("kas100_maxdev", max(abs(binom(k, 100, 0.01) - pois(k, 1.0)) for k in range(11)))

# normalization + moments of the Poisson pmf
print("\n=== 3.2c  Poisson pmf sanity: sum = 1, mean = var = mu ===")
for mu in (0.5, 2.5, 5.0):
    tag = str(mu).replace(".", "p")
    ks = np.arange(0, 200)
    pk = np.exp(-mu) * mu ** ks / special.factorial(ks)
    show(f"pois_sum_mu{tag}", float(pk.sum()))
    show(f"pois_mean_mu{tag}", float((ks * pk).sum()))
    show(f"pois_var_mu{tag}", float((ks ** 2 * pk).sum() - ((ks * pk).sum()) ** 2))

# =====================================================================
# 3.2d  L14 slide 5 — email example (UNSOLVED on the slide)
# =====================================================================
print("\n=== 3.2d  L14 slide 5: lambda = 5/hour, tau = 0.5 hour ===")
lam_e, tau_e = 5.0, 0.5
mu_e = lam_e * tau_e
show("mail_lam", lam_e)
show("mail_tau", tau_e)
show("mail_mu", mu_e, "lambda*tau")
show("mail_P0", pois(0, mu_e))
show("mail_P1", pois(1, mu_e))
show("mail_P2", pois(2, mu_e))
show("mail_Pge2", 1 - pois(0, mu_e) - pois(1, mu_e))
show("mail_mean", mu_e)
show("mail_var", mu_e)
show("mail_sd", math.sqrt(mu_e))
# B&T Example 6.8 variant: lambda = 0.2 per hour, tau = 1 hour
show("mail_bt_mu", 0.2 * 1.0)
show("mail_bt_P0", pois(0, 0.2))
show("mail_bt_P1", pois(1, 0.2))
# a two-piece time set of total length 1 hour (B&T Example 6.9 idea)
show("mail_split_mu", lam_e * (0.25 + 0.75))
show("mail_split_P0", pois(0, lam_e * 1.0))
# bank example 6.9 numbers
show("bank_mu_M", 10 * 10.0)
show("bank_mu_N", 10 * 5.0)
show("bank_mu_sum", 10 * 15.0)

# =====================================================================
# 3.3  Interarrival times: exponential
# =====================================================================
print("\n=== 3.3  first arrival time T ~ Exp(lambda), lambda = 5/hour ===")
show("exp_lam", lam_e)
show("exp_mean", 1 / lam_e, "hours")
show("exp_mean_min", 60 / lam_e, "minutes")
show("exp_var", 1 / lam_e ** 2)
show("exp_sd", 1 / lam_e)
show("exp_P_gt_half", math.exp(-lam_e * 0.5), "P(T > 0.5 h) = P(0, 0.5)")
show("exp_check_P0", pois(0, mu_e), "same number as P(0,tau)")
show("exp_cdf_half", 1 - math.exp(-lam_e * 0.5))
show("exp_median", math.log(2) / lam_e, "hours")
show("exp_median_min", 60 * math.log(2) / lam_e, "minutes")
# memorylessness check
t0, s0 = 0.4, 0.2
show("mem_t", t0)
show("mem_s", s0)
show("mem_cond", math.exp(-lam_e * (t0 + s0)) / math.exp(-lam_e * t0))
show("mem_fresh", math.exp(-lam_e * s0))
show("mem_devi", abs(math.exp(-lam_e * (t0 + s0)) / math.exp(-lam_e * t0) - math.exp(-lam_e * s0)))
# normalization of the exponential density
show("exp_norm", float(integrate.quad(lambda y: lam_e * math.exp(-lam_e * y), 0, np.inf)[0]))

# =====================================================================
# 3.4  k-th arrival: Erlang
# =====================================================================
print("\n=== 3.4  Erlang(k, lambda) ===")
show("erl_lam", lam_e)
for k in (1, 2, 3):
    show(f"erl_mean_k{k}", k / lam_e)
    show(f"erl_var_k{k}", k / lam_e ** 2)
    show(f"erl_mode_k{k}", (k - 1) / lam_e, "peak of the density")
    show(f"erl_norm_k{k}", float(integrate.quad(
        lambda y, k=k: lam_e ** k * y ** (k - 1) * math.exp(-lam_e * y) / math.factorial(k - 1),
        0, np.inf)[0]))
    show(f"erl_peak_k{k}", (lam_e ** k * ((k - 1) / lam_e) ** (k - 1) *
                           math.exp(-(k - 1)) / math.factorial(k - 1)) if k > 1 else lam_e)
# Erlang CDF identity check: F_{Y_k}(y) = 1 - sum_{n<k} P(n,y)
yv, kv = 0.7, 3
lhs = float(integrate.quad(lambda y: lam_e ** kv * y ** (kv - 1) * math.exp(-lam_e * y)
                           / math.factorial(kv - 1), 0, yv)[0])
rhs = 1 - sum(pois(n, lam_e * yv) for n in range(kv))
show("erl_cdf_lhs", lhs, "integral of Erlang(3) density to y=0.7")
show("erl_cdf_rhs", rhs, "1 - sum_{n=0}^{2} P(n, 0.7)")
show("erl_cdf_dev", abs(lhs - rhs))

# B&T Example 6.12 — IRS hotline, 56th in line, lambda = 2 per minute
print("\n=== 3.4b  B&T Example 6.12: k = 56, lambda = 2/min ===")
K_IRS, LAM_IRS = 56, 2.0
show("irs_k", K_IRS)
show("irs_lam", LAM_IRS)
show("irs_mean", K_IRS / LAM_IRS, "minutes")
show("irs_var", K_IRS / LAM_IRS ** 2)
show("irs_sd", math.sqrt(K_IRS / LAM_IRS ** 2))
tail = sum(pois(n, LAM_IRS * 30) for n in range(K_IRS))
show("irs_mu30", LAM_IRS * 30, "expected arrivals in 30 min")
show("irs_tail_exact", tail, "P(Y_56 > 30) = P(fewer than 56 departures in 30 min)")
show("irs_tail_scipy", float(stats.erlang.sf(30, K_IRS, scale=1 / LAM_IRS)))
show("irs_tail_dev", abs(tail - float(stats.erlang.sf(30, K_IRS, scale=1 / LAM_IRS))))
z_irs = (30 - K_IRS / LAM_IRS) / math.sqrt(K_IRS / LAM_IRS ** 2)
show("irs_z", z_irs)
show("irs_tail_clt", float(stats.norm.sf(z_irs)))
show("irs_clt_err", abs(float(stats.norm.sf(z_irs)) - tail))

# =====================================================================
# 3.5  merging (L14 slide 8 unsolved example) — numeric illustration
# =====================================================================
print("\n=== 3.5  merging two Poisson processes ===")
l1, l2 = 3.0, 2.0
show("mrg_l1", l1)
show("mrg_l2", l2)
show("mrg_lsum", l1 + l2)
show("mrg_p_first", l1 / (l1 + l2))
show("mrg_p_second", l2 / (l1 + l2))
# check by direct integration: P(T1 < T2) with T1~Exp(l1), T2~Exp(l2)
show("mrg_check_int", float(integrate.quad(
    lambda t: l1 * math.exp(-l1 * t) * math.exp(-l2 * t), 0, np.inf)[0]))
show("mrg_check_dev", abs(float(integrate.quad(
    lambda t: l1 * math.exp(-l1 * t) * math.exp(-l2 * t), 0, np.inf)[0]) - l1 / (l1 + l2)))

# =====================================================================
# 3.5b  rec14 P1 — mosquito / tick Bernoulli merging
# =====================================================================
print("\n=== 3.5b  rec14 P1 ===")
p_m = F(1, 2) * F(1, 5)
show("r1_p", p_m, "0.5 * 0.2")
show("r1_p_dec", float(p_m))
show("r1_EX", 1 / p_m)
show("r1_varX", (1 - p_m) / p_m ** 2)
q_t = F(1, 10) * F(7, 10)
show("r1_q", q_t, "0.1 * 0.7")
show("r1_q_dec", float(q_t))
r_b = p_m + q_t - p_m * q_t
show("r1_r", r_b)
show("r1_r_dec", float(r_b))
show("r1_pq", p_m * q_t)
show("r1_EY", float(1 / r_b))
show("r1_varY", float((1 - r_b) / r_b ** 2))
show("r1_1mr", float(1 - r_b))
show("r1_r2", float(r_b ** 2))
# alternative: r = 1 - (1-p)(1-q)
show("r1_r_alt", float(1 - (1 - p_m) * (1 - q_t)), "1-(1-p)(1-q), must equal r")

# =====================================================================
# 3.5c  rec14 P2 — Al and Bob
# =====================================================================
print("\n=== 3.5c  rec14 P2 ===")
show("r2a", F(1, 8) ** 2, "P(two more all-tails trials)")
show("r2a_dec", float(F(1, 8) ** 2))
ps = F(2, 8)
show("r2_psucc", ps, "P(all 3 coins same) = 2/8")
show("r2_psucc_dec", float(ps))
show("r2_pK_check", float(sum(k * float(ps) ** 2 * (1 - float(ps)) ** (k - 1)
                              for k in range(1, 4000))), "sum of p_K(k) must be 1")
show("r2_EK", float(sum(k * k * float(ps) ** 2 * (1 - float(ps)) ** (k - 1)
                        for k in range(1, 6000))), "E[K] = 2/p - 1")
show("r2_EK_formula", float(2 / ps - 1))
# (b)(ii) M = number of tails before the first success
EX2 = F(3, 2)
varX2 = F(1, 4)
show("r2_EXi", EX2, "X uniform on {1,2}")
show("r2_varXi", varX2, "E[X^2]-(E[X])^2 = 5/2 - 9/4")
show("r2_EX2sq", F(5, 2), "E[X^2] = (1+4)/2")
show("r2_ER", 1 / ps, "geometric mean 1/p")
show("r2_EN", 1 / ps - 1, "shifted geometric N = R-1")
show("r2_varR", (1 - ps) / ps ** 2)
show("r2_varN", (1 - ps) / ps ** 2, "shift does not change variance")
EM = EX2 * (1 / ps - 1)
show("r2_EM", EM)
show("r2_EM_dec", float(EM))
t1 = (1 / ps - 1) * varX2
t2 = EX2 ** 2 * ((1 - ps) / ps ** 2)
show("r2_varM_term1", t1, "E[N] var(X)")
show("r2_varM_term2", t2, "(E[X])^2 var(N)")
show("r2_varM", t1 + t2)
show("r2_varM_dec", float(t1 + t2))
# (c) Bob
for m in (4, 3, 2):
    show(f"r2c_p{m}coins", F(2, 2 ** m), f"P(all {m} coins same side)")
show("r2c_EX", float(1 / F(2, 16)))
show("r2c_EY", float(1 / F(2, 8)))
show("r2c_EZ", float(1 / F(2, 4)))
show("r2c_EN", float(1 / F(2, 16) + 1 / F(2, 8) + 1 / F(2, 4)))
show("r2c_varN", float((1 - F(1, 8)) / F(1, 8) ** 2 + (1 - F(1, 4)) / F(1, 4) ** 2
                       + (1 - F(1, 2)) / F(1, 2) ** 2), "bonus: var(N)")

# =====================================================================
# 3.5d  rec14 P3 — coupon collector
# =====================================================================
print("\n=== 3.5d  rec14 P3 ===")
for n in (4, 10, 100, 1000):
    H = sum(1 / k for k in range(1, n + 1))
    show(f"r3_H{n}", H, f"harmonic number H_{n}")
    show(f"r3_EM{n}", n * H, "n H_n")
    show(f"r3_nlogn{n}", n * math.log(n))
    show(f"r3_ratio{n}", n * H / (n * math.log(n)))
show("r3_gamma", 0.5772156649015329, "Euler-Mascheroni constant")
show("r3_EM10_approx", 10 * (math.log(10) + 0.5772156649015329 + 1 / 20),
     "n(log n + gamma + 1/(2n))")
# simulate to confirm E[M] for n = 10
rng = np.random.default_rng(20101026)
trials = 200000
n_sim = 10
draws = 0
tot = 0
for _ in range(trials):
    seen = 0
    mask = 0
    c = 0
    while seen < n_sim:
        j = rng.integers(0, n_sim)
        c += 1
        if not (mask >> int(j)) & 1:
            mask |= 1 << int(j)
            seen += 1
    tot += c
show("r3_sim_n10", tot / trials, f"Monte-Carlo mean over {trials} runs")
show("r3_sim_trials", trials)

# =====================================================================
# 3.6  widget verification: max deviation binomial vs Poisson
# =====================================================================
print("\n=== 3.6  widget check: max |binom(n, mu/n) - Poisson(mu)| ===")
wid = {}
for mu in (0.5, 1.0, 2.5, 5.0):
    for n in (5, 10, 20, 50, 100, 500):
        if mu / n >= 1:
            continue
        d = max(abs(binom(k, n, mu / n) - pois(k, mu)) for k in range(0, min(n, 40) + 1))
        wid[f"mu{mu}_n{n}"] = d
        print(f"  mu={mu:4} n={n:4}  maxdev = {d:.8f}")
R["widget_maxdev_grid"] = wid
show("widget_spot_mu2p5_n50", max(abs(binom(k, 50, 2.5 / 50) - pois(k, 2.5)) for k in range(41)))
show("widget_spot_mu2p5_n500", max(abs(binom(k, 500, 2.5 / 500) - pois(k, 2.5)) for k in range(41)))
show("widget_decay_ratio", (max(abs(binom(k, 50, 2.5 / 50) - pois(k, 2.5)) for k in range(41))
                            / max(abs(binom(k, 500, 2.5 / 500) - pois(k, 2.5)) for k in range(41))),
     "roughly 10 => deviation ~ C/n")

# =====================================================================
# practice-question answers
# =====================================================================
print("\n=== practice answers ===")
# P3.1 delta accuracy
show("pq_31_lam", 4.0)
show("pq_31_delta", 0.002)
show("pq_31_lin", 4.0 * 0.002)
show("pq_31_exact", pois(1, 4.0 * 0.002))
show("pq_31_relerr", abs(pois(1, 0.008) - 0.008) / pois(1, 0.008))
# P3.2 buses lambda = 6/hour, 20 minutes
show("pq_32_mu", 6.0 * (20 / 60))
show("pq_32_P0", pois(0, 2.0))
show("pq_32_Pge3", 1 - sum(pois(k, 2.0) for k in range(3)))
show("pq_32_P_exactly2_in_two_disjoint", pois(1, 1.0) ** 2, "one in each of two 10-min halves")
show("pq_32_P2_total", pois(2, 2.0))
show("pq_32_cond", pois(1, 1.0) ** 2 / pois(2, 2.0), "should be C(2,1)(1/2)^2 = 0.5")
# P3.3 exponential/typing
show("pq_33_lam", 12.0)
show("pq_33_P_gt_10min", math.exp(-12.0 * (10 / 60)))
show("pq_33_median_min", 60 * math.log(2) / 12.0)
# P3.4 Erlang
show("pq_34_mean", 4 / 3.0)
show("pq_34_var", 4 / 9.0)
show("pq_34_P_le_1", 1 - sum(pois(n, 3.0 * 1.0) for n in range(4)))
show("pq_34_scipy", float(stats.erlang.cdf(1.0, 4, scale=1 / 3.0)))
show("pq_34_dev", abs((1 - sum(pois(n, 3.0) for n in range(4)))
                      - float(stats.erlang.cdf(1.0, 4, scale=1 / 3.0))))
# P3.5 Bernoulli merge with 3 processes
p1, p2, p3 = F(1, 10), F(7, 100), F(1, 20)
merged = 1 - (1 - p1) * (1 - p2) * (1 - p3)
show("pq_35_merged", merged)
show("pq_35_merged_dec", float(merged))
show("pq_35_E", float(1 / merged))
show("pq_35_var", float((1 - merged) / merged ** 2))

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(R, indent=1), encoding="utf-8")
print(f"\nwrote {out}  ({len(R)} keys)")
