# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""G4 section 1 (Conditional expectation as a r.v.; iterated expectations; total variance)
— every number that appears in notes/src/fragments/g4_s1.html.

Run:  uv run computes/g4_s1.py
Writes computes/g4_s1.json
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy import integrate

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict = {}


def show(key, val, note=""):
    if isinstance(val, F):
        R[key] = [val.numerator, val.denominator]
        txt = f"{val}  = {float(val):.6f}"
    elif isinstance(val, float):
        R[key] = val
        txt = f"{val:.6f}"
    else:
        R[key] = val
        txt = str(val)
    print(f"  {key:34s} = {txt}" + (f"   [{note}]" if note else ""))


def head(t):
    print("\n" + t)
    print("-" * len(t))


# ----------------------------------------------------------------------------
head("A. Section means and variances (L12 slides 4-5)")
# 30 students: 10 in section y=1 with mean 90 and within-variance 10,
#              20 in section y=2 with mean 60 and within-variance 20.
n1, n2 = 10, 20
m1, m2 = F(90), F(60)
v1, v2 = F(10), F(20)
n = n1 + n2
p1, p2 = F(n1, n), F(n2, n)
show("sec_p1", p1, "P(Y=1) = 10/30")
show("sec_p2", p2, "P(Y=2) = 20/30")
EX = p1 * m1 + p2 * m2
show("sec_EX", EX, "E[X] = (90*10+60*20)/30")
show("sec_EX_direct", F(90 * 10 + 60 * 20, 30))
# var(E[X|Y]) two ways
varEc = p1 * (m1 - EX) ** 2 + p2 * (m2 - EX) ** 2
show("sec_varE", varEc, "var(E[X|Y]) definition form")
E_of_sq = p1 * m1 ** 2 + p2 * m2 ** 2
show("sec_E_condmean_sq", E_of_sq, "E[(E[X|Y])^2]")
show("sec_varE_alt", E_of_sq - EX ** 2, "E[(E[X|Y])^2] - (E[X])^2")
EvarC = p1 * v1 + p2 * v2
show("sec_Evar", EvarC, "E[var(X|Y)] = (1/3)10 + (2/3)20")
show("sec_Evar_dec", float(EvarC))
varX = EvarC + varEc
show("sec_varX", varX, "total variance")
show("sec_varX_dec", float(varX))
show("sec_within_share", float(EvarC / varX))
show("sec_between_share", float(varEc / varX))
# explicit 30-point population realizing these numbers (used for the figure):
#   section 1: 90 +/- sqrt(10); section 2: 60 +/- sqrt(20)
s1 = [90 + math.sqrt(10)] * 5 + [90 - math.sqrt(10)] * 5
s2 = [60 + math.sqrt(20)] * 10 + [60 - math.sqrt(20)] * 10
pop = np.array(s1 + s2)
show("sec_pop_mean", float(pop.mean()), "population check")
show("sec_pop_var", float(pop.var()), "population check = 650/3")

# ----------------------------------------------------------------------------
head("B. Stick breaking (L12 slide 2; B&T Example 4.17)")
# Y ~ U(0, ell); X | {Y=y} ~ U(0, y).  Report coefficients of ell and ell^2.
show("stick_EY_coef", F(1, 2), "E[Y] = ell/2")
show("stick_EcondX", "Y/2", "E[X|Y] = Y/2")
show("stick_EX_coef", F(1, 4), "E[X] = ell/4")
show("stick_varY_coef", F(1, 12), "var(Y) = ell^2/12")
show("stick_varE_coef", F(1, 48), "var(E[X|Y]) = var(Y/2) = ell^2/48")
show("stick_EY2_coef", F(1, 3), "E[Y^2] = ell^2/3")
show("stick_Evar_coef", F(1, 36), "E[var(X|Y)] = E[Y^2]/12 = ell^2/36")
show("stick_varX_coef", F(1, 36) + F(1, 48), "var(X) = ell^2 * 7/144")
show("stick_varX_dec", float(F(7, 144)))
# ell = 1 numeric + Monte-Carlo cross-check
rng = np.random.default_rng(20101019)
Ysim = rng.uniform(0, 1, 4_000_000)
Xsim = rng.uniform(0, 1, 4_000_000) * Ysim
show("stick_EX_mc", float(Xsim.mean()), "MC vs 0.25")
show("stick_varX_mc", float(Xsim.var()), "MC vs 7/144 = 0.048611")
# marginal density of X for the figure: f_X(x) = ln(1/x) on (0,1)
show("stick_fX_check", float(integrate.quad(lambda x: math.log(1 / x), 1e-14, 1)[0]),
     "integral of ln(1/x) on (0,1) = 1")
show("stick_EX_quad", float(integrate.quad(lambda x: x * math.log(1 / x), 1e-14, 1)[0]))
show("stick_EX2_quad", float(integrate.quad(lambda x: x * x * math.log(1 / x), 1e-14, 1)[0]),
     "E[X^2] = 1/9")
show("stick_varX_quad", float(integrate.quad(lambda x: x * x * math.log(1 / x), 1e-14, 1)[0]
                              - 0.25 ** 2))

# ----------------------------------------------------------------------------
head("C. L12 slide 6 UNSOLVED EXAMPLE: two-piece density 1/3 on [0,1], 2/3 on [1,2]")
q1, q2 = F(1, 3), F(2, 3)          # P(Y=1), P(Y=2)
show("q_pY1", q1)
show("q_pY2", q2)
# conditional densities: uniform on [0,1] and uniform on [1,2]
qm1, qm2 = F(1, 2), F(3, 2)
show("q_EX_Y1", qm1, "midpoint of [0,1]")
show("q_EX_Y2", qm2, "midpoint of [1,2]")
qv1, qv2 = F(1, 12), F(1, 12)
show("q_var_Y1", qv1, "(1-0)^2/12")
show("q_var_Y2", qv2, "(2-1)^2/12")
qEX = q1 * qm1 + q2 * qm2
show("q_EX", qEX, "law of iterated expectations")
show("q_EX_dec", float(qEX))
q_Esq = q1 * qm1 ** 2 + q2 * qm2 ** 2
show("q_E_condmean_sq", q_Esq, "E[(E[X|Y])^2] = (1/3)(1/4)+(2/3)(9/4)")
q_varE = q_Esq - qEX ** 2
show("q_varE", q_varE, "var(E[X|Y])")
show("q_varE_dev", q1 * (qm1 - qEX) ** 2 + q2 * (qm2 - qEX) ** 2, "same by deviation form")
show("q_varE_dec", float(q_varE))
q_Evar = q1 * qv1 + q2 * qv2
show("q_Evar", q_Evar, "E[var(X|Y)]")
q_varX = q_Evar + q_varE
show("q_varX", q_varX, "law of total variance")
show("q_varX_dec", float(q_varX))
# direct check from the density
fq = lambda x: (1 / 3) if 0 <= x <= 1 else ((2 / 3) if 1 < x <= 2 else 0.0)
m_dir = integrate.quad(lambda x: x * fq(x), 0, 2, points=[1])[0]
m2_dir = integrate.quad(lambda x: x * x * fq(x), 0, 2, points=[1])[0]
show("q_EX_direct", float(m_dir))
show("q_EX2_direct", float(m2_dir), "E[X^2] = 5/3")
show("q_varX_direct", float(m2_dir - m_dir ** 2), "= 11/36")
show("q_area_check", float(integrate.quad(fq, 0, 2, points=[1])[0]))

# ----------------------------------------------------------------------------
head("D. B&T Example 4.21 (companion: 1/2 on [0,1], 1/4 on [1,3])")
b1, b2 = F(1, 2), F(1, 2)
bm1, bm2 = F(1, 2), F(2)
bv1, bv2 = F(1, 12), F(4, 12)
bEX = b1 * bm1 + b2 * bm2
show("bt_EX", bEX, "5/4")
bt_varE = b1 * (bm1 - bEX) ** 2 + b2 * (bm2 - bEX) ** 2
show("bt_varE", bt_varE, "9/16")
bt_Evar = b1 * bv1 + b2 * bv2
show("bt_Evar", bt_Evar, "5/24")
show("bt_varX", bt_Evar + bt_varE, "37/48")
show("bt_varX_dec", float(bt_Evar + bt_varE))

# ----------------------------------------------------------------------------
head("E. Coin with random bias (B&T Example 4.16), n = 10")
nc = 10
show("coin_n", nc)
show("coin_EY", F(1, 2))
show("coin_EY2", F(1, 3))
show("coin_varY", F(1, 12))
show("coin_EX", F(nc, 2), "E[X] = n/2")
show("coin_Evar", F(nc, 6), "E[nY(1-Y)] = n(E[Y]-E[Y^2]) = n/6")
show("coin_varE", F(nc ** 2, 12), "var(nY) = n^2/12")
coin_var = F(nc, 6) + F(nc ** 2, 12)
show("coin_varX", coin_var, "n/6 + n^2/12")
show("coin_varX_dec", float(coin_var))
# Monte-Carlo cross-check
Yc = rng.uniform(0, 1, 2_000_000)
Xc = rng.binomial(nc, Yc)
show("coin_EX_mc", float(Xc.mean()))
show("coin_varX_mc", float(Xc.var()))

# ----------------------------------------------------------------------------
head("F. Widget check: two-group mixture decomposer  (w-g4s1-vardecomp)")
def decomp(p, mu1, mu2, s1_, s2_):
    """p = P(Y=1); group means mu, group sds s.  Returns (E[X], E[var], var(E), var)."""
    q = 1 - p
    ex = p * mu1 + q * mu2
    ev = p * s1_ ** 2 + q * s2_ ** 2
    ve = p * (mu1 - ex) ** 2 + q * (mu2 - ex) ** 2
    return ex, ev, ve, ev + ve


for (p, a, b, sa, sb) in [(0.5, 0.0, 0.0, 1.0, 1.0),
                          (1 / 3, 90.0, 60.0, math.sqrt(10), math.sqrt(20)),
                          (0.25, -2.0, 1.0, 0.5, 1.5),
                          (0.7, 3.0, 3.0, 2.0, 0.5)]:
    ex, ev, ve, vt = decomp(p, a, b, sa, sb)
    tag = f"w p={p:.4f} mu=({a},{b}) sd=({sa:.4f},{sb:.4f})"
    print(f"  {tag}")
    print(f"      E[X]={ex:.6f}  E[var(X|Y)]={ev:.6f}  var(E[X|Y])={ve:.6f}  var(X)={vt:.6f}")
    # brute-force check by sampling the mixture
    m = 400_000
    g = rng.random(m) < p
    xs = np.where(g, rng.normal(a, sa, m), rng.normal(b, sb, m))
    print(f"      MC: mean={xs.mean():.4f}  var={xs.var():.4f}")
R["widget_cases"] = [
    dict(p=p, mu1=a, mu2=b, sd1=sa, sd2=sb,
         EX=decomp(p, a, b, sa, sb)[0], Evar=decomp(p, a, b, sa, sb)[1],
         varE=decomp(p, a, b, sa, sb)[2], varX=decomp(p, a, b, sa, sb)[3])
    for (p, a, b, sa, sb) in [(1 / 3, 90.0, 60.0, math.sqrt(10), math.sqrt(20)),
                              (0.5, 0.0, 4.0, 1.0, 1.0),
                              (0.5, 2.0, 2.0, 1.0, 3.0)]
]
ex, ev, ve, vt = decomp(0.5, 0.0, 4.0, 1.0, 1.0)
show("wid_b_EX", ex); show("wid_b_Evar", ev); show("wid_b_varE", ve); show("wid_b_varX", vt)
ex, ev, ve, vt = decomp(0.5, 2.0, 2.0, 1.0, 3.0)
show("wid_c_EX", ex); show("wid_c_Evar", ev); show("wid_c_varE", ve); show("wid_c_varX", vt)

# ----------------------------------------------------------------------------
head("G. rec12 P2 — Romeo & Juliet, Z = X - Y, Laplace density")
lam = 1.0
fZ = lambda z: (lam / 2) * math.exp(-lam * abs(z))
show("rj_norm", float(integrate.quad(fZ, -60, 60)[0]), "density integrates to 1")
show("rj_mean", float(integrate.quad(lambda z: z * fZ(z), -60, 60)[0]))
show("rj_var", float(integrate.quad(lambda z: z * z * fZ(z), -60, 60)[0]), "= 2/lambda^2")
show("rj_var_formula", 2 / lam ** 2)
show("rj_P_pos", float(integrate.quad(fZ, 0, 60)[0]), "P(Z>0) = 1/2")
show("rj_P_abs_le_1", float(integrate.quad(fZ, -1, 1)[0]), "1 - e^{-1}")
show("rj_1_minus_exp", 1 - math.exp(-1))
# CDF checks at a couple of points
show("rj_F_at_1", 1 - 0.5 * math.exp(-lam * 1))
show("rj_F_at_m1", 0.5 * math.exp(-lam * 1))
# Monte-Carlo
Xr = rng.exponential(1 / lam, 3_000_000)
Yr = rng.exponential(1 / lam, 3_000_000)
Zr = Xr - Yr
show("rj_mean_mc", float(Zr.mean()))
show("rj_var_mc", float(Zr.var()))
# variance the fast way: var(X-Y) = var(X)+var(Y) = 1/lam^2 + 1/lam^2
show("rj_var_indep", 1 / lam ** 2 + 1 / lam ** 2)

# ----------------------------------------------------------------------------
head("H. rec12 P3 — polar coordinates of a standard normal pair (Rayleigh)")
fR = lambda r: r * math.exp(-r * r / 2)
show("ray_norm", float(integrate.quad(fR, 0, 40)[0]))
show("ray_ER", float(integrate.quad(lambda r: r * fR(r), 0, 40)[0]), "sqrt(pi/2)")
show("ray_ER_closed", math.sqrt(math.pi / 2))
show("ray_ER2", float(integrate.quad(lambda r: r * r * fR(r), 0, 40)[0]), "= 2")
show("ray_varR", float(integrate.quad(lambda r: r * r * fR(r), 0, 40)[0]
                       - (math.sqrt(math.pi / 2)) ** 2))
show("ray_varR_closed", 2 - math.pi / 2)
show("ray_median", math.sqrt(2 * math.log(2)), "F_R(r)=1/2")
show("ray_P_le_1", 1 - math.exp(-0.5))
# joint factorization check on a grid
rr = np.linspace(0.01, 8, 900)
tt = np.linspace(0, 2 * math.pi, 400)
Rg, Tg = np.meshgrid(rr, tt, indexing="ij")
joint = (1 / (2 * math.pi)) * Rg * np.exp(-Rg ** 2 / 2)
prod = (Rg * np.exp(-Rg ** 2 / 2)) * (1 / (2 * math.pi))
show("ray_factor_maxerr", float(np.abs(joint - prod).max()), "f_{R,Theta} = f_R f_Theta")
# MC: R and Theta from standard normals
Xn = rng.normal(0, 1, 2_000_000)
Yn = rng.normal(0, 1, 2_000_000)
Rm = np.hypot(Xn, Yn)
show("ray_ER_mc", float(Rm.mean()))
show("ray_ER2_mc", float((Rm ** 2).mean()))
# R^2 is exponential(1/2)
show("ray_R2_mean_mc", float((Rm ** 2).mean()), "exponential with lambda=1/2 has mean 2")

# ----------------------------------------------------------------------------
head("I. rec12 P4 — Schwarz inequality, numeric illustration")
# X uniform on {-1,0,1,2}; Y = X^2 - 1
xs = np.array([-1.0, 0.0, 1.0, 2.0])
ys = xs ** 2 - 1
EXY = float((xs * ys).mean())
EX2 = float((xs ** 2).mean())
EY2 = float((ys ** 2).mean())
show("sch_EXY", EXY)
show("sch_EX2", EX2)
show("sch_EY2", EY2)
show("sch_lhs", EXY ** 2, "(E[XY])^2")
show("sch_rhs", EX2 * EY2, "E[X^2]E[Y^2]")
show("sch_alpha_star", EXY / EY2, "minimizing alpha")
Jmin = EX2 - EXY ** 2 / EY2
show("sch_Jmin", Jmin, "J(alpha*) >= 0")
show("sch_cos", EXY / math.sqrt(EX2 * EY2), "E[XY]/sqrt(E[X^2]E[Y^2]) — Schwarz ratio, NOT rho")
show("sch_EX", float(xs.mean()))
show("sch_EY", float(ys.mean()))
# equality case: Y = 3X
ys2 = 3 * xs
show("sch_eq_lhs", float((xs * ys2).mean()) ** 2)
show("sch_eq_rhs", float((xs ** 2).mean()) * float((ys2 ** 2).mean()))

# ----------------------------------------------------------------------------
head("J. rec12 P1 — correlation invariance, numeric illustration")
xh = np.array([70.0, 85.0, 90.0, 60.0, 95.0])   # homework scores
ye = np.array([65.0, 80.0, 88.0, 55.0, 92.0])   # exam scores
rho = float(np.corrcoef(xh, ye)[0, 1])
show("corr_rho", rho)
a, b = 105 / 100, -3.0
show("corr_a", a)
show("corr_b", b)
show("corr_rho_affine", float(np.corrcoef(a * xh + b, ye)[0, 1]), "unchanged")
show("corr_rho_negative_a", float(np.corrcoef(-a * xh + b, ye)[0, 1]), "sign flips when a<0")
show("corr_cov", float(np.cov(xh, ye, bias=True)[0, 1]))
show("corr_var_x", float(xh.var()))
show("corr_var_y", float(ye.var()))

# ----------------------------------------------------------------------------
head("K. Practice-question answers")
# Practice 1.1 — fair die, Y = 1 if even
odd, even = np.array([1.0, 3.0, 5.0]), np.array([2.0, 4.0, 6.0])
show("pr1_EX_odd", F(3), "(1+3+5)/3")
show("pr1_EX_even", F(4), "(2+4+6)/3")
show("pr1_EX", F(7, 2))
show("pr1_varE", F(1, 4), "(1/2)(3-3.5)^2+(1/2)(4-3.5)^2")
show("pr1_var_within", F(8, 3), "((-2)^2+0+2^2)/3")
show("pr1_Evar", F(8, 3))
show("pr1_varX", F(8, 3) + F(1, 4), "= 35/12")
show("pr1_varX_dec", float(F(35, 12)))
show("pr1_varX_direct", float(np.arange(1, 7).var()))

# Practice 1.2 — N uniform on {1,2,3,4}, X | N uniform on {1,...,N}
Ns = [1, 2, 3, 4]
pN = F(1, 4)
EN = sum(pN * F(k) for k in Ns)
EN2 = sum(pN * F(k) ** 2 for k in Ns)
show("pr2_EN", EN)
show("pr2_EN2", EN2)
show("pr2_varN", EN2 - EN ** 2)
condmean = {k: F(k + 1, 2) for k in Ns}
show("pr2_EX", sum(pN * condmean[k] for k in Ns), "(E[N]+1)/2")
condvar = {k: F(k * k - 1, 12) for k in Ns}
pr2_Evar = sum(pN * condvar[k] for k in Ns)
show("pr2_Evar", pr2_Evar, "E[(N^2-1)/12]")
pr2_varE = (EN2 - EN ** 2) / 4
show("pr2_varE", pr2_varE, "var((N+1)/2) = var(N)/4")
show("pr2_varX", pr2_Evar + pr2_varE)
show("pr2_varX_dec", float(pr2_Evar + pr2_varE))
# brute force over the joint PMF
vals, probs = [], []
for k in Ns:
    for x in range(1, k + 1):
        vals.append(x); probs.append(float(pN) / k)
vals = np.array(vals); probs = np.array(probs)
mu = float((vals * probs).sum())
show("pr2_EX_brute", mu)
show("pr2_varX_brute", float((vals ** 2 * probs).sum() - mu ** 2))
show("pr2_prob_total", float(probs.sum()))

# Practice 1.3 — mixture: with prob 0.4, X ~ N(0,1); else X ~ N(5, 2^2)
pm = 0.4
ex, ev, ve, vt = decomp(pm, 0.0, 5.0, 1.0, 2.0)
show("pr3_EX", ex)
show("pr3_Evar", ev)
show("pr3_varE", ve)
show("pr3_varX", vt)
show("pr3_sd", math.sqrt(vt))
show("pr3_between_share", ve / vt)

# Practice 1.4 — stick broken three times
show("pr4_EX3_coef", F(1, 8), "E[X3] = ell/8")
show("pr4_varE_coef", F(7, 576), "var(E[X3|X2]) = var(X2/2) = (7/144)/4")
show("pr4_EX2sq_coef", F(1, 9), "E[X2^2] = var+mean^2 = 7/144+1/16 = 1/9")
show("pr4_Evar_coef", F(1, 108), "E[X2^2]/12")
pr4 = F(7, 576) + F(1, 108)
show("pr4_varX3_coef", pr4, "var(X3)/ell^2")
show("pr4_varX3_dec", float(pr4))
X3 = rng.uniform(0, 1, 3_000_000) * Xsim[:3_000_000]
show("pr4_EX3_mc", float(X3.mean()))
show("pr4_varX3_mc", float(X3.var()))

# Practice 1.5 — Laplace tail
show("pr5_P_gt_2", float(integrate.quad(fZ, 2, 60)[0]), "(1/2)e^{-2}")
show("pr5_closed", 0.5 * math.exp(-2))

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(R, indent=1), encoding="utf-8")
print(f"\nwrote {out}")
