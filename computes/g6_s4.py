# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Numbers for G6 section 4 - LMS and linear LMS estimation (L22 + rec22 estimation parts).

Every numeric value that appears in notes/src/fragments/g6_s4.html is produced here.
Closed forms are cross-checked against numerical quadrature and Monte-Carlo simulation.

Run:  uv run computes/g6_s4.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
from scipy import integrate

ROOT = Path(__file__).resolve().parent.parent
OUT: dict[str, float] = {}
rng = np.random.default_rng(20221122)


def rec(key, val, note=""):
    v = float(val)
    OUT[key] = v
    print(f"{key:34s} = {v:.10g}   {note}")
    return v


def head(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


# ===========================================================================
head("A.  L22 slides 2-3, 5  -  Theta ~ U[4,10],  X = Theta + W,  W ~ U[-1,1]")
# ===========================================================================
# prior height, conditional height, joint height
rec("L22_prior_h", F(1, 6), "f_Theta(theta) = 1/6 on [4,10]  (slide figure)")
rec("L22_cond_h", F(1, 2), "f_{X|Theta}(x|theta) = 1/2 on [theta-1,theta+1]")
rec("L22_joint_h", F(1, 12), "f_{Theta,X} = (1/6)(1/2) on the parallelogram")
rec("L22_prior_mean", 7.0, "E[Theta] = (4+10)/2")
rec("L22_prior_var", F(6 ** 2, 12), "var(Theta) = (10-4)^2/12 = 3")
rec("L22_W_var", F(2 ** 2, 12), "var(W) = (1-(-1))^2/12 = 1/3")


def fX(x):
    """Marginal density of X, from the three regions of the parallelogram."""
    if 3.0 <= x < 5.0:
        return (x - 3.0) / 12.0
    if 5.0 <= x <= 9.0:
        return 1.0 / 6.0
    if 9.0 < x <= 11.0:
        return (11.0 - x) / 12.0
    return 0.0


def lms(x):
    """E[Theta | X = x] : midpoint of the vertical slice."""
    if 3.0 <= x < 5.0:
        return (4.0 + x + 1.0) / 2.0          # slice = [4, x+1]
    if 5.0 <= x <= 9.0:
        return x                              # slice = [x-1, x+1]
    if 9.0 < x <= 11.0:
        return (x - 1.0 + 10.0) / 2.0         # slice = [x-1, 10]
    return float("nan")


def cvar(x):
    """var(Theta | X = x) = (slice length)^2 / 12."""
    if 3.0 <= x < 5.0:
        return (x - 3.0) ** 2 / 12.0
    if 5.0 <= x <= 9.0:
        return 4.0 / 12.0
    if 9.0 < x <= 11.0:
        return (11.0 - x) ** 2 / 12.0
    return float("nan")


# marginal density checkpoints quoted in the text
rec("L22_fX_4", fX(4.0), "f_X(4)  = (4-3)/12 = 1/12")
rec("L22_fX_7", fX(7.0), "f_X(7)  = 1/6")
rec("L22_fX_10", fX(10.0), "f_X(10) = (11-10)/12 = 1/12")
rec("L22_fX_total", integrate.quad(fX, 3, 11, limit=200)[0], "integrates to 1 (check)")

rec("L22_lms_3p5", lms(3.5), "E[Theta|X=3.5] = (3.5+5)/2")
rec("L22_lms_4", lms(4.0), "E[Theta|X=4]   = 4.5")
rec("L22_lms_7", lms(7.0), "E[Theta|X=7]   = 7")
rec("L22_lms_10", lms(10.0), "E[Theta|X=10]  = (10+9)/2")
rec("L22_cvar_mid", 1.0 / 3.0, "var(Theta|X=x) = 1/3 for 5<=x<=9")
rec("L22_cvar_3p5", cvar(3.5), "var(Theta|X=3.5) = (0.5)^2/12")
rec("L22_naive_mse_3p5", cvar(3.5) + (lms(3.5) - 3.5) ** 2,
    "cond. mse of the naive estimate 3.5 = var + (4.25-3.5)^2")
rec("L22_lin_at_3p5", 0.9 * 3.5 + 0.7, "best line at x=3.5")
rec("L22_cvar_4", cvar(4.0), "var(Theta|X=4) = 1/12")
rec("L22_cvar_10", cvar(10.0), "var(Theta|X=10) = 1/12")

# overall LMS mean squared error  E[var(Theta|X)]
mid = integrate.quad(lambda x: cvar(x) * fX(x), 5, 9)[0]
left = integrate.quad(lambda x: cvar(x) * fX(x), 3, 5)[0]
right = integrate.quad(lambda x: cvar(x) * fX(x), 9, 11)[0]
rec("L22_mse_mid", mid, "middle band contributes 4/18 = 2/9")
rec("L22_mse_edge", left, "each edge band contributes 1/36")
mse_lms = mid + left + right
rec("L22_mse_lms", mse_lms, "E[var(Theta|X)] = 2/9 + 2/36 = 5/18")
rec("L22_mse_lms_exact", F(5, 18), "closed form 5/18")
rec("L22_var_hat", 3.0 - mse_lms, "var(Theta_hat) = var(Theta) - var(error) = 49/18")

# linear LMS for the same model
EX = 7.0
varX = 3.0 + 1.0 / 3.0
covTX = 3.0        # cov(Theta, Theta + W) = var(Theta) since W independent
a_lin = covTX / varX
b_lin = 7.0 - a_lin * EX
rho2 = covTX ** 2 / (varX * 3.0)
mse_lin = (1 - rho2) * 3.0
rec("L22_EX", EX, "E[X] = E[Theta] + E[W] = 7 + 0")
rec("L22_varX", varX, "var(X) = var(Theta) + var(W) = 3 + 1/3 = 10/3")
rec("L22_cov", covTX, "cov(Theta,X) = var(Theta) = 3")
rec("L22_a", a_lin, "a = cov/var(X) = 3/(10/3) = 9/10")
rec("L22_b", b_lin, "b = E[Theta] - a E[X] = 7 - 6.3 = 0.7")
rec("L22_rho2", rho2, "rho^2 = 9/10")
rec("L22_rho", np.sqrt(rho2), "rho = sqrt(0.9)")
rec("L22_mse_lin", mse_lin, "(1-rho^2)var(Theta) = 0.1*3 = 0.3")
rec("L22_mse_gap", mse_lin - mse_lms, "0.3 - 5/18 = 1/45")
rec("L22_lin_at_4", a_lin * 4 + b_lin, "line at x=4  (vs LMS 4.5)")
rec("L22_lin_at_7", a_lin * 7 + b_lin, "line at x=7  (vs LMS 7)")
rec("L22_lin_at_10", a_lin * 10 + b_lin, "line at x=10 (vs LMS 9.5)")

# Monte-Carlo check
N = 4_000_000
th = rng.uniform(4, 10, N)
xs = th + rng.uniform(-1, 1, N)
est = np.array([lms(v) for v in xs[:400_000]])
rec("L22_mse_lms_mc", np.mean((th[:400_000] - est) ** 2), "simulated LMS mse")
rec("L22_mse_lin_mc", np.mean((th - (a_lin * xs + b_lin)) ** 2), "simulated linear-LMS mse")
rec("L22_varX_mc", np.var(xs), "simulated var(X)")
rec("L22_cov_mc", np.cov(th, xs)[0, 1], "simulated cov(Theta,X)")

# ===========================================================================
head("B.  rec22 P1 / B&T Examples 8.2, 8.7, 8.12, 8.15 - Romeo and Juliet")
# ===========================================================================
# Theta ~ U[0,1];  X | Theta = t  ~  U[0,t]
rec("RJ_prior_mean", 0.5, "E[Theta] = 1/2")
rec("RJ_prior_var", F(1, 12), "var(Theta) = 1/12")
rec("RJ_EX", 0.25, "E[X] = E[Theta/2] = 1/4")
rec("RJ_ETheta2", F(1, 3), "E[Theta^2] = 1/12 + 1/4 = 1/3")
rec("RJ_EvarXgT", F(1, 36), "E[var(X|Theta)] = E[Theta^2/12] = 1/36")
rec("RJ_varEXgT", F(1, 48), "var(E[X|Theta]) = var(Theta/2) = 1/48")
rec("RJ_varX", F(7, 144), "var(X) = 1/36 + 1/48 = 7/144")
rec("RJ_EThetaX", F(1, 6), "E[Theta X] = E[Theta^2/2] = 1/6")
rec("RJ_cov", F(1, 24), "cov = 1/6 - (1/2)(1/4) = 1/24")
a_rj = float(F(1, 24) / F(7, 144))
b_rj = 0.5 - a_rj * 0.25
rec("RJ_a", a_rj, "a = (1/24)/(7/144) = 6/7")
rec("RJ_b", b_rj, "b = 1/2 - (6/7)(1/4) = 2/7")
rho2_rj = float(F(1, 24) ** 2 / (F(1, 12) * F(7, 144)))
rec("RJ_rho2", rho2_rj, "rho^2 = 3/7")
rec("RJ_rho", np.sqrt(rho2_rj), "rho = sqrt(3/7)")
mse_lin_rj = (1 - rho2_rj) * (1 / 12)
rec("RJ_mse_lin", mse_lin_rj, "(1-3/7)(1/12) = 1/21")
rec("RJ_mse_lin_exact", F(1, 21), "closed form 1/21")


def map_est(x):
    return x


def lms_rj(x):
    return (1 - x) / abs(np.log(x))


def E2_rj(x):
    return (1 - x ** 2) / (2 * abs(np.log(x)))


def cmse(x, that):
    return that ** 2 - 2 * that * lms_rj(x) + E2_rj(x)


for xv in (0.1, 0.25, 0.5, 0.75, 0.9):
    tag = str(xv).replace(".", "")
    rec(f"RJ_lms_x{tag}", lms_rj(xv), f"E[Theta|X={xv}]")
    rec(f"RJ_lin_x{tag}", a_rj * xv + b_rj, f"linear LMS at x={xv}")
    rec(f"RJ_cmse_map_x{tag}", cmse(xv, map_est(xv)), f"cond. mse of MAP at x={xv}")
    rec(f"RJ_cmse_lms_x{tag}", cmse(xv, lms_rj(xv)), f"cond. mse of LMS at x={xv}")
    rec(f"RJ_cmse_lin_x{tag}", cmse(xv, a_rj * xv + b_rj), f"cond. mse of lin LMS at x={xv}")

rec("RJ_lin_at_1", a_rj * 1.0 + b_rj, "linear LMS at x=1 -> 8/7 > 1, outside [0,1]")
rec("RJ_lin_infeasible_x", (1.0 - b_rj) / a_rj, "x beyond which the line exceeds 1")

# unconditional mean squared errors
fX_rj = lambda x: -np.log(x)      # marginal of X on (0,1)
rec("RJ_fX_check", integrate.quad(fX_rj, 0, 1)[0], "marginal integrates to 1")
mse_lms_rj = integrate.quad(lambda x: cmse(x, lms_rj(x)) * fX_rj(x), 0, 1, limit=400)[0]
rec("RJ_mse_lms", mse_lms_rj, "E[var(Theta|X)] by quadrature")
rec("RJ_mse_lms_closed", 1 / 3 - np.log(4 / 3), "closed form 1/3 - ln(4/3)")
rec("RJ_log43", np.log(4 / 3), "ln(4/3)")
mse_map_rj = integrate.quad(lambda x: cmse(x, x) * fX_rj(x), 0, 1, limit=400)[0]
rec("RJ_mse_map", mse_map_rj, "E[(Theta-X)^2] by quadrature")
rec("RJ_mse_map_closed", 1 / 9, "closed form 1/9")
mse_lin_q = integrate.quad(lambda x: cmse(x, a_rj * x + b_rj) * fX_rj(x), 0, 1, limit=400)[0]
rec("RJ_mse_lin_quad", mse_lin_q, "linear-LMS mse by quadrature (should be 1/21)")

# Monte-Carlo
M = 4_000_000
tt = rng.uniform(0, 1, M)
xx = rng.uniform(0, 1, M) * tt
rec("RJ_EX_mc", xx.mean(), "simulated E[X]")
rec("RJ_varX_mc", xx.var(), "simulated var(X)")
rec("RJ_cov_mc", np.cov(tt, xx)[0, 1], "simulated cov")
rec("RJ_mse_map_mc", np.mean((tt - xx) ** 2), "simulated MAP mse")
rec("RJ_mse_lms_mc", np.mean((tt - (1 - xx) / np.abs(np.log(xx))) ** 2), "simulated LMS mse")
rec("RJ_mse_lin_mc", np.mean((tt - (a_rj * xx + b_rj)) ** 2), "simulated linear-LMS mse")

# multiple observations, part (b): posterior normalizing constant for n observations
for n in (1, 2, 5):
    xb = 0.4
    c = 1.0 / integrate.quad(lambda t: t ** (-n), xb, 1)[0]
    rec(f"RJ_c_n{n}_xbar04", c, f"normalizer c(xbar) for n={n}, xbar=0.4")
    m = integrate.quad(lambda t: t * c * t ** (-n), xb, 1)[0]
    rec(f"RJ_lmsn_n{n}_xbar04", m, f"E[Theta | max = 0.4], n={n}")

# ===========================================================================
head("C.  Linear LMS with many observations:  X_i = Theta + W_i")
# ===========================================================================
mu, s0 = 5.0, 2.0
sig = [1.0, 2.0, 3.0]            # sd of W_1, W_2, W_3
obs = [6.0, 4.0, 9.0]
prec = 1.0 / s0 ** 2 + sum(1.0 / s ** 2 for s in sig)
num = mu / s0 ** 2 + sum(o / s ** 2 for o, s in zip(obs, sig))
rec("MO_prec", prec, "sum_{i=0..n} 1/sigma_i^2")
rec("MO_num", num, "mu/sigma_0^2 + sum x_i/sigma_i^2")
rec("MO_est", num / prec, "linear LMS estimate")
rec("MO_mse", 1.0 / prec, "mse = 1/(sum of precisions)")
for i, s in enumerate(sig, start=1):
    rec(f"MO_w{i}", (1.0 / s ** 2) / prec, f"weight on x_{i}")
rec("MO_w0", (1.0 / s0 ** 2) / prec, "weight on the prior mean mu")

# brute-force check by solving the normal equations numerically
n = 3
Sig = np.diag([s ** 2 for s in sig]) + s0 ** 2 * np.ones((n, n))   # cov(X)
c = s0 ** 2 * np.ones(n)                                           # cov(Theta, X_i)
a_vec = np.linalg.solve(Sig, c)
b_sc = mu - a_vec @ (mu * np.ones(n))
rec("MO_est_check", a_vec @ np.array(obs) + b_sc, "same estimate from normal equations")
rec("MO_mse_check", s0 ** 2 - c @ a_vec, "same mse from var(Theta) - c'Sigma^{-1}c")

# ===========================================================================
head("D.  Slide 9: does it matter whether you feed X or X^3 to a linear estimator?")
# ===========================================================================
sig_n2 = 0.01
EX2, EX4, EX6 = 1 / 3, 1 / 5, 1 / 7     # X ~ U[-1,1]
varTh = EX6 + sig_n2
covX = EX4 - 0.0                        # cov(X^3 + N, X) = E[X^4]
covX3 = EX6                             # cov(X^3 + N, X^3) = var(X^3)
mse_X = varTh - covX ** 2 / EX2
mse_X3 = varTh - covX3 ** 2 / EX6
rec("CUBE_varTheta", varTh, "var(Theta) = E[X^6] + sigma^2 = 1/7 + 0.01")
rec("CUBE_cov_X", covX, "cov(Theta,X) = E[X^4] = 1/5")
rec("CUBE_cov_X3", covX3, "cov(Theta,X^3) = 1/7")
rec("CUBE_mse_linX", mse_X, "linear in X")
rec("CUBE_mse_linX3", mse_X3, "linear in X^3 = sigma^2, exact")
rec("CUBE_a_X", covX / EX2, "a = (1/5)/(1/3) = 3/5")
rec("CUBE_a_X3", covX3 / EX6, "a = 1 for the X^3 regressor")

# ===========================================================================
head("E.  Widget grid:  X ~ U[c-1,c+1],  Theta = X^2 + sigma*N")
# ===========================================================================
def widget(c, s):
    varX_ = 1 / 3
    EX_ = c
    ETh = c ** 2 + 1 / 3
    cov_ = (2 / 3) * c
    EX4_ = c ** 4 + 2 * c ** 2 + 1 / 5
    varTh_ = EX4_ - (c ** 2 + 1 / 3) ** 2 + s ** 2
    a_ = cov_ / varX_
    b_ = ETh - a_ * EX_
    r2 = cov_ ** 2 / (varX_ * varTh_)
    return a_, b_, varTh_, r2, s ** 2, varTh_ - cov_ ** 2 / varX_


for (c, s) in [(0.0, 0.20), (0.5, 0.20), (1.0, 0.20), (1.0, 0.60), (2.0, 0.20)]:
    a_, b_, vT, r2, m_lms, m_lin = widget(c, s)
    tag = f"c{str(c).replace('.', '')}_s{str(s).replace('.', '')}"
    rec(f"WID_{tag}_a", a_, f"a = 2c   (c={c}, sigma={s})")
    rec(f"WID_{tag}_b", b_, "b = 1/3 - c^2")
    rec(f"WID_{tag}_rho2", r2, "rho^2")
    rec(f"WID_{tag}_mseLMS", m_lms, "LMS mse = sigma^2")
    rec(f"WID_{tag}_mseLIN", m_lin, "linear mse = sigma^2 + 4/45")
rec("WID_gap", 4 / 45, "linear-LMS penalty 4/45, independent of c and sigma")

# Monte-Carlo check of the widget claim
for (c, s) in [(0.0, 0.20), (1.0, 0.20), (2.0, 0.60)]:
    K = 2_000_000
    xw = rng.uniform(c - 1, c + 1, K)
    thw = xw ** 2 + s * rng.standard_normal(K)
    a_, b_, *_ = widget(c, s)
    tag = f"c{str(c).replace('.', '')}_s{str(s).replace('.', '')}"
    rec(f"WID_{tag}_mseLMS_mc", np.mean((thw - xw ** 2) ** 2), "simulated LMS mse")
    rec(f"WID_{tag}_mseLIN_mc", np.mean((thw - (a_ * xw + b_)) ** 2), "simulated linear mse")

# ===========================================================================
head("F.  Practice-question numbers")
# ===========================================================================
# Practice 4.1: Theta ~ exponential(lambda=2) -- best constant and its mse
rec("P41_best_const", 0.5, "E[Theta] = 1/lambda = 1/2")
rec("P41_mse", 0.25, "var(Theta) = 1/lambda^2 = 1/4")
rec("P41_mse_at_1", 0.25 + (1 - 0.5) ** 2, "mse of the estimate 1: var + (1-1/2)^2")

# Practice 4.2: discrete example  Theta in {0,1}, X in {0,1}
pj = np.array([[0.4, 0.1], [0.2, 0.3]])   # rows Theta=0,1; cols X=0,1
pX = pj.sum(axis=0)
post1 = pj[1] / pX
rec("P42_pX0", pX[0], "P(X=0)")
rec("P42_pX1", pX[1], "P(X=1)")
rec("P42_E_given0", post1[0], "E[Theta|X=0] = P(Theta=1|X=0)")
rec("P42_E_given1", post1[1], "E[Theta|X=1]")
mse_opt = sum(pX[k] * post1[k] * (1 - post1[k]) for k in (0, 1))
rec("P42_mse_opt", mse_opt, "E[var(Theta|X)]")
rec("P42_var_prior", pj[1].sum() * (1 - pj[1].sum()), "var(Theta) = p(1-p)")
rec("P42_mse_round", pX[0] * post1[0] + pX[1] * (1 - post1[1]),
    "mse of the rounded (MAP) rule g(0)=0,g(1)=1")

# Practice 4.5: Theta mean 5 var 4, X = Theta + W, var(W) = 1
rec("P45_a", 4 / 5, "a = 4/(4+1)")
rec("P45_b", 5 - (4 / 5) * 5, "b = 5 - 0.8*5 = 1")
rec("P45_rho2", 16 / (5 * 4), "rho^2 = 16/20 = 4/5")
rec("P45_mse", (1 - 16 / 20) * 4, "(1-4/5)*4 = 0.8")
rec("P45_est_at_7", (4 / 5) * 7 + 1, "estimate when x = 7")

# Practice 4.4: uninformative observation
rec("P44_var", 2 / 3, "var(Theta) for Theta uniform on {-1,0,1}")

# ===========================================================================
head("G.  Jointly normal case: E[Theta|X] IS the straight line")
# ===========================================================================
mu_t, sd_t, mu_x, sd_x, rho_g = 2.0, 1.5, 5.0, 2.0, 0.8
a_g = rho_g * sd_t / sd_x
b_g = mu_t - a_g * mu_x
rec("NORM_mu_theta", mu_t, "E[Theta]")
rec("NORM_sd_theta", sd_t, "sigma_Theta")
rec("NORM_mu_x", mu_x, "E[X]")
rec("NORM_sd_x", sd_x, "sigma_X")
rec("NORM_rho", rho_g, "rho")
rec("NORM_cov", rho_g * sd_t * sd_x, "cov = rho sigma_Theta sigma_X")
rec("NORM_a", a_g, "a = rho sigma_Theta/sigma_X = 0.8*1.5/2")
rec("NORM_b", b_g, "b = E[Theta] - a E[X]")
rec("NORM_mse", (1 - rho_g ** 2) * sd_t ** 2, "(1-rho^2)sigma_Theta^2")
rec("NORM_prior_var", sd_t ** 2, "sigma_Theta^2 for comparison")
rec("NORM_est_at_8", a_g * 8 + b_g, "estimate at x = 8")
G = 2_000_000
z1 = rng.standard_normal(G)
z2 = rng.standard_normal(G)
Xg = mu_x + sd_x * z1
Tg = mu_t + sd_t * (rho_g * z1 + np.sqrt(1 - rho_g ** 2) * z2)
rec("NORM_mse_mc", np.mean((Tg - (a_g * Xg + b_g)) ** 2), "simulated mse of the line")
# conditional mean in a thin slice around x = 8: should sit on the line
sel = np.abs(Xg - 8.0) < 0.05
rec("NORM_slice_mean_at_8", Tg[sel].mean(), "empirical E[Theta | X near 8]")
rec("NORM_slice_n", int(sel.sum()), "sample size in that slice")

# ===========================================================================
head("H.  Largest gap between the LMS curve and the best line (Part A model)")
# ===========================================================================
xg = np.linspace(3, 11, 80001)
curve = np.array([lms(v) for v in xg])
liney = a_lin * xg + b_lin
k = int(np.argmax(np.abs(curve - liney)))
rec("L22_maxgap", float(np.abs(curve - liney)[k]), "max |E[Theta|X=x] - (0.9x+0.7)|")
rec("L22_maxgap_at", float(xg[k]), "attained at x =")

out = ROOT / "computes" / "g6_s4.json"
out.write_text(json.dumps(OUT, indent=1, sort_keys=True), encoding="utf-8")
print(f"\nwrote {out}  ({len(OUT)} keys)")
