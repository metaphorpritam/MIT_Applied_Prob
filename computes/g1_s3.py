# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""G1 section 3 (Independence) — every number that appears in the fragment.

Run:  uv run computes/g1_s3.py
Writes computes/g1_s3.json
"""
from __future__ import annotations

import json
import sys
from math import comb
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R = {}


def show(key, val, note=""):
    R[key] = val
    if isinstance(val, float):
        print(f"{key:44s} = {val!r:22s} {note}")
    else:
        print(f"{key:44s} = {val} {note}")


# ---------------------------------------------------------------- 3.1 tree
print("\n=== 3.1  three tosses of a biased coin (L03 slide 2) ===")
p = 0.6
show("tree_p", p)
show("tree_1mp", 1 - p)
show("P_THT", (1 - p) * p * (1 - p), "= p(1-p)^2")
show("P_HTT", p * (1 - p) ** 2)
show("P_TTH", (1 - p) ** 2 * p)
show("P_one_head", 3 * p * (1 - p) ** 2)
show("P_first_H_given_one_head", (p * (1 - p) ** 2) / (3 * p * (1 - p) ** 2))
show("P_HHH", p ** 3)
show("P_TTT", (1 - p) ** 3)
show("P_HHT", p ** 2 * (1 - p))
show("P_two_heads", 3 * p ** 2 * (1 - p))
show("P_at_least_one_head", 1 - (1 - p) ** 3)
leaves = {
    "HHH": p ** 3, "HHT": p ** 2 * (1 - p), "HTH": p ** 2 * (1 - p), "HTT": p * (1 - p) ** 2,
    "THH": p ** 2 * (1 - p), "THT": p * (1 - p) ** 2, "TTH": p * (1 - p) ** 2, "TTT": (1 - p) ** 3,
}
show("tree_leaves", {k: round(v, 6) for k, v in leaves.items()})
show("tree_leaf_sum", sum(leaves.values()))

# practice 3.1: two rolls of a 4-sided die, A = first roll <= 2, B = sum = 5
outc = [(i, j) for i in range(1, 5) for j in range(1, 5)]
A = [o for o in outc if o[0] <= 2]
B = [o for o in outc if sum(o) == 5]
AB = [o for o in outc if o in A and o in B]
show("die4_PA", len(A) / 16)
show("die4_PB", len(B) / 16)
show("die4_PAB", len(AB) / 16)
show("die4_PA_PB", len(A) / 16 * len(B) / 16)
show("die4_AB_outcomes", AB)
# practice: A = max is 2, B = min is 2  (dependent)
A2 = [o for o in outc if max(o) == 2]
B2 = [o for o in outc if min(o) == 2]
show("die4_Pmax2", len(A2) / 16)
show("die4_Pmin2", len(B2) / 16)
show("die4_Pmax2_min2", len([o for o in outc if max(o) == 2 and min(o) == 2]) / 16)
show("die4_Pmax2_times_Pmin2", len(A2) / 16 * len(B2) / 16)

# ---------------------------------------------------------------- 3.2 traps
print("\n=== 3.2  independence vs disjointness ===")
PA, PB = 0.5, 0.4
show("t2_PA", PA)
show("t2_PB", PB)
show("t2_PAB_indep", PA * PB)
show("t2_PAuB_indep", PA + PB - PA * PB)
show("t2_PAcBc", (1 - PA) * (1 - PB))
show("t2_PAuB_disjoint", PA + PB)
# figure panel numbers: disjoint example P(A)=0.3,P(B)=0.25
show("fig_disj_PA", 0.3)
show("fig_disj_PB", 0.25)
show("fig_disj_PAB", 0.0)
show("fig_disj_PA_PB", 0.3 * 0.25)
# independent panel built as a product rectangle
show("fig_ind_PA", 0.4)
show("fig_ind_PB", 0.5)
show("fig_ind_PAB", 0.4 * 0.5)

# ---------------------------------------------------------------- 3.3 cond. indep.
print("\n=== 3.3  two unfair coins (L03 slide 5) ===")
qA, qB, pi = 0.9, 0.1, 0.5
show("coin_qA", qA)
show("coin_qB", qB)
show("P_H1", pi * qA + (1 - pi) * qB)
show("P_H1H2_given_A", qA * qA)
show("P_H1H2_given_B", qB * qB)
show("P_H1H2", pi * qA ** 2 + (1 - pi) * qB ** 2)
show("P_H1_times_P_H2", (pi * qA + (1 - pi) * qB) ** 2)
show("P_H1H2_minus_prod", pi * qA ** 2 + (1 - pi) * qB ** 2 - (pi * qA + (1 - pi) * qB) ** 2)


def post_A(k, n=None, q=qA, prior=pi):
    """P(coin A | k heads out of first k tosses)  (all-heads observation)."""
    n = k if n is None else n
    la = prior * q ** k * (1 - q) ** (n - k)
    lb = (1 - prior) * (1 - q) ** k * q ** (n - k)
    return la / (la + lb)


show("P_10H_given_A", qA ** 10)
show("P_10H_given_B", qB ** 10)
show("P_10H", pi * qA ** 10 + pi * qB ** 10)
show("P_A_given_10H", post_A(10))
show("P_B_given_10H", 1 - post_A(10))
show("P_toss11_H_given_10H", post_A(10) * qA + (1 - post_A(10)) * qB)
show("P_A_given_1H", post_A(1))
show("P_toss2_H_given_1H", post_A(1) * qA + (1 - post_A(1)) * qB)
show("P_A_given_3H", post_A(3))
show("P_toss4_H_given_3H", post_A(3) * qA + (1 - post_A(3)) * qB)
show("posterior_curve_k0to12", [round(post_A(k), 8) for k in range(13)])
show("predictive_curve_k0to12",
     [round(post_A(k) * qA + (1 - post_A(k)) * qB, 8) for k in range(13)])

# rec03 P1 / L03 slide 7 numbers (fair coins)
print("\n=== 3.3/3.4  two fair coins: H1, H2, D (rec03 P1, L03 slide 7) ===")
show("fair_PH1", 0.5)
show("fair_PH2", 0.5)
show("fair_PH1H2", 0.25)
show("fair_PD", 0.5)
show("fair_PH1_given_D", 0.25 / 0.5)
show("fair_PH2_given_D", 0.25 / 0.5)
show("fair_PH1H2_given_D", 0.0)
show("fair_PH1D_prod", 0.5 * 0.5)
show("fair_PC", 0.5)          # C = same result = D^c
show("fair_PCA", 0.25)
show("fair_PA_PC", 0.5 * 0.5)
show("fair_PABC", 0.25)
show("fair_PA_PB_PC", 0.5 ** 3)
show("fair_PC_given_AB", 1.0)

# king's sibling
print("\n=== 3.3  the king's sibling (L03 slide 8) ===")
fam = ["BB", "BG", "GB", "GG"]
atleast1B = [f for f in fam if "B" in f]
show("king_families_atleast1B", atleast1B)
show("king_P_sibling_female_reading1", sum(1 for f in atleast1B if "G" in f) / len(atleast1B))
show("king_P_sibling_female_reading2", 0.5)

# practice 3.3: two coins q=0.8 / 0.3
qa2, qb2 = 0.8, 0.3
show("prac33_PH1", 0.5 * qa2 + 0.5 * qb2)
show("prac33_PH1H2", 0.5 * qa2 ** 2 + 0.5 * qb2 ** 2)
show("prac33_prod", (0.5 * qa2 + 0.5 * qb2) ** 2)
show("prac33_P_A_given_H1", 0.5 * qa2 / (0.5 * qa2 + 0.5 * qb2))
show("prac33_P_H2_given_H1", (0.5 * qa2 ** 2 + 0.5 * qb2 ** 2) / (0.5 * qa2 + 0.5 * qb2))

# practice 3.3b: A, B independent, condition on C = A u B
def cond_on_union(a, b):
    """Returns (P(C), P(A|C), P(B|C), P(A n B|C), P(A|C)P(B|C)) for independent A, B."""
    pc = a + b - a * b
    return pc, a / pc, b / pc, a * b / pc, (a / pc) * (b / pc)


for (aa, bb) in ((0.5, 0.5), (0.8, 0.3), (1.0, 0.3)):
    pc, pac, pbc, pabc, prod = cond_on_union(aa, bb)
    show(f"prac33b_a{aa}_b{bb}",
         {"P(C)": round(pc, 8), "P(A|C)": round(pac, 8), "P(B|C)": round(pbc, 8),
          "P(AnB|C)": round(pabc, 8), "P(A|C)P(B|C)": round(prod, 8),
          "equal": abs(pabc - prod) < 1e-12})
show("prac33b_gap_half_half", cond_on_union(0.5, 0.5)[3] - cond_on_union(0.5, 0.5)[4])

# ---------------------------------------------------------------- 3.4 collections
print("\n=== 3.4  triple-product without pairwise independence (book Ex 1.23) ===")
rolls = [(i, j) for i in range(1, 7) for j in range(1, 7)]
Ae = [o for o in rolls if o[0] in (1, 2, 3)]
Be = [o for o in rolls if o[0] in (3, 4, 5)]
Ce = [o for o in rolls if sum(o) == 9]
n36 = len(rolls)
show("die6_PA", len(Ae) / n36)
show("die6_PB", len(Be) / n36)
show("die6_PC", len(Ce) / n36)
show("die6_C_outcomes", Ce)
show("die6_PAB", len([o for o in rolls if o in Ae and o in Be]) / n36)
show("die6_PA_PB", len(Ae) / n36 * len(Be) / n36)
show("die6_PAC", len([o for o in rolls if o in Ae and o in Ce]) / n36)
show("die6_PA_PC", len(Ae) / n36 * len(Ce) / n36)
show("die6_PBC", len([o for o in rolls if o in Be and o in Ce]) / n36)
show("die6_PB_PC", len(Be) / n36 * len(Ce) / n36)
show("die6_PABC", len([o for o in rolls if o in Ae and o in Be and o in Ce]) / n36)
show("die6_PA_PB_PC", len(Ae) / n36 * len(Be) / n36 * len(Ce) / n36)
show("collection_n_conditions_n3", 2 ** 3 - 3 - 1)
show("collection_n_conditions_n4", 2 ** 4 - 4 - 1)
show("collection_n_conditions_n5", 2 ** 5 - 5 - 1)

# ---------------------------------------------------------------- 3.5 random walk
print("\n=== 3.5  drunk tightrope walker (rec03 P2) ===")
pw = 0.6
show("rw_p", pw)
show("rw_PFB", pw * (1 - pw))
show("rw_PBF", (1 - pw) * pw)
show("rw_P_same_after2", 2 * pw * (1 - pw))
show("rw_P_plus2_after2", pw ** 2)
show("rw_P_minus2_after2", (1 - pw) ** 2)
show("rw_check_2steps", pw ** 2 + 2 * pw * (1 - pw) + (1 - pw) ** 2)
show("rw_C32", comb(3, 2))
show("rw_path_prob_3steps_2F", pw ** 2 * (1 - pw))
show("rw_P_plus1_after3", 3 * pw ** 2 * (1 - pw))
show("rw_P_first_F_given_plus1", 2 * pw ** 2 * (1 - pw) / (3 * pw ** 2 * (1 - pw)))
show("rw_P_plus3_after3", pw ** 3)
show("rw_C42", comb(4, 2))
show("rw_P_back_at_0_after4", comb(4, 2) * pw ** 2 * (1 - pw) ** 2)
show("rw_dist_after3", {d: round(comb(3, k) * pw ** k * (1 - pw) ** (3 - k), 6)
                        for k, d in zip(range(4), (-3, -1, 1, 3))})

# ---------------------------------------------------------------- 3.6 channel
print("\n=== 3.6  noisy binary channel + repetition code (rec03 P3) ===")
e0, e1, ps = 0.05, 0.10, 0.60
show("ch_e0", e0)
show("ch_e1", e1)
show("ch_p", ps)
show("ch_a_P_correct", ps * (1 - e0) + (1 - ps) * (1 - e1))
show("ch_a_term0", ps * (1 - e0))
show("ch_a_term1", (1 - ps) * (1 - e1))
show("ch_a_P_error", 1 - (ps * (1 - e0) + (1 - ps) * (1 - e1)))
show("ch_b_P_1011_ok", (1 - e1) * (1 - e0) * (1 - e1) * (1 - e1))
show("ch_b_factored", (1 - e0) * (1 - e1) ** 3)
show("ch_c_term_nofail", (1 - e0) ** 3)
show("ch_c_term_one_err", 3 * (1 - e0) ** 2 * e0)
show("ch_c_P_decode0_ok", (1 - e0) ** 3 + 3 * (1 - e0) ** 2 * e0)
show("ch_c_P_decode0_bad", e0 ** 3 + 3 * e0 ** 2 * (1 - e0))
show("ch_c_single_bit_err", e0)
show("ch_c_improvement_factor", e0 / (e0 ** 3 + 3 * e0 ** 2 * (1 - e0)))
show("ch_c_P_decode1_ok", (1 - e1) ** 3 + 3 * (1 - e1) ** 2 * e1)
lik0 = e0 * (1 - e0) * e0                # sent 000, received 101
lik1 = (1 - e1) * e1 * (1 - e1)          # sent 111, received 101
show("ch_d_lik0", lik0)
show("ch_d_lik1", lik1)
show("ch_d_num", ps * lik0)
show("ch_d_den", ps * lik0 + (1 - ps) * lik1)
show("ch_d_P_0_given_101", ps * lik0 / (ps * lik0 + (1 - ps) * lik1))
show("ch_d_P_1_given_101", (1 - ps) * lik1 / (ps * lik0 + (1 - ps) * lik1))
# odds-form cross-check of part (d): everything stated "in favour of 1"
show("ch_d_prior_odds_1_over_0", (1 - ps) / ps)
show("ch_d_likelihood_ratio_1_over_0", lik1 / lik0)
show("ch_d_posterior_odds_1_over_0", ((1 - ps) / ps) * (lik1 / lik0))
_po = ((1 - ps) / ps) * (lik1 / lik0)
show("ch_d_P_1_given_101_from_odds", _po / (1 + _po))


def maj_err(n, eps):
    """P(majority decoder wrong) for odd n, symmetric bit-error prob eps."""
    return sum(comb(n, k) * eps ** k * (1 - eps) ** (n - k) for k in range((n + 1) // 2, n + 1))


odd = list(range(1, 16, 2))
for eps in (0.05, 0.10, 0.20, 0.30, 0.45):
    show(f"rep_err_eps{eps}", {n: round(maj_err(n, eps), 10) for n in odd})
show("rep_err_eps0.10_n3", maj_err(3, 0.10))
show("rep_err_eps0.10_n5", maj_err(5, 0.10))
show("rep_err_eps0.10_n7", maj_err(7, 0.10))
show("rep_err_eps0.10_n15", maj_err(15, 0.10))
show("rep_err_eps0.05_n3", maj_err(3, 0.05))
show("rep_err_eps0.45_n15", maj_err(15, 0.45))
show("rep_n5_terms_eps0.10", {k: round(comb(5, k) * 0.10 ** k * 0.90 ** (5 - k), 8)
                              for k in (3, 4, 5)})
show("rep_err_eps0.5_n7", maj_err(7, 0.5))

# widget cross-check table (what the JS must reproduce)
show("widget_repcode_check",
     {f"eps={eps},n={n}": round(maj_err(n, eps), 8)
      for eps in (0.10, 0.30) for n in (1, 3, 7, 15)})
show("widget_twocoin_check",
     {f"q={q},k={k}": [round(post_A(k, q=q), 8),
                       round(post_A(k, q=q) * q + (1 - post_A(k, q=q)) * (1 - q), 8)]
      for q in (0.75, 0.9) for k in (0, 1, 3, 10)})

# ---------------------------------------------------------------- extra practice
print("\n=== practice questions ===")
# 3.2 practice: one fair die, A = {1,2,3}, B = {3,6}  -> independent
die = list(range(1, 7))
Ad = [x for x in die if x <= 3]
Bd = [x for x in die if x % 3 == 0]
show("prac32_PA", len(Ad) / 6)
show("prac32_PB", len(Bd) / 6)
show("prac32_PAB", len([x for x in die if x in Ad and x in Bd]) / 6)
show("prac32_PA_PB", len(Ad) / 6 * len(Bd) / 6)
# same die, A' = {1,2,3}, B' = {2,4,6}: dependent?
Bev = [x for x in die if x % 2 == 0]
show("prac32b_PAB", len([x for x in die if x in Ad and x in Bev]) / 6)
show("prac32b_PA_PB", len(Ad) / 6 * len(Bev) / 6)

# 3.4 practice: two fair dice, A=1st odd, B=2nd odd, C=sum odd
d2 = [(i, j) for i in range(1, 7) for j in range(1, 7)]
Ao = [o for o in d2 if o[0] % 2 == 1]
Bo = [o for o in d2 if o[1] % 2 == 1]
Co = [o for o in d2 if (o[0] + o[1]) % 2 == 1]
show("prac34_PA", len(Ao) / 36)
show("prac34_PB", len(Bo) / 36)
show("prac34_PC", len(Co) / 36)
show("prac34_PAB", len([o for o in d2 if o in Ao and o in Bo]) / 36)
show("prac34_PAC", len([o for o in d2 if o in Ao and o in Co]) / 36)
show("prac34_PBC", len([o for o in d2 if o in Bo and o in Co]) / 36)
show("prac34_PABC", len([o for o in d2 if o in Ao and o in Bo and o in Co]) / 36)
show("prac34_PA_PB_PC", (1 / 2) ** 3)

# 3.5 practice: 4 steps
show("prac35_C42", comb(4, 2))
show("prac35_C31", comb(3, 1))
show("prac35_P_back0_after4", comb(4, 2) * pw ** 2 * (1 - pw) ** 2)
show("prac35_P_first_F_given_back0", comb(3, 1) / comb(4, 2))
show("prac35_P_plus2_after4", comb(4, 3) * pw ** 3 * (1 - pw))
show("prac35_P_plus4_after4", pw ** 4)

# 3.6 practice: 5-fold repetition of a 0, and posterior after receiving 110
show("prac36_rep5_err_e0", maj_err(5, e0))
show("prac36_rep3_err_e0", maj_err(3, e0))
show("prac36_gain_3to5", maj_err(3, e0) / maj_err(5, e0))
lik0_000 = (1 - e0) ** 3                  # sent 000, received 000
lik1_000 = e1 ** 3                        # sent 111, received 000
show("prac36_lik0_000", lik0_000)
show("prac36_lik1_000", lik1_000)
show("prac36_num_000", ps * lik0_000)
show("prac36_den_000", ps * lik0_000 + (1 - ps) * lik1_000)
show("prac36_P_0_given_000", ps * lik0_000 / (ps * lik0_000 + (1 - ps) * lik1_000))
# how large must the prior p be before 101 is decoded as 0?
show("prac36_prior_threshold_101", lik1 / (lik0 + lik1))

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(R, indent=1, default=str), encoding="utf-8")
print(f"\nwrote {out}  ({len(R)} keys)")
