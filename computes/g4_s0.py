# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Numbers used in G4 section 0 (orientation: iterated expectations & arrival processes).

Every numeric value printed in notes/src/fragments/g4_s0.html is produced here.

Sources
-------
L12 slides 2-5  (conditional expectation as a r.v.; two-section quiz-score example)
L13 slides 2-6  (Bernoulli process; random processes as families of r.v.'s)
L14 slides 4, 7 (Poisson pmf; the Bernoulli <-> Poisson correspondence table)
L15 slide 2     (Poisson review: E[N_tau] = var(N_tau) = lambda*tau)
B&T 4.3, 4.5, 6.1, 6.2

Three quantitative threads:
 (A) the two-section quiz-score teaser (L12 slides 4-5): E[X|Y] and var(X|Y) as
     random variables, and the law-of-total-variance split of var(X);
 (B) the Bernoulli -> Poisson discretization limit (L14 slide 7): Binomial(n,
     lambda*t/n) -> Poisson(lambda*t), checked numerically at lambda*t = 2.5;
 (C) the matching moment/interarrival correspondence: geometric slot count times
     slot width -> exponential mean, i.e. delta/p = 1/lambda.
"""
import io
import json
import sys
from fractions import Fraction

import numpy as np
from scipy.stats import binom, poisson

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
OUT = {}


def show(key, val, label):
    OUT[key] = val
    print(f"{label:<58} = {val}")


print("=" * 74)
print("(A) L12 slides 4-5 -- two sections, quiz scores")
print("=" * 74)

# Model (the [DERIVATION GAP] on L12 slide 4): pick ONE student uniformly at
# random out of 30.  X = that student's score, Y = that student's section.
n1, n2 = 10, 20                      # students in section y=1 and y=2
n_tot = n1 + n2
m1, m2 = 90, 60                      # section sample means  (L12 slide 4)
v1, v2 = 10, 20                      # section sample variances (L12 slide 5)

pY1 = Fraction(n1, n_tot)
pY2 = Fraction(n2, n_tot)
show("pY1", str(pY1), "P(Y=1) = 10/30")
show("pY2", str(pY2), "P(Y=2) = 20/30")

EX = Fraction(m1 * n1 + m2 * n2, n_tot)
show("EX", float(EX), "E[X] = (90*10 + 60*20)/30")

# E[X|Y] is a random variable: value m1 w.p. pY1, m2 w.p. pY2.
EEXY = pY1 * m1 + pY2 * m2
show("E_of_EXY", float(EEXY), "E[E[X|Y]] = (1/3)(90) + (2/3)(60)")
print(f"    iterated-expectations check  E[E[X|Y]] == E[X] : {EEXY == EX}")
OUT["iterated_check"] = bool(EEXY == EX)

var_EXY = pY1 * (m1 - EX) ** 2 + pY2 * (m2 - EX) ** 2
show("var_EXY", float(var_EXY), "var(E[X|Y]) = (1/3)(90-70)^2 + (2/3)(60-70)^2")

E_varXY = pY1 * v1 + pY2 * v2
show("E_varXY_frac", str(E_varXY), "E[var(X|Y)] = (1/3)(10) + (2/3)(20)  [exact]")
show("E_varXY", round(float(E_varXY), 4), "E[var(X|Y)]  (decimal)")

varX = E_varXY + var_EXY
show("varX_frac", str(varX), "var(X) = E[var(X|Y)] + var(E[X|Y])  [exact]")
show("varX", round(float(varX), 4), "var(X)  (decimal)")
show("within_share", round(float(E_varXY / varX), 4), "within-section share of var(X)")
show("between_share", round(float(var_EXY / varX), 4), "between-section share of var(X)")

print("\n" + "=" * 74)
print("(B) L14 slide 7 -- Bernoulli -> Poisson: Binomial(n, lam*t/n) -> Poisson(lam*t)")
print("=" * 74)

lam, t = 5.0, 0.5                    # L14 slide 5: 5 emails/hour, half-hour window
lt = lam * t
show("lam", lam, "lambda (messages per hour)")
show("t", t, "t (hours)")
show("lam_t", lt, "lambda*t")

pois0 = poisson.pmf(0, lt)
pois1 = poisson.pmf(1, lt)
show("pois0", round(float(pois0), 6), "Poisson P(0 arrivals in t) = e^{-2.5}")
show("pois1", round(float(pois1), 6), "Poisson P(1 arrival  in t) = 2.5 e^{-2.5}")

rows = []
for n in (5, 25, 250, 2500):
    p = lt / n                       # p = lambda*delta with delta = t/n
    b0 = float(binom.pmf(0, n, p))
    b1 = float(binom.pmf(1, n, p))
    rows.append({"n": n, "delta_hours": round(t / n, 6), "p": round(p, 6),
                 "binom0": round(b0, 6), "binom1": round(b1, 6),
                 "err0": round(abs(b0 - float(pois0)), 6),
                 "err1": round(abs(b1 - float(pois1)), 6)})
    print(f"  n={n:<6} delta={t/n:<10.6f} p={p:<9.6f} "
          f"P(0)={b0:.6f} (err {abs(b0-pois0):.6f})  "
          f"P(1)={b1:.6f} (err {abs(b1-pois1):.6f})")
OUT["binom_to_poisson"] = rows

# moments match in the limit too
for n in (5, 250):
    p = lt / n
    print(f"  n={n:<6} binomial mean np = {n*p:.4f}, var np(1-p) = {n*p*(1-p):.6f}"
          f"   -> Poisson mean = var = {lt}")
OUT["binom_var_n5"] = round(5 * (lt / 5) * (1 - lt / 5), 6)
OUT["binom_var_n250"] = round(250 * (lt / 250) * (1 - lt / 250), 6)

print("\n" + "=" * 74)
print("(C) interarrival correspondence: geometric slots -> exponential time")
print("=" * 74)

lam2 = 0.6                           # L15 slide 3 fishing rate, per hour
delta = 1.0 / 60                     # one-minute slots
p2 = lam2 * delta
show("lam2", lam2, "lambda (catches per hour)")
show("delta_min", 1.0, "slot width delta (minutes)")
show("p2", round(p2, 6), "p = lambda*delta (success prob. per slot)")
show("geo_mean_slots", round(1 / p2, 4), "E[T1] in slots = 1/p")
show("geo_mean_hours", round(delta / p2, 6), "E[T1] in hours = delta/p")
show("exp_mean_hours", round(1 / lam2, 6), "exponential mean 1/lambda (hours)")
print(f"    match: delta/p == 1/lambda : {abs(delta / p2 - 1 / lam2) < 1e-12}")
OUT["interarrival_match"] = bool(abs(delta / p2 - 1 / lam2) < 1e-12)

# variance also matches: geometric var (1-p)/p^2 slots -> delta^2(1-p)/p^2 hours^2
gv = (1 - p2) / p2 ** 2 * delta ** 2
show("geo_var_hours2", round(gv, 6), "geometric var in hours^2 = delta^2 (1-p)/p^2")
show("exp_var_hours2", round(1 / lam2 ** 2, 6), "exponential var 1/lambda^2 (hours^2)")

with open("d:/Python-UV/MIT_Applied_Prob/computes/g4_s0.json", "w", encoding="utf-8") as f:
    json.dump(OUT, f, indent=1)
print("\nwrote computes/g4_s0.json")
