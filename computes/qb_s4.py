# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Question bank section 4 (Iterated expectations & arrival processes, Q73-Q94).

Every number that appears in notes/src/fragments/qb_s4.html is computed here.
Monte-Carlo cross-checks for the subtle items (random sums, split-stream
independence, competing exponentials, random incidence, mixed Poisson).

Run:  uv run computes/qb_s4.py
Writes computes/qb_s4.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict = {}
rng = np.random.default_rng(20260815)
N = 2_000_000


def show(key, val, note=""):
    if isinstance(val, float):
        R[key] = val
        txt = f"{val:.6f}" if abs(val) >= 1e-4 or val == 0 else f"{val:.6e}"
    else:
        R[key] = val
        txt = str(val)
    print(f"  {key:40s} = {txt}   {note}")


def head(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


# ------------------------------------------------ Q73  E[X|Y] as a random var
head("Q73  Y ~ unif{1,2,4}; X|Y=y ~ Unif[0,y]")
ys = np.array([1.0, 2.0, 4.0])
py = np.array([1 / 3, 1 / 3, 1 / 3])
show("q73_E_X_given_Y2", 2.0 / 2, "a NUMBER")
cond_means = ys / 2
show("q73_cond_mean_vals", [float(v) for v in cond_means], "PMF support of E[X|Y]=Y/2")
EX = float((py * cond_means).sum())
show("q73_EX", EX, "= 7/6 by iterated expectations")
var_of_condmean = float((py * cond_means**2).sum() - EX**2)
show("q73_E_condmean_sq", float((py * cond_means**2).sum()), "= 5.25/3")
show("q73_var_E_X_given_Y", var_of_condmean, "between-group / 'explained'")
cond_vars = ys**2 / 12
show("q73_cond_var_vals", [float(v) for v in cond_vars])
E_condvar = float((py * cond_vars).sum())
show("q73_E_var_X_given_Y", E_condvar, "= 21/36 within-group")
show("q73_var_X", E_condvar + var_of_condmean)
EX2 = float((py * ys**2 / 3).sum())
show("q73_EX2_direct", EX2, "= 21/9")
show("q73_var_X_direct", EX2 - EX**2, "must match q73_var_X")
yy = rng.choice(ys, size=N, p=py)
xx = rng.random(N) * yy
show("q73_mc_EX", float(xx.mean()))
show("q73_mc_var", float(xx.var()))

# --------------------------------------------------- Q74  iterated expectation
head("Q74  three support tiers")
ptier = np.array([0.50, 0.35, 0.15])
mtier = np.array([6.0, 18.0, 47.0])
contrib = ptier * mtier
show("q74_contrib", [float(c) for c in contrib], "p_i * m_i")
ET = float(contrib.sum())
show("q74_ET_min", ET)
show("q74_cost_per_min", 1.20)
show("q74_E_cost", 1.20 * ET)
show("q74_tier3_share", float(contrib[2] / ET))
show("q74_tier1_share", float(contrib[0] / ET))
show("q74_tier3_share_pct", float(100 * contrib[2] / ET))

# ---------------------------------------------------------- Q75 total variance
head("Q75  three shifts: between vs within")
ps = np.array([0.5, 0.3, 0.2])
ms = np.array([40.0, 52.0, 70.0])
vs = np.array([25.0, 64.0, 144.0])
EXs = float((ps * ms).sum())
show("q75_EX", EXs)
within = float((ps * vs).sum())
show("q75_within_terms", [float(a) for a in ps * vs])
show("q75_E_var_within", within)
Ems2 = float((ps * ms**2).sum())
show("q75_E_condmean_sq", Ems2)
show("q75_EX_sq", EXs**2)
between = Ems2 - EXs**2
show("q75_var_E_between", between)
tot = within + between
show("q75_var_total", tot)
show("q75_sd_total", math.sqrt(tot))
show("q75_between_fraction", between / tot)
show("q75_sd_if_means_equalized", math.sqrt(within))

# ------------------------------------------------------- Q76 true/false claims
head("Q76  var(X) >= E[var(X|Y)];  constant E[X|Y] does not give independence")
# counterexample: Y unif{1,2}; X = +-1 given Y=1, +-2 given Y=2
show("q76_condvar_y1", 1.0)
show("q76_condvar_y2", 4.0)
show("q76_E_var", 0.5 * 1.0 + 0.5 * 4.0)
show("q76_var_E", 0.0, "E[X|Y] = 0 identically")
show("q76_var_X", 0.5 * 1.0 + 0.5 * 4.0)
show("q76_P_X_eq_2", 0.5 * 0.5, "unconditional")
show("q76_P_X_eq_2_given_Y1", 0.0, "!= 0.25, so dependent")

# --------------------------------------------------------------- Q77 random sum
head("Q77  food truck: N (mean 120, var 200), X (mean 14, var 36)")
EN, varN, EXo, varX = 120.0, 200.0, 14.0, 36.0
show("q77_EY", EN * EXo)
t1 = EN * varX
t2 = EXo**2 * varN
show("q77_term_sizes", t1, "E[N]var(X)")
show("q77_term_count", t2, "E[X]^2 var(N)")
show("q77_varY", t1 + t2)
show("q77_sdY", math.sqrt(t1 + t2))
show("q77_count_share", t2 / (t1 + t2))
# MC with N ~ negative-binomial matched to mean 120 var 200, X gamma matched
p_nb = EN / varN
r_nb = EN * p_nb / (1 - p_nb)
nn = rng.negative_binomial(r_nb, p_nb, size=400_000)
shape = EXo**2 / varX
scale = varX / EXo
tot_mc = np.array([rng.gamma(shape, scale, size=k).sum() if k else 0.0 for k in nn[:60_000]])
show("q77_mc_EY", float(tot_mc.mean()))
show("q77_mc_varY", float(tot_mc.var()))

# ------------------------------------------------- Q78 spot the error (X const)
head("Q78  N unif{0,1,2,3}, X == 5 constant")
nvals = np.arange(4)
ENq, varNq = float(nvals.mean()), float(nvals.var())
show("q78_EN", ENq)
show("q78_varN", varNq, "= 1.25")
show("q78_varX", 0.0)
show("q78_wrong_varY", ENq * 0.0, "student's E[N]var(X) only")
show("q78_correct_varY", ENq * 0.0 + 25.0 * varNq)
show("q78_EY", ENq * 5.0)
nmc = rng.integers(0, 4, size=N)
show("q78_mc_varY", float((5.0 * nmc).var()))

# --------------------------------------------------- Q79 compound Poisson claims
head("Q79  claims Poisson(8)/day, size mean 2500 sd 4000")
lam79, mu79, sd79 = 8.0, 2500.0, 4000.0
show("q79_EY", lam79 * mu79)
EX2_79 = sd79**2 + mu79**2
show("q79_EX2", EX2_79)
show("q79_varY", lam79 * EX2_79)
show("q79_varY_split_sizes", lam79 * sd79**2)
show("q79_varY_split_count", mu79**2 * lam79)
show("q79_sdY", math.sqrt(lam79 * EX2_79))
show("q79_cv", math.sqrt(lam79 * EX2_79) / (lam79 * mu79))
nmc79 = rng.poisson(lam79, size=300_000)
sh79 = mu79**2 / sd79**2
sc79 = sd79**2 / mu79
tot79 = np.array([rng.gamma(sh79, sc79, size=k).sum() if k else 0.0 for k in nmc79[:60_000]])
show("q79_mc_EY", float(tot79.mean()))
show("q79_mc_varY", float(tot79.var()))

# ------------------------------------------------------------ Q80 Pascal / k-th
head("Q80  Bernoulli p=0.15, third defective")
p80 = 0.15
show("q80_p", p80)
show("q80_binom_coeff", float(math.comb(6, 2)))
show("q80_p_cubed", p80**3)
show("q80_q_fourth", (1 - p80) ** 4)
pT3_7 = math.comb(6, 2) * p80**3 * (1 - p80) ** 4
show("q80_P_T3_eq_7", pT3_7)
show("q80_ET3", 3 / p80)
show("q80_varT3", 3 * (1 - p80) / p80**2)
show("q80_sdT3", math.sqrt(3 * (1 - p80) / p80**2))
show("q80_q_fifth", (1 - p80) ** 5)
show("q80_P_first_le_5", 1 - (1 - p80) ** 5)
show("q80_wrong_binom_pmf", float(stats.binom.pmf(3, 7, p80)), "P(3 in 7 trials), the trap")

# ------------------------------------------------------- Q81 fresh start / memory
head("Q81  polls, alarm prob p=0.02")
p81 = 0.02
show("q81_p", p81)
show("q81_E_extra_polls", 1 / p81)
show("q81_q50", (1 - p81) ** 50)
show("q81_E_alarms_next_100", 100 * p81)
show("q81_E_time_second_alarm", 2 / p81)
show("q81_var_time_second", 2 * (1 - p81) / p81**2)
show("q81_wrong_catchup", 3.0, "gambler's-fallacy answer")
show("q81_P_no_alarm_first_100", (1 - p81) ** 100)

# --------------------------------------------------------- Q82 merging Bernoulli
head("Q82  merge two Bernoulli streams pA=0.10, pB=0.25")
pA, pB = 0.10, 0.25
pboth = pA * pB
pmerge = pA + pB - pboth
show("q82_p_both", pboth)
show("q82_p_merge", pmerge)
show("q82_wrong_sum", pA + pB, "the double-counting trap")
show("q82_E_first_merged", 1 / pmerge)
show("q82_P_A_only_given_report", pA * (1 - pB) / pmerge)
show("q82_P_B_only_given_report", pB * (1 - pA) / pmerge)
show("q82_P_both_given_report", pboth / pmerge)
show("q82_E_slots_until_both", 1 / pboth)
show("q82_check_sum_of_three",
     (pA * (1 - pB) + pB * (1 - pA) + pboth) / pmerge)

# ------------------------------------- Q83 random number of geometric interarrivals
head("Q83  K ~ unif{1,2,3,4} rounds of a geometric(p=0.4) wait")
p83 = 0.4
kv = np.arange(1, 5)
EK, varK = float(kv.mean()), float(kv.var())
show("q83_EK", EK)
show("q83_varK", varK, "= 1.25")
EXg = 1 / p83
varXg = (1 - p83) / p83**2
show("q83_EX_geom", EXg)
show("q83_var_geom", varXg)
show("q83_ET", EK * EXg)
show("q83_varT_sizes", EK * varXg)
show("q83_varT_count", EXg**2 * varK)
show("q83_varT", EK * varXg + EXg**2 * varK)
show("q83_sdT", math.sqrt(EK * varXg + EXg**2 * varK))
show("q83_P_T2_K1", 0.25 * (1 - p83) * p83)
show("q83_P_T2_K2", 0.25 * p83**2)
show("q83_P_T_eq_2", 0.25 * (1 - p83) * p83 + 0.25 * p83**2)
kmc = rng.integers(1, 5, size=N)
tmc = np.array([rng.geometric(p83, size=k).sum() for k in kmc[:200_000]])
show("q83_mc_ET", float(tmc.mean()))
show("q83_mc_varT", float(tmc.var()))
show("q83_mc_P_T_eq_2", float((tmc == 2).mean()))

# ------------------------------------------------------------- Q84 Poisson counts
head("Q84  clinic, lambda = 3/hour")
lam84 = 3.0
m_half = lam84 * 0.5
show("q84_mean_half_hour", m_half)
show("q84_exp_neg_1p5", math.exp(-1.5))
p2 = math.exp(-m_half) * m_half**2 / 2
show("q84_P_exactly_2_in_30min", p2)
show("q84_mean_2h", lam84 * 2)
show("q84_P_at_least_1_in_2h", 1 - math.exp(-6.0))
show("q84_P_0_in_30min", math.exp(-m_half))
show("q84_P_joint", p2 * math.exp(-m_half))
show("q84_P_0_second_given_2_first", math.exp(-m_half), "unchanged: independence")
show("q84_mc_check_P2", float((rng.poisson(m_half, size=N) == 2).mean()))

# ------------------------------------------------- Q85 exponential interarrivals
head("Q85  911 calls, lambda = 5/hour = 1/12 per minute")
lam85_min = 5 / 60
show("q85_lambda_per_min", lam85_min)
show("q85_mean_gap_min", 1 / lam85_min)
show("q85_P_gt_20min", math.exp(-lam85_min * 20))
show("q85_P_gt_20_more_given_8", math.exp(-lam85_min * 20), "memoryless")
show("q85_E_extra_given_8", 1 / lam85_min)
show("q85_E_total_given_8", 8 + 1 / lam85_min)
show("q85_exp_m5_12", math.exp(-5 * lam85_min))
show("q85_exp_m15_12", math.exp(-15 * lam85_min))
show("q85_P_between_5_15", math.exp(-5 * lam85_min) - math.exp(-15 * lam85_min))
show("q85_wrong_no_memory", math.exp(-lam85_min * 12), "P(T>12) if you 'subtract' 8 wrongly")

# ------------------------------------------------------------------- Q86 Erlang
head("Q86  fifth call, lambda = 5/hour")
lam86, k86 = 5.0, 5
show("q86_EY5_hours", k86 / lam86)
show("q86_varY5", k86 / lam86**2)
show("q86_sdY5_hours", math.sqrt(k86 / lam86**2))
show("q86_sdY5_min", 60 * math.sqrt(k86 / lam86**2))
m86 = lam86 * 1.5
terms86 = [math.exp(-m86) * m86**j / math.factorial(j) for j in range(5)]
show("q86_mean_in_1p5h", m86)
show("q86_poisson_terms", [round(float(t), 6) for t in terms86])
show("q86_P_Y5_gt_1p5", float(sum(terms86)))
show("q86_erlang_pdf_at_1", float(lam86**5 * 1**4 * math.exp(-lam86) / math.factorial(4)))
show("q86_gamma_sf_check", float(stats.gamma.sf(1.5, a=5, scale=1 / lam86)))
show("q86_mc_P_Y5_gt_1p5",
     float((rng.gamma(5, 1 / lam86, size=N) > 1.5).mean()))

# --------------------------------------- Q87 small-interval def / Poisson approx
head("Q87  small interval, lambda = 2 per minute, delta = 0.001 min")
lam87, d87 = 2.0, 0.001
ld = lam87 * d87
show("q87_lambda_delta", ld)
show("q87_P_at_least_1", 1 - math.exp(-ld))
show("q87_rel_error_pct", 100 * abs((1 - math.exp(-ld)) - ld) / (1 - math.exp(-ld)))
p_ge2 = 1 - math.exp(-ld) * (1 + ld)
show("q87_P_at_least_2", p_ge2)
show("q87_P_ge2_over_delta", p_ge2 / d87)
show("q87_P_ge2_over_delta_half", (1 - math.exp(-ld / 2) * (1 + ld / 2)) / (d87 / 2),
     "halving delta halves the ratio -> o(delta)")
show("q87_binom_P3", float(stats.binom.pmf(3, 1000, 0.002)))
show("q87_pois_P3", float(stats.poisson.pmf(3, 2.0)))
show("q87_abs_gap", abs(float(stats.binom.pmf(3, 1000, 0.002)) - float(stats.poisson.pmf(3, 2.0))))

# --------------------------------------------------- Q88 competing exponentials
head("Q88  three failure modes, rates 0.5, 0.3, 0.2 per year")
lams = np.array([0.5, 0.3, 0.2])
L = float(lams.sum())
show("q88_total_rate", L)
show("q88_ET_years", 1 / L)
show("q88_sdT_years", 1 / L)
show("q88_P_mode2", float(lams[1] / L))
show("q88_P_mode3", float(lams[2] / L))
show("q88_P_T_gt_2", math.exp(-L * 2))
show("q88_P_T_gt2_and_mode3", math.exp(-L * 2) * float(lams[2] / L))
show("q88_E_T_given_mode3", 1 / L, "independence of min and argmin")
t1s = rng.exponential(1 / lams[0], size=N)
t2s = rng.exponential(1 / lams[1], size=N)
t3s = rng.exponential(1 / lams[2], size=N)
tmin = np.minimum(np.minimum(t1s, t2s), t3s)
who = np.argmin(np.vstack([t1s, t2s, t3s]), axis=0)
show("q88_mc_ET", float(tmin.mean()))
show("q88_mc_P_mode3", float((who == 2).mean()))
show("q88_mc_E_T_given_mode3", float(tmin[who == 2].mean()))
show("q88_mc_P_T_gt2_and_mode3", float(((tmin > 2) & (who == 2)).mean()))

# ------------------------------------------- Q89 splitting: independent streams
head("Q89  split Poisson(12/hr) over 2 hours, p(spam)=0.25")
lam89, tau89, p89 = 12.0, 2.0, 0.25
m_all = lam89 * tau89
m_spam, m_ham = m_all * p89, m_all * (1 - p89)
show("q89_mean_all", m_all)
show("q89_mean_spam", m_spam)
show("q89_mean_ham", m_ham)
ps5 = float(stats.poisson.pmf(5, m_spam))
ph20 = float(stats.poisson.pmf(20, m_ham))
show("q89_P_spam_5", ps5)
show("q89_P_ham_20", ph20)
show("q89_P_joint", ps5 * ph20)
show("q89_P_total_25", float(stats.poisson.pmf(25, m_all)))
show("q89_P_binom_5_of_25", float(stats.binom.pmf(5, 25, p89)))
show("q89_factorization_check", float(stats.poisson.pmf(25, m_all)) * float(stats.binom.pmf(5, 25, p89)))
show("q89_cov_theory", 0.0)
ntot = rng.poisson(m_all, size=N)
nspam = rng.binomial(ntot, p89)
nham = ntot - nspam
show("q89_mc_cov", float(np.cov(nspam, nham)[0, 1]))
show("q89_mc_P_joint", float(((nspam == 5) & (nham == 20)).mean()))
show("q89_mc_var_spam", float(nspam.var()))

# ---------------------------------------------- Q90 splitting + merging, mixed
head("Q90  email 10/hr, 20% urgent; second inbox 4/hr")
lam90, p90 = 10.0, 0.20
show("q90_urgent_rate", lam90 * p90)
show("q90_mean_urgent_3h", lam90 * p90 * 3)
show("q90_P_urgent_4_in_3h", float(stats.poisson.pmf(4, lam90 * p90 * 3)))
show("q90_P_2_urgent_of_8", float(stats.binom.pmf(2, 8, p90)))
show("q90_binom_coeff_8_2", float(math.comb(8, 2)))
show("q90_0p8_pow6", 0.8**6)
show("q90_merged_rate", lam90 + 4.0)
show("q90_P_next_from_inbox1", lam90 / (lam90 + 4.0))
show("q90_E_gap_merged_min", 60 / (lam90 + 4.0))
show("q90_wrong_poisson_for_part_b", float(stats.poisson.pmf(2, lam90 * p90)),
     "treating the conditional count as Poisson(2)")

# ------------------------------------------------- Q91 random incidence, discrete
head("Q91  train gaps: 4 min w.p. 0.8, 24 min w.p. 0.2")
gv = np.array([4.0, 24.0])
gp = np.array([0.8, 0.2])
EG = float((gv * gp).sum())
EG2 = float((gv**2 * gp).sum())
show("q91_E_gap", EG)
show("q91_E_gap_sq", EG2)
wq = gp * gv / EG
show("q91_lengthbias_probs", [float(w) for w in wq])
show("q91_E_L", float((wq * gv).sum()))
show("q91_E_L_formula", EG2 / EG, "= E[X^2]/E[X]")
show("q91_E_wait", 0.5 * EG2 / EG)
show("q91_wrong_wait", EG / 2, "the tempting half-the-mean-gap answer")
show("q91_frac_passengers_long_gap", float(wq[1]))
show("q91_frac_gaps_long", float(gp[1]))
# MC: simulate a long timeline, drop passengers uniformly
ngaps = 400_000
gaps = rng.choice(gv, size=ngaps, p=gp)
edges = np.concatenate([[0.0], np.cumsum(gaps)])
tarr = rng.random(N) * edges[-1]
idx = np.searchsorted(edges, tarr, side="right") - 1
show("q91_mc_E_L", float(gaps[idx].mean()))
show("q91_mc_E_wait", float((edges[idx + 1] - tarr).mean()))

# ---------------------------------------------- Q92 Poisson random incidence
head("Q92  buses Poisson 6/hour")
lam92 = 6.0
mean_gap92 = 60 / lam92
show("q92_mean_gap_min", mean_gap92)
show("q92_E_forward_wait", mean_gap92)
show("q92_E_backward", mean_gap92)
show("q92_E_L", 2 * mean_gap92)
show("q92_var_L_min2", 2 * mean_gap92**2)
show("q92_sd_L_min", math.sqrt(2 * mean_gap92**2))
show("q92_ratio", (2 * mean_gap92) / mean_gap92)
lam92_min = lam92 / 60
show("q92_mc_E_L",
     float((rng.exponential(1 / lam92_min, size=N) + rng.exponential(1 / lam92_min, size=N)).mean()))

# -------------------------------------------------------- Q93 mixed Poisson
head("Q93  Lambda = 20 w.p. 0.7, 90 w.p. 0.3; N | Lambda ~ Poisson")
lv = np.array([20.0, 90.0])
lp = np.array([0.7, 0.3])
EL93 = float((lv * lp).sum())
show("q93_terms", [float(a) for a in lv * lp])
show("q93_EN", EL93)
show("q93_E_var_within", EL93, "E[var(N|Lambda)] = E[Lambda]")
EL2 = float((lv**2 * lp).sum())
show("q93_E_Lambda_sq", EL2)
show("q93_EN_sq", EL93**2)
varL93 = EL2 - EL93**2
show("q93_var_E_between", varL93)
show("q93_var_N", EL93 + varL93)
show("q93_sd_N", math.sqrt(EL93 + varL93))
show("q93_sd_pure_poisson", math.sqrt(EL93))
show("q93_overdispersion", (EL93 + varL93) / EL93)
show("q93_P_N_0", 0.7 * math.exp(-20) + 0.3 * math.exp(-90))
show("q93_P_N_0_exp20_term", 0.7 * math.exp(-20))
lmc = rng.choice(lv, size=N, p=lp)
nmc93 = rng.poisson(lmc)
show("q93_mc_EN", float(nmc93.mean()))
show("q93_mc_varN", float(nmc93.var()))

# ------------------------------------------------------------- Q94 which tool
head("Q94  tool-selection item (no free numbers beyond these checks)")
show("q94_n_scenarios", 5)

# ------------------------------------------ extras quoted in the fragment prose
head("Extras quoted in the fragment text")
show("q74_wrong_unweighted", (6 + 18 + 47) / 3, "averaging tiers, not tickets")
show("q79_size_share", 128.0 / 178.0, "fraction of var from claim sizes")
show("q80_wrong_binom_value", float(stats.binom.pmf(3, 7, 0.15)), "the binomial trap")
show("q83_understatement", 1 - 9.375 / 17.1875, "how much the k=E[K] shortcut drops")
show("q84_wrong_lambda3", math.exp(-3) * 9 / 2, "using lambda*tau=3 over half an hour")
show("q86_wrong_le5", float(sum(math.exp(-7.5) * 7.5**j / math.factorial(j) for j in range(6))),
     "including k=5 by mistake")
show("q89_var_sum_check", 6.0 + 18.0 + 0.0, "= var(N) = 24 with zero covariance")
show("q77_wrong_var_product", 200.0 * 36.0, "var(N)var(X): multiplying the variances")
show("q83_wrong_unweighted_PT2", (1 - 0.4) * 0.4 + 0.4**2, "P(T=2) with the K-weights dropped")
show("q89_cond_cov_given_25", -25 * 0.25 * 0.75, "cov(N_S,N_L | N=25): the fixed-total answer")
show("q91_bias_ratio", 16.0 / 8.0)
show("q93_between_share", 1029.0 / 1070.0)
show("q93_pure_poisson_P0", math.exp(-41.0), "Poisson(41) at 0, for contrast")
show("q93_exp_neg20", math.exp(-20.0))

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(R, indent=1, sort_keys=True), encoding="utf-8")
print(f"\nWrote {out}  ({len(R)} keys)")
