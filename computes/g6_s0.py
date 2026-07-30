# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy"]
# ///
"""G6 §0 — orientation preview numbers.

Arc A: concentration of the sample mean (Chebyshev vs exact vs CLT),
       the pollster's problem of L19 slide 6, and the L19 slide 4 PMF.
Arc B: the coin with unknown bias of L21 slide 4 (uniform prior),
       posterior / MAP / conditional expectation.
Every number quoted in notes/src/fragments/g6_s0.html comes from here.
"""
import io
import json
import math
import sys

import numpy as np
from scipy import stats

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

R = {}


def show(key, val, fmt="{}"):
    R[key] = val
    print(f"{key:38s} = " + fmt.format(val))


# ----------------------------------------------------------------- Arc A
# L19 slide 6: pollster, f = fraction of "yes", X_i Bernoulli(f),
# M_n = sample mean, want P(|M_n - f| >= 0.01) <= 0.05.
eps = 0.01
alpha = 0.05
show("eps", eps)
show("alpha", alpha)

# per-person variance is f(1-f), maximized at f = 1/2
f_worst = 0.5
var_worst = f_worst * (1 - f_worst)
show("max_f(1-f)", var_worst)

# Chebyshev sample size:  var_worst / (n eps^2) <= alpha
n_cheb = math.ceil(var_worst / (alpha * eps**2))
show("n_chebyshev", n_cheb)
show("cheb_bound_at_50000", var_worst / (50000 * eps**2))

# CLT sample size: 2(1 - Phi(eps sqrt(n)/sigma)) <= alpha
z = stats.norm.ppf(1 - alpha / 2)
show("z_0.975", z, "{:.6f}")
n_clt_real = z**2 * var_worst / eps**2
show("n_clt_real", n_clt_real, "{:.4f}")
n_clt = math.ceil(n_clt_real)
show("n_clt", n_clt)
show("ratio_cheb_over_clt", n_cheb / n_clt, "{:.4f}")

# how the two bounds and the truth compare, f = 1/2, eps = 0.01
table = []
for n in (100, 1000, 10000, n_clt, 50000):
    cheb = var_worst / (n * eps**2)
    # exact two-sided binomial tail P(|S_n/n - 1/2| >= eps)
    k_lo = math.floor(n * (f_worst - eps))          # S_n <= k_lo
    k_hi = math.ceil(n * (f_worst + eps))           # S_n >= k_hi
    exact = stats.binom.cdf(k_lo, n, f_worst) + stats.binom.sf(k_hi - 1, n, f_worst)
    clt = 2 * stats.norm.sf(eps * math.sqrt(n) / math.sqrt(var_worst))
    table.append({"n": n, "cheb": min(cheb, 1.0), "cheb_raw": cheb,
                  "exact": exact, "clt": clt})
    print(f"  n={n:6d}  Chebyshev={min(cheb,1.0):.6f}  exact={exact:.6f}  CLT={clt:.6f}")
R["table"] = table

# L19 slide 4: Y_n = 0 w.p. 1-1/n, = n w.p. 1/n.
yn = []
for n in (10, 100, 1000):
    p_tail = 1 / n                 # P(|Y_n - 0| >= eps) for any eps in (0, n]
    mean = n * (1 / n)             # E[Y_n]
    second = n**2 * (1 / n)        # E[Y_n^2]
    yn.append({"n": n, "P_tail": p_tail, "mean": mean, "E_sq": second})
    print(f"  Y_{n}: P(|Y_n|>=eps)={p_tail:.6f}  E[Y_n]={mean:.6f}  E[Y_n^2]={second:.1f}")
R["Yn"] = yn

# ----------------------------------------------------------------- Arc B
# L21 slide 4: coin, prior Theta ~ U(0,1), X ~ Bin(n, theta), observe x heads.
n_toss, x_heads = 10, 7
a_post, b_post = x_heads + 1, n_toss - x_heads + 1     # Beta(x+1, n-x+1)
show("n_toss", n_toss)
show("x_heads", x_heads)
show("post_alpha", a_post)
show("post_beta", b_post)

# normalizing constant p_X(x) = C(n,x) B(x+1, n-x+1) = 1/(n+1)
pX = math.comb(n_toss, x_heads) * math.exp(
    math.lgamma(a_post) + math.lgamma(b_post) - math.lgamma(a_post + b_post))
show("p_X(x)", pX, "{:.10f}")
show("1/(n+1)", 1 / (n_toss + 1), "{:.10f}")

show("MAP_x_over_n", x_heads / n_toss, "{:.6f}")
post_mean = a_post / (a_post + b_post)
show("LMS_post_mean", post_mean, "{:.6f}")
post_var = a_post * b_post / ((a_post + b_post) ** 2 * (a_post + b_post + 1))
show("post_var", post_var, "{:.6f}")
show("post_sd", math.sqrt(post_var), "{:.6f}")
show("P(Theta>0.5|x)", float(stats.beta.sf(0.5, a_post, b_post)), "{:.6f}")
show("P(Theta<=0.5|x)", float(stats.beta.cdf(0.5, a_post, b_post)), "{:.6f}")
lo, hi = stats.beta.ppf([0.025, 0.975], a_post, b_post)
show("post_2.5pct", float(lo), "{:.6f}")
show("post_97.5pct", float(hi), "{:.6f}")

# prior mean/var for contrast (uniform on [0,1])
show("prior_mean", 0.5)
show("prior_var", 1 / 12, "{:.6f}")
show("var_reduction_factor", (1 / 12) / post_var, "{:.4f}")

# same data, ten times as much of it: x = 70 heads in 100 tosses
n2, x2 = 100, 70
a2, b2 = x2 + 1, n2 - x2 + 1
show("n_toss_big", n2)
show("x_heads_big", x2)
show("MAP_big", x2 / n2, "{:.6f}")
show("LMS_big", a2 / (a2 + b2), "{:.6f}")
show("post_sd_big", math.sqrt(a2 * b2 / ((a2 + b2) ** 2 * (a2 + b2 + 1))), "{:.6f}")

show("MAP_minus_LMS_n10", x_heads / n_toss - a_post / (a_post + b_post), "{:.6f}")
show("MAP_minus_LMS_n100", x2 / n2 - a2 / (a2 + b2), "{:.6f}")

# ------------------------------------------------- three scalings (Fig 0.1)
# X_i uniform on [0,1]: mu = 1/2, sigma^2 = 1/12.  L19 slide 7.
mu_u, var_u = 0.5, 1 / 12
show("uniform_mu", mu_u)
show("uniform_var", var_u, "{:.6f}")
show("uniform_sd", math.sqrt(var_u), "{:.6f}")
scal = []
for n in (1, 4, 16, 64, 256):
    row = {"n": n,
           "sd_S": math.sqrt(n * var_u),        # sd(S_n)      = sigma sqrt(n)
           "sd_M": math.sqrt(var_u / n),        # sd(M_n)      = sigma/sqrt(n)
           "sd_Z": math.sqrt(var_u)}            # sd(S_n/sqrt n) = sigma, constant
    scal.append(row)
    print(f"  n={n:4d}  sd(S_n)={row['sd_S']:.6f}  sd(M_n)={row['sd_M']:.6f}"
          f"  sd(S_n/sqrt n)={row['sd_Z']:.6f}")
R["scalings"] = scal

with open("d:/Python-UV/MIT_Applied_Prob/computes/g6_s0.json", "w", encoding="utf-8") as fh:
    json.dump(R, fh, indent=1)
print("\nwrote computes/g6_s0.json")
