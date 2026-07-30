# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy"]
# ///
"""G3 §5 (synthesis + rec10 checkpoint) — every number in fragments/g3_s5.html.

Closed forms quoted in the cheatsheet are each checked a second way: continuous
moments by numerical quadrature (scipy.integrate.quad), discrete/combinatorial
answers by exact Fraction arithmetic, symbolic identities in p by evaluation on a
grid of p values.

Run:  uv run computes/g3_s5.py
"""
import io
import json
import sys
from fractions import Fraction as F

import numpy as np
from scipy import integrate, stats

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

R = {}
TOL = 1e-9


def check(name, a, b, tol=TOL):
    ok = abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b)))
    print(f"    [{'OK ' if ok else 'FAIL'}] {name}: {float(a):.12g} vs {float(b):.12g}")
    if not ok:
        raise SystemExit(f"MISMATCH in {name}")
    return float(a)


def moments(pdf, lo, hi):
    """(total mass, mean, second moment, variance) of a density by quadrature."""
    m0 = integrate.quad(pdf, lo, hi, limit=400)[0]
    m1 = integrate.quad(lambda x: x * pdf(x), lo, hi, limit=400)[0]
    m2 = integrate.quad(lambda x: x * x * pdf(x), lo, hi, limit=400)[0]
    return m0, m1, m2, m2 - m1 * m1


print("=" * 74)
print("1. THE CONTINUOUS ZOO — closed form vs quadrature")
print("=" * 74)

# ---- uniform on [a,b]: a=2, b=7 (L08 slide 3; B&T 3.1) ---------------------
a, b = 2.0, 7.0
m0, m1, m2, v = moments(lambda x: 1.0 / (b - a), a, b)
print(f"  Uniform[{a},{b}]  mass={m0:.12f}")
check("uniform mean", m1, (a + b) / 2)
check("uniform var", v, (b - a) ** 2 / 12)
R["uniform"] = {"a": a, "b": b, "density": 1 / (b - a), "mean": (a + b) / 2,
                "var": (b - a) ** 2 / 12, "mass": m0}

# unit uniform, and the >1 density example U[0,1/2]
check("U[0,1/2] density", 1 / 0.5, 2.0)
check("U[0,1/2] mass", integrate.quad(lambda x: 2.0, 0, 0.5)[0], 1.0)
R["u_half_density"] = 2.0

# ---- exponential(lam): lam = 2 (B&T 3.2; rec08 P3) -------------------------
lam = 2.0
m0, m1, m2, v = moments(lambda x: lam * np.exp(-lam * x), 0, np.inf)
print(f"  Exponential(lam={lam})  mass={m0:.12f}")
check("exp mean", m1, 1 / lam)
check("exp var", v, 1 / lam ** 2)
check("exp P(X>1)", integrate.quad(lambda x: lam * np.exp(-lam * x), 1, np.inf)[0],
      np.exp(-lam))
check("exp median", np.log(2) / lam, stats.expon(scale=1 / lam).median())
R["exponential"] = {"lam": lam, "mean": 1 / lam, "var": 1 / lam ** 2,
                    "P_gt_1": float(np.exp(-lam)), "median": float(np.log(2) / lam),
                    "mass": m0}

# ---- normal N(mu, sigma^2): mu = 2, sigma^2 = 16 (L08 slides 6-7) ----------
mu, sig = 2.0, 4.0


def npdf(x, mu=mu, sig=sig):
    return np.exp(-((x - mu) ** 2) / (2 * sig ** 2)) / (sig * np.sqrt(2 * np.pi))


m0, m1, m2, v = moments(npdf, -np.inf, np.inf)
print(f"  Normal(mu={mu}, sigma^2={sig**2})  mass={m0:.12f}")
check("normal mean", m1, mu)
check("normal var", v, sig ** 2)
phi025 = stats.norm.cdf(0.25)
check("Phi(0.25) vs slide table .5987", round(phi025, 4), 0.5987)
p_x_le_3 = stats.norm.cdf(3, loc=mu, scale=sig)
check("P(X<=3), X~N(2,16)", p_x_le_3, phi025)
R["normal"] = {"mu": mu, "sigma": sig, "mean": m1, "var": v,
               "Phi_0_25": float(phi025), "P_X_le_3": float(p_x_le_3),
               "peak_height_sigma_0_1": float(1 / (0.1 * np.sqrt(2 * np.pi)))}
print(f"  N(0,0.1^2) peak height = {R['normal']['peak_height_sigma_0_1']:.6f}  (>1)")

# ---- beta(alpha,beta) (rec11 P2 posterior; B&T 3.6) -----------------------
for al, be in [(2, 1), (1, 1), (2, 3), (3, 2)]:
    def bpdf(q, al=al, be=be):
        return stats.beta.pdf(q, al, be)
    m0, m1, m2, v = moments(bpdf, 0, 1)
    mean_cf = al / (al + be)
    var_cf = al * be / ((al + be) ** 2 * (al + be + 1))
    print(f"  Beta({al},{be})  mass={m0:.12f}")
    check(f"beta({al},{be}) mean", m1, mean_cf)
    check(f"beta({al},{be}) var", v, var_cf)
R["beta_2_1"] = {"pdf": "2q on [0,1]", "mean": 2 / 3, "var": 2 * 1 / (9 * 4)}
print(f"  Beta(2,1): mean=2/3={2/3:.6f}, var={R['beta_2_1']['var']:.6f}")

print()
print("=" * 74)
print("2. DERIVED-DISTRIBUTION METHOD TABLE — worked checks")
print("=" * 74)

# ---- CDF method: X ~ U[0,2], Y = X^3  (L10 slide 6) ------------------------
fY = lambda y: 1.0 / (6.0 * y ** (2.0 / 3.0))
m0, m1, m2, v = moments(fY, 0, 8)
print(f"  Y=X^3, X~U[0,2]: mass={m0:.12f}")
check("E[Y] via f_Y", m1, integrate.quad(lambda x: x ** 3 * 0.5, 0, 2)[0])
check("E[Y] closed form (=2)", m1, 2.0)
R["cube"] = {"mass": m0, "mean": m1, "fY_at_1": fY(1.0), "fY_at_8": fY(8.0)}
print(f"    f_Y(1)={fY(1.0):.6f}, f_Y(8)={fY(8.0):.6f}")

# ---- monotonic formula: Joan, T = 200/V, V ~ U[30,60] (L10 slide 7) --------
fT = lambda t: 200.0 / (30.0 * t * t)
lo_t, hi_t = 200 / 60, 200 / 30
m0, m1, m2, v = moments(fT, lo_t, hi_t)
print(f"  T=200/V, V~U[30,60]: support [{lo_t:.6f},{hi_t:.6f}] mass={m0:.12f}")
check("E[T] direct", m1, integrate.quad(lambda v: (200 / v) / 30, 30, 60)[0])
check("E[T] closed form (20/3)ln2", m1, (20.0 / 3.0) * np.log(2))
print(f"    E[T]={m1:.6f} h  vs 200/E[V]=200/45={200/45:.6f} h  (Jensen gap"
      f" {m1-200/45:.6f})")
R["joan"] = {"lo": lo_t, "hi": hi_t, "mass": m0, "ET": m1, "naive": 200 / 45,
             "fT_lo": fT(lo_t), "fT_hi": fT(hi_t)}

# ---- linear formula: Y = aX+b for normal (L10 slide 8) --------------------
aa, bb = -3.0, 5.0
g = lambda y: npdf((y - bb) / aa) / abs(aa)
m0, m1, m2, v = moments(g, -np.inf, np.inf)
check("aX+b mass", m0, 1.0)
check("aX+b mean", m1, aa * mu + bb)
check("aX+b var", v, aa ** 2 * sig ** 2)
R["linear"] = {"a": aa, "b": bb, "mean": aa * mu + bb, "var": aa ** 2 * sig ** 2}

# ---- convolution: sum of two independent U[0,1] --------------------------
def tri(w):
    return w if 0 <= w <= 1 else (2 - w if 1 < w <= 2 else 0.0)


conv = lambda w: integrate.quad(lambda x: 1.0 * (0 <= x <= 1) * (0 <= w - x <= 1),
                                0, 1)[0]
for w in (0.3, 1.0, 1.5):
    check(f"convolution f_W({w})", conv(w), tri(w), tol=1e-6)
m0, m1, m2, v = moments(tri, 0, 2)
check("triangular mass", m0, 1.0)
check("triangular mean", m1, 1.0)
check("triangular var", v, 2 * (1 / 12))
R["conv_unif"] = {"mass": m0, "mean": m1, "var": v}
print(f"  U[0,1]+U[0,1]: mean={m1:.6f}, var={v:.9f} = 2/12")

# ---- convolution of normals (L11 slide 6) --------------------------------
sx, sy = 1.5, 2.0
cn = lambda w: integrate.quad(
    lambda x: npdf(x, 0, sx) * npdf(w - x, 0, sy), -np.inf, np.inf, limit=400)[0]
for w in (0.0, 1.0, 3.0):
    check(f"normal conv at w={w}", cn(w), npdf(w, 0.0, np.sqrt(sx ** 2 + sy ** 2)))
R["normal_conv_sd"] = float(np.sqrt(sx ** 2 + sy ** 2))
print(f"  N(0,{sx**2})+N(0,{sy**2}) = N(0,{sx**2+sy**2}), sd={R['normal_conv_sd']:.6f}")

print()
print("=" * 74)
print("3. GOTCHA NUMBERS")
print("=" * 74)

# triangle joint pdf (rec09 P3): uniform on {0<=x<=1, 0<=y<=x}, f=2
fx = lambda x: 2 * x          # marginal of X on [0,1]
fy = lambda y: 2 * (1 - y)    # marginal of Y on [0,1]
check("triangle marginal X mass", integrate.quad(fx, 0, 1)[0], 1.0)
check("triangle marginal Y mass", integrate.quad(fy, 0, 1)[0], 1.0)
prod = fx(0.2) * fy(0.8)
print(f"  at (x,y)=(0.2,0.8): f_XY=0 (outside support) but f_X f_Y = "
      f"{fx(0.2):.3f}*{fy(0.8):.3f} = {prod:.3f}  -> not independent")
check("triangle E[X]", integrate.quad(lambda x: x * fx(x), 0, 1)[0], 2 / 3)
check("triangle E[Y]", integrate.quad(lambda y: y * fy(y), 0, 1)[0], 1 / 3)
R["triangle"] = {"fX_02": fx(0.2), "fY_08": fy(0.8), "product": prod,
                 "EX": 2 / 3, "EY": 1 / 3}

# forgetting |dg/dx|: Y = X^2 for X ~ U[0,1]
right = lambda y: 1.0 / (2 * np.sqrt(y))
check("Y=X^2 correct mass", integrate.quad(right, 0, 1)[0], 1.0)
wrong_mass = integrate.quad(lambda y: 1.0, 0, 1)[0]  # naive f_Y(y)=f_X(sqrt y)=1
print(f"  Y=X^2, X~U[0,1]: correct f_Y(y)=1/(2 sqrt y), mass=1; naive f_X(sqrt y)=1 "
      f"has mass {wrong_mass} on [0,1] but wrong shape: f_Y(0.01)="
      f"{right(0.01):.3f} vs naive 1")
check("Y=X^2 E[Y] via f_Y", integrate.quad(lambda y: y * right(y), 0, 1)[0], 1 / 3)
R["sq"] = {"fY_001": right(0.01), "EY": 1 / 3}

print()
print("=" * 74)
print("4. rec10 PROBLEM 1 — true/false identities, all options")
print("=" * 74)

# 1.1(b): var(X) vs var(2X)
Xs, Ps = [0, 1], [F(1, 2), F(1, 2)]
mX = sum(x * p for x, p in zip(Xs, Ps))
vX = sum((x - mX) ** 2 * p for x, p in zip(Xs, Ps))
print(f"  1.1(b) Bernoulli(1/2): var(X)={vX}, var(2X)=4var(X)={4*vX} -> never smaller")
# 1.1(d) counterexample: Omega={1,2}, A={1,2}, B={2}
PA, PB, PAB = F(1), F(1, 2), F(1, 2)
print(f"  1.1(d) A=Omega,B={{2}}: A^c∩B^c=∅, P(A∩B)={PAB}, P(A)P(B)={PA*PB} — here equal;")
# a real counterexample needs P(A),P(B)<1
PA2, PB2 = F(2, 3), F(2, 3)   # A={1,2},B={2,3} on uniform {1,2,3}
PAB2 = F(1, 3)
print(f"       uniform on {{1,2,3}}, A={{1,2}}, B={{2,3}}: A^c∩B^c={{3}}∩{{1}}=∅, "
      f"P(A∩B)={PAB2} but P(A)P(B)={PA2*PB2} -> (d) false")
# 1.1(e): A=B with P=0.6
print(f"  1.1(e) A=B with P(A)=P(B)=3/5: P(A∪B)={F(3,5)} ≠ 1 -> false")
# 1.2(a): E[X]=0 but P(X>0) != P(X<0)
Xs2, Ps2 = [-1, 2], [F(2, 3), F(1, 3)]
m = sum(x * p for x, p in zip(Xs2, Ps2))
print(f"  1.2(a) X=-1 w.p. 2/3, X=2 w.p. 1/3: E[X]={m}, P(X>0)={Ps2[1]}, "
      f"P(X<0)={Ps2[0]} -> false")
# 1.2(b),(c),(d) with A=B, P(A)=1/2
print(f"  1.2(b) A=B, P(A)=1/2: P(A|B)+P(A|B^c)=1+0=1 ≠ P(A)=1/2 -> false")
print(f"  1.2(c) A=B, P(A)=1/2: P(B|A)+P(B|A^c)=1+0=1  (holds here) but with "
      f"B=Omega: 1+1=2 ≠ 1 -> false in general")
print(f"  1.2(d) B=Omega: P(B|A)+P(B^c|A^c)=1+0=1 (holds) but B=∅: 0+1=1 ... "
      f"use A,B independent with P(B)=1/3: 1/3+2/3=1 (holds); "
      f"take P(B|A)=1/4, P(B^c|A^c)=1/4 -> sum 1/2 ≠ 1")
R["p1"] = {"varX": float(vX), "var2X": float(4 * vX)}

# explicit 1.2(d) counterexample by construction on a 4-point space
# P(A)=1/2; P(B|A)=1/4 ; P(B|A^c)=3/4  => P(B^c|A^c)=1/4 ; sum = 1/2
s = F(1, 4) + F(1, 4)
print(f"       explicit: P(A)=1/2, P(B|A)=1/4, P(B|A^c)=3/4 -> "
      f"P(B|A)+P(B^c|A^c)={s} ≠ 1 -> (d) false")
R["p1_d_sum"] = float(s)

print()
print("=" * 74)
print("5. rec10 PROBLEM 2 — Heather / Taylor unfair coin")
print("=" * 74)

outcomes = {
    "HH": lambda p: p ** 2,
    "HTH": lambda p: p ** 2 * (1 - p),
    "HTT": lambda p: p * (1 - p) ** 2,
    "THH": lambda p: p ** 2 * (1 - p),
    "THT": lambda p: p * (1 - p) ** 2,
    "TT": lambda p: (1 - p) ** 2,
}
heather = ["HH", "HTH", "THH"]
for p in [F(1, 2), F(1, 3), F(3, 4), F(1, 5)]:
    tot = sum(f(p) for f in outcomes.values())
    ph = sum(outcomes[o](p) for o in heather)
    cond1 = sum(outcomes[o](p) for o in ["HH", "HTH"]) / p
    cond2 = sum(outcomes[o](p) for o in ["HH", "HTH"]) / ph
    assert tot == 1, tot
    assert ph == p ** 2 * (3 - 2 * p)
    assert cond1 == p * (2 - p)
    assert cond2 == (2 - p) / (3 - 2 * p)
    print(f"  p={p}: sum={tot}  P(H wins)={ph}={float(ph):.6f}  "
          f"P(H|1st H)={cond1}  P(1st H|H wins)={cond2}")
p = F(1, 2)
R["p2"] = {"p": 0.5,
           "P_heather": float(F(1, 2)),
           "P_H_given_firstH": float(p * (2 - p)),
           "P_firstH_given_H": float((2 - p) / (3 - 2 * p))}
# Taylor-side practice: P(1st toss T | Taylor wins) = (1+p)/(1+2p)
for p in [F(1, 2), F(1, 3), F(2, 5)]:
    q = 1 - p
    taylor = ["TT", "THT", "HTT"]
    pt = sum(outcomes[o](p) for o in taylor)
    num = sum(outcomes[o](p) for o in ["TT", "THT"])
    assert pt == q ** 2 * (3 - 2 * q), (pt, q ** 2 * (3 - 2 * q))
    assert num / pt == (1 + p) / (1 + 2 * p), (num / pt, (1 + p) / (1 + 2 * p))
    print(f"  p={p}: P(Taylor wins)={pt}  P(1st T | Taylor wins)={num/pt}")
R["p2_practice"] = {"p": 0.5, "P_taylor": float(F(1, 2)),
                    "P_firstT_given_T": float(F(3, 4))}

print()
print("=" * 74)
print("6. rec10 PROBLEM 3 — 4-sided-die casino game")
print("=" * 74)

space = {(1,): (F(1, 4), 1), (2,): (F(1, 4), 2), (3,): (F(1, 4), 3),
         (4, 1): (F(1, 16), 3), (4, 2): (F(1, 16), 4),
         (4, 3): (F(1, 16), 5), (4, 4): (F(1, 16), 6)}
assert sum(pr for pr, _ in space.values()) == 1
pmf = {}
for om, (pr, x) in space.items():
    pmf[x] = pmf.get(x, F(0)) + pr
print("  PMF of X:", {k: str(v) for k, v in sorted(pmf.items())})
assert pmf == {1: F(1, 4), 2: F(1, 4), 3: F(5, 16), 4: F(1, 16),
               5: F(1, 16), 6: F(1, 16)}
EX = sum(x * pr for x, pr in pmf.items())
EX2 = sum(x * x * pr for x, pr in pmf.items())
varX = EX2 - EX ** 2
print(f"  E[X]={EX}={float(EX):.6f}   E[X^2]={EX2}   var(X)={varX}="
      f"{float(varX):.6f}")
assert EX == F(21, 8)
# total expectation cross-check
tot_exp = F(1, 4) * F(9, 2) + F(3, 4) * 2
check("E[X] total expectation", float(tot_exp), float(EX))
# conditional PMF of first roll Z given B={X=3}
PB = pmf[3]
pz = {3: F(1, 4) / PB, 4: F(1, 16) / PB}
print(f"  P(B)=P(X=3)={PB};  p_Z|B(3)={pz[3]}, p_Z|B(4)={pz[4]}, sum={pz[3]+pz[4]}")
assert pz == {3: F(4, 5), 4: F(1, 5)}
# 3.4 extended game
EN = F(1) / F(3, 4)
EW = 2 * EN - 2
EL = F(2)
EY = EW + EL
print(f"  E[N]={EN}, E[W]={EW}, E[L]={EL}, E[Y]={EY}={float(EY):.6f}")
assert EY == F(8, 3)
# brute-force series check of E[Y]
ser = sum(F(1, 4) ** k * F(3, 4) * (2 * k + 2) for k in range(0, 400))
check("E[Y] by series", float(ser), float(EY), tol=1e-12)
# PMF of Y (truncated) and its mean
pY = {}
for k in range(0, 200):
    for last in (1, 2, 3):
        val = 2 * k + last
        pY[val] = pY.get(val, F(0)) + F(1, 4) ** k * F(1, 4)
mass = sum(pY.values())
meanY = sum(v * pr for v, pr in pY.items())
print(f"  truncated PMF of Y: mass={float(mass):.15f}, mean={float(meanY):.12f}")
R["p3"] = {"EX": float(EX), "EX_frac": "21/8", "varX": float(varX),
           "varX_frac": str(varX), "PB": float(PB), "EY": float(EY),
           "EN": float(EN), "EW": float(EW), "meanY_bruteforce": float(meanY)}

# practice variant: fair 6-sided die, roll 6 pays $3 and continues
ELp = F(1 + 2 + 3 + 4 + 5, 5)
ENp = F(1) / F(5, 6)
EWp = 3 * (ENp - 1)
EYp = EWp + ELp
print(f"  practice (6-sided): E[L]={ELp}, E[N]={ENp}, E[W]={EWp}, E[Y]={EYp}="
      f"{float(EYp):.6f}")
serp = sum(F(1, 6) ** k * F(5, 6) * (3 * k + 3) for k in range(0, 400))
check("practice E[Y] series", float(serp), float(EYp), tol=1e-12)
R["p3_practice"] = {"EL": float(ELp), "EN": float(ENp), "EW": float(EWp),
                    "EY": float(EYp), "EY_frac": str(EYp)}

print()
print("=" * 74)
print("7. PRACTICE-QUESTION NUMBERS")
print("=" * 74)

# P: Y = e^X, X ~ U[0,1]
fYe = lambda y: 1.0 / y
m0, m1, _, _ = moments(fYe, 1, np.e)
check("Y=e^X mass", m0, 1.0)
check("Y=e^X mean", m1, np.e - 1)
print(f"  Y=e^X, X~U[0,1]: support [1,e]=[1,{np.e:.6f}], E[Y]=e-1={np.e-1:.6f}")
R["expY"] = {"e": float(np.e), "mean": float(np.e - 1)}

# P: Y = X^2, X ~ N(0,1)  (chi-square with 1 dof)
f_chi = lambda y: np.exp(-y / 2) / np.sqrt(2 * np.pi * y)
m0, m1, _, v = moments(f_chi, 0, np.inf)
check("chi1 mass", m0, 1.0, tol=1e-7)
check("chi1 mean", m1, 1.0, tol=1e-7)
check("chi1 var", v, 2.0, tol=1e-6)
print(f"  Y=X^2, X~N(0,1): E[Y]=1, var(Y)=2  (mass {m0:.9f})")
R["chi1"] = {"mean": m1, "var": v}

# P: exponential quantities for lam=2 already in R["exponential"]
# P: min of two independent exponentials (rec08 P3)
l1, l2 = 2.0, 3.0
fmin = lambda x: (l1 + l2) * np.exp(-(l1 + l2) * x)
m0, m1, _, _ = moments(fmin, 0, np.inf)
check("min-exp mean", m1, 1 / (l1 + l2))
print(f"  min of Exp(2),Exp(3) ~ Exp(5), mean={1/(l1+l2):.6f}")
R["min_exp"] = {"lam": l1 + l2, "mean": 1 / (l1 + l2)}

# P: normal standardization practice: X~N(5,9), P(2<X<11)
lo_z, hi_z = (2 - 5) / 3, (11 - 5) / 3
pr = stats.norm.cdf(hi_z) - stats.norm.cdf(lo_z)
print(f"  X~N(5,9): P(2<X<11)=Phi({hi_z:.0f})-Phi({lo_z:.0f})="
      f"{stats.norm.cdf(hi_z):.4f}-{stats.norm.cdf(lo_z):.4f}={pr:.4f}")
R["norm_practice"] = {"z_lo": lo_z, "z_hi": hi_z,
                      "Phi_hi": float(stats.norm.cdf(hi_z)),
                      "Phi_lo": float(stats.norm.cdf(lo_z)),
                      "Phi_1": float(stats.norm.cdf(1.0)),
                      "Phi_2": float(stats.norm.cdf(2.0)),
                      "prob": float(pr)}

# P: triangular density f(x)=2x on [0,1]  (= Beta(2,1))
tri21 = lambda x: 2 * x
m0, m1, m2, v = moments(tri21, 0, 1)
check("2x mass", m0, 1.0)
check("2x mean", m1, 2 / 3)
check("2x var", v, 1 / 18)
tail = integrate.quad(tri21, 0.5, 1)[0]
check("2x P(X>1/2)", tail, 3 / 4)
print(f"  f(x)=2x on [0,1]: E={m1:.6f}=2/3, var={v:.6f}=1/18, P(X>1/2)={tail:.4f}")
R["tri21"] = {"mean": m1, "var": v, "tail_half": tail}

# P: uniform[2,7] tail
check("U[2,7] P(X>4)", integrate.quad(lambda x: 0.2, 4, 7)[0], 0.6)
R["uniform"]["P_gt_4"] = 0.6

with open("computes/g3_s5.json", "w", encoding="utf-8") as fh:
    json.dump(R, fh, indent=2)
print("\nwrote computes/g3_s5.json")
