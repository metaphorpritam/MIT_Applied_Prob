# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""G6 section 5 (synthesis + bridge) — every number quoted in notes/src/fragments/g6_s5.html.

Covers: Chebyshev looseness vs. exact tails, the pollster sample sizes (Chebyshev vs CLT),
the L20 binomial CLT example with and without the 1/2 correction, MAP vs posterior mean for a
skewed Beta posterior, and the LMS vs linear-LMS MSE gap for a nonlinear observation.
"""
import io
import json
import sys
from fractions import Fraction

import numpy as np
from scipy import integrate, optimize, stats

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

R = {}


def rec(key, val, label=""):
    R[key] = val
    print(f"{key:38s} = {val!r}   {label}")


# ---------------------------------------------------------------- 0. Markov looseness
print("=" * 78)
print("0. Markov bound mu/a vs the exact tail P(X >= a), X ~ Exponential(1), mu = 1")
print("=" * 78)

markov = {}
for a in (2, 3, 4, 5, 10):
    bound = 1.0 / a                      # Markov: E[X]/a with E[X] = 1
    exact = float(np.exp(-a))            # exponential(1) survival
    # Chebyshev on the same event: {X >= a} subset of {|X-1| >= a-1}; sigma^2 = 1
    cheb_b = 1.0 / (a - 1) ** 2
    markov[a] = dict(markov=bound, chebyshev=cheb_b, exact=exact,
                     ratio_markov=bound / exact, ratio_cheb=cheb_b / exact)
    print(f"  a={a:2d}: Markov={bound:.6f}  Chebyshev={cheb_b:.6f}  exact={exact:.8f}"
          f"  (Markov/exact={bound/exact:.1f}x, Cheb/exact={cheb_b/exact:.1f}x)")
rec("markov_table", markov)

# Markov is tight: X = a with probability mu/a, X = 0 otherwise
a_t, mu_t = 4.0, 1.0
rec("markov_tight_a", a_t)
rec("markov_tight_p", mu_t / a_t, "P(X=a); mean = a*(mu/a) = mu, tail = mu/a exactly")

# ---------------------------------------------------------------- 1. Chebyshev looseness
print("=" * 78)
print("1. Chebyshev bound 1/k^2 vs the exact tail P(|X-mu| >= k*sigma)")
print("=" * 78)

cheb = {}
for k in (1, 2, 3):
    bound = 1.0 / k**2
    # standard normal: exact two-sided tail
    normal = 2 * stats.norm.sf(k)
    # exponential(1): mu = 1, sigma = 1 -> P(|X-1| >= k) = P(X >= 1+k) (+ P(X <= 1-k) if k<1)
    lo = 1 - k
    expo = np.exp(-(1 + k)) + (1 - np.exp(-lo) if lo > 0 else 0.0)
    # uniform on [0,1]: mu = .5, sigma = 1/sqrt(12)
    su = 1 / np.sqrt(12)
    unif = max(0.0, 1 - 2 * min(0.5, k * su))
    # worst case two-point-plus-atom distribution attaining 1/k^2 exactly
    worst = 1.0 / k**2
    cheb[k] = dict(bound=bound, normal=normal, exponential=expo, uniform=unif, worst=worst)
    print(f"  k={k}: bound={bound:.6f} normal={normal:.6f} exp={expo:.6f} "
          f"unif={unif:.6f} worst-case={worst:.6f}")
rec("chebyshev_table", cheb)

# the worst-case distribution: P(X=-k*s)=P(X=+k*s)=1/(2k^2), P(X=0)=1-1/k^2 (mu=0, sigma=s)
k = 2.0
p_out = 1 / (2 * k**2)
mu_w = 0.0
var_w = 2 * p_out * (k**2)  # with s = 1
rec("worst_case_k", k)
rec("worst_case_p_each_atom", p_out)
rec("worst_case_variance", var_w, "(must be 1.0 with sigma=1)")
rec("worst_case_tail", 2 * p_out, "= 1/k^2 exactly -> Chebyshev is tight")

# ---------------------------------------------------------------- 2. Pollster sample sizes
print("=" * 78)
print("2. Pollster: P(|M_n - f| >= 0.01) <= 0.05  (L19 slide 6, L20 slide 4)")
print("=" * 78)

eps, target = 0.01, 0.05
sigma2_max = 0.25          # var of Bernoulli <= 1/4
n_cheb = float(Fraction(1, 4) / (Fraction(1, 20) * Fraction(1, 100) ** 2))
rec("poll_eps", eps)
rec("poll_target", target)
rec("poll_n_chebyshev", n_cheb)
# check the lecture's own figure at n = 50000 and n = 10000
for n in (10000, 50000):
    rec(f"poll_cheb_bound_n{n}", sigma2_max / (n * eps**2))
z975 = stats.norm.ppf(1 - target / 2)
rec("poll_z_975", float(z975))
n_clt = (z975 * 0.5 / eps) ** 2      # sigma <= 1/2
rec("poll_n_clt_raw", float(n_clt))
rec("poll_n_clt", int(np.ceil(n_clt)))
rec("poll_ratio", float(n_cheb / np.ceil(n_clt)))
# what the Chebyshev-sized poll actually delivers, by CLT
rec("poll_clt_prob_at_cheb_n",
    float(2 * stats.norm.sf(eps * np.sqrt(n_cheb) / 0.5)))

# ------------------------------------------------------- 3. Binomial CLT (L20 slides 6-7)
print("=" * 78)
print("3. Binomial n=36, p=0.5 — CDF and PMF via the CLT (L20 slides 6-7)")
print("=" * 78)

n_b, p_b = 36, 0.5
mu_b, sd_b = n_b * p_b, np.sqrt(n_b * p_b * (1 - p_b))
rec("binom_n", n_b); rec("binom_p", p_b)
rec("binom_mean", mu_b); rec("binom_sd", float(sd_b))
exact_le21 = float(stats.binom.cdf(21, n_b, p_b))
clt_le21 = float(stats.norm.cdf((21 - mu_b) / sd_b))
clt_le21_hc = float(stats.norm.cdf((21.5 - mu_b) / sd_b))
rec("binom_exact_le21", exact_le21)
rec("binom_clt_le21", clt_le21)
rec("binom_clt_le21_halfcorr", clt_le21_hc)
rec("binom_err_nocorr", abs(clt_le21 - exact_le21))
rec("binom_err_halfcorr", abs(clt_le21_hc - exact_le21))
rec("binom_z_21", (21 - mu_b) / sd_b)
rec("binom_z_215", (21.5 - mu_b) / sd_b)

exact_eq19 = float(stats.binom.pmf(19, n_b, p_b))
z_lo, z_hi = (18.5 - mu_b) / sd_b, (19.5 - mu_b) / sd_b
clt_eq19 = float(stats.norm.cdf(z_hi) - stats.norm.cdf(z_lo))
density_eq19 = float(stats.norm.pdf((19 - mu_b) / sd_b) / sd_b)
rec("binom_exact_eq19", exact_eq19)
rec("binom_z_185", z_lo); rec("binom_z_195", z_hi)
rec("binom_clt_eq19_window", clt_eq19)
# what the slide does: round the lower z to the 2-decimal normal table
rec("binom_Phi_050", float(stats.norm.cdf(0.50)))
rec("binom_Phi_017", float(stats.norm.cdf(0.17)))
rec("binom_clt_eq19_tabled", float(stats.norm.cdf(0.50) - stats.norm.cdf(0.17)))
rec("binom_clt_eq19_density", density_eq19)

# ---------------------------------------------------------------- 4. MAP vs posterior mean
print("=" * 78)
print("4. Beta posterior: MAP vs conditional mean (L21 slides 4-5, B&T 8.2-8.3)")
print("=" * 78)

beta_cases = {}
for heads, tosses in ((5, 5), (3, 5), (7, 10), (70, 100)):
    a, b = heads + 1, tosses - heads + 1        # uniform prior = Beta(1,1)
    mean = a / (a + b)
    mode = (a - 1) / (a + b - 2) if (a > 1 and b > 1) else (1.0 if b == 1 else 0.0)
    med = float(stats.beta.ppf(0.5, a, b))
    skew = float(stats.beta.stats(a, b, moments="s"))
    beta_cases[f"{heads}of{tosses}"] = dict(a=a, b=b, mean=mean, map=mode,
                                            median=med, skew=skew, gap=mean - mode)
    print(f"  {heads}/{tosses}: Beta({a},{b}) mean={mean:.6f} MAP={mode:.6f} "
          f"median={med:.6f} skew={skew:+.6f} gap={mean-mode:+.6f}")
rec("beta_cases", beta_cases)
rec("beta_5of5_mean_frac", str(Fraction(6, 7)))

# mean-square error of each point estimate under the Beta(6,1) posterior
a, b = 6, 1
m1, m2 = a / (a + b), a * (a + 1) / ((a + b) * (a + b + 1))
for name, c in (("mean", m1), ("map", 1.0), ("median", float(stats.beta.ppf(.5, a, b)))):
    mse = m2 - 2 * c * m1 + c**2
    rec(f"beta_6_1_mse_{name}", float(mse))
rec("beta_6_1_postvar", float(m2 - m1**2))

# ---------------------------------------------------------------- 5. LMS vs linear LMS
print("=" * 78)
print("5. Theta ~ U[0,1], X = Theta^2 : LMS is exact, linear LMS pays (L22 slides 5-6)")
print("=" * 78)

ETh = Fraction(1, 2)
ETh2 = Fraction(1, 3)
ETh3 = Fraction(1, 4)
ETh4 = Fraction(1, 5)
EX, EX2 = ETh2, ETh4
varTh = ETh2 - ETh**2
varX = EX2 - EX**2
covXT = ETh3 - EX * ETh
aL = covXT / varX
bL = ETh - aL * EX
rho2 = covXT**2 / (varX * varTh)
mseL = (1 - rho2) * varTh
rec("lms_ETheta", float(ETh)); rec("lms_varTheta", float(varTh))
rec("lms_EX", float(EX)); rec("lms_varX", float(varX))
rec("lms_cov", float(covXT))
rec("lms_a", float(aL), f"= {aL}")
rec("lms_b", float(bL), f"= {bL}")
rec("lms_rho2", float(rho2), f"= {rho2}")
rec("lms_rho", float(np.sqrt(float(rho2))))
rec("lms_mse_linear", float(mseL), f"= {mseL}")
rec("lms_mse_optimal", 0.0, "E[Theta|X] = sqrt(X) is exact")
rec("lms_mse_noobs", float(varTh), "the do-nothing estimate E[Theta]")

# independent Monte-Carlo cross-check
rng = np.random.default_rng(20260729)
th = rng.random(4_000_000)
x = th**2
a_hat, b_hat = np.polyfit(x, th, 1)
rec("lms_a_mc", float(a_hat)); rec("lms_b_mc", float(b_hat))
rec("lms_mse_linear_mc", float(np.mean((th - (float(aL) * x + float(bL))) ** 2)))
rec("lms_mse_optimal_mc", float(np.mean((th - np.sqrt(x)) ** 2)))

# ---------------------------------------------------------------- 6. Convergence gotcha
print("=" * 78)
print("6. Convergence in probability is not convergence of expectations (L19 slide 4)")
print("=" * 78)

for n in (10, 100, 10**6):
    rec(f"conv_P_Yn_ne0_n{n}", 1.0 / n)
    rec(f"conv_EYn_n{n}", n * (1.0 / n))
rec("conv_var_Yn_n100", 100 * 100 * (1 / 100) - 1.0**2)

# WLLN Chebyshev rate
sig2, eps_w = 1.0, 0.1
for n in (100, 1000, 10000):
    rec(f"wlln_bound_n{n}", sig2 / (n * eps_w**2))

# ---------------------------------------------------------------- 7. Practice questions
print("=" * 78)
print("7. Numbers for the Practice boxes (5.1-5.7)")
print("=" * 78)

# --- Practice 5.1: Markov vs Chebyshev on a nonnegative service time
mu_p1, var_p1, a_p1 = 10.0, 25.0, 40.0
rec("p1_markov", mu_p1 / a_p1)
rec("p1_cheb", var_p1 / (a_p1 - mu_p1) ** 2, "{X>=40} subset {|X-10|>=30}")
rec("p1_ratio", (mu_p1 / a_p1) / (var_p1 / (a_p1 - mu_p1) ** 2))

# --- Practice 5.2: sample size, Chebyshev vs CLT, sigma^2 = 4, eps = 0.5, delta = 0.01
sig2_p2, eps_p2, del_p2 = 4.0, 0.5, 0.01
n_cheb_p2 = sig2_p2 / (del_p2 * eps_p2**2)
z_p2 = float(stats.norm.ppf(1 - del_p2 / 2))
n_clt_p2 = (z_p2 * np.sqrt(sig2_p2) / eps_p2) ** 2
rec("p2_n_cheb", n_cheb_p2)
rec("p2_z", z_p2)
rec("p2_n_clt_raw", float(n_clt_p2))
rec("p2_n_clt", int(np.ceil(n_clt_p2)))
rec("p2_ratio", float(n_cheb_p2 / np.ceil(n_clt_p2)))
rec("p2_cheb_bound_at_nclt", float(sig2_p2 / (np.ceil(n_clt_p2) * eps_p2**2)))

# --- Practice 5.3: uniform prior, 2 heads in 3 tosses -> Beta(3,2)
a3, b3 = 3, 2
m1_3 = a3 / (a3 + b3)
m2_3 = a3 * (a3 + 1) / ((a3 + b3) * (a3 + b3 + 1))
mode3 = (a3 - 1) / (a3 + b3 - 2)
rec("p3_norm_const", 12.0, "posterior = 12 theta^2 (1-theta) on [0,1]")
rec("p3_mean", float(m1_3), str(Fraction(3, 5)))
rec("p3_map", float(mode3), str(Fraction(2, 3)))
rec("p3_postvar", float(m2_3 - m1_3**2), str(Fraction(1, 25)))
rec("p3_mse_map", float(m2_3 - 2 * mode3 * m1_3 + mode3**2))
rec("p3_mse_ratio", float((m2_3 - 2 * mode3 * m1_3 + mode3**2) / (m2_3 - m1_3**2)))
rec("p3_median", float(stats.beta.ppf(0.5, a3, b3)))

# --- Practice 5.4: Theta ~ U[0,1], X = Theta + W, W ~ U[-1,1] independent
ETh4_ = Fraction(1, 2)
varTh4 = Fraction(1, 12)
varW4 = Fraction(1, 3)          # var of U[-1,1] = (2)^2/12
EX4 = ETh4_                      # E[W] = 0
varX4 = varTh4 + varW4
cov4 = varTh4                    # cov(Theta+W, Theta) = var(Theta)
a4 = cov4 / varX4
b4 = ETh4_ - a4 * EX4
rho2_4 = cov4**2 / (varX4 * varTh4)
mse4 = (1 - rho2_4) * varTh4
rec("p4_varTheta", float(varTh4), str(varTh4))
rec("p4_varX", float(varX4), str(varX4))
rec("p4_cov", float(cov4), str(cov4))
rec("p4_a", float(a4), str(a4))
rec("p4_b", float(b4), str(b4))
rec("p4_rho2", float(rho2_4), str(rho2_4))
rec("p4_mse", float(mse4), str(mse4))
rec("p4_mse_noobs", float(varTh4))
rng4 = np.random.default_rng(20260730)
th4 = rng4.random(4_000_000)
x4 = th4 + rng4.uniform(-1, 1, 4_000_000)
a4h, b4h = np.polyfit(x4, th4, 1)
rec("p4_a_mc", float(a4h)); rec("p4_b_mc", float(b4h))
rec("p4_mse_mc", float(np.mean((th4 - (float(a4) * x4 + float(b4))) ** 2)))
# the exact LMS estimator: Theta | X=x is uniform on [max(0,x-1), min(1,x+1)],
# so E[Theta|X=x] is the midpoint of that overlap and var(Theta|X=x) = L(x)^2/12.
# E[var(Theta|X)] = int L(x)^3/24 dx over x in [-1,2]  (f_X(x) = L(x)/2).
p4_lms_mse = float(integrate.quad(
    lambda x: (min(1.0, x + 1) - max(0.0, x - 1)) ** 3 / 24.0, -1, 2,
    points=[0, 1])[0])
rec("p4_mse_lms", p4_lms_mse, "= 1/16 exactly")
lo4 = np.maximum(0.0, x4 - 1); hi4 = np.minimum(1.0, x4 + 1)
rec("p4_mse_lms_mc", float(np.mean((th4 - 0.5 * (lo4 + hi4)) ** 2)))
rec("p4_lms_vs_linear", float(mse4) / p4_lms_mse)

# --- Practice 5.7: 60 heads in 100 tosses, Bayesian vs classical
n7, k7 = 100, 60
rec("p7_ml", k7 / n7)
a7, b7 = k7 + 1, n7 - k7 + 1
rec("p7_map", (a7 - 1) / (a7 + b7 - 2), "uniform prior -> MAP = ML")
rec("p7_post_mean", a7 / (a7 + b7), str(Fraction(a7, a7 + b7)))
rec("p7_post_sd", float(stats.beta.std(a7, b7)))
rec("p7_cred_lo", float(stats.beta.ppf(0.025, a7, b7)))
rec("p7_cred_hi", float(stats.beta.ppf(0.975, a7, b7)))
se7 = np.sqrt((k7 / n7) * (1 - k7 / n7) / n7)
rec("p7_se", float(se7))
rec("p7_ci_half", float(z975 * se7))
rec("p7_ci_lo", float(k7 / n7 - z975 * se7))
rec("p7_ci_hi", float(k7 / n7 + z975 * se7))

with open("d:/Python-UV/MIT_Applied_Prob/computes/g6_s5.json", "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1, default=float)
print("\nwrote computes/g6_s5.json  (%d keys)" % len(R))
