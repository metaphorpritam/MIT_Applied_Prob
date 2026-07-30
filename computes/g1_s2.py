# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""All numbers used in note G1 section 2 (Conditioning, total probability, Bayes).

Sources: L02 slides 3-8, rec02 problems 1-4, Bertsekas-Tsitsiklis 1.3-1.4
Run:  uv run computes/g1_s2.py
"""
from __future__ import annotations
import itertools, json, sys, random
from fractions import Fraction as F
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = {}


def show(key, val, note=""):
    R[key] = val
    print(f"{key:38s} = {val}   {note}")


print("=" * 78)
print("2.1  Die roll example (L02 slide 4): 4-sided die rolled twice")
print("=" * 78)
omega = [(x, y) for x in range(1, 5) for y in range(1, 5)]
show("die_omega_size", len(omega))
B = [w for w in omega if min(w) == 2]
show("die_B_cells", [list(w) for w in B])
show("die_B_size", len(B))
show("die_P_B", str(F(len(B), len(omega))), f"= {len(B)/len(omega):.4f}")
for m in (1, 2, 3, 4):
    Am = [w for w in omega if max(w) == m]
    inter = [w for w in Am if w in B]
    show(f"die_M{m}_and_B_cells", [list(w) for w in inter])
    show(f"die_P_M{m}_given_B", str(F(len(inter), len(B))), f"= {len(inter)/len(B):.4f}")
    show(f"die_P_M{m}_uncond", str(F(len(Am), 16)), f"= {len(Am)/16:.4f}")
# practice: given max = 3, P(min = 1)
A3 = [w for w in omega if max(w) == 3]
mn1 = [w for w in A3 if min(w) == 1]
show("prac_max3_cells", len(A3))
show("prac_max3_min1_cells", [list(w) for w in mn1])
show("prac_P_min1_given_max3", str(F(len(mn1), len(A3))), f"= {len(mn1)/len(A3):.4f}")
# practice: given min <= 2, P(X = 1)
C = [w for w in omega if min(w) <= 2]
D = [w for w in C if w[0] == 1]
show("prac_min_le2_cells", len(C))
show("prac_min_le2_X1_cells", len(D))
show("prac_P_X1_given_min_le2", str(F(len(D), len(C))), f"= {len(D)/len(C):.4f}")

print()
print("=" * 78)
print("2.2  Alice's two-heads claim (rec02 P1 = text Problem 1.15)")
print("=" * 78)
four = ["HH", "HT", "TH", "TT"]
A = [w for w in four if w[0] == "H"]        # first toss head
Bev = [w for w in four if w[1] == "H"]      # second toss head
AB = [w for w in four if w in A and w in Bev]
AuB = sorted(set(A) | set(Bev))
show("alice_A", A); show("alice_B", Bev); show("alice_AandB", AB); show("alice_AorB", AuB)
show("alice_P_A", str(F(len(A), 4)), f"= {len(A)/4:.4f}")
show("alice_P_AB", str(F(len(AB), 4)), f"= {len(AB)/4:.4f}")
show("alice_P_AuB", str(F(len(AuB), 4)), f"= {len(AuB)/4:.4f}")
show("alice_fair_given_A", str(F(len(AB), len(A))), f"= {len(AB)/len(A):.6f}")
show("alice_fair_given_AuB", str(F(len(AB), len(AuB))), f"= {len(AB)/len(AuB):.6f}")
p = 0.6  # unfair coin, P(head) = p, tosses independent
show("alice_p_unfair", p)
show("alice_unfair_given_A", round(p, 6))
show("alice_unfair_given_AuB", round(p * p / (2 * p - p * p), 6), "= p/(2-p)")
show("alice_unfair_P_AB", round(p * p, 6))
show("alice_unfair_P_AuB", round(2 * p - p * p, 6))

print()
print("=" * 78)
print("2.3  Two fair 6-sided dice (rec02 P2 = text Problem 1.14)")
print("=" * 78)
om2 = [(i, j) for i in range(1, 7) for j in range(1, 7)]
show("dice_omega", len(om2))
dbl = [w for w in om2 if w[0] == w[1]]
show("dice_doubles_n", len(dbl))
show("dice_a_P_doubles", str(F(len(dbl), 36)), f"= {len(dbl)/36:.6f}")
S4 = [w for w in om2 if sum(w) <= 4]
show("dice_sum_le4_cells", [list(w) for w in sorted(S4)])
show("dice_sum_le4_n", len(S4))
d_in_S4 = [w for w in S4 if w[0] == w[1]]
show("dice_sum_le4_doubles", [list(w) for w in sorted(d_in_S4)])
show("dice_b_cond", str(F(len(d_in_S4), len(S4))), f"= {len(d_in_S4)/len(S4):.6f}")
six = [w for w in om2 if 6 in w]
show("dice_atleast_one6_n", len(six))
show("dice_c_P", str(F(len(six), 36)), f"= {len(six)/36:.6f}")
diff = [w for w in om2 if w[0] != w[1]]
show("dice_diff_n", len(diff), "= 36 - 6")
six_diff = [w for w in diff if 6 in w]
show("dice_six_and_diff_n", len(six_diff), "= 11 - 1")
show("dice_d_cond", str(F(len(six_diff), len(diff))), f"= {len(six_diff)/len(diff):.6f}")

print()
print("=" * 78)
print("2.4  Chess tournament (rec02 P3 = text Examples 1.13 / 1.17)")
print("=" * 78)
pri = {1: 0.5, 2: 0.25, 3: 0.25}
win = {1: 0.3, 2: 0.4, 3: 0.5}
terms = {i: pri[i] * win[i] for i in pri}
for i in pri:
    show(f"chess_joint_A{i}", round(terms[i], 6), f"= {pri[i]} * {win[i]}")
PB = sum(terms.values())
show("chess_P_win", round(PB, 6))
for i in pri:
    show(f"chess_post_A{i}", round(terms[i] / PB, 6))
show("chess_post_sum", round(sum(terms[i] / PB for i in pri), 6))
show("chess_P_lose", round(1 - PB, 6))
show("chess_post_A1_given_loss", round(pri[1] * (1 - win[1]) / (1 - PB), 6))

print()
print("=" * 78)
print("2.5  Radar / aircraft detection (L02 slide 5; text Example 1.16)")
print("=" * 78)
pA, pBA, pBAc = 0.05, 0.99, 0.10
show("radar_P_A", pA); show("radar_P_Ac", round(1 - pA, 6))
show("radar_P_B_given_A", pBA); show("radar_P_Bc_given_A", round(1 - pBA, 6))
show("radar_P_B_given_Ac", pBAc); show("radar_P_Bc_given_Ac", round(1 - pBAc, 6))
AB_ = pA * pBA
show("radar_P_A_and_B", round(AB_, 6))
show("radar_P_A_and_Bc", round(pA * (1 - pBA), 6))
AcB = (1 - pA) * pBAc
show("radar_P_Ac_and_B", round(AcB, 6))
show("radar_P_Ac_and_Bc", round((1 - pA) * (1 - pBAc), 6))
show("radar_leaf_sum", round(pA * pBA + pA * (1 - pBA) + (1 - pA) * pBAc + (1 - pA) * (1 - pBAc), 6))
PBr = AB_ + AcB
show("radar_P_B", round(PBr, 6))
show("radar_P_A_given_B", round(AB_ / PBr, 6))
show("radar_P_A_given_B_4dp", round(AB_ / PBr, 4))
show("radar_P_Ac_given_B", round(AcB / PBr, 6))
show("radar_P_A_given_Bc", round(pA * (1 - pBA) / (1 - PBr), 6))
show("radar_prior_odds", round(pA / (1 - pA), 6))
show("radar_LR", round(pBA / pBAc, 6))
show("radar_post_odds", round((pA / (1 - pA)) * (pBA / pBAc), 6))
show("radar_post_from_odds", round(((pA / (1 - pA)) * (pBA / pBAc)) / (1 + (pA / (1 - pA)) * (pBA / pBAc)), 6))
show("radar_boost_factor", round((AB_ / PBr) / pA, 4), "posterior / prior")
# indifference prior: what prior makes posterior = 0.5?
show("radar_prior_for_post_half", round(pBAc / (pBA + pBAc), 6), "solves p*.99=(1-p)*.10")

print()
print("=" * 78)
print("2.6  Bayes-explorer widget math check (posterior vs prior curve)")
print("=" * 78)


def post(pr, se, fa):
    den = pr * se + (1 - pr) * fa
    return pr * se / den, den


for pr in (0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.95):
    q, den = post(pr, 0.99, 0.10)
    show(f"widget_post_prior{pr}", round(q, 6), f"P(B)={den:.6f}")
show("widget_default_post", round(post(0.05, 0.99, 0.10)[0], 6))
show("widget_default_PB", round(post(0.05, 0.99, 0.10)[1], 6))
# monotone in prior?
xs = [i / 1000 for i in range(1, 1000)]
ys = [post(x, 0.99, 0.10)[0] for x in xs]
show("widget_monotone_increasing", all(b > a for a, b in zip(ys, ys[1:])))
show("widget_post_eq_prior_when_se_eq_fa", round(post(0.3, 0.4, 0.4)[0], 6), "uninformative test")

print()
print("=" * 78)
print("2.7  Monty Hall (rec02 P4 = text Example 1.12)")
print("=" * 78)
show("monty_P_stick", str(F(1, 3)), f"= {1/3:.6f}")
show("monty_P_switch", str(F(2, 3)), f"= {2/3:.6f}")
show("monty_c_host_always_2", str(F(2, 3)), f"= {2/3:.6f}", )
show("monty_c_host_random", str(F(1, 2)), f"= {1/2:.6f}")
show("monty_c_general", "(1/3)*(P(O2|P1,C1) + 1)")
# exhaustive enumeration with host randomizing 1/2 when free, you always pick door 1
tot = {"stick": F(0), "switch": F(0), "strategyC": F(0)}
for prize in (1, 2, 3):
    pp = F(1, 3)
    choice = 1
    opens = [d for d in (1, 2, 3) if d != choice and d != prize]
    for o in opens:
        po = pp * F(1, len(opens))
        other = [d for d in (1, 2, 3) if d != choice and d != o][0]
        tot["stick"] += po * (1 if choice == prize else 0)
        tot["switch"] += po * (1 if other == prize else 0)
        pick = choice if o == 2 else other       # strategy (c): switch only if door 3 opened
        tot["strategyC"] += po * (1 if pick == prize else 0)
show("monty_enum_stick", str(tot["stick"]), f"= {float(tot['stick']):.6f}")
show("monty_enum_switch", str(tot["switch"]), f"= {float(tot['switch']):.6f}")
show("monty_enum_strategyC_hostrandom", str(tot["strategyC"]), f"= {float(tot['strategyC']):.6f}")
# host always opens door 2 when he is free (prize behind 1)
tot2 = F(0)
for prize in (1, 2, 3):
    pp = F(1, 3)
    opens = [d for d in (1, 2, 3) if d != 1 and d != prize]
    o = 2 if 2 in opens else opens[0]
    other = [d for d in (1, 2, 3) if d != 1 and d != o][0]
    pick = 1 if o == 2 else other
    tot2 += pp * (1 if pick == prize else 0)
show("monty_enum_strategyC_host2", str(tot2), f"= {float(tot2):.6f}")
# simulation cross-check of widget logic
random.seed(6041)
N = 200000
ws = wk = 0
for _ in range(N):
    prize = random.randint(1, 3)
    choice = 1
    opts = [d for d in (1, 2, 3) if d != choice and d != prize]
    o = random.choice(opts)
    other = [d for d in (1, 2, 3) if d != choice and d != o][0]
    wk += (choice == prize)
    ws += (other == prize)
show("monty_sim_N", N)
show("monty_sim_stick_freq", round(wk / N, 5))
show("monty_sim_switch_freq", round(ws / N, 5))
# posterior on the prize location AFTER the host opens a door (demolishes 50-50)
# you chose door 1; host opens door 3.  q = P(O3 | P1 ∩ C1) complement handled below.
for q in (F(1, 2), F(1, 1)):
    # P(P1 ∩ C1 ∩ O3) = (1/3)(1-q_2) where q_2 = P(O2|P1∩C1) = q
    j1 = F(1, 3) * (1 - q)          # prize 1, host free, opens 3
    j2 = F(1, 3) * 1                # prize 2, host forced to open 3
    den = j1 + j2
    tag = "q_half" if q == F(1, 2) else "q_one"
    show(f"monty_post_P1_given_O3_{tag}", str(j1 / den) if den else "undef",
         f"= {float(j1/den):.6f}" if den else "")
    show(f"monty_post_P2_given_O3_{tag}", str(j2 / den) if den else "undef",
         f"= {float(j2/den):.6f}" if den else "")
# host opens door 2 instead, q = 1/2
qh = F(1, 2)
k1 = F(1, 3) * qh
k3 = F(1, 3) * 1
show("monty_post_P1_given_O2_q_half", str(k1 / (k1 + k3)), f"= {float(k1/(k1+k3)):.6f}")
show("monty_post_P3_given_O2_q_half", str(k3 / (k1 + k3)), f"= {float(k3/(k1+k3)):.6f}")
# 4-door practice variant
show("prac_monty4_stick", str(F(1, 4)), f"= {0.25:.6f}")
show("prac_monty4_switch", str(F(3, 4) * F(1, 2)), f"= {float(F(3,4)*F(1,2)):.6f}")

print()
print("=" * 78)
print("2.8  Practice-question numbers")
print("=" * 78)
# chain rule: urn 5 red 3 blue, draw 3 without replacement, all red
num = F(5, 8) * F(4, 7) * F(3, 6)
show("prac_urn_allred", str(num), f"= {float(num):.6f}")
show("prac_urn_f1", str(F(5, 8))); show("prac_urn_f2", str(F(4, 7))); show("prac_urn_f3", str(F(3, 6)))
# total probability: two machines
pm = {"old": 0.6, "new": 0.4}
pd = {"old": 0.03, "new": 0.01}
tp = sum(pm[k] * pd[k] for k in pm)
show("prac_mach_joint_old", round(pm["old"] * pd["old"], 6))
show("prac_mach_joint_new", round(pm["new"] * pd["new"], 6))
show("prac_mach_P_defect", round(tp, 6))
show("prac_mach_post_old", round(pm["old"] * pd["old"] / tp, 6))
# false-positive puzzle (text Example 1.18)
pdis, sens, spec = 0.001, 0.95, 0.95
jp = pdis * sens
jn = (1 - pdis) * (1 - spec)
show("prac_fp_joint_pos_disease", round(jp, 8))
show("prac_fp_joint_pos_healthy", round(jn, 8))
show("prac_fp_P_pos", round(jp + jn, 8))
show("prac_fp_post", round(jp / (jp + jn), 6))
# conditional-probability practice: 3 cards drawn, P(2nd red | 1st red) style
show("prac_alice_gen_check", "B subset C and A∩B = A∩C  =>  P(A|B) >= P(A|C)")
show("prac_mach_post_new", round(pm["new"] * pd["new"] / tp, 6))

print()
print("=" * 78)
print("2.9  Decimal forms quoted verbatim in the §2 prose (provenance)")
print("=" * 78)
# every rounded decimal that appears in the running text of the fragment, as a
# JSON-stored float so no value in the prose is hand-computed.
show("dec_die_P_B", round(len(B) / len(omega), 4))                  # 5/16, Ex 2.1 Step 1
show("dec_die_P_M2_uncond", round(3 / 16, 4))                       # Gotcha after Ex 2.1
show("dec_die_P_M4_uncond", round(7 / 16, 4))                       # Gotcha after Ex 2.1
show("dec_dice_P_doubles", round(len(dbl) / 36, 4))                 # Ex 2.2(a)
show("dec_dice_P_atleast_one6", round(len(six) / 36, 4))            # Ex 2.2(c)
show("dec_urn_allred", round(float(num), 6))                        # Practice 2.C
show("dec_radar_P_Bc", round(1 - PBr, 4))                           # Ex 2.5 Step 5 denominator
show("dec_mach_post_new", round(pm["new"] * pd["new"] / tp, 6))     # Practice 2.F check

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(R, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"\nwrote {out}  ({len(R)} values)")
