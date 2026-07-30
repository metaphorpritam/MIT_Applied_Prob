# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""G7 section 1 - estimators, bias, consistency, MSE, confidence intervals.

Every number quoted in notes/src/fragments/g7_s1.html is produced here.

Run:  uv run computes/g7_s1.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "g7_s1.json"

R: dict[str, float | int | str | list] = {}


def rec(key, val, note=""):
    if isinstance(val, (np.floating, np.integer)):
        val = val.item()
    R[key] = val
    print(f"{key:34s} = {val!r}   {note}")


print("=" * 78)
print("A.  Exponential ML estimator  Theta_n = n/(X_1+...+X_n):  bias and MSE")
print("=" * 78)
# X_i iid exponential(theta).  S_n = sum X_i ~ Erlang(n, theta), density
#   f_S(s) = theta^n s^(n-1) e^{-theta s}/(n-1)!,  s >= 0.
# E[1/S_n] = theta/(n-1) for n >= 2 ; E[1/S_n^2] = theta^2/((n-1)(n-2)) for n >= 3.
# Verified symbolically by the Gamma-integral identity and numerically below.
for n in (1, 2, 5, 10, 100):
    if n == 1:
        rec("A_E_inv_S_n1", "infinity", "E[1/X_1] diverges: int_0^inf (1/x) theta e^{-theta x} dx = inf")
        continue
    rec(f"A_Ehat_n{n}", n / (n - 1), f"E[Theta_n]/theta at n={n}")
    rec(f"A_bias_n{n}", 1 / (n - 1), f"bias/theta at n={n}")

# numeric check of E[1/S_n] = theta/(n-1) by quadrature, theta = 1, n = 5
from scipy import integrate

n, th = 5, 1.0
val, _ = integrate.quad(lambda s: (1 / s) * th**n * s ** (n - 1) * np.exp(-th * s) / float(math.factorial(n - 1)), 0, np.inf)
rec("A_quad_check_n5", round(float(val), 10), "quadrature E[1/S_5] vs theta/(n-1)=0.25")

# divergence check for n = 1: truncated integral grows without bound
for eps in (1e-2, 1e-4, 1e-8):
    v, _ = integrate.quad(lambda x: (1 / x) * np.exp(-x), eps, np.inf)
    rec(f"A_trunc_eps{eps:g}", round(float(v), 6), f"int_{eps}^inf (1/x)e^-x dx")

# variance and MSE of Theta_n for theta = 1
for n in (3, 5, 10, 100):
    var = n**2 / ((n - 1) ** 2 * (n - 2))
    bias2 = 1 / (n - 1) ** 2
    rec(f"A_var_n{n}", round(var, 6), f"var(Theta_n)/theta^2 at n={n}")
    rec(f"A_bias2_n{n}", round(bias2, 6), f"bias^2/theta^2 at n={n}")
    rec(f"A_mse_n{n}", round(var + bias2, 6), f"MSE/theta^2 at n={n}")

rng = np.random.default_rng(6041)
X = rng.exponential(scale=1.0, size=(400000, 5))
Th = 5.0 / X.sum(axis=1)
rec("A_sim_mean_n5", round(float(Th.mean()), 4), "simulated E[Theta_5], theory 1.25")
rec("A_sim_mse_n5", round(float(((Th - 1.0) ** 2).mean()), 4), "simulated MSE, theory 0.583333")

print()
print("=" * 78)
print("B.  MSE decomposition:  sample mean  M_n  vs  shrunk estimator  T_n = S_n/(n+1)")
print("=" * 78)
# X_i iid, mean theta, variance v.   M_n = S_n/n ,  T_n = S_n/(n+1)   (B&T Example 9.5)
nB, vB = 10, 1.0
rec("B_n", nB)
rec("B_v", vB)
rec("B_mse_M", round(vB / nB, 6), "MSE(M_n) = v/n, free of theta")
for th in (0.0, 0.5, 1.0, 1.449, 2.0, 3.0):
    bias = -th / (nB + 1)
    var = nB * vB / (nB + 1) ** 2
    rec(f"B_bias_th{th}", round(bias, 6))
    rec(f"B_var_T", round(var, 6), "var(T_n) = n v/(n+1)^2, free of theta")
    rec(f"B_mse_T_th{th}", round(var + bias**2, 6), f"MSE(T_n) at theta={th}")
cross = np.sqrt(vB * (2 * nB + 1) / nB)
rec("B_crossover", round(float(cross), 6), "|theta| below which MSE(T_n) < MSE(M_n): sqrt(v(2n+1)/n)")
rec("B_var_ratio", round(nB * vB / (nB + 1) ** 2 / (vB / nB), 6), "var(T_n)/var(M_n) = n^2/(n+1)^2")

# optimal shrinkage c* for c*M_n  (practice question)
th_p, v_p, n_p = 1.0, 1.0, 10
c_star = th_p**2 / (th_p**2 + v_p / n_p)
rec("B_cstar", round(float(c_star), 6), "c* = theta^2/(theta^2+v/n)")
rec("B_mse_cstar", round(float(c_star**2 * v_p / n_p + (c_star - 1) ** 2 * th_p**2), 6), "MSE at c*")
rec("B_mse_c1", round(v_p / n_p, 6), "MSE at c=1 (the sample mean)")

print()
print("=" * 78)
print("C.  The normal quantile z:  Phi(z) = 1 - alpha/2")
print("=" * 78)
rec("C_Phi_196", round(float(stats.norm.cdf(1.96)), 6), "Phi(1.96)")
rec("C_2Phi196_m1", round(float(2 * stats.norm.cdf(1.96) - 1), 7), "P(|Z| <= 1.96)")
for a in (0.25, 0.10, 0.05, 0.02, 0.01):
    z = float(stats.norm.ppf(1 - a / 2))
    rec(f"C_z_alpha{a}", round(z, 6), f"z for {100*(1-a):.0f}% CI")
rec("C_z_exact_005", round(float(stats.norm.ppf(0.975)), 6), "exact 97.5% quantile (1.96 is the rounded table value)")
rec("C_cover_at_196", round(float(2 * stats.norm.cdf(1.959964) - 1), 6), "coverage at the exact quantile")

print()
print("=" * 78)
print("D.  rec23 Problem 3 / B&T Example 9.8 - polling, three variance choices")
print("=" * 78)
nD, kD = 1200, 684
that = kD / nD
rec("D_n", nD)
rec("D_k", kD)
rec("D_thetahat", round(that, 6), "684/1200")
ssq_sum = kD * (1 - that) ** 2 + (nD - kD) * (0 - that) ** 2
rec("D_sumsq", round(float(ssq_sum), 6), "sum_i (x_i - thetahat)^2")
S2 = ssq_sum / (nD - 1)
rec("D_S2", round(float(S2), 8), "(a) sample variance with 1/(n-1)")
plug = that * (1 - that)
rec("D_plug", round(float(plug), 8), "(b) thetahat(1-thetahat)")
rec("D_bound", 0.25, "(c) conservative upper bound sigma^2 <= 1/4")
rec("D_S2_over_plug", round(float(S2 / plug), 8), "equals n/(n-1)")
rec("D_n_over_nm1", round(nD / (nD - 1), 8))
z95 = 1.96
for tag, v in (("a", float(S2)), ("b", float(plug)), ("c", 0.25)):
    se = np.sqrt(v / nD)
    hw = z95 * se
    rec(f"D_se_{tag}", round(float(se), 8), f"sqrt(v/n) for ({tag})")
    rec(f"D_hw_{tag}", round(float(hw), 6), f"half-width 1.96*sqrt(v/n) for ({tag})")
    rec(f"D_lo_{tag}", round(float(that - hw), 6))
    rec(f"D_hi_{tag}", round(float(that + hw), 6))
rec("D_hw_c_minus_b", round(float(1.96 * np.sqrt(0.25 / nD) - 1.96 * np.sqrt(plug / nD)), 8),
    "how much wider the conservative interval is")
rec("D_excludes_half", bool(that - 1.96 * np.sqrt(0.25 / nD) > 0.5), "does the widest CI exclude theta = 1/2?")

# small-n comparison for the (b) vs (c) figure (B&T its Figure 9.4)
for n_small in (10, 30, 100, 1000, 10000):
    hb = 1.96 * np.sqrt(plug / n_small)
    hc = 1.96 * np.sqrt(0.25 / n_small)
    rec(f"D_hwb_n{n_small}", round(float(hb), 6))
    rec(f"D_hwc_n{n_small}", round(float(hc), 6))
    rec(f"D_hwdiff_n{n_small}", round(float(hc - hb), 6))

print()
print("=" * 78)
print("E.  Bernoulli variance bound theta(1-theta) <= 1/4, and sample-size design")
print("=" * 78)
# maximize g(theta) = theta(1-theta) over [0,1] on a fine grid, as a check on the
# calculus argument g'(theta) = 1 - 2theta = 0 at theta = 1/2
_grid = np.linspace(0.0, 1.0, 1000001)
_gvals = _grid * (1 - _grid)
rec("E_bern_max_var", round(float(_gvals.max()), 6), "max of theta(1-theta) over [0,1]  (= 1/4)")
rec("E_bern_argmax", round(float(_grid[int(np.argmax(_gvals))]), 6), "argmax, i.e. theta = 1/2")
rec("E_bern_max_sd", round(float(np.sqrt(_gvals.max())), 6), "max standard deviation sigma = 1/2")
for th in (0.1, 0.3, 0.5, 0.57):
    rec(f"E_bern_var_{th}", round(float(th * (1 - th)), 6), f"theta(1-theta) at theta={th}")
for margin in (0.05, 0.03, 0.01, 0.005):
    n_need = (1.96**2) * 0.25 / margin**2
    rec(f"E_n_margin{margin}", int(np.ceil(n_need)), f"n for +/-{margin} at 95%")
rec("E_rule_1oversqrtn_1200", round(float(1 / np.sqrt(1200)), 6), "the '1/sqrt(n)' rule of thumb at n=1200")
rec("E_hw_c_1200", round(float(1.96 * np.sqrt(0.25 / 1200)), 6), "exact conservative half-width at n=1200")
rec("E_quadruple", 4, "halving the margin multiplies n by 4")

print()
print("=" * 78)
print("F.  Sample variance:  E[sigmahat_n^2] and E[S_n^2]")
print("=" * 78)
for n in (2, 5, 10, 100):
    rec(f"F_biasfac_n{n}", round((n - 1) / n, 6), "E[(1/n)sum(X_i-M_n)^2] = (n-1)v/n")
    rec(f"F_pct_low_n{n}", round(100 * (1 - (n - 1) / n), 4), "percent understatement at v=1")
# simulation check, normal(0,1), n = 5
Z = rng.normal(0, 1, size=(400000, 5))
M = Z.mean(axis=1, keepdims=True)
sq = ((Z - M) ** 2).sum(axis=1)
rec("F_sim_div_n", round(float((sq / 5).mean()), 5), "simulated E[(1/n)sum], theory 0.8")
rec("F_sim_div_nm1", round(float((sq / 4).mean()), 5), "simulated E[(1/(n-1))sum], theory 1.0")

print()
print("=" * 78)
print("G.  Coverage: exact for normal data, empirical for Bernoulli data")
print("=" * 78)
# G1: normal data, sigma known -> coverage is exactly 2*Phi(1.96)-1
rec("G_normal_exact", round(float(2 * stats.norm.cdf(1.96) - 1), 6), "exact coverage, normal data, known sigma")

# G2: Bernoulli data, plug-in variance, 95% nominal -> Monte Carlo coverage
theta_true = 0.57
NS = 200000
for n in (5, 10, 30, 100, 1000):
    s = rng.binomial(n, theta_true, size=NS) / n
    v = s * (1 - s)
    hw = 1.96 * np.sqrt(v / n)
    cov = float(np.mean((s - hw <= theta_true) & (theta_true <= s + hw)))
    rec(f"G_cov_plug_n{n}", round(cov, 4), f"empirical coverage, plug-in variance, theta=0.57, n={n}")
    hw_c = 1.96 * np.sqrt(0.25 / n)
    cov_c = float(np.mean((s - hw_c <= theta_true) & (theta_true <= s + hw_c)))
    rec(f"G_cov_bound_n{n}", round(cov_c, 4), f"empirical coverage, 1/4 bound, n={n}")

# worst-case for the plug-in at small n: theta near 0
s = rng.binomial(20, 0.03, size=NS) / 20
v = s * (1 - s)
hw = 1.96 * np.sqrt(v / 20)
rec("G_cov_plug_n20_th003", round(float(np.mean((s - hw <= 0.03) & (0.03 <= s + hw))), 4),
    "plug-in coverage collapses for theta=0.03, n=20")
rec("G_p_allzero_n20_th003", round(float(0.97**20), 6), "P(no successes) -> degenerate zero-width interval")

print()
print("=" * 78)
print("H.  The 100-interval coverage picture (Fig 1.2 data)")
print("=" * 78)
mu, sig, nH, reps = 10.0, 2.0, 25, 100
rg2 = np.random.default_rng(2010)
samp = rg2.normal(mu, sig, size=(reps, nH))
mn = samp.mean(axis=1)
hw = 1.96 * sig / np.sqrt(nH)
miss = int(np.sum((mn - hw > mu) | (mu > mn + hw)))
rec("H_mu", mu)
rec("H_sigma", sig)
rec("H_n", nH)
rec("H_halfwidth", round(float(hw), 6), "1.96*sigma/sqrt(n)")
rec("H_reps", reps)
rec("H_misses", miss, "intervals out of 100 that miss mu (seed 2010)")
rec("H_hits", reps - miss)
big = rg2.normal(mu, sig, size=(200000, nH)).mean(axis=1)
rec("H_longrun", round(float(np.mean(np.abs(big - mu) <= hw)), 5), "long-run coverage over 200000 replications")

print()
print("=" * 78)
print("I.  B&T Example 9.7 - t vs normal at n = 8 (aside; t-CIs are not examinable)")
print("=" * 78)
w = np.array([0.5547, 0.5404, 0.6364, 0.6438, 0.4917, 0.5674, 0.5564, 0.6066])
nI = len(w)
mI = w.mean()
S2I = w.var(ddof=1)
rec("I_n", nI)
rec("I_mean", round(float(mI), 6))
rec("I_S2", round(float(S2I), 8), "sample variance, 1/(n-1)")
rec("I_S2_over_n", round(float(S2I / nI), 10), "estimated variance of the sample mean")
rec("I_se", round(float(np.sqrt(S2I / nI)), 6), "S_n/sqrt(n)")
rec("I_t7", round(float(stats.t.ppf(0.975, nI - 1)), 6), "t quantile, 7 d.o.f.")
rec("I_t_lo", round(float(mI - stats.t.ppf(0.975, nI - 1) * np.sqrt(S2I / nI)), 4))
rec("I_t_hi", round(float(mI + stats.t.ppf(0.975, nI - 1) * np.sqrt(S2I / nI)), 4))
rec("I_z_lo", round(float(mI - 1.96 * np.sqrt(S2I / nI)), 4))
rec("I_z_hi", round(float(mI + 1.96 * np.sqrt(S2I / nI)), 4))
rec("I_width_ratio", round(float(stats.t.ppf(0.975, nI - 1) / 1.96), 4), "t interval is this many times wider")

print()
print("=" * 78)
print("J.  Practice-question numbers")
print("=" * 78)
# J1: uniform [0,theta]; moment estimator 2 M_n
th_J, n_J = 1.0, 12
rec("J_unif_var_X", round(th_J**2 / 12, 8), "var of uniform[0,theta] = theta^2/12")
rec("J_unif_mse_2M", round(th_J**2 / (3 * n_J), 8), f"MSE(2M_n) = theta^2/(3n) at n={n_J}")
# ML estimator max X_i:  E = n theta/(n+1),  MSE = 2 theta^2/((n+1)(n+2))
rec("J_unif_E_max", round(n_J / (n_J + 1), 6), "E[max]/theta")
rec("J_unif_mse_max", round(2 / ((n_J + 1) * (n_J + 2)), 8), "MSE(max)/theta^2")
rec("J_unif_ratio", round((th_J**2 / (3 * n_J)) / (2 / ((n_J + 1) * (n_J + 2))), 4), "MSE(2M_n)/MSE(max)")

# J2: single-observation estimator X_1 - unbiased, not consistent
rec("J_X1_var", 1.0, "var(X_1) = sigma^2, never shrinks -> not consistent")
# J3: M_n + 1/n - biased, consistent
for n in (10, 100, 1000):
    rec(f"J_shift_bias_n{n}", round(1 / n, 6), "bias of M_n + 1/n")

# J4: bulb lifetimes CI
xbar, sd, n_J4 = 1180.0, 240.0, 64
se4 = sd / np.sqrt(n_J4)
rec("J4_se", round(float(se4), 6))
for lev, z in (("90", float(stats.norm.ppf(0.95))), ("95", 1.96), ("99", float(stats.norm.ppf(0.995)))):
    rec(f"J4_z{lev}", round(z, 6))
    rec(f"J4_lo{lev}", round(float(xbar - z * se4), 3))
    rec(f"J4_hi{lev}", round(float(xbar + z * se4), 3))
    rec(f"J4_width{lev}", round(float(2 * z * se4), 3))
rec("J4_n_for_width40", int(np.ceil((2 * 1.96 * sd / 40) ** 2)), "n so the 95% CI has total width 40")

# J5: coin, 40 heads in 100
n5, k5 = 100, 40
t5 = k5 / n5
rec("J5_thetahat", t5)
rec("J5_plug_v", round(float(t5 * (1 - t5)), 6))
rec("J5_hw_plug", round(float(1.96 * np.sqrt(t5 * (1 - t5) / n5)), 6))
rec("J5_lo_plug", round(float(t5 - 1.96 * np.sqrt(t5 * (1 - t5) / n5)), 6))
rec("J5_hi_plug", round(float(t5 + 1.96 * np.sqrt(t5 * (1 - t5) / n5)), 6))
rec("J5_hw_bound", round(float(1.96 * np.sqrt(0.25 / n5)), 6))
rec("J5_lo_bound", round(float(t5 - 1.96 * np.sqrt(0.25 / n5)), 6))
rec("J5_hi_bound", round(float(t5 + 1.96 * np.sqrt(0.25 / n5)), 6))
rec("J5_excludes_half_plug", bool(t5 + 1.96 * np.sqrt(t5 * (1 - t5) / n5) < 0.5))
rec("J5_excludes_half_bound", bool(t5 + 1.96 * np.sqrt(0.25 / n5) < 0.5))

# J7: Practice 1.10 - second poll, n = 400, thetahat = 0.90
n7, t7 = 400, 0.90
rec("J7_plug_v", round(float(t7 * (1 - t7)), 6), "plug-in variance 0.9*0.1")
rec("J7_hw_plug", round(float(1.96 * np.sqrt(t7 * (1 - t7) / n7)), 6), "plug-in 95% margin")
rec("J7_hw_bound", round(float(1.96 * np.sqrt(0.25 / n7)), 6), "conservative 95% margin")
rec("J7_ratio", round(float(np.sqrt(0.25 / (t7 * (1 - t7)))), 6), "ratio of the two margins")
rec("J7_var_ratio", round(float(0.25 / (t7 * (1 - t7))), 6), "ratio of the two variances")
rec("J7_npq", round(float(n7 * t7 * (1 - t7)), 6), "n*thetahat*(1-thetahat), CLT adequacy check")

# J8: Practice 1.5 - weighings needed for a target standard error
sd8 = 0.02
for tgt in (0.005, 0.001):
    rec(f"J8_n_for_se{tgt}", int(np.ceil((sd8 / tgt) ** 2)), f"n so that sigma/sqrt(n) <= {tgt}")

# J6: MSE of the "always zero" estimator (B&T remark)
rec("J6_mse_zero_th2", 4.0, "MSE of Thetahat = 0 at theta = 2 is theta^2 = 4")
rec("J6_mse_M_n25_v1", round(1.0 / 25, 6), "MSE(M_25) with v = 1")

print()
print("=" * 78)
print("K.  Gaussian ML = sample mean (L23 slide 5 unsolved example) - numeric check")
print("=" * 78)
xs = np.array([2.1, 3.4, 1.8, 2.9, 3.3])
rec("K_data", [float(v) for v in xs])
rec("K_samplemean", round(float(xs.mean()), 6))
grid = np.linspace(xs.mean() - 2, xs.mean() + 2, 400001)
ll = -0.5 * ((xs[None, :] - grid[:, None]) ** 2).sum(axis=1)  # sigma = 1, constants dropped
rec("K_grid_argmax", round(float(grid[int(np.argmax(ll))]), 6), "numerical argmax of the log-likelihood")
rec("K_matches", bool(abs(grid[int(np.argmax(ll))] - xs.mean()) < 1e-4))

print()
print("=" * 78)
print("L.  Sample-mean spread, and Chebyshev vs CLT confidence intervals")
print("=" * 78)
for n in (1, 4, 25, 100, 400, 1600):
    rec(f"L_se_n{n}", round(1.0 / np.sqrt(n), 6), f"sigma/sqrt(n) with sigma=1, n={n}")
rec("L_quadruple_halves", 0.5, "n -> 4n halves the standard error")
# Chebyshev interval:  P(|M_n - theta| >= c) <= sigma^2/(n c^2) = alpha  =>  c = sigma/sqrt(alpha n)
for a in (0.05, 0.01):
    kcheb = 1 / np.sqrt(a)
    kclt = float(stats.norm.ppf(1 - a / 2))
    rec(f"L_cheb_k_alpha{a}", round(float(kcheb), 6), f"Chebyshev multiplier 1/sqrt(alpha), alpha={a}")
    rec(f"L_clt_k_alpha{a}", round(kclt, 6), f"CLT multiplier z, alpha={a}")
    rec(f"L_ratio_alpha{a}", round(float(kcheb / kclt), 4), "Chebyshev interval is this many times wider")
    rec(f"L_narea_alpha{a}", round(float((kcheb / kclt) ** 2), 4), "equivalently this many times more data")
# true coverage of the Chebyshev interval for normal data at alpha = 0.05
rec("L_cheb_true_cover_005", round(float(2 * stats.norm.cdf(1 / np.sqrt(0.05)) - 1), 6),
    "actual coverage of the Chebyshev 95% interval when the data are normal")

print()
print("=" * 78)
print("M.  Accuracy check of the widget's own z-lookup (A&S 7.1.26 erf + bisection)")
print("=" * 78)


def erf_as(x):
    """Abramowitz-Stegun 7.1.26, the formula coded inside the widget."""
    sgn = -1.0 if x < 0 else 1.0
    x = abs(x)
    t = 1.0 / (1.0 + 0.3275911 * x)
    y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
                - 0.284496736) * t + 0.254829592) * t * math.exp(-x * x)
    return sgn * y


def phi_as(z):
    return 0.5 * (1.0 + erf_as(z / math.sqrt(2.0)))


def zfor_as(conf):
    """Bisection inverse used by the widget: Phi(z) = 1 - alpha/2."""
    target = 1.0 - (1.0 - conf) / 2.0
    lo, hi = 0.0, 6.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if phi_as(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


worst = 0.0
for conf in (0.50, 0.75, 0.80, 0.90, 0.95, 0.98, 0.99):
    za = zfor_as(conf)
    ze = float(stats.norm.ppf(1 - (1 - conf) / 2))
    worst = max(worst, abs(za - ze))
    rec(f"M_z_widget_{int(conf*100)}", round(za, 6), f"widget z at {conf:.0%}")
    rec(f"M_z_scipy_{int(conf*100)}", round(ze, 6), f"scipy z at {conf:.0%}")
rec("M_worst_abs_error", float(f"{worst:.3g}"), "largest |widget z - exact z| over the table")

OUT.write_text(json.dumps(R, indent=1), encoding="utf-8")
print()
print("wrote", OUT, "with", len(R), "keys")
