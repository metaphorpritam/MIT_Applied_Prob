# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Numbers for G4 section 2 — random sums and the Bernoulli process.

Sources: L12 slides 7-8, L13 slides 1-8, rec13 problems 1-3, B&T section 4.5 and 6.1.

Run:  uv run computes/g4_s2.py
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT: dict[str, object] = {}


def rec(key, val, note=""):
    if isinstance(val, Fraction):
        val = float(val)
    OUT[key] = val
    print(f"{key:38s} = {val!r}   {note}")


print("=" * 74)
print("A. rec13 P2 — breaking a stick twice (also B&T Example 4.17)")
print("=" * 74)
# X = ell * U1 * U2 with U1,U2 iid Uniform(0,1)
ell = 1.0
E_U = Fraction(1, 2)
E_U2 = Fraction(1, 3)
E_X2break = ell * float(E_U ** 2)
E_X2sq = ell ** 2 * float(E_U2 ** 2)
var_X2break = E_X2sq - E_X2break ** 2
rec("stick2_EX_over_ell", E_X2break, "E[X]/ell = 1/4")
rec("stick2_EX2_over_ell2", E_X2sq, "E[X^2]/ell^2 = 1/9")
rec("stick2_var_over_ell2", var_X2break, "var(X)/ell^2 = 7/144")
rec("stick2_var_frac", float(Fraction(7, 144)), "7/144")
rec("stick2_Evar_term", float(Fraction(1, 36)), "E[var(X|Y)] = ell^2/36")
rec("stick2_varE_term", float(Fraction(1, 48)), "var(E[X|Y]) = ell^2/48")
rec("stick2_sum_check", float(Fraction(1, 36) + Fraction(1, 48)), "should equal 7/144")

rng = np.random.default_rng(6041)
NMC = 4_000_000
u = rng.random((NMC, 2))
x2 = u[:, 0] * u[:, 1]
rec("stick2_mc_mean", round(float(x2.mean()), 6), "Monte Carlo E[X], ell=1")
rec("stick2_mc_var", round(float(x2.var()), 6), "Monte Carlo var(X), ell=1")

# three breaks (practice)
E_X3 = float(E_U ** 3)
E_X3sq = float(E_U2 ** 3)
var_X3 = E_X3sq - E_X3 ** 2
rec("stick3_EX_over_ell", E_X3, "1/8")
rec("stick3_EX2_over_ell2", E_X3sq, "1/27")
rec("stick3_var_over_ell2", var_X3, "37/1728")
rec("stick3_var_frac", float(Fraction(37, 1728)), "37/1728")
x3 = x2 * rng.random(NMC)
rec("stick3_mc_var", round(float(x3.var()), 6), "Monte Carlo var, ell=1")

print()
print("=" * 74)
print("B. L12 slide 7-8 — random sum Y = X_1 + ... + X_N (shopping example)")
print("=" * 74)
# concrete instance: N uniform on {1,...,5}; X_i mean 100, var 400
EX, varX = 100.0, 400.0
nvals = np.arange(1, 6)
pN = np.full(5, 1 / 5)
EN = float((nvals * pN).sum())
EN2 = float((nvals ** 2 * pN).sum())
varN = EN2 - EN ** 2
rec("shop_EX", EX, "E[X] dollars per store")
rec("shop_varX", varX, "var(X)")
rec("shop_sdX", math.sqrt(varX))
rec("shop_EN", EN, "E[N], N uniform on {1..5}")
rec("shop_EN2", EN2)
rec("shop_varN", varN, "var(N) = 2")
EY = EN * EX
term_within = EN * varX
term_between = EX ** 2 * varN
varY = term_within + term_between
rec("shop_EY", EY, "E[N]E[X]")
rec("shop_term_within", term_within, "E[N] var(X)")
rec("shop_term_between", term_between, "(E[X])^2 var(N)")
rec("shop_varY", varY)
rec("shop_sdY", round(math.sqrt(varY), 4))
rec("shop_between_share", round(term_between / varY, 4), "fraction of var(Y) from randomness in N")

# Monte Carlo cross-check with X_i ~ Uniform(100-sqrt(1200), 100+sqrt(1200)) (mean 100, var 400)
half = math.sqrt(3 * varX)
M = 2_000_000
Ns = rng.integers(1, 6, size=M)
maxN = 5
Xs = 100.0 + (rng.random((M, maxN)) * 2 - 1) * half
mask = (np.arange(maxN)[None, :] < Ns[:, None])
Ys = (Xs * mask).sum(axis=1)
rec("shop_mc_EY", round(float(Ys.mean()), 3))
rec("shop_mc_varY", round(float(Ys.var()), 1))

print()
print("=" * 74)
print("C. rec13 P3 — widgets in boxes in a crate")
print("=" * 74)
EXw, varXw, ENw, varNw = 10.0, 16.0, 10.0, 16.0
ETw = ENw * EXw
w_within = ENw * varXw
w_between = EXw ** 2 * varNw
varTw = w_within + w_between
rec("crate_ET", ETw)
rec("crate_within", w_within, "E[N]var(X) = 10*16")
rec("crate_between", w_between, "(E[X])^2 var(N) = 100*16")
rec("crate_varT", varTw)
rec("crate_sdT", round(math.sqrt(varTw), 4))
rec("crate_wrong_varT", ENw * varXw + 0.0, "the common WRONG answer (forgetting var(N) term)")
rec("crate_ratio", round(w_between / w_within, 4), "between/within")

print()
print("=" * 74)
print("D. B&T Example 4.35 — geometric number of exponentials (mean/variance only)")
print("=" * 74)
p_g, lam = 0.2, 0.5
EN_g = 1 / p_g
varN_g = (1 - p_g) / p_g ** 2
EX_g = 1 / lam
varX_g = 1 / lam ** 2
EY_g = EN_g * EX_g
varY_g = EN_g * varX_g + EX_g ** 2 * varN_g
rec("bk_p", p_g)
rec("bk_lam", lam)
rec("bk_EN", EN_g)
rec("bk_varN", varN_g)
rec("bk_EX", EX_g)
rec("bk_varX", varX_g)
rec("bk_EY", EY_g, "= 1/(p*lambda)")
rec("bk_varY", varY_g, "= 1/(p*lambda)^2")
rec("bk_closed_EY", 1 / (p_g * lam))
rec("bk_closed_varY", 1 / (p_g * lam) ** 2)
rec("bk_rate", p_g * lam, "Y is exponential with parameter p*lambda")

print()
print("=" * 74)
print("E. Bernoulli process basics (L13 slides 2-4)")
print("=" * 74)
p = 0.3
n = 20
rec("bp_p", p)
rec("bp_n", n)
rec("bp_EXt", p, "E[X_t]")
rec("bp_varXt", round(p * (1 - p), 4), "var(X_t) = p(1-p)")
rec("bp_ES", n * p, "E[S] = np")
rec("bp_varS", round(n * p * (1 - p), 4), "var(S) = np(1-p)")
rec("bp_sdS", round(math.sqrt(n * p * (1 - p)), 4))
for k in (0, 3, 6, 10):
    rec(f"bp_pS_{k}", round(math.comb(n, k) * p ** k * (1 - p) ** (n - k), 6),
        f"P(S={k}), n=20 p=0.3")
rec("bp_all_ones_20", float(f"{p ** 20:.4g}"), "P(X_t=1 for t=1..20)")
rec("bp_all_ones_5", round(p ** 5, 6), "P(X_t=1 for t=1..5)")
rec("bp_all_ones_limit", 0.0, "limit of p^n as n->inf, p<1")

print()
print("=" * 74)
print("F. Interarrival times / memorylessness (L13 slide 5)")
print("=" * 74)
rec("geo_ET1", round(1 / p, 6), "E[T1] = 1/p")
rec("geo_varT1", round((1 - p) / p ** 2, 6), "var(T1) = (1-p)/p^2")
rec("geo_sdT1", round(math.sqrt((1 - p) / p ** 2), 4))
for t in (1, 2, 3, 5):
    rec(f"geo_pT1_{t}", round((1 - p) ** (t - 1) * p, 6), f"P(T1={t})")
rec("geo_tail_5", round((1 - p) ** 5, 6), "P(T1 > 5) = (1-p)^5")
rec("geo_cond_check", round(((1 - p) ** (5 + 3 - 1) * p) / ((1 - p) ** 5), 8),
    "P(T1=8 | T1>5) should equal P(T1=3)")
rec("geo_pT1_3_again", round((1 - p) ** 2 * p, 8))

# lottery: length L of first string of losing days (UNSOLVED EXAMPLE, L13 slide 5)
rec("lot_p", p)
for l_ in (0, 1, 2, 5):
    rec(f"lot_pL_{l_}", round((1 - p) ** l_ * p, 6), f"P(L={l_}) = (1-p)^l p")
rec("lot_EL", round((1 - p) / p, 6), "E[L] = (1-p)/p = E[T1]-1")
rec("lot_varL", round((1 - p) / p ** 2, 6), "var(L) = var(T1)")
# Monte Carlo for L
g = rng.geometric(p, size=2_000_000)
rec("lot_mc_EL", round(float((g - 1).mean()), 4))

print()
print("=" * 74)
print("G. Pascal PMF / kth arrival time (L13 slide 6)")
print("=" * 74)
k = 3
rec("pas_k", k)
rec("pas_EY", round(k / p, 6), "E[Y_k] = k/p")
rec("pas_varY", round(k * (1 - p) / p ** 2, 6), "var(Y_k) = k(1-p)/p^2")
rec("pas_sdY", round(math.sqrt(k * (1 - p) / p ** 2), 4))


def pascal(t, k, p):
    return math.comb(t - 1, k - 1) * p ** k * (1 - p) ** (t - k)


for t in (3, 5, 8, 10):
    rec(f"pas_p_{t}", round(pascal(t, k, p), 6), f"P(Y_3={t}), p=0.3")
rec("pas_mode_t", int(max(range(k, 80), key=lambda t: pascal(t, k, p))),
    "most likely value of Y_3")
rec("pas_norm_check", round(sum(pascal(t, k, p) for t in range(k, 4000)), 10),
    "sum of Pascal PMF over t")
# decomposition check: P(Y_3 = 8) via A and B
pA = p
pB = math.comb(7, 2) * p ** 2 * (1 - p) ** 5
rec("pas_pA", pA, "P(trial 8 is a success)")
rec("pas_pB", round(pB, 6), "P(exactly 2 successes in first 7 trials)")
rec("pas_product", round(pA * pB, 6), "P(A)P(B) = P(Y_3=8)")

print()
print("=" * 74)
print("H. B&T Example 6.5 — Alicia fouls out")
print("=" * 74)
p_a = 0.05
tail = [pascal(z, 6, p_a) for z in range(6, 30)]
rec("alicia_p", p_a)
rec("alicia_EY6", round(6 / p_a, 4), "E[Y_6] = 6/p")
rec("alicia_pZ_6", round(pascal(6, 6, p_a), 10))
rec("alicia_pZ_20", round(pascal(20, 6, p_a), 8))
rec("alicia_pZ_29", round(pascal(29, 6, p_a), 8))
rec("alicia_sum_6_29", round(sum(tail), 6), "P(fouls out before minute 30)")
rec("alicia_pZ_30", round(1 - sum(tail), 6), "P(Z=30) = P(plays full 30 min)")
EZ = sum(z * pascal(z, 6, p_a) for z in range(6, 30)) + 30 * (1 - sum(tail))
rec("alicia_EZ", round(EZ, 4), "E[Z] = E[min(Y_6,30)]")

print()
print("=" * 74)
print("I. B&T Example 6.2 — busy/idle periods, and 6.3 fresh start at a random time")
print("=" * 74)
rec("cpu_p", p)
rec("cpu_EI", round(1 / p, 4), "mean idle period length = 1/p")
rec("cpu_EB", round(1 / (1 - p), 4), "mean busy period length = 1/(1-p)")
rec("cpu_varI", round((1 - p) / p ** 2, 4))
rec("cpu_varB", round(p / (1 - p) ** 2, 4))
rec("cpu_EZ_first_idle_end", round(1 + 1 / p, 4), "E[Z] = E[L]+E[I] with L=1")
rec("fresh_p2", round((1 - p) ** 2, 6), "P(X_{N+1}=X_{N+2}=0) = (1-p)^2")

print()
print("=" * 74)
print("J. Merging and splitting of Bernoulli processes (L13 slides 7-8)")
print("=" * 74)
q_split = 0.6
rec("split_q", q_split)
rec("split_p1", round(p * q_split, 6), "kept stream: pq")
rec("split_p2", round(p * (1 - q_split), 6), "discarded stream: p(1-q)")
rec("split_sum", round(p * q_split + p * (1 - q_split), 6), "= p")
p1_m, p2_m = 0.3, 0.2
rec("merge_p1", p1_m)
rec("merge_p2", p2_m)
rec("merge_p", round(p1_m + p2_m - p1_m * p2_m, 6), "p+q-pq")
rec("merge_none", round((1 - p1_m) * (1 - p2_m), 6), "P(no arrival in either)")
rec("merge_collision", round(p1_m * p2_m, 6), "P(collision) per slot")
rec("merge_pcoll_given_arr", round(p1_m * p2_m / (p1_m + p2_m - p1_m * p2_m), 6),
    "P(both | merged arrival)")

print()
print("=" * 74)
print("K. Widget cross-check: interarrival empirical vs geometric")
print("=" * 74)
for pw in (0.15, 0.3, 0.5):
    trials = rng.random(400_000) < pw
    idx = np.flatnonzero(trials)
    gaps = np.diff(np.concatenate(([-1], idx)))
    emp = np.array([(gaps == t).mean() for t in range(1, 16)])
    th = np.array([(1 - pw) ** (t - 1) * pw for t in range(1, 16)])
    rec(f"wid_p={pw}_maxdiff", round(float(np.abs(emp - th).max()), 5),
        "max |empirical - geometric| over t=1..15")
    rec(f"wid_p={pw}_meangap", round(float(gaps.mean()), 4), f"vs 1/p = {1/pw:.4f}")

print()
print("=" * 74)
print("L. Practice-question numbers")
print("=" * 74)
# P2.4: N ~ Poisson(lam=4), X_i Bernoulli(q=0.25)  -> Y Poisson(1)
lam_p, q_p = 4.0, 0.25
EY_p = lam_p * q_p
varY_p = lam_p * q_p * (1 - q_p) + q_p ** 2 * lam_p
rec("prac_pois_EY", EY_p)
rec("prac_pois_within", lam_p * q_p * (1 - q_p))
rec("prac_pois_between", q_p ** 2 * lam_p)
rec("prac_pois_varY", varY_p, "equals E[Y]: Y is Poisson(lam*q)")
# P: coupons - number of emails
EN_e, varN_e, EX_e, varX_e = 8.0, 8.0, 2.5, 6.25
rec("prac_em_EY", EN_e * EX_e)
rec("prac_em_varY", EN_e * varX_e + EX_e ** 2 * varN_e)
# P: Bernoulli p=0.2, P(2nd arrival at time 6)
rec("prac_pas_val", round(pascal(6, 2, 0.2), 6), "P(Y_2=6), p=0.2")
rec("prac_pas_EY2", round(2 / 0.2, 4))
rec("prac_pas_varY2", round(2 * 0.8 / 0.04, 4))
# P: P(S=2 in 6 trials AND 2nd success at 6) comparison
rec("prac_bin_S2_6", round(math.comb(6, 2) * 0.2 ** 2 * 0.8 ** 4, 6), "P(S_6=2)")
# P: merging practice
rec("prac_merge", round(0.4 + 0.25 - 0.4 * 0.25, 6))
rec("prac_split_keep", round(0.4 * 0.7, 6))
# P: memoryless practice, p=0.05 machine
rec("prac_mem_tail", round(0.95 ** 40, 6), "P(T>40), p=0.05")
rec("prac_mem_extra", round(1 / 0.05, 4), "expected additional trials")
rec("prac_mem_cond", round(40 + 1 / 0.05, 4), "E[T | T>40]")

print()
print("=" * 74)
print("M. More practice-question numbers")
print("=" * 74)
# Practice 2.6: disjoint-trial independence, p=0.3
pA26 = math.comb(3, 1) * 0.3 ** 1 * 0.7 ** 2
pB26 = math.comb(7, 2) * 0.3 ** 2 * 0.7 ** 5
rec("prac26_PA", round(pA26, 6), "P(exactly 1 success in trials 1-3)")
rec("prac26_PB", round(pB26, 6), "P(exactly 2 successes in trials 4-10)")
rec("prac26_joint", round(pA26 * pB26, 6), "P(A and B)")
# Practice 2.7 (c) ratio
rec("prac27_ratio", round(pascal(6, 2, 0.2) / (math.comb(6, 2) * 0.2 ** 2 * 0.8 ** 4), 6),
    "P(Y_2=6)/P(S_6=2) = 5/15")
# Example 2.10 rain
rec("rain_p2", round(p ** 2, 6), "P(day 5 and day 8 rainy) = p^2, p=0.3")
# Practice 2.9
m29 = 0.4 + 0.25 - 0.4 * 0.25
rec("prac29_merged", round(m29, 6))
rec("prac29_forward", round(m29 * 0.7, 6), "merged then split with 0.7")
rec("prac29_E100", round(100 * m29 * 0.7, 4), "expected forwarded alarms in 100 slots")
rec("prac29_var100", round(100 * m29 * 0.7 * (1 - m29 * 0.7), 6))
# Practice 2.10, n=1 counterexample
rec("prac210_pM1M1", 0.0, "P(M=1, M'=1) for n=1")
rec("prac210_product", round((0.3 / 2) ** 2, 6), "P(M=1)P(M'=1) for n=1, p=0.3")
# Gotcha counterexample for dependence (N = X_i = N)
rec("gotcha_EY_true", 2.5, "E[N^2] with N in {1,2} equally likely")
rec("gotcha_EY_formula", 2.25, "(E[N])^2 = 1.5^2, the WRONG value the formula would give")

out_path = ROOT / "computes" / "g4_s2.json"
out_path.write_text(json.dumps(OUT, indent=1, sort_keys=True), encoding="utf-8")
print()
print("wrote", out_path, f"({len(OUT)} keys)")
