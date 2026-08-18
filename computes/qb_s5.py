# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy"]
# ///
"""Recompute every number appearing in fragments/qb_s5.html (Q95-Q114, Markov chains)."""

import json
import sys
from fractions import Fraction

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
    print(f"{k:44s} = {v}")


def stat(P):
    """Stationary distribution of an irreducible stochastic matrix, by linear solve."""
    P = np.asarray(P, dtype=float)
    m = P.shape[0]
    A = np.vstack([P.T - np.eye(m), np.ones(m)])
    b = np.zeros(m + 1)
    b[-1] = 1.0
    return np.linalg.lstsq(A, b, rcond=None)[0]


rng = np.random.default_rng(20260814)


def mc_chain(P, start, steps, n_paths):
    """Monte-Carlo empirical distribution of X_steps given X_0 = start."""
    P = np.asarray(P, dtype=float)
    m = P.shape[0]
    cur = np.full(n_paths, start, dtype=int)
    C = np.cumsum(P, axis=1)
    for _ in range(steps):
        u = rng.random(n_paths)
        cur = (u[:, None] > C[cur]).sum(axis=1)
    return np.bincount(cur, minlength=m) / n_paths


print("=" * 70)
print("Q95  spot-the-error: is this a transition matrix?")
print("=" * 70)
Q95 = np.array([[0.5, 0.3, 0.3], [0.2, 0.5, 0.3], [0.4, -0.1, 0.7]])
put("Q95_row_sums", np.round(Q95.sum(axis=1), 10))
put("Q95_col_sums", np.round(Q95.sum(axis=0), 10))
put("Q95_row1_sum", float(Q95[0].sum()))
put("Q95_row1_excess", float(Q95[0].sum() - 1))
put("Q95_neg_entry", float(Q95[2, 1]))
put("Q95_fix_p13", float(Q95[0, 2] - 0.1))
Q95f = np.array([[0.5, 0.3, 0.2], [0.2, 0.5, 0.3], [0.4, 0.1, 0.5]])
put("Q95_fixed_row_sums", np.round(Q95f.sum(axis=1), 10))
put("Q95_fixed_col_sums", np.round(Q95f.sum(axis=0), 10))

print("=" * 70)
print("Q96  n-step probabilities")
print("=" * 70)
Q96 = np.array([[0.5, 0.4, 0.1], [0.2, 0.3, 0.5], [0.0, 0.6, 0.4]])
put("Q96_rowsums", np.round(Q96.sum(axis=1), 10))
P2 = Q96 @ Q96
P3 = P2 @ Q96
put("Q96_P2", np.round(P2, 6))
put("Q96_P3", np.round(P3, 6))
put("Q96_r13_2", round(float(P2[0, 2]), 6))
put("Q96_r13_2_terms", [round(float(Q96[0, k] * Q96[k, 2]), 6) for k in range(3)])
put("Q96_r13_3", round(float(P3[0, 2]), 6))
put("Q96_r13_3_terms", [round(float(P2[0, k] * Q96[k, 2]), 6) for k in range(3)])
put("Q96_path_1_2_3", round(float(Q96[0, 1] * Q96[1, 2]), 6))
put("Q96_r12_2", round(float(P2[0, 1]), 6))
put("Q96_MC_r13_2", round(float(mc_chain(Q96, 0, 2, 400000)[2]), 4))
put("Q96_MC_r13_3", round(float(mc_chain(Q96, 0, 3, 400000)[2]), 4))

print("=" * 70)
print("Q97  building P from a story: subscription chain (A,P,C)")
print("=" * 70)
Q97 = np.array([[0.80, 0.15, 0.05], [0.30, 0.55, 0.15], [0.0, 0.0, 1.0]])
put("Q97_rowsums", np.round(Q97.sum(axis=1), 10))
Q97_2 = Q97 @ Q97
Q97_3 = Q97_2 @ Q97
put("Q97_P2", np.round(Q97_2, 6))
put("Q97_P3", np.round(Q97_3, 6))
put("Q97_rAC_2", round(float(Q97_2[0, 2]), 6))
put("Q97_rAA_2", round(float(Q97_2[0, 0]), 6))
put("Q97_rAP_2", round(float(Q97_2[0, 1]), 6))
put("Q97_rAC_3", round(float(Q97_3[0, 2]), 6))
put("Q97_rAA_3", round(float(Q97_3[0, 0]), 6))
put("Q97_rAP_3", round(float(Q97_3[0, 1]), 6))
put("Q97_naive_wrong_3x005", round(3 * 0.05, 6))
put("Q97_MC_rAC_3", round(float(mc_chain(Q97, 0, 3, 400000)[2]), 4))

print("=" * 70)
print("Q98  initial distribution forwards, Bayes backwards")
print("=" * 70)
Q98 = np.array([[0.9, 0.1], [0.4, 0.6]])
pi0 = np.array([0.3, 0.7])
pi1 = pi0 @ Q98
pi2 = pi1 @ Q98
put("Q98_pi1", np.round(pi1, 6))
put("Q98_P_X1_1", round(float(pi1[0]), 6))
put("Q98_P_X1_1_terms", [round(0.3 * 0.9, 6), round(0.7 * 0.4, 6)])
put("Q98_P_X2_1", round(float(pi2[0]), 6))
put("Q98_P_X2_1_terms", [round(float(pi1[0] * 0.9), 6), round(float(pi1[1] * 0.4), 6)])
put("Q98_post_X0_1_given_X1_1", round(0.27 / 0.55, 6))
put("Q98_post_X0_2_given_X1_1", round(0.28 / 0.55, 6))
put("Q98_prior_X0_1", 0.3)
# Monte Carlo the backwards posterior
n = 600000
s0 = (rng.random(n) > 0.3).astype(int)
u = rng.random(n)
C98 = np.cumsum(Q98, axis=1)
s1 = (u[:, None] > C98[s0]).sum(axis=1)
put("Q98_MC_post", round(float(((s0 == 0) & (s1 == 0)).sum() / (s1 == 0).sum()), 4))
put("Q98_MC_P_X1_1", round(float((s1 == 0).mean()), 4))

print("=" * 70)
print("Q99  hidden coin: naive state is NOT Markov, enlarge it")
print("=" * 70)
pA, pB, w = 0.8, 0.3, 0.5
pH = w * pA + (1 - w) * pB
pHH = w * pA**2 + (1 - w) * pB**2
pHHH = w * pA**3 + (1 - w) * pB**3
put("Q99_P_H", round(pH, 6))
put("Q99_P_HH", round(pHH, 6))
put("Q99_P_HHH", round(pHHH, 6))
put("Q99_P_H_given_H", round(pHH / pH, 6))
put("Q99_P_H_given_HH", round(pHHH / pHH, 6))
put("Q99_gap", round(pHHH / pHH - pHH / pH, 6))
put("Q99_post_A_given_HH", round(w * pA**2 / pHH, 6))
put("Q99_check_mix", round(0.8 * (w * pA**2 / pHH) + 0.3 * (1 - w * pA**2 / pHH), 6))
# enlarged chain on (coin, last flip): 4 states (A,H),(A,T),(B,H),(B,T)
Penl = np.array(
    [
        [0.8, 0.2, 0.0, 0.0],
        [0.8, 0.2, 0.0, 0.0],
        [0.0, 0.0, 0.3, 0.7],
        [0.0, 0.0, 0.3, 0.7],
    ]
)
put("Q99_Penl_rowsums", np.round(Penl.sum(axis=1), 10))
put("Q99_Penl_P10_rowAH", np.round(np.linalg.matrix_power(Penl, 10)[0], 6))
nmc = 400000
coin = rng.random(nmc) < w
p_of = np.where(coin, pA, pB)
f0 = rng.random(nmc) < p_of
f1 = rng.random(nmc) < p_of
f2 = rng.random(nmc) < p_of
put("Q99_MC_P_H_given_H", round(float((f0 & f1).sum() / f0.sum()), 4))
put("Q99_MC_P_H_given_HH", round(float((f0 & f1 & f2).sum() / (f0 & f1).sum()), 4))

print("=" * 70)
print("Q100  classification of a six-state chain")
print("=" * 70)
Q100 = np.array(
    [
        [0.2, 0.3, 0.5, 0.0, 0.0, 0.0],
        [0.4, 0.0, 0.0, 0.0, 0.6, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.7, 0.3, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
    ]
)
put("Q100_rowsums", np.round(Q100.sum(axis=1), 10))
reach = (Q100 > 0).astype(int)
acc = reach.copy()
for _ in range(6):
    acc = ((acc + acc @ reach) > 0).astype(int)
put("Q100_accessibility_matrix", acc.tolist())
put("Q100_from1_reaches", [j + 1 for j in range(6) if acc[0, j]])
put("Q100_from2_reaches", [j + 1 for j in range(6) if acc[1, j]])
put("Q100_from3_reaches", [j + 1 for j in range(6) if acc[2, j]])
put("Q100_from5_reaches", [j + 1 for j in range(6) if acc[4, j]])
# probability of ending in the {5,6} class from state 1: absorption-style solve
# b_i = P(absorbed into {5,6}) ; b_3=b_4=0, b_5=b_6=1
A = np.array([[1 - 0.2, -0.3], [-0.4, 1.0]])
rhs = np.array([0.0, 0.6])
b12 = np.linalg.solve(A, rhs)
put("Q100_P_class56_from1", round(float(b12[0]), 6))
put("Q100_P_class56_from2", round(float(b12[1]), 6))
put("Q100_P_class34_from1", round(1 - float(b12[0]), 6))
put("Q100_MC_class56_from1", round(float(mc_chain(Q100, 0, 200, 200000)[4:].sum()), 4))
put("Q100_P200_row1", np.round(np.linalg.matrix_power(Q100, 200)[0], 6))
put("Q100_P201_row1", np.round(np.linalg.matrix_power(Q100, 201)[0], 6))

print("=" * 70)
print("Q101  periodicity: cycles of length 3 and 4")
print("=" * 70)
Q101 = np.array(
    [
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.6, 0.0, 0.0, 0.4],
        [1.0, 0.0, 0.0, 0.0],
    ]
)
put("Q101_rowsums", np.round(Q101.sum(axis=1), 10))
r11 = [round(float(np.linalg.matrix_power(Q101, k)[0, 0]), 6) for k in range(1, 13)]
put("Q101_r11_n_1to12", r11)
put("Q101_n_with_r11_zero_upto12", [k + 1 for k in range(12) if r11[k] == 0.0])
put("Q101_cycle_lengths", [3, 4])
put("Q101_gcd", int(np.gcd(3, 4)))
put("Q101_first_n_all_positive", 6)
put("Q101_pi", np.round(stat(Q101), 6))
put("Q101_P100_row1", np.round(np.linalg.matrix_power(Q101, 100)[0], 6))
put("Q101_P101_row1", np.round(np.linalg.matrix_power(Q101, 101)[0], 6))

print("=" * 70)
print("Q102  the two ways convergence fails")
print("=" * 70)
QA = np.array([[0.0, 1.0], [1.0, 0.0]])
put("Q102_A_r11_even", round(float(np.linalg.matrix_power(QA, 10)[0, 0]), 6))
put("Q102_A_r11_odd", round(float(np.linalg.matrix_power(QA, 11)[0, 0]), 6))
put("Q102_A_pi", np.round(stat(QA), 6))
put("Q102_A_cesaro", np.round(sum(np.linalg.matrix_power(QA, k) for k in range(1, 2001))[0] / 2000, 6))
QB = np.array(
    [
        [0.7, 0.3, 0.0, 0.0],
        [0.4, 0.6, 0.0, 0.0],
        [0.0, 0.0, 0.5, 0.5],
        [0.0, 0.0, 0.1, 0.9],
    ]
)
put("Q102_B_rowsums", np.round(QB.sum(axis=1), 10))
put("Q102_B_class1_pi", np.round(stat(QB[:2, :2]), 6))
put("Q102_B_class2_pi", np.round(stat(QB[2:, 2:]), 6))
put("Q102_B_class1_pi_frac", ["4/7", "3/7"])
put("Q102_B_class2_pi_frac", ["1/6", "5/6"])
put("Q102_B_P200", np.round(np.linalg.matrix_power(QB, 200), 6))
put("Q102_B_r13_limit", 0.0)

print("=" * 70)
print("Q103  true/false trio")
print("=" * 70)
put("Q103_counterexample_r11_even", round(float(np.linalg.matrix_power(QA, 200)[0, 0]), 6))
put("Q103_counterexample_r11_odd", round(float(np.linalg.matrix_power(QA, 201)[0, 0]), 6))
Q103c = np.array([[0.5, 0.5, 0.0], [0.0, 0.6, 0.4], [0.0, 0.3, 0.7]])
put("Q103_c_pi", np.round(stat(Q103c), 6))
put("Q103_c_P200_row1", np.round(np.linalg.matrix_power(Q103c, 200)[0], 6))
put("Q103_c_pi_transient", round(float(stat(Q103c)[0]), 6))

print("=" * 70)
print("Q104  two-state steady state")
print("=" * 70)
Q104 = np.array([[0.85, 0.15], [0.25, 0.75]])
pi104 = stat(Q104)
put("Q104_pi", np.round(pi104, 6))
put("Q104_pi1_frac", "5/8")
put("Q104_pi2_frac", "3/8")
put("Q104_pi1", round(float(pi104[0]), 6))
put("Q104_pi2", round(float(pi104[1]), 6))
put("Q104_ratio", round(0.25 / 0.15, 6))
put("Q104_days_in_1_of_400", round(400 * float(pi104[0]), 4))
put("Q104_mean_recurrence_2", round(1 / float(pi104[1]), 6))
put("Q104_P50_row1", np.round(np.linalg.matrix_power(Q104, 50)[0], 6))
put("Q104_MC_frac_state1", round(float(mc_chain(Q104, 1, 300, 200000)[0]), 4))

print("=" * 70)
print("Q105  three-state steady state: the vending machine")
print("=" * 70)
Q105 = np.array([[0.2, 0.5, 0.3], [0.7, 0.3, 0.0], [0.2, 0.5, 0.3]])
put("Q105_rowsums", np.round(Q105.sum(axis=1), 10))
pi105 = stat(Q105)
put("Q105_pi", np.round(pi105, 6))
put("Q105_pi0_frac", str(Fraction(49, 120)))
put("Q105_pi1_frac", str(Fraction(50, 120)))
put("Q105_pi2_frac", str(Fraction(21, 120)))
put("Q105_pi0", round(float(pi105[0]), 6))
put("Q105_pi1", round(float(pi105[1]), 6))
put("Q105_pi2", round(float(pi105[2]), 6))
put("Q105_frac_exact_check", [float(Fraction(49, 120)), float(Fraction(5, 12)), float(Fraction(7, 40))])
put("Q105_s_frac", str(Fraction(7, 12)))
put("Q105_restock_days_per_year", round(365 * float(pi105[0]), 4))
put("Q105_expected_stock", round(float(pi105 @ np.array([0, 1, 2])), 6))
put("Q105_MC_pi", np.round(mc_chain(Q105, 2, 400, 200000), 4))
put("Q105_P200_row1", np.round(np.linalg.matrix_power(Q105, 200)[0], 6))

print("=" * 70)
print("Q106  frequency interpretation")
print("=" * 70)
Q106 = np.array([[0.6, 0.2, 0.2], [0.4, 0.5, 0.1], [0.4, 0.25, 0.35]])
put("Q106_rowsums", np.round(Q106.sum(axis=1), 10))
pi106 = stat(Q106)
put("Q106_pi", np.round(pi106, 6))
put("Q106_pi_claimed", [0.5, 0.3, 0.2])
put("Q106_balance_check_col1", round(float(0.5 * 0.6 + 0.3 * 0.4 + 0.2 * 0.4), 6))
put("Q106_balance_check_col2", round(float(0.5 * 0.2 + 0.3 * 0.5 + 0.2 * 0.25), 6))
put("Q106_balance_check_col3", round(float(0.5 * 0.2 + 0.3 * 0.1 + 0.2 * 0.35), 6))
put("Q106_freq_2to3", round(0.3 * 0.1, 6))
put("Q106_p23", 0.1)
put("Q106_visits_state1_in_1000", round(1000 * 0.5, 4))
put("Q106_transitions_2to3_in_1000", round(1000 * 0.03, 4))
put("Q106_mean_recurrence_3", round(1 / 0.2, 6))
put("Q106_mean_recurrence_1", round(1 / 0.5, 6))
# Monte Carlo the long-run 2->3 transition frequency
nsteps = 2_000_000
cur = 0
C106 = np.cumsum(Q106, axis=1)
us = rng.random(nsteps)
cnt23 = 0
cnt1 = 0
for t in range(nsteps):
    nxt = int((us[t] > C106[cur]).sum())
    if cur == 1 and nxt == 2:
        cnt23 += 1
    if cur == 0:
        cnt1 += 1
    cur = nxt
put("Q106_MC_freq_2to3", round(cnt23 / nsteps, 4))
put("Q106_MC_frac_state1", round(cnt1 / nsteps, 4))

print("=" * 70)
print("Q107  spot-the-error: local balance on a non-birth-death chain")
print("=" * 70)
Q107 = np.array(
    [
        [0.4, 0.4, 0.2, 0.0],
        [0.3, 0.4, 0.3, 0.0],
        [0.0, 0.5, 0.2, 0.3],
        [0.0, 0.0, 0.6, 0.4],
    ]
)
put("Q107_rowsums", np.round(Q107.sum(axis=1), 10))
pi107 = stat(Q107)
put("Q107_pi", np.round(pi107, 6))
put("Q107_pi0", round(float(pi107[0]), 6))
put("Q107_pi1", round(float(pi107[1]), 6))
put("Q107_pi2", round(float(pi107[2]), 6))
put("Q107_pi3", round(float(pi107[3]), 6))
put("Q107_true_ratio_pi1_over_pi0", round(float(pi107[1] / pi107[0]), 6))
put("Q107_student_ratio_pi1_over_pi0", round(0.4 / 0.3, 6))
put("Q107_correct_cut0_out", round(0.4 + 0.2, 6))
put("Q107_correct_cut0_in_coeff", 0.3)
# student's (wrong) chain of local-balance ratios, normalized
r_st = [1.0, 0.4 / 0.3]
r_st.append(r_st[1] * 0.3 / 0.5)
r_st.append(r_st[2] * 0.3 / 0.6)
r_st = np.array(r_st) / sum(r_st)
put("Q107_student_pi", np.round(r_st, 6))
put("Q107_student_pi0_error", round(float(r_st[0] - pi107[0]), 6))
put("Q107_MC_pi", np.round(mc_chain(Q107, 0, 500, 200000), 4))
# cut equations done correctly, as a check: {0,1} vs {2,3}
put("Q107_cut01_out", round(float(pi107[0] * 0.2 + pi107[1] * 0.3), 6))
put("Q107_cut01_in", round(float(pi107[2] * 0.5), 6))

print("=" * 70)
print("Q108  doubly stochastic => uniform")
print("=" * 70)
Q108 = np.array(
    [
        [0.5, 0.2, 0.3, 0.0],
        [0.1, 0.4, 0.2, 0.3],
        [0.2, 0.3, 0.1, 0.4],
        [0.2, 0.1, 0.4, 0.3],
    ]
)
put("Q108_rowsums", np.round(Q108.sum(axis=1), 10))
put("Q108_colsums", np.round(Q108.sum(axis=0), 10))
put("Q108_pi", np.round(stat(Q108), 6))
put("Q108_uniform", [0.25] * 4)
put("Q108_P50", np.round(np.linalg.matrix_power(Q108, 50), 6))
put("Q108_P50_maxdev", round(float(np.abs(np.linalg.matrix_power(Q108, 50) - 0.25).max()), 10))
put("Q108_mean_recurrence_any", 4.0)
put("Q108_MC_pi", np.round(mc_chain(Q108, 0, 400, 200000), 4))
# periodic doubly stochastic counterexample for the convergence caveat
Q108p = np.array([[0.0, 1.0], [1.0, 0.0]])
put("Q108_periodic_colsums", np.round(Q108p.sum(axis=0), 10))
put("Q108_periodic_pi", np.round(stat(Q108p), 6))

print("=" * 70)
print("Q109  birth-death local balance")
print("=" * 70)
p_up = [0.5, 0.4, 0.3]
q_dn = [0.6, 0.5, 0.7]  # q_1, q_2, q_3
ratios = [Fraction(1)]
for i in range(3):
    ratios.append(ratios[-1] * Fraction(p_up[i]).limit_denominator() / Fraction(q_dn[i]).limit_denominator())
tot = sum(ratios)
pi109 = [r / tot for r in ratios]
put("Q109_ratios_over_pi0", [str(r) for r in ratios])
put("Q109_total_over_pi0", str(tot))
put("Q109_pi_frac", [str(x) for x in pi109])
put("Q109_pi", [round(float(x), 6) for x in pi109])
Q109 = np.array(
    [
        [0.5, 0.5, 0.0, 0.0],
        [0.6, 0.0, 0.4, 0.0],
        [0.0, 0.5, 0.2, 0.3],
        [0.0, 0.0, 0.7, 0.3],
    ]
)
put("Q109_rowsums", np.round(Q109.sum(axis=1), 10))
put("Q109_pi_numeric_check", np.round(stat(Q109), 6))
put("Q109_expected_state", round(float(sum(i * float(pi109[i]) for i in range(4))), 6))
put("Q109_MC_pi", np.round(mc_chain(Q109, 0, 500, 200000), 4))

# part (b): inhomogeneous birth-death with a state-proportional death rate (G5 s3.6)
p109b, q109b = Fraction(3, 10), Fraction(1, 5)
a109b = p109b / q109b
put("Q109b_a", str(a109b))
w109b = []
acc = Fraction(1)
for i in range(4):
    if i:
        acc = acc * a109b / i
    w109b.append(acc)
tot109b = sum(w109b)
pi109b = [w / tot109b for w in w109b]
put("Q109b_weights", [str(w) for w in w109b])
put("Q109b_weight_sum", str(tot109b))
put("Q109b_weight_sum_dec", round(float(tot109b), 6))
put("Q109b_pi_frac", [str(x) for x in pi109b])
put("Q109b_pi", [round(float(x), 6) for x in pi109b])
Q109b = np.zeros((4, 4))
for i in range(4):
    if i < 3:
        Q109b[i, i + 1] = float(p109b)
    if i > 0:
        Q109b[i, i - 1] = float(q109b) * i
    Q109b[i, i] = 1.0 - Q109b[i].sum()
put("Q109b_matrix", np.round(Q109b, 10))
put("Q109b_rowsums", np.round(Q109b.sum(axis=1), 10))
put("Q109b_pi_numeric_check", np.round(stat(Q109b), 6))
put("Q109b_expected_state", round(float(sum(i * float(pi109b[i]) for i in range(4))), 6))
put("Q109b_MC_pi", np.round(mc_chain(Q109b, 0, 500, 200000), 4))
# the geometric (wrong) shortcut: pi_i propto a^i, ignoring the 1/i!
w109b_geo = [a109b**i for i in range(4)]
tot_geo = sum(w109b_geo)
pi_geo = [float(w / tot_geo) for w in w109b_geo]
put("X_Q109b_geometric_pi", [round(x, 6) for x in pi_geo])
put("X_Q109b_geometric_EX", round(sum(i * pi_geo[i] for i in range(4)), 6))

print("=" * 70)
print("Q110  finite-buffer queue, load factor rho")
print("=" * 70)
p, q, m = 0.2, 0.5, 4
up = p * (1 - q)
dn = q * (1 - p)
rho = up / dn
put("Q110_p_up", round(up, 6))
put("Q110_p_down", round(dn, 6))
put("Q110_rho", round(rho, 6))
put("Q110_rho_frac", str(Fraction(up).limit_denominator(1000) / Fraction(dn).limit_denominator(1000)))
powers = np.array([rho**i for i in range(m + 1)])
put("Q110_rho_powers", [round(float(x), 8) for x in powers])
pi0_110 = 1 / powers.sum()
put("Q110_denom_sum", round(float(powers.sum()), 8))
put("Q110_pi0", round(float(pi0_110), 6))
put("Q110_pi0_closed_form", round(float((1 - rho) / (1 - rho ** (m + 1))), 6))
pi110 = pi0_110 * powers
put("Q110_pi", [round(float(x), 6) for x in pi110])
put("Q110_pi4_full", round(float(pi110[4]), 6))
put("Q110_EX", round(float(pi110 @ np.arange(m + 1)), 6))
put("Q110_P_loss", round(float(pi110[4] * p * (1 - q)) / p, 6))
put("Q110_infinite_pi0", round(1 - rho, 6))
put("Q110_infinite_EX", round(rho / (1 - rho), 6))
put("Q110_infinite_EX_frac", str(Fraction(1, 3)))
put("Q110_infinite_pi4", round(float((1 - rho) * rho**4), 8))
# --- the chain ACTUALLY used in the question: physical boundary rows ---
# state 0: no departure possible, so p_01 = p ; state 4: arrivals blocked, so p_43 = q
Q110 = np.array(
    [
        [1 - p, p, 0.0, 0.0, 0.0],
        [dn, 1 - dn - up, up, 0.0, 0.0],
        [0.0, dn, 1 - dn - up, up, 0.0],
        [0.0, 0.0, dn, 1 - dn - up, up],
        [0.0, 0.0, 0.0, q, 1 - q],
    ]
)
put("Q110_matrix", np.round(Q110, 6))
put("Q110_rowsums", np.round(Q110.sum(axis=1), 10))
put("Q110_boundary_p01", round(p, 6))
put("Q110_boundary_p43", round(q, 6))
put("Q110_ratio_pi1_over_pi0", round(p / dn, 6))
put("Q110_ratio_pi4_over_pi3", round(up / q, 6))
rel = [1.0, p / dn]
rel.append(rel[-1] * rho)
rel.append(rel[-1] * rho)
rel.append(rel[-1] * up / q)
rel = np.array(rel)
put("Q110_relative_weights", [round(float(x), 8) for x in rel])
put("Q110_weight_sum", round(float(rel.sum()), 8))
pi110b = rel / rel.sum()
put("Q110_pi", [round(float(x), 6) for x in pi110b])
put("Q110_pi0", round(float(pi110b[0]), 6))
put("Q110_pi4", round(float(pi110b[4]), 6))
put("Q110_EX", round(float(pi110b @ np.arange(m + 1)), 6))
put("Q110_EX_terms", [round(float(i * pi110b[i]), 6) for i in range(1, 5)])
put("Q110_pi_numeric_check", np.round(stat(Q110), 6))
put("Q110_MC_pi", np.round(mc_chain(Q110, 0, 800, 200000), 4))
put("Q110_naive_geometric_pi0", round(float(pi0_110), 6))
put("Q110_naive_geometric_EX", round(float(pi110 @ np.arange(m + 1)), 6))
# infinite-buffer version with the same boundary
inf_sum = 1 + (p / dn) / (1 - rho)
put("Q110_inf_sum", round(float(inf_sum), 8))
inf_pi0 = 1 / inf_sum
put("Q110_inf_pi0", round(float(inf_pi0), 6))
put("Q110_inf_EX", round(float(inf_pi0 * (p / dn) / (1 - rho) ** 2), 6))
put("Q110_inf_EX_frac", str(Fraction(8, 15)))
big = np.array([inf_pi0] + [inf_pi0 * (p / dn) * rho ** (i - 1) for i in range(1, 400)])
put("Q110_inf_EX_series_check", round(float(big @ np.arange(400)), 6))

print("=" * 70)
print("Q111  which equation system: chain with two absorbing states")
print("=" * 70)
Q111 = np.array(
    [
        [0.2, 0.5, 0.1, 0.2, 0.0],
        [0.3, 0.1, 0.4, 0.0, 0.2],
        [0.0, 0.4, 0.2, 0.1, 0.3],
        [0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0],
    ]
)
put("Q111_rowsums", np.round(Q111.sum(axis=1), 10))
A111 = np.eye(3) - Q111[:3, :3]
a111 = np.linalg.solve(A111, Q111[:3, 3])
put("Q111_a_absorb4", np.round(a111, 6))
put("Q111_a1_absorb4", round(float(a111[0]), 6))
mu111 = np.linalg.solve(A111, np.ones(3))
put("Q111_mu", np.round(mu111, 6))
put("Q111_mu1", round(float(mu111[0]), 6))
put("Q111_r12_3", round(float(np.linalg.matrix_power(Q111, 3)[0, 1]), 6))
put("Q111_pi", np.round(np.linalg.matrix_power(Q111, 400)[0], 6))
put("Q111_pi_state2_longrun", 0.0)
put("Q111_MC_absorb4_from1", round(float(mc_chain(Q111, 0, 400, 200000)[3]), 4))
put("Q111_MC_r12_3", round(float(mc_chain(Q111, 0, 3, 400000)[1]), 4))
# part (v): expected time to absorption CONDITIONED on absorbing at 4 (G5 s4.5)
a111_full = np.concatenate([a111, [1.0, 0.0]])
Ptil = np.zeros((5, 5))
for i in range(3):
    for j in range(5):
        Ptil[i, j] = a111_full[j] * Q111[i, j] / a111_full[i]
put("Q111_cond_P_rows", np.round(Ptil[:3], 6))
put("Q111_cond_P_rowsums", np.round(Ptil[:3].sum(axis=1), 10))
nu111 = np.linalg.solve(np.eye(3) - Ptil[:3, :3], np.ones(3))
put("Q111_cond_nu", np.round(nu111, 6))
put("Q111_cond_nu1", round(float(nu111[0]), 6))
# the same construction conditioned on absorption at 5, used only as a consistency check
b111_full = np.concatenate([1.0 - a111, [0.0, 1.0]])
Ptil5 = np.zeros((5, 5))
for i in range(3):
    for j in range(5):
        Ptil5[i, j] = b111_full[j] * Q111[i, j] / b111_full[i]
nu111_5 = np.linalg.solve(np.eye(3) - Ptil5[:3, :3], np.ones(3))
put("Q111_cond_nu1_at5", round(float(nu111_5[0]), 6))
put(
    "Q111_cond_mixture_check",
    round(float(a111[0] * nu111[0] + (1 - a111[0]) * nu111_5[0]), 6),
)


def mc_absorption_time(P, start, absorbing, n_paths, cap=600):
    """Monte-Carlo absorption times and absorbing state reached."""
    P = np.asarray(P, dtype=float)
    C = np.cumsum(P, axis=1)
    cur = np.full(n_paths, start, dtype=int)
    T = np.zeros(n_paths, dtype=int)
    done = np.zeros(n_paths, dtype=bool)
    for step in range(1, cap + 1):
        u = rng.random(n_paths)
        nxt = (u[:, None] > C[cur]).sum(axis=1)
        newly = (~done) & np.isin(nxt, absorbing)
        T[newly] = step
        done |= newly
        cur = nxt
        if done.all():
            break
    return T, cur


T111, end111 = mc_absorption_time(Q111, 0, [3, 4], 600000)
put("Q111_MC_cond_nu1", round(float(T111[end111 == 3].mean()), 4))
put("Q111_MC_mu1", round(float(T111.mean()), 4))

print("=" * 70)
print("Q112  absorption probability, first-step analysis")
print("=" * 70)
# states 1(abs), 2, 3, 4(abs); a_i = P(absorbed at 4)
a3 = Fraction(10, 13)
a2 = Fraction(7, 13)
put("Q112_a3_frac", str(a3))
put("Q112_a2_frac", str(a2))
put("Q112_a3", round(float(a3), 6))
put("Q112_a2", round(float(a2), 6))
put("Q112_a2_complement", round(1 - float(a2), 6))
Q112 = np.array(
    [
        [1.0, 0.0, 0.0, 0.0],
        [0.3, 0.0, 0.7, 0.0],
        [0.0, 0.5, 0.0, 0.5],
        [0.0, 0.0, 0.0, 1.0],
    ]
)
put("Q112_rowsums", np.round(Q112.sum(axis=1), 10))
A112 = np.eye(2) - Q112[1:3, 1:3]
put("Q112_solve_check", np.round(np.linalg.solve(A112, Q112[1:3, 3]), 6))
put("Q112_MC_from2", round(float(mc_chain(Q112, 1, 400, 300000)[3]), 4))
put("Q112_MC_from3", round(float(mc_chain(Q112, 2, 400, 300000)[3]), 4))

print("=" * 70)
print("Q113  expected time to absorption")
print("=" * 70)
Q113 = np.array(
    [
        [0.4, 0.6, 0.0, 0.0],
        [0.3, 0.2, 0.5, 0.0],
        [0.0, 0.6, 0.0, 0.4],
        [0.0, 0.0, 0.0, 1.0],
    ]
)
put("Q113_rowsums", np.round(Q113.sum(axis=1), 10))
mu113 = np.linalg.solve(np.eye(3) - Q113[:3, :3], np.ones(3))
put("Q113_mu", np.round(mu113, 6))
put("Q113_mu1", round(float(mu113[0]), 6))
put("Q113_mu2", round(float(mu113[1]), 6))
put("Q113_mu3", round(float(mu113[2]), 6))
put("Q113_mu1_frac", str(Fraction(35, 3)))
put("Q113_mu1_minus_mu2", round(float(mu113[0] - mu113[1]), 6))
put("Q113_5over3", round(5 / 3, 6))
# Monte Carlo the hitting time
nmc = 200000
cur = np.zeros(nmc, dtype=int)
T = np.zeros(nmc)
C113 = np.cumsum(Q113, axis=1)
alive = np.ones(nmc, dtype=bool)
for _ in range(4000):
    if not alive.any():
        break
    uu = rng.random(nmc)
    nxt = (uu[:, None] > C113[cur]).sum(axis=1)
    T[alive] += 1
    cur = np.where(alive, nxt, cur)
    alive = alive & (cur != 3)
put("Q113_MC_mu1", round(float(T.mean()), 4))

print("=" * 70)
print("Q114  gambler's ruin flavour")
print("=" * 70)
pw = 0.45
i0, mtot = 4, 10
rho114 = (1 - pw) / pw
put("Q114_rho", round(rho114, 6))
put("Q114_rho_frac", str(Fraction(11, 9)))
put("Q114_rho_i", round(rho114**i0, 6))
put("Q114_rho_m", round(rho114**mtot, 6))
a114 = (1 - rho114**i0) / (1 - rho114**mtot)
put("Q114_num", round(1 - rho114**i0, 6))
put("Q114_den", round(1 - rho114**mtot, 6))
put("Q114_P_win", round(float(a114), 6))
put("Q114_P_ruin", round(1 - float(a114), 6))
put("Q114_fair_P_win", round(i0 / mtot, 6))
D114 = (i0 - mtot * a114) / (1 - 2 * pw)
put("Q114_1_minus_2p", round(1 - 2 * pw, 6))
put("Q114_m_times_a", round(mtot * float(a114), 6))
put("Q114_E_duration", round(float(D114), 6))
put("Q114_fair_E_duration", i0 * (mtot - i0))
# Monte Carlo
nmc = 300000
pos = np.full(nmc, i0, dtype=int)
steps = np.zeros(nmc)
live = np.ones(nmc, dtype=bool)
for _ in range(200000):
    if not live.any():
        break
    step = np.where(rng.random(nmc) < pw, 1, -1)
    pos = np.where(live, pos + step, pos)
    steps[live] += 1
    live = live & (pos > 0) & (pos < mtot)
put("Q114_MC_P_win", round(float((pos >= mtot).mean()), 4))
put("Q114_MC_E_duration", round(float(steps.mean()), 3))

print("=" * 70)
print("Extra numbers quoted in trap/comment lines")
print("=" * 70)
put("X_Q97_one_minus_095_cubed", round(1 - 0.95**3, 6))
put("X_Q98_r11_2", round(float(np.linalg.matrix_power(Q98, 2)[0, 0]), 6))
put("X_Q98_indep_joint", round(0.3 * 0.55, 6))
put("X_Q104_inverted_ratio", round(0.15 / (0.15 + 0.25), 6))
put("X_Q104_correct_ratio", round(0.25 / (0.15 + 0.25), 6))
put("X_Q105_sum_check", round(0.2 * 49 / 120 + 0.7 * 50 / 120 + 0.2 * 21 / 120, 6))
put("X_Q108_P2_min_entry", round(float((Q108 @ Q108).min()), 6))
put("X_Q109_total_decimal", round(39 / 14, 6))
rho_wrong = 0.2 / 0.5
pw_wrong = np.array([rho_wrong**i for i in range(5)])
pi_wrong = pw_wrong / pw_wrong.sum()
put("X_Q110_wrong_rho", round(rho_wrong, 6))
put("X_Q110_wrong_EX", round(float(pi_wrong @ np.arange(5)), 6))
put("X_Q110_geometric_underestimate_pct", round(100 * (1 - 0.328446 / 0.522556), 2))
rho_inv = 0.45 / 0.55
put("X_Q114_inverted_rho", round(rho_inv, 6))
put("X_Q114_inverted_a4", round((1 - rho_inv**4) / (1 - rho_inv**10), 6))
put("X_Q114_fair_a4", round(4 / 10, 6))
put("X_Q111_a5_from1", round(1 - float(a111[0]), 6))
put("X_Q112_from3_check", round(float(Fraction(10, 13)), 6))

print("=" * 70)
print("Intermediate products displayed inside the solution derivations")
print("=" * 70)
inter = {
    "I_Q97_015x015": 0.15 * 0.15,
    "I_Q97_015x055": 0.15 * 0.55,
    "I_Q97_0685x005": 0.685 * 0.05,
    "I_Q97_02025x015": 0.2025 * 0.15,
    "I_Q98_015x0625": 0.15 * 0.625,
    "I_Q98_075x0375": 0.75 * 0.375,
    "I_Q99_05x064": 0.5 * 0.8**2,
    "I_Q99_05x009": 0.5 * 0.3**2,
    "I_Q99_08cubed": 0.8**3,
    "I_Q99_03cubed": 0.3**3,
    "I_Q99_05x0512": 0.5 * 0.8**3,
    "I_Q99_05x0027": 0.5 * 0.3**3,
    "I_Q99_post_x_08": (0.32 / 0.365) * 0.8,
    "I_Q99_postc_x_03": (1 - 0.32 / 0.365) * 0.3,
    "I_Q105_02x49o120": 0.2 * 49 / 120,
    "I_Q105_07x50o120": 0.7 * 50 / 120,
    "I_Q105_02x21o120": 0.2 * 21 / 120,
    "I_Q105_pct": 100 * 49 / 120,
    "I_Q105_pct_4dp": round(100 * 49 / 120, 4),
    "I_Q107_5o27x02": (5 / 27) * 0.2,
    "I_Q107_10o27x03": (10 / 27) * 0.3,
    "I_Q109_2xpi2": 2 * 28 / 117,
    "I_Q109_3xpi3": 3 * 12 / 117,
    "I_Q110_075sq": 0.75**2,
    "I_Q114_rho4_minus1": (11 / 9) ** 4 - 1,
    "I_Q114_rho10_minus1": (11 / 9) ** 10 - 1,
    "I_Q114_4_minus_ma": 4 - 10 * 0.191266,
}
for k, v in inter.items():
    put(k, round(float(v), 6))

with open("d:/Python-UV/MIT_Applied_Prob/computes/qb_s5.json", "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1)
print(f"\nwrote {len(R)} keys to computes/qb_s5.json")
