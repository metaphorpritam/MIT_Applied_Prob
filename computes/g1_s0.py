# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Numbers used in G1 section 0 (orientation / roadmap).

Every numeric value that appears in notes/src/fragments/g1_s0.html is produced
here. Sources: L01 slides 5, 8, 11; rec02 problem 4 (Monty Hall); rec04
problem 1 (birthday problem).
"""
import io
import json
import sys
from fractions import Fraction
from itertools import product

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

out = {}

# --- L01 slide 5/8: two rolls of a tetrahedral die, sample-space size ---------
omega = [(x, y) for x in range(1, 5) for y in range(1, 5)]
out["tetra_faces"] = 4
out["tetra_outcomes"] = len(omega)                       # 4 * 4
out["tetra_outcome_prob"] = str(Fraction(1, len(omega)))

# --- L01 slide 11: P(n) = 2^-n on {1,2,...}; P(outcome is even) --------------
# exact geometric sum: sum_{k>=1} (1/4)^k = (1/4)/(1 - 1/4)
r = Fraction(1, 4)
p_even_exact = r / (1 - r)
p_even_partial = sum(Fraction(1, 2) ** (2 * k) for k in range(1, 40))
out["p_even_exact"] = str(p_even_exact)                  # 1/3
out["p_even_decimal"] = round(float(p_even_exact), 6)
out["p_even_partial_40_terms"] = round(float(p_even_partial), 12)

# --- rec02 P4: Monty Hall, brute force over (car, initial pick) --------------
win_stay = 0
win_switch = 0
trials = 0
for car in (1, 2, 3):
    for pick in (1, 2, 3):
        trials += 1
        win_stay += (pick == car)
        # host opens a non-car, non-pick door; switching lands on the remaining
        # door, which is the car exactly when the initial pick was wrong
        win_switch += (pick != car)
out["monty_trials"] = trials
out["monty_p_stay"] = str(Fraction(win_stay, trials))
out["monty_p_switch"] = str(Fraction(win_switch, trials))

# --- rec04 P1: birthday problem, 23 people, 365 equally likely days ----------
n, days = 23, 365
p_all_distinct = 1.0
for i in range(n):
    p_all_distinct *= (days - i) / days
out["birthday_n"] = n
out["birthday_days"] = days
out["birthday_p_match"] = round(1 - p_all_distinct, 4)

# --- §0.1 practice: granularity of the two-roll model ------------------------
# coarse sample space of sums for two tetrahedral rolls: how many cells per sum
sum_counts = {}
for x, y in omega:
    sum_counts[x + y] = sum_counts.get(x + y, 0) + 1
out["sum_values"] = sorted(sum_counts)
out["sum_counts"] = [sum_counts[s] for s in sorted(sum_counts)]
out["sum_n_values"] = len(sum_counts)
out["sum_p_of_5"] = str(Fraction(sum_counts[5], len(omega)))
out["sum_uniform_would_give"] = str(Fraction(1, len(sum_counts)))

# --- §0.1 practice: 3-roll model, all rolls equal ----------------------------
omega3 = list(product(range(1, 5), repeat=3))
out["tetra3_outcomes"] = len(omega3)
out["tetra3_all_equal"] = sum(1 for t in omega3 if t[0] == t[1] == t[2])
out["tetra3_p_all_equal"] = str(
    Fraction(out["tetra3_all_equal"], len(omega3))
)
out["tetra3_exactly_two_equal"] = sum(
    1 for t in omega3 if len(set(t)) == 2
)
out["tetra3_all_different"] = sum(1 for t in omega3 if len(set(t)) == 3)
out["tetra3_p_exactly_two_equal"] = str(
    Fraction(out["tetra3_exactly_two_equal"], len(omega3))
)
out["tetra3_p_all_different"] = str(
    Fraction(out["tetra3_all_different"], len(omega3))
)

for k, v in out.items():
    print(f"{k:28s} = {v}")

with open("d:/Python-UV/MIT_Applied_Prob/computes/g1_s0.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
