# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Question bank section 3 (Continuous random variables, Q48-Q72) — every number.

Run:  uv run computes/qb_s3.py
Writes computes/qb_s3.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, stats

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict = {}
rng = np.random.default_rng(20260814)
N = 4_000_000


def show(key, val, note=""):
    if isinstance(val, float):
        R[key] = val
        txt = f"{val:.6f}"
    else:
        R[key] = val
        txt = str(val)
    print(f"  {key:38s} = {txt}   {note}")


def head(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


Phi = stats.norm.cdf

# ---------------------------------------------------------------- Q48 tent PDF
head("Q48  tent density f(x)=x on [0,1], 2-x on [1,2]")
show("q48_c", 1.0, "normalizing constant")
show("q48_area_check", float(integrate.quad(lambda x: x, 0, 1)[0]
                            + integrate.quad(lambda x: 2 - x, 1, 2)[0]))
q48_p = integrate.quad(lambda x: 2 - x, 1.5, 2)[0]
show("q48_P_ge_1p5", float(q48_p))
q48_EX = integrate.quad(lambda x: x * x, 0, 1)[0] + integrate.quad(lambda x: x * (2 - x), 1, 2)[0]
q48_EX2 = integrate.quad(lambda x: x**2 * x, 0, 1)[0] + integrate.quad(lambda x: x**2 * (2 - x), 1, 2)[0]
show("q48_EX", float(q48_EX))
show("q48_EX2", float(q48_EX2))
show("q48_var", float(q48_EX2 - q48_EX**2), "= 1/6")
# MC: tent = sum of two U(0,1)
s = rng.random(N) + rng.random(N)
show("q48_mc_P_ge_1p5", float((s >= 1.5).mean()))
show("q48_mc_var", float(s.var()))
# trap: "x=1.5 is the midpoint of [1,2], which carries mass 1/2, so the tail is 1/4"
show("q48_wrong_half_of_right_mass", 0.25, "trap; true tail is 0.125")
show("q48_right_piece_mass", float(integrate.quad(lambda x: 2 - x, 1, 2)[0]), "= 1/2")

# ---------------------------------------------------------------- Q49 CDF->PDF
head("Q49  F(x)=x^2/4 on [0,2]")
show("q49_P_1_to_1p5", float(1.5**2 / 4 - 1**2 / 4))
show("q49_median", float(math.sqrt(2)))
q49_EX = integrate.quad(lambda x: x * (x / 2), 0, 2)[0]
q49_EX2 = integrate.quad(lambda x: x**2 * (x / 2), 0, 2)[0]
show("q49_EX", float(q49_EX), "= 4/3")
show("q49_EX2", float(q49_EX2), "= 2")
show("q49_var", float(q49_EX2 - q49_EX**2), "= 2/9")
show("q49_f_at_1p5", float(1.5 / 2))
# traps: reporting the mean as the median; using F itself as the density
show("q49_median_minus_mean", float(math.sqrt(2) - q49_EX))
show("q49_wrong_F_as_f_mass", float(integrate.quad(lambda x: x**2 / 4, 0, 2)[0]), "= 2/3, not 1")

# ---------------------------------------------------------- Q50 memorylessness
head("Q50  Exp mean 30 months; survived 18, wants 12 more")
lam50 = 1 / 30
show("q50_lambda", float(lam50))
show("q50_answer", float(math.exp(-lam50 * 12)), "e^{-0.4}")
show("q50_exponent", float(-lam50 * 12))
show("q50_P_T_gt_30", float(math.exp(-lam50 * 30)))
show("q50_P_T_gt_18", float(math.exp(-lam50 * 18)))
show("q50_ratio_check", float(math.exp(-lam50 * 30) / math.exp(-lam50 * 18)))
x50 = rng.exponential(30, N)
sel = x50 > 18
show("q50_mc", float((x50[sel] > 30).mean()))

# ------------------------------------------------------------ Q51 normal table
head("Q51  X ~ N(70, 25);  P(63 <= X <= 78)")
show("q51_z_lo", float((63 - 70) / 5))
show("q51_z_hi", float((78 - 70) / 5))
show("q51_Phi_1p6", float(Phi(1.6)))
show("q51_Phi_1p4", float(Phi(1.4)))
show("q51_Phi_minus1p4", float(Phi(-1.4)))
show("q51_answer_exact", float(Phi(1.6) - Phi(-1.4)))
show("q51_answer_table", float(0.9452 - (1 - 0.9192)))

# --------------------------------------------------------- Q52 joint normalize
head("Q52  f(x,y) = c(x + 2y) on the unit square")
inner = integrate.dblquad(lambda y, x: x + 2 * y, 0, 1, 0, 1)[0]
show("q52_integral_of_x_plus_2y", float(inner), "= 3/2")
show("q52_c", float(1 / inner), "= 2/3")
c52 = 2 / 3
show("q52_fX_at_0", float(c52 * (0 + 1)))
show("q52_fX_at_1", float(c52 * (1 + 1)))
q52_EX = integrate.quad(lambda x: x * c52 * (x + 1), 0, 1)[0]
show("q52_EX", float(q52_EX), "= 5/9")
q52_fY = lambda y: c52 * (0.5 + 2 * y)
show("q52_EY", float(integrate.quad(lambda y: y * q52_fY(y), 0, 1)[0]), "= 11/18")
# trap: "the square is symmetric in x and y, so E[X] = 0.5 (or E[X] = E[Y])"
show("q52_wrong_symmetry_EX", 0.5, "trap; true 5/9")
show("q52_EY_minus_EX", float(integrate.quad(lambda y: y * q52_fY(y), 0, 1)[0] - q52_EX), "11/18 - 5/9 = 1/18")

# ------------------------------------------------------------- Q53 covariance
head("Q53  var X = 4, var Y = 9, cov = -3")
show("q53_rho", float(-3 / (2 * 3)))
show("q53_var_sum", float(4 + 9 + 2 * (-3)))
show("q53_var_2XminusY", float(4 * 4 + 9 - 2 * 2 * (-3)))
show("q53_var_sum_if_indep", float(4 + 9))

# ------------------------------------------------------- Q54 derived Y = 1/X
head("Q54  X ~ U(1,3): uniform basics, then Y = 1/X")
# (a) the continuous uniform in its own right (G3 s1.3)
A54, B54 = 1.0, 3.0
show("q54_fX", float(1 / (B54 - A54)), "1/(b-a)")
show("q54_FX_at_2p5", float((2.5 - A54) / (B54 - A54)), "(x-a)/(b-a)")
show("q54_EX", float((A54 + B54) / 2), "(a+b)/2")
show("q54_varX", float((B54 - A54) ** 2 / 12), "(b-a)^2/12")
show("q54_sdX", float(math.sqrt((B54 - A54) ** 2 / 12)))
show("q54_P_1p5_to_2p5", float((2.5 - 1.5) / (B54 - A54)), "= 1/2")
show("q54_EX2", float(integrate.quad(lambda x: x**2 / (B54 - A54), A54, B54)[0]), "= 13/3")
# (b) the derived distribution of Y = 1/X on [1/3, 1]
show("q54_y_lo", float(1 / B54), "= 1/3")
show("q54_y_hi", float(1 / A54))
show("q54_fY_at_lo", float(1 / (B54 - A54) / (1 / B54) ** 2), "= 4.5")
show("q54_fY_at_hi", float(1 / (B54 - A54) / (1 / A54) ** 2), "= 0.5")
show("q54_norm_check", float(integrate.quad(lambda y: 1 / (2 * y**2), 1 / B54, 1 / A54)[0]))
show("q54_EY", float(math.log(B54 / A54) / (B54 - A54)), "ln 3 / 2")
show("q54_EY_check", float(integrate.quad(lambda y: y / (2 * y**2), 1 / B54, 1 / A54)[0]))
show("q54_wrong_reciprocal_of_mean", float(1 / ((A54 + B54) / 2)), "Jensen trap")
x54 = rng.uniform(A54, B54, N)
show("q54_mc_EY", float((1 / x54).mean()))
show("q54_mc_P_Y_le_0p75", float((1 / x54 <= 0.75).mean()))
show("q54_P_Y_le_0p75", float(integrate.quad(lambda y: 1 / (2 * y**2), 1 / B54, 0.75)[0]))

# -------------------------------------------------- Q55 conditional from Q52
head("Q55  f_{Y|X}(y|0.5) and E[Y|X=0.5] for f = (2/3)(x+2y)")
show("q55_fX_at_0p5", float(c52 * 1.5), "= 1")
cond = lambda y: (0.5 + 2 * y) / 1.5
show("q55_cond_check", float(integrate.quad(cond, 0, 1)[0]))
show("q55_cond_at_0", float(cond(0)))
show("q55_cond_at_1", float(cond(1)))
q55_E = integrate.quad(lambda y: y * cond(y), 0, 1)[0]
show("q55_EY_given_X_0p5", float(q55_E), "= 11/18")
show("q55_general_formula_at_0p5", float((0.5 / 2 + 2 / 3) / (0.5 + 1)))
show("q55_general_formula_at_0", float((0 / 2 + 2 / 3) / (0 + 1)))
show("q55_general_formula_at_1", float((1 / 2 + 2 / 3) / (1 + 1)))
show("q55_fX_at_0", float(c52 * (0 + 1)), "= 2/3, NOT 1")
show("q55_cond_at_x0_slope", float(c52 * 2 / (c52 * 1)), "f_{Y|X}(y|0) = 2y")
# where does E[Y|X=x] cross the unconditional 11/18?  (x/2+2/3)/(x+1) = 11/18
_x_cross = optimize.brentq(lambda x: (x / 2 + 2 / 3) / (x + 1) - 11 / 18, 0.0, 1.0)
show("q55_crossing_x", float(_x_cross), "exactly 1/2")

# ------------------------------------------------------------- Q56 heavy tail
head("Q56  f(x) = c x^{-3}, x >= 1")
show("q56_c", 2.0)
show("q56_norm_check", float(integrate.quad(lambda x: 2 * x**-3, 1, np.inf)[0]))
show("q56_P_gt_2", float(integrate.quad(lambda x: 2 * x**-3, 2, np.inf)[0]), "= 1/4")
show("q56_EX", float(integrate.quad(lambda x: x * 2 * x**-3, 1, np.inf)[0]), "= 2")
show("q56_median", float(math.sqrt(2)), "F(m)=1-m^-2=1/2")
show("q56_EX2_partial_10", float(integrate.quad(lambda x: x**2 * 2 * x**-3, 1, 10)[0]), "2 ln 10")
show("q56_EX2_partial_1000", float(integrate.quad(lambda x: x**2 * 2 * x**-3, 1, 1000)[0]))
show("q56_wrong_var", float(4 - 4), "the tempting 'E[X^2]-E[X]^2' if you mis-integrate")

# ----------------------------------------------------------- Q57 mixed r.v.
head("Q57  wait W: mass 0.3 at 0, density 0.35 on (0,2]")
show("q57_atom", 0.3)
show("q57_density", 0.35)
show("q57_F_at_1", float(0.3 + 0.35 * 1))
show("q57_P_0_to_1", float(0.35 * 1))
show("q57_P_gt_1p5", float(0.35 * 0.5))
q57_EX = 0.3 * 0 + integrate.quad(lambda x: x * 0.35, 0, 2)[0]
q57_EX2 = 0.3 * 0 + integrate.quad(lambda x: x**2 * 0.35, 0, 2)[0]
show("q57_EW", float(q57_EX), "= 0.7")
show("q57_EW2", float(q57_EX2), "= 14/15")
show("q57_var", float(q57_EX2 - q57_EX**2))
show("q57_median", float((0.5 - 0.3) / 0.35), "= 4/7")
u = rng.random(N)
w = np.where(u < 0.3, 0.0, rng.uniform(0, 2, N))
show("q57_mc_EW", float(w.mean()))
show("q57_mc_var", float(w.var()))
show("q57_wrong_EW_uniform_only", 1.0, "0.7*1 + ... careless 'E[W]=1'")

# --------------------------------------------------- Q58 competing exponentials
head("Q58  X ~ Exp(1/4), Y ~ Exp(1/6), independent")
l1, l2 = 0.25, 1 / 6
show("q58_lambda1", float(l1))
show("q58_lambda2", float(l2))
show("q58_lambda_sum", float(l1 + l2))
show("q58_P_X_lt_Y", float(l1 / (l1 + l2)), "= 0.6")
show("q58_E_min", float(1 / (l1 + l2)), "= 2.4 h")
show("q58_EX", float(1 / l1))
show("q58_EY", float(1 / l2))
show("q58_E_max", float(1 / l1 + 1 / l2 - 1 / (l1 + l2)))
show("q58_P_min_gt_3", float(math.exp(-(l1 + l2) * 3)))
xa = rng.exponential(1 / l1, N)
ya = rng.exponential(1 / l2, N)
show("q58_mc_P_X_lt_Y", float((xa < ya).mean()))
show("q58_mc_E_min", float(np.minimum(xa, ya).mean()))
show("q58_mc_E_max", float(np.maximum(xa, ya).mean()))
show("q58_wrong_E_max_sum", float(1 / l1 + 1 / l2), "tempting wrong 'E[max]=EX+EY'")

# ------------------------------------------------------------- Q59 normal design
head("Q59  N(mu, 1.2^2), want P(X < 500) <= 0.01")
z59 = stats.norm.ppf(0.99)
show("q59_z_exact", float(z59))
show("q59_z_table", 2.33)
show("q59_mu_exact", float(500 + z59 * 1.2))
show("q59_mu_table", float(500 + 2.33 * 1.2))
show("q59_check_tail", float(Phi((500 - (500 + 2.33 * 1.2)) / 1.2)))
show("q59_wrong_z_1p96", float(500 + 1.96 * 1.2), "two-sided 95% mix-up")

# ------------------------------------------------ Q60 continuous Bayes (G3 s3)
# Prior f_T(t) = 2t on [0,1]; X | T=t ~ Bin(3, t); observe X = 1.
head("Q60  continuous prior, discrete observation (Bayes)")
prior60 = lambda t: 2 * t
lik60 = lambda t: 3 * t * (1 - t) ** 2                      # P(X=1 | T=t)
show("q60_prior_mean", float(integrate.quad(lambda t: t * prior60(t), 0, 1)[0]), "= 2/3")
show("q60_prior_P_gt_half", float(integrate.quad(prior60, 0.5, 1)[0]), "= 3/4")
den60 = integrate.quad(lambda t: prior60(t) * lik60(t), 0, 1)[0]
show("q60_P_X_eq_1", float(den60), "= 1/5, the Bayes denominator")
show("q60_beta_integral", float(integrate.quad(lambda t: t**2 * (1 - t) ** 2, 0, 1)[0]), "= 1/30")
post60 = lambda t: prior60(t) * lik60(t) / den60
show("q60_post_const", float(post60(0.5) / (0.5**2 * 0.5**2)), "= 30, i.e. Beta(3,3)")
show("q60_post_norm_check", float(integrate.quad(post60, 0, 1)[0]))
show("q60_post_at_0p25", float(post60(0.25)))
show("q60_post_at_0p5", float(post60(0.5)), "the mode")
show("q60_post_mean", float(integrate.quad(lambda t: t * post60(t), 0, 1)[0]), "= 1/2")
show("q60_post_var", float(integrate.quad(lambda t: t**2 * post60(t), 0, 1)[0] - 0.5**2), "= 1/28")
show("q60_post_P_gt_half", float(integrate.quad(post60, 0.5, 1)[0]), "= 1/2 by symmetry")
show("q60_ml_estimate", 1.0 / 3.0, "the wrong answer: ignores the prior")
# Monte Carlo: draw from the prior, keep the draws that produced X = 1.
t60 = np.sqrt(rng.random(N))                                # prior f(t) = 2t
x60 = rng.binomial(3, t60)
keep = t60[x60 == 1]
show("q60_mc_P_X_eq_1", float((x60 == 1).mean()))
show("q60_mc_post_mean", float(keep.mean()))
show("q60_mc_post_P_gt_half", float((keep > 0.5).mean()))

# ---------------------------------------------------- Q61 exponential wedge
head("Q61  f(x,y) = c e^{-y} on 0 <= x <= y")
i61 = integrate.quad(lambda y: y * math.exp(-y), 0, np.inf)[0]
show("q61_inner_integral", float(i61), "= 1 so c = 1")
show("q61_c", 1.0)
show("q61_fY_at_1", float(1 * math.exp(-1)))
show("q61_fY_at_2", float(2 * math.exp(-2)))
show("q61_fX_at_1", float(math.exp(-1)))
show("q61_EY", float(integrate.quad(lambda y: y * y * math.exp(-y), 0, np.inf)[0]), "= 2")
show("q61_EX", float(integrate.quad(lambda x: x * math.exp(-x), 0, np.inf)[0]), "= 1")
show("q61_P_Y_le_1", float(integrate.quad(lambda y: y * math.exp(-y), 0, 1)[0]), "= 1-2/e")
show("q61_P_X_le_1_given_Y_3", float(1 / 3))
Yw = rng.gamma(2, 1, N)
Xw = rng.random(N) * Yw
show("q61_mc_EX", float(Xw.mean()))
show("q61_mc_EY", float(Yw.mean()))
show("q61_mc_P_X_le_1", float((Xw <= 1).mean()))
show("q61_P_X_le_1", float(1 - math.exp(-1)))

# ----------------------------------------------------------- Q62 Cauchy
head("Q62  X ~ U(0,1), Y = tan(pi(X - 1/2))")
show("q62_fY_at_0", float(1 / math.pi))
show("q62_fY_at_1", float(1 / (math.pi * 2)))
show("q62_norm_check", float(integrate.quad(lambda y: 1 / (math.pi * (1 + y**2)), -np.inf, np.inf)[0]))
show("q62_P_abs_le_1", float(integrate.quad(lambda y: 1 / (math.pi * (1 + y**2)), -1, 1)[0]), "= 1/2")
show("q62_P_abs_le_10", float(integrate.quad(lambda y: 1 / (math.pi * (1 + y**2)), -10, 10)[0]))
show("q62_E_abs_partial_1000", float(integrate.quad(lambda y: abs(y) / (math.pi * (1 + y**2)), -1000, 1000)[0]),
     "diverges like (2/pi) ln M")
xc = rng.random(N)
yc = np.tan(math.pi * (xc - 0.5))
show("q62_mc_P_abs_le_1", float((np.abs(yc) <= 1).mean()))
show("q62_mc_median", float(np.median(yc)))

# ------------------------------------------------- Q63 convolution U(0,1)+Exp(1)
head("Q63  Z = X + Y, X ~ U(0,1), Y ~ Exp(1)")
fZ = lambda z: (1 - math.exp(-z)) if z <= 1 else (math.e - 1) * math.exp(-z)
show("q63_fZ_at_0p5", float(fZ(0.5)))
show("q63_fZ_at_1", float(fZ(1.0)), "1 - 1/e, continuous at z=1")
show("q63_fZ_at_1_other_branch", float((math.e - 1) * math.exp(-1)))
show("q63_fZ_at_2", float(fZ(2.0)))
show("q63_mass_0_1", float(integrate.quad(lambda z: 1 - math.exp(-z), 0, 1)[0]), "= 1/e")
show("q63_mass_1_inf", float(integrate.quad(lambda z: (math.e - 1) * math.exp(-z), 1, np.inf)[0]))
show("q63_EZ", 1.5)
show("q63_varZ", float(1 / 12 + 1), "= 13/12")
zc = rng.random(N) + rng.exponential(1, N)
show("q63_mc_EZ", float(zc.mean()))
show("q63_mc_P_le_1", float((zc <= 1).mean()))
show("q63_mc_varZ", float(zc.var()))

# ------------------------------------------- Q64 uncorrelated but dependent
head("Q64  Theta ~ U(0,2pi), X = cos Theta, Y = sin Theta")
show("q64_EX", float(integrate.quad(lambda t: math.cos(t) / (2 * math.pi), 0, 2 * math.pi)[0]))
show("q64_EY", float(integrate.quad(lambda t: math.sin(t) / (2 * math.pi), 0, 2 * math.pi)[0]))
show("q64_EXY", float(integrate.quad(lambda t: math.sin(t) * math.cos(t) / (2 * math.pi), 0, 2 * math.pi)[0]))
show("q64_cov", 0.0)
show("q64_varX", float(integrate.quad(lambda t: math.cos(t) ** 2 / (2 * math.pi), 0, 2 * math.pi)[0]), "= 1/2")
show("q64_rho", 0.0)
show("q64_P_absY_le_0p1", float(2 * math.asin(0.1) / math.pi), "unconditional")
th = rng.uniform(0, 2 * math.pi, N)
Xc, Yc = np.cos(th), np.sin(th)
show("q64_mc_cov", float(np.cov(Xc, Yc)[0, 1]))
sel64 = np.abs(Xc - 0.9) < 0.01
show("q64_mc_P_absY_le_0p1_given_X_near_0p9", float((np.abs(Yc[sel64]) <= 0.1).mean()))
show("q64_P_absY_le_0p1_given_X_0p9", 0.0, "|Y| = sqrt(1-0.81) = 0.4359 exactly")
show("q64_Y_given_X_0p9", float(math.sqrt(1 - 0.81)))

# ------------------------------------------------------- Q65 sum of normals
head("Q65  X ~ N(10, 0.04), Y ~ N(15, 0.09), T = X + Y")
var65 = 0.04 + 0.09
sd65 = math.sqrt(var65)
show("q65_varT", float(var65))
show("q65_sdT", float(sd65))
show("q65_z", float(0.5 / sd65))
show("q65_answer", float(1 - Phi(0.5 / sd65)))
show("q65_Phi_z", float(Phi(0.5 / sd65)))
show("q65_wrong_sd_sum", float(0.2 + 0.3))
show("q65_wrong_answer", float(1 - Phi(0.5 / 0.5)))
t65 = rng.normal(10, 0.2, N) + rng.normal(15, 0.3, N)
show("q65_mc", float((t65 > 25.5).mean()))

# --------------------------------------------- Q66 factorization on a triangle
head("Q66  f(x,y) = 8xy on {0 <= y <= x <= 1}: factors, but NOT independent")
show("q66_norm", float(integrate.dblquad(lambda y, x: 8 * x * y, 0, 1, 0, lambda x: x)[0]))
show("q66_fX_at_0p5", float(4 * 0.5**3), "f_X(x) = 4x^3")
show("q66_fY_at_0p75", float(4 * 0.75 * (1 - 0.75**2)), "f_Y(y) = 4y(1-y^2)")
show("q66_product_at_0p5_0p75", float(4 * 0.5**3 * 4 * 0.75 * (1 - 0.75**2)))
show("q66_joint_at_0p5_0p75", 0.0, "point lies outside the triangle")
show("q66_fY_norm_check", float(integrate.quad(lambda y: 4 * y * (1 - y**2), 0, 1)[0]))

# --------------------------------------------- Q67 conditional-mean of Exp
head("Q67  T ~ Exp(1/5); E[T | T > 3]")
lam67 = 0.2
show("q67_mean", float(1 / lam67))
show("q67_answer", float(3 + 1 / lam67))
num = integrate.quad(lambda t: t * lam67 * math.exp(-lam67 * t), 3, np.inf)[0]
den = math.exp(-lam67 * 3)
show("q67_direct_integral", float(num / den))
show("q67_wrong", float(1 / lam67), "the memorylessness over-reach")
t67 = rng.exponential(5, N)
show("q67_mc", float(t67[t67 > 3].mean()))

# ------------------------------------------------- Q68 two-branch CDF method
head("Q68  X ~ U(-1,2), Y = X^2")
show("q68_fX", float(1 / 3))
show("q68_FY_at_0p25", float(2 * math.sqrt(0.25) / 3), "0<y<1 branch")
show("q68_FY_at_2", float((math.sqrt(2) + 1) / 3), "1<y<4 branch")
show("q68_fY_at_0p25", float(1 / (3 * math.sqrt(0.25))))
show("q68_fY_at_0p9", float(1 / (3 * math.sqrt(0.9))))
show("q68_fY_at_1p1", float(1 / (6 * math.sqrt(1.1))))
show("q68_mass_0_1", float(integrate.quad(lambda y: 1 / (3 * math.sqrt(y)), 0, 1)[0]), "= 2/3")
show("q68_mass_1_4", float(integrate.quad(lambda y: 1 / (6 * math.sqrt(y)), 1, 4)[0]), "= 1/3")
show("q68_EY", float(integrate.quad(lambda y: y / (3 * math.sqrt(y)), 0, 1)[0]
                     + integrate.quad(lambda y: y / (6 * math.sqrt(y)), 1, 4)[0]))
show("q68_EY_via_var", float(9 / 12 + 0.5**2), "var(X)+E[X]^2")
show("q68_wrong_one_branch", float(1 / (6 * math.sqrt(0.25))), "using 1/(6 sqrt y) everywhere")
x68 = rng.uniform(-1, 2, N)
y68 = x68**2
show("q68_mc_P_Y_le_1", float((y68 <= 1).mean()))
show("q68_mc_EY", float(y68.mean()))

# ------------------------------------ Q69 uniform between y = x^2 and y = x
head("Q69  (X,Y) uniform on {0 <= x <= 1, x^2 <= y <= x}")
area69 = integrate.quad(lambda x: x - x**2, 0, 1)[0]
show("q69_area", float(area69), "= 1/6")
show("q69_density", float(1 / area69), "= 6")
show("q69_fX_at_0p5", float(6 * (0.5 - 0.25)))
show("q69_fY_at_0p25", float(6 * (math.sqrt(0.25) - 0.25)))
show("q69_EX", float(integrate.quad(lambda x: x * 6 * (x - x**2), 0, 1)[0]), "= 1/2")
show("q69_EY", float(integrate.quad(lambda y: y * 6 * (math.sqrt(y) - y), 0, 1)[0]), "= 2/5")
show("q69_EXgivenY_0p25", float((math.sqrt(0.25) + 0.25) / 2))
show("q69_EXgivenY_0p81", float((math.sqrt(0.81) + 0.81) / 2))
show("q69_tower_check", float(integrate.quad(
    lambda y: (math.sqrt(y) + y) / 2 * 6 * (math.sqrt(y) - y), 0, 1)[0]), "must equal E[X]")
show("q69_EX2", float(integrate.quad(lambda x: x**2 * 6 * (x - x**2), 0, 1)[0]), "= 3/10")
show("q69_varX", float(0.3 - 0.25))
exy = integrate.dblquad(lambda y, x: 6 * x * y, 0, 1, lambda x: x**2, lambda x: x)[0]
show("q69_EXY", float(exy), "= 1/4")
show("q69_cov", float(exy - 0.5 * 0.4))
# MC by rejection
xr = rng.random(3_000_000)
yr = rng.random(3_000_000)
keep = (yr <= xr) & (yr >= xr**2)
show("q69_mc_EX", float(xr[keep].mean()))
show("q69_mc_EY", float(yr[keep].mean()))
show("q69_mc_accept_rate", float(keep.mean()))

# --------------------------------------------------- Q70 sum and difference
head("Q70  X, Y iid U(0,1); U = X+Y, V = X-Y")
show("q70_varX", float(1 / 12))
show("q70_cov_UV", float(1 / 12 - 1 / 12), "var X - var Y")
show("q70_varU", float(2 / 12), "= 1/6")
show("q70_varV", float(2 / 12))
show("q70_rho", 0.0)
show("q70_P_absV_gt_0p5", 0.25, "two corner triangles, each area 1/8")
show("q70_P_U_lt_0p5", 0.125)
show("q70_P_both", 0.0, "|V| <= U always")
show("q70_P_absV_gt_0p5_given_U_lt_0p5", 0.0)
X70 = rng.random(N)
Y70 = rng.random(N)
U70, V70 = X70 + Y70, X70 - Y70
show("q70_mc_cov", float(np.cov(U70, V70)[0, 1]))
show("q70_mc_P_absV_gt_0p5", float((np.abs(V70) > 0.5).mean()))
show("q70_mc_P_both", float(((np.abs(V70) > 0.5) & (U70 < 0.5)).mean()))

# ------------------------------------------- Q71 convolution of two exponentials
head("Q71  X ~ Exp(1), Y ~ Exp(2) independent, Z = X + Y")
fz71 = lambda z: 2 * (math.exp(-z) - math.exp(-2 * z))
show("q71_norm", float(integrate.quad(fz71, 0, np.inf)[0]))
show("q71_fZ_at_0p5", float(fz71(0.5)))
show("q71_fZ_at_1", float(fz71(1.0)))
show("q71_mode", float(math.log(2)))
show("q71_fZ_at_mode", float(fz71(math.log(2))), "= 1/2")
show("q71_EZ", float(integrate.quad(lambda z: z * fz71(z), 0, np.inf)[0]), "= 1 + 1/2")
show("q71_varZ", float(1 + 0.25), "1/1^2 + 1/2^2")
show("q71_P_gt_1", float(integrate.quad(fz71, 1, np.inf)[0]))
show("q71_P_gt_1_closed", float(2 * math.exp(-1) - math.exp(-2)))
z71 = rng.exponential(1, N) + rng.exponential(0.5, N)
show("q71_mc_EZ", float(z71.mean()))
show("q71_mc_P_gt_1", float((z71 > 1).mean()))
show("q71_mc_varZ", float(z71.var()))
show("q71_wrong_erlang", float(1 * math.exp(-1)), "assuming equal rates -> z e^{-z} at z=1")

# --------------------------------------------------------- Q72 censored Exp
head("Q72  X ~ Exp(1), Y = min(X, 2)")
show("q72_atom", float(math.exp(-2)))
show("q72_F_at_1", float(1 - math.exp(-1)))
show("q72_int_y_exp", float(integrate.quad(lambda y: y * math.exp(-y), 0, 2)[0]), "= 1 - 3e^{-2}")
q72_EY = integrate.quad(lambda y: y * math.exp(-y), 0, 2)[0] + 2 * math.exp(-2)
show("q72_EY", float(q72_EY))
show("q72_EY_shortcut", float(1 - math.exp(-2)), "(1 - e^{-lambda c})/lambda")
q72_EY2 = integrate.quad(lambda y: y**2 * math.exp(-y), 0, 2)[0] + 4 * math.exp(-2)
show("q72_int_y2_exp", float(integrate.quad(lambda y: y**2 * math.exp(-y), 0, 2)[0]), "= 2 - 10e^{-2}")
show("q72_EY2", float(q72_EY2))
show("q72_EY_sq", float(q72_EY**2))
show("q72_varY", float(q72_EY2 - q72_EY**2))
show("q72_wrong_EY_pure_exp", 1.0, "forgetting the cap")
x72 = rng.exponential(1, N)
y72 = np.minimum(x72, 2.0)
show("q72_mc_EY", float(y72.mean()))
show("q72_mc_varY", float(y72.var()))
show("q72_mc_atom", float((x72 > 2).mean()))

# ------------------------------------------------- extra numbers quoted in prose
head("Extras quoted in the fragment text")
show("q51_wrong_sigma25_z_lo", float((63 - 70) / 25))
show("q51_wrong_sigma25_z_hi", float((78 - 70) / 25))
show("q51_wrong_sigma25_answer", float(Phi(0.32) - Phi(-0.28)))
show("q59_margin_sigma_0p6", float(2.33 * 0.6), "safety margin halves with sigma")
show("q63_e_minus_1", float(math.e - 1))
show("q65_answer_table", float(1 - 0.9177))
show("q67_P_T_gt_3", float(math.exp(-0.6)))
show("q68_second_branch_mean_piece", float((1 / 6) * (2 / 3) * (4**1.5 - 1)), "= 7/9")
show("q71_two_over_e", float(2 * math.exp(-1)))
show("q71_e_minus_2", float(math.exp(-2)))
show("q72_three_e_minus_2", float(3 * math.exp(-2)))
show("q72_ten_e_minus_2", float(10 * math.exp(-2)))
show("q72_wrong_renormalized", float((1 - 3 * math.exp(-2)) / (1 - math.exp(-2))),
     "dropping the atom instead of placing it at 2")
show("q72_atom_pct", float(100 * math.exp(-2)))

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(R, indent=1, sort_keys=True), encoding="utf-8")
print(f"\nWrote {out}  ({len(R)} keys)")
