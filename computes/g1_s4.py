# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Section 4 (Counting, L04 + rec04) — every number that appears in g1_s4.html.

Run:  uv run computes/g1_s4.py
Writes computes/g1_s4.json
"""
from __future__ import annotations
import json, sys
from fractions import Fraction
from math import comb, factorial, perm

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict = {}


def rec(key, val, note=""):
    R[key] = val
    print(f"{key:38s} = {val}   {note}")


print("=" * 78)
print("4.2  Basic counting principle")
print("=" * 78)
rec("stage_tree_leaves", 4 * 3 * 2, "n1*n2*n3 = 4*3*2 (L04 slide 3 figure)")
rec("plates_rep", 26 ** 3 * 10 ** 4, "26^3 * 10^4")
rec("plates_26cubed", 26 ** 3)
rec("plates_10k", 10 ** 4)
rec("plates_norep_letters", 26 * 25 * 24)
rec("plates_norep_digits", 10 * 9 * 8 * 7)
rec("plates_norep", 26 * 25 * 24 * 10 * 9 * 8 * 7)
rec("plates_ratio", round((26 * 25 * 24 * 10 * 9 * 8 * 7) / (26 ** 3 * 10 ** 4), 6))
rec("subsets_n3", 2 ** 3)
rec("fact_4", factorial(4))

print()
print("=" * 78)
print("4.3  Permutations / k-permutations — six rolls of a die all different")
print("=" * 78)
rec("die_fav", factorial(6), "6!")
rec("die_total", 6 ** 6, "6^6")
rec("die_prob", round(factorial(6) / 6 ** 6, 6))
rec("die_prob_frac", str(Fraction(factorial(6), 6 ** 6)))
rec("die_prob_pct", round(100 * factorial(6) / 6 ** 6, 3))
# stagewise product for the derivation
rec("die_stage_product", [round(x, 6) for x in
                          [6 / 6, 5 / 6, 4 / 6, 3 / 6, 2 / 6, 1 / 6]])
rec("kperm_7_3", perm(7, 3), "7!/(7-3)! = 7*6*5")

print()
print("=" * 78)
print("4.4  Combinations")
print("=" * 78)
rec("C_4_2", comb(4, 2))
rec("C_10_3", comb(10, 3))
rec("C_8_1", comb(8, 1))
rec("C_52_5", comb(52, 5))
rec("C_5_2", comb(5, 2))
rec("perm_5_2", perm(5, 2))
rec("fact_2", factorial(2))
pascal = [[comb(n, k) for k in range(n + 1)] for n in range(9)]
rec("pascal_rows_0_8", pascal)
rec("sum_C_5_k", sum(comb(5, k) for k in range(6)), "= 2^5")
rec("two_pow_5", 2 ** 5)
rec("sum_identity_check_n_0_12",
    all(sum(comb(n, k) for k in range(n + 1)) == 2 ** n for n in range(13)))

print()
print("=" * 78)
print("4.5  Binomial probabilities")
print("=" * 78)
p_ex = 0.5
rec("binom_seq_HTTHHH_heads", 4)
rec("binom_seq_HTTHHH_tails", 2)
rec("binom_10_3_count", comb(10, 3))
# conditional coin problem (L04 slide 7)
rec("coin_B_size", comb(10, 3))
rec("coin_HH_in_B", comb(8, 1))
rec("coin_cond_prob", round(comb(8, 1) / comb(10, 3), 6))
rec("coin_cond_frac", str(Fraction(comb(8, 1), comb(10, 3))))
# sanity: direct check by brute force over all 2^10 sequences with p arbitrary
import itertools

for p in (0.2, 0.5, 0.77):
    num = den = 0.0
    for s in itertools.product([1, 0], repeat=10):
        k = sum(s)
        if k != 3:
            continue
        w = p ** 3 * (1 - p) ** 7
        den += w
        if s[0] == 1 and s[1] == 1:
            num += w
    R.setdefault("coin_cond_bruteforce", {})[str(p)] = round(num / den, 9)
    print(f"  brute force p={p}: P(first two H | B) = {num/den:.9f}")
rec("coin_cond_bruteforce", R["coin_cond_bruteforce"], "independent of p -> uniform")
# binomial pmf table n=10 p=0.3 (practice)
rec("binom_10_0.3_k4", round(comb(10, 4) * 0.3 ** 4 * 0.7 ** 6, 6))
rec("C_10_4", comb(10, 4))
rec("binom_10_0.5_k5", round(comb(10, 5) * 0.5 ** 10, 6))
rec("C_10_5", comb(10, 5))

print()
print("=" * 78)
print("4.6  Partitions / multinomial — 52 cards to 4 players, each gets an ace")
print("=" * 78)
n_partitions = factorial(52) // (factorial(13) ** 4)
rec("cards_total_partitions", n_partitions, "52!/(13!)^4")
rec("cards_total_partitions_sci", f"{n_partitions:.6e}")
rec("cards_ace_ways", factorial(4), "4*3*2*1")
rem = factorial(48) // (factorial(12) ** 4)
rec("cards_remaining_partitions", rem, "48!/(12!)^4")
rec("cards_remaining_partitions_sci", f"{rem:.6e}")
ace_p = Fraction(factorial(4) * rem, n_partitions)
rec("cards_ace_prob", round(float(ace_p), 6))
rec("cards_ace_prob_frac", str(ace_p))
# closed form check 24 * 13^4 / (52*51*50*49)
alt = Fraction(24 * 13 ** 4, 52 * 51 * 50 * 49)
rec("cards_ace_prob_closedform", str(alt))
rec("cards_ace_prob_closedform_matches", alt == ace_p)
rec("cards_13pow4", 13 ** 4)
rec("cards_24_times_13pow4", 24 * 13 ** 4)
rec("cards_52x51x50x49", 52 * 51 * 50 * 49)
# multinomial coefficient examples
rec("multinom_MISSISSIPPI", factorial(11) // (factorial(1) * factorial(4) * factorial(4) * factorial(2)))
rec("fact_11", factorial(11))
rec("multinom_denom_MISSISSIPPI", factorial(1) * factorial(4) * factorial(4) * factorial(2))
rec("multinom_6_into_321", factorial(6) // (factorial(3) * factorial(2) * factorial(1)))
# multinomial probability example: 10 draws, p = (0.5,0.3,0.2), counts (5,3,2)
mn_coef = factorial(10) // (factorial(5) * factorial(3) * factorial(2))
rec("mnprob_coef", mn_coef)
rec("mnprob_value", round(mn_coef * 0.5 ** 5 * 0.3 ** 3 * 0.2 ** 2, 6))
# sanity: multinomial pmf sums to 1 over all compositions of n=10 into 3 parts
tot = 0.0
for a in range(11):
    for b in range(11 - a):
        c = 10 - a - b
        tot += factorial(10) // (factorial(a) * factorial(b) * factorial(c)) * 0.5 ** a * 0.3 ** b * 0.2 ** c
rec("mnprob_sums_to_one", round(tot, 12))

print()
print("=" * 78)
print("4.7  rec04 P1 — birthday problem")
print("=" * 78)


def p_distinct(n, D=365):
    if n > D:
        return 0.0
    x = 1.0
    for i in range(n):
        x *= (D - i) / D
    return x


bd = {n: p_distinct(n) for n in range(1, 101)}
tbl_ns = [5, 10, 15, 20, 22, 23, 24, 30, 40, 50, 57, 60, 70, 80]
rec("birthday_table", {str(n): round(bd[n], 6) for n in tbl_ns})
rec("birthday_collision_table", {str(n): round(1 - bd[n], 6) for n in tbl_ns})
first = min(n for n in bd if bd[n] < 0.5)
rec("birthday_first_n_collision_over_half", first)
rec("birthday_P22", round(bd[22], 6))
rec("birthday_P23", round(bd[23], 6))
rec("birthday_collision_23", round(1 - bd[23], 6))
rec("birthday_collision_22", round(1 - bd[22], 6))
rec("birthday_first_n_collision_over_99pct", min(n for n in bd if 1 - bd[n] > 0.99))
rec("birthday_P30", round(bd[30], 6))
rec("birthday_collision_30", round(1 - bd[30], 6))
rec("birthday_P50", round(bd[50], 6))
rec("birthday_collision_50", round(1 - bd[50], 6))
# exact rational for n=23
ex23 = Fraction(perm(365, 23), 365 ** 23)
rec("birthday_P23_exact_float", float(ex23))
# where log-scale curve hits 1e-10 (rec04 handout says n ~ 122)
n_1em10 = min(n for n in range(1, 200) if p_distinct(n) < 1e-10)
rec("birthday_n_at_1e-10", n_1em10, "handout log panel ends ~122")
rec("birthday_P122", f"{p_distinct(122):.4e}")
rec("birthday_P121", f"{p_distinct(121):.4e}")
# approximation check
import math

rec("birthday_approx_23", round(math.exp(-23 * 22 / (2 * 365)), 6), "exp(-n(n-1)/730)")
rec("birthday_n_star_approx", round(math.sqrt(2 * 365 * math.log(2)), 3), "sqrt(2D ln2)")

print()
print("=" * 78)
print("4.8  rec04 P2 — 8 non-attacking rooks")
print("=" * 78)
rec("rooks_fav_ordered_factors", [k ** 2 for k in range(8, 0, -1)])
fav_ord = 1
for k in range(8, 0, -1):
    fav_ord *= k ** 2
rec("rooks_fav_ordered", fav_ord, "(8!)^2")
rec("rooks_8fact_sq", factorial(8) ** 2)
rec("rooks_total_ordered", perm(64, 8), "64!/56!")
rooks_p = Fraction(fav_ord, perm(64, 8))
rec("rooks_prob", float(rooks_p))
rec("rooks_prob_sci", f"{float(rooks_p):.6e}")
rec("rooks_prob_frac", str(rooks_p))
rec("rooks_one_over", round(1 / float(rooks_p), 1))
# unordered view
rec("rooks_fav_unordered", factorial(8))
rec("rooks_total_unordered", comb(64, 8))
rec("rooks_prob_unordered", float(Fraction(factorial(8), comb(64, 8))))
rec("rooks_two_views_agree", Fraction(factorial(8), comb(64, 8)) == rooks_p)
# small case for practice: 3 non-attacking rooks on 4x4
rec("rooks_3_on_4x4_C43", comb(4, 3))
rec("rooks_3_on_4x4_fact3", factorial(3))
rec("rooks_3_on_4x4_fav", comb(4, 3) * comb(4, 3) * factorial(3), "C(4,3)^2 * 3!")
rec("rooks_3_on_4x4_total", comb(16, 3))
_r3 = Fraction(comb(4, 3) * comb(4, 3) * factorial(3), comb(16, 3))
rec("rooks_3_on_4x4_prob", round(float(_r3), 6))
rec("rooks_3_on_4x4_frac", str(_r3))

print()
print("=" * 78)
print("4.9  rec04 P3 — hypergeometric")
print("=" * 78)


def hyper(n, m, k, i):
    if i < 0 or i > m or i > k or k - i > n - m:
        return Fraction(0)
    return Fraction(comb(m, i) * comb(n - m, k - i), comb(n, k))


nH, mH, kH = 20, 8, 5
rec("hyper_params", {"n": nH, "m": mH, "k": kH})
rec("hyper_pmf", {str(i): round(float(hyper(nH, mH, kH, i)), 6) for i in range(0, kH + 1)})
rec("hyper_pmf_frac", {str(i): str(hyper(nH, mH, kH, i)) for i in range(0, kH + 1)})
rec("hyper_pmf_sums_to_one", float(sum(hyper(nH, mH, kH, i) for i in range(0, kH + 1))))
rec("hyper_mean", round(sum(i * float(hyper(nH, mH, kH, i)) for i in range(kH + 1)), 6))
rec("hyper_mean_formula", round(kH * mH / nH, 6), "k*m/n")
rec("hyper_C_20_5", comb(20, 5))
rec("hyper_C_8_2", comb(8, 2))
rec("hyper_C_12_3", comb(12, 3))
rec("hyper_i2_num", comb(8, 2) * comb(12, 3))
# Vandermonde sanity
rec("vandermonde_check", sum(comb(mH, i) * comb(nH - mH, kH - i) for i in range(0, kH + 1)) == comb(nH, kH))
# edge sanity: m = n (all red)
rec("hyper_all_red_i_eq_k", float(hyper(10, 10, 4, 4)))
rec("hyper_k_eq_n", float(hyper(10, 4, 10, 4)))
# practice: 5-card hand exactly 2 aces
rec("cards_2aces_num", comb(4, 2) * comb(48, 3))
rec("cards_C_48_3", comb(48, 3))
rec("cards_2aces_prob", round(comb(4, 2) * comb(48, 3) / comb(52, 5), 6))

print()
print("=" * 78)
print("Practice-question numbers")
print("=" * 78)
rec("pq_3dice_alldiff_fav", 6 * 5 * 4)
rec("pq_3dice_alldiff_total", 6 ** 3)
rec("pq_3dice_alldiff_prob", round(6 * 5 * 4 / 6 ** 3, 6))
rec("pq_3dice_alldiff_frac", str(Fraction(6 * 5 * 4, 6 ** 3)))
rec("pq_4letter_norep", perm(26, 4))
rec("pq_medals_12", perm(12, 3))
rec("pq_committee_C_12_5", comb(12, 5))
rec("pq_committee_chair", comb(12, 5) * 5)
rec("pq_binom_8_0.25_ge2",
    round(1 - (0.75 ** 8 + comb(8, 1) * 0.25 * 0.75 ** 7), 6))
rec("pq_binom_8_0.25_k0", round(0.75 ** 8, 6))
rec("pq_binom_8_0.25_k1", round(comb(8, 1) * 0.25 * 0.75 ** 7, 6))
rec("pq_teams_12_into_3fours", factorial(12) // (factorial(4) ** 3))
rec("pq_fact_12", factorial(12))
rec("pq_fact4_cubed", factorial(4) ** 3)
rec("pq_bd_month_12_n5", round(p_distinct(5, 12), 6))
rec("pq_bd_month_12_n5_collision", round(1 - p_distinct(5, 12), 6))
rec("pq_bd_month_first_half", min(n for n in range(1, 13) if p_distinct(n, 12) < 0.5))
rec("pq_hyper_defect_num", comb(3, 1) * comb(17, 3))
rec("pq_hyper_C_17_3", comb(17, 3))
rec("pq_hyper_C_20_4", comb(20, 4))
rec("pq_hyper_defect_prob", round(comb(3, 1) * comb(17, 3) / comb(20, 4), 6))

print()
print("=" * 78)
print("Extra numbers appearing in prose / practice solutions (added pass 2)")
print("=" * 78)
rec("two_dice_sum4", str(Fraction(3, 36)))
rec("two_dice_sum4_dec", round(3 / 36, 6))
rec("menu_meals", 4 * 6 * 5)
rec("menu_meals_nonempty", 4 * 6 * 5 - 1)
rec("seat5_adjacent_fav", factorial(4) * factorial(2))
rec("seat5_total", factorial(5))
rec("seat5_frac", str(Fraction(factorial(4) * factorial(2), factorial(5))))
rec("committee_chairfirst", 12 * comb(11, 4))
rec("C_11_4", comb(11, 4))
rec("C_7_3", comb(7, 3))
rec("C_7_4", comb(7, 4))
rec("C_8_4", comb(8, 4))
rec("pascal_rule_check", comb(7, 3) + comb(7, 4) == comb(8, 4))
rec("C_11_5", comb(11, 5))
rec("C_12_6", comb(12, 6))
rec("cond_head_first_of_12", str(Fraction(comb(11, 5), comb(12, 6))))
rec("p075_pow7", round(0.75 ** 7, 6))
rec("p03_pow4", 0.3 ** 4)
rec("p07_pow6", round(0.7 ** 6, 6))
rec("two_pow_10", 2 ** 10)
rec("teams_unlabeled_12_3x4", factorial(12) // (factorial(4) ** 3) // factorial(3))
rec("die12_eachface_twice_fav", factorial(12) // (factorial(2) ** 6))
rec("die12_total", 6 ** 12)
rec("die12_eachface_twice_prob", round(factorial(12) // (factorial(2) ** 6) / 6 ** 12, 6))
rec("fact2_pow6", factorial(2) ** 6)
rec("rooks_rowmodel_prob", round(factorial(8) / 8 ** 8, 6), "one rook per row, random column")
rec("rooks_rowmodel_ratio_to_main", round((factorial(8) / 8 ** 8) / float(rooks_p), 1))
rec("hyper_defect_binom_approx", round(comb(4, 1) * 0.15 * 0.85 ** 3, 6))
rec("hyper_defect_relerr_pct",
    round(100 * abs(comb(4, 1) * 0.15 * 0.85 ** 3 - comb(3, 1) * comb(17, 3) / comb(20, 4))
          / (comb(3, 1) * comb(17, 3) / comb(20, 4)), 1))
rec("pq_seat6", factorial(6))
rec("pq_pin5", 10 ** 5)
rec("pq_C_12_4", comb(12, 4))
rec("pq_deal9_3x3", factorial(9) // (factorial(3) ** 3))
rec("pq_fact_9", factorial(9))
rec("pq_fact3_cubed", factorial(3) ** 3)
rec("socks_total", comb(20, 4))
rec("socks_C_10_4", comb(10, 4))
rec("socks_fav_nopair", comb(10, 4) * 2 ** 4)
rec("socks_p_nopair", round(comb(10, 4) * 2 ** 4 / comb(20, 4), 6))
rec("socks_p_pair", round(1 - comb(10, 4) * 2 ** 4 / comb(20, 4), 6))
rec("C_23_2_pairs", comb(23, 2))
rec("multinom_triples_n10_r3", sum(1 for a in range(11) for b in range(11 - a)))
rec("multinom_6_321_seq_check", comb(6, 3) * comb(3, 2) * comb(1, 1))
rec("fact_9_over_216", factorial(9) // 216)

with open("d:/Python-UV/MIT_Applied_Prob/computes/g1_s4.json", "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1, default=str)
print("\nwrote computes/g1_s4.json")
