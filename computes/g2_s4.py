# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""G2 section 4 (Joint PMFs and multiple random variables) — every number in the fragment.

Run:  uv run computes/g2_s4.py
Writes computes/g2_s4.json
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict = {}


def show(key, val, note=""):
    if isinstance(val, F):
        R[key] = [val.numerator, val.denominator]
        txt = f"{val}  = {float(val):.6f}"
    elif isinstance(val, float):
        R[key] = val
        txt = f"{val:.6f}"
    else:
        R[key] = val
        txt = str(val)
    print(f"{key:46s} = {txt}   {note}")


def fs(x: F) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def mean(pmf: dict) -> F:
    return sum(F(v) * k for k, v in pmf.items())


def var(pmf: dict) -> F:
    m = mean(pmf)
    return sum(F(v) * (F(k) - m) ** 2 for k, v in pmf.items())


def norm(d: dict) -> dict:
    s = sum(d.values())
    return {k: v / s for k, v in d.items() if v != 0}


# ================================================================= 4.1-4.4  L07 slide 3 grid
print("\n=== L07 slide 3 : the joint PMF grid (denominator 20) ===")
# joint[(x,y)] = numerator/20
num = {
    (1, 4): 1, (2, 4): 2, (3, 4): 2, (4, 4): 0,
    (1, 3): 2, (2, 3): 4, (3, 3): 1, (4, 3): 2,
    (1, 2): 0, (2, 2): 1, (3, 2): 3, (4, 2): 1,
    (1, 1): 0, (2, 1): 1, (3, 1): 0, (4, 1): 0,
}
joint = {k: F(v, 20) for k, v in num.items()}
show("grid_total", sum(joint.values()), "must be 1")

pX = {x: sum(joint[(x, y)] for y in range(1, 5)) for x in range(1, 5)}
pY = {y: sum(joint[(x, y)] for x in range(1, 5)) for y in range(1, 5)}
for x in range(1, 5):
    show(f"pX_{x}", pX[x])
for y in range(1, 5):
    show(f"pY_{y}", pY[y])
show("pX_sum", sum(pX.values()))
show("pY_sum", sum(pY.values()))

show("EX", mean(pX))
show("EX_float", float(mean(pX)))
show("EY", mean(pY))
show("EY_float", float(mean(pY)))
show("varX", var(pX))
show("varX_float", float(var(pX)))
show("varY", var(pY))
show("varY_float", float(var(pY)))
EXY = sum(F(x) * F(y) * p for (x, y), p in joint.items())
show("EXY", EXY)
show("EXY_float", float(EXY))
show("EX_times_EY", mean(pX) * mean(pY))
show("cov_XY", EXY - mean(pX) * mean(pY))
show("cov_XY_float", float(EXY - mean(pX) * mean(pY)))

# independence check on the full grid
bad = [(x, y, fs(joint[(x, y)]), fs(pX[x] * pY[y]))
       for (x, y) in joint if joint[(x, y)] != pX[x] * pY[y]]
show("indep_violations_count", len(bad))
show("indep_first_violation", bad[0] if bad else None,
     "(x, y, p_XY, pX*pY)")
show("indep_check_1_1_joint", joint[(1, 1)])
show("indep_check_1_1_product", pX[1] * pY[1])
show("indep_check_2_4_joint", joint[(2, 4)])
show("indep_check_2_4_product", pX[2] * pY[4])

# conditional PMFs of X given Y=y
print("\n--- conditional PMFs p_{X|Y}(x|y) ---")
condX_given_Y = {}
for y in range(1, 5):
    row = {x: joint[(x, y)] / pY[y] for x in range(1, 5)}
    condX_given_Y[y] = row
    for x in range(1, 5):
        show(f"pXgY_{x}_given_{y}", row[x])
    show(f"E_X_given_Y{y}", mean(row))
    show(f"E_X_given_Y{y}_float", float(mean(row)))
    show(f"var_X_given_Y{y}", var(row))
    show(f"var_X_given_Y{y}_float", float(var(row)))

# conditional PMF of Y given X=2 (used in prose)
print("\n--- p_{Y|X}(y|2) ---")
row2 = {y: joint[(2, y)] / pX[2] for y in range(1, 5)}
for y in range(1, 5):
    show(f"pYgX_{y}_given_2", row2[y])
show("E_Y_given_X2", mean(row2))
show("E_Y_given_X2_float", float(mean(row2)))

# total expectation check
tot = sum(pY[y] * mean(condX_given_Y[y]) for y in range(1, 5))
show("total_expectation_check_EX", tot)

# ---- conditioning on B = {X<=2, Y>=3}
print("\n--- conditioning on B = {X<=2 and Y>=3} (L07 slide 3) ---")
Bcells = [(x, y) for (x, y) in joint if x <= 2 and y >= 3]
PB = sum(joint[c] for c in sorted(Bcells))
show("P_B", PB)
show("P_B_float", float(PB))
condB = {c: joint[c] / PB for c in sorted(Bcells)}
for c in sorted(condB):
    show(f"pB_joint_{c[0]}_{c[1]}", condB[c])
pXB = {x: sum(condB[(x, y)] for y in (3, 4)) for x in (1, 2)}
pYB = {y: sum(condB[(x, y)] for x in (1, 2)) for y in (3, 4)}
for x in (1, 2):
    show(f"pXgB_{x}", pXB[x])
for y in (3, 4):
    show(f"pYgB_{y}", pYB[y])
show("E_X_given_B", mean(pXB))
show("E_X_given_B_float", float(mean(pXB)))
show("var_X_given_B", var(pXB))
show("var_X_given_B_float", float(var(pXB)))
show("E_Y_given_B", mean(pYB))
show("var_Y_given_B", var(pYB))
condB_indep = all(condB[(x, y)] == pXB[x] * pYB[y] for x in (1, 2) for y in (3, 4))
show("cond_on_B_independent", condB_indep)
for x in (1, 2):
    for y in (3, 4):
        show(f"condB_prod_{x}_{y}", pXB[x] * pYB[y])
EXY_B = sum(F(x) * F(y) * p for (x, y), p in condB.items())
show("E_XY_given_B", EXY_B)
show("E_XY_given_B_float", float(EXY_B))
show("E_X_given_B_times_E_Y_given_B", mean(pXB) * mean(pYB))

# ---- widget verification table: conditional PMF of X under each conditioning event
print("\n--- widget table: conditional PMF of X under each event ---")
widget = {}


def add_event(name, cells):
    tot = sum(joint[c] for c in cells)
    d = {x: sum(joint[(xx, yy)] for (xx, yy) in cells if xx == x) / tot for x in range(1, 5)}
    m, v = mean(d), var(d)
    widget[name] = {
        "P_event": [tot.numerator, tot.denominator],
        "pmf": {str(x): [d[x].numerator, d[x].denominator] for x in range(1, 5)},
        "E": float(m), "var": float(v),
        "E_frac": fs(m), "var_frac": fs(v),
    }
    print(f"{name:14s} P={fs(tot):6s} pmf=" +
          " ".join(fs(d[x]) for x in range(1, 5)) +
          f"  E={fs(m)}={float(m):.4f}  var={fs(v)}={float(v):.4f}")


allcells = sorted(joint)
add_event("none", [c for c in allcells if joint[c] > 0])
for y in range(1, 5):
    add_event(f"Y={y}", [c for c in allcells if c[1] == y and joint[c] > 0])
add_event("X<=2,Y>=3", [c for c in allcells if c[0] <= 2 and c[1] >= 3 and joint[c] > 0])
add_event("X<=2", [c for c in allcells if c[0] <= 2 and joint[c] > 0])
R["widget"] = widget

# ================================================================= 4.6 variance of sums
print("\n=== L07 slide 5 : variance examples (grid X as the concrete case) ===")
vX = var(pX)
show("slide5_varX_used", vX)
show("slide5_var_2X", 4 * vX, "var(X+Y) when Y=X, i.e. var(2X)=4var(X)")
show("slide5_var_2X_float", float(4 * vX))
show("slide5_var_zero", F(0), "var(X+Y) when Y=-X: var(0)=0")
# Z = X - 3Y with X,Y independent copies
show("slide5_var_X_minus_3Y_symbolic", "var(X)+9var(Y)")
vY = var(pY)
show("slide5_indep_example_varX", vX)
show("slide5_indep_example_varY", vY)
show("slide5_var_X_minus_3Y_num", vX + 9 * vY)
show("slide5_var_X_minus_3Y_num_float", float(vX + 9 * vY))

# ================================================================= 4.7 binomial via indicators
print("\n=== L07 slide 6 : binomial mean/variance via indicators ===")
n, p = 10, F(3, 10)
show("binom_n", n)
show("binom_p", p)
show("binom_E_Xi", p)
show("binom_var_Xi", p * (1 - p))
show("binom_var_Xi_float", float(p * (1 - p)))
show("binom_EX_formula", n * p)
show("binom_EX_float", float(n * p))
show("binom_varX_formula", n * p * (1 - p))
show("binom_varX_float", float(n * p * (1 - p)))
brute_E = sum(F(k) * comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1))
brute_E2 = sum(F(k) ** 2 * comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1))
show("binom_brute_EX", brute_E, "brute-force sum agrees with np")
show("binom_brute_varX", brute_E2 - brute_E ** 2)
show("binom_pmf", [float(comb(n, k) * p ** k * (1 - p) ** (n - k)) for k in range(n + 1)])

# ================================================================= 4.8a rec06 P1
print("\n=== rec06 P1 : four-sided die sets the number of fair coin flips ===")
pN = {n_: F(1, 4) for n_ in range(4)}
jNK = {}
for n_ in range(4):
    for k in range(n_ + 1):
        jNK[(n_, k)] = F(1, 4) * F(comb(n_, k), 2 ** n_)
for n_ in range(4):
    for k in range(4):
        show(f"rec06p1_pNK_{n_}_{k}", jNK.get((n_, k), F(0)))
show("rec06p1_total", sum(jNK.values()))
pK = {k: sum(jNK.get((n_, k), F(0)) for n_ in range(4)) for k in range(4)}
for k in range(4):
    show(f"rec06p1_pK_{k}", pK[k])
show("rec06p1_pK_sum", sum(pK.values()))
cKgN2 = {k: jNK[(2, k)] / pN[2] for k in range(3)}
for k in range(3):
    show(f"rec06p1_pKgN_{k}_given2", cKgN2[k])
cNgK2 = {n_: jNK.get((n_, 2), F(0)) / pK[2] for n_ in (2, 3)}
for n_ in (2, 3):
    show(f"rec06p1_pNgK_{n_}_given2", cNgK2[n_])
show("rec06p1_E_K_given_N2", mean(cKgN2))
show("rec06p1_E_N_given_K2", mean(cNgK2))
show("rec06p1_E_N_given_K2_float", float(mean(cNgK2)))
show("rec06p1_E_N", mean(pN))
show("rec06p1_E_K", mean(pK))
show("rec06p1_E_K_float", float(mean(pK)))
show("rec06p1_E_K_total_exp", sum(pN[n_] * F(n_, 2) for n_ in range(4)),
     "sum_n p_N(n) E[K|N=n] = sum n/2 * 1/4")
show("rec06p1_var_K", var(pK))
show("rec06p1_var_K_float", float(var(pK)))
show("rec06p1_var_N", var(pN))
indep_NK = all(jNK.get((n_, k), F(0)) == pN[n_] * pK[k] for n_ in range(4) for k in range(4))
show("rec06p1_N_K_independent", indep_NK)
show("rec06p1_pNK_0_1", jNK.get((0, 1), F(0)))
show("rec06p1_pN0_times_pK1", pN[0] * pK[1])

# ================================================================= 4.8b rec06 P2
print("\n=== rec06 P2 : eight equally likely points ===")
pts = [(0, 3), (4, 3), (2, 2), (4, 2), (0, 1), (2, 1), (4, 1), (4, 0)]
w = F(1, 8)
jXY = {q: w for q in pts}
pXs = {}
for (x, y) in pts:
    pXs[x] = pXs.get(x, F(0)) + w
pYs = {}
for (x, y) in pts:
    pYs[y] = pYs.get(y, F(0)) + w
for x in sorted(pXs):
    show(f"rec06p2_pX_{x}", pXs[x])
for y in sorted(pYs):
    show(f"rec06p2_pY_{y}", pYs[y])
# (a) E[Y|X=x]
for x in sorted(pXs):
    d = {y: w / pXs[x] for (xx, y) in pts if xx == x}
    show(f"rec06p2_E_Y_given_X{x}", mean(d))
    show(f"rec06p2_var_Y_given_X{x}", var(d))
# (b) var(X|Y=y)
for y in sorted(pYs):
    d = {}
    for (xx, yy) in pts:
        if yy == y:
            d[xx] = d.get(xx, F(0)) + w
    d = {k: v / pYs[y] for k, v in d.items()}
    show(f"rec06p2_E_X_given_Y{y}", mean(d))
    show(f"rec06p2_var_X_given_Y{y}", var(d))
    show(f"rec06p2_var_X_given_Y{y}_float", float(var(d)))
# (c) R = min(X,Y)
pR = {}
for (x, y) in pts:
    r = min(x, y)
    pR[r] = pR.get(r, F(0)) + w
for r in sorted(pR):
    show(f"rec06p2_pR_{r}", pR[r])
show("rec06p2_pR_sum", sum(pR.values()))
show("rec06p2_E_R", mean(pR))
show("rec06p2_E_R_float", float(mean(pR)))
# (d) E[XY], E[XY|A] with A = {X^2 >= Y}
show("rec06p2_EXY", sum(F(x * y) * w for (x, y) in pts))
show("rec06p2_EXY_float", float(sum(F(x * y) * w for (x, y) in pts)))
A = [(x, y) for (x, y) in pts if x * x >= y]
notA = [q for q in pts if q not in A]
show("rec06p2_A_points", A)
show("rec06p2_notA_points", notA)
show("rec06p2_P_A", w * len(A))
show("rec06p2_E_XY_given_A", sum(F(x * y) for (x, y) in A) / len(A))
show("rec06p2_E_X", mean(pXs))
show("rec06p2_E_Y", mean(pYs))
show("rec06p2_E_X_times_E_Y", mean(pXs) * mean(pYs))
show("rec06p2_cov", sum(F(x * y) * w for (x, y) in pts) - mean(pXs) * mean(pYs))

# ================================================================= 4.8c rec07 P2
print("\n=== rec07 P2 : 3x3 joint PMF with unspecified entries ===")
known = {(1, 3): F(1, 12), (2, 3): F(1, 12),
         (1, 2): F(2, 12),
         (1, 1): F(1, 12), (2, 1): F(2, 12), (3, 1): F(0)}
show("rec07p2_pX1", known[(1, 1)] + known[(1, 2)] + known[(1, 3)])
cY1 = {y: known[(1, y)] / (F(1, 3)) for y in (1, 2, 3)}
for y in (1, 2, 3):
    show(f"rec07p2_pYgX_{y}_given1", cY1[y])
show("rec07p2_E_Y_given_X1", mean(cY1))
show("rec07p2_var_Y_given_X1", var(cY1))
show("rec07p2_var_Y_given_X1_float", float(var(cY1)))
# (d) independence attempt
pY1 = known[(1, 1)] + known[(2, 1)] + known[(3, 1)]
show("rec07p2_pY1_row", pY1, "row y=1 total = 1/12+2/12+0")
rem = 1 - (known[(1, 1)] + known[(1, 2)] + known[(1, 3)] +
           known[(2, 1)] + known[(2, 3)])
show("rec07p2_mass_forced_into_22", rem)
pX2 = known[(2, 1)] + rem + known[(2, 3)]
pY2 = known[(1, 2)] + rem + F(0)
show("rec07p2_pX2_if_indep", pX2)
show("rec07p2_pY2_if_indep", pY2)
show("rec07p2_product_pX2_pY2", pX2 * pY2)
show("rec07p2_product_float", float(pX2 * pY2))
show("rec07p2_pXY22_needed", rem)
show("rec07p2_pXY22_needed_float", float(rem))
show("rec07p2_ratio_x1", known[(1, 3)] / known[(1, 1)])
show("rec07p2_ratio_x2", known[(2, 3)] / known[(2, 1)])
# (e)(f) conditional independence given B
p22 = known[(1, 2)] * known[(2, 1)] / known[(1, 1)]
show("rec07p2_p22_from_condindep", p22)
show("rec07p2_p22_float", float(p22))
PBr = known[(1, 1)] + known[(2, 1)] + known[(1, 2)] + p22
show("rec07p2_P_B", PBr)
show("rec07p2_P_B_float", float(PBr))
show("rec07p2_pXY_given_B_22", p22 / PBr)
show("rec07p2_pXY_given_B_22_float", float(p22 / PBr))
for (x, y) in [(1, 1), (2, 1), (1, 2)]:
    show(f"rec07p2_pXY_given_B_{x}_{y}", known[(x, y)] / PBr)
cXB = {1: (known[(1, 1)] + known[(1, 2)]) / PBr, 2: (known[(2, 1)] + p22) / PBr}
cYB = {1: (known[(1, 1)] + known[(2, 1)]) / PBr, 2: (known[(1, 2)] + p22) / PBr}
for x in (1, 2):
    show(f"rec07p2_pXgB_{x}", cXB[x])
for y in (1, 2):
    show(f"rec07p2_pYgB_{y}", cYB[y])
show("rec07p2_condB_check_22", cXB[2] * cYB[2])

# ================================================================= practice answers
print("\n=== practice-question numbers ===")
# P4.1: marginals of a 2x2 table
prac = {(0, 0): F(1, 8), (0, 1): F(3, 8), (1, 0): F(1, 8), (1, 1): F(3, 8)}
show("prac41_pX0", prac[(0, 0)] + prac[(0, 1)])
show("prac41_pX1", prac[(1, 0)] + prac[(1, 1)])
show("prac41_pY0", prac[(0, 0)] + prac[(1, 0)])
show("prac41_pY1", prac[(0, 1)] + prac[(1, 1)])
show("prac41_indep", all(prac[(a, b)] == (prac[(a, 0)] + prac[(a, 1)]) *
                         (prac[(0, b)] + prac[(1, b)]) for a in (0, 1) for b in (0, 1)))
# P4.3: conditioning the L07 grid on {X = Y}
diag = [(k, k) for k in range(1, 5) if joint[(k, k)] > 0]
Pdiag = sum(joint[c] for c in diag)
show("prac43_P_XeqY", Pdiag)
show("prac43_cond", {str(c): fs(joint[c] / Pdiag) for c in diag})
show("prac43_E_X_given_diag", mean({c[0]: joint[c] / Pdiag for c in diag}))
show("prac43_E_X_given_diag_float", float(mean({c[0]: joint[c] / Pdiag for c in diag})))
# P4.5: var of sum of two independent grid-like RVs; 3 fair dice
die = {k: F(1, 6) for k in range(1, 7)}
show("prac_die_mean", mean(die))
show("prac_die_var", var(die))
show("prac_die_var_float", float(var(die)))
show("prac_var_sum_3dice", 3 * var(die))
show("prac_var_D1_minus_D2", 2 * var(die))
# P4.6: binomial n=5 p=1/2 mean/var
show("prac_binom_mean_5_half", F(5, 2))
show("prac_binom_var_5_half", F(5, 4))
# rec06 P1 practice: E[N | K=0]
cNgK0 = {n_: jNK.get((n_, 0), F(0)) / pK[0] for n_ in range(4)}
for n_ in range(4):
    show(f"prac_pNgK0_{n_}", cNgK0[n_])
show("prac_E_N_given_K0", mean(cNgK0))
show("prac_E_N_given_K0_float", float(mean(cNgK0)))

# ================================================================= extra values quoted in prose
print("\n=== extra values quoted in the fragment ===")
row3 = {y: joint[(3, y)] / pX[3] for y in range(1, 5)}
for y in range(1, 5):
    show(f"pYgX_{y}_given_3", row3[y])
show("E_Y_given_X3", mean(row3))
show("E_Y_given_X3_float", float(mean(row3)))
show("E_Y2_given_X3", sum(F(y) ** 2 * p for y, p in row3.items()))
show("var_Y_given_X3", var(row3))
show("var_Y_given_X3_float", float(var(row3)))
show("EX2_grid", sum(F(x) ** 2 * p for x, p in pX.items()))
show("EY2_grid", sum(F(y) ** 2 * p for y, p in pY.items()))
show("E_X_plus_Y", sum(F(x + y) * p for (x, y), p in joint.items()))
show("E_X_plus_Y_float", float(sum(F(x + y) * p for (x, y), p in joint.items())))
show("P_Xle2", sum(pX[x] for x in (1, 2)))
show("P_Yge3", sum(pY[y] for y in (3, 4)))
show("P_union", sum(pX[x] for x in (1, 2)) + sum(pY[y] for y in (3, 4)) - PB)
show("P_Xle2_given_Yge3", PB / sum(pY[y] for y in (3, 4)))
show("P_Yge3_given_Xle2", PB / sum(pX[x] for x in (1, 2)))
show("rec06p1_EK2", sum(F(k) ** 2 * p for k, p in pK.items()))
show("prac49c_each_star", (1 - sum(known.values())) / 3)
show("binom_EX2", brute_E2)
show("binom_EX2_float", float(brute_E2))

# ================================================================= hat problem (L07 slides 7-8)
print("\n=== hat problem: n people, n hats, uniformly random permutation (L07 slides 7-8) ===")


def hat_bruteforce(n: int):
    """Exact E[X], E[X^2], var(X) over all n! permutations (X = number of fixed points)."""
    from itertools import permutations
    tot = 0
    s1 = 0
    s2 = 0
    for perm in permutations(range(n)):
        x = sum(1 for i, v in enumerate(perm) if v == i)
        tot += 1
        s1 += x
        s2 += x * x
    return F(s1, tot), F(s2, tot), F(s2, tot) - F(s1, tot) ** 2


for n_ in (2, 3, 5, 10, 100):
    # closed forms derived in the fragment
    p_i = F(1, n_)                      # P(X_i = 1) = 1/n
    e_i = p_i                           # E[X_i] = 1/n
    e_ii = p_i                          # E[X_i^2] = E[X_i] since X_i^2 = X_i
    p_pair = F(1, n_) * F(1, n_ - 1)    # P(X_i X_j = 1) = (1/n)(1/(n-1)), i != j
    n_offdiag = n_ * (n_ - 1)           # ordered pairs i != j
    e_x = n_ * e_i                      # = 1
    e_x2 = n_ * e_ii + n_offdiag * p_pair  # = 1 + 1 = 2
    v_x = e_x2 - e_x ** 2               # = 1
    show(f"hat_n{n_}_P_Xi_eq_1", p_i)
    show(f"hat_n{n_}_E_Xi", e_i)
    show(f"hat_n{n_}_E_Xi2", e_ii)
    show(f"hat_n{n_}_P_X1X2_eq_1", p_pair)
    show(f"hat_n{n_}_n_offdiag_pairs", n_offdiag)
    show(f"hat_n{n_}_E_X", e_x)
    show(f"hat_n{n_}_E_X2", e_x2)
    show(f"hat_n{n_}_var_X", v_x)
    # conditional dependence check: P(X_2 = 1 | X_1 = 1) = 1/(n-1) != 1/n = P(X_2 = 1)
    show(f"hat_n{n_}_P_X2_given_X1", F(1, n_ - 1))
    show(f"hat_n{n_}_indicators_independent", F(1, n_ - 1) == F(1, n_))
    if n_ <= 7:
        b1, b2, bv = hat_bruteforce(n_)
        show(f"hat_n{n_}_brute_E_X", b1)
        show(f"hat_n{n_}_brute_E_X2", b2)
        show(f"hat_n{n_}_brute_var_X", bv)
        assert (b1, b2, bv) == (e_x, e_x2, v_x), (n_, b1, b2, bv)
        print(f"    brute force over {n_}! permutations agrees with the closed form")


# ================================================================= 4.11  the multinomial distribution
print("\n=== 4.11 : the multinomial distribution ===")

from math import factorial, prod, isqrt  # noqa: E402
import random  # noqa: E402


def multinom_coef(counts) -> int:
    """n! / (n_1! ... n_r!) for a count vector."""
    n = sum(counts)
    d = 1
    for c in counts:
        d *= factorial(c)
    return factorial(n) // d


def multinom_pmf(counts, thetas) -> F:
    """Joint multinomial PMF at a count vector, exact."""
    assert len(counts) == len(thetas)
    assert sum(thetas) == 1
    return F(multinom_coef(counts)) * prod((F(t) ** c for t, c in zip(thetas, counts)), start=F(1))


def binom_pmf(k, n, p) -> F:
    return F(comb(n, k)) * F(p) ** k * (1 - F(p)) ** (n - k)


# --- Example 4.10 : the grading line.  r = 4 grades, n = 10 items -----------------
n_ex = 10
th = [F(1, 2), F(3, 10), F(3, 20), F(1, 20)]        # A, B, C, D
names = ["A", "B", "C", "D"]
show("mult_ex_n", n_ex)
for nm, t in zip(names, th):
    show(f"mult_ex_theta_{nm}", t)
show("mult_ex_theta_sum", sum(th))

cv = [5, 3, 1, 1]                                    # the queried count vector
show("mult_ex_countvec", cv)
show("mult_ex_coef", multinom_coef(cv))              # 10!/(5!3!1!1!)
show("mult_ex_10fact", factorial(10))
show("mult_ex_denomfact", factorial(5) * factorial(3) * factorial(1) * factorial(1))
prob_part = prod((t ** c for t, c in zip(th, cv)), start=F(1))
show("mult_ex_prodtheta", prob_part)
show("mult_ex_prodtheta_dec", float(prob_part))
p_joint = multinom_pmf(cv, th)
show("mult_ex_joint", p_joint)
show("mult_ex_joint_dec", float(p_joint))

# marginal:  N_C ~ Bin(10, 3/20)
show("mult_ex_marg_NC_eq_2", binom_pmf(2, n_ex, F(3, 20)))
show("mult_ex_marg_NC_eq_2_dec", float(binom_pmf(2, n_ex, F(3, 20))))
show("mult_ex_E_NC", n_ex * F(3, 20))
show("mult_ex_var_NC", n_ex * F(3, 20) * (1 - F(3, 20)))
show("mult_ex_var_NC_dec", float(n_ex * F(3, 20) * (1 - F(3, 20))))

# lumping:  "defective" = C or D, theta = 3/20 + 1/20 = 1/5
th_def = F(3, 20) + F(1, 20)
show("mult_ex_theta_def", th_def)
show("mult_ex_lump_Ndef_eq_3", binom_pmf(3, n_ex, th_def))
show("mult_ex_lump_Ndef_eq_3_dec", float(binom_pmf(3, n_ex, th_def)))
show("mult_ex_E_Ndef", n_ex * th_def)
# lumped trinomial (A, B, defective) at (5, 3, 2)
p_lump3 = multinom_pmf([5, 3, 2], [th[0], th[1], th_def])
show("mult_ex_lump3_coef", multinom_coef([5, 3, 2]))
show("mult_ex_lump3", p_lump3)
show("mult_ex_lump3_dec", float(p_lump3))

# conditioning on N_A = 5 : remaining 5 trials over B, C, D with renormalized thetas
n_rem = n_ex - cv[0]
th_rem = [t / (1 - th[0]) for t in th[1:]]
show("mult_ex_n_rem", n_rem)
for nm, t in zip(names[1:], th_rem):
    show(f"mult_ex_thetarem_{nm}", t)
show("mult_ex_thetarem_sum", sum(th_rem))
p_cond = multinom_pmf(cv[1:], th_rem)
show("mult_ex_cond_coef", multinom_coef(cv[1:]))
show("mult_ex_cond", p_cond)
show("mult_ex_cond_dec", float(p_cond))
p_NA5 = binom_pmf(5, n_ex, th[0])
show("mult_ex_P_NA_eq_5", p_NA5)
show("mult_ex_P_NA_eq_5_dec", float(p_NA5))
show("mult_ex_cond_times_marg", p_NA5 * p_cond)
assert p_NA5 * p_cond == p_joint, (p_NA5 * p_cond, p_joint)
print("    check: P(N_A=5) * P(rest | N_A=5) = joint PMF  OK")

# covariance / correlation
cov_AB = -n_ex * th[0] * th[1]
show("mult_ex_cov_AB", cov_AB)
show("mult_ex_cov_AB_dec", float(cov_AB))
show("mult_ex_var_NA", n_ex * th[0] * (1 - th[0]))
show("mult_ex_var_NB", n_ex * th[1] * (1 - th[1]))
show("mult_ex_var_NB_dec", float(n_ex * th[1] * (1 - th[1])))
rho2 = (th[0] * th[1]) / ((1 - th[0]) * (1 - th[1]))
show("mult_ex_rho_AB_sq", rho2)
show("mult_ex_rho_AB", -float(rho2) ** 0.5)
show("mult_ex_cov_AC", -n_ex * th[0] * th[2])
show("mult_ex_cov_AD", -n_ex * th[0] * th[3])
show("mult_ex_cov_row_A_sum", -n_ex * th[0] * (th[1] + th[2] + th[3]))

# --- Monte Carlo cross-check of every Example 4.10 number ------------------------
rng = random.Random(20410)
M = 4_000_000
thf = [float(t) for t in th]
cum = []
acc = 0.0
for t in thf:
    acc += t
    cum.append(acc)
hit_joint = hit_marg = hit_lump = 0
sA = sB = sAB = 0
for _ in range(M):
    c = [0, 0, 0, 0]
    for _t in range(n_ex):
        u = rng.random()
        k = 0
        while u > cum[k]:
            k += 1
        c[k] += 1
    if c == cv:
        hit_joint += 1
    if c[2] == 2:
        hit_marg += 1
    if c[2] + c[3] == 3:
        hit_lump += 1
    sA += c[0]
    sB += c[1]
    sAB += c[0] * c[1]
mc_joint = hit_joint / M
mc_marg = hit_marg / M
mc_lump = hit_lump / M
mc_cov = sAB / M - (sA / M) * (sB / M)
show("mult_ex_mc_trials", M)
show("mult_ex_mc_joint", mc_joint)
show("mult_ex_mc_marg_NC_eq_2", mc_marg)
show("mult_ex_mc_lump_Ndef_eq_3", mc_lump)
show("mult_ex_mc_cov_AB", mc_cov)
for lab, exact, mc, tol in (
    ("joint", float(p_joint), mc_joint, 2e-3),
    ("marginal", float(binom_pmf(2, n_ex, F(3, 20))), mc_marg, 2e-3),
    ("lumped", float(binom_pmf(3, n_ex, th_def)), mc_lump, 2e-3),
    ("cov", float(cov_AB), mc_cov, 5e-3),
):
    assert abs(exact - mc) < tol, (lab, exact, mc)
    print(f"    Monte Carlo {lab:9s}: exact {exact:.6f} vs simulated {mc:.6f}  OK")

# --- Practice 4.25 : fair die, n = 12, every face exactly twice -------------------
p25 = multinom_pmf([2] * 6, [F(1, 6)] * 6)
show("mult_p25_coef", multinom_coef([2] * 6))
show("mult_p25_12fact", factorial(12))
show("mult_p25_2fact6", factorial(2) ** 6)
show("mult_p25_6pow12", 6 ** 12)
show("mult_p25_prob", p25)
show("mult_p25_prob_dec", float(p25))
show("mult_p25_marg_N1_eq_2", binom_pmf(2, 12, F(1, 6)))
show("mult_p25_marg_N1_eq_2_dec", float(binom_pmf(2, 12, F(1, 6))))
show("mult_p25_cov", -12 * F(1, 6) * F(1, 6))
show("mult_p25_var", 12 * F(1, 6) * F(5, 6))
show("mult_p25_rho", -float(F(1, 5)))

# --- Practice 4.26 : survey, r = 3, n = 8 ---------------------------------------
th26 = [F(1, 2), F(3, 10), F(1, 5)]          # yes, no, undecided
show("mult_p26_theta_sum", sum(th26))
p26 = multinom_pmf([4, 3, 1], th26)
show("mult_p26_coef", multinom_coef([4, 3, 1]))
show("mult_p26_joint", p26)
show("mult_p26_joint_dec", float(p26))
show("mult_p26_marg_Nund_eq_1", binom_pmf(1, 8, F(1, 5)))
show("mult_p26_marg_Nund_eq_1_dec", float(binom_pmf(1, 8, F(1, 5))))
show("mult_p26_theta_notyes", F(3, 10) + F(1, 5))
show("mult_p26_lump_Nnotyes_eq_4", binom_pmf(4, 8, F(1, 2)))
show("mult_p26_lump_Nnotyes_eq_4_dec", float(binom_pmf(4, 8, F(1, 2))))
show("mult_p26_cov_yes_no", -8 * th26[0] * th26[1])
show("mult_p26_cov_yes_no_dec", float(-8 * th26[0] * th26[1]))

# --- Practice 4.27 : var of a lumped pair, two ways ------------------------------
n27, t1, t2 = 8, F(1, 2), F(3, 10)
v1 = n27 * t1 * (1 - t1)
v2 = n27 * t2 * (1 - t2)
c12 = -n27 * t1 * t2
show("mult_p27_var_N1", v1)
show("mult_p27_var_N2", v2)
show("mult_p27_var_N2_dec", float(v2))
show("mult_p27_cov_12", c12)
show("mult_p27_cov_12_dec", float(c12))
show("mult_p27_sum_route", v1 + v2 + 2 * c12)
show("mult_p27_sum_route_dec", float(v1 + v2 + 2 * c12))
show("mult_p27_lump_route", n27 * (t1 + t2) * (1 - t1 - t2))
show("mult_p27_lump_route_dec", float(n27 * (t1 + t2) * (1 - t1 - t2)))
assert v1 + v2 + 2 * c12 == n27 * (t1 + t2) * (1 - t1 - t2)
print("    check: var(N_1+N_2) both routes agree  OK")

out = Path(__file__).resolve().parent / "g2_s4.json"
out.write_text(json.dumps(R, indent=1), encoding="utf-8")
print("\nwrote", out)
