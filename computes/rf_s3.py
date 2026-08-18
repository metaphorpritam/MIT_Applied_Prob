# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "sympy"]
# ///
"""RF section 3 (Beyond the syllabus: transforms, and a cautionary tale) — every number.

Part A: moment generating functions.  Each table entry M_X(t) is verified TWICE —
symbolically (sympy Sum/Integral of e^{tx} against the pmf/pdf) and numerically at a
test value of t — and the first two moments are recovered by differentiating at t=0.
Then the two payoff results: sum of independent Poissons, sum of independent normals.

Part B: Simpson's paradox — the kidney-stone table (Charig et al. 1986) and the
Jeter/Justice batting averages (1995-96), with every conditional probability, the
total-probability weighting that produces the reversal, and the standardized rates.

Run:  uv run computes/rf_s3.py
Writes computes/rf_s3.json
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict = {}


def show(key, val, note=""):
    if isinstance(val, F):
        R[key] = [val.numerator, val.denominator]
        txt = f"{val}  = {float(val):.6f}"
    elif isinstance(val, float):
        R[key] = val
        txt = f"{val:.6f}"
    elif isinstance(val, (list, tuple)):
        R[key] = [float(v) for v in val]
        txt = "[" + ", ".join(f"{float(v):.6f}" for v in val) + "]"
    else:
        R[key] = val
        txt = str(val)
    print(f"{key:34s} {txt}" + (f"   # {note}" if note else ""))


def head(s):
    print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78)


# =====================================================================
head("A1. MGF table — symbolic verification and moments")
# =====================================================================

t, x, k, n_, p_, lam, a_, b_, mu, sig = sp.symbols(
    "t x k n p lam a b mu sigma", positive=True)
tt = sp.Symbol("t", real=True)

z = sp.Symbol("z", positive=True)   # stands for e^t; sympy sums series in z happily


def first_branch(e):
    """sympy returns Piecewise (convergent branch first) for conditional sums/integrals."""
    return e.replace(lambda a: isinstance(a, sp.Piecewise), lambda a: a.args[0][0])


# --- Bernoulli(p): sum over x in {0,1} -------------------------------
p = sp.Rational(3, 10)
bern_direct = sp.simplify((1 - p) * sp.exp(0 * tt) + p * sp.exp(tt))
bern_closed = 1 - p + p * sp.exp(tt)
bern_ok = sp.simplify(bern_direct - bern_closed) == 0
show("mgf_bernoulli_symbolic_ok", bool(bern_ok), "sum_x e^{tx}p_X(x) == 1-p+pe^t")

# --- Binomial(n,p): binomial theorem ---------------------------------
nB = 5
binom_direct = sp.summation(sp.binomial(nB, x) * p**x * (1 - p)**(nB - x) * sp.exp(tt * x),
                            (x, 0, nB))
binom_closed = (1 - p + p * sp.exp(tt))**nB
binom_ok = sp.simplify(sp.expand(binom_direct) - sp.expand(binom_closed)) == 0
show("mgf_binomial_symbolic_ok", bool(binom_ok), "n=5, p=3/10")

# --- Geometric(p) on {1,2,...}: geometric series ----------------------
geo_direct = first_branch(sp.summation((1 - p)**(x - 1) * p * z**x, (x, 1, sp.oo)))
geo_closed = p * z / (1 - (1 - p) * z)
geo_ok = sp.simplify(geo_direct - geo_closed) == 0
show("mgf_geometric_symbolic_ok", bool(geo_ok), "converges iff e^t(1-p)<1")
show("mgf_geometric_radius", float(-math.log(1 - float(p))),
     "t < -ln(1-p) for p=3/10")

# --- Poisson(lam) ----------------------------------------------------
lm = sp.Rational(3, 2)
pois_direct = first_branch(sp.summation(sp.exp(-lm) * lm**x / sp.factorial(x) * z**x,
                                        (x, 0, sp.oo)))
pois_closed = sp.exp(lm * (z - 1))
pois_ok = sp.simplify(pois_direct - pois_closed) == 0
show("mgf_poisson_symbolic_ok", bool(pois_ok), "lambda=3/2")

# --- Uniform(a,b) ----------------------------------------------------
uni_direct = first_branch(sp.integrate(sp.exp(tt * x) / (b_ - a_), (x, a_, b_)))
uni_closed = (sp.exp(tt * b_) - sp.exp(tt * a_)) / (tt * (b_ - a_))
uni_ok = sp.simplify(uni_direct - uni_closed) == 0
show("mgf_uniform_symbolic_ok", bool(uni_ok), "general a<b, t != 0")

# --- Exponential(lam), t < lam ---------------------------------------
lam_pos = sp.Symbol("lam", positive=True)
t_small = sp.Symbol("t", negative=True)      # guarantees convergence
exp_direct = sp.integrate(lam_pos * sp.exp(-lam_pos * x) * sp.exp(t_small * x), (x, 0, sp.oo))
exp_closed = lam_pos / (lam_pos - t_small)
exp_ok = sp.simplify(exp_direct - exp_closed) == 0
show("mgf_exponential_symbolic_ok", bool(exp_ok), "t<0 branch; extends to t<lambda")

# --- Normal(mu, sigma^2) ---------------------------------------------
mu_r, sg = sp.Symbol("mu", real=True), sp.Symbol("sigma", positive=True)
norm_direct = sp.integrate(
    sp.exp(tt * x) * sp.exp(-(x - mu_r)**2 / (2 * sg**2)) / (sp.sqrt(2 * sp.pi) * sg),
    (x, -sp.oo, sp.oo))
norm_closed = sp.exp(mu_r * tt + sg**2 * tt**2 / 2)
norm_ok = sp.simplify(norm_direct - norm_closed) == 0
show("mgf_normal_symbolic_ok", bool(norm_ok), "general mu, sigma")

# =====================================================================
head("A2. MGF table — numerical spot checks at t = 0.4 (and t = -0.4)")
# =====================================================================

t0 = 0.4
pv, nv, lamv, av, bv, muv, sgv = 0.3, 5, 1.5, 2.0, 6.0, 1.0, 2.0

checks = {}


def num_check(name, direct, closed):
    d, c = float(direct), float(closed)
    show(f"mgf_{name}_direct", d)
    show(f"mgf_{name}_closed", c)
    show(f"mgf_{name}_abserr", abs(d - c))
    checks[name] = abs(d - c)


num_check("bern_num",
          (1 - pv) + pv * math.exp(t0),
          1 - pv + pv * math.exp(t0))
num_check("binom_num",
          sum(math.comb(nv, i) * pv**i * (1 - pv)**(nv - i) * math.exp(t0 * i)
              for i in range(nv + 1)),
          (1 - pv + pv * math.exp(t0))**nv)
# geometric needs t < -ln(1-p) = 0.356675 for p=0.3, so use t=0.2
tg = 0.2
num_check("geom_num",
          sum((1 - pv)**(i - 1) * pv * math.exp(tg * i) for i in range(1, 700)),
          pv * math.exp(tg) / (1 - (1 - pv) * math.exp(tg)))
num_check("pois_num",
          sum(math.exp(-lamv) * lamv**i / math.factorial(i) * math.exp(t0 * i)
              for i in range(0, 60)),
          math.exp(lamv * (math.exp(t0) - 1)))
xs = np.linspace(av, bv, 400001)
num_check("unif_num",
          np.trapezoid(np.exp(t0 * xs) / (bv - av), xs),
          (math.exp(t0 * bv) - math.exp(t0 * av)) / (t0 * (bv - av)))
xe = np.linspace(0, 200, 4000001)
num_check("expo_num",
          np.trapezoid(lamv * np.exp(-lamv * xe) * np.exp(t0 * xe), xe),
          lamv / (lamv - t0))
xn = np.linspace(muv - 60 * sgv, muv + 60 * sgv, 4000001)
num_check("norm_num",
          np.trapezoid(np.exp(t0 * xn) * np.exp(-(xn - muv)**2 / (2 * sgv**2))
                       / (math.sqrt(2 * math.pi) * sgv), xn),
          math.exp(muv * t0 + sgv**2 * t0**2 / 2))
show("mgf_num_maxerr", max(checks.values()), "worst absolute error over the 7 rows")

# =====================================================================
head("A3. Moments by differentiation at t = 0")
# =====================================================================


def moments_from(expr, label, known_mean, known_var):
    m1 = sp.simplify(sp.diff(expr, tt).subs(tt, 0))
    m2 = sp.simplify(sp.diff(expr, tt, 2).subs(tt, 0))
    var = sp.simplify(m2 - m1**2)
    show(f"mom_{label}_M0", float(sp.simplify(expr.subs(tt, 0))), "M(0) must be 1")
    show(f"mom_{label}_mean", float(m1))
    show(f"mom_{label}_EX2", float(m2))
    show(f"mom_{label}_var", float(var))
    show(f"mom_{label}_mean_ok", bool(abs(float(m1) - known_mean) < 1e-12))
    show(f"mom_{label}_var_ok", bool(abs(float(var) - known_var) < 1e-12))


# Poisson(1.5): mean = var = 1.5
moments_from(sp.exp(sp.Rational(3, 2) * (sp.exp(tt) - 1)), "pois", 1.5, 1.5)
# Exponential(1.5): mean 1/lam, var 1/lam^2
moments_from(sp.Rational(3, 2) / (sp.Rational(3, 2) - tt), "expo",
             1 / 1.5, 1 / 1.5**2)
# Normal(1,4): mean 1, var 4
moments_from(sp.exp(1 * tt + 4 * tt**2 / 2), "norm", 1.0, 4.0)
# Bernoulli(0.3): mean p, var p(1-p)
moments_from(sp.Rational(7, 10) + sp.Rational(3, 10) * sp.exp(tt), "bern",
             0.3, 0.3 * 0.7)

# =====================================================================
head("A4. Payoff 1 — sum of independent Poissons")
# =====================================================================

l1, l2 = 1.5, 2.5
prod = sp.simplify(sp.exp(sp.Rational(3, 2) * (sp.exp(tt) - 1))
                   * sp.exp(sp.Rational(5, 2) * (sp.exp(tt) - 1)))
target = sp.exp(4 * (sp.exp(tt) - 1))
show("pois_sum_symbolic_ok", bool(sp.simplify(prod - target) == 0),
     "M_X M_Y = exp(4(e^t-1)) = MGF of Poisson(4)")
show("pois_sum_lambda", l1 + l2)
show("pois_sum_mgf_at_0.4", float(target.subs(tt, 0.4)))
show("pois_sum_prodmgf_at_0.4",
     math.exp(l1 * (math.exp(0.4) - 1)) * math.exp(l2 * (math.exp(0.4) - 1)))


def pois_pmf(lm_, w):
    return math.exp(-lm_) * lm_**w / math.factorial(w)


conv = [sum(pois_pmf(l1, i) * pois_pmf(l2, w - i) for i in range(w + 1)) for w in range(9)]
closed = [pois_pmf(l1 + l2, w) for w in range(9)]
show("pois_conv_pmf", conv, "convolution, w=0..8")
show("pois_closed_pmf", closed, "Poisson(4) pmf, w=0..8")
show("pois_conv_maxerr", max(abs(c - d) for c, d in zip(conv, closed)))

# =====================================================================
head("A5. Payoff 2 — sum of independent normals (matches G3 s4 numbers)")
# =====================================================================

m1n, s1n, m2n, s2n = 0.0, 1.0, 0.0, 2.0
prodN = sp.simplify(sp.exp(0 * tt + 1 * tt**2 / 2) * sp.exp(0 * tt + 4 * tt**2 / 2))
targN = sp.exp(0 * tt + 5 * tt**2 / 2)
show("norm_sum_symbolic_ok", bool(sp.simplify(prodN - targN) == 0),
     "exp(t^2/2)exp(4t^2/2) = exp(5t^2/2) = MGF of N(0,5)")
show("norm_sum_var", s1n**2 + s2n**2)
show("norm_sum_sd", math.sqrt(s1n**2 + s2n**2))


def npdf(w, m, s2):
    return math.exp(-(w - m)**2 / (2 * s2)) / math.sqrt(2 * math.pi * s2)


show("norm_sum_density_0_1_3", [npdf(w, 0.0, 5.0) for w in (0, 1, 3)],
     "matches G3 s4's convolution values 0.178412 / 0.161434 / 0.072537")
# general-parameter check
show("norm_sum_general_ok",
     bool(sp.simplify(sp.exp(mu_r * tt + sg**2 * tt**2 / 2)
                      * sp.exp(2 * mu_r * tt + 9 * sg**2 * tt**2 / 2)
                      - sp.exp(3 * mu_r * tt + 10 * sg**2 * tt**2 / 2)) == 0),
     "N(mu,s^2)+N(2mu,9s^2) = N(3mu,10s^2)")

# Erlang: sum of n iid Exponential(lam) has MGF (lam/(lam-t))^n
n_erl, lam_erl = 3, 2.0
show("erlang_mgf_at_0.5", (lam_erl / (lam_erl - 0.5))**n_erl)
xg = np.linspace(0, 120, 2000001)
erl_pdf = lam_erl**n_erl * xg**(n_erl - 1) * np.exp(-lam_erl * xg) / math.factorial(n_erl - 1)
show("erlang_mgf_numeric", float(np.trapezoid(np.exp(0.5 * xg) * erl_pdf, xg)))
show("erlang_mgf_abserr",
     abs((lam_erl / (lam_erl - 0.5))**n_erl - float(np.trapezoid(np.exp(0.5 * xg) * erl_pdf, xg))))

# =====================================================================
head("B1. Simpson's paradox — kidney stones (Charig et al. 1986)")
# =====================================================================

# B  = treated with PN (percutaneous nephrolithotomy)   -> looks better in aggregate
# Bc = treated with OS (open surgery)                   -> better in BOTH strata
# C  = small stone,  Cc = large stone,  A = treatment succeeds
succ = {("PN", "small"): 234, ("PN", "large"): 55,
        ("OS", "small"): 81,  ("OS", "large"): 192}
tot = {("PN", "small"): 270, ("PN", "large"): 80,
       ("OS", "small"): 87,  ("OS", "large"): 263}

for trt in ("PN", "OS"):
    for st in ("small", "large"):
        fr = F(succ[(trt, st)], tot[(trt, st)])
        show(f"ks_rate_{trt}_{st}", float(fr),
             f"{succ[(trt,st)]}/{tot[(trt,st)]} = {fr}")

for trt in ("PN", "OS"):
    s = succ[(trt, "small")] + succ[(trt, "large")]
    n = tot[(trt, "small")] + tot[(trt, "large")]
    show(f"ks_succ_{trt}", s)
    show(f"ks_n_{trt}", n)
    show(f"ks_rate_{trt}_all", float(F(s, n)), f"{s}/{n} = {F(s,n)}")

show("ks_reversal_small", bool(F(succ[("PN", "small")], tot[("PN", "small")])
                               < F(succ[("OS", "small")], tot[("OS", "small")])),
     "P(A|B,C) < P(A|Bc,C)")
show("ks_reversal_large", bool(F(succ[("PN", "large")], tot[("PN", "large")])
                               < F(succ[("OS", "large")], tot[("OS", "large")])),
     "P(A|B,Cc) < P(A|Bc,Cc)")
show("ks_reversal_aggregate",
     bool(F(succ[("PN", "small")] + succ[("PN", "large")], 350)
          > F(succ[("OS", "small")] + succ[("OS", "large")], 350)),
     "P(A|B) > P(A|Bc)  -- the reversal")

# gaps
show("ks_gap_small", float(F(succ[("OS", "small")], tot[("OS", "small")])
                           - F(succ[("PN", "small")], tot[("PN", "small")])),
     "OS advantage among small stones")
show("ks_gap_large", float(F(succ[("OS", "large")], tot[("OS", "large")])
                           - F(succ[("PN", "large")], tot[("PN", "large")])),
     "OS advantage among large stones")
show("ks_gap_aggregate", float(F(289, 350) - F(273, 350)),
     "PN advantage in the aggregate")

# --- the lurking-variable weights ------------------------------------
for trt in ("PN", "OS"):
    n = tot[(trt, "small")] + tot[(trt, "large")]
    show(f"ks_wsmall_{trt}", float(F(tot[(trt, 'small')], n)),
         f"P(C | {trt}) = {tot[(trt,'small')]}/{n}")
    show(f"ks_wlarge_{trt}", float(F(tot[(trt, 'large')], n)))

# --- total probability check, conditioned throughout on the treatment --
for trt in ("PN", "OS"):
    n = tot[(trt, "small")] + tot[(trt, "large")]
    ws, wl = F(tot[(trt, "small")], n), F(tot[(trt, "large")], n)
    rs = F(succ[(trt, "small")], tot[(trt, "small")])
    rl = F(succ[(trt, "large")], tot[(trt, "large")])
    agg = rs * ws + rl * wl
    show(f"ks_totprob_{trt}", float(agg),
         f"{float(rs):.6f}*{float(ws):.6f} + {float(rl):.6f}*{float(wl):.6f}")
    show(f"ks_totprob_{trt}_exact_ok",
         bool(agg == F(succ[(trt, 'small')] + succ[(trt, 'large')], n)))

# --- direct standardization: give both treatments the SAME case mix ----
n_small = tot[("PN", "small")] + tot[("OS", "small")]
n_large = tot[("PN", "large")] + tot[("OS", "large")]
N = n_small + n_large
w_small, w_large = F(n_small, N), F(n_large, N)
show("ks_pool_nsmall", n_small)
show("ks_pool_nlarge", n_large)
show("ks_pool_N", N)
show("ks_pool_wsmall", float(w_small), f"= {w_small}")
show("ks_pool_wlarge", float(w_large), f"= {w_large}")
for trt in ("PN", "OS"):
    rs = F(succ[(trt, "small")], tot[(trt, "small")])
    rl = F(succ[(trt, "large")], tot[(trt, "large")])
    std = rs * w_small + rl * w_large
    show(f"ks_std_{trt}", float(std), "standardized (common-weight) success rate")
show("ks_std_gap", float((F(81, 87) * w_small + F(192, 263) * w_large)
                         - (F(234, 270) * w_small + F(55, 80) * w_large)),
     "OS minus PN after standardization -- sign restored")

# --- how strongly is the lurking variable tied to the treatment? -------
show("ks_P_C", float(F(n_small, N)), "P(small stone) overall")
show("ks_P_C_given_PN", float(F(270, 350)))
show("ks_P_C_given_OS", float(F(87, 350)))
show("ks_assoc_ratio", float(F(270, 350) / F(87, 350)),
     "P(C|PN)/P(C|OS): stone size is strongly associated with treatment")

# =====================================================================
head("B2. Simpson's paradox — batting averages, Jeter vs Justice 1995-96")
# =====================================================================

bat = {("Jeter", 1995): (12, 48), ("Jeter", 1996): (183, 582),
       ("Justice", 1995): (104, 411), ("Justice", 1996): (45, 140)}
for who in ("Jeter", "Justice"):
    for yr in (1995, 1996):
        h, ab = bat[(who, yr)]
        show(f"bat_{who}_{yr}", float(F(h, ab)), f"{h}/{ab}")
    h = bat[(who, 1995)][0] + bat[(who, 1996)][0]
    ab = bat[(who, 1995)][1] + bat[(who, 1996)][1]
    show(f"bat_{who}_hits", h)
    show(f"bat_{who}_ab", ab)
    show(f"bat_{who}_combined", float(F(h, ab)), f"{h}/{ab}")
    show(f"bat_{who}_w1996", float(F(bat[(who, 1996)][1], ab)),
         "fraction of at-bats in the (easier) 1996 season")
show("bat_gap_1995", float(F(104, 411) - F(12, 48)), "Justice minus Jeter, 1995")
show("bat_gap_1996", float(F(45, 140) - F(183, 582)), "Justice minus Jeter, 1996")
show("bat_gap_combined", float(F(195, 630) - F(149, 551)), "Jeter minus Justice, combined")
show("prac32_p0", 0.7**5, "P(W=0) for Bin(5,0.3)")
show("bat_reversal_ok",
     bool(F(104, 411) > F(12, 48) and F(45, 140) > F(183, 582)
          and F(195, 630) > F(149, 551)),
     "Justice better each year, Jeter better combined")

# --- the no-reversal theorem: equal weights kill the paradox ----------
w = F(1, 2)
show("noreversal_demo",
     float((F(234, 270) * w + F(55, 80) * w) - (F(81, 87) * w + F(192, 263) * w)),
     "with EQUAL weights the aggregate gap has the stratum sign (negative = OS better)")

Path(__file__).with_suffix(".json").write_text(
    json.dumps(R, indent=1, sort_keys=True), encoding="utf-8")
print(f"\nwrote {Path(__file__).with_suffix('.json')}  ({len(R)} keys)")
