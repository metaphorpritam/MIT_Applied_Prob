# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Numbers for G4 section 4 — Poisson process II: merging, splitting, random incidence.

Sources: L15 slides 3-8, rec15 problems 1-3, B&T 6.2.
Run:  uv run computes/g4_s4.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
from scipy import integrate, stats

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "computes" / "g4_s4.json"
R: dict[str, object] = {}


def rec(key, val, note=""):
    R[key] = val
    if isinstance(val, float):
        print(f"{key:34s} = {val:.6f}   {note}")
    else:
        print(f"{key:34s} = {val}   {note}")


print("=" * 74)
print("A. Poisson fishing  (L15 slide 3), lambda = 0.6 / hour")
print("=" * 74)
lam = 0.6
rec("fish_lambda", lam)
rec("fish_lam_t2", lam * 2, "lambda*2 = expected catch in 2 hrs")
p0_2 = math.exp(-lam * 2)
rec("fish_a_P_more_than_2", p0_2, "P(N_2 = 0) = e^{-1.2}")
p_no_catch_3more = math.exp(-lam * 3)
rec("fish_exp_m18", p_no_catch_3more, "e^{-1.8}")
rec("fish_b_between_2_and_5", p0_2 * (1 - p_no_catch_3more), "e^{-1.2}(1-e^{-1.8})")
p1_2 = lam * 2 * math.exp(-lam * 2)
rec("fish_P_N2_eq_1", p1_2, "1.2 e^{-1.2}")
rec("fish_P_N2_le_1", p0_2 + p1_2, "2.2 e^{-1.2}")
rec("fish_c_at_least_two", 1 - (p0_2 + p1_2), "1 - 2.2 e^{-1.2}")
rec("fish_d_E_num_fish", lam * 2 + p0_2, "E[max(N_2,1)] = 1.2 + e^{-1.2}")
rec("fish_e_future_time", 1 / lam, "memorylessness: 1/lambda")
rec("fish_f_E_total_time", 2 + p0_2 / lam, "2 + e^{-1.2}/lambda")

# Monte-Carlo cross-check of (c),(d),(f)
rng = np.random.default_rng(6041)
NS = 400_000
n2 = rng.poisson(lam * 2, NS)
extra = rng.exponential(1 / lam, NS)
fish_count = np.maximum(n2, 1)
total_time = np.where(n2 >= 1, 2.0, 2.0 + extra)
rec("fish_mc_c_at_least_two", float(np.mean(n2 >= 2)))
rec("fish_mc_d_E_num_fish", float(np.mean(fish_count)))
rec("fish_mc_f_E_total_time", float(np.mean(total_time)))

print()
print("=" * 74)
print("B. Merging / competing exponentials  (L15 slide 4, rec15 P3, B&T Example 6.15)")
print("=" * 74)
l1, l2 = 2.0, 3.0
rec("merge_lam1", l1)
rec("merge_lam2", l2)
rec("merge_lam_sum", l1 + l2)
rec("merge_p_first_from_1", l1 / (l1 + l2), "lambda1/(lambda1+lambda2)")
rec("merge_p_first_from_2", l2 / (l1 + l2))
rec("merge_E_min", 1 / (l1 + l2), "E[min] = 1/(l1+l2)")
T1 = rng.exponential(1 / l1, NS)
T2 = rng.exponential(1 / l2, NS)
rec("merge_mc_p_first_from_1", float(np.mean(T1 < T2)))
rec("merge_mc_E_min", float(np.mean(np.minimum(T1, T2))))
# exact integral P(T1 < T2)
val, err = integrate.quad(lambda t: l1 * math.exp(-l1 * t) * math.exp(-l2 * t), 0, np.inf)
rec("merge_int_p_first_from_1", float(val), f"quad, abserr={err:.2e}")

print()
print("=" * 74)
print("C. Light bulb example  (L15 slide 5, B&T Example 6.16), lambda = 1")
print("=" * 74)
lb = 1.0
rec("bulb_lambda", lb)
rec("bulb_stage1", 1 / (3 * lb), "1/(3 lambda)")
rec("bulb_stage2", 1 / (2 * lb), "1/(2 lambda)")
rec("bulb_stage3", 1 / lb, "1/lambda")
rec("bulb_E_total", 1 / (3 * lb) + 1 / (2 * lb) + 1 / lb, "= 11/(6 lambda)")
rec("bulb_E_total_coeff", 11 / 6, "coefficient of 1/lambda")
rec("bulb_var_total", 1 / (9 * lb ** 2) + 1 / (4 * lb ** 2) + 1 / lb ** 2, "= 49/(36 lambda^2)")
rec("bulb_var_coeff", 49 / 36)
mx = np.maximum.reduce([rng.exponential(1 / lb, NS) for _ in range(3)])
rec("bulb_mc_E_total", float(np.mean(mx)))
rec("bulb_mc_var_total", float(np.var(mx)))

print()
print("=" * 74)
print("D. Splitting  (L15 slide 6, B&T Example 6.13): independence of the streams")
print("=" * 74)
lam_s, p_s, tau_s = 5.0, 0.3, 2.0
rec("split_lambda", lam_s)
rec("split_p", p_s)
rec("split_tau", tau_s)
rec("split_rate_usa", p_s * lam_s)
rec("split_rate_foreign", (1 - p_s) * lam_s)
rec("split_mean_usa", p_s * lam_s * tau_s, "p lambda tau")
rec("split_mean_foreign", (1 - p_s) * lam_s * tau_s)
NTOT = rng.poisson(lam_s * tau_s, NS)
K = rng.binomial(NTOT, p_s)
M = NTOT - K
rec("split_mc_mean_usa", float(np.mean(K)))
rec("split_mc_var_usa", float(np.var(K)))
rec("split_mc_corr", float(np.corrcoef(K, M)[0, 1]), "corr(K,M) ~ 0  => independent")
# exact joint vs product check at (k,m) = (2,5)
k0, m0 = 2, 5
pj = math.exp(-lam_s * tau_s) * (lam_s * tau_s) ** (k0 + m0) / math.factorial(k0 + m0) \
    * math.comb(k0 + m0, k0) * p_s ** k0 * (1 - p_s) ** m0
pk = stats.poisson.pmf(k0, p_s * lam_s * tau_s)
pm = stats.poisson.pmf(m0, (1 - p_s) * lam_s * tau_s)
rec("split_joint_25", float(pj))
rec("split_marg_k2", float(pk))
rec("split_marg_m5", float(pm))
rec("split_prod_25", float(pk * pm))
rec("split_joint_minus_prod", float(pj - pk * pm), "0 => exact independence")

print()
print("=" * 74)
print("E. Random incidence for Poisson  (L15 slide 7, B&T 6.2 its Figure 6.7)")
print("=" * 74)
lam_r = 0.5
rec("ri_lambda", lam_r)
rec("ri_mean_typical", 1 / lam_r, "1/lambda = mean of a *numbered* interval")
rec("ri_mean_seen", 2 / lam_r, "2/lambda = mean of the interval containing t*")
rec("ri_var_seen", 2 / lam_r ** 2, "Erlang(2) variance 2/lambda^2")
rec("ri_ratio", 2.0, "seen mean / typical mean")
rec("ri_erlang2_mode", 1 / lam_r, "mode of Erlang(2) is 1/lambda")
# simulation: run a process, drop a pin, measure containing interval
T_END, N_PIN = 400_000.0, 400_000
gaps = rng.exponential(1 / lam_r, int(lam_r * T_END * 1.4))
times = np.cumsum(gaps)
times = times[times < T_END]
pins = rng.uniform(times[0], times[-1], N_PIN)
idx = np.searchsorted(times, pins)
L = times[idx] - times[idx - 1]
rec("ri_mc_mean_seen", float(np.mean(L)))
rec("ri_mc_var_seen", float(np.var(L)))
rec("ri_mc_mean_forward", float(np.mean(times[idx] - pins)), "V - t*  ~ Exp(lambda)")
rec("ri_mc_mean_backward", float(np.mean(pins - times[idx - 1])), "t* - U ~ Exp(lambda)")
rec("ri_mc_mean_all_gaps", float(np.mean(np.diff(times))), "plain average of all gaps = 1/lambda")
# KS-style check against Erlang(2)
rec("ri_ks_stat_erlang2", float(stats.kstest(L, lambda x: stats.gamma.cdf(x, 2, scale=1 / lam_r)).statistic))
rec("ri_ks_stat_expon", float(stats.kstest(L, lambda x: stats.expon.cdf(x, scale=1 / lam_r)).statistic))
# P(L > 2/lambda) under the two laws
rec("ri_P_L_gt_2overlam_erlang", float(1 - stats.gamma.cdf(2 / lam_r, 2, scale=1 / lam_r)), "3e^{-2}")
rec("ri_P_L_gt_2overlam_expon", float(math.exp(-2)), "e^{-2}")

print()
print("=" * 74)
print("F. Renewal random incidence: buses 5 or 10 min, equally likely (L15 slide 8)")
print("=" * 74)
a, b = 5.0, 10.0
rec("bus_len_a", a)
rec("bus_len_b", b)
rec("bus_mean_interarrival", 0.5 * a + 0.5 * b, "unbiased mean interarrival")
den = 0.5 * a + 0.5 * b
rec("bus_P_pick_5", 0.5 * a / den, "5*(1/2)/7.5")
rec("bus_P_pick_10", 0.5 * b / den)
rec("bus_E_selected_len", (0.5 * a * a + 0.5 * b * b) / den, "E[L^2]/E[L]")
rec("bus_E_wait_given_5", a / 2)
rec("bus_E_wait_given_10", b / 2)
ew = (0.5 * a / den) * (a / 2) + (0.5 * b / den) * (b / 2)
rec("bus_E_wait", ew, "(1/3)(5/2)+(2/3)(10/2) = 25/6")
rec("bus_E_wait_naive", den / 2, "wrong answer: half the mean interarrival")
rec(
    "bus_naive_shortfall_pct",
    100.0 * (ew - den / 2) / ew,
    "(25/6 - 3.75)/(25/6) in percent -- shortfall relative to the TRUE wait",
)
# simulation
NB = 300_000
lens = rng.choice([a, b], size=NB)
edges = np.concatenate([[0.0], np.cumsum(lens)])
pins = rng.uniform(edges[10], edges[-10], 300_000)
j = np.searchsorted(edges, pins)
sel = edges[j] - edges[j - 1]
rec("bus_mc_P_pick_5", float(np.mean(sel == a)))
rec("bus_mc_E_selected_len", float(np.mean(sel)))
rec("bus_mc_E_wait", float(np.mean(edges[j] - pins)))

print()
print("Erlang(2) renewal process (B&T Problem 27): observed interval should be Erlang(3)")
lam_e = 1.0
rec("erl_lambda", lam_e)
rec("erl_interarrival_mean", 2 / lam_e, "Erlang(2) mean")
rec("erl_seen_mean_theory", 3 / lam_e, "Erlang(3) mean")
rec("erl_ratio", 1.5)
gaps_e = rng.gamma(2, 1 / lam_e, 400_000)
edges_e = np.concatenate([[0.0], np.cumsum(gaps_e)])
pins_e = rng.uniform(edges_e[10], edges_e[-10], 300_000)
je = np.searchsorted(edges_e, pins_e)
sel_e = edges_e[je] - edges_e[je - 1]
rec("erl_mc_seen_mean", float(np.mean(sel_e)))
rec("erl_ks_vs_erlang3", float(stats.kstest(sel_e, lambda x: stats.gamma.cdf(x, 3, scale=1 / lam_e)).statistic))

print()
print("B&T 6.2 book variant: 5 min or 55 min, equally likely")
a2, b2 = 5.0, 55.0
den2 = 0.5 * a2 + 0.5 * b2
rec("bt_bus_mean_interarrival", den2)
rec("bt_bus_P_pick_5", 0.5 * a2 / den2, "= 1/12")
rec("bt_bus_P_pick_55", 0.5 * b2 / den2, "= 11/12")
rec("bt_bus_E_selected_len", (0.5 * a2 * a2 + 0.5 * b2 * b2) / den2, "5/12 + 55*11/12")
rec("bt_bus_E_wait", 0.5 * (0.5 * a2 * a2 + 0.5 * b2 * b2) / den2)

print()
print("=" * 74)
print("G. rec15 P1 — type-A / type-B bulbs (B&T Problem 6.14)")
print("=" * 74)
lA, lB = 1.0, 3.0
rec("p1_lamA", lA)
rec("p1_lamB", lB)
rec("p1_a_E_first_failure", 0.5 * (1 / lA) + 0.5 * (1 / lB), "1/2 + 1/6 = 2/3")
t_ex = 1.0
rec("p1_t_example", t_ex)
pD = 0.5 * math.exp(-lA * t_ex) + 0.5 * math.exp(-lB * t_ex)
rec("p1_b_PD_at_t1", pD, "(1/2)e^{-1}+(1/2)e^{-3}")
rec("p1_c_PA_given_D_at_t1", 0.5 * math.exp(-lA * t_ex) / pD, "1/(1+e^{-2})")
rec("p1_c_closed_form_t1", 1 / (1 + math.exp(-2 * t_ex)))
rec("p1_d_split_pA", lA / (lA + lB), "1/4")
rec("p1_d_split_pB", lB / (lA + lB), "3/4")
rec("p1_d_answer", lA / (lA + lB) + (lB / (lA + lB)) * (lA / (lA + lB)), "1/4 + 3/4*1/4 = 7/16")
# integral route
f = lambda y: 9 * y * math.exp(-3 * y) * (1 - math.exp(-y))
val, err = integrate.quad(f, 0, np.inf)
rec("p1_d_integral", float(val), f"int 9y e^{{-3y}}(1-e^{{-y}}) dy, abserr={err:.1e}")
rec("p1_d_term_1_9", 1 / 9)
rec("p1_d_term_1_16", 1 / 16)
rec("p1_d_9x", 9 * (1 / 9 - 1 / 16))
XA = rng.exponential(1 / lA, NS)
YB = rng.exponential(1 / lB, NS) + rng.exponential(1 / lB, NS)
rec("p1_d_mc", float(np.mean(YB > XA)))
rec("p1_e_EN", 12 * 0.5)
rec("p1_e_varN", 12 * 0.5 * 0.5)
rec("p1_e_EX", 1 / lB)
rec("p1_e_varX", 1 / lB ** 2)
rec("p1_e_EV", (12 * 0.5) * (1 / lB), "E[N]E[X]")
rec("p1_e_varV", (1 / lB ** 2) * (12 * 0.5) + (1 / lB) ** 2 * (12 * 0.5 * 0.5), "var(X)E[N]+E[X]^2 var(N)")
Nb = rng.binomial(12, 0.5, NS)
V = rng.gamma(Nb, 1 / lB)
rec("p1_e_mc_EV", float(np.mean(V)))
rec("p1_e_mc_varV", float(np.var(V)))
pAD = 1 / (1 + math.exp(-2 * t_ex))
rec("p1_f_ET_given_D_t1", t_ex + 1 / 3 + (2 / 3) * pAD, "t + 1/3 + (2/3)/(1+e^{-2t})")
rec("p1_f_check_direct", t_ex + 1.0 * pAD + (1 / 3) * (1 - pAD))

print()
print("=" * 74)
print("H. rec15 P2 — service station (B&T Problem 6.15)")
print("=" * 74)
lA2, lB2 = 3.0, 4.0
rec("p2_lamA", lA2)
rec("p2_lamB", lB2)
rec("p2_lam_total", lA2 + lB2)
rec("p2_a_mean", 3 * (lA2 + lB2), "3 minutes * 7")
rec("p2_a_var", 3 * (lA2 + lB2))
rec("p2_a_pmf_at_21", float(stats.poisson.pmf(21, 21)), "p_N(21)")
pa = lA2 / (lA2 + lB2)
rec("p2_pA", pa, "3/7")
rec("p2_b_answer", float(stats.binom.pmf(3, 10, pa)), "C(10,3)(3/7)^3(4/7)^7")
rec("p2_b_binom_coef", math.comb(10, 3))
rec("p2_b_pa3", pa ** 3)
rec("p2_b_pb7", (1 - pa) ** 7)
rec("p2_c_pmf_at_0", pa, "(3/7)(4/7)^0")
rec("p2_c_pmf_at_1", pa * (1 - pa))
rec("p2_c_pmf_at_2", pa * (1 - pa) ** 2)
rec("p2_c_mean", (1 - pa) / pa, "E[K-1] = (1-p)/p = 4/3")

print()
print("=" * 74)
print("I. rec15 P3 — P(X < Y < Z) for three independent exponentials")
print("=" * 74)
lx, my, nz = 1.0, 2.0, 3.0
rec("p3_lambda", lx)
rec("p3_mu", my)
rec("p3_nu", nz)
rec("p3_P_Y_lt_Z", my / (my + nz), "mu/(mu+nu)")
rec("p3_P_X_lt_min", lx / (lx + my + nz), "lambda/(lambda+mu+nu)")
ans = lx * my / ((lx + my + nz) * (my + nz))
rec("p3_answer", ans, "lambda mu / ((l+m+n)(m+n))")
X_ = rng.exponential(1 / lx, NS)
Y_ = rng.exponential(1 / my, NS)
Z_ = rng.exponential(1 / nz, NS)
rec("p3_mc", float(np.mean((X_ < Y_) & (Y_ < Z_))))
inner = lambda y: my * math.exp(-my * y) * (1 - math.exp(-lx * y)) * math.exp(-nz * y)
val, err = integrate.quad(inner, 0, np.inf)
rec("p3_integral", float(val), f"triple integral collapsed, abserr={err:.1e}")

print()
print("=" * 74)
print("J. Practice-question numbers")
print("=" * 74)
# Practice 4.1: two servers rates 1/min and 4/min, merged
rec("pr1_lam1", 1.0)
rec("pr1_lam2", 4.0)
rec("pr1_merged", 5.0)
rec("pr1_p_first_from_slow", 1 / 5)
rec("pr1_P_exactly2_in_30s", float(stats.poisson.pmf(2, 5 * 0.5)), "Poisson(2.5) at 2")
rec("pr1_P_both_from_fast_given_2", (4 / 5) ** 2, "0.8^2")
# Practice 4.2: splitting, taxi 12/hr, 1/4 free
rec("pr2_lam", 12.0)
rec("pr2_p", 0.25)
rec("pr2_free_rate", 3.0)
rec("pr2_E_wait_free", 1 / 3.0, "hours = 20 min")
rec("pr2_E_wait_free_min", 60 / 3.0)
rec("pr2_P_no_free_in_1h", float(math.exp(-3.0)))
rec("pr2_P_3_occupied_before_first_free", 0.75 ** 3 * 0.25, "geometric")
# Practice 4.3: random incidence, lambda = 4/hr
rec("pr3_lam", 4.0)
rec("pr3_typical_mean_min", 60 / 4.0)
rec("pr3_seen_mean_min", 2 * 60 / 4.0)
rec("pr3_P_seen_gt_30min", float(1 - stats.gamma.cdf(0.5, 2, scale=1 / 4.0)), "P(Erlang2 > 0.5 hr)")
rec("pr3_P_typical_gt_30min", float(math.exp(-2.0)))
# Practice: renewal incidence with 1,2,6 min equally likely
ls = np.array([1.0, 2.0, 6.0])
ps = np.array([1 / 3, 1 / 3, 1 / 3])
mu_l = float(ls @ ps)
rec("pr4_mean_interarrival", mu_l)
bias = ls * ps / mu_l
rec("pr4_P_pick_1", float(bias[0]))
rec("pr4_P_pick_2", float(bias[1]))
rec("pr4_P_pick_6", float(bias[2]))
rec("pr4_E_selected", float(ls @ bias))
rec("pr4_E_wait", float((ls / 2) @ bias))
rec("pr4_E_wait_naive", mu_l / 2)
rec(
    "pr4_naive_shortfall_pct",
    100.0 * (float((ls / 2) @ bias) - mu_l / 2) / float((ls / 2) @ bias),
    "(41/18 - 1.5)/(41/18) in percent -- shortfall relative to the TRUE wait",
)
# fishing practice
rec("fish_pr_P_exactly_one_fish", p0_2 + p1_2, "N=1 iff N_2 <= 1")
rec("fish_pr_E_T_given_more_than_2", 2 + 1 / lam, "memorylessness")
rec("pr1_E_min_sec", 60 / 5.0, "seconds")
rec("pr3_P_backward_gt_15min", float(math.exp(-4.0 * 0.25)), "e^{-1}")
rec("split_cov_given_N10", -10 * p_s * (1 - p_s), "cov(K,M | N=10) = -n p q")

print()
print("=" * 74)
print("K. Widget cross-check: random-incidence simulator (lambda sweep)")
print("=" * 74)
wid = {}
for lw in (0.5, 1.0, 2.0, 4.0):
    g = rng.exponential(1 / lw, 60000)
    tt = np.cumsum(g)
    pn = rng.uniform(tt[5], tt[-5], 120000)
    ii = np.searchsorted(tt, pn)
    LL = tt[ii] - tt[ii - 1]
    wid[str(lw)] = {"mc_mean_seen": float(np.mean(LL)), "theory_seen": 2 / lw,
                    "mc_mean_gap": float(np.mean(np.diff(tt))), "theory_gap": 1 / lw}
    print(f"  lambda={lw:<4}  seen mean {np.mean(LL):.4f} (theory {2/lw:.4f})   "
          f"plain gap mean {np.mean(np.diff(tt)):.4f} (theory {1/lw:.4f})")
R["widget_incidence_sweep"] = wid
# Erlang(2) pdf peak value used for widget y-limit, lambda=1
rec("widget_erlang2_peak_lam1", float(stats.gamma.pdf(1.0, 2, scale=1.0)), "lambda^2 x e^{-lambda x} at x=1/lambda")

OUT.write_text(json.dumps(R, indent=1), encoding="utf-8")
print()
print("wrote", OUT, f"({len(R)} keys)")
