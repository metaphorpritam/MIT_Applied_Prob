# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy"]
# ///
"""All numbers for G7 section 2 — Maximum likelihood estimation.

Sources: L23 slides 3-5 (ML review), L24 slide 2 (review of ML), rec23 P1/P2
(uniform [0,theta]; normal mean+variance), rec24 P1 (blackbody photon counting)
and rec24 P2 (least squares as ML).  B&T Sections 9.1 (Examples 9.1-9.4) and 9.2.

Every numeric value that appears in notes/src/fragments/g7_s2.html is produced here.
Run:  uv run computes/g7_s2.py
"""
from __future__ import annotations

import io
import json
import math
import sys

import numpy as np
from scipy import optimize, stats

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

R: dict = {}


def put(k, v):
    R[k] = v
    return v


def head(t):
    print()
    print("=" * 74)
    print(t)
    print("=" * 74)


# =====================================================================
# A.  Bernoulli / binomial ML  (B&T Example 9.2; L23 slide 3 pattern)
# =====================================================================
head("A. Bernoulli ML: n = 10 tosses, k = 7 heads")

n_A, k_A = 10, 7
put("bern_n", n_A)
put("bern_k", k_A)
theta_hat_A = k_A / n_A
put("bern_hat", theta_hat_A)
print(f"theta_hat = k/n = {k_A}/{n_A} = {theta_hat_A}")

# likelihood and log-likelihood at a few candidate thetas
grid_A = [0.3, 0.5, 0.6, 0.7, 0.8, 0.9]
lik_A, loglik_A = {}, {}
for t in grid_A:
    L = t ** k_A * (1 - t) ** (n_A - k_A)          # likelihood of the SEQUENCE
    lik_A[f"{t}"] = L
    loglik_A[f"{t}"] = math.log(L)
    print(f"  theta = {t:.1f}:  L = {L:.8f}   log L = {math.log(L):.6f}")
put("bern_lik", lik_A)
put("bern_loglik", loglik_A)
put("bern_lik_max", theta_hat_A ** k_A * (1 - theta_hat_A) ** (n_A - k_A))
print(f"  max value L(0.7) = {R['bern_lik_max']:.8f}")

# the likelihood is NOT a density in theta: its integral over theta
from scipy.integrate import quad  # noqa: E402

area_A, _ = quad(lambda t: t ** k_A * (1 - t) ** (n_A - k_A), 0, 1)
put("bern_lik_area", area_A)
# 1/(area) = (n+1) choose ... : Beta(k+1, n-k+1) = k!(n-k)!/(n+1)!
exact_area = math.factorial(k_A) * math.factorial(n_A - k_A) / math.factorial(n_A + 1)
put("bern_lik_area_exact", exact_area)
print(f"  integral over theta in [0,1] = {area_A:.10f}  (exact B(8,4) = {exact_area:.10f})")
print("  -> NOT 1, so the likelihood is not a density in theta")

# same statement for the COUNT model (binomial pmf), which is what Fig 2.1 plots
comb_A = math.comb(n_A, k_A)
put("bern_comb", comb_A)
binom_lik = {}
for t in grid_A:
    binom_lik[f"{t}"] = comb_A * t ** k_A * (1 - t) ** (n_A - k_A)
put("bern_binom_lik", binom_lik)
put("bern_binom_lik_max", comb_A * theta_hat_A ** k_A * (1 - theta_hat_A) ** (n_A - k_A))
put("bern_binom_area", comb_A * exact_area)
put("bern_binom_area_frac", 1 / (n_A + 1))
print(f"  count model: C(10,7) = {comb_A}, L(0.7) = {R['bern_binom_lik_max']:.6f}, "
      f"area over theta = {comb_A*exact_area:.10f} = 1/{n_A+1} = {1/(n_A+1):.10f}")

# sum over the DATA at fixed theta is 1 (it IS a PMF in the data)
for t in (0.3, 0.7):
    s = sum(t ** k * (1 - t) ** (n_A - k) for k in range(n_A + 1) for _ in [0])
    # careful: sum over sequences, i.e. over all 2^n outcomes -> use binomial weights
    s = sum(math.comb(n_A, k) * t ** k * (1 - t) ** (n_A - k) for k in range(n_A + 1))
    print(f"  sum over all 2^{n_A} data sequences at theta={t}: {s:.12f}")
    put(f"bern_datasum_{t}", s)

# polling ML point estimate (rec23 P3 data, ML part only; CI lives in section 1)
put("poll_n", 1200)
put("poll_k", 684)
put("poll_hat", 684 / 1200)
print(f"polling: theta_hat = 684/1200 = {684/1200}")

# =====================================================================
# B.  Exponential ML  (L23 slide 3; B&T Example 9.3)
# =====================================================================
head("B. Exponential ML")

x_B = [0.42, 1.31, 0.08, 2.05, 0.64]
put("exp_data", x_B)
sB = sum(x_B)
put("exp_sum", sB)
put("exp_n", len(x_B))
put("exp_mean", sB / len(x_B))
put("exp_hat", len(x_B) / sB)
print(f"data {x_B}, sum = {sB}, mean = {sB/len(x_B)}, theta_hat = n/sum = {len(x_B)/sB:.6f}")

# =====================================================================
# C.  Normal ML: mean and variance  (rec23 P2 = B&T Example 9.4)
# =====================================================================
head("C. Normal ML on a concrete sample")

rng = np.random.default_rng(20101207)          # rec24 date as seed
mu_true, v_true = 5.0, 4.0
x_C = np.round(rng.normal(mu_true, math.sqrt(v_true), 10), 2)
x_C = np.array([4.62, 6.28, 3.31, 7.05, 5.44, 2.87, 5.91, 4.03, 6.77, 3.52])  # frozen
put("norm_data", [float(v) for v in x_C])
n_C = len(x_C)
put("norm_n", n_C)
m_C = float(x_C.mean())
put("norm_mhat", m_C)
put("norm_sum", float(x_C.sum()))
dev = x_C - m_C
put("norm_devs", [round(float(d), 4) for d in dev])
ss = float((dev ** 2).sum())
put("norm_ss", ss)
v_ml = ss / n_C
put("norm_vhat_ml", v_ml)
v_unb = ss / (n_C - 1)
put("norm_vhat_unb", v_unb)
put("norm_sd_ml", math.sqrt(v_ml))
print(f"data      = {list(x_C)}")
print(f"sum       = {x_C.sum():.2f}")
print(f"m_n       = {m_C:.4f}")
print(f"sum sq dev= {ss:.4f}")
print(f"v_ML  = ss/n     = {v_ml:.4f}   (sd {math.sqrt(v_ml):.4f})")
print(f"v_unb = ss/(n-1) = {v_unb:.4f}")
print(f"ratio v_ML / v_unb = (n-1)/n = {(n_C-1)/n_C}")

# log-likelihood check: the ML pair really maximizes it
def loglik_norm(mu, v, x=x_C):
    n = len(x)
    return -n / 2 * math.log(2 * math.pi) - n / 2 * math.log(v) - float(((x - mu) ** 2).sum()) / (2 * v)


put("norm_loglik_at_ml", loglik_norm(m_C, v_ml))
put("norm_loglik_at_unb", loglik_norm(m_C, v_unb))
put("norm_loglik_at_true", loglik_norm(mu_true, v_true))
print(f"log L(m_n, v_ML)  = {loglik_norm(m_C, v_ml):.6f}   <- maximum")
print(f"log L(m_n, v_unb) = {loglik_norm(m_C, v_unb):.6f}")
print(f"log L(5, 4)       = {loglik_norm(mu_true, v_true):.6f}")
opt = optimize.minimize(lambda p: -loglik_norm(p[0], math.exp(p[1])), [0.0, 0.0])
put("norm_numeric_argmax", [float(opt.x[0]), float(math.exp(opt.x[1]))])
print(f"numeric argmax  = ({opt.x[0]:.6f}, {math.exp(opt.x[1]):.6f})  (matches)")

# the identity  sum (x_i-mu)^2 = n s_n^2 + n (m_n - mu)^2  at mu = 4
mu_chk = 4.0
lhs = float(((x_C - mu_chk) ** 2).sum())
rhs = ss + n_C * (m_C - mu_chk) ** 2
put("norm_ident_lhs", lhs)
put("norm_ident_rhs", rhs)
print(f"identity check at mu=4: LHS {lhs:.4f} = RHS {rhs:.4f}")

# bias of the ML variance: E[S_n^2] = (n-1)/n v
bias_tab = {}
for n in (2, 5, 10, 100, 1000):
    bias_tab[str(n)] = {"factor": (n - 1) / n, "E_at_v4": 4 * (n - 1) / n, "bias_at_v4": -4 / n}
    print(f"  n={n:5d}: E[S_n^2] = {(n-1)/n:.4f} v ; at v=4 -> {4*(n-1)/n:.4f}, bias {-4/n:+.4f}")
put("norm_bias_table", bias_tab)

# Monte-Carlo confirmation of the bias
M = 400_000
rng2 = np.random.default_rng(9041)
samp = rng2.normal(mu_true, math.sqrt(v_true), size=(M, 5))
s2 = ((samp - samp.mean(axis=1, keepdims=True)) ** 2).sum(axis=1) / 5
put("norm_bias_mc_n5", float(s2.mean()))
put("norm_bias_mc_n5_target", 4 * 4 / 5)
print(f"Monte Carlo n=5: mean of S_n^2 = {s2.mean():.4f}  (theory {4*4/5:.4f})")

# =====================================================================
# D.  Uniform [0, theta] ML  (rec23 P1 = B&T Example 9.1)
# =====================================================================
head("D. Uniform [0, theta] ML")

x_D = [3.1, 7.4, 2.2, 6.9, 5.3]
put("unif_data", x_D)
put("unif_n", len(x_D))
put("unif_hat", max(x_D))
print(f"data {x_D} -> theta_hat = max = {max(x_D)}")
for t in (7.0, 7.4, 8.0, 10.0):
    L = 0.0 if t < max(x_D) else t ** (-len(x_D))
    print(f"  L({t}) = {L:.3e}")
    put(f"unif_L_{t}", L)

unif_tab = {}
for n in (1, 2, 5, 10, 50, 100):
    e = n / (n + 1)
    var = n / ((n + 1) ** 2 * (n + 2))
    mse = 2 / ((n + 1) * (n + 2))
    unif_tab[str(n)] = {"E_over_theta": e, "bias_over_theta": e - 1,
                        "var_over_theta2": var, "mse_over_theta2": mse}
    print(f"  n={n:4d}: E[max]/theta = {e:.6f}  bias/theta = {e-1:+.6f} "
          f" var/theta^2 = {var:.3e}  MSE/theta^2 = {mse:.3e}")
put("unif_moment_table", unif_tab)
put("unif_corrected_factor_n5", 6 / 5)
print("bias-corrected estimator ((n+1)/n)*max : at n=5 the factor is 6/5 = 1.2, "
      f"estimate {1.2*max(x_D):.3f}")
put("unif_corrected_est_n5", 1.2 * max(x_D))

# Monte Carlo check of E[max] at n=5, theta=8
rng3 = np.random.default_rng(4141)
mx = rng3.uniform(0, 8, size=(400_000, 5)).max(axis=1)
put("unif_mc_n5_theta8", float(mx.mean()))
put("unif_mc_n5_theta8_target", 8 * 5 / 6)
print(f"Monte Carlo E[max] (n=5, theta=8) = {mx.mean():.4f}  (theory {8*5/6:.4f})")

# derivative of L is never zero: dL/dtheta = -n theta^{-(n+1)} at theta = 7.4, n = 5
put("unif_dL", -5 * max(x_D) ** (-6))
print(f"dL/dtheta at theta = max = {-5*max(x_D)**(-6):.3e}  (never zero)")

# =====================================================================
# E.  rec24 Problem 1 — blackbody photon counting
# =====================================================================
head("E. rec24 P1 — blackbody photon counting")


def Z(th):
    return 1.0 / (1.0 - math.exp(-1.0 / th))


def muK(th):
    return 1.0 / (math.exp(1.0 / th) - 1.0)


def varK(th):
    return muK(th) ** 2 + muK(th)


for th in (1.0, 5.0, 100.0):
    p = 1 - math.exp(-1 / th)
    m, v = muK(th), varK(th)
    v2 = (1 - p) / p ** 2
    print(f"  theta={th:6.1f}: Z={Z(th):10.4f}  p={p:.6f}  mu_K={m:10.4f}  "
          f"var_K={v:12.4f}  (1-p)/p^2={v2:12.4f}  sd={math.sqrt(v):9.4f}")
    put(f"photon_theta_{th}", {"Z": Z(th), "p": p, "mu": m, "var": v, "var_alt": v2,
                               "sd": math.sqrt(v)})

# numerically confirm the PMF normalizes and its mean/variance at theta = 100
th0 = 100.0
ks = np.arange(0, 400_000)
pmf = np.exp(-ks / th0) / Z(th0)
put("photon_pmf_sum_th100", float(pmf.sum()))
put("photon_pmf_mean_th100", float((ks * pmf).sum()))
put("photon_pmf_var_th100", float((ks ** 2 * pmf).sum() - ((ks * pmf).sum()) ** 2))
print(f"  numeric at theta=100: sum p = {pmf.sum():.10f}, mean = {(ks*pmf).sum():.6f} "
      f"(formula {muK(th0):.6f}), var = {(ks**2*pmf).sum() - ((ks*pmf).sum())**2:.4f} "
      f"(formula {varK(th0):.4f})")

# exact ML estimator: theta_hat = 1 / log(1 + 1/s_n)
def theta_exact(s):
    return 1.0 / math.log(1.0 + 1.0 / s)


sn_vals = [0.5, 2.0, 10.0, 99.5, 250.0]
ml_tab = {}
for s in sn_vals:
    te = theta_exact(s)
    ml_tab[str(s)] = {"exact": te, "approx": s, "rel_err_pct": 100 * (s - te) / te}
    print(f"  s_n={s:8.2f}: exact theta_hat = {te:12.6f}   hot-body approx = {s:8.2f}"
          f"   relative error {100*(s-te)/te:+7.4f}%")
put("photon_ml_table", ml_tab)

# consistency: with theta = 100 the sample mean converges to mu_K(100) = 99.5008...
put("photon_muK_100", muK(100.0))
put("photon_theta_exact_from_muK100", theta_exact(muK(100.0)))
print(f"  sanity: theta_exact(mu_K(100)) = {theta_exact(muK(100.0)):.10f}  (must be 100)")

# a simulated data set of n = 12 counts at theta = 100
rng4 = np.random.default_rng(1207)
p100 = 1 - math.exp(-1 / 100)
counts = rng4.geometric(p100, size=12) - 1          # shifted geometric on {0,1,2,...}
counts = np.array([53, 132, 8, 214, 61, 97, 19, 156, 44, 88, 3, 121])   # frozen
put("photon_counts", [int(c) for c in counts])
s_n = float(counts.mean())
put("photon_sn", s_n)
put("photon_hat_exact", theta_exact(s_n))
put("photon_hat_approx", s_n)
print(f"  sample of 12 counts {list(counts)}: sum = {counts.sum()}, s_n = {s_n:.6f}")
print(f"    exact ML theta_hat = {theta_exact(s_n):.6f}, hot-body approx = {s_n:.6f}")

# verify by direct numerical maximization of the log-likelihood
def loglik_photon(th, k=counts):
    return len(k) * math.log(1 - math.exp(-1 / th)) - k.sum() / th


br = optimize.minimize_scalar(lambda t: -loglik_photon(t), bracket=(50, 90, 200))
put("photon_numeric_argmax", float(br.x))
print(f"  numerical argmax of log-likelihood = {br.x:.6f}  (matches exact formula)")
put("photon_loglik_at_hat", loglik_photon(theta_exact(s_n)))
for t in (60.0, 80.0, theta_exact(s_n), 120.0, 160.0):
    print(f"    log L({t:9.4f}) = {loglik_photon(t):.6f}")

# (d) sample size from the noise-to-signal ratio
mu_d = muK(100.0)
root = 100 * math.sqrt(1 + 1 / mu_d)
put("photon_d_muK", mu_d)
put("photon_d_sqrt_n", root)
put("photon_d_n_exact", root ** 2)
put("photon_d_n_ceiling", math.ceil(root ** 2))
put("photon_d_n_limit", 10000)
print(f"(d) mu_K(100) = {mu_d:.6f}; sqrt(n) > 100 sqrt(1 + 1/mu_K) = {root:.6f}")
print(f"    n > {root**2:.4f}  ->  n = {math.ceil(root**2)}; in the limit mu_K>>1, n = 10000")
put("photon_d_factor", math.sqrt(1 + 1 / mu_d))
for m in (1, 10, 99.5008, 1000):
    print(f"    mu_K = {m:10.4f}: n_min = {10000*(1+1/m):12.2f}")
    put(f"photon_d_n_mu_{m}", 10000 * (1 + 1 / m))

# (e) 95% confidence interval
z = float(stats.norm.ppf(0.975))
put("photon_z", z)
put("photon_z_rounded", 1.96)
put("photon_e_halfwidth_coeff", 1.96 * 0.01)
put("photon_e_halfwidth_at_mu", 1.96 * 0.01 * mu_d)
print(f"(e) z_{{0.975}} = {z:.6f} ~ 1.96; half width = 1.96 * 0.01 * mu_K "
      f"= {1.96*0.01:.4f} mu_K = {1.96*0.01*mu_d:.6f} at mu_K = {mu_d:.4f}")
put("photon_e_sigma_Khat", 0.01 * mu_d)
put("photon_e_Phi_1p96", float(stats.norm.cdf(1.96)))
print(f"    Phi(1.96) = {stats.norm.cdf(1.96):.6f}, 2*Phi(1.96)-1 = "
      f"{2*stats.norm.cdf(1.96)-1:.6f}")
put("photon_e_coverage", float(2 * stats.norm.cdf(1.96) - 1))

# =====================================================================
# F.  rec24 Problem 2 — least squares as ML
# =====================================================================
head("F. rec24 P2 — linear and quadratic ML fits")

xs = np.array([0.8, 2.5, 5.0, 7.3, 9.1])
ys = np.array([-2.3, 20.9, 103.5, 215.8, 334.0])
put("reg_x", [float(v) for v in xs])
put("reg_y", [float(v) for v in ys])
n_F = len(xs)
xbar = float(xs.mean())
ybar = float(ys.mean())
put("reg_n", n_F)
put("reg_xbar", xbar)
put("reg_ybar", ybar)
put("reg_xsum", float(xs.sum()))
put("reg_ysum", float(ys.sum()))
print(f"sum x = {xs.sum()}, xbar = {xbar}")
print(f"sum y = {ys.sum()}, ybar = {ybar}")

dx = xs - xbar
dy = ys - ybar
put("reg_dx", [round(float(v), 4) for v in dx])
put("reg_dy", [round(float(v), 4) for v in dy])
Sxy = float((dx * dy).sum())
Sxx = float((dx * dx).sum())
put("reg_Sxy", Sxy)
put("reg_Sxx", Sxx)
th1 = Sxy / Sxx
th0 = ybar - th1 * xbar
put("reg_th1", th1)
put("reg_th0", th0)
print("  per-point products (x_i-xbar)(y_i-ybar):",
      [round(float(a * b), 4) for a, b in zip(dx, dy)])
print("  per-point squares  (x_i-xbar)^2      :", [round(float(a * a), 4) for a in dx])
print(f"  Sxy = {Sxy:.4f}, Sxx = {Sxx:.4f}")
print(f"  theta1_hat = {th1:.6f} (rounded {round(th1,2)}), "
      f"theta0_hat = {th0:.6f} (rounded {round(th0,2)})")
put("reg_th1_r", round(th1, 2))
put("reg_th0_r", round(th0, 2))

# quadratic model in u = x^2
us = xs ** 2
ubar = float(us.mean())
put("reg_u", [float(v) for v in us])
put("reg_ubar", ubar)
du = us - ubar
Suy = float((du * dy).sum())
Suu = float((du * du).sum())
put("reg_Suy", Suy)
put("reg_Suu", Suu)
b1 = Suy / Suu
b0 = ybar - b1 * ubar
put("reg_b1", b1)
put("reg_b0", b0)
put("reg_b1_r", round(b1, 2))
put("reg_b0_r", round(b0, 2))
print(f"  u = x^2 = {list(us)}, ubar = {ubar}")
print(f"  Suy = {Suy:.4f}, Suu = {Suu:.4f}")
print(f"  beta1_hat = {b1:.6f} (rounded {round(b1,2)}), "
      f"beta0_hat = {b0:.6f} (rounded {round(b0,2)})")

# residuals and ML noise variances
res1 = ys - (th0 + th1 * xs)
res2 = ys - (b0 + b1 * us)
put("reg_res_lin", [round(float(v), 4) for v in res1])
put("reg_res_quad", [round(float(v), 4) for v in res2])
put("reg_SSE_lin", float((res1 ** 2).sum()))
put("reg_SSE_quad", float((res2 ** 2).sum()))
put("reg_sigma2_lin_ml", float((res1 ** 2).sum()) / n_F)
put("reg_sigma2_quad_ml", float((res2 ** 2).sum()) / n_F)
print(f"  linear residuals    {[round(float(v),3) for v in res1]}  SSE = {(res1**2).sum():.4f}")
print(f"  quadratic residuals {[round(float(v),3) for v in res2]}  SSE = {(res2**2).sum():.4f}")
print(f"  ML sigma^2: linear {(res1**2).sum()/n_F:.4f}, quadratic {(res2**2).sum()/n_F:.4f}")
put("reg_SSE_ratio", float((res1 ** 2).sum() / (res2 ** 2).sum()))
# R^2 for each
sst = float((dy ** 2).sum())
put("reg_SST", sst)
put("reg_R2_lin", 1 - float((res1 ** 2).sum()) / sst)
put("reg_R2_quad", 1 - float((res2 ** 2).sum()) / sst)
print(f"  SST = {sst:.4f}, R^2 linear = {1-(res1**2).sum()/sst:.6f}, "
      f"R^2 quadratic = {1-(res2**2).sum()/sst:.6f}")

# cross-check with numpy polyfit / lstsq
put("reg_np_lin", [float(v) for v in np.polyfit(xs, ys, 1)])
A = np.vstack([np.ones(n_F), us]).T
sol, *_ = np.linalg.lstsq(A, ys, rcond=None)
put("reg_np_quad", [float(v) for v in sol])
print(f"  numpy polyfit linear: slope {np.polyfit(xs,ys,1)[0]:.6f}, "
      f"intercept {np.polyfit(xs,ys,1)[1]:.6f}")
print(f"  numpy lstsq quadratic: b0 {sol[0]:.6f}, b1 {sol[1]:.6f}")
# source rounding check
print(f"  source prints (40.53, -65.86) and (4.09, -3.07); "
      f"we get ({round(th1,2)}, {round(th0,2)}) and ({round(b1,2)}, {round(b0,2)})")
put("reg_source_check_lin", [40.53, -65.86])
put("reg_source_check_quad", [4.09, -3.07])
put("reg_b0_source_note", 134.38 - 4.09 * 33.60)

# =====================================================================
# G.  Practice-question numbers
# =====================================================================
head("G. Practice questions")

# Practice 2.1 — Poisson ML
pois = [3, 1, 4, 0, 2, 5, 2, 3]
put("prac_pois_data", pois)
put("prac_pois_n", len(pois))
put("prac_pois_sum", sum(pois))
put("prac_pois_hat", sum(pois) / len(pois))
print(f"P2.1 Poisson data {pois}: sum {sum(pois)}, n {len(pois)}, "
      f"lambda_hat = {sum(pois)/len(pois)}")
put("prac_pois_invariance", math.exp(-sum(pois) / len(pois)))
print(f"     invariance: ML of P(X=0) = e^{{-lambda_hat}} = {math.exp(-sum(pois)/len(pois)):.6f}")
put("prac_pois_naive", sum(1 for v in pois if v == 0) / len(pois))
print(f"     empirical fraction of zeros = {sum(1 for v in pois if v==0)/len(pois):.4f}")

# Practice 2.2 — normal with KNOWN mean 0, unknown variance
y22 = [1.2, -0.4, 2.1, -1.7, 0.9]
put("prac_var_data", y22)
put("prac_var_n", len(y22))
put("prac_var_sumsq", sum(v * v for v in y22))
put("prac_var_hat", sum(v * v for v in y22) / len(y22))
print(f"P2.2 known-mean-0 normal, data {y22}: sum sq = {sum(v*v for v in y22):.4f}, "
      f"v_hat = {sum(v*v for v in y22)/len(y22):.4f}")

# Practice 2.3 — uniform [theta, theta+1]
u23 = [4.30, 4.95, 4.62, 5.10, 4.41]
put("prac_u_data", u23)
put("prac_u_lo", max(u23) - 1)
put("prac_u_hi", min(u23))
print(f"P2.3 uniform [theta, theta+1], data {u23}: any theta in "
      f"[{max(u23)-1:.2f}, {min(u23):.2f}] maximizes; width "
      f"{min(u23)-(max(u23)-1):.2f}")
put("prac_u_width", min(u23) - (max(u23) - 1))

# Practice 2.4 — exact vs approximate photon ML at a cool body
put("prac_photon_sn", 3.0)
put("prac_photon_exact", theta_exact(3.0))
put("prac_photon_relerr", 100 * (3.0 - theta_exact(3.0)) / theta_exact(3.0))
print(f"P2.4 s_n = 3: exact theta_hat = {theta_exact(3.0):.6f}, approx 3, "
      f"relative error {100*(3-theta_exact(3.0))/theta_exact(3.0):.3f}%")
put("prac_photon_muK_at_exact", muK(theta_exact(3.0)))

# Practice 2.5 — regression through the origin, ML of theta in Y = theta x + W
put("prac_org_num", float((xs * ys).sum()))
put("prac_org_den", float((xs * xs).sum()))
put("prac_org_hat", float((xs * ys).sum() / (xs * xs).sum()))
print(f"P2.5 no-intercept fit on rec24 data: sum x y = {(xs*ys).sum():.4f}, "
      f"sum x^2 = {(xs*xs).sum():.4f}, theta_hat = {(xs*ys).sum()/(xs*xs).sum():.6f}")
res_org = ys - (xs * ys).sum() / (xs * xs).sum() * xs
put("prac_org_SSE", float((res_org ** 2).sum()))
print(f"     SSE = {(res_org**2).sum():.4f} (vs {(res1**2).sum():.4f} with an intercept)")

# =====================================================================
# H.  Widget parity — 'Likelihood explorer'
#     Reproduces exactly the JS LCG used in w-g7s2-mle.
# =====================================================================
head("H. Widget parity (LCG-matched samples)")


class LCG:
    """seed = (seed*1103515245 + 12345) & 0x7fffffff ;  u = seed / 0x7fffffff.

    The widget must do this multiply with Math.imul (product mod 2^32) — a plain
    `sd * 1103515245` reaches ~2.4e18, past 2^53, so the double is rounded and
    the low bits are lost before the mask, and the JS stream then diverges from
    this exact-integer one after two draws.
    """

    def __init__(self, seed):
        self.s = seed & 0x7FFFFFFF

    def u(self):
        self.s = (self.s * 1103515245 + 12345) & 0x7FFFFFFF
        return self.s / 0x7FFFFFFF


def gen(model, n, seed, p=0.65, mu=2.0, sd=1.0, thmax=3.0):
    r = LCG(seed)
    out = []
    if model == "bern":
        for _ in range(n):
            out.append(1.0 if r.u() < p else 0.0)
    elif model == "norm":
        for _ in range(n):
            a, b = r.u(), r.u()
            z = math.sqrt(-2 * math.log(a + 1e-12)) * math.cos(2 * math.pi * b)
            out.append(mu + sd * z)
    else:  # uniform [0, thmax]
        for _ in range(n):
            out.append(thmax * r.u())
    return out


parity = {}
for model, n, seed in [("bern", 20, 12345), ("bern", 200, 12345),
                       ("norm", 20, 12345), ("norm", 200, 12345),
                       ("unif", 20, 12345), ("unif", 200, 12345)]:
    d = gen(model, n, seed)
    if model == "bern":
        hat = sum(d) / n
        extra = {"heads": int(sum(d))}
    elif model == "norm":
        m = sum(d) / n
        hat = m
        extra = {"v_hat": sum((v - m) ** 2 for v in d) / n}
    else:
        hat = max(d)
        extra = {}
    parity[f"{model}_{n}"] = {"hat": hat, **extra}
    print(f"  {model:5s} n={n:4d} seed=12345 -> hat = {hat:.6f}  {extra}")
put("widget_parity", parity)

# the log-likelihood value at the ML point for the parity samples (Bernoulli n=20)
d = gen("bern", 20, 12345)
k = int(sum(d))
put("widget_bern20_k", k)
put("widget_bern20_loglik_hat", k * math.log(k / 20) + (20 - k) * math.log(1 - k / 20))
put("widget_bern20_loglik_true", k * math.log(0.65) + (20 - k) * math.log(0.35))
print(f"  Bernoulli n=20: k = {k}, log L(hat) = {R['widget_bern20_loglik_hat']:.6f}, "
      f"log L(0.65) = {R['widget_bern20_loglik_true']:.6f}")

# =====================================================================
# I.  Remaining prose numbers used verbatim in the fragment
# =====================================================================
head("I. Remaining prose numbers")

# Practice 2.1 — single Poisson observation k = 3
for t in (1.0, 3.0, 5.0):
    L = math.exp(-t) * t ** 3 / 6
    put(f"p21_L_{t}", L)
    print(f"P2.1 L({t}) = e^-{t} * {t}^3/6 = {math.exp(-t):.6f} * {t**3/6:.6f} = {L:.6f}")
put("p21_exp1", math.exp(-1))
put("p21_exp3", math.exp(-3))
put("p21_exp5", math.exp(-5))
put("p21_125over6", 125 / 6)
put("p21_27over6", 27 / 6)
# the Poisson likelihood in theta DOES integrate to 1 (Gamma identity) — say so honestly
area21, _ = quad(lambda t: math.exp(-t) * t ** 3 / 6, 0, 200)
put("p21_area", area21)
print(f"     integral over theta of e^-theta theta^3/6 = {area21:.10f}  (Gamma(4)/3! = 1 exactly)")
# reparametrize psi = sqrt(theta): L*(psi) = e^{-psi^2} psi^6 / 6, no Jacobian (likelihood!)
area21b, _ = quad(lambda ps: math.exp(-ps * ps) * ps ** 6 / 6, 0, 40)
put("p21_area_reparam", area21b)
put("p21_gamma72_half", math.gamma(3.5) / 2)
print(f"     after psi = sqrt(theta): integral of e^-psi^2 psi^6/6 = {area21b:.10f} "
      f"(= Gamma(7/2)/12 = {math.gamma(3.5)/12:.10f}) -> NOT 1")

# Bernoulli likelihood ratio 0.7 vs 0.3
put("bern_ratio_07_03", R["bern_lik"]["0.7"] / R["bern_lik"]["0.3"])
print(f"Bernoulli L(0.7)/L(0.3) = {R['bern_lik']['0.7']/R['bern_lik']['0.3']:.4f}")

# Practice 2.2 — posterior mean (k+1)/(n+2) with flat prior, n=10 k=7
put("p22_post_mean", 8 / 12)
print(f"P2.2 (k+1)/(n+2) = 8/12 = {8/12:.6f}")

# rec24 P1(d) — 10101 one-second intervals in hours
put("photon_d_hours", 10101 / 3600)
print(f"rec24 P1d: 10101 s = {10101/3600:.4f} hours")

# rec24 P2 — intermediate products and the SSE ratio
put("reg_th1_times_xbar", th1 * xbar)
put("reg_b1_times_ubar", b1 * ubar)
put("reg_sse_factor", float((res1 ** 2).sum() / (res2 ** 2).sum()))
print(f"rec24 P2: th1*xbar = {th1*xbar:.6f}, b1*ubar = {b1*ubar:.6f}, "
      f"SSE ratio = {(res1**2).sum()/(res2**2).sum():.4f}")

# Practice 2.4 — the individual squares
put("p24_squares", [round(v * v, 4) for v in y22])
print(f"P2.4 squares = {[round(v*v,4) for v in y22]}")

# Practice 2.6 — MSE of max vs of the bias-corrected estimator, n = 5
n26 = 5
mse_ml = 2 / ((n26 + 1) * (n26 + 2))
var_max = n26 / ((n26 + 1) ** 2 * (n26 + 2))
mse_corr = ((n26 + 1) / n26) ** 2 * var_max
put("p26_mse_ml", mse_ml)
put("p26_var_max", var_max)
put("p26_mse_corr", mse_corr)
put("p26_ratio", mse_corr / mse_ml)
print(f"P2.6 MSE(max)/theta^2 = 2/42 = {mse_ml:.6f} (=1/21); "
      f"MSE(corrected)/theta^2 = {mse_corr:.6f} (=1/35); ratio {mse_corr/mse_ml:.4f}")

# Practice 2.7 — the log used
put("p27_log", math.log(1 + 1 / 3))
print(f"P2.7 log(4/3) = {math.log(1+1/3):.6f}, 1/that = {1/math.log(1+1/3):.6f}")

# Practice 2.10 — invariance for the exponential
th_exp = R["exp_hat"]
put("p210_tau", 1 / th_exp)
put("p210_pgt1", math.exp(-th_exp))
put("p210_empirical", sum(1 for v in x_B if v > 1) / len(x_B))
print(f"P2.10 tau_hat = 1/{th_exp:.6f} = {1/th_exp:.6f}; "
      f"P(X>1)_hat = e^-{th_exp:.6f} = {math.exp(-th_exp):.6f}; "
      f"empirical fraction = {sum(1 for v in x_B if v>1)/len(x_B):.4f}")

# =====================================================================
head("Writing JSON")
with open("computes/g7_s2.json", "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1, default=float)
print(f"wrote computes/g7_s2.json with {len(R)} keys")
