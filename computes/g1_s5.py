# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""G1 §5 — Synthesis / cheatsheet numbers.

Every numeric value quoted in notes/src/fragments/g1_s5.html is produced here.
Run:  uv run computes/g1_s5.py
"""
import io
import json
import sys
from fractions import Fraction
from math import comb, factorial, perm

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

R = {}


def rec(key, val, note=""):
    R[key] = {"value": val, "note": note}
    print(f"{key:38s} = {val}   {note}")


# ---------------------------------------------------------------- axioms / L01
# Uniform law on the 4x4 tetrahedral grid (L01 slide 8): 16 outcomes, each 1/16.
n_grid = 4 * 4
rec("grid.outcomes", n_grid, "L01 s8: two rolls of a tetrahedral die")
rec("grid.p_each", str(Fraction(1, n_grid)), "uniform law weight per outcome")
# P(min(X,Y)=2): cells with min exactly 2 -> (2,2),(2,3),(2,4),(3,2),(4,2)
minB = [(x, y) for x in range(1, 5) for y in range(1, 5) if min(x, y) == 2]
rec("grid.n_min2", len(minB), "cells with min(X,Y)=2")
rec("grid.P_min2", str(Fraction(len(minB), n_grid)), "= |B|/|Omega|")

# ------------------------------------------------------- conditional / Bayes L02
pA, pBgA, pBgAc = 0.05, 0.99, 0.10
pAc = 1 - pA
pAB = pA * pBgA
pAcB = pAc * pBgAc
pB = pAB + pAcB
pAgB = pAB / pB
rec("radar.P_A_and_B", round(pAB, 6), "0.05*0.99 (multiplication rule)")
rec("radar.P_Ac_and_B", round(pAcB, 6), "0.95*0.10")
rec("radar.P_B", round(pB, 6), "total probability theorem")
rec("radar.P_A_given_B", round(pAgB, 6), "Bayes' rule")
rec("radar.P_A_given_B_pct", round(100 * pAgB, 2), "percent")
rec("radar.prior_pct", round(100 * pA, 2), "prior percent")
rec("radar.bayes_factor", round(pA / pB, 6), "P(A)/P(B): shrinks 0.99 to the posterior")
rec("radar.factor_times_like", round(pBgA * pA / pB, 6), "0.99 * P(A)/P(B) = P(A|B) check")

# -------------------------------------------------------------- independence L03
# Pairwise-independent-but-not-independent triple (L03 slide 7).
rec("pw.P_A", str(Fraction(1, 2)), "first toss H")
rec("pw.P_C", str(Fraction(1, 2)), "same result on both tosses")
rec("pw.P_A_and_C", str(Fraction(1, 4)), "= P(A)P(C) -> pairwise independent")
rec("pw.P_ABC", str(Fraction(1, 4)), "A cap B cap C = {HH}")
rec("pw.P_A_P_B_P_C", str(Fraction(1, 2) ** 3), "product of the three marginals")

# Disjoint != independent, smallest counterexample: fair coin, A={H}, B={T}.
rec("dj.P_A", str(Fraction(1, 2)), "A = {H}")
rec("dj.P_B", str(Fraction(1, 2)), "B = {T}, disjoint from A")
rec("dj.P_A_and_B", str(Fraction(0, 1)), "A cap B empty")
rec("dj.P_A_times_P_B", str(Fraction(1, 4)), "product -> 0 != 1/4, so NOT independent")

# Conditioning destroys independence (L03 slide 5, two unfair coins).
p_coinA_H, p_coinB_H = 0.9, 0.1
p_toss_H = 0.5 * p_coinA_H + 0.5 * p_coinB_H
post_A_10H = (0.5 * p_coinA_H ** 10) / (0.5 * p_coinA_H ** 10 + 0.5 * p_coinB_H ** 10)
p11 = post_A_10H * p_coinA_H + (1 - post_A_10H) * p_coinB_H
rec("coins.P_toss_H", round(p_toss_H, 6), "0.5*0.9+0.5*0.1, total probability")
rec("coins.post_A_given_10H", round(post_A_10H, 10), "Bayes after 10 heads")
rec("coins.P_toss11_H_given_10H", round(p11, 6), "vs 0.5 unconditionally")

# Conditioning CREATES dependence (rec03 P1 / Example 1.20): two fair tosses,
# D = {results differ}. Enumerate the 4 equally likely outcomes.
om = ["HH", "HT", "TH", "TT"]
D = [w for w in om if w[0] != w[1]]
P_H1_D = Fraction(len([w for w in D if w[0] == "H"]), len(D))
P_H2_D = Fraction(len([w for w in D if w[1] == "H"]), len(D))
P_H1H2_D = Fraction(len([w for w in D if w == "HH"]), len(D))
rec("cd.P_H1_given_D", str(P_H1_D), "rec03 P1: P(H1|D)")
rec("cd.P_H2_given_D", str(P_H2_D), "rec03 P1: P(H2|D)")
rec("cd.P_H1H2_given_D", str(P_H1H2_D), "0: HH is not in D")
rec("cd.prod_given_D", str(P_H1_D * P_H2_D), "1/4 != 0 -> dependent given D")

# ------------------------------------------------------------------ counting L04
rec("cnt.plates_rep", 26 ** 3 * 10 ** 4, "26^3 * 10^4 license plates")
rec("cnt.plates_norep", 26 * 25 * 24 * 10 * 9 * 8 * 7, "no repetition")
rec("cnt.six_diff_num", factorial(6), "6! favorable orderings")
rec("cnt.six_diff_den", 6 ** 6, "6^6 outcomes")
rec("cnt.six_diff", round(factorial(6) / 6 ** 6, 6), "P(six rolls all different)")
rec("cnt.six_multisets", comb(6 + 6 - 1, 6),
    "C(11,6)=C(11,5): unordered multisets of six die rolls (Gotcha 5 mismatch)")
rec("cnt.six_mismatch", round(factorial(6) / comb(11, 6), 6), "720/462 > 1: not a probability")
rec("cnt.C10_3", comb(10, 3), "number of 3-head sequences in 10 tosses")
rec("cnt.C8_1", comb(8, 1), "3-head sequences starting HH")
rec("cnt.cond_first2H", str(Fraction(comb(8, 1), comb(10, 3))), "8/120 reduced")
rec("cnt.cond_first2H_dec", round(comb(8, 1) / comb(10, 3), 6), "decimal")

# Four-aces partition problem (L04 slide 8).
num = factorial(4) * factorial(48) // (factorial(12) ** 4)
den = factorial(52) // (factorial(13) ** 4)
rec("cards.P_each_ace", round(num / den, 6), "4!*(48!/12!^4) / (52!/13!^4)")

# Birthday problem (rec04 P1).
n_bd = 23
p_distinct = perm(365, n_bd) / 365 ** n_bd
rec("bday.n", n_bd, "people")
rec("bday.P_all_distinct", round(p_distinct, 6), "365!/(365-n)! / 365^n")
rec("bday.P_match", round(1 - p_distinct, 6), "> 1/2 already at n=23")

# Rooks (rec04 P2) and hypergeometric shape check (rec04 P3).
rooks = (factorial(8) ** 2) / (perm(64, 8))
rec("rooks.P_safe", f"{rooks:.6e}", "(8!)^2 / (64!/56!)")
n_h, m_h, k_h, i_h = 20, 8, 5, 2
hyp = comb(m_h, i_h) * comb(n_h - m_h, k_h - i_h) / comb(n_h, k_h)
rec("hyp.example", round(hyp, 6), "n=20,m=8,k=5,i=2: C(8,2)C(12,3)/C(20,5)")

# Binomial sanity: sum_k C(n,k) p^k q^(n-k) = 1  (validates the cheatsheet row).
n_b, p_b = 10, 0.3
tot = sum(comb(n_b, k) * p_b ** k * (1 - p_b) ** (n_b - k) for k in range(n_b + 1))
rec("binom.normalization_check", round(tot, 12), "must be 1.0")
rec("binom.subset_identity", 2 ** n_b == sum(comb(n_b, k) for k in range(n_b + 1)),
    "sum_k C(n,k) = 2^n")

# King's sibling (L03 slide 8), both readings.
rec("king.P_female_atleast1boy", str(Fraction(2, 3)), "condition on >=1 boy")
rec("king.P_female_randomchild", str(Fraction(1, 2)), "condition on a tagged child")

# ---------------------------------------------- extra calibration-table rows
# Monty Hall (rec02 P4 / Example 1.12): stick vs switch.
rec("monty.P_stick", str(Fraction(1, 3)), "win iff first guess was right")
rec("monty.P_switch", str(Fraction(2, 3)), "win iff first guess was wrong")

# Chess tournament (L02 s7, s8): opponent types 1,2,3 with priors .5,.25,.25.
chess_prior = [Fraction(1, 2), Fraction(1, 4), Fraction(1, 4)]
chess_like = [Fraction(3, 10), Fraction(2, 5), Fraction(1, 2)]
chess_win = sum(p * q for p, q in zip(chess_prior, chess_like))
chess_t1 = chess_prior[0] * chess_like[0] / chess_win
rec("chess.P_win", float(chess_win), "0.5*0.3+0.25*0.4+0.25*0.5, total probability")
rec("chess.P_type1_given_win", float(chess_t1), "Bayes: 0.15/0.375")

# Romeo & Juliet (rec01 P4): continuous uniform on [0,1]^2, w = 15 min = 1/4.
w_rj = Fraction(1, 4)
rj = 1 - (1 - w_rj) ** 2
rec("romeo.P_meet", str(rj), "1-(1-w)^2 with w=1/4")
rec("romeo.P_meet_dec", float(rj), "decimal")

# Loaded die (rec01 P3): P(even face) = 2*P(odd face), 9c = 1.
c_die = Fraction(1, 9)
rec("die.c", str(c_die), "normalization 3c+3(2c)=9c=1")
rec("die.P_123", str(c_die + 2 * c_die + c_die), "c+2c+c = 4c")
rec("die.P_123_dec", round(float(4 * c_die), 6), "decimal")

# ----------------------------------------------------- §5 practice problems
# P5.1 two urns, 3 draws without replacement, exactly 2 red -> which urn?
L1 = Fraction(comb(6, 2) * comb(4, 1), comb(10, 3))
L2 = Fraction(comb(3, 2) * comb(7, 1), comb(10, 3))
p51_B = Fraction(1, 2) * L1 + Fraction(1, 2) * L2
p51_post = Fraction(1, 2) * L1 / p51_B
rec("p51.like_box1", str(L1), "C(6,2)C(4,1)/C(10,3)")
rec("p51.like_box2", str(L2), "C(3,2)C(7,1)/C(10,3)")
rec("p51.P_two_red", str(p51_B), "total probability over the two boxes")
rec("p51.P_two_red_dec", float(p51_B), "decimal")
rec("p51.P_box1_given", str(p51_post), "Bayes' rule")
rec("p51.P_box1_given_dec", round(float(p51_post), 6), "decimal")

# P5.2 roll a fair die -> N, then toss a fair coin N times; P(exactly 2 heads).
terms52 = {n: Fraction(1, 6) * Fraction(comb(n, 2), 2 ** n) for n in range(1, 7)}
p52 = sum(terms52.values())
for n in range(2, 7):
    rec(f"p52.term_n{n}", str(Fraction(comb(n, 2), 2 ** n)), f"C({n},2)/2^{n} = P(2 H | N={n})")
rec("p52.P_two_heads", str(p52), "sum_n (1/6) C(n,2) 2^-n")
rec("p52.P_two_heads_dec", float(p52), "decimal")
p52_post = terms52[2] / p52
rec("p52.P_N2_given_2H", str(p52_post), "Bayes: which N did I roll?")
rec("p52.P_N2_given_2H_dec", round(float(p52_post), 6), "decimal")

# P5.3 10 fair tosses, condition on exactly 3 heads: are H1, H2 independent?
p53_1 = Fraction(comb(9, 2), comb(10, 3))
p53_12 = Fraction(comb(8, 1), comb(10, 3))
rec("p53.P_H1_given_B", str(p53_1), "C(9,2)/C(10,3), conditional uniform law")
rec("p53.P_H1_given_B_dec", float(p53_1), "decimal")
rec("p53.P_H1H2_given_B", str(p53_12), "C(8,1)/C(10,3)")
rec("p53.P_H1H2_given_B_dec", round(float(p53_12), 6), "decimal")
rec("p53.product", str(p53_1 * p53_1), "P(H1|B)P(H2|B) = 0.09 != 1/15 -> dependent")
rec("p53.product_dec", float(p53_1 * p53_1), "decimal")
rec("p53.P_H2_given_H1B", str(p53_12 / p53_1), "2/9: budget of 3 heads is now short one")

# P5.4 committee of 5 from 6 women + 4 men.
p54_all_w = Fraction(comb(6, 5), comb(10, 5))
p54_atleast1m = 1 - p54_all_w
p54_n_B = comb(10, 5) - comb(6, 5)
p54_cond = Fraction(comb(6, 3) * comb(4, 2), p54_n_B)
rec("p54.total", comb(10, 5), "C(10,5) committees")
rec("p54.P_all_women", str(p54_all_w), "C(6,5)/C(10,5)")
rec("p54.P_atleast_one_man", str(p54_atleast1m), "complement rule")
rec("p54.P_atleast_one_man_dec", round(float(p54_atleast1m), 6), "decimal")
rec("p54.n_exactly2men", comb(6, 3) * comb(4, 2), "C(6,3)C(4,2)")
rec("p54.n_B", p54_n_B, "committees with at least one man")
rec("p54.P_2men_given", str(p54_cond), "conditional uniform law: recount inside B")
rec("p54.P_2men_given_dec", round(float(p54_cond), 6), "decimal")
p54_uncond = Fraction(comb(6, 3) * comb(4, 2), comb(10, 5))
rec("p54.P_2men_uncond", str(p54_uncond), "120/252 = 10/21, for comparison")
rec("p54.P_2men_uncond_dec", round(float(p54_uncond), 6), "decimal")

# P5.5 twelve rolls of a fair die.
p55_num = factorial(12) // (factorial(2) ** 6)
p55_a = p55_num / 6 ** 12
p55_b = comb(12, 2) * (1 / 6) ** 2 * (5 / 6) ** 10
rec("p55.multinom_count", p55_num, "12!/(2!)^6 arrangements with each face twice")
rec("p55.den", 6 ** 12, "6^12 ordered outcomes")
rec("p55.P_each_face_twice", round(p55_a, 6), "multinomial probability")
rec("p55.P_six_exactly_twice", round(p55_b, 6), "binomial C(12,2)(1/6)^2(5/6)^10")
rec("p55.ratio", round(p55_b / p55_a, 1), "(b)/(a): how far below the product of marginals (a) sits")
rec("p51.likelihood_ratio", round(float(L1 / L2), 6), "20/7 = 2.857...")

with open("d:/Python-UV/MIT_Applied_Prob/computes/g1_s5.json", "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1, default=str)
print("\nwrote computes/g1_s5.json  (%d values)" % len(R))
