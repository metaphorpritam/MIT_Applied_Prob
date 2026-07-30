# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy"]
# ///
"""G5 §5 — synthesis + checkpoint (rec16 continuous-RV review, rec17 Poisson review).

Every number quoted in notes/src/fragments/g5_s5.html is produced here.
Exact rational arithmetic (fractions.Fraction) wherever the answer is rational;
numpy linear algebra / matrix powers for the Markov cheatsheet numbers;
numeric quadrature + Monte Carlo as independent cross-checks.
"""
import io
import json
import math
import sys
from fractions import Fraction as F

import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
R = {}


def show(k, v, note=""):
    R[k] = v
    print(f"{k:44s} = {v}" + (f"   # {note}" if note else ""))


rng = np.random.default_rng(20101102)

# ======================================================================
# PART A — Markov cheatsheet numbers (the three question types)
# ======================================================================
print("=" * 72)
print("A. THE THREE QUESTION TYPES")
print("=" * 72)

# --- A1. Chain R: the course two-state chain (L16 s5 / L17 s7 / L18 s3)
P = np.array([[0.5, 0.5],
              [0.2, 0.8]])
show("A_R_P", P.tolist())

# n-step: r(n) = P^n
for n in (1, 2, 3, 100, 101):
    Pn = np.linalg.matrix_power(P, n)
    show(f"A_R_rn_{n}", np.round(Pn, 10).tolist())

# steady state by linear solve: pi (P - I) = 0 with sum pi = 1
A = np.vstack([P.T - np.eye(2), np.ones(2)])
b = np.array([0.0, 0.0, 1.0])
pi_R, *_ = np.linalg.lstsq(A, b, rcond=None)
show("A_R_pi", pi_R.tolist(), "balance + normalization")
show("A_R_pi_exact", [str(F(2, 7)), str(F(5, 7))])
show("A_R_pi_dec", [round(2 / 7, 6), round(5 / 7, 6)])
show("A_R_mean_recurrence_t1", round(7 / 2, 6), "1/pi_1")
show("A_R_mean_recurrence_t2", round(7 / 5, 6), "1/pi_2")

# joint probabilities used in the cheatsheet demo (L18 s3 unsolved example)
# P(X1=1 and X100=1 | X0=1) = p_11 * r_11(99)
r99 = np.linalg.matrix_power(P, 99)
show("A_R_P_X1eq1_X100eq1_given_X0eq1", round(P[0, 0] * r99[0, 0], 8))
r100 = np.linalg.matrix_power(P, 100)
show("A_R_P_X100eq1_X101eq2_given_X0eq1", round(r100[0, 0] * P[0, 1], 8))

# --- A2. Chain A: the L18 slide 5 absorption chain
# states 1..5 with 4,5 absorbing (course numbering from L18 s5 text):
# use order [1,2,3,4,5] = [B, C, D, A(=4 absorbing), E(=5 absorbing)] mapped as
# 1 = B (transient), 2 = C (transient), 3 = D (transient), 4 = absorbing target, 5 = other absorbing
Q = np.array([
    [0.0, 0.5, 0.3, 0.2, 0.0],   # 1 -> 2 (.5), 3 (.3), 4 (.2)
    [0.4, 0.0, 0.6, 0.0, 0.0],   # 2 -> 1 (.4), 3 (.6)
    [0.0, 0.8, 0.0, 0.0, 0.2],   # 3 -> 2 (.8), 5 (.2)
    [0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 1.0],
])
assert np.allclose(Q.sum(axis=1), 1)
show("A_A_P", Q.tolist())

# absorption probs a_i = P(absorbed in state 4 | X0 = i): a_4=1, a_5=0,
# a_i = sum_j p_ij a_j  ->  (I - T) a = c   for transient block
T = Q[:3, :3]
c = Q[:3, 3]                     # one-step probability of hitting state 4
a_tr = np.linalg.solve(np.eye(3) - T, c)
show("A_A_absorb_a", np.round(a_tr, 8).tolist(), "a1,a2,a3 for target state 4")
show("A_A_absorb_a_frac", [str(F(x).limit_denominator(10**6)) for x in a_tr])

# expected time to absorption (either absorbing state): mu = (I-T)^{-1} 1
mu_tr = np.linalg.solve(np.eye(3) - T, np.ones(3))
show("A_A_mu", np.round(mu_tr, 8).tolist())
show("A_A_mu_frac", [str(F(x).limit_denominator(10**6)) for x in mu_tr])

# what the balance equations WOULD give on chain A (gotcha: pi=0 on transient)
vals, vecs = np.linalg.eig(Q.T)
show("A_A_eig_ones", int(np.sum(np.isclose(vals, 1))), "multiplicity of eigenvalue 1")
Q200 = np.linalg.matrix_power(Q, 200)
show("A_A_P200_row1", np.round(Q200[0], 8).tolist(), "transient entries -> 0")

# --- A3. periodic chain (L16 s6): no convergence
Pp = np.array([[0.0, 1.0, 0.0],
               [0.5, 0.0, 0.5],
               [0.0, 1.0, 0.0]])
show("A_per_r22_odd", float(np.linalg.matrix_power(Pp, 101)[1, 1]))
show("A_per_r22_even", float(np.linalg.matrix_power(Pp, 100)[1, 1]))
Ap = np.vstack([Pp.T - np.eye(3), np.ones(3)])
pi_p, *_ = np.linalg.lstsq(Ap, np.array([0., 0., 0., 1.]), rcond=None)
show("A_per_pi_solves_balance", np.round(pi_p, 8).tolist(), "balance solvable, limit still absent")
Cesaro = np.mean([np.linalg.matrix_power(Pp, n)[1, 1] for n in range(1, 20001)])
show("A_per_cesaro_r22", round(float(Cesaro), 6), "time-average -> pi_2 = 1/2")

# --- A4. gotcha figure, panel (b): state 1 transient, {2,3} recurrent aperiodic
Pb = np.array([[0.5, 0.5, 0.0],
               [0.0, 0.4, 0.6],
               [0.0, 0.5, 0.5]])
assert np.allclose(Pb.sum(1), 1)
Ab = np.vstack([Pb.T - np.eye(3), np.ones(3)])
pib, *_ = np.linalg.lstsq(Ab, np.array([0., 0., 0., 1.]), rcond=None)
show("A_b_pi", np.round(pib, 8).tolist(), "pi_1 = 0 exactly")
show("A_b_pi_frac", [str(F(x).limit_denominator(10**5)) for x in pib])
show("A_b_r_50_row1", np.round(np.linalg.matrix_power(Pb, 50)[0], 8).tolist())

# --- A5. gotcha figure, panel (c): two recurrent classes {1} and {3,4}, 2 transient
Pc = np.array([[1.0, 0.0, 0.0, 0.0],
               [0.3, 0.4, 0.3, 0.0],
               [0.0, 0.0, 0.5, 0.5],
               [0.0, 0.0, 0.5, 0.5]])
assert np.allclose(Pc.sum(1), 1)
Pc200 = np.linalg.matrix_power(Pc, 200)
show("A_c_r_row1", np.round(Pc200[0], 8).tolist(), "start in 1")
show("A_c_r_row2", np.round(Pc200[1], 8).tolist(), "start in 2: 1/2 - 1/4 - 1/4")
show("A_c_r_row3", np.round(Pc200[2], 8).tolist(), "start in 3")
show("A_c_r21_limit", round(float(Pc200[1, 0]), 8))

# ======================================================================
# PART B — rec16 Problem 1 (continuous RVs)
# ======================================================================
print()
print("=" * 72)
print("B. rec16 PROBLEM 1")
print("=" * 72)

c_const = F(1, 3)
show("B1a_c", str(c_const))
show("B1a_c_dec", round(float(c_const), 6))
show("B1a_area_check", str(2 * c_const * 1 + c_const * 1))

EX = F(1, 3) * (3**2 - 2**2) + F(1, 6) * (4**2 - 3**2)
EX2 = F(2, 9) * (3**3 - 2**3) + F(1, 9) * (4**3 - 3**3)
show("B1a_EX", str(EX), "= 17/6")
show("B1a_EX_dec", round(float(EX), 6))
show("B1a_EX_term1", str(F(1, 3) * 5))
show("B1a_EX_term2", str(F(1, 6) * 7))
show("B1a_EX2", str(EX2), "= 25/3")
show("B1a_EX2_dec", round(float(EX2), 6))
show("B1a_EX2_term1", str(F(2, 9) * 19))
show("B1a_EX2_term2", str(F(1, 9) * 37))
varX = EX2 - EX**2
show("B1a_varX", str(varX))
show("B1a_varX_dec", round(float(varX), 6))
show("B1a_sdX_dec", round(math.sqrt(float(varX)), 6))
# numeric cross-check of the moments by quadrature
xs = np.linspace(2, 4, 2_000_001)
fx = np.where(xs < 3, 2 / 3, 1 / 3)
show("B1a_quad_norm", round(float(np.trapezoid(fx, xs)), 6))
show("B1a_quad_EX", round(float(np.trapezoid(xs * fx, xs)), 6))
show("B1a_quad_EX2", round(float(np.trapezoid(xs**2 * fx, xs)), 6))

# Y = 2X+1
show("B1a_Y_range", [5, 9])
show("B1a_fY_left", str(c_const), "height on 5<=y<=7 equals c=1/3")
show("B1a_fY_right", str(c_const / 2), "height on 7<=y<=9 equals c/2=1/6")
show("B1a_fY_area", str(F(1, 3) * 2 + F(1, 6) * 2))
show("B1a_EY", str(2 * EX + 1))
show("B1a_EY_dec", round(float(2 * EX + 1), 6))
show("B1a_varY", str(4 * varX))
show("B1a_varY_dec", round(float(4 * varX), 6))

# (b) P(X <= W)
c1 = F(2, 3) * F(1, 2)
c2 = F(1, 3) * F(1, 2)
show("B1b_c1", str(c1))
show("B1b_c2", str(c2))
area_trap = F(3, 2)      # {2<=x<=3, x<=w<=4}
area_tri = F(1, 2)       # {3<=x<=4, x<=w<=4}
show("B1b_area_trapezoid", str(area_trap))
show("B1b_area_triangle", str(area_tri))
PXW = c1 * area_trap + c2 * area_tri
show("B1b_P_XleW", str(PXW), "= 7/12")
show("B1b_P_XleW_dec", round(float(PXW), 6))
show("B1b_term1", str(c1 * area_trap))
show("B1b_term2", str(c2 * area_tri))
# Monte Carlo cross-check
n_mc = 4_000_000
u = rng.random(n_mc)
Xs = np.where(u < 2 / 3, 2 + u * 3 / 2, 3 + (u - 2 / 3) * 3)
Ws = rng.uniform(2, 4, n_mc)
show("B1b_MC_P_XleW", round(float(np.mean(Xs <= Ws)), 5))
show("B1b_MC_EX", round(float(np.mean(Xs)), 5))

# (c) posterior of W given T = 3
show("B1c_joint_height", 10 * 0.5, "f_W(w) f_{T|W}(3|w) = (1/2)(10) = 5")
show("B1c_w_range", [2.9, 3.0])
show("B1c_fT3", 5 * 0.1)
show("B1c_posterior_height", round(5 / 0.5, 6), "uniform on [2.9,3]")
show("B1c_posterior_mean", 2.95)

# (d) normal tail
mu_N, var_N = 1 / 60, 4 / 3600
sd_N = math.sqrt(var_N)
z = (5 / 60 - mu_N) / sd_N
Phi2 = 0.5 * (1 + math.erf(z / math.sqrt(2)))
show("B1d_sd", round(sd_N, 8), "= 2/60")
show("B1d_z", round(z, 8))
show("B1d_Phi_z_exact", round(Phi2, 7))
show("B1d_tail_exact", round(1 - Phi2, 7))
show("B1d_tail_table", round(1 - 0.9772, 6), "with the 4-digit table value 0.9772")
show("B1d_source_misprint", 0.0028)

# (e) S = 24/W
show("B1e_S_range", [6, 12])
ss = np.linspace(6, 12, 1_200_001)
fs = 12 / ss**2
show("B1e_fS_norm", round(float(np.trapezoid(fs, ss)), 8))
show("B1e_ES", round(float(12 * math.log(2)), 6), "= 12 ln 2")
show("B1e_ES_quad", round(float(np.trapezoid(ss * fs, ss)), 6))
show("B1e_E24overW_via_W", round(float(np.trapezoid(24 / np.linspace(2, 4, 1_200_001) * 0.5,
                                                    np.linspace(2, 4, 1_200_001))), 6))
show("B1e_fS_at_6", round(12 / 36, 6))
show("B1e_fS_at_12", round(12 / 144, 6))
show("B1e_CDF_at_8", round(2 - 12 / 8, 6))

# ======================================================================
# PART C — rec16 Problem 2 (random sums of normals)
# ======================================================================
print()
print("=" * 72)
print("C. rec16 PROBLEM 2")
print("=" * 72)

p_geo = 0.4
show("C_p", p_geo)
show("C_EN", round(1 / p_geo, 6))
show("C_varN", round((1 - p_geo) / p_geo**2, 6))
show("C_EN2", round((1 - p_geo) / p_geo**2 + 1 / p_geo**2, 6))
show("C_mu_a", round(1 / p_geo, 6), "E[A] = E[N] E[A_i] = 1/p")
show("C_sigma2_a_terms", [round(1 / p_geo, 6), round((1 - p_geo) / p_geo**2, 6)])
show("C_sigma2_a", round(1 / p_geo + (1 - p_geo) / p_geo**2, 6), "= 1/p^2")
show("C_sigma2_a_closed", round(1 / p_geo**2, 6))
show("C_c_ab", round((2 - p_geo) / p_geo**2, 6), "= E[N^2]")
show("C_cov_ab", round((2 - p_geo) / p_geo**2 - (1 / p_geo) ** 2, 6), "= var(N)")
show("C_corr_ab", round(((2 - p_geo) / p_geo**2 - 1 / p_geo**2) / (1 / p_geo**2), 6))
# Monte Carlo cross-check of mean/var/E[AB]
n_mc2 = 1_000_000
Nsim = rng.geometric(p_geo, n_mc2)
Asim = rng.normal(Nsim * 1.0, np.sqrt(Nsim * 1.0))
Bsim = rng.normal(Nsim * 1.0, np.sqrt(Nsim * 1.0))
show("C_MC_EA", round(float(Asim.mean()), 4))
show("C_MC_varA", round(float(Asim.var()), 4))
show("C_MC_EAB", round(float((Asim * Bsim).mean()), 4))

# (b) two-point N
w1, w2 = F(1, 3), F(2, 3)
show("C_b_weights", [str(w1), str(w2)])
show("C_b_components", ["Normal(1,1)", "Normal(2,2)"])


def f_mix(a):
    return (1 / 3) * math.exp(-(a - 1) ** 2 / 2) / math.sqrt(2 * math.pi) \
        + (2 / 3) * math.exp(-(a - 2) ** 2 / 4) / math.sqrt(4 * math.pi)


def post_N1(a):
    num = (1 / 3) * math.exp(-(a - 1) ** 2 / 2) / math.sqrt(2 * math.pi)
    return num / f_mix(a)


aa = np.linspace(-8, 12, 2_000_001)
fm = np.array([(1 / 3) * np.exp(-(aa - 1) ** 2 / 2) / np.sqrt(2 * np.pi)
               + (2 / 3) * np.exp(-(aa - 2) ** 2 / 4) / np.sqrt(4 * np.pi)]).ravel()
show("C_b_mix_norm", round(float(np.trapezoid(fm, aa)), 8))
show("C_b_EA", round(float(np.trapezoid(aa * fm, aa)), 6), "= (1/3)(1)+(2/3)(2)")
show("C_b_EA_closed", round(1 / 3 + 4 / 3, 6))
show("C_b_EA2_closed", round((1 / 3) * (1 + 1) + (2 / 3) * (2 + 4), 6))
show("C_b_varA_closed", round((1 / 3) * 2 + (2 / 3) * 6 - (5 / 3) ** 2, 6))
_lo, _hi = 1.0, 3.0
for _ in range(200):
    _mid = (_lo + _hi) / 2
    if post_N1(_mid) > 1 / 3:
        _lo = _mid
    else:
        _hi = _mid
show("C_b_post_crosses_prior_at", round(_lo, 4), "posterior = prior = 1/3")

for a0 in (0.0, 1.0, 1.5, 2.0, 4.0):
    show(f"C_b_post_N1_at_{a0}", round(post_N1(a0), 6))
    show(f"C_b_fA_at_{a0}", round(f_mix(a0), 6))

# ======================================================================
# PART D — rec17 Problem 1 (Iwana Passe)
# ======================================================================
print()
print("=" * 72)
print("D. rec17 PROBLEM 1")
print("=" * 72)

lam_c, lam_s, T_min, pc, ps = 1.5, 0.5, 4.0, 0.6, 0.3
show("D_params", dict(lam_c=lam_c, lam_s=lam_s, T=T_min, p_c=pc, p_s=ps))
mu_c = lam_c * T_min
show("D_a_mean_count", mu_c)
for k in (0, 1, 2, 3, 5, 6, 10):
    show(f"D_a_pK_{k}", round(mu_c**k * math.exp(-mu_c) / math.factorial(k), 6))
# Poisson with integer mean is doubly maximized at mu-1 and mu: check the tie explicitly.
show(
    "D_a_pK_mode_tie",
    round(mu_c**5 * math.exp(-mu_c) / math.factorial(5), 9)
    == round(mu_c**6 * math.exp(-mu_c) / math.factorial(6), 9),
)
_terms, _t = [], math.exp(-mu_c)
for k in range(0, 200):
    _terms.append(_t)
    _t *= mu_c / (k + 1)
show("D_a_pK_sum_check", round(sum(_terms), 8))
show("D_b_i", round(lam_c / (lam_c + lam_s), 6))
show("D_b_ii", round(lam_c / (lam_c + lam_s) * pc, 6))
show("D_b_correct_overall", round(lam_c / (lam_c + lam_s) * pc
                                  + lam_s / (lam_c + lam_s) * ps, 6))
r_, s_ = 3, 2
show("D_c_joint_r3_s2", round((lam_c * T_min) ** r_ * math.exp(-lam_c * T_min) / math.factorial(r_)
                              * (lam_s * T_min) ** s_ * math.exp(-lam_s * T_min) / math.factorial(s_), 6))
show("D_c_marginal_r3", round((lam_c * T_min) ** 3 * math.exp(-lam_c * T_min) / 6, 6))
show("D_c_marginal_s2", round((lam_s * T_min) ** 2 * math.exp(-lam_s * T_min) / 2, 6))

# (d) hypoexponential density
xs2 = np.linspace(0, 60, 3_000_001)
fX_hypo = lam_s * lam_c / (lam_s - lam_c) * (np.exp(-lam_c * xs2) - np.exp(-lam_s * xs2))
show("D_d_norm", round(float(np.trapezoid(fX_hypo, xs2)), 6))
show("D_d_mean_quad", round(float(np.trapezoid(xs2 * fX_hypo, xs2)), 6))
show("D_d_mean_closed", round(1 / lam_s + 1 / lam_c, 6))
show("D_d_var_closed", round(1 / lam_s**2 + 1 / lam_c**2, 6))
show("D_d_mode", round(math.log(lam_s / lam_c) / (lam_s - lam_c), 6))
show("D_d_f_at_1", round(float(lam_s * lam_c / (lam_s - lam_c)
                               * (math.exp(-lam_c) - math.exp(-lam_s))), 6))
# Monte Carlo cross-check
n_mc3 = 8_000_000
Xd = rng.exponential(1 / lam_s, n_mc3) + rng.exponential(1 / lam_c, n_mc3)
show("D_d_MC_mean", round(float(Xd.mean()), 4))
show("D_d_MC_P_le_2", round(float(np.mean(Xd <= 2)), 5))
cdf2 = 1 - (lam_s * math.exp(-lam_c * 2) - lam_c * math.exp(-lam_s * 2)) / (lam_s - lam_c)
show("D_d_closed_P_le_2", round(cdf2, 5))

# ======================================================================
# PART E — rec17 Problem 2 (Shem) and Problem 3 (random incidence)
# ======================================================================
print()
print("=" * 72)
print("E. rec17 PROBLEMS 2 AND 3")
print("=" * 72)

lam_sh, p_acc, mu_radio = 6.0, 0.2, 3.0
show("E_params", dict(lam=lam_sh, p=p_acc, mu=mu_radio))
show("E_a_EN", round(1 / p_acc, 6))
show("E_a_varN", round((1 - p_acc) / p_acc**2, 6))
for n in (1, 2, 5):
    show(f"E_a_pN_{n}", round((1 - p_acc) ** (n - 1) * p_acc, 6))
lam_eff = p_acc * lam_sh
show("E_b_thinned_rate", round(lam_eff, 6))
show("E_b_mean_gap", round(1 / lam_eff, 6))
show("E_b_fQ_at_0", round(lam_eff, 6))
show("E_b_P_Q_gt_1", round(math.exp(-lam_eff), 6))
show("E_c_mean_2hr", round(2 * lam_eff, 6))
for m in (0, 1, 2, 3):
    show(f"E_c_pM_{m}", round(math.exp(-2 * lam_eff) * (2 * lam_eff) ** m / math.factorial(m), 6))
q_radio = mu_radio / (mu_radio + lam_eff)
show("E_d_q", round(q_radio, 6))
for k in (0, 1, 2, 3):
    show(f"E_d_pK_{k}", round((1 - q_radio) ** k * q_radio, 6))
show("E_d_EK", round((1 - q_radio) / q_radio, 6), "= p*lambda/mu")
show("E_d_EK_check", round(lam_eff / mu_radio, 6))
show("E_e_EW", round(2 / mu_radio, 6))
show("E_e_varW", round(2 / mu_radio**2, 6))
show("E_e_fW_mode", round(1 / mu_radio, 6))
ww = np.linspace(0, 30, 3_000_001)
fW = mu_radio**2 * ww * np.exp(-mu_radio * ww)
show("E_e_norm", round(float(np.trapezoid(fW, ww)), 6))
show("E_e_mean_quad", round(float(np.trapezoid(ww * fW, ww)), 6))

# Monte Carlo: random incidence in the radio-call (Poisson) process
horizon, n_rep = 4000.0, 1
gaps = rng.exponential(1 / mu_radio, int(horizon * mu_radio * 1.4))
times = np.cumsum(gaps)
tobs = rng.uniform(times[10], times[-10], 500_000)
idx = np.searchsorted(times, tobs)
Wobs = times[idx] - times[idx - 1]
show("E_e_MC_meanW", round(float(Wobs.mean()), 4), "vs 2/mu")
show("E_e_MC_mean_ordinary_gap", round(float(gaps.mean()), 4), "vs 1/mu")

# Problem 3: Erlang-2 interarrivals, rate lambda
lam3 = 1.0
show("E3_lambda", lam3)
show("E3_interarrival_mean", round(2 / lam3, 6))
show("E3_interarrival_var", round(2 / lam3**2, 6))
show("E3_observed_mean", round(3 / lam3, 6), "Erlang order 3")
show("E3_observed_var", round(3 / lam3**2, 6))
ll = np.linspace(0, 60, 3_000_001)
f2 = lam3**2 * ll * np.exp(-lam3 * ll)
f3 = lam3**3 * ll**2 * np.exp(-lam3 * ll) / 2
show("E3_f2_norm", round(float(np.trapezoid(f2, ll)), 6))
show("E3_f3_norm", round(float(np.trapezoid(f3, ll)), 6))
show("E3_lengthbias_check", round(float(np.trapezoid(np.abs(f3 - ll * f2 / (2 / lam3)), ll)), 8),
     "|f3 - l f2 / E[L]| integrates to 0")
show("E3_f3_mode", round(2 / lam3, 6))
show("E3_ratio_means", round(3 / 2, 6))
# Monte Carlo random incidence in the Erlang-2 process
g2 = rng.exponential(1 / lam3, 400_000) + rng.exponential(1 / lam3, 400_000)
t2 = np.cumsum(g2)
tob2 = rng.uniform(t2[10], t2[-10], 500_000)
i2 = np.searchsorted(t2, tob2)
Lobs = t2[i2] - t2[i2 - 1]
show("E3_MC_observed_mean", round(float(Lobs.mean()), 4))
show("E3_MC_observed_var", round(float(Lobs.var()), 4))
show("E3_MC_ordinary_mean", round(float(g2.mean()), 4))

# ======================================================================
# PART F — practice-question numbers
# ======================================================================
print()
print("=" * 72)
print("F. PRACTICE QUESTIONS")
print("=" * 72)

# F1: three questions on one 3-state chain
Pf = np.array([[0.4, 0.6, 0.0],
               [0.2, 0.5, 0.3],
               [0.0, 0.4, 0.6]])
assert np.allclose(Pf.sum(1), 1)
show("F1_P", Pf.tolist())
show("F1_r13_2", round(float(np.linalg.matrix_power(Pf, 2)[0, 2]), 6))
Af = np.vstack([Pf.T - np.eye(3), np.ones(3)])
pif, *_ = np.linalg.lstsq(Af, np.array([0., 0., 0., 1.]), rcond=None)
show("F1_pi", np.round(pif, 6).tolist())
show("F1_pi_frac", [str(F(x).limit_denominator(10**5)) for x in pif])
show("F1_r_100", np.round(np.linalg.matrix_power(Pf, 100)[0], 6).tolist())
show("F1_t_star_3", round(1 / pif[2], 6))

# F2: absorption practice — gambler-style chain on {0,1,2,3}, 0 and 3 absorbing, p=0.6 up
pu = 0.6
Pg = np.array([[1, 0, 0, 0],
               [1 - pu, 0, pu, 0],
               [0, 1 - pu, 0, pu],
               [0, 0, 0, 1]], dtype=float)
Tg = Pg[1:3, 1:3]
cg = Pg[1:3, 3]
ag = np.linalg.solve(np.eye(2) - Tg, cg)
show("F2_absorb_win", np.round(ag, 6).tolist())
show("F2_absorb_win_frac", [str(F(x).limit_denominator(10**5)) for x in ag])
mug = np.linalg.solve(np.eye(2) - Tg, np.ones(2))
show("F2_mu", np.round(mug, 6).tolist())
show("F2_mu_frac", [str(F(x).limit_denominator(10**5)) for x in mug])

# F3: birth-death load factor practice
p_bd, q_bd = 0.2, 0.3
rho = p_bd / q_bd
show("F3_rho", round(rho, 6))
show("F3_pi0", round(1 - rho, 6))
show("F3_EX", round(rho / (1 - rho), 6))
show("F3_pi_3", round((1 - rho) * rho**3, 6))

# F4: rec16-style practice — piecewise PDF with heights 3c, c
# f(x) = 3k on [0,1], k on [1,3]  ->  3k + 2k = 1 -> k = 1/5
k_p = F(1, 5)
show("F4_k", str(k_p))
EXp = F(3, 5) * F(1, 2) + F(1, 5) * (F(3**2 - 1**2, 2))
show("F4_EX", str(EXp))
show("F4_EX_dec", round(float(EXp), 6))
EX2p = F(3, 5) * F(1, 3) + F(1, 5) * F(3**3 - 1**3, 3)
show("F4_EX2", str(EX2p))
show("F4_varX", str(EX2p - EXp**2))
show("F4_varX_dec", round(float(EX2p - EXp**2), 6))

# F5: rec17-style practice — split Poisson
lam_p, split = 10.0, 0.25
show("F5_rate_split", round(lam_p * split, 6))
show("F5_P_exactly2_in_0p5", round(math.exp(-lam_p * split * 0.5)
                                   * (lam_p * split * 0.5) ** 2 / 2, 6))
show("F5_P_first_type_A", round(lam_p * split / lam_p, 6))
show("F5_E_gap", round(1 / (lam_p * split), 6))

# F6: deterministic 4-cycle (Practice 5.4) — periodic with d = 4
Pcyc = np.roll(np.eye(4), 1, axis=1)
show("F6_r11_n4", float(np.linalg.matrix_power(Pcyc, 4)[0, 0]))
show("F6_r11_n5", float(np.linalg.matrix_power(Pcyc, 5)[0, 0]))
Ac = np.vstack([Pcyc.T - np.eye(4), np.ones(4)])
pic, *_ = np.linalg.lstsq(Ac, np.array([0., 0., 0., 0., 1.]), rcond=None)
show("F6_pi", np.round(pic, 8).tolist())

# F7: V = W^2 with W ~ U[2,4] (Practice 5.7)
vv = np.linspace(4, 16, 1_200_001)
fv = 1 / (4 * np.sqrt(vv))
show("F7_norm", round(float(np.trapezoid(fv, vv)), 6))
show("F7_EV_quad", round(float(np.trapezoid(vv * fv, vv)), 6))
show("F7_EV_closed", round((4**3 - 2**3) / 3 / 2, 6), "E[W^2] = 28/3")

with open("computes/g5_s5.json", "w", encoding="utf-8") as fh:
    json.dump(R, fh, indent=1, default=str)
print()
print(f"wrote computes/g5_s5.json with {len(R)} entries")
