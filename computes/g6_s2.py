# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy"]
# ///
"""All numbers for G6 section 2 (Central Limit Theorem, L20 + rec21).

Every numeric value that appears in notes/src/fragments/g6_s2.html is produced here.
Run:  uv run computes/g6_s2.py
"""
import io
import json
import math
import sys
from fractions import Fraction

import numpy as np
from scipy import stats
from scipy.special import comb, gammaln

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

R = {}


def put(k, v):
    R[k] = v
    return v


Phi = stats.norm.cdf
phi = stats.norm.pdf
Phinv = stats.norm.ppf

# =====================================================================
# A. Standard normal table lookups used throughout
# =====================================================================
print("=" * 70)
print("A. Standard normal CDF values")
for name, c in [("0.17", 0.17), ("0.1667", 0.5 / 3), ("0.5", 0.5), ("1", 1.0),
                ("1.17", 1.17), ("1.1667", 3.5 / 3), ("1.73", 1.73), ("1.92", 1.92),
                ("1.96", 1.96), ("2", 2.0), ("2.19", 2.19), ("2.1398", 2.1398),
                ("1.645", 1.645), ("1.6449", 1.6448536269514722)]:
    put(f"Phi_{name}", float(Phi(c)))
    print(f"  Phi({name:8s}) = {Phi(c):.6f}")

put("z_975", float(Phinv(0.975)))
put("z_95", float(Phinv(0.95)))
print(f"  Phi^-1(0.975) = {R['z_975']:.6f}")
print(f"  Phi^-1(0.95)  = {R['z_95']:.6f}")

# =====================================================================
# B. L20 slide 5-7 : Binomial(36, 0.5)
# =====================================================================
print("=" * 70)
print("B. Binomial(36,0.5): exact vs plain CLT vs 1/2-corrected")
n_b, p_b = 36, 0.5
mu_S = n_b * p_b
sd_S = math.sqrt(n_b * p_b * (1 - p_b))
put("b36_n", n_b); put("b36_p", p_b)
put("b36_mean", mu_S); put("b36_var", n_b * p_b * (1 - p_b)); put("b36_sd", sd_S)
print(f"  n={n_b} p={p_b}  E[S]={mu_S}  var={n_b*p_b*(1-p_b)}  sd={sd_S}")

bino = stats.binom(n_b, p_b)

# exact P(S<=21) by explicit summation (matches the slide's displayed sum)
exact_le21 = float(sum(comb(n_b, k, exact=True) for k in range(0, 22)) * 0.5 ** n_b)
put("b36_exact_le21", exact_le21)
put("b36_exact_le21_r4", round(exact_le21, 4))
z_plain = (21 - mu_S) / sd_S
z_corr = (21.5 - mu_S) / sd_S
put("b36_z_plain", z_plain); put("b36_z_corr", z_corr)
put("b36_clt_plain_le21", float(Phi(z_plain)))
put("b36_clt_corr_le21", float(Phi(z_corr)))
put("b36_err_plain_le21", float(Phi(z_plain)) - exact_le21)
put("b36_err_corr_le21", float(Phi(z_corr)) - exact_le21)
print(f"  exact P(S<=21)      = {exact_le21:.6f}")
print(f"  plain  z={z_plain:.4f} -> {Phi(z_plain):.6f}  (err {Phi(z_plain)-exact_le21:+.6f})")
print(f"  corr   z={z_corr:.4f} -> {Phi(z_corr):.6f}  (err {Phi(z_corr)-exact_le21:+.6f})")

# P(S=19)
exact_19 = float(comb(n_b, 19, exact=True) * 0.5 ** n_b)
put("b36_exact_eq19", exact_19)
zl = (18.5 - mu_S) / sd_S
zu = (19.5 - mu_S) / sd_S
put("b36_z_eq19_lo", zl); put("b36_z_eq19_hi", zu)
put("b36_Phi_lo_exact", float(Phi(zl)))
put("b36_Phi_hi_exact", float(Phi(zu)))
put("b36_clt_eq19", float(Phi(zu) - Phi(zl)))
# slide's rounded version: 0.17 and 0.5
put("b36_clt_eq19_slide", float(Phi(0.5) - Phi(0.17)))
put("b36_err_eq19", float(Phi(zu) - Phi(zl)) - exact_19)
# plain (uncorrected) attempt: Phi(19)-Phi(19) = 0
print(f"  exact P(S=19)  = {exact_19:.6f}")
print(f"  z range        = [{zl:.6f}, {zu:.6f}]")
print(f"  Phi lo/hi      = {Phi(zl):.6f} / {Phi(zu):.6f}")
print(f"  corr P(S=19)   = {Phi(zu)-Phi(zl):.6f}   (slide rounding: {Phi(0.5)-Phi(0.17):.6f})")

# comparison table over several events
tab = []
for label, lo, hi in [("S<=18", None, 18), ("S<=21", None, 21), ("S=19", 19, 19),
                      ("16<=S<=20", 16, 20), ("S>=24", 24, None)]:
    lo_i = 0 if lo is None else lo
    hi_i = n_b if hi is None else hi
    ex = float(bino.cdf(hi_i) - (bino.cdf(lo_i - 1) if lo_i > 0 else 0.0))
    # plain: use endpoints as-is
    a = -np.inf if lo is None else (lo_i - mu_S) / sd_S
    b = np.inf if hi is None else (hi_i - mu_S) / sd_S
    plain = float(Phi(b) - Phi(a))
    ac = -np.inf if lo is None else (lo_i - 0.5 - mu_S) / sd_S
    bc = np.inf if hi is None else (hi_i + 0.5 - mu_S) / sd_S
    corr = float(Phi(bc) - Phi(ac))
    tab.append(dict(event=label, exact=ex, plain=plain, corrected=corr,
                    err_plain=plain - ex, err_corr=corr - ex))
    print(f"  {label:10s} exact={ex:.6f}  plain={plain:.6f} ({plain-ex:+.6f})"
          f"  corr={corr:.6f} ({corr-ex:+.6f})")
put("b36_table", tab)

# p away from 1/2 : Binomial(50, 0.1)
print("  --- Binomial(50,0.1), the skewed case ---")
n2, p2 = 50, 0.1
m2, s2 = n2 * p2, math.sqrt(n2 * p2 * (1 - p2))
bn2 = stats.binom(n2, p2)
tab2 = []
for k in [2, 5, 8, 11]:
    ex = float(bn2.cdf(k))
    plain = float(Phi((k - m2) / s2))
    corr = float(Phi((k + 0.5 - m2) / s2))
    tab2.append(dict(k=k, exact=ex, plain=plain, corrected=corr,
                     err_plain=plain - ex, err_corr=corr - ex))
    print(f"  P(S<={k:2d}) exact={ex:.6f} plain={plain:.6f} ({plain-ex:+.6f})"
          f" corr={corr:.6f} ({corr-ex:+.6f})")
put("b50_mean", m2); put("b50_sd", s2); put("b50_table", tab2)

# de Moivre-Laplace applied to single PMF values of Binomial(36,0.5)
print("  --- de Moivre-Laplace on single PMF values, Binomial(36,0.5) ---")
tab3 = []
for k in [16, 17, 18, 19, 20, 22, 25]:
    ex = float(comb(n_b, k, exact=True) * 0.5 ** n_b)
    dm = float(Phi((k + 0.5 - mu_S) / sd_S) - Phi((k - 0.5 - mu_S) / sd_S))
    tab3.append(dict(k=k, exact=ex, dml=dm, abs_err=dm - ex,
                     rel_err_pct=100 * (dm - ex) / ex))
    print(f"  P(S={k:2d}) exact={ex:.6f}  dML={dm:.6f}  abs.err={dm-ex:+.6f}"
          f"  rel={100*(dm-ex)/ex:+.3f}%")
put("b36_pmf_table", tab3)

# sup-gap of the two CDF approximations over ALL integers, Binomial(36,0.5)
ks_all = np.arange(0, n_b + 1)
ex_cdf = bino.cdf(ks_all)
pl_cdf = Phi((ks_all - mu_S) / sd_S)
co_cdf = Phi((ks_all + 0.5 - mu_S) / sd_S)
put("b36_maxgap_plain", float(np.abs(pl_cdf - ex_cdf).max()))
put("b36_maxgap_corr", float(np.abs(co_cdf - ex_cdf).max()))
put("b36_maxgap_plain_at_k", int(ks_all[int(np.argmax(np.abs(pl_cdf - ex_cdf)))]))
put("b36_maxgap_corr_at_k", int(ks_all[int(np.argmax(np.abs(co_cdf - ex_cdf)))]))
print(f"  max |CDF err| over all k: plain {np.abs(pl_cdf-ex_cdf).max():.6f}"
      f" (at k={ks_all[np.argmax(np.abs(pl_cdf-ex_cdf))]}),"
      f" corrected {np.abs(co_cdf-ex_cdf).max():.6f}"
      f" (at k={ks_all[np.argmax(np.abs(co_cdf-ex_cdf))]})")

# =====================================================================
# C. L20 slide 4 + B&T Example 5.11 : the pollster's problem
# =====================================================================
print("=" * 70)
print("C. Polling with the CLT")
eps, delta = 0.01, 0.05
z_need = float(Phinv(1 - delta / 2))
put("poll_eps", eps); put("poll_delta", delta); put("poll_z", z_need)
n_clt_exact = (z_need / (2 * eps)) ** 2
put("poll_n_clt_exact", float(n_clt_exact))
put("poll_n_clt", int(math.ceil(n_clt_exact)))
# with the table value 1.96
n_196 = (1.96 / (2 * eps)) ** 2
put("poll_n_clt_196", float(n_196))
put("poll_n_clt_196_ceil", int(math.ceil(n_196)))
# Chebyshev requirement (rec20 / L19 style): n >= 1/(4 eps^2 delta)
n_cheb = 1.0 / (4 * eps ** 2 * delta)
put("poll_n_cheb", float(n_cheb))
put("poll_ratio", float(n_cheb / n_196))
print(f"  z needed = Phi^-1(0.975) = {z_need:.6f}   (table value 1.96)")
print(f"  n_CLT (exact z)  = {n_clt_exact:.4f} -> {math.ceil(n_clt_exact)}")
print(f"  n_CLT (z=1.96)   = {n_196:.4f} -> {math.ceil(n_196)}")
print(f"  n_Chebyshev      = {n_cheb:.0f}")
print(f"  ratio            = {n_cheb/n_196:.4f}")
# check the achieved probability at n = 9604 with worst-case sigma
n_star = 9604
achieved = float(2 * (1 - Phi(2 * eps * math.sqrt(n_star))))
put("poll_check_arg", float(2 * eps * math.sqrt(n_star)))
put("poll_achieved", achieved)
print(f"  at n=9604: 2(1-Phi({2*eps*math.sqrt(n_star):.4f})) = {achieved:.6f}")
# n = 100, eps = 0.1 (B&T Example 5.11 first half)
n_100, eps_1 = 100, 0.1
arg_100 = 2 * eps_1 * math.sqrt(n_100)
put("poll100_arg", float(arg_100))
put("poll100_bound", float(2 - 2 * Phi(arg_100)))
put("poll100_bound_table", float(2 - 2 * 0.977))
put("poll100_cheb", float(1 / (4 * n_100 * eps_1 ** 2)))
print(f"  n=100, eps=0.1: CLT bound 2-2Phi({arg_100}) = {2-2*Phi(arg_100):.6f}"
      f"   (table 0.977 -> {2-2*0.977:.4f});  Chebyshev = {1/(4*n_100*eps_1**2):.4f}")
# exact binomial check at p=1/2, n=100
sb = stats.binom(n_100, 0.5)
exact_poll = float(1 - (sb.cdf(59) - sb.cdf(40)))
put("poll100_exact_p_half", exact_poll)
print(f"  exact (p=1/2): P(|M100-0.5|>=0.1) = {exact_poll:.6f}")

# sample size curve, CLT vs Chebyshev
eps_grid = [0.05, 0.03, 0.02, 0.01, 0.005]
curve = []
for e in eps_grid:
    nc = (z_need / (2 * e)) ** 2
    nch = 1.0 / (4 * e ** 2 * delta)
    curve.append(dict(eps=e, n_clt=math.ceil(nc), n_cheb=math.ceil(nch),
                      ratio=nch / nc))
    print(f"  eps={e:<6} n_CLT={math.ceil(nc):>7}  n_Cheb={math.ceil(nch):>7}"
          f"  ratio={nch/nc:.2f}")
put("poll_curve", curve)

# =====================================================================
# D. rec21 Problem 1 : 10 uniforms, Markov vs Chebyshev vs CLT vs exact
# =====================================================================
print("=" * 70)
print("D. rec21 P1: X_1..X_10 ~ U[0,1], P(sum >= 7)")
n_u = 10
mu_u, var_u = 0.5, Fraction(1, 12)
EX = n_u * mu_u
varX = n_u * var_u
sdX = math.sqrt(float(varX))
put("r1_n", n_u); put("r1_EX", EX)
put("r1_varX_frac", str(varX)); put("r1_varX", float(varX)); put("r1_sdX", sdX)
markov = Fraction(5, 7)
put("r1_markov_frac", "5/7"); put("r1_markov", float(markov))
cheb_two = float(varX) / 4
cheb_one = cheb_two / 2
put("r1_cheb_twosided", cheb_two)
put("r1_cheb_onesided", cheb_one)
put("r1_cheb_frac", "5/48")
z_r1 = 2 / sdX
put("r1_z", z_r1); put("r1_z_r2", round(z_r1, 2))
put("r1_Phi_z", float(Phi(z_r1)))
put("r1_Phi_219", float(Phi(2.19)))
put("r1_clt", float(1 - Phi(z_r1)))
put("r1_clt_219", float(1 - Phi(2.19)))
print(f"  E[X]={EX}  var(X)={varX}={float(varX):.6f}  sd={sdX:.6f}")
print(f"  Markov     : 5/7 = {float(markov):.6f}")
print(f"  Chebyshev  : two-sided {cheb_two:.6f}, one-sided 5/48 = {cheb_one:.6f}")
print(f"  CLT        : z = 2/{sdX:.4f} = {z_r1:.6f} (~2.19), 1-Phi = {1-Phi(z_r1):.6f}"
      f"  [slide 1-Phi(2.19) = {1-Phi(2.19):.6f}]")


def irwin_hall_cdf(x, n):
    """Exact P(U_1+...+U_n <= x), U_i iid uniform[0,1], via the Irwin-Hall formula."""
    x = Fraction(x)
    tot = Fraction(0)
    kmax = int(math.floor(x))
    for k in range(0, kmax + 1):
        tot += Fraction((-1) ** k) * comb(n, k, exact=True) * (x - k) ** n
    return tot / math.factorial(n)


ih = irwin_hall_cdf(7, 10)
exact_r1 = 1 - float(ih)
put("r1_exact_frac", f"{(1-ih).numerator}/{(1-ih).denominator}")
put("r1_exact", exact_r1)
print(f"  EXACT (Irwin-Hall): P(sum>=7) = {(1-ih)} = {exact_r1:.8f}")
r1_bars = dict(markov=float(markov), chebyshev=cheb_one, clt=float(1 - Phi(z_r1)),
               exact=exact_r1)
put("r1_bars", r1_bars)
put("r1_markov_over_exact", float(markov) / exact_r1)
put("r1_cheb_over_exact", cheb_one / exact_r1)
put("r1_clt_over_exact", float(1 - Phi(z_r1)) / exact_r1)
print(f"  ratios to exact: Markov {float(markov)/exact_r1:.1f}x, "
      f"Chebyshev {cheb_one/exact_r1:.1f}x, CLT {(1-Phi(z_r1))/exact_r1:.3f}x")
# 1/2-correction is NOT applicable (continuous) - sanity: corrected would be wrong
# also the Chebyshev one-sided (Cantelli) bound, for the Gotcha
cantelli = float(varX) / (float(varX) + 4)
put("r1_cantelli", cantelli)
print(f"  (Cantelli one-sided bound var/(var+a^2) = {cantelli:.6f})")

# =====================================================================
# E. rec21 Problem 2 : gadget factory (unsolved on the sheet)
# =====================================================================
print("=" * 70)
print("E. rec21 P2: gadgets, mean 5 variance 9")
mu_g, var_g = 5.0, 9.0
sd_g = 3.0
put("g_mu", mu_g); put("g_var", var_g); put("g_sd", sd_g)
# (a)
n_a = 100
mean_a, sd_a = n_a * mu_g, math.sqrt(n_a * var_g)
z_a = (440 - mean_a) / sd_a
put("g_a_n", n_a); put("g_a_mean", mean_a); put("g_a_var", n_a * var_g); put("g_a_sd", sd_a)
put("g_a_z", z_a); put("g_a_prob", float(Phi(z_a)))
z_a_c = (439.5 - mean_a) / sd_a
put("g_a_z_corr", z_a_c); put("g_a_prob_corr", float(Phi(z_a_c)))
print(f"  (a) mean={mean_a} sd={sd_a} z=({440}-{mean_a})/{sd_a}={z_a} -> {Phi(z_a):.6f}")
print(f"      (with 1/2 correction, if integer-valued: z={z_a_c:.6f} -> {Phi(z_a_c):.6f})")
# (b)
zb = z_need if False else float(Phinv(0.95))
nb_exact = (200 / (sd_g * zb)) ** 2
put("g_b_z", zb); put("g_b_n_exact", float(nb_exact))
put("g_b_n", int(math.floor(nb_exact)))
put("g_b_sqrt_n", float(200 / (sd_g * zb)))
print(f"  (b) need 1-Phi(200/(3 sqrt n)) <= 0.05 -> 200/(3 sqrt n) >= {zb:.6f}")
print(f"      sqrt(n) <= {200/(3*zb):.6f}  ->  n <= {nb_exact:.4f}  -> n* = {math.floor(nb_exact)}")
for nn in [1642, 1643]:
    pr = float(1 - Phi(200 / (3 * math.sqrt(nn))))
    put(f"g_b_check_{nn}", pr)
    print(f"      check n={nn}: 1-Phi({200/(3*math.sqrt(nn)):.6f}) = {pr:.6f}")
# with the rounded table value 1.645
nb_1645 = (200 / (3 * 1.645)) ** 2
put("g_b_n_1645", float(nb_1645)); put("g_b_n_1645_floor", int(math.floor(nb_1645)))
print(f"      with z=1.645: n <= {nb_1645:.4f} -> {math.floor(nb_1645)}")
# (c)
n_c = 219
mean_c, sd_c = n_c * mu_g, math.sqrt(n_c * var_g)
z_c = (1000 - mean_c) / sd_c
put("g_c_n", n_c); put("g_c_mean", mean_c); put("g_c_sd", sd_c)
put("g_c_z", z_c); put("g_c_prob", float(Phi(z_c)))
print(f"  (c) N>=220 <=> S_219 <= 1000; mean={mean_c} sd=3*sqrt(219)={sd_c:.6f}")
print(f"      z=({1000}-{mean_c})/{sd_c:.4f} = {z_c:.6f} -> {Phi(z_c):.6f}")
n_c2 = 220
mean_c2, sd_c2 = n_c2 * mu_g, math.sqrt(n_c2 * var_g)
z_c2 = (1000 - mean_c2) / sd_c2
put("g_c_alt_n", n_c2); put("g_c_alt_z", z_c2); put("g_c_alt_prob", float(Phi(z_c2)))
print(f"      (variant using S_220: z={z_c2:.6f} -> {Phi(z_c2):.6f})")

# =====================================================================
# F. rec21 Problem 3 : Stirling from the CLT
# =====================================================================
print("=" * 70)
print("F. rec21 P3: Stirling's formula from the CLT")
stir = []
for n in [1, 2, 5, 10, 20, 50, 100]:
    exact = math.factorial(n)
    approx = math.sqrt(2 * math.pi * n) * (n / math.e) ** n
    rel = (approx - exact) / exact
    lam = math.log(exact) - math.log(approx)
    stir.append(dict(n=n, exact=float(exact), approx=approx, rel_err=rel,
                     lam=lam, lo=1 / (12 * n + 1), hi=1 / (12 * n)))
    print(f"  n={n:4d}  n! = {exact:.6e}   approx = {approx:.6e}   rel.err = {rel:+.6f}"
          f"   lambda_n = {lam:.8f}  in ({1/(12*n+1):.8f}, {1/(12*n):.8f})")
put("stirling", stir)
# the CLT step itself, P(S_n = n) for Poisson(n)
pois = []
for n in [5, 10, 20, 50, 100]:
    ex = float(stats.poisson(n).pmf(n))
    ap = 1 / math.sqrt(2 * math.pi * n)
    clt = float(Phi(0.5 / math.sqrt(n)) - Phi(-0.5 / math.sqrt(n)))
    pois.append(dict(n=n, exact=ex, one_over=ap, clt_interval=clt,
                     rel_err=(ap - ex) / ex))
    print(f"  n={n:4d}  P(S_n=n) exact = {ex:.8f}   1/sqrt(2 pi n) = {ap:.8f}"
          f"   CLT interval = {clt:.8f}   rel.err = {(ap-ex)/ex:+.6f}")
put("poisson_atom", pois)

# =====================================================================
# G. B&T Examples 5.9, 5.10 (worked normal approximations)
# =====================================================================
print("=" * 70)
print("G. B&T Examples 5.9 / 5.10")
mu59 = (5 + 50) / 2
var59 = (50 - 5) ** 2 / 12
n59 = 100
m59, s59 = n59 * mu59, math.sqrt(n59 * var59)
z59 = (3000 - m59) / s59
put("e59_mu", mu59); put("e59_var", var59); put("e59_mean", m59); put("e59_sd", s59)
put("e59_z", z59); put("e59_Phi", float(Phi(z59))); put("e59_ans", float(1 - Phi(z59)))
put("e59_Phi_192", float(Phi(1.92))); put("e59_ans_192", float(1 - Phi(1.92)))
print(f"  5.9: mu={mu59} var={var59} mean={m59} sd={s59:.4f} z={z59:.6f}")
print(f"       Phi(z)={Phi(z59):.6f} -> P(S>3000)={1-Phi(z59):.6f}"
      f"  [book: Phi(1.92)={Phi(1.92):.4f}, ans {1-Phi(1.92):.4f}]")
mu510 = 3.0
var510 = (5 - 1) ** 2 / 12
m510, s510 = 100 * mu510, math.sqrt(100 * var510)
z510 = (320 - m510) / s510
put("e510_mu", mu510); put("e510_var", var510); put("e510_sd", s510)
put("e510_z", z510); put("e510_Phi", float(Phi(z510)))
put("e510_Phi_173", float(Phi(1.73)))
print(f"  5.10: mu={mu510} var={var510:.6f} mean={m510} sd={s510:.6f} z={z510:.6f}")
print(f"        Phi(z)={Phi(z510):.6f}  [book Phi(1.73)={Phi(1.73):.4f}]")
# exact check on 5.10 by Irwin-Hall scaling: X_i = 1 + 4U_i, S = 100 + 4*sum U
x_ih = Fraction(320 - 100, 4)
ex510 = float(stats.irwinhall.cdf(float(x_ih), 100))
put("e510_exact", ex510)
print(f"        exact (Irwin-Hall) = {ex510:.6f}   CLT error = {Phi(z510)-ex510:+.6f}")

# =====================================================================
# H. Kolmogorov distance sup_z |F_{Z_n}(z) - Phi(z)| for several base shapes
# =====================================================================
print("=" * 70)
print("H. max CDF gap  sup_z |F_Zn(z) - Phi(z)|")


def lattice_gap(vals, probs, n):
    """Exact sup-gap for a lattice base distribution, by PMF convolution."""
    vals = np.asarray(vals, dtype=float)
    probs = np.asarray(probs, dtype=float)
    step = 1.0
    # assume integer support
    lo, hi = int(vals.min()), int(vals.max())
    base = np.zeros(hi - lo + 1)
    for v, p in zip(vals, probs):
        base[int(v) - lo] += p
    f = base.copy()
    for _ in range(n - 1):
        f = np.convolve(f, base)
    supp = np.arange(n * lo, n * hi + 1, dtype=float)
    mu = float((vals * probs).sum())
    var = float((vals ** 2 * probs).sum() - mu ** 2)
    sd = math.sqrt(n * var)
    z = (supp - n * mu) / sd
    F = np.cumsum(f)
    # sup over reals attained just left or just right of each atom
    gap_right = np.abs(F - Phi(z))
    Fleft = np.concatenate([[0.0], F[:-1]])
    gap_left = np.abs(Fleft - Phi(z))
    return float(max(gap_right.max(), gap_left.max())), step / sd


def cont_gap(kind, n, h=None):
    """sup-gap sup_z |F_{Z_n}(z) - Phi(z)| for a continuous base distribution,
    computed from the EXACT distribution of the sum:
      uniform[0,1] sum  -> Irwin-Hall(n)
      Exp(1) sum        -> Gamma(n, 1) (Erlang).
    The h argument is kept for call compatibility and ignored."""
    if kind == "unif":
        mu, var = 0.5, 1 / 12
        sd = math.sqrt(n * var)
        z = np.linspace(-9.0, 9.0, 600001)
        F = stats.irwinhall.cdf(z * sd + n * mu, n)
    elif kind == "expo":
        mu, var = 1.0, 1.0
        sd = math.sqrt(n * var)
        z = np.linspace(-9.0, 14.0, 600001)
        F = stats.gamma.cdf(z * sd + n * mu, a=n)
    else:
        raise ValueError(kind)
    return float(np.max(np.abs(F - Phi(z))))


gap_table = {}
for n in [1, 2, 4, 8, 16, 32]:
    row = {}
    row["unif"] = cont_gap("unif", n)
    row["expo"] = cont_gap("expo", n, h=0.004)
    row["bern5"], _ = lattice_gap([0, 1], [0.5, 0.5], n)
    row["bern1"], _ = lattice_gap([0, 1], [0.9, 0.1], n)
    row["bimodal"], _ = lattice_gap([0, 1, 5, 6], [0.25] * 4, n)
    gap_table[n] = row
    print(f"  n={n:3d}  unif={row['unif']:.5f}  expo={row['expo']:.5f}"
          f"  Bern(.5)={row['bern5']:.5f}  Bern(.1)={row['bern1']:.5f}"
          f"  bimodal={row['bimodal']:.5f}")
put("gap_table", {str(k): v for k, v in gap_table.items()})

# widget cross-check values (the widget uses a coarser grid; these are the targets)
widget_check = {}
for label, n in [("unif_n4", 4), ("unif_n16", 16), ("expo_n4", 4), ("expo_n16", 16)]:
    kind = label.split("_")[0]
    widget_check[label] = cont_gap(kind, n, h=0.004)
for label, n in [("bern5_n8", 8), ("bern1_n8", 8), ("bimodal_n8", 8)]:
    if label.startswith("bern5"):
        widget_check[label] = lattice_gap([0, 1], [0.5, 0.5], n)[0]
    elif label.startswith("bern1"):
        widget_check[label] = lattice_gap([0, 1], [0.9, 0.1], n)[0]
    else:
        widget_check[label] = lattice_gap([0, 1, 5, 6], [0.25] * 4, n)[0]
put("widget_check", widget_check)
print("  widget cross-check:", {k: round(v, 5) for k, v in widget_check.items()})

# ---- parity table for the §2.2 widget: EXACTLY the four bases it offers ----
print("  --- widget parity table (same four bases as w-g6s2-clt) ---")
w_rows = []
for n in [1, 2, 4, 8, 16, 32, 64]:
    row = dict(
        n=n,
        unif8=lattice_gap(list(range(1, 9)), [1 / 8] * 8, n)[0],
        expo=cont_gap("expo", n),
        bern05=lattice_gap([0, 1], [0.5, 0.5], n)[0],
        bern02=lattice_gap([0, 1], [0.8, 0.2], n)[0],
        bimodal=lattice_gap([0, 1, 5, 6], [0.25] * 4, n)[0],
    )
    w_rows.append(row)
    print(f"  n={n:3d}  unif8={row['unif8']:.5f}  expo={row['expo']:.5f}"
          f"  Bern(.5)={row['bern05']:.5f}  Bern(.2)={row['bern02']:.5f}"
          f"  bimodal={row['bimodal']:.5f}")
put("widget_parity", w_rows)

# Berry-Esseen constant check for Bernoulli(0.5): C * rho / (sigma^3 sqrt n), C=0.4748
be = {}
for n in [8, 16, 32]:
    sig = 0.5
    rho = 0.5 * abs(0 - 0.5) ** 3 + 0.5 * abs(1 - 0.5) ** 3
    be[n] = 0.4748 * rho / (sig ** 3 * math.sqrt(n))
put("berry_esseen_bern5", {str(k): v for k, v in be.items()})
print("  Berry-Esseen bound, Bernoulli(0.5):",
      {k: round(v, 5) for k, v in be.items()})

# =====================================================================
# I. Poisson vs normal approximation of the binomial (L20 slide 8)
# =====================================================================
print("=" * 70)
print("I. Poisson vs normal approximation of the binomial")
pn = []
for (n, p) in [(100, 0.01), (500, 0.1)]:
    b = stats.binom(n, p)
    lam = n * p
    ks = np.arange(0, n + 1)
    ex = b.pmf(ks)
    po = stats.poisson(lam).pmf(ks)
    mu_, sd_ = n * p, math.sqrt(n * p * (1 - p))
    no = Phi((ks + 0.5 - mu_) / sd_) - Phi((ks - 0.5 - mu_) / sd_)
    row = dict(n=n, p=p, lam=lam, sd=sd_,
               max_pmf_err_poisson=float(np.abs(po - ex).max()),
               max_pmf_err_normal=float(np.abs(no - ex).max()),
               max_cdf_err_poisson=float(np.abs(np.cumsum(po) - np.cumsum(ex)).max()),
               max_cdf_err_normal=float(np.abs(np.cumsum(no) - np.cumsum(ex)).max()))
    pn.append(row)
    print(f"  n={n} p={p}: lambda={lam} sd={sd_:.4f}")
    print(f"     max |pmf err|  Poisson {row['max_pmf_err_poisson']:.6f} | "
          f"normal {row['max_pmf_err_normal']:.6f}")
    print(f"     max |cdf err|  Poisson {row['max_cdf_err_poisson']:.6f} | "
          f"normal {row['max_cdf_err_normal']:.6f}")
put("poisson_vs_normal", pn)

# =====================================================================
# J. Practice question answers
# =====================================================================
print("=" * 70)
print("J. Practice questions")
# P2.1 : 300 dice rolls, P(sum between 1000 and 1100)
mu_d = 3.5
var_d = 35 / 12
n_d = 300
m_d, s_d = n_d * mu_d, math.sqrt(n_d * var_d)
put("pr_dice_mu", mu_d); put("pr_dice_var", var_d)
put("pr_dice_mean", m_d); put("pr_dice_sd", s_d)
za = (1000 - 0.5 - m_d) / s_d
zb = (1100 + 0.5 - m_d) / s_d
put("pr_dice_zlo", za); put("pr_dice_zhi", zb)
put("pr_dice_ans", float(Phi(zb) - Phi(za)))
za0 = (1000 - m_d) / s_d
zb0 = (1100 - m_d) / s_d
put("pr_dice_ans_plain", float(Phi(zb0) - Phi(za0)))
print(f"  dice: mean={m_d} sd={s_d:.6f} z=[{za:.6f},{zb:.6f}] -> {Phi(zb)-Phi(za):.6f}"
      f"  (uncorrected {Phi(zb0)-Phi(za0):.6f})")
# exact by convolution
base = np.ones(6) / 6
f = base.copy()
for _ in range(n_d - 1):
    f = np.convolve(f, base)
supp = np.arange(n_d, 6 * n_d + 1)
mask = (supp >= 1000) & (supp <= 1100)
put("pr_dice_exact", float(f[mask].sum()))
print(f"        exact = {f[mask].sum():.6f}")

# P2.2 : exponential service times, lambda = 1/4 min, 60 customers, P(total <= 250)
lam_s = 0.25
mu_s, var_s = 1 / lam_s, 1 / lam_s ** 2
n_s = 60
m_s, sd_s2 = n_s * mu_s, math.sqrt(n_s * var_s)
z_s = (250 - m_s) / sd_s2
put("pr_exp_mu", mu_s); put("pr_exp_var", var_s)
put("pr_exp_mean", m_s); put("pr_exp_sd", sd_s2); put("pr_exp_z", z_s)
put("pr_exp_ans", float(Phi(z_s)))
put("pr_exp_exact", float(stats.gamma(a=n_s, scale=1 / lam_s).cdf(250)))
print(f"  exp: mean={m_s} sd={sd_s2:.6f} z={z_s:.6f} -> CLT {Phi(z_s):.6f}"
      f"  exact(Erlang) {stats.gamma(a=n_s, scale=1/lam_s).cdf(250):.6f}")

# P2.3 : coin, n = 1000 fair flips, P(heads >= 530)
n_f = 1000
m_f, s_f = 500.0, math.sqrt(1000 * 0.25)
z_f = (529.5 - m_f) / s_f
put("pr_coin_mean", m_f); put("pr_coin_sd", s_f); put("pr_coin_z", z_f)
put("pr_coin_ans", float(1 - Phi(z_f)))
put("pr_coin_plain", float(1 - Phi((530 - m_f) / s_f)))
put("pr_coin_exact", float(1 - stats.binom(n_f, 0.5).cdf(529)))
put("pr_coin_cheb", float(0.25 * n_f / 30 ** 2 / 2))
print(f"  coin: sd={s_f:.6f} z={z_f:.6f} corrected {1-Phi(z_f):.6f}"
      f"  plain {1-Phi((530-m_f)/s_f):.6f}  exact {1-stats.binom(n_f,0.5).cdf(529):.6f}"
      f"  Chebyshev(one-sided-by-symmetry) {0.25*n_f/900/2:.6f}")

# P2.4 : how many samples so that sample mean of Exp(1) is within 0.05 w.p. 0.99
z99 = float(Phinv(0.995))
n_req = (z99 * 1.0 / 0.05) ** 2
put("pr_size_z", z99); put("pr_size_n", float(n_req)); put("pr_size_n_ceil", int(math.ceil(n_req)))
put("pr_size_cheb", float(1 / (0.01 * 0.05 ** 2)))
print(f"  sample size: z={z99:.6f} n>={n_req:.4f} -> {math.ceil(n_req)}"
      f"   (Chebyshev would need {1/(0.01*0.05**2):.0f})")

# P2.5 : symmetric vs skewed at the same n (used in a Gotcha)
put("gap_unif_n4", gap_table[4]["unif"])
put("gap_expo_n4", gap_table[4]["expo"])
put("gap_expo_n32", gap_table[32]["expo"])
put("gap_unif_n2", gap_table[2]["unif"])

# =====================================================================
# K. Every remaining number quoted in the prose of g6_s2.html
# =====================================================================
print("=" * 70)
print("K. Remaining prose numbers")

# largest atom of the standardized Bernoulli(1/2) sum (the §2.2 Gotcha)
for n in [16, 64]:
    pk = float(stats.binom(n, 0.5).pmf(n // 2))
    put(f"atom_max_bern5_n{n}", pk)
    print(f"  largest atom of Z_{n} (Bernoulli .5): {pk:.6f}")

# the "cut at 22" alternative in the §2.4 derivation
put("b36_z_cut22", (22 - mu_S) / sd_S)
put("b36_clt_cut22", float(Phi((22 - mu_S) / sd_S)))
put("b36_cut_ambiguity", float(Phi((22 - mu_S) / sd_S) - Phi((21 - mu_S) / sd_S)))
print(f"  cut at 22: z={(22-mu_S)/sd_S:.6f} -> {Phi((22-mu_S)/sd_S):.6f}"
      f"   ambiguity = {Phi((22-mu_S)/sd_S)-Phi((21-mu_S)/sd_S):.6f}")

put("b36_C_36_19", comb(n_b, 19, exact=True))
put("b36_pmf_21", float(comb(n_b, 21, exact=True) * 0.5 ** n_b))
put("b36_half_bar_21", 0.5 * float(comb(n_b, 21, exact=True) * 0.5 ** n_b))
put("b36_pmf_18", float(comb(n_b, 18, exact=True) * 0.5 ** n_b))
print(f"  C(36,19) = {comb(n_b,19,exact=True)}   P(S=21)={comb(n_b,21,exact=True)*0.5**n_b:.6f}"
      f"   half of it = {0.5*comb(n_b,21,exact=True)*0.5**n_b:.6f}")
put("b36_err_ratio_le21", abs(float(Phi(z_plain)) - exact_le21)
    / abs(float(Phi(z_corr)) - exact_le21))
put("b36_maxgap_ratio", float(np.abs(pl_cdf - ex_cdf).max()
                              / np.abs(co_cdf - ex_cdf).max()))
print(f"  error-improvement factor at k=21: "
      f"{abs(Phi(z_plain)-exact_le21)/abs(Phi(z_corr)-exact_le21):.1f}x;"
      f"  worst-case: {np.abs(pl_cdf-ex_cdf).max()/np.abs(co_cdf-ex_cdf).max():.1f}x")

# exact binomial check of the poll at the worst case f = 1/2, n = 9604
n_star2, f_star = 9604, 0.5
bb = stats.binom(n_star2, f_star)
lo_k = int(math.floor(n_star2 * (f_star - eps)))     # |M-f| >= .01  <=>  S <= lo or S >= hi
hi_k = int(math.ceil(n_star2 * (f_star + eps)))
exact_poll2 = float(bb.cdf(lo_k) + (1 - bb.cdf(hi_k - 1)))
put("poll_exact_binom_f0p5_n9604", exact_poll2)
put("poll_cheb_guarantee_at_9604", float(1 / (4 * n_star2 * eps ** 2)))
print(f"  exact P(|M_n - 0.5| >= 0.01) at n=9604: {exact_poll2:.6f}"
      f"   (Chebyshev would only promise <= {1/(4*n_star2*eps**2):.4f})")

# Berry-Esseen shape ratio rho/sigma^3 for Bernoulli(p)
for pp in [0.5, 0.1]:
    q = 1 - pp
    put(f"be_ratio_p{str(pp).replace('.', 'p')}", (pp ** 2 + q ** 2) / math.sqrt(pp * q))
    print(f"  Bernoulli({pp}): rho/sigma^3 = (p^2+q^2)/sqrt(pq) = "
          f"{(pp**2+q**2)/math.sqrt(pp*q):.6f}")
put("bern0p1_atom_zero_n16", float(0.9 ** 16))
print(f"  Bernoulli(0.1), n=16: P(S=0) = 0.9^16 = {0.9**16:.6f}")

# Practice 2.5 - e-mails
m_e, sd_e = 30 * 40.0, math.sqrt(30 * 144.0)
put("pr_mail_mean", m_e); put("pr_mail_var", 30 * 144.0); put("pr_mail_sd", sd_e)
put("pr_mail_z", (1300 - m_e) / sd_e)
put("pr_mail_ans", float(1 - Phi((1300 - m_e) / sd_e)))
put("pr_mail_z_corr", (1300.5 - m_e) / sd_e)
put("pr_mail_ans_corr", float(1 - Phi((1300.5 - m_e) / sd_e)))
print(f"  e-mails: mean={m_e} sd={sd_e:.6f} z={(1300-m_e)/sd_e:.6f}"
      f" -> {1-Phi((1300-m_e)/sd_e):.6f}   corrected"
      f" z={(1300.5-m_e)/sd_e:.6f} -> {1-Phi((1300.5-m_e)/sd_e):.6f}")

# Practice 2.10 ratio
put("pr_size_ratio", float((1 / (0.01 * 0.05 ** 2)) / ((Phinv(0.995) / 0.05) ** 2)))
print(f"  sample-size ratio Chebyshev/CLT = {R['pr_size_ratio']:.4f}")

# Practice 2.11 - central binomial coefficient
m_c = 18
put("pr_cbc_m", m_c)
put("pr_cbc_approx", 1 / math.sqrt(math.pi * m_c))
put("pr_cbc_exact", float(comb(2 * m_c, m_c, exact=True) * 0.5 ** (2 * m_c)))
put("pr_cbc_rel_pct", 100 * (1 / math.sqrt(math.pi * m_c)
                             - comb(2 * m_c, m_c, exact=True) * 0.5 ** (2 * m_c))
    / (comb(2 * m_c, m_c, exact=True) * 0.5 ** (2 * m_c)))
print(f"  central binomial m=18: 1/sqrt(pi m) = {1/math.sqrt(math.pi*m_c):.6f}"
      f"  exact = {comb(2*m_c,m_c,exact=True)*0.5**(2*m_c):.6f}"
      f"  rel = {R['pr_cbc_rel_pct']:+.3f}%")

# Practice 2.12 - call centre, Poisson(180)
mu_p = 180.0
sd_p = math.sqrt(mu_p)
put("pr_call_mu", mu_p); put("pr_call_sd", sd_p)
put("pr_call_z_corr", (200.5 - mu_p) / sd_p)
put("pr_call_ans_corr", float(1 - Phi((200.5 - mu_p) / sd_p)))
put("pr_call_z_plain", (200 - mu_p) / sd_p)
put("pr_call_ans_plain", float(1 - Phi((200 - mu_p) / sd_p)))
put("pr_call_exact", float(1 - stats.poisson(mu_p).cdf(200)))
print(f"  calls: sd={sd_p:.6f} z_corr={(200.5-mu_p)/sd_p:.6f}"
      f" -> {1-Phi((200.5-mu_p)/sd_p):.6f}   plain -> {1-Phi((200-mu_p)/sd_p):.6f}"
      f"   exact = {1-stats.poisson(mu_p).cdf(200):.6f}")
put("pr_call_err_ratio",
    abs(float(1 - Phi((200 - mu_p) / sd_p)) - float(1 - stats.poisson(mu_p).cdf(200)))
    / abs(float(1 - Phi((200.5 - mu_p) / sd_p)) - float(1 - stats.poisson(mu_p).cdf(200))))
print(f"         correction improves the error by {R['pr_call_err_ratio']:.1f}x")

# =====================================================================
print("=" * 70)
with open("computes/g6_s2.json", "w", encoding="utf-8") as fh:
    json.dump(R, fh, indent=1, default=float)
print(f"wrote computes/g6_s2.json  ({len(R)} keys)")
