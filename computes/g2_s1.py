# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""Every number quoted in notes/src/fragments/g2_s1.html (L05 slides 2-5, named PMFs).

Run:  uv run computes/g2_s1.py
Writes computes/g2_s1.json.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict = {}


def show(key, val, note=""):
    R[key] = val
    print(f"{key:44s} = {val}   {note}")


print("=" * 78)
print("A. Two rolls of a fair tetrahedral die  (L05 slide 4)")
print("=" * 78)

OMEGA = list(itertools.product([1, 2, 3, 4], repeat=2))
show("omega_size", len(OMEGA))
show("p_each", str(F(1, len(OMEGA))))

# --- X = min(F,S) --------------------------------------------------------
min_cells = {k: [w for w in OMEGA if min(w) == k] for k in range(1, 5)}
show("min_eq_2_outcomes", [list(w) for w in min_cells[2]])
show("min_eq_2_count", len(min_cells[2]))
pmf_min = {k: F(len(v), 16) for k, v in min_cells.items()}
show("pmf_min_frac", {k: str(v) for k, v in pmf_min.items()})
show("pmf_min_dec", {k: round(float(v), 6) for k, v in pmf_min.items()})
show("pmf_min_sum", str(sum(pmf_min.values())))
# closed form 9-2k, and via the tail-count identity (5-k)^2-(4-k)^2
show("min_closed_form_check",
     all(len(min_cells[k]) == 9 - 2 * k == (5 - k) ** 2 - (4 - k) ** 2 for k in range(1, 5)))
show("min_ge_k_counts", {k: sum(1 for w in OMEGA if min(w) >= k) for k in range(1, 6)})

# --- M = max(F,S)  (practice; book Fig. 2.2) ------------------------------
max_cells = {k: [w for w in OMEGA if max(w) == k] for k in range(1, 5)}
pmf_max = {k: F(len(v), 16) for k, v in max_cells.items()}
show("pmf_max_counts", {k: len(v) for k, v in max_cells.items()})
show("pmf_max_frac", {k: str(v) for k, v in pmf_max.items()})
show("pmf_max_sum", str(sum(pmf_max.values())))
show("max_eq_2_outcomes", [list(w) for w in max_cells[2]])
show("max_closed_form_check", all(len(max_cells[k]) == 2 * k - 1 for k in range(1, 5)))

# --- D = |F-S| (practice) -------------------------------------------------
d_cells = {k: [w for w in OMEGA if abs(w[0] - w[1]) == k] for k in range(0, 4)}
pmf_d = {k: F(len(v), 16) for k, v in d_cells.items()}
show("pmf_d_counts", {k: len(v) for k, v in d_cells.items()})
show("pmf_d_frac", {k: str(v) for k, v in pmf_d.items()})
show("pmf_d_sum", str(sum(pmf_d.values())))

# --- S = F + S (used in prose) -------------------------------------------
show("pmf_sum_counts", {s: sum(1 for w in OMEGA if sum(w) == s) for s in range(2, 9)})

print()
print("=" * 78)
print("B. Binomial  (L05 slide 5)")
print("=" * 78)

# n=4 exact enumeration of the sequences with exactly 2 heads
seqs4 = ["".join(s) for s in itertools.product("HT", repeat=4)]
two_head_seqs = [s for s in seqs4 if s.count("H") == 2]
show("n4_total_sequences", len(seqs4))
show("n4_k2_sequences", two_head_seqs)
show("n4_k2_count", len(two_head_seqs))
show("C_4_2", math.comb(4, 2))


def binom_pmf(n, p, k):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


for p in (0.5, 0.6, 0.3):
    show(f"binom_n4_k2_p{p}", round(binom_pmf(4, 2, 0) if False else binom_pmf(4, p, 2), 6),
         f"= 6*{p}^2*{round(1-p,2)}^2")

# normalization checks
for (n, p) in [(4, 0.5), (4, 0.6), (10, 0.35), (12, 0.2), (25, 0.5)]:
    tot = sum(binom_pmf(n, p, k) for k in range(n + 1))
    show(f"binom_norm_n{n}_p{p}", round(tot, 12))

show("binom_n10_p035_table",
     {k: round(binom_pmf(10, 0.35, k), 6) for k in range(11)})
show("binom_n5_p03_k2", round(binom_pmf(5, 0.3, 2), 6))
show("binom_n5_p03_k2_parts",
     {"C(5,2)": math.comb(5, 2), "p^2": round(0.3 ** 2, 6), "(1-p)^3": round(0.7 ** 3, 6),
      "product_term": round(0.3 ** 2 * 0.7 ** 3, 6)})
show("binom_n3_p05_table", {k: str(F(math.comb(3, k), 8)) for k in range(4)})

# mean/variance of binomial verified numerically (derivation deferred to s2/s3)
for (n, p) in [(10, 0.35), (4, 0.5), (20, 0.7)]:
    ks = np.arange(n + 1)
    pk = np.array([binom_pmf(n, p, int(k)) for k in ks])
    m = float((ks * pk).sum())
    v = float(((ks - m) ** 2 * pk).sum())
    show(f"binom_mean_n{n}_p{p}", (round(m, 8), round(n * p, 8)))
    show(f"binom_var_n{n}_p{p}", (round(v, 8), round(n * p * (1 - p), 8)))

print()
print("=" * 78)
print("C. Geometric  (L05 slide 3)")
print("=" * 78)


def geom_pmf(p, k):
    return (1 - p) ** (k - 1) * p


show("geom_p03_table", {k: round(geom_pmf(0.3, k), 6) for k in range(1, 9)})
show("geom_p03_partial_sums",
     {K: round(sum(geom_pmf(0.3, k) for k in range(1, K + 1)), 6) for K in (1, 2, 3, 5, 10, 20, 50)})
for p in (0.3, 0.5, 0.1):
    tot = sum(geom_pmf(p, k) for k in range(1, 20000))
    show(f"geom_norm_p{p}", round(tot, 12))
    show(f"geom_tail_p{p}_k3",
         (round(sum(geom_pmf(p, k) for k in range(4, 20000)), 8), round((1 - p) ** 3, 8)))

# geometric series partial-sum identity used in the normalization derivation
q = 0.7
show("geom_series_partial_N10_q0.7",
     (round(sum(q ** i for i in range(10)), 8), round((1 - q ** 10) / (1 - q), 8)))
show("geom_series_limit_q0.7", (round(1 / (1 - q), 8), round(1 / 0.3, 8)))

for p in (0.3, 0.5, 0.2):
    ks = np.arange(1, 200000)
    pk = (1 - p) ** (ks - 1) * p
    m = float((ks * pk).sum())
    v = float(((ks - m) ** 2 * pk).sum())
    show(f"geom_mean_p{p}", (round(m, 6), round(1 / p, 6)))
    show(f"geom_var_p{p}", (round(v, 6), round((1 - p) / p ** 2, 6)))

# truncated geometric practice problem: at most 3 tosses, X = number of tosses made
p = 0.4
trunc = {1: p, 2: (1 - p) * p, 3: (1 - p) ** 2}
show("trunc_geom_p04", {k: round(v, 6) for k, v in trunc.items()})
show("trunc_geom_p04_sum", round(sum(trunc.values()), 12))

print()
print("=" * 78)
print("D. Bernoulli and discrete uniform")
print("=" * 78)

for p in (0.5, 0.3):
    ks = np.array([0, 1])
    pk = np.array([1 - p, p])
    m = float((ks * pk).sum())
    v = float(((ks - m) ** 2 * pk).sum())
    show(f"bern_mean_p{p}", (round(m, 8), round(p, 8)))
    show(f"bern_var_p{p}", (round(v, 8), round(p * (1 - p), 8)))

for (a, b) in [(0, 5), (1, 4), (0, 9), (3, 7)]:
    ks = np.arange(a, b + 1)
    n = len(ks)
    pk = np.full(n, 1.0 / n)
    m = float((ks * pk).sum())
    v = float(((ks - m) ** 2 * pk).sum())
    show(f"unif_{a}_{b}_mass", (n, round(1.0 / n, 8)))
    show(f"unif_{a}_{b}_mean", (round(m, 8), round((a + b) / 2, 8)))
    show(f"unif_{a}_{b}_var", (round(v, 8), round((n * n - 1) / 12, 8)))

print()
print("=" * 78)
print("E. Widget arithmetic check (w-g2s1-pmf): JS formulas replicated here")
print("=" * 78)
# The widget computes binomial pmf by the multiplicative recursion
#   p_0 = (1-p)^n,  p_k = p_{k-1} * (n-k+1)/k * p/(1-p)
# Check it against math.comb for a grid of (n,p).
worst = 0.0
for n in range(1, 41):
    for p in [0.01, 0.05, 0.2, 0.35, 0.5, 0.66, 0.9, 0.99]:
        pk = (1 - p) ** n
        for k in range(0, n + 1):
            if k > 0:
                pk = pk * (n - k + 1) / k * p / (1 - p)
            worst = max(worst, abs(pk - binom_pmf(n, p, k)))
show("widget_binom_recursion_max_abs_err", f"{worst:.3e}")

# geometric truncation used for the widget display window: show k=1..K with K chosen
# so the displayed mass covers >= 0.999 of the distribution.
for p in (0.05, 0.1, 0.3, 0.5):
    K = math.ceil(math.log(0.001) / math.log(1 - p))
    show(f"widget_geom_window_p{p}", (K, round(1 - (1 - p) ** K, 6)))

cross = max(p for p in [i/1000 for i in range(20, 951)]
            if math.ceil(math.log(0.001) / math.log(1 - p)) > 60)
show("widget_geom_cap60_crossover_p", cross)
show("widget_geom_p005_mass_at_60", round(1 - 0.95 ** 60, 6))

show("widget_readout_examples", {
    "binomial n=10 p=0.35": {"mean": round(10 * 0.35, 4), "var": round(10 * 0.35 * 0.65, 4)},
    "geometric p=0.30": {"mean": round(1 / 0.3, 4), "var": round(0.7 / 0.09, 4)},
    "uniform 0..5": {"mean": 2.5, "var": round((36 - 1) / 12, 4)},
})

print()
print("=" * 78)
print("F. Numbers quoted inside practice solutions")
print("=" * 78)

# Practice 1.10 : binomial n=10 p=0.35, P(X>=1)
show("p110_binom_p0", round(0.65 ** 10, 6))
show("p110_binom_atleast1", round(1 - 0.65 ** 10, 6))

# Practice 1.11 : geometric p = 0.3
show("p111_pX4", round(0.7 ** 3 * 0.3, 6))
show("p111_tail3", round(0.7 ** 3, 6))
show("p111_2to4_sum", round(0.21 + 0.147 + 0.1029, 6))
show("p111_2to4_tails", round(0.7 - 0.7 ** 4, 6))
show("p111_07_pow4", round(0.7 ** 4, 6))

# Practice 1.13 : geometric p = 0.2, smallest k with P(X<=k) >= 0.9
show("p113_ln01", round(math.log(0.1), 6))
show("p113_ln08", round(math.log(0.8), 6))
show("p113_threshold", round(math.log(0.1) / math.log(0.8), 6))
show("p113_k", min(k for k in range(1, 100) if 1 - 0.8 ** k >= 0.9))
show("p113_cdf10", (round(0.8 ** 10, 6), round(1 - 0.8 ** 10, 6)))
show("p113_cdf11", (round(0.8 ** 11, 6), round(1 - 0.8 ** 11, 6)))

# Practice 1.15 : inspection, p = 0.05
show("p115_095_pow19", round(0.95 ** 19, 6))
show("p115_binom_n20_k1", round(binom_pmf(20, 0.05, 1), 6))
show("p115_geom_k20", round(geom_pmf(0.05, 20), 6))
show("p115_ratio", round(binom_pmf(20, 0.05, 1) / geom_pmf(0.05, 20), 6))

# Practice 1.7 : uniform on {3,...,17}
show("p17_n_values", 17 - 3 + 1)
show("p17_mass", round(1 / 15, 6))
show("p17_ge12", (6, round(6 / 15, 6)))
show("p17_mult5", (3, round(3 / 15, 6)))

# Practice 1.5 : hypergeometric urn 3 red / 2 blue, draw 2
show("p15_counts", {r: math.comb(3, r) * math.comb(2, 2 - r) for r in range(3)})
show("p15_total", math.comb(5, 2))

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(R, indent=1, default=str), encoding="utf-8")
print("\nwrote", out)
