# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Every number quoted in notes/src/fragments/qb_s1.html
(question bank section 1 - probability fundamentals, Q1-Q25).

Run:  uv run computes/qb_s1.py
Writes computes/qb_s1.json.
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from itertools import permutations, product
from math import comb, factorial, log
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict[str, object] = {}
rng = np.random.default_rng(20260815)
N_MC = 4_000_000


def put(key: str, val, label: str = "") -> None:
    if isinstance(val, F):
        R[key] = float(val)
        R[key + "_frac"] = f"{val.numerator}/{val.denominator}"
        print(f"{key:38s} = {float(val):.10g}   ({val})   {label}")
    else:
        R[key] = val
        if isinstance(val, float):
            print(f"{key:38s} = {val:.10g}   {label}")
        else:
            print(f"{key:38s} = {val}   {label}")


def head(t: str) -> None:
    print("\n" + "=" * 74 + f"\n{t}\n" + "=" * 74)


# ----------------------------------------------------------------- Q1 axioms
head("Q1  two-event bookkeeping from the axioms")
pA, pB, pAuB = F(55, 100), F(40, 100), F(75, 100)
q1_and = pA + pB - pAuB
put("q1_PA", pA)
put("q1_PB", pB)
put("q1_PAuB", pAuB)
put("q1_PAandB", q1_and, "inclusion-exclusion")
put("q1_PAc_and_B", pB - q1_and, "B minus overlap")
put("q1_P_exactly_one", pAuB - q1_and)
put("q1_P_exactly_one_alt", pA + pB - 2 * q1_and, "cross-check")
put("q1_P_neither", 1 - pAuB)
put("q1_PA_given_B", q1_and / pB)
put("q1_trap_sum", pA + pB, "wrong 'union' if disjointness assumed")
assert pAuB - q1_and == pA + pB - 2 * q1_and

# ----------------------------------------------------------------- Q2 axioms
head("Q2  a proposed sample space that is wrong (three coin tosses)")
outcomes3 = ["".join(t) for t in product("HT", repeat=3)]
put("q2_n_outcomes", len(outcomes3))
cnt = {k: sum(1 for o in outcomes3 if o.count("H") == k) for k in range(4)}
put("q2_counts_by_heads", cnt)
for k in range(4):
    put(f"q2_P_{k}_heads", F(cnt[k], 8))
put("q2_uniform_claim", 0.25, "what the wrong uniform law would give each")
# proposal III omits TTT
put("q2_missing_outcome_prob", F(1, 8), "P(TTT) unaccounted for in proposal III")
put("q2_proposalIII_total", F(7, 8))
# proposal II overlap: "at least one tail" and "at least two tails" both contain e.g. HTT
put("q2_overlap_size", sum(1 for o in outcomes3 if o.count("T") >= 2))
put("q2_P_at_least_one_tail", F(sum(1 for o in outcomes3 if o.count("T") >= 1), 8))
put("q2_P_at_least_two_tails", F(sum(1 for o in outcomes3 if o.count("T") >= 2), 8))
put("q2_P_all_heads", F(1, 8))
put("q2_proposalII_total", F(1, 8) + F(7, 8) + F(4, 8), "> 1, so not a partition")

# ----------------------------------------------------------------- Q3 axioms
head("Q3  countably infinite model  P(n) = c (2/3)^(n-1)")
r = F(2, 3)
c = 1 - r  # geometric sum c/(1-r)=1
put("q3_c", c)
put("q3_P_n_ge_4", r**3, "(2/3)^3")
p_even = c * r / (1 - r * r)
put("q3_P_even", p_even)
put("q3_P_odd", 1 - p_even)
put("q3_P_n_eq_1", c)
put("q3_P_n_eq_2", c * r)
# brute partial sum sanity
s_even = sum(float(c) * float(r) ** (n - 1) for n in range(2, 400, 2))
put("q3_P_even_partialsum", s_even, "numeric check of 2/5")
assert abs(s_even - float(p_even)) < 1e-12

# ----------------------------------------------------------------- Q4 axioms
head("Q4  three-set inclusion-exclusion (course survey, 200 students)")
n_tot = 200
nA, nB, nC = 92, 78, 64
nAB, nAC, nBC = 34, 28, 22
nABC = 12
n_union = nA + nB + nC - nAB - nAC - nBC + nABC
put("q4_n_total", n_tot)
put("q4_singles_sum", nA + nB + nC)
put("q4_pairs_sum", nAB + nAC + nBC)
put("q4_nABC", nABC)
put("q4_n_union", n_union)
put("q4_P_union", F(n_union, n_tot))
put("q4_n_none", n_tot - n_union)
put("q4_P_none", F(n_tot - n_union, n_tot))
n_exactly3 = nABC
n_exactly2 = (nAB + nAC + nBC) - 3 * nABC
n_exactly1 = (nA + nB + nC) - 2 * (nAB + nAC + nBC) + 3 * nABC
put("q4_n_exactly1", n_exactly1)
put("q4_n_exactly2", n_exactly2)
put("q4_n_exactly3", n_exactly3)
put("q4_P_exactly1", F(n_exactly1, n_tot))
put("q4_P_exactly2", F(n_exactly2, n_tot))
put("q4_P_exactly3", F(n_exactly3, n_tot))
assert n_exactly1 + n_exactly2 + n_exactly3 == n_union
put("q4_trap_naive_union", F(nA + nB + nC, n_tot), "adding the three alone: 1.17 > 1")

# ----------------------------------------------------------------- Q5 axioms
head("Q5  Bonferroni / union-bound lower bound on an intersection")
n_sub, r_sub = 4, F(98, 100)
put("q5_r_each", r_sub)
put("q5_q_each", 1 - r_sub)
put("q5_bonferroni_lb", 1 - n_sub * (1 - r_sub))
put("q5_indep_value", float(r_sub) ** n_sub, "0.98^4, only if independent")
put("q5_trivial_ub", r_sub, "cannot exceed any single P(A_i)")
put("q5_gap", float(r_sub) ** n_sub - float(1 - n_sub * (1 - r_sub)))
# worst case attainability check: bound is tight when the complements are disjoint
put("q5_worst_case", 1 - n_sub * (1 - r_sub), "attained when the 4 failures are disjoint")

# ----------------------------------------------------------------- Q6 area
head("Q6  geometric probability on the unit square")
q6a = F(2, 3)  # int_0^1 (1-x^2) dx
put("q6_P_Y_ge_X2", q6a)
q6b = 1.0 - (0.5 - 0.5 * log(2.0))
put("q6_P_XY_le_half", q6b, "1 - (1/2 - (1/2)ln2)")
put("q6_ln2", log(2.0))
put("q6_P_XY_gt_half", 0.5 - 0.5 * log(2.0))
u = rng.random(N_MC)
v = rng.random(N_MC)
put("q6_mc_Y_ge_X2", float(np.mean(v >= u * u)))
put("q6_mc_XY_le_half", float(np.mean(u * v <= 0.5)))
put("q6_trap_half", 0.5, "the bogus 'by symmetry' answer for P(XY<=1/2)")

# ----------------------------------------------------------------- Q7 counting
head("Q7  anagrams of PROBABILITY")
word = "PROBABILITY"
put("q7_len", len(word))
put("q7_letter_counts", {ch: word.count(ch) for ch in sorted(set(word))})
q7_total = factorial(11) // (factorial(2) * factorial(2))
put("q7_11fact", factorial(11))
put("q7_total_arrangements", q7_total)
q7_block = factorial(10) // factorial(2)  # glue the two I's, B still doubled
put("q7_I_adjacent_count", q7_block)
put("q7_P_I_adjacent", F(q7_block, q7_total))
# brute-force check on the multiset (11!/4 is small enough only via formula; check a proxy)
proxy = "PROBAB"  # 6 letters, B twice
pr_total = len(set(permutations(proxy)))
put("q7_proxy_check", pr_total, "distinct arrangements of PROBAB = 6!/2! = 360")
assert pr_total == factorial(6) // 2

# ----------------------------------------------------------------- Q8 counting
head("Q8  committee of 5 from 9 engineers + 7 analysts")
tot8 = comb(16, 5)
put("q8_total", tot8)
e3 = comb(9, 3) * comb(7, 2)
put("q8_exactly3_eng", e3)
put("q8_P_exactly3", F(e3, tot8))
ge4 = comb(9, 4) * comb(7, 1) + comb(9, 5) * comb(7, 0)
put("q8_c94_c71", comb(9, 4) * comb(7, 1))
put("q8_c95", comb(9, 5))
put("q8_atleast4_eng", ge4)
put("q8_P_atleast4", F(ge4, tot8))
put("q8_trap_ordered_total", 16 * 15 * 14 * 13 * 12, "16!/(11!) if you wrongly order")

# ----------------------------------------------------------------- Q9 counting
head("Q9  partition 15 students into labeled groups of 4, 5, 6")
q9_tot = factorial(15) // (factorial(4) * factorial(5) * factorial(6))
put("q9_15fact", factorial(15))
put("q9_denominator", factorial(4) * factorial(5) * factorial(6))
put("q9_multinomial", q9_tot)
fav4 = comb(12, 1) * comb(11, 5)
fav5 = comb(12, 2) * comb(10, 4)
fav6 = comb(12, 3) * comb(9, 4)
put("q9_fav_group4", fav4)
put("q9_fav_group5", fav5)
put("q9_fav_group6", fav6)
q9_fav = fav4 + fav5 + fav6
put("q9_fav_total", q9_fav)
put("q9_P_three_together", F(q9_fav, q9_tot))
slick = F(comb(4, 3) + comb(5, 3) + comb(6, 3), comb(15, 3))
put("q9_slick", slick, "[C(4,3)+C(5,3)+C(6,3)]/C(15,3)")
assert slick == F(q9_fav, q9_tot)
# Monte Carlo
hits = 0
M9 = 400_000
for _ in range(M9):
    perm = rng.permutation(15)
    g = np.empty(15, dtype=np.int8)
    g[perm[:4]] = 0
    g[perm[4:9]] = 1
    g[perm[9:]] = 2
    if g[0] == g[1] == g[2]:
        hits += 1
put("q9_mc", hits / M9)

# ----------------------------------------------------------------- Q10 stars/bars
head("Q10  12 identical grants among 5 departments (stars and bars)")
put("q10_free", comb(12 + 5 - 1, 5 - 1))
put("q10_atleast1", comb(11, 4))
put("q10_distinguishable", 5**12)
put("q10_P_dept1_gets_zero", F(comb(12 + 4 - 1, 3), comb(16, 4)), "C(15,3)/C(16,4)")
put("q10_C15_3", comb(15, 3))
# brute force check of both counts
allocs = [t for t in product(range(13), repeat=5) if sum(t) == 12]
put("q10_brute_free", len(allocs))
put("q10_brute_atleast1", sum(1 for t in allocs if min(t) >= 1))
put("q10_brute_dept1_zero", sum(1 for t in allocs if t[0] == 0))
assert len(allocs) == comb(16, 4)
assert sum(1 for t in allocs if min(t) >= 1) == comb(11, 4)
assert sum(1 for t in allocs if t[0] == 0) == comb(15, 3)

# ----------------------------------------------------------------- Q11 circular
head("Q11  8 people at a round table")
put("q11_circular_total", factorial(7))
q11_adj = 2 * factorial(6)
put("q11_adj_count", q11_adj)
put("q11_P_adjacent", F(q11_adj, factorial(7)))
q11_trip = factorial(3) * factorial(5)
put("q11_triple_count", q11_trip)
put("q11_P_triple_block", F(q11_trip, factorial(7)))
put("q11_labeled_total", factorial(8))
put("q11_labeled_adj", 8 * 2 * factorial(6))
put("q11_labeled_ratio", F(8 * 2 * factorial(6), factorial(8)), "same 2/7, as it must be")
put("q11_trap_quarter", F(2 * factorial(7), factorial(8)), "the classic 1/4 mismatch error")
# brute force over labeled seatings, fixing person 0 in seat 0 (circular)
cnt_adj = cnt_tri = 0
tot_b = 0
for perm in permutations(range(1, 8)):
    seat = (0,) + perm
    pos = {p: i for i, p in enumerate(seat)}
    tot_b += 1
    d01 = (pos[0] - pos[1]) % 8
    if d01 in (1, 7):
        cnt_adj += 1
    ps = sorted([pos[0], pos[1], pos[2]])
    # three consecutive around a circle of 8
    consec = any(sorted([(s + k) % 8 for k in range(3)]) == ps for s in range(8))
    if consec:
        cnt_tri += 1
put("q11_brute_total", tot_b)
put("q11_brute_P_adjacent", F(cnt_adj, tot_b))
put("q11_brute_P_triple", F(cnt_tri, tot_b))
assert F(cnt_adj, tot_b) == F(2, 7) and F(cnt_tri, tot_b) == F(1, 7)

# ----------------------------------------------------------------- Q12 derangement
head("Q12  five letters into five envelopes (inclusion-exclusion)")
n12 = 5


def derange(n: int) -> int:
    return round(factorial(n) * sum((-1) ** k / factorial(k) for k in range(n + 1)))


put("q12_total", factorial(5))
terms = [F((-1) ** k, factorial(k)) for k in range(6)]
put("q12_ie_terms", [str(t) for t in terms])
q12_none = sum(terms)
put("q12_P_no_match", q12_none)
put("q12_D5", derange(5))
put("q12_D4", derange(4))
put("q12_exactly1_count", comb(5, 1) * derange(4))
put("q12_P_exactly1", F(comb(5, 1) * derange(4), factorial(5)))
put("q12_P_exactly2", F(comb(5, 2) * derange(3), factorial(5)))
put("q12_P_exactly3", F(comb(5, 3) * derange(2), factorial(5)))
put("q12_P_exactly5", F(1, factorial(5)))
put("q12_exp_limit", math.exp(-1.0), "1/e, the n -> infinity limit")
# brute force
fixed_counts = [0] * 6
for perm in permutations(range(5)):
    fixed_counts[sum(1 for i, v in enumerate(perm) if i == v)] += 1
put("q12_brute_fixed_counts", fixed_counts)
assert fixed_counts[0] == derange(5) == 44
assert fixed_counts[1] == 45
put("q12_trap_naive", 1 - F(1, 5), "'each letter misses w.p. 4/5 so 4/5' is nonsense")

# ----------------------------------------------------------------- Q13 keys
head("Q13  five keys, one opens, tried at random")
put("q13_P_third_no_repl", F(4, 5) * F(3, 4) * F(1, 3))
put("q13_P_first", F(1, 5))
put("q13_P_le2", F(1, 5) + F(1, 5))
put("q13_P_third_with_repl", F(4, 5) ** 2 * F(1, 5))
put("q13_P_more_than_5_with_repl", F(4, 5) ** 5)
put("q13_mean_tries_no_repl", F(1 + 2 + 3 + 4 + 5, 5))
mc13 = 0
M13 = 500_000
for _ in range(M13):
    order = rng.permutation(5)
    if order[2] == 0:
        mc13 += 1
put("q13_mc_third", mc13 / M13)

# ----------------------------------------------------------------- Q14 T/F
head("Q14  true / false about conditional probability")
# (iii) counterexample: fair die, A = {<=4}, B = {even}
faces = [1, 2, 3, 4, 5, 6]
A14 = {1, 2, 3, 4}
B14 = {2, 4, 6}
put("q14_PA_given_B", F(len(A14 & B14), len(B14)))
put("q14_PA_given_Bc", F(len(A14 - B14), 3))
put("q14_sum", F(len(A14 & B14), len(B14)) + F(len(A14 - B14), 3))
put("q14_PA", F(len(A14), 6))
# (i) illustrative numbers
put("q14_PAB_prod", F(len(A14), 6) * F(len(B14), 6))
put("q14_PAB_joint", F(len(A14 & B14), 6))

# ----------------------------------------------------------------- Q16 total prob
head("Q16  three suppliers, overall defect rate")
w = [F(50, 100), F(30, 100), F(20, 100)]
d = [F(2, 100), F(3, 100), F(5, 100)]
parts = [w[i] * d[i] for i in range(3)]
for i in range(3):
    put(f"q16_term{i+1}", parts[i])
pD = sum(parts)
put("q16_P_defective", pD)
put("q16_P_at_least_one_of_two", 1 - (1 - pD) ** 2)
put("q16_one_minus_pD_sq", (1 - pD) ** 2)
put("q16_P_S3_given_D", parts[2] / pD)
put("q16_P_S1_given_D", parts[0] / pD)
put("q16_P_S2_given_D", parts[1] / pD)
assert parts[0] / pD + parts[1] / pD + parts[2] / pD == 1
put("q16_trap_plain_average", (d[0] + d[1] + d[2]) / 3, "unweighted average of defect rates")

# ----------------------------------------------------------------- Q17 base rate
head("Q17  base rate / false positive")
prev = F(4, 1000)
sens = F(99, 100)
spec = F(97, 100)
fpr = 1 - spec
put("q17_prevalence", prev)
put("q17_sensitivity", sens)
put("q17_specificity", spec)
put("q17_fpr", fpr)
num17 = prev * sens
den17 = prev * sens + (1 - prev) * fpr
put("q17_num", num17)
put("q17_false_positive_mass", (1 - prev) * fpr)
put("q17_P_positive", den17)
put("q17_P_D_given_pos", num17 / den17)
num2 = prev * sens**2
den2 = prev * sens**2 + (1 - prev) * fpr**2
put("q17_num_two_tests", num2)
put("q17_falsemass_two_tests", (1 - prev) * fpr**2)
put("q17_P_pos_pos", den2)
put("q17_P_D_given_two_pos", num2 / den2)
put("q17_trap_accuracy", sens, "'99% accurate so P(D|+)=0.99'")
# per-1000 framing
put("q17_per100000_sick_pos", float(100000 * prev * sens))
put("q17_per100000_well_pos", float(100000 * (1 - prev) * fpr))

# ----------------------------------------------------------------- Q18 odds
head("Q18  odds form of Bayes' rule")
prior_p = F(1, 1000)
prior_odds = prior_p / (1 - prior_p)
put("q18_prior_P", prior_p)
put("q18_prior_odds", prior_odds, "1:999")
LR1 = F(1, 1) / F(2, 1000)
put("q18_P_E_given_G", F(1, 1))
put("q18_P_E_given_Gc", F(2, 1000))
put("q18_LR1", LR1)
post_odds1 = prior_odds * LR1
put("q18_post_odds1", post_odds1)
put("q18_post_P1", post_odds1 / (1 + post_odds1))
LR2 = F(20, 1)
put("q18_LR2", LR2)
post_odds2 = post_odds1 * LR2
put("q18_post_odds2", post_odds2)
put("q18_post_P2", post_odds2 / (1 + post_odds2))
put("q18_prosecutor_fallacy", F(2, 1000), "wrongly reported as P(innocent | evidence)")
# direct Bayes cross-check
direct = (prior_p * 1) / (prior_p * 1 + (1 - prior_p) * F(2, 1000))
put("q18_direct_check", direct)
assert direct == post_odds1 / (1 + post_odds1)

# ----------------------------------------------------------------- Q19 coins
head("Q19  three coins, 3 heads in 4 flips, posterior and next flip")
prior19 = [F(5, 10), F(3, 10), F(2, 10)]
bias19 = [F(3, 10), F(5, 10), F(8, 10)]
lik = [F(comb(4, 3)) * b**3 * (1 - b) for b in bias19]
for i, L in enumerate(lik):
    put(f"q19_lik_{'ABC'[i]}", L)
joint = [prior19[i] * lik[i] for i in range(3)]
for i, j in enumerate(joint):
    put(f"q19_joint_{'ABC'[i]}", j)
pE = sum(joint)
put("q19_P_evidence", pE)
post = [j / pE for j in joint]
for i, p in enumerate(post):
    put(f"q19_post_{'ABC'[i]}", p)
assert sum(post) == 1
nxt = sum(post[i] * bias19[i] for i in range(3))
put("q19_P_next_head", nxt)
put("q19_prior_mean_bias", sum(prior19[i] * bias19[i] for i in range(3)), "the tempting wrong answer")
# Monte Carlo
M19 = 2_000_000
which = rng.choice(3, size=M19, p=[0.5, 0.3, 0.2])
b_arr = np.array([0.3, 0.5, 0.8])[which]
flips = (rng.random((M19, 5)) < b_arr[:, None])
sel = flips[:, :4].sum(axis=1) == 3
put("q19_mc_P_evidence", float(sel.mean()))
put("q19_mc_post_C", float((which[sel] == 2).mean()))
put("q19_mc_next_head", float(flips[sel, 4].mean()))

# ----------------------------------------------------------------- Q20 Simpson
head("Q20  Simpson's paradox via the total probability theorem")
A_h1, A_h1_rec, A_h2, A_h2_rec = 90, 81, 10, 3
B_h1, B_h1_rec, B_h2, B_h2_rec = 20, 19, 80, 28
put("q20_A_h1_rate", F(A_h1_rec, A_h1))
put("q20_A_h2_rate", F(A_h2_rec, A_h2))
put("q20_B_h1_rate", F(B_h1_rec, B_h1))
put("q20_B_h2_rate", F(B_h2_rec, B_h2))
put("q20_A_wh1", F(A_h1, A_h1 + A_h2))
put("q20_A_wh2", F(A_h2, A_h1 + A_h2))
put("q20_B_wh1", F(B_h1, B_h1 + B_h2))
put("q20_B_wh2", F(B_h2, B_h1 + B_h2))
pA20 = F(A_h1, 100) * F(A_h1_rec, A_h1) + F(A_h2, 100) * F(A_h2_rec, A_h2)
pB20 = F(B_h1, 100) * F(B_h1_rec, B_h1) + F(B_h2, 100) * F(B_h2_rec, B_h2)
put("q20_A_overall", pA20)
put("q20_B_overall", pB20)
put("q20_A_overall_count", A_h1_rec + A_h2_rec)
put("q20_B_overall_count", B_h1_rec + B_h2_rec)
put("q20_gap_h1", F(B_h1_rec, B_h1) - F(A_h1_rec, A_h1))
put("q20_gap_h2", F(B_h2_rec, B_h2) - F(A_h2_rec, A_h2))
put("q20_gap_overall", pB20 - pA20)
assert pA20 == F(84, 100) and pB20 == F(47, 100)

# ----------------------------------------------------------------- Q21 disjoint
head("Q21  disjoint versus independent")
p21A, p21B = F(3, 10), F(45, 100)
put("q21_PA", p21A)
put("q21_PB", p21B)
put("q21_P_union_disjoint", p21A + p21B)
put("q21_PA_given_B_disjoint", F(0, 1))
put("q21_product", p21A * p21B)
put("q21_P_union_if_independent", p21A + p21B - p21A * p21B)
put("q21_difference", (p21A + p21B) - (p21A + p21B - p21A * p21B))

# ----------------------------------------------------------------- Q22 reliability
head("Q22  series-parallel system, independent components")
r1 = r2 = F(8, 10)
r3 = F(95, 100)
r4 = r5 = F(7, 10)
blockA = 1 - (1 - r1) * (1 - r2)
blockB = 1 - (1 - r4) * (1 - r5)
put("q22_blockA", blockA)
put("q22_blockB", blockB)
put("q22_r3", r3)
pw = blockA * r3 * blockB
put("q22_P_works", pw)
put("q22_P_fails", 1 - pw)
put("q22_P_3_failed_given_fail", (1 - r3) / (1 - pw))
put("q22_trap_series_pair", r1 * r2, "0.64 if you multiply a PARALLEL pair")
put("q22_trap_all_series", r1 * r2 * r3 * r4 * r5)
# Monte Carlo
M22 = 2_000_000
c1 = rng.random(M22) < 0.8
c2 = rng.random(M22) < 0.8
c3 = rng.random(M22) < 0.95
c4 = rng.random(M22) < 0.7
c5 = rng.random(M22) < 0.7
works = (c1 | c2) & c3 & (c4 | c5)
put("q22_mc_P_works", float(works.mean()))
put("q22_mc_P_3failed_given_fail", float((~c3 & ~works).sum() / (~works).sum()))

# ----------------------------------------------------------------- Q23 explaining away
head("Q23  independent but NOT conditionally independent (explaining away)")
pJ, pD23 = F(10, 100), F(5, 100)
pS = pJ + pD23 - pJ * pD23
put("q23_PJ", pJ)
put("q23_PD", pD23)
put("q23_PJD", pJ * pD23)
put("q23_PS", pS)
put("q23_PJ_given_S", pJ / pS)
put("q23_PD_given_S", pD23 / pS)
put("q23_PJD_given_S", pJ * pD23 / pS)
put("q23_product_given_S", (pJ / pS) * (pD23 / pS))
put("q23_PJ_given_S_and_D", pJ, "= P(J), i.e. drops back to the prior")
put("q23_PJ_given_S_and_notD", F(1, 1))
put("q23_drop", pJ / pS - pJ)
# Monte Carlo
M23 = 3_000_000
J = rng.random(M23) < 0.10
D = rng.random(M23) < 0.05
S = J | D
put("q23_mc_PS", float(S.mean()))
put("q23_mc_PJ_given_S", float(J[S].mean()))
put("q23_mc_PJ_given_S_D", float(J[S & D].mean()))
put("q23_mc_PJD_given_S", float((J & D)[S].mean()))

# ----------------------------------------------------------------- Q24 cond indep
head("Q24  conditionally independent given status, but NOT independent")
p24 = F(2, 10)
se24 = F(9, 10)
fp24 = F(1, 10)
p1pos = p24 * se24 + (1 - p24) * fp24
put("q24_prevalence", p24)
put("q24_sens", se24)
put("q24_fpr", fp24)
put("q24_P_T1_pos", p1pos)
both = p24 * se24**2 + (1 - p24) * fp24**2
put("q24_sick_branch", p24 * se24**2)
put("q24_well_branch", (1 - p24) * fp24**2)
put("q24_P_both_pos", both)
put("q24_product_if_independent", p1pos**2)
put("q24_P_T2_given_T1", both / p1pos)
put("q24_P_both_given_sick", se24**2)
put("q24_P_both_given_well", fp24**2)
put("q24_P_sick_given_both", p24 * se24**2 / both)
put("q24_ratio", both / p1pos**2)

# ----------------------------------------------------------------- Q25 useless test
head("Q25  independence = the observation carries no information")
p25 = F(5, 100)
rate = F(2, 10)
put("q25_prevalence", p25)
put("q25_P_pos_given_D", rate)
put("q25_P_pos_given_Dc", rate)
p25pos = p25 * rate + (1 - p25) * rate
put("q25_P_pos", p25pos)
put("q25_P_D_given_pos", p25 * rate / p25pos)
put("q25_P_D_given_neg", p25 * (1 - rate) / (1 - p25pos))
put("q25_LR", rate / rate)
put("q25_joint", p25 * rate)
put("q25_product", p25 * p25pos)

# -------------------------------------------- remaining numbers quoted in prose
head("Auxiliary numbers quoted in the question / solution prose")
put("q5_pair_failure_scale", 0.02**2, "order of a joint failure, why the union bound is tight")
put("q7_C11_2", comb(11, 2))
put("q7_adjacent_position_pairs", 10)
put("q7_position_ratio", F(10, comb(11, 2)), "10/55 = 2/11 cross-check")
put("q8_C93", comb(9, 3))
put("q8_C72", comb(7, 2))
put("q8_C16_5_numerator", 16 * 15 * 14 * 13 * 12)
put("q9_C15_3", comb(15, 3))
put("q9_C12_1", comb(12, 1))
put("q9_C11_5", comb(11, 5))
put("q9_C12_2", comb(12, 2))
put("q9_C10_4", comb(10, 4))
put("q9_C12_3", comb(12, 3))
put("q9_C9_4", comb(9, 4))
put("q9_inner_counts", [comb(4, 3), comb(5, 3), comb(6, 3)])
put("q10_C16_4_numerator", 16 * 15 * 14 * 13)
put("q10_C11_4_numerator", 11 * 10 * 9 * 8)
put("q10_C15_3_numerator", 15 * 14 * 13)
put("q10_indep_dept1_zero", (4 / 5) ** 12, "different model: each grant picks a dept")
put("q11_6fact", factorial(6))
put("q11_5fact", factorial(5))
put("q12_ie_partial", 1 - F(1, 2) + F(1, 6) - F(1, 24) + F(1, 120), "P(M>=1)")
put("q12_indep_fallacy", (4 / 5) ** 5, "the bogus (4/5)^5")
put("q12_indep_fallacy_relerr", (float(F(11, 30)) - (4 / 5) ** 5) / ((4 / 5) ** 5))
put("q12_dist_to_limit", math.exp(-1.0) - float(F(11, 30)))
put("q16_two_times_pD", 2 * float(pD))
put("q16_pD_squared", float(pD) ** 2)
put("q17_LR", sens / fpr, "0.99/0.03 = 33")
put("q17_population_ratio", float((1 - prev) / prev), "healthy-to-affected ratio")
put("q17_falsepos_to_truepos", float(((1 - prev) * fpr) / (prev * sens)))
put("q17_fallacy_factor", float(sens / (num17 / den17)))
put("q18_denominator", prior_p + (1 - prior_p) * F(2, 1000))
put("q18_innocent_branch", (1 - prior_p) * F(2, 1000))
put("q18_P_innocent_given_E", 1 - post_odds1 / (1 + post_odds1))
put("q18_fallacy_factor", float((1 - post_odds1 / (1 + post_odds1)) / F(2, 1000)))
put("q19_binom_coef", comb(4, 3))
put("q20_h2_easy_gap", F(9, 10) - F(3, 10), "range the weights can move the average over")
put("q22_parallel1_fail", F(2, 10) ** 2)
put("q22_parallel2_fail", F(3, 10) ** 2)
put("q22_partial_product", F(96, 100) * F(95, 100))
put("q23_JD_prod_check", pJ * pD23, "= P(J)P(D), independence holds unconditionally")
put("q23_ratio_cond", float((pJ / pS) * (pD23 / pS) / (pJ * pD23 / pS)))
put("q23_J_and_notD", pJ * (1 - pD23))
put("q24_P_C_given_T1", p24 * se24 / p1pos)
put("q25_useful_LR_example", F(20, 100) / F(5, 100), "sens .20, fpr .05 -> LR 4")
put("q25_P_Yc", 1 - p25pos)
put("q25_C_and_Yc", p25 * (1 - rate))

# ----------------------------------------------------------------- write
out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(R, indent=1, sort_keys=True), encoding="utf-8")
print(f"\nwrote {out}  ({len(R)} keys)")
