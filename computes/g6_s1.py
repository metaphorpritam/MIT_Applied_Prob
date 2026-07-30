# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Numbers for G6 section 1 - Markov and Chebyshev inequalities, the sample
mean, the weak law of large numbers, convergence in probability.

Sources: L19 slides 1-7, rec20 problems 1-3, B&T sections 5.1-5.3.

Run:  uv run computes/g6_s1.py
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
OUT: dict[str, object] = {}


def rec(key, val, label=""):
    if isinstance(val, np.ndarray):
        val = val.tolist()
    if isinstance(val, (np.floating, np.integer)):
        val = val.item()
    if isinstance(val, dict):
        val = {k: (v.item() if isinstance(v, (np.floating, np.integer)) else v)
               for k, v in val.items()}
    OUT[key] = val
    print(f"{key:30s} = {val}   {label}")


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


# ===========================================================================
# A. Markov inequality - B&T Example 5.1, X ~ uniform[0,4]
# ===========================================================================
head("A. Markov inequality, X ~ U[0,4] (B&T Example 5.1)")

a_lo, a_hi = 0.0, 4.0
EX_unif = (a_lo + a_hi) / 2
rec("A_EX", EX_unif, "E[X] for U[0,4]")
for a in (2.0, 3.0, 4.0):
    bound = EX_unif / a
    exact = max(0.0, (a_hi - a) / (a_hi - a_lo))
    rec(f"A_markov_a{int(a)}", round(bound, 6), f"E[X]/a at a={a}")
    rec(f"A_exact_a{int(a)}", round(exact, 6), f"true P(X>={a})")
    rec(f"A_ratio_a{int(a)}", round(bound / exact, 6) if exact > 0 else "inf",
        "bound / truth")

# Markov applied to an exponential(1) tail
rec("A_exp_markov_c4", round(1.0 / 4.0, 6), "E[X]/a with E[X]=1, a=4")
rec("A_exp_exact_c4", round(math.exp(-4.0), 8), "true P(X>=4), Exp(1)")

# ===========================================================================
# B. Chebyshev inequality - B&T Example 5.2
# ===========================================================================
head("B. Chebyshev, U[0,4] and Exp(1) (B&T Example 5.2)")

var_unif = (a_hi - a_lo) ** 2 / 12
rec("B_var_unif", round(var_unif, 6), "sigma^2 = 16/12 = 4/3")
rec("B_cheb_c1", round(var_unif / 1.0 ** 2, 6), "Chebyshev bound on P(|X-2|>=1)")
rec("B_exact_c1", round(1 - 2.0 / 4.0, 6), "true P(|X-2|>=1) = 1/2")

# range bound  sigma^2 <= (b-a)^2/4    (B&T Example 5.3)
rec("B_rangebound_unif", round((a_hi - a_lo) ** 2 / 4, 6), "(b-a)^2/4 = 4")
rec("B_rangebound_ratio", round(((a_hi - a_lo) ** 2 / 4) / var_unif, 6),
    "range bound / true variance")

# exponential(1) tail via Chebyshev
exp_tbl = []
for c in (2, 3, 4, 5, 10):
    cheb = 1.0 / (c - 1) ** 2
    exact = math.exp(-c)
    exp_tbl.append({"c": c, "cheb": round(cheb, 8), "exact": round(exact, 8),
                    "ratio": round(cheb / exact, 3)})
    rec(f"B_exp_c{c}", exp_tbl[-1])
OUT["B_exp_table"] = exp_tbl

# ===========================================================================
# C. The k-sigma form:  P(|X-mu| >= k sigma) <= 1/k^2  vs the truth
# ===========================================================================
head("C. k-sigma form vs exact tails (widget verification)")


def tail_uniform(k):
    """X ~ U[m-h, m+h]; sigma = h/sqrt(3).  P(|X-mu| >= k sigma)."""
    return max(0.0, 1.0 - k / math.sqrt(3.0))


def tail_exponential(k):
    """X ~ Exp(1): mu = sigma = 1.  P(|X-1| >= k)."""
    upper = math.exp(-(1.0 + k))
    lower = 1.0 - math.exp(-(1.0 - k)) if k < 1.0 else 0.0
    return upper + lower


def tail_normal(k):
    return 2.0 * stats.norm.sf(k)


ks = [0.5, 1.0, 1.5, 1.732050808, 2.0, 2.5, 3.0, 4.0]
ctab = []
for k in ks:
    row = {"k": k,
           "bound": round(1.0 / k ** 2, 6),
           "uniform": round(tail_uniform(k), 6),
           "exponential": round(tail_exponential(k), 6),
           "normal": float(f"{tail_normal(k):.4g}")}
    ctab.append(row)
    rec(f"C_k{k}", row)
OUT["C_table"] = ctab
rec("C_sqrt3", round(math.sqrt(3.0), 6), "uniform tail is exactly 0 beyond k=sqrt(3)")
rec("C_gap_k2_normal", round((1 / 4) / tail_normal(2.0), 3),
    "Chebyshev bound / true normal tail at k=2")
rec("C_gap_k3_normal", round((1 / 9) / tail_normal(3.0), 3), "same at k=3")
rec("C_gap_k4_normal", round((1 / 16) / tail_normal(4.0), 3), "same at k=4")

# two-point distribution attaining Chebyshev with equality
rec("C_tight_k", 2.0, "equality case: P(X=+-k sigma)=1/(2k^2), P(X=0)=1-1/k^2")
rec("C_tight_p", round(1 / (2 * 2.0 ** 2), 6), "each atom mass at k=2")
rec("C_tight_check_var", round(2 * (1 / (2 * 4)) * 4, 6), "variance of that r.v. = 1")

# ===========================================================================
# D. The sample mean M_n: variance and concentration
# ===========================================================================
head("D. Sample mean of Bernoulli(0.5): exact vs Chebyshev")

p0, eps0 = 0.5, 0.1
dtab = []
for n in (1, 4, 16, 64, 100, 256, 1000):
    var_Mn = p0 * (1 - p0) / n
    cheb = min(1.0, var_Mn / eps0 ** 2)
    # exact P(|M_n - p| >= eps) for Bernoulli sums
    ks_ = np.arange(0, n + 1)
    pmf = stats.binom.pmf(ks_, n, p0)
    exact = float(pmf[np.abs(ks_ / n - p0) >= eps0 - 1e-12].sum())
    dtab.append({"n": n, "var": round(var_Mn, 8), "cheb": round(cheb, 6),
                 "exact": float(f"{exact:.4g}")})
    rec(f"D_n{n}", dtab[-1])
OUT["D_table"] = dtab
rec("D_sd_ratio_n4", round(math.sqrt(4), 4), "sd(M_n) shrinks like 1/sqrt(n)")

# ===========================================================================
# E. The pollster's problem - L19 slide 6, B&T Example 5.5
# ===========================================================================
head("E. Pollster (L19 slide 6, B&T Example 5.5)")

rec("E_maxvar", 0.25, "max_f f(1-f) at f=1/2")
rec("E_check_50000", round(1 / (4 * 50000 * 0.01 ** 2), 8),
    "1/(4 n eps^2) at n=50000, eps=0.01  -> must equal 0.05")
rec("E_n_required", math.ceil(1 / (4 * 0.05 * 0.01 ** 2)),
    "smallest n with 1/(4 n eps^2) <= 0.05")
rec("E_n100_eps01", round(1 / (4 * 100 * 0.1 ** 2), 6),
    "B&T: n=100, eps=0.1 gives bound 0.25")
# if f were known to be near 0.1
rec("E_var_f01", round(0.1 * 0.9, 6), "f(1-f) at f=0.1")
rec("E_n_required_f01", math.ceil(0.09 / (0.05 * 0.01 ** 2)),
    "n needed if f(1-f)=0.09 instead of 1/4")
# exact and normal-approximation sample sizes for comparison (forward ref to §2)
z975 = float(stats.norm.ppf(0.975))
rec("E_z975", round(z975, 6), "97.5th percentile of standard normal")
rec("E_n_clt", math.ceil((z975 / (2 * 0.01)) ** 2),
    "n from the CLT with f(1-f)<=1/4: (z/(2 eps))^2")
rec("E_ratio_cheb_clt", round(50000 / math.ceil((z975 / (2 * 0.01)) ** 2), 4),
    "Chebyshev n / CLT n")
# exact binomial tail at n = 50000, f = 0.5
n_p, f_p = 50000, 0.5
sd_p = math.sqrt(f_p * (1 - f_p) * n_p)
exact_poll = float(2 * stats.binom.cdf(math.floor(n_p * (f_p - 0.01)), n_p, f_p))
rec("E_exact_50000", round(exact_poll, 10),
    "true P(|M_n - f| >= 0.01) at n=50000, f=0.5")

# accuracy curve: bound as a function of n at eps = 0.01
for n in (1000, 5000, 10000, 25000, 50000, 100000):
    rec(f"E_bound_n{n}", round(min(1.0, 1 / (4 * n * 0.01 ** 2)), 6))

# ===========================================================================
# F. rec20 Problem 1 - lightbulbs
# ===========================================================================
head("F. rec20 P1 - lightbulb quality")

rec("F_b_bound", round((1 / 4) / (50 * 0.1 ** 2), 6),
    "(1/4)/(50*0.01) = 0.5, bound on P(|Z50-p|>=0.1)")
rec("F_b_conclusion", round(1 - (1 / 4) / (50 * 0.1 ** 2), 6),
    "so P(|Z50-p|<0.1) >= 0.5")
rec("F_c_n", float(Fraction(1, 4) / (Fraction(5, 100) * Fraction(1, 100))),
    "n from (1/4)/(n*0.01) = 0.05  [exact rational arithmetic]")
rec("F_c_n_var16", float(Fraction(1, 16) / (Fraction(5, 100) * Fraction(1, 100))),
    "n when sigma^2 = 1/16")
rec("F_c_bound_at_500", float(Fraction(1, 4) / (500 * Fraction(1, 100))),
    "bound at n=500 is exactly 0.05")
rec("F_c_bound_at_125", float(Fraction(1, 16) / (125 * Fraction(1, 100))),
    "bound at n=125 is exactly 0.05")
# exact numbers for a couple of true p values at n = 50 and n = 500
for (nn, pp) in ((50, 0.5), (50, 0.9), (500, 0.5), (500, 0.9)):
    ks_ = np.arange(0, nn + 1)
    pmf = stats.binom.pmf(ks_, nn, pp)
    exact = float(pmf[np.abs(ks_ / nn - pp) >= 0.1 - 1e-12].sum())
    rec(f"F_exact_n{nn}_p{int(pp*100)}", float(f"{exact:.4g}"),
        f"true P(|Z_{nn}-p|>=0.1) at p={pp}")

# ===========================================================================
# G. rec20 Problem 2 - two-point PMFs
# ===========================================================================
head("G. rec20 P2 - X_n and Y_n")

for n in (2, 4, 10, 100):
    EXn = Fraction(1, n)
    varXn = Fraction(n - 1, n ** 2)
    rec(f"G_EX_n{n}", f"{EXn} = {float(EXn):.6f}")
    rec(f"G_varX_n{n}", f"{varXn} = {float(varXn):.6f}")
    rec(f"G_varY_n{n}", n - 1, "var(Y_n) = n-1")
    rec(f"G_EY2_n{n}", n, "E[Y_n^2] = n")
# algebra check of var(X_n) = (n-1)/n^2
for n in (2, 5, 37):
    lhs = (0 - Fraction(1, n)) ** 2 * (1 - Fraction(1, n)) + \
          (1 - Fraction(1, n)) ** 2 * Fraction(1, n)
    rec(f"G_varX_check_n{n}", f"{lhs} == {Fraction(n-1, n**2)} -> {lhs == Fraction(n-1, n**2)}")
# algebra check of var(Y_n) = n-1
for n in (2, 5, 37):
    lhs = (0 - 1) ** 2 * (1 - Fraction(1, n)) + (n - 1) ** 2 * Fraction(1, n)
    rec(f"G_varY_check_n{n}", f"{lhs} == {n-1} -> {lhs == n - 1}")
# Chebyshev bound for Y_n is useless
rec("G_cheb_Y_n100_eps1", 100 - 1, "(n-1)/eps^2 at n=100, eps=1 -> 99, vacuous")
rec("G_true_Y_tail_n100", 0.01, "true P(|Y_100| >= eps) = 1/n = 0.01")

# ===========================================================================
# H. rec20 Problem 3 - i.i.d. uniform[-1,1] transforms
# ===========================================================================
head("H. rec20 P3 - X_i, X_i/i, (X_i)^i for U[-1,1]")

eps = 0.5
rec("H_var_unif11", round((1 - (-1)) ** 2 / 12, 8),
    "var(X) = (beta-alpha)^2/12 = 4/12 = 1/3 for X ~ uniform[-1,1]")
rec("H_Xi_tail", round(1 - eps, 6), "P(|X_i| > 0.5) = 1 - 0.5 = 0.5 for every i")
for i in (1, 2, 3, 10):
    rec(f"H_Yi_tail_i{i}", round(max(0.0, 1 - min(1.0, i * eps)), 6),
        f"P(|X_i/i| > 0.5) = max(0, 1 - i*0.5)")
rec("H_Yi_zero_from", math.ceil(1 / eps), "P(|Y_i|>0.5) is exactly 0 once i >= 2")
for i in (1, 2, 5, 20, 100, 1000):
    rec(f"H_Zi_tail_i{i}", round(1 - eps ** (1 / i), 8),
        f"P(|X_i^i| > 0.5) = 1 - 0.5^(1/i)")
rec("H_Zi_i100_check", round(1 - math.exp(math.log(0.5) / 100), 8))
rec("H_Zi_limit", 0.0, "limit as i -> infinity")

# B&T Example 5.6: min of n uniforms on [0,1]
for n in (1, 5, 20, 100):
    rec(f"H_min_tail_n{n}", round((1 - 0.1) ** n, 8),
        "P(min{X_1..X_n} >= 0.1) = 0.9^n")

# ===========================================================================
# I. Practice-question numbers
# ===========================================================================
head("I. Practice numbers")

# B&T Problem 5.1 - statistician's heights
rec("I_p1a_n", math.ceil(1.0 ** 2 / 0.01 ** 2), "sd(M_n)<=0.01 with sigma=1 -> n>=10^4")
rec("I_p1b_n", math.ceil(1.0 ** 2 / (0.05 ** 2 * 0.01)),
    "Chebyshev: sigma^2/(eps^2 delta) with eps=0.05, delta=0.01")
sig2_rev = (2.0 - 1.4) ** 2 / 4
sig2_rev_F = (Fraction(20, 10) - Fraction(14, 10)) ** 2 / 4   # exact rational
rec("I_p1c_sigma2", float(sig2_rev_F), "(b-a)^2/4 with a=1.4, b=2.0")
rec("I_p1c_a", math.ceil(sig2_rev_F / Fraction(1, 100) ** 2),
    "revised n for part (a)  [exact rational arithmetic]")
rec("I_p1c_b", math.ceil(sig2_rev_F / (Fraction(5, 100) ** 2 * Fraction(1, 100))),
    "revised n for part (b)  [exact rational arithmetic]")

# B&T Problem 5.4 - Alvin's smokers, n = f(1-f)/(eps^2 delta)
rec("I_p4_note", "n = f(1-f)/(eps^2 delta): halving f roughly halves n; halving delta doubles n")
for f in (0.4, 0.2, 0.1, 0.05):
    rec(f"I_p4_f{int(f*100)}", round(f * (1 - f), 6), "f(1-f)")
rec("I_p4_ratio_f04_02", round((0.2 * 0.8) / (0.4 * 0.6), 6), "n(f/2)/n(f) at f=0.4")

# Practice: Markov on a nonnegative r.v. with mean 3
rec("I_markov_mean3_a12", round(3 / 12, 6), "P(X>=12) <= 3/12")
# Practice: dice sample mean
mu_die = sum(range(1, 7)) / 6
var_die = sum((k - mu_die) ** 2 for k in range(1, 7)) / 6
rec("I_die_mu", round(mu_die, 6))
rec("I_die_var", round(var_die, 8), "35/12")
rec("I_die_n", math.ceil(var_die / (0.1 ** 2 * 0.05)),
    "n so Chebyshev gives P(|M_n-3.5|>=0.1)<=0.05")
ndie = math.ceil(var_die / (0.1 ** 2 * 0.05))
rec("I_die_bound_check", round(var_die / (ndie * 0.1 ** 2), 6))

# Practice: mean-square convergence rate for M_n
rec("I_ms_Mn", "E[(M_n-mu)^2] = sigma^2/n -> 0, so M_n -> mu in mean square too")

# Practice: two-sided vs one-sided Chebyshev on a light-bulb lifetime
rec("I_bulb_mu", 1000)
rec("I_bulb_sigma", 100)
rec("I_bulb_cheb", round(100 ** 2 / 250 ** 2, 6), "P(|X-1000|>=250) <= 0.16")
rec("I_bulb_markov", round(1000 / 1250, 6), "Markov: P(X>=1250) <= 0.8")

# ===========================================================================
# J. "Convergence in probability says nothing about a single sequence"
#    Independent Y_n with P(Y_n = 1) = 1/n, n = 2,3,...
# ===========================================================================
head("J. Independent flashing sequence: P(no 1 in n=2..N) = 1/N")

for N in (10, 100, 10 ** 4, 10 ** 6):
    prod = 1.0
    # prod_{n=2}^{N} (1 - 1/n) telescopes to 1/N
    tele = 1.0 / N
    rec(f"J_no1_upto_{N}", float(f"{tele:.6g}"),
        "prod_{n=2}^{N}(1-1/n) = 1/N  (telescoping)")
# direct check of the telescoping for a small N
N = 12
prod = 1.0
for n in range(2, N + 1):
    prod *= (1 - 1 / n)
rec("J_telescope_check_N12", f"{prod:.10f} vs 1/12 = {1/12:.10f}")
rec("J_tail_at_n", "P(|Y_n - 0| >= 1/2) = 1/n -> 0, so Y_n -> 0 in probability")
rec("J_ones_forever", "yet with probability 1 the realized sequence hits 1 infinitely often")

# ===========================================================================
# K. Chebyshev bound for rec20 P2's X_n at a few n (centered at 1/n)
# ===========================================================================
head("K. rec20 P2(b): Chebyshev bound (n-1)/(n^2 eps^2) for X_n")
for n in (10, 100, 1000):
    for e in (0.1, 0.5):
        rec(f"K_Xn_bound_n{n}_eps{e}", float(f"{(n-1)/(n**2 * e**2):.6g}"),
            "var(X_n)/eps^2")
rec("K_Xn_true_tail", "true P(X_n >= eps) = 1/n for 0 < eps <= 1 -- Chebyshev is off by ~1/(n eps^2)")

# ===========================================================================
# L. More practice numbers (B&T Problem 5.5(c),(d); Example 5.6 sample size)
# ===========================================================================
head("L. Extra practice numbers")

rec("L_min_n_for_001", math.ceil(math.log(0.01) / math.log(0.9)),
    "smallest n with 0.9^n <= 0.01  (min of n uniforms on [0,1])")
rec("L_min_check", round(0.9 ** math.ceil(math.log(0.01) / math.log(0.9)), 8),
    "0.9^n at that n")
rec("L_EabsX_unif11", 0.5, "E[|X|] for X ~ U[-1,1]")
for n in (1, 5, 10, 20):
    rec(f"L_prod_markov_n{n}", float(f"{0.5 ** n / 0.1:.6g}"),
        "Markov bound P(|X_1...X_n| >= 0.1) <= (1/2)^n / 0.1")
rec("L_prod_first_useful_n", math.ceil(math.log(0.1) / math.log(0.5)) + 0,
    "smallest n making (1/2)^n/0.1 <= 1")
for n in (1, 10, 50, 100):
    rec(f"L_max_tail_n{n}", float(f"{0.95 ** n:.6g}"),
        "P(|max{X_1..X_n} - 1| > 0.1) = 0.95^n for U[-1,1]")
rec("L_max_n_for_001", math.ceil(math.log(0.01) / math.log(0.95)),
    "smallest n with 0.95^n <= 0.01")

with open(ROOT / "computes" / "g6_s1.json", "w", encoding="utf-8") as fh:
    json.dump(OUT, fh, indent=1, default=str)
print("\nwrote computes/g6_s1.json  (%d keys)" % len(OUT))
