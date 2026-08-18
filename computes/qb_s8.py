# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy"]
# ///
"""Recompute every number appearing in fragments/qb_s8.html
(Q151-Q170: multinomial, random walks, waiting times).

Monte-Carlo cross-checks are included for the pattern-waiting and
coupon-collector answers, plus the ruin/duration and multinomial covariance
items.
"""

import json
import sys
from fractions import Fraction
from math import comb, factorial

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

R = {}


def put(k, v):
    if isinstance(v, np.ndarray):
        v = v.tolist()
    if isinstance(v, (np.floating,)):
        v = float(v)
    if isinstance(v, (np.integer,)):
        v = int(v)
    R[k] = v
    print(f"{k:46s} = {v}")


rng = np.random.default_rng(20260819)

# =====================================================================
# MULTINOMIAL  (Q151-Q156)
# =====================================================================
print("\n--- Q151  joint count vector -------------------------------")
p = np.array([0.5, 0.3, 0.2])          # lanes A, B, C
n = 12
mult_coef = factorial(12) // (factorial(6) * factorial(4) * factorial(2))
put("q151_multcoef_6_4_2", mult_coef)
put("q151_powA", 0.5 ** 6)
put("q151_powB", 0.3 ** 4)
put("q151_powC", 0.2 ** 2)
q151 = mult_coef * 0.5 ** 6 * 0.3 ** 4 * 0.2 ** 2
put("q151_p_6_4_2", q151)
coef444 = factorial(12) // factorial(4) ** 3
put("q151_multcoef_4_4_4", coef444)
q151b = coef444 * 0.5 ** 4 * 0.3 ** 4 * 0.2 ** 4
put("q151_p_4_4_4", q151b)
put("q151_p_all_A", 0.5 ** 12)

# Monte-Carlo
S = 400_000
draws = rng.multinomial(n, p, size=S)
put("q151_mc_p_6_4_2", float(np.mean((draws == np.array([6, 4, 2])).all(axis=1))))
put("q151_mc_p_4_4_4", float(np.mean((draws == np.array([4, 4, 4])).all(axis=1))))

print("\n--- Q152  a marginal count ---------------------------------")
put("q152_pmf_NB_4", comb(12, 4) * 0.3 ** 4 * 0.7 ** 8)
put("q152_binom_coef_12_4", comb(12, 4))
put("q152_pow_p4", 0.3 ** 4)
put("q152_pow_q8", 0.7 ** 8)
put("q152_E_NB", 12 * 0.3)
put("q152_var_NB", 12 * 0.3 * 0.7)
put("q152_sd_NB", (12 * 0.3 * 0.7) ** 0.5)
put("q152_p_NB_ge1", 1 - 0.7 ** 12)
put("q152_pow_q12", 0.7 ** 12)
put("q152_mc_pmf_NB_4", float(np.mean(draws[:, 1] == 4)))

print("\n--- Q153  lumping categories -------------------------------")
ps = np.array([0.40, 0.25, 0.20, 0.15])   # four survey answers
n3 = 10
p_lump = ps[2] + ps[3]
put("q153_p_lump", float(p_lump))
put("q153_binom_coef_10_3", comb(10, 3))
put("q153_pow_lump3", float(p_lump ** 3))
put("q153_pow_notlump7", float((1 - p_lump) ** 7))
q153 = comb(10, 3) * p_lump ** 3 * (1 - p_lump) ** 7
put("q153_p_lumped_eq3", float(q153))
coef_433 = factorial(10) // (factorial(4) * factorial(3) * factorial(3))
put("q153_multcoef_4_3_3", coef_433)
q153b = coef_433 * 0.40 ** 4 * 0.25 ** 3 * float(p_lump) ** 3
put("q153_p_4_3_3", float(q153b))
put("q153_E_lump", 10 * float(p_lump))
put("q153_var_lump", 10 * float(p_lump) * (1 - float(p_lump)))
d3 = rng.multinomial(n3, ps, size=S)
put("q153_mc_p_lumped_eq3", float(np.mean(d3[:, 2] + d3[:, 3] == 3)))
put("q153_mc_p_4_3_3", float(np.mean((d3[:, 0] == 4) & (d3[:, 1] == 3) & (d3[:, 2] + d3[:, 3] == 3))))

print("\n--- Q154  conditioning on one count ------------------------")
# 12 customers, p = (.5,.3,.2); condition on N_A = 5
nrem = 12 - 5
put("q154_n_remaining", nrem)
pB = 0.3 / (1 - 0.5)
pC = 0.2 / (1 - 0.5)
put("q154_pB_cond", pB)
put("q154_pC_cond", pC)
put("q154_binom_coef_7_4", comb(7, 4))
put("q154_pow_pB4", pB ** 4)
put("q154_pow_pC3", pC ** 3)
q154 = comb(7, 4) * pB ** 4 * pC ** 3
put("q154_p_NB4_given_NA5", q154)
put("q154_E_NB_given_NA5", nrem * pB)
put("q154_var_NB_given_NA5", nrem * pB * (1 - pB))
put("q154_E_NB_uncond", 12 * 0.3)
# joint / marginal check
joint = (factorial(12) // (factorial(5) * factorial(4) * factorial(3))) * 0.5 ** 5 * 0.3 ** 4 * 0.2 ** 3
marg = comb(12, 5) * 0.5 ** 5 * 0.5 ** 7
put("q154_joint_5_4_3", joint)
put("q154_marg_NA5", marg)
put("q154_ratio_check", joint / marg)
sel = draws[draws[:, 0] == 5]
put("q154_mc_p_NB4_given_NA5", float(np.mean(sel[:, 1] == 4)))
put("q154_mc_E_NB_given_NA5", float(np.mean(sel[:, 1])))

print("\n--- Q155  covariance / correlation of two counts -----------")
cov_AB = -12 * 0.5 * 0.3
put("q155_cov_AB", cov_AB)
put("q155_var_A", 12 * 0.5 * 0.5)
put("q155_var_B", 12 * 0.3 * 0.7)
rho_AB = cov_AB / ((12 * 0.5 * 0.5) ** 0.5 * (12 * 0.3 * 0.7) ** 0.5)
put("q155_rho_AB", rho_AB)
put("q155_rho_formula_check", -((0.5 * 0.3) / ((1 - 0.5) * (1 - 0.3))) ** 0.5)
put("q155_var_A_plus_B", 12 * 0.8 * 0.2)
put("q155_var_sum_via_cov", 3.0 + 2.52 + 2 * cov_AB)
put("q155_cov_AC", -12 * 0.5 * 0.2)
put("q155_mc_cov_AB", float(np.cov(draws[:, 0], draws[:, 1])[0, 1]))
put("q155_mc_rho_AB", float(np.corrcoef(draws[:, 0], draws[:, 1])[0, 1]))

print("\n--- Q156  which distribution -------------------------------")
# urn: 8 red, 6 green, 6 blue, draw 5 WITHOUT replacement
hyp = comb(8, 2) * comb(6, 2) * comb(6, 1) / comb(20, 5)
put("q156_hyp_num_C82", comb(8, 2))
put("q156_hyp_num_C62", comb(6, 2))
put("q156_hyp_num_C61", comb(6, 1))
put("q156_hyp_den_C205", comb(20, 5))
put("q156_hyp_p_2_2_1", hyp)
mn = (factorial(5) // (factorial(2) * factorial(2) * factorial(1))) * 0.4 ** 2 * 0.3 ** 2 * 0.3
put("q156_multcoef_2_2_1", factorial(5) // (factorial(2) * factorial(2) * factorial(1)))
put("q156_mult_p_2_2_1", mn)
put("q156_ratio_hyp_over_mult", hyp / mn)
put("q156_binom_marg_red2_withrepl", comb(5, 2) * 0.4 ** 2 * 0.6 ** 3)
put("q156_hyp_marg_red2", comb(8, 2) * comb(12, 3) / comb(20, 5))
# MC for the without-replacement draw
urn = np.array([0] * 8 + [1] * 6 + [2] * 6)
hits = 0
M = 200_000
for _ in range(M):
    s = rng.choice(urn, size=5, replace=False)
    if (s == 0).sum() == 2 and (s == 1).sum() == 2:
        hits += 1
put("q156_mc_hyp_p_2_2_1", hits / M)

# =====================================================================
# RANDOM WALKS  (Q157-Q163)
# =====================================================================


def ruin(i, N, p):
    """P(hit N before 0) starting from i, up-prob p."""
    if abs(p - 0.5) < 1e-15:
        return i / N
    rho = (1 - p) / p
    return (1 - rho ** i) / (1 - rho ** N)


def duration(i, N, p):
    """E[steps until absorption at 0 or N] from i."""
    if abs(p - 0.5) < 1e-15:
        return i * (N - i)
    return (i - N * ruin(i, N, p)) / (1 - 2 * p)


def mc_walk(i, N, p, reps=300_000):
    pos = np.full(reps, i, dtype=np.int64)
    steps = np.zeros(reps, dtype=np.int64)
    live = np.ones(reps, dtype=bool)
    while live.any():
        k = live.sum()
        mv = np.where(rng.random(k) < p, 1, -1)
        pos[live] += mv
        steps[live] += 1
        live = (pos > 0) & (pos < N)
    return float(np.mean(pos == N)), float(np.mean(steps))


print("\n--- Q157  symmetric ruin -----------------------------------")
put("q157_a3_of_8", ruin(3, 8, 0.5))
put("q157_ruin3", 1 - ruin(3, 8, 0.5))
put("q157_D3", duration(3, 8, 0.5))
put("q157_a6_of_8", ruin(6, 8, 0.5))
put("q157_D6", duration(6, 8, 0.5))
put("q157_a4_of_8", ruin(4, 8, 0.5))
put("q157_D4", duration(4, 8, 0.5))
m_a, m_d = mc_walk(3, 8, 0.5)
put("q157_mc_a3", m_a)
put("q157_mc_D3", m_d)

print("\n--- Q158  biased ruin --------------------------------------")
rho58 = 0.4 / 0.6
put("q158_rho", rho58)
put("q158_rho_pow2", rho58 ** 2)
put("q158_rho_pow6", rho58 ** 6)
put("q158_num", 1 - rho58 ** 2)
put("q158_den", 1 - rho58 ** 6)
put("q158_a2_of_6", ruin(2, 6, 0.6))
put("q158_ruin2", 1 - ruin(2, 6, 0.6))
put("q158_a2_fair", ruin(2, 6, 0.5))
put("q158_a3_of_6", ruin(3, 6, 0.6))
put("q158_a2_of_6_p045", ruin(2, 6, 0.45))
m_a58, m_d58 = mc_walk(2, 6, 0.6)
put("q158_mc_a2", m_a58)

print("\n--- Q159  expected duration, biased ------------------------")
put("q159_1_minus_2p", 1 - 2 * 0.6)
put("q159_N_times_a", 6 * ruin(2, 6, 0.6))
put("q159_D2", duration(2, 6, 0.6))
put("q159_D2_fair", duration(2, 6, 0.5))
put("q159_D3", duration(3, 6, 0.6))
put("q159_mc_D2", m_d58)
put("q159_drift_per_step", 2 * 0.6 - 1)
put("q159_net_change_expected", ruin(2, 6, 0.6) * (6 - 2) + (1 - ruin(2, 6, 0.6)) * (0 - 2))
put("q159_wald_check", (ruin(2, 6, 0.6) * 4 + (1 - ruin(2, 6, 0.6)) * (-2)) / (2 * 0.6 - 1))

print("\n--- Q160  first passage, unbounded -------------------------")
p160 = 0.55
put("q160_drift", 2 * p160 - 1)
put("q160_E_first_hit_plus1", 1 / (2 * p160 - 1))
put("q160_E_first_hit_plus5", 5 / (2 * p160 - 1))
put("q160_p_ever_reach_plus1_p045", 0.45 / 0.55)
put("q160_E_hit_plus5_p06", 5 / (2 * 0.6 - 1))


def mc_firsthit(k, p, reps=200_000):
    pos = np.zeros(reps, dtype=np.int64)
    steps = np.zeros(reps, dtype=np.int64)
    live = np.ones(reps, dtype=bool)
    for _ in range(200_000):
        if not live.any():
            break
        n_ = live.sum()
        pos[live] += np.where(rng.random(n_) < p, 1, -1)
        steps[live] += 1
        live = live & (pos < k)
    return float(np.mean(steps)), float(np.mean(~live))


e1, f1 = mc_firsthit(1, p160)
put("q160_mc_E_first_hit_plus1", e1)
e5, f5 = mc_firsthit(5, p160)
put("q160_mc_E_first_hit_plus5", e5)

print("\n--- Q161  reflecting barriers ------------------------------")
p161, q161 = 0.4, 0.6
r = p161 / q161
put("q161_r", r)
powers = np.array([r ** i for i in range(5)])
put("q161_powers", powers)
Z = powers.sum()
put("q161_Z", float(Z))
pi161 = powers / Z
put("q161_pi", pi161)
put("q161_pi0", float(pi161[0]))
put("q161_pi4", float(pi161[4]))
put("q161_mean_state", float(np.dot(np.arange(5), pi161)))
# explicit chain + numerical stationary check
P161 = np.zeros((5, 5))
P161[0, 0], P161[0, 1] = q161, p161
for i in range(1, 4):
    P161[i, i - 1], P161[i, i + 1] = q161, p161
P161[4, 3], P161[4, 4] = q161, p161
put("q161_rowsums", P161.sum(axis=1))
v = np.ones(5) / 5
for _ in range(20_000):
    v = v @ P161
put("q161_pi_numeric", v)
put("q161_pi_maxerr", float(np.max(np.abs(v - pi161))))
# MC time-average
st = 0
cnt = np.zeros(5)
for _ in range(400_000):
    st = int(rng.choice(5, p=P161[st]))
    cnt[st] += 1
put("q161_mc_pi", cnt / cnt.sum())

print("\n--- Q162  fair-game interpretation -------------------------")
put("q162_E_final_fair", 8 * ruin(3, 8, 0.5) + 0 * (1 - ruin(3, 8, 0.5)))
put("q162_a3", ruin(3, 8, 0.5))
put("q162_ruin3", 1 - ruin(3, 8, 0.5))
put("q162_E_gain_per_step_fair", 0.0)
put("q162_E_gain_per_step_p06", 2 * 0.6 - 1)
put("q162_E_fortune_after10_p06", 3 + 10 * (2 * 0.6 - 1))
put("q162_E_final_p06", 8 * ruin(3, 8, 0.6))
put("q162_a3_p06", ruin(3, 8, 0.6))
put("q162_D3_p06", duration(3, 8, 0.6))
put("q162_E_final_check_p06", 3 + duration(3, 8, 0.6) * (2 * 0.6 - 1))

print("\n--- Q163  spot the error: steady state vs absorption --------")
P163 = np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.5, 0.0, 0.5, 0.0],
    [0.0, 0.5, 0.0, 0.5],
    [0.0, 0.0, 0.0, 1.0],
])
put("q163_rowsums", P163.sum(axis=1))
put("q163_a1_absorb_at_3", ruin(1, 3, 0.5))
put("q163_a2_absorb_at_3", ruin(2, 3, 0.5))
put("q163_mu1", duration(1, 3, 0.5))
put("q163_mu2", duration(2, 3, 0.5))
# two distinct stationary vectors -> non-uniqueness
s1 = np.array([1.0, 0, 0, 0])
s2 = np.array([0.0, 0, 0, 1.0])
s3 = 0.5 * s1 + 0.5 * s2
put("q163_stat_check_s1", s1 @ P163)
put("q163_stat_check_s3", s3 @ P163)
put("q163_bogus_claim", 0.5)
put("q163_correct_from1", ruin(1, 3, 0.5))
# long-run limits of P^n
Pn = np.linalg.matrix_power(P163, 4000)
put("q163_Pn_row1", Pn[1])
put("q163_Pn_row2", Pn[2])

# =====================================================================
# WAITING TIMES  (Q164-Q170)
# =====================================================================
print("\n--- Q164  geometric: first head ----------------------------")
pg = 0.35
put("q164_E_T", 1 / pg)
put("q164_var_T", (1 - pg) / pg ** 2)
put("q164_sd_T", ((1 - pg) / pg ** 2) ** 0.5)
put("q164_p_T_eq3", (1 - pg) ** 2 * pg)
put("q164_p_T_gt5", (1 - pg) ** 5)
put("q164_p_T_gt8_given_gt3", (1 - pg) ** 5)
put("q164_mc_E_T", float(np.mean(rng.geometric(pg, size=1_000_000))))

print("\n--- Q165  Pascal: kth head ---------------------------------")
pp, kk = 0.4, 3
put("q165_E_T", kk / pp)
put("q165_var_T", kk * (1 - pp) / pp ** 2)
put("q165_sd_T", (kk * (1 - pp) / pp ** 2) ** 0.5)
put("q165_binom_coef_7_2", comb(7, 2))
put("q165_pow_p3", pp ** 3)
put("q165_pow_q5", (1 - pp) ** 5)
put("q165_p_T_eq8", comb(7, 2) * pp ** 3 * (1 - pp) ** 5)
put("q165_p_T_eq3", pp ** 3)
mcT = rng.geometric(pp, size=(400_000, kk)).sum(axis=1)
put("q165_mc_E_T", float(np.mean(mcT)))
put("q165_mc_var_T", float(np.var(mcT)))
put("q165_mc_p_T_eq8", float(np.mean(mcT == 8)))


def mc_pattern(pat, p, reps=300_000):
    """Mean tosses until the string `pat` first appears; P(head)=p."""
    L = len(pat)
    tot = 0
    for _ in range(reps):
        buf = ""
        c = 0
        while True:
            c += 1
            buf += "H" if rng.random() < p else "T"
            if len(buf) > L:
                buf = buf[-L:]
            if buf == pat:
                break
        tot += c
    return tot / reps


print("\n--- Q166  pattern HH ---------------------------------------")
put("q166_E_HH_fair", (1 + 0.5) / 0.5 ** 2)
put("q166_E_from_H_fair", 1 / 0.5 ** 2)          # state "one H so far"
put("q166_E_HH_p06", (1 + 0.6) / 0.6 ** 2)
put("q166_E_HH_p035", (1 + 0.35) / 0.35 ** 2)
put("q166_mc_E_HH_fair", mc_pattern("HH", 0.5, 200_000))
put("q166_mc_E_HH_p06", mc_pattern("HH", 0.6, 100_000))

print("\n--- Q167  HT vs HH vs two heads total ----------------------")
put("q167_E_HT_fair", 1 / 0.5 + 1 / 0.5)
put("q167_E_HH_fair", (1 + 0.5) / 0.5 ** 2)
put("q167_E_two_heads_total_fair", 2 / 0.5)
put("q167_E_HT_p06", 1 / 0.6 + 1 / 0.4)
put("q167_E_HH_p06", (1 + 0.6) / 0.6 ** 2)
put("q167_E_two_heads_total_p06", 2 / 0.6)
put("q167_mc_E_HT_fair", mc_pattern("HT", 0.5, 200_000))
put("q167_mc_E_HT_p06", mc_pattern("HT", 0.6, 100_000))

print("\n--- Q168  pattern HTH --------------------------------------")
# states: 0 = nothing, 1 = H, 2 = HT ; e_i = expected further tosses
A = np.array([[0.5, -0.5, 0.0],
              [0.0, 0.5, -0.5],
              [-0.5, 0.0, 1.0]])
b = np.array([1.0, 1.0, 1.0])
e = np.linalg.solve(A, b)
put("q168_e_states", e)
put("q168_E_HTH_fair", float(e[0]))
put("q168_E_from_H", float(e[1]))
put("q168_E_from_HT", float(e[2]))
put("q168_E_HTT_fair", 8.0)
put("q168_mc_E_HTH_fair", mc_pattern("HTH", 0.5, 200_000))
put("q168_mc_E_HTT_fair", mc_pattern("HTT", 0.5, 200_000))

print("\n--- Q169  coupon collector, fair die -----------------------")
H6 = sum(Fraction(1, k) for k in range(1, 7))
put("q169_H6_frac", str(H6))
put("q169_H6", float(H6))
put("q169_E_T", float(6 * H6))
stages = [Fraction(6, 6 - j) for j in range(6)]
put("q169_stage_means", [float(s) for s in stages])
var6 = sum((1 - Fraction(6 - j, 6)) / Fraction(6 - j, 6) ** 2 for j in range(6))
put("q169_var_T_frac", str(var6))
put("q169_var_T", float(var6))
put("q169_sd_T", float(var6) ** 0.5)
pn20 = sum((-1) ** (j + 1) * comb(6, j) * (1 - j / 6) ** 20 for j in range(1, 7))
put("q169_p_T_gt20", pn20)
put("q169_p_T_gt30", sum((-1) ** (j + 1) * comb(6, j) * (1 - j / 6) ** 30 for j in range(1, 7)))


def mc_coupon(probs, reps=200_000):
    m = len(probs)
    probs = np.asarray(probs)
    tot = 0
    over20 = 0
    for _ in range(reps):
        seen = np.zeros(m, dtype=bool)
        c = 0
        while not seen.all():
            c += 1
            seen[rng.choice(m, p=probs)] = True
        tot += c
        if c > 20:
            over20 += 1
    return tot / reps, over20 / reps


mcE, mcP = mc_coupon(np.full(6, 1 / 6))
put("q169_mc_E_T", mcE)
put("q169_mc_p_T_gt20", mcP)

print("\n--- Q170  coupon collector, unequal probabilities -----------")
pv = [0.5, 0.3, 0.2]
t1 = sum(1 / x for x in pv)
t2 = 1 / (pv[0] + pv[1]) + 1 / (pv[0] + pv[2]) + 1 / (pv[1] + pv[2])
t3 = 1 / sum(pv)
put("q170_single_terms", [1 / x for x in pv])
put("q170_sum_singles", t1)
put("q170_pair_sums", [pv[0] + pv[1], pv[0] + pv[2], pv[1] + pv[2]])
put("q170_pair_terms", [1 / (pv[0] + pv[1]), 1 / (pv[0] + pv[2]), 1 / (pv[1] + pv[2])])
put("q170_sum_pairs", t2)
put("q170_triple_term", t3)
put("q170_E_T", t1 - t2 + t3)
put("q170_E_T_uniform3", float(3 * sum(Fraction(1, k) for k in range(1, 4))))
put("q170_excess_over_uniform", (t1 - t2 + t3) - 5.5)
mcE170, _ = mc_coupon(np.array(pv))
put("q170_mc_E_T", mcE170)
put("q170_E_last_is_type3", 1 / pv[2])

# =====================================================================
# Intermediates quoted in the prose, and the wrong answers named in the
# "Trap." lines -- these are numbers too, so they get computed here.
# =====================================================================
print("\n--- intermediates and trap values --------------------------")
put("q151_one_sequence", 0.5 ** 6 * 0.3 ** 4 * 0.2 ** 2)
put("q153_one_sequence", 0.40 ** 4 * 0.25 ** 3 * 0.35 ** 3)
put("q154_one_sequence", 0.5 ** 5 * 0.3 ** 4 * 0.2 ** 3)
put("q154_trap_no_renorm", comb(7, 4) * 0.3 ** 4 * 0.7 ** 3)
put("q155_sd_A", 3.0 ** 0.5)
put("q155_sd_B", 2.52 ** 0.5)
put("q155_sd_product", (3.0 ** 0.5) * (2.52 ** 0.5))
put("q155_trap_var_sum_indep", 3.0 + 2.52)
put("q156_fpc_15_over_19", 15 / 19)
put("q158_rho_p045", 0.55 / 0.45)
put("q158_rho2_p045", (0.55 / 0.45) ** 2)
put("q158_rho6_p045", (0.55 / 0.45) ** 6)
put("q158_num_p045", 1 - (0.55 / 0.45) ** 2)
put("q158_den_p045", 1 - (0.55 / 0.45) ** 6)
put("q158_trap_rho_inverted", 0.6 / 0.4)
put("q158_trap_a2", (1 - 1.5 ** 2) / (1 - 1.5 ** 6))
put("q160_disc", 1 - 4 * 0.55 * 0.45)
put("q162_rho3", (2 / 3) ** 3)
put("q162_rho8", (2 / 3) ** 8)
put("q162_num", 1 - (2 / 3) ** 3)
put("q162_den", 1 - (2 / 3) ** 8)
put("q162_fair_check", -3 * 0.625 + 5 * 0.375)
put("q164_p_T_ge5", 0.65 ** 4)
put("q165_trap_binomial_8_3", comb(8, 3) * 0.4 ** 3 * 0.6 ** 5)
# Q168 trap: mis-handling HH by resetting to S0 instead of staying at S1
Abad = np.array([[0.5, -0.5, 0.0],
                 [-0.5, 1.0, -0.5],
                 [-0.5, 0.0, 1.0]])
put("q168_trap_E_reset_on_HH", float(np.linalg.solve(Abad, np.array([1.0, 1.0, 1.0]))[0]))
put("q169_var_terms", [float((1 - Fraction(6 - j, 6)) / Fraction(6 - j, 6) ** 2) for j in range(6)])
put("q169_first_ie_term", 6 * (5 / 6) ** 20)
put("q169_ie_terms_n20", [(-1) ** (j + 1) * comb(6, j) * (1 - j / 6) ** 20 for j in range(1, 7)])
put("q169_pow_5_6_20", (5 / 6) ** 20)
put("q169_frac_last_stage_mean", 6 / 14.7)
put("q169_frac_last_stage_var", 30 / 38.99)
put("q169_trap_6_times_6", 36)
put("q170_excess_pct", ((t1 - t2 + t3) - 5.5) / 5.5)
put("q170_H3", float(sum(Fraction(1, k) for k in range(1, 4))))

with open("d:/Python-UV/MIT_Applied_Prob/computes/qb_s8.json", "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1, sort_keys=True)
print("\nwrote computes/qb_s8.json with", len(R), "keys")
