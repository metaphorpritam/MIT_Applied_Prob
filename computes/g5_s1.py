# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Numbers for G5 section 1 — the Markov model, transition probabilities,
n-step transition probabilities r_ij(n) and Chapman-Kolmogorov.

Sources: L16 slides 2-6, rec18 problems 1 and 3, B&T sections 7.1-7.2.

Run:  uv run computes/g5_s1.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
OUT: dict[str, object] = {}


def rec(key, val, label=""):
    if isinstance(val, np.ndarray):
        val = val.tolist()
    OUT[key] = val
    print(f"{key:34s} = {val}   {label}")


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


# ===========================================================================
# A. The two-state chain of L16 slide 5:  p11=0.5 p12=0.5 p21=0.2 p22=0.8
# ===========================================================================
head("A. Two-state chain (L16 slide 5)")

P2 = np.array([[0.5, 0.5],
               [0.2, 0.8]])
rec("A_P", P2, "transition matrix")
rec("A_rowsums", P2.sum(axis=1), "each row must be 1")

# n-step matrices by repeated multiplication
ns = [0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 20, 50, 100, 101]
tbl = {}
R = np.eye(2)
cur = 0
for n in range(0, 102):
    if n in ns:
        tbl[n] = R.copy()
    R = R @ P2
for n in ns:
    M = tbl[n]
    rec(f"A_r_n{n}", [[float(f"{M[i,j]:.12f}") for j in range(2)] for i in range(2)],
        f"r_ij({n})")

# the table exactly as the slide asks for it
for n in [0, 1, 2, 100, 101]:
    M = tbl[n]
    rec(f"A_r11_{n}", round(float(M[0, 0]), 12))
    rec(f"A_r12_{n}", round(float(M[0, 1]), 12))
    rec(f"A_r21_{n}", round(float(M[1, 0]), 12))
    rec(f"A_r22_{n}", round(float(M[1, 1]), 12))

# closed form  r11(n) = 2/7 + (5/7) 0.3^n ,  r21(n) = 2/7 - (2/7) 0.3^n
lam = P2[0, 0] + P2[1, 1] - 1.0
rec("A_lambda2", lam, "second eigenvalue p11+p22-1")
rec("A_eigs", sorted(np.linalg.eigvals(P2).real.tolist(), reverse=True))
pi1, pi2 = 2 / 7, 5 / 7
rec("A_pi1", round(pi1, 12), "limit of r_i1(n) = 0.2/(0.5+0.2)")
rec("A_pi2", round(pi2, 12))


def r11_closed(n):
    return pi1 + pi2 * lam ** n


def r21_closed(n):
    return pi1 - pi1 * lam ** n


err = max(abs(r11_closed(n) - tbl[n][0, 0]) for n in ns)
rec("A_closedform_maxerr_r11", float(f"{err:.3e}"), "closed form vs matrix power")
err2 = max(abs(r21_closed(n) - tbl[n][1, 0]) for n in ns)
rec("A_closedform_maxerr_r21", float(f"{err2:.3e}"))
rec("A_r11_100_minus_pi1", float(f"{tbl[100][0,0] - pi1:.3e}"),
    "distance from the limit at n=100")
# how many decimals of agreement at small n (the Interpretation box of s1.4)
for n in [10, 11, 12]:
    gap = max(abs(tbl[n][i, 0] - pi1) for i in (0, 1))
    rec(f"A_gap_n{n}", float(f"{gap:.3e}"),
        f"max_i |r_i1({n}) - 2/7|; < 0.5e-d means d correct decimals")
rec("A_lam_pow100", float(f"{lam**100:.3e}"))

# Chapman-Kolmogorov in the general form r(n+m) = r(n) r(m)
ck = np.linalg.matrix_power(P2, 7) - np.linalg.matrix_power(P2, 3) @ np.linalg.matrix_power(P2, 4)
rec("A_CK_general_maxerr", float(f"{np.abs(ck).max():.3e}"), "r(7) vs r(3)r(4)")

# random initial state:  P(X0=1)=0.6, P(X0=2)=0.4
p0 = np.array([0.6, 0.4])
rec("A_p0", p0)
for n in [1, 2, 5, 100]:
    rec(f"A_dist_n{n}", [round(v, 12) for v in (p0 @ np.linalg.matrix_power(P2, n)).tolist()])

# monotone convergence data for the figure
A_conv_n = list(range(0, 21))
A_conv_r11 = [float(np.linalg.matrix_power(P2, n)[0, 0]) for n in A_conv_n]
A_conv_r21 = [float(np.linalg.matrix_power(P2, n)[1, 0]) for n in A_conv_n]
OUT["A_conv_n"] = A_conv_n
OUT["A_conv_r11"] = A_conv_r11
OUT["A_conv_r21"] = A_conv_r21


# ===========================================================================
# B. Checkout counter (L16 slide 2): Bernoulli(p) arrivals, geometric(q) service
# ===========================================================================
head("B. Checkout counter, buffer m")


def checkout_matrix(p, q, m):
    """States 0..m = number of customers at the counter.

    Within one slot: an arrival occurs w.p. p (independently); if the counter is
    busy (state >= 1) the customer in service departs w.p. q (independently).
    An arrival that finds the buffer full (state m) is turned away.
    """
    P = np.zeros((m + 1, m + 1))
    P[0, 1] = p            # arrival, nobody in service so no departure
    P[0, 0] = 1 - p
    for i in range(1, m):
        P[i, i + 1] = p * (1 - q)          # arrival, no departure
        P[i, i - 1] = q * (1 - p)          # departure, no arrival
        P[i, i] = p * q + (1 - p) * (1 - q)  # both or neither
    P[m, m - 1] = q * (1 - p)
    P[m, m] = 1 - q * (1 - p)
    return P


p_a, q_s, m_buf = 0.2, 0.4, 10
Pc = checkout_matrix(p_a, q_s, m_buf)
rec("B_p", p_a)
rec("B_q", q_s)
rec("B_m", m_buf)
rec("B_p_up", round(p_a * (1 - q_s), 12), "p(1-q) = p_{i,i+1}")
rec("B_p_down", round(q_s * (1 - p_a), 12), "q(1-p) = p_{i,i-1}")
rec("B_p_self", round(p_a * q_s + (1 - p_a) * (1 - q_s), 12), "pq+(1-p)(1-q) = p_ii")
rec("B_p_self_check", round(1 - p_a * (1 - q_s) - q_s * (1 - p_a), 12),
    "same thing as 1 - up - down")
rec("B_p00", round(1 - p_a, 12))
rec("B_p01", round(p_a, 12))
rec("B_pmm", round(1 - q_s * (1 - p_a), 12))
rec("B_rowsums_max_dev", float(f"{np.abs(Pc.sum(axis=1) - 1).max():.3e}"))
rec("B_rho", round((p_a * (1 - q_s)) / (q_s * (1 - p_a)), 12), "up/down ratio")

for n in [1, 2, 5, 20, 100]:
    row = np.linalg.matrix_power(Pc, n)[0]
    rec(f"B_r0j_n{n}", [round(float(v), 6) for v in row], f"start empty, n={n}")
OUT["B_states"] = list(range(m_buf + 1))

# expected number in system after n steps starting empty
for n in [1, 5, 20, 100]:
    row = np.linalg.matrix_power(Pc, n)[0]
    rec(f"B_mean_n{n}", round(float(row @ np.arange(m_buf + 1)), 6))

# a second parameter pair where the queue fills up: p=0.5, q=0.3
Pc2 = checkout_matrix(0.5, 0.3, m_buf)
rec("B2_p_up", round(0.5 * 0.7, 12))
rec("B2_p_down", round(0.3 * 0.5, 12))
rec("B2_r0j_n100", [round(float(v), 6) for v in np.linalg.matrix_power(Pc2, 100)[0]])
rec("B2_mean_n100", round(float(np.linalg.matrix_power(Pc2, 100)[0] @ np.arange(m_buf + 1)), 6))


# ===========================================================================
# C. Spider-and-fly chain (B&T Example 7.2), m = 4
# ===========================================================================
head("C. Spider and fly, m = 4 (B&T Example 7.2)")

Ps = np.zeros((4, 4))
Ps[0, 0] = 1.0
Ps[3, 3] = 1.0
for i in (1, 2):
    Ps[i, i - 1] = 0.3
    Ps[i, i] = 0.4
    Ps[i, i + 1] = 0.3
rec("C_P", Ps)
rec("C_rowsums_max_dev", float(f"{np.abs(Ps.sum(axis=1) - 1).max():.3e}"))
for n in [1, 2, 3, 10, 50]:
    rec(f"C_r2j_n{n}", [round(float(v), 6) for v in np.linalg.matrix_power(Ps, n)[1]],
        f"start at state 2, n={n}")
rec("C_r2j_n200", [round(float(v), 6) for v in np.linalg.matrix_power(Ps, 200)[1]])


# ===========================================================================
# D. rec18 P1 — painting fish
# ===========================================================================
head("D. rec18 P1 — painting fish, n fish in the lake")

n_fish = 4


def fish_matrix(n):
    P = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        P[i, i] = (n - i) / n        # a blue fish is caught: state unchanged
        if i >= 1:
            P[i, i - 1] = i / n      # a green fish is caught and painted blue
    return P


Pf = fish_matrix(n_fish)
rec("D_n", n_fish)
rec("D_P", Pf)
rec("D_rowsums_max_dev", float(f"{np.abs(Pf.sum(axis=1) - 1).max():.3e}"))
rec("D_p00", float(Pf[0, 0]), "state 0 is absorbing")
for n in [1, 2, 5, 10, 30]:
    rec(f"D_r4j_n{n}", [round(float(v), 6) for v in np.linalg.matrix_power(Pf, n)[n_fish]],
        f"start with all {n_fish} green, n={n}")
# expected number of green fish after n days, start i=n_fish : (1-1/n)^n * n_fish
for n in [1, 5, 10]:
    row = np.linalg.matrix_power(Pf, n)[n_fish]
    rec(f"D_mean_green_n{n}", round(float(row @ np.arange(n_fish + 1)), 6))
    rec(f"D_mean_green_formula_n{n}", round(n_fish * (1 - 1 / n_fish) ** n, 6))


# ===========================================================================
# E. rec18 P3 — six-state chain s0..s5
# ===========================================================================
head("E. rec18 P3 — six-state chain")

# index order: 0->s0, 1->s1, 2->s2, 3->s3, 4->s4, 5->s5
S = np.zeros((6, 6))
S[0, 1] = S[0, 3] = S[0, 5] = 1 / 3
S[1, 1] = 1.0
S[2, 1] = 0.5
S[2, 2] = 0.5
S[3, 2] = 0.25
S[3, 3] = 0.25
S[3, 4] = 0.5
S[4, 4] = 0.5
S[4, 5] = 0.5
S[5, 5] = 1.0
rec("E_P", S)
rec("E_rowsums_max_dev", float(f"{np.abs(S.sum(axis=1) - 1).max():.3e}"))

# (a) P(first entry to s2 on trial k) = (1/3)(1/4)^{k-1}, k >= 2
Ea = {k: float(Fraction(1, 3) * Fraction(1, 4) ** (k - 1)) for k in range(2, 9)}
rec("E_a_k2", round(Ea[2], 12), "= 1/12")
rec("E_a_k3", round(Ea[3], 12), "= 1/48")
rec("E_a_k4", round(Ea[4], 12))
OUT["E_a_table"] = {str(k): round(v, 10) for k, v in Ea.items()}
# brute-force check by enumerating paths of length k
def first_entry_s2(k):
    """P(X_1..X_{k-1} != s2, X_k = s2 | X_0 = s0) by dynamic programming."""
    v = np.zeros(6)
    v[0] = 1.0
    tot = 0.0
    for step in range(1, k + 1):
        v = v @ S
        tot_here = v[2]
        if step == k:
            return tot_here
        v[2] = 0.0     # kill paths that already hit s2
    return tot


for k in range(2, 9):
    d = abs(first_entry_s2(k) - Ea[k])
    assert d < 1e-12, (k, d)
rec("E_a_dp_check_maxerr", 0.0, "DP over killed chain matches the formula")
rec("E_a_sum", round(float(sum(Fraction(1, 3) * Fraction(1, 4) ** (k - 1)
                              for k in range(2, 400))), 12), "P(ever enter s2) = 1/9")
rec("E_a_sum_exact", "1/9")

# (b) P(never enter s4)
#     a_i = P(ever reach s4 | start i)
#     a_1 = a_5 = 0, a_4 = 1, a_2 = 0.5 a_2 + 0.5 a_1, a_3 = .25a_3+.25a_2+.5a_4
A = np.zeros((4, 4))   # unknowns a_0, a_2, a_3  (a_1=a_5=0, a_4=1)
# solve directly with a linear system on states {0,2,3}
M = np.array([[1.0, 0.0, -1 / 3],
              [0.0, 0.5, 0.0],
              [0.0, -0.25, 0.75]])
b = np.array([0.0, 0.0, 0.5])
a0, a2, a3 = np.linalg.solve(M, b)
rec("E_b_a3", round(float(a3), 12), "P(reach s4 | start s3) = 2/3")
rec("E_b_a2", round(float(a2), 12))
rec("E_b_a0", round(float(a0), 12), "P(reach s4 | start s0) = 2/9")
rec("E_b_never", round(float(1 - a0), 12), "= 7/9")
rec("E_b_two_thirds", round(2 / 3, 12), "P(first transition to s1 or s5)")
rec("E_b_ninth", round(1 / 9, 12), "P(s0->s3 then eventually to s2)")
rec("E_b_leave_to_s2", round(0.25 / (0.25 + 0.5), 12), "(1/4)/(1/4+1/2) = 1/3")
rec("E_b_geom_check", round(float(sum(0.25 ** mm * 0.25 for mm in range(0, 400))), 12),
    "sum_{m>=0} (1/4)^m (1/4) = 1/3")
# Monte-Carlo cross check of (b)
rng = np.random.default_rng(20101109)
NSIM = 400000
hits = 0
for _ in range(NSIM):
    s = 0
    for _t in range(400):
        s = rng.choice(6, p=S[s])
        if s == 4:
            hits += 1
            break
        if s in (1, 5):
            break
rec("E_b_never_mc", round(1 - hits / NSIM, 6), f"Monte Carlo, {NSIM} runs")

# (c) enters s2 and leaves on the next trial
rec("E_c", round(float(Fraction(1, 9) * Fraction(1, 2)), 12), "(1/9)(1/2) = 1/18")
rec("E_c_exact", "1/18")

# (d) first entry into s1 on the third trial
rec("E_d", round(float(Fraction(1, 3) * Fraction(1, 4) * Fraction(1, 2)), 12), "= 1/24")
rec("E_d_exact", "1/24")
# DP check: probability of being in s1 for the first time at step 3
v = np.zeros(6); v[0] = 1.0
for step in range(1, 4):
    v = v @ S
    if step < 3:
        v[1] = 0.0
rec("E_d_dp", round(float(v[1]), 12))

# (e) P(X_n = s3) = (1/3)(1/4)^{n-1}
for n in [1, 2, 3, 5]:
    val = float(np.linalg.matrix_power(S, n)[0, 3])
    rec(f"E_e_n{n}", round(val, 12))
    rec(f"E_e_n{n}_formula", round(float(Fraction(1, 3) * Fraction(1, 4) ** (n - 1)), 12))
OUT["E_e_n"] = list(range(1, 11))
OUT["E_e_vals"] = [round(float(np.linalg.matrix_power(S, n)[0, 3]), 12) for n in range(1, 11)]


# ===========================================================================
# F. L16 slide 6 — the two convergence chains, answered as r_ij(n) computations
# ===========================================================================
head("F. L16 slide 6 chains")

# (i) periodic 3-state chain: p12=1, p21=0.5, p23=0.5, p32=1
Pp = np.array([[0.0, 1.0, 0.0],
               [0.5, 0.0, 0.5],
               [0.0, 1.0, 0.0]])
rec("F_Pper", Pp)
rec("F_per_rowsums_max_dev", float(f"{np.abs(Pp.sum(axis=1) - 1).max():.3e}"))
F_r22 = [round(float(np.linalg.matrix_power(Pp, n)[1, 1]), 12) for n in range(0, 11)]
rec("F_r22_n0to10", F_r22, "r_22(n): 1,0,1,0,... period 2")
OUT["F_r22_n"] = list(range(0, 11))

# (ii) four-state chain: state 1 absorbing; state 2 -> 1 w.p. .3, self .4, -> 3 w.p. .3;
#      {3,4} a closed recurrent class (internal probabilities immaterial)
F_r21 = [round(0.5 * (1 - 0.4 ** n), 12) for n in range(0, 13)]
rec("F_r21_n0to12", F_r21, "r_21(n) = (1/2)(1 - 0.4^n) -> 1/2")
OUT["F_r21_n"] = list(range(0, 13))
# explicit numeric confirmation with an arbitrary completion of the {3,4} block
Pq = np.array([[1.0, 0.0, 0.0, 0.0],
               [0.3, 0.4, 0.3, 0.0],
               [0.0, 0.0, 0.6, 0.4],
               [0.0, 0.0, 0.7, 0.3]])
chk = max(abs(np.linalg.matrix_power(Pq, n)[1, 0] - 0.5 * (1 - 0.4 ** n)) for n in range(0, 13))
rec("F_r21_completion_maxerr", float(f"{chk:.3e}"),
    "r_21(n) does not depend on the {3,4} internals")
rec("F_r11_any_n", 1.0, "state 1 is absorbing")
rec("F_r31_any_n", 0.0, "1 is not reachable from 3")
rec("F_r21_limit", 0.5)
rec("F_r21_n1", F_r21[1])
rec("F_r21_n5", F_r21[5])
rec("F_r21_n10", F_r21[10])


# ===========================================================================
# G. Practice questions
# ===========================================================================
head("G. Practice")

# G1: Alice up-to-date / behind (B&T Example 7.1)
Pa = np.array([[0.8, 0.2],
               [0.6, 0.4]])
rec("G1_r_n2", [[round(float(v), 6) for v in row] for row in (Pa @ Pa)])
rec("G1_r11_2", round(float((Pa @ Pa)[0, 0]), 6), "0.8*0.8+0.2*0.6")
rec("G1_r_n10", [[round(float(v), 6) for v in row]
                 for row in np.linalg.matrix_power(Pa, 10)])
rec("G1_limit", [round(0.75, 6), round(0.25, 6)], "0.6/(0.2+0.6) = 3/4")
rec("G1_lambda", round(0.8 + 0.4 - 1, 6))

# G2: two-day weather chain, P(X0=sun)=0.5
Pw = np.array([[0.9, 0.1],
               [0.5, 0.5]])
p0w = np.array([0.5, 0.5])
rec("G2_P", Pw)
rec("G2_r_n2", [[round(float(v), 6) for v in row] for row in (Pw @ Pw)])
rec("G2_dist_n2", [round(float(v), 6) for v in (p0w @ Pw @ Pw)])
rec("G2_dist_n1", [round(float(v), 6) for v in (p0w @ Pw)])
rec("G2_limit", [round(5 / 6, 6), round(1 / 6, 6)])

# G3: two independent 2-state chains -> product chain of 4 states (Markov?) - numeric
# G3 practice: three-state chain with a given matrix, compute r(3) and check CK
Pg = np.array([[0.5, 0.3, 0.2],
               [0.0, 0.6, 0.4],
               [0.4, 0.0, 0.6]])
rec("G3_P_rowsums", [round(float(v), 6) for v in Pg.sum(axis=1)])
rec("G3_r_n2", [[round(float(v), 6) for v in row] for row in (Pg @ Pg)])
rec("G3_r_n3", [[round(float(v), 6) for v in row] for row in np.linalg.matrix_power(Pg, 3)])
rec("G3_r13_3", round(float(np.linalg.matrix_power(Pg, 3)[0, 2]), 6))
rec("G3_CK_err", float(f"{np.abs(np.linalg.matrix_power(Pg,3) - Pg @ (Pg @ Pg)).max():.3e}"))

# G4: gambler / random walk on {0,1,2,3} with absorbing ends, p=0.6
Pgw = np.zeros((4, 4))
Pgw[0, 0] = 1.0
Pgw[3, 3] = 1.0
for i in (1, 2):
    Pgw[i, i + 1] = 0.6
    Pgw[i, i - 1] = 0.4
rec("G4_r1j_n2", [round(float(v), 6) for v in (Pgw @ Pgw)[1]])
rec("G4_r1j_n3", [round(float(v), 6) for v in np.linalg.matrix_power(Pgw, 3)[1]])
rec("G4_r13_2", round(float((Pgw @ Pgw)[1, 3]), 6), "0.6*0.6 = 0.36")

# G5: the non-Markov counterexample. Z_1,Z_2,... i.i.d. fair coin flips (1 = heads);
# X_n = Z_{n-1} + Z_n = number of heads among the last two flips, n >= 2.
# Enumerate all 2^4 patterns of (Z_{n-2}, Z_{n-1}, Z_n, Z_{n+1}), each of probability 1/16.
import itertools  # noqa: E402

pats = list(itertools.product([0, 1], repeat=4))
w = 1 / 16


def prob(cond, target):
    num = sum(w for z in pats if cond(z) and target(z))
    den = sum(w for z in pats if cond(z))
    return num / den, den


v, d = prob(lambda z: z[1] + z[2] == 1, lambda z: z[2] + z[3] == 2)
rec("G5_P_next2_given_Xn1", round(v, 12), "P(X_{n+1}=2 | X_n=1) = 1/4")
v2, _ = prob(lambda z: z[1] + z[2] == 1 and z[0] + z[1] == 2,
             lambda z: z[2] + z[3] == 2)
rec("G5_P_next2_given_Xn1_Xnm1_2", round(v2, 12),
    "P(X_{n+1}=2 | X_n=1, X_{n-1}=2) = 0")
v3, _ = prob(lambda z: z[1] + z[2] == 1 and z[0] + z[1] == 0,
             lambda z: z[2] + z[3] == 2)
rec("G5_P_next2_given_Xn1_Xnm1_0", round(v3, 12),
    "P(X_{n+1}=2 | X_n=1, X_{n-1}=0) = 1/2")
# the enlarged state (Z_{n-1}, Z_n) IS Markov: 4 states, each row two 1/2's
Penl = np.array([[0.5, 0.5, 0.0, 0.0],     # (0,0) -> (0,0) or (0,1)
                 [0.0, 0.0, 0.5, 0.5],     # (0,1) -> (1,0) or (1,1)
                 [0.5, 0.5, 0.0, 0.0],     # (1,0) -> (0,0) or (0,1)
                 [0.0, 0.0, 0.5, 0.5]])    # (1,1) -> (1,0) or (1,1)
rec("G5_Penl_rowsums", [round(float(v), 6) for v in Penl.sum(axis=1)])
rec("G5_Penl_r_n2", [[round(float(v), 6) for v in row] for row in (Penl @ Penl)])

path = ROOT / "computes" / "g5_s1.json"
path.write_text(json.dumps(OUT, indent=1), encoding="utf-8")
print()
print("wrote", path, f"({len(OUT)} keys)")
