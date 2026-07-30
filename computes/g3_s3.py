# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "sympy"]
# ///
"""G3 §3 — The four faces of Bayes' rule (L10 slides 1-3, rec11 P1-P2, B&T §3.6).

Every number quoted in fragments/g3_s3.html is produced here.
Symbolic derivations are in the prose; this file only *checks* them numerically.
"""
import io
import json
import sys
from math import exp, log, sqrt, pi, lgamma, erf

import numpy as np
from scipy import integrate, stats, special
import sympy as sp

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
R = {}


def put(k, v, note=""):
    R[k] = v
    print(f"{k:44s} = {v!r}" + (f"   # {note}" if note else ""))


# ------------------------------------------------------------------ #
print("\n== A. (D|D) radar recap — G1 §2.4 Example 2.5, L10 slide 2 ==")
pA, sens, fa = 0.05, 0.99, 0.10
pB = pA * sens + (1 - pA) * fa
put("A_PB", round(pB, 6))
put("A_post", round(pA * sens / pB, 6))
put("A_prior_odds", round(pA / (1 - pA), 6))
put("A_LR", round(sens / fa, 6))
put("A_post_odds", round((pA / (1 - pA)) * (sens / fa), 6))
put("A_boost_factor", round((pA * sens / pB) / pA, 6))

# ------------------------------------------------------------------ #
print("\n== B. (C|C) light bulb, B&T Example 3.19: Lambda~U[1,3/2], Y|L=l ~ Exp(l) ==")
lam_lo, lam_hi = 1.0, 1.5
f_prior = 1.0 / (lam_hi - lam_lo)                      # = 2
put("B_prior_height", f_prior)
put("B_prior_mean", (lam_lo + lam_hi) / 2)
# E[Y] = E[1/Lambda] = int_1^{3/2} 2/lambda dlambda = 2 ln(3/2)  -- NOT 1/E[Lambda]
put("B_prior_mean_lifetime", round(integrate.quad(lambda t: 2.0 / t, lam_lo, lam_hi)[0], 6))
put("B_prior_mean_lifetime_closed", round(2 * log(1.5), 6))
put("B_recip_prior_mean_rate", round(1 / 1.25, 6), "1/E[Lambda] != E[1/Lambda]")


def denom_closed(y):
    """int_1^{3/2} 2 t e^{-t y} dt  via antiderivative -e^{-ty}(ty+1)/y^2."""
    return (2.0 / y ** 2) * ((y + 1) * exp(-y) - (1.5 * y + 1) * exp(-1.5 * y))


for y in (0.5, 2.0, 5.0):
    num_quad = integrate.quad(lambda t: 2 * t * exp(-t * y), lam_lo, lam_hi)[0]
    put(f"B_denom_closed_y={y}", round(denom_closed(y), 9))
    put(f"B_denom_quad_y={y}", round(num_quad, 9))
    put(f"B_denom_match_y={y}", abs(num_quad - denom_closed(y)) < 1e-12)

    post = lambda l, y=y: 2 * l * exp(-l * y) / denom_closed(y)
    put(f"B_post_norm_y={y}", round(integrate.quad(post, lam_lo, lam_hi)[0], 12))
    put(f"B_post_mean_y={y}", round(integrate.quad(lambda l: l * post(l), lam_lo, lam_hi)[0], 6))
    put(f"B_post_at_1.0_y={y}", round(post(1.0), 6))
    put(f"B_post_at_1.5_y={y}", round(post(1.5), 6))
    put(f"B_post_ratio_hi_lo_y={y}", round(post(1.5) / post(1.0), 6))

# the pieces of the y=2 denominator, quoted step by step in the prose
put("B_y2_term1", round(3 * exp(-2.0), 6))
put("B_y2_term2", round(4 * exp(-3.0), 6))
put("B_y2_bracket", round(3 * exp(-2.0) - 4 * exp(-3.0), 6))
put("B_y2_denom", round(denom_closed(2.0), 6))

# ------------------------------------------------------------------ #
print("\n== C. (C|C) Gaussian prior + Gaussian noise: X~N(0,1), Y=X+W, W~N(0,s2) ==")
s2 = 0.5
yobs = 1.5
post_var = s2 / (1 + s2)
post_mean = yobs / (1 + s2)
put("C_sigma2", s2)
put("C_y", yobs)
put("C_post_mean_closed", round(post_mean, 6))
put("C_post_var_closed", round(post_var, 6))
put("C_weight_on_y", round(1 / (1 + s2), 6))


def joint(x, y=yobs, s2=s2):
    return (1 / sqrt(2 * pi)) * exp(-x * x / 2) * (1 / sqrt(2 * pi * s2)) * exp(-(y - x) ** 2 / (2 * s2))


Z = integrate.quad(joint, -12, 12)[0]
m = integrate.quad(lambda x: x * joint(x), -12, 12)[0] / Z
v = integrate.quad(lambda x: x * x * joint(x), -12, 12)[0] / Z - m * m
put("C_post_mean_numeric", round(m, 6))
put("C_post_var_numeric", round(v, 6))
put("C_marginal_y_numeric", round(Z, 6))
put("C_marginal_y_closed", round(stats.norm(0, sqrt(1 + s2)).pdf(yobs), 6))

# ------------------------------------------------------------------ #
print("\n== D. (D|C) rec11 P1: X=+-1, Y Laplacian(lambda), Z=X+Y ==")


def d_of_z(z):
    return abs(z + 1) - abs(z - 1)


def post1(z, p, lam):
    return p / (p + (1 - p) * exp(-lam * d_of_z(z)))


def post1_raw(z, p, lam):
    """unsimplified form, for cross-checking the algebra"""
    a = p * 0.5 * lam * exp(-lam * abs(z - 1))
    b = (1 - p) * 0.5 * lam * exp(-lam * abs(z + 1))
    return a / (a + b)


put("D_d_of_z_examples", {str(z): round(d_of_z(z), 6) for z in (-3, -1, -0.5, 0, 0.5, 1, 3)})
mismatch = max(abs(post1(z, p, l) - post1_raw(z, p, l))
               for z in np.linspace(-4, 4, 401) for p in (0.2, 0.5, 0.8) for l in (0.5, 1, 3))
put("D_algebra_max_mismatch", float(f"{mismatch:.3e}"), "simplified == raw")

for (p, lam) in ((0.5, 1.0), (0.3, 2.0)):
    tag = f"p={p}_lam={lam}"
    for z in (-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 5.0):
        put(f"D_{tag}_post_z={z}", round(post1(z, p, lam), 6))
    put(f"D_{tag}_plateau_hi", round(p / (p + (1 - p) * exp(-2 * lam)), 6))
    put(f"D_{tag}_plateau_lo", round(p / (p + (1 - p) * exp(2 * lam)), 6))

# limits
put("D_lim_lam0", round(post1(0.7, 0.3, 1e-9), 6), "-> p = 0.3")
put("D_lim_laminf_zpos", round(post1(0.7, 0.3, 400.0), 6))
put("D_lim_laminf_zneg", round(post1(-0.7, 0.3, 400.0), 6))
put("D_lim_p0", round(post1(0.7, 1e-9, 1.0), 9))
put("D_lim_p1", round(post1(0.7, 1 - 1e-9, 1.0), 9))

# MAP threshold and error probability
for (p, lam) in ((0.5, 1.0), (0.3, 2.0), (0.3, 0.2)):
    tag = f"p={p}_lam={lam}"
    zstar = log((1 - p) / p) / (2 * lam)
    put(f"D_{tag}_zstar", round(zstar, 6))
    put(f"D_{tag}_zstar_in_range", abs(zstar) <= 1)
    perr_closed = exp(-lam) * sqrt(p * (1 - p))

    def fY(u, lam=lam):
        return 0.5 * lam * exp(-lam * abs(u))

    # P(err) = p P(Z<=t|X=1) + (1-p) P(Z>t|X=-1),  Z|X=x ~ Laplacian shifted to x
    t = zstar
    e1 = integrate.quad(lambda z: fY(z - 1), -60, t)[0]
    e2 = integrate.quad(lambda z: fY(z + 1), t, 60)[0]
    perr_num = p * e1 + (1 - p) * e2
    put(f"D_{tag}_perr_closed", round(perr_closed, 6))
    put(f"D_{tag}_perr_numeric", round(perr_num, 6))
    put(f"D_{tag}_perr_match", abs(perr_closed - perr_num) < 1e-8 if abs(zstar) <= 1 else "threshold outside [-1,1]")
    put(f"D_{tag}_e1_term", round(p * e1, 6))
    put(f"D_{tag}_e2_term", round((1 - p) * e2, 6))
    if abs(zstar) > 1:
        # MAP rule saturates: the posterior never crosses 1/2, so we always guess
        # the prior favorite and the MAP error probability is min(p, 1-p).
        put(f"D_{tag}_post_max", round(p / (p + (1 - p) * exp(-2 * lam)), 6))
        put(f"D_{tag}_post_min", round(p / (p + (1 - p) * exp(2 * lam)), 6))
        put(f"D_{tag}_MAP_perr_true", round(min(p, 1 - p), 6))

# Gaussian comparison (B&T Example 3.20)
def post_gauss(y, p):
    return p * exp(y) / (p * exp(y) + (1 - p) * exp(-y))


def post_gauss_raw(y, p):
    a = p * stats.norm(1, 1).pdf(y)
    b = (1 - p) * stats.norm(-1, 1).pdf(y)
    return a / (a + b)


gm = max(abs(post_gauss(y, p) - post_gauss_raw(y, p)) for y in np.linspace(-5, 5, 501) for p in (0.2, 0.5, 0.8))
put("D_gauss_algebra_max_mismatch", float(f"{gm:.3e}"))
for y in (0.5, 1.0, 2.0, 5.0):
    put(f"D_gauss_post_p=0.5_y={y}", round(post_gauss(y, 0.5), 6))
put("D_gauss_perr_p0.5", round(1 - stats.norm.cdf(1.0), 6), "Q(1) for unit-variance noise")

# ------------------------------------------------------------------ #
print("\n== E. (C|D) rec11 P2: f_Q(q)=6q(1-q), Bernoulli observation ==")
q = sp.symbols("q", positive=True)
I0 = sp.integrate(6 * q * (1 - q) * (1 - q), (q, 0, 1))
I1 = sp.integrate(6 * q * (1 - q) * q, (q, 0, 1))
put("E_norm_x0_symbolic", str(I0))
put("E_norm_x1_symbolic", str(I1))
put("E_norm_x0_pieces", [str(sp.Rational(1, 2)), str(sp.Rational(2, 3)), str(sp.Rational(1, 4))])
put("E_post_x0_check_norm", str(sp.integrate(12 * q * (1 - q) ** 2, (q, 0, 1))))
put("E_post_x1_check_norm", str(sp.integrate(12 * q ** 2 * (1 - q), (q, 0, 1))))
put("E_prior_mean", str(sp.integrate(q * 6 * q * (1 - q), (q, 0, 1))))
put("E_post_x1_mean", str(sp.integrate(q * 12 * q ** 2 * (1 - q), (q, 0, 1))))
put("E_post_x0_mean", str(sp.integrate(q * 12 * q * (1 - q) ** 2, (q, 0, 1))))
put("E_pX1", str(sp.integrate(6 * q * (1 - q) * q, (q, 0, 1))))
put("E_post_x1_mode", str(sp.Rational(2, 3)))
put("E_post_x0_mode", str(sp.Rational(1, 3)))

print("\n-- general Beta update: prior Beta(a,b), k heads in n tosses --")
a0, b0, n, k = 2, 2, 10, 7
a1, b1 = a0 + k, b0 + n - k
put("E_gen_prior", [a0, b0])
put("E_gen_n_k", [n, k])
put("E_gen_post", [a1, b1])
put("E_gen_post_mean", round(a1 / (a1 + b1), 6))
put("E_gen_post_mean_frac", f"{a1}/{a1+b1}")
put("E_gen_post_mode", round((a1 - 1) / (a1 + b1 - 2), 6))
put("E_gen_post_var", round(a1 * b1 / ((a1 + b1) ** 2 * (a1 + b1 + 1)), 6))
put("E_gen_post_sd", round(sqrt(a1 * b1 / ((a1 + b1) ** 2 * (a1 + b1 + 1))), 6))
put("E_gen_sample_freq", k / n)
put("E_gen_prior_mean", a0 / (a0 + b0))
# shrinkage identity: post mean = w*(k/n) + (1-w)*prior mean, w = n/(n+a0+b0)
w = n / (n + a0 + b0)
put("E_gen_shrink_w", round(w, 6))
put("E_gen_shrink_check", round(w * (k / n) + (1 - w) * (a0 / (a0 + b0)), 6))
put("E_gen_pK", round(special.beta(a1, b1) / special.beta(a0, b0) * special.comb(n, k), 6),
    "P(K=7) marginal")
put("E_gen_pK_quad", round(integrate.quad(
    lambda t: special.comb(n, k) * t ** k * (1 - t) ** (n - k) * 6 * t * (1 - t), 0, 1)[0], 6))
put("E_beta_B_2_2", round(special.beta(2, 2), 6), "= 1/6, so 1/B = 6")
put("E_beta_B_9_5", round(special.beta(9, 5), 9))

# ------------------------------------------------------------------ #
print("\n== F. (C|D) L10 slide 3 light beam: X~Exp(1) intensity, Y|X ~ Poisson(x) ==")
for yv in (0, 1, 3, 8):
    # marginal p_Y(y) = 2^{-(y+1)}
    closed = 2.0 ** (-(yv + 1))
    num = integrate.quad(lambda x: exp(-x) * exp(-x) * x ** yv / np.math.factorial(yv), 0, 80)[0] \
        if hasattr(np, "math") else integrate.quad(
            lambda x: exp(-x) * exp(-x) * x ** yv / special.factorial(yv), 0, 80)[0]
    put(f"F_pY_closed_y={yv}", round(closed, 9))
    put(f"F_pY_quad_y={yv}", round(num, 9))
    post = lambda x, yv=yv: 2 ** (yv + 1) * x ** yv * exp(-2 * x) / special.factorial(yv)
    put(f"F_post_norm_y={yv}", round(integrate.quad(post, 0, 80)[0], 9))
    put(f"F_post_mean_y={yv}", round(integrate.quad(lambda x: x * post(x), 0, 80)[0], 6))
    put(f"F_post_mean_closed_y={yv}", (yv + 1) / 2)
    put(f"F_post_mode_y={yv}", yv / 2)
put("F_marginal_is_geometric_sum", round(sum(2.0 ** (-(y + 1)) for y in range(200)), 9))
put("F_prior_mean", 1.0)

# ------------------------------------------------------------------ #
print("\n== G. widget verification: JS log-Beta pdf vs scipy ==")


_LZ = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
       771.32342877765313, -176.61502916214059, 12.507343278686905,
       -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]


def lgamma_js(x):
    """Byte-for-byte port of the Lanczos log-gamma used in the widget script."""
    if x < 0.5:
        return log(pi / abs(np.sin(pi * x))) - lgamma_js(1 - x)
    x -= 1.0
    a = _LZ[0]
    t = x + 7 + 0.5
    for i in range(1, 9):
        a += _LZ[i] / (x + i)
    return 0.5 * log(2 * pi) + (x + 0.5) * log(t) - t + log(a)


def lbeta(a, b):
    return lgamma_js(a) + lgamma_js(b) - lgamma_js(a + b)


def beta_pdf_js(x, a, b):
    if x <= 0 or x >= 1:
        return 0.0
    return exp((a - 1) * log(x) + (b - 1) * log(1 - x) - lbeta(a, b))


worst = 0.0
for a in (0.5, 1, 2, 3.7, 9, 25):
    for b in (0.5, 1, 2, 5, 14, 40):
        for x in np.linspace(0.01, 0.99, 99):
            worst = max(worst, abs(beta_pdf_js(x, a, b) - stats.beta(a, b).pdf(x)))
put("G_beta_pdf_max_abs_err", float(f"{worst:.3e}"))
put("G_lgamma_check_lgamma(5)", round(lgamma(5), 9), "= ln 24")
put("G_widget_default_readout", {
    "prior": "Beta(2,2)", "n": 10, "k": 7, "post": "Beta(9,5)",
    "post_mean": round(9 / 14, 6), "post_mode": round(8 / 12, 6), "freq": 0.7})

# ------------------------------------------------------------------ #
print("\n== H. practice-question numbers ==")
# H1: radar-style D|C with exponential-ish? -> use Gaussian detector practice
put("H1_post", round(post_gauss(0.4, 0.5), 6))
put("H1_post_p03", round(post_gauss(0.4, 0.3), 6))
# H2: light bulb posterior odds at y=5
put("H2_ratio_y5", round((1.5 * exp(-1.5 * 5.0)) / (1.0 * exp(-1.0 * 5.0)), 6))
# H3: Laplacian threshold when it falls outside [-1,1]
put("H3_zstar_p0.05_lam0.2", round(log(0.95 / 0.05) / (2 * 0.2), 6))
# H4: Beta with uniform prior
put("H4_post_uniform_3of4", [1 + 3, 1 + 1])
put("H4_post_mean", round(4 / 6, 6))
put("H4_post_mode", round(3 / 4, 6))
put("H4_laplace_rule", "posterior mean = (k+1)/(n+2) for a uniform prior")
# H5: two-sided exponential noise, p=1/2, lambda=2 error prob
put("H5_perr_lam2_p05", round(exp(-2.0) * sqrt(0.25), 6))
put("H5_perr_lam1_p05", round(exp(-1.0) * sqrt(0.25), 6))
# H6: photon count, y=8
put("H6_post_mean_y8", 4.5)
put("H6_pY8", round(2.0 ** -9, 9))
# H7: sequential vs batch beta update
put("H7_seq_equals_batch", [2 + 7, 2 + 3])

# ------------------------------------------------------------------ #
print("\n== I. appendix: the three L10 derived-distribution [UNSOLVED EXAMPLE]s ==")
# I1 ratio Y/X on the unit square
rng = np.random.default_rng(6041)
U = rng.random(4_000_000)
V = rng.random(4_000_000)
Rt = V / U
for yv in (0.5, 1.0, 2.0, 4.0):
    closed = yv / 2 if yv <= 1 else 1 - 1 / (2 * yv)
    put(f"I1_F_closed_y={yv}", round(closed, 6))
    put(f"I1_F_mc_y={yv}", round(float(np.mean(Rt <= yv)), 6))
put("I1_pdf_total", round(0.5 + 0.5, 6), "int_0^1 1/2 + int_1^inf 1/(2y^2)")
# I2 Joan
put("I2_T_range", [round(200 / 60, 6), round(200 / 30, 6)])
put("I2_fT_at_4", round(20 / (3 * 16), 6))
put("I2_fT_norm", round(integrate.quad(lambda t: 20 / (3 * t * t), 200 / 60, 200 / 30)[0], 9))
put("I2_ET", round(integrate.quad(lambda t: t * 20 / (3 * t * t), 200 / 60, 200 / 30)[0], 6))
put("I2_ET_direct", round(integrate.quad(lambda v: (200 / v) / 30, 30, 60)[0], 6))
put("I2_200_over_EV", round(200 / 45, 6))
# I3 aX+b normal
mu, sg, aa, bb = 1.0, 2.0, -3.0, 5.0
put("I3_new_mean", aa * mu + bb)
put("I3_new_var", aa ** 2 * sg ** 2)
xs = np.linspace(-40, 40, 200001)
lhs = (1 / abs(aa)) * stats.norm(mu, sg).pdf((xs - bb) / aa)
rhs = stats.norm(aa * mu + bb, abs(aa) * sg).pdf(xs)
put("I3_max_abs_err", float(f"{np.max(np.abs(lhs - rhs)):.3e}"))

# I4 practice: V ~ U[40,80], 300-mile trip, T = 300/V
d4, v_lo, v_hi = 300.0, 40.0, 80.0
put("I4_T_range", [round(d4 / v_hi, 6), round(d4 / v_lo, 6)])
put("I4_fT_coef", round(d4 / (v_hi - v_lo), 6), "f_T(t) = 7.5/t^2")
put("I4_fT_norm", round(integrate.quad(lambda t: 7.5 / t ** 2, d4 / v_hi, d4 / v_lo)[0], 9))
put("I4_ET", round(integrate.quad(lambda t: t * 7.5 / t ** 2, d4 / v_hi, d4 / v_lo)[0], 6))
put("I4_ET_closed", round(7.5 * log(2), 6))
put("I4_ET_direct", round(integrate.quad(lambda v: (d4 / v) / (v_hi - v_lo), v_lo, v_hi)[0], 6))
put("I4_d_over_EV", round(d4 / ((v_lo + v_hi) / 2), 6))
put("I4_jensen_gap", round(7.5 * log(2) - d4 / 60.0, 6))

# I5 practice: X ~ U[0,2], Y = 1/X
put("I5_support_lo", 0.5, "Y = 1/X >= 1/2")
put("I5_fY_norm", round(integrate.quad(lambda y: 1 / (2 * y ** 2), 0.5, np.inf)[0], 9))
put("I5_fY_at_1", round(1 / 2.0, 6))
put("I5_EY_truncated", [round(integrate.quad(lambda y: 1 / (2 * y), 0.5, M)[0], 6)
                        for M in (10.0, 100.0, 1000.0)])
put("I5_EY", "divergent: int_{1/2}^{M} dy/(2y) = (1/2)ln(2M) -> infinity")
put("I5_median", round(1 / 1.0, 6), "F_Y(y)=1-1/(2y)=1/2 at y=1")

# ------------------------------------------------------------------ #
print("\n== J. every remaining numeral quoted in the prose ==")
put("J_exp_m1", round(exp(-1), 6))
put("J_exp_m2", round(exp(-2), 6))
put("J_exp_m3", round(exp(-3), 6))
put("J_exp_m2p5", round(exp(-2.5), 6))
put("J_exp_p04", round(exp(0.4), 6))
put("J_exp_m04", round(exp(-0.4), 6))
put("J_exp_p08_LR", round(exp(0.8), 6))
put("J_P3.7_p03_num", round(0.3 * exp(0.4), 6))
put("J_P3.7_p03_den", round(0.3 * exp(0.4) + 0.7 * exp(-0.4), 6))
put("J_P3.7_p05_num", round(0.5 * exp(0.4), 6))
put("J_P3.7_p05_den", round(0.5 * exp(0.4) + 0.5 * exp(-0.4), 6))
put("J_ln50", round(log(50), 6))
put("J_lap_sd_at_ln50", round(sqrt(2) / log(50), 6), "sqrt(2)/lambda")
put("J_gauss_post_y3", round(1 / (1 + exp(-6)), 6))
put("J_lap_post_z3", round(1 / (1 + exp(-2)), 6))
put("J_one_plus_exp_m2", round(1 + exp(-2), 6))
put("J_beta33_sd", round(sqrt(1 / 28), 6))
put("J_beta22_sd", round(sqrt(1 / 20), 6))
put("J_beta22_var", round(2 * 2 / (4 ** 2 * 5), 6))
put("J_beta33_var", round(3 * 3 / (6 ** 2 * 7), 6))
put("J_ET_joan_closed", round(20 / 3 * log(2), 6))
put("J_ratio_EX_infinite", "E[Y/X] diverges: int_1^inf dr/(2r) = infinity")
put("J_lightbulb_mean_lifetime_at_prior_mean", round(1 / 1.25, 6))
put("J_beta_B_3_2", "2!*1!/4! = 1/12"), put("J_beta_B_4_2", "3!*1!/5! = 1/20")
put("J_beta_B_3_3", "2!*2!/5! = 1/30")
put("J_photon_y8_coef", [2 ** 9, 40320])

with open("g3_s3.json", "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1, default=str)
print("\nwrote g3_s3.json with", len(R), "keys")
