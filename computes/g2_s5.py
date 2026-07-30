# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""G2 section 5 (synthesis) — every number that appears in fragments/g2_s5.html.

All distributional means/variances are recomputed twice: once by the closed-form
formula quoted in the cheatsheet, once by brute-force summation over the PMF.
Both must agree to 1e-12.
"""
import io
import json
import sys
from fractions import Fraction as F
from math import comb, isclose, sqrt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

R = {}


def moments(support, pmf):
    """Exact mean, second moment, variance of a finite PMF given as dicts/lists."""
    tot = sum(pmf)
    m1 = sum(x * p for x, p in zip(support, pmf))
    m2 = sum(x * x * p for x, p in zip(support, pmf))
    return tot, m1, m2, m2 - m1 * m1


# ---------------------------------------------------------------- PMF zoo ----
print("=" * 68)
print("1. The discrete PMF zoo: closed form vs brute-force summation")
print("=" * 68)

# --- Bernoulli(p), p = 3/10 (L07 s6 indicator X_i) --------------------------
p = F(3, 10)
sup = [0, 1]
pm = [1 - p, p]
tot, m1, m2, v = moments(sup, pm)
print(f"Bernoulli(p={p}):  sum={tot}  E={m1}  E[X^2]={m2}  var={v}")
print(f"   closed form: E=p={p}, var=p(1-p)={p * (1 - p)}  -> match: "
      f"{m1 == p and v == p * (1 - p)}")
R["bernoulli"] = {"p": str(p), "mean": str(m1), "var": str(v),
                  "mean_dec": float(m1), "var_dec": float(v)}

# --- Discrete uniform on {a,...,b} = {0,...,4} (L05 s6) ---------------------
a, b = 0, 4
sup = list(range(a, b + 1))
n_vals = b - a + 1
pm = [F(1, n_vals)] * n_vals
tot, m1, m2, v = moments(sup, pm)
cf_mean = F(a + b, 2)
cf_var = F((b - a) * (b - a + 2), 12)
print(f"Uniform{{{a}..{b}}}: sum={tot}  E={m1}  E[X^2]={m2}  var={v}")
print(f"   closed form: (a+b)/2={cf_mean}, (b-a)(b-a+2)/12={cf_var}  -> match: "
      f"{m1 == cf_mean and v == cf_var}")
R["uniform_0_4"] = {"a": a, "b": b, "mean": str(m1), "var": str(v)}

# uniform on {0,...,n}: E = n/2 (the L05 s6 blank), var = n(n+2)/12
_unif_inst = {}
for nn in (1, 4, 9, 100):
    sup = list(range(nn + 1))
    pm = [F(1, nn + 1)] * (nn + 1)
    _, mm, _, vv = moments(sup, pm)
    ok = (mm == F(nn, 2)) and (vv == F(nn * (nn + 2), 12))
    print(f"   uniform{{0..{nn}}}: E={mm} (=n/2 {mm == F(nn, 2)}), "
          f"var={vv} (=n(n+2)/12 {vv == F(nn * (nn + 2), 12)}) -> {ok}")
    _unif_inst[str(nn)] = {"mean": str(mm), "mean_dec": float(mm),
                           "var": str(vv), "var_dec": float(vv)}
R["uniform_0_n_rule"] = {"mean": "n/2", "var": "n(n+2)/12",
                         "verified_n": [1, 4, 9, 100],
                         "instances": _unif_inst}

# --- Binomial(n,p), n = 10, p = 3/10 (L05 s5, L07 s6) ----------------------
n, p = 10, F(3, 10)
sup = list(range(n + 1))
pm = [comb(n, k) * p**k * (1 - p)**(n - k) for k in sup]
tot, m1, m2, v = moments(sup, pm)
print(f"Binomial(n={n},p={p}): sum={tot}  E={m1}  E[X^2]={m2}  var={v}")
print(f"   closed form: np={n * p}, np(1-p)={n * p * (1 - p)}  -> match: "
      f"{m1 == n * p and v == n * p * (1 - p)}")
R["binomial_10_0.3"] = {"n": n, "p": str(p), "mean": str(m1), "var": str(v),
                        "mean_dec": float(m1), "var_dec": float(v)}

# the L05 s5 special case n=4, k=2
n4, k2 = 4, 2
print(f"   C(4,2) = {comb(n4, k2)}  (the 6 sequences HHTT...TTHH on L05 s5)")
R["C_4_2"] = comb(n4, k2)

# --- Geometric(p), p = 1/5 (L05 s3, L06 s6-s7) -----------------------------
p = F(1, 5)
KMAX = 4000  # truncation for the brute-force check
sup = list(range(1, KMAX + 1))
pm = [(1 - p)**(k - 1) * p for k in sup]
tot_f = float(sum(pm))
m1_f = float(sum(k * q for k, q in zip(sup, pm)))
m2_f = float(sum(k * k * q for k, q in zip(sup, pm)))
v_f = m2_f - m1_f * m1_f
cf_mean, cf_var = float(1 / p), float((1 - p) / p**2)
print(f"Geometric(p={p}) truncated at k={KMAX}: sum={tot_f:.15f}  E={m1_f:.12f}  "
      f"var={v_f:.12f}")
print(f"   closed form: 1/p={cf_mean}, (1-p)/p^2={cf_var}  -> match: "
      f"{isclose(m1_f, cf_mean, abs_tol=1e-9) and isclose(v_f, cf_var, abs_tol=1e-9)}")
R["geometric_0.2"] = {"p": str(p), "mean": cf_mean, "var": cf_var,
                      "sum_check": tot_f, "mean_num": m1_f, "var_num": v_f}

# ------------------------------------------- 2. canonical G2 numbers -------
print()
print("=" * 68)
print("2. Canonical worked numbers of G2 (calibration table)")
print("=" * 68)

# L05 s4: X = min(F,S), two independent fair tetrahedral rolls
cells = [(f, s) for f in range(1, 5) for s in range(1, 5)]
pmin = {}
for f, s in cells:
    pmin[min(f, s)] = pmin.get(min(f, s), 0) + 1
pmin_pmf = {k: F(c, 16) for k, c in sorted(pmin.items())}
print("min(F,S) PMF:", {k: str(v) for k, v in pmin_pmf.items()},
      " sum =", sum(pmin_pmf.values()))
_, mmin, _, vmin = moments(list(pmin_pmf), list(pmin_pmf.values()))
print(f"   p_X(2) = {pmin_pmf[2]}   E[min] = {mmin} = {float(mmin)}   "
      f"var(min) = {vmin} = {float(vmin)}")
R["min_tetra"] = {"pmf": {str(k): str(v) for k, v in pmin_pmf.items()},
                  "p2": str(pmin_pmf[2]), "mean": str(mmin), "mean_dec": float(mmin),
                  "var": str(vmin), "var_dec": float(vmin)}

# L06 s3-s4: random speed V uniform on {1,200}, T = 200/V
sup = [1, 200]
pm = [F(1, 2), F(1, 2)]
_, EV, EV2, varV = moments(sup, pm)
sdV = sqrt(float(varV))
ET = sum(F(200, v) * q for v, q in zip(sup, pm))
ETV = sum(F(200, v) * v * q for v, q in zip(sup, pm))
print(f"Speed: E[V]={EV}={float(EV)}  E[V^2]={EV2}  var(V)={varV}={float(varV)}  "
      f"sigma_V={sdV}")
print(f"   E[T]={ET}={float(ET)}   200/E[V]={float(F(200, 1) / EV):.6f}   "
      f"E[T]*E[V]={float(ET * EV)}   E[TV]={ETV}")
R["speed"] = {"EV": float(EV), "EV2": float(EV2), "varV": float(varV),
              "sigmaV": sdV, "ET": float(ET), "two_hundred_over_EV": float(F(200) / EV),
              "ET_times_EV": float(ET * EV), "ETV": float(ETV)}

# L06 s5: X uniform on 1..4, A = {X >= 2}
sup = [1, 2, 3, 4]
pm = [F(1, 4)] * 4
_, EX_u, _, _ = moments(sup, pm)
supA = [2, 3, 4]
pmA = [F(1, 3)] * 3
_, EXA, _, _ = moments(supA, pmA)
print(f"Uniform 1..4: E[X]={EX_u}={float(EX_u)};  conditioned on X>=2: "
      f"p=1/3 each, E[X|A]={EXA}")
R["cond_unif"] = {"EX": float(EX_u), "EX_given_A": float(EXA)}

# L07 s7-s8: hat problem
for nh in (3, 5, 10, 100):
    EXi = F(1, nh)
    EX = nh * EXi                       # linearity
    EXi2 = F(1, nh)                     # indicator: X_i^2 = X_i
    EXiXj = F(1, nh) * F(1, nh - 1)     # P(X_1 X_2 = 1)
    EX2 = nh * EXi2 + nh * (nh - 1) * EXiXj
    varX = EX2 - EX * EX
    print(f"   hats n={nh}: E[X_i]={EXi}  E[X]={EX}  P(X_1X_2=1)={EXiXj}  "
          f"E[X^2]={EX2}  var(X)={varX}")
R["hat"] = {"EX": 1, "EX2": 2, "var": 1, "checked_n": [3, 5, 10, 100]}

# rec05 P3: size-biased bus sampling
buses = [40, 33, 25, 50]
N = sum(buses)
EX_sb = F(sum(b * b for b in buses), N)
EY_sb = F(sum(buses), len(buses))
print(f"Buses {buses}: total={N}  sum b^2={sum(b * b for b in buses)}")
print(f"   E[X] = {sum(b * b for b in buses)}/{N} = {EX_sb} = {float(EX_sb):.6f} "
      f"(rounds to {round(float(EX_sb), 2)})")
print(f"   E[Y] = {sum(buses)}/4 = {EY_sb} = {float(EY_sb)}")
print(f"   gap  = {float(EX_sb - EY_sb):.6f} = var(Y)/E[Y] check: "
      f"{float(moments(buses, [F(1, 4)] * 4)[3] / EY_sb):.6f}")
R["buses"] = {"sizes": buses, "total": N, "sumsq": sum(b * b for b in buses),
              "EX": float(EX_sb), "EX_round2": round(float(EX_sb), 2),
              "EY": float(EY_sb), "gap": float(EX_sb - EY_sb)}

# rec05 P4: St Petersburg partial sums (infinite expectation)
for K in (10, 30, 100):
    partial = sum(2**k * F(1, 2**k) for k in range(1, K + 1))
    print(f"   St Petersburg partial sum to k={K}: {partial} dollars")
R["st_petersburg"] = {"term": 1, "partial_100": 100, "limit": "infinite"}

# rec06 P3 / B&T Example 2.17: geometric variance instances
_geo_inst = {}
for pp in (F(1, 2), F(1, 5), F(9, 10)):
    gm, gv = 1 / pp, (1 - pp) / pp**2
    print(f"   geometric p={pp}: E=1/p={float(gm)}, "
          f"var=(1-p)/p^2={gv} = {float(gv):.6f}")
    _geo_inst[str(pp)] = {"mean": str(gm), "mean_dec": float(gm),
                          "var": str(gv), "var_dec": float(gv),
                          "var_round6": round(float(gv), 6)}
R["geometric_var_instances"] = _geo_inst

# L07 s7-s8 hat problem: the two ingredients the derivation needs, at several n
_hat_ing = {}
for nh in (3, 5, 10, 100):
    _hat_ing[str(nh)] = {"P_Xi_1": str(F(1, nh)),
                         "E_XiXj": str(F(1, nh * (nh - 1))),
                         "n_pairs": nh * (nh - 1)}
    print(f"   hat ingredients n={nh}: P(X_i=1)={F(1, nh)}  "
          f"E[X_iX_j]={F(1, nh * (nh - 1))}  off-diagonal pairs={nh * (nh - 1)}")
R["hat_ingredients"] = _hat_ing

# ---------------------------------------- 3. identity spot-checks ----------
print()
print("=" * 68)
print("3. Identity spot-checks (the expectation/variance table)")
print("=" * 68)

# use the joint PMF of L06 s8 / L07 s3 for the two-variable identities
tbl = {(1, 4): 1, (2, 4): 2, (3, 4): 2,
       (1, 3): 2, (2, 3): 4, (3, 3): 1, (4, 3): 2,
       (2, 2): 1, (3, 2): 3, (4, 2): 1,
       (2, 1): 1}
joint = {k: F(v, 20) for k, v in tbl.items()}
print("joint sums to", sum(joint.values()))
xs = sorted({x for x, _ in joint})
ys = sorted({y for _, y in joint})
pX = {x: sum(joint.get((x, y), 0) for y in ys) for x in xs}
pY = {y: sum(joint.get((x, y), 0) for x in xs) for y in ys}
EX = sum(x * q for x, q in pX.items())
EY = sum(y * q for y, q in pY.items())
EXY = sum(x * y * q for (x, y), q in joint.items())
EX2 = sum(x * x * q for x, q in pX.items())
EY2 = sum(y * y * q for y, q in pY.items())
vX, vY = EX2 - EX * EX, EY2 - EY * EY
EsumXY = sum((x + y) * q for (x, y), q in joint.items())
vsum = sum((x + y)**2 * q for (x, y), q in joint.items()) - EsumXY**2
cov = EXY - EX * EY
print(f"   E[X]={EX}={float(EX)}  E[Y]={EY}={float(EY)}  var(X)={vX}={float(vX):.6f}"
      f"  var(Y)={vY}={float(vY):.6f}")
print(f"   linearity: E[X+Y]={EsumXY}={float(EsumXY)} vs E[X]+E[Y]={EX + EY} -> "
      f"{EsumXY == EX + EY}")
print(f"   NOT independent: E[XY]={EXY}={float(EXY):.6f} vs E[X]E[Y]="
      f"{EX * EY}={float(EX * EY):.6f}  cov={cov}={float(cov):.6f}")
print(f"   var not additive here: var(X+Y)={vsum}={float(vsum):.6f} vs "
      f"var(X)+var(Y)={vX + vY}={float(vX + vY):.6f}  (difference 2cov="
      f"{float(2 * cov):.6f})")
R["joint"] = {"EX": float(EX), "EY": float(EY), "varX": float(vX), "varY": float(vY),
              "EXY": float(EXY), "EX_EY": float(EX * EY), "cov": float(cov),
              "EXplusY": float(EsumXY), "varXplusY": float(vsum),
              "varX_plus_varY": float(vX + vY)}

# E[g(X)] != g(E[X]) with g(x) = x^2 on the uniform 1..4
sup = [1, 2, 3, 4]
pm = [F(1, 4)] * 4
_, m1, m2, _ = moments(sup, pm)
print(f"   Jensen-style gap: E[X^2]={m2}={float(m2)} vs (E[X])^2={m1 * m1}="
      f"{float(m1 * m1)}  gap = var = {float(m2 - m1 * m1)}")
R["jensen_gap"] = {"EX2": float(m2), "EX_sq": float(m1 * m1), "gap": float(m2 - m1 * m1)}

# var(aX+b) = a^2 var(X): check a=-3, b=7 on binomial(10,0.3)
n, p = 10, F(3, 10)
sup = list(range(n + 1))
pm = [comb(n, k) * p**k * (1 - p)**(n - k) for k in sup]
aa, bb = -3, 7
sup2 = [aa * x + bb for x in sup]
_, m1b, _, vb = moments(sup2, pm)
_, m1a, _, va = moments(sup, pm)
print(f"   var(-3X+7) = {vb} = {float(vb)}  vs 9*var(X) = {9 * va} = {float(9 * va)}"
      f"  -> {vb == 9 * va};  E[-3X+7]={m1b} vs -3E[X]+7={aa * m1a + bb} -> "
      f"{m1b == aa * m1a + bb}")
R["linear_transform"] = {"a": aa, "b": bb, "var_transformed": float(vb),
                         "a2_var": float(9 * va), "mean_transformed": float(m1b)}

# total expectation: geometric(1/5) split on {X=1} vs {X>1}
p = F(1, 5)
lhs = float(1 / p)
rhs = float(p * 1 + (1 - p) * (1 + 1 / p))
print(f"   total expectation on geometric p={p}: 1/p={lhs} vs "
      f"p*1+(1-p)*(1+1/p)={rhs} -> {isclose(lhs, rhs)}")
R["total_exp_geom"] = {"p": str(p), "lhs": lhs, "rhs": rhs}

# --------------------------------------------------- 4. G3 teaser ---------
print()
print("=" * 68)
print("4. Bridge to G3: discretizing a continuous uniform on [0,1]")
print("=" * 68)
for m in (4, 10, 100, 1000):
    sup = [F(2 * i + 1, 2 * m) for i in range(m)]
    pm = [F(1, m)] * m
    _, mu, _, vv = moments(sup, pm)
    print(f"   m={m:5d} bins: E={float(mu):.9f} (limit 0.5)  "
          f"var={float(vv):.9f} (limit 1/12 = {1 / 12:.9f})  "
          f"mass per bin = {float(F(1, m)):.6f}, density = {float(m * F(1, m)):.3f}")
R["g3_teaser"] = {"limit_mean": 0.5, "limit_var": 1 / 12,
                  "m1000_var": float(moments([F(2 * i + 1, 2000) for i in range(1000)],
                                             [F(1, 1000)] * 1000)[3])}

# ------------------------------------- 5. practice-box answers (§5.1-5.5) ---
print()
print("=" * 68)
print("5. Practice-box answers")
print("=" * 68)
P = {}


def _binom(nn, pp):
    sup = list(range(nn + 1))
    pm = [comb(nn, k) * pp**k * (1 - pp)**(nn - k) for k in sup]
    return moments(sup, pm)


# P5.1b: X = heads in 3 fair tosses, E[X^2] two ways
tot, m1, m2, v = _binom(3, F(1, 2))
# route 2: expected-value rule applied to g(x)=x^2 over the same PMF (identical
# arithmetic by construction) -- and the closed form np(1-p) + (np)^2
cf = F(3, 1) * F(1, 2) * F(1, 2) + (F(3, 2))**2
print(f"P5.1b binomial(3,1/2): sum={tot} E={m1} E[X^2]={m2} var={v}; "
      f"np(1-p)+(np)^2={cf} -> match {m2 == cf}")
P["p5_1b"] = {"EX": str(m1), "EX2": str(m2), "var": str(v), "var_dec": float(v)}

# P5.2a: four verbal setups -> four families
_, mb, _, vb = _binom(50, F(2, 100))
pg = F(1, 4)
gm, gv = 1 / pg, (1 - pg) / pg**2
a12, b12 = 1, 12
_, mu12, _, vu12 = moments(list(range(1, 13)), [F(1, 12)] * 12)
pber = F(12, 30)
print(f"P5.2a binomial(50,0.02): E={mb}={float(mb)} var={vb}={float(vb)}")
print(f"P5.2a geometric(1/4):    E={gm}={float(gm)} var={gv}={float(gv)}")
print(f"P5.2a uniform{{1..12}}:   E={mu12}={float(mu12)} var={vu12}={float(vu12):.6f}"
      f"  (closed form (b-a)(b-a+2)/12={F((b12 - a12) * (b12 - a12 + 2), 12)})")
print(f"P5.2a Bernoulli(12/30):  E={pber}={float(pber)} "
      f"var={pber * (1 - pber)}={float(pber * (1 - pber))}")
P["p5_2a"] = {
    "binom_50_002": {"mean": str(mb), "mean_dec": float(mb), "var": str(vb),
                     "var_dec": float(vb)},
    "geom_quarter": {"mean": str(gm), "mean_dec": float(gm), "var": str(gv),
                     "var_dec": float(gv)},
    "unif_1_12": {"mean": str(mu12), "mean_dec": float(mu12), "var": str(vu12),
                  "var_dec": float(vu12), "var_round6": round(float(vu12), 6)},
    "bern_04": {"mean": str(pber), "mean_dec": float(pber),
                "var": str(pber * (1 - pber)), "var_dec": float(pber * (1 - pber))},
}

# P5.2b: 5 cards dealt without replacement, X = number of aces (NOT binomial)
p_ace = F(4, 52)
E_aces = 5 * p_ace
# brute force over the hypergeometric PMF, to show linearity still gives the mean
hsup = list(range(0, 5))
hpm = [F(comb(4, k) * comb(48, 5 - k), comb(52, 5)) for k in hsup]
th, mh, _, vh = moments(hsup, hpm)
print(f"P5.2b aces in 5 cards: indicators give 5*(4/52)={E_aces}={float(E_aces):.6f}; "
      f"hypergeometric sum={th} mean={mh} -> match {mh == E_aces}; var={vh}="
      f"{float(vh):.6f} (binomial would say {float(5 * p_ace * (1 - p_ace)):.6f})")
P["p5_2b"] = {"p_ace": str(p_ace), "mean": str(E_aces), "mean_dec": float(E_aces),
              "var_true": str(vh), "var_true_dec": float(vh),
              "var_if_binomial": float(5 * p_ace * (1 - p_ace))}

# P5.3a: which functionals are computable from var(X)=3, var(Y)=5, E[X]=2, E[Y]=-1
vX3, vY5, eX2, eYm1 = 3, 5, 2, -1
print(f"P5.3a E[X+Y]={eX2 + eYm1}  E[3X-2Y+4]={3 * eX2 - 2 * eYm1 + 4}  "
      f"var(2X+1)={4 * vX3}  sigma_X=sqrt(3)={sqrt(vX3):.6f}  "
      f"[var(X+Y) and E[XY] NOT determined]")
P["p5_3a"] = {"E_XplusY": eX2 + eYm1, "E_3Xm2Yp4": 3 * eX2 - 2 * eYm1 + 4,
              "var_2Xp1": 4 * vX3, "sigma_X": sqrt(vX3),
              "sigma_X_round6": round(sqrt(vX3), 6),
              "undetermined": ["var(X+Y)", "E[XY]"]}

# P5.3b: geometric(1/5) memorylessness -> E[X | X>3], var(X | X>3)
pg5 = F(1, 5)
E_cond = 3 + 1 / pg5
v_cond = (1 - pg5) / pg5**2
# brute-force check on the conditional PMF p(k) = (1-p)^(k-4) p for k >= 4
csup = list(range(4, 4004))
cpm = [float((1 - pg5)**(k - 4) * pg5) for k in csup]
cm1 = sum(k * q for k, q in zip(csup, cpm))
cm2 = sum(k * k * q for k, q in zip(csup, cpm))
print(f"P5.3b geometric(1/5) given X>3: closed form E={E_cond}, var={v_cond}; "
      f"brute force E={cm1:.9f}, var={cm2 - cm1 * cm1:.9f} -> match "
      f"{isclose(cm1, float(E_cond), abs_tol=1e-6) and isclose(cm2 - cm1 * cm1, float(v_cond), abs_tol=1e-6)}")
P["p5_3b"] = {"E_given": float(E_cond), "var_given": float(v_cond)}

# P5.4a: spot-the-error numbers
_, mdie, _, vdie = moments([1, 2, 3, 4, 5, 6], [F(1, 6)] * 6)
n, p = 10, F(3, 10)
_, _, _, vbin = _binom(n, p)
print(f"P5.4a fair die: E={mdie}={float(mdie)} var={vdie}={float(vdie):.6f}; "
      f"Y=7-X gives X+Y=7 constant so var(X+Y)=0, NOT 2*var(X)="
      f"{float(2 * vdie):.6f}")
print(f"P5.4a var(2X-5) for binomial(10,0.3) = 4*{vbin} = {4 * vbin}={float(4 * vbin)}")
P["p5_4a"] = {"var_die": float(vdie), "two_var_die": float(2 * vdie),
              "var_XplusY_true": 0, "var_binom": float(vbin),
              "var_2Xm5": float(4 * vbin)}

# P5.5a: the discretized uniform variance has the closed form (1 - 1/m^2)/12
print("P5.5a discretized-uniform variance closed form (1-1/m^2)/12:")
_p55 = {}
for m in (4, 10, 100, 1000):
    sup = [F(2 * i + 1, 2 * m) for i in range(m)]
    _, _, _, vv = moments(sup, [F(1, m)] * m)
    cfv = (1 - F(1, m * m)) / 12
    print(f"   m={m:5d}: var={vv}={float(vv):.9f}  closed form={cfv} -> {vv == cfv}")
    _p55[str(m)] = {"var": str(vv), "var_dec": float(vv), "matches_closed_form": vv == cfv}
P["p5_5a"] = {"closed_form": "(1 - 1/m^2)/12", "instances": _p55,
              "gap_to_limit": "1/(12 m^2), so the approach is from below"}

R["practice"] = P

with open(r"d:/Python-UV/MIT_Applied_Prob/computes/g2_s5.json", "w",
          encoding="utf-8") as fh:
    json.dump(R, fh, indent=2)
print()
print("wrote computes/g2_s5.json")
