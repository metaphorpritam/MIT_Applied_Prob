# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Numbers for G5 section 3 - steady-state probabilities, balance equations,
birth-death chains.

Sources: L17 slides 5-8, L18 slides 2-4, B&T section 7.3 (Examples 7.5, 7.9),
B&T Problems 7.20, 7.24, 7.25.

Run:  uv run computes/g5_s3.py
"""
from __future__ import annotations

import json
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
    if isinstance(val, np.ndarray):
        val = val.tolist()
    OUT[key] = val
    print(f"{key:44s} = {val!r}   {note}")


def stationary(P):
    """Solve pi = pi P, sum pi = 1, by replacing the last balance equation
    with the normalization equation (the balance equations are dependent)."""
    P = np.asarray(P, dtype=float)
    m = P.shape[0]
    A = (P.T - np.eye(m))          # rows: sum_k pi_k p_kj - pi_j = 0
    A[-1, :] = 1.0                 # overwrite last row with normalization
    b = np.zeros(m)
    b[-1] = 1.0
    return np.linalg.solve(A, b)


# =====================================================================
print("=" * 78)
print("A. The two-state chain of L17 slide 7 / L18 slide 3")
print("=" * 78)
# =====================================================================
P2 = np.array([[0.5, 0.5],
               [0.2, 0.8]])
rec("A_rowsums", P2.sum(axis=1))

# balance: pi1 = 0.5 pi1 + 0.2 pi2  ->  0.5 pi1 = 0.2 pi2  ->  pi1 = 0.4 pi2
# normalization: 0.4 pi2 + pi2 = 1 -> pi2 = 1/1.4
pi2_frac = Fraction(1, 1) / Fraction(14, 10)
pi1_frac = Fraction(4, 10) * pi2_frac
rec("A_pi1_exact_num", pi1_frac.numerator)
rec("A_pi1_exact_den", pi1_frac.denominator)
rec("A_pi2_exact_num", pi2_frac.numerator)
rec("A_pi2_exact_den", pi2_frac.denominator)
rec("A_pi1", float(pi1_frac))
rec("A_pi2", float(pi2_frac))
pi_lin = stationary(P2)
rec("A_pi_linalg", pi_lin, "numpy linear solve, must match 2/7, 5/7")
rec("A_pi_maxerr_vs_exact", float(np.max(np.abs(pi_lin - np.array([2 / 7, 5 / 7])))))
rec("A_check_balance_residual", float(np.max(np.abs(pi_lin @ P2 - pi_lin))))

# eigenvalues: 1 and 0.3 (trace = 1.3)
ev = np.linalg.eigvals(P2)
rec("A_eigenvalues", np.sort(ev.real)[::-1])
rec("A_second_eigenvalue", float(np.sort(ev.real)[0]), "= p11+p22-1 = 0.3")

# n-step transition matrices
rows = []
for n in [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20]:
    R = np.linalg.matrix_power(P2, n)
    rows.append({"n": n, "r11": R[0, 0], "r12": R[0, 1],
                 "r21": R[1, 0], "r22": R[1, 1],
                 "err11": abs(R[0, 0] - 2 / 7), "err21": abs(R[1, 0] - 2 / 7)})
    print(f"   n={n:3d}  r11={R[0,0]:.9f} r12={R[0,1]:.9f} "
          f"r21={R[1,0]:.9f} r22={R[1,1]:.9f}  |r11-2/7|={abs(R[0,0]-2/7):.3e}")
OUT["A_nstep_table"] = rows
rec("A_r11_n1", float(np.linalg.matrix_power(P2, 1)[0, 0]))
rec("A_r11_n2", float(np.linalg.matrix_power(P2, 2)[0, 0]))
rec("A_r11_n3", float(np.linalg.matrix_power(P2, 3)[0, 0]))
rec("A_r11_n4", float(np.linalg.matrix_power(P2, 4)[0, 0]))
rec("A_r11_n6", float(np.linalg.matrix_power(P2, 6)[0, 0]))
rec("A_r11_n10", float(np.linalg.matrix_power(P2, 10)[0, 0]))

# closed form r11(n) = 2/7 + (5/7) 0.3^n, r21(n) = 2/7 - (2/7) 0.3^n
cf_err = max(abs(np.linalg.matrix_power(P2, n)[0, 0] - (2 / 7 + (5 / 7) * 0.3 ** n))
             for n in range(0, 25))
rec("A_closedform_r11_maxerr", float(cf_err))
cf_err2 = max(abs(np.linalg.matrix_power(P2, n)[1, 0] - (2 / 7 - (2 / 7) * 0.3 ** n))
              for n in range(0, 25))
rec("A_closedform_r21_maxerr", float(cf_err2))
# how long until within 1e-3 of the limit, starting from state 1
n_eps = next(n for n in range(200)
             if abs(np.linalg.matrix_power(P2, n)[0, 0] - 2 / 7) < 1e-3)
rec("A_n_within_1e3", n_eps)

# --- L18 slide 3 unsolved examples, X0 = 1 -------------------------------
r11_99 = np.linalg.matrix_power(P2, 99)[0, 0]
r11_100 = np.linalg.matrix_power(P2, 100)[0, 0]
rec("A_r11_99", float(r11_99))
rec("A_r11_100", float(r11_100))
rec("A_r11_99_minus_pi1", float(r11_99 - 2 / 7))
rec("A_slide3_q1", float(P2[0, 0] * r11_99), "P(X1=1, X100=1 | X0=1) = p11 * r11(99)")
rec("A_slide3_q1_approx", float(0.5 * 2 / 7), "= 1/7")
rec("A_slide3_q2", float(r11_100 * P2[0, 1]), "P(X100=1, X101=2 | X0=1) = r11(100) p12")
rec("A_slide3_q2_approx", float((2 / 7) * 0.5), "= 1/7")
rec("A_one_seventh", 1 / 7)
rec("A_theory_gap_99", float((5 / 7) * 0.3 ** 99),
    "exact size of r11(99)-pi1 = (5/7)(0.3)^99")
rec("A_theory_gap_99_exp", int(np.floor(np.log10((5 / 7) * 0.3 ** 99))))
# transition-frequency reading of the second answer
rec("A_freq_1to2", float(pi_lin[0] * P2[0, 1]), "pi_1 p_12 = long-run frequency of 1->2")

# simulation check of the frequency interpretation
rng = np.random.default_rng(20101109)
N = 400_000
x = 0
visits = np.zeros(2)
trans12 = 0
for _ in range(N):
    visits[x] += 1
    u = rng.random()
    nx = 0 if u < P2[x, 0] else 1
    if x == 0 and nx == 1:
        trans12 += 1
    x = nx
rec("A_sim_frac_state1", float(visits[0] / N))
rec("A_sim_frac_state2", float(visits[1] / N))
rec("A_sim_freq_1to2", float(trans12 / N))
rec("A_sim_N", N)

# mean recurrence time (forward reference to section 4)
rec("A_t1_star", float(1 / pi_lin[0]), "1/pi_1")
rec("A_t2_star", float(1 / pi_lin[1]), "1/pi_2")


# =====================================================================
print()
print("=" * 78)
print("B. B&T Example 7.5 - the other two-state chain (0.8/0.2/0.6/0.4)")
print("=" * 78)
# =====================================================================
PB = np.array([[0.8, 0.2],
               [0.6, 0.4]])
piB = stationary(PB)
rec("B_pi", piB, "expect 0.75, 0.25")
rec("B_check", float(np.max(np.abs(piB @ PB - piB))))
rec("B_ratio_pi1_over_pi2", float(piB[0] / piB[1]), "= 3")


# =====================================================================
print()
print("=" * 78)
print("C. A three-state chain - the general linear solve (authored example)")
print("=" * 78)
# =====================================================================
P3 = np.array([[0.7, 0.2, 0.1],
               [0.3, 0.4, 0.3],
               [0.0, 0.5, 0.5]])
rec("C_rowsums", P3.sum(axis=1))
pi3 = stationary(P3)
rec("C_pi_linalg", pi3)
rec("C_pi_exact", [5 / 14, 5 / 14, 4 / 14])
rec("C_maxerr", float(np.max(np.abs(pi3 - np.array([5 / 14, 5 / 14, 4 / 14])))))
rec("C_pi1_dec", float(pi3[0]))
rec("C_pi2_dec", float(pi3[1]))
rec("C_pi3_dec", float(pi3[2]))
rec("C_check_balance_residual", float(np.max(np.abs(pi3 @ P3 - pi3))))
# convergence: r_ij(n) for a couple of n
for n in [1, 5, 10, 20, 40]:
    R = np.linalg.matrix_power(P3, n)
    print(f"   n={n:3d}  row1 = {np.round(R[0], 6)}   row3 = {np.round(R[2], 6)}")
rec("C_r_n20_rows", np.linalg.matrix_power(P3, 20))
rec("C_r_n40_row1", np.linalg.matrix_power(P3, 40)[0])
ev3 = np.sort(np.abs(np.linalg.eigvals(P3)))[::-1]
rec("C_eig_abs", ev3)
rec("C_second_eig_abs", float(ev3[1]))
# demonstration that the three balance equations are dependent:
# summing all three gives 0 = 0 (B&T Problem 24)
A3 = (P3.T - np.eye(3))
rec("C_sum_of_balance_rows", A3.sum(axis=0), "each column sums to 0 -> equations dependent")
rec("C_rank_of_balance_system", int(np.linalg.matrix_rank(A3)), "3 unknowns, rank 2")


# =====================================================================
print()
print("=" * 78)
print("D. Birth-death queue with constant p, q (L17 slide 8; B&T Example 7.9)")
print("=" * 78)
# =====================================================================
def bd_matrix(p, q, m):
    """Birth-death chain on states 0..m: up prob p, down prob q, rest self-loop."""
    P = np.zeros((m + 1, m + 1))
    for i in range(m + 1):
        up = p if i < m else 0.0
        dn = q if i > 0 else 0.0
        P[i, i] = 1.0 - up - dn
        if i < m:
            P[i, i + 1] = up
        if i > 0:
            P[i, i - 1] = dn
    return P


def bd_pi_formula(p, q, m):
    rho = p / q
    if abs(rho - 1.0) < 1e-14:
        return np.full(m + 1, 1.0 / (m + 1)), rho
    pi0 = (1 - rho) / (1 - rho ** (m + 1))
    return pi0 * rho ** np.arange(m + 1), rho


cases = [("rho_half", 0.2, 0.4, 10),
         ("rho_one", 0.3, 0.3, 10),
         ("rho_1p5", 0.45, 0.30, 10),
         ("rho_0p8", 0.24, 0.30, 10)]
D = {}
for name, p, q, m in cases:
    P = bd_matrix(p, q, m)
    pil = stationary(P)
    pif, rho = bd_pi_formula(p, q, m)
    EX = float(np.dot(np.arange(m + 1), pil))
    D[name] = {"p": p, "q": q, "m": m, "rho": rho,
               "pi_linalg": pil.tolist(), "pi_formula": pif.tolist(),
               "maxerr": float(np.max(np.abs(pil - pif))),
               "pi0": float(pil[0]), "pim": float(pil[-1]), "EX": EX}
    print(f"   {name:9s} p={p} q={q} m={m}  rho={rho:.6g}  pi0={pil[0]:.6f} "
          f"pim={pil[-1]:.6f}  E[X]={EX:.6f}  |linalg-formula|max={D[name]['maxerr']:.2e}")
    # local balance check
    lb = max(abs(pil[i] * p - pil[i + 1] * q) for i in range(m))
    D[name]["local_balance_maxres"] = float(lb)
    print(f"              local-balance max residual |pi_i p - pi_{{i+1}} q| = {lb:.2e}")
OUT["D_cases"] = D
rec("D_rho_half_EX", D["rho_half"]["EX"])
rec("D_rho_half_pi0", D["rho_half"]["pi0"])
rec("D_rho_one_pi0", D["rho_one"]["pi0"], "= 1/(m+1) = 1/11")
rec("D_rho_one_EX", D["rho_one"]["EX"], "= m/2 = 5")
rec("D_rho_1p5_pi0", D["rho_1p5"]["pi0"])
rec("D_rho_1p5_pim", D["rho_1p5"]["pim"])
rec("D_rho_1p5_EX", D["rho_1p5"]["EX"])
rec("D_rho_0p8_pi0", D["rho_0p8"]["pi0"])
rec("D_rho_0p8_EX", D["rho_0p8"]["EX"])

# finite-m closed form for E[X] cross-check, rho != 1
def bd_EX_closed(rho, m):
    if abs(rho - 1) < 1e-14:
        return m / 2
    return rho / (1 - rho) - (m + 1) * rho ** (m + 1) / (1 - rho ** (m + 1))


for name in D:
    rho, m = D[name]["rho"], D[name]["m"]
    ecl = bd_EX_closed(rho, m)
    print(f"   {name:9s} E[X] closed form = {ecl:.9f}  vs sum = {D[name]['EX']:.9f}  "
          f"diff = {abs(ecl-D[name]['EX']):.2e}")
    D[name]["EX_closed"] = float(ecl)
rec("D_EX_closed_maxdiff",
    float(max(abs(D[n]["EX_closed"] - D[n]["EX"]) for n in D)))

# infinite buffer, rho < 1: pi_i = (1-rho) rho^i, E[X] = rho/(1-rho)
print("\n   Infinite buffer (m -> infinity), rho < 1:")
inf_tab = []
for rho in [0.2, 0.5, 0.8, 0.9, 0.95, 0.99]:
    EX = rho / (1 - rho)
    # numeric check: truncate at m large and renormalize
    mbig = 4000
    pi = (1 - rho) * rho ** np.arange(mbig + 1)
    EXnum = float(np.dot(np.arange(mbig + 1), pi))
    inf_tab.append({"rho": rho, "pi0": 1 - rho, "EX": EX, "EX_numeric": EXnum})
    print(f"      rho={rho:5.2f}  pi0=1-rho={1-rho:6.3f}  E[X]=rho/(1-rho)={EX:9.4f}  "
          f"(numeric {EXnum:9.4f})")
OUT["D_infinite_table"] = inf_tab
rec("D_inf_EX_maxerr", float(max(abs(t["EX"] - t["EX_numeric"]) for t in inf_tab)))
# how far does a finite buffer have to go before it looks infinite?
rho = 0.5
for m in [3, 5, 10, 20, 40]:
    pif, _ = bd_pi_formula(0.2, 0.4, m)
    print(f"      rho=0.5, m={m:3d}: pi0={pif[0]:.9f}  (limit 0.5), "
          f"E[X]={np.dot(np.arange(m+1),pif):.9f} (limit 1.0)")
rec("D_m10_rho_half_pi0", float(bd_pi_formula(0.2, 0.4, 10)[0][0]))
rec("D_m10_rho_half_EX", float(np.dot(np.arange(11), bd_pi_formula(0.2, 0.4, 10)[0])))

# rho > 1 : every fixed state's probability -> 0 as m grows
print("\n   rho = 1.5 > 1: pi_0 as the buffer grows")
grow = []
for m in [5, 10, 20, 40, 80]:
    pif, _ = bd_pi_formula(0.45, 0.30, m)
    grow.append({"m": m, "pi0": float(pif[0]), "pim": float(pif[-1]),
                 "EX": float(np.dot(np.arange(m + 1), pif))})
    print(f"      m={m:3d}: pi0={pif[0]:.3e}  pi_m={pif[-1]:.6f}  "
          f"E[X]={np.dot(np.arange(m+1),pif):.4f}")
OUT["D_overload_table"] = grow

# widget cross-check points (p, q, m) -> pi0, pim, E[X]
wchk = []
for (p, q, m) in [(0.3, 0.5, 12), (0.4, 0.4, 12), (0.5, 0.3, 12), (0.45, 0.5, 25)]:
    pif, rho = bd_pi_formula(p, q, m)
    wchk.append({"p": p, "q": q, "m": m, "rho": rho, "pi0": float(pif[0]),
                 "pim": float(pif[-1]),
                 "EX": float(np.dot(np.arange(m + 1), pif))})
    print(f"   widget check p={p} q={q} m={m}: rho={rho:.4f} pi0={pif[0]:.6f} "
          f"pi_m={pif[-1]:.6f} E[X]={wchk[-1]['EX']:.6f}")
OUT["D_widget_checks"] = wchk


# =====================================================================
print()
print("=" * 78)
print("E. The phone company / Erlang B chain (L18 slide 4)")
print("=" * 78)
# =====================================================================
def erlang_pi(a, B):
    """pi_i proportional to a^i / i!, i = 0..B, with a = lambda/mu."""
    terms = np.array([a ** i / np.math.factorial(i) for i in range(B + 1)], dtype=float) \
        if False else np.array([np.exp(i * np.log(a) - sum(np.log(k) for k in range(1, i + 1)))
                                for i in range(B + 1)])
    return terms / terms.sum()


def erlang_pi_exact(a, B):
    t = [Fraction(1)]
    for i in range(1, B + 1):
        t.append(t[-1] * Fraction(a).limit_denominator(10 ** 6) / i)
    s = sum(t)
    return [x / s for x in t]


# Slide-4 chain, discretized: up-rate lambda*delta from every state, down-rate i*mu*delta
lam, mu, B, delta = 30.0, 10.0, 4, 1e-4   # lambda = 30/min, mean call 1/mu = 0.1 min
a = lam / mu
rec("E_lambda", lam)
rec("E_mu", mu)
rec("E_a_offered_load", a, "a = lambda/mu, in erlangs")
rec("E_B_lines", B)

Pph = np.zeros((B + 1, B + 1))
for i in range(B + 1):
    up = lam * delta if i < B else 0.0
    dn = i * mu * delta
    Pph[i, i] = 1 - up - dn
    if i < B:
        Pph[i, i + 1] = up
    if i > 0:
        Pph[i, i - 1] = dn
rec("E_rowsums", Pph.sum(axis=1))
piph = stationary(Pph)
piex = erlang_pi(a, B)
rec("E_pi_linalg", piph)
rec("E_pi_formula", piex)
rec("E_maxerr", float(np.max(np.abs(piph - piex))), "delta cancels out exactly")
rec("E_pi0", float(piex[0]))
rec("E_pi1", float(piex[1]))
rec("E_pi2", float(piex[2]))
rec("E_pi3", float(piex[3]))
rec("E_pi4_blocking", float(piex[4]), "Erlang B: probability an arriving call is blocked")
ex = erlang_pi_exact(3.0, 4)
rec("E_pi_exact_fracs", [f"{x.numerator}/{x.denominator}" for x in ex])
rec("E_blocking_exact_frac", f"{ex[-1].numerator}/{ex[-1].denominator}")
rec("E_expected_lines_busy", float(np.dot(np.arange(B + 1), piex)))
rec("E_carried_load", float(a * (1 - piex[-1])), "a(1-P_block) = mean number of busy lines")
rec("E_carried_check", float(abs(a * (1 - piex[-1]) - np.dot(np.arange(B + 1), piex))))

print("\n   Erlang-B blocking probability vs number of lines, a = 3 erlangs:")
etab = []
for Bx in range(1, 13):
    pp = erlang_pi(a, Bx)
    etab.append({"B": Bx, "block": float(pp[-1])})
    print(f"      B={Bx:2d}  P(block) = {pp[-1]:.6f}")
OUT["E_blocking_vs_B"] = etab
rec("E_B_for_1pct", next(t["B"] for t in etab if t["block"] < 0.01))
rec("E_block_B8", next(t["block"] for t in etab if t["B"] == 8))
rec("E_block_B9", next(t["block"] for t in etab if t["B"] == 9))

# a second load for the practice question
a2, B2 = 5.0, 8
p2 = erlang_pi(a2, B2)
rec("E2_a", a2)
rec("E2_B", B2)
rec("E2_blocking", float(p2[-1]))
rec("E2_pi0", float(p2[0]))
rec("E2_mean_busy", float(np.dot(np.arange(B2 + 1), p2)))
etab2 = []
for Bx in range(5, 16):
    etab2.append({"B": Bx, "block": float(erlang_pi(a2, Bx)[-1])})
OUT["E2_blocking_vs_B"] = etab2
rec("E2_B_for_2pct", next(t["B"] for t in etab2 if t["block"] < 0.02))
rec("E2_block_that_B", next(t["block"] for t in etab2 if t["block"] < 0.02))

# recursive Erlang-B check:  E(B) = a E(B-1) / (B + a E(B-1)),  E(0) = 1
EB = 1.0
for Bx in range(1, B + 1):
    EB = a * EB / (Bx + a * EB)
rec("E_recursive_blocking", EB)
rec("E_recursive_vs_direct", float(abs(EB - piex[-1])))


# =====================================================================
print()
print("=" * 78)
print("F. Practice-question numbers")
print("=" * 78)
# =====================================================================
# P3.1 - three-state weather chain
Pw = np.array([[0.6, 0.3, 0.1],
               [0.2, 0.5, 0.3],
               [0.1, 0.4, 0.5]])
rec("F_P31_rowsums", Pw.sum(axis=1))
piw = stationary(Pw)
rec("F_P31_pi", piw)
rec("F_P31_pi_frac", [str(Fraction(v).limit_denominator(2000)) for v in piw])
rec("F_P31_residual", float(np.max(np.abs(piw @ Pw - piw))))
rec("F_P31_freq_sun_to_rain", float(piw[0] * Pw[0, 2]))
rec("F_P31_long_run_rain_days_per_100", float(100 * piw[2]))

# P3.2 - frequency interpretation on the two-state chain
rec("F_P32_freq_2to1", float(pi_lin[1] * P2[1, 0]))
rec("F_P32_freq_1to2", float(pi_lin[0] * P2[0, 1]))
rec("F_P32_equal", float(abs(pi_lin[1] * P2[1, 0] - pi_lin[0] * P2[0, 1])))

# P3.3 - birth-death with m = 4, p = 0.3, q = 0.5
pif43, rho43 = bd_pi_formula(0.3, 0.5, 4)
rec("F_P33_rho", rho43)
rec("F_P33_pi", pif43)
rec("F_P33_pi0", float(pif43[0]))
rec("F_P33_pi4", float(pif43[-1]))
rec("F_P33_EX", float(np.dot(np.arange(5), pif43)))
rec("F_P33_pi0_exact", str(Fraction(float(pif43[0])).limit_denominator(10 ** 6)))
# 1 + r + r^2 + r^3 + r^4 with r = 0.6
r = Fraction(3, 5)
S = sum(r ** k for k in range(5))
rec("F_P33_geom_sum_frac", f"{S.numerator}/{S.denominator}")
rec("F_P33_pi0_frac", f"{(1/S).numerator}/{(1/S).denominator}")

# P3.4 - infinite queue, target E[X]
for target in [1.0, 4.0, 9.0]:
    rho_t = target / (1 + target)
    print(f"   E[X] = {target} requires rho = {rho_t:.6f}")
rec("F_P34_rho_for_EX9", 9 / 10)
rec("F_P34_rho_for_EX4", 4 / 5)
# P(X >= 5) under geometric with rho = 0.9
rec("F_P34_tail_ge5_rho09", float(0.9 ** 5))
rec("F_P34_tail_ge5_rho05", float(0.5 ** 5))

# P3.5 - Erlang B sizing
rec("F_P35_a", 2.0)
p35 = erlang_pi(2.0, 5)
rec("F_P35_pi", p35)
rec("F_P35_blocking_B5", float(p35[-1]))
rec("F_P35_blocking_B4", float(erlang_pi(2.0, 4)[-1]))
rec("F_P35_blocking_B6", float(erlang_pi(2.0, 6)[-1]))

# P3.6 - call center two-state chain with state and transition costs
Pc = np.array([[0.6, 0.4], [0.1, 0.9]])
pic = stationary(Pc)
rec("F_P36_pi", pic, "idle, busy")
rec("F_P36_revenue", float(3 * pic[1]))
rec("F_P36_setup_cost", float(1 * pic[0] * Pc[0, 1]))
rec("F_P36_profit", float(3 * pic[1] - pic[0] * Pc[0, 1]))

# P3.7 - three-state birth-death solved by local balance
p0_, p1_, q1_, q2_ = 0.5, 0.4, 0.3, 0.6
u = np.array([1.0, p0_ / q1_, (p0_ / q1_) * (p1_ / q2_)])
pi37 = u / u.sum()
rec("F_P37_unnormalized", u)
rec("F_P37_pi", pi37)
rec("F_P37_pi_frac", [str(Fraction(v).limit_denominator(200)) for v in pi37])
P37 = np.array([[1 - p0_, p0_, 0.0],
                [q1_, 1 - p0_ - q1_ + (p0_ - p1_), p1_],
                [0.0, q2_, 1 - q2_]])
P37 = np.array([[0.5, 0.5, 0.0],
                [0.3, 0.3, 0.4],
                [0.0, 0.6, 0.4]])
rec("F_P37_rowsums", P37.sum(axis=1))
rec("F_P37_pi_linalg", stationary(P37))
rec("F_P37_maxerr", float(np.max(np.abs(stationary(P37) - pi37))))

# P3.8 / P3.9 geometric tails
rec("F_P38_tail_ge5_rho06", float(0.6 ** 5))
rec("F_P39_tail_ge5_rho08", float(0.8 ** 5))
rec("F_P38_inf_EX_rho06", float(0.6 / 0.4))
rec("C_hours_down_per_day", float(24 * 2 / 7))

# Erlang-B intermediate sums quoted in the prose
w3 = np.array([3.0 ** i / np.prod(np.arange(1, i + 1)) if i else 1.0 for i in range(5)])
rec("E_weights_a3_B4", w3)
rec("E_weightsum_a3_B4", float(w3.sum()))
rec("E_weights_a3_B4_times8", (w3 * 8))
w5 = np.array([5.0 ** i / np.prod(np.arange(1, i + 1)) if i else 1.0 for i in range(9)])
rec("E2_weights_a5_B8", w5)
rec("E2_weightsum_a5_B8", float(w5.sum()))

# =====================================================================
outp = ROOT / "computes" / "g5_s3.json"
outp.write_text(json.dumps(OUT, indent=1), encoding="utf-8")
print(f"\nwrote {outp}")
