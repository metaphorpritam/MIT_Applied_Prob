# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Numbers for G5 section 2 — classification of states (recurrent / transient /
periodic) and the steady-state convergence question.

Sources: L17 slides 3-5, L16 slides 6-7, rec18 P1 and P3, B&T 7.2-7.3.

Run:  uv run computes/g5_s2.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
OUT: dict[str, object] = {}


def rec(key, val, fmt="{}"):
    if isinstance(val, np.ndarray):
        val = np.round(val, 12).tolist()
    OUT[key] = val
    print(f"{key:44s} = " + fmt.format(val))


def head(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# =====================================================================
# A.  Generic tools: accessibility, classes, period
# =====================================================================
def reach(P, i):
    """Set of states accessible from i (including i itself, reached in >=0 steps)."""
    n = P.shape[0]
    seen = {i}
    stack = [i]
    while stack:
        u = stack.pop()
        for v in range(n):
            if P[u, v] > 0 and v not in seen:
                seen.add(v)
                stack.append(v)
    return seen


def classify(P):
    """Return (recurrent_states, transient_states, recurrent_classes)."""
    n = P.shape[0]
    A = {i: reach(P, i) for i in range(n)}
    recurrent = [i for i in range(n) if all(i in A[j] for j in A[i])]
    transient = [i for i in range(n) if i not in recurrent]
    classes = []
    left = set(recurrent)
    while left:
        i = min(left)
        C = sorted(A[i])
        classes.append(C)
        left -= set(C)
    return recurrent, transient, classes


def period(P, i, nmax=400):
    """gcd of all n>=1 with r_ii(n) > 0."""
    Pn = np.eye(P.shape[0])
    d = 0
    for n in range(1, nmax + 1):
        Pn = Pn @ P
        if Pn[i, i] > 1e-14:
            d = gcd(d, n)
            if d == 1:
                return 1
    return d


def first_all_positive(P, nmax=200):
    """Smallest n with every entry of P^n strictly positive (aperiodicity test)."""
    Pn = np.eye(P.shape[0])
    for n in range(1, nmax + 1):
        Pn = Pn @ P
        if np.all(Pn > 1e-14):
            return n
    return None


# =====================================================================
# B.  L17 slide 3 warm-up chain (9 states) — our explicit reconstruction
#     States: 1=B2, 2=B3, 3=T1, 4=T2, 5=B1, 6=R1, 7=R2, 8=T3, 9=R3
#     (labels 1..9 stored at indices 0..8)
# =====================================================================
head("B. L17 slide 3 warm-up chain (9 states)")

W = np.zeros((9, 9))


def w(i, j, p):
    W[i - 1, j - 1] = p


w(1, 5, 0.2); w(1, 2, 0.5); w(1, 8, 0.3)
w(2, 1, 0.4); w(2, 6, 0.6)
w(3, 3, 0.2); w(3, 4, 0.5); w(3, 5, 0.3)
w(4, 3, 1.0)
w(5, 5, 0.4); w(5, 3, 0.6)
w(6, 6, 0.3); w(6, 7, 0.7)
w(7, 6, 1.0)
w(8, 4, 0.5); w(8, 2, 0.5)
w(9, 7, 1.0)

rec("warmup_rowsums_ok", bool(np.allclose(W.sum(axis=1), 1)))
r, t, cl = classify(W)
rec("warmup_recurrent_states", [i + 1 for i in r])
rec("warmup_transient_states", [i + 1 for i in t])
rec("warmup_recurrent_classes", [[i + 1 for i in c] for c in cl])
rec("warmup_period_class1_state3", period(W, 2))
rec("warmup_period_class2_state6", period(W, 5))
rec("warmup_A_of_1", sorted(i + 1 for i in reach(W, 0)))
rec("warmup_A_of_2", sorted(i + 1 for i in reach(W, 1)))
rec("warmup_A_of_8", sorted(i + 1 for i in reach(W, 7)))
rec("warmup_A_of_9", sorted(i + 1 for i in reach(W, 8)))
rec("warmup_A_of_3", sorted(i + 1 for i in reach(W, 2)))
rec("warmup_A_of_6", sorted(i + 1 for i in reach(W, 5)))

# Q1: P(X1=2, X2=6, X3=7 | X0=1) = p_12 p_26 p_67
q1 = W[0, 1] * W[1, 5] * W[5, 6]
rec("warmup_p12", W[0, 1])
rec("warmup_p26", W[1, 5])
rec("warmup_p67", W[5, 6])
rec("warmup_Q1", q1, "{:.6f}")

# Q2: r_27(4)
W4 = np.linalg.matrix_power(W, 4)
rec("warmup_Q2_r27_4", W4[1, 6], "{:.6f}")
# the four length-4 paths 2 -> ... -> 7 spelled out
paths = []
for a in range(9):
    for b in range(9):
        for c in range(9):
            pr = W[1, a] * W[a, b] * W[b, c] * W[c, 6]
            if pr > 0:
                paths.append(([2, a + 1, b + 1, c + 1, 7], pr))
rec("warmup_Q2_paths", [[p, round(v, 8)] for p, v in paths])
rec("warmup_Q2_path_sum", sum(v for _, v in paths), "{:.6f}")

# limiting behaviour of r_2j(n): absorbed into class {6,7}
W200 = np.linalg.matrix_power(W, 200)
W201 = np.linalg.matrix_power(W, 201)
rec("warmup_r2_row_n200", np.round(W200[1], 6))
rec("warmup_r2_row_n201", np.round(W201[1], 6))
rec("warmup_r26_avg_limit", (W200[1, 5] + W201[1, 5]) / 2, "{:.6f}")

# absorption split from state 1 (checked against the linear system in s4's language)
# a_i = P(end in class {6,7} | X0 = i)
Tset = [0, 1, 7, 8]  # transient labels 1,2,8,9 -> indices
Q = W[np.ix_(Tset, Tset)]
b = np.array([sum(W[i, j] for j in [5, 6]) for i in Tset])
a = np.linalg.solve(np.eye(4) - Q, b)
rec("warmup_absorb_right_class", dict(zip(["1", "2", "8", "9"], np.round(a, 6).tolist())))

# =====================================================================
# C.  L16 slide 6 chain (a): 3-state periodic chain
#     p12 = 1, p21 = .5, p23 = .5, p32 = 1
# =====================================================================
head("C. L16 slide 6(a): three-state periodic chain")

A3 = np.array([[0.0, 1.0, 0.0],
               [0.5, 0.0, 0.5],
               [0.0, 1.0, 0.0]])
rec("per3_rowsums_ok", bool(np.allclose(A3.sum(axis=1), 1)))
r, t, cl = classify(A3)
rec("per3_classes", [[i + 1 for i in c] for c in cl])
rec("per3_transient", [i + 1 for i in t])
rec("per3_period", period(A3, 1))
r22 = []
Pn = np.eye(3)
for n in range(1, 9):
    Pn = Pn @ A3
    r22.append(round(float(Pn[1, 1]), 10))
rec("per3_r22_n1to8", r22)
r11 = []
Pn = np.eye(3)
for n in range(1, 9):
    Pn = Pn @ A3
    r11.append(round(float(Pn[0, 0]), 10))
rec("per3_r11_n1to8", r11)
# balance-equation solution (exists but is not a limit)
M = np.vstack([(A3.T - np.eye(3))[:2], np.ones(3)])
rhs = np.array([0.0, 0.0, 1.0])
pi3 = np.linalg.solve(M, rhs)
rec("per3_balance_solution", np.round(pi3, 8))
# Cesaro (time-average) convergence
Pn = np.eye(3)
S = np.zeros((3, 3))
N = 20000
for n in range(1, N + 1):
    Pn = Pn @ A3
    S += Pn
rec("per3_cesaro_row1", np.round(S[0] / N, 6))

# =====================================================================
# D.  L16 slide 6 chain (b): four-state chain, two recurrent classes
#     1 absorbing; 2 transient (0.4 self, 0.3 -> 1, 0.3 -> 3); {3,4} recurrent
# =====================================================================
head("D. L16 slide 6(b): four-state chain with two recurrent classes")

B4 = np.array([[1.0, 0.0, 0.0, 0.0],
               [0.3, 0.4, 0.3, 0.0],
               [0.0, 0.0, 0.5, 0.5],
               [0.0, 0.0, 0.5, 0.5]])
rec("two3_rowsums_ok", bool(np.allclose(B4.sum(axis=1), 1)))
r, t, cl = classify(B4)
rec("two_classes", [[i + 1 for i in c] for c in cl])
rec("two_transient", [i + 1 for i in t])
rec("two_period_class34", period(B4, 2))
for n in (1, 2, 5, 10, 30):
    Bn = np.linalg.matrix_power(B4, n)
    rec(f"two_r21_n{n}", Bn[1, 0], "{:.8f}")
    rec(f"two_r23_n{n}", Bn[1, 2], "{:.8f}")
B60 = np.linalg.matrix_power(B4, 60)
rec("two_r11_n60", B60[0, 0], "{:.8f}")
rec("two_r31_n60", B60[2, 0], "{:.8f}")
rec("two_r21_limit", B60[1, 0], "{:.8f}")
rec("two_r21_limit_exact", "0.3/(1-0.4) = 1/2")
# closed form: r21(n) = 0.5 * (1 - 0.4^n) ... check
n = 7
Bn = np.linalg.matrix_power(B4, n)
rec("two_r21_n7_matrix", Bn[1, 0], "{:.10f}")
rec("two_r21_n7_formula", 0.5 * (1 - 0.4 ** n), "{:.10f}")
rec("two_r23p4_n7_matrix", Bn[1, 2] + Bn[1, 3], "{:.10f}")

# =====================================================================
# E.  L17 slide 4: two cycles sharing a node, lengths 6 and 4 -> d = 2
#     0 = shared node; left cycle 0->1->2->3->4->5->0; right cycle 0->6->7->8->0
# =====================================================================
head("E. L17 slide 4: two cycles (lengths 6 and 4) sharing one node")

C9 = np.zeros((9, 9))
C9[0, 1] = 0.5
C9[0, 6] = 0.5
for i in range(1, 5):
    C9[i, i + 1] = 1.0
C9[5, 0] = 1.0
C9[6, 7] = 1.0
C9[7, 8] = 1.0
C9[8, 0] = 1.0
rec("cyc_rowsums_ok", bool(np.allclose(C9.sum(axis=1), 1)))
r, t, cl = classify(C9)
rec("cyc_single_class", [i for i in cl[0]] if len(cl) == 1 else "multiple")
rec("cyc_gcd_of_cycle_lengths", gcd(6, 4))
rec("cyc_period_state0", period(C9, 0))
ret = []
Pn = np.eye(9)
for n in range(1, 15):
    Pn = Pn @ C9
    if Pn[0, 0] > 1e-14:
        ret.append(n)
rec("cyc_return_times_n_le_14", ret)
# the two groups (parity of graph distance from node 0)
dist = {0: 0}
frontier = [0]
while frontier:
    nxt = []
    for u in frontier:
        for v in range(9):
            if C9[u, v] > 0 and v not in dist:
                dist[v] = dist[u] + 1
                nxt.append(v)
    frontier = nxt
rec("cyc_group_even", sorted(k for k, v in dist.items() if v % 2 == 0))
rec("cyc_group_odd", sorted(k for k, v in dist.items() if v % 2 == 1))
rec("cyc_r00_n120", float(np.linalg.matrix_power(C9, 120)[0, 0]), "{:.6f}")
rec("cyc_r00_n121", float(np.linalg.matrix_power(C9, 121)[0, 0]), "{:.6f}")

# =====================================================================
# F.  rec18 P1 — painting fish (n fish), classification
# =====================================================================
head("F. rec18 P1: painting fish chain")

nfish = 4
F = np.zeros((nfish + 1, nfish + 1))
for i in range(nfish + 1):
    F[i, i] = (nfish - i) / nfish
    if i >= 1:
        F[i, i - 1] = i / nfish
rec("fish_n", nfish)
rec("fish_matrix", np.round(F, 6))
rec("fish_rowsums_ok", bool(np.allclose(F.sum(axis=1), 1)))
r, t, cl = classify(F)
rec("fish_recurrent", r)
rec("fish_transient", t)
rec("fish_classes", cl)
rec("fish_p00", F[0, 0])
rec("fish_period_state0", period(F, 0))
# probability of still having i>0 green fish after m days, from state n
for m in (1, 5, 10, 30):
    Fm = np.linalg.matrix_power(F, m)
    rec(f"fish_r_n0_m{m}", Fm[nfish, 0], "{:.8f}")
# naive "independent fish" guess P(all painted by day m) = (1-(1-1/n)^m)^n -- FAILS
m = 10
lhs = np.linalg.matrix_power(F, m)[nfish, 0]
rhs = (1 - (1 - 1 / nfish) ** m) ** nfish
rec("fish_absorb_m10_matrix", lhs, "{:.10f}")
rec("fish_absorb_m10_naive_product", rhs, "{:.10f}")
# correct marginal check: E[# green after m days | start at n] = n(1-1/n)^m
for m in (1, 5, 10):
    Fm = np.linalg.matrix_power(F, m)
    ev = float(sum(i * Fm[nfish, i] for i in range(nfish + 1)))
    rec(f"fish_Egreen_m{m}_matrix", ev, "{:.10f}")
    rec(f"fish_Egreen_m{m}_formula", nfish * (1 - 1 / nfish) ** m, "{:.10f}")

# =====================================================================
# G.  rec18 P3 — six-state chain: classification and where it ends up
#     order of indices: 0 -> s0, 1 -> s1, ..., 5 -> s5
# =====================================================================
head("G. rec18 P3: six-state chain")

S = np.zeros((6, 6))
S[0, 1] = Fraction(1, 3); S[0, 3] = Fraction(1, 3); S[0, 5] = Fraction(1, 3)
S[1, 1] = 1
S[2, 2] = 0.5; S[2, 1] = 0.5
S[3, 3] = 0.25; S[3, 2] = 0.25; S[3, 4] = 0.5
S[4, 4] = 0.5; S[4, 5] = 0.5
S[5, 5] = 1
S = S.astype(float)
S[0, 1] = S[0, 3] = S[0, 5] = 1 / 3
rec("p3_rowsums_ok", bool(np.allclose(S.sum(axis=1), 1)))
r, t, cl = classify(S)
rec("p3_recurrent_states", ["s%d" % i for i in r])
rec("p3_transient_states", ["s%d" % i for i in t])
rec("p3_classes", [["s%d" % i for i in c] for c in cl])
rec("p3_period_s1", period(S, 1))
rec("p3_period_s5", period(S, 5))
Sbig = np.linalg.matrix_power(S, 400)
rec("p3_limit_row_s0", np.round(Sbig[0], 8))
rec("p3_limit_row_s3", np.round(Sbig[3], 8))
rec("p3_limit_row_s2", np.round(Sbig[2], 8))
rec("p3_limit_row_s4", np.round(Sbig[4], 8))
rec("p3_abs_s1_from_s0_exact", "4/9 = %.6f" % (4 / 9))
rec("p3_abs_s5_from_s0_exact", "5/9 = %.6f" % (5 / 9))
rec("p3_abs_s1_from_s3_exact", "1/3 = %.6f" % (1 / 3))
# geometric series: P(leave s3 to s2) = sum_m (1/4)^m (1/4) = (1/4)/(1-1/4)
rec("p3_escape_to_s2_series", float(Fraction(1, 4) / (1 - Fraction(1, 4))), "{:.6f}")
rec("p3_never_enter_s4", float(Fraction(2, 3) + Fraction(1, 3) * Fraction(1, 3)), "{:.6f}")
rec("p3_r03_n", [round(float(np.linalg.matrix_power(S, n)[0, 3]), 8) for n in range(1, 7)])

# =====================================================================
# H.  Widget check: two-state chain P = [[eps, 1-eps], [1, 0]]
# =====================================================================
head("H. widget: periodic vs aperiodic two-state chain")

def two_state(eps):
    return np.array([[eps, 1 - eps], [1.0, 0.0]])


for eps in (0.0, 0.05, 0.2, 0.5):
    Pe = two_state(eps)
    ev = np.sort(np.linalg.eigvals(Pe).real)[::-1]
    pi1 = 1 / (2 - eps)
    seq1 = [round(float(np.linalg.matrix_power(Pe, n)[0, 0]), 6) for n in range(0, 9)]
    seq2 = [round(float(np.linalg.matrix_power(Pe, n)[1, 0]), 6) for n in range(0, 9)]
    tag = str(eps).replace(".", "p")
    rec(f"w_eps{tag}_eigs", np.round(ev, 8))
    rec(f"w_eps{tag}_pi1_formula", pi1, "{:.6f}")
    rec(f"w_eps{tag}_r11_n0to8", seq1)
    rec(f"w_eps{tag}_r21_n0to8", seq2)
    rec(f"w_eps{tag}_period_state1", period(Pe, 0))
    # closed form check r11(n) = pi1 + (1-pi1)(eps-1)^n
    n = 6
    rec(f"w_eps{tag}_r11_n6_closed", pi1 + (1 - pi1) * (eps - 1) ** n, "{:.8f}")
    rec(f"w_eps{tag}_r11_n6_matrix", float(np.linalg.matrix_power(Pe, 6)[0, 0]), "{:.8f}")
    # first n with all entries positive
    rec(f"w_eps{tag}_first_all_positive", first_all_positive(Pe))

# mixing time: smallest n with |r11(n) - pi1| < 0.001
for eps in (0.05, 0.2, 0.5):
    Pe = two_state(eps)
    pi1 = 1 / (2 - eps)
    n = 0
    while abs(float(np.linalg.matrix_power(Pe, n)[0, 0]) - pi1) >= 1e-3:
        n += 1
        if n > 5000:
            break
    rec(f"w_eps{str(eps).replace('.', 'p')}_n_to_1e-3", n)

# =====================================================================
# I.  Aperiodicity test on the warm-up chain restricted to each class
# =====================================================================
head("I. aperiodicity tests (all-entries-positive n)")

C1 = W[np.ix_([2, 3, 4], [2, 3, 4])]  # states 3,4,5
C2 = W[np.ix_([5, 6], [5, 6])]        # states 6,7
rec("warmup_class1_matrix", np.round(C1, 6))
rec("warmup_class2_matrix", np.round(C2, 6))
rec("warmup_class1_first_all_pos_n", first_all_positive(C1))
rec("warmup_class2_first_all_pos_n", first_all_positive(C2))
rec("per3_first_all_pos_n", first_all_positive(A3))
rec("cyc_first_all_pos_n", first_all_positive(C9))

# =====================================================================
# J.  Warm-up chain: class-conditional steady states, and how they combine
# =====================================================================
head("J. class-conditional steady states of the warm-up chain")


def steady(Q):
    k = Q.shape[0]
    M = np.vstack([(Q.T - np.eye(k))[: k - 1], np.ones(k)])
    rhs = np.zeros(k)
    rhs[-1] = 1.0
    return np.linalg.solve(M, rhs)


pi1 = steady(C1)
pi2 = steady(C2)
rec("warmup_class1_steady_345", np.round(pi1, 8))
rec("warmup_class2_steady_67", np.round(pi2, 8))
aR = a[1]  # P(right class | X0 = 2)
rec("warmup_from2_P_rightclass", aR, "{:.6f}")
rec("warmup_from2_P_leftclass", 1 - aR, "{:.6f}")
rec("warmup_from2_predicted_row",
    np.round(np.array([0, 0, *( (1 - aR) * pi1 ), *(aR * pi2), 0, 0]), 6))
rec("warmup_from2_actual_row_n200", np.round(W200[1], 6))

# =====================================================================
# K.  L17 slide 7 two-state example: hypotheses check only (Practice 2.8)
# =====================================================================
head("K. L17 slide 7 two-state chain: hypotheses + pi (used only as a check)")

E2 = np.array([[0.5, 0.5], [0.2, 0.8]])
r, t, cl = classify(E2)
rec("slide7_classes", [[i + 1 for i in c] for c in cl])
rec("slide7_transient", [i + 1 for i in t])
rec("slide7_period", period(E2, 0))
rec("slide7_steady", np.round(steady(E2), 10))
rec("slide7_steady_fractions", "pi = (2/7, 5/7) = (%.6f, %.6f)" % (2 / 7, 5 / 7))
rec("slide7_r_row_n60", np.round(np.linalg.matrix_power(E2, 60), 8))

with open(ROOT / "computes" / "g5_s2.json", "w", encoding="utf-8") as f:
    json.dump(OUT, f, indent=1, default=str)
print(f"\n{len(OUT)} keys -> computes/g5_s2.json")
