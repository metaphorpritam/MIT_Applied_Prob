# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Numbers for G7 section 4 - binary hypothesis testing and the likelihood ratio test (L25).

Every numeric value that appears in notes/src/fragments/g7_s4.html is produced here.
Closed forms are cross-checked against exact rational arithmetic, numerical quadrature,
and Monte-Carlo simulation wherever an independent route exists.

Run:  uv run computes/g7_s4.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
from scipy import stats, integrate, optimize

ROOT = Path(__file__).resolve().parent.parent
OUT: dict[str, object] = {}
rng = np.random.default_rng(20101207)

W = 46


def rec(key, val, note=""):
    if isinstance(val, (list, tuple)):
        OUT[key] = [float(v) for v in val]
        print(f"{key:<{W}} {['%.6g' % v for v in val]}   {note}")
    else:
        v = float(val)
        OUT[key] = v
        print(f"{key:<{W}} {v!r:>22}   {note}")
    return val


def head(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


Phi = stats.norm.cdf
Phinv = stats.norm.ppf

# =====================================================================
# 0. standard normal quantiles used throughout
# =====================================================================
head("0. normal quantiles")
z95 = rec("Z_0950", Phinv(0.95), "z_{1-0.05}, one-sided 5%")
z90 = rec("Z_0900", Phinv(0.90), "z_{1-0.10}, one-sided 10%")
z975 = rec("Z_0975", Phinv(0.975), "z_{1-0.025}, two-sided 5%")
z99 = rec("Z_0990", Phinv(0.99), "one-sided 1%")
rec("Z_0950_CHECK_TAIL", 1 - Phi(z95), "must be 0.05")

# =====================================================================
# 1. L25 slide 3 - test on the normal mean, H0: N(0,1) vs H1: N(1,1)
#    LRT reduces to  sum X_i > xi'  with  xi' = log xi + n/2.
#    Under H0 sum ~ N(0,n)  =>  xi' = sqrt(n) z_{1-alpha}.
#    Under H1 sum ~ N(n,n)  =>  beta = Phi(z_{1-alpha} - sqrt(n)).
# =====================================================================
head("1. L25 slide 3 - test on the normal mean (mu=0 vs mu=1)")
for n in (1, 4, 9, 10, 16, 25, 100):
    xip = np.sqrt(n) * z95
    xi = np.exp(xip - n / 2)
    beta = Phi(z95 - np.sqrt(n))
    rec(f"MEAN_n{n}_XIP", xip, f"xi' = sqrt({n})*z95, alpha=0.05")
    rec(f"MEAN_n{n}_XI", xi, "equivalent likelihood-ratio threshold xi")
    rec(f"MEAN_n{n}_BETA", beta, "false acceptance probability")
    rec(f"MEAN_n{n}_POWER", 1 - beta, "power = 1 - beta")
    rec(f"MEAN_n{n}_XBAR", xip / n, "equivalent threshold on the sample mean")

# Monte-Carlo check at n = 10
n = 10
xip10 = np.sqrt(n) * z95
S0 = rng.standard_normal((400_000, n)).sum(axis=1)
S1 = S0 + n  # shifting each of the n coordinates by 1 shifts the sum by n
rec("MEAN_n10_ALPHA_MC", (S0 > xip10).mean(), "MC check of alpha (target 0.05)")
rec("MEAN_n10_BETA_MC", (S1 <= xip10).mean(), "MC check of beta")

# beta if we (wrongly) used a two-sided region of the same alpha
rec("MEAN_n10_TWOSIDED_C", z975 * np.sqrt(10), "two-sided cut |sum|>c, alpha=0.05")
rec("MEAN_n10_TWOSIDED_BETA",
    Phi((z975 * np.sqrt(10) - 10) / np.sqrt(10)) - Phi((-z975 * np.sqrt(10) - 10) / np.sqrt(10)),
    "its beta - strictly worse than the LRT's")

# alpha = 0.01 comparison at n = 10 (the tradeoff)
rec("MEAN_n10_A01_XIP", np.sqrt(10) * z99, "alpha=0.01 threshold")
rec("MEAN_n10_A01_BETA", Phi(z99 - np.sqrt(10)), "alpha=0.01 beta")
rec("MEAN_n10_A10_XIP", np.sqrt(10) * z90, "alpha=0.10 threshold")
rec("MEAN_n10_A10_BETA", Phi(z90 - np.sqrt(10)), "alpha=0.10 beta")

# smallest n making beta <= 0.05 at alpha = 0.05
nn = next(k for k in range(1, 500) if Phi(z95 - np.sqrt(k)) <= 0.05)
rec("MEAN_NMIN_BETA05", nn, "smallest n with beta<=0.05 at alpha=0.05")
rec("MEAN_NMIN_BETA05_BETA", Phi(z95 - np.sqrt(nn)), "its beta")
rec("MEAN_NMIN_EXACT", (z95 + z95) ** 2, "(z_{1-a}+z_{1-b})^2 formula, a=b=0.05")

# =====================================================================
# 2. B&T Example 9.13 - two i.i.d. normals, mean 0 vs mean 2, alpha=0.05
#    LRT: X1+X2 > gamma ; alternative test: max(X1,X2) > zeta
# =====================================================================
head("2. B&T Example 9.13 - LRT vs the max-statistic test (n=2, mu=0 vs 2)")
gam = rec("E913_GAMMA", z95 * np.sqrt(2), "gamma = 1.645*sqrt2 (book: 2.33)")
rec("E913_BETA_LRT", Phi((gam - 4) / np.sqrt(2)), "beta of the LRT (book: 0.12)")
rec("E913_BETA_LRT_ARG", (gam - 4) / np.sqrt(2), "standardized argument (book: -1.18)")
zeta = rec("E913_ZETA", Phinv(np.sqrt(0.95)), "zeta with Phi(zeta)^2 = 0.95 (book: 1.96)")
rec("E913_SQRT095", np.sqrt(0.95), "Phi(zeta) required")
rec("E913_BETA_MAX", Phi(zeta - 2) ** 2, "beta of the max test (book: 0.24)")
rec("E913_BETA_MAX_INNER", Phi(zeta - 2), "P(X1<=zeta; H1)")
# book's rounded arithmetic, reproduced for the [SOURCE CONFLICT] discussion
rec("E913_BOOK_BETA_MAX_ROUND", Phi(1.96 - 2) ** 2, "with the book's zeta=1.96")
# MC check
Z = rng.standard_normal((400_000, 2))
rec("E913_ALPHA_LRT_MC", ((Z.sum(axis=1)) > gam).mean(), "MC alpha of LRT")
rec("E913_BETA_LRT_MC", ((Z + 2).sum(axis=1) <= gam).mean(), "MC beta of LRT")
rec("E913_ALPHA_MAX_MC", (Z.max(axis=1) > zeta).mean(), "MC alpha of max test")
rec("E913_BETA_MAX_MC", ((Z + 2).max(axis=1) <= zeta).mean(), "MC beta of max test")

# =====================================================================
# 3. L25 slide 4 - test on the normal variance, H0: N(0,1) vs H1: N(0,4)
#    LRT reduces to sum X_i^2 > xi' ; under H0 that is chi^2_n.
# =====================================================================
head("3. L25 slide 4 - test on the normal variance (sigma^2 = 1 vs 4)")
for n in (1, 5, 10, 25):
    c = stats.chi2.ppf(0.95, n)
    rec(f"VAR_n{n}_XIP", c, f"chi2_{n} 95th percentile, alpha=0.05")
    # under H1, sum X_i^2 = 4 * (chi2_n)
    rec(f"VAR_n{n}_BETA", stats.chi2.cdf(c / 4.0, n), "beta = P(chi2_n <= xi'/4)")
    rec(f"VAR_n{n}_POWER", 1 - stats.chi2.cdf(c / 4.0, n), "power")
    # xi corresponding to xi': xi' = (8/3)(log xi + n log 2)
    rec(f"VAR_n{n}_XI", np.exp(3.0 * c / 8.0 - n * np.log(2.0)), "equivalent LR threshold xi")
n = 10
c10 = stats.chi2.ppf(0.95, 10)
Q0 = (rng.standard_normal((400_000, 10)) ** 2).sum(axis=1)
Q1 = ((2 * rng.standard_normal((400_000, 10))) ** 2).sum(axis=1)
rec("VAR_n10_ALPHA_MC", (Q0 > c10).mean(), "MC alpha (target 0.05)")
rec("VAR_n10_BETA_MC", (Q1 <= c10).mean(), "MC beta")
rec("VAR_n10_LOG2", np.log(2.0), "log 2, used in the algebra step")
rec("VAR_n10_38", 3.0 / 8.0, "coefficient 1/2 - 1/8 = 3/8")

# =====================================================================
# 4. B&T Example 9.10 - the loaded die, a DISCRETE likelihood ratio
#    H0: p_i = 1/6 ;  H1: p_1 = p_2 = 1/4, p_3..p_6 = 1/8
# =====================================================================
head("4. B&T Example 9.10 - loaded die, discrete LRT")
L_hi = F(1, 4) / F(1, 6)
L_lo = F(1, 8) / F(1, 6)
rec("DIE10_L_HI", float(L_hi), f"L(x) for x in {{1,2}} = {L_hi}")
rec("DIE10_L_LO", float(L_lo), f"L(x) for x in {{3..6}} = {L_lo}")
rec("DIE10_ALPHA_MID", float(F(2, 6)), "alpha when 3/4 < xi < 3/2  (reject on x in {1,2})")
rec("DIE10_BETA_MID", float(F(4, 8)), "beta  when 3/4 < xi < 3/2")
rec("DIE10_ALPHA_LOW", 1.0, "alpha when xi < 3/4 (always reject)")
rec("DIE10_BETA_LOW", 0.0, "beta  when xi < 3/4")
rec("DIE10_ALPHA_HIGH", 0.0, "alpha when xi > 3/2 (never reject)")
rec("DIE10_BETA_HIGH", 1.0, "beta  when xi > 3/2")
rec("DIE10_H1_CHECK", float(2 * F(1, 4) + 4 * F(1, 8)), "H1 pmf sums to 1")
# n = 4 i.i.d. rolls: the LRT depends on K = #rolls landing in {1,2}
head("4b. same die, n = 4 i.i.d. rolls: statistic K = #{rolls in {1,2}}")
n4 = 4
p0, p1 = F(1, 3), F(1, 2)   # P(roll in {1,2}) under H0 and H1
rec("DIE10N4_P0", float(p0), "P(roll in {1,2}; H0) = 2/6")
rec("DIE10N4_P1", float(p1), "P(roll in {1,2}; H1) = 2/4")
for k in range(n4 + 1):
    Lk = (F(3, 2) ** k) * (F(3, 4) ** (n4 - k))
    rec(f"DIE10N4_L_k{k}", float(Lk), f"likelihood ratio at K={k}  = {Lk}")
tail0 = [float(stats.binom.sf(k - 1, n4, 1 / 3)) for k in range(n4 + 2)]
for k in range(n4 + 1):
    rec(f"DIE10N4_ALPHA_K{k}", stats.binom.sf(k - 1, n4, 1 / 3), f"alpha if reject when K>={k}")
    rec(f"DIE10N4_BETA_K{k}", stats.binom.cdf(k - 1, n4, 0.5), f"beta  if reject when K>={k}")
rec("DIE10N4_ALPHA_K4_EXACT", float(F(1, 3) ** 4), "exact (1/3)^4")
rec("DIE10N4_BETA_K4_EXACT", float(1 - F(1, 2) ** 4), "exact 1-(1/2)^4")

# =====================================================================
# 5. B&T Example 9.14 - 25 coin tosses, theta0 = 1/2 vs theta1 = 2/3, alpha <= 0.1
# =====================================================================
head("5. B&T Example 9.14 - n=25 tosses, p=1/2 vs p=2/3, alpha<=0.10")
n25 = 25
for g in (14, 15, 16, 17):
    rec(f"E914_TAIL_g{g}", stats.binom.sf(g, n25, 0.5), f"P(X > {g}; H0)")
gstar = min(g for g in range(n25 + 1) if stats.binom.sf(g, n25, 0.5) <= 0.10)
rec("E914_GAMMA_EXACT", gstar, "smallest gamma with P(X>gamma;H0)<=0.10 (book: 16)")
rec("E914_ALPHA_ACHIEVED", stats.binom.sf(gstar, n25, 0.5), "achieved alpha at gamma=16")
rec("E914_BETA_AT16", stats.binom.cdf(gstar, n25, 2 / 3), "beta = P(X<=16; H1)")
rec("E914_ALPHA_AT15", stats.binom.sf(15, n25, 0.5), "alpha if gamma=15 (CLT answer)")
rec("E914_BETA_AT15", stats.binom.cdf(15, n25, 2 / 3), "beta if gamma=15")
# CLT route
rec("E914_MEAN_H0", n25 * 0.5, "n*theta0")
rec("E914_SD_H0", np.sqrt(n25 * 0.5 * 0.5), "sqrt(n theta0 (1-theta0)) = 2.5")
rec("E914_Z", z90, "z_{0.90} (book uses 1.28)")
rec("E914_GAMMA_CLT", n25 * 0.5 + z90 * np.sqrt(n25 * 0.25), "CLT gamma (book: 15.7)")
rec("E914_LR_AT_K", float(2 ** 16 * F(2, 3) ** 25), "L(16) = 2^16 (2/3)^25, check >1")
rec("E914_LR_XI_AT_16", float(2 ** 16 * (F(2, 3) ** 25)), "critical xi = L(16.0+)")
rec("E914_LR_AT_15", float(2 ** 15 * (F(2, 3) ** 25)), "L(15)")

# =====================================================================
# 6. ROC / Neyman-Pearson geometry for the normal-shift family
#    d = separation in standard deviations of the statistic.
#    power(alpha) = Phi(d - z_{1-alpha}) ;  AUC = Phi(d/sqrt2)
# =====================================================================
head("6. ROC curves for the normal shift family")
for d in (0.0, 0.5, 1.0, 2.0, 3.1622776601683795, 5.0):
    tag = f"{d:.4f}".replace(".", "p")
    rec(f"ROC_d{tag}_AUC", Phi(d / np.sqrt(2)), f"AUC at separation d={d:.4f}")
    rec(f"ROC_d{tag}_POW05", Phi(d - z95), "power at alpha=0.05")
rec("ROC_d_n10", np.sqrt(10), "d for the n=10 normal-mean test = sqrt(n)")
# numerical check of AUC by quadrature for d = sqrt(10)
d = np.sqrt(10)
auc_q = integrate.quad(lambda a: Phi(d - Phinv(1 - a)), 0, 1, limit=400)[0]
rec("ROC_AUC_QUAD_d_sqrt10", auc_q, "quadrature check of AUC")
rec("ROC_AUC_FORM_d_sqrt10", Phi(d / np.sqrt(2)), "closed form Phi(d/sqrt2)")
# the B&T 9.13 pair of operating points
rec("ROC_913_LRT_POINT_ALPHA", 0.05, "LRT operating point alpha")
rec("ROC_913_LRT_POINT_POWER", 1 - Phi((gam - 4) / np.sqrt(2)), "LRT power")
rec("ROC_913_MAX_POINT_POWER", 1 - Phi(zeta - 2) ** 2, "max-test power at the same alpha")
rec("ROC_913_d", 2 * np.sqrt(2), "separation d for n=2, mu=2")

# =====================================================================
# 7. Bayesian bridge: xi = P(H0)/P(H1) ; MAP error probability
# =====================================================================
head("7. Bayesian MAP bridge (cross-ref G6 section 3)")
d1 = np.sqrt(10)          # n = 10 normal-mean test, statistic standardized
for pr in (0.5, 0.9, 0.99):
    tag = str(pr).replace(".", "p")
    xi_b = pr / (1 - pr)
    # MAP threshold on the standardized statistic T ~ N(0,1) vs N(d,1):
    # reject when T > d/2 + log(xi)/d
    t = d1 / 2 + np.log(xi_b) / d1
    a = 1 - Phi(t)
    b = Phi(t - d1)
    rec(f"MAP_p{tag}_XI", xi_b, f"xi = P(H0)/P(H1) at P(H0)={pr}")
    rec(f"MAP_p{tag}_T", t, "MAP threshold on the standardized statistic")
    rec(f"MAP_p{tag}_ALPHA", a, "resulting alpha")
    rec(f"MAP_p{tag}_BETA", b, "resulting beta")
    rec(f"MAP_p{tag}_PERR", pr * a + (1 - pr) * b, "overall MAP error probability")
# check: MAP minimizes p*alpha + (1-p)*beta over thresholds
for pr in (0.5, 0.9, 0.99):
    tag = str(pr).replace(".", "p")
    f = lambda t: pr * (1 - Phi(t)) + (1 - pr) * Phi(t - d1)
    r = optimize.minimize_scalar(f, bounds=(-8, 12), method="bounded",
                                 options={"xatol": 1e-12})
    rec(f"MAP_p{tag}_TSTAR_NUM", r.x, "numerical argmin of p*alpha+(1-p)*beta")
    rec(f"MAP_p{tag}_PERR_NUM", r.fun, "its value - must match MAP_PERR")

# =====================================================================
# 8. L25 slide 5 - is my coin fair?  S = 472 heads in n = 1000
# =====================================================================
head("8. L25 slide 5 - is my coin fair? (S=472, n=1000)")
nC = 1000
sdC = rec("COIN_SD", np.sqrt(nC * 0.25), "sqrt(1000*0.5*0.5) = sqrt(250)")
rec("COIN_MEAN", nC * 0.5, "E[S; H0]")
rec("COIN_196SD", z975 * sdC, "1.96 * 15.8114 (slide rounds to xi=31)")
rec("COIN_XI", 31.0, "slide's critical value")
rec("COIN_EXACT_COVER_31", stats.binom.cdf(531, nC, 0.5) - stats.binom.cdf(468, nC, 0.5),
    "exact P(|S-500|<=31; H0)")
rec("COIN_EXACT_COVER_30", stats.binom.cdf(530, nC, 0.5) - stats.binom.cdf(469, nC, 0.5),
    "exact P(|S-30|<=30; H0)")
rec("COIN_EXACT_ALPHA_31", 1 - (stats.binom.cdf(531, nC, 0.5) - stats.binom.cdf(468, nC, 0.5)),
    "exact alpha at xi=31")
rec("COIN_OBS_DEV", abs(472 - 500), "|s - 500| observed")
rec("COIN_OBS_Z", (472 - 500) / sdC, "observed z-score")
rec("COIN_PVALUE_CLT", 2 * Phi((472 - 500) / sdC), "two-sided CLT p-value")
rec("COIN_PVALUE_EXACT", 2 * stats.binom.cdf(472, nC, 0.5), "two-sided exact p-value")
rec("COIN_PVALUE_CC", 2 * Phi((472 + 0.5 - 500) / sdC), "CLT with continuity correction")
# power against a genuinely biased coin
for th in (0.52, 0.55, 0.60):
    tag = str(th).replace(".", "p")
    lo, hi = 500 - 31, 500 + 31
    rec(f"COIN_POWER_{tag}", 1 - (stats.binom.cdf(hi, nC, th) - stats.binom.cdf(lo - 1, nC, th)),
        f"P(reject; theta={th})")

# =====================================================================
# 9. L25 slide 6 - is my die fair?  chi-square goodness of fit
#    Data: B&T Example 9.18 (n = 600 rolls)
# =====================================================================
head("9. L25 slide 6 / B&T Example 9.18 - is my die fair? (n=600)")
counts = np.array([92, 120, 88, 98, 95, 107], dtype=float)
nD = counts.sum()
rec("DIE_N", nD, "total rolls")
exp = nD / 6.0
rec("DIE_EXPECTED", exp, "n p_i = 600/6")
terms = (counts - exp) ** 2 / exp
for i, t in enumerate(terms, start=1):
    rec(f"DIE_TERM_{i}", t, f"({counts[i-1]:.0f}-100)^2/100")
T = rec("DIE_T", terms.sum(), "chi-square statistic T (book: 6.86)")
rec("DIE_T_SCIPY", stats.chisquare(counts).statistic, "scipy cross-check")
rec("DIE_DF", 5, "degrees of freedom m-1 = 6-1")
rec("DIE_CRIT_05", stats.chi2.ppf(0.95, 5), "chi2_5 95th percentile (book: 11.1)")
rec("DIE_CRIT_25", stats.chi2.ppf(0.75, 5), "chi2_5 75th percentile (book: 6.63)")
rec("DIE_CRIT_01", stats.chi2.ppf(0.99, 5), "chi2_5 99th percentile")
rec("DIE_PVALUE", stats.chi2.sf(T, 5), "p-value of T")
# the exact generalized-LRT statistic 2S
S = float(np.sum(counts * np.log(counts / exp)))
rec("DIE_S", S, "S = sum n_k log(n_k / n theta_k*)")
rec("DIE_2S", 2 * S, "2S (book: 6.68)")
for i, c in enumerate(counts, start=1):
    rec(f"DIE_SLOG_{i}", c * np.log(c / exp), f"{c:.0f} log({c:.0f}/100)")
rec("DIE_2S_PVALUE", stats.chi2.sf(2 * S, 5), "p-value of 2S")
# Monte-Carlo check that T is approximately chi2_5 under H0
MC = 200_000
sim = rng.multinomial(600, [1 / 6] * 6, size=MC)
Tsim = ((sim - 100.0) ** 2 / 100.0).sum(axis=1)
rec("DIE_MC_CRIT_05", np.quantile(Tsim, 0.95), "MC 95th percentile of T under H0")
rec("DIE_MC_PVALUE", (Tsim > T).mean(), "MC p-value of T=6.86")
rec("DIE_MC_MEAN", Tsim.mean(), "MC E[T] under H0 (theory: df = 5)")
rec("DIE_MC_VAR", Tsim.var(), "MC var(T) under H0 (theory: 2df = 10)")
# a loaded die that IS rejected, for contrast
loaded = np.array([70, 85, 105, 110, 105, 125], dtype=float)
rec("DIE_LOADED_SUM", loaded.sum(), "must be 600")
Tl = float(((loaded - 100) ** 2 / 100).sum())
rec("DIE_LOADED_T", Tl, "T for the contrast data set")
rec("DIE_LOADED_PVALUE", stats.chi2.sf(Tl, 5), "its p-value")

# =====================================================================
# 10. L25 slide 7 - Kolmogorov-Smirnov, 100 normal random numbers
# =====================================================================
head("10. L25 slide 7 - Kolmogorov-Smirnov test")
nK = 100
rec("KS_N", nK, "sample size on the slide's figure")
rec("KS_CRIT_STAT", 1.36, "critical value of sqrt(n) D_n at 5%")
rec("KS_CRIT_D", 1.36 / np.sqrt(nK), "corresponding critical D_n")
rec("KS_CRIT_D_EXACT", stats.kstwo.ppf(0.95, nK), "exact 5% critical D_n for n=100")
rec("KS_ASYMP_P_AT_136", stats.kstwobign.sf(1.36), "asymptotic P(sqrt(n)D_n >= 1.36)")

samp = rng.standard_normal(nK)
samp = (samp - samp.mean()) / samp.std(ddof=0)   # fix the sample exactly to mean 0, sd 1
xs = np.sort(samp)
ecdf_hi = np.arange(1, nK + 1) / nK
ecdf_lo = np.arange(0, nK) / nK
Fx = Phi(xs)
Dn = float(max(np.max(ecdf_hi - Fx), np.max(Fx - ecdf_lo)))
rec("KS_DN", Dn, "observed D_n for the standardized normal sample")
rec("KS_DN_SCIPY", stats.kstest(samp, "norm").statistic, "scipy cross-check")
rec("KS_SQRTN_DN", np.sqrt(nK) * Dn, "sqrt(n) D_n - compare with 1.36")
rec("KS_PVALUE", stats.kstest(samp, "norm").pvalue, "exact p-value")
rec("KS_ARGMAX_X", float(xs[int(np.argmax(np.maximum(ecdf_hi - Fx, Fx - ecdf_lo)))]),
    "x at which the gap is attained")
np.save(ROOT / "computes" / "g7_s4_kssample.npy", samp)

# a sample that IS rejected: exponential(1) - 1 data tested against N(0,1)
bad = rng.exponential(1.0, nK) - 1.0
rec("KSBAD_DN", stats.kstest(bad, "norm").statistic, "D_n for shifted-exponential data")
rec("KSBAD_SQRTN_DN", np.sqrt(nK) * stats.kstest(bad, "norm").statistic, "sqrt(n) D_n")
rec("KSBAD_PVALUE", stats.kstest(bad, "norm").pvalue, "its p-value - rejected")
np.save(ROOT / "computes" / "g7_s4_ksbad.npy", bad)

# =====================================================================
# 11. widget verification: LRT threshold explorer
#     H0: X ~ N(0,1), H1: X ~ N(d,1); reject when X > t.
#     alpha = 1 - Phi(t), beta = Phi(t - d), and the LR threshold is
#     xi = exp(d t - d^2/2).
# =====================================================================
head("11. widget check - LRT threshold explorer (N(0,1) vs N(d,1))")
for d, t in ((1.0, 1.6449), (2.0, 1.0), (2.0, 1.6449), (3.0, 1.5), (0.5, 0.0)):
    tag = f"d{d:.1f}t{t:.4f}".replace(".", "p").replace("-", "m")
    rec(f"WID_{tag}_ALPHA", 1 - Phi(t), "")
    rec(f"WID_{tag}_BETA", Phi(t - d), "")
    rec(f"WID_{tag}_XI", np.exp(d * t - d * d / 2), "equivalent likelihood-ratio threshold")
    rec(f"WID_{tag}_SUMERR", (1 - Phi(t)) + Phi(t - d), "alpha + beta")
    rec(f"WID_{tag}_AUC", Phi(d / np.sqrt(2)), "AUC of this ROC")
# the alpha+beta minimizing threshold is t = d/2 (the ML rule, xi = 1)
for d in (1.0, 2.0, 3.0):
    tag = f"d{d:.1f}".replace(".", "p")
    r = optimize.minimize_scalar(lambda t: (1 - Phi(t)) + Phi(t - d),
                                 bounds=(-6, 8), method="bounded",
                                 options={"xatol": 1e-12})
    rec(f"WID_MLmin_{tag}_T", r.x, "argmin of alpha+beta (theory d/2)")
    rec(f"WID_MLmin_{tag}_VAL", r.fun, "min alpha+beta = 2 Phi(-d/2)")
    rec(f"WID_MLmin_{tag}_FORM", 2 * Phi(-d / 2), "closed form")

# =====================================================================
# 12. practice-question answers
# =====================================================================
head("12. practice questions")
# P4.1 exponential rates: H0 lambda=1, H1 lambda=2, single observation, alpha=0.05
# L(x) = 2 e^{-2x} / e^{-x} = 2 e^{-x}, DEcreasing in x -> reject for SMALL x.
rec("P41_XI_STAR", 2 * np.exp(-0.0), "L(0) = 2, the largest the ratio gets")
c41 = -np.log(1 - 0.05)
rec("P41_C", c41, "reject if x < c with 1-e^{-c} = 0.05")
rec("P41_ALPHA_CHECK", 1 - np.exp(-c41), "must be 0.05")
rec("P41_BETA", np.exp(-2 * c41), "beta = P(X >= c; H1) = e^{-2c}")
rec("P41_XI_EQUIV", 2 * np.exp(-c41), "equivalent xi = 2 e^{-c}")
# P4.2 n=4 normal mean test at alpha=0.01, mu=0 vs mu=1
rec("P42_XIP", 2 * z99, "xi' = sqrt(4) z_{0.99}")
rec("P42_BETA", Phi(z99 - 2), "beta")
rec("P42_XBAR", 2 * z99 / 4, "threshold on the sample mean")
# P4.3 Poisson: H0 lambda=2, H1 lambda=5, single observation, alpha<=0.05
rec("P43_TAIL_k4", stats.poisson.sf(4, 2), "P(X>4; lam=2)")
rec("P43_TAIL_k5", stats.poisson.sf(5, 2), "P(X>5; lam=2)")
k43 = min(k for k in range(30) if stats.poisson.sf(k, 2) <= 0.05)
rec("P43_GAMMA", k43, "smallest gamma with P(X>gamma;H0)<=0.05")
rec("P43_ALPHA", stats.poisson.sf(k43, 2), "achieved alpha")
rec("P43_BETA", stats.poisson.cdf(k43, 5), "beta = P(X<=gamma; H1)")
rec("P43_LR_RATIO", (5 / 2), "L(k+1)/L(k) = lam1/lam0 = 2.5 > 1, so L increases in k")
# P4.4 discrete-die practice: reject H0 (fair) when a single roll is 1 or 2 -> already above
# P4.5 chi-square with a 3-category table
obs = np.array([48.0, 35.0, 17.0])
expc = np.array([50.0, 30.0, 20.0])
T45 = float(((obs - expc) ** 2 / expc).sum())
rec("P45_T", T45, "T for (48,35,17) vs (50,30,20)")
rec("P45_CRIT", stats.chi2.ppf(0.95, 2), "chi2_2 95th percentile")
rec("P45_PVALUE", stats.chi2.sf(T45, 2), "p-value")
# P4.6 coin fairness sample size: how large must n be to detect theta=0.52 with power 0.8?
def power_coin(nn, th=0.52, alpha=0.05):
    c = z975 * np.sqrt(nn * 0.25)
    return 1 - (Phi((c - nn * (th - 0.5)) / np.sqrt(nn * th * (1 - th)))
                - Phi((-c - nn * (th - 0.5)) / np.sqrt(nn * th * (1 - th))))
nstar = next(k for k in range(1000, 40001, 100) if power_coin(k) >= 0.80)
rec("P46_NSTAR", nstar, "n (to the nearest 100) giving power 0.80 at theta=0.52")
rec("P46_POWER_AT_NSTAR", power_coin(nstar), "its power")
rec("P46_POWER_AT_1000", power_coin(1000), "power of the lecture's n=1000 test")
# P4.6 (variance test, n=5): the uncalibrated region {sum x_i^2 > 12}
rec("P44_ALPHA_12", stats.chi2.sf(12.0, 5), "true level of the region {sum x^2 > 12}, n=5")
rec("P44_BETA_12", stats.chi2.cdf(12.0 / 4.0, 5), "its beta = P(chi2_5 <= 12/4)")
# P4.13 (test-selection drill, radar with a genuine 2% prior): the MAP threshold is the prior odds
rec("P413_MAP_ODDS", 0.98 / 0.02, "MAP threshold xi = P(H0)/P(H1) = 0.98/0.02 for a 2% target rate")
# P4.14 (test-selection drill): beta of the n=1000 coin test AT the specific alternative theta=0.55
rec("P414_BETA_AT_0p55", 1.0 - OUT["COIN_POWER_0p55"],
    "beta = 1 - power of the 5% two-sided n=1000 coin test at theta=0.55 (exact binomial)")

# =====================================================================
head("done")
p = ROOT / "computes" / "g7_s4.json"
p.write_text(json.dumps(OUT, indent=1, sort_keys=True), encoding="utf-8")
print(f"wrote {p}  ({len(OUT)} values)")
