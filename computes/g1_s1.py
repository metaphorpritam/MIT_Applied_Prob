# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Every number quoted in notes/src/fragments/g1_s1.html (L01 + rec01).

Run:  uv run computes/g1_s1.py
Writes computes/g1_s1.json.
"""
from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict = {}


def show(key, val, note=""):
    R[key] = val
    print(f"{key:38s} = {val}   {note}")


# ---------------------------------------------------------------- L01 slide 8
# Two rolls of a fair tetrahedral die: Omega = {1,2,3,4}^2, each outcome 1/16.
OMEGA = list(itertools.product([1, 2, 3, 4], repeat=2))
N = len(OMEGA)
show("omega_size", N)
show("p_each", str(F(1, N)))

events = {
    "A_11_or_12": lambda x, y: (x, y) in [(1, 1), (1, 2)],
    "B_X_eq_1": lambda x, y: x == 1,
    "C_sum_odd": lambda x, y: (x + y) % 2 == 1,
    "D_min_eq_2": lambda x, y: min(x, y) == 2,
}
grid_counts, grid_probs, grid_cells = {}, {}, {}
for name, f in events.items():
    cells = [o for o in OMEGA if f(*o)]
    grid_cells[name] = cells
    grid_counts[name] = len(cells)
    grid_probs[name] = str(F(len(cells), N))
    print(f"  {name:12s} count={len(cells):2d}  P={F(len(cells), N)} = {len(cells)/N}")
show("grid_counts", grid_counts)
show("grid_probs", grid_probs)
show("grid_cells", {k: [list(c) for c in v] for k, v in grid_cells.items()})
show("grid_probs_dec", {k: grid_counts[k] / N for k in grid_counts})

# sub-counts used in prose for the sum-odd event
odd_first_even_second = sum(1 for x, y in OMEGA if x % 2 == 1 and y % 2 == 0)
even_first_odd_second = sum(1 for x, y in OMEGA if x % 2 == 0 and y % 2 == 1)
show("sum_odd_split", [odd_first_even_second, even_first_odd_second])
# min = 2 decomposition:  (2,y) y>=2   plus  (x,2) x>2
minA = [o for o in OMEGA if o[0] == 2 and o[1] >= 2]
minB = [o for o in OMEGA if o[1] == 2 and o[0] > 2]
show("min2_partA", [list(c) for c in minA])
show("min2_partB", [list(c) for c in minB])

# ------------------------------------------------------- L01 slide 11 series
# P(n) = 2^-n on {1,2,...}; P(even) = sum_{k>=1} 2^{-2k} = sum (1/4)^k
terms = [F(1, 4) ** k for k in range(1, 9)]
partial = []
s = F(0)
for t in terms:
    s += t
    partial.append(str(s))
show("geom_terms", [str(t) for t in terms[:5]])
show("geom_partials", partial)
show("geom_partials_dec", [float(F(x)) for x in partial])
show("geom_sum_exact", str(F(1, 4) / (1 - F(1, 4))))
show("geom_sum_dec", float(F(1, 4) / (1 - F(1, 4))))
# closed form of the partial sum: (1/4)(1-(1/4)^n)/(1-1/4) = (1/3)(1-4^-n)
check = [F(1, 3) * (1 - F(1, 4) ** n) for n in range(1, 9)]
show("geom_partial_closedform_ok", [str(a) == str(b) for a, b in zip(partial, [str(c) for c in check])])
# odd-index counterpart, used in the squeeze argument
odd_sum = F(1, 2) / (1 - F(1, 4))
show("geom_odd_sum_exact", str(odd_sum))
show("geom_odd_sum_dec", float(odd_sum))
show("geom_even_plus_odd", str(F(1, 3) + odd_sum))
show("normalization_check", str(sum(F(1, 2) ** n for n in range(1, 200))) == str(1 - F(1, 2) ** 199))
show("sum_2minusn_limit", 1.0)
show("tail_after_4_terms", str(1 - sum(F(1, 2) ** n for n in range(1, 5))))
show("first_four_masses", [str(F(1, 2) ** n) for n in range(1, 5)])

# ------------------------------------------------------- rec01 P2 chocolate
pA, pB, pAB = 0.6, 0.7, 0.4
pAuB = pA + pB - pAB
show("choc_pA", pA)
show("choc_pB", pB)
show("choc_pAB", pAB)
show("choc_union", round(pAuB, 10))
show("choc_neither", round(1 - pAuB, 10))
show("choc_only_genius", round(pA - pAB, 10))
show("choc_only_choc", round(pB - pAB, 10))
show("choc_venn_check", round((pA - pAB) + pAB + (pB - pAB) + (1 - pAuB), 10))
show("choc_symdiff", round(pA + pB - 2 * pAB, 10))

# ------------------------------------------------------- rec01 P3 loaded die
c = F(1, 9)
show("die_c", str(c))
show("die_normalization_lhs", "3c + 3(2c) = 3c + 6c = 9c")
show("die_odd_prob", str(c))
show("die_even_prob", str(2 * c))
show("die_total", str(3 * c + 3 * 2 * c))
show("die_P123", str(c + 2 * c + c))
show("die_P123_dec", float(4 * c))
show("die_P_even_face_set", str(3 * 2 * c))

# ------------------------------------------------------- L01 slide 10 square
# P(X+Y <= z) on the unit square, uniform (probability = area)
def p_sum_le(z: float) -> float:
    if z <= 0:
        return 0.0
    if z <= 1:
        return z * z / 2.0
    if z <= 2:
        return 1.0 - (2.0 - z) ** 2 / 2.0
    return 1.0


show("p_sum_le_half_exact", str(F(1, 2) ** 2 / 2))
show("p_sum_le_half", p_sum_le(0.5))
show("triangle_legs", 0.5)
show("triangle_area_formula", "(1/2) * base * height = (1/2)*(1/2)*(1/2) = 1/8")
show("p_sum_le_table", {f"{z:.2f}": round(p_sum_le(z), 6) for z in [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]})

rng = np.random.default_rng(6041)
M = 4_000_000
xs, ys = rng.random(M), rng.random(M)
show("mc_p_sum_le_half", round(float(np.mean(xs + ys <= 0.5)), 5))

# point mass: P(X in [0.5-eps, 0.5+eps], Y in [0.3-eps, 0.3+eps]) = (2 eps)^2
show("point_box_areas", {f"eps=1e-{k}": (2 * 10.0 ** (-k)) ** 2 for k in [1, 2, 3, 6]})

# ------------------------------------------------------- rec01 P4 Romeo&Juliet
def p_meet(w: float) -> float:
    return 1.0 - (1.0 - w) ** 2


w0 = 0.25
show("rj_w", w0)
show("rj_one_minus_w", 1 - w0)
show("rj_corner_triangle_area_each", str(F(1, 2) * F(3, 4) ** 2))
show("rj_two_triangles_area", str(F(3, 4) ** 2))
show("rj_P_meet_exact", str(1 - F(3, 4) ** 2))
show("rj_P_meet", p_meet(w0))
show("rj_P_meet_pct", round(100 * p_meet(w0), 2))
show("rj_P_nomeet_exact", str(F(3, 4) ** 2))
show("rj_table", {f"{w:.2f}": round(p_meet(w), 6) for w in [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]})
show("mc_rj_P_meet", round(float(np.mean(np.abs(xs - ys) <= w0)), 5))

# widget formula check on a grid: 1-(1-w)^2 vs. direct area integration
ws = np.linspace(0, 1, 101)
grid = np.linspace(0, 1, 2001)
XX, YY = np.meshgrid(grid, grid)
num_err = 0.0
for w in [0.05, 0.25, 0.4, 0.6, 0.9]:
    num = float(np.mean(np.abs(XX - YY) <= w))
    num_err = max(num_err, abs(num - p_meet(w)))
show("widget_rj_max_grid_err", round(num_err, 5))
zerr = 0.0
for z in [0.3, 0.5, 0.9, 1.0, 1.3, 1.7]:
    num = float(np.mean(XX + YY <= z))
    zerr = max(zerr, abs(num - p_sum_le(z)))
show("widget_sumz_max_grid_err", round(zerr, 5))
show("rj_curve", {f"{w:.2f}": round(p_meet(w), 4) for w in ws[::10]})

# ------------------------------------------------- rec01 G1 continuity check
# numeric sanity: A_n = [0, n] under an exponential-ish law on [0,inf)
lam = 1.0
show("cont_P_0_n", {str(n): round(1 - np.exp(-lam * n), 6) for n in [1, 2, 5, 10, 20]})
show("cont_P_n_inf", {str(n): float(f"{np.exp(-lam*n):.3e}") for n in [1, 2, 5, 10, 20]})

# =====================================================================
# Numbers quoted in the practice questions of g1_s1.html
# =====================================================================
# --- 1.1 practice: three rolls of the tetrahedral die
show("pr_three_rolls_size", 4 ** 3)
O3 = list(itertools.product([1, 2, 3, 4], repeat=3))
show("pr_three_rolls_check", len(O3))
show("pr_P_all_distinct", str(F(sum(1 for o in O3 if len(set(o)) == 3), 4 ** 3)))
# sum of two tetrahedral rolls: distribution over the coarse space {2,...,8}
sum_counts = {s: sum(1 for x, y in OMEGA if x + y == s) for s in range(2, 9)}
show("pr_sum_counts", sum_counts)
show("pr_sum_probs", {s: str(F(c, 16)) for s, c in sum_counts.items()})
show("pr_P_sum_eq_5", str(F(sum_counts[5], 16)))

# --- 1.2 practice: numeric set-algebra drill
qA, qB, qAB = 0.5, 0.4, 0.1
show("pr2_union", round(qA + qB - qAB, 10))
show("pr2_neither", round(1 - (qA + qB - qAB), 10))
show("pr2_exactly_one", round(qA + qB - 2 * qAB, 10))
show("pr2_A_only", round(qA - qAB, 10))
show("pr2_B_only", round(qB - qAB, 10))

# --- 1.3 practice: more events on the 4x4 grid
pr_events = {
    "max_eq_3": lambda x, y: max(x, y) == 3,
    "X_ge_Y": lambda x, y: x >= y,
    "sum_eq_5": lambda x, y: x + y == 5,
    "X_ne_Y": lambda x, y: x != y,
}
show("pr3_counts", {k: sum(1 for o in OMEGA if f(*o)) for k, f in pr_events.items()})
show("pr3_probs", {k: str(F(sum(1 for o in OMEGA if f(*o)), 16)) for k, f in pr_events.items()})
show("pr3_probs_dec", {k: sum(1 for o in OMEGA if f(*o)) / 16 for k, f in pr_events.items()})

# --- 1.4 practice: more regions of the unit square
show("pr4_P_sum_le_1p5", p_sum_le(1.5))
show("pr4_P_sum_le_1p5_exact", str(1 - F(1, 2) * F(1, 2) ** 2))
show("pr4_P_max_le_half", 0.25)
show("pr4_P_max_le_half_exact", str(F(1, 2) ** 2))
# P(XY <= 1/2) = 1/2 + (1/2)ln 2   (area under y = 1/(2x) for x in [1/2,1])
pr4_xy = 0.5 + 0.5 * float(np.log(2.0))
show("pr4_P_prod_le_half", round(pr4_xy, 6))
show("pr4_P_prod_le_half_mc", round(float(np.mean(xs * ys <= 0.5)), 5))

# --- 1.5 practice: other events under P(n) = 2^-n
show("pr5_P_n_ge_3_exact", str(sum(F(1, 2) ** n for n in range(3, 300))))
show("pr5_P_n_ge_3", 0.25)
div3 = F(1, 8) / (1 - F(1, 8))
show("pr5_P_div_by_3_exact", str(div3))
show("pr5_P_div_by_3", round(float(div3), 6))

# --- 1.7 practice: loaded die with P(k) proportional to k, and R&J variants
tot = sum(range(1, 7))
show("pr7_die_total_weight", tot)
show("pr7_die_c", str(F(1, tot)))
show("pr7_die_P123_exact", str(F(1 + 2 + 3, tot)))
show("pr7_die_P123", round(float(F(6, tot)), 6))
w20 = F(1, 3)
show("pr7_rj_w20_exact", str(1 - (1 - w20) ** 2))
show("pr7_rj_w20", round(float(1 - (1 - w20) ** 2), 6))
show("pr7_rj_w20_mc", round(float(np.mean(np.abs(xs - ys) <= 1 / 3)), 5))
a_, b_ = F(1, 4), F(1, 2)          # Romeo waits a, Juliet waits b
pr7_asym = 1 - (1 - a_) ** 2 / 2 - (1 - b_) ** 2 / 2
show("pr7_rj_asym_exact", str(pr7_asym))
show("pr7_rj_asym", round(float(pr7_asym), 6))
show("pr7_rj_asym_mc", round(float(np.mean((ys - xs <= 0.25) & (xs - ys <= 0.5))), 5))

# --- extra counts / differences quoted verbatim in the prose
show("pr_three_rolls_distinct_count", sum(1 for o in O3 if len(set(o)) == 3))
show("pr_three_rolls_distinct_frac", round(sum(1 for o in O3 if len(set(o)) == 3) / 64, 6))
show("pr3_max3_split", [sum(1 for o in OMEGA if o[0] == 3 and o[1] <= 3),
                        sum(1 for o in OMEGA if o[1] == 3 and o[0] < 3)])
show("pr3_XgtY_count", sum(1 for x, y in OMEGA if x > y))
show("pr3_diag_count", sum(1 for x, y in OMEGA if x == y))
u_col_row = [o for o in OMEGA if o[0] == 1 or o[1] == 1]
show("pr6_union_count", len(u_col_row))
show("pr6_union_prob", str(F(len(u_col_row), 16)))
show("pr6_union_prob_dec", len(u_col_row) / 16)
show("pr6_naive_sum", str(F(4, 16) + F(4, 16)))
show("rj_gain_25_to_50", round(p_meet(0.5) - p_meet(0.25), 6))
show("rj_gain_50_to_100", round(p_meet(1.0) - p_meet(0.5), 6))
show("rj_gain_15_to_20min", round(float(1 - (1 - F(1, 3)) ** 2) - p_meet(0.25), 6))
show("choc_bounds_on_pAB", [round(pA + pB - 1, 10), round(min(pA, pB), 10)])
show("choc_bad_case_neither", round(1 - (pA + pB - 0.2), 10))
show("min2_ge2_count", sum(1 for x, y in OMEGA if min(x, y) >= 2))
show("min2_ge3_count", sum(1 for x, y in OMEGA if min(x, y) >= 3))
show("pr7_die_masses", [str(F(k, 21)) for k in range(1, 7)])

# --- 1.6 practice: classify-then-solve decision drills
# (a) fair 8-sided die rolled twice, P(X + Y = 5)  [finite + equally likely]
O8 = list(itertools.product(range(1, 9), repeat=2))
show("pr6d_omega8_size", len(O8))
n_sum5 = sum(1 for x, y in O8 if x + y == 5)
show("pr6d_sum5_count", n_sum5)
show("pr6d_sum5_exact", str(F(n_sum5, len(O8))))
show("pr6d_sum5", round(n_sum5 / len(O8), 6))
# (b) geometric masses P(n) = (2/3)(1/3)^(n-1) on {1,2,...}, P(n >= 3)  [countably infinite]
geo = [F(2, 3) * F(1, 3) ** (n - 1) for n in range(1, 400)]
show("pr6d_geo_total", str(round(float(sum(geo)), 12)))          # -> 1.0
geo_ge3 = F(2, 3) * F(1, 3) ** 2 / (1 - F(1, 3))                 # closed form
show("pr6d_geo_ge3_exact", str(geo_ge3))
show("pr6d_geo_ge3", round(float(geo_ge3), 6))
show("pr6d_geo_ge3_partialsum_check", round(float(sum(geo[2:])), 12))
# (c) X, Y uniform on the unit square, P(Y >= 2X)  [continuous, polygon area]
show("pr6d_tri_exact", str(F(1, 2) * F(1, 2) * 1))
show("pr6d_tri", 0.25)
show("pr6d_tri_mc", round(float(np.mean(ys >= 2 * xs)), 5))
# trap item: no discrete uniform law on a countably infinite Omega; P({1,2}) under 2^-n
show("pr6d_trap_exact", str(F(1, 2) + F(1, 4)))
show("pr6d_trap", 0.75)

Path(__file__).with_suffix(".json").write_text(json.dumps(R, indent=1), encoding="utf-8")
print("\nwrote", Path(__file__).with_suffix(".json"))
