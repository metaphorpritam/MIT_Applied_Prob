# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Every number quoted in notes/src/fragments/g2_s3.html
(L06 slides 2-7, rec06 P3 = B&T Example 2.17, rec07 P3 = B&T Problem 2.33).

Run:  uv run computes/g2_s3.py
Writes computes/g2_s3.json.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict = {}


def show(key, val, note=""):
    R[key] = val
    print(f"{key:44s} = {val}   {note}")


def head(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


# ==========================================================================
head("A. E[X - E[X]] = 0  (L06 slide 2) -- numeric sanity check")
# ==========================================================================
# Take an arbitrary lopsided PMF and verify the centered mean is exactly 0.
xs_a = [-3, 0, 2, 7]
ps_a = [F(1, 8), F(3, 8), F(1, 4), F(1, 4)]
show("A_pmf_sums_to", str(sum(ps_a)))
EA = sum(F(x) * p for x, p in zip(xs_a, ps_a))
show("A_EX", str(EA), f"= {float(EA)}")
centered = sum((F(x) - EA) * p for x, p in zip(xs_a, ps_a))
show("A_E_centered", str(centered), "must be exactly 0")
assert centered == 0

# ==========================================================================
head("B. Random speed (L06 slides 3-4): V = 1 or 200, each w.p. 1/2, d = 200")
# ==========================================================================
d = 200
v_vals = [F(1), F(200)]
v_probs = [F(1, 2), F(1, 2)]

EV = sum(v * p for v, p in zip(v_vals, v_probs))
show("B_EV", str(EV), f"= {float(EV)} mph")
EV2 = sum(v * v * p for v, p in zip(v_vals, v_probs))
show("B_EV2", str(EV2), f"E[V^2] = {float(EV2)}")
varV = EV2 - EV ** 2
show("B_varV", str(varV), f"= {float(varV)}")
# cross-check with the definition sum (v - E[V])^2 p_V(v)
varV_def = sum((v - EV) ** 2 * p for v, p in zip(v_vals, v_probs))
show("B_varV_definition", str(varV_def), "definition form agrees")
assert varV == varV_def
sigV = float(varV) ** 0.5
show("B_sigmaV", sigV, "= 199/2 exactly (two-point PMF: sigma = half the gap)")
assert abs(sigV - 199 / 2) < 1e-12

t_vals = [F(d) / v for v in v_vals]
show("B_T_values", [str(t) for t in t_vals], "T = 200/V in hours")
ET = sum(t * p for t, p in zip(t_vals, v_probs))
show("B_ET", str(ET), f"= {float(ET)} hours")
ET2 = sum(t * t * p for t, p in zip(t_vals, v_probs))
show("B_ET2", str(ET2))
varT = ET2 - ET ** 2
show("B_varT", str(varT), f"= {float(varT)}")
show("B_sigmaT", float(varT) ** 0.5)

naive = F(d) / EV
show("B_d_over_EV", str(naive), f"= {float(naive):.6f} hours   (the WRONG answer)")
show("B_ratio_ET_over_naive", float(ET / naive),
     "E[T] is this many times bigger than 200/E[V]")
show("B_ET_times_EV", str(ET * EV), f"= {float(ET * EV)}   vs  E[TV] = 200")
show("B_ETV", str(sum(t * v * p for t, v, p in zip(t_vals, v_vals, v_probs))),
     "T*V = 200 identically, so E[TV] = 200")
# harmonic-mean reading: 1/E[T] is the effective average speed
show("B_effective_speed_d_over_ET", float(F(d) / ET), "mph  (harmonic mean of 1 and 200)")
harm = 2 / (1 / 1 + 1 / 200)
show("B_harmonic_mean_check", harm, "2/(1/1 + 1/200)")
assert abs(float(F(d) / ET) - harm) < 1e-12

# Jensen direction check: t(v) = 200/v is convex, so E[t(V)] >= t(E[V])
show("B_jensen_gap", float(ET - naive), "E[T] - 200/E[V] >= 0 (convexity)")

# ==========================================================================
head("C. Conditional PMF / expectation, uniform on {1,2,3,4}, A = {X >= 2} (L06 slide 5)")
# ==========================================================================
xs_c = [1, 2, 3, 4]
p_c = [F(1, 4)] * 4
EXc = sum(F(x) * p for x, p in zip(xs_c, p_c))
show("C_EX", str(EXc), f"= {float(EXc)}")
EX2c = sum(F(x) ** 2 * p for x, p in zip(xs_c, p_c))
show("C_EX2", str(EX2c), f"= {float(EX2c)}")
varc = EX2c - EXc ** 2
show("C_varX", str(varc), f"= {float(varc)}")
PA = sum(p for x, p in zip(xs_c, p_c) if x >= 2)
show("C_P_A", str(PA))
cond = {x: p / PA for x, p in zip(xs_c, p_c) if x >= 2}
show("C_cond_pmf", {k: str(v) for k, v in cond.items()})
show("C_cond_sums_to", str(sum(cond.values())))
EXA = sum(F(x) * pp for x, pp in cond.items())
show("C_E_X_given_A", str(EXA), f"= {float(EXA)}")
EX2A = sum(F(x) ** 2 * pp for x, pp in cond.items())
show("C_E_X2_given_A", str(EX2A))
varXA = EX2A - EXA ** 2
show("C_var_X_given_A", str(varXA), f"= {float(varXA)}")
# total expectation cross-check with the complementary event {X = 1}
PAc = 1 - PA
EXAc = F(1)
tot = PAc * EXAc + PA * EXA
show("C_total_expectation_check", str(tot), "must equal E[X] = 5/2")
assert tot == EXc

# ==========================================================================
head("D. Geometric PMF, memorylessness, mean, variance (L06 slides 6-7; rec06 P3)")
# ==========================================================================
def geo_pmf(p, k):
    return (1 - p) ** (k - 1) * p


for p in [F(1, 2), F(1, 5), F(3, 10)]:
    pf = float(p)
    # normalization of the PMF (numeric truncation)
    ks = np.arange(1, 20000)
    tot_num = float(np.sum((1 - pf) ** (ks - 1) * pf))
    EX_num = float(np.sum(ks * (1 - pf) ** (ks - 1) * pf))
    EX2_num = float(np.sum(ks ** 2 * (1 - pf) ** (ks - 1) * pf))
    var_num = EX2_num - EX_num ** 2
    show(f"D_p={p}_pmf_total_numeric", round(tot_num, 12))
    show(f"D_p={p}_EX_numeric", EX_num)
    show(f"D_p={p}_EX_closed_1_over_p", float(1 / p))
    show(f"D_p={p}_EX2_closed", float(1 / p + 2 * (1 - p) / p ** 2))
    show(f"D_p={p}_EX2_numeric", EX2_num)
    show(f"D_p={p}_var_numeric", var_num)
    show(f"D_p={p}_var_closed_(1-p)/p^2", float((1 - p) / p ** 2))
    show(f"D_p={p}_sigma", float((1 - p) / p ** 2) ** 0.5)
    assert abs(EX_num - float(1 / p)) < 1e-6
    assert abs(var_num - float((1 - p) / p ** 2)) < 1e-5

# Memorylessness, exact in fractions: P(X - k = n | X > k) == p_X(n)
head("D2. Memorylessness check  P(X-k = n | X > k) = p_X(n), exact rationals")
for p in [F(1, 3), F(1, 5)]:
    q = 1 - p
    for k in [2, 5]:
        Pgt = q ** k                       # P(X > k) = (1-p)^k
        bad = []
        for n in range(1, 12):
            joint = q ** (k + n - 1) * p   # P(X = k+n) (and X>k is implied)
            condp = joint / Pgt
            if condp != q ** (n - 1) * p:
                bad.append(n)
        show(f"D2_p={p}_k={k}_P(X>k)", str(Pgt))
        show(f"D2_p={p}_k={k}_mismatches", bad, "empty list = memoryless holds exactly")
        assert not bad

# Worked numbers used in the text for p = 1/5
p = F(1, 5)
show("D3_p", str(p))
show("D3_EX", str(1 / p))
show("D3_var", str((1 - p) / p ** 2), f"= {float((1 - p) / p ** 2)}")
show("D3_sigma", float((1 - p) / p ** 2) ** 0.5)
show("D3_pX(1)", str(geo_pmf(p, 1)))
show("D3_pX(2)", str(geo_pmf(p, 2)), f"= {float(geo_pmf(p,2)):.4f}")
show("D3_pX(3)", str(geo_pmf(p, 3)), f"= {float(geo_pmf(p,3)):.4f}")
show("D3_P(X>3)", str((1 - p) ** 3), f"= {float((1-p)**3):.4f}")
show("D3_E[X|X>3]", str(3 + 1 / p), "= 3 + 1/p by memorylessness")

# ==========================================================================
head("E. rec07 P3 = B&T Problem 2.33: toss until HH or TT. E[X] = (2+pq)/(1-pq)")
# ==========================================================================
def two_in_row_exact(p):
    """Exact E[X] from the closed form, plus a from-scratch linear solve."""
    q = 1 - p
    closed = (2 + p * q) / (1 - p * q)
    # solve a = E[X|H1], b = E[X|T1] from  a = 2p + q(1+b),  b = 2q + p(1+a)
    # -> a - q b = 2p + q ;  -p a + b = 2q + p
    A = np.array([[1.0, -float(q)], [-float(p), 1.0]])
    rhs = np.array([float(2 * p + q), float(2 * q + p)])
    a, b = np.linalg.solve(A, rhs)
    EX = float(p) * a + float(q) * b
    return closed, a, b, EX


def two_in_row_sim_pmf(p, nmax=200):
    """Exact PMF of X by enumeration of the alternating pattern.
    The game lasts >= n tosses iff the first n-1 tosses alternate.
    X = n (n>=2) means tosses 1..n-1 alternate and toss n repeats toss n-1."""
    q = 1 - p
    tot = 0.0
    EX = 0.0
    for n in range(2, nmax):
        # two alternating starting patterns of length n-1: starts H or starts T
        # pattern starting H of length m has ceil(m/2) H's and floor(m/2) T's
        m = n - 1
        pr = 0.0
        for start in ("H", "T"):
            nh = (m + 1) // 2 if start == "H" else m // 2
            nt = m - nh
            base = (float(p) ** nh) * (float(q) ** nt)
            # last toss of the alternating run is H if (m odd and start H) etc.
            last = start if m % 2 == 1 else ("T" if start == "H" else "H")
            pr += base * (float(p) if last == "H" else float(q))
        tot += pr
        EX += n * pr
    return tot, EX


for p in [F(1, 2), F(2, 5), F(1, 10)]:
    q = 1 - p
    closed, a, b, EXls = two_in_row_exact(p)
    tot, EXen = two_in_row_sim_pmf(float(p))
    show(f"E_p={p}_pq", str(p * q), f"= {float(p*q)}")
    show(f"E_p={p}_E[X|H1]_closed", str((2 + q ** 2) / (1 - p * q)), f"= {float((2+q**2)/(1-p*q)):.6f}")
    show(f"E_p={p}_E[X|H1]_linsolve", a)
    show(f"E_p={p}_E[X|T1]_closed", str((2 + p ** 2) / (1 - p * q)), f"= {float((2+p**2)/(1-p*q)):.6f}")
    show(f"E_p={p}_E[X|T1]_linsolve", b)
    show(f"E_p={p}_EX_closed", str(closed), f"= {float(closed):.6f}")
    show(f"E_p={p}_EX_enumeration", EXen)
    show(f"E_p={p}_pmf_total", round(tot, 12))
    assert abs(float(closed) - EXen) < 1e-8
    assert abs(float(closed) - EXls) < 1e-10

# range of E[X] over p
pp = np.linspace(1e-6, 1 - 1e-6, 200001)
vals = (2 + pp * (1 - pp)) / (1 - pp * (1 - pp))
show("E_min_EX_over_p", float(vals.min()), "-> 2 as p -> 0 or 1")
show("E_max_EX_over_p", float(vals.max()), "= 3 at p = 1/2")
show("E_argmax_p", float(pp[vals.argmax()]))

# ==========================================================================
head("F. Companion recursion: expected tosses until TWO HEADS IN A ROW")
# ==========================================================================
def hh_exact(p):
    q = 1 - p
    A = (1 + p) / p ** 2          # start state (no useful head yet)
    B = 1 + q * A                 # one head banked
    return A, B


def hh_enum(p, nmax=4000):
    """P(N = n): last two tosses HH, no HH before. Count via Fibonacci-style DP."""
    q = 1 - p
    # states: 0 = no trailing H, 1 = trailing H; absorbing when HH occurs
    s0, s1 = 1.0, 0.0
    EX, tot = 0.0, 0.0
    for n in range(1, nmax):
        done = s1 * p                      # from state1 a head ends it at toss n
        EX += n * done
        tot += done
        s0, s1 = (s0 + s1) * q, s0 * p
    return tot, EX


for p in [F(1, 2), F(1, 3), F(2, 3)]:
    A, B = hh_exact(p)
    tot, EXn = hh_enum(float(p))
    show(f"F_p={p}_E[N]_start_closed_(1+p)/p^2", str((1 + p) / p ** 2), f"= {float((1+p)/p**2):.6f}")
    show(f"F_p={p}_E[N]_enumeration", EXn)
    show(f"F_p={p}_E[from one head banked]", str(B), f"= {float(B):.6f}")
    show(f"F_p={p}_pmf_total", round(tot, 12))
    assert abs(float(A) - EXn) < 1e-6

# ==========================================================================
head("G. var(aX + b) = a^2 var(X) -- numeric verification on the die PMF")
# ==========================================================================
a_, b_ = F(-3), F(7)
Y_vals = [a_ * F(x) + b_ for x in xs_c]
EY = sum(y * p for y, p in zip(Y_vals, p_c))
EY2 = sum(y * y * p for y, p in zip(Y_vals, p_c))
varY = EY2 - EY ** 2
show("G_a", str(a_))
show("G_b", str(b_))
show("G_EY", str(EY), f"= a*E[X]+b = {float(a_*EXc+b_)}")
show("G_varY", str(varY), f"= {float(varY)}")
show("G_a2_varX", str(a_ ** 2 * varc), "must match G_varY")
assert varY == a_ ** 2 * varc

# ==========================================================================
head("H. Widget check: renormalized conditional PMF of X-k given X>k")
# ==========================================================================
for p in [0.15, 0.35, 0.6]:
    for k in [1, 4, 9]:
        Pgt = (1 - p) ** k
        ns = np.arange(1, 41)
        cond = ((1 - p) ** (k + ns - 1) * p) / Pgt
        orig = (1 - p) ** (ns - 1) * p
        err = float(np.max(np.abs(cond - orig)))
        show(f"H_p={p}_k={k}_max_abs_diff", err, "conditional == original PMF")
        assert err < 1e-15
    show(f"H_p={p}_E[X|X>k]-k", 1 / p, "always 1/p, independent of k")

# ==========================================================================
head("I. Practice-question answers")
# ==========================================================================
# I1: X uniform on {0,1,2,3,4,5}; var(X)?
xs = list(range(6))
ps = [F(1, 6)] * 6
E1 = sum(F(x) * q for x, q in zip(xs, ps))
E1sq = sum(F(x) ** 2 * q for x, q in zip(xs, ps))
show("I1_EX", str(E1), f"= {float(E1)}")
show("I1_EX2", str(E1sq), f"= {float(E1sq)}")
show("I1_var", str(E1sq - E1 ** 2), f"= {float(E1sq - E1**2):.6f}")
show("I1_var_formula_(n^2-1)/12", str(F(6 ** 2 - 1, 12)))
show("I1_sigma", float(E1sq - E1 ** 2) ** 0.5)

# I2: 120-mile trip, V = 30 or 60 w.p. 1/2
dd = 120
vv = [F(30), F(60)]
EV2t = sum(v * F(1, 2) for v in vv)
Tt = [F(dd) / v for v in vv]
ETt = sum(t * F(1, 2) for t in Tt)
show("I2_EV", str(EV2t), f"= {float(EV2t)} mph")
show("I2_naive_time", str(F(dd) / EV2t), f"= {float(F(dd)/EV2t):.6f} h")
show("I2_T_values", [str(t) for t in Tt])
show("I2_ET", str(ETt), f"= {float(ETt)} h")
show("I2_effective_speed", str(F(dd) / ETt), f"= {float(F(dd)/ETt)} mph")

# I3: geometric p = 1/4 -> E[X], var, P(X > 6), E[X | X > 6]
p3 = F(1, 4)
show("I3_EX", str(1 / p3))
show("I3_var", str((1 - p3) / p3 ** 2), f"= {float((1-p3)/p3**2)}")
show("I3_P(X>6)", str((1 - p3) ** 6), f"= {float((1-p3)**6):.6f}")
show("I3_E[X|X>6]", str(6 + 1 / p3))
show("I3_var[X|X>6]", str((1 - p3) / p3 ** 2), "shift does not change variance")

# I4: conditional on A = {X even} for geometric p
# P(X even) = sum_{j>=1} q^{2j-1} p = pq/(1-q^2) = q/(1+q)
for pv in [F(1, 2), F(1, 4)]:
    qv = 1 - pv
    Peven = qv / (1 + qv)
    show(f"I4_p={pv}_P(X_even)", str(Peven), f"= {float(Peven):.6f}")
    ks = np.arange(1, 200000)
    num = float(np.sum(np.where(ks % 2 == 0, 1.0, 0.0) * (1 - float(pv)) ** (ks - 1) * float(pv)))
    show(f"I4_p={pv}_P(X_even)_numeric", num)
    assert abs(num - float(Peven)) < 1e-9

# I5: three-point PMF for var(aX+b) practice
xs5 = [-2, 1, 4]
ps5 = [F(1, 4), F(1, 2), F(1, 4)]
E5 = sum(F(x) * q for x, q in zip(xs5, ps5))
E5s = sum(F(x) ** 2 * q for x, q in zip(xs5, ps5))
v5 = E5s - E5 ** 2
show("I5_EX", str(E5), f"= {float(E5)}")
show("I5_EX2", str(E5s))
show("I5_var", str(v5), f"= {float(v5)}")
show("I5_E[5-2X]", str(5 - 2 * E5))
show("I5_var(5-2X)", str(4 * v5), f"= {float(4*v5)}")
show("I5_sigma(5-2X)", float(4 * v5) ** 0.5)

# I6: total expectation with a mixed population
# 60% of emails 'short' with mean 2 KB, 40% 'long' with mean 30 KB
show("I6_EX", str(F(6, 10) * 2 + F(4, 10) * 30), f"= {float(F(6,10)*2 + F(4,10)*30)} KB")

# I7: two-in-a-row with p = 1/3
p7 = F(1, 3)
q7 = 1 - p7
show("I7_pq", str(p7 * q7))
show("I7_E[X|H1]", str((2 + q7 ** 2) / (1 - p7 * q7)), f"= {float((2+q7**2)/(1-p7*q7)):.6f}")
show("I7_E[X|T1]", str((2 + p7 ** 2) / (1 - p7 * q7)), f"= {float((2+p7**2)/(1-p7*q7)):.6f}")
show("I7_EX", str((2 + p7 * q7) / (1 - p7 * q7)), f"= {float((2+p7*q7)/(1-p7*q7)):.6f}")
c7, a7, b7, e7 = two_in_row_exact(p7)
assert abs(float(c7) - two_in_row_sim_pmf(float(p7))[1]) < 1e-8

# I8: three heads in a row, fair coin
# E = (1 + p + p^2)/p^3  ... verify by DP
def kk_in_row(p, k, nmax=20000):
    q = 1 - p
    st = [0.0] * k
    st[0] = 1.0
    EX = 0.0
    tot = 0.0
    for n in range(1, nmax):
        done = st[k - 1] * p
        EX += n * done
        tot += done
        new = [0.0] * k
        new[0] = sum(st) * q
        for i in range(1, k):
            new[i] = st[i - 1] * p
        st = new
    return tot, EX


for k in [2, 3]:
    for pv in [0.5, 1 / 3]:
        tot, EXk = kk_in_row(pv, k)
        closed = sum(pv ** i for i in range(k)) / pv ** k
        show(f"I8_k={k}_p={pv:.4f}_E[N]_closed", closed)
        show(f"I8_k={k}_p={pv:.4f}_E[N]_dp", EXk)
        assert abs(closed - EXk) < 1e-6
show("I8_three_heads_fair_coin", 14.0, "(1+1/2+1/4)/(1/8) = 14")

# I9: Practice 3.1 -- lopsided three-point PMF, centered mean and MAD
xs9 = [F(1), F(4), F(9)]
ps9 = [F(2, 10), F(5, 10), F(3, 10)]
E9 = sum(x * q for x, q in zip(xs9, ps9))
show("I9_EX", str(E9), f"= {float(E9)}")
show("I9_E_centered", str(sum((x - E9) * q for x, q in zip(xs9, ps9))), "must be 0")
show("I9_MAD", str(sum(abs(x - E9) * q for x, q in zip(xs9, ps9))),
     f"= {float(sum(abs(x-E9)*q for x, q in zip(xs9, ps9)))}")

# I10: Practice 3.2 tail -- var(10 - 4X) for X uniform on {0..5}
show("I10_var(10-4X)", str(16 * (E1sq - E1 ** 2)), f"= {float(16*(E1sq-E1**2)):.6f}")

# I11: Practice 3.5 -- X = # heads in two fair tosses
xs11, ps11 = [0, 1, 2], [F(1, 4), F(1, 2), F(1, 4)]
E11 = sum(F(x) * q for x, q in zip(xs11, ps11))
E11s = sum(F(x) ** 2 * q for x, q in zip(xs11, ps11))
show("I11_EX", str(E11))
show("I11_EX2", str(E11s), f"= {float(E11s)}")
show("I11_var", str(E11s - E11 ** 2), f"= {float(E11s - E11**2)}")

# I12: Practice 3.6 -- fair die conditioned on even
xs12, ps12 = list(range(1, 7)), [F(1, 6)] * 6
PA12 = F(1, 2)
cond12 = {x: F(1, 3) for x in (2, 4, 6)}
E12 = sum(F(x) * q for x, q in cond12.items())
E12s = sum(F(x) ** 2 * q for x, q in cond12.items())
show("I12_E[X|even]", str(E12))
show("I12_E[X^2|even]", str(E12s))
show("I12_var[X|even]", str(E12s - E12 ** 2), f"= {float(E12s - E12**2):.6f}")
Ed = sum(F(x) * q for x, q in zip(xs12, ps12))
Eds = sum(F(x) ** 2 * q for x, q in zip(xs12, ps12))
show("I12_EX_uncond", str(Ed), f"= {float(Ed)}")
show("I12_var_uncond", str(Eds - Ed ** 2), f"= {float(Eds - Ed**2):.6f}")

# I13: Practice 3.7 -- three-point PMF conditioned on X >= 1
xs13 = [F(0), F(1), F(5)]
ps13 = [F(1, 2), F(3, 10), F(2, 10)]
PA13 = ps13[1] + ps13[2]
E13A = (xs13[1] * ps13[1] + xs13[2] * ps13[2]) / PA13
show("I13_P(A)", str(PA13))
show("I13_p(1|A)", str(ps13[1] / PA13))
show("I13_p(5|A)", str(ps13[2] / PA13))
show("I13_E[X|A]", str(E13A), f"= {float(E13A)}")
E13 = sum(x * q for x, q in zip(xs13, ps13))
show("I13_EX", str(E13), f"= {float(E13)}")
show("I13_TE_check", str(F(1, 2) * 0 + PA13 * E13A), "must equal I13_EX")
assert F(1, 2) * 0 + PA13 * E13A == E13

# I14: Practice 3.8 -- component with p = 0.02
show("I14_P(X>30)", 0.98 ** 30)
show("I14_E_remaining", 1 / 0.02)
show("I14_E[X|X>30]", 30 + 1 / 0.02)

# I15: Practice 3.10 -- file sizes
E15 = 0.6 * 2 + 0.4 * 30
E15s = 0.6 * 4 + 0.4 * ((400 + 1600) / 2)
show("I15_EX", E15)
show("I15_E[X^2|long]", (400 + 1600) / 2)
show("I15_EX2", E15s)
show("I15_var", E15s - E15 ** 2)
show("I15_sigma", (E15s - E15 ** 2) ** 0.5)

# I16: Example 3.4 -- book Example 2.16 transit times
show("I16_EX_transit", 0.5 * 0.05 + 0.3 * 0.1 + 0.2 * 0.3, "seconds")

# I17: Practice 3.13 -- inspector, p = 0.05
show("I17_EX", 1 / 0.05)
show("I17_var", 0.95 / 0.05 ** 2)
show("I17_sigma", (0.95 / 0.05 ** 2) ** 0.5)
show("I17_cov", (1 - 0.05) ** 0.5, "sigma/mean = sqrt(1-p)")

# I18: coefficient-of-variation example in the interpretation box (p = 0.01)
show("I18_EX", 1 / 0.01)
show("I18_sigma", (0.99 ** 0.5) / 0.01)

# I19: Fig 3.5(b) weighted average
show("I19_weighted_mean", 0.5 * 2 + 0.3 * 5 + 0.2 * 9)

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(R, indent=1, default=str), encoding="utf-8")
print(f"\nwrote {out}")
