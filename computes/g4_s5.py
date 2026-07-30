# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""G4 §5 (synthesis + bridge to Markov chains) — every number in fragments/g4_s5.html.

Each cheatsheet identity is checked a second, independent way:
  * iterated expectation / total variance  -> exact Fraction arithmetic on the
    L12 two-section model, and brute-force enumeration of a joint PMF;
  * random-sum mean/variance               -> exact convolution of the full PMF of
    Y = X_1 + ... + X_N against the formulas E[N]E[X], E[N]var(X)+(E[X])^2 var(N);
  * Bernoulli -> Poisson limit             -> total-variation distance between
    binomial(t/delta, lambda*delta) and Poisson(lambda t) as delta -> 0;
  * merging / splitting                    -> direct joint-PMF factorization tests,
    which SEPARATE the Bernoulli case (split streams dependent) from the Poisson
    case (split streams independent);
  * random incidence                       -> length-biased density l*f(l)/E[L],
    integrated numerically, against the Erlang-2 closed form.

Run:  uv run computes/g4_s5.py
"""
import io
import json
import math
import sys
from fractions import Fraction as F

import numpy as np
from scipy import integrate, stats

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

R = {}
TOL = 1e-9


def check(name, a, b, tol=TOL):
    ok = abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b)))
    print(f"    [{'OK ' if ok else 'FAIL'}] {name}: {float(a):.12g} vs {float(b):.12g}")
    assert ok, name
    return float(a)


# ---------------------------------------------------------------- 1. iterated
print("1. Iterated expectation / law of total variance (L12 slides 4-5)")
# Two sections: y=1 has 10 students, mean 90, within-variance 10;
# y=2 has 20 students, mean 60, within-variance 20.  A student is drawn uniformly
# from the 30, so P(Y=1)=10/30=1/3, P(Y=2)=20/30=2/3.
pY = [F(10, 30), F(20, 30)]
mu = [F(90), F(60)]
v = [F(10), F(20)]
EX = sum(p * m for p, m in zip(pY, mu))                       # E[E[X|Y]]
Evar = sum(p * s for p, s in zip(pY, v))                      # E[var(X|Y)]
varE = sum(p * (m - EX) ** 2 for p, m in zip(pY, mu))         # var(E[X|Y])
varX = Evar + varE
print(f"    P(Y=1)={pY[0]}, P(Y=2)={pY[1]}")
print(f"    E[X] = {EX} ; E[var(X|Y)] = {Evar} = {float(Evar):.6f}")
print(f"    var(E[X|Y]) = {varE} ; var(X) = {varX} = {float(varX):.6f}")
# Independent check: build an explicit 30-student roster with the stated section
# means and within-section variances, then compute the pooled variance directly.
# Section 1: 10 values, mean 90, mean square deviation 10  -> 90 +/- sqrt(10).
# Section 2: 20 values, mean 60, mean square deviation 20  -> 60 +/- sqrt(20).
s1 = np.array([90 + math.sqrt(10)] * 5 + [90 - math.sqrt(10)] * 5)
s2 = np.array([60 + math.sqrt(20)] * 10 + [60 - math.sqrt(20)] * 10)
roster = np.concatenate([s1, s2])
check("roster mean = E[X]", roster.mean(), float(EX))
check("roster var  = var(X)", roster.var(), float(varX))
check("within-section variances", s1.var() + s2.var(), 10 + 20)
R["sections"] = {"EX": float(EX), "E_var": float(Evar), "E_var_frac": "50/3",
                 "var_E": float(varE), "varX": float(varX), "varX_frac": "650/3",
                 "pct_between": float(varE / varX) * 100}
print(f"    between-section share of var(X): {float(varE/varX)*100:.4f}%")

# ---------------------------------------------------------------- 2. random sum
print("2. Random sum Y = X_1 + ... + X_N (L12 slides 7-8)")
LAM_N = 2.5                       # N ~ Poisson(2.5): number of stores visited
NMAX = 120                        # truncation (Poisson tail beyond this is < 1e-90)
pN = stats.poisson.pmf(np.arange(NMAX + 1), LAM_N)
pN = pN / pN.sum()
EN, varN = LAM_N, LAM_N
# X_i i.i.d. uniform on {1,2,3} dollars
xs = np.array([1, 2, 3])
pX = np.array([1 / 3, 1 / 3, 1 / 3])
EXi = float(xs @ pX)
EXi2 = float((xs ** 2) @ pX)
varXi = EXi2 - EXi ** 2
print(f"    E[N]={EN}, var(N)={varN}; E[X]={EXi:.6f}, var(X)={varXi:.6f} (=2/3)")
# Exact PMF of Y by repeated convolution, mixed over N.
maxY = 3 * NMAX
pY_sum = np.zeros(maxY + 1)
conv = np.zeros(maxY + 1)
conv[0] = 1.0                      # PMF of the empty sum (n = 0)
for n in range(NMAX + 1):
    pY_sum[: len(conv)] += pN[n] * conv
    if n < NMAX:
        new = np.zeros_like(conv)
        for x, px in zip(xs, pX):
            new[x:] += px * conv[: len(conv) - x]
        conv = new
ys = np.arange(maxY + 1)
EY_direct = float(ys @ pY_sum)
EY2_direct = float((ys ** 2) @ pY_sum)
varY_direct = EY2_direct - EY_direct ** 2
EY_formula = EN * EXi
varY_formula = EN * varXi + EXi ** 2 * varN
check("total mass of Y", pY_sum.sum(), 1.0)
check("E[Y] = E[N]E[X]", EY_direct, EY_formula, 1e-8)
check("var(Y) = E[N]var(X) + (E[X])^2 var(N)", varY_direct, varY_formula, 1e-8)
print(f"    E[Y] = {EY_formula:.6f}, var(Y) = {EN*varXi:.6f} + {EXi**2*varN:.6f}"
      f" = {varY_formula:.6f}")
# The WRONG formula students write, var(Y) = E[N] var(X), for comparison:
print(f"    wrong 'var(Y)=E[N]var(X)' would give {EN*varXi:.6f}"
      f" ({EN*varXi/varY_formula*100:.2f}% of the truth)")
R["random_sum"] = {"EN": EN, "varN": varN, "EX": EXi, "varX": varXi,
                   "EY": EY_formula, "varY": varY_formula,
                   "term_within": EN * varXi, "term_across": EXi ** 2 * varN,
                   "wrong_pct": EN * varXi / varY_formula * 100}

# ---------------------------------------------------------------- 3. B -> P limit
print("3. Bernoulli -> Poisson limit (L14 slides 4, 7)")
LAM, T = 2.0, 1.0                  # lambda = 2 arrivals per unit time, t = 1
tv = {}
for delta in (0.5, 0.25, 0.1, 0.01, 0.001):
    n = int(round(T / delta))
    p = LAM * delta
    k = np.arange(0, 40)
    d = 0.5 * np.abs(stats.binom.pmf(k, n, p) - stats.poisson.pmf(k, LAM * T)).sum()
    tv[delta] = float(d)
    print(f"    delta={delta:<6} n={n:<6} p={p:<6} np={n*p:.3f}   TV distance={d:.3e}")
check("np = lambda t", 100 * (LAM * 0.01), LAM * T)
# binomial mean/variance -> Poisson mean/variance
for delta in (0.1, 0.01):
    n, p = int(round(T / delta)), LAM * delta
    print(f"    delta={delta}: binomial mean np={n*p:.4f}, var np(1-p)={n*p*(1-p):.6f}"
          f"  -> Poisson {LAM*T:.4f}, {LAM*T:.4f}")
R["bp_limit"] = {"lam": LAM, "t": T, "tv": tv,
                 "binom_var_d01": 100 * 0.2 * (1 - 0.2) * 0 + int(round(1 / 0.1)) * (LAM * 0.1) * (1 - LAM * 0.1),
                 "binom_var_d001": int(round(1 / 0.01)) * (LAM * 0.01) * (1 - LAM * 0.01)}
# Geometric -> exponential, Pascal -> Erlang (means)
p_small = LAM * 0.001
print(f"    geometric mean 1/p = {1/p_small:.3f} slots = {0.001/p_small:.4f} time units"
      f"  vs exponential 1/lambda = {1/LAM:.4f}")
check("geometric slot mean -> 1/lambda", 0.001 / p_small, 1 / LAM)

# ---------------------------------------------------------------- 4. merging
print("4. Merging")
p1, p2 = 0.2, 0.3
p_merge = 1 - (1 - p1) * (1 - p2)
print(f"    Bernoulli: p1={p1}, p2={p2} -> merged p = 1-(1-p1)(1-p2) = {p_merge:.4f}"
      f"  (naive p1+p2 = {p1+p2:.4f}, overshoot {p1+p2-p_merge:.4f} = p1*p2)")
check("collision correction", p1 + p2 - p_merge, p1 * p2)
lam1, lam2 = 2.0, 3.0
lam_merge = lam1 + lam2
q_first = lam1 / lam_merge
print(f"    Poisson: lambda1={lam1}, lambda2={lam2} -> merged {lam_merge}"
      f"; P(next arrival is red) = {q_first:.4f}")
# check by the small-interval argument: P(red first) = lim over the discretization
d = 1e-6
q_disc = (lam1 * d) / (lam1 * d + lam2 * d - lam1 * lam2 * d * d)
check("P(next from first) small-interval", q_disc, q_first, 1e-5)
# check by the exponential race: P(T1 < T2) with T_i ~ exp(lambda_i)
race = integrate.quad(lambda t: lam1 * math.exp(-lam1 * t) * math.exp(-lam2 * t), 0, 60)[0]
check("P(T1 < T2) exponential race", race, q_first)
R["merging"] = {"p1": p1, "p2": p2, "p_merge": p_merge, "lam1": lam1, "lam2": lam2,
                "lam_merge": lam_merge, "q_first": q_first}

# ---------------------------------------------------------------- 5. splitting
print("5. Splitting: Bernoulli streams are DEPENDENT, Poisson streams are INDEPENDENT")
p, q = 0.5, 0.5                  # arrival prob per slot, routed up w.p. q
# One slot of the Bernoulli split: (A,B) = (arrival in stream 1, in stream 2)
pA1 = p * q
pB1 = p * (1 - q)
pAB = 0.0                        # impossible: one arrival cannot go both ways
print(f"    Bernoulli slot: P(A=1)={pA1}, P(B=1)={pB1}, P(A=1,B=1)={pAB}"
      f"  but P(A=1)P(B=1)={pA1*pB1}")
assert abs(pAB - pA1 * pB1) > 1e-12
# Poisson split: joint PMF of (N1, N2) over [0,t]
lam, t, pp = 4.0, 1.0, 0.25
kmax = 40
joint = np.zeros((kmax + 1, kmax + 1))
for n in range(2 * kmax + 1):
    pn = stats.poisson.pmf(n, lam * t)
    for j in range(min(n, kmax) + 1):
        i = n - j
        if i <= kmax:
            joint[j, i] += pn * stats.binom.pmf(j, n, pp)
m1 = joint.sum(axis=1)
m2 = joint.sum(axis=0)
err = np.abs(joint - np.outer(m1, m2)).max()
print(f"    Poisson split lambda={lam}, p={pp}: max |P(N1,N2) - P(N1)P(N2)| = {err:.3e}")
check("N1 marginal is Poisson(p*lam*t)", m1[3], stats.poisson.pmf(3, pp * lam * t), 1e-9)
check("N2 marginal is Poisson((1-p)lam t)", m2[3],
      stats.poisson.pmf(3, (1 - pp) * lam * t), 1e-9)
assert err < 1e-12
R["splitting"] = {"p": p, "q": q, "pA1": pA1, "pB1": pB1, "prod": pA1 * pB1,
                  "lam": lam, "p_route": pp, "rate1": pp * lam, "rate2": (1 - pp) * lam,
                  "indep_err": float(err)}

# ---------------------------------------------------------------- 6. incidence
print("6. Random incidence")
lam_ri = 0.5                     # buses at 0.5 per minute -> mean gap 2 minutes
f_exp = lambda l: lam_ri * math.exp(-lam_ri * l)
mean_gap = integrate.quad(lambda l: l * f_exp(l), 0, 400)[0]
check("E[T] exponential", mean_gap, 1 / lam_ri)
f_len = lambda l: l * f_exp(l) / mean_gap          # length-biased density
mass = integrate.quad(f_len, 0, 400)[0]
mean_len = integrate.quad(lambda l: l * f_len(l), 0, 400)[0]
erl2 = lambda l: lam_ri ** 2 * l * math.exp(-lam_ri * l)
check("length-biased density = Erlang-2", f_len(3.0), erl2(3.0))
check("length-biased mass", mass, 1.0)
check("E[L] = 2/lambda", mean_len, 2 / lam_ri)
print(f"    exponential gaps mean {1/lam_ri:.4f} min; observed gap mean {mean_len:.4f} min")
# Renewal example (L15 slide 8): gaps 5 or 10 minutes with probability 1/2 each.
g = [F(5), F(10)]
pg = [F(1, 2), F(1, 2)]
EL_plain = sum(w * x for w, x in zip(pg, g))
w5 = pg[0] * g[0] / EL_plain
w10 = pg[1] * g[1] / EL_plain
EL_obs = w5 * g[0] + w10 * g[1]
Enext = w5 * g[0] / 2 + w10 * g[1] / 2
print(f"    buses 5/10 min: plain mean gap {EL_plain} = {float(EL_plain)}")
print(f"    length-biased weights: 5-min {w5} = {float(w5):.6f}, 10-min {w10} = {float(w10):.6f}")
print(f"    observed gap mean {EL_obs} = {float(EL_obs):.6f};"
      f" E[wait to next] {Enext} = {float(Enext):.6f}; naive {float(EL_plain)/2}")
# simulation cross-check of the bus example
rng = np.random.default_rng(6041)
NB = 400000
gaps = rng.choice([5.0, 10.0], size=NB)
edges = np.concatenate([[0.0], np.cumsum(gaps)])
tstars = rng.uniform(edges[NB // 4], edges[-1] - 10.0, size=200000)
idx = np.searchsorted(edges, tstars) - 1
sim_gap = gaps[idx].mean()
sim_wait = (edges[idx + 1] - tstars).mean()
check("sim observed gap", sim_gap, float(EL_obs), 3e-3)
check("sim wait to next", sim_wait, float(Enext), 5e-3)
R["incidence"] = {"lam": lam_ri, "mean_gap": 1 / lam_ri, "mean_observed": mean_len,
                  "bus_EL_plain": float(EL_plain), "w5": float(w5), "w10": float(w10),
                  "bus_EL_obs": float(EL_obs), "bus_Enext": float(Enext),
                  "bus_naive": float(EL_plain) / 2,
                  "sim_gap": float(sim_gap), "sim_wait": float(sim_wait)}

# ---------------------------------------------------------------- 7. light bulbs
print("7. Light-bulb / competing-exponentials example (L15 slide 5)")
lam_b = 1.0
E_last = F(1, 3) + F(1, 2) + F(1, 1)
print(f"    3 bulbs, lambda={lam_b}: E[last death] = 1/(3L)+1/(2L)+1/L = {E_last}"
      f" = {float(E_last):.6f}")
rng2 = np.random.default_rng(41)
sim = rng2.exponential(1 / lam_b, size=(400000, 3)).max(axis=1).mean()
check("simulated max of 3 exponentials", sim, float(E_last), 5e-3)
R["bulbs"] = {"lam": lam_b, "E_last": float(E_last), "E_last_frac": "11/6",
              "sim": float(sim)}

# ---------------------------------------------------------------- 8. table cells
print("8. Cheatsheet table cells (means/variances)")
pb = 0.2
kk = 3
geo_mean, geo_var = 1 / pb, (1 - pb) / pb ** 2
pas_mean, pas_var = kk / pb, kk * (1 - pb) / pb ** 2
t_grid = np.arange(kk, 4000)
pas_pmf = stats.nbinom.pmf(t_grid - kk, kk, pb)
check("Pascal mean", (t_grid * pas_pmf).sum(), pas_mean, 1e-6)
check("Pascal var", ((t_grid ** 2) * pas_pmf).sum() - pas_mean ** 2, pas_var, 1e-6)
lam_e, ke = 0.6, 3
erl_mean = integrate.quad(
    lambda y: y * lam_e ** ke * y ** (ke - 1) * math.exp(-lam_e * y) / math.factorial(ke - 1),
    0, 400)[0]
check("Erlang mean = k/lambda", erl_mean, ke / lam_e, 1e-8)
print(f"    p={pb}: geometric mean {geo_mean:.4f} var {geo_var:.4f};"
      f" Pascal(k=3) mean {pas_mean:.4f} var {pas_var:.4f}")
print(f"    lambda={lam_e}: Erlang(k=3) mean {erl_mean:.6f} = {ke/lam_e:.6f}")
R["table"] = {"p": pb, "k": kk, "geo_mean": geo_mean, "geo_var": geo_var,
              "pascal_mean": pas_mean, "pascal_var": pas_var,
              "lam": lam_e, "erlang_mean": erl_mean}

# ------------------------------------------- 9. discrete (Bernoulli) length bias
print("9. Length-biased gap for a Bernoulli(p) process (discrete analogue of §4.4)")
# T ~ geometric(p) on {1,2,...}: p_T(l) = p(1-p)^(l-1), E[T] = 1/p.
# p_L(l) = l p_T(l) / E[T] = l p^2 (1-p)^(l-1);  E[L] = p E[T^2] = (2-p)/p.
p_lb = 0.2
L = np.arange(1, 20000)
pT = p_lb * (1 - p_lb) ** (L - 1)
pL = L * pT / (1 / p_lb)
check("length-biased PMF sums to 1", pL.sum(), 1.0, 1e-9)
check("E[L] = (2-p)/p", (L * pL).sum(), (2 - p_lb) / p_lb, 1e-9)
check("E[T^2] = (2-p)/p^2", (L ** 2 * pT).sum(), (2 - p_lb) / p_lb ** 2, 1e-9)
# continuum limit: with p = lambda*delta, delta*E[L] -> 2/lambda
lam_lb, dlt_lb = 2.0, 1e-4
p_small = lam_lb * dlt_lb
EL_slots = (2 - p_small) / p_small
print(f"    p={p_lb}: E[T]={1/p_lb:.6f} slots, E[L]={(2-p_lb)/p_lb:.6f} slots"
      f" (ratio {((2-p_lb)/p_lb)*p_lb:.6f})")
print(f"    p=lambda*delta={p_small}: delta*E[L] = {dlt_lb*EL_slots:.6f} -> 2/lambda ="
      f" {2/lam_lb:.6f}")
R["bern_lengthbias"] = {"p": p_lb, "E_T": 1 / p_lb, "E_L": (2 - p_lb) / p_lb,
                        "E_T2": (2 - p_lb) / p_lb ** 2,
                        "lam": lam_lb, "delta": dlt_lb,
                        "delta_E_L": dlt_lb * EL_slots, "limit": 2 / lam_lb}

# ---------------------------------------------------------------- 10. practice items
print("10. Practice 5.1-5.5")
# --- 5.1 mixture of Poissons: busy/quiet call day
pbusy = F(2, 5)
mu_b, mu_q = F(20), F(8)
EN = pbusy * mu_b + (1 - pbusy) * mu_q
EvarN = pbusy * mu_b + (1 - pbusy) * mu_q            # var(N|B) = mean for Poisson
varEN = pbusy * (mu_b - EN) ** 2 + (1 - pbusy) * (mu_q - EN) ** 2
varN = EvarN + varEN
# brute-force cross-check on the exact mixture PMF
kk9 = np.arange(0, 400)
mix = 0.4 * stats.poisson.pmf(kk9, 20.0) + 0.6 * stats.poisson.pmf(kk9, 8.0)
m1 = (kk9 * mix).sum()
check("P5.1 E[N]", m1, float(EN))
check("P5.1 var(N)", (kk9 ** 2 * mix).sum() - m1 ** 2, float(varN), 1e-8)
print(f"    P5.1: E[N]={float(EN)}, E[var(N|B)]={float(EvarN)},"
      f" var(E[N|B])={float(varEN)}, var(N)={float(varN)}")
R["p51"] = {"p_busy": 0.4, "mu_busy": 20, "mu_quiet": 8, "EN": float(EN),
            "E_varN": float(EvarN), "var_EN": float(varEN), "varN": float(varN)}

# --- 5.2 Poisson splitting + random sum
lam52, q52, T52 = 10.0, 0.2, 3.0
lamB = q52 * lam52
EN52 = lamB * T52                                     # Poisson(6)
EX52, varX52 = 50.0, 20.0 ** 2
EY52 = EN52 * EX52
varY52 = EN52 * varX52 + EX52 ** 2 * EN52
sdY52 = math.sqrt(varY52)
term_within52 = EN52 * varX52
term_count52 = EX52 ** 2 * EN52
share_count52 = term_count52 / varY52
sd_within52 = math.sqrt(term_within52)
rng3 = np.random.default_rng(552)
ns = rng3.poisson(EN52, size=2000000)
tot = rng3.normal(EX52, 20.0, size=(int(ns.sum()),))
csum = np.concatenate([[0.0], np.cumsum(tot)])
sums = np.diff(csum[np.concatenate([[0], np.cumsum(ns)])])
check("P5.2 sim E[Y]", sums.mean(), EY52, 5e-3)
check("P5.2 sim var(Y)", sums.var(), varY52, 5e-3)
print(f"    P5.2: rate {lamB}/h, E[N]={EN52}, E[Y]={EY52}, var(Y)={varY52},"
      f" sd={sdY52:.6f}")
print(f"          within {term_within52} + count {term_count52};"
      f" count share {100*share_count52:.6f}%; sd from within term only {sd_within52:.6f}")
R["p52"] = {"lam": lam52, "q": q52, "T": T52, "lam_big": lamB, "EN": EN52,
            "EX": EX52, "varX": varX52, "EY": EY52, "varY": varY52, "sdY": sdY52,
            "term_within": term_within52, "term_count": term_count52,
            "share_count_pct": 100 * share_count52, "sd_within_only": sd_within52,
            "sim_EY": float(sums.mean()), "sim_varY": float(sums.var())}

# --- 5.3 unit trap: lambda=3/min, delta=0.01 min, window 0.5 min
lam53, dlt53, w53 = 3.0, 0.01, 0.5
p53 = lam53 * dlt53
n53 = int(round(w53 / dlt53))
exact53 = math.exp(-lam53 * w53)
binom53 = (1 - p53) ** n53
check("P5.3 binomial P(no arrival)", binom53, stats.binom.pmf(0, n53, p53))
geo_slots = 1 / p53
geo_time = geo_slots * dlt53
print(f"    P5.3: p={p53}, n={n53}, P0 exact {exact53:.6f} vs binomial {binom53:.6f},"
      f" |diff| {abs(exact53-binom53):.6f}; geometric mean {geo_slots:.6f} slots"
      f" = {geo_time:.6f} min = 1/lambda = {1/lam53:.6f}")
R["p53"] = {"lam": lam53, "delta": dlt53, "p": p53, "n": n53, "window": w53,
            "P0_exact": exact53, "P0_binom": binom53, "diff": abs(exact53 - binom53),
            "geo_slots": geo_slots, "geo_time": geo_time, "inv_lam": 1 / lam53}

# --- 5.4 merging: work/personal email, time until one of each
lw, lp = 5.0, 3.0
lm = lw + lp
p_personal_first = lp / lm
E_one_each = 1 / lm + (lw / lm) * (1 / lp) + (lp / lm) * (1 / lw)
rng4 = np.random.default_rng(554)
tw = rng4.exponential(1 / lw, size=400000)
tp = rng4.exponential(1 / lp, size=400000)
check("P5.4 sim E[max]", np.maximum(tw, tp).mean(), E_one_each, 5e-3)
print(f"    P5.4: merged rate {lm}, P(personal first)={p_personal_first:.6f},"
      f" E[one of each]={E_one_each:.6f} h = {E_one_each*60:.6f} min")
R["p54"] = {"lam_work": lw, "lam_pers": lp, "lam_merged": lm,
            "p_personal_first": p_personal_first, "E_one_each": E_one_each,
            "E_one_each_min": E_one_each * 60}

# --- 5.5 class-size (discrete length bias)
f_small, s_small, s_big = F(4, 5), F(20), F(100)
E_class = f_small * s_small + (1 - f_small) * s_big
w_big = (1 - f_small) * s_big / E_class
w_small = 1 - w_big
E_student = w_small * s_small + w_big * s_big
print(f"    P5.5: E[size | random class] = {float(E_class)};"
      f" P(student in big class) = {w_big} = {float(w_big):.6f};"
      f" E[size | random student] = {E_student} = {float(E_student):.6f}")
R["p55"] = {"frac_small": 0.8, "size_small": 20, "size_big": 100,
            "E_class": float(E_class), "w_small": float(w_small),
            "w_big": float(w_big), "E_student": float(E_student),
            "E_student_frac": "580/9"}

with open("computes/g4_s5.json", "w", encoding="utf-8") as fh:
    json.dump(R, fh, indent=2)
print("\nwrote computes/g4_s5.json")
