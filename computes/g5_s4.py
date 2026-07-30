# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Numbers for G5 section 4 - absorption probabilities and expected time to absorption.

Sources: L18 slides 5-7, rec19 Problem 1 (a)-(h), B&T 7.4 (Examples 7.11 gambler's ruin,
7.12 spider-and-fly, 7.13 up-to-date/behind mean first passage & recurrence times).

Every displayed number in notes/src/fragments/g5_s4.html is produced here.
Exact rational arithmetic (fractions.Fraction) is the primary computation; every
linear system is ALSO solved independently with numpy.linalg.solve, and the two
are cross-checked.  Monte-Carlo simulation independently checks the headline
absorption probabilities / expected times.

Run:  uv run computes/g5_s4.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "computes" / "g5_s4.json"
R: dict[str, object] = {}


def rec(key, val, note=""):
    """Record + print one result."""
    if isinstance(val, F):
        R[key] = [val.numerator, val.denominator]
        print(f"{key:32s} = {val.numerator}/{val.denominator} = {float(val):.6f}   {note}")
    elif isinstance(val, float):
        R[key] = val
        print(f"{key:32s} = {val:.6f}   {note}")
    else:
        R[key] = val
        print(f"{key:32s} = {val}   {note}")


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def frac_solve(A, b):
    """Exact Gauss-Jordan on Fractions.  A: list of rows, b: list."""
    n = len(b)
    M = [list(map(F, A[i])) + [F(b[i])] for i in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b_ for a, b_ in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]


def np_check(A, b, exact, tag):
    x = np.linalg.solve(np.array(A, float), np.array(b, float))
    e = np.array([float(v) for v in exact])
    dev = float(np.max(np.abs(x - e)))
    print(f"    [numpy cross-check {tag}] max|exact - numpy| = {dev:.2e}")
    assert dev < 1e-9, tag
    return dev


def absorb_sim(P, states, start, absorbing, rng, n=400_000, target=None):
    """Monte-Carlo: returns (P(hit target), E[steps to absorption])."""
    idx = {s: k for k, s in enumerate(states)}
    Pm = np.array([[float(P.get((i, j), 0)) for j in states] for i in states])
    cum = np.cumsum(Pm, axis=1)
    cur = np.full(n, idx[start])
    steps = np.zeros(n)
    alive = np.ones(n, bool)
    absidx = {idx[s] for s in absorbing}
    for _ in range(4000):
        if not alive.any():
            break
        u = rng.random(alive.sum())
        nxt = (u[:, None] > cum[cur[alive]]).sum(axis=1)
        cur[alive] = nxt
        steps[alive] += 1
        alive = np.array([c not in absidx for c in cur]) & alive
    hit = float(np.mean(cur == idx[target])) if target is not None else None
    return hit, float(steps.mean())


rng = np.random.default_rng(60412018)

# =====================================================================
head("A.  L18 slide 5 - absorption probabilities on the five-state chain")
# states 1,2,3 transient; 4 and 5 absorbing.  a_i = P(absorbed at 4 | X_0 = i)
# p13 = 0.3, p12 = 0.5, p14 = 0.2 ; p21 = 0.4, p23 = 0.6 ; p32 = 0.8, p35 = 0.2
# a1 = 0.2 + 0.5 a2 + 0.3 a3
# a2 = 0.4 a1 + 0.6 a3
# a3 = 0.8 a2
A = [[1, F(-1, 2), F(-3, 10)],
     [F(-2, 5), 1, F(-3, 5)],
     [0, F(-4, 5), 1]]
b = [F(1, 5), 0, 0]
a1, a2, a3 = frac_solve(A, b)
rec("L18_a1", a1, "a_1 = 13/28")
rec("L18_a2", a2, "a_2 = 5/14")
rec("L18_a3", a3, "a_3 = 2/7")
np_check(A, b, [a1, a2, a3], "L18 absorption")
# intermediate algebra values quoted in the prose
rec("L18_a2_over_a1", F(10, 13), "a_2 = (10/13) a_1  [from 0.52 a_2 = 0.4 a_1]")
rec("L18_a3_over_a1", F(8, 13), "a_3 = (8/13) a_1")
rec("L18_coeff_74_13", F(74, 130), "0.5*(10/13) + 0.3*(8/13) = 7.4/13")
rec("L18_resid_56_130", F(56, 130), "1 - 7.4/13 = 5.6/13")
P5 = {(1, 2): F(1, 2), (1, 3): F(3, 10), (1, 4): F(1, 5),
      (2, 1): F(2, 5), (2, 3): F(3, 5),
      (3, 2): F(4, 5), (3, 5): F(1, 5),
      (4, 4): F(1), (5, 5): F(1)}
h, _ = absorb_sim(P5, [1, 2, 3, 4, 5], 1, {4, 5}, rng, target=4)
rec("L18_a1_mc", h, "Monte-Carlo (400k runs) estimate of a_1")

# =====================================================================
head("B.  L18 slide 6 - expected time to absorption on the four-state chain")
# same chain with state 4 deleted and p_{1,3} = 0.5 (0.3 + 0.2 rerouted);
# 5 is the unique absorbing state.  mu_i = 1 + sum_j p_ij mu_j
# mu1 = 1 + 0.5 mu2 + 0.5 mu3
# mu2 = 1 + 0.4 mu1 + 0.6 mu3
# mu3 = 1 + 0.8 mu2
A = [[1, F(-1, 2), F(-1, 2)],
     [F(-2, 5), 1, F(-3, 5)],
     [0, F(-4, 5), 1]]
b = [F(1), F(1), F(1)]
m1, m2, m3 = frac_solve(A, b)
rec("L18_mu1", m1, "mu_1 = 111/8 = 13.875")
rec("L18_mu2", m2, "mu_2 = 55/4 = 13.75")
rec("L18_mu3", m3, "mu_3 = 12")
np_check(A, b, [m1, m2, m3], "L18 absorption time")
rec("L18_mu2_expr_num", F(8, 5), "1.6 in  0.52 mu_2 = 1.6 + 0.4 mu_1")
rec("L18_mu1_step_222", F(222, 100), "0.16 mu_1 = 2.22")
P4 = {(1, 2): F(1, 2), (1, 3): F(1, 2),
      (2, 1): F(2, 5), (2, 3): F(3, 5),
      (3, 2): F(4, 5), (3, 5): F(1, 5), (5, 5): F(1)}
_, ms = absorb_sim(P4, [1, 2, 3, 5], 1, {5}, rng, target=5)
rec("L18_mu1_mc", ms, "Monte-Carlo estimate of mu_1")

# =====================================================================
head("C.  B&T Example 7.12 - spider and fly, m = 4")
# states 1..4 = distance/position of fly; 1 and 4 absorbing (spiders).
# p_{i,i-1} = p_{i,i+1} = 0.3, p_ii = 0.4 for i = 2,3
A = [[F(3, 5), F(-3, 10)], [F(-3, 10), F(3, 5)]]
b = [F(1), F(1)]
sf2, sf3 = frac_solve(A, b)
rec("spider_mu2", sf2, "mu_2 = 10/3")
rec("spider_mu3", sf3, "mu_3 = 10/3")
np_check(A, b, [sf2, sf3], "spider-fly times")
# absorption at state 4 (right-hand spider)
A = [[F(3, 5), F(-3, 10)], [F(-3, 10), F(3, 5)]]
b = [F(0), F(3, 10)]
sa2, sa3 = frac_solve(A, b)
rec("spider_a2", sa2, "P(absorbed at 4 | start 2) = 1/3")
rec("spider_a3", sa3, "P(absorbed at 4 | start 3) = 2/3")
np_check(A, b, [sa2, sa3], "spider-fly absorption")
Psf = {(1, 1): F(1), (4, 4): F(1),
       (2, 1): F(3, 10), (2, 2): F(2, 5), (2, 3): F(3, 10),
       (3, 2): F(3, 10), (3, 3): F(2, 5), (3, 4): F(3, 10)}
h, ms = absorb_sim(Psf, [1, 2, 3, 4], 2, {1, 4}, rng, target=4)
rec("spider_a2_mc", h, "Monte-Carlo a_2")
rec("spider_mu2_mc", ms, "Monte-Carlo mu_2")

# =====================================================================
head("D.  B&T Example 7.11 - gambler's ruin: closed forms vs linear solve")


def ruin_exact(p, m):
    """a_i = P(reach m before 0 | X_0 = i) for i = 0..m, exact Fractions."""
    p = F(p)
    if p == F(1, 2):
        return [F(i, m) for i in range(m + 1)]
    rho = (1 - p) / p
    den = 1 - rho ** m
    return [(1 - rho ** i) / den for i in range(m + 1)]


def ruin_duration_exact(p, m):
    """D_i = E[number of rounds until 0 or m], i = 0..m."""
    p = F(p)
    a = ruin_exact(p, m)
    if p == F(1, 2):
        return [F(i * (m - i)) for i in range(m + 1)]
    return [(F(i) - m * a[i]) / (1 - 2 * p) for i in range(m + 1)]


def ruin_linear(p, m):
    """Solve a_i = (1-p) a_{i-1} + p a_{i+1} and D_i = 1 + ... numerically."""
    n = m - 1
    A = np.zeros((n, n))
    ba = np.zeros(n)
    bd = np.ones(n)
    for k in range(n):
        i = k + 1
        A[k, k] = 1.0
        if i - 1 >= 1:
            A[k, k - 1] = -(1 - p)
        if i + 1 <= m - 1:
            A[k, k + 1] = -p
        if i + 1 == m:
            ba[k] += p            # a_m = 1 contributes p*1
    return np.linalg.solve(A, ba), np.linalg.solve(A, bd)


for (pp, mm) in [(F(1, 2), 10), (F(2, 5), 10), (F(3, 5), 10), (F(9, 20), 20)]:
    ax = ruin_exact(pp, mm)
    dx = ruin_duration_exact(pp, mm)
    an, dn = ruin_linear(float(pp), mm)
    da = float(np.max(np.abs(an - np.array([float(v) for v in ax[1:mm]]))))
    dd = float(np.max(np.abs(dn - np.array([float(v) for v in dx[1:mm]]))))
    tag = f"p={pp}, m={mm}"
    print(f"  {tag:16s}  max|closed form - linear solve|:  a {da:.2e}   D {dd:.2e}")
    assert da < 1e-9 and dd < 1e-9

rec("ruin_p50_m10_i5_a", ruin_exact(F(1, 2), 10)[5], "fair game, a_5 = 1/2")
rec("ruin_p50_m10_i5_D", ruin_duration_exact(F(1, 2), 10)[5], "fair game, D_5 = 25")
rec("ruin_p45_m10_i5_a", float(ruin_exact(F(9, 20), 10)[5]), "p=0.45, m=10, a_5")
rec("ruin_p45_m10_i5_D", float(ruin_duration_exact(F(9, 20), 10)[5]), "p=0.45, m=10, D_5")
rec("ruin_p45_m100_i50_a", float(ruin_exact(F(9, 20), 100)[50]), "p=0.45, m=100, a_50")
rec("ruin_p45_m100_i50_D", float(ruin_duration_exact(F(9, 20), 100)[50]), "p=0.45, m=100, D_50")
# the m -> infinity limit of a_i for p < 1/2 is 0; for p > 1/2 it is 1 - rho^i
rec("ruin_rho_p45", F(11, 9), "rho = (1-p)/p = 0.55/0.45 = 11/9 at p = 0.45")
rec("ruin_rho_p55", F(9, 11), "rho = (1-p)/p = 0.45/0.55 = 9/11 at p = 0.55")
rec("ruin_p55_inf_i10", float(1 - (F(9, 20) / F(11, 20)) ** 10),
    "p=0.55: lim_{m->inf} a_10 = 1 - rho^10 with rho = 9/11")
# small illustrative table for the widget note
for pv in [0.40, 0.45, 0.50, 0.55]:
    axx = ruin_exact(F(pv).limit_denominator(100), 20)
    print(f"    p={pv:.2f}, m=20 : a_10 = {float(axx[10]):.6f}")
rec("ruin_tab_p40_m20_i10", float(ruin_exact(F(2, 5), 20)[10]))
rec("ruin_tab_p45_m20_i10", float(ruin_exact(F(9, 20), 20)[10]))
rec("ruin_tab_p50_m20_i10", float(ruin_exact(F(1, 2), 20)[10]))
rec("ruin_tab_p55_m20_i10", float(ruin_exact(F(11, 20), 20)[10]))
rec("ruin_tab_p45_m20_i10_D", float(ruin_duration_exact(F(9, 20), 20)[10]))
rec("ruin_tab_p50_m20_i10_D", float(ruin_duration_exact(F(1, 2), 20)[10]))
# Monte-Carlo check of one gambler's ruin cell
p_, m_, i_ = 0.45, 20, 10
NS = 200_000
pos = np.full(NS, i_)
dur = np.zeros(NS)
live = np.ones(NS, bool)
for _ in range(20000):
    if not live.any():
        break
    step = np.where(rng.random(live.sum()) < p_, 1, -1)
    pos[live] += step
    dur[live] += 1
    live = live & (pos > 0) & (pos < m_)
rec("ruin_mc_p45_m20_i10_a", float(np.mean(pos == m_)), "Monte-Carlo a_10")
rec("ruin_mc_p45_m20_i10_D", float(dur.mean()), "Monte-Carlo D_10")

# =====================================================================
head("E.  L18 slide 7 / B&T Example 7.13 - mean first passage and recurrence")
# up-to-date (1) / behind (2):  p11=0.8, p12=0.2, p21=0.6, p22=0.4
t2 = F(1) / F(6, 10)          # t_2 = 1 + 0.4 t_2  =>  0.6 t_2 = 1
rec("bt713_t2", t2, "t_2 = 5/3")
t1s = 1 + F(8, 10) * 0 + F(2, 10) * t2
rec("bt713_t1star", t1s, "t_1^* = 1 + 0.2*(5/3) = 4/3")
rec("bt713_pi1", 1 / t1s, "pi_1 = 1/t_1^* = 3/4")
rec("bt713_pi2", 1 - 1 / t1s, "pi_2 = 1/4")
# steady state cross-check by matrix power
Pm = np.array([[0.8, 0.2], [0.6, 0.4]])
rec("bt713_pi_matrixpower", float(np.linalg.matrix_power(Pm, 60)[0, 0]),
    "(P^60)_{11} -> pi_1")

# =====================================================================
head("F.  rec19 P1 - Josephina.  States 1 = 6-1, 2 = 6-2, 3 = 6-3, plus 9 and 15")
# p_1: 1/2 stay, 1/8 each to 6-2, 6-3, 9, 15
# p_2 (6-2): 1/2 -> 15, 3/8 -> 6-1, 1/8 -> 6-3
# p_3 (6-3): 1/4 -> 9,  3/8 -> 6-1, 3/8 -> 6-2
rows = {
    1: {1: F(1, 2), 2: F(1, 8), 3: F(1, 8), 9: F(1, 8), 15: F(1, 8)},
    2: {15: F(1, 2), 1: F(3, 8), 3: F(1, 8)},
    3: {9: F(1, 4), 1: F(3, 8), 2: F(3, 8)},
}
for k, r in rows.items():
    assert sum(r.values()) == 1, k
print("  all three transient rows sum to 1  [checked]")

print("\n-- (b) absorption probabilities into course 15 --")
# a_i = sum_j p_ij a_j, a_15 = 1, a_9 = 0
A = [[F(1, 2), F(-1, 8), F(-1, 8)],
     [F(-3, 8), F(1), F(-1, 8)],
     [F(-3, 8), F(-3, 8), F(1)]]
b = [F(1, 8), F(1, 2), F(0)]
ra1, ra2, ra3 = frac_solve(A, b)
rec("rec19_a1", ra1, "a_{6-1} = 105/184")
rec("rec19_a2", ra2, "a_{6-2} = 8723/11224")
rec("rec19_a3", ra3, "a_{6-3} = 5673/11224")
np_check(A, b, [ra1, ra2, ra3], "rec19 (b)")
rec("rec19_a1_f", float(ra1))
rec("rec19_a2_f", float(ra2))
rec("rec19_a3_f", float(ra3))
# intermediate elimination constants quoted in the prose
rec("rec19_b_a2_of_a1_num", 32, "61 a_2 = 32 + 27 a_1")
rec("rec19_b_a3_of_a1_num", 12, "61 a_3 = 12 + 33 a_1")
Pj = {(1, 1): F(1, 2), (1, 2): F(1, 8), (1, 3): F(1, 8), (1, 4): F(1, 8), (1, 5): F(1, 8),
      (2, 5): F(1, 2), (2, 1): F(3, 8), (2, 3): F(1, 8),
      (3, 4): F(1, 4), (3, 1): F(3, 8), (3, 2): F(3, 8),
      (4, 4): F(1), (5, 5): F(1)}   # 4 = course 9, 5 = course 15
h, ms = absorb_sim(Pj, [1, 2, 3, 4, 5], 1, {4, 5}, rng, target=5)
rec("rec19_a1_mc", h, "Monte-Carlo a_{6-1}")

print("\n-- (c) expected time until she leaves course 6 --")
A = [[F(1, 2), F(-1, 8), F(-1, 8)],
     [F(-3, 8), F(1), F(-1, 8)],
     [F(-3, 8), F(-3, 8), F(1)]]
b = [F(1), F(1), F(1)]
rm1, rm2, rm3 = frac_solve(A, b)
rec("rec19_mu1", rm1, "mu_{6-1} = 81/23")
rec("rec19_mu2", rm2, "mu_{6-2} = 3843/1403")
rec("rec19_mu3", rm3, "mu_{6-3} = 4697/1403")
np_check(A, b, [rm1, rm2, rm3], "rec19 (c)")
rec("rec19_mu1_f", float(rm1))
rec("rec19_mu2_f", float(rm2))
rec("rec19_mu3_f", float(rm3))
rec("rec19_mu1_mc", ms, "Monte-Carlo mu_{6-1}")

print("\n-- (d) ice cream cones --")
# v_i(0) = P(no further 6-2 -> 6-1 or 6-3 -> 6-1 transition ever | now at i)
A = [[F(1, 2), F(-1, 8), F(-1, 8)],
     [F(0), F(1), F(-1, 8)],
     [F(0), F(-3, 8), F(1)]]
b = [F(1, 4), F(1, 2), F(1, 4)]
v10, v20, v30 = frac_solve(A, b)
rec("rec19_v1_0", v10, "v_{6-1}(0) = 46/61")
rec("rec19_v2_0", v20, "v_{6-2}(0) = 34/61")
rec("rec19_v3_0", v30, "v_{6-3}(0) = 28/61")
np_check(A, b, [v10, v20, v30], "rec19 (d) v(0)")
# v_i(1): exactly one more such transition
A = [[F(1, 2), F(-1, 8), F(-1, 8)],
     [F(0), F(1), F(-1, 8)],
     [F(0), F(-3, 8), F(1)]]
b = [F(0), F(3, 8) * v10, F(3, 8) * v10]
v11, v21, v31 = frac_solve(A, b)
rec("rec19_v1_1", v11, "v_{6-1}(1) = 690/3721")
rec("rec19_v2_1", v21, "v_{6-2}(1) = 1242/3721")
rec("rec19_v3_1", v31, "v_{6-3}(1) = 1518/3721")
np_check(A, b, [v11, v21, v31], "rec19 (d) v(1)")
rec("rec19_v1_0_over3721", v10 - 0, "46/61 = 2806/3721")
p2 = 1 - v10 - v11
rec("rec19_v1_2plus", p2, "P(2 or more cones) = 225/3721")
EN = 0 * v10 + 1 * v11 + 2 * p2
rec("rec19_EN", EN, "E[N] = 1140/3721")
rec("rec19_EN_f", float(EN))
rec("rec19_v1_0_f", float(v10))
rec("rec19_v1_1_f", float(v11))
rec("rec19_v1_2plus_f", float(p2))
# Monte-Carlo for E[N]
NS = 300_000
states = [1, 2, 3, 4, 5]
Pmat = np.array([[float(Pj.get((i, j), 0)) for j in states] for i in states])
cum = np.cumsum(Pmat, axis=1)
cur = np.zeros(NS, int)          # index 0 = state 1 = 6-1
cones = np.zeros(NS, int)
live = np.ones(NS, bool)
for _ in range(3000):
    if not live.any():
        break
    u = rng.random(live.sum())
    prev = cur[live]
    nxt = (u[:, None] > cum[prev]).sum(axis=1)
    got = ((prev == 1) | (prev == 2)) & (nxt == 0)
    c = cones[live]
    c = c + (got & (c < 2))
    cones[live] = c
    cur[live] = nxt
    live = live & (cur < 3)
rec("rec19_EN_mc", float(cones.mean()), "Monte-Carlo E[N]")

print("\n-- (e) expected time to absorption CONDITIONED on ending in course 15 --")
av = {1: ra1, 2: ra2, 3: ra3, 4: F(0), 5: F(1)}
cond = {}
for i in (1, 2, 3):
    row = {}
    for j, p in Pj.items() and [(j, p) for (ii, j), p in Pj.items() if ii == i]:
        row[j] = av[j] * p / av[i]
    cond[i] = row
    s = sum(row.values())
    print(f"    conditional row {i}: " +
          ", ".join(f"p~_{i},{j} = {v.numerator}/{v.denominator} = {float(v):.6f}"
                    for j, v in sorted(row.items())) + f"   (sums to {s})")
    assert s == 1
for i in (1, 2, 3):
    for j in (1, 2, 3, 5):
        if j in cond[i]:
            rec(f"rec19_cond_p{i}{j}", float(cond[i][j]))
A = [[(1 if i == j else 0) - cond[i].get(j, F(0)) for j in (1, 2, 3)] for i in (1, 2, 3)]
b = [F(1), F(1), F(1)]
mt1, mt2, mt3 = frac_solve(A, b)
# elimination intermediates quoted in the prose:
#   mu~_2 = B2 + C2 mu~_1 ,  mu~_3 = B3 + C3 mu~_1 ,  then mu~_1 = N / D
c21, c23 = cond[2][1], cond[2][3]
c31, c32 = cond[3][1], cond[3][2]
B2 = (1 + c23) / (1 - c23 * c32)
C2 = (c21 + c23 * c31) / (1 - c23 * c32)
rec("rec19_e_B2", B2, "mu~_2 = B2 + C2 mu~_1 : B2 = 306776/270413")
rec("rec19_e_C2", C2, "C2 = 87885/270413")
rec("rec19_e_B2_f", float(B2))
rec("rec19_e_C2_f", float(C2))
B3 = 1 + c32 * B2
C3 = c31 + c32 * C2
rec("rec19_e_B3", B3, "mu~_3 = B3 + C3 mu~_1")
rec("rec19_e_C3", C3)
rec("rec19_e_B3_f", float(B3))
rec("rec19_e_C3_f", float(C3))
c12, c13 = cond[1][2], cond[1][3]
NUM = 2 + 2 * c12 * B2 + 2 * c13 * B3
DEN = 1 - 2 * c12 * C2 - 2 * c13 * C3
rec("rec19_e_NUM", NUM, "mu~_1 = NUM / DEN after substituting")
rec("rec19_e_DEN", DEN)
rec("rec19_e_NUM_f", float(NUM))
rec("rec19_e_DEN_f", float(DEN))
assert NUM / DEN == mt1
# the four products displayed in the final substitution step of (e)
rec("rec19_e_t1", float(2 * c12 * B2), "2*p~12*B2")
rec("rec19_e_t2", float(2 * c12 * C2), "2*p~12*C2")
rec("rec19_e_t3", float(2 * c13 * B3), "2*p~13*B3")
rec("rec19_e_t4", float(2 * c13 * C3), "2*p~13*C3")
rec("rec19_e_2p12", float(2 * c12), "2*p~12 = 143/420")
rec("rec19_e_2p13", float(2 * c13), "2*p~13 = 31/140")
rec("rec19_e_c21plus", float(c21 + c23 * c31), "0.275350 + 0.081294*0.423387")
rec("rec19_e_c23c32", float(c23 * c32), "p~23 * p~32 = 3/64")
rec("rec19_e_1minus", float(1 - c23 * c32), "1 - 3/64 = 61/64")
rec("rec19_mutilde1", mt1, "mu~_{6-1} = 1763/483")
rec("rec19_mutilde2", mt2)
rec("rec19_mutilde3", mt3)
np_check(A, b, [mt1, mt2, mt3], "rec19 (e)")
rec("rec19_mutilde1_f", float(mt1))
rec("rec19_mutilde2_f", float(mt2))
rec("rec19_mutilde3_f", float(mt3))
# Monte-Carlo: simulate original chain, keep only runs absorbed at 15
NS = 400_000
cur = np.zeros(NS, int)
steps = np.zeros(NS)
live = np.ones(NS, bool)
for _ in range(4000):
    if not live.any():
        break
    u = rng.random(live.sum())
    nxt = (u[:, None] > cum[cur[live]]).sum(axis=1)
    cur[live] = nxt
    steps[live] += 1
    live = live & (cur < 3)
sel = cur == 4        # index 4 = state 15
rec("rec19_mutilde1_mc", float(steps[sel].mean()),
    "Monte-Carlo E[time | absorbed at 15]")
rec("rec19_mu_given9_mc", float(steps[cur == 3].mean()),
    "Monte-Carlo E[time | absorbed at 9]  (sanity: mixes back to mu_1)")
rec("rec19_mu_mix_check",
    float(h * steps[sel].mean() + (1 - h) * steps[cur == 3].mean()),
    "a_1*mu~_1 + (1-a_1)*mu~_1(9) should equal mu_1 = 3.5217")

print("\n-- (f) course 15 removed: expected days until course 9 --")
# 6-1: 1/2 stay, 1/6 each to 6-2, 6-3, 9.
# 6-2: 3/4 -> 6-1, 1/4 -> 6-3  (3/8 : 1/8 = 3 : 1 renormalized)
# 6-3: unchanged 3/8, 3/8, 1/4
A = [[F(1, 2), F(-1, 6), F(-1, 6)],
     [F(-3, 4), F(1), F(-1, 4)],
     [F(-3, 8), F(-3, 8), F(1)]]
b = [F(1), F(1), F(1)]
f1, f2, f3 = frac_solve(A, b)
rec("rec19_f_mu1", f1, "mu_{6-1} = 86/13")
rec("rec19_f_mu2", f2)
rec("rec19_f_mu3", f3)
np_check(A, b, [f1, f2, f3], "rec19 (f)")
rec("rec19_f_mu1_f", float(f1))
rec("rec19_f_mu2_f", float(f2))
rec("rec19_f_mu3_f", float(f3))
Pf = {(1, 1): F(1, 2), (1, 2): F(1, 6), (1, 3): F(1, 6), (1, 4): F(1, 6),
      (2, 1): F(3, 4), (2, 3): F(1, 4),
      (3, 1): F(3, 8), (3, 2): F(3, 8), (3, 4): F(1, 4), (4, 4): F(1)}
for i in (1, 2, 3):
    assert sum(p for (ii, j), p in Pf.items() if ii == i) == 1
_, ms = absorb_sim(Pf, [1, 2, 3, 4], 1, {4}, rng, target=4)
rec("rec19_f_mu1_mc", ms, "Monte-Carlo")

print("\n-- (g) 9 and 15 communicate: long-run distribution --")
Pg = np.array([
    [0.5, 0.125, 0.125, 0.125, 0.125],
    [0.375, 0.0, 0.125, 0.0, 0.5],
    [0.375, 0.375, 0.0, 0.25, 0.0],
    [0.0, 0.0, 0.0, 0.5, 0.5],
    [0.0, 0.0, 0.0, 0.5, 0.5]])
assert np.allclose(Pg.sum(1), 1)
Pg_big = np.linalg.matrix_power(Pg, 400)
rec("rec19_g_pi9", float(Pg_big[0, 3]), "lim r_{6-1,9}(n)")
rec("rec19_g_pi15", float(Pg_big[0, 4]), "lim r_{6-1,15}(n)")
rec("rec19_g_pi61", float(Pg_big[0, 0]), "lim r_{6-1,6-1}(n) = 0")
rec("rec19_g_pi62", float(Pg_big[0, 1]))
rec("rec19_g_pi63", float(Pg_big[0, 2]))

print("\n-- (h) mean recurrence time of 6-1 --")
# chain: 9 and 15 each return to 6-1 w.p. 1/8, stay w.p. 7/8
mu9 = F(1) / F(1, 8)
rec("rec19_h_mu9", mu9, "mu_9 = 8 (geometric with p = 1/8)")
# mu_2 = 1 + (1/8) mu_3 + (1/2) mu_15 ; mu_3 = 1 + (3/8) mu_2 + (1/4) mu_9
A = [[F(1), F(-1, 8)], [F(-3, 8), F(1)]]
b = [1 + F(1, 2) * mu9, 1 + F(1, 4) * mu9]
h2, h3 = frac_solve(A, b)
rec("rec19_h_mu2", h2, "mu_{6-2} = 344/61")
rec("rec19_h_mu3", h3, "mu_{6-3} = 312/61")
np_check(A, b, [h2, h3], "rec19 (h)")
ER = F(1, 2) * 1 + F(1, 8) * (1 + mu9) * 2 + F(1, 8) * (1 + h2) + F(1, 8) * (1 + h3)
rec("rec19_h_ER", ER, "E[R] = 265/61")
rec("rec19_h_ER_f", float(ER))
rec("rec19_h_term_9", F(1, 8) * (1 + mu9), "(1/8)(1+8) = 9/8")
rec("rec19_h_term_62", F(1, 8) * (1 + h2), "(1/8)(405/61)")
rec("rec19_h_term_63", F(1, 8) * (1 + h3), "(1/8)(373/61)")
# steady state of the part-(h) chain
Ph = np.array([
    [0.5, 0.125, 0.125, 0.125, 0.125],
    [0.375, 0.0, 0.125, 0.0, 0.5],
    [0.375, 0.375, 0.0, 0.25, 0.0],
    [0.125, 0.0, 0.0, 0.875, 0.0],
    [0.125, 0.0, 0.0, 0.0, 0.875]])
assert np.allclose(Ph.sum(1), 1)
M = np.vstack([(Ph.T - np.eye(5))[:4], np.ones(5)])
pi = np.linalg.solve(M, np.array([0, 0, 0, 0, 1.0]))
for k, nm in enumerate(["61", "62", "63", "9", "15"]):
    rec(f"rec19_h_pi_{nm}", float(pi[k]), f"pi_{nm} (target {[61,11,9,79,105][k]}/265)")
rec("rec19_h_pi61_recip", float(1 / pi[0]), "1/pi_{6-1} = 265/61")
rec("rec19_h_pi_targets", [61 / 265, 11 / 265, 9 / 265, 79 / 265, 105 / 265],
    "quoted values 61,11,9,79,105 over 265")
print(f"    max deviation from quoted pi = "
      f"{float(np.max(np.abs(pi - np.array([61,11,9,79,105])/265))):.2e}")
rec("rec19_h_pi_dev", float(np.max(np.abs(pi - np.array([61, 11, 9, 79, 105]) / 265))))

# =====================================================================
head("G.  Practice-question answers")
# P4.1 two transient, one absorbing pair:  0 <-1/3- 1 -2/3-> 2 (absorbing at 0 and 2)
A = [[F(1)]]
rec("prac_1_a", F(2, 3), "single transient state: a = 2/3")
# P4.2 three-state: 1 -> 2 (0.5), 1 -> A (0.5); 2 -> 1 (0.25), 2 -> B (0.75)
A = [[F(1), F(-1, 2)], [F(-1, 4), F(1)]]
b = [F(1, 2), F(0)]
q1, q2 = frac_solve(A, b)
rec("prac_2_a1", q1, "P(absorbed at A | start 1) = 4/7")
rec("prac_2_a2", q2, "P(absorbed at A | start 2) = 1/7")
b = [F(1), F(1)]
w1, w2 = frac_solve(A, b)
rec("prac_2_mu1", w1, "mu_1 = 12/7")
rec("prac_2_mu2", w2, "mu_2 = 10/7")
# P4.3 gambler's ruin with p = 0.48, m = 100, i = 50
rec("prac_3_a", float(ruin_exact(F(12, 25), 100)[50]), "p=0.48, m=100, a_50")
rec("prac_3_D", float(ruin_duration_exact(F(12, 25), 100)[50]), "p=0.48, m=100, D_50")
rec("prac_3_a_fair", float(ruin_exact(F(1, 2), 100)[50]))
rec("prac_3_D_fair", float(ruin_duration_exact(F(1, 2), 100)[50]))
# P4.4 spider-fly with m = 5 (three transient states, symmetric 0.3/0.4/0.3)
A = [[F(3, 5), F(-3, 10), F(0)],
     [F(-3, 10), F(3, 5), F(-3, 10)],
     [F(0), F(-3, 10), F(3, 5)]]
b = [F(1), F(1), F(1)]
s2, s3, s4 = frac_solve(A, b)
rec("prac_4_mu2", s2, "m=5 spider-fly, mu_2")
rec("prac_4_mu3", s3, "mu_3")
rec("prac_4_mu4", s4, "mu_4")
np_check(A, b, [s2, s3, s4], "practice 4.4")
# P4.9 mean first passage time to course 9 in the part-(h) chain.
# unknowns t_1 (6-1), t_2 (6-2), t_3 (6-3), t_15 ; t_9 = 0
A = [[F(1, 2), F(-1, 8), F(-1, 8), F(-1, 8)],
     [F(-3, 8), F(1), F(-1, 8), F(-1, 2)],
     [F(-3, 8), F(-3, 8), F(1), F(0)],
     [F(-1, 8), F(0), F(0), F(1, 8)]]
b = [F(1), F(1), F(1), F(1)]
q1, q2, q3, q15 = frac_solve(A, b)
rec("prac_9_t1", q1, "t_{6-1} to course 9")
rec("prac_9_t2", q2)
rec("prac_9_t3", q3)
rec("prac_9_t15", q15, "should equal 8 + t_1")
np_check(A, b, [q1, q2, q3, q15], "practice 4.9")
rec("prac_9_t1_f", float(q1))
rec("prac_9_t2_f", float(q2))
rec("prac_9_t3_f", float(q3))
rec("prac_9_t15_f", float(q15))
assert q15 == 8 + q1

# P4.5 mean recurrence time in the L18 slide-3 two-state chain:
# p11 = 0.5, p12 = 0.5, p21 = 0.2, p22 = 0.8  -> pi_1 = 2/7 (established in section 3)
tt2b = F(1) / F(2, 10)
rec("prac_5_t2_correct", tt2b, "t_2 = 1/0.2 = 5")
tt1sb = 1 + F(5, 10) * 0 + F(5, 10) * tt2b
rec("prac_5_t1star_correct", tt1sb, "t_1^* = 1 + 0.5*5 = 7/2")
rec("prac_5_pi1_correct", 1 / tt1sb, "pi_1 = 2/7  [matches L18 slide 3]")

# =====================================================================
head("H.  Widget verification grid (gambler's ruin explorer)")
grid = []
for pv, mv, iv in [(0.50, 20, 10), (0.45, 20, 10), (0.55, 20, 10),
                   (0.40, 30, 15), (0.50, 30, 10), (0.48, 50, 25)]:
    pf = F(pv).limit_denominator(1000)
    aa = float(ruin_exact(pf, mv)[iv])
    dd = float(ruin_duration_exact(pf, mv)[iv])
    an, dn = ruin_linear(pv, mv)
    print(f"  p={pv:.2f} m={mv:3d} i={iv:3d} :  a_i = {aa:.6f}  D_i = {dd:10.4f}   "
          f"(linear solve {an[iv-1]:.6f}, {dn[iv-1]:.4f})")
    grid.append({"p": pv, "m": mv, "i": iv, "a": aa, "D": dd})
R["widget_grid"] = grid

OUT.write_text(json.dumps(R, indent=1), encoding="utf-8")
print(f"\nwrote {OUT}  ({len(R)} keys)")
