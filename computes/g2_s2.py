# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy"]
# ///
"""All numbers used in note G2 section 2 (Expectation).

Sources: L05 slides 6-7 (expectation), rec05 problems 1-4,
Bertsekas-Tsitsiklis 2nd ed. section 2.4 (printed pp. 81-88).
Run:  uv run computes/g2_s2.py
"""
from __future__ import annotations
import json
import random
import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R: dict = {}


def show(key, val, note=""):
    R[key] = val
    print(f"{key:34s} = {val}   {note}")


L = "=" * 78

# ---------------------------------------------------------------- 2.1 uniform
print(L)
print("2.1  Uniform on {0,1,...,n}  (L05 slide 6 UNSOLVED example)")
print(L)
for n in (1, 2, 4, 6, 10, 100):
    s = sum(F(k, n + 1) for k in range(n + 1))
    show(f"unif_n{n}_EX", str(s), f"= {float(s):.4f}   (n/2 = {n/2})")
    assert s == F(n, 2)
# arithmetic series check
for n in (4, 6, 10):
    show(f"unif_n{n}_sum_k", sum(range(n + 1)), f"n(n+1)/2 = {n*(n+1)//2}")
show("unif_n4_terms", [f"{k}*1/5" for k in range(5)])
show("unif_n4_EX_dec", float(F(4, 2)))

# ------------------------------------------------------------ center of mass
print()
print(L)
print("2.1  Center-of-gravity demo PMF (asymmetric; used in Fig. 2.1)")
print(L)
cm_x = [1, 2, 3, 6]
cm_p = [F(1, 10), F(1, 2), F(1, 4), F(3, 20)]
show("cm_x", cm_x)
show("cm_p", [str(p) for p in cm_p])
show("cm_p_sum", str(sum(cm_p)))
cm_mean = sum(x * p for x, p in zip(cm_x, cm_p))
show("cm_terms", [f"{x}*{p}={x*p}" for x, p in zip(cm_x, cm_p)])
show("cm_mean", str(cm_mean), f"= {float(cm_mean):.4f}")
tl = sum((x - cm_mean) * p for x, p in zip(cm_x, cm_p) if x < cm_mean)
tr = sum((x - cm_mean) * p for x, p in zip(cm_x, cm_p) if x > cm_mean)
show("cm_torque_left", str(tl), f"= {float(tl):.4f}")
show("cm_torque_right", str(tr), f"= {float(tr):.4f}")
show("cm_torque_net", str(tl + tr))
show("cm_mode", cm_x[cm_p.index(max(cm_p))], "most likely value (not the mean)")
# median
cum = 0
for x, p in zip(cm_x, cm_p):
    cum += p
    if cum >= F(1, 2):
        show("cm_median", x, f"cumulative prob {cum}")
        break
# what a wrong fulcrum does
for c in (2, 3):
    t = sum((x - c) * p for x, p in zip(cm_x, cm_p))
    show(f"cm_torque_at_c{c}", str(t), f"= {float(t):.4f}  (nonzero -> beam tips)")

# ----------------------------------------------------- 2.2 expected value rule
print()
print(L)
print("2.2  Expected value rule, grouping demo (rec05 P1a)")
print(L)
# small demo: X uniform on {-2,-1,0,1,2}, g(x) = x^2
gx = list(range(-2, 3))
gp = [F(1, 5)] * 5
show("evr_x", gx)
show("evr_px", [str(p) for p in gp])
easy = sum(F(x * x) * p for x, p in zip(gx, gp))
show("evr_easy_terms", [f"{x*x}*1/5" for x in gx])
show("evr_easy", str(easy), f"= {float(easy):.4f}")
# hard way: PMF of Y = X^2
py: dict = {}
for x, p in zip(gx, gp):
    py[x * x] = py.get(x * x, F(0)) + p
show("evr_pY", {k: str(v) for k, v in sorted(py.items())})
hard = sum(F(y) * p for y, p in sorted(py.items()))
show("evr_hard_terms", [f"{y}*{py[y]}" for y in sorted(py)])
show("evr_hard", str(hard), f"= {float(hard):.4f}")
assert easy == hard
# E[g(X)] vs g(E[X])
mx = sum(F(x) * p for x, p in zip(gx, gp))
show("evr_EX", str(mx))
show("evr_g_of_EX", str(mx ** 2), "g(E[X]) = 0  != E[g(X)] = 2")

# book Example 2.4 Alice speed/time (B&T p.87-88)
print()
print("Book Example 2.4 (B&T p. 87-88): average speed vs average time")
pt_good, v_good, v_bad, dist = F(6, 10), 5, 30, 2
pt_bad = 1 - pt_good
ET = pt_good * F(dist, v_good) + pt_bad * F(dist, v_bad)
show("alice_p_good", str(pt_good))
show("alice_T_good", str(F(dist, v_good)), f"= {float(F(dist,v_good)):.4f} h")
show("alice_T_bad", str(F(dist, v_bad)), f"= {float(F(dist,v_bad)):.6f} h")
show("alice_ET", str(ET), f"= {float(ET):.6f} h = {float(ET)*60:.2f} min")
EV = pt_good * v_good + pt_bad * v_bad
show("alice_EV", str(EV), "mph")
show("alice_dist_over_EV", str(F(dist, 1) / EV), f"= {float(F(dist,1)/EV):.6f} h  (WRONG)")

# ------------------------------------------------------------- 2.3 linearity
print()
print(L)
print("2.3  Linearity check (L05 slide 7 UNSOLVED): E[aX+b] = aE[X]+b")
print(L)
a, b = 3, -7
lin = sum((a * x + b) * p for x, p in zip(gx, gp))
show("lin_a", a)
show("lin_b", b)
show("lin_direct", str(lin), f"= {float(lin):.4f}")
show("lin_formula", str(a * mx + b), "a*E[X]+b")
assert lin == a * mx + b

# --------------------------------------------------------------- 2.4 marksman
print()
print(L)
print("2.4  Marksman: Binomial(n=10, p=0.2)   (rec05 P2)")
print(L)
n, p = 10, F(1, 5)
pmf = [F(comb(n, k)) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
for k in range(n + 1):
    show(f"mk_pmf_{k}", f"{float(pmf[k]):.10f}", f"exact {pmf[k]}  C(10,{k})={comb(n,k)}")
show("mk_pmf_sum", str(sum(pmf)))
show("mk_P0", f"{float(pmf[0]):.6f}", "= 0.8^10 ; solution rounds to 0.1074")
show("mk_0p8_pow10", f"{0.8**10:.10f}")
tail = sum(pmf[6:])
show("mk_tail_terms", [f"{float(pmf[k]):.8f}" for k in range(6, 11)])
show("mk_tail_terms_sci", [f"{float(pmf[k]):.3e}" for k in range(6, 11)])
show("mk_tail", f"{float(tail):.8f}", f"exact {tail} ; solution rounds to 0.0064")
show("mk_tail_round4", round(float(tail), 4))
EX = sum(F(k) * pmf[k] for k in range(n + 1))
EX2 = sum(F(k * k) * pmf[k] for k in range(n + 1))
show("mk_EX", str(EX), f"= {float(EX):.6f}  (np = {n}*0.2)")
show("mk_EX2_direct", str(EX2), f"= {float(EX2):.6f}  (sum k^2 p(k))")
var = EX2 - EX ** 2
show("mk_var", str(var), f"= {float(var):.6f}  (np(1-p) = 10*0.2*0.8)")
show("mk_sd", f"{float(var) ** 0.5:.6f}")
show("mk_EX2_from_var", str(var + EX ** 2), "E[X^2] = var + (E[X])^2 = 1.6 + 4")
# Y = 2X - 3
EY = 2 * EX - 3
show("mk_EY", str(EY), "E[Y] = 2E[X]-3 = 2*2-3")
show("mk_varY", str(4 * var), "var(Y) = 2^2 var(X) = 4*1.6")
EY_direct = sum((2 * F(k) - 3) * pmf[k] for k in range(n + 1))
show("mk_EY_direct", str(EY_direct), "direct sum cross-check")
assert EY_direct == EY
show("mk_EZ", str(EX2), "E[Z] = E[X^2] = 5.6")
# termwise E[X^2] display
show("mk_EX2_terms", [f"{k*k}*{float(pmf[k]):.6f}={float(F(k*k)*pmf[k]):.6f}" for k in range(n + 1)])
show("mk_EX_terms", [f"{k}*{float(pmf[k]):.6f}={float(F(k)*pmf[k]):.6f}" for k in range(n + 1)])
show("mk_profit_range", [2 * k - 3 for k in range(n + 1)])
show("mk_P_more_hits_check", f"{float(sum(pmf[k] for k in range(n+1) if k > n - k)):.8f}",
     "k > 10-k  <=>  k >= 6")

# ------------------------------------------------------------ 2.5 bus paradox
print()
print(L)
print("2.5  Buses / job-seeking students (rec05 P3): size-biased sampling")
print(L)
sizes = [40, 33, 25, 50]
tot = sum(sizes)
show("bus_sizes", sizes)
show("bus_total", tot)
show("bus_nbuses", len(sizes))
show("bus_pX", [f"{s}/{tot}" for s in sizes])
show("bus_X_terms", [f"{s}*{s}/{tot} = {s*s}/{tot}" for s in sizes])
show("bus_X_numer_parts", [s * s for s in sizes])
show("bus_X_numer", sum(s * s for s in sizes))
EXb = F(sum(s * s for s in sizes), tot)
show("bus_EX", str(EXb), f"= {float(EXb):.6f} ; solution rounds to 39.28")
show("bus_EX_round2", round(float(EXb), 2))
EYb = F(sum(sizes), len(sizes))
show("bus_EY_terms", [f"{s}/4" for s in sizes])
show("bus_EY", str(EYb), f"= {float(EYb):.4f}")
show("bus_gap", str(EXb - EYb), f"= {float(EXb - EYb):.6f}")
EY2 = F(sum(s * s for s in sizes), len(sizes))
varY = EY2 - EYb ** 2
show("bus_EY2", str(EY2), f"= {float(EY2):.4f}")
show("bus_varY", str(varY), f"= {float(varY):.4f}")
show("bus_sdY", f"{float(varY) ** 0.5:.6f}")
show("bus_identity_rhs", str(EYb + varY / EYb),
     f"E[Y]+var(Y)/E[Y] = {float(EYb + varY/EYb):.6f}  (equals E[X])")
assert EYb + varY / EYb == EXb
# equal-size control case
eq = [37, 37, 37, 37]
show("bus_equal_EX", str(F(sum(s * s for s in eq), sum(eq))), "all buses equal -> no bias")
# extra: what if one bus is empty
alt = [0, 40, 33, 25, 50]
show("bus_alt_sizes", alt)
show("bus_alt_EY", str(F(sum(alt), len(alt))), f"= {float(F(sum(alt), len(alt))):.4f}")
show("bus_alt_EX", str(F(sum(s * s for s in alt), sum(alt))),
     f"= {float(F(sum(s*s for s in alt), sum(alt))):.4f}  (unchanged: empty bus carries no student)")

# --------------------------------------------------------- 2.6 St. Petersburg
print()
print(L)
print("2.6  St. Petersburg paradox (rec05 P4 = text Problem 2.21, p. 123)")
print(L)
show("sp_pmf_rule", "P(X=k) = (1/2)^(k-1) * (1/2) = 2^-k", "k-1 heads then a tail")
show("sp_pmf_first5", [f"P(X={k})=1/{2**k}={2.0**-k}" for k in range(1, 6)])
show("sp_payout_first5", [2 ** k for k in range(1, 6)])
show("sp_terms_first5", [f"2^{k} * 2^-{k} = 1" for k in range(1, 6)])
partials = {}
for m in (1, 2, 5, 10, 20, 40, 100):
    partials[m] = sum(2 ** k * F(1, 2 ** k) for k in range(1, m + 1))
    show(f"sp_partial_m{m}", str(partials[m]), "sum_{k<=m} 2^k 2^-k = m")
# truncated / bankroll-capped versions  (widget math)
print()
print("Truncated versions (widget w-g2s2-petersburg):")
for m in (1, 2, 3, 5, 10, 20, 30, 40, 50):
    capped = sum(F(2 ** k, 2 ** k) for k in range(1, m + 1)) + F(2 ** m, 2 ** m)
    forfeit = sum(F(2 ** k, 2 ** k) for k in range(1, m + 1))
    show(f"sp_cap_m{m}", str(capped), f"cap rule E = m+1 = {m+1}")
    assert capped == m + 1
    assert forfeit == m
show("sp_cap_formula", "E[2^min(X,m)] = m + 1")
show("sp_forfeit_formula", "E[payout, 0 if X>m] = m")
show("sp_P_hit_cap_m10", f"{2.0**-10:.10f}", "P(X > m) = 2^-m")
show("sp_P_hit_cap_m20", f"{2.0**-20:.12f}")
show("sp_cap_dollars_m10", 2 ** 10)
show("sp_cap_dollars_m20", 2 ** 20)
show("sp_cap_dollars_m30", 2 ** 30)
show("sp_cap_m30_value", 31)
# typical values
for t in (1, 2, 3, 4, 5, 10):
    show(f"sp_P_payout_le_2pow{t}", str(1 - F(1, 2 ** t)),
         f"P(payout <= {2**t}) = 1-2^-{t} = {float(1-F(1,2**t)):.6f}")
show("sp_median_payout", 2, "P(payout = 2) = 1/2")
show("sp_P_payout_ge_1000", f"{2.0**-9:.8f}", "payout >= 1024 iff X >= 10")
show("sp_P_payout_lt_20", str(1 - F(1, 2 ** 4)), "payout <= 16 (< 20) w.p. 15/16 = 0.9375")
# simulation (mirrors the rec05 extra handout histograms)
rng = random.Random(6041)


def play():
    k = 1
    while rng.random() < 0.5:
        k += 1
    return 2 ** k


for N in (20, 200, 2000, 20000, 200000):
    s = [play() for _ in range(N)]
    show(f"sp_sim_N{N}_mean", f"{sum(s)/N:.2f}", f"max payout seen {max(s)}")
show("sp_sim_note", "handout: 20 sims avg $19.20, 200 sims avg $11.16 (their run)")

# ------------------------------------------------------------------ practice
print()
print(L)
print("Practice-question numbers")
print(L)
# P1: uniform on {5,...,15}
lo, hi = 5, 15
m = hi - lo + 1
show("pq_unif_count", m)
show("pq_unif_EX", str(F(sum(range(lo, hi + 1)), m)), f"= {(lo+hi)/2}")
# P2: E[1/(X+1)] for X uniform on 0..3
xs = list(range(4))
val = sum(F(1, x + 1) * F(1, 4) for x in xs)
show("pq_recip_terms", [f"1/{x+1} * 1/4" for x in xs])
show("pq_recip_E", str(val), f"= {float(val):.6f}")
show("pq_recip_g_of_EX", str(F(1, 1) / (F(3, 2) + 1)), f"= {float(F(1,1)/(F(3,2)+1)):.6f}  (g(E[X]), different)")
# P3: temperature conversion
show("pq_temp_EC", 20)
show("pq_temp_EF", str(F(9, 5) * 20 + 32), "9/5*20+32")
show("pq_temp_varF", str(F(9, 5) ** 2 * 9), f"= {float(F(9,5)**2*9):.4f}")
show("pq_temp_EF2", str(F(9, 5) ** 2 * 9 + 68 ** 2), f"= {float(F(9,5)**2*9 + 68**2):.4f}")
# marksman follow-ups
show("pq_fair_fee", str(2 * EX), "2*E[X] = fee making E[2X-f]=0")
show("pq_fair_lose", f"{float(pmf[0] + pmf[1]):.6f}", "P(X<=1): loses money at fair fee 4")
show("pq_fair_even", f"{float(pmf[2]):.6f}", "P(X=2): breaks even")
show("pq_fair_win", f"{float(sum(pmf[3:])):.6f}", "P(X>=3): profits")
show("pq_sdY_marksman", f"{float(4 * var) ** 0.5:.6f}", "sd of Y = 2X-3")
show("pq_ratio_P0_20_vs_10", f"{float(pmf[0]) / (0.8 ** 20):.4f}", "0.8^10/0.8^20")
# practice 2.9 / 2.10 buses
bs2 = [10, 20, 60]
EY3 = F(sum(bs2), 3)
EY3sq = F(sum(s * s for s in bs2), 3)
show("pq_bus_EY2", str(EY3sq), f"= {float(EY3sq):.4f}")
show("pq_bus_varY", str(EY3sq - EY3 ** 2), f"= {float(EY3sq - EY3**2):.4f}")
show("pq_bus_identity", str(EY3 + (EY3sq - EY3 ** 2) / EY3), f"= {float(EY3 + (EY3sq-EY3**2)/EY3):.4f}")
show("pq_bus_bias_pct_3bus", f"{float(F(sum(s*s for s in bs2), sum(bs2)) / EY3) - 1:.4f}")
show("pq_bus_bias_pct_rec05", f"{float(EXb / EYb) - 1:.4f}")
show("pq_bus_varY_from_means", str(EYb * (EXb - EYb)), "E[Y](E[X]-E[Y]) = var(Y) = 84.5")
# P4: marksman 20 shots
n2 = 20
pmf2 = [F(comb(n2, k)) * p ** k * (1 - p) ** (n2 - k) for k in range(n2 + 1)]
EX20 = sum(F(k) * pmf2[k] for k in range(n2 + 1))
var20 = sum(F(k * k) * pmf2[k] for k in range(n2 + 1)) - EX20 ** 2
show("pq_mk20_EX", str(EX20))
show("pq_mk20_var", str(var20))
show("pq_mk20_EX2", str(var20 + EX20 ** 2), f"= {float(var20 + EX20**2):.4f}")
show("pq_mk20_P0", f"{float(pmf2[0]):.8f}")
# P5: bus practice - 3 buses 10,20,60
bs = [10, 20, 60]
show("pq_bus_sizes", bs)
show("pq_bus_EY", str(F(sum(bs), len(bs))), f"= {float(F(sum(bs), len(bs))):.4f}")
show("pq_bus_EX", str(F(sum(s * s for s in bs), sum(bs))),
     f"= {float(F(sum(s*s for s in bs), sum(bs))):.4f}")
show("pq_bus_numer", [s * s for s in bs])
show("pq_bus_numer_sum", sum(s * s for s in bs))
# P6: St Petersburg variant paying 3^n with fair coin -> also infinite; 2^n with P(tail)=q
show("pq_sp_variant", "payout 2^n, P(tail)=3/4: E = sum 2^k (1/4)^{k-1}(3/4) = 3/4 * sum (1/2)^{k-1} *? ")
q = F(3, 4)  # P(tail)
terms = [2 ** k * (1 - q) ** (k - 1) * q for k in range(1, 60)]
show("pq_sp_variant_E", str(sum(terms)), f"= {float(sum(terms)):.6f}  (finite: ratio 2*(1/4)=1/2)")
show("pq_sp_variant_closed", str(F(2 * 3, 4) / (1 - F(1, 2))), "2q/(1-2(1-q)) with q=3/4 -> 3")
# P7: capped game fair price
show("pq_cap_m10_E", 11)
show("pq_cap_m20_E", 21)

# ------------------------------------------------------------ widget crosscheck
print()
print(L)
print("Widget cross-check table  w-g2s2-petersburg  (E = m+1)")
print(L)
wc = {}
for m in range(1, 41):
    wc[m] = m + 1
show("widget_cap_table_m1_5_10_20_40", [wc[m] for m in (1, 5, 10, 20, 40)])
show("widget_forfeit_table_m1_5_10_20_40", [m for m in (1, 5, 10, 20, 40)])
show("widget_cap_dollars_m1_5_10_20_40", [2 ** m for m in (1, 5, 10, 20, 40)])
show("widget_Phitcap_m1_5_10_20_40", [f"{2.0**-m:.3e}" for m in (1, 5, 10, 20, 40)])

out = Path(__file__).resolve().parent / "g2_s2.json"
out.write_text(json.dumps(R, indent=1, default=str), encoding="utf-8")
print()
print("wrote", out, f"({len(R)} keys)")
