# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Every number quoted in notes/src/fragments/g3_s1.html.

Sources: L08 slides 2-8, rec08 P1-P3(a-e), rec09 P2 (memorylessness),
B&T Problem 3.9 (p.187), B&T Example 3.13 (p.165), B&T section 3.3.

Run:  uv run computes/g3_s1.py
Writes computes/g3_s1.json.
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy import integrate, stats

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R: dict = {}


def show(key, val, note=""):
    R[key] = val
    print(f"{key:46s} = {val}   {note}")


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


# =====================================================================
head("A. PDF basics: normalization, area, the delta-interval reading (L08 slide 2)")
# =====================================================================

# A pdf may exceed 1: uniform on [0, w] has height 1/w.
for w in (1.0, 0.5, 0.1, 0.02):
    show(f"unif_height_w{w}", round(1.0 / w, 6), "= 1/w, the density value")

# Delta-slab approximation for the exponential lambda=1, at x=0.5
lam, x0 = 1.0, 0.5
for delta in (0.5, 0.1, 0.01, 0.001):
    exact = math.exp(-lam * x0) - math.exp(-lam * (x0 + delta))
    approx = lam * math.exp(-lam * x0) * delta
    show(f"delta_slab_exact_d{delta}", round(exact, 9))
    show(f"delta_slab_approx_d{delta}", round(approx, 9))
    show(f"delta_slab_relerr_d{delta}", round(abs(approx - exact) / exact, 6))

# Practice: f(x) = c x on [0,2]
show("p11_c", str(F(1, 2)), "from c*2^2/2 = 1")
show("p11_P_X_le_1", str(F(1, 4)))
show("p11_P_X_le_1_dec", round(0.25, 6))
# f(x) = 3x^2 on [0,1]: P(0.2<=X<=0.5)
show("p12_val", round(0.5 ** 3 - 0.2 ** 3, 6), "= 0.125 - 0.008")

# =====================================================================
head("B. rec08 P1 - quadratic pdf  f_Z(z) = gamma (1+z^2) on (-2,1)")
# =====================================================================

# antiderivative G(z) = z + z^3/3
G = lambda z: z + z ** 3 / 3
show("recP1_G_at_1", str(F(1) + F(1, 3)), "= 4/3")
show("recP1_G_at_m2", str(F(-2) + F(-8, 3)), "= -14/3")
show("recP1_integral_no_gamma", str((F(1) + F(1, 3)) - (F(-2) + F(-8, 3))), "= 6")
show("recP1_gamma", str(F(1, 6)))
show("recP1_gamma_dec", round(1 / 6, 6))
num, err = integrate.quad(lambda z: (1 + z ** 2) / 6, -2, 1)
show("recP1_scipy_norm_check", (round(num, 12), f"{err:.2e}"))
show("recP1_cdf_constant", str(F(14, 3)), "the -G(-2) term")
# CDF spot values
FZ = lambda z: (z + z ** 3 / 3 + 14 / 3) / 6
for z in (-2, -1, 0, 0.5, 1):
    show(f"recP1_FZ_{z}", round(FZ(z), 6))
show("recP1_FZ_frac_at_0", str(F(14, 3) / 6), "= 7/9")
show("recP1_FZ_frac_at_m1", str((F(-1) + F(-1, 3) + F(14, 3)) / 6), "= 10/18 = 5/9")
show("recP1_density_max_at_m2", round((1 + 4) / 6, 6), "f_Z(-2^+) = 5/6")
show("recP1_density_min_at_0", round(1 / 6, 6))
# practice: P(-1 <= Z <= 1)
show("recP1_P_m1_to_1", str(F(1, 6) * ((F(1) + F(1, 3)) - (F(-1) + F(-1, 3)))), "= 4/9")
show("recP1_P_m1_to_1_dec", round(4 / 9, 6))
# mean of Z (practice)
mZ, _ = integrate.quad(lambda z: z * (1 + z ** 2) / 6, -2, 1)
show("recP1_mean_scipy", round(mZ, 8))
show("recP1_mean_exact", str(F(1, 6) * ((F(1, 2) + F(1, 4)) - (F(4, 2) + F(16, 4)))), "= -7/8")
show("recP1_mean_exact_dec", round(-7 / 8, 6))
show("recP1_mean_bracket", str((F(1, 2) + F(1, 4)) - (F(4, 2) + F(16, 4))), "3/4 - 6 = -21/4")

# =====================================================================
head("C. Expectation / variance by integration (L08 slide 3)")
# =====================================================================

# f(x) = 2x on [0,1]  (used in practice)
show("p2a_mean", str(F(2, 3)))
show("p2a_EX2", str(F(1, 2)))
show("p2a_var", str(F(1, 2) - F(4, 9)), "= 1/18")
show("p2a_var_dec", round(1 / 18, 6))
m, _ = integrate.quad(lambda x: x * 2 * x, 0, 1)
v, _ = integrate.quad(lambda x: (x - 2 / 3) ** 2 * 2 * x, 0, 1)
show("p2a_scipy", (round(m, 8), round(v, 8)))

# E[g(X)] check: g(x) = x^2 for uniform[0,1]
show("p2b_Eg", str(F(1, 3)))

# =====================================================================
head("D. Continuous uniform on [a,b]  (L08 slide 3 blanks)")
# =====================================================================

for (a, b) in [(0, 1), (0, 10), (2, 7), (-1, 3), (0, 5)]:
    n = b - a
    mean = (a + b) / 2
    var = (b - a) ** 2 / 12
    # numeric confirmation by quadrature
    mq, _ = integrate.quad(lambda x: x / n, a, b)
    vq, _ = integrate.quad(lambda x: (x - mean) ** 2 / n, a, b)
    show(f"unif_{a}_{b}_height", round(1 / n, 8))
    show(f"unif_{a}_{b}_mean", (round(mean, 8), round(mq, 8)))
    show(f"unif_{a}_{b}_var", (round(var, 8), round(vq, 8)))
    show(f"unif_{a}_{b}_sd", round(math.sqrt(var), 6))
show("unif_2_7_var_frac", str(F(25, 12)))
# the substitution u = x - (a+b)/2 gives (1/(b-a)) * u^3/3 evaluated at +-(b-a)/2
show("unif_var_algebra", "2*((b-a)/2)^3/3/(b-a) = (b-a)^2/12")
show("unif_var_check_symbolic", round(2 * (5 / 2) ** 3 / 3 / 5, 8), "b-a=5 -> 25/12")
show("unif_25_over_12", round(25 / 12, 6))

# =====================================================================
head("E. CDFs: continuous, discrete staircase, mixed (L08 slides 4-5)")
# =====================================================================

# discrete staircase of L08 slide 4: masses 1/6 at 1, 3/6 at 2, 2/6 at 4
show("stair_pmf", {1: "1/6", 2: "3/6", 4: "2/6"})
show("stair_cdf_levels", {1: "1/6", 2: "4/6", 4: "6/6 = 1"})
show("stair_cdf_dec", {1: round(1 / 6, 6), 2: round(4 / 6, 6), 4: 1.0})

# L08 slide 5 mixed distribution: uniform slab on [0,1] of total mass 1/2 plus
# an atom of mass 1/2 at x = 1/2.  Slab height = 1/2.
show("mix_slab_height", 0.5)
show("mix_cdf_at_half_minus", str(F(1, 4)))
show("mix_cdf_at_half_plus", str(F(3, 4)))
show("mix_cdf_at_1", 1.0)
show("mix_mean", str(F(1, 2) * F(1, 2) + F(1, 2) * F(1, 2)), "= 1/2 (slab mean 1/2, atom 1/2)")

# =====================================================================
head("F. rec08 P2 - Al's taxi/bus waiting time (B&T Problem 3.9, p.187)")
# =====================================================================

p_taxi_waiting = F(2, 3)
p_must_wait = 1 - p_taxi_waiting
p_taxi_gt_5 = F(1, 2)              # taxi ~ U[0,10]
pA = p_taxi_waiting + p_must_wait * p_taxi_gt_5
show("taxi_p_wait", str(p_must_wait))
show("taxi_p_taxi_gt5", str(p_taxi_gt_5), "P(U[0,10] > 5)")
show("taxi_p_bus_branch", str(p_must_wait * p_taxi_gt_5), "= 1/6")
show("taxi_PA", str(pA), "= 5/6")
show("taxi_PA_dec", round(5 / 6, 6))
pY0 = p_taxi_waiting / pA
pY5 = (p_must_wait * p_taxi_gt_5) / pA
show("taxi_pY0", (str(pY0), str(F(12, 15))), "= 4/5")
show("taxi_pY5", (str(pY5), str(F(3, 15))), "= 1/5")
show("taxi_pY_sum", str(pY0 + pY5))
show("taxi_1_minus_PA", str(1 - pA), "= 1/6")
show("taxi_fZ_height", str(F(1, 5)), "Z ~ U[0,5]")
# CDF on [0,5): P(A)*F_Y(x) + (1-P(A))*F_Z(x) = (5/6)(4/5) + (1/6)(x/5)
show("taxi_F_const_term", str(pA * pY0), "= 2/3")
show("taxi_F_slope", str((1 - pA) * F(1, 5)), "= 1/30")
FX = lambda x: 0.0 if x < 0 else (1.0 if x >= 5 else 2 / 3 + x / 30)
for x in (-1, 0, 1, 2.5, 4.999, 5, 7):
    show(f"taxi_FX_{x}", round(FX(x), 6))
show("taxi_FX_at_5_minus_frac", str(F(2, 3) + F(5, 30)), "= 5/6")
show("taxi_jump_at_0", str(F(2, 3)))
show("taxi_jump_at_5", str(1 - (F(2, 3) + F(5, 30))), "= 1/6")
EY = 0 * pY0 + 5 * pY5
EZ = F(5, 2)
EX = pA * EY + (1 - pA) * EZ
show("taxi_EY", str(EY), "= 1")
show("taxi_EZ", str(EZ), "= 5/2")
show("taxi_EX", (str(EX), str(F(15, 12))), "= 5/4 minutes")
show("taxi_EX_dec", round(5 / 4, 6))
# Monte-Carlo cross-check of the whole story
rng = np.random.default_rng(20101005)
N = 4_000_000
u_stand = rng.random(N) < 2 / 3            # taxi already waiting
taxi = rng.random(N) * 10                  # next taxi arrival, U[0,10]
wait = np.where(u_stand, 0.0, np.minimum(taxi, 5.0))
show("taxi_MC_mean", round(float(wait.mean()), 5), "target 1.25")
show("taxi_MC_F_2.5", round(float((wait <= 2.5).mean()), 5), "target 0.75")
show("taxi_MC_F_5minus", round(float((wait < 5).mean()), 5), "target 5/6=0.8333")
show("taxi_F_2.5_exact", round(2 / 3 + 2.5 / 30, 6))

# =====================================================================
head("G. Exponential (rec08 P3 a-c)")
# =====================================================================

for lam in (0.5, 1.0, 2.0, 0.2):
    mq, _ = integrate.quad(lambda x, L=lam: x * L * math.exp(-L * x), 0, np.inf)
    m2q, _ = integrate.quad(lambda x, L=lam: x * x * L * math.exp(-L * x), 0, np.inf)
    show(f"exp_lam{lam}_mean", (round(mq, 8), round(1 / lam, 8)))
    show(f"exp_lam{lam}_EX2", (round(m2q, 8), round(2 / lam ** 2, 8)))
    show(f"exp_lam{lam}_var", (round(m2q - mq ** 2, 8), round(1 / lam ** 2, 8)))
    show(f"exp_lam{lam}_sd", round(1 / lam, 8))
# the boundary term of the integration by parts really vanishes
for lam in (0.5, 1.0, 2.0):
    for X in (5, 20, 100):
        pass
show("exp_bdry_x_e_1_at_100", f"{100*math.exp(-100):.3e}", "x e^{-x} at x=100")
show("exp_bdry_x2_e_1_at_100", f"{10000*math.exp(-100):.3e}")
# numbers used in prose/practice
show("exp_lam02_mean", 5.0)
show("exp_lam02_P_gt_10", round(math.exp(-2), 6))
show("exp_lam02_P_gt_5", round(math.exp(-1), 6))
show("exp_lam02_P_le_5", round(1 - math.exp(-1), 6))
show("exp_lam02_median", round(math.log(2) / 0.2, 6), "= 5 ln2")
show("ln2", round(math.log(2), 6))
show("exp_P_within_1sd", round(1 - math.exp(-1), 6), "P(X <= mean) for any lambda")
show("exp_lam1_P_1_to_2", round(math.exp(-1) - math.exp(-2), 6))

# =====================================================================
head("H. Memorylessness (rec09 P2 / B&T Example 3.13, p.165)")
# =====================================================================

lam = 0.4
for t in (0, 1, 3, 10):
    for x in (0.5, 2, 5):
        cond = math.exp(-lam * (t + x)) / math.exp(-lam * t)
        show(f"mem_lam{lam}_t{t}_x{x}", (round(cond, 8), round(math.exp(-lam * x), 8)))
show("mem_max_abs_dev",
     max(abs(math.exp(-lam * (t + x)) / math.exp(-lam * t) - math.exp(-lam * x))
         for t in (0, 1, 3, 10, 50) for x in (0.5, 2, 5, 9)))
# residual mean life is always 1/lambda
show("mem_residual_mean_lam0.4", round(1 / 0.4, 6))
# practice: bulb mean 1000 h, still on at 800 h, P(lasts 200 more)
show("mem_bulb_P200_more", round(math.exp(-200 / 1000), 6))
show("mem_bulb_P_fresh_200", round(math.exp(-0.2), 6))
show("mem_bulb_E_remaining", 1000)

# =====================================================================
head("I. Max and min of independent exponentials (rec08 P3 d,e)")
# =====================================================================

lam = 1.0
# max of 3
fZ = lambda z: 3 * lam * math.exp(-lam * z) * (1 - math.exp(-lam * z)) ** 2
tot, _ = integrate.quad(fZ, 0, np.inf)
mZ, _ = integrate.quad(lambda z: z * fZ(z), 0, np.inf)
show("max3_pdf_integrates_to", round(tot, 10))
show("max3_mean_quad", round(mZ, 8))
show("max3_mean_formula", round((1 + 1 / 2 + 1 / 3) / lam, 8), "= 11/6")
show("max3_mean_frac", str(F(11, 6)))
show("max3_mode", round(math.log(3) / lam, 6), "argmax of f_Z, = ln 3")
show("max3_F_at_1", round((1 - math.exp(-1)) ** 3, 6))
# min of 2
fW = lambda w: 2 * lam * math.exp(-2 * lam * w)
totW, _ = integrate.quad(fW, 0, np.inf)
mW, _ = integrate.quad(lambda w: w * fW(w), 0, np.inf)
show("min2_pdf_integrates_to", round(totW, 10))
show("min2_mean", (round(mW, 8), round(1 / (2 * lam), 8)))
show("min2_var", round(1 / (2 * lam) ** 2, 8))
# general: min of n exponentials with rates lam_i is exponential with sum of rates
rates = [0.5, 1.5, 2.0]
show("min_general_rates", rates)
show("min_general_sum", sum(rates))
show("min_general_mean", round(1 / sum(rates), 6))
# Monte Carlo cross-check
rng = np.random.default_rng(7)
N = 2_000_000
E3 = rng.exponential(1.0, size=(N, 3))
show("max3_MC_mean", round(float(E3.max(axis=1).mean()), 5), "target 1.83333")
show("min2_MC_mean", round(float(E3[:, :2].min(axis=1).mean()), 5), "target 0.5")
Eg = rng.exponential(1.0 / np.array(rates), size=(N, 3))
show("min_general_MC_mean", round(float(Eg.min(axis=1).mean()), 5), "target 0.25")
# practice: three machines rates 1/10, 1/20, 1/30 per hour
rr = [1 / 10, 1 / 20, 1 / 30]
show("p_min_machines_rate", round(sum(rr), 8))
show("p_min_machines_mean", round(1 / sum(rr), 6))
show("p_min_machines_frac", str(F(60, 11)))

# =====================================================================
head("J. The normal (L08 slides 6-7, B&T section 3.3)")
# =====================================================================

# Gaussian integral: the 1/sqrt(2 pi) prefactor
I, _ = integrate.quad(lambda x: math.exp(-x ** 2 / 2), -np.inf, np.inf)
show("gauss_integral", round(I, 10))
show("sqrt_2pi", round(math.sqrt(2 * math.pi), 10))
show("gauss_integral_matches", abs(I - math.sqrt(2 * math.pi)) < 1e-9)
show("one_over_sqrt_2pi", round(1 / math.sqrt(2 * math.pi), 6))

# standard normal mean and variance by quadrature
phi = lambda x: math.exp(-x ** 2 / 2) / math.sqrt(2 * math.pi)
m, _ = integrate.quad(lambda x: x * phi(x), -np.inf, np.inf)
v, _ = integrate.quad(lambda x: x * x * phi(x), -np.inf, np.inf)
show("stdnormal_mean", round(m, 10))
show("stdnormal_var", round(v, 10))

# general normal N(mu, sigma^2)
for (mu, sig) in [(2, 4), (-1, 0.5), (10, 3)]:
    m, _ = integrate.quad(lambda x, M=mu, S=sig: x * stats.norm.pdf(x, M, S), -np.inf, np.inf)
    v, _ = integrate.quad(lambda x, M=mu, S=sig: (x - M) ** 2 * stats.norm.pdf(x, M, S), -np.inf, np.inf)
    show(f"normal_mu{mu}_sig{sig}_mean", (round(m, 8), mu))
    show(f"normal_mu{mu}_sig{sig}_var", (round(v, 8), sig ** 2))
    show(f"normal_mu{mu}_sig{sig}_peak", round(1 / (sig * math.sqrt(2 * math.pi)), 6))

# L08 slide 7 example : X ~ N(2,16), P(X <= 3)
show("slide7_sigma", math.sqrt(16))
show("slide7_z", round((3 - 2) / 4, 6))
show("slide7_Phi_0.25_scipy", round(float(stats.norm.cdf(0.25)), 6))
show("slide7_Phi_0.25_table", 0.5987)
show("slide7_direct", round(float(stats.norm.cdf(3, 2, 4)), 6))

# table spot values quoted in the fragment
for z in (0.0, 0.25, 0.5, 0.71, 1.0, 1.5, 1.71, 1.96, 2.0, 2.5, 3.0):
    show(f"Phi_{z}", round(float(stats.norm.cdf(z)), 6))
show("Phi_minus_0.5", round(float(stats.norm.cdf(-0.5)), 6))
show("Phi_minus_0.5_via_symmetry", round(1 - float(stats.norm.cdf(0.5)), 6))
show("Phi_1.71_table", 0.9564)

# k-sigma probabilities (B&T Problem 12)
for k in (1, 2, 3):
    show(f"normal_P_gt_{k}sigma", round(float(1 - stats.norm.cdf(k)), 6))
    show(f"normal_P_abs_gt_{k}sigma", round(float(2 * (1 - stats.norm.cdf(k))), 6))
    show(f"normal_P_within_{k}sigma", round(float(2 * stats.norm.cdf(k) - 1), 6))
    # "one time in N" odds quoted in Practice 1.17 -- two-sided and one-sided
    show(f"normal_odds_abs_gt_{k}sigma", round(1.0 / float(2 * (1 - stats.norm.cdf(k))), 1))
    show(f"normal_odds_gt_{k}sigma", round(1.0 / float(1 - stats.norm.cdf(k)), 1))

# practice: X ~ N(70, 25) (test scores), P(65 <= X <= 80)
show("pnorm_z_lo", round((65 - 70) / 5, 4))
show("pnorm_z_hi", round((80 - 70) / 5, 4))
show("pnorm_Phi_2", round(float(stats.norm.cdf(2)), 6))
show("pnorm_Phi_m1", round(float(stats.norm.cdf(-1)), 6))
show("pnorm_answer", round(float(stats.norm.cdf(2) - stats.norm.cdf(-1)), 6))
show("pnorm_answer_table", round(0.9772 - (1 - 0.8413), 6))

# practice: Y = 3X + 1 with X ~ N(2,16)
show("pY_mean", 3 * 2 + 1)
show("pY_var", 9 * 16)
show("pY_sd", round(math.sqrt(144), 6))
show("pY_P_le_19", round(float(stats.norm.cdf(19, 7, 12)), 6))
show("pY_z", round((19 - 7) / 12, 6))
show("pY_Phi_1", round(float(stats.norm.cdf(1)), 6))

# =====================================================================
head("K. Widget arithmetic (w-g3s1-normal, w-g3s1-memoryless)")
# =====================================================================

# JS Phi via Zelen & Severo (A&S 26.2.17) -- replicate exactly here.
def phi_js(z):
    p, b = 0.2316419, [0.319381530, -0.356563782, 1.781477937, -1.821255978, 1.330274429]
    s = 1.0 if z >= 0 else -1.0
    z = abs(z)
    t = 1.0 / (1.0 + p * z)
    poly = t * (b[0] + t * (b[1] + t * (b[2] + t * (b[3] + t * b[4]))))
    tail = math.exp(-z * z / 2) / math.sqrt(2 * math.pi) * poly
    val = 1.0 - tail
    return val if s > 0 else 1.0 - val


worst, worst_z = 0.0, None
for i in range(-6000, 6001):
    z = i / 1000.0
    e = abs(phi_js(z) - float(stats.norm.cdf(z)))
    if e > worst:
        worst, worst_z = e, z
show("widget_Phi_max_abs_err", f"{worst:.3e}")
show("widget_Phi_worst_z", worst_z)
show("widget_Phi_spotcheck", {str(z): (round(phi_js(z), 7), round(float(stats.norm.cdf(z)), 7))
                              for z in (-2.0, -0.5, 0.0, 0.25, 1.0, 1.96, 3.0)})
# widget default readout: mu=0, sigma=1, [a,b]=[-1,1]
show("widget_default_prob", round(float(stats.norm.cdf(1) - stats.norm.cdf(-1)), 6))
show("widget_example_mu2_sig4_a0_b6",
     round(float(stats.norm.cdf(6, 2, 4) - stats.norm.cdf(0, 2, 4)), 6))
show("widget_peak_sig1", round(1 / math.sqrt(2 * math.pi), 6))
show("widget_peak_sig0.4", round(1 / (0.4 * math.sqrt(2 * math.pi)), 6))

# memorylessness widget: conditional tail equals fresh tail
show("widget_mem_check",
     max(abs(math.exp(-l * (t + x)) / math.exp(-l * t) - math.exp(-l * x))
         for l in (0.2, 0.5, 1.0, 2.0) for t in (0, 1, 2, 5, 10) for x in (0, 1, 3, 7)))

out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(R, indent=1, default=str), encoding="utf-8")
print("\nwrote", out)
