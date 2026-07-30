# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""Numbers for note G3 section 2 - Joint, marginal and conditional PDFs.

Sources: L09 slides 3-8, rec09 P1/P3/P4, B&T 3.4-3.5.
Every numeric value quoted in fragments/g3_s2.html comes from here.
"""
from __future__ import annotations

import json
import sys
from math import exp, log, pi, sin, sqrt
from pathlib import Path

import numpy as np
from scipy import integrate

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

R = {}


def rec(k, v, note=""):
    R[k] = v
    print(f"{k:34s} = {v!r}   {note}")


# ============================================================ 2.1  f(x,y)=x+y
print("\n--- 2.1  running example: f(x,y) = x + y on the unit square ---")
# normalization constant: int int c(x+y) dx dy = c  =>  c = 1
norm, _ = integrate.dblquad(lambda y, x: x + y, 0, 1, 0, 1)
rec("xy_normalization", round(norm, 12), "int int (x+y) = 1  => c = 1")

# P(X + Y <= 1)
p_sum, _ = integrate.dblquad(lambda y, x: x + y, 0, 1, 0, lambda x: 1 - x)
rec("xy_P_sum_le_1", p_sum, "= 1/3")
rec("xy_P_sum_le_1_exact", 1 / 3)

# delta-square check at (0.5,0.5), delta = 0.05
x0 = y0 = 0.5
d = 0.05
exact, _ = integrate.dblquad(lambda y, x: x + y, x0, x0 + d, y0, y0 + d)
approx = (x0 + y0) * d * d
rec("xy_delta", d)
rec("xy_delta_exact", exact, "delta^2 (x0+y0+delta)")
rec("xy_delta_approx", approx, "f(x0,y0) * delta^2")
rec("xy_delta_ratio", exact / approx, "= 1 + delta/(x0+y0) = 1.05")

# marginals, moments
EX, _ = integrate.dblquad(lambda y, x: x * (x + y), 0, 1, 0, 1)
EXY, _ = integrate.dblquad(lambda y, x: x * y * (x + y), 0, 1, 0, 1)
EX2, _ = integrate.dblquad(lambda y, x: x * x * (x + y), 0, 1, 0, 1)
rec("xy_EX", EX, "= 7/12")
rec("xy_EX_exact", 7 / 12)
rec("xy_EXY", EXY, "= 1/3")
rec("xy_EX_times_EY", (7 / 12) ** 2, "= 49/144")
rec("xy_cov", EXY - (7 / 12) ** 2, "= -1/144")
rec("xy_cov_exact", -1 / 144)
rec("xy_EX2", EX2, "= 5/12")
rec("xy_varX", EX2 - EX * EX, "= 5/12 - 49/144 = 11/144")

# conditional mean E[X|Y=y] = (3y+2)/(3(2y+1))
def cond_mean_xy(y):
    num, _ = integrate.quad(lambda x: x * (x + y), 0, 1)
    den, _ = integrate.quad(lambda x: (x + y), 0, 1)
    return num / den


for yv in (0.0, 0.25, 0.5, 0.75, 1.0):
    a = cond_mean_xy(yv)
    b = (3 * yv + 2) / (3 * (2 * yv + 1))
    rec(f"xy_EXgY_{str(yv).replace('.', 'p')}", a, f"closed form {b:.10f}")

tot, _ = integrate.quad(lambda y: ((3 * y + 2) / (3 * (2 * y + 1))) * (y + 0.5), 0, 1)
rec("xy_total_expectation", tot, "int E[X|Y=y] f_Y(y) dy = 7/12")

# ============================================================ 2.4  Buffon
print("\n--- 2.4  Buffon's needle ---")
rec("buffon_f_joint_expr", "4/(pi d)", "= (2/d)*(2/pi)")
for ratio, tag in ((1.0, "1"), (0.5, "0p5"), (0.25, "0p25")):
    rec(f"buffon_p_l_over_d_{tag}", 2 * ratio / pi, f"2*l/(pi d) with l/d = {ratio}")

rng = np.random.default_rng(6041)
N = 4_000_000
dd, ll = 1.0, 0.5
xs = rng.uniform(0, dd / 2, N)
th = rng.uniform(0, pi / 2, N)
hit = xs <= (ll / 2) * np.sin(th)
phat = hit.mean()
rec("buffon_mc_N", N)
rec("buffon_mc_phat", float(phat), "l/d = 0.5, seed 6041")
rec("buffon_mc_exact", 2 * ll / (pi * dd))
rec("buffon_mc_pi_estimate", float(2 * ll / (dd * phat)), "pi ~ 2l/(d phat)")

# integral check of the double integral itself
val, _ = integrate.dblquad(lambda x, t: 4 / (pi * dd), 0, pi / 2,
                           0, lambda t: (ll / 2) * sin(t))
rec("buffon_dblquad", val, "should equal 2l/(pi d)")

# ============================================================ 2.5  stick break
print("\n--- 2.5  stick breaking (L09 slides 7-8), ell = 1 ---")
ell = 1.0
fY = lambda y: (1 / ell) * log(ell / y)
nrm, _ = integrate.quad(fY, 1e-14, ell)
rec("stick_fY_normalization", nrm, "int_0^ell (1/ell) log(ell/y) dy = 1")
EY, _ = integrate.quad(lambda y: y * fY(y), 1e-14, ell)
rec("stick_EY", EY, "= ell/4 = 0.25")
rec("stick_EY_exact", ell / 4)
EY_tot, _ = integrate.quad(lambda x: (x / 2) * (1 / ell), 0, ell)
rec("stick_EY_via_total_expectation", EY_tot, "int (x/2)(1/ell) dx = ell/4")
for yv in (0.05, 0.25, 0.5, 0.75):
    rec(f"stick_fY_at_{str(yv).replace('.', 'p')}", fY(yv))
EY2, _ = integrate.quad(lambda y: y * y * fY(y), 1e-14, ell)
rec("stick_EY2", EY2, "= ell^2/9")
rec("stick_varY", EY2 - EY ** 2, "= 1/9 - 1/16 = 7/144")
rec("stick_varY_exact", 7 / 144)
# conditional mean of X given Y=y for the stick joint: (1-y)/log(1/y)
for yv in (0.1, 0.5, 0.9):
    num, _ = integrate.quad(lambda x: x * (1 / (ell * x)), yv, ell)
    den, _ = integrate.quad(lambda x: (1 / (ell * x)), yv, ell)
    rec(f"stick_EXgY_{str(yv).replace('.', 'p')}", num / den,
        f"closed form {(1 - yv) / log(1 / yv):.10f}")

# ============================================================ 2.6  rec09 P1
print("\n--- 2.6  rec09 P1: exponential in [n, n+1] with n odd ---")


def p_odd(lam):
    return 1.0 / (exp(lam) + 1.0)


for lam in (0.25, 0.5, 1.0, 2.0, 5.0):
    tag = str(lam).replace(".", "p")
    closed = p_odd(lam)
    # brute force: sum over odd n of the CDF difference
    s = 0.0
    for n in range(1, 4000, 2):
        s += exp(-lam * n) * (1 - exp(-lam))
    rec(f"p1_lam{tag}_closed", closed)
    rec(f"p1_lam{tag}_bruteforce", s, "sum over odd n up to 3999")
    rec(f"p1_lam{tag}_even", 1 - closed, "complement = even n incl. 0")

rec("p1_limit_lam_to_0", 0.5, "1/(e^0+1) = 1/2")
rec("p1_interval_lam1_n1", exp(-1.0) * (1 - exp(-1.0)), "P(1<=X<=2), lambda=1")
rec("p1_interval_lam1_n3", exp(-3.0) * (1 - exp(-1.0)), "P(3<=X<=4), lambda=1")
rec("p1_interval_lam1_n5", exp(-5.0) * (1 - exp(-1.0)), "P(5<=X<=6), lambda=1")
rng2 = np.random.default_rng(41)
M = 4_000_000
sample = rng2.exponential(1.0, M)  # lambda = 1
n_floor = np.floor(sample).astype(int)
rec("p1_mc_lam1", float((n_floor % 2 == 1).mean()), "MC, lambda=1, seed 41")

# ============================================================ 2.7  rec09 P3
print("\n--- 2.7  rec09 P3: uniform on the triangle (0,0),(0,1),(1,0) ---")
rec("p3_area", 0.5)
rec("p3_f_joint", 2.0, "1/area")
tot3, _ = integrate.dblquad(lambda y, x: 2.0, 0, 1, 0, lambda x: 1 - x)
rec("p3_normalization", tot3)
for yv in (0.0, 0.25, 0.5, 0.75):
    rec(f"p3_fY_{str(yv).replace('.', 'p')}", 2 * (1 - yv))
    rec(f"p3_EXgY_{str(yv).replace('.', 'p')}", (1 - yv) / 2)
EX3, _ = integrate.quad(lambda x: x * 2 * (1 - x), 0, 1)
EY3, _ = integrate.quad(lambda y: y * 2 * (1 - y), 0, 1)
rec("p3_EX", EX3, "= 1/3")
rec("p3_EY", EY3, "= 1/3")
tot_exp3, _ = integrate.quad(lambda y: ((1 - y) / 2) * 2 * (1 - y), 0, 1)
rec("p3_EX_via_total_expectation", tot_exp3, "int (1-y)/2 * 2(1-y) dy = 1/3")
EX3_2, _ = integrate.quad(lambda x: x * x * 2 * (1 - x), 0, 1)
rec("p3_EX2", EX3_2, "= 1/6")
rec("p3_varX", EX3_2 - EX3 ** 2, "= 1/6 - 1/9 = 1/18")
EXY3, _ = integrate.dblquad(lambda y, x: x * y * 2.0, 0, 1, 0, lambda x: 1 - x)
rec("p3_EXY", EXY3, "= 1/12")
rec("p3_cov", EXY3 - EX3 * EY3, "= 1/12 - 1/9 = -1/36")

# ============================================================ 2.8  rec09 P4
print("\n--- 2.8  rec09 P4: broken stick forms a triangle ---")
rec("p4_answer", 0.25)
rng3 = np.random.default_rng(322)
K = 4_000_000
u = rng3.random(K)
v = rng3.random(K)
lo = np.minimum(u, v)
hi = np.maximum(u, v)
a, b, c = lo, hi - lo, 1 - hi
ok = (a < 0.5) & (b < 0.5) & (c < 0.5)
rec("p4_mc_N", K)
rec("p4_mc", float(ok.mean()), "seed 322")
# practice: every piece at least alpha
for al in (0.2, 0.25, 0.1):
    tag = str(al).replace(".", "p")
    ok2 = (a >= al) & (b >= al) & (c >= al)
    rec(f"p4_all_ge_{tag}_formula", (1 - 3 * al) ** 2)
    rec(f"p4_all_ge_{tag}_mc", float(ok2.mean()))
# practice: sequential stick breaking, break left piece
rec("p4_seq_answer", log(2) - 0.5, "ln 2 - 1/2")
seq, _ = integrate.quad(lambda x: (1 - x) / x, 0.5, 1.0)
rec("p4_seq_integral", seq)
X = rng3.random(K)
Y = rng3.random(K) * X
p1_, p2_, p3_ = Y, X - Y, 1 - X
okseq = (p1_ < 0.5) & (p2_ < 0.5) & (p3_ < 0.5)
rec("p4_seq_mc", float(okseq.mean()), "seed 322")

# ============================================================ widget checks
print("\n--- widget: conditional slice explorer, spot checks ---")
W = {}
for yv in (0.2, 0.5, 0.8):
    W[f"tri_y{yv}"] = {"height": 1 / (1 - yv), "xmax": 1 - yv, "EX": (1 - yv) / 2}
    W[f"sq_y{yv}"] = {"peak": (1 + yv) / (yv + 0.5),
                      "EX": (3 * yv + 2) / (3 * (2 * yv + 1))}
    W[f"stick_y{yv}"] = {"height_at_y": (1 / yv) / log(1 / yv),
                         "EX": (1 - yv) / log(1 / yv)}
    # numeric confirmation of each conditional mean
    m1, _ = integrate.quad(lambda x: x / (1 - yv), 0, 1 - yv)
    m2n, _ = integrate.quad(lambda x: x * (x + yv), 0, 1)
    m2d, _ = integrate.quad(lambda x: (x + yv), 0, 1)
    m3n, _ = integrate.quad(lambda x: x * (1 / x), yv, 1)
    m3d, _ = integrate.quad(lambda x: (1 / x), yv, 1)
    W[f"tri_y{yv}"]["EX_num"] = m1
    W[f"sq_y{yv}"]["EX_num"] = m2n / m2d
    W[f"stick_y{yv}"]["EX_num"] = m3n / m3d
    print(f"  y={yv}: tri {m1:.8f} vs {(1-yv)/2:.8f} | "
          f"sq {m2n/m2d:.8f} vs {(3*yv+2)/(3*(2*yv+1)):.8f} | "
          f"stick {m3n/m3d:.8f} vs {(1-yv)/log(1/yv):.8f}")
R["widget_checks"] = W

# ============================================================ practice extras
print("\n--- practice question numbers ---")
# Practice: f(x,y)=x+y, P(X > 1/2, Y < 1/2)
pq1, _ = integrate.dblquad(lambda y, x: x + y, 0.5, 1, 0, 0.5)
rec("pq_xy_quadrant", pq1, "P(X>1/2, Y<1/2) = 1/4")
rec("pq_xy_quadrant_exact", 1 / 4)
# Practice: uniform on unit disk of radius 1 -> marginal
rec("pq_disk_f", 1 / pi)
pq_dm, _ = integrate.quad(lambda x: (2 / pi) * sqrt(1 - x * x) * x * x, -1, 1)
rec("pq_disk_EX2", pq_dm, "= 1/4")
# Practice: independent exponentials, P(X < Y)
rec("pq_expo_PXlY", 1.0 / (1 + 2.0), "lam_X/(lam_X+lam_Y) with lam_X=1, lam_Y=2 = 1/3")
pq_e, _ = integrate.dblquad(lambda y, x: 1 * exp(-x) * 2 * exp(-2 * y),
                            0, 50, lambda x: x, 50)
rec("pq_expo_PXlY_num", pq_e, "P(X<Y) with lam_X=1, lam_Y=2 = 1/3")
# Practice: Buffon with l = d (needle exactly the line spacing)
rec("pq_buffon_l_eq_d", 2 / pi)
# Practice: rec09 P1 with lambda = ln 2
rec("pq_p1_lam_ln2", 1 / (exp(log(2)) + 1), "lambda = ln 2 -> 1/3")

OUT = Path(__file__).resolve().parent / "g3_s2.json"
OUT.write_text(json.dumps(R, indent=1, default=float), encoding="utf-8")
print("\nwrote", OUT, "with", len(R), "keys")
