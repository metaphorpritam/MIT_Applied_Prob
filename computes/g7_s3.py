# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy"]
# ///
"""G7 §3 — Linear regression (L24 slides 3-6, B&T §9.2).

Every number that appears in fragments/g7_s3.html is produced here.
Nothing in the fragment is hand-computed.
"""
import io
import json
import sys
from fractions import Fraction as F

import numpy as np
from scipy import stats

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

R = {}


def put(k, v, label=None):
    R[k] = v
    print(f"{k:38s} = {v!r}" + (f"   [{label}]" if label else ""))


def head(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# ==========================================================================
# 1. THE WORKED DATASET  (invented: weekly problem-set hours vs final score)
#    Constructed so that the least-squares answers are exact integers:
#    y_i = 55 + 5 x_i + r_i with sum r_i = 0 and sum (x_i - xbar) r_i = 0.
# ==========================================================================
head("1. Worked dataset — exact rational least squares")

xs = [1, 2, 3, 4, 5, 6, 7, 8]
ys = [63, 61, 72, 74, 79, 87, 86, 98]
n = len(xs)
put("data_x", xs)
put("data_y", ys)
put("n", n)

Fx = [F(v) for v in xs]
Fy = [F(v) for v in ys]
xbar = sum(Fx) / n
ybar = sum(Fy) / n
put("sum_x", int(sum(xs)))
put("sum_y", int(sum(ys)))
put("xbar", str(xbar), "= 4.5")
put("ybar", str(ybar), "= 77.5")
put("xbar_f", float(xbar))
put("ybar_f", float(ybar))

dx = [v - xbar for v in Fx]
dy = [v - ybar for v in Fy]
prod = [a * b for a, b in zip(dx, dy)]
sq = [a * a for a in dx]
Sxy = sum(prod)
Sxx = sum(sq)
Syy = sum(b * b for b in dy)
put("dx", [str(v) for v in dx])
put("dy", [str(v) for v in dy])
put("prod_terms", [str(v) for v in prod])
put("sq_terms", [str(v) for v in sq])
put("Sxy", str(Sxy), "sum (x-xbar)(y-ybar)")
put("Sxx", str(Sxx), "sum (x-xbar)^2")
put("Syy", str(Syy), "sum (y-ybar)^2")
put("Sxy_f", float(Sxy))
put("Sxx_f", float(Sxx))
put("Syy_f", float(Syy))

th1 = Sxy / Sxx
th0 = ybar - th1 * xbar
put("th1", str(th1), "theta1-hat exact")
put("th0", str(th0), "theta0-hat exact")
put("th1_f", float(th1))
put("th0_f", float(th0))

# raw-sum (computational) form, as a cross-check
sum_xy = sum(a * b for a, b in zip(xs, ys))
sum_xx = sum(a * a for a in xs)
sum_yy = sum(b * b for b in ys)
put("sum_xy", sum_xy)
put("sum_xx", sum_xx)
put("sum_yy", sum_yy)
Sxy_raw = F(sum_xy) - n * xbar * ybar
Sxx_raw = F(sum_xx) - n * xbar * xbar
put("Sxy_raw_check", str(Sxy_raw))
put("Sxx_raw_check", str(Sxx_raw))
assert Sxy_raw == Sxy and Sxx_raw == Sxx

fit = [th0 + th1 * v for v in Fx]
res = [b - f for b, f in zip(Fy, fit)]
put("fitted", [str(v) for v in fit])
put("residuals", [str(v) for v in res])
put("residuals_f", [float(v) for v in res])
put("sum_residuals", str(sum(res)), "must be 0 (first normal equation)")
put("sum_x_residuals", str(sum(a * b for a, b in zip(Fx, res))), "must be 0 (second normal eq.)")
assert sum(res) == 0
assert sum(a * b for a, b in zip(Fx, res)) == 0

SSE = sum(r * r for r in res)
SSR = th1 * th1 * Sxx
put("SSE", str(SSE), "sum of squared residuals")
put("SSR", str(SSR), "explained sum of squares = th1^2 * Sxx")
put("SST_decomp_check", str(SSR + SSE), "must equal Syy")
assert SSR + SSE == Syy
R2 = float(SSR / Syy)
put("R2", round(R2, 6))
put("R2_exact", str(SSR / Syy))
put("r_corr", round(float(Sxy) / (float(Sxx) * float(Syy)) ** 0.5, 6), "sample correlation")

# numpy independent check
c = np.polyfit(np.array(xs, float), np.array(ys, float), 1)
put("numpy_polyfit_slope", round(float(c[0]), 12))
put("numpy_polyfit_intercept", round(float(c[1]), 12))
lin = stats.linregress(xs, ys)
put("scipy_slope", round(float(lin.slope), 12))
put("scipy_intercept", round(float(lin.intercept), 12))
put("scipy_rvalue2", round(float(lin.rvalue) ** 2, 12))

# standard error and confidence intervals for the coefficients (L24 slide 6)
sigma_hat2 = float(SSE) / (n - 2)
sigma_hat = sigma_hat2 ** 0.5
put("sigma_hat2", round(sigma_hat2, 6), "SSE/(n-2)")
put("sigma_hat", round(sigma_hat, 6), "standard error of the regression")
se_th1 = sigma_hat / float(Sxx) ** 0.5
se_th0 = sigma_hat * (1.0 / n + float(xbar) ** 2 / float(Sxx)) ** 0.5
put("se_th1", round(se_th1, 6))
put("se_th0", round(se_th0, 6))
tcrit = float(stats.t.ppf(0.975, n - 2))
put("t_crit_6df_975", round(tcrit, 6))
put("ci_th1", [round(float(th1) - tcrit * se_th1, 6), round(float(th1) + tcrit * se_th1, 6)])
put("ci_th0", [round(float(th0) - tcrit * se_th0, 6), round(float(th0) + tcrit * se_th0, 6)])
put("scipy_stderr_slope", round(float(lin.stderr), 6))
put("scipy_stderr_intercept", round(float(lin.intercept_stderr), 6))
# prediction at x = 10 (extrapolation gotcha)
put("pred_x10", float(th0 + th1 * 10))
put("pred_x20", float(th0 + th1 * 20))
put("pred_x0", float(th0))

# ==========================================================================
# 2. B&T EXAMPLE 9.9 — leaning tower of Pisa
# ==========================================================================
head("2. B&T Example 9.9 — leaning tower of Pisa")
py = [1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987]
pl = [2.9642, 2.9644, 2.9656, 2.9667, 2.9673, 2.9688, 2.9696,
      2.9698, 2.9713, 2.9717, 2.9725, 2.9742, 2.9757]
pn = len(py)
put("pisa_n", pn)
pxb = float(np.mean(py))
pyb = float(np.mean(pl))
put("pisa_xbar", pxb, "B&T prints 1981")
put("pisa_ybar", round(pyb, 6), "B&T prints 2.9694")
pSxy = float(np.sum((np.array(py) - pxb) * (np.array(pl) - pyb)))
pSxx = float(np.sum((np.array(py) - pxb) ** 2))
put("pisa_Sxy", round(pSxy, 8))
put("pisa_Sxx", round(pSxx, 6))
pth1 = pSxy / pSxx
pth0 = pyb - pth1 * pxb
put("pisa_th1", round(pth1, 10))
put("pisa_th1_rounded4", round(pth1, 4), "B&T prints 0.0009")
put("pisa_th0", round(pth0, 6))
put("pisa_th0_rounded4", round(pth0, 4), "B&T prints 1.1233")
pres = np.array(pl) - (pth0 + pth1 * np.array(py))
put("pisa_SSE", float(f"{np.sum(pres ** 2):.3e}"))
put("pisa_R2", round(1 - np.sum(pres ** 2) / np.sum((np.array(pl) - pyb) ** 2), 6))
put("pisa_mm_per_year", round(pth1 * 1000, 4), "slope in millimetres per year")
put("pisa_resid_mm", [round(float(v) * 1000, 3) for v in pres], "residuals in millimetres")
put("pisa_resid_absmax_mm", round(float(np.max(np.abs(pres))) * 1000, 3))
_sg = np.sign(pres)
put("pisa_sign_runs", int(1 + np.sum(_sg[1:] != _sg[:-1])), "number of same-sign runs (13 points)")
put("pisa_neg_run_8285", [int(v) for v in np.arange(1975, 1988)[pres < 0]],
    "years with a negative residual")
put("pisa_pred_2010", round(pth0 + pth1 * 2010, 6), "extrapolation 23 yr past the data")

# ==========================================================================
# 3. WIDGET ANCHORS — sampling distribution of the estimators
#    Model Y_i = 55 + 5 x_i + W_i, W_i ~ N(0, sigma^2) i.i.d., x_i fixed.
#    Theory: E[th1hat] = 5, var(th1hat) = sigma^2 / Sxx,
#            var(th0hat) = sigma^2 (1/n + xbar^2/Sxx), E[SSE] = (n-2) sigma^2.
# ==========================================================================
head("3. Widget anchors — Monte Carlo check of the sampling distribution")


def grid(nn):
    return np.linspace(1.0, 8.0, nn)


def sxx_of(nn):
    g = grid(nn)
    return float(np.sum((g - g.mean()) ** 2))


for nn in (8, 30):
    put(f"WID_Sxx_n{nn}", round(sxx_of(nn), 6))
    put(f"WID_Sxx_n{nn}_formula", round((7.0 / (nn - 1)) ** 2 * nn * (nn * nn - 1) / 12, 6),
        "h^2 n(n^2-1)/12")

rng = np.random.default_rng(20101216)
MC = 400_000
for (nn, sg) in ((8, 5.0), (8, 12.0), (30, 5.0)):
    g = grid(nn)
    Sx = float(np.sum((g - g.mean()) ** 2))
    Y = 55.0 + 5.0 * g + sg * rng.standard_normal((MC, nn))
    yb = Y.mean(axis=1)
    b1 = ((g - g.mean()) * (Y - yb[:, None])).sum(axis=1) / Sx
    b0 = yb - b1 * g.mean()
    sse = ((Y - (b0[:, None] + b1[:, None] * g)) ** 2).sum(axis=1)
    tag = f"n{nn}_s{sg:g}"
    put(f"WID_{tag}_mean_th1_MC", round(float(b1.mean()), 5))
    put(f"WID_{tag}_mean_th0_MC", round(float(b0.mean()), 5))
    put(f"WID_{tag}_se_th1_theory", round(sg / Sx ** 0.5, 6))
    put(f"WID_{tag}_se_th1_MC", round(float(b1.std(ddof=1)), 6))
    put(f"WID_{tag}_se_th0_theory", round(sg * (1 / nn + g.mean() ** 2 / Sx) ** 0.5, 6))
    put(f"WID_{tag}_se_th0_MC", round(float(b0.std(ddof=1)), 6))
    put(f"WID_{tag}_ESSE_theory", round((nn - 2) * sg * sg, 4))
    put(f"WID_{tag}_ESSE_MC", round(float(sse.mean()), 4))
    put(f"WID_{tag}_ER2_MC", round(float((1 - sse / ((Y - yb[:, None]) ** 2).sum(axis=1)).mean()), 5))

# ==========================================================================
# 4. PRACTICE PROBLEM NUMBERS
# ==========================================================================
head("4. Practice problems")

# --- Practice 3.2: shifting / rescaling the data
ys_shift = [v + 10 for v in ys]
b1s = F(sum((F(a) - xbar) * (F(b) - (ybar + 10)) for a, b in zip(xs, ys_shift)), 1) / Sxx
put("P32_shift_th1", str(b1s))
put("P32_shift_th0", str((ybar + 10) - b1s * xbar))
xs_dbl = [2 * v for v in xs]
xb2 = 2 * xbar
Sxx2 = sum((F(a) - xb2) ** 2 for a in xs_dbl)
Sxy2 = sum((F(a) - xb2) * (F(b) - ybar) for a, b in zip(xs_dbl, ys))
put("P32_double_Sxx", str(Sxx2))
put("P32_double_Sxy", str(Sxy2))
put("P32_double_th1", str(Sxy2 / Sxx2))
put("P32_double_th0", str(ybar - (Sxy2 / Sxx2) * xb2))

# --- Practice 3.4: regression through the origin
th_orig = F(sum_xy, sum_xx)
put("P34_sum_xy", sum_xy)
put("P34_sum_xx", sum_xx)
put("P34_theta_origin", str(th_orig))
put("P34_theta_origin_f", round(float(th_orig), 6))
res_o = [F(b) - th_orig * F(a) for a, b in zip(xs, ys)]
put("P34_SSE_origin", str(sum(r * r for r in res_o)))
put("P34_SSE_origin_f", round(float(sum(r * r for r in res_o)), 4))
put("P34_SSE_ratio", round(float(sum(r * r for r in res_o)) / float(SSE), 4))

# --- Check (used in 3.2/3.3 prose): the line passes through (xbar, ybar)
put("fit_at_xbar_check", str(th0 + th1 * xbar), "must equal ybar = 155/2")
assert th0 + th1 * xbar == ybar

# --- Practice 3.8: the reverse regression (x on y)
th1_rev = Sxy / Syy
put("P38_th1_reverse", str(th1_rev))
put("P38_th1_reverse_f", round(float(th1_rev), 6))
put("P38_th0_reverse", str(xbar - th1_rev * ybar))
put("P38_th0_reverse_f", round(float(xbar - th1_rev * ybar), 6))
put("P38_product", str(th1 * th1_rev), "must equal R^2")
put("P38_product_f", round(float(th1 * th1_rev), 6))
assert th1 * th1_rev == SSR / Syy
# where the reverse line crosses y = ... expressed as y on x
put("P38_reverse_as_y_on_x_slope", round(1.0 / float(th1_rev), 6))

# --- Practice 3.13: an outlier / high-leverage point
xs2 = xs + [15]
ys2 = ys + [60]
n2 = len(xs2)
xb2b = F(sum(xs2), n2)
yb2b = F(sum(ys2), n2)
Sxx_b = sum((F(a) - xb2b) ** 2 for a in xs2)
Sxy_b = sum((F(a) - xb2b) * (F(b) - yb2b) for a, b in zip(xs2, ys2))
th1_b = Sxy_b / Sxx_b
th0_b = yb2b - th1_b * xb2b
put("P313_n", n2)
put("P313_xbar", str(xb2b))
put("P313_xbar_f", round(float(xb2b), 6))
put("P313_ybar", str(yb2b))
put("P313_ybar_f", round(float(yb2b), 6))
put("P313_Sxx", str(Sxx_b))
put("P313_Sxy", str(Sxy_b))
put("P313_th1", str(th1_b))
put("P313_th1_f", round(float(th1_b), 6))
put("P313_th0", str(th0_b))
put("P313_th0_f", round(float(th0_b), 6))
res_b = [F(b) - (th0_b + th1_b * F(a)) for a, b in zip(xs2, ys2)]
Syy_b = sum((F(b) - yb2b) ** 2 for b in ys2)
put("P313_SSE", round(float(sum(r * r for r in res_b)), 4))
put("P313_R2", round(float(1 - sum(r * r for r in res_b) / Syy_b), 6))
put("P313_resid_outlier", round(float(res_b[-1]), 4))

# --- Practice 3.12: log-linearised exponential fit
ex = [0, 1, 2, 3, 4, 5]
ey = [2.0, 3.4, 5.5, 9.1, 14.8, 24.6]
lz = [float(np.log(v)) for v in ey]
exb, lzb = float(np.mean(ex)), float(np.mean(lz))
b1e = float(np.sum((np.array(ex) - exb) * (np.array(lz) - lzb)) / np.sum((np.array(ex) - exb) ** 2))
b0e = lzb - b1e * exb
put("P312_x", ex)
put("P312_y", ey)
put("P312_lny", [round(v, 6) for v in lz])
put("P312_xbar", exb)
put("P312_lnybar", round(lzb, 6))
put("P312_Sxx", round(float(np.sum((np.array(ex) - exb) ** 2)), 6))
put("P312_Sxz", round(float(np.sum((np.array(ex) - exb) * (np.array(lz) - lzb))), 6))
put("P312_b1", round(b1e, 6), "estimate of b in y = a e^{bx}")
put("P312_b0", round(b0e, 6), "estimate of ln a")
put("P312_a", round(float(np.exp(b0e)), 6))
pred = [float(np.exp(b0e) * np.exp(b1e * v)) for v in ex]
put("P312_fitted_y", [round(v, 4) for v in pred])
put("P312_SSE_original_scale", round(float(np.sum((np.array(ey) - np.array(pred)) ** 2)), 6))
put("P312_R2_log_scale", round(float(1 - np.sum((np.array(lz) - (b0e + b1e * np.array(ex))) ** 2)
                                   / np.sum((np.array(lz) - lzb) ** 2)), 6))

# ==========================================================================
# 5. FIGURE 3.2 SUPPORT — the SSE surface and the two normal-equation lines
#    Normal equations:  (E0) n*th0 + (sum x) th1 = sum y
#                       (E1) (sum x) th0 + (sum x^2) th1 = sum xy
# ==========================================================================
head("5. Normal-equation coefficients (figure 3.2 support)")
put("NE_E0", [n, int(sum(xs)), int(sum(ys))], "n, sum x, sum y")
put("NE_E1", [int(sum(xs)), sum_xx, sum_xy], "sum x, sum x^2, sum xy")
put("NE_det", n * sum_xx - int(sum(xs)) ** 2, "= n * Sxx")
put("NE_det_check", n * float(Sxx))
put("NE_E0_line", [ -float(sum(xs)) / n, float(sum(ys)) / n], "th0 = (sum y - (sum x) th1)/n : slope, intercept")
put("NE_E1_line", [ -float(sum_xx) / float(sum(xs)), float(sum_xy) / float(sum(xs))],
    "th0 = (sum xy - (sum x^2) th1)/(sum x)")
# SSE value at the optimum and at a couple of nearby points, for the contour figure
def sse_at(t0, t1):
    return float(sum((b - t0 - t1 * a) ** 2 for a, b in zip(xs, ys)))
put("SSE_at_opt", round(sse_at(55, 5), 6))
put("SSE_at_50_5", round(sse_at(50, 5), 4))
put("SSE_at_55_6", round(sse_at(55, 6), 4))
put("SSE_at_45_7", round(sse_at(45, 7), 4))
put("SSE_curvature_th0", 2 * n, "d2 SSE/d th0^2 = 2n")
put("SSE_curvature_th1", 2 * sum_xx, "d2 SSE/d th1^2 = 2 sum x^2")
put("SSE_cross", 2 * int(sum(xs)), "d2 SSE/d th0 d th1 = 2 sum x")
put("Hessian_det", 4 * (n * sum_xx - int(sum(xs)) ** 2), "= 4 n Sxx > 0 : strict minimum")

# ==========================================================================
# 6. LINEAR-LMS CONSISTENCY CHECK (the [UNSOLVED EXAMPLE] of L24 slide 4)
#    Y = th0 + th1 X + W, W indep. of X, E[W] = 0  =>  cov(X,Y)/var(X) = th1.
#    Verified numerically for a non-normal X and a non-normal W.
# ==========================================================================
head("6. cov(X,Y)/var(X) = theta1 — numerical verification")
rng2 = np.random.default_rng(7)
N = 4_000_000
Xs = rng2.exponential(scale=3.0, size=N)          # skewed, non-normal
Ws = rng2.laplace(loc=0.0, scale=2.0, size=N)     # heavy-tailed, mean 0
T0, T1 = 55.0, 5.0
Ys = T0 + T1 * Xs + Ws
cov = float(np.mean((Xs - Xs.mean()) * (Ys - Ys.mean())))
var = float(np.var(Xs))
put("MC_cov_XY", round(cov, 4))
put("MC_var_X", round(var, 4), "theory 9 for Exp(1/3)")
put("MC_cov_over_var", round(cov / var, 5), "theory 5")
put("MC_EY_minus_th1EX", round(float(Ys.mean() - (cov / var) * Xs.mean()), 4), "theory 55")

# ==========================================================================
# 7. ML SIDE-NUMBERS AND SAMPLE-MOMENT FORMS (L24 slide 3; B&T §9.2)
#    sigma-hat^2_ML = SSE/n (biased low), sigma-hat^2 = SSE/(n-2) (unbiased).
#    The linear-LMS reading of theta1-hat uses sample covariance / sample variance.
# ==========================================================================
head("7. ML variance estimate and the sample-moment reading of the formulas")
put("sigma2_ML", float(SSE) / n, "SSE/n — the maximizer of the likelihood over sigma^2")
put("sigma2_unbiased", float(SSE) / (n - 2), "SSE/(n-2) — the unbiased 'standard error' version")
put("sigma2_ML_bias_factor", round((n - 2) / n, 6), "E[sigma^2_ML] = (n-2)/n * sigma^2")
put("samp_cov", float(Sxy) / n, "Sxy/n : the sample covariance of (x,y)")
put("samp_var_x", float(Sxx) / n, "Sxx/n : the sample variance of x")
put("samp_var_y", float(Syy) / n, "Syy/n : the sample variance of y")
put("samp_cov_over_var", (float(Sxy) / n) / (float(Sxx) / n), "= theta1-hat = 5")
put("logL_const_term", round(float(-n / 2 * np.log(2 * np.pi)), 6), "-(n/2) ln(2 pi)")
# value of the maximized log-likelihood, for the record
sig2ml = float(SSE) / n
put("logL_max", round(float(-n / 2 * np.log(2 * np.pi * sig2ml) - float(SSE) / (2 * sig2ml)), 6))
# E[SSE] = (n-2) sigma^2 with the sigma the widget anchors already confirm
put("ESSE_over_sigma2", n - 2, "E[SSE]/sigma^2 = n-2 = 6")
put("sigma_ML_width_factor", round(float(np.sqrt((n - 2) / n)), 6),
    "sqrt(3/4): ML-based intervals are this fraction of the correct width")
put("sigma_ML_too_narrow_pct", round(100 * (1 - float(np.sqrt((n - 2) / n))), 4), "percent too narrow")

# intermediate roots quoted in the section-3.5 arithmetic
put("sqrt_Sxx", round(float(Sxx) ** 0.5, 6), "sqrt(42)")
put("se_th0_radicand", round(1.0 / n + float(xbar) ** 2 / float(Sxx), 6), "1/n + xbar^2/Sxx")
put("se_th0_root", round((1.0 / n + float(xbar) ** 2 / float(Sxx)) ** 0.5, 6))

# --- Practice 3.9: sigma known to be 3
z975 = float(stats.norm.ppf(0.975))
put("P39_z975", round(z975, 6))
put("P39_sd_known", round(3.0 / float(Sxx) ** 0.5, 6), "sigma/sqrt(Sxx) with sigma = 3")
put("P39_half_width", round(z975 * 3.0 / float(Sxx) ** 0.5, 6))
put("P39_ci", [round(float(th1) - z975 * 3.0 / float(Sxx) ** 0.5, 6),
                round(float(th1) + z975 * 3.0 / float(Sxx) ** 0.5, 6)])
put("P39_t_over_z_n8", round(tcrit / z975, 6), "widening factor at n = 8 (6 d.o.f.)")
put("P39_t_over_z_n30", round(float(stats.t.ppf(0.975, 28)) / z975, 6), "at n = 30 (28 d.o.f.)")
put("P39_tcrit_n30", round(float(stats.t.ppf(0.975, 28)), 6))

# --- Practice 3.5: a dataset with R^2 = 0 but an exact relation
qx = [-2, -1, 0, 1, 2]
qy = [v * v for v in qx]
qxb = F(sum(qx), len(qx))
qyb = F(sum(qy), len(qy))
qSxy = sum((F(a) - qxb) * (F(b) - qyb) for a, b in zip(qx, qy))
qSxx = sum((F(a) - qxb) ** 2 for a in qx)
qSyy = sum((F(b) - qyb) ** 2 for b in qy)
put("P35_x", qx)
put("P35_y", qy)
put("P35_xbar", str(qxb))
put("P35_ybar", str(qyb))
put("P35_Sxy", str(qSxy), "exactly 0")
put("P35_Sxx", str(qSxx))
put("P35_Syy", str(qSyy))
put("P35_th1", str(qSxy / qSxx))
put("P35_th0", str(qyb - (qSxy / qSxx) * qxb))
put("P35_R2", float(qSxy ** 2) / float(qSxx * qSyy))
put("P35_sum_x_cubed", int(sum(v ** 3 for v in qx)), "= 0, which is why Sxy = 0")

# --- centred Pisa fit: same slope, intercept becomes ybar
pcx = np.array([v - 1981 for v in py], dtype=float)
pcl = np.array(pl, dtype=float)
pcSxy = float(np.sum((pcx - pcx.mean()) * (pcl - pcl.mean())))
pcSxx = float(np.sum((pcx - pcx.mean()) ** 2))
pc_th1 = pcSxy / pcSxx
put("pisa_centred_th1", round(pc_th1, 10), "unchanged by centring")
put("pisa_centred_th0", round(float(pcl.mean()) - pc_th1 * float(pcx.mean()), 6),
    "= ybar = 2.969369")

with open("d:/Python-UV/MIT_Applied_Prob/computes/g7_s3.json", "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1, default=str)
print("\nwrote computes/g7_s3.json with", len(R), "keys")
