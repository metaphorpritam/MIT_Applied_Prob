# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Every number quoted in notes/src/fragments/qb_s2.html
(question bank section 2 - discrete random variables, Q26-Q47).

Run:  uv run computes/qb_s2.py
Writes computes/qb_s2.json.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict[str, object] = {}
rng = np.random.default_rng(20260814)


def put(key: str, val, note: str = "") -> None:
    v = float(val) if isinstance(val, F) else val
    R[key] = v
    extra = f"   # {note}" if note else ""
    print(f"{key:34s} = {v}{extra}")


def sec(t: str) -> None:
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


# ---------------------------------------------------------------- Q26
sec("Q26 - PMF of the larger of two chips drawn from {1,...,5}")
pairs = list(combinations(range(1, 6), 2))
put("q26_n_pairs", len(pairs))
pmf26 = {}
for a, b in pairs:
    m = max(a, b)
    pmf26[m] = pmf26.get(m, F(0)) + F(1, len(pairs))
for x in sorted(pmf26):
    put(f"q26_pmf_{x}", pmf26[x])
put("q26_pmf_total", sum(pmf26.values()))
E26 = sum(F(x) * pmf26[x] for x in pmf26)
put("q26_EX", E26, "= 40/10")
put("q26_P_ge_4", pmf26[4] + pmf26[5])
E26sq = sum(F(x * x) * pmf26[x] for x in pmf26)
put("q26_EX2", E26sq)
put("q26_var", E26sq - E26**2)

# ---------------------------------------------------------------- Q27
sec("Q27 - which named family applies")
put("q27_geom_p", 0.04)
put("q27_geom_mean", 1 / 0.04)
put("q27_geom_var", (1 - 0.04) / 0.04**2)
put("q27_bin_mean", 12 * 0.7)
put("q27_bin_var", 12 * 0.7 * 0.3)
a27, b27 = 1, 20
put("q27_unif_mean", (a27 + b27) / 2)
put("q27_unif_var", (b27 - a27) * (b27 - a27 + 2) / 12, "(b-a)(b-a+2)/12")
# hypergeometric: 10 fuses, 3 bad, draw 4 without replacement
hyp = {k: F(comb(3, k) * comb(7, 4 - k), comb(10, 4)) for k in range(0, 4)}
for k in sorted(hyp):
    put(f"q27_hyp_P{k}", hyp[k])
put("q27_hyp_total", sum(hyp.values()))
put("q27_hyp_mean", sum(F(k) * hyp[k] for k in hyp), "= 4 * 3/10 by indicators")
put("q27_bin_wrong_P1", comb(4, 1) * 0.3 * 0.7**3, "binomial answer for the same query")
put("q27_hyp_P1_dec", float(hyp[1]))

# ---------------------------------------------------------------- Q28
sec("Q28 - E[60/X] vs 60/E[X], X uniform on {1,...,5}")
xs28 = range(1, 6)
E28 = sum(F(x) for x in xs28) / 5
put("q28_EX", E28)
E28_inv = sum(F(1, x) for x in xs28) / 5
put("q28_E_inv_X", E28_inv, "= 137/300")
put("q28_E_60_over_X", 60 * E28_inv, "= 27.4")
put("q28_60_over_EX", 60 / float(E28), "the tempting wrong answer")
put("q28_gap", 60 * float(E28_inv) - 60 / float(E28))

# ---------------------------------------------------------------- Q29
sec("Q29 - var(aX+b)")
EX29, var29, a29, b29 = 3.0, 4.0, -2.0, 7.0
put("q29_EY", a29 * EX29 + b29)
put("q29_varY", a29**2 * var29)
put("q29_sdX", var29**0.5)
put("q29_sdY", (a29**2 * var29) ** 0.5, "= |a| * sd(X)")
put("q29_wrong_sd", a29 * var29**0.5, "the sign-carrying wrong answer")

# ---------------------------------------------------------------- Q30
sec("Q30 - geometric memorylessness, p = 0.2")
p30 = F(1, 5)
q30 = 1 - p30
put("q30_P_gt_4", q30**4)
put("q30_P_gt_7", q30**7)
put("q30_P_cond", q30**7 / q30**4, "= P(X>3) = 0.8^3")
put("q30_P_gt_3", q30**3)
put("q30_E_cond", 4 + 1 / p30, "= 4 + 1/p")
put("q30_P_X7_given", q30**6 * p30 / q30**4, "= 0.8^2 * 0.2")
put("q30_E_uncond", 1 / p30)
# Monte-Carlo
n30 = 400_000
g = rng.geometric(0.2, n30)
put("q30_mc_cond", float(np.mean(g[g > 4] > 7)))
put("q30_mc_Econd", float(np.mean(g[g > 4])))

# ---------------------------------------------------------------- Q31
sec("Q31 - joint PMF table (units of 1/20)")
tab31 = {(1, 0): 2, (1, 1): 1, (1, 2): 1,
         (2, 0): 1, (2, 1): 3, (2, 2): 4,
         (3, 0): 3, (3, 1): 4, (3, 2): 1}
put("q31_total_units", sum(tab31.values()))
pX31 = {x: F(sum(v for (a, b), v in tab31.items() if a == x), 20) for x in (1, 2, 3)}
pY31 = {y: F(sum(v for (a, b), v in tab31.items() if b == y), 20) for y in (0, 1, 2)}
for x in pX31:
    put(f"q31_pX_{x}", pX31[x])
for y in pY31:
    put(f"q31_pY_{y}", pY31[y])
EX31 = sum(F(x) * pX31[x] for x in pX31)
put("q31_EX", EX31, "= 44/20")
cond31 = {x: F(tab31[(x, 1)], 20) / pY31[1] for x in (1, 2, 3)}
for x in cond31:
    put(f"q31_pXgivenY1_{x}", cond31[x])
put("q31_cond_total", sum(cond31.values()))
put("q31_E_X_given_Y1", sum(F(x) * cond31[x] for x in cond31))
put("q31_indep_check_11", float(pX31[1] * pY31[1]), "vs joint 1/20 = 0.05")
put("q31_unnormalized_trap", sum(F(x) * F(tab31[(x, 1)], 20) for x in (1, 2, 3)),
    "the forgot-to-renormalize wrong answer, = E[X|Y=1] * p_Y(1)")

# ---------------------------------------------------------------- Q32
sec("Q32 - total expectation over two job types")
E32_t1 = sum(F(x) for x in range(1, 6)) / 5
put("q32_E_type1", E32_t1)
put("q32_E_type2", 1 / F(1, 4), "geometric(0.25) mean")
E32 = F(2, 5) * E32_t1 + F(3, 5) * 4
put("q32_EX", E32, "= 0.4*3 + 0.6*4")
p32_2 = F(2, 5) * F(1, 5) + F(3, 5) * (F(3, 4) * F(1, 4))
put("q32_P_X_eq_2_t1", F(2, 5) * F(1, 5))
put("q32_P_X_eq_2_t2", F(3, 5) * F(3, 4) * F(1, 4))
put("q32_P_X_eq_2", p32_2)
put("q32_wrong_avg", 3.5, "the (3+4)/2 wrong answer")

# ---------------------------------------------------------------- Q33
sec("Q33 - binomial n=6, p=0.3: pmf, mode, mean, variance")
n33, p33 = 6, 0.3
pmf33 = {k: comb(n33, k) * p33**k * (1 - p33) ** (n33 - k) for k in range(n33 + 1)}
for k in pmf33:
    put(f"q33_P{k}", pmf33[k])
put("q33_total", sum(pmf33.values()))
put("q33_mean", n33 * p33)
put("q33_var", n33 * p33 * (1 - p33))
put("q33_ratio_k2", ((n33 - 2 + 1) / 2) * (p33 / (1 - p33)), "p(2)/p(1)")
put("q33_ratio_k3", ((n33 - 3 + 1) / 3) * (p33 / (1 - p33)), "p(3)/p(2)")
put("q33_np1p", (n33 + 1) * p33, "floor gives the mode")
put("q33_mode", max(pmf33, key=lambda k: pmf33[k]))

# ---------------------------------------------------------------- Q34
sec("Q34 - elevator stops: 5 passengers, 8 floors, indicators")
n34, m34 = 5, 8
p_stop = 1 - (F(7, 8)) ** n34
put("q34_q_pow", F(7, 8) ** n34, "= 16807/32768")
put("q34_p_one_floor", p_stop)
put("q34_E_stops", m34 * p_stop)
put("q34_wrong_5", 5, "the 'one stop per passenger' wrong answer")
put("q34_wrong_uniform", m34 * n34 / m34, "the 8 * 5/8 wrong answer")
# Monte-Carlo
n_mc = 200_000
draws = rng.integers(0, 8, size=(n_mc, 5))
stops = np.array([len(set(row)) for row in draws[:20000]])
put("q34_mc_E_stops", float(stops.mean()), "20k trials")

# ---------------------------------------------------------------- Q35
sec("Q35 - expected-value rule with g(x) = 3x - 0.5x^2")
pmf35 = {0: F(1, 10), 1: F(2, 10), 2: F(4, 10), 3: F(3, 10)}
put("q35_total", sum(pmf35.values()))
EX35 = sum(F(x) * pmf35[x] for x in pmf35)
EX35sq = sum(F(x * x) * pmf35[x] for x in pmf35)
put("q35_EX", EX35)
put("q35_EX2", EX35sq)
put("q35_var", EX35sq - EX35**2)
Eg35 = sum((3 * F(x) - F(1, 2) * F(x * x)) * pmf35[x] for x in pmf35)
put("q35_Eg", Eg35)
gE35 = 3 * EX35 - F(1, 2) * EX35**2
put("q35_g_of_EX", gE35, "the wrong answer")
put("q35_gap", gE35 - Eg35)
put("q35_half_var", F(1, 2) * (EX35sq - EX35**2), "equals the gap")

# ---------------------------------------------------------------- Q36
sec("Q36 - variance of a PMF and of a linear transform")
pmf36 = {0: F(2, 10), 1: F(5, 10), 2: F(2, 10), 3: F(1, 10)}
put("q36_total", sum(pmf36.values()))
EX36 = sum(F(x) * pmf36[x] for x in pmf36)
EX36sq = sum(F(x * x) * pmf36[x] for x in pmf36)
var36 = EX36sq - EX36**2
put("q36_EX", EX36)
put("q36_EX2", EX36sq)
put("q36_var", var36)
put("q36_sd", float(var36) ** 0.5)
put("q36_ET", 40 * float(EX36) + 5)
put("q36_varT", 1600 * float(var36))
put("q36_sdT", (1600 * float(var36)) ** 0.5)
put("q36_wrong_varT", 1600 * float(var36) + 5, "adding b to the variance")

# ---------------------------------------------------------------- Q37
sec("Q37 - E[min(X,m)] for geometric X via the recursion a_m = 1 + q a_{m-1}")
p37 = F(3, 10)
q37 = 1 - p37
a = F(0)
for m in range(1, 5):
    a = 1 + q37 * a
    put(f"q37_a{m}", a)
closed = (1 - q37**4) / p37
put("q37_closed_form", closed, "(1-q^4)/p")
put("q37_q4", q37**4)
put("q37_E_untruncated", 1 / p37)
# brute force check
brute = sum(min(k, 4) * float(q37) ** (k - 1) * float(p37) for k in range(1, 2000))
put("q37_brute", brute)

# ---------------------------------------------------------------- Q38
sec("Q38 - independence check on a 2x3 joint PMF (units of 1/24)")
tab38 = {(0, 0): 2, (0, 1): 4, (0, 2): 6,
         (1, 0): 4, (1, 1): 2, (1, 2): 6}
put("q38_total_units", sum(tab38.values()))
pX38 = {x: F(sum(v for (a, b), v in tab38.items() if a == x), 24) for x in (0, 1)}
pY38 = {y: F(sum(v for (a, b), v in tab38.items() if b == y), 24) for y in (0, 1, 2)}
for x in pX38:
    put(f"q38_pX_{x}", pX38[x])
for y in pY38:
    put(f"q38_pY_{y}", pY38[y])
for (x, y), v in sorted(tab38.items()):
    put(f"q38_joint_{x}{y}", F(v, 24))
    put(f"q38_prod_{x}{y}", pX38[x] * pY38[y])
EX38 = sum(F(x) * pX38[x] for x in pX38)
EY38 = sum(F(y) * pY38[y] for y in pY38)
EXY38 = sum(F(x * y) * F(v, 24) for (x, y), v in tab38.items())
put("q38_EX", EX38)
put("q38_EY", EY38)
put("q38_EXY", EXY38)
put("q38_EX_EY", EX38 * EY38)
put("q38_cov", EXY38 - EX38 * EY38)

# ---------------------------------------------------------------- Q39
sec("Q39 - N uniform on {1,2,3}, then N fair tosses, X = heads")
pmf39 = {k: F(0) for k in range(4)}
for n in (1, 2, 3):
    for k in range(n + 1):
        pmf39[k] += F(1, 3) * F(comb(n, k), 2**n)
for k in sorted(pmf39):
    put(f"q39_pX_{k}", pmf39[k])
put("q39_total", sum(pmf39.values()))
EX39 = sum(F(k) * pmf39[k] for k in pmf39)
EX39sq = sum(F(k * k) * pmf39[k] for k in pmf39)
put("q39_EX", EX39)
put("q39_EX2", EX39sq)
put("q39_var", EX39sq - EX39**2)
put("q39_EN", F(2))
put("q39_check_EX_via_TET", F(1, 3) * (F(1, 2) + F(2, 2) + F(3, 2)))
put("q39_wrong_var", float(F(2) * F(1, 4)), "E[N]p(1-p): ignores randomness of N")
# Monte-Carlo
n_mc39 = 400_000
Ns = rng.integers(1, 4, n_mc39)
Xs = np.array([rng.binomial(n, 0.5) for n in Ns[:40000]])
put("q39_mc_EX", float(Xs.mean()), "40k trials")
put("q39_mc_var", float(Xs.var()))

# ---------------------------------------------------------------- Q40
sec("Q40 - inverting a size-biased sample: shuttle vans of 8, 12, 20, 40")
# The question GIVES only the rider-sampled PMF; the sizes/fleet are recovered from it.
sizes = [8, 12, 20, 40]
T = sum(sizes)                      # recovered from p_X(n) = n/T
k40 = len(sizes)                    # recovered from E[1/X] = k/T
put("q40_total_riders", T)
put("q40_num_vans", k40)
for s in sizes:
    put(f"q40_pX_{s}", F(s, T))
put("q40_pX_total", sum(F(s, T) for s in sizes))
put("q40_recover_T_from_smallest", F(sizes[0]) / F(sizes[0], T), "n / p_X(n) = T for every n")
EY40 = F(T, k40)
put("q40_EY", EY40, "van sampled uniformly = T/k")
EX40 = F(sum(s * s for s in sizes), T)
put("q40_sum_sq", sum(s * s for s in sizes))
put("q40_EX", EX40, "rider sampled uniformly")
EY40sq = F(sum(s * s for s in sizes), k40)
varY40 = EY40sq - EY40**2
put("q40_EY2", EY40sq)
put("q40_varY", varY40)
put("q40_sdY", float(varY40) ** 0.5)
put("q40_identity", EY40 + varY40 / EY40, "must equal q40_EX")
E_inv_X40 = sum(F(s, T) * F(1, s) for s in sizes)
put("q40_E_inv_X", E_inv_X40, "= k/T = 1/E[Y]")
put("q40_k_recovered", E_inv_X40 * T, "k = T * E[1/X], must equal q40_num_vans")
put("q40_inv_E_inv_X", 1 / E_inv_X40, "= E[Y] exactly")
E_inv_Y40 = sum(F(1, k40) * F(1, s) for s in sizes)
put("q40_E_inv_Y", E_inv_Y40)
put("q40_harmonic_mean_Y", 1 / E_inv_Y40, "1/E[1/Y] is the harmonic mean, NOT E[Y]")
put("q40_excess_pct", 100 * (float(EX40) / float(EY40) - 1))

# ---------------------------------------------------------------- Q41
sec("Q41 - spot the error: uncorrelated but dependent (X in {-1,0,1}, Y=|X|)")
sup41 = [-1, 0, 1]
EX41 = sum(F(x, 3) for x in sup41)
EY41 = sum(F(abs(x), 3) for x in sup41)
EXY41 = sum(F(x * abs(x), 3) for x in sup41)
put("q41_EX", EX41)
put("q41_EY", EY41)
put("q41_EXY", EXY41)
put("q41_EX_EY", EX41 * EY41)
put("q41_cov", EXY41 - EX41 * EY41)
put("q41_P_X0_Y0_true", F(1, 3))
put("q41_P_X0_times_P_Y0", F(1, 3) * F(1, 3), "the claimed value")
put("q41_P_Y0", F(1, 3))
put("q41_P_Y0_given_X0", F(1))
EX41sq = sum(F(x * x, 3) for x in sup41)
put("q41_varX", EX41sq - EX41**2)
EY41sq = sum(F(x * x, 3) for x in sup41)
put("q41_varY", EY41sq - EY41**2)
S41 = [x + abs(x) for x in sup41]
ES = sum(F(s, 3) for s in S41)
ESsq = sum(F(s * s, 3) for s in S41)
put("q41_var_sum", ESsq - ES**2, "equals varX+varY since cov=0")

# ---------------------------------------------------------------- Q42
sec("Q42 - true/false items (numbers reused)")
put("q42_var_2X_minus_5", 4.0, "coefficient a^2 with a = 2")
put("q42_E_inv_example_E_inv", float(E28_inv))
put("q42_E_inv_example_inv_E", 1 / float(E28))
# item (e): the St. Petersburg payout, value 2^k with probability 2^-k (G2 s2.6)
put("q42_stpete_term", 1, "every term 2^k * 2^-k contributes exactly 1")
for m in (10, 30, 100):
    put(f"q42_stpete_partial_{m}", float(sum(2**k * F(1, 2**k) for k in range(1, m + 1))),
        f"partial sum of E[W] to k = {m}")
put("q42_stpete_total_prob", float(sum(F(1, 2**k) for k in range(1, 200))),
    "the probabilities do sum to 1")

# ---------------------------------------------------------------- Q43
sec("Q43 - minimum of two independent geometrics (p=0.25, q=0.40)")
pa, pb = F(1, 4), F(2, 5)
fail = (1 - pa) * (1 - pb)
put("q43_fail_per_round", fail, "= 0.75 * 0.60")
pT = 1 - fail
put("q43_pT", pT)
put("q43_ET", 1 / pT)
put("q43_varT", (1 - pT) / pT**2)
put("q43_P_T3", fail**2 * pT)
put("q43_P_T_gt_2", fail**2)
# part (a): the PMF built from first principles (G2 s1.5)
for k in (1, 2, 3, 4):
    put(f"q43_pmf_{k}", fail ** (k - 1) * pT, f"(0.45)^{k - 1} * 0.55")
put("q43_pmf_tail_sum", sum(fail ** (k - 1) * pT for k in range(1, 400)),
    "the geometric series sums to 1")
put("q43_wrong_min_mean", min(float(1 / pa), float(1 / pb)), "the min-of-means wrong answer")
put("q43_wrong_sum_p", float(pa + pb), "the added-probabilities wrong answer")
n43 = 300_000
ga = rng.geometric(0.25, n43)
gb = rng.geometric(0.40, n43)
put("q43_mc_ET", float(np.minimum(ga, gb).mean()))
put("q43_mc_varT", float(np.minimum(ga, gb).var()))

# ---------------------------------------------------------------- Q44
sec("Q44 - expected fair-coin flips until the pattern HT")
# states: 0 = no pending H, 1 = last flip was H
E1 = F(2)          # E1 = 1 + (1/2)E1  ->  E1 = 2
E0 = 2 * (1 + F(1, 2) * E1)  # (1/2)E0 = 1 + (1/2)E1
put("q44_E1", E1)
put("q44_E0", E0)
# HH comparison
# A = 1 + (1/2)B + (1/2)A ; B = 1 + (1/2)*0 + (1/2)A
A, B = None, None
# solve: A = 2 + B ; B = 1 + A/2  -> A = 2 + 1 + A/2 -> A/2 = 3 -> A = 6
A = F(6)
B = 1 + A / 2
put("q44_HH_E", A)
put("q44_HH_B", B)
put("q44_diff", A - E0)


def mc_pattern(pat: str, trials: int = 200_000) -> float:
    tot = 0
    for _ in range(trials):
        prev = ""
        n = 0
        while True:
            c = "H" if rng.random() < 0.5 else "T"
            n += 1
            if prev + c == pat:
                break
            prev = c
        tot += n
    return tot / trials


put("q44_mc_HT", mc_pattern("HT", 60_000), "60k trials")
put("q44_mc_HH", mc_pattern("HH", 60_000), "60k trials")

# ---------------------------------------------------------------- Q45
sec("Q45 - X = # of adjacent HH pairs in 5 fair tosses")
n45 = 5
outcomes = list(product("HT", repeat=n45))


def count_hh(seq) -> int:
    return sum(1 for i in range(len(seq) - 1) if seq[i] == "H" and seq[i + 1] == "H")


vals = [count_hh(s) for s in outcomes]
pmf45 = {}
for v in vals:
    pmf45[v] = pmf45.get(v, F(0)) + F(1, len(outcomes))
for v in sorted(pmf45):
    put(f"q45_pmf_{v}", pmf45[v])
put("q45_total", sum(pmf45.values()))
EX45 = sum(F(v) * pmf45[v] for v in pmf45)
EX45sq = sum(F(v * v) * pmf45[v] for v in pmf45)
put("q45_EX", EX45, "= 4 * 1/4")
put("q45_EX2", EX45sq)
put("q45_var", EX45sq - EX45**2)
put("q45_n_indicators", n45 - 1)
put("q45_p_indicator", F(1, 4))
put("q45_adjacent_ordered_pairs", 6)
put("q45_adjacent_EIiIj", F(1, 8), "three consecutive heads")
put("q45_disjoint_ordered_pairs", 6)
put("q45_disjoint_EIiIj", F(1, 16))
put("q45_cross_sum", 6 * F(1, 8) + 6 * F(1, 16))
put("q45_wrong_binomial_var", 4 * 0.25 * 0.75, "the 'independent indicators' wrong answer")
# Monte-Carlo
n45mc = 300_000
tosses = rng.integers(0, 2, size=(n45mc, 5))
hh = ((tosses[:, :-1] == 1) & (tosses[:, 1:] == 1)).sum(axis=1)
put("q45_mc_EX", float(hh.mean()))
put("q45_mc_var", float(hh.var()))

# ---------------------------------------------------------------- Q46
sec("Q46 - coupon collector: three equally likely toy types, T = boxes to get all three")
n46_types = 3
ps = [F(n46_types - i, n46_types) for i in range(n46_types)]   # 1, 2/3, 1/3
for i, pi in enumerate(ps, start=1):
    put(f"q46_p{i}", pi)
    put(f"q46_E_T{i}", 1 / pi)
    put(f"q46_var_T{i}", (1 - pi) / pi**2)
ET46 = sum(1 / pi for pi in ps)
put("q46_ET", ET46, "= 3 * (1 + 1/2 + 1/3) = 11/2")
put("q46_harmonic", sum(F(1, k) for k in range(1, n46_types + 1)), "= 11/6")
varT46 = sum((1 - pi) / pi**2 for pi in ps)
put("q46_varT", varT46)
put("q46_sdT", float(varT46) ** 0.5)
put("q46_P_T3", ps[1] * ps[2], "the fastest possible collection: 1 * (2/3) * (1/3)")
put("q46_wrong_3", 3, "the 'three types, three boxes' wrong answer")
put("q46_wrong_gap", float(ET46) - 3)
put("q46_last_stage_share_mean", float((1 / ps[2]) / ET46), "fraction of E[T] in the last stage")
put("q46_last_stage_share_var", float(((1 - ps[2]) / ps[2] ** 2) / varT46))
# Monte-Carlo: simulate the collection directly (no stage decomposition assumed)
n46 = 50_000
boxes46 = rng.integers(0, n46_types, size=(n46, 40))
t46 = np.empty(n46, dtype=np.int64)
for r in range(n46):
    seen = set()
    row = boxes46[r]
    for j, b in enumerate(row):
        seen.add(int(b))
        if len(seen) == n46_types:
            t46[r] = j + 1
            break
    else:
        t46[r] = len(row)
put("q46_mc_ET", float(t46.mean()), "50k simulated collections")
put("q46_mc_varT", float(t46.var()))
put("q46_mc_P_T3", float((t46 == 3).mean()))

# ---------------------------------------------------------------- Q47
sec("Q47 - tail-sum formula, applied to the max of two fair dice")
pmf47 = {m: F(2 * m - 1, 36) for m in range(1, 7)}
for m in pmf47:
    put(f"q47_pmf_{m}", pmf47[m])
put("q47_total", sum(pmf47.values()))
EM_direct = sum(F(m) * pmf47[m] for m in pmf47)
put("q47_E_direct", EM_direct, "= 161/36")
tails = {k: 1 - F((k - 1) ** 2, 36) for k in range(1, 7)}
for k in tails:
    put(f"q47_tail_{k}", tails[k], f"P(M >= {k})")
put("q47_E_tailsum", sum(tails.values()))
put("q47_sum_squares", sum((k - 1) ** 2 for k in range(1, 7)))
put("q47_E_decimal", float(EM_direct))
put("q47_wrong_35", 3.5, "the E[single die] wrong answer")
# Monte-Carlo
d1 = rng.integers(1, 7, 400_000)
d2 = rng.integers(1, 7, 400_000)
put("q47_mc_EM", float(np.maximum(d1, d2).mean()))

# ------------------------------------------------- derived figures quoted in prose
sec("Derived figures quoted in the fragment prose")
put("q27_P1_error", float(hyp[1]) - comb(4, 1) * 0.3 * 0.7**3, "0.5 - 0.4116")
put("q28_overshoot_pct", 100 * (60 * float(E28_inv) / (60 / float(E28)) - 1))
put("q35_gap_dollars", 100 * float(gE35 - Eg35), "hundreds of dollars -> dollars")
put("q37_saving", float(1 / p37) - float(closed))
put("q37_fail_prob", float(q37**4))
put("q43_both_succeed", float(pa * pb))
put("q43_check_inclusion_exclusion", float(pa + pb - pa * pb), "must equal q43_pT")
put("q45_var_gap", 1.125 - 4 * 0.25 * 0.75)
put("q47_excess_over_single_die", float(EM_direct) - 3.5)
put("q47_single_die_mean", 3.5)

# ---------------------------------------------------------------- write
out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(R, indent=1, sort_keys=True), encoding="utf-8")
print(f"\nWrote {out} with {len(R)} keys.")
