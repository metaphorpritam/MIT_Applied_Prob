# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""G3 section 4 (Derived distributions and convolution) — every number in the fragment.

Run:  uv run computes/g3_s4.py
Writes computes/g3_s4.json
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
        txt = f"{val:.8f}"
    else:
        R[key] = val
        txt = str(val)
    print(f"{key:44s} = {txt}   {note}")


def fs(x: F) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


# ===================================================================
# 4.1  Linear case Y = aX + b   (L11 slide 2 special case, B&T Fig 4.2)
# ===================================================================
print("\n=== 4.1  Y = aX+b : X ~ U(0,1), a=2, b=3  ->  U(3,5) ===")
a, b = 2.0, 3.0
show("lin_a", a)
show("lin_b", b)
show("lin_fY", 1.0 / abs(a), "f_Y(y) = 1/|a| on [3,5]")
show("lin_mean_X", 0.5)
show("lin_mean_Y", a * 0.5 + b)
show("lin_var_X", 1.0 / 12.0)
show("lin_var_Y", a ** 2 / 12.0)
# negative-slope check: a = -2, b = 1 -> U(-1,1)
show("lin_neg_lo", -2.0 * 1 + 1.0)
show("lin_neg_hi", -2.0 * 0 + 1.0)

print("\n=== 4.1b  Y = X^2 for X ~ U(0,1)  ->  f_Y(y) = 1/(2 sqrt y) ===")
show("sq_norm", float(integrate.quad(lambda y: 1 / (2 * math.sqrt(y)), 0, 1)[0]))
show("sq_mean", float(integrate.quad(lambda y: y / (2 * math.sqrt(y)), 0, 1)[0]), "= E[X^2] = 1/3")
show("sq_F_at_0.25", 0.5, "F_Y(0.25)=sqrt(0.25)=0.5")

print("\n=== 4.1c  inverse transform: X~U(0,1), Y = -(1/lam) ln(1-X), lam=2 ===")
lam = 2.0
rng = np.random.default_rng(20101014)
u = rng.random(2_000_000)
y = -np.log(1 - u) / lam
show("invtr_lambda", lam)
show("invtr_mean_theory", 1 / lam)
show("invtr_mean_mc", float(y.mean()))
show("invtr_var_theory", 1 / lam ** 2)
show("invtr_var_mc", float(y.var()))

# ===================================================================
# 4.2  Monotonic change of variables — check on Y = e^X, X ~ Exp(1)
# ===================================================================
print("\n=== 4.2  Y = e^X for X ~ Exp(1):  f_Y(y) = 1/y^2 on y>1 (Pareto) ===")
show("pareto_norm", float(integrate.quad(lambda t: 1 / t ** 2, 1, np.inf)[0]))
show("pareto_P_Y_le_3", float(integrate.quad(lambda t: 1 / t ** 2, 1, 3)[0]), "= 1 - 1/3 = 2/3")

# ===================================================================
# 4.3  Z = Y/X on the unit square   (L11 slide 1 UNSOLVED; B&T Ex 4.8)
# ===================================================================
print("\n=== 4.3  Z = Y/X, (X,Y) uniform on the unit square ===")


def F_Z(z):
    if z <= 0:
        return 0.0
    return z / 2 if z <= 1 else 1 - 1 / (2 * z)


def f_Z(z):
    if z <= 0:
        return 0.0
    return 0.5 if z <= 1 else 1 / (2 * z * z)


for zz in (0.5, 1.0, 2.0, 4.0):
    show(f"ratio_F_{zz}", float(F_Z(zz)))
    show(f"ratio_f_{zz}", float(f_Z(zz)))
show("ratio_norm_lo", float(integrate.quad(f_Z, 0, 1)[0]), "mass on (0,1]")
show("ratio_norm_hi", float(integrate.quad(f_Z, 1, np.inf)[0]), "mass on (1,inf)")
show("ratio_norm_tot", float(integrate.quad(f_Z, 0, 1)[0] + integrate.quad(f_Z, 1, np.inf)[0]))
show("ratio_median", 1.0, "F_Z(1)=1/2 so median is exactly 1")
for M in (10, 100, 1000):
    tail = float(integrate.quad(lambda t: t * f_Z(t), 1, M)[0])
    show(f"ratio_partial_mean_M{M}", 0.25 + tail, "= 1/4 + (1/2)ln M  -> diverges")
    show(f"ratio_halflog_M{M}", 0.25 + 0.5 * math.log(M))
# Monte-Carlo cross check of the CDF
X = rng.random(4_000_000)
Y = rng.random(4_000_000)
Zs = Y / X
for zz in (0.5, 1.0, 2.0, 4.0):
    show(f"ratio_F_{zz}_mc", float((Zs <= zz).mean()))

# ===================================================================
# 4.4  rec11 P3 :  X ~ N(0,1),  Y = g(X),  g(t) = -t (t<=0), sqrt(t) (t>0)
# ===================================================================
print("\n=== 4.4  rec11 P3 ===")


def fX_std(t):
    return math.exp(-t * t / 2) / math.sqrt(2 * math.pi)


def f_Y_rec(yv):
    if yv <= 0:
        return 0.0
    return (2 * yv * math.exp(-(yv ** 4) / 2) + math.exp(-(yv ** 2) / 2)) / math.sqrt(2 * math.pi)


show("rec_norm", float(integrate.quad(f_Y_rec, 0, np.inf)[0]), "must be 1")
for yv in (0.25, 0.5, 1.0, 1.5, 2.0):
    show(f"rec_fY_{yv}", float(f_Y_rec(yv)))
show("rec_mean", float(integrate.quad(lambda t: t * f_Y_rec(t), 0, np.inf)[0]))
show("rec_var", float(integrate.quad(lambda t: t * t * f_Y_rec(t), 0, np.inf)[0])
     - float(integrate.quad(lambda t: t * f_Y_rec(t), 0, np.inf)[0]) ** 2)
show("rec_branchmass_left", 0.5, "P(X<=0) = mass contributed by the -t branch")
show("rec_branchmass_right", 0.5)
# the two sub-integrals separately
show("rec_int_sqrtbranch", float(integrate.quad(
    lambda t: 2 * t * math.exp(-(t ** 4) / 2) / math.sqrt(2 * math.pi), 0, np.inf)[0]))
show("rec_int_linbranch", float(integrate.quad(
    lambda t: math.exp(-(t ** 2) / 2) / math.sqrt(2 * math.pi), 0, np.inf)[0]))
# Monte-Carlo cross check
xs = rng.standard_normal(4_000_000)
ys = np.where(xs <= 0, -xs, np.sqrt(np.abs(xs)))
show("rec_mean_mc", float(ys.mean()))
show("rec_P_Y_le_1_mc", float((ys <= 1).mean()))
show("rec_P_Y_le_1", float(integrate.quad(f_Y_rec, 0, 1)[0]))
# closed form of P(Y<=1) = F_X(1) - F_X(-1) ... careful: F_X(y^2) - F_X(-y) at y=1
from scipy.stats import norm as _norm  # noqa: E402
show("rec_P_Y_le_1_closed", float(_norm.cdf(1.0) - _norm.cdf(-1.0)))

# ===================================================================
# 4.5  Discrete convolution  (L11 slide 3)
# ===================================================================
print("\n=== 4.5  discrete convolution example ===")
pX = {0: F(1, 6), 1: F(1, 3), 2: F(1, 2)}
pY = {0: F(1, 4), 1: F(1, 4), 2: F(1, 2)}
show("disc_pX", [fs(v) for v in pX.values()])
show("disc_pY", [fs(v) for v in pY.values()])
pW = {}
terms = {}
for w in range(0, 5):
    tt = []
    s = F(0)
    for x in sorted(pX):
        if (w - x) in pY:
            s += pX[x] * pY[w - x]
            tt.append(f"p_X({x})p_Y({w-x}) = {fs(pX[x])}*{fs(pY[w-x])} = {fs(pX[x]*pY[w-x])}")
    pW[w] = s
    terms[w] = tt
    show(f"disc_pW_{w}", s, " + ".join(tt))
show("disc_pW_sum", sum(pW.values()))
R["disc_terms"] = terms
R["disc_pW_frac"] = {str(k): fs(v) for k, v in pW.items()}
mX = sum(F(k) * v for k, v in pX.items())
mY = sum(F(k) * v for k, v in pY.items())
mW = sum(F(k) * v for k, v in pW.items())
show("disc_EX", mX)
show("disc_EY", mY)
show("disc_EW", mW, "= E[X]+E[Y] check")
vX = sum(v * (F(k) - mX) ** 2 for k, v in pX.items())
vY = sum(v * (F(k) - mY) ** 2 for k, v in pY.items())
vW = sum(v * (F(k) - mW) ** 2 for k, v in pW.items())
show("disc_varX", vX)
show("disc_varY", vY)
show("disc_varW", vW, "= var X + var Y check")
show("disc_var_sum_check", vX + vY)
# numpy cross-check
npW = np.convolve([1 / 6, 1 / 3, 1 / 2], [1 / 4, 1 / 4, 1 / 2])
show("disc_pW_numpy", [round(float(t), 10) for t in npW])

# ===================================================================
# 4.6  Sum of two uniforms — triangular PDF
# ===================================================================
print("\n=== 4.6  W = X+Y, X,Y ~ U(0,1) independent ===")


def f_tri(w):
    if 0 <= w <= 1:
        return w
    if 1 < w <= 2:
        return 2 - w
    return 0.0


show("tri_norm", float(integrate.quad(f_tri, 0, 2)[0]))
show("tri_mean", float(integrate.quad(lambda t: t * f_tri(t), 0, 2)[0]))
show("tri_var", float(integrate.quad(lambda t: t * t * f_tri(t), 0, 2)[0]) - 1.0)
show("tri_var_frac", fs(F(1, 6)))
for wv in (0.3, 0.5, 1.0, 1.5, 1.7):
    show(f"tri_f_{wv}", float(f_tri(wv)))
show("tri_overlap_len_w0.3", 0.3)
show("tri_overlap_len_w1.5", 0.5)
show("tri_P_W_le_1", float(integrate.quad(f_tri, 0, 1)[0]))

print("\n=== 4.6b  U(0,1) + Exp(1) and Exp(1)+Exp(1) closed forms ===")
show("uexp_at_0.5", float(1 - math.exp(-0.5)))
show("uexp_at_1.5", float(math.exp(-1.5) * (math.e - 1)))
show("expexp_at_1", float(1 * math.exp(-1)), "w e^{-w} at w=1 (Erlang-2)")

# ===================================================================
# 4.7  Sum of independent normals — constants c and gamma  (L11 slide 6)
# ===================================================================
print("\n=== 4.7  W = X+Y, X~N(0,sx^2), Y~N(0,sy^2) ===")
sx, sy = 1.0, 2.0
s2 = sx ** 2 + sy ** 2
show("norm_sx", sx)
show("norm_sy", sy)
show("norm_varW", s2)
show("norm_sdW", math.sqrt(s2))
show("norm_a_const", 1 / (2 * sx ** 2) + 1 / (2 * sy ** 2), "a = 1/2sx^2 + 1/2sy^2")
show("norm_a_closed", s2 / (2 * sx ** 2 * sy ** 2))
show("norm_gamma", 1 / (2 * s2), "gamma = 1/(2(sx^2+sy^2))")
show("norm_c", 1 / math.sqrt(2 * math.pi * s2), "c = 1/sqrt(2 pi (sx^2+sy^2))")
show("norm_sqrt_pi_over_a", math.sqrt(math.pi / (s2 / (2 * sx ** 2 * sy ** 2))))
# numerical convolution check at a few w
for wv in (0.0, 1.0, 3.0):
    num = integrate.quad(lambda t: math.exp(-t ** 2 / (2 * sx ** 2)) *
                         math.exp(-(wv - t) ** 2 / (2 * sy ** 2)),
                         -np.inf, np.inf)[0] / (2 * math.pi * sx * sy)
    show(f"norm_conv_{wv}", float(num))
    show(f"norm_closed_{wv}", float(math.exp(-wv ** 2 / (2 * s2)) / math.sqrt(2 * math.pi * s2)))

# ===================================================================
# 4.7b  Binomial additivity: Bin(n1,p) + Bin(n2,p) = Bin(n1+n2,p)
# ===================================================================
print("\n=== 4.7b  W = X+Y, X~Bin(n1,p), Y~Bin(n2,p) independent ===")
n1b, n2b, pb = 2, 3, F(3, 10)


def binpmf(n, p, k):
    return F(math.comb(n, k)) * p ** k * (1 - p) ** (n - k)


binconv = [sum(binpmf(n1b, pb, x) * binpmf(n2b, pb, w - x)
               for x in range(0, n1b + 1) if 0 <= w - x <= n2b)
           for w in range(0, n1b + n2b + 1)]
binclosed = [binpmf(n1b + n2b, pb, w) for w in range(0, n1b + n2b + 1)]
show("binadd_conv", [fs(v) for v in binconv], "convolution of Bin(2,3/10) and Bin(3,3/10)")
show("binadd_closed", [fs(v) for v in binclosed], "Bin(5,3/10) pmf")
show("binadd_exact_match", binconv == binclosed, "identical as exact fractions")
show("binadd_maxerr", max(abs(float(a) - float(b)) for a, b in zip(binconv, binclosed)))
show("binadd_conv_2", binconv[2], "w=2 term")
# different p: the sum is NOT binomial.  Bin(1,1/5) + Bin(1,4/5)
pa, pc = F(1, 5), F(4, 5)
bad2 = pa * pc
bad1 = pa * (1 - pc) + (1 - pa) * pc
show("binadd_bad_p2", bad2, "P(W=2) with p1=1/5, p2=4/5")
show("binadd_bad_p1", bad1, "P(W=1) with p1=1/5, p2=4/5")
show("binadd_bad_fit_p", float(math.sqrt(float(bad2))), "the p a Bin(2,p) would need to match P(W=2)")
show("binadd_bad_fit_p1", 2 * math.sqrt(float(bad2)) * (1 - math.sqrt(float(bad2))),
     "that Bin(2,p) gives this P(W=1) -- disagrees with binadd_bad_p1")

# ===================================================================
# 4.8  Covariance and correlation  (L11 slides 7-8)
# ===================================================================
print("\n=== 4.8  covariance / correlation ===")
# (i) uncorrelated but dependent: X uniform on {-1,0,1}, Y = X^2
pXc = {-1: F(1, 3), 0: F(1, 3), 1: F(1, 3)}
EXc = sum(F(k) * v for k, v in pXc.items())
EYc = sum(F(k) ** 2 * v for k, v in pXc.items())
EXYc = sum(F(k) ** 3 * v for k, v in pXc.items())
show("cov_ex_EX", EXc)
show("cov_ex_EY", EYc)
show("cov_ex_EXY", EXYc)
show("cov_ex_cov", EXYc - EXc * EYc, "zero, yet Y is a function of X")
show("cov_ex_P_X0_Y0", fs(F(1, 3)))
show("cov_ex_P_X0_times_P_Y0", fs(F(1, 3) * F(1, 3)), "1/9 != 1/3 -> dependent")

# (ii) unit square joint from a linear model: Y = X + N, X~U(0,1), N~U(0,1) indep
show("cov_lin_covXY", float(1 / 12), "cov(X, X+N) = var(X) = 1/12")
show("cov_lin_varY", float(1 / 12 + 1 / 12))
show("cov_lin_rho", float((1 / 12) / math.sqrt((1 / 12) * (2 / 12))))
show("cov_lin_rho_exact", float(1 / math.sqrt(2)))
# Monte-Carlo check
Xr = rng.random(3_000_000)
Nr = rng.random(3_000_000)
Yr = Xr + Nr
show("cov_lin_cov_mc", float(np.cov(Xr, Yr)[0, 1]))
show("cov_lin_rho_mc", float(np.corrcoef(Xr, Yr)[0, 1]))

# (iii) var of a sum with three correlated terms, worked number
show("varsum_demo_varX", 1.0)
show("varsum_demo_varY", 4.0)
show("varsum_demo_cov", 1.0)
show("varsum_demo_total", 1.0 + 4.0 + 2 * 1.0, "var(X+Y) = 1+4+2*1")

# (iv) rho = 1 example: Y = 3X + 5
show("rho_lin_pos", 1.0)
show("rho_lin_neg", -1.0, "Y = -3X + 5")

# ===================================================================
# 4.9  WIDGET verification: grid convolution vs numpy.convolve + closed forms
# ===================================================================
print("\n=== 4.9  widget grid check ===")
h = 0.002
grid = np.arange(-1.0, 8.0 + h / 2, h)


def pdf_uniform(t):
    return np.where((t >= 0) & (t <= 1), 1.0, 0.0)


def pdf_exp(t):
    return np.where(t >= 0, np.exp(-t), 0.0)


def pdf_tri(t):
    return np.where((t >= 0) & (t <= 1), t, np.where((t > 1) & (t <= 2), 2 - t, 0.0))


PDFS = {"uniform": pdf_uniform, "exponential": pdf_exp, "triangle": pdf_tri}


def conv_grid(fa, fb, w):
    """trapezoid evaluation of int f_a(x) f_b(w-x) dx on `grid` — exactly what the widget does."""
    return float(np.trapezoid(fa(grid) * fb(w - grid), grid))


checks = {}
for na, fa in PDFS.items():
    for nb, fb in PDFS.items():
        vals_grid = np.array([conv_grid(fa, fb, w) for w in np.arange(0, 4.001, 0.05)])
        # numpy.convolve reference on the same grid
        ref_full = np.convolve(fa(grid), fb(grid)) * h
        wref = grid[0] + grid[0] + np.arange(len(ref_full)) * h
        vals_np = np.interp(np.arange(0, 4.001, 0.05), wref, ref_full)
        err = float(np.max(np.abs(vals_grid - vals_np)))
        checks[f"{na}+{nb}"] = err
        print(f"  max|grid - numpy.convolve|  {na:12s}+{nb:12s} = {err:.3e}")
R["widget_conv_maxerr"] = checks
show("widget_conv_worst", max(checks.values()))

# closed-form spot checks the widget must reproduce
show("wchk_uu_at_0.7", conv_grid(pdf_uniform, pdf_uniform, 0.7), "triangle -> 0.7")
show("wchk_uu_at_1.4", conv_grid(pdf_uniform, pdf_uniform, 1.4), "triangle -> 0.6")
show("wchk_ee_at_1.0", conv_grid(pdf_exp, pdf_exp, 1.0), "Erlang-2 -> 1*e^-1")
show("wchk_ee_closed", float(math.exp(-1)))
show("wchk_ue_at_0.5", conv_grid(pdf_uniform, pdf_exp, 0.5), "-> 1-e^{-0.5}")
show("wchk_ue_closed", float(1 - math.exp(-0.5)))
show("wchk_tt_at_2.0", conv_grid(pdf_tri, pdf_tri, 2.0), "Irwin-Hall n=4 at 2 -> 2/3")
show("wchk_tt_closed", float(2 / 3))

# ===================================================================
# 4.10  practice-question checks
# ===================================================================
print("\n=== 4.10  practice checks ===")
# P4.2  X~Exp(2), Y=5X  -> Exp(2/5)
show("p42_rate", 2 / 5)
show("p42_mean", 5 / 2)
# P4.3  X~U(0,1), Y=X^3 -> f_Y = (1/3) y^{-2/3}
show("p43_norm", float(integrate.quad(lambda t: t ** (-2 / 3) / 3, 0, 1)[0]))
show("p43_mean", float(integrate.quad(lambda t: t * t ** (-2 / 3) / 3, 0, 1)[0]), "= E[X^3] = 1/4")
# P4.4  X~Exp(1), Y=ln X -> Gumbel f_Y(y)=e^{y-e^{y}}
show("p44_norm", float(integrate.quad(lambda t: math.exp(t - math.exp(t)), -30, 20)[0]))
show("p44_mean", float(integrate.quad(lambda t: t * math.exp(t - math.exp(t)), -30, 20)[0]),
     "= -Euler gamma")
show("p44_euler", -0.5772156649015329)
# P4.5  Z=Y/X : P(1/2 <= Z <= 2)
show("p45", float(F_Z(2) - F_Z(0.5)))
# P4.6  T = max(X,Y), X,Y iid U(0,1)
show("p46_mean", float(integrate.quad(lambda t: t * 2 * t, 0, 1)[0]), "= 2/3")
# P4.7  Y=|X|, X~N(0,1):  f_Y = sqrt(2/pi) e^{-y^2/2}
show("p47_norm", float(integrate.quad(lambda t: math.sqrt(2 / math.pi) * math.exp(-t * t / 2),
                                      0, np.inf)[0]))
show("p47_mean", float(integrate.quad(lambda t: t * math.sqrt(2 / math.pi) * math.exp(-t * t / 2),
                                      0, np.inf)[0]), "= sqrt(2/pi)")
show("p47_sqrt2overpi", math.sqrt(2 / math.pi))
# P4.8  Y=X^2, X~N(0,1): chi-square(1)
show("p48_norm", float(integrate.quad(lambda t: math.exp(-t / 2) / math.sqrt(2 * math.pi * t),
                                      0, np.inf)[0]))
show("p48_mean", float(integrate.quad(lambda t: t * math.exp(-t / 2) / math.sqrt(2 * math.pi * t),
                                      0, np.inf)[0]), "= 1")
# P4.9  two fair dice
dice = np.convolve([1 / 6] * 6, [1 / 6] * 6)
show("p49_p7", float(dice[5]), "w=7 is index 7-2=5 of support 2..12 -> 6/36")
show("p49_p7_frac", fs(F(6, 36)))
# P4.10  X,Y iid uniform on {1..4}
u4 = np.convolve([0.25] * 4, [0.25] * 4)
show("p410_p5", float(u4[3]), "w=5 is index 5-2=3 of support 2..8 -> 4/16")
show("p410_p4", float(u4[2]), "w=4 -> 3/16")
show("p410_p5_frac", fs(F(4, 16)))
# P4.11  X,Y iid Exp(lam): Erlang-2
show("p411_norm", float(integrate.quad(lambda t: 3 ** 2 * t * math.exp(-3 * t), 0, np.inf)[0]),
     "lam=3")
show("p411_mean", float(integrate.quad(lambda t: t * 9 * t * math.exp(-3 * t), 0, np.inf)[0]),
     "= 2/lam = 2/3")
# P4.12  U(0,1) + Exp(1)
show("p412_norm", float(integrate.quad(lambda t: 1 - math.exp(-t), 0, 1)[0]
                        + integrate.quad(lambda t: math.exp(-t) * (math.e - 1), 1, np.inf)[0]))
# P4.13  X - Y for iid U(0,1): triangle on [-1,1]
show("p413_norm", float(integrate.quad(lambda t: 1 - abs(t), -1, 1)[0]))
show("p413_var", float(integrate.quad(lambda t: t * t * (1 - abs(t)), -1, 1)[0]), "= 1/6")
# P4.14  X~N(1,4), Y~N(-2,9)
show("p414_mean", 1 + (-2))
show("p414_var", 4 + 9)
show("p414b_mean", 2 * 1 - (-2))
show("p414b_var", 4 * 4 + 9)
# P4.17 rho = -1
show("p417_var", 1.0 + 1.0 - 2 * 1.0, "sigma=1 each, rho=-1")
# P4.18 uniform on the unit disk
show("p418_cov", 0.0)
show("p418_condrange", float(2 * math.sqrt(1 - 0.9 ** 2)),
     "|Y| <= sqrt(1-x^2): at x=0.9 the conditional range has width 0.87")

out = Path(__file__).resolve().parent / "g3_s4.json"
out.write_text(json.dumps(R, indent=1), encoding="utf-8")
print(f"\nwrote {out}  ({len(R)} keys)")
