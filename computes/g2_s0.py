# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Numbers used in G2 section 0 (orientation: from outcomes to numbers).

Every numeric value printed in notes/src/fragments/g2_s0.html is produced here.
Sources: L05 slides 2-4, 6 (random variable as a function, PMF recipe,
expectation); L06 slide 2 (review); L07 slide 1 (multiple r.v.'s).

Running example: two independent tosses of a fair coin, with three different
random variables defined on the SAME sample space (L05 slide 2: "Can have
several random variables defined on the same sample space").
"""
import io
import json
import sys
from fractions import Fraction
from itertools import product

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

out = {}

# --- running example: two independent tosses of a fair coin ------------------
omega = ["".join(t) for t in product("HT", repeat=2)]     # HH, HT, TH, TT
p_omega = Fraction(1, len(omega))                          # equally likely
out["coin_outcomes"] = omega
out["coin_n_outcomes"] = len(omega)
out["coin_outcome_prob"] = str(p_omega)

# three random variables on the same sample space
X = {w: w.count("H") for w in omega}                       # number of heads
Y = {w: (1 if w[0] == "H" else 0) for w in omega}          # indicator: 1st toss H
Z = {w: (1 if w[0] == w[1] else 0) for w in omega}         # indicator: tosses match
out["X_values"] = X
out["Y_values"] = Y
out["Z_values"] = Z


def pmf(V):
    """PMF of a r.v. given as an outcome->value dict, by the L05 slide 4 recipe:
    collect all outcomes with V(omega)=v, add their probabilities."""
    d = {}
    for w, v in V.items():
        d[v] = d.get(v, Fraction(0)) + p_omega
    return dict(sorted(d.items()))


def expectation(V):
    return sum(Fraction(v) * p for v, p in pmf(V).items())


def variance(V):
    m = expectation(V)
    return sum((Fraction(v) - m) ** 2 * p for v, p in pmf(V).items())


for name, V in (("X", X), ("Y", Y), ("Z", Z)):
    out[f"pmf_{name}"] = {str(v): str(p) for v, p in pmf(V).items()}
    out[f"pmf_{name}_sum"] = str(sum(pmf(V).values()))     # must be 1
    out[f"E_{name}"] = str(expectation(V))
    out[f"var_{name}"] = str(variance(V))

# X and Y are different functions but here happen to share nothing: check that
# knowing Y does not determine X (motivates conditional PMFs, section 4)
out["outcomes_with_X_eq_1"] = sorted(w for w in omega if X[w] == 1)

# --- section-1 hook: L05 slide 4, X = min(F,S), two fair tetrahedral dice ----
tetra = [(f, s) for f in range(1, 5) for s in range(1, 5)]
n_min2 = sum(1 for (f, s) in tetra if min(f, s) == 2)
out["tetra_outcomes"] = len(tetra)
out["tetra_count_min_eq_2"] = n_min2
out["tetra_p_min_eq_2"] = str(Fraction(n_min2, len(tetra)))

for k, v in out.items():
    print(f"{k:22s} = {v}")

with open("d:/Python-UV/MIT_Applied_Prob/computes/g2_s0.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
